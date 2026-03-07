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

A climbing physical therapist sets σ tight: only queries about climbing injuries and finger pulley rehab. A general sports PT sets σ wide — anything sports-related is worth a bid.

The scoring function already rewards accurate positioning: an advertiser closer to the query wins, all else equal. σ controls *how much* of the space around that position they're willing to serve. Tight σ scores high near the center but falls off fast; a wide σ trades peak score for breadth.

## τ Is the Publisher's Lever

Before bids are considered, the publisher applies a relevance threshold τ. Only ads whose distance to the content falls below τ enter the auction. This is a UX decision. The publisher is saying "ads on my site must be at least *this* relevant."

τ is a knob, tuned by directional feedback. Tighten it if users are bouncing; loosen it if fill rates are too low.

[Hartline, Hoy & Taggart (2023)](https://arxiv.org/abs/2310.03702) prove that competitive efficiency is closed under reserve pricing. τ has zero auction cost.

τ is zoning. The publisher decides what's allowed in the neighborhood.

## log(b) Is the Platform's Lever

Why compress bids logarithmically instead of using raw price?

Consider a publisher who sets τ = ∞. No relevance gate at all. Without log compression, the auction becomes highest-bidder-wins. A $100 bid stomps a $7 bid regardless of fit.

Log compression caps that. With log scoring:

- log(100) − log(7) ≈ 2.66
- log(7) − log(2) ≈ 1.25

The $100 bidder gets a 2.66-unit head start over the $7 bidder. The distance term `||x − c||² / σ²` easily swings by 3–5 units between a well-matched ad and a mediocre one. Distance still decides most auctions, even with no τ.

Each lever reshapes the [power diagram](/2026/02/04/power-diagrams-ad-auctions) differently: σ stretches individual cells, τ clips them at a radius, log(b) shifts boundaries with diminishing returns.

## Information Asymmetry

Advertisers publish their embeddings. Users and publishers don't.

**Advertiser embeddings are public.** "I want people interested in marathon training" is a storefront sign. Advertisers can see each other's positions, like seeing what shelf space a competitor occupies.

**Publisher and user embeddings are private.** The auction runs inside the publisher's domain or a trusted execution environment. Advertisers learn only whether their ad passed and at what price. The publisher can verify the auction because all advertiser embeddings are public inputs. The user's query never leaves the gate.

Advertisers learn where demand is indirectly, through performance feedback, the way a store learns from foot traffic.

## Platform Competition Does the Rest

Who forces the platform to serve the user's interests?

For LLM platforms, the answer is competition. Switching from ChatGPT to Claude to Perplexity costs nothing — there's no data lock-in and no switching penalty. If a platform over-serves ads or lets irrelevant ones through, users leave.

Perplexity already demonstrated this: total ad revenue came in at $20,000 against $34 million in subscriptions. They killed the ad program. The market revealed that for their users, ad-free was worth paying for, and ads weren't worth the churn risk.

Getting τ wrong is fatal: the platform that shows irrelevant ads loses users to one that gets it right. Competition audits the levers continuously.

---

*Part of the [Vector Space](/vector-space) series.*
