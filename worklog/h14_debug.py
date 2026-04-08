"""
Debug: why does Phase 1 keep all k^2 edges?

Hypothesis: every edge in timestamp order always creates at least one new pair,
because the source vertex a_i can always reach itself, and b_j might not be
reachable from a_i yet.

Let's trace a small example.
"""

import random
from collections import defaultdict
import heapq

def random_matrix(k):
    vals = list(range(1, k * k + 1))
    random.shuffle(vals)
    return [vals[i * k:(i + 1) * k] for i in range(k)]

def matrix_to_edges(k, M):
    return [(i, k + j, M[i][j]) for i in range(k) for j in range(k)]

def is_fully_reachable(k, edges):
    adj = defaultdict(list)
    for (a, b, t) in edges:
        adj[a].append((b, t))
        adj[b].append((a, t))
    n = 2 * k
    for s in range(n):
        best = {s: -1}
        queue = [(-1, s)]
        while queue:
            t_arr, u = heapq.heappop(queue)
            if t_arr > best.get(u, float('inf')):
                continue
            for (v, t_edge) in adj[u]:
                if t_edge >= t_arr:
                    if t_edge < best.get(v, float('inf')):
                        best[v] = t_edge
                        heapq.heappush(queue, (t_edge, v))
        if len(best) < n:
            return False
    return True

random.seed(42)
k = 3

# Find a fully reachable matrix
while True:
    M = random_matrix(k)
    edges = matrix_to_edges(k, M)
    if is_fully_reachable(k, edges):
        break

print(f"k={k}, Matrix:")
for row in M:
    print(f"  {row}")

n = 2 * k
INF = float('inf')
reach = [[INF] * n for _ in range(n)]
for i in range(n):
    reach[i][i] = -1

edges_sorted = sorted(edges, key=lambda e: e[2])

for (a, b, t) in edges_sorted:
    S = [u for u in range(n) if reach[u][a] <= t]
    T = [v for v in range(n) if reach[b][v] < INF]

    new_pairs = []
    for u in S:
        for v in T:
            if reach[u][v] == INF:
                new_pairs.append((u, v))

    print(f"\nEdge (a{a}, b{b-k}) at t={t}")
    print(f"  S (can reach a{a} by t={t}): {S}")
    print(f"  T (reachable from b{b-k}): {T}")
    print(f"  New pairs: {new_pairs}")

    if new_pairs:
        # Build adj from kept edges + this one
        # For simplicity, just add the direct connection for now
        # The issue is: T only has {b} initially since reach[b][v] uses current spanner only
        # And a_i is always in S (reach[a][a] = -1 <= t)
        # So (a_i, b_j) is always a new pair if reach[a_i][b_j] == INF

        # Update: just set the direct pairs
        adj_kept = defaultdict(list)
        # We need all previously kept edges... let me track them
        pass

# The insight is clear: reach[b][v] starts empty (only b itself),
# and reach[a][a] = -1 always, so (a, b) is ALWAYS a new pair
# on the first edge from a to any b.
#
# More importantly: EVERY a_i->b_j pair is new because we process
# edges in order, and the bipartite structure means a_i has never
# directly connected to b_j before.

print("\n" + "=" * 60)
print("DIAGNOSIS: In a bipartite graph with all-distinct timestamps,")
print("every edge (a_i, b_j) at its unique timestamp creates the")
print("NEW pair (a_i, b_j) because there is no other edge between")
print("exactly a_i and b_j. Thus Phase 1 keeps ALL k^2 edges.")
print()
print("The forward incremental algorithm CANNOT eliminate any edge")
print("in Phase 1 for temporal cliques with all-distinct timestamps.")
print("This is because each (a_i, b_j) is the ONLY direct edge")
print("between that specific pair, so the pair a_i->b_j can only")
print("be established by keeping that edge.")
print()
print("Wait — that's wrong. a_i CAN reach b_j via a_i -> b_k -> a_m -> b_j")
print("if those edges have non-decreasing timestamps. Let me check...")

# Actually let's check: when we process edge (a_i, b_j) at time t,
# is it possible that a_i already reaches b_j via kept edges?
print()

random.seed(42)
k = 4
while True:
    M = random_matrix(k)
    edges = matrix_to_edges(k, M)
    if is_fully_reachable(k, edges):
        break

print(f"\nk={k}, checking if any edge is skippable...")
n = 2 * k
reach = [[INF] * n for _ in range(n)]
for i in range(n):
    reach[i][i] = -1

edges_sorted = sorted(edges, key=lambda e: e[2])
kept = []
skipped = 0

for (a, b, t) in edges_sorted:
    # Recompute reach from scratch using kept edges + possibly this one
    # Check if a can already reach b
    S = [u for u in range(n) if reach[u][a] <= t]
    T = [v for v in range(n) if reach[b][v] < INF]

    new_pairs = [(u, v) for u in S for v in T if reach[u][v] == INF]

    if not new_pairs:
        skipped += 1
        print(f"  SKIPPED: ({a}, {b}) at t={t}")
        continue

    kept.append((a, b, t))

    # Update reach matrix properly
    # Build adj from all kept edges
    adj = defaultdict(list)
    for (ea, eb, et) in kept:
        adj[ea].append((eb, et))
        adj[eb].append((ea, et))

    # BFS from b at time t
    best_b = {b: t}
    queue = [(t, b)]
    while queue:
        t_arr, node = heapq.heappop(queue)
        if t_arr > best_b.get(node, INF):
            continue
        for (nxt, t_edge) in adj[node]:
            if t_edge >= t_arr:
                if t_edge < best_b.get(nxt, INF):
                    best_b[nxt] = t_edge
                    heapq.heappush(queue, (t_edge, nxt))

    for u in S:
        for v, arr_v in best_b.items():
            reach[u][v] = min(reach[u][v], arr_v)

print(f"\nKept: {len(kept)}, Skipped: {skipped}")
print(f"k^2 = {k*k}")

# The problem is clear: reach[b][v] only reflects current spanner,
# but b_j only has edges to a-vertices, and those edges may not
# have been kept yet. So reach[b_j][v] is very sparse initially.
#
# KEY ISSUE: The reach matrix correctly tracks what's reachable,
# but the bipartite clique has SO MANY unique pairs that nearly
# every edge creates some new pair.
#
# Let's count: for the LAST edge processed (highest timestamp),
# how many new pairs does it create?

print(f"\nLast edge kept: {kept[-1]}")
# Check reach matrix at the end - how many INF entries?
inf_count = sum(1 for u in range(n) for v in range(n) if u != v and reach[u][v] == INF)
print(f"INF entries remaining: {inf_count} out of {n*(n-1)}")
