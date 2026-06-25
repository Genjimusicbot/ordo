# ORDO IMPROVEMENT CHARTER

The single source of truth for what we measured wrong, what we keep, and the one rerun that settles it. Ordered
by value. Every line is honest about its tier. Governing law: a number prints only if a gate produced it, and no
instinct keeps complexity the measurement did not buy. Grounded in the papers behind ORDO (MT-Bench 2306.05685,
Reflexion 2303.11366, Snell 2408.03314, MoA 2406.04692, Sakana AB-MCTS, FrugalGPT 2305.05176, Manus/12-factor).

Tiers: **COMPUTED** (a deterministic gate or arithmetic over recorded votes produced it) · **AGENT-JUDGED** (a
model judged it) · **GROUNDED** (literature predicts it, no ORDO run yet) · **PENDING** (protocol built, the run
is blocked here because live cross-family API is unavailable — identical to how `clock-ab`/`rot-ab` already wait).

---

## 1 · measurement-rigor — the foolproof judge protocol `tools/judge.py` (highest value: it gates all the others)
**Decision: SCOPE to a five-lock judge protocol + two immediate CUTs. Build now, run when API-armed.**

First because every AGENT-JUDGED number flows through it. Without it, divergence's −3, goal-lock's +4, and
classifyTask's 100% are the same untrustworthy shape: Claude-authored AND Claude-judged, near-tie, small-N, on
corpora the answer was written against. Grounded in MT-Bench: self-preference (§3.3, judges favor their own family
10–25pp), position bias (Table 2, GPT-4 only 65% swap-consistent; §3.4 conservative fix = win only if it wins both
orders else tie), the agreement target (§4.2, judge-human 85% ≈ human-human 81%; Fig 2: reliability collapses on
the near-ties our n=6 reads live in), plus Hamel (judge on real traffic, report precision/recall not raw agreement).

**Five locks, each kills one gameable path:** (1) cross-family panel — Claude artifacts judged only by ≥2 non-Claude
families; same-family appears only as a logged "self" bias-gap column, never a vote. (2) position-swap conservative
— every pair judged A/B and B/A, win only if it wins both, else forced tie; drop judges under 60% swap-consistent.
(3) blinding + length-control — strip every ORDO/ON/OFF marker; quarantine >20% length-delta pairs. (4) real-workload
corpus — sample the 71,736 metered `~/.claude/projects/**/*.jsonl` messages, stratified, N≥50, hash frozen + committed.
(5) stats + pre-registration — Wilson 95% interval + two-sided sign-test, "WIN" only if the interval excludes 0.5;
a ≥20-item human-gold subset anchors judge-vs-human κ to the MT-Bench bar, below it the judge is "unvalidated" and
no pillar may cite it. Output contract: `judge.py` writes only COMPUTED rows backed by `judge-ab.json`; `pillars.py`
reads them like `measure-ab`/`clock-ab`/`rot-ab`.

**Two CUTs, runnable now:** CUT-1 classifyTask "100%" → CONSISTENCY-ONLY; CUT-2 divergence stays WITHDRAWN; and
goal-lock's +4 is de-headlined to "directional, single-family, n=6, 95% interval ≈ [0.39, 0.86] straddles 0.5."

**Foolproof:** it can only DEMOTE, never manufacture a win — run honestly it may turn goal-lock's +4 into a wash,
and that outcome is allowed to print. **Tier:** the cuts + the `judge.py` scaffold + Wilson/sign-test/κ math =
COMPUTED-now (pure stdlib, testable cold against synthetic votes); the N≥50 cross-family run = PENDING.

---

## 2 · classifyTask-groundtruth — the misroute-cost harness `tools/route_truth.py` (the moat's missing number)
**Decision: BUILD a ground-truth misroute-cost harness + a frozen labelled corpus. Withdraw "100% consistency."**

classifyTask gates everything downstream and has no accuracy number — only consistency, which (context-rot.md
admits) "may mean the items were unambiguous." Grounded in FrugalGPT (2305.05176): accuracy and cost are SEPARATE
axes, so a misroute is a point in 2-D cost space, not one error; its MPI matrix shows the cheap model is right where
the expensive one is wrong 6–13% of the time → routing truth is per-item empirical, never a surface property.

**Design:** `route_corpus.jsonl`, N≥40, frozen + content-hashed. Each item `{id, prompt, label, basis, adversarial,
family}`. The label is OUTCOME-derived (STRICT iff a HARD trigger was objectively true of the realized task), `basis`
records which realized fact sets it — auditable, not circular. Strata: 30% easy LIGHT, 30% clear STRICT, **40%
ADVERSARIAL** (short-but-hard "rename our auth cookie" = STRICT; long-but-trivial ramble = LIGHT; "clean up the test
users" = a prod DELETE = STRICT). Half the adversarial items are MINED from real transcripts where the classifier's
call and the run's actual outcome disagreed — ground-truth-by-construction, un-tunable. **Asymmetric misroute-cost
matrix:** over-spend (STRICT-on-LIGHT) = bounded ~1-unit tax; under-verify (LIGHT-on-STRICT) = unbounded on the
irreversibility row, weight 10, ∞-flagged where basis=irreversible. Headline = cost-weighted misroute rate, reported
with the raw 2×2 and the two directional rates separately, never collapsed. Hard floor: under-verify-on-irreversible = 0.

**Foolproof:** no judge in the loop (string-equality to a frozen outcome-pinned label). The 40% adversarial stratum
is built FROM the rule's failure mode, so a length/surface heuristic scores near-zero there by construction. Report
the mined-only sub-rate separately so the floor rests on the un-gameable subset. **Validating:** classifyTask vs
control-0 (length-threshold router) vs control-1 (always-STRICT); it must hold the irreversible floor, beat
always-STRICT's over-spend%, and crush the length-router on stratum C. Can come back RED. **Tier:** COMPUTED, zero
API. Closes BUILD-LOG open item #3.

---

## 3 · verify-assert-scope — the baseline-fails-first trap corpus `tools/trap_corpus/` (turns a WASH into a real verdict)
**Decision: FIX the corpus, do not re-run the old set. The 8/12 ties were a CORPUS failure, not an instinct failure.**

The washout had a known cause, named in BUILD-LOG's VOKU note: "the plain baseline is already at the floor (0
confident-wrong)." You cannot measure a confident-wrong-rescuer on items where nothing is confidently wrong.
Grounded in MT-Bench Table 4 (a planted wrong answer drives confident-wrong 14/20 → 3/20 with derive-then-assert —
the delta only appears when the item MISLEADS) + Reflexion (self-correction is emergent in strong models only;
the substrate is computation, a signature passing a flaky self-test, hallucinated possession/freshness).

**Design:** 24 items, 6 per zone, each `{prompt, planted_misleader, oracle(answer)->bool, baseline_must_fail:true}`.
Zone A computation-misled (plant a wrong f(2), oracle = exact recompute). Zone B signature-vs-spec (self-test passes
on a subtly-wrong impl, oracle = HIDDEN tests). Zone C freshness/possession (stale-state plant contradicted by a
provided source-of-truth, oracle = string-match). Zone D strong-model-hard. **The un-gameable core is the ENTRY
GATE:** an item enters only if a 3-seed no-verify run fails it ≥2/3 — items the baseline already passes are REJECTED
at build time, which kills the 8-tie washout by construction. Score: net = Σ[oracle(B)−oracle(A)], McNemar on
discordant pairs. No judge → COMPUTED, no position bias, no self-enhancement.

**Foolproof:** verify-assert can only score net-positive by flipping an oracle-confirmed-wrong to an
oracle-confirmed-right answer — it cannot win on style. Built to KILL the claim: if it STILL washes on a baseline-
fails corpus, the instinct gets CUT from always-on. Honesty bound shipped with the number: a net-positive proves
reduced confident-COMMITMENT on misled items, NOT a general hallucination cut. **Validating:** net ≥ +6 with
McNemar p<0.05 → COMPUTED lift, debt #4 retired; net ≈ 0 → confirmed no-op, CUT. **Tier:** COMPUTED if the target is
the local strand model; the 24×2×3 ≈ 144 completions are the only live cost (PENDING if they must hit a hosted API).

---

## 4 · goal-lock-invest — the goal-lock bench (the one instinct with directional lift; make it the STRICT backbone)
**Decision: FIX and build a bench mirroring `rot_bench`; promote to the mandatory STRICT backbone only after it
clears tier-one COMPUTED exact-match + the cross-family judge.**

goal-lock is the single instinct that measured positive (8W/0T/4L, +4) — exactly why it must not be headlined on
n=6 single-family; it is the most tempting number to launder. Grounded in Manus recitation + the 12-factor stateless
reducer + Anthropic ground-truth: re-derive each step from {immutable goal + ACTUAL prior result}, not the stale plan.

**Design:** a bench mirroring `rot_bench.py`. Items where the ACTUAL prior result invalidates the planned next step,
each with a key-determined ground-truth action. Arm A follows the plan; arm B re-derives. Construction-validation
forces a real divergence per item (the planned step must genuinely be wrong), so B can only win by matching where A
diverges. Tier-one = exact-match against the key-determined action → COMPUTED, no self-judge. Tier-two = cross-family
judge (through §1) → AGENT-JUDGED, separate row. **Validating:** 24 items; tier-one delta (B−A) COMPUTED;
tier-two AGENT-JUDGED, never merged. **Tier:** construction + tier-one + validation = COMPUTED now offline;
tier-two = PENDING.

---

## 5 · divergence — SCOPE the §8 width move to a difficulty FLAG; CUT its generative half (claim NULL)
**Decision: SCOPE-TO-DISCRIMINATOR-FLAG. CUT the generative half of §8; KEEP one line that routes
hard-fork-weak-modal cases to the experimentalist gate. Do NOT merely raise the switch-bar — a higher threshold
still ships the same verifier-less same-model generator that measured net-negative.**

Lowest by value because the honest answer is mostly subtraction: the move lost 7/12, the claim is withdrawn.
Grounded in three papers that all predict the exact null §8 was: Snell 2408.03314 (the stronger optimizer DEGRADES
easy bins, every gain needs a verifier/PRM); MoA 2406.04692 (width helps only with a synthesizing AGGREGATOR + DIVERSE
proposers, neither present single-pass); Sakana AB-MCTS (width's lift is selector-bound — Pass@k 30% → Pass@2 19.2%
with a naive selector). §8 single-pass was same-model + no verifier + self-cull: the null all three predict.

**Design:** rewrite §8 to "DIVERGENCE — a FLAG, not a search." §8 ships NOTHING generative single-pass. The only
surviving line: if the task is HARD-real-fork AND the modal answer reads generic against the explicit win-condition,
do NOT diverge here — ESCALATE to the EXPERIMENTALIST gate, which supplies the missing aggregator
(synthesize-best-of-both) and the missing verifier (adversarial cull against a written win-condition). Default = take
the modal answer. **Foolproof:** the move that produced the −3 is DELETED, not threshold-tuned; what remains routes to
an already-separately-measured gate (3W/1T, tie failed safe), so no new unmeasured claim is created.
**Tier:** AGENT-JUDGED. Low effort: ~15-line spec rewrite + one cross-link; the A/B reuses the existing harness.

---

## Honest bottom line
Of the seven single-pass instincts, the measurements bought complexity for exactly **two and a half**: goal-lock
(real lift, COMPUTED-able backbone), classifyTask (a real gate once it has a misroute number — currently
consistency-only), and verify-assert conditionally (only on a baseline-fails corpus, prove-or-cut). divergence's
generative half is **deleted**. diction, self-heal, and reuse-replan stay as lossless/process disciplines that never
claimed a measured win — they keep their honest GROUNDED tier and earn nothing more until a gate says so.

---

## The subtraction call (across the 7 single-pass instincts)
1. **classifyTask (§1)** — SCOPE-NARROW + re-tier. KEEP the gate (it routes everything) but CUT the "100%
   consistency" accuracy claim → CONSISTENCY-ONLY; earn a real COMPUTED misroute number via `route_truth.py`.
2. **goal-lock (§4)** — KEEP, promote to mandatory STRICT backbone — but hold the promotion until tier-one COMPUTED
   exact-match clears it; the n=6 single-family +4 is de-headlined to "directional."
3. **diction (§5)** — KEEP as-is, no new claim. Lossless sub-discipline of ponytail; never claimed a win, nothing to launder. GROUNDED.
4. **verify-assert (§6)** — SCOPE-NARROW, conditional KEEP. Prove on the baseline-fails-first corpus (net≥+6, p<0.05) or CUT from always-on.
5. **reuse-replan (§7)** — KEEP as-is, no new claim. A single pre-build check; process discipline; lean by definition (it PREVENTS files). GROUNDED.
6. **divergence (§8)** — CUT the generative half; SCOPE the remainder to a one-line escalation FLAG. The headline subtraction.
7. **self-heal (§9)** — KEEP as-is, no new claim. Cause-first regenerate (Reflexion); a process router under REFEED. GROUNDED.

NET: **1 hard CUT** (divergence's generator), **2 SCOPE-NARROWS** that must earn a COMPUTED number or shrink further
(classifyTask accuracy, verify-assert always-on status), **1 conditional promotion** (goal-lock), **3 kept-as-honest-
process** (diction, reuse-replan, self-heal). The lean move is to stop printing claims they cannot back, not to keep
building scaffolding around them.

---

## The one rerun (the highest-value un-gameable measurement)
The cross-family, real-corpus, N≥50, pre-registered judge run that retires **goal-lock**, executed THROUGH
`tools/judge.py` so the same protocol that validates goal-lock simultaneously proves the harness itself.
Frozen before the run (append-only `judge-ab.json`): the claim (arm B re-derive beats arm A follow-plan on
multi-step tasks where the actual result invalidates the planned step); a real-traffic N≥50 corpus, content-hash
committed BEFORE any completion; identical model/temp/prompt except the goal-lock block; a cross-family panel (≥2
non-Claude families, same-family logged as a "self" column not a vote), every pair judged both orders (win only if
both, else tie), judges under 60% swap-consistency dropped, markers stripped, >20% length-delta quarantined; Wilson
95% + sign-test, WIN only if the interval excludes 0.5; a ≥20-item human-gold subset gates judge-vs-human κ to the
MT-Bench bar or the panel is "unvalidated" and the number cannot print. Two independent rows print: tier-one COMPUTED
exact-match (B−A vs key-determined actions) AND tier-two AGENT-JUDGED Wilson/sign-test. PASS only if BOTH. **The rerun
is allowed to kill its own most-favored instinct — that is what makes it un-gameable.** Blocked here only by live
cross-family API; fully specified to run the moment keys are armed.

---

## The standing foolproof self-check (run against ANY ORDO measurement before its number prints)
Derived from the three null-launderings we already committed (divergence's self-judged width win, classifyTask's
consistency-as-accuracy, verify-assert's wrong-corpus wash). Fail any line → it does not print as a win.

1. **NO SELF-JUDGE.** Claude-authored AND Claude-judged → presumed inflated by the MT-Bench self-preference margin
   (10–25pp), NON-REPORTABLE as a win. Same-family may appear only as a logged "self" bias-gap column.
2. **POSITION-SWAPPED, CONSERVATIVE.** Every pair scored in both orders, win only if it wins both, else forced tie.
3. **BLIND + LENGTH-CONTROLLED.** All ORDO/ON/OFF markers stripped before judging; >20% length-delta pairs quarantined.
4. **REAL CORPUS, FROZEN BEFORE THE RUN.** Sampled from real traffic, content-hash committed BEFORE any completion.
   A corpus the answer was written against scores CONSISTENCY ONLY, never accuracy.
5. **BASELINE-FAILS-FIRST** where the claim is "I rescue errors." Entry gate admits only items the no-instinct
   baseline actually fails (≥2/3 over seeds). A corpus the baseline passes produces a fake tie.
6. **PREFER A DETERMINISTIC ORACLE OVER A JUDGE.** Recompute / hidden-test / source-match / exact-match against a
   key-determined label lands COMPUTED with no judge to agree with itself. A judge is the last resort.
7. **STATS, NOT VIBES.** A proportion with a 95% Wilson interval + sign-test p; "WIN" only if the interval excludes
   0.5. Any n<~30 near-tie prints DIRECTIONAL, never WIN. (n=6 with [0.39, 0.86] is directional.)
8. **PRE-REGISTERED + APPEND-ONLY.** N, corpus hash, judge set, win/tie rule written to the AB JSON BEFORE the run.
9. **TIER HONESTY — MEASURED-OR-MARKED.** The printed tier matches what produced the number. AGENT-JUDGED may NEVER
   print as COMPUTED. A blocked run keeps its "protocol built, run pending" string — never a placeholder win.
10. **THE KILL-CLAUSE.** The measurement is built so it CAN return a null that demotes the instinct — including the
    author's favorite. A harness that structurally cannot return a flattering-failure is itself invalid.
11. **SUBTRACT BEFORE YOU SCAFFOLD.** Did the measurement buy this complexity, or am I preserving it on ambition? If
    the honest read is CUT, cut it — delete the regressing path, do not threshold-tune it back to life.

**GOVERNING LAW:** a number prints only if a gate produced it, the gate passes 1–8, the tier matches 9, the harness
satisfies 10, and the instinct survived 11. Any "win" that skips a line is a laundered null and is withdrawn.
