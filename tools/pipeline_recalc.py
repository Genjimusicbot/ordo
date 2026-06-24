"""pipeline_recalc — the total token saving across all three layers, pool-weighted (not additive).

Layers act on different token pools (inbound context vs the command vs the output), so the total is a
weighted blend, dominated by whichever pool is largest (usually inbound on agent turns). All per-layer
reductions below are MEASURED in this repo; the pool sizes model a realistic coding-agent turn. Adjust
the mix to your workload.
"""
from __future__ import annotations

# measured per-content inbound reductions (take-best of headroom vs our TSV/whitespace, this repo)
INBOUND = {
    "logs/tool-output": (3000, 0.90),   # headroom sampling (lossy, CCR-retrievable) — its sweet spot
    "structured JSON":  (1500, 0.55),   # our TSV (lossless) — beats base-headroom's noop
    "code":             (2000, 0.07),   # builtin whitespace; headroom CodeCompressor noop'd on base
    "prose docs":       (1500, 0.00),   # ML prose (Kompress) didn't engage on base; lossy + modest anyway
}
COMMAND = (22, 0.32)    # ORDO-G readable grammar (lossless, decode 2.00/2)
OUTPUT = (300, 0.77)    # ponytail (lossless filler cut); format-by-shape stacks where structured


def blend(pools):
    before = sum(b for b, _ in pools)
    after = sum(b * (1 - r) for b, r in pools)
    return before, after, (before - after) / before if before else 0


def main():
    print("=== INBOUND (context the model READS) ===")
    for name, (b, r) in INBOUND.items():
        print(f"  {name:18} {b:5} -> {round(b*(1-r)):5}  ({int(r*100):3}%)")
    ib_before, ib_after, ib_r = blend(list(INBOUND.values()))
    print(f"  {'inbound blended':18} {ib_before:5} -> {round(ib_after):5}  ({int(ib_r*100):3}%)")

    pools = [(ib_before, ib_r), COMMAND, OUTPUT]
    labels = ["inbound (headroom + TSV)", "command (ORDO-G)", "output (ponytail)"]
    print("\n=== FULL TURN (pool-weighted) ===")
    for (b, r), lab in zip(pools, labels):
        print(f"  {lab:26} {b:5} -> {round(b*(1-r)):5}  ({int(r*100):3}%)")
    tb, ta, tr = blend(pools)
    print(f"  {'TOTAL':26} {round(tb):5} -> {round(ta):5}  ({tr*100:.0f}% combined)")

    # log/tool-heavy turn (the common agent case): inbound dominated by redundant context
    heavy = [(9000, 0.88), COMMAND, OUTPUT]
    _, _, hr = blend(heavy)
    print(f"\nlog/tool-heavy turn (inbound 88%): {hr*100:.0f}% combined — inbound dominates, total approaches the inbound rate")
    # prose/doc-library turn (our omni-wiki case): inbound is dense prose (compresses poorly + lossy)
    libturn = [(6000, 0.10), COMMAND, OUTPUT]
    _, _, lr = blend(libturn)
    print(f"dense-prose-library turn (inbound 10%): {lr*100:.0f}% combined — inbound resists; the win shifts to output + the novel levers (relevance-gate, glossary-inward, JIT)")


if __name__ == "__main__":
    main()
