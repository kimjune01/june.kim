#!/usr/bin/env python3
"""Controlled keep-criterion ablation (synthetic abstraction-learning domain).

Isolates the KEEP rule: every variant sees the SAME candidate-abstraction stream
(frequent substrings mined from training traces); they differ only in which
candidates they retain. We then plan held-out tasks with each library and measure
library size against planning cost.

Cost model (transparent proxy for search under a world model):
  - A task is reconstructed by greedy longest-match over the library.
  - A maximal run of r uncovered primitive steps costs B**r  (deep search over a
    hard span the library does not abstract).
  - Each token also pays (B + |L|): B primitive branches + |L| macro candidates to
    match. So a bigger library lowers search by covering spans but raises the
    per-step matching floor -- the carrying cost.

The domain plants one RARE but LONG "bottleneck" skill: it appears in few traces
(low frequency, low MDL gain) yet each use collapses a B**6 span (huge planning
utility). This is the separating case: compression keeps the frequent short skills
and drops the bottleneck; utility keeps the bottleneck.
"""
import random, math
from collections import Counter

random.seed(7)
PRIMS = "abcdefgh"          # 8 primitive actions
B = len(PRIMS)              # primitive branching factor
N_TRAIN, N_TEST = 100, 40

# ground-truth reusable skills: name -> (subsequence, fraction of tasks containing)
SKILLS = {
    "freq_abc": ("abc", 0.60),   # frequent, short -> high MDL gain, modest utility
    "freq_abd": ("abd", 0.25),   # frequent, short, overlaps freq_abc on "ab"
    "mid_efg":  ("efg", 0.30),   # medium
    "BOTTLE":   ("hgfedc", 0.08),# RARE, LONG -> low MDL gain, huge planning utility
}

def make_task(rng, force_bottleneck=False):
    parts = []
    for name, (s, frac) in SKILLS.items():
        if (name == "BOTTLE" and force_bottleneck) or rng.random() < frac:
            parts.append(s)
    parts.append("".join(rng.choice(PRIMS) for _ in range(rng.randint(1, 3))))  # filler
    rng.shuffle(parts)
    return "".join(parts)

rng = random.Random(7)
train = [make_task(rng) for _ in range(N_TRAIN)]
# held-out: half forced to require the bottleneck span, half not
test_bottle = [make_task(rng, force_bottleneck=True) for _ in range(N_TEST // 2)]
test_plain  = [make_task(rng, force_bottleneck=False) for _ in range(N_TEST // 2)]

# ---- proposal: mine frequent substrings (length 2..6, support >= 5) ----
def mine_candidates(traces, lo=2, hi=6, min_support=5):
    cnt = Counter()
    for t in traces:
        seen = set()
        for L in range(lo, hi + 1):
            for i in range(len(t) - L + 1):
                seen.add(t[i:i + L])
        for s in seen:
            cnt[s] += 1
    return {s: c for s, c in cnt.items() if c >= min_support}

CAND = mine_candidates(train)                       # the shared candidate stream

# ---- planning cost of a task under a library L (set of macro strings) ----
def cost(task, L):
    macros = sorted(L, key=len, reverse=True)
    i, toks, run, c = 0, 0, 0, 0
    while i < len(task):
        m = next((x for x in macros if task.startswith(x, i)), None)
        if m:
            if run: c += B ** run; run = 0
            i += len(m); toks += 1
        else:
            run += 1; i += 1; toks += 1
    if run: c += B ** run
    return c + toks * (B + len(L))

def mean_cost(tasks, L):
    return sum(cost(t, L) for t in tasks) / len(tasks)

def corpus_cost(L):  # training planning cost, for greedy utility selection
    return sum(cost(t, L) for t in train)

# ---- keep rules (all draw from CAND) ----
def keep_accumulate():
    return set(CAND)

def keep_frequency(thresh=20):
    return {s for s, c in CAND.items() if c >= thresh}

def keep_mdl(budget=None):
    # greedy by net description-length gain on the residual corpus; stop at budget
    # (carrying cost) or when no positive gain remains.
    L, residual = set(), list(train)
    while budget is None or len(L) < budget:
        best, best_g = None, 0
        for s in CAND:
            if s in L: continue
            occ = sum(t.count(s) for t in residual)
            g = occ * (len(s) - 1) - (len(s) + 1)
            if g > best_g: best, best_g = s, g
        if best is None: break
        L.add(best)
        residual = [t.replace(best, "\x00") for t in residual]
    return L

def keep_utility(budget=None):
    # greedy by marginal training-planning-cost reduction; stop at budget or no gain.
    L = set()
    while budget is None or len(L) < budget:
        base = corpus_cost(L)
        best, best_g = None, 0
        for s in CAND:
            if s in L: continue
            g = base - corpus_cost(L | {s})
            if g > best_g: best, best_g = s, g
        if best is None: break
        L.add(best)
    return L

def lg(x):
    return round(math.log10(x), 2) if x > 0 else 0.0

BOTT = SKILLS["BOTTLE"][0]
def has_bottleneck(L):
    return any(len(m) >= 4 and m in BOTT for m in L)

print(f"primitives={B}  train={N_TRAIN}  test={N_TEST}  candidates_mined={len(CAND)}\n")

print("Unconstrained baselines (no library budget):")
print(f"{'keep rule':<16}{'|L|':>5}{'logCost_plain':>15}{'logCost_bottle':>16}  bottleneck?")
print("-" * 70)
for name, L in [("no-library", set()), ("accumulate-all", keep_accumulate()),
                ("frequency>=20", keep_frequency(20)),
                ("MDL (uncapped)", keep_mdl()), ("utility (uncapped)", keep_utility())]:
    print(f"{name:<16}{len(L):>5}{lg(mean_cost(test_plain, L)):>15}"
          f"{lg(mean_cost(test_bottle, L)):>16}  {'YES' if has_bottleneck(L) else 'no'}")

print("\nBudget sweep -- held-out cost on BOTTLENECK tasks (log10), MDL vs utility:")
print(f"{'budget K':>9}{'MDL |bottle':>14}{'MDL has-b':>11}{'util |bottle':>14}{'util has-b':>12}")
print("-" * 60)
for K in [2, 3, 4, 5, 6, 8, 12, 20]:
    Lm, Lu = keep_mdl(K), keep_utility(K)
    print(f"{K:>9}{lg(mean_cost(test_bottle, Lm)):>14}{('YES' if has_bottleneck(Lm) else 'no'):>11}"
          f"{lg(mean_cost(test_bottle, Lu)):>14}{('YES' if has_bottleneck(Lu) else 'no'):>12}")

print("\nAt K=4:")
print("  MDL keeps:    ", sorted(keep_mdl(4), key=len, reverse=True))
print("  utility keeps:", sorted(keep_utility(4), key=len, reverse=True))
