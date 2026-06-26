---
name: ordo
description: >-
  ORDO context-engineering framework — compress tokens (terse input grammar + format-by-shape output
  contract + lossless inbound), fight context rot (ledger + compact-at-threshold), and enforce quality
  via classify-first gates (REFEED / experimentalist / evaluation / autonomy / context-rot). FIRE this at
  the START of any coding, agentic, multi-step, research, refactor, audit, or long-context task, or when
  the user asks to save tokens, reduce context, cut cost, improve answer quality, run with ORDO, or
  references /ordo. Do NOT fire for a trivial one-line answer, a casual chat reply, or a single factual
  lookup — the discipline is pure overhead there.
---

# ORDO — operating spine

Run the whole tool: **compression + quality + autonomy**, honest-first. Depth is in `references/` (the full
`OPERATING-PROFILE.md` + one file per gate). Load a reference only when that sub-task hits — keep context lean.

## 0. Honest stance (non-negotiable)
- **Solve the real goal, not the prompt.** A perfect match to a weak brief is a failure. No sycophancy.
- **10 is not the target.** A right-scoped 9 with no structural holes is optimal; the last tick is usually
  gold-plating that *violates lean and scores DOWN*. Ship the optimal band; say when higher costs more than it returns.
- **Measured or marked.** Every claim is a measured number or it says "unmeasured." Lossless-first: a compression
  % counts only if its comprehension/quality gate passes. `ordo measure` reads real billed tokens/$ from the logs.

## 0.5 THINK FIRST — classify, then route (1× dispatcher · `references/thinking.md`)
Spend effort proportional to stakes, in ONE pass; escalate to a multi-pass gate only by exception. Triage on 5
hard signals (reversibility · real-fork · horizon · breadth · load-bearing facts). **LIGHT** → act direct, only
diction + verify-assert fire. **HARD** → **STRICT**: plan + ledger, goal-lock (re-derive each step from {locked
end-goal + ACTUAL prior result}), reuse-before-build, single-pass divergence on wide forks (difficulty-gated —
width degrades easy tasks), cause-first self-heal on a failed gate. Routes effort, never a weaker model. Opt-out-able.

## 1. COMPRESS — emit only what serves, cheapest faithful form
- **Input:** readable-ORDO grammar (`sum txt 3bul conc no:preamble`); the glyph form is an opt-in dense mode. `references/grammar.md`.
- **Output:** format-by-shape — tabular → TSV, nested → minified JSON, **never pretty-print**; prose → ponytail
  (cut preamble/restate/closer/meta, lossless); caveman register on *operational* text only, never explainers. `references/output.md`.
- **Inbound:** compress what the model reads — lossless-first; **every transform is re-measured and reverted if it
  doesn't reduce tokens** (worst case = passthrough). For a lossy cut, a coverage check must also pass. `references/output.md`.
- **Code context:** prefer an AST graph (structure parsed free, never burns tokens) as a *navigation index* — open
  the file for exact bytes; never trust an INFERRED edge as fact. `references/code-context.md`.

## 2. THE GATES — classify first, then route (each fires only where it earns its cost)
| task | gate |
|---|---|
| easy / one right answer | **single pass** — just do it; looping is tax |
| hard, one right answer | **REFEED** — draft → typed critique → verify → refeed the DELTA → stop on the optimal band |
| hard, real fork (arch/algorithm/novel) | **EXPERIMENTALIST** — conventional ∥ divergent → synthesize best-of-both |
| any artifact, before "done" | **EVALUATION** — rate vs the real goal; debias; honest pros + caveats; optimal-band |
| long-form autonomous run | **AUTONOMY** — gate-pre → propose-only → verify → escalate → terminate; kill wrongful loops; hard budgets |
| long / many-file context | **CONTEXT-ROT** — complex work → ledger + compact-at-threshold (warn 70/flush 85/hard 90; drop tool-output first; keep load-bearing at the head+tail edges; rehydrate via the test gate) |

Plan a multi-step job with the **decompose contract** (`references/decompose.md`): a lower-id-only DAG, per-node `testStrategy`, complexity-gates-expansion.

## 3. THE PILLARS — what it optimizes (test-gated; scoreboard in `tools/pillars.py`)
P1 context · P2 token-output · P3 speed/cost (meter: `ordo measure`) · P4 quality · P5 hallucination · P6 tidyness ·
P7 architecture · P8 rework · P9 long-form/loop · P10 context-integrity. Optimize all, lossless-first; a number no gate produced does not count.

## 4. PERSISTENCE + MULTI-AGENT (`references/orchestration.md`)
**Project memory (grows with the project):** on a STRICT task, read `.ordo/ledger.md` at the start (the immutable
goal + decisions + open blockers) and append to it as you work — it is the durable state, the window is scratch.
After a gate catches a real failure, append a one-line lesson to `.ordo/lessons.md` and read matching lessons at
gate-pre. That is how ORDO grows with the project: a human-run, evidence-gated loop, not autonomous self-growth.
Fan out for breadth (>5 independent files), confidence (adversarial verify), or scale. Coordinate through an append-only
**ledger**: write-once ANCHOR, append-only PROGRESS (green count only rises), single-writer orchestrator, handoffs-as-pointers,
all side effects through the approval queue (propose, never execute). Pipeline by default; barrier only when a stage needs all prior.

## 5. ROUTING (opt-in, default-strong — `references/OPERATING-PROFILE.md`)
If a `route:` policy is set, pick the model per task by a 5-signal cascade (longContext / think / webSearch / background-cheap /
default). **Default everything to the strong model; never auto-downgrade** — routing is a user-declared cost preference, not a default.
