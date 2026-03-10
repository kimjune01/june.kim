---
layout: post
title: "Set It and Forget It"
tags: vector-space
---

In a [power-diagram auction](/power-diagrams-ad-auctions), advertisers declare [three numbers](/one-shot-bidding): center, sigma, and bid. The bid is the hard part. Guessing `margin × P(conversion)` requires knowing your conversion rate, which requires running ads, which requires a bid. Circular.

With verified conversions ([cryptographic coupons](/croupier)), the bid collapses to margin. The advertiser states what a conversion is worth. The exchange handles the rest.

But it does something else: it makes sigma tunable from data.

## The Guessing Game

Sigma controls how broad or narrow the advertiser's reach should be. A climbing gym that sets sigma too wide wastes money on irrelevant impressions. Too narrow, and they miss customers who would have converted. The advertiser has to guess how far their relevance extends in embedding space. Nobody knows that before running ads.

The data exists, after. The publisher reports aggregated distance histograms per batch: how many coupons were distributed at each distance bin from the advertiser's center. No individual embeddings, no timestamps, no point cloud to fingerprint. Just a histogram.

This isn't optional. [de Montjoye et al. (2013)](https://www.nature.com/articles/srep01376) showed that 4 spatio-temporal data points re-identify 95% of individuals in a 1.5 million person dataset. The FTC has [brought five enforcement actions](https://www.ftc.gov/business-guidance/blog/2022/07/location-health-and-other-sensitive-information-ftc-committed-fully-enforcing-law-against-illegal) against location data brokers since 2022 for claiming "anonymized" data that wasn't. [CMS requires](https://www.hhs.gov/guidance/document/cms-cell-suppression-policy) a minimum cell size of 11 before any count can be reported. [Google's own Ads Data Hub](https://developers.google.com/ads-data-hub/guides/privacy-checks) requires 50 users minimum per query. Individual embedding points are location data with extra dimensions. Histograms with minimum bin sizes satisfy these thresholds by design.

Pair the histograms with verified conversions ([cryptographic coupons](/croupier)), and the exchange observes conversion rates at different distances. It can estimate the [Gaussian decay curve](/power-diagrams-ad-auctions), the rate at which conversion probability drops with distance. That curve *is* sigma. The exchange learns it from data the advertiser never had to provide.

The advertiser can always override sigma. But the default is automatic, and the default improves with every conversion.

## The Control Loop

Sigma isn't estimated once. It's continuously adjusted. Conditions change: a competitor enters, a seasonal shift moves the audience, a new creative performs differently at the edges. A static sigma drifts out of calibration.

A [PID controller](https://en.wikipedia.org/wiki/PID_controller) on sigma keeps it tracking reality. The target is the conversion rate the advertiser's margin can sustain profitably. The error is the gap between observed and target conversion rates at the boundary.

- **Proportional**: if conversions at the current boundary are below target, sigma is too wide. Pull it in.
- **Integral**: if sigma has been slightly too wide for three weeks, the accumulated error forces a correction the proportional term alone wouldn't catch.
- **Derivative**: if conversions are dropping fast (a competitor just entered the adjacent territory), adjust now instead of waiting for the error to accumulate.

The same mechanism that keeps a thermostat from oscillating between freezing and boiling keeps sigma from oscillating between too broad and too narrow. Overshoot, correct, settle.

## The Upsell

The base product is three numbers and an auction. Set center, margin, and sigma. Run coupons. Count conversions.

The PID is an upsell. The exchange offers to tune sigma for a fee. The algorithm is public, the inputs (distance histograms, conversion counts) are on the [public ledger](/croupier), and the output (sigma) is deterministic given those inputs. Anyone can replay the computation. The exchange can't widen sigma beyond what the data justifies without contradicting the ledger. Same auditability pattern as [P_est](/croupier): deterministic formula, public inputs, verifiable by anyone.

The advertiser who wants control keeps it. The advertiser who wants convenience pays for it and audits anytime. The exchange earns a fee for a service it can prove is honest. [Aligned greed](/aligned-greed).

---

*Part of the [Vector Space](/vector-space) series.*
