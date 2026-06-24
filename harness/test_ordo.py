"""Harness CI — run with pytest OR `python harness/test_ordo.py`. The round-trip + parse gate (C8)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ordo import parse, decode, DIRECTIVES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIR_WORDS = {  # first word of each directive's English, for coverage checks
    "σ": "summarize", "ε": "explain", "δ": "define", "α": "analyze", "χ": "critique", "ρ": "rewrite",
    "τ": "translate", "π": "plan", "λ": "code", "γ": "generate", "β": "brainstorm", "μ": "compare",
    "φ": "fix", "ν": "refactor", "★": "rate", "※": "extract", "§": "outline", "●": "list", "↓": "shorten",
}


def test_ast_slots():
    a = parse("σ文3列简心金业通¬序")[0]
    assert a["directives"] == ["summarize"]
    assert a["operand"] == "the following text"
    assert a["quantity"] == "3 bullet points"
    assert a["length"] == "concisely"
    assert "financial" in (a["focus"] or "")
    assert a["audience"] == "a non-expert"
    assert any("preamble" in c for c in a["constraints"])


def test_dual_use_码():
    # operand position -> code operand; format position -> code-only
    assert parse("ν码")[0]["operand"] == "the following code"
    assert parse("λ文码")[0]["format"] == "as code only"


def test_constraints_polarity():
    a = parse('ν码×"duplication"据"behavior"')[0]
    cs = " ".join(a["constraints"])
    assert "remove duplication" in cs and "preserve behavior" in cs  # × != 据


def test_pipe_chain():
    stages = parse("β5名|★")
    assert len(stages) == 2
    assert stages[0]["directives"] == ["brainstorm"] and stages[0]["quantity"] == "5 names"
    assert stages[1]["directives"] == ["rate from 1 to 10"]


def test_epistemic_and_format():
    a = parse("α上信源表")[0]
    assert "as a table (TSV)" == a["format"]
    assert any("certainty" in e for e in a["epistemic"]) and any("cite" in e for e in a["epistemic"])


def test_unknown_glyph_graceful():
    # a glyph in no table must not crash and must be preserved as literal
    a = parse("σ☃文")[0]
    assert a["directives"] == ["summarize"]
    assert "☃" in a["literals"]


def test_units():
    assert parse("ρ此80字")[0]["quantity"] == "80 words"
    assert parse("↓此3行")[0]["quantity"] == "3 sentences"
    assert parse("σ文2段")[0]["quantity"] == "2 paragraphs"


def test_roundtrip_covers_benchmark():
    """Every glyph-ORDO benchmark line decodes to text carrying its directive (round-trip coverage)."""
    lines = [l for l in (ROOT / "tests" / "prompts-ordo.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(lines) == 20
    misses = []
    for s in lines:
        eng = decode(s).lower()
        lead = s[0]
        word = DIR_WORDS.get(lead)
        if word and word not in eng:
            misses.append((s, word))
    assert not misses, f"directive lost in decode: {misses}"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} harness tests passed.")
