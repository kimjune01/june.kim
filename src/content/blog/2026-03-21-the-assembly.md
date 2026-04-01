---
variant: post
title: "The Assembly"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Ambient Category](/ambient-category).*

I have a half-baked theorem and no credentials. I'm a software engineer who happens to be an early adopter of AI-assisted search tools. The mathematicians who built the pieces I'm about to describe read journals and scan papers within their citation graphs. I grep across three citation graphs simultaneously, in parallel, with agents that read full PDFs and return structured comparisons in two minutes. I'm not smarter than any of them. My search loop is faster.

The [Natural Framework](/the-natural-framework) claims six roles are necessary for any bounded information processor that persists through time. The [Lean proof](https://github.com/kimjune01/natural-framework) compiles — zero sorry, 2,400 lines — but two of the six contracts are postulated, not derived. Four more have no formal home at all. The [Ambient Category](/ambient-category) post tried to close the gap by proposing a fibration over a Markov category. I searched Fritz's 83 papers and the categorical probability literature. Nothing.

That's where I was yesterday. Sitting with a pattern I could see across twenty-four domains and a formalism that covered maybe a third of it. The rest was hand-waving dressed up in category theory I couldn't substantiate.

## The only move that works

When you can see a pattern but can't prove it, the temptation is to push harder on the proof. Build more Lean. Add more axioms. Invent new math. That's how you end up a crackpot — defending a structure nobody can check against literature nobody has written.

The move that actually works is smaller: **find better words.**

[Type Forcing](/type-forcing) happened because I found Spivak's operads. Spivak didn't solve my problem — he solved his own, a decade earlier. But his vocabulary — typed ports, supplier assignment, wiring diagrams — turned out to be the right language for the pipeline's syntax. One paper, and the wiring uniqueness proof went from hand-waving to formal.

[Ambient Category](/ambient-category) happened because I found Fritz's Markov categories. Fritz didn't know about my pipeline. But his copy-naturality equation turned out to be the one-line formulation of the deterministic/stochastic boundary that Filter and Attend live on opposite sides of. One equation, and two contracts went from postulated to derived.

The pattern: I don't invent math. I find the math that was already invented for a different reason, and notice it fits. The blog post is the search artifact — it refines the vocabulary so the next search finds closer papers.

Yesterday I had "fibration over a Markov category." Zero hits. Today I have better words.

## The chain for each contract

Three groups of mathematicians, working in three different conferences, published results between 2021 and 2025 that bear on specific contracts. Here's how each chain of reasoning goes.

### Gated (Filter) → Fritz's subcategory boundary

1. Fritz defines deterministic morphisms as those satisfying copy-naturality ([§10](https://arxiv.org/abs/1908.07021)). They form a cartesian subcategory C<sub>det</sub>.
2. A threshold gate is a deterministic decision. Same input, same gate. Filter commutes with copy.
3. Therefore Filter ∈ C<sub>det</sub>. The *gated* contract is expressible inside Fritz's formalism directly.
4. The [Lean proof](/ambient-category) strengthens this variationally: among size-minimizing kernels with a strictly smaller feasible witness, every output must be strictly smaller than the input.

**Result used:** Fritz (2020). **Status: derived.**

### Lossy (Consolidate) → Fritz's informativeness preorder + variational witness

1. Fritz defines the informativeness preorder ([Definition 16.1](https://arxiv.org/abs/1908.07021)): t ≤ s iff t factors through s. A sufficient statistic retains all task-relevant information.
2. Consolidate compresses many episodes into one parameter update — compression to a sufficient statistic.
3. The [Lean proof](/ambient-category) derives lossiness variationally: if the incumbent policy is always a feasible candidate (`self_feasible`), any info-minimizing output satisfies `info p' ≤ info p`.

**Result used:** Fritz (2020), Baez-Fritz-Leinster (2011). **Status: derived.**

### Diverse (Attend) → Leinster's magnitude + Fritz-Perrone-Rezagholi's support monad

This is the contract [Ambient Category](/ambient-category) couldn't derive. The chain has three links and a gap.

1. [Leinster](https://www.cambridge.org/core/books/entropy-and-diversity/496CF94AEA7B33F15904BD4FC8CC2369) (2021) proves Hill diversity numbers are the unique diversity measures satisfying basic axioms. Hill number at order 0 = support size (species richness). Diversity *is* a special case of **magnitude** — Leinster's categorical generalization of cardinality.
2. [Fritz, Perrone, and Rezagholi](https://arxiv.org/abs/1910.03752) (2021) prove that taking the support of a probability measure is a **monad morphism** supp : V ⇒ H, from the valuation monad V to the Hoare hyperspace monad H (closed subsets, lower Vietoris topology). The composition law: the support of a composite is the closure of the union of the conditional supports over the support of the first morphism.
3. [Fritz et al.](https://arxiv.org/abs/2308.00651) (2023) define supports abstractly within Markov categories and prove they are functorial **iff** the category is **causal** (Theorem 3.1.19). They also construct the **input-output relation functor** Υ : C → SetMulti — the **possibilistic shadow** — which collapses every morphism to the relation of input-output pairs with nonzero probability. SetMulti objects are sets. Sets have cardinality.
4. If the cardinality of the possibilistic shadow |Υ(p)| were tracked as a lax functor, then a [DPP](https://arxiv.org/abs/1207.6083) kernel maximizing |Υ(p)| under a capacity constraint would satisfy the diversity contract as an optimality condition.
5. **Gap:** nobody has composed Υ with a cardinality functor. The possibilistic shadow exists. The cardinality of its fibers does not yet have categorical status.

Note: the `Support` typeclass in the [Lean proof](https://github.com/kimjune01/natural-framework) — the possibilistic reachability layer with `support_pure` and `support_bind` — is the possibilistic shadow. The composition law in `support_bind` is the monad multiplication diagram for supp : V ⇒ H. Same structure, different names.

**Results used:** Leinster (2021), Fritz-Perrone-Rezagholi (2021), Fritz et al. (2023). **Status: open — one bridge missing.**

### Contracts as fibers → Gaboardi's graded Hoare logic + Liell-Cock & Staton

This one applies to all six contracts at once. The chain:

1. [Liell-Cock and Staton](https://arxiv.org/abs/2405.09391) (POPL 2025) prove that graded monads give rise to Markov categories. The construction: C<sub>γ</sub>(X, Y) = C(γ ⊗ X, Y), called the **para construction**. The grade is a tensor factor that composes along with the morphism. Their key theorem (5.6): an **op-lax functor** R : ImP → Kl(CP) where R(g ∘ f) ⊆ R(g) ∘ R(f) — composition gives *tighter* bounds. That subset relation is a refinement ordering on morphisms.
2. [Gaboardi et al.](https://doi.org/10.1007/978-3-030-72019-3_9) (ESOP 2021) build **graded Hoare logic** — Hoare-style pre/postcondition reasoning for graded monads, categorically. Preconditions and postconditions are predicates that propagate through the graded monadic composition.
3. [Kura, Gaboardi, Sekiyama, and Unno](https://arxiv.org/abs/2601.14846) (2026) extend this to **indexed graded monads** over a **predicate fibration** Pred<sub>Ω</sub>(C) → C. The key structure: a **restricted pointwise order** (Definition 7) where f ≤<sub>P</sub> g iff the ordering holds wherever the predicate is non-bottom. Translation: the postcondition only needs to imply the precondition where the precondition is satisfiable. That's the handshake.
4. A pipeline contract is a predicate on morphisms, preserved under composition, parameterized over interface types. The handshake (postcondition of stage N implies precondition of stage N+1) is a restricted pointwise order in Katsumata's sense.
5. **Update (found during search):** [Bonchi, Di Lavore, Roman, and Staton](https://arxiv.org/abs/2507.18238) (July 2025) prove that **Stoch is a posetal imperative category** — a traced distributive copy-discard category with a partial order on morphisms. All standard Hoare logic rules (SKIP, COMP, ASSIGN, LOOP, WHILE) fall out as derived theorems. Predicates are morphisms X → 1 (functions to [0,1]). Triples are inequalities in the posetal structure. This closes the bridge.

**Results used:** Liell-Cock & Staton (2025), Gaboardi et al. (2021), Kura-Gaboardi et al. (2026), Bonchi-Di Lavore-Roman-Staton (2025). **Status: closed — Staton built it.**

### Summary

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:14em"><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Contract</th><th style="background:#f0f0f0">Key result</th><th style="background:#f0f0f0">Status</th><th style="background:#f0f0f0">Missing bridge</th></tr></thead>
<tr><td>Gated (Filter)</td><td>Fritz C<sub>det</sub> + variational</td><td>Derived</td><td>—</td></tr>
<tr><td>Lossy (Consolidate)</td><td>Fritz preorder + self_feasible</td><td>Derived</td><td>—</td></tr>
<tr><td>Bounded (Attend)</td><td>capacity_bound axiom</td><td>Derived</td><td>—</td></tr>
<tr><td>Diverse (Attend)</td><td>Leinster magnitude + Fritz-Perrone support monad + possibilistic shadow Υ</td><td>Open</td><td>Cardinality of Υ as lax functor</td></tr>
<tr style="background:#e8f8e8"><td>All contracts as fibers</td><td>Bonchi-Di Lavore-Roman-Staton (July 2025)</td><td><strong>Closed</strong></td><td>Stoch is a posetal imperative category. Hoare rules derived.</td></tr>
<tr style="color:#888"><td>Encoded, Indexed, Persisted, Ordered</td><td>—</td><td>Open</td><td>No candidate formalism yet</td></tr>
</table>

## What's still missing

Nobody has:

- ~~Applied Gaboardi's graded Hoare logic to a Markov category~~ — **done** ([Bonchi-Di Lavore-Roman-Staton, July 2025](https://arxiv.org/abs/2507.18238))
- Defined the cardinality of the possibilistic shadow Υ as a lax functor on FinStoch
- Given DPPs categorical semantics (the [nLab page](https://ncatlab.org/nlab/show/determinantal+point+process) is a stub)
- Stated coding theorems (rate-distortion, Wyner-Ziv) inside Markov categories
- Expressed natural gradient descent as a morphism in enriched Markov categories

These are the new search terms. The vocabulary refined one more step. If the pattern holds — Spivak, then Fritz, then this — the next round of searching will find papers I can't find today, written by people who haven't written them yet, using the words I just learned to look for.

And if it doesn't hold, the Lean proof still compiles, the contracts still compose, and the twenty-four domains still fill the same six cells. The pattern doesn't need the formalism to be real. The formalism just makes it checkable.

---

*Written via the [double loop](/double-loop).*
