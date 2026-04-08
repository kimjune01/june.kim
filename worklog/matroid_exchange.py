#!/usr/bin/env python3
"""
H25: Matroid basis exchange on CPS residual biclique matchings.

Tests whether the exchange graph over emitter collector-neighborhoods
is connected and Hamiltonian, giving a useful ordering for temporal spanners.
"""

import itertools
import random
import sys
from collections import defaultdict

random.seed(42)

# ─── Utilities ───────────────────────────────────────────────────────────

def random_biclique_timestamps(n, seed=None):
    """
    Generate a random complete bipartite temporal graph K_{n,n}.
    Each edge (emitter i, collector j) gets a random timestamp in [1, 2n].
    Returns dict: (i, j) -> timestamp.
    """
    if seed is not None:
        random.seed(seed)
    timestamps = {}
    for i in range(n):
        for j in range(n):
            timestamps[(i, j)] = random.randint(1, 2 * n)
    return timestamps


def compute_temporal_neighborhoods(n, timestamps):
    """
    Compute collector neighborhood N(i) for each emitter i.
    N(i) = set of collectors reachable via 2-hop temporal journeys from emitter i.

    A 2-hop temporal journey from emitter i to collector j:
      i -> relay_collector c at time t1, then relay_emitter e -> j at time t2, where t1 < t2.

    In a biclique: emitter i sends to collector c at time t(i,c),
    then some emitter e sends to collector j at time t(e,j) where t(i,c) < t(e,j).
    So j is reachable from i if there exist c, e such that t(i,c) < t(e,j).
    """
    neighborhoods = {}
    for i in range(n):
        reachable = set()
        for c in range(n):  # relay collector
            t1 = timestamps[(i, c)]
            for e in range(n):  # relay emitter
                for j in range(n):  # target collector
                    t2 = timestamps[(e, j)]
                    if t1 < t2:
                        reachable.add(j)
        neighborhoods[i] = frozenset(reachable)
    return neighborhoods


def compute_neighborhoods_strict(n, timestamps):
    """
    Stricter 2-hop: emitter i -> collector c (time t1),
    then from c's perspective, another emitter e picks up from c and delivers to j.

    Actually for CPS residual: N(i) = collectors that emitter i can reach
    in the residual after removing the direct matching.

    Simpler model: N(i) = {j : exists c such that t(i,c) < t(c',j) for some path}.

    Let's use the simple version: N(i) = collectors j where min_c t(i,c) < max_e t(e,j).
    This captures "i can start a journey that ends at j".
    """
    neighborhoods = {}
    for i in range(n):
        reachable = set()
        # i's earliest send time to any relay
        min_send = min(timestamps[(i, c)] for c in range(n))
        for j in range(n):
            # j's latest receive time from any emitter
            max_recv = max(timestamps[(e, j)] for e in range(n))
            if min_send < max_recv:
                reachable.add(j)
        neighborhoods[i] = frozenset(reachable)
    return neighborhoods


def build_exchange_graph(neighborhoods, max_sym_diff):
    """
    Build exchange graph: vertices = emitters, edge if |N(i) Δ N(j)| <= max_sym_diff.
    Returns adjacency list.
    """
    emitters = sorted(neighborhoods.keys())
    adj = defaultdict(set)
    for i, j in itertools.combinations(emitters, 2):
        sd = len(neighborhoods[i].symmetric_difference(neighborhoods[j]))
        if sd <= max_sym_diff:
            adj[i].add(j)
            adj[j].add(i)
    return dict(adj), emitters


def is_connected(adj, vertices):
    """BFS connectivity check."""
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


def find_hamiltonian_path(adj, vertices):
    """
    Exact Hamiltonian path search via backtracking.
    Only feasible for small n.
    Returns path if found, None otherwise.
    """
    n = len(vertices)
    if n == 0:
        return []
    if n == 1:
        return [vertices[0]]

    # Try each starting vertex
    for start in vertices:
        path = [start]
        visited = {start}
        if _hp_backtrack(adj, vertices, path, visited, n):
            return path
    return None


def _hp_backtrack(adj, vertices, path, visited, n):
    if len(path) == n:
        return True
    current = path[-1]
    neighbors = sorted(adj.get(current, set()) - visited,
                       key=lambda v: len(adj.get(v, set()) - visited))
    for nxt in neighbors:
        path.append(nxt)
        visited.add(nxt)
        if _hp_backtrack(adj, vertices, path, visited, n):
            return True
        path.pop()
        visited.remove(nxt)
    return False


def greedy_hamiltonian_path(adj, vertices):
    """
    Greedy nearest-neighbor heuristic for HP.
    Returns (path, success).
    """
    if not vertices:
        return [], True

    best_path = None
    for start in vertices:
        path = [start]
        visited = {start}
        while len(path) < len(vertices):
            current = path[-1]
            candidates = adj.get(current, set()) - visited
            if not candidates:
                break
            # Pick neighbor with most remaining connections (Warnsdorff-like)
            nxt = min(candidates, key=lambda v: len(adj.get(v, set()) - visited))
            path.append(nxt)
            visited.add(nxt)
        if len(path) == len(vertices):
            return path, True
        if best_path is None or len(path) > len(best_path):
            best_path = path
    return best_path, len(best_path) == len(vertices)


def compute_delegation_matching(n, timestamps):
    """
    D(i) = primary collector for emitter i = collector with earliest timestamp.
    This gives a matching if all emitters pick distinct collectors.
    """
    delegation = {}
    for i in range(n):
        best_j = min(range(n), key=lambda j: timestamps[(i, j)])
        delegation[i] = best_j
    return delegation


# ─── Task 1: Exchange graph connectivity ─────────────────────────────────

def task1(n_values=(6, 8, 10), num_trials=20):
    print("=" * 70)
    print("TASK 1: Exchange graph connectivity")
    print("=" * 70)

    for n in n_values:
        connected_count = 0
        trivial_count = 0  # all neighborhoods identical
        distinct_neighborhoods = []

        for trial in range(num_trials):
            ts = random_biclique_timestamps(n, seed=trial * 1000 + n)
            nbrs = compute_temporal_neighborhoods(n, ts)

            unique_nbrs = len(set(nbrs.values()))
            distinct_neighborhoods.append(unique_nbrs)

            if unique_nbrs <= 1:
                trivial_count += 1
                connected_count += 1
                continue

            adj, verts = build_exchange_graph(nbrs, max_sym_diff=2)
            conn = is_connected(adj, verts)
            if conn:
                connected_count += 1

        print(f"\nn={n}: {connected_count}/{num_trials} connected (c=2), "
              f"{trivial_count} trivial, "
              f"avg distinct neighborhoods: {sum(distinct_neighborhoods)/num_trials:.1f}")

        # Also check with stricter neighborhoods
        connected_strict = 0
        for trial in range(num_trials):
            ts = random_biclique_timestamps(n, seed=trial * 1000 + n)
            nbrs = compute_neighborhoods_strict(n, ts)
            unique = len(set(nbrs.values()))
            if unique <= 1:
                connected_strict += 1
                continue
            adj, verts = build_exchange_graph(nbrs, max_sym_diff=2)
            if is_connected(adj, verts):
                connected_strict += 1

        print(f"  strict neighborhoods: {connected_strict}/{num_trials} connected (c=2)")


# ─── Task 2: Hamiltonian path search ────────────────────────────────────

def task2(n_values=(6, 8, 10), num_trials=10):
    print("\n" + "=" * 70)
    print("TASK 2: Hamiltonian path search (c=2)")
    print("=" * 70)

    for n in n_values:
        hp_found = 0
        hp_attempted = 0

        for trial in range(num_trials):
            ts = random_biclique_timestamps(n, seed=trial * 1000 + n)
            nbrs = compute_temporal_neighborhoods(n, ts)

            unique_nbrs = set(nbrs.values())
            if len(unique_nbrs) <= 1:
                continue  # trivial

            adj, verts = build_exchange_graph(nbrs, max_sym_diff=2)
            if not is_connected(adj, verts):
                hp_attempted += 1
                continue

            hp_attempted += 1
            if n <= 10:
                path = find_hamiltonian_path(adj, verts)
            else:
                path, _ = greedy_hamiltonian_path(adj, verts)

            if path:
                hp_found += 1
                if trial == 0:
                    # Show first example
                    print(f"\n  n={n}, trial 0: HP found: {path}")
                    for idx in range(len(path) - 1):
                        sd = len(nbrs[path[idx]].symmetric_difference(nbrs[path[idx + 1]]))
                        print(f"    step {idx}: {path[idx]}->{path[idx+1]}, "
                              f"|ΔN|={sd}, N({path[idx]})={set(nbrs[path[idx]])}")

        print(f"\nn={n}: HP found in {hp_found}/{hp_attempted} non-trivial instances (c=2)")


# ─── Task 3: Relaxed exchange ────────────────────────────────────────────

def task3(n_values=(6, 8, 10), num_trials=20):
    print("\n" + "=" * 70)
    print("TASK 3: Relaxed exchange — minimum c for Hamiltonicity")
    print("=" * 70)

    for n in n_values:
        results = {c: {"connected": 0, "hamiltonian": 0, "tested": 0}
                   for c in [2, 3, 4, 5, 6, 8, 10]}

        for trial in range(num_trials):
            ts = random_biclique_timestamps(n, seed=trial * 1000 + n)
            nbrs = compute_temporal_neighborhoods(n, ts)

            if len(set(nbrs.values())) <= 1:
                for c in results:
                    results[c]["connected"] += 1
                    results[c]["hamiltonian"] += 1
                    results[c]["tested"] += 1
                continue

            for c in results:
                results[c]["tested"] += 1
                adj, verts = build_exchange_graph(nbrs, max_sym_diff=c)
                if is_connected(adj, verts):
                    results[c]["connected"] += 1
                    if n <= 10:
                        path = find_hamiltonian_path(adj, verts)
                    else:
                        path, success = greedy_hamiltonian_path(adj, verts)
                        if success:
                            path = path
                        else:
                            path = None
                    if path:
                        results[c]["hamiltonian"] += 1

        print(f"\nn={n}:")
        print(f"  {'c':>3} | {'Connected':>12} | {'Hamiltonian':>12}")
        print(f"  {'-'*3}-+-{'-'*12}-+-{'-'*12}")
        for c in sorted(results.keys()):
            r = results[c]
            print(f"  {c:>3} | {r['connected']:>5}/{r['tested']:<5} | "
                  f"{r['hamiltonian']:>5}/{r['tested']:<5}")


# ─── Task 4: Matroid structure of delegation matchings ───────────────────

def task4(n_values=(6, 8, 10), num_trials=20):
    print("\n" + "=" * 70)
    print("TASK 4: Delegation matchings and matroid basis exchange")
    print("=" * 70)

    for n in n_values:
        is_matching_count = 0
        basis_exchange_holds = 0
        total_pairs = 0

        for trial in range(num_trials):
            ts = random_biclique_timestamps(n, seed=trial * 1000 + n)
            delegation = compute_delegation_matching(n, ts)

            # Check if it's a perfect matching (all collectors distinct)
            collectors_used = set(delegation.values())
            is_perfect = len(collectors_used) == n
            if is_perfect:
                is_matching_count += 1

            # Check basis exchange between consecutive emitters in delegation order
            # Sort emitters by their delegation collector
            sorted_emitters = sorted(range(n), key=lambda i: delegation[i])

            nbrs = compute_temporal_neighborhoods(n, ts)

            for idx in range(len(sorted_emitters) - 1):
                i = sorted_emitters[idx]
                j = sorted_emitters[idx + 1]
                B1 = nbrs[i]
                B2 = nbrs[j]
                diff = B1 - B2
                total_pairs += 1

                # Check: for each e in B1\B2, exists f in B2\B1 s.t. (B1\{e})∪{f}
                # is "valid" (here: is some other emitter's neighborhood)
                all_nbrs = set(nbrs.values())
                exchange_ok = True
                for e in diff:
                    found_f = False
                    for f in B2 - B1:
                        candidate = (B1 - {e}) | {f}
                        # Relaxed check: is this a subset of some neighborhood?
                        # Strict check: is this exactly some neighborhood?
                        if candidate in all_nbrs:
                            found_f = True
                            break
                    if not found_f:
                        exchange_ok = False
                        break
                if exchange_ok or not diff:
                    basis_exchange_holds += 1

        print(f"\nn={n}:")
        print(f"  Perfect matchings: {is_matching_count}/{num_trials}")
        print(f"  Basis exchange holds: {basis_exchange_holds}/{total_pairs} consecutive pairs")


# ─── Task 5: Worst-case instances ────────────────────────────────────────

def compute_min_max_step(n, timestamps):
    """
    For the best ordering σ, compute max_i |N(σ(i)) Δ N(σ(i+1))|.
    Return the min over all orderings of this max step.
    """
    nbrs = compute_temporal_neighborhoods(n, timestamps)
    emitters = list(range(n))

    unique_nbrs = set(nbrs.values())
    if len(unique_nbrs) <= 1:
        return 0

    if n <= 8:
        # Exact: try all permutations
        best = float('inf')
        for perm in itertools.permutations(emitters):
            max_step = max(
                len(nbrs[perm[i]].symmetric_difference(nbrs[perm[i + 1]]))
                for i in range(n - 1)
            )
            best = min(best, max_step)
        return best
    else:
        # Greedy: nearest-neighbor on sym diff
        best = float('inf')
        for start in emitters:
            path = [start]
            visited = {start}
            max_step = 0
            while len(path) < n:
                current = path[-1]
                remaining = [e for e in emitters if e not in visited]
                if not remaining:
                    break
                nxt = min(remaining,
                         key=lambda e: len(nbrs[current].symmetric_difference(nbrs[e])))
                step = len(nbrs[current].symmetric_difference(nbrs[nxt]))
                max_step = max(max_step, step)
                path.append(nxt)
                visited.add(nxt)
            if len(path) == n:
                best = min(best, max_step)
        return best


def task5(n_values=(6, 8), num_hill_climb=50, num_trials=200):
    print("\n" + "=" * 70)
    print("TASK 5: Worst-case instances (hill-climbing on timestamps)")
    print("=" * 70)

    for n in n_values:
        worst_score = 0
        worst_ts = None

        # Random sampling first
        for trial in range(num_trials):
            ts = random_biclique_timestamps(n, seed=trial * 7919 + n)
            score = compute_min_max_step(n, ts)
            if score > worst_score:
                worst_score = score
                worst_ts = dict(ts)

        print(f"\nn={n}: worst min-max step from random sampling = {worst_score}")

        # Hill-climb from worst found
        if worst_ts is not None:
            current_ts = dict(worst_ts)
            current_score = worst_score

            for step in range(num_hill_climb):
                # Perturb: change one random timestamp
                new_ts = dict(current_ts)
                i = random.randint(0, n - 1)
                j = random.randint(0, n - 1)
                new_ts[(i, j)] = random.randint(1, 2 * n)

                new_score = compute_min_max_step(n, new_ts)
                if new_score >= current_score:
                    current_ts = new_ts
                    current_score = new_score

            print(f"  after hill-climbing: worst min-max step = {current_score}")

            # Show the neighborhoods for worst case
            nbrs = compute_temporal_neighborhoods(n, current_ts)
            print(f"  neighborhoods:")
            for i in range(n):
                print(f"    N({i}) = {sorted(nbrs[i])}")

            # Compute pairwise distances
            print(f"  pairwise |ΔN| matrix:")
            for i in range(n):
                row = []
                for j in range(n):
                    row.append(len(nbrs[i].symmetric_difference(nbrs[j])))
                print(f"    {row}")


# ─── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
    task5()
