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

## Next: P2 — the grammar
Operand type-tags (text/file/code/list determinatives), the modifier set (brevity/length/format/
tone), the mandatory epistemic slot (certainty + source), directive chaining (pipe), and the
deterministic parse rules. Then P3 (writing system + skillstone) and P4 (round-trip + measured
sentence-level savings).
