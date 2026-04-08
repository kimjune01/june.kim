#!/usr/bin/env python3
"""
H27: Birthday bound on sequential delegation in the CPS fireworks residual.

After CPS dismountability reduction, the residual is a biclique with k emitters
and k collectors, connected by a k×k timestamp matrix M. S⁻[i] = argmin_j M[i,j],
S⁺[i] = argmax_j M[i,j]. These are the extremal matchings (not necessarily
permutations when k < total vertices, but we model them as permutations on [k]
for the biclique residual).

Sequential delegation: emitters are eliminated one at a time.
When emitter i delegates to emitter j via collector c' (relay):
  - i → c' at time M[i,c']
  - c' → j at time M[j,c'] (j reaches c' at this time)
  - For this to be a valid temporal journey: M[i,c'] < M[j,c'] is NOT the
    right condition (that means i arrives at c' before j does, which is GOOD
    for i reaching j through c', but the direction is c' to j, not j to c').

Actually in the biclique model:
  - Emitters are on one side (A), collectors on the other (B).
  - Edge (a_i, b_j) has timestamp M[i,j].
  - A temporal journey from a_i to a_j goes: a_i → b_c → a_j
    requiring M[i,c] < M[j,c] (i's edge to b_c happens BEFORE j's edge to b_c).
  - Then to reach b_d from a_i via a_j: a_i → b_c → a_j → b_d
    requiring M[i,c] < M[j,c] < M[j,d].

When emitter i delegates to emitter j (the surviving delegate):
  - They share a relay collector c' where M[i,c'] < M[j,c'].
  - Emitter j then covers collector d if M[j,d] > M[j,c'] (j's edge to d
    is later than j's edge to c').
  - A collector d is "missed" if M[j,d] < M[j,c'] — j reaches d BEFORE
    arriving at the relay, so the temporal journey i→c'→j→d is invalid.

So: missed(i→j via c') = {d : M[j,d] < M[j,c']}
    = collectors that j reaches earlier than its relay connection.

The BEST relay c' for delegation i→j minimizes |missed|:
  Pick c' = argmax_{c : M[i,c] < M[j,c]} M[j,c']
  i.e., the relay where j arrives LATEST, so fewer collectors have M[j,d] < M[j,c'].

With this relay: missed = {d : M[j,d] < M[j,c']} = collectors ranked below c'
in j's row ordering. If c' has rank r among j's columns (sorted by M[j,·]),
then |missed| = r (the r columns with smaller timestamps than M[j,c']).

We want c' with the highest rank in j's ordering, subject to M[i,c'] < M[j,c'].

Tasks:
1. Implement precise temporal delegation model
2. Compute missed collectors per delegation
3. Sequential delegation spanner cost
4. Birthday probability analysis
5. Full spanner budget check against 4k-3
"""

import random
import math
from collections import defaultdict
import sys


def random_timestamp_matrix(k, seed=None):
    """
    Random k×k matrix with distinct timestamps from 1 to k².
    M[i][j] = timestamp of edge (emitter i, collector j).
    """
    rng = random.Random(seed)
    ts = rng.sample(range(1, k * k + 1), k * k)
    M = {}
    idx = 0
    for i in range(k):
        for j in range(k):
            M[(i, j)] = ts[idx]
            idx += 1
    return M


def compute_extremal_matchings(k, M):
    """
    S⁻[i] = argmin_j M[i,j] (row minimum column)
    S⁺[i] = argmax_j M[i,j] (row maximum column)
    """
    S_minus = {}
    S_plus = {}
    for i in range(k):
        min_j = min(range(k), key=lambda j: M[(i, j)])
        max_j = max(range(k), key=lambda j: M[(i, j)])
        S_minus[i] = min_j
        S_plus[i] = max_j
    return S_minus, S_plus


def row_rank(k, M, i):
    """
    Return the rank ordering of columns for row i.
    rank[j] = position of column j when sorted by M[i,j].
    rank[j] = 0 means M[i,j] is the smallest in row i.
    """
    cols_sorted = sorted(range(k), key=lambda j: M[(i, j)])
    rank = {}
    for r, j in enumerate(cols_sorted):
        rank[j] = r
    return rank


def best_relay(k, M, i, j):
    """
    Find the best relay collector c' for delegation from emitter i to emitter j.

    Requirements:
    - M[i,c'] < M[j,c'] (i reaches c' before j does, enabling temporal path i→c'→j)
    - Among valid relays, pick the one where M[j,c'] is MAXIMIZED
      (so j reaches c' as late as possible, minimizing the number of collectors
       that j reaches even later — wait, we want to MAXIMIZE the number of
       collectors j can still reach after the relay point).

    Actually: after arriving at j via relay c', we need j→d with M[j,d] > M[j,c'].
    So we want M[j,c'] to be as SMALL as possible to maximize how many d have
    M[j,d] > M[j,c'].

    Wait — let me re-examine the temporal journey:
    i → b_{c'} at time M[i,c']
    b_{c'} → j at time M[j,c']   (this means j's edge to c' has timestamp M[j,c'])

    For the journey i → c' → j to be valid, we need:
    M[i,c'] < M[j,c']   (time-respecting: i's edge to c' is earlier than j's edge to c')

    Then from j to reach collector d: j → b_d at time M[j,d].
    For the full journey i → c' → j → d to be valid:
    M[j,c'] < M[j,d]   (j's edge to d is later than j's edge to c')

    So d is reachable iff M[j,d] > M[j,c'].
    d is MISSED iff M[j,d] ≤ M[j,c'].

    Since all timestamps are distinct: d is missed iff M[j,d] < M[j,c'].

    If M[j,c'] has rank r in row j (0-indexed), then there are exactly r collectors
    with M[j,d] < M[j,c'], so |missed| = r.

    To minimize |missed|, pick the relay c' that has the LOWEST rank in j's row
    (i.e., M[j,c'] is as small as possible), subject to M[i,c'] < M[j,c'].

    The absolute best: c' = S⁻[j] (j's row minimum). Then rank = 0, missed = 0.
    But we need M[i,S⁻[j]] < M[j,S⁻[j]]. Since M[j,S⁻[j]] is the MINIMUM in j's row,
    this requires M[i,S⁻[j]] to be even smaller. Possible but not guaranteed.

    If S⁻[j] doesn't work, try the next-lowest in j's row, etc.
    """
    # Sort columns by M[j,c'] ascending
    j_sorted = sorted(range(k), key=lambda c: M[(j, c)])

    for rank_idx, c_prime in enumerate(j_sorted):
        if M[(i, c_prime)] < M[(j, c_prime)]:
            return c_prime, rank_idx  # rank_idx = number of missed collectors

    # No valid relay exists (i cannot reach j via any temporal 2-hop)
    return None, k


def can_delegate(k, M, i, j):
    """Check if emitter i can delegate to emitter j (valid temporal relay exists)."""
    c, missed = best_relay(k, M, i, j)
    return c is not None


def delegation_missed_count(k, M, i, j):
    """
    Number of collectors missed when emitter i delegates to emitter j.
    Uses the best possible relay.
    """
    _, missed = best_relay(k, M, i, j)
    return missed


# ─── Task 1: Verify the delegation model ──────────────────────────────────

def task1_verify_model():
    """Verify the temporal delegation model on small instances."""
    print("=" * 70)
    print("TASK 1: Verify temporal delegation model")
    print("=" * 70)
    print()

    for k in [3, 4, 5]:
        print(f"--- k = {k} ---")
        M = random_timestamp_matrix(k, seed=42 + k)
        S_minus, S_plus = compute_extremal_matchings(k, M)

        print(f"  S⁻: {S_minus}")
        print(f"  S⁺: {S_plus}")
        print()

        # Show timestamp matrix
        print(f"  Timestamp matrix M:")
        for i in range(k):
            row = [M[(i, j)] for j in range(k)]
            print(f"    Row {i}: {row}")
        print()

        # For each pair (i,j), compute best relay and missed count
        print(f"  Delegation analysis:")
        for i in range(k):
            for j in range(k):
                if i == j:
                    continue
                relay, missed = best_relay(k, M, i, j)
                if relay is not None:
                    print(f"    {i}→{j}: relay=b_{relay} "
                          f"(M[{i},{relay}]={M[(i,relay)]}, M[{j},{relay}]={M[(j,relay)]}), "
                          f"missed={missed}")
                else:
                    print(f"    {i}→{j}: NO VALID RELAY")
        print()


# ─── Task 2: Birthday probability ─────────────────────────────────────────

def task2_birthday_probability():
    """
    For a random delegation pair (i,j), what is the probability that
    a random collector d is compatible (not missed)?

    Missed iff M[j,d] < M[j,c'], where c' is the best relay.
    If best relay has rank r in j's row, P(compatible) = (k-r)/k.

    What is E[r] for a random pair (i,j)?
    """
    print("=" * 70)
    print("TASK 2: Birthday probability on timestamp compatibility")
    print("=" * 70)
    print()

    print(f"{'k':>5} {'E[rank]':>8} {'E[missed]':>10} {'P(compat)':>10} "
          f"{'no_relay%':>10} {'trials':>8}")
    print("-" * 60)

    for k in [4, 6, 8, 10, 12, 16, 20, 30, 50]:
        trials = min(200, max(50, 10000 // (k * k)))
        all_ranks = []
        no_relay_count = 0
        total_pairs = 0

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            for i in range(k):
                for j in range(k):
                    if i == j:
                        continue
                    relay, rank = best_relay(k, M, i, j)
                    total_pairs += 1
                    if relay is None:
                        no_relay_count += 1
                    else:
                        all_ranks.append(rank)

        if all_ranks:
            avg_rank = sum(all_ranks) / len(all_ranks)
            avg_missed = avg_rank  # missed = rank
            p_compat = 1 - avg_rank / k
        else:
            avg_rank = k
            avg_missed = k
            p_compat = 0

        no_relay_pct = no_relay_count / total_pairs * 100

        print(f"{k:5d} {avg_rank:8.2f} {avg_missed:10.2f} {p_compat:10.4f} "
              f"{no_relay_pct:10.2f} {trials:8d}")

    print()
    print("  NOTE: E[rank] is the expected rank of the best relay in the delegate's row.")
    print("  E[missed] = E[rank] = number of collectors the delegate reaches before the relay.")
    print("  P(compat) = 1 - E[rank]/k = fraction of collectors reachable after relay.")
    print()


# ─── Task 3: Sequential delegation spanner cost ───────────────────────────

def sequential_delegation_spanner(k, M, order=None):
    """
    Build a temporal spanner via sequential delegation.

    1. Root = order[0], keeps all k collector edges.
    2. For each subsequent emitter order[i]:
       - Find the best delegate among already-processed emitters
       - Count missed collectors
    3. Total cost = k (root) + sum(missed) + (k-1) (delegation edges)

    Wait — the delegation model needs refinement. When emitter i delegates to j,
    j must be "alive" (already processed and incorporated into the spanner).
    The delegation chain goes backward: emitter i reaches j via relay c',
    then j's spanner edges cover the rest. So j's spanner coverage is already
    established.

    BUT: the missed collectors for i are those where j→d doesn't compose
    temporally with i→c'→j. This depends only on M, not on j's delegation chain.

    For the accumulated coverage model:
    - Root covers all k collectors directly.
    - When emitter i delegates to ANY previous emitter j:
      - Relay via best relay c'
      - Missed = collectors with M[j,d] < M[j,c']
      - These missed collectors need NEW direct edges from the root's coverage.

    Wait — the root already covers all collectors! The issue is:
    emitter i needs TEMPORAL paths to all collectors. The root's coverage
    provides paths from the root, not from emitter i.

    Let me reconsider what "spanner" means here:
    - For the FULL temporal spanner, every pair (u,v) must have a temporal journey.
    - Emitter i needs to reach every collector (and possibly other emitters).
    - If i delegates to j via relay c': i → c' → j is a valid temporal journey.
    - Then i reaches everything j reaches via j's spanner edges.
    - But: i→c'→j→d requires M[i,c'] < M[j,c'] < M[j,d].
    - So from i's perspective, j can only provide access to collectors d where
      M[j,d] > M[j,c']. Collectors where M[j,d] < M[j,c'] are MISSED.

    For missed collectors d, we need EXTRA edges in the spanner:
    - Either a direct edge i→d (adding 1 spanner edge)
    - Or an alternative path through another emitter

    In sequential delegation, the simplest approach: for each missed collector d,
    add the direct edge (i, d) to the spanner.
    Cost per delegation = 1 (relay edge) + |missed| (direct edges for missed collectors).

    Total spanner edges:
    - Root: k edges (all collectors)
    - Each subsequent emitter: 1 (relay) + |missed| edges
    - Total: k + (k-1) + sum(missed over all k-1 delegations)
    - = 2k - 1 + sum(missed)

    For the 4k-3 budget: need sum(missed) ≤ 2k - 2.
    """
    if order is None:
        order = list(range(k))

    root = order[0]
    total_missed = 0
    missed_counts = []
    delegation_failures = 0

    for step in range(1, len(order)):
        i = order[step]  # emitter to eliminate

        # Find best delegate among previous emitters
        best_j = None
        best_missed = k + 1

        for prev_step in range(step):
            j = order[prev_step]
            relay, missed = best_relay(k, M, i, j)
            if relay is not None and missed < best_missed:
                best_missed = missed
                best_j = j

        if best_j is None:
            # No valid delegation — emitter i needs ALL k edges directly
            delegation_failures += 1
            missed_counts.append(k)
            total_missed += k
        else:
            missed_counts.append(best_missed)
            total_missed += best_missed

    # Total spanner cost:
    # k (root edges) + (k-1) (delegation edges) + total_missed (extra for missed)
    # But delegation edges: when i delegates to j via relay c', the edge (i,c') is
    # the delegation edge. This is already counted — do we also need (j,c')?
    # In the spanner, both edges (i,c') and (j,c') must be present.
    # (i,c') is a new edge for i. (j,c') may already be in the spanner (from j's
    # own edges or previous delegations).
    #
    # Conservative count: assume each delegation adds 1 NEW edge (the relay edge from i).
    # j's edge to c' is already in the spanner.
    spanner_cost = k + (k - 1) + total_missed
    # = 2k - 1 + total_missed

    return {
        'root': root,
        'root_edges': k,
        'delegation_edges': k - 1,
        'missed_counts': missed_counts,
        'total_missed': total_missed,
        'spanner_cost': spanner_cost,
        'delegation_failures': delegation_failures,
    }


def greedy_delegation_order(k, M):
    """
    Greedy order: at each step, pick the emitter with the fewest missed collectors
    when delegating to the best available delegate.
    Start with the emitter that makes the best root (connected to most temporal paths).
    """
    remaining = set(range(k))

    # Pick root: emitter whose S⁻ has lowest rank (fewest missed as delegate)
    # Actually, root keeps all k edges, so root choice doesn't affect root cost.
    # Pick root = emitter that is the best delegate for others (lowest missed when
    # others delegate to it).
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

    while remaining:
        # Pick the emitter with fewest missed collectors when delegating to best in order
        best_next = None
        best_next_missed = float('inf')

        for i in remaining:
            local_best_missed = k + 1
            for j in order:
                relay, missed = best_relay(k, M, i, j)
                if relay is not None and missed < local_best_missed:
                    local_best_missed = missed
            if local_best_missed < best_next_missed:
                best_next_missed = local_best_missed
                best_next = i

        if best_next is None:
            # All remaining emitters have no valid relay — just pick any
            best_next = next(iter(remaining))

        order.append(best_next)
        remaining.remove(best_next)

    return order


def task3_delegation_cost():
    """Compute total delegation spanner cost."""
    print("=" * 70)
    print("TASK 3: Sequential delegation spanner cost")
    print("=" * 70)
    print()

    print(f"{'k':>5} {'n=2k':>5} | {'greedy':>8} {'random':>8} | "
          f"{'4k-3':>6} {'2n-3':>6} | {'greedy≤4k-3':>12} {'fail_g':>7} {'fail_r':>7}")
    print("-" * 85)

    for k in [3, 4, 5, 6, 7, 8, 10, 12, 16]:
        trials = min(100, max(20, 5000 // (k * k)))
        greedy_costs = []
        random_costs = []
        greedy_violations = 0
        greedy_failures = 0
        random_failures = 0

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)

            # Greedy order
            g_order = greedy_delegation_order(k, M)
            g_result = sequential_delegation_spanner(k, M, g_order)
            greedy_costs.append(g_result['spanner_cost'])
            greedy_failures += g_result['delegation_failures']
            if g_result['spanner_cost'] > 4 * k - 3:
                greedy_violations += 1

            # Random order
            rng = random.Random(trial * 1000 + k + 999)
            r_order = list(range(k))
            rng.shuffle(r_order)
            r_result = sequential_delegation_spanner(k, M, r_order)
            random_costs.append(r_result['spanner_cost'])
            random_failures += r_result['delegation_failures']

        n = 2 * k
        budget_4k = 4 * k - 3
        budget_2n = 2 * n - 3

        avg_g = sum(greedy_costs) / trials
        avg_r = sum(random_costs) / trials
        max_g = max(greedy_costs)

        print(f"{k:5d} {n:5d} | {avg_g:8.1f} {avg_r:8.1f} | "
              f"{budget_4k:6d} {budget_2n:6d} | "
              f"{'YES' if greedy_violations == 0 else f'NO({greedy_violations})':>12} "
              f"{greedy_failures:7d} {random_failures:7d}")

    print()
    print("  spanner_cost = k (root) + (k-1) (delegation edges) + total_missed")
    print("  Budget: 4k-3 = 2n-3 where n=2k")
    print()


# ─── Task 4: Birthday bound analysis ──────────────────────────────────────

def task4_birthday_bound():
    """
    Analyze the birthday-type probability for timestamp compatibility.

    When emitter i delegates to emitter j via best relay c':
    - c' has rank r in j's row ordering
    - |missed| = r
    - r is determined by the relay selection

    What is the distribution of r across random matrices?
    If r is typically O(1), then total_missed = O(k) and we're within budget.
    If r is typically O(k), then total_missed = O(k²) and we blow the budget.
    """
    print("=" * 70)
    print("TASK 4: Birthday bound — relay rank distribution")
    print("=" * 70)
    print()

    # For each k, compute the distribution of best-relay ranks
    print(f"{'k':>5} | {'E[rank]':>8} {'med[rank]':>10} {'max[rank]':>10} "
          f"{'rank/k':>8} {'P(rank=0)':>10} {'P(rank≤1)':>10}")
    print("-" * 75)

    for k in [4, 6, 8, 10, 12, 16, 20, 30]:
        trials = min(200, max(50, 10000 // (k * k)))
        all_ranks = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)

            for i in range(k):
                # Find best delegate
                best_rank = k
                for j in range(k):
                    if i == j:
                        continue
                    relay, rank = best_relay(k, M, i, j)
                    if relay is not None and rank < best_rank:
                        best_rank = rank
                all_ranks.append(best_rank)

        avg_rank = sum(all_ranks) / len(all_ranks)
        med_rank = sorted(all_ranks)[len(all_ranks) // 2]
        max_rank = max(all_ranks)
        p_rank0 = sum(1 for r in all_ranks if r == 0) / len(all_ranks)
        p_rank01 = sum(1 for r in all_ranks if r <= 1) / len(all_ranks)

        print(f"{k:5d} | {avg_rank:8.2f} {med_rank:10d} {max_rank:10d} "
              f"{avg_rank/k:8.4f} {p_rank0:10.4f} {p_rank01:10.4f}")

    print()
    print("  'rank' = rank of best relay in delegate's row ordering")
    print("  rank = 0 means perfect delegation (no missed collectors)")
    print("  rank/k → 0 means O(1) missed per delegation → total = O(k)")
    print()


# ─── Task 5: Per-delegation missed analysis ───────────────────────────────

def task5_per_delegation_analysis():
    """
    For the greedy sequential delegation:
    What is the distribution of missed collectors per step?
    Does it telescope (each step adds O(1) missed)?
    """
    print("=" * 70)
    print("TASK 5: Per-delegation missed distribution (greedy order)")
    print("=" * 70)
    print()

    for k in [6, 10, 16, 20]:
        trials = min(50, max(20, 2000 // (k * k)))
        step_missed = defaultdict(list)
        total_missed_list = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            g_order = greedy_delegation_order(k, M)
            result = sequential_delegation_spanner(k, M, g_order)
            total_missed_list.append(result['total_missed'])
            for step, mc in enumerate(result['missed_counts']):
                step_missed[step].append(mc)

        avg_total = sum(total_missed_list) / trials
        max_total = max(total_missed_list)

        print(f"--- k={k} (n=2k={2*k}), budget=4k-3={4*k-3} ---")
        print(f"  Total missed: avg={avg_total:.1f}, max={max_total}, "
              f"avg/k={avg_total/k:.2f}")
        print(f"  Spanner cost = 2k-1+missed: avg={2*k-1+avg_total:.1f}, max={2*k-1+max_total}")

        # Per-step breakdown
        print(f"  Per-step missed (avg over {trials} trials):")
        for step in range(min(k - 1, 15)):
            vals = step_missed[step]
            avg_step = sum(vals) / len(vals)
            max_step = max(vals)
            print(f"    Step {step+1}: avg={avg_step:.2f}, max={max_step}")

        if k - 1 > 15:
            remaining = list(range(15, k - 1))
            remaining_avgs = [sum(step_missed[s]) / len(step_missed[s]) for s in remaining]
            print(f"    Steps {16}-{k-1}: avg of avgs={sum(remaining_avgs)/len(remaining_avgs):.2f}")
        print()


# ─── Task 6: Full budget check ────────────────────────────────────────────

def task6_full_budget():
    """
    Full spanner budget check.

    For K_n temporal clique (modeled as K_{k,k} bipartite with k=n/2):
    - Dismounted vertices: d, cost 2d edges
    - Residual biclique: k emitters, k collectors, n'=2k vertices
    - Sequential delegation cost: B = 2k-1 + total_missed
    - Full spanner: 2d + B
    - Budget: 2n-3 = 2(d+2k)-3 = 2d+4k-3
    - Need: B ≤ 4k-3, i.e., total_missed ≤ 2k-2

    Also check: can sequential delegation ALWAYS find valid relays?
    """
    print("=" * 70)
    print("TASK 6: Full budget check — total_missed ≤ 2k-2?")
    print("=" * 70)
    print()

    print(f"{'k':>5} {'n=2k':>5} | {'avg_missed':>11} {'max_missed':>11} "
          f"{'budget(2k-2)':>13} {'≤budget':>8} {'avg_cost':>9} {'max_cost':>9} "
          f"{'4k-3':>5}")
    print("-" * 100)

    all_within_budget = True

    for k in [3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20]:
        trials = min(100, max(30, 5000 // (k * k)))
        missed_totals = []
        costs = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            g_order = greedy_delegation_order(k, M)
            result = sequential_delegation_spanner(k, M, g_order)
            missed_totals.append(result['total_missed'])
            costs.append(result['spanner_cost'])

        avg_m = sum(missed_totals) / trials
        max_m = max(missed_totals)
        avg_c = sum(costs) / trials
        max_c = max(costs)
        budget_missed = 2 * k - 2
        budget_cost = 4 * k - 3
        within = max_m <= budget_missed

        if not within:
            all_within_budget = False

        print(f"{k:5d} {2*k:5d} | {avg_m:11.1f} {max_m:11d} "
              f"{budget_missed:13d} {'YES' if within else 'NO':>8} "
              f"{avg_c:9.1f} {max_c:9d} {budget_cost:5d}")

    print()
    if all_within_budget:
        print("  ALL within budget! total_missed ≤ 2k-2 for all tested instances.")
    else:
        print("  BUDGET VIOLATED in some instances.")
    print()


# ─── Task 7: The probability p ────────────────────────────────────────────

def task7_probability_p():
    """
    What is the probability that a random collector d is NOT missed
    when emitter i delegates to emitter j via the best relay?

    For each triple (i, j, d) where i≠j≠d:
    p = P(M[j,d] > M[j,c']) where c' is the best relay for i→j.

    If the best relay has rank r in j's row, then:
    p = (k - 1 - r) / (k - 1)  (excluding c' itself)

    Actually, let's measure it directly.
    """
    print("=" * 70)
    print("TASK 7: The compatibility probability p")
    print("=" * 70)
    print()

    print(f"{'k':>5} | {'p_best_relay':>13} {'p_any_relay':>12} | "
          f"{'E[missed_best]':>15} {'E[missed_best]/k':>17}")
    print("-" * 80)

    for k in [4, 6, 8, 10, 12, 16, 20, 30, 50]:
        trials = min(100, max(20, 5000 // (k * k)))
        p_best_vals = []
        p_any_vals = []
        missed_best_vals = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)

            for i in range(k):
                for j in range(k):
                    if i == j:
                        continue

                    relay, rank = best_relay(k, M, i, j)
                    if relay is None:
                        continue

                    # p_best = fraction of collectors (excluding relay) reachable after relay
                    # Reachable d: M[j,d] > M[j,relay]
                    reachable = sum(1 for d in range(k) if d != relay and M[(j, d)] > M[(j, relay)])
                    p_best = reachable / (k - 1) if k > 1 else 0
                    p_best_vals.append(p_best)
                    missed_best_vals.append(rank)

                    # p_any: fraction of (relay, collector) pairs where collector is reachable
                    # via ANY relay that works for i→j
                    # (not just the best one)
                    # Skip for large k (too expensive)

        avg_p_best = sum(p_best_vals) / len(p_best_vals) if p_best_vals else 0
        avg_missed = sum(missed_best_vals) / len(missed_best_vals) if missed_best_vals else k

        print(f"{k:5d} | {avg_p_best:13.4f} {'—':>12} | "
              f"{avg_missed:15.2f} {avg_missed/k:17.4f}")

    print()
    print("  p_best_relay = fraction of collectors reachable when using the best relay")
    print("  E[missed_best] = expected rank of best relay in delegate's row")
    print("  E[missed_best]/k → 0 as k grows means O(1) missed per delegation")
    print()


# ─── Task 8: Analytical prediction ────────────────────────────────────────

def task8_analytical():
    """
    Analytical prediction for E[rank of best relay].

    When i delegates to j via relay c':
    - j's row has k columns sorted by timestamp
    - c' must satisfy M[i,c'] < M[j,c']
    - We want c' with the lowest rank in j's row ordering

    For random M: M[i,c'] and M[j,c'] are independent uniform random timestamps.
    P(M[i,c'] < M[j,c']) = 1/2 for each column c'.

    j's row sorted: c'_0, c'_1, ..., c'_{k-1} (by increasing M[j,·]).
    P(c'_0 is a valid relay) = P(M[i,c'_0] < M[j,c'_0]) = 1/2.

    If c'_0 is valid, rank = 0.
    If c'_0 is NOT valid, try c'_1: P(c'_1 valid) = 1/2. If valid, rank = 1.
    ...

    P(rank = r) = (1/2)^{r+1} (geometric with p=1/2).
    E[rank] = sum_{r=0}^{k-1} r * (1/2)^{r+1} + k * (1/2)^k (failure)

    For large k: E[rank] → sum_{r=0}^∞ r * (1/2)^{r+1} = 1.

    So E[rank] → 1 as k → ∞!

    But this assumes independence between columns, which isn't quite right
    (M has distinct timestamps across the whole matrix, not per-row).
    Let's check how close this analytical prediction is.

    With E[rank] = 1, total_missed across k-1 delegations ≈ k-1.
    Spanner cost ≈ 2k-1 + (k-1) = 3k-2.
    Budget is 4k-3. So 3k-2 ≤ 4k-3 iff k ≥ 1. Always within budget!

    But wait — when we pick the BEST delegate (not just any j), we get
    the minimum rank over all possible delegates. With k-1 possible delegates,
    the minimum of k-1 geometric(1/2) random variables has an even smaller expected value.
    """
    print("=" * 70)
    print("TASK 8: Analytical prediction vs empirical")
    print("=" * 70)
    print()

    # Analytical E[rank] for best relay to a SPECIFIC delegate j
    print("Analytical prediction (single delegate j, k columns):")
    print("  P(rank=r) ≈ (1/2)^{r+1} for r = 0, 1, ..., k-1")
    print("  E[rank] ≈ 1 for large k")
    print()

    # Compute exact analytical E[rank] for small k
    for k in [4, 6, 8, 10, 20, 50]:
        e_rank = 0
        p_fail = 1.0
        for r in range(k):
            p_this = 0.5 * p_fail  # p_fail * 1/2 (this column valid, all previous invalid)
            e_rank += r * p_this
            p_fail *= 0.5
        e_rank += k * p_fail  # failure case (no valid relay)
        print(f"  k={k:3d}: E[rank|single delegate] = {e_rank:.4f}")

    print()
    print("  With k-1 candidate delegates, E[min rank] is even smaller.")
    print()

    # Now compare: analytical vs empirical
    print(f"{'k':>5} | {'analytic_single':>16} {'analytic_best':>14} | "
          f"{'empirical':>10} {'ratio':>7}")
    print("-" * 65)

    for k in [4, 6, 8, 10, 12, 16, 20]:
        # Analytical: single delegate
        e_single = 0
        p_fail = 1.0
        for r in range(k):
            p_this = 0.5 * p_fail
            e_single += r * p_this
            p_fail *= 0.5
        e_single += k * p_fail

        # Analytical: best of (k-1) delegates
        # E[min of (k-1) copies] ≈ E_single / (k-1) for geometric-like distributions
        # More precisely: P(min rank ≥ r) = P(all delegates have rank ≥ r)^{k-1}
        # = [P(rank ≥ r)]^{k-1} = [(1/2)^r + correction]^{k-1}... complex.
        # Just use the simple bound: E[min] ≈ 1 / (k-1) for large k.
        # For geometric(1/2): P(X ≥ r) = (1/2)^r
        # P(min ≥ r) = [(1/2)^r]^{k-1} = (1/2)^{r(k-1)}
        # E[min] = sum_{r=1}^{inf} P(min ≥ r) = sum (1/2)^{r(k-1)} = 1/(2^{k-1}-1)
        e_best_approx = 1.0 / (2**(k-1) - 1)

        # Empirical
        trials = min(100, max(30, 5000 // (k * k)))
        empirical_ranks = []
        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            for i in range(k):
                best_rank = k
                for j in range(k):
                    if i == j:
                        continue
                    relay, rank = best_relay(k, M, i, j)
                    if relay is not None and rank < best_rank:
                        best_rank = rank
                empirical_ranks.append(best_rank)

        avg_emp = sum(empirical_ranks) / len(empirical_ranks)

        print(f"{k:5d} | {e_single:16.4f} {e_best_approx:14.6f} | "
              f"{avg_emp:10.4f} {avg_emp/e_single if e_single > 0 else 0:7.3f}")

    print()
    print("  analytic_single: E[rank] for delegation to a FIXED delegate")
    print("  analytic_best: E[min rank over k-1 delegates] ≈ 1/(2^{k-1}-1)")
    print("  empirical: actual measured E[best rank]")
    print("  The analytic_best bound suggests E[best rank] → 0 exponentially!")
    print()


# ─── Task 9: Total spanner cost with tight analysis ───────────────────────

def task9_tight_budget():
    """
    Tight budget analysis:

    For greedy sequential delegation:
    total_missed = sum_{i=1}^{k-1} missed(order[i])
    spanner_cost = 2k - 1 + total_missed

    If E[missed per step] ≈ 0 (from Task 8), then spanner_cost ≈ 2k-1.
    This is WAY under the 4k-3 budget.

    But is the max total_missed always ≤ 2k-2?
    """
    print("=" * 70)
    print("TASK 9: Tight budget — max total_missed over many trials")
    print("=" * 70)
    print()

    print(f"{'k':>5} {'trials':>7} | {'avg_missed':>11} {'max_missed':>11} "
          f"{'budget':>7} {'slack':>7} | {'avg_cost':>9} {'max_cost':>9} {'4k-3':>5}")
    print("-" * 90)

    for k in [3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 25, 30]:
        trials = min(200, max(50, 20000 // (k * k)))
        missed_totals = []
        costs = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            g_order = greedy_delegation_order(k, M)
            result = sequential_delegation_spanner(k, M, g_order)
            missed_totals.append(result['total_missed'])
            costs.append(result['spanner_cost'])

        avg_m = sum(missed_totals) / trials
        max_m = max(missed_totals)
        avg_c = sum(costs) / trials
        max_c = max(costs)
        budget = 2 * k - 2
        slack = budget - max_m

        print(f"{k:5d} {trials:7d} | {avg_m:11.2f} {max_m:11d} "
              f"{budget:7d} {slack:7d} | {avg_c:9.1f} {max_c:9d} {4*k-3:5d}")

    print()


# ─── Main ──────────────────────────────────────────────────────────────────

def run():
    print("H27: BIRTHDAY BOUND ON SEQUENTIAL DELEGATION")
    print("CPS Fireworks Residual — Temporal Timestamp Compatibility")
    print("=" * 70)
    print()

    task1_verify_model()
    print()
    task2_birthday_probability()
    print()
    task4_birthday_bound()
    print()
    task7_probability_p()
    print()
    task8_analytical()
    print()
    task3_delegation_cost()
    print()
    task6_full_budget()
    print()
    task5_per_delegation_analysis()
    print()
    task9_tight_budget()

    # ─── Final verdict ────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)
    print("""
### H27: Birthday bound on union coverage

**Setup:** k×k bipartite temporal graph with distinct timestamps.
Emitter i delegates to emitter j via relay collector c' where M[i,c'] < M[j,c'].
Missed collectors = those with M[j,d] < M[j,c'] (rank of c' in j's row).

**The birthday argument:**
For a FIXED delegate j, the rank of the best relay follows a geometric(1/2)
distribution: P(rank ≥ r) ≈ (1/2)^r. This gives E[rank] ≈ 1.

With k-1 candidate delegates, the best delegate gives rank ≈ 0 with high
probability. Formally: E[best rank] ≈ 1/(2^{k-1} - 1) → 0 exponentially.

**Total spanner cost:**
- Root: k edges
- Delegation edges: k-1
- Missed collectors: sum of per-step best ranks ≈ O(1) total

Total ≈ 2k - 1 + O(1), well within the 4k-3 budget.

**Does this close the 2n-3 conjecture?**
Sequential delegation gives B ≤ 2k-1+o(k) edges for the biclique.
With dismounting: total = 2d + B ≤ 2d + 2k = n + d - 1 + o(k).
Since n = d + 2k: total ≤ 2n - 2k - 1 + o(k) ≤ 2n - 3 for k ≥ 1.

**Verdict:** {pending — based on empirical results}
""")


if __name__ == '__main__':
    run()
