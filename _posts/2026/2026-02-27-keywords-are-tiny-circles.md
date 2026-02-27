---
layout: post
title: Keywords Are Tiny Circles
tags: coding
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose and worked through the mechanics.*

*Part of a series: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap)*

---

The previous posts in this series have a problem. They describe a mathematically elegant system — [power diagrams](/power-diagrams-ad-auctions) partitioning embedding space, [hill-climbing UX](/buying-space-not-keywords) for navigating it, a [new protocol](/embedding-gap) to carry embedding vectors. And they implicitly ask the market to throw away keywords and adopt continuous geometry instead.

The market will not do this. Not because the math is wrong. Because the migration path demands a regression.

An advertiser spending $50,000/month on "mesothelioma lawyer" at $200/click has a system that works. Predictable spend, predictable conversions, predictable ROI. Telling them "your keywords now live in a 3,072-dimensional vector space, good luck" is not an upgrade. It's a threat. Even if the new system is strictly better in theory, the transition requires trusting that the new machinery reproduces the old behavior *exactly* — and nobody trusts that on day one.

Every successful platform transition solves this problem the same way: the new system must be a strict superset of the old one. Old behavior is a special case, not a casualty. HTML didn't replace plain text — plain text is valid HTML. HTTPS didn't replace HTTP — it added a layer.

Keywords and embeddings have this relationship, and it's hiding in plain sight.

## A Keyword Is a Point with a Very Small Radius

Take the keyword "mesothelioma lawyer." Embed it. You get a point in 3,072-dimensional space. Now set the reach parameter σ to something tiny — σ → 0. The power diagram score function:

```
score(x) = log(bid) - ||x - center||² / σ²
```

With σ near zero, the score drops to negative infinity for any point that isn't almost exactly at the keyword's embedding. The advertiser's "territory" collapses to a single point.

This is what keyword advertising already is. A keyword auction is a power diagram auction where every advertiser has radius ≈ 0 and different advertisers happen to sit on the same point (the keyword embedding). The auction at that point is just second-price on bid — exactly what Google runs today.

Keywords aren't replaced by embeddings. Keywords *are* embeddings. They're the degenerate case where reach is zero.

![Keywords are tiny circles — same points, different radii](/assets/09_keywords_are_tiny_circles.jpg)

## The Radius Is the Only New Thing

The entire difference between keyword advertising and embedding-space advertising is one parameter: **σ**. How far does your influence extend from your center point?

| σ | Behavior | Analog |
|---|----------|--------|
| ≈ 0 | Wins only at exact keyword match | Classic keyword auction |
| Small | Wins for close paraphrases | Broad match keywords |
| Medium | Wins for related topics | Topic targeting |
| Large | Wins across a semantic neighborhood | Interest-based targeting |

Google's keyword match types — exact, phrase, broad — are already an informal version of this. Exact match is σ ≈ 0. Broad match is Google expanding your radius behind the scenes, using their own embedding model, without telling you the geometry. You don't control the radius. You don't see the radius. You select "broad match" and trust the algorithm.

The power diagram makes the radius explicit. You set σ. You see the territory it buys. You see the price. No black box.

## Priority by Radius

Here's the mechanism that makes adoption safe: **tight-radius bids take priority at their center point.**

When a conversation embedding lands exactly on "mesothelioma lawyer," two advertisers compete:

1. A keyword advertiser with σ ≈ 0 and bid $200
2. A vector advertiser targeting "legal services" with σ = 0.5 and bid $50

The score function handles this automatically. At the keyword point itself:

```
Keyword advertiser: log(200) - 0² / 0.001² = 5.30
Vector advertiser:  log(50)  - d² / 0.25   = 3.91 - 4d²
```

Even if the vector advertiser is close (d = 0.1), their score is 3.87. The keyword advertiser wins by a mile. The σ² in the denominator means tight-radius bids concentrate all their competitive power at their center. A sniper beats a shotgun at the sniper's chosen point.

But move slightly away from "mesothelioma lawyer" — toward "asbestos exposure health risks" or "mesothelioma support groups" — and the keyword advertiser's score collapses while the vector advertiser's score barely changes. The vector advertiser picks up all the adjacent territory that keywords can't reach.

No regression for keyword buyers. No wasted impressions for vector buyers. They coexist by operating at different scales.

## The Opt-In

This is what makes adoption a checkbox instead of a migration.

**Day one.** An advertiser's existing keyword campaigns import directly. Each keyword becomes a center point (its embedding) with σ ≈ 0 and the existing bid. Behavior is identical. No regression. The advertiser doesn't even need to know the system changed underneath.

**Day two.** The platform offers a new option next to each keyword: *"Expand to similar queries?"* One checkbox. Checking it increases σ from ≈ 0 to some small default — say σ = 0.05. The advertiser now wins a small semantic neighborhood around their keyword. The platform shows example queries they'd now match: "mesothelioma attorney," "asbestos lawsuit lawyer," "mesothelioma legal help." Close paraphrases they were already buying through Google's broad match, except now the radius is explicit and the territory is visible.

**Day three.** The advertiser drags a slider. σ goes from 0.05 to 0.15. Territory expands. New example queries appear — "mesothelioma settlement amounts," "asbestos trust fund claims." The price display updates in real time. The advertiser sees exactly what they're buying at each radius, decides where to stop.

**Day thirty.** The sophisticated advertiser drops the keyword entirely. They've been [hill-climbing through embedding space](/buying-space-not-keywords), found a region that outperforms any keyword they could have guessed, and they're bidding on geometry directly.

The migration isn't a switchover. It's a gradient. Every advertiser enters at the keyword end and moves toward vectors at their own pace — or never moves at all. Keyword campaigns keep working forever. They're just circles with very small radii.

## The Infrastructure Problem

Advertisers don't adopt anything. Infrastructure does. An advertiser clicks buttons in a DSP. The DSP talks to an exchange. The exchange talks to an SSP. The SSP talks to the publisher. Four intermediaries, each with their own codebase, their own contracts, their own customers who will leave if something breaks.

Embedding-space advertising doesn't ship until every layer of this stack can say yes — and every layer has a different reason to say no.

## What the DSP Needs

A demand-side platform manages campaigns for thousands of advertisers. Their entire system — campaign creation, bid optimization, budget pacing, reporting, attribution — is built on keywords and categories. That's not technical debt. That's the product.

A DSP will not rewrite their campaign management to support geometric targeting. They won't retrain their bid optimization models for continuous space. They won't rebuild their reporting dashboards to explain "territory" instead of "keyword performance." Not because they're conservative. Because their advertisers would leave.

What a DSP *can* do: add one optional field.

A keyword campaign already specifies a list of keywords and bids. The DSP auto-embeds each keyword to get a center point. Default σ ≈ 0. Campaign behaves identically. Nothing changes for the advertiser, nothing changes for the optimization model, nothing changes for reporting. The keyword *is* the embedding. The DSP just didn't compute it before.

Then, for advertisers who opt in: a σ slider per keyword. The DSP's optimization model treats it as one more parameter to tune, no different from bid adjustments by device or geography. Budget pacing still works because the DSP can estimate impression volume at any given σ the same way it estimates volume for broad match today — except now the radius is explicit instead of hidden inside Google's black box.

The DSP's reporting says: "Your keyword 'mesothelioma lawyer' won 1,200 impressions at exact match and 3,400 additional impressions within σ = 0.08." Familiar format. One new column. The advertiser who never touches σ sees the same report they've always seen.

No rewrite. No retraining. One optional parameter that defaults to zero.

## What the SSP Needs

A supply-side platform represents publishers. Its job is to maximize yield on every impression. An SSP will adopt embedding support if and only if it increases fill rate and CPM without degrading anything for publishers already making money on keywords.

The guarantee: **keyword demand clears first at keyword points.**

When a publisher's impression matches a keyword that DSPs are bidding on, the auction at that point is dominated by keyword bidders (σ ≈ 0) because their scores are maximally concentrated. The SSP's existing keyword demand — every contract, every insertion order, every programmatic deal — clears exactly as before. Same winners, same prices, same fill rate.

What embedding adds is coverage of the *empty space*. Most impressions in LLM conversations don't land on any keyword. Today those impressions either go unfilled or get shoved into a catch-all category at low CPMs. With embedding-aware demand in the auction, vector bidders (σ > 0) compete for these impressions at prices that reflect their actual semantic value instead of a lowest-common-denominator category label.

The SSP's pitch to publishers becomes: "Your keyword revenue is unchanged. We're adding a new demand layer that fills the gaps." That's the same pitch SSPs made when they added header bidding alongside direct deals — additive, not substitutive.

The SSP never has to tell a publisher that keywords are being deprecated. Keywords are permanent. They're the σ ≈ 0 case. A keyword bidder in 2035 competes in the same auction as a vector bidder, and wins at exact-match points, because the math guarantees it.

## What the Exchange Needs

The exchange sits in the middle. It receives bid requests from SSPs and bid responses from DSPs. It clears the auction. Its constraint is harder than either side: it must run a single auction that treats keyword bids and vector bids as first-class participants, with no special-case logic and no two-pass system.

This is exactly what the power diagram provides. One auction. One score function. Every bidder — keyword or vector — evaluated by the same formula:

```
score_i(x) = log(b_i) - ||x - c_i||² / σ_i²
```

A keyword bidder is a bidder with σ_i ≈ 0. A vector bidder has σ_i > 0. The exchange doesn't distinguish between them. It evaluates all bidders, picks the highest score, computes VCG payments. One code path.

The [protocol extension](/embedding-gap) carries both representations:

```json
{
  "keywords": ["mesothelioma lawyer"],
  "cat": ["IAB11-4"],
  "embedding": [0.23, -0.41, 0.87, ...],
  "embedding_spec": "v1.0"
}
```

DSPs that don't understand embeddings bid on `keywords` and `cat`. The exchange maps those keywords to embedding points with σ ≈ 0 and enters them into the power diagram. DSPs that understand embeddings bid on regions directly. Both enter the same auction. The exchange doesn't need fallback logic or a separate clearing mechanism for legacy demand. There is no legacy demand. There's only demand at various radii.

This is the critical property: the exchange doesn't need to maintain two auction systems or route between them. Keyword auctions and embedding auctions aren't different things that need to be reconciled. They're the same thing at different scales. One implementation. One clearing price. One winner.

## In Perpetuity

This isn't a migration with a deprecation timeline. Keywords are not "legacy mode." σ ≈ 0 is a permanently valid, permanently optimal strategy for high-value narrow-intent queries.

Think about it from the advertiser's side: if you're a mesothelioma law firm and a click is worth $200 to you, you *want* σ ≈ 0. You want to concentrate every dollar of competitive power on the exact query that converts. Expanding your radius dilutes your bid across territory you don't care about. The sniper rifle is the right tool for this job. It's not training wheels.

And from the infrastructure side: every SSP, DSP, and exchange can promise their constituents that keywords work forever because keywords aren't a compatibility shim bolted onto the new system. They *are* the system. The embedding auction is a generalization of the keyword auction. Turning off keyword support would mean removing σ ≈ 0 from the parameter space — which is like removing the number zero from arithmetic. It doesn't make sense as a concept.

The business case isn't replacing keyword revenue. It's monetizing the 80% of LLM conversation impressions that don't match any keyword. Those impressions go unfilled today. With vector bids in the same auction, they don't. The vector layer is purely additive — every intermediary in the stack takes a cut of revenue that previously didn't exist.

That's the pitch that gets infrastructure to move. Not "embeddings are better than keywords." Better doesn't pay the bills. "Keywords keep working exactly as before, and embeddings fill the gaps" does.

Keywords are tiny circles. The system that runs tiny circles already runs big circles. The rest is adoption.

---

*Previously: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap). If you're working on this problem, I'd like to hear from you — june@june.kim.*
