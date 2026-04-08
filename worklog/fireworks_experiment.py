"""
Fireworks algorithm for temporal cliques: scaling experiment.

Tests whether layered delegation cost scales with |alive_j| (giving O(n) total)
or with n (giving O(n log n) total).

Reference: Casteigts-Peters-Schoeters, JCSS 2021.
"""

import random
import math
import itertools
from collections import defaultdict
import json
import sys

# ─── Temporal clique generation ───────────────────────────────────────────────

def random_temporal_clique(n, seed=None):
    """
    Generate K_n with distinct timestamps on each edge.
    Returns dict: (i,j) -> timestamp for i<j.
    Each unordered pair gets exactly one timestamp; all timestamps distinct.
    """
    rng = random.Random(seed)
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    num_edges = len(pairs)
    timestamps = rng.sample(range(1, 10 * num_edges + 1), num_edges)
    return {pair: t for pair, t in zip(pairs, timestamps)}


def edge_key(u, v):
    return (min(u, v), max(u, v))


# ─── G⁻ and G⁺: directed min/max edge graphs ────────────────────────────────

def compute_directed_graphs(n, timestamps):
    """
    G⁻: for each vertex v, the edge to each neighbor with minimum timestamp.
         Directed: v -> neighbor (outgoing = "I use this edge earliest").
         Actually: G⁻[v] = argmin_u t(v,u) for each v. Each v has one outgoing edge.

    In CPS: G⁻ is the "min-edge graph". For each vertex v, pick the neighbor u
    that minimizes t(v,u). This gives n directed edges (one per vertex).

    G⁺: same but max timestamp.
    """
    g_minus = {}  # v -> (neighbor, timestamp)
    g_plus = {}   # v -> (neighbor, timestamp)

    for v in range(n):
        min_t = float('inf')
        min_u = None
        max_t = float('-inf')
        max_u = None
        for u in range(n):
            if u == v:
                continue
            key = edge_key(v, u)
            t = timestamps[key]
            if t < min_t:
                min_t = t
                min_u = u
            if t > max_t:
                max_t = t
                max_u = u
        g_minus[v] = (min_u, min_t)
        g_plus[v] = (max_u, max_t)

    return g_minus, g_plus


# ─── In-tree T⁻ and out-tree T⁺ ─────────────────────────────────────────────

def build_in_tree(n, g_minus):
    """
    T⁻: directed graph where each v points to its g_minus neighbor.
    Sinks (vertices with no incoming edges that others point to, but
    actually sinks = vertices that no one points to...

    Wait: In T⁻, each vertex v has one outgoing edge v -> g_minus[v].
    Emitters = sinks of T⁻ = vertices with in-degree 0 in the reversed graph.
    Actually: emitters = vertices that are NOT pointed to by anyone.

    Let me reconsider. T⁻ is a functional graph (each node has out-degree 1).
    Its structure is a union of rho-shaped components (cycle + trees hanging off).

    CPS definition: X⁻ = emitters = sources of T⁻ (vertices with in-degree 0
    when we consider T⁻ as v -> g_minus(v) edges).

    No wait - re-reading CPS more carefully:

    For each vertex v, the "min-edge" from v goes to the vertex u that minimizes
    t(v,u). So G⁻ has edges v -> u meaning "v's earliest connection is to u".

    T⁻ is built from these edges. Sinks of T⁻ are vertices that don't point to
    anyone... but every vertex points to someone. So sinks don't exist in the
    functional graph.

    Let me redefine: In the CPS framework:
    - S⁻ = set of min-edges. Each vertex contributes its minimum-timestamp edge.
    - S⁺ = set of max-edges.
    - The edges form matchings in the bipartite residual.

    Actually, the CPS framework works differently. Let me re-implement properly.
    """
    # T⁻: each vertex v has outgoing edge to g_minus[v][0]
    # Build adjacency
    children = defaultdict(list)  # parent -> list of children pointing to it
    for v in range(n):
        target = g_minus[v][0]
        children[target].append(v)

    # In-degree of each vertex (how many point TO it)
    in_degree = defaultdict(int)
    for v in range(n):
        target = g_minus[v][0]
        in_degree[target] += 1

    # Leaves = vertices with in-degree 0 (no one points to them)
    # These are the "emitters" in CPS terminology - they emit to others
    # but receive from no one via min-edges
    emitters = [v for v in range(n) if in_degree[v] == 0]

    return children, emitters


def build_out_tree(n, g_plus):
    """
    T⁺: each vertex v has outgoing edge to g_plus[v].
    Collectors = vertices with in-degree 0 in T⁺.
    """
    in_degree = defaultdict(int)
    children = defaultdict(list)
    for v in range(n):
        target = g_plus[v][0]
        children[target].append(v)
        in_degree[target] += 1

    collectors = [v for v in range(n) if in_degree[v] == 0]
    return children, collectors


# ─── Dismountability ─────────────────────────────────────────────────────────

def find_dismountable(n, g_minus, g_plus, alive):
    """
    A vertex v is dismountable if g_minus(v) == g_plus(v), i.e., its min and
    max edge go to the same vertex. Or more generally, if it can be removed
    by adding at most 2 edges.

    CPS: v is dismountable if it is a leaf in both T⁻ and T⁺.
    A leaf of T⁻ means in-degree 0 in the min-edge graph.
    A leaf of T⁺ means in-degree 0 in the max-edge graph.
    """
    # Compute in-degrees among alive vertices
    in_deg_minus = defaultdict(int)
    in_deg_plus = defaultdict(int)

    for v in alive:
        target_minus = g_minus[v][0]
        if target_minus in alive:
            in_deg_minus[target_minus] += 1
        target_plus = g_plus[v][0]
        if target_plus in alive:
            in_deg_plus[target_plus] += 1

    dismountable = []
    for v in alive:
        if in_deg_minus.get(v, 0) == 0 and in_deg_plus.get(v, 0) == 0:
            dismountable.append(v)

    return dismountable


# ─── Core fireworks: layered delegation ───────────────────────────────────────

def fireworks_algorithm(n, timestamps):
    """
    Full fireworks algorithm. Returns:
    - total_edges: number of spanner edges
    - spanner_edges: set of (u,v) pairs in the spanner
    - round_data: list of dicts with per-round statistics
    - dismount_edges: edges added during dismounting phase
    """
    spanner_edges = set()
    round_data = []
    dismount_count = 0

    alive = set(range(n))

    # Recompute directed graphs restricted to alive vertices
    def restricted_g(alive_set):
        g_minus = {}
        g_plus = {}
        for v in alive_set:
            min_t = float('inf')
            min_u = None
            max_t = float('-inf')
            max_u = None
            for u in alive_set:
                if u == v:
                    continue
                key = edge_key(v, u)
                t = timestamps[key]
                if t < min_t:
                    min_t = t
                    min_u = u
                if t > max_t:
                    max_t = t
                    max_u = u
            if min_u is not None:
                g_minus[v] = (min_u, min_t)
            if max_u is not None:
                g_plus[v] = (max_u, max_t)
        return g_minus, g_plus

    # Phase 1: Dismounting
    while len(alive) > 1:
        g_minus, g_plus = restricted_g(alive)

        # Add all min and max edges to spanner
        for v in alive:
            if v in g_minus:
                u = g_minus[v][0]
                spanner_edges.add(edge_key(v, u))
            if v in g_plus:
                u = g_plus[v][0]
                spanner_edges.add(edge_key(v, u))

        dismountable = find_dismountable(n, g_minus, g_plus, alive)

        if not dismountable:
            break

        # Dismount one vertex at a time (could batch but sequential is cleaner)
        v = dismountable[0]
        alive.remove(v)
        dismount_count += 1

    if len(alive) <= 1:
        return len(spanner_edges), spanner_edges, round_data, dismount_count

    # Phase 2: Layered delegation on the non-dismountable residual
    # Now we have a bipartite structure: emitters and collectors

    g_minus, g_plus = restricted_g(alive)

    # Identify emitters and collectors in the residual
    in_deg_minus = defaultdict(int)
    in_deg_plus = defaultdict(int)
    for v in alive:
        if v in g_minus:
            in_deg_minus[g_minus[v][0]] += 1
        if v in g_plus:
            in_deg_plus[g_plus[v][0]] += 1

    # Emitters: leaves of T⁻ (in-degree 0 in min-edge graph)
    emitters = set(v for v in alive if in_deg_minus.get(v, 0) == 0)
    # Collectors: leaves of T⁺ (in-degree 0 in max-edge graph)
    collectors = set(v for v in alive if in_deg_plus.get(v, 0) == 0)

    # S⁻ matching: emitter -> collector via min-edges
    # S⁺ matching: emitter -> collector via max-edges
    # For each emitter, find its S⁻ partner (the collector it reaches via min-edge chain)
    # and S⁺ partner (via max-edge chain)

    def follow_chain(start, g, targets):
        """Follow the directed edges from start until hitting a vertex in targets."""
        visited = set()
        v = start
        while v not in targets and v not in visited:
            visited.add(v)
            if v not in g:
                return None
            v = g[v][0]
        if v in targets:
            return v
        return None

    # Build S⁻ and S⁺ matchings
    s_minus = {}  # emitter -> collector via min-edges
    s_plus = {}   # emitter -> collector via max-edges

    for e in emitters:
        c = follow_chain(e, g_minus, collectors)
        if c is not None:
            s_minus[e] = c
        c = follow_chain(e, g_plus, collectors)
        if c is not None:
            s_plus[e] = c

    # Layered delegation
    alive_emitters = set(emitters)
    round_j = 0

    while len(alive_emitters) > 8 and len(alive_emitters) > 1:
        round_j += 1
        edges_before = len(spanner_edges)

        # For each alive emitter, check if it can delegate via 2-hop journey
        # An emitter e can delegate if there exists another alive emitter e'
        # such that e and e' share a collector (via S⁻ or S⁺)

        # Build collector -> emitter maps for alive emitters
        collector_to_emitters_minus = defaultdict(set)
        collector_to_emitters_plus = defaultdict(set)

        for e in alive_emitters:
            if e in s_minus:
                collector_to_emitters_minus[s_minus[e]].add(e)
            if e in s_plus:
                collector_to_emitters_plus[s_plus[e]].add(e)

        # X_a: emitters that CAN delegate (share a collector with another emitter)
        # X_b: emitters that CANNOT delegate
        can_delegate = set()
        delegate_to = {}  # e -> e' (the emitter it delegates to)

        for c, es in collector_to_emitters_minus.items():
            if len(es) >= 2:
                es_list = sorted(es)
                # First one survives, rest delegate to it
                survivor = es_list[0]
                for e in es_list[1:]:
                    if e not in can_delegate:
                        can_delegate.add(e)
                        delegate_to[e] = survivor

        for c, es in collector_to_emitters_plus.items():
            if len(es) >= 2:
                es_list = sorted(es)
                survivor = es_list[0]
                for e in es_list[1:]:
                    if e not in can_delegate:
                        can_delegate.add(e)
                        delegate_to[e] = survivor

        if not can_delegate:
            # No more delegations possible
            break

        # Ensure at most half are eliminated
        if len(can_delegate) > len(alive_emitters) // 2:
            can_delegate_list = sorted(can_delegate)
            can_delegate = set(can_delegate_list[:len(alive_emitters) // 2])
            delegate_to = {e: delegate_to[e] for e in can_delegate}

        # Count missed collectors
        # A collector c is "missed" by eliminated emitter e if:
        # - e was connected to c via S⁻ or S⁺
        # - the emitter e delegates to (e') is NOT connected to c via S⁻ or S⁺
        missed_pairs = []
        for e in can_delegate:
            e_prime = delegate_to[e]
            # Collectors that e reaches
            e_collectors = set()
            if e in s_minus:
                e_collectors.add(s_minus[e])
            if e in s_plus:
                e_collectors.add(s_plus[e])
            # Collectors that e' reaches
            ep_collectors = set()
            if e_prime in s_minus:
                ep_collectors.add(s_minus[e_prime])
            if e_prime in s_plus:
                ep_collectors.add(s_plus[e_prime])

            missed = e_collectors - ep_collectors
            for c in missed:
                missed_pairs.append((e, c))
                # Add direct edge e-c to spanner (to cover the missed connection)
                spanner_edges.add(edge_key(e, c))

        # Also add delegation edges (e -> e' via their shared collector)
        for e in can_delegate:
            e_prime = delegate_to[e]
            spanner_edges.add(edge_key(e, e_prime))

        edges_added = len(spanner_edges) - edges_before

        round_data.append({
            'round': round_j,
            'alive_before': len(alive_emitters),
            'eliminated': len(can_delegate),
            'edges_added': edges_added,
            'missed_pairs': len(missed_pairs),
            'missed_per_eliminated': len(missed_pairs) / max(len(can_delegate), 1),
        })

        # Remove eliminated emitters
        alive_emitters -= can_delegate

    # Final phase: keep all edges for remaining emitters (≤ 8)
    for e in alive_emitters:
        for v in alive:
            if v != e:
                spanner_edges.add(edge_key(e, v))

    return len(spanner_edges), spanner_edges, round_data, dismount_count


def verify_spanner(n, timestamps, spanner_edges):
    """
    Verify that spanner_edges form a temporal spanner of K_n.
    A temporal spanner must preserve temporal reachability:
    for every pair (u,v), there must be a temporal path in the spanner
    (sequence of edges with strictly increasing timestamps).

    This is expensive (exponential in worst case), so we only check for small n.
    """
    if n > 12:
        return None  # too expensive

    # Build adjacency with timestamps for spanner
    adj = defaultdict(list)
    for (u, v) in spanner_edges:
        t = timestamps[edge_key(u, v)]
        adj[u].append((v, t))
        adj[v].append((u, t))

    # For each pair, check temporal reachability via BFS/DFS
    for u in range(n):
        # BFS: reachable from u via increasing timestamps
        # State: (current_vertex, last_timestamp)
        reachable = set()
        reachable.add(u)
        # Use BFS with states (vertex, last_time)
        from collections import deque
        queue = deque()
        queue.append((u, -1))
        visited_states = set()
        visited_states.add((u, -1))

        while queue:
            v, last_t = queue.popleft()
            for (w, t) in adj[v]:
                if t > last_t and (w, t) not in visited_states:
                    visited_states.add((w, t))
                    reachable.add(w)
                    queue.append((w, t))

        if len(reachable) < n:
            return False

    return True


def optimal_spanner_greedy(n, timestamps, spanner_edges):
    """
    Greedy edge removal: try removing edges one by one (highest timestamp first).
    If connectivity is preserved, remove it. Returns minimal edge count.
    Only feasible for small n.
    """
    if n > 10:
        return None

    edges_sorted = sorted(spanner_edges, key=lambda e: -timestamps[e])
    current = set(spanner_edges)

    for edge in edges_sorted:
        test = current - {edge}
        if verify_spanner(n, timestamps, test):
            current = test

    return len(current)


# ─── Main experiment ──────────────────────────────────────────────────────────

def run_experiments():
    ns = [6, 8, 10, 12, 14, 16, 20]
    num_trials = 50

    all_results = []
    summary_by_n = {}

    for n in ns:
        print(f"\n{'='*60}")
        print(f"n = {n}")
        print(f"{'='*60}")

        totals = []
        ratios_by_round = defaultdict(list)
        missed_by_round = defaultdict(list)
        cost_alive_pairs = []  # (alive_j, cost_j) across all trials

        for trial in range(num_trials):
            seed = n * 10000 + trial
            timestamps = random_temporal_clique(n, seed)
            total_edges, spanner, rounds, dismounts = fireworks_algorithm(n, timestamps)

            totals.append(total_edges)

            for rd in rounds:
                j = rd['round']
                alive = rd['alive_before']
                cost = rd['edges_added']
                missed = rd['missed_pairs']

                ratio = cost / alive if alive > 0 else 0
                ratios_by_round[j].append(ratio)
                missed_by_round[j].append(missed)
                cost_alive_pairs.append((alive, cost, n, j))

            # Verification for small n
            if n <= 10 and trial < 5:
                valid = verify_spanner(n, timestamps, spanner)
                if valid is False:
                    print(f"  WARNING: spanner NOT valid for trial {trial}!")

            all_results.append({
                'n': n,
                'trial': trial,
                'total_edges': total_edges,
                'num_rounds': len(rounds),
                'dismounts': dismounts,
                'rounds': rounds,
                'bound_2n3': 2*n - 3,
            })

        # Summary stats
        avg_edges = sum(totals) / len(totals)
        max_edges = max(totals)
        min_edges = min(totals)
        bound = 2 * n - 3

        # Compute k (typical number of emitters)
        emitter_counts = [r['rounds'][0]['alive_before'] if r['rounds'] else 0
                         for r in all_results if r['n'] == n]
        avg_k = sum(emitter_counts) / max(len(emitter_counts), 1) if emitter_counts else 0

        print(f"  Avg edges: {avg_edges:.1f}, range [{min_edges}, {max_edges}], 2n-3 = {bound}")
        print(f"  Avg emitters (k): {avg_k:.1f}")
        print(f"  Avg edges / n: {avg_edges/n:.2f}")
        if avg_k > 0:
            print(f"  Avg edges / k: {avg_edges/avg_k:.2f}")

        # Per-round ratio analysis
        print(f"\n  Per-round cost/alive ratios:")
        for j in sorted(ratios_by_round.keys()):
            rats = ratios_by_round[j]
            avg_r = sum(rats) / len(rats)
            max_r = max(rats)
            min_r = min(rats)
            print(f"    Round {j}: avg ratio={avg_r:.3f}, range=[{min_r:.3f}, {max_r:.3f}], "
                  f"n_samples={len(rats)}")

        # Missed collector analysis
        print(f"\n  Missed collectors per round:")
        for j in sorted(missed_by_round.keys()):
            ms = missed_by_round[j]
            avg_m = sum(ms) / len(ms)
            print(f"    Round {j}: avg missed={avg_m:.2f}")

        summary_by_n[n] = {
            'avg_edges': avg_edges,
            'bound_2n3': bound,
            'ratio_edges_n': avg_edges / n,
            'avg_k': avg_k,
            'cost_alive_pairs': cost_alive_pairs,
        }

    # ─── Task 4: Geometric series test ─────────────────────────────────────
    print(f"\n{'='*60}")
    print("TASK 4: Geometric series test")
    print(f"{'='*60}")

    print(f"\n  {'n':>4} {'avg_edges':>10} {'2n-3':>6} {'edges/n':>8} "
          f"{'edges/k':>8} {'log_k':>6} {'edges/(k*log_k)':>16}")

    for n in ns:
        s = summary_by_n[n]
        k = s['avg_k']
        log_k = math.log2(max(k, 1))
        edges_per_k = s['avg_edges'] / max(k, 1)
        edges_per_k_logk = s['avg_edges'] / max(k * log_k, 1)
        print(f"  {n:4d} {s['avg_edges']:10.1f} {s['bound_2n3']:6d} "
              f"{s['ratio_edges_n']:8.2f} {edges_per_k:8.2f} {log_k:6.2f} "
              f"{edges_per_k_logk:16.3f}")

    # ─── Task 5: Amortization argument ────────────────────────────────────
    print(f"\n{'='*60}")
    print("TASK 5: Missed collectors per eliminated emitter")
    print(f"{'='*60}")

    for n in ns:
        trials_for_n = [r for r in all_results if r['n'] == n and r['rounds']]
        if not trials_for_n:
            continue
        print(f"\n  n={n}:")
        by_round = defaultdict(list)
        for r in trials_for_n:
            for rd in r['rounds']:
                by_round[rd['round']].append(rd['missed_per_eliminated'])
        for j in sorted(by_round.keys()):
            vals = by_round[j]
            avg = sum(vals) / len(vals)
            print(f"    Round {j}: avg missed_per_eliminated = {avg:.3f} (n_samples={len(vals)})")

    # ─── Task 6: Comparison to optimal ────────────────────────────────────
    print(f"\n{'='*60}")
    print("TASK 6: Comparison to optimal (small n only)")
    print(f"{'='*60}")

    for n in [6, 8, 10]:
        print(f"\n  n={n}:")
        fw_totals = []
        opt_totals = []
        for trial in range(min(10, num_trials)):
            seed = n * 10000 + trial
            timestamps = random_temporal_clique(n, seed)
            total_edges, spanner, _, _ = fireworks_algorithm(n, timestamps)
            fw_totals.append(total_edges)

            opt = optimal_spanner_greedy(n, timestamps, spanner)
            if opt is not None:
                opt_totals.append(opt)

        bound = 2 * n - 3
        avg_fw = sum(fw_totals) / len(fw_totals)
        if opt_totals:
            avg_opt = sum(opt_totals) / len(opt_totals)
            print(f"    Avg fireworks: {avg_fw:.1f}, Avg greedy-opt: {avg_opt:.1f}, "
                  f"2n-3={bound}")
            print(f"    Fireworks ≤ 2n-3: {sum(1 for x in fw_totals if x <= bound)}/{len(fw_totals)}")
        else:
            print(f"    Avg fireworks: {avg_fw:.1f}, 2n-3={bound}")

    # ─── Cost vs alive scatter data ───────────────────────────────────────
    print(f"\n{'='*60}")
    print("COST vs ALIVE scatter (all rounds, all instances)")
    print(f"{'='*60}")
    print(f"  {'alive':>6} {'cost':>6} {'n':>4} {'round':>6} {'ratio':>8}")

    # Collect all (alive, cost) pairs
    all_pairs = []
    for r in all_results:
        for rd in r['rounds']:
            all_pairs.append((rd['alive_before'], rd['edges_added'], r['n'], rd['round']))

    # Sort by alive count
    all_pairs.sort()

    # Print sample (every ~10th entry for readability)
    step = max(1, len(all_pairs) // 40)
    for i in range(0, len(all_pairs), step):
        alive, cost, n_val, j = all_pairs[i]
        ratio = cost / alive if alive > 0 else 0
        print(f"  {alive:6d} {cost:6d} {n_val:4d} {j:6d} {ratio:8.3f}")

    # ─── Linear regression: cost = a * alive + b ─────────────────────────
    if all_pairs:
        xs = [p[0] for p in all_pairs]
        ys = [p[1] for p in all_pairs]
        n_pts = len(xs)
        mean_x = sum(xs) / n_pts
        mean_y = sum(ys) / n_pts
        cov_xy = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n_pts)) / n_pts
        var_x = sum((xs[i] - mean_x) ** 2 for i in range(n_pts)) / n_pts

        if var_x > 0:
            a = cov_xy / var_x
            b = mean_y - a * mean_x
            # R²
            ss_res = sum((ys[i] - (a * xs[i] + b)) ** 2 for i in range(n_pts))
            ss_tot = sum((ys[i] - mean_y) ** 2 for i in range(n_pts))
            r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else 0

            print(f"\n  Linear fit: cost = {a:.3f} * alive + {b:.3f}")
            print(f"  R² = {r_sq:.4f}")

    # ─── Final verdict ────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("VERDICT")
    print(f"{'='*60}")

    # Check if edges/n converges
    ratios = [(n, summary_by_n[n]['ratio_edges_n']) for n in ns]
    print("\n  edges/n across n values:")
    for n_val, r in ratios:
        print(f"    n={n_val}: {r:.3f}")

    # Check if it's growing
    first_ratio = ratios[0][1]
    last_ratio = ratios[-1][1]
    growth = last_ratio / first_ratio if first_ratio > 0 else 0

    log_growth = math.log2(ns[-1]) / math.log2(ns[0]) if ns[0] > 1 else 0

    print(f"\n  Ratio growth from n={ns[0]} to n={ns[-1]}: {growth:.3f}x")
    print(f"  Expected if O(n log n): ~{log_growth:.2f}x")
    print(f"  Expected if O(n): ~1.0x")

    if growth < 1.3:
        status = "supported"
        verdict = "Per-round cost appears proportional to |alive_j|. Total cost O(n)."
    elif growth > 1.8:
        status = "refuted"
        verdict = "Per-round cost appears proportional to n, not |alive_j|. Total cost O(n log n)."
    else:
        status = "inconclusive"
        verdict = "Evidence is mixed. Need larger n or tighter analysis."

    print(f"\n### H22: Amortized delegation cost ({status})")
    print(f"**Verdict:** {verdict}")
    if growth < 1.3:
        print(f"**Per-round cost scales with:** |alive_j|")
        print(f"**Total cost:** O(n)")
    elif growth > 1.8:
        print(f"**Per-round cost scales with:** n")
        print(f"**Total cost:** O(n log n)")
    else:
        print(f"**Per-round cost scales with:** unclear")
        print(f"**Total cost:** unclear")


if __name__ == '__main__':
    run_experiments()
