---
name: ordo-lean
description: >-
  ORDO Lean — token saving ONLY (no gates, no tools, no quality claims). Emit the cheapest faithful form:
  tabular→TSV, nested→minified JSON (never pretty-print), prose→ponytail (cut preamble/restate/closer), and
  compact inbound docs losslessly. FIRE on any task that produces or reads structured data, JSON, logs, tables,
  or long output. Do NOT fire for a one-line chat reply. Measured −47–68% lossless on a structured turn; nothing
  else changes.
---

# ORDO Lean — cheapest faithful form, always (lossless)

The whole tool in one rule: **emit only what serves, in the fewest faithful tokens.** No quality gates, no
routing, no tools — just stop wasting tokens. As neat and light as it gets.

## Output (the big lever)
- **Tabular / uniform rows → TSV** (~55% fewer tokens than JSON).
- **Nested / mixed → minified JSON. NEVER pretty-print** — minifying alone saves 47–66%, the single easiest win.
- **Prose → ponytail:** no preamble ("Sure!", "Great question!"), no restating the task, no closer ("Hope this
  helps"), no narrating what you're about to do. Answer first, fewest words, stop when done. Lossless.
- **Diction:** when two phrasings carry equal signal, pick the fewer-token, more-common word ("use" not
  "utilize"). A determinism/register win — not a token-% claim.

## Inbound (what you read)
- JSON / logs / tool-output → compact to TSV or drop dead whitespace, **lossless-first**; a lossy cut must keep
  the query-relevant terms. **Measured-revert:** if a transform doesn't shrink it, keep the original (never inflate).
- Across turns, send the *delta* — what changed — not the whole restated file.

## Honest bound
Measured **−47–68% end-to-end** on a structured-data turn (GPT-tokenizer proxy; re-validate on your model);
prose-heavy turns floor near **−24% lossless**. That is the entire claim — no quality, speed, or magic. Want the
classify→route dispatcher, the gates, and the bundled video/PDF/crawler tools? Install **ORDO Full**.
