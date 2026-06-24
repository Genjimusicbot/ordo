# ADAPT anchor — ORDO to done (frozen acceptance spec)

> Write-once. The loop reads this every tick and never edits it. Kickoff sign-off: GRANTED in advance
> by the user ("no preferences, go with the best for each step, audit tomorrow, do NOT stop to ask").

## Goal
Take ORDO from "a measured language (P0-P4)" to a **decidable, audit-ready done** that proves it is
worthwhile on the user's real terms: not just token density, but **quality, hallucination, precision,
and speed**, with a working **harness**, the **deanchor** reframe tested, and a **semantic-density
(intent-as-symbol)** layer. Floor: **≥10% combined token save on a realistic task mix**, plus evidence
of more-than-tokens gains. Honest about where ORDO does NOT help (the cut list).

## Acceptance criteria (DONE := all PASS; each is machine/evidence-checkable)
- **C1 · Research digested.** `docs/research-synthesis.md` exists, drawing on all 20 xenolinguistics
  docs, listing ≥8 distinct mechanisms BEYOND token-density (quality / hallucination / speed /
  capability), each with source + concrete ORDO application + how it was/will be tested.
- **C2 · Deanchor experiment.** Measured head-to-head: exotic-glyph vs terse-readable ORDO encodings
  on BOTH token cost AND blind decode accuracy, on the 20-prompt benchmark. Verdict recorded in
  BUILD-LOG with the chosen direction. PASS = the experiment ran and a direction is chosen on evidence.
- **C3 · ≥10% combined floor.** A realistic end-to-end task mix (input prompt + produced output)
  measured English-vs-ORDO; combined reduction **≥10%**, documented with the number. (Stretch, not
  gating: the output layer alone already clears this; C3 requires the *measured* end-to-end figure.)
- **C4 · Quality axis.** A blind multi-agent test: same N tasks done from a verbose-English prompt vs
  the ORDO prompt; an independent judge scores OUTPUT quality/on-target/completeness. PASS = ORDO
  output quality ≥ English (within noise), measured, recorded. (If it LOSES, that is a finding to
  record + a fix attempt, not a silent pass.)
- **C5 · Hallucination / epistemic.** A factual-task test of whether ORDO's epistemic markers
  (信/源/?/确) reduce confident-wrong answers vs an unmarked prompt; measured rate, recorded.
- **C6 · Speed.** Output-token delta quantified into a wall-clock proxy (fewer output tokens → faster);
  documented with the measured per-task token saving on output.
- **C7 · Intent-as-symbol layer.** A measured set of high-frequency WHOLE-INTENT macros → single glyph
  (e.g. "explain your reasoning step by step", "what are the trade-offs", "give me only the code"),
  tokenizer-validated AND blind decode-tested ≥ the grammar's bar (~1.7/2 fidelity).
- **C8 · The harness.** A runnable Python runtime in `harness/` that takes an ORDO string + ORDO.md
  and produces the expanded English prompt (auto-decode) and/or enforces the output contract, with a
  passing self-test (`pytest`/`__main__` demo green, shown).
- **C9 · Committed + honest verdict.** Every phase committed locally to the ordo git (NOT pushed) with
  a BUILD-LOG entry; a final `VERDICT.md` summarizes every measured number, what ORDO helps, and the
  explicit CUT LIST (where it is not worth it). Repo tooling self-tests green; `git status` clean.

## Out of exit test (backlog, not gating)
Maximal compression beyond what's measured; multi-model re-validation beyond the workflow model;
training a custom tokenizer; UI/visualizers; pushing to GitHub.

## Budgets
Overnight autonomous, ultracode (token cost not a constraint). Per phase: ≤ a few parallel workflows.
Run cap: loop until all C1-C9 PASS, or HALT with a STUCK report naming the blocked criterion + the one
human question. No side effects outside the ordo repo + this ledger. No push.

## Frozen-progress rule
A PASSED criterion is frozen; later work that breaks it is rejected. Green count only rises.

content-hash: (computed on commit)
