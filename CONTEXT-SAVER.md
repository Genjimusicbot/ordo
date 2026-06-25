# ORDO Context Saver (Lane 1 — the lite mode)

Load this alone if all you want is **less token waste and no context rot** — no ORDO language, no
quality gates. It's the part that makes your LLM *smarter by keeping its context clean*: degraded
context measurably lowers accuracy (a 200K model rots at ~50K; middle context can score *below*
no-context), so fighting rot is a quality lever, not just a cost one. ~1k tokens; paste it into your
system prompt / CLAUDE.md / project rules. (Want the whole framework? Load `OPERATING-PROFILE.md` instead.)

## The rules (follow these every turn)
**1. Output in the cheapest faithful form.**
- Tabular / rows of the same shape → **TSV** (≈55% fewer tokens than JSON).
- Nested / mixed → **minified JSON**. **Never pretty-print.** Avoid YAML for machine output (it's a trap).
- Prose → **ponytail:** no preamble ("Sure!", "Great question!"), no restating the task, no closer
  ("Hope this helps"), no narrating what you're about to do. Answer first, fewest words, stop when done.
  This is lossless — cut the filler, keep the substance. Caveman-terse register on *operational* notes
  only (plans, status), never on explanations a human reads to learn.

**2. Don't inline what you can summarize or retrieve.**
- Redundant tool output / logs: keep a representative sample + the count, not all of it.
- Big docs: keep the load-bearing facts; reference the rest by pointer and fetch on demand.
- Across turns: send the *delta* (what changed), not the whole restated file.

**3. Beat context rot with a ledger + compaction (complex work only).**
Route to this track when the work is long (>~15 tool calls), broad (>5 files), has load-bearing facts
that must survive (IDs, decisions, contracts), or is irreversible. Simple Q&A / single edits stay
standard — no overhead.
- **Externalize state to a short ledger** (the goal, the acceptance criteria, key decisions, files
  touched, open blockers). The ledger is the durable record; the context window is scratch.
- **Compact before you're starved:** warn at ~70% of the window, hard-compact by ~90% (95% is too late
  to even summarize). On compaction: drop tool-output first (it's 70-80% of the budget and is on disk),
  collapse resolved subtasks to a one-line outcome, summarize old turns into the ledger.
- **Keep the load-bearing context at the HIGH-ATTENTION EDGES** (start and end), never the middle — the
  middle is where models read worst.
- **Rehydrate after compacting:** re-read the ledger + the few live files + run the tests. The test is
  the non-lossy backstop that lets you compact aggressively.

## Honest limits
Token cuts are GPT-tokenizer-measured proxies; re-validate on your model. Compaction is lossy — it can't
recover a fact you never wrote to the ledger before dropping it; the rehydrate/test step is the
safety net. Grounded in Chroma *Context Rot* (2025), *Lost in the Middle* (2023), RULER (2024), NoLiMa
(2025). See `spec/context-rot.md` and `spec/output.md` for the full versions.
