"""
H11: O(n) heuristic budget construction for temporal spanners.

Tests four variants (A: column popularity, B: timestamp spread, C: column coverage,
D: combined) on random all-distinct k×k temporal bipartite cliques.

Each variant uses 1 round of neighbor announcements + local selection.
Budget per A-vertex: floor(c * log(k)) + 2 for c ∈ {0.5, 1.0, 1.5, 2.0}.
"""

import random
import math
import statistics
from collections import defaultdict
import heapq
import sys

random.seed(42)

# ---------------------------------------------------------------------------
# Temporal reachability engine (from H10)
# ---------------------------------------------------------------------------

def build_adj(k, edges):
    adj = defaultdict(list)
    for (a, b, t) in edges:
        adj[a].append((b, t))
        adj[b].append((a, t))
    return adj

def temporal_reachable_from(source, adj):
    best = {source: 0}
    queue = [(0, source)]
    heapq.heapify(queue)
    while queue:
        t_arr, u = heapq.heappop(queue)
        if t_arr > best.get(u, float('inf')):
            continue
        for (v, t_edge) in adj[u]:
            if t_edge >= t_arr:
                if t_edge < best.get(v, float('inf')):
                    best[v] = t_edge
                    heapq.heappush(queue, (t_edge, v))
    return set(best.keys())

def all_pairs_reach(k, edges):
    adj = build_adj(k, edges)
    n = 2 * k
    reach = {}
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        for d in range(n):
            if s != d:
                reach[(s, d)] = d in r
    return reach

def count_reachable_pairs(k, edges):
    """Count number of reachable (s,d) pairs, s≠d."""
    adj = build_adj(k, edges)
    n = 2 * k
    count = 0
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        count += len(r) - 1  # exclude self
    return count

def reachability_fraction(k, edges, orig_reach):
    """Fraction of originally-reachable pairs that are still reachable."""
    adj = build_adj(k, edges)
    n = 2 * k
    orig_count = sum(1 for v in orig_reach.values() if v)
    if orig_count == 0:
        return 1.0
    preserved = 0
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        for d in range(n):
            if s != d and orig_reach.get((s, d), False):
                if d in r:
                    preserved += 1
    return preserved / orig_count

def is_fully_reachable(k, edges):
    """Check if all n*(n-1) directed pairs are reachable."""
    adj = build_adj(k, edges)
    n = 2 * k
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        if len(r) < n:
            return False
    return True

def failing_pairs_by_type(k, edges, orig_reach):
    """Return counts of failing pairs by type: AA, AB, BA, BB."""
    adj = build_adj(k, edges)
    n = 2 * k
    fails = {'AA': 0, 'AB': 0, 'BA': 0, 'BB': 0}
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        for d in range(n):
            if s != d and orig_reach.get((s, d), False) and d not in r:
                s_type = 'A' if s < k else 'B'
                d_type = 'A' if d < k else 'B'
                fails[s_type + d_type] += 1
    return fails


# ---------------------------------------------------------------------------
# Matrix generation with reachability filter
# ---------------------------------------------------------------------------

def random_matrix(k):
    vals = list(range(1, k*k+1))
    random.shuffle(vals)
    return [vals[i*k:(i+1)*k] for i in range(k)]

def matrix_to_edges(k, M):
    return {(i, k+j, M[i][j]) for i in range(k) for j in range(k)}

def generate_reachable_matrices(k, count):
    """Generate `count` random matrices where the full graph is temporally fully reachable."""
    matrices = []
    attempts = 0
    while len(matrices) < count:
        M = random_matrix(k)
        edges = matrix_to_edges(k, M)
        attempts += 1
        if is_fully_reachable(k, edges):
            matrices.append(M)
    return matrices, attempts


# ---------------------------------------------------------------------------
# Heuristic variants
# ---------------------------------------------------------------------------

def compute_row_info(k, M):
    """For each A-vertex (row i), find min and max column indices."""
    info = []
    for i in range(k):
        row = M[i]
        min_j = min(range(k), key=lambda j: row[j])
        max_j = max(range(k), key=lambda j: row[j])
        info.append((min_j, max_j))
    return info

def compute_column_popularity(k, row_info):
    """For each B-vertex (column j), count how many A-vertices have it as min or max."""
    popularity = [0] * k
    for (min_j, max_j) in row_info:
        popularity[min_j] += 1
        popularity[max_j] += 1
    return popularity


def heuristic_A(k, M, c):
    """Column popularity: keep min+max, then most popular columns."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)
    col_pop = compute_column_popularity(k, row_info)

    kept_edges = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        # Always keep min and max
        kept_edges.add((i, k + min_j, M[i][min_j]))
        kept_edges.add((i, k + max_j, M[i][max_j]))

        # Remaining edges sorted by column popularity (descending)
        remaining = [(j, col_pop[j]) for j in range(k) if j != min_j and j != max_j]
        remaining.sort(key=lambda x: -x[1])

        extras = budget_per_node - 2
        for j, _ in remaining[:extras]:
            kept_edges.add((i, k + j, M[i][j]))

    return kept_edges


def heuristic_B(k, M, c):
    """Timestamp spread: keep min+max, then greedily maximize timestamp dispersion."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)

    kept_edges = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        kept_edges.add((i, k + min_j, M[i][min_j]))
        kept_edges.add((i, k + max_j, M[i][max_j]))

        kept_times = {M[i][min_j], M[i][max_j]}
        remaining = [j for j in range(k) if j != min_j and j != max_j]

        extras = budget_per_node - 2
        for _ in range(min(extras, len(remaining))):
            # Pick the edge whose timestamp is most distant from all kept timestamps
            best_j = None
            best_dist = -1
            for j in remaining:
                t = M[i][j]
                min_dist = min(abs(t - kt) for kt in kept_times)
                if min_dist > best_dist:
                    best_dist = min_dist
                    best_j = j
            if best_j is not None:
                kept_edges.add((i, k + best_j, M[i][best_j]))
                kept_times.add(M[i][best_j])
                remaining.remove(best_j)

    return kept_edges


def heuristic_C(k, M, c):
    """Column coverage: keep min+max, then prioritize columns with fewest incoming edges."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)

    # Phase 1: everyone keeps min+max
    col_kept_count = [0] * k
    for i in range(k):
        min_j, max_j = row_info[i]
        col_kept_count[min_j] += 1
        col_kept_count[max_j] += 1

    # Phase 2: each A-vertex picks remaining edges to least-covered columns
    kept_edges = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        kept_edges.add((i, k + min_j, M[i][min_j]))
        kept_edges.add((i, k + max_j, M[i][max_j]))

        remaining = [(j, col_kept_count[j]) for j in range(k) if j != min_j and j != max_j]
        remaining.sort(key=lambda x: x[1])  # ascending: least covered first

        extras = budget_per_node - 2
        for j, _ in remaining[:extras]:
            kept_edges.add((i, k + j, M[i][j]))
            col_kept_count[j] += 1  # update for subsequent rows

    return kept_edges


def heuristic_D(k, M, c):
    """Combined: column popularity × timestamp distance."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)
    col_pop = compute_column_popularity(k, row_info)

    kept_edges = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        kept_edges.add((i, k + min_j, M[i][min_j]))
        kept_edges.add((i, k + max_j, M[i][max_j]))

        kept_times = {M[i][min_j], M[i][max_j]}
        remaining = [j for j in range(k) if j != min_j and j != max_j]

        # Score each remaining edge
        extras = budget_per_node - 2
        scored = []
        for j in remaining:
            t = M[i][j]
            min_dist = min(abs(t - kt) for kt in kept_times)
            pop = col_pop[j]
            # Normalize: pop in [0, 2k], dist in [0, k²]
            # Use product (both matter)
            score = pop * min_dist
            scored.append((j, score))

        scored.sort(key=lambda x: -x[1])
        for j, _ in scored[:extras]:
            kept_edges.add((i, k + j, M[i][j]))

    return kept_edges


# ---------------------------------------------------------------------------
# Best-response repair (1 round)
# ---------------------------------------------------------------------------

def one_round_repair(k, kept_edges, M, orig_reach):
    """
    Check each non-kept edge; add it if it creates new reachability.
    One pass through all missing edges, sorted by timestamp.
    """
    all_edges = matrix_to_edges(k, M)
    missing = all_edges - kept_edges
    # Sort by timestamp to try earlier edges first (they open more paths)
    missing_sorted = sorted(missing, key=lambda e: e[2])

    repaired = set(kept_edges)
    for e in missing_sorted:
        # Check if adding this edge creates any new reachability
        trial = repaired | {e}
        # Quick check: does it connect any new pair?
        adj_before = build_adj(k, repaired)
        adj_after = build_adj(k, trial)

        # Only check nodes involved in this edge
        a, b, t = e
        # Check if reach from a or b increases
        r_a_before = temporal_reachable_from(a, adj_before)
        r_a_after = temporal_reachable_from(a, adj_after)
        r_b_before = temporal_reachable_from(b, adj_before)
        r_b_after = temporal_reachable_from(b, adj_after)

        if len(r_a_after) > len(r_a_before) or len(r_b_after) > len(r_b_before):
            repaired = trial

    return repaired


def one_round_repair_full(k, kept_edges, M, orig_reach):
    """
    More thorough repair: add edge if it increases total reachability count.
    """
    all_edges = matrix_to_edges(k, M)
    missing = all_edges - kept_edges
    missing_sorted = sorted(missing, key=lambda e: e[2])

    repaired = set(kept_edges)
    current_reach_count = count_reachable_pairs(k, repaired)

    for e in missing_sorted:
        trial = repaired | {e}
        new_count = count_reachable_pairs(k, trial)
        if new_count > current_reach_count:
            repaired = trial
            current_reach_count = new_count

    return repaired


# ---------------------------------------------------------------------------
# Best-response from full (H10 baseline)
# ---------------------------------------------------------------------------

def best_response_from_full(k, M, n_orderings=5):
    """Run best-response dynamics from the full graph. Return best result."""
    all_e = matrix_to_edges(k, M)
    orig = all_pairs_reach(k, all_e)
    n = 2 * k
    best = None

    for _ in range(n_orderings):
        cur = set(all_e)
        order = list(range(n))
        random.shuffle(order)
        changed = True
        rounds = 0
        while changed and rounds < 50:
            changed = False
            rounds += 1
            for node in order:
                while True:
                    node_e = [e for e in cur if e[0] == node or e[1] == node]
                    found = False
                    for e in node_e:
                        trial = cur - {e}
                        # Check if reachability preserved
                        cur_reach = all_pairs_reach(k, trial)
                        ok = True
                        for pair, was in orig.items():
                            if was and not cur_reach.get(pair, False):
                                ok = False
                                break
                        if ok:
                            cur = trial
                            changed = True
                            found = True
                            break
                    if not found:
                        break
        if best is None or len(cur) < len(best):
            best = cur

    return best


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

VARIANTS = {
    'A': heuristic_A,
    'B': heuristic_B,
    'C': heuristic_C,
    'D': heuristic_D,
}

C_VALUES = [0.5, 1.0, 1.5, 2.0]
K_VALUES = [3, 4, 5, 6, 7, 8]
N_MATRICES = 50

def run_experiment():
    print("=" * 80)
    print("H11: O(n) Heuristic Budget Construction for Temporal Spanners")
    print("=" * 80)
    print(f"Matrices per k: {N_MATRICES} (reachable only)")
    print(f"k values: {K_VALUES}")
    print(f"c values: {C_VALUES}")
    print(f"Variants: A (col popularity), B (timestamp spread), C (col coverage), D (combined)")
    print()

    # Pregenerate matrices
    all_matrices = {}
    all_orig_reach = {}
    for k in K_VALUES:
        print(f"Generating {N_MATRICES} reachable matrices for k={k}...", end=" ", flush=True)
        matrices, attempts = generate_reachable_matrices(k, N_MATRICES)
        print(f"done ({attempts} attempts, {attempts/N_MATRICES:.1f}x overhead)")
        all_matrices[k] = matrices
        # Precompute original reachability
        reach_list = []
        for M in matrices:
            edges = matrix_to_edges(k, M)
            reach_list.append(all_pairs_reach(k, edges))
        all_orig_reach[k] = reach_list

    # Also precompute best-response baselines
    print("\nComputing best-response baselines (H10)...")
    br_baselines = {}
    for k in K_VALUES:
        if k > 7:
            print(f"  k={k}: skipping (too slow)")
            continue
        print(f"  k={k}...", end=" ", flush=True)
        counts = []
        for M in all_matrices[k]:
            br = best_response_from_full(k, M, n_orderings=3)
            counts.append(len(br))
        br_baselines[k] = counts
        print(f"mean={statistics.mean(counts):.1f}, range=[{min(counts)}-{max(counts)}]")

    print()

    # Main results table
    results = {}  # (variant, c, k) -> dict of metrics

    for variant_name, heuristic_fn in VARIANTS.items():
        for c in C_VALUES:
            for k in K_VALUES:
                matrices = all_matrices[k]
                orig_reaches = all_orig_reach[k]
                budget_per_node = int(math.floor(c * math.log(k))) + 2

                edge_counts = []
                reach_fracs = []
                full_reach_count = 0
                fail_types_agg = defaultdict(int)
                fail_pair_counts = []

                # After repair
                repair_edge_counts = []
                repair_full_count = 0

                for idx, M in enumerate(matrices):
                    orig_reach = orig_reaches[idx]

                    # Apply heuristic
                    kept = heuristic_fn(k, M, c)
                    edge_counts.append(len(kept))

                    # Reachability
                    frac = reachability_fraction(k, kept, orig_reach)
                    reach_fracs.append(frac)

                    if frac >= 1.0 - 1e-9:
                        full_reach_count += 1
                    else:
                        fails = failing_pairs_by_type(k, kept, orig_reach)
                        for ft, cnt in fails.items():
                            fail_types_agg[ft] += cnt
                        fail_pair_counts.append(sum(fails.values()))

                    # One round of repair
                    repaired = one_round_repair(k, kept, M, orig_reach)
                    repair_edge_counts.append(len(repaired))
                    r_frac = reachability_fraction(k, repaired, orig_reach)
                    if r_frac >= 1.0 - 1e-9:
                        repair_full_count += 1

                n_mat = len(matrices)
                results[(variant_name, c, k)] = {
                    'budget_per_node': budget_per_node,
                    'total_budget': budget_per_node * k,  # only A-vertices have budget
                    'mean_edges': statistics.mean(edge_counts),
                    'mean_reach': statistics.mean(reach_fracs),
                    'full_reach_pct': full_reach_count / n_mat * 100,
                    'mean_fail_pairs': statistics.mean(fail_pair_counts) if fail_pair_counts else 0,
                    'fail_types': dict(fail_types_agg),
                    'repair_mean_edges': statistics.mean(repair_edge_counts),
                    'repair_full_pct': repair_full_count / n_mat * 100,
                }

    # ---------------------------------------------------------------------------
    # Print results
    # ---------------------------------------------------------------------------

    print("=" * 80)
    print("RESULTS: Heuristic construction (no repair)")
    print("=" * 80)

    for variant_name in VARIANTS:
        print(f"\n--- Variant {variant_name} ---")
        print(f"{'c':>4} | {'k':>2} | {'budget':>6} | {'edges':>6} | {'reach%':>7} | {'full%':>6} | {'fail_pairs':>10}")
        print("-" * 65)
        for c in C_VALUES:
            for k in K_VALUES:
                r = results[(variant_name, c, k)]
                print(f"{c:>4.1f} | {k:>2} | {r['total_budget']:>6} | "
                      f"{r['mean_edges']:>6.1f} | {r['mean_reach']:>6.1f}% | "
                      f"{r['full_reach_pct']:>5.1f}% | {r['mean_fail_pairs']:>10.1f}")

    print()
    print("=" * 80)
    print("RESULTS: After 1-round repair")
    print("=" * 80)

    for variant_name in VARIANTS:
        print(f"\n--- Variant {variant_name} ---")
        print(f"{'c':>4} | {'k':>2} | {'heur_edges':>10} | {'repair_edges':>12} | {'repair_full%':>12}")
        print("-" * 60)
        for c in C_VALUES:
            for k in K_VALUES:
                r = results[(variant_name, c, k)]
                added = r['repair_mean_edges'] - r['mean_edges']
                print(f"{c:>4.1f} | {k:>2} | {r['mean_edges']:>10.1f} | "
                      f"{r['repair_mean_edges']:>12.1f} (+{added:.1f}) | "
                      f"{r['repair_full_pct']:>11.1f}%")

    # ---------------------------------------------------------------------------
    # Comparison with H10 best-response
    # ---------------------------------------------------------------------------

    print()
    print("=" * 80)
    print("COMPARISON: Heuristic+repair vs H10 best-response")
    print("=" * 80)
    print(f"{'var':>3} | {'c':>4} | {'k':>2} | {'h+r edges':>10} | {'BR edges':>9} | {'ratio':>6} | {'4k-3':>5}")
    print("-" * 60)
    for variant_name in VARIANTS:
        for c in C_VALUES:
            for k in K_VALUES:
                if k not in br_baselines:
                    continue
                r = results[(variant_name, c, k)]
                br_mean = statistics.mean(br_baselines[k])
                ratio = r['repair_mean_edges'] / br_mean if br_mean > 0 else float('inf')
                budget = 4 * k - 3
                print(f"{variant_name:>3} | {c:>4.1f} | {k:>2} | "
                      f"{r['repair_mean_edges']:>10.1f} | {br_mean:>9.1f} | "
                      f"{ratio:>5.2f}x | {budget:>5}")

    # ---------------------------------------------------------------------------
    # KEY METRIC: minimum c for ≥95% full reachability after repair
    # ---------------------------------------------------------------------------

    print()
    print("=" * 80)
    print("KEY METRIC: Minimum c for ≥95% full reachability (heuristic + 1-round repair)")
    print("=" * 80)
    for variant_name in VARIANTS:
        print(f"\nVariant {variant_name}:")
        for k in K_VALUES:
            found = None
            for c in C_VALUES:
                r = results[(variant_name, c, k)]
                if r['repair_full_pct'] >= 95.0:
                    found = c
                    break
            if found is not None:
                r = results[(variant_name, found, k)]
                print(f"  k={k}: c={found:.1f} (repair_full={r['repair_full_pct']:.0f}%, "
                      f"edges={r['repair_mean_edges']:.1f})")
            else:
                best_c = max(C_VALUES)
                r = results[(variant_name, best_c, k)]
                print(f"  k={k}: NOT REACHED (best: c={best_c:.1f}, "
                      f"repair_full={r['repair_full_pct']:.0f}%, edges={r['repair_mean_edges']:.1f})")

    # ---------------------------------------------------------------------------
    # Failure type analysis
    # ---------------------------------------------------------------------------

    print()
    print("=" * 80)
    print("FAILURE TYPE ANALYSIS (heuristic only, no repair)")
    print("=" * 80)
    for variant_name in VARIANTS:
        print(f"\nVariant {variant_name}, c=1.0:")
        for k in K_VALUES:
            r = results[(variant_name, 1.0, k)]
            ft = r['fail_types']
            total_fails = sum(ft.values())
            if total_fails > 0:
                pcts = {t: cnt/total_fails*100 for t, cnt in ft.items()}
                print(f"  k={k}: full_reach={r['full_reach_pct']:.0f}%, "
                      f"fail distribution: AA={pcts.get('AA',0):.0f}% AB={pcts.get('AB',0):.0f}% "
                      f"BA={pcts.get('BA',0):.0f}% BB={pcts.get('BB',0):.0f}%")
            else:
                print(f"  k={k}: full_reach={r['full_reach_pct']:.0f}%, no failures")

    # ---------------------------------------------------------------------------
    # Summary verdict
    # ---------------------------------------------------------------------------

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    # Find best variant overall
    best_variant = None
    best_score = -1
    for variant_name in VARIANTS:
        # Score = average repair_full_pct across all k and c values
        scores = []
        for c in C_VALUES:
            for k in K_VALUES:
                scores.append(results[(variant_name, c, k)]['repair_full_pct'])
        avg = statistics.mean(scores)
        print(f"Variant {variant_name}: avg repair_full = {avg:.1f}%")
        if avg > best_score:
            best_score = avg
            best_variant = variant_name

    print(f"\nBest variant: {best_variant} (avg {best_score:.1f}%)")

    # Best variant at c=1.0 summary
    print(f"\nBest variant ({best_variant}) at c=1.0:")
    for k in K_VALUES:
        r = results[(best_variant, 1.0, k)]
        budget = 4 * k - 3
        print(f"  k={k}: {r['mean_edges']:.1f} edges -> {r['repair_mean_edges']:.1f} after repair "
              f"(budget={budget}), reach={r['mean_reach']:.1f}% -> repair_full={r['repair_full_pct']:.0f}%")


if __name__ == '__main__':
    run_experiment()
