---
layout: post
title: "Set It and Forget It"
image: "/assets/set-it-and-forget-it.jpg"
tags: vector-space
---

![Set It and Forget It](/assets/set-it-and-forget-it.jpg)

In a [power-diagram auction](/power-diagrams-ad-auctions), advertisers declare [three numbers](/one-shot-bidding): center, sigma, and bid. The bid is the hard part. Guessing `margin × P(conversion)` requires knowing your conversion rate, which requires running ads, which requires a bid. Circular.

With verified conversions ([cryptographic coupons](/croupier)), the bid collapses to margin. But verified conversions do something else. They make sigma tunable from data.

## The Guessing Game

Sigma controls how broad or narrow the advertiser's reach should be. A climbing gym that sets sigma too wide wastes money on irrelevant impressions. Set it too narrow and they miss customers who would have converted. The advertiser has to guess how far their relevance extends in embedding space. Nobody knows that before running ads.

The data exists, after. The publisher reports aggregated distance histograms: how many coupons were distributed at each distance bin from the advertiser's center. No individual embeddings, no timestamps, no point cloud to fingerprint. Just a histogram.

Pair the histograms with verified conversions, and the exchange observes conversion rates at different distances. It estimates the [Gaussian decay curve](/power-diagrams-ad-auctions). That curve *is* sigma. The exchange learns it from data the advertiser never had to provide.

Why histograms and not raw data? Because individual embedding points are location data with extra dimensions. [de Montjoye et al. (2013)](https://www.nature.com/articles/srep01376) showed that 4 spatio-temporal data points re-identify 95% of individuals in a 1.5 million person dataset. The FTC has [brought five enforcement actions](https://www.ftc.gov/business-guidance/blog/2022/07/location-health-and-other-sensitive-information-ftc-committed-fully-enforcing-law-against-illegal) against location data brokers since 2022 for claiming "anonymized" data that wasn't. [CMS requires](https://www.hhs.gov/guidance/document/cms-cell-suppression-policy) a minimum cell size of 11 before any count can be reported. [Google's own Ads Data Hub](https://developers.google.com/ads-data-hub/guides/privacy-checks) requires 50 users minimum per query. Histograms with minimum bin sizes satisfy these thresholds by design.

The advertiser can override sigma anytime. But the default improves with every conversion.

## The Control Loop

Sigma is continuously adjusted. Competitors enter. Seasons shift the audience. A new creative performs differently at the edges. A static sigma drifts out of calibration.

A [PID controller](https://en.wikipedia.org/wiki/PID_controller) keeps sigma tracking reality. The target is the conversion rate the advertiser's margin can sustain. The error is the gap between observed and target rates at the boundary.

- **Proportional**: conversions at the current boundary are below target. Sigma is too wide. Pull it in.
- **Integral**: sigma has been slightly too wide for three weeks. The accumulated error forces a correction the proportional term alone wouldn't catch.
- **Derivative**: conversions are dropping fast, say a competitor just entered the adjacent territory. Adjust now instead of waiting for the error to accumulate.

Overshoot, correct, settle.

## The Upsell

The exchange offers to tune sigma for a fee. The algorithm is public, the inputs (distance histograms, conversion counts) are on the [public ledger](/croupier), and the output is deterministic. Anyone can replay the computation. The exchange can't widen sigma beyond what the data justifies without contradicting the ledger.

The advertiser who wants control keeps it. The advertiser who wants convenience pays for it and audits anytime. [Aligned greed](/aligned-greed).

That's the advertiser's side. The publisher has the same problem in reverse.

## The Other Dial

The advertiser's dial is sigma. The publisher's is [τ](/three-levers).

The publisher doesn't set τ directly. They set a percentage: "10% of conversations should include a recommendation." Their server adjusts τ to hit that target. This loop runs on the publisher's own infrastructure.

The unit matters. A conversation is a series of turns, not a single exchange. The publisher's target is per-conversation, not per-turn. Twelve turns, one suggestion. That's the difference between a helpful nudge and a spam cannon.

A second PID controller manages it:

- **Proportional**: 14% of conversations are getting recommendations against a 10% target. τ is too loose. Tighten it.
- **Integral**: the rate has been 12% for two weeks. Seasonal drift, maybe more commercial queries in December. The accumulated error pulls τ in.
- **Derivative**: a new advertiser category just entered the auction. Recommendation rate is climbing fast. Adjust before users notice.

Tighten, loosen, settle.

The publisher who wants 5% sets 5%. The publisher who wants 20% sets 20%. τ finds the distance threshold that delivers it.

Each side gets one dial. Each dial tunes itself. Set it and forget it.

---

*Part of the [Vector Space](/vector-space) series.*
