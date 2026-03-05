---
layout: post
title: "τ and log(b)"
tags: vector-space
image: "/assets/tau_and_log_b.jpg"
---

![L2 sphere and L-infinity cube](/assets/tau_and_log_b.jpg)

The [power diagram scoring function](/2026/02/04/power-diagrams-ad-auctions) combines two terms:

```
score_i(x) = log(b_i) - ||x - c_i||² / σ_i²
```

`log(b_i)` is the auction's concern — what the advertiser will pay. The distance term is the relevance concern — how well the ad fits the content. Combining them into a single score forces a tradeoff between relevance and revenue at every impression.

That tradeoff shouldn't be the auction's job. Split them. Run two phases, controlled by different parties.

## Phase 1: The Publisher Sets τ

Before any bids are considered, the publisher applies a relevance threshold τ. Only ads whose distance to the content falls below τ pass through. This is a UX decision, not an economic one — the publisher is saying "ads on my site must be at least *this* relevant."

## Phase 2: The Auction Ranks by log(b)

Among the ads that passed the relevance gate, the auction runs on bids. Standard second-price mechanics, clean incentives, no relevance considerations.

## No Value Function Required

The publisher can't quantify their users' value function — nobody can. The mapping from ad relevance to engagement, trust, and willingness to return is noisy, delayed, and confounded by everything else on the page.

But τ doesn't require a value function. It's a knob. Tighten it if users are bouncing. Loosen it if fill rates are too low. Directional feedback, not optimization.

The auction never trades off relevance against revenue — that tension is already resolved. The publisher protects UX independently. The auction maximizes revenue within whatever inventory the publisher approved.

τ is zoning. log(b) is the market.

## The Geometry of τ

The threshold τ defines an admission region around the publisher's content embedding. The shape of that region depends on which distance metric the publisher uses — and in 384 dimensions, the choice of metric changes everything.

The Lp norm family gives a spectrum of options. For two points in d-dimensional space:

```
Lp distance = (Σ |x_i - c_i|^p)^(1/p)
```

- **p = 2 (Euclidean):** the admission region is a hypersphere. An ad passes if it's close *on average* across all dimensions. A few bad dimensions get diluted by many good ones.
- **p = ∞ (Chebyshev):** the admission region is a hypercube. An ad passes only if *no single dimension* exceeds τ. One bad dimension kills it.
- **1 < p < ∞:** a smooth interpolation between the two.

In low dimensions, these are similar shapes. In 384 dimensions — the embedding space of models like BGE-small — they diverge dramatically.

The volume of a unit L2 ball collapses toward zero as dimension grows (it peaks around d=5, then shrinks). The volume of a unit L∞ ball stays at 1. The corners of the hypercube extend √d ≈ 19.6 times further from the center than the face centers. An L2 threshold and an L∞ threshold with the same radius admit different ads.

Two different UX philosophies:

- **L2 (sphere):** "be good on average"
- **L∞ (cube):** "don't be terrible on anything"

An intermediate p — say p = 4 or p = 8 — penalizes outlier dimensions more aggressively than L2 without discarding all other information like L∞ does. The publisher's choice of p is another lever, independent of τ itself.

## Information Asymmetry

Advertisers publish their embeddings. Users and publishers don't.

**Advertiser embeddings are public.** "I want people interested in marathon training" is a storefront sign. There's no reason to hide it. Advertisers can see each other's positions — normal competitive transparency, like seeing what shelf space a competitor occupies.

**Publisher and user embeddings are private.** The publisher's content and the user's query stay behind the relevance gate. The auction runs inside the publisher's domain or a trusted execution environment. Advertisers never see the content embedding — they only learn whether their ad passed or didn't, and at what price.

This asymmetry is clean. The publisher has enough information to verify the auction (all advertiser embeddings are public inputs). The advertiser has enough information to compete (they see competitor positions and their own win rates). The user's query never leaves the gate.

Advertisers can't strategically shift toward high-traffic regions because they don't know where those are. They learn indirectly through performance feedback — the same way a store learns from foot traffic, not from a map of every pedestrian's route.

## Platform Competition Does the Rest

Who forces the platform to serve the user's interests?

For LLM platforms, the answer is competition. Switching from ChatGPT to Claude to Perplexity costs nothing. There's no data lock-in, no social graph, no app ecosystem. If a platform over-serves ads or lets irrelevant ones through, users leave.

Perplexity already demonstrated this — total ad revenue came in at $20,000 against $34 million in subscriptions. They killed the ad program. The market revealed that for their users, ad-free was worth paying for, and ads weren't worth the churn risk.

The platform's own relevance threshold is a proxy for user preferences. Getting it wrong is fatal: the platform that shows irrelevant ads loses users to one that doesn't.

This is a stronger guarantee than regulation. It means the two-phase structure doesn't require anyone to audit the platform's τ. Competitive pressure keeps it honest.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
