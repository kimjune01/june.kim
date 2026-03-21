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

Ten axes, forty-five possible planes. Most are uninteresting. Three have blanks worth building.

### Planes that validate

The Parts Bin drew two planes that fill on sight: selection semantics × error guarantee (Filter, 4×3) and output form × redundancy control (Attend, 3×3). Three more planes also fill completely, confirming the taxonomy works at each new crossing:

**Stationarity × Selection semantics** (bounded error). [ADWIN](https://dl.acm.org/doi/10.1145/1150402.1150423) handles drifting predicates. [Dynamic skyline queries](https://www.mdpi.com/2220-9964/6/5/137) handle drifting dominance criteria. [Weighted conformal p-values under covariate shift](https://academic.oup.com/biomet/advance-article/doi/10.1093/biomet/asaf066/8250683) (Biometrika 2025) handles drifting causal filtering. All cells occupied.

**Temporality × Selection semantics** (bounded error). Streaming predicate filtering has [Count-Min Sketch](https://en.wikipedia.org/wiki/Count%E2%80%93min_sketch). Streaming similarity has LSH variants. Streaming dominance has [sliding window skylines](https://cse.hkust.edu.hk/~dimitris/PAPERS/TKDE06-Sky.pdf). Streaming causal has [Xie et al. (2018)](https://arxiv.org/abs/1808.04904) for online A/B experiments. All cells occupied.

Five fully-occupied planes. The grid validates. Now for the blanks.

### Planes that predict

**Plane 1: Data structure × Selection semantics** (bounded error). "My data has structure. What filters exist?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Predicate</th><th style="background:#f0f0f0">Similarity</th><th style="background:#f0f0f0">Dominance</th><th style="background:#f0f0f0">Causal</th></tr></thead>
<tr><td><strong>Flat</strong></td><td>Threshold filtering</td><td>k-NN radius pruning</td><td>ε-dominance</td><td><a href="https://doi.org/10.1515/jci-2023-0059">Conformal causal selection</a></td></tr>
<tr><td><strong>Sequence</strong></td><td>Change-point detection</td><td>DTW pruning</td><td><a href="https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z">Dominant skyline over time series</a></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Tree</strong></td><td>XPath + depth bound</td><td>Tree edit distance threshold</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#e8f4e8"><a href="https://doi.org/10.1002/sim.9900">Luo & Guo</a><sup>†</sup></td></tr>
<tr><td><strong>Graph</strong></td><td>Approx subgraph match</td><td>Graph kernel pruning</td><td><a href="https://weiguozheng.github.io/pub/tkde16-skyline.pdf">Subgraph skyline</a></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Partial order</strong></td><td><a href="https://doi.org/10.1093/biomet/asy066">DAGGER</a></td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#e8f4e8"><a href="https://ideas.repec.org/a/oup/biomet/v109y2022i2p457-471..html">Smoothed nested testing</a><sup>†</sup></td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

<small><sup>†</sup> Thin: occupies a narrow interpretation of the cell.</small>

The flat row fills completely. Everything below it is new. The predicate and similarity columns fill quickly. The dominance column mostly fills: [dominant skyline over multiple time series](https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z) (2013) handles sequences, [subgraph skyline](https://weiguozheng.github.io/pub/tkde16-skyline.pdf) (TKDE 2016) handles graphs. Tree × dominance remains open.

Five blanks. The causal column is the emptiest: only flat data has a complete algorithm. [Luo & Guo (2023)](https://doi.org/10.1002/sim.9900) fills tree × causal for prespecified subgroup hierarchies but not arbitrary trees. Partial order × similarity is the most conceptually interesting blank: similarity filtering assumes a metric space, but partial orders have reachability, not distance.

**Plane 2: Codebook type × Temporality** (Perceive). "Can my encoder adapt online?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Fixed codebook</th><th style="background:#f0f0f0">Learned codebook</th></tr></thead>
<tr><td><strong>Batch</strong></td><td>Lexical analysis, JSON parsing</td><td>BPE tokenization</td></tr>
<tr><td><strong>Stream</strong></td><td>A/D conversion</td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

One blank. BPE is learned offline. Recent vocabulary adaptation work is still offline: [Adaptive BPE](https://aclanthology.org/2024.findings-emnlp.863/) (Balde et al. 2024), [PickyBPE](https://aclanthology.org/2024.emnlp-main.925/) (Chizhov et al. 2024). Generic online encoders exist ([online dictionary learning](https://www.jmlr.org/papers/v11/mairal10a.html), [Growing Neural Gas](https://papers.nips.cc/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c0067e7-Abstract.html)) but neither satisfies the Perceive contract: parseable by downstream, backward-compatible, bounded retokenization rate.

**Plane 3: Pipeline stage × Data structure.** "For this data structure, which stages have gaps?"

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

### Why the blanks cluster

Causal filtering on structured data is the emptiest region. Only flat data has a complete bounded-error causal filter. [CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html) estimates effects on time series but doesn't gate with bounded error. Causal inference on known DAGs is a mature field, yet "filter graph nodes whose interventional effect exceeds τ with bounded error" has no standard algorithm. The pieces exist. The composition doesn't.

Dominance on trees is the lone holdout in its column. Sequences have [dominant skyline over time series](https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z). Graphs have [subgraph skyline](https://weiguozheng.github.io/pub/tkde16-skyline.pdf). Partial orders have [smoothed nested testing](https://ideas.repec.org/a/oup/biomet/v109y2022i2p457-471..html) (under a narrow reading). Trees have nothing. "Subtree dominates subtree" needs a definition before it needs an algorithm.

Partial order × similarity is the most conceptually interesting blank: similarity filtering assumes a metric space, but partial orders have reachability, not distance. What does "similar" mean when some pairs of items are incomparable?

### What the blanks tell us

Seven blanks survive validation across three planes. They cluster around three broken assumptions:

1. **Causal estimation assumes pointwise treatment.** Structure introduces spillover, nesting, and temporal lag. Three cells empty in plane 1 (sequence, graph, partial order).
2. **Tree dominance has no definition.** The other structured data types have skyline algorithms. Trees don't, because "subtree dominates subtree" requires a hierarchy-respecting comparison that nobody has formalized.
3. **Diversity and similarity assume a metric space.** Partial orders have reachability, not distance. Two cells empty (similarity in plane 1, attend in plane 3).

Plus one in Perceive (learned codebook × stream, plane 2).

Mendeleev predicted germanium's density before anyone found the element. I-Con predicted a new algorithm. These blanks predict compositions: the pieces exist in separate literatures (skyline queries, causal inference, FDR control, graph kernels, poset theory), and the contract names what they must satisfy when assembled. Ten axes tell you where to look. Three planes tell you where to build. The grid writes the spec. The spec is seven algorithms nobody's built.

### Composition sketches

Two blanks from plane 1 have compositions close enough to sketch. Each wires existing libraries into a pipeline that satisfies the contract: input strictly larger than output, bounded FDR.

**Sequence × Causal (bounded).** For each time-series segment: fit [CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html) to estimate the intervention effect, compute a [split-conformal](https://proceedings.mlr.press/v162/fisch22a.html) interval from pre-period residuals, derive a one-sided p-value for effect > τ, and feed it to [SAFFRON](https://proceedings.mlr.press/v80/ramdas18a.html) for online FDR control. Accept segments where both the conformal lower bound exceeds the threshold and the online test rejects. FDR ≤ α under SAFFRON's dependence assumptions. Pieces: `causalimpact`, `mapie`, custom SAFFRON implementation.

**Graph × Causal (bounded).** For each node in a known causal DAG: identify the estimand via [DoWhy](https://github.com/py-why/dowhy), estimate the node-specific interventional effect with doubly robust estimation under an [exposure mapping](https://www.frontiersin.org/articles/10.3389/fdata.2023.1128649/full) that accounts for network spillover, compute a one-sided p-value for effect > τ, and apply [Benjamini-Hochberg](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Hochberg_procedure) across all nodes. FDR ≤ α under independence/PRDS; use [BY](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Yekutieli_procedure) for arbitrary dependence. Pieces: `dowhy`, `causallib`, `networkx`, `statsmodels`.

The remaining blanks need definitions before they need code. The algorithms are standard (greedy, branch-and-bound, threshold). The definitions are what's missing. Candidate definitions for each:

**Tree × Dominance.** *(Minor variation of [tree edit distance](https://doi.org/10.1137/0218082) mechanics, reframed as dominance.)* Define subtree value via a monotone tree aggregator (additive rollup, max-plus, discounted sum). Subtree A dominates B if there exists a hierarchy-respecting coupling between their nodes where every matched pair satisfies coordinate-wise ε-slack and unmatched structure incurs a penalty. Reduces to Pareto when the tree is flat. Filter via bottom-up interval sketches: compare `[L,U]` bounds, only resolve ambiguous pairs exactly. The matching mechanics come from [Zhang & Shasha (1989)](https://doi.org/10.1137/0218082); what's new is using them as a dominance order rather than a distance.

**Graph × Dominance.** *(Novel — no prior work on residualized dominance for overlapping communities.)* Factor out shared substructure before comparing. For communities C₁ and C₂ with overlap I, decompose into residuals R₁, R₂ and compare only marginal contributions g(R₁ given I) vs g(R₂ given I). Overlap-aware dominance: C₁ ≤ C₂ iff the residual of C₁ is no better than C₂'s on every objective. Filter via minhash overlap estimation and residual bound comparison. Nearest prior art: [skyline community search](https://doi.org/10.1145/3183713.3183736) (SIGMOD 2018) does exact dominance but doesn't handle overlap; [group skyline](https://doi.org/10.1016/j.ins.2021.12.028) compares sets but doesn't subtract shared members.

**Partial order × Similarity.** *(Minor variation of ontology similarity — [Jaccard on ancestor sets](https://doi.org/10.1186/s12864-024-10759-4) exists in bioinformatics.)* Replace metric distance with contextual overlap: Sim(x,y) = α·J(Down(x),Down(y)) + β·J(Up(x),Up(y)) + γ·C(x,y), where J is Jaccard on principal ideals/filters and C is a comparability bonus. The analogue of radius is a lower-bound frontier on contextual overlap. Filter via minhash sketches of ideals/filters and threshold pruning. Prior art: [simona](https://doi.org/10.1186/s12864-024-10759-4) (Gu 2024) uses Jaccard on ancestor sets for bio-ontologies; [GOntoSim](https://doi.org/10.1038/s41598-022-07624-3) uses common descendants; [Formica (2006)](https://doi.org/10.1016/j.ins.2005.11.014) combines intensional/extensional context in FCA. What's new is the symmetric poset formulation with tunable weights and a bounded-error filter contract.

**Partial order × Causal.** *(Novel estimand class — no prior work defines τₓ via feasible closure interventions on posets.)* The unit of treatment is a feasible order-closure, not a single node. Treating node x forces treatment of its descendants: T(x) = closure({x}). The causal effect is τₓ = E[Y(S₀ ∪ T(x)) − Y(S₀)] where S₀ is the baseline feasible set. Estimate via isotonic outcome models or doubly robust estimators with order-constrained nuisance fits. Filter by interval bounds on τₓ. Requires positivity over feasible closures. Nearest prior art: [Shpitser & Tchetgen Tchetgen (2016)](https://doi.org/10.1214/15-AOS1411) on hierarchical interventions; [Manski (1997)](https://doi.org/10.2307/2171738) on monotone treatment response; [Forastiere et al. (2016)](https://www.emergentmind.com/papers/1609.06245) on network interference. None defines the closure-level estimand.

**Attend × Partial order.** *(Minor variation — standard [submodular diversification](https://doi.org/10.1145/3130348.3130369) with a new poset-specific kernel.)* Diversity = order repulsion: D(x,y) = 1 − Sim(x,y) using the same contextual overlap from above. Two options: (1) build a PSD order kernel from ideal/filter indicator features and use DPP, or (2) use submodular greedy over F(S) = Σr(x) + λ·cover(S) where coverage rewards spanning distinct antichain regions. "Top-k diverse from a poset" means: size-k set maximizing relevance plus order-context coverage, not a total order. The framework is [MMR](https://doi.org/10.1145/3130348.3130369) / [submodular bandits](https://authors.library.caltech.edu/records/4ka4j-v7d44/latest); the poset kernel is the new piece.

---

*Written via the [double loop](/double-loop).*
