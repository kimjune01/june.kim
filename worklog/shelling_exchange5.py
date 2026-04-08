"""
Fix: n=5 lines gave 15 chambers instead of 16 (not general position with random seed 42).
The conjecture failure at k=4 for n=5 is likely due to non-general-position.
Let's use carefully chosen lines and verify.
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
                vertices.append(((b1*c2-b2*c1)/det, (a2*c1-a1*c2)/det))
    # Check general position: no three lines concurrent
    for i, j, k in itertools.combinations(range(n), 3):
        a1,b1,c1 = lines[i]; a2,b2,c2 = lines[j]; a3,b3,c3 = lines[k]
        det = a1*(b2*c3-b3*c2) - b1*(a2*c3-a3*c2) + c1*(a2*b3-a3*b2)
        if abs(det) < 1e-8:
            print(f"  WARNING: lines {i},{j},{k} are concurrent!")

    chamber_set = set()
    for v in vertices:
        for dx in np.linspace(-0.3, 0.3, 7):
            for dy in np.linspace(-0.3, 0.3, 7):
                sv = tuple(sign(a*(v[0]+dx)+b*(v[1]+dy)+c) for a,b,c in lines)
                if 0 not in sv: chamber_set.add(sv)
    if vertices:
        all_x = [v[0] for v in vertices]; all_y = [v[1] for v in vertices]
        for x in np.linspace(min(all_x)-3, max(all_x)+3, 80):
            for y in np.linspace(min(all_y)-3, max(all_y)+3, 80):
                sv = tuple(sign(a*x+b*y+c) for a,b,c in lines)
                if 0 not in sv: chamber_set.add(sv)
    for angle in np.linspace(0, 2*np.pi, 200):
        sv = tuple(sign(a*1000*np.cos(angle)+b*1000*np.sin(angle)+c) for a,b,c in lines)
        if 0 not in sv: chamber_set.add(sv)
    expected = 1 + n + comb(n, 2)
    if len(chamber_set) != expected:
        print(f"  WARNING: {len(chamber_set)} chambers, expected {expected}")
    else:
        print(f"  OK: {len(chamber_set)} chambers")
    return sorted(chamber_set)

def enumerate_chambers_3d(planes):
    n = len(planes)
    vertices = []
    for i, j, k in itertools.combinations(range(n), 3):
        A = np.array([planes[i][:3], planes[j][:3], planes[k][:3]], dtype=float)
        b_vec = np.array([-planes[i][3], -planes[j][3], -planes[k][3]], dtype=float)
        if abs(np.linalg.det(A)) > 1e-12:
            vertices.append(np.linalg.solve(A, b_vec))
    # Check general position: no 4 planes concurrent
    for combo in itertools.combinations(range(n), 4):
        A = np.array([planes[i][:3] for i in combo], dtype=float)[:3]
        b_vec = np.array([-planes[i][3] for i in combo], dtype=float)[:3]
        if abs(np.linalg.det(A)) > 1e-12:
            pt = np.linalg.solve(A, b_vec)
            val = planes[combo[3]][0]*pt[0]+planes[combo[3]][1]*pt[1]+planes[combo[3]][2]*pt[2]+planes[combo[3]][3]
            if abs(val) < 1e-8:
                print(f"  WARNING: planes {combo} meet at a point!")

    chamber_set = set()
    offsets = np.linspace(-0.2, 0.2, 5)
    for v in vertices:
        for dx in offsets:
            for dy in offsets:
                for dz in offsets:
                    pt = v + np.array([dx, dy, dz])
                    sv = tuple(sign(planes[i][0]*pt[0]+planes[i][1]*pt[1]+planes[i][2]*pt[2]+planes[i][3]) for i in range(n))
                    if 0 not in sv: chamber_set.add(sv)
    for phi in np.linspace(0, np.pi, 30):
        for theta in np.linspace(0, 2*np.pi, 60):
            pt = 1000*np.array([np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)])
            sv = tuple(sign(planes[i][0]*pt[0]+planes[i][1]*pt[1]+planes[i][2]*pt[2]+planes[i][3]) for i in range(n))
            if 0 not in sv: chamber_set.add(sv)
    expected = sum(comb(n, i) for i in range(4))
    if len(chamber_set) != expected:
        print(f"  WARNING: {len(chamber_set)} chambers, expected {expected}")
    else:
        print(f"  OK: {len(chamber_set)} chambers")
    return sorted(chamber_set)

def build_graph(chambers):
    adj = defaultdict(set)
    for i in range(len(chambers)):
        for j in range(i+1, len(chambers)):
            if sum(1 for a, b in zip(chambers[i], chambers[j]) if a != b) == 1:
                adj[i].add(j); adj[j].add(i)
    return adj

def edge_boundary(S_set, adj):
    return sum(1 for v in S_set for u in adj[v] if u not in S_set)

def is_convex(S_set, adj):
    for u in S_set:
        dist_full = {u: 0}; q = [u]; qi = 0
        while qi < len(q):
            v = q[qi]; qi += 1
            for w in adj[v]:
                if w not in dist_full: dist_full[w] = dist_full[v]+1; q.append(w)
        dist_S = {u: 0}; q2 = [u]; qi2 = 0
        while qi2 < len(q2):
            v = q2[qi2]; qi2 += 1
            for w in adj[v]:
                if w in S_set and w not in dist_S: dist_S[w] = dist_S[v]+1; q2.append(w)
        for v in S_set:
            if v != u and (v not in dist_S or dist_S[v] != dist_full[v]): return False
    return True

if __name__ == '__main__':
    print("="*60)
    print("GENERAL POSITION LINES for d=2")
    print("="*60)

    # Carefully chosen lines in general position
    # Use y = m*x + b form, ensure no 3 concurrent
    # Line i: y = i*x + prime_i
    # As (a, b, c) = (m, -1, b) for y = mx + b, i.e. mx - y + b = 0

    for n_lines in [3, 4, 5, 6]:
        primes = [0, 1, 3, 7, 13, 23]
        slopes = [0.0, 1.0, -0.5, 2.0, -1.5, 0.3]
        lines = [(slopes[i], -1.0, primes[i]) for i in range(n_lines)]
        print(f"\nn={n_lines} lines:")
        ch = enumerate_chambers_2d(lines)
        adj = build_graph(ch)
        N = len(ch)

        for k in range(n_lines):
            target_size = sum(comb(k, i) for i in range(3))
            target_bound = sum(comb(k, i) for i in range(2))
            if target_size > N or target_size == 0: continue
            if comb(N, target_size) > 5_000_000:
                print(f"  k={k}: |S|={target_size}, bound={target_bound} (skipped)")
                continue

            min_bd = float('inf')
            min_S = None
            for subset in itertools.combinations(range(N), target_size):
                S = set(subset)
                bd = edge_boundary(S, adj)
                if bd < min_bd:
                    min_bd = bd
                    min_S = S

            mc = is_convex(min_S, adj) if min_S else None
            holds = min_bd >= target_bound
            print(f"  k={k}: |S|={target_size}, bound={target_bound}, min_bd={min_bd}, "
                  f"holds={holds}, convex={mc}")

    print("\n" + "="*60)
    print("GENERAL POSITION PLANES for d=3")
    print("="*60)

    for n_planes in [4, 5]:
        # Use specific planes in general position
        if n_planes == 4:
            planes = [(1,0,0,0), (0,1,0,0), (0,0,1,0), (1,1,1,-2)]
        else:
            planes = [(1,0,0,0), (0,1,0,0), (0,0,1,0), (1,1,1,-2), (1,-1,2,-3)]

        print(f"\nn={n_planes} planes:")
        ch = enumerate_chambers_3d(planes)
        adj = build_graph(ch)
        N = len(ch)

        for k in range(n_planes):
            target_size = sum(comb(k, i) for i in range(4))
            target_bound = sum(comb(k, i) for i in range(3))
            if target_size > N or target_size == 0: continue
            if comb(N, target_size) > 10_000_000:
                print(f"  k={k}: |S|={target_size}, bound={target_bound} (skipped)")
                continue

            min_bd = float('inf')
            min_S = None
            for subset in itertools.combinations(range(N), target_size):
                S = set(subset)
                bd = edge_boundary(S, adj)
                if bd < min_bd:
                    min_bd = bd
                    min_S = S

            mc = is_convex(min_S, adj) if min_S else None
            holds = min_bd >= target_bound
            print(f"  k={k}: |S|={target_size}, bound={target_bound}, min_bd={min_bd}, "
                  f"holds={holds}, convex={mc}")

    # ================================================================
    # Now let's understand f(k) properly
    # ================================================================
    print("\n" + "="*60)
    print("f(k) ANALYSIS: What the decreasing trend means")
    print("="*60)

    # f(k) = change in boundary when adding C_k to I_{k-1}
    # f(k) = deg(C_k) - 2 * |{nbrs of C_k in I_{k-1}}|
    #
    # Cumulative boundary: |∂I_k| = sum_{j=1}^{k} f(j)
    #
    # For initial segments to minimize: we need |∂I_m| <= |∂S| for all |S|=m.
    # For K-K: we need f to be non-decreasing (so removing last, adding earlier doesn't help).
    #
    # f is DECREASING because:
    # - Early chambers (extremes of ell) have few neighbors in the initial segment -> high f
    # - Late chambers have MANY neighbors in the initial segment -> low (negative) f
    # - This is exactly backwards from what K-K needs!
    #
    # In the classical K-K for hypercube/simplicial complex:
    # - The order is by "weight" or "level"
    # - Adding a vertex of weight k to the initial segment contributes exactly k to boundary
    # - k increases with position -> f non-decreasing
    #
    # For chamber graphs, the analog would need:
    # - Chambers ordered so that "larger" chambers have more neighbors inside
    # - But the shelling order does the opposite: it adds boundary chambers first
    #
    # CONCLUSION: The K-K-via-shelling approach is fundamentally mismatched.
    # The shelling order produces DECREASING f(k), when we need NON-DECREASING.
    #
    # This doesn't mean the conjecture is false - just that this proof strategy fails.

    print("""
ANALYSIS:

The shelling order adds chambers from one extreme of a linear functional to the other.
Each new chamber C_k has at least one facet touching the previous convex hull.

f(k) = deg(C_k) - 2 * |neighbors of C_k in {C_1,...,C_{k-1}}|

f(k) measures the CHANGE in boundary when adding C_k.

OBSERVATION: f(k) is DECREASING, not increasing.
- Early chambers (at the extreme) have few neighbors already added -> large f
- Late chambers (in the interior relative to what's been added) -> more neighbors -> small/negative f
- The last chamber (opposite extreme) has ALL its neighbors already added -> most negative f

For K-K to work via shelling, f would need to be NON-DECREASING.
Since f is decreasing, the exchange argument goes the WRONG way:
swapping a late chamber (low f) for an early one (high f) would DECREASE boundary,
which means initial segments have EXCESS boundary, not minimum.

This is the OPPOSITE of what happens in the Boolean lattice / Kruskal-Katona,
where the compression pushes toward initial segments because they have LESS boundary.

The shelling approach is structurally incompatible with edge-isoperimetry.
""")
