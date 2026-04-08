"""
Shelling exchange lemma verification for chamber graphs of hyperplane arrangements.

Tests:
1. Does the initial segment of a line shelling minimize edge boundary?
2. Does the exchange lemma hold (swapping last for first gap)?
3. Is f(k) = deg(C_k) - 2*|neighbors in earlier segment| non-decreasing?
"""

import itertools
import numpy as np
from collections import defaultdict

# ============================================================
# Part 1: Build chamber graphs from hyperplane arrangements
# ============================================================

def sign(x):
    if x > 1e-9:
        return +1
    elif x < -1e-9:
        return -1
    else:
        return 0

def enumerate_chambers_2d(lines):
    """
    lines: list of (a, b, c) where ax + by + c = 0
    Returns: list of sign vectors (tuples of +1/-1), one per chamber.
    """
    n = len(lines)
    # Find all intersection points
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

    # Sample many points and collect sign vectors
    chambers = set()
    # Use intersection points offset in all 2^n quadrants, plus far-away points
    test_points = []
    for v in vertices:
        for dx in [-0.1, 0.1]:
            for dy in [-0.1, 0.1]:
                test_points.append((v[0]+dx, v[1]+dy))
    # Also add far points
    for angle_deg in range(0, 360, 15):
        angle = np.radians(angle_deg)
        test_points.append((100*np.cos(angle), 100*np.sin(angle)))

    for x, y in test_points:
        sv = tuple(sign(a*x + b*y + c) for a, b, c in lines)
        if 0 not in sv:
            chambers.add(sv)

    # Verify count: n lines in general position -> C(n,0)+C(n,1)+C(n,2) chambers
    from math import comb
    expected = sum(comb(n, i) for i in range(3))  # d=2
    if len(chambers) != expected:
        print(f"WARNING: found {len(chambers)} chambers, expected {expected}")

    return sorted(chambers)

def enumerate_chambers_3d(planes):
    """
    planes: list of (a, b, c, d) where ax + by + cz + d = 0
    Returns: list of sign vectors.
    """
    n = len(planes)
    # Find intersection points of triples of planes
    vertices = []
    for i, j, k in itertools.combinations(range(n), 3):
        A = np.array([planes[i][:3], planes[j][:3], planes[k][:3]], dtype=float)
        b = np.array([-planes[i][3], -planes[j][3], -planes[k][3]], dtype=float)
        if abs(np.linalg.det(A)) > 1e-12:
            pt = np.linalg.solve(A, b)
            vertices.append(pt)

    chambers = set()
    offsets = [-0.1, 0.1]
    for v in vertices:
        for dx in offsets:
            for dy in offsets:
                for dz in offsets:
                    pt = (v[0]+dx, v[1]+dy, v[2]+dz)
                    sv = tuple(sign(a*pt[0] + b*pt[1] + c*pt[2] + d) for a, b, c, d in planes)
                    if 0 not in sv:
                        chambers.add(sv)
    # Far points
    for angle1 in range(0, 360, 30):
        for angle2 in range(-90, 91, 30):
            a1, a2 = np.radians(angle1), np.radians(angle2)
            pt = (100*np.cos(a2)*np.cos(a1), 100*np.cos(a2)*np.sin(a1), 100*np.sin(a2))
            sv = tuple(sign(a*pt[0] + b*pt[1] + c*pt[2] + d) for a, b, c, d in planes)
            if 0 not in sv:
                chambers.add(sv)

    from math import comb
    expected = sum(comb(n, i) for i in range(4))  # d=3
    if len(chambers) != expected:
        print(f"WARNING: found {len(chambers)} chambers, expected {expected}")

    return sorted(chambers)

def build_chamber_graph(chambers):
    """
    Two chambers are adjacent iff their sign vectors differ in exactly one coordinate.
    Returns adjacency list.
    """
    n = len(chambers)
    adj = defaultdict(set)
    idx = {c: i for i, c in enumerate(chambers)}

    for i in range(n):
        for j in range(i+1, n):
            diffs = sum(1 for a, b in zip(chambers[i], chambers[j]) if a != b)
            if diffs == 1:
                adj[i].add(j)
                adj[j].add(i)

    return adj

def shelling_order(chambers, ell):
    """
    Sort chambers by ℓ(centroid). For sign vectors, we use a proxy:
    the dot product of the sign vector with ell.

    Actually, we need centroids. For sign vectors, a reasonable proxy is
    the signed distance sum: sum(ell_i * sign_i).
    This gives the correct relative order for generic ell.
    """
    # Use dot product of sign vector with ell as proxy for centroid evaluation
    def key(sv):
        return sum(l * s for l, s in zip(ell, sv))

    order = sorted(range(len(chambers)), key=lambda i: key(chambers[i]))
    return order

def edge_boundary(S_set, adj, n_vertices):
    """Count edges with exactly one endpoint in S."""
    count = 0
    counted = set()
    for v in S_set:
        for u in adj[v]:
            edge = (min(u,v), max(u,v))
            if edge not in counted:
                counted.add(edge)
                if (u in S_set) != (v in S_set):
                    count += 1
    # Also count edges from vertices not in S to vertices in S
    # Actually the above loop only visits neighbors of S, which covers all boundary edges
    return count

def compute_f(order, adj):
    """
    f(k) = deg(C_k) - 2 * |{C_j : j < k, C_j ~ C_k}|
    This is the boundary contribution when adding C_k to the initial segment.
    """
    f_values = []
    initial = set()
    for k, v in enumerate(order):
        deg_v = len(adj[v])
        neighbors_in_initial = len(adj[v] & initial)
        f_val = deg_v - 2 * neighbors_in_initial
        f_values.append(f_val)
        initial.add(v)
    return f_values

# ============================================================
# Part 2: Test the conjectures
# ============================================================

def test_arrangement(name, chambers, adj, dim, ell, max_subset_size=None):
    print(f"\n{'='*60}")
    print(f"Arrangement: {name}")
    print(f"Chambers: {len(chambers)}, Dimension: {dim}")
    print(f"{'='*60}")

    N = len(chambers)
    order = shelling_order(chambers, ell)

    print(f"\nShelling order (by index): {order}")
    print(f"Sign vectors in shelling order:")
    for k, v in enumerate(order):
        print(f"  k={k}: chamber {v} = {chambers[v]}, deg={len(adj[v])}")

    # Task 6: Compute f(k)
    f_vals = compute_f(order, adj)
    print(f"\nMonotonicity check: f(k) values:")
    for k, (v, f) in enumerate(zip(order, f_vals)):
        neighbors_before = len(adj[v] & set(order[:k]))
        print(f"  k={k}: f={f}  (deg={len(adj[v])}, neighbors_before={neighbors_before})")

    is_monotone = all(f_vals[i] <= f_vals[i+1] for i in range(len(f_vals)-1))
    print(f"\nf(k) non-decreasing? {is_monotone}")
    if not is_monotone:
        for i in range(len(f_vals)-1):
            if f_vals[i] > f_vals[i+1]:
                print(f"  VIOLATION at k={i}: f({i})={f_vals[i]} > f({i+1})={f_vals[i+1]}")

    # Task 2/3: Check all subsets
    if max_subset_size is None:
        max_subset_size = N

    exchange_failures = []
    initial_not_minimal = []

    for m in range(1, min(max_subset_size, N) + 1):
        initial_segment = set(order[:m])
        initial_boundary = edge_boundary(initial_segment, adj, N)

        min_boundary = float('inf')
        min_sets = []

        for subset in itertools.combinations(range(N), m):
            S = set(subset)
            bd = edge_boundary(S, adj, N)
            if bd < min_boundary:
                min_boundary = bd
                min_sets = [S]
            elif bd == min_boundary:
                min_sets.append(S)

        initial_is_min = (initial_boundary == min_boundary)

        if not initial_is_min:
            initial_not_minimal.append((m, initial_boundary, min_boundary))

        print(f"\nm={m}: initial_seg boundary={initial_boundary}, min boundary={min_boundary}, "
              f"initial is min? {initial_is_min}")

        # Check exchange lemma for non-initial-segment sets
        for subset in itertools.combinations(range(N), m):
            S = set(subset)
            if S == initial_segment:
                continue

            # Find position of each element in shelling order
            pos = {v: k for k, v in enumerate(order)}
            S_positions = sorted([pos[v] for v in S])

            # Check if S is an initial segment
            if S_positions == list(range(m)):
                continue  # This IS an initial segment (shouldn't happen since we checked)

            # Find first gap: smallest position NOT in S
            all_positions = set(S_positions)
            first_gap = None
            for p in range(N):
                if p not in all_positions:
                    first_gap = p
                    break

            # Find last present: largest position in S
            last_present = max(S_positions)

            if first_gap is not None and last_present > first_gap:
                C_i = order[first_gap]   # missing chamber to add
                C_j = order[last_present] # present chamber to remove

                S_prime = (S - {C_j}) | {C_i}
                bd_S = edge_boundary(S, adj, N)
                bd_S_prime = edge_boundary(S_prime, adj, N)

                if bd_S_prime > bd_S:
                    exchange_failures.append({
                        'm': m,
                        'S': S,
                        'S_prime': S_prime,
                        'bd_S': bd_S,
                        'bd_S_prime': bd_S_prime,
                        'swapped_out': C_j,
                        'swapped_in': C_i,
                        'pos_out': last_present,
                        'pos_in': first_gap,
                    })

    print(f"\n--- SUMMARY for {name} ---")
    if initial_not_minimal:
        print(f"INITIAL SEGMENT NOT MINIMAL for sizes: {initial_not_minimal}")
    else:
        print(f"Initial segment is ALWAYS minimal ✓")

    if exchange_failures:
        print(f"EXCHANGE LEMMA FAILURES: {len(exchange_failures)}")
        for fail in exchange_failures[:5]:  # show first 5
            print(f"  m={fail['m']}: S={fail['S']} -> S'={fail['S_prime']}")
            print(f"    boundary {fail['bd_S']} -> {fail['bd_S_prime']} (INCREASED)")
            print(f"    swapped out pos {fail['pos_out']} for pos {fail['pos_in']}")
    else:
        print(f"Exchange lemma ALWAYS holds ✓")

    print(f"f(k) monotone: {is_monotone}")

    return {
        'monotone': is_monotone,
        'f_vals': f_vals,
        'initial_always_min': len(initial_not_minimal) == 0,
        'exchange_always_holds': len(exchange_failures) == 0,
        'exchange_failures': exchange_failures,
        'initial_not_minimal': initial_not_minimal,
    }


# ============================================================
# Part 3: Run tests
# ============================================================

if __name__ == '__main__':
    from math import comb

    # --- Task 2: d=2, n=3 lines ---
    # y=0: (0,1,0), x=0: (1,0,0), x+y=1: (1,1,-1)
    lines_3 = [(0, 1, 0), (1, 0, 0), (1, 1, -1)]
    chambers_3 = enumerate_chambers_2d(lines_3)
    adj_3 = build_chamber_graph(chambers_3)
    ell_3 = (1.0, 0.7, 0.3)  # generic functional on sign space

    r3 = test_arrangement("3 lines in R² (d=2, n=3)", chambers_3, adj_3, 2, ell_3)

    # --- Task 3: d=2, n=4 lines ---
    # y=0, x=0, x+y=1, x-y=2
    lines_4 = [(0, 1, 0), (1, 0, 0), (1, 1, -1), (1, -1, -2)]
    chambers_4 = enumerate_chambers_2d(lines_4)
    adj_4 = build_chamber_graph(chambers_4)
    ell_4 = (1.0, 0.7, 0.3, 0.15)

    r4 = test_arrangement("4 lines in R² (d=2, n=4)", chambers_4, adj_4, 2, ell_4, max_subset_size=6)

    # --- Task 3: d=2, n=5 lines ---
    lines_5 = [(0, 1, 0), (1, 0, 0), (1, 1, -1), (1, -1, -2), (2, 1, -3)]
    chambers_5 = enumerate_chambers_2d(lines_5)
    adj_5 = build_chamber_graph(chambers_5)
    ell_5 = (1.0, 0.7, 0.3, 0.15, 0.08)

    r5 = test_arrangement("5 lines in R² (d=2, n=5)", chambers_5, adj_5, 2, ell_5, max_subset_size=6)

    # --- Task 4: d=3, n=4 planes ---
    # z=0, y=0, x=0, x+y+z=1
    planes_4 = [(0,0,1,0), (0,1,0,0), (1,0,0,0), (1,1,1,-1)]
    chambers_3d = enumerate_chambers_3d(planes_4)
    adj_3d = build_chamber_graph(chambers_3d)
    ell_3d = (1.0, 0.7, 0.3, 0.15)

    r3d = test_arrangement("4 planes in R³ (d=3, n=4)", chambers_3d, adj_3d, 3, ell_3d)

    # --- d=3, n=5 planes ---
    planes_5 = [(0,0,1,0), (0,1,0,0), (1,0,0,0), (1,1,1,-1), (1,-1,2,-3)]
    chambers_3d_5 = enumerate_chambers_3d(planes_5)
    adj_3d_5 = build_chamber_graph(chambers_3d_5)
    ell_3d_5 = (1.0, 0.7, 0.3, 0.15, 0.08)

    r3d5 = test_arrangement("5 planes in R³ (d=3, n=5)", chambers_3d_5, adj_3d_5, 3, ell_3d_5, max_subset_size=8)

    # --- Overall summary ---
    print("\n" + "="*60)
    print("OVERALL SUMMARY")
    print("="*60)
    results = [
        ("3 lines, d=2", r3),
        ("4 lines, d=2", r4),
        ("5 lines, d=2", r5),
        ("4 planes, d=3", r3d),
        ("5 planes, d=3", r3d5),
    ]

    for name, r in results:
        print(f"\n{name}:")
        print(f"  Initial segment always minimal: {r['initial_always_min']}")
        print(f"  Exchange lemma always holds: {r['exchange_always_holds']}")
        print(f"  f(k) monotone non-decreasing: {r['monotone']}")
        print(f"  f(k) values: {r['f_vals']}")
        if not r['exchange_always_holds']:
            print(f"  Exchange failures: {len(r['exchange_failures'])}")
