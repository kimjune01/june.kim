#!/usr/bin/env python3
"""
H25 supplementary: growth rate of min_c and scaling behavior.
"""

import itertools
import random
from collections import defaultdict

random.seed(42)


def random_temporal_biclique(n, sparsity=0.5, seed=None):
    rng = random.Random(seed)
    all_edges = [(i, j) for i in range(n) for j in range(n)]
    timestamps_list = list(range(1, n * n + 1))
    rng.shuffle(timestamps_list)
    timestamps = {}
    for idx, (i, j) in enumerate(all_edges):
        if rng.random() > sparsity:
            timestamps[(i, j)] = timestamps_list[idx]
    return timestamps


def direct_neighborhoods(n, timestamps):
    neighborhoods = {}
    for i in range(n):
        reachable = frozenset(j for j in range(n) if (i, j) in timestamps)
        neighborhoods[i] = reachable
    return neighborhoods


def build_exchange_graph(neighborhoods, max_sym_diff):
    emitters = sorted(neighborhoods.keys())
    adj = defaultdict(set)
    for i, j in itertools.combinations(emitters, 2):
        sd = len(neighborhoods[i].symmetric_difference(neighborhoods[j]))
        if sd <= max_sym_diff:
            adj[i].add(j)
            adj[j].add(i)
    return dict(adj), emitters


def is_connected(adj, vertices):
    if not vertices:
        return True
    visited = set()
    queue = [vertices[0]]
    visited.add(vertices[0])
    while queue:
        v = queue.pop(0)
        for u in adj.get(v, set()):
            if u not in visited:
                visited.add(u)
                queue.append(u)
    return len(visited) == len(vertices)


def greedy_hp(adj, vertices):
    """Greedy HP with Warnsdorff heuristic, try all starts."""
    best = None
    for start in vertices:
        path = [start]
        visited = {start}
        while len(path) < len(vertices):
            current = path[-1]
            cands = adj.get(current, set()) - visited
            if not cands:
                break
            nxt = min(cands, key=lambda v: len(adj.get(v, set()) - visited))
            path.append(nxt)
            visited.add(nxt)
        if len(path) == len(vertices):
            return path, True
        if best is None or len(path) > len(best):
            best = path
    return best, (best is not None and len(best) == len(vertices))


def find_hamiltonian_path_exact(adj, vertices, timeout_nodes=500000):
    """Exact HP with node count limit."""
    n = len(vertices)
    if n <= 1:
        return vertices[:] if vertices else [], True

    nodes_explored = [0]

    def bt(path, visited):
        nodes_explored[0] += 1
        if nodes_explored[0] > timeout_nodes:
            return False
        if len(path) == n:
            return True
        current = path[-1]
        for nxt in sorted(adj.get(current, set()) - visited,
                          key=lambda v: len(adj.get(v, set()) - visited)):
            path.append(nxt)
            visited.add(nxt)
            if bt(path, visited):
                return True
            path.pop()
            visited.remove(nxt)
        return False

    for start in vertices:
        nodes_explored[0] = 0
        path = [start]
        visited = {start}
        if bt(path, visited):
            return path, True
    return None, False


def min_c_for_hp(neighborhoods, use_exact=True, max_c=None):
    """Find minimum c such that c-distance graph has a Hamiltonian path."""
    emitters = sorted(neighborhoods.keys())
    n = len(emitters)
    if n <= 1:
        return 0
    if max_c is None:
        max_c = 2 * n

    for c in range(1, max_c + 1):
        adj, verts = build_exchange_graph(neighborhoods, max_sym_diff=c)
        if not is_connected(adj, verts):
            continue
        if use_exact and n <= 12:
            path, found = find_hamiltonian_path_exact(adj, verts)
        else:
            path, found = greedy_hp(adj, verts)
        if found:
            return c
    return max_c + 1


# ═══════════════════════════════════════════════════════════════════════════
# Growth rate of min_c
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("GROWTH RATE: min_c vs n (direct neighborhoods, sparsity=0.7)")
print("=" * 70)

sparsity = 0.7
num_trials = 30

for n in [4, 6, 8, 10, 12, 14, 16, 20]:
    use_exact = (n <= 12)
    min_cs = []
    for trial in range(num_trials):
        ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
        nbrs = direct_neighborhoods(n, ts)
        if len(set(nbrs.values())) <= 1:
            min_cs.append(0)
            continue
        mc = min_c_for_hp(nbrs, use_exact=use_exact)
        min_cs.append(mc)

    valid = [x for x in min_cs if x < 100]
    if valid:
        mean_c = sum(valid) / len(valid)
        max_c = max(valid)
        median_c = sorted(valid)[len(valid)//2]
        print(f"  n={n:>2}: mean={mean_c:.1f}, median={median_c}, max={max_c}, "
              f"ratio_to_n={mean_c/n:.2f}"
              f"{'  (greedy upper bound)' if not use_exact else ''}")


# ═══════════════════════════════════════════════════════════════════════════
# Connectivity threshold
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("CONNECTIVITY THRESHOLD: min c for connectivity")
print("=" * 70)

for n in [4, 6, 8, 10, 12, 14, 16, 20]:
    min_conn_cs = []
    for trial in range(num_trials):
        ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
        nbrs = direct_neighborhoods(n, ts)
        if len(set(nbrs.values())) <= 1:
            min_conn_cs.append(0)
            continue
        for c in range(1, 2*n+1):
            adj, verts = build_exchange_graph(nbrs, max_sym_diff=c)
            if is_connected(adj, verts):
                min_conn_cs.append(c)
                break
        else:
            min_conn_cs.append(2*n+1)

    valid = [x for x in min_conn_cs if x < 100]
    if valid:
        mean_c = sum(valid) / len(valid)
        max_c = max(valid)
        print(f"  n={n:>2}: mean={mean_c:.1f}, max={max_c}, ratio={mean_c/n:.2f}")


# ═══════════════════════════════════════════════════════════════════════════
# Compare: matroid basis exchange vs arbitrary neighborhoods
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("MATROID TEST: Do neighborhoods form transversal matroid bases?")
print("=" * 70)

for n in [6, 8, 10]:
    uniform_size = 0
    total = 0
    for trial in range(num_trials):
        ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
        nbrs = direct_neighborhoods(n, ts)
        total += 1
        sizes = [len(s) for s in nbrs.values()]
        if len(set(sizes)) == 1:
            uniform_size += 1

    print(f"  n={n}: uniform-size neighborhoods: {uniform_size}/{total}")
    print(f"    -> neighborhoods are NOT matroid bases (non-uniform sizes)")

    # But are same-size neighborhoods related by basis exchange?
    exchange_pairs = 0
    exchange_holds = 0
    for trial in range(min(num_trials, 10)):
        ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
        nbrs = direct_neighborhoods(n, ts)
        all_nbrs = set(nbrs.values())
        emitters = list(range(n))
        for i, j in itertools.combinations(emitters, 2):
            if len(nbrs[i]) != len(nbrs[j]):
                continue
            B1, B2 = nbrs[i], nbrs[j]
            diff = B1 - B2
            if not diff:
                exchange_pairs += 1
                exchange_holds += 1
                continue
            exchange_pairs += 1
            ok = True
            for e in diff:
                found = any((B1 - {e}) | {f} in all_nbrs for f in B2 - B1)
                if not found:
                    ok = False
                    break
            if ok:
                exchange_holds += 1

    print(f"    same-size pairs with basis exchange: {exchange_holds}/{exchange_pairs}")


# ═══════════════════════════════════════════════════════════════════════════
# Key question: does min_c grow as O(1), O(log n), or O(n)?
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("SCALING SUMMARY")
print("=" * 70)
print("  If min_c / n stays constant -> O(n) growth -> matroid exchange NOT useful")
print("  If min_c / log(n) stays constant -> O(log n) -> partial help")
print("  If min_c stays constant -> O(1) -> matroid exchange gives SJT-like ordering")

import math
for n in [4, 6, 8, 10, 12, 14, 16, 20]:
    use_exact = (n <= 12)
    min_cs = []
    for trial in range(num_trials):
        ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
        nbrs = direct_neighborhoods(n, ts)
        if len(set(nbrs.values())) <= 1:
            continue
        mc = min_c_for_hp(nbrs, use_exact=use_exact)
        min_cs.append(mc)

    if min_cs:
        mean_c = sum(min_cs) / len(min_cs)
        print(f"  n={n:>2}: mean_c={mean_c:.1f}, "
              f"c/n={mean_c/n:.3f}, "
              f"c/log(n)={mean_c/math.log2(n):.2f}, "
              f"c/sqrt(n)={mean_c/math.sqrt(n):.2f}")
