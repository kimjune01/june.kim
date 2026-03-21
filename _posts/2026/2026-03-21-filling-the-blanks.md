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

### 4. Spillover-adjusted causal segments

**The near-miss.** Causal filtering on flat data is solved ([Duan et al. 2024](https://doi.org/10.1515/jci-2023-0059)). [Aronow & Samii (2017)](https://isps.yale.edu/research/publications/isps18-01) handle interference via exposure mappings. But nobody has composed interference-aware causal estimation on time-series segments with FDR control.

**The failure mode.** A marketing team runs promotions on different weeks. Week 3 gets a promotion, but weeks 2 and 4 also see a lift because customers shift purchases to adjacent weeks. The standard per-segment test attributes the full lift to week 3. The spillover-adjusted version estimates week 3's *direct* effect after removing the interference from neighboring treated weeks.

**The algorithm.** For each segment i with treatment Z_i and outcome Y_i:

1. Compute spillover exposure: S_i = Σ K(d(i,j)) · Z_j, where K is a Gaussian kernel over segment distance.
2. Regress outcomes on (Z_i, S_i) to separate direct effect from spillover.
3. Compute per-segment p-values from the adjusted estimates.
4. Apply [Benjamini-Yekutieli](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/6791919) for FDR control under arbitrary dependence.

**The patch.** Wire exposure mappings to segment-level FDR. The pieces are standard; the composition for time-series segments is new.

**Reductions.** Zero bandwidth (no spillover) → standard per-segment test. All segments treated → empty output (no controls). Both cases [tested](https://github.com/kimjune01/filling-the-blanks).

### 5. Stochastic dominance over subtrees

**The near-miss.** Stochastic dominance testing exists for distributions. Hierarchical FDR exists for tree-structured hypotheses ([Yekutieli 2008](https://cris.tau.ac.il/en/publications/hierarchical-false-discovery-rate-controlling-methodology)). Nobody has defined "subtree A dominates subtree B" or tested it with bounded error.

**The failure mode.** Two departments in a company, each a subtree of the org chart. Department A has employees scoring [3, 4, 5]. Department B has [1, 2, 6]. Average is similar (4 vs 3). But A's score distribution is uniformly better at every threshold: more employees above 2, more above 3, more above 4. A stochastically dominates B. Raw averages miss this.

**The algorithm.** Define dominance via leaf-score CDFs:

1. Map each subtree to its weighted leaf-score empirical CDF.
2. Subtree A dominates B if F_A(t) ≤ F_B(t) for all thresholds t (first-order stochastic dominance).
3. Test each pair with a one-sided [Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).
4. Apply [Benjamini-Hochberg](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Hochberg_procedure) across all pairwise hypotheses.
5. Return the non-dominated set.

**The patch.** The definition itself. "Subtree dominates subtree" is stochastic dominance over leaf distributions. The testing and FDR machinery are standard; the definition is novel.

**Reductions.** Flat tree (all leaves) → each "subtree" is a single leaf, dominance reduces to scalar comparison. Single subtree → trivially non-dominated. Both cases [tested](https://github.com/kimjune01/filling-the-blanks).

### 6. Order-context similarity

**The near-miss.** [simona](https://doi.org/10.1186/s12864-024-10759-4) (Gu 2024) uses Jaccard on ancestor sets for bio-ontologies. [MinHash](https://ieeexplore.ieee.org/document/666900) (Broder 1997) estimates set similarity efficiently. Nobody has used order-theoretic context (ideals + filters) as a similarity measure for filtering with bounded error.

**The failure mode.** A taxonomy: Math ≤ Algebra ≤ Linear Algebra, Math ≤ Geometry ≤ Topology. Query: "items similar to Algebra." In a metric space you'd use distance. In a poset there is no distance. But Algebra and Geometry share a downset ({Math}) and have overlapping upsets. Linear Algebra and Topology share nothing below and nothing above. Order context captures this: Algebra and Geometry are similar (shared ancestry), Linear Algebra and Topology are not.

**The algorithm.** For query q and threshold τ:

1. Compute downset ↓x and upset ↑x for each element.
2. Similarity: s(q, x) = λ · J(↓q, ↓x) + (1−λ) · J(↑q, ↑x), where J is Jaccard.
3. Return elements with s(q, x) ≥ τ.

**The patch.** Use principal ideals and filters as the "feature sets" for Jaccard similarity. The radius is replaced by a similarity threshold. At scale, MinHash sketches approximate Jaccard with bounded additive error.

**Reductions.** Discrete poset (no edges) → all downsets/upsets are singletons → all pairwise similarities are zero → empty output. Total order → downsets are prefixes, similarities reflect positional proximity. Both cases [tested](https://github.com/kimjune01/filling-the-blanks).

### 7. Embedding-space causal filtering

**The near-miss.** [Giffin et al. (2023)](https://pubmed.ncbi.nlm.nih.gov/35996756/) model spatial interference where nearer treatments matter more. [Duan et al. (2024)](https://doi.org/10.1515/jci-2023-0059) give FDR-controlled causal selection. Nobody has composed embedding-distance interference with item-level FDR for recommendation cannibalization.

**The failure mode.** A content platform recommends articles. Recommending article A (machine learning) cannibalizes article B (deep learning) because they're nearby in embedding space — users who would have clicked B click A instead. The standard ATE treats each article independently. The interference-adjusted version estimates A's *direct* effect after accounting for cannibalization of similar articles.

**The algorithm.** For each item i with embedding e_i, treatment Z_i, outcome Y_i:

1. Compute interference exposure: S_i = Σ K(‖e_i − e_j‖) · Z_j, where K is a Gaussian kernel.
2. Build a local weighted regression at each item: outcome ~ treatment + exposure, weighted by embedding proximity.
3. Extract the direct effect coefficient and its standard error. Compute p-values.
4. Apply [Benjamini-Yekutieli](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/6791919) across all treated items.

**The patch.** Use embedding distance as the interference kernel. The regression separates direct effect from cannibalization. Same pattern as sequence × causal (#4) but in embedding geometry instead of temporal distance.

**Reductions.** Zero bandwidth (no interference) → standard per-item regression. All items treated → empty output (no controls). Both cases [tested](https://github.com/kimjune01/filling-the-blanks).

### 8. Streaming tokenizer

**The near-miss.** [Adaptive BPE](https://aclanthology.org/2024.findings-emnlp.863/) (Balde et al. 2024) and [TokAlign](https://aclanthology.org/2025.acl-long.207/) (Li et al. 2025) adapt vocabularies but operate offline. No existing tokenizer guarantees all three: online updates, backward compatibility, and bounded retokenization.

**The failure mode.** A search engine indexes documents over months. The vocabulary learned from January's documents doesn't cover March's new terminology. Re-tokenizing everything is expensive. A streaming tokenizer would learn new merges from recent documents without invalidating old token IDs or forcing a full reindex.

**The algorithm.**

1. **Append-only vocabulary**: every character gets a token ID. New merge tokens get new IDs. Old IDs never change meaning.
2. **Sliding window**: maintain a buffer of the most recent W token IDs.
3. **Bigram frequency tracking**: count adjacent pairs in the window. When a pair exceeds the merge threshold, create a new merge token.
4. **Window-local retokenization**: apply merges only within the window. Older tokens (frozen) keep their original tokenization.
5. **Flush**: when the window fills, push the oldest tokens to frozen storage.

**The patch.** Append-only merge DAG. Existing BPE mutates the vocabulary (merge = replace two tokens with one). This version only *adds* — the merge token is a new ID, the original tokens still exist. Backward compatibility is structural, not checked.

**The central limitation.** Old text is suboptimally tokenized forever. A merge learned in March doesn't retokenize January's documents. The tradeoff: bounded retokenization cost vs. compression quality. Deep streams accumulate vocabulary debt.

**Reductions.** Empty stream → empty vocabulary. Single-character stream → no bigram pairs → no merges. High threshold → no merges (vocabulary stays character-level). All cases [tested](https://github.com/kimjune01/filling-the-blanks).

### Summary

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:8em"><col style="width:14em"><col style="width:14em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Cell</th><th style="background:#f0f0f0">Novelty</th><th style="background:#f0f0f0">Near-miss</th><th style="background:#f0f0f0">Patch</th></tr></thead>
<tr><td>Graph × Dominance</td><td>Novel</td><td>Magnani & Assent 2013</td><td>Residualize</td></tr>
<tr><td>Partial order × Causal</td><td>Novel</td><td>Staggered rollout</td><td>Closure estimand</td></tr>
<tr><td>Attend × Partial order</td><td>Minor variation</td><td>Phylogenetic diversity</td><td>Jaccard kernel + MMR</td></tr>
<tr><td>Sequence × Causal</td><td>Minor variation</td><td>Spatial causal + FDR</td><td>Exposure mapping on segments</td></tr>
<tr><td>Tree × Dominance</td><td>Novel</td><td>Stochastic dominance + hierarchical FDR</td><td>Dominance = leaf CDF comparison</td></tr>
<tr><td>Partial order × Similarity</td><td>Novel</td><td>MinHash + bio-ontology similarity</td><td>Jaccard on ideals/filters</td></tr>
<tr><td>Embedding × Causal</td><td>Minor variation</td><td>Spatial interference + FDR</td><td>Embedding distance as kernel</td></tr>
<tr><td>Learned × Stream</td><td>Novel</td><td>Adaptive BPE, TokAlign</td><td>Append-only DAG + window buffer</td></tr>
</table>

---

*Written via the [double loop](/double-loop).*
