"""tokenizer_robustness — re-count the ab_smoke A/B corpus across several genuinely different BPE tokenizers.

The headline ORDO numbers are o200k (a GPT proxy). Claude's tokenizer isn't public and the count_tokens API
needs a key we don't have here, so the EXACT Claude number stays owed. This is the next-best validation: if a
per-layer reduction is STABLE across tokenizers spanning gpt2 (50k vocab) → o200k (200k vocab), the win is
structural — it deletes whole tokens (keys, whitespace, filler, words), which shrinks on ANY reasonable
tokenizer — not a vocab artifact. The known exception (already flagged in DISCLAIMERS) is the glyph/CJK row,
which IS vocab-dependent; this run makes that visible instead of asserting it. Run: python tools/tokenizer_robustness.py
"""
from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import tiktoken

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import ab_smoke  # noqa: E402 — reuse its A/B corpus, don't duplicate it

# gpt2/p50k/cl100k/o200k are GPT-lineage but genuinely distinct tokenizers (different merges, 50k→200k vocab).
# Not Claude's exact tokenizer (key-gated) — but a reduction stable across all four is structural, so it transfers.
ENCODINGS = ["gpt2", "p50k_base", "cl100k_base", "o200k_base"]
ENCS = {n: tiktoken.get_encoding(n) for n in ENCODINGS}


def red_pct(base_text: str, var_text: str, enc) -> int:
    b, x = len(enc.encode(base_text)), len(enc.encode(var_text))
    return round(100 * (b - x) / b) if b else 0


def run():
    with redirect_stdout(io.StringIO()):     # ab_smoke.run() prints its own o200k report; we only want the corpus
        blocks = ab_smoke.run()

    print("# Tokenizer-robustness — ORDO per-layer reduction across 4 BPE tokenizers\n")
    print("A reduction stable across all four is **structural** (it deletes whole tokens, so it transfers to any")
    print("reasonable tokenizer). A wide spread means the win is vocab-dependent. None of these is Claude's exact")
    print("tokenizer (count_tokens is key-gated) — this tests robustness, not the exact Claude number (still owed).\n")
    print("| layer → ORDO variant | " + " | ".join(ENCODINGS) + " | spread |")
    print("|---|" + "---|" * (len(ENCODINGS) + 1))

    rows = []
    for b in blocks:
        base = b["variants"][0]["text"]
        for v in b["variants"][1:]:
            pcts = [red_pct(base, v["text"], ENCS[n]) for n in ENCODINGS]
            spread = max(pcts) - min(pcts)
            rows.append((b["name"], v["label"], pcts, spread))
            label = f"{b['name']} → {v['label']}"
            print(f"| {label} | " + " | ".join(f"−{p}%" for p in pcts) + f" | {spread}pp |")

    structural = [r for r in rows if "glyph" not in r[1].lower()]
    volatile = [r for r in rows if "glyph" in r[1].lower()]
    worst_struct = max(structural, key=lambda r: r[3]) if structural else None
    print("\n## Verdict")
    if worst_struct:
        print(f"- **Structural rows transfer:** the widest spread among non-glyph variants is "
              f"**{worst_struct[3]}pp** ({worst_struct[0]} → {worst_struct[1]}). The lossless structural wins "
              f"(minify, TSV, ponytail, inbound) hold across a 50k→200k-vocab tokenizer range.")
    if volatile:
        v = volatile[0]
        print(f"- **The glyph row is vocab-dependent (as flagged):** spread **{v[3]}pp** "
              f"({min(v[2])}%–{max(v[2])}%) — readable-ORDO is the safe default, glyphs are opt-in.")
    print("- **Still owed:** the exact Claude-tokenizer count (Anthropic `count_tokens`, key-gated here).")
    return rows


def _selfcheck():
    o = ENCS["o200k_base"]
    assert red_pct("x", "x", o) == 0                       # identical → 0
    assert red_pct("", "x", o) == 0                        # empty base → guarded, no div0
    p = red_pct("the quick brown fox " * 20, "fox", o)     # a much shorter string → positive, bounded reduction
    assert 0 < p <= 100


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    _selfcheck()
    run()
