---
layout: post
title: "Aligned Greed"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

The question isn't how to make platforms behave. It's how to set up material conditions such that their greedy behavior is aligned with ours.

This is mechanism design — designing a game where the selfish move is the fair move.

## Three Kinds of Greed

**Google: low resolution, misaligned.** [$265 billion in annual ad revenue](https://abc.xyz/assets/77/e1/69d1fbc74c26b6b4813d14b7b501/2025q4-alphabet-10k.pdf). Every design choice that increases time-on-platform increases revenue. Every link that sends you elsewhere is lost monetization. Google's greed is perfectly aligned — with Google.

**Meta: high resolution, misaligned.** Behavioral targeting builds a richer model of you than any single query can — interests, demographics, purchase history, social graph, years of activity. Resolution is revenue. But their resolution comes from surveillance. The precision is real. The mechanism is extractive.

**Perplexity: high trust, broke.** [Killed ads](https://www.macrumors.com/2026/02/18/perplexity-abandons-ai-advertising/) in February 2026. Total ad revenue: [$20,000](https://digiday.com/media/perplexitys-ad-business-hasnt-exactly-been-a-hit/). First-party ads destroyed user trust. Correct diagnosis, wrong conclusion — the problem was the architecture, not the advertising.

## Why Regulation Can't Fix This

The DOJ [proved](https://www.justice.gov/opa/pr/department-justice-prevails-landmark-antitrust-case-against-google) Google monopolized ad tech. The EU fined them billions. Five SSPs filed private suits. Google's ad revenue keeps growing.

Regulation can punish specific bad behavior — [Project Bernanke's](https://www.techpolicy.press/how-google-manipulated-digital-ad-prices-and-hurt-publishers-per-doj/) hidden bid manipulation, demand steering through Project Poirot. But regulation can't make good behavior profitable. A fine is a cost of doing business when the business makes $265 billion.

If the greedy move is the extractive move, regulation is whack-a-mole. The game theory doesn't change because you penalized one round.

## Aligned by Construction

An embedding auction aligns greed differently — by making the profitable move the fair move.

**For the exchange:** Revenue comes from clearing volume — more matches, more auctions, more revenue. Unlike keyword auctions, where revenue maximizes by cramming everyone into the same bin and driving up bids, embedding auctions [generate more total surplus](/keyword-tax) when specialists spread out to their niches. The exchange earns more when matches are better.

**For the advertiser:** The [scoring function](/power-diagrams-ad-auctions) is `score = log(bid) - distance² / σ²`. Proximity reduces the bid needed to win. Lying about what you do pushes your position away from the queries you convert on — you win irrelevant impressions and waste money. The greedy move is to describe yourself accurately.

**For the chatbot platform:** This is where Perplexity's story inverts. With [TEE-sealed auctions](/perplexity-was-right-to-kill-ads), the chatbot doesn't select ads and can prove it cryptographically. The same company that had to choose between trust and revenue no longer faces the choice. The protocol makes monetization and trust compatible. Perplexity's greed — fund inference, grow the product — aligns with user trust instead of opposing it.

**For the customer:** You say what you need. The auction matches it to someone who does that thing. No tracking, no behavioral profiles, no cookies. Embeddings can't match Meta's depth on *who you are* — Meta has years of behavioral data and it's genuinely richer than a single query. But embeddings capture *what you need right now* with a precision keywords never could, and they do it from what you volunteered, not what was collected.

## The Resolution Tradeoff

Meta's insight was correct: resolution is revenue. Embeddings trade off on a different axis — shallower on the individual, but operating on declared intent rather than inferred behavior. A single query carries less information than Meta's full profile, but it carries the most important information: what this person wants, right now, in their own words.

The [Plumber Test](/the-plumber-test) is the concrete version: "sewage backup residential basement Bloomington" contains enough signal to match the right specialist without knowing the customer's age, income, or browsing history. Whether embeddings can match Meta's raw precision is open. Whether they beat keywords is not — keywords are a [special case](/keywords-are-tiny-circles) of embeddings with zero radius.

## The Profit Motive

Intentcasting — where people declare what they need and let the market come to them — has been talked about for years. The vision is right. But vision without a profit motive is a blog post, not a business.

The embedding auction is the business model that makes intentcasting viable. An exchange earns on every matched query. A chatbot monetizes without compromising trust. An advertiser converts at higher rates and lower cost. Perplexity gets to keep its product integrity *and* fund inference.

Intentcasting stalled because there was no protocol that made it profitable for every participant simultaneously. The embedding auction is that protocol.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
