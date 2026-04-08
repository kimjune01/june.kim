#!/usr/bin/env python3
"""
H25: Matroid basis exchange on CPS residual biclique matchings.
V2: Uses strict temporal reachability to get non-trivial neighborhoods.

Key fix: 2-hop temporal journey i -> j requires:
  - i sends to relay collector c at time t(i,c)
  - The SAME relay c is received by some emitter e who then sends to j
  - Concretely: exists c, e such that t(i,c) < t(e,j) AND e != i AND c != j
  - Even more realistically: each edge has a DISTINCT timestamp (permutation),
    and we require strict time ordering.
"""

import itertools
import random
import sys
from collections import defaultdict

random.seed(42)


def random_temporal_biclique(n, sparsity=0.5, seed=None):
    """
    Generate temporal bipartite graph K_{n,n} where each edge gets a
    UNIQUE timestamp (a permutation of 1..n²), simulating distinct arrival times.
    Then remove edges with probability `sparsity` to create a non-complete temporal graph.
    """
    rng = random.Random(seed)
    all_edges = [(i, j) for i in range(n) for j in range(n)]
    timestamps_list = list(range(1, n * n + 1))
    rng.shuffle(timestamps_list)

    timestamps = {}
    for idx, (i, j) in enumerate(all_edges):
        if rng.random() > sparsity:
            timestamps[(i, j)] = timestamps_list[idx]
    return timestamps


def temporal_neighborhoods_strict(n, timestamps):
    """
    N(i) = collectors reachable from emitter i via a strict 2-hop temporal journey.
    Journey: i -> c at time t1, then e -> j at time t2, where t1 < t2.
    We do NOT require e=i or c=j (that would be a 1-hop).
    But we DO require the journey passes through an intermediate.
    """
    neighborhoods = {}
    for i in range(n):
        reachable = set()
        for c in range(n):
            if (i, c) not in timestamps:
                continue
            t1 = timestamps[(i, c)]
            for e in range(n):
                for j in range(n):
                    if (e, j) not in timestamps:
                        continue
                    t2 = timestamps[(e, j)]
                    if t1 < t2:
                        reachable.add(j)
        neighborhoods[i] = frozenset(reachable)
    return neighborhoods


def temporal_neighborhoods_vertex_disjoint(n, timestamps):
    """
    Stricter: 2-hop journey i -> c -> j via relay emitter e.
    Requires: t(i,c) < t(e,j), e != i, and j != c (truly 2-hop, vertex-disjoint).
    """
    neighborhoods = {}
    for i in range(n):
        reachable = set()
        for c in range(n):
            if (i, c) not in timestamps:
                continue
            t1 = timestamps[(i, c)]
            for e in range(n):
                if e == i:
                    continue
                for j in range(n):
                    if j == c:
                        continue
                    if (e, j) not in timestamps:
                        continue
                    t2 = timestamps[(e, j)]
                    if t1 < t2:
                        reachable.add(j)
        neighborhoods[i] = frozenset(reachable)
    return neighborhoods


def temporal_neighborhoods_3hop(n, timestamps):
    """
    3-hop: i -> c1 at t1, e1 -> c2 at t2, e2 -> j at t3, t1 < t2 < t3.
    Even more restrictive — fewer reachable collectors.
    """
    neighborhoods = {}
    # Precompute: for each (emitter, time), what collectors are available after time t
    send_times = defaultdict(list)  # emitter -> [(time, collector)]
    for (e, c), t in timestamps.items():
        send_times[e].append((t, c))
    for e in send_times:
        send_times[e].sort()

    for i in range(n):
        reachable = set()
        for c1 in range(n):
            if (i, c1) not in timestamps:
                continue
            t1 = timestamps[(i, c1)]
            # Second hop: any emitter e1 sends to c2 at t2 > t1
            for e1 in range(n):
                for c2 in range(n):
                    if (e1, c2) not in timestamps:
                        continue
                    t2 = timestamps[(e1, c2)]
                    if t2 <= t1:
                        continue
                    # Third hop: any emitter e2 sends to j at t3 > t2
                    for e2 in range(n):
                        for j in range(n):
                            if (e2, j) not in timestamps:
                                continue
                            t3 = timestamps[(e2, j)]
                            if t3 > t2:
                                reachable.add(j)
        neighborhoods[i] = frozenset(reachable)
    return neighborhoods


def direct_temporal_neighborhoods(n, timestamps):
    """
    Simplest: N(i) = {j : (i,j) has a timestamp} — direct 1-hop reachability.
    With sparsity, this gives non-trivial subsets.
    """
    neighborhoods = {}
    for i in range(n):
        reachable = set()
        for j in range(n):
            if (i, j) in timestamps:
                reachable.add(j)
        neighborhoods[i] = frozenset(reachable)
    return neighborhoods


def build_exchange_graph(neighborhoods, max_sym_diff):
    adj = defaultdict(set)
    emitters = sorted(neighborhoods.keys())
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


def find_hamiltonian_path(adj, vertices):
    n = len(vertices)
    if n <= 1:
        return vertices[:] if vertices else []

    for start in vertices:
        path = [start]
        visited = {start}
        if _hp_bt(adj, path, visited, n):
            return path
    return None


def _hp_bt(adj, path, visited, n):
    if len(path) == n:
        return True
    current = path[-1]
    for nxt in sorted(adj.get(current, set()) - visited,
                      key=lambda v: len(adj.get(v, set()) - visited)):
        path.append(nxt)
        visited.add(nxt)
        if _hp_bt(adj, path, visited, n):
            return True
        path.pop()
        visited.remove(nxt)
    return False


def greedy_hp(adj, vertices):
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
    return best, len(best) == len(vertices) if best else False


def sym_diff_matrix(neighborhoods):
    emitters = sorted(neighborhoods.keys())
    n = len(emitters)
    mat = [[0]*n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            mat[a][b] = len(neighborhoods[emitters[a]].symmetric_difference(
                neighborhoods[emitters[b]]))
    return mat, emitters


def compute_min_max_step(neighborhoods):
    """Min over all orderings of max consecutive sym_diff."""
    emitters = sorted(neighborhoods.keys())
    n = len(emitters)
    if n <= 1:
        return 0

    if n <= 10:
        best = float('inf')
        for perm in itertools.permutations(emitters):
            mx = max(len(neighborhoods[perm[i]].symmetric_difference(
                neighborhoods[perm[i+1]])) for i in range(n-1))
            best = min(best, mx)
        return best
    else:
        best = float('inf')
        for start in emitters:
            path = [start]
            visited = {start}
            mx = 0
            while len(path) < n:
                current = path[-1]
                remaining = [e for e in emitters if e not in visited]
                nxt = min(remaining,
                         key=lambda e: len(neighborhoods[current].symmetric_difference(
                             neighborhoods[e])))
                mx = max(mx, len(neighborhoods[current].symmetric_difference(
                    neighborhoods[nxt])))
                path.append(nxt)
                visited.add(nxt)
            best = min(best, mx)
        return best


# ═══════════════════════════════════════════════════════════════════════════
# EXPERIMENTS
# ═══════════════════════════════════════════════════════════════════════════

def experiment_sweep():
    """
    Sweep over sparsity and neighborhood models to find the interesting regime.
    """
    print("=" * 70)
    print("SWEEP: Finding the non-trivial regime")
    print("=" * 70)

    for n in [6, 8]:
        for sparsity in [0.3, 0.5, 0.7, 0.85]:
            for model_name, model_fn in [
                ("direct", direct_temporal_neighborhoods),
                ("2hop-vdisjoint", temporal_neighborhoods_vertex_disjoint),
            ]:
                distinct_counts = []
                avg_sizes = []
                for trial in range(20):
                    ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
                    nbrs = model_fn(n, ts)
                    unique = len(set(nbrs.values()))
                    avg_size = sum(len(s) for s in nbrs.values()) / n
                    distinct_counts.append(unique)
                    avg_sizes.append(avg_size)

                avg_distinct = sum(distinct_counts) / len(distinct_counts)
                avg_sz = sum(avg_sizes) / len(avg_sizes)
                print(f"  n={n}, sparse={sparsity}, model={model_name:16s}: "
                      f"avg_distinct={avg_distinct:.1f}, avg_|N|={avg_sz:.1f}")
        print()


def task1_v2(n_values=(6, 8, 10), num_trials=30, sparsity=0.7):
    """Direct neighborhoods with sparsity — non-trivial subsets."""
    print("\n" + "=" * 70)
    print(f"TASK 1 v2: Exchange graph (direct neighborhoods, sparsity={sparsity})")
    print("=" * 70)

    for n in n_values:
        for c in [1, 2, 3, 4]:
            conn = 0
            non_trivial = 0
            for trial in range(num_trials):
                ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
                nbrs = direct_temporal_neighborhoods(n, ts)
                if len(set(nbrs.values())) <= 1:
                    conn += 1
                    continue
                non_trivial += 1
                adj, verts = build_exchange_graph(nbrs, max_sym_diff=c)
                if is_connected(adj, verts):
                    conn += 1

            print(f"  n={n}, c={c}: connected {conn}/{num_trials} "
                  f"({non_trivial} non-trivial)")


def task2_v2(n_values=(6, 8, 10), num_trials=30, sparsity=0.7):
    print("\n" + "=" * 70)
    print(f"TASK 2 v2: Hamiltonian path (direct, sparsity={sparsity})")
    print("=" * 70)

    for n in n_values:
        for c in [1, 2, 3, 4, 5, 6]:
            hp_found = 0
            tested = 0
            for trial in range(num_trials):
                ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
                nbrs = direct_temporal_neighborhoods(n, ts)
                if len(set(nbrs.values())) <= 1:
                    continue
                tested += 1
                adj, verts = build_exchange_graph(nbrs, max_sym_diff=c)
                if not is_connected(adj, verts):
                    continue
                if n <= 10:
                    path = find_hamiltonian_path(adj, verts)
                else:
                    path, ok = greedy_hp(adj, verts)
                    if not ok:
                        path = None
                if path:
                    hp_found += 1

            print(f"  n={n}, c={c}: HP {hp_found}/{tested} non-trivial")


def task3_v2(n_values=(6, 8, 10), num_trials=30, sparsity=0.7):
    print("\n" + "=" * 70)
    print(f"TASK 3 v2: Min c for Hamiltonicity (direct, sparsity={sparsity})")
    print("=" * 70)

    for n in n_values:
        min_c_list = []
        for trial in range(num_trials):
            ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
            nbrs = direct_temporal_neighborhoods(n, ts)
            if len(set(nbrs.values())) <= 1:
                min_c_list.append(0)
                continue

            found_c = None
            for c in range(1, 2*n+1):
                adj, verts = build_exchange_graph(nbrs, max_sym_diff=c)
                if not is_connected(adj, verts):
                    continue
                if n <= 10:
                    path = find_hamiltonian_path(adj, verts)
                else:
                    path, ok = greedy_hp(adj, verts)
                    if not ok:
                        path = None
                if path:
                    found_c = c
                    break
            min_c_list.append(found_c if found_c else 999)

        valid = [x for x in min_c_list if x < 999]
        if valid:
            print(f"  n={n}: min_c stats: mean={sum(valid)/len(valid):.1f}, "
                  f"max={max(valid)}, "
                  f"distribution={sorted(valid)}")
        else:
            print(f"  n={n}: no valid instances found")


def task4_v2(n_values=(6, 8), num_trials=30, sparsity=0.7):
    print("\n" + "=" * 70)
    print(f"TASK 4 v2: Matroid structure (direct, sparsity={sparsity})")
    print("=" * 70)

    for n in n_values:
        total_pairs = 0
        exchange_holds = 0
        sizes_are_equal = 0

        for trial in range(num_trials):
            ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*1000+n)
            nbrs = direct_temporal_neighborhoods(n, ts)
            all_nbr_sets = set(nbrs.values())

            # Check if neighborhoods form a matroid (uniform size = necessary condition)
            sizes = [len(s) for s in nbrs.values()]
            if len(set(sizes)) == 1 and len(sizes) > 0:
                sizes_are_equal += 1

            # Check basis exchange for all pairs
            emitters = list(range(n))
            for i, j in itertools.combinations(emitters, 2):
                B1 = nbrs[i]
                B2 = nbrs[j]
                if len(B1) != len(B2):
                    total_pairs += 1
                    continue  # Can't be bases of same matroid

                diff = B1 - B2
                total_pairs += 1

                exchange_ok = True
                for e in diff:
                    found_f = False
                    for f in B2 - B1:
                        candidate = (B1 - {e}) | {f}
                        if candidate in all_nbr_sets:
                            found_f = True
                            break
                    if not found_f:
                        exchange_ok = False
                        break
                if exchange_ok:
                    exchange_holds += 1

        print(f"\n  n={n}:")
        print(f"    Uniform-size neighborhoods: {sizes_are_equal}/{num_trials}")
        print(f"    Basis exchange holds: {exchange_holds}/{total_pairs}")


def task5_v2(n_values=(6, 8), num_random=200, num_hill=100, sparsity=0.7):
    print("\n" + "=" * 70)
    print(f"TASK 5 v2: Worst-case min-max step (direct, sparsity={sparsity})")
    print("=" * 70)

    rng = random.Random(999)

    for n in n_values:
        worst_score = 0
        worst_ts = None
        worst_nbrs = None

        for trial in range(num_random):
            ts = random_temporal_biclique(n, sparsity=sparsity, seed=trial*7919+n)
            nbrs = direct_temporal_neighborhoods(n, ts)
            if len(set(nbrs.values())) <= 1:
                continue
            score = compute_min_max_step(nbrs)
            if score > worst_score:
                worst_score = score
                worst_ts = dict(ts)
                worst_nbrs = dict(nbrs)

        print(f"\n  n={n}: worst min-max step from random = {worst_score}")

        # Hill-climb
        if worst_ts:
            current_ts = dict(worst_ts)
            current_score = worst_score
            for step in range(num_hill):
                new_ts = dict(current_ts)
                i = rng.randint(0, n-1)
                j = rng.randint(0, n-1)
                if rng.random() < 0.5:
                    # Toggle edge existence
                    if (i, j) in new_ts:
                        del new_ts[(i, j)]
                    else:
                        new_ts[(i, j)] = rng.randint(1, n*n)
                else:
                    if (i, j) in new_ts:
                        new_ts[(i, j)] = rng.randint(1, n*n)

                nbrs = direct_temporal_neighborhoods(n, new_ts)
                if len(set(nbrs.values())) <= 1:
                    continue
                score = compute_min_max_step(nbrs)
                if score >= current_score:
                    current_ts = new_ts
                    current_score = score

            print(f"    after hill-climbing: worst min-max step = {current_score}")

            nbrs = direct_temporal_neighborhoods(n, current_ts)
            print(f"    neighborhoods:")
            for i in range(n):
                print(f"      N({i}) = {sorted(nbrs[i])}")

            mat, emitters = sym_diff_matrix(nbrs)
            print(f"    |ΔN| matrix:")
            for row in mat:
                print(f"      {row}")

            # What's the actual optimal ordering?
            best_perm = None
            best_max = float('inf')
            if n <= 8:
                for perm in itertools.permutations(emitters):
                    mx = max(len(nbrs[perm[i]].symmetric_difference(
                        nbrs[perm[i+1]])) for i in range(n-1))
                    if mx < best_max:
                        best_max = mx
                        best_perm = perm
                print(f"    optimal ordering: {best_perm} with max step = {best_max}")


if __name__ == "__main__":
    experiment_sweep()
    task1_v2()
    task2_v2()
    task3_v2()
    task4_v2()
    task5_v2()
