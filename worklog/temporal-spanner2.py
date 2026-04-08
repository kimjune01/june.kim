"""
Phase 2: Systematic search for adversarial timestamp assignments
that maximize minimum spanner size.

Key insight from Phase 1: forced edges (edges in ALL journeys for some pair)
are too conservative. The minimum spanner can be much larger because of
combinatorial dependencies between pairs.
"""

from itertools import combinations, permutations
from collections import defaultdict
import math
import random

def build_adj(n, timestamps):
    adj = defaultdict(list)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t, (u, v)))
        adj[v].append((u, t, (u, v)))
    for v in adj:
        adj[v].sort(key=lambda x: x[1])
    return adj


def check_reachability_subset(n, timestamps):
    """Check all-pairs reachability. Returns set of reachable pairs."""
    adj = defaultdict(list)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t))
        adj[v].append((u, t))

    reachable = set()
    for src in range(n):
        # BFS/relaxation from src
        best = {src: 0}
        changed = True
        while changed:
            changed = False
            for v in list(best.keys()):
                mt = best[v]
                for (w, t) in adj[v]:
                    if t >= mt:
                        if w not in best or t < best[w]:
                            best[w] = t
                            changed = True
        for dst in best:
            if dst != src:
                reachable.add((src, dst))
    return reachable


def find_all_journeys(n, timestamps, src, dst, max_j=500):
    """Find all journeys from src to dst (up to max_j)."""
    adj = build_adj(n, timestamps)
    journeys = []

    def dfs(cur, last_t, path_edges, visited):
        if len(journeys) >= max_j:
            return
        if cur == dst:
            journeys.append(frozenset(path_edges))
            return
        for (w, t, edge) in adj[cur]:
            if t >= last_t and w not in visited:
                visited.add(w)
                path_edges.append(edge)
                dfs(w, t, path_edges, visited)
                path_edges.pop()
                visited.remove(w)

    dfs(src, 0, [], {src})
    return journeys


def exact_min_spanner(n, timestamps):
    """
    Compute exact minimum spanner using the hitting set formulation.
    For each reachable pair (s,t), find all journeys (as edge sets).
    A valid spanner must contain at least one complete journey for each pair.
    This is a minimum weight set cover / hitting set problem.
    """
    edges = list(timestamps.keys())
    m = len(edges)
    edge_idx = {e: i for i, e in enumerate(edges)}

    full_reach = check_reachability_subset(n, timestamps)

    # For each pair, compute journey edge-sets as bitmasks
    pair_options = []  # list of (pair, list of bitmasks)
    for (s, d) in full_reach:
        journeys = find_all_journeys(n, timestamps, s, d)
        if not journeys:
            return None  # unreachable — shouldn't happen
        masks = []
        for j in journeys:
            mask = 0
            for e in j:
                mask |= (1 << edge_idx[e])
            masks.append(mask)
        pair_options.append(((s, d), masks))

    # Binary search on spanner size + bitmask enumeration
    def is_valid_spanner(mask):
        for (pair, options) in pair_options:
            ok = False
            for jm in options:
                if (jm & mask) == jm:
                    ok = True
                    break
            if not ok:
                return False
        return True

    # Check from smallest size upward
    for size in range(1, m + 1):
        for subset in combinations(range(m), size):
            mask = 0
            for i in subset:
                mask |= (1 << i)
            if is_valid_spanner(mask):
                return size
        # Safety: if too many combinations, use greedy
        if math.comb(m, size + 1) > 2_000_000:
            print(f"  Switching to greedy at size {size + 1}")
            return greedy_spanner_size(n, timestamps)

    return m


def greedy_spanner_size(n, timestamps):
    """Greedy: remove edges one by one if removal preserves reachability."""
    edges = list(timestamps.keys())
    full_reach = check_reachability_subset(n, timestamps)
    current = set(edges)

    # Try removing in various orders; try reverse timestamp order (remove latest first)
    for order in [
        sorted(edges, key=lambda e: -timestamps[e]),  # latest first
        sorted(edges, key=lambda e: timestamps[e]),    # earliest first
        sorted(edges, key=lambda e: abs(timestamps[e] - len(edges)//2)),  # middle first
    ]:
        trial = set(edges)
        for e in order:
            trial2 = trial - {e}
            ts2 = {edge: timestamps[edge] for edge in trial2}
            if check_reachability_subset(n, ts2) == full_reach:
                trial = trial2
        if len(trial) < len(current):
            current = trial

    return len(current)


def exhaustive_search_k5():
    """
    For K_5 (10 edges), try ALL possible timestamp assignments (10! = 3.6M)
    to find the one with maximum minimum spanner size.

    This is too slow for all 10!. Sample instead.
    """
    edges = []
    for i in range(5):
        for j in range(i+1, 5):
            edges.append((i, j))
    m = len(edges)  # 10

    best_spanner = 0
    best_ts = None
    count = 0

    # Sample random permutations
    n_samples = 50000
    for _ in range(n_samples):
        perm = list(range(1, m + 1))
        random.shuffle(perm)
        ts = {edges[i]: perm[i] for i in range(m)}

        # Quick check: all-pairs reachable
        reach = check_reachability_subset(5, ts)
        if len(reach) < 20:
            continue

        gs = greedy_spanner_size(5, ts)
        if gs > best_spanner:
            best_spanner = gs
            best_ts = ts.copy()
            print(f"  New best: spanner size {gs}, assignment: {ts}")

        count += 1
        if count % 10000 == 0:
            print(f"  Tried {count} valid assignments, best so far: {best_spanner}")

    return best_spanner, best_ts


def analyze_specific_labeling(n, timestamps):
    """Detailed analysis of a specific labeling."""
    edges = list(timestamps.keys())
    m = len(edges)

    reach = check_reachability_subset(n, timestamps)
    print(f"  Reachable pairs: {len(reach)} / {n*(n-1)}")

    gs = greedy_spanner_size(n, timestamps)
    print(f"  Greedy spanner size: {gs}")
    print(f"  n = {n}, n*lg(n) = {n*math.log2(n):.1f}, ratio = {gs/n:.2f}")

    return gs


def monotone_path_construction(n):
    """
    Try the "monotone path" adversarial construction:
    Label edges so that each vertex has very different in/out temporal neighborhoods.

    Idea: Order vertices 0,...,n-1. Edge (i,j) with i<j gets timestamp f(i,j)
    such that from vertex i, outgoing edges go to j=i+1,...,n-1 in increasing timestamp,
    but these interleave with edges from other vertices.

    Specific construction: edge (i,j) gets timestamp i*n + j.
    This creates a "layered" structure.
    """
    edges = {}
    for i in range(n):
        for j in range(i+1, n):
            edges[(i, j)] = i * n + j
    return edges


def binary_interleave_construction(n):
    """
    Binary interleave: assign timestamps based on a binary tree structure.
    Edge (i,j) gets timestamp based on the level at which i and j diverge
    in a binary representation.

    For edge (i,j), timestamp = encode(i,j) where the encoding creates
    maximal temporal dependencies.
    """
    edges = {}
    t = 1
    # Assign timestamps level by level in a divide-and-conquer fashion
    def assign(vertices, time_start):
        if len(vertices) <= 1:
            return time_start
        mid = len(vertices) // 2
        left = vertices[:mid]
        right = vertices[mid:]
        t = time_start
        # First: all cross edges left->right
        for u in left:
            for v in right:
                edge = (min(u,v), max(u,v))
                edges[edge] = t
                t += 1
        # Then recurse
        t = assign(left, t)
        t = assign(right, t)
        return t

    assign(list(range(n)), 1)
    return edges


def reverse_binary_construction(n):
    """
    Reverse of binary interleave: recurse first, then cross edges.
    This forces journeys to "commit" to a subtree before crossing.
    """
    edges = {}

    def assign(vertices, time_start):
        if len(vertices) <= 1:
            return time_start
        mid = len(vertices) // 2
        left = vertices[:mid]
        right = vertices[mid:]
        t = time_start
        # First recurse
        t = assign(left, t)
        t = assign(right, t)
        # Then cross edges
        for u in left:
            for v in right:
                edge = (min(u,v), max(u,v))
                edges[edge] = t
                t += 1
        return t

    assign(list(range(n)), 1)
    return edges


def bit_reversal_construction(n):
    """
    Assign timestamps by bit-reversal permutation of edge indices.
    """
    edge_list = []
    for i in range(n):
        for j in range(i+1, n):
            edge_list.append((i, j))
    m = len(edge_list)

    # Create a "maximally interleaved" ordering
    # Sort edges by (i XOR j, i+j) to create complex temporal structure
    indexed = list(range(m))
    random.seed(42)

    # Try: sort edges so that edges incident to the same vertex are spread out
    # This should make it hard to find alternative journeys
    edge_order = sorted(range(m), key=lambda idx: (
        edge_list[idx][0] ^ edge_list[idx][1],
        edge_list[idx][0] + edge_list[idx][1]
    ))

    ts = {}
    for rank, idx in enumerate(edge_order):
        ts[edge_list[idx]] = rank + 1
    return ts


def star_interleave_construction(n):
    """
    Interleave star edges: for each vertex v, edges from v get every n-th timestamp.
    Edge from vertex v to vertex w (v < w) in the v-star gets timestamp
    that interleaves with all other stars.

    This should force spanners to keep many edges per star.
    """
    edges = {}
    # For each vertex, list its edges
    stars = defaultdict(list)
    for i in range(n):
        for j in range(i+1, n):
            stars[i].append((i, j))
            stars[j].append((i, j))

    # Assign timestamps round-robin across vertices
    # Round r: give vertex r's (r-th) edge a timestamp
    t = 1
    max_degree = n - 1
    assigned = set()
    for round_num in range(max_degree):
        for v in range(n):
            remaining = [e for e in stars[v] if e not in assigned]
            if round_num < len(remaining):
                e = remaining[round_num]
                if e not in assigned:
                    edges[e] = t
                    assigned.add(e)
                    t += 1

    # Fill any unassigned
    for i in range(n):
        for j in range(i+1, n):
            if (i,j) not in edges:
                edges[(i,j)] = t
                t += 1

    return edges


if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 2: Searching for adversarial labelings")
    print("=" * 60)

    # First: exhaustive search on K_5
    print("\n--- K_5: Random search (50K samples) ---")
    best5, best_ts5 = exhaustive_search_k5()
    print(f"\nK_5 best minimum spanner: {best5}")
    print(f"n*lg(n) = {5*math.log2(5):.1f}")

    # Analyze specific constructions on K_7, K_9
    print("\n--- Named constructions on K_7 ---")
    for name, constructor in [
        ("monotone_path", monotone_path_construction),
        ("binary_interleave", binary_interleave_construction),
        ("reverse_binary", reverse_binary_construction),
        ("bit_reversal", bit_reversal_construction),
        ("star_interleave", star_interleave_construction),
    ]:
        print(f"\n  {name}:")
        ts = constructor(7)
        if len(ts) != 21:
            print(f"    WARNING: only {len(ts)} edges assigned (expected 21)")
            continue
        analyze_specific_labeling(7, ts)

    print("\n--- Named constructions on K_9 ---")
    for name, constructor in [
        ("monotone_path", monotone_path_construction),
        ("binary_interleave", binary_interleave_construction),
        ("reverse_binary", reverse_binary_construction),
        ("bit_reversal", bit_reversal_construction),
        ("star_interleave", star_interleave_construction),
    ]:
        print(f"\n  {name}:")
        ts = constructor(9)
        if len(ts) != 36:
            print(f"    WARNING: only {len(ts)} edges assigned (expected 36)")
            continue
        analyze_specific_labeling(9, ts)

    print("\n--- Named constructions on K_11 ---")
    for name, constructor in [
        ("monotone_path", monotone_path_construction),
        ("binary_interleave", binary_interleave_construction),
        ("reverse_binary", reverse_binary_construction),
        ("star_interleave", star_interleave_construction),
    ]:
        print(f"\n  {name}:")
        ts = constructor(11)
        if len(ts) != 55:
            print(f"    WARNING: only {len(ts)} edges assigned (expected 55)")
            continue
        analyze_specific_labeling(11, ts)

    # Random search on K_7
    print("\n--- K_7: Random search (10K samples) ---")
    edges7 = [(i,j) for i in range(7) for j in range(i+1,7)]
    best7 = 0
    best_ts7 = None
    for trial in range(10000):
        perm = list(range(1, 22))
        random.shuffle(perm)
        ts = {edges7[i]: perm[i] for i in range(21)}
        reach = check_reachability_subset(7, ts)
        if len(reach) < 42:
            continue
        gs = greedy_spanner_size(7, ts)
        if gs > best7:
            best7 = gs
            best_ts7 = ts.copy()
            print(f"  New best: {gs}")
        if (trial+1) % 5000 == 0:
            print(f"  Tried {trial+1}, best: {best7}")

    print(f"\nK_7 best greedy spanner: {best7}")
    print(f"n*lg(n) = {7*math.log2(7):.1f}")

    # Summary table
    print("\n" + "=" * 60)
    print("SUMMARY: Best minimum spanner sizes found")
    print("=" * 60)
    print(f"{'n':>4} {'edges':>6} {'best_spanner':>13} {'n*lg(n)':>8} {'spanner/n':>10} {'spanner/(n*lgn)':>16}")
    for n_val, sp in [(5, best5), (7, best7)]:
        nlgn = n_val * math.log2(n_val)
        print(f"{n_val:>4} {n_val*(n_val-1)//2:>6} {sp:>13} {nlgn:>8.1f} {sp/n_val:>10.2f} {sp/nlgn:>16.3f}")
