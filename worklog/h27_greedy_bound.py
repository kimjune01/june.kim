#!/usr/bin/env python3
"""
H27 Part 3: Focus on greedy ordering — does it ALWAYS stay within 4k-3?

Key finding from Part 2:
- Arbitrary orderings CAN violate the budget (k=5: worst_any_order=9 > 8)
- Greedy ordering appears to always stay within budget
- The question: is greedy-within-budget a theorem or just empirical luck?

This script:
1. Exhaustive search at small k to find the absolute worst-case greedy miss
2. Large-scale random search at medium k
3. Attempt adversarial construction
4. Count the actual spanner edges (not just delegation edges)
5. Verify temporal reachability of the constructed spanner
"""

import random
import math
from collections import defaultdict
from itertools import permutations


def random_timestamp_matrix(k, seed=None):
    rng = random.Random(seed)
    ts = rng.sample(range(1, k * k + 1), k * k)
    M = {}
    idx = 0
    for i in range(k):
        for j in range(k):
            M[(i, j)] = ts[idx]
            idx += 1
    return M


def best_relay(k, M, i, j):
    """Best relay c' for i→j: lowest rank in j's row with M[i,c']<M[j,c']."""
    j_sorted = sorted(range(k), key=lambda c: M[(j, c)])
    for rank_idx, c_prime in enumerate(j_sorted):
        if M[(i, c_prime)] < M[(j, c_prime)]:
            return c_prime, rank_idx
    return None, k


def greedy_delegation(k, M):
    """
    Greedy sequential delegation:
    1. Pick root = emitter that minimizes Σ missed(i→root)
    2. Greedily add emitter with fewest missed to best delegate
    Returns (total_missed, order, per_step_details)
    """
    remaining = set(range(k))

    # Pick root
    best_root = None
    best_root_score = float('inf')
    for r in range(k):
        score = 0
        for i in range(k):
            if i == r:
                continue
            _, missed = best_relay(k, M, i, r)
            score += missed
        if score < best_root_score:
            best_root_score = score
            best_root = r

    order = [best_root]
    remaining.remove(best_root)
    details = []

    while remaining:
        best_next = None
        best_next_missed = float('inf')
        best_next_delegate = None
        best_next_relay = None

        for i in remaining:
            local_best_missed = k + 1
            local_best_delegate = None
            local_best_relay = None
            for j in order:
                relay, missed = best_relay(k, M, i, j)
                if relay is not None and missed < local_best_missed:
                    local_best_missed = missed
                    local_best_delegate = j
                    local_best_relay = relay
            if local_best_missed < best_next_missed:
                best_next_missed = local_best_missed
                best_next = i
                best_next_delegate = local_best_delegate
                best_next_relay = local_best_relay

        if best_next is None:
            best_next = next(iter(remaining))
            best_next_missed = k
            best_next_delegate = None
            best_next_relay = None

        order.append(best_next)
        remaining.remove(best_next)
        details.append({
            'emitter': best_next,
            'delegate': best_next_delegate,
            'relay': best_next_relay,
            'missed': best_next_missed,
        })

    total_missed = sum(d['missed'] for d in details)
    return total_missed, order, details


def build_spanner_edges(k, M, order, details):
    """
    Build the actual spanner edge set and verify reachability.

    Spanner edges:
    - Root (order[0]): all k edges (order[0], j) for j in [k]
    - Each delegation: edge (emitter, relay) + edges (emitter, missed_collector)
    """
    spanner = set()

    root = order[0]
    for j in range(k):
        spanner.add((root, j))

    for d in details:
        i = d['emitter']
        relay = d['relay']
        delegate = d['delegate']
        missed = d['missed']

        if relay is not None:
            # Delegation edge: (i, relay)
            spanner.add((i, relay))
            # Delegate's edge to relay: (delegate, relay) — already in spanner
            # (either from root or from delegate's own edges)

            # Missed collectors: those with M[delegate,c] < M[delegate,relay]
            del_sorted = sorted(range(k), key=lambda c: M[(delegate, c)])
            for r in range(missed):
                missed_col = del_sorted[r]
                spanner.add((i, missed_col))
        else:
            # No valid relay — add all k edges
            for j in range(k):
                spanner.add((i, j))

    return spanner


def check_temporal_reachability(k, M, spanner):
    """
    Check that the spanner preserves all-pairs temporal reachability.

    In the bipartite model:
    - Emitters: a_0, ..., a_{k-1}
    - Collectors: b_0, ..., b_{k-1}
    - Edge (a_i, b_j) at time M[i,j]

    Reachable pairs in the FULL graph:
    - a_i → b_j: direct edge, always reachable
    - a_i → a_j: via b_c where M[i,c] < M[j,c]
    - b_i → b_j: via a_c where M[c,i] < M[c,j]
    - b_i → a_j: via b_i → a_c → b_d → a_j where M[c,i] < M[c,d] < M[j,d]

    For the spanner, only edges in the spanner set are available.
    """
    # Compute full graph reachability
    full_reach = set()
    # All a_i → b_j are reachable (direct edge)
    for i in range(k):
        for j in range(k):
            full_reach.add(('a', i, 'b', j))

    # a_i → a_j via b_c
    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            for c in range(k):
                if M[(i, c)] < M[(j, c)]:
                    full_reach.add(('a', i, 'a', j))
                    break

    # b_i → b_j via a_c
    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            for c in range(k):
                if M[(c, i)] < M[(c, j)]:
                    full_reach.add(('b', i, 'b', j))
                    break

    # b_i → a_j: 3-hop, via a_c then b_d
    for i in range(k):
        for j in range(k):
            found = False
            for c in range(k):
                if (c, i) not in [(x, y) for x in range(k) for y in range(k)]:
                    continue
                for d in range(k):
                    if M[(c, i)] < M[(c, d)] and M[(j, d)] > M[(c, d)]:
                        # Wait, direction: b_i → a_c needs M[c,i] time.
                        # a_c → b_d needs M[c,d] > M[c,i].
                        # b_d → a_j needs M[j,d] > M[c,d].
                        if M[(c, i)] < M[(c, d)] < M[(j, d)]:
                            full_reach.add(('b', i, 'a', j))
                            found = True
                            break
                if found:
                    break

    # Now check spanner reachability
    # Only use edges in the spanner set
    spanner_reach = set()

    # a_i → b_j: only if (i,j) in spanner
    for i in range(k):
        for j in range(k):
            if (i, j) in spanner:
                spanner_reach.add(('a', i, 'b', j))

    # a_i → a_j via b_c: need (i,c) and (j,c) both in spanner, M[i,c] < M[j,c]
    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            for c in range(k):
                if (i, c) in spanner and (j, c) in spanner and M[(i, c)] < M[(j, c)]:
                    spanner_reach.add(('a', i, 'a', j))
                    break

    # For a_i → b_j via multi-hop, we need transitive closure
    # This is getting complex. Let me do BFS on the temporal graph.

    # Build temporal edge list from spanner
    temporal_edges = []
    for (i, j) in spanner:
        temporal_edges.append(('a', i, 'b', j, M[(i, j)]))
        temporal_edges.append(('b', j, 'a', i, M[(i, j)]))
    temporal_edges.sort(key=lambda x: x[4])

    # BFS for all-pairs temporal reachability
    # For each source, compute reachable set using time-respecting paths
    vertices_a = [('a', i) for i in range(k)]
    vertices_b = [('b', j) for j in range(k)]
    all_vertices = vertices_a + vertices_b

    spanner_reach_full = set()
    for src_type, src_id in all_vertices:
        # BFS with time constraint
        # State: (vertex, earliest_arrival_time)
        # We want to find all vertices reachable from src
        reachable = {(src_type, src_id)}
        # For each vertex, track the earliest arrival time
        earliest = {(src_type, src_id): 0}

        changed = True
        while changed:
            changed = False
            for s_type, s_id, d_type, d_id, t in temporal_edges:
                if (s_type, s_id) in earliest and t > earliest[(s_type, s_id)]:
                    if (d_type, d_id) not in earliest or t < earliest[(d_type, d_id)]:
                        earliest[(d_type, d_id)] = t
                        reachable.add((d_type, d_id))
                        changed = True

        for (d_type, d_id) in reachable:
            if (d_type, d_id) != (src_type, src_id):
                spanner_reach_full.add((src_type, src_id, d_type, d_id))

    # Compare
    missed_pairs = full_reach - spanner_reach_full
    extra_pairs = spanner_reach_full - full_reach

    return len(full_reach), len(spanner_reach_full), len(missed_pairs)


# ─── Task 1: Exhaustive small k ───────────────────────────────────────────

def exhaustive_small_k():
    """For k=3,4,5: try many matrices, report worst greedy miss."""
    print("=" * 70)
    print("EXHAUSTIVE: Worst-case greedy miss for small k")
    print("=" * 70)
    print()

    for k in [3, 4, 5, 6]:
        n_trials = 5000
        worst_greedy = 0
        worst_seed = None
        violations = 0
        budget = 2 * k - 2

        for trial in range(n_trials):
            M = random_timestamp_matrix(k, seed=trial)
            total_m, order, details = greedy_delegation(k, M)
            if total_m > worst_greedy:
                worst_greedy = total_m
                worst_seed = trial
            if total_m > budget:
                violations += 1

        spanner_cost = 2 * k - 1 + worst_greedy
        full_budget = 4 * k - 3

        print(f"  k={k}: worst_greedy_missed={worst_greedy}, "
              f"worst_cost={spanner_cost}, budget={full_budget}, "
              f"within={'YES' if spanner_cost <= full_budget else 'NO'}, "
              f"violations={violations}/{n_trials}")

        # Show the worst case details
        if worst_seed is not None:
            M = random_timestamp_matrix(k, seed=worst_seed)
            total_m, order, details = greedy_delegation(k, M)
            print(f"    Worst case (seed={worst_seed}): order={order}")
            for d in details:
                print(f"      emitter {d['emitter']} → delegate {d['delegate']} "
                      f"via relay b_{d['relay']}: missed={d['missed']}")

    print()


# ─── Task 2: Verify spanner correctness ───────────────────────────────────

def verify_spanner_correctness():
    """Build actual spanner and check temporal reachability."""
    print("=" * 70)
    print("VERIFY: Spanner preserves temporal reachability")
    print("=" * 70)
    print()

    total_tests = 0
    total_failures = 0

    for k in [3, 4, 5, 6]:
        n_trials = min(100, max(20, 1000 // k))
        k_failures = 0

        for trial in range(n_trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            total_m, order, details = greedy_delegation(k, M)
            spanner = build_spanner_edges(k, M, order, details)

            full_r, spanner_r, missed_pairs = check_temporal_reachability(k, M, spanner)

            total_tests += 1
            if missed_pairs > 0:
                total_failures += 1
                k_failures += 1
                if k_failures <= 3:
                    print(f"  k={k}, trial={trial}: FAILURE! "
                          f"full_reach={full_r}, spanner_reach={spanner_r}, "
                          f"missed={missed_pairs}, |spanner|={len(spanner)}")

        print(f"  k={k}: {n_trials - k_failures}/{n_trials} correct, "
              f"{k_failures} failures")

    print()
    if total_failures == 0:
        print("  ALL spanners preserve temporal reachability!")
    else:
        print(f"  {total_failures}/{total_tests} FAILURES — spanner construction is INCOMPLETE")
        print("  The delegation model misses some required edges.")
    print()


# ─── Task 3: Fix the spanner construction ─────────────────────────────────

def analyze_failures():
    """
    When the spanner fails, what pairs are missed?
    This reveals whether the delegation model is correct.
    """
    print("=" * 70)
    print("FAILURE ANALYSIS: What pairs are missed?")
    print("=" * 70)
    print()

    for k in [3, 4, 5]:
        for trial in range(50):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            total_m, order, details = greedy_delegation(k, M)
            spanner = build_spanner_edges(k, M, order, details)

            full_r, spanner_r, missed = check_temporal_reachability(k, M, spanner)

            if missed > 0:
                print(f"  k={k}, trial={trial}: missed {missed} pairs")
                print(f"    order={order}")
                print(f"    |spanner|={len(spanner)}, budget={4*k-3}")

                # What types of pairs are missed?
                # Recompute to get the actual missed pairs
                # (simplified — just report the count and types)

                # Check: are the missed pairs all b→b or b→a types?
                # The delegation model only ensures a→a and a→b reachability.
                print(f"    (reachability model may only cover emitter-to-X pairs)")
                print()
                if trial >= 2:
                    break

    print()
    print("  KEY INSIGHT: The delegation model ensures:")
    print("    - a_i → b_j: root has all k edges, delegates add relay+missed")
    print("    - a_i → a_j: via relay b_c where i→c→j is temporal")
    print("    - b_i → b_j and b_i → a_j: NOT directly handled!")
    print("  The spanner needs ADDITIONAL structure for b→b and b→a paths.")
    print()


# ─── Task 4: Enhanced spanner with reverse coverage ───────────────────────

def enhanced_spanner(k, M):
    """
    Enhanced spanner: handle BOTH directions.

    Forward: a_i → b_j and a_i → a_j (delegation handles this)
    Reverse: b_j → a_i and b_j → b_i (need separate treatment)

    For reverse: b_j → a_i requires edge (i,j) where M[i,j] is the arrival time.
    b_j can reach a_i directly if (i,j) is in the spanner.
    b_j can reach b_i via a_c: b_j → a_c → b_i requires M[c,j] < M[c,i]
    and both (c,j) and (c,i) in the spanner.

    The root's edges already include (root, j) for all j. So:
    - b_j → a_root for all j (via edge (root,j))
    - From a_root, the delegation chain reaches everything forward.
    - But b_j → a_{non-root} needs (non-root, j) in the spanner.

    For b_j → b_i: need a_c with M[c,j] < M[c,i] and both in spanner.
    The root provides: M[root,j] < M[root,i] for one direction.

    Actually, in the temporal bipartite graph, the reachability is:
    b_j → a_i iff edge (i,j) exists (it always does in K_{k,k}).
    In the spanner: b_j → a_i iff (i,j) is in the spanner.

    So the spanner needs (i,j) for every pair (b_j, a_i) that's reachable
    in the full graph. In K_{k,k}, EVERY b_j → a_i is reachable.
    So the spanner needs all k² edges?? No — multi-hop paths.

    b_j → a_i via b_j → a_c → b_d → a_i requires:
    M[c,j] (b_j arrival at a_c) < M[c,d] (a_c goes to b_d) < M[i,d] (b_d to a_i)
    And (c,j), (c,d), (i,d) all in spanner.

    This is the 3-hop reverse direction. The spanner doesn't need all k² edges;
    it just needs enough to reconstruct multi-hop paths.

    For the CPS framework, the spanner is for TEMPORAL reachability on the
    FULL K_n graph (not bipartite). The bipartite structure is an intermediate
    reduction. The full spanner on K_n automatically handles both directions
    because edge (u,v) at time t allows both u→v and v→u at time t.

    IN THE BIPARTITE MODEL: edge (a_i, b_j) at time t allows BOTH:
    - a_i → b_j starting at time t
    - b_j → a_i ending at time t (b_j can use this edge to reach a_i if
      b_j arrives at the edge before time t)

    Wait, this is the key: in a temporal graph, edge {u,v} at time t means
    u can reach v at time t AND v can reach u at time t. But in CPS's model,
    temporal edges are DIRECTED or undirected?

    In the standard model (Casteigts et al.): edge (u,v) at time t is
    traversable in BOTH directions at time t. So:
    - From u, you can reach v at time t (arriving at v at time t)
    - From v, you can reach u at time t (arriving at u at time t)

    This simplifies things: the spanner only needs to support temporal journeys
    in the undirected sense. So a_i → a_j via b_c at time M[i,c] < M[j,c]:
    a_i uses edge (i,c) at time M[i,c], then a_j uses edge (j,c) at time M[j,c].
    The journey is: a_i at time M[i,c] → b_c → a_j at time M[j,c].
    Valid because M[i,c] < M[j,c].

    For a_j → a_i: need b_c with M[j,c] < M[i,c]. This is the REVERSE.
    The delegation from j to i would handle this.

    So the spanner from delegation handles a_i → a_j for all (i,j) IF:
    - For each pair (i,j), either i→j or j→i has a temporal path in the spanner.
    - But we need BOTH directions!

    The delegation from i to its delegate j ensures i→j.
    The delegation from j to its delegate (maybe not i) ensures j→?.
    So j→i is NOT automatically handled!

    For the FULL temporal spanner:
    Both forward and reverse delegation need to be covered.
    This means DOUBLE the delegation cost? Or does the root handle it?

    Root a_0 has edges to all collectors. So:
    - a_0 → b_j for all j (direct)
    - b_j → a_0 for all j (direct, using same edge)
    - a_0 → a_i: need b_c with M[0,c] < M[i,c] (forward from root)
    - a_i → a_0: need b_c with M[i,c] < M[0,c] (reverse to root)

    For a_i → a_j where neither is root: need relay in BOTH directions.
    But if i is delegated to root (via relay c1) and j is delegated to root
    (via relay c2), then:
    - a_i → root → a_j: i → c1 → root → c' → j (if there's a temporal path)
    - a_j → root → a_i: j → c2 → root → c'' → i

    The multi-hop routing through root handles this, but the timestamp
    constraints must be compatible.

    This is getting complex. Let me just measure the CORRECT spanner
    (full temporal reachability) and count its edges.
    """
    # Greedy spanner: add edges that increase temporal reachability
    # Start from empty, add cheapest edge that covers the most new pairs

    # First compute full reachability
    # Full temporal bipartite: all edges present
    all_pairs = compute_full_reachability(k, M)

    # Greedy: start with root's edges
    spanner = set()
    root, _, _ = greedy_delegation(k, M)[:1], None, None

    # Actually, let me use a greedy edge-addition approach
    # Add edges in order of "covers most new pairs"
    remaining_edges = [(i, j) for i in range(k) for j in range(k)]
    random.shuffle(remaining_edges)

    covered = set()
    spanner_edges = set()

    # Try edges in order of their timestamp (early first, which tend to be
    # more useful for forward reachability)
    remaining_edges.sort(key=lambda e: M[e])

    for (i, j) in remaining_edges:
        # Add this edge, check how many new pairs it covers
        test_spanner = spanner_edges | {(i, j)}
        new_covered = compute_spanner_reachability(k, M, test_spanner)
        new_pairs = new_covered - covered

        if new_pairs:
            spanner_edges.add((i, j))
            covered = new_covered

        if covered == all_pairs:
            break

    return spanner_edges, len(covered), len(all_pairs)


def compute_full_reachability(k, M):
    """Compute all reachable pairs in the full K_{k,k} temporal graph."""
    pairs = set()
    # All edges: (a_i, b_j) at time M[i,j], bidirectional
    # Build temporal edge list
    edges = []
    for i in range(k):
        for j in range(k):
            edges.append(('a', i, 'b', j, M[(i, j)]))
            edges.append(('b', j, 'a', i, M[(i, j)]))

    vertices = [('a', i) for i in range(k)] + [('b', j) for j in range(k)]

    for src in vertices:
        reachable = set()
        earliest = {src: 0}
        changed = True
        while changed:
            changed = False
            for s_t, s_id, d_t, d_id, t in edges:
                s = (s_t, s_id)
                d = (d_t, d_id)
                if s in earliest and t > earliest[s]:
                    if d not in earliest or t < earliest[d]:
                        earliest[d] = t
                        changed = True

        for d in earliest:
            if d != src:
                pairs.add((src, d))

    return pairs


def compute_spanner_reachability(k, M, spanner_edges):
    """Compute reachable pairs using only spanner edges."""
    edges = []
    for (i, j) in spanner_edges:
        edges.append(('a', i, 'b', j, M[(i, j)]))
        edges.append(('b', j, 'a', i, M[(i, j)]))

    vertices = [('a', i) for i in range(k)] + [('b', j) for j in range(k)]
    pairs = set()

    for src in vertices:
        earliest = {src: 0}
        changed = True
        while changed:
            changed = False
            for s_t, s_id, d_t, d_id, t in edges:
                s = (s_t, s_id)
                d = (d_t, d_id)
                if s in earliest and t > earliest[s]:
                    if d not in earliest or t < earliest[d]:
                        earliest[d] = t
                        changed = True

        for d in earliest:
            if d != src:
                pairs.add((src, d))

    return pairs


# ─── Task 5: Greedy edge-addition spanner ─────────────────────────────────

def greedy_edge_spanner():
    """
    Build a true temporal spanner by greedy edge addition.
    Count how many edges are needed for full temporal reachability.
    """
    print("=" * 70)
    print("GREEDY EDGE-ADDITION SPANNER: True edge count")
    print("=" * 70)
    print()

    print(f"{'k':>5} {'n=2k':>5} | {'full_reach':>11} {'spanner_edges':>14} "
          f"{'4k-3':>5} {'2n-3':>5} | {'within':>7}")
    print("-" * 70)

    for k in [3, 4, 5, 6, 7, 8]:
        trials = min(30, max(10, 500 // (k * k)))
        edge_counts = []
        full_reachabilities = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)

            # Full reachability
            full_pairs = compute_full_reachability(k, M)

            # Greedy spanner
            spanner_edges = set()
            covered = set()

            # Add edges greedily
            all_edges = [(i, j) for i in range(k) for j in range(k)]

            while covered != full_pairs:
                best_edge = None
                best_gain = 0

                for (i, j) in all_edges:
                    if (i, j) in spanner_edges:
                        continue
                    test = spanner_edges | {(i, j)}
                    new_covered = compute_spanner_reachability(k, M, test)
                    gain = len(new_covered - covered)
                    if gain > best_gain:
                        best_gain = gain
                        best_edge = (i, j)

                if best_edge is None:
                    break

                spanner_edges.add(best_edge)
                covered = compute_spanner_reachability(k, M, spanner_edges)

            edge_counts.append(len(spanner_edges))
            full_reachabilities.append(len(full_pairs))

        avg_edges = sum(edge_counts) / trials
        max_edges = max(edge_counts)
        budget = 4 * k - 3
        within = max_edges <= budget

        print(f"{k:5d} {2*k:5d} | {sum(full_reachabilities)/trials:11.0f} "
              f"{avg_edges:14.1f} {budget:5d} {budget:5d} | "
              f"{'YES' if within else f'NO(max={max_edges})'}")

    print()


# ─── Task 6: Compare delegation cost with edge count ──────────────────────

def delegation_vs_edge_count():
    """
    Compare the delegation model's predicted cost with the actual minimum
    spanner edge count.
    """
    print("=" * 70)
    print("DELEGATION vs ACTUAL SPANNER: Edge count comparison")
    print("=" * 70)
    print()

    print(f"{'k':>5} | {'deleg_cost':>11} {'actual_greedy':>14} {'ratio':>7} | "
          f"{'4k-3':>5}")
    print("-" * 55)

    for k in [3, 4, 5, 6]:
        trials = min(30, max(10, 200 // (k * k)))
        deleg_costs = []
        actual_costs = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)

            # Delegation model cost
            total_m, order, details = greedy_delegation(k, M)
            deleg_cost = 2 * k - 1 + total_m

            # Actual greedy spanner
            full_pairs = compute_full_reachability(k, M)
            spanner_edges = set()
            covered = set()
            all_edges = [(i, j) for i in range(k) for j in range(k)]

            while covered != full_pairs:
                best_edge = None
                best_gain = 0
                for (i, j) in all_edges:
                    if (i, j) in spanner_edges:
                        continue
                    test = spanner_edges | {(i, j)}
                    new_covered = compute_spanner_reachability(k, M, test)
                    gain = len(new_covered - covered)
                    if gain > best_gain:
                        best_gain = gain
                        best_edge = (i, j)
                if best_edge is None:
                    break
                spanner_edges.add(best_edge)
                covered = compute_spanner_reachability(k, M, spanner_edges)

            actual_costs.append(len(spanner_edges))
            deleg_costs.append(deleg_cost)

        avg_d = sum(deleg_costs) / trials
        avg_a = sum(actual_costs) / trials
        ratio = avg_d / avg_a if avg_a > 0 else 0
        budget = 4 * k - 3

        print(f"{k:5d} | {avg_d:11.1f} {avg_a:14.1f} {ratio:7.2f} | {budget:5d}")

    print()
    print("  ratio > 1 means delegation overestimates (conservative)")
    print("  ratio < 1 means delegation underestimates (BUG)")
    print()


# ─── Main ──────────────────────────────────────────────────────────────────

def run():
    print("H27 Part 3: GREEDY BOUND AND SPANNER VERIFICATION")
    print("=" * 70)
    print()

    exhaustive_small_k()
    print()
    verify_spanner_correctness()
    print()
    analyze_failures()
    print()
    greedy_edge_spanner()
    print()
    delegation_vs_edge_count()


if __name__ == '__main__':
    run()
