"""
Fireworks algorithm for temporal cliques: scaling experiment v2.

Proper implementation of CPS (Casteigts-Peters-Schoeters) fireworks algorithm.

The algorithm on K_n with distinct timestamps:
1. Build G⁻ (each vertex's minimum-timestamp edge) and G⁺ (maximum-timestamp edge).
   These are functional graphs (each vertex has out-degree 1).
2. G⁻ edges form a forest of in-trees. Roots = emitters (X⁻).
   G⁺ edges form a forest of out-trees. Roots = collectors (X⁺).
3. Include all tree edges in the spanner (2(n-1) edges, but overlaps reduce this).
4. The trees connect each vertex to at least one emitter (via G⁻) and one collector (via G⁺).
5. Emitters and collectors form a bipartite residual graph.
   Each emitter e has a "row" of collectors it must reach.
   S⁻[e] = the collector reached from e via G⁻ path (or e's min-edge chain).
   S⁺[e] = the collector reached from e via G⁺ path.
6. The bipartite residual needs a temporal spanner. Layered delegation reduces emitters.

Key insight from CPS: The tree edges already give temporal paths from any vertex to
emitters/collectors. The remaining problem is connecting emitters to collectors.

For the actual experiment, we focus on the BIPARTITE RESIDUAL and the layered
delegation phase, which is where the log factor lives.
"""

import random
import math
from collections import defaultdict


def random_temporal_clique(n, seed=None):
    """K_n with distinct timestamps. Returns dict (i,j)->t for i<j."""
    rng = random.Random(seed)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    ts = rng.sample(range(1, 10 * len(pairs) + 1), len(pairs))
    return {p: t for p, t in zip(pairs, ts)}


def ekey(u, v):
    return (min(u, v), max(u, v))


def build_min_max_graphs(n, timestamps):
    """For each vertex, find its min-timestamp and max-timestamp neighbor."""
    g_min = {}  # v -> (neighbor, timestamp)
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


def follow_to_root(v, parent_map, visited=None):
    """Follow parent pointers to root. Returns (root, path)."""
    if visited is None:
        visited = set()
    path = [v]
    while parent_map.get(v) is not None and v not in visited:
        visited.add(v)
        v = parent_map[v]
        path.append(v)
    return v, path


def build_forest(n, g):
    """
    g is a functional graph: each vertex v has one outgoing edge g[v] = (target, timestamp).
    This forms a union of "rho" shapes: each connected component has exactly one cycle
    with trees hanging off it.

    We break each cycle by choosing one vertex as root (parent=None) and directing
    the rest of the cycle toward it. Trees hanging off the cycle already point inward.

    Returns:
    - roots: set of root vertices (one per component, chosen from each cycle)
    - parent: dict v -> parent vertex (None for roots)
    - tree_edges: set of undirected (u,v) edges in the forest
    """
    parent = {}
    tree_edges = set()
    visited = set()  # fully processed
    roots = set()

    for start in range(n):
        if start in visited:
            continue

        # Trace the path from start following g-edges
        path = []
        path_set = set()
        v = start

        while v not in visited and v not in path_set:
            path_set.add(v)
            path.append(v)
            v = g[v][0]

        if v in path_set:
            # v is on a cycle within our current path
            cycle_start_idx = path.index(v)

            # Make v the root
            roots.add(v)
            parent[v] = None
            visited.add(v)

            # Other cycle members: chain toward v
            # Cycle is path[cycle_start_idx], path[cycle_start_idx+1], ..., path[-1]
            # where path[-1] -> g[path[-1]] = ... eventually -> v
            # In the functional graph: path[i] -> g[path[i]] = path[i+1]
            # For the tree, we want parent[path[i+1]] = path[i] ... no, we want
            # edges that form a tree. Let's just use g-edges but skip the one
            # that closes the cycle (the edge from the vertex before v back to v).

            for i in range(cycle_start_idx + 1, len(path)):
                node = path[i]
                # node's g-edge goes to path[(i+1) % cycle] but we use that edge
                # The parent in the tree = where g points, EXCEPT for the last
                # cycle node whose g-edge points to v (closing the cycle).
                target = g[node][0]
                parent[node] = target
                tree_edges.add(ekey(node, target))
                visited.add(node)

            # Tail before the cycle: these vertices point toward the cycle
            for i in range(cycle_start_idx - 1, -1, -1):
                node = path[i]
                target = g[node][0]  # = path[i+1]
                parent[node] = target
                tree_edges.add(ekey(node, target))
                visited.add(node)

        else:
            # v is already visited (in a previous component)
            # All path vertices point toward v's component
            for node in path:
                target = g[node][0]
                parent[node] = target
                tree_edges.add(ekey(node, target))
                visited.add(node)

    # Safety: any unvisited vertex becomes a root
    for v in range(n):
        if v not in parent:
            parent[v] = None
            roots.add(v)

    return roots, parent, tree_edges


def compute_residual_bipartite(n, timestamps, g_min, g_max):
    """
    Compute the bipartite residual after tree construction.

    Emitters = roots of G⁻ forest (sources of the in-tree).
    Collectors = roots of G⁺ forest (sinks of the out-tree).

    Actually, in CPS:
    - G⁻: v -> min-neighbor. Roots of this functional graph are emitters.
      These are vertices that "emit" -- they have the earliest connections.
    - G⁺: v -> max-neighbor. Roots are collectors.

    Each emitter e needs to reach every collector c via a temporal path.
    The tree edges give paths from each non-root vertex to its root.
    The remaining connections needed are emitter-to-collector.

    For the bipartite residual:
    - Rows = emitters, Cols = collectors
    - S⁻ matching: for each emitter e, S⁻(e) = the collector reachable from e
      by following G⁺ (max-edge) chain.
    - S⁺ matching: for each emitter e, S⁺(e) = the collector reachable from e
      by following... hmm, this needs more careful thought.

    Let me reconsider. The CPS paper says:
    - After building T⁻ and T⁺, the residual is K_{X⁻, X⁺} (complete bipartite
      between emitters and collectors).
    - For each emitter e and collector c, there's an edge with timestamp = t(e,c).
    - S⁻ = row minima of this bipartite graph (each emitter's minimum-timestamp
      edge to a collector).
    - S⁺ = row maxima.
    """
    # Build forests
    roots_min, parent_min, edges_min = build_forest(n, g_min)
    roots_max, parent_max, edges_max = build_forest(n, g_max)

    emitters = roots_min   # roots of min-edge forest
    collectors = roots_max  # roots of max-edge forest

    tree_edges = edges_min | edges_max

    # Bipartite residual: emitters x collectors
    # Row minima (S⁻) and row maxima (S⁺) for each emitter
    s_minus = {}  # emitter -> collector with minimum timestamp
    s_plus = {}   # emitter -> collector with maximum timestamp

    for e in emitters:
        best_min = (None, float('inf'))
        best_max = (None, float('-inf'))
        for c in collectors:
            if e == c:
                # An emitter can also be a collector
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

    return emitters, collectors, tree_edges, s_minus, s_plus


def layered_delegation(emitters, collectors, timestamps, s_minus, s_plus):
    """
    Layered delegation on bipartite residual.

    Each round:
    1. For each alive emitter, it has S⁻ and S⁺ partners among collectors.
    2. Split into X_a (can delegate) and X_b (cannot).
       X_a = emitters that share a collector (via S⁻ or S⁺) with another emitter.
    3. Eliminate ≤ half of alive emitters (from X_a).
    4. For eliminated emitter e delegating to e':
       - The 2-hop path e -> c -> e' covers collector c.
       - "Missed collectors" = collectors reachable from e but not from e'.
       - Add edges for missed collectors.

    Returns: (spanner_edges, round_data)
    """
    alive = set(emitters) - set(collectors)  # pure emitters
    # Actually emitters and collectors can overlap. Let's keep all emitters alive.
    alive = set(emitters)

    spanner_edges = set()
    round_data = []

    # Include S⁻ and S⁺ edges
    for e in emitters:
        if e in s_minus:
            spanner_edges.add(ekey(e, s_minus[e]))
        if e in s_plus:
            spanner_edges.add(ekey(e, s_plus[e]))

    round_j = 0

    while len(alive) > 1:
        round_j += 1
        edges_before = len(spanner_edges)
        alive_before = len(alive)

        # Recompute S⁻ and S⁺ restricted to alive emitters
        # Each alive emitter's row minima/maxima among all collectors
        current_s_minus = {}
        current_s_plus = {}
        for e in alive:
            best_min = (None, float('inf'))
            best_max = (None, float('-inf'))
            for c in collectors:
                if e == c:
                    continue
                t = timestamps[ekey(e, c)]
                if t < best_min[1]:
                    best_min = (c, t)
                if t > best_max[1]:
                    best_max = (c, t)
            if best_min[0] is not None:
                current_s_minus[e] = best_min[0]
            if best_max[0] is not None:
                current_s_plus[e] = best_max[0]

        # Build collector -> emitter maps
        col_to_em_minus = defaultdict(set)
        col_to_em_plus = defaultdict(set)
        for e in alive:
            if e in current_s_minus:
                col_to_em_minus[current_s_minus[e]].add(e)
            if e in current_s_plus:
                col_to_em_plus[current_s_plus[e]].add(e)

        # Find delegation pairs: emitters sharing a collector
        can_delegate = {}  # eliminated_emitter -> (surviving_emitter, shared_collector)

        for c, es in col_to_em_minus.items():
            if len(es) >= 2:
                es_list = sorted(es)
                survivor = es_list[0]
                for e in es_list[1:]:
                    if e not in can_delegate:
                        can_delegate[e] = (survivor, c, 'minus')

        for c, es in col_to_em_plus.items():
            if len(es) >= 2:
                es_list = sorted(es)
                survivor = es_list[0]
                for e in es_list[1:]:
                    if e not in can_delegate:
                        can_delegate[e] = (survivor, c, 'plus')

        if not can_delegate:
            break

        # Limit to at most half
        if len(can_delegate) > len(alive) // 2:
            items = sorted(can_delegate.items())
            can_delegate = dict(items[:len(alive) // 2])

        # Process delegations
        missed_count = 0
        for e, (e_prime, shared_c, match_type) in can_delegate.items():
            # Add delegation edge: e -> shared_c -> e' (2-hop via collector)
            spanner_edges.add(ekey(e, shared_c))
            spanner_edges.add(ekey(e_prime, shared_c))

            # Missed collectors: those e reaches but e' doesn't
            e_cols = set()
            if e in current_s_minus:
                e_cols.add(current_s_minus[e])
            if e in current_s_plus:
                e_cols.add(current_s_plus[e])

            ep_cols = set()
            if e_prime in current_s_minus:
                ep_cols.add(current_s_minus[e_prime])
            if e_prime in current_s_plus:
                ep_cols.add(current_s_plus[e_prime])

            missed = e_cols - ep_cols - {shared_c}
            for c in missed:
                spanner_edges.add(ekey(e, c))
                missed_count += 1

        edges_added = len(spanner_edges) - edges_before
        eliminated = set(can_delegate.keys())
        alive -= eliminated

        round_data.append({
            'round': round_j,
            'alive_before': alive_before,
            'alive_after': len(alive),
            'eliminated': len(eliminated),
            'edges_added': edges_added,
            'missed_pairs': missed_count,
            'missed_per_eliminated': missed_count / max(len(eliminated), 1),
        })

    return spanner_edges, round_data, alive


def fireworks(n, timestamps):
    """
    Full fireworks algorithm.
    Returns: (total_edges, spanner_edges, tree_edge_count, round_data, k_emitters, k_collectors)
    """
    g_min, g_max = build_min_max_graphs(n, timestamps)
    emitters, collectors, tree_edges, s_minus, s_plus = compute_residual_bipartite(
        n, timestamps, g_min, g_max)

    delegation_edges, round_data, remaining = layered_delegation(
        emitters, collectors, timestamps, s_minus, s_plus)

    all_edges = tree_edges | delegation_edges

    # For remaining emitters (those that couldn't delegate), add all their
    # edges to collectors
    for e in remaining:
        for c in collectors:
            if e != c:
                all_edges.add(ekey(e, c))

    return (len(all_edges), all_edges, len(tree_edges), round_data,
            len(emitters), len(collectors))


def verify_temporal_spanner(n, timestamps, spanner_edges):
    """Check temporal reachability for all pairs. Only for small n."""
    if n > 14:
        return None

    adj = defaultdict(list)
    for (u, v) in spanner_edges:
        t = timestamps[ekey(u, v)]
        adj[u].append((v, t))
        adj[v].append((u, t))

    for source in range(n):
        # BFS with (vertex, last_time) states
        reachable = {source}
        frontier = [(source, -1)]
        visited = {(source, -1)}

        while frontier:
            next_frontier = []
            for v, last_t in frontier:
                for w, t in adj[v]:
                    if t > last_t and (w, t) not in visited:
                        visited.add((w, t))
                        reachable.add(w)
                        next_frontier.append((w, t))
            frontier = next_frontier

        if len(reachable) < n:
            return False
    return True


# ─── Experiments ──────────────────────────────────────────────────────────────

def run():
    ns = [6, 8, 10, 12, 14, 16, 20, 24, 30]
    trials = 50

    all_results = []
    summary = {}

    for n in ns:
        print(f"\n{'='*60}")
        print(f"n = {n}, C(n,2) = {n*(n-1)//2}")
        print(f"{'='*60}")

        edge_totals = []
        tree_totals = []
        emitter_counts = []
        collector_counts = []
        round_records = []
        cost_alive_pairs = []
        valid_count = 0
        check_count = 0

        for trial in range(trials):
            seed = n * 10000 + trial
            ts = random_temporal_clique(n, seed)
            total, edges, tree_ct, rounds, k_e, k_c = fireworks(n, ts)

            edge_totals.append(total)
            tree_totals.append(tree_ct)
            emitter_counts.append(k_e)
            collector_counts.append(k_c)
            round_records.append(rounds)

            for rd in rounds:
                cost_alive_pairs.append({
                    'alive': rd['alive_before'],
                    'cost': rd['edges_added'],
                    'n': n,
                    'round': rd['round'],
                    'missed': rd['missed_pairs'],
                    'eliminated': rd['eliminated'],
                })

            # Verify for small n
            if n <= 12 and trial < 10:
                check_count += 1
                v = verify_temporal_spanner(n, ts, edges)
                if v:
                    valid_count += 1

            all_results.append({
                'n': n, 'total': total, 'tree': tree_ct,
                'k_e': k_e, 'k_c': k_c, 'rounds': rounds,
            })

        avg_e = sum(edge_totals) / trials
        avg_tree = sum(tree_totals) / trials
        avg_ke = sum(emitter_counts) / trials
        avg_kc = sum(collector_counts) / trials
        avg_rounds = sum(len(r) for r in round_records) / trials
        bound = 2 * n - 3

        print(f"  Avg total edges: {avg_e:.1f} (2n-3 = {bound})")
        print(f"  Avg tree edges:  {avg_tree:.1f}")
        print(f"  Avg emitters:    {avg_ke:.1f}")
        print(f"  Avg collectors:  {avg_kc:.1f}")
        print(f"  Avg delegation rounds: {avg_rounds:.1f}")
        print(f"  edges/n: {avg_e/n:.2f}")
        if check_count > 0:
            print(f"  Validity: {valid_count}/{check_count}")

        # Per-round analysis
        by_round = defaultdict(lambda: {'costs': [], 'alives': [], 'missed': [],
                                         'elim': [], 'missed_per_elim': []})
        for rounds in round_records:
            for rd in rounds:
                j = rd['round']
                by_round[j]['costs'].append(rd['edges_added'])
                by_round[j]['alives'].append(rd['alive_before'])
                by_round[j]['missed'].append(rd['missed_pairs'])
                by_round[j]['elim'].append(rd['eliminated'])
                by_round[j]['missed_per_elim'].append(rd['missed_per_eliminated'])

        if by_round:
            print(f"\n  Per-round statistics:")
            print(f"  {'Rnd':>4} {'avg_alive':>10} {'avg_cost':>10} {'avg_ratio':>10} "
                  f"{'avg_missed':>11} {'avg_m/elim':>11} {'samples':>8}")
            for j in sorted(by_round.keys()):
                d = by_round[j]
                avg_a = sum(d['alives']) / len(d['alives'])
                avg_c = sum(d['costs']) / len(d['costs'])
                ratio = avg_c / avg_a if avg_a > 0 else 0
                avg_m = sum(d['missed']) / len(d['missed'])
                avg_me = sum(d['missed_per_elim']) / len(d['missed_per_elim'])
                print(f"  {j:4d} {avg_a:10.1f} {avg_c:10.1f} {ratio:10.3f} "
                      f"{avg_m:11.2f} {avg_me:11.3f} {len(d['costs']):8d}")

        summary[n] = {
            'avg_edges': avg_e,
            'avg_tree': avg_tree,
            'avg_ke': avg_ke,
            'avg_kc': avg_kc,
            'edges_per_n': avg_e / n,
            'cost_alive_pairs': cost_alive_pairs,
        }

    # ─── Task 2: Cost vs alive regression ─────────────────────────────────
    print(f"\n{'='*60}")
    print("TASK 2: cost_j vs |alive_j| regression")
    print(f"{'='*60}")

    all_pairs = []
    for n in ns:
        all_pairs.extend(summary[n]['cost_alive_pairs'])

    if all_pairs:
        xs = [p['alive'] for p in all_pairs]
        ys = [p['cost'] for p in all_pairs]
        n_pts = len(xs)

        if n_pts > 1:
            mean_x = sum(xs) / n_pts
            mean_y = sum(ys) / n_pts
            cov = sum((xs[i]-mean_x)*(ys[i]-mean_y) for i in range(n_pts)) / n_pts
            var_x = sum((xs[i]-mean_x)**2 for i in range(n_pts)) / n_pts

            if var_x > 0:
                a = cov / var_x
                b = mean_y - a * mean_x
                ss_res = sum((ys[i]-(a*xs[i]+b))**2 for i in range(n_pts))
                ss_tot = sum((ys[i]-mean_y)**2 for i in range(n_pts))
                r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
                print(f"  cost = {a:.3f} * alive + {b:.3f}")
                print(f"  R² = {r2:.4f}")
                print(f"  n_points = {n_pts}")

        # Also check cost vs n (not alive)
        xs_n = [p['n'] for p in all_pairs]
        if len(xs_n) > 1:
            mean_xn = sum(xs_n) / n_pts
            cov_n = sum((xs_n[i]-mean_xn)*(ys[i]-mean_y) for i in range(n_pts)) / n_pts
            var_xn = sum((xs_n[i]-mean_xn)**2 for i in range(n_pts)) / n_pts
            if var_xn > 0:
                a_n = cov_n / var_xn
                b_n = mean_y - a_n * mean_xn
                ss_res_n = sum((ys[i]-(a_n*xs_n[i]+b_n))**2 for i in range(n_pts))
                r2_n = 1 - ss_res_n/ss_tot if ss_tot > 0 else 0
                print(f"\n  cost = {a_n:.3f} * n + {b_n:.3f}")
                print(f"  R²(n) = {r2_n:.4f}")

    # ─── Task 4: Geometric series test ────────────────────────────────────
    print(f"\n{'='*60}")
    print("TASK 4: Geometric series test — does total_edges/k converge?")
    print(f"{'='*60}")
    print(f"  {'n':>4} {'edges':>8} {'2n-3':>6} {'k_e':>6} {'k_c':>6} "
          f"{'e/n':>6} {'e/k':>8} {'log2(k)':>8} {'e/(k·log)':>10}")

    for n in ns:
        s = summary[n]
        k = s['avg_ke']
        lk = math.log2(max(k, 2))
        ek = s['avg_edges'] / max(k, 1)
        ekl = s['avg_edges'] / max(k * lk, 1)
        print(f"  {n:4d} {s['avg_edges']:8.1f} {2*n-3:6d} {k:6.1f} {s['avg_kc']:6.1f} "
              f"{s['edges_per_n']:6.2f} {ek:8.2f} {lk:8.2f} {ekl:10.3f}")

    # ─── Task 5: Missed per eliminated ────────────────────────────────────
    print(f"\n{'='*60}")
    print("TASK 5: Missed collectors per eliminated emitter")
    print(f"{'='*60}")

    for n in ns:
        pairs = summary[n]['cost_alive_pairs']
        if not pairs:
            continue
        by_round = defaultdict(list)
        for p in pairs:
            by_round[p['round']].append(p['missed'] / max(p['eliminated'], 1))
        print(f"\n  n={n}:")
        for j in sorted(by_round.keys()):
            vals = by_round[j]
            avg = sum(vals) / len(vals)
            print(f"    Round {j}: missed/eliminated = {avg:.3f} (n={len(vals)})")

    # ─── Verdict ──────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("VERDICT")
    print(f"{'='*60}")

    ratios = [(n, summary[n]['edges_per_n']) for n in ns]
    print("\n  edges/n scaling:")
    for nv, r in ratios:
        print(f"    n={nv:3d}: edges/n = {r:.3f}")

    # Growth analysis
    r_first = ratios[0][1]
    r_last = ratios[-1][1]
    growth = r_last / r_first if r_first > 0 else 0
    expected_log = math.log2(ns[-1]) / math.log2(ns[0]) if ns[0] > 1 else 0

    print(f"\n  Growth factor (n={ns[0]} to n={ns[-1]}): {growth:.3f}x")
    print(f"  Expected if O(n log n): ~{expected_log:.2f}x")
    print(f"  Expected if O(n): ~1.0x")

    # Also check edges/k scaling
    k_ratios = []
    for n in ns:
        k = summary[n]['avg_ke']
        if k > 0:
            k_ratios.append((n, summary[n]['avg_edges'] / k))

    if len(k_ratios) >= 2:
        print(f"\n  edges/k scaling:")
        for nv, r in k_ratios:
            print(f"    n={nv:3d}: edges/k = {r:.3f}")

        kr_first = k_ratios[0][1]
        kr_last = k_ratios[-1][1]
        k_growth = kr_last / kr_first if kr_first > 0 else 0
        print(f"  edges/k growth: {k_growth:.3f}x")

    # Determine status
    if growth < 1.3:
        status = "supported"
        scales_with = "|alive_j|"
        total_cost = "O(n)"
    elif growth > 1.6:
        status = "refuted"
        scales_with = "n"
        total_cost = "O(n log n)"
    else:
        status = "inconclusive"
        scales_with = "unclear"
        total_cost = "unclear"

    print(f"\n### H22: Amortized delegation cost ({status})")
    print(f"**Verdict:** Per-round delegation cost scales with {scales_with}.")
    print(f"**Per-round cost scales with:** {scales_with}")
    print(f"**Total cost:** {total_cost}")


if __name__ == '__main__':
    run()
