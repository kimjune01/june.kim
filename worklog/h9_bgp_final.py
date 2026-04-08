#!/usr/bin/env python3 -u
"""
H9 final analysis: consolidate all findings.

Key findings so far:
1. Greedy pruning is suboptimal (misses some feasible solutions)
2. The 4k-3 budget is sometimes truly infeasible
3. All three BGP variants (standard, aggressive, economic) converge to same answer

This script:
- Runs exhaustive checks at k=4 to get exact statistics
- Tests a smarter algorithm (simulated annealing) to close the greedy gap
- Quantifies the "greedy suboptimality" rate
- Tests 1-healability on optimal solutions
"""

import random
from itertools import combinations
import time

random.seed(42)


def random_matrix(k):
    perm = list(range(1, k * k + 1))
    random.shuffle(perm)
    return [perm[i * k:(i + 1) * k] for i in range(k)]


def compute_reachability_set(active_edges, M, k):
    n = 2 * k
    INF = float('inf')
    reach = [[INF] * n for _ in range(n)]
    for u in range(n):
        reach[u][u] = 0
    edge_list = sorted([(i, k + j, M[i][j]) for (i, j) in active_edges], key=lambda e: e[2])
    changed = True
    while changed:
        changed = False
        for (u, v, t) in edge_list:
            for src in range(n):
                if reach[src][u] <= t and t < reach[src][v]:
                    reach[src][v] = t
                    changed = True
                if reach[src][v] <= t and t < reach[src][u]:
                    reach[src][u] = t
                    changed = True
    reachable = set()
    for u in range(n):
        for v in range(n):
            if u != v and reach[u][v] < INF:
                reachable.add((u, v))
    return reachable


def greedy_prune(M, k):
    active = {(i, j) for i in range(k) for j in range(k)}
    base = compute_reachability_set(active, M, k)
    changed = True
    while changed:
        changed = False
        for e in list(active):
            trial = active - {e}
            if base.issubset(compute_reachability_set(trial, M, k)):
                active = trial
                base = compute_reachability_set(active, M, k)
                changed = True
    return active


def greedy_prune_random_order(M, k):
    """Greedy prune with randomized edge order (may find different solutions)."""
    active = {(i, j) for i in range(k) for j in range(k)}
    base = compute_reachability_set(active, M, k)
    changed = True
    while changed:
        changed = False
        edges = list(active)
        random.shuffle(edges)
        for e in edges:
            if e not in active:
                continue
            trial = active - {e}
            if base.issubset(compute_reachability_set(trial, M, k)):
                active = trial
                base = compute_reachability_set(active, M, k)
                changed = True
    return active


def find_minimum_exact(M, k, budget):
    """Exhaustive: find if budget edges suffice."""
    all_edges = [(i, j) for i in range(k) for j in range(k)]
    full = compute_reachability_set(set(all_edges), M, k)
    for subset in combinations(all_edges, budget):
        if full.issubset(compute_reachability_set(set(subset), M, k)):
            return True, set(subset)
    return False, None


def find_true_minimum(M, k, upper_bound):
    """Find true minimum edge count via binary search + exhaustive."""
    lo = 2 * k - 1  # tree lower bound
    hi = upper_bound
    best = upper_bound
    best_set = None

    for target in range(upper_bound - 1, lo - 1, -1):
        ok, sol = find_minimum_exact(M, k, target)
        if ok:
            best = target
            best_set = sol
        else:
            break
    return best, best_set


def simulated_annealing_prune(M, k, budget, max_iter=10000):
    """
    SA-based search: start from greedy solution, try swapping edges
    (remove one, add another from unused pool) to reduce edge count
    while preserving reachability.
    """
    active = greedy_prune_random_order(M, k)
    full = compute_reachability_set({(i,j) for i in range(k) for j in range(k)}, M, k)
    all_edges = {(i, j) for i in range(k) for j in range(k)}
    best = set(active)
    best_count = len(active)

    temp = 1.0
    for it in range(max_iter):
        temp = max(0.01, 1.0 - it / max_iter)

        if len(active) <= budget:
            if len(active) < best_count:
                best = set(active)
                best_count = len(active)

        # Try removing a random edge
        if active:
            e = random.choice(list(active))
            trial = active - {e}
            if full.issubset(compute_reachability_set(trial, M, k)):
                active = trial
                if len(active) < best_count:
                    best = set(active)
                    best_count = len(active)
                continue

        # Try swap: remove one, add one from unused
        unused = all_edges - active
        if active and unused:
            rem = random.choice(list(active))
            add = random.choice(list(unused))
            trial = (active - {rem}) | {add}
            if full.issubset(compute_reachability_set(trial, M, k)):
                # Accept if fewer edges or with temperature probability
                if len(trial) <= len(active) or random.random() < temp * 0.1:
                    active = trial

    return best, best_count


def test_healability(active_edges, M, k):
    """Test 1-healability of the spanner."""
    base = compute_reachability_set(active_edges, M, k)
    all_edges = {(i, j) for i in range(k) for j in range(k)}
    non_spanner = all_edges - active_edges

    survived = 0
    healed = 0
    unhealed = 0

    for e in list(active_edges):
        trial = active_edges - {e}
        trial_reach = compute_reachability_set(trial, M, k)
        if base.issubset(trial_reach):
            survived += 1
            continue
        found = False
        for e2 in non_spanner:
            repair = trial | {e2}
            if base.issubset(compute_reachability_set(repair, M, k)):
                found = True
                break
        if found:
            healed += 1
        else:
            unhealed += 1

    return survived, healed, unhealed


def main():
    print("=" * 80)
    print("H9 FINAL: Exact feasibility + algorithm comparison")
    print("=" * 80)

    # ─── k=4: complete analysis ───
    print(f"\n{'═' * 60}")
    print(f"k=4: EXHAUSTIVE ANALYSIS (50 trials)")
    print(f"{'═' * 60}")

    random.seed(42)
    budget = 13
    results = {'greedy': 0, 'sa': 0, 'exact': 0, 'infeasible': 0,
               'greedy_suboptimal': 0}
    greedy_counts_4 = []
    exact_counts_4 = []

    for trial in range(50):
        M = random_matrix(4)

        # Greedy (multiple random orders, take best)
        best_greedy = None
        for _ in range(10):
            g = greedy_prune_random_order(M, 4)
            if best_greedy is None or len(g) < len(best_greedy):
                best_greedy = g
        gc = len(best_greedy)
        greedy_counts_4.append(gc)

        if gc <= budget:
            results['greedy'] += 1

        # Exact
        if gc > budget:
            ok, sol = find_minimum_exact(M, 4, budget)
            if ok:
                results['exact'] += 1
                results['greedy_suboptimal'] += 1
                exact_counts_4.append(budget)
            else:
                results['infeasible'] += 1
                # Find true minimum
                true_min, _ = find_true_minimum(M, 4, gc)
                exact_counts_4.append(true_min)
        else:
            exact_counts_4.append(gc)

        if (trial + 1) % 10 == 0:
            print(f"  trial {trial+1}/50")

    print(f"\n  Greedy within budget: {results['greedy']}/50")
    print(f"  Greedy suboptimal (budget feasible but greedy missed): {results['greedy_suboptimal']}/50")
    print(f"  Truly infeasible: {results['infeasible']}/50")
    print(f"  Total feasible: {results['greedy'] + results['exact']}/50")
    print(f"  Greedy edge counts: {sorted(greedy_counts_4)}")
    print(f"  Exact edge counts: {sorted(exact_counts_4)}")

    # ─── k=4: healability on optimal solutions ───
    print(f"\n{'═' * 60}")
    print(f"k=4: 1-HEALABILITY on optimal solutions")
    print(f"{'═' * 60}")

    random.seed(42)
    for trial in range(10):
        M = random_matrix(4)
        # Find best solution
        best = None
        for _ in range(20):
            g = greedy_prune_random_order(M, 4)
            if best is None or len(g) < len(best):
                best = g
        if len(best) > 13:
            ok, sol = find_minimum_exact(M, 4, 13)
            if ok:
                best = sol

        s, h, u = test_healability(best, M, 4)
        print(f"  trial {trial}: {len(best)} edges, survived={s} healed={h} unhealed={u}")

    # ─── k=5: SA vs greedy ───
    print(f"\n{'═' * 60}")
    print(f"k=5: SIMULATED ANNEALING vs GREEDY (50 trials)")
    print(f"{'═' * 60}")

    random.seed(42)
    budget5 = 17
    greedy_in = 0
    sa_in = 0
    sa_better = 0
    greedy_counts_5 = []
    sa_counts_5 = []

    for trial in range(50):
        M = random_matrix(5)

        # Multi-start greedy
        best_g = None
        for _ in range(10):
            g = greedy_prune_random_order(M, 5)
            if best_g is None or len(g) < len(best_g):
                best_g = g
        gc = len(best_g)
        greedy_counts_5.append(gc)
        if gc <= budget5:
            greedy_in += 1

        # SA
        sa_set, sa_count = simulated_annealing_prune(M, 5, budget5, max_iter=5000)
        sa_counts_5.append(sa_count)
        if sa_count <= budget5:
            sa_in += 1
        if sa_count < gc:
            sa_better += 1

        if (trial + 1) % 10 == 0:
            print(f"  trial {trial+1}/50")

    print(f"\n  Greedy within budget: {greedy_in}/50")
    print(f"  SA within budget: {sa_in}/50")
    print(f"  SA found better than greedy: {sa_better}/50")
    g_mean = sum(greedy_counts_5) / 50
    s_mean = sum(sa_counts_5) / 50
    print(f"  Greedy mean edges: {g_mean:.1f}")
    print(f"  SA mean edges: {s_mean:.1f}")

    # ─── k=6,7: multi-start greedy ───
    for k in [6, 7]:
        print(f"\n{'═' * 60}")
        print(f"k={k}: MULTI-START GREEDY (50 trials, 10 starts each)")
        print(f"{'═' * 60}")

        random.seed(42)
        budgetk = 4 * k - 3
        counts = []
        in_budget = 0

        for trial in range(50):
            M = random_matrix(k)
            best = None
            for _ in range(10):
                g = greedy_prune_random_order(M, k)
                if best is None or len(g) < len(best):
                    best = g
            counts.append(len(best))
            if len(best) <= budgetk:
                in_budget += 1

            if (trial + 1) % 10 == 0:
                print(f"  trial {trial+1}/50")

        mean_c = sum(counts) / 50
        print(f"\n  Budget: {budgetk}")
        print(f"  Edge counts: min={min(counts)} max={max(counts)} mean={mean_c:.1f}")
        print(f"  Within budget: {in_budget}/50")

    # ─── Summary table ───
    print(f"\n{'═' * 80}")
    print("FINAL SUMMARY")
    print(f"{'═' * 80}")


if __name__ == "__main__":
    main()
