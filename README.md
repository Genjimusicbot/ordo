# ORDO

**An experimental, LLM-native command language.** ORDO collapses the verbose prompts people type
every day ("summarize the following in three bullet points", "refactor this and explain why") into
terse symbolic directives a frontier model reads zero-shot from a spec. One directive-glyph plus a
few typed slots replaces a sentence. It is built *for* a transformer, not retrofitted from human
speech.

Latin *ordo*: order, rank, arrangement. A language that puts intent in order.

> **Two standalone, complementary concepts.** ORDO (this repo) is the *language*. The *harness*
> (orchestration, auto-commanding, verbosity control, self-learning) is a separate piece that will
> *use* ORDO. This repo builds the language first; the harness comes after. They are designed to
> compose, but each stands alone.

## Why this can work (the entrypoint)
The premise is no longer speculative. Two independent results ground it:
- **Zero-shot acquisition** (elder_plinius, GLOSSOPETRAE, June 2026): given only a grammar *spec*,
  frontier models read, write, and translate a never-before-seen constructed language with no
  fine-tuning, and at full glyph-swap they execute alien code *better* than the English version
  (Opus +36pp zero-shot on hard programs) while human legibility drops to ~15%.
- **The redundancy is measured** (Microsoft LLMLingua, peer-reviewed): ~80-95% of natural-language
  tokens are recoverable redundancy to a model; compressing prompts 4x can *raise* accuracy.

ORDO turns those findings into a *usable, lossless* notation. See `docs/method.md` for the full
lineage (Lojban's unambiguous grammar, logographic determinatives, VOKU's epistemic marking, runes,
and the honest corrections).

## The four design laws (the anti-shortcut discipline)
1. **Every symbol is tokenizer-validated.** "One glyph = one token" is false for exotic glyphs (BPE
   shatters them). A symbol earns its place only by *measured* token cost vs the phrase it replaces.
   See `tools/tokcost.py` and the measured costs in `spec/lexicon.md`.
2. **The compression is the grammar, not the glyph.** One directive + terse typed slots collapses a
   whole request; the glyph is the writing system, the slot-grammar is the engine.
3. **Lossless-to-intent, always.** Every symbol has a precise meaning and an English expansion; a
   model loading the ORDO spec must reconstruct the original intent (round-trip gate). Unlike lossy
   prompt-compression, ORDO round-trips.
4. **Epistemic + brevity are native grammar.** A mandatory certainty/evidence slot (kills confident
   hallucination) and a brevity/format slot (terseness is structural, not a request).

## Status
Experimental research. Building phase by phase: the alphabet (directive glyphs) -> the grammar ->
the writing system + skillstone -> validation. Read `docs/method.md` and `DISCLAIMERS.md` first.
Nothing here claims a magic compression multiplier; it claims a measured, lossless, grammar-driven
reduction on the operational/command layer. The numbers will be measured, not promised.

## Layout
- `DISCLAIMERS.md` — what ORDO is and is not; the honest caveats.
- `docs/method.md` — research lineage, design method, build phases, the corrections.
- `spec/` — the language: the alphabet (`lexicon.md`), the grammar, the writing system, the skillstone.
- `examples/` — worked English <-> ORDO translations.
- `tools/` — the measurement + round-trip tooling that keeps the language honest.

## Use (once the spec lands)
Load the ORDO skillstone (a compact system-prompt spec) into any frontier LLM; it then reads and
writes ORDO. Plug-in instructions: `spec/skillstone.md` (coming in a later phase).
