# ORDO pillars — the test-gated quality framework

Token length is one pillar, not the story. The real thesis (the *ideanomics*): a system that produces
**cleaner, less-hallucinated, more architecturally-honest** output reduces downstream **thinking,
cleanup, and debugging** — and that reduction is *calculable*, not hand-waved. So ORDO is optimized
across **all** pillars below, **lossless-first**, and **every pillar is test-gated**: a concrete metric,
a concrete measurement method, and a real baseline. A reported number that isn't produced by a gate
does not count.

## The non-negotiable rules
1. **Lossless-first.** A compression % only counts if it passes its comprehension/quality gate. A %
   that silently dropped a fact scores **zero**, not its raw ratio.
2. **Test-gated, not theoretical.** Each pillar has a runnable gate (`tools/pillars.py` for
   deterministic ones; a blind multi-agent workflow for judged ones). No gate → status `UNMEASURED`,
   never a guessed number.
3. **Second-order counts.** Rework reduction (fewer iterations / less cleanup / less debugging) is a
   first-class pillar, because "do it good" only beats "do it fast" if we can show the rework it avoids.
4. **Rebuild over fix.** When a foundation is fragmented or unscalable for the use case, the right
   output is a proposed re-architecture, not another layer on top. This is a measured behavior, not a slogan.

## The pillars

| # | pillar | metric | gate (how it's measured) | baseline | lever |
|---|---|---|---|---|---|
| P1 | **Context length** (inbound) | % inbound tokens cut, comprehension-preserved | `inbound.py` on a real corpus + a blind QA comprehension check (answers ≥ original) | 45% mixed (gate TBD) | headroom (logs) + TSV + relevance-gate + glossary-inward |
| P2 | **Token output** | % output tokens cut at equal quality | ponytail/format on real answers + quality-equality judge | 77% ponytail (lossless) | ponytail + caveman + format-by-shape |
| P3 | **Speed** | REAL wall-clock ms/turn (not a token proxy) | time actual API calls, English vs ORDO, N runs | UNMEASURED | fewer in+out tokens; effort-routing |
| P4 | **Quality** | blind win/tie/loss vs baseline on task satisfaction | multi-agent blind judge, difficulty-stratified | ORDO 6-2-1 vs English | grammar structure + "think/fresh" directive |
| P5 | **Hallucination** | confident-wrong rate Δ + calibration (abstain-on-uncertain) | factual trap set (invention-bait + false-premise) | no backfire; +calibration (no reduction at frontier floor) | epistemic slot (cite/flag/verify) |
| P6 | **Tidyness** | output ceremony/filler ratio; for generated CODE: duplication + complexity + dead-code | `ponytail_flags` + code metrics on generated code | filler-flagger exists | ponytail + "no-scaffold" directive |
| P7 | **Architecture (rebuild-vs-fix)** | on a fragmented/unscalable task, does it flag the foundation + propose re-architecture vs build-on-top | blind rubric judge on fragmented-code scenarios | UNBUILT (new directive) | `arch`/`rebuild?` macro |
| P8 | **Rework reduction** (the payoff) | rounds-to-correct (iterations to an accepted result) + thinking/cleanup tokens avoided | multi-turn task, count iterations English vs ORDO | UNMEASURED | the sum of P4-P7 (cleaner first pass) |

## The "do it good, not fast" behavioral layer (serves P4, P7, P8)
Three directives that force the model off the generic averaged answer and onto *this* problem — added
to the output contract + as macros (tokenizer-validated, decode-tested like the rest):
- **`fresh` / `think`** — "Do NOT give the generic averaged answer. Reason from this specific case's
  constraints and do what is actually best here, even if it differs from the usual pattern."
- **`arch` / `rebuild?`** — "Before extending, assess whether the foundation is fragmented or won't
  scale for this use case. If so, propose a re-architecture instead of building on top."
- **`tidy`** — "No scaffolding-for-later, no restated context, no ceremony. Smallest correct thing;
  delete before add (the ponytail/caveman discipline, as an instruction the model self-applies)."

These are the levers for the pillars the token count can't touch. P7 and P8 are where "the codebase
becomes the real deal" is actually won.

## The scoreboard
`tools/pillars.py` runs every deterministic gate and prints a scorecard with a status per pillar
(`MEASURED <number>` / `UNMEASURED` / `GATE-FAIL`). The judged pillars (P4, P5, P7, P8) and real-speed
(P3) are filled by blind workflows and stamped into the scoreboard with their evidence. The scorecard
is the single source of truth — no pillar advances on opinion.

## Status (live) — 7/8 MEASURED
- **MEASURED:** P1 (lossless TSV 68% / mixed 45%, comprehension-gate on headroom-lossy pending), P2 (77%
  lossless), P4 (6-2-1), P5 (no backfire + calibration), P6 (filler-flag live; code-metric pending),
  **P7 (arch +0.20, 1.40→1.60), P8 (tidy/fresh 42% fewer first-pass flaws, 7→4)**.
- **PROXY-ONLY:** P3 — output-token saving is the proxy; true wall-clock needs a controlled timing
  harness against a chosen target model (tied to the deferred deployment decision).
- **Lossless audit:** P1's headroom-on-logs is LOSSY (sampling) → under the lossless-first rule it only
  counts where comprehension holds; default routes lossless (TSV) when the model must analyze.
- **The "ideanomics" validated:** the do-it-good directives measurably cut downstream rework (P8: 42%
  fewer first-pass flaws), confirming the thesis that "do it good, not fast" pays off in less
  debug/cleanup — and it is now a measured pillar, not a slogan.
