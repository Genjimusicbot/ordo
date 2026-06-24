# ORDO macros — intent-as-symbol (C7)

The user's reframe, where the vocabulary lever actually lives: not single words (dead, ~1%) but whole
recurring **intents**. A prompt people retype constantly ("think step by step and show your reasoning",
"review it like a senior engineer would") is 8-16 tokens; a short **readable** code collapses it to
1-2. Per the deanchor verdict, these are mnemonic codes (not exotic glyphs) so they decode reliably.

Measured (`o200k`): 16 macros, avg span **8.2 tokens → 1.4-token code, avg 6.8 saved per use**, every
code ≤2 tokens.

| code | expands to | saved (o200k) |
|---|---|---|
| `srev` | review it like a senior engineer in code review: what would you reject and why | 14 |
| `eli5` | explain in the simplest possible terms, as if to a beginner | 10 |
| `steel` | steelman the strongest opposing view, then critique it | 9 |
| `gap` | what important question am I not asking that I should | 9 |
| `hon` | be brutally honest, no hedging or flattery | 9 |
| `risk` | what could go wrong — list the failure modes | 8 |
| `cot` | think step by step and show your reasoning | 7 |
| `5why` | do a five-whys root-cause analysis | 7 |
| `elip` | explain for an expert peer, assume domain knowledge | 7 |
| `asm` | list the assumptions you are making | 5 |
| `dev` | play devil's advocate against this | 5 |
| `trd` | lay out the key trade-offs | 4 |
| `one` | answer in a single sentence | 4 |
| `eg` | give a concrete worked example | 4 |
| `next` | give the concrete next steps | 4 |
| `pnc` | give the pros and cons | 3 |

## Use
Macros stack onto a command as extra tokens: `anlz this risk cot` = "analyze this; what could go wrong
(failure modes); think step by step and show your reasoning." They are the cheapest place the model's
own best behaviors (chain-of-thought, devil's advocate, senior-review) get triggered, so the macro
layer is also a **quality** lever, not only a token lever — a 1-token code that reliably invokes a
strong reasoning mode.

## Honesty
Codes are readable English abbreviations (some are established: eli5, cot) so decode is reliable;
exotic single-glyph versions were rejected (deanchor: they cost reliability for ~0 extra tokens). The
macro list is extensible; each new macro must be tokenizer-cheap (≤2 tokens) and pass the decode test.
