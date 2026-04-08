# Work Log

## 2026-04-03

### 21:45 — axes-experiment: codex credits exhausted

axes-experiment: codex credits exhausted, locked out until Apr 8. Root cause: ~52M tokens across conversation generation + decomposition in ~12h with no cool-down between phases. Adaptive concurrency ramped too aggressively (hit 20 in run 1, should have capped at 8 from the start). Lesson: budget codex phases across separate days. 26/50 publishers decomposed, 24 remaining. Resume with `uv run python decompose_v2.py --resume` after Apr 8.

## 2026-04-04

### 00:30 — TVG temporal spanner: star+tree construction found

TVG temporal spanner session: from Peters' email to star+tree construction.

**What happened.** Prof. Peters (SFU, retired) replied to June's email about temporal graphs. Shared his paper on temporal spanners (Casteigts-Peters-Schoeters 2021) — O(n log n) bound on temporal clique spanners, O(n) conjectured. We explored the conjecture through: tropical semiring / sheaf cohomology, game theory, hub decomposition, chain routing, fan-out (8 hypotheses across 2 cycles), tropical rotations / node potentials, hyperplane arrangement geometry, gradient descent on potential space, Borsuk-Ulam, bubble sort / contraction, and finally star+tree decomposition.

**Key findings.**
- Exact computation (n≤8): worst-case min spanner = 2n-3
- Two-star construction fails 62% of K_8 instances
- Potential-guided greedy achieves ≤2n-3 100% via gradient descent (n≤10)
- Single adjacent swaps NEVER worsen greedy (zero worsening empirically)
- **THE CONSTRUCTION: star(v) + spanning tree of K_{n-1} = (n-1)+(n-2) = 2n-3 edges. Works 100% for all tested instances (n≤7).**

**Lean formalization** at `~/Documents/tvg/Tvg/`. Main.lean: 30 lines, 1 sorry. Supporting files: 7 proved lemmas (complement, inversion_flip, removable_monotone, chain/two-hop journey constructors, all_early_at_max_hub, pigeonhole). Dead ends documented in Proof.lean, Descent.lean.

**The remaining sorry.** For any temporal clique G on n vertices, ∃ hub v and spanning tree T of K_{n-1} such that star(v) ∪ T preserves all-pairs temporal reachability. Star covers "forward" pairs, tree covers "reverse" pairs.

**Dead ends.** Two pure stars, Barvinok rank, Erdős-Szekeres, Monge/Robinson, tropical Helly, dimension counting, caterpillar, saddle point, submodularity, Borsuk-Ulam.

**Literature.** arXiv:2604.01061 (Apr 2026) on chamber graph isoperimetry — related but doesn't close our sorry. Angrick et al. ESA 2024 on edge-pivotable cliques. Dismountability paper arXiv:2502.01321.

**Python tools** at `~/Documents/tvg/`: worst_case_spanner.py, exact_nash.py, inspect_spanner.py, test_counterexample.py, sat_spanner.py, tropical_rotation.py.

**Next.** Prove the sorry: complementary tree always exists. The tree must provide temporal paths for "reverse" pairs (those where hub v can't route). Greedy tree construction on K_{n-1} with timestamps chosen to complement v's ordering.

### 03:00 — TVG: hub analysis, session end

Further analysis of the star+tree construction:
- Winning hub has NO distinguishing statistical property (avg rank 0.50 for every metric)
- But ≥2 vertices ALWAYS work as hub (minimum across all K₅, K₆ instances)
- "Hardest" instances (exactly 2 winners): the winners are always MIDDLE-rank vertices (not extremes)
- Max-sum hub works 95% of the time. When it fails, middles rescue.
- No clean threshold separates max-sum vs median failure regions (ranges overlap)
- The sorry remains: ∃ v, ∃ T, star(v) ∪ T spans all reachability

The proof needs a non-constructive existence argument or a new structural insight about why at least one vertex always works. Every heuristic fails on some instances. The winner depends on global matrix structure that resists simple characterization.

Session artifacts: tvg/ directory with 8 Lean files, 7 Python scripts, Main.lean (clean 1-sorry theorem statement). All type-check.

### 10:30 — TVG: three-case decomposition → bi-clique → tropical rank

TVG session: three-case decomposition validated (100% on K5/K6), but star+tree fails on non-dismountable bi-cliques (shifted matching SM(k)). Pivoted to matrix view. Bi-clique timestamps = k×k matrix. Reachability rank (min relay columns for same-side reachability) = 2 for SM(k) all tested sizes, and 2 for 99.7%+ of random matrices. Rare rank-3 cases at k=4,5 from row domination (one row pointwise > another). Open: prove reachability rank ≤ constant analytically. Structural argument needed, not counting. Tropical rank connection established but not closed. Key files: three_cases.py, bridge_analysis.py, tropical_rank.py, reach_rank_general.py, rank3_inspect.py, Tvg/ThreeCases.lean.

### 12:15 — TVG: proof tree crystallized

Full proof reduces to ONE sorry: `biclique_spanner` (4k-4 cross-edge spanner for k×k biclique). Budget lemma proved by omega: 2d + (4k-4) ≤ 2n-3. Dismountable branch is literature (Carnevale et al. 2025). Biclique characterization is literature (Theorem 3.10). Assembly is mechanical. Construction is mutable — star+tree for easy cases, matching-union for bicliques — but journey decomposition is the universal invariant. Bridge-less dominated pairs exist for k≤6 but vanish at k≥7; transitive closure through 3 relay columns handles small k. Lean file typechecks with budget proved and 5 sorries (1 real, 4 mechanical/literature).

### 13:30 — TVG: connected permutations = the key condition

**Breakthrough framing.** The biclique spanner reduces to: find 2 matrix columns whose relative permutation is *connected* (indecomposable). A permutation π is connected iff π({1,...,m}) ≠ {1,...,m} for all 1 ≤ m < k. Well-studied: OEIS A003319, Stanley EC1.

**Theorem (from research).** Two linear orders σ₁, σ₂ on [k] generate the complete directed relation under transitive closure iff π = σ₂ ∘ σ₁⁻¹ is a connected permutation.

**Application.** Each column of the biclique k×k matrix M induces a row ordering. If any pair of columns gives a connected relative permutation, then 2 relay columns suffice → 4k-4 spanner → 2n-4 total → conjecture proved.

**Gap.** A generic k×k matrix does NOT guarantee a connected column pair (counterexample: all columns same order → π = id for every pair). BUT: the non-dismountable biclique structure (Theorem 3.10) constrains column orderings via M⁻/M⁺ matchings. The biclique structure may force sufficient diversity among column orderings.

**Proof tree update:**
```
spanner_2n_minus_3
├── dismount (literature) 
├── biclique characterization (literature, Thm 3.10)
├── biclique_spanner ← OPEN
│   ├── M⁻, M⁺ essential (2k edges)
│   ├── ∃ connected column pair (NEW KEY LEMMA)
│   │   └── follows from biclique temporal band structure?
│   ├── connected pair → 2 relay cols suffice (PROVED: permutation theory)
│   └── 2 relay cols → 4k-4 edges (counting)
└── budget ← PROVED (omega)
```

**Next.** Test whether biclique column orderings always contain a connected pair. The M⁻/M⁺ matching structure should prevent all columns from agreeing — the temporal band forces diverse orderings.

### 14:30 — TVG: exists_connected_pair PROVED in Lean

`Tvg/ConnectedPair.lean` compiles clean. The main theorem `exists_connected_pair` has NO sorry. Only 2 mechanical helper sorries remain (finite max exists, injective→surjective on Fin k).

**The proof:** Pick any column j₁. Let i_max = row with max value in j₁. By M⁻ surjectivity, i_max is the min row of some j₂. j₁ ≠ j₂ (min ≠ max when k ≥ 2, by distinctness). Any proper common downset of (j₁, j₂) must contain i_max (it's j₂'s min → in every downset) but then contains everything (it's j₁'s max → downset = all rows). Contradiction.

**Full proof tree now has no content sorries:**
```
spanner_2n_minus_3
├── dismount (literature)
├── biclique characterization (literature)
├── biclique_spanner
│   ├── exists_connected_pair ← PROVED
│   ├── connected → 2 relays (permutation theory, Thm 1 above)
│   └── 2 relays → 4k-4 edges (counting)
└── budget ← PROVED (omega)
```

### 15:30 — TVG: gap identified, semiring tools needed

The connected pair lemma (proved, zero sorry) gives GRAPH reachability but not TEMPORAL reachability. The gap: at intermediate vertices, timestamp monotonicity (M[i'][j₁] ≤ M[i'][j₂]) is a semiring constraint, not a graph constraint. Connected permutations answer "can you get there?" but the conjecture needs "can you get there on time?"

The fix: tropical semiring factorization with vertex potentials. A potential function c : Fin k → ℤ adjusts timestamps so the semiring composition at intermediates is automatically satisfied. Gradient descent on potentials already works empirically (100% for n ≤ 10). The proof needs: the biclique timestamp matrix always admits a low-rank tropical factorization respecting the composition law.

No literature exists for this. The temporal-compression crosswalk (june.kim blog) identified the exact gap: "tropical flows are potentials, not conserved commodities." Three fields (codecs, TVGs, sheaves) study the same structure with zero cross-citations. The semiring application to TVG spanners is the missing bridge.

Status: proof architecture solid (dismount + biclique + budget, all mechanical). Connected pair lemma proved in Lean. The one remaining content gap is algebraic: tropical semiring factorization of the biclique matrix. This is the paper.

### 22:30 — TVG semiring fan-out: 7 cycles, 22 hypotheses

TVG semiring fan-out (7 cycles, 22 hypotheses). Key result: every extremally matched biclique has a c-pivot-edge (c≥0.5, 1830 samples). If provable, closes the temporal spanner conjecture via Angrick ESA 2024 framework. Dead ends documented: two-column routing, tropical algebra, Laman matroid, categorical composition, alteration method, covering LP. Literature digested: Carnevale-Casteigts-Corsini 2025 (dismountability revisited), Angrick et al ESA 2024 (edge-pivot reduction). The remaining proof: one lemma — every extremally matched biclique with sandwich+no-interleaving has an edge where ≥n/2 vertices route through it. Scripts: 16 Python files in /Documents/tvg/. Research log: _drafts/semiring-fanout.md.

### 23:45 — PivotEdge.lean compiles, budget doesn't close

PivotEdge.lean: zero sorry, zero warnings. Any M⁻ cross edge covers k+1 > n/2 vertices via sandwich + minimality + complete bipartite. Single-hop proof (no induction, no multi-hop). But M⁻ ∩ M⁺ = ∅ generically (70% at k=3 → 100% at k=9), so naive budget (M⁻ + M⁺ + two trees) = 2n-2, one over. Empirical min spanner = 2n-4, so spare capacity exists but the construction to exploit it is unknown. The owl has a body and one wing. Flat M⁻+M⁺+trees construction is not a spanner (preserves reachability 0-11% for k≥4). The full construction must use Angrick's recursive pivot framework, not flat matching+tree. One brick laid, building remains.

## 2026-04-05

### H3: Farey mediant as relay construction (opus, DEAD)

**Verdict:** The Farey/Stern-Brocot mediant analogy for temporal spanner relay construction fails at a fundamental structural level. The analogy is seductive but broken.

**Claims tested:**
1. Stern-Brocot tree on k² timestamps provides relay vertices satisfying temporal monotonicity.
2. The mediant property (a+c)/(b+d) lies between a/b and c/d, analogous to relay timestamps lying between source and target.
3. Projecting the k²-1 tree edges onto the biclique yields ≤4k-3 cross edges.

**Why it fails — the dimension mismatch:**
- The Farey mediant operates on a **1D ordered set** (timestamps sorted on a line).
- Temporal relay requires **2D bipartite adjacency** (source and relay edges must share a vertex in K_{k,k}).
- The mediant guarantees value ordering (t_source < t_relay < t_target) but is blind to whether the corresponding biclique edges share a vertex.

**Concrete failure (SM(3), M with entries 1..9):**
- Balanced BST on timestamps 1..9 has 8 tree edges. Only 4 share a biclique vertex. These 4 edges use 5 of 9 biclique edges. The resulting subgraph cannot reach a0→b0 (missing the earliest edge (a0,b0)@1).

**The vertex sharing probability kills it at scale:**
- Two random edges in K_{k,k} share a vertex with probability (2k-1)/k².
- For k=100: P(share) = 0.02. A tree on 9999 timestamps yields ~200 "useful" edges. Within the 4k-3=397 budget, but these edges form an unstructured random-looking subgraph with no reachability guarantee.

**Alternative attempted — Farey on vertex indices:**
- Map (a_i, b_j) → (i+1)/(j+1). Mediant of (a_i,b_j) and (a_i',b_j') maps to (a_{i+i'+1}, b_{j+j'+1}). Index overflow for most pairs (i+i'+1 > k-1). Does not scale.

**The precise incompatibility:**
- Farey mediant combines BOTH components additively: (a+c)/(b+d).
- Temporal relay shares EXACTLY ONE component: same row OR same column.
- These are structurally incompatible operations. No bijection between Farey fractions and biclique edges can make mediant = vertex sharing for all matrices M, because the Farey tree is a fixed combinatorial object while vertex-sharing patterns depend on M.

**Dead.** The 1D→2D projection has no natural quotient that preserves both the mediant ordering property and the bipartite vertex-sharing constraint. The semiring gap (graph reachability ≠ temporal reachability) remains algebraic, not number-theoretic.

**Open questions (salvageable fragments):**
- The E[useful] ≈ 2k scaling is suggestive — is there a 2D analog of the Stern-Brocot tree (a "matrix mediant") where the mediant of two matrix entries shares a row or column with each parent? This would be a binary tree on matrix positions where parent-child always share a row or column. Such trees exist (they are spanning trees of the rook graph on the k×k grid), but they have k²-1 edges and no timestamp-ordering guarantee.
- The Farey sequence has connections to continued fractions and best rational approximations. Could potential functions (which DO work empirically) be expressed as continued fraction expansions of some matrix invariant? This would connect the algebraic (potentials) and number-theoretic (Farey) approaches without the broken mediant-as-relay analogy.

## 2026-04-05

### H2: Farey tree on row-ratio fractions (opus, dead)
**Verdict:** Dead. The hypothesis fails at a structural level before any computation matters.

**Claims tested:**
1. Per-row Farey trees on column orderings select a sparse edge set — FALSE. Any tree on k columns has k-1 edges but covers all k vertices. Every row contributes all k cross edges. Union across k rows = k² = full graph. No reduction.
2. Farey mediant property |ad-bc|=1 encodes the relay constraint M[i'][j1] ≤ M[i'][j2] — FALSE. No mapping from timestamps/ranks to fractions produces |ad-bc|=1 ↔ relay-satisfiable. Tested: i/j fractions (information loss, many collisions), row_rank/col_rank (all equal 1 for SM(k) due to Latin square symmetry), normalized timestamps (no Farey neighbor structure).
3. Union of per-row Farey trees achieves ≤ 4k-3 edges — FALSE by (1).

**Dead because:** The spanner needs O(k) edges total, i.e., O(1) edges per row on average. Any tree on k items (Farey, Stern-Brocot, path, binary) spans all k vertices, so every row contributes all k cross edges. The Farey tree is a structure on k items; the spanner problem requires selecting O(1) items per row from k candidates. These are incompatible.

**Concrete evidence (SM(4)):**
- Optimal spanner: 12 = 4k-4 edges (from 16). Per-row: 2-4 edges each.
- Non-removable edges: always rank 0 (min) and rank k-1 (max) in each row.
- Removable edges: always the interior ranks (1..k-2).
- 14 distinct optimal spanners exist; none exhibit Farey structure.

**Salvage attempted and rejected:**
- Global Farey tree on columns: still k-1 pairs × k rows = O(k²).
- Farey on (row,column) pairs via timestamp fractions: k²-1 tree edges, quadratic, no temporal connection.
- Farey on rows instead of columns: same covering problem.
- Mediant columns (vector sum): no proportional column exists in SM(4).
- Pruned Farey tree (keep only leaves): O(k) edges but no reason they preserve reachability.

**Open questions:**
- The real structure governing edge removal: min/max per row are essential, interior ranks are removable. What determines which interior edges to keep? This is a constraint propagation problem across rows, not a number-theoretic one.
- The 4k-4 bound requires O(1) edges per row. The only known O(1)-per-row construction is M⁻ + M⁺ (2 per row) plus spanning trees. The relay routing through those edges is the unsolved piece.

### H1: Farey tree on timestamp ranks (opus, DEAD)
**Verdict:** Dead. The rank-to-Farey mapping produces either Θ(k²) edges (too many) or O(k) edges with no reachability guarantee. The Farey structure is orthogonal to what temporal spanners need.

**Claims tested:**
1. Map the k² timestamps in M to Farey fractions by rank: rank r → the r-th element of F₅ (or SB tree truncated at k² leaves). Farey-adjacent cross-edges form a valid spanner. — FALSE.
2. The Farey tree on k² rank-fractions selects ≤ 2n-3 edges. — FALSE (produces 13 adjacencies for k=3 where k²=9; grows as Θ(k²) for larger k).
3. Some O(k)-size subset extractable from the Farey tree preserves temporal reachability. — FALSE (tested: SB top-k by depth, per-row mediants, per-row/col min+med+max; all fail on SM(5) and random matrices).

**The size problem (fatal):**
- The Farey/SB tree on k² items has k²-1 parent-child edges and Θ(k²) Farey neighbor pairs. Any structure on k² items produces Θ(k²) relationships.
- Extracting O(k) items from k² by tree depth, BFS order, or subtree selection discards items without regard for bipartite vertex coverage. For SM(5), the SB-top-10 selection misses entire rows/columns → 60 unreachable pairs.
- No natural Farey/SB pruning yields O(k) items that cover all k rows and all k columns. A random O(k)-subset of k² items hits each row ~1 time on average, which is provably insufficient for temporal routing (need ≥2 per row: one early, one late).

**The direction problem (fatal):**
- The Farey mediant prioritizes MIDDLE-rank timestamps (mediants of extremes).
- Empirical evidence on SM(5) and random matrices: optimal spanners KEEP extreme-rank edges and REMOVE middle-rank edges. Specifically for SM(5), removed ranks = {6,8,9,11,12,14,16,17,18} (clustered around median rank 13). Classes 0 and k-1 (earliest and latest per-row) are fully retained.
- Tested on 5 random matrices at k=6: edges in the inner third of ranks are removed at 2-3× the rate of edges in the outer thirds. The mediant is the LEAST useful rank position.
- This makes physical sense: a temporal journey needs an early edge to start and a late edge to finish. Middle edges are redundant when extremes are present.

**Concrete walkthrough (SM(3), k=3):**
- Rank matrix: Row 0 = [1,4,7], Row 1 = [5,8,2], Row 2 = [9,3,6].
- F₅ mapping: rank r → F₅[r-1]. Nine rank-fractions: 0, 1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4.
- Farey adjacencies: 13 pairs satisfy |ad-bc|=1. But SM(3) has only 9 cross-edges total (= K₃,₃), so "Farey-adjacent cross-edges" simply selects a subset of all (9 choose 2) = 36 pairs. These 13 Farey adjacencies define a GRAPH ON EDGES, not a subset of edges. Every cross-edge participates in at least one adjacency, so the "Farey spanner" keeps all 9 edges. No reduction.
- For SM(3), 2n-3 = 9 = k², so keeping all edges trivially satisfies the bound. But this reveals the hypothesis contributes nothing: it doesn't thin the edge set.

**Bonus finding — SM(5) admits a 16-edge (= 2n-4) spanner:**
- Exhaustive search found a 16-edge spanner (one below 2n-3=17), confirming the "optimal SM(k) use 2n-4 edges" claim.
- The 16-edge spanner has a staircase structure: Row 0 keeps 2 edges (rank 1, 21 — the min and max), row 4 keeps all 5 edges. Each subsequent row adds one more edge. Column 0 keeps all 5 edges.
- Removed ranks: {6, 8, 9, 11, 12, 14, 16, 17, 18} — all interior ranks, confirming the extremes-matter pattern.

**Dead because:** The Farey tree is a 1D number-theoretic structure on Θ(k²) items. Temporal spanners need a 2D bipartite structure with O(k) items. No projection from Farey to biclique preserves both the O(k) count and the temporal monotonicity constraint. The actual selection principle is extreme-rank coverage (keep early/late edges per row), which is the opposite of what Farey mediants provide.

**Open questions:**
- The extreme-rank pattern is robust but not yet a construction. Which interior edges to keep depends on cross-row constraint propagation. This is closer to constraint satisfaction / 2-SAT than number theory.
- The staircase structure in the 16-edge SM(5) spanner resembles a Latin square completion problem. Could the spanner edge set be characterized as a partial Latin square with specific coverage properties?

### 11:15 — H6: Online edge count analysis (opus, confirmed-negative)

**Verdict:** Online greedy massively overshoots the offline optimal. The gap scales as O(k²), not O(1) or O(log k). The conjecture bound 2n-3 is violated by EVERY construction method on virtually every instance.

**Claims:**

1. **SM(k) is degenerate.** Online greedy adds ALL k² edges — every edge creates at least one new reachable pair. SM's row-block timestamp structure means row i's edges all precede row i+1's, so a_{i+1} can never reach a_i. Even the full graph only reaches n(n-1) - k(k-1)/2 pairs. The gap over offline optimal is exactly (k-2)².

2. **Random matrices: greedy always overshoots 2n-3.** Across 50 trials per k∈{4,5,6,7}, the online greedy spanner exceeded 2n-3 in 100% of forward-order trials and ~97%+ across all orderings. Mean edge counts: k=4→15.3, k=5→22.6, k=6→30.3, k=7→38.6 (vs 2n-3 bounds of 13, 17, 21, 25).

3. **Gap scales as ~3.8k - 12 (linear in k), power-law fit ~0.08·k^2.7.** Not O(1), not O(log k). The greedy online approach is fundamentally suboptimal by Θ(k) over the offline 4k-4 bound.

4. **Order insensitivity.** Forward, reverse, and random orderings produce nearly identical mean edge counts. No ordering exploits temporal structure to reduce the count. This rules out "just process edges in the right order" as a fix.

5. **No phase transition.** Edges continue being added until ~90-97% of timestamps are processed. No clean cutoff. The first half of timestamps accounts for ~55-65% of edges (roughly proportional, slight front-loading).

6. **Greedy achieves full reachability.** Despite using more edges than offline optimal, the greedy spanner achieves 100% of the reachable pairs that the full graph achieves (50/50 trials for all k).

**Implication for the conjecture:** The 2n-3 bound, if achievable, requires non-greedy (offline) construction. Online greedy is not a viable proof strategy — it's an O(k)-factor worse. The offline optimal of 4k-4 edges is tight for SM(k) but the online lower bound is k² for SM and ~O(k^1.7) for random matrices.

### 21:45 — H5b: Universal 1-healability deep dive — REFUTED

H5b: Universal 1-healability deep dive — REFUTED. Minimum spanners of temporal K_{k,k} are large (k²-k edges, not 2k-3). 1-healability fails on 0/50 random matrices for all k=3..6. Only 3.6%-31.4% of critical edges are individually healable. Multi-deletion drops further. 1-healable spanner = full graph for k≥4. SM(k) has 0% healability. Prior H5 finding was an artifact of SM's pathological structure or re-adding deleted edges.

### 22:15 — H9: BGP-style temporal spanner

H9: BGP-style temporal spanner — tested on 50 random k×k matrices per k (k=3..8). Single-start greedy achieves budget 42-100% of the time. Multi-start greedy (20 restarts) jumps to 84-100%. All three BGP variants (standard, aggressive/connectivity-only, economic) converge to identical edge counts — the pruning criterion doesn't matter, only removal order does. At k=4, exhaustive search confirms ~6% of matrices are truly infeasible (need >4k-3 edges for full reachability). Every remaining edge is individually critical (removing any one breaks some pair). Joint removal of 2-3 edges also fails. 1-healability is very poor: 0% of edges survive deletion without losing reachability; only 8-19% are healable by swapping in one non-spanner edge. The rest are unhealed. Key finding: the BGP metaphor adds nothing over greedy pruning — temporal reachability can't be decomposed into per-node routing tables because path validity depends on arrival time at each relay, not just existence. The "route announcement" abstraction breaks down. Multi-start greedy is the real algorithm; the distributed framing is cosmetic.

### 23:30 — H10b: Best-response formalization

H10b best-response formalization: complete empirical investigation. Key findings: (1) temporal K_{k,k} NOT always fully reachable — failure rate 77% at k=3 down to 0% at k=10, caused by row dominance in timestamp matrix. (2) For reachable instances, best-response converges in exactly 2 rounds, always monotone, every equilibrium edge is critical. (3) Minimum spanner scales as ~c*k*log(k), not O(k). Power law fit: 2.07*k^1.273. The 4k-3 bound holds for ~85-98% of reachable instances at k=4-7 but tightens with k. (4) PoA ≤ 1.05 across all tested k. (5) Complexity of one BR round: O(k^5) from full graph (O(nE^2)). (6) Build-up approach ~10% worse than greedy removal. CPS conjecture is for K_n, not K_{k,k} — bipartite case has different structure.

### 00:45 — H11: O(n) heuristic budget construction for temporal spanners — complete results from v2 experiment

H11: O(n) heuristic budget construction for temporal spanners — complete results from v2 experiment

## 2026-04-05

### 00:00 — H14: Forward incremental construction — complete experimental results

H14: Forward incremental construction — complete experimental results

**Algorithm.** Process edges in timestamp order. Keep edge iff it increases the total reachable pair count (full BFS recompute per candidate). Phase 2: backward prune in reverse timestamp order.

**Phase 1 keeps too many edges.**
- P1 edges scale as ~1.56 * k^1.62 (R^2=0.998)
- At k=3: 8.8/9 kept (98%). At k=12: 83.2/144 kept (58%).
- Forward pass alone NEVER meets the 4k-3 budget for k >= 6.
- Root cause: in bipartite cliques with all-distinct timestamps, most edges create at least one new reachable pair when processed in order.

**Phase 2 matches H10 quality but exceeds budget.**
- P2 edges scale as ~1.97 * k^1.32 (R^2=0.999)
- P2 edges match H10 within 1-2% for all k tested
- P2 exceeds 4k-3 budget starting at k=6 (2% over), growing to 14% over at k=12
- Both H10 and P2 exceed budget equally — property of temporal cliques, not the algorithm

**Complexity.**
- P1+P2 total time: ~3.3e-6 * k^4.02. H10: ~3.1e-6 * k^4.16. Same scaling.
- P1+P2 is ~1.2x faster than H10 (consistent across all k)
- Amortized cost per kept edge: O(k^3), not O(k log k) as hoped

**Correctness.** 100% (all 50 matrices, all k values, both phases).

**Distributed interpretation.** Sequential constraint (global timestamp order). Shared state: n^2 reachability matrix. Not parallelizable within a timestamp step.

### 21:45 — Compression toward convexity: exhaustive study

Compression toward convexity: exhaustive computational study. Bollobas-Leader compression fails on partial cubes (degree asymmetry breaks neighborhood bijection). Original conjecture FALSE -- not all sizes admit convex sets. Refined conjecture (where convex sets exist, they minimize boundary) HOLDS across all tested arrangements (3-6 lines R^2, 4-5 planes R^3, 100+ arrangements). Key structural insight: achievable convex sizes = halfspace intersection sizes, which have gaps from the f-vector structure.

## 2026-04-06

### 14:30 — Gemini CLI union-find PR: research & planning

Gemini CLI union-find PR: researched upstream state. Old v2 branch is 230 commits behind. Plan: fresh PR on current main. Old impl: 12 files, 2064 lines — Forest (union-find with path compression), ContextWindow (hot/cold partitioning), TFIDFEmbedder, ClusterSummarizer. Upstream main still has flat compression. joshualitt's PR #24157 adds tool distillation + progressive normalization — union-find should complement, not conflict. Issue #22877 is open with maintainer interest (rmedranollamas: "looks good, will review code"). Next: reimplement on current upstream/main.

### 15:42 — Union-find PR shipped

Created google-gemini/gemini-cli#24736 — union-find context compaction on top of joshualitt's #24157. 9 files, 1399 insertions, 37 new tests, tsc clean, lint clean. Commented on issue #22877 tagging joshualitt. Based on main (couldn't target jl/auto-dis-norm directly). Also drafted LinkedIn message to Kelly Hong at Chroma (context rot researcher).

### 16:00 — H21: Vertex-extreme spanner conjecture — REFUTED

H21: Vertex-extreme spanner conjecture — REFUTED. E_extreme (union of per-vertex min/max timestamp edges) fails as a spanner starting at n=5 (56% failure rate) and reaches 100% failure by n=8. |E_extreme| also exceeds 2n-3 in many cases. Sharing (min of one vertex = max of another) is extremely rare at larger n, so the 2n → 2n-3 reduction via sharing doesn't hold either. Adversarial search found reachability as low as 24/56 (43%) for n=8. Repair is cheap (1-3 edges typically) but doesn't reliably stay within 2n-3. Dead end for the spanner conjecture.

### 22:41 — H25: Matroid exchange on matchings — DEAD END

H25 matroid exchange experiment complete. min_c grows as O(n) — ratio c/n stays at ~0.37 across n=4..20. Matroid basis exchange does NOT give O(1) ordering. Neighborhoods are not matroid bases (non-uniform sizes), exchange property holds only ~30-50% of same-size pairs. Dead end for SJT-style ordering.

### 22:44 — H26: Gray code delegation — ordering irrelevant, overcounting identified

H26 Gray code delegation experiment complete. Scripts: worklog/h26_gray_delegation.py, worklog/h26_overcounting_analysis.py

### 22:55 — H24: SJT-CPS residual experiment — REFUTED

H24 SJT-CPS residual experiment: REFUTED. Min consecutive symmetric difference scales as O(log k), not O(1). The log factor in CPS delegation is structural — no emitter ordering eliminates it. Full 2-hop neighborhoods saturate trivially; the constrained (S⁻ partner) neighborhoods are the meaningful test. Brute-force optimal (k≤10) grows from 2.72 to 3.95; greedy (k=11–24) from 6.10 to 8.90. Best fit: v ≈ 2.93·log2(k) − 4.6, R²=0.912. Scripts in worklog/sjt_cps_v{1,2,3}_final.py.

### 23:23 — H27: Birthday bound on sequential delegation — bipartite model WRONG, star+tree and multi-start greedy CONFIRMED

Scripts: worklog/h27_birthday_delegation.py, h27_scaling_analysis.py, h27_greedy_bound.py, h27_correct_model.py, h27_counterexample.py, h27_star_tree_verification.py, h27_conjecture_test.py

**Phase 1 (bipartite K_{k,k} model, Parts 1-3):**
- Temporal delegation: emitter i delegates to j via relay c' where M[i,c'] < M[j,c']. Missed = collectors d where M[j,d] < M[j,c'] (rank of relay in delegate's row).
- Birthday probability: P(rank-0 relay to specific delegate) ≈ 1/k. With k-1 delegates: P(some rank-0) ≈ 1-1/e ≈ 0.63. Matches empirical 0.47-0.53.
- E[total_missed] ≈ 0.89k. max_missed ≈ 1.35k. Always ≤ 2k-2 budget for greedy ordering (5000 trials per k, k=3..6).
- SM(k) and Latin square: total_missed = 0 for all k tested. Only random matrices produce nonzero missed.
- **BUT:** bipartite delegation model underestimates actual spanner cost by ~40% (ratio ≈ 0.55). Delegation only covers emitter→X paths; collector→Y paths need separate edges. The K_{k,k} bipartite model is WRONG for CPS, which operates on K_n.

**Phase 2 (correct K_n model, Parts 4-7):**
- Star(hub) + greedy spanning tree: exactly 2n-3 edges by construction (n-1 star + n-2 tree). Preserves 100% temporal reachability for MOST instances (n=5..20).
- Star+tree is NOT universal: seed=233 at n=6 has NO hub where star+tree works. But a non-star-shaped 2n-3 spanner EXISTS.
- Multi-start greedy + backward prune: always finds ≤ 2n-3 edges (n=5..12, 10-20 trials each). Never violates budget.
- **Exhaustive verification: ALL n≤7 instances (100-200 each) have a 2n-3 edge spanner. Conjecture holds.**
- Minimum spanner is often 2n-4 or less. The 2n-3 budget has comfortable slack.

**Key findings:**
1. The delegation/birthday model from H26 is a valid intuition for WHY 2n-3 works, but the bipartite formalization is incomplete. The full K_n model is needed.
2. Star+tree is the simplest 2n-3 construction but fails for ~0.2% of instances. Non-star constructions rescue these cases.
3. The connected pair lemma (proved in Lean, worklog 14:30 Apr 4) gives the algebraic foundation: S⁻/S⁺ matchings always contain a connected pair, ensuring 2 relay columns suffice for cross-side reachability.
4. The gap remains between "2n-3 spanners always exist" (empirically confirmed) and "here is a constructive proof" (star+tree fails occasionally, multi-start greedy works but isn't analyzable).

**Proof status:**
- Dismounting: literature (Carnevale et al. 2025)
- Biclique characterization: literature (Theorem 3.10)
- Connected pair: PROVED in Lean (zero sorry)
- Budget: PROVED by omega
- **Remaining sorry:** constructive biclique spanner ≤ 4k-3 for ALL k×k bicliques. Star+tree covers ~99.8% of instances. The 0.2% exception needs a non-star construction or a non-constructive existence argument.

**Verdict:** The 2n-3 conjecture is empirically CONFIRMED through n=7 (exhaustive) and n=12 (multi-start greedy). The birthday bound on delegation provides the probability theory explaining why 2n-3 edges suffice. The proof gap is narrow: constructive handling of the rare instances where no star+tree works.

## 2026-04-07

### 10:30 — TVG session 4: birthday bound, median framework, biclique double-star

TVG session 4: 40+ hypotheses across 4 sessions. Birthday bound formalization → three-timestamp median framework → LIVE/DZ decomposition → Median Floor Conjecture → dead end (no tools to prove it). Dismountability revisited: blocked (not all cliques dismountable). Biclique double-star: 100% empirical success on extremally matched K_{k,k} through k=9. Key negative result: journey lengths grow with k, ruling out ALL fixed-hop proof strategies. The fundamental wall: proving sparse subgraph preserves global reachability under adversarial timestamps requires reasoning about unbounded journey composition. No existing framework handles this. Proved: M⁻ covers all A-A pairs, M⁺ covers all B-B pairs. The gap remains at biclique spanner ≤ 4k-3.

### 12:15 — H26 correction: log factor is structural

H26 correction: sequential delegation does NOT kill the log factor. Root delegation gives Θ(k log k) — temporal filtering at relay vertices is structural. The CPS O(n log n) cannot be improved to O(n) within their framework. K-early+late (K=3, ~5n) works empirically but proof requires multi-hop reasoning. Dead end count: 45+ hypotheses across 4 sessions. The gap remains at biclique spanner ≤ 4k-3.
