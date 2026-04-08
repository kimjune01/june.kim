#!/usr/bin/env python3 -u
"""
H9: BGP-style distributed temporal spanner construction.

Tests whether a BGP-inspired distributed pruning algorithm can produce
temporal spanners within the 4k-3 edge budget on random k×k bipartite
temporal cliques.
"""

import random
from collections import defaultdict
from copy import deepcopy
import time

random.seed(42)


def random_matrix(k):
    """Random all-distinct k×k matrix: permutation of 1..k²."""
    perm = list(range(1, k * k + 1))
    random.shuffle(perm)
    return [perm[i * k:(i + 1) * k] for i in range(k)]


def compute_reachability(active_edges, M, k):
    """
    Compute reach[src][dst] = earliest arrival time.
    Vertices 0..k-1 are A, k..2k-1 are B. Edges are undirected at their timestamp.
    A temporal journey uses edges with non-decreasing timestamps.

    Returns (reach matrix, reachable set).
    """
    n = 2 * k
    INF = float('inf')
    reach = [[INF] * n for _ in range(n)]
    for u in range(n):
        reach[u][u] = 0

    # Build sorted edge list (undirected: A_i <-> B_j at time t)
    edge_list = []
    for (i, j) in active_edges:
        edge_list.append((i, k + j, M[i][j]))
    edge_list.sort(key=lambda e: e[2])

    # Bellman-Ford style: iterate until no change
    changed = True
    while changed:
        changed = False
        for (u, v, t) in edge_list:
            for src in range(n):
                if reach[src][u] <= t and t < reach[src][v]:
                    reach[src][v] = t
                    changed = True
                if reach[src][v] <= t and t < reach[src][u]:
                    reach[src][u] = t
                    changed = True

    reachable = set()
    for u in range(n):
        for v in range(n):
            if u != v and reach[u][v] < INF:
                reachable.add((u, v))
    return reach, reachable


def reachability_preserved(active_edges, remove_edge, M, k, baseline_reachable):
    """Check if removing remove_edge preserves all baseline reachability."""
    trial = active_edges - {remove_edge}
    _, trial_reachable = compute_reachability(trial, M, k)
    return baseline_reachable.issubset(trial_reachable)


# ─── Algorithm 1: BGP-style (greedy pruning, preserves reachability) ──

def run_bgp_standard(M, k):
    """
    Standard BGP pruning: iteratively remove edges that don't affect
    temporal reachability. Each round, try removing each edge; if
    reachability is preserved, drop it. Repeat until stable.
    """
    active = {(i, j) for i in range(k) for j in range(k)}
    rounds = 0

    while True:
        rounds += 1
        _, baseline = compute_reachability(active, M, k)
        pruned = False
        edges = list(active)
        random.shuffle(edges)

        for e in edges:
            if e not in active:
                continue
            if reachability_preserved(active, e, M, k, baseline):
                active.discard(e)
                # Recompute baseline after each removal (greedy)
                _, baseline = compute_reachability(active, M, k)
                pruned = True

        if not pruned:
            break

    _, final_reachable = compute_reachability(active, M, k)
    full_active = {(i, j) for i in range(k) for j in range(k)}
    _, full_reachable = compute_reachability(full_active, M, k)
    frac = len(final_reachable) / len(full_reachable) if full_reachable else 1.0
    return active, rounds, frac


# ─── Algorithm 2: Aggressive (connectivity-only, timing can degrade) ──

def run_bgp_aggressive(M, k):
    """
    Drop edges even if timing degrades, as long as all reachable pairs
    remain reachable (allows longer journeys = stretch tolerance).
    Sort by "least timing damage" first.
    """
    active = {(i, j) for i in range(k) for j in range(k)}
    n = 2 * k
    full_reach, full_reachable = compute_reachability(active, M, k)
    rounds = 0

    while True:
        rounds += 1
        current_reach, current_reachable = compute_reachability(active, M, k)
        pruned = False

        # Score each edge by timing damage if removed
        scores = []
        for e in active:
            trial = active - {e}
            trial_reach, trial_reachable = compute_reachability(trial, M, k)
            if not current_reachable.issubset(trial_reachable):
                scores.append((e, float('inf')))
            else:
                damage = sum(
                    max(0, trial_reach[u][v] - current_reach[u][v])
                    for u in range(n) for v in range(n)
                    if u != v and current_reach[u][v] < float('inf')
                )
                scores.append((e, damage))

        scores.sort(key=lambda x: x[1])

        for (e, dmg) in scores:
            if dmg == float('inf'):
                continue
            if e not in active:
                continue
            trial = active - {e}
            _, trial_reachable = compute_reachability(trial, M, k)
            if current_reachable.issubset(trial_reachable):
                active = trial
                # Recompute for next edge in this round
                current_reach, current_reachable = compute_reachability(active, M, k)
                pruned = True

        if not pruned:
            break

    _, final_reachable = compute_reachability(active, M, k)
    frac = len(final_reachable) / len(full_reachable) if full_reachable else 1.0
    return active, rounds, frac


# ─── Algorithm 3: Economic pruning ───────────────────────────────────

def run_bgp_economic(M, k):
    """
    Economic: each edge costs 1. Value = # of (src,dst) pairs where this edge
    is on the UNIQUE shortest temporal path. Drop edges with value 0 first,
    then edges with lowest value, always checking connectivity preservation.
    """
    active = {(i, j) for i in range(k) for j in range(k)}
    n = 2 * k
    _, full_reachable = compute_reachability(active, M, k)
    rounds = 0

    while True:
        rounds += 1
        _, current_reachable = compute_reachability(active, M, k)
        pruned = False

        # Compute criticality: how many pairs lose connectivity if this edge is removed
        criticality = {}
        for e in active:
            trial = active - {e}
            _, trial_reachable = compute_reachability(trial, M, k)
            criticality[e] = len(current_reachable - trial_reachable)

        # Sort: non-critical first, then by lowest criticality
        order = sorted(active, key=lambda e: criticality[e])

        for e in order:
            if criticality[e] > 0:
                break  # all remaining are critical
            if e not in active:
                continue
            trial = active - {e}
            _, trial_reachable = compute_reachability(trial, M, k)
            if current_reachable.issubset(trial_reachable):
                active = trial
                _, current_reachable = compute_reachability(active, M, k)
                pruned = True

        if not pruned:
            break

    _, final_reachable = compute_reachability(active, M, k)
    frac = len(final_reachable) / len(full_reachable) if full_reachable else 1.0
    return active, rounds, frac


# ─── Algorithm 4: Greedy offline optimal ─────────────────────────────

def greedy_offline(M, k):
    """
    Greedy offline: repeatedly remove the edge whose removal causes least
    damage, stopping when no edge can be removed without losing connectivity.
    """
    active = {(i, j) for i in range(k) for j in range(k)}
    n = 2 * k
    _, full_reachable = compute_reachability(active, M, k)

    while len(active) > 1:
        _, current_reachable = compute_reachability(active, M, k)
        best_edge = None
        best_damage = float('inf')

        for e in active:
            trial = active - {e}
            trial_reach, trial_reachable = compute_reachability(trial, M, k)
            lost = len(current_reachable - trial_reachable)
            if lost > 0:
                damage = lost * 10000
            else:
                # Timing degradation
                curr_reach, _ = compute_reachability(active, M, k)
                damage = sum(
                    max(0, trial_reach[u][v] - curr_reach[u][v])
                    for u in range(n) for v in range(n)
                    if u != v and curr_reach[u][v] < float('inf')
                )

            if damage < best_damage:
                best_damage = damage
                best_edge = e

        if best_damage >= 10000:
            break
        active.discard(best_edge)

    _, final_reachable = compute_reachability(active, M, k)
    frac = len(final_reachable) / len(full_reachable) if full_reachable else 1.0
    return active, frac


# ─── 1-Healability test ──────────────────────────────────────────────

def test_healability(active_edges, M, k):
    """
    For each edge in the spanner, remove it and check:
    1. Does removal preserve connectivity? (survived)
    2. If not, can adding one non-spanner edge restore it? (healed)
    3. Otherwise: unhealed.
    """
    n = 2 * k
    base_reach, base_reachable = compute_reachability(active_edges, M, k)
    all_edges = {(i, j) for i in range(k) for j in range(k)}
    non_spanner = all_edges - active_edges

    survived = 0
    healed = 0
    unhealed = 0

    for e in list(active_edges):
        trial = active_edges - {e}
        _, trial_reachable = compute_reachability(trial, M, k)

        if base_reachable.issubset(trial_reachable):
            survived += 1
            continue

        # Try healing with one non-spanner edge
        found_heal = False
        for e2 in non_spanner:
            repair = trial | {e2}
            _, repair_reachable = compute_reachability(repair, M, k)
            if base_reachable.issubset(repair_reachable):
                found_heal = True
                break

        if found_heal:
            healed += 1
        else:
            unhealed += 1

    return survived, healed, unhealed


# ─── True BGP simulation (distributed announcement rounds) ───────────

def run_true_bgp(M, k):
    """
    True BGP simulation with announcement rounds:

    Each A-vertex maintains a routing table: for each destination vertex,
    the earliest arrival time and which B-neighbor to use.

    Round 0: Each A_i knows it can reach B_j at time M[i][j] for all j.

    Each round: B-vertices relay. For each B_j, collect announcements from
    all connected A-vertices, then relay: if A_i1 says "I can reach X at time T"
    and A_i2 is connected to B_j at time M[i2][j], then A_i2 learns it can
    reach X at time max(M[i2][j], T) IF M[i2][j] <= T (must arrive at B_j
    before the onward journey departs... wait, the journey is non-decreasing,
    so we just need max(M[i2][j], T) as arrival time and M[i2][j] <= T means
    the relay is valid with arrival T. If M[i2][j] > T, arrival is M[i2][j]
    but the ONWARD path from B_j needs timestamps > M[i2][j]...

    Actually the relay only works if the onward path's timestamps are all >= M[i2][j].
    We don't track full paths, so we conservatively require:
    - A_i2 reaches B_j at time M[i2][j]
    - From B_j onward to X, need timestamps >= M[i2][j]
    - A_i1 can reach X from B_j, but via a path that starts at time M[i1][j] at B_j
    - This path works for A_i2 only if M[i2][j] <= M[i1][j] (earlier arrival at B_j,
      so the same onward path is still valid with non-decreasing timestamps)

    Better approach: track routes as (target, arrival_time, departure_time_from_relay)
    where departure_time_from_relay is the timestamp of the first edge after B_j.

    Simplest correct approach: each A_i maintains routes[target] = earliest_arrival.
    During relay through B_j, A_i2 can reach target X via B_j if:
      arrival_at_X = we compute it directly from the edge times.

    Let me use a different formulation: route = (target, arrival_time).
    A_i advertises to B_j: all its routes.
    B_j relays to A_i2: for each route (target, T) from A_i1,
    A_i2 can reach target at time T if M[i2][j] <= M[i1][j] AND M[i1][j] <= T.
    Wait, no. The path is: A_i2 -> B_j at time M[i2][j], then B_j -> A_i1 at time M[i1][j]
    (if M[i1][j] >= M[i2][j]), then A_i1 -> ... -> target.

    But A_i1's route to target might not start from A_i1. It could be a direct edge.
    The arrival time T at target was computed assuming A_i1 starts from time 0.
    The path from A_i1 to target uses edges with timestamps that form a non-decreasing
    sequence starting from some time. We need the first timestamp >= M[i1][j].

    This is fundamentally the problem: we can't decompose temporal paths this way
    because the "onward" path timing depends on when you arrive.

    CORRECT APPROACH: Don't try to decompose. Just use the reachability matrix.
    After computing full reachability, determine which edges are used in shortest paths.
    The "BGP" metaphor maps to: iterative pruning with reachability recomputation.
    """
    # Fall back to the standard pruning (which IS what BGP converges to)
    return run_bgp_standard(M, k)


# ─── Per-node edge counts ────────────────────────────────────────────

def per_node_counts(active_edges, k):
    """Return (A-node degrees, B-node degrees)."""
    a_deg = [0] * k
    b_deg = [0] * k
    for (i, j) in active_edges:
        a_deg[i] += 1
        b_deg[j] += 1
    return a_deg, b_deg


# ─── Main experiment ──────────────────────────────────────────────────

def main():
    num_trials = 50

    print("=" * 80)
    print("H9: BGP-style Temporal Spanner Construction")
    print("=" * 80)
    print(f"Trials per k: {num_trials}")
    print(f"Matrices: random permutations of 1..k^2")

    all_results = {}

    for k in [3, 4, 5, 6, 7]:
        budget = 4 * k - 3
        n = 2 * k
        print(f"\n{'─' * 70}")
        print(f"k={k}, n={n}, budget=4k-3={budget}, full_edges={k*k}")
        print(f"{'─' * 70}")

        results = {
            'bgp': {'counts': [], 'rounds': [], 'in_budget': 0},
            'aggressive': {'counts': [], 'rounds': [], 'in_budget': 0},
            'economic': {'counts': [], 'rounds': [], 'in_budget': 0},
            'greedy': {'counts': [], 'in_budget': 0},
            'heal': [],
        }

        t0 = time.time()

        for trial in range(num_trials):
            M = random_matrix(k)

            # 1. Standard BGP
            edges, rounds, frac = run_bgp_standard(M, k)
            results['bgp']['counts'].append(len(edges))
            results['bgp']['rounds'].append(rounds)
            if len(edges) <= budget:
                results['bgp']['in_budget'] += 1

            # 2. Aggressive (k <= 6)
            if k <= 6:
                agg_edges, agg_rounds, agg_frac = run_bgp_aggressive(M, k)
                results['aggressive']['counts'].append(len(agg_edges))
                results['aggressive']['rounds'].append(agg_rounds)
                if len(agg_edges) <= budget:
                    results['aggressive']['in_budget'] += 1

            # 3. Economic (k <= 6)
            if k <= 6:
                eco_edges, eco_rounds, eco_frac = run_bgp_economic(M, k)
                results['economic']['counts'].append(len(eco_edges))
                results['economic']['rounds'].append(eco_rounds)
                if len(eco_edges) <= budget:
                    results['economic']['in_budget'] += 1

            # 4. Greedy offline (k <= 5 -- expensive)
            if k <= 5:
                gr_edges, gr_frac = greedy_offline(M, k)
                results['greedy']['counts'].append(len(gr_edges))
                if len(gr_edges) <= budget:
                    results['greedy']['in_budget'] += 1

            # 5. Healability (first 5 trials, k <= 5)
            if trial < 5 and k <= 5:
                surv, heal, unheal = test_healability(edges, M, k)
                results['heal'].append((len(edges), surv, heal, unheal))

            if (trial + 1) % 10 == 0:
                elapsed = time.time() - t0
                print(f"  trial {trial+1}/{num_trials} [{elapsed:.1f}s]")

        all_results[k] = results
        elapsed = time.time() - t0

        # ── Report ──
        c = results['bgp']['counts']
        r = results['bgp']['rounds']
        print(f"\n  Standard BGP:")
        print(f"    edges: min={min(c)} max={max(c)} mean={sum(c)/len(c):.1f} median={sorted(c)[len(c)//2]}")
        print(f"    rounds: min={min(r)} max={max(r)} mean={sum(r)/len(r):.1f}")
        print(f"    within budget: {results['bgp']['in_budget']}/{num_trials}")

        a_degs_all = []
        b_degs_all = []
        # Just report on last trial's edge set for per-node info
        a_deg, b_deg = per_node_counts(edges, k)
        print(f"    last trial per-node A-degrees: {a_deg}")
        print(f"    last trial per-node B-degrees: {b_deg}")

        if results['aggressive']['counts']:
            c = results['aggressive']['counts']
            print(f"\n  Aggressive BGP (connectivity-only):")
            print(f"    edges: min={min(c)} max={max(c)} mean={sum(c)/len(c):.1f} median={sorted(c)[len(c)//2]}")
            print(f"    within budget: {results['aggressive']['in_budget']}/{num_trials}")

        if results['economic']['counts']:
            c = results['economic']['counts']
            print(f"\n  Economic BGP:")
            print(f"    edges: min={min(c)} max={max(c)} mean={sum(c)/len(c):.1f} median={sorted(c)[len(c)//2]}")
            print(f"    within budget: {results['economic']['in_budget']}/{num_trials}")

        if results['greedy']['counts']:
            c = results['greedy']['counts']
            print(f"\n  Greedy Offline:")
            print(f"    edges: min={min(c)} max={max(c)} mean={sum(c)/len(c):.1f} median={sorted(c)[len(c)//2]}")
            print(f"    within budget: {results['greedy']['in_budget']}/{num_trials}")

        if results['heal']:
            print(f"\n  1-Healability (first 5 trials):")
            for idx, (ec, s, h, u) in enumerate(results['heal']):
                print(f"    trial {idx}: {ec} edges, survived={s} healed={h} unhealed={u}")

        print(f"\n  Total time for k={k}: {elapsed:.1f}s")

    # ── Summary ──
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'k':>3} {'budget':>6} {'BGP mean':>9} {'BGP %ok':>8} {'Agg mean':>9} {'Agg %ok':>8} {'Eco mean':>9} {'Eco %ok':>8} {'Greedy':>9}")
    for k in [3, 4, 5, 6, 7]:
        r = all_results[k]
        budget = 4 * k - 3
        bgp_mean = sum(r['bgp']['counts']) / len(r['bgp']['counts'])
        bgp_pct = 100 * r['bgp']['in_budget'] / num_trials

        if r['aggressive']['counts']:
            agg_mean = sum(r['aggressive']['counts']) / len(r['aggressive']['counts'])
            agg_pct = 100 * r['aggressive']['in_budget'] / num_trials
        else:
            agg_mean = float('nan')
            agg_pct = float('nan')

        if r['economic']['counts']:
            eco_mean = sum(r['economic']['counts']) / len(r['economic']['counts'])
            eco_pct = 100 * r['economic']['in_budget'] / num_trials
        else:
            eco_mean = float('nan')
            eco_pct = float('nan')

        if r['greedy']['counts']:
            gr_mean = sum(r['greedy']['counts']) / len(r['greedy']['counts'])
        else:
            gr_mean = float('nan')

        print(f"{k:>3} {budget:>6} {bgp_mean:>9.1f} {bgp_pct:>7.0f}% {agg_mean:>9.1f} {agg_pct:>7.0f}% {eco_mean:>9.1f} {eco_pct:>7.0f}% {gr_mean:>9.1f}")


if __name__ == "__main__":
    main()
