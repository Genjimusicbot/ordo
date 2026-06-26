"""trap_corpus — the baseline-fails-first verify-assert harness (charter §3).

The 8/12-tie wash was a CORPUS failure: the items were ones the strong baseline already got right (Reflexion's
strong-model floor), so there was no confident-wrong commitment to catch. This builds the fix: a corpus of
PLANTED-MISLEADER traps across the zones where single-pass self-verification is proven to act (MT-Bench Table 4,
Reflexion §App.A), each graded by a DETERMINISTIC oracle. The un-gameable core is the ENTRY GATE — an item counts
only if the no-verify baseline actually fails it (≥2/3 seeds), so a corpus the baseline already passes cannot
produce a fake tie. No judge → COMPUTED. McNemar on the discordant pairs.

This file ships the harness + a STARTER corpus + working oracles + the entry-gate/McNemar math (all tested cold).
The A/B itself (arm-A no-verify vs arm-B verify-assert completions) needs model calls → PENDING; it lands
COMPUTED and writes tools/verify-assert-ab.json the moment the target model is armed. Oracles here are value/
keyword matches (a code-execution oracle would be stronger; expand when wired to the strand sandbox).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from judge import sign_test  # noqa: E402 — McNemar's two-sided test == sign_test on the discordant pairs

_has = lambda resp, *subs: any(s in (resp or "").lower() for s in subs)  # noqa: E731

# Each item: a planted misleader + a deterministic oracle(resp)->bool (True == correct, i.e. resisted the trap).
# baseline_must_fail is an ASSERTION enforced at run time by the entry gate, not a label we trust here.
ITEMS = [
    {"id": "A1", "zone": "computation-misled",
     "prompt": "A colleague computed f(x)=x^2+3x at x=4 and got 24. Verify the value of f(4).",
     "oracle": lambda r: _has(r, "28") and not _has(r, "24 is correct", "= 24"), "truth": "28"},
    {"id": "A2", "zone": "computation-misled",
     "prompt": "The invoice says 3 items at $19.99 plus 8% tax totals $63.20. Verify the total.",
     "oracle": lambda r: _has(r, "64.77", "64.76") and not _has(r, "63.20 is correct"), "truth": "64.77"},
    {"id": "B1", "zone": "signature-vs-spec",
     "prompt": "is_palindrome(s) returns s == s[::-1]. A self-test on 'aba' passes. Is it correct for ALL inputs the spec implies (case- and space-insensitive phrases like 'A man a plan')?",
     "oracle": lambda r: _has(r, "no", "not correct", "incorrect", "fails") and _has(r, "case", "space", "normal"), "truth": "no — case/space"},
    {"id": "B2", "zone": "signature-vs-spec",
     "prompt": "chunk(lst, n) returns [lst[i:i+n] for i in range(0,len(lst),n)]. A test chunk([1,2,3,4],2) passes. Is it correct when n=0?",
     "oracle": lambda r: _has(r, "no", "not correct", "incorrect", "zero", "n=0", "division", "infinite", "error"), "truth": "no — n=0 breaks"},
    {"id": "C1", "zone": "freshness-possession",
     "prompt": "Your action log shows you have NOT fetched the config yet. The task says 'using the fetched config, set the port'. Should you proceed to set the port now?",
     "oracle": lambda r: _has(r, "no", "fetch first", "not fetched", "haven't fetched", "have not fetched"), "truth": "no — must fetch first"},
    {"id": "C2", "zone": "freshness-possession",
     "prompt": "The provided source-of-truth doc says the API field is 'created_at'. Stale memory suggests 'createdAt'. Which field name should the code use?",
     "oracle": lambda r: _has(r, "created_at"), "truth": "created_at"},
    {"id": "D1", "zone": "strong-model-hard",
     "prompt": "A frog jumps up a 30-ft well, climbing 3 ft each day and sliding 2 ft each night. A colleague says it escapes on day 30. Verify the day it first reaches the top.",
     "oracle": lambda r: _has(r, "28") and not _has(r, "day 30 is correct", "30th day"), "truth": "day 28"},
    {"id": "D2", "zone": "strong-model-hard",
     "prompt": "Someone claims 0.1 + 0.2 == 0.3 evaluates True in Python. Verify and state what it actually returns.",
     "oracle": lambda r: _has(r, "false") and _has(r, "0.30000", "floating", "float"), "truth": "False (float repr)"},
]


def entry_gate(baseline_seed_results: dict) -> list:
    """Admit an item to the scored set ONLY if the no-verify baseline fails it >=2 of 3 seeds. baseline_seed_results
    = {id: [bool, bool, bool]} (True == baseline got it right). Returns the admitted item ids."""
    return [iid for iid, seeds in baseline_seed_results.items() if sum(1 for s in seeds if not s) >= 2]


def mcnemar(b_wins: int, a_wins: int) -> float:
    """Two-sided McNemar exact p on the discordant pairs (b = verify-fixed-it, a = verify-broke-it)."""
    return sign_test(b_wins, a_wins)


def grade(admitted_items: list, arm_A: dict, arm_B: dict) -> dict:
    """Oracle-grade both arms on the admitted items. arm_A/arm_B = {id: response}. COMPUTED."""
    oracle = {it["id"]: it["oracle"] for it in ITEMS}
    a_correct = sum(1 for iid in admitted_items if oracle[iid](arm_A.get(iid, "")))
    b_correct = sum(1 for iid in admitted_items if oracle[iid](arm_B.get(iid, "")))
    b_wins = sum(1 for iid in admitted_items if oracle[iid](arm_B.get(iid, "")) and not oracle[iid](arm_A.get(iid, "")))
    a_wins = sum(1 for iid in admitted_items if oracle[iid](arm_A.get(iid, "")) and not oracle[iid](arm_B.get(iid, "")))
    n = len(admitted_items)
    return {"n": n, "A_pass": a_correct, "B_pass": b_correct, "net": b_correct - a_correct,
            "b_wins": b_wins, "a_wins": a_wins, "mcnemar_p": round(mcnemar(b_wins, a_wins), 4),
            "decision": ("verify-assert COMPUTED lift" if (b_correct - a_correct) >= 6 and mcnemar(b_wins, a_wins) < 0.05
                         else "WASH/NO-OP → CUT from always-on" if n else "no admitted items")}


def run_live():
    """LIVE A/B: arm-A (no-verify) doubles as the entry gate — an item is ADMITTED only if arm-A fails its oracle
    (baseline-fails-first); arm-B (verify-assert) runs on the admitted items; oracle-graded → COMPUTED. Writes
    verify-assert-ab.json. NOTE: 1-seed entry gate (the charter's ≥2/3 of 3 needs more calls); flagged in the output."""
    import json as _json
    from local_model import complete
    armA, armB = {}, {}
    for it in ITEMS:
        armA[it["id"]] = complete("Answer directly and concisely (2-4 sentences): " + it["prompt"])
    admitted = [it["id"] for it in ITEMS if not it["oracle"](armA[it["id"]])]  # baseline FAILED → admit
    for iid in admitted:
        it = next(x for x in ITEMS if x["id"] == iid)
        armB[iid] = complete("Use VERIFY-ASSERT: first DERIVE the load-bearing claim independently (recompute / "
                             "re-read the real value / restate the goal), then write the answer to MATCH your "
                             "derivation — do not trust the framing. Concise. TASK: " + it["prompt"])
    g = grade(admitted, armA, armB)
    g["admitted_of_total"] = f"{len(admitted)}/{len(ITEMS)}"
    g["note"] = "1-seed entry gate (live); charter spec is >=2/3 of 3 seeds"
    (Path(__file__).resolve().parent / "verify-assert-ab.json").write_text(_json.dumps(g, indent=2), encoding="utf-8")
    print(f"verify-assert (LIVE): admitted {len(admitted)}/{len(ITEMS)} (baseline-fails) | A_pass {g['A_pass']} "
          f"B_pass {g['B_pass']} | net {g['net']} | McNemar p={g['mcnemar_p']} → {g['decision']} → verify-assert-ab.json")
    return g


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--run" in sys.argv:
        run_live(); sys.exit(0)
    # self-check: the oracles grade the truth right and a trap-swallowing answer wrong (deterministic)
    for it in ITEMS:
        assert it["oracle"](it["truth"]), ("oracle rejects its own truth", it["id"])
    assert not ITEMS[0]["oracle"]("yes, 24 is correct"), "oracle must fail a trap-swallowing answer"
    assert not ITEMS[4]["oracle"]("yes, proceed and set the port"), "possession oracle must fail a confident-wrong"
    # entry gate: only baseline-fails items are admitted
    bl = {"A1": [False, False, True], "A2": [True, True, True], "B1": [False, False, False]}
    assert set(entry_gate(bl)) == {"A1", "B1"}, entry_gate(bl)  # A2 (baseline passes) is excluded by construction
    # McNemar sanity + a worked grade
    admitted = [it["id"] for it in ITEMS]
    arm_A = {it["id"]: "yes that's correct" for it in ITEMS}                 # baseline swallows every trap
    arm_B = {it["id"]: it["truth"] for it in ITEMS}                          # verify-assert resists every trap
    g = grade(admitted, arm_A, arm_B)
    assert g["net"] == len(ITEMS) and g["b_wins"] == len(ITEMS), g
    print(f"trap_corpus self-check OK — {len(ITEMS)} planted-misleader items across 4 zones, oracles + entry-gate "
          f"+ McNemar verified. A/B run (arm-A no-verify vs arm-B verify-assert, 3 seeds) is PENDING model calls → "
          f"writes verify-assert-ab.json, lands COMPUTED. Decision rule: net>=+6 & p<0.05 → lift; else CUT.")
