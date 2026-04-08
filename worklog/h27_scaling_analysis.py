#!/usr/bin/env python3
"""
H27 part 2: Precise scaling analysis.

Key observations from part 1:
1. E[best rank] ≈ 0.7, NOT → 0 as k grows. The analytical independence
   assumption is WRONG because timestamps share a global pool.
2. total_missed ≈ 0.8k (avg), max ≈ 1.3k. Scales linearly in k.
3. Spanner cost ≈ 2k-1 + 0.8k ≈ 2.8k. Well within 4k-3 budget.
4. max_missed is always ≤ 2k-2 in all tested instances.

This script:
- Precisely measures the scaling of total_missed / k
- Tests adversarial cases (shifted matching, structured matrices)
- Attempts to prove total_missed ≤ 2k-2 analytically
- Tests the delegation model with full CPS dismountability
"""

import random
import math
from collections import defaultdict


def random_timestamp_matrix(k, seed=None):
    rng = random.Random(seed)
    ts = rng.sample(range(1, k * k + 1), k * k)
    M = {}
    idx = 0
    for i in range(k):
        for j in range(k):
            M[(i, j)] = ts[idx]
            idx += 1
    return M


def shifted_matching_matrix(k):
    """
    SM(k): the adversarial shifted matching matrix.
    M[i,j] = i*k + j + 1 (row-major order).
    Row i timestamps: i*k+1, i*k+2, ..., (i+1)*k.
    """
    M = {}
    for i in range(k):
        for j in range(k):
            M[(i, j)] = i * k + j + 1
    return M


def latin_square_matrix(k, seed=None):
    """
    Random Latin square: each row and column is a permutation of [1..k].
    Timestamps in [1..k²] but with Latin square structure.
    """
    rng = random.Random(seed)
    # Simple construction: M[i,j] = ((i+j) % k) * k + (permuted position)
    # Actually, just use a cyclic Latin square scaled to distinct timestamps
    M = {}
    for i in range(k):
        for j in range(k):
            rank_in_row = (i + j) % k  # 0 to k-1
            # Give distinct timestamps: row i has timestamps i*k+1 ... i*k+k
            # but reordered by Latin square
            M[(i, j)] = i * k + rank_in_row + 1
    return M


def best_relay(k, M, i, j):
    """Find best relay c' for i→j: minimize rank of c' in j's row."""
    j_sorted = sorted(range(k), key=lambda c: M[(j, c)])
    for rank_idx, c_prime in enumerate(j_sorted):
        if M[(i, c_prime)] < M[(j, c_prime)]:
            return c_prime, rank_idx
    return None, k


def greedy_delegation_order(k, M):
    """Pick root as best delegate target, then greedily add emitters."""
    remaining = set(range(k))

    best_root = None
    best_root_score = float('inf')
    for r in range(k):
        score = 0
        for i in range(k):
            if i == r:
                continue
            _, missed = best_relay(k, M, i, r)
            score += missed
        if score < best_root_score:
            best_root_score = score
            best_root = r

    order = [best_root]
    remaining.remove(best_root)

    while remaining:
        best_next = None
        best_next_missed = float('inf')
        for i in remaining:
            local_best = k + 1
            for j in order:
                relay, missed = best_relay(k, M, i, j)
                if relay is not None and missed < local_best:
                    local_best = missed
            if local_best < best_next_missed:
                best_next_missed = local_best
                best_next = i
        if best_next is None:
            best_next = next(iter(remaining))
        order.append(best_next)
        remaining.remove(best_next)

    return order


def sequential_delegation_cost(k, M, order):
    """Total missed collectors in sequential delegation."""
    total_missed = 0
    missed_list = []
    for step in range(1, len(order)):
        i = order[step]
        best_missed = k + 1
        for prev in range(step):
            j = order[prev]
            relay, missed = best_relay(k, M, i, j)
            if relay is not None and missed < best_missed:
                best_missed = missed
        if best_missed > k:
            best_missed = k  # failure
        missed_list.append(best_missed)
        total_missed += best_missed
    return total_missed, missed_list


# ─── Scaling analysis ─────────────────────────────────────────────────────

def scaling_analysis():
    """Measure total_missed/k as k grows."""
    print("=" * 70)
    print("SCALING: total_missed / k as k grows")
    print("=" * 70)
    print()

    print(f"{'k':>5} {'trials':>7} | {'avg_m/k':>8} {'max_m/k':>8} "
          f"{'avg_cost/k':>10} {'max_cost/k':>10} | "
          f"{'avg_rank':>9} {'max_rank':>9}")
    print("-" * 85)

    for k in [4, 6, 8, 10, 12, 16, 20, 25, 30, 40, 50]:
        trials = min(100, max(20, 5000 // (k * k)))
        missed_totals = []
        costs = []
        ranks_all = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            g_order = greedy_delegation_order(k, M)
            total_m, missed_list = sequential_delegation_cost(k, M, g_order)
            missed_totals.append(total_m)
            costs.append(2 * k - 1 + total_m)
            ranks_all.extend(missed_list)

        avg_m = sum(missed_totals) / trials
        max_m = max(missed_totals)
        avg_c = sum(costs) / trials
        max_c = max(costs)
        avg_r = sum(ranks_all) / len(ranks_all) if ranks_all else 0
        max_r = max(ranks_all) if ranks_all else 0

        print(f"{k:5d} {trials:7d} | {avg_m/k:8.4f} {max_m/k:8.4f} "
              f"{avg_c/k:10.4f} {max_c/k:10.4f} | "
              f"{avg_r:9.3f} {max_r:9d}")

    print()
    print("  If avg_m/k → constant c < 2, total_missed ≤ 2k-2 is plausible.")
    print("  Spanner cost = 2k-1 + total_missed ≤ (2+c)k - 1 ≤ 4k-3 requires c ≤ 2.")
    print()


# ─── Adversarial cases ────────────────────────────────────────────────────

def adversarial_analysis():
    """Test on adversarial matrix structures."""
    print("=" * 70)
    print("ADVERSARIAL: Shifted matching and structured matrices")
    print("=" * 70)
    print()

    for k in [4, 6, 8, 10, 12, 16]:
        print(f"--- k={k} ---")

        # Shifted matching
        M_sm = shifted_matching_matrix(k)
        g_order = greedy_delegation_order(k, M_sm)
        total_m, missed_list = sequential_delegation_cost(k, M_sm, g_order)
        cost = 2 * k - 1 + total_m
        budget = 4 * k - 3
        print(f"  SM(k): missed={total_m}, cost={cost}, budget={budget}, "
              f"within={'YES' if cost <= budget else 'NO'}")
        print(f"    per-step: {missed_list}")

        # Latin square
        M_ls = latin_square_matrix(k)
        g_order = greedy_delegation_order(k, M_ls)
        total_m, missed_list = sequential_delegation_cost(k, M_ls, g_order)
        cost = 2 * k - 1 + total_m
        print(f"  Latin: missed={total_m}, cost={cost}, budget={budget}, "
              f"within={'YES' if cost <= budget else 'NO'}")
        print(f"    per-step: {missed_list}")

        # Random (5 samples)
        worst_m = 0
        for trial in range(5):
            M = random_timestamp_matrix(k, seed=trial * 7777 + k)
            g_order = greedy_delegation_order(k, M)
            total_m, _ = sequential_delegation_cost(k, M, g_order)
            worst_m = max(worst_m, total_m)
        print(f"  Random (5 trials, worst): missed={worst_m}, cost={2*k-1+worst_m}")
        print()


# ─── Worst-case search ────────────────────────────────────────────────────

def worst_case_search():
    """
    Search for matrices that maximize total_missed.
    Use random search with many seeds.
    """
    print("=" * 70)
    print("WORST-CASE SEARCH: Find matrices maximizing total_missed")
    print("=" * 70)
    print()

    for k in [4, 5, 6, 7, 8]:
        n_trials = 2000
        worst_missed = 0
        worst_seed = None
        budget = 2 * k - 2

        for trial in range(n_trials):
            M = random_timestamp_matrix(k, seed=trial)
            g_order = greedy_delegation_order(k, M)
            total_m, _ = sequential_delegation_cost(k, M, g_order)
            if total_m > worst_missed:
                worst_missed = total_m
                worst_seed = trial

        # Also try all orderings for the worst matrix (small k)
        if worst_seed is not None and k <= 6:
            M = random_timestamp_matrix(k, seed=worst_seed)
            from itertools import permutations
            worst_any_order = 0
            for perm in permutations(range(k)):
                total_m, _ = sequential_delegation_cost(k, M, list(perm))
                worst_any_order = max(worst_any_order, total_m)
            print(f"  k={k}: worst_greedy={worst_missed} (seed={worst_seed}), "
                  f"worst_any_order={worst_any_order}, budget={budget}, "
                  f"within={'YES' if worst_any_order <= budget else 'NO'}")
        else:
            print(f"  k={k}: worst_greedy={worst_missed} (seed={worst_seed}), "
                  f"budget={budget}, "
                  f"within={'YES' if worst_missed <= budget else 'NO'}")

    print()


# ─── The analytical argument ──────────────────────────────────────────────

def analytical_argument():
    """
    Develop the analytical bound.

    Key insight from Task 4 (part 1): E[best rank] for a SPECIFIC emitter i
    delegating to its best delegate is ~0.7, roughly constant in k.

    Why NOT geometric(1/2) with independent delegates?
    Because timestamps are drawn from a shared pool of k² values.
    When M[i,c'] < M[j,c'], this depends on the GLOBAL structure.

    Better model: for random M with k² distinct timestamps,
    consider emitter i and delegate j.
    j's row sorted by timestamp: c'_0, c'_1, ..., c'_{k-1}.
    P(c'_r is a valid relay for i) = P(M[i,c'_r] < M[j,c'_r]).

    In a random matrix with ALL k² timestamps distinct:
    M[j,c'_r] has rank r in j's row (by definition).
    Globally, M[j,c'_r] has some rank R among all k² timestamps.
    M[i,c'_r] is an independent random position in its row.

    P(M[i,c'_r] < M[j,c'_r]) = P(uniform < M[j,c'_r]) = (R-1)/(k²-1)
    where R = global rank of M[j,c'_r].

    For a random matrix, E[R | rank in j's row = r] ≈ (r+0.5)/(k) * k²
    = (r+0.5) * k.

    So P(valid relay at rank r) ≈ (r+0.5)*k / k² = (r+0.5)/k.

    For r=0: P ≈ 0.5/k ← VERY SMALL for large k!
    For r=1: P ≈ 1.5/k
    ...

    This means: for a SINGLE delegate j, P(rank=0) ≈ 1/(2k), not 1/2!

    With k-1 delegates: P(some delegate has rank=0) ≈ (k-1)/(2k) ≈ 1/2.
    So E[best rank] doesn't go to 0 — it stays O(1)! This matches the empirical ~0.7.

    Let me verify this refined analysis.
    """
    print("=" * 70)
    print("ANALYTICAL: Refined probability model")
    print("=" * 70)
    print()

    # Verify: P(rank-0 relay exists for i→j) for a single delegate j
    print("P(rank-0 relay) for a SINGLE delegate j:")
    print(f"{'k':>5} | {'empirical':>10} {'analytic(1/2)':>14} {'analytic(0.5/k)':>16}")
    print("-" * 50)

    for k in [4, 6, 8, 10, 16, 20, 30]:
        trials = min(200, max(50, 10000 // (k * k)))
        rank0_count = 0
        total_pairs = 0

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            for i in range(k):
                for j in range(k):
                    if i == j:
                        continue
                    # What's the rank-0 column for j?
                    j_min_col = min(range(k), key=lambda c: M[(j, c)])
                    # Is it a valid relay?
                    if M[(i, j_min_col)] < M[(j, j_min_col)]:
                        rank0_count += 1
                    total_pairs += 1

        emp = rank0_count / total_pairs
        # Analytic: P(M[i,c0] < M[j,c0]) where c0 = argmin_j M[j,·]
        # M[j,c0] is the minimum in j's row, so it has expected global rank ~k/2
        # P(M[i,c0] < M[j,c0]) = E[R]/k² where R = global rank of M[j,c0]
        # For the minimum of k uniform draws from [1,k²]: E = k²/(k+1) ≈ k
        # Wait, E[min of k values from 1..k²] = k²/(k+1)
        # P = (k²/(k+1) - 1) / (k²-1) ≈ k/(k+1)... no that's too high.

        # Actually: M[j,c0] is the minimum of k values, each drawn WITHOUT
        # replacement from the pool. But each row draws k values from k² total.
        # The row's values are a random k-subset of [1..k²].
        # The minimum of a random k-subset of [1..k²] has E ≈ k²/(k+1).
        # Hmm, that's k for large k. Let me compute:
        # E[min of k uniform draws from {1,...,N}] = (N+1)/(k+1)
        # Here N=k², so E[min] = (k²+1)/(k+1) ≈ k-1.
        # P(M[i,c0] < M[j,c0]) where M[i,c0] is from i's row.
        # Given M[j,c0] = v, P(M[i,c0] < v) = (v-1)/(k²-1) approximately.
        # E[P] = E[(M[j,c0]-1)]/(k²-1) ≈ (k-2)/(k²-1) ≈ 1/k.

        analytic_half = 0.5
        analytic_refined = 1.0 / (k + 1)

        print(f"{k:5d} | {emp:10.4f} {analytic_half:14.4f} {analytic_refined:16.4f}")

    print()

    # Now: P(rank=0 with BEST delegate)
    print("P(rank=0) with BEST delegate among k-1 options:")
    print(f"{'k':>5} | {'empirical':>10} {'1-(1-1/k)^(k-1)':>18} {'1-1/e':>8}")
    print("-" * 50)

    for k in [4, 6, 8, 10, 16, 20, 30]:
        trials = min(200, max(50, 10000 // (k * k)))
        rank0_best = 0
        total_emitters = 0

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            for i in range(k):
                has_rank0 = False
                for j in range(k):
                    if i == j:
                        continue
                    j_min_col = min(range(k), key=lambda c: M[(j, c)])
                    if M[(i, j_min_col)] < M[(j, j_min_col)]:
                        has_rank0 = True
                        break
                if has_rank0:
                    rank0_best += 1
                total_emitters += 1

        emp = rank0_best / total_emitters
        # If P(rank-0 for single delegate) ≈ 1/k,
        # P(rank-0 for SOME delegate) ≈ 1 - (1-1/k)^{k-1}
        analytic = 1 - (1 - 1/k) ** (k - 1)

        print(f"{k:5d} | {emp:10.4f} {analytic:18.4f} {1-1/math.e:8.4f}")

    print()
    print("  Converges to 1-1/e ≈ 0.632!")
    print("  So ~63% of emitters get a rank-0 relay (0 missed).")
    print("  The other ~37% get rank ≥ 1.")
    print()

    # Distribution of best rank for the non-rank-0 emitters
    print("Distribution of best rank (conditioned on rank ≥ 1):")
    print(f"{'k':>5} | {'E[rank|rank≥1]':>15} {'E[rank|rank≥2]':>15}")
    print("-" * 40)

    for k in [6, 10, 16, 20, 30]:
        trials = min(200, max(50, 10000 // (k * k)))
        ranks_ge1 = []
        ranks_ge2 = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            for i in range(k):
                best_rank = k
                for j in range(k):
                    if i == j:
                        continue
                    relay, rank = best_relay(k, M, i, j)
                    if relay is not None and rank < best_rank:
                        best_rank = rank
                if best_rank >= 1:
                    ranks_ge1.append(best_rank)
                if best_rank >= 2:
                    ranks_ge2.append(best_rank)

        e1 = sum(ranks_ge1) / len(ranks_ge1) if ranks_ge1 else 0
        e2 = sum(ranks_ge2) / len(ranks_ge2) if ranks_ge2 else 0
        print(f"{k:5d} | {e1:15.3f} {e2:15.3f}")

    print()


# ─── Total missed: scaling law ────────────────────────────────────────────

def total_missed_scaling():
    """
    Measure total_missed precisely for the greedy delegation.

    If ~63% of emitters have 0 missed and the rest have ~1.8 missed,
    then E[total_missed] ≈ 0.37 * 1.8 * k ≈ 0.67k.

    For the 4k-3 budget:
    cost = 2k-1 + total_missed ≈ 2.67k ≤ 4k-3 for k ≥ 1. Always fine.

    For 2n-3 = 4k-3: also always fine.

    The question is whether total_missed ≤ 2k-2 ALWAYS holds.
    """
    print("=" * 70)
    print("TOTAL MISSED SCALING: precise coefficients")
    print("=" * 70)
    print()

    results = []

    for k in [4, 6, 8, 10, 12, 16, 20, 25, 30, 40, 50]:
        trials = min(200, max(30, 10000 // (k * k)))
        missed_totals = []
        rank0_fracs = []

        for trial in range(trials):
            M = random_timestamp_matrix(k, seed=trial * 1000 + k)
            g_order = greedy_delegation_order(k, M)
            total_m, missed_list = sequential_delegation_cost(k, M, g_order)
            missed_totals.append(total_m)
            rank0_frac = sum(1 for m in missed_list if m == 0) / len(missed_list) if missed_list else 0
            rank0_fracs.append(rank0_frac)

        avg_m = sum(missed_totals) / trials
        max_m = max(missed_totals)
        avg_r0 = sum(rank0_fracs) / trials

        results.append((k, avg_m, max_m, avg_r0, trials))

    print(f"{'k':>5} {'avg_m':>7} {'max_m':>7} {'avg_m/k':>8} {'max_m/k':>8} "
          f"{'%rank0':>7} {'2k-2':>6} {'slack':>6}")
    print("-" * 65)

    for k, avg_m, max_m, avg_r0, trials in results:
        print(f"{k:5d} {avg_m:7.1f} {max_m:7d} {avg_m/k:8.3f} {max_m/k:8.3f} "
              f"{avg_r0:7.1%} {2*k-2:6d} {2*k-2-max_m:6d}")

    print()

    # Fit: total_missed ≈ c * k
    # Use least squares on (k, avg_m) pairs
    ks = [r[0] for r in results]
    avg_ms = [r[1] for r in results]
    max_ms = [r[2] for r in results]

    # Linear fit y = c*x
    c_avg = sum(k * m for k, m in zip(ks, avg_ms)) / sum(k * k for k in ks)
    c_max = sum(k * m for k, m in zip(ks, max_ms)) / sum(k * k for k in ks)

    print(f"  Linear fit: avg_missed ≈ {c_avg:.3f} * k")
    print(f"  Linear fit: max_missed ≈ {c_max:.3f} * k")
    print(f"  Budget needs: c_max < 2.0 → {'YES' if c_max < 2.0 else 'NO'}")
    print()

    # Log-log fit to check if actually k * log(k) or similar
    # y = a * k^b
    import numpy as np
    try:
        log_ks = [math.log(k) for k in ks]
        log_avgs = [math.log(m) if m > 0 else 0 for m in avg_ms]
        log_maxs = [math.log(m) if m > 0 else 0 for m in max_ms]

        # Linear regression on logs
        n = len(ks)
        mean_lk = sum(log_ks) / n
        mean_la = sum(log_avgs) / n
        num = sum((lk - mean_lk) * (la - mean_la) for lk, la in zip(log_ks, log_avgs))
        den = sum((lk - mean_lk) ** 2 for lk in log_ks)
        b_avg = num / den if den > 0 else 1
        a_avg = math.exp(mean_la - b_avg * mean_lk)

        mean_lm = sum(log_maxs) / n
        num = sum((lk - mean_lk) * (lm - mean_lm) for lk, lm in zip(log_ks, log_maxs))
        b_max = num / den if den > 0 else 1
        a_max = math.exp(mean_lm - b_max * mean_lk)

        print(f"  Power law fit: avg_missed ≈ {a_avg:.3f} * k^{b_avg:.3f}")
        print(f"  Power law fit: max_missed ≈ {a_max:.3f} * k^{b_max:.3f}")
        print(f"  If exponent ≈ 1, it's linear. If > 1, superlinear (dangerous).")
    except:
        pass

    print()


# ─── The proof structure ──────────────────────────────────────────────────

def proof_sketch():
    """
    Print the proof sketch based on empirical findings.
    """
    print("=" * 70)
    print("PROOF SKETCH: Sequential delegation spanner ≤ 4k-3")
    print("=" * 70)
    print()
    print("""
THEOREM (claimed): For any k×k bipartite temporal graph with distinct
timestamps, the sequential delegation spanner has at most 4k-3 edges.

PROOF SKETCH:

1. DELEGATION MODEL
   Emitter i delegates to emitter j via relay collector c' where:
   - M[i,c'] < M[j,c'] (temporal monotonicity at relay)
   - c' minimizes rank(j, c') = |{d : M[j,d] < M[j,c']}| (fewest missed)

   Missed collectors = {d : M[j,d] < M[j,c']} (rank of c' in j's row).

2. SPANNER CONSTRUCTION
   - Root emitter: k edges (all collectors).
   - Each of k-1 non-root emitters: 1 delegation edge + missed(i) direct edges.
   - Total = k + (k-1) + Σ missed(i) = 2k-1 + Σ missed(i).
   - Budget: 4k-3. Need: Σ missed(i) ≤ 2k-2.

3. THE RELAY RANK BOUND
   For emitter i delegating to best delegate j among processed emitters:
   - Relay c' has rank r in j's row.
   - missed(i) = r.

   CLAIM: For any timestamp matrix M and greedy ordering,
   Σ_{i=1}^{k-1} missed(i) ≤ 2k-2.

   HEURISTIC ARGUMENT (not a proof):
   - P(rank-0 relay from i to specific j) ≈ 1/k (the minimum of j's row
     has global rank ~k, and P(M[i,c0] < global-rank-k value) ≈ 1/k).
   - With k-1 delegates: P(some delegate gives rank 0) ≈ 1-(1-1/k)^{k-1} ≈ 1-1/e.
   - ~63% of emitters contribute 0 missed. Remaining ~37% contribute ≈ 1.7 each.
   - E[total_missed] ≈ 0.37 * 1.7 * k ≈ 0.63k.
   - But max_missed scales as ~1.0k empirically. Always < 2k-2.

4. THE GAP
   The heuristic gives E[total] ≈ 0.63k but max ≈ 1.0k.
   We need max ≤ 2k-2. The slack is about k-2.

   To prove this, we'd need: even in the worst case, the greedy delegation
   cannot make every emitter miss more than 2 collectors on average.

   Pigeonhole argument attempt: if total_missed > 2k-2, then at least
   one collector d is missed by ≥ 3 emitters. But the greedy ordering
   ensures that once a collector d is missed by emitter i (delegating to j),
   subsequent emitters can use j (who DOES reach d) or other delegates
   that reach d. So the number of emitters missing d is limited.

   This needs formalization.

5. CONNECTION TO 2n-3 CONJECTURE
   Full spanner = 2d (dismounted) + B (biclique), where n = d + 2k.
   B ≤ 4k-3 gives total ≤ 2d + 4k - 3 = 2(d + 2k) - 3 = 2n - 3. QED.
""")


# ─── Main ──────────────────────────────────────────────────────────────────

def run():
    print("H27 Part 2: SCALING ANALYSIS AND PROOF ATTEMPT")
    print("=" * 70)
    print()

    scaling_analysis()
    print()
    adversarial_analysis()
    print()
    worst_case_search()
    print()
    analytical_argument()
    print()
    total_missed_scaling()
    print()
    proof_sketch()


if __name__ == '__main__':
    run()
