# Exchange Fees

How much can/should the exchange charge?

## Reference Points

- Stock exchanges: fractions of a penny. Competitive, commoditized, regulated.
- Google Ads: ~30-35%. Monopoly distribution.
- App stores: 30%. Distribution monopoly.
- Stripe: 2.9% + 30c. Competitive, low switching cost, reflects infrastructure cost.

## Where the Costs Actually Are

- The auction itself is nearly free: evaluate N scores, pick max, compute VCG price
- The real costs are transaction costs between the exchange and its players, not between advertisers and publishers
- Onboarding, integration, payment processing, support, compliance — all exchange-to-player friction
- Advertiser never talks to publisher. Every interaction passes through the exchange.
- Google's 30% reflects handling all of that friction. Reduce the friction, reduce the floor.
- Exchanges are incentivized to reduce friction further: lower friction → more advertisers → more liquidity → better auctions → more publishers → flywheel
- Onboarding and integration costs get amortized across volume. The exchange that makes signup easiest wins the liquidity race.
- Competition doesn't drive fees to marginal cost — it drives them to what the market tolerates
- Credit card processing costs fractions of a penny. Visa/MC/Amex all charge 2-3%. Decades of "competition." Fee never collapsed.
- Stripe: 2.9% + 30c is orders of magnitude above marginal cost, but low enough that nobody switches to save a fraction of a percent
- Fees settle where the pain of paying < pain of switching
- Fixed costs (infra, compliance, engineering) need covering, and fee is small relative to transaction value
- So: exchange fee won't be "cost of TEE computation" (basically free). It'll be a few percent, like payment processing.
- Equilibrium take rate should look like Stripe (2-3%), not Google (30%). Not marginal cost (0.01%), not monopoly rent.
- This is epsilon-Nash: no exchange can improve its position by more than ε by deviating. Cutting fees 0.5% doesn't win enough share to offset revenue loss. ε = switching cost + inertia.
- Explains why Visa and Stripe coexist at similar prices. Why the fee settles at 2-3%, not zero, not thirty.
- What about rent extraction through the scoring function? We showed in Three Levers that log(b) is an inflationary tax the exchange keeps. An exchange that controls the compression function would keep changing it to reset σ adaptation. The fee isn't the only way to extract rent — the rules are.
- But log(b) can only move in one direction, and every advertiser sees their costs change for the same allocation. In a transparent system with TEE attestation, the scoring function is published code. Changing it is a public act. The exchange can't hide it any more than a predator can hide a wide σ.

## The Fee Is the Wrong Question

- 2-3%. Done. The fee question is answered.
- The harder question: what does the exchange publish?
- Three-number input (center, σ, bid) → minimal onboarding cost
- TEE attestation → no trust disputes to adjudicate
- But what about σ? That's where it gets interesting.

## What the Exchange Can See

- Advertiser centers are PUBLIC — storefront signs, "I serve these customers"
- Bids are partially revealed through VCG pricing (you learn what you pay, which leaks info about competitors)
- User/publisher query embeddings are PRIVATE — TEE protects these
- σ (reach) is PRIVATE by default — only the TEE needs it at auction time
- But advertisers would likely choose to publish it: σ IS the positioning statement
- Tight σ = "I specialize" — a credibility signal. Wide σ = "I serve broadly" — also a marketing message.
- Competitors benefit from seeing each other's σ: it's a de-escalation signal
- Climbing PT publishes σ=0.30 → sports PT sees "they're not on my turf" → no need to bid defensively
- Without visible σ, everyone assumes worst-case competitor reach and overbids (the keyword problem restated)
- Public σ is a credible commitment to territory size. Reduces wasted spend for everyone.
- Exchange doesn't force transparency — advertisers volunteer it because it helps them AND their competitors
- Counterargument: visible σ enables predatory positioning — generalist sees tight σ, widens to surround you
- But it goes both ways: predatory positioning is a public act. You see it. Other specialists see it. The next exchange sees it.
- Opacity is what lets predation work — in keywords you don't know who's bidding on your terms until you've lost
- Visible σ means the predator can't hide
- Kills the analytics industry: Keyword Planner, auction insights, competitor research tools, bid simulators — all exist to reverse-engineer hidden targeting. If centers and σ are visible, the map IS the analytics.
- Advertiser looks at the landscape, sees gaps, positions accordingly. No consultant needed.

## Path Dependence

- Whether σ is public depends on the first mover's design choice
- If first exchange publishes σ: transparency becomes the norm, later entrants can't take it back
- If first exchange keeps σ private: analytics layer builds around opacity, creates its own switching cost
- If the first exchange is transparent, competitors must match or lose advertisers
- If the first exchange is opaque, later entrants can collude on opacity — "nobody publishes σ" becomes the Nash equilibrium
- Collusion on opacity only works if the first mover sets the precedent. A transparent first mover makes collusion impossible — you can't un-publish what advertisers already expect to see.
- Transparency is a one-way gate. Once open, no one can close it.
- Google chose opacity. An entire consulting industry grew to fill the gap — agencies, tools, certifications, careers. Billions of dollars of economic activity that didn't have to exist. An industry that now resists transparency because its revenue depends on the fog. All of it is an artifact of a design choice someone made once and never revisited.

## The Full Stack, Side by Side

Opaque exchange (Google Ads today):
- 30% take rate
- Agency management fees: 15-20% of spend
- Bid management software: $500-2000/mo
- Keyword research tools: $100-500/mo
- Analytics platforms to interpret opaque signals
- Consultants to operate all of the above
- Smart Bidding: a black box you pay to not understand
- Advertiser can't see competitor targeting, can't verify auction integrity
- Total cost: 30% + layers of fees to navigate the opacity

Transparent attestable exchange:
- 2-3% take rate (epsilon-Nash)
- No agency needed: three inputs (center, σ, bid)
- No bid optimizer needed: VCG is truthful, one-shot
- No keyword research: the map IS the analytics
- No consultant: visible landscape, position yourself
- TEE attestation: auction is verifiable, no trust disputes
- Total cost: 2-3%. That's it.

The opaque model isn't a market — it's rent extraction with market aesthetics. Every agency, tool, and consultant exists to navigate artificial complexity the exchange created. They're not adding value. They're paying to see through fog that someone manufactured.

The transparent model is a free market in the classical sense: visible supply, visible prices, verifiable clearing, low transaction costs. The invisible hand works when you can see the hands.

## No Moat

- With transparency, no exchange has a moat. Scoring function is attested. σ is public. Fees are epsilon-Nash. The exchange is just a pipe.
- Advertiser positions are public. Any new exchange can bootstrap by importing the entire advertiser landscape on day one. Advertisers don't need to re-onboard — their declarations are portable.
- Zero switching cost for advertisers. The exchange that misbehaves loses its supply side overnight.
- Inevitably consolidates into a shared registry: one source of truth for every entity's center and σ. Exchanges don't want to maintain separate copies or sync state — that's friction, and they're racing to reduce friction.
- Advertiser updates position once, every exchange sees it. The registry isn't an exchange. It's a phonebook.
- Stock exchanges ended up here: NYSE and NASDAQ compete on speed and reliability, not proprietary mechanics. They're utilities.
- If there's no moat, who builds the first one? No venture-scale returns in commodity infrastructure.
- Maybe the exchange isn't a company. Maybe it's a protocol.
- The moat belongs to the advertisers (positioning, conversion advantage) and the publishers (audience). Not the pipe between them.
- The registry is the protocol. The exchanges are just execution nodes.
- DNS for advertising identity. Advertiser registers center and σ once. Any exchange can resolve it. Exchanges compete on query volume, latency, and fee. They're interchangeable.
- DNS took decades to become invisible infrastructure nobody thinks about. Same trajectory.
- Embeddings and σ are lightweight, portable, translatable. Like domain names: tiny, cheap to replicate, meaningful enough that everything else depends on them.
- Keywords were never portable. A Google Ads campaign doesn't translate to Meta or Amazon — different taxonomies, match types, quality scores. Rebuild from scratch. An embedding and σ are platform-agnostic. Same position means the same thing on every exchange.
- The protocol doesn't need an industry lobby (IAB has 698 categories nobody uses correctly). It needs an RFC and a version tag. The spec is the scoring function. The registry is the phonebook. Everything else is execution.

## Adtech Margins Collapse into Fintech Margins

- Coase (1960): in the absence of transaction costs, efficient allocation is guaranteed
- Opacity creates transaction costs (consulting, analytics, bid optimization)
- Transaction costs prevent efficient allocation (keyword tax, specialists priced out)
- Remove them (transparency, attestation, published scoring function) and efficient allocation follows (VCG, power diagrams, one-shot bidding)
- The 30% margin isn't a fee for a service — it's the cost of the transaction costs
- Adtech charges 30% because opacity justifies a service industry
- Fintech charges 2-3% because the protocol is transparent and the pipe is commoditized
- The only difference is how much information the intermediary hides
- Collapse the transaction costs to near zero and the margin follows
- The infrastructure becomes fintech: moving money from advertiser to publisher through a verifiable scoring function is a payment rail with extra math
- But it's not just a discount for existing advertisers. The 30% + consulting stack is exclusionary. Every business that can't justify the total cost simply doesn't advertise.
- At 2-3% with no analytics layer, the math changes for millions of small businesses — the long tail that was priced out entirely
- Stripe didn't just make payments cheaper for existing merchants. It enabled an entire generation of businesses that couldn't have existed when payment processing required a merchant account and a sales call.
- Same trajectory. Lower transaction costs don't just redistribute surplus — they expand the market.
- It's not that 30% becomes 3%. It's that the climbing PT with a $200/month budget can reach her exact patients. A niche publisher with 10,000 users can monetize without an ad sales team. Every long-tail business and long-tail publisher that currently can't participate suddenly can.
- The margin collapse is the mechanism. The market expansion is the story.

## Closing

- This isn't a proposal. It's a prediction.
- Coase (1960): remove transaction costs, efficient allocation follows. Vickrey (1961): truthful mechanisms make strategy unnecessary. Aurenhammer (1987): power diagrams partition space in any dimension.
- The theory has been predicting this for sixty years. Embeddings just made the application real.
- The series isn't proposing something new. It's pointing at something inevitable.
- The academics were prophets. The blog is the poem. The builder will follow.

## Open Thread

- Historical precedent: did stock exchanges stay neutral or did they find ways to extract rent? (payment for order flow, dark pools)
- If the exchange is a protocol, who governs it? Who updates the scoring function? Who sets the fee?
