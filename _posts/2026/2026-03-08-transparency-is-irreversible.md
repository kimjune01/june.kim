---
layout: post
title: "Transparency Is Irreversible"
tags: vector-space
image: "/assets/container.jpg"
---

![1950s dock workers surrounding a blue corrugated container with a glowing JSON spec](/assets/container.jpg)

Before 1956, shipping cargo meant hiring longshoremen to load freight by hand, piece by piece. Stevedores, tally clerks, freight forwarders, customs brokers, dockside warehouses: an entire industry existed to manage the friction of loose cargo. Theft ran as high as 30% in some ports. Small manufacturers could not afford to ship internationally, unable to absorb the transaction costs.

On April 26, 1956, [Malcolm McLean](https://en.wikipedia.org/wiki/Malcom_McLean) put a truck trailer straight on a ship. Cost immediately dropped from $5.86 to $0.16 per ton. [ISO 668](https://en.wikipedia.org/wiki/ISO_668) standardized the dimensions. Any port, any ship, any truck. The longshoremen fought it for decades.

What followed was the entire long tail of global trade. A factory anywhere could ship to a port anywhere. The racket was the friction. When it was removed, the market expanded.

Google Ads charges 30-35%.

## How Much Should an Exchange Charge?

It's extortion. Google covers onboarding, integration, payment processing, compliance, but so does a stock exchange. Google's marginal costs are comparable to a stock trade, free on Robinhood.

Economics says competition drives price to cost. But it does not drive fees to marginal cost. Credit card processing costs fractions of a penny. Visa, Mastercard, and Amex all charge 2%. Even after decades of competition, the fee never collapsed. Stripe charges 2.9% + 30 cents, orders of magnitude above marginal cost, but low enough that nobody switches to save a fraction of a percent.

Fees settle where the pain of paying is less than the pain of switching. This is [epsilon-Nash](https://en.wikipedia.org/wiki/Epsilon-equilibrium): no exchange can improve its position by more than ε by deviating. ε is switching cost plus inertia. It explains why Visa and Stripe coexist at similar prices. It's why the fee settles at 2%, not zero, not thirty.

The cost of settling an [embedding auction](/power-diagrams-ad-auctions) is nearly free. Evaluate N scores, pick the max, compute the [VCG price](/one-shot-bidding). Much like credit card companies, actual costs incurred by the exchange are everything around it: onboarding, engineering, customer support. So in theory: an embedding exchange should charge 2%, in the absence of information asymmetry.

## Transparency

User queries must stay private. That means someone else has to declare their position for matching to work. Google has it backwards: the user's search is exposed to advertisers, while advertiser targeting stays opaque. The [embedding model](/three-levers) flips this. User queries stay inside the [TEE](/monetizing-the-untouchable). Advertisers declare their [center and σ](/buying-space-not-keywords) publicly.

But there's no privacy reason for σ to be public, so it stays hidden inside the exchange. Only the TEE needs it at auction time. But advertisers collectively benefit if σ is public. [Milgrom & Weber (1982)](https://doi.org/10.2307/1911865) proved that in auctions with correlated values, revealing more information reduces the winner's curse and defensive overbidding. A specialist with tight σ is visibly not competing on a generalist's turf. No need to bid defensively. Without visible σ, everyone assumes worst-case competitor reach and [overbids](/keyword-tax). Public σ is a de-escalation signal, a credible commitment to territory size.

"Market positioning" has always been a metaphor. Here, your position is a coordinate. The metaphor becomes the mechanism.

If centers and σ are visible, the map is the analytics. Keyword Planner, auction insights, competitor research tools, bid simulators all go away. These are transaction costs in the [Coasean](https://doi.org/10.1086/466560) sense: they exist only because information is hidden. Remove the hiding, remove the cost.

Visible σ makes predatory positioning a public act. Opacity is what lets predation work. In keyword auctions, you don't know who's bidding on your terms until you've lost.

## One-Way Gate

Suppose the first exchange keeps σ private. Advertisers cannot see each other's reach. Parasitic startups appear to solve non-problems created by the opacity. Switching costs accumulate. The fog becomes the business model. Sound familiar?

The entirety of the adtech industry that grew around it now resists transparency because its revenue depends on the fog. For example, [attested attribution](/attested-attribution) has been commodity technology for years. Any exchange could have proven that its auctions were honest. None did.

Now suppose the first exchange publishes σ. Transparency becomes a product requirement for all who come after. Later entrants cannot claw it back without breaking trust. Collusion on opacity requires a first mover willing to set that precedent.

Transparency is a one-way gate. It's the difference between 30% and 2%.

## No Moat

With transparency, no exchange has a moat. The scoring function is attested, σ is public, and fees are epsilon-Nash. The exchange is a pipe.

Advertiser positions are public. Any new exchange can bootstrap by importing the entire advertiser landscape on day one. Advertisers don't re-onboard. Their declarations are portable. The exchange that misbehaves loses its supply side overnight.

If declarations are portable, why would each exchange maintain its own copy? Every duplicate is friction. Every sync protocol is overhead. Exchanges competing on reducing friction converge on a single source of truth for every entity's center and σ. The advertiser updates their position once and every exchange resolves it. The registry does not live inside an exchange. It's a phonebook.

Every legitimate commercial entity already has a domain. The spec writes itself: `example.com/marketing-position.json`. Center, σ, geolocation if applicable.
Keywords were never portable. A Google Ads campaign does not translate to Meta or Amazon. An embedding and σ are platform-agnostic.

## Market Expansion

[Coase (1960)](https://doi.org/10.1086/466560): in the absence of transaction costs, efficient allocation is guaranteed. Remove opacity, and the infrastructure becomes fintech: a payment rail with extra math.

The full cost is exclusionary. Every business that cannot justify 30% plus the consulting stack simply does not advertise. Stripe enabled an entire generation of businesses that could not have existed when payment processing required a merchant account and a sales call.

It's not just that 30% becomes 3% as a nice discount. It's that every specialist with a tiny budget can reach their exact audience. Every niche publisher with 10,000 users can monetize without an ad sales team. A business anywhere can reach a customer anywhere.

## Inevitable

This is a prophecy.

[Vickrey (1961)](https://doi.org/10.2307/2977633): truthful mechanisms make strategy unnecessary. [Milgrom & Weber (1982)](https://doi.org/10.2307/1911865): transparency reduces defensive bidding. [Aurenhammer (1987)](https://doi.org/10.1137/0216006): power diagrams partition space in any dimension. The theory was available for sixty years. Market positions represented as embeddings in a continuous vector space made the application real.

For every time in protocol history, open won against closed. TCP/IP over proprietary networks. SMTP over CompuServe. HTTP over AOL. The pattern repeats because the economics are the same: when the value is in the connection, not the intermediary, open protocols outcompete closed platforms on reach. The intermediary's margin is the tax on the connection. Remove the extortion, keep the connection.

The academics were prophets. This blog is the poem. The builder will follow. You now carry this knowledge. So does everyone else reading this. That's common knowledge, and now starts the race.

---

*Part of the [Vector Space](/vector-space) series.*
