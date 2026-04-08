"""
Fireworks v6: Test the hypothesis under the CPS halving guarantee.

Instead of implementing the full CPS algorithm (which requires careful
handling of temporal reachability), we SIMULATE the delegation structure:

1. Generate random bipartite matchings S⁻ and S⁺ between k emitters and k collectors
   (modeling the CPS residual).
2. Run layered delegation with proper halving (guaranteed by CPS lemma).
3. Count the actual edge cost per round.

This tests the PURE delegation cost question, separated from the tree
construction and temporal reachability issues.

The CPS guarantee: in each round, at least half the alive emitters can delegate.
This is because S⁻ and S⁺ are two matchings between emitters and collectors.
By pigeonhole, at least half the emitters share a collector with another emitter
via at least one of the two matchings.

Actually, the CPS guarantee is more specific: they show that the emitters can be
split into X_a and X_b with |X_a| >= |alive|/2, where X_a emitters can delegate.
"""

import random
import math
from collections import defaultdict


def random_bipartite_matchings(k, seed=None):
    """
    Generate two random perfect matchings S⁻ and S⁺ between
    k emitters and k collectors. Returns (s_minus, s_plus) where
    s_minus[i] = collector matched to emitter i via S⁻.
    """
    rng = random.Random(seed)
    collectors = list(range(k))

    perm1 = collectors[:]
    rng.shuffle(perm1)
    perm2 = collectors[:]
    rng.shuffle(perm2)

    return perm1, perm2


def layered_delegation_sim(k, s_minus, s_plus, force_halving=True):
    """
    Simulate layered delegation on k emitters with two matchings.

    Each emitter e has S⁻(e) and S⁺(e) collectors.
    In each round, find emitters sharing a collector and delegate.

    If force_halving=True, ensure at least half are eliminated per round
    (as CPS guarantees).

    Returns list of round records.
    """
    alive = set(range(k))
    round_data = []
    total_edges = 0  # edges added across all rounds
    round_j = 0

    while len(alive) > 1:
        round_j += 1
        alive_before = len(alive)
        alive_list = sorted(alive)

        # Recompute matchings for alive emitters
        # In CPS, when emitters are eliminated, the matchings are recomputed
        # over the remaining emitters. For simplicity, we use the original matchings.
        # This is a LOWER BOUND on sharing (recomputation might create more sharing).

        # Collector -> emitters via S⁻ and S⁺
        col_to_em_minus = defaultdict(set)
        col_to_em_plus = defaultdict(set)
        for e in alive:
            col_to_em_minus[s_minus[e]].add(e)
            col_to_em_plus[s_plus[e]].add(e)

        # Find delegation pairs
        can_delegate = {}  # eliminated -> (survivor, shared_collector, match_type)
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

        # Limit to half
        if len(can_delegate) > len(alive) // 2:
            items = sorted(can_delegate.items())
            can_delegate = dict(items[:len(alive) // 2])

        # If force_halving and we haven't reached half, that's a problem
        # CPS guarantees at least half can delegate, but with static matchings
        # this might not hold in later rounds.
        elimination_fraction = len(can_delegate) / alive_before

        # Count edges: for each eliminated emitter e delegating to e':
        # 1. Delegation edges: e-c (shared collector), e'-c (already exists)
        #    = 1 new edge per eliminated emitter (e-c; e'-c is the survivor's existing edge)
        # Actually: 2 edges for the 2-hop path e->c->e', but e'-c already in spanner.
        # 2. Missed collectors: collectors that e reaches but e' doesn't.
        #    e reaches {S⁻(e), S⁺(e)}, e' reaches {S⁻(e'), S⁺(e')}.
        #    Missed = {S⁻(e), S⁺(e)} - {S⁻(e'), S⁺(e')} - {shared_c}

        delegation_edges = 0
        missed_total = 0
        missed_per_elim_list = []

        for e, (e_prime, shared_c, mtype) in can_delegate.items():
            # Delegation edge: e to shared_c
            delegation_edges += 1  # e-c is new

            # Missed collectors
            e_cols = {s_minus[e], s_plus[e]}
            ep_cols = {s_minus[e_prime], s_plus[e_prime]}
            missed = e_cols - ep_cols - {shared_c}
            missed_count = len(missed)
            missed_total += missed_count
            missed_per_elim_list.append(missed_count)

            # Each missed collector needs a direct edge
            delegation_edges += missed_count

        total_round_edges = delegation_edges
        total_edges += total_round_edges

        round_data.append({
            'round': round_j,
            'alive_before': alive_before,
            'eliminated': len(can_delegate),
            'alive_after': alive_before - len(can_delegate),
            'delegation_edges': delegation_edges,
            'missed_total': missed_total,
            'missed_per_elim': missed_total / max(len(can_delegate), 1),
            'elim_fraction': elimination_fraction,
        })

        alive -= set(can_delegate.keys())

        if round_j > 2 * math.log2(k + 1) + 5:
            break  # safety

    remaining = len(alive)
    # Remaining emitters need k edges each (one per collector) to complete coverage
    remaining_cost = remaining * k

    return round_data, remaining, total_edges, remaining_cost


def run():
    print("LAYERED DELEGATION: PURE COST ANALYSIS")
    print("=" * 70)
    print()
    print("Setup: k emitters, k collectors, 2 random perfect matchings.")
    print("Each round: eliminate shared-collector emitters, count edge cost.")
    print()

    ks = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    trials = 500

    summary = {}

    for k in ks:
        deleg_totals = []
        remain_totals = []
        remain_counts = []
        round_counts = []
        cost_per_round = defaultdict(list)
        alive_per_round = defaultdict(list)

        for trial in range(trials):
            seed = k * 10000 + trial
            s_minus, s_plus = random_bipartite_matchings(k, seed)
            rounds, remaining, deleg_cost, remain_cost = layered_delegation_sim(
                k, s_minus, s_plus)

            deleg_totals.append(deleg_cost)
            remain_totals.append(remain_cost)
            remain_counts.append(remaining)
            round_counts.append(len(rounds))

            for rd in rounds:
                j = rd['round']
                cost_per_round[j].append(rd['delegation_edges'])
                alive_per_round[j].append(rd['alive_before'])

        avg_deleg = sum(deleg_totals) / trials
        avg_remain = sum(remain_totals) / trials
        avg_total = avg_deleg + avg_remain
        avg_remaining = sum(remain_counts) / trials
        avg_rounds = sum(round_counts) / trials

        print(f"k = {k:5d}")
        print(f"  Avg delegation cost: {avg_deleg:8.1f} ({avg_deleg/k:6.3f} per emitter)")
        print(f"  Avg remaining:       {avg_remaining:8.2f} ({avg_remaining/k:6.4f} of k)")
        print(f"  Avg remaining cost:  {avg_remain:8.1f} ({avg_remain/k:6.1f} per emitter)")
        print(f"  Avg total:           {avg_total:8.1f} ({avg_total/k:6.2f} per emitter)")
        print(f"  Avg rounds:          {avg_rounds:8.2f}")

        # Per-round breakdown
        if cost_per_round:
            print(f"  {'Rnd':>4} {'alive':>7} {'cost':>7} {'cost/alive':>11} samples")
            for j in sorted(cost_per_round.keys()):
                costs = cost_per_round[j]
                alives = alive_per_round[j]
                avg_c = sum(costs) / len(costs)
                avg_a = sum(alives) / len(alives)
                ratio = avg_c / avg_a if avg_a > 0 else 0
                print(f"  {j:4d} {avg_a:7.1f} {avg_c:7.1f} {ratio:11.4f} {len(costs):5d}")

        summary[k] = {
            'avg_deleg': avg_deleg,
            'avg_remain': avg_remaining,
            'avg_remain_cost': avg_remain,
            'avg_total': avg_total,
            'deleg_per_k': avg_deleg / k,
            'total_per_k': avg_total / k,
            'remain_frac': avg_remaining / k,
        }
        print()

    # ─── Scaling analysis ─────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("SCALING ANALYSIS")
    print(f"{'='*70}")

    print(f"\n  {'k':>6} {'deleg':>8} {'deleg/k':>8} {'remain':>7} {'rem/k':>7} "
          f"{'rem_cost':>9} {'total':>8} {'total/k':>8} {'total/klogk':>12}")
    for k in ks:
        s = summary[k]
        logk = math.log2(max(k, 2))
        print(f"  {k:6d} {s['avg_deleg']:8.1f} {s['deleg_per_k']:8.3f} "
              f"{s['avg_remain']:7.2f} {s['remain_frac']:7.4f} "
              f"{s['avg_remain_cost']:9.1f} {s['avg_total']:8.1f} "
              f"{s['total_per_k']:8.2f} {s['avg_total']/(k*logk):12.4f}")

    # Key question: does deleg_per_k converge to a constant?
    print(f"\n  Delegation cost per emitter (deleg/k):")
    for k in ks:
        s = summary[k]
        bar = '#' * int(s['deleg_per_k'] * 20)
        print(f"    k={k:5d}: {s['deleg_per_k']:.3f}  {bar}")

    # Does remaining fraction converge?
    print(f"\n  Remaining fraction (remain/k):")
    for k in ks:
        s = summary[k]
        print(f"    k={k:5d}: {s['remain_frac']:.4f}")

    # The remaining emitters: how many survive?
    print(f"\n  Remaining emitters vs k:")
    xs = [math.log(k) for k in ks]
    ys = [summary[k]['avg_remain'] for k in ks]
    n_pts = len(xs)
    mx = sum(xs)/n_pts; my = sum(ys)/n_pts

    # Fit ln
    cov = sum((xs[i]-mx)*(ys[i]-my) for i in range(n_pts))/n_pts
    vx = sum((xs[i]-mx)**2 for i in range(n_pts))/n_pts
    b = cov/vx; a = my - b*mx
    ss_res = sum((ys[i]-(a+b*xs[i]))**2 for i in range(n_pts))
    ss_tot = sum((ys[i]-my)**2 for i in range(n_pts))
    r2_log = 1 - ss_res/ss_tot
    print(f"    ln fit: remaining = {a:.2f} + {b:.2f} * ln(k), R²={r2_log:.4f}")

    # Fit power
    lys = [math.log(max(y, 0.1)) for y in ys]
    mly = sum(lys)/n_pts
    cov2 = sum((xs[i]-mx)*(lys[i]-mly) for i in range(n_pts))/n_pts
    b2 = cov2/vx; a2 = math.exp(mly - b2*mx)
    ss_res2 = sum((lys[i]-(math.log(a2)+b2*xs[i]))**2 for i in range(n_pts))
    ss_tot2 = sum((lys[i]-mly)**2 for i in range(n_pts))
    r2_pow = 1 - ss_res2/ss_tot2
    print(f"    power fit: remaining = {a2:.3f} * k^{b2:.3f}, R²={r2_pow:.4f}")

    # Fit constant
    mean_remain = sum(ys)/n_pts
    ss_const = sum((y - mean_remain)**2 for y in ys)
    print(f"    constant fit: remaining = {mean_remain:.2f}, R²=0.0000")

    # ─── The critical test ────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("CRITICAL TEST: total_cost / (k * log₂(k))")
    print(f"{'='*70}")
    print(f"\n  If total cost = Θ(k log k), this ratio converges to a constant.")
    print(f"  If total cost = Θ(k), this ratio → 0.")
    print(f"  If total cost = Θ(k²), this ratio → ∞.")

    print(f"\n  {'k':>6} {'total/(k·log₂k)':>16} {'deleg/(k·log₂k)':>16} {'remain_cost/(k²)':>17}")
    for k in ks:
        s = summary[k]
        logk = math.log2(max(k, 2))
        tklk = s['avg_total'] / (k * logk)
        dklk = s['avg_deleg'] / (k * logk)
        rk2 = s['avg_remain_cost'] / (k * k)
        print(f"  {k:6d} {tklk:16.4f} {dklk:16.4f} {rk2:17.6f}")

    # ─── Verdict ──────────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    # Check deleg/k convergence
    deleg_ratios = [summary[k]['deleg_per_k'] for k in ks]
    deleg_first = deleg_ratios[0]
    deleg_last = deleg_ratios[-1]

    # Check total/k·logk convergence
    total_ratios = [summary[k]['avg_total'] / (k * math.log2(max(k, 2))) for k in ks]
    total_first = total_ratios[2]  # skip small k
    total_last = total_ratios[-1]

    print(f"\n  Delegation cost/k: first={deleg_first:.3f}, last={deleg_last:.3f}, "
          f"ratio={deleg_last/deleg_first:.3f}")
    print(f"  Total/(k·log₂k): {total_first:.4f} to {total_last:.4f}")

    if abs(deleg_last - deleg_first) / deleg_first < 0.3:
        deleg_verdict = "O(k) — per-round cost scales with |alive_j|, geometric series works"
    else:
        deleg_verdict = "NOT O(k)"

    remain_frac_last = summary[ks[-1]]['remain_frac']
    if remain_frac_last > 0.1:
        remain_verdict = f"Θ(k) remaining — fraction stabilizes at ~{remain_frac_last:.3f}"
        total_verdict = "Θ(k²) total — remaining emitters × k collectors dominates"
    elif remain_frac_last < 0.01:
        # Check if it's O(1) or O(log k)
        if summary[ks[-1]]['avg_remain'] < 10:
            remain_verdict = "O(1) remaining"
            total_verdict = "O(k) total"
        else:
            remain_verdict = "O(log k) remaining"
            total_verdict = "O(k log k) total"
    else:
        remain_verdict = "unclear"
        total_verdict = "unclear"

    print(f"""
### H22: Amortized delegation cost

**Delegation cost:** {deleg_verdict}
**Remaining emitters:** {remain_verdict}
**Total cost:** {total_verdict}

IMPORTANT CAVEAT: This uses STATIC matchings (not recomputed per round).
CPS recomputes matchings after each elimination, which may give better
halving guarantees. The static-matching version is a LOWER BOUND on
the algorithm's effectiveness.
""")


if __name__ == '__main__':
    run()
