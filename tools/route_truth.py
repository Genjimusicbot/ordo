"""route_truth — the COMPUTED misroute-cost harness for classifyTask (charter §2).

Replaces the meaningless "100% inter-rater consistency" with a real, deterministic misroute number against an
OUTCOME-pinned ground-truth corpus (tools/route_corpus.jsonl, content-hashed). ASYMMETRIC cost (FrugalGPT's
2-axis objective made concrete): over-spend (STRICT on a true-LIGHT) is a bounded ~1-unit tax; under-verify
(LIGHT on a true-STRICT) is weight 10 AND a HARD-FLOOR violation when the item is irreversible. No judge in the
loop — string-equality to a frozen label — so it is COMPUTED and un-gameable.

Honesty: `ordo_rule` is scored on the corpus's GOLD signals → it measures whether the 5-trigger TAXONOMY is
complete (0 misroute = every STRICT case has a trigger), NOT real-world extraction. The real classifyTask number
(a MODEL extracts the 5 signals from the raw prompt) is PENDING; `keyword_router` is the runnable-now no-model
extraction floor. Run: `python tools/route_truth.py`.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

CORPUS = Path(__file__).resolve().parent / "route_corpus.jsonl"
UNDER_W = 10  # under-verify is 10x an over-spend; irreversible under-verify is a hard-floor breach (∞)


def load():
    items = [json.loads(ln) for ln in CORPUS.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return items, hashlib.sha256(CORPUS.read_bytes()).hexdigest()[:16]


def classify(sig: dict) -> str:
    """The ORDO routing rule (mirror of src/index.js classifyTask): ANY hard signal ⇒ STRICT."""
    return "STRICT" if any(sig.get(k) for k in ("irreversible", "realFork", "longHorizon", "broad", "loadBearing")) else "LIGHT"


# routers: item → LIGHT|STRICT, all deterministic
def ordo_rule(it):     return classify(it["signals"])                          # gold signals → taxonomy completeness
def always_strict(it): return "STRICT"                                         # control-1: 0 under-verify, max over-spend
def length_router(it): return "STRICT" if len(it["prompt"]) > 60 else "LIGHT"  # control-0: the strawman

_KW = ("migrat", "delete", "remove", "send", "email everyone", "deploy", "production", "prod", "all customer",
       "all user", "all client", "all our services", "monorepo", "payment", "billing", "invoice", "schema",
       "credential", "api key", "rewrite", "refactor", "reconcile", "auth cookie", "feature flag", "database",
       "real-time", "websocket", "pricing")


def keyword_router(it):  # a no-model deterministic extractor (runnable-now floor; model-extraction is PENDING)
    p = it["prompt"].lower()
    return "STRICT" if any(k in p for k in _KW) else "LIGHT"


def score(router, items) -> dict:
    over = under = floor = 0
    nL = sum(1 for it in items if it["label"] == "LIGHT")
    nS = sum(1 for it in items if it["label"] == "STRICT")
    for it in items:
        pred, gold = router(it), it["label"]
        if pred == gold:
            continue
        if pred == "STRICT":              # over-spend (tax)
            over += 1
        else:                             # under-verify (dangerous)
            under += 1
            if it["signals"].get("irreversible"):
                floor += 1
    return {"over_spend": over, "over_spend_pct": round(100 * over / max(nL, 1)),
            "under_verify": under, "under_verify_pct": round(100 * under / max(nS, 1)),
            "irreversible_floor_violations": floor, "cost": over * 1 + under * UNDER_W}


ROUTERS = [("ordo_rule (gold signals)", ordo_rule, "COMPUTED — taxonomy completeness"),
           ("keyword_router (no-model)", keyword_router, "COMPUTED — extraction floor"),
           ("length_router (control-0)", length_router, "COMPUTED — strawman"),
           ("always_strict (control-1)", always_strict, "COMPUTED — safe but taxing")]


def report():
    items, h = load()
    print(f"# route_truth — classifyTask misroute on {len(items)} outcome-pinned items (corpus {h}) [COMPUTED]\n")
    print("| router | over-spend% | under-verify% | irrev-floor (must=0) | cost | tier |")
    print("|---|---|---|---|---|---|")
    for name, fn, tier in ROUTERS:
        r = score(fn, items)
        print(f"| {name} | {r['over_spend_pct']}% | {r['under_verify_pct']}% | {r['irreversible_floor_violations']} | {r['cost']} | {tier} |")
    print("\nHonest read: `ordo_rule` on GOLD signals measures 5-trigger TAXONOMY completeness (0 misroute = every "
          "STRICT case has a trigger), NOT real-world extraction. The real classifyTask number (a MODEL extracts the "
          "signals from the raw prompt) is PENDING; `keyword_router` is the runnable-now no-model floor. The cardinal "
          "sin is an under-verify-on-irreversible (hard floor = 0).")
    return items


def run_live():
    """LIVE: the model EXTRACTS the 5 signals from each raw prompt → classify → score vs gold. The misroute rate
    is COMPUTED (arithmetic vs frozen labels) over a model's extraction. Writes route-truth-ab.json."""
    from local_model import complete
    items, h = load()
    SYS = ('Triage a task. Output ONLY a JSON object with 5 booleans, no prose: '
           '{"irreversible":bool,"realFork":bool,"longHorizon":bool,"broad":bool,"loadBearing":bool}. '
           'irreversible=a wrong answer costs more than a re-ask (money/sends/migrations/a claim shipped to a user); '
           'realFork=a real architecture/algorithm/novel-design choice vs one deterministic answer; '
           'longHorizon=>~15-20 tool calls or multi-phase; broad=>5 files or >1 repo; '
           'loadBearing=IDs/contracts/schema/decisions that must survive.')

    def extract(prompt):
        r = complete("TASK: " + prompt, system=SYS)
        try:
            j = json.loads(r[r.find("{"):r.rfind("}") + 1])
            return {k: bool(j.get(k)) for k in ("irreversible", "realFork", "longHorizon", "broad", "loadBearing")}
        except Exception:
            return {}  # extraction failure → LIGHT (the dangerous default; an under-verify if the item is STRICT)

    res = score(lambda it: classify(extract(it["prompt"])), items)
    out = {"router": "classifyTask (model extraction, opus-4-8)", "corpus": h,
           "tier": "COMPUTED scoring over model extraction", **res}
    (Path(__file__).resolve().parent / "route-truth-ab.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"classifyTask (LIVE model extraction): over-spend {res['over_spend_pct']}% | under-verify "
          f"{res['under_verify_pct']}% | irrev-floor {res['irreversible_floor_violations']} (must=0) | cost "
          f"{res['cost']} → route-truth-ab.json  [vs always-strict cost 17, keyword-floor 31]")
    return out


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if "--run" in sys.argv:
        run_live(); sys.exit(0)
    items = report()
    # deterministic self-checks
    o = score(ordo_rule, items)
    assert o["over_spend"] == 0 and o["under_verify"] == 0, ("TAXONOMY INCOMPLETE — a STRICT item has no trigger", o)
    assert score(length_router, items)["under_verify"] > 0, "the length strawman must under-verify on short-but-hard items"
    a = score(always_strict, items)
    assert a["under_verify"] == 0 and a["over_spend"] > 0, "always-strict = 0 under-verify, positive over-spend"
    print("\nroute_truth self-check OK — taxonomy complete on the corpus (incl. 12 adversarial); strawmen misroute as predicted.")
