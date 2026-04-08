#!/usr/bin/env python3
"""
H27 Part 4: Correct model — CPS operates on K_n, not K_{k,k}.

Critical insight from Part 3: the bipartite K_{k,k} model is WRONG for
the CPS spanner. CPS works on the COMPLETE temporal graph K_n (not bipartite).

The 2n-3 conjecture: every temporal K_n has a 2-hop temporal spanner with ≤ 2n-3 edges.

In K_n, edges are between ALL pairs of n vertices. The bipartite structure
(emitters vs collectors) is an ARTIFACT of the dismountability analysis,
not the actual graph.

This script:
1. Compute exact minimum temporal spanners for K_n
2. Test whether star+tree construction achieves 2n-3
3. Test sequential delegation on K_n directly
4. Verify against the known results from the worklog
"""

import random
import math
from collections import defaultdict
from itertools import combinations


def random_temporal_clique(n, seed=None):
    """
    K_n temporal clique: each edge {u,v} gets a distinct timestamp.
    Returns: timestamp dict {frozenset({u,v}): t}
    """
    rng = random.Random(seed)
    edges = list(combinations(range(n), 2))
    timestamps = rng.sample(range(1, len(edges) * 10 + 1), len(edges))
    return {frozenset(e): t for e, t in zip(edges, timestamps)}


def temporal_reachability(n, timestamps, edge_set=None):
    """
    Compute all temporally reachable pairs.

    A temporal journey from u to v: sequence of edges e1, e2, ..., el
    where consecutive edges share a vertex and t(e1) < t(e2) < ... < t(el).

    If edge_set is None, use all edges. Otherwise, only use edges in edge_set.
    """
    # Build sorted edge list
    if edge_set is None:
        edge_set = set(timestamps.keys())

    edges = [(e, timestamps[e]) for e in edge_set]
    edges.sort(key=lambda x: x[1])

    # BFS-style: for each source, compute reachable set
    reachable = set()
    for src in range(n):
        # earliest[v] = earliest time we can be at v (starting from src at time 0)
        earliest = {src: 0}
        for edge, t in edges:
            u, v = tuple(edge)
            if u in earliest and t > earliest[u]:
                if v not in earliest or t < earliest[v]:
                    earliest[v] = t
            if v in earliest and t > earliest[v]:
                if u not in earliest or t < earliest[u]:
                    earliest[u] = t
        for v in earliest:
            if v != src:
                reachable.add((src, v))

    return reachable


def greedy_spanner(n, timestamps):
    """
    Build a greedy temporal spanner: add edges that cover the most new pairs.
    """
    full_reach = temporal_reachability(n, timestamps)

    spanner_edges = set()
    covered = set()

    all_edges = list(timestamps.keys())

    while covered != full_reach:
        best_edge = None
        best_gain = 0

        for e in all_edges:
            if e in spanner_edges:
                continue
            test = spanner_edges | {e}
            new_covered = temporal_reachability(n, timestamps, test)
            gain = len(new_covered - covered)
            if gain > best_gain:
                best_gain = gain
                best_edge = e

        if best_edge is None or best_gain == 0:
            break

        spanner_edges.add(best_edge)
        covered = temporal_reachability(n, timestamps, spanner_edges)

    return spanner_edges, len(covered), len(full_reach)


def star_plus_tree_spanner(n, timestamps, hub):
    """
    Star + spanning tree construction:
    - Star: all edges incident to hub (n-1 edges)
    - Tree: spanning tree of K_{n-1} on non-hub vertices
      (pick edges greedily to maximize reachability)

    Total: (n-1) + (n-2) = 2n-3 edges.
    """
    star_edges = set()
    for v in range(n):
        if v != hub:
            star_edges.add(frozenset({hub, v}))

    # Greedy spanning tree on non-hub vertices
    non_hub = [v for v in range(n) if v != hub]
    tree_edges = set()
    covered = temporal_reachability(n, timestamps, star_edges)

    remaining = [frozenset({u, v}) for u, v in combinations(non_hub, 2)]

    for _ in range(n - 2):
        best_edge = None
        best_gain = 0

        for e in remaining:
            if e in tree_edges:
                continue
            test = star_edges | tree_edges | {e}
            new_covered = temporal_reachability(n, timestamps, test)
            gain = len(new_covered - covered)
            if gain > best_gain:
                best_gain = gain
                best_edge = e

        if best_edge is None or best_gain == 0:
            # Add any remaining edge for the tree
            for e in remaining:
                if e not in tree_edges:
                    best_edge = e
                    break
            if best_edge is None:
                break

        tree_edges.add(best_edge)
        remaining = [e for e in remaining if e != best_edge]
        covered = temporal_reachability(n, timestamps, star_edges | tree_edges)

    spanner = star_edges | tree_edges
    final_reach = temporal_reachability(n, timestamps, spanner)
    full_reach = temporal_reachability(n, timestamps)

    return spanner, len(final_reach), len(full_reach)


def sequential_delegation_kn(n, timestamps):
    """
    Sequential delegation on K_n:
    1. Pick root vertex (best hub)
    2. Add all root's edges (n-1 edges)
    3. For each remaining vertex v, find best delegate u (already processed)
       such that u→v temporal path exists using only spanner edges.
       If v is not reachable, add the edge {u,v} to the spanner.
    4. Count total spanner edges.
    """
    # Try each vertex as hub, pick the one that gives best initial coverage
    best_hub = None
    best_hub_coverage = -1

    for h in range(n):
        hub_edges = {frozenset({h, v}) for v in range(n) if v != h}
        reach = temporal_reachability(n, timestamps, hub_edges)
        if len(reach) > best_hub_coverage:
            best_hub_coverage = len(reach)
            best_hub = h

    hub = best_hub
    spanner = {frozenset({hub, v}) for v in range(n) if v != hub}
    covered = temporal_reachability(n, timestamps, spanner)
    full_reach = temporal_reachability(n, timestamps)

    # Now greedily add edges to cover remaining pairs
    remaining = list(timestamps.keys())
    random.shuffle(remaining)

    while covered != full_reach:
        best_edge = None
        best_gain = 0

        for e in remaining:
            if e in spanner:
                continue
            test = spanner | {e}
            new_covered = temporal_reachability(n, timestamps, test)
            gain = len(new_covered - covered)
            if gain > best_gain:
                best_gain = gain
                best_edge = e

        if best_edge is None or best_gain == 0:
            break

        spanner.add(best_edge)
        covered = temporal_reachability(n, timestamps, spanner)

    return spanner, len(covered), len(full_reach)


# ─── Task 1: Exact minimum spanners for small n ───────────────────────────

def exact_minimum_spanner(n, timestamps):
    """
    For small n, find the MINIMUM edge set that preserves all temporal reachability.
    Use branch-and-bound.
    """
    full_reach = temporal_reachability(n, timestamps)
    all_edges = list(timestamps.keys())
    m = len(all_edges)

    # Try edge sets of increasing size
    # Start from greedy solution as upper bound
    greedy_edges, _, _ = greedy_spanner(n, timestamps)
    best_size = len(greedy_edges)
    best_set = greedy_edges

    # For very small instances, try all subsets up to best_size
    if m <= 20:
        for size in range(1, best_size + 1):
            for subset in combinations(range(m), size):
                edge_set = {all_edges[i] for i in subset}
                reach = temporal_reachability(n, timestamps, edge_set)
                if reach == full_reach:
                    return edge_set, size
            if size >= best_size:
                break

    return best_set, best_size


def task1_exact_spanners():
    """Find exact minimum spanners for small n."""
    print("=" * 70)
    print("TASK 1: Exact minimum temporal K_n spanners")
    print("=" * 70)
    print()

    print(f"{'n':>4} {'trial':>6} | {'|E|':>4} {'|reach|':>8} {'greedy':>7} "
          f"{'star+tree':>10} {'min':>5} {'2n-3':>5}")
    print("-" * 60)

    for n in [4, 5, 6, 7]:
        for trial in range(5):
            ts = random_temporal_clique(n, seed=trial * 100 + n)
            full_reach = temporal_reachability(n, ts)
            num_edges = n * (n - 1) // 2

            # Greedy spanner
            g_edges, g_reach, _ = greedy_spanner(n, ts)

            # Star+tree (best hub)
            best_st_size = float('inf')
            for hub in range(n):
                st_edges, st_reach, _ = star_plus_tree_spanner(n, ts, hub)
                if st_reach == len(full_reach) and len(st_edges) < best_st_size:
                    best_st_size = len(st_edges)
            if best_st_size == float('inf'):
                best_st_size = -1

            # Exact minimum (only for small n)
            if n <= 6:
                min_edges, min_size = exact_minimum_spanner(n, ts)
            else:
                min_size = len(g_edges)  # approximate

            budget = 2 * n - 3

            print(f"{n:4d} {trial:6d} | {num_edges:4d} {len(full_reach):8d} "
                  f"{len(g_edges):7d} {best_st_size:10d} {min_size:5d} {budget:5d}")

    print()


# ─── Task 2: Star+tree at larger n ────────────────────────────────────────

def task2_star_tree():
    """Test star+tree construction at larger n."""
    print("=" * 70)
    print("TASK 2: Star+tree spanner — does it always achieve 2n-3?")
    print("=" * 70)
    print()

    print(f"{'n':>4} {'trials':>7} | {'avg_edges':>10} {'max_edges':>10} "
          f"{'2n-3':>5} {'full_reach%':>12} {'violations':>11}")
    print("-" * 65)

    for n in [5, 6, 7, 8, 9, 10]:
        trials = min(30, max(10, 200 // n))
        edge_counts = []
        reach_pcts = []
        violations = 0

        for trial in range(trials):
            ts = random_temporal_clique(n, seed=trial * 100 + n)
            full_reach = temporal_reachability(n, ts)

            # Try all hubs, pick best
            best_hub = None
            best_reach_pct = 0
            best_edges = None

            for hub in range(n):
                st_edges, st_reach, f_reach = star_plus_tree_spanner(n, ts, hub)
                pct = st_reach / f_reach if f_reach > 0 else 0
                if pct > best_reach_pct or (pct == best_reach_pct and
                        (best_edges is None or len(st_edges) < len(best_edges))):
                    best_reach_pct = pct
                    best_hub = hub
                    best_edges = st_edges

            edge_counts.append(len(best_edges))
            reach_pcts.append(best_reach_pct)

            if len(best_edges) > 2 * n - 3:
                violations += 1

        avg_e = sum(edge_counts) / trials
        max_e = max(edge_counts)
        avg_r = sum(reach_pcts) / trials
        budget = 2 * n - 3

        print(f"{n:4d} {trials:7d} | {avg_e:10.1f} {max_e:10d} "
              f"{budget:5d} {avg_r:12.1%} {violations:11d}")

    print()


# ─── Task 3: Delegation on K_n ────────────────────────────────────────────

def task3_delegation_kn():
    """Sequential delegation on K_n: edge count."""
    print("=" * 70)
    print("TASK 3: Sequential delegation on K_n")
    print("=" * 70)
    print()

    print(f"{'n':>4} {'trials':>7} | {'avg_edges':>10} {'max_edges':>10} "
          f"{'2n-3':>5} {'reach%':>8} {'violations':>11}")
    print("-" * 65)

    for n in [5, 6, 7, 8, 9, 10]:
        trials = min(20, max(5, 100 // n))
        edge_counts = []
        reach_pcts = []
        violations = 0

        for trial in range(trials):
            ts = random_temporal_clique(n, seed=trial * 100 + n)
            full_reach = temporal_reachability(n, ts)

            sp_edges, sp_reach, f_reach = sequential_delegation_kn(n, ts)
            edge_counts.append(len(sp_edges))
            pct = sp_reach / f_reach if f_reach > 0 else 0
            reach_pcts.append(pct)

            if len(sp_edges) > 2 * n - 3:
                violations += 1

        avg_e = sum(edge_counts) / trials
        max_e = max(edge_counts)
        avg_r = sum(reach_pcts) / trials
        budget = 2 * n - 3

        print(f"{n:4d} {trials:7d} | {avg_e:10.1f} {max_e:10d} "
              f"{budget:5d} {avg_r:8.1%} {violations:11d}")

    print()


# ─── Task 4: The full picture ─────────────────────────────────────────────

def task4_summary():
    """
    Summary: compare all construction methods.
    """
    print("=" * 70)
    print("TASK 4: FULL COMPARISON")
    print("=" * 70)
    print()

    print(f"{'n':>4} | {'greedy':>8} {'star+tree':>10} {'delegation':>11} | "
          f"{'2n-3':>5} {'min':>5}")
    print("-" * 55)

    for n in [4, 5, 6, 7, 8]:
        trials = min(10, max(3, 50 // n))
        g_edges = []
        st_edges = []
        d_edges = []
        min_sizes = []

        for trial in range(trials):
            ts = random_temporal_clique(n, seed=trial * 100 + n)

            # Greedy
            ge, _, _ = greedy_spanner(n, ts)
            g_edges.append(len(ge))

            # Star+tree (best hub)
            best_st = float('inf')
            for hub in range(n):
                ste, str_reach, f_reach = star_plus_tree_spanner(n, ts, hub)
                if str_reach == f_reach:
                    best_st = min(best_st, len(ste))
            if best_st == float('inf'):
                best_st = -1
            st_edges.append(best_st)

            # Delegation
            de, _, _ = sequential_delegation_kn(n, ts)
            d_edges.append(len(de))

            # Minimum (small n only)
            if n <= 6:
                _, ms = exact_minimum_spanner(n, ts)
                min_sizes.append(ms)

        budget = 2 * n - 3
        avg_g = sum(g_edges) / trials
        avg_st = sum(st_edges) / trials
        avg_d = sum(d_edges) / trials
        avg_m = sum(min_sizes) / trials if min_sizes else -1

        print(f"{n:4d} | {avg_g:8.1f} {avg_st:10.1f} {avg_d:11.1f} | "
              f"{budget:5d} {avg_m:5.1f}")

    print()


# ─── Main ──────────────────────────────────────────────────────────────────

def run():
    print("H27 Part 4: CORRECT MODEL — K_n TEMPORAL SPANNERS")
    print("=" * 70)
    print()

    task1_exact_spanners()
    print()
    task2_star_tree()
    print()
    task3_delegation_kn()
    print()
    task4_summary()

    # Verdict
    print("=" * 70)
    print("VERDICT")
    print("=" * 70)
    print("""
The bipartite K_{k,k} model used in Parts 1-3 is the WRONG model.
CPS operates on K_n (complete temporal graph on n vertices), not K_{k,k}.

In K_n:
- star+tree gives exactly 2n-3 edges (by construction: n-1 star + n-2 tree)
- The question is whether star+tree preserves ALL temporal reachability
- If yes for some hub, the conjecture is proved.

The bipartite model was a detour: it models CROSS-SIDE reachability only,
missing same-side and multi-hop paths. The actual CPS spanner operates on
the full temporal graph.
""")


if __name__ == '__main__':
    run()
