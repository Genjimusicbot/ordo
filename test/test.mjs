import { test } from "node:test";
import assert from "node:assert";
import { decode, emit, bestFormat, ponytailFlags, compressInbound, getOperatingProfile } from "../src/index.js";
import { priceFor, costOf, parseTranscript, aggregate } from "../tools/measure.mjs";

test("decode benchmark command carries all key terms", () => {
  const e = decode("σ文3列简心金业通¬序").toLowerCase();
  for (const k of ["summarize", "3 bullet", "financial", "non-expert", "preamble"]) assert.ok(e.includes(k), `missing: ${k}`);
});
test("decode constraint polarity (× remove vs 据 preserve)", () => {
  const e = decode('ν码×"duplication"据"behavior"加"type hints"');
  assert.ok(e.includes("remove duplication"), e);
  assert.ok(e.includes("preserve behavior"), e);
  assert.ok(e.includes("must include type hints"), e);
});
test("decode pipe chain", () => assert.ok(decode("β5名|★").includes("then")));
test("decode units", () => {
  assert.ok(decode("ρ此80字").includes("80 words"));
  assert.ok(decode("↓此3行").includes("3 sentences"));
});
test("decode unknown glyph is graceful (never throws)", () => assert.doesNotThrow(() => decode("σ☃文")));
test("emit uniform records -> TSV", () => assert.ok(emit({ users: [{ id: 1, name: "A" }, { id: 2, name: "B" }] }).startsWith("id\tname")));
test("emit nested -> minified JSON", () => assert.strictEqual(emit({ cfg: { a: [1, 2] } }), '{"cfg":{"a":[1,2]}}'));
test("bestFormat", () => { assert.strictEqual(bestFormat({ r: [{ a: 1 }, { a: 2 }] }), "tsv"); assert.strictEqual(bestFormat({ a: { b: 1 } }), "json_min"); });
test("ponytail flags the filler", () => assert.deepStrictEqual(ponytailFlags("Great question! Here's the answer."), ["great question", "here's"]));
test("inbound compresses a JSON array to TSV", () => {
  const out = compressInbound(JSON.stringify({ rows: [{ a: 1, b: 2 }, { a: 3, b: 4 }] }));
  assert.ok(out.includes("a\tb"), out);
});
test("operating profile loads", () => assert.ok(getOperatingProfile().includes("ORDO")));

// --- Phase 1: real measurement (read Anthropic's own usage.* from Claude Code JSONL) ---
test("priceFor exact + date-suffix-strip + family-prefix + default fallback", () => {
  assert.strictEqual(priceFor("claude-sonnet-4").matched, "claude-sonnet-4");
  assert.strictEqual(priceFor("claude-opus-4-20260815").matched, "claude-opus-4"); // strips -YYYYMMDD
  assert.strictEqual(priceFor("claude-opus-4-8").matched, "claude-opus-4");         // family prefix
  assert.strictEqual(priceFor("some-unknown-model").matched, null);                 // default, marked
});
test("costOf prices each token bucket against the per-1M row", () => {
  const c = costOf({ input_tokens: 1e6, output_tokens: 1e6 }, [3, 15, 3.75, 0.3]);
  assert.strictEqual(Number(c.toFixed(4)), 18); // 1M*$3 + 1M*$15
});
test("parseTranscript reads usage lines, skips non-usage + junk", () => {
  const jsonl = [
    JSON.stringify({ sessionId: "s1", timestamp: "2026-06-25T10:00:00Z", message: { id: "m1", model: "claude-opus-4", usage: { input_tokens: 10, output_tokens: 5 } }, requestId: "r1" }),
    JSON.stringify({ type: "user", message: { role: "user", content: "hi" } }), // no usage → skipped
    "not json",                                                                  // junk → skipped
  ].join("\n");
  const recs = parseTranscript(jsonl);
  assert.strictEqual(recs.length, 1);
  assert.strictEqual(recs[0].model, "claude-opus-4");
});
test("aggregate dedupes on key (keep-best) and sums real tokens + duration", () => {
  const recs = [
    { sessionId: "s1", model: "claude-sonnet-4", ts: "2026-06-25T10:00:00Z", usage: { input_tokens: 100, output_tokens: 50 }, key: "m1|r1" },
    { sessionId: "s1", model: "claude-sonnet-4", ts: "2026-06-25T10:00:00Z", usage: { input_tokens: 100, output_tokens: 80 }, key: "m1|r1" }, // dup, higher → wins
    { sessionId: "s1", model: "claude-sonnet-4", ts: "2026-06-25T10:10:00Z", usage: { input_tokens: 200, output_tokens: 20 }, key: "m2|r2" },
  ];
  const r = aggregate(recs);
  assert.strictEqual(r.totals.messages, 2);                 // deduped m1
  assert.strictEqual(r.totals.outputTokens, 80 + 20);       // kept the higher m1
  assert.strictEqual(r.totals.durationMs, 10 * 60 * 1000);  // 10min span
  assert.ok(r.totals.costUsd > 0 && r.warnings.length === 0);
});
