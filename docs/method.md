# ORDO method: lineage, design laws, and build phases

How ORDO is built, what it borrows, and how each piece is checked. The companion research base is the
`xenolinguistics/` folder of the llm-omni-wiki repo (the full Lojban grammar, the GLOSSOPETRAE paper,
the five-source sweep, and the two language blueprints). This file is the working method.

## Lineage (what we borrow, and what we reject)
- **Lojban (CLL grammar)** -> the GRAMMAR SHAPE. A `bridi` is a predicate with numbered typed slots,
  structurally a typed function call, and the grammar is mechanically unambiguous (one parse per
  utterance), so surface form IS the logical form. ORDO's directive+slots structure is this, minus
  the human phonology. *Reject:* speakability, ~1300 memorizable roots.
- **GLOSSOPETRAE (Pliny)** -> the DELIVERY + the evidence. Frontier models acquire a generative
  grammar zero-shot from a spec; ship ORDO as a spec/"skillstone". *Reject:* its stego/covert-channel
  mechanisms (safety; see DISCLAIMERS).
- **LLMLingua (Microsoft)** -> the PROOF the redundancy exists (~80-95% of prose is recoverable) and
  a ready-made evaluator (its self-information metric finds low-information spans). *Reject:* its lossy
  one-way deletion; ORDO must round-trip.
- **VOKU** -> mandatory EPISTEMIC marking (certainty + evidence-source as a required slot). Kills
  confident hallucination structurally.
- **Logographic determinatives** (Egyptian/Chinese radicals) -> a silent TYPE tag on operands, so the
  parser gets the category for free and the grammar constrains what may follow.
- **Runes / bind-runes / Blissymbolics** -> the WRITING-SYSTEM intuition (meaning-bearing glyphs,
  composition). *Reject:* the occult layer, and any glyph that fails the token-cost test.
- **Caveman + ponytail (house skills)** -> terseness (register) + do-less (amount), folded into the
  brevity slot and the design.
- **Huffman-the-intent-space** -> assign the shortest symbols to the highest-frequency directives.

## The four design laws (enforced, not aspirational)
1. **Tokenizer-validate every symbol.** A symbol is admitted only if its measured token cost (on
   `cl100k_base` + `o200k_base`, with the Claude-proprietary caveat) is <= the phrase it replaces, net
   of the grammar. Tool: `tools/tokcost.py`. Costs recorded per symbol in `spec/lexicon.md`.
2. **The grammar is the compression.** ORDO's savings come from collapsing a verbose request into
   `directive + typed-slots`, not from the glyph's appearance. The glyph is the writing system.
3. **Lossless-to-intent.** Every symbol has a precise meaning + an English expansion; a round-trip gate
   (`tools/`) checks that a model with the spec reconstructs the original intent. Meaning never
   silently drops.
4. **Epistemic + brevity are native grammar.** A required certainty/evidence slot and a brevity/format
   slot make "solid, terse outputs" structural, not a per-call plea.

## The grammar shape (preview; full spec in spec/grammar.md)
An ORDO directive is an ordered, typed frame:

    [DIRECTIVE] [OPERAND:type] [MODIFIERS] [EPISTEMIC]

- **DIRECTIVE** = the mandate task (summarize, explain, refactor...), one glyph. The verb.
- **OPERAND** = the subject/target, optionally with a determinative type tag (text, file, code, list).
- **MODIFIERS** = brevity/length/format/tone (e.g. "3 bullets", "as table", "terse").
- **EPISTEMIC** = certainty + source demand (e.g. "cite", "verify-first", "mark-confidence").

Directives chain with a pipe connector (do A then B). The grammar is unambiguous: each slot is marked,
so order can be relaxed and the parse stays deterministic. Surface = intent.

## Build phases (language first; harness later)
- **P0 — genesis** (this commit): repo, README, DISCLAIMERS, this method, the measurement tool.
- **P1 — the alphabet.** The core directive lexicon: the highest-frequency LLM command tasks, each a
  tokenizer-validated glyph with a precise meaning + English expansion + measured token cost.
- **P2 — the grammar.** Operand type tags, modifier set, epistemic set, chaining, the parse rules.
- **P3 — the writing system + skillstone.** The compact spec a model loads to read/write ORDO; the
  plug-into-any-LLM instructions; worked examples.
- **P4 — validation.** The round-trip gate over a task set; measured net token savings vs English;
  honest report (incl. the Claude-tokenizer caveat and the per-token-compute unknown).
- **Later — the harness** (separate concept): orchestration, auto-commanding, verbosity control, the
  self-learning lessons loop. It USES ORDO; it is not part of this language repo.

## What gets checked at each step (the record)
Every phase logs, in `docs/BUILD-LOG.md`: what was built, how, what was measured/verified, and what is
still open. No step claims a saving without a `tokcost.py` number behind it; no symbol ships without a
round-trip meaning. Honesty over hype is the whole point of doing this rigorously.
