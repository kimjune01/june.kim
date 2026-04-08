#!/usr/bin/env python3
"""
H5b: Universal 1-healability deep dive — FINAL consolidated run.
Corrected sequential healing (no re-adding deleted edge).
"""

import itertools
import random
import time
from collections import defaultdict

random.seed(42)

def compute_reachability(k, edge_set, M):
    n = 2 * k
    sorted_edges = sorted([(M[i][j], i, k + j) for (i, j) in edge_set])
    can_reach = [dict() for _ in range(n)]
    for v in range(n):
        can_reach[v][v] = 0
    for (t, a, b) in sorted_edges:
        new_b = {s: t for s, at in can_reach[a].items()
                 if at < t and (s not in can_reach[b] or t < can_reach[b][s])}
        new_a = {s: t for s, at in can_reach[b].items()
                 if at < t and (s not in can_reach[a] or t < can_reach[a][s])}
        can_reach[b].update(new_b)
        can_reach[a].update(new_a)
    reachable = set()
    for v in range(n):
        for src in can_reach[v]:
            if src != v:
                reachable.add((src, v))
    return reachable


def full_reachability(k, M):
    return compute_reachability(k, set((i, j) for i in range(k) for j in range(k)), M)


def random_matrix(k):
    perm = list(range(1, k * k + 1))
    random.shuffle(perm)
    return [perm[i * k:(i + 1) * k] for i in range(k)]


def sm_matrix(k):
    return [list(range(i * k + 1, (i + 1) * k + 1)) for i in range(k)]


def find_min_spanner_greedy(k, M):
    all_e = set((i, j) for i in range(k) for j in range(k))
    full = compute_reachability(k, all_e, M)
    edges = sorted(all_e, key=lambda e: M[e[0]][e[1]], reverse=True)
    cur = set(all_e)
    for e in edges:
        c = cur - {e}
        if compute_reachability(k, c, M) == full:
            cur = c
    return cur, full


def find_min_spanner(k, M):
    if k <= 3:
        all_e = [(i, j) for i in range(k) for j in range(k)]
        full = full_reachability(k, M)
        for size in range(1, k * k + 1):
            for combo in itertools.combinations(all_e, size):
                if compute_reachability(k, set(combo), M) == full:
                    return set(combo), full
    return find_min_spanner_greedy(k, M)


# ════════════════════════════════════════════════════════════
# PART 1
# ════════════════════════════════════════════════════════════
def run_part1(n_samples=50):
    print("=" * 70)
    print("PART 1: 1-healability on random matrices")
    print("=" * 70)

    for k in [3, 4, 5, 6]:
        stats = defaultdict(int)
        candidate_counts = []
        spanner_sizes = []

        t0 = time.time()
        for trial in range(n_samples):
            M = random_matrix(k)
            spanner, full_reach = find_min_spanner(k, M)
            spanner_sizes.append(len(spanner))
            all_edges = set((i, j) for i in range(k) for j in range(k))
            non_spanner = all_edges - spanner

            trial_ok = True
            for e in sorted(spanner):
                reduced = spanner - {e}
                red_reach = compute_reachability(k, reduced, M)
                if red_reach == full_reach:
                    stats['redundant'] += 1
                    continue
                cands = [r for r in non_spanner
                         if compute_reachability(k, reduced | {r}, M) == full_reach]
                if cands:
                    stats['healable'] += 1
                    candidate_counts.append(len(cands))
                else:
                    stats['fail'] += 1
                    trial_ok = False
            if trial_ok:
                stats['matrix_ok'] += 1

        elapsed = time.time() - t0
        non_red = stats['healable'] + stats['fail']
        total = non_red + stats['redundant']

        print(f"\n--- k={k} ({elapsed:.1f}s) ---")
        print(f"  Spanner: avg {sum(spanner_sizes)/len(spanner_sizes):.1f}/{k*k}, "
              f"non-spanner: avg {k*k - sum(spanner_sizes)/len(spanner_sizes):.1f}")
        print(f"  Edges: {total} total, {stats['redundant']} redundant, {non_red} critical")
        if non_red > 0:
            print(f"  1-healable: {stats['healable']}/{non_red} = "
                  f"{stats['healable']/non_red*100:.1f}% of critical edges")
        print(f"  Matrices fully 1-healable: {stats['matrix_ok']}/{n_samples}")
        if candidate_counts:
            u1 = sum(1 for c in candidate_counts if c == 1)
            print(f"  Candidates: avg={sum(candidate_counts)/len(candidate_counts):.1f}, "
                  f"exactly 1: {u1}/{len(candidate_counts)} ({u1/len(candidate_counts)*100:.0f}%)")


# ════════════════════════════════════════════════════════════
# PART 2
# ════════════════════════════════════════════════════════════
def run_part2(n_samples=50):
    print("\n" + "=" * 70)
    print("PART 2: Characterize the replacement edge")
    print("=" * 70)

    for k in [3, 4, 5, 6]:
        loc = defaultdict(int)
        rank_diffs = []
        total = 0

        t0 = time.time()
        for trial in range(n_samples):
            M = random_matrix(k)
            spanner, full_reach = find_min_spanner(k, M)
            all_edges = set((i, j) for i in range(k) for j in range(k))
            non_spanner = all_edges - spanner

            for e in sorted(spanner):
                reduced = spanner - {e}
                if compute_reachability(k, reduced, M) == full_reach:
                    continue
                cands = [r for r in non_spanner
                         if compute_reachability(k, reduced | {r}, M) == full_reach]
                if not cands:
                    continue
                total += 1
                any_local = False
                for c in cands:
                    sr, sc = c[0] == e[0], c[1] == e[1]
                    if sr and sc:
                        loc['both'] += 1
                    elif sr:
                        loc['row'] += 1
                    elif sc:
                        loc['col'] += 1
                    else:
                        loc['neither'] += 1
                    if sr or sc:
                        any_local = True
                    rank_diffs.append(abs(M[e[0]][e[1]] - M[c[0]][c[1]]))
                if any_local:
                    loc['has_local'] += 1

        elapsed = time.time() - t0
        nc = loc['row'] + loc['col'] + loc['both'] + loc['neither']

        print(f"\n--- k={k} ({elapsed:.1f}s), {total} healable edges ---")
        if nc > 0:
            print(f"  Same row:    {loc['row']:4d} ({loc['row']/nc*100:5.1f}%)")
            print(f"  Same col:    {loc['col']:4d} ({loc['col']/nc*100:5.1f}%)")
            print(f"  Neither:     {loc['neither']:4d} ({loc['neither']/nc*100:5.1f}%)")
        if total > 0:
            print(f"  Has local candidate: {loc['has_local']}/{total} ({loc['has_local']/total*100:.0f}%)")
        if rank_diffs:
            print(f"  Timestamp gap: avg={sum(rank_diffs)/len(rank_diffs):.1f}")


# ════════════════════════════════════════════════════════════
# PART 3
# ════════════════════════════════════════════════════════════
def run_part3(n_samples=20):
    print("\n" + "=" * 70)
    print("PART 3: Multi-deletion resilience (corrected)")
    print("=" * 70)

    for k in [3, 4, 5, 6]:
        print(f"\n--- k={k} ---")

        for nd in [1, 2, 3]:
            batch_h = batch_t = seq_h = seq_t = 0
            t0 = time.time()

            for trial in range(n_samples):
                M = random_matrix(k)
                spanner, full_reach = find_min_spanner(k, M)
                all_edges = set((i, j) for i in range(k) for j in range(k))
                non_spanner = list(all_edges - spanner)
                sp_list = list(spanner)

                if nd > len(sp_list):
                    continue

                # Batch: delete nd edges, heal with ≤nd from non-spanner
                combos = list(itertools.combinations(sp_list, nd))
                if len(combos) > 200:
                    combos = random.sample(combos, 200)

                for dc in combos:
                    batch_t += 1
                    reduced = spanner - set(dc)
                    if compute_reachability(k, reduced, M) == full_reach:
                        batch_h += 1
                        continue
                    found = False
                    for rs in range(1, nd + 1):
                        if found:
                            break
                        if rs > len(non_spanner):
                            break
                        for rc in itertools.combinations(non_spanner, rs):
                            if compute_reachability(k, reduced | set(rc), M) == full_reach:
                                found = True
                                break
                    if found:
                        batch_h += 1

                # Sequential: delete one, heal (from non-deleted only), repeat
                for _ in range(50):
                    seq = random.sample(sp_list, nd)
                    seq_t += 1
                    current = set(spanner)
                    ok = True
                    for e in seq:
                        if e not in current:
                            ok = False; break
                        current.discard(e)
                        if compute_reachability(k, current, M) == full_reach:
                            continue
                        avail = all_edges - current - set(seq)
                        repaired = False
                        for r in sorted(avail):
                            if compute_reachability(k, current | {r}, M) == full_reach:
                                current.add(r)
                                repaired = True
                                break
                        if not repaired:
                            ok = False; break
                    if ok:
                        seq_h += 1

            elapsed = time.time() - t0
            print(f"  Delete {nd} ({elapsed:.1f}s):")
            if batch_t:
                print(f"    Batch: {batch_h}/{batch_t} = {batch_h/batch_t*100:.1f}%")
            if seq_t:
                print(f"    Sequential: {seq_h}/{seq_t} = {seq_h/seq_t*100:.1f}%")


# ════════════════════════════════════════════════════════════
# PART 4
# ════════════════════════════════════════════════════════════
def run_part4(n_samples=50):
    print("\n" + "=" * 70)
    print("PART 4: Greedy construction from empty / spanning tree")
    print("=" * 70)

    for k in [3, 4, 5, 6, 7]:
        from_empty = []
        from_tree = []
        t0 = time.time()

        for trial in range(n_samples):
            M = random_matrix(k)
            full_reach = full_reachability(k, M)
            all_e = [(i, j) for i in range(k) for j in range(k)]

            # From empty
            cur = set()
            for _ in range(k * k):
                cr = compute_reachability(k, cur, M)
                if cr == full_reach:
                    break
                best = max((e for e in all_e if e not in cur),
                           key=lambda e: len(compute_reachability(k, cur | {e}, M)) - len(cr),
                           default=None)
                if best is None:
                    break
                cur.add(best)
            from_empty.append(len(cur))

            # From random spanning tree
            n = 2 * k
            visited = {0}
            tree = set()
            random.shuffle(all_e)
            while len(visited) < n:
                for (i, j) in all_e:
                    a, b = i, k + j
                    if a in visited and b not in visited:
                        tree.add((i, j)); visited.add(b); break
                    elif b in visited and a not in visited:
                        tree.add((i, j)); visited.add(a); break
                else:
                    break
                random.shuffle(all_e)

            cur = set(tree)
            for _ in range(k * k):
                cr = compute_reachability(k, cur, M)
                if cr == full_reach:
                    break
                remaining = [e for e in all_e if e not in cur]
                if not remaining:
                    break
                best = max(remaining,
                           key=lambda e: len(compute_reachability(k, cur | {e}, M)) - len(cr))
                if len(compute_reachability(k, cur | {best}, M)) <= len(cr):
                    break
                cur.add(best)
            from_tree.append(len(cur))

        elapsed = time.time() - t0
        print(f"\n--- k={k} ({elapsed:.1f}s) ---")
        print(f"  From empty: avg={sum(from_empty)/len(from_empty):.1f}, "
              f"min={min(from_empty)}, max={max(from_empty)}")
        print(f"  From tree:  avg={sum(from_tree)/len(from_tree):.1f}, "
              f"min={min(from_tree)}, max={max(from_tree)}")

        # Compare to greedy min spanner
        min_sizes = []
        for trial in range(min(n_samples, 20)):
            M = random_matrix(k)
            sp, _ = find_min_spanner_greedy(k, M)
            min_sizes.append(len(sp))
        print(f"  Greedy min:  avg={sum(min_sizes)/len(min_sizes):.1f}")
        print(f"  k²={k*k}")


# ════════════════════════════════════════════════════════════
# PART 5
# ════════════════════════════════════════════════════════════
def run_part5(n_samples=20):
    print("\n" + "=" * 70)
    print("PART 5: Pruning from full graph maintaining 1-healability")
    print("=" * 70)

    for k in [3, 4, 5]:
        min_sp = []
        heal_sp = []
        t0 = time.time()

        for trial in range(n_samples):
            M = random_matrix(k)
            full_reach = full_reachability(k, M)
            all_edges = set((i, j) for i in range(k) for j in range(k))

            sp, _ = find_min_spanner(k, M)
            min_sp.append(len(sp))

            # Prune: start from full, remove edges maintaining spanner + 1-healable
            current = set(all_edges)
            for e in list(current):
                if e not in current:
                    continue
                cand = current - {e}
                if compute_reachability(k, cand, M) != full_reach:
                    continue  # e is critical, can't remove

                # Check 1-healability of cand
                non_cand = all_edges - cand  # just {e}
                ok = True
                for e2 in cand:
                    red = cand - {e2}
                    if compute_reachability(k, red, M) == full_reach:
                        continue
                    if any(compute_reachability(k, red | {r}, M) == full_reach for r in non_cand):
                        continue
                    ok = False
                    break
                if ok:
                    current = cand

            heal_sp.append(len(current))

        elapsed = time.time() - t0
        print(f"\n--- k={k} ({elapsed:.1f}s) ---")
        print(f"  Min spanner:     avg={sum(min_sp)/len(min_sp):.1f}")
        print(f"  1-healable size: avg={sum(heal_sp)/len(heal_sp):.1f}")
        print(f"  Overhead:        avg={sum(h-m for h,m in zip(heal_sp,min_sp))/len(heal_sp):.1f}")
        print(f"  k²={k*k}")


# ════════════════════════════════════════════════════════════
# SM(k) secondary
# ═��══════════════════════════════════════════════════════════
def run_sm():
    print("\n" + "=" * 70)
    print("SM(k) COMPARISON")
    print("=" * 70)

    for k in [3, 4, 5, 6]:
        M = sm_matrix(k)
        sp, full = find_min_spanner(k, M)
        all_e = set((i, j) for i in range(k) for j in range(k))
        non_sp = all_e - sp

        healable = 0
        critical = 0
        for e in sorted(sp):
            red = sp - {e}
            if compute_reachability(k, red, M) == full:
                continue
            critical += 1
            if any(compute_reachability(k, red | {r}, M) == full for r in non_sp):
                healable += 1

        print(f"\n--- SM(k={k}): spanner {len(sp)}/{k*k}, "
              f"healable {healable}/{critical} critical edges ---")


# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("H5b: Universal 1-healability deep dive (FINAL)")
    print("Random all-distinct k×k matrices\n")

    run_part1(50)
    run_part2(50)
    run_part3(20)
    run_part4(50)
    run_part5(20)
    run_sm()

    print("\n" + "=" * 70)
    print("DONE")
