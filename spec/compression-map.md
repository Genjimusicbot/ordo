# ORDO compression matrix — what to glyph, ranked by total savings

The matrix answers one question with measured data: **of all the words and phrases people actually
type, which ones are worth replacing with a single glyph?** The law is blunt:

> value of glyphing an item = its **frequency** × (**its current token count** − 1)

A glyph that is itself 1 token replaces an item; the saving per use is `(tokens − 1)`, and the total
saving is that times how often the item appears. This kills two intuitions at once.

## The measured verdict (run `python tools/freqmatrix.py`)

**1. The single-word layer is nearly dead — ~1-3%, skip it.**
- Of the top ~29,000 real English words, only **35% are even multi-token** in o200k; the other 65% are
  already 1 token, so glyphing them saves **zero**. Modern tokenizers already won the common-word fight.
- Glyphing *every* multi-token word in that list buys only **~3.3%** of a running-text token stream.
- Worse, the top multi-token words by value are **proper nouns** (February, Jesus, Russia, Robert) —
  useless for a command language. The genuinely useful single-word lever is **~1%**.
- Conclusion: do **not** build a common-word substitution table. It is effort for almost nothing.
  (The full ranking is in `word-matrix.tsv` for the record — note how proper-noun-heavy the top is.)

**2. The phrase layer is the real word-level lever.** Frequent *collocations* are always multi-token
("at the same time" = 3, "on the other hand" = 4, "the following" = 2) and English leans on them
constantly. These are where vocabulary-level compression actually lives. This map glyphs the top 27.

**3. The big levers are not vocabulary at all** — they are the other two ORDO layers:
- **Command structure** (`lexicon.md` directives): a whole instruction like "summarize the following
  from 1 to 10 bullet points" collapses to ~2 glyphs. Biggest **input** win.
- **Verbosity** (the harness/caveman layer, built later): not *generating* the recoverable prose in the
  first place. Biggest **output** win, and output usually dominates the bill.

So the matrix's most valuable output is the redirection: spend effort on **phrases + structure +
verbosity**, not on swapping `information` for a glyph.

## The phrase map (27 collocations → CJK morpheme glyphs)

Each glyph is a Chinese morpheme whose meaning *matches* the phrase — "almost readable, repurposed."
Every glyph verified **1 token in both** cl100k + o200k. Average saving **1.59 tokens per use**.
Machine-readable: `compression-map.tsv`.

| glyph | phrase | saved (o200k) | morpheme sense |
|---|---|---|---|
| 同 | at the same time | 3 | 同 = same |
| 反 | on the other hand | 3 | 反 = opposite |
| 则 | as a result / therefore | 2 | 则 = then/thus |
| 步 | step by step | 2 | 步 = step |
| 即 | in other words | 2 | 即 = namely |
| 关 | in terms of | 2 | 关 = regarding |
| 对 | with respect to | 2 | 对 = toward |
| 及 | as well as | 2 | 及 = and/reach |
| 记 | keep in mind | 2 | 记 = remember |
| 约 | more or less | 2 | 约 = approximately |
| 量 | take into account | 2 | 量 = weigh |
| 例 | for example *(alias: for instance)* | 1 | 例 = example |
| 如 | such as | 1 | 如 = like |
| 因 | because | 1 | 因 = cause |
| 确 | make sure | 1 | 确 = confirm |
| 据 | based on | 1 | 据 = grounded-on |
| 按 | according to | 1 | 按 = per |
| 注 | note that | 1 | 注 = note |
| 加 | in addition | 1 | 加 = add |
| 下 | the following | 1 | 下 = below |
| 为 | in order to | 1 | 为 = for-the-purpose |
| 多 | a lot of | 1 | 多 = many |
| 总 | in general | 1 | 总 = overall |
| 使 | such that | 1 | 使 = so-that |
| 比 | compared to | 1 | 比 = compare |
| 此 | in this case | 1 | 此 = this |
| 异 | the difference between | 1 | 异 = differ |

**Aliases.** Synonyms collapse to the canonical glyph (encode "for instance" → 例; decode 例 → "for
example"). One glyph, one decoded meaning — the decode map stays collision-free.

## Use
- **Encode** (writing a prompt): substitute the phrase for its glyph. `因` instead of "because".
- **Decode** (model reads the spec, expands): glyph → canonical phrase. The model needs `lexicon.md` +
  this map in context once (Design Law: the spec must be present).
- Stacks with the directive layer: `σ 下` = "summarize the following".

## Honesty
Frequencies for the phrase ranking are coarse register estimates (refine from a real corpus later);
the *token costs* are exact. All costs are GPT-tokenizer proxies — a CJK glyph that is 1 token in
o200k may be 2-3 in Claude's proprietary tokenizer, so re-validate per target model (Phase 4). The
matrix proves *direction* (phrases ≫ words; structure ≫ vocabulary), which holds regardless of the
exact per-model number.
