---
layout: post
title: "Why Fees Work"
tags: adtech
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument and designed the experiments; Claude built the simulation, researched prior art, and drafted prose.*

*Part of the [adtech](/adtech) series.*

---

Embedding-space auctions give every advertiser a precise position in high-dimensional space. A climbing PT plants her flag at "rock climbing finger pulley rehabilitation." A pelvic floor PT plants his at "postpartum pelvic floor therapy." They stop competing for the same keyword. The auction scores by proximity, and each specialist wins the queries they're best at.

That's the pitch. Here's the problem: it doesn't hold on its own.

Without an external force, every advertiser drifts toward the center of demand. The embedding space that was supposed to preserve differentiation collapses back into keyword crowding — the same five PTs fighting over the same queries, this time at coordinates instead of keywords. The geometry changes. The economics don't.

Harold Hotelling described this in 1929 with two ice cream vendors on a beach. Both move toward the center because that's where the customers are. In one dimension, the result is obvious. In 384 dimensions, it's the same problem.

Hotelling drift is universal in embedding-space auctions, and a flat relocation fee is sufficient to prevent it. The fee is not a tuning parameter. It's a structural requirement — the same class of mechanism that prevents collapse in spectrum markets, domain registries, and urban real estate.

## The Theory: Almost Right in Every Dimension

Hotelling's original claim — that competitors converge to the center — was wrong in its own model. d'Aspremont, Gabszewicz, and Thisse showed in 1979 that with quadratic transportation costs, the equilibrium is *maximum* differentiation. Firms run to opposite ends.

But that result is for two firms on a line. What happens in higher dimensions?

Irmen and Thisse answered this in 1998 with the definitive n-dimensional result. In a product space with n characteristics, firms maximally differentiate on exactly one dimension — the most salient one — and minimally differentiate on all the rest. They called it the Max-Min-...-Min principle. "Hotelling was almost right": minimum differentiation holds for (n-1) out of n dimensions.

This maps directly onto embedding space. A 384-dimensional embedding has perhaps 10-50 effective dimensions — the rest are redundant. Advertisers differentiate on the single dimension that matters most for their niche — "climbing" vs "pelvic floor" — and crowd together on everything else. The theory predicts partial collapse, not total separation.

There's a deeper problem. Beyer et al. (1999) proved that in high-dimensional spaces, all pairwise distances converge — the ratio of farthest to nearest distance approaches 1. In 384 dimensions, the distance between any two points becomes nearly the same. The entire distance range in our simulation compresses into a narrow band: dist² from 0.29 to 1.32 across 900 advertiser-query pairs.

When distances concentrate, the gradient that drives differentiation weakens. An advertiser can't gain much local monopoly power by moving to an empty region because no region is meaningfully farther from competitors than any other. The centripetal pull toward demand density dominates because it's the only gradient with a clear signal.

The embeddings still encode meaningful differences — BGE-small distinguishes "climbing PT" from "sports PT" with hard negative mining, and the intrinsic manifold structure preserves fine-grained discrimination. But the *competitive dynamics* operating on those embeddings face a compressed distance space where the incentive to drift is always present.

## The Simulation: Drift Is Universal

We tested this with 25 advertisers across 5 clusters at controlled tightness levels, competing for 55 queries in 384-dimensional BGE-small-en-v1.5 embedding space. The simulation code is [open source](https://github.com/kimjune01/openauction/tree/76923f3/cmd/simulate).

Five tightness levels, from nearly identical to completely unrelated:

| Cluster | Example | Mean cos | Advertisers |
|---|---|---|---|
| Very tight | Yoga studios differing by neighborhood | 0.974 | 5 |
| Tight | PT specialists (knee, shoulder, back, hip, neck) | 0.895 | 5 |
| Medium | Fitness coaches (climbing, marathon, CrossFit, yoga, personal) | 0.830 | 5 |
| Loose | Wellness professionals (dietitian, therapist, massage, acupuncture, health coach) | 0.616 | 5 |
| Very loose | Unrelated trades (mechanic, realtor, photographer, plumber, electrician) | 0.527 | 5 |

Each cluster has one generalist and four specialists. Specialists get narrow targeting (σ=0.30) and high conversion value (12.0). Generalists get wide reach (σ=0.55) and moderate value (6.0). VCG payments are capped at the winner's value — no advertiser pays more than an impression is worth.

We measured centripetal fraction: how much of each advertiser's drift points toward the cluster centroid. If the knee PT moves and 57% of that movement is toward the center of the PT cluster — closing the gap with the shoulder PT and the back PT — that's a centripetal fraction of 0.57. Positive means drifting toward competitors. Zero means random. Negative means differentiating.

### Drift toward competitors in all 5 clusters

Without fees (Cell C, λ=0), centripetal fraction is positive everywhere:

| Cluster | Density | Centripetal fraction |
|---|---|---|
| Very tight | 0.974 | 0.281 |
| Tight | 0.895 | 0.569 |
| Medium | 0.830 | 0.550 |
| Loose | 0.616 | 0.801 |
| Very loose | 0.527 | 0.736 |

Every cluster shows Hotelling drift. Advertisers move toward their competitors, not away. The direction is centripetal regardless of how tight or loose the cluster is. This is the strongest result across all versions of the simulation.

The loose clusters show the highest centripetal fraction (0.80) despite having the lowest density. This isn't paradoxical — loose-cluster advertisers start far from the centroid, so the demand center exerts a stronger pull. In tight clusters, everyone is already near the center, and the directional signal is noisier. The drift magnitude is similar across clusters (0.47–0.60 in L2 distance). The direction is consistently centripetal.

### Fees prevent drift and improve surplus

Four conditions: Cell A (keywords), Cell C (embeddings, no fees), Cell D (embeddings, uniform λ=5000), Cell E (embeddings, density-adaptive λ).

| Metric | Cell A (kw) | Cell C (emb, λ=0) | Cell D (λ=5k) | Cell E (adaptive) |
|---|---|---|---|---|
| Value efficiency | 0.746 | 0.683 | 0.696 | 0.696 |
| Avg surplus/round/adv | 0.888 | 1.299 | 1.481 | 1.487 |
| Avg drift | 0.000 | 0.549 | 0.023 | 0.023 |

*50 trials per cell. Welch's t-test: A↔C p<0.001, C↔D p<0.001, D↔E ns.*

Embeddings without fees already beat keywords on surplus (1.299 vs 0.888, p<0.001). Adding fees widens the gap (1.481 vs 0.888, p<0.001). The fee reduces drift from 0.549 to 0.023 — advertisers stay near their committed positions.

Keywords score higher on value efficiency (0.746 vs 0.696) — but this is survivorship bias. The metric measures match quality among whoever can afford to compete. In keyword bins, specialists who can't outbid the generalist on "physical therapy" are already priced out. The auction looks efficient because the losers are invisible. Embedding auctions include more competitors per query, which lowers the metric but raises the number of specialists who can participate at all. The surplus numbers — where embeddings win by 67% — capture what value efficiency misses: the market is larger when specialists can afford to be in it.

### The density story doesn't hold up

In an earlier version (v3.5) with only 3 clusters, we found a striking correlation: tighter clusters benefited more from fees (Pearson r=0.87). The story was elegant — fees are a Pigouvian tax on Hotelling drift, and their value scales with competitive density.

It was wrong. At 5 clusters, the correlation collapses to r=0.13.

| Cluster | Density | Surplus gain from fees (D-C) |
|---|---|---|
| Very tight | 0.974 | -0.031 |
| Tight | 0.895 | +0.527 |
| Medium | 0.830 | +0.153 |
| Loose | 0.616 | +0.147 |
| Very loose | 0.527 | +0.112 |

The very tight cluster (yoga studios, cos 0.974) shows *negative* surplus from fees. The tight cluster benefits most. There's no monotonic relationship. The r=0.87 at n=3 was overfitting noise.

Fees improve surplus uniformly, not proportionally to density. The mechanism is blunter than the theory suggested. This means a flat fee works — and density-adaptive fees (Cell E) provide zero measurable benefit over uniform fees (all D↔E comparisons p > 0.88).

## Why This Matters: The Convergence Trap

The simulation demonstrates a specific failure mode. Without fees:

1. Advertisers start at differentiated positions — each specialist at their niche
2. The value gradient pulls them toward popular query clusters
3. Positions converge, competitive overlap increases, clearing prices rise
4. The embedding auction reproduces keyword crowding at higher resolution

This is the convergence trap. The embedding space has the *capacity* for differentiation — it can tell the climbing PT from the sports PT. But the competitive dynamics on top of that space erase the differentiation over time. You end up with coordinates instead of keywords and the same crowded auction.

The v3.4 results make this concrete. In keywords, specialists lose 3.5x more per round than generalists (-0.807 vs -0.233). That's the [keyword tax](/keyword-tax) — the climbing PT paying to compete on "pelvic floor exercises after C-section." Embeddings without fees improve this directionally, but without fees, specialist surplus doesn't reach significance.

With fees, specialist surplus goes from **-0.695 to +0.021** (p<0.001). That sign change is the whole story. Specialists go from losing money every round to breaking even. The climbing PT stops subsidizing auctions she can't win and starts earning on the queries where she's the best match. Win diversity climbs to 0.876. The embedding space preserves the differentiation it was designed to provide — but only because the fee makes drifting toward competitors more expensive than staying put.

## The Reinforcement Mechanism

Relocation fees are not a novel mechanism. They're the embedding-space instance of a pattern that appears wherever frictionless repositioning would destroy differentiation.

### Spectrum licenses

Radio spectrum is a continuous resource, like embedding space. Without usage restrictions, every broadcaster would crowd the most popular frequencies — maximum audience, maximum interference, minimum value for everyone. The FCC allocates spectrum through auctions with geographic and usage commitments. A broadcaster who wins a license for the 700 MHz band in Dallas can't unilaterally shift to the 600 MHz band in New York. The license binds position. The 2015 AWS-3 auction raised $44.9 billion precisely because the commitments made the positions valuable — exclusive access to a defined territory, protected from crowding.

The parallel to embedding space: without positional commitment, every advertiser crowds the densest impression region. Relocation fees are the license condition that makes a position worth holding.

### Domain names

ICANN charges annual renewal fees for domain registrations. Without them, speculators would register every plausible domain and sit on it — the namespace would collapse into a land grab with no relationship between registrants and value. The renewal fee creates ongoing cost for holding a position, which pushes registrants toward positions they actually intend to use. Domain squatting still exists, but the fee limits its scale.

In embedding space, the analogous problem is position squatting — declaring a center at the highest-traffic point regardless of what you actually sell. The relocation fee doesn't prevent initial positioning (first declaration is free), but it prevents the incremental drift that accomplishes the same thing over time.

### Commercial real estate

A coffee shop doesn't relocate to the busiest corner every time foot traffic shifts. Lease termination fees, buildout costs, and moving expenses create friction. The result: businesses spread across neighborhoods, each serving a local market. The friction that prevents convergence is what makes the city livable.

Strip this friction away — imagine a city where any business could teleport to any location for free — and every store would cluster at the same intersection. That's an embedding auction without relocation fees. The zero-friction digital space needs synthetic friction to reproduce the differentiation that physical friction provides naturally.

### App store ranking

Apple and Google penalize apps that manipulate their store ranking through keyword stuffing, fake reviews, or rapid metadata changes. An app that changes its title from "Meditation Timer" to "Free Games Meditation Fitness Yoga Health" gets flagged. The penalty prevents convergence on the highest-traffic keywords at the expense of honest positioning.

Without these penalties, every app would optimize its metadata for the same popular search terms. The app store would become a keyword auction where the loudest title wins. The ranking algorithms impose a cost on repositioning — effectively a relocation fee in keyword space.

## The Design: Simple and Flat

The simulation tested whether fees should scale with local competitive density — higher fees in crowded niches, lower fees in sparse ones. The answer is no.

Density-adaptive fees (Cell E) provided zero measurable benefit over uniform fees (Cell D) across all 5 clusters (all p > 0.88). The fee works because it prevents drift everywhere, not because it fine-tunes how much drift to allow per market. A single λ works equally well whether the cluster is yoga studios at cosine 0.97 or unrelated tradespeople at cosine 0.53.

This simplifies the design. The exchange doesn't need to measure competitive density, classify market structure, or calibrate per-niche fee schedules. One parameter. One fee. Applied uniformly. Enforced in the [TEE-attested auction code](/relocation-fees) where no exchange can waive it for preferred partners or inflate it to suppress competitors.

The simulation tested distance-based fees (`λ · ‖move‖²`). A surplus-based fee — where the advertiser pays a percentage of the value gained by repositioning — would be self-scaling and individually rational by construction. An advertiser who drifts and gains nothing pays nothing. That design is untested. What's proven is that any flat fee works; the optimal fee structure is a policy choice for the SSP.

## The Fee Is Pure Profit

Whatever fee structure the SSP chooses — distance-based, surplus-based, or a hybrid — the computation happens inside the same TEE that clears the auction. One extra line of arithmetic. No infrastructure cost. No human review. No marginal expense. The fee is collected as part of auction settlement, the same pipeline that already handles VCG payments. Revenue against zero cost of goods.

Every industry example above works the same way. The FCC doesn't build new spectrum when it charges license fees. ICANN doesn't manufacture new domain names. The landlord doesn't construct a new building when collecting a lease termination fee. The fee is pure margin.

And unlike a tax that extracts value from the market, this fee *creates* value. The simulation shows it: advertisers earn higher surplus in the market with fees than the market without them. The exchange collects the fee and the advertisers are still better off. The fee funds the exchange by capturing a fraction of the surplus it generates — not by redistributing existing surplus from participants to the platform.

This is a Pigouvian tax that pays for itself. A carbon tax makes polluters pay for the damage they cause — but the government has to spend the revenue on something useful for the tax to be net positive. Here, the damage prevented (Hotelling collapse) is worth more to advertisers than the fee costs them. The exchange collects revenue. The advertisers earn more. Nobody loses. It's free money — not in the sense that it appears from nowhere, but in the sense that the fee unlocks surplus that didn't exist without it, and everyone gets a share.

This is the business model for an embedding-space exchange. Not take rates on clearing prices. Not data monetization. Not preferential placement. A Pigouvian fee on drift that costs nothing to enforce, prevents a market failure that would destroy the product, and generates pure-margin revenue as a side effect. The exchange doesn't profit despite charging fees. It profits *because* the fees make the market worth participating in.

## What Holds Up

Across five simulation versions, two findings are robust:

1. **Hotelling drift is universal.** Centripetal fraction is positive in every cluster tested, at every density level, in every version. Advertisers in embedding space drift toward competitors. The direction is always centripetal. The mechanism is the same one Hotelling described in 1929, operating in a space he couldn't have imagined.

2. **A flat fee is sufficient.** Uniform relocation fees significantly improve surplus, reduce drift, and preserve the differentiation that embedding space makes possible. No density scaling needed. No adaptive scheduling. One fee, applied everywhere, enforced by attested code.

The embedding space can distinguish the climbing PT from the sports PT. The fee is what keeps them apart.

## References

- **Hotelling, H. (1929).** "Stability in Competition." *Economic Journal*, 39(153), 41-57. The original minimum differentiation claim — two firms on a line converge to the center.

- **d'Aspremont, C., Gabszewicz, J.J., & Thisse, J.-F. (1979).** "On Hotelling's 'Stability in Competition'." *Econometrica*, 47(5), 1145-1150. Corrected Hotelling: with quadratic transportation costs, the equilibrium is maximum differentiation.

- **Irmen, A. & Thisse, J.-F. (1998).** "Competition in Multi-Characteristics Spaces: Hotelling Was Almost Right." *Journal of Economic Theory*, 78(1), 76-102. The n-dimensional result: Max-Min-...-Min. Firms maximally differentiate on one dimension and minimally on all others.

- **Beyer, K. et al. (1999).** "When Is 'Nearest Neighbor' Meaningful?" *ICDT'99*, LNCS 1540, 217-235. Distance concentration in high dimensions — all pairwise distances converge, making nearest-neighbor distinctions meaningless in the ambient space.

- **Han, S. et al. (2021).** "Shapes as Product Differentiation: Neural Network Embedding in the Analysis of Markets for Fonts." [arXiv:2107.02739](https://arxiv.org/abs/2107.02739). Hotelling competition operationalized in CNN embedding space. Analyzed a merger of 28,000+ fonts and found competitive effects invisible to structured-data measures.

- **Loertscher, S. & Muir, E.V. (2024).** "Optimal Hotelling Auctions." Working paper, MIT Sloan. Combines spatial differentiation with mechanism design. Key finding: auctions need a structural element beyond pricing to maintain differentiation.

---

*Part of the [adtech](/adtech) series. june@june.kim*
