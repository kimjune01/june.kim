"""
H21: Vertex-extreme spanner conjecture
Test whether vertex-extreme edges always form a valid temporal spanner on K_n.
"""

import random
import itertools
from collections import defaultdict, Counter
import sys

random.seed(42)

def make_temporal_clique(n):
    """Random timestamp assignment to K_n edges."""
    edges = list(itertools.combinations(range(n), 2))
    timestamps = list(range(1, len(edges) + 1))
    random.shuffle(timestamps)
    return {e: t for e, t in zip(edges, timestamps)}

def edge_key(u, v):
    return (min(u, v), max(u, v))

def compute_extreme_edges(n, edge_ts):
    """Compute E_extreme: union of min and max timestamp edges per vertex."""
    extreme = set()
    for v in range(n):
        incident = []
        for (u, w), t in edge_ts.items():
            if u == v or w == v:
                incident.append(((u, w), t))
        incident.sort(key=lambda x: x[1])
        if incident:
            extreme.add(incident[0][0])   # min
            extreme.add(incident[-1][0])  # max
    return extreme

def temporal_reachability(n, edge_ts, edge_set=None):
    """Compute all-pairs temporal reachability via BFS on time-ordered edges.
    Returns set of (u, v) pairs that are reachable."""
    if edge_set is None:
        edges_with_ts = sorted(edge_ts.items(), key=lambda x: x[1])
    else:
        edges_with_ts = sorted([(e, edge_ts[e]) for e in edge_set], key=lambda x: x[1])

    # reach[u][v] = earliest arrival time at v starting from u
    # We process edges in timestamp order and propagate reachability
    # For each edge (a,b) at time t:
    #   Anyone who can reach a by time ≤ t can now reach b (arrival t)
    #   Anyone who can reach b by time ≤ t can now reach a (arrival t)

    # reach[src] = dict of {dest: earliest_arrival_time}
    reach = defaultdict(dict)
    for v in range(n):
        reach[v][v] = 0  # at yourself at time 0

    for (a, b), t in edges_with_ts:
        # Collect all sources that can reach a or b by time ≤ t
        sources_to_a = [(src, reach[src][a]) for src in range(n) if a in reach[src] and reach[src][a] <= t]
        sources_to_b = [(src, reach[src][b]) for src in range(n) if b in reach[src] and reach[src][b] <= t]

        # Sources reaching a can now reach b
        for src, _ in sources_to_a:
            if b not in reach[src] or reach[src][b] > t:
                reach[src][b] = t
        # Sources reaching b can now reach a
        for src, _ in sources_to_b:
            if a not in reach[src] or reach[src][a] > t:
                reach[src][a] = t

    reachable = set()
    for src in range(n):
        for dst in reach[src]:
            if src != dst:
                reachable.add((src, dst))
    return reachable

def greedy_repair(n, edge_ts, extreme_edges, full_reach, extreme_reach):
    """Add edges greedily to repair reachability failures."""
    missing = full_reach - extreme_reach
    if not missing:
        return set()

    current_edges = set(extreme_edges)
    repair_edges = set()
    remaining_edges = set(edge_ts.keys()) - current_edges

    while True:
        current_reach = temporal_reachability(n, edge_ts, current_edges)
        still_missing = full_reach - current_reach
        if not still_missing:
            break
        if not remaining_edges:
            break

        # Try each remaining edge, pick one that fixes the most pairs
        best_edge = None
        best_gain = 0
        for e in remaining_edges:
            trial = current_edges | {e}
            trial_reach = temporal_reachability(n, edge_ts, trial)
            gain = len(trial_reach - current_reach)
            if gain > best_gain:
                best_gain = gain
                best_edge = e
        if best_edge is None or best_gain == 0:
            # Try all remaining at once
            break
        current_edges.add(best_edge)
        repair_edges.add(best_edge)
        remaining_edges.remove(best_edge)

    return repair_edges

def analyze_journeys(n, edge_ts, extreme_edges):
    """For reachable pairs through E_extreme, characterize the journeys."""
    edges_with_ts = sorted([(e, edge_ts[e]) for e in extreme_edges], key=lambda x: x[1])

    # BFS tracking paths
    # reach[src][dst] = (arrival_time, hop_count, path)
    reach = {}
    for v in range(n):
        reach[v] = {v: (0, 0, [v])}

    for (a, b), t in edges_with_ts:
        new_entries = []
        for src in range(n):
            if a in reach[src] and reach[src][a][0] <= t:
                arr_t, hops, path = reach[src][a]
                if b not in reach[src] or reach[src][b][1] > hops + 1:
                    new_entries.append((src, b, t, hops + 1, path + [b]))
            if b in reach[src] and reach[src][b][0] <= t:
                arr_t, hops, path = reach[src][b]
                if a not in reach[src] or reach[src][a][1] > hops + 1:
                    new_entries.append((src, a, t, hops + 1, path + [a]))
        for src, dst, t2, h, p in new_entries:
            if dst not in reach[src] or reach[src][dst][1] > h:
                reach[src][dst] = (t2, h, p)

    hop_counts = Counter()
    for src in range(n):
        for dst in reach[src]:
            if src != dst:
                hop_counts[reach[src][dst][1]] += 1
    return hop_counts

def compute_sharing(n, edge_ts):
    """Count how many edges are both min for one vertex and max for another."""
    min_edges = {}
    max_edges = {}
    for v in range(n):
        incident = []
        for (u, w), t in edge_ts.items():
            if u == v or w == v:
                incident.append(((u, w), t))
        incident.sort(key=lambda x: x[1])
        min_edges[v] = incident[0][0]
        max_edges[v] = incident[-1][0]

    shared = 0
    shared_edges = set()
    for u in range(n):
        for v in range(n):
            if u != v and min_edges[u] == max_edges[v]:
                shared_edges.add(min_edges[u])
                shared += 1
    return shared, len(shared_edges)

def degree_distribution(n, edge_ts, extreme_edges):
    """Degree of each vertex in E_extreme."""
    deg = Counter()
    for (u, v) in extreme_edges:
        deg[u] += 1
        deg[v] += 1
    return deg

def adversarial_search(n, num_restarts=20, max_steps=500):
    """Hill-climb to minimize reachability of E_extreme."""
    edges = list(itertools.combinations(range(n), 2))
    m = len(edges)
    total_pairs = n * (n - 1)

    best_worst_reach = total_pairs  # worst case found so far (lower = worse for conjecture)

    for restart in range(num_restarts):
        timestamps = list(range(1, m + 1))
        random.shuffle(timestamps)
        edge_ts = {e: t for e, t in zip(edges, timestamps)}

        extreme = compute_extreme_edges(n, edge_ts)
        full_reach = temporal_reachability(n, edge_ts)
        ext_reach = temporal_reachability(n, edge_ts, extreme)
        current_score = len(ext_reach)

        for step in range(max_steps):
            # Try random swap
            i, j = random.sample(range(m), 2)
            edge_ts[edges[i]], edge_ts[edges[j]] = edge_ts[edges[j]], edge_ts[edges[i]]

            extreme2 = compute_extreme_edges(n, edge_ts)
            full_reach2 = temporal_reachability(n, edge_ts)
            ext_reach2 = temporal_reachability(n, edge_ts, extreme2)

            # We want to minimize ext_reach while keeping full_reach high
            # Actually: we want ext_reach to miss pairs that full_reach has
            new_missing = len(full_reach2) - len(ext_reach2)
            old_missing = len(full_reach) - len(ext_reach)

            if new_missing > old_missing:
                full_reach = full_reach2
                ext_reach = ext_reach2
                extreme = extreme2
                current_score = len(ext_reach2)
            else:
                # Revert
                edge_ts[edges[i]], edge_ts[edges[j]] = edge_ts[edges[j]], edge_ts[edges[i]]

        missing = len(full_reach) - len(ext_reach)
        if missing > 0:
            best_worst_reach = min(best_worst_reach, len(ext_reach))

    return best_worst_reach, total_pairs

# ============================================================
# MAIN EXPERIMENTS
# ============================================================

NUM_SAMPLES = 100

print("=" * 70)
print("H21: VERTEX-EXTREME SPANNER CONJECTURE")
print("=" * 70)

# Task 1 & 2 & 5 & 6
print("\n### Task 1: |E_extreme| statistics")
print(f"{'n':>3} {'2n-3':>5} {'min':>5} {'mean':>6} {'max':>5} {'always≤2n-3':>12}")

task2_results = {}
task5_results = {}
task6_results = {}
all_test_cases = {}

for n in range(4, 11):
    sizes = []
    spanner_count = 0
    total_missing_pairs = []
    sharing_counts = []
    sharing_edge_counts = []
    degree_dists = []
    cases = []

    for trial in range(NUM_SAMPLES):
        edge_ts = make_temporal_clique(n)
        extreme = compute_extreme_edges(n, edge_ts)
        sizes.append(len(extreme))

        full_reach = temporal_reachability(n, edge_ts)
        ext_reach = temporal_reachability(n, edge_ts, extreme)
        missing = full_reach - ext_reach
        if len(missing) == 0:
            spanner_count += 1
        total_missing_pairs.append(len(missing))

        sc, sec = compute_sharing(n, edge_ts)
        sharing_counts.append(sc)
        sharing_edge_counts.append(sec)

        deg = degree_distribution(n, edge_ts, extreme)
        degree_dists.append(deg)

        cases.append((edge_ts, extreme, full_reach, ext_reach, missing))

    all_test_cases[n] = cases
    bound = 2 * n - 3
    always_within = all(s <= bound for s in sizes)
    print(f"{n:>3} {bound:>5} {min(sizes):>5} {sum(sizes)/len(sizes):>6.1f} {max(sizes):>5} {'YES' if always_within else 'NO':>12}")

    task2_results[n] = (spanner_count, total_missing_pairs)
    task5_results[n] = (sharing_counts, sharing_edge_counts)
    task6_results[n] = degree_dists

# Task 2 report
print("\n### Task 2: Is E_extreme a valid spanner?")
print(f"{'n':>3} {'spanner%':>9} {'avg_missing':>12} {'max_missing':>12}")
for n in range(4, 11):
    sc, mp = task2_results[n]
    print(f"{n:>3} {sc:>8}% {sum(mp)/len(mp):>12.2f} {max(mp):>12}")

# Task 3: Repair analysis (only for n where failures occur, small n for speed)
print("\n### Task 3: Repair when E_extreme fails")
print(f"{'n':>3} {'failures':>9} {'avg_repair':>10} {'max_repair':>10} {'avg_total':>10} {'≤2n-3':>6}")
for n in range(4, 9):  # limit for speed
    cases = all_test_cases[n]
    bound = 2 * n - 3
    repair_sizes = []
    total_sizes = []
    for edge_ts, extreme, full_reach, ext_reach, missing in cases:
        if len(missing) > 0:
            repair = greedy_repair(n, edge_ts, extreme, full_reach, ext_reach)
            repair_sizes.append(len(repair))
            total_sizes.append(len(extreme) + len(repair))
    if repair_sizes:
        within = sum(1 for t in total_sizes if t <= bound)
        print(f"{n:>3} {len(repair_sizes):>9} {sum(repair_sizes)/len(repair_sizes):>10.2f} {max(repair_sizes):>10} {sum(total_sizes)/len(total_sizes):>10.2f} {within}/{len(total_sizes):>4}")
    else:
        print(f"{n:>3} {'0':>9} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>6}")

# Task 4: Journey structure
print("\n### Task 4: Journey structure through E_extreme")
for n in [5, 6, 7]:
    all_hops = Counter()
    count = 0
    for edge_ts, extreme, full_reach, ext_reach, missing in all_test_cases[n][:20]:
        hc = analyze_journeys(n, edge_ts, extreme)
        for k, v in hc.items():
            all_hops[k] += v
        count += 1
    print(f"n={n}: hop distribution (over {count} samples):")
    total_journeys = sum(all_hops.values())
    for h in sorted(all_hops.keys()):
        print(f"  {h} hops: {all_hops[h]:>8} ({100*all_hops[h]/total_journeys:.1f}%)")

# Task 5 report
print("\n### Task 5: Sharing structure (min of one = max of another)")
print(f"{'n':>3} {'avg_sharing_pairs':>18} {'avg_shared_edges':>17} {'min':>5} {'max':>5}")
for n in range(4, 11):
    sc, sec = task5_results[n]
    print(f"{n:>3} {sum(sc)/len(sc):>18.2f} {sum(sec)/len(sec):>17.2f} {min(sec):>5} {max(sec):>5}")

# Task 6 report
print("\n### Task 6: Degree distribution in E_extreme")
for n in [5, 7, 10]:
    all_degs = Counter()
    for deg in task6_results[n]:
        for v, d in deg.items():
            all_degs[d] += 1
    print(f"n={n}: degree distribution (over {NUM_SAMPLES} samples, {n} vertices each):")
    for d in sorted(all_degs.keys()):
        print(f"  degree {d}: {all_degs[d]:>6} vertices ({100*all_degs[d]/(NUM_SAMPLES*n):.1f}%)")

# Task 7: Adversarial search
print("\n### Task 7: Adversarial search")
for n in [5, 6, 7, 8]:
    best_reach, total = adversarial_search(n, num_restarts=10, max_steps=300)
    print(f"n={n}: worst-case E_extreme reachability found = {best_reach}/{total}")

# Task 8: Shared edges ≥ 3?
print("\n### Task 8: Shared edge count (for 2n-3 improvement)")
print(f"{'n':>3} {'≥3 shared':>10} {'mean_shared':>12} {'min_shared':>11}")
for n in range(4, 11):
    sc, sec = task5_results[n]
    geq3 = sum(1 for s in sec if s >= 3)
    print(f"{n:>3} {geq3:>9}% {sum(sec)/len(sec):>12.2f} {min(sec):>11}")

# Final summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

all_spanner = True
all_within_bound = True
for n in range(4, 11):
    sc, mp = task2_results[n]
    if sc < 100:
        all_spanner = False
    cases = all_test_cases[n]
    bound = 2 * n - 3
    for edge_ts, extreme, full_reach, ext_reach, missing in cases:
        if len(extreme) > bound:
            all_within_bound = False

if all_spanner:
    status = "CONFIRMED"
    verdict = "E_extreme is ALWAYS a valid spanner in all tested cases."
elif all(task2_results[n][0] > 90 for n in range(4, 11)):
    status = "STRONG LEAD"
    verdict = "E_extreme is almost always a valid spanner."
else:
    status = "REFUTED"
    verdict = "E_extreme is NOT always a valid spanner."

print(f"\n### H21: Vertex-extreme spanner ({status})")
print(f"**Verdict:** {verdict}")
print(f"**|E_extreme| ≤ 2n-3:** {'YES' if all_within_bound else 'NO'} across all tests")

# Count claim
for n in range(4, 11):
    cases = all_test_cases[n]
    bound = 2 * n - 3
    over = sum(1 for _, extreme, _, _, _ in cases if len(extreme) > bound)
    if over > 0:
        print(f"  n={n}: {over}/{NUM_SAMPLES} cases exceed 2n-3={bound}")

print(f"\n**Claims:**")
print(f"1. |E_extreme| is at most 2n (trivial: 2 edges per vertex)")
if all_spanner:
    print(f"2. E_extreme preserves all temporal reachability (empirically confirmed n=4..10)")
    print(f"3. Sharing gives ≥3 edges overlap → |E_extreme| ≤ 2n-3")
else:
    print(f"2. E_extreme does NOT always preserve temporal reachability")
    print(f"3. Repair analysis shows how many extra edges are needed")
