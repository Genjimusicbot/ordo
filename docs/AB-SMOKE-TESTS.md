# ORDO A/B smoke tests — measured, with the flaws named

Every number here is **tiktoken-counted on o200k** (no estimates), reproduce with `python tools/ab_smoke.py`.
The harness shows the **full variant ladder per layer** (not just the best case) and prints the honest weak
spots inline. o200k is a GPT proxy; Claude/Gemini tokenizers differ ([`DISCLAIMERS.md`](../DISCLAIMERS.md)) —
the per-layer **delta** transfers directionally, the glyph row least of all. Run 2026-06-25.

## Results (real o200k token counts)

| # | layer | A (no ORDO) | best ORDO | reduction | the honest read |
|---|---|---|---|---|---|
| 1 | Input command (grammar) | 31 | 11–16 | **−48% readable / −65% glyph** | readable-ORDO is the safe default; glyph is denser but proxy-fragile |
| 2 | Output format (tabular) | 417 | 94 | **−47% minify / −77% TSV** | the −47% minify is FREE + universal; TSV adds the rest, tabular only |
| 3 | Output verbosity (ponytail) | 58 | 17 | **−71%** | lossless, prose answers only; code/substance untouched |
| 4 | Inbound — structured | 729 | 225 | **−69%** | best case (uniform records → TSV) |
| 5 | Inbound — prose (lossless) | 54 | 41 | **−24%** | the honest floor; big prose wins need headroom (lossy, opt-in) |
| 6 | End-to-end realistic turn | 819 | 260 | **−68%** | **shape-dependent** — structured-heavy here; prose-heavy lands far lower |

## Per-layer inputs → outputs (the A/B pairs)

**1 · Input grammar** — same instruction, three encodings:
- A `summarize the following text in 3 bullet points concisely focusing on the financial figures for a non-expert; do not include any preamble` — **31 tok**
- B-readable `sum txt 3bul conc focus:financials aud:lay no:preamble` — **16 tok (−48%)** ← canonical, ASCII-robust
- B-glyph `σ文3列简心金业通¬序` — **11 tok (−65%)** ← opt-in, decodes verbatim, *most proxy-sensitive*

**2 · Output format** — a 12-row uniform array:
- A pretty-printed JSON — **417 tok**
- B-minify `{"rows":[{"id":1,...}]}` — **221 tok (−47%)** ← *just stop pretty-printing*, free, works on ANY JSON
- B-TSV `id⇥user⇥plan⇥mrr / 1⇥user1⇥pro⇥29 / …` — **94 tok (−77%)** ← tabular only; nested data stays minified

**3 · Output verbosity (ponytail)** — a prose answer:
- A `Great question! I'd be happy to help. Here's the answer: …I hope this helps! Let me know if…` — **58 tok**
- B `The function iterates over the list, sums the values, and returns the total.` — **17 tok (−71%)**, lossless
  (flagged filler: great question / i'd be happy to / here's / i hope this helps / let me know if)

**4 · Inbound structured** — a 20-event log fed as context:
- A raw pretty JSON — **729 tok** → B `compress_inbound` (builtin, lossless TSV) — **225 tok (−69%)**

**5 · Inbound prose** — the honest weaker case:
- A redundant-whitespace prose — **54 tok** → B builtin lossless cleanup — **41 tok (−24%)**. Lossless on prose
  is modest by design; the big prose numbers (headroom 60-92%) are *lossy + retrieval* and stay opt-in/gated.

## The meter on real logs (`ordo measure`, read-only)
Ran against the real `~/.claude/projects/**/*.jsonl` history: **71,736 messages · 18.6B tokens · ~42-day span ·
$39,548 (retail, directional)**. The meter flagged `claude-fable-5` + `<synthetic>` as unpriced and reported
**only 7% of tokens are default-priced** — so 93% of the figure is against real model rates, and the integrity
warning tells you exactly how directional the rest is. This is the meter working as designed: it never silently
misleads. (For Max-plan subscription users the *absolute* $ is wrong by construction — the figure is for **A/B
deltas**: run a task corpus with the ORDO profile on vs off and diff.)

## Flaws found (the honest critique) + status

| # | flaw | status |
|---|---|---|
| F1 | **Glyph input is GPT-proxy-fragile** — CJK glyphs may tokenize very differently on Claude; the −65% is the least transferable number | **Reframed:** README leads with readable-ORDO (−48%, ASCII-robust); glyph is labeled opt-in/proxy-sensitive |
| F2 | **Output-format headline conflated two wins** (the free minify vs the TSV format win) | **Fixed:** decomposed — −47% minify (universal) + −77% TSV (tabular only) reported separately |
| F3 | **Inbound was cherry-picked structured** (best case) | **Fixed:** added the prose case (−24% lossless floor); headroom's big numbers labeled lossy+opt-in |
| F4 | **End-to-end implied a flat %** | **Fixed:** labeled SHAPE-DEPENDENT (68% structured-heavy, far lower prose-heavy) |
| F5 | **Meter gave no visibility into how directional the $ is** when a model is unpriced | **Fixed this pass:** `aggregate` now reports `defaultPct` ("7% of tokens default-priced"); +test |
| F6 | **This harness measures TOKENS, not answer quality** | **Bounded:** quality is a separate axis — the blind-judge pillars P4–P9 (`tools/pillars.py`); never conflate token% with quality |

## Still open (upgrades not yet done)
- **Meter `--since` / session filter** for a cleanly scoped A/B (today: isolate runs via `--dir`).
- **Price table for current models** (fable-5, etc.) — the WARN is the honest stand-in; extend `PRICES` to price them.
- **A quality A/B** (blind judge) run alongside the token A/B, committed with transcripts.
- **Validate the deltas on a non-GPT (Anthropic) tokenizer.** *Partially done:* `python tools/tokenizer_robustness.py`
  re-counts the corpus across 4 BPE tokenizers (gpt2 50k → o200k 200k vocab) — the structural wins hold (ponytail
  1pp, TSV 8pp, end-to-end 11pp spread; −68% is the conservative end), the glyph row is the volatile one (33pp).
  Still owed: the *exact* Claude count via Anthropic `count_tokens` (key-gated here; all four above are GPT-lineage).

## The one-line honest summary
On a **structured-data-heavy turn** ORDO cuts ~**47–68%** of tokens **losslessly**, with the single biggest
universal win being *stop pretty-printing JSON* (−47%, free). On a **prose-heavy turn** the lossless floor is
modest (~24%) and the bigger numbers require opt-in lossy compaction that is coverage-gated. Every layer is
measured; nothing lossy is on by default.
