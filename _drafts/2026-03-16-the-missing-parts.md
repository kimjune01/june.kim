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

The design space has ten dimensions. An axis qualifies if it's discrete, orthogonal, and crossing it with another axis produces cells that aren't trivially occupied or empty.

Four are universal:

1. **Pipeline stage**: perceive, cache, filter, attend, consolidate, remember
2. **Data structure**: flat, sequence, tree, graph, partial order, embedding space
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

Ten axes, forty-five possible planes. Most are uninteresting. Four have blanks worth building.

### Planes that validate

The Parts Bin drew two planes that fill on sight: selection semantics × error guarantee (Filter, 3×3) and output form × redundancy control (Attend, 3×3). Three more planes also fill completely, confirming the taxonomy works at each new crossing:

**Stationarity × Selection semantics** (bounded error). [ADWIN](https://dl.acm.org/doi/10.1145/1150402.1150423) handles drifting predicates. [Dynamic skyline queries](https://www.mdpi.com/2220-9964/6/5/137) handle drifting dominance criteria. [Weighted conformal p-values under covariate shift](https://academic.oup.com/biomet/advance-article/doi/10.1093/biomet/asaf066/8250683) (Biometrika 2025) handles drifting causal filtering. All cells occupied.

**Temporality × Selection semantics** (bounded error). Streaming predicate filtering has [Count-Min Sketch](https://en.wikipedia.org/wiki/Count%E2%80%93min_sketch). Streaming similarity has LSH variants. Streaming dominance has [sliding window skylines](https://cse.hkust.edu.hk/~dimitris/PAPERS/TKDE06-Sky.pdf). Streaming causal has [Xie et al. (2018)](https://arxiv.org/abs/1808.04904) for online A/B experiments. All cells occupied.

Five fully-occupied planes. The grid validates. Now for the blanks.

### Planes that predict

**Plane 1: Data structure × Selection semantics** (bounded error). "My data has structure. What filters exist?"

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Predicate</th><th style="background:#f0f0f0">Similarity</th><th style="background:#f0f0f0">Dominance</th><th style="background:#f0f0f0">Causal</th></tr></thead>
<tr><td><strong>Flat</strong></td><td>Threshold filtering</td><td>k-NN radius pruning</td><td>ε-dominance</td><td><a href="https://doi.org/10.1515/jci-2023-0059">Conformal causal selection</a></td></tr>
<tr><td><strong>Sequence</strong></td><td>Change-point detection</td><td>DTW pruning</td><td><a href="https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z">Dominant skyline over time series</a></td><td>Operant conditioning (Filter-Remember couple)</td></tr>
<tr><td><strong>Tree</strong></td><td>XPath + depth bound</td><td>Tree edit distance threshold</td><td>Tree inclusion filter (Kilpeläinen-Mannila)</td><td style="background:#e8f4e8"><a href="https://doi.org/10.1002/sim.9900">Luo & Guo</a><sup>†</sup></td></tr>
<tr><td><strong>Graph</strong></td><td>Approx subgraph match</td><td>Graph kernel pruning</td><td><a href="https://weiguozheng.github.io/pub/tkde16-skyline.pdf">Subgraph skyline</a></td><td><a href="/return-to-sender">Graph causal filter</a> (Filter-Remember couple)</td></tr>
<tr><td><strong>Partial order</strong></td><td><a href="https://doi.org/10.1093/biomet/asy066">DAGGER</a></td><td style="background:#fff3cd"><em>blank</em></td><td style="background:#e8f4e8"><a href="https://ideas.repec.org/a/oup/biomet/v109y2022i2p457-471..html">Smoothed nested testing</a><sup>†</sup></td><td style="background:#fff3cd"><em>blank</em></td></tr>
</table>

<small><sup>†</sup> Thin: occupies a narrow interpretation of the cell.</small>

The flat row fills completely. Everything below it is new. The predicate and similarity columns fill quickly. The dominance column mostly fills: [dominant skyline over multiple time series](https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z) (2013) handles sequences, [subgraph skyline](https://weiguozheng.github.io/pub/tkde16-skyline.pdf) (TKDE 2016) handles graphs. Tree × dominance remains open.

Two blanks. The causal column was the emptiest, but two cells now fill via the same structural insight: causal filtering requires intervention, and intervention is a Filter-Remember couple — the selection *is* the environmental write. Operant conditioning fills sequence × causal (every animal with a nervous system runs it). The [graph causal filter](/return-to-sender) fills graph × causal (exposure mappings → e-values → e-BH). Both are unfillable from observation alone; both fill once the system acts on what it selects. [Luo & Guo (2023)](https://doi.org/10.1002/sim.9900) fills tree × causal thinly for prespecified subgroup hierarchies. Partial order × similarity is the most conceptually interesting remaining blank: similarity filtering assumes a metric space, but partial orders have reachability, not distance.

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

Causal filtering on structured data was the emptiest region until the [Filter-Remember couple](/union-find-compaction) resolved two cells. The insight: causal filtering requires intervention, and for an acting system, the filter decision *is* the intervention. Operant conditioning fills sequence × causal — the agent's action is simultaneously a selection and an experiment, with pair frequency as the causal estimate and extinction as the filter. The [graph causal filter](/return-to-sender) fills graph × causal by composing exposure mappings, doubly robust scores, e-values, and e-BH. Both are unfillable from pure observation. Both fill once the system has the full six roles — because Consolidate creates the precondition (intervention policy) that Filter needs.

Dominance on trees was the lone holdout in its column. The definition was the missing piece, not the algorithm. [Tree inclusion](https://epubs.siam.org/doi/abs/10.1137/S0097539791218202) (Kilpeläinen & Mannila 1995) defines the relation: T₁ dominates T₂ if T₂ can be obtained from T₁ by deleting nodes and reconnecting children. That's injective, ancestor-preserving containment — a natural partial order on trees. The non-dominated set under tree inclusion is computable in O(n² · |P| · |T|) via candidate-set filtering. Approximate containment via [Pinter et al. (2007)](https://www.sciencedirect.com/science/article/pii/S1570866707000780) gives the bounded-error variant. The frequent subtree mining community (CMTreeMiner, Chi et al. 2004) already computed maximal sets under this relation — they just never called it a dominance filter.

Partial order × similarity is the most conceptually interesting blank: similarity filtering assumes a metric space, but partial orders have reachability, not distance. What does "similar" mean when some pairs of items are incomparable?

### What the blanks tell us

Five blanks survive validation across four planes. They cluster around two broken assumptions:

1. **Causal estimation assumes observation.** The literature searched for pure Filter algorithms on observational data. Two cells (sequence, graph) dissolve once you allow intervention — a Filter-Remember couple where selection *is* the environmental write. Partial order × causal remains open: the order relation complicates both intervention design and effect propagation.
2. **Diversity and similarity assume a metric space.** Partial orders have reachability, not distance. Two cells empty (similarity in plane 1, attend in plane 3).

Plus one in Perceive (learned codebook × stream, plane 2).

The grid's first contribution is making cells addressable. Without the grid, nobody searches for "bounded-error dominance filtering on time series" because that combination of concepts has no name. The [time series skyline paper](https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z) from 2013 exists, but you'd never find it unless you knew to cross those two axes. And even when you find a paper, judging whether it fills the cell requires checking the contract: does it satisfy bounded error? Does it respect temporal order? Is it a filter (strictly smaller output) or something else? The grid writes the question. The question is still hard to answer.

For each blank, adjacent work exists: nearby algorithms that solve a restricted version or a related problem. The grid names the cell. The adjacent work names the near-miss. [Filling the Blanks](/filling-the-blanks) develops all eight compositions, each [implemented and tested](https://github.com/kimjune01/filling-the-blanks).

---

*Written via the [double loop](/double-loop).*
