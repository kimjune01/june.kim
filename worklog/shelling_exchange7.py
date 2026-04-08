"""
The conjecture may depend on the arrangement. One 6-line arrangement gives min_bd=5 < 6,
another gives min_bd=6 = 6 (tight). The conjecture might be about SPECIFIC arrangements
(like the braid arrangement) or about ALL arrangements.

Let me:
1. Test multiple random 6-line arrangements to see how often the counterexample appears
2. Characterize what makes the first arrangement fail
3. Check: is the conjecture only about the Boolean case (all 2^n sign vectors realized)?
"""

import itertools
import numpy as np
from collections import defaultdict
from math import comb

def sign(x):
    if x > 1e-9: return +1
    elif x < -1e-9: return -1
    else: return 0

def enumerate_chambers_2d(lines, verbose=False):
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
    expected = 1 + n + comb(n, 2)
    if verbose and len(chamber_set) != expected:
        print(f"  WARNING: {len(chamber_set)} != {expected}")
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
    # Test many random 6-line arrangements
    print("Testing 50 random 6-line arrangements for k=5 (|S|=16, bound=6):")
    print()

    np.random.seed(0)
    n_fail = 0
    n_total = 0

    for trial in range(50):
        # Random lines through origin + offset
        lines = []
        for i in range(6):
            theta = np.random.uniform(0, np.pi)
            c = np.random.uniform(-5, 5)
            lines.append((np.cos(theta), np.sin(theta), c))

        ch = enumerate_chambers_2d(lines)
        if len(ch) != 22:
            continue  # not general position

        adj = build_graph(ch)
        n_total += 1

        # Min boundary for size 6 (= complement of size 16)
        min_bd = float('inf')
        for subset in itertools.combinations(range(22), 6):
            bd = edge_boundary(set(subset), adj)
            if bd < min_bd:
                min_bd = bd

        if min_bd < 6:
            n_fail += 1
            if n_fail <= 3:
                print(f"  Trial {trial}: FAIL min_bd={min_bd}")

    print(f"\nResult: {n_fail}/{n_total} arrangements fail at k=5")
    print(f"({100*n_fail/max(n_total,1):.1f}% failure rate)")

    # The failing arrangement from before
    print("\n" + "="*60)
    print("Analyzing the failing arrangement")
    print("="*60)
    slopes = [0.0, 1.0, -0.5, 2.0, -1.5, 0.3]
    primes = [0, 1, 3, 7, 13, 23]
    lines_fail = [(slopes[i], -1.0, primes[i]) for i in range(6)]
    ch = enumerate_chambers_2d(lines_fail)
    adj = build_graph(ch)

    # Find the minimizing set of size 6
    min_bd = float('inf')
    min_sets = []
    for subset in itertools.combinations(range(22), 6):
        S = set(subset)
        bd = edge_boundary(S, adj)
        if bd < min_bd:
            min_bd = bd
            min_sets = [S]
        elif bd == min_bd:
            min_sets.append(S)

    print(f"Min boundary for |S|=6: {min_bd}")
    print(f"Number of minimizers: {len(min_sets)}")
    for S in min_sets[:5]:
        print(f"  {sorted(S)} convex={is_convex(S, adj)}")
        print(f"    signs: {[ch[i] for i in sorted(S)]}")

    # Degree distribution
    degs = [len(adj[i]) for i in range(22)]
    print(f"\nDegree distribution: {sorted(degs)}")
    print(f"Min degree: {min(degs)}, Max degree: {max(degs)}")

    # Compare with the working arrangement
    print("\n" + "="*60)
    print("Analyzing the working arrangement")
    print("="*60)
    lines_work = [(0, 1, 0), (1, 0, 0), (1, 1, -1), (1, -1, -2), (2, 1, -3), (1, 2, -4)]
    ch2 = enumerate_chambers_2d(lines_work)
    adj2 = build_graph(ch2)

    degs2 = [len(adj2[i]) for i in range(22)]
    print(f"Degree distribution: {sorted(degs2)}")

    min_bd2 = float('inf')
    for subset in itertools.combinations(range(22), 6):
        bd = edge_boundary(set(subset), adj2)
        if bd < min_bd2:
            min_bd2 = bd
    print(f"Min boundary for |S|=6: {min_bd2}")

    # Check: are both arrangements "generic" in the combinatorial sense?
    # (same number of chambers, same matroid)
    # For lines in general position in R^2, the matroid is uniform U_{2,n}
    # and all arrangements are combinatorially equivalent.
    # But wait -- they have different chamber graphs!

    # Actually for LINES through origin, all arrangements in general position
    # are combinatorially equivalent (same zonotope). But for AFFINE lines,
    # the combinatorial type can differ.

    # The key question: is the conjecture supposed to hold for ALL arrangements
    # in general position, or only for specific ones?

    print("\n" + "="*60)
    print("Do the two arrangements have the same degree sequence?")
    print("="*60)
    print(f"Fail arrangement degrees: {sorted(degs)}")
    print(f"Work arrangement degrees: {sorted(degs2)}")
    print(f"Same degree sequence: {sorted(degs) == sorted(degs2)}")

    # Check: total edges
    total_edges_1 = sum(degs) // 2
    total_edges_2 = sum(degs2) // 2
    print(f"Total edges: {total_edges_1} vs {total_edges_2}")

    # For n lines in R^2 in general position:
    # Each chamber is bounded by some number of lines.
    # Each line separates the arrangement, creating an edge for each pair
    # of adjacent chambers across it.
    # Total edges = sum over lines of (number of chamber pairs separated by that line)
    # For each line, the other n-1 lines divide it into n segments,
    # giving n+1 intervals, hence n+1 crossing edges? No...

    # Actually, for a simple arrangement of n lines:
    # Number of edges = sum_{i=1}^{n} (n - i + 1) ... no, simpler:
    # Each pair of adjacent chambers shares exactly one separating hyperplane.
    # The number of edges of the chamber graph = n*(n+1)/2 + n = ???

    # Let me just count
    print(f"\nExpected edges for n=6 lines: each of 6 lines has segments.")
    print(f"Each line is cut by 5 others into 6 pieces (in general position).")
    print(f"But each piece separates two chambers, giving 6 edges per line.")
    print(f"Wait, that gives 6*6=36 edges. Actual: {total_edges_1}")

    # Actually: n lines in general position, each line is divided into
    # n-1 bounded segments + 2 unbounded rays = n+1 pieces.
    # But not all pieces separate two chambers...
    # Actually each piece of a line (segment or ray) separates exactly
    # two adjacent chambers. So edges per line = n+1 segments (including rays).
    # Wait no. Line i is cut by the other n-1 lines into (n-1)+1 = n pieces
    # (n-1 intersection points, creating n intervals on the line including 2 rays).
    # Hmm, n-1 intersection points on a line create n intervals. Each interval
    # is a facet shared by two chambers. So edges per line = n.
    # Total edges = n * n = n^2.
    # For n=6: 36. Both have 36. Good.

    print(f"n^2 = 36. Both = {total_edges_1}. Consistent.")
