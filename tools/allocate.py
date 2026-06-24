"""allocate — assign the 1-token glyph pool to the highest-value items, then VERIFY on real corpora.

Two commands:
  python tools/allocate.py build  <candidates.json>     # measure -> value-rank -> greedy glyph assign
  python tools/allocate.py verify <map.tsv> <file...>   # exact before/after token reduction on real text

Value law (Design Law of the matrix): value = frequency x (current_token_count - 1). We rank ALL
candidates (harvested phrases + every multi-token common word from wordfreq) by value, then hand the
safest glyphs (Tier A = 1 token in both cl100k+o200k) to the top items and Tier B (o200k-only) to the
tail. The 28 directive glyphs and 27 existing phrase glyphs are RESERVED (never reused). Allocation
uses estimated frequency (a heuristic for WHAT to glyph); the verify command measures the REALIZED
saving exactly on real corpora (the math). cl100k+o200k are GPT proxies; Claude is proprietary.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import tiktoken

CL = tiktoken.get_encoding("cl100k_base")
O2 = tiktoken.get_encoding("o200k_base")
ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec"


def tok(s):
    return len(CL.encode(s)), len(O2.encode(s))


def _read_tsv(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == len(header):
                rows.append(dict(zip(header, parts)))
    return rows


def load_pool():
    """Return (tierA_glyphs, tierB_glyphs) excluding glyphs already used by directives + phrase map."""
    reserved = set()
    for r in _read_tsv(SPEC / "lexicon.tsv"):
        reserved.add(r["glyph"])
    phrase_map = {}
    for r in _read_tsv(SPEC / "compression-map.tsv"):
        reserved.add(r["glyph"])
        phrase_map[r["phrase"]] = r["glyph"]
    A, B = [], []
    for r in _read_tsv(SPEC / "glyph-pool.tsv"):
        g = r["glyph"]
        if g in reserved:
            continue
        (A if r["tier"] == "A" else B).append(g)
    return A, B, phrase_map, reserved


def wordfreq_words(n=30000):
    try:
        import wordfreq
    except ImportError:
        return []
    out = []
    for w in wordfreq.top_n_list("en", n):
        if w.isalpha() and len(w) >= 2:
            out.append({"text": w, "freq_per_million": wordfreq.word_frequency(w, "en") * 1e6, "domain": "word"})
    return out


def build(candidates_path):
    A, B, phrase_map, reserved = load_pool()
    cands = json.loads(Path(candidates_path).read_text(encoding="utf-8")).get("items", [])
    cands = cands + wordfreq_words()
    # measure + filter + dedup (keep max freq per text)
    best = {}
    for c in cands:
        text = (c.get("text") or "").strip()
        if not text or text in phrase_map:        # skip already-mapped phrases
            continue
        cl, o2 = tok(text)
        if o2 < 2:                                # 1 token already -> no saving
            continue
        f = float(c.get("freq_per_million") or 0)
        prev = best.get(text)
        if prev is None or f > prev["freq"]:
            best[text] = {"text": text, "cl": cl, "o2": o2, "freq": f, "domain": c.get("domain", "?")}
    items = list(best.values())
    for it in items:
        it["value"] = it["freq"] * (it["o2"] - 1)
    items.sort(key=lambda it: -it["value"])
    # greedy allocation: Tier A to the top, then Tier B
    glyphs = A + B
    n = min(len(items), len(glyphs))
    rows = []
    for i in range(n):
        it = items[i]
        it["glyph"] = glyphs[i]
        it["tier"] = "A" if i < len(A) else "B"
        rows.append(it)
    # master map = existing 27 phrases (kept) + new allocations
    out = SPEC / "master-map.tsv"
    cum = 0.0
    total_value = sum(it["value"] for it in rows) + 1e-9
    with out.open("w", encoding="utf-8") as f:
        f.write("rank\ttext\tglyph\ttier\tcl100k\to200k\tsaved\tfreq_per_M\tvalue\tcum_value_pct\tdomain\n")
        # pre-existing phrase map first (already shipped), then new
        for ph, g in phrase_map.items():
            cl, o2 = tok(" " + ph)
            f.write(f"-\t{ph}\t{g}\tA\t{cl}\t{o2}\t{o2-1}\t-\t-\t-\tphrase-map\n")
        for i, it in enumerate(rows):
            cum += it["value"]
            f.write(f"{i+1}\t{it['text']}\t{it['glyph']}\t{it['tier']}\t{it['cl']}\t{it['o2']}\t"
                    f"{it['o2']-1}\t{round(it['freq'],2)}\t{round(it['value'],1)}\t{round(100*cum/total_value,2)}\t{it['domain']}\n")
    # marginal curve checkpoints
    print(f"candidates measured: {len(items)} multi-token (after dropping 1-token + dupes + 27 mapped)")
    print(f"glyphs available (pool 1674 - {len(reserved)} reserved): A={len(A)} B={len(B)} -> allocated {n}")
    for k in (50, 100, 200, 400, 800, 1200, n):
        if k <= n:
            c = sum(it["value"] for it in rows[:k])
            print(f"  top {k:4} glyphs capture {100*c/total_value:5.1f}% of total estimated value")
    print(f"\nwrote spec/master-map.tsv ({len(phrase_map)} phrase-map + {n} new = {len(phrase_map)+n} entries)")
    return 0


def verify(map_path, files):
    # build replacement list, longest-first (avoid partial overlaps)
    pairs = []
    for r in _read_tsv(map_path):
        if r.get("text") and r.get("glyph"):
            pairs.append((r["text"], r["glyph"]))
    pairs.sort(key=lambda p: -len(p[0]))
    print(f"map: {len(pairs)} substitutions\n")
    tot_o_before = tot_o_after = tot_c_before = tot_c_after = 0
    for fp in files:
        text = Path(fp).read_text(encoding="utf-8", errors="ignore")
        sub = text
        for s, g in pairs:
            if s in sub:
                sub = sub.replace(s, g)
        cb, ob = len(CL.encode(text)), len(O2.encode(text))
        ca, oa = len(CL.encode(sub)), len(O2.encode(sub))
        tot_c_before += cb; tot_c_after += ca; tot_o_before += ob; tot_o_after += oa
        name = Path(fp).name
        print(f"  {name:28} o200k {ob:6} -> {oa:6}  ({100*(ob-oa)/ob:4.1f}% )   cl100k {cb:6} -> {ca:6}  ({100*(cb-ca)/cb:4.1f}% )")
    print(f"\n  TOTAL  o200k {tot_o_before:7} -> {tot_o_after:7}  = {100*(tot_o_before-tot_o_after)/tot_o_before:.2f}% reduction")
    print(f"  TOTAL  cl100k {tot_c_before:7} -> {tot_c_after:7}  = {100*(tot_c_before-tot_c_after)/tot_c_before:.2f}% reduction")
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "build":
        sys.exit(build(sys.argv[2]))
    elif len(sys.argv) >= 4 and sys.argv[1] == "verify":
        sys.exit(verify(sys.argv[2], sys.argv[3:]))
    else:
        print(__doc__)
        sys.exit(2)
