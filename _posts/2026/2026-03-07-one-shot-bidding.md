---
layout: post
title: "One-Shot Bidding"
tags: vector-space
---

You're at a used car auction. Heart racing. Should you bid early to signal confidence, or wait and snipe? Shade 10% below your number, or 20%? You rehearse three different strategies on the drive over.

Then the car ends up selling for a hundred bucks more than your cap. What else did you expect? With enough bidders who've done the same homework, the winning bid was guaranteed to converge to what the car is worth. All that strategy for nothing.

## That's Google Ads

An entire industry agonizes over bidding strategy. Target ROAS, manual CPC, bid adjustments by device and time of day. Google built Smart Bidding, Meta built Advantage+, and agencies built careers around managing them.

In a competitive market with enough advertisers, the winning bid converges to the advertiser's true value. Expected surplus approaches zero. Bidding complexity is pure friction.

## Manufactured

Google's Generalized Second-Price auction isn't [truthful](https://en.wikipedia.org/wiki/Strategyproofness). [Edelman, Ostrovsky & Schwarz (2007)](https://www.aeaweb.org/articles?id=10.1257/aer.97.1.242) proved that GSP has no dominant strategy. Your optimal bid depends on what everyone else bids, and you can't see their bids. First-price auctions, which Google [switched to in 2019](https://blog.google/products/admanager/simplifying-programmatic-first-price-auctions/) for display, aren't truthful either. You have to shade your bid below your true value, but by how much depends on the competition you can't observe.

Smart Bidding is the fake solution to the fake problem. Google dug the pothole and sells you wheel alignment. Advertisers can't leave because years of optimizations lock them in, huddled around the keyword fountain for a sip.

## Vickrey, 1961

[Vickrey (1961)](https://doi.org/10.2307/2977633) solved this sixty-five years ago. In a second-price sealed-bid auction, the dominant strategy is to bid your true value. You never overpay because you pay the second-highest bid. You never underbid because shading can only lose you auctions you would have won profitably. Honesty is optimal.

Clarke (1971) and Groves (1973) generalized this to multiple items: the VCG mechanism. Each winner pays the externality they impose on everyone else. Total value is maximized, truthful reporting is dominant, and the whole thing resolves in one pass.

It turns out, the allocation problem is a [linear program](https://en.wikipedia.org/wiki/Linear_programming). The LP dual gives the prices. [Lahaie & Lubin (2025)](https://arxiv.org/abs/2507.03252) show that even multi-item heterogeneous auctions with complex preferences reduce to iterative LP solves that converge to welfare-maximizing outcomes.

Contrast the computational cost:

| | VCG/LP | Autobidding |
|---|---|---|
| **Agents** | 0 | n, each running ML |
| **Rounds** | 1 | Thousands |
| **Convergence** | Guaranteed | Not guaranteed |
| **Strategy** | Truthful | Approximate |
| **Input** | Your value | Everyone's bids |

The computational waste is fixing a strategic complexity that nobody asked for.

## The Man Who Proved It

Sebastien Lahaie works at Google Research. His [2025 paper](https://arxiv.org/abs/2507.03252) with Benjamin Lubin proves that VCG outcomes can be computed via linear programming. Truthful multi-item auctions are tractable at scale. Google didn't use it.

## Three Numbers

In a [power-diagram auction](/power-diagrams-ad-auctions) with VCG payments, an advertiser declares three things:

1. **Center**: an embedding of who their customer is
2. **Sigma**: how broad or narrow their reach should be
3. **Bid**: what a conversion is worth to them

<iframe src="/assets/bid-demo.html" style="width:100%;max-width:620px;height:310px;border:none;display:block;margin:1.5em auto" loading="lazy"></iframe>

<!-- static fallback for RSS/no-JS -->
<noscript>
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:600px;width:100%;margin:1.5em auto;display:block">
  <defs>
    <linearGradient id="gA" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="gB" x1="1" x2="0" y1="0" y2="0">
      <stop offset="0%" stop-color="#f97316" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#f97316" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <!-- axis -->
  <line x1="40" y1="220" x2="560" y2="220" stroke="#888" stroke-width="1"/>
  <text x="300" y="260" text-anchor="middle" font-size="13" fill="#888" font-family="system-ui">embedding space</text>
  <!-- territory shading — full width, overlapping gradients -->
  <rect x="40" y="30" width="520" height="190" fill="url(#gA)"/>
  <rect x="40" y="30" width="520" height="190" fill="url(#gB)"/>
  <!-- Advertiser A: center=220, σ_px=70, peak at y=75 -->
  <polyline points="40,220 50,220 60,219 70,218 80,217 90,215 100,212 110,207 120,200 130,191 140,179 150,165 160,148 170,130 175,120 180,112 185,104 190,96 195,90 200,84 205,80 210,78 215,76 218,75 220,75 222,75 225,76 230,78 235,80 240,84 245,90 250,96 255,104 260,112 265,120 270,130 280,148 290,165 300,179 310,191 320,200 330,207 340,212 350,215 360,217 370,218 380,219 390,220" fill="none" stroke="#3b82f6" stroke-width="2.5" stroke-linejoin="round"/>
  <text x="220" y="62" text-anchor="middle" font-size="12" fill="#3b82f6" font-weight="bold" font-family="system-ui">Climbing PT</text>
  <text x="130" y="250" text-anchor="middle" font-size="11" fill="#3b82f6" font-family="system-ui">bid=$8 · σ=0.30</text>
  <!-- Advertiser B: center=380, σ_px=160, peak at y=150 -->
  <polyline points="40,218 60,216 80,214 100,211 120,208 140,204 160,199 180,194 200,188 220,182 240,176 260,170 280,164 300,159 310,156 320,154 330,152 340,150 350,149 360,148 370,147 375,147 378,146 380,146 382,146 385,147 390,147 400,148 410,149 420,150 430,152 440,154 450,156 460,159 480,164 500,170 520,176 540,182 560,188" fill="none" stroke="#f97316" stroke-width="2.5" stroke-linejoin="round"/>
  <text x="380" y="133" text-anchor="middle" font-size="12" fill="#f97316" font-weight="bold" font-family="system-ui">Sports PT</text>
  <text x="470" y="250" text-anchor="middle" font-size="11" fill="#f97316" font-family="system-ui">bid=$5 · σ=0.55</text>
</svg>
</noscript>

Drag the query dot. The Climbing PT's max bid is $8, but she never pays that. The price is always what the runner-up was worth. Move the query to the left, and see the price drop. This reflects how much less likely the customers there will convert. Move it toward the Sports PT and they take over. The customer is worth more to them in their turf.

That's the whole job. The publisher sets a [relevance threshold τ](/three-levers) to filter bad matches. The [scoring function](/power-diagrams-ad-auctions) picks the winner. VCG sets the price. No optimizer. No consultant. The advertiser just answers three business questions and the auction handles the rest. The [simulation](/keyword-tax) shows what happens when it does: specialists win the queries they're best at, generalists stop overpaying, and the keyword tax disappears.

## How do I set my bid?

Conversion rate times revenue per conversion. If 3% of clicks become customers worth $200 each, bid $6. You'll always pay less anyway.

One-shot bidding. Report your value and let the mechanism do the rest. If your auction requires a PhD in game theory to bid optimally, the auction is the bug.

---

*Part of the [Vector Space](/vector-space) series.*
