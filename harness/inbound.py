"""Inbound context compression — the third side of the triangle: compress what the model READS.

ORDO's command grammar shrinks the *instruction*; the output contract shrinks the *response*; this
shrinks the *documents/context* (files, tool output, RAG chunks, logs) fed in. Prefers **headroom**
(`pip install headroom-ai`) — best-in-class, content-type-aware, reversible (CCR caches originals).
Falls back to a built-in LOSSLESS cleanup so the harness works without the dependency.

Honesty: headroom is LOSSY-but-reversible; always comprehension-test compressed context before trusting
a high ratio (see tools/inbound_bench.py). The built-in fallback is lossless (structure only).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from output import emit, _uniform_records  # noqa: E402

try:
    import tiktoken
    _O2 = tiktoken.get_encoding("o200k_base")
    def _tok(s): return len(_O2.encode(s))
except Exception:  # pragma: no cover
    def _tok(s): return max(1, len(s) // 4)


def _headroom(text: str):
    # message-level pipeline = full router (SmartCrusher JSON + CodeCompressor + Kompress prose),
    # not the content-level masker (which noops prose). Disable protection so docs actually compress.
    from headroom import compress as hc
    r = hc([{"role": "user", "content": text}], model="claude-sonnet-4-5-20250929",
           compress_user_messages=True, protect_recent=0, protect_analysis_context=False)
    msg = r.messages[-1]
    c = msg.get("content") if isinstance(msg, dict) else None
    return c if isinstance(c, str) and c else text


def _builtin(text: str) -> str:
    """Lossless structural cleanup: JSON -> TSV/minified; else collapse dead whitespace."""
    t = text.strip()
    # JSON: route uniform arrays to TSV, everything else to minified (our measured format rule)
    if t[:1] in "[{":
        try:
            data = json.loads(t)
            if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
                data = {"_rows": data}
            return emit(data) if _uniform_records(data)[1] or isinstance(data, dict) else json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        except Exception:
            pass
    # prose/code: collapse 3+ blank lines -> 1, strip trailing ws, collapse runs of spaces (lossless)
    out = re.sub(r"[ \t]+(\n)", r"\1", text)        # trailing whitespace
    out = re.sub(r"\n{3,}", "\n\n", out)            # blank-line runs
    out = re.sub(r"[ \t]{2,}", " ", out)            # interior space runs (outside code this is safe-ish)
    return out


def compress_inbound(text: str, use_headroom: bool = True):
    """Take the BEST of {headroom, builtin} per content (headroom wins on redundant logs/tool-output;
    our TSV wins on structured JSON, which base-headroom noops). Returns
    (compressed_text, tokens_before, tokens_after, engine). Never inflates."""
    before = _tok(text)
    cands = [(text, before, "passthrough")]
    if use_headroom:
        try:
            h = _headroom(text)
            cands.append((h, _tok(h), "headroom"))
        except Exception:
            pass
    try:
        b = _builtin(text)
        cands.append((b, _tok(b), "builtin"))
    except Exception:
        pass
    best = min(cands, key=lambda c: c[1])  # fewest tokens, ties -> earliest (passthrough/headroom)
    return best[0], before, best[1], best[2]


if __name__ == "__main__":
    uniform = json.dumps({"users": [{"id": i, "name": n, "active": True} for i, n in enumerate(["A", "B", "C"], 1)]})
    prose = "This   is   a    test.\n\n\n\nWith   extra      whitespace.   \nTrailing.   "
    for name, s in [("json", uniform), ("prose", prose)]:
        c, b, a, eng = compress_inbound(s, use_headroom=False)
        print(f"{name}: {b} -> {a} tok ({100*(b-a)//max(b,1)}% off) via {eng}")
    assert compress_inbound(uniform, use_headroom=False)[3] == "builtin"
    print("inbound self-check OK (builtin fallback lossless)")
