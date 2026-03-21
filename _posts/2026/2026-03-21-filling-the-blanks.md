---
layout: post-wide
title: "Filling the Blanks"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Missing Parts](/the-missing-parts).*

### Near-misses

[The Missing Parts](/the-missing-parts) found seven blank cells in the design-space grid: places where the axes name a contract and the literature has nothing that satisfies it. But "nothing" overstates the gap. For three of the seven, existing work got close. A paper identified the right problem, or solved a restricted version, or built the machinery but aimed it at a different target. The blank isn't empty. It has a near-miss.

The pattern: find the near-miss, name what it didn't do, patch that one thing.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col style="width:14em"><col style="width:10em"><col style="width:14em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Cell</th><th style="background:#f0f0f0">Near-miss</th><th style="background:#f0f0f0">What it didn't do</th><th style="background:#f0f0f0">Patch</th></tr></thead>
<tr><td>Graph × Dominance</td><td><a href="https://openproceedings.org/2013/conf/edbt/MagnaniA13.pdf">Magnani & Assent (2013)</a> — probabilistic fix for overlap</td><td>Factor out shared members</td><td>Residualize: compare marginal contributions only</td></tr>
<tr><td>Partial order × Causal</td><td><a href="https://proceedings.neurips.cc/paper_files/paper/2022/file/3103b25853719847502559bf67eb4037-Paper-Conference.pdf">Staggered rollout</a> — temporal order on treatment</td><td>Poset structure on prerequisites</td><td>Treatment unit = downward closure <code>↓{x}</code></td></tr>
<tr><td>Attend × Partial order</td><td><a href="https://en.wikipedia.org/wiki/Phylogenetic_diversity">Phylogenetic diversity</a> — tree-spread selection</td><td>Generalize beyond trees</td><td>Jaccard on poset context as MMR kernel</td></tr>
</table>

Each patch is [implemented and tested](https://github.com/kimjune01/filling-the-blanks) against its contract (is output strictly smaller? is the bound respected?) and reduction cases (does it collapse to the known algorithm when structure vanishes?). The tests don't prove usefulness on real data.

### 1. Residualized dominance

*The near-miss.* Dominance filtering asks: does item A beat item B on every objective? The skyline literature has this for [sequences](https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z) (2013) and [non-overlapping subgraphs](https://weiguozheng.github.io/pub/tkde16-skyline.pdf) (TKDE 2016). [Magnani & Assent (EDBT 2013)](https://openproceedings.org/2013/conf/edbt/MagnaniA13.pdf) got closest to the overlapping case: they showed that naive aggregation over shared members misleads and proposed a probabilistic fix. But they redefined dominance to tolerate overlap. They didn't factor it out.

*The failure mode.* Three research groups share a star postdoc (output: 50 papers). Group A has the postdoc plus a junior researcher (2 papers). Group B has the postdoc plus a senior researcher (8 papers). Raw objectives: A = 52, B = 58. B dominates A. But the real question is whether B's *unique* contribution beats A's. Residuals: A contributes 2, B contributes 8. B still dominates — but now imagine Group C also has the postdoc, with objectives 51. Raw: C looks nearly tied with A (52 vs 51). Residuals: C contributes 1 vs A's 2. A dominates C. Without residualization, the 50-paper postdoc makes all three groups look similar. With it, the marginal differences are exposed.

*The algorithm.* Factor out shared substructure before comparing. For communities `C₁` and `C₂` with overlap `I`, decompose into residuals `R₁ = C₁ \ I` and `R₂ = C₂ \ I`, then compare only the marginal contributions:

> `C₁ ≤ C₂` iff `g(R₁ | I) ≤ g(R₂ | I)` on every objective, strictly on at least one.

where `g(R | I)` is the additive marginal contribution of the residual members given the shared base.

The skyline literature's response to overlap has been to redefine dominance probabilistically or ignore it. Residualizing hasn't appeared in the skyline literature.

*Filter implementation.* Estimate overlap via minhash sketches. Compute residual bounds from sketch intersection sizes. Prune pairs where the upper bound of one residual is dominated by the lower bound of the other. Only resolve ambiguous pairs exactly. Error guarantee comes from the sketch's collision bound.

*Reductions.* No overlap → residuals equal the full communities → standard group skyline. Singleton communities → ordinary Pareto dominance. Both cases pass in the [test suite](https://github.com/kimjune01/filling-the-blanks).

### 2. Closure-level causal effects

*The near-miss.* Causal filtering on flat data is solved: [conformal causal selection](https://doi.org/10.1515/jci-2023-0059) (Duan, Wasserman & Ramdas 2024) gates items by treatment effect with bounded FDR. But flat data assumes pointwise treatment. Partial orders break this. In a poset where a ≤ b means "a is a prerequisite for b," treating b requires first treating everything below it.

Three lines of work got close. [Staggered rollout designs](https://proceedings.neurips.cc/paper_files/paper/2022/file/3103b25853719847502559bf67eb4037-Paper-Conference.pdf) impose temporal order on treatment adoption (once treated, always treated), but the order is total, not a poset over prerequisites. [Shpitser & Tchetgen Tchetgen (2016)](https://doi.org/10.1214/15-AOS1411) define hierarchical interventions, but the hierarchy is over causal pathways, not treatment bundles. [Manski (1997)](https://doi.org/10.2307/2171738) assumes monotone treatment response, but as a constraint on outcomes, not on which bundles are feasible.

*The failure mode.* An org chart: CEO ≤ VP ≤ Engineer. You want to know whether training the Engineer improves output. But training the Engineer requires first training the VP (who supervises), which requires training the CEO (who approves the budget). The standard ATE asks: "what's the effect of training the Engineer?" The closure-level estimand asks: "what's the effect of training {CEO, VP, Engineer} vs the status quo?" — because that's the actual intervention. Pointwise ATE misattributes the VP's and CEO's contributions to the Engineer.

*The estimand.* The order runs upward: a ≤ b means a is below b, a must be treated before b can be. Treating node `x` means treating its entire downward closure: `T(x) = ↓{x} = {y : y ≤ x}`. The causal effect is:

> `τₓ = E[Y(S₀ ∪ T(x)) − Y(S₀)]`

where `S₀` is the baseline treated set. Intervening at a leaf is cheap (small closure). Intervening near the root treats an entire branch.

*The patch.* Make the treatment unit a downward closure. Existing causal inference assumes the treatment is a binary toggle on a unit. Here the treatment is a set determined by the order structure.

*The central limitation.* Identification requires positivity over feasible closures: you must observe both treated and untreated versions of each closure. Deep posets have large closures with thin support, so the deeper the intervention point, the fewer observations where that closure was untreated. Shallow posets have tractable closures. Deep chains may not.

*Estimation.* The modeling recipe is standard once you have the estimand: isotonic outcome models, propensity scores over feasible closures, [Benjamini-Hochberg](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Hochberg_procedure) for FDR control. The hard part is identification, not estimation. Whether you can actually observe enough untreated closures to identify `τₓ` depends on the poset's shape and the treatment adoption process. The recipe is a sketch, not a settled pipeline.

*Reductions.* Discrete poset (no edges) → closures are singletons → standard ATE per node. Tree poset → closures are subtrees → natural intervention unit for hierarchical policies (treat a department = treat everyone in it). Both cases [tested](https://github.com/kimjune01/filling-the-blanks).

### 3. Diverse top-k from a poset

*The near-miss.* Attend requires: output a bounded-size set that is ranked by relevance and diverse. On flat data, [MMR](https://doi.org/10.1145/3130348.3130369) and [DPP](https://arxiv.org/abs/1207.6083) deliver this by defining diversity as distance in a metric space. Partial orders have reachability, not distance. [Phylogenetic diversity](https://en.wikipedia.org/wiki/Phylogenetic_diversity) (Faith 1992) got closest: it selects species to maximize total branch length on a tree, using the tree structure itself as the diversity measure. But it's restricted to trees, uses branch-length sums, and hasn't been generalized to arbitrary posets. [Hu et al. (CIKM 2015)](https://dou.playbigdata.com/publication/2015_CIKM_DivByHieIntent.pdf) diversify search results over a hierarchy of intents, but the hierarchy provides coverage targets, not a similarity kernel.

*The failure mode.* A taxonomy: Math ≤ Algebra ≤ Linear Algebra, Math ≤ Geometry ≤ Topology. Pick 2 topics for a study guide. Relevance-only top-k picks Linear Algebra and Topology (highest demand). But those sit on separate branches — that's actually *good* diversity. Now suppose it picks Linear Algebra and Algebra instead. One subsumes the other. That's redundant. Without order-aware similarity, the algorithm can't tell the difference: both pairs look equally "far apart" because there's no metric, only reachability.

*The kernel.* Define similarity from order context:

> `Sim(x, y) = α · J(↓x, ↓y) + β · J(↑x, ↑y) + γ · C(x, y)`

where `↓x` and `↑x` are the downset and upset (all elements below/above x), `J` is Jaccard similarity, and `C(x, y)` is a comparability term (1 if one element is above the other, 0 otherwise). Diversity is the complement: `D(x, y) = 1 − Sim(x, y)`.

Downset overlap measures shared ancestry. Upset overlap measures shared descendants. The comparability term penalizes selecting both x and its ancestor, since one subsumes the other. The linear combination is a heuristic (a principled choice would need a task-specific loss function), but it has useful boundary behavior: zero for disjoint context, one for identical items, tunable weights for ancestry vs. descent.

*The patch.* Generalize from trees to posets by replacing branch length with Jaccard on order context. [simona](https://doi.org/10.1186/s12864-024-10759-4) (Gu 2024) uses Jaccard on ancestor sets for biomedical ontologies, but only as a comparison tool. Plugging the symmetric formulation into an MMR loop with a diversity contract is the new step.

*Implementation.* MMR-style greedy: at each step, select the element maximizing `(1 − λ) · relevance(x) − λ · max_sim_to_selected(x)`. Higher `λ` pushes harder toward diversity. `λ = 0` recovers pure relevance ranking. The greedy loop is `O(k·n)` per selection round, with similarity computed from precomputed downsets and upsets.

*Reductions.* Discrete poset → all pairwise similarities are zero → pure relevance top-k. Total order → adjacent elements are maximally similar → selections spread across the ranking. In a tree, the algorithm picks from different branches before doubling up within one. All cases [tested](https://github.com/kimjune01/filling-the-blanks).

### What patching tells us

Three near-misses, three patches. No new formalism. Each is an adaptation that existing work came close to but didn't make, because the combination wasn't named.

They're not equally robust.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:10em"><col style="width:12em"><col style="width:14em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Patch</th><th style="background:#f0f0f0">Robustness</th><th style="background:#f0f0f0">Limitation</th><th style="background:#f0f0f0">Viable when</th></tr></thead>
<tr><td>Residualize</td><td>Strong</td><td>Sketch accuracy (computational)</td><td>Any overlapping communities</td></tr>
<tr><td>Closure estimand</td><td>Conditional</td><td>Positivity over closures (statistical)</td><td>Shallow posets, wide trees</td></tr>
<tr><td>Poset kernel</td><td>Heuristic</td><td>Weight choice is design, not derivation</td><td>Any poset with exploitable context</td></tr>
</table>

Residualized dominance is the most straightforward: the limitation is only computational. Closure-level causal effects have the strongest conceptual bite, but the positivity requirement may kill it for deep posets. The poset diversity kernel is well-behaved at the boundaries but the interior depends on weight tuning.

The grid's role was making the near-miss findable. Without it, you'd never cross-reference skyline queries with community overlap, or staggered rollout with poset structure, or phylogenetic diversity with MMR.

Three cells brought into candidate form: one strong, one conditional, one heuristic. The [Parts Bin](/the-parts-bin) gets closer to what it promised: given a broken step, look up the fix.

### Sketches for the remaining blanks

Five cells have no near-miss close enough to patch with one operation. Each needs a definition or a composition from further-apart literatures. These are sketches, not implementations.

**4. Sequence × Causal (bounded).** Define interference via embedding distance between segments: treating segment *i* spills over to nearby segments with weight *w_ij* = K(d(i,j)). Estimate per-segment effects with a doubly robust score under an exposure mapping ([Aronow & Samii 2017](https://isps.yale.edu/research/publications/isps18-01)). Get valid p-values via randomization inference. Apply [BY](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/6791919) for FDR control under arbitrary dependence. Minor variation of spatial causal inference + classical FDR.

**5. Tree × Dominance (bounded).** Define subtree A to dominate subtree B if the empirical distribution of leaf utilities in A first-order stochastically dominates that of B: F_A(t) ≤ F_B(t) for all thresholds t, after depth-normalization. Test each pair with simultaneous confidence bands on F_A − F_B. Organize pairwise hypotheses on the tree and run hierarchical FDR top-down ([Yekutieli 2008](https://cris.tau.ac.il/en/publications/hierarchical-false-discovery-rate-controlling-methodology)). Novel definition — stochastic dominance over leaf CDFs hasn't been applied to subtree comparison.

**6. Partial order × Similarity (bounded).** Replace metric distance with order-context overlap: s(x,y) = λ·J(↓x,↓y) + (1−λ)·J(↑x,↑y), where J is Jaccard on principal ideals/filters. Compute sketches via [MinHash](https://ieeexplore.ieee.org/document/666900). The "radius" becomes a similarity threshold τ. Test H_x: s(q,x) < τ using sketch confidence bounds. Keep discoveries after BH/BY. Novel — set-similarity search on order context hasn't been formalized as a filter.

**7. Embedding × Causal (bounded).** Each item has treatment Z_i, outcome Y_i, and cannibalization exposure S_i = Σ K(‖e_i − e_j‖)Z_j from embedding distance. Estimate direct effects net of interference with a generalized propensity estimator ([Giffin et al. 2023](https://pubmed.ncbi.nlm.nih.gov/35996756/)). Produce valid p-values by sample splitting. Apply BY. Minor variation — spatial causal interference applied to embedding geometry.

**8. Learned codebook × Stream (Perceive).** Keep an append-only merge DAG: existing token IDs never change. Track candidate new merges with streaming heavy-hitters over adjacent pairs. Add a new token only if compression gain exceeds a threshold and activation is forward-only. Retokenize only inside a rolling checkpoint buffer of size W; older text keeps its old tokenization. Backward compatibility is exact (append-only). Retokenization rate is bounded (buffer size). Novel composition — existing work adapts vocabularies ([Chizhov et al. 2024](https://aclanthology.org/2024.emnlp-main.925/), [Li et al. 2025](https://aclanthology.org/2025.acl-long.207/)) but none guarantees all three: online updates, backward compatibility, bounded retokenization.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:8em"><col style="width:14em"><col style="width:14em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Cell</th><th style="background:#f0f0f0">Novelty</th><th style="background:#f0f0f0">Near-miss</th><th style="background:#f0f0f0">What's new</th></tr></thead>
<tr><td>Sequence × Causal</td><td>Minor variation</td><td>Spatial causal inference + FDR</td><td>Apply to time-series segments</td></tr>
<tr><td>Tree × Dominance</td><td>Novel</td><td>Stochastic dominance + hierarchical FDR</td><td>Dominance defined over leaf CDFs</td></tr>
<tr><td>Partial order × Similarity</td><td>Novel</td><td>MinHash + set-similarity search</td><td>Jaccard on order context as filter</td></tr>
<tr><td>Embedding × Causal</td><td>Minor variation</td><td>Spatial interference + FDR</td><td>Apply to embedding cannibalization</td></tr>
<tr><td>Learned × Stream</td><td>Novel</td><td>Adaptive BPE, TokAlign</td><td>Append-only DAG + bounded retokenization</td></tr>
</table>

---

*Written via the [double loop](/double-loop).*
