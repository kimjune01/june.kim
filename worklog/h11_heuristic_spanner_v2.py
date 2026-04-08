"""
H11 v2: O(n) heuristic budget construction for temporal spanners.

Fixes from v1:
- reach% now correctly multiplied by 100
- Full repair checks global reachability gain (not just 2-node local)
- Tests higher c values: {0.5, 1.0, 1.5, 2.0, 3.0, 4.0}
- Edge budget displayed vs 4k-3
"""

import random
import math
import statistics
from collections import defaultdict
import heapq

random.seed(42)

# ---------------------------------------------------------------------------
# Temporal reachability engine
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
    adj = build_adj(k, edges)
    n = 2 * k
    count = 0
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        count += len(r) - 1
    return count

def reachability_fraction(k, edges, orig_reach):
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
    adj = build_adj(k, edges)
    n = 2 * k
    for s in range(n):
        r = temporal_reachable_from(s, adj)
        if len(r) < n:
            return False
    return True

def failing_pairs_by_type(k, edges, orig_reach):
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
# Matrix generation
# ---------------------------------------------------------------------------

def random_matrix(k):
    vals = list(range(1, k*k+1))
    random.shuffle(vals)
    return [vals[i*k:(i+1)*k] for i in range(k)]

def matrix_to_edges(k, M):
    return {(i, k+j, M[i][j]) for i in range(k) for j in range(k)}

def generate_reachable_matrices(k, count):
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
    info = []
    for i in range(k):
        row = M[i]
        min_j = min(range(k), key=lambda j: row[j])
        max_j = max(range(k), key=lambda j: row[j])
        info.append((min_j, max_j))
    return info

def compute_column_popularity(k, row_info):
    popularity = [0] * k
    for (min_j, max_j) in row_info:
        popularity[min_j] += 1
        popularity[max_j] += 1
    return popularity

def heuristic_A(k, M, c):
    """Column popularity."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)
    col_pop = compute_column_popularity(k, row_info)
    kept = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        kept.add((i, k + min_j, M[i][min_j]))
        kept.add((i, k + max_j, M[i][max_j]))
        remaining = [(j, col_pop[j]) for j in range(k) if j != min_j and j != max_j]
        remaining.sort(key=lambda x: -x[1])
        for j, _ in remaining[:budget_per_node - 2]:
            kept.add((i, k + j, M[i][j]))
    return kept

def heuristic_B(k, M, c):
    """Timestamp spread (greedy dispersion)."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)
    kept = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        kept.add((i, k + min_j, M[i][min_j]))
        kept.add((i, k + max_j, M[i][max_j]))
        kept_times = {M[i][min_j], M[i][max_j]}
        remaining = [j for j in range(k) if j != min_j and j != max_j]
        extras = budget_per_node - 2
        for _ in range(min(extras, len(remaining))):
            best_j, best_dist = None, -1
            for j in remaining:
                t = M[i][j]
                d = min(abs(t - kt) for kt in kept_times)
                if d > best_dist:
                    best_dist = d
                    best_j = j
            if best_j is not None:
                kept.add((i, k + best_j, M[i][best_j]))
                kept_times.add(M[i][best_j])
                remaining.remove(best_j)
    return kept

def heuristic_C(k, M, c):
    """Column coverage."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)
    col_kept_count = [0] * k
    for i in range(k):
        min_j, max_j = row_info[i]
        col_kept_count[min_j] += 1
        col_kept_count[max_j] += 1
    kept = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        kept.add((i, k + min_j, M[i][min_j]))
        kept.add((i, k + max_j, M[i][max_j]))
        remaining = [(j, col_kept_count[j]) for j in range(k) if j != min_j and j != max_j]
        remaining.sort(key=lambda x: x[1])
        for j, _ in remaining[:budget_per_node - 2]:
            kept.add((i, k + j, M[i][j]))
            col_kept_count[j] += 1
    return kept

def heuristic_D(k, M, c):
    """Combined: popularity * timestamp distance."""
    budget_per_node = int(math.floor(c * math.log(k))) + 2
    row_info = compute_row_info(k, M)
    col_pop = compute_column_popularity(k, row_info)
    kept = set()
    for i in range(k):
        min_j, max_j = row_info[i]
        kept.add((i, k + min_j, M[i][min_j]))
        kept.add((i, k + max_j, M[i][max_j]))
        kept_times = {M[i][min_j], M[i][max_j]}
        remaining = [j for j in range(k) if j != min_j and j != max_j]
        scored = []
        for j in remaining:
            t = M[i][j]
            d = min(abs(t - kt) for kt in kept_times)
            scored.append((j, col_pop[j] * d))
        scored.sort(key=lambda x: -x[1])
        for j, _ in scored[:budget_per_node - 2]:
            kept.add((i, k + j, M[i][j]))
    return kept

# ---------------------------------------------------------------------------
# Repair: 1-round global reachability check
# ---------------------------------------------------------------------------

def one_round_repair(k, kept_edges, M, orig_reach):
    """Add non-kept edges that increase total reachability. One pass, timestamp-sorted."""
    all_edges = matrix_to_edges(k, M)
    missing = sorted(all_edges - kept_edges, key=lambda e: e[2])
    repaired = set(kept_edges)
    current_count = count_reachable_pairs(k, repaired)
    target = sum(1 for v in orig_reach.values() if v)

    for e in missing:
        if current_count >= target:
            break
        trial = repaired | {e}
        new_count = count_reachable_pairs(k, trial)
        if new_count > current_count:
            repaired = trial
            current_count = new_count

    return repaired

# ---------------------------------------------------------------------------
# Best-response from full (H10)
# ---------------------------------------------------------------------------

def best_response_from_full(k, M, n_orderings=3):
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
                        cur_reach = all_pairs_reach(k, trial)
                        ok = all(cur_reach.get(p, False) for p, was in orig.items() if was)
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

VARIANTS = {'A': heuristic_A, 'B': heuristic_B, 'C': heuristic_C, 'D': heuristic_D}
C_VALUES = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
K_VALUES = [3, 4, 5, 6, 7, 8]
N_MATRICES = 50

def run_experiment():
    print("=" * 80)
    print("H11 v2: O(n) Heuristic Budget Construction for Temporal Spanners")
    print("=" * 80)

    # Generate reachable matrices
    all_matrices = {}
    all_orig_reach = {}
    for k in K_VALUES:
        print(f"Generating {N_MATRICES} reachable matrices for k={k}...", end=" ", flush=True)
        matrices, attempts = generate_reachable_matrices(k, N_MATRICES)
        print(f"done ({attempts} attempts, {attempts/N_MATRICES:.1f}x)")
        all_matrices[k] = matrices
        reach_list = []
        for M in matrices:
            edges = matrix_to_edges(k, M)
            reach_list.append(all_pairs_reach(k, edges))
        all_orig_reach[k] = reach_list

    # Best-response baselines
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

    # Run all variants
    results = {}
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
                repair_edge_counts = []
                repair_full_count = 0

                for idx, M in enumerate(matrices):
                    orig_reach = orig_reaches[idx]

                    kept = heuristic_fn(k, M, c)
                    edge_counts.append(len(kept))

                    frac = reachability_fraction(k, kept, orig_reach)
                    reach_fracs.append(frac)

                    if frac >= 1.0 - 1e-9:
                        full_reach_count += 1
                    else:
                        fails = failing_pairs_by_type(k, kept, orig_reach)
                        for ft, cnt in fails.items():
                            fail_types_agg[ft] += cnt
                        fail_pair_counts.append(sum(fails.values()))

                    # Repair
                    repaired = one_round_repair(k, kept, M, orig_reach)
                    repair_edge_counts.append(len(repaired))
                    r_frac = reachability_fraction(k, repaired, orig_reach)
                    if r_frac >= 1.0 - 1e-9:
                        repair_full_count += 1

                n_mat = len(matrices)
                results[(variant_name, c, k)] = {
                    'budget_per_node': budget_per_node,
                    'total_budget': budget_per_node * k,
                    'mean_edges': statistics.mean(edge_counts),
                    'mean_reach_pct': statistics.mean(reach_fracs) * 100,
                    'full_reach_pct': full_reach_count / n_mat * 100,
                    'mean_fail_pairs': statistics.mean(fail_pair_counts) if fail_pair_counts else 0,
                    'fail_types': dict(fail_types_agg),
                    'repair_mean_edges': statistics.mean(repair_edge_counts),
                    'repair_full_pct': repair_full_count / n_mat * 100,
                }

                status = "OK" if repair_full_count / n_mat >= 0.95 else ""
                print(f"  {variant_name} c={c:.1f} k={k}: "
                      f"edges={statistics.mean(edge_counts):.0f}, "
                      f"reach={statistics.mean(reach_fracs)*100:.1f}%, "
                      f"full={full_reach_count}/{n_mat}, "
                      f"repair_edges={statistics.mean(repair_edge_counts):.1f}, "
                      f"repair_full={repair_full_count}/{n_mat} {status}",
                      flush=True)

    # ---------------------------------------------------------------------------
    # Summary tables
    # ---------------------------------------------------------------------------

    print()
    print("=" * 80)
    print("TABLE 1: Heuristic-only reachability (% of pairs preserved)")
    print("=" * 80)
    for variant_name in VARIANTS:
        print(f"\n--- Variant {variant_name} ---")
        header = f"{'c':>4} |"
        for k in K_VALUES:
            header += f" k={k:>2} |"
        print(header)
        print("-" * len(header))
        for c in C_VALUES:
            line = f"{c:>4.1f} |"
            for k in K_VALUES:
                r = results[(variant_name, c, k)]
                line += f" {r['mean_reach_pct']:>4.1f} |"
            print(line)

    print()
    print("=" * 80)
    print("TABLE 2: % matrices achieving 100% reachability (heuristic only)")
    print("=" * 80)
    for variant_name in VARIANTS:
        print(f"\n--- Variant {variant_name} ---")
        header = f"{'c':>4} |"
        for k in K_VALUES:
            header += f" k={k:>2}  |"
        print(header)
        print("-" * len(header))
        for c in C_VALUES:
            line = f"{c:>4.1f} |"
            for k in K_VALUES:
                r = results[(variant_name, c, k)]
                line += f" {r['full_reach_pct']:>4.0f}% |"
            print(line)

    print()
    print("=" * 80)
    print("TABLE 3: After 1-round repair — % matrices with 100% reachability")
    print("=" * 80)
    for variant_name in VARIANTS:
        print(f"\n--- Variant {variant_name} ---")
        header = f"{'c':>4} |"
        for k in K_VALUES:
            header += f" k={k:>2}  |"
        print(header)
        print("-" * len(header))
        for c in C_VALUES:
            line = f"{c:>4.1f} |"
            for k in K_VALUES:
                r = results[(variant_name, c, k)]
                marker = "*" if r['repair_full_pct'] >= 95 else " "
                line += f" {r['repair_full_pct']:>4.0f}%{marker}|"
            print(line)
    print("  * = >=95% threshold met")

    print()
    print("=" * 80)
    print("TABLE 4: Mean edges after repair (vs 4k-3 budget)")
    print("=" * 80)
    for variant_name in VARIANTS:
        print(f"\n--- Variant {variant_name} ---")
        header = f"{'c':>4} |"
        for k in K_VALUES:
            budget = 4*k - 3
            header += f" k={k}({budget:>2}) |"
        print(header)
        print("-" * len(header))
        for c in C_VALUES:
            line = f"{c:>4.1f} |"
            for k in K_VALUES:
                r = results[(variant_name, c, k)]
                budget = 4*k - 3
                ratio = r['repair_mean_edges'] / budget
                line += f" {r['repair_mean_edges']:>5.1f}/{ratio:.1f}|"
            print(line)

    # Comparison with H10
    print()
    print("=" * 80)
    print("TABLE 5: Repair edges / H10 best-response edges")
    print("=" * 80)
    # Only show best variant (B) and best c per k
    for variant_name in VARIANTS:
        print(f"\n--- Variant {variant_name} ---")
        for c in C_VALUES:
            line = f"  c={c:.1f}: "
            for k in K_VALUES:
                if k in br_baselines:
                    r = results[(variant_name, c, k)]
                    br_mean = statistics.mean(br_baselines[k])
                    ratio = r['repair_mean_edges'] / br_mean
                    line += f"k={k}:{ratio:.2f}x  "
            print(line)

    # KEY METRIC
    print()
    print("=" * 80)
    print("KEY METRIC: Minimum c for >=95% full reachability after repair")
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
                budget = 4*k - 3
                print(f"  k={k}: c={found:.1f}  edges={r['repair_mean_edges']:.1f} (budget={budget}, "
                      f"ratio={r['repair_mean_edges']/budget:.2f}x)")
            else:
                best_c = max(C_VALUES)
                r = results[(variant_name, best_c, k)]
                print(f"  k={k}: NOT REACHED  best c={best_c:.1f} -> {r['repair_full_pct']:.0f}%")

    # Failure type analysis (brief)
    print()
    print("=" * 80)
    print("FAILURE TYPES (heuristic only, c=1.0)")
    print("=" * 80)
    for variant_name in VARIANTS:
        print(f"\n  Variant {variant_name}:", end="")
        for k in K_VALUES:
            r = results[(variant_name, 1.0, k)]
            ft = r['fail_types']
            total = sum(ft.values())
            if total > 0:
                bb_pct = ft.get('BB', 0) / total * 100
                print(f"  k={k}:BB={bb_pct:.0f}%", end="")
            else:
                print(f"  k={k}:none", end="")
        print()

    # Edge budget analysis: what does floor(c*log(k))+2 actually give?
    print()
    print("=" * 80)
    print("BUDGET TABLE: floor(c*log(k))+2 per A-vertex")
    print("=" * 80)
    header = f"{'c':>4} |"
    for k in K_VALUES:
        header += f" k={k:>2} |"
    print(header)
    print("-" * len(header))
    for c in C_VALUES:
        line = f"{c:>4.1f} |"
        for k in K_VALUES:
            b = int(math.floor(c * math.log(k))) + 2
            total = b * k
            line += f" {b}({total:>2}) |"
        print(line)
    print("  Format: per-node(total-edges)")

if __name__ == '__main__':
    run_experiment()
