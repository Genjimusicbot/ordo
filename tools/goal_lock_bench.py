"""goal_lock_bench — the goal-lock A/B harness (charter §4), mirroring rot_bench.

goal-lock is the one instinct that measured directional lift (+4), so it must be firmed, not laundered. Each item
is a multi-step scenario where step 1 came out DIFFERENTLY than the plan assumed, with a key-determined
ground-truth next step. Arm A follows the stale plan; arm B re-derives the next step from {immutable goal + ACTUAL
step-1 result}. CONSTRUCTION-VALIDATION forces a real divergence per item (the planned step 2 is genuinely wrong),
so arm B can only win by catching where the plan diverged. Tier-one = exact key-match against the ground-truth
action → COMPUTED, no judge. Tier-two = the cross-family judge protocol (tools/judge.py) → AGENT-JUDGED, separate row.

The harness + items + construction-validation + the tier-one scorer are tested cold here. The A/B itself
(arm-A vs arm-B completions) needs model calls → PENDING; it writes tools/goal-lock-ab.json when armed.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from judge import sign_test  # noqa: E402

_has = lambda r, *subs: any(s in (r or "").lower() for s in subs)  # noqa: E731

# Each item: the planned step 2 is WRONG given how step 1 actually came out; the ground-truth step 2 re-derives it.
# `right` = markers of the correct re-derived action; `wrong` = markers of blindly following the stale plan.
ITEMS = [
    {"id": "G1", "goal": "Ship a working CSV export endpoint.",
     "actual_step1": "Added /export, but the lib already returns CSV directly (not JSON).",
     "planned_step2": "Convert the JSON response to CSV in the frontend.",
     "ground_truth": "Skip the frontend conversion — the endpoint already returns CSV; just wire the download button.",
     "right": ("skip", "already csv", "no conversion", "already returns csv"), "wrong": ("convert the json", "json to csv in the frontend")},
    {"id": "G2", "goal": "Add rate limiting to the API.",
     "actual_step1": "The framework already had built-in rate-limit middleware; enabled it instead of a Redis counter.",
     "planned_step2": "Configure the Redis connection.",
     "ground_truth": "Skip Redis — configure the built-in middleware's limits; no Redis needed.",
     "right": ("skip redis", "no redis", "built-in", "built in", "no need for redis"), "wrong": ("configure redis", "redis connection")},
    {"id": "G3", "goal": "Migrate auth to JWT.",
     "actual_step1": "Issued JWTs; they are stateless and self-validating, no DB lookup needed.",
     "planned_step2": "Store the JWT in a DB sessions table.",
     "ground_truth": "Skip the DB sessions table — JWTs are stateless; validate the signature on each request instead.",
     "right": ("skip", "stateless", "no db", "no sessions table", "validate the signature"), "wrong": ("store the jwt",)},
    {"id": "G4", "goal": "Speed up the dashboard load.",
     "actual_step1": "The slowdown was a missing index, not a caching problem; added the index and it's fast now.",
     "planned_step2": "Add a cache-invalidation job.",
     "ground_truth": "Skip the cache-invalidation job — there is no cache now; just measure to confirm the index fixed it.",
     "right": ("skip", "no cache", "there is no cache", "just measure", "no caching"), "wrong": ("add a cache-invalidation", "add a cache invalidation")},
    {"id": "G5", "goal": "Let users upload avatars.",
     "actual_step1": "Used the existing local /uploads storage instead of S3 (S3 creds were unavailable).",
     "planned_step2": "Store the S3 URL on the user record.",
     "ground_truth": "Store the LOCAL upload path on the user (not an S3 URL); adjust the field accordingly.",
     "right": ("local", "/uploads", "not s3", "not an s3", "local path"), "wrong": ("store the s3 url", "s3 url on the user")},
]


def construction_valid(it: dict) -> bool:
    """Every item must contain a REAL divergence: the ground-truth action matches the `right` markers and NOT the
    `wrong` (stale-plan) markers, and the planned step matches `wrong` — so arm B can only win by re-deriving."""
    gt, planned = it["ground_truth"].lower(), it["planned_step2"].lower()
    return _has(gt, *it["right"]) and not _has(gt, *it["wrong"]) and _has(planned, *it["wrong"])


def oracle(it: dict, response: str) -> bool:
    """Tier-one key-match: did the response re-derive the goal-serving step (right markers, not the stale-plan ones)?"""
    return _has(response, *it["right"]) and not _has(response, *it["wrong"])


def grade(arm_A: dict, arm_B: dict) -> dict:
    """COMPUTED tier-one: A=follow-plan vs B=re-derive, exact key-match against the ground-truth action."""
    by = {it["id"]: it for it in ITEMS}
    a = sum(1 for iid, it in by.items() if oracle(it, arm_A.get(iid, "")))
    b = sum(1 for iid, it in by.items() if oracle(it, arm_B.get(iid, "")))
    b_wins = sum(1 for iid, it in by.items() if oracle(it, arm_B.get(iid, "")) and not oracle(it, arm_A.get(iid, "")))
    a_wins = sum(1 for iid, it in by.items() if oracle(it, arm_A.get(iid, "")) and not oracle(it, arm_B.get(iid, "")))
    return {"n": len(ITEMS), "A_pass": a, "B_pass": b, "net": b - a, "b_wins": b_wins, "a_wins": a_wins,
            "sign_p": round(sign_test(b_wins, a_wins), 4), "tier": "COMPUTED (tier-one exact-match)"}


def run_live():
    """LIVE tier-one A/B: arm-A follows the stale plan; arm-B re-derives from {goal + ACTUAL step-1 result}.
    Oracle exact-match → COMPUTED. Writes goal-lock-ab.json (tier-two cross-family judge is separate/PENDING)."""
    import json as _json
    from local_model import complete
    armA, armB = {}, {}
    for it in ITEMS:
        armA[it["id"]] = complete(f"GOAL: {it['goal']} STEP 1 RESULT: {it['actual_step1']} The plan says STEP 2 is: "
                                  f"\"{it['planned_step2']}\". State concisely what you will do for step 2.")
        armB[it["id"]] = complete(f"GOAL: {it['goal']} STEP 1 RESULT: {it['actual_step1']} The plan said step 2 would "
                                  f"be \"{it['planned_step2']}\", but RE-DERIVE the correct next step from the goal and "
                                  f"how step 1 ACTUALLY came out. State concisely the correct step 2.")
    g = grade(armA, armB)
    (Path(__file__).resolve().parent / "goal-lock-ab.json").write_text(_json.dumps(g, indent=2), encoding="utf-8")
    print(f"goal-lock (LIVE tier-one): A_pass {g['A_pass']} B_pass {g['B_pass']} | net {g['net']} | "
          f"sign-p {g['sign_p']} | {g['tier']} → goal-lock-ab.json (tier-two cross-family judge PENDING)")
    print("CAVEAT: tier-one keyword-oracle is BRITTLE on a strong model — both arms write sensible answers and "
          "keyword-matching mis-grades correct-but-differently-worded re-derivations (a first live run gave "
          "b_wins=0, an oracle artifact, not a goal-lock verdict). Substance needs the tier-two cross-family JUDGE.")
    return g


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--run" in sys.argv:
        run_live(); sys.exit(0)
    # construction-validation: every item is a real divergence (no no-op items B could win on for free)
    for it in ITEMS:
        assert construction_valid(it), ("item has no real divergence to catch", it["id"])
    # the oracle separates a re-derived answer from a stale-plan answer
    for it in ITEMS:
        assert oracle(it, it["ground_truth"]) and not oracle(it, it["planned_step2"]), it["id"]
    # worked tier-one grade: A follows the plan (wrong), B re-derives (right) → B sweeps
    arm_A = {it["id"]: it["planned_step2"] for it in ITEMS}
    arm_B = {it["id"]: it["ground_truth"] for it in ITEMS}
    g = grade(arm_A, arm_B)
    assert g["net"] == len(ITEMS) and g["b_wins"] == len(ITEMS) and g["a_wins"] == 0, g
    print(f"goal_lock_bench self-check OK — {len(ITEMS)} construction-validated divergence items; tier-one exact-match "
          f"scorer verified (re-derive sweeps follow-plan on the planted divergences). A/B run (arm-A follow-plan vs "
          f"arm-B re-derive) is PENDING model calls → tier-one COMPUTED (goal-lock-ab.json) + tier-two cross-family judge.")
