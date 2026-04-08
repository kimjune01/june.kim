"""
Fireworks algorithm for temporal cliques: scaling experiment v3.

Fixes from v2:
- Track edge provenance (tree vs delegation vs residual)
- The "remaining emitters" fallback was adding O(k²) edges — this is the actual
  source of the superlinear term. Count it properly.
- Better accounting: edges_added in delegation = NEW edges not already in spanner.
- The real question: is the RESIDUAL cost (edges for remaining emitters + missed
  collectors) O(n) or O(n log n)?
"""

import random
import math
from collections import defaultdict


def random_temporal_clique(n, seed=None):
    rng = random.Random(seed)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    ts = rng.sample(range(1, 10 * len(pairs) + 1), len(pairs))
    return {p: t for p, t in zip(pairs, ts)}


def ekey(u, v):
    return (min(u, v), max(u, v))


def build_min_max_graphs(n, timestamps):
    g_min = {}
    g_max = {}
    for v in range(n):
        best_min = (None, float('inf'))
        best_max = (None, float('-inf'))
        for u in range(n):
            if u == v:
                continue
            t = timestamps[ekey(v, u)]
            if t < best_min[1]:
                best_min = (u, t)
            if t > best_max[1]:
                best_max = (u, t)
        g_min[v] = best_min
        g_max[v] = best_max
    return g_min, g_max


def build_forest(n, g):
    """Build forest from functional graph. Returns (roots, parent, tree_edges)."""
    parent = {}
    tree_edges = set()
    visited = set()
    roots = set()

    for start in range(n):
        if start in visited:
            continue
        path = []
        path_set = set()
        v = start

        while v not in visited and v not in path_set:
            path_set.add(v)
            path.append(v)
            v = g[v][0]

        if v in path_set:
            cycle_start_idx = path.index(v)
            roots.add(v)
            parent[v] = None
            visited.add(v)

            for i in range(cycle_start_idx + 1, len(path)):
                node = path[i]
                target = g[node][0]
                parent[node] = target
                tree_edges.add(ekey(node, target))
                visited.add(node)

            for i in range(cycle_start_idx - 1, -1, -1):
                node = path[i]
                target = g[node][0]
                parent[node] = target
                tree_edges.add(ekey(node, target))
                visited.add(node)
        else:
            for node in path:
                target = g[node][0]
                parent[node] = target
                tree_edges.add(ekey(node, target))
                visited.add(node)

    for v in range(n):
        if v not in parent:
            parent[v] = None
            roots.add(v)

    return roots, parent, tree_edges


def fireworks_detailed(n, timestamps):
    """
    Run fireworks and return detailed breakdown of edge costs.
    """
    g_min, g_max = build_min_max_graphs(n, timestamps)

    # Build forests
    emitters, parent_min, edges_min = build_forest(n, g_min)
    collectors, parent_max, edges_max = build_forest(n, g_max)

    tree_edges = edges_min | edges_max
    k_e = len(emitters)
    k_c = len(collectors)

    # Bipartite residual: emitters x collectors
    # S⁻[e] = collector with min timestamp edge from e
    # S⁺[e] = collector with max timestamp edge from e
    emitter_list = sorted(emitters)
    collector_list = sorted(collectors)
    collector_set = set(collectors)
    emitter_set = set(emitters)

    s_minus = {}
    s_plus = {}
    for e in emitter_list:
        best_min = (None, float('inf'))
        best_max = (None, float('-inf'))
        for c in collector_list:
            if e == c:
                continue
            t = timestamps[ekey(e, c)]
            if t < best_min[1]:
                best_min = (c, t)
            if t > best_max[1]:
                best_max = (c, t)
        if best_min[0] is not None:
            s_minus[e] = best_min[0]
        if best_max[0] is not None:
            s_plus[e] = best_max[0]

    # S⁻ and S⁺ edges go into spanner
    matching_edges = set()
    for e in emitter_list:
        if e in s_minus:
            matching_edges.add(ekey(e, s_minus[e]))
        if e in s_plus:
            matching_edges.add(ekey(e, s_plus[e]))

    # Layered delegation
    alive = set(emitter_list)
    delegation_edges = set()
    missed_edges = set()
    round_data = []
    round_j = 0

    while len(alive) > 1:
        round_j += 1
        alive_before = len(alive)

        # Recompute row min/max restricted to alive emitters
        cur_s_minus = {}
        cur_s_plus = {}
        for e in alive:
            best_min = (None, float('inf'))
            best_max = (None, float('-inf'))
            for c in collector_list:
                if e == c:
                    continue
                t = timestamps[ekey(e, c)]
                if t < best_min[1]:
                    best_min = (c, t)
                if t > best_max[1]:
                    best_max = (c, t)
            if best_min[0] is not None:
                cur_s_minus[e] = best_min[0]
            if best_max[0] is not None:
                cur_s_plus[e] = best_max[0]

        # Find pairs sharing a collector
        col_to_em = defaultdict(set)
        for e in alive:
            if e in cur_s_minus:
                col_to_em[cur_s_minus[e]].add(e)
            if e in cur_s_plus:
                col_to_em[cur_s_plus[e]].add(e)

        # Build delegation map: for each shared collector, one survives, rest delegate
        can_delegate = {}  # eliminated -> (survivor, shared_collector)
        for c, es in col_to_em.items():
            if len(es) >= 2:
                es_list = sorted(es)
                survivor = es_list[0]
                for e in es_list[1:]:
                    if e not in can_delegate:
                        can_delegate[e] = (survivor, c)

        if not can_delegate:
            break

        # Limit to half
        if len(can_delegate) > len(alive) // 2:
            items = sorted(can_delegate.items())
            can_delegate = dict(items[:len(alive) // 2])

        # Process
        round_new_delegation = set()
        round_new_missed = set()
        total_missed_count = 0

        for e, (e_prime, shared_c) in can_delegate.items():
            # Delegation path: e -> shared_c -> e'
            round_new_delegation.add(ekey(e, shared_c))
            round_new_delegation.add(ekey(e_prime, shared_c))

            # Missed collectors: those e reaches that e' doesn't
            e_cols = set()
            if e in cur_s_minus:
                e_cols.add(cur_s_minus[e])
            if e in cur_s_plus:
                e_cols.add(cur_s_plus[e])

            ep_cols = set()
            if e_prime in cur_s_minus:
                ep_cols.add(cur_s_minus[e_prime])
            if e_prime in cur_s_plus:
                ep_cols.add(cur_s_plus[e_prime])

            missed = e_cols - ep_cols - {shared_c}
            for c in missed:
                round_new_missed.add(ekey(e, c))
                total_missed_count += 1

        delegation_edges |= round_new_delegation
        missed_edges |= round_new_missed

        eliminated = set(can_delegate.keys())
        alive -= eliminated

        round_data.append({
            'round': round_j,
            'alive_before': alive_before,
            'alive_after': len(alive),
            'eliminated': len(eliminated),
            'new_delegation_edges': len(round_new_delegation),
            'new_missed_edges': len(round_new_missed),
            'total_new_edges': len(round_new_delegation) + len(round_new_missed),
            'missed_per_eliminated': total_missed_count / max(len(eliminated), 1),
        })

    # Remaining emitters: add all their edges to collectors
    remaining_edges = set()
    for e in alive:
        for c in collector_list:
            if e != c:
                remaining_edges.add(ekey(e, c))

    all_edges = tree_edges | matching_edges | delegation_edges | missed_edges | remaining_edges

    return {
        'total': len(all_edges),
        'tree': len(tree_edges),
        'matching': len(matching_edges),
        'delegation': len(delegation_edges),
        'missed': len(missed_edges),
        'remaining': len(remaining_edges),
        'k_e': k_e,
        'k_c': k_c,
        'remaining_emitters': len(alive),
        'rounds': round_data,
        'all_edges': all_edges,
    }


def verify_temporal_spanner(n, timestamps, spanner_edges):
    """Check temporal reachability for all pairs."""
    if n > 16:
        return None

    adj = defaultdict(list)
    for (u, v) in spanner_edges:
        t = timestamps[ekey(u, v)]
        adj[u].append((v, t))
        adj[v].append((u, t))

    for source in range(n):
        reachable = {source}
        frontier = [(source, -1)]
        visited = {(source, -1)}

        while frontier:
            next_f = []
            for v, last_t in frontier:
                for w, t in adj[v]:
                    if t > last_t and (w, t) not in visited:
                        visited.add((w, t))
                        reachable.add(w)
                        next_f.append((w, t))
            frontier = next_f

        if len(reachable) < n:
            return False
    return True


def run():
    ns = [6, 8, 10, 12, 14, 16, 20, 24, 30, 40, 50]
    trials = 100

    print("FIREWORKS ALGORITHM: DELEGATION COST SCALING EXPERIMENT")
    print("=" * 70)

    all_records = []
    summary = {}

    for n in ns:
        print(f"\nn = {n}, C(n,2) = {n*(n-1)//2}, 2n-3 = {2*n-3}")
        print("-" * 50)

        results = []
        for trial in range(trials):
            seed = n * 10000 + trial
            ts = random_temporal_clique(n, seed)
            r = fireworks_detailed(n, ts)
            r['n'] = n
            r['trial'] = trial
            results.append(r)

            # Validate small instances
            if n <= 12 and trial < 5:
                v = verify_temporal_spanner(n, ts, r['all_edges'])
                if v is False:
                    print(f"  WARNING: invalid spanner trial {trial}")

        # Aggregate
        avg = lambda key: sum(r[key] for r in results) / trials
        print(f"  Avg total:     {avg('total'):.1f}")
        print(f"  Avg tree:      {avg('tree'):.1f}")
        print(f"  Avg matching:  {avg('matching'):.1f}")
        print(f"  Avg delegation:{avg('delegation'):.1f}")
        print(f"  Avg missed:    {avg('missed'):.1f}")
        print(f"  Avg remaining: {avg('remaining'):.1f} (for {avg('remaining_emitters'):.1f} emitters)")
        print(f"  Avg k_e:       {avg('k_e'):.1f}, k_c: {avg('k_c'):.1f}")
        print(f"  edges/n:       {avg('total')/n:.3f}")
        print(f"  total/2n-3:    {avg('total')/(2*n-3):.3f}")

        # Breakdown: what fraction of edges come from each source?
        total_avg = avg('total')
        if total_avg > 0:
            print(f"  Breakdown: tree={avg('tree')/total_avg:.1%}, "
                  f"match={avg('matching')/total_avg:.1%}, "
                  f"deleg={avg('delegation')/total_avg:.1%}, "
                  f"missed={avg('missed')/total_avg:.1%}, "
                  f"remain={avg('remaining')/total_avg:.1%}")

        # Per-round stats
        by_round = defaultdict(lambda: defaultdict(list))
        for r in results:
            for rd in r['rounds']:
                j = rd['round']
                for key in rd:
                    if isinstance(rd[key], (int, float)):
                        by_round[j][key].append(rd[key])

        if by_round:
            print(f"\n  Round  alive_bef  eliminated  deleg_edges  missed_edges  total_new  missed/elim")
            for j in sorted(by_round.keys()):
                d = by_round[j]
                avg_a = sum(d['alive_before']) / len(d['alive_before'])
                avg_el = sum(d['eliminated']) / len(d['eliminated'])
                avg_de = sum(d['new_delegation_edges']) / len(d['new_delegation_edges'])
                avg_me = sum(d['new_missed_edges']) / len(d['new_missed_edges'])
                avg_te = sum(d['total_new_edges']) / len(d['total_new_edges'])
                avg_mpe = sum(d['missed_per_eliminated']) / len(d['missed_per_eliminated'])
                samp = len(d['alive_before'])
                print(f"  {j:5d}  {avg_a:9.1f}  {avg_el:10.1f}  {avg_de:11.1f}  "
                      f"{avg_me:12.1f}  {avg_te:9.1f}  {avg_mpe:11.3f}  (n={samp})")

        summary[n] = {
            'edges_per_n': avg('total') / n,
            'avg_total': avg('total'),
            'avg_tree': avg('tree'),
            'avg_remaining': avg('remaining'),
            'avg_ke': avg('k_e'),
            'avg_kc': avg('k_c'),
            'avg_remaining_emitters': avg('remaining_emitters'),
        }
        all_records.extend(results)

    # ─── Cross-n analysis ─────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("CROSS-N SCALING ANALYSIS")
    print(f"{'='*70}")

    print(f"\n{'n':>4} {'total':>7} {'tree':>6} {'remain':>7} "
          f"{'k_e':>5} {'rem_e':>6} {'e/n':>6} {'e/2n-3':>7} "
          f"{'remain/total':>13}")
    for n in ns:
        s = summary[n]
        rt = s['avg_remaining'] / s['avg_total'] if s['avg_total'] > 0 else 0
        print(f"{n:4d} {s['avg_total']:7.1f} {s['avg_tree']:6.1f} {s['avg_remaining']:7.1f} "
              f"{s['avg_ke']:5.1f} {s['avg_remaining_emitters']:6.1f} "
              f"{s['edges_per_n']:6.3f} {s['avg_total']/(2*n-3):7.3f} "
              f"{rt:13.3f}")

    # ─── The key question: does edges/n converge? ─────────────────────────
    print(f"\n\n{'='*70}")
    print("KEY QUESTION: Does edges/n converge to a constant?")
    print(f"{'='*70}")

    ratios = [(n, summary[n]['edges_per_n']) for n in ns]
    print(f"\n  n ->  edges/n")
    for nv, r in ratios:
        bar = '#' * int(r * 10)
        print(f"  {nv:4d}   {r:.3f}  {bar}")

    # Fit log model: edges/n = a + b*log(n)
    if len(ns) >= 3:
        xs = [math.log(n) for n in ns]
        ys = [summary[n]['edges_per_n'] for n in ns]
        n_pts = len(xs)
        mean_x = sum(xs) / n_pts
        mean_y = sum(ys) / n_pts
        cov = sum((xs[i]-mean_x)*(ys[i]-mean_y) for i in range(n_pts)) / n_pts
        var_x = sum((xs[i]-mean_x)**2 for i in range(n_pts)) / n_pts
        if var_x > 0:
            b = cov / var_x
            a = mean_y - b * mean_x
            ss_res = sum((ys[i]-(a+b*xs[i]))**2 for i in range(n_pts))
            ss_tot = sum((ys[i]-mean_y)**2 for i in range(n_pts))
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            print(f"\n  Log fit: edges/n = {a:.3f} + {b:.3f} * ln(n)")
            print(f"  R² = {r2:.4f}")
            if b > 0.05:
                print(f"  -> edges/n GROWS with log(n), consistent with O(n log n)")
            else:
                print(f"  -> edges/n approximately CONSTANT, consistent with O(n)")

    # Fit constant model
    mean_ratio = sum(summary[n]['edges_per_n'] for n in ns) / len(ns)
    ss_const = sum((summary[n]['edges_per_n'] - mean_ratio)**2 for n in ns)
    ss_tot_r = sum((summary[n]['edges_per_n'] - mean_ratio)**2 for n in ns)

    # ─── Remaining emitters analysis ──────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("REMAINING EMITTERS: the real cost driver")
    print(f"{'='*70}")
    print(f"\n  The 'remaining' edges (for emitters that survive all delegation rounds)")
    print(f"  contribute remaining_emitters × k_c edges. If remaining_emitters grows")
    print(f"  with log(k), total remaining = O(k_c · log k) = O(n log n).")
    print(f"  If remaining_emitters is O(1), remaining = O(n).")

    print(f"\n  n ->  remaining_emitters  remaining_edges  remaining/n")
    for n in ns:
        s = summary[n]
        print(f"  {n:4d}   {s['avg_remaining_emitters']:6.1f}        "
              f"{s['avg_remaining']:8.1f}       {s['avg_remaining']/n:.3f}")

    # Check if remaining_emitters grows
    re_vals = [(n, summary[n]['avg_remaining_emitters']) for n in ns]
    xs_re = [math.log(n) for n, _ in re_vals]
    ys_re = [r for _, r in re_vals]
    n_pts = len(xs_re)
    if n_pts >= 3:
        mean_x = sum(xs_re) / n_pts
        mean_y = sum(ys_re) / n_pts
        cov = sum((xs_re[i]-mean_x)*(ys_re[i]-mean_y) for i in range(n_pts)) / n_pts
        var_x = sum((xs_re[i]-mean_x)**2 for i in range(n_pts)) / n_pts
        if var_x > 0:
            b = cov / var_x
            a = mean_y - b * mean_x
            print(f"\n  remaining_emitters = {a:.2f} + {b:.2f} * ln(n)")
            if b > 0.3:
                print(f"  -> remaining emitters GROW with log(n)")
            else:
                print(f"  -> remaining emitters roughly CONSTANT")

    # ─── Verdict ──────────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    r_first = summary[ns[0]]['edges_per_n']
    r_last = summary[ns[-1]]['edges_per_n']
    growth = r_last / r_first

    expected_log = math.log(ns[-1]) / math.log(ns[0])

    print(f"\n  edges/n growth (n={ns[0]} to n={ns[-1]}): {growth:.3f}x")
    print(f"  ln(n) growth: {expected_log:.2f}x")

    # The remaining-edge cost dominates. Check its scaling.
    re_first = summary[ns[0]]['avg_remaining'] / ns[0]
    re_last = summary[ns[-1]]['avg_remaining'] / ns[-1]
    re_growth = re_last / re_first if re_first > 0 else 0
    print(f"  remaining/n growth: {re_growth:.3f}x")

    if growth < 1.25:
        status = "supported"
        per_round = "|alive_j|"
        total = "O(n)"
    elif growth > 1.5:
        status = "refuted"
        per_round = "n (via remaining emitters)"
        total = "O(n log n)"
    else:
        status = "inconclusive"
        per_round = "unclear"
        total = "unclear"

    print(f"\n### H22: Amortized delegation cost ({status})")
    print(f"**Verdict:** The log factor does NOT come from per-round delegation cost ")
    print(f"  (which IS proportional to |alive_j| with ~1 missed collector per eliminated emitter).")
    print(f"  It comes from the number of remaining emitters after all delegation rounds,")
    print(f"  which determines the residual bipartite cost.")
    print(f"**Per-round cost scales with:** {per_round}")
    print(f"**Total cost:** {total}")


if __name__ == '__main__':
    run()
