---
layout: post
title: "Trustworth"
tags: vector-space
image: "/assets/trustworth.jpg"
---

*Part of the [Vector Space](/vector-space) series.*

Digital advertising has a [$63 billion](https://www.mediapost.com/publications/article/412156/ad-spend-wasted-on-invalid-traffic-reached-63b-in.html) fraud problem. For every ad dollar a merchant spends, [most of it](https://www.fraudlogix.com/stats/ad-fraud-statistics-2026) never reaches a real consumer. The open market is a [lemons pool](https://en.wikipedia.org/wiki/The_Market_for_%22Lemons%22). A publisher running ads can't tell the difference between a pet food brand sourcing from a USDA-inspected facility with ten years of retailer relationships and one that white-labels products of unknown origin and launched last month. Neither can the buyer. You can't taste dog food. Your dog can't leave a review. The packaging looks the same. The only signal is the ad.

![Trustworth](/assets/trustworth.jpg)

## Which kibble?

| | Bark & Bond (legit) | Sunny Paws (shady) |
|---|---|---|
| Track record | Decade of clean payments | Launched last month |
| Endorsements | Hundreds of retailers | Stock photo of a golden retriever |
| Supply chain | Direct relationships with inspected facilities | White-labeled, origin unknown |
| Ad strategy | Bids conservatively — fraud dilutes ROI | Bids aggressively — repeat customers don't matter |
| Growth | Word of mouth | Facebook ad budget |

The publisher gets worse advertisers, the audience gets worse ads, and Bark & Bond competes through reputation instead of reach. Everyone loses except the fraudsters.

Bark & Bond has the evidence to prove it's real, but nobody can read their signals.

[Proof of Trust](/proof-of-trust) described a protocol that could read them: attestation emails, DKIM signatures, federated curators, a public trust graph. But nobody uses it, because nobody uses it. The exchange doesn't exist. Classic cold start.

## What if it worked

Imagine Bark & Bond's decade of clean Stripe history, its hundreds of retailer endorsements, its supplier relationships with inspected facilities. All publicly attested, cryptographically signed, indexed by competing curators. Publishers subscribe to curators who filter the lemons out. Sunny Paws can't fake twenty handshakes with real retailers. It can buy ads, but it can't buy the trust signals. Bark & Bond's ad rates drop because its trust score is high, and Sunny Paws's rates climb because its graph is thin. Fraud doesn't disappear, but it gets expensive. The lemons pool drains. Trustworthiness becomes measurable. Trustworth.

But why would Stripe publish Bark & Bond's attestations to a graph that Square can read? They wouldn't. Not voluntarily. Not first.

## Who starts

Exchanges already price risk and route demand. One that builds a trust graph gets higher CPMs because trust-scored inventory means better advertisers and better publisher relationships. A curated marketplace commands a premium over a lemons pool.

The exchange just needs enough demand-side liquidity that merchants care about being in its graph. Bark & Bond attests and gets better placement; Sunny Paws doesn't and gets the lemons rate. The exchange publishes the graph; curators interpret it; publishers compose trust policies. Each layer has its own incentive.

## Who follows

Once the exchange exists, who attests on Bark & Bond's behalf? Stripe's merchant base is a competitive asset, and attestations leak signal about who their best customers are. Why hand competitors a prospecting list?

But a smaller processor has a different calculus. Fewer merchants, weaker brand, every acquisition matters more. If attesting gets merchants like Bark & Bond better ad placement, attestation is a growth feature. The entrant has nothing to protect and everything to gain.

Bark & Bond sees two options: Stripe, who hoards its data, or the entrant, who will vouch for it publicly. Bark & Bond keeps Stripe and adds the entrant as a second processor — one that comes with attestation.

## Why shallow fails

Stripe's first response is to offer the minimum: "good standing." Check the box, give away nothing useful.

But curators rank on depth. "Good standing" puts Bark & Bond on the graph. A detailed attestation showing 0.1% chargebacks over 14,000 transactions across ten years puts it at the top. Richer leaderboards attract more publisher subscribers, which attracts better advertisers. The pressure runs downhill: Bark & Bond demands deeper attestation because depth determines rank.

Depth also creates stickiness. Ten years of detailed history with Stripe can't be reproduced on day one at a competitor. The attestation creates the switching cost it was supposed to leak. Platforms compete on attestation depth the way credit card companies compete on rewards. The richer the signal, the harder to leave.

Why not proprietary scores instead of open attestations? A score locked inside Stripe's dashboard is a walled garden. Bark & Bond needs portable proof that curators, publishers, and competing exchanges can all read.

<table>
<thead><tr><th>Who</th><th>Why</th></tr></thead>
<tr><td>Exchange</td><td>Higher CPMs from trust-scored inventory</td></tr>
<tr><td>Legit merchant</td><td>Better ad placement, lower fraud tax</td></tr>
<tr><td>Entrant processor</td><td>Growth lever, nothing to protect</td></tr>
<tr><td>Incumbent processor</td><td style="opacity:0.35">Leaks signal about best customers</td></tr>
<tr><td>Publisher</td><td>Better advertisers, better audience</td></tr>
<tr><td>Curator</td><td>Subscriber revenue from richer leaderboards</td></tr>
</table>

One holdout. Everyone else is ready.

## Who let the dogs out

Milgrom's [unraveling](https://www.semanticscholar.org/paper/Good-News-and-Bad-News:-Representation-Theorems-and-Milgrom/be34ed573a272e1a78a056ec29a1932fe6915ad2): the firm with the most favorable information discloses first. The audience infers that anyone staying silent must have worse information. So the next-best firm discloses. Then the next. The cascade continues until silence is an admission.

Once Bark & Bond attests through the entrant, every pet food brand on a non-attesting processor looks worse. The market now has a baseline for what disclosure looks like. The trust graph is a ticket into the exchange, and not having one is a position statement.

Bark & Bond stays on Stripe. It just asks: *why can't I get attestations like my competitor on that other processor?* Enough merchants asking that question, and Stripe attests. For retention.

1. *An exchange builds the trust graph.* Higher CPMs pay for the infrastructure.
2. *Bark & Bond attests.* It gets out of the lemons pool. Its ad rates improve. The ROI is immediate.
3. *An entrant payment processor attests on Bark & Bond's behalf.* It's a growth lever — "your merchants get trust-scored ad placement" writes itself.
4. *Stripe resists.* Until merchant churn forces their hand. The question changes from "why would Stripe attest?" to "how long can Stripe afford not to?"
5. *The graph reaches critical mass.* Merchants self-select into transparency because the alternative is paying a fraud tax on every ad dollar.

## Two emails make a handshake

SSL Certificate Transparency followed the same arc. Let's Encrypt baked transparency in from day one, and when it became a requirement, it exposed 30,000 improperly issued Symantec certificates. Symantec sold their CA business. What made CT irreversible was that the protocol was open. No gatekeeper to lobby, no API to shut down.

The attestation graph works the same way. The protocol is [SMTP and DKIM](/proof-of-trust), infrastructure that's been running for twenty years. Exchanges index attestation emails, curators pull the graph and publish allowlists, and publishers compose trust policies from competing curators.

That's what makes the unraveling permanent. Once merchants like Bark & Bond discover that transparency gets them better ad rates, the demand is structural. No single exchange owns it. The protocol spreads the way ads.txt [spread](https://pubmatic.com/blog/ads-txt-rise-ad-tech/), because non-participation became expensive. The cost of joining is two emails.

You still can't taste dog food. But you can read the graph of who made it, who inspected it, and who's been buying it for ten years. That's what trustworth means.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
