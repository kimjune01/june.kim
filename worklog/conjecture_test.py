"""
Critical finding: non-convex boundary minimizers exist in chamber graphs.
This script verifies and characterizes the failure of the convexity conjecture.

Key questions:
1. At what sizes do non-convex minimizers appear?
2. Is there a size threshold (|S| <= N/2) where convex minimizers still dominate?
3. What structure do the non-convex minimizers have?
4. Does a WEAKER conjecture hold: convex minimizer EXISTS (but isn't unique) for each size?
"""

import itertools
import numpy as np
from collections import defaultdict
from compression_study import (
    chambers_2d, chambers_3d, chamber_graph, edge_boundary, is_convex,
    generic_lines_2d, generic_planes_3d
)


def full_minimizer_analysis(name, sv_list, edges, max_exhaustive=18):
    """Comprehensive analysis of boundary minimizers."""
    N = len(sv_list)
    n = len(sv_list[0])

    print(f"\n{'='*70}")
    print(f"{name}: {N} chambers, {n} hyperplanes, {len(edges)} edges")
    print(f"{'='*70}")

    if N > max_exhaustive:
        print(f"  Too large for exhaustive search (N={N})")
        return

    # For each size, find all convex sets and their boundaries
    # First enumerate all convex sets
    convex_sets_by_size = defaultdict(list)
    for size in range(1, N):
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            if is_convex(S, sv_list, edges):
                b = edge_boundary(S, edges)
                convex_sets_by_size[size].append((b, S))

    # For each size, find global minimizer and convex minimizer
    print(f"\n{'Size':>4} | {'Min ∂':>5} | {'#Min':>4} | {'#Cvx Min':>8} | {'Best Cvx ∂':>10} | {'Match':>5} | Notes")
    print("-" * 80)

    conjecture_holds_small = True  # for |S| <= N/2
    conjecture_holds_all = True

    for size in range(1, N):
        # Global minimizer
        min_boundary = float('inf')
        min_count = 0
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            b = edge_boundary(S, edges)
            if b < min_boundary:
                min_boundary = b
                min_count = 1
            elif b == min_boundary:
                min_count += 1

        # Convex minimizer
        if convex_sets_by_size[size]:
            best_convex_boundary = min(b for b, _ in convex_sets_by_size[size])
            convex_min_count = sum(1 for b, _ in convex_sets_by_size[size] if b == best_convex_boundary)
        else:
            best_convex_boundary = float('inf')
            convex_min_count = 0

        # Count how many global minimizers are convex
        convex_global_mins = 0
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            b = edge_boundary(S, edges)
            if b == min_boundary and is_convex(S, sv_list, edges):
                convex_global_mins += 1

        match = "YES" if min_boundary == best_convex_boundary else "NO"
        half = "<=N/2" if size <= N//2 else ">N/2"

        notes = []
        if min_boundary != best_convex_boundary:
            notes.append(f"gap={best_convex_boundary - min_boundary}")
            if size <= N//2:
                conjecture_holds_small = False
            conjecture_holds_all = False
        if convex_global_mins == 0 and min_count > 0:
            notes.append("no convex minimizer")
        if convex_min_count == 0:
            notes.append("no convex sets at all!")

        print(f"{size:>4} | {min_boundary:>5} | {min_count:>4} | {convex_global_mins:>8} | "
              f"{best_convex_boundary if best_convex_boundary < float('inf') else 'N/A':>10} | "
              f"{match:>5} | {half} {'; '.join(notes)}")

    print()
    if conjecture_holds_all:
        print("  CONJECTURE HOLDS: convex sets achieve min boundary at ALL sizes")
    elif conjecture_holds_small:
        print("  WEAK CONJECTURE HOLDS: convex min = global min for |S| <= N/2")
        print("  Fails for |S| > N/2")
    else:
        print("  CONJECTURE FAILS: even for |S| <= N/2")


def test_complement_symmetry(sv_list, edges, N):
    """Check: is ∂(S) = ∂(V\S)? If so, minimizers at size k correspond to size N-k."""
    print(f"\n--- Complement symmetry check ---")
    # ∂(S) = ∂(V\S) by definition (same edges cross the cut)
    print("  ∂(S) = ∂(V\\S) always (by definition of edge boundary)")
    print("  So minimizers at size k biject with minimizers at size N-k")
    print("  Convex sets need not have convex complements though!")

    # Check: for which sizes do convex sets exist?
    for size in range(1, N):
        has_convex = False
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            if is_convex(S, sv_list, edges):
                has_convex = True
                break
        complement_size = N - size
        comp_has_convex = False
        for S_tuple in itertools.combinations(range(N), complement_size):
            S = frozenset(S_tuple)
            if is_convex(S, sv_list, edges):
                comp_has_convex = True
                break
        if has_convex != comp_has_convex:
            print(f"  Asymmetry: size {size} has convex={has_convex}, "
                  f"complement size {complement_size} has convex={comp_has_convex}")


def count_convex_sets(sv_list, edges, N):
    """Count convex sets by size."""
    print(f"\n--- Convex set counts ---")
    for size in range(0, N+1):
        count = 0
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            if is_convex(S, sv_list, edges):
                count += 1
        print(f"  |S|={size}: {count} convex sets")


if __name__ == "__main__":
    # Test multiple arrangements
    for n_lines in [3, 4, 5]:
        lines = generic_lines_2d(n_lines)
        sv = chambers_2d(lines)
        sv_list, edges = chamber_graph(sv)
        N = len(sv_list)

        full_minimizer_analysis(f"{n_lines} lines in R²", sv_list, edges)
        if N <= 16:
            count_convex_sets(sv_list, edges, N)

    # 4 planes in R^3
    planes = generic_planes_3d(4)
    sv = chambers_3d(planes)
    sv_list, edges = chamber_graph(sv)
    N = len(sv_list)
    full_minimizer_analysis("4 planes in R³", sv_list, edges)

    # Try a second random arrangement to check robustness
    for seed in [7, 13, 99]:
        lines = generic_lines_2d(4, seed=seed)
        sv = chambers_2d(lines)
        sv_list, edges = chamber_graph(sv)
        full_minimizer_analysis(f"4 lines in R² (seed={seed})", sv_list, edges)
