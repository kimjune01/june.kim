---
layout: post
title: "Room to Exist"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

Keywords are a bottleneck. Not metaphorically — structurally. Every advertiser who does a version of the same thing competes in the same bin. A dozen auto shops bid on "mechanic near me." The auction can't distinguish the BMW transmission specialist from the classic car restorer from the hybrid battery shop. They all pay the same inflated price for the same undifferentiated slot.

The result is predictable. The biggest bidder wins. The [keyword tax](/keyword-tax) showed this quantitatively: specialists lose 3.5x more per round than generalists in keyword auctions (-0.807 vs -0.233). Small shops with narrow expertise subsidize the auction with money they'll never earn back, because the bin forces them to compete on queries they'll never convert.

This is how market power concentrates through ad infrastructure. Not through conspiracy. Through compression.

## The Bottleneck

Consider auto repair in a mid-sized city. There might be thirty shops: transmission, European imports, Japanese imports, classic restoration, hybrid/EV, diesel, body work, performance tuning, fleet maintenance, off-road, marine engines, motorcycle, alignment, paint correction, audio installation. Thirty distinct services. Car owners have specific problems. The market *should* have room for all of them.

Google Ads offers them maybe four keyword bins: "auto repair," "mechanic near me," "car shop," "body shop." Thirty shops, four bins. The auction is dense by construction. CPCs rise until only the best-capitalized shops — usually national chains like Midas, Jiffy Lube, or Caliber Collision — can afford to stay. In a [recent industry poll](https://searchengineland.com/small-businesses-compete-google-ads-462009), more than 50% of respondents said small businesses have been priced out of Google Ads entirely.

The independent shop that specializes in vintage Porsche air-cooled engine rebuilds has no keyword that describes what he does. He bids on "auto repair" and loses to Midas. He bids on "Porsche repair" — a smaller bin, but still shared with dealerships, general European shops, and parts retailers. The bin is always too coarse. The specialist always overpays.

This isn't a failure of Google's implementation. It's a property of discrete categorization. Keywords are finite bins. Expertise is continuous. When you force continuous variation into discrete bins, you compress the space and concentrate competition. The businesses that survive are the ones that can afford to win generic auctions — which means the ones with the most capital, not the most relevant service.

## Removing the Bottleneck

Embedding space is continuous. There are no bins. The vintage Porsche specialist positions at the point in high-dimensional space that represents exactly what he does. The hybrid battery shop positions somewhere else entirely. They don't compete because they aren't close.

When a user tells a chatbot "my 1987 911 Carrera is losing oil pressure and the engine sounds like it's knocking at high RPM," that query lands in embedding space near the air-cooled Porsche specialist — not near the hybrid shop, not near Midas. The [scoring function](/power-diagrams-ad-auctions) is `score = log(bid) - distance² / σ²`. Proximity dominates. The specialist wins not by outbidding, but by being closer to the problem he actually solves.

The [simulation](/keyword-tax) measured this directly. With embedding auctions and [relocation fees](/synthetic-friction), specialist surplus goes from -0.807 (losing money every round) to +0.021 (profitable). Win diversity rises from 0.809 to 0.876 — different specialists win different queries instead of one dominant bidder sweeping the bin.

More winners. More viable businesses. Not because the mechanism redistributes anything, but because it stops compressing the space.

## Why Chatbots Change the Math

The strongest objection is that most queries are generic. People search "mechanic near me," not "air-cooled Porsche engine rebuild specialist." If queries are generic, embeddings don't help — there's nothing to differentiate on.

But chatbot queries aren't search queries. The [Ask First](/ask-first) UX shows why: each conversational turn produces a new embedding. "My car is making a knocking sound" → "it's a 1987 Porsche 911" → "the oil pressure drops at high RPM" → "I think it might need an engine rebuild." Four turns, four positions in embedding space, each more specific than any keyword. The interface *elicits* specificity. People talk to chatbots the way they talk to a friend — in detail, with context, with follow-up.

This is the variable that changes everything. The keyword bottleneck persists partly because search boxes train users to compress their intent into two or three words. Chatbots undo that compression. When the input is a paragraph instead of a phrase, the embedding carries enough signal to distinguish thirty types of auto shop. The bottleneck dissolves because the queries are finally as specific as the expertise.

## Why the Space Stays Open

A continuous space with better differentiation is worth nothing if large players can just occupy all the niches. What stops Midas from creating thirty embedding positions and capturing every niche query?

[Stay or Pay](/who-pays-the-fee) addresses this with three mechanisms, each borrowed from markets that already work:

**Identity binding.** Position history follows a hashed payment credential across exchanges. You can't spin up shell accounts without separate verified business identities, separate payment credentials, and separate bonds.

**Entry bonds.** Refundable deposits that make each new identity expensive. One bond for one shop is temporary cost. Thirty bonds for thirty fake identities is permanent capital drain — and triggers correlation penalties.

**Correlation penalties.** Borrowed from Ethereum's proof-of-stake slashing: coordinated resets by related accounts cost quadratically. Five simultaneous resets don't cost 5x. They cost 25x.

The economics of niche-squatting don't work when each occupied position requires a verified identity, a locked bond, and tenure to earn fee discounts. A chain could legitimately operate thirty locations with thirty specialties — and if each location genuinely serves that niche, the mechanism is working as designed. What it prevents is occupying positions you don't actually serve, which is the keyword-era strategy of bidding on everything and converting on nothing.

## What This Means

In keyword markets, the number of viable competitors is bounded by the number of bins and the depth of your budget. In embedding markets, the number of viable competitors is bounded by the diversity of real expertise.

A city with thirty distinct types of auto shop can support thirty distinct advertisers — each profitable on their own niche queries, none needing to outbid a chain on a generic keyword. The independent specialist who rebuilds air-cooled Porsche engines can reach the exact customers who need him, at a price that reflects his proximity to the query, not his ability to outspend Midas.

This isn't a utopian claim about ending market concentration. Chains will still exist. Capital advantages don't disappear. But the advertising layer — the mechanism that connects demand to supply — stops being the bottleneck that forces consolidation. When the marketplace has room for thirty competitors instead of four, more businesses survive. When more businesses survive, more people build them. The value created by thirty specialists serving thirty niches is greater than the value extracted by four generalists fighting over one bin.

The mechanism doesn't redistribute wealth. It creates room for more of it to exist.[^1]

[^1]: Socialists correctly diagnose that wealth concentrates. Their fix is redistribution — which requires authority to decide who gets what, enforced by compulsion. The embedding auction reaches the same destination through voluntary exchange: specialists position accurately because it's profitable, users tap because it's useful, exchanges enforce fees because it attracts better inventory. Nobody is compelled. The outcome is broader because the mechanism is better, not because anyone was forced.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
