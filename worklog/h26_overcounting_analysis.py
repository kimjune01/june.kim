"""
H26 part 2: Precise overcounting analysis.

The first script showed overcounting factor ≈ avg_degree, NOT log(k).
That's suspicious — it suggests the overcounting is proportional to the
number of emitters that share each collector, which is avg_degree (not log k).

Need to separate two effects:
1. Overcounting from PARALLEL elimination (same round)
2. Overcounting from REPEATED rounds (same collector missed in round 1 AND round 2)

Also need to verify with the ACTUAL CPS structure (S⁻/S⁺ neighborhoods)
rather than random sparse bipartite.
"""

import random
import math
from collections import defaultdict


def random_sparse_bipartite(n_emitters, n_collectors, avg_degree, seed=None):
    rng = random.Random(seed)
    neighborhoods = {}
    for e in range(n_emitters):
        deg = max(1, int(rng.gauss(avg_degree, avg_degree * 0.3)))
        deg = min(deg, n_collectors)
        neighborhoods[e] = set(rng.sample(range(n_collectors), deg))
    return neighborhoods


def cps_halving_detailed(neighborhoods):
    """
    CPS halving with detailed per-round, per-collector tracking.
    Returns overcounting broken down by source.
    """
    alive = list(neighborhoods.keys())
    rng = random.Random(42)

    # Track: for each collector, which rounds it was missed in
    collector_rounds = defaultdict(list)  # collector -> [round numbers]
    # Track: within each round, how many emitters miss each collector
    round_data = []

    round_num = 0
    while len(alive) > 1:
        round_num += 1
        rng.shuffle(alive)

        pairs = []
        for i in range(0, len(alive) - 1, 2):
            pairs.append((alive[i], alive[i + 1]))

        within_round_counts = defaultdict(int)  # collector -> times missed this round
        eliminated = []

        for e1, e2 in pairs:
            missed = neighborhoods[e1] - neighborhoods[e2]
            for c in missed:
                within_round_counts[c] += 1
                collector_rounds[c].append(round_num)
            eliminated.append(e1)

        # Within-round overcounting: collectors missed by >1 emitter in same round
        within_overcount = sum(max(0, v - 1) for v in within_round_counts.values())

        round_data.append({
            'round': round_num,
            'alive': len(alive),
            'eliminated': len(eliminated),
            'total_missed': sum(within_round_counts.values()),
            'unique_missed': len(within_round_counts),
            'within_overcount': within_overcount,
        })

        alive = [e for e in alive if e not in set(eliminated)]
        if round_num > 50:
            break

    # Cross-round overcounting: collectors that appear in multiple rounds
    cross_round = sum(max(0, len(rounds) - 1) for rounds in collector_rounds.values())

    return round_data, dict(collector_rounds), cross_round


def analyze_overcounting_scaling():
    """
    Key question: does CPS overcounting scale as O(log k) or O(degree)?

    Fix degree, vary k: if overcounting ~ log k, it's the rounds.
    Fix k, vary degree: if overcounting ~ degree, it's the density.
    """
    print("=" * 70)
    print("OVERCOUNTING SCALING: DEGREE vs LOG(K)")
    print("=" * 70)
    print()

    # Experiment 1: Fix degree = 10, vary k
    print("--- Fixed degree=10, varying k ---")
    print(f"{'k':>6} {'log k':>6} {'overcount':>10} {'oc/k':>8} {'oc/k/logk':>10} "
          f"{'within':>8} {'cross':>8}")

    for k in [20, 50, 100, 200, 500, 1000]:
        trials = 20
        ocs = []
        withins = []
        crosses = []
        for trial in range(trials):
            nbrs = random_sparse_bipartite(k, k, 10, seed=k * 10000 + trial)
            rds, col_rounds, cross = cps_halving_detailed(nbrs)
            total = sum(r['total_missed'] for r in rds)
            within = sum(r['within_overcount'] for r in rds)
            ocs.append(total)
            withins.append(within)
            crosses.append(cross)

        avg_oc = sum(ocs) / trials
        avg_w = sum(withins) / trials
        avg_c = sum(crosses) / trials
        logk = math.log2(k)
        print(f"{k:6d} {logk:6.1f} {avg_oc:10.1f} {avg_oc/k:8.2f} "
              f"{avg_oc/k/logk:10.4f} {avg_w:8.1f} {avg_c:8.1f}")

    print()

    # Experiment 2: Fix k=100, vary degree
    print("--- Fixed k=100, varying degree ---")
    print(f"{'deg':>6} {'overcount':>10} {'oc/k':>8} {'oc/deg':>8} "
          f"{'within':>8} {'cross':>8}")

    for deg in [5, 10, 20, 30, 50, 80]:
        trials = 20
        ocs = []
        withins = []
        crosses = []
        for trial in range(trials):
            nbrs = random_sparse_bipartite(100, 100, deg, seed=deg * 10000 + trial)
            rds, col_rounds, cross = cps_halving_detailed(nbrs)
            total = sum(r['total_missed'] for r in rds)
            within = sum(r['within_overcount'] for r in rds)
            ocs.append(total)
            withins.append(within)
            crosses.append(cross)

        avg_oc = sum(ocs) / trials
        avg_w = sum(withins) / trials
        avg_c = sum(crosses) / trials
        print(f"{deg:6d} {avg_oc:10.1f} {avg_oc/100:8.2f} {avg_oc/deg:8.2f} "
              f"{avg_w:8.1f} {avg_c:8.1f}")

    print()

    # Experiment 3: The CPS-relevant structure: S⁻/S⁺ neighborhoods (degree=2)
    print("--- CPS S⁻/S⁺ structure (degree=2 per emitter) ---")
    print(f"{'k':>6} {'log k':>6} {'overcount':>10} {'oc/k':>8} {'oc/k/logk':>10}")

    for k in [20, 50, 100, 200, 500, 1000]:
        trials = 20
        ocs = []
        for trial in range(trials):
            rng = random.Random(k * 10000 + trial)
            nbrs = {}
            for e in range(k):
                # S⁻ and S⁺: two random collectors
                c1 = rng.randrange(k)
                c2 = rng.randrange(k)
                while c2 == c1:
                    c2 = rng.randrange(k)
                nbrs[e] = {c1, c2}

            rds, col_rounds, cross = cps_halving_detailed(nbrs)
            total = sum(r['total_missed'] for r in rds)
            ocs.append(total)

        avg_oc = sum(ocs) / trials
        logk = math.log2(k)
        print(f"{k:6d} {logk:6.1f} {avg_oc:10.1f} {avg_oc/k:8.2f} "
              f"{avg_oc/k/logk:10.4f}")

    print()


def analyze_within_vs_cross():
    """Where does the overcounting come from?"""
    print("=" * 70)
    print("WITHIN-ROUND vs CROSS-ROUND OVERCOUNTING")
    print("=" * 70)
    print()

    for k in [100, 500]:
        for deg in [10, 50]:
            print(f"--- k={k}, deg={deg} ---")
            trials = 20

            for trial in range(min(3, trials)):
                nbrs = random_sparse_bipartite(k, k, deg, seed=k * 10000 + trial)
                rds, col_rounds, cross = cps_halving_detailed(nbrs)

                total_missed = sum(r['total_missed'] for r in rds)
                total_within = sum(r['within_overcount'] for r in rds)
                unique_collectors = len(col_rounds)

                print(f"  Trial {trial}: total_missed={total_missed}, "
                      f"unique_collectors={unique_collectors}, "
                      f"within_round_overcount={total_within}, "
                      f"cross_round_overcount={cross}")

                # Per-round breakdown
                for r in rds[:5]:
                    print(f"    Round {r['round']}: alive={r['alive']}, "
                          f"elim={r['eliminated']}, "
                          f"missed={r['total_missed']}, "
                          f"unique={r['unique_missed']}, "
                          f"within_oc={r['within_overcount']}")
                if len(rds) > 5:
                    print(f"    ... ({len(rds)} rounds total)")
            print()


def sequential_vs_halving_spanner():
    """
    The ultimate comparison: sequential delegation spanner vs CPS halving spanner.
    Both on the same instances.
    """
    print("=" * 70)
    print("SPANNER COMPARISON: SEQUENTIAL vs CPS HALVING")
    print("=" * 70)
    print()

    # CPS S⁻/S⁺ structure (the actual relevant case)
    print("--- CPS S⁻/S⁺ structure ---")
    print(f"{'k':>6} {'seq':>8} {'halv':>8} {'ratio':>7} {'2k-1':>6} {'within budget':>14}")

    for k in [10, 20, 50, 100, 200, 500]:
        trials = 30
        seq_costs = []
        halv_costs = []

        for trial in range(trials):
            rng = random.Random(k * 10000 + trial)
            nbrs = {}
            for e in range(k):
                c1 = rng.randrange(k)
                c2 = rng.randrange(k)
                while c2 == c1:
                    c2 = rng.randrange(k)
                nbrs[e] = {c1, c2}

            # Sequential: cost = |∪N| + (k-1)
            union = set()
            for n_e in nbrs.values():
                union |= n_e
            seq_cost = len(union) + (k - 1)

            # Halving: cost = delegation edges + missed (with overcounting)
            rds, _, _ = cps_halving_detailed(nbrs)
            halv_cost = sum(r['total_missed'] for r in rds) + sum(r['eliminated'] for r in rds)

            seq_costs.append(seq_cost)
            halv_costs.append(halv_cost)

        avg_seq = sum(seq_costs) / trials
        avg_halv = sum(halv_costs) / trials
        budget = 2 * k - 1

        print(f"{k:6d} {avg_seq:8.1f} {avg_halv:8.1f} {avg_halv/max(avg_seq,1):7.2f} "
              f"{budget:6d} {'YES' if avg_seq <= budget else 'NO':>14}")

    print()
    print("Sequential cost = |∪N| + (k-1)")
    print("  |∪N| for S⁻/S⁺ with k emitters, k collectors:")
    print("  Each emitter has 2 random collectors → ∪N ~ k(1-(1-1/k)^(2k)) ~ k(1-e^-2) ≈ 0.865k")
    print("  So seq cost ≈ 0.865k + k - 1 ≈ 1.865k ≤ 2k - 1 for k ≥ ... ")
    print()

    # Verify the union size empirically
    print("--- Empirical |∪N|/k for S⁻/S⁺ ---")
    for k in [10, 50, 100, 500, 1000, 5000]:
        trials = 50
        ratios = []
        for trial in range(trials):
            rng = random.Random(k * 10000 + trial)
            union = set()
            for e in range(k):
                c1 = rng.randrange(k)
                c2 = rng.randrange(k)
                while c2 == c1:
                    c2 = rng.randrange(k)
                union.add(c1)
                union.add(c2)
            ratios.append(len(union) / k)
        avg = sum(ratios) / trials
        expected = 1 - (1 - 1/k) ** (2*k)  # approx
        print(f"  k={k:5d}: |∪N|/k = {avg:.4f}, expected 1-e^-2 = {1 - math.exp(-2):.4f}")


def run():
    analyze_overcounting_scaling()
    analyze_within_vs_cross()
    sequential_vs_halving_spanner()


if __name__ == '__main__':
    run()
