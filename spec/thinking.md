# ORDO thinking.md — the single-pass, complexity-adaptive thinking protocol

> The dispatcher and the in-reasoning instincts that fire on EVERY task before any multi-pass gate. This is
> the **1× layer**: one pass, one strong model, no second run. It does not replace the 6 gates (REFEED /
> EXPERIMENTALIST / EVALUATION / AUTONOMY / CONTEXT-ROT / decompose) — it **sequences** them and makes them
> RARE, escalating only by exception. Honest-first per §0 of `OPERATING-PROFILE`: every instinct below ships a
> scoped, defensible claim; none re-introduces a dead lever. Depth in `spec/` per gate. Grounding: Snell
> 2408.03314 (test-time compute), Sakana AB-MCTS, MoA 2406.04692, Reflexion 2303.11366, MT-Bench 2306.05685,
> FrugalGPT 2305.05176, Manus context-engineering, 12-factor-agents, Anthropic building-effective-agents.

## 0 · One law
Spend thinking **proportional to stakes**, in ONE pass, and escalate to a multi-pass gate only by exception.
Width, verification, and refinement all measurably HELP on hard work and measurably HURT (or are pure tax) on
easy work — so the first move is always to classify, then apply only the instincts the task earns. Opt-out is
first-class: any instinct can be skipped with a one-line reason; this is a discipline, not a ritual.

## 1 · classifyTask — the single upfront triage (extends CONTEXT-ROT §1, does not fork it)
Before committing to an approach, spend ONE cheap in-reasoning judgment — the same read you already do to
understand the ask, at zero extra cost, no tool calls, no second model. REUSE the CONTEXT-ROT 5-trigger
classifier verbatim as the HARD signals; do not invent a parallel one:

- **Reversibility** — wrong answer costs more than a re-ask? (money / sends / migrations / a claim shipped to a user) → HARD.
- **Right-answer cardinality** — one deterministic answer (LIGHT) vs a real fork (architecture / algorithm / novel design) → HARD.
- **Horizon** — answerable now vs >~15-20 tool calls or multi-phase → HARD.
- **Breadth** — single file/lookup (LIGHT) vs >5 files or >1 lane/repo → HARD.
- **Load-bearing facts** — none (LIGHT) vs IDs/contracts/schema/decisions that must survive a long horizon → HARD.

**ANY HARD trigger ⇒ STRICT mode; else LIGHT.** This gate routes EFFORT and STRUCTURE only — NEVER a weaker
model (`OPERATING-PROFILE` §6 stays default-strong; routing is lossy, a short prompt can be a hard fork).
Honest tier: the overhead it SAVES on LIGHT turns is measurable (P2/P3 proxy improves vs always-strict); the
classifier's own LIGHT/HARD **accuracy is UNMEASURED** — a conservative judgment call, not a proof (the same
admission CONTEXT-ROT already makes). Never claim a misroute rate until a harness records one.

Re-check at boundaries, not continuously: a LIGHT task that trips horizon/breadth mid-run is PROMOTED to STRICT
at that tick (write the anchor + acceptance criteria to a fresh ledger first). Promotion is one-way; never
demote mid-run.

## 2 · LIGHT mode — the default for most turns
Act directly. No ledger, no compaction machinery, no REFEED/EXPERIMENTALIST gate, minimal cleaning. Looping or
externalizing here is pure tax. The only two always-on instincts that still fire (both lossless, both 1×):
**DICTION (§5)** and, on the one deciding claim, **VERIFY-ASSERT (§6)**. Everything else is suppressed. Just answer.

## 3 · STRICT mode — armed only on a HARD verdict
Lead with a sectioned plan. Arm the LEDGER + compaction track from tick 0 (CONTEXT-ROT). Then fold in the
instincts the fork actually needs, each opt-out-able with a reason: **GOAL-LOCK (§4)** on any multi-step plan,
**REUSE-REPLAN (§7)** before any new file, the **DIVERGENCE WIDTH MOVE (§8)** on a wide-solution-space fork,
**SELF-HEAL (§9)** on any failed gate. Route the work to its gate by the fork it is: one right answer → REFEED;
real fork → EXPERIMENTALIST; any artifact before done → EVALUATION. Keep state out of the window.

## 4 · GOAL-LOCK — pin the goal, re-derive the next step (STRICT, multi-step; 1×)
Grounded in Manus attention-recitation + 12-factor stateless-reducer + Anthropic orchestrator-workers. Single
pass, append-only, no extra model call.
1. **Lock the goal ONCE** before step 1 — a one-line immutable END-GOAL anchor (done-condition in the user's
   terms + success test + hard constraints). Recite it verbatim at the head of every plan revision; never
   silently edit it — if the goal genuinely changes, REPLACE it explicitly and say so. (Reuses the CONTEXT-ROT
   KEEP-rule-1 head placement; do NOT stand up a second compaction track.)
2. **Plan is a hypothesis, the goal is the contract.** Do not carry a step forward just because it was written.
3. **Re-derive on divergence** (load-bearing): when a step finishes, read how it ACTUALLY came out, not how it
   was planned. If the result differs (shape/file/approach/partial), do NOT run the next planned step blind —
   regenerate it from {locked goal + actual state} in one pass, then run it. If the result matched the plan, run
   the planned step unchanged (zero overhead). This lives INSIDE the AUTONOMY observe→verify transition; it is
   not a second control loop and not a critique pass.
4. **One-line inline drift check** before each step: "does this still move the LOCKED goal given what actually
   happened?" Yes → act; no → re-derive.

Honesty: REAL mechanism / UNMEASURED outcome — claim the discipline, never a "reduces drift by X%" number until
a blind goal-direction A/B exists (the P6 evidence bar).

## 5 · DICTION — always-on cheapest-faithful WORD choice (lossless; sub-discipline of ponytail)
Belongs in `output.md` Part 2 UNDER ponytail (ponytail deletes WHICH words survive; diction chooses the FORM of
the survivors), inline at generation, never a rewrite pass.
- When two phrasings carry equal signal, pick the one that is **fewer tokens AND more common**: "use" over
  "utilize", "so" over "as a result", "about" over "approximately". Plain Germanic core over Latinate inflation.
- The higher-frequency word tokenizes shorter AND samples more deterministically (lower per-step entropy), so
  output is **steadier across runs** at no quality cost.
- **Hard floor — TIE-BREAK only, never a quality cut:** never trade a precise term for a vague short one (keep
  "idempotent", "race condition", "p95"); never touch a quoted string, identifier, API name, or number; never
  compress explainer/creative prose into worse prose.
- Do NOT consult a synonym/swap table. ORDO measured that lever at ~1% (`freqmatrix.py`: BPE already 1-tokens
  most common words). **Claim DETERMINISM + cleaner register; do NOT claim a token-% win** — the token savings
  live in ponytail/format, not diction.

## 6 · VERIFY-ASSERT — derive-then-assert the one load-bearing claim (always-on; 1×)
The single-pass distillation of REFEED's re-read; fires INSIDE the first pass on the ONE claim the answer stands
or falls on. Grounded in MT-Bench reference-guided judging (confident-wrong 14/20→3/20 in one prompt) +
Reflexion precondition-check.
1. **NAME the load-bearing claim** — the number, the signature/contract, the "X is best" pick, the
   existence/possession/availability fact. A second, non-deciding claim is a caveat, not a second pass.
2. **SELF-SOLVE-FIRST, THEN MATCH** — derive that claim independently (re-compute the value, re-read the actual
   source/signature, restate the real goal), then write the answer to MATCH your derivation. Do not grade your
   first instinct correct; grade it against what you just derived.
3. **BEST-SUPPORTED OVER FIRST-FLUENT** — pick the candidate your derivation supports, not the smoothest. Kill
   "I think this is best": either you checked (state the support) or mark it unverified.
4. **SOFT-OVERWRITE A WEAK PROMPT** — if the grounded answer diverges from the literal ask, lead with the
   better-supported suggestion + the one-line reason, then still answer the literal ask. Offer, never silently fork.
5. **MARK, DON'T LOOP** — tag the claim with its support tier (derived/checked · grounded-in-a-real-source ·
   unverified-stated-as-such). The mark IS the deliverable. Escalate to REFEED ONLY when a load-bearing claim
   stays unverified AND being wrong is expensive.

Scope (honesty bound): ONE claim, ONE in-pass derivation; the instant you re-draft the whole output against a
typed critique you have left verify-assert and entered REFEED. Strong-model-only lift (Reflexion: weak models
0.26→0.26). It reduces confident COMMITMENT on the checked claim; it is NOT a measured factual-hallucination
reduction — no number until an own-corpus single-pass A/B is run (the corpus number belongs to REFEED at 3.3×).

## 7 · REUSE-REPLAN — the one pre-build check (STRICT, before any new file; 1×)
Grounded in Anthropic explore→plan→code + reference-existing-patterns and Ronacher's refactor-timing rule. Rides
the CODE-CONTEXT graph as a navigation index; vendors no AST.
1. **Reuse-first** — query the code-context graph (or grep) for something that already does this or 80% of it.
   Name the candidate. Default to EXTEND it or copy its pattern over authoring a parallel one. Use only deps the
   project already uses; write a small function before adding a dependency.
2. **Scale-judgment** (ONE call, against the END goal not the ticket): if I build on this, does its shape survive
   where this is going, or force a rewrite within a few steps? Replan only on a NAMED structural reason
   (duplicated state, a god-file about to grow, a foundation that locks the wrong boundary, complexity past the
   component-library threshold). Do NOT replan on taste or impossible future inputs — that is gold-plating,
   scores DOWN (defer to the §0 lean / 10-is-not-the-target rule).
3. **Act once** — reuse → extend; doesn't scale → replan the structure FIRST (state the new shape), then build on
   the fixed foundation in the same pass. A genuine architecture fork escalates to EXPERIMENTALIST; else inline.

Honesty: PROCESS claim, not a measured reduction. P7/P8 stay GROUNDED until a teardown→measure run clocks
rework/rebuild-vs-fix; no "−X% rework" number before then.

## 8 · DIVERGENCE — a FLAG, not a search (single-pass width CUT; claim NULL)
**The single-pass generate-2-3-and-self-cull move is DELETED.** It measured net-negative (4 win / 1 tie / 7 loss,
AGENT-JUDGED) and the science predicts exactly that null: Snell 2408.03314 (the stronger optimizer DEGRADES
within-capability bins and every gain needs a VERIFIER/PRM), MoA 2406.04692 (width helps only with a synthesizing
AGGREGATOR + DIVERSE proposers), Sakana AB-MCTS (width's lift is selector-bound — Pass@k collapses with a naive
selector). Single-pass §8 had none of those — same-model, no verifier, self-cull — so it shipped the regression,
not the lift. We **delete** it rather than threshold-tune it (a higher bar still ships the same verifier-less generator).

**What survives is ONE line — a difficulty FLAG, no generation:** if the task is HARD-real-fork (classifyTask) AND
the modal answer reads generic against the explicit win-condition, do NOT diverge here — **ESCALATE to the
EXPERIMENTALIST gate** (`spec/experimentalist-gate.md`), which supplies the missing aggregator (synthesize-best-of-
both) and the missing verifier (adversarial cull against a written win-condition) — the two ingredients the science
requires, and the only width config that survived a real cull (3W/1T, the tie failed safe). **Default = take the
modal answer** (Snell's easy-bin rule). Claim **NULL** for single-pass width; never "more creative across fields."
The flag's fire/no-fire boundary could later be COMPUTED against an oracle pass@1 set (Snell §3.2).

## 9 · SELF-HEAL — on a failed gate, diagnose the CAUSE before regenerating (STRICT; the REFEED failure-branch)
Belongs in `framework.md` under REFEED as the failure-branch router, not a new pass. Grounded in Reflexion's
ablation: blind retry collapses to baseline on hard tasks (0.68→0.60); the value is the ONE verbal
credit-assignment step. On a failed gate/test/assertion, write ONE typed reflection line —
**cause: \<which earlier step/premise/assumption produced this\>** — then branch ON THE DIAGNOSIS in the same pass:
- **local bug** (footing sound, one wrong line) → REFEED the delta in place.
- **structural** (the cause is an earlier premise) → DISCARD the broken branch and regenerate from the re-derived
  premise. Do NOT re-adapt a footing the diagnosis just named as the fault (the blind-retry failure mode).

**SELF-GROW** (human-run, evidence-gated): a lesson enters the existing `tools/pillars.py` scoreboard (or
`docs/lessons`) — {pattern, cause, fix, gate-that-caught-it}, bounded + deduped — ONLY after a real gate caught a
real failure; a run reads matching lessons at GATE-PRE. **Nothing self-modifies at runtime.** Claim the human-run
accretion; the word "self" stays a FALLACY — NEVER claim autonomous self-growth (GTM claim 8 is NULL).
**SELF-CLEAN** (loop-kill ~3 reps, revert-gate, rot-ledger, cost-meter) is already shipped — confirm, don't rebuild.

## 10 · The opt-out contract (why this is a discipline, not a ritual)
Every §4-§9 instinct is skippable with a one-line reason ("LIGHT verdict, skip goal-lock"; "deterministic API,
skip divergence"). The §5 diction and §6 verify-assert instincts are always-on because they are lossless and 1×.
The dispatcher (§1) is the only mandatory step. Get the classification wrong and you either over-spend (STRICT on
a lookup) or under-verify (LIGHT on a migration) — so the one place to be conservative is the HARD triggers,
which is why they are inherited verbatim from the rot gate, not re-tuned.
