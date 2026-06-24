# ORDO REFEED — the Fable-style multi-pass refeeding framework

> Synthesized from one GLOSSOPETRAE analysis per pillar (honest verdicts) + long-form/loop methods + Fable
> operating principles. The loop that turns ORDO's grammar + output contract into Fable-class quality
> per token, by refeeding through typed verification instead of brute force. Ships as a spec the model
> (or the harness) follows.

# REFEED — ORDO's Multi-Pass Refeeding Framework

> A Fable-style quality loop. It refeeds an output through critique + verification until it clears an explicit, evidence-gated bar — then **stops**. The gain is *more quality per token via structure and loops*, not brute force. It is built ON TOP of ORDO's grammar (the command form) and ORDO's OUTPUT contract (the response form), and it is honest about where each of the 9 pillars actually moves the needle.

## 0 · What this is (and what it is not)

REFEED is the synthesis layer above ORDO. ORDO gives you a *cheap, one-parse command* (readable-ORDO grammar, ~32% input tokens) and a *cheap, faithful response* (format-by-shape + ponytail, the ~55-77% output lever, 64% end-to-end). REFEED adds the missing axis: a **loop** that takes a first draft and drives it to Fable-class quality by refeeding it through critique and verification a bounded number of times.

The whole bet rests on one measured fact from the ORDO build: **the value was never the opaque surface — it was the grammar structure + the output contract** (VERDICT.md, finding 1 + 2; C2/C4 PASS). REFEED inherits that bet. It never asks the model to think in glyph-soup. It asks the model to *commit to an explicit contract, then check itself against that contract, repeatedly, against the cheapest real signal available* — and it spends extra passes only where a measured gate says they buy quality.

It is NOT: best-of-N brute force as a default, an LLM-judge rubber stamp, or a license to pay 5x tokens for 3% gain. Every loop is a *bet that the next pass earns its tokens*, and the STOP rule is what makes it a framework instead of a token furnace.

## 1 · The unit of work: an ORDO command with a contract

A REFEED job is an ORDO command plus a **DONE contract** — the explicit success criteria, chosen before the first draft (Fable: *explicit success criteria*, *solve the real problem not the literal tokens*). The contract is itself written in ORDO and pins three things:

- **GATE** — the cheapest *real* signal that decides pass/fail. Tiered, hardest-evidence-first:
  - **G-exec** (gold): an executable / deterministic oracle — code that runs to byte-exact stdout, a schema that validates, a regex/property that holds, a diff that applies, a type-check / lint / test suite that goes green. This is the only signal the ORDO corpus proved trustworthy at scale (P4/P5/P8: execution-graded). **Always prefer it. Always.**
  - **G-rubric** (silver): a written rubric the output is self-graded against (Fable: *rubric self-grading*), used ONLY when no executable oracle exists (prose, plans, strategy, design rationale). Each criterion is a checkable assertion, not a vibe.
  - **G-deanchor-pair** (bronze, NL-decode tasks): a blind re-read — a fresh pass reads the output cold and reconstructs the intent; mismatch = fail. This is the natural-language analogue of the ORDO C2 deanchor decode test.
- **TARGET** — the band that ends the loop (e.g. "all G-exec gates green", "rubric ≥ 8/10 on every criterion with no criterion < 6", "blind re-read matches intent 2/2").
- **BUDGET** — `Kmax` passes and a token ceiling. The loop may never exceed either.

The contract is the de-anchor: it forces *what would a senior, perfectionist reviewer reject* (Fable: *honest pushback*) into checkable form before any drafting, so the loop has a real target instead of "looks good."

## 2 · The REFEED cycle (one pass)

Each pass is **DRAFT → REFEED → DECIDE**, with the refeed step being the heart:

```
        ┌────────────────────────────────────────────┐
        │  PASS k                                      │
        │                                              │
  ┌─────▼─────┐   ┌──────────────┐   ┌──────────────┐ │
  │  DRAFT    │──▶│   REFEED      │──▶│   DECIDE     │ │
  │ produce   │   │ run the GATE  │   │ pass→STOP    │ │
  │ under     │   │ on the draft, │   │ fail→distil  │ │
  │ ORDO      │   │ emit a TYPED  │   │ delta, k++,  │ │
  │ output    │   │ verdict +     │   │ loop (unless │ │
  │ contract  │   │ minimal delta │   │ budget hit)  │ │
  └───────────┘   └──────────────┘   └──────┬───────┘ │
        ▲                                    │         │
        └────────────────────────────────────┘  refeed only the delta
```

- **DRAFT.** Produce the output under the full ORDO OUTPUT contract: format-by-shape (TSV for uniform rows, minified JSON for nested, prose only where a human reads it), ponytail verbosity (no preamble, no restating, no closer), caveman only on operational text. Fable: *act, do not survey* — the first draft is a real attempt, not an outline.
- **REFEED (the load-bearing step).** Run the GATE on the draft. This is **chain-of-verification + verifier-loop** done right: the verdict is a *typed* object, not prose praise. For G-exec it is `{pass, mode∈{wrong_output, missing_structure, parse_error, degenerate, abstained}, observed, expected}` (the P5 failure-mode taxonomy — `wrong_output` is confident-wrong, the most valuable signal). For G-rubric it is `{criterion → {score, the single concrete edit that raises it}}`. The verdict carries the **minimal delta** only: the smallest change that flips a failing gate. No full rewrite is emitted at this step.
- **DECIDE.** If every gate is in TARGET → **STOP**, emit. If not, and budget remains → distil the delta into the next DRAFT's instruction (refeed only what failed, not the whole history) and increment k. If budget is hit → STOP and emit with an **honest shortfall note** (which gates are still red), never a false "done."

The discipline that makes this cheap: **refeed the delta, not the transcript.** Each pass re-drafts against a tight, typed critique of the *previous* draft, so context stays clean (Fable: *keep main context clean*) and you pay for correction, not for re-reading your own history.

## 3 · Choosing the loop *shape* per task (the method selector)

REFEED is not one loop — it is a small family, and the task picks the member. This is where the best long-form/loop methods fold in, each used *only where it pays*:

| Task shape | Loop member | Method folded in | Why |
|---|---|---|---|
| Hard structured code / has an executable oracle | **execute-until-correct** (self-refine on G-exec) | self-refine, reflexion, verifier-loop, chain-of-verification | P4/P9: gate removes judge tokens + judge false-passes; pass-count drops ~3.3x on hard tasks. The single most reliable loop. |
| One hard call, high variance, oracle exists | **best-of-N → gate-filter → synthesize** | best-of-N, decomposition | N parallel drafts, the executable gate filters to the survivors, one synthesis pass grafts the best move from each (Fable: *fan-out then synthesize*). Use N small (2-4); N is a tax you justify, not a default. |
| Open design / architecture / naming / "think differently" | **diverge-3-to-5 → debate → pick → graft** | debate, divergence | Fable: *wide solution space means diverge*. 3-5 genuinely distinct approaches, a debate pass that argues them against the REAL goal, pick one, graft the best runner-up move. Gate is G-rubric. |
| Prose / explainer / plan / strategy (no oracle) | **draft → critique → rewrite** (CoVe on a rubric) | draft-critique-rewrite, chain-of-verification, rubric self-grading | No G-exec, so the rubric IS the gate. The critique pass must *adversarially* hunt rejects (Fable: *honest pushback*), not validate. |
| NL command / instruction-following | **draft → blind re-read → reconcile** | deanchor decode, chain-of-verification | G-deanchor-pair: a fresh pass reconstructs intent from the output; divergence is the bug. This is the ONLY honest gate for "did it follow the instruction." |
| Large / multi-file scope | **decompose → per-part REFEED → barrier-synthesize** | decomposition, fan-out | Fable: *more than 5 independent files means parallel subagents, pipeline by default*. Each part runs its own REFEED; synthesize at a barrier only when you need all results at once. |

The selector itself is one cheap classification (an ORDO `■` classify on the task), run once at the top. Get the shape wrong and you either over-spend (best-of-N on an easy task) or under-verify (rubric-only on something that had an executable oracle the whole time).

## 4 · How the OUTPUT FORMAT is chosen per task

Format is not a loop concern — it is decided once, by **data shape**, straight from the ORDO OUTPUT contract, and then held constant across every pass so the gate compares like-for-like:

1. **Uniform rows / tabular → TSV** (header + tabs). ~55% fewer tokens than JSON (VERDICT.md). Never CSV-with-quotes, never a markdown table for machine consumption.
2. **Nested / heterogeneous → minified JSON.** Never pretty-print, never YAML (both measured token traps).
3. **A human reads it to learn or feel → prose**, ponytail-trimmed. This is the one place caveman is forbidden.
4. **Operational text** (status, working notes, the typed verdicts inside the loop) → caveman fragments + arrows.

An explicit ORDO modifier (`表`/`构`/`段`/`全`) overrides the shape default; an epistemic glyph (`信 源 ?`) adds required marking the gate must then check. The rule: **emit only what serves the instruction, in the cheapest faithful form.** The verdict objects passed *between* passes are themselves minified — the loop's own metabolism obeys the output contract.

## 5 · When to STOP (the part that makes it a framework)

A loop without a hard stop is a token furnace. REFEED stops on the FIRST of:

1. **TARGET met** — every gate in band. Emit. (The good exit.)
2. **Budget exhausted** — `k = Kmax` or token ceiling hit. Emit best-so-far + honest shortfall note naming the red gates. (The bounded exit. Fable: *never claim done without evidence* — a budget stop is explicitly "not done.")
3. **No-progress** — two consecutive passes produce no gate-state change (the delta stopped moving). Stop; refeeding a stuck draft burns tokens for nothing. This is the convergence detector.
4. **Marginal-quality-per-token below threshold** — if a pass improves the rubric/gate by less than its token cost warrants (ΔQ/Δtokens under the pre-set floor), stop. This is the explicit *quality-per-token* governor that keeps the loop honest to its own thesis: structure and loops, not brute force.

`Kmax` defaults: **1** for easy tasks where the first draft typically clears the gate (most format/extract jobs — the ORDO output contract alone is usually enough, no loop needed), **3** for hard structured tasks (matches the measured "expected passes drop from ~3.4 to ~1 on hard cells" — you rarely need the third), **5** ceiling for open/diverge work. More passes than that is almost always a wrong gate or a wrong loop shape, not a task that needs more grinding.

## 6 · How it ties to ORDO grammar + output + the harness

- **Command in → ORDO grammar.** The job arrives (or is rewritten) as a readable-ORDO command. The DONE contract is appended as ORDO constraints + epistemic glyphs (`†` verify, `确` state-only-verifiable, `源` cite). `†` at the front of a command is literally "run the REFEED verify gate before answering."
- **Draft out → ORDO OUTPUT contract.** Every draft and every inter-pass verdict obeys format-by-shape + ponytail. This is non-negotiable and is what keeps the *loop itself* token-lean.
- **Harness enforcement.** `harness/ordo.py` already decodes the command deterministically; `harness/output.py` already enforces the output format. REFEED is the orchestration layer that wraps a draft→gate→decide loop around those two, so the model needn't follow the spec by hand and the gate is applied mechanically, not on vibes. The execution gate reuses the P8 per-eval pattern where a fresh oracle is appropriate (capability/regression checks), and the project's real `tests/test_*.py` where product correctness is the question — never randomized language for product code.
- **Macros as loop primitives.** ORDO intent-macros (`cot`, `srev`, `risk`, `eli5`; ~7 tokens each, measured to reliably trigger strong reasoning modes — C7 PASS) are the cheap way to invoke a whole loop shape. A macro like `srev` (self-review) *is* a one-token request for a draft→critique→rewrite pass. This is the highest-leverage, lowest-token way to fire REFEED.

## 7 · The honest core

REFEED multiplies the part of ORDO that *measured true* (grammar structure + output contract + execution gates + a quality lift that reproduced from structure, not glyphs) and refuses to launder the part that didn't (opaque surface as a token or NL-quality lever). The loop buys quality with *structure and a hard gate*, spends extra passes only where a tiered gate says they pay, and stops the instant they stop paying. That is the whole framework: cheap command, cheap output, honest gate, bounded loop, decisive stop.


## The refeed loop (ordered)
1. CLASSIFY: run one cheap ORDO classify on the task to pick the loop shape (execute-until-correct / best-of-N+gate / diverge-debate-graft / draft-critique-rewrite / blind-re-read / decompose-fan-out) and the cheapest REAL gate tier (G-exec executable oracle > G-rubric written rubric > G-deanchor blind re-read).
2. CONTRACT: before any drafting, write the DONE contract in ORDO — GATE (the pass/fail signal), TARGET (the band that ends the loop), BUDGET (Kmax passes + token ceiling). This is the de-anchor: force 'what a perfectionist reviewer would reject' into checkable form up front.
3. FORMAT: choose the output format once by DATA SHAPE from the ORDO output contract (uniform rows→TSV, nested→minified JSON, human-read→ponytail prose, operational→caveman) and hold it constant across all passes so the gate compares like-for-like.
4. DRAFT: produce a real first attempt (act, do not survey) under the full ORDO OUTPUT contract — format-by-shape, ponytail verbosity, caveman only on operational text.
5. REFEED: run the GATE on the draft and emit a TYPED verdict, not prose praise — for G-exec the {pass, mode, observed, expected} failure-mode taxonomy (wrong_output = confident-wrong, the key signal); for G-rubric {criterion→score + the one concrete edit that raises it}; for G-deanchor a blind re-read that reconstructs intent. Carry only the MINIMAL DELTA that flips a failing gate.
6. DECIDE: if every gate is in TARGET → STOP and emit. Else if budget remains → distil ONLY the failed delta into the next draft instruction (refeed the delta, not the transcript), increment k, loop. Else → STOP and emit best-so-far with an honest shortfall note naming the red gates.
7. STOP-CHECK (evaluated every pass, stop on the first true): TARGET met; OR budget exhausted (k=Kmax or token ceiling); OR no-progress (two passes with no gate-state change); OR marginal quality-per-token below the floor (ΔQ/Δtokens too low to justify another pass).
8. EMIT: deliver the final output under the ORDO output contract. If the exit was a budget/no-progress stop rather than TARGET-met, state plainly that it is not done and which gates remain red — never a false 'complete'.

## Pillar integration (honest)
REFEED is built to move each pillar exactly as far as its honest verdict allows, and no further.

P1-context (verdict=NULL): REFEED takes ZERO context-compression from the opaque surface. P1 proved opacity is the wrong axis for token count (glyph-soup roughly doubles the conlang and costs several times plain English, because every multibyte glyph fragments under BPE, and frontier models even strip exotic glyphs during normalization = lossy). So REFEED never skins inbound context into glyphs. Its token savings come only from the layers that measured real: the ORDO grammar on the command (~32%) and the output contract on the response (~55-77%, the 64% end-to-end figure). The one P1 hint REFEED honors is that plain language is already near-optimal inbound, so the framework refeeds DELTAS, not full transcripts, to cut tokens by carrying less context, not by encoding it more densely.

P2-linguistics (verdict=LIMITED): REFEED does not chase a denser keyed surface above readable-ORDO — P2 measured that null-to-negative on tokens (glyph-ORDO 13 vs readable-ORDO 12 on the canonical command) and strictly negative on reliability (1.95 vs 2.00, with silent confident-wrong misreads). So every REFEED command is readable-ORDO. The framework instead banks P2's two real adjacent levers: the grammar structure (typed slots, no-whitespace, determinatives = the 32-35% input cut) lives in the command form, and the output contract (the 55-77% lever) lives in every draft. Phrase glyphing (~1.59 tok/use, small-but-positive) is available via macros but capped, not leaned on.

P3-speed (verdict=LIMITED): REFEED claims NO direct per-call latency win — P3 found the opacity dial token-neutral-to-negative and the corpus has zero wall-clock data. The ONE real speed angle, retry reduction on hard tasks (expected passes ~5→1.03, a ~4.8x drop), is exactly what REFEED's execute-until-correct loop captures: an executable gate that passes first-try more often means fewer loop iterations. REFEED counts this honestly as a THROUGHPUT consequence of the P4 quality result wearing a latency hat (P3's own warning against double-counting), and bounds it to hard, execution-graded tasks only — the easy/med slices get Kmax=1 and no retries to save.

P4-quality (verdict=REAL-LEVER): This is REFEED's spine. P4 measured that forcing composition through an explicit grammar lifts hard-structure correctness (the L0-hard 20% → L3-hard 97% surprise), with the honest caveat that the effect is partly a grading artifact and the AST-regrade may shrink the gap from ~70pp to ~25-40pp. REFEED operationalizes the DEFENSIBLE half: it forces every output through an explicit DONE contract and a typed gate (the explicit-grammar forcing function), and grades on STRUCTURE/EXECUTION where possible, never raw surface. It does NOT pitch opaque grammar as a general quality lever — P4's hard bound (execution-graded code only, does NOT transfer to NL/prose per the deanchor) is why REFEED routes prose to G-rubric and NL to G-deanchor, not to any opaque surface.

P5-halluc (verdict=LIMITED): REFEED adopts P5's split exactly. For code/structured output it uses the {wrong_output, parse_error, degenerate, abstained} failure-mode taxonomy as the gate verdict, because wrong_output (a complete, parseable, confidently-WRONG program) is the cleanest confident-wrong signal and the explicit-grammar forcing function measurably cuts it on hard tasks (70+pp). For NL/factual hallucination REFEED claims NOTHING — P5 is null/untested there, contamination-free only blocks memorization-leak, and there is no abstention axis in the harness yet. So REFEED ADDS the missing axis: the gate verdict includes 'abstained' as a first-class, rewarded outcome (correct abstention on underspecified input beats a confident guess), which is the one new-direction P5 flagged.

P6-tidy (verdict=LIMITED): REFEED's gate measures conformance to the explicit contract (where opaque surface genuinely forces one grammar, P6's real-but-narrow win) and includes a dead-code / surface-tidiness check per pass. It does NOT claim general craft quality from this — P6's caveat (surface tidiness only, not general quality) means the tidiness gate is a conformance check, not a quality verdict, and never substitutes for the G-rubric on actual design quality.

P7-arch (verdict=LIMITED): REFEED uses the diverge-debate-graft loop for architecture decisions but credits the lift to the RIGHT mechanism. P7 was explicit: opacity is null-to-negative for architecture (no executable oracle, NL-judgment regime where readable WINS 2.00 vs 1.95), and the only survivor is 'forcing the answer through an explicit formal schema improves structural consistency' — which is the ordinary structured-output/CoT scaffolding effect (ARM B beats ARM A; ARM C opacity adds nothing). So REFEED's architecture gate is a filled formal schema (dependency edges, blast-radius, typed verdict over fix/refactor/strangler/rebuild) in READABLE form, and the framework does NOT claim the glossopetrae invented-language result improves architectural reasoning. It is structured prompting plus a debate pass, honestly labeled.

P8-rework (verdict=LIMITED): REFEED's G-exec gate reuses the P8 per-eval pattern (CodeForge fresh-language + gradeStructured) ONLY for its proven scope: contamination-free CAPABILITY/regression checks where un-gameability matters. P8's hard caveat governs: this NEVER replaces the project's real tests/test_*.py for PRODUCT correctness — randomizing the language tests the model's coding ability, not whether your code is right. So REFEED routes product-code gates to the real test suite and reserves per-eval generation for the narrow capability-eval niche where retrieval-of-a-memorized-shape is the threat.

P9-longform (verdict=LIMITED): REFEED IS the loop P9 specified, with P9's metric (Q/T = final-pass-rate / total-tokens-across-all-passes) as its quality-per-token STOP governor. P9 measured the loop wins on HARD execution-graded tasks (Q/T up, expected passes 3.36→1.03) and is null-or-slight-loss on easy/med (no headroom, you pay the per-pass tax for nothing). REFEED encodes this directly: Kmax=1 on easy (no loop), the full loop only where the gate is executable and the task is hard, and a marginal-Q/T floor that halts the loop the instant a pass stops earning its tokens. P9's compression-is-null and NL-boundary caveats are why REFEED never uses an opaque surface inside the loop and bounds the Q/T win to code-with-a-real-interpreter.

## Measured (P9 test-gate — single-pass vs REFEED on 5 hard tasks)
Blind judge + token count: **REFEED 2 wins / 3 ties, flaws 4→0** (it caught a genuine correctness
BLOCKER on an LRU cache that the single pass shipped while claiming "audited, all correct" — the
confident-wrong failure, the most valuable kind), at **3.3× the tokens** (13,049 vs 3,944 o200k). The
wins landed exactly on the 2 tasks with a latent bug; neutral on the 3 already-correct ones.
**Conclusion: REFEED is NOT a token saver — it is a bug-catching quality lever, net-positive only when a
latent bug exists and its downstream cost exceeds ~3.3× the generation tokens (correctness-critical
work), and pure tax otherwise.** This is exactly why the loop is SELECTIVE (classify first, Kmax=1 on
easy, stop on the marginal-quality-per-token floor): everywhere it is a token furnace; on hard work it
pays for itself in avoided rework (the P8 link).

## Honest limits
COST OF EXTRA PASSES. Every pass is real tokens, and the loop only nets positive where the quality gate clears more value than the passes cost. Measured shape (P9/P4, n=30, CIs ±7-18pp, one task family of textbook 3-construct logic): on HARD execution-graded tasks the loop cuts expected passes ~3.4→1 and Q/T rises; on EASY/MED tasks there is no headroom — the first ORDO-output-contract draft already clears the gate, so a loop is pure tax (per-pass glyph/verdict overhead with near-zero pass-count benefit). That is why Kmax defaults to 1 for easy work and the marginal quality-per-token floor exists: REFEED must STOP the instant ΔQ/Δtokens drops below the pre-set floor, or it becomes the brute-force token furnace it was built to avoid. Best-of-N is the most expensive member (N parallel drafts) and is justified per-call, never a default; N stays 2-4. The throughput/latency 'win' is a quality result wearing a latency hat (P3) and applies ONLY to hard execution-graded tasks — do not bill it twice.

WHERE GLOSSOPETRAE IS NULL. P1-context is a hard null: the opaque surface does not compress inbound context — it INFLATES tokens (glyph-soup ~2x the conlang, several x plain English, BPE fragments every multibyte glyph, and models strip exotic glyphs during normalization = lossy). REFEED takes zero from this axis. P5-halluc is null on the thing 'hallucination' usually means: there is NO measured reduction in factual/NL confident-wrong, contamination-free only blocks memorization-leak (a small slice), and the abstention axis was unbuilt in the corpus — REFEED adds 'abstained' as a gate outcome but cannot claim a measured NL-hallucination reduction. The opaque-surface-as-token-lever (P2) and opaque-surface-as-NL-quality-lever (P3/P7) are also null-to-negative; REFEED uses readable-ORDO everywhere and credits architecture/prose gains to ordinary structured-prompting scaffolding, not to any invented-language result. Several pillars are LIMITED, not real-lever: their wins are narrow (code/execution only) and the honest framework refuses to generalize them.

THE DEANCHOR CAVEAT (the governing constraint). ORDO's machine-usability gains were EXECUTION-GRADED CODE, and ORDO's own deanchor probe found READABLE WINS on natural-language intent decode (2.00 vs 1.95, with the opaque form producing silent confident-wrong misreads). Therefore an opaque surface does NOT transfer to NL decode, and REFEED must never assume it does. Concretely: REFEED routes execution-graded tasks to G-exec (where the forcing-function quality lift is real), prose/strategy to G-rubric, and NL-instruction-following to G-deanchor (a blind re-read), and it keeps every command and every inter-pass verdict in READABLE form. The loop's quality lever is structure + a hard gate + bounded refeeding — not opacity. Final honesty bounds: the headline numbers are GPT-tokenizer proxies on one frontier model at n=30 (below the publication bar of ~166 seeds), so re-validate per target model before treating any margin as universal; and REFEED's product-correctness gate must use the project's real test suite, never randomized per-eval languages, which test model capability and not whether your code is right.
