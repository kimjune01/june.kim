---
layout: post
title: "Trustworth"
tags: vector-space
---

*Part of the [Vector Space](/vector-space) series.*

Digital advertising has a [$63 billion](https://www.mediapost.com/publications/article/412156/ad-spend-wasted-on-invalid-traffic-reached-63b-in.html) fraud problem. For every ad dollar a merchant spends, [most of it](https://www.fraudlogix.com/stats/ad-fraud-statistics-2026) never reaches a real consumer. The open market is a [lemons pool](https://en.wikipedia.org/wiki/The_Market_for_%22Lemons%22): publishers can't distinguish a pet food brand sourcing from a USDA-inspected facility with ten years of retailer relationships from one that white-labels products of unknown origin and launched last month. Neither can the buyer. You can't taste dog food. Your dog can't leave a review. The packaging looks the same. The only signal is the ad.

Call them WholePet and BarkBox Plus. WholePet has a decade of clean payment processing, hundreds of retailer endorsements, direct supplier relationships with inspected facilities. BarkBox Plus has a Shopify store, a stock photo of a golden retriever, and a Facebook ad budget. WholePet bids conservatively because fraud dilutes its ROI. BarkBox Plus bids aggressively because it doesn't need repeat customers. The publisher gets worse advertisers, the audience gets worse ads, and WholePet grows through word of mouth instead. Everyone loses except the fraud layer.

WholePet has the evidence to prove it's real. The signals exist. Nobody can read them.

[Proof of Trust](/proof-of-trust) described a protocol that could read them: attestation emails, DKIM signatures, federated curators, a public trust graph. But nobody uses it, because nobody uses it. The graph is empty. The exchange doesn't exist. Classic cold start.

Who would start?

Imagine WholePet's decade of clean Stripe history, its hundreds of retailer endorsements, its supplier relationships with inspected facilities. All publicly attested, cryptographically signed, indexed by competing curators. Publishers subscribe to curators who filter the lemons out. BarkBox Plus can't fake twenty bilateral attestations from real retailers. It can buy ads, but it can't buy topology. WholePet's ad rates drop because its trust score is high. BarkBox Plus's rates climb because its graph is thin. Fraud doesn't disappear, but it gets expensive. The lemons pool drains. Trustworthiness becomes measurable. Trustworth.

Why would Stripe publish WholePet's attestations to a graph that Square can read? They wouldn't. Not voluntarily. Not first.

## Who starts

Exchanges already price risk and route demand. One that builds a trust graph gets higher CPMs because trust-scored inventory means better advertisers, better ads, better publisher relationships. A curated marketplace commands a premium over a lemons pool.

The exchange just needs enough demand-side liquidity that merchants care about being in its graph. WholePet attests and gets better placement. BarkBox Plus doesn't and gets the lemons rate. The exchange publishes the graph; curators interpret it; publishers compose trust policies. Each layer has its own incentive.

## Who follows

Once the exchange exists, who attests on WholePet's behalf? Stripe's merchant base is a competitive asset, and attestations leak signal about who their best customers are. The rational move is to hoard.

But a smaller processor has a different calculus. Fewer merchants, weaker brand, every acquisition matters more. If attesting gets merchants like WholePet better ad placement, attestation is a growth feature. The entrant has nothing to protect and everything to gain.

WholePet sees two options: Stripe, who hoards its data, or the entrant, who will vouch for it publicly. WholePet keeps Stripe and adds the entrant as a second processor — one that comes with attestation.

## Why shallow fails

Stripe's first response is to offer the minimum: "good standing." Check the box, neutralize the entrant's advantage, protect the real data.

But curators rank on depth. "Good standing" puts WholePet on the graph. A detailed attestation showing 0.1% chargebacks over 14,000 transactions across ten years puts it at the top. Richer leaderboards attract more publisher subscribers, and richer curators attract better advertisers. The pressure runs downhill: WholePet demands deeper attestation because depth determines rank.

Depth also creates stickiness. Ten years of detailed history with Stripe can't be reproduced on day one at a competitor. The attestation creates the switching cost it was supposed to leak. Platforms compete on attestation depth the way credit card companies compete on rewards. The richer the signal, the harder to leave.

Why not proprietary scores instead of open attestations? A score locked inside Stripe's dashboard is a walled garden. WholePet needs portable proof that curators, publishers, and competing exchanges can all read.

## Who let the dogs out

Milgrom's [unraveling](https://www.semanticscholar.org/paper/Good-News-and-Bad-News:-Representation-Theorems-and-Milgrom/be34ed573a272e1a78a056ec29a1932fe6915ad2): the firm with the most favorable information discloses first. The audience infers that anyone staying silent must have worse information. So the next-best firm discloses. Then the next. The cascade continues until silence is an admission.

Once WholePet attests through the entrant, every pet food brand on a non-attesting processor looks worse. The market now has a baseline for what disclosure looks like. The trust graph is a leaderboard, and not being on it is a position statement.

WholePet stays on Stripe. It just asks: *why can't I get attestations like my competitor on that other processor?* Enough merchants asking that question, and Stripe attests. Not out of generosity. Out of retention.

## The unraveling

1. *An exchange builds the trust graph.* Higher CPMs pay for the infrastructure.
2. *WholePet attests.* It gets out of the lemons pool. Its ad rates improve. The ROI is immediate.
3. *An entrant payment processor attests on WholePet's behalf.* It's a growth lever — "your merchants get trust-scored ad placement" writes itself.
4. *Stripe resists.* Until merchant churn forces their hand. The question changes from "why would Stripe attest?" to "how long can Stripe afford not to?"
5. *The graph reaches critical mass.* Merchants self-select into transparency because the alternative is paying a fraud tax on every ad dollar.

## The protocol is the point

SSL Certificate Transparency followed the same arc. Let's Encrypt baked transparency in from day one. Symantec resisted. When transparency became a requirement, it exposed 30,000 improperly issued Symantec certificates, and Symantec sold their CA business. What made CT irreversible was that the protocol was open. No gatekeeper to lobby, no platform to acquire, no API to shut down.

The attestation graph works the same way. The protocol is [SMTP and DKIM](/proof-of-trust), infrastructure that's been running for twenty years. Exchanges index attestation emails. Curators pull the graph and publish allowlists. Publishers compose trust policies from competing curators.

That's what makes the unraveling permanent. Once merchants like WholePet discover that transparency gets them better ad rates, the demand is structural. No single exchange owns it. No single curator controls it. The protocol spreads the way ads.txt [spread](https://pubmatic.com/blog/ads-txt-rise-ad-tech/), because non-participation became expensive. The cost of joining is two emails.

You still can't taste dog food. But you can read the graph of who made it, who inspected it, and who's been buying it for ten years. That's what trustworth means.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
