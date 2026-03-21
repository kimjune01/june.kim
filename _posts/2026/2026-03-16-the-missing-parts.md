---
layout: post-wide
title: "The Missing Parts"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Parts Bin](/the-parts-bin).*

### The 3×3 problem

[The Parts Bin](/the-parts-bin) ended with two grids, Filter and Attend, where every cell filled with a known algorithm. That validates the axes: selection semantics × error guarantee partitions Filter cleanly, output form × redundancy control partitions Attend cleanly. No misplacements, no awkward fits.

But a grid where every cell fills on sight is a catalog, not a periodic table. Mendeleev's grid had blanks. He predicted germanium's density, melting point, and oxide formula before anyone found the element. [I-Con (2025)](https://mhamilton.net/icon) did the same for Consolidate: a blank cell in their periodic table led to a new algorithm that beat the state of the art.

Can the parts bin do this? Where are the genuine blanks?

### Filter: the causal row

The existing Filter grid has three rows: predicate, similarity, dominance. All nine cells are occupied. To find a blank, we need a fourth row where the selection semantics are genuinely different and at least one error-guarantee column is empty.

**Causal filtering**: select items by whether they causally affect an outcome. Correlation is similarity filtering. Dominance across objectives is dominance filtering. Causal means: if you intervene on this item, the outcome changes.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Exact</th><th style="background:#f0f0f0">Bounded</th><th style="background:#f0f0f0">Probabilistic</th></tr></thead>
<tr><td><strong>Predicate</strong></td><td>WHERE, range query</td><td>Threshold filtering</td><td>Bloom filter</td></tr>
<tr><td><strong>Similarity</strong></td><td>Exact NN pruning</td><td>k-NN radius pruning</td><td>LSH filtering</td></tr>
<tr><td><strong>Dominance</strong></td><td>Pareto filtering</td><td>ε-dominance</td><td>Stochastic dominance</td></tr>
<tr><td><strong>Causal</strong></td><td>do-calculus gate</td><td style="background:#fff3cd"><em>blank</em></td><td>Propensity score gate</td></tr>
</table>

**Causal × Exact**: Given a fully identified causal graph, select items on active causal paths. The do-calculus gives the criterion; applying it as a binary gate is deterministic. This exists in theory (the backdoor criterion, the front-door criterion) but isn't packaged as a standalone filter. Call it a *do-calculus gate*: pass items with nonzero causal effect under the identified model, reject the rest. The pieces exist. The assembly doesn't.

**Causal × Probabilistic**: Propensity score gating. Discard items with treatment probability below a threshold. Practitioners use propensity scores for [weighting (IPW)](https://en.wikipedia.org/wiki/Inverse_probability_weighting), not hard gating. Truncated IPW, which discards extreme-propensity items, is a probabilistic filter. Borderline occupied.

**Causal × Bounded**: Filter items whose estimated causal effect exceeds a threshold, with bounded false-positive and false-negative rates. This is the genuine blank.

The pieces exist in three separate literatures. For scores: [doubly robust estimators](https://proceedings.mlr.press/v193/argaw22a.html), honest causal forests, R-learners. For uncertainty: [conformalized effect intervals](https://proceedings.mlr.press/v162/fisch22a.html), influence-function CIs. For the decision rule: [knockoff filters](https://proceedings.mlr.press/v48/daia16.html), [e-value procedures](https://proceedings.mlr.press/v238/xu24a.html), [class-conditional conformal risk bounds](https://proceedings.mlr.press/v252/garcia24a.html). Adjacent work in [safe treatment policy learning](https://proceedings.mlr.press/v202/li23ay.html) gets close but optimizes a policy (Consolidate), not a gate (Filter).

No one has composed these into a single filter operation with the contract: *strictly smaller, causal criterion, bounded error*. The composition would look like:

1. **Score**: DR-learner or causal forest → CATE estimate per item
2. **Bound**: conformalized effect interval or bootstrap CI
3. **Gate**: threshold on lower confidence bound, with BH/e-LOND error control
4. **Abstain region**: items with CIs spanning zero are rejected, keeping the operator a filter rather than a policy

Real problems want it: personalized medicine (filter patients who will benefit from treatment), policy evaluation (filter interventions with causal impact), ad targeting (filter users causally affected, not just correlated with conversion).

### Attend: saturated

The Attend grid fills completely. Set output, allocation, rejection — every extension tried reduces to existing algorithms. No blanks at this resolution.

### Perceive: a second blank

Perceive has no grid. A first sketch:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Fixed codebook</th><th style="background:#f0f0f0">Learned codebook</th></tr></thead>
<tr><td><strong>Batch</strong></td><td>Lexical analysis, JSON parsing</td><td>BPE tokenization</td></tr>
<tr><td><strong>Stream</strong></td><td>A/D conversion</td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

**Learned codebook × Stream**: Adapt the encoding as data arrives. BPE is learned offline. Recent vocabulary adaptation work is still offline: [Adaptive BPE](https://aclanthology.org/2024.findings-emnlp.863/) (Balde et al. 2024), [PickyBPE](https://aclanthology.org/2024.emnlp-main.925/) (Chizhov et al. 2024). Generic online encoders exist — [online dictionary learning](https://www.jmlr.org/papers/v11/mairal10a.html) (Mairal et al. 2010), [Growing Neural Gas](https://papers.nips.cc/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c0067e7-Abstract.html) (Fritzke 1994) — but neither satisfies the Perceive contract: parseable by downstream, backward-compatible, stable enough to avoid catastrophic retokenization. This blank is less developed than the causal filter. The spec is shorter: online merge/split of codebook entries, bounded retokenization rate, predictive-utility objective. The literature is thinner. It belongs on the list but isn't ready for a composition sketch.

### The third axis

The grids above are two-dimensional. Filter is selection semantics × error guarantee. Attend is output form × redundancy control. Both assume the input is a flat collection — a bag of items where each item is independent.

But algorithms operate *on* data structures. A sequence has order. A tree has hierarchy. A graph has adjacency. A partial order has comparability without totality. The data structure constrains which operations are possible and which postconditions are achievable. That makes it a genuine third axis, not a label.

Hold the error guarantee at **bounded** — the column where the causal blank already lives — and cross data structure against selection semantics:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Predicate</th><th style="background:#f0f0f0">Similarity</th><th style="background:#f0f0f0">Dominance</th><th style="background:#f0f0f0">Causal</th></tr></thead>
<tr><td><strong>Flat</strong></td><td>Threshold filtering</td><td>k-NN radius pruning</td><td>ε-dominance</td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Sequence</strong></td><td>Change-point detection</td><td>DTW pruning</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Tree</strong></td><td>XPath + depth bound</td><td>Tree edit distance threshold</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Graph</strong></td><td>Approx subgraph match</td><td>Graph kernel pruning</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Partial order</strong></td><td><a href="https://doi.org/10.1093/biomet/asy066">DAGGER</a></td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

The flat row repeats the original grid. Everything below it is new. The predicate and similarity columns fill quickly — CS has been filtering structured data by predicate and proximity for decades. The right half empties out. Dominance and causal filtering were built for flat collections. Nobody carried them over.

One cell that looked blank turned out to be occupied. [DAGGER](https://doi.org/10.1093/biomet/asy066) (Ramdas et al., Biometrika 2019) does FDR-controlled hypothesis filtering on DAGs — partial order × predicate with bounded error. The algorithm exists. The rest of the partial order row does not.

### Dominance on structured data

Pareto filtering assumes independent objective vectors: each item is a point in ℝ^d, dominance is coordinate-wise. What happens when items have structure?

**Sequence × Dominance.** Trajectory skylines exist — [skyline queries over moving objects](https://doi.org/10.1007/s00778-020-00618-5) — but they filter *points that happen to move*, not *sequences whose ordering constrains which comparisons are valid*. A bounded-error algorithm for "this trajectory dominates that trajectory, respecting temporal order" has no standard name.

**Tree × Dominance.** Tree data structures *for* Pareto processing exist (KD-trees for skyline queries). But "this subtree dominates that subtree across multiple objectives" — where the tree structure is the *input*, not the index — is unstudied.

**Graph × Dominance.** The closest work is skyline community search: ["Skyline Community Search in Multi-valued Networks"](https://doi.org/10.1145/3183713.3183736) (SIGMOD 2018) finds communities that aren't dominated on multiple graph attributes. That's exact. No bounded-error variant exists.

**Partial order × Dominance.** Exact algorithms exist: [TSS](https://researchportal.hkust.edu.hk/en/publications/topologically-sorted-skylines-for-partially-ordered-domains) for topologically sorted skylines, [DRSA](https://en.wikipedia.org/wiki/Dominance-based_rough_set_approach) for rough-set dominance. No bounded-error version in the FPR/FNR sense.

The pattern: exact dominance on structured data has scattered coverage. Bounded-error dominance on structured data has none. Four empty cells, same gap.

### Causal filtering on structured data

The original blank — causal × bounded on flat data — has a composition sketch. What about structured inputs?

**Sequence × Causal.** [CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html) estimates causal effects on time series. [FDR-controlled change detection](https://doi.org/10.1016/j.jmva.2023.105224) bounds error rates on sequence data. Nobody has composed them into: "filter time-series segments by interventional effect with bounded FPR/FNR."

**Tree × Causal.** Uplift trees and causal forests estimate treatment effects by recursive partitioning. But they *build* the tree (Consolidate). Filtering branches of an *existing* tree by causal effect with bounded error — that's a different operation, and it doesn't exist.

**Graph × Causal.** Causal inference on known DAGs is a mature field. FDR-controlled selection on graph-structured hypotheses exists. But "given this causal graph, filter nodes whose interventional effect exceeds threshold τ with bounded error" has no standard algorithm. The pieces are closer here than anywhere else in the grid.

### The partial order desert

The bottom row is the most striking. Partial orders are everywhere — dependency graphs, taxonomies, version histories, lattices of formal concepts. One cell is occupied (DAGGER for predicate filtering). The other three are empty.

Partial order × similarity is the most conceptually interesting blank. Similarity filtering assumes a metric space. Partial orders don't have distances — they have reachability. What does "similar" mean when some pairs of items are incomparable? Poset search algorithms exist. Metric-space search exists. The intersection is unstudied.

### Attend and Perceive

The Attend grid looked saturated in two dimensions. With data structure as an axis, two cells that looked blank turned out to be occupied:

- **Graph × explicit diversity**: [Diversified Top-k Graph Pattern Matching](https://doi.org/10.14778/2536258.2536263) (PVLDB 2013) and [TED+](https://doi.org/10.1109/TKDE.2023.3312566) (TKDE 2024) both rank graph patterns with explicit redundancy control.
- **Hypergraph ranking**: [Top-k Hyperedge Triplets](https://www.pnnl.gov/publications/retrieving-top-k-hyperedge-triplets-models-and-applications) (IEEE BigData 2024) ranks hypergraph outputs directly.

Attend remains saturated even in three dimensions. The Perceive blank (learned codebook × stream) remains open — recent work on vocabulary adaptation ([BPE-knockout](https://aclanthology.org/2024.naacl-long.324/), [TokAlign](https://aclanthology.org/2025.acl-long.207/)) still operates offline.

### What the blanks tell us

The original two-dimensional grids found two blanks. The data structure axis reveals eight more — and they cluster. The dominance column empties whenever the input has structure. The causal column was already empty for flat data; structured data makes it worse. The partial order row is a desert.

These aren't random gaps. They follow from a structural fact: dominance and causal filtering were designed for flat collections. The algorithms assume independent items with coordinate-wise comparison or pointwise treatment assignment. Structure breaks both assumptions. Order constrains which comparisons are valid. Hierarchy nests effects. Adjacency creates interference.

Mendeleev predicted germanium's density before anyone found the element. I-Con predicted a new algorithm. These blanks predict something more specific: *compositions*. The pieces exist in separate literatures — skyline queries, causal inference, FDR control, graph kernels. The contract names what they must satisfy when assembled. The grid writes the spec. The data structure axis tells you which assembly hasn't been attempted.

The causal filter blank has a 4-step composition sketch, six literature entry points, and three application domains waiting. The eight new blanks have the same shape: pieces in separate papers, a contract from the framework, and a gap where the composition should be. That's not "something goes here." That's a build order — eight times over.

---

*Written via the [double loop](/double-loop).*
