---
layout: post
title: "Room to Exist"
tags: vector-space
image: "/assets/room_to_exist.png"
---

![Room to exist](/assets/room_to_exist.png)

Keywords are a bottleneck. Structurally. A dozen auto shops bid on "mechanic near me." The auction can't distinguish the BMW transmission specialist from the classic car restorer from the hybrid battery shop. The [keyword tax](/keyword-tax) showed this quantitatively: specialists lose 3.5x more per round than generalists (-0.807 vs -0.233).

## The Bottleneck

Consider auto repair in a mid-sized city. There might be thirty shops: transmission, European imports, classic restoration, hybrid/EV, diesel, body work, performance tuning, fleet maintenance, off-road, marine engines, motorcycle, alignment, paint correction, and more. Thirty distinct services. Car owners have specific problems. The market *should* have room for all of them.

Google Ads offers them maybe four keyword bins: "auto repair," "mechanic near me," "car shop," "body shop." Thirty shops, four bins. The auction is dense because the categories are coarse. CPCs rise until only the best-capitalized shops (usually national chains like Midas, Jiffy Lube, or Caliber Collision) can afford to stay. In a [recent industry poll](https://searchengineland.com/small-businesses-compete-google-ads-462009), more than 50% of respondents said small businesses have been priced out of Google Ads entirely.

The independent shop that specializes in vintage Porsche air-cooled engine rebuilds has no keyword that describes what he does. "Auto repair" goes to Midas. "Porsche repair" is a smaller bin, but still shared with dealerships, general European shops, and parts retailers. Every available keyword is too coarse, so the specialist always overpays.

Discrete categorization works this way. Keywords are finite bins, but expertise is continuous. Forcing continuous variation into discrete bins compresses the space and concentrates competition, so the businesses that survive are the best-capitalized, regardless of relevance.

## Removing the Bottleneck

Embedding space is continuous. The vintage Porsche specialist positions at the point in high-dimensional space that represents exactly what he does; the hybrid battery shop positions somewhere else entirely. They don't compete because they aren't close.

When a user tells a chatbot "my 1987 911 Carrera is losing oil pressure and the engine sounds like it's knocking at high RPM," that query lands in embedding space near the air-cooled Porsche specialist, far from the hybrid shop or Midas. The [scoring function](/power-diagrams-ad-auctions) is `score = log(bid) - distance² / σ²`. Proximity dominates. The specialist wins by being closer to the problem he actually solves.

The [simulation](/keyword-tax) measured this directly. With embedding auctions and [relocation fees](/synthetic-friction), specialist surplus goes from -0.807 (losing money every round) to +0.021 (profitable). Win diversity rises from 0.809 to 0.876 — different specialists win different queries instead of one dominant bidder sweeping the bin.

The mechanism just removes the bottleneck. More businesses survive as a result.

## Why Chatbots Change the Math

The strongest objection is that most queries are generic. People search "mechanic near me." If queries stay that vague, embeddings have nothing to differentiate on.

But chatbot queries differ from search queries. The [Ask First](/ask-first) UX shows why: each conversational turn produces a new embedding. "My car is making a knocking sound" → "it's a 1987 Porsche 911" → "the oil pressure drops at high RPM." Three turns, three positions in embedding space, each more specific than any keyword. The interface *elicits* specificity. People talk to chatbots the way they talk to a friend: with detail and follow-up.

The keyword bottleneck persists partly because search boxes train users to compress their intent into two or three words. Chatbots undo that compression. When the input is a paragraph instead of a phrase, the embedding carries enough signal to match the right shop.

## Why the Space Stays Open

A continuous space with better differentiation is worth nothing if large players can just occupy all the niches. What stops Midas from creating thirty embedding positions and capturing every niche query?

[Stay or Pay](/stay-or-pay) addresses this with mechanisms borrowed from markets that already work. Position history follows a hashed payment credential across exchanges, so spinning up shell accounts requires separate verified identities and separate bonds for each. Refundable entry deposits make each new identity expensive: one bond for one shop is a temporary cost, but thirty bonds for thirty fake identities is permanent capital drain. Coordinated resets by related accounts cost quadratically (borrowed from Ethereum's proof-of-stake slashing), so five simultaneous resets cost 25x.

The economics of niche-squatting don't work when each occupied position requires a verified identity and a locked bond. A chain could legitimately operate thirty locations with thirty specialties, and if each location genuinely serves that niche, the mechanism is working as designed. What breaks is the keyword-era strategy of occupying positions you don't actually serve.

## What This Means

Chains will still exist and capital advantages don't disappear, but the advertising layer stops being the bottleneck that forces consolidation. The air-cooled Porsche specialist reaches the customers who need him at a price that reflects proximity to the query.

Whether this actually produces a more diverse market is an empirical question. The [simulation data](/keyword-tax) suggests yes: specialist surplus goes positive and win diversity increases. But a simulation with 25 advertisers is far from a market with thousands of participants. The mechanism creates room. Whether businesses fill it depends on factors the auction can't control.[^1]

[^1]: Socialists correctly diagnose that wealth concentrates. Their fix is redistribution, which requires authority to decide who gets what. The embedding auction reaches a similar destination through voluntary exchange: specialists position accurately because it's profitable, and exchanges enforce fees because it attracts better inventory. The outcome is broader because the mechanism is better.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
