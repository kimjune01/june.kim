---
layout: post
title: "Trustworth"
tags: vector-space
---

*Part of the [Vector Space](/vector-space) series.*

[Proof of Trust](/proof-of-trust) described the protocol: attestation emails, DKIM signatures, federated curators, a public trust graph. The technical machinery works. But why would anyone use it?

Specifically: why would Stripe publish attestations about its best merchants to a graph that Square can read?

They wouldn't. Not voluntarily. Not first.

## The lemons pool

Digital advertising has a [$63 billion](https://www.mediapost.com/publications/article/412156/ad-spend-wasted-on-invalid-traffic-reached-63b-in.html) fraud problem. For every dollar a merchant spends on programmatic ads, [less than half](https://www.fraudlogix.com/stats/ad-fraud-statistics-2026) reaches a real consumer. One in five impressions is invalid. The open market is a [lemons pool](https://en.wikipedia.org/wiki/The_Market_for_%22Lemons%22): publishers can't distinguish a plumber who's served the same neighborhood for twenty years from a dropshipper who registered yesterday.

The plumber bids conservatively because her ROI is diluted by fraud. The dropshipper bids aggressively because he doesn't care about repeat customers. The publisher gets worse advertisers, the audience gets worse ads, and the plumber finds customers through word of mouth instead. Everyone loses except the fraud layer.

The plumber has the evidence to prove she's legitimate. Three years of clean payment processing. Forty-seven satisfied customers. Five supplier relationships. The signals exist. Nobody can read them.

## The exchange moves first

An ad exchange that builds a trust graph gets higher CPMs. Trust-scored inventory means better advertisers, better ads, better publisher relationships. The exchange is the natural first mover because it captures value directly: a curated marketplace commands a premium over a lemons pool.

The exchange doesn't need monopoly power. It needs enough demand-side liquidity that merchants care about being in its graph. Merchants who attest get better ad placement. Merchants who don't get the lemons rate. The exchange publishes the graph; curators interpret it; publishers compose trust policies from curators. Each layer has its own incentive to participate.

## Entrants have nothing to lose

Once the exchange exists, who attests?

Stripe won't go first. Their merchant base is a competitive asset, and publishing attestations leaks signal about who their best customers are. The rational move is to hoard.

But a smaller payment processor has a different calculus. Fewer merchants. Weaker brand. Every customer acquisition matters more. If attesting gets their merchants better ad placement and lower acquisition costs, attestation is a growth feature. The entrant has no merchant base to protect and everything to gain from transparency.

The merchant sees two options: the incumbent who hoards data, or the entrant who will vouch for you publicly. The merchant who needs better ad rates picks the entrant. Not to replace Stripe — to add a second relationship that comes with attestation.

## Shallow won't cut it

The incumbent's first response is to offer the minimum: "good standing." Check the box, neutralize the entrant's advantage, protect the real data.

But curators rank on depth. A coarse attestation — "good standing" — puts you on the graph. A detailed one showing 0.1% chargebacks over 14,000 transactions across three years puts you at the top. Curators who publish richer leaderboards attract more publisher subscribers. Publishers who use richer curators get better advertisers. The pressure runs downhill: merchants demand deeper attestation because depth determines rank.

And depth is what creates stickiness. Three years of detailed history with one processor can't be reproduced on day one at a competitor. The merchant's trust position is anchored to the relationship that generated it. The attestation creates the switching cost it was supposed to leak. Platforms end up competing on attestation depth the way credit card companies compete on rewards — the richer the signal, the harder to leave.

## Silence becomes a signal

This is where Milgrom's [unraveling](https://www.semanticscholar.org/paper/Good-News-and-Bad-News:-Representation-Theorems-and-Milgrom/be34ed573a272e1a78a056ec29a1932fe6915ad2) kicks in. The firm with the most favorable information discloses first. The audience infers that anyone staying silent must have worse information. So the next-best firm discloses. Then the next. The cascade continues until silence is an admission.

Once the entrant attests, merchants on non-attesting platforms look worse than before. Not because anything changed about their business — but because the market now has a baseline for what disclosure looks like. The trust graph is a leaderboard, and not being on it is a position statement.

The merchant doesn't need to leave Stripe. She just needs to ask: *why can't I get attestations like my competitor on that other processor?* Enough merchants asking that question, and Stripe attests. Not out of generosity. Out of retention.

SSL Certificate Transparency followed the same arc. Let's Encrypt, a new entrant, baked transparency in from day one. Symantec, the incumbent, resisted. When transparency became a requirement, it exposed 30,000 improperly issued certificates. Symantec sold their CA business. The entrant's transparency became the standard.

## The sequence

1. *An exchange builds the trust graph.* Trust-scored inventory commands higher CPMs. The exchange captures value directly.
2. *Merchants in good standing attest.* It gets them out of the lemons pool. The ROI on attestation is immediate.
3. *An entrant payment processor attests.* It's a growth lever. "Your merchants get trust-scored ad placement" is a sales pitch that writes itself.
4. *The incumbent resists.* Until merchant churn forces their hand. The question changes from "why would Stripe attest?" to "how long can Stripe afford not to?"
5. *The graph reaches critical mass.* Not through mandate or monopoly power — through merchants self-selecting into transparency because the alternative is paying a fraud tax on every ad dollar.

The same dynamic that made ads.txt [universal within two years](https://pubmatic.com/blog/ads-txt-rise-ad-tech/) — DSPs deprioritizing non-adopting inventory — applies here. Once curators weight attested merchants higher, non-attestation is a cost. Once it's a cost, it's a matter of time.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
