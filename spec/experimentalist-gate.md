# ORDO experimentalist gate — dual-perspective synthesis for hard tasks

A second mode of the REFEED loop, for the tasks where the *best-known method* may not be the *best
method*. It runs two perspectives in parallel — the **gated-conventional** arm (rigorous, English-gated,
the REFEED verify loop) and the **experimentalist** arm (genuinely unconventional, challenge-the-status-
quo) — then **synthesizes the best of both into one answer and acts on it.** Repurposed from the house
`experimentalist` divergence skill, generalized from creative work to all coding, and **gated** so it
fires only where it earns its cost. This is a QUALITY lever (P4/P9), never a compression one.

## The gate — WHEN it fires (the integral decision)
The classifier (REFEED step 1) routes the task:
- **Dual-perspective (run both arms)** when the task is HARD/ADVANCED and the conventional approach is
  not obviously right: a real fork (architecture, data model, algorithm choice), a novel problem with
  no settled answer, something "we cannot take shortcuts with," or where the obvious solution smells
  generic/AI-default. These are the cases where a different *principle* can beat the best execution of
  the default.
- **Single-perspective (REFEED-only or single pass)** when the task is deterministic and has one right
  answer: a bug with one root cause, a spec'd API contract, a mechanical edit, anything trivial.
  **Divergence here is theatre — the gate says skip it and proceed straight.** Enforcing the
  experimentalist everywhere is the failure mode; the gate exists to prevent exactly that.

## The integral steps (when the gate opens)
1. **WIN-CONDITION** — one line: what "best" actually means here + the hard constraints. Both arms are
   scored against this, so it must be honest and specific.
2. **ARM A · GATED-CONVENTIONAL** — the REFEED loop produces the rigorous best-known-method answer:
   draft → typed critique → verify against an executable/rubric gate → rewrite the delta. This is the
   "do it by the book, perfectly" perspective.
3. **ARM B · EXPERIMENTALIST** — generate up to 5 genuinely DISTINCT approaches (distinct = a different
   *principle*, not different paint), forcing range with the coding divergence methods:
   - **Invert the obvious** — do the opposite of the default approach.
   - **Change the paradigm/medium** — imperative↔functional, OOP↔data-oriented, sync↔event-driven,
     compute↔lookup, runtime↔compile-time.
   - **Steal from a far field** — borrow a mechanism from databases, distributed systems, compilers,
     games, biology, control theory.
   - **Remove the "required" element** — drop the assumed-mandatory piece (the framework, the ORM, the
     class, the mutable state, the allocation) and make it work without.
   - **Exaggerate one trait to 11** — push simplicity / performance / correctness / laziness to the
     extreme; everything else serves it.
   - **Constraint roulette** — impose an arbitrary hard limit (stdlib-only, one function, zero-alloc,
     immutable, no dependency) and solve to it.
   - **Change the POV** — solve as a different engineer would: a perf-obsessed systems dev, a
     formal-methods correctness zealot, a lazy senior (ponytail), a security auditor.
   Then **adversarially score** each (serves the win-condition? failure mode? buildable in scope? beats
   the default and on which axis?), kill the "different but worse," pick the single best principle.
4. **SYNTHESIZE — best of both** — put Arm A and Arm B's winner side by side against the win-condition.
   Take the higher goal-service as the spine; **graft the one strongest move from the loser** if it
   sharpens the winner; produce ONE coherent final answer that reads intentional, not a committee
   compromise. **Be honest:** often the gated-conventional arm wins (the default is the default for a
   reason) — when it does, ship it and say why the experiment lost.
5. **ACT** on the synthesized best perspective.

## Guardrails (carried from the house skill)
- Divergence must be **applicable, not random** — every option buildable and serving the goal.
- **"Different" is the bar; "intentional" is the gate.** Chaos that feels planned, never chaos for its
  own sake.
- **Cap at 5** (three strong beats five weak). The experimentalist winner must **beat the gated arm on
  the stated win-condition** or you keep the gated answer and state why.
- **Cost is real.** Two arms + synthesis cost more tokens/passes than one — which is exactly why the
  gate is selective (hard/advanced/fork only). Whether the dual-perspective actually beats REFEED-alone
  on hard tasks is **test-gated**, not assumed (see `BUILD-LOG.md`).

## Measured (test-gate: conventional-only vs synthesized, 4 hard fork tasks)
Blind judge: **synthesis(conv+experimentalist) beat conventional-alone on 3 of 4** (rate-limiter,
full-text-search, undo/redo), **tied on 1** (dedup), and the tie **failed safe** (the divergent idea was
unsafe and got culled, not shipped). The wins were substantive, not cosmetic: on the rate limiter the
experimentalist caught the conventional arm *quietly reframing the win-condition* to justify a
per-request network hop that structurally loses a p99 contest (a single pass ships that unchallenged);
on undo/redo it grafted a CRDT counter-toggle that makes "correct under conflict" free instead of
proof-bound. **The gate's value is dual: the grafts AND the disciplined adversarial CULLING** (rejecting
its own different-but-worse ideas against the literal win-condition) — which is what keeps it from
shipping novelty for its own sake. **Verdict: earns its 2-arm cost on hard, wide-solution-space forks;
the chief risk it guards is the conventional answer bending the spec to habit.** Cost is why the gate
stays selective (the classifier), never default.

## Relation to the framework
This is REFEED's "diverge-debate-graft" loop-shape, promoted to a first-class gated mode. The classifier
chooses: single pass (easy) → REFEED-only (hard, one right answer) → dual-perspective (hard, real fork).
Same DONE-contract, format-by-shape, and honest-stop discipline as the rest of the framework.
