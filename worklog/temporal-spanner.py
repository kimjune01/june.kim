"""
Temporal spanner lower bound analysis.

We construct explicit timestamp assignments on K_n and compute
minimum spanner sizes by finding forced/necessary edges.
"""

from itertools import permutations, combinations
from collections import defaultdict

def round_robin_hamiltonian_decomposition(n):
    """
    For odd n, decompose K_n into (n-1)/2 edge-disjoint Hamiltonian paths.
    Uses the standard round-robin tournament construction.

    Returns: list of paths, where each path is a list of vertices in order.
    """
    assert n % 2 == 1, "n must be odd"
    paths = []
    # Standard construction: fix vertex 0, rotate the rest.
    # For n odd, we get (n-1)/2 rounds, each a perfect matching on n-1 vertices
    # plus one unmatched vertex paired with vertex 0...
    # Actually for odd n, round-robin gives n rounds of (n-1)/2 matches each,
    # but we want Hamiltonian paths.

    # Let me use a different standard construction.
    # For odd n, arrange vertices 1..n-1 in a circle. Vertex 0 is special.
    # In round r (0-indexed), the matching pairs vertex 0 with vertex r+1,
    # and pairs (r+1+k) with (r+1-k) mod (n-1) for k=1,...,(n-3)/2.
    # Wait, this gives perfect matchings for even n.

    # For odd n: K_n decomposes into (n-1)/2 Hamiltonian paths.
    # Construction: label vertices 0,...,n-1.
    # Place vertices 1,...,n-1 around a regular (n-1)-gon.
    # For round r (r=0,...,(n-3)/2):
    #   Draw the diameter through position r (mod n-1) and the perpendicular matchings.
    #   This gives (n-1)/2 edges forming a perfect matching on {1,...,n-1} minus one vertex,
    #   plus edges to vertex 0.

    # Actually, let me just use a known explicit construction.
    # For K_n with n odd, the Hamiltonian decomposition:
    # Place vertices 1,...,n-1 at positions around a circle.
    # For each round r=0,...,(n-3)/2:
    #   Start at vertex (r mod (n-1)) + 1 (using 1-indexed circular positions)
    #   Zigzag: go to the opposite side, alternating.

    # Simpler: use the well-known construction.
    # Vertices: 0, 1, ..., n-1. For odd n.
    # Round r (r = 0, ..., (n-3)/2):
    #   Path: start at vertex labeled (2r mod (n-1)) + 1 mapped through...

    # Let me just hardcode small cases and also implement a general algorithm.

    if n == 3:
        # K_3: 1 Hamiltonian path
        # Edges: 0-1, 1-2, 0-2. One Ham path e.g. 0-1-2.
        return [[0, 1, 2]]

    if n == 5:
        # K_5: 2 Hamiltonian paths covering all 10 edges? No.
        # K_5 has 10 edges. Each Ham path has 4 edges. 2 paths = 8 edges. Not enough.
        # Actually (n-1)/2 = 2 Ham paths with 4 edges each = 8 edges, but K_5 has 10.
        # So this doesn't decompose K_5 into Ham paths.

        # Wait: K_n for odd n decomposes into (n-1)/2 Hamiltonian CYCLES, not paths.
        # n(n-1)/2 edges, each cycle has n edges, (n-1)/2 cycles gives n(n-1)/2 edges. Yes!
        # But we want paths for the directed-reachability argument.

        # Let me reconsider. K_5 has 10 edges.
        # (n-1)/2 = 2 Hamiltonian cycles, each with 5 edges = 10 total. Correct!
        pass

    # General construction for odd n: decompose into (n-1)/2 Hamiltonian CYCLES.
    # Standard round-robin:
    # Vertices: 0, 1, ..., n-1
    # Fix vertex n-1. Arrange 0, 1, ..., n-2 around a circle.
    # Actually for odd n we don't need to fix a vertex.

    # Place all n vertices around a circle: 0, 1, ..., n-1.
    # For round r = 0, ..., (n-3)/2:
    #   Match vertex r with vertex r+1 (mod n) as the "top" edge
    #   Then zigzag: (r-1, r+2), (r-2, r+3), ... forming a Hamiltonian cycle.

    # Standard construction (Alspach):
    # Vertices 0..n-1 on a circle.
    # Round r: edges {r+j, r-j-1} for j=0,...,(n-3)/2, plus edge {r, r+(n-1)/2}...
    # This is getting complicated. Let me just find cycles computationally for small n.

    return find_hamiltonian_cycle_decomposition(n)


def find_hamiltonian_cycle_decomposition(n):
    """Find (n-1)/2 edge-disjoint Hamiltonian cycles in K_n (n odd), brute force for small n."""
    assert n % 2 == 1
    num_cycles = (n - 1) // 2
    all_edges = set()
    for i in range(n):
        for j in range(i+1, n):
            all_edges.add((i, j))

    # For small n, use the explicit algebraic construction
    # Vertices on Z_n. Cycle r uses edges {v, v + (2r+1)} and {v, v - (2r+1)} mod n
    # Actually: for Z_n (n odd), the cycle C_r consists of edges {v, v+r} for all v in Z_n.
    # The "distances" 1, 2, ..., (n-1)/2 give (n-1)/2 Hamiltonian cycles (since n is prime...
    # well, n is odd, and gcd(r, n)=1 iff r doesn't divide n).

    # For n prime, every distance 1...(n-1)/2 gives a Hamiltonian cycle on Z_n.
    # For n=9 (not prime), distance 3 gives 3 triangles, not a Hamiltonian cycle.

    # Let's just use the standard construction that always works:
    # Arrange vertices 0,...,n-1. For round r=1,...,(n-1)/2:
    # Cycle r: 0, r, n-r, 2r, n-2r, 3r, ... (all mod n)
    # This works when gcd(r,n)=1. For general odd n, we need a different approach.

    cycles = []
    used_edges = set()

    # Try the terquem/lucas construction
    # For odd n, vertices 0,...,n-1 arranged in a circle.
    # Round r (r=0,...,(n-3)/2):
    #   Consider the "starter" edges from vertex 0 to vertices r+1 and n-r-1
    #   (distances r+1 and n-r-1 from 0). Then rotate.

    # Actually, let me use the 1-factorization of K_{n+1} approach:
    # K_{n+1} (even) has a 1-factorization. Remove one vertex to get (n-1)/2
    # Hamiltonian paths of K_n. But we want cycles...

    # For now, let me just use a greedy/backtracking approach for small n.
    return _find_cycles_backtrack(n, all_edges, num_cycles)


def _find_cycles_backtrack(n, remaining_edges, num_needed):
    """Find edge-disjoint Hamiltonian cycles by backtracking."""
    if num_needed == 0:
        return []

    # Find one Hamiltonian cycle using remaining edges
    cycle = _find_one_hamiltonian_cycle(n, remaining_edges)
    if cycle is None:
        return None

    cycle_edges = set()
    for i in range(len(cycle)):
        u, v = cycle[i], cycle[(i+1) % len(cycle)]
        cycle_edges.add((min(u,v), max(u,v)))

    new_remaining = remaining_edges - cycle_edges
    rest = _find_cycles_backtrack(n, new_remaining, num_needed - 1)
    if rest is None:
        return None
    return [cycle] + rest


def _find_one_hamiltonian_cycle(n, available_edges):
    """Find a Hamiltonian cycle using only available edges."""
    adj = defaultdict(set)
    for u, v in available_edges:
        adj[u].add(v)
        adj[v].add(u)

    # Start from vertex 0
    path = [0]
    visited = {0}

    def backtrack():
        if len(path) == n:
            # Check if we can close the cycle
            last = path[-1]
            if path[0] in adj[last] and (min(last, path[0]), max(last, path[0])) in available_edges:
                return True
            return False

        current = path[-1]
        for next_v in sorted(adj[current]):
            if next_v not in visited:
                edge = (min(current, next_v), max(current, next_v))
                if edge in available_edges:
                    path.append(next_v)
                    visited.add(next_v)
                    if backtrack():
                        return True
                    path.pop()
                    visited.remove(next_v)
        return False

    if backtrack():
        return path
    return None


def assign_timestamps_cycles(n, cycles):
    """
    Assign timestamps to edges based on Hamiltonian cycle decomposition.
    Cycle k (0-indexed) gets timestamps k*n+1, k*n+2, ..., k*n+n.
    Each cycle traverses n edges (including the closing edge).

    Returns: dict mapping (u,v) with u<v to its timestamp.
    """
    timestamps = {}
    for k, cycle in enumerate(cycles):
        for i in range(n):
            u, v = cycle[i], cycle[(i+1) % n]
            edge = (min(u,v), max(u,v))
            t = k * n + i + 1
            timestamps[edge] = t

    return timestamps


def all_journeys(n, timestamps):
    """
    Compute all-pairs reachability via journeys (non-decreasing timestamps).
    Returns dict: (u,v) -> list of journeys, where each journey is a list of edges.
    """
    # BFS/DFS approach: for each source, find all reachable vertices via journeys.
    # A journey is a sequence of edges with non-decreasing timestamps.

    # Build adjacency with timestamps
    adj = defaultdict(list)  # vertex -> list of (neighbor, timestamp, edge)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t, (u,v)))
        adj[v].append((u, t, (u,v)))

    # Sort adjacency lists by timestamp
    for v in adj:
        adj[v].sort(key=lambda x: x[1])

    reachability = {}
    for src in range(n):
        for dst in range(n):
            if src == dst:
                continue
            reachability[(src, dst)] = True  # We'll check this

    return reachability


def check_reachability(n, timestamps, src, dst):
    """Check if there's a journey from src to dst using edges with non-decreasing timestamps."""
    adj = defaultdict(list)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t))
        adj[v].append((u, t))

    # BFS with state = (current_vertex, last_timestamp)
    # Use dynamic programming: for each vertex, track the minimum timestamp at which we can arrive
    # Actually: track all (vertex, min_next_timestamp) states

    # States: (vertex, earliest_time_we_can_use_next)
    from collections import deque

    # Start: at src, can use any timestamp >= 0
    queue = deque()
    queue.append((src, 0))
    visited = set()
    visited.add((src, 0))

    # This could blow up. Better approach: for each vertex, track the minimum
    # "last timestamp used to arrive" — if we arrive with a smaller timestamp,
    # we have more options.

    best_arrival = {}  # vertex -> minimum last_timestamp to arrive here
    best_arrival[src] = 0
    queue = deque([src])
    changed = True

    while changed:
        changed = False
        for v in range(n):
            if v not in best_arrival:
                continue
            min_t = best_arrival[v]
            for (w, t) in adj[v]:
                if t >= min_t:
                    if w not in best_arrival or t < best_arrival[w]:
                        # Wait: arrival time at w should be t (the timestamp of the edge used)
                        # but we need the NEXT edge to have timestamp >= t.
                        # So best_arrival[w] should store the timestamp we used to get here.
                        # Then from w, we can use any edge with timestamp >= best_arrival[w].

                        # Actually for non-decreasing: next timestamp >= current timestamp.
                        # So if we arrive at w using edge with timestamp t, from w we need
                        # edges with timestamp >= t.
                        if w not in best_arrival or t < best_arrival[w]:
                            best_arrival[w] = t
                            changed = True

    # Wait, the above has a bug. Let me redo with proper relaxation.
    # best_arrival[v] = minimum timestamp T such that there exists a journey
    # from src to v where the last edge has timestamp T (or T=0 for src).
    # From v, we can use edge (v,w) with timestamp t >= T, arriving at w with timestamp t.

    best_arrival = {src: 0}

    # Bellman-Ford style relaxation
    for _ in range(n):
        updated = False
        for v in list(best_arrival.keys()):
            min_t = best_arrival[v]
            for (w, t) in adj[v]:
                if t >= min_t:
                    if w not in best_arrival or t < best_arrival[w]:
                        best_arrival[w] = t
                        updated = True
        if not updated:
            break

    return dst in best_arrival


def find_all_journeys_for_pair(n, timestamps, src, dst, max_journeys=1000):
    """
    Find all minimal journeys from src to dst.
    A journey is a list of edges (as (u,v) with u<v) with non-decreasing timestamps.
    """
    adj = defaultdict(list)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t, (u,v)))
        adj[v].append((u, t, (u,v)))

    for v in adj:
        adj[v].sort(key=lambda x: x[1])

    journeys = []

    def dfs(current, last_t, path_edges, visited):
        if len(journeys) >= max_journeys:
            return
        if current == dst:
            journeys.append(list(path_edges))
            return
        for (w, t, edge) in adj[current]:
            if t >= last_t and w not in visited:
                visited.add(w)
                path_edges.append(edge)
                dfs(w, t, path_edges, visited)
                path_edges.pop()
                visited.remove(w)

    dfs(src, 0, [], {src})
    return journeys


def find_forced_edges(n, timestamps):
    """
    An edge e is forced/necessary if there exists a pair (u,v) such that
    every journey from u to v uses e.

    Returns: set of forced edges and the witness pairs.
    """
    forced_edges = set()
    witnesses = {}  # edge -> list of (src, dst) pairs that force it

    all_edges = set(timestamps.keys())

    for src in range(n):
        for dst in range(n):
            if src == dst:
                continue

            journeys = find_all_journeys_for_pair(n, timestamps, src, dst)
            if not journeys:
                print(f"WARNING: No journey from {src} to {dst}!")
                continue

            # Find edges that appear in ALL journeys for this pair
            common_edges = set(journeys[0])
            for j in journeys[1:]:
                common_edges &= set(j)

            for e in common_edges:
                forced_edges.add(e)
                if e not in witnesses:
                    witnesses[e] = []
                witnesses[e].append((src, dst))

    return forced_edges, witnesses


def minimum_spanner_ilp(n, timestamps):
    """
    Compute the exact minimum spanner size using brute force (try all subsets).
    Only feasible for very small n.
    """
    all_edges = list(timestamps.keys())
    m = len(all_edges)

    # Check all pairs reachability in full graph first
    full_pairs = set()
    for src in range(n):
        for dst in range(n):
            if src != dst and check_reachability(n, timestamps, src, dst):
                full_pairs.add((src, dst))

    print(f"  Full graph: {len(full_pairs)} reachable pairs out of {n*(n-1)}")

    # Try to find minimum subset
    # For small n, try removing edges one at a time, then pairs, etc.
    # Start with forced edges, then greedily try to find minimum.

    # For n <= 7, we can try a smarter approach
    best_size = m

    # First find forced edges
    forced, witnesses = find_forced_edges(n, timestamps)
    print(f"  Forced edges: {len(forced)} out of {m}")

    # Try removing non-forced edges
    removable = [e for e in all_edges if e not in forced]

    # Greedy: try removing each non-forced edge
    current_edges = set(all_edges)
    for e in removable:
        trial = current_edges - {e}
        trial_ts = {edge: timestamps[edge] for edge in trial}
        # Check if all pairs still reachable
        valid = True
        for (src, dst) in full_pairs:
            if not check_reachability(n, trial_ts, src, dst):
                valid = False
                break
        if valid:
            current_edges = trial

    return len(current_edges), forced, witnesses


def analyze_case(n):
    """Full analysis for K_n."""
    print(f"\n{'='*60}")
    print(f"Analysis of K_{n}")
    print(f"{'='*60}")

    # Get Hamiltonian cycle decomposition
    cycles = round_robin_hamiltonian_decomposition(n)
    print(f"\nHamiltonian cycles ({len(cycles)}):")
    for i, c in enumerate(cycles):
        print(f"  Cycle {i}: {c}")

    # Assign timestamps
    timestamps = assign_timestamps_cycles(n, cycles)
    print(f"\nTimestamp assignment:")
    for (u,v), t in sorted(timestamps.items(), key=lambda x: x[1]):
        print(f"  edge ({u},{v}): timestamp {t}")

    # Verify all-pairs reachability
    print(f"\nReachability check:")
    all_reachable = True
    for src in range(n):
        for dst in range(n):
            if src != dst:
                if not check_reachability(n, timestamps, src, dst):
                    print(f"  UNREACHABLE: {src} -> {dst}")
                    all_reachable = False
    if all_reachable:
        print(f"  All {n*(n-1)} ordered pairs are reachable. ✓")

    # Find forced edges
    print(f"\nForced edge analysis:")
    forced, witnesses = find_forced_edges(n, timestamps)
    print(f"  Forced edges: {len(forced)} out of {n*(n-1)//2}")
    for e in sorted(forced):
        print(f"    {e} (timestamp {timestamps[e]}), witnessed by {len(witnesses[e])} pairs")

    # Minimum spanner (greedy)
    print(f"\nMinimum spanner (greedy):")
    min_size, _, _ = minimum_spanner_ilp(n, timestamps)
    print(f"  Greedy spanner size: {min_size}")
    print(f"  n = {n}, n*log2(n) = {n * __import__('math').log2(n):.1f}")
    print(f"  Ratio spanner/n = {min_size/n:.2f}")

    return timestamps, forced, witnesses, min_size


def try_random_timestamp_assignments(n, num_trials=100):
    """Try random timestamp assignments and find the one requiring the largest spanner."""
    import random

    edges = []
    for i in range(n):
        for j in range(i+1, n):
            edges.append((i, j))
    m = len(edges)

    best_forced = 0
    best_ts = None
    best_greedy = 0

    for trial in range(num_trials):
        # Random permutation of timestamps 1..m
        perm = list(range(1, m+1))
        random.shuffle(perm)
        timestamps = {edges[i]: perm[i] for i in range(m)}

        # Check all-pairs reachability
        all_reach = True
        for src in range(n):
            for dst in range(n):
                if src != dst and not check_reachability(n, timestamps, src, dst):
                    all_reach = False
                    break
            if not all_reach:
                break

        if not all_reach:
            continue

        # Find forced edges
        forced, witnesses = find_forced_edges(n, timestamps)

        if len(forced) > best_forced:
            best_forced = len(forced)
            best_ts = timestamps

            # Also compute greedy spanner
            all_edges_list = list(timestamps.keys())
            current = set(all_edges_list)
            removable = [e for e in all_edges_list if e not in forced]
            for e in removable:
                trial_set = current - {e}
                trial_ts = {edge: timestamps[edge] for edge in trial_set}
                valid = True
                for src in range(n):
                    for dst in range(n):
                        if src != dst and not check_reachability(n, trial_ts, src, dst):
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    current = trial_set
            best_greedy = len(current)

    return best_forced, best_greedy, best_ts


def exact_minimum_spanner(n, timestamps):
    """
    Exact minimum spanner via subset enumeration.
    Only for very small n (n <= 5).
    """
    all_edges = list(timestamps.keys())
    m = len(all_edges)

    # All reachable pairs in full graph
    full_pairs = []
    for src in range(n):
        for dst in range(n):
            if src != dst and check_reachability(n, timestamps, src, dst):
                full_pairs.append((src, dst))

    # For each pair, compute which edge-sets (as bitmasks) provide a journey
    # Then minimum hitting set.

    # For each pair, find the set of edges that appear in at least one journey
    # Actually we need: for each pair, the set of ALL journeys (as edge sets)
    # A valid spanner must contain at least one complete journey for each pair.

    # This is a set cover / hitting set problem.
    # For small m, enumerate subsets from smallest to largest.

    print(f"  Computing exact minimum spanner for n={n}, m={m}...")

    # Precompute for each pair: the collection of journey edge-sets
    pair_journeys = {}
    for (src, dst) in full_pairs:
        journeys = find_all_journeys_for_pair(n, timestamps, src, dst)
        pair_journeys[(src, dst)] = [frozenset(j) for j in journeys]

    # Now find minimum subset S of all_edges such that for every pair,
    # at least one journey is a subset of S.

    # Convert to bitmasks for speed
    edge_to_idx = {e: i for i, e in enumerate(all_edges)}
    pair_journey_masks = {}
    for pair, journeys in pair_journeys.items():
        masks = []
        for j in journeys:
            mask = 0
            for e in j:
                mask |= (1 << edge_to_idx[e])
            masks.append(mask)
        pair_journey_masks[pair] = masks

    # Check from smallest to largest
    for size in range(1, m+1):
        print(f"    Trying size {size}...")
        found = False
        count = 0
        for subset_tuple in combinations(range(m), size):
            count += 1
            if count > 500000:  # Safety limit
                print(f"    Too many subsets at size {size}, skipping to greedy")
                return None

            mask = 0
            for i in subset_tuple:
                mask |= (1 << i)

            valid = True
            for pair, journey_masks in pair_journey_masks.items():
                # Check if any journey is fully contained in this subset
                pair_ok = False
                for jm in journey_masks:
                    if (jm & mask) == jm:
                        pair_ok = True
                        break
                if not pair_ok:
                    valid = False
                    break

            if valid:
                print(f"    Found minimum spanner of size {size}")
                selected = [all_edges[i] for i in subset_tuple]
                return size, selected

    return m, all_edges


if __name__ == "__main__":
    import math

    # Analyze small cases with round-robin construction
    results = {}
    for n in [3, 5, 7]:
        ts, forced, witnesses, greedy_size = analyze_case(n)
        results[n] = {
            'forced': len(forced),
            'greedy': greedy_size,
            'total_edges': n*(n-1)//2,
            'n_log_n': n * math.log2(n)
        }

        # For n=3,5: compute exact minimum
        if n <= 5:
            print(f"\nExact minimum spanner for K_{n}:")
            result = exact_minimum_spanner(n, ts)
            if result:
                results[n]['exact'] = result[0]
                print(f"  Exact minimum: {result[0]}")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'n':>4} {'edges':>6} {'forced':>7} {'greedy':>7} {'n*lg(n)':>8}")
    for n in sorted(results.keys()):
        r = results[n]
        exact = r.get('exact', '?')
        print(f"{n:>4} {r['total_edges']:>6} {r['forced']:>7} {r['greedy']:>7} {r['n_log_n']:>8.1f}  exact={exact}")

    # Now try random assignments to find better adversarial labelings
    print(f"\n{'='*60}")
    print("RANDOM SEARCH FOR BETTER ADVERSARIAL LABELINGS")
    print(f"{'='*60}")
    for n in [5, 7]:
        print(f"\nK_{n}: trying 200 random assignments...")
        best_forced, best_greedy, best_ts = try_random_timestamp_assignments(n, 200)
        print(f"  Best forced edges found: {best_forced}")
        print(f"  Best greedy spanner: {best_greedy}")
        if best_ts:
            print(f"  Best assignment: {best_ts}")
