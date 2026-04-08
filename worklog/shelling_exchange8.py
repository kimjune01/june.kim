"""
Key findings so far:
- The conjecture holds for k <= n-2 in all tested cases (d=2, d=3)
- The conjecture FAILS for k=n-1 in many arrangements (58.5% of random 6-line)
- The shelling/K-K approach fails because f(k) is decreasing, not increasing
- All boundary minimizers are convex in tested cases

Now let's verify:
1. Does the conjecture always hold for k <= n-2?
2. Check the paper's formula more carefully.
   For n hyperplanes in R^d, the chambers are the vertices of the zonotope.
   The conjecture talks about subsets of size sum_{i=0}^d C(k,i).
   For d=2: |S| = 1+k+C(k,2). For k <= n-1.

   Actually wait -- I need to re-read the conjecture. It says:
   "Among all subsets S of chambers with |S| = sum_{i=0}^d C(k,i)"

   Maybe the conjecture is only for k <= n-d? Or k <= n/2?
   Let me just exhaustively check for which (n, k, d) it holds.

3. Separately: verify the ACTUAL conjecture that convex sets minimize boundary.
"""

import itertools
import numpy as np
from collections import defaultdict
from math import comb

def sign(x):
    if x > 1e-9: return +1
    elif x < -1e-9: return -1
    else: return 0

def make_gp_lines(n, seed=None):
    """Make n lines in general position in R^2."""
    if seed is not None:
        np.random.seed(seed)
    # Use slopes that are algebraically independent-ish
    for attempt in range(100):
        lines = []
        for i in range(n):
            theta = np.random.uniform(0, np.pi)
            c = np.random.uniform(-5, 5)
            lines.append((np.cos(theta), np.sin(theta), c))
        # Check general position
        ok = True
        for i, j, k in itertools.combinations(range(n), 3):
            a1,b1,c1 = lines[i]; a2,b2,c2 = lines[j]; a3,b3,c3 = lines[k]
            det = a1*(b2*c3-b3*c2) - b1*(a2*c3-a3*c2) + c1*(a2*b3-a3*b2)
            if abs(det) < 1e-6:
                ok = False; break
        if ok:
            return lines
    raise ValueError("Could not find GP arrangement")

def enumerate_chambers_2d(lines):
    n = len(lines)
    vertices = []
    for i in range(n):
        for j in range(i+1, n):
            a1,b1,c1 = lines[i]; a2,b2,c2 = lines[j]
            det = a1*b2 - a2*b1
            if abs(det) > 1e-12:
                vertices.append(((b1*c2-b2*c1)/det, (a2*c1-a1*c2)/det))
    chamber_set = set()
    for v in vertices:
        for dx in np.linspace(-0.3, 0.3, 7):
            for dy in np.linspace(-0.3, 0.3, 7):
                sv = tuple(sign(a*(v[0]+dx)+b*(v[1]+dy)+c) for a,b,c in lines)
                if 0 not in sv: chamber_set.add(sv)
    if vertices:
        xs = [v[0] for v in vertices]; ys = [v[1] for v in vertices]
        for x in np.linspace(min(xs)-3, max(xs)+3, 80):
            for y in np.linspace(min(ys)-3, max(ys)+3, 80):
                sv = tuple(sign(a*x+b*y+c) for a,b,c in lines)
                if 0 not in sv: chamber_set.add(sv)
    for angle in np.linspace(0, 2*np.pi, 200):
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

def min_boundary_for_size(m, N, adj):
    min_bd = float('inf')
    for subset in itertools.combinations(range(N), m):
        bd = edge_boundary(set(subset), adj)
        if bd < min_bd:
            min_bd = bd
    return min_bd

if __name__ == '__main__':
    print("="*60)
    print("SYSTEMATIC CHECK: For which (n, k) does the conjecture hold?")
    print("d=2, testing 10 random arrangements per n")
    print("="*60)

    for n in [3, 4, 5, 6]:
        expected_N = 1 + n + comb(n, 2)
        print(f"\nn={n} lines, N={expected_N}")

        for k in range(n):
            target_size = sum(comb(k, i) for i in range(3))
            target_bound = sum(comb(k, i) for i in range(2))

            if target_size > expected_N or target_size == 0:
                continue

            if comb(expected_N, target_size) > 10_000_000:
                print(f"  k={k}: |S|={target_size}, bound={target_bound} (skipped - too large)")
                continue

            n_pass = 0
            n_total = 0
            min_min_bd = float('inf')

            for seed in range(10):
                lines = make_gp_lines(n, seed=seed*100+n)
                ch = enumerate_chambers_2d(lines)
                if len(ch) != expected_N:
                    continue
                adj = build_graph(ch)
                n_total += 1

                mb = min_boundary_for_size(target_size, expected_N, adj)
                min_min_bd = min(min_min_bd, mb)
                if mb >= target_bound:
                    n_pass += 1

            print(f"  k={k}: |S|={target_size}, bound={target_bound}, "
                  f"pass={n_pass}/{n_total}, worst min_bd={min_min_bd}")

    # Now check: is the failure at k=n-1 related to the complement being "too small"?
    # For d=2, n=6, k=5: |S|=16, |V\S|=6.
    # The complement has size 6 and needs boundary >= 6.
    # A convex set of size 6 (= halfspace with 6 chambers) has boundary...
    # Let's check: how many convex sets of size 6 exist, and their boundaries.

    print("\n" + "="*60)
    print("CONVEX SET BOUNDARIES for n=6, d=2")
    print("="*60)

    lines = make_gp_lines(6, seed=100)
    ch = enumerate_chambers_2d(lines)
    adj = build_graph(ch)
    N = len(ch)
    n_hyp = 6

    convex_by_size = defaultdict(list)
    for mask in itertools.product([-1, 0, 1], repeat=n_hyp):
        S = set()
        for i, sv in enumerate(ch):
            if all(mask[j] == 0 or sv[j] == mask[j] for j in range(n_hyp)):
                S.add(i)
        if 0 < len(S) < N:
            bd = edge_boundary(S, adj)
            convex_by_size[len(S)].append((frozenset(S), mask, bd))

    print(f"N={N}")
    for size in sorted(convex_by_size.keys()):
        entries = convex_by_size[size]
        bds = [e[2] for e in entries]
        print(f"  size={size}: {len(entries)} convex sets, boundaries={sorted(set(bds))}")
