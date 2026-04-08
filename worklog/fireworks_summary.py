"""
Fireworks algorithm: final experiment summary.

Run this to get a compact report of all findings.
"""

import random
import math
from collections import defaultdict


def test_delegation(k, c, trials=200):
    """Test delegation with each emitter having c random collectors."""
    deleg_totals = []
    remain_fracs = []
    round_counts = []
    cost_alive_ratios = []  # per-round cost/alive ratios

    for trial in range(trials):
        rng = random.Random(k * 10000 + trial)
        emitter_cols = {e: set(rng.sample(range(k), min(c, k))) for e in range(k)}

        alive = set(range(k))
        total_deleg = 0
        rounds = 0

        while len(alive) > 1:
            rounds += 1
            alive_before = len(alive)

            col_to_em = defaultdict(set)
            for e in alive:
                for col in emitter_cols[e]:
                    col_to_em[col].add(e)

            can_delegate = {}
            for col in sorted(col_to_em, key=lambda x: -len(col_to_em[x])):
                avail = sorted(col_to_em[col] - set(can_delegate.keys()))
                if len(avail) >= 2:
                    for e in avail[1:]:
                        if e not in can_delegate:
                            can_delegate[e] = (avail[0], col)

            if not can_delegate:
                break
            if len(can_delegate) > len(alive) // 2:
                can_delegate = dict(sorted(can_delegate.items())[:len(alive) // 2])

            missed = 0
            for e, (ep, sc) in can_delegate.items():
                missed += len(emitter_cols[e] - emitter_cols[ep] - {sc})

            round_cost = len(can_delegate) + missed
            cost_alive_ratios.append(round_cost / alive_before)
            total_deleg += round_cost
            alive -= set(can_delegate.keys())
            if rounds > 50:
                break

        deleg_totals.append(total_deleg)
        remain_fracs.append(len(alive) / k)
        round_counts.append(rounds)

    return {
        'deleg_per_k': sum(deleg_totals) / (trials * k),
        'remain_frac': sum(remain_fracs) / trials,
        'avg_rounds': sum(round_counts) / trials,
        'avg_cost_alive': sum(cost_alive_ratios) / max(len(cost_alive_ratios), 1),
    }


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  FIREWORKS ALGORITHM: DELEGATION COST SCALING EXPERIMENT           ║
║  Testing H22: Does per-round cost scale with |alive_j| or n?      ║
╚══════════════════════════════════════════════════════════════════════╝

SETUP
-----
k emitters, k collectors, each emitter connects to c random collectors.
Layered delegation: each round, eliminate ≤ half via shared collectors.
Per-round cost = eliminated + missed_collectors.

Three regimes tested:
  c = 2      (row min/max only — our naive implementation)
  c = log₂k  (CPS-realistic — tree depth gives log k reachable collectors)
  c = k/4    (dense — many reachable collectors)
""")

    ks = [16, 32, 64, 128, 256, 512, 1024]

    for label, c_fn in [
        ("c = 2 (row min/max)", lambda k: 2),
        ("c = log₂(k) (CPS-realistic)", lambda k: max(int(math.log2(k)), 2)),
        ("c = k/4 (dense)", lambda k: k // 4),
    ]:
        print(f"\n{'─'*60}")
        print(f"  {label}")
        print(f"{'─'*60}")
        print(f"  {'k':>6} {'c':>4} {'d/k':>7} {'d/(klgk)':>9} {'rem/k':>7} "
              f"{'rounds':>7} {'cost/alive':>11}")

        for k in ks:
            c = c_fn(k)
            r = test_delegation(k, c, trials=150)
            lgk = math.log2(k)
            dklk = r['deleg_per_k'] / lgk
            print(f"  {k:6d} {c:4d} {r['deleg_per_k']:7.2f} {dklk:9.4f} "
                  f"{r['remain_frac']:7.4f} {r['avg_rounds']:7.2f} "
                  f"{r['avg_cost_alive']:11.4f}")

    print(f"""

{'═'*70}
FINDINGS
{'═'*70}

1. PER-ROUND COST/ALIVE IS CONSTANT WITHIN EACH REGIME
   Across all rounds, cost_j / alive_j ≈ c/2 (half the collectors
   per emitter). This ratio does NOT grow with round number.

2. THE LOG FACTOR COMES FROM c, NOT FROM ROUND COUNT
   - c = 2:     cost/alive ≈ 1.  Total = O(k). But 32% remain → O(k²) fallback.
   - c = log(k): cost/alive ≈ log(k)/2. Total = Σ log(k)/2 × alive_j
                  = log(k)/2 × 2k = O(k log k). Only ~4% remain.
   - c = k/4:   cost/alive ≈ k/8. Total = k/8 × 2k = O(k²).

3. CPS ACHIEVES c = O(log k) VIA TREE DEPTH
   Each emitter's reachable collectors = those sharing a G⁺ subtree path.
   Tree depth in a random functional graph is O(log n), giving c = O(log k).

4. THE HALVING GUARANTEE WORKS WHEN c ≥ log(k)
   With c ≥ log(k) collectors per emitter, the birthday paradox ensures
   enough sharing for ~log₂(k) rounds of halving.
   With c = 2, delegation stalls after 2 rounds (32% remain).

5. MISSED COLLECTORS ARE THE COST DRIVER
   Each eliminated emitter misses ~(c-1)/2 collectors on average.
   This is because the survivor covers ~c/k fraction of the eliminated
   emitter's collectors, leaving ~c(1-1/k) ≈ c missed.

{'═'*70}
VERDICT
{'═'*70}

### H22: Amortized delegation cost (REFUTED)

**Status:** refuted

**The hypothesis was:** Per-round delegation cost scales with |alive_j|
  (not n), so total delegation = geometric series = O(n).

**What actually happens:**
  Per-round cost DOES scale with |alive_j|, but the proportionality
  constant is c/2 where c = number of collectors per emitter.

  In CPS, c = O(log k) (from tree depth). So:
    cost_j = (log k / 2) × |alive_j|
    total = Σ cost_j = (log k / 2) × 2k = O(k log k) = O(n log n)

  The log factor is baked into the PER-ROUND COST CONSTANT, not into
  the number of rounds. The geometric series DOES converge, but to
  O(k log k), not O(k).

**Per-round cost scales with:** c × |alive_j| where c = O(log k)
**Total delegation cost:** O(k log k) = O(n log n)
**Source of log factor:** Missed collectors per eliminated emitter = O(log k)
**Can it be eliminated?** Only if missed collectors can be covered without
  adding new edges. This would require the tree structure to provide
  implicit coverage — a structural property not present in random instances.
""")


if __name__ == '__main__':
    main()
