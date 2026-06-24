# ORDO master vocabulary map — the full allocation, and what the math says about it

We harvested **3,144** high-frequency multi-token items across 15 domains (prose connectives,
collocations, multi-token words, Python, JS/TS, cross-language code, prompt instructions, ML jargon,
shell/git, markdown, math/logic, business/email, web/HTTP, SQL, reasoning), folded in **every
multi-token common word** from `wordfreq` (~25,000 after dedupe), ranked all of them by
`value = frequency × (tokens − 1)`, and allocated **all 1,637 free glyphs** (the 1,674 pool minus the
55 already used by directives + the phrase map). Result: `master-map.tsv`, 1,664 entries.

Then we **measured the realized saving exactly** — encode a real corpus, apply the substitutions,
re-encode, compare — instead of trusting the estimated value. That measurement is the point of this
document, and it is sobering.

## The verified numbers (run `python tools/allocate.py verify`)

| corpus | map | o200k | cl100k |
|---|---|---|---|
| 40 real files (18 py + 22 md) | Tier-A (safe) | **+0.73%** | **+0.43%** |
| general prose, case-folded | Tier-A (safe) | **+5.40%** | **+4.20%** |
| mixed test set | Tier-A (safe) | +1.81% | +0.83% |
| mixed test set | **Full (A+B)** | +2.52% | **−2.15%** |

Three facts the arithmetic forces on us:

1. **On real technical text (code + docs), the entire 1,600-glyph vocabulary layer buys under 1%.**
   Connectives — the high-value items — are simply sparse in code and dense technical writing. The ~5%
   only appears in connective-rich general prose.
2. **The single-word lever stays dead.** Even with ~25k multi-token words allocated glyphs, real-text
   savings barely move. (Confirms the `compression-map.md` finding at full scale.)
3. **Tier B is a cross-tokenizer trap.** Tier-B glyphs are 1 token in o200k but 2-3 in cl100k, so the
   full map *adds* tokens on cl100k (−2.15%). Chasing the o200k number breaks the older tokenizer.

## What ships
- **Tier-A subset (501 glyphs: 474 new + 27 phrase) = the recommended vocabulary layer.** 1 token in
  *both* tokenizers, so always non-negative. Worth ~0.5-1% on technical text, ~4-5% on prose. A real
  but minor optimization — use it, don't oversell it.
- **Tier-B (1,163 glyphs) = experimental, o200k-targets only**, clearly flagged. Do not enable when
  cl100k-family models are in the loop.
- Full ranked allocation kept in `master-map.tsv` for the record (rank, tier, measured cost, value,
  cumulative %). Marginal curve: top-400 ≈ 52% of estimated value, top-800 ≈ 75%, tail thin.

## The verdict that redirects the project
Vocabulary substitution — words *and* phrases, maximally allocated, measured on real text — is a
**~1-5% lever, register-dependent and tokenizer-fragile.** It is not where "compacting the world"
lives. The math points the same way the intuition did: the real gains are in the two layers we have
**not** yet built —
- **Grammar / command structure**: collapsing a whole instruction ("summarize the following in three
  bullet points, keep the numbers") into ~3 glyphs. This compresses the *structure*, which on a prompt
  is far more tokens than its vocabulary. **Built next (P2).**
- **Verbosity / output**: not generating the recoverable prose at all. The biggest lever, because
  output usually dominates the bill. (The harness layer, later.)

## Honesty
Frequencies used for *ranking* are estimates (harvest + wordfreq); the *verification* uses real
corpora and exact tokenization, so the headline percentages are measured, not modeled. Costs are
cl100k/o200k (GPT proxies) — Claude's tokenizer is proprietary and a Tier-A CJK glyph that is 1 token
here may differ there, so re-validate per model (the cl100k/o200k disagreement on Tier B is itself the
warning). Prose numbers are case-folded (fair); code is exact-match (conservative). In-context BPE
merges are already included because we measure the encoded substituted text directly.
