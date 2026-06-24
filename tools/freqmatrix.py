"""freqmatrix — rank what to glyph by total token savings (frequency x tokens-saved).

The compression law: the value of replacing a word/phrase with a 1-token glyph is
    value = frequency  x  (current_tokens - 1)
so a frequent MULTI-token item beats a rare big word AND beats a frequent already-1-token word
(swapping "the" 1->1 saves nothing). We score in "tokens saved per 1,000,000 words of typical text"
so the numbers are interpretable and additive. Token costs are measured space-prefixed (running-text
form). cl100k + o200k (GPT proxies; Claude proprietary, see DISCLAIMERS).
"""
from __future__ import annotations

from pathlib import Path

import tiktoken
import wordfreq

CL = tiktoken.get_encoding("cl100k_base")
O2 = tiktoken.get_encoding("o200k_base")
SPEC = Path(__file__).resolve().parent.parent / "spec"

# High-frequency MULTI-token phrases (instruction + connective + dev). Frequencies are coarse
# per-million estimates (English running text / LLM-prompt register); refine later from a real corpus.
PHRASES = {
    "the following": 900, "for example": 700, "make sure": 500, "in order to": 500, "such as": 700,
    "as well as": 600, "based on": 500, "according to": 400, "in other words": 200, "step by step": 150,
    "on the other hand": 150, "as a result": 250, "keep in mind": 120, "take into account": 80,
    "a lot of": 600, "in addition": 250, "for instance": 200, "note that": 200, "in this case": 200,
    "at the same time": 150, "in terms of": 250, "with respect to": 120, "let me know": 150,
    "feel free to": 100, "I would like to": 150, "can you": 400, "could you": 200, "please": 800,
    "make a list of": 60, "write a function that": 80, "the bug": 90, "error handling": 90,
    "return value": 120, "unit test": 90, "for the most part": 60, "due to the fact that": 40,
    "as soon as": 150, "more or less": 80, "in general": 200, "as shown": 100, "the difference between": 90,
}


def tok(s: str):
    return len(CL.encode(s)), len(O2.encode(s))


def score_items(items):
    """items: dict word/phrase -> per-million frequency. Returns ranked rows + totals."""
    rows, tot_tokens, tot_saved = [], 0.0, 0.0
    for w, fpm in items.items():
        cl_b, o2_b = tok(" " + w)           # running-text form
        saved = o2_b - 1                     # if mapped to a single 1-token glyph
        score = fpm * saved                  # tokens saved per 1M words
        rows.append((w, cl_b, o2_b, saved, round(score, 1), fpm))
        tot_tokens += fpm * o2_b
        tot_saved += fpm * saved
    rows.sort(key=lambda r: -r[4])
    return rows, tot_tokens, tot_saved


def main():
    N = 30000
    words = {w: wordfreq.word_frequency(w, "en") * 1e6
             for w in wordfreq.top_n_list("en", N) if w.isalpha() and len(w) >= 2}
    N = len(words)  # real alphabetic words only (drop digits/abbreviations)
    wrows, wtok, wsav = score_items(words)
    multi = [r for r in wrows if r[2] > 1]
    print(f"WORDS: top {N} English words")
    print(f"  multi-token in o200k (the real targets): {len(multi)}/{N} ({100*len(multi)/N:.0f}%); "
          f"the rest are already 1 token (glyphing them saves 0)")
    print(f"  word-layer ceiling: ~{wsav:,.0f} tokens saved / 1M words vs ~{wtok:,.0f} total = "
          f"{100*wsav/wtok:.1f}% reduction from the WORD layer alone")
    print("  top 12 words by value (word, o200k_tok, saved/1M):")
    for r in wrows[:12]:
        print(f"     {r[0]:16} {r[2]}tok  score={r[4]}")

    prows, ptok, psav = score_items(PHRASES)
    print(f"\nPHRASES: {len(PHRASES)} common multi-token phrases")
    print("  top 12 phrases by value (phrase, o200k_tok, saved/1M):")
    for r in prows[:12]:
        print(f"     {r[0]:22} {r[2]}tok  score={r[4]}")

    # write the matrices
    with (SPEC / "word-matrix.tsv").open("w", encoding="utf-8") as f:
        f.write("word\tcl100k\to200k\tsaved\tscore_per_1M\tfreq_per_1M\n")
        for r in wrows:
            if r[3] > 0:
                f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{round(r[5],2)}\n")
    with (SPEC / "phrase-matrix.tsv").open("w", encoding="utf-8") as f:
        f.write("phrase\tcl100k\to200k\tsaved\tscore_per_1M\tfreq_per_1M_est\n")
        for r in prows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]}\n")
    nw = sum(1 for r in wrows if r[3] > 0)
    print(f"\nwrote spec/word-matrix.tsv ({nw} multi-token words) + spec/phrase-matrix.tsv ({len(prows)} phrases)")


if __name__ == "__main__":
    main()
