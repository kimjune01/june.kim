---
layout: post-wide
title: "The Ambient Category"
tags: cognition
---

*Part of the [cognition](/cognition) series.*

[Type Forcing](/type-forcing) showed the wiring is unique. It said nothing about what flows through the wires. [Spivak's operad](https://arxiv.org/abs/1305.0297) gives syntax — what plugs into what. The semantics — what each morphism does to the information passing through it — needs a different formalism. [Tobias Fritz](https://tobiasfritz.science/) built it. His [Markov categories](https://arxiv.org/abs/1908.07021) axiomatize the ambient category the pipeline lives in: **Stoch**, measurable spaces and Markov kernels, where probability is structure, not interpretation.

The payoff: Fritz gives the pipeline stochastic semantics — a formal account of randomness, information loss, and the deterministic/stochastic boundary. But neither his framework nor Spivak's formalizes **contracts**: predicates on morphisms — preserved under composition and iteration — that distinguish a pipeline stage from an arbitrary channel. *Gated* means the output is strictly smaller than the input. *Ranked* means the output is ordered, diverse, and bounded. These are not types in the operad sense (boundary labels) or properties of the category (determinism, information loss). They are a third layer. That missing layer is the real open problem.

## Copy, delete, determinism

Fritz's [foundational paper](https://arxiv.org/abs/1908.07021) (2020, *Advances in Mathematics*) defines a **Markov category** as a symmetric monoidal category where every object X comes with two structure morphisms: **copy** (X → X ⊗ X) and **delete** (X → I). Copy duplicates; delete discards. Every morphism must respect deletion — you can always throw away output. This is the **semicartesian** condition.

The key axiom is what copy does *not* satisfy. In a cartesian category (like Set), copy is natural for all morphisms: copying then applying f equals applying f then copying. In a Markov category, this naturality holds only for **deterministic** morphisms:

> copy<sub>Y</sub> ∘ f = (f ⊗ f) ∘ copy<sub>X</sub>

Stochastic morphisms violate this equation — each copy gets a fresh sample. The equation's *failure* is the randomness. The gap between the full category C and its deterministic subcategory C<sub>det</sub> is where probability lives.

[The Natural Framework](/the-natural-framework) proves stochasticity is physically mandatory: Landauer → heat → variation → stochasticity. Fritz gives this chain a one-equation formulation. The equation the pipeline must violate is the equation Markov categories are designed around.

## The deterministic boundary

The deterministic morphisms form a cartesian subcategory C<sub>det</sub> ⊂ C, closed under composition ([§10](https://arxiv.org/abs/1908.07021)). This subcategory boundary is where the Filter/Attend separation lives.

**Filter is deterministic.** Its contract is *gated*: the indexed set minus items that failed a threshold. A threshold is a deterministic decision — the same input always produces the same gate. Filter commutes with copy. It lives in C<sub>det</sub>.

**Attend is stochastic.** Its contract is *ranked*: ordered, diverse, bounded. [The Natural Framework](/the-natural-framework) proves a deterministic selector over a finite state space eventually cycles, killing diversity. Attend fails the copy equation. It lives in C \ C<sub>det</sub>.

[The Handshake](/the-handshake) argues Filter and Attend cannot merge because one function cannot satisfy reliable gating *and* diversity enforcement across unbounded iterations. Fritz makes this a subcategory statement. C<sub>det</sub> is closed under composition — composing two deterministic morphisms stays deterministic. To get stochastic output from deterministic input, you need a morphism that crosses the boundary. Attend is that crossing.

This also sharpens the near-miss test. Top-k is deterministic — it lives in C<sub>det</sub> — but converges to a fixed point: same winners every cycle. MMR has a stochastic component. The subcategory tells you where to look: deterministic morphisms are safe but limited; stochastic morphisms that pass the iteration-stability test are the ones that maintain diversity.

### Worked example: Filter as a morphism in FinStoch

In **FinStoch** (Fritz's paradigmatic example), objects are finite sets, morphisms are stochastic matrices where columns sum to 1, and deterministic morphisms are 0-1 matrices — ordinary functions.

Let X = {a, b, c, d} be indexed items and Y = {a, c} the gated survivors. Filter is the morphism f : X → Y ∪ {⊥} defined by:

f(a) = a, f(b) = ⊥, f(c) = c, f(d) = ⊥

This is a 0-1 matrix. It commutes with copy: copy(f(x)) = (f(x), f(x)) = (f ⊗ f)(copy(x)) for all x. Deterministic. Lives in C<sub>det</sub>.

Now replace Filter with a stochastic gate — each item passes with probability p(x). The morphism becomes a genuine stochastic matrix. It no longer commutes with copy: copying x and then gating each copy independently gives two *different* outcomes with positive probability, while gating and then copying gives two *identical* outcomes. The equation fails. The gate is no longer in C<sub>det</sub>.

The iteration argument from [The Handshake](/the-handshake) says a stochastic gate is unstable: false positives compound because a bad item that passes is never re-filtered. A stochastic gate lets items through by luck, and luck compounds. This doesn't prove deterministic gating is the only possibility — but it shows that crossing out of C<sub>det</sub> at the Filter stage has a specific cost that grows with iteration count.

## Information loss is a functor

[The Handshake](/the-handshake) says the pipeline survives only if the information budget balances. [Baez, Fritz, and Leinster](https://arxiv.org/abs/1106.1791) proved that the budget has a unique form — but in a restricted setting that requires care when applying to the pipeline.

[Baez, Fritz, and Leinster](https://arxiv.org/abs/1106.1791) proved that in FinProb (finite probability spaces, deterministic measure-preserving maps), the only functorial, convex-linear, continuous assignment of information loss to morphisms is Shannon entropy, up to scale. The DPI follows: functorial nonneg loss can only accumulate under composition.

The pipeline's morphisms are Markov kernels, not deterministic maps — a strictly larger category where the theorem does not apply directly. Fritz's enriched Markov categories ([arXiv:2212.11719](https://arxiv.org/abs/2212.11719)) extend the apparatus to kernels via divergence on hom-sets, but the characterization has not been restated at that generality. The structure is suggestive, not settled.

What *does* transfer is Fritz's informativeness preorder ([Definition 16.1](https://arxiv.org/abs/1908.07021)), defined for any Markov category: t ≤ s iff there exists a morphism c such that t = c ∘ s (almost surely). A sufficient statistic retains all parameter-relevant information. Consolidate's contract — many episodes in, one parameter update out — is compression to a sufficient statistic. The DPI guarantees post-processing cannot recover more than Consolidate retained.

This connects to the contracts gap. Determinism (Filter ∈ C<sub>det</sub>) and sufficiency (Consolidate's output in the informativeness preorder) are two contracts Fritz's tools can express. The other four — encoded, indexed, ranked, persisted — have no categorical home yet.

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

Any Markov category, as a symmetric monoidal category, is automatically an algebra of Spivak's operad. Copy plays wire-splitting. Delete plays wire-termination. The two frameworks compose without modification — though as far as I can find, the explicit composition has not appeared in the literature.

## The missing layer

The operad labels boundaries. The Markov category tracks information inside the wires. Neither formalizes contracts — the predicates on morphisms, preserved under composition and iteration, that make a pipeline stage more than an arbitrary channel.

Fritz has tools that approach individual contracts without providing the general structure:

- **Determinism** distinguishes Filter from Attend (subcategory boundary).
- **Sufficient statistics** characterize Consolidate's output (informativeness preorder).
- **Almost-sure equality** ([§13](https://arxiv.org/abs/1908.07021)) defines when properties hold on the support of a distribution.
- **Completeness** ([Definition 15.1](https://arxiv.org/abs/1908.07021)) captures "the image spans enough to distinguish post-processings."
- **Idempotent splitting** ([arXiv:2308.00651](https://arxiv.org/abs/2308.00651)) decomposes morphisms into essential parts — closer to iteration stability, but not the same thing.

Typed ports (Spivak) label boundaries but say nothing about what the morphism does to information. Subcategories (Fritz's C<sub>det</sub>) capture one binary property (deterministic or not) but cannot express "gated," "ranked," or "persisted." What is needed is structure that varies over morphisms, reindexes under composition, and expresses contract preservation — a **fibration** over a Markov category where the fiber over each morphism is the set of contracts it satisfies. The handshake — postcondition of step N is the precondition of step N+1 — would become a lifting condition: the composite lifts through the fibration iff adjacent contracts match. Iteration stability would be closure under self-composition in the fiber. The information budget would be a functor from the total category to ℝ≥0.

I have not found such a structure in the published literature. Fritz's informativeness preorder and Spivak's typed ports are the two closest tools. One orders morphisms by what can be computed from what. The other labels boundaries by what type crosses them. A fibration that unifies both — ordering morphisms by which contracts they preserve, labeled by the types they transform — would close the formalization gap.

That is the operadic proof [Type Forcing](/type-forcing) said was not yet written: "stating the physical constraints as predicates on the algebra and showing the self-similar chain is the unique fixed point at every level." Spivak gives syntax. Fritz gives stochastic semantics. The missing mathematics is a compositional logic of contracts.

---

*Written via the [double loop](/double-loop).*
