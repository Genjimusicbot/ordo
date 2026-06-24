# ORDO lexicon — the directive alphabet (Phase 1)

The core verbs of ORDO: the highest-frequency LLM command tasks, each a **tokenizer-validated**
single glyph. A directive is the predicate of an ORDO sentence (`[DIRECTIVE] [OPERAND] [MODIFIERS]
[EPISTEMIC]`, see `grammar.md`). One glyph replaces a whole verbose request phrase.

## Measured basis (Design Law 1)
Every glyph below is **1 token in both** `cl100k_base` (GPT-3.5/4) and `o200k_base` (GPT-4o/o1),
measured with `tools/tokcost.py`. The empirical findings that picked this set:
- **Runes are the worst choice: 3 tokens each** (ᚠ ᚢ ᚦ ... = 3/3). Beautiful, expensive. They are
  therefore NOT used on the wire; they may serve as an optional display/tier skin only.
- **Lowercase Greek = 1 token** (α β γ δ ε λ μ ν π ρ σ τ φ χ ω). The efficient, distinct, mnemonic core.
- **Uppercase Greek = 2 tokens in cl100k** (Σ Δ Π = 2/1), so we use lowercase even where uppercase is
  more mnemonic.
- **Select symbols = 1 token** (→ ← ↑ ↓ × ¬ ★ ☆ ● ■ ※ § ¶ †).
A directive earns its place because the English it replaces is 3-9 tokens (e.g. "rate the following
from 1 to 10" = 9 tokens), so a 1-token glyph nets a real saving. Caveat: costs are GPT-tokenizer
proxies; Claude's is proprietary (see `DISCLAIMERS.md`). Adjacency in full sentences is re-validated
in Phase 4.

## The 28 core directives

| glyph | tok (cl/o) | directive | expands to (English) | mnemonic |
|---|---|---|---|---|
| σ | 1/1 | **summarize** | "summarize the following" | sigma = sum |
| ε | 1/1 | **explain** | "explain the following" | epsilon ~ explain |
| δ | 1/1 | **define / describe** | "define / describe" | delta ~ definition |
| α | 1/1 | **analyze** | "analyze the following" | alpha ~ analyze |
| χ | 1/1 | **critique / review** | "critique the following" | chi ~ check |
| ρ | 1/1 | **rewrite / rephrase** | "rewrite the following" | rho ~ rewrite |
| τ | 1/1 | **translate** | "translate the following" | tau ~ translate |
| π | 1/1 | **plan (step-by-step)** | "make a step-by-step plan for" | pi ~ plan |
| λ | 1/1 | **code / implement** | "write code that" | lambda = function |
| γ | 1/1 | **generate / write / create** | "generate / write" | gamma ~ generate |
| β | 1/1 | **brainstorm / ideate** | "brainstorm ideas for" | beta ~ brainstorm |
| μ | 1/1 | **compare / contrast** | "compare the following" | mu ~ match |
| φ | 1/1 | **fix / debug** | "find and fix the bug in" | phi ~ fix |
| ν | 1/1 | **refactor** | "refactor the following code" | nu ~ renew |
| ω | 1/1 | **conclude / final answer** | "give the final answer / conclusion" | omega = the end |
| → | 1/1 | **continue / proceed** | "continue" | arrow forward |
| ↑ | 1/1 | **expand / elaborate** | "expand on / elaborate" | up = more |
| ↓ | 1/1 | **shorten / compress / tldr** | "make this shorter / tl;dr" | down = less |
| ★ | 1/1 | **rate / score** | "rate from 1 to 10" | star = rating |
| ☆ | 1/1 | **example / demo** | "give a worked example of" | hollow star = illustrate |
| ※ | 1/1 | **extract** | "extract the key points from" | reference mark |
| § | 1/1 | **outline / structure** | "outline / give the structure of" | section sign |
| ● | 1/1 | **list / enumerate** | "list the" | bullet |
| ■ | 1/1 | **classify / categorize** | "classify / categorize" | box = bin |
| × | 1/1 | **remove / strip / delete** | "remove / delete" | x = delete |
| ¬ | 1/1 | **exclude / do-not (constraint)** | "do NOT / exclude" | logical not |
| ± | 1/1 | **vary / give alternatives** | "give alternatives / variations of" | plus-minus |
| † | 1/1 | **verify / fact-check** | "verify the following is correct" | dagger = mark |

## Notes
- **Default directive = answer.** A bare operand with no directive means "answer / respond to this".
  No glyph spent on the most common act.
- **Composition over minting.** Tasks not in the core (simplify, proofread, optimize) are *composed*,
  not given a new glyph: simplify = `ε` + brevity-simple modifier; proofread = `χ` + format; optimize
  = `ρ` + "better" modifier. New glyphs are minted only for genuinely high-frequency, non-composable
  directives (Design Law 2: the grammar carries the load).
- **Chaining.** Directives chain with a pipe (`grammar.md`): `σ ↓` = "summarize, then make it terse".
- **Extensible.** This is the Phase-1 core (28). The pool of measured 1-token glyphs supports more;
  later phases add directives only against measured frequency, never for completeness's sake.

Machine-readable companion: `lexicon.tsv` (glyph, directive, cl100k, o200k, expansion).
