"""judge.py — the foolproof blind-judge protocol (the gate every AGENT-JUDGED number must pass).

Five locks (docs/IMPROVEMENT-CHARTER.md §1, grounded in MT-Bench 2306.05685): (1) cross-family panel, (2)
position-swap conservative, (3) blind + length-control, (4) real-frozen corpus, (5) stats + pre-registration.
The STATS here are COMPUTED-now (pure stdlib, tested cold against synthetic votes); the cross-family MODEL judging
is PENDING (needs live API, blocked in this sandbox) and writes tools/judge-ab.json when armed. Governing rule:
a number prints WIN only if its Wilson 95% interval excludes 0.5 — an n=6 near-tie prints DIRECTIONAL, never WIN.
"""
from __future__ import annotations

import math
from collections import Counter
from typing import List, Tuple

Z95 = 1.959963984540054  # z for a 95% two-sided interval


def wilson(wins: int, n: int, z: float = Z95) -> Tuple[float, float]:
    """Wilson score 95% interval for a proportion wins/n. Returns (lo, hi)."""
    if n == 0:
        return (0.0, 1.0)
    p = wins / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (max(0.0, c - h), min(1.0, c + h))


def sign_test(wins: int, losses: int) -> float:
    """Two-sided exact binomial sign-test p over the non-tie pairs (H0: win-rate = 0.5)."""
    n = wins + losses
    if n == 0:
        return 1.0
    k = max(wins, losses)
    tail = sum(math.comb(n, i) for i in range(k, n + 1)) * (0.5 ** n)
    return min(1.0, 2 * tail)


def cohen_kappa(a: List, b: List) -> float:
    """Cohen's kappa for two raters' aligned categorical labels (judge-vs-human gate, MT-Bench §4.2)."""
    n = len(a)
    if n == 0 or n != len(b):
        return 0.0
    cats = set(a) | set(b)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def resolve_swap(order1_winner: str, order2_winner: str) -> str:
    """Lock 2 (conservative): a side WINS only if it wins in BOTH orders; else TIE. Args are the SIDE
    ('ON'|'OFF'), not the slot — that is what removes position bias. Returns 'ON'|'OFF'|'tie'."""
    return order1_winner if (order1_winner == order2_winner and order1_winner in ("ON", "OFF")) else "tie"


def panel_majority(votes: List[str]) -> str:
    """Item verdict = strict majority of the swap-resolved judge votes; no majority → tie."""
    if not votes:
        return "tie"
    top, n = Counter(votes).most_common(1)[0]
    return top if n * 2 > len(votes) else "tie"


def assert_cross_family(judge_family: str, forbidden: List[str]) -> None:
    """Lock 1: a judge whose family overlaps the generator/profile family may NOT vote (MT-Bench self-preference
    +10–25pp). Raises so the harness fails closed instead of emitting a self-judged win."""
    if judge_family.lower() in {f.lower() for f in forbidden}:
        raise ValueError(f"self-judge forbidden: judge_family={judge_family!r} overlaps {forbidden} — "
                         "log it as a 'self' bias-gap column, never a vote")


def verdict(wins: int, ties: int, losses: int) -> dict:
    """Lock 5: WIN only if the Wilson 95% interval on the non-tie pairs excludes 0.5; else DIRECTIONAL/LOSS/NULL.
    Tier is AGENT-JUDGED (a model judged the pairs) — never COMPUTED."""
    n_eff = wins + losses
    lo, hi = wilson(wins, n_eff)
    if n_eff == 0:
        decision = "NULL (all ties)"
    elif lo > 0.5:
        decision = "WIN"
    elif hi < 0.5:
        decision = "LOSS"
    else:
        decision = "DIRECTIONAL (interval straddles 0.5)"
    return {"wins": wins, "ties": ties, "losses": losses, "n_eff": n_eff,
            "wilson95": [round(lo, 3), round(hi, 3)], "sign_p": round(sign_test(wins, losses), 4),
            "decision": decision, "tier": "AGENT-JUDGED"}


if __name__ == "__main__":
    # goal-lock's 8W/0T/4L: the interval straddles 0.5 → DIRECTIONAL, NOT a WIN (this is what de-headlines it)
    g = verdict(8, 0, 4)
    assert g["decision"].startswith("DIRECTIONAL"), g
    assert g["wilson95"][0] < 0.5 < g["wilson95"][1], g          # ~[0.39, 0.86]
    # a powered result clears the bar
    assert verdict(40, 0, 10)["decision"] == "WIN"
    assert verdict(0, 6, 0)["decision"].startswith("NULL")
    assert verdict(4, 1, 7)["decision"] in ("LOSS", "DIRECTIONAL (interval straddles 0.5)")  # divergence
    # sign-test: a coin-flip is p=1, a sweep is tiny
    assert abs(sign_test(5, 5) - 1.0) < 1e-9 and sign_test(10, 0) < 0.01
    # swap (conservative): ON wins only if both orders agree
    assert resolve_swap("ON", "ON") == "ON" and resolve_swap("ON", "OFF") == "tie"
    # panel: strict majority, else tie
    assert panel_majority(["ON", "ON", "OFF"]) == "ON" and panel_majority(["ON", "OFF", "tie"]) == "tie"
    # kappa: perfect agreement = 1
    assert abs(cohen_kappa(["A", "B", "A", "B"], ["A", "B", "A", "B"]) - 1.0) < 1e-9
    # cross-family lock fails closed on a self-judge
    try:
        assert_cross_family("claude", ["claude"]); raise AssertionError("cross-family lock should have raised")
    except ValueError:
        pass
    print(f"judge.py self-check OK — goal-lock 8/0/4 → {g['decision']} {g['wilson95']} (DIRECTIONAL, not WIN). "
          "Wilson/sign-test/kappa/swap/panel + cross-family lock all green. Cross-family run → judge-ab.json (PENDING).")
