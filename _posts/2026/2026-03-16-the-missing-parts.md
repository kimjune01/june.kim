---
layout: post-wide
title: "The Missing Parts"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Parts Bin](/the-parts-bin).*

### Every cell fills

[The Parts Bin](/the-parts-bin) ended with two grids where every cell filled with a known algorithm. That validates the axes but proves nothing. A grid where every cell fills on sight is a catalog, not a periodic table. Mendeleev's grid had blanks. [I-Con (2025)](https://mhamilton.net/icon) had blanks. Can the parts bin find genuine blanks?

Adding a fourth row to Filter (causal filtering, selecting items by interventional effect) filled immediately: [Duan, Wasserman & Ramdas (2024)](https://doi.org/10.1515/jci-2023-0059) already composed the DR-learner + conformal + FDR stack. [Weighted conformal selection](https://academic.oup.com/biomet/article/doi/10.1093/biomet/asaf066/8250683) (Biometrika 2025) extends it. The grid predicted the composition; the composition already exists. More validation.

To find genuine blanks, the grid needs more dimensions.

### Ten axes

The design space has ten dimensions. An axis qualifies if it's discrete, orthogonal to the others, and crossing it with at least one other axis produces cells that aren't trivially occupied or trivially empty.

Four are universal:

1. **Pipeline stage**: perceive, cache, filter, attend, consolidate, remember
2. **Data structure**: flat, sequence, tree, graph, partial order
3. **Error guarantee**: exact, bounded, probabilistic
4. **Temporality**: batch, stream

Six are stage-specific:

<ol start="5">
<li><strong>Selection semantics</strong> <em>(Filter)</em>: predicate, similarity, dominance, causal</li>
<li><strong>Stationarity</strong> <em>(Filter)</em>: static criterion, drifting criterion</li>
<li><strong>Output form</strong> <em>(Attend)</em>: top-k slate, single best, path/tree</li>
<li><strong>Redundancy control</strong> <em>(Attend)</em>: none, implicit, explicit</li>
<li><strong>Codebook type</strong> <em>(Perceive)</em>: fixed, learned</li>
<li><strong>Supervision signal</strong> <em>(Consolidate)</em>: unsupervised, supervised, self-supervised</li>
</ol>

Ten axes, forty-five possible planes. Most are uninteresting. Five have blanks worth building.

### Five planes

The Parts Bin already drew two planes: selection semantics × error guarantee (Filter, 4×3) and output form × redundancy control (Attend, 3×3). Both fill on sight. They validate the axes but don't predict. The five planes below are where the blanks appear.

**Plane 1: Data structure × Selection semantics** (bounded error). "My data has structure. What filters exist?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Predicate</th><th style="background:#f0f0f0">Similarity</th><th style="background:#f0f0f0">Dominance</th><th style="background:#f0f0f0">Causal</th></tr></thead>
<tr><td><strong>Flat</strong></td><td>Threshold filtering</td><td>k-NN radius pruning</td><td>ε-dominance</td><td><a href="https://doi.org/10.1515/jci-2023-0059">Conformal causal selection</a></td></tr>
<tr><td><strong>Sequence</strong></td><td>Change-point detection</td><td>DTW pruning</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Tree</strong></td><td>XPath + depth bound</td><td>Tree edit distance threshold</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#e8f4e8"><a href="https://doi.org/10.1002/sim.9900">Luo & Guo</a><sup>†</sup></td></tr>
<tr><td><strong>Graph</strong></td><td>Approx subgraph match</td><td>Graph kernel pruning</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Partial order</strong></td><td><a href="https://doi.org/10.1093/biomet/asy066">DAGGER</a></td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#e8f4e8"><a href="https://ideas.repec.org/a/oup/biomet/v109y2022i2p457-471..html">Smoothed nested testing</a><sup>†</sup></td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

<small><sup>†</sup> Thin: occupies a narrow interpretation of the cell.</small>

The flat row fills completely. Everything below it is new. The predicate and similarity columns fill quickly. The right half empties out: dominance and causal filtering were designed for flat collections. Structure breaks both assumptions.

Seven blanks. [DAGGER](https://doi.org/10.1093/biomet/asy066) (Ramdas et al., Biometrika 2019) fills partial order × predicate. [Luo & Guo (2023)](https://doi.org/10.1002/sim.9900) fills tree × causal for prespecified subgroup hierarchies. [Smoothed nested testing](https://ideas.repec.org/a/oup/biomet/v109y2022i2p457-471..html) (Biometrika 2022) fills partial order × dominance under the hypothesis-poset reading. Each occupies a narrow reading of its cell. The broader versions remain open.

**Plane 2: Stationarity × Selection semantics** (bounded error). "My filter criterion drifts. What still works?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Predicate</th><th style="background:#f0f0f0">Similarity</th><th style="background:#f0f0f0">Dominance</th><th style="background:#f0f0f0">Causal</th></tr></thead>
<tr><td><strong>Static</strong></td><td>Threshold filtering</td><td>k-NN radius pruning</td><td>ε-dominance</td><td><a href="https://doi.org/10.1515/jci-2023-0059">Conformal causal selection</a></td></tr>
<tr><td><strong>Drifting</strong></td><td><a href="https://dl.acm.org/doi/10.1145/1150402.1150423">ADWIN</a></td><td style="background:#e8f4e8">Adaptive k-NN<sup>†</sup></td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

<small><sup>†</sup> Thin: [Losing et al. (2016)](https://ieeexplore.ieee.org/document/6835986) maintains k-NN under drift but lacks formal error bounds.</small>

The static row repeats plane 1's flat row. The drifting row is where things break. [ADWIN](https://dl.acm.org/doi/10.1145/1150402.1150423) (Bifet & Gavalda, 2007) handles drifting predicates with ε-bounded error via Chernoff bounds. Adaptive k-NN exists but without formal guarantees.

Drifting × dominance and drifting × causal are genuine blanks. Streaming skylines handle insertion drift (new items arriving) but not criterion drift (the dominance relation itself changing). Causal effect estimation under distribution shift has pieces ([adaptive conformal prediction](https://arxiv.org/abs/2110.13179), [anytime-valid inference](https://arxiv.org/abs/2011.03312)) but no composed filter. The right half empties for the same reason as plane 1: dominance and causal filtering assume stationarity in their criteria, not just in their data.

**Plane 3: Codebook type × Temporality** (Perceive). "Can my encoder adapt online?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Fixed codebook</th><th style="background:#f0f0f0">Learned codebook</th></tr></thead>
<tr><td><strong>Batch</strong></td><td>Lexical analysis, JSON parsing</td><td>BPE tokenization</td></tr>
<tr><td><strong>Stream</strong></td><td>A/D conversion</td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

One blank. BPE is learned offline. Recent vocabulary adaptation work is still offline: [Adaptive BPE](https://aclanthology.org/2024.findings-emnlp.863/) (Balde et al. 2024), [PickyBPE](https://aclanthology.org/2024.emnlp-main.925/) (Chizhov et al. 2024). Generic online encoders exist ([online dictionary learning](https://www.jmlr.org/papers/v11/mairal10a.html), [Growing Neural Gas](https://papers.nips.cc/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c0067e7-Abstract.html)) but neither satisfies the Perceive contract: parseable by downstream, backward-compatible, bounded retokenization rate.

**Plane 4: Pipeline stage × Data structure.** "For this data structure, which stages have gaps?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Flat</th><th style="background:#f0f0f0">Sequence</th><th style="background:#f0f0f0">Tree</th><th style="background:#f0f0f0">Graph</th><th style="background:#f0f0f0">Partial order</th></tr></thead>
<tr><td><strong>Perceive</strong></td><td>JSON parsing</td><td>A/D conversion</td><td>XML parsing</td><td>Edge list parsing</td><td style="background:#e8f4e8">PC algorithm<sup>†</sup></td></tr>
<tr><td><strong>Cache</strong></td><td>Hash index</td><td>B-tree</td><td>Trie</td><td>Adjacency index</td><td style="background:#e8f4e8">Transitive closure<sup>†</sup></td></tr>
<tr><td><strong>Filter</strong></td><td>WHERE</td><td>Change-point</td><td>XPath</td><td>Subgraph match</td><td style="background:#e8f4e8">DAGGER<sup>†</sup></td></tr>
<tr><td><strong>Attend</strong></td><td>MMR</td><td>Beam search</td><td>MCTS</td><td><a href="https://doi.org/10.14778/2536258.2536263">Div. top-k</a></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Consolidate</strong></td><td>Gradient descent</td><td>Grammar induction</td><td>Decision tree induction</td><td>GNN training</td><td style="background:#e8f4e8">Lattice learning<sup>†</sup></td></tr>
<tr><td><strong>Remember</strong></td><td>WAL append</td><td>SSTable flush</td><td>Git commit</td><td>Graph DB commit</td><td>Topological serialization</td></tr>
</table>

<small><sup>†</sup> Thin: 1-2 algorithms exist but no standard toolkit.</small>

The partial order column is the weak column. Attend × partial order is a genuine blank. DPP-style diversity requires a kernel over a metric space, but partial orders have reachability, not distance. The contract demands top-k diverse from a poset. The algorithm doesn't exist.

**Plane 5: Selection semantics × Error guarantee** (Filter). The anchor plane, fully occupied.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Exact</th><th style="background:#f0f0f0">Bounded</th><th style="background:#f0f0f0">Probabilistic</th></tr></thead>
<tr><td><strong>Predicate</strong></td><td>WHERE, range query</td><td>Threshold filtering</td><td><a href="https://en.wikipedia.org/wiki/Bloom_filter">Bloom filter</a></td></tr>
<tr><td><strong>Similarity</strong></td><td>Exact NN pruning</td><td>k-NN radius pruning</td><td><a href="https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/">LSH filtering</a></td></tr>
<tr><td><strong>Dominance</strong></td><td>Pareto filtering</td><td>ε-dominance</td><td>Stochastic dominance</td></tr>
<tr><td><strong>Causal</strong></td><td>do-calculus gate</td><td><a href="https://doi.org/10.1515/jci-2023-0059">Conformal causal selection</a></td><td>Propensity score gate</td></tr>
</table>

All sixteen cells fill. This plane validates the axes: selection semantics and error guarantee partition Filter cleanly. Every cell has a known algorithm, including causal × bounded (which filled after the grid predicted it). The anchor plane shows the taxonomy works. The four planes above show where it breaks.

### Why the blanks cluster

The blanks from planes 1 and 2 follow from the same structural facts. Dominance assumes independent objective vectors: each item is a point in ℝ^d, dominance is coordinate-wise. Causal effect estimation assumes pointwise treatment assignment and stationarity. Structure breaks independence. Drift breaks stationarity.

Exact dominance on structured data has scattered coverage: [skyline community search](https://doi.org/10.1145/3183713.3183736) (SIGMOD 2018) for graphs, [TSS](https://researchportal.hkust.edu.hk/en/publications/topologically-sorted-skylines-for-partially-ordered-domains) for partial orders, trajectory skylines for sequences. Every one of these is exact. Nobody has built the bounded-error variant for any of them.

The causal column has the same shape. [CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html) estimates effects on time series but doesn't gate with bounded error. Causal inference on known DAGs is a mature field, yet "filter graph nodes whose interventional effect exceeds τ with bounded error" has no standard algorithm. Under drift it's worse: the pieces for adaptive estimation exist, but the composition with FDR control doesn't.

Partial order × similarity is the most conceptually interesting blank: similarity filtering assumes a metric space, but partial orders have reachability, not distance. What does "similar" mean when some pairs of items are incomparable?

### What the blanks tell us

Eleven blanks survive validation across five planes. They cluster around four broken assumptions:

1. **Dominance assumes independence.** Structure introduces dependencies. Four cells empty in plane 1.
2. **Causal estimation assumes pointwise treatment.** Structure introduces spillover, nesting, and temporal lag. Three cells empty in plane 1 (plus the thin streaming cell).
3. **Both assume stationarity.** Drift empties two more cells in plane 2.
4. **Diversity assumes a metric space.** Partial orders have reachability, not distance. One cell empty in plane 4.

Plus one in Perceive (learned codebook × stream, plane 3).

Mendeleev predicted germanium's density before anyone found the element. I-Con predicted a new algorithm. These blanks predict compositions: the pieces exist in separate literatures (skyline queries, causal inference, FDR control, graph kernels, poset theory, drift detection), and the contract names what they must satisfy when assembled. Ten axes tell you where to look. Five planes tell you where to build. The grid writes the spec. The spec is eleven algorithms nobody's built.

### Composition sketches

Three blanks from plane 1 have compositions close enough to sketch. Each wires existing libraries into a pipeline that satisfies the contract: input strictly larger than output, bounded FDR.

**Sequence × Causal (bounded).** For each time-series segment: fit [CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html) to estimate the intervention effect, compute a [split-conformal](https://proceedings.mlr.press/v162/fisch22a.html) interval from pre-period residuals, derive a one-sided p-value for effect > τ, and feed it to [SAFFRON](https://proceedings.mlr.press/v80/ramdas18a.html) for online FDR control. Accept segments where both the conformal lower bound exceeds the threshold and the online test rejects. FDR ≤ α under SAFFRON's dependence assumptions. Pieces: `causalimpact`, `mapie`, custom SAFFRON implementation.

**Graph × Causal (bounded).** For each node in a known causal DAG: identify the estimand via [DoWhy](https://github.com/py-why/dowhy), estimate the node-specific interventional effect with doubly robust estimation under an [exposure mapping](https://www.frontiersin.org/articles/10.3389/fdata.2023.1128649/full) that accounts for network spillover, compute a one-sided p-value for effect > τ, and apply [Benjamini-Hochberg](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Hochberg_procedure) across all nodes. FDR ≤ α under independence/PRDS; use [BY](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Yekutieli_procedure) for arbitrary dependence. Pieces: `dowhy`, `causallib`, `networkx`, `statsmodels`.

**Sequence × Dominance (bounded).** For each trajectory: evaluate objectives in temporal order, compute pairwise [conformal p-values](https://proceedings.mlr.press/v162/fisch22a.html) for "trajectory j dominates trajectory i," aggregate per-trajectory with Bonferroni, and correct across trajectories with BY. Retain trajectories whose domination null is not rejected. P(retaining a truly dominated trajectory) ≤ α. Pieces: `paretoset`, `mapie`, `statsmodels`.

The remaining blanks need definitions before they need code. The algorithms are standard (greedy, branch-and-bound, threshold). The definitions are what's missing. Candidate definitions for each:

**Tree × Dominance.** *(Minor variation of [tree edit distance](https://doi.org/10.1137/0218082) mechanics, reframed as dominance.)* Define subtree value via a monotone tree aggregator (additive rollup, max-plus, discounted sum). Subtree A dominates B if there exists a hierarchy-respecting coupling between their nodes where every matched pair satisfies coordinate-wise ε-slack and unmatched structure incurs a penalty. Reduces to Pareto when the tree is flat. Filter via bottom-up interval sketches: compare `[L,U]` bounds, only resolve ambiguous pairs exactly. The matching mechanics come from [Zhang & Shasha (1989)](https://doi.org/10.1137/0218082); what's new is using them as a dominance order rather than a distance.

**Graph × Dominance.** *(Novel — no prior work on residualized dominance for overlapping communities.)* Factor out shared substructure before comparing. For communities C₁ and C₂ with overlap I, decompose into residuals R₁, R₂ and compare only marginal contributions g(R₁ given I) vs g(R₂ given I). Overlap-aware dominance: C₁ ≤ C₂ iff the residual of C₁ is no better than C₂'s on every objective. Filter via minhash overlap estimation and residual bound comparison. Nearest prior art: [skyline community search](https://doi.org/10.1145/3183713.3183736) (SIGMOD 2018) does exact dominance but doesn't handle overlap; [group skyline](https://doi.org/10.1016/j.ins.2021.12.028) compares sets but doesn't subtract shared members.

**Partial order × Similarity.** *(Minor variation of ontology similarity — [Jaccard on ancestor sets](https://doi.org/10.1186/s12864-024-10759-4) exists in bioinformatics.)* Replace metric distance with contextual overlap: Sim(x,y) = α·J(Down(x),Down(y)) + β·J(Up(x),Up(y)) + γ·C(x,y), where J is Jaccard on principal ideals/filters and C is a comparability bonus. The analogue of radius is a lower-bound frontier on contextual overlap. Filter via minhash sketches of ideals/filters and threshold pruning. Prior art: [simona](https://doi.org/10.1186/s12864-024-10759-4) (Gu 2024) uses Jaccard on ancestor sets for bio-ontologies; [GOntoSim](https://doi.org/10.1038/s41598-022-07624-3) uses common descendants; [Formica (2006)](https://doi.org/10.1016/j.ins.2005.11.014) combines intensional/extensional context in FCA. What's new is the symmetric poset formulation with tunable weights and a bounded-error filter contract.

**Partial order × Causal.** *(Novel estimand class — no prior work defines τₓ via feasible closure interventions on posets.)* The unit of treatment is a feasible order-closure, not a single node. Treating node x forces treatment of its descendants: T(x) = closure({x}). The causal effect is τₓ = E[Y(S₀ ∪ T(x)) − Y(S₀)] where S₀ is the baseline feasible set. Estimate via isotonic outcome models or doubly robust estimators with order-constrained nuisance fits. Filter by interval bounds on τₓ. Requires positivity over feasible closures. Nearest prior art: [Shpitser & Tchetgen Tchetgen (2016)](https://doi.org/10.1214/15-AOS1411) on hierarchical interventions; [Manski (1997)](https://doi.org/10.2307/2171738) on monotone treatment response; [Forastiere et al. (2016)](https://www.emergentmind.com/papers/1609.06245) on network interference. None defines the closure-level estimand.

**Attend × Partial order.** *(Minor variation — standard [submodular diversification](https://doi.org/10.1145/3130348.3130369) with a new poset-specific kernel.)* Diversity = order repulsion: D(x,y) = 1 − Sim(x,y) using the same contextual overlap from above. Two options: (1) build a PSD order kernel from ideal/filter indicator features and use DPP, or (2) use submodular greedy over F(S) = Σr(x) + λ·cover(S) where coverage rewards spanning distinct antichain regions. "Top-k diverse from a poset" means: size-k set maximizing relevance plus order-context coverage, not a total order. The framework is [MMR](https://doi.org/10.1145/3130348.3130369) / [submodular bandits](https://authors.library.caltech.edu/records/4ka4j-v7d44/latest); the poset kernel is the new piece.

---

*Written via the [double loop](/double-loop).*
