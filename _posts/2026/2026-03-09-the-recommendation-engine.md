---
layout: post
title: "The Recommendation Engine"
tags: vector-space
---

Every ad metric is a proxy for the thing advertisers actually care about: did someone buy?

CPM is a race to the bottom. Impressions are [inflated with bot traffic and MFA slop](/receipts-please). CPC is gamed. Click farms, accidental taps, [Honey-style cookie hijacking](/adtech-from-1887). Both metrics force advertisers to guess: multiply margin by some estimated conversion probability, shade for uncertainty, hope the math works out. It never does, because the proxy is too far from the signal.

With [cryptographic coupons](/croupier) issued at publisher-time and redeemed at conversion, the proxy disappears. What's left is the thing itself.

## PPR: Pay Per Redemption

A coupon rides with the ad. The customer carries it to checkout. The advertiser's endpoint [verifies the signature](/not-worth-the-squeeze). If valid, log the redemption. If not, discard.

The advertiser pays only for verified redemptions. Impressions and clicks are someone else's problem.

| Metric | What you pay for | What you actually want | Gap |
|---|---|---|---|
| CPM | 1,000 eyeballs (maybe bots) | Customers | Enormous |
| CPC | A click (maybe accidental) | Customers | Large |
| **PPR** | A verified redemption | Customers | **Zero** |

CPA looks similar but differs in one way that matters. CPA relies on the ad platform self-reporting conversions through its own pixel. The platform that sells the ad also grades its own homework. PPR is cryptographically attested by the advertiser's own key. No intermediary claims credit. The receipt is the proof.

The advertiser defines what "redemption" means. A checkout. A booking. A signed contract. A free trial activation. The exchange only sees that a signed coupon came back. A yoga studio counts a first class attended. A SaaS company counts a paid subscription. A restaurant counts a seated reservation. Same protocol, different thresholds, each set by the business that knows its own funnel.

## Honest Bidding

In the current system, an advertiser's bid is a compound guess:

```
bid = margin × P(conversion) × P(click) × discount_for_uncertainty
```

Each term is noisy. Conversion probability varies by publisher, by time of day, by creative. Click probability is gamed. The uncertainty discount is loss aversion dressed up as strategy. The bid lands somewhere in the neighborhood of the truth, minus a fear tax.

PPR collapses the advertiser's side of the equation:

```
declared bid = margin
```

The advertiser states what a conversion is worth to them. In a [VCG auction](/one-shot-bidding), truthful reporting is dominant for risk-neutral bidders: you never overpay because you pay the externality, not your bid. You never underbid because shading can only lose you profitable auctions.

A caveat: small businesses are risk-averse. [Hu, Shin & Tang (2016)](https://pubsonline.informs.org/doi/10.1287/mnsc.2015.2223) showed that risk-averse advertisers shade below their true value even under CPA models. A climbing gym owner who'd profit at $30 per new member might bid $22 because the variance hurts. The VCG truthfulness result weakens when the bidder fears the downside more than they value the upside. But the compound guess still collapses. Instead of four noisy terms, it's one honest term with a risk discount. That's progress.

The auction still needs conversion probability. It just moves to the exchange's side of the ledger. The effective score becomes:

```
score = log(margin × P_est(conv)) - d² / σ²
```

The advertiser declares margin. The exchange estimates `P_est(conv)` from observed redemption data across that advertiser's campaigns. A new advertiser starts with a prior based on their vertical's average. As redemptions come in, the estimate updates. An advertiser who bids high and never redeems, trying to freeload on brand impressions, sees `P_est` drop toward zero. Their effective score collapses and they lose territory. The mechanism is self-correcting: you can't occupy space you don't convert in.

This looks like [Quality Score](https://support.google.com/google-ads/answer/6167118), and structurally it is. Google's Ad Rank is `bid × P_est(click)`. This is `margin × P_est(conv)`. Same pattern. The difference is auditability. Google's Quality Score is a black box: a neural net whose inputs and weights are opaque, controlled by the same company that profits from manipulating it. This `P_est` is a count ratio: coupons relayed divided by coupons redeemed. The [croupier](/croupier) counts envelopes. The advertiser counts redemptions at their own endpoint. The publisher counts distributions. Every redemption carries a [counter-signature](/croupier) proving the exchange facilitated the match, a cryptographic event that all three parties independently observe. If the exchange claims `P_est = 2%` but the advertiser redeemed 5% of issued coupons, the discrepancy is visible. No model to audit. Just division.

This also means the exchange is performance-only. An advertiser who wants brand awareness without conversions has no place in this auction. Their `P_est` would be zero, and zero times any margin is zero. CPM networks exist for brand campaigns. This is a recommendation engine, not a billboard.

## Set It and Forget It

In the current [power-diagram auction](/power-diagrams-ad-auctions), advertisers declare [three numbers](/one-shot-bidding): center, sigma, and bid. The bid is the hard part. Guessing `margin × P(conversion)` requires knowing your conversion rate, which requires running ads, which requires a bid. Circular.

PPR breaks the circle. The bid is just margin. But it does something else: it makes sigma tunable by the exchange.

Previously, sigma (how broad or narrow the advertiser's reach should be) was the advertiser's responsibility. A climbing gym that sets sigma too wide wastes money on irrelevant impressions. Too narrow, and they miss customers who would have converted. The advertiser had to guess.

With PPR, the exchange observes redemption rates at different distances from the advertiser's center. It can estimate the [Gaussian decay curve](https://en.wikipedia.org/wiki/Radial_basis_function_kernel), the rate at which conversion probability drops with distance in embedding space. That curve *is* sigma. The exchange learns it from data the advertiser never had to provide.

The advertiser's job reduces to two things: describe your ideal customer (center) and state your margin (bid). The exchange handles the geometry. The advertiser can still override sigma if they want. Maybe they know their niche better than the data shows yet. But the default is automatic, and the default improves as the exchange sees more redemptions.

[One-shot bidding](/one-shot-bidding) becomes zero-shot tuning. Describe what you do, say what it's worth, and the mechanism figures out the rest.

## The Insurance Company

Here's where it gets interesting.

A small business running ads faces a cold-start problem. They don't know their conversion rate yet. They're spending real money on uncertain outcomes. This is measurable. [Lewis & Rao (2015)](https://doi.org/10.1093/qje/qjv023) ran 25 large-scale randomized experiments with $2.8M in ad spend and found that the median confidence interval on ROI exceeds 100%. An advertiser literally cannot tell if their campaign is profitable. Even the most sophisticated measurement can't close the gap at small scale.

[Loss aversion](https://en.wikipedia.org/wiki/Loss_aversion) under these conditions is rational. Google's own data shows [62% of small businesses abandon Google Ads](https://research.google.com/pubs/prediction-of-advertiser-churn-for-google-adwords/), with over half lapsing within three months. [Killeen (2025)](https://gkilleen33.github.io/papers/working/Killeen-JMP.pdf) ran field experiments with 1,200 Kenyan retail firms and found that offering an insurance contract (same expected value, lower variance) increased new product adoption by 50%. The effect concentrated among owners with higher personal risk aversion. Firms avoid profitable-in-expectation investments because the variance is too high relative to what they can afford to lose.

Individually, this is a dead end. The advertiser leaves money on the table. The publisher loses a buyer. The exchange loses volume.

In aggregate, it's an insurance problem.

The exchange sees thousands of advertiser-publisher pairs. Some convert at 12%. Some at 0.3%. The variance is high per pair but [predictable across the portfolio](https://en.wikipedia.org/wiki/Law_of_large_numbers). The exchange takes on the conversion risk: pay the publisher upfront, collect from the advertiser only on redemption. The exchange becomes an underwriter.

| Role | Insurance analog |
|---|---|
| Advertiser | Policyholder (pays premium on conversion) |
| Publisher | Beneficiary (gets paid for distribution) |
| Exchange | Insurer (pools risk across the book) |
| Conversion rate | Loss ratio |

The exchange's margin is the spread between what it pays publishers for distribution and what it collects from advertisers on redemption. That margin depends on two things:

**Publisher quality.** A niche podcast that converts at 8% is a low-risk policy. An MFA content farm at 0.01% is a high-risk one. The exchange's [τ threshold](/three-levers) is its underwriting standard. Admit quality publishers, the book stays profitable. Let in junk, the losses mount. The [leaderboard](/croupier) is the actuarial table.

**Advertiser quality.** An advertiser with a smooth checkout flow and a product people want converts easily. One with a broken funnel doesn't. Admitting advertisers who actually convert is the other half of underwriting. The exchange is incentivized to screen for quality on both sides.

This is the opposite of Google's incentive. Google makes money on volume: more impressions, more clicks, more revenue, regardless of quality. The insurer makes money on quality: better conversion rates mean lower payouts relative to premiums. [Aligned greed](/aligned-greed).

## The Friction Is the Feature

Onboarding gets harder. The exchange needs to verify that advertisers have real margins, real products, and real conversion endpoints. Publishers need to demonstrate real audiences with real engagement. No self-serve portal. No credit card and five minutes.

Good. The friction is the underwriting.

Every insurance company that tried to skip underwriting went bankrupt. Every ad network that skipped quality control became a [market for lemons](/receipts-please). The friction filters for quality, and quality is the product.

The advertisers who survive onboarding get something no current platform offers: an auction where they state their actual margin, pay only for verified conversions, and let the mechanism handle allocation. No bid strategy. No ROAS target. No agency. No sigma tuning. Describe what you do, say what it's worth, done.

## Open Risks

The insurance analogy has known failure modes.

**Adverse selection.** [Edelman & Lee (2008)](https://www.hbs.edu/faculty/Pages/item.aspx?num=34975) showed that advertisers with low conversion rates self-select into CPA models because it shifts risk to the platform. Advertisers who convert well prefer CPC because it's cheaper for them. The exchange must underwrite against this: screen for funnel quality, set experience-rated pricing, or require minimum conversion history before admission. The onboarding friction is the underwriting that prevents the worst risks from entering the pool.

**Moral hazard.** [Agarwal, Athey & Yang (2009)](https://www.aeaweb.org/articles?id=10.1257/aer.99.2.441) identified that advertisers in pay-per-action auctions can underreport conversions. The cryptographic coupon mitigates publisher-side fraud (you can't fabricate a redemption without the advertiser's signing key) but the advertiser could choose not to verify valid coupons. If the advertiser's endpoint rejects real customers to avoid paying, their `P_est(conv)` drops, their territory shrinks, and they're paying the same margin for fewer impressions in a worse position. Suppressing redemptions to avoid payment is suppressing the signal that keeps you in the auction.

**Correlated risk.** The law of large numbers diversifies idiosyncratic variance: one campaign failing while another succeeds. It does not help when a recession drops conversion rates across every advertiser simultaneously. The exchange needs capital reserves for systematic risk, the same way insurers hold reserves for catastrophic events. The spread must price in tail risk, not just expected losses.

**Attestability.** Per-batch `P_est` is independently verifiable. The advertiser knows how many coupons they signed and how many they redeemed. The exchange committed the batch size in the Merkle tree. The aggregation could be opaque: the exchange combines batches across publishers and time windows using its own logic, and the advertiser can't verify the weighting. That's a trust surface.

The fix is a public ledger. Not per-impression (that's a [scaling problem](/not-worth-the-squeeze): CT handles 10 billion certificates; programmatic does hundreds of billions of impressions). Per-batch. An advertiser running 10 batches a month across 5 publishers produces 50 ledger entries. Each entry: batch ID, Merkle root, batch size, redemption count at settlement. `P_est` = redemptions / batch sizes over the last K entries, where K is published. Deterministic formula, public inputs, anyone can replay. The exchange can't fudge the score without contradicting the ledger. The croupier is blind at the relay layer. The ledger makes it transparent at the scoring layer. Two incorruptibility mechanisms for two trust surfaces. But this only works if it ships with the first embeddings exchange. [Transparency is irreversible](/transparency-is-irreversible): once users expect attestable scoring, every competitor either matches it or explains why they won't. If the first exchange launches opaque, opacity becomes the norm. The ledger is a design choice and a land grab.

These are real constraints, not fatal ones. Traditional insurance manages the same failure modes through underwriting, experience rating, and reserves. The ad exchange does the same, with the added advantage that cryptographic coupons make the raw data harder to fabricate.

## The Ceiling

How efficient can this get? Conversion probability decays with distance from the advertiser's center in embedding space. The natural model is [Gaussian decay](https://en.wikipedia.org/wiki/Radial_basis_function_kernel): `P(convert) = exp(-d² / 2σ²)`. Close to center, nearly every impression converts. Far away, nearly none do. A bell curve around the advertiser's ideal customer.

Why Gaussian? If you know two things about an advertiser's conversion curve (where it peaks and how wide it is) the Gaussian is the [maximum entropy](https://en.wikipedia.org/wiki/Maximum_entropy_probability_distribution) distribution: the least biased guess you can make. Anything else imports assumptions you don't have evidence for. It also happens to be the only model consistent with the auction's [scoring function](/power-diagrams-ad-auctions). The `d²` penalty in `score = log(bid) - d²/σ²` *is* the Gaussian, expressed in log-space. Not an approximation. An identity.

In practice, the curve is noisy, shaped by creative quality, landing page experience, seasonality, and a hundred other factors the auction can't observe. PPR doesn't eliminate that noise. It just stops penalizing advertisers for it. The advertiser absorbs conversion risk they can control (their own funnel) and offloads the risk they can't (publisher quality, audience composition) to the exchange.

The exchange, seeing thousands of campaigns, can estimate the Gaussian's parameters (center and bandwidth) better than any individual advertiser. [Bergemann & Bonatti (2024)](https://www.aeaweb.org/articles?id=10.1257/aer.20230478) showed that a platform's information advantage over conversion curves translates directly to market power. The question is what the platform does with it. Google uses it to [extract rents](https://www.bigtechontrial.com/p/google-knows-its-ad-exchange-isnt). An insurer uses it to improve matching. The better the exchange estimates conversion curves, the better it allocates, the lower its loss ratio, the more it earns. The incentive to improve the model is the incentive to serve better ads.

A recommendation engine that gets paid for being right.

---

*Part of the [Vector Space](/vector-space) series.*
