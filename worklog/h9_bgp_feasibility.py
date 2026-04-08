#!/usr/bin/env python3 -u
"""
H9 feasibility check: Is 4k-3 always achievable?

The key question: when greedy pruning produces an all-critical spanner with
more than 4k-3 edges, is the 4k-3 budget actually feasible for that matrix?

For k=4 (budget=13, 16 edges): exhaustive search is feasible.
Check every subset of 13 edges, see if any preserves full reachability.
C(16,13) = 560. Very fast.

For k=5 (budget=17, 25 edges): C(25,17) = 1,081,575. Feasible.
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


def is_feasible(M, k, budget):
    """Check if there exists a subset of ≤ budget edges preserving full reachability."""
    all_edges = [(i, j) for i in range(k) for j in range(k)]
    full_reachable = compute_reachability_set(set(all_edges), M, k)

    # Try subsets of exactly budget edges
    for subset in combinations(all_edges, budget):
        sub_reachable = compute_reachability_set(set(subset), M, k)
        if full_reachable.issubset(sub_reachable):
            return True, set(subset)

    return False, None


def greedy_prune(M, k):
    active = {(i, j) for i in range(k) for j in range(k)}
    full_reachable = compute_reachability_set(active, M, k)
    while True:
        removed = False
        for e in list(active):
            trial = active - {e}
            if full_reachable.issubset(compute_reachability_set(trial, M, k)):
                active = trial
                full_reachable = compute_reachability_set(active, M, k)
                removed = True
        if not removed:
            break
    return active


def main():
    print("=" * 80)
    print("H9 FEASIBILITY: Is 4k-3 budget achievable for random matrices?")
    print("=" * 80)

    # k=4: exhaustive check on all 50 trials
    print(f"\n{'─' * 60}")
    print(f"k=4, budget=13, C(16,13)=560 subsets")
    print(f"{'─' * 60}")

    random.seed(42)
    feasible_count = 0
    infeasible_examples = []
    for trial in range(50):
        M = random_matrix(4)
        greedy_edges = greedy_prune(M, 4)
        gc = len(greedy_edges)

        if gc <= 13:
            feasible_count += 1
        else:
            ok, solution = is_feasible(M, 4, 13)
            if ok:
                feasible_count += 1
                print(f"  trial {trial}: greedy={gc}, but budget IS feasible (greedy suboptimal!)")
            else:
                infeasible_examples.append((trial, M, gc))

        if (trial + 1) % 10 == 0:
            print(f"  checked {trial+1}/50")

    print(f"\n  Budget 13 feasible: {feasible_count}/50")
    print(f"  Budget 13 infeasible: {len(infeasible_examples)}/50")

    if infeasible_examples:
        trial_idx, M_ex, gc = infeasible_examples[0]
        print(f"\n  Example infeasible matrix (trial {trial_idx}, greedy={gc}):")
        for row in M_ex:
            print(f"    {row}")

        # What's the actual minimum for this matrix?
        for target in range(gc - 1, 2 * 4 - 2, -1):
            ok, _ = is_feasible(M_ex, 4, target)
            if not ok:
                print(f"  True minimum edges: {target + 1}")
                break

    # k=5: exhaustive check on over-budget cases
    print(f"\n{'─' * 60}")
    print(f"k=5, budget=17, C(25,17)=1,081,575 subsets")
    print(f"{'─' * 60}")

    random.seed(42)
    feasible_5 = 0
    infeasible_5 = 0
    greedy_optimal_5 = 0
    t0 = time.time()

    for trial in range(50):
        M = random_matrix(5)
        greedy_edges = greedy_prune(M, 5)
        gc = len(greedy_edges)

        if gc <= 17:
            feasible_5 += 1
            greedy_optimal_5 += 1
        else:
            # Check feasibility (might be slow)
            if time.time() - t0 > 300:
                print(f"  (skipping remaining trials due to time)")
                break
            ok, solution = is_feasible(M, 5, 17)
            if ok:
                feasible_5 += 1
                print(f"  trial {trial}: greedy={gc}, but budget IS feasible!")
            else:
                infeasible_5 += 1

        if (trial + 1) % 5 == 0:
            elapsed = time.time() - t0
            print(f"  checked {trial+1}/50 [{elapsed:.1f}s]")

    print(f"\n  Budget 17 feasible: {feasible_5}")
    print(f"  Budget 17 infeasible: {infeasible_5}")
    print(f"  Greedy already optimal: {greedy_optimal_5}")

    # k=5: what fraction of reachable pairs need preserving?
    print(f"\n{'─' * 60}")
    print(f"Reachability counts: how many pairs are reachable in full graph?")
    print(f"{'─' * 60}")

    random.seed(42)
    for k in [3, 4, 5, 6, 7]:
        n = 2 * k
        max_pairs = n * (n - 1)
        counts = []
        for _ in range(20):
            M = random_matrix(k)
            all_edges = {(i, j) for i in range(k) for j in range(k)}
            reachable = compute_reachability_set(all_edges, M, k)
            counts.append(len(reachable))
        mean_r = sum(counts) / len(counts)
        print(f"  k={k}: max_pairs={max_pairs}, mean_reachable={mean_r:.1f} ({100*mean_r/max_pairs:.1f}%)")


if __name__ == "__main__":
    main()
