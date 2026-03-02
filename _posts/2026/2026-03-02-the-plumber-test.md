---
layout: post
title: "The Plumber Test"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument from a reader's challenge; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

Doc Searls — the guy who wrote [*The Intention Economy*](https://doc.searls.com/2024/12/30/the-real-intention-economy/) — read [The Last Ad Layer](/the-last-ad-layer) and asked the question that matters:

> Sewage backed up into my basement in Bloomington, Indiana. I searched Google. Got Peterman Brothers — large plumbing outfit, diagnosed the problem, wanted $3,000. Checked with neighbors. Got local guys in a truck who knew their shit and fixed it for just hundreds. Would your system have made a better match?

Not whether embedding auctions are mathematically elegant. Not whether TEEs provide cryptographic guarantees. Whether the person with sewage in their basement finds the right plumber.

## Cattle Into Keyword Bins

Google returned Peterman Brothers because Peterman Brothers pays to be returned. They bid on "plumber Bloomington Indiana" and every variation of it. Their ad budget reflects their overhead — trucks with logos, dispatchers, upsell training, a marketing department. The $3,000 quote isn't gouging. It's the cost structure of a company that wins by being found first.

The guys with the truck don't bid on "plumber Bloomington Indiana." Their margins can't support it. A keyword click in the plumbing vertical costs [$30–80](https://www.wordstream.com/blog/ws/2022/04/19/google-ads-benchmarks). Convert one in ten clicks and your customer acquisition cost is $300–800. If your job averages a few hundred dollars, you're working for free before the first wrench turns.

This is the [keyword tax](/keyword-tax). The auction can't distinguish between a company that sends a sales team and a company that sends a plumber. It resolves on bid price. The company with the highest overhead wins because it has the highest margins to fund the highest bids.

The deeper problem is resolution. A keyword is a bin. "Plumber Bloomington" is a bin, and every query that matches those words gets sorted into it — sewage backups, water heater installations, bathroom remodels, gas line repairs. The auction doesn't see people with problems. It sees inventory sorted by label, sold to the biggest bidder.

The neighbors solved Doc's problem by routing around the auction entirely. Word of mouth. The oldest matching algorithm. It works, but it doesn't scale, and it doesn't help the person who just moved to Bloomington.

## Resolution Is the Variable

Meta figured out that higher resolution means higher revenue. Their behavioral targeting — interests, demographics, lookalike audiences, engagement patterns — tells advertisers *who you are*. Higher CTR, higher return on ad spend, more advertiser spending. But that resolution comes from surveillance. You get precision by watching everything someone does — not by understanding what they need right now.

An embedding is resolution on a different axis. Not *who you are* — *what you need*. "Sewage backup residential basement Bloomington" lands at a specific point in a high-dimensional space that captures the problem. You're not in a bin. You're at coordinates.

The guys with the truck can describe what they do: *residential sewer line repair and clearing, Bloomington Indiana, same-day service.* That maps to a point near Doc's problem.

Peterman Brothers does everything — new construction, water heaters, HVAC, remodels, commercial contracts. In an [embedding auction](/power-diagrams-ad-auctions), the score combines bid with proximity: `score = log(bid) - distance² / σ²`. The wider you spread, the farther you are from any specific query. A higher bid compensates for distance, but the geometry imposes a cost on generality that keywords never did.

The truck guys don't need to outbid Peterman Brothers. They need to be closer to the problem. And they are — because the problem is their entire business.

Meta's resolution comes from knowing everything about you. Embedding resolution comes from you stating what you need. Both are more precise than keywords. Only one requires surveillance.

## The Economics Flip

In keyword auctions, scale wins. More revenue means more ad budget means more visibility means more revenue. Flywheel favors consolidation.

In embedding auctions, specificity wins. The [simulation evidence](/keyword-tax) shows this: when specialists position at their niche instead of competing on a shared keyword, surplus redistributes from generalists to specialists. Proximity to the query is worth more than a higher bid from farther away.

This doesn't eliminate Peterman Brothers. They still win broad queries — "I need a plumber" with no other context. The mechanism distinguishes between "I need a plumber" and "sewage is backing up into my basement." Keywords can't. Embeddings can.

The guys with the truck compete on the queries where they convert. Modest budget, narrow radius, and they stop paying for clicks from people who need water heater installation.

## Passing the Test

Doc's plumber test has three criteria:

1. **Match quality.** The person with the problem finds someone who solves that specific problem — not the biggest company in the category.
2. **Cost to the customer.** The match doesn't route through a company whose overhead inflates the price.
3. **Cost to the provider.** The small operator can afford to be found without an ad budget that eats their margins.

Keyword auctions fail all three. An embedding auction addresses all three — not by favoring small businesses, but by scoring on proximity. The math compresses budget advantages logarithmically — a 10x bigger bid adds only ~2.3 to the score, which a closer specialist can overcome. What matters most is distance between what someone needs and what someone does.

The guys with the truck weren't invisible because they're bad at marketing. They were invisible because the auction had no resolution. It saw bins, not problems.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
