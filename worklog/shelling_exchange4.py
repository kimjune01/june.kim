"""
Key finding: f(k) is DECREASING (roughly), not increasing.
This means the approach is fundamentally backwards.

But the CONJECTURE might still be true. Let's verify:
1. All boundary minimizers are convex (confirmed for small cases).
2. No single shelling gives initial segments that minimize.
3. The obstacle is structural: the first chamber in ANY shelling has high boundary
   (it's a vertex of the arrangement with max degree), while interior chambers
   have low boundary contribution.

Let's also check: is the issue that the proxy for centroid evaluation is wrong?
The sign-vector dot product may not match the actual centroid-based shelling.

And: try the COMPLEMENTARY approach. The complement of an initial segment is a
final segment. By symmetry of the shelling (reverse ell gives reverse order),
the boundary of a set equals the boundary of its complement. So
|∂I_k| = |∂I_{N-k}| only if the graph is vertex-transitive, which it's not.

Actually |∂S| = |∂(V\S)| always (same set of boundary edges), so the profile
IS symmetric: |∂I_k| should equal |∂(final segment of size N-k)| = |∂I_{N-k}| of reverse.

Let me verify this and see if for the CONJECTURE's specific sizes,
convex sets match the bound.
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
    chamber_set = set()
    for v in vertices:
        for dx in np.linspace(-0.5, 0.5, 5):
            for dy in np.linspace(-0.5, 0.5, 5):
                sv = tuple(sign(a*(v[0]+dx)+b*(v[1]+dy)+c) for a,b,c in lines)
                if 0 not in sv: chamber_set.add(sv)
    all_x = [v[0] for v in vertices]; all_y = [v[1] for v in vertices]
    for x in np.linspace(min(all_x)-2, max(all_x)+2, 50):
        for y in np.linspace(min(all_y)-2, max(all_y)+2, 50):
            sv = tuple(sign(a*x+b*y+c) for a,b,c in lines)
            if 0 not in sv: chamber_set.add(sv)
    for angle in np.linspace(0, 2*np.pi, 100):
        sv = tuple(sign(a*1000*np.cos(angle)+b*1000*np.sin(angle)+c) for a,b,c in lines)
        if 0 not in sv: chamber_set.add(sv)
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
    # Verify |∂S| = |∂(V\S)|
    lines_3 = [(0, 1, 0), (1, 0, 0), (1, 1, -1)]
    ch = enumerate_chambers_2d(lines_3)
    adj = build_graph(ch)
    N = len(ch)
    print(f"Symmetry check (3 lines, N={N}):")
    all_v = set(range(N))
    for m in range(1, N):
        for subset in itertools.combinations(range(N), m):
            S = set(subset)
            comp = all_v - S
            assert edge_boundary(S, adj) == edge_boundary(comp, adj), f"Asymmetry for {S}"
    print("  ∂S = ∂(V\\S) confirmed for all subsets.")

    # THE REAL QUESTION: For what subset sizes does the conjecture predict?
    # |S| = C(k,0) + C(k,1) + ... + C(k,d) for some k.
    # The conjecture says: min |∂S| >= C(k,0) + ... + C(k,d-1).

    # For d=2, n lines: the arrangement has C(n,0)+C(n,1)+C(n,2) = 1+n+C(n,2) chambers.
    # Target sizes: |S| = 1+k+C(k,2) for k=0,1,...,n-1
    # (k=n gives all chambers, boundary=0, not interesting)

    print("\n" + "="*60)
    print("CONJECTURE VERIFICATION: d=2")
    print("="*60)

    for n_lines in [3, 4, 5]:
        # Use lines in truly general position
        np.random.seed(42)
        lines = []
        for i in range(n_lines):
            a, b = np.random.randn(2)
            c = np.random.randn() * 0.5
            lines.append((a, b, c))

        ch = enumerate_chambers_2d(lines)
        adj = build_graph(ch)
        N = len(ch)
        expected = 1 + n_lines + comb(n_lines, 2)
        print(f"\nn={n_lines} lines: N={N} (expected {expected})")

        for k in range(n_lines):  # k from 0 to n-1
            target_size = sum(comb(k, i) for i in range(3))  # 1 + k + C(k,2)
            target_bound = sum(comb(k, i) for i in range(2))  # 1 + k

            if target_size > N or target_size == 0:
                continue

            # Find min boundary over all subsets of this size
            if comb(N, target_size) > 2_000_000:
                print(f"  k={k}: |S|={target_size}, bound={target_bound} (skipped - too many subsets)")
                continue

            min_bd = float('inf')
            min_convex = False
            for subset in itertools.combinations(range(N), target_size):
                S = set(subset)
                bd = edge_boundary(S, adj)
                if bd < min_bd:
                    min_bd = bd
                    min_S = S

            min_convex = is_convex(min_S, adj)
            holds = min_bd >= target_bound
            print(f"  k={k}: |S|={target_size}, conj_bound={target_bound}, min_bd={min_bd}, "
                  f"holds={holds}, minimizer_convex={min_convex}")

    print("\n" + "="*60)
    print("CONJECTURE VERIFICATION: d=3")
    print("="*60)

    for n_planes in [4, 5]:
        from shelling_exchange3 import enumerate_chambers_3d

        np.random.seed(42 + n_planes)
        planes = []
        for i in range(n_planes):
            a, b, c = np.random.randn(3)
            d = np.random.randn() * 0.5
            planes.append((a, b, c, d))

        ch = enumerate_chambers_3d(planes)
        adj = build_graph(ch)
        N = len(ch)
        expected = sum(comb(n_planes, i) for i in range(4))
        print(f"\nn={n_planes} planes: N={N} (expected {expected})")

        for k in range(n_planes):
            target_size = sum(comb(k, i) for i in range(4))  # 1+k+C(k,2)+C(k,3)
            target_bound = sum(comb(k, i) for i in range(3))  # 1+k+C(k,2)

            if target_size > N or target_size == 0:
                continue

            if comb(N, target_size) > 2_000_000:
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

            min_convex = is_convex(min_S, adj) if min_S else None
            holds = min_bd >= target_bound
            print(f"  k={k}: |S|={target_size}, conj_bound={target_bound}, min_bd={min_bd}, "
                  f"holds={holds}, minimizer_convex={min_convex}")

    # Now the key analysis: WHY does the shelling approach fail?
    print("\n" + "="*60)
    print("STRUCTURAL ANALYSIS: Why shelling fails")
    print("="*60)

    lines_3 = [(0, 1, 0), (1, 0, 0), (1, 1, -1)]
    ch = enumerate_chambers_2d(lines_3)
    adj = build_graph(ch)
    N = len(ch)

    print(f"\n3 lines, N={N}")
    print("Degree sequence:", sorted([len(adj[i]) for i in range(N)]))

    # The problem: chambers at the "corners" of the arrangement (sign vectors
    # with all coordinates the same sign) have low degree (d = dim = 2).
    # They have the smallest boundary contribution.
    # But they are at the EXTREMES of any shelling, either first or last.
    # The initial segment starts with a corner (high ell value) which has low degree.
    # But its neighbors are NOT the next in the shelling -- they may be far apart.

    # The actual minimizers for m=1 are the degree-2 vertices.
    # In the shelling, the first vertex may or may not have degree 2.

    print("\nDegree of each vertex:")
    for i in range(N):
        print(f"  {i}: {ch[i]} deg={len(adj[i])}")

    print("\nConvex sets of size 4 (the interesting size for d=2, k=2 -> |S|=4):")
    n_hyp = len(ch[0])
    for mask in itertools.product([-1, 0, 1], repeat=n_hyp):
        S = set()
        for i, sv in enumerate(ch):
            if all(mask[j] == 0 or sv[j] == mask[j] for j in range(n_hyp)):
                S.add(i)
        if len(S) == 4:
            bd = edge_boundary(S, adj)
            conv = is_convex(S, adj)
            print(f"  mask={mask}: S={sorted(S)}, bd={bd}, convex={conv}")
