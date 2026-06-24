# ADAPT progress ledger — ORDO to done (append-only)

Criteria: C1 research · C2 deanchor · C3 ≥10% floor · C4 quality · C5 hallucination · C6 speed ·
C7 intent-as-symbol · C8 harness · C9 committed+verdict.

| tick | phase | action | result | criteria green |
|---|---|---|---|---|
| 0 | ANCHOR | wrote acceptance spec (C1-C9), kickoff pre-authorized | OK | 0/9 |
| 1 | DISCOVER | parallel digest of 20 xeno docs → 63 mechanisms → plan | OK | 0/9 |
| 2 | P5 | wrote docs/research-synthesis.md (12 mechanisms, ≥8 beyond density) | **C1 PASS** | 1/9 |
| 3 | P5/C2 | deanchor experiment: English 437 / readable 297 (+32%) / glyph 285 (+35%) o200k; blind decode readable **2.00/2** vs glyph 1.95; glitch screen clean | **C2 PASS** → readable is default, glyph opt-in | 2/9 |
| 4 | P6 | built harness/ (ordo.py parser+decoder, output.py format-picker); harness/test_ordo.py 8/8 green + output self-check | **C8 PASS** | 3/9 |
| 5 | P7/C3 | end-to-end floor: 3 realistic exchanges (prompt+output) English→ORDO = 495→178 = **64%** combined | **C3 PASS** | 4/9 |
| 6 | P8/C4+C6 | blind A/B 9 tasks: quality ORDO 6 wins / 2 tie / 1 loss (structure-driven, readable-ORDO) → **quality holds/exceeds**; output tokens 6468→4423 = ~32% (≈48% ex one over-delivery outlier) | **C4 PASS, C6 PASS** | 6/9 |
| 7 | P7/C7 | built spec/macros.md (16 intent-as-symbol macros, avg 8.2tok→1.4tok, saved 6.8/use); decode test launched | running | 6/9 |
| 8 | P8/C7 | macro decode test: mean **1.8/2** (54/60), deterministic; bare-subject fix noted | **C7 PASS** | 7/9 |
| 9 | P8/C5 | hallucination v1: both arms 0/24 confident-wrong, 8/8 abstain — markers DON'T backfire but test under-discriminates (easy fictional items); T1 escalation → harder traps | inconclusive → re-run | 7/9 |
| 10 | P8/C5b | hallucination v2 (harder traps): both arms 0 confident-wrong / 0 false-premise / 0 invention; epistemic arm ABSTAINED on recall traps where plain volunteered (better calibration); no backfire | **C5 PASS** (null on reduction at saturated baseline, + calibration) | 8/9 |
| 11 | P9/C9 | wrote VERDICT.md (every measured number + cut list + recommendation); ORDO.md deanchor banner; harness gate 8/8 green | **C9 PASS** | **9/9 SUCCESS** |

## TERMINATION: SUCCESS (9/9 all criteria PASS, 2026-06-24)
All acceptance criteria green. The language is built, measured, and honestly verdicted. Headline: the
value is GRAMMAR STRUCTURE + OUTPUT DISCIPLINE (~64% end-to-end + quality ≥ English), not exotic glyphs
(deanchored). Full numbers in `VERDICT.md`. No criterion was reopened; green count rose monotonically
0→9. One T1 escalation (C5 harder traps) used; no T2+ needed. Commits local, not pushed.
