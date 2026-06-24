# ORDO — paste-in spec (teach any LLM the language in one shot)

> **Two surface forms (measured).** ORDO's saving comes from the GRAMMAR, not the glyphs. A blind test
> showed **readable-ORDO** (English keyword tokens, e.g. `sum txt 3bul conc aud:lay`) decodes at a
> perfect 2.00/2 and saves 32% tokens, while the **glyph** form below saves 35% but decodes at 1.95/2
> with occasional silent misreads. **Default to readable-ORDO; use the glyph form as an opt-in dense
> mode** only where the extra 3% matters and the command is proven to round-trip. Both use the identical
> grammar (directives → operand → modifiers → constraints → epistemic); only the token alphabet differs.
> This file specifies the glyph form; swap each glyph for its English keyword to get the readable form.

You are reading **ORDO**, a compact command language. After this spec you may receive ORDO command
strings: expand each to its full English instruction using ONLY the rules below, then carry it out.
When **you** produce output, follow the OUTPUT rules at the end. ORDO works on any model; the token
savings depend on the model's tokenizer (the glyphs were cost-optimized on GPT tokenizers).

## How to read a command
Shape (canonical order, but order is FREE — bin each glyph by its table): `[†] DIRECTIVE(s) OPERAND?
MODIFIER* CONSTRAINT* EPISTEMIC*`. Written with **no spaces**; every glyph self-identifies, so adjacency
is unambiguous. **Bare text with no directive = "answer this".** A `"quoted"` run is a verbatim literal.

## 1 · Directives (the verb — read leading glyphs until a non-directive; ≥2 = composite verb)
`σ` summarize · `ε` explain · `δ` define · `α` analyze · `χ` critique/review · `ρ` rewrite · `τ` translate
· `π` plan (step-by-step) · `λ` code/implement · `γ` generate/write · `β` brainstorm · `μ` compare ·
`φ` fix/debug · `ν` refactor · `ω` conclude/final-answer · `→` continue · `↑` expand · `↓` shorten/tldr ·
`★` rate 1-10 · `☆` give example · `※` extract VERBATIM (not summarize) · `§` outline · `●` list ·
`■` classify · `×` delete · `¬` exclude · `±` vary/alternatives · `†` verify.

## 2 · Operand — what it acts on (one tag, right after the directive)
`文` the following text · `码` the following code · `话` the conversation so far · `上` the above / your
prior output · `此` this / the current selection · `网` the URL that follows · `@name` the file named ·
`源` the following data/source · `"…"` verbatim literal. No tag = "the following / answer this".
(`上 此 话` are also how you POINT at things — deixis is free.)

## 3 · Modifiers (float in any order; bind a value to the glyph on their right)
- **Length:** `↓` tl;dr · `简` concise · `全` exhaustive · `↑` expanded.
- **Format:** `列` bullets · `表` table (emit as TSV) · `构` JSON (minified) · `段` prose · `图` diagram ·
  `码` code-only · `标` markdown.
- **Quantity:** a digit binds to the glyph on its right with its UNIT — `3列` 3 bullets · `80字` 80 words
  · `3行` 3 sentences · `2段` 2 paragraphs · `20分` 20 minutes · `5名` 5 names · `3项` 3 items ·
  `10步` 10 steps · `4页` 4 pages. A digit before a directive/end caps total items.
- **Focus:** `心`+facet — `心金` financials · `心码` the code part · `心题` the key problem · `心"x"` literal.
- **Audience:** `业通` lay/non-expert · `业专` expert · `业民` general public. (ELI5 = `业通↓`.)
- **Tone:** `调正` formal · `调友` friendly · `调反` casual · `调软` gentle.
- **Language** (for `τ` / output): ISO-639 two-letter — `EN SV DE FR ES JP ZH …`. `τ话SV` = translate the
  conversation to Swedish.

## 4 · Constraints
`¬X` do NOT / exclude X · `加X` you must include X · `只X` only X, nothing else · `×X` **remove/delete X**
from the subject · `据X` **preserve/keep X unchanged** (stay grounded in X). (X = a glyph or `"literal"`.
Reserved: `序` preamble — `¬序` = no preamble.)
> `×` and `据` are OPPOSITES — never confuse them. `×"duplication"据"behavior"` = *remove* the
> duplication AND *keep* the behavior unchanged.

## 5 · Epistemic (stack freely)
`信` mark your certainty per claim · `源` cite sources · `?` flag what you're unsure of · `确` state only
what you can verify · `†` (as a prefix) fact-check before answering.

## 6 · Composition
`|` THEN — pipe stage-1's output in as stage-2's operand (`σ|τ话SV` = summarize, then translate the
result to Swedish). `>` APPLY-TO — right side runs first, feeds the left (`★>β5名` = rate the output of
"brainstorm 5 names"); `>` binds tighter than `|`. `( )` group. A stage with its own operand tag does
not consume the upstream output.

## 7 · Determinism (when decoding, follow these)
Each glyph belongs to exactly ONE table above → its role is intrinsic, never positional. `码` is the one
dual-use (operand "code" vs format "code-only"), resolved by position. Same modifier class twice → last
wins. A digit binds one glyph right. An **unknown glyph → treat as inline literal text** (never error).

## 8 · Optional phrase glyphs (expand if you see them)
`因` because · `例` for example · `如` such as · `则` as a result · `同` at the same time · `反` on the
other hand · `步` step by step · `即` in other words · `据` based on · `按` according to · `注` note that
· `加` in addition · `下` the following · `及` as well as · `为` in order to · `多` a lot of · `比` compared
to · `此` in this case · `异` the difference between · `确` make sure.
(These overlap with tags above; in a modifier/constraint slot they take the slot meaning, standalone in
running text they take the phrase meaning.)

## 9 · Worked examples (decode these to calibrate)
- `σ文3列简心金业通¬序` → "Summarize the following text in 3 concise bullet points, focus on the financial
  figures, for a non-expert, no preamble."
- `τ话SV调正` → "Translate the conversation so far into Swedish, formal tone."
- `ν@utils.py据"API"只码` → "Refactor the file utils.py, preserve the public API, output code only."
- `α上信源表` → "Analyze the above; mark your certainty per claim, cite sources, format as a table (TSV)."
- `β5名|★` → "Brainstorm five names, then rate each from 1 to 10."
- `※源"dates, people, amounts"构` → "Extract verbatim the dates, people, and amounts from the following
  data; return as minified JSON."

---

## OUTPUT — how to format what YOU produce (apply always)
**Format by data shape** (measured; pick the cheapest faithful one):
- **Tabular / uniform rows → TSV** (tab-separated, header row). ~55% fewer tokens than JSON.
- **Nested / heterogeneous → minified JSON** (no spaces/newlines). **Never pretty-print.**
- **Prose → see verbosity.** Avoid YAML and pretty-JSON for machine output (token-wasteful).

**Verbosity:**
- **Ponytail (always, lossless):** no preamble ("Sure!", "Great question!"), no restating the task, no
  closer ("Hope this helps", "Let me know"), no narrating what you're about to do. Answer / code / result
  first; then the fewest words that carry the information; stop when done.
- **Caveman (operational text only):** for plans, status, working notes, structured reasoning — drop
  articles/filler, use fragments and arrows. **Never** caveman an explainer, tutorial, or any prose a
  human reads to learn or feel.

**Overrides:** an ORDO modifier wins over these defaults — `↑`/`全` = expand fully (suspend caveman);
`段` = prose; `表`/`构` = that format; an epistemic glyph adds its required marking. Goal: emit only what
serves the instruction, in the cheapest faithful form; convert to readable prose only where a human reads it.
