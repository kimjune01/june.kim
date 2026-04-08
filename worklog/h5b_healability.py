#!/usr/bin/env python3
"""
H5b: Universal 1-healability deep dive for temporal spanners.
Tests on RANDOM all-distinct k×k matrices (primary) and SM(k) (secondary).

Key finding from sizing: minimum spanners of K_{k,k} are LARGE:
  k=3: ~8/9 edges, k=4: ~12/16, k=5: ~17/25, k=6: ~22/36
This means very few non-spanner edges available as replacements.
"""

import itertools
import random
import time
from collections import defaultdict

random.seed(42)

# ─── Core: temporal reachability (single-pass, verified correct) ───

def compute_reachability(k, edge_set, M):
    """
    All-pairs temporal reachability in K_{k,k}.
    Vertices: a_i = i, b_j = k+j. Edge (i,j) has timestamp M[i][j].
    Strictly increasing timestamps for journeys (all timestamps distinct).
    """
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
    all_edges = set((i, j) for i in range(k) for j in range(k))
    return compute_reachability(k, all_edges, M)


def is_spanner(k, M, edge_set, full_reach):
    return compute_reachability(k, edge_set, M) == full_reach


# ─── Matrix generation ───

def random_matrix(k):
    perm = list(range(1, k * k + 1))
    random.shuffle(perm)
    return [perm[i * k:(i + 1) * k] for i in range(k)]


def sm_matrix(k):
    return [list(range(i * k + 1, (i + 1) * k + 1)) for i in range(k)]


# ─── Spanner finding ───

def find_minimum_spanner_brute(k, M):
    full_reach = full_reachability(k, M)
    all_edges = [(i, j) for i in range(k) for j in range(k)]
    for size in range(1, k * k + 1):
        for combo in itertools.combinations(all_edges, size):
            if compute_reachability(k, set(combo), M) == full_reach:
                return set(combo), full_reach
    return set(all_edges), full_reach


def find_minimum_spanner_greedy(k, M):
    full_reach = full_reachability(k, M)
    all_edges = [(i, j) for i in range(k) for j in range(k)]
    all_edges.sort(key=lambda e: M[e[0]][e[1]], reverse=True)
    current = set(all_edges)
    for e in all_edges:
        candidate = current - {e}
        if is_spanner(k, M, candidate, full_reach):
            current = candidate
    return current, full_reach


def find_minimum_spanner(k, M):
    if k <= 3:
        return find_minimum_spanner_brute(k, M)
    else:
        return find_minimum_spanner_greedy(k, M)


# ─── Part 1: 1-healability ───

def test_1_healability(k, M, spanner, full_reach):
    all_edges = set((i, j) for i in range(k) for j in range(k))
    non_spanner = all_edges - spanner

    results = []
    for e in sorted(spanner):
        reduced = spanner - {e}
        reduced_reach = compute_reachability(k, reduced, M)

        if reduced_reach == full_reach:
            results.append({'deleted': e, 'redundant': True, 'healable': True,
                            'candidates': [], 'lost_pairs': 0})
            continue

        lost = len(full_reach) - len(reduced_reach)
        candidates = []
        for r in sorted(non_spanner):
            healed = reduced | {r}
            if compute_reachability(k, healed, M) == full_reach:
                candidates.append(r)

        results.append({'deleted': e, 'redundant': False, 'healable': len(candidates) > 0,
                        'candidates': candidates, 'lost_pairs': lost})
    return results


def run_part1(n_samples=50):
    print("=" * 70)
    print("PART 1: 1-healability on random matrices")
    print("=" * 70)

    for k in [3, 4, 5, 6]:
        total_edges = 0
        healable_edges = 0
        redundant_edges = 0
        non_red_non_heal = 0
        candidate_counts = []
        spanner_sizes = []
        non_spanner_sizes = []
        lost_pairs_list = []
        matrix_all_heal = 0

        t0 = time.time()
        for trial in range(n_samples):
            M = random_matrix(k)
            spanner, full_reach = find_minimum_spanner(k, M)
            spanner_sizes.append(len(spanner))
            non_spanner_sizes.append(k * k - len(spanner))

            results = test_1_healability(k, M, spanner, full_reach)

            trial_ok = True
            for r in results:
                total_edges += 1
                if r['redundant']:
                    redundant_edges += 1
                    continue
                if r['healable']:
                    healable_edges += 1
                    candidate_counts.append(len(r['candidates']))
                else:
                    non_red_non_heal += 1
                    lost_pairs_list.append(r['lost_pairs'])
                    trial_ok = False
            if trial_ok:
                matrix_all_heal += 1

        elapsed = time.time() - t0
        non_red = total_edges - redundant_edges

        print(f"\n--- k={k} ({elapsed:.1f}s) ---")
        print(f"  Samples: {n_samples}")
        print(f"  Spanner size: avg={sum(spanner_sizes)/len(spanner_sizes):.1f}, k²={k*k}")
        print(f"  Non-spanner (available replacements): avg={sum(non_spanner_sizes)/len(non_spanner_sizes):.1f}")
        print(f"  Total spanner edges: {total_edges}, redundant: {redundant_edges}")
        if non_red > 0:
            print(f"  Healable: {healable_edges}/{non_red} = {healable_edges/non_red*100:.1f}%")
        print(f"  Failures: {non_red_non_heal}")
        print(f"  Matrices where ALL edges healable: {matrix_all_heal}/{n_samples} = {matrix_all_heal/n_samples*100:.1f}%")
        if candidate_counts:
            print(f"  Candidates when healable: min={min(candidate_counts)}, max={max(candidate_counts)}, avg={sum(candidate_counts)/len(candidate_counts):.1f}")
            u1 = sum(1 for c in candidate_counts if c == 1)
            print(f"  Exactly 1 candidate: {u1}/{len(candidate_counts)} = {u1/len(candidate_counts)*100:.1f}%")
        if lost_pairs_list:
            print(f"  Lost pairs on failure: min={min(lost_pairs_list)}, max={max(lost_pairs_list)}, avg={sum(lost_pairs_list)/len(lost_pairs_list):.1f}")


# ─── Part 2: Characterize replacement ───

def run_part2(n_samples=50):
    print("\n" + "=" * 70)
    print("PART 2: Characterize the replacement edge")
    print("=" * 70)

    for k in [3, 4, 5, 6]:
        same_row = 0
        same_col = 0
        neither = 0
        both = 0
        rank_diffs = []
        unique_best = 0
        ties = 0
        total = 0

        # Local information test: can replacement be found using only
        # the deleted edge's row/column?
        local_row_col = 0  # replacement in same row or col
        non_local = 0

        t0 = time.time()
        for trial in range(n_samples):
            M = random_matrix(k)
            spanner, full_reach = find_minimum_spanner(k, M)
            results = test_1_healability(k, M, spanner, full_reach)

            for r in results:
                if r['redundant'] or not r['healable']:
                    continue
                total += 1
                del_e = r['deleted']

                any_local = False
                for cand in r['candidates']:
                    sr = (cand[0] == del_e[0])
                    sc = (cand[1] == del_e[1])
                    if sr and sc:
                        both += 1
                    elif sr:
                        same_row += 1
                    elif sc:
                        same_col += 1
                    else:
                        neither += 1

                    if sr or sc:
                        any_local = True

                    rank_diffs.append(abs(M[del_e[0]][del_e[1]] - M[cand[0]][cand[1]]))

                if any_local:
                    local_row_col += 1
                else:
                    non_local += 1

                if len(r['candidates']) == 1:
                    unique_best += 1
                else:
                    ties += 1

        elapsed = time.time() - t0
        n_cands = same_row + same_col + neither + both

        print(f"\n--- k={k} ({elapsed:.1f}s) ---")
        print(f"  Total healable edges: {total}")
        if total == 0:
            print(f"  No healable edges to characterize")
            continue
        print(f"  Total (deleted, replacement) pairs: {n_cands}")
        if n_cands > 0:
            print(f"  Same row only:  {same_row} ({same_row/n_cands*100:.1f}%)")
            print(f"  Same col only:  {same_col} ({same_col/n_cands*100:.1f}%)")
            print(f"  Same row & col: {both} ({both/n_cands*100:.1f}%)")
            print(f"  Neither:        {neither} ({neither/n_cands*100:.1f}%)")
        print(f"  At least 1 local (same row/col) candidate: {local_row_col}/{total} = {local_row_col/total*100:.1f}%")
        if rank_diffs:
            print(f"  Timestamp diff: min={min(rank_diffs)}, max={max(rank_diffs)}, avg={sum(rank_diffs)/len(rank_diffs):.1f}")
        print(f"  Unique replacement: {unique_best}/{total} ({unique_best/total*100:.1f}%)")
        print(f"  Multiple replacements: {ties}/{total} ({ties/total*100:.1f}%)")


# ─── Part 3: Multi-deletion resilience ───

def run_part3(n_samples=20):
    print("\n" + "=" * 70)
    print("PART 3: Multi-deletion resilience")
    print("=" * 70)

    for k in [3, 4, 5]:
        print(f"\n--- k={k} ---")

        for num_del in [2, 3]:
            batch_h = 0
            batch_t = 0
            seq_h = 0
            seq_t = 0

            t0 = time.time()
            for trial in range(n_samples):
                M = random_matrix(k)
                spanner, full_reach = find_minimum_spanner(k, M)
                all_edges = set((i, j) for i in range(k) for j in range(k))
                non_spanner = list(all_edges - spanner)
                spanner_list = list(spanner)

                if num_del > len(spanner_list):
                    continue

                # Batch: try deletion combos
                if len(spanner_list) <= 15:
                    combos = list(itertools.combinations(spanner_list, num_del))
                    if len(combos) > 200:
                        combos = random.sample(combos, 200)
                else:
                    combos = [tuple(random.sample(spanner_list, num_del)) for _ in range(100)]

                for del_combo in combos:
                    batch_t += 1
                    reduced = spanner - set(del_combo)
                    red_reach = compute_reachability(k, reduced, M)

                    if red_reach == full_reach:
                        batch_h += 1
                        continue

                    found = False
                    # Try single replacement first
                    for r in non_spanner:
                        if compute_reachability(k, reduced | {r}, M) == full_reach:
                            found = True
                            break
                    # Try pairs if needed and num_del >= 2
                    if not found and num_del >= 2 and len(non_spanner) <= 30:
                        for r1, r2 in itertools.combinations(non_spanner, 2):
                            if compute_reachability(k, reduced | {r1, r2}, M) == full_reach:
                                found = True
                                break
                    # Try triples
                    if not found and num_del >= 3 and len(non_spanner) <= 20:
                        for combo_r in itertools.combinations(non_spanner, min(3, len(non_spanner))):
                            if compute_reachability(k, reduced | set(combo_r), M) == full_reach:
                                found = True
                                break

                    if found:
                        batch_h += 1

                # Sequential: delete one, heal, delete next, heal
                seq_combos = [tuple(random.sample(spanner_list, num_del)) for _ in range(50)]
                for seq in seq_combos:
                    seq_t += 1
                    current = set(spanner)
                    success = True

                    for e in seq:
                        if e not in current:
                            success = False
                            break
                        current = current - {e}
                        cur_reach = compute_reachability(k, current, M)

                        if cur_reach == full_reach:
                            continue

                        avail = all_edges - current
                        found_r = False
                        for r in avail:
                            if compute_reachability(k, current | {r}, M) == full_reach:
                                current = current | {r}
                                found_r = True
                                break

                        if not found_r:
                            success = False
                            break

                    if success:
                        seq_h += 1

            elapsed = time.time() - t0
            print(f"  Delete {num_del} ({elapsed:.1f}s):")
            if batch_t > 0:
                print(f"    Batch healable (≤{num_del} replacements): {batch_h}/{batch_t} = {batch_h/batch_t*100:.1f}%")
            if seq_t > 0:
                print(f"    Sequential (delete-heal-delete-heal): {seq_h}/{seq_t} = {seq_h/seq_t*100:.1f}%")


# ─── Part 4: Build by healing ───

def run_part4(n_samples=50):
    print("\n" + "=" * 70)
    print("PART 4: Constructive — build by greedily adding edges")
    print("=" * 70)

    for k in [3, 4, 5, 6, 7]:
        edge_counts = []
        step_counts = []
        t0 = time.time()

        for trial in range(n_samples):
            M = random_matrix(k)
            full_reach = full_reachability(k, M)
            all_edges_list = [(i, j) for i in range(k) for j in range(k)]

            # Random spanning tree on K_{k,k} (2k-1 edges)
            n = 2 * k
            visited = {0}
            tree_edges = set()
            random.shuffle(all_edges_list)

            while len(visited) < n:
                found = False
                for (i, j) in all_edges_list:
                    a_n, b_n = i, k + j
                    if a_n in visited and b_n not in visited:
                        tree_edges.add((i, j))
                        visited.add(b_n)
                        found = True
                        break
                    elif b_n in visited and a_n not in visited:
                        tree_edges.add((i, j))
                        visited.add(a_n)
                        found = True
                        break
                if not found:
                    break
                random.shuffle(all_edges_list)

            current = set(tree_edges)
            steps = 0

            for _ in range(k * k):
                cur_reach = compute_reachability(k, current, M)
                if cur_reach == full_reach:
                    break

                best_edge = None
                best_gain = 0
                remaining = set(all_edges_list) - current
                for e in remaining:
                    cand_reach = compute_reachability(k, current | {e}, M)
                    gain = len(cand_reach) - len(cur_reach)
                    if gain > best_gain:
                        best_gain = gain
                        best_edge = e

                if best_edge is None or best_gain == 0:
                    break
                current.add(best_edge)
                steps += 1

            edge_counts.append(len(current))
            step_counts.append(steps)

        elapsed = time.time() - t0

        print(f"\n--- k={k} ({elapsed:.1f}s) ---")
        print(f"  Start: spanning tree ({2*k-1} edges)")
        print(f"  Final edges: min={min(edge_counts)}, max={max(edge_counts)}, avg={sum(edge_counts)/len(edge_counts):.1f}")
        print(f"  Steps added: min={min(step_counts)}, max={max(step_counts)}, avg={sum(step_counts)/len(step_counts):.1f}")
        print(f"  k²={k*k}, k²-k+1={k*k-k+1}")

        # Also: start from empty and build
        edge_counts2 = []
        for trial in range(n_samples):
            M = random_matrix(k)
            full_reach = full_reachability(k, M)
            all_edges_list2 = [(i, j) for i in range(k) for j in range(k)]

            current = set()
            for _ in range(k * k):
                cur_reach = compute_reachability(k, current, M)
                if cur_reach == full_reach:
                    break
                best_edge = None
                best_gain = 0
                for e in all_edges_list2:
                    if e in current:
                        continue
                    cand_reach = compute_reachability(k, current | {e}, M)
                    gain = len(cand_reach) - len(cur_reach)
                    if gain > best_gain:
                        best_gain = gain
                        best_edge = e
                if best_edge is None or best_gain == 0:
                    break
                current.add(best_edge)

            edge_counts2.append(len(current))

        print(f"  From empty: min={min(edge_counts2)}, max={max(edge_counts2)}, avg={sum(edge_counts2)/len(edge_counts2):.1f}")


# ─── Part 5: Pruning from full graph maintaining 1-healability ───

def run_part5(n_samples=30):
    print("\n" + "=" * 70)
    print("PART 5: Pruning from full graph maintaining 1-healability")
    print("=" * 70)

    for k in [3, 4, 5]:
        # Compare: min spanner size vs 1-healable spanner size
        min_sizes = []
        healable_sizes = []
        t0 = time.time()

        for trial in range(n_samples):
            M = random_matrix(k)
            full_reach = full_reachability(k, M)
            all_edges = set((i, j) for i in range(k) for j in range(k))

            # Min spanner (greedy)
            spanner, _ = find_minimum_spanner(k, M)
            min_sizes.append(len(spanner))

            # Prune maintaining 1-healability
            current = set(all_edges)
            edges_to_try = list(current)
            random.shuffle(edges_to_try)

            for e in edges_to_try:
                if e not in current:
                    continue
                candidate = current - {e}

                if not is_spanner(k, M, candidate, full_reach):
                    continue

                # Check: is candidate 1-healable?
                non_cand = all_edges - candidate
                all_ok = True
                for e2 in candidate:
                    reduced = candidate - {e2}
                    red_reach = compute_reachability(k, reduced, M)
                    if red_reach == full_reach:
                        continue
                    healed = any(
                        compute_reachability(k, reduced | {r}, M) == full_reach
                        for r in non_cand
                    )
                    if not healed:
                        all_ok = False
                        break

                if all_ok:
                    current = candidate

            healable_sizes.append(len(current))

        elapsed = time.time() - t0

        print(f"\n--- k={k} ({elapsed:.1f}s) ---")
        print(f"  k²={k*k}")
        print(f"  Min spanner: min={min(min_sizes)}, max={max(min_sizes)}, avg={sum(min_sizes)/len(min_sizes):.1f}")
        print(f"  1-healable spanner: min={min(healable_sizes)}, max={max(healable_sizes)}, avg={sum(healable_sizes)/len(healable_sizes):.1f}")
        overhead = [h - m for h, m in zip(healable_sizes, min_sizes)]
        print(f"  Overhead (healable - min): min={min(overhead)}, max={max(overhead)}, avg={sum(overhead)/len(overhead):.1f}")


# ─── SM(k) secondary ───

def run_sm():
    print("\n" + "=" * 70)
    print("SECONDARY: SM(k) comparison")
    print("=" * 70)

    for k in [3, 4, 5, 6]:
        M = sm_matrix(k)
        full_reach = full_reachability(k, M)
        spanner, _ = find_minimum_spanner(k, M)
        results = test_1_healability(k, M, spanner, full_reach)

        healable = sum(1 for r in results if r['healable'] and not r['redundant'])
        non_red = sum(1 for r in results if not r['redundant'])
        redundant = sum(1 for r in results if r['redundant'])

        print(f"\n--- SM(k={k}) ---")
        print(f"  Spanner: {len(spanner)}/{k*k}, redundant edges: {redundant}")
        if non_red > 0:
            print(f"  1-healable: {healable}/{non_red} = {healable/non_red*100:.1f}%")
        for r in results:
            if not r['redundant']:
                print(f"    Del {r['deleted']} (t={M[r['deleted'][0]][r['deleted'][1]]}): "
                      f"{'HEAL' if r['healable'] else 'FAIL'} "
                      f"({len(r['candidates'])} cand, lost {r['lost_pairs']} pairs)")


# ─── Main ───

if __name__ == "__main__":
    print("H5b: Universal 1-healability deep dive")
    print("Random all-distinct k×k matrices (primary)\n")

    run_part1(n_samples=50)
    run_part2(n_samples=50)
    run_part3(n_samples=15)
    run_part4(n_samples=50)
    run_part5(n_samples=20)
    run_sm()

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
