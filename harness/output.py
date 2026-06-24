"""Output-contract enforcement (the other half of the harness): pick the cheapest faithful format.

Measured rule (see spec/output.md + tools/formatbench.py): uniform array of records -> TSV (~55% off
JSON); everything else -> minified JSON (never pretty-print). emit() applies it; ponytail_flags()
catches the filler the verbosity layer forbids.
"""
from __future__ import annotations

import json


def _uniform_records(data):
    """Return (key, rows) if data is {k: [ {..}, .. ]} with uniform flat dicts, else (None, None)."""
    if isinstance(data, dict) and len(data) == 1:
        k = next(iter(data)); v = data[k]
        if isinstance(v, list) and v and all(isinstance(x, dict) for x in v) \
           and all(x.keys() == v[0].keys() for x in v) \
           and all(not isinstance(val, (dict, list)) for x in v for val in x.values()):
            return k, v
    return None, None


def _scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return "" if v is None else str(v)


def best_format(data) -> str:
    k, rows = _uniform_records(data)
    return "tsv" if rows else "json_min"


def emit(data) -> str:
    """Serialize data in the measured-cheapest faithful format."""
    k, rows = _uniform_records(data)
    if rows:
        fields = list(rows[0].keys())
        out = ["\t".join(fields)]
        out += ["\t".join(_scalar(r[f]) for f in fields) for r in rows]
        return "\n".join(out)
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


_FILLER = ["great question", "sure!", "certainly", "i hope this helps", "let me know if",
           "feel free to", "as an ai", "here's", "here is", "i'd be happy to", "of course!"]


def ponytail_flags(text: str):
    """Return the filler phrases present (the ponytail layer says cut these)."""
    low = text.lower()
    return [p for p in _FILLER if p in low]


if __name__ == "__main__":
    uniform = {"users": [{"id": 1, "name": "A", "role": "admin"}, {"id": 2, "name": "B", "role": "user"}]}
    nested = {"cfg": {"db": {"pool": {"min": 2, "max": 10}}, "auth": ["read", "write"]}}
    assert best_format(uniform) == "tsv"
    assert best_format(nested) == "json_min"
    assert emit(uniform).startswith("id\tname\trole")
    assert emit(nested) == '{"cfg":{"db":{"pool":{"min":2,"max":10}},"auth":["read","write"]}}'
    assert ponytail_flags("Great question! Here's the answer.") == ["great question", "here's"]
    print("output-contract self-check OK: TSV for uniform, minified JSON for nested, filler flagged.")
