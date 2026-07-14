---
variant: post-paper
title: "Formally Verified VCG Ad Auctions for LLMs"
subtitle: "Zero-sorry Lean 4 artifact: DOI 10.5281/zenodo.21214697"
tags: vector-space
autonumber: true
---

*[Download PDF](/assets/formally-verified-vcg-mechanisms.pdf)*

## Abstract {-}

Large language model (LLM) chat assistants are becoming an advertising surface. A scoring rule for them has circulated as a heuristic: embed the conversation as a point `x` in a continuous embedding space, have each advertiser declare a center `c` (who their customer is), a reach `σ` (how wide a neighborhood they serve), and a bid `b` (what a conversion is worth). The slot beside the reply goes to the highest `log(b) - ‖x-c‖²/σ²`. The mechanism touches nothing inside the model: no training, no modification of the responses. We prove in Lean 4, with zero `sorry`, that the rule is VCG: truthful reporting of bid, center, and reach is a dominant strategy, the allocation maximizes welfare at every query point, and its territories form a power diagram with keyword auctions as the degenerate case. The auction sells regions of embedding space.

## One-Shot Bidding

Keyword auctions are strategically broken, and the industry monetizes the breakage. [Edelman, Ostrovsky and Schwarz (2007)](https://www.aeaweb.org/articles?id=10.1257/aer.97.1.242) proved that Google's Generalized Second-Price auction has no dominant-strategy equilibrium: your optimal bid depends on bids you cannot see. First-price display auctions require shading by an amount that also depends on bids you cannot see. The response was an autobidding industry, agents running machine learning against each other to approximate what [Vickrey (1961)](https://doi.org/10.2307/2977633) made exact sixty-five years ago in one shot: report your value, pay the externality, done.

Ad auctions for large language models (LLMs) restart the design problem, a chance to get the incentives right on day one. The setting: a user's conversation embeds to a point `x` in a real inner product space; each advertiser declares a center `c` (who their customer is), a reach `σ` (how wide a neighborhood they serve), and a bid `b` (what a conversion is worth). The platform scores each advertiser at `x` and the highest score wins. The scoring rule was proposed in a blog series, an open-source exchange implements it, multi-agent simulations probe its market dynamics, and an interactive explorer renders the allocation live: drag a center or raise a bid and the territories shift.[^1] What was missing is a proof that the mechanism deserves the trust the proposal asks for.

Here we supply the proof, in Lean, so that trust in the mechanism reduces to running a build command. The contribution is one bridge lemma, `score_eq_log_reportedVal`: the scoring rule is the logarithm of the value a report implies, unconditionally. Everything downstream is the classical VCG argument of [Vickrey (1961)](https://doi.org/10.2307/2977633), [Clarke (1971)](https://doi.org/10.1007/BF01726210), and [Groves (1973)](https://doi.org/10.2307/1914085), executed formally. On top of the chain we prove two geometric bookends: the allocation is a power diagram for arbitrary heterogeneous reaches, and the mechanism collapses to Vickrey's sealed-bid second-price auction at any keyword point.

## Model

An advertiser's report is a triple `(c, σ, b)` with `σ, b > 0`. Their private valuation is a triple `(c*, σ*, v)` of the same shape, and each report field may differ from its starred counterpart. The distinction is operational. Reported distance controls which impression the advertiser wins; true distance controls whether the person who sees the ad converts. A burger advertiser can declare a center near a shoe query, but the declaration does not turn burgers into shoes. Its true value at query `x` remains Gaussian around its private center:

```
trueVal(x) = v · exp(-‖x - c*‖² / σ*²)
```

True value reads as margin times conversion probability. The Gaussian is strictly positive: even a badly matched impression can convert, only with a probability that decays rapidly with semantic distance. That is the object observed in impression advertising, not a binary relevance label. The Gaussian family is an approximation, and the best available one: embedding coordinates are not human-interpretable, so a peak and a width are all an advertiser can meaningfully declare, and the Gaussian is the [maximum-entropy](https://en.wikipedia.org/wiki/Maximum_entropy_probability_distribution) model of a conversion curve known only by those two; any other decay imports structure for which the advertiser has no evidence. The theorems hold inside the family, and the Limits section says what stays outside it. The platform scores reports by

```
score(x) = log(b) - ‖x - c‖² / σ²
```

and allocates each query to an argmax of score. Thus allocation uses the reported Gaussian while utility uses the fixed true Gaussian. Changing a report changes the impressions won, never the underlying conversion surface. The winner pays the Clarke pivot, the externality their presence imposes on the rest. With a single winner per query the pivot has a closed form: losers pay nothing, and the winner pays the runner-up's implied value (zero when unopposed).

```
payment_w(x) = max_{j ≠ w}  b_j · exp(-‖x - c_j‖² / σ_j²)
```

Utility is quasilinear. Impressions are opt-in opportunities: the model does not force an advertiser into an auction it declined to enter. A publisher may separately restrict eligibility, but that policy defines the player set upstream and is not a second allocation mechanism here. All definitions follow Nisan's mechanism-design chapter in [Nisan, Roughgarden, Tardos and Vazirani, eds. (2007)](https://doi.org/10.1017/CBO9780511800481).

The scoring rule is the embedding-space member of a known family. [Lahaie and Pennock (2007)](https://doi.org/10.1145/1250910.1250918) analyzed keyword scoring rules of the form `bid × quality^s`. Ranking by the score written in base `β` is ranking by `b · q^ln(β)` with quality `q = exp(-‖x-c‖²/σ²)`. The log base is therefore the squashing parameter, `s = ln(β)`, and the squashing-parameter literature transfers intact: sweeping the log base is the platform's revenue-relevance dial.

![The allocation is the upper envelope of score parabolas. Winning intervals along the axis are the power-diagram cells; a higher bid raises a parabola, a wider σ flattens it.](/assets/vcg-fig1.svg)

The formalization states everything over an arbitrary real inner product space. No finite-dimension hypothesis appears anywhere in the chain: the theorems hold for a 384-dimensional sentence embedding and for an infinite-dimensional feature space alike.

## The Bridge

The mechanism-design results hang on one identity. Define the value implied by a report, `reportedVal(x) = b · exp(-‖x - c‖²/σ²)`. Then

```math
score(x) = log(reportedVal(x))
```

with no truthfulness hypothesis (`score_eq_log_reportedVal`). The disguise is a logarithm. Log is monotone, so the argmax of score is the argmax of reported value. The mechanism always maximizes reported welfare, which is the allocation rule VCG requires. When a report is truthful, reported value equals true value (`reportedVal_eq_trueVal_of_truthful`), and the same identity becomes `score = log(trueVal)` (`score_eq_log_trueVal`). The winner is the advertiser who values the impression most (`winner_maximizes_welfare`).

## Dominant Strategy

`vcg_dsic` is the main incentive theorem: for any deviation report `r'`, a truthful player's utility is at least their deviated utility, regardless of what every other player reports. The Clarke payment is computed from others' reported values only, so a player's report moves their allocation and never their price schedule (`welfareOthersWithout_invariant`); the four-case comparison then closes the argument. A false center can make the burger advertiser win the shoe impression, but its utility still contains the small true burger-conversion value, while its payment contains the value of the shoe advertiser it displaced.

The theorem proves more than the informal claim usually attached to VCG. Truthfulness here constrains all three report fields: center, reach, and bid. Misreporting your center toward a traffic hotspot is a deviation `r'` like any other, and the theorem says it cannot profit you.

The qualifier is **weakly** dominant. In a thin market an unopposed winner pays zero, so every center report that preserves its allocation gives the same utility. The artifact proves this limit explicitly: with one player, pointwise and expected utility are invariant under every report (`playerUtility_invariant_of_subsingleton`, `expectedPlayerUtility_invariant_of_subsingleton`). Weak dominance rules out profitable manipulation; it does not by itself identify the literal report.

Competition closes that gap wherever it is informative. If truth wins a query, a deviation loses it, and true value strictly clears the best rival welfare, utility falls strictly (`vcg_strict_at_contested_point`). If allocation changes throughout a positive-weight region away from competitive ties, expected utility falls strictly (`vcg_strict_expected_on_allocation_change_set`). Equivalently, an expected-utility tie cannot place positive query weight on its strictly contested allocation-disagreement set (`expected_utility_tie_disagreement_not_positive`). The strict expectation premise is separate from monotonicity: `QueryMeasure.PositiveOn` records that the query distribution detects a region, and finite weighted query logs discharge it constructively whenever that region contains a logged query of positive weight.

This is the answer to the most immediate Hotelling objection. In spatial competition from [Hotelling (1929)](https://doi.org/10.2307/2224214) onward, sellers drift toward the center of the market; the analogue here is advertisers declaring centers near high-traffic regions. Inside this model such drift cannot profit, and drift that changes allocation on an informatively contested region is strictly costly. What remains are allocation-equivalent reports. Under an additional spatial-coverage condition that shrinks that equivalence class around `c*`, every selection from the surviving class converges to `c*` (`centers_converge_of_competitive_coverage`); the artifact states this implication but does not assume that arbitrary market entry supplies the coverage. Hotelling is therefore a stress test of the incentive claim, not a second mechanism or a claim about adjustment dynamics. Profitable drift can return through what the model excludes: budgets, volume-dependent objectives, endogenous products or creatives, and non-Gaussian true values.

## The Geometry

The name "power diagram auction" is now a theorem at two levels.

### Equal Reach

When two advertisers share `σ`, comparing scores at `x` is comparing power distances `‖x - c‖² - w` with sites at the centers and weights `w = σ² log(b)` (`score_le_iff_powerDist_le`). The score difference is an affine function of `x` (`score_sub_affine`), so cell boundaries are hyperplanes. That is the classical power diagram of [Aurenhammer (1987)](https://doi.org/10.1137/0216006), with bids setting the weights. When every advertiser shares `σ`, the winner rule is that cell assignment in `E` directly: the argmax of score minimizes power distance (`winner_minimizes_powerDist`), no lift required.

### Heterogeneous Reach

With distinct `σ`s the in-space boundaries curve, and the folk description of the allocation as a power diagram fails in `E`. It succeeds in `E × ℝ`. Lift each query to the paraboloid `(x, ‖x‖²)` and give advertiser `i` a lifted site and weight:

```
site_i = (σᵢ⁻² · cᵢ ,  -σᵢ⁻²/2)
w_i    = ‖σᵢ⁻² · cᵢ‖² + σᵢ⁻⁴/4 - σᵢ⁻² ‖cᵢ‖² + log(bᵢ)
```

Then

```
liftedPowerDist(x, ‖x‖²) = ‖x‖² + ‖x‖⁴ - score(x)
```

exactly (`liftedPowerDist_paraboloid`), and the leading terms are advertiser-independent. Maximizing score is minimizing lifted power distance (`score_le_iff_liftedPowerDist_ge`), and the auction's winner rule is the lifted diagram's cell assignment (`winner_minimizes_liftedPowerDist`). Aurenhammer proved diagrams of quadratic distance functions lift this way; the formalization instantiates his lift for this scoring rule and checks the algebra once. Exact O(log N) point location is a fixed-low-dimension result and does not survive embedding dimension, but the lift still pays at serving time: score comparisons are affine in the lifted query `(x, ‖x‖²)`, so finding the winner is a maximum-inner-product search against static lifted sites, which approximate-nearest-neighbor indexes and cache layers serve sublinearly in practice, with the O(N) scan as the exact fallback.

![The lift, drawn for a one-dimensional embedding. A tight advertiser T and a wide advertiser W produce two boundary points downstairs (T's cell is the interval between them); upstairs, the boundary is one straight radical axis cutting the paraboloid. Quadric bisectors in E are hyperplanes in E × ℝ.](/assets/vcg-fig2.svg)

## Keywords Recovered

The migration path follows from the geometry: a keyword is a tiny circle, a report whose reach has shrunk to a point, so keyword auctions are the degenerate case of the embedding auction and adopting the general mechanism strands no existing buyer. The claim is now a theorem pair.

### The Limit

At any point other than its center, a report's score diverges to `-∞` as `σ → 0`, while its score at the center is `log(b)` independent of `σ` (`keyword_is_degenerate_limit`, `score_at_center`). The tiny circle collapses to its point.

![Shrinking σ at a fixed center against a wide rival with equal bid. The score at the center is log b for every σ, while territory off-center collapses; in the limit the advertiser competes at one point only, on bid alone.](/assets/vcg-fig3.svg)

### The Mechanism

At a query point that is every advertiser's shared center, the Gaussian factor is `exp(0) = 1` for every bidder: reported value is the bid, the winner is a highest bidder (`winner_maximizes_bid_of_common_center`), the Clarke pivot equals the highest competing bid (`vcgPayment_common_center_second_price`), and every loser pays nothing (`vcgPayment_eq_zero_of_loser`). That is Vickrey's sealed-bid second-price auction, allocation and payment both. A keyword auction is what this mechanism does at a point.

## Optimality

Pointwise welfare maximization integrates. The step is bookkeeping, and the bookkeeping is compiled: for any measure over queries, expected welfare under the score-argmax allocation weakly dominates expected welfare under any rule the expectation operator evaluates, power-diagram or not (`integral_efficiency`, `gaussian_optimality`; the theorem statements carry the exact quantifiers). The capstone, `gaussian_vcg_weakly_dominates`, conjoins the three properties: welfare-optimal, dominant-strategy incentive compatible, equilibrium-efficient. The last is the welfare guarantee evaluated at truthful play, which `vcg_strategyproof` certifies as a Nash equilibrium. The artifact separately proves the equilibrium-decomposition theorem of [Ghani, Hedges, Winschel and Zahn (2018)](https://arxiv.org/abs/1603.04641): in their open games, where large games compose from smaller ones, an equilibrium of the composite induces equilibria of the components (`composed_equilibria_decompose`). Whether DSIC composes the same way is an open question, and the formalization records it as open instead of assuming it.

The weak-order chain uses one modeling assumption, `QueryMeasure.integral_mono`: a monotone expectation operator respects pointwise inequality (no normalization or probability mass required). Strict expected comparisons additionally carry `PositiveAt` or `PositiveOn`, stating that the operator detects a contested point or region. These are structure hypotheses, not Lean `axiom`s: `QueryMeasure.dirac` and `QueryMeasure.ofWeightedFinset` construct the operator, and a finite weighted query log constructs the strictness witness whenever a contested region contains a logged query of positive weight. Nothing here rests on a trusted axiom of our own (the artifact audit records the check). A measure-theoretic integral satisfies the corresponding interfaces on functions and positive-mass regions it can evaluate. Keeping the operator abstract lets the theorems quantify over query distributions instead of fixing one, and each theorem carries the exact strength it uses.

## Related Work

### LLM Ad Auctions

[Feizi, Hajiaghayi, Rezaei and Shin (2025)](https://arxiv.org/abs/2311.07601) survey the design space as four modules (modification, bidding, prediction, auction) and leave open how the pieces sustain an ad ecosystem. The idea of an auction inside the generation begins with [Dütting, Mirrokni, Paes Leme, Xu and Zuo (2024)](https://arxiv.org/abs/2310.10826), who aggregate advertisers' token distributions into the reply and price the result through a monotonicity condition. [Dubey, Feng, Kidambi, Mehta and Wang (2024)](https://arxiv.org/abs/2404.08126) auction placements inside an LLM-written summary of the ads. MOSAIC and the retrieval-time mechanism are later points on that line; all of them keep the ad inside the text the model emits.

[Soumalias, Curry and Seuken (2025)](https://arxiv.org/abs/2405.05905) give the prior LLM ad mechanism with dominant-strategy guarantees. Their MOSAIC auction allocates the reply itself: advertiser reward functions score candidate responses sampled from the model, and softmax selects one. Computing the exact welfare-maximizing reply is out of reach, so exact VCG is unavailable; the softmax allocation is instead cyclically monotone, and [Rochet (1987)](https://doi.org/10.1016/0304-4068(87)90007-3) turns cyclic monotonicity into dominant-strategy payments through a convex potential. Auctioning an embedded intent point instead of the reply shrinks the outcome space from token sequences to N known advertisers. Exact VCG becomes one argmax plus one counterfactual argmax, and the guarantees become simple enough for Lean to check. Allocating a separate ad object also removes MOSAIC's deployment costs: no M-fold candidate generation per query, deterministic winners an advertiser can budget against, and a discrete placement that can be attributed and priced.

[Hajiaghayi, Lahaie, Rezaei and Shin (2024)](https://arxiv.org/abs/2406.09459) place the auction at retrieval time instead: ads are probabilistically retrieved per discourse segment by bid and relevance, with incentive-compatible pricing. The outcome space is far smaller than MOSAIC's, but the placement still lives inside the generated text, and the winner is a draw rather than an argmax. The geometric mechanism keeps the retrieval-time simplicity while making the allocation deterministic and the ad a separate object.

[Alaei, Makhdoumi and Malekian (2026)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6212838) share the geometric premise: a user is an unknown preference vector, each advertiser a feature vector, match value their inner product. Their platform learns the vector as the conversation proceeds, trading a sharper estimate against the risk the user leaves. That learning dynamic is what the static model here holds fixed, and fixing the query point and the Gaussian family is what buys the closed-form diagram and the compiled proof.

The other family bakes advertising into the model by training. Alibaba's [LLM-Auction](https://arxiv.org/abs/2512.10551) post-trains the model with preference alignment to balance ad revenue against user experience, encoding commercial incentives directly in the weights. Training is the wrong cadence for an ad market: campaigns change hourly, fine-tuning takes weeks, and retraining per campaign rotation costs more than the campaign. It is also the wrong trust surface. Bias learned in weights cannot be audited from outside, and users cannot police it from inside either: [evaluators shown chatbot responses with embedded ads](https://arxiv.org/abs/2409.15436) failed to detect the ads and preferred the responses that contained them. The mechanism here is the opposite limiting case. The scoring rule is public, the allocation is its argmax, the incentive properties are a compiled theorem, and the audit reduces to a build command.

### Semantic Matching

Advertisers competing in a vector space is not new. [Grbovic et al. (2016)](https://arxiv.org/abs/1607.01869) learned joint query and ad embeddings to match ads beyond literal keywords, and embedding-based retrieval is now standard ad-system infrastructure. In that line the geometry supplies candidates or relevance features to a separate auction. Here the distance function is the valuation, and the auction is the geometry.

### Formalized Auctions

[Caminati, Kerber, Lange and Rowat (2013)](https://arxiv.org/abs/1308.1779) proved soundness of combinatorial Vickrey auctions in Isabelle and generated verified executable code. [Barthe, Gaboardi, Gallego Arias, Hsu, Roth and Strub (2015)](https://arxiv.org/abs/1502.04052) verified incentive compatibility for VCG in a probabilistic relational calculus, and [Jouvelot and Gallego Arias (2022)](https://github.com/jouvelot/mech.v) built mech.v, a Coq library that proves VCG's incentive properties generically and refines an online-advertising VCG down to that specification. Formalized VCG is not new, and neither is a verified online-ad mechanism. What is new here is the object: the verified allocation is a partition of a vector space, and the same artifact that checks truthfulness checks its identification as a power diagram. Kerber, Lange and Rowat ([2016](https://doi.org/10.1016/j.jmateco.2016.06.005)) formalized Vickrey's auction in Isabelle and argued mechanized reasoning should be ordinary practice in economic theory; [Ghani, Hedges, Winschel and Zahn (2018)](https://arxiv.org/abs/1603.04641) rebuilt game theory compositionally so that mechanisms assemble from smaller games. Here the practice extends from a discrete allocation rule to a geometric one.

### Filters and Reserves

[Hartline, Hoy and Taggart (2023)](https://arxiv.org/abs/2310.03702) show competitive efficiency survives reserve pricing. The same holds trivially here for any pre-auction relevance filter, since welfare maximization restricted to a nonempty eligible set is welfare maximization on that set (`tau_preserves_efficiency_among_eligible`). Reserves are also where revenue lives: the Clarke pivot collects only the runner-up's implied value, zero when a winner is unopposed, and a reserve puts a price floor under exactly those impressions.

## Limits

The theorems end where the model does, and the model is deliberately narrow.

| Element | In the formalization |
|---|---|
| Embedding space `E` | any real inner product space; dimension unconstrained, infinite allowed |
| Advertisers | arbitrary finite type; no bound on the count |
| Query distribution | universally quantified expectation operator; one assumption, monotonicity |
| Utility | quasilinear; no budget constraints |
| True valuations | isotropic Gaussian family |
| Deviations | any `(center, σ, bid)` triple |
| Rival allocation rules | any rule the expectation operator evaluates |
| Winners per query | exactly one; ties broken by fixed enumeration |


*Single winner.* Slates, pacing, and cross-impression externalities are outside the model.

*No budgets.* Budget-constrained clearing has known structure (with fixed budgets it is [semi-discrete optimal transport](https://arxiv.org/abs/2106.14730), whose solution is again a power diagram), but its incentives and dynamics are open. The simulations suggest the dynamics are where the difficulty lives.

*Gaussian truth.* The Gaussian family is a bidding language, and every deployed auction clears one: the reigning language is the keyword, the σ → 0 point mass of this same family. What a bidding language buys is expressiveness against clearing cost, the central tradeoff of the combinatorial-auction literature ([Nisan, 2000](https://doi.org/10.1145/352871.352872)). On that frontier the isotropic Gaussian is the most expressive language currently known to admit sub-linear clearing, exact VCG, and a compiled proof. Anisotropic preferences (elliptical rather than spherical reach) stay computable at O(N) per query but break the bridge lemma as stated; whether a lifted variant survives for quadratic-form preferences is the natural next theorem, since Aurenhammer's lift already accommodates general quadrics. Mixtures turn the score into a log-sum-exp whose bisectors admit no fixed-dimension lift, and the clearing speed and the proof leave with the geometry.

*Frozen embedder.* The embedding model is held fixed. Retraining or replacing it moves every conversation point and every declared center at once, invalidating reports with no advertiser misreporting anything; re-declaration cadence is an operational question the model does not pose.

*Statics only.* Nothing here says bidding dynamics converge. The simulations in the provenance note study the dynamics empirically; a formal convergence or limit-cycle result would be a separate paper's contribution.

## Artifact {-}

The formalization is at [github.com/kimjune01/auction-proof](https://github.com/kimjune01/auction-proof), archived as [DOI 10.5281/zenodo.21214697](https://doi.org/10.5281/zenodo.21214697), AGPL-3.0, [Lean 4](https://lean-lang.org/) (v4.29.0-rc6) with [Mathlib](https://github.com/leanprover-community/mathlib4). Verification:

```
lake exe cache get
lake build
```

Zero `sorry`, and no trusted axiom of our own: `#print axioms` on every theorem below returns only Lean's three standard background axioms (`propext`, `Classical.choice`, `Quot.sound`), because the single modeling assumption is a `QueryMeasure` typeclass that concrete instances discharge by proof. The claims-to-theorems map:

| Claim | Lean theorem | File |
|---|---|---|
| score = log(reported value) | `score_eq_log_reportedVal` | Efficiency.lean |
| winner maximizes true welfare | `winner_maximizes_welfare` | Efficiency.lean |
| truthful reporting is dominant | `vcg_dsic` | Strategyproof.lean |
| no allocation rule beats VCG | `gaussian_optimality` | GaussianOptimality.lean |
| capstone conjunction | `gaussian_vcg_weakly_dominates` | GaussianOptimality.lean |
| equal-σ power diagram, hyperplane bisectors, winner minimizes power distance | `score_le_iff_powerDist_le`, `score_sub_affine`, `winner_minimizes_powerDist` | PowerDiagram.lean |
| variable-σ power diagram via paraboloid lift | `liftedPowerDist_paraboloid`, `winner_minimizes_liftedPowerDist` | PowerDiagram.lean |
| keyword limit | `keyword_is_degenerate_limit` | VectorSpace.lean |
| exact Vickrey at a keyword point | `vcgPayment_common_center_second_price` | SecondPrice.lean |
| losers pay nothing | `vcgPayment_eq_zero_of_loser` | Strategyproof.lean |

## Acknowledgments {-}

Conversations with Sébastien Lahaie and Mohammad Hajiaghayi sharpened the mechanism-design framing, and Sébastien pointed me to MOSAIC. Errors, and the claims, are mine.

## Disclosures {-}

*LLM use.* This paper and its artifact were produced with large language models via [Claude Code](https://claude.ai/claude-code). The author directed the research and reviewed every claim; agents wrote the Lean proofs, generated the figures, and drafted the prose. A separate model ran an adversarial review of the prose against the formalization. No guarantee in this paper rests on any model's judgment: the artifact type-checks with zero `sorry`, and verification reduces to `lake build`.

*Funding.* Self-funded independent research. No external funding, no employer direction, no advertiser or platform relationship. The author maintains [openauction](https://github.com/kimjune01/openauction), the open-source exchange implementation.

[^1]: Proposal series: [june.kim/power-diagrams-ad-auctions](https://june.kim/power-diagrams-ad-auctions), [june.kim/the-price-of-relevance](https://june.kim/the-price-of-relevance), [june.kim/keywords-are-tiny-circles](https://june.kim/keywords-are-tiny-circles). Implementation: [github.com/kimjune01/openauction](https://github.com/kimjune01/openauction). Simulations: [june.kim/relocation-fees](https://june.kim/relocation-fees), [june.kim/relocation-fee-dividend](https://june.kim/relocation-fee-dividend). Demo: [june.kim/vectorspace-ads](https://june.kim/vectorspace-ads/).

---

*Part of the [Vector Space](/vector-space) series.*
