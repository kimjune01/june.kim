"""
Final verification:
1. The extra "convex but not halfspace intersection" set -- is our convexity check correct?
2. For 5-line 2D failures: are these also "no convex sets exist" at that size?
3. The refined conjecture: WHERE convex sets exist, do they always achieve min boundary?
"""

import itertools
import numpy as np
from collections import defaultdict
from compression_study import (
    chambers_2d, chambers_3d, chamber_graph, edge_boundary, is_convex,
    generic_lines_2d, generic_planes_3d
)


def check_convex_vs_halfspace(sv_list, sv_set, edges, N, n, name):
    """Find convex sets that aren't halfspace intersections and vice versa."""
    print(f"\n--- Checking convex = halfspace for {name} ---")

    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    # All halfspace intersections
    hs_sets = set()
    for pattern in itertools.product([-1, 0, 1], repeat=n):
        members = []
        for idx, sv in enumerate(sv_list):
            matches = True
            for j in range(n):
                if pattern[j] != 0 and sv[j] != pattern[j]:
                    matches = False
                    break
            if matches:
                members.append(idx)
        if members:
            hs_sets.add(frozenset(members))

    # All convex sets
    all_convex = set()
    for size in range(0, N+1):
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            if is_convex(S, sv_list, edges):
                all_convex.add(S)

    extra_convex = all_convex - hs_sets
    extra_hs = hs_sets - all_convex

    if extra_convex:
        print(f"  Convex but not halfspace intersection ({len(extra_convex)}):")
        for S in extra_convex:
            signs = [sv_list[j] for j in sorted(S)]
            print(f"    {signs}")
            # Verify convexity manually
            # A set is convex in a partial cube iff it's "gated"
            # For sign vectors: S is convex iff for every pair u,v in S,
            # the "interval" (chambers on shortest paths) is in S

    if extra_hs:
        print(f"  Halfspace intersection but not convex ({len(extra_hs)}):")
        for S in extra_hs:
            signs = [sv_list[j] for j in sorted(S)]
            print(f"    {signs}")

    # Actually, the empty set is both
    print(f"  Total convex: {len(all_convex)}, total HS: {len(hs_sets)}")
    print(f"  Convex ⊂ HS: {all_convex <= hs_sets}")
    print(f"  HS ⊂ Convex: {hs_sets <= all_convex}")


def full_refined_test(n_lines_or_planes, dim, seed):
    """Test refined conjecture: where convex sets exist, do they minimize?"""
    if dim == 2:
        lines = generic_lines_2d(n_lines_or_planes, seed=seed)
        sv = chambers_2d(lines)
    else:
        planes = generic_planes_3d(n_lines_or_planes, seed=seed)
        sv = chambers_3d(planes)

    sv_list, edges = chamber_graph(sv)
    sv_set = set(sv)
    N = len(sv_list)
    n = len(sv_list[0])

    # For each size
    result = {'arrangement': f"{n_lines_or_planes} {'lines' if dim==2 else 'planes'} (d={dim}, seed={seed})",
              'N': N, 'n': n}

    fails_refined = []
    for size in range(1, N):
        # Check if convex sets exist
        has_convex = False
        best_convex_b = float('inf')
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            if is_convex(S, sv_list, edges):
                has_convex = True
                b = edge_boundary(S, edges)
                best_convex_b = min(best_convex_b, b)

        if not has_convex:
            continue

        # Global min
        min_b = float('inf')
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            b = edge_boundary(S, edges)
            min_b = min(min_b, b)

        if best_convex_b > min_b:
            fails_refined.append((size, min_b, best_convex_b))

    return fails_refined


if __name__ == "__main__":
    # Check the convex vs halfspace discrepancy
    planes = generic_planes_3d(4)
    sv = chambers_3d(planes)
    sv_list, edges = chamber_graph(sv)
    sv_set = set(sv)
    N = len(sv_list)
    n = len(sv_list[0])
    check_convex_vs_halfspace(sv_list, sv_set, edges, N, n, "4 planes R^3")

    lines3 = generic_lines_2d(3)
    sv3 = chambers_2d(lines3)
    sv_list3, edges3 = chamber_graph(sv3)
    sv_set3 = set(sv3)
    check_convex_vs_halfspace(sv_list3, sv_set3, edges3, len(sv_list3), len(sv_list3[0]), "3 lines R^2")

    # Refined conjecture: comprehensive test
    print("\n" + "=" * 60)
    print("REFINED CONJECTURE TEST")
    print("Where convex sets exist, do they always achieve min boundary?")
    print("=" * 60)

    all_pass = True

    # 2D tests
    for n_lines in [3, 4, 5]:
        for seed in range(20):
            fails = full_refined_test(n_lines, 2, seed)
            if fails:
                all_pass = False
                print(f"  FAIL: {n_lines} lines seed {seed}: {fails}")

    # 3D tests
    for seed in range(30):
        fails = full_refined_test(4, 3, seed)
        if fails:
            all_pass = False
            print(f"  FAIL: 4 planes seed {seed}: {fails}")

    if all_pass:
        print("\n  REFINED CONJECTURE HOLDS across all tested arrangements!")
    else:
        print("\n  REFINED CONJECTURE FAILS.")

    # Summary of the 5-line failure investigation
    print("\n" + "=" * 60)
    print("5-line failures: checking if 'no convex sets' or 'convex sets lose'")
    print("=" * 60)

    for seed in [2, 3, 6, 13, 16, 17, 18, 19]:
        lines = generic_lines_2d(5, seed=seed)
        sv = chambers_2d(lines)
        sv_list, edges = chamber_graph(sv)
        sv_set = set(sv)
        N = len(sv_list)
        n = len(sv_list[0])

        # Check size 8 (N/2 = 8)
        for size in [7, 8]:
            convex_count = 0
            for S_tuple in itertools.combinations(range(N), size):
                S = frozenset(S_tuple)
                if is_convex(S, sv_list, edges):
                    convex_count += 1

            if convex_count == 0:
                print(f"  Seed {seed}, |S|={size}: NO convex sets exist (N={N})")
            else:
                print(f"  Seed {seed}, |S|={size}: {convex_count} convex sets exist")
