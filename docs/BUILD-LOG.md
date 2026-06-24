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

## Next: P2 — the grammar
Operand type-tags (text/file/code/list determinatives), the modifier set (brevity/length/format/
tone), the mandatory epistemic slot (certainty + source), directive chaining (pipe), and the
deterministic parse rules. Then P3 (writing system + skillstone) and P4 (round-trip + measured
sentence-level savings).
