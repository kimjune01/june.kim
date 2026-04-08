#!/usr/bin/env python3 -u
"""
H9 consolidated summary: all findings in one table.
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

def greedy_prune_random(M, k):
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

def multi_start_greedy(M, k, starts=20):
    best = None
    for _ in range(starts):
        g = greedy_prune_random(M, k)
        if best is None or len(g) < len(best):
            best = g
    return best

def find_minimum_exact(M, k, budget):
    all_edges = [(i, j) for i in range(k) for j in range(k)]
    full = compute_reachability_set(set(all_edges), M, k)
    for subset in combinations(all_edges, budget):
        if full.issubset(compute_reachability_set(set(subset), M, k)):
            return True
    return False

def test_healability(active_edges, M, k):
    base = compute_reachability_set(active_edges, M, k)
    all_edges = {(i, j) for i in range(k) for j in range(k)}
    non_spanner = all_edges - active_edges
    survived = healed = unhealed = 0
    for e in list(active_edges):
        trial = active_edges - {e}
        if base.issubset(compute_reachability_set(trial, M, k)):
            survived += 1
            continue
        found = False
        for e2 in non_spanner:
            if base.issubset(compute_reachability_set(trial | {e2}, M, k)):
                found = True
                break
        if found:
            healed += 1
        else:
            unhealed += 1
    return survived, healed, unhealed

def main():
    num_trials = 50
    print("=" * 80)
    print("H9: BGP-style Temporal Spanner — CONSOLIDATED RESULTS")
    print("=" * 80)
    print(f"50 random k×k matrices per k. Multi-start greedy (20 starts).")
    print(f"Reachability preservation: all (src,dst) pairs reachable in full graph")
    print(f"must remain reachable in the spanner.\n")

    # Header
    print(f"{'k':>3} {'n':>4} {'budget':>6} {'1-start':>9} {'20-start':>9} "
          f"{'%budget':>8} {'infeas':>7} {'heal-rate':>10}")
    print(f"{'':>3} {'':>4} {'4k-3':>6} {'mean|%ok':>9} {'mean|%ok':>9} "
          f"{'20-start':>8} {'(exact)':>7} {'(first 5)':>10}")
    print("─" * 75)

    for k in [3, 4, 5, 6, 7, 8]:
        budget = 4 * k - 3
        random.seed(42 + k)  # reproducible per k

        single_counts = []
        multi_counts = []
        single_in = 0
        multi_in = 0
        heal_data = []
        infeasible = 0

        for trial in range(num_trials):
            M = random_matrix(k)

            # Single-start greedy
            s = greedy_prune_random(M, k)
            single_counts.append(len(s))
            if len(s) <= budget:
                single_in += 1

            # Multi-start greedy (20 starts)
            m = multi_start_greedy(M, k, starts=20)
            multi_counts.append(len(m))
            if len(m) <= budget:
                multi_in += 1

            # Exact feasibility check (k=4 only)
            if k == 4 and len(m) > budget:
                if not find_minimum_exact(M, k, budget):
                    infeasible += 1

            # Healability (first 5)
            if trial < 5 and k <= 6:
                s_h, h_h, u_h = test_healability(m, M, k)
                total = s_h + h_h + u_h
                heal_rate = (s_h + h_h) / total if total > 0 else 0
                heal_data.append(heal_rate)

        s_mean = sum(single_counts) / num_trials
        m_mean = sum(multi_counts) / num_trials
        s_pct = 100 * single_in / num_trials
        m_pct = 100 * multi_in / num_trials
        heal_str = f"{100*sum(heal_data)/len(heal_data):.0f}%" if heal_data else "n/a"
        infeas_str = f"{infeasible}" if k == 4 else "n/a"

        print(f"{k:>3} {2*k:>4} {budget:>6} {s_mean:>5.1f}|{s_pct:>2.0f}% "
              f"{m_mean:>5.1f}|{m_pct:>2.0f}% {m_pct:>7.0f}% {infeas_str:>7} {heal_str:>10}")

    # ─── Detailed healability ───
    print(f"\n{'─' * 60}")
    print("1-HEALABILITY DETAIL (first 5 trials per k)")
    print(f"{'─' * 60}")

    for k in [4, 5, 6]:
        budget = 4 * k - 3
        random.seed(42 + k)
        print(f"\n  k={k} (budget={budget}):")
        for trial in range(5):
            M = random_matrix(k)
            m = multi_start_greedy(M, k, starts=20)
            s, h, u = test_healability(m, M, k)
            print(f"    trial {trial}: {len(m)} edges | survived={s} healed={h} unhealed={u}")

    # ─── Key finding: edge distribution ───
    print(f"\n{'─' * 60}")
    print("EDGE COUNT DISTRIBUTIONS (multi-start greedy, 50 trials)")
    print(f"{'─' * 60}")
    for k in [3, 4, 5, 6, 7]:
        budget = 4 * k - 3
        random.seed(42 + k)
        counts = []
        for _ in range(50):
            M = random_matrix(k)
            m = multi_start_greedy(M, k, starts=20)
            counts.append(len(m))
        from collections import Counter
        dist = Counter(counts)
        dist_str = " ".join(f"{v}:{c}" for v, c in sorted(dist.items()))
        print(f"  k={k} (budget={budget}): {dist_str}")


if __name__ == "__main__":
    main()
