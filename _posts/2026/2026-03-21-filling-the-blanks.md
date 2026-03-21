---
layout: post-wide
title: "Filling the Blanks"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Missing Parts](/the-missing-parts).*

### Three blanks

[The Missing Parts](/the-missing-parts) crossed ten axes of the design space — pipeline stage, data structure, error guarantee, temporality, and six stage-specific dimensions — and found seven cells where the grid says an algorithm should exist and a literature search turns up nothing. A blank means: the axes name a well-defined contract (output strictly smaller than input, bounded error, diversity enforced), and no known algorithm satisfies it.

The gap is compositional. The pieces exist in separate literatures. Three of the seven blanks can be filled by wiring known techniques with one new piece each:

1. **Graph × Dominance** — comparing overlapping communities when shared structure inflates the comparison.
2. **Partial order × Causal** — estimating treatment effects when the treatment unit is a closure, not a point.
3. **Attend × Partial order** — selecting a diverse top-k from a poset where distance has no meaning.

Each composition is [implemented and tested against its contract and reduction cases](https://github.com/kimjune01/filling-the-blanks). The tests verify boundary behavior (does it reduce to the known algorithm when structure vanishes?) and contract compliance (is output strictly smaller? is the bound respected?). They don't prove the algorithms are useful on real data. That's a different kind of work.

### 1. Residualized dominance

**The blank.** Dominance filtering asks: does item A beat item B on every objective? Sequences have [dominant skyline over time series](https://jcst.ict.ac.cn/en/article/doi/10.1007/s11390-013-1363-z) (2013). Graphs have [subgraph skyline](https://weiguozheng.github.io/pub/tkde16-skyline.pdf) (TKDE 2016). But subgraph skyline compares non-overlapping subgraphs. When communities share members, the shared structure inflates both sides equally.

**Why it's empty.** [Skyline community search](https://doi.org/10.1145/3183713.3183736) (SIGMOD 2018) does exact dominance over community attributes but treats each community as atomic. [Group skyline](https://doi.org/10.1016/j.ins.2021.12.028) compares sets but doesn't subtract shared members. Neither decomposes the comparison into what's shared and what's marginal.

**The failure mode.** Three research groups share a star postdoc (output: 50 papers). Group A has the postdoc plus a junior researcher (2 papers). Group B has the postdoc plus a senior researcher (8 papers). Raw objectives: A = 52, B = 58. B dominates A. But the real question is whether B's *unique* contribution beats A's. Residuals: A contributes 2, B contributes 8. B still dominates — but now imagine Group C also has the postdoc, with objectives 51. Raw: C looks nearly tied with A (52 vs 51). Residuals: C contributes 1 vs A's 2. A dominates C. Without residualization, the 50-paper postdoc makes all three groups look similar. With it, the marginal differences are exposed.

**The algorithm.** Factor out shared substructure before comparing. For communities C₁ and C₂ with overlap I:

1. Decompose into residuals: R₁ = C₁ \ I, R₂ = C₂ \ I.
2. Compute marginal contributions: g(R₁ | I) and g(R₂ | I) for each objective — the value added by the residual given the shared base.
3. Dominance test: C₁ ≤ C₂ iff g(R₁ | I) ≤ g(R₂ | I) on every objective, strictly on at least one.

**The new piece** is the residualization step. Standard skyline queries compare raw attribute vectors. This decomposes the vector into shared and marginal components, then compares only the marginal. It's a straightforward adaptation — the non-obvious part is that nobody in the skyline literature has done it, despite overlap being the common case in community detection.

**Filter implementation.** Estimate overlap via minhash sketches. Compute residual bounds from sketch intersection sizes. Prune pairs where the upper bound of one residual is dominated by the lower bound of the other. Only resolve ambiguous pairs exactly. Error guarantee comes from the sketch's collision bound.

**Reductions.** No overlap → residuals equal the full communities → standard group skyline. Singleton communities → ordinary Pareto dominance. Both cases pass in the [test suite](https://github.com/kimjune01/filling-the-blanks).

### 2. Closure-level causal effects

**The blank.** Causal filtering on flat data is solved: [conformal causal selection](https://doi.org/10.1515/jci-2023-0059) (Duan, Wasserman & Ramdas 2024) gates items by treatment effect with bounded FDR. But flat data assumes pointwise treatment: treat one unit, observe one effect. Partial orders break this. In a poset where a ≤ b means "a is a prerequisite for b," treating b requires first treating everything below it.

**Why it's empty.** [Shpitser & Tchetgen Tchetgen (2016)](https://doi.org/10.1214/15-AOS1411) study hierarchical interventions but don't define a filterable estimand. [Forastiere et al. (2016)](https://www.emergentmind.com/papers/1609.06245) handle network interference but the interference pattern is arbitrary, not order-constrained. No prior work defines the unit of treatment as an order-theoretic closure.

**The failure mode.** An org chart: CEO ≤ VP ≤ Engineer. You want to know whether training the Engineer improves output. But training the Engineer requires first training the VP (who supervises), which requires training the CEO (who approves the budget). The standard ATE asks: "what's the effect of training the Engineer?" The closure-level estimand asks: "what's the effect of training {CEO, VP, Engineer} vs the status quo?" — because that's the actual intervention. Pointwise ATE misattributes the VP's and CEO's contributions to the Engineer.

**The estimand.** The order runs upward: a ≤ b means a is below b, a must be treated before b can be. Treating node x means treating its entire downward closure: T(x) = ↓{x} = {y : y ≤ x}. The causal effect is:

> τₓ = E[Y(S₀ ∪ T(x)) − Y(S₀)]

where S₀ is the baseline treated set. Intervening at a leaf is cheap (small closure). Intervening near the root treats an entire branch.

**The new piece** is the closure-level estimand itself. Existing causal inference assumes the treatment is a binary toggle on a unit. Here the treatment is a set determined by the order structure.

**The central limitation.** Identification requires positivity over feasible closures: you must observe both treated and untreated versions of each closure. Deep posets have large closures with thin support — the deeper the intervention point, the fewer observations where that exact closure happened to be untreated. This is the structural reason this cell was empty. Shallow posets (wide trees, flat hierarchies) have tractable closures. Deep chains may not.

**Estimation.** Observe outcomes under naturally occurring treatment patterns. Fit an outcome model with isotonic constraints (if x ≤ y and x is treated, y must be treated — the model respects this). Correct for selection bias via propensity scores estimated over feasible closures. Threshold: gate nodes where the lower confidence bound on τₓ exceeds the threshold, apply [Benjamini-Hochberg](https://en.wikipedia.org/wiki/False_discovery_rate#Benjamini%E2%80%93Hochberg_procedure) across all nodes for FDR control.

**Reductions.** Discrete poset (no edges) → closures are singletons → standard ATE per node. Tree poset → closures are subtrees → natural intervention unit for hierarchical policies (treat a department = treat everyone in it). Both cases [tested](https://github.com/kimjune01/filling-the-blanks).

### 3. Diverse top-k from a poset

**The blank.** Attend requires: output a bounded-size set that is ranked by relevance and diverse. On flat data, [MMR](https://doi.org/10.1145/3130348.3130369) and [DPP](https://arxiv.org/abs/1207.6083) deliver this by defining diversity as distance in a metric space. Partial orders have reachability, not distance. Two items might be incomparable — neither above nor below the other — without any notion of "how far apart" they are.

**Why it's empty.** DPP requires a kernel over a feature space. Submodular maximization needs a set function that rewards spread. Both assume you can measure how different two items are. In a poset, comparable items are redundant (one subsumes the other) and incomparable items are diverse (neither subsumes the other), but "how diverse" has no natural scale.

**The failure mode.** A taxonomy of skills: Programming ≤ Backend ≤ Databases, Programming ≤ Frontend ≤ React, Programming ≤ Frontend ≤ CSS. A job board wants to show 2 diverse skills from a candidate's profile. Relevance-only top-k might pick Databases and React (both high-demand). But Backend and Frontend share a parent — a candidate with both is less surprising than one with Databases and CSS, which sit on fully separate branches. Without order-aware diversity, the algorithm can't distinguish "redundant because related" from "diverse because independent."

**The kernel.** Define similarity from order context:

> Sim(x, y) = α · J(↓x, ↓y) + β · J(↑x, ↑y) + γ · C(x, y)

where ↓x and ↑x are the downset and upset (all elements below/above x), J is Jaccard similarity, and C(x, y) is a comparability term (1 if one element is above the other, 0 otherwise). Diversity is the complement: D(x, y) = 1 − Sim(x, y).

Why these three terms: downset overlap measures shared ancestry (similar roots → similar items). Upset overlap measures shared descendants (similar consequences → similar items). The comparability term penalizes selecting both x and its ancestor, since one subsumes the other. The linear combination is a heuristic — a principled choice would require a task-specific loss function — but it has useful boundary behavior: zero for items with disjoint context, one for identical items, and the weights let you tune whether ancestry or descendancy matters more for your domain.

**The new piece** is using order-theoretic context as a similarity kernel for diversification. [simona](https://doi.org/10.1186/s12864-024-10759-4) (Gu 2024) uses Jaccard on ancestor sets for biomedical ontologies, but only as a comparison tool. Plugging the symmetric formulation into an MMR loop with a diversity contract is the new step.

**Implementation.** MMR-style greedy: at each step, select the element maximizing (1 − λ) · relevance(x) − λ · max-similarity-to-selected(x). Higher λ pushes harder toward diversity. λ = 0 recovers pure relevance ranking. The greedy loop is O(k·n) per selection round, with similarity computed from precomputed downsets and upsets.

**Reductions.** Discrete poset → all pairwise similarities are zero → pure relevance top-k. Total order → adjacent elements are maximally similar → selections spread across the ranking. In a tree, the algorithm picks from different branches before doubling up within one. All cases [tested](https://github.com/kimjune01/filling-the-blanks).

### What filling tells us

Three blanks, three compositions. Each wires known techniques with one new piece: a residualization step, a closure-level estimand, a poset similarity kernel. None of the new pieces required new mathematics. Each is a straightforward adaptation that nobody made because nobody had a name for the cell.

The grid helped surface these candidate compositions by naming the intersection of axes where a contract exists but no algorithm does. Three turned out to be compositional — fillable by assembling existing pieces with one new operation. Four remain: Sequence × Causal, Tree × Dominance, Graph × Causal, and Partial order × Similarity. Each is blocked on definitions or identification conditions, not just assembly.

---

*Written via the [double loop](/double-loop).*
