// ORDO measure — turn Claude Code's own session logs into a REAL token + $ + duration meter.
//
// Read-only. The billed token counts already sit in ~/.claude/projects/**/*.jsonl — Anthropic writes
// `message.usage.*` per assistant message — so we read, dedupe, and price them. No re-tokenization,
// lossless: these are the actual billed figures, not a proxy. Use it for an A/B: run a task corpus with
// the ORDO profile ON vs OFF and diff the totals → the real dollar/token delta ORDO saves.
//
// Honesty: prices are RETAIL per-token (LiteLLM-style). For Max-plan subscription users they are
// DIRECTIONAL — correct for an ORDO-on-vs-off A/B delta, wrong for absolute spend. Unpriced models WARN
// and fall back (never silently zeroed). Pure functions are exported so the logic is tested without logs.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

// $/1M tokens: [input, output, cache-write-5m, cache-read]. Keyed by model family; the fallback chain
// (exact → strip date/version suffix → family-prefix → default) handles new dated snapshots.
export const PRICES = {
  "claude-opus-4": [15, 75, 18.75, 1.5],
  "claude-sonnet-4": [3, 15, 3.75, 0.3],
  "claude-haiku-4": [1, 5, 1.25, 0.1],
  "claude-3-5-sonnet": [3, 15, 3.75, 0.3],
  "claude-3-5-haiku": [0.8, 4, 1, 0.08],
  "claude-3-opus": [15, 75, 18.75, 1.5],
  "gpt-4o": [2.5, 10, 0, 1.25],
  "gpt-4o-mini": [0.15, 0.6, 0, 0.075],
};
const DEFAULT_PRICE = [3, 15, 3.75, 0.3]; // sonnet-class fallback; WARN-and-mark whenever it is used

/** Resolve a model id to a price row via the fallback chain. matched=null means the default was used. */
export function priceFor(model) {
  if (!model) return { price: DEFAULT_PRICE, matched: null };
  const m = String(model).toLowerCase();
  if (PRICES[m]) return { price: PRICES[m], matched: m };
  const stripped = m.replace(/-(\d{8}|\d{6}|latest|v\d+)$/, ""); // drop -YYYYMMDD / -latest / -vN
  if (PRICES[stripped]) return { price: PRICES[stripped], matched: stripped };
  for (const k of Object.keys(PRICES).sort((a, b) => b.length - a.length)) {
    if (m.startsWith(k) || stripped.startsWith(k)) return { price: PRICES[k], matched: k };
  }
  return { price: DEFAULT_PRICE, matched: null };
}

const tot = (u) => (u?.input_tokens || 0) + (u?.output_tokens || 0) +
  (u?.cache_creation_input_tokens || 0) + (u?.cache_read_input_tokens || 0);

/** USD cost of one usage block against a per-1M [in,out,cacheW,cacheR] price row. */
export function costOf(usage, price) {
  const [pi, po, pcw, pcr] = price; const u = usage || {};
  return ((u.input_tokens || 0) * pi + (u.output_tokens || 0) * po +
    (u.cache_creation_input_tokens || 0) * pcw + (u.cache_read_input_tokens || 0) * pcr) / 1e6;
}

/** Parse one JSONL transcript → [{sessionId, model, ts, usage, key}] for assistant lines carrying usage. */
export function parseTranscript(text, sessionFallback = "?") {
  const out = [];
  for (const line of text.split("\n")) {
    const s = line.trim(); if (!s) continue;
    let o; try { o = JSON.parse(s); } catch { continue; }
    const msg = o.message || o;
    if (!msg || !msg.usage) continue;
    const id = msg.id || ""; const req = o.requestId || "";
    const key = (id || req) ? `${id}|${req}` : (o.uuid || `${out.length}`); // unkeyed events never merge
    out.push({ sessionId: o.sessionId || sessionFallback, model: msg.model || o.model || null, ts: o.timestamp || null, usage: msg.usage, key });
  }
  return out;
}

/** Dedupe on key (keep-best = highest total tokens), then aggregate per-session + overall + price. */
export function aggregate(records) {
  const seen = new Map();
  for (const r of records) {
    const prev = seen.get(r.key);
    if (!prev || tot(r.usage) > tot(prev.usage)) seen.set(r.key, r);
  }
  const sessions = new Map(); const warnings = new Set();
  let tIn = 0, tOut = 0, tCW = 0, tCR = 0, cost = 0, minTs = null, maxTs = null, defaultTokens = 0;
  for (const r of seen.values()) {
    const { price, matched } = priceFor(r.model);
    if (!matched) { warnings.add(r.model || "(no model field)"); defaultTokens += tot(r.usage); }
    const c = costOf(r.usage, price); const u = r.usage;
    tIn += u.input_tokens || 0; tOut += u.output_tokens || 0;
    tCW += u.cache_creation_input_tokens || 0; tCR += u.cache_read_input_tokens || 0; cost += c;
    if (r.ts) { const t = Date.parse(r.ts); if (!isNaN(t)) { if (minTs === null || t < minTs) minTs = t; if (maxTs === null || t > maxTs) maxTs = t; } }
    const ss = sessions.get(r.sessionId) || { sessionId: r.sessionId, msgs: 0, tokens: 0, costUsd: 0, model: r.model };
    ss.msgs++; ss.tokens += tot(u); ss.costUsd += c; sessions.set(r.sessionId, ss);
  }
  return {
    sessions: [...sessions.values()].sort((a, b) => b.costUsd - a.costUsd),
    totals: { messages: seen.size, inputTokens: tIn, outputTokens: tOut, cacheWriteTokens: tCW,
      cacheReadTokens: tCR, totalTokens: tIn + tOut + tCW + tCR, costUsd: cost,
      defaultTokens, defaultPct: Math.round(100 * defaultTokens / Math.max(tIn + tOut + tCW + tCR, 1)),
      durationMs: (minTs !== null && maxTs !== null) ? maxTs - minTs : null },
    warnings: [...warnings],
  };
}

/** Walk the Claude Code projects tree (every .jsonl, recursively) or a given dir, and aggregate. Read-only. */
export function measure(dir) {
  const base = dir || join(process.env.CLAUDE_CONFIG_DIR || join(homedir(), ".claude"), "projects");
  const records = [];
  const walk = (d) => {
    let entries; try { entries = readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const e of entries) {
      const p = join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith(".jsonl")) { try { records.push(...parseTranscript(readFileSync(p, "utf8"), e.name.replace(/\.jsonl$/, ""))); } catch { /* skip unreadable */ } }
    }
  };
  if (existsSync(base)) walk(base);
  return aggregate(records);
}

/** Render TSV (default) or pretty JSON. */
export function render(result, json = false) {
  if (json) return JSON.stringify(result, null, 2);
  const t = result.totals;
  const lines = ["session\tmessages\ttokens\tcost_usd"];
  for (const s of result.sessions) lines.push(`${s.sessionId}\t${s.msgs}\t${s.tokens}\t${s.costUsd.toFixed(4)}`);
  lines.push("");
  lines.push(`TOTAL\tmsgs=${t.messages}\ttokens=${t.totalTokens}\t$${t.costUsd.toFixed(4)}` + (t.durationMs !== null ? `\tspan=${(t.durationMs / 60000).toFixed(1)}min` : ""));
  lines.push(`tokens: in=${t.inputTokens} out=${t.outputTokens} cacheW=${t.cacheWriteTokens} cacheR=${t.cacheReadTokens}`);
  if (result.warnings.length) lines.push(`WARN unpriced (counted at sonnet-default): ${result.warnings.join(", ")} — ${t.defaultPct}% of tokens are default-priced, so the $ is only that-much directional`);
  lines.push("# retail per-token prices — DIRECTIONAL for Max-plan users (right for A/B deltas, wrong for absolute spend)");
  return lines.join("\n");
}

if (process.argv[1]?.replace(/\\/g, "/").endsWith("measure.mjs")) {
  const a = process.argv.slice(2); const di = a.indexOf("--dir");
  console.log(render(measure(di >= 0 ? a[di + 1] : undefined), a.includes("--json")));
}
