"""
H14 FINAL: Forward-transitive incremental construction — comprehensive analysis.

Three algorithms compared:
1. Forward incremental (Phase 1) + backward prune (Phase 2)
2. Greedy offline (random-order removal)
3. Best-response (H10)

Precise operation counts, wall clock, power law fits.
"""

import random
import time
import statistics
from collections import defaultdict
import heapq
import math
import sys

# ─── Core ───

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

def temporal_reach_from(source, adj, depart=-1):
    best = {source: depart}
    queue = [(depart, source)]
    while queue:
        t_arr, u = heapq.heappop(queue)
        if t_arr > best.get(u, float('inf')):
            continue
        for (v, te) in adj[u]:
            if te >= t_arr and te < best.get(v, float('inf')):
                best[v] = te
                heapq.heappush(queue, (te, v))
    return best

def count_reachable(k, edges):
    adj = build_adj(edges)
    n = 2 * k
    return sum(len(temporal_reach_from(s, adj)) - 1 for s in range(n))

def is_fully_reachable(k, edges):
    adj = build_adj(edges)
    n = 2 * k
    return all(len(temporal_reach_from(s, adj)) == n for s in range(n))

def all_pairs_reachable_set(k, edges):
    """Return set of reachable (u,v) pairs."""
    adj = build_adj(edges)
    n = 2 * k
    pairs = set()
    for s in range(n):
        r = temporal_reach_from(s, adj)
        for d in r:
            if d != s:
                pairs.add((s, d))
    return pairs

# ─── Algorithms ───

def forward_incremental(k, M):
    """Phase 1: process edges in timestamp order, keep if increases reachable pairs."""
    n = 2 * k
    total_target = n * (n - 1)
    edges = sorted(matrix_to_edges(k, M), key=lambda e: e[2])

    kept = []
    current_pairs = 0
    edges_checked = 0  # BFS recomputation count
    bfs_ops = 0  # individual edge relaxations in BFS

    for idx, (a, b, t) in enumerate(edges):
        if current_pairs == total_target:
            break

        trial = kept + [(a, b, t)]
        edges_checked += 1

        # Count BFS ops precisely
        adj = build_adj(trial)
        trial_pairs = 0
        for s in range(n):
            best = {s: -1}
            queue = [(-1, s)]
            while queue:
                t_arr, u = heapq.heappop(queue)
                if t_arr > best.get(u, float('inf')):
                    bfs_ops += 1
                    continue
                for (v, te) in adj[u]:
                    bfs_ops += 1
                    if te >= t_arr and te < best.get(v, float('inf')):
                        best[v] = te
                        heapq.heappush(queue, (te, v))
            trial_pairs += len(best) - 1

        if trial_pairs > current_pairs:
            kept.append((a, b, t))
            current_pairs = trial_pairs

    return kept, {
        'edges_checked': edges_checked,
        'bfs_ops': bfs_ops,
        'kept': len(kept),
        'skipped': edges_checked - len(kept),
        'pairs': current_pairs,
    }


def backward_prune(k, kept_edges):
    """Phase 2: remove edges in reverse timestamp order if not needed."""
    n = 2 * k
    ordered = sorted(kept_edges, key=lambda e: -e[2])
    final = list(kept_edges)
    removals = 0
    checks = 0
    bfs_ops = 0

    ref_pairs = all_pairs_reachable_set(k, final)

    for edge in ordered:
        trial = [e for e in final if e != edge]
        checks += 1

        adj = build_adj(trial)
        trial_pairs = set()
        for s in range(n):
            best = {s: -1}
            queue = [(-1, s)]
            while queue:
                t_arr, u = heapq.heappop(queue)
                if t_arr > best.get(u, float('inf')):
                    bfs_ops += 1
                    continue
                for (v, te) in adj[u]:
                    bfs_ops += 1
                    if te >= t_arr and te < best.get(v, float('inf')):
                        best[v] = te
                        heapq.heappush(queue, (te, v))
            for d in best:
                if d != s:
                    trial_pairs.add((s, d))

        if ref_pairs <= trial_pairs:
            final = trial
            removals += 1

    return final, {
        'checks': checks,
        'bfs_ops': bfs_ops,
        'removals': removals,
        'final': len(final),
    }


def best_response_h10(k, M, max_rounds=10):
    """H10: best-response removal."""
    all_e = list(matrix_to_edges(k, M))
    n = 2 * k
    cur = set(map(tuple, all_e))
    ref_pairs = all_pairs_reachable_set(k, list(cur))
    bfs_ops = 0
    rounds = 0

    for _ in range(max_rounds):
        changed = False
        rounds += 1
        for e in list(cur):
            trial = cur - {e}
            adj = build_adj(list(trial))
            trial_pairs = set()
            for s in range(n):
                best = {s: -1}
                queue = [(-1, s)]
                while queue:
                    t_arr, u = heapq.heappop(queue)
                    if t_arr > best.get(u, float('inf')):
                        bfs_ops += 1
                        continue
                    for (v, te) in adj[u]:
                        bfs_ops += 1
                        if te >= t_arr and te < best.get(v, float('inf')):
                            best[v] = te
                            heapq.heappush(queue, (te, v))
                for d in best:
                    if d != s:
                        trial_pairs.add((s, d))

            if ref_pairs <= trial_pairs:
                cur = trial
                changed = True
        if not changed:
            break

    return list(cur), {
        'bfs_ops': bfs_ops,
        'rounds': rounds,
        'final': len(cur),
    }


# ─── Main experiment ───

def main():
    random.seed(42)

    K_VALUES = [3, 4, 5, 6, 7, 8, 10, 12]
    N_MATRICES = 50

    print("=" * 90)
    print("H14 FINAL: Forward Incremental Construction — Temporal Spanner")
    print("=" * 90)

    results_all = {}

    for k in K_VALUES:
        budget = 4 * k - 3
        n = 2 * k
        target = n * (n - 1)

        print(f"\n{'─'*70}")
        print(f"k={k}  n={n}  budget={budget}  k^2={k*k}  target_pairs={target}")
        print(f"{'─'*70}")

        R = {
            'p1_edges': [], 'p2_edges': [], 'h10_edges': [],
            'p1_correct': 0, 'p2_correct': 0, 'h10_correct': 0,
            'p1_time': [], 'p2_time': [], 'h10_time': [],
            'p1_bfs_ops': [], 'p2_bfs_ops': [], 'h10_bfs_ops': [],
            'p1_checked': [], 'p2_checks': [],
            'reachable_frac': 0, 'attempts': 0,
        }

        count = 0
        attempts = 0
        skip_h10 = (k > 10)  # H10 too slow for k>10

        while count < N_MATRICES:
            attempts += 1
            if attempts > N_MATRICES * 50:
                print(f"  ABORT: {attempts} attempts, {count} found")
                break

            M = random_matrix(k)
            edges = matrix_to_edges(k, M)
            if not is_fully_reachable(k, edges):
                continue

            count += 1

            # Phase 1
            t0 = time.time()
            p1_edges, p1_stats = forward_incremental(k, M)
            p1_time = time.time() - t0

            p1_ok = (p1_stats['pairs'] == target)
            if p1_ok:
                R['p1_correct'] += 1
            R['p1_edges'].append(p1_stats['kept'])
            R['p1_time'].append(p1_time)
            R['p1_bfs_ops'].append(p1_stats['bfs_ops'])
            R['p1_checked'].append(p1_stats['edges_checked'])

            # Phase 2
            t0 = time.time()
            p2_edges, p2_stats = backward_prune(k, p1_edges)
            p2_time = time.time() - t0

            p2_ok = (count_reachable(k, p2_edges) == target)
            if p2_ok:
                R['p2_correct'] += 1
            R['p2_edges'].append(p2_stats['final'])
            R['p2_time'].append(p2_time)
            R['p2_bfs_ops'].append(p2_stats['bfs_ops'])
            R['p2_checks'].append(p2_stats['checks'])

            # H10
            if not skip_h10:
                t0 = time.time()
                h10_edges, h10_stats = best_response_h10(k, M)
                h10_time = time.time() - t0

                h10_ok = (count_reachable(k, h10_edges) == target)
                if h10_ok:
                    R['h10_correct'] += 1
                R['h10_edges'].append(h10_stats['final'])
                R['h10_time'].append(h10_time)
                R['h10_bfs_ops'].append(h10_stats['bfs_ops'])

            if count % 10 == 0:
                sys.stdout.write(f"  [{count}/{N_MATRICES}] P1={p1_stats['kept']} "
                                 f"P2={p2_stats['final']} "
                                 f"{'H10='+str(h10_stats['final']) if not skip_h10 else ''}\n")
                sys.stdout.flush()

        R['attempts'] = attempts
        R['reachable_frac'] = count / max(attempts, 1)
        R['count'] = count
        results_all[k] = R

        # Per-k summary
        p1m = statistics.mean(R['p1_edges'])
        p2m = statistics.mean(R['p2_edges'])
        print(f"  Reachable: {count}/{attempts} ({R['reachable_frac']*100:.0f}%)")
        print(f"  Phase 1: edges={p1m:.1f}  correct={R['p1_correct']}/{count}  "
              f"time={statistics.mean(R['p1_time'])*1000:.1f}ms")
        print(f"  Phase 2: edges={p2m:.1f}  correct={R['p2_correct']}/{count}  "
              f"time={statistics.mean(R['p2_time'])*1000:.1f}ms")
        print(f"  P1+P2 total time: {(statistics.mean(R['p1_time'])+statistics.mean(R['p2_time']))*1000:.1f}ms")
        if R['h10_edges']:
            h10m = statistics.mean(R['h10_edges'])
            print(f"  H10:     edges={h10m:.1f}  correct={R['h10_correct']}/{count}  "
                  f"time={statistics.mean(R['h10_time'])*1000:.1f}ms")
        print(f"  Budget 4k-3 = {budget}")

    # ════════════════════════════════════════════════
    # CROSS-K TABLES
    # ════════════════════════════════════════════════
    print("\n" + "=" * 90)
    print("COMPREHENSIVE RESULTS")
    print("=" * 90)

    # Table 1: Edge counts
    print("\n--- Table 1: Edge Counts ---")
    print(f"{'k':>3} {'k^2':>5} {'4k-3':>5} {'P1':>7} {'P2':>7} {'H10':>7} "
          f"{'P1/k^2':>7} {'P2/4k-3':>8}")
    print("-" * 65)
    for k in K_VALUES:
        R = results_all[k]
        if not R['p1_edges']:
            continue
        p1 = statistics.mean(R['p1_edges'])
        p2 = statistics.mean(R['p2_edges'])
        h10 = statistics.mean(R['h10_edges']) if R['h10_edges'] else -1
        print(f"{k:>3} {k*k:>5} {4*k-3:>5} {p1:>7.1f} {p2:>7.1f} {h10:>7.1f} "
              f"{p1/(k*k):>7.2f} {p2/(4*k-3):>8.3f}")

    # Table 2: Correctness
    print("\n--- Table 2: Correctness (out of 50) ---")
    print(f"{'k':>3} {'P1':>5} {'P2':>5} {'H10':>5}")
    for k in K_VALUES:
        R = results_all[k]
        if not R['p1_edges']:
            continue
        h10c = R['h10_correct'] if R['h10_edges'] else '-'
        print(f"{k:>3} {R['p1_correct']:>5} {R['p2_correct']:>5} {str(h10c):>5}")

    # Table 3: Wall clock times
    print("\n--- Table 3: Wall Clock (ms) ---")
    print(f"{'k':>3} {'P1':>8} {'P2':>8} {'P1+P2':>8} {'H10':>8} {'speedup':>8}")
    print("-" * 50)
    ks_for_fit = []
    p1_times_fit = []
    p12_times_fit = []
    h10_times_fit = []

    for k in K_VALUES:
        R = results_all[k]
        if not R['p1_edges']:
            continue
        t1 = statistics.mean(R['p1_time']) * 1000
        t2 = statistics.mean(R['p2_time']) * 1000
        t12 = t1 + t2
        if R['h10_time']:
            th = statistics.mean(R['h10_time']) * 1000
            speedup = th / max(t12, 0.001)
            print(f"{k:>3} {t1:>8.1f} {t2:>8.1f} {t12:>8.1f} {th:>8.1f} {speedup:>8.2f}x")
            h10_times_fit.append(statistics.mean(R['h10_time']))
        else:
            print(f"{k:>3} {t1:>8.1f} {t2:>8.1f} {t12:>8.1f} {'--':>8}")
        ks_for_fit.append(k)
        p1_times_fit.append(statistics.mean(R['p1_time']))
        p12_times_fit.append(statistics.mean(R['p1_time']) + statistics.mean(R['p2_time']))

    # Table 4: BFS operation counts
    print("\n--- Table 4: BFS Operations (mean) ---")
    print(f"{'k':>3} {'P1_ops':>10} {'P2_ops':>10} {'H10_ops':>10} "
          f"{'P1_ops/k^4':>11} {'H10_ops/k^4':>12}")
    print("-" * 65)
    p1_ops_fit = []
    p2_ops_fit = []
    h10_ops_fit = []

    for k in K_VALUES:
        R = results_all[k]
        if not R['p1_edges']:
            continue
        p1o = statistics.mean(R['p1_bfs_ops'])
        p2o = statistics.mean(R['p2_bfs_ops'])
        p1_ops_fit.append(p1o)
        p2_ops_fit.append(p2o)
        if R['h10_bfs_ops']:
            h10o = statistics.mean(R['h10_bfs_ops'])
            h10_ops_fit.append(h10o)
            print(f"{k:>3} {p1o:>10.0f} {p2o:>10.0f} {h10o:>10.0f} "
                  f"{p1o/(k**4):>11.2f} {h10o/(k**4):>12.2f}")
        else:
            print(f"{k:>3} {p1o:>10.0f} {p2o:>10.0f} {'--':>10}")

    # Table 5: Forward pass efficiency
    print("\n--- Table 5: Forward Pass Efficiency ---")
    print(f"{'k':>3} {'checked':>8} {'kept':>6} {'skip%':>6} {'skip/k^2':>9}")
    for k in K_VALUES:
        R = results_all[k]
        if not R['p1_edges']:
            continue
        ch = statistics.mean(R['p1_checked'])
        ke = statistics.mean(R['p1_edges'])
        sk = ch - ke
        print(f"{k:>3} {ch:>8.1f} {ke:>6.1f} {100*sk/max(ch,1):>5.1f}% {sk/(k*k):>9.3f}")

    # Power law fits
    print("\n--- Power Law Fits: y = c * k^alpha ---")

    def fit_power(xs, ys, label):
        xs2 = [x for x, y in zip(xs, ys) if y > 0]
        ys2 = [y for y in ys if y > 0]
        if len(xs2) < 3:
            return None
        lx = [math.log(x) for x in xs2]
        ly = [math.log(y) for y in ys2]
        nn = len(lx)
        mx, my = sum(lx)/nn, sum(ly)/nn
        num = sum((lx[i]-mx)*(ly[i]-my) for i in range(nn))
        den = sum((lx[i]-mx)**2 for i in range(nn))
        if den == 0: return None
        alpha = num / den
        c = math.exp(my - alpha * mx)
        ss_res = sum((ly[i] - (math.log(c) + alpha*lx[i]))**2 for i in range(nn))
        ss_tot = sum((ly[i] - my)**2 for i in range(nn))
        r2 = 1 - ss_res / max(ss_tot, 1e-12)
        print(f"  {label}: {c:.4g} * k^{alpha:.2f}  (R^2={r2:.4f})")
        return alpha

    p1_edges_fit = [statistics.mean(results_all[k]['p1_edges']) for k in K_VALUES if results_all[k]['p1_edges']]
    p2_edges_fit = [statistics.mean(results_all[k]['p2_edges']) for k in K_VALUES if results_all[k]['p2_edges']]
    ks_used = [k for k in K_VALUES if results_all[k]['p1_edges']]

    a_p1e = fit_power(ks_used, p1_edges_fit, "Phase 1 edges")
    a_p2e = fit_power(ks_used, p2_edges_fit, "Phase 2 edges")
    a_p1t = fit_power(ks_for_fit, p1_times_fit, "Phase 1 time")
    a_p12t = fit_power(ks_for_fit, p12_times_fit, "P1+P2 total time")
    if h10_times_fit:
        a_h10t = fit_power(ks_for_fit[:len(h10_times_fit)], h10_times_fit, "H10 time")
    fit_power(ks_used, p1_ops_fit, "Phase 1 BFS ops")
    fit_power(ks_used, p2_ops_fit, "Phase 2 BFS ops")
    if h10_ops_fit:
        fit_power(ks_used[:len(h10_ops_fit)], h10_ops_fit, "H10 BFS ops")

    # Critical question: amortized cost per kept edge
    print("\n--- Amortized Analysis ---")
    print(f"{'k':>3} {'P1_kept':>8} {'P1_ops/kept':>12} {'P2_ops/kept':>12}")
    for k in K_VALUES:
        R = results_all[k]
        if not R['p1_edges']:
            continue
        ke = statistics.mean(R['p1_edges'])
        p1o = statistics.mean(R['p1_bfs_ops'])
        p2o = statistics.mean(R['p2_bfs_ops'])
        print(f"{k:>3} {ke:>8.1f} {p1o/max(ke,1):>12.1f} {p2o/max(ke,1):>12.1f}")

    # Verdict
    print("\n" + "=" * 90)
    print("VERDICT")
    print("=" * 90)
    print()

    # Check budget compliance
    budget_ok = all(
        statistics.mean(results_all[k]['p2_edges']) <= 4*k - 3 + 0.5
        for k in K_VALUES if results_all[k]['p2_edges']
    )
    budget_exceed = {k: statistics.mean(results_all[k]['p2_edges']) / (4*k-3)
                     for k in K_VALUES if results_all[k]['p2_edges']}

    all_correct = all(
        results_all[k]['p2_correct'] == results_all[k].get('count', 0)
        for k in K_VALUES if results_all[k]['p2_edges']
    )

    # Is P1 alone within budget?
    p1_budget = all(
        statistics.mean(results_all[k]['p1_edges']) <= 4*k - 3 + 0.5
        for k in K_VALUES if results_all[k]['p1_edges']
    )

    print(f"Phase 1 alone within budget: {'YES' if p1_budget else 'NO'}")
    print(f"Phase 1+2 preserves reachability: {'YES' if all_correct else 'NO'}")
    print(f"Phase 2 within budget: {'YES' if budget_ok else 'NO'}")
    for k in sorted(budget_exceed.keys()):
        ratio = budget_exceed[k]
        status = 'OK' if ratio <= 1.01 else f'OVER by {(ratio-1)*100:.0f}%'
        print(f"  k={k}: P2/budget = {ratio:.3f} ({status})")


if __name__ == '__main__':
    main()
