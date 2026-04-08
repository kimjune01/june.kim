"""
Final analysis:
1. The conjecture values only make sense for k < n. Check properly.
2. f(k) is DECREASING not increasing - this means initial segments have LARGER boundary.
   The correct direction: FINAL segments (removing from the end) should minimize.
3. Check: do FINAL segments of the shelling minimize boundary?
4. Check: does the REVERSE shelling (compression toward the end) work?
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
    n = len(lines)
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

    chamber_set = set()
    for v in vertices:
        for dx in np.linspace(-0.5, 0.5, 5):
            for dy in np.linspace(-0.5, 0.5, 5):
                x, y = v[0]+dx, v[1]+dy
                sv = tuple(sign(a*x + b*y + c) for a, b, c in lines)
                if 0 not in sv:
                    chamber_set.add(sv)
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]
    for x in np.linspace(min(all_x)-2, max(all_x)+2, 50):
        for y in np.linspace(min(all_y)-2, max(all_y)+2, 50):
            sv = tuple(sign(a*x + b*y + c) for a, b, c in lines)
            if 0 not in sv:
                chamber_set.add(sv)
    for angle in np.linspace(0, 2*np.pi, 100):
        x, y = 1000*np.cos(angle), 1000*np.sin(angle)
        sv = tuple(sign(a*x + b*y + c) for a, b, c in lines)
        if 0 not in sv:
            chamber_set.add(sv)
    return sorted(chamber_set)

def enumerate_chambers_3d(planes):
    n = len(planes)
    vertices = []
    for i, j, k in itertools.combinations(range(n), 3):
        A = np.array([planes[i][:3], planes[j][:3], planes[k][:3]], dtype=float)
        b_vec = np.array([-planes[i][3], -planes[j][3], -planes[k][3]], dtype=float)
        if abs(np.linalg.det(A)) > 1e-12:
            pt = np.linalg.solve(A, b_vec)
            vertices.append(pt)
    chamber_set = set()
    offsets = np.linspace(-0.3, 0.3, 5)
    for v in vertices:
        for dx in offsets:
            for dy in offsets:
                for dz in offsets:
                    pt = v + np.array([dx, dy, dz])
                    sv = tuple(sign(planes[i][0]*pt[0]+planes[i][1]*pt[1]+planes[i][2]*pt[2]+planes[i][3]) for i in range(n))
                    if 0 not in sv:
                        chamber_set.add(sv)
    for phi in np.linspace(0, np.pi, 20):
        for theta in np.linspace(0, 2*np.pi, 40):
            pt = 1000*np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)])
            sv = tuple(sign(planes[i][0]*pt[0]+planes[i][1]*pt[1]+planes[i][2]*pt[2]+planes[i][3]) for i in range(n))
            if 0 not in sv:
                chamber_set.add(sv)
    return sorted(chamber_set)

def build_graph(chambers):
    adj = defaultdict(set)
    for i in range(len(chambers)):
        for j in range(i+1, len(chambers)):
            if sum(1 for a, b in zip(chambers[i], chambers[j]) if a != b) == 1:
                adj[i].add(j)
                adj[j].add(i)
    return adj

def edge_boundary(S_set, adj):
    return sum(1 for v in S_set for u in adj[v] if u not in S_set)

def shelling_order(chambers, ell):
    def key(sv):
        return sum(l * s for l, s in zip(ell, sv))
    return sorted(range(len(chambers)), key=lambda i: key(chambers[i]))

def is_convex(S_set, adj):
    """Convex iff distances within S match distances in full graph."""
    for u in S_set:
        # BFS in full graph
        dist_full = {u: 0}
        q = [u]; qi = 0
        while qi < len(q):
            v = q[qi]; qi += 1
            for w in adj[v]:
                if w not in dist_full:
                    dist_full[w] = dist_full[v] + 1
                    q.append(w)
        # BFS in S
        dist_S = {u: 0}
        q2 = [u]; qi2 = 0
        while qi2 < len(q2):
            v = q2[qi2]; qi2 += 1
            for w in adj[v]:
                if w in S_set and w not in dist_S:
                    dist_S[w] = dist_S[v] + 1
                    q2.append(w)
        for v in S_set:
            if v == u: continue
            if v not in dist_S or dist_S[v] != dist_full[v]:
                return False
    return True

def test_final_segments(name, chambers, adj, ell):
    """Check if FINAL segments (complements of initial segments) minimize boundary."""
    N = len(chambers)
    order = shelling_order(chambers, ell)

    print(f"\n--- {name} ---")
    print(f"N={N}")

    failures_initial = 0
    failures_final = 0

    for m in range(1, N):
        initial_seg = set(order[:m])
        final_seg = set(order[N-m:])  # last m chambers

        initial_bd = edge_boundary(initial_seg, adj)
        final_bd = edge_boundary(final_seg, adj)

        min_bd = float('inf')
        if N <= 16 or m <= 8:
            for subset in itertools.combinations(range(N), m):
                bd = edge_boundary(set(subset), adj)
                if bd < min_bd:
                    min_bd = bd

            if initial_bd > min_bd:
                failures_initial += 1
            if final_bd > min_bd:
                failures_final += 1

            print(f"  m={m}: initial={initial_bd}, final={final_bd}, min={min_bd}  "
                  f"{'*INIT_FAIL' if initial_bd > min_bd else ''}  "
                  f"{'*FINAL_FAIL' if final_bd > min_bd else ''}")

    print(f"  Initial segment failures: {failures_initial}/{N-1}")
    print(f"  Final segment failures: {failures_final}/{N-1}")


def test_edge_counts_along_shelling(name, chambers, adj, ell):
    """
    Key insight test: For the shelling order C_1, ..., C_N,
    let the initial segment I_k = {C_1, ..., C_k}.

    Compute |∂I_k| for each k.

    For the K-K approach to work via initial segments, we need:
    The boundary |∂I_k| is a "nice" function of k.

    Also compute: boundary of initial segment of the ANTIPODAL shelling.
    """
    N = len(chambers)
    order = shelling_order(chambers, ell)
    rev_order = list(reversed(order))

    print(f"\n--- Boundary profile: {name} ---")
    print(f"  k  |∂I_k|(fwd)  |∂I_k|(rev)")
    for k in range(1, N):
        fwd = set(order[:k])
        rev = set(rev_order[:k])
        bd_fwd = edge_boundary(fwd, adj)
        bd_rev = edge_boundary(rev, adj)
        print(f"  {k:3d}   {bd_fwd:4d}        {bd_rev:4d}")


def exhaustive_boundary_minimizers(name, chambers, adj, dim):
    """For each m, find ALL sets that minimize boundary. Check if any is a half-space intersection."""
    N = len(chambers)
    n_hyp = len(chambers[0])

    print(f"\n--- Minimizers analysis: {name} ---")

    # Enumerate all halfspace intersections (convex sets)
    # A convex set is determined by choosing for each hyperplane: +, -, or "don't constrain"
    # That's 3^n subsets to check
    convex_sets_by_size = defaultdict(list)
    for mask in itertools.product([-1, 0, 1], repeat=n_hyp):
        S = set()
        for i, sv in enumerate(chambers):
            ok = True
            for j in range(n_hyp):
                if mask[j] != 0 and sv[j] != mask[j]:
                    ok = False
                    break
            if ok:
                S.add(i)
        if len(S) > 0:
            convex_sets_by_size[len(S)].append((frozenset(S), mask))

    for m in range(1, min(N, 10)):
        min_bd = float('inf')
        min_sets = []
        for subset in itertools.combinations(range(N), m):
            S = set(subset)
            bd = edge_boundary(S, adj)
            if bd < min_bd:
                min_bd = bd
                min_sets = [frozenset(subset)]
            elif bd == min_bd:
                min_sets.append(frozenset(subset))

        # Check if any minimizer is convex
        convex_minimizers = [S for S in min_sets if is_convex(set(S), adj)]

        # Check if any convex set of this size achieves min boundary
        convex_at_size = convex_sets_by_size.get(m, [])
        convex_boundaries = [edge_boundary(set(S), adj) for S, mask in convex_at_size]
        best_convex_bd = min(convex_boundaries) if convex_boundaries else float('inf')

        print(f"  m={m}: min_bd={min_bd}, #minimizers={len(min_sets)}, "
              f"#convex_minimizers={len(convex_minimizers)}, "
              f"best_convex_bd={best_convex_bd}, "
              f"convex achieves min={best_convex_bd == min_bd}")


if __name__ == '__main__':
    print("="*60)
    print("CRITICAL TEST: Initial vs Final segments")
    print("="*60)

    lines_3 = [(0, 1, 0), (1, 0, 0), (1, 1, -1)]
    ch3 = enumerate_chambers_2d(lines_3)
    adj3 = build_graph(ch3)
    ell3 = (1.0, 0.7, 0.3)

    test_final_segments("3 lines d=2", ch3, adj3, ell3)
    test_edge_counts_along_shelling("3 lines d=2", ch3, adj3, ell3)
    exhaustive_boundary_minimizers("3 lines d=2", ch3, adj3, 2)

    lines_4 = [(0, 1, 0), (1, 0, 0), (-1, 1, -1), (2, 1, -3)]
    ch4 = enumerate_chambers_2d(lines_4)
    adj4 = build_graph(ch4)
    ell4 = (1.0, 0.7, 0.3, 0.15)

    test_final_segments("4 lines d=2", ch4, adj4, ell4)
    test_edge_counts_along_shelling("4 lines d=2", ch4, adj4, ell4)
    exhaustive_boundary_minimizers("4 lines d=2", ch4, adj4, 2)

    planes_4 = [(0,0,1,0), (0,1,0,0), (1,0,0,0), (1,1,1,-1)]
    ch3d = enumerate_chambers_3d(planes_4)
    adj3d = build_graph(ch3d)
    ell3d = (1.0, 0.7, 0.3, 0.15)

    test_final_segments("4 planes d=3", ch3d, adj3d, ell3d)
    test_edge_counts_along_shelling("4 planes d=3", ch3d, adj3d, ell3d)
    exhaustive_boundary_minimizers("4 planes d=3", ch3d, adj3d, 3)

    # Key question: is the boundary profile of initial segments concave?
    # If concave, then initial segments are NOT minimizers (they overshoot).
    # If convex, they are good candidates.
    print("\n" + "="*60)
    print("BOUNDARY PROFILE SHAPE")
    print("="*60)
    for name, ch, adj, ell in [
        ("3 lines", ch3, adj3, ell3),
        ("4 lines", ch4, adj4, ell4),
        ("4 planes", ch3d, adj3d, ell3d),
    ]:
        N = len(ch)
        order = shelling_order(ch, ell)
        profile = []
        for k in range(N+1):
            if k == 0:
                profile.append(0)
            else:
                profile.append(edge_boundary(set(order[:k]), adj))

        # Compute second differences
        second_diff = [profile[k+1] - 2*profile[k] + profile[k-1] for k in range(1, N)]
        print(f"\n{name}:")
        print(f"  Profile: {profile}")
        print(f"  First diff (f(k)): {[profile[k+1]-profile[k] for k in range(N)]}")
        print(f"  Second diff: {second_diff}")
