---
layout: post-wide
title: "Framework Lexicon"
tags: cognition
---

*Part of the [cognition](/cognition) series. Reference post — updated as vocabulary sharpens.*

Several mathematical communities have independently formalized overlapping structures under different names. This post maps the translations.

**If you're here because you found your name:** The [Rosetta stone](#rosetta-stone-same-objects-different-names) below maps your work to parallel results in other communities. The dashes mark where one community has no term for a concept the other has named.

**Authors cited:** [Fritz](#pipeline-structure), [Spivak](#pipeline-structure), [Gaboardi](#contracts-and-composition), [Katsumata](#contracts-and-composition), [Kura](#contracts-and-composition), [Jacobs](#contracts-and-composition), [Liell-Cock](#contracts-and-composition), [Staton](#contracts-and-composition), [Perrone](#information-theory), [Leinster](#information-theory), [Baez](#information-theory), [Sato](#rosetta-stone-same-objects-different-names), [Chen](#near-misses), [Vigneaux](#near-misses), [Rezagholi](#support-and-possibilism).

🍞 [Run these papers interactively](/natural-breadcrumbs/)

---

## Rosetta stone: same objects, different names

Corrections welcome — [june@june.kim](mailto:june@june.kim).

<table style="width:100%; font-size:13px; table-layout:fixed;">
<colgroup><col style="width:20%"><col style="width:20%"><col style="width:22%"><col style="width:12%"><col style="width:26%"></colgroup>
<thead><tr>
<th style="background:#e8f0fe">PL theory</th>
<th style="background:#fef3e8">Categorical probability</th>
<th style="background:#f0f0f0">Shared object</th>
<th style="background:#f0e8f0">Framework</th>
<th style="background:#f0f0f0">Confidence</th>
</tr></thead>
<tr style="background:#f8f8f8">
<td>Kleisli(D)<br><small><a href="https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/abs/weakest-preconditions-in-fibrations/657A41FD194D8CC5E4662B71F2E1454E">Jacobs 2014</a></small></td>
<td>FinStoch<br><small><a href="https://arxiv.org/abs/1908.07021">Fritz 2020</a></small></td>
<td>Category of finite sets + stochastic matrices</td>
<td>Ambient category<br><small><a href="/ambient-category">post</a></small></td>
<td><strong>Exact.</strong> Same category</td>
</tr>
<tr>
<td>Hoare triple {P} c {Q}<br><small><a href="https://doi.org/10.1007/978-3-030-72019-3_9">Gaboardi 2021</a></small></td>
<td>—</td>
<td>Predicate on morphism outputs, preserved under composition</td>
<td>Contract<br><small><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Graded.lean">Graded.lean</a></small></td>
<td><strong>Plausible.</strong> Grade algebra matches: <code>PreorderedMonoid</code> typeclass with additive composition, weakening, Nat instance (<a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Graded.lean">Graded.lean</a>). Gaboardi's categorical semantics (graded Freyd categories, coherent fibrations, soundness theorem) not formalized.</td>
</tr>
<tr style="background:#f8f8f8">
<td>Restricted pointwise order<br><small><a href="https://arxiv.org/abs/2601.14846">Kura-Gaboardi 2026 Def 7</a></small></td>
<td>—</td>
<td>Post(N) implies Pre(N+1), restricted to support</td>
<td>Handshake<br><small><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Comp.lean">Comp.lean</a></small></td>
<td><strong>Exact.</strong> <code>forward_triple</code> chains four COMP rules through real pre/postconditions. Each stage's postcondition is the next stage's precondition — the restricted pointwise order, machine-checked.</td>
</tr>
<tr>
<td>wp via poset fibration over Kleisli(D)<br><small><a href="https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/abs/weakest-preconditions-in-fibrations/657A41FD194D8CC5E4662B71F2E1454E">Jacobs 2014</a></small></td>
<td>Posetal imperative category<br><small><a href="https://arxiv.org/abs/2507.18238">Staton 2025 Cor. 76</a></small></td>
<td>Predicate logic over a stochastic category</td>
<td>"Fibration"<br><small><a href="/ambient-category">post</a></small></td>
<td><strong>Exact.</strong> Staton proves Hoare rules over Stoch (Thm 79)</td>
</tr>
<tr style="background:#f8f8f8">
<td>Graded Freyd category<br><small><a href="https://doi.org/10.1007/978-3-030-72019-3_9">Gaboardi 2021</a></small></td>
<td>Graded Markov category<br><small><a href="https://arxiv.org/abs/2405.09391">Liell-Cock & Staton 2025</a></small></td>
<td>Effectful computation with tracked side-effects</td>
<td>Stage + contract<br><small><a href="https://github.com/kimjune01/natural-framework">Lean</a></small></td>
<td><strong>Plausible.</strong> Freyd vs. Markov differ on exponentials</td>
</tr>
<tr>
<td>Divergence on monad<br><small><a href="https://arxiv.org/abs/2206.05716">Sato-Katsumata 2023</a></small></td>
<td>Enriched Markov category<br><small><a href="https://link.springer.com/chapter/10.1007/978-3-031-38271-0_27">Perrone 2023</a></small></td>
<td>Metric on morphism spaces for verification</td>
<td>NonExpanding<br><small><a href="https://github.com/kimjune01/natural-framework">Lean</a></small></td>
<td><strong>Plausible.</strong> <code>nonExpanding_iff_threshold_triple</code> characterizes NonExpanding as a family of unary threshold Hoare triples (<a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Divergence.lean">Divergence.lean</a>). Analogous in spirit to Sato-Katsumata, but their framework is relational (compares two morphisms via graded divergence), ours is unary. Not a formal instance of their construction.</td>
</tr>
<tr style="background:#f8f8f8">
<td>—</td>
<td>Possibilistic shadow Υ<br><small><a href="https://arxiv.org/abs/2308.00651">Fritz et al. 2023</a></small></td>
<td>Possibilistic collapse of a probabilistic morphism</td>
<td>Support typeclass<br><small><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Support.lean">Support.lean</a></small></td>
<td><strong>Exact.</strong> support_bind = monad multiplication</td>
</tr>
<tr>
<td>—</td>
<td>supp : V ⇒ H<br><small><a href="https://arxiv.org/abs/1910.03752">Fritz-Perrone-Rezagholi 2021</a></small></td>
<td>Monad morphism: valuations → closed subsets</td>
<td>support_bind<br><small><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Support.lean">Support.lean</a></small></td>
<td><strong>Exact.</strong> Same composition law</td>
</tr>
<tr style="background:#f8f8f8">
<td>—</td>
<td>Static idempotent<br><small><a href="https://arxiv.org/abs/2308.00651">Fritz et al. 2023 Prop 4.4.1</a></small></td>
<td>Idempotent that stabilizes after one step</td>
<td>IterationStable<br><small><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Contracts.lean">Contracts.lean</a></small></td>
<td><strong>Plausible.</strong> IterationStable = Hoare triple {'{'}c{'}'} f {'{'}c{'}'} (definitional). StaticOn (output = input) is strictly stronger. The splitting factorization of Fritz Prop 4.4.1 is not yet formalized — <code>stableSplit</code> in <a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Static.lean">Static.lean</a> is a placeholder. Gap is characterized but not closed.</td>
</tr>
<tr>
<td>—</td>
<td>Magnitude<br><small><a href="https://www.cambridge.org/core/books/entropy-and-diversity/496CF94AEA7B33F15904BD4FC8CC2369">Leinster 2021</a></small></td>
<td>Categorical cardinality / effective species count</td>
<td>Diversity<br><small><a href="/the-natural-framework">post</a></small></td>
<td><strong>Speculative.</strong> No composition law for magnitude</td>
</tr>
<tr style="background:#f8f8f8">
<td>Free ℕ-semimodule monad<br><small><a href="https://dl.acm.org/doi/10.1145/3473577">Kidney & Wu 2021</a></small></td>
<td>Double dualization<br><small><a href="https://arxiv.org/abs/1910.03752">Fritz-Perrone-Rezagholi 2021</a></small></td>
<td>Counting monad parameterized by semiring S</td>
<td><strong>Gap</strong><br><small>supp composed with |·|</small></td>
<td><strong>Speculative.</strong> Exists on Set, not via double dualization on Top</td>
</tr>
<tr>
<td>Selection relation on parametrised optics<br><small><a href="https://arxiv.org/abs/2105.06332">Capucci et al. 2021</a></small></td>
<td>—</td>
<td>"What is a goal but a predicate on a system?" Compositional predicate on morphisms.</td>
<td>Contract<br><small><a href="/the-handshake">post</a></small></td>
<td><strong>Plausible.</strong> Same role (behavioral predicate); different ambient structure (optics vs. Kleisli)</td>
</tr>
<tr style="background:#f8f8f8">
<td>Nash equilibrium as compositional predicate<br><small><a href="https://arxiv.org/abs/1603.04641">Ghani-Hedges et al. 2018</a></small></td>
<td>—</td>
<td>Equilibrium checked locally on subgames, preserved under game composition</td>
<td>Contract preserved under composition<br><small><a href="https://github.com/kimjune01/natural-framework">Lean</a></small></td>
<td><strong>Plausible.</strong> Structural parallel; games ≠ pipelines</td>
</tr>
<tr>
<td>Bayesian lens / statistical game<br><small><a href="https://arxiv.org/abs/2109.04461">Smithe 2021</a></small></td>
<td>Bayesian inversion in Markov category<br><small><a href="https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2023.24">Braithwaite-Hedges-Smithe 2023</a></small></td>
<td>Optic with forward (inference) and backward (learning) pass over stochastic morphisms</td>
<td>Forward pipeline + Consolidate<br><small><a href="/the-natural-framework">post</a></small></td>
<td><strong>Plausible.</strong> Both have forward+backward; optic composition ≠ Kleisli composition</td>
</tr>
<tr style="background:#f8f8f8">
<td>—</td>
<td>Dagger structure on kernels<br><small><a href="https://arxiv.org/abs/2001.08375">Parzygnat 2020</a></small></td>
<td>Bayesian inversion as categorical involution on morphisms</td>
<td>Consolidate (backward pass)<br><small><a href="/the-natural-framework">post</a></small></td>
<td><strong>Speculative.</strong> Consolidate updates policy; dagger inverts morphisms. Related but not the same operation</td>
</tr>
<tr>
<td>Effect algebra predicates (X → 1+1)<br><small><a href="https://arxiv.org/abs/1512.05813">Cho-Jacobs 2015</a></small></td>
<td>—</td>
<td>Predicates as effects, not subobjects. States/effects duality.</td>
<td>Contract<br><small><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Effects.lean">Effects.lean</a></small></td>
<td><strong>Plausible.</strong> Boolean contracts embed as {0,1}-valued effects (<a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Effects.lean">Effects.lean</a>), but the bridge is a Bool-to-Prop encoding, not a full effect algebra structure. The quantitative case (effects in [0,1]) is not formalized.</td>
</tr>
<tr style="background:#f8f8f8">
<td>Partial correctness<br><small>Standard PL</small></td>
<td>Partial Markov categories<br><small><a href="https://arxiv.org/abs/2502.03477">Di Lavore-Roman-Sobocinski 2025</a></small></td>
<td>Morphisms can fail. Observations, normalization, conditioning in restriction categories.</td>
<td>—<br><small>(pipeline assumes total morphisms)</small></td>
<td><strong>Plausible.</strong> Pipeline stages don't fail; but Filter's rejection maps to partiality</td>
</tr>
<tr>
<td>Program equivalence metrics<br><small><a href="https://www.worldscientific.com/worldscibooks/10.1142/p595">Panangaden 2009</a></small></td>
<td>—</td>
<td>Bisimulation metrics = behavioral distance between stochastic processes</td>
<td>—<br><small>(no framework analog)</small></td>
<td><strong>Speculative.</strong> Could connect to magnitude as behavioral distance. Nobody has tried.</td>
</tr>
</table>

---

## Pipeline structure

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Terminology</th><th style="background:#f0f0f0">Source</th><th style="background:#f0f0f0">Connection</th><th style="background:#f0f0f0">Framework term</th></tr></thead>
<tr><td>Operad algebra</td><td><a href="https://arxiv.org/abs/1305.0297">Spivak 2013</a></td><td>The six roles are boxes in a wiring diagram. Typed ports constrain which boxes connect.</td><td>Pipeline</td></tr>
<tr><td>Type forcing</td><td><a href="/type-forcing">Type Forcing post</a> + <a href="https://github.com/kimjune01/natural-framework">Lean proof</a></td><td>Given the six interface types, the supplier assignment is unique. Pipeline topology is forced.</td><td>Wiring uniqueness</td></tr>
<tr><td><strong>Stoch</strong> — Markov category</td><td><a href="https://arxiv.org/abs/1908.07021">Fritz 2020</a></td><td>The category the pipeline lives in. Measurable spaces + Markov kernels. Copy/delete structure.</td><td>Ambient category</td></tr>
<tr><td>Kleisli arrow α → M β</td><td>Standard</td><td>Each pipeline stage is a monadic kernel. When M = Id, it's a deterministic function.</td><td>Kernel</td></tr>
<tr><td>Kleisli composite of five kernels</td><td><a href="https://github.com/kimjune01/natural-framework">Lean proof</a> (Pipeline.lean)</td><td>Perceive → Cache → Filter → Attend → Remember. Five morphisms composed via >=>.</td><td>Forward pipeline</td></tr>
<tr><td>Traced monoidal category</td><td><a href="https://en.wikipedia.org/wiki/Traced_monoidal_category">Joyal-Street-Verity 1996</a></td><td>Remember's output feeds Perceive's input. The loop closes via a trace operator.</td><td>Feedback loop</td></tr>
<tr><td>Forward + Consolidate</td><td><a href="https://github.com/kimjune01/natural-framework">Lean proof</a> (Pipeline.lean)</td><td>One complete iteration: forward pass produces ranked output, Consolidate updates policy.</td><td>Cycle</td></tr>
</table>

## Deterministic / stochastic boundary

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Terminology</th><th style="background:#f0f0f0">Source</th><th style="background:#f0f0f0">Connection</th><th style="background:#f0f0f0">Framework term</th></tr></thead>
<tr><td>Copy-natural morphism</td><td><a href="https://arxiv.org/abs/1908.07021">Fritz 2020 §10</a></td><td>Filter is deterministic: same input, same gate. Commutes with copy. Lives in C<sub>det</sub>.</td><td>Deterministic morphism</td></tr>
<tr><td>Copy-non-natural morphism</td><td><a href="https://arxiv.org/abs/1908.07021">Fritz 2020</a></td><td>Attend must be stochastic: deterministic selectors cycle, killing diversity.</td><td>Stochastic morphism</td></tr>
<tr><td>Cartesian subcategory C<sub>det</sub></td><td><a href="https://arxiv.org/abs/1908.07021">Fritz 2020 §10</a></td><td>Filter lives inside. Attend crosses out. C<sub>det</sub> closed under composition — two det morphisms compose to det.</td><td>C<sub>det</sub> boundary</td></tr>
<tr><td>Pigeonhole → state collision</td><td><a href="https://github.com/kimjune01/natural-framework">Lean proof</a> (Stochasticity.lean, Pigeonhole.lean)</td><td>Deterministic transducer over Fin N must collide within N+1 steps. Confusion → error.</td><td>Stochasticity is mandatory</td></tr>
</table>

## Information theory

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Terminology</th><th style="background:#f0f0f0">Source</th><th style="background:#f0f0f0">Connection</th><th style="background:#f0f0f0">Framework term</th></tr></thead>
<tr><td>F(f) = c(H(p) − H(q))</td><td><a href="https://arxiv.org/abs/1106.1791">Baez-Fritz-Leinster 2011</a></td><td>The pipeline's information budget. Unique form under functoriality + convex-linearity + continuity. FinProb only.</td><td>Information loss</td></tr>
<tr><td>Functorial nonneg loss accumulates</td><td><a href="https://arxiv.org/abs/1106.1791">Baez-Fritz-Leinster 2011</a></td><td>Information only decreases through pipeline stages. Post-processing can't recover lost bits.</td><td>DPI</td></tr>
<tr><td>t ≤ s iff t = c ∘ s (a.s.)</td><td><a href="https://arxiv.org/abs/1908.07021">Fritz 2020 Def 16.1</a></td><td>Consolidate's output is a sufficient statistic. Retains task-relevant info, discards the rest.</td><td>Informativeness preorder</td></tr>
<tr><td>Distance from determinism</td><td><a href="https://arxiv.org/abs/2212.11719">Fritz-Gonda-Perrone-Rischel 2024</a></td><td>Measures how far a morphism is from being deterministic. Enriched Markov categories.</td><td>Categorical entropy</td></tr>
<tr><td>Divergences in enriched hom-spaces</td><td><a href="https://link.springer.com/chapter/10.1007/978-3-031-38271-0_27">Perrone 2023</a></td><td>Fisher metric lives in the enrichment. Potential home for Consolidate's update dynamics.</td><td>Info geometry</td></tr>
<tr><td>Magnitude / Hill number</td><td><a href="https://www.cambridge.org/core/books/entropy-and-diversity/496CF94AEA7B33F15904BD4FC8CC2369">Leinster 2021</a></td><td>Hill at q=0 = support size = species richness. Diversity IS categorical cardinality (magnitude).</td><td>Diversity</td></tr>
</table>

## Support and possibilism

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Terminology</th><th style="background:#f0f0f0">Source</th><th style="background:#f0f0f0">Connection</th><th style="background:#f0f0f0">Framework term</th></tr></thead>
<tr><td><strong>Possibilistic shadow</strong> Υ : C → SetMulti</td><td><a href="https://arxiv.org/abs/2308.00651">Fritz et al. 2023</a></td><td>The Lean proof's Support class IS this. Collapses probabilistic to possibilistic. support_bind = monad multiplication for supp : V ⇒ H.</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Support.lean">Support typeclass</a></td></tr>
<tr><td>Unit of Hoare hyperspace monad H</td><td><a href="https://arxiv.org/abs/1910.03752">Fritz-Perrone-Rezagholi 2021</a></td><td>σ(x) = cl({x}). Pure computation has singleton support.</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Support.lean">support_pure</a></td></tr>
<tr><td>supp(E(ξ)) = U(supp<sub>#</sub>(supp(ξ)))</td><td><a href="https://arxiv.org/abs/1910.03752">Fritz-Perrone-Rezagholi 2021</a></td><td>Support of composite = closure of union of conditional supports. Bind distributes support via existential.</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Support.lean">support_bind</a></td></tr>
<tr><td>Closed subsets, lower Vietoris topology</td><td><a href="https://arxiv.org/abs/1910.03752">Fritz-Perrone-Rezagholi 2021</a></td><td>The codomain of the support monad morphism. Algebras are complete join-semilattices.</td><td>Hoare hyperspace H</td></tr>
<tr><td>Functorial iff <strong>causal</strong></td><td><a href="https://arxiv.org/abs/2308.00651">Fritz et al. 2023 Thm 3.1.19</a></td><td>Causality axiom = composition condition for supports. The pipeline is causal.</td><td>Support is functorial</td></tr>
<tr><td><strong>Static idempotent</strong> (e =<sub>e</sub> id)</td><td><a href="https://arxiv.org/abs/2308.00651">Fritz et al. 2023</a></td><td>Iteration-stable = static idempotent. Splitting = having a support (Prop 4.4.1). Fixed-point structure captured by support object.</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Contracts.lean">IterationStable</a></td></tr>
<tr><td><strong>Gap:</strong> |Υ(p)| as lax functor</td><td>Nobody yet</td><td>Cardinality of possibilistic shadow. Would connect Leinster magnitude to Fritz support. Missing bridge for diversity.</td><td><a href="/the-natural-framework">Diversity (Attend)</a></td></tr>
</table>

## Contracts and composition

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Terminology</th><th style="background:#f0f0f0">Source</th><th style="background:#f0f0f0">Connection</th><th style="background:#f0f0f0">Framework term</th></tr></thead>
<tr><td>Predicate on outputs (β → Prop)</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Contracts.lean">Lean proof</a></td><td>Each pipeline stage carries a postcondition. All six contracts quantify over the support of the kernel.</td><td><a href="/the-handshake">Contract</a></td></tr>
<tr><td><strong>Hoare postcondition</strong></td><td><a href="https://doi.org/10.1007/978-3-030-72019-3_9">Gaboardi et al. ESOP 2021</a></td><td>Graded Hoare logic gives pre/postconditions for graded monads categorically. ContractPreserving IS a Hoare triple.</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Contracts.lean">ContractPreserving</a></td></tr>
<tr><td><strong>Restricted pointwise order</strong></td><td><a href="https://arxiv.org/abs/2601.14846">Kura-Gaboardi et al. 2026 Def 7</a></td><td>f ≤<sub>P</sub> g iff ordering holds where predicate is non-bottom. Post(N) implies Pre(N+1), restricted to support. <code>forward_triple</code> chains four COMP rules through real pre/postconditions — machine-checked.</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Hoare/Comp.lean">Handshake (Comp.lean)</a></td></tr>
<tr><td><strong>Graded monad lifting</strong></td><td><a href="https://arxiv.org/abs/2601.14846">Kura-Gaboardi et al. 2026</a></td><td>Lifting through predicate fibration Pred<sub>Ω</sub>(C) → C. Interpreting in total category preserves fibrational structure.</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Contracts.lean">Contracts propagate</a></td></tr>
<tr><td>Pred<sub>Ω</sub>(C) → C</td><td><a href="https://doi.org/10.1016/S0049-237X(99)80004-6">Jacobs 2001</a></td><td>Standard construction. SCCompC gives dependent types on top. The fiber over each morphism carries its contracts.</td><td>Predicate fibration</td></tr>
<tr><td><strong>Para construction</strong> C<sub>γ</sub>(X,Y) = C(γ⊗X, Y)</td><td><a href="https://arxiv.org/abs/2405.09391">Liell-Cock & Staton POPL 2025</a></td><td>The grade is a tensor factor. Grading and stochastic semantics are the same structure.</td><td><a href="/ambient-category">Graded monad = Markov cat</a></td></tr>
<tr><td><strong>Op-lax functor</strong> R : ImP → Kl(CP)</td><td><a href="https://arxiv.org/abs/2405.09391">Liell-Cock & Staton 2025 Thm 5.6</a></td><td>R(g∘f) ⊆ R(g)∘R(f). Composing in ImP gives tighter uncertainty sets than composing in the quotient. Subset = refinement.</td><td>Tighter bounds under composition</td></tr>
<tr><td>B<sup>op</sup> → PreMon</td><td><a href="https://arxiv.org/abs/2601.14846">Kura-Gaboardi et al. 2026 Def 6</a></td><td>The grading monoid varies with the base index. Effects (contracts) are value-dependent, not just type-dependent.</td><td>Indexed preordered monoid</td></tr>
</table>

## Variational derivations

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Terminology</th><th style="background:#f0f0f0">Source</th><th style="background:#f0f0f0">Connection</th><th style="background:#f0f0f0">Framework term</th></tr></thead>
<tr><td>Optimality over feasible set</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Variational.lean">Lean proof</a></td><td>Element-level: x is feasible and no feasible y has lower cost. Used for Consolidate and Filter.</td><td><a href="/ambient-category#derived-consolidate">MinimizesOn</a></td></tr>
<tr><td>Incumbent is always admissible</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Variational.lean">Lean proof</a></td><td>The current policy is always a feasible candidate. Optimal output ≤ incumbent. Derives Consolidate's lossiness.</td><td><a href="/ambient-category#derived-consolidate">self_feasible</a></td></tr>
<tr><td>Nontrivial feasible reduction exists</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Variational.lean">Lean proof</a></td><td>For every input, a strictly smaller feasible output exists. Minimality + witness → strict reduction. Derives Filter's gating.</td><td><a href="/ambient-category#derived-filter">strict_witness</a></td></tr>
<tr><td>Contract as optimality condition</td><td><a href="https://github.com/kimjune01/natural-framework/blob/master/NaturalFramework/Variational.lean">Lean proof</a></td><td>Constructors that build contract structures from optimization problems. Plug into existing handshake machinery.</td><td><a href="/ambient-category#contracts-as-optimality-conditions">fromOptimal</a></td></tr>
</table>

## Open bridges

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Bridge</th><th style="background:#f0f0f0">Connects</th><th style="background:#f0f0f0">Would give us</th><th style="background:#f0f0f0">Search terms</th></tr></thead>
<tr style="background:#e8f8e8"><td>Hoare logic over Markov category</td><td><a href="https://arxiv.org/abs/2507.18238">Bonchi-Di Lavore-Roman-Staton 2025</a></td><td><strong>CLOSED.</strong> Stoch is a posetal imperative category (Cor. 76). All Hoare rules (SKIP, COMP, ASSIGN, LOOP, WHILE...) derived as theorems (Thm 79). Predicates = morphisms X → 1. Triples = inequalities in posetal structure.</td><td>Staton's "imperative category" = traced distributive copy-discard category. Markov categories ARE copy-discard categories. Paper explicitly names Stoch and proves the rules.</td></tr>
<tr><td>Semiring-valued monad via change of base</td><td><a href="https://arxiv.org/abs/1910.03752">Fritz-Perrone-Rezagholi supp : V ⇒ H</a> + <a href="https://www.cambridge.org/core/books/entropy-and-diversity/496CF94AEA7B33F15904BD4FC8CC2369">Leinster magnitude</a></td><td>Diversity contract derived variationally — DPP maximizes support cardinality under capacity</td><td>Double dualization uses a semiring S: {0,1} → reachability, [0,∞) → probability. <strong>(ℕ, +, 0) → counting.</strong> Not via double dualization, but the <a href="https://dl.acm.org/doi/10.1145/3473577">free ℕ-semimodule monad</a> (= multiset monad) exists on Set. <a href="https://arxiv.org/abs/2105.06908">Jacobs</a> proves a distributive law M∘D → D∘M (multiset over distribution). Compose with support to track cardinality.</td></tr>
<tr><td>Categorical DPPs</td><td>Exterior algebra functor + Markov categories</td><td>The concrete Attend mechanism (DPP kernel) with categorical semantics</td><td>determinantal point process categorical; DPP monoidal; L-ensemble categorical</td></tr>
<tr><td>Coding theorems</td><td><a href="https://arxiv.org/abs/2212.11719">Fritz entropy</a> + Shannon theory</td><td>Consolidate's compression as a categorical rate-distortion theorem</td><td>rate-distortion Markov category; Wyner-Ziv categorical</td></tr>
<tr><td>Natural gradient as morphism</td><td><a href="https://link.springer.com/chapter/10.1007/978-3-031-38271-0_27">Perrone info geometry</a> + optimization</td><td>Consolidate's update step as a gradient flow on the statistical manifold</td><td>natural gradient categorical; gradient descent enriched Markov</td></tr>
</table>

## Authors and papers

<table style="width:100%; font-size:13px;">
<thead><tr><th style="background:#f0f0f0">Author</th><th style="background:#f0f0f0">Paper</th><th style="background:#f0f0f0">What it does</th></tr></thead>
<tr><td rowspan="3"><strong>Tobias Fritz</strong></td><td><a href="https://arxiv.org/abs/1908.07021">Markov categories (2020)</a></td><td>Defines the ambient category for stochastic morphisms. Copy-naturality distinguishes deterministic from stochastic. Informativeness preorder captures sufficient statistics.</td></tr>
<tr style="background:#f8f8f8"><td><a href="https://arxiv.org/abs/2212.11719">Markov Categories and Entropy (2024)</a></td><td>Defines entropy categorically as distance from determinism. Enriched Markov categories with divergences on hom-sets. Data processing inequality proved abstractly.</td></tr>
<tr><td><a href="https://arxiv.org/abs/2308.00651">Supports and idempotent splitting (2023)</a></td><td>Defines supports abstractly in Markov categories. Supports are functorial iff the category is causal. Static idempotents split iff they have supports.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Fritz, Perrone, Rezagholi</strong></td><td><a href="https://arxiv.org/abs/1910.03752">Support as monad morphism (2021)</a></td><td>Proves supp : V ⇒ H is a monad morphism from valuations to Hoare hyperspace. Both constructed via double dualization against different semirings.</td></tr>
<tr><td><strong>Baez, Fritz, Leinster</strong></td><td><a href="https://arxiv.org/abs/1106.1791">Entropy characterization (2011)</a></td><td>Shannon entropy is the unique functorial, convex-linear, continuous information loss assignment in FinProb, up to scale.</td></tr>
<tr><td rowspan="2"><strong>Sam Staton</strong></td><td><a href="https://arxiv.org/abs/2507.18238">Program Logics via Distributive Monoidal Categories (2025)</a></td><td>Derives Hoare logic from traced distributive copy-discard categories ("imperative categories"). Proves Stoch is a posetal imperative category. All Hoare rules follow as theorems.</td></tr>
<tr style="background:#f8f8f8"><td><a href="https://arxiv.org/abs/2405.09391">Compositional Imprecise Probability (POPL 2025)</a></td><td>Graded monads over Markov categories for imprecise probability. The para construction makes the graded model itself a Markov category.</td></tr>
<tr><td rowspan="2"><strong>Marco Gaboardi</strong></td><td><a href="https://doi.org/10.1007/978-3-030-72019-3_9">Graded Hoare Logic (ESOP 2021)</a></td><td>Hoare triples parameterized by a preordered monoid grade. Categorical semantics via graded Freyd categories over coherent fibrations. Instantiated for cost, privacy, and probability.</td></tr>
<tr><td><a href="https://arxiv.org/abs/2601.14846">Indexed graded monads (2026)</a></td><td>Graded monads parameterized fibrewise over a predicate fibration. Restricted pointwise order propagates pre/postconditions through composition.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Shin-ya Katsumata</strong></td><td><a href="https://arxiv.org/abs/2206.05716">Divergences on Monads (MSCS 2023)</a></td><td>Divergences on a monad = enrichments of its Kleisli category. Connects metric structure on morphism spaces to relational Hoare logic. Instantiated for differential privacy and cost.</td></tr>
<tr><td rowspan="2"><strong>Bart Jacobs</strong></td><td><a href="https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/abs/weakest-preconditions-in-fibrations/657A41FD194D8CC5E4662B71F2E1454E">Weakest preconditions in fibrations (2014)</a></td><td>Derives wp-semantics from order-enriched Kleisli categories via poset fibrations. Instantiated for the distribution monad — whose Kleisli category is FinStoch.</td></tr>
<tr><td><a href="https://www.cs.ru.nl/B.Jacobs/PAPERS/ProbabilisticReasoning.pdf">Structured Probabilistic Reasoning (2025 draft)</a></td><td>Book-length treatment of distributions, predicates, channels, conditioning via effectus theory. Cites Fritz extensively but uses his own formalism. FPred fibration for fuzzy predicates.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Tom Leinster</strong></td><td><a href="https://www.cambridge.org/core/books/entropy-and-diversity/496CF94AEA7B33F15904BD4FC8CC2369">Entropy and Diversity (2021)</a></td><td>Hill diversity numbers are the unique axiomatic diversity measures. Diversity is a special case of magnitude — the categorical generalization of cardinality for enriched categories.</td></tr>
<tr><td><strong>Paolo Perrone</strong></td><td><a href="https://link.springer.com/chapter/10.1007/978-3-031-38271-0_27">Categorical Information Geometry (2023)</a></td><td>Information geometry inside enriched Markov categories. Divergences in hom-spaces recover Shannon/Renyi entropy, DPI, and the Gini-Simpson index.</td></tr>
<tr style="background:#f8f8f8"><td><strong>David Spivak</strong></td><td><a href="https://arxiv.org/abs/1305.0297">Operad of wiring diagrams (2013)</a></td><td>Typed ports and supplier assignment for composing boxes in wiring diagrams. Gives the syntax layer — which boxes connect to which.</td></tr>
<tr><td><strong>Kidney & Wu</strong></td><td><a href="https://dl.acm.org/doi/10.1145/3473577">Algebras for Weighted Search (ICFP 2021)</a></td><td>Free semimodule monad parameterized by arbitrary semiring S. S = ℕ gives multiset monad (counting). S = [0,1] gives probability. Unifies search and probability via semiring choice.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Chen & Vigneaux</strong></td><td><a href="https://arxiv.org/abs/2303.00879">Categorical Magnitude and Entropy (2023)</a></td><td>Unifies Shannon entropy and log(magnitude) for finite categories with probability. Recovers magnitude under uniform distribution. Invariant of individual categories, not a functor on morphisms.</td></tr>
<tr><td><strong>Luca Reggio</strong></td><td><a href="https://arxiv.org/abs/1807.10637">Semiring-valued measures (2020)</a></td><td>Codensity monad of finite S-semimodules gives S-valued measures on Stone spaces. Change-of-semiring framework for codensity monads. Requires finite semirings.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Kenta Cho</strong></td><td><a href="https://arxiv.org/abs/1512.05813">Introduction to Effectus Theory (2015)</a></td><td>With Jacobs. Predicates as effect-algebra-valued maps (X → 1+1), not subobjects. States/effects duality with Born rule. Parallel formalism to Markov categories.</td></tr>
<tr><td><strong>Dario Stein</strong></td><td><a href="https://arxiv.org/abs/2312.17141">Probabilistic Programming with Exact Conditions (2023)</a></td><td>With Staton. Internal language of CD categories gives precise correspondence between Markov categories and a class of programming languages. Exact conditioning as categorical structure.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Eigil Rischel</strong></td><td><a href="https://compositionality.episciences.org/13509">Infinite products and zero-one laws (2020)</a></td><td>With Fritz. Kolmogorov and Hewitt-Savage zero-one laws proved in categorical probability. Exchangeability and independence axiomatized.</td></tr>
<tr><td><strong>Tomáš Gonda</strong></td><td><a href="https://arxiv.org/abs/2212.11719">Markov Categories and Entropy (2024)</a></td><td>With Fritz, Perrone, Rischel. Categorical entropy recovers Shannon, Renyi, and the Gini-Simpson index used in ecology — direct bridge to Leinster's diversity.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Arthur Parzygnat</strong></td><td><a href="https://arxiv.org/abs/2001.08375">Quantum Markov categories (2020)</a></td><td>Bayesian inversion as dagger structure on morphisms. Three levels of reversibility: inverses, disintegrations, Bayesian inverses. No-broadcasting theorem.</td></tr>
<tr><td><strong>Elena Di Lavore</strong></td><td><a href="https://arxiv.org/abs/2502.03477">Partial Markov Categories (2025)</a></td><td>With Roman, Sobocinski. Blends Fritz's Markov categories with restriction categories. Observations, Bayes' theorem, Pearl's and Jeffrey's updates in categorical terms.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Prakash Panangaden</strong></td><td><a href="https://www.worldscientific.com/worldscibooks/10.1142/p595">Labelled Markov Processes (2009)</a></td><td>Continuous-state probabilistic transition systems as coalgebras. Bisimulation metrics = behavioral distance between processes. Logical characterization of bisimulation.</td></tr>
<tr><td rowspan="2"><strong>Jules Hedges</strong></td><td><a href="https://arxiv.org/abs/1603.04641">Compositional Game Theory (2018)</a></td><td>With Ghani, Kupke, Forsberg. Nash equilibrium as a compositional predicate on strategy profiles — checked locally on subgames. Open games via string diagrams.</td></tr>
<tr><td><a href="https://arxiv.org/abs/2009.06831">Mixed Strategies (2020)</a></td><td>With Ghani, Kupke, Lambert. Relational Kleisli lifting of the probability monad lifts equilibrium predicates from pure to probabilistic games.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Matteo Capucci</strong></td><td><a href="https://arxiv.org/abs/2105.06332">Towards Foundations of Categorical Cybernetics (2021)</a></td><td>With Gavranović, Hedges, Rischel. Selection relations on parametrised optics. "What is a goal but a predicate on a system?" Goals unify optimization, homeostasis, learning, equilibria.</td></tr>
<tr><td><strong>Toby Smithe</strong></td><td><a href="https://arxiv.org/abs/2109.04461">Bayesian Lenses. Statistical Games (2021)</a></td><td>Bayesian inversions compose as lenses in a Markov category. Statistical games = optics + free-energy objective. Explicit bridge between Fritz and the cybernetics community.</td></tr>
<tr style="background:#f8f8f8"><td><strong>Ho, Wu, Raad</strong></td><td><a href="https://arxiv.org/abs/2507.15530">Bayesian Separation Logic (POPL 2026)</a></td><td>Hoare logic for Bayesian probabilistic programming. Model is s-finite kernels. Internal Bayes' theorem via disintegration. Frame rule = probabilistic independence.</td></tr>
</table>

---

## Jargon decoder

For software engineers who know code but not the math vocabulary.

<table style="width:100%; font-size:13px;">
<thead><tr>
<th style="background:#f0f0f0">Category theory</th>
<th style="background:#f0f0f0">Software equivalent</th>
<th style="background:#f0f0f0">What it is → what it unlocks</th>
</tr></thead>
<tr><td>Category</td><td>Type system + composition</td><td>Objects are types, morphisms are functions, composition is chaining. → Prove something about composition once, it holds for every instance.</td></tr>
<tr style="background:#f8f8f8"><td>Morphism</td><td>Function</td><td>A → B. Takes input, produces output. → The building block everything else is made of.</td></tr>
<tr><td>Functor</td><td>Adapter / map</td><td>Translates one type system into another, preserving composition. → Port theorems between domains for free.</td></tr>
<tr style="background:#f8f8f8"><td>Natural transformation</td><td>API migration</td><td>Converts between two adapters without breaking anything. → Swap implementations without re-proving correctness.</td></tr>
<tr><td>Monad</td><td>Plugin architecture</td><td>A wrapper (Promise, Maybe, List, Distribution) with a composition law (flatMap). → Swap the wrapper, keep all your theorems.</td></tr>
<tr style="background:#f8f8f8"><td>Kleisli category</td><td>Everything that uses this plugin</td><td>The world of functions that return wrapped values. kl(Promise) = async functions. → One composition law works for every monad.</td></tr>
<tr><td>Kleisli composition (>=>)</td><td>flatMap / .then() / >>=</td><td>Chain two wrapped-output functions. Run the first, feed each result into the second. → Chain stochastic functions the same way you chain Promises.</td></tr>
<tr style="background:#f8f8f8"><td>Adjunction</td><td>Optimal adapter pair</td><td>Two functors that are "best possible" translations in opposite directions. → Guarantees the translation loses the minimum possible information.</td></tr>
<tr><td>FinStoch</td><td>Dict of dicts</td><td>Stochastic matrices. For each input key, a probability distribution over output keys. → Probability becomes composition, not special-case math.</td></tr>
<tr style="background:#f8f8f8"><td>Markov category</td><td>Dict of dicts + copy + delete</td><td>FinStoch with the ability to duplicate and discard data. → Detect determinism vs stochasticity by a single test (copy-naturality).</td></tr>
<tr><td>Copy-natural (C_det)</td><td>Pure function</td><td>Deterministic. Same input always gives same output. Commutes with copy. → One test tells you if a function is pure: does copying commute?</td></tr>
<tr style="background:#f8f8f8"><td>Support</td><td>Set of possible outputs</td><td>Which keys have nonzero probability. Forget the weights, keep the keys. → Prove safety without computing probabilities.</td></tr>
<tr><td>Possibilistic shadow</td><td>support(distribution)</td><td>Collapse probabilities to yes/no. <code>{'{k for k,v in d.items() if v>0}'}</code>. → Defer probability calculations — reason about reachability first.</td></tr>
<tr style="background:#f8f8f8"><td>Monad morphism</td><td>Plugin-to-plugin adapter</td><td>Converts wrapped values from one monad to another, preserving flatMap. → Translate between probability and reachability without losing composition.</td></tr>
<tr><td>Hoare triple {'{P}'} c {'{Q}'}</td><td>assert P; c(); assert Q</td><td>If P holds before running c, Q holds after. → Machine-check that your pipeline can't produce bad output.</td></tr>
<tr style="background:#f8f8f8"><td>Weakest precondition</td><td>Reverse assert</td><td>Given c and Q, what's the minimum P that guarantees Q? → Automatically compute what your input must satisfy.</td></tr>
<tr><td>Graded monad</td><td>Effect system with costs</td><td>Like a monad but tracks how much side effect each computation uses. → Budget side effects across a pipeline — costs compose additively.</td></tr>
<tr style="background:#f8f8f8"><td>Preordered monoid</td><td>Cost algebra</td><td>Costs add (monoid) and can be compared (preorder). Nat, privacy budget, resource levels. → Swap the cost model, keep the composition theorems.</td></tr>
<tr><td>Fibration</td><td>Type → metadata mapping</td><td>Each type carries a layer of predicates/properties above it. Reindexing = weakest precondition. → Properties propagate backward through composition automatically.</td></tr>
<tr style="background:#f8f8f8"><td>Optic / Lens</td><td>Getter + setter pair</td><td>Forward: read data. Backward: update data. Compose bidirectionally. → Build forward inference + backward learning as one composable structure.</td></tr>
<tr><td>String diagram</td><td>Data flow diagram</td><td>Boxes are functions. Wires are types. Connecting wires = composition. → Visual proofs — if the diagram connects, the types check.</td></tr>
<tr style="background:#f8f8f8"><td>Traced monoidal category</td><td>Feedback loop</td><td>Output feeds back to input. while loops, recursion, closed systems. → Prove loop invariants from the categorical structure, not by hand.</td></tr>
<tr><td>Posetal</td><td>Has a ≤ ordering</td><td>Morphisms can be compared. "This program refines that one." → Refinement composes — if each stage improves, the pipeline improves.</td></tr>
<tr style="background:#f8f8f8"><td>Imperative category</td><td>Language with Hoare rules</td><td>A category where assert/run/assert works as a theorem, not an assumption. → Every Hoare rule is free once you verify the category has the right structure.</td></tr>
<tr><td>Effect algebra</td><td>Fuzzy boolean</td><td>Predicates that can be partial (70% true). Generalizes boolean contracts to [0,1]. → Grade your assertions quantitatively, not just pass/fail.</td></tr>
<tr style="background:#f8f8f8"><td>Enriched category</td><td>Typed hom-sets</td><td>The "space" between two objects carries structure (distance, cost, lattice order). → Measure how far apart two programs are, not just whether they're equal.</td></tr>
<tr><td>DPI</td><td>Processing can't create info</td><td>H(output) ≤ H(input). You can only lose or preserve, never gain. → Proves your pipeline must have external input or it dies.</td></tr>
<tr style="background:#f8f8f8"><td>Magnitude</td><td>Effective size</td><td>How many "independent" things are in a collection. Diversity = categorical cardinality. → Measure diversity as a single number that respects composition.</td></tr>
</table>

---

*Updated 2026-03-23. Previous vocabulary: [Type Forcing](/type-forcing) (Spivak), [Ambient Category](/ambient-category) (Fritz).*
