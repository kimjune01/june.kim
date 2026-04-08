"""
Deep analysis of the 3D counterexample and the structure of the conjecture failure.

Key findings so far:
1. In R^2 (lines): weak conjecture holds (convex min = global min for |S| <= N/2)
2. In R^3 (4 planes): conjecture FAILS at |S|=5,6 (which is <= N/2 = 7)
3. The failure is because no convex sets of size 5 or 6 EXIST in 4 planes in R^3

The maximum convex set size matters. In n hyperplanes in R^d:
- Chamber count = sum_{k=0}^{d} C(n,k)
- Max convex set = halfspace intersection, which can be at most... depends on the arrangement

Let's understand:
- Why do no convex sets of size 5 exist for 4 planes in R^3?
- What are all convex set sizes for various arrangements?
- Is there a refined conjecture that accounts for this?
"""

import itertools
import numpy as np
from collections import defaultdict
from compression_study import (
    chambers_2d, chambers_3d, chamber_graph, edge_boundary, is_convex,
    generic_lines_2d, generic_planes_3d
)


def convex_set_analysis(name, sv_list, edges, N, n):
    """Detailed analysis of convex sets."""
    print(f"\n{'='*60}")
    print(f"{name}: {N} chambers, {n} hyperplanes")

    # Enumerate all convex sets
    convex_by_size = defaultdict(list)
    for size in range(0, N+1):
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            if is_convex(S, sv_list, edges):
                b = edge_boundary(S, edges) if size > 0 and size < N else 0
                convex_by_size[size].append((S, b))

    total_convex = sum(len(v) for v in convex_by_size.values())
    print(f"Total convex sets: {total_convex}")

    # For partial cubes, convex sets = intersections of halfspaces
    # Each halfspace is defined by choosing a side (+/-) for one hyperplane
    # So convex sets correspond to sign-vector constraints:
    # fix some subset of coordinates to specific values

    # Enumerate halfspace intersections
    print(f"\nHalfspace intersection analysis:")
    print(f"  Each convex set is an intersection of halfspaces.")
    print(f"  With {n} hyperplanes, there are 3^n = {3**n} possible constraint patterns")
    print(f"  (each hyperplane: +, -, or unconstrained)")

    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    # Generate all halfspace intersections
    hs_sets = {}
    for pattern in itertools.product([-1, 0, 1], repeat=n):
        # 0 means unconstrained, +1 means must be +, -1 means must be -
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
            key = frozenset(members)
            if key not in hs_sets:
                hs_sets[key] = pattern

    print(f"  Distinct halfspace intersections: {len(hs_sets)}")

    # Check: are these exactly the convex sets?
    all_convex = set()
    for size_sets in convex_by_size.values():
        for S, _ in size_sets:
            all_convex.add(S)

    hs_as_sets = set(hs_sets.keys())

    if all_convex == hs_as_sets:
        print(f"  CONFIRMED: convex sets = halfspace intersections")
    else:
        extra_convex = all_convex - hs_as_sets
        extra_hs = hs_as_sets - all_convex
        if extra_convex:
            print(f"  {len(extra_convex)} convex sets NOT halfspace intersections!")
        if extra_hs:
            print(f"  {len(extra_hs)} halfspace intersections NOT convex!")

    # Size distribution
    hs_by_size = defaultdict(int)
    for s in hs_sets:
        hs_by_size[len(s)] += 1

    print(f"\n  Size distribution of convex (= halfspace intersection) sets:")
    for size in sorted(hs_by_size.keys()):
        print(f"    |S|={size}: {hs_by_size[size]} sets")

    # The key question: what sizes are MISSING?
    missing_sizes = [s for s in range(1, N) if s not in hs_by_size or hs_by_size[s] == 0]
    if missing_sizes:
        print(f"\n  MISSING SIZES (no convex sets exist): {missing_sizes}")
        print(f"  These are the sizes where the conjecture trivially fails")
        print(f"  (no convex competitor exists)")

    return convex_by_size, missing_sizes


def refined_conjecture_test(name, sv_list, edges, N, n, convex_by_size, missing_sizes):
    """
    Test refined conjecture: among sizes where convex sets exist,
    does the minimum boundary convex set match the global minimum?
    """
    print(f"\n--- Refined conjecture: for sizes where convex sets exist ---")

    holds = True
    for size in range(1, N):
        if size in missing_sizes:
            continue

        # Global min
        min_boundary = float('inf')
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            b = edge_boundary(S, edges)
            if b < min_boundary:
                min_boundary = b

        # Best convex
        best_convex = min(b for _, b in convex_by_size[size])

        if best_convex > min_boundary:
            print(f"  |S|={size}: FAILS. Global min ∂={min_boundary}, best convex ∂={best_convex}")
            holds = False

    if holds:
        print(f"  HOLDS: at every size with convex sets, convex min = global min")
    return holds


def investigate_3d_failure(sv_list, edges, N, n):
    """Why do some sizes have no convex sets in 3D?"""
    print(f"\n--- Why sizes 5,6 have no convex sets for 4 planes in R^3 ---")

    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    # Convex sets = halfspace intersections
    # With 4 planes, pattern has 4 entries each in {-1, 0, 1}
    # Size of intersection depends on how many constraints are imposed

    # For 4 planes in general position in R^3:
    # 0 constraints: all N=15 chambers
    # 1 constraint (fix 1 coord): each halfspace has how many chambers?
    for j in range(n):
        plus_count = sum(1 for sv in sv_list if sv[j] == 1)
        minus_count = sum(1 for sv in sv_list if sv[j] == -1)
        print(f"  H_{j}: + side has {plus_count}, - side has {minus_count}")

    # 2 constraints: fix 2 coords
    print(f"\n  Two-constraint intersections:")
    for i in range(n):
        for j in range(i+1, n):
            for si in [-1, 1]:
                for sj in [-1, 1]:
                    count = sum(1 for sv in sv_list if sv[i] == si and sv[j] == sj)
                    print(f"    H_{i}={'+' if si==1 else '-'}, H_{j}={'+' if sj==1 else '-'}: {count} chambers")


def test_many_3d_arrangements():
    """Test the conjecture across many 3D arrangements."""
    print(f"\n{'='*60}")
    print("Testing conjecture across multiple 3D arrangements")
    print(f"{'='*60}")

    fails_small = 0
    total = 0

    for seed in range(50):
        planes = generic_planes_3d(4, seed=seed)
        sv = chambers_3d(planes)
        sv_list, edges = chamber_graph(sv)
        N = len(sv_list)
        n = len(sv_list[0])

        if N != 15:
            continue  # Not in general position

        total += 1
        weak_holds = True

        for size in range(1, N//2 + 1):
            # Global min
            min_boundary = float('inf')
            for S_tuple in itertools.combinations(range(N), size):
                S = frozenset(S_tuple)
                b = edge_boundary(S, edges)
                if b < min_boundary:
                    min_boundary = b

            # Check if any convex set achieves this
            has_convex_minimizer = False
            for S_tuple in itertools.combinations(range(N), size):
                S = frozenset(S_tuple)
                b = edge_boundary(S, edges)
                if b == min_boundary and is_convex(S, sv_list, edges):
                    has_convex_minimizer = True
                    break

            if not has_convex_minimizer:
                weak_holds = False
                # Check if convex sets even exist at this size
                has_any_convex = False
                for S_tuple in itertools.combinations(range(N), size):
                    S = frozenset(S_tuple)
                    if is_convex(S, sv_list, edges):
                        has_any_convex = True
                        break
                reason = "no convex sets exist" if not has_any_convex else "convex sets exist but none minimize"
                print(f"  Seed {seed}: FAILS at |S|={size} ({reason})")
                break

        if not weak_holds:
            fails_small += 1

    print(f"\nTotal 3D arrangements tested: {total}")
    print(f"Failures at |S| <= N/2: {fails_small}")


def test_2d_more_lines():
    """Test more 2D arrangements to verify the weak conjecture holds there."""
    print(f"\n{'='*60}")
    print("Testing weak conjecture (|S| <= N/2) for 2D arrangements")
    print(f"{'='*60}")

    for n_lines in [3, 4, 5, 6]:
        fails = 0
        tested = 0
        for seed in range(20):
            lines = generic_lines_2d(n_lines, seed=seed)
            sv = chambers_2d(lines)
            sv_list, edges = chamber_graph(sv)
            N = len(sv_list)
            expected = 1 + n_lines + n_lines*(n_lines-1)//2
            if N != expected:
                continue
            tested += 1

            weak_holds = True
            for size in range(1, N//2 + 1):
                min_boundary = float('inf')
                for S_tuple in itertools.combinations(range(N), size):
                    S = frozenset(S_tuple)
                    b = edge_boundary(S, edges)
                    if b < min_boundary:
                        min_boundary = b

                has_convex_minimizer = False
                for S_tuple in itertools.combinations(range(N), size):
                    S = frozenset(S_tuple)
                    b = edge_boundary(S, edges)
                    if b == min_boundary and is_convex(S, sv_list, edges):
                        has_convex_minimizer = True
                        break

                if not has_convex_minimizer:
                    weak_holds = False
                    print(f"  {n_lines} lines, seed {seed}: FAILS at |S|={size}")
                    break

            if not weak_holds:
                fails += 1

        print(f"  {n_lines} lines: {tested} tested, {fails} failures")


if __name__ == "__main__":
    # Detailed 3D analysis
    planes = generic_planes_3d(4)
    sv = chambers_3d(planes)
    sv_list, edges = chamber_graph(sv)
    N = len(sv_list)
    n = len(sv_list[0])

    convex_by_size, missing_sizes = convex_set_analysis("4 planes in R³", sv_list, edges, N, n)
    refined_conjecture_test("4 planes in R³", sv_list, edges, N, n, convex_by_size, missing_sizes)
    investigate_3d_failure(sv_list, edges, N, n)

    # Also check 3 lines
    lines3 = generic_lines_2d(3)
    sv3 = chambers_2d(lines3)
    sv_list3, edges3 = chamber_graph(sv3)
    N3 = len(sv_list3)
    n3 = len(sv_list3[0])
    cb3, ms3 = convex_set_analysis("3 lines in R²", sv_list3, edges3, N3, n3)
    refined_conjecture_test("3 lines in R²", sv_list3, edges3, N3, n3, cb3, ms3)

    # Broader tests
    test_many_3d_arrangements()
    test_2d_more_lines()
