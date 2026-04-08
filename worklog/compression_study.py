"""
Compression toward convexity for chamber graphs of hyperplane arrangements.

Chamber graph: vertices = chambers (regions), edges = pairs separated by exactly one hyperplane.
Sign vectors: each chamber gets sigma in {+,-}^n based on which side of each hyperplane it lies on.
Partial cube: the chamber graph embeds isometrically into the hypercube {+,-}^n.
"""

import itertools
import numpy as np
from collections import defaultdict

# ============================================================
# Part 1: Generate hyperplane arrangements and chamber graphs
# ============================================================

def chambers_2d(lines):
    """
    Given lines in R^2 as list of (a, b, c) for ax + by + c > 0,
    enumerate all chambers by their sign vectors.

    For general position lines in R^2, there are C(n,0)+C(n,1)+C(n,2) = 1+n+n(n-1)/2 chambers.

    We use sampling: pick many random points and record their sign vectors.
    """
    n = len(lines)
    # Find all intersection points
    intersections = []
    for i in range(n):
        for j in range(i+1, n):
            a1, b1, c1 = lines[i]
            a2, b2, c2 = lines[j]
            det = a1*b2 - a2*b1
            if abs(det) < 1e-12:
                continue
            x = (c1*b2 - c2*b1) / det  # Note: solving a1*x+b1*y = -c1, a2*x+b2*y = -c2
            # Actually let's be more careful. Line i: a_i * x + b_i * y + c_i = 0
            # So a1*x + b1*y = -c1, a2*x + b2*y = -c2
            x = (-c1*b2 + c2*b1) / det
            y = (-a1*c2 + a2*c1) / det
            intersections.append((x, y))

    # Sample many points, including near intersections
    sign_vectors = set()

    # Random points in a large region
    np.random.seed(42)
    points = np.random.randn(10000, 2) * 100

    # Also sample near each intersection
    for ix, iy in intersections:
        offsets = np.random.randn(500, 2) * 0.01
        near_pts = np.array([[ix, iy]]) + offsets
        points = np.vstack([points, near_pts])

    for pt in points:
        sv = tuple(1 if lines[i][0]*pt[0] + lines[i][1]*pt[1] + lines[i][2] > 0 else -1
                    for i in range(n))
        sign_vectors.add(sv)

    return sign_vectors


def chambers_3d(planes):
    """
    Given planes in R^3 as list of (a, b, c, d) for ax + by + cz + d > 0,
    enumerate all chambers by their sign vectors.
    """
    n = len(planes)
    sign_vectors = set()

    np.random.seed(42)
    points = np.random.randn(50000, 3) * 100

    # Find triple intersections (vertices of the arrangement)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                A = np.array([planes[i][:3], planes[j][:3], planes[k][:3]])
                b = np.array([-planes[i][3], -planes[j][3], -planes[k][3]])
                try:
                    pt = np.linalg.solve(A, b)
                    offsets = np.random.randn(200, 3) * 0.01
                    near_pts = pt + offsets
                    points = np.vstack([points, near_pts])
                except np.linalg.LinAlgError:
                    pass

    for pt in points:
        sv = tuple(1 if planes[i][0]*pt[0] + planes[i][1]*pt[1] + planes[i][2]*pt[2] + planes[i][3] > 0 else -1
                    for i in range(n))
        sign_vectors.add(sv)

    return sign_vectors


def chamber_graph(sign_vectors):
    """
    Build the chamber graph: edge between two chambers iff their sign vectors
    differ in exactly one coordinate AND both are valid chambers.
    """
    sv_list = sorted(sign_vectors)
    sv_set = set(sv_list)
    n = len(sv_list[0])

    edges = set()
    sv_to_idx = {sv: i for i, sv in enumerate(sv_list)}

    for sv in sv_list:
        for i in range(n):
            # Flip coordinate i
            flipped = list(sv)
            flipped[i] = -flipped[i]
            flipped = tuple(flipped)
            if flipped in sv_set:
                idx1 = sv_to_idx[sv]
                idx2 = sv_to_idx[flipped]
                edges.add((min(idx1, idx2), max(idx1, idx2)))

    return sv_list, edges


def edge_boundary(S_indices, edges):
    """Count edges with exactly one endpoint in S."""
    S_set = set(S_indices)
    count = 0
    for u, v in edges:
        if (u in S_set) != (v in S_set):
            count += 1
    return count


# ============================================================
# Part 2: Compression operator
# ============================================================

def compress(S_indices, sv_list, sign_vectors_set, hyperplane_idx, direction=-1):
    """
    Compress set S along hyperplane H_i toward the given direction (default: -1 side).

    For each matched pair (C+, C-) differing only in coordinate i:
    - If C+ in S but C- not in S: swap (move to - side)
    - If C- in S but C+ not in S: keep (already on preferred side)
    - If both in S or both out: keep

    Returns new set of indices.
    """
    sv_to_idx = {sv: idx for idx, sv in enumerate(sv_list)}
    S_set = set(S_indices)
    new_S = set(S_set)  # Start with copy

    i = hyperplane_idx
    processed = set()

    for idx in range(len(sv_list)):
        if idx in processed:
            continue
        sv = sv_list[idx]
        # Find partner: flip coordinate i
        partner_sv = list(sv)
        partner_sv[i] = -partner_sv[i]
        partner_sv = tuple(partner_sv)

        if partner_sv in sign_vectors_set:
            partner_idx = sv_to_idx[partner_sv]
            processed.add(idx)
            processed.add(partner_idx)

            # Determine which is on + side, which on - side
            if sv[i] == 1:
                plus_idx, minus_idx = idx, partner_idx
            else:
                plus_idx, minus_idx = partner_idx, idx

            # Compression toward direction
            if direction == -1:
                # Move to - side: if + in S but - not, swap
                if plus_idx in S_set and minus_idx not in S_set:
                    new_S.discard(plus_idx)
                    new_S.add(minus_idx)
            else:
                # Move to + side: if - in S but + not, swap
                if minus_idx in S_set and plus_idx not in S_set:
                    new_S.discard(minus_idx)
                    new_S.add(plus_idx)
        # Unmatched chambers stay where they are

    return frozenset(new_S)


def is_convex(S_indices, sv_list, edges):
    """
    Check if S is convex in the chamber graph.
    S is convex iff for every pair in S, all shortest paths stay in S.

    Equivalently for partial cubes: S is convex iff S is an intersection of halfspaces,
    i.e., S can be described by fixing some coordinates of the sign vector.

    For partial cubes, S is convex iff it's a "gated set": for every vertex v,
    there exists a "gate" g in S such that g lies on a shortest path from v to every s in S.

    Simpler check for partial cubes: S is convex iff for every pair u,v in S,
    the interval I(u,v) = {w : d(u,w) + d(w,v) = d(u,v)} is contained in S.

    For sign vectors in a partial cube, d(u,v) = Hamming distance restricted to valid edges.
    But we can use BFS.
    """
    if len(S_indices) <= 1:
        return True

    S_set = set(S_indices)
    N = len(sv_list)

    # Build adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # For each pair in S, check that the interval is in S
    # Use BFS to compute distances
    S_list = list(S_indices)

    # Precompute all-pairs distances via BFS (feasible for small graphs)
    dist = {}
    for start in range(N):
        d = {start: 0}
        queue = [start]
        qi = 0
        while qi < len(queue):
            u = queue[qi]
            qi += 1
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1
                    queue.append(v)
        dist[start] = d

    # Check: for every pair u,v in S, every vertex w on a shortest path (d(u,w)+d(w,v)=d(u,v)) is in S
    for u in S_list:
        for v in S_list:
            if u >= v:
                continue
            duv = dist[u][v]
            for w in range(N):
                if dist[u].get(w, float('inf')) + dist[w].get(v, float('inf')) == duv:
                    if w not in S_set:
                        return False
    return True


# ============================================================
# Part 3: Run experiments
# ============================================================

def test_arrangement(name, sign_vectors, expected_count=None):
    """Full compression test on a hyperplane arrangement."""
    sv_list, edges = chamber_graph(sign_vectors)
    sv_set = set(sign_vectors)
    N = len(sv_list)
    n = len(sv_list[0])  # number of hyperplanes

    print(f"\n{'='*60}")
    print(f"Arrangement: {name}")
    print(f"Chambers: {N}, Hyperplanes: {n}, Edges: {len(edges)}")
    if expected_count is not None:
        print(f"Expected chambers: {expected_count}, Got: {N}")

    # Task 1: Matching fractions
    print(f"\n--- Matching fractions ---")
    for i in range(n):
        matched = 0
        unmatched = 0
        for sv in sv_list:
            partner = list(sv)
            partner[i] = -partner[i]
            partner = tuple(partner)
            if partner in sv_set:
                matched += 1
            else:
                unmatched += 1
        # matched counts each partner twice
        print(f"  H_{i}: matched pairs = {matched//2}, matched = {matched}, unmatched = {unmatched}, "
              f"fraction matched = {matched/N:.3f}")

    # Task 2: Compression test on ALL subsets (only feasible for small N)
    if N > 16:
        print(f"\n--- Compression test: N={N} too large for exhaustive, sampling ---")
        test_compression_sampled(sv_list, sv_set, edges, n, N)
    else:
        print(f"\n--- Exhaustive compression test ---")
        test_compression_exhaustive(sv_list, sv_set, edges, n, N)


def test_compression_exhaustive(sv_list, sv_set, edges, n, N):
    """Test compression on all 2^N subsets."""
    total_tests = 0
    boundary_increased = 0
    counterexamples = []

    compression_preserves = True

    for size in range(1, N):
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            orig_boundary = edge_boundary(S, edges)

            for i in range(n):
                for direction in [-1, 1]:
                    compressed = compress(S, sv_list, sv_set, i, direction)
                    new_boundary = edge_boundary(compressed, edges)
                    total_tests += 1

                    if new_boundary > orig_boundary:
                        boundary_increased += 1
                        compression_preserves = False
                        if len(counterexamples) < 5:
                            counterexamples.append({
                                'S': S,
                                'size': size,
                                'hyperplane': i,
                                'direction': direction,
                                'orig_boundary': orig_boundary,
                                'new_boundary': new_boundary,
                                'S_signs': [sv_list[j] for j in S],
                                'compressed_signs': [sv_list[j] for j in compressed],
                            })

    print(f"  Total compression tests: {total_tests}")
    print(f"  Boundary increased: {boundary_increased}")
    print(f"  Compression preserves boundary: {compression_preserves}")

    if counterexamples:
        print(f"\n  Counterexamples (first {len(counterexamples)}):")
        for cx in counterexamples:
            print(f"    |S|={cx['size']}, H_{cx['hyperplane']} dir={cx['direction']}: "
                  f"∂={cx['orig_boundary']} -> {cx['new_boundary']}")
            print(f"      S signs: {cx['S_signs']}")
            print(f"      C(S) signs: {cx['compressed_signs']}")

    # Task 5: Iterative compression to fixed point
    print(f"\n--- Iterative compression to convexity ---")
    test_iterative_compression(sv_list, sv_set, edges, n, N)


def test_compression_sampled(sv_list, sv_set, edges, n, N, num_samples=5000):
    """Test compression on random subsets."""
    np.random.seed(123)
    total_tests = 0
    boundary_increased = 0
    counterexamples = []

    for _ in range(num_samples):
        size = np.random.randint(1, N)
        S = frozenset(np.random.choice(N, size, replace=False))
        orig_boundary = edge_boundary(S, edges)

        for i in range(n):
            for direction in [-1, 1]:
                compressed = compress(S, sv_list, sv_set, i, direction)
                new_boundary = edge_boundary(compressed, edges)
                total_tests += 1

                if new_boundary > orig_boundary:
                    boundary_increased += 1
                    if len(counterexamples) < 5:
                        counterexamples.append({
                            'size': size,
                            'hyperplane': i,
                            'direction': direction,
                            'orig_boundary': orig_boundary,
                            'new_boundary': new_boundary,
                        })

    print(f"  Total compression tests: {total_tests}")
    print(f"  Boundary increased: {boundary_increased}")

    if counterexamples:
        print(f"\n  Counterexamples (first {len(counterexamples)}):")
        for cx in counterexamples:
            print(f"    |S|={cx['size']}, H_{cx['hyperplane']} dir={cx['direction']}: "
                  f"∂={cx['orig_boundary']} -> {cx['new_boundary']}")

    # Also test iterative on some samples
    print(f"\n--- Iterative compression (sampled) ---")
    test_iterative_sampled(sv_list, sv_set, edges, n, N)


def test_iterative_compression(sv_list, sv_set, edges, n, N):
    """Test: does iterating compressions converge to a convex set?"""
    convergence_results = defaultdict(int)
    convex_at_fixed_point = 0
    not_convex_at_fixed_point = 0
    total = 0

    # Test all subsets for small N
    max_subsets = min(2**N, 2000)

    for size in range(1, N):
        for S_tuple in itertools.combinations(range(N), size):
            S = frozenset(S_tuple)
            total += 1

            # Iterate compressions
            current = S
            for iteration in range(100):
                changed = False
                for i in range(n):
                    new_S = compress(current, sv_list, sv_set, i, -1)
                    if new_S != current:
                        changed = True
                        current = new_S
                if not changed:
                    break

            if is_convex(current, sv_list, edges):
                convex_at_fixed_point += 1
            else:
                not_convex_at_fixed_point += 1
                if not_convex_at_fixed_point <= 3:
                    print(f"    NOT CONVEX at fixed point: |S|={size}, "
                          f"S_signs={[sv_list[j] for j in S]}, "
                          f"FP_signs={[sv_list[j] for j in current]}")

    print(f"  Total subsets tested: {total}")
    print(f"  Convex at fixed point: {convex_at_fixed_point}")
    print(f"  NOT convex at fixed point: {not_convex_at_fixed_point}")


def test_iterative_sampled(sv_list, sv_set, edges, n, N, num_samples=1000):
    """Test iterative compression on random subsets."""
    np.random.seed(456)
    convex_count = 0
    not_convex_count = 0

    for _ in range(num_samples):
        size = np.random.randint(1, N)
        S = frozenset(np.random.choice(N, size, replace=False))

        current = S
        for iteration in range(200):
            changed = False
            for i in range(n):
                new_S = compress(current, sv_list, sv_set, i, -1)
                if new_S != current:
                    changed = True
                    current = new_S
            if not changed:
                break

        if is_convex(current, sv_list, edges):
            convex_count += 1
        else:
            not_convex_count += 1
            if not_convex_count <= 3:
                print(f"    NOT CONVEX: size={size}")

    print(f"  Convex at fixed point: {convex_count}/{num_samples}")
    print(f"  NOT convex: {not_convex_count}/{num_samples}")


# ============================================================
# Define test arrangements
# ============================================================

def generic_lines_2d(n, seed=42):
    """Generate n lines in general position in R^2."""
    np.random.seed(seed)
    lines = []
    for _ in range(n):
        # Random line: ax + by + c = 0 with random a, b, c
        a, b = np.random.randn(2)
        c = np.random.randn() * 2
        lines.append((a, b, c))
    return lines


def generic_planes_3d(n, seed=42):
    """Generate n planes in general position in R^3."""
    np.random.seed(seed)
    planes = []
    for _ in range(n):
        a, b, c = np.random.randn(3)
        d = np.random.randn() * 2
        planes.append((a, b, c, d))
    return planes


if __name__ == "__main__":
    # 3 lines in R^2: expect 1+3+3 = 7 chambers
    print("=" * 60)
    print("TASK 1 & 2: Compression analysis")
    print("=" * 60)

    lines3 = generic_lines_2d(3)
    sv3 = chambers_2d(lines3)
    test_arrangement("3 lines in R²", sv3, expected_count=7)

    # 4 lines in R^2: expect 1+4+6 = 11 chambers
    lines4 = generic_lines_2d(4)
    sv4 = chambers_2d(lines4)
    test_arrangement("4 lines in R²", sv4, expected_count=11)

    # 5 lines in R^2: expect 1+5+10 = 16 chambers
    lines5 = generic_lines_2d(5)
    sv5 = chambers_2d(lines5)
    test_arrangement("5 lines in R²", sv5, expected_count=16)

    # 4 planes in R^3: expect 1+4+6+4 = 15 chambers
    planes4 = generic_planes_3d(4)
    sv4_3d = chambers_3d(planes4)
    test_arrangement("4 planes in R³", sv4_3d, expected_count=15)
