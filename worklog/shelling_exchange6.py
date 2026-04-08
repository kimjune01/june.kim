"""
The failure at k=n-1 for n=6 lines: |S|=16, bound=6, min_bd=5.
Is this a real counterexample to the conjecture, or a bug?

Check: for n=6 lines, |S|=16 = C(5,0)+C(5,1)+C(5,2) = 1+5+10 = 16.
The bound says min |∂S| >= C(5,0)+C(5,1) = 1+5 = 6.
But we found min_bd = 5.

This means |∂S| = 5 < 6 = conjectured bound.

BUT WAIT: the conjecture is about sets of size C(k,0)+...+C(k,d).
For d=2, that's 1+k+C(k,2).
For k=5: 1+5+10 = 16.
N = 22 for n=6 lines.

The question is: is k allowed to be n-1=5 when n=6?

Let me check: what's the actual min boundary for all interesting sizes,
and whether the issue is the complement symmetry (|S|=16, |V\S|=6,
and |∂S|=|∂(V\S)|, so this is equivalent to a set of size 6 with boundary 5).

Also check: the bound C(k,0)+...+C(k,d-1) = 1+k for d=2.
For |S|=16 out of 22, the complement has size 6.
A complement of size 6 with boundary 5 seems reasonable.

The conjecture might only apply for k < n/2 or when |S| <= N/2.
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
    primes = [0, 1, 3, 7, 13, 23]
    slopes = [0.0, 1.0, -0.5, 2.0, -1.5, 0.3]
    lines_6 = [(slopes[i], -1.0, primes[i]) for i in range(6)]
    ch = enumerate_chambers_2d(lines_6)
    adj = build_graph(ch)
    N = len(ch)
    print(f"n=6 lines, N={N} (expected {1+6+15}=22)")

    # Check all subset sizes
    print(f"\nBoundary profile for n=6, d=2:")
    print(f"{'m':>4} {'min_bd':>7} {'any_convex_min':>15} {'conj_size':>10} {'conj_bd':>8}")

    conj_sizes = {}
    for k in range(6):
        s = sum(comb(k, i) for i in range(3))
        b = sum(comb(k, i) for i in range(2))
        conj_sizes[s] = (k, b)

    for m in range(1, N):
        # For large m, use complement
        if m > N//2 + 1:
            # |∂S| = |∂(V\S)|, so min boundary for size m = min boundary for size N-m
            # (already computed)
            continue

        if comb(N, m) > 5_000_000:
            print(f"{m:>4}  (skipped)")
            continue

        min_bd = float('inf')
        min_S = None
        for subset in itertools.combinations(range(N), m):
            S = set(subset)
            bd = edge_boundary(S, adj)
            if bd < min_bd:
                min_bd = bd
                min_S = S

        mc = is_convex(min_S, adj) if min_S else None
        conj_info = ""
        if m in conj_sizes:
            k, b = conj_sizes[m]
            conj_info = f"  k={k}, bound={b}, {'OK' if min_bd >= b else 'FAIL'}"

        print(f"{m:>4} {min_bd:>7} {'Y' if mc else 'N':>15}{conj_info}")

    # Now check the complement: |S|=16 means |V\S|=6
    print(f"\nComplement check:")
    print(f"|S|=16 with min_bd=? is equivalent to |V\\S|=6 with same boundary")

    # Find min boundary for size 6
    min_bd_6 = float('inf')
    min_S_6 = None
    for subset in itertools.combinations(range(N), 6):
        S = set(subset)
        bd = edge_boundary(S, adj)
        if bd < min_bd_6:
            min_bd_6 = bd
            min_S_6 = S

    print(f"Min boundary for |S|=6: {min_bd_6}")
    print(f"This set: {min_S_6}")
    print(f"Convex: {is_convex(min_S_6, adj)}")
    print(f"Signs: {[ch[i] for i in min_S_6]}")

    # Is its complement of size 16 convex?
    comp = set(range(N)) - min_S_6
    print(f"Complement size: {len(comp)}")
    print(f"Complement boundary: {edge_boundary(comp, adj)}")
    print(f"Complement convex: {is_convex(comp, adj)}")

    print(f"\nSo for |S|=16 (=C(5,0)+C(5,1)+C(5,2)), the conjecture predicts |∂S|≥6.")
    print(f"The complement of a size-6 set with boundary 5 gives |S|=16 with boundary 5.")
    print(f"This is a genuine counterexample IF k=5 is within the conjecture's scope for n=6.")
    print(f"\nNote: The conjecture (arxiv 2604.01061) states the bound for")
    print(f"sets of size sum_{{i=0}}^d C(k,i). The parameter k can be up to n")
    print(f"(giving all chambers), but the bound is only interesting for k < n.")
    print(f"For k=n-1=5, n=6: the set has 16 out of 22 chambers (73%).")
    print(f"The complement has only 6 chambers. The minimizer for size 6 has boundary 5.")
    print(f"Since |∂S|=|∂(V\\S)|, min boundary for size 16 also = 5.")
    print(f"But the conjectured bound is 1+5=6. So this is a COUNTEREXAMPLE to the conjecture")
    print(f"as stated, unless the conjecture restricts k to be at most floor(n/2) or similar.")

    # Double-check with a different set of 6 lines
    print("\n" + "="*60)
    print("Verification with different 6-line arrangement")
    print("="*60)
    lines_6b = [(0, 1, 0), (1, 0, 0), (1, 1, -1), (1, -1, -2), (2, 1, -3), (1, 2, -4)]
    ch_b = enumerate_chambers_2d(lines_6b)
    adj_b = build_graph(ch_b)
    N_b = len(ch_b)
    print(f"N={N_b}")

    if N_b == 22:
        # Check size 16
        min_bd_16 = float('inf')
        # Use complement: find min boundary for size 6
        min_bd_6b = float('inf')
        for subset in itertools.combinations(range(N_b), 6):
            S = set(subset)
            bd = edge_boundary(S, adj_b)
            if bd < min_bd_6b:
                min_bd_6b = bd

        print(f"Min boundary for |S|=6: {min_bd_6b}")
        print(f"So min boundary for |S|=16: {min_bd_6b}")
        print(f"Conjecture bound for k=5: {1+5}=6")
        print(f"Holds: {min_bd_6b >= 6}")
