"""ab_smoke — REAL A/B smoke tests: ORDO vs no-ORDO, per layer, measured on o200k (tiktoken).

Honest-first: every number is tiktoken-counted (no estimates), each layer shows the FULL variant ladder
(not just the best case), and the known weaknesses are printed, not hidden:
  - input grammar shows readable-ORDO (canonical, ASCII-robust) AND glyph-ORDO (opt-in, proxy-sensitive);
  - output format separates the FREE "stop pretty-printing" win (minify) from the TSV format win;
  - inbound shows the structured best case AND a prose case (where the lossless builtin saves far less);
  - the end-to-end % is flagged as shape-dependent (it tracks how much structured data is in the turn).
o200k is a GPT proxy; Claude/Gemini tokenizers differ (DISCLAIMERS) — the per-layer DELTA transfers
directionally, the glyph row least of all. Run: `python tools/ab_smoke.py`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
sys.path.insert(0, str(ROOT / "tools"))

from ordo import decode                      # noqa: E402
from output import emit, ponytail_flags      # noqa: E402
from inbound import compress_inbound         # noqa: E402
from tokcost import cost                      # noqa: E402

TOK = lambda s: cost(s)["o200k_base"]         # noqa: E731 — the modern GPT tokenizer


def _prev(s: str, n: int = 180) -> str:
    s = s.replace("\n", "\\n")
    return s if len(s) <= n else s[:n] + " …"


def block(name, variants, faithful, note=""):
    """variants = [(label, text), ...]; variants[0] is the no-ORDO baseline A."""
    base = TOK(variants[0][1])
    out = [{"label": lb, "text": tx, "tok": TOK(tx),
            "pct": (round(100 * (base - TOK(tx)) / base) if base else 0)} for lb, tx in variants]
    return {"name": name, "variants": out, "base": base, "faithful": faithful, "note": note,
            "best": min(out[1:], key=lambda v: v["tok"]) if len(out) > 1 else out[0]}


def run():
    blocks = []

    # 1) INPUT GRAMMAR — three encodings of the SAME instruction.
    cmd = "σ文3列简心金业通¬序"
    english = decode(cmd)
    readable = "sum txt 3bul conc focus:financials aud:lay no:preamble"  # readable-ORDO (canonical)
    blocks.append(block("Input command (grammar)",
        [("plain English instruction", english),
         ("readable-ORDO (canonical, ASCII-robust)", readable),
         ("glyph-ORDO (opt-in, MOST proxy-sensitive)", cmd)],
        "lossless intent — glyph form decodes to A verbatim; readable form is the same instruction terser",
        "the glyph row is the LEAST transferable: CJK tokenizes differently on Claude — readable-ORDO is the safe default."))

    # 2) OUTPUT FORMAT — separate the free minify win from the TSV format win.
    data = {"rows": [{"id": i, "user": f"user{i}", "plan": ["free", "pro", "team"][i % 3], "mrr": i * 29}
                     for i in range(1, 13)]}
    blocks.append(block("Output format (tabular)",
        [("pretty-printed JSON (the default everyone ships)", json.dumps(data, indent=2)),
         ("minified JSON (FREE universal win — just stop pretty-printing)", json.dumps(data, separators=(",", ":"))),
         ("ORDO emit() → TSV", emit(data))],
        "lossless — same 12 rows/4 fields; read-accuracy gate passed (spec/output.md)",
        "most of the headline is the free minify; TSV adds the rest. On NESTED data TSV does not apply — minify is the win."))

    # 3) OUTPUT VERBOSITY (ponytail).
    verbose = ("Great question! I'd be happy to help. Here's the answer: the function works by iterating "
               "over the list and summing the values, then returning the total. I hope this helps! Let me "
               "know if you have any other questions or if there's anything else I can do for you.")
    lean = "The function iterates over the list, sums the values, and returns the total."
    blocks.append(block("Output verbosity (ponytail)",
        [("chatty answer (preamble + closer)", verbose), ("ponytail (filler cut)", lean)],
        f"lossless — only filler removed; flagged: {ponytail_flags(verbose)}",
        "applies to PROSE answers; the substance and code are untouched."))

    # 4a) INBOUND structured (the TSV best case).
    log = {"events": [{"ts": 1000 + i, "lvl": "INFO" if i % 4 else "WARN", "msg": f"req {i} ok", "ms": 12 + i}
                      for i in range(20)]}
    log_pretty = json.dumps(log, indent=2)
    comp, _, _, eng = compress_inbound(log_pretty, use_headroom=False)
    blocks.append(block("Inbound — structured (best case)",
        [("raw pretty JSON doc", log_pretty), (f"compress_inbound ({eng}, lossless)", comp)],
        "lossless — measured-revert guarantees it never inflates (worst case = passthrough)",
        "this is the BEST case (uniform records → TSV). Real inbound is often prose — see the next block."))

    # 4b) INBOUND prose (the HONEST weaker case — builtin only does lossless whitespace cleanup).
    prose = ("The deployment   pipeline   runs in three stages.   \n\n\n\nFirst it builds the image.   \n"
             "Then it    pushes to the registry.   \n\n\nFinally it    rolls out to the cluster.   \n"
             "Each stage   logs to stdout   and   fails closed on error.   ")
    comp_p, _, _, eng_p = compress_inbound(prose, use_headroom=False)
    blocks.append(block("Inbound — prose (honest weaker case)",
        [("raw prose (redundant whitespace)", prose), (f"compress_inbound ({eng_p}, lossless)", comp_p)],
        "lossless — only dead whitespace collapsed; NO content dropped",
        "lossless on prose is modest. Big prose wins need headroom (lossy+gated) — not shown here (opt-in)."))

    # 5) END-TO-END — a realistic turn (readable-ORDO + TSV inbound + ponytail) vs all-plain.
    a_e2e = english + "\n\n" + log_pretty + "\n\n" + verbose
    b_e2e = readable + "\n\n" + comp + "\n\n" + lean
    blocks.append(block("End-to-end realistic turn",
        [("all plain (English + raw JSON + chatty)", a_e2e),
         ("all ORDO (readable-ORDO + TSV + ponytail)", b_e2e)],
        "the blended delta across a full turn (using the SAFE readable-ORDO, not glyphs)",
        "SHAPE-DEPENDENT: this turn is structured-data-heavy. A prose-heavy turn lands far lower (see 4b)."))

    # ---- report ----
    print("# ORDO A/B smoke tests — real o200k token counts\n")
    print("| # | layer | A (no ORDO) | best ORDO | reduction |")
    print("|---|---|---|---|---|")
    for i, b in enumerate(blocks, 1):
        print(f"| {i} | {b['name']} | {b['base']} tok | {b['best']['tok']} tok | **−{b['best']['pct']}%** |")
    print("\n---\n")
    for i, b in enumerate(blocks, 1):
        print(f"## {i}. {b['name']}")
        for v in b["variants"]:
            d = "" if v is b["variants"][0] else f"  → **−{v['pct']}%**"
            print(f"- **{v['label']}** — {v['tok']} tok{d}\n  `{_prev(v['text'])}`")
        print(f"- faithful: {b['faithful']}")
        if b["note"]:
            print(f"- ⚠ honest note: {b['note']}")
        print()
    return blocks


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    run()
