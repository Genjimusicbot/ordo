"""tokcost — measure the real token cost of ORDO symbols (the anti-shortcut tool).

Design Law 1: a symbol is admitted to the alphabet only if its MEASURED token cost is <= the phrase
it replaces. "One glyph = one token" is false for many exotic glyphs (BPE shatters them). We measure
on OpenAI tiktoken (cl100k_base = GPT-3.5/4, o200k_base = GPT-4o/o1) as PROXIES; Claude/Gemini
tokenizers are proprietary and may differ (see DISCLAIMERS).

Usage:
  python tools/tokcost.py                 # measure the built-in candidate pool + print a table
  python tools/tokcost.py "Σ" "explain"   # measure specific strings
"""
from __future__ import annotations

import sys
import tiktoken

_ENC = {name: tiktoken.get_encoding(name) for name in ("cl100k_base", "o200k_base")}


def cost(s: str) -> dict:
    return {name: len(enc.encode(s)) for name, enc in _ENC.items()}


def net_savings(ordo: str, english: str) -> dict:
    o, e = cost(ordo), cost(english)
    return {name: {"ordo": o[name], "english": e[name], "saved": e[name] - o[name],
                   "ratio": round(e[name] / o[name], 2) if o[name] else None} for name in _ENC}


# Candidate pool: mnemonic glyphs to test for the directive alphabet. Grouped only for readability.
CANDIDATES = {
    "greek": list("ΣΔΠΦΨΩΛΘΞΓαβγδελμνπρστφχψω"),
    "math": list("∑∏∫∂∇√∞≈≠≡≤≥±×÷∈∀∃∴∵⇒⇔→←↔↦⊕⊗⊙⊳⊲⊤⊥¬∧∨∝∅"),
    "arrows": list("↑↓↹⇄⇅⟲⟳↻⇶⇡⇣"),
    "marks": list("✓✗✎✂✦★☆◆◇●○■□▶◀※§¶†‡№℮ℹ⌘⌥⎇⏎⌫⚙⚑⌁⍰⊞⊟"),
    "runes": list("ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛊᛏᛒᛖᛗᛚᛜᛞᛟ"),
    "misc": list("¶◊※⁂✱❖➤▷◈⟐⟡⊙⊚"),
}

# Some directives we want, with the verbose English they must beat (for net-savings sanity).
DIRECTIVE_TARGETS = {
    "summarize": "summarize the following",
    "explain": "explain the following",
    "list": "list the",
    "compare": "compare the following",
    "translate": "translate the following",
    "rewrite": "rewrite the following",
    "fix": "find and fix the bug in",
    "refactor": "refactor the following code",
    "critique": "critique the following",
    "rate": "rate the following from 1 to 10",
    "extract": "extract the key points from",
    "plan": "make a step by step plan for",
    "simplify": "explain this simply",
    "expand": "expand on the following",
    "shorten": "make the following shorter",
    "verify": "verify the following is correct",
}


def main(argv):
    if argv:
        for s in argv:
            c = cost(s)
            print(f"{s!r:8}  cl100k={c['cl100k_base']}  o200k={c['o200k_base']}")
        return 0
    print("=== candidate glyph token costs (cl100k / o200k) ===")
    one_token = []
    for group, glyphs in CANDIDATES.items():
        cheap = []
        for g in glyphs:
            c = cost(g)
            tag = "" if (c["cl100k_base"] == 1 and c["o200k_base"] == 1) else f"  ({c['cl100k_base']}/{c['o200k_base']})"
            if c["cl100k_base"] == 1 and c["o200k_base"] == 1:
                cheap.append(g)
                one_token.append(g)
            else:
                cheap.append(f"{g}{tag}")
        print(f"\n{group}: " + " ".join(cheap))
    print(f"\n=== 1-token in BOTH (admittable, {len(one_token)}): " + " ".join(one_token))
    print("\n=== directive net-savings sanity (English phrase these must beat) ===")
    for d, eng in DIRECTIVE_TARGETS.items():
        c = cost(eng)
        print(f"  {d:10} <- \"{eng}\"  english={c['cl100k_base']}/{c['o200k_base']} tokens (a 1-token glyph saves that minus 1)")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # glyphs print on a default Windows console
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
