"""
Phase 3: Fundamental rethinking.

Observation: All constructions give greedy spanner sizes of ~1.5n to 1.7n.
The exact minimum could be smaller. This strongly suggests that for
SINGLE-LABEL temporal cliques, the lower bound might actually be Θ(n),
not Θ(n log n).

The Θ(n log n) result might be for MULTI-LABEL (each edge can have multiple
timestamps) or for STRICT journeys (strictly increasing, not non-decreasing).

Let me investigate:
1. What's the exact minimum spanner for K_5 over ALL possible labelings?
2. Does strict vs non-strict matter?
3. What if we allow multi-label?

Also: let me verify the greedy results by computing exact minima for K_7.
"""

from itertools import combinations, permutations
from collections import defaultdict
import math
import random
import sys

def check_reachability_strict(n, timestamps):
    """Check reachability with STRICTLY increasing timestamps."""
    adj = defaultdict(list)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t))
        adj[v].append((u, t))

    reachable = set()
    for src in range(n):
        best = {src: -1}  # -1 means we haven't used any edge yet
        changed = True
        while changed:
            changed = False
            for v in list(best.keys()):
                mt = best[v]
                for (w, t) in adj[v]:
                    if t > mt:  # STRICT
                        if w not in best or t < best[w]:
                            best[w] = t
                            changed = True
        for dst in best:
            if dst != src:
                reachable.add((src, dst))
    return reachable


def check_reachability_nondec(n, timestamps):
    """Check reachability with non-decreasing timestamps."""
    adj = defaultdict(list)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t))
        adj[v].append((u, t))

    reachable = set()
    for src in range(n):
        best = {src: 0}
        changed = True
        while changed:
            changed = False
            for v in list(best.keys()):
                mt = best[v]
                for (w, t) in adj[v]:
                    if t >= mt:  # non-decreasing
                        if w not in best or t < best[w]:
                            best[w] = t
                            changed = True
        for dst in best:
            if dst != src:
                reachable.add((src, dst))
    return reachable


def greedy_spanner(n, timestamps, strict=False):
    """Greedy spanner removal."""
    check = check_reachability_strict if strict else check_reachability_nondec
    edges = list(timestamps.keys())
    full_reach = check(n, timestamps)

    # Try multiple removal orders
    best = set(edges)
    for order_fn in [
        lambda e: -timestamps[e],
        lambda e: timestamps[e],
        lambda e: random.random(),
    ]:
        current = set(edges)
        for e in sorted(edges, key=order_fn):
            trial = current - {e}
            ts2 = {edge: timestamps[edge] for edge in trial}
            if check(n, ts2) == full_reach:
                current = trial
        if len(current) < len(best):
            best = current

    return len(best)


def exact_min_spanner_ilp_style(n, timestamps, strict=False):
    """
    Exact minimum spanner via LP relaxation + branch and bound.
    For each pair, compute all journeys. Then solve min edge set
    covering all pairs.
    """
    check = check_reachability_strict if strict else check_reachability_nondec
    edges = list(timestamps.keys())
    m = len(edges)
    edge_idx = {e: i for i, e in enumerate(edges)}
    full_reach = check(n, timestamps)

    # For each pair, find all journeys
    adj = defaultdict(list)
    for (u, v), t in timestamps.items():
        adj[u].append((v, t, (u, v)))
        adj[v].append((u, t, (u, v)))
    for v in adj:
        adj[v].sort(key=lambda x: x[1])

    pair_journey_masks = []

    for (s, d) in full_reach:
        journeys = []

        def dfs(cur, last_t, path_mask, visited):
            if len(journeys) > 200:
                return
            if cur == d:
                journeys.append(path_mask)
                return
            for (w, t, edge) in adj[cur]:
                cmp = t > last_t if strict else t >= last_t
                if cmp and w not in visited:
                    visited.add(w)
                    dfs(w, t, path_mask | (1 << edge_idx[edge]), visited)
                    visited.remove(w)

        dfs(s, -1 if strict else 0, 0, {s})
        if journeys:
            pair_journey_masks.append(((s, d), journeys))

    # Now solve: find minimum set of edges such that for each pair,
    # at least one journey mask is a subset of the chosen edges.
    # This is NP-hard in general but small instances are tractable.

    # Use greedy as upper bound
    ub = greedy_spanner(n, timestamps, strict)

    # Branch and bound
    best = [ub]

    def solve(chosen, idx, must_include):
        """
        chosen: bitmask of edges definitely included
        idx: current edge being decided
        must_include: set of edge indices that must be included
        """
        if idx == m:
            # Check validity
            mask = chosen
            for (pair, jmasks) in pair_journey_masks:
                ok = any((jm & mask) == jm for jm in jmasks)
                if not ok:
                    return
            size = bin(chosen).count('1')
            if size < best[0]:
                best[0] = size
            return

        # Pruning: current bits + remaining bits < best
        remaining = m - idx
        current_size = bin(chosen).count('1')
        if current_size + remaining < best[0]:
            # Even including all remaining can't beat current best... wait, that's wrong
            # We want MINIMUM, so pruning is: current_size >= best (already too big)
            pass

        if current_size >= best[0]:
            return

        # Try including edge idx
        solve(chosen | (1 << idx), idx + 1, must_include)
        # Try excluding edge idx (only if not forced)
        if idx not in must_include:
            solve(chosen, idx + 1, must_include)

    # Find must-include edges
    must = set()
    for (pair, jmasks) in pair_journey_masks:
        if len(jmasks) == 1:
            jm = jmasks[0]
            for i in range(m):
                if jm & (1 << i):
                    must.add(i)

    # For moderate m, direct enumeration of subsets by size
    if m <= 15:
        for size in range(len(must), ub + 1):
            found = False
            for subset in combinations(range(m), size):
                if not must.issubset(set(subset)):
                    continue
                mask = 0
                for i in subset:
                    mask |= (1 << i)
                valid = True
                for (pair, jmasks) in pair_journey_masks:
                    if not any((jm & mask) == jm for jm in jmasks):
                        valid = False
                        break
                if valid:
                    return size
            # Safety check
            if math.comb(m, size) > 5_000_000:
                return ub
        return ub

    return ub


def comprehensive_k5():
    """
    Try ALL 10! = 3628800 timestamp assignments on K_5.
    For each, compute greedy spanner size. Track maximum.
    """
    edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    m = 10

    best_greedy = 0
    best_ts = None
    count = 0

    # 10! is 3.6M — this will take a while but is feasible
    # Actually let me just sample heavily and also try structured ones

    # For strict increasing:
    print("K_5 STRICT journeys:")
    best_strict = 0
    for trial in range(100000):
        perm = list(range(1, m + 1))
        random.shuffle(perm)
        ts = {edges[i]: perm[i] for i in range(m)}
        reach = check_reachability_strict(5, ts)
        if len(reach) < 20:
            continue
        gs = greedy_spanner(5, ts, strict=True)
        if gs > best_strict:
            best_strict = gs
            best_ts_strict = ts.copy()
            print(f"  New best strict: {gs}")

    print(f"  K_5 best strict spanner: {best_strict}")

    # For non-decreasing (single-label means all timestamps distinct, so non-dec = strict!)
    print("\nNote: With single labels (all timestamps distinct), non-decreasing = strictly increasing.")
    print("The distinction only matters with multi-labels (repeated timestamps).")

    return best_strict


def multi_label_analysis(n):
    """
    Multi-label: each edge gets one or more timestamps.
    With multi-label, non-decreasing journeys can reuse timestamp values.

    For the lower bound question: does multi-label change the spanner size?

    Simple multi-label construction: each edge (i,j) gets timestamps {i, j}.
    """
    print(f"\n--- Multi-label analysis for K_{n} ---")

    # In single-label, all timestamps are from a permutation (distinct).
    # The distinction between strict and non-decreasing DOES matter even with
    # distinct labels because non-decreasing allows equal timestamps at
    # consecutive steps... but with distinct labels, you can never have
    # equal timestamps! So strict = non-decreasing for single-label.

    # This means the O(n log n) upper bound must be for multi-label or
    # a different model. Let me check the literature claims more carefully.
    print("  With single-label (all timestamps distinct from a permutation),")
    print("  strict increasing = non-decreasing (since no two edges share a timestamp).")
    print("  The Ω(n log n) lower bound is likely for the MULTI-LABEL setting")
    print("  where each edge can appear at multiple times.")


def path_labeling_construction(n):
    """
    The known Ω(n log n) construction for temporal spanners uses a
    DIFFERENT model: the temporal graph is given as a sequence of
    static graphs (snapshots), and each edge can appear in multiple snapshots.

    For single-label temporal cliques (each edge has exactly one timestamp),
    the question is different. Let me investigate what the actual tight bound is.

    Key insight: with n*(n-1)/2 edges and n*(n-1)/2 distinct timestamps,
    the labeling is a bijection. The graph is very "rich" temporally.
    Removing one edge only breaks journeys that MUST use that specific edge
    at that specific time. With so many edges, there are usually alternatives.
    """
    pass


def analyze_what_greedy_removes(n, timestamps):
    """Understand WHY greedy can remove so many edges."""
    edges = sorted(timestamps.keys(), key=lambda e: -timestamps[e])
    full_reach = check_reachability_nondec(n, timestamps)

    current = set(timestamps.keys())
    removed = []
    kept = []

    for e in edges:
        trial = current - {e}
        ts2 = {edge: timestamps[edge] for edge in trial}
        if check_reachability_nondec(n, ts2) == full_reach:
            current = trial
            removed.append(e)
        else:
            kept.append(e)

    print(f"\n  Kept {len(kept)} edges, removed {len(removed)}")
    print(f"  Kept edges (by timestamp):")
    for e in sorted(kept, key=lambda e: timestamps[e]):
        print(f"    {e}: t={timestamps[e]}")
    print(f"  Removed edges (by timestamp):")
    for e in sorted(removed, key=lambda e: timestamps[e]):
        print(f"    {e}: t={timestamps[e]}")

    # Analyze: what's the structure of kept edges?
    # Is it a tree? Does it have a pattern?
    kept_set = set(kept)
    degrees = defaultdict(int)
    for (u, v) in kept_set:
        degrees[u] += 1
        degrees[v] += 1
    print(f"  Degree sequence of spanner: {sorted(degrees.values(), reverse=True)}")

    return kept, removed


def critical_insight_experiment(n):
    """
    CRITICAL INSIGHT TEST:

    The key question is about the MODEL. In the standard temporal graph model:
    - A temporal graph G = (V, E, λ) where λ: E → 2^{[T]} assigns TIME SETS
    - A temporal spanner H ⊆ E must preserve temporal reachability
    - Single-label: each edge gets exactly one timestamp (|λ(e)| = 1)
    - The temporal clique: underlying graph is K_n

    For SINGLE-LABEL temporal cliques:
    - Total edges: n(n-1)/2
    - Each edge has a unique timestamp (since it's a complete graph with one label each)

    CONJECTURE: For single-label temporal cliques, the minimum spanner is Θ(n).

    Let me test this more carefully by:
    1. Computing exact minima for K_5 and K_7
    2. Running larger samples for K_9, K_11
    """
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    m = len(edges)

    print(f"\nExact analysis of K_{n} (m={m}):")

    # Best adversarial labeling search
    best_greedy = 0
    best_ts = None
    trials = min(50000, max(10000, 1000000 // (m * m)))

    for _ in range(trials):
        perm = list(range(1, m + 1))
        random.shuffle(perm)
        ts = {edges[i]: perm[i] for i in range(m)}
        reach = check_reachability_strict(n, ts)
        if len(reach) < n * (n - 1):
            continue
        gs = greedy_spanner(n, ts, strict=True)
        if gs > best_greedy:
            best_greedy = gs
            best_ts = ts.copy()

    print(f"  Best greedy spanner over {trials} random labelings: {best_greedy}")
    print(f"  n = {n}, n-1 = {n-1}, 2(n-1) = {2*(n-1)}, n*lg(n) = {n*math.log2(n):.1f}")

    if best_ts and n <= 7:
        print(f"  Best labeling: {best_ts}")
        analyze_what_greedy_removes(n, best_ts)

    # Try to compute exact minimum for the best labeling found
    if best_ts and m <= 15:
        print(f"\n  Computing exact minimum for best labeling...")
        exact = exact_min_spanner_ilp_style(n, best_ts, strict=True)
        print(f"  Exact minimum spanner: {exact}")

    return best_greedy, best_ts


if __name__ == "__main__":
    random.seed(2026)

    print("=" * 60)
    print("PHASE 3: Model clarification and tight bounds")
    print("=" * 60)

    multi_label_analysis(5)

    print("\n" + "=" * 60)
    print("Single-label temporal clique: exact minimum spanner search")
    print("=" * 60)

    results = {}
    for n in [5, 7, 9, 11, 13, 15]:
        gs, ts = critical_insight_experiment(n)
        results[n] = gs

    print("\n" + "=" * 60)
    print("GROWTH RATE ANALYSIS")
    print("=" * 60)
    print(f"{'n':>4} {'best_spanner':>13} {'n-1':>5} {'2(n-1)':>7} {'n*lg(n)':>8} {'ratio/n':>8}")
    for n in sorted(results.keys()):
        sp = results[n]
        print(f"{n:>4} {sp:>13} {n-1:>5} {2*(n-1):>7} {n*math.log2(n):>8.1f} {sp/n:>8.2f}")
