# ORDO ADD-PLAN — the honest gap-fillers (post-eval gate)

> Derived from [`COMPETITIVE-TEARDOWN.md`](COMPETITIVE-TEARDOWN.md) (12 repos, source-level). Governing law from
> `OPERATING-PROFILE.md` §0: **measured-or-marked, lossless-first, 10 ≠ target.** Every addition either (a) produces a real
> measured number where ORDO currently estimates, or (b) fills a named structural gap as a spec contract. **Nothing lossy
> ships as a default. No foreign runtime is vendored** — ORDO stays a spec + thin JS/Python runtime. Five of six phases are
> spec contracts / one read-only script / packaging; only Phases 3 and 6 touch the runtime, both additively and reversibly.

ORDO today (verified in repo): a JS runtime (`src/index.js`: `decode`/`emit`/`compressInbound`/`ponytailFlags`), a Python
harness (`harness/`), 10 pillars, 6 gates (single / REFEED / experimentalist / evaluation / autonomy / context-rot), and
`OPERATING-PROFILE.md` as the paste-in spine. `docs/SELF-EVAL.md` already names the open roadmap: **P3 ($/wall-clock) is
PROXY-only, model routing absent, no code-structure context, no task-decomposition format, `/ordo` not packaged.** The
teardown maps exactly onto those gaps.

---

## Phase 1 — Real cost + token measurement (close the P3 proxy gap) · **HIGHEST VALUE**
**Build:** a ~80-line read-only Node script `tools/measure.mjs` (+ `ordo measure` in `bin/ordo.js`). Walk
`~/.claude/projects/**/*.jsonl` (Claude Code's own transcripts), read the **real** `usage.{input_tokens, output_tokens,
cache_creation_input_tokens, cache_read_input_tokens}` Anthropic already writes per assistant message, dedupe on
message UUID + request_id (keep-best on collision), price each row by **the per-message `model` field** against an embedded
LiteLLM `$/token` table (date-suffix-strip → family → prefix → default fallback), take wall-clock duration from first/last
timestamp. Emit TSV/JSON: tokens + USD + duration per session/day.

**Why first:** the single number ORDO cannot currently produce. Converts the headline claims (grammar ~32%, output ~55-77%,
end-to-end ~47-64%) from tokenizer-proxy into an **A/B dollar delta** (ORDO-profile-on vs off, same task corpus). Lossless by
construction — the billed counts sit in the logs, no re-tokenization. (Triangulated by ccusage, agentgraphed, and
claude-code-templates independently.)

**Integration point:** new `tools/measure.mjs` → `ordo measure`; output feeds `tools/pillars.py` P3, **retagging it COMPUTED
instead of PROXY** in the scorecard.

**Risk:** LiteLLM retail prices are "directional" for Max-plan subscription users (right for A/B deltas, wrong for absolute
spend) — label it. Must key price by the per-message `model` (the catalog repos hardcode one rate — do not copy that bug).
Missing-model rows WARN + exclude, never silently zero.

## Phase 2 — `/ordo` slash-command + installable skill packaging · **HIGHEST VALUE** (the non-coder endgame)
**Build:** package `OPERATING-PROFILE.md` as a Claude Code **Agent Skill** + a `.claude-plugin` marketplace manifest,
installable two ways — `/plugin marketplace add Genjimusicbot/ordo` → `/plugin install`, or one `npx ordo-llm init` that drops
`.claude/` files. Apply the **3-tier progressive disclosure** shape (obsidian-skills convention): a trigger-rich `description`
with **negative triggers** ("fire when starting a coding/agentic task; do NOT fire for trivial one-line answers") always in
context, the profile body on match, `spec/*.md` as on-demand `references/`.

**Why:** this IS the stated endgame — a non-coder runs/references `/ordo` and gets the whole stack (compress + 6 gates + 10
pillars + orchestration) without pasting a 1.4k-token file by hand. Pure packaging discipline: lossless, zero new behavior.

**Integration point:** new `.claude-plugin/plugin.json` + `skills/ordo/SKILL.md` (frontmatter trigger + body) + `references/`
→ existing `spec/`; `npx ordo-llm init` in `bin/ordo.js`. No runtime change.

**Risk:** the `description` must encode precise fire/don't-fire triggers or it misfires and adds latency to trivial turns. Keep
the always-on layer tiny (description only); lazy-load gates so a non-coder loads only the rule they hit.

## Phase 3 — Measured-revert gate for the inbound/output compressors · **HIGH VALUE**
**Build:** make ORDO's "lossless-first, never make it worse" promise a runtime **mechanism**, not a slogan. In `compressInbound`
(and the Python `compress_inbound`, which already takes best-of-candidates) add an explicit **count-before/count-after assert
that reverts any transform whose result is not strictly smaller** — worst case = passthrough, never inflation. Codify the
principle as one SOP line in `spec/output.md` + `OPERATING-PROFILE.md` §1: *"every transform is re-measured on the real
tokenizer; if it doesn't reduce tokens it is reverted."* (llmtrim's token gate, generalized.)

**Why:** ORDO's compression is currently prompt-SOP "do this" with no runtime proof it helped. The gate is strictly **additive
to safety** (it can only refuse a bad transform) and directly discharges the lossless-first invariant. The Python side already
picks min-tokens across candidates; this hardens it, names it, and brings the JS runtime to parity.

**Integration point:** `src/index.js::compressInbound` + `harness/inbound.py::compress_inbound` (≈90% there) + one law in `spec/output.md`.

**Risk:** Anthropic/Gemini tokenizers are proprietary; the o200k/cl100k count is a proxy, so a "win" can be mis-measured ~10-20%
on Claude. Mitigation: revert on `after ≥ before` (conservative direction), flag the proxy. Low — the gate only ever refuses,
never drops signal. **Also fold in** llmtrim's cheap **coverage check** (distinct query-relevant n-gram-type survival) as the
deterministic "did the lossy cut drop signal" revert signal for any lossy inbound path.

## Phase 4 — Code-structure context as an OPTIONAL external provider + spec contract · **HIGH VALUE, BOUNDED**
**Build:** do NOT vendor an AST engine. Recommend `codegraph` (default, lossless/code-only) or `graphify` (multimodal) as the
optional external code-graph provider ORDO's context layer consumes (both ship as slash-commands/MCP for ~20 agents), and codify
the **architecture pattern** in a new `spec/code-context.md`: (1) **deterministic-AST-first / LLM-only-for-prose** split —
structure parsed free, never burns tokens; (2) **token-budgeted subgraph render** with a hard cut + self-describing truncation
hint ("narrow / open the file"); (3) **confidence-tagged edges** (EXTRACTED 1.0 / INFERRED / AMBIGUOUS) that pass through the
evaluation gate — never present an inferred edge as fact. Lift codegraph's two format ideas (dynamic-dispatch hop annotated by
registration site; polymorphic-family skeletonization).

**Why:** the one genuinely **empty** layer in ORDO (zero AST / call-graph / project-map). Filling it as a *consumable contract +
provider recommendation* keeps ORDO a spec+thin-runtime instead of absorbing a tree-sitter product.

**Integration point:** new `spec/code-context.md`, referenced from `OPERATING-PROFILE.md` §1 (inbound) + §2 (gates — INFERRED edges
route through evaluation). Optional: a `context_provider` hook field the runtime can shell out to.

**Risk:** a graph is a **lossy navigation index, not the source**. A graph-first hook that over-suppresses real file Reads degrades
editing/debugging — the contract must say "navigation only; open the file for exact bytes." INFERRED edges are LLM guesses; gate them.

## Phase 5 — Task-decomposition DATA CONTRACT · **MEDIUM VALUE**
**Build:** a single output-format spec `spec/decompose.md`: the task-node shape `{id, title, deps:number[] (lower-id-only → free
DAG), priority, complexityScore 1-10, testStrategy, status}`, the three-stage **decompose → score → expand-by-score** contract (the
complexity pass **pre-writes** the expansion prompt), and the pure `priority → fewest-deps → lowest-id` next-task selector. Format
+ one SOP only. (claude-task-master's schema, not its runtime.)

**Why:** "task decomposition FORMAT" is a named gap. The lower-id-only DAG invariant gives trivially topo-sortable plans, and the
per-node `testStrategy` field forces **evidence-gating at decomposition time** — aligning with the test-gated pillars and the autonomy gate.

**Integration point:** new `spec/decompose.md`, consumed by the AUTONOMY gate (`spec/autonomy.md`) as the plan shape it iterates;
emit via existing `emit()`.

**Risk:** the lower-id invariant can mis-rank genuinely parallel work, and a naive next-task picker returns null on dependency-deadlock
— *which looks like done*. ORDO keeps its own autonomy kill/anchor logic on top; never let an unverified single-LLM-pass decomposition
feed a loop without REFEED. **Take the format, not the trust model.**

## Phase 6 — Opt-in declarative model-routing policy · **MEDIUM VALUE, GUARDED** (lowest priority — most quality risk)
**Build:** a tiny `route:` block in the operating-profile spec — a **5-signal fixed-priority cascade** (default / background-cheap /
think / longContext / webSearch + `longContextThreshold`), resolved by a ~30-line `resolveModel()` in the runtime that a
strand_runner or `/ordo` consults to pick the model *before* spawning. Signals all cheap + statically detectable: context-token size,
reasoning/plan flag, web-search tool present, background/throwaway class, explicit per-subagent override tag. Plus the longContext
heuristic (current>60k OR last-turn>threshold AND current>20k). (claude-code-router's table shape, not its proxy.)

**Why:** "cheap-vs-strong by task" is a declared gap; the routing *table shape* is the transferable insight (not the
proxy/transformers/UI of the source repo).

**Integration point:** a `route:` map in `OPERATING-PROFILE.md` + `resolveModel()` in `src/index.js`; opt-in, **defaults everything to
the strong model.**

**Risk:** routing is **lossy by construction** — every cheap substitution trades quality for cost, and crude signals (a short prompt
can be a hard reasoning fork) silently degrade exactly the calls that *look* cheap. Mitigation: ship OPT-IN like the glyph mode, default
strong, gate any downgrade behind a user-declared cost preference. **Never auto-downgrade.** This is last precisely because it carries the
most quality risk against the 10≠target / no-quality-loss discipline.

---

## Prioritized additions (ranked)
1. **Real cost+token+duration meter** from Claude Code's own JSONL `usage.*` fields (`ordo measure`) — converts P3 PROXY → COMPUTED, lossless, ~80 LOC read-only.
2. **`/ordo` as an installable Agent Skill** + `.claude-plugin` manifest with negative-trigger description + 3-tier progressive disclosure — the non-coder endgame, pure packaging.
3. **Measured-revert gate** in `compressInbound`/`compress_inbound` (count-before/after, revert on no-win + coverage check) — makes lossless-first a mechanism (Python side ~90% there).
4. **Code-structure context** `spec/code-context.md` (AST-first + budgeted-render + confidence-tagged edges) consuming codegraph/graphify as an OPTIONAL external provider — fills the one empty layer without vendoring an engine.
5. **Task-decomposition data contract** `spec/decompose.md` (lower-id DAG + per-node testStrategy + complexity-gates-expansion + pure next-task picker) — fills the named decompose-FORMAT gap.
6. **Opt-in declarative model-routing policy** (5-signal priority cascade + longContext heuristic), default-strong, ~30-line resolver — fills the cheap-vs-strong gap but guarded as the riskiest add.

## Overlaps to avoid (refuse — they duplicate owned layers and import quality risk)
- **rtk** command-output compression + aggressive body-stripping — duplicates the INBOUND layer; body-stripper is lossy. (Only the failure-tee-with-pointer pattern is worth a line in `spec/code-context.md`.)
- **llmtrim's lossy STAGES** (BM25 chunk-drop, body skeletonization, JSON down-sampling) — duplicate + degrade the inbound pillar (GSM8K −8pp). Take only the measured-revert + coverage *principles* (Phase 3).
- **context-mode's FTS5/BM25 session-memory + RRF engine** — duplicates the context-rot ledger; heavy SQLite infra + silent recall-failure. (The Think-in-Code OBSERVE/PROCESS/EDIT SOP is a separate lossless line for `spec/output.md`.)
- **andrej-karpathy-skills** (4-principle CLAUDE.md) — subsumed by gates+LEAN; its "ask rather than guess" register *contradicts* act-don't-survey and causes clarification-stalls. **Add nothing.**
- **obsidian defuddle** as a default inbound path — lossy heuristic stripper, violates lossless-first; opt-in for known-noisy articles only. (Only its description-trigger + 3-tier convention informs Phase 2.)
- **claude-code-templates installer/catalog + claude-code-router proxy/transformers/UI** — whole products' worth of surface ORDO doesn't need. Take only the read-only cost-reader (Phase 1) and the routing table shape (Phase 6).
- **claude-task-master executor + babysit loop + MCP server** — ORDO has stronger MEASURED versions (autonomy gate + (tool,args,result) detector, REFEED). Take only the decomposition contract (Phase 5).

## The `/ordo` command vision
A non-coder types `/ordo` (or installs it once) and gets the best Claude Code experience without understanding any of it. **Path:** ship
`OPERATING-PROFILE.md` as a Claude Code Agent Skill behind a `.claude-plugin` marketplace manifest (the claude-code-templates / karpathy-skills
distribution pattern), installable via `/plugin marketplace add Genjimusicbot/ordo` → `/plugin install`, or one `npx ordo-llm init`. **Strict 3-tier
progressive disclosure** (obsidian-skills): an always-in-context `description` with explicit **negative triggers** so the gate never misfires; the
profile body on match; the six gate specs + new `spec/code-context` + `spec/decompose` load only when that sub-task hits. Once installed, `/ordo`
activates the whole stack — compress (grammar + output contract + inbound, now with the measured-revert gate), the six classify-first gates, the ten
pillars, ledger orchestration — and `ordo measure` shows even a non-coder the real dollar/token A/B delta of running with it vs without. The packaging
is **lossless and additive**: it changes nothing about ORDO's behavior, it just removes the "paste this 1.4k-token file by hand" friction that currently
gates adoption to people who already know what a `CLAUDE.md` is.

## Honest risks (the standing audit)
The dominant risk is **scope-creep diluting the honesty moat**: every added layer is one more number that must be MEASURED-or-MARKED. The Phase 1 meter,
priced on retail LiteLLM rates, will silently mislead Max-plan users on absolute spend (valid for A/B deltas only — label it). **Model routing (Phase 6)
is the genuine quality-loss risk** — lossy by construction, its cheap signals can't tell a short-but-hard fork from a throwaway; it must stay opt-in and
default-strong or it violates the 10≠target law. The code-graph (Phase 4) carries a subtler regression: a graph-first hook that over-suppresses real Reads
makes editing/debugging WORSE, and INFERRED edges can inject false structure if not gated. Task decomposition (Phase 5) can deadlock-as-done and its
single-pass edges are hallucination-prone — format yes, trust model no. **Cross-cutting law:** never let Phase 1's per-tool byte-attribution or Phase 6's
routing feed a quality/cost GATE — they are directional telemetry, not ground truth, and wiring them into a gate would corrupt the un-gameable test-gate
discipline that is ORDO's whole credibility. Five of six phases are thin spec contracts + packaging; only two touch the runtime, both reversibly. **The moment
any phase adds a lossy default or an unmarked number, it makes ORDO worse, not bigger.**
