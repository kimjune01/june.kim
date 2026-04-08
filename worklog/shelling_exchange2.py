"""
Deeper investigation:
1. Fix the chamber enumeration (general position issues)
2. Check what sets actually minimize boundary - are they convex?
3. Test different shelling directions
4. Look at whether the CONJECTURE itself holds even if the shelling approach fails
"""

import itertools
import numpy as np
from collections import defaultdict
from math import comb

def sign(x):
    if x > 1e-9: return +1
    elif x < -1e-9: return -1
    else: return 0

def enumerate_chambers_2d(lines):
    """Brute force: try all 2^n sign vectors, keep those that are feasible."""
    n = len(lines)
    chambers = []
    # For each sign vector, check if the corresponding region is non-empty
    # by solving the LP: find (x,y) s.t. sign_i * (a_i*x + b_i*y + c_i) > 0
    # We use a grid of points to test feasibility

    # First, find all intersection points
    vertices = []
    for i in range(n):
        for j in range(i+1, n):
            a1, b1, c1 = lines[i]
            a2, b2, c2 = lines[j]
            det = a1*b2 - a2*b1
            if abs(det) > 1e-12:
                x = (b1*c2 - b2*c1) / det
                y = (a2*c1 - a1*c2) / det
                vertices.append((x, y))

    if not vertices:
        vertices = [(0, 0)]

    # Generate dense test points around and between vertices
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]
    x_min, x_max = min(all_x) - 2, max(all_x) + 2
    y_min, y_max = min(all_y) - 2, max(all_y) + 2

    chamber_set = set()

    # Vertex-based sampling
    for v in vertices:
        for dx in np.linspace(-0.5, 0.5, 5):
            for dy in np.linspace(-0.5, 0.5, 5):
                x, y = v[0]+dx, v[1]+dy
                sv = tuple(sign(a*x + b*y + c) for a, b, c in lines)
                if 0 not in sv:
                    chamber_set.add(sv)

    # Grid sampling
    for x in np.linspace(x_min, x_max, 50):
        for y in np.linspace(y_min, y_max, 50):
            sv = tuple(sign(a*x + b*y + c) for a, b, c in lines)
            if 0 not in sv:
                chamber_set.add(sv)

    # Far points
    for angle in np.linspace(0, 2*np.pi, 100):
        x, y = 1000*np.cos(angle), 1000*np.sin(angle)
        sv = tuple(sign(a*x + b*y + c) for a, b, c in lines)
        if 0 not in sv:
            chamber_set.add(sv)

    expected = sum(comb(n, i) for i in range(3))
    chambers = sorted(chamber_set)

    if len(chambers) != expected:
        print(f"  WARNING: found {len(chambers)} chambers, expected {expected} (lines may not be in general position)")
    else:
        print(f"  Found {len(chambers)} chambers (correct)")

    return chambers

def enumerate_chambers_3d(planes):
    n = len(planes)
    vertices = []
    for i, j, k in itertools.combinations(range(n), 3):
        A = np.array([planes[i][:3], planes[j][:3], planes[k][:3]], dtype=float)
        b_vec = np.array([-planes[i][3], -planes[j][3], -planes[k][3]], dtype=float)
        if abs(np.linalg.det(A)) > 1e-12:
            pt = np.linalg.solve(A, b_vec)
            vertices.append(pt)

    if not vertices:
        vertices = [np.array([0,0,0])]

    chamber_set = set()

    offsets = np.linspace(-0.3, 0.3, 5)
    for v in vertices:
        for dx in offsets:
            for dy in offsets:
                for dz in offsets:
                    pt = v + np.array([dx, dy, dz])
                    sv = tuple(sign(planes[i][0]*pt[0] + planes[i][1]*pt[1] + planes[i][2]*pt[2] + planes[i][3]) for i in range(n))
                    if 0 not in sv:
                        chamber_set.add(sv)

    # Spherical far points
    for phi in np.linspace(0, np.pi, 20):
        for theta in np.linspace(0, 2*np.pi, 40):
            pt = 1000 * np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)])
            sv = tuple(sign(planes[i][0]*pt[0] + planes[i][1]*pt[1] + planes[i][2]*pt[2] + planes[i][3]) for i in range(n))
            if 0 not in sv:
                chamber_set.add(sv)

    expected = sum(comb(n, i) for i in range(4))
    chambers = sorted(chamber_set)

    if len(chambers) != expected:
        print(f"  WARNING: found {len(chambers)} chambers, expected {expected}")
    else:
        print(f"  Found {len(chambers)} chambers (correct)")

    return chambers

def build_graph(chambers):
    adj = defaultdict(set)
    for i in range(len(chambers)):
        for j in range(i+1, len(chambers)):
            if sum(1 for a, b in zip(chambers[i], chambers[j]) if a != b) == 1:
                adj[i].add(j)
                adj[j].add(i)
    return adj

def edge_boundary(S_set, adj):
    count = 0
    for v in S_set:
        for u in adj[v]:
            if u not in S_set:
                count += 1
    return count  # each boundary edge counted once from S side

def shelling_order(chambers, ell):
    def key(sv):
        return sum(l * s for l, s in zip(ell, sv))
    return sorted(range(len(chambers)), key=lambda i: key(chambers[i]))

def is_convex(S_set, chambers, adj):
    """Check if S is convex in the chamber graph (closed under shortest paths)."""
    # BFS shortest paths between all pairs in S
    n = len(chambers)
    for u in S_set:
        # BFS from u
        dist = {u: 0}
        parent = {u: []}
        queue = [u]
        qi = 0
        while qi < len(queue):
            v = queue[qi]; qi += 1
            for w in adj[v]:
                if w not in dist:
                    dist[w] = dist[v] + 1
                    queue.append(w)

        # For each other vertex in S, check if there's a shortest path leaving S
        # Actually, we need: for every shortest path from u to v (both in S),
        # all intermediate vertices are in S.
        # Simpler check: BFS restricted to S should give same distances as BFS in full graph

        dist_restricted = {u: 0}
        queue2 = [u]
        qi2 = 0
        while qi2 < len(queue2):
            v = queue2[qi2]; qi2 += 1
            for w in adj[v]:
                if w in S_set and w not in dist_restricted:
                    dist_restricted[w] = dist_restricted[v] + 1
                    queue2.append(w)

        for v in S_set:
            if v == u: continue
            if v not in dist_restricted:
                return False  # not even connected in S
            if dist_restricted[v] != dist[v]:
                return False  # shortest path leaves S

    return True

def check_conjecture_value(chambers, adj, dim):
    """
    The conjecture: among sets of size sum_{i=0}^{dim} C(k,i),
    min boundary >= sum_{i=0}^{dim-1} C(k,i).

    Check for small k values.
    """
    n_hyperplanes = len(chambers[0])  # number of hyperplanes
    N = len(chambers)

    print(f"\n  Conjecture check (n={n_hyperplanes}, d={dim}):")
    for k in range(1, n_hyperplanes + 1):
        target_size = sum(comb(k, i) for i in range(dim + 1))
        target_boundary = sum(comb(k, i) for i in range(dim))

        if target_size > N:
            break
        if target_size > 15:  # skip if enumeration too expensive
            print(f"    k={k}: |S|={target_size}, conjectured |∂S|≥{target_boundary} (skipped - too large)")
            continue

        min_bd = float('inf')
        min_set = None
        for subset in itertools.combinations(range(N), target_size):
            S = set(subset)
            bd = edge_boundary(S, adj)
            if bd < min_bd:
                min_bd = bd
                min_set = S

        holds = min_bd >= target_boundary
        convex = is_convex(min_set, chambers, adj) if min_set else None
        print(f"    k={k}: |S|={target_size}, conjectured |∂S|≥{target_boundary}, actual min |∂S|={min_bd}, "
              f"holds={holds}, minimizer convex={convex}")


def test_multiple_shellings(chambers, adj, dim, n_trials=20):
    """Try many shelling directions to see if any gives initial segments that always minimize."""
    N = len(chambers)
    n_hyp = len(chambers[0])

    max_check = min(N, 8)  # only check subsets up to this size

    best_direction = None
    best_failures = float('inf')

    np.random.seed(42)
    for trial in range(n_trials):
        ell = np.random.randn(n_hyp)
        order = shelling_order(chambers, ell)

        failures = 0
        for m in range(1, max_check + 1):
            initial = set(order[:m])
            initial_bd = edge_boundary(initial, adj)

            # Check all subsets (expensive but thorough)
            min_bd = float('inf')
            for subset in itertools.combinations(range(N), m):
                bd = edge_boundary(set(subset), adj)
                if bd < min_bd:
                    min_bd = bd

            if initial_bd > min_bd:
                failures += 1

        if failures < best_failures:
            best_failures = failures
            best_direction = ell

    print(f"\n  Best shelling direction (out of {n_trials} trials): {best_failures} failures")
    if best_failures == 0:
        print(f"    Direction: {best_direction}")
    return best_failures


if __name__ == '__main__':
    print("="*60)
    print("TASK 2: 3 lines in general position, d=2")
    print("="*60)
    # Use lines that are guaranteed in general position
    # y = 0, x = 0, x + y - 1 = 0
    lines_3 = [(0, 1, 0), (1, 0, 0), (1, 1, -1)]
    ch3 = enumerate_chambers_2d(lines_3)
    adj3 = build_graph(ch3)

    print(f"\n  Chamber graph adjacency:")
    for i, sv in enumerate(ch3):
        print(f"    {i}: {sv}  neighbors={sorted(adj3[i])}")

    check_conjecture_value(ch3, adj3, 2)
    test_multiple_shellings(ch3, adj3, 2)

    # f(k) for several directions
    print("\n  f(k) for several shelling directions:")
    directions = [
        (1.0, 0.7, 0.3),
        (0.5, 1.0, 0.2),
        (0.1, 0.2, 1.0),
        (1.0, -0.5, 0.3),
    ]
    for ell in directions:
        order = shelling_order(ch3, ell)
        f_vals = []
        initial = set()
        for k, v in enumerate(order):
            deg = len(adj3[v])
            nb = len(adj3[v] & initial)
            f_vals.append(deg - 2*nb)
            initial.add(v)
        print(f"    ell={ell}: f(k)={f_vals}, monotone={all(f_vals[i]<=f_vals[i+1] for i in range(len(f_vals)-1))}")

    print("\n" + "="*60)
    print("TASK 3: 4 lines in general position, d=2")
    print("="*60)
    # Choose lines more carefully to ensure general position
    # y = 0, x = 0, y - x - 1 = 0, 2x + y - 3 = 0
    lines_4 = [(0, 1, 0), (1, 0, 0), (-1, 1, -1), (2, 1, -3)]
    ch4 = enumerate_chambers_2d(lines_4)
    adj4 = build_graph(ch4)
    check_conjecture_value(ch4, adj4, 2)
    test_multiple_shellings(ch4, adj4, 2, n_trials=50)

    print("\n" + "="*60)
    print("TASK 4: 4 planes in general position, d=3")
    print("="*60)
    # z=0, y=0, x=0, x+y+z-1=0 (the 4 faces of a tetrahedron)
    planes_4 = [(0,0,1,0), (0,1,0,0), (1,0,0,0), (1,1,1,-1)]
    ch3d = enumerate_chambers_3d(planes_4)
    adj3d = build_graph(ch3d)

    print(f"\n  Chamber graph adjacency:")
    for i, sv in enumerate(ch3d):
        print(f"    {i}: {sv}  deg={len(adj3d[i])} neighbors={sorted(adj3d[i])}")

    check_conjecture_value(ch3d, adj3d, 3)
    test_multiple_shellings(ch3d, adj3d, 3, n_trials=50)

    print("\n" + "="*60)
    print("KEY QUESTION: Do convex sets minimize boundary?")
    print("="*60)
    # For 3 lines, check which sets of each size minimize boundary and whether they're convex
    print("\n3 lines:")
    N = len(ch3)
    for m in range(1, N+1):
        min_bd = float('inf')
        min_sets = []
        for subset in itertools.combinations(range(N), m):
            S = set(subset)
            bd = edge_boundary(S, adj3)
            if bd < min_bd:
                min_bd = bd
                min_sets = [S]
            elif bd == min_bd:
                min_sets.append(S)

        # Check convexity of each minimizer
        convex_count = sum(1 for S in min_sets if is_convex(S, ch3, adj3))
        print(f"  m={m}: min boundary={min_bd}, {len(min_sets)} minimizers, {convex_count} convex")
        if convex_count < len(min_sets):
            for S in min_sets:
                c = is_convex(S, ch3, adj3)
                print(f"    {S} signs={[ch3[i] for i in S]} convex={c}")

    print("\n4 planes in R³:")
    N3d = len(ch3d)
    for m in range(1, min(N3d+1, 10)):
        min_bd = float('inf')
        min_sets = []
        for subset in itertools.combinations(range(N3d), m):
            S = set(subset)
            bd = edge_boundary(S, adj3d)
            if bd < min_bd:
                min_bd = bd
                min_sets = [S]
            elif bd == min_bd:
                min_sets.append(S)

        convex_count = sum(1 for S in min_sets if is_convex(S, ch3d, adj3d))
        print(f"  m={m}: min boundary={min_bd}, {len(min_sets)} minimizers, {convex_count} convex")
        if convex_count == 0 and len(min_sets) <= 5:
            for S in min_sets:
                print(f"    {S} signs={[ch3d[i] for i in S]} convex={is_convex(S, ch3d, adj3d)}")
