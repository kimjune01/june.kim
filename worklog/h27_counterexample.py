#!/usr/bin/env python3
"""
H27 Part 6: Investigate the n=6 counterexample (seed=163).

Star+tree fails for ALL hubs. This means the greedy tree construction
is not finding the right tree. The question: is there ANY set of n-2=4
non-hub edges that, combined with a star, preserves full reachability?

Or is 2n-3 genuinely insufficient for this instance?
"""

import random
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


def exhaustive_star_tree(n, ts, hub):
    """Try ALL possible sets of n-2 non-hub edges (exhaustive)."""
    star = {frozenset({hub, v}) for v in range(n) if v != hub}
    full_reach = temporal_reachability(n, ts, set(ts.keys()))

    non_hub = [v for v in range(n) if v != hub]
    non_hub_edges = [frozenset({u, v}) for u, v in combinations(non_hub, 2)]

    # Try all subsets of size n-2
    best_reach = 0
    best_tree = None

    for tree_edges in combinations(non_hub_edges, n - 2):
        spanner = star | set(tree_edges)
        reach = temporal_reachability(n, ts, spanner)
        if len(reach) > best_reach:
            best_reach = len(reach)
            best_tree = tree_edges
        if reach == full_reach:
            return set(tree_edges), True, len(reach), len(full_reach)

    return set(best_tree) if best_tree else set(), False, best_reach, len(full_reach)


def exhaustive_any_2n3(n, ts):
    """Try ALL subsets of size 2n-3 to find a valid spanner."""
    full_reach = temporal_reachability(n, ts, set(ts.keys()))
    all_edges = list(ts.keys())
    target_size = 2 * n - 3

    count = 0
    for edge_set in combinations(all_edges, target_size):
        count += 1
        reach = temporal_reachability(n, ts, set(edge_set))
        if reach == full_reach:
            return set(edge_set), True, count
        if count > 500000:
            return None, False, count

    return None, False, count


def investigate_n6():
    """Deep investigation of the n=6 counterexample."""
    n = 6
    ts = random_temporal_clique(n, seed=163)
    full_reach = temporal_reachability(n, ts, set(ts.keys()))

    print(f"K_{n} instance (seed=163)")
    print(f"  Total edges: {len(ts)}")
    print(f"  Total reachable pairs: {len(full_reach)}")
    print(f"  Expected max: {n*(n-1)} = {n*(n-1)}")
    print()

    # Print timestamp matrix
    print("  Edge timestamps:")
    for e in sorted(ts.keys(), key=lambda e: ts[e]):
        u, v = sorted(tuple(e))
        print(f"    ({u},{v}) @ t={ts[e]}")
    print()

    # Test each hub with greedy tree
    print("  Hub analysis (greedy tree):")
    for hub in range(n):
        star = {frozenset({hub, v}) for v in range(n) if v != hub}
        star_reach = temporal_reachability(n, ts, star)
        star_pct = len(star_reach) / len(full_reach) * 100

        # Exhaustive tree search
        tree, found, best_reach, _ = exhaustive_star_tree(n, ts, hub)
        spanner = star | tree
        sp_reach = temporal_reachability(n, ts, spanner)

        print(f"    Hub {hub}: star covers {len(star_reach)}/{len(full_reach)} ({star_pct:.0f}%), "
              f"best tree gives {len(sp_reach)}/{len(full_reach)} "
              f"({'FULL' if found else 'INCOMPLETE'}), tree={sorted(tuple(sorted(tuple(e))) for e in tree)}")

    print()

    # Does ANY 2n-3 edge set work?
    print("  Exhaustive search for ANY 2n-3=9 edge set that spans all pairs...")
    result, found, count = exhaustive_any_2n3(n, ts)
    if found:
        print(f"    FOUND after {count} tries!")
        print(f"    Edges: {sorted(tuple(sorted(tuple(e))) for e in result)}")
    else:
        print(f"    NOT FOUND in {count} subsets. 2n-3 may be insufficient for this instance!")
    print()

    # What's the minimum number of edges needed?
    print("  Searching for minimum spanner size...")
    for size in range(n-1, len(ts)+1):
        found_any = False
        count = 0
        for edge_set in combinations(list(ts.keys()), size):
            count += 1
            reach = temporal_reachability(n, ts, set(edge_set))
            if reach == full_reach:
                found_any = True
                print(f"    Minimum spanner size: {size} (found after {count} checks)")
                print(f"    Edges: {sorted(tuple(sorted(tuple(e))) for e in edge_set)}")
                break
            if count > 500000:
                print(f"    Size {size}: checked {count} subsets, none found (may exist)")
                break
        if found_any:
            break
    print()


def check_more_counterexamples():
    """Check if the greedy tree failure is due to greedy tree quality."""
    print("=" * 70)
    print("Checking if failures are greedy-tree-specific or fundamental")
    print("=" * 70)
    print()

    for n in [6]:
        failures = 0
        greedy_only_failures = 0
        fundamental_failures = 0

        for seed in range(500):
            ts = random_temporal_clique(n, seed=seed)
            full_reach = temporal_reachability(n, ts, set(ts.keys()))

            greedy_works = False
            exhaustive_works = False

            for hub in range(n):
                # Greedy tree
                star = {frozenset({hub, v}) for v in range(n) if v != hub}
                non_hub = [v for v in range(n) if v != hub]
                tree = set()
                current = star.copy()
                covered = temporal_reachability(n, ts, current)
                candidates = [frozenset({u, v}) for u, v in combinations(non_hub, 2)]

                for _ in range(n - 2):
                    best_edge = None
                    best_gain = -1
                    for e in candidates:
                        if e in tree:
                            continue
                        test = current | tree | {e}
                        new_covered = temporal_reachability(n, ts, test)
                        gain = len(new_covered) - len(covered)
                        if gain > best_gain:
                            best_gain = gain
                            best_edge = e
                    if best_edge is None:
                        for e in candidates:
                            if e not in tree:
                                best_edge = e
                                break
                    if best_edge is None:
                        break
                    tree.add(best_edge)
                    current = star | tree
                    covered = temporal_reachability(n, ts, current)

                if covered == full_reach:
                    greedy_works = True
                    exhaustive_works = True
                    break

            if not greedy_works:
                failures += 1
                # Check exhaustive
                for hub in range(n):
                    _, found, _, _ = exhaustive_star_tree(n, ts, hub)
                    if found:
                        exhaustive_works = True
                        break

                if exhaustive_works:
                    greedy_only_failures += 1
                else:
                    fundamental_failures += 1
                    if fundamental_failures <= 3:
                        print(f"  Fundamental failure at seed={seed}")

        print(f"  n={n}: {failures} total failures / 500")
        print(f"    Greedy-only failures: {greedy_only_failures} (fixed by exhaustive tree)")
        print(f"    Fundamental failures: {fundamental_failures} (no star+tree works)")
        print()


def check_fundamental_with_2n3():
    """For fundamental failures, check if ANY 2n-3 edge set works."""
    print("=" * 70)
    print("Fundamental failures: does ANY 2n-3 edge set work?")
    print("=" * 70)
    print()

    n = 6
    for seed in range(500):
        ts = random_temporal_clique(n, seed=seed)
        full_reach = temporal_reachability(n, ts, set(ts.keys()))

        # Quick check: does any star+exhaustive-tree work?
        any_works = False
        for hub in range(n):
            _, found, _, _ = exhaustive_star_tree(n, ts, hub)
            if found:
                any_works = True
                break

        if not any_works:
            # Fundamental failure. Check if any 2n-3 set works.
            print(f"  seed={seed}: no star+tree works. Checking 2n-3 subsets...")
            result, found, count = exhaustive_any_2n3(n, ts)
            if found:
                print(f"    YES — 2n-3 spanner exists but NOT as star+tree! Edges:")
                for e in sorted(result, key=lambda e: ts[e]):
                    u, v = sorted(tuple(e))
                    print(f"      ({u},{v}) @ t={ts[e]}")
            else:
                print(f"    NO — 2n-3 edges are INSUFFICIENT. The conjecture is FALSE!")

                # Find minimum
                for size in range(2*n-3+1, len(ts)+1):
                    found_min = False
                    cnt = 0
                    for edge_set in combinations(list(ts.keys()), size):
                        cnt += 1
                        reach = temporal_reachability(n, ts, set(edge_set))
                        if reach == full_reach:
                            print(f"    Minimum spanner size: {size}")
                            found_min = True
                            break
                        if cnt > 500000:
                            break
                    if found_min:
                        break
            print()


def run():
    print("H27 Part 6: COUNTEREXAMPLE INVESTIGATION")
    print("=" * 70)
    print()

    investigate_n6()
    check_more_counterexamples()
    check_fundamental_with_2n3()


if __name__ == '__main__':
    run()
