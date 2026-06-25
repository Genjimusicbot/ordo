# ORDO Competitive Teardown — 12 repos, judged through the evaluation gate

> Method: each repo was **cloned and read at the source level** (the actual engine, not the README), then
> judged through ORDO's own evaluation gate — **adopt only what fills a real gap WITHOUT overlapping a layer
> ORDO already owns AND without a quality-loss risk.** A thing that duplicates an owned layer scores
> `skip-overlap`; a lossy compressor gets a `quality-loss` flag. 10 is not the target; we do not add complexity
> the framework does not need. Generated 2026-06-25 from a 13-agent parallel teardown (~1.04M tokens).

## Verdict at a glance

| # | Repo | Category | Verdict | What it fills / why skipped |
|---|---|---|---|---|
| 1 | [ccusage](https://github.com/ccusage/ccusage) | measurement | **adapt-partial** | external before/after **$ meter** (COST half of P3); shell out, don't vendor |
| 2 | [rtk](https://github.com/rtk-ai/rtk) | cmd-output compression | **skip-overlap** | duplicates inbound layer; take only the **failure-tee-with-pointer** pattern |
| 3 | [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | skills (prompt SOP) | **skip-overlap** | subsumed by gates+LEAN; its "ask, don't guess" register *contradicts* act-don't-survey |
| 4 | [graphify](https://github.com/safishamsi/graphify) | code-graph | **adapt-partial** | fills the **code-structure gap**; lift AST-first split + budgeted render + confidence-tagged edges |
| 5 | [obsidian-skills](https://github.com/kepano/obsidian-skills) | packaging/skills | **skip-overlap** | content irrelevant; copy the **negative-trigger + 3-tier** packaging convention for `/ordo` |
| 6 | [codegraph](https://github.com/colbymchenry/codegraph) | code-graph | **adapt-partial** | external provider for the code gap + 2 render-format ideas |
| 7 | [agentgraphed](https://www.npmjs.com/package/agentgraphed) | measurement | **adapt-partial** | the **~100-LOC recipe** to read Anthropic's own `usage.*` from JSONL → real tokens/$ |
| 8 | [context-mode](https://github.com/mksglu/context-mode) | cmd-output + context-mgmt | **adapt-partial** | lift the **Think-in-Code** inbound SOP (OBSERVE/PROCESS/EDIT/MUTATE); skip the FTS5 engine |
| 9 | [llmtrim](https://github.com/fkiene/llmtrim) | cmd-output compression | **adapt-partial** | lift the **measured-revert gate** + coverage gate + lossless log/array recipes; skip proxy + lossy stages |
| 10 | [claude-code-router](https://github.com/musistudio/claude-code-router) | model-routing | **adapt-partial** | the **5-signal routing table shape**; skip the proxy/transformers/UI |
| 11 | [claude-task-master](https://github.com/eyaltoledano/claude-task-master) | task decomposition | **adapt-partial** | the **task-node data contract** (lower-id DAG + testStrategy + complexity-gates-expansion); skip the loop |
| 12 | [claude-code-templates](https://github.com/davila7/claude-code-templates) | measurement + packaging | **adapt-partial** | the read-only **cost reader**; skip the installer/catalog |

**Net:** 6 gap-fillers worth adopting (as principles/spec/one script — never a foreign runtime), 6 layers to refuse.

---

## 1. ccusage — `adapt-partial` (external $ meter)
**What.** Read-only post-hoc usage/cost CLI for ~15 coding-agent CLIs. Parses the JSONL transcripts those tools
already write and reports tokens + USD per day/session/5h-block, plus a live statusline. Tiny JS launcher → Rust core.

**How (the mechanism).** All-Rust pipeline: (1) discover logs by convention (`CLAUDE_CONFIG_DIR`/XDG/`~/.claude`,
recursive `projects/**/*.jsonl`); (2) byte-scan parse with parallel file reads; (3) **dedupe** on
`hash(message_id + request_id)` (FxHasher), keep-best-on-collision (prefer non-sidechain → higher token total →
speed-tagged); (4) **cost** = each token bucket (input/output/cache-create-5m/cache-create-1h@2×/cache-read) ×
per-model price, with **tiered pricing above 200k** and a fast-tier multiplier; prices from a build-time-embedded
LiteLLM table + models.dev, HTTP-refreshable; (5) **blocks** = rolling 5h windows, burn-rate = tokens/wall-minutes;
(6) render TSV/table/JSON. Note: its "speed" is a *billing tier*, not latency.

**vs ORDO.** Hits the named gap "real wall-clock SPEED + $ COST" — but only the **COST** half (its speed is a price
tier, never seconds/response). ORDO has no cost instrument; P3 is proxy-only.

**Take / risk.** Use it as an **external before/after meter** (`ccusage claude session --json`, diff $/tokens
ORDO-on vs off) — don't build any of it. Internalize one discipline conceptually: **dedupe-then-price**
(hash, keep-best, tiered/cache-aware). **Overlap:** none (ORDO has no cost layer). **Quality-loss:** none (read-only);
caveat is interpretive — LiteLLM prices under-count new models, and "fewer tokens billed" never proves quality held.
**Effort:** low.

## 2. rtk ("Rust Token Killer") — `skip-overlap`
**What.** Single Rust binary that compresses shell-command **output** before it reaches the LLM (claimed 60-90% on
~100 dev commands), via a PreToolUse hook that rewrites `git status` → `rtk git status`. Plus `discover`/`learn` analytics.

**How.** Hook → `rtk rewrite` → static command registry gated by a **security exit-code protocol**
(0 allow / 1 passthrough / 2 deny / 3 ask), passthrough on any unparseable construct (backticks, `$()`, redirects).
Each `rtk <cmd>` runs the real command then applies a per-command filter (smart-noise / group / truncate / dedup-with-counts).
Test/error filters are **streaming**: keep only failure lines + summary, and **TEE the full raw output to disk** with the
path printed inline (`[full output: …log]`) so the agent recovers it without re-running. Code filter has an *aggressive*
mode that strips function bodies (lossy). Savings tracked in SQLite via chars/4 estimate. <10ms, fallback-to-raw.

**vs ORDO.** RTK *is* the inbound layer (headroom + TSV), packaged and hardened. We have the policy; it has one slice's
implementation.

**Take / risk.** Lift exactly one mechanism: the **failure-tee-with-pointer** — compress to a summary in-context but
stash the full payload at a disk path and print it, so it's **lossless-on-demand** (neutralizes the quality objection,
fits lossless-first). Also note the security exit-code protocol is the right shape *if* `/ordo` ever ships a command-rewriting
hook. **Overlap:** high — adopting RTK wholesale duplicates inbound + adds a 15k-LOC Rust binary + SQLite. **Quality-loss:**
yes — aggressive body-stripping drops signal (reject); chars/4 is not a real tokenizer. **Effort:** low (tee pattern only).

## 3. andrej-karpathy-skills — `skip-overlap`
**What.** A ~65-line CLAUDE.md/SKILL.md packaging four behavioral principles (Think Before Coding / Simplicity First /
Surgical Changes / Goal-Driven Execution). No code, no runtime.

**How.** No algorithm — the "mechanism" is the prompt text, injected via CLAUDE.md or a skill description, distributed as a
`.claude-plugin` marketplace manifest (+ Cursor `.mdc` mirror + raw-curl path). Each principle is a terse rule list with a
one-line self-test.

**vs ORDO.** Every principle is already covered at higher resolution: Goal-Driven ≈ REFEED + autonomy (which adds a
`(tool,args,result)` kill-detector this repo has nothing for); Think-Before ≈ experimentalist + orchestration; Simplicity/Surgical
≈ the quality/tidyness/architecture/rework pillars + LEAN doctrine.

**Take / risk.** Nothing mechanical. **Overlap:** total — it would create a second, lower-resolution statement of four owned
layers (the exact context-bloat ORDO's compression exists to prevent). **Quality-loss:** subtle but real *behavioral regression* —
its "bias to caution / ask rather than guess / stop and ask" register **contradicts** ORDO+Fable's act-don't-survey norm and would
cause clarification-stalls. **Add nothing.**

## 4. graphify — `adapt-partial` (code-structure gap)
**What.** A `/graphify` slash-command (YC S26) that maps a whole project (code, docs, PDFs, images, video) into a persistent
queryable knowledge graph the agent reads *instead of* grepping/reading files. Serves it to ~20 agents via a query interface +
MCP. Headline: **71.5× fewer tokens/query** vs raw reads on a 52-file corpus (~1× at 6 files).

**How.** Three-pass build. **Pass 1 (free, no LLM):** tree-sitter parses 25 languages into nodes/edges (classes, fns, imports,
call graph); SQL gets tables/views/FKs deterministically; parallel via ProcessPoolExecutor, each file SHA256-fingerprinted so
re-runs skip unchanged. **Code is never sent to the LLM.** Pass 2: local whisper for audio/video. **Pass 3 (costs tokens):**
Claude subagents over docs/PDFs/images only → JSON fragments merged. Every edge tagged **EXTRACTED (1.0) / INFERRED (0.55-0.95
rubric) / AMBIGUOUS**. Communities via Leiden on the graph's own edges (no vector DB). **Query side (the ORDO-relevant core):**
tokenize question → seed-match nodes → BFS to depth N → render NODE/EDGE lines and **hard-cut at token_budget (default 2000)**
with a truncation message telling the agent to narrow. Incremental re-extract via git post-commit hook over the changed-file
blast radius.

**vs ORDO.** Hits the one **genuinely empty** ORDO layer (zero AST / call-graph / project-map).

**Take / risk.** Take the **architecture**, not a dependency: (1) **deterministic-AST-first / LLM-only-for-prose** split (structure
is free, never burns tokens); (2) **token-budgeted subgraph render** with hard cut + self-describing truncation hint (ORDO-shaped
output-contract thinking on graph traversal); (3) **confidence-tagged edges** (pair with the evaluation gate — never present an
INFERRED edge as fact). Recommend graphify as the **optional external provider** ORDO's context layer consumes. **Overlap:** bounded
— the render layer is conceptually adjacent to the output contract but renders a graph ORDO has no source for, so it complements.
**Quality-loss:** real — a graph is a **lossy navigation index, not the source**; for editing/debugging the agent must still open the
file, and a graph-first hook that over-suppresses Reads degrades quality. INFERRED edges can hallucinate structure. **Effort:** medium.

## 5. obsidian-skills (kepano) — `skip-overlap` (packaging lesson only)
**What.** A 5-skill pack teaching an agent Obsidian's file formats (markdown, `.base`, `.canvas`, the CLI, `defuddle`). The clean,
canonical reference implementation of the Agent Skills spec. No engine.

**How.** Pure **progressive disclosure**: each skill is a folder whose SKILL.md frontmatter has only `name` + a trigger-rich
`description` (the only always-in-context part); body is a terse procedure; heavy material lives in `references/*.md` loaded on demand.
Two craft details: **negative triggers** in the description ("Do NOT use for URLs ending in .md") to prevent misfire, and every workflow
ends in an explicit **Validate/Test** step. The one mechanical asset is `defuddle parse <url> --md` (lossy web→markdown extractor).

**vs ORDO.** Substance is already owned (gates-as-SOP, loadable profile, inbound compression). The **packaging discipline** is what
ORDO's known-gap list wants.

**Take / risk.** Two free packaging lessons for the `/ordo` skill (no code): **negative/exclusion triggers in the `description`** so the
gate fires precisely, and the strict **3-tier split** (always-on description → on-match body → on-demand references). **Overlap:** high
(skill-spec structure ≈ ORDO's loadable profile; defuddle ≈ compressInbound; validate-step ≈ REFEED). **Quality-loss:** low for the
packaging lessons (structural, lossless); flag on **defuddle** — lossy heuristic stripper, never the default inbound path. **Effort:** low
(a manifest convention, not engineering).

## 6. codegraph — `adapt-partial` (external code-graph provider)
**What.** Local CLI + MCP server giving the agent a pre-built knowledge graph: tree-sitter parses 20+ languages into a SQLite symbol
graph; `codegraph_explore` returns the relevant source + call paths + impact radius in one call; a file watcher keeps it fresh. Claims
~58% fewer tool calls, ~22% faster. (The npm `agentgraphed` name collision is unrelated.)

**How.** Deterministic, **no embeddings**. Tree-sitter WASM → nodes/edges in SQLite with FTS5. Explore: regex symbol extraction
(minus stopwords) → exact-name + FTS5 lookup with co-location boost → BFS subgraph → DFS call-paths over `calls` edges, keeping chains
that link ≥2 query roots, **dynamic-dispatch hops annotated by registration site** → render **verbatim on-disk source** for spine files
with **adaptive skeletonization** (collapse off-spine polymorphic-family members to signatures).

**vs ORDO.** Fully fills the code-structure gap; nothing in ORDO to retrieve/index.

**Take / risk.** Adopt as an **external MIT dependency** for the gap; lift two format ideas into the spec: the **call-path format that
annotates dynamic-dispatch hops with the registration site**, and the **polymorphic-family skeletonization** (spine full, redundant
siblings → signatures). **Overlap:** low. **Quality-loss:** bounded — retrieval re-reads **verbatim** source (lossless); skeletonization is
lossy but gated to redundant families and reversible via explore; lexical-only extraction can surface off-target entries (emits a
low-confidence banner). **Effort:** low to adopt, medium to lift the two ideas.

> graphify vs codegraph: same core idea (AST-graph the codebase, query instead of grep). graphify is broader (multimodal, communities,
> cross-agent) and noisier (Pass-3 LLM inference); codegraph is leaner, code-only, verbatim-source, no LLM in the loop. **codegraph is the
> better fit for ORDO's lossless-first stance**; graphify is the better fit when docs/PDFs matter. Recommend codegraph as default provider,
> graphify as the multimodal option.

## 7. agentgraphed — `adapt-partial` (the P3 recipe)
**What.** Despite the name, **not** an orchestration framework — a local usage/cost dashboard for Claude Code + Codex. Indexes the JSONL
transcripts into SQLite and renders timeline/sessions/analytics: per-session tokens + $ + wall-clock duration + a live quota widget.

**How (the part worth taking).** **INGEST:** walk JSONL; for assistant lines read the `message.usage` block Anthropic **already writes**
(`input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`) — **real billed counts, no re-tokenization** —
summed per session; incremental skip on `(mtime,size)`; idempotent upsert on per-message UUID so subagent JSONLs accumulate not clobber.
**COST:** build-time LiteLLM table (~2700 models) × rate with a 5-step fallback (exact → strip date-suffix → family → prefix → $3/$15
default). **Duration** = max−min timestamp. (Skip its quota probe, classifier, leaderboard, UI.)

**vs ORDO.** Exactly the P3 substrate — converts proxy → measured at near-zero effort because **the billed numbers are sitting in the logs.**

**Take / risk.** Build a **~100-line read-only script** that parses `message.usage` from ORDO's own run transcripts, prices via embedded
LiteLLM with the date-strip/family fallback, takes duration from timestamps → real A/B (ORDO-on vs off). **Overlap:** none — it fills P3, it
doesn't duplicate it. **Quality-loss:** low on the load-bearing path (lossless billed counts); the one lossy piece (byte/4 per-source
attribution) must carry an explicit approx badge and never feed a gate; retail $ is "directional" for Max-plan users (right for deltas, wrong
for absolute). **Effort:** low.

> ccusage (#1), agentgraphed (#7), claude-code-templates (#12) all independently converge on the same insight: **Anthropic writes the real
> token counts into the JSONL; read them, price them.** That triangulation is why Phase 1 is the highest-confidence add.

## 8. context-mode — `adapt-partial` (Think-in-Code inbound SOP)
**What.** Multi-harness MCP plugin that keeps raw tool output **out** of the context window. Two engines: (1) **Think-in-Code** sandbox
tools — the model writes a script that reads/filters/aggregates data in a child-process sandbox and only `console.log`s the derived answer;
the raw bytes never enter context. (2) An **FTS5/BM25** knowledge store auto-indexing every command output / fetched URL / file edit, queried
by `ctx_search` instead of re-dumping. Claims ~96-98% savings. Notably its README **refuses output-side prose compression**, citing the
kimi-k2.5 finding that aggressive brevity degrades reasoning.

**How.** **Sandbox:** spawn a child process per language, run a temp script, capture stdout, discard the FS (analysis-only — writes still go
through native Write/Edit). 47 Reads (700KB) → one script printing 3.6KB. **Store:** SQLite with **two** FTS5 tables over the same chunks
(porter-stemmed + trigram-fuzzy), queried via **Reciprocal Rank Fusion**, with levenshtein fuzzy-correction fallback, bm25 ranking
(title 5×), and a min-span proximity re-rank. Chunks split on markdown headings under a byte cap. **Routing:** a static
`<context_window_protection>` prompt block injected at SessionStart + PreToolUse (pure nudge — the model still chooses). Session continuity
classifies every tool call (file/git/error/decision/...) into a SessionDB for chronological merge on compaction.

**vs ORDO.** The Think-in-Code half is a **structurally different inbound move** ORDO lacks (never bring the bytes in vs ORDO's format-level
compressor). The FTS5 store **duplicates** the context-rot ledger.

**Take / risk.** Lift **one idea as a prompt SOP** (no code): a **Think-in-Code inbound rule** — "when you will PROCESS a large tool output
(filter/count/parse/aggregate), write a sandbox/Bash script that prints only the derived answer; reserve raw reads for OBSERVE (short fixed
output) or EDIT (need exact bytes)." Steal the crisp **OBSERVE / PROCESS / EDIT / MUTATE** decision boundary (debiased trigger that won't
misfire on `git status`). **Overlap:** the FTS5/RRF session-memory half directly duplicates the context-rot ledger + context-integrity pillar
(skip — heavy SQLite infra for what ORDO does as a prompt). **Quality-loss:** the adopted SOP is **lossless by construction** (model chooses
what to print; under-print → re-run). The parts we skip are lossy: `ctx_execute_file` summarize drops raw lines; top-k `ctx_search` has silent
recall failure. **Effort:** low (~6-10 lines of SOP).

## 9. llmtrim — `adapt-partial` (the measured-revert gate)
**What.** A local HTTPS proxy (CA constrained to LLM domains) that sits between any agent and the provider and **deterministically compresses
each request's tokens** before forwarding, reply untouched. Also CLI/MCP/lib. Headline measured across 112 live A/B cases: **−31% input,
−74% output, −66% round-trip $, quality 78.9→82.2% (no degradation).**

**How (rich, worth studying).** A sequential **gated stage pipeline** over a normalized JSON IR. The core safety invariant = the **TOKEN GATE**:
after every stage re-count tokens with the provider's real tokenizer (tiktoken exact for OpenAI, BPE proxy for Anthropic/Gemini, *flagged*) and
if `after ≥ before` **revert to the pre-stage snapshot.** Worst case = zero savings, never bigger/broken. Token counts memoized per segment, skip
re-tokenizing unchanged subtrees. Stages: (A) lossless template-fold of repeated log lines `[×N]` then window logs/diffs to errors/changes;
(B) BM25+RM3+TextTiling+TextRank relevance retrieval (LOSSY); (C) tree-sitter skeletonization to signatures (LOSSY); (D) minify + TOON/columnar
encode (lossless); (E) exact + SimHash dedup; reversible **abbreviation dictionary with in-prompt legend** (suffix-array maximal repeats, lossless);
(F) output-control terse/Chain-of-Draft injection; (G) drop unused tools + **never rewrite the cache_control prefix** (preserves prompt-cache
discount). The **second** safety axis = the **QUALITY GATE**: for lossy content stages, a zero-model **n-gram COVERAGE** check — fraction of distinct
query-relevant unigram/bigram *types* (from the last-user-turn question) surviving the cut; if coverage < 0.5 (split-conformal calibrated to ≥0.90
answer recall) revert exactly like a token failure. Every stage cites a paper; "the ideas are theirs, the token gate is ours." Its `auto` is
**preset routing by request shape — NOT model routing** (don't confuse the two).

**vs ORDO.** ORDO already has the compression *layer* conceptually. What it genuinely lacks and llmtrim has: (1) a **per-step measured token gate**
that auto-reverts any transform that doesn't actually save; (2) a cheap **deterministic coverage gate** that proves a lossy cut kept the answer;
(3) real $/wall-clock A/B; (4) concrete **lossless** log/array recipes (template-fold, TOON columnar, suffix-array legend).

**Take / risk.** Three liftable **ideas**, none of the Rust proxy: (1) the **measured-revert gate principle** — "every transform is re-measured;
if it doesn't reduce tokens it's reverted" — the single most valuable concept, it turns lossless-first from a slogan into a mechanism; (2) the
**coverage quality-gate** as a cheap deterministic "did the cut drop signal" check (far cheaper than an LLM judge); (3) the **concrete lossless
recipes** as named entries in the inbound spec (they beat a blanket "use TSV"). **Overlap:** its lossy stages + output-control terse instruction
duplicate the inbound layer + ponytail (skip). **Quality-loss:** low if we take only the gate *principles* (they're strictly additive safety); the
lossy stages themselves delete content (GSM8K −8pp with its reasoning preset on) — **skip as defaults.** **Effort:** medium.

## 10. claude-code-router — `adapt-partial` (model-routing table shape)
**What.** An HTTP proxy (~24k★) you point Claude Code at via `ANTHROPIC_BASE_URL`. Re-routes each `/v1/messages` to a cheaper/stronger non-Anthropic
model by request shape, transforming to/from the target provider's API. Routing is the ORDO-relevant ~1%; the bulk is provider transformers + UI.

**How (the whole routing engine is one function).** `getUseModel()`: count tokens (tiktoken cl100k) over messages+system+tools, then a **fixed-priority
cascade** returning `"provider,model"`: explicit model wins → **longContext** if `tokenCount>60000` OR (last-turn input>threshold AND current>20000) →
a `<CCR-SUBAGENT-MODEL>` tag → **background** if model name contains claude+haiku → **webSearch** if any tool is web_search → **think** if
`thinking` is set → default. A session-usage LRU carries last-turn tokens. `CUSTOM_ROUTER_PATH` can replace the cascade. **No quality scoring, no
learning, no cost model** — a deterministic dispatch table on 5 cheap, statically-detectable signals.

**vs ORDO.** Directly the named "cheap-vs-strong by task" gap. ORDO has the signals (token count, hard-fork instinct) but not the dispatch mechanism.

**Take / risk.** Take the **routing table shape + signal set**, not the code: 5 signals (context-size threshold / reasoning-required / web-search-required /
background-cheap / explicit subagent override) resolved by a fixed priority cascade with a hard default, plus the longContext heuristic. Codify as a
tiny declarative `route:` block in the spec. **Overlap:** low-to-moderate — the proxy belongs to no pillar (scope-creep, not overlap); the one real
overlap is conceptual (the gates already do task-discrimination — routing must be a mechanical step *downstream* of the gate, not a competing classifier).
**Quality-loss:** real — routing is **lossy by construction**; crude signals can't tell a short-but-hard fork from a throwaway and silently degrade exactly
the cheap-looking calls. **Mitigation: opt-in like the glyph mode, default everything to the strong model, never auto-downgrade.** **Effort:** low for the
spec table + ~30-line resolver; high (and not worth it) for the proxy/transformers/UI.

## 11. claude-task-master — `adapt-partial` (decomposition data contract)
**What.** Turns a free-text PRD into a managed, dependency-aware task graph an agent works through: generate N tasks → score complexity 1-10 → expand complex
ones into subtasks → answer "what's next" respecting deps + priority. npm CLI + MCP server + Claude Code plugin. Also a `claude -p`-per-task executor + a
self-correcting loop mode.

**How (prompt+schema, no clever algorithm).** (1) **parse-PRD** — a Handlebars prompt asks for ~N tasks as JSON, validated by Zod; hard rule baked in:
**"a task can only depend on lower IDs"** → the dependency graph is a **DAG by construction**. (2) **analyze-complexity** — feed the task array back,
get `{complexityScore, recommendedSubtasks, expansionPrompt, reasoning}`; the clever bit: the complexity pass **pre-writes the breakdown prompt**. (3)
**expand-task** — `finalSubtaskCount = arg ?? recommendedSubtasks ?? default`, reusing the stored expansionPrompt → complexity **gates** decomposition depth.
(4) **find-next-task** (pure function, zero AI) — prefer an eligible subtask of an in-progress parent, else top-level; eligible = pending/in-progress AND
all deps complete; sort by `priority → fewest deps → lowest id`. Executor just `spawn()`s the CLI per task; the loop runs K iterations with a progress file.

**vs ORDO.** The named gap is "task decomposition **FORMAT**" — and the **schema** is the one thing worth taking. ORDO already has stronger *measured*
versions of the executor/loop (autonomy gate + REFEED).

**Take / risk.** Lift **only the data contract** as an output-format spec: `{id, title, deps (lower-id-only DAG), priority, complexityScore, testStrategy,
status}`, the **decompose → score → expand-by-score** contract with the **pre-written expansionPrompt**, and the pure `priority→deps→id` next-task selector.
The embedded per-task **testStrategy** field forces evidence-gating *at decomposition time* — aligns with the test-gated pillars. **Overlap:** high on
everything except the format (executor/loop ≈ autonomy gate; progress-file ≈ ledger; complexity prompt ≈ evaluation gate). **Quality-loss:** low for the
schema; two risks if over-adopted — the lower-id invariant can mis-rank parallel work and the next-task picker **returns null on deadlock (looks like done)**;
single-pass deps/complexity are hallucination-prone. **Take the format, not the trust model.** **Effort:** low.

## 12. claude-code-templates — `adapt-partial` (cost reader + packaging hint)
**What.** Two things bolted together: (1) a component-catalog **installer** (`npx … --agent X --command Y --mcp Z`) that fetches ready-made `.claude/`
config files; (2) a local **analytics dashboard** (`--analytics`) tailing Claude Code session logs for live tokens + $ + state.

**How.** **Installer:** `downloadFileFromGitHub` → `raw.githubusercontent.com/.../components/<type>/<name>.md` → write into `.claude/`. Pure fetch-and-place,
no transformation. **Analytics:** tails `~/.claude/projects/**/*.jsonl`, reads the **real** `usage.{input,output,cache_*}_tokens` Anthropic writes per message
and sums (`calculateRealTokenUsage`); **cost** = a **hardcoded flat per-million map** (input×$3, output×$15, … labeled "Sonnet 4.5") regardless of which model
ran. Session state = heuristic substring-matching (`tool_use`/`error`).

**vs ORDO.** Same JSONL-usage insight as #1/#7 (the P3 substrate). The installer/catalog is the wrong shape for ORDO (it distributes static prompt files; ORDO
is a runtime+spec).

**Take / risk.** Lift the **read-only cost/token reader** (~50 LOC) — but **key the price map by the per-message `model` field** (their code ignores it and hardcodes
one rate; do not copy that bug). **Overlap:** the installer ≈ ORDO's packaging goal but wrong mechanism (skip); token-summing is additive to the token-output pillar.
**Quality-loss:** none for the reader (read-only); their flat-rate $ is *wrong across models* — fix by keying on `model`. The heuristic state detector is unreliable —
do not adopt it as a loop-fingerprint source (the autonomy gate's real `(tool,args,result)` detector is strictly better). **Effort:** low.

---

## Cross-cutting conclusions
1. **Three repos triangulate the P3 fix** (ccusage, agentgraphed, claude-code-templates all read Anthropic's own `usage.*` from JSONL) → highest-confidence add.
2. **The compression/trim repos (rtk, llmtrim, context-mode) overlap ORDO's owned inbound/output/ledger layers** and import quality risk → take only their *gate principles*
   and *lossless recipes*, refuse the lossy engines.
3. **The code-graph repos (graphify, codegraph) fill the one empty ORDO layer** → adopt as an external provider + codify the AST-first/budgeted-render/confidence-tag pattern.
4. **The routing + decompose repos give transferable contracts** (a 5-signal table, a task-node schema) but their *runtimes* duplicate the autonomy gate → take the shape, not the loop.
5. **The skills repos (karpathy, obsidian) are packaging exemplars, not mechanisms** → karpathy is refused outright (contradicts act-don't-survey); obsidian's negative-trigger + 3-tier
   convention informs `/ordo` packaging.

See [`ADD-PLAN.md`](ADD-PLAN.md) for the prioritized 6-phase implementation.
