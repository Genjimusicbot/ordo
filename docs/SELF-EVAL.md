# ORDO — self-evaluation

Two evals on the record. The **current** score (7.6, below) re-graded the system after the V2 rebuild with five
blind raters on an anchored scale. The **historical** 6.5 graded an earlier artifact (a "spec repo + scripts")
and is kept for the audit trail, not as the live score — nearly every hole it named is now fixed.

## Current: 7.6 / 10 — five blind raters, anchored scale (2026-06-26)
Five independent raters (skeptical buyer · LLM-infra engineer · honesty auditor · competitor · daily user), each
grading the *current* files blind on an explicit anchor (5 = average tool in this space, 7 = solid/above-average,
8.5 = excellent with only minor gaps, 9.5 = best-in-class proven). Composites: **7.5 / 7.6 / 7.6 / 7.5 / 7.7** — a
tight band. Median **7.6**.

| dimension | median | the read |
|---|---|---|
| D1 core efficacy | 7.5 | lossless −47–68%, reproducible cold; capped by the GPT-proxy tokenizer |
| **D2 evidence & honesty** | **9** (unanimous) | every number tier-tagged, nulls named, self-grades shipped unedited |
| D3 ease of install / use | 7 | three real tiers + `/ordo`; auto-activation undemonstrated live |
| D4 breadth / completeness | 7 (unanimous) | four layers as one; the non-compression legs are grounded-not-measured |
| D5 differentiation | 7 | fewest-among-lossless *by stacking* — honest, narrow moat |
| **D6 honesty about its own gaps** | **9** (unanimous) | gaps named cleanly; an owed-measurements ledger is published |

**The one flaw all five named, independently:** every load-bearing token number is counted on GPT's tiktoken
(o200k) and **never validated on Claude's own tokenizer** — the model the product targets. The headline −68% is
also shape-dependent (the lossless prose floor is only −24%). That single cap is what holds D1, and the composite,
below 8.5. The honesty machinery (D2/D6) is already best-in-class; the proven core is narrower than the surface
ambition, and the ambitions (auto-activation live, the gates, rot-mitigation) are openly fenced as unproven.

### Partial close — tokenizer-robustness (`python tools/tokenizer_robustness.py`, 2026-06-26)
The exact Claude count needs the key-gated `count_tokens` API (owed). The next-best validation: re-count the same
A/B corpus across four BPE tokenizers spanning gpt2 (50k vocab) → o200k (200k). The **structural** wins transfer —
ponytail spread **1pp**, TSV **8pp**, readable-grammar **6pp**, end-to-end **11pp**, and the published −68% is the
*conservative* end (gpt2 gives −79%). The **glyph** row is vocab-dependent (**33pp**, −32% to −65%), exactly as
`DISCLAIMERS.md` flags — readable-ORDO is the safe default. So the lossless headline transfers across a
50k→200k-vocab range; what's still owed is the exact Claude tokenizer (all four here are GPT-lineage).

---

## Historical: 6.5 / 10 — pre-V2 artifact, superseded (2026-06-25)
ORDO's own evaluation gate (`spec/evaluation-gate.md`) run on ORDO-as-a-product, judged by an independent agent
against the real goal ("an importable framework that measurably improves how people build with LLMs, honestly"),
instructed to be brutal. The cap it named — the gap between what ORDO *measured* and what it *marketed as a
framework* — is exactly what the V2 rebuild closed (three tiers, `/ordo`, the evidence tiers, the honest reframe).
Kept unedited below for the record; what it graded no longer exists.

### Verdict (historical): 6.5 / 10 (upper "fair"), reproducible spread 6-7
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
- ~~A real wall-clock timing harness to move P3 (speed) off proxy.~~ → **BUILT:** `ordo measure` reads
  Anthropic's own billed `usage.*` + timestamps from Claude Code's JSONL (lossless). P3 auto-upgrades
  PROXY→COMPUTED once a paired ORDO-on/off A/B is recorded (`tools/measure-ab.json`). *Open:* run the A/B.
- Make REFEED / evaluation callable as code (not only SOPs), or keep them honestly labeled as SOPs.

## Post-eval additions (the competitive teardown, 2026-06-25)
A source-level teardown of 12 public repos ([`COMPETITIVE-TEARDOWN.md`](COMPETITIVE-TEARDOWN.md)) found 6
non-overlapping gap-fillers, now shipped (see [`ADD-PLAN.md`](ADD-PLAN.md)): the **real cost/token meter**
(above), **`/ordo` packaging** (installable skill + `.claude-plugin` manifest, closes the "paste a 1.4k file
by hand" adoption gap), the **measured-revert gate** (compression's lossless-first promise as a runtime
mechanism, not a slogan), the **code-context** contract (`spec/code-context.md`), the **decompose** contract
(`spec/decompose.md`), and **opt-in model routing** (`resolveModel`). The discipline held: no foreign runtime
vendored, 5 of 6 are spec/packaging/one script, nothing lossy ships as a default. The teardown *refused* 6
overlapping layers (rtk/llmtrim/context-mode compressors, the skill-packs, the installer/proxy products).

The single most important thing the evaluator named — *close the honesty gap between "framework" and what
executes* — is what this release does. ORDO is an honest research artifact with a small trustworthy runtime,
one excellent finding (the compression is the grammar + output contract, not the glyphs), and now a real
spend meter that lets anyone measure its dollar delta — packaged and labeled as exactly that, no more.
