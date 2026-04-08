#!/usr/bin/env python3 -u
"""
H9 deep analysis: WHY does BGP pruning fail to reach the budget?

Key questions:
1. Are ALL remaining edges critical (removing any one breaks some pair)?
2. Is there a subset of edges that could be jointly removed but not individually?
3. What's the minimum edge count for random matrices (via exhaustive search for small k)?
4. Distribution analysis: how many edges over budget are we?
5. Does the gap grow linearly or faster with k?
"""

import random
from itertools import combinations
import time

random.seed(42)


def random_matrix(k):
    perm = list(range(1, k * k + 1))
    random.shuffle(perm)
    return [perm[i * k:(i + 1) * k] for i in range(k)]


def compute_reachability(active_edges, M, k):
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
    return reach, reachable


def greedy_prune(M, k):
    """Greedy prune: remove edges one by one, always the least impactful."""
    active = {(i, j) for i in range(k) for j in range(k)}
    _, base_reachable = compute_reachability(active, M, k)

    while True:
        removed_any = False
        edges = list(active)
        random.shuffle(edges)
        for e in edges:
            if e not in active:
                continue
            trial = active - {e}
            _, trial_reachable = compute_reachability(trial, M, k)
            if base_reachable.issubset(trial_reachable):
                active = trial
                _, base_reachable = compute_reachability(active, M, k)
                removed_any = True
        if not removed_any:
            break
    return active


def check_all_critical(active_edges, M, k):
    """Check if every remaining edge is critical (removing it breaks some pair)."""
    _, base_reachable = compute_reachability(active_edges, M, k)
    critical_count = 0
    non_critical = []
    for e in active_edges:
        trial = active_edges - {e}
        _, trial_reachable = compute_reachability(trial, M, k)
        if not base_reachable.issubset(trial_reachable):
            critical_count += 1
        else:
            non_critical.append(e)
    return critical_count, non_critical


def try_joint_removal(active_edges, M, k, max_remove=3):
    """
    Try removing 2 or 3 edges jointly. Sometimes individual edges are all
    critical but a pair can be removed together (one edge becomes redundant
    once another is removed).
    """
    _, base_reachable = compute_reachability(active_edges, M, k)
    edge_list = list(active_edges)

    best_removal = 0
    for size in range(2, min(max_remove + 1, len(edge_list))):
        found = False
        # Only sample if too many combinations
        combos = list(combinations(edge_list, size))
        if len(combos) > 5000:
            combos = random.sample(combos, 5000)
        for subset in combos:
            trial = active_edges - set(subset)
            _, trial_reachable = compute_reachability(trial, M, k)
            if base_reachable.issubset(trial_reachable):
                best_removal = max(best_removal, size)
                found = True
                break
        if not found and size == 2:
            break  # if no pair works, triples won't either (usually)
    return best_removal


def minimum_edge_count_exact(M, k, max_time=5.0):
    """
    For small k, find the true minimum number of edges preserving full reachability.
    Uses iterative deepening: try removing n edges for increasing n.
    """
    active = {(i, j) for i in range(k) for j in range(k)}
    _, full_reachable = compute_reachability(active, M, k)

    # Start from greedy result
    greedy_result = greedy_prune(M, k)
    current_best = len(greedy_result)

    # For k=3: 9 edges, try all subsets of size current_best-1, current_best-2, etc.
    t0 = time.time()
    for target_size in range(current_best - 1, 2 * k - 2, -1):  # at least 2k-1 edges needed (tree)
        if time.time() - t0 > max_time:
            break
        found = False
        all_edges = [(i, j) for i in range(k) for j in range(k)]
        combos = combinations(all_edges, target_size)
        count = 0
        for subset in combos:
            count += 1
            if count > 100000:
                break
            if time.time() - t0 > max_time:
                break
            _, sub_reachable = compute_reachability(set(subset), M, k)
            if full_reachable.issubset(sub_reachable):
                current_best = target_size
                found = True
                break
        if not found:
            break

    return current_best


def analyze_why_critical(active_edges, M, k):
    """
    For each critical edge, identify WHICH pairs it uniquely serves.
    """
    n = 2 * k
    _, base_reachable = compute_reachability(active_edges, M, k)

    edge_serves = {}
    for e in active_edges:
        trial = active_edges - {e}
        _, trial_reachable = compute_reachability(trial, M, k)
        lost_pairs = base_reachable - trial_reachable
        edge_serves[e] = lost_pairs

    return edge_serves


def main():
    print("=" * 80)
    print("H9 DEEP ANALYSIS: Why does BGP pruning overshoot the budget?")
    print("=" * 80)

    num_trials = 50

    for k in [3, 4, 5, 6, 7]:
        budget = 4 * k - 3
        print(f"\n{'─' * 70}")
        print(f"k={k}, budget={budget}")
        print(f"{'─' * 70}")

        over_budget_count = 0
        over_budget_amounts = []
        all_critical_count = 0
        joint_removable = 0
        min_edges_exact = []

        for trial in range(num_trials):
            M = random_matrix(k)
            edges = greedy_prune(M, k)
            ec = len(edges)

            if ec > budget:
                over_budget_count += 1
                over_budget_amounts.append(ec - budget)

                # Check if all edges are critical
                crit, non_crit = check_all_critical(edges, M, k)
                if crit == ec:
                    all_critical_count += 1

                # Try joint removal (k <= 5)
                if k <= 5:
                    jr = try_joint_removal(edges, M, k, max_remove=3)
                    if jr > 0:
                        joint_removable += 1

            # Exact minimum (k=3 only)
            if k == 3 and trial < 20:
                min_e = minimum_edge_count_exact(M, k, max_time=2.0)
                min_edges_exact.append(min_e)

            if (trial + 1) % 10 == 0:
                print(f"  trial {trial+1}/{num_trials}")

        print(f"\n  Over budget: {over_budget_count}/{num_trials}")
        if over_budget_amounts:
            print(f"  Excess edges: min={min(over_budget_amounts)} max={max(over_budget_amounts)} "
                  f"mean={sum(over_budget_amounts)/len(over_budget_amounts):.1f}")
            print(f"  All-critical (no slack): {all_critical_count}/{over_budget_count}")
            if k <= 5:
                print(f"  Joint-removable (2-3 at once): {joint_removable}/{over_budget_count}")

        if min_edges_exact:
            print(f"\n  Exact minimum edges (k=3, first 20 trials):")
            print(f"    min={min(min_edges_exact)} max={max(min_edges_exact)} "
                  f"mean={sum(min_edges_exact)/len(min_edges_exact):.1f}")
            in_budget = sum(1 for e in min_edges_exact if e <= budget)
            print(f"    within budget: {in_budget}/{len(min_edges_exact)}")

    # ── Detailed case study: one failure at k=5 ──
    print(f"\n{'─' * 70}")
    print("CASE STUDY: Analyzing one over-budget instance at k=5")
    print(f"{'─' * 70}")

    random.seed(42)
    for _ in range(100):
        M = random_matrix(5)
        edges = greedy_prune(M, 5)
        if len(edges) > 17:
            break

    print(f"  Matrix M:")
    for row in M:
        print(f"    {row}")
    print(f"  Edges retained: {len(edges)} (budget=17)")
    print(f"  Edges: {sorted(edges)}")

    serves = analyze_why_critical(edges, M, 5)
    print(f"\n  Critical edge analysis:")
    for e in sorted(edges):
        pairs = serves[e]
        if pairs:
            print(f"    ({e[0]},{e[1]}) t={M[e[0]][e[1]]:>3}: critical for {len(pairs)} pairs")
        else:
            print(f"    ({e[0]},{e[1]}) t={M[e[0]][e[1]]:>3}: NOT critical (greedy missed it!)")

    # Check reachability count
    _, full_reach = compute_reachability({(i,j) for i in range(5) for j in range(5)}, M, 5)
    _, sparse_reach = compute_reachability(edges, M, 5)
    print(f"\n  Full graph reachable pairs: {len(full_reach)}")
    print(f"  Sparse graph reachable pairs: {len(sparse_reach)}")

    # ── Growth rate analysis ──
    print(f"\n{'─' * 70}")
    print("GROWTH RATE: mean edge count vs budget")
    print(f"{'─' * 70}")

    random.seed(42)
    for k in range(3, 11):
        budget = 4 * k - 3
        counts = []
        num = 30 if k <= 7 else 10
        for _ in range(num):
            M = random_matrix(k)
            edges = greedy_prune(M, k)
            counts.append(len(edges))
        mean_c = sum(counts) / len(counts)
        ratio = mean_c / budget
        print(f"  k={k:>2}: budget={budget:>3}, mean_edges={mean_c:>6.1f}, ratio={ratio:.3f}, "
              f"excess={mean_c - budget:>+5.1f}")


if __name__ == "__main__":
    main()
