---
variant: post-wide
title: "Ambient Category"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Type Forcing](/type-forcing).*

[Type Forcing](/type-forcing) showed the wiring is unique. It said nothing about what flows through the wires. [Spivak's operad](https://arxiv.org/abs/1305.0297) gives syntax: what plugs into what. The semantics, what each morphism does to information passing through it, needs a different formalism. [Tobias Fritz](https://tobiasfritz.science/) built it. His [Markov categories](https://arxiv.org/abs/1908.07021) axiomatize the ambient category the pipeline lives in: **Stoch**, measurable spaces and Markov kernels, where probability is structure.

Fritz gives the pipeline stochastic semantics: a formal account of randomness, information loss, and the deterministic/stochastic boundary. But neither his framework nor Spivak's formalizes **contracts**: predicates on morphisms, preserved under composition and iteration, that distinguish a pipeline stage from an arbitrary channel. *Gated* means the output is strictly smaller than the input. *Ranked* means the output is ordered, diverse, and bounded. The question is whether contracts require a third formal layer or fall out of the first two.

## The equation that fails

Fritz's [foundational paper](https://arxiv.org/abs/1908.07021) (2020, *Advances in Mathematics*) defines a **Markov category** as a symmetric monoidal category where every object X comes with two structure morphisms: **copy** (X → X ⊗ X) and **delete** (X → I). Copy duplicates; delete discards. Every morphism must respect deletion: you can always throw away output. This is the **semicartesian** condition.

The key axiom is what copy does *not* satisfy. In a cartesian category (like Set), copy is natural for all morphisms: copying then applying f equals applying f then copying. In a Markov category, this naturality holds only for **deterministic** morphisms:

> copy<sub>Y</sub> ∘ f = (f ⊗ f) ∘ copy<sub>X</sub>

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-copy-equation.svg" alt="String diagrams: deterministic morphism commutes with copy (same output both ways). Stochastic morphism does not (each copy samples fresh, different outputs)." style="width:100%; display:block;">
</div>

Stochastic morphisms violate this equation. Each copy gets a fresh sample. The gap between the full category C and its deterministic subcategory C<sub>det</sub> is where probability lives.

[The Natural Framework](/the-natural-framework) proves stochasticity is physically mandatory ([Landauer → heat → variation → stochasticity](/the-natural-framework#stochasticity)). Fritz gives that chain a one-equation formulation: the copy-naturality equation is the equation the pipeline must violate.

## Filter stays, Attend crosses

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-det-boundary.svg" alt="The full Markov category C contains a cartesian subcategory C_det. Filter lives inside C_det (copy equation holds). Attend lives outside (copy equation fails). A dashed arrow shows Attend crossing the boundary." style="width:100%; display:block;">
</div>

The deterministic morphisms form a cartesian subcategory C<sub>det</sub> ⊂ C, closed under composition ([§10](https://arxiv.org/abs/1908.07021)). This subcategory boundary is where the Filter/Attend separation lives.

**Filter is deterministic.** Its contract is *gated*: the indexed set minus items that failed a threshold. A threshold is a deterministic decision. Same input, same gate. Filter commutes with copy. It lives in C<sub>det</sub>.

**Attend must leave C<sub>det</sub>.** Its contract is *ranked*: ordered, diverse, bounded. [The Natural Framework](/the-natural-framework) proves a deterministic selector over a finite state space eventually cycles, killing diversity. Any morphism that maintains diversity under iteration must fail the copy equation — it lives in C \ C<sub>det</sub>.

[The Handshake](/the-handshake) argues Filter and Attend cannot merge because one function cannot satisfy reliable gating *and* diversity enforcement across unbounded iterations. Fritz makes this a subcategory statement. C<sub>det</sub> is closed under composition: two deterministic morphisms compose to a deterministic morphism. To get stochastic output from deterministic input, you need a morphism that crosses the boundary. Attend is that crossing.

This also sharpens the near-miss test. Top-k is deterministic (lives in C<sub>det</sub>) but converges to a fixed point: same winners every cycle. A [DPP](https://arxiv.org/abs/1207.6083) kernel samples from the full category. The subcategory tells you where to look: deterministic morphisms are safe but limited; stochastic morphisms that pass the iteration-stability test are the ones that maintain diversity.

### Worked example: Filter as a morphism in FinStoch

In **FinStoch** (Fritz's paradigmatic example), objects are finite sets, morphisms are stochastic matrices where columns sum to 1, and deterministic morphisms are 0-1 matrices (ordinary functions).

Let X = {a, b, c, d} be indexed items and Y = {a, c} the gated survivors. Filter is the morphism f : X → Y ∪ {⊥} defined by:

> f(a) = a, f(b) = ⊥, f(c) = c, f(d) = ⊥

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-filter-example.svg" alt="Four indexed items enter Filter. Items a and c pass (blue), items b and d are rejected (grey, mapped to ⊥). The 0-1 matrix commutes with copy." style="width:100%; display:block;">
</div>

This is a 0-1 matrix. It commutes with copy: copy(f(x)) = (f(x), f(x)) = (f ⊗ f)(copy(x)) for all x. Deterministic. Lives in C<sub>det</sub>.

Now replace Filter with a stochastic gate. Each item passes with probability p(x). The morphism becomes a genuine stochastic matrix. It no longer commutes with copy: copying x and then gating each copy independently gives two *different* outcomes with positive probability, while gating and then copying gives two *identical* outcomes. The equation fails. The gate is no longer in C<sub>det</sub>.

If the gate crosses out of C<sub>det</sub>, false positives compound: a bad item that passes by luck is never re-filtered, and luck compounds per cycle. This is the minimal example of a contract — *gated* — expressed entirely inside Fritz's formalism, without a third layer. The subcategory boundary does the work.

## Information loss is a functor

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-info-loss.svg" alt="Pipeline with bit-bars shrinking at each lossy stage. Perceive injects bits, Filter and Attend erase bits, the DPI guarantees total loss only accumulates." style="width:100%; display:block;">
</div>

[Baez, Fritz, and Leinster](https://arxiv.org/abs/1106.1791) proved the information budget has a unique form. Their Theorem 2: any map F sending morphisms in **FinProb** to nonneg reals that satisfies

1. **Functoriality**: F(f ∘ g) = F(f) + F(g)
2. **Convex linearity**: F(λf ⊕ (1−λ)g) = λF(f) + (1−λ)F(g)
3. **Continuity**: F(f) is continuous in f

must equal c(H(p) − H(q)) — Shannon entropy loss, up to scale. The data processing inequality follows: nonneg additive loss can only accumulate under composition.

The theorem applies to **FinProb** — finite probability spaces with deterministic measure-preserving maps. The pipeline's morphisms are Markov kernels, not deterministic maps. But Fritz's informativeness preorder ([Definition 16.1](https://arxiv.org/abs/1908.07021)) does transfer to any Markov category: t ≤ s iff there exists a morphism c such that t = c ∘ s (almost surely). A sufficient statistic retains all parameter-relevant information. Consolidate's contract — many episodes in, one parameter update out — is compression to a sufficient statistic. The DPI guarantees post-processing cannot recover more than Consolidate retained.

Two contracts already have a home in Fritz's tools: determinism (Filter ∈ C<sub>det</sub>) and sufficiency (Consolidate in the informativeness preorder). Whether the others require new structure or fall out as optimality conditions is the question the next section answers.

## Syntax and semantics

[Type Forcing](/type-forcing) fixed the wiring with Spivak. This post fills the wires with Fritz. A Markov category is a symmetric monoidal category, so it provides an algebra of Spivak's operad ([§2.1](https://arxiv.org/abs/1305.0297)): copy plays wire-splitting, delete plays wire-termination.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:14em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Spivak (operad)</th><th style="background:#f0f0f0">Fritz (Markov category)</th></tr></thead>
<tr><td>Handles</td><td>Which boxes connect to which</td><td>What flows through the connections</td></tr>
<tr><td>Constrains</td><td>Topology (wiring diagram)</td><td>Semantics (probability, information loss)</td></tr>
<tr><td>Key structure</td><td>Typed ports, supplier assignment</td><td>Copy/delete, deterministic subcategory</td></tr>
<tr><td>Stochasticity</td><td>Not expressible</td><td>Non-naturality of copy</td></tr>
<tr><td>DPI</td><td>Not expressible</td><td>Functorial information loss</td></tr>
<tr><td>Feedback</td><td>Delay nodes (cross-cycle)</td><td>Transition kernel (HMM structure)</td></tr>
<tr><td>Contracts</td><td>Port types (boundary labels)</td><td><strong>Partially derived</strong> (see below)</td></tr>
</table>

## Contracts as optimality conditions

Shannon didn't axiomatize communication — he observed what telegraph systems actually do, then proved the optimum. [Rate-distortion theory](https://en.wikipedia.org/wiki/Rate%E2%80%93distortion_theory) is a variational principle: minimize mutual information subject to a distortion constraint. The optimal code falls out as the extremum. The principle of least action does the same for physics: Lagrange defines a global functional, the Euler-Lagrange equations give local step-by-step constraints. Global objective in, local behavior out.

The same pattern applies here. Spivak gives boundary types (the constraints). Fritz gives information loss (the objective). Some contracts fall out as optimality conditions — not a third layer, but consequences of the first two.

### Derived: Consolidate

Among kernels that update policy from ranked input, the one minimizing output information over a feasible set must be lossy. The key hypothesis: the incumbent policy is always an admissible candidate (`self_feasible`). Any optimal output therefore costs no more than the incumbent — `info p' ≤ info p`. The [Lean 4 proof](https://github.com/kimjune01/natural-framework) derives it in three lines from a `MinimizesOn` predicate and that one witness.

### Derived: Filter

Among kernels that select from indexed items, the one minimizing output size over a feasible set that contains a strictly smaller element must be strictly reducing. Minimality gives `sizeOf b ≤ sizeOf c` for any feasible `c`; the strict witness gives `sizeOf c < sizeOf a`. Chain: `sizeOf b < sizeOf a`. The contract falls out of cardinality minimization plus the existence of a nontrivial reduction.

### Open: Attend (diversity)

Attend's boundedness follows from capacity — any realizable kernel keeps `measure b ≤ bound`. But diversity (distinct, non-repeating outputs) does not fall out of an information-theoretic objective at the possibilistic level. Nothing in the current objective distinguishes a duplicate from a novel item, so diversity cannot be derived from that objective alone. A genuine variational derivation would need a packing argument: replacing a bounded duplicate with a novel element increases support cardinality. That requires finite-set combinatorics not present in the current formalization.

### Open: the rest

Four contracts have no variational derivation: *encoded* (Perceive), *indexed* (Cache), *persisted* (Remember), and *ordered* (the ordering component of Attend). These may be genuinely extra structure — axioms about format and storage that don't reduce to information minimization. Whether they eventually yield to a richer objective or remain independent is the remaining open problem.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:10em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Contract</th><th style="background:#f0f0f0">Status</th><th style="background:#f0f0f0">Mechanism</th></tr></thead>
<tr><td>Gated (Filter)</td><td>Derived</td><td>Cardinality minimization + strict witness</td></tr>
<tr><td>Lossy (Consolidate)</td><td>Derived</td><td>Info minimization + self-feasible incumbent</td></tr>
<tr><td>Bounded (Attend)</td><td>Derived</td><td>Capacity constraint (trivial)</td></tr>
<tr><td>Diverse (Attend)</td><td>Open</td><td>Needs finite-set packing argument</td></tr>
<tr><td>Deterministic (Filter)</td><td>Fritz</td><td>Subcategory C<sub>det</sub></td></tr>
<tr><td>Sufficient (Consolidate)</td><td>Fritz</td><td>Informativeness preorder</td></tr>
<tr style="color:#888"><td>Encoded, Indexed, Persisted, Ordered</td><td>Open</td><td>May be extra structure</td></tr>
</table>

Implementation is the free variable. The universe doesn't care how you gate, only that you gate. A WHERE clause and clonal selection are interchangeable at the contract level. Twenty-four domains, six contracts, one survival condition. The ambient category tells you what probability *is*. The variational principle tells you what each stage *must do* — for some stages. For the rest, the question is open.

---

*Written via the [double loop](/double-loop).*
