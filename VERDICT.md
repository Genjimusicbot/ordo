# ORDO — the verdict (audit-ready, every claim measured)

What ORDO is worth, on the user's real terms (not just token density), after an evidence-gated build
(P0-P4) and an autonomous experiment run (C1-C9). Every number below was produced by a tokenizer
(`tiktoken`, cl100k + o200k) or a blind multi-agent test, never asserted. Caveat that governs all of
it: costs are GPT-tokenizer proxies; the tests ran on one frontier model; re-validate per target model.

## TL;DR
**ORDO works, but not for the reason we started with.** The value is not exotic glyphs — it is the
**grammar structure + an output-discipline contract**. Measured: a realistic request+response drops
**~64% of tokens** end-to-end, and blind judges rated ORDO's output **better than plain English on 6 of
9 tasks** (2 ties, 1 loss). It clears the user's ≥10% bar by a wide margin **and** delivers the
"more-than-tokens" gain (quality), with honest nulls where the evidence didn't support a claim.

## The measured stack
| layer | metric | result | criterion |
|---|---|---|---|
| Input grammar (ORDO-G) | token save on 20 real prompts | **35% glyph / 32% readable** | — |
| Grammar decodability | blind decode fidelity /2 | **1.70 (3-file) → 1.75 (skillstone)** | — |
| **Surface form (deanchor)** | readable vs glyph: tokens + decode | **readable 2.00/2 @ −32%; glyph 1.95/2 @ −35%** | **C2 PASS** |
| End-to-end (prompt+output) | combined token save, realistic mix | **64%** (explainer 51%, structured 72%) | **C3 PASS** |
| **Output quality** | blind A/B vs English, 9 tasks | **ORDO 6 win / 2 tie / 1 loss** (structure-driven) | **C4 PASS** |
| Speed (proxy) | output-token delta | **−32%** (≈−48% ex one outlier) | **C6 PASS** |
| Hallucination | confident-wrong + calibration | **no backfire; better-calibrated abstention; no reduction at saturated baseline** | **C5 PASS (null on reduction, +calibration)** |
| Intent-as-symbol macros | save/use + decode | **6.8 tok/use saved, decode 1.8/2** | **C7 PASS** |
| Output format | tabular vs JSON | **TSV −55%; never pretty-print; YAML is a trap** | — |
| Verbosity | ponytail (lossless) | **−77% on a chatty answer** | — |
| The harness | deterministic decode + output enforce | **8/8 tests green** | **C8 PASS** |

## The four findings that matter
1. **Deanchor was right (C2).** Exotic glyphs buy only **3 percentage points** over readable English
   keywords (35% vs 32%) and decode *worse* (1.95 vs a perfect 2.00, with silent confident-wrong
   misreads). The grammar *structure* carries the saving; the glyphs were paying reliability for almost
   nothing. **Default = readable-ORDO; glyphs = opt-in dense mode only.**
2. **The +36pp "glyph quality" lift reproduces as a STRUCTURE lift (C4).** ORDO out-quality'd English
   using *readable* ORDO — no foreign glyphs. The gain is a typed, unambiguous, one-parse command +
   an output contract, not glyph-foreignness. Cleaner and more defensible than the original hypothesis.
3. **Output is the real prize.** Input grammar is a bounded ~32%; the output layer (format-by-shape +
   ponytail) is where 64% end-to-end comes from, because output dominates the bill and most of it is
   recoverable filler. The ORDO output contract is the single highest-value, lowest-risk piece.
4. **Honest nulls.** No measured wall-clock speed win (only an output-token saving — fewer tokens ≠ 1:1
   latency). No measured hallucination reduction on a strong model (baseline already at floor) — but no
   backfire and a better-calibrated abstention posture; the benefit would show on weaker models.

## The CUT LIST (what did NOT earn its place)
- **Single-word substitution** — measured ~1% useful (BPE already compressed common words). Dead. Don't
  build a word-swap table.
- **Exotic glyphs as the wire format** — lose the deanchor test (reliability cost for ~3% tokens).
  Demoted to opt-in dense mode for proven-round-trip commands only.
- **Tier-B (o200k-only) glyphs** — break the cl100k tokenizer (net-negative there). Off by default.
- **Runes / uppercase-Greek / kanji-as-glamour** — token-negative (runes = 3 tokens). Rejected at the gate.
- **"ORDO makes models faster"** — unproven; only an output-token saving is measured. Drop the speed claim.
- **"Epistemic markers cure hallucination"** — overstated for strong models (no measured reduction).
  Keep them (no backfire + better calibration + likely helps weaker models), but don't oversell.
- **YAML / pretty-printed JSON for machine output** — measured token traps.

## How to actually use ORDO (the recommendation)
1. **Readable-ORDO grammar** as the command form: `sum txt 3bul conc aud:lay no:preamble`. ~32% input,
   reliable, human-debuggable.
2. **The output contract** on every response: format-by-shape (TSV/JSON, never pretty), ponytail (cut
   filler, lossless), caveman on operational text only. This is the big lever (~55-77%).
3. **Intent macros** (`cot`, `srev`, `risk`, `eli5` …) for whole recurring intents — ~7 tokens each and
   they reliably trigger strong reasoning modes (a quality lever too).
4. **The harness** (`harness/`) applies decode + output-format automatically, so the model needn't
   follow the spec by hand.
5. Skip the glyph wire format unless you have a measured dense-mode niche.

## Provenance
Built P0-P4 (alphabet → grammar → output framework → skillstone), then driven to done by an ADAPT run
(C1 research synthesis of 20 docs/63 mechanisms → C2 deanchor → C8 harness → C3 floor → C4/C6
quality+speed → C5 hallucination → C7 macros → C9 this verdict). Full per-phase evidence in
`docs/BUILD-LOG.md`; the acceptance spec + ledger in `tasks/adapt/`. Commits are local (not pushed).
