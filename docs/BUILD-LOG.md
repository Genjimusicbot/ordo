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
  strong reasoning mode). Decode test running.

## The language is done (P0-P4). Next: the harness (separate concept)
P0 alphabet → P1.x pool/matrix/allocation → P2 grammar (ORDO-G, ~35%, decode 1.70) → P3 output
framework (format-by-shape + ponytail 77% + caveman) → P4 skillstone (`ORDO.md`, 1.75/2). The LANGUAGE
is built and measured end-to-end. The remaining piece is the **harness**: a runtime that auto-encodes
requests / auto-decodes ORDO / enforces the output contract, instead of relying on the model following
`ORDO.md` by hand. That is the separate second concept the project was always two-of.
P3 = the skillstone (a single self-contained `ORDO.md` a user pastes into any LLM to teach it ORDO in
one shot) + writing-system polish. Then the separate **harness** concept (the runtime that
auto-encodes/decodes + the verbosity layer). The language itself (P0-P2) is now real and measured.
