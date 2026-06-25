// ORDO runtime — the deterministic, runnable core (a faithful JS port of harness/ordo.py + output.py).
// What's RUNTIME (this file): decode an ORDO-G command to English; emit data in the cheapest faithful
// format; flag ponytail filler; a lossless built-in inbound compressor; load the paste-in spec.
// What's METHODOLOGY (not code): the gates (REFEED / experimentalist / evaluation / autonomy /
// context-rot) are prompt SOPs in spec/*.md — they are loaded as text via getSpec(), not executed here.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

// ---- decode tables (ported from harness/ordo.py) ----
const DIRECTIVES = { "σ": "summarize", "ε": "explain", "δ": "define", "α": "analyze", "χ": "critique",
  "ρ": "rewrite", "τ": "translate", "π": "make a step-by-step plan for", "λ": "write code for",
  "γ": "generate", "β": "brainstorm", "μ": "compare", "φ": "find and fix the bug in", "ν": "refactor",
  "ω": "give the final answer for", "→": "continue", "↑": "expand on", "↓": "shorten",
  "★": "rate from 1 to 10", "☆": "give a worked example of", "※": "extract verbatim from", "§": "outline",
  "●": "list", "■": "classify", "×": "delete", "¬": "exclude", "±": "give variations of", "†": "verify" };
const OPERAND = { "文": "the following text", "码": "the following code", "话": "the conversation so far",
  "上": "the above", "此": "this / the current selection", "网": "the URL that follows", "源": "the following data" };
const LENGTH = { "↓": "in tl;dr form", "简": "concisely", "全": "exhaustively", "↑": "in expanded detail" };
const FORMAT = { "列": "as bullet points", "表": "as a table (TSV)", "构": "as minified JSON", "段": "as prose",
  "图": "as a diagram", "码": "as code only", "标": "as markdown" };
const UNIT = { "字": "words", "行": "sentences", "段": "paragraphs", "分": "minutes", "名": "names",
  "项": "items", "步": "steps", "页": "pages", "节": "sections", "列": "bullet points" };
const FOCUS_VAL = { "金": "the financial figures", "码": "the code", "题": "the key problem" };
const AUD = { "通": "a non-expert", "专": "an expert", "民": "the general public" };
const TONE = { "正": "a formal", "友": "a friendly", "反": "a casual", "软": "a gentle" };
const CONSTRAINT = { "¬": "do not include", "加": "must include", "只": "restrict to only", "×": "remove", "据": "preserve" };
const CVAL = { "序": "any preamble", "名": "names", "码": "code" };
const EPI = { "信": "mark your certainty for each claim", "源": "cite your sources",
  "?": "flag anything you are unsure of", "确": "state only what you can verify", "†": "fact-check before answering" };
const FOCUS_TAG = "心", AUD_TAG = "业", TONE_TAG = "调";
const CTAGS = new Set(Object.keys(CONSTRAINT));

function tokens(s) {
  const out = []; let i = 0; const n = s.length;
  while (i < n) {
    const c = s[i];
    if (c === '"') { let j = s.indexOf('"', i + 1); if (j === -1) j = n; out.push(["LIT", s.slice(i + 1, j)]); i = j + 1; }
    else if (c === "@") { let j = i + 1; while (j < n && !(s[j] in OPERAND) && !"|>\"".includes(s[j]) && !CTAGS.has(s[j])) j++; out.push(["FILE", s.slice(i + 1, j)]); i = j; }
    else if (c >= "0" && c <= "9") { let j = i; while (j < n && s[j] >= "0" && s[j] <= "9") j++; out.push(["NUM", s.slice(i, j)]); i = j; }
    else if (/[A-Z]/.test(c)) { let j = i; while (j < n && /[A-Za-z]/.test(s[j]) && s[j] === s[j].toUpperCase()) j++; out.push(["CODE", s.slice(i, j)]); i = j; }
    else if ("|>()".includes(c)) { out.push(["OP", c]); i++; }
    else if (/\s/.test(c)) { i++; }
    else { out.push(["G", c]); i++; }
  }
  return out;
}

function parseStage(toks) {
  const a = { directives: [], operand: null, length: null, format: null, quantity: null, focus: null,
    audience: null, tone: null, language: null, constraints: [], epistemic: [], literals: [] };
  let i = 0;
  while (i < toks.length && toks[i][0] === "G" && DIRECTIVES[toks[i][1]] !== undefined) { a.directives.push(DIRECTIVES[toks[i][1]]); i++; }
  for (; i < toks.length; i++) {
    const [kind, val] = toks[i]; const nxt = toks[i + 1] || null;
    if (kind === "LIT") { if (a.operand === null && a.constraints.length === 0) a.operand = `"${val}"`; else a.literals.push(val); }
    else if (kind === "FILE") a.operand = `the file ${val}`;
    else if (kind === "CODE") a.language = val;
    else if (kind === "NUM") { let unit = "items"; if (nxt && nxt[0] === "G" && UNIT[nxt[1]] !== undefined) { unit = UNIT[nxt[1]]; i++; } a.quantity = `${val} ${unit}`; }
    else if (kind === "OP") { /* | > ( ) handled at chain level */ }
    else if (kind === "G") {
      const g = val;
      if (OPERAND[g] !== undefined && a.operand === null && a.constraints.length === 0) a.operand = OPERAND[g];
      else if (LENGTH[g] !== undefined) a.length = LENGTH[g];
      else if (g === "段" && a.operand !== null) a.format = FORMAT["段"];
      else if (FORMAT[g] !== undefined && !(g === "码" && a.operand === null)) a.format = FORMAT[g];
      else if (g === FOCUS_TAG) { if (nxt && nxt[0] === "LIT") { a.focus = nxt[1]; i++; } else if (nxt && nxt[0] === "G" && FOCUS_VAL[nxt[1]] !== undefined) { a.focus = FOCUS_VAL[nxt[1]]; i++; } else a.focus = "the key part"; }
      else if (g === AUD_TAG) { if (nxt && nxt[0] === "G" && AUD[nxt[1]] !== undefined) { a.audience = AUD[nxt[1]]; i++; } else a.audience = "a general reader"; }
      else if (g === TONE_TAG) { if (nxt && nxt[0] === "G" && TONE[nxt[1]] !== undefined) { a.tone = TONE[nxt[1]]; i++; } else a.tone = "a neutral"; }
      else if (CONSTRAINT[g] !== undefined) {
        if (nxt && nxt[0] === "LIT") { a.constraints.push(`${CONSTRAINT[g]} ${nxt[1]}`); i++; }
        else if (nxt && nxt[0] === "G" && CVAL[nxt[1]] !== undefined) { a.constraints.push(`${CONSTRAINT[g]} ${CVAL[nxt[1]]}`); i++; }
        else if (nxt && nxt[0] === "G" && FORMAT[nxt[1]] !== undefined && g === "只") { a.format = FORMAT[nxt[1]]; i++; }
        else a.constraints.push(CONSTRAINT[g]);
      }
      else if (EPI[g] !== undefined) a.epistemic.push(EPI[g]);
      else if (DIRECTIVES[g] !== undefined) a.directives.push(DIRECTIVES[g]);
      else a.literals.push(g); // unknown glyph -> literal (graceful, never throws)
    }
  }
  return a;
}

export function parse(s) {
  const stages = []; let cur = [];
  for (const t of tokens(s)) { if (t[0] === "OP" && t[1] === "|") { stages.push(cur); cur = []; } else cur.push(t); }
  stages.push(cur);
  return stages.map(parseStage);
}

function stageEnglish(a) {
  const parts = [a.directives.join(" and ") || "respond to", a.operand || "the following"];
  if (a.quantity) parts.push("in " + a.quantity);
  if (a.format) parts.push(a.format);
  if (a.length) parts.push(a.length);
  if (a.focus) parts.push("focusing on " + a.focus);
  if (a.audience) parts.push("for " + a.audience);
  if (a.tone) parts.push("in " + a.tone + " tone");
  if (a.language) parts.push("into " + a.language);
  let s = parts.join(" ");
  const extra = a.constraints.concat(a.literals.map((l) => "also " + l));
  if (extra.length) s += "; " + extra.join("; ");
  if (a.epistemic.length) s += "; " + a.epistemic.join(", ");
  return s;
}

/** Decode an ORDO-G command string to its full English instruction (deterministic). */
export function decode(s) { return parse(s).map(stageEnglish).join("; then "); }

// ---- output contract (ported from output.py) ----
function uniformRecords(data) {
  if (data && typeof data === "object" && !Array.isArray(data) && Object.keys(data).length === 1) {
    const v = data[Object.keys(data)[0]];
    if (Array.isArray(v) && v.length && v.every((x) => x && typeof x === "object" && !Array.isArray(x))) {
      const k0 = JSON.stringify(Object.keys(v[0]));
      if (v.every((x) => JSON.stringify(Object.keys(x)) === k0) && v.every((x) => Object.values(x).every((val) => typeof val !== "object"))) return v;
    }
  }
  return null;
}
const scalar = (v) => (typeof v === "boolean" ? (v ? "true" : "false") : v == null ? "" : String(v));

/** Serialize data in the measured-cheapest faithful format: TSV for uniform records, else minified JSON. */
export function emit(data) {
  const rows = uniformRecords(data);
  if (rows) { const f = Object.keys(rows[0]); return [f.join("\t"), ...rows.map((r) => f.map((k) => scalar(r[k])).join("\t"))].join("\n"); }
  return JSON.stringify(data);
}
export function bestFormat(data) { return uniformRecords(data) ? "tsv" : "json_min"; }

const FILLER = ["great question", "sure!", "certainly", "i hope this helps", "let me know if",
  "feel free to", "as an ai", "here's", "here is", "i'd be happy to", "of course!"];
/** Return the ponytail-forbidden filler phrases present (the verbosity layer says cut these). */
export function ponytailFlags(text) { const low = text.toLowerCase(); return FILLER.filter((p) => low.includes(p)); }

/** Lossless built-in inbound compressor: JSON arrays -> TSV; else collapse dead whitespace. */
export function compressInbound(text) {
  const t = text.trim();
  if (t[0] === "[" || t[0] === "{") {
    try { let data = JSON.parse(t); if (Array.isArray(data)) data = { _rows: data }; return emit(data); } catch { /* fall through */ }
  }
  return text.replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").replace(/[ \t]{2,}/g, " ");
}

// ---- the paste-in spec (METHODOLOGY: load as text, give to your LLM) ----
const _cache = {};
function read(p) { if (!(p in _cache)) _cache[p] = readFileSync(join(ROOT, p), "utf8"); return _cache[p]; }
/** The full operating profile — paste into a system prompt to run the whole framework. */
export const getOperatingProfile = () => read("OPERATING-PROFILE.md");
/** The language skillstone — paste in to teach an LLM ORDO-G. */
export const getSkillstone = () => read("ORDO.md");
/** Load any methodology spec by name, e.g. getSpec("framework") for the REFEED loop. */
export const getSpec = (name) => read(`spec/${name}.md`);
