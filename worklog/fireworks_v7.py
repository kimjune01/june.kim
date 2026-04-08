"""
Fireworks v7: Correct delegation with combined collector maps.

Fix from v6: Two perfect matchings S⁻ and S⁺ each have 1 emitter per collector.
Sharing happens BETWEEN matchings: s_minus[i] = s_plus[j] means emitters i and j
share a collector. Must combine both matchings into one collector->emitters map.
"""

import random
import math
from collections import defaultdict


def random_bipartite_matchings(k, seed=None):
    """Two random perfect matchings between k emitters and k collectors."""
    rng = random.Random(seed)
    perm1 = list(range(k)); rng.shuffle(perm1)
    perm2 = list(range(k)); rng.shuffle(perm2)
    return perm1, perm2


def layered_delegation(k, s_minus, s_plus):
    """
    Simulate layered delegation with correct combined collector maps.

    Each emitter e reaches collectors s_minus[e] and s_plus[e].
    Two emitters share a collector if any of their 4 collector values coincide.

    Returns: (round_data, remaining_count, total_delegation_edges)
    """
    alive = set(range(k))
    round_data = []
    total_deleg_edges = 0
    round_j = 0

    while len(alive) > 1:
        round_j += 1
        alive_before = len(alive)

        # Combined collector -> emitter map (both matchings)
        col_to_em = defaultdict(set)
        for e in alive:
            col_to_em[s_minus[e]].add(e)
            col_to_em[s_plus[e]].add(e)

        # Find delegation pairs: emitters sharing a collector
        can_delegate = {}  # eliminated -> (survivor, shared_collector)
        for c in sorted(col_to_em.keys(), key=lambda c: -len(col_to_em[c])):
            es = col_to_em[c]
            available = sorted(es - set(can_delegate.keys()))
            if len(available) >= 2:
                survivor = available[0]
                for e in available[1:]:
                    if e not in can_delegate:
                        can_delegate[e] = (survivor, c)

        if not can_delegate:
            break

        # CPS guarantees at most half eliminated per round
        if len(can_delegate) > len(alive) // 2:
            items = sorted(can_delegate.items())
            can_delegate = dict(items[:len(alive) // 2])

        # Count edges
        round_deleg = 0
        round_missed = 0
        missed_per_elim_vals = []

        for e, (e_prime, shared_c) in can_delegate.items():
            # 1 delegation edge: e -> shared_c (e_prime -> shared_c already covered)
            round_deleg += 1

            # Missed collectors: e's collectors not covered by e_prime
            e_cols = {s_minus[e], s_plus[e]}
            ep_cols = {s_minus[e_prime], s_plus[e_prime]}
            missed = e_cols - ep_cols - {shared_c}
            missed_count = len(missed)
            round_missed += missed_count
            missed_per_elim_vals.append(missed_count)

            # Each missed collector needs a direct edge
            round_deleg += missed_count

        total_deleg_edges += round_deleg
        eliminated = set(can_delegate.keys())
        alive -= eliminated

        round_data.append({
            'round': round_j,
            'alive_before': alive_before,
            'eliminated': len(eliminated),
            'alive_after': len(alive),
            'elim_fraction': len(eliminated) / alive_before,
            'delegation_edges': round_deleg,
            'missed_total': round_missed,
            'missed_per_elim': round_missed / max(len(eliminated), 1),
        })

        if round_j > 2 * math.log2(k + 2) + 10:
            break

    return round_data, len(alive), total_deleg_edges


def run():
    print("LAYERED DELEGATION: CORRECT COMBINED COLLECTOR MAPS")
    print("=" * 70)

    ks = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    trials = 500

    summary = {}

    for k in ks:
        deleg_totals = []
        remain_counts = []
        round_counts = []
        cost_per_round = defaultdict(list)
        alive_per_round = defaultdict(list)
        missed_per_round = defaultdict(list)

        for trial in range(trials):
            seed = k * 10000 + trial
            s_minus, s_plus = random_bipartite_matchings(k, seed)
            rounds, remaining, deleg_cost = layered_delegation(k, s_minus, s_plus)

            deleg_totals.append(deleg_cost)
            remain_counts.append(remaining)
            round_counts.append(len(rounds))

            for rd in rounds:
                j = rd['round']
                cost_per_round[j].append(rd['delegation_edges'])
                alive_per_round[j].append(rd['alive_before'])
                missed_per_round[j].append(rd['missed_per_elim'])

        avg_deleg = sum(deleg_totals) / trials
        avg_remaining = sum(remain_counts) / trials
        avg_rounds = sum(round_counts) / trials

        print(f"\nk = {k:5d}")
        print(f"  Delegation cost:  {avg_deleg:8.1f} (per emitter: {avg_deleg/k:.3f})")
        print(f"  Remaining:        {avg_remaining:8.2f} (fraction: {avg_remaining/k:.4f})")
        print(f"  Rounds:           {avg_rounds:8.2f}")

        if cost_per_round:
            print(f"  {'Rnd':>4} {'alive':>7} {'cost':>7} {'cost/alive':>11} "
                  f"{'miss/elim':>10} samples")
            for j in sorted(cost_per_round.keys()):
                costs = cost_per_round[j]
                alives = alive_per_round[j]
                misses = missed_per_round[j]
                avg_c = sum(costs) / len(costs)
                avg_a = sum(alives) / len(alives)
                avg_m = sum(misses) / len(misses)
                ratio = avg_c / avg_a if avg_a > 0 else 0
                print(f"  {j:4d} {avg_a:7.1f} {avg_c:7.1f} {ratio:11.4f} "
                      f"{avg_m:10.3f} {len(costs):5d}")

        summary[k] = {
            'avg_deleg': avg_deleg,
            'deleg_per_k': avg_deleg / k,
            'avg_remain': avg_remaining,
            'remain_frac': avg_remaining / k,
            'avg_rounds': avg_rounds,
        }

    # ─── Scaling ──────────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("SCALING ANALYSIS")
    print(f"{'='*70}")

    print(f"\n  {'k':>6} {'deleg':>8} {'d/k':>7} {'d/(k·lgk)':>10} "
          f"{'remain':>8} {'r/k':>7} {'rounds':>7}")
    for k in ks:
        s = summary[k]
        lgk = math.log2(max(k, 2))
        print(f"  {k:6d} {s['avg_deleg']:8.1f} {s['deleg_per_k']:7.3f} "
              f"{s['avg_deleg']/(k*lgk):10.4f} "
              f"{s['avg_remain']:8.2f} {s['remain_frac']:7.4f} "
              f"{s['avg_rounds']:7.2f}")

    # Fit delegation cost
    xs = [math.log(k) for k in ks]
    ys_d = [summary[k]['avg_deleg'] for k in ks]
    ys_r = [summary[k]['avg_remain'] for k in ks]
    n_pts = len(xs)

    # Power law fit for delegation
    lyd = [math.log(max(y, 0.01)) for y in ys_d]
    mx = sum(xs)/n_pts
    myd = sum(lyd)/n_pts
    cov = sum((xs[i]-mx)*(lyd[i]-myd) for i in range(n_pts))/n_pts
    vx = sum((xs[i]-mx)**2 for i in range(n_pts))/n_pts
    b = cov/vx; a = math.exp(myd - b*mx)
    print(f"\n  Delegation cost: {a:.3f} * k^{b:.3f}")

    # Power law fit for remaining
    lyr = [math.log(max(y, 0.01)) for y in ys_r]
    myr = sum(lyr)/n_pts
    cov_r = sum((xs[i]-mx)*(lyr[i]-myr) for i in range(n_pts))/n_pts
    b_r = cov_r/vx; a_r = math.exp(myr - b_r*mx)
    print(f"  Remaining: {a_r:.3f} * k^{b_r:.3f}")

    # ─── The key test ─────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("THE KEY TEST")
    print(f"{'='*70}")

    # Does deleg/k converge to a constant?
    deleg_ratios = [summary[k]['deleg_per_k'] for k in ks]
    print(f"\n  deleg/k: {[f'{r:.3f}' for r in deleg_ratios]}")

    # Does deleg/(k·logk) converge?
    deleg_log_ratios = [summary[k]['avg_deleg'] / (k * math.log2(max(k, 2)))
                        for k in ks]
    print(f"  deleg/(k·lg k): {[f'{r:.4f}' for r in deleg_log_ratios]}")

    # Is deleg_per_k constant (O(k) total) or growing (O(k log k))?
    growth = deleg_ratios[-1] / deleg_ratios[2] if deleg_ratios[2] > 0 else 0
    lg_growth = math.log2(ks[-1]) / math.log2(ks[2])

    print(f"\n  deleg/k growth (k={ks[2]} to {ks[-1]}): {growth:.3f}x")
    print(f"  log₂(k) growth: {lg_growth:.2f}x")
    print(f"  If O(k): growth ~ 1x")
    print(f"  If O(k·log k): growth ~ {lg_growth:.1f}x")

    # ─── Remaining emitters ───────────────────────────────────────────────
    print(f"\n  Remaining emitters scaling:")
    for k in ks:
        s = summary[k]
        print(f"    k={k:5d}: remaining={s['avg_remain']:.2f}, "
              f"fraction={s['remain_frac']:.4f}")

    # ─── Verdict ──────────────────────────────────────────────────────────
    print(f"\n\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    if growth < 1.3:
        deleg_status = "O(k)"
        deleg_desc = "Delegation cost is O(k). Geometric series works."
    elif growth < 2.0:
        deleg_status = "O(k log k)"
        deleg_desc = "Delegation cost is O(k log k)."
    else:
        deleg_status = f"O(k^{b:.2f})"
        deleg_desc = f"Delegation cost grows as k^{b:.2f}."

    remain_last = summary[ks[-1]]['remain_frac']
    if remain_last > 0.1:
        remain_status = "Θ(k)"
        remain_desc = f"~{remain_last*100:.0f}% of emitters survive. Remaining cost = Θ(k²)."
    elif remain_last < 0.001:
        remain_status = "O(1)"
        remain_desc = "Almost all emitters eliminated. Remaining cost = O(k)."
    else:
        remain_status = "o(k), ω(1)"
        remain_desc = f"Remaining fraction = {remain_last:.4f}, declining but not zero."

    print(f"""
### H22: Amortized delegation cost

**Per-round delegation cost:** {deleg_status}
  {deleg_desc}

**Remaining emitters:** {remain_status}
  {remain_desc}

**Total cost (delegation only):** {deleg_status}
**Total cost (with remaining):** depends on remaining × k

**Per-round cost scales with:** {'|alive_j|' if growth < 1.5 else 'unclear'}
""")


if __name__ == '__main__':
    run()
