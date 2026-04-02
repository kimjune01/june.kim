---
variant: post-wide
title: "Lego with Algorithms"
tags: cognition, methodology
---

*Part of the [cognition](/cognition) series. Builds on [The Parts Bin](/the-parts-bin).*

Cognitive architectures look like inventions. ACT-R. CLARION. DreamCoder. Cobweb. Each has a name, a lab, a body of literature. Each feels like a thing someone built from scratch.

They're Lego. Assembled from algorithms that already had names, proofs, and provenance. The novelty lives in the coupling: which parts to connect, in what order, under what theory.

### The parts

Four architectures, decomposed. Every row is a named algorithm with independent provenance. The **Role** column maps to the [Parts Bin](/the-parts-bin) grid.

<div class="table-wrap">

**ACT-R** — Anderson & Lebiere, 1998

| Component | What it does | Role | Borrowed from |
|-----------|-------------|------|---------------|
| Power-law decay | Tracks memory availability by recency and frequency | Remember | [Ebbinghaus, 1885](https://en.wikipedia.org/wiki/Forgetting_curve) |
| Spreading activation | Boosts contextually relevant memories | Attend | Quillian, 1967; [Collins & Loftus, 1975](https://en.wikipedia.org/wiki/Spreading_activation) |
| Softmax / Luce choice rule | Converts activations into retrieval probabilities | Attend | [Luce, 1959](https://en.wikipedia.org/wiki/Luce%27s_choice_axiom); Boltzmann, 1868 |
| Partial matching | Penalizes imperfect matches by similarity | Filter | [Shepard, 1987](https://en.wikipedia.org/wiki/Universal_law_of_generalization) |
| Blended value | Averages across retrieved instances | Consolidate | [Nadaraya-Watson, 1964](https://en.wikipedia.org/wiki/Kernel_regression) |
| Retrieval threshold | Gates out memories below a criterion | Filter | Neyman-Pearson, 1933 |

**Original contribution:** *Rational analysis* — a Bayesian argument for why these parts compose. Each term in the activation equation is a factor in the posterior odds that a memory will be needed.

</div>

<div class="table-wrap">

**CLARION** — Sun, Merrill & Peterson, 2001

| Component | What it does | Role | Borrowed from |
|-----------|-------------|------|---------------|
| Q-Learning + Backpropagation | Trains implicit (subsymbolic) level | Consolidate | [Watkins, 1989](https://en.wikipedia.org/wiki/Q-learning); [Rumelhart et al., 1986](https://en.wikipedia.org/wiki/Backpropagation) |
| Boltzmann selection | Picks actions from Q-values | Attend | Luce, 1959 (same part as ACT-R) |
| Information gain | Evaluates rule quality for refinement | Filter | Lavrač & Džeroski, 1994 |
| Rule generalization / specialization | Traverses a generality lattice to broaden or narrow rules | Consolidate | Sun et al., 2001 |
| Weighted-sum integration | Combines implicit and explicit recommendations | Attend | Maclin & Shavlik, 1994 |
| Rule extraction (positivity gate) | Creates explicit rule when implicit level succeeds | Filter | Sun et al., 1996 |

**Original contribution:** *The coupling* — bottom-up extraction, top-down assimilation, and IG-based lattice traversal that refines rules across the implicit/explicit boundary.

</div>

<div class="table-wrap">

**Cobweb** — Fisher, 1987

| Component | What it does | Role | Borrowed from |
|-----------|-------------|------|---------------|
| Category Utility | Scores competing tree operations | Attend | [Gluck & Corter, 1985](https://en.wikipedia.org/wiki/Category_utility); Gini, 1912 |
| Incorporate | Routes instance down best branch | Filter | Kolodner, 1984; Lebowitz, 1987 |
| Create | Adds a new leaf node | Cache | Fisher, 1987 |
| Merge / Split | Restructures tree from accumulated evidence | Consolidate | Fisher, 1987 |
| Count update | Writes frequencies to each node | Remember | Frequency estimation (MLE) |

**Original contribution:** *Category utility as the universal scoring function* — one metric drives all four tree operators. Five roles in a single function call.

</div>

<div class="table-wrap">

**DreamCoder** — Ellis et al., PLDI 2021

| Component | What it does | Role | Borrowed from |
|-----------|-------------|------|---------------|
| Type-guided enumeration | Searches for programs that solve tasks | Attend | Ellis et al., 2018; Hindley, 1969 |
| Recognition model (GRU) | Prunes irrelevant productions per task | Filter | Helmholtz Machine, Dayan et al., 1995 |
| Helmholtz enumeration | Generates synthetic training data | Cache | Dayan, Hinton et al., 1995 |
| Inside-Outside (EM for PCFGs) | Re-estimates grammar weights | Consolidate | [Baker, 1979](https://en.wikipedia.org/wiki/Inside%E2%80%93outside_algorithm) |
| MDL scoring | Gates which fragments enter the library | Filter | [Rissanen, 1978](https://en.wikipedia.org/wiki/Minimum_description_length) |
| Version space compression | Compresses program library via inverse beta-reduction | Consolidate | **Ellis et al., 2021** |

**Original contribution:** *Version space compression* — n-step inverse beta-reduction over hash-consed DAGs.

</div>

### The pattern

Four architectures, twenty-three components, four original contributions.

Decomposition isn't the whole story. Representation choices and training dynamics matter too. But when people call an architecture novel, the novelty almost always sits in the coupling. Anderson had rational analysis. Sun had dual-process theory. Fisher had category utility. Ellis had wake-sleep with library compression. Each invented *a reason to connect these parts in this order*.

The algorithms are cheap to look up. They have names. The composition is expensive to discover.

### The Parts Bin

[The Parts Bin](/the-parts-bin) makes the lookup explicit. Six roles, six data structures, thirty-six cells. Each cell lists the algorithms that satisfy that role's [contract](/the-handshake) over that structure.

If you're building a cognitive architecture, you don't need to invent algorithms. You need to:

1. **[Diagnose](/diagnosis-soar)** which roles your architecture is missing.
2. **Look up** which algorithms fill those roles in the grid.
3. **Wire** them together — that's your contribution.

The algorithms have names because someone already did the hard work. What's left is the wiring. That's the architecture. That's yours to invent.
