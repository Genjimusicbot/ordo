"""standalone_compare — ORDO's full stack vs each single-layer standalone tool, on the SAME turn.

The honest question the README must answer: "how many tokens vs just using tool X?" Each rival tool covers
ONE layer; ORDO stacks all of them, lossless-first. This measures the marginal truth, not a marketing line:
  - ORDO beats every LOSSLESS single-layer tool because it covers more layers (input + format + verbosity +
    inbound), not because its per-layer ratio is higher;
  - a LOSSY specialist (headroom/llmtrim) on the DOMINANT layer can beat ORDO's raw token count — at a
    quality/retrieval risk ORDO refuses by default and only opts into behind the coverage gate;
  - so "fewest tokens" is NOT ORDO's claim. "Fewest tokens WITHOUT quality loss, across every layer" is.
Tokens measured on o200k (tiktoken). Run: `python tools/standalone_compare.py`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
sys.path.insert(0, str(ROOT / "tools"))

from ordo import decode                      # noqa: E402
from output import emit                       # noqa: E402
from inbound import compress_inbound          # noqa: E402
from tokcost import cost                       # noqa: E402

TOK = lambda s: cost(s)["o200k_base"]         # noqa: E731


def main():
    # the same realistic, structured-data-heavy turn as ab_smoke (instruction + inbound log + answer)
    cmd = "σ文3列简心金业通¬序"
    english = decode(cmd)
    readable = "sum txt 3bul conc focus:financials aud:lay no:preamble"
    log = {"events": [{"ts": 1000 + i, "lvl": "INFO" if i % 4 else "WARN", "msg": f"req {i} ok", "ms": 12 + i}
                      for i in range(20)]}
    log_pretty = json.dumps(log, indent=2)
    log_min = json.dumps(log, separators=(",", ":"))
    log_tsv, _, _, _ = compress_inbound(log_pretty, use_headroom=False)        # lossless TSV
    verbose = ("Great question! I'd be happy to help. Here's the answer: the function works by iterating over "
               "the list and summing the values, then returning the total. I hope this helps! Let me know if "
               "you have any other questions or if there's anything else I can do for you.")
    lean = "The function iterates over the list, sums the values, and returns the total."

    # is headroom installed? if so we MEASURE the lossy inbound; else we cite its published claim.
    log_hr, _, _, hr_eng = compress_inbound(log_pretty, use_headroom=True)
    have_hr = (hr_eng == "headroom")
    log_hr_tok = TOK(log_hr) if have_hr else round(TOK(log_pretty) * 0.08)     # 92%-off published claim

    base = TOK(english) + TOK(log_pretty) + TOK(verbose)

    # each row: (label, tokens, lossless?, layers covered, note)
    rows = [
        ("RAW Claude harness (no tool)", base, True, "none", "the baseline everyone starts from"),
        ("minify-only (any JSON minifier)", TOK(english) + TOK(log_min) + TOK(verbose), True, "format",
         "the free universal win — but only the inbound JSON, nothing else"),
        ("formatter-only (TOON/TSV tool)", TOK(english) + TOK(log_tsv) + TOK(verbose), True, "format",
         "tabular structure only; leaves the prompt + the answer untouched"),
        ("ponytail-only (a terse-output tool)", TOK(english) + TOK(log_pretty) + TOK(lean), True, "verbosity",
         "cuts the answer's filler; the dominant inbound blob is untouched → tiny win on a data-heavy turn"),
        ("inbound-lossless-only (rtk-style lossless)", TOK(english) + TOK(log_tsv) + TOK(verbose), True, "inbound",
         "lossless inbound; same as the formatter here because the data is the dominant layer"),
        (f"headroom-only ({'measured' if have_hr else 'PUBLISHED 92% claim'}, LOSSY)",
         TOK(english) + log_hr_tok + TOK(verbose), False, "inbound",
         "aggressive lossy on the dominant blob — can BEAT ORDO on tokens, at retrieval/quality risk"),
        ("ORDO full stack (readable+TSV+ponytail)", TOK(readable) + TOK(log_tsv) + TOK(lean), True, "input+format+verbosity+inbound",
         "every layer, lossless — beats every LOSSLESS single-layer tool"),
        (f"ORDO + headroom inbound ({'measured' if have_hr else 'claim'}, gated)",
         TOK(readable) + log_hr_tok + TOK(lean), False, "all + lossy-inbound (coverage-gated)",
         "ORDO does not compete with headroom — it INCLUDES it as a gated lossy option for the inbound layer"),
    ]

    print("# ORDO stack vs standalone tools — same turn, real o200k tokens\n")
    print(f"baseline (raw Claude harness) = **{base} tok**. headroom installed: **{have_hr}**.\n")
    print("| approach | tokens | vs raw | lossless | layers | note |")
    print("|---|---|---|---|---|---|")
    for lb, tk, lossless, layers, note in rows:
        pct = round(100 * (base - tk) / base) if base else 0
        print(f"| {lb} | {tk} | **−{pct}%** | {'✅' if lossless else '⚠ LOSSY'} | {layers} | {note} |")
    print("\n**The honest read:** among LOSSLESS approaches, ORDO's full stack wins (−"
          f"{round(100*(base-(TOK(readable)+TOK(log_tsv)+TOK(lean)))/base)}% vs the best single-layer lossless "
          "tool's far smaller cut) — *because it covers more layers, not because any one ratio is higher*. A "
          "LOSSY specialist on the dominant layer (headroom) can beat ORDO's raw token count, but that is a "
          "different trade (it can drop the line you needed). ORDO doesn't fight that tool — it stacks it, "
          "coverage-gated, as its inbound layer. Tokens are one axis; losslessness + the quality gates are the other.")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
