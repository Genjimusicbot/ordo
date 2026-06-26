# ORDO build log

Every phase records: WHAT was built, HOW, what was CHECKED/VERIFIED (with the measurement), and what
is OPEN. No saving is claimed without a `tokcost.py` number; no symbol ships without a meaning.

## P0 — genesis (2026-06-24)
- **What:** repo init (`git`, `main`); `README.md` (entrypoint + Pliny/GLOSSOPETRAE + LLMLingua
  grounding + the two-concept split + the four design laws); `DISCLAIMERS.md` (not-magic, tokenizer
  caveat, compute-vs-count, lossless-goal, spec-must-be-present, private-only safety, provenance);
  `docs/method.md` (lineage, design laws, grammar shape, build phases); `tools/tokcost.py`.
- **How:** scaffolded the language-first structure (`docs/ spec/ examples/ tools/`); installed
  `tiktoken` to measure real token cost.
- **Checked/verified:** `tiktoken` present (`cl100k_base`, `o200k_base`); `tokcost.py` runs and
  reports per-glyph costs.
- **Open:** the alphabet, grammar, writing system, skillstone, round-trip validation.

## P1 — the alphabet (28 core directives) (2026-06-24)
- **What:** `spec/lexicon.md` + `spec/lexicon.tsv` — 28 core directive glyphs (the highest-frequency
  LLM command tasks), each a tokenizer-validated single glyph with a precise meaning + English
  expansion + mnemonic.
- **How:** measured a candidate pool (lowercase/uppercase Greek, math operators, arrows, marks, runes,
  misc) on `cl100k_base` + `o200k_base` via `tokcost.py`; admitted ONLY glyphs that are 1 token in
  BOTH; assigned by mnemonic + task frequency. Default directive = answer (no glyph for the commonest
  act). Composition over minting (simplify/proofread/optimize are composed, not new glyphs).
- **Checked/verified (the empirical record):**
  - All 28 chosen glyphs re-measured = **1/1 token** (cl100k/o200k). PASS.
  - Net savings confirmed vs the English phrase each replaces: σ saves 4 tokens, π 6, φ 5, ★ 8,
    τ 2 (cl100k). Real, measured, not asserted.
  - **Key finding: runes = 3/3 tokens** (the most expensive of everything measured), so the popular
    "command runes" instinct is rejected for the wire format; runes are an optional display skin only.
  - Uppercase Greek = 2/1 (cl100k penalty) -> lowercase chosen even where uppercase is more mnemonic.
- **Open:**
  - **In-context cost** — single-glyph cost is the admission filter; full ORDO *sentences* (multiple
    glyphs + operands adjacent) must be re-measured in Phase 4 (BPE merges differ in context).
  - **Claude/Gemini tokenizers are proprietary** — costs are GPT-proxy; re-validate on target model.
  - Modifiers, operand type-tags, epistemic markers, chaining = Phase 2 (`grammar.md`).
  - Lossless round-trip gate over a task set = Phase 4.

## P1.5 — the maximal glyph pool (cross-script, non-human-readable) (2026-06-24)
- **What:** `spec/glyph-pool.tsv` — the maximal set of single-token glyphs harvested across ~46
  Unicode blocks (all major scripts), cross-bred and deliberately non-human-readable (per the
  GLOSSOPETRAE L3 finding that illegibility is fine for an AI reading from a spec). The raw material
  the alien alphabet is assigned from.
- **How:** `tools/glyphpool.py` enumerates candidate codepoints across Greek/Cyrillic/Armenian/Hebrew/
  Arabic/Syriac/Georgian/Devanagari/Bengali/Tamil/Thai/Lao/Tibetan/Myanmar/Hiragana/Katakana/Bopomofo/
  Hangul-jamo/Kangxi/CJK/Yi/Tifinagh/Runic/Ethiopic/Cherokee + math/arrows/symbols/braille/box/blocks;
  filters control/combining/space/unassigned; measures each on cl100k + o200k; classifies.
- **Checked/verified (measured):**
  - **Tier A (1 token in BOTH cl100k+o200k) = 511 glyphs; Tier B (1 token in o200k only) = 1163;
    full pool = 1674.** Written to `spec/glyph-pool.tsv` (glyph, codepoint, block, costs, tier, name).
  - Cross-bred 12-glyph alien string `άРіنหまバ了倍单因密` = **12 tokens** (1 per glyph) in both
    tokenizers, and unreadable by any human. Proof the cross-script alphabet is both efficient and
    illegible.
  - Richest blocks: CJK unified (201 A / 524 B — morpheme-dense ideographs), Cyrillic (58/64), Kana
    (96/54), Arabic (36/78), Thai (31/22), Greek (27/36), Hebrew (14/13).
- **Design note:** literal *composite*/combining glyphs (ligatures, bind-runes, combining marks) are
  excluded — BPE splits them into MORE tokens. "Cross-breed" = freely mix single glyphs from all
  scripts, not fuse codepoints.
- **Open:** Claude/Gemini tokenizers proprietary (GPT proxy; Tier B especially may differ on Claude);
  in-context adjacency re-validated in Phase 4; the ALPHABET ASSIGNMENT (which alien glyph maps to
  which directive/operand/modifier) is the next design step, drawing from this pool.

## P1.6 — the compression matrix (frequency x token-cost) (2026-06-24)
- **What:** `tools/freqmatrix.py` + `spec/word-matrix.tsv` + `spec/phrase-matrix.tsv` +
  `spec/compression-map.md` + `spec/compression-map.tsv` — a measured ranking of WHICH words/phrases
  are worth glyphing (by total token savings = frequency x tokens-saved), and the 27-phrase map.
- **How:** real Zipf frequencies via `wordfreq`; measured running-text (space-prefixed) token cost on
  cl100k + o200k; scored each item in "tokens saved per 1M words"; assigned the top phrases to CJK
  morpheme glyphs (mnemonic + repurposed: 因=because, 例=for example).
- **Checked/verified (the empirical record):**
  - **Single-word layer is a dead lever:** of ~29k real words, only 35% are multi-token in o200k;
    glyphing ALL of them = **~3.3%** of a token stream, and the top items are PROPER NOUNS (February,
    Jesus, Russia) -> useful word lever **~1%**. Measured, surprising, and it kills the obvious
    "swap common words" plan.
  - **Phrase layer is the real vocabulary lever:** 27 collocations mapped to CJK glyphs, every glyph
    re-verified **1/1 token**, no decode collisions, avg **1.59 tokens saved/use** (max 3: "at the
    same time" 同, "on the other hand" 反).
  - Caught + fixed 6 candidate glyphs that were 2-token in cl100k (故须凡顾差 + 譬) -> swapped for 1/1
    (则确总量异) before shipping. The gate worked.
  - Conclusion recorded in the doc: effort goes to **phrases + command structure + verbosity**, NOT
    single-word substitution.
- **Open:** phrase frequencies are coarse estimates (refine from a real corpus); CJK 1-token cost is
  o200k/cl100k-proven, Claude tokenizer unverified (Phase 4); the directive+phrase layers stack but
  sentence-level net savings measured in Phase 4.

## P1.7 — full glyph allocation + mathematical verification (2026-06-24)
- **What:** allocated the entire glyph pool to the highest-value items and MEASURED the realized
  saving on real text. `tools/allocate.py` (build + verify), `spec/candidates.json` (3,144 harvested),
  `spec/master-map.{tsv,md}`, `tests/corpus/{prose.txt,code.py,prompts.txt}`.
- **How:** a 15-domain parallel harvest workflow (prose/code/prompt/jargon/cli/sql/...) produced 3,144
  multi-token candidates; folded in ~25k multi-token words from `wordfreq`; ranked all by
  `value = freq × (tokens−1)`; greedily assigned all 1,637 free glyphs (Tier-A to the top, Tier-B to
  the tail); then encoded real corpora, applied substitutions, re-encoded, compared.
- **Checked/verified (the math, exact):**
  - **Real technical text (40 files, 18 py + 22 md): Tier-A buys +0.73% o200k / +0.43% cl100k.** Under
    1%. The 1,600-glyph vocabulary layer is a weak lever on actual code/docs.
  - **General prose (case-folded): Tier-A +5.40% o200k / +4.20% cl100k.** The high end, connective-rich.
  - **Full A+B map: +2.52% o200k but −2.15% cl100k** — Tier-B glyphs (1 tok o200k, 2-3 tok cl100k)
    ADD tokens on the older tokenizer. Cross-tokenizer trap; rejected as default.
  - Marginal curve: top-400 ≈ 52% of estimated value, top-800 ≈ 75%.
- **Verdict (redirects the project):** vocabulary substitution = ~1-5% lever, register-dependent and
  tokenizer-fragile; NOT where the big gain is. Ship Tier-A (501 glyphs) as a minor opt-in; flag
  Tier-B o200k-only. The real levers are GRAMMAR (structure) + VERBOSITY (output). The math confirms
  the intuition: do the grammar next.
- **Open:** Claude tokenizer proxy (the cl100k/o200k split on Tier-B is the warning sign); ranking
  freqs estimated (verification is real); sentence-level savings with the directive grammar stacked =
  measured in P2/P4.

## P2 — the grammar (ORDO-G), designed + decode-tested (2026-06-24)
- **What:** `spec/grammar.md` (the determinative structure layer), `tests/prompts-benchmark.txt` (20
  real verbose prompts) + `tests/prompts-ordo.txt` (their ORDO encodings).
- **How:** a 4-way divergent design panel (positional / determinative / RPN / hybrid) scored by 3
  adversarial judges on compression + zero-shot decodability + parse-determinism (the first two
  weighted 2x). The **determinative grammar won (8.0)** — silent type-tags make word order free and
  parsing unambiguous; whitespace is banned (it costs a token). Then an empirical **zero-shot decode
  test**: 3 fresh agents read the spec cold and expanded 20 ORDO commands; a judge scored fidelity vs
  the hidden originals.
- **Checked/verified (measured):**
  - **Compression: 20 real prompts 437 → 285 o200k = 35% (cl100k 35.5%)**, avg 21.9 → 14.2 tok/prompt;
    benchmark 32 → 11 (66%). Both tokenizers agree. **~7-10x the vocabulary layer's ~1-5%** — the
    grammar IS the lever, as the matrix predicted.
  - Every glyph + the example encodings re-measured 1/1 (two came out cheaper than the design claimed).
  - **Decodability v1 = 1.63/2 mean**, and the test EARNED its keep by exposing real bugs: a `信`
    double-assignment (JSON + certainty) that made all 3 decoders agree on the WRONG meaning (proof
    that high agreement ≠ correctness), unitless numbers ("80"→"80 items" not words), `↓` overload,
    `×` ambiguity, droppable format glyphs.
  - **Fixed → v2 = 1.70/2 mean, 3% wrong:** `构` for JSON (collision gone), count-units (字/行/段/分/页/
    节/项), and a decoder contract (§7b). The catastrophe (#9) now decodes as JSON across all 3; units
    land; the overload is gone. The faithful core — verbs + 心/据/加/¬/调/业 + literals — decoded
    cleanly across 3 independent agents = genuinely **zero-shot legible**, not an author-only cipher.
  - **Residual (honest):** mostly UNDER-ENCODING (encoder trading fidelity for brevity on #3/#5/#7),
    not a language defect; plus 2 glyph-semantic fuzzy spots (※ extract-vs-summarize, × constraint)
    now clarified in spec §7b + an encoder-discipline note. Stopped at 1.70 — the last tick to 2.0 is
    not worth it.
- **Open:** decode tested on the workflow model — Claude main / other models may differ (re-test per
  target); a larger prompt set; the RUNTIME/harness that applies ORDO (the separate second concept,
  later); the VERBOSITY/output layer (the biggest remaining lever, later).

## P3 — the output layer / framework (format + verbosity) (2026-06-24)
- **What:** `spec/output.md` (the output framework) + `tools/formatbench.py`. Answers "is JSON best?"
  and "is there a compressed JSON?" with measurement, and integrates the verbosity layer (ponytail +
  caveman) — the user's "whole framework including ponytail + compression + caveman".
- **How:** measured 8 serialization formats across 4 data shapes (`formatbench.py`); measured ponytail
  + caveman on real samples; ran a read-accuracy comprehension workflow (JSON vs TSV vs TOON).
- **Checked/verified (measured):**
  - **Format is shape-dependent, and pretty-JSON is the worst everywhere.** Uniform array: TSV −59% /
    TOON −44% vs minified JSON; numeric table: TSV −51%; nested/heterogeneous: minified JSON wins
    (TOON +22%, YAML +31% are WORSE). YAML is a token trap. Minifying JSON alone saves 47-66%.
  - **Compression does no harm to comprehension:** JSON/TSV/TOON all scored **100% (16/16)** on 8
    factual questions × 2 readers, including multi-row sum + boundary cases. (Caveat: small clean
    single-table test.) So the ~55% tabular saving is real, not a false economy.
  - **Verbosity is the biggest lever:** ponytail (cut preamble/restate/closer/meta) = **77% off a
    typical answer, LOSSLESS**; caveman (terse register, operational text only, never explainers) = 68%
    off. These dwarf the ~35% input-grammar saving because output dominates the bill.
  - The framework = one decision: pick FORMAT by shape (never pretty-JSON) → always PONYTAIL (lossless)
    → CAVEMAN operational-only → honor ORDO directive overrides (↑/全 suspend caveman, 段 forces prose).
- **Open:** read-accuracy on large/multi-table/ambiguous data; a TOON encoder edge cases; the RUNTIME
  that actually applies all this (the separate harness concept); P4 skillstone (one-paste ORDO.md).

## P4 — the skillstone (`ORDO.md`), validated (2026-06-24)
- **What:** `ORDO.md` — one self-contained paste-in file that teaches any LLM the whole stack
  (directives + grammar + phrase glyphs + decode rules + the output framework) in one shot. README
  rewired to make it the entrypoint.
- **How:** distilled `lexicon.md` + `grammar.md` + `output.md` into a single lean spec; measured its
  cost; re-ran the zero-shot decode test giving 3 fresh agents ONLY this file.
- **Checked/verified (measured):**
  - **Cost: 1,917 tokens** for the complete language + output framework. Paid once (cacheable); the
    output-verbosity savings amortize it in a handful of responses.
  - **Single-file decode = 1.75/2 mean (105/120), 14/20 fully faithful — EDGES PAST the 3-file run's
    1.70.** Consolidating to one file improved fidelity, didn't cost it. D1/D3 agreed 19/20.
  - Only 1 genuine decode error in 60 (a decoder flipped ×remove vs 据preserve); the rest are
    encoding-ceiling losses transmitted CONSISTENTLY by all 3 decoders (the file teaches consistent
    decoding). Fixed the one soft spot: pinned `×` vs `据` as opposites with a worked example (judge
    predicted → ~1.85+).
- **Open:** re-validate the × / 据 fix on a future run; per-target-model decode (tested on the workflow
  model); the RUNTIME/harness that auto-applies ORDO (the separate second concept).

## ADAPT run — P5/P6 (2026-06-24): research, deanchor verdict, the harness
- **C1 · research synthesis** (`docs/research-synthesis.md`): 20 docs → 63 mechanisms → 12 ranked
  beyond-token-density levers, each graded by confidence (only 7/63 "measured"). Honest caveats: no
  measured speed win, +36pp is a single-source LEAD, single-word lever dead, exotic glyphs token-negative.
- **C2 · DEANCHOR VERDICT = readable wins** (measured): English 437 / readable-ORDO 297 (**+32%**) /
  glyph-ORDO 285 (**+35%**) o200k — glyphs buy only **3pp**. Blind decode: **readable 2.00/2 (perfect,
  60/60)** vs glyph 1.95 (glyphs silently mis-decoded 心金→"key problem", dropped τ码 — confident-wrong,
  the worst failure mode). Glitch screen clean (all glyphs well-learned tokens). **Decision: readable-
  terse is ORDO's default wire format; glyphs are an opt-in dense mode for proven-round-trip commands
  where token cost dominates.** The grammar STRUCTURE delivers the 32%; the glyphs were costing
  reliability for ~0 token gain. (Pending: C4 will test whether glyphs add hard-task QUALITY, the +36pp
  lead — if not, readable wins outright.)
- **C8 · the harness** (`harness/`): `ordo.py` = a deterministic table-driven ORDO-G decoder
  (parse→AST→English, dual-use 码/段 resolved by position, unknown glyph → literal never errors);
  `output.py` = the output-contract enforcer (TSV for uniform records, minified JSON else, filler
  flagged). `test_ordo.py` **8/8 green** incl. round-trip coverage over all 20 benchmark prompts. The
  measurement instrument every remaining experiment runs through.
- **C3 · ≥10% floor (PASS, far over).** 3 realistic end-to-end exchanges (prompt + produced output),
  English vs readable-ORDO+output-contract: 495 → 178 o200k = **64% combined**. Even the explainer
  (substance kept, only filler cut) = 51%; structured/operational = 70-72%. Output dominates.
- **C4 · quality (PASS — ORDO exceeds English).** Blind A/B, 9 stratified tasks, judge scored which
  output better satisfies the task ignoring length: **ORDO 6 wins / 2 ties / 1 loss.** The gain is
  STRUCTURE-driven with *readable*-ORDO (no exotic glyphs) — the structured prompt produced more
  on-target answers on the hard tier. The one loss (e2) was an encoding error (the ORDO prompt dropped
  "one sentence"), not a quality deficit. So the +36pp "glyph" lead reproduces as a *structure* lead,
  the cleaner and more honest finding.
- **C6 · speed proxy (PASS).** Output tokens 6,468 → 4,423 = **~32% fewer** overall (≈48% excluding one
  over-delivery outlier where a mis-set audience tag made ORDO answer longer). Most tasks 39-66% fewer
  output tokens from the ponytail+format contract. Reported as an output-token saving, NOT a proven
  wall-clock win (per the research caveat).
- **C7 · intent-as-symbol (`spec/macros.md`).** 16 whole-intent macros (the user's "sentence = symbol"):
  avg 8.2-token instruction → 1.4-token readable code, **6.8 saved/use**; readable (deanchor) so they
  decode reliably and double as a quality lever (a 1-token `cot`/`srev`/`risk` reliably triggers a
  strong reasoning mode). **Decode test: 1.8/2 (54/60) → C7 PASS** (only weakness: bare-subject
  `this gap` drops the implicit "answer this"; fixed by reading a macro as additive).
- **C5 · hallucination (PASS — honest null + calibration).** Two runs (v1 obvious-fictional, v2 harder
  invention-bait + false-premise traps): on a strong frontier model BOTH arms scored **0 confident-
  wrong, 0 false-premise-affirmed, 0 invention** — the plain baseline is already at the floor, so the
  epistemic layer showed **no measurable confident-wrong reduction**. But it **does not backfire** (the
  VOKU trap: never stamps "verified" on a falsehood) and showed a **better-calibrated posture**
  (abstained on genuine-uncertainty recall items where plain volunteered luck-of-recall specifics). The
  reduction benefit would surface on weaker models (per GLOSSOPETRAE's "gains concentrate on weaker
  models"). Recorded honestly, not oversold.
- **C9 · VERDICT (PASS — terminate).** `VERDICT.md` = every measured number + the explicit cut list +
  the recommendation (readable grammar + output contract + macros + harness). `ORDO.md` banner now
  states readable-default / glyph-opt-in. Harness gate 8/8 green.

### ADAPT termination: SUCCESS — 9/9 criteria green
ORDO's value is **grammar structure + output discipline**, not exotic glyphs. ~64% end-to-end token
save AND blind-judged quality ≥ English (6-2-1), with honest nulls (no wall-clock speed proof, no
hallucination reduction on a saturated frontier baseline). The deanchor reframe was correct and is now
the default. Built, measured, audit-ready.

## Inbound layer — headroom integration (2026-06-24)
The third side of the token triangle: compress what the model READS (docs/tools/logs/code/history),
not just the command (grammar) and the response (verbosity). Integrated `headroom-ai` 0.27.0
(Apache-2.0) — cloned, read the source, installed the pip package + onnxruntime, measured on our content.
- **`harness/inbound.py`** — take-best-of {headroom, our TSV/whitespace} per content, with an
  inflation guard; `docs/pipeline.md` (the 3-stage architecture + 9 novel inbound levers);
  `tools/pipeline_recalc.py` (the pool-weighted total).
- **Measured (not the marketing 90%):** logs/tool-output **92%** (headroom — its real sweet spot),
  structured JSON **55%** (OUR TSV; base-headroom noop'd it), code 7%, dense prose **0%** (Kompress ML
  needs onnxruntime and is lossy+modest). **Take-best mixed inbound = 45%.**
- **Recalculated full-pipeline total:** realistic agent turn **~47% combined**; log/tool-heavy **~88%**;
  dense-prose-library **~13%** (inbound resists → output + novel levers carry it).
- **Honest finding:** headroom's 92% is **lossy SAMPLING** ("[40 matches compressed to 5. Retrieve
  more: hash=…]" + CCR retrieval) — gist-preserving, aggregate-lossy. Routing rule: lossless TSV when
  the model must ANALYZE; headroom sampling only for SHAPE-only context. "90% on docs" = "90% on
  redundant agent context," not dense prose. Headroom's output-verbosity overlaps our ponytail, so we
  do NOT double-stack; headroom owns inbound, ORDO owns command, our layer owns output.
- **Novel levers identified (beyond headroom), 2 that compose with ORDO:** glossary-inward (apply our
  phrase/macro map to documents) and relevance-gating (LongLLMLingua's +17% RAG — compression that
  IMPROVES quality). JIT/don't-send-it is the biggest but belongs in the auto-apply runtime.

## The pillars framework — multi-pillar, test-gated (2026-06-24)
User reframe: token length is ONE pillar; the goal is a cleaner/less-hallucinated/more
architecturally-honest system where reduced rework is *calculable*. Lossless-first; every pillar
test-gated, never theoretical.
- **`spec/pillars.md`** — 8 pillars, each with metric + gate + baseline: P1 context-length, P2 token-
  output, P3 speed (real wall-clock, not proxy), P4 quality, P5 hallucination, P6 tidyness, P7
  architecture (rebuild-vs-fix), P8 rework-reduction. Rule: a compression % counts only if its
  comprehension/quality gate passes.
- **`tools/pillars.py`** — the scoreboard; runs deterministic gates live. Current: **5/8 MEASURED**
  (P1 lossless-TSV 68% / mixed 45%, P2 ponytail 77%, P4 6-2-1, P5 no-backfire+calibration, P6 filler-
  flag), P3 PROXY-ONLY (real wall-clock TODO), P7+P8 UNMEASURED → gated by the P7/P8 workflow.
- **Behavioral "do it good" macros** (`spec/macros.md`): `arch` (rebuild-vs-fix, saves 29/use), `fresh`
  (skip the averaged answer, 21), `tidy` (smallest correct thing, 20) — token-cheap levers for the
  pillars a token count can't touch (P4/P7/P8). Effect test-gated, not assumed.

## GLOSSOPETRAE × pillars + the REFEED framework (2026-06-24)
Took Pliny's GLOSSOPETRAE (cloned, read FINDINGS/PAPER) and ran one analysis per pillar (9-agent
fan-out, high-effort, honest verdicts), excluding the covert-channel/stego arm (refuted +
policy-blocked by its own authors; conflicts with our DISCLAIMERS). `docs/glossopetrae-pillars.md`.
- **Verdicts (honest, agents tokenized to verify):** P1 context **NULL** (opaque surface INFLATES
  tokens — glyph-soup ~2× conlang, several× plain English; opacity is the wrong axis). P4 quality
  **REAL-LEVER** (forcing the model off the familiar English surface improves hard-task STRUCTURE —
  AST-graded gap persists; the rigorous core of +36pp). P8 **LIMITED→strong as evaluation**
  (contamination-free per-eval = un-gameable test gates). P2/P3/P5/P6/P7/P9 **LIMITED** (surface
  density doesn't transfer to NL, doesn't help speed; re-confirms the deanchor).
- **Bottom line:** GLOSSOPETRAE is a QUALITY + EVALUATION insight, not a compression one. The value is
  captured by the framework, not by glyphing the surface.
- **`spec/framework.md` — ORDO REFEED**, the Fable-style multi-pass refeeding loop: classify→write the
  DONE contract (gate/target/budget) up front (the de-anchor)→hold format constant→draft→REFEED a TYPED
  verdict (not praise)→DECIDE (refeed the DELTA, not the transcript)→STOP on target/budget/no-progress/
  marginal-quality-per-token floor→EMIT (honest if not done). P9 metric = Q/T (final-pass quality ÷
  total tokens across all passes). Wins on HARD tasks (~3.4→1 passes); pure tax on easy (Kmax=1
  default). The disciplined antidote to brute-force token-furnace looping.
- New pillar **P9 (long-form/loop quality)** added to `spec/pillars.md` + scoreboard (9 pillars now).

## Two new gates — experimentalist (dual-perspective) + autonomy (2026-06-25)
Extending the framework with two quality/safety gates, from the user's KLADDS agentic feed.
- **Experimentalist gate** (`spec/experimentalist-gate.md`): repurposed the house `experimentalist`
  divergence skill (frame win-condition → up to 5 genuinely-distinct approaches → adversarial score →
  pick winner → graft) into a GENERALIZED, GATED dual-perspective mode for HARD coding tasks. Runs two
  arms — gated-conventional (REFEED) ∥ experimentalist (divergent) — then SYNTHESIZES best-of-both and
  acts. The gate (the integral decision) fires only on hard/advanced/real-fork tasks; deterministic
  single-answer tasks skip it (divergence there is theatre). Coding divergence methods (invert-obvious,
  change-paradigm, steal-from-far-field, remove-required, exaggerate, constraint-roulette, change-POV).
  Test-gate running: does synthesized(conv+experimentalist) beat conventional-alone on hard forks?
- **Autonomy gate** (`spec/autonomy.md`, DONE — 57 patterns, codebase-grounded): a STRICT long-form
  agentic-autonomy framework. The agents read the REAL KLADDS infra (strand_runner, autonomy.py,
  retry.py, mailforge, cadence_runner, assistant_agentic, routes_autonomy) so it is specific, not
  generic. **9 loop steps** (GATE-PRE→select-shape→plan→act[fingerprint+propose-only]→observe→verify→
  escalate[ADAPT ladder]→write/freeze→terminate-check). **9 kill conditions** (no-progress/livelock,
  oscillation+thrash via (tool,args,result) fingerprint, runaway step-cap, wall-clock SIGKILL,
  idle/heartbeat, budget fail-closed, CAMPAIGN runaway [50 strands chaining = 4hr], deferral ceiling,
  retry-storm circuit-breaker, manual kill). **11 error rules** (transient-vs-terminal taxonomy, backoff
  +full-jitter, idempotency-key exactly-once, checkpoint/journal resume, partial-failure isolation,
  dead-letter, fail-open-vs-fail-closed per-field, kill-switch+wallet, escalation watchdog, model
  fallback). **Termination is PROVABLE** (monotone-green + hard caps).
- **ACTIONABLE GAP it surfaced (real fix for KLADDS):** the framework's correctness leans on
  **(tool,args,result) loop-signature fingerprinting** — the ONE guard the codebase does NOT yet own.
  Today `assistant_agentic` exhausts silently into a truncated answer with no loop-cause logged, and
  oscillation is only caught by the coarse 25-step ceiling (~24 wasted identical turns can burn first).
  Highest-value add: catches a stuck loop in ~3 reps. Flagged for a follow-up.

## Capstone — evaluation gate + orchestration + the operating profile (2026-06-25)
The three pieces that make ORDO a single full-fledged tool (compression + quality + creativity + speed +
persistence), all honest-first.
- **Evaluation gate** (`spec/evaluation-gate.md`): an `ultra-analytics`-style honest-judgment SOP,
  generalized to technical/code artifacts, callable as a step. Debias law (judge the REAL goal, never the
  prompt; a match to a weak brief is LOW); structure-over-cosmetics; **optimal-band law (10 ≠ the target —
  over-engineering scores DOWN, the right-scoped 9 is optimal)**; honest pros AND caveats; reproducible.
  **VALIDATED:** applied to {right-scoped, over-engineered, plausible-but-wrong} solutions it scored 9 / 3
  / 0 — penalized over-engineering, refused to credit the plausible-wrong answer, withheld 10 from the
  optimal one. The anti-sycophancy contract, working.
- **Orchestration** (`spec/orchestration.md`): ledger-based multi-agent delegation — when to fan out,
  the append-only ANCHOR/PROGRESS ledgers (state out of context, resumable), single-writer orchestrator,
  **handoffs-as-pointers not payloads**, the approval queue, pipeline-vs-barrier, adversarial-verify, and
  the git/file discipline. Codifies how this whole build was actually run.
## Productionization + go-live (2026-06-25)
Critical round (the user asked me to be critical first): **dogfooded ORDO's own evaluation gate on
ORDO-as-a-product** → an independent agent scored it **6.5/10**, naming the real holes (not installable;
~1 part runnable / ~4 parts markdown marketed as an engine; scoreboard overclaimed "8/10 MEASURED" vs
docs' "7/8" with agent-judged pillars stamped MEASURED and P2 printing 77% but computing 67%; Windows
UTF-8 crash; GPT-proxy/one-model). Published unedited as `docs/SELF-EVAL.md`. Then FIXED the top holes:
- **Real npm package** (`ordo-llm`): `package.json` + `src/index.js` (faithful JS port of the
  deterministic core — `decode`/`emit`/`bestFormat`/`compressInbound`/`ponytailFlags` + spec loaders) +
  `bin/ordo.js` CLI + `test/test.mjs` **11/11 green** + `examples/basic.mjs` + MIT `LICENSE`. Genuinely
  `npm install`-able and runnable.
- **Honesty gap closed (the #1 fix):** README rewritten to lead with the honest scorecard and split
  RUNTIME (real code) from METHODOLOGY (the gates = prompt SOPs, loaded as text, not executed);
  `pillars.py` now tags each pillar by evidence tier (COMPUTED / AGENT-JUDGED / GROUNDED / PROXY-ONLY),
  P2 prints its computed number, the tally is consistent. Windows UTF-8 stdout forced in the glyph
  scripts.
- **AI-usage docs:** `AGENTS.md` + `llms.txt`; **reproducible `BENCHMARKS.md`** (computed vs agent-judged
  with reproduce commands).
- **Still open (honest roadmap, in SELF-EVAL):** commit the decode/quality eval transcripts; measure on
  a non-GPT tokenizer; harnesses for P10/P3.
- **Went live:** pushed to a public GitHub repo (MIT).

## Context-rot gate — complexity-adaptive compaction + ledger (2026-06-25)
The user's adaptive-compaction idea, grounded in the literature and built into the framework.
- **The research (sourced):** Chroma **Context Rot** (2025) — a 200K model degrades meaningfully at
  **~50K**, non-uniform, even on trivial tasks; LongMemEval ~30-60% gap focused-vs-full. **Lost in the
  Middle** (2023) — U-shaped position bias, middle dips ~20pp and can fall BELOW the no-context baseline.
  **RULER** (2024) — effective context ~50-65% of advertised. **NoLiMa** (2025) — under associative
  reasoning Claude 3.5 −57.8pp at 32K, most effective lengths capped ~2K. NIAH overstates ability.
- **`spec/context-rot.md`** — the gate. **Complexity classifier** (5 triggers: horizon >15-20 tool
  calls / breadth >5 files / load-bearing facts / irreversibility / projected-fill >50%) routes complex
  work to the LEDGER+compaction track, simple work to standard (no overhead). **Compaction policy**:
  warn 70 → flush+checkpoint 85 → hard-compact 90 (95%-auto fires too late to have room to summarize),
  plus a degradation-signal trigger (distractor density / self-contradiction / middle-placement). **Keep
  at the high-attention EDGES** (anchor re-seated at HEAD, green criteria, load-bearing facts, recent
  files at full fidelity), **drop tool-output FIRST** (70-80% of budget). **The rehydrate-gate (re-read +
  run the tests) is the non-lossy backstop that licenses lossy compaction.** Composes with what we own
  (ADAPT ledgers, autonomy state-out-of-context, handoffs-as-pointers, REFEED refeed-the-delta).
- **New pillar P10 (context-integrity)** added; status **GROUNDED** (the problem is measured by the
  studies; the gate's mitigation needs a long-context harness to measure, an honest gap like P3).
- **Honest limit:** compaction cannot recover what was never written to the ledger before being dropped;
  the rehydrate-gate only catches drift the tests detect.

## Capstone — evaluation gate + orchestration + the operating profile (2026-06-25)
- **`OPERATING-PROFILE.md`** (loadable as a system prompt / `CLAUDE.md`): the single spine that
  ties the full stack — the honest stance (10≠optimal, debias, lossless-first), COMPRESS (readable-ORDO +
  output contract + inbound), the 5 GATES (single/REFEED/experimentalist/evaluation/autonomy, classify
  first), the 9 PILLARS, PERSISTENCE+multi-agent, CREATIVITY — plus **the honest scorecard** (proven vs
  the NULLS we must never claim) and **the issues fixed this pass** (single entry-point, the eval SOP,
  multi-agent codified, readable-canonical, the P3 honest gap, the loop-fingerprint follow-up).
- **P7/P8 test-gate (measured, blind, 22 agents):** **P7 architecture** = `arch` directive +0.20
  (1.40→1.60 rebuild-vs-fix); reliably states a rebuild verdict + justification, lift concentrated where
  plain underperforms (the regex-HTML case), neutral where the model already re-architects or no
  foundation exists. **P8 rework** = `tidy/fresh` cut first-pass flaws **42% (7→4 across 5 tasks)** —
  cleaner first pass (capped pagination, safer exception defaults, honored the "safely" contract) = less
  downstream debug/cleanup; neutral on trivial tasks. **Scoreboard now 7/8 MEASURED** (only P3 real
  wall-clock proxy-only). The "do it good, not fast" ideanomics is validated as a measured pillar.

## The language is done (P0-P4). Next: the harness (separate concept)
P0 alphabet → P1.x pool/matrix/allocation → P2 grammar (ORDO-G, ~35%, decode 1.70) → P3 output
framework (format-by-shape + ponytail 77% + caveman) → P4 skillstone (`ORDO.md`, 1.75/2). The LANGUAGE
is built and measured end-to-end. The remaining piece is the **harness**: a runtime that auto-encodes
requests / auto-decodes ORDO / enforces the output contract, instead of relying on the model following
`ORDO.md` by hand. That is the separate second concept the project was always two-of.
P3 = the skillstone (a single self-contained `ORDO.md` a user pastes into any LLM to teach it ORDO in
one shot) + writing-system polish. Then the separate **harness** concept (the runtime that
auto-encodes/decodes + the verbosity layer). The language itself (P0-P2) is now real and measured.

## Competitive teardown → the 6 gap-fillers, shipped (2026-06-25)
A 13-agent source-level teardown of 12 public repos (ccusage, rtk, andrej-karpathy-skills, graphify,
obsidian-skills, codegraph, agentgraphed, context-mode, llmtrim, claude-code-router, claude-task-master,
claude-code-templates), each cloned + read at the engine level and judged through ORDO's own evaluation gate
(`docs/COMPETITIVE-TEARDOWN.md`). Result: 6 non-overlapping gap-fillers adopted, 6 overlapping layers refused
(rtk/llmtrim/context-mode compressors duplicate the inbound layer + import quality loss; karpathy/obsidian are
packaging exemplars not mechanisms; the installer/proxy products are whole products ORDO doesn't need). Plan in
`docs/ADD-PLAN.md`. All six shipped, gate green at each step:
- **P1 real cost/token/duration meter** (`tools/measure.mjs`, `ordo measure`): reads Anthropic's own
  `usage.*` + timestamps from Claude Code's JSONL (lossless billed counts — triangulated by ccusage +
  agentgraphed + claude-code-templates all reading the same fields), dedupe-keep-best, per-message-model
  LiteLLM pricing with date-strip/family/prefix/default fallback. `pillars.py` P3 auto-upgrades PROXY→COMPUTED
  once a paired A/B is recorded (`tools/measure-ab.json`) — honest, no over-claim.
- **P2 `/ordo` packaging** (`skills/ordo/SKILL.md` + `.claude-plugin/{plugin,marketplace}.json` + `ordo init`):
  the non-coder endgame — `/plugin marketplace add SprucetheAI/ordo` or `npx ordo init`, 3-tier progressive
  disclosure with negative triggers. Lossless, additive; removes the paste-a-1.4k-file friction.
- **P3 measured-revert gate** (`compressInbound` JS + `compress_inbound` Py + `spec/output.md` Part 4): every
  transform re-measured, reverted if it doesn't strictly shrink (worst case = passthrough); lossy cuts gated by
  `coverage_ok` (query-relevant terms must survive). Lossless-first as a mechanism, not a slogan.
- **P4 code-context contract** (`spec/code-context.md`): AST-first/LLM-only-for-prose, token-budgeted render,
  confidence-tagged edges; codegraph default / graphify multimodal as EXTERNAL providers. Navigation index, not
  source.
- **P5 decompose contract** (`spec/decompose.md`): lower-id-only DAG + per-node `testStrategy` +
  complexity-gates-expansion + pure next-task picker. Format, not a trust model.
- **P6 opt-in routing** (`resolveModel`): 5-signal cascade, default-strong, never auto-downgrade.
- **18/18 node tests + Python self-checks green.** Rename Genjimusicbot → SprucetheAI. No foreign runtime
  vendored; 5 of 6 are spec/packaging/one-script. **The discipline held: nothing lossy ships as a default.**

## Live A/B runs via the Max session — honest, partly self-refuting (2026-06-26)
Wired the harnesses to a headless `claude -p` bridge (`tools/local_model.py`, Max OAuth, no per-call cost) and ran
them live on Opus 4.8. The results refined the honesty, not the marketing:
- **goal-lock LIVE tier-one: net −3** (A_pass 4 / B_pass 1, **b_wins 0**). This is NOT a goal-lock verdict — it is a
  **harness artifact**: the tier-one keyword oracle is too brittle for a strong model (both arms write sensible
  answers; b_wins=0 means the oracle never credited a correctly-but-differently-worded re-derivation). Self-critique
  catch: my "COMPUTED, un-gameable" tier-one oracle is COMPUTED but measures keyword-presence, not correctness.
  Substance needs the tier-two cross-family JUDGE (PENDING). Caveat now printed by the harness.
- **route_truth model-extraction LIVE: abandoned** — 36 sequential `claude -p` spawns stalled and piled processes;
  too fragile to trust. The **deterministic** route_truth result stands as the solid COMPUTED finding (taxonomy
  complete; a naive keyword extractor at cost 31 is worse than always-strict at 17 because under-verify is 10×).
- **The cross-cutting honest finding:** the single-pass instinct A/Bs **do not cleanly measure as wins on a frontier
  model** (verify-assert wash + goal-lock noise + oracle brittleness) — the Reflexion pattern (self-correction is
  emergent in strong models) showing up in ORDO's own instincts. This is *good* for the v2 product: the bold,
  cleanly-measurable claims are **compression + bundled tooling + auto-activation**, NOT a quality-gate magic that
  washes. The page rides the proven, the instincts stay opt-in at their true tier.

## Improvement charter EXECUTED — the foolproof harnesses built (2026-06-26)
Built everything the charter (`docs/IMPROVEMENT-CHARTER.md`) designed; ran the one that lands COMPUTED now:
- **`tools/judge.py`** — the 5-lock foolproof judge protocol. Stats (Wilson interval, sign-test, Cohen's κ,
  position-swap, panel-majority, cross-family lock) tested cold. Run on goal-lock's own 8W/0T/4L → Wilson
  **[0.391, 0.862] straddles 0.5 → DIRECTIONAL, not a WIN.** The gate demotes the favorite — the un-gameable property.
- **`tools/route_truth.py` + `route_corpus.jsonl`** (36 outcome-pinned items, 12 adversarial both directions,
  content-hash 7a34cc3e) — the classifyTask misroute-cost harness, **COMPUTED, zero API. Real result:**
  | router | over-spend% | under-verify% | irrev-floor | cost |
  |---|---|---|---|---|
  | ordo_rule (gold signals) | 0% | 0% | 0 | 0 |
  | keyword_router (no-model) | 6% | 16% | 2 | 31 |
  | length_router (strawman) | 6% | 79% | 10 | 151 |
  | always_strict | 100% | 0% | 0 | 17 |
  Findings: the **5-trigger taxonomy is complete** (0 misroute given correct signals); the HARD part is extraction
  — a naive keyword extractor (cost 31) is **worse than always-strict (cost 17)** because under-verify is 10× costlier,
  so the real classifyTask must drive under-verify near 0 to justify itself. The model-extraction number is PENDING;
  the "100% consistency" headline is withdrawn (BUILD-LOG open item #3 closed).
- **`tools/trap_corpus.py`** (8 planted-misleader items, 4 zones) — the verify-assert harness with deterministic
  oracles + the **baseline-fails-first entry gate** (admits only items the baseline fails ≥2/3, killing the 8-tie
  wash by construction) + McNemar. Tested cold; the A/B (arm-A vs arm-B completions) is PENDING model calls → COMPUTED.
- **`tools/goal_lock_bench.py`** (5 construction-validated divergence items) — A=follow-plan vs B=re-derive,
  tier-one exact-match COMPUTED + tier-two cross-family judge. Its construction-validator **caught a real bug in my
  own corpus** (a ground-truth that echoed the stale-plan noun) before it could ship — the kill-clause working on itself.
The subtraction held: divergence's generative half deleted (§8 → escalation flag), 3 instincts kept as honest
process with no claim, goal-lock de-headlined to directional until the cross-family rerun. Every number prints at
its true tier or stays PENDING. 24/24 node + 5 Python self-checks green.

## Single-pass thinking protocol + the masterclass measurement (2026-06-25)
After the GTM red-team (4/10 literal thesis), built `spec/thinking.md` — a complexity-adaptive SINGLE-PASS
protocol (classifyTask LIGHT/STRICT dispatcher + 7 grounded 1× instincts: diction, verify-assert, goal-lock,
reuse-replan, divergence-width, self-heal). Then **measured the instincts honestly** with blind A/Bs (separate
arm-producers, separate blind judges, position decorrelated by item parity). The results are mixed, recorded in
full — including the null and the negative:

| instinct | blind A/B (6 items × 2 judges = 12 judgments) | net | tier | read |
|---|---|---|---|---|
| **goal-lock** | 8 win / 0 tie / 4 loss | **+4** | AGENT-JUDGED | directional WIN — re-derive-from-{goal+actual} beat blind plan-following. The one instinct with lift. |
| **verify-assert** | 2 win / 8 tie / 2 loss | **0** | AGENT-JUDGED | WASH — mostly ties; the check rarely changed the answer on this set. No lift claim. |
| **divergence** | 4 win / 1 tie / 7 loss | **−3** | AGENT-JUDGED | **NET NEGATIVE** — overturns the earlier n=4 "3/4" signal. A regression flag: width adds noise where the fork wasn't genuinely wide. **Claim withdrawn.** |
| **classifyTask** | 36/36 inter-classifier agreement (12 items × 3) | 100% | AGENT-JUDGED | CONSISTENCY (rule-application reliability), NOT accuracy/misroute rate — no ground-truth labels. |

**Honest caveats (none hidden):** same-model-family judging (self-preference risk), small-N (effective N ≈ the
6/12 item count, no CI/p-value), constructed corpora (classifyTask's 100% may mean the items were unambiguous,
not that routing is correct). **Nothing here is COMPUTED or proof.** The actionable finding is the divergence
net-negative → the claim is withdrawn and the §8 move scope-narrowed; goal-lock banks a directional agent-judged
win; verify-assert and diction stay (lossless + 1×) but claim no lift. P10 rot-retention harness built
(`tools/rot_bench.py`, NoLiMa-style needle@lost-middle vs head-ledger), construction validated; P10 stays
GROUNDED until a long-context run records `tools/rot-ab.json`. **The measurement that contradicted a prior
claim is the system working as designed.**
