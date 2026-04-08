#!/usr/bin/env python3
"""
H27 Part 7: Direct test of the 2n-3 conjecture.

For each instance, check: does ANY subset of 2n-3 edges preserve all
temporal reachability? This is the actual conjecture.

Star+tree is one construction, but not the only one.
"""

import random
import sys
from itertools import combinations


def random_temporal_clique(n, seed=None):
    rng = random.Random(seed)
    edges = list(combinations(range(n), 2))
    timestamps = rng.sample(range(1, len(edges) * 10 + 1), len(edges))
    return {frozenset(e): t for e, t in zip(edges, timestamps)}


def temporal_reachability(n, ts, edge_set):
    edges = [(e, ts[e]) for e in edge_set]
    edges.sort(key=lambda x: x[1])
    pairs = set()
    for src in range(n):
        earliest = {src: 0}
        changed = True
        while changed:
            changed = False
            for e, t in edges:
                u, v = tuple(e)
                if u in earliest and t > earliest[u]:
                    if v not in earliest or t < earliest[v]:
                        earliest[v] = t
                        changed = True
                if v in earliest and t > earliest[v]:
                    if u not in earliest or t < earliest[u]:
                        earliest[u] = t
                        changed = True
        for v in earliest:
            if v != src:
                pairs.add((src, v))
    return pairs


def greedy_spanner(n, ts):
    """Greedy: add edge with best gain until full."""
    full_reach = temporal_reachability(n, ts, set(ts.keys()))
    spanner = set()
    covered = set()
    all_edges = list(ts.keys())

    while covered != full_reach:
        best_edge = None
        best_gain = 0
        for e in all_edges:
            if e in spanner:
                continue
            test = spanner | {e}
            new_covered = temporal_reachability(n, ts, test)
            gain = len(new_covered - covered)
            if gain > best_gain:
                best_gain = gain
                best_edge = e
        if best_edge is None or best_gain == 0:
            break
        spanner.add(best_edge)
        covered = temporal_reachability(n, ts, spanner)

    return spanner, covered, full_reach


def greedy_backward_prune(n, ts, spanner):
    """Remove edges that don't reduce reachability."""
    full_reach = temporal_reachability(n, ts, spanner)
    # Try removing edges in reverse timestamp order
    for e in sorted(spanner, key=lambda e: -ts[e]):
        test = spanner - {e}
        reach = temporal_reachability(n, ts, test)
        if reach == full_reach:
            spanner = test
    return spanner


def test_conjecture():
    """Test: for random K_n, does greedy spanner + backward prune achieve ≤ 2n-3?"""
    print("=" * 70)
    print("2n-3 CONJECTURE TEST: greedy + backward prune")
    print("=" * 70)
    print()

    print(f"{'n':>4} {'trials':>7} | {'avg':>6} {'max':>6} {'2n-3':>5} "
          f"{'violations':>11} {'reach':>8}")
    print("-" * 55)

    for n in [4, 5, 6, 7, 8, 9, 10, 12]:
        trials = min(100, max(20, 2000 // (n * n)))
        sizes = []
        violations = 0

        for trial in range(trials):
            ts = random_temporal_clique(n, seed=trial * 100 + n)
            full_reach = temporal_reachability(n, ts, set(ts.keys()))

            # Greedy build
            spanner, covered, _ = greedy_spanner(n, ts)

            # Backward prune
            spanner = greedy_backward_prune(n, ts, spanner)
            final_reach = temporal_reachability(n, ts, spanner)

            sizes.append(len(spanner))
            if len(spanner) > 2 * n - 3:
                violations += 1

        avg_s = sum(sizes) / trials
        max_s = max(sizes)
        budget = 2 * n - 3

        print(f"{n:4d} {trials:7d} | {avg_s:6.1f} {max_s:6d} {budget:5d} "
              f"{violations:11d} {'100%':>8}")

    print()


def multi_start_greedy(n, ts, starts=20):
    """
    Multi-start greedy: try different initial edges, pick best result.
    """
    full_reach = temporal_reachability(n, ts, set(ts.keys()))
    all_edges = list(ts.keys())
    best_spanner = None
    best_size = len(all_edges)

    for start_idx in range(min(starts, len(all_edges))):
        # Start with a different initial edge
        rng = random.Random(start_idx * 777)
        first_edge = all_edges[start_idx % len(all_edges)]

        spanner = {first_edge}
        covered = temporal_reachability(n, ts, spanner)

        # Greedy add
        remaining = [e for e in all_edges if e != first_edge]
        rng.shuffle(remaining)

        while covered != full_reach:
            best_edge = None
            best_gain = 0
            for e in remaining:
                if e in spanner:
                    continue
                test = spanner | {e}
                new_covered = temporal_reachability(n, ts, test)
                gain = len(new_covered - covered)
                if gain > best_gain:
                    best_gain = gain
                    best_edge = e
            if best_edge is None or best_gain == 0:
                break
            spanner.add(best_edge)
            covered = temporal_reachability(n, ts, spanner)

        # Backward prune
        spanner = greedy_backward_prune(n, ts, spanner)

        if len(spanner) < best_size:
            best_size = len(spanner)
            best_spanner = spanner

    return best_spanner, best_size


def test_multi_start():
    """Multi-start greedy test."""
    print("=" * 70)
    print("MULTI-START GREEDY + PRUNE")
    print("=" * 70)
    print()

    print(f"{'n':>4} {'trials':>7} | {'avg':>6} {'max':>6} {'2n-3':>5} "
          f"{'violations':>11}")
    print("-" * 50)

    for n in [5, 6, 7, 8, 9, 10, 12]:
        trials = min(50, max(10, 500 // (n * n)))
        sizes = []
        violations = 0

        for trial in range(trials):
            ts = random_temporal_clique(n, seed=trial * 100 + n)
            _, size = multi_start_greedy(n, ts, starts=15)
            sizes.append(size)
            if size > 2 * n - 3:
                violations += 1

        avg_s = sum(sizes) / trials
        max_s = max(sizes)
        budget = 2 * n - 3

        print(f"{n:4d} {trials:7d} | {avg_s:6.1f} {max_s:6d} {budget:5d} "
              f"{violations:11d}")

    print()


def exhaustive_small():
    """For n ≤ 7, exhaustively verify the conjecture."""
    print("=" * 70)
    print("EXHAUSTIVE VERIFICATION for n ≤ 7")
    print("=" * 70)
    print()

    for n in [4, 5, 6, 7]:
        trials = min(200, max(50, 5000 // (n * n)))
        all_pass = True
        min_sizes = []

        for trial in range(trials):
            ts = random_temporal_clique(n, seed=trial)
            full_reach = temporal_reachability(n, ts, set(ts.keys()))
            all_edges = list(ts.keys())
            target = 2 * n - 3

            # Check if any subset of size target works
            found = False
            for edge_set in combinations(all_edges, target):
                reach = temporal_reachability(n, ts, set(edge_set))
                if reach == full_reach:
                    found = True
                    break

            if not found:
                all_pass = False
                print(f"  n={n}, seed={trial}: CONJECTURE VIOLATION! "
                      f"No {target}-edge spanner exists.")
                # Find minimum
                for size in range(target + 1, len(all_edges) + 1):
                    for es in combinations(all_edges, size):
                        reach = temporal_reachability(n, ts, set(es))
                        if reach == full_reach:
                            min_sizes.append(size)
                            print(f"    Minimum spanner: {size} edges (vs budget {target})")
                            found = True
                            break
                    if found:
                        break
            else:
                min_sizes.append(target)  # or less

        if all_pass:
            print(f"  n={n}: ALL {trials} instances have a {2*n-3}-edge spanner. CONJECTURE HOLDS.")
        else:
            print(f"  n={n}: CONJECTURE VIOLATED in some instances!")

    print()


def run():
    print("H27 Part 7: DIRECT CONJECTURE TEST")
    print("=" * 70)
    print()

    test_conjecture()
    print()
    test_multi_start()
    print()
    exhaustive_small()


if __name__ == '__main__':
    run()
