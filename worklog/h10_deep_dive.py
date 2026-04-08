"""
H10 deep dive: investigate budget violations and tighten findings.
"""

import random
import statistics
from collections import defaultdict
import heapq

# Reuse core engine
def build_adj(k, edges):
    adj = defaultdict(list)
    for (a, b, t) in edges:
        adj[a].append((b, t))
        adj[b].append((a, t))
    return adj

def temporal_reachable_from(source, adj):
    best = {source: 0}
    queue = [(0, source)]
    heapq.heapify(queue)
    while queue:
        t_arr, u = heapq.heappop(queue)
        if t_arr > best.get(u, float('inf')):
            continue
        for (v, t_edge) in adj[u]:
            if t_edge >= t_arr:
                if t_edge < best.get(v, float('inf')):
                    best[v] = t_edge
                    heapq.heappush(queue, (t_edge, v))
    return set(best.keys())

def all_pairs_reach(k, edges):
    adj = build_adj(k, edges)
    n = 2 * k
    reach = {}
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        for d in range(n):
            reach[(s, d)] = d in r
    return reach

def reach_preserved(k, orig, edges):
    cur = all_pairs_reach(k, edges)
    for pair, was in orig.items():
        if was and not cur.get(pair, False):
            return False
    return True

def random_matrix(k):
    vals = list(range(1, k*k+1))
    random.shuffle(vals)
    return [vals[i*k:(i+1)*k] for i in range(k)]

def matrix_to_edges(k, M):
    return {(i, k+j, M[i][j]) for i in range(k) for j in range(k)}

def greedy_offline(k, M, n_trials=20):
    """More thorough greedy with many orderings."""
    all_e = matrix_to_edges(k, M)
    orig = all_pairs_reach(k, all_e)
    best = None
    for _ in range(n_trials):
        el = list(all_e)
        random.shuffle(el)
        cur = set(all_e)
        for e in el:
            trial = cur - {e}
            if reach_preserved(k, orig, trial):
                cur = trial
        if best is None or len(cur) < len(best):
            best = cur
    return best

def best_response_seq(k, M, order=None, max_rounds=100):
    all_e = matrix_to_edges(k, M)
    orig = all_pairs_reach(k, all_e)
    cur = set(all_e)
    n = 2 * k
    if order is None:
        order = list(range(n))
    for rnd in range(1, max_rounds+1):
        dropped = False
        for node in order:
            while True:
                node_e = [e for e in cur if e[0] == node or e[1] == node]
                found = False
                for e in node_e:
                    trial = cur - {e}
                    if reach_preserved(k, orig, trial):
                        cur = trial
                        dropped = True
                        found = True
                        break
                if not found:
                    break
        if not dropped:
            return cur, rnd
    return cur, max_rounds


random.seed(123)

print("="*70)
print("DEEP DIVE: Are budget violations due to inherent graph structure?")
print("="*70)

for k in [4, 5, 6, 7]:
    budget = 4*k - 3
    violations = 0
    greedy_also_over = 0
    total = 100
    nash_counts = []
    greedy_counts = []

    for t in range(total):
        M = random_matrix(k)

        # Thorough greedy (20 trials)
        g = greedy_offline(k, M, n_trials=20)
        gc = len(g)
        greedy_counts.append(gc)

        # Best Nash across 10 orderings
        best_nash = None
        for _ in range(10):
            order = list(range(2*k))
            random.shuffle(order)
            ne, _ = best_response_seq(k, M, order)
            if best_nash is None or len(ne) < len(best_nash):
                best_nash = ne
        nc = len(best_nash)
        nash_counts.append(nc)

        if nc > budget:
            violations += 1
            if gc > budget:
                greedy_also_over += 1

    print(f"\nk={k}, budget={budget}, tested={total}")
    print(f"  Nash violations: {violations}/{total}")
    print(f"  Of those, greedy also over budget: {greedy_also_over}/{violations if violations else 1}")
    print(f"  Nash: mean={statistics.mean(nash_counts):.1f} [{min(nash_counts)}-{max(nash_counts)}]")
    print(f"  Greedy: mean={statistics.mean(greedy_counts):.1f} [{min(greedy_counts)}-{max(greedy_counts)}]")

    # Check: is the MINIMUM possible spanner ever > budget?
    over_both = sum(1 for i in range(total)
                    if nash_counts[i] > budget and greedy_counts[i] > budget)
    under_both = sum(1 for i in range(total)
                     if nash_counts[i] <= budget and greedy_counts[i] <= budget)
    nash_only_over = sum(1 for i in range(total)
                         if nash_counts[i] > budget and greedy_counts[i] <= budget)
    greedy_only_over = sum(1 for i in range(total)
                           if nash_counts[i] <= budget and greedy_counts[i] > budget)
    print(f"  Both ≤ budget: {under_both}, Both > budget: {over_both}")
    print(f"  Nash only over: {nash_only_over}, Greedy only over: {greedy_only_over}")

    # Gap distribution
    gaps = [nash_counts[i] - greedy_counts[i] for i in range(total)]
    print(f"  Nash-Greedy gap: mean={statistics.mean(gaps):.2f}, "
          f"[{min(gaps)}, {max(gaps)}], stdev={statistics.stdev(gaps):.2f}")

print("\n" + "="*70)
print("KEY QUESTION: When optimal > budget, does Nash also exceed?")
print("="*70)
print("If greedy-also-over ≈ violations, then the budget bound itself")
print("is too tight for some matrices, and Nash is blameless.")
print()
print("If nash-only-over >> 0, then Nash is genuinely worse than optimal.")
