#!/usr/bin/env python3
"""
H6 deep analysis:
- SM(k) adds all edges because SM rows are monotonically structured
- Focus on random matrices where greedy actually prunes
- Examine whether the FULL complete temporal graph achieves full reachability
- Check if spanner = full reachability subset
"""
import random
from collections import defaultdict

random.seed(42)

def sm_matrix(k):
    M = [[0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            M[i][j] = i*k + ((i+j) % k) + 1
    return M

def random_distinct_matrix(k):
    vals = list(range(1, k*k + 1))
    random.shuffle(vals)
    M = [[0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            M[i][j] = vals[i*k + j]
    return M

def compute_reachable_pairs(spanner_edges, k):
    n = 2 * k
    sorted_edges = sorted(spanner_edges, key=lambda e: e[0])
    time_groups = defaultdict(list)
    for (t, ai, bj) in sorted_edges:
        time_groups[t].append((ai, k + bj))
    times = sorted(time_groups.keys())
    reachable = set()
    for src in range(n):
        active = {src}
        for t in times:
            changed = True
            while changed:
                changed = False
                for (u, v) in time_groups[t]:
                    if u in active and v not in active:
                        active.add(v)
                        changed = True
                    if v in active and u not in active:
                        active.add(u)
                        changed = True
        for dst in active:
            if dst != src:
                reachable.add((src, dst))
    return reachable

def online_construction(M, k, order='forward'):
    edges = []
    for i in range(k):
        for j in range(k):
            edges.append((M[i][j], i, j))
    if order == 'forward':
        edges.sort(key=lambda e: e[0])
    elif order == 'reverse':
        edges.sort(key=lambda e: -e[0])
    elif order == 'random':
        random.shuffle(edges)

    spanner = []
    current_reachable = set()
    history = []

    for rank, (t, ai, bj) in enumerate(edges):
        candidate = spanner + [(t, ai, bj)]
        new_reachable = compute_reachable_pairs(candidate, k)
        new_pairs = new_reachable - current_reachable
        if len(new_pairs) > 0:
            spanner.append((t, ai, bj))
            current_reachable = new_reachable
            history.append({
                'rank': rank, 'time': t, 'ai': ai, 'bj': bj,
                'new_pairs': len(new_pairs), 'cum_edges': len(spanner),
                'total_reachable': len(current_reachable),
            })
    return spanner, history, current_reachable

# ── Check: does SM achieve full reachability with all edges? ──
print("=" * 70)
print("SM(k): Full reachability check")
print("=" * 70)
for k in [3, 4, 5]:
    n = 2*k
    M = sm_matrix(k)
    all_edges = [(M[i][j], i, j) for i in range(k) for j in range(k)]
    r = compute_reachable_pairs(all_edges, k)
    total = n*(n-1)
    print(f"k={k}: {len(r)}/{total} pairs reachable with ALL edges. Missing={total-len(r)}")

    # What's missing?
    missing = []
    for u in range(n):
        for v in range(n):
            if u != v and (u,v) not in r:
                u_l = f"a{u}" if u < k else f"b{u-k}"
                v_l = f"a{v}" if v < k else f"b{v-k}"
                missing.append(f"{u_l}->{v_l}")
    if missing:
        print(f"  Missing: {missing}")

# SM has the property that row i has timestamps in block [ik+1, (i+1)k].
# a_i's edges are ALL earlier than a_{i+1}'s edges. So a_{i+1} can NEVER
# reach a_i via any path, because all edges from a_{i+1} happen AFTER
# all edges from a_i. This makes backward A->A reachability impossible.
# That's k*(k-1)/2 missing pairs.

print("\n" + "=" * 70)
print("Random matrices: Full reachability check")
print("=" * 70)
for k in [3, 4, 5, 6]:
    n = 2*k
    full_reach_counts = []
    for _ in range(20):
        M = random_distinct_matrix(k)
        all_edges = [(M[i][j], i, j) for i in range(k) for j in range(k)]
        r = compute_reachable_pairs(all_edges, k)
        full_reach_counts.append(len(r))
    total = n*(n-1)
    mean_r = sum(full_reach_counts)/len(full_reach_counts)
    print(f"k={k}: mean full reachability = {mean_r:.1f}/{total}, min={min(full_reach_counts)}, max={max(full_reach_counts)}")

# ── Main analysis: random matrices, focus on actual pruning ──
print("\n" + "=" * 70)
print("Random matrices: Online greedy analysis (50 trials)")
print("=" * 70)

for k in [4, 5, 6, 7]:
    n = 2*k
    offline_opt = 4*k - 4
    conj = 2*n - 3

    fwd_counts = []
    rev_counts = []
    rnd_counts = []
    full_reach_vs_spanner = []
    first_half_fracs = []
    last_edge_ranks = []

    for trial in range(50):
        M = random_distinct_matrix(k)

        # Full reachability
        all_edges = [(M[i][j], i, j) for i in range(k) for j in range(k)]
        full_r = compute_reachable_pairs(all_edges, k)

        # Forward
        sp_f, hist_f, reach_f = online_construction(M, k, 'forward')
        fwd_counts.append(len(sp_f))
        full_reach_vs_spanner.append((len(full_r), len(reach_f)))

        half = k*k // 2
        fh = sum(1 for h in hist_f if h['rank'] < half)
        first_half_fracs.append(fh / len(sp_f) if sp_f else 0)

        if hist_f:
            last_edge_ranks.append(hist_f[-1]['rank'] / (k*k - 1))

        # Reverse
        sp_r, hist_r, _ = online_construction(M, k, 'reverse')
        rev_counts.append(len(sp_r))

        # Random (3 trials per matrix)
        for _ in range(3):
            sp_rnd, hist_rnd, _ = online_construction(M, k, 'random')
            rnd_counts.append(len(sp_rnd))

    mean_f = sum(fwd_counts)/len(fwd_counts)
    mean_r = sum(rev_counts)/len(rev_counts)
    mean_rnd = sum(rnd_counts)/len(rnd_counts)

    # Check: does greedy spanner achieve same reachability as full graph?
    same_reach = sum(1 for fr, sr in full_reach_vs_spanner if fr == sr)

    print(f"\nk={k} (n={n}), offline_opt={offline_opt}, conj_bound={conj}:")
    print(f"  Forward:  mean={mean_f:.1f}, min={min(fwd_counts)}, max={max(fwd_counts)}, std={((sum((x-mean_f)**2 for x in fwd_counts)/len(fwd_counts))**0.5):.1f}")
    print(f"  Reverse:  mean={mean_r:.1f}, min={min(rev_counts)}, max={max(rev_counts)}")
    print(f"  Random:   mean={mean_rnd:.1f}, min={min(rnd_counts)}, max={max(rnd_counts)}")
    print(f"  Spanner achieves full reachability: {same_reach}/50")
    print(f"  First-half fraction: mean={sum(first_half_fracs)/len(first_half_fracs):.2f}")
    print(f"  Last edge rank (fraction of total): mean={sum(last_edge_ranks)/len(last_edge_ranks):.2f}")
    print(f"  Forward exceeds 2n-3: {sum(1 for x in fwd_counts if x > conj)}/50")
    print(f"  Reverse exceeds 2n-3: {sum(1 for x in rev_counts if x > conj)}/50")
    print(f"  Random exceeds 2n-3: {sum(1 for x in rnd_counts if x > conj)}/{len(rnd_counts)}")

    # Gap characterization
    gaps_f = [x - offline_opt for x in fwd_counts]
    mean_gap = sum(gaps_f)/len(gaps_f)
    # Is gap O(1), O(log k), or O(k)?
    import math
    print(f"  Mean gap over offline: {mean_gap:.1f} (vs log(k)={math.log2(k):.1f}, k={k})")

# ── Phase transition analysis ──
print("\n" + "=" * 70)
print("Phase transition: cumulative edges over time (k=5, single example)")
print("=" * 70)

k = 5
M = random_distinct_matrix(k)
sp, hist, _ = online_construction(M, k, 'forward')
print(f"Total edges in spanner: {len(sp)}/{k*k}")
print(f"Timestamp | Cum. Edges | New Pairs | Total Reachable")
for h in hist:
    bar = '#' * h['cum_edges']
    print(f"  t={h['time']:>3} (rank {h['rank']:>2}) | {h['cum_edges']:>3} | +{h['new_pairs']:>2} pairs | {h['total_reachable']:>3} | {bar}")

# Check if there's a plateau
if hist:
    last_big_jump = max((i for i, h in enumerate(hist) if h['new_pairs'] > 2), default=len(hist)-1)
    print(f"\nLast edge adding >2 pairs: entry {last_big_jump} (rank {hist[last_big_jump]['rank']})")
    print(f"Edges after that point: {len(hist) - last_big_jump - 1}")

# ── Gap scaling ──
print("\n" + "=" * 70)
print("Gap scaling analysis")
print("=" * 70)

import math
print(f"{'k':>3} {'n':>4} {'mean_fwd':>9} {'4k-4':>5} {'2n-3':>5} {'mean_gap':>9} {'gap/k':>7} {'gap/logk':>9} {'gap/k^2':>8}")

for k in [4, 5, 6, 7]:
    n = 2*k
    counts = []
    for _ in range(50):
        M = random_distinct_matrix(k)
        sp, _, _ = online_construction(M, k, 'forward')
        counts.append(len(sp))
    mean_c = sum(counts)/len(counts)
    gap = mean_c - (4*k-4)
    print(f"{k:>3} {n:>4} {mean_c:>9.1f} {4*k-4:>5} {2*n-3:>5} {gap:>9.1f} {gap/k:>7.2f} {gap/math.log2(k):>9.2f} {gap/k**2:>8.3f}")
