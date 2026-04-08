"""
H14 v2: Fixed forward incremental construction.

Key insight from v1 failure: The reach matrix was not building up transitivity
because S (vertices reaching a_i) was almost always just {a_i} itself.
The issue: in a bipartite temporal clique, to reach a_i from some other vertex u,
u must first go to some b_k (using an earlier edge), then from b_k to a_i
(using a later edge). But the b_k -> a_i edge might not be kept yet!

The reach matrix IS updated correctly — the problem is structural:
in a complete bipartite graph with all-distinct timestamps, each
a_i -> b_j pair has EXACTLY ONE direct edge. Even with transitivity,
early in the process the matrix is too sparse for indirect paths to exist.

REVISED ALGORITHM: Instead of checking for NEW reachable pairs,
check if the pair (a_i, b_j) is ALREADY reachable. If a_i can reach b_j
via the current spanner (indirectly through other vertices), skip the edge.

This is the correct formulation: keep an edge iff it makes a currently-
unreachable DIRECT pair reachable (but the pair might be reachable indirectly).

Actually, the issue is more subtle. The spanner needs to preserve ALL-PAIRS
reachability, not just direct-neighbor pairs. An edge can be skipped if
ALL the new reachability it would provide is already covered.

Let me reconsider: the original algorithm IS correct — it just keeps all edges
because every edge does create a genuinely new reachable pair. The forward
construction with "keep if new pair" is too conservative.

NEW APPROACH: Forward construction with REACHABILITY PRESERVATION.
Instead of "does this edge create a new pair", ask:
"is the pair (u,v) reachable WITHOUT this edge, for ALL pairs?"

But that's backward pruning, not forward construction.

TRUE FORWARD INCREMENTAL: Process in timestamp order. Keep an edge iff
it is NECESSARY for some pair's reachability in the FINAL graph.
But we don't know the final graph yet...

APPROACH 3: Forward construction with lookahead.
Process in timestamp order. Maintain "reach matrix of full graph"
as reference. Keep an edge only if it's the EARLIEST edge that
can establish some pair's connection.

Actually, let's try a different criterion:
Keep edge (a_i, b_j, t) iff:
- There exists a pair (u, v) such that the ONLY temporal path from u to v
  that uses edges with timestamp <= t goes through this edge.

This is hard to check. Let me try a simpler greedy:

FORWARD GREEDY (correct version):
Process edges in timestamp order. For each edge:
- Temporarily add it to the spanner
- Check: does it increase the reachable pair count?
  (Not just "new pairs from S x T" but actual temporal BFS reachable pairs)
- If yes: keep. If no: skip.

The difference from v1: v1's "new pairs" check was actually correct but
the transitive closure update was wrong! Let me re-examine...

Actually wait. In v1, INF entries remaining was 40 out of 56 for k=4.
That means even with ALL 16 edges kept, only 16 out of 56 pairs are
reached? That can't be right if the matrix is fully reachable...

The issue must be in the reach matrix update. Let me verify.
"""

import random
import time
import statistics
from collections import defaultdict
import heapq
import math

def random_matrix(k):
    vals = list(range(1, k * k + 1))
    random.shuffle(vals)
    return [vals[i * k:(i + 1) * k] for i in range(k)]

def matrix_to_edges(k, M):
    return [(i, k + j, M[i][j]) for i in range(k) for j in range(k)]

def build_adj(edges):
    adj = defaultdict(list)
    for (a, b, t) in edges:
        adj[a].append((b, t))
        adj[b].append((a, t))
    return adj

def temporal_reach_from(source, adj, depart_time=-1):
    """BFS/Dijkstra from source, edges must have timestamp >= depart_time."""
    best = {source: depart_time}
    queue = [(depart_time, source)]
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

def count_reachable(k, edges):
    adj = build_adj(edges)
    n = 2 * k
    total = 0
    for s in range(n):
        r = temporal_reach_from(s, adj)
        total += len(r) - 1
    return total

def is_fully_reachable(k, edges):
    adj = build_adj(edges)
    n = 2 * k
    for s in range(n):
        r = temporal_reach_from(s, adj)
        if len(r) < n:
            return False
    return True

def all_pairs_earliest(k, edges):
    adj = build_adj(edges)
    n = 2 * k
    reach = {}
    for s in range(n):
        r = temporal_reach_from(s, adj)
        for d in range(n):
            reach[(s, d)] = r.get(d, float('inf'))
    return reach


def forward_incremental_v2(k, M, stats=None):
    """
    Forward incremental: process edges in timestamp order.
    Keep edge iff it increases the reachable pair count.
    Uses full temporal BFS to check — correct but O(k^2) per edge check.

    Total: O(k^2 * k^2 * k) = O(k^5) per matrix.
    """
    if stats is None:
        stats = {}

    n = 2 * k
    total_target = n * (n - 1)

    edges = matrix_to_edges(k, M)
    edges.sort(key=lambda e: e[2])

    kept = []
    current_pairs = 0
    skipped = 0
    bfs_count = 0  # number of full reachability checks

    for (a, b, t) in edges:
        # Check if adding this edge increases reachable pairs
        trial = kept + [(a, b, t)]
        bfs_count += 1
        trial_pairs = count_reachable(k, trial)

        if trial_pairs > current_pairs:
            kept.append((a, b, t))
            current_pairs = trial_pairs
        else:
            skipped += 1

        # Early exit if fully reachable
        if current_pairs == total_target:
            skipped += len(edges) - edges.index((a, b, t)) - 1
            break

    stats['phase1_kept'] = len(kept)
    stats['phase1_skipped'] = skipped + (len(edges) - len(kept) - skipped)
    stats['bfs_count'] = bfs_count
    stats['final_pairs'] = current_pairs
    stats['target_pairs'] = total_target

    return kept, stats


def forward_incremental_v3(k, M, stats=None):
    """
    Forward incremental with proper reach matrix maintenance.

    Fix from v1: After adding each edge, do a FULL reachability recompute
    from scratch using only kept edges. This is O(k^3) per kept edge
    but ensures correctness.
    """
    if stats is None:
        stats = {}

    n = 2 * k
    INF = float('inf')
    total_target = n * (n - 1)

    edges = matrix_to_edges(k, M)
    edges.sort(key=lambda e: e[2])

    # Full reachability matrix: reach[u][v] = earliest arrival
    reach = [[INF] * n for _ in range(n)]
    for i in range(n):
        reach[i][i] = -1

    kept = []
    skipped = 0
    pair_count = 0  # current reachable pairs

    lookup_count = 0
    update_count = 0

    for (a, b, t) in edges:
        if pair_count == total_target:
            skipped += 1
            continue

        # Check: would adding this edge create any new reachable pair?
        # Build adj from kept + this edge
        trial_edges = kept + [(a, b, t)]
        adj = build_adj(trial_edges)

        # Full reachability
        new_reach = [[INF] * n for _ in range(n)]
        for s in range(n):
            r = temporal_reach_from(s, adj)
            for d, arr in r.items():
                new_reach[s][d] = arr

        # Count new pairs
        new_pairs = 0
        for u in range(n):
            for v in range(n):
                lookup_count += 1
                if u != v and reach[u][v] == INF and new_reach[u][v] < INF:
                    new_pairs += 1

        if new_pairs > 0:
            kept.append((a, b, t))
            # Update reach to new_reach
            for u in range(n):
                for v in range(n):
                    update_count += 1
                    reach[u][v] = new_reach[u][v]
            pair_count += new_pairs
        else:
            skipped += 1

    stats['phase1_kept'] = len(kept)
    stats['phase1_skipped'] = skipped
    stats['lookup_count'] = lookup_count
    stats['update_count'] = update_count
    stats['final_pairs'] = pair_count
    stats['target_pairs'] = total_target

    return kept, stats


def backward_prune(k, kept_edges, stats=None):
    if stats is None:
        stats = {}

    n = 2 * k
    ordered = sorted(kept_edges, key=lambda e: -e[2])
    final = set(map(tuple, kept_edges))

    full_reach = all_pairs_earliest(k, list(final))
    removals = 0

    for edge in ordered:
        trial = final - {edge}
        trial_reach = all_pairs_earliest(k, list(trial))

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


def greedy_offline(k, M, n_trials=3):
    all_e = list(matrix_to_edges(k, M))
    orig = all_pairs_earliest(k, all_e)
    n = 2 * k
    best_set = None
    for _ in range(n_trials):
        random.shuffle(all_e)
        cur = set(map(tuple, all_e))
        for e in list(cur):
            trial = cur - {e}
            trial_reach = all_pairs_earliest(k, list(trial))
            ok = all(
                trial_reach.get((s, d), float('inf')) < float('inf')
                for s in range(n) for d in range(n)
                if s != d and orig[(s, d)] < float('inf')
            )
            if ok:
                cur = trial
        if best_set is None or len(cur) < len(best_set):
            best_set = cur
    return list(best_set)


def best_response(k, M, max_rounds=10):
    all_e = list(matrix_to_edges(k, M))
    orig = all_pairs_earliest(k, all_e)
    n = 2 * k
    cur = set(map(tuple, all_e))
    for _ in range(max_rounds):
        changed = False
        for e in list(cur):
            trial = cur - {e}
            trial_reach = all_pairs_earliest(k, list(trial))
            ok = all(
                trial_reach.get((s, d), float('inf')) < float('inf')
                for s in range(n) for d in range(n)
                if s != d and orig[(s, d)] < float('inf')
            )
            if ok:
                cur = trial
                changed = True
        if not changed:
            break
    return list(cur)


def run_experiment():
    random.seed(42)

    K_VALUES = [3, 4, 5, 6, 7, 8, 10]
    N_MATRICES = 50

    print("=" * 80)
    print("H14 v2: Forward Incremental with Full Reachability Check")
    print("=" * 80)

    all_results = {}

    for k in K_VALUES:
        print(f"\n{'─' * 60}")
        print(f"k = {k}  (n = {2*k}, budget = {4*k-3}, k^2 = {k*k})")
        print(f"{'─' * 60}")

        budget = 4 * k - 3
        n = 2 * k
        total_pairs = n * (n - 1)

        results = {
            'phase1_edges': [], 'phase2_edges': [],
            'greedy_edges': [], 'h10_edges': [],
            'phase1_correct': 0, 'phase2_correct': 0,
            'phase1_times': [], 'phase2_times': [],
            'greedy_times': [], 'h10_times': [],
            'lookup_counts': [], 'update_counts': [],
            'bfs_counts': [],
            'matrices_tried': 0, 'matrices_reachable': 0,
        }

        count = 0
        attempts = 0

        while count < N_MATRICES:
            attempts += 1
            if attempts > N_MATRICES * 20:
                print(f"  WARNING: gave up after {attempts}")
                break

            M = random_matrix(k)
            edges = matrix_to_edges(k, M)
            if not is_fully_reachable(k, edges):
                continue

            results['matrices_tried'] = attempts
            results['matrices_reachable'] += 1
            count += 1

            # Phase 1: v2 (pair count based)
            stats = {}
            t0 = time.time()
            kept, stats = forward_incremental_v2(k, M, stats)
            t1 = time.time()
            phase1_time = t1 - t0

            p1_correct = (stats['final_pairs'] == total_pairs)
            if p1_correct:
                results['phase1_correct'] += 1

            results['phase1_edges'].append(len(kept))
            results['phase1_times'].append(phase1_time)
            results['bfs_counts'].append(stats['bfs_count'])

            # Phase 2: backward prune
            t0 = time.time()
            final, stats2 = backward_prune(k, kept, stats)
            t1 = time.time()

            p2_pairs = count_reachable(k, final)
            p2_correct = (p2_pairs == total_pairs)
            if p2_correct:
                results['phase2_correct'] += 1

            results['phase2_edges'].append(len(final))
            results['phase2_times'].append(t1 - t0)

            # Comparisons (small k only)
            if k <= 8:
                t0 = time.time()
                g = greedy_offline(k, M, n_trials=3)
                results['greedy_edges'].append(len(g))
                results['greedy_times'].append(time.time() - t0)

                t0 = time.time()
                h = best_response(k, M, max_rounds=10)
                results['h10_edges'].append(len(h))
                results['h10_times'].append(time.time() - t0)

            if count % 10 == 0:
                print(f"  [{count}/{N_MATRICES}] P1={len(kept)}, P2={len(final)}, "
                      f"ok={p1_correct}/{p2_correct}")

        all_results[k] = results

        # Summary
        p1m = statistics.mean(results['phase1_edges'])
        p2m = statistics.mean(results['phase2_edges'])
        p1c = results['phase1_correct']
        p2c = results['phase2_correct']
        t1m = statistics.mean(results['phase1_times']) * 1000
        t2m = statistics.mean(results['phase2_times']) * 1000

        print(f"  P1: mean={p1m:.1f}, correct={p1c}/{count}")
        print(f"  P2: mean={p2m:.1f}, correct={p2c}/{count}")
        print(f"  Budget: {budget}")
        if results['greedy_edges']:
            print(f"  Greedy: mean={statistics.mean(results['greedy_edges']):.1f}")
        if results['h10_edges']:
            print(f"  H10: mean={statistics.mean(results['h10_edges']):.1f}")
        print(f"  Time P1={t1m:.1f}ms, P2={t2m:.1f}ms")
        if results['greedy_times']:
            print(f"  Time greedy={statistics.mean(results['greedy_times'])*1000:.1f}ms, "
                  f"H10={statistics.mean(results['h10_times'])*1000:.1f}ms")
        print(f"  BFS calls: mean={statistics.mean(results['bfs_counts']):.0f}")

    # Cross-k summary
    print("\n" + "=" * 80)
    print("CROSS-K SUMMARY")
    print("=" * 80)
    print(f"\n{'k':>3} {'n':>4} {'4k-3':>5} {'P1':>7} {'P2':>7} {'Grdy':>7} {'H10':>7} "
          f"{'P1ok':>5} {'P2ok':>5} {'P1ms':>8} {'P2ms':>8}")
    print("-" * 80)

    ks, p1s, p2s, t1s = [], [], [], []
    for k in K_VALUES:
        r = all_results[k]
        p1m = statistics.mean(r['phase1_edges'])
        p2m = statistics.mean(r['phase2_edges'])
        gm = statistics.mean(r['greedy_edges']) if r['greedy_edges'] else 0
        hm = statistics.mean(r['h10_edges']) if r['h10_edges'] else 0
        t1m = statistics.mean(r['phase1_times']) * 1000
        t2m = statistics.mean(r['phase2_times']) * 1000
        p1c = f"{r['phase1_correct']}"
        p2c = f"{r['phase2_correct']}"
        print(f"{k:>3} {2*k:>4} {4*k-3:>5} {p1m:>7.1f} {p2m:>7.1f} {gm:>7.1f} {hm:>7.1f} "
              f"{p1c:>5} {p2c:>5} {t1m:>8.1f} {t2m:>8.1f}")
        ks.append(k)
        p1s.append(p1m)
        p2s.append(p2m)
        t1s.append(statistics.mean(r['phase1_times']))

    # Power law fits
    print("\n--- Power Law Fits (y = c * k^alpha) ---")
    def fit_power(xs, ys, label):
        lx = [math.log(x) for x in xs]
        ly = [math.log(max(y, 1e-12)) for y in ys]
        n = len(lx)
        mx, my = sum(lx)/n, sum(ly)/n
        num = sum((lx[i]-mx)*(ly[i]-my) for i in range(n))
        den = sum((lx[i]-mx)**2 for i in range(n))
        if den == 0: return
        alpha = num / den
        c = math.exp(my - alpha * mx)
        ss_res = sum((ly[i] - (math.log(c) + alpha*lx[i]))**2 for i in range(n))
        ss_tot = sum((ly[i] - my)**2 for i in range(n))
        r2 = 1 - ss_res / max(ss_tot, 1e-12)
        print(f"  {label}: {c:.4g} * k^{alpha:.2f}  (R^2={r2:.4f})")
        return alpha

    fit_power(ks, p1s, "Phase 1 edges")
    fit_power(ks, p2s, "Phase 2 edges")
    fit_power(ks, t1s, "Phase 1 wall time")

    # Budget comparison
    print("\n--- Budget Analysis ---")
    print(f"{'k':>3} {'P1':>7} {'P2':>7} {'4k-3':>5} {'P2/budget':>10} {'P1/k^2':>8}")
    for k in K_VALUES:
        r = all_results[k]
        p1m = statistics.mean(r['phase1_edges'])
        p2m = statistics.mean(r['phase2_edges'])
        print(f"{k:>3} {p1m:>7.1f} {p2m:>7.1f} {4*k-3:>5} {p2m/(4*k-3):>10.3f} {p1m/(k*k):>8.3f}")


if __name__ == '__main__':
    run_experiment()
