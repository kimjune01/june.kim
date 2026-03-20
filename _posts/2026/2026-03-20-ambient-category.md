---
layout: post-wide
title: "Ambient Category"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Type Forcing](/type-forcing).*

[Type Forcing](/type-forcing) showed the wiring is unique. It said nothing about what flows through the wires. [Spivak's operad](https://arxiv.org/abs/1305.0297) gives syntax: what plugs into what. The semantics, what each morphism does to information passing through it, needs a different formalism. [Tobias Fritz](https://tobiasfritz.science/) built it. His [Markov categories](https://arxiv.org/abs/1908.07021) axiomatize the ambient category the pipeline lives in: **Stoch**, measurable spaces and Markov kernels, where probability is structure.

Fritz gives the pipeline stochastic semantics: a formal account of randomness, information loss, and the deterministic/stochastic boundary. But neither his framework nor Spivak's formalizes **contracts**: predicates on morphisms, preserved under composition and iteration, that distinguish a pipeline stage from an arbitrary channel. *Gated* means the output is strictly smaller than the input. *Ranked* means the output is ordered, diverse, and bounded. Contracts are a third layer, beyond boundary types (Spivak) and morphism properties (Fritz). That missing layer is the real open problem.

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-three-layers.svg" alt="Three layers: Spivak (syntax, boundary types), Fritz (structure, morphism properties), Contracts (function, behavioral predicates — open problem). A brace on the right labels their convergence: reality." style="width:100%; display:block;">
</div>

## The equation that fails

Fritz's [foundational paper](https://arxiv.org/abs/1908.07021) (2020, *Advances in Mathematics*) defines a **Markov category** as a symmetric monoidal category where every object X comes with two structure morphisms: **copy** (X → X ⊗ X) and **delete** (X → I). Copy duplicates; delete discards. Every morphism must respect deletion: you can always throw away output. This is the **semicartesian** condition.

The key axiom is what copy does *not* satisfy. In a cartesian category (like Set), copy is natural for all morphisms: copying then applying f equals applying f then copying. In a Markov category, this naturality holds only for **deterministic** morphisms:

> copy<sub>Y</sub> ∘ f = (f ⊗ f) ∘ copy<sub>X</sub>

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-copy-equation.svg" alt="String diagrams: deterministic morphism commutes with copy (same output both ways). Stochastic morphism does not (each copy samples fresh, different outputs)." style="width:100%; display:block;">
</div>

Stochastic morphisms violate this equation. Each copy gets a fresh sample. The gap between the full category C and its deterministic subcategory C<sub>det</sub> is where probability lives.

[The Natural Framework](/the-natural-framework) proves stochasticity is physically mandatory: Landauer → heat → variation → stochasticity. Fritz gives this chain a one-equation formulation. The equation the pipeline must violate is the equation Markov categories were built around.

## Filter stays, Attend crosses

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-det-boundary.svg" alt="The full Markov category C contains a cartesian subcategory C_det. Filter lives inside C_det (copy equation holds). Attend lives outside (copy equation fails). A dashed arrow shows Attend crossing the boundary." style="width:100%; display:block;">
</div>

The deterministic morphisms form a cartesian subcategory C<sub>det</sub> ⊂ C, closed under composition ([§10](https://arxiv.org/abs/1908.07021)). This subcategory boundary is where the Filter/Attend separation lives.

**Filter is deterministic.** Its contract is *gated*: the indexed set minus items that failed a threshold. A threshold is a deterministic decision. Same input, same gate. Filter commutes with copy. It lives in C<sub>det</sub>.

**Attend is stochastic.** Its contract is *ranked*: ordered, diverse, bounded. [The Natural Framework](/the-natural-framework) proves a deterministic selector over a finite state space eventually cycles, killing diversity. Attend fails the copy equation. It lives in C \ C<sub>det</sub>.

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

If the gate crosses out of C<sub>det</sub>, false positives compound: a bad item that passes by luck is never re-filtered, and luck compounds per cycle.

## Information loss is a functor

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-info-loss.svg" alt="Pipeline with bit-bars shrinking at each lossy stage. Perceive injects bits, Filter and Attend erase bits, the DPI guarantees total loss only accumulates." style="width:100%; display:block;">
</div>

[Baez, Fritz, and Leinster](https://arxiv.org/abs/1106.1791) proved the information budget has a unique form.

In FinProb (finite probability spaces, deterministic measure-preserving maps), the only functorial, convex-linear, continuous assignment of information loss to morphisms is Shannon entropy, up to scale. The DPI follows: functorial nonneg loss can only accumulate under composition.

The pipeline's morphisms are Markov kernels, not deterministic maps. FinProb is a subcategory of Stoch; the theorem does not apply directly. Fritz's enriched Markov categories ([arXiv:2212.11719](https://arxiv.org/abs/2212.11719)) extend the apparatus to kernels via divergence on hom-sets, but the characterization has not been restated at that generality. Each formalism narrows the gap: Spivak's operads, Fritz's Markov categories, this entropy characterization. The structure is internally consistent and not yet falsified.

What *does* transfer is Fritz's informativeness preorder ([Definition 16.1](https://arxiv.org/abs/1908.07021)), defined for any Markov category: t ≤ s iff there exists a morphism c such that t = c ∘ s (almost surely). A sufficient statistic retains all parameter-relevant information. Consolidate's contract (many episodes in, one parameter update out) is compression to a sufficient statistic. The DPI guarantees post-processing cannot recover more than Consolidate retained.

This connects to the contracts gap. Determinism (Filter ∈ C<sub>det</sub>) and sufficiency (Consolidate's output in the informativeness preorder) are two contracts Fritz's tools can express. The other four (encoded, indexed, ranked, persisted) have no categorical home yet.

## Syntax and semantics

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:14em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Spivak (operad)</th><th style="background:#f0f0f0">Fritz (Markov category)</th></tr></thead>
<tr><td>Handles</td><td>Which boxes connect to which</td><td>What flows through the connections</td></tr>
<tr><td>Constrains</td><td>Topology (wiring diagram)</td><td>Semantics (probability, information loss)</td></tr>
<tr><td>Key structure</td><td>Typed ports, supplier assignment</td><td>Copy/delete, deterministic subcategory</td></tr>
<tr><td>Stochasticity</td><td>Not expressible</td><td>Non-naturality of copy</td></tr>
<tr><td>DPI</td><td>Not expressible</td><td>Functorial information loss</td></tr>
<tr><td>Feedback</td><td>Delay nodes (cross-cycle)</td><td>Transition kernel (HMM structure)</td></tr>
<tr><td>Contracts</td><td>Port types (boundary labels)</td><td><strong>Open problem</strong></td></tr>
</table>

A Markov category is a symmetric monoidal category, so it provides an algebra of Spivak's operad ([§2.1](https://arxiv.org/abs/1305.0297)): copy plays wire-splitting, delete plays wire-termination. [Type Forcing](/type-forcing) fixed the wiring with Spivak. This post fills the wires with Fritz.

## The missing layer

The operad labels boundaries. The Markov category tracks information inside the wires. Neither formalizes contracts: predicates on morphisms, preserved under composition and iteration, that make a pipeline stage more than an arbitrary channel.

Fritz has tools that approach individual contracts without providing the general structure:

- **Determinism** distinguishes Filter from Attend (subcategory boundary).
- **Sufficient statistics** characterize Consolidate's output (informativeness preorder).
- **Almost-sure equality** ([§13](https://arxiv.org/abs/1908.07021)) defines when properties hold on the support of a distribution.
- **Completeness** ([Definition 15.1](https://arxiv.org/abs/1908.07021)) captures "the image spans enough to distinguish post-processings."
- **Idempotent splitting** ([arXiv:2308.00651](https://arxiv.org/abs/2308.00651)) decomposes morphisms into essential parts. Closer to iteration stability, but not the same thing.

The [Lean 4 proof](https://github.com/kimjune01/natural-framework) confirms the gap empirically. The spec compiles against a lawful monad with contracts as predicates on morphisms. Attempts to import Markov category structure for the contracts failed at the dependency level.

The reason is [Coplien's duality](https://en.wikipedia.org/wiki/Data,_context_and_interaction): structure and function are complements. Fritz gives you structure: what morphisms *are* (deterministic, sufficient, complete). Contracts give you function: what morphisms *must do* (gate, rank, persist). Structure constrains which functions are possible. Function selects which structures survive. Neither reduces to the other. In Lean, the two live in different paradigms: types vs predicates. You can't derive a verb from a noun.

- A heart is tissue (structure) and circulation (function). You need both to pump blood.
- A building is a stack of bricks (structure) and a thing people seek shelter in (function).
- [Plato's Forms](https://en.wikipedia.org/wiki/Theory_of_forms) are structure. The just act is function. Fritz gives you the Forms. Contracts are the acts.

Twenty-four centuries and the tension is unresolved. It is the same wall.

Subcategories (Fritz's C<sub>det</sub>) capture one binary property (deterministic or not) but cannot express "gated," "ranked," or "persisted." What is needed is structure that varies over morphisms, reindexes under composition, and expresses contract preservation.

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/ambient-fibration.svg" alt="Fibration diagram: base category Stoch with morphisms Filter, Attend, Remember, Consolidate. Fibers above each carry their contracts (gated, ranked, persisted, policy). Lifting arrows show the handshake: postcondition of step N is precondition of step N+1." style="width:100%; display:block;">
</div>

A **fibration** over a Markov category where the fiber over each morphism is the set of contracts it satisfies. The handshake (postcondition of step N is the precondition of step N+1) would become a lifting condition: the composite lifts through the fibration iff adjacent contracts match. Iteration stability would be closure under self-composition in the fiber. The information budget would be a functor from the total category to ℝ≥0.

A search of Fritz's 83 arXiv papers, Spivak's operad program, and the categorical probability literature turned up no such structure. Fritz's informativeness preorder and Spivak's typed ports are the two closest tools. One orders morphisms by what can be computed from what. The other labels boundaries by what type crosses them. A fibration that unifies both, ordering morphisms by which contracts they preserve and labeled by the types they transform, would close the formalization gap.

That is the operadic proof [Type Forcing](/type-forcing) said was not yet written: "stating the physical constraints as predicates on the algebra and showing the self-similar chain is the unique fixed point at every level." Spivak gives syntax. Fritz gives structure. The missing mathematics is function: a compositional logic of what each morphism must do.

Implementation is the free variable. The universe doesn't care how you gate, only that you gate. A WHERE clause and clonal selection are interchangeable at the contract level. Twenty-four domains, six contracts, one survival condition. The ambient category tells you what probability *is*. Contracts tell you what probability *is for*.

Where the two converge, we call it reality.

---

*Written via the [double loop](/double-loop).*
