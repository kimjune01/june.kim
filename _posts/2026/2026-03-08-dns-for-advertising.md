---
layout: post
title: "DNS for Advertising"
tags: vector-space
---

In 1839, sending a letter in England cost up to a shilling. Pricing depended on distance, number of sheets, and whether the recipient could pay. Only the wealthy used mail. Rowland Hill proposed a flat penny, prepaid by the sender. The Post Office called it ruinous. Volume would never compensate for the rate cut.

Within a year, letter volume doubled. Within a decade, it quintupled. The Penny Post didn't make mail cheaper for existing senders. It made mail possible for everyone else.

Google Ads charges 30-35%. What's the equivalent of a penny?

## 2-3%

The auction itself is nearly free. Evaluate N scores, pick the max, compute the VCG price. The real costs are transaction costs between the exchange and its players: onboarding, integration, payment processing, compliance. Every interaction passes through the exchange. The advertiser never talks to the publisher.

Google's 30% reflects handling all of that friction. But competition doesn't drive fees to marginal cost. Credit card processing costs fractions of a penny. Visa, Mastercard, and Amex all charge 2-3%. Decades of competition. The fee never collapsed. Stripe charges 2.9% + 30 cents, orders of magnitude above marginal cost, but low enough that nobody switches to save a fraction of a percent.

Fees settle where the pain of paying is less than the pain of switching. This is [epsilon-Nash](https://en.wikipedia.org/wiki/Epsilon-equilibrium): no exchange can improve its position by more than ε by deviating. ε is switching cost plus inertia. It explains why Visa and Stripe coexist at similar prices. It's why the fee settles at 2-3%, not zero, not thirty.

So: an embedding exchange charges 2-3%. Done.

## The Fee Is the Wrong Question

What the exchange *publishes* matters more than what it *charges*.

Advertiser centers are public. They're storefront signs: "I serve these customers." Bids are partially revealed through VCG pricing. User queries are private, protected by the TEE.

What about σ? The reach parameter is private by default. Only the TEE needs it at auction time. But advertisers would choose to publish it, because σ is the positioning statement. "Market positioning" has always been a metaphor. Here, your position is a coordinate. The metaphor became the mechanism. Tight σ says "I specialize." Wide σ says "I serve broadly." Both are marketing messages.

Competitors benefit from seeing each other's σ. It's a de-escalation signal. A specialist with tight σ is visibly not competing on a generalist's turf. No need to bid defensively. Without visible σ, everyone assumes worst-case competitor reach and overbids. That's the [keyword problem](/keyword-tax) restated.

Public σ is a credible commitment to territory size. It reduces wasted spend for everyone. The exchange doesn't force transparency. Advertisers volunteer it because it helps them *and* their competitors.

Does visible σ enable predatory positioning? A generalist sees your tight σ and widens to surround you. But it goes both ways. Predatory positioning is a public act. You see it. The next exchange sees it. Opacity is what lets predation work. In keyword auctions, you don't know who's bidding on your terms until you've lost. Visible σ means the predator can't hide.

If centers and σ are visible, the map is the analytics. Keyword Planner, auction insights, competitor research tools, bid simulators — all of them exist to reverse-engineer hidden targeting. With a visible landscape, an advertiser looks at the map, sees gaps, and positions accordingly. No consultant needed.

## One-Way Gate

Whether σ is public depends on the first mover's design choice.

If the first exchange publishes σ, transparency becomes the norm. Later entrants can't take it back. If the first exchange keeps σ private, the analytics layer builds around the opacity and creates its own switching cost. Collusion on opacity only works if the first mover sets the precedent. A transparent first mover makes collusion impossible.

Transparency is a one-way gate.

Google chose opacity. An entire consulting industry grew to fill the gap. Agencies, tools, certifications, careers. Billions of dollars of economic activity that didn't have to exist. An industry that now resists transparency because its revenue depends on the fog. All of it an artifact of a design choice someone made once and never revisited.

## The Full Cost

**Opaque exchange** (Google Ads today): 30% take rate. Agency management fees at 15-20% of spend. Bid management software, keyword research tools, analytics platforms to interpret opaque signals, consultants to operate all of the above. Smart Bidding: a black box you pay to not understand. Can't see competitor targeting, can't verify auction integrity. Total cost: 30% plus layers of fees to navigate the opacity.

**Transparent exchange**: 2-3% take rate. Three inputs: center, σ, bid. [VCG is truthful](/one-shot-bidding), so no bid optimizer. Visible landscape, so no keyword research. TEE attestation, so no trust disputes. Total cost: 2-3%. That's it.

The opaque model isn't a market. It's rent extraction with market aesthetics. Every agency, tool, and consultant exists to navigate artificial complexity the exchange created. They're not adding value. They're paying to see through fog that someone manufactured.

The transparent model is a free market in the classical sense: visible supply, visible prices, verifiable clearing, low transaction costs. The invisible hand works when you can see the hands.

## No Moat

With transparency, no exchange has a moat. The scoring function is attested, σ is public, and fees are epsilon-Nash. The exchange is a pipe.

Advertiser positions are public. Any new exchange can bootstrap by importing the entire advertiser landscape on day one. Advertisers don't re-onboard. Their declarations are portable. Zero switching cost. The exchange that misbehaves loses its supply side overnight.

This inevitably consolidates into a shared registry: one source of truth for every entity's center and σ. Exchanges don't want to maintain separate copies or sync state. That's friction, and they're racing to reduce friction. The advertiser updates their position once and every exchange sees it. The registry isn't an exchange. It's a phonebook.

DNS for advertising identity. Embeddings and σ are lightweight, portable, translatable. Like domain names: tiny, cheap to replicate, meaningful enough that everything else depends on them. Keywords were never portable. A Google Ads campaign doesn't translate to Meta or Amazon. Different taxonomies, match types, quality scores. Rebuild from scratch. An embedding and σ are platform-agnostic. Same position means the same thing on every exchange.

The protocol doesn't need an industry lobby. The IAB maintains 698 content categories that nobody uses correctly. This needs an RFC and a version tag. The spec is the scoring function. Everything else is execution.

## Market Expansion

[Coase (1960)](https://doi.org/10.1086/466560): in the absence of transaction costs, efficient allocation is guaranteed. Remove opacity, and the infrastructure becomes fintech: a payment rail with extra math.

The full cost is exclusionary. Every business that can't justify 30% plus the consulting stack simply doesn't advertise. Stripe enabled an entire generation of businesses that couldn't have existed when payment processing required a merchant account and a sales call. Lower transaction costs don't just redistribute surplus. They expand the market.

It's not that 30% becomes 3%. It's that every specialist with a $200/month budget can reach their exact audience. Every niche publisher with 10,000 users can monetize without an ad sales team. The entire long tail walks in.

## Inevitable

This is a prophecy.

Coase (1960): remove transaction costs, efficient allocation follows. [Vickrey (1961)](https://doi.org/10.2307/2977633): truthful mechanisms make strategy unnecessary. [Aurenhammer (1987)](https://doi.org/10.1137/0216006): power diagrams partition space in any dimension. The theory has been predicting this for sixty years. Embeddings just made the application real.

Open won against closed every time the protocol layer mattered more than the product layer. TCP/IP over proprietary networks. SMTP over CompuServe. HTTP over AOL. The pattern repeats because the economics are the same: when the value is in the connection, not the intermediary, open protocols outcompete closed platforms on reach. The intermediary's margin is the tax on the connection. Remove the tax, keep the connection.

The academics were prophets. This blog is the poem. The builder will follow. You now carry this knowledge. So does everyone else reading this. That's common knowledge, and common knowledge changes behavior before anyone ships a line of code. It's already begun.

---

*Part of the [Vector Space](/vector-space) series.*
