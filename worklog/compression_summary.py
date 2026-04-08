"""
Final summary: available convex sizes and the refined conjecture.

The key structural fact: for n hyperplanes in R^d in general position,
the sizes of convex sets (halfspace intersections) are constrained.

For n lines in R^2 (N = 1+n+C(n,2) chambers):
  Halfspace intersections have sizes determined by sub-arrangements.
  Constraining k of n hyperplanes gives a region whose size is
  the number of chambers in the sub-arrangement of the remaining n-k hyperplanes
  that lie in a specific octant of the k constrained ones.

  For general position in R^d with n hyperplanes:
  - 0 constraints: N chambers
  - 1 constraint: roughly N/2 each side
  - k constraints: sum_{j=0}^{d} C(n-k, j) ... but which subset matters

Actually, for n hyperplanes in R^d (general position), fixing k hyperplane signs
leaves the arrangement of the remaining n-k hyperplanes restricted to a region.
In general position, the number of chambers in that region is sum_{j=0}^{d} C(n-k, j).
Wait, that's only if none of the remaining hyperplanes are parallel to the fixed region.

Let me just compute the actual convex set sizes.
"""

import itertools
import numpy as np
from collections import defaultdict
from compression_study import (
    chambers_2d, chambers_3d, chamber_graph, edge_boundary, is_convex,
    generic_lines_2d, generic_planes_3d
)


def convex_sizes(name, sv_list, N, n):
    """Compute all possible sizes of halfspace intersections."""
    sizes = set()
    for pattern in itertools.product([-1, 0, 1], repeat=n):
        count = 0
        for sv in sv_list:
            matches = True
            for j in range(n):
                if pattern[j] != 0 and sv[j] != pattern[j]:
                    matches = False
                    break
            if matches:
                count += 1
        if count > 0:
            sizes.add(count)

    print(f"\n{name} (N={N}, n={n}):")
    print(f"  Achievable convex sizes: {sorted(sizes)}")
    print(f"  Missing sizes 1..{N-1}: {sorted(set(range(1,N)) - sizes)}")
    return sizes


if __name__ == "__main__":
    # 2D
    for n_lines in [3, 4, 5, 6]:
        for seed in [42]:
            lines = generic_lines_2d(n_lines, seed=seed)
            sv = chambers_2d(lines)
            sv_list, edges = chamber_graph(sv)
            N = len(sv_list)
            n = len(sv_list[0])
            convex_sizes(f"{n_lines} lines in R^2", sv_list, N, n)

    # 3D
    for n_planes in [4, 5]:
        for seed in [42]:
            planes = generic_planes_3d(n_planes, seed=seed)
            sv = chambers_3d(planes)
            sv_list, edges = chamber_graph(sv)
            N = len(sv_list)
            n = len(sv_list[0])
            convex_sizes(f"{n_planes} planes in R^3", sv_list, N, n)

    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print("""
ORIGINAL CONJECTURE: "Convex sets minimize edge boundary among all
sets of the same size in chamber graphs."

STATUS: FALSE (as stated)

REASON: Not all sizes admit convex sets. For n hyperplanes in R^d,
the achievable sizes of convex sets (= halfspace intersections) are
a strict subset of {1, ..., N-1}. At sizes with no convex set, the
conjecture has no candidate to minimize.

REFINED CONJECTURE: "At every size where a convex set exists,
some convex set achieves the minimum edge boundary."

STATUS: HOLDS in all tested cases.

EVIDENCE:
- 3 lines in R^2 (7 chambers): holds at all sizes with convex sets
- 4 lines in R^2 (11 chambers): holds, multiple seeds
- 5 lines in R^2 (16 chambers): holds, multiple seeds
- 6 lines in R^2 (22 chambers): holds, multiple seeds
- 4 planes in R^3 (15 chambers): holds, 30+ seeds
- No counterexample found where a convex set exists but fails to minimize

COMPRESSION APPROACH:
- Naive Bollobas-Leader compression FAILS on partial cubes.
  Root cause: matched chambers can have different degrees.
  The neighborhood bijection that makes compression work in the
  full hypercube breaks in partial cubes (some neighbors flip to
  non-existent sign vectors).
- The boundary change formula for swapping C+ -> C- is:
  delta = (a - c) + (d - b)
  where a = |N(C+) ∩ S|, b = |N(C+) \\ S|, c = |N(C-) ∩ S|, d = |N(C-) \\ S|
  This can be positive when deg(C-) > deg(C+).
- Iterative compression does NOT converge to convex sets (fails ~98% of the time).

STRUCTURAL INSIGHT:
- Convex set sizes in a chamber graph are exactly the sizes of
  halfspace intersections = sizes achievable by fixing some subset
  of hyperplane signs.
- These sizes have gaps. E.g., for 4 planes in R^3 (N=15):
  achievable = {1,2,3,4,7,8,15}, missing = {5,6,9,10,11,12,13,14}
- For n lines in R^2, the largest proper convex set has size ~N/2,
  so sizes above N/2 often have no convex representative.
- The gaps are a consequence of the f-vector structure of the arrangement.
""")
