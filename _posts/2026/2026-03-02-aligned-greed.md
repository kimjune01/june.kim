---
layout: post
title: "Aligned Greed"
tags: vector-space
image: "/assets/aligned_greed.png"
---

![Aligned forces](/assets/aligned_greed.png)

Google makes $265 billion a year in ad revenue. They aren't going to stop being greedy. Neither is Meta, neither is OpenAI. The interesting question is whether a system exists where their greed produces good outcomes. Mechanism design is the field that studies this: how to build games where the selfish move is the fair move.

## What Greed Looks Like Now

Google's [revenue](https://abc.xyz/assets/77/e1/69d1fbc74c26b6b4813d14b7b501/2025q4-alphabet-10k.pdf) comes from keeping people on Google. Every link that sends you somewhere else is lost monetization, and design choices that increase time-on-platform increase revenue. Their greed is perfectly aligned with their own interests alone.

Meta built a richer model of you than any single query can capture: interests, demographics, purchase history, social graph, years of activity. The precision is real, built on surveillance. Resolution is revenue, and their resolution comes from collecting everything you do across the web.

Perplexity [killed ads](https://www.macrumors.com/2026/02/18/perplexity-abandons-ai-advertising/) in February 2026 after total ad revenue of [$20,000](https://digiday.com/media/perplexitys-ad-business-hasnt-exactly-been-a-hit/). First-party ads destroyed user trust. They diagnosed the problem correctly (ads feel intrusive) but drew the wrong conclusion (stop advertising). The architecture was broken.

## The Limits of Regulation

The DOJ [proved](https://www.justice.gov/opa/pr/department-justice-prevails-landmark-antitrust-case-against-google) Google monopolized ad tech. The EU fined them billions. Five SSPs filed private suits. Google's ad revenue keeps growing. Regulation can punish specific bad behavior, like [Project Bernanke's](https://www.techpolicy.press/how-google-manipulated-digital-ad-prices-and-hurt-publishers-per-doj/) hidden bid manipulation or demand steering through Project Poirot. Making good behavior profitable is outside its scope. A fine is a cost of doing business when the business makes $265 billion.

The underlying problem is structural: if the greedy move is the extractive move, enforcement is whack-a-mole. You penalize one tactic and the next one appears. The game theory doesn't change between rounds.

## How Embedding Auctions Change the Incentives

An embedding auction makes the profitable move the fair move. The mechanism is different for each participant, and worth tracing through.

The exchange earns revenue from clearing volume: more matches means more fees. In keyword auctions, revenue maximizes when everyone is crammed into the same bin and bids escalate. In embedding auctions, the [simulation data](/keyword-tax) shows total surplus increases when specialists spread out to their niches. The exchange earns more when matches are better, because better matches mean more active advertisers willing to participate.

The advertiser faces a [scoring function](/power-diagrams-ad-auctions): `score = log(bid) - distance² / σ²`. Proximity reduces the bid needed to win. Lying about what you do pushes your position away from the queries you actually convert on, so you win irrelevant impressions and waste money. Describing yourself accurately is the profit-maximizing strategy.

This is where Perplexity's story inverts. With [TEE-sealed auctions](/perplexity-was-right-to-kill-ads), the chatbot doesn't select ads and can prove it cryptographically. The same company that had to choose between trust and revenue no longer faces the choice. Perplexity's incentive (fund inference, grow the product) aligns with user trust directly.

The customer says what they need. The auction matches it to someone who does that thing, based on what the customer volunteered, without tracking or behavioral profiles.

## The Resolution Tradeoff

Meta's insight was correct: resolution is revenue. Embeddings are shallower on the individual but operate on declared intent. A single query carries less information than Meta's full profile, but it carries the most important information: what this person wants, right now, in their own words.

The [Plumber Test](/the-plumber-test) is the concrete version: "sewage backup residential basement Bloomington" contains enough signal to match the right specialist without knowing the customer's age, income, or browsing history. Whether embeddings can match Meta's raw precision is open. They already beat keywords — keywords are a [special case](/keywords-are-tiny-circles) of embeddings with zero radius.

## The Profit Motive

Intentcasting (where people declare what they need and let the market come to them) has been talked about for years. Doc Searls proposed it in 2006. The vision is right. The reason it stalled is that nobody built a protocol that made it profitable for every participant simultaneously.

The embedding auction might be that protocol. The exchange earns on every matched query, the chatbot monetizes without compromising trust, and the advertiser converts at higher rates and lower cost. Whether this is enough to bootstrap a market is an open question. But the alignment is structural: every participant's greedy move produces the outcome the other participants want.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
