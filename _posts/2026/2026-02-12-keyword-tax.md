---
layout: post
title: "Keyword Tax"
tags: vector-space
image: "/assets/11_egalitarian_auction.png"
---

![The keyword tax: specialists crammed into one auction](/assets/11_egalitarian_auction.png)

Keywords herd traffic into a narrow, dense auction. Five physical therapists — a climbing specialist, a pelvic floor specialist, a pediatric specialist, a sports rehab specialist, and a generalist — all bid on "physical therapy." The auction can't tell them apart. Each bin has 4–5 bidders fighting over every query, pushing clearing prices up and extracting maximum revenue. This is what the publisher wants.

[Levin & Milgrom (2010)](https://web.stanford.edu/~jdlevin/Papers/OnlineAds.pdf) call this **conflation**: pooling heterogeneous items into one auction. The auction mechanism is efficient (GSP works); the item definition is not. The climbing PT pays to compete on "pelvic floor exercises after C-section." The pelvic floor PT pays to compete on "finger pulley injury from rock climbing." Neither will convert on the other's queries, but the keyword bin forces them into the same auction anyway. That's the keyword tax.

Can embedding auctions fix it? We built both auction types and ran 50 randomized trials.

## The Simulation

Fifteen advertisers compete across 62 queries in a high-dimensional embedding space using real embeddings from [BGE-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5):

- **Physical therapy** (5): climbing PT, sports PT, pelvic floor PT, pediatric PT, general PT
- **Fitness coaching** (4): climbing coach, running coach, CrossFit coach, personal trainer
- **Nutrition** (4): sports dietitian, gut health specialist, weight loss coach, general nutritionist
- **Tutoring** (2): ADHD math tutor, general math tutor

Eleven are specialists; four are generalists who compete broadly. Specialists have narrow targeting radius (σ=0.30) and high max value (12.0) reflecting their conversion advantage. Generalists have wide radius (σ=0.55) and moderate max value (6.0). The 2x ratio is an assumption, but a climber who finds the climbing PT books follow-up sessions and refers other climbers, while a climber who finds a general PT might not come back.

Two auction mechanisms:

- **Keywords.** Queries binned by cluster. Only advertisers in the matching cluster compete, on price alone. Today's market.
- **Embeddings.** Full `log(price) - dist²/σ²` scoring. Agents optimize bid, position, and σ. Tested with and without [relocation fees](/relocation-fees#the-protocol-layer) penalizing drift from committed position.

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

Publisher revenue drops 8%, from 79.39 to 72.82 (p<0.001). That surplus goes to the advertisers. Generalists benefit most, going from -0.233 to nearly break-even at -0.022. Specialist surplus improves directionally (-0.807 to -0.695) but doesn't reach significance; more on that below.

### The keyword tax, measured

Specialists lose 3.5x more than generalists (-0.807 vs -0.233 per round). The conflation penalty is visible in the data: specialists pay to compete on queries they can't convert.

### What embeddings fix

![Keywords collapse everyone to gray; embeddings let each specialist find their color](/assets/11_egalitarian_auction_dots.png)

Embeddings move surplus from the publisher to the advertisers. Win diversity improves from 0.809 to 0.833 (p<0.01), so the consumer who searches "finger pulley injury from rock climbing" finds the climbing PT, not whoever bid highest on "physical therapy."

Specialist surplus improves directionally (-0.807 to -0.695, ns) but specialists are still losing money. Without [relocation fees](/relocation-fees#the-gap-vcg-leaves), advertisers drift toward popular queries and the niche advantage erodes.

Adding relocation fees changes the picture. Specialist surplus goes from -0.695 to +0.021 (p<0.001). Specialists make money. Fees pin them at their niche, and their conversion advantage translates into winning their best queries at prices that leave positive surplus. Win diversity climbs further to 0.876. Value efficiency recovers to 0.834, within 2.4pp of keywords.

### Why a monopolist wouldn't switch

Dense keyword auctions extract more rent. The publisher's optimal auction is `α = 0`: no distance weighting, everyone competes everywhere. That's keywords.

This is already visible in practice: Google keeps expanding broad match and deprecating exact match, making keyword bins vaguer and auctions denser. [Athey & Gans (2010)](https://www.aeaweb.org/articles?id=10.1257/aer.100.2.608) showed theoretically why: better targeting disproportionately benefits large general-audience platforms, which can segment audiences to match what niche publishers offer naturally. The dominant platform's rational move is to keep targeting coarse enough that its breadth advantage holds. In a [recent industry poll](https://web.archive.org/web/20250918041138/https://searchengineland.com/small-businesses-compete-google-ads-462009), more than 50% of respondents said small businesses have been priced out of Google Ads entirely.

A monopolist publisher would not adopt embedding auctions. Specialists have no outside option: they either pay the keyword tax or don't advertise.

## Part 2: What If a Competitor Offers Embeddings?

If a competitor offers embedding auctions, every participant can compare their surplus:

<table>
<tr><th>Participant</th><th>Keywords (incumbent)</th><th>Embeddings + fees (competitor)</th><th>Switching gain</th></tr>
<tr><td><b>Specialists (11)</b></td><td><b>-0.807/round</b></td><td><b>+0.021/round</b></td><td><b>+0.828</b></td></tr>
<tr><td>Generalists (4)</td><td>-0.233/round</td><td>-0.052/round</td><td>+0.181</td></tr>
<tr><td>Publisher</td><td>79.39/round</td><td>67.23/round</td><td>-12.16</td></tr>
</table>

Specialists gain +0.828 per round, from losing money to making money. That's the switching incentive that bootstraps the competing exchange. Generalists gain too, but specialists gain 4.6x more and outnumber generalists 11 to 4.

### The distribution moat

But advertisers go where the users are. No queries, no auction.

Google pays Apple [over $18 billion a year](https://web.archive.org/web/20260219183446/https://www.theverge.com/2023/10/26/23933206/google-apple-search-deal-safari-18-billion) to be the default search engine on Safari. Queries flow to keyword auctions because users flow to Google, and users flow to Google because of a default payment that costs more per year than most companies are worth.

The keyword equilibrium is stable because the moat is expensive to cross.

### Where the queries are going

AI chatbots already have the traffic. They just can't monetize it.

Perplexity, ChatGPT, Claude, Gemini: millions of queries, burning inference costs, no ad revenue. These queries are conversational: "my finger hurts after a climbing session, should I see a physical therapist?" There's no keyword to bid on when the query is a paragraph. But it maps to the climbing PT's position in embedding space.

![Keywords shout nothing; specialists with something to say get drowned out](/assets/11_keyword_megaphone.png)

Meanwhile, search advertising is shrinking. As covered in [The Convergence](/the-convergence), organic CTR dropped 65% and paid CTR fell 68% on queries where AI Overviews appeared. Specialists paying the keyword tax are the first to get priced out, and the chatbots already have the queries they'd pay to reach. The connection is missing.

### The missing piece

The long tail of chatbot platforms (vertical assistants, domain-specific tools, niche communities) doesn't exist yet, because there's no way to monetize conversational traffic. An embedding auction that works across platforms would let any chatbot with a focused query stream sell ad inventory. The equilibrium is thousands of small platforms, connected by a shared auction layer.

Whether embedding auctions generate enough revenue per query to offset inference costs is open. Perplexity tried keyword-style ads: $20K in total revenue. OpenAI projects $1B in 2026 ads against $14B in inference costs. Current ad formats are a poor fit for conversational queries. Embedding auctions might change the yield, but that's speculation, not measurement.

The climbing PT who's losing -0.807 per round on Google keywords will buy ads on the platform where her niche queries exist, at prices where she breaks even. The keyword incumbent can't replicate this without cannibalizing their own revenue.

### What ships first will be wrong

The likely first implementation is RAG-based ad selection: embed the query, find the nearest ad embeddings, show the top results. This is already how these platforms retrieve context. Extending it to ads is a small step.

But RAG selection is a [Voronoi diagram](/power-diagrams-ad-auctions): equal radius for every advertiser, no price integration, and no way to control competitive radius. Better resolution, same structural flaw.

Whoever ships RAG ad selection first will discover what the simulation already shows: without per-advertiser σ, price-integrated scoring, and drift penalties, the embedding auction degrades. Positions drift toward popular queries and aggressive bids override relevance. They'll patch in radius control, then scoring, then fees. They'll reinvent the [power diagram auction](/power-diagrams-ad-auctions) incrementally.

## The Caveats

The 2x specialist conversion advantage drives the surplus story. At 1.25x (v3.3), all effects shrank to non-significance. The mechanism works at any ratio (specialists always do directionally better with embeddings) but whether the effect is significant depends on how much better specialists actually convert. The argument is strongest for deep niches with high repeat-customer value.

The marketplace wedge doesn't require the simulation's exact numbers. It requires that AI platforms need ad revenue (inference costs aren't free) and that some specialists are losing enough on keywords to buy ads elsewhere. Whether the first embedding auction emerges from an open protocol or a startup building the SSP layer, that won't be answered by simulation.

---

*Part of the [Vector Space](/vector-space) series. Written with help from Claude Opus 4.6.*
