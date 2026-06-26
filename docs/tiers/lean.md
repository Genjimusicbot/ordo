# ⚫ ORDO Lean — token saving only

The smallest thing that pays for itself: *just* the compacting + verbosity. No gates, no tools, no quality claims.
As neat and light as caveman.

## Install
```bash
npx ordo init --lean
```
Drops a single stateless skill at `.claude/skills/ordo-lean/SKILL.md`. Auto-fires on tasks that produce or read
structured data, JSON, logs, tables, or long output.

## What you get
- **Output:** tabular → TSV, nested → minified JSON (never pretty-print), prose → ponytail (cut preamble / restate
  / closer). Diction (cheapest-faithful word form).
- **Inbound:** compact what the model reads, lossless-first, with the **measured-revert gate** (never inflate) +
  a coverage check for any lossy cut.

## What you DON'T get
- No classify→route dispatcher, no gates (REFEED/etc.), no bundled MCP tools, no `.ordo/` persistence. **Stateless.**
  Want those? → [ORDO Full](full.md).

## Proven
- **−47–68%** end-to-end on a structured turn; **−24%** lossless floor on prose-heavy turns (measured, GPT-proxy).
  That is the entire claim — no quality, speed, or magic. `python tools/ab_smoke.py` reproduces it.

## For
"I just want lower bills / fewer tokens, nothing else."
