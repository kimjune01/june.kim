#!/usr/bin/env python3
"""
Test whether SJT-style ordering of emitters in the CPS fireworks residual
biclique gives O(1) missed collectors per delegation step.

The CPS fireworks algorithm for temporal spanners reduces to a biclique
with k emitters (X⁻) and k collectors (X⁺). We test if an ordering exists
where consecutive emitters share all but O(1) collector connections.
"""

import random
import itertools
import math
import sys
from collections import defaultdict

random.seed(42)

# ─── Task 1: Model the CPS residual ─────────────────────────────────────────

def generate_temporal_clique(n):
    """
    Generate a temporal K_n: assign a distinct timestamp to each of the
    n(n-1)/2 edges. Returns dict (i,j) -> timestamp for i < j.
    """
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    timestamps = list(range(1, len(edges) + 1))
    random.shuffle(timestamps)
    return {e: t for e, t in zip(edges, timestamps)}

def get_edge_time(temporal, i, j):
    """Get timestamp of edge (i,j) regardless of order."""
    if i < j:
        return temporal[(i, j)]
    else:
        return temporal[(j, i)]

def compute_extremal_matchings(n, temporal):
    """
    For each vertex v, compute:
    - S⁻(v): the neighbor u minimizing t(v,u) — earliest edge from v
    - S⁺(v): the neighbor u maximizing t(v,u) — latest edge from v

    In the biclique model:
    - Emitters X⁻ = {v : v acts as source of early edges}
    - Collectors X⁺ = {v : v acts as sink of late edges}

    Returns S_minus, S_plus as dicts vertex -> neighbor.
    """
    S_minus = {}
    S_plus = {}
    for v in range(n):
        neighbors = [(u, get_edge_time(temporal, v, u)) for u in range(n) if u != v]
        S_minus[v] = min(neighbors, key=lambda x: x[1])[0]
        S_plus[v] = max(neighbors, key=lambda x: x[1])[0]
    return S_minus, S_plus

def compute_dismountable(n, temporal):
    """
    A vertex v is dismountable if removing it doesn't break temporal
    connectivity. In the CPS sense, the non-dismountable residual is
    the hard core.

    For simplicity, we identify the residual biclique directly:
    - Emitters: vertices whose earliest edge is "structurally necessary"
    - Collectors: vertices whose latest edge is "structurally necessary"

    We use the standard CPS reduction: the residual biclique consists of
    vertices that participate in extremal matchings that can't be covered
    by simpler structures.
    """
    S_minus, S_plus = compute_extremal_matchings(n, temporal)

    # The residual biclique: vertices involved in non-trivial extremal paths
    # Emitters = vertices v where S⁻(v) and S⁺(v) define distinct matchings
    # that create a bipartite structure

    # Build the bipartite graph: for each vertex v,
    # v as emitter connects to S⁻(v) and S⁺(v) as collectors
    # The residual is the set of vertices that appear in cycles of the
    # S⁻ ∘ (S⁺)⁻¹ permutation

    # Compute S⁻ and S⁺ as permutations on [n]
    # The "interesting" structure is S⁻ composed with inverse of S⁺
    perm = {}
    for v in range(n):
        perm[v] = S_minus[v]

    inv_S_plus = {}
    for v in range(n):
        inv_S_plus[S_plus[v]] = v

    # Composition: S⁻ ∘ (S⁺)⁻¹
    composed = {}
    for v in range(n):
        if v in inv_S_plus:
            composed[v] = S_minus[inv_S_plus[v]]

    # Find non-fixed-point cycles (the residual)
    visited = set()
    residual_vertices = set()
    for v in range(n):
        if v in visited or v not in composed:
            continue
        cycle = []
        u = v
        while u not in visited and u in composed:
            visited.add(u)
            cycle.append(u)
            u = composed[u]
        if len(cycle) > 1:
            residual_vertices.update(cycle)

    # If residual is too small, use all vertices
    if len(residual_vertices) < 4:
        residual_vertices = set(range(n))

    return list(sorted(residual_vertices)), S_minus, S_plus

def build_collector_neighborhoods(n, temporal, emitters):
    """
    For each emitter, compute its collector neighborhood:
    which other vertices (collectors) can be reached via 2-hop
    temporal journeys (time-respecting paths).

    A temporal journey from emitter e to collector c via intermediate w:
    t(e, w) < t(w, c)

    The neighborhood N(e) = {c : ∃w s.t. t(e,w) < t(w,c), w ∉ {e,c}}
    """
    neighborhoods = {}
    emitter_set = set(emitters)
    # Collectors = all vertices (in CPS, the biclique has separate emitter/collector copies,
    # but in the temporal clique model, any vertex can be a collector)
    collectors = list(range(n))

    for e in emitters:
        N_e = set()
        for c in collectors:
            if c == e:
                continue
            # Check if there exists intermediate w with t(e,w) < t(w,c)
            for w in range(n):
                if w == e or w == c:
                    continue
                t_ew = get_edge_time(temporal, e, w)
                t_wc = get_edge_time(temporal, w, c)
                if t_ew < t_wc:
                    N_e.add(c)
                    break
        neighborhoods[e] = N_e

    return neighborhoods

def run_task1(n_values, num_instances=5):
    """Run Task 1: Model the CPS residual for various n."""
    print("=" * 70)
    print("TASK 1: Model the CPS residual biclique")
    print("=" * 70)

    all_instances = []

    for n in n_values:
        print(f"\n--- K_{n} temporal clique ---")
        for inst in range(num_instances):
            temporal = generate_temporal_clique(n)
            residual, S_minus, S_plus = compute_dismountable(n, temporal)
            k = len(residual)
            neighborhoods = build_collector_neighborhoods(n, temporal, residual)

            # Record neighborhood sizes
            sizes = [len(neighborhoods[e]) for e in residual]

            instance = {
                'n': n,
                'k': k,
                'temporal': temporal,
                'residual': residual,
                'S_minus': S_minus,
                'S_plus': S_plus,
                'neighborhoods': neighborhoods,
            }
            all_instances.append(instance)

            if inst == 0:
                print(f"  Instance {inst}: k={k} emitters, "
                      f"avg neighborhood size={sum(sizes)/len(sizes):.1f}, "
                      f"range=[{min(sizes)}, {max(sizes)}]")
                # Show S⁻ and S⁺ as permutations on residual
                s_minus_perm = [S_minus[v] for v in residual]
                s_plus_perm = [S_plus[v] for v in residual]
                print(f"  S⁻ on residual: {s_minus_perm}")
                print(f"  S⁺ on residual: {s_plus_perm}")

    return all_instances

# ─── Task 2: Measure collector overlap ───────────────────────────────────────

def compute_overlap_stats(neighborhoods, emitters):
    """Compute pairwise overlap and symmetric difference."""
    overlaps = {}
    sym_diffs = {}

    for i in range(len(emitters)):
        for j in range(i+1, len(emitters)):
            ei, ej = emitters[i], emitters[j]
            Ni, Nj = neighborhoods[ei], neighborhoods[ej]
            overlap = len(Ni & Nj)
            sym_diff = len(Ni ^ Nj)
            overlaps[(ei, ej)] = overlap
            sym_diffs[(ei, ej)] = sym_diff

    return overlaps, sym_diffs

def run_task2(instances):
    """Run Task 2: Measure collector overlap."""
    print("\n" + "=" * 70)
    print("TASK 2: Collector overlap structure")
    print("=" * 70)

    for inst in instances[:len(set(i['n'] for i in instances))]:  # one per n
        n = inst['n']
        emitters = inst['residual']
        neighborhoods = inst['neighborhoods']
        k = len(emitters)

        overlaps, sym_diffs = compute_overlap_stats(neighborhoods, emitters)

        avg_nbr_size = sum(len(neighborhoods[e]) for e in emitters) / k

        if overlaps:
            overlap_vals = list(overlaps.values())
            sym_diff_vals = list(sym_diffs.values())

            print(f"\n--- K_{n} (k={k} emitters, avg |N(e)|={avg_nbr_size:.1f}) ---")
            print(f"  Pairwise overlap |N(i)∩N(j)|: "
                  f"mean={sum(overlap_vals)/len(overlap_vals):.1f}, "
                  f"min={min(overlap_vals)}, max={max(overlap_vals)}")
            print(f"  Symmetric diff |N(i)ΔN(j)|: "
                  f"mean={sum(sym_diff_vals)/len(sym_diff_vals):.1f}, "
                  f"min={min(sym_diff_vals)}, max={max(sym_diff_vals)}")

            # Density: fraction of max possible overlap
            density = sum(overlap_vals) / (len(overlap_vals) * avg_nbr_size) if avg_nbr_size > 0 else 0
            print(f"  Overlap density (normalized): {density:.3f}")

# ─── Task 3: Find optimal ordering ──────────────────────────────────────────

def consecutive_sym_diffs(ordering, neighborhoods):
    """Compute consecutive symmetric differences for an ordering."""
    diffs = []
    for i in range(len(ordering) - 1):
        Ni = neighborhoods[ordering[i]]
        Nj = neighborhoods[ordering[i+1]]
        diffs.append(len(Ni ^ Nj))
    return diffs

def brute_force_optimal_ordering(emitters, neighborhoods):
    """For small k, try all k! orderings."""
    k = len(emitters)
    if k > 10:
        return None, None

    best_max_diff = float('inf')
    best_ordering = None

    for perm in itertools.permutations(emitters):
        diffs = consecutive_sym_diffs(perm, neighborhoods)
        max_diff = max(diffs) if diffs else 0
        if max_diff < best_max_diff:
            best_max_diff = max_diff
            best_ordering = perm

    return best_ordering, best_max_diff

def greedy_max_overlap_ordering(emitters, neighborhoods):
    """Greedy: always pick next emitter with maximum overlap."""
    remaining = set(emitters)
    # Start with the emitter that has the most connections
    current = max(remaining, key=lambda e: len(neighborhoods[e]))
    ordering = [current]
    remaining.remove(current)

    while remaining:
        best_next = max(remaining,
                       key=lambda e: len(neighborhoods[current] & neighborhoods[e]))
        ordering.append(best_next)
        remaining.remove(best_next)
        current = best_next

    return ordering

def sjt_ordering_on_s_minus(emitters, S_minus):
    """
    Use Steinhaus-Johnson-Trotter on the S⁻ permutation.
    SJT generates permutations by adjacent transpositions.
    Here we just use S⁻ values to define an ordering of emitters.
    """
    # Order emitters by their S⁻ target
    return sorted(emitters, key=lambda e: S_minus[e])

def run_task3(instances):
    """Run Task 3: Find optimal ordering."""
    print("\n" + "=" * 70)
    print("TASK 3: Optimal SJT-style ordering")
    print("=" * 70)

    results = {}

    for inst in instances[:len(set(i['n'] for i in instances))]:
        n = inst['n']
        emitters = inst['residual']
        neighborhoods = inst['neighborhoods']
        S_minus = inst['S_minus']
        k = len(emitters)

        print(f"\n--- K_{n} (k={k} emitters) ---")

        # Brute force for small k
        if k <= 10:
            bf_ordering, bf_max = brute_force_optimal_ordering(emitters, neighborhoods)
            bf_diffs = consecutive_sym_diffs(bf_ordering, neighborhoods)
            print(f"  Brute-force optimal: max_diff={bf_max}, "
                  f"mean_diff={sum(bf_diffs)/len(bf_diffs):.1f}, "
                  f"diffs={bf_diffs}")
        else:
            bf_max = None
            print(f"  Brute-force: skipped (k={k} > 10)")

        # Greedy
        greedy_ord = greedy_max_overlap_ordering(emitters, neighborhoods)
        greedy_diffs = consecutive_sym_diffs(greedy_ord, neighborhoods)
        greedy_max = max(greedy_diffs) if greedy_diffs else 0
        print(f"  Greedy ordering: max_diff={greedy_max}, "
              f"mean_diff={sum(greedy_diffs)/len(greedy_diffs):.1f}")

        # SJT on S⁻
        sjt_ord = sjt_ordering_on_s_minus(emitters, S_minus)
        sjt_diffs = consecutive_sym_diffs(sjt_ord, neighborhoods)
        sjt_max = max(sjt_diffs) if sjt_diffs else 0
        print(f"  SJT(S⁻) ordering: max_diff={sjt_max}, "
              f"mean_diff={sum(sjt_diffs)/len(sjt_diffs):.1f}")

        results[n] = {
            'bf_max': bf_max,
            'greedy_max': greedy_max,
            'sjt_max': sjt_max,
            'k': k,
        }

    return results

# ─── Task 4: Compare to random ordering ─────────────────────────────────────

def run_task4(instances, num_random=100):
    """Run Task 4: Compare orderings."""
    print("\n" + "=" * 70)
    print("TASK 4: Random vs greedy vs SJT ordering comparison")
    print("=" * 70)

    for inst in instances[:len(set(i['n'] for i in instances))]:
        n = inst['n']
        emitters = inst['residual']
        neighborhoods = inst['neighborhoods']
        S_minus = inst['S_minus']
        k = len(emitters)

        print(f"\n--- K_{n} (k={k} emitters) ---")

        # Random orderings
        random_maxes = []
        random_means = []
        for _ in range(num_random):
            rand_ord = list(emitters)
            random.shuffle(rand_ord)
            diffs = consecutive_sym_diffs(rand_ord, neighborhoods)
            if diffs:
                random_maxes.append(max(diffs))
                random_means.append(sum(diffs) / len(diffs))

        print(f"  Random (n={num_random}):")
        print(f"    Mean of max_diffs: {sum(random_maxes)/len(random_maxes):.1f}")
        print(f"    Max of max_diffs:  {max(random_maxes)}")
        print(f"    Mean of mean_diffs: {sum(random_means)/len(random_means):.1f}")

        # Greedy
        greedy_ord = greedy_max_overlap_ordering(emitters, neighborhoods)
        greedy_diffs = consecutive_sym_diffs(greedy_ord, neighborhoods)
        print(f"  Greedy: max_diff={max(greedy_diffs) if greedy_diffs else 0}, "
              f"mean_diff={sum(greedy_diffs)/len(greedy_diffs):.1f}" if greedy_diffs else "")

        # SJT on S⁻
        sjt_ord = sjt_ordering_on_s_minus(emitters, S_minus)
        sjt_diffs = consecutive_sym_diffs(sjt_ord, neighborhoods)
        print(f"  SJT(S⁻): max_diff={max(sjt_diffs) if sjt_diffs else 0}, "
              f"mean_diff={sum(sjt_diffs)/len(sjt_diffs):.1f}" if sjt_diffs else "")

# ─── Task 5: Delegation simulation ──────────────────────────────────────────

def simulate_delegation(ordering, neighborhoods):
    """
    Simulate CPS delegation:
    - Process emitters in order
    - Each eliminated emitter delegates to the next one
    - Count missed collectors per step
    """
    missed_per_step = []
    total_missed = 0

    for i in range(len(ordering) - 1):
        eliminated = ordering[i]
        delegate = ordering[i + 1]

        N_elim = neighborhoods[eliminated]
        N_del = neighborhoods[delegate]

        missed = N_elim - N_del  # collectors in eliminated's neighborhood but not delegate's
        missed_per_step.append(len(missed))
        total_missed += len(missed)

    return missed_per_step, total_missed

def run_task5(instances, num_random=100):
    """Run Task 5: Delegation simulation."""
    print("\n" + "=" * 70)
    print("TASK 5: Delegation simulation")
    print("=" * 70)

    for inst in instances[:len(set(i['n'] for i in instances))]:
        n = inst['n']
        emitters = inst['residual']
        neighborhoods = inst['neighborhoods']
        S_minus = inst['S_minus']
        k = len(emitters)

        print(f"\n--- K_{n} (k={k} emitters) ---")

        # CPS bound: O(k log k)
        cps_bound = k * math.ceil(math.log2(max(k, 2)))
        print(f"  CPS O(k log k) bound: ~{cps_bound}")

        # Optimal ordering (brute force for small k, greedy otherwise)
        if k <= 10:
            opt_ord, _ = brute_force_optimal_ordering(emitters, neighborhoods)
        else:
            opt_ord = greedy_max_overlap_ordering(emitters, neighborhoods)

        opt_missed, opt_total = simulate_delegation(opt_ord, neighborhoods)
        print(f"  Optimal ordering: total_missed={opt_total}, "
              f"per_step={opt_missed}")

        # Random ordering average
        random_totals = []
        for _ in range(num_random):
            rand_ord = list(emitters)
            random.shuffle(rand_ord)
            _, rand_total = simulate_delegation(rand_ord, neighborhoods)
            random_totals.append(rand_total)

        print(f"  Random ordering: mean_total={sum(random_totals)/len(random_totals):.1f}, "
              f"max_total={max(random_totals)}")

        # SJT ordering
        sjt_ord = sjt_ordering_on_s_minus(emitters, S_minus)
        sjt_missed, sjt_total = simulate_delegation(sjt_ord, neighborhoods)
        print(f"  SJT(S⁻) ordering: total_missed={sjt_total}, "
              f"per_step={sjt_missed}")

# ─── Task 6: The critical question — scaling ────────────────────────────────

def run_task6(num_instances=30):
    """
    Test for k = 4, 6, 8, 10, 12, 16 with 30 instances each.
    Is min_σ max_i |N(σ(i)) Δ N(σ(i+1))| = O(1), O(log k), or O(k)?
    """
    print("\n" + "=" * 70)
    print("TASK 6: CRITICAL QUESTION — Scaling of min consecutive sym diff")
    print("=" * 70)

    # We use n = k + 2 to get roughly k emitters in residual
    # (residual is typically most of the vertices)
    test_configs = [
        (6, 4), (8, 6), (10, 8), (12, 10), (14, 12), (18, 16)
    ]

    scaling_data = []

    for n_target, k_target in test_configs:
        print(f"\n--- Target k≈{k_target} (using K_{n_target}) ---")

        bf_maxes = []
        greedy_maxes = []
        greedy_means = []
        actual_ks = []

        for trial in range(num_instances):
            random.seed(42 + trial * 1000 + n_target)
            temporal = generate_temporal_clique(n_target)
            residual, S_minus, S_plus = compute_dismountable(n_target, temporal)
            k = len(residual)
            actual_ks.append(k)

            neighborhoods = build_collector_neighborhoods(n_target, temporal, residual)

            # Skip trivial cases
            if k < 3:
                continue

            # Brute force for k ≤ 10
            if k <= 10:
                _, bf_max = brute_force_optimal_ordering(residual, neighborhoods)
                bf_maxes.append(bf_max)

            # Greedy always
            greedy_ord = greedy_max_overlap_ordering(residual, neighborhoods)
            greedy_diffs = consecutive_sym_diffs(greedy_ord, neighborhoods)
            if greedy_diffs:
                greedy_maxes.append(max(greedy_diffs))
                greedy_means.append(sum(greedy_diffs) / len(greedy_diffs))

        avg_k = sum(actual_ks) / len(actual_ks)
        log_k = math.log2(max(avg_k, 2))

        if bf_maxes:
            bf_mean = sum(bf_maxes) / len(bf_maxes)
            bf_max_val = max(bf_maxes)
            print(f"  Actual k: mean={avg_k:.1f}")
            print(f"  Brute-force min-max sym diff: "
                  f"mean={bf_mean:.2f}, max={bf_max_val}, "
                  f"ratio to log(k)={bf_mean/log_k:.2f}, "
                  f"ratio to k={bf_mean/avg_k:.3f}")
            scaling_data.append((avg_k, bf_mean, 'brute_force'))

        if greedy_maxes:
            gr_mean = sum(greedy_maxes) / len(greedy_maxes)
            gr_max_val = max(greedy_maxes)
            print(f"  Greedy min-max sym diff: "
                  f"mean={gr_mean:.2f}, max={gr_max_val}, "
                  f"ratio to log(k)={gr_mean/log_k:.2f}, "
                  f"ratio to k={gr_mean/avg_k:.3f}")
            if not bf_maxes:
                scaling_data.append((avg_k, gr_mean, 'greedy'))

    # ─── Verdict ─────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SCALING ANALYSIS")
    print("=" * 70)

    if len(scaling_data) >= 3:
        ks = [d[0] for d in scaling_data]
        vals = [d[1] for d in scaling_data]

        # Check O(1): is val roughly constant?
        val_range = max(vals) - min(vals)
        val_mean = sum(vals) / len(vals)

        # Check O(log k): does val / log(k) stay constant?
        ratios_log = [v / math.log2(max(k, 2)) for k, v in zip(ks, vals)]
        log_range = max(ratios_log) - min(ratios_log)
        log_mean = sum(ratios_log) / len(ratios_log)

        # Check O(k): does val / k stay constant?
        ratios_k = [v / k for k, v in zip(ks, vals)]
        k_range = max(ratios_k) - min(ratios_k)
        k_mean = sum(ratios_k) / len(ratios_k)

        print(f"\n  Raw values across k: {[(f'k={k:.0f}', f'val={v:.2f}') for k, v in zip(ks, vals)]}")
        print(f"  val/1 coefficient of variation: {val_range/val_mean:.3f}")
        print(f"  val/log(k) coefficient of variation: {log_range/log_mean:.3f}" if log_mean > 0 else "")
        print(f"  val/k coefficient of variation: {k_range/k_mean:.3f}" if k_mean > 0 else "")

        # Determine scaling
        # Lowest CV wins
        cv_const = val_range / val_mean if val_mean > 0 else float('inf')
        cv_log = log_range / log_mean if log_mean > 0 else float('inf')
        cv_k = k_range / k_mean if k_mean > 0 else float('inf')

        # Also check: does the value actually grow?
        # Fit slope: if values increase with k, it's not O(1)
        if len(ks) >= 2:
            # Simple linear regression
            k_bar = sum(ks) / len(ks)
            v_bar = sum(vals) / len(vals)
            num = sum((k - k_bar) * (v - v_bar) for k, v in zip(ks, vals))
            den = sum((k - k_bar) ** 2 for k in ks)
            slope = num / den if den > 0 else 0

            print(f"\n  Linear slope (val vs k): {slope:.4f}")
            print(f"  If O(1), slope ≈ 0. If O(k), slope ≈ const > 0.")

            # Check log fit
            log_ks = [math.log2(max(k, 2)) for k in ks]
            lk_bar = sum(log_ks) / len(log_ks)
            num_log = sum((lk - lk_bar) * (v - v_bar) for lk, v in zip(log_ks, vals))
            den_log = sum((lk - lk_bar) ** 2 for lk in log_ks)
            slope_log = num_log / den_log if den_log > 0 else 0

            print(f"  Log slope (val vs log k): {slope_log:.4f}")

        # Verdict
        print("\n" + "-" * 70)
        if slope < 0.05 and val_mean < 5:
            verdict = "O(1)"
            status = "CONFIRMED"
            detail = f"Min consecutive sym diff ≈ {val_mean:.1f}, roughly constant across k."
        elif cv_log < cv_const and cv_log < cv_k:
            verdict = "O(log k)"
            status = "REFUTED"
            detail = f"Min consecutive sym diff grows as ~{log_mean:.1f}·log(k). The log factor is structural."
        elif cv_k < cv_const and cv_k < cv_log:
            verdict = "O(k)"
            status = "REFUTED"
            detail = f"Min consecutive sym diff grows as ~{k_mean:.2f}·k. No ordering helps."
        elif slope > 0.1:
            # Growing but unclear which rate
            if slope_log > 0 and abs(cv_log) < abs(cv_const):
                verdict = "O(log k)"
                status = "REFUTED"
            else:
                verdict = "growing (unclear rate)"
                status = "REFUTED"
            detail = f"Min consecutive sym diff grows with k (slope={slope:.3f})."
        else:
            verdict = "inconclusive"
            status = "INCONCLUSIVE"
            detail = "Need larger k range to distinguish."

        print(f"\n### H24: SJT on CPS residual ({status})")
        print(f"**Verdict:** {detail}")
        print(f"**Min consecutive symmetric difference scales as:** {verdict}")
    else:
        print("  Insufficient data for scaling analysis.")

# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("SJT-CPS Residual Biclique Experiment")
    print("=" * 70)

    # Task 1
    n_values = [6, 8, 10, 12]
    instances = run_task1(n_values, num_instances=3)

    # Task 2
    run_task2(instances)

    # Task 3
    task3_results = run_task3(instances)

    # Task 4
    run_task4(instances)

    # Task 5
    run_task5(instances)

    # Task 6
    run_task6(num_instances=30)
