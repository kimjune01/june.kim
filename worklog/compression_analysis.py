"""
Analysis of WHY naive compression fails and what might fix it.

Key insight: In a hypercube, flipping coordinate i preserves degree (every vertex has degree n).
In a partial cube, the partner chamber may have a different degree. Moving a chamber to a
higher-degree position increases the boundary.

Let's examine this carefully with the 3-line example.
"""

import itertools
import numpy as np
from collections import defaultdict
from compression_study import (
    chambers_2d, chamber_graph, edge_boundary, compress, is_convex,
    generic_lines_2d
)

def analyze_failure(sv_list, sv_set, edges, n, N):
    """Analyze why compression increases boundary."""

    # Build adjacency
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    print("\n--- Degree analysis of matched pairs ---")
    for hi in range(n):
        print(f"\n  Hyperplane H_{hi}:")
        for idx, sv in enumerate(sv_list):
            partner_sv = list(sv)
            partner_sv[hi] = -partner_sv[hi]
            partner_sv = tuple(partner_sv)
            if partner_sv in sv_set:
                partner_idx = sv_to_idx[partner_sv]
                if sv[hi] == 1:  # Only print once per pair
                    deg_plus = len(adj[idx])
                    deg_minus = len(adj[partner_idx])
                    print(f"    + {sv} (deg={deg_plus}) <-> - {partner_sv} (deg={deg_minus})"
                          f"  {'SAME' if deg_plus == deg_minus else f'DIFF by {abs(deg_plus-deg_minus)}'}")
            else:
                print(f"    {sv} (deg={len(adj[idx])}) -- UNMATCHED on H_{hi}")


def analyze_neighborhood_structure(sv_list, sv_set, edges, n, N):
    """
    For a matched pair (C+, C-), analyze how their neighborhoods relate.

    In the hypercube: if we flip coord i, the neighborhoods of C+ and C- are in
    perfect bijection (flip coord i of each neighbor). This is why compression works.

    In a partial cube: this bijection may break. Some neighbors of C+ may not have
    their flipped counterpart as a neighbor of C-.
    """
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    print("\n--- Neighborhood bijection analysis ---")
    for hi in range(n):
        print(f"\n  Hyperplane H_{hi}:")
        for idx, sv in enumerate(sv_list):
            partner_sv = list(sv)
            partner_sv[hi] = -partner_sv[hi]
            partner_sv = tuple(partner_sv)
            if partner_sv not in sv_set or sv[hi] != 1:
                continue
            partner_idx = sv_to_idx[partner_sv]

            # Neighbors of C+ (excluding the partner itself)
            nbrs_plus = adj[idx] - {partner_idx}
            nbrs_minus = adj[partner_idx] - {idx}

            # For each neighbor of C+, check if flipping coord i gives a neighbor of C-
            bijection_works = True
            for nbr in nbrs_plus:
                nbr_sv = sv_list[nbr]
                # Flip coord i of this neighbor
                flipped = list(nbr_sv)
                flipped[hi] = -flipped[hi]
                flipped = tuple(flipped)
                if flipped in sv_set:
                    flipped_idx = sv_to_idx[flipped]
                    if flipped_idx in nbrs_minus:
                        pass  # Good: bijection holds
                    else:
                        bijection_works = False
                        print(f"    Pair {sv}<->{partner_sv}: nbr {nbr_sv} flips to {flipped} "
                              f"which exists but is NOT a neighbor of {partner_sv}")
                else:
                    bijection_works = False
                    print(f"    Pair {sv}<->{partner_sv}: nbr {nbr_sv} flips to {flipped} "
                          f"which DOES NOT EXIST")

            # Also check: neighbors of C- that don't correspond to any neighbor of C+
            for nbr in nbrs_minus:
                nbr_sv = sv_list[nbr]
                flipped = list(nbr_sv)
                flipped[hi] = -flipped[hi]
                flipped = tuple(flipped)
                if flipped in sv_set:
                    flipped_idx = sv_to_idx[flipped]
                    if flipped_idx not in nbrs_plus:
                        print(f"    Pair {sv}<->{partner_sv}: nbr of minus {nbr_sv} flips to {flipped} "
                              f"which is NOT a neighbor of {sv}")
                else:
                    print(f"    Pair {sv}<->{partner_sv}: nbr of minus {nbr_sv} flips to {flipped} "
                          f"which DOES NOT EXIST")

            if bijection_works and len(nbrs_plus) == len(nbrs_minus):
                pass  # Perfect bijection
            else:
                print(f"    SUMMARY: {sv} has {len(nbrs_plus)} other-nbrs, "
                      f"{partner_sv} has {len(nbrs_minus)} other-nbrs")


def boundary_change_analysis(sv_list, sv_set, edges, n, N):
    """
    Detailed boundary change when compressing a single matched pair.

    Suppose C+ in S, C- not in S. Compression: remove C+, add C-.

    Change in boundary:
    - Edge C+--C- was boundary (C+ in S, C- out) -> now C- in S, C+ out -> still boundary. No change.
    - For each neighbor N of C+ (other than C-):
      - If N in S: edge C+--N was internal -> C+ removed -> edge gone. Boundary increases by 0 or...
        wait, N is still in S but C+ is removed. The edge C+--N no longer matters.
        But we need to think about it as: did C+--N contribute to boundary? No (both in S).
        After removal of C+: N might have new boundary edges? No, we're just removing C+ from S.
        So: edge C+--N was NOT boundary (both in S). After removing C+: this edge is now boundary
        (N in S, C+ out of S). Boundary increases by 1.
      - If N not in S: edge C+--N was boundary. After removing C+: not boundary (both out).
        Boundary decreases by 1.
    - For each neighbor N of C- (other than C+):
      - If N in S: edge C---N was boundary (C- out, N in). After adding C-: internal.
        Boundary decreases by 1.
      - If N not in S: edge C---N was not boundary (both out). After adding C-: boundary.
        Boundary increases by 1.

    Net change = (count of nbrs of C+ in S, excl C-) - (count of nbrs of C+ not in S, excl C-)
                 + (count of nbrs of C- not in S, excl C+) - (count of nbrs of C- in S, excl C+)

    Let a = |N(C+) ∩ S| - 1  (exclude the C+--C- edge, and C+ itself is in S)
    Wait, let me be more careful.

    Let:
    - a = |{N ∈ N(C+) \ {C-} : N ∈ S}|  (neighbors of C+ in S, excluding C-)
    - b = |{N ∈ N(C+) \ {C-} : N ∉ S}|  (neighbors of C+ not in S, excluding C-)
    - c = |{N ∈ N(C-) \ {C+} : N ∈ S}|  (neighbors of C- in S, excluding C+)
    - d = |{N ∈ N(C-) \ {C+} : N ∉ S}|  (neighbors of C- not in S, excluding C+)

    Net change = +a - b + d - c = (a - c) + (d - b)

    For the boundary to not increase: need (a - c) + (d - b) ≤ 0
    i.e., a + d ≤ b + c
    i.e., (nbrs of C+ in S) + (nbrs of C- not in S) ≤ (nbrs of C+ not in S) + (nbrs of C- in S)

    In a hypercube with perfect bijection: a = c and b = d (by the bijection flipping coord i).
    Wait, that's not right either. The bijection maps neighbors of C+ to neighbors of C-.
    But whether those neighbors are in S depends on S.

    Actually in the hypercube, after compression has already been applied to all other coordinates,
    the argument is more subtle. Bollobás-Leader works because ALL compressions have been applied.

    Let me check: does simultaneous compression (compressing ALL matched pairs at once) also fail?
    """
    print("\n--- Boundary change formula verification ---")
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    # Verify the formula on counterexample
    # Take the first counterexample: S = {(-1,-1,-1)}, compress H_0 toward +
    # For 3 lines arrangement

    # Let's just verify the formula matches the actual boundary change
    print("  Verifying boundary change formula on all compressions that increase boundary:")

    violations = 0
    for size in range(1, min(N, 8)):
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            orig_boundary = edge_boundary(S, edges)

            for hi in range(n):
                for direction in [-1, 1]:
                    compressed = compress(S, sv_list, sv_set, hi, direction)
                    new_boundary = edge_boundary(compressed, edges)

                    if new_boundary > orig_boundary:
                        violations += 1
                        if violations <= 3:
                            # Identify which pairs were swapped
                            removed = S - compressed
                            added = compressed - S
                            print(f"\n  S={[sv_list[j] for j in sorted(S)]}")
                            print(f"  Compress H_{hi} dir={direction}: ∂={orig_boundary} -> {new_boundary}")
                            for r in removed:
                                for a in added:
                                    sv_r = sv_list[r]
                                    sv_a = sv_list[a]
                                    # Check they're a matched pair
                                    diff = sum(1 for x,y in zip(sv_r, sv_a) if x != y)
                                    if diff == 1:
                                        # Compute a, b, c, d
                                        nbrs_r = adj[r] - {a}
                                        nbrs_a = adj[a] - {r}
                                        aa = len([x for x in nbrs_r if x in S])
                                        bb = len([x for x in nbrs_r if x not in S])
                                        cc = len([x for x in nbrs_a if x in S])
                                        dd = len([x for x in nbrs_a if x not in S])
                                        net = aa - bb + dd - cc
                                        print(f"    Swap {sv_r} -> {sv_a}")
                                        print(f"    deg(removed)={len(adj[r])}, deg(added)={len(adj[a])}")
                                        print(f"    a(nbrs_rem ∩ S)={aa}, b(nbrs_rem \\ S)={bb}, "
                                              f"c(nbrs_add ∩ S)={cc}, d(nbrs_add \\ S)={dd}")
                                        print(f"    Net change = {net} (predicted), "
                                              f"actual = {new_boundary - orig_boundary}")

    print(f"\n  Total violations: {violations}")


def test_degree_aware_compression(sv_list, sv_set, edges, n, N):
    """
    Modified compression: only swap if deg(C-) <= deg(C+).
    This ensures we don't move a chamber to a higher-degree position.
    """
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    print("\n--- Degree-aware compression test ---")
    violations = 0
    total = 0

    for size in range(1, N):
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            S_set = set(S)
            orig_boundary = edge_boundary(S, edges)

            for hi in range(n):
                # Only compress pairs where target has <= degree
                new_S = set(S)
                for idx in range(N):
                    sv = sv_list[idx]
                    partner_sv = list(sv)
                    partner_sv[hi] = -partner_sv[hi]
                    partner_sv = tuple(partner_sv)
                    if partner_sv not in sv_set:
                        continue
                    partner_idx = sv_to_idx[partner_sv]

                    if sv[hi] == 1 and idx in S_set and partner_idx not in S_set:
                        # Would compress + to -
                        if len(adj[partner_idx]) <= len(adj[idx]):
                            new_S.discard(idx)
                            new_S.add(partner_idx)

                new_S = frozenset(new_S)
                new_boundary = edge_boundary(new_S, edges)
                total += 1

                if new_boundary > orig_boundary:
                    violations += 1
                    if violations <= 3:
                        print(f"  VIOLATION: |S|={size}, H_{hi}: ∂={orig_boundary} -> {new_boundary}")

    print(f"  Total tests: {total}, violations: {violations}")


def find_boundary_minimizers(sv_list, sv_set, edges, n, N):
    """Find the actual boundary minimizers for each size and check convexity."""
    print("\n--- Boundary minimizers and convexity ---")

    for size in range(1, N):
        min_boundary = float('inf')
        minimizers = []

        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            b = edge_boundary(S, edges)
            if b < min_boundary:
                min_boundary = b
                minimizers = [S]
            elif b == min_boundary:
                minimizers.append(S)

        all_convex = all(is_convex(S, sv_list, edges) for S in minimizers)
        convex_count = sum(1 for S in minimizers if is_convex(S, sv_list, edges))

        print(f"  |S|={size}: min ∂={min_boundary}, "
              f"minimizers={len(minimizers)}, "
              f"convex={convex_count}/{len(minimizers)}")

        if not all_convex:
            for S in minimizers:
                if not is_convex(S, sv_list, edges):
                    print(f"    NON-CONVEX minimizer: {[sv_list[j] for j in S]}")


if __name__ == "__main__":
    lines3 = generic_lines_2d(3)
    sv3 = chambers_2d(lines3)
    sv_list, edges = chamber_graph(sv3)
    sv_set = set(sv3)
    N = len(sv_list)
    n = len(sv_list[0])

    print("=" * 60)
    print(f"3 lines in R²: {N} chambers, {n} hyperplanes")
    print(f"Sign vectors: {[sv for sv in sv_list]}")
    print("=" * 60)

    analyze_failure(sv_list, sv_set, edges, n, N)
    analyze_neighborhood_structure(sv_list, sv_set, edges, n, N)
    boundary_change_analysis(sv_list, sv_set, edges, n, N)

    print("\n" + "=" * 60)
    print("Boundary minimizers for 3 lines")
    print("=" * 60)
    find_boundary_minimizers(sv_list, sv_set, edges, n, N)

    # Now 4 lines
    lines4 = generic_lines_2d(4)
    sv4 = chambers_2d(lines4)
    sv_list4, edges4 = chamber_graph(sv4)
    sv_set4 = set(sv4)
    N4 = len(sv_list4)
    n4 = len(sv_list4[0])

    print("\n" + "=" * 60)
    print(f"4 lines in R²: {N4} chambers")
    print("=" * 60)
    find_boundary_minimizers(sv_list4, sv_set4, edges4, n4, N4)

    # 5 lines
    lines5 = generic_lines_2d(5)
    sv5 = chambers_2d(lines5)
    sv_list5, edges5 = chamber_graph(sv5)
    sv_set5 = set(sv5)
    N5 = len(sv_list5)
    n5 = len(sv_list5[0])

    print("\n" + "=" * 60)
    print(f"5 lines in R²: {N5} chambers")
    print("=" * 60)
    find_boundary_minimizers(sv_list5, sv_set5, edges5, n5, N5)
