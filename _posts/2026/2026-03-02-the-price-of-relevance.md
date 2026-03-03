---
layout: post
title: "The Price of Relevance"
tags: vector-space
---

Every ad auction has to decide how much to weight relevance versus price. Weight relevance too little and users see irrelevant ads. Weight it too much and the platform loses revenue. In keyword auctions, this tradeoff is controlled by a single number — the squashing parameter `s` — and twenty years of research has gone into understanding it.

[Embedding auctions](/power-diagrams-ad-auctions) have the same tradeoff, but it's been hiding in the formula. The scoring rule `score = log_b(price) - dist²/σ²` ranks advertisers by a combination of price and proximity, where `dist` is the distance to the query, `σ` is the advertiser's targeting radius, and `b` is the log base. That log base is the squashing parameter: `s = ln(b)`. Change `b` from `e` to `10` and an advertiser needs 10× the price to overcome one unit of distance penalty instead of 2.72×. Change it to `50` and proximity is everything.

Lahaie and Pennock (2007) formalized the keyword version as `score = bid × relevance^s` and showed that tuning `s` matters more than setting reserve prices. The mapping `s = ln(b)` means every finding about `s` in keyword auctions transfers directly to embedding auctions. We swept it from `s = 0` (pure rank-by-bid) to `s = 3.91` (near-Voronoi) across 50 trials.

## The Derivation

Why does `s = ln(b)`? Rewrite the score: `log_b(price) = ln(price)/ln(b)`, so `score = ln(price)/ln(b) - dist²/σ²`. Define quality as `exp(-dist²/σ²)`. Then in log space the score is `ln(price)/ln(b) + ln(quality)`, and `ln(b)` is the weight on quality relative to price — which is exactly what `s` does in the keyword formula `bid × quality^s`.

| Log base b | 1/ln(b) | Equivalent s | Interpretation |
|------------|---------|--------------|----------------|
| 1.0 | ∞ | 0.00 | Pure rank-by-bid (distance ignored) |
| 1.1 | 10.5 | 0.10 | Very weak distance weight |
| 1.5 | 2.47 | 0.41 | Moderate — between rank-by-bid and industry default |
| 2 | 1.44 | 0.69 | Price has edge over distance |
| **e ≈ 2.72** | **1.00** | **1.00** | **Rank-by-revenue (industry default)** |
| 5 | 0.62 | 1.61 | Distance dominates |
| 10 | 0.43 | 2.30 | Strong territorial defense |
| 50 | 0.26 | 3.91 | Near-Voronoi |

At `b = 1`, distance is completely ignored — the auction ranks purely by price. Higher `b` means distance matters more. At `b = 50`, the auction approaches a Voronoi partition where the closest advertiser wins regardless of bid.

## What the Log Base Controls

Che (1993) showed that in multidimensional auctions, under-rewarding quality maximizes short-term revenue while over-rewarding it maximizes buyer surplus. For chatbot platforms, higher `b` is the natural direction — retention depends on answer quality, not ad revenue per query. The question is how much higher.

To overcome one unit of `dist²/σ²`:

- At `b = 1`: distance doesn't matter — highest bid wins
- At `b = e`: multiply price by 2.72×
- At `b = 10`: multiply price by 10×
- At `b = 50`: multiply price by 50×

A climbing physical therapist at cosine 0.95 to a climbing query is hard to outbid at `b = 10` — a generalist sports physical therapist at cosine 0.80 would need to pay 10× more per unit of distance disadvantage. At `b = e`, the generalist needs only 2.72×.

The platform has three levers: `b` (continuous weight on relevance), `τ` (hard relevance gate — minimum cosine to enter the auction), and `λ` ([drift penalty](/synthetic-friction) preventing position gaming). This experiment tests the first two.

## Experiment Design

The simulation models a local services market — physical therapists, fitness coaches, wellness professionals. 25 advertisers across 5 clusters in 384-dimensional BGE-small-en-v1.5 embedding space. Each cluster has one generalist and four specialists.

Key assumptions:

- **Specialists know their niche.** They target narrowly (σ=0.30) and convert well (max value 12.0). A knee physical therapist bidding on knee rehab queries gets high value; on generic fitness queries, almost none.
- **Generalists spread wide.** They target broadly (σ=0.55) with lower per-impression value (max value 6.0). A general sports physical therapist bids on everything sports-related but converts less on any specific query.
- **Value decays with distance.** An advertiser's value for a query is `max(0, MaxVal × (cos_sim - threshold))`. No advertiser bids on queries they can't convert on — this is the soft relevance gate that turns out to matter more than the hard one.
- **Positions are locked.** [Relocation fees](/synthetic-friction) (λ=5000) prevent drift. This experiment isolates the scoring rule by holding positions fixed.
- **VCG payments, not GSP.** Winners pay the externality they impose — the incentive-compatible mechanism. Lahaie and Pennock analyzed GSP in symmetric equilibrium; our results use VCG in dominant strategy. Revenue levels aren't directly comparable, but the directional tradeoffs should hold across both mechanisms.
- **Positive value-relevance correlation.** Specialists have both higher values and higher cosine similarity to their niche queries. This assumption matters: Vorobeychik (2009) found that when value-quality correlation is weak, lower `s` can dominate higher `s` on welfare. The monotonic tradeoff in our results depends on specialists being genuinely better at what they're close to. We sweep the full range from `b = 1` (s=0, pure rank-by-bid) through `b = 50` (s=3.91) — the same parameter space Lahaie and Pennock explored in keyword auctions.

Scoring: `log_b(price) - dist²/σ²`, implemented via sigma scaling (`σ/√ln(b)`) so the core auction library stays untouched. At `b = 1`, embeddings are removed entirely — the auction ranks by `log(price)` only. 300 rounds per trial, 50 trials per condition.

**Part A** sweeps the log base: `b ∈ {1.0, 1.1, 1.5, 2, e, 5, 10, 50}` with τ=0.3, covering `s ∈ [0, 3.91]`.

**Part B** sweeps the discovery threshold: `τ ∈ {0.0, 0.2, 0.3, 0.5, 0.7}` at b=50.

The simulation is [open source](https://github.com/kimjune01/openauction/tree/v3.5.1/cmd/simulate).

## Results

### Part A: Log Base Sweep

**Price-dominated regime (s < 1):**

| Metric | b=1.0 | b=1.1 | b=1.5 | b=2 | b=e |
|--------|-------|-------|-------|-----|-----|
| Value efficiency | 0.657\*\*\* | 0.664\*\* | 0.670 | 0.673 | 0.683 |
| Avg surplus/rnd/adv | 1.90\*\*\* | 1.96\*\*\* | 2.13\*\*\* | 2.27\*\* | 2.42 |
| Specialist surplus | 2.38\*\*\* | 2.45\*\*\* | 2.66\*\*\* | 2.83\*\* | 3.01 |
| Generalist surplus | -0.014\*\*\* | -0.012\*\*\* | 0.010 | 0.031 | 0.040 |
| Revenue/round | 90.0 | 90.8 | 90.6 | 89.9 | 89.6 |
| Winner cos_sim | — | 0.688\*\*\* | 0.691\* | 0.693 | 0.696 |

**Quality-dominated regime (s > 1):**

| Metric | b=e | b=5 | b=10 | b=50 |
|--------|-----|-----|------|------|
| Value efficiency | 0.683 | 0.692 | 0.700 | 0.737\*\*\* |
| Avg surplus/rnd/adv | 2.42 | 2.66\*\* | 2.84\*\*\* | 3.36\*\*\* |
| Specialist surplus | 3.01 | 3.31\*\* | 3.52\*\*\* | 4.15\*\*\* |
| Generalist surplus | 0.040 | 0.086 | 0.120\*\* | 0.202\*\*\* |
| Revenue/round | 89.6 | 87.8\* | 86.1\*\*\* | 82.9\*\*\* |
| Winner cos_sim | 0.696 | 0.700 | 0.703 | 0.712\*\*\* |

*Significance vs b=e baseline (Welch's t-test): \* p<0.05, \*\* p<0.01, \*\*\* p<0.001. No-show rate is 0% and win diversity is flat across all conditions. Winner cos_sim for b=1.0 is undefined (embeddings removed for pure price ranking).*

Higher `b` monotonically improves value efficiency, surplus, and winner relevance at the cost of publisher revenue.

Revenue is flat up to `b = e` (all within 1.3%, none significant), then drops: 2% at `b = 5`, 4% at `b = 10`, 7.5% at `b = 50`. Specialist surplus grows 75% from `b = 1.0` to `b = 50` (2.38 → 4.15). Generalists go *negative* at `b ≤ 1.1` — they systematically overpay when distance doesn't protect specialists' territories. Win diversity is flat across the range.

The stakeholders want opposite things. Advertisers want lower `b` — it lets them win impressions outside their niche by outbidding closer competitors. Users want higher `b` — it means the ad they see is actually relevant to what they asked. The platform sits in the middle. At `b = 5`, it buys 10% more surplus and 1.3% better value efficiency for a 2% revenue cost — a good trade. At `b = 10`, double the quality gain for double the revenue cost. The curve is smooth enough that the platform can pick its point.

### Part B: Discovery Threshold Sweep

| Metric | τ=0.0 | τ=0.2 | τ=0.3 | τ=0.5 | τ=0.7 |
|--------|-------|-------|-------|-------|-------|
| Value efficiency | 0.737 | 0.737 | 0.737 | 0.737 | **0.930** |
| Surplus | 3.36 | 3.36 | 3.36 | 3.36 | 1.87 |
| Revenue/round | 82.9 | 82.9 | 82.9 | 82.9 | **154.3** |
| Winner cos_sim | 0.712 | 0.712 | 0.712 | 0.712 | **0.797** |
| No-show rate | 0% | 0% | 0% | 0% | **22.1%** |
| Win diversity | 0.289 | 0.289 | 0.289 | 0.289 | **0.492** |

τ=0.0 through τ=0.5 produce **identical** results (p=1.000). The value decay function `max(0, MaxVal × (cos - threshold))` already acts as a soft relevance gate. Advertisers don't bid on queries where their expected value falls below 5% of their maximum. The hard threshold has nothing to filter because the soft gate already did the work.

Only τ=0.7 has any effect, and it's dramatic. Value efficiency jumps to 0.930. Winner cosine similarity climbs from 0.712 to 0.797. But 22.1% of queries get no ad at all — no advertiser clears the bar.

Revenue doubles at τ=0.7 despite fewer competitors. Fewer bidders should mean lower VCG payments, but the surviving bidders have much higher values for their winning queries (cosine 0.797 vs 0.712), so the individual rationality cap — payment ≤ value — binds at a higher level. The auction collects more per impression because each impression is worth more to whoever wins it.

## The Tradeoff

`b` (continuous weight) is the primary lever; `τ` (hard gate) is redundant until extreme values. This matches Asker and Cantillon's (2008) theoretical result that scoring auctions dominate mechanisms that combine price-only ranking with minimum quality thresholds. The continuous score subsumes the hard cutoff.

The discovery threshold matters only if the platform is willing to accept 22% no-shows. That's a product decision, not a scoring decision. For most chatbot deployments, showing no ad is acceptable — it's a conversation, not a search results page. If the best match is mediocre, say nothing. That argues for high `τ` as a quality floor. But the scoring formula with high `b` already achieves most of this effect without the binary cutoff.

In isolation, a revenue-maximizing platform would set `b` as low as possible. But platforms don't operate in isolation. A chatbot that shows irrelevant ads loses users to one that shows relevant ads. Gomes (2014) formalized this: in two-sided markets, user participation elasticity pushes the platform's optimal quality weight above the pure revenue-maximizer's choice. Competition between platforms pushes `b` up — the same way competition between advertisers pushes bids up. The floor on `b` isn't set by the platform's own revenue curve, it's set by the `b` of the next-best alternative.

Recommended ranges:
- **Balanced:** `b = 5`, `τ = 0`. Best quality-per-revenue-dollar on the curve.
- **Revenue maximization:** `b = 2` or lower, `τ = 0`. Revenue is flat below `b = e`, so any low value works — if you can afford the user experience.
- **Quality absolutist:** `b = 50`, `τ = 0.7`. Maximum relevance, accept the no-shows.

## What's Still Open

**Should noisy relevance estimates push `b` lower?** Lahaie and McAfee (2011) showed that when quality estimates are noisy, `s < 1` can improve welfare by reducing weight on unreliable signals. Cosine similarity in embedding space is a noisy proxy for true relevance — an advertiser at cosine 0.85 isn't reliably better than one at 0.82. Our simulation assumes perfect cosine-to-value mapping. With noisy estimates, the optimal `b` might be lower than what the clean tradeoff curve suggests.

**Does the optimal `b` depend on market density?** With 25 advertisers across 5 clusters, the tradeoff is clean. With 250 advertisers — or 5 — the shape of the curve might change. More competitors could shift the efficient frontier, making higher `b` less costly in revenue terms.

**How does `b` interact with σ adaptation?** In our simulation, σ values are fixed. In a live market, advertisers learn their optimal σ — and the optimal σ depends on `b`. At high `b`, a narrower σ is more valuable because proximity matters more. This creates a feedback loop: `b` shapes σ, which shapes clearing prices, which shifts the revenue-quality curve.

**Is there a dynamic `b` that adjusts per query?** A query with 12 qualified advertisers could use lower `b` (more price competition). A query with 2 could use higher `b` (protect the closer match). Variable `b` would complicate the mechanism's transparency — the [attested auction](/perplexity-was-right-to-kill-ads) would need to commit to the adjustment rule, not just the scoring formula.

**The log form gives diminishing returns on price.** Going from $1 to $10 has the same effect as $10 to $100. No major platform uses explicit `log(price)` — they use multiplicative quality scores that achieve a similar compression. Whether the log form is an advantage (prevents runaway bidding) or a limitation (suppresses price signal) depends on market structure.

## References

- **Lahaie, S. & Pennock, D.M. (2007).** "Revenue Analysis of a Family of Ranking Rules for Keyword Auctions." *EC'07*, 50-56. Parameterized ranking rules as `score = bid × relevance^s`, showed the revenue-optimal `s` depends on value-relevance correlation.

- **Lahaie, S. & McAfee, R.P. (2011).** "Efficient Ranking in Sponsored Search." *WINE'11*, LNCS 7090, 227-238. When quality estimates are noisy, `s < 1` improves expected welfare by reducing weight on unreliable signals.

- **Che, Y.-K. (1993).** "Design Competition through Multidimensional Auctions." *RAND Journal of Economics*, 24(4), 668-680. Optimal scoring rule depends on buyer's objectives — under-rewarding quality maximizes revenue, over-rewarding maximizes surplus.

- **Asker, J. & Cantillon, E. (2008).** "Properties of Scoring Auctions." *RAND Journal of Economics*, 39(1), 69-85. Scoring auctions dominate price-only auctions with minimum quality thresholds.

- **Vorobeychik, Y. (2009).** "Simulation-Based Analysis of Keyword Auctions." *SIGecom Exchanges*, 8(1). When value-quality correlation is weak, `s < 1` can dominate `s = 1` on welfare.

- **Gomes, R. (2014).** "Optimal Auction Design in Two-Sided Markets." *RAND Journal of Economics*, 45(2), 248-272. User participation elasticity pushes the platform's optimal quality weight above the pure revenue-maximizer's choice.

- **Simulation source:** [openauction v3.5.1](https://github.com/kimjune01/openauction/tree/v3.5.1/cmd/simulate)

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument and designed the experiments; Claude built the simulation, researched prior art, and drafted prose.*

*Part of the [Vector Space](/vector-space) series. june@june.kim*
