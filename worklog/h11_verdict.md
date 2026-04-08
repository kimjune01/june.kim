### H11: Heuristic budget construction (opus, negative)

**Verdict:** The O(n) heuristic construction fails to produce competitive temporal spanners. All four variants require either (a) budgets exceeding 4k-3 to achieve reliable reachability, or (b) an expensive O(k^6) repair pass that defeats the purpose of an O(n) heuristic.

**Claims:**

1. **Construction is genuinely O(n) but insufficient alone.** All variants (A: column popularity, B: timestamp spread, C: column coverage, D: combined) run in O(k) per node with 1 round of neighbor announcements. At budget c=2.0 (5 edges/node for k≥5), heuristic-only reachability is 86-98% of pairs — never 100% for k≥6. No variant achieves ≥95% of matrices with full reachability at c≤2.0 for k≥6 without repair.

2. **Repair restores reachability but kills the complexity advantage.** 1-round global repair (add edge if it increases total reachable pairs) brings success to 94-100% at c=2.0. But repair checks each of O(k²) missing edges against O(k) reachability queries costing O(k² log k) each — total O(k^5 log k), comparable to H10's best-response dynamics. The "O(n) heuristic" is really "O(n) seed + O(n^2.5) repair."

3. **Edge overhead is 1.4-1.7x vs best-response (H10).** At the minimum c achieving ≥95% repair success:
   - k=5: C uses 21.3 edges vs H10's 16.3 (1.31x), budget 17
   - k=6: C uses 28.1 edges vs H10's 20.6 (1.36x), budget 21
   - k=7: C uses 35.5 edges vs H10's 24.7 (1.44x), budget 25
   All exceed the 4k-3 budget by 1.3-1.5x.

4. **Variant ranking:** C (column coverage) ≥ B (timestamp spread) > D (combined) > A (popularity). C achieves ≥95% repair success at the lowest c for most k. B has best heuristic-only reachability. D underperforms both B and C despite combining their signals — the product scoring is suboptimal.

5. **Budget threshold: c=3.0 is trivially correct.** At c=3.0, floor(3·ln(k))+2 ≥ k for all tested k, meaning the heuristic keeps ALL edges. Full reachability is guaranteed but useless — no spanner is produced. The interesting regime (c=1.0-2.0) never achieves competitive results.

6. **Failure type distribution:** BB pairs fail most often (28-41% of failures), followed by AB and BA (~25% each), then AA (6-24%). Column coverage (C) produces the most balanced failure distribution, suggesting it best addresses the structural bottleneck.

7. **The fundamental problem:** Local information (row min/max, column popularity) cannot predict which edges serve as temporal relays. An edge's relay value depends on the GLOBAL timestamp structure — whether it sits between two other edges' timestamps in a way that enables multi-hop journeys. This is inherently a non-local property. The min+max anchor is necessary but the interior edge selection is essentially random with respect to actual relay utility.

**Bottom line:** No O(n) heuristic tested here comes close to H10's O(n^2.5) best-response quality. The gap is structural: temporal spanner construction requires knowing which edges form relay chains, and relay chain membership is a global property. Column coverage (C) is the best variant but still needs 1.4-1.5x the optimal edge count even after expensive repair. The O(n) dream is dead for temporal bipartite cliques.
