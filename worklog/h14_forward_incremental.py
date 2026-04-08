"""
H14: Forward-transitive incremental construction for temporal spanners.

Core idea: process edges in timestamp order, maintain reachability matrix,
keep an edge iff it creates at least one new reachable pair.
Phase 2: backward prune removes edges that became redundant.

Measures: correctness, edge count, precise operation counts, wall clock time.
"""

import random
import time
import statistics
from collections import defaultdict
import heapq
import sys

# ─── Core utilities ───

def random_matrix(k):
    vals = list(range(1, k * k + 1))
    random.shuffle(vals)
    return [vals[i * k:(i + 1) * k] for i in range(k)]

def matrix_to_edges(k, M):
    return [(i, k + j, M[i][j]) for i in range(k) for j in range(k)]

def build_adj(k, edges):
    adj = defaultdict(list)
    for (a, b, t) in edges:
        adj[a].append((b, t))
        adj[b].append((a, t))
    return adj

def temporal_reachable_from(source, adj):
    best = {source: -1}  # source reachable at time -1 (before all edges)
    queue = [(-1, source)]
    while queue:
        t_arr, u = heapq.heappop(queue)
        if t_arr > best.get(u, float('inf')):
            continue
        for (v, t_edge) in adj[u]:
            if t_edge >= t_arr:
                if t_edge < best.get(v, float('inf')):
                    best[v] = t_edge
                    heapq.heappush(queue, (t_edge, v))
    return best

def all_pairs_earliest(k, edges):
    """Return dict: (u,v) -> earliest arrival time, or inf if unreachable."""
    adj = build_adj(k, edges)
    n = 2 * k
    reach = {}
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        for d in range(n):
            reach[(s, d)] = r.get(d, float('inf'))
    return reach

def is_fully_reachable(k, edges):
    """Check if all pairs (u,v) with u!=v are temporally reachable."""
    adj = build_adj(k, edges)
    n = 2 * k
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        if len(r) < n:
            return False
    return True

def count_reachable_pairs(k, edges):
    """Count number of reachable pairs (u,v) with u!=v."""
    adj = build_adj(k, edges)
    n = 2 * k
    total = 0
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        total += len(r) - 1  # exclude self
    return total


# ─── H14: Forward incremental construction ───

def forward_incremental(k, M, stats=None):
    """
    Phase 1: Process edges in timestamp order, keep if creates new reachable pair.

    Returns: set of kept edges, stats dict with operation counts.
    """
    if stats is None:
        stats = {}

    n = 2 * k
    INF = float('inf')

    # Initialize reach matrix: reach[u][v] = earliest time u can reach v
    # using only kept edges
    reach = [[INF] * n for _ in range(n)]
    for i in range(n):
        reach[i][i] = -1  # self-reachable before any time

    # All edges sorted by timestamp
    edges = matrix_to_edges(k, M)
    edges.sort(key=lambda e: e[2])

    kept = []
    skipped = 0

    # Operation counters
    lookup_count = 0
    update_count = 0
    total_pairs_touched = 0
    pairs_per_kept_edge = []

    for (a, b, t) in edges:
        # Phase 1 QUERY: does this edge create any new reachable pair?
        # S = vertices that can reach a by time t (in current spanner)
        # T = vertices reachable from b (in current spanner) at time >= t
        #
        # For u in S, v in T: if reach[u][v] == INF, this edge is useful

        S = []
        for u in range(n):
            lookup_count += 1
            if reach[u][a] <= t:  # u can reach a by time t
                S.append(u)

        T = []
        for v in range(n):
            lookup_count += 1
            if reach[b][v] < INF:  # b can reach v at some time
                T.append(v)

        # Check for new pairs
        new_pairs = 0
        for u in S:
            for v in T:
                lookup_count += 1
                if reach[u][v] == INF:
                    new_pairs += 1

        if new_pairs == 0:
            skipped += 1
            continue

        # KEEP this edge
        kept.append((a, b, t))
        pairs_per_kept_edge.append(new_pairs)

        # UPDATE: for each u in S, for each v in T, update reach[u][v]
        # New arrival time at v via this edge = max(t, reach[b][v])
        # But reach[b][v] might be updated during this loop, so pre-compute T info

        # Pre-compute arrival times from b (before this update)
        b_reach = [(v, reach[b][v]) for v in T]

        # Also: after taking edge (a,b) at time t, we arrive at b at time t
        # Then from b we can reach v at time reach[b][v] (but only if reach[b][v] >= t)
        # The arrival time at v = reach[b][v] if reach[b][v] >= t, else not reachable via this path
        # Wait — reach[b][v] already accounts for the earliest time to get from b to v.
        # If reach[b][v] < t, that means b→v uses edges with timestamps < t.
        # But we arrive at b at time t, so we need edges from b at time >= t.
        #
        # CORRECTION: reach[b][v] is the earliest ARRIVAL time at v starting from b.
        # If reach[b][v] >= t, then the journey b→v uses edges at time >= reach[b][b_next] >= ...
        # But reach[b][v] could be achieved via a path that starts at time < t!
        # We need: earliest arrival at v from b using only edges at time >= t.
        #
        # This is MORE COMPLEX than the simple matrix suggests.
        # The reach matrix stores earliest arrival, not "earliest arrival given departure >= t".
        #
        # SIMPLIFICATION: Since reach[b][v] = earliest arrival at v from b,
        # if reach[b][v] >= t, then there exists a journey from b to v where
        # the first edge has timestamp >= ... hmm, no. The first edge could be < t.
        #
        # Actually wait. reach[b][b] = -1 (self). For v != b:
        # reach[b][v] = earliest time we arrive at v starting from b at time -1.
        # This uses edges from time -1 onwards (i.e., any edge).
        # But we arrive at b at time t, so we need edges starting from time t.
        #
        # We need a DEPARTURE-CONDITIONAL reach matrix.
        # reach_from[b][v] given departure time t is NOT the same as reach[b][v].

        # REVISED APPROACH: Use a proper departure-conditional query.
        # For the update, we need: for each u in S, u reaches b at time
        # max(reach[u][a], t) = t (since reach[u][a] <= t).
        # Actually u reaches a at reach[u][a], then takes edge (a,b) at time t
        # (since t >= reach[u][a]), arriving at b at time t.
        # Then from b at time t, we can reach v if there's a temporal journey
        # from b to v using only edges at time >= t IN THE CURRENT SPANNER.

        # So we need: forward_reach_from(b, t, current_spanner)
        # This is a BFS/Dijkstra from b restricted to edges >= t.

        # For efficiency, let's just recompute reachability from b at time t
        # using only kept edges (including this one).

        # Actually, let's think about this differently.
        # The reach matrix should store: reach[u][v] = earliest ARRIVAL time at v from u.
        # When we add edge (a,b,t):
        # - For u reaching a by time t: u reaches b at time t
        # - From b at time t, using EXISTING kept edges at time >= t, u reaches further vertices
        # - The existing reach[b][v] was computed with departure time -inf from b
        #   but we need departure time t from b

        # Let me just do a forward BFS from b at time t using kept edges.
        # This is correct and the cost is bounded.

        # Build adjacency from kept edges (including this new one)
        # Actually, the new edge (a,b,t) only helps a→b direction.
        # From b, we use previously kept edges.

        adj_kept = defaultdict(list)
        for (ea, eb, et) in kept:  # includes the new edge
            adj_kept[ea].append((eb, et))
            # Edges are directed a_i → b_j in temporal bipartite graphs?
            # No — temporal reachability is over undirected edges with non-decreasing timestamps.
            adj_kept[eb].append((ea, et))

        # BFS from b at time t
        best_from_b = {b: t}
        queue = [(t, b)]
        while queue:
            t_arr, node = heapq.heappop(queue)
            if t_arr > best_from_b.get(node, INF):
                continue
            for (nxt, t_edge) in adj_kept[node]:
                if t_edge >= t_arr:
                    if t_edge < best_from_b.get(nxt, INF):
                        best_from_b[nxt] = t_edge
                        heapq.heappush(queue, (t_edge, nxt))

        # Now update reach matrix
        pairs_touched = 0
        for u in S:
            for v, arr_v in best_from_b.items():
                update_count += 1
                if arr_v < reach[u][v]:
                    reach[u][v] = arr_v
                    pairs_touched += 1

        total_pairs_touched += pairs_touched

    stats['phase1_kept'] = len(kept)
    stats['phase1_skipped'] = skipped
    stats['lookup_count'] = lookup_count
    stats['update_count'] = update_count
    stats['total_pairs_touched'] = total_pairs_touched
    stats['pairs_per_kept_edge'] = pairs_per_kept_edge

    return kept, stats


def backward_prune(k, kept_edges, stats=None):
    """
    Phase 2: Process kept edges in REVERSE timestamp order.
    Remove edge if it doesn't break any reachable pair.
    """
    if stats is None:
        stats = {}

    n = 2 * k
    # Sort by timestamp descending
    ordered = sorted(kept_edges, key=lambda e: -e[2])

    final = set(map(tuple, kept_edges))
    removals = 0

    # Get full reachability from phase 1 result
    full_reach = all_pairs_earliest(k, list(final))

    for edge in ordered:
        trial = final - {edge}
        trial_reach = all_pairs_earliest(k, list(trial))

        # Check: does removing this edge break any reachable pair?
        broken = False
        for s in range(n):
            for d in range(n):
                if s == d:
                    continue
                if full_reach[(s, d)] < float('inf') and trial_reach[(s, d)] == float('inf'):
                    broken = True
                    break
            if broken:
                break

        if not broken:
            final = trial
            removals += 1

    stats['phase2_removals'] = removals
    stats['phase2_final'] = len(final)

    return list(final), stats


# ─── Greedy offline (best-response) for comparison ───

def greedy_offline(k, M, n_trials=5):
    """Greedy removal from full edge set, multiple random orderings."""
    all_e = list(matrix_to_edges(k, M))
    orig = all_pairs_earliest(k, all_e)
    n = 2 * k

    best_set = None
    for _ in range(n_trials):
        random.shuffle(all_e)
        cur = set(map(tuple, all_e))
        for e in all_e:
            if e not in cur:
                continue
            trial = cur - {e}
            trial_reach = all_pairs_earliest(k, list(trial))
            ok = True
            for s in range(n):
                for d in range(n):
                    if s == d:
                        continue
                    if orig[(s, d)] < float('inf') and trial_reach[(s, d)] == float('inf'):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                cur = trial
        if best_set is None or len(cur) < len(best_set):
            best_set = cur
    return list(best_set)


# ─── Best-response (H10) for comparison ───

def best_response(k, M, max_rounds=50):
    """H10-style best-response dynamics."""
    all_e = list(matrix_to_edges(k, M))
    orig = all_pairs_earliest(k, all_e)
    n = 2 * k
    cur = set(map(tuple, all_e))

    for _ in range(max_rounds):
        changed = False
        el = list(cur)
        random.shuffle(el)
        for e in el:
            if e not in cur:
                continue
            trial = cur - {e}
            trial_reach = all_pairs_earliest(k, list(trial))
            ok = True
            for s in range(n):
                for d in range(n):
                    if s == d:
                        continue
                    if orig[(s, d)] < float('inf') and trial_reach[(s, d)] == float('inf'):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                cur = trial
                changed = True
        if not changed:
            break
    return list(cur)


# ─── Main experiment ───

def run_experiment():
    random.seed(42)

    K_VALUES = [3, 4, 5, 6, 7, 8, 10]
    N_MATRICES = 50

    print("=" * 80)
    print("H14: Forward Incremental Construction — Temporal Spanner Experiment")
    print("=" * 80)

    all_results = {}

    for k in K_VALUES:
        print(f"\n{'─' * 60}")
        print(f"k = {k}  (n = {2*k}, budget 4k-3 = {4*k-3}, k^2 = {k*k} edges)")
        print(f"{'─' * 60}")

        budget = 4 * k - 3
        n = 2 * k
        total_pairs = n * (n - 1)

        results = {
            'k': k,
            'phase1_edges': [],
            'phase2_edges': [],
            'greedy_edges': [],
            'h10_edges': [],
            'phase1_correct': 0,
            'phase2_correct': 0,
            'phase1_times': [],
            'phase2_times': [],
            'greedy_times': [],
            'h10_times': [],
            'lookup_counts': [],
            'update_counts': [],
            'pairs_touched': [],
            'pairs_per_edge': [],
            'matrices_tried': 0,
            'matrices_reachable': 0,
        }

        count = 0
        attempts = 0

        while count < N_MATRICES:
            attempts += 1
            if attempts > N_MATRICES * 20:
                print(f"  WARNING: gave up after {attempts} attempts, got {count}/{N_MATRICES}")
                break

            M = random_matrix(k)
            edges = matrix_to_edges(k, M)

            if not is_fully_reachable(k, edges):
                continue

            results['matrices_tried'] = attempts
            results['matrices_reachable'] += 1
            count += 1

            # Phase 1: Forward incremental
            stats = {}
            t0 = time.time()
            kept, stats = forward_incremental(k, M, stats)
            t1 = time.time()
            phase1_time = t1 - t0

            # Check correctness
            p1_pairs = count_reachable_pairs(k, kept)
            p1_correct = (p1_pairs == total_pairs)
            if p1_correct:
                results['phase1_correct'] += 1

            results['phase1_edges'].append(len(kept))
            results['phase1_times'].append(phase1_time)
            results['lookup_counts'].append(stats['lookup_count'])
            results['update_counts'].append(stats['update_count'])
            results['pairs_touched'].append(stats['total_pairs_touched'])
            results['pairs_per_edge'].append(stats['pairs_per_kept_edge'])

            # Phase 2: Backward prune
            t0 = time.time()
            final, stats = backward_prune(k, kept, stats)
            t1 = time.time()
            phase2_time = t1 - t0

            p2_pairs = count_reachable_pairs(k, final)
            p2_correct = (p2_pairs == total_pairs)
            if p2_correct:
                results['phase2_correct'] += 1

            results['phase2_edges'].append(len(final))
            results['phase2_times'].append(phase2_time)

            # Greedy offline (only for small k due to cost)
            if k <= 8:
                t0 = time.time()
                greedy_set = greedy_offline(k, M, n_trials=3)
                t1 = time.time()
                results['greedy_edges'].append(len(greedy_set))
                results['greedy_times'].append(t1 - t0)

            # H10 best-response (only for small k)
            if k <= 8:
                t0 = time.time()
                h10_set = best_response(k, M, max_rounds=10)
                t1 = time.time()
                results['h10_edges'].append(len(h10_set))
                results['h10_times'].append(t1 - t0)

            if count % 10 == 0:
                print(f"  [{count}/{N_MATRICES}] P1={len(kept)} edges, "
                      f"P2={len(final)}, correct={p1_correct}/{p2_correct}")

        all_results[k] = results

        # Summary for this k
        print(f"\n  Reachability filter: {results['matrices_reachable']}/{results['matrices_tried']} "
              f"({100*results['matrices_reachable']/max(1,results['matrices_tried']):.0f}%)")
        print(f"  Phase 1 correctness: {results['phase1_correct']}/{count} "
              f"({100*results['phase1_correct']/max(1,count):.0f}%)")
        print(f"  Phase 2 correctness: {results['phase2_correct']}/{count} "
              f"({100*results['phase2_correct']/max(1,count):.0f}%)")

        p1_mean = statistics.mean(results['phase1_edges'])
        p1_med = statistics.median(results['phase1_edges'])
        p2_mean = statistics.mean(results['phase2_edges'])
        p2_med = statistics.median(results['phase2_edges'])

        print(f"  Phase 1 edges: mean={p1_mean:.1f}, median={p1_med:.0f}, "
              f"budget={budget}")
        print(f"  Phase 2 edges: mean={p2_mean:.1f}, median={p2_med:.0f}")

        if results['greedy_edges']:
            g_mean = statistics.mean(results['greedy_edges'])
            print(f"  Greedy offline: mean={g_mean:.1f}")
        if results['h10_edges']:
            h_mean = statistics.mean(results['h10_edges'])
            print(f"  H10 best-resp: mean={h_mean:.1f}")

        # Operation counts
        lk_mean = statistics.mean(results['lookup_counts'])
        up_mean = statistics.mean(results['update_counts'])
        pt_mean = statistics.mean(results['pairs_touched'])

        print(f"  Lookups: mean={lk_mean:.0f}")
        print(f"  Updates: mean={up_mean:.0f}")
        print(f"  Pairs touched: mean={pt_mean:.0f}")

        # Timing
        t1_mean = statistics.mean(results['phase1_times'])
        t2_mean = statistics.mean(results['phase2_times'])
        print(f"  Phase 1 time: mean={t1_mean*1000:.1f}ms")
        print(f"  Phase 2 time: mean={t2_mean*1000:.1f}ms")
        if results['greedy_times']:
            tg_mean = statistics.mean(results['greedy_times'])
            print(f"  Greedy time:  mean={tg_mean*1000:.1f}ms")
        if results['h10_times']:
            th_mean = statistics.mean(results['h10_times'])
            print(f"  H10 time:     mean={th_mean*1000:.1f}ms")

    # ─── Cross-k analysis ───
    print("\n" + "=" * 80)
    print("CROSS-K ANALYSIS")
    print("=" * 80)

    print(f"\n{'k':>3} {'n':>4} {'4k-3':>5} {'P1mean':>7} {'P2mean':>7} "
          f"{'Greedy':>7} {'H10':>7} {'P1corr':>7} {'P2corr':>7}")
    print("-" * 70)

    ks = []
    p1_means = []
    p2_means = []
    p1_times_all = []
    lookup_means = []
    update_means = []
    touch_means = []

    for k in K_VALUES:
        r = all_results[k]
        p1m = statistics.mean(r['phase1_edges'])
        p2m = statistics.mean(r['phase2_edges'])
        gm = statistics.mean(r['greedy_edges']) if r['greedy_edges'] else -1
        hm = statistics.mean(r['h10_edges']) if r['h10_edges'] else -1
        p1c = f"{100*r['phase1_correct']/max(1,len(r['phase1_edges'])):.0f}%"
        p2c = f"{100*r['phase2_correct']/max(1,len(r['phase2_edges'])):.0f}%"

        print(f"{k:>3} {2*k:>4} {4*k-3:>5} {p1m:>7.1f} {p2m:>7.1f} "
              f"{gm:>7.1f} {hm:>7.1f} {p1c:>7} {p2c:>7}")

        ks.append(k)
        p1_means.append(p1m)
        p2_means.append(p2m)
        p1_times_all.append(statistics.mean(r['phase1_times']))
        lookup_means.append(statistics.mean(r['lookup_counts']))
        update_means.append(statistics.mean(r['update_counts']))
        touch_means.append(statistics.mean(r['pairs_touched']))

    # Power law fits
    import math

    print("\n--- Power Law Fits ---")

    def fit_power(xs, ys, label):
        """Fit y = c * x^alpha via log-log regression."""
        if len(xs) < 2:
            return
        lx = [math.log(x) for x in xs]
        ly = [math.log(max(y, 1e-12)) for y in ys]
        n = len(lx)
        mx = sum(lx) / n
        my = sum(ly) / n
        num = sum((lx[i] - mx) * (ly[i] - my) for i in range(n))
        den = sum((lx[i] - mx) ** 2 for i in range(n))
        if den == 0:
            return
        alpha = num / den
        log_c = my - alpha * mx
        c = math.exp(log_c)
        # R^2
        ss_res = sum((ly[i] - (log_c + alpha * lx[i])) ** 2 for i in range(n))
        ss_tot = sum((ly[i] - my) ** 2 for i in range(n))
        r2 = 1 - ss_res / max(ss_tot, 1e-12)
        print(f"  {label}: y = {c:.4g} * k^{alpha:.2f}  (R^2={r2:.4f})")
        return alpha

    fit_power(ks, p1_means, "Phase 1 edges")
    fit_power(ks, p2_means, "Phase 2 edges")
    fit_power(ks, p1_times_all, "Phase 1 wall time")
    fit_power(ks, lookup_means, "Lookups")
    fit_power(ks, update_means, "Updates")
    fit_power(ks, touch_means, "Pairs touched")

    # Amortized cost per kept edge
    print("\n--- Amortized Cost per Kept Edge ---")
    print(f"{'k':>3} {'kept':>6} {'lookups/kept':>13} {'updates/kept':>13} {'touch/kept':>11}")
    for k in K_VALUES:
        r = all_results[k]
        ke = statistics.mean(r['phase1_edges'])
        lk = statistics.mean(r['lookup_counts'])
        up = statistics.mean(r['update_counts'])
        pt = statistics.mean(r['pairs_touched'])
        print(f"{k:>3} {ke:>6.1f} {lk/max(ke,1):>13.1f} {up/max(ke,1):>13.1f} {pt/max(ke,1):>11.1f}")

    # Edge overlap with H10
    if all(all_results[k]['h10_edges'] for k in K_VALUES if k <= 8):
        print("\n--- Edge Count Comparison (Phase 2 vs H10) ---")
        print(f"{'k':>3} {'P2':>6} {'H10':>6} {'ratio':>7}")
        for k in K_VALUES:
            r = all_results[k]
            if r['h10_edges']:
                p2m = statistics.mean(r['phase2_edges'])
                hm = statistics.mean(r['h10_edges'])
                print(f"{k:>3} {p2m:>6.1f} {hm:>6.1f} {p2m/max(hm,1):>7.3f}")

    # Distributed interpretation
    print("\n--- Distributed Interpretation ---")
    print("Forward incremental processes edges in global timestamp order.")
    print("Each edge decision requires querying the reachability matrix (shared state).")
    print("The matrix is updated only when an edge is kept.")
    print("For distributed execution:")
    print("  - Edges at different timestamps are SEQUENTIAL (must process in order)")
    print("  - But: could batch edges at 'nearby' timestamps with bounded staleness")
    print("  - Each node knows its own edges. Local state: which of MY edges are kept.")
    print("  - Shared state: n x n reachability matrix (O(k^2) entries)")
    print("  - Broadcast cost per kept edge: O(k) new pairs to announce")
    print("  - Total broadcast: O(k^2 log k) if O(k log k) edges kept, O(k) pairs each")


if __name__ == '__main__':
    run_experiment()
