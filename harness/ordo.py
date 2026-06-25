"""ordo — the harness: a deterministic ORDO-G decoder (the measurement instrument).

parse(s) -> AST (dict of slots); to_english(ast) -> the expanded instruction. Table-driven, one
left-to-right scan, no model in the loop. Each glyph is classified by which table it belongs to (the
one-parse guarantee); the two deliberate dual-use glyphs (码 operand/format, 段 format/unit) resolve by
position. Unknown glyphs degrade to inline literal (never error). This is the auto-decode the harness
gives you instead of relying on the model to follow ORDO.md by hand.

# ponytail: a table-driven scanner, not a full PEG engine — the grammar is regular enough that role =
# table-membership + a couple of positional rules. Swap for a PEG lib only if the grammar grows context-
# sensitive (it is not today).
"""
from __future__ import annotations

DIRECTIVES = {
    "σ": "summarize", "ε": "explain", "δ": "define", "α": "analyze", "χ": "critique", "ρ": "rewrite",
    "τ": "translate", "π": "make a step-by-step plan for", "λ": "write code for", "γ": "generate",
    "β": "brainstorm", "μ": "compare", "φ": "find and fix the bug in", "ν": "refactor",
    "ω": "give the final answer for", "→": "continue", "↑": "expand on", "↓": "shorten",
    "★": "rate from 1 to 10", "☆": "give a worked example of", "※": "extract verbatim from",
    "§": "outline", "●": "list", "■": "classify", "×": "delete", "¬": "exclude", "±": "give variations of",
    "†": "verify",
}
OPERAND = {"文": "the following text", "码": "the following code", "话": "the conversation so far",
           "上": "the above", "此": "this / the current selection", "网": "the URL that follows",
           "源": "the following data"}
LENGTH = {"↓": "in tl;dr form", "简": "concisely", "全": "exhaustively", "↑": "in expanded detail"}
FORMAT = {"列": "as bullet points", "表": "as a table (TSV)", "构": "as minified JSON", "段": "as prose",
          "图": "as a diagram", "码": "as code only", "标": "as markdown"}
UNIT = {"字": "words", "行": "sentences", "段": "paragraphs", "分": "minutes", "名": "names", "项": "items",
        "步": "steps", "页": "pages", "节": "sections", "列": "bullet points"}
FOCUS_VAL = {"金": "the financial figures", "码": "the code", "题": "the key problem"}
AUD = {"通": "a non-expert", "专": "an expert", "民": "the general public"}
TONE = {"正": "a formal", "友": "a friendly", "反": "a casual", "软": "a gentle"}
CONSTRAINT = {"¬": "do not include", "加": "must include", "只": "restrict to only", "×": "remove",
              "据": "preserve"}
CVAL = {"序": "any preamble", "名": "names", "码": "code"}
EPI = {"信": "mark your certainty for each claim", "源": "cite your sources",
       "?": "flag anything you are unsure of", "确": "state only what you can verify",
       "†": "fact-check before answering"}
FOCUS_TAG, AUD_TAG, TONE_TAG = "心", "业", "调"
CTAGS = set(CONSTRAINT)


def _tokens(s: str):
    """Tokenize: quoted literals, @files, ISO/upper runs, numbers, single glyphs."""
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '"':
            j = s.find('"', i + 1)
            j = n if j == -1 else j
            out.append(("LIT", s[i + 1:j])); i = j + 1
        elif c == "@":
            j = i + 1
            while j < n and s[j] not in OPERAND and s[j] not in "|>\"" and s[j] not in CTAGS:
                j += 1
            out.append(("FILE", s[i + 1:j])); i = j
        elif c.isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            out.append(("NUM", s[i:j])); i = j
        elif c.isascii() and c.isupper():
            j = i
            while j < n and s[j].isascii() and (s[j].isupper() or s[j] == s[j]) and s[j].isalpha():
                j += 1
            out.append(("CODE", s[i:j])); i = j
        elif c in "|>()":
            out.append(("OP", c)); i += 1
        elif c.isspace():
            i += 1
        else:
            out.append(("G", c)); i += 1
    return out


def _parse_stage(toks):
    ast = {"directives": [], "operand": None, "length": None, "format": None, "quantity": None,
           "focus": None, "audience": None, "tone": None, "language": None, "constraints": [],
           "epistemic": [], "literals": []}
    i, started = 0, False
    # leading directives (until first non-directive)
    while i < len(toks) and toks[i][0] == "G" and toks[i][1] in DIRECTIVES and not started:
        ast["directives"].append(DIRECTIVES[toks[i][1]]); i += 1
    while i < len(toks):
        kind, val = toks[i]
        nxt = toks[i + 1] if i + 1 < len(toks) else None
        if kind == "LIT":
            if ast["operand"] is None and not ast["constraints"]:
                ast["operand"] = f'"{val}"'
            else:
                ast["literals"].append(val)
        elif kind == "FILE":
            ast["operand"] = f"the file {val}"
        elif kind == "CODE":
            ast["language"] = val  # ISO / target language
        elif kind == "NUM":
            unit = UNIT.get(nxt[1]) if nxt and nxt[0] == "G" and nxt[1] in UNIT else "items"
            if nxt and nxt[0] == "G" and nxt[1] in UNIT:
                i += 1
            ast["quantity"] = f"{val} {unit}"
        elif kind == "OP":
            pass  # | > ( ) handled at the chain level
        elif kind == "G":
            g = val
            if g in OPERAND and ast["operand"] is None and not ast["constraints"]:
                # 码 operand only when no operand yet and right after directive region
                ast["operand"] = OPERAND[g]
            elif g in LENGTH:
                ast["length"] = LENGTH[g]
            elif g == "段" and ast["operand"] is not None:
                ast["format"] = FORMAT["段"]
            elif g in FORMAT and not (g == "码" and ast["operand"] is None):
                ast["format"] = FORMAT[g]
            elif g == FOCUS_TAG:
                if nxt and nxt[0] == "LIT":
                    ast["focus"] = nxt[1]; i += 1
                elif nxt and nxt[0] == "G" and nxt[1] in FOCUS_VAL:
                    ast["focus"] = FOCUS_VAL[nxt[1]]; i += 1
                else:
                    ast["focus"] = "the key part"
            elif g == AUD_TAG:
                if nxt and nxt[0] == "G" and nxt[1] in AUD:
                    ast["audience"] = AUD[nxt[1]]; i += 1
                else:
                    ast["audience"] = "a general reader"
            elif g == TONE_TAG:
                if nxt and nxt[0] == "G" and nxt[1] in TONE:
                    ast["tone"] = TONE[nxt[1]]; i += 1
                else:
                    ast["tone"] = "a neutral"
            elif g in CONSTRAINT:
                if nxt and nxt[0] == "LIT":
                    ast["constraints"].append(f"{CONSTRAINT[g]} {nxt[1]}"); i += 1
                elif nxt and nxt[0] == "G" and nxt[1] in CVAL:
                    ast["constraints"].append(f"{CONSTRAINT[g]} {CVAL[nxt[1]]}"); i += 1
                elif nxt and nxt[0] == "G" and nxt[1] in FORMAT and g == "只":
                    ast["format"] = FORMAT[nxt[1]]; i += 1
                else:
                    ast["constraints"].append(CONSTRAINT[g])
            elif g in EPI:
                ast["epistemic"].append(EPI[g])
            elif g in DIRECTIVES:
                ast["directives"].append(DIRECTIVES[g])
            else:
                ast["literals"].append(g)  # unknown glyph -> literal (graceful)
        started = True
        i += 1
    return ast


def parse(s: str):
    """Return a list of stage-ASTs (one per `|` pipe stage)."""
    stages, cur = [], []
    for t in _tokens(s):
        if t == ("OP", "|"):
            stages.append(cur); cur = []
        else:
            cur.append(t)
    stages.append(cur)
    return [_parse_stage(st) for st in stages]


def _stage_english(a):
    verb = " and ".join(a["directives"]) or "respond to"
    parts = [verb]
    op = a["operand"] or "the following"
    parts.append(op)
    if a["quantity"]:
        parts.append("in " + a["quantity"])
    if a["format"]:
        parts.append(a["format"])
    if a["length"]:
        parts.append(a["length"])
    if a["focus"]:
        parts.append("focusing on " + a["focus"])
    if a["audience"]:
        parts.append("for " + a["audience"])
    if a["tone"]:
        parts.append("in " + a["tone"] + " tone")
    if a["language"]:
        parts.append("into " + a["language"])
    s = " ".join(parts)
    extra = a["constraints"] + ([("also " + l) for l in a["literals"]] if a["literals"] else [])
    if extra:
        s += "; " + "; ".join(extra)
    if a["epistemic"]:
        s += "; " + ", ".join(a["epistemic"])
    return s


def to_english(stages) -> str:
    return "; then ".join(_stage_english(a) for a in stages)


def decode(s: str) -> str:
    return to_english(parse(s))


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # glyphs print on a default Windows console
    except Exception:
        pass
    cases = {
        "σ文3列简心金业通¬序": ["summarize", "3 bullet points", "financial", "non-expert", "preamble"],
        "τ话SV调正": ["translate", "conversation", "SV", "formal"],
        "α上信源表": ["analyze", "the above", "table", "certainty", "cite"],
        "β5名|★": ["brainstorm", "5 names", "then", "rate from 1 to 10"],
        "ν码×\"duplication\"据\"behavior\"加\"type hints\"": ["refactor", "remove duplication", "preserve behavior", "must include type hints"],
        "※源\"dates, people\"构": ["extract verbatim", "JSON", "dates, people"],
    }
    ok = 0
    for s, expect in cases.items():
        eng = decode(s)
        miss = [e for e in expect if e.lower() not in eng.lower()]
        status = "OK " if not miss else "MISS " + str(miss)
        print(f"[{status}] {s}\n    -> {eng}")
        ok += not miss
    # graceful: unknown glyph must not crash
    decode("σ☃文")
    print(f"\n{ok}/{len(cases)} decode cases carried all key terms; unknown-glyph handled gracefully.")
    assert ok >= len(cases) - 1, "too many decode misses"
