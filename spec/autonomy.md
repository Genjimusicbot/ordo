# ORDO autonomy gate — strict long-form agentic-autonomy framework

> The last gate. A strict contract any long-running coding agent (hermes/openclaw-class, or ORDO's own
> long runs) follows to stay safe over long horizons: a decidable loop, error handling + recovery, and
> the DESTRUCTION OF WRONGFUL LOOPS. Synthesized from our docs (ADAPT ladder/termination, the strand
> approval-queue) + external best practices. Composes after REFEED + the experimentalist gate.

# STRICT AUTONOMY FRAMEWORK — hermes/openclaw-class coding agents + ORDO long runs

> One law: **an autonomous run ends in exactly one named state — SUCCESS, STUCK, or BLOCKED-ON-HUMAN — and never silently spins, never rewrites its own objective, and never fires an irreversible side effect without passing the queue.** Everything below is the machinery that makes that law hold. Optimality is explicitly out of scope of every exit test, so the loop can actually terminate.

This is a control law, not a vibe. It composes three proven layers we already run — the ADAPT ladder/termination invariants, the ORDO REFEED quality loop, and the strand approval-queue/budget spine (`scripts/autonomy.py`, `scripts/strand_runner.py`, `scripts/actions_registry.py`) — and grafts the one external best-practice we do **not** yet own: **(tool,args,result) loop-signature fingerprinting** (OpenClaw `loop-detection`, TIDE doom-loop analysis).

---

## 0. Preconditions (refuse to start without these)

A run is **forbidden to begin** unless all four exist. No exceptions, no "I'll figure out done as I go."

1. **Immutable goal anchor.** Goal + acceptance spec are written ONCE, content-hashed, read every tick, **never written** by the loop. Any change is a human-gated `BLOCKED-ON-HUMAN` event. This is the structural kill for goal drift (ADAPT non-negotiable #6).
2. **Decidable acceptance set.** A boolean `DONE := all criteria PASS`, each criterion `{id, statement, check_cmd, pass_threshold, stake_tier∈{trivial,normal,high,irreversible}, status}`. **No machine-checkable criterion ⇒ no start.** "Better" goes to a backlog, never to the exit test (ADAPT non-negotiable #1).
3. **Three-scope budget envelope, armed.** Per-step (~3 retries), per-phase (~2 replans), per-run (max reframes, **max tokens, max spend, max wall-clock, max steps, max strands-spawned**). For self-directed runs the per-run money/kill ceiling is the armed **wallet** in `autonomy.py` (`set_wallet`); `gate()` (autonomy.py:161) is the single pre-action choke point.
4. **Write posture declared.** Live Mode default OFF (`actions_registry.live_mode_enabled`). Every mutating capability routes through `stage_proposal`; the agent has READ + PROPOSE tools only. OUTBOUND/paid/destructive classes are on the never-auto-approve denylist regardless of tier.

---

## 1. The autonomous loop (PLAN → ACT → OBSERVE → VERIFY) with gates

Outer skeleton is **Plan-and-Execute** (inspectable plan, vetoable before any action); inner per-subgoal motion is **ReAct** (act on freshly-observed world state, not a stale plan). Bound the inner loop with the step cap so ReAct cannot spin.

```
TICK (read state ONCE from ledgers; survives compaction/crash):
  0. GATE-PRE   autonomy.gate(); check step/token/wall-clock/strand-count caps
                PRE-action (gateway, not after). If the next action would
                exceed any cap → do not take it → HALT(STUCK).
  1. SELECT     pick loop-shape ONCE (ORDO classify-first): execute-until-correct |
                best-of-N→gate→synth | diverge-3→debate→pick→graft |
                draft→critique→rewrite | draft→blind-reread→reconcile |
                decompose→per-part-REFEED→barrier. Wrong shape = over/under-verify.
  2. PLAN/REPLAN  phases ≤5 steps; decompose ONLY high/irreversible or >3-action
                steps (demand-driven); stake-tag each step ONCE at plan time.
  3. ACT (BATCH) do a whole phase or ≤5 independent ready steps in parallel.
                Side effects → stage_proposal ONLY. Fingerprint EVERY action
                (§ kill-conditions): hash (tool, canonical-args), fold result hash.
  4. OBSERVE    read real results. This is the only source of truth for VERIFY.
  5. VERIFY     stake-calibrated, per-step, grader-never-the-doer.
                Run criterion check_cmd → typed verdict
                {pass, mode∈{wrong_output,missing_structure,parse_error,
                 degenerate,abstained}, observed, expected}.
                wrong_output is the highest-value signal; abstained is REWARDED.
                After any T2+ change → re-run FULL checklist as a REGRESSION suite;
                reject any fix that turns a frozen-green criterion red.
  6. ESCALATE-ON-FAIL  climb the ladder ONE rung (§2), never jump.
  7. WRITE      append to ledgers ONCE; freeze newly-green criteria; yield.
  8. TERMINATE-CHECK  evaluate the three exit states (§5).
```

Re-read state only after a crash or compaction, not between steps in a tick (batch-the-tick momentum doctrine). Progress is measured in **green criteria, not steps logged.**

---

## 2. Tiered evidence-gated escalation ladder (ADAPT) — the anti-thrash spine

On FAIL, climb **one rung at a time**, only after the rung below exhausts its bounded retries. ~95% resolve at T0–T1.

| Rung | Scope | Bounded budget | Gate |
|------|-------|----------------|------|
| **T0** retry-in-place | bump model/effort, same step | ~3 | none |
| **T1** local repair | fix step + its subtasks | ~2 | none |
| **T2** phase replan | current phase only, upstream **frozen** | ~2 | **+evidence** |
| **T3** plan amend | FUTURE steps only | bounded | **+evidence** |
| **T4** frontier reframe | not-yet-accepted frontier ONLY | per-run cap ~2 | **+evidence + human/budget** |

**Evidence gate (T2+):** escalation fires ONLY on a concrete artifact — a failing test, a measured metric below threshold, a reproduced error, a contradicted plan assumption, or a criterion the plan **structurally cannot** satisfy. It must name the at-risk criterion + the evidence. **"Feels suboptimal" is inadmissible** and never triggers a reframe. This replaces "reframe the whole plan after every action" (which never terminates) with a bounded climb whose scope widens only as cheaper repairs are proven exhausted.

**Self-adjust in the right scope.** A DOMAIN learning (a fact about the task) may update the not-yet-frozen plan frontier **this run** — that IS the self-adjustment. A PROCESS learning (about the framework/rubric) goes to lessons and applies **next run only**; the controller never edits itself mid-flight; the goal anchor is never edited autonomously.

---

## 3. ORDO REFEED + experimentalist gate + pillars — how quality composes in

The loop's VERIFY step (§1.5) on a non-trivial artifact *is* a REFEED cycle: **DRAFT → REFEED (run gate, emit TYPED verdict not prose praise) → DECIDE.**

- **Tiered gate, hardest-evidence-first:** `G-exec` (executable oracle / test / type-check / schema — always prefer) > `G-rubric` (each criterion a checkable assertion, only when no oracle) > `G-deanchor` (blind re-read reconstructs intent, for NL instruction-following).
- **DONE contract written BEFORE drafting:** GATE + TARGET band + BUDGET (Kmax + token ceiling). Kmax defaults: **1 easy (no loop), 3 hard-structured, 5 ceiling for open/diverge.**
- **Refeed only the MINIMAL DELTA** that flips a failing gate — never the whole transcript. Keeps context clean and the loop cheap.
- **Experimentalist gate** is the `diverge-3-to-5→debate→pick→graft` loop-shape, fired ONLY when the loop-shape selector classifies the task as open design (architecture forks, naming, "think differently"). It is a verification *shape*, not a default — best-of-N on an easy task is the canonical over-spend.
- **Marginal Q/T governor (pillar P9):** a pass that improves the gate by **less than its token cost** halts the loop (ΔQ/Δtokens below a pre-set floor). Honest core: **REFEED is not a token saver** — measured 3.3× token cost, net-positive only where a latent bug's downstream cost exceeds that, pure tax otherwise. Hence selective: classify first, Kmax=1 on easy, stop on the floor.

This is where ORDO and ADAPT fuse: ADAPT's criteria checklist *is* ORDO's gate set; ADAPT's frozen-green *is* ORDO's TARGET-met-per-criterion; ADAPT's STUCK report *is* ORDO's "best-so-far + honest shortfall naming red gates."

---

## 4. The approval queue for destructive side effects (the hard mechanical boundary)

**Autonomy proposes; a human (or an evidence-gated auto-approve rule) disposes. The agent never holds a direct side-effecting capability.**

1. **Propose-only by construction.** Strands/headless sessions get READ + PROPOSAL tools. Every mutation flows through `actions_registry.stage_proposal` + Live Mode. A strand cannot send an email; it can only stage one. The read-script sandbox is mechanically barred from reaching `stage_proposal`. **No new write paths, ever.**
2. **Three independent yeses for a destructive action:** `kill=off` AND `live_mode=armed` AND (auto-approve-tier OR human click). No single failure or single prompt-injection can fire it.
3. **Pre-execution classifier on the ASSEMBLED payload**, not the literal string — re-check a shell command built up before exec. The destructive guard sees only user messages + tool-call payloads (strips the agent's own reasoning), so the agent cannot rationalize a dangerous action into approval and the guard is robust to prompt injection. **Deny > ask > allow, first match wins.** Keep this guard OUT of the model's control path (the HTTP kill-switch `routes_autonomy halt/resume` has "no model in the path" by design).
4. **Earned widening, fail-closed.** A class becomes auto-approved only after **N consecutive zero-correction approvals (start N=50)**, per `(action_type, strand)`; **any** correction resets to zero. Widening drops the effective tier ONE notch behind one reversible flag — never raises a tier, never below T0, never for OUTBOUND/paid. Any error reading the evidence store degrades to the stricter static tier.
5. **Handoffs are POINTERS not payloads.** Single-writer orchestrator owns the plan/ledgers; workers return results or escalate, never reframe the global plan. The memory layer is the message bus (SCOUT writes leads, emits `signal(result_pointer=list_id)`; BROCA reads what it needs). One writer + durable substrate = auditability, replay, crash-safety, no concurrent plan corruption.

---

## 5. Decidable termination — exactly one of three states

Exit at the **FIRST** of:

- **SUCCESS** — all criteria PASS. Then exactly ONE bounded elevate pass + a RETRO, then **STOP. Do not keep going for "better."**
- **STUCK** — any cap/budget exhausts, OR an item hits **K+1 deferrals**, OR REFEED hits no-progress/marginal-floor, OR a kill-condition (§ below) trips. → HALT + STUCK report routed to a human, naming the red gates and best-so-far. Never a false "done."
- **BLOCKED-ON-HUMAN** — irreversible action or anchor change pending approval. Durable, resumable pause (state persisted; resumes on answer/cancel/timeout — the wait is ALWAYS bounded, falls back to inbox on timeout so a thread never wedges forever).

**Termination proof:** green count is non-decreasing over a finite criteria set ⇒ the loop is a monotone fill of a finite checklist ⇒ it must terminate or trip a cap. KEEP-BEST: never return a later revision scoring worse than an earlier accepted one. Stationary rubric: the bar never moves mid-run.

---

## 6. State: append-only resumable ledgers (state lives OUT of context)

Four markdown ledgers, append-only, supersede-with-dated-entries, never edit-in-place:

- **GOAL ANCHOR** (immutable, content-hashed).
- **TASK LEDGER** (facts vs flagged load-bearing guesses + plan DAG).
- **PROGRESS LEDGER** — one row per step attempt: `ts | agent | action | tier | external-evidence | verdict | escalation | retries_used | criteria_green_delta | deferral_count | budget_burn`. This row IS the livelock detector and the journal.
- **STUCK REPORT.**

The queue/ledger row IS the crash journal: always **finalize a run terminal in a `finally` backstop** (strand_runner pattern, :1210 timeout finalize) so a crash never leaves a "running" zombie. Next `/loop` tick resumes the exact state. Survives compaction, crash, approval pause.

---

## 7. How it all composes (the stack, one glance)

```
GLOBAL KILL + WALLET ............ autonomy.gate() — the outermost breaker, no model in path
  └ CAMPAIGN ceilings ........... wall-clock T, strands-spawned N, total tokens/$ (the gap we close)
     └ PER-STRAND session caps .. max-turns AND wall-clock per job class; concurrency 2–3
        └ PLAN (≤5-step phases) .. inspectable, vetoable, replan-on-failed-gate
           └ ReAct inner loop ... step-capped + FINGERPRINTED
              └ REFEED gate ..... typed verdict, minimal-delta, Q/T floor
                 └ stage_proposal  every side effect; OUTBOUND never auto
                    └ devil gate . different model scores ≥9.2 before it's even a proposal
```

Four ordered QC gates wrap any outbound artifact (all logged to `automation_ledger`): (1) deterministic pre-gate (tool whitelist, dry-run default, idem-key dedupe, privacy preflight); (2) in-session self-review; (3) **devil gate — a DIFFERENT model scores ≥9.2** before it may become a proposal, one rewrite cycle then escalate, never ship; (4) nightly post-hoc audit cross-checking every action against a store row. Producer and judge never share a brain.

---

## 8. Recurring-run hygiene

Deterministic-first routing (type→node lookup; LLM only on no-rule-hit, on a cheap classifier) keeps the expensive/non-deterministic model OUT of the control path — the agent reasons *inside* a job, not over *which* job runs. Multi-step jobs are code-declared DAGs, not improvised. Auth is the firstParty subscription with API keys stripped from the child env and a fail-fast pre-flight; the runner stays a thin one-swap shim. Anti-thrash debounce: advance `next_run_at` BEFORE firing so a crash mid-fire can't re-trigger the same schedule in a tight loop.

Every phase must **delete a real recurring manual job that phase**, pass the green test gate (`.venv pytest -q`), be independently abandonable, ≤5 files. Measured `strand_usage` numbers beat estimates — this is the kill for the autonomy-theater trap (impressive idle agents that replace no work).

## The autonomous loop (with safety gates)
1. GATE-PRE (gateway, not after): autonomy.gate() — refuse if killed OR wallet exhausted; check step/token/wall-clock/strands-spawned caps. If the NEXT action would exceed any cap, do not take it → HALT(STUCK). This is the one pre-action check every self-directed routine makes.
2. SELECT loop-shape ONCE (ORDO classify-first): execute-until-correct | best-of-N→gate→synthesize | diverge-3-to-5→debate→pick→graft (experimentalist) | draft→critique→rewrite | draft→blind-reread→reconcile | decompose→per-part-REFEED→barrier. Wrong shape = over-spend (best-of-N on easy) or under-verify (rubric-only where an executable oracle exists).
3. PLAN / REPLAN: phases ≤5 steps; decompose ONLY high/irreversible or >3-action steps (demand-driven — everything else stays one line until it FAILS); stake-tag every step ONCE at plan time on cost-if-wrong × reversibility (trivial|normal|high|irreversible), NOT on optimality. Read the immutable goal anchor; never write it.
4. ACT (BATCH-the-tick): read state once, then do a whole phase or ≤5 independent ready steps in parallel. Bias to action on trivial/reversible; reserve alternatives+INSPECTOR for high/irreversible. EVERY action gets fingerprinted: hash (tool, canonical-json(args)), fold the result hash. ALL side effects go through stage_proposal — propose, never execute.
5. OBSERVE: read the real, freshly-returned results (ReAct grounding). This is the ONLY source of truth for VERIFY — never verify against the plan's expectation, verify against the world.
6. VERIFY: stake-calibrated, per-step, grader-is-never-the-doer. Run each criterion's check_cmd → typed verdict {pass, mode∈{wrong_output,missing_structure,parse_error,degenerate,abstained}, observed, expected}. wrong_output is the most valuable signal; 'abstained' is a FIRST-CLASS REWARDED outcome. A batch never passes as a block. After any T2+ change, re-run the FULL checklist as a REGRESSION suite and reject any fix that turns a frozen-green criterion red.
7. ESCALATE-ON-FAIL: climb the ADAPT ladder ONE rung (T0 retry-in-place ~3 → T1 local repair ~2 → T2 phase replan +evidence ~2 → T3 plan amend +evidence → T4 frontier reframe, per-run cap ~2, +evidence+human/budget). Never jump rungs. T2+ fires ONLY on a concrete artifact naming the at-risk criterion; 'feels suboptimal' is inadmissible.
8. WRITE / FREEZE: append one row to the PROGRESS LEDGER (ts|agent|action|tier|evidence|verdict|escalation|retries_used|criteria_green_delta|deferral_count|budget_burn); FREEZE newly-green criteria (never reopened); apply only DOMAIN learnings to the not-yet-frozen frontier (PROCESS learnings → lessons, next run only); yield. Finalize terminal in a finally backstop.
9. TERMINATE-CHECK: exit at the FIRST of SUCCESS (all green → one bounded elevate pass + RETRO → STOP, no 'better') | STUCK (any cap/budget exhausts, K+1 deferrals, no-progress/marginal-floor, or a kill-condition trips → HALT + STUCK report naming red gates + best-so-far) | BLOCKED-ON-HUMAN (irreversible/anchor-change pending → durable resumable pause). Never silently spin. Next /loop tick resumes exact ledger state.

## Kill conditions — DESTROY a wrongful loop on the first true
- NO-PROGRESS (livelock): a sliding window of N ticks turns ZERO criteria green (criteria_green_delta==0 across the window) — busy but not converging. Detect via the PROGRESS LEDGER; HALT(STUCK). ORDO analog: two consecutive REFEED passes with no gate-state change. Progress is green criteria, never steps logged.
- OSCILLATION / THRASHING (the precise detector the step-cap can't be): hash each action as a (toolName, canonical-json(args), resultHash) triple; count repeats in a sliding window. >=3 identical triples ⇒ A-B-A oscillation or identical-retry thrash. Two-tier (OpenClaw): warn/dampen at the lower count, HARD-BLOCK + emit a 'loop' event at the higher count, reason recorded in the run row. Catches the stuck loop in ~3 reps vs waiting for a 25-step ceiling. Special-case write-tools and known polling/idempotent tools so a legit re-read doesn't false-trip. THIS IS THE ONE GUARD WE DO NOT YET OWN — highest-value add; wrap assistant_agentic per-call exec + the strand event stream.
- RUNAWAY (step/turn ceiling): reason-act iterations hit the per-run cap (strand_runner budget_turns, --max-turns; assistant_agentic max_steps). Coarse universal backstop — exits regardless of 'feels done'. Tune from real strand_usage p95, not a round default, so it rarely fires on honest work. On its own it cannot tell big-legit-task from stuck-repeat — pair with fingerprinting.
- WALL-CLOCK / HANG (the only guard that catches a single wedged call that never increments a step counter): time.monotonic() vs a precomputed PER-ATTEMPT deadline (strand_runner :1153) — on breach, SIGKILL the child, finalize 'timeout' (:1210). The per-attempt-vs-whole-process split is deliberate; a global-only deadline lets N retries each eat the full budget. stdin=DEVNULL so a headless agent can't block on input to the deadline. Set the idle/heartbeat ceiling above the slowest legitimate single tool (renders/fetches) or it false-trips them.
- IDLE / STALLED-STREAM (heartbeat ceiling): time-since-last-real-event exceeds an idle ceiling; resets on every meaningful state change (new tool result / new file write), so it tolerates arbitrarily long work AS LONG AS it produces. chat_run_manager :351 reader-idle pattern — lift the same 'reset-on-progress' into the AGENT loop, tracking last MEANINGFUL change, not just any frame.
- BUDGET-EXHAUSTION (cost/spend, fail-closed): cumulative real $ from strand_usage >= armed wallet ⇒ exhausted ⇒ autonomy.gate() refuses all self-directed work. An unreadable spend read counts as +inf = exhausted (fail-closed on money). Only ever stops self-directed work; the human reply path is NEVER gated.
- CAMPAIGN RUNAWAY (the codebase gap to close): 50 well-behaved 5-min strands chain into a 4-hour runaway no per-attempt deadline catches. Extend gate() to ALSO refuse when strands-spawned-this-run > N OR elapsed-since-goal-set > T OR 'no green criteria gained in the last K strands'. Campaign-level loop-count + wall-clock + no-progress, not just the dollar cap.
- DEFERRAL CEILING (anti-livelock): 'push skipped item forward' is capped at K deferrals per item (deferral_count); at K+1 the item BLOCKS and the run goes STUCK rather than infinitely re-queuing.
- RETRY-STORM (circuit breaker): after K consecutive failures of a shared dependency (claude CLI, an external API), OPEN the circuit and fail fast for a cooldown; HALF-OPEN probes one; close on success, re-open longer on failure. Distinct from per-call backoff — stops the WHOLE flow when failures are systemic. Gap: retry.py is stateless (per-site), so add a tiny process-level breaker in front of any shared flaky dependency.
- MANUAL KILL: the founder's one-switch HTTP halt (routes_autonomy) — no model in the path. Immediate, gates every self-directed action via gate().

## Error handling + recovery
- Retry only the transient; let terminal errors through. The taxonomy IS the retry gate. Transient (timeout, connection drop, 429, 5xx, dependency-down) → backoff+retry. Terminal/poison (validation error, 4xx, auth 401, raised ValueError, bad data) → STOP immediately, route to dead-letter / fail the unit / escalate. retry.py catches NOTHING by default (on=()), forcing the caller to enumerate transient types. Pre-classify poison at the gate (mailforge _blocked_reason) so it fails terminally once and never re-drains. Retrying a terminal error burns budget, hides the real bug, and can double-fire a side effect.
- Exponential backoff with FULL jitter, capped. base*2^(attempt-1) capped at a max, then randomize the actual sleep into [0,delay]. Cap stops a long chain sleeping for minutes; full jitter de-synchronizes many clients retrying a recovering service (beats thundering herd; AWS-benchmarked lowest total work/server load). Reuse retry.call_with_retry / @retry at every new flaky call site — do not hand-roll a loop. Default cap 30s; raise for 429 waits. On exhaustion re-raise the last exception.
- Idempotency key + atomic claim = exactly-once side effects (makes retries SAFE). Every side-effecting unit carries a natural-identity idem key (recipient+campaign+step, or daily_review:linus:2026-06-01). A UNIQUE constraint means the first caller wins, every duplicate tick gets None and skips. Before acting, a conditional UPDATE flips queued→sending so two workers racing the same tick can't both fire. claim_run / enqueue / _claim. Any new autonomous action gets an idem key BEFORE doing work; never loop immediate sends.
- Checkpoint / journal for resume-after-crash. Persist progress (completed steps, status, JSON event log) to durable storage after every major action so a crashed run wakes and resumes from the last event instead of restarting (~90% recovery-cost cut: only the failed step re-runs). The queue/ledger row IS the journal (automation_ledger, WAL). ALWAYS finalize a run terminal in a finally backstop (strand_runner append_event/finalize_run, :1210) so a crash never leaves a 'running' zombie. For runs spanning context windows, write progress to a memory file the next session re-reads.
- Partial-failure isolation: one failed step never sinks the run. In a batch/tick, wrap EACH unit at its boundary; record status+error on the failing unit and continue; aggregate a compact per-unit results summary. cadence_runner per-cadence try/except (skip-with-reason), mailforge process_due per-row → _mark_retry_or_fail keep draining. Never let one bad unit raise out of the tick; mark it terminal (skipped/failed) so it doesn't re-fire forever.
- Dead-letter for unrecoverable work. After max_attempts (default 5) or a poison classification, stamp the unit terminal-failed with the last error string kept (mailforge _mark_retry_or_fail, _mark_blocked); never retry forever, never silently drop. The failed row IS the dead-letter record — keep correlation id, last error code, first/last failure ts; expose a list-failed view for weekly triage. Distinguish 'blocked:' (poison, discard) from retry-exhausted (may be reprocessed once the dependency is fixed).
- Fail-open vs fail-closed, chosen PER-FIELD and stated in the docstring. autonomy.py is the template: the GUARD FILE fails OPEN (missing/corrupt .autonomy.json → 'no goal, no wallet, not halted' so a gate check can never crash the runner), but MONEY fails CLOSED (any spend-read error → spent=+inf = exhausted, so a read fault can never read as 'money left'). Availability guards (registry load, knowledge load, logging) fail open; spend/kill/security guards fail closed. Unknown-state degrades safe-FOR-THE-STAKES, never uniformly. cadence_runner: a guard-IMPORT fault degrades open ('gate_unavailable'→allowed) but the wallet/kill STATES stay enforced.
- Kill-switch + budget guardrail = bounded autonomy with clean human handoff. A single global stop flag + a capped wallet gate every self-directed action via gate(); on not-allowed return status 'paused' with reason (killed:<r> / wallet_exhausted) and DO NO WORK. The human-facing reply/answer path is NEVER gated (a paused brain still answers leads — cortex_budget P0/P1 doctrine). The founder re-arms the wallet or flips kill to resume.
- Escalation triggers (watchdog: claim-guard + requeue-once-then-escalate + heartbeat). Durable runs in SQLite (WAL + short txns + atomic-UPDATE claim-guard). A stale/dead-but-claimed run is REQUEUED ONCE, then escalates — never retried forever. Escalate on: gate-blocked twice, budget exceeded, devil score unrecoverable, ambiguous instruction → Telegram + KLADDS notification + run flagged. NSSM keeps the daemon alive across reboots; nothing lives only in RAM.
- Model/provider fallback chain (survive a provider outage). When the LLM call itself is the failing dependency (overloaded, 529, region down), classify as transient-provider → retry primary briefly → on continued failure route to an ordered fallback (secondary model → degraded deterministic path) rather than failing the whole run. Verify model_policy.py actually CHAINS rather than picking once — flagged as a likely gap. Treat 429/529/5xx as transient.
- Rollback / compensation (saga) — PREFER the existing defense over building one. The platform leans on approval-gating + idempotent dry-run-by-default so most flows never half-commit (sends gated; strands write only via stage_proposal). cancel_campaign_queued/cancel_item are the closest 'undo'. A true compensation orchestrator is NOT present and should not be built speculatively. Only if a genuinely irreversible multi-step external flow appears: register a per-step compensation with the orchestrator and fire compensations in reverse on terminal failure (compensation is a new business operation, not a DB rollback).

## Honest limits (residual risk)
"What this framework genuinely guarantees vs. where residual risk lives.\n\nPROVABLE: termination is real — monotone-green over a finite criteria set, plus hard step/wall-clock/token/spend ceilings, means the loop must end or trip a cap. The fail-closed money gate and the propose-only write boundary are structural, not advisory: an unreadable wallet reads as exhausted, and a strand has no direct side-effecting capability by construction. These hold even if the model misbehaves.\n\nTHE ONE REAL GAP IN OURS: we do NOT yet have (tool,args,result) loop-signature fingerprinting. Today assistant_agentic exhausts SILENTLY into a truncated answer with no loop-cause logged, and oscillation/thrash is only caught by the coarse 25-step ceiling — so up to ~24 wasteful identical turns can burn before the cap trips. This is the single highest-value add and the framework's correctness leans on it being built; until then the anti-oscillation guarantee is aspirational, not implemented. Second gap: there is no CAMPAIGN-level wall-clock/strand-count ceiling — 50 well-behaved 5-min strands chain into a 4-hour runaway no per-attempt deadline catches. gate() is the right place to hang it but it isn't there yet.\n\nFINGERPRINTING IS NOT FREE: a legitimately idempotent-and-polling tool (same args, waiting for external state to change) looks identical to a stuck loop. Mature impls must special-case known polling tools or the detector false-trips on honest work. Same tension on every wall-clock/idle ceiling: tuned too tight it guillotines a slow-but-legitimate generation mid-stream; the only honest tuning is real strand_usage p95, and we have thin data (measured max strand duration 4.88 min, n is small).\n\nREFEED IS A TAX, NOT A SAVER: measured 3.3x token cost, net-positive ONLY where a latent bug's downstream cost exceeds it. The Q/T floor keeps it honest but the framework can still spend real money chasing quality on a task that didn't need it if the loop-shape classifier mis-routes — and that classifier is a single cheap LLM call with no ground truth on its own accuracy.\n\nGAPS WE CHOSE NOT TO CLOSE: no state-machine circuit breaker (retry.py is stateless per-site, so N call sites can each hammer a downed dependency simultaneously); no saga/compensation orchestrator (we rely on gate+dry-run+idempotent-claim so nothing half-commits, which sidesteps rather than solves true multi-step irreversible external flows); model/provider fallback in model_policy.py may pick-once rather than chain (unverified). These are lean stand-ins, acceptable until a measured failure rate forces the heavier pattern — but they ARE stand-ins.\n\nRESIDUAL HUMAN-JUDGMENT RISK: the devil-gate ≥9.2 threshold and the N=50 zero-correction widening bar are calibrated by hand, not derived; a mis-set widening counter could auto-approve a class one notch too eagerly (it's still bounded to one reversible notch and never OUTBOUND, so blast radius is capped, but it's a judgment call). And the deepest limit: every gate that depends on the model writing a truthful typed verdict can be defeated by a confidently-wrong model that reports pass on a red criterion — which is exactly why G-exec (executable oracle) is always preferred over G-rubric, and why the grader is never the doer. Where no executable oracle exists, verification degrades to rubric/blind-reread and the guarantee weakens to 'two independent models agreed,' not 'proven correct.'"
