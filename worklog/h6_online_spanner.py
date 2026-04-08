#!/usr/bin/env python3
"""H6: Online edge count analysis for temporal spanner construction."""

import random
import itertools
from collections import defaultdict

random.seed(42)

# ── Temporal reachability via transitive closure ──

def sm_matrix(k):
    """Generate SM(k) timestamp matrix."""
    M = [[0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            M[i][j] = i*k + ((i+j) % k) + 1
    return M

def random_distinct_matrix(k):
    """Generate random k×k matrix with all-distinct entries."""
    vals = list(range(1, k*k + 1))
    random.shuffle(vals)
    M = [[0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            M[i][j] = vals[i*k + j]
    return M

def edges_sorted(M, k, order='forward'):
    """Return edges sorted by timestamp. Each edge: (time, a_i, b_j)."""
    edges = []
    for i in range(k):
        for j in range(k):
            edges.append((M[i][j], i, j))
    if order == 'forward':
        edges.sort(key=lambda e: e[0])
    elif order == 'reverse':
        edges.sort(key=lambda e: -e[0])
    elif order == 'random':
        random.shuffle(edges)
    return edges

def compute_reachable_pairs(spanner_edges, k):
    """
    Compute all reachable pairs in the temporal graph defined by spanner_edges.
    Vertices: a_0..a_{k-1} (indices 0..k-1), b_0..b_{k-1} (indices k..2k-1).
    A temporal journey: sequence of edges with non-decreasing timestamps.
    Reachable pair (u,v): exists a temporal journey from u to v.
    """
    n = 2 * k
    # Sort spanner edges by timestamp
    sorted_edges = sorted(spanner_edges, key=lambda e: e[0])

    # reach[u] = set of vertices reachable from u
    # We build this incrementally: process edges in timestamp order.
    # For each edge (t, a_i, b_j), vertex a_i (index i) connects to b_j (index k+j).
    # Anyone who can reach a_i by time t can now also reach everything b_j can reach after time t.
    # And anyone who can reach b_j... wait, edges are bipartite A->B only? No.
    # Edges are undirected in a biclique. A temporal journey can go A->B->A->B...
    # with non-decreasing timestamps.

    # Floyd-Warshall style on timestamps:
    # reach_from[u] = set of (vertex, latest_arrival_time) pairs
    # This is complex. Let me use a simpler approach:
    #
    # For each vertex u, compute all vertices reachable via temporal journey.
    # Use BFS/DFS over edges in timestamp order.

    # Efficient approach: for each source vertex, do a sweep over sorted edges.
    # maintain "active" set = vertices reachable from source at current time.
    # When processing edge (t, a_i, b_j):
    #   if a_i (or b_j) is in active set, add b_j (or a_i) to active set.
    # But we need NON-DECREASING timestamps, so same-time edges can all be used.
    # Group edges by timestamp.

    from collections import defaultdict as dd
    time_groups = dd(list)
    for (t, ai, bj) in sorted_edges:
        time_groups[t].append((ai, k + bj))  # map to vertex indices

    times = sorted(time_groups.keys())

    # For each source, sweep through time groups
    reachable = set()
    for src in range(n):
        active = {src}
        for t in times:
            # Check which edges in this time group connect to active set
            # Need fixed-point within same timestamp group
            changed = True
            while changed:
                changed = False
                for (u, v) in time_groups[t]:
                    if u in active and v not in active:
                        active.add(v)
                        changed = True
                    if v in active and u not in active:
                        active.add(u)
                        changed = True
        for dst in active:
            if dst != src:
                reachable.add((src, dst))

    return reachable

def online_construction(M, k, order='forward'):
    """
    Online greedy spanner construction.
    Process edges in given order. Add edge only if it creates new reachable pairs.
    Returns: list of (edge_rank, timestamp, ai, bj, new_pairs_count, cumulative_edges, total_reachable)
    """
    edges = edges_sorted(M, k, order)
    spanner = []
    history = []
    current_reachable = set()

    for rank, (t, ai, bj) in enumerate(edges):
        # Try adding this edge
        candidate = spanner + [(t, ai, bj)]
        new_reachable = compute_reachable_pairs(candidate, k)
        new_pairs = new_reachable - current_reachable

        if len(new_pairs) > 0:
            spanner.append((t, ai, bj))
            current_reachable = new_reachable
            history.append({
                'rank': rank,
                'time': t,
                'ai': ai,
                'bj': bj,
                'new_pairs': len(new_pairs),
                'cum_edges': len(spanner),
                'total_reachable': len(current_reachable),
            })

    return spanner, history, current_reachable

def max_reachable_pairs(k):
    """Total possible directed reachable pairs in a 2k-vertex graph = 2k*(2k-1)."""
    n = 2*k
    return n * (n - 1)

# ── Part 1: SM(k) analysis ──

print("=" * 70)
print("PART 1: SM(k) Online Construction")
print("=" * 70)

sm_results = {}
for k in [3, 4, 5, 6, 7, 8]:
    n = 2 * k
    M = sm_matrix(k)
    spanner, history, reachable = online_construction(M, k, 'forward')
    sm_results[k] = (spanner, history, reachable)

    total_possible = max_reachable_pairs(k)
    offline_opt = 4*k - 4
    conjecture_bound = 2*n - 3

    print(f"\nk={k} (n={n}):")
    print(f"  Final edge count: {len(spanner)}")
    print(f"  Offline optimal (4k-4): {offline_opt}")
    print(f"  Conjecture bound (2n-3): {conjecture_bound}")
    print(f"  Overshoot vs offline: {len(spanner) - offline_opt}")
    print(f"  Reachable pairs: {len(reachable)} / {total_possible}")

    # First half vs second half
    total_timestamps = k * k
    half = total_timestamps // 2
    first_half = sum(1 for h in history if h['rank'] < half)
    second_half = len(history) - first_half
    print(f"  Edges added in first half: {first_half}, second half: {second_half}")

    # Phase transition: last rank where an edge was added
    if history:
        last_rank = history[-1]['rank']
        print(f"  Last edge added at rank {last_rank}/{total_timestamps-1} (timestamp {history[-1]['time']})")

    # Growth detail
    print(f"  Growth: ", end="")
    for h in history:
        print(f"r{h['rank']}:e{h['cum_edges']}(+{h['new_pairs']}p) ", end="")
    print()

# ── Part 2: Random matrices ──

print("\n" + "=" * 70)
print("PART 2: Random Matrices (50 trials each)")
print("=" * 70)

for k in [4, 5, 6, 7]:
    n = 2 * k
    offline_opt = 4*k - 4
    conjecture_bound = 2*n - 3
    edge_counts = []

    for trial in range(50):
        M = random_distinct_matrix(k)
        spanner, history, reachable = online_construction(M, k, 'forward')
        edge_counts.append(len(spanner))

    mean_ec = sum(edge_counts) / len(edge_counts)
    min_ec = min(edge_counts)
    max_ec = max(edge_counts)
    variance = sum((x - mean_ec)**2 for x in edge_counts) / len(edge_counts)
    stddev = variance ** 0.5
    over_conjecture = sum(1 for x in edge_counts if x > conjecture_bound)

    print(f"\nk={k} (n={n}):")
    print(f"  Offline optimal: {offline_opt}, Conjecture bound: {conjecture_bound}")
    print(f"  Mean: {mean_ec:.1f}, Stddev: {stddev:.1f}")
    print(f"  Min: {min_ec}, Max: {max_ec}")
    print(f"  Over conjecture bound: {over_conjecture}/50")
    print(f"  Mean overshoot vs offline: {mean_ec - offline_opt:.1f}")

# ── Part 3: Order sensitivity ──

print("\n" + "=" * 70)
print("PART 3: Order Sensitivity (SM matrices)")
print("=" * 70)

for k in [3, 4, 5, 6, 7]:
    n = 2 * k
    M = sm_matrix(k)

    _, hist_fwd, _ = online_construction(M, k, 'forward')
    _, hist_rev, _ = online_construction(M, k, 'reverse')

    # Multiple random orderings
    random_counts = []
    for _ in range(20):
        _, hist_rnd, _ = online_construction(M, k, 'random')
        random_counts.append(len(hist_rnd))

    mean_rnd = sum(random_counts) / len(random_counts)

    print(f"\nk={k} (n={n}):")
    print(f"  Forward (timestamp order): {len(hist_fwd)} edges")
    print(f"  Reverse (latest first):    {len(hist_rev)} edges")
    print(f"  Random (20 trials):        mean={mean_rnd:.1f}, min={min(random_counts)}, max={max(random_counts)}")

# ── Part 4: Order sensitivity on RANDOM matrices ──

print("\n" + "=" * 70)
print("PART 4: Order Sensitivity (Random matrices, k=5)")
print("=" * 70)

k = 5
n = 2 * k
for trial in range(10):
    M = random_distinct_matrix(k)
    _, hist_fwd, _ = online_construction(M, k, 'forward')
    _, hist_rev, _ = online_construction(M, k, 'reverse')
    random_counts = []
    for _ in range(10):
        _, hist_rnd, _ = online_construction(M, k, 'random')
        random_counts.append(len(hist_rnd))
    mean_rnd = sum(random_counts) / len(random_counts)
    print(f"  Trial {trial}: fwd={len(hist_fwd)}, rev={len(hist_rev)}, rnd_mean={mean_rnd:.1f} (min={min(random_counts)}, max={max(random_counts)})")

# ── Summary ──

print("\n" + "=" * 70)
print("SUMMARY TABLE: SM(k) final edge counts")
print("=" * 70)
print(f"{'k':>3} {'n':>4} {'online':>7} {'4k-4':>5} {'2n-3':>5} {'overshoot':>10} {'gap_type':>10}")
for k in [3, 4, 5, 6, 7, 8]:
    n = 2*k
    spanner, history, _ = sm_results[k]
    ec = len(spanner)
    opt = 4*k - 4
    conj = 2*n - 3
    gap = ec - opt
    print(f"{k:>3} {n:>4} {ec:>7} {opt:>5} {conj:>5} {gap:>10} {'':>10}")
