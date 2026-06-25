# ORDO — self-evaluation (ORDO graded by its own evaluation gate)

We ran ORDO's own evaluation gate (`spec/evaluation-gate.md`) on ORDO-as-a-product, judged by an
independent agent against the real goal ("an importable framework that measurably improves how people
build with LLMs, honestly"), instructed to be brutal, not kind. Publishing the verdict unedited is the
point: the gate is only worth anything if we apply it to ourselves.

## Verdict: 6.5 / 10 (upper "fair"), reproducible spread 6-7
Not the ~9 an over-eager reading of the operating profile would imply. The gap between what ORDO
*measures* and what it *markets as a framework* is the cap.

## Honest pros (verified cold)
- **The measurement spine reproduces.** Run the tools cold: grammar reproduces exactly (437→285 =
  34.8%), `formatbench` confirms TSV −59% on uniform arrays, `tokcost` confirms runes = 3 tokens. The
  numbers are not fabricated.
- **The runtime is real and tested.** The decoder + output contract are deterministic; `npm test` and
  `pytest harness/` are green.
- **Unusually honest disclaimers + a real cut list** that self-refute the original thesis.

## The structural holes it found (and their status)
1. **Not installable as a "framework" — a spec repo + scripts.** → **FIXED:** shipped as an npm package
   (`npm install ordo-llm`) with a runtime + CLI + 11 tests; `examples/` populated.
2. **~1 part runnable, ~4 parts markdown SOPs, marketed as one engine.** → **FIXED (by honesty):** the
   README + operating profile now state plainly that the gates are prompt SOPs (methodology), not code;
   `getSpec()` loads them as text. We stopped implying they execute.
3. **The scoreboard overclaimed and contradicted itself** ("8/10 MEASURED" vs docs' "7/8"; agent-judged
   pillars stamped MEASURED; P2 printed 77% but computed 67%). → **FIXED:** `pillars.py` now tags every
   pillar by evidence tier (COMPUTED / AGENT-JUDGED / GROUNDED / PROXY-ONLY); P2 prints its computed
   number; the tally is internally consistent.
4. **The flagship decode/quality scores are GPT-proxy, one-model, agent-judged with no committed
   transcript.** → **PARTIALLY ADDRESSED:** the README + scorecard now label these AGENT-JUDGED with the
   GPT-proxy caveat front and center. **Still open:** committing the eval harness + transcripts so
   `pytest` re-derives the fidelity scores, and a real measurement on a non-GPT (Anthropic) tokenizer.
5. **The scripts crashed on a default Windows console (UnicodeEncodeError).** → **FIXED:** the
   glyph-printing scripts force UTF-8 stdout.

## Still open (the honest roadmap)
- Commit the decode/quality eval harness + transcripts (reproducible, not just logged).
- Measure the 20-prompt benchmark on a real Claude/Gemini tokenizer, not only `tiktoken`.
- A long-context harness to move P10 (context-integrity) from GROUNDED to measured.
- A real wall-clock timing harness to move P3 (speed) off proxy.
- Make REFEED / evaluation callable as code (not only SOPs), or keep them honestly labeled as SOPs.

The single most important thing the evaluator named — *close the honesty gap between "framework" and
what executes* — is what this release does. ORDO is an honest research artifact with a small trustworthy
runtime and one excellent finding (the compression is the grammar + output contract, not the glyphs); it
is now packaged and labeled as exactly that, no more.
