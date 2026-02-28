---
layout: post
title: "Adtech: The Keyword Tax"
tags: adtech
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument and designed the experiments; Claude built the simulation and drafted prose.*

*Part of the [adtech](/adtech) series.*

---

![The keyword tax — specialists crammed into one auction](/assets/11_egalitarian_auction.png)

Keywords herd traffic into a narrow, dense auction. Five physical therapists — a climbing specialist, a pelvic floor specialist, a pediatric specialist, a sports rehab specialist, and a generalist — all bid on "physical therapy." The auction can't tell them apart. 62 queries collapse into 4 bins. Each bin has 4–5 bidders fighting over every query. Dense competition, high clearing prices, maximum revenue extraction. This is what the publisher wants.

Embedding auctions decompress. Each advertiser plants a flag at a point in high-dimensional space that represents what they actually sell. The climbing PT positions at "physical therapy rehabilitation specializing in rock climbing finger pulley injuries." The pelvic floor PT positions at "pelvic floor postpartum." They stop competing with each other because the auction scores by proximity: `log(price) - distance² / σ²`. Each query has 2–3 effective competitors instead of 5. Sparser auctions, lower clearing prices, more surplus stays with advertisers.

Do embedding auctions let niche advertisers compete profitably on the queries they're best at — or do keywords already do that well enough? We built a keyword auction and an embedding auction and ran 50 randomized trials of each.

## The Simulation

Fifteen advertisers compete across 62 queries in a high-dimensional embedding space using real embeddings from [BGE-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5):

- **Physical therapy** (5): climbing PT, sports PT, pelvic floor PT, pediatric PT, general PT
- **Fitness coaching** (4): climbing coach, running coach, CrossFit coach, personal trainer
- **Nutrition** (4): sports dietitian, gut health specialist, weight loss coach, general nutritionist
- **Tutoring** (2): ADHD math tutor, general math tutor

Eleven are specialists — they chose a niche. Four are generalists who compete broadly. Specialists have narrow targeting radius (σ=0.30) and high max value (12.0) reflecting their conversion advantage. Generalists have wide radius (σ=0.55) and moderate max value (6.0). The 2x conversion ratio is an assumption, not a measurement — but a climber who finds the climbing PT books follow-up sessions and refers other climbers, while a climber who finds a general PT might not come back. The directional gap is real; the exact magnitude matters for effect size.

Two auction mechanisms:

- **Keywords.** Queries binned by cluster. Only advertisers in the matching cluster compete, on price alone. Today's market.
- **Embeddings.** Full `log(price) - dist²/σ²` scoring. Agents optimize bid, position, and σ. Tested with and without [relocation fees](/relocation-fees) penalizing drift from committed position.

The simulation code is [open source](https://github.com/kimjune01/openauction/tree/v3.4/cmd/simulate).

## Part 1: Would a Monopolist Switch?

What happens if a single publisher replaces their keyword auction with an embedding auction?

<table>
<tr><th>Metric</th><th>Keywords</th><th>Embeddings</th><th>Effect</th></tr>
<tr><td>Value efficiency</td><td>0.858 ± 0.015</td><td>0.793 ± 0.032</td><td>lower ¹</td></tr>
<tr><td>Win diversity</td><td>0.809 ± 0.016</td><td>0.833 ± 0.049</td><td>higher ²</td></tr>
<tr><td>Specialist surplus</td><td>-0.807 ± 0.280</td><td>-0.695 ± 0.329</td><td>inconclusive</td></tr>
<tr><td>Generalist surplus</td><td>-0.233 ± 0.411</td><td>-0.022 ± 0.129</td><td>higher ²</td></tr>
<tr><td>Avg surplus/round</td><td>-0.654 ± 0.200</td><td>-0.516 ± 0.238</td><td>higher ²</td></tr>
<tr><td><b>Publisher revenue/round</b></td><td><b>79.39 ± 1.72</b></td><td><b>72.82 ± 2.59</b></td><td><b>lower ¹</b></td></tr>
</table>

*50 trials per cell. Welch's t-test: ¹ p<0.001, ² p<0.01.*

Publisher revenue drops 8% — from 79.39 to 72.82 (p<0.001). That surplus goes to the advertisers instead. Generalists benefit most, going from -0.233 to nearly break-even at -0.022. Specialist surplus improves directionally (-0.807 to -0.695) but doesn't reach significance — more on that below.

### The keyword tax

In keywords, specialists lose 3.5x more than generalists (-0.807 vs -0.233 per round). The climbing PT pays to compete on "pelvic floor exercises after C-section." The pelvic floor PT pays to compete on "finger pulley injury from rock climbing." Neither will convert on the other's queries, but the keyword bin forces them into the same auction anyway.

This is the keyword tax. It's not a bug — it's the revenue model. Five competitors in every auction drives up clearing prices. The publisher captures 79.39 per round precisely because specialists are paying to compete on queries they'll never close.

### What embeddings fix

![Keywords collapse everyone to gray — embeddings let each specialist find their color](/assets/11_egalitarian_auction_dots.png)

Embeddings move surplus from the publisher to the advertisers. Win diversity improves from 0.809 to 0.833 (p<0.01) — different specialists win different queries instead of one dominant bidder sweeping the bin. The consumer who searches "finger pulley injury from rock climbing" finds the climbing PT, not whoever bid highest on "physical therapy."

Specialist surplus improves directionally but doesn't reach significance (-0.807 to -0.695, ns). Specialists are still losing money. The embedding mechanism helps — proximity scoring rewards niche positioning — but without [relocation fees](/relocation-fees), advertisers drift toward popular queries and the advantage erodes.

Adding relocation fees changes the picture. Specialist surplus goes from -0.695 to +0.021 (p<0.001). Specialists make money. Fees pin them at their niche, and their conversion advantage translates into winning the queries they're best at — at prices that leave positive surplus. Win diversity climbs further to 0.876. Value efficiency recovers to 0.834 — within 2.4pp of keywords.

### Why a monopolist wouldn't switch

Publisher revenue drops from **79.39** to **72.82** per round — an 8% cut. Dense keyword auctions extract more rent. The publisher is incentivized to *flatten* the distance penalty — widen σ, reduce the weight on distance — until the auction looks like keywords again. More competitors per query means higher clearing prices.

The publisher's optimal auction is `α = 0`: no distance weighting, everyone competes everywhere. That's keywords. The scoring formula has a distance weight parameter, and the publisher's incentive is to turn it all the way down. This is already visible in practice — Google keeps expanding broad match and deprecating exact match, making keyword bins vaguer and auctions denser. In a [recent industry poll](https://searchengineland.com/small-businesses-compete-google-ads-462009), more than 50% of respondents said small businesses have been priced out of Google Ads entirely. The incentive is to make matches *less* precise, not more.

A monopolist publisher would not adopt embedding auctions. Specialists have no outside option — they either pay the keyword tax or don't advertise.

## Part 2: What If a Competitor Offers Embeddings?

The simulation data from Part 1 also quantifies the switching incentive. If a competing exchange offers embedding auctions, every participant can compare their surplus:

<table>
<tr><th>Participant</th><th>Keywords (incumbent)</th><th>Embeddings + fees (competitor)</th><th>Switching gain</th></tr>
<tr><td><b>Specialists (11)</b></td><td><b>-0.807/round</b></td><td><b>+0.021/round</b></td><td><b>+0.828</b></td></tr>
<tr><td>Generalists (4)</td><td>-0.233/round</td><td>-0.052/round</td><td>+0.181</td></tr>
<tr><td>Publisher</td><td>79.39/round</td><td>67.23/round</td><td>-12.16</td></tr>
</table>

Specialists gain +0.828 per round — from losing money to making money. That's the switching incentive that bootstraps the competing exchange. Generalists gain too, but specialists gain 4.6x more. They switch first, they switch fastest, and there are 11 of them to 4 generalists. The competitor's marketplace bootstraps from the advertisers the incumbent is squeezing hardest.

### The distribution moat

But advertisers go where the users are. You can't run an ad auction without queries to auction. And getting queries means getting users, which means getting distribution.

Google pays Apple [$20 billion a year](https://www.theverge.com/2023/10/26/23933206/google-apple-search-deal-safari-18-billion) to be the default search engine on Safari. Users go to Google out of habit and defaults, not because keyword auctions produce better results. The queries flow to keyword auctions because the users flow to Google, and the users flow to Google because of a default payment that costs more per year than most companies are worth.

The keyword equilibrium is stable not because it's optimal, but because the moat is expensive to cross.

### Where the queries are going

AI chatbots already have the traffic. They just can't monetize it.

Perplexity, ChatGPT, Claude, Gemini — millions of queries, burning inference costs, no ad revenue. These queries are conversational: "my finger hurts after a climbing session, should I see a physical therapist?" That doesn't map to a keyword bid. There's no keyword to bid on when the query is a paragraph. But it maps to the climbing PT's position in embedding space.

![Keywords shout nothing — specialists with something to say get drowned out](/assets/11_keyword_megaphone.png)

Meanwhile, the advertisers are running out of places to go. As covered in [The Convergence](/the-convergence), organic CTR dropped 65% and paid CTR fell 68% on queries where AI Overviews appeared. Zero-click searches account for roughly 60% of queries. Search advertising is shrinking as a channel, and the specialists paying the keyword tax are the first to get priced out. They need somewhere else to advertise. The chatbots have the queries they'd pay to reach. The connection is missing.

### The missing piece

The long tail of chatbot platforms — vertical assistants, domain-specific tools, niche communities — doesn't exist yet, because there's no way to monetize conversational traffic. The SSP is the missing piece. An embedding auction that works across platforms would let any chatbot with a focused query stream sell ad inventory. The specialist revenue would be strongest on these long-tail platforms where every query is high-intent. The equilibrium isn't one big platform running embedding auctions — it's thousands of small ones, connected by a shared auction layer.

Whether embedding auctions generate enough revenue per query to offset inference costs is an open question. Perplexity tried keyword-style ads and abandoned them — $20K in total ad revenue. OpenAI projects $1B in 2026 from ads, against $14B in inference costs. The current ad formats are a poor fit for conversational queries. Embedding auctions might change the yield — higher relevance means higher conversion, which means advertisers pay more per impression — but that's speculation, not measurement.

The climbing PT who's losing -0.807 per round on Google keywords will buy ads on the platform where her niche queries actually exist, at prices where she breaks even. The keyword incumbent can't replicate this without cannibalizing their own revenue. The first embedding auction — whether on a major AI platform or a long-tail vertical — has a temporary monopoly on the only ad mechanism that works for conversational queries, and a built-in supply of the queries that specialists will pay to reach.

### What ships first will be wrong

The likely first implementation is RAG-based ad selection: embed the query, find the nearest ad embeddings by cosine similarity, show the top results. This is already how these platforms retrieve context — extending it to ads is a small step.

But RAG selection is a [Voronoi diagram](/power-diagrams-ad-auctions) — equal radius for every advertiser, no price integration, no mechanism for a specialist to say "I only want to compete on climbing queries" or for a generalist to say "I want to compete broadly." It reproduces the keyword problem at embedding resolution: instead of everyone bidding on the same keyword, everyone's embedding gets retrieved by the same cosine threshold. Better resolution, same structural flaw.

The [first post in this series](/power-diagrams-ad-auctions) argued that equal-weight Voronoi diagrams are insufficient — you need power diagrams, where each advertiser controls their own radius. The scoring formula `log(price) - dist²/σ²` is the power diagram formulation: price sets the weight, σ sets the radius, and the geometry determines who wins each query.

Whoever ships RAG ad selection first will discover what the simulation already shows: without per-advertiser σ, without price integrated into the scoring geometry, and without drift penalties, the embedding auction degrades. Specialists and generalists compete at the same radius. Aggressive bids override relevance. Positions drift toward popular queries. They'll add radius control, then price-integrated scoring, then relocation fees. They'll reinvent the power diagram auction one patch at a time.

## The Caveats

The 2x specialist conversion advantage drives the surplus story. When we ran the same simulation with a 1.25x ratio (v3.3), all surplus effects shrank to non-significance. The mechanism works at any ratio — specialists always do directionally better with embeddings — but whether the effect reaches significance depends on how much better specialists actually convert. The 2x ratio is plausible for a climbing PT vs a general PT on a climbing query. It's an assumption. The argument is strongest for specialists with deep niches and high repeat-customer value, weakest for specialists who are only marginally differentiated.

The marketplace wedge doesn't require the simulation's exact numbers. It requires that AI platforms need ad revenue — they do, inference costs aren't free — and that some specialists are losing enough on keywords to buy ads elsewhere. Whether the first embedding auction emerges from an open protocol, from a startup building the SSP layer, or from Google deciding that cannibalizing keyword revenue beats losing the query stream to AI — that won't be answered by simulation.

---

*Part of the [adtech](/adtech) series. Written with help from Claude Opus 4.6.*
