import { test } from "node:test";
import assert from "node:assert";
import { decode, emit, bestFormat, ponytailFlags, compressInbound, getOperatingProfile } from "../src/index.js";

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
