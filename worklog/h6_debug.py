#!/usr/bin/env python3
"""Debug: why does SM(k) online greedy add ALL edges? What pairs are missing?"""

def sm_matrix(k):
    M = [[0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            M[i][j] = i*k + ((i+j) % k) + 1
    return M

def compute_reachable_pairs(spanner_edges, k):
    n = 2 * k
    sorted_edges = sorted(spanner_edges, key=lambda e: e[0])
    from collections import defaultdict
    time_groups = defaultdict(list)
    for (t, ai, bj) in sorted_edges:
        time_groups[t].append((ai, k + bj))
    times = sorted(time_groups.keys())
    reachable = set()
    for src in range(n):
        active = {src}
        for t in times:
            changed = True
            while changed:
                changed = False
                for (u, v) in time_groups[t]:
                    if u in active and v not in active:
                        active.add(v)
                        changed = True
                    if v in active and u not in active:
                        active.add(u)
                        changed = True
        for dst in active:
            if dst != src:
                reachable.add((src, dst))
    return reachable

# Check k=3: what pairs are unreachable even with ALL edges?
k = 3
n = 2*k
M = sm_matrix(k)
print(f"SM({k}) matrix:")
for row in M:
    print(f"  {row}")

all_edges = [(M[i][j], i, j) for i in range(k) for j in range(k)]
reachable = compute_reachable_pairs(all_edges, k)
total = n*(n-1)
print(f"\nWith ALL edges: {len(reachable)}/{total} pairs reachable")

# Which pairs are missing?
missing = []
for u in range(n):
    for v in range(n):
        if u != v and (u,v) not in reachable:
            u_label = f"a{u}" if u < k else f"b{u-k}"
            v_label = f"a{v}" if v < k else f"b{v-k}"
            missing.append((u_label, v_label))

print(f"Missing pairs: {missing}")

# The issue might be: temporal journeys require STRICTLY increasing timestamps?
# Let me re-check: the conjecture says "non-decreasing" but SM has all distinct timestamps
# so non-decreasing = strictly increasing in this case.
#
# Wait - the issue is that A-A and B-B pairs require going through intermediaries.
# a_0 -> b_j (time t1) -> a_i (time t2 > t1) -> b_j' (time t3 > t2)
# For a_0 to reach a_1, we need b_j such that edge(a_0, b_j) has time < edge(a_1, b_j').
# But we also need edge(a_1, b_j') to come AFTER edge(b_j, a_1)... wait, b_j connects to a_1
# only if there's an edge. All edges are A-B. So a_0 -> b_j at time t1, then b_j -> a_1 at time t2 > t1.
# This requires M[0][j] < M[1][j] for some j.

print(f"\nChecking A-A reachability for k={k}:")
for a1 in range(k):
    for a2 in range(k):
        if a1 != a2:
            # a1 can reach a2 if exists j: M[a1][j] < M[a2][j]
            # (1-hop through b_j)
            ways = []
            for j in range(k):
                if M[a1][j] < M[a2][j]:
                    ways.append(f"via b{j}: t={M[a1][j]}<{M[a2][j]}")
            if ways:
                print(f"  a{a1}->a{a2}: {ways[0]}")
            else:
                print(f"  a{a1}->a{a2}: NO direct 2-hop path")

print(f"\nChecking B-B reachability for k={k}:")
for b1 in range(k):
    for b2 in range(k):
        if b1 != b2:
            ways = []
            for i in range(k):
                if M[i][b1] < M[i][b2]:
                    ways.append(f"via a{i}: t={M[i][b1]}<{M[i][b2]}")
            if ways:
                print(f"  b{b1}->b{b2}: {ways[0]}")
            else:
                print(f"  b{b1}->b{b2}: NO direct 2-hop path")

# Now the KEY question: does the greedy check reachability correctly?
# A "new reachable pair" means adding this edge opens a path that didn't exist before.
# But our greedy adds EVERY edge. That means each edge creates at least one new pair.
# Let's verify: is the reachability computation correct?

print(f"\n--- Verifying reachability computation step by step for k=3 ---")
all_edges_sorted = sorted(all_edges, key=lambda e: e[0])
print("Edges in timestamp order:")
for t, ai, bj in all_edges_sorted:
    print(f"  t={t}: a{ai}-b{bj}")

# Manual check: after first edge only, what's reachable?
first = [all_edges_sorted[0]]
r1 = compute_reachable_pairs(first, k)
print(f"\nAfter edge 1 (t={first[0][0]}, a{first[0][1]}-b{first[0][2]}):")
for u, v in sorted(r1):
    u_l = f"a{u}" if u < k else f"b{u-k}"
    v_l = f"a{v}" if v < k else f"b{v-k}"
    print(f"  {u_l} -> {v_l}")

# After first 2 edges
first2 = all_edges_sorted[:2]
r2 = compute_reachable_pairs(first2, k)
print(f"\nAfter edges 1-2:")
for u, v in sorted(r2):
    u_l = f"a{u}" if u < k else f"b{u-k}"
    v_l = f"a{v}" if v < k else f"b{v-k}"
    print(f"  {u_l} -> {v_l}")

new = r2 - r1
print(f"  New pairs: {len(new)}")
for u, v in sorted(new):
    u_l = f"a{u}" if u < k else f"b{u-k}"
    v_l = f"a{v}" if v < k else f"b{v-k}"
    print(f"    {u_l} -> {v_l}")

# Check edge counts: is online=k² because SM never creates redundant reachability?
# The overshoot pattern is 1, 4, 9, 16, 25, 36 = (k-2)² for k>=3
# Actually: k=3:1, k=4:4, k=5:9, k=6:16, k=7:25, k=8:36
# That's (k-2)²! So online=k², offline=4k-4, gap=(k-2)²
# Verify: k²-(4k-4) = k²-4k+4 = (k-2)²  ✓

print(f"\n--- Gap analysis ---")
for k in [3,4,5,6,7,8]:
    gap = k*k - (4*k-4)
    print(f"k={k}: online=k²={k*k}, offline=4k-4={4*k-4}, gap={gap} = (k-2)²={(k-2)**2}")
