"""
Fireworks v5: Correct S⁻/S⁺ matchings via tree chain following.

Key fix: S⁻[e] = the collector that emitter e reaches by following G⁻ tree edges
upward. S⁺[e] = same for G⁺. These are forest-induced matchings, NOT row min/max
of the bipartite adjacency matrix.

The G⁻ forest: each vertex points to its minimum-timestamp neighbor.
Roots of this forest = emitters (no incoming edges).
Following the tree from an emitter leads to... wait, emitters ARE the roots.
So an emitter can't follow G⁻ upward — it IS the root.

Let me re-read CPS more carefully.

Actually: G⁻ has each vertex pointing to its min-timestamp neighbor. The roots
are vertices that form cycles (in the functional graph). After cycle-breaking,
roots = one vertex per cycle.

Emitters are vertices with in-degree 0 in G⁻ (leaves of the reversed tree).
Collectors are vertices with in-degree 0 in G⁺.

S⁻ matching: each emitter e follows G⁻ edges (e -> g⁻(e) -> g⁻(g⁻(e)) -> ...)
until reaching a collector in the G⁺ tree. But this doesn't make sense either —
G⁻ and G⁺ are different forests.

OK let me think about this more carefully from first principles.

In CPS:
- T⁻ is an in-branching (edges directed toward roots). Roots = sinks.
  Each non-root vertex has exactly one outgoing edge (to its min-neighbor).
  Emitters = roots of T⁻ (they receive edges but don't send).
  Wait no — if T⁻ directs toward roots, roots receive, leaves send.

Actually I think the confusion is about direction conventions. Let me be precise:

G⁻: functional graph where v -> argmin_u t(v,u).
  - This gives each vertex an outgoing edge.
  - "Sinks" of this aren't natural since every vertex has out-degree 1.
  - After cycle-breaking, we get a forest.
  - Vertices with in-degree 0 = leaves (no one points TO them).
  - Roots = cycle vertices = vertices that many point to.

CPS calls the roots "emitters" — vertices at the center of the trees.
No wait, I need to look at this from the temporal graph perspective.

In a temporal graph:
- G⁻(v) = the edge from v with minimum timestamp = v's "first" connection.
  This edge goes OUT from v at the earliest time.
- An emitter is a vertex that "emits" first — its minimum edge is earlier
  than its neighbors'. In the G⁻ forest, emitters are vertices that others
  point to (high in-degree) — they're the popular early-connection targets.

Actually, the simplest interpretation: In G⁻, emitters = roots. Non-emitters
follow G⁻ edges toward emitters. Similarly, in G⁺, collectors = roots, and
non-collectors follow G⁺ edges toward collectors.

S⁻ matching: each emitter e doesn't follow G⁻ (it's a root). Instead,
S⁻ matches emitter e to the collector c such that c is reachable from e
by following G⁺ edges. No — that's S⁺.

Hmm. Let me just try: S⁻[e] = the root of the G⁺ tree that e belongs to.
S⁺[e] = the root of the G⁻ tree that... no, e IS a root of G⁻.

I think the correct interpretation is:
- S⁻ matches emitter e to a collector c if there's a path in G⁻ from c to e.
  i.e., c reaches e by following min-edges. But c is a collector (G⁺ root),
  and in G⁻, c follows its min-edge to some vertex, which follows its min-edge...
  eventually reaching an emitter (G⁻ root). S⁻[e] = set of collectors in the
  G⁻ subtree rooted at e.

Wait, that gives a set, not a matching. Let me reconsider.

Actually, I think S⁻ is: for each emitter e, its min-timestamp edge to a
collector. And S⁺ is: for each emitter e, its max-timestamp edge to a collector.
This IS row min/max of the bipartite graph. My original implementation was right.

The CPS halving guarantee must work differently than I thought. Let me just
implement it correctly and see what happens.

ALTERNATIVE INTERPRETATION: S⁻ and S⁺ are the two perfect matchings between
emitters and collectors that arise because:
- Each non-emitter/collector vertex v belongs to exactly one G⁻ tree (rooted
  at an emitter) and exactly one G⁺ tree (rooted at a collector).
- This induces a bipartite graph: emitter e is connected to collector c if
  some vertex v is in both e's G⁻ subtree and c's G⁺ subtree.
- S⁻ and S⁺ are specific matchings extracted from this bipartite structure.

Let me implement THIS version.
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


def build_functional_graph(n, timestamps, mode='min'):
    """Build G⁻ (mode='min') or G⁺ (mode='max')."""
    g = {}
    for v in range(n):
        best = (None, float('inf') if mode == 'min' else float('-inf'))
        for u in range(n):
            if u == v:
                continue
            t = timestamps[ekey(v, u)]
            if mode == 'min' and t < best[1]:
                best = (u, t)
            elif mode == 'max' and t > best[1]:
                best = (u, t)
        g[v] = best
    return g


def build_forest_with_subtrees(n, g):
    """
    Build forest from functional graph g.
    Returns:
    - roots: set of root vertices
    - subtree: dict root -> set of vertices in that root's subtree (including root)
    - tree_edges: set of undirected edges
    - root_of: dict v -> its root
    """
    visited = set()
    roots = set()
    tree_edges = set()
    parent = {}

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
            idx = path.index(v)
            roots.add(v)
            parent[v] = None
            visited.add(v)
            for i in range(idx + 1, len(path)):
                node = path[i]
                parent[node] = g[node][0]
                tree_edges.add(ekey(node, g[node][0]))
                visited.add(node)
            for i in range(idx - 1, -1, -1):
                node = path[i]
                parent[node] = g[node][0]
                tree_edges.add(ekey(node, g[node][0]))
                visited.add(node)
        else:
            for node in path:
                parent[node] = g[node][0]
                tree_edges.add(ekey(node, g[node][0]))
                visited.add(node)

    for v in range(n):
        if v not in parent:
            parent[v] = None
            roots.add(v)

    # Build root_of mapping
    root_of = {}
    for v in range(n):
        r = v
        seen = set()
        while parent.get(r) is not None and r not in seen:
            seen.add(r)
            r = parent[r]
        root_of[v] = r

    # Build subtrees
    subtree = defaultdict(set)
    for v in range(n):
        subtree[root_of[v]].add(v)

    return roots, subtree, tree_edges, root_of


def analyze_fireworks(n, timestamps):
    """
    Proper fireworks analysis using forest-induced matchings.

    The bipartite connection between emitters and collectors:
    Each non-root vertex v belongs to G⁻ subtree of some emitter e,
    and G⁺ subtree of some collector c. This creates a bipartite graph.

    S⁻ and S⁺ are matchings in this bipartite graph.
    CPS extracts them from the min/max edges between the two sides.
    """
    g_min = build_functional_graph(n, timestamps, 'min')
    g_max = build_functional_graph(n, timestamps, 'max')

    emitters, subtree_min, edges_min, root_min = build_forest_with_subtrees(n, g_min)
    collectors, subtree_max, edges_max, root_max = build_forest_with_subtrees(n, g_max)

    tree_edges = edges_min | edges_max
    k_e = len(emitters)
    k_c = len(collectors)

    # Build the bipartite connection graph:
    # emitter e is connected to collector c if there exists a vertex v
    # in both subtree_min[e] and subtree_max[c].
    emitter_to_collectors = defaultdict(set)
    collector_to_emitters = defaultdict(set)

    for v in range(n):
        e = root_min[v]  # v's emitter
        c = root_max[v]  # v's collector
        emitter_to_collectors[e].add(c)
        collector_to_emitters[c].add(e)

    # S⁻ matching: for each emitter e, pick the collector c in its connection
    # set with the minimum timestamp direct edge.
    # S⁺ matching: same but maximum timestamp.
    emitter_list = sorted(emitters)
    collector_list = sorted(collectors)

    s_minus = {}  # emitter -> collector
    s_plus = {}

    for e in emitter_list:
        connected_collectors = emitter_to_collectors[e]
        if not connected_collectors:
            continue
        best_min = (None, float('inf'))
        best_max = (None, float('-inf'))
        for c in connected_collectors:
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

    # Layered delegation using forest-induced structure
    alive = set(emitter_list)
    spanner_edges = set(tree_edges)
    round_data = []
    round_j = 0

    # Add matching edges
    for e in emitter_list:
        if e in s_minus:
            spanner_edges.add(ekey(e, s_minus[e]))
        if e in s_plus:
            spanner_edges.add(ekey(e, s_plus[e]))

    while len(alive) > 1:
        round_j += 1
        alive_before = len(alive)
        edges_before = len(spanner_edges)

        # Recompute matchings for alive emitters
        # Use the forest-induced bipartite structure
        cur_s_minus = {}
        cur_s_plus = {}

        for e in alive:
            connected = emitter_to_collectors[e]
            if not connected:
                continue
            best_min = (None, float('inf'))
            best_max = (None, float('-inf'))
            for c in connected:
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

        # Collector -> alive emitters sharing it
        col_to_em = defaultdict(set)
        for e in alive:
            if e in cur_s_minus:
                col_to_em[cur_s_minus[e]].add(e)
            if e in cur_s_plus:
                col_to_em[cur_s_plus[e]].add(e)

        # Build delegation map
        can_delegate = {}
        for c, es in sorted(col_to_em.items(), key=lambda x: -len(x[1])):
            if len(es) >= 2:
                es_list = sorted(es - set(can_delegate.keys()))
                if len(es_list) >= 2:
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

        # Process delegations
        missed_count = 0
        for e, (e_prime, shared_c) in can_delegate.items():
            spanner_edges.add(ekey(e, shared_c))
            spanner_edges.add(ekey(e_prime, shared_c))

            # Missed collectors
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
            for mc in missed:
                spanner_edges.add(ekey(e, mc))
                missed_count += 1

        edges_added = len(spanner_edges) - edges_before
        eliminated = set(can_delegate.keys())
        alive -= eliminated

        # Count isolated emitters (those with unique collectors in both S- and S+)
        isolated = 0
        for e in alive:
            e_cols = set()
            if e in cur_s_minus:
                e_cols.add(cur_s_minus[e])
            if e in cur_s_plus:
                e_cols.add(cur_s_plus[e])
            is_iso = all(len(col_to_em.get(c, set()) - eliminated) <= 1 for c in e_cols)
            if is_iso:
                isolated += 1

        round_data.append({
            'round': round_j,
            'alive_before': alive_before,
            'alive_after': len(alive),
            'eliminated': len(eliminated),
            'edges_added': edges_added,
            'missed': missed_count,
            'missed_per_elim': missed_count / max(len(eliminated), 1),
            'isolated_after': isolated,
            'elim_fraction': len(eliminated) / alive_before,
        })

    # Remaining emitters: add edges to all collectors
    remaining_edges = 0
    for e in alive:
        for c in collector_list:
            if e != c:
                spanner_edges.add(ekey(e, c))
                remaining_edges += 1

    return {
        'total': len(spanner_edges),
        'tree': len(tree_edges),
        'k_e': k_e,
        'k_c': k_c,
        'remaining_emitters': len(alive),
        'remaining_edges': remaining_edges,
        'rounds': round_data,
        'emitter_collector_overlap': len(emitters & collectors),
        'avg_collectors_per_emitter': (
            sum(len(emitter_to_collectors[e]) for e in emitters) / max(k_e, 1)
        ),
    }


def run():
    ns = [8, 12, 16, 20, 30, 40, 50, 60, 80, 100]
    trials = 100

    print("FIREWORKS v5: FOREST-INDUCED MATCHINGS")
    print("=" * 70)

    summary = {}

    for n in ns:
        print(f"\nn = {n}")
        print("-" * 40)

        results = []
        for trial in range(trials):
            seed = n * 10000 + trial
            ts = random_temporal_clique(n, seed)
            r = analyze_fireworks(n, ts)
            results.append(r)

        avg = lambda key: sum(r[key] for r in results) / trials

        print(f"  k_e={avg('k_e'):.1f}, k_c={avg('k_c'):.1f}, "
              f"overlap={avg('emitter_collector_overlap'):.1f}")
        print(f"  Avg collectors per emitter (forest-induced): "
              f"{avg('avg_collectors_per_emitter'):.2f}")
        print(f"  Total edges: {avg('total'):.1f}, tree: {avg('tree'):.1f}, "
              f"remaining: {avg('remaining_edges'):.1f}")
        print(f"  Remaining emitters: {avg('remaining_emitters'):.2f}")
        print(f"  edges/n = {avg('total')/n:.3f}")

        # Per-round stats
        by_round = defaultdict(lambda: defaultdict(list))
        for r in results:
            for rd in r['rounds']:
                j = rd['round']
                for key, val in rd.items():
                    if isinstance(val, (int, float)):
                        by_round[j][key].append(val)

        if by_round:
            print(f"\n  {'Rnd':>4} {'alive':>6} {'elim':>5} {'frac':>6} "
                  f"{'edges':>6} {'miss/el':>8} {'isolated':>9} samples")
            for j in sorted(by_round.keys()):
                d = by_round[j]
                a = lambda k: sum(d[k])/len(d[k])
                print(f"  {j:4d} {a('alive_before'):6.1f} {a('eliminated'):5.1f} "
                      f"{a('elim_fraction'):6.3f} {a('edges_added'):6.1f} "
                      f"{a('missed_per_elim'):8.3f} {a('isolated_after'):9.1f} "
                      f"{len(d['alive_before']):5d}")

        summary[n] = {
            'edges_per_n': avg('total') / n,
            'avg_total': avg('total'),
            'avg_ke': avg('k_e'),
            'avg_kc': avg('k_c'),
            'avg_remaining': avg('remaining_emitters'),
            'avg_coll_per_emit': avg('avg_collectors_per_emitter'),
        }

    # Cross-n analysis
    print(f"\n\n{'='*70}")
    print("SCALING ANALYSIS")
    print(f"{'='*70}")

    print(f"\n{'n':>4} {'k_e':>5} {'k_c':>5} {'remain':>7} {'e/n':>6} "
          f"{'rem/k':>7} {'coll/emit':>10}")
    for n in ns:
        s = summary[n]
        print(f"{n:4d} {s['avg_ke']:5.1f} {s['avg_kc']:5.1f} "
              f"{s['avg_remaining']:7.2f} {s['edges_per_n']:6.3f} "
              f"{s['avg_remaining']/max(s['avg_ke'],1):7.3f} "
              f"{s['avg_coll_per_emit']:10.2f}")

    # Key: does forest-induced matching give more connections?
    print(f"\n  If each emitter connects to ~{summary[ns[-1]]['avg_coll_per_emit']:.1f} "
          f"collectors via the forest,")
    print(f"  there are more collision opportunities than with just 2 (row min/max).")

    # Check remaining/k trend
    rk = [(n, summary[n]['avg_remaining'] / max(summary[n]['avg_ke'], 1)) for n in ns]
    print(f"\n  remaining/k trend:")
    for nv, r in rk:
        print(f"    n={nv:4d}: {r:.3f}")

    # Fit
    xs = [math.log(summary[n]['avg_ke']) for n in ns]
    ys = [summary[n]['avg_remaining'] for n in ns]
    n_pts = len(xs)
    mx = sum(xs)/n_pts; my = sum(ys)/n_pts
    cov = sum((xs[i]-mx)*(ys[i]-my) for i in range(n_pts))/n_pts
    vx = sum((xs[i]-mx)**2 for i in range(n_pts))/n_pts
    if vx > 0:
        b = cov/vx; a = my - b*mx
        print(f"\n  remaining = {a:.2f} + {b:.2f} * ln(k)")

    # Power law
    lys = [math.log(max(y, 0.1)) for y in ys]
    mly = sum(lys)/n_pts
    cov2 = sum((xs[i]-mx)*(lys[i]-mly) for i in range(n_pts))/n_pts
    b2 = cov2/vx
    a2 = math.exp(mly - b2*mx)
    print(f"  remaining = {a2:.3f} * k^{b2:.3f}")

    # Verdict
    r_first = summary[ns[0]]['edges_per_n']
    r_last = summary[ns[-1]]['edges_per_n']
    growth = r_last / r_first

    print(f"\n  edges/n growth: {growth:.3f}x (from n={ns[0]} to n={ns[-1]})")
    print(f"  ln(n) growth: {math.log(ns[-1])/math.log(ns[0]):.2f}x")

    if growth < 1.25:
        status = "supported"
    elif growth > 1.5:
        status = "refuted"
    else:
        status = "inconclusive"

    print(f"\n### H22: Amortized delegation cost ({status})")


if __name__ == '__main__':
    run()
