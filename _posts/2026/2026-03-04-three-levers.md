---
layout: post
title: "Three Levers"
tags: vector-space
image: "/assets/tau_and_log_b.jpg"
---

![L2 sphere and L-infinity cube](/assets/tau_and_log_b.jpg)

The [scoring function](/2026/02/04/power-diagrams-ad-auctions) has three parameters:

```
score_i(x) = log(b_i) - ||x - c_i||² / σ_i²
```

| Lever | Player | What it does | Protects against |
|-------|--------|-------------|-----------------|
| σ | Advertiser | Controls reach vs precision | Wasting budget on irrelevant impressions |
| τ | Publisher | Sets relevance floor | Showing bad ads to users |
| log(b) | Platform | Compresses bid advantage | Publishers who skip τ and just maximize revenue |

## σ Is the Advertiser's Lever

A climbing physical therapist sets σ tight: only queries about climbing injuries, rehab for finger pulleys, bouldering recovery. A general sports PT sets σ wide. Anything sports-related is worth a bid.

The scoring function already rewards accurate positioning: an advertiser closer to the query wins, all else equal. σ controls *how much* of the space around that position they're willing to serve. Tight σ means high scores near the center but rapid falloff. Wide σ means moderate scores across a broad region.

## τ Is the Publisher's Lever

Before bids are considered, the publisher applies a relevance threshold τ. Only ads whose distance to the content falls below τ enter the auction. This is a UX decision. The publisher is saying "ads on my site must be at least *this* relevant."

τ doesn't require a value function. It's a knob. Tighten it if users are bouncing. Loosen it if fill rates are too low. Directional feedback.

[Hartline, Hoy & Taggart (2023)](https://arxiv.org/abs/2310.03702) prove that competitive efficiency is closed under reserve pricing. τ has zero auction cost.

τ is zoning. The publisher decides what's allowed in the neighborhood.

## log(b) Is the Platform's Lever

Why compress bids logarithmically instead of using raw price?

Consider a publisher who sets τ = ∞. No relevance gate at all. Without log compression, the auction becomes highest-bidder-wins. A $100 bid stomps a $7 bid regardless of fit.

Log compression caps that. With log scoring:

- log(100) − log(7) ≈ 2.66
- log(7) − log(2) ≈ 1.25

The $100 bidder doesn't get a 14× advantage over the $7 bidder — they get a 2.66-unit head start. The distance term `||x − c||² / σ²` easily swings by 3–5 units between a well-matched ad and a mediocre one. Distance still decides most auctions, even with no τ.

Even when τ is slack, the scoring function doesn't degenerate into a pure price auction.

Each lever reshapes the [power diagram](/2026/02/04/power-diagrams-ad-auctions) differently: σ stretches individual cells, τ clips them at a radius, log(b) shifts boundaries with diminishing returns.

## Information Asymmetry

Advertisers publish their embeddings. Users and publishers don't.

**Advertiser embeddings are public.** "I want people interested in marathon training" is a storefront sign. There's no reason to hide it. Advertisers can see each other's positions, like seeing what shelf space a competitor occupies.

**Publisher and user embeddings are private.** The publisher's content and the user's query stay behind the relevance gate. The auction runs inside the publisher's domain or a trusted execution environment. Advertisers never see the content embedding — they only learn whether their ad passed or didn't, and at what price.

The publisher has enough information to verify the auction (all advertiser embeddings are public inputs). The advertiser has enough information to compete (they see competitor positions and their own win rates). The user's query never leaves the gate.

Advertisers can't strategically shift toward high-traffic regions because they don't know where those are. They learn indirectly through performance feedback, the way a store learns from foot traffic.

## Platform Competition Does the Rest

Who forces the platform to serve the user's interests?

For LLM platforms, the answer is competition. Switching from ChatGPT to Claude to Perplexity costs nothing. There's no data lock-in, no social graph, no app ecosystem. If a platform over-serves ads or lets irrelevant ones through, users leave.

Perplexity already demonstrated this: total ad revenue came in at $20,000 against $34 million in subscriptions. They killed the ad program. The market revealed that for their users, ad-free was worth paying for, and ads weren't worth the churn risk.

Getting τ wrong is fatal: the platform that shows irrelevant ads loses users to one that doesn't. Competition audits the levers better than regulation could.

---

*Part of the [Vector Space](/vector-space) series.*
