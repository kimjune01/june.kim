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

### What the blanks tell us

Mendeleev predicted germanium's density before anyone found the element. I-Con predicted a new algorithm. These blanks predict something more specific: *compositions*. The pieces exist. The contract names what they must satisfy when assembled. The grid writes the spec.

The causal filter blank has a 4-step composition sketch, six literature entry points, and three application domains waiting. That's not "something goes here." That's a build order.

---

*Written via the [double loop](/double-loop).*
