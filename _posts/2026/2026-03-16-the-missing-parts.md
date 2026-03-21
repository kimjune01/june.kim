---
layout: post-wide
title: "The Missing Parts"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Parts Bin](/the-parts-bin).*

### Every cell fills

[The Parts Bin](/the-parts-bin) ended with two grids where every cell filled with a known algorithm. That validates the axes but proves nothing. A grid where every cell fills on sight is a catalog, not a periodic table. Mendeleev's grid had blanks. [I-Con (2025)](https://mhamilton.net/icon) had blanks. Can the parts bin find genuine blanks?

Adding a fourth row to Filter — **causal filtering**, select items by whether they causally affect an outcome — looked promising. But [Duan, Wasserman & Ramdas (2024)](https://doi.org/10.1515/jci-2023-0059) already composed the DR-learner + conformal + FDR stack for causal × bounded. [Weighted conformal selection](https://academic.oup.com/biomet/article/doi/10.1093/biomet/asaf066/8250683) (Biometrika 2025) extends it. The grid predicted the composition; the composition already exists. More validation.

Perceive has one blank: learned codebook × stream, where no online tokenizer satisfies the contract (parseable, backward-compatible, bounded retokenization). Attend fills completely. One blank in two dimensions. The grid has a deeper problem.

### Ten axes

The grids above are two-dimensional. Each one picks two axes and draws a plane. But the design space has more than two dimensions. How many?

An axis is a dimension if it's discrete, orthogonal to the others, and crossing it with at least one other axis produces cells that aren't trivially occupied or trivially empty. By that test, there are ten.

Four are universal — they apply to every pipeline stage:

1. **Pipeline stage**: perceive, cache, filter, attend, consolidate, remember
2. **Data structure**: flat, sequence, tree, graph, partial order
3. **Error guarantee**: exact, bounded, probabilistic
4. **Temporality**: batch, stream

Six are stage-specific — they partition one stage's operations but don't generalize:

<ol start="5">
<li><strong>Selection semantics</strong> <em>(Filter)</em>: predicate, similarity, dominance, causal</li>
<li><strong>Stationarity</strong> <em>(Filter)</em>: static criterion, drifting criterion</li>
<li><strong>Output form</strong> <em>(Attend)</em>: top-k slate, single best, path/tree</li>
<li><strong>Redundancy control</strong> <em>(Attend)</em>: none, implicit, explicit</li>
<li><strong>Codebook type</strong> <em>(Perceive)</em>: fixed, learned</li>
<li><strong>Supervision signal</strong> <em>(Consolidate)</em>: unsupervised, supervised, self-supervised</li>
</ol>

Ten axes, forty-five possible planes. Most planes are uninteresting — crossing codebook type with stationarity doesn't produce anything you'd look up. Five planes are the ones practitioners would actually reach for.

### Five planes

The grids so far explored two planes: selection semantics × error guarantee (Filter) and output form × redundancy control (Attend). Both fill on sight. Adding three more planes is where the blanks appear.

**Plane 3: Data structure × Selection semantics** (bounded error). "My data has structure. What filters exist?"

Error guarantee fixed at **bounded**. Data structure × selection semantics:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Predicate</th><th style="background:#f0f0f0">Similarity</th><th style="background:#f0f0f0">Dominance</th><th style="background:#f0f0f0">Causal</th></tr></thead>
<tr><td><strong>Flat</strong></td><td>Threshold filtering</td><td>k-NN radius pruning</td><td>ε-dominance</td><td><a href="https://doi.org/10.1515/jci-2023-0059">Conformal causal selection</a></td></tr>
<tr><td><strong>Sequence</strong></td><td>Change-point detection</td><td>DTW pruning</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Tree</strong></td><td>XPath + depth bound</td><td>Tree edit distance threshold</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#e8f4e8"><a href="https://doi.org/10.1002/sim.9900">Luo & Guo</a><sup>†</sup></td></tr>
<tr><td><strong>Graph</strong></td><td>Approx subgraph match</td><td>Graph kernel pruning</td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Partial order</strong></td><td><a href="https://doi.org/10.1093/biomet/asy066">DAGGER</a></td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#e8f4e8"><a href="https://doi.org/10.1093/biomet/asy066">Smoothed nested testing</a><sup>†</sup></td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

<small><sup>†</sup> Thin: occupies a narrow interpretation of the cell.</small>

The flat row fills completely — the 4×3 grid validated this. Everything below it is new. The predicate and similarity columns fill quickly — CS has been filtering structured data by predicate and proximity for decades. The right half empties out, but not uniformly.

Three cells that looked blank turned out to be occupied. [DAGGER](https://doi.org/10.1093/biomet/asy066) (Ramdas et al., Biometrika 2019) does FDR-controlled hypothesis filtering on DAGs, filling partial order × predicate. [Luo & Guo (2023)](https://doi.org/10.1002/sim.9900) filters branches of subgroup trees by causal effect with error control, filling tree × causal for prespecified hierarchies. [Smoothed nested testing](https://ideas.repec.org/a/oup/biomet/v109y2022i2p457-471..html) (Biometrika 2022) handles dominance on hypothesis posets. Each occupies a narrow reading of its cell. The broader versions remain open.

### Why the right half empties

The blanks cluster because dominance and causal filtering were designed for flat collections. Pareto assumes independent objective vectors — each item is a point in ℝ^d, dominance is coordinate-wise. Causal effect estimation assumes pointwise treatment assignment. Structure breaks both assumptions. Order constrains which comparisons are valid. Hierarchy nests effects. Adjacency creates interference.

The dominance column shows the pattern most clearly. Exact dominance on structured data has scattered coverage — [skyline community search](https://doi.org/10.1145/3183713.3183736) (SIGMOD 2018) for graphs, [TSS](https://researchportal.hkust.edu.hk/en/publications/topologically-sorted-skylines-for-partially-ordered-domains) for partial orders, trajectory skylines for sequences. But every one of these is exact. Nobody has built the bounded-error variant for any of them. Four cells, same gap: the pieces exist for scoring, the FDR/FPR machinery exists for bounding, and the composition hasn't been attempted.

The causal column has the same shape. [CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html) estimates effects on time series but doesn't gate with bounded error. Tree × causal has [Luo & Guo](https://doi.org/10.1002/sim.9900) for subgroup hierarchies, but arbitrary tree-structured objects remain open. Causal inference on known DAGs is a mature field, yet "filter graph nodes whose interventional effect exceeds τ with bounded error" has no standard algorithm. The pieces are closest for graphs. The composition is missing.

The bottom row is the most striking. Partial orders are everywhere — dependency graphs, taxonomies, version histories, lattices of formal concepts. Predicate filtering has DAGGER. Dominance has [smoothed nested testing](https://ideas.repec.org/a/oup/biomet/v109y2022i2p457-471..html) under the hypothesis-poset reading. Similarity and causal are empty. Partial order × similarity is the most conceptually interesting blank: similarity filtering assumes a metric space, but partial orders don't have distances — they have reachability. What does "similar" mean when some pairs of items are incomparable?

### Plane 4: Temporality × Selection semantics

Hold the error guarantee at **bounded** again and swap data structure for temporality. "I'm processing a stream. What can I filter by?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Predicate</th><th style="background:#f0f0f0">Similarity</th><th style="background:#f0f0f0">Dominance</th><th style="background:#f0f0f0">Causal</th></tr></thead>
<tr><td><strong>Batch</strong></td><td>Threshold filtering</td><td>k-NN radius pruning</td><td>ε-dominance</td><td><a href="https://doi.org/10.1515/jci-2023-0059">Conformal causal selection</a></td></tr>
<tr><td><strong>Stream</strong></td><td><a href="https://en.wikipedia.org/wiki/Count%E2%80%93min_sketch">Count-Min Sketch</a></td><td>Streaming LSH</td><td><a href="http://personal.denison.edu/~lalla/papers/skyline-vldb09.pdf">Sliding window skyline</a></td><td style="background:#e8f4e8"><a href="https://arxiv.org/abs/1808.04904">Xie et al.</a><sup>†</sup></td></tr>
</table>

Both rows fill. The batch row validates — conformal causal selection closes that cell. The streaming row fills aggressively: Count-Min Sketch and Stable Bloom Filters for predicates, LSH variants for similarity, [sliding window skylines](https://cse.hkust.edu.hk/~dimitris/PAPERS/TKDE06-Sky.pdf) (Tao et al.) and [randomized multi-pass skylines](http://personal.denison.edu/~lalla/papers/skyline-vldb09.pdf) (Das Sarma et al., VLDB 2009) for dominance.

Streaming × causal is the thinnest cell. [Xie et al. (2018)](https://arxiv.org/abs/1808.04904) does FDR-controlled heterogeneous treatment effect detection for online A/B experiments, but only for that narrow setting. A general streaming causal filter (streaming CATE estimation, online confidence sequences, sequential FDR control composed into a single gate) doesn't exist. The cell is occupied if you squint.

Temporality alone doesn't empty the grid. Streaming algorithms have been built aggressively for predicate, similarity, and dominance. The gaps live at the intersection: streaming *and* structured *and* causal. All three assumptions break at once.

### Plane 5: Pipeline stage × Data structure

The overview map. "For this data structure, which stages have gaps?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Flat</th><th style="background:#f0f0f0">Sequence</th><th style="background:#f0f0f0">Tree</th><th style="background:#f0f0f0">Graph</th><th style="background:#f0f0f0">Partial order</th></tr></thead>
<tr><td><strong>Perceive</strong></td><td>JSON parsing</td><td>A/D conversion</td><td>XML parsing</td><td>Edge list parsing</td><td style="background:#e8f4e8">PC algorithm<sup>†</sup></td></tr>
<tr><td><strong>Cache</strong></td><td>Hash index</td><td>B-tree</td><td>Trie</td><td>Adjacency index</td><td style="background:#e8f4e8">Transitive closure<sup>†</sup></td></tr>
<tr><td><strong>Filter</strong></td><td>WHERE</td><td>Change-point</td><td>XPath</td><td>Subgraph match</td><td style="background:#e8f4e8">DAGGER<sup>†</sup></td></tr>
<tr><td><strong>Attend</strong></td><td>MMR</td><td>Beam search</td><td>MCTS</td><td><a href="https://doi.org/10.14778/2536258.2536263">Div. top-k</a></td><td style="background:#fff3cd"><em>blank</em></td></tr>
<tr><td><strong>Consolidate</strong></td><td>Gradient descent</td><td>Grammar induction</td><td>Decision tree induction</td><td>GNN training</td><td style="background:#e8f4e8">Lattice learning<sup>†</sup></td></tr>
<tr><td><strong>Remember</strong></td><td>WAL append</td><td>SSTable flush</td><td>Git commit</td><td>Graph DB commit</td><td>Topological serialization</td></tr>
</table>

<small><sup>†</sup> Thin: 1–2 algorithms exist but no standard toolkit.</small>

The partial order column is the weak column. Perceive and Cache have algorithms but they're thin — PC algorithm for causal discovery, transitive closure for indexing. Filter has one solid entry (DAGGER). Attend is blank — no standard algorithm ranks items in a partial order with diversity and bound. Consolidate has lattice learning but it's algebraic CS, not mainstream. Remember is the only stage where partial orders are well-served (topological sort is standard).

Attend × partial order is a genuine blank. Linear extension enumeration is combinatorially explosive. DPP-style diversity requires a kernel over a metric space, but partial orders have reachability, not distance. The contract demands top-k diverse from a poset. The algorithm doesn't exist.

### What the blanks tell us

The first two planes filled on sight — twelve cells each, all occupied. That's the parts bin doing its job: validation. The next three planes are where the blanks appear.

The data structure plane (plane 3) empties whenever dominance or causality meets structure. The temporality plane (plane 4) fills almost completely — streaming algorithms are mature — but confirms the causal column is the thinnest across every slice. The stage × structure plane (plane 5) shows partial orders are thin across the entire pipeline and blank at Attend. Eight genuine blanks survive validation. They cluster around three broken assumptions:

1. **Dominance assumes independence.** Pareto filtering treats each item as a point in ℝ^d. Structure introduces dependencies — order constrains comparisons, adjacency creates interference. Four cells empty.
2. **Causal estimation assumes pointwise treatment.** Structure introduces spillover, nesting, and temporal lag. Three cells empty (plus the thin streaming cell).
3. **Diversity assumes a metric space.** Attend needs distances between items to enforce redundancy control. Partial orders have reachability, not distance. One cell empty.

Mendeleev predicted germanium's density before anyone found the element. I-Con predicted a new algorithm. These blanks predict compositions: the pieces exist in separate literatures (skyline queries, causal inference, FDR control, graph kernels, poset theory), and the contract names what they must satisfy when assembled. Ten axes tell you where to look. Five planes tell you where to build. The grid writes the spec. The spec is eight algorithms nobody's built.

### Composition sketches

Three of the eight blanks have compositions close enough to sketch. Each wires existing libraries into a pipeline that satisfies the contract: input strictly larger than output, bounded FDR.

**Sequence × Causal (bounded).** For each time-series segment: fit [CausalImpact](https://google.github.io/CausalImpact/CausalImpact.html) to estimate the intervention effect, compute a [split-conformal](https://proceedings.mlr.press/v162/fisch22a.html) interval from pre-period residuals, derive a one-sided p-value for effect > τ, and feed it to [SAFFRON](https://proceedings.mlr.press/v80/ramdas18a.html) for online FDR control. Accept segments where both the conformal lower bound exceeds the threshold and the online test rejects. FDR ≤ α under SAFFRON's dependence assumptions. Pieces: `causalimpact`, `mapie`, custom SAFFRON implementation.

**Graph × Causal (bounded).** For each node in a known causal DAG: identify the estimand via [DoWhy](https://github.com/py-why/dowhy), estimate the node-specific interventional effect with doubly robust estimation under an [exposure mapping](https://www.frontiersin.org/articles/10.3389/fdata.2023.1128649/full) that accounts for network spillover, compute a one-sided p-value for effect > τ, and apply [Benjamini-Hochberg](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Hochberg_procedure) across all nodes. FDR ≤ α under independence/PRDS; use [BY](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Yekutieli_procedure) for arbitrary dependence. Pieces: `dowhy`, `causallib`, `networkx`, `statsmodels`.

**Sequence × Dominance (bounded).** For each trajectory: evaluate objectives in temporal order, compute pairwise [conformal p-values](https://proceedings.mlr.press/v162/fisch22a.html) for "trajectory j dominates trajectory i," aggregate per-trajectory with Bonferroni, and correct across trajectories with BY. Retain trajectories whose domination null is not rejected. P(retaining a truly dominated trajectory) ≤ α. Pieces: `paretoset`, `mapie`, `statsmodels`.

The remaining five blanks need definitions before they need code. "Subtree dominates subtree" and "top-k diverse from a poset" are design choices waiting for a specification, not compositions waiting for assembly.

---

*Written via the [double loop](/double-loop).*
