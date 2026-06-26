# ORDO context-rot gate — complexity-adaptive compaction + ledger

> Context degrades NON-UNIFORMLY as it grows, well before the window fills (a 200K model rots at ~50K;
> middle context can score below no-context; effective length is ~50-65% of advertised). The fix is not
> a bigger window, it is keeping the WORKING context small and the state in a LEDGER. Complexity-adaptive:
> complex work gets the ledger + compact-at-threshold track; simple work runs the standard protocol.
> Grounded in Chroma Context Rot (2025), Lost-in-the-Middle (2023), RULER (2024), NoLiMa (2025).

# ORDO context-integrity gate — the complexity-adaptive anti-rot contract

> The gate that keeps a long run accurate, not just terminating. Performance degrades as input
> grows — non-uniformly, and **long before the window fills** (Chroma Context Rot: measurable drop at
> ~50K of a 200K window; LongMemEval ~30–60% gap focused-vs-full; NoLiMa: 10/12 models score
> half-or-less of base at 32K). The autonomy gate proves a run *ends*; this gate keeps the run *correct
> over its length*. It composes AFTER REFEED + experimentalist + autonomy, and it is **adaptive on
> purpose**: compaction itself loses "subtle but critical context whose importance only becomes
> apparent later," so it is pure tax on a short task and only earns its keep on a long one.

## 0 · One law

> **Nothing load-bearing lives only in the window.** The window is a scratchpad that rots; the LEDGER
> is the source of truth. On the LEDGER track, every fact whose loss would cause a wrong next action is
> written to the ledger BEFORE the compaction event that would drop it — so the post-compaction agent
> rehydrates fidelity by *reading the file*, never by *trusting summary recall*. This is the structural
> difference from naive context-stuffing (let it grow, hope) and from blind truncation (drop whatever
> scrolled off, including the fact that became load-bearing later).

Two philosophies, and we run both by classifier: **prevention** (bound the context structurally — the
LEDGER track) vs **cure** (let it grow, compress on demand — the STANDARD track's fallback). A short
task gets cure-only-if-it-runs-long; a heavy task gets prevention from tick 0.

---

## 1 · The complexity classifier — which track (scored at intake, RE-checked every tick)

Route to the **LEDGER+compaction track** if **ANY** trigger fires; otherwise **STANDARD track** (normal
protocol, no ledger file, no compaction machinery). Re-score each tick because a STANDARD task that runs
long crosses into LEDGER territory mid-flight (the band trigger catches it).

| Trigger | LEDGER track if… | Why (grounded) |
|---|---|---|
| **Horizon** | >~15–20 tool calls expected, OR multi-phase | tool outputs are 70–80% of budget; they accumulate past the rot threshold fast |
| **Breadth** | >5 files OR >1 repo/lane | already the fan-out gate; breadth = distractor density = Context-Rot's measured compounding driver |
| **Load-bearing facts** | IDs, contracts, schema/migration state, decisions, ledger lane IDs that must survive a long horizon | these are exactly what truncation silently drops and what only becomes load-bearing later |
| **Irreversibility** | money / sends / migrations where a dropped fact → wrong action | the cost of a bad summary is unbounded here; a forgotten constraint fires a real side effect |
| **Projected fill** | total tokens projected >~50% of window | conservative-by-design (not a measured optimum); rot is observable from the ~25–40% fill band |

**STANDARD track** (Q&A, single-file edit, lookup, short refactor): normal protocol, **no ledger, no
compaction overhead.** It carries exactly one fallback — if it unexpectedly runs long and trips the
projected-fill or horizon trigger mid-run, it is **promoted** to the LEDGER track at that tick (write the
anchor + green criteria to a fresh ledger first, then proceed). Promotion is one-way within a run.

Do NOT put a single-fact task on the LEDGER track. Compaction loses subtle context and the ledger is
write-overhead; on a short task that is all cost, no payoff.

---

## 2 · The compaction policy (LEDGER track only) — staged band + degradation signal

Two independent triggers. **Either** fires compaction. The band is **harness-tunable, not a universal
constant** (public Claude Code references cite 70/85/90 and historically 83.5/95 — version-dependent;
the *principle* is stable: compact BEFORE the model is starved, with warnings that externalize first).

**(a) Token band — high-water-mark, not a single cliff** (against the working budget, ~200K for Opus/Sonnet-4-class):
- **~70% WARN** → pre-write the ledger to current state; offload any pending heavy read to a sub-agent so it never enters the main window.
- **~85% FLUSH + CHECKPOINT** → run the DROP pre-pass (§3); force a ledger checkpoint so the record is never behind live state.
- **~90% HARD-COMPACT** → summarize older history into a fresh window per the KEEP/DROP rules; carry the ledger pointer forward; **rehydrate (§4) before resuming.**

The 95%-style auto-trigger fires *too late to even have room to summarize* — that is why the band warns at
70 and checkpoints at 85, never waiting for the cliff.

**(b) Degradation signal — compact on rot RISK even under the token threshold.** Performance falls before
the window is full, so token count alone is the wrong sole trigger. Treat as a degradation event and
compact when the live context is large AND any of:
- **Distractor density** — dense with near-duplicate / competing tool outputs (1 distractor measurably
  hurts; 4 compound — Chroma). Compaction here removes *distractors, not signal*, because the
  load-bearing facts already live in the low-distractor ledger.
- **Self-contradiction / re-derivation** — the agent re-reads a file it already read, re-derives a known
  fact, or contradicts an earlier recorded decision. That is rot surfacing behaviorally.
- **Middle-bloat** — load-bearing content has been pushed into the under-attended middle (lost-in-the-
  middle U-curve: ~20+pp swing from position alone). Compaction re-seats the anchor + green criteria at
  the high-attention head, the live working set at the tail.

**How compaction runs (the pass order):** re-summarize older history into the ledger (the durable record),
DROP per §3 priority, then KEEP per §3 at the edges. The ledger is what makes this *safe to be lossy*:
the summary is a recall aid, not ground truth — §4's gate run is the only non-lossy verification.

**Prevention beats cure — defer the trigger.** Before compacting the main thread, offload bounded
research/exploration to **sub-agents** (existing fan-out: >5 files → 5–8 per agent). Each burns its own
window and returns a ~1,000–2,000-token distilled summary; the heavy trace never enters the orchestrator
window. This keeps the main context low-distractor (directly fights the Context-Rot distractor effect) and
pushes the compaction trigger out. The main thread keeps the ledger; sub-agents keep nothing durable.

---

## 3 · KEEP / DROP rules — the keep-set is exactly "loss → wrong next action"

**KEEP (carried into the fresh window, placed at the HIGH-ATTENTION EDGES — head and tail, never the
middle):**
1. **The immutable ANCHOR** — original task + clarifications, the definition-of-done (content-hashed, the §0-of-autonomy goal anchor). Placed at the head every tick; the U-curve's primacy slot is reserved for the objective so it can never rot into drift.
2. **The decidable GREEN CRITERIA** — the acceptance set + which are frozen-green. This *is* progress; steps logged are not.
3. **Load-bearing facts** — key decisions + rationale, open bugs / blockers + how prior ones resolved, IDs / contracts / paths / lane IDs, files modified + current state.
4. **The recent working set at full fidelity** — the ~5 most-recently-accessed files verbatim + the recent message window (~20K tokens). Summarize everything *behind* this; keep the live edge sharp.

**DROP (in strict priority order — reclaim the biggest, safest first):**
1. **Tool-output pre-pass FIRST** — file contents + command/search outputs are 70–80% of the budget; summarize or evict them as a dedicated pass *before* touching any conversation prose. Largest single reclaim, lowest risk (the durable copy is on disk / behind a pointer).
2. **Resolved subtasks** — once a phase/item passes its check, collapse its detailed trace to a one-line outcome; the ledger holds the durable record.
3. **Stale older turns** beyond the recent-keep window.
4. **Superseded drafts + redundant/duplicate messages + intermediate reasoning** already captured as a decision.

The keep-set is the minimal set whose loss flips the next action wrong. Everything else is a recall aid the
ledger already holds — so dropping it is reversible (re-read the file / the pointer), and the §4 gate
catches anything the drop got wrong.

---

## 4 · Restore protocol — rehydrate, don't trust the summary

After ANY compaction (or a fresh session/strand on the same task), the agent does **NOT** treat the summary
as ground truth. It rehydrates, in order:
1. Read **git log** (what actually landed) + the **PROGRESS / TASK ledger** (recorded facts) + the **anchor / acceptance checklist** (the definition-of-done).
2. Re-read the **~5 recent files** live (working-set fidelity the summary can't carry).
3. **Run the test / acceptance gate** — the only non-lossy verification. It catches undocumented drift the notes missed and the known failure mode that "compaction doesn't always pass perfectly clear instructions to the next agent."

Ledger restores *recorded* facts; the live re-read restores *working-set* fidelity; the gate run validates
*both*. Only then resume. This is also why the LEDGER write-discipline is "update at every phase boundary
AND at the 70%/85% warnings, not only at compaction time" — so the record is never behind live state when a
crash or compaction hits.

---

## 5 · How it composes with what we already own (do NOT rebuild)

This gate is ~80% wiring of existing ORDO parts; the only genuinely new piece is the **adaptive classifier
+ the degradation-signal trigger.**

- **ADAPT / autonomy ledgers (`autonomy.md` §6)** — the LEDGER track **IS** the existing append-only GOAL-ANCHOR / TASK / PROGRESS / STUCK ledgers. We add no new ledger; we add the *write-discipline timing* (write at the 70/85 warnings) and the *rehydrate-after-compaction* step. The content-hashed anchor read-every-tick already kills goal drift across compaction — §3-KEEP rule 1 just re-seats it at the high-attention head.
- **Autonomy "state lives OUT of context" + "batch-the-tick"** — already the structural defense. This gate makes compaction *safe* precisely because that invariant already holds: re-read state only after a crash **or compaction** (compaction is now an explicit re-read trigger, which it already named).
- **Orchestration handoffs-as-pointers + single-writer** — the answer to "don't re-serialize a 10K payload through chat." Compaction's tool-output DROP pre-pass and the sub-agent offload are the same lever: keep payloads behind a `result_pointer`, carry the pointer not the bytes.
- **REFEED minimal-delta (`autonomy.md` §3 / `framework.md`)** — the same rule applied to history: refeed the delta, not the transcript. Compaction is the *coarse* version (whole-history → summary); REFEED is the *fine* version (failing-gate → minimal delta). Same discipline, two scales; do not double-compress.
- **Headroom inbound compression (`harness/inbound.py`, P1)** — the per-read lever beneath compaction. Headroom shrinks what a single read costs (lossless TSV when the model must ANALYZE; lossy sampling + CCR retrieval only when it needs SHAPE); compaction shrinks accumulated history. They stack across different token pools, never on the same content. The **don't-send-it / JIT** lever is the strongest: a dropped tool output becomes a 1-line index + retrieval handle, so DROP rule 1 is reversible by construction.
- **Relevance-gated inclusion + lost-in-the-middle ordering (`harness/inbound.py` + `spec/output.md`, our docs)** — the placement half of KEEP: order by relevance, lead with the answer-bearing content, trim the middle. This is the one compression that *improves* quality (removes the distractors the U-curve punishes). Already specified; this gate just invokes it at the compaction edge.
- **Pillars model (`pillars.md`)** — adds **P10** below, test-gated like the other nine; no number advances on opinion.

The net: STANDARD track runs the framework unchanged. LEDGER track is the existing autonomy spine + the
existing inbound/orchestration levers, sequenced by a classifier and tripped by a band + a rot signal.

---

## 6 · The pillar — P10 context-integrity (rot-resistance)

| # | pillar | metric | gate (how it's measured) | baseline | lever |
|---|---|---|---|---|---|
| **P10** | **Context integrity** (rot-resistance) | **accuracy retention ratio** = (acc on a long, rot-baited run with the gate) ÷ (acc on the same task short-context) — held across length, vs naive context-stuffing as the control | a length-scaled multi-needle + distractor task (NoLiMa-style low-similarity needle, ≥1 distractor, answer planted mid-context) run at the short baseline AND at the long/full length, **gate-on vs naive-stuff control**; PASS = retention stays ≥ a set floor (target ≥85% of short-context base, the NoLiMa effective-length bar) where the naive control collapses | **UNMEASURED** (build the harness) | LEDGER externalization + staged compaction + edge-placement + degradation-trigger + sub-agent isolation |

**Why this metric, not raw NIAH:** vanilla single-needle NIAH is near-saturated and *overstates* long-context ability (RULER, NoLiMa) — passing it proves nothing. P10's gate deliberately uses the *hard* setup that breaks models: low query-needle similarity (forces associative reasoning, not string-match), distractors present (the measured compounding driver), answer mid-context (the U-curve trap). The number that counts is **retention vs a naive-stuffing control on the same task** — does the gate hold accuracy where stuffing rots? Single-needle pass = inadmissible, same as "feels suboptimal" is inadmissible to the autonomy ladder.

**Family note for calibration:** Claude is the most conservative family (highest abstention, lowest hallucination — Opus 4 refused 2.89% on the repeated-words task vs GPT confidently-wrong). P10 should reward abstention-under-uncertainty exactly as the autonomy VERIFY step rewards `abstained` — a model that says "I dropped that, let me re-read the ledger" is passing, not failing.

---

## 7 · The stack, one glance (where this gate sits)

```
COMPLEXITY CLASSIFIER ............ scored at intake, re-scored every tick → STANDARD | LEDGER track
  STANDARD track ................. normal protocol, NO ledger/compaction (promote if it runs long)
  LEDGER track:
    └ ANCHOR (content-hashed, read every tick) ...... §0-autonomy, re-seated at high-attention HEAD
       └ append-only LEDGER (state OUT of context) .. autonomy §6, written at 70/85 warnings
          └ sub-agent isolation (prevention) ........ heavy reads never enter main window
             └ COMPACTION (cure): band 70/85/90 + degradation signal
                └ DROP pre-pass (tool-output 70–80% first) → KEEP at edges (anchor+green+recent)
                   └ REHYDRATE (git+ledger+re-read 5 files+RUN THE GATE) — never trust the summary
                      └ Headroom inbound + relevance-gate + JIT ... per-read lever beneath it all
```

Composes after REFEED + experimentalist + autonomy. P10 measures the whole stack's rot-resistance.

## Complexity classifier (which track)
- Two-track gate scored at task intake AND re-checked every tick. Route to the LEDGER+compaction track if ANY trigger fires; else STANDARD track (no ledger, no compaction overhead).
- Trigger 1 HORIZON: work projected >~15-20 tool calls OR spans multiple phases (tool outputs hit 70-80% of budget fast).
- Trigger 2 BREADTH: touches >5 files OR >1 repo/lane (breadth = distractor density = Context-Rot's measured compounding driver; same as the fan-out gate).
- Trigger 3 LOAD-BEARING FACTS: IDs, contracts, schema/migration state, decisions, lane IDs that must survive a long horizon (exactly what truncation silently drops).
- Trigger 4 IRREVERSIBILITY: money / sends / migrations where a dropped fact causes a wrong action (cost of a bad summary is unbounded here).
- Trigger 5 PROJECTED FILL: total tokens projected >~50% of window (conservative-by-design, NOT a measured optimum; rot is observable from the ~25-40% fill band).
- STANDARD track = Q&A, single-file edit, lookup, short refactor: normal protocol, NO ledger file, NO compaction machinery — compaction loses subtle-but-critical context, so it is pure tax on short work.
- One-way mid-run PROMOTION: a STANDARD task that unexpectedly trips the horizon/projected-fill trigger is promoted to LEDGER track at that tick (write anchor + green criteria to a fresh ledger first, then proceed).
- Never put a single-fact lookup on the LEDGER track — the externalization + compaction overhead is all cost, no payoff.

## Compaction policy (the trigger + how it runs)
- LEDGER track only. Two independent triggers — EITHER fires compaction. Band is harness-tunable (public refs cite 70/85/90 and historically 83.5/95), the PRINCIPLE is fixed: compact BEFORE the model is starved, warn early so externalization happens first.
- TRIGGER A — token band (high-water-mark, not a single cliff, against ~200K working budget): ~70% WARN -> pre-write ledger + offload pending heavy reads to a sub-agent; ~85% FLUSH+CHECKPOINT -> run the DROP pre-pass + force a ledger checkpoint; ~90% HARD-COMPACT -> summarize older history into a fresh window, carry the ledger pointer, then rehydrate. The 95%-style auto-trigger fires too late to even have room to summarize — that is why we warn at 70.
- TRIGGER B — degradation signal (compact on rot RISK even UNDER the token threshold, because performance falls before the window fills): fire when context is large AND (distractor density: near-duplicate/competing tool outputs — 1 hurts, 4 compound) OR (self-contradiction / re-reading a file already read / re-deriving a known fact) OR (load-bearing content pushed into the under-attended middle).
- HOW compaction runs (pass order): re-summarize older history INTO the ledger (the durable record) -> DROP per priority -> KEEP at the high-attention edges. Lossy is SAFE only because the ledger holds ground truth and the rehydrate gate (run the tests) is the non-lossy backstop.
- PREVENTION before cure: before compacting, offload bounded research/exploration to sub-agents (existing fan-out, 5-8 files each). Each returns a ~1-2K-token distilled summary; the heavy trace never enters the main window. Keeps the orchestrator low-distractor and defers the trigger.
- REHYDRATE after every compaction: read git log + ledger + acceptance checklist, re-read the ~5 recent files live, then RUN THE GATE. Never trust the summary as ground truth — the gate is the only non-lossy verification.
- Write-discipline: update the ledger at every phase boundary AND at the 70%/85% warnings, NOT only at compaction time, so the durable record is never behind live state when a crash or compaction hits.

## Keep / drop rules
- KEEP rule = the minimal set whose loss flips the next action wrong. Everything kept is placed at the HIGH-ATTENTION EDGES (head and tail), never the under-attended middle (lost-in-the-middle ~20+pp swing from position alone).
- KEEP 1: the immutable content-hashed ANCHOR (task + clarifications = definition-of-done), re-seated at the HEAD every tick so the objective can never rot into drift.
- KEEP 2: the decidable GREEN CRITERIA (acceptance set + which are frozen-green) — progress is green criteria, not steps logged.
- KEEP 3: load-bearing facts — key decisions+rationale, open bugs/blockers + how prior ones resolved, IDs/contracts/paths/lane IDs, files modified + current state.
- KEEP 4: the recent working set at FULL fidelity — the ~5 most-recently-accessed files verbatim + the recent message window (~20K tokens). Summarize everything BEHIND this; keep the live edge sharp.
- DROP 1 (FIRST, biggest+safest reclaim): tool-output pre-pass — file contents + command/search outputs are 70-80% of budget; evict/summarize them as a dedicated pass BEFORE touching any conversation prose. Reversible: the durable copy is on disk / behind a result_pointer.
- DROP 2: resolved subtasks — once a phase/item passes its check, collapse its detailed trace to a one-line outcome (the ledger holds the durable record).
- DROP 3: stale older turns beyond the recent-keep window.
- DROP 4: superseded drafts + redundant/duplicate messages + intermediate reasoning already captured as a recorded decision.
- Dropping is reversible by construction (re-read the file / the pointer / the ledger) and the rehydrate-gate catches anything the drop got wrong — which is what licenses lossy compaction.

## P10 context-integrity (the pillar metric)
P10 context-integrity (rot-resistance). METRIC: accuracy retention ratio = (accuracy on a long, rot-baited run WITH the gate) / (accuracy on the same task at short-context baseline), measured across length and compared against NAIVE CONTEXT-STUFFING as the control. GATE: a length-scaled multi-needle + distractor task run at both the short baseline and the long/full length, gate-on vs naive-stuff. The setup is deliberately the HARD one that actually breaks models — NoLiMa-style low query-needle similarity (forces associative reasoning, not string-match), >=1 distractor present (the measured compounding driver), answer planted mid-context (the U-curve trap) — because vanilla single-needle NIAH is near-saturated and OVERSTATES long-context ability (RULER/NoLiMa), so passing it is inadmissible evidence. PASS = retention stays >= floor (target >=85% of short-context base, the NoLiMa effective-length bar) at a length where the naive-stuffing control collapses. Reward abstention-under-uncertainty exactly as autonomy VERIFY rewards 'abstained' (Claude is the most conservative family: Opus 4 refused 2.89% vs GPT confidently-wrong). Baseline UNMEASURED — the harness is the build item; no number advances on opinion (pillars rule).

## Honest limits
WHAT COMPACTION CANNOT RECOVER: anything that was load-bearing but NEVER written to the ledger before the compaction event that dropped it is gone — irreversibly. Compaction is lossy by definition; the ledger only preserves what the agent had the foresight to externalize. The known failure mode is real: 'compaction doesn't always pass perfectly clear instructions to the next agent,' and a fact's importance often 'only becomes apparent later' — after it has already scrolled off. The rehydrate gate (re-read git+ledger+files, run the tests) is the ONLY non-lossy backstop, and it only catches drift that the test suite can detect; an undocumented decision with no failing test passes silently wrong.

COST OF A BAD SUMMARY: the summary is carried forward AS the agent's working memory. A summary that mis-states a decision, inverts a constraint, or quietly omits a blocker propagates that error into every subsequent tick with full confidence — and on the irreversibility trigger (money/sends/migrations) that confident-wrong summary can FIRE a real side effect before the gate catches it. This is why the approval queue (propose-never-execute) sits underneath: compaction can corrupt the plan, but it cannot directly fire an OUTBOUND action. The blast radius is capped by the write boundary, not by compaction being correct.

LOSSY RISK + AGGREGATE LOSS: the tool-output DROP pre-pass (the 70-80% reclaim) is lossy sampling — 'what do these lines look like?' survives, 'how many status-500 errors / max latency?' does NOT unless the model retrieves the original via the pointer. If the agent compacts away a tool output and then needs an AGGREGATE over it, it must re-fetch or it answers wrong. Same tension as Headroom's 92%: gist-preserving, aggregate-lossy.

THE CLASSIFIER IS A JUDGMENT CALL, NOT A PROOF: the ~50% projected-fill threshold and the band (70/85/90) are conservative DESIGN choices, not measured optima — tuned too tight, compaction guillotines a run that had headroom and pays the bad-summary tax needlessly; too loose, the model rots before the trigger fires. The degradation signal (re-reads, contradictions, distractor density) is heuristic — it can false-trigger on a legitimately repetitive task (real polling, intentional re-reads) and miss silent rot that produces confident-wrong output with no behavioral tell. There is no ground truth on the classifier's own accuracy short of the P10 harness, which is UNMEASURED until built.

DEEPEST LIMIT (shared with the whole stack): every gate that depends on the model writing a truthful typed verdict can be defeated by a confidently-wrong model reporting 'pass' on a red criterion or 'I have it' on a fact it actually dropped. That is precisely why P10's gate uses an EXECUTABLE retention test (G-exec), not the model's self-report, and why rehydrate ends in a real test run — where no executable oracle exists, rot-resistance degrades to 'the summary looked complete,' which is exactly the failure mode the studies measured. Until the P10 harness exists, the rot-resistance guarantee is aspirational, not proven.
