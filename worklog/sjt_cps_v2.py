#!/usr/bin/env python3
"""
V2: More rigorous test of SJT ordering on CPS residual biclique.

Key fixes from V1:
1. Use the full vertex set as emitters (not just non-dismountable residual)
   to get actual k=n scaling
2. Check neighborhood saturation — if |N(e)| ≈ n for all e, then
   symmetric differences are trivially small
3. Use the proper CPS biclique model: separate emitter/collector copies
4. Test larger k values
"""

import random
import itertools
import math
import sys
from collections import defaultdict

# ─── CPS Biclique Model ─────────────────────────────────────────────────────

def generate_temporal_clique(n, seed=None):
    """Generate temporal K_n with distinct timestamps on edges."""
    if seed is not None:
        random.seed(seed)
    edges = [(i, j) for i in range(n) for j in range(i+1, n)]
    timestamps = list(range(1, len(edges) + 1))
    random.shuffle(timestamps)
    return {e: t for e, t in zip(edges, timestamps)}

def get_time(temporal, i, j):
    return temporal[(min(i,j), max(i,j))]

def build_biclique_neighborhoods(n, temporal):
    """
    CPS biclique: emitters = collectors = [0, n).

    Emitter e's collector neighborhood N(e):
    Collector c is in N(e) if there exists a 2-hop temporal path
    e -> w -> c with t(e,w) < t(w,c), for some intermediate w.

    This models the "reachability through temporal journeys" that
    defines the CPS residual structure.
    """
    neighborhoods = {}
    for e in range(n):
        N_e = set()
        for c in range(n):
            if c == e:
                continue
            for w in range(n):
                if w == e or w == c:
                    continue
                if get_time(temporal, e, w) < get_time(temporal, w, c):
                    N_e.add(c)
                    break
        neighborhoods[e] = N_e
    return neighborhoods

def build_constrained_biclique(n, temporal, hop_constraint=2):
    """
    More constrained neighborhoods using the extremal matching structure.

    For each emitter e, its collector neighborhood is defined by:
    N(e) = {c : the min-time path from e reaches c}

    Specifically, using S⁻ (row minima) matching:
    Emitter e connects to collector c if t(e, S⁻(e)) < t(S⁻(e), c)

    This is the RESIDUAL after the greedy spanner picks S⁻ edges.
    """
    # Compute S⁻: for each vertex, its earliest neighbor
    S_minus = {}
    for v in range(n):
        best_u, best_t = None, float('inf')
        for u in range(n):
            if u == v:
                continue
            t = get_time(temporal, v, u)
            if t < best_t:
                best_t = t
                best_u = u
        S_minus[v] = (best_u, best_t)

    # Residual neighborhood: what collectors does emitter e miss
    # when it delegates to its S⁻ partner?
    # N(e) = {c : ∃ path through S⁻(e) reaching c with time-respecting edges}
    neighborhoods = {}
    for e in range(n):
        N_e = set()
        w, t_ew = S_minus[e]
        for c in range(n):
            if c == e or c == w:
                continue
            # Can reach c from e via w if t(e,w) < t(w,c)
            if t_ew < get_time(temporal, w, c):
                N_e.add(c)
        neighborhoods[e] = N_e

    return neighborhoods, S_minus

def build_extremal_residual(n, temporal):
    """
    The actual CPS residual biclique structure.

    After the spanner algorithm picks edges greedily, the residual
    consists of edges NOT covered by the chosen spanner edges.

    For each emitter e, define:
    - Forward neighborhood F(e) = {c : t(e,c) > t(e, S⁻(e))}
      (collectors reachable by later edges from e)
    - Backward neighborhood B(e) = {c : t(e,c) < t(e, S⁺(e))}
      (collectors reachable by earlier edges from e)

    The residual is F(e) ∩ B(e) — the collectors that need
    indirect coverage.
    """
    neighborhoods_full = {}  # Full 2-hop neighborhoods
    neighborhoods_constrained = {}  # Only through S⁻ partner

    # Full 2-hop
    for e in range(n):
        N_e = set()
        for c in range(n):
            if c == e:
                continue
            for w in range(n):
                if w == e or w == c:
                    continue
                if get_time(temporal, e, w) < get_time(temporal, w, c):
                    N_e.add(c)
                    break
        neighborhoods_full[e] = N_e

    return neighborhoods_full


# ─── Ordering algorithms ────────────────────────────────────────────────────

def consecutive_sym_diffs(ordering, neighborhoods):
    diffs = []
    for i in range(len(ordering) - 1):
        Ni = neighborhoods[ordering[i]]
        Nj = neighborhoods[ordering[i+1]]
        diffs.append(len(Ni ^ Nj))
    return diffs

def brute_force_optimal(emitters, neighborhoods):
    """Exact optimal for k ≤ 10."""
    if len(emitters) > 10:
        return None, None, None

    best_max = float('inf')
    best_ord = None

    for perm in itertools.permutations(emitters):
        diffs = consecutive_sym_diffs(perm, neighborhoods)
        mx = max(diffs) if diffs else 0
        if mx < best_max:
            best_max = mx
            best_ord = perm

    diffs = consecutive_sym_diffs(best_ord, neighborhoods) if best_ord else []
    return best_ord, best_max, diffs

def greedy_ordering(emitters, neighborhoods):
    """Greedy: next emitter maximizes overlap with current."""
    remaining = set(emitters)
    current = max(remaining, key=lambda e: len(neighborhoods[e]))
    ordering = [current]
    remaining.remove(current)

    while remaining:
        best = max(remaining,
                   key=lambda e: len(neighborhoods[current] & neighborhoods[e]))
        ordering.append(best)
        remaining.remove(best)
        current = best

    return ordering

def random_ordering(emitters):
    o = list(emitters)
    random.shuffle(o)
    return o


# ─── Saturation check ───────────────────────────────────────────────────────

def check_saturation(n, neighborhoods):
    """Check if neighborhoods are nearly complete (trivially small sym diffs)."""
    sizes = [len(neighborhoods[e]) for e in range(n)]
    max_possible = n - 1  # can reach all other vertices
    avg_size = sum(sizes) / len(sizes)
    saturation = avg_size / max_possible
    return saturation, avg_size, min(sizes), max(sizes)


# ─── Main experiment ────────────────────────────────────────────────────────

def run_scaling_experiment():
    """
    Test scaling of min consecutive sym diff across k values.

    Key question: does the min-max consecutive symmetric difference
    grow with k, or stay O(1)?
    """
    print("=" * 70)
    print("SJT-CPS RESIDUAL BICLIQUE: SCALING EXPERIMENT (V2)")
    print("=" * 70)

    # Test configurations: (n, num_instances)
    # We use n directly as k (all vertices are emitters)
    configs = [
        (5, 50),
        (6, 50),
        (7, 50),
        (8, 40),
        (9, 30),
        (10, 30),
        (12, 20),
        (14, 15),
        (16, 10),
    ]

    # Store results for scaling analysis
    all_results = []

    for n, num_inst in configs:
        print(f"\n{'─'*60}")
        print(f"k = {n} ({num_inst} instances)")
        print(f"{'─'*60}")

        bf_maxes = []
        greedy_maxes = []
        greedy_means = []
        random_maxes = []
        saturations = []

        # Also track constrained neighborhoods
        constrained_bf_maxes = []
        constrained_greedy_maxes = []
        constrained_saturations = []

        for trial in range(num_inst):
            seed = trial * 10000 + n * 100
            temporal = generate_temporal_clique(n, seed=seed)

            # ── Full 2-hop neighborhoods ──
            nbrs_full = build_extremal_residual(n, temporal)
            emitters = list(range(n))

            sat, avg_sz, min_sz, max_sz = check_saturation(n, nbrs_full)
            saturations.append(sat)

            if n <= 10:
                _, bf_max, _ = brute_force_optimal(emitters, nbrs_full)
                if bf_max is not None:
                    bf_maxes.append(bf_max)

            g_ord = greedy_ordering(emitters, nbrs_full)
            g_diffs = consecutive_sym_diffs(g_ord, nbrs_full)
            if g_diffs:
                greedy_maxes.append(max(g_diffs))
                greedy_means.append(sum(g_diffs)/len(g_diffs))

            # Random baseline (mean of 20 random orderings)
            r_maxes = []
            for _ in range(20):
                r_ord = random_ordering(emitters)
                r_diffs = consecutive_sym_diffs(r_ord, nbrs_full)
                if r_diffs:
                    r_maxes.append(max(r_diffs))
            if r_maxes:
                random_maxes.append(sum(r_maxes)/len(r_maxes))

            # ── Constrained (S⁻ partner only) neighborhoods ──
            nbrs_con, S_minus = build_constrained_biclique(n, temporal)
            c_sat, _, _, _ = check_saturation(n, nbrs_con)
            constrained_saturations.append(c_sat)

            if n <= 10:
                _, c_bf_max, _ = brute_force_optimal(emitters, nbrs_con)
                if c_bf_max is not None:
                    constrained_bf_maxes.append(c_bf_max)

            c_g_ord = greedy_ordering(emitters, nbrs_con)
            c_g_diffs = consecutive_sym_diffs(c_g_ord, nbrs_con)
            if c_g_diffs:
                constrained_greedy_maxes.append(max(c_g_diffs))

        # Report
        avg_sat = sum(saturations)/len(saturations)
        avg_c_sat = sum(constrained_saturations)/len(constrained_saturations)

        print(f"  FULL 2-HOP neighborhoods:")
        print(f"    Saturation: {avg_sat:.3f} (avg |N(e)|/{n-1})")
        if bf_maxes:
            print(f"    Brute-force optimal max sym diff: "
                  f"mean={sum(bf_maxes)/len(bf_maxes):.2f}, "
                  f"median={sorted(bf_maxes)[len(bf_maxes)//2]}, "
                  f"max={max(bf_maxes)}")
        print(f"    Greedy max sym diff: "
              f"mean={sum(greedy_maxes)/len(greedy_maxes):.2f}, "
              f"max={max(greedy_maxes)}")
        print(f"    Random max sym diff: "
              f"mean={sum(random_maxes)/len(random_maxes):.2f}")

        print(f"  CONSTRAINED (S⁻ partner) neighborhoods:")
        print(f"    Saturation: {avg_c_sat:.3f}")
        if constrained_bf_maxes:
            print(f"    Brute-force optimal max sym diff: "
                  f"mean={sum(constrained_bf_maxes)/len(constrained_bf_maxes):.2f}, "
                  f"median={sorted(constrained_bf_maxes)[len(constrained_bf_maxes)//2]}, "
                  f"max={max(constrained_bf_maxes)}")
        print(f"    Greedy max sym diff: "
              f"mean={sum(constrained_greedy_maxes)/len(constrained_greedy_maxes):.2f}, "
              f"max={max(constrained_greedy_maxes)}")

        # Record for scaling
        if bf_maxes:
            all_results.append({
                'k': n, 'type': 'full_bf',
                'mean_max': sum(bf_maxes)/len(bf_maxes),
                'saturation': avg_sat
            })
        all_results.append({
            'k': n, 'type': 'full_greedy',
            'mean_max': sum(greedy_maxes)/len(greedy_maxes),
            'saturation': avg_sat
        })
        if constrained_bf_maxes:
            all_results.append({
                'k': n, 'type': 'constrained_bf',
                'mean_max': sum(constrained_bf_maxes)/len(constrained_bf_maxes),
                'saturation': avg_c_sat
            })
        all_results.append({
            'k': n, 'type': 'constrained_greedy',
            'mean_max': sum(constrained_greedy_maxes)/len(constrained_greedy_maxes),
            'saturation': avg_c_sat
        })

    # ─── Scaling analysis ────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SCALING ANALYSIS")
    print("=" * 70)

    for nbr_type in ['full_bf', 'full_greedy', 'constrained_bf', 'constrained_greedy']:
        data = [r for r in all_results if r['type'] == nbr_type]
        if len(data) < 3:
            continue

        ks = [d['k'] for d in data]
        vals = [d['mean_max'] for d in data]
        sats = [d['saturation'] for d in data]

        print(f"\n  [{nbr_type}]")
        for k, v, s in zip(ks, vals, sats):
            log_k = math.log2(k)
            print(f"    k={k:2d}: mean_max_symdiff={v:.2f}, "
                  f"v/1={v:.2f}, v/log(k)={v/log_k:.2f}, v/k={v/k:.3f}, "
                  f"sat={s:.3f}")

        # Linear regression: val vs k
        k_bar = sum(ks)/len(ks)
        v_bar = sum(vals)/len(vals)
        num = sum((k-k_bar)*(v-v_bar) for k,v in zip(ks, vals))
        den = sum((k-k_bar)**2 for k in ks)
        slope = num/den if den > 0 else 0

        # Log regression: val vs log(k)
        log_ks = [math.log2(k) for k in ks]
        lk_bar = sum(log_ks)/len(log_ks)
        num_log = sum((lk-lk_bar)*(v-v_bar) for lk,v in zip(log_ks, vals))
        den_log = sum((lk-lk_bar)**2 for lk in log_ks)
        slope_log = num_log/den_log if den_log > 0 else 0

        # R² for each model
        ss_tot = sum((v-v_bar)**2 for v in vals)
        if ss_tot > 0:
            # Linear
            intercept = v_bar - slope * k_bar
            ss_res_lin = sum((v - (slope*k + intercept))**2 for k,v in zip(ks, vals))
            r2_lin = 1 - ss_res_lin/ss_tot

            # Log
            intercept_log = v_bar - slope_log * lk_bar
            ss_res_log = sum((v - (slope_log*lk + intercept_log))**2 for lk,v in zip(log_ks, vals))
            r2_log = 1 - ss_res_log/ss_tot

            # Constant
            r2_const = 0  # by definition

            print(f"    Slope (linear): {slope:.4f}, R²={r2_lin:.3f}")
            print(f"    Slope (log):    {slope_log:.4f}, R²={r2_log:.3f}")
            print(f"    Constant model: mean={v_bar:.2f}, R²=0 (baseline)")

        # Check saturation trend
        sat_slope_num = sum((k-k_bar)*(s-sum(sats)/len(sats)) for k,s in zip(ks, sats))
        sat_slope = sat_slope_num/den if den > 0 else 0
        print(f"    Saturation trend: slope={sat_slope:.5f}")

    # ─── Delegation simulation ───────────────────────────────────────────
    print("\n" + "=" * 70)
    print("DELEGATION SIMULATION (Task 5)")
    print("=" * 70)

    for n in [6, 8, 10, 12]:
        temporal = generate_temporal_clique(n, seed=999)
        nbrs_full = build_extremal_residual(n, temporal)
        nbrs_con, _ = build_constrained_biclique(n, temporal)
        emitters = list(range(n))

        for label, nbrs in [("full", nbrs_full), ("constrained", nbrs_con)]:
            # Optimal ordering
            if n <= 10:
                opt_ord, _, _ = brute_force_optimal(emitters, nbrs)
            else:
                opt_ord = greedy_ordering(emitters, nbrs)

            # Delegation: each eliminated emitter delegates to next
            total_missed_opt = 0
            for i in range(len(opt_ord)-1):
                missed = nbrs[opt_ord[i]] - nbrs[opt_ord[i+1]]
                total_missed_opt += len(missed)

            # Random delegation baseline
            rand_totals = []
            for _ in range(100):
                r_ord = random_ordering(emitters)
                total = sum(len(nbrs[r_ord[i]] - nbrs[r_ord[i+1]])
                           for i in range(len(r_ord)-1))
                rand_totals.append(total)

            cps_bound = n * math.ceil(math.log2(max(n, 2)))
            print(f"\n  K_{n} ({label}): CPS bound ~{cps_bound}")
            print(f"    Optimal delegation total missed: {total_missed_opt}")
            print(f"    Random delegation: mean={sum(rand_totals)/len(rand_totals):.1f}, "
                  f"max={max(rand_totals)}")

    # ─── Final verdict ───────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    # Use constrained neighborhoods for the structural question
    # (full neighborhoods are trivially saturated)
    con_data = [r for r in all_results if r['type'] == 'constrained_bf']
    if not con_data:
        con_data = [r for r in all_results if r['type'] == 'constrained_greedy']

    if con_data:
        ks = [d['k'] for d in con_data]
        vals = [d['mean_max'] for d in con_data]
        sats = [d['saturation'] for d in con_data]

        # Check if saturation explains the result
        if all(s > 0.8 for s in sats):
            print("\n  WARNING: Neighborhoods are >80% saturated at all k values.")
            print("  The low symmetric differences may be an artifact of saturation,")
            print("  not a genuine structural property of the CPS residual.")

        k_bar = sum(ks)/len(ks)
        v_bar = sum(vals)/len(vals)
        den = sum((k-k_bar)**2 for k in ks)
        num = sum((k-k_bar)*(v-v_bar) for k,v in zip(ks, vals))
        slope = num/den if den > 0 else 0

        if slope > 0.3:
            scaling = "O(k)"
            status = "REFUTED"
        elif slope > 0.05:
            scaling = "O(log k)"
            status = "REFUTED"
        elif v_bar < 5 and abs(slope) < 0.05:
            scaling = "O(1)"
            status = "CONFIRMED — but see saturation caveat"
        else:
            scaling = "inconclusive"
            status = "INCONCLUSIVE"

        print(f"\n### H24: SJT on CPS residual ({status})")
        print(f"**Verdict:** Mean optimal max consecutive sym diff = {v_bar:.2f}, slope = {slope:.4f}")
        print(f"**Min consecutive symmetric difference scales as:** {scaling}")
        print(f"**Saturation:** {sum(sats)/len(sats):.3f} average")

        if all(s > 0.7 for s in sats):
            print(f"\n**CRITICAL CAVEAT:** High saturation ({sum(sats)/len(sats):.1%}) means")
            print(f"  most emitter pairs share almost all collectors. The O(1) result")
            print(f"  is TRIVIALLY TRUE when neighborhoods are near-complete — it says")
            print(f"  nothing about sparse residuals. The real test would require")
            print(f"  neighborhoods with saturation < 50%.")


if __name__ == "__main__":
    run_scaling_experiment()
