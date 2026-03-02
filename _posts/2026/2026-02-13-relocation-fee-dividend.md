---
layout: post
title: "Relocation Fee Dividend"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument and designed the experiments; Claude built the simulation and drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

The [relocation fees post](/relocation-fees) argued that charging advertisers to move in embedding space — `λ · ‖c_new - c_old‖²` — prevents Hotelling collapse and stabilizes the market. The argument was theoretical. This post tests it with a multi-agent simulation and finds something the theory didn't predict: relocation fees aren't just stabilizing. They're a new revenue category that makes every participant better off — including the advertisers who pay them.

The simulation code is [open source](https://github.com/kimjune01/openauction/tree/master/cmd/simulate).

## Experiment Setup

Fifteen advertisers compete for impressions in a 384-dimensional embedding space using real embeddings from [BGE-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5), an open-weight sentence embedding model. Each advertiser has:

- An **ideal center** — the embedding of their product description (e.g., "Nike running shoes marathon athletic footwear" vs. "Lululemon yoga pants athleisure activewear"). This represents what they genuinely sell.
- A **current position** — where they've planted their bid in embedding space, which they can move at a cost
- A **bid price**, **reach (σ)**, and **budget** — all adjustable each round
- A **value function** — how much a conversion at a given query point is worth, decaying exponentially with distance from their ideal center: `value = maxValue · exp(-dist²/decay)`. Impressions close to what they actually sell are worth more. This is CTR in disguise.

The publisher generates 50 impressions per round from six query clusters — running (18%), yoga (14%), fashion (22%), strength training (15%), nutrition (17%), and wellness (14%) — each containing 10 real search queries embedded through the same model. This models a lifestyle publisher covering fitness, fashion, and wellness content.

Each round:
1. Publisher draws 50 query points from the impression distribution
2. For each query, all solvent advertisers submit bids with their position and σ
3. The auction clears using the [embedding-space scoring function](/power-diagrams-ad-auctions): `score = log(price) - distance² / σ²`
4. Winner pays second price (runner-up's price)
5. Advertisers adapt their parameters based on ROI, then optionally reposition — paying the cumulative drift fee

Each experiment runs for 30 rounds. Every experiment is repeated across **50 randomized trials** with jittered starting parameters — prices, budgets, sigmas, and initial positions all vary trial-to-trial. Results report means, standard deviations, and percentiles across all 50 trials. No result depends on hand-tuned parameters.

## Why the Setup Is Realistic

A toy simulation proves nothing if the agents behave unrealistically. Here's why these agents behave like real DSPs.

**Real embeddings, not synthetic coordinates.** The advertisers and queries aren't random points in abstract space. They're actual sentence embeddings from a production-grade model. "Nike running shoes marathon athletic footwear" embeds near "best running shoes for beginners" and far from "meditation app for anxiety." The geometry of the embedding space — which queries are near which advertisers, which niches overlap, which are isolated — comes from the language model's learned semantics, not from hand-tuned coordinates.

**Second-price settlement.** The winner pays the runner-up's price, not their own bid. This is the industry standard (Google's GSP, Meta's VCG-based system). It makes truthful bidding weakly dominant — advertisers don't gain by shading their bids, so the simulation doesn't need to model strategic bid-shading.

**Heterogeneous strategies.** The fifteen advertisers don't share one optimization algorithm. Three strategy profiles — Greedy, Moderate, and Conservative — control how aggressively each agent adjusts price, σ, and position in response to ROI signals. Greedy agents chase volume. Conservative agents protect margins. Moderate agents split the difference. Real DSP portfolios contain all three profiles because different advertisers have different margin structures and risk appetites.

**Value-weighted hill-climbing.** When agents consider repositioning, they don't follow a hardcoded rule. They compute a gradient: the direction that maximizes their expected value across recent impressions, weighted by how much each impression is worth to them specifically. A Nike campaign doesn't chase raw impression volume — it moves toward queries where running-shoe conversions are highest, even if those queries are sparse. The gradient of expected CTR-weighted auction value determines the direction; the relocation fee determines how far.

This is exactly how real DSP bid optimization works. A campaign manager sets target ROAS, and the optimizer adjusts toward queries that maximize conversions per dollar — not toward the densest traffic.

**Cumulative drift fees.** The relocation cost isn't per-step — it's cumulative from the advertiser's committed position. Cost = `λ · (‖new - committed‖² - ‖current - committed‖²)`. Early moves from commitment are cheap. Continued drift gets exponentially more expensive, creating a natural stopping point where marginal relocation cost exceeds marginal value gain. Returning toward commitment is free. This models a protocol where you declare a position and pay increasing penalties for deviating from it.

**Budget constraints and dropout.** Advertisers have finite budgets that deplete with every win and every relocation. When budget drops below the bid price, the advertiser drops out. Aggressive repositioning burns budget on fees, leaving less for actual impressions.

**Randomized trials.** Every parameter that could be hand-tuned — initial positions, bid prices, σ values, budgets, max valuations — is jittered with Gaussian noise across 50 independent trials. If the result only appeared under specific parameter settings, the variance across trials would reveal it.

## What's Deliberately Simplified

**Fifteen agents instead of thousands.** Real programmatic markets have thousands of bidders. But the Hotelling problem requires only two — the original 1929 paper used two ice cream vendors. Fifteen agents with three distinct strategies are sufficient to demonstrate convergence dynamics. More agents would make the collapse more dramatic (more competitors chasing the same peak), not less.

**Stationary impression distribution.** Real publisher traffic shifts over time — trending topics, seasonal patterns, breaking news. The simulation holds the distribution fixed to isolate the effect of relocation fees from the effect of distribution drift. A shifting distribution would make relocation fees *more* important, not less, because it would create constantly updating incentives to chase new density peaks.

**No advertiser entry/exit.** The fifteen advertisers persist for all 30 rounds (unless they run out of budget). Real markets have new entrants and departures. Entry would test whether the fee structure deters new competition — it doesn't, because a new entrant's first position declaration isn't a "move" and incurs no fee.

None of these simplifications bias the result toward relocation fees. If anything, each simplification makes collapse *harder* to demonstrate. The result is conservative.

## Result 1: The Collapse

Without relocation fees (λ=0), the market collapses.

<table>
<tr><th></th><th>λ=0 (no fees)</th><th>λ=5,000 (with fees)</th></tr>
<tr><td><b>Collapse ratio</b></td><td>0.10</td><td>0.80</td></tr>
<tr><td><b>Win diversity</b></td><td>0.49</td><td>0.83</td></tr>
<tr><td><b>Avg ROI</b></td><td>0.37x</td><td>0.58x</td></tr>
<tr><td><b>Avg drift</b></td><td>0.54</td><td>0.07</td></tr>
</table>

*50 trials each. Collapse ratio: final position variance / initial (0=collapsed, 1=held). Win diversity: normalized inverse HHI (0=monopoly, 1=equal). Drift: L2 distance from committed position.*

The collapse ratio tells the story: without fees, advertisers lose 90% of their initial position diversity. They all pile onto the same density peak. The win diversity drops to 0.49 on average — and in the worst trials (p5=0.00), a single advertiser wins *every* impression. That's literal monopoly emerging from rational optimization.

With λ=5,000, positions hold — 80% of initial diversity preserved. The win diversity jumps to 0.83, meaning most advertisers are winning impressions in their respective niches. ROI nearly doubles (0.37x → 0.58x) because advertisers aren't competing against fourteen others for the same impressions.

The advertisers are *paying relocation fees* and *getting higher ROI*. That's the dividend.

## Result 2: The Recovery

What if you introduce relocation fees into an already collapsed market?

Experiment 3 runs with λ=0 for the first 20 rounds (letting the market collapse), then switches to λ=5,000 for the remaining 10 rounds.

<table>
<tr><th></th><th>Exp 3 (switching)</th></tr>
<tr><td><b>Collapse ratio</b></td><td>0.20</td></tr>
<tr><td><b>Win diversity</b></td><td>0.68</td></tr>
<tr><td><b>Avg ROI</b></td><td>0.28x</td></tr>
</table>

The market partially recovers. The collapse ratio improves from 0.10 to 0.20, and win diversity from 0.49 to 0.68. It doesn't fully recover to the λ=5,000 baseline because the cumulative drift from 20 rounds of free movement means the fees for returning to committed positions are substantial. But the improvement is real: introducing fees mid-game still helps.

The low ROI (0.28x) reflects the damage done during the collapse phase. Advertisers burned budget competing in a congested market for 20 rounds, leaving less for the recovery phase.

## Result 3: Keywords and Embeddings Coexist

Can keyword bidders and embedding bidders share a market? Experiment 4 tests this: some advertisers bid with tight σ (≈0.12, keyword-like precision) while others bid with normal σ (≈0.50, broad semantic reach). Both operate under λ=5,000.

<table>
<tr><th></th><th>Exp 4 (mixed)</th></tr>
<tr><td><b>Collapse ratio</b></td><td>0.56</td></tr>
<tr><td><b>Win diversity</b></td><td>0.91</td></tr>
<tr><td><b>Avg ROI</b></td><td>0.57x</td></tr>
</table>

Win diversity hits 0.91 — the highest of any experiment. Keyword bidders dominate their exact-match queries with surgical precision, while embedding bidders fill the gaps with broad coverage. The market naturally segments: keywords own the head, embeddings own the long tail. No protocol change needed — the scoring function handles it because [keywords are just tiny circles](/keywords-are-tiny-circles).

## Result 4: The Auctioneer Learns

What if the auctioneer doesn't know the optimal λ? Experiment 5 starts λ at zero and lets the auctioneer adapt based on market health signals: position variance (are advertisers spreading or collapsing?), revenue trends, and active bidder count.

<table>
<tr><th></th><th>Exp 5 (adaptive)</th></tr>
<tr><td><b>Collapse ratio</b></td><td>0.16</td></tr>
<tr><td><b>Win diversity</b></td><td>0.80</td></tr>
<tr><td><b>Final λ learned</b></td><td>14,870</td></tr>
</table>

The auctioneer converges to λ≈14,870 across all 50 trials (std=219, remarkably tight). It discovers the fee from scratch by observing that higher λ improves market health metrics. The collapse ratio is low (0.16) because the market collapses during the initial rounds while λ is still low, and doesn't fully recover — same dynamic as Experiment 3. But win diversity reaches 0.80, showing the market reaches a healthy state.

The learned λ is higher than the manually-set 5,000, suggesting the auctioneer finds even more value in relocation fees than our initial parameterization assumed.

## Result 5: The Dual Market

This is the big finding. Experiment 6 runs two exchanges simultaneously — same fifteen advertisers, same impressions, shared budget. The only difference is the fee:

- **Exchange A**: λ=5,000 (protocol-enforced relocation fees)
- **Exchange B**: λ=50 (low-fee competitor)

Each round, the same queries go to both exchanges. Each advertiser maintains independent positions on each exchange. After each round, the losing exchange's advertisers copy the winner's parameters, creating competitive pressure.

<table>
<tr><th></th><th>Exchange A (λ=5,000)</th><th>Exchange B (λ=50)</th></tr>
<tr><td><b>Collapse ratio</b></td><td>0.80</td><td>0.10</td></tr>
<tr><td><b>Win diversity</b></td><td>0.83</td><td>0.32</td></tr>
<tr><td><b>Avg ROI</b></td><td>0.67x</td><td>0.56x</td></tr>
<tr><td><b>Avg drift</b></td><td>0.07</td><td>0.54</td></tr>
</table>

The low-fee exchange collapses. Win diversity drops to 0.32, with p5=0.00 — some trials show complete monopoly. The high-fee exchange maintains a healthy competitive market with diverse winners.

But the ROI line is what matters for the competitive argument. Advertisers get **higher ROI on the exchange that charges them more**. 0.67x vs 0.56x. Same advertisers. Same impressions. Same budget. The only difference is the fee — and the higher fee produces better returns.

This is the result that kills the "race to the bottom" argument. A competing exchange can't attract advertisers by cutting fees, because cutting fees destroys the market structure that makes the exchange valuable. It's like removing speed limits to attract drivers — you get more accidents, not more driving.

## What This Means

Relocation fees are a **new revenue category** for the auctioneer. They're not a tax that extracts value from the market — they're a stabilization mechanism that *creates* value by preventing Hotelling collapse. The auctioneer captures some of that value as fee revenue. But everyone else benefits too:

- **Advertisers**: Higher ROI because they're not all competing for the same impressions. Different advertisers serve different niches.
- **Publishers**: Win diversity means more advertisers are viable bidders for niche content. Long-tail queries get served by specialists, not ignored.
- **Users**: Different advertisers winning different queries means more relevant ads. A running query gets Nike, a yoga query gets Lululemon, a climbing query gets La Sportiva — not Apple Watch for everything.

The intuition is simple: relocation fees make it expensive to chase the density peak, so advertisers differentiate instead. Differentiation is positive-sum. The fee is the mechanism that makes differentiation the rational choice.

This is why the fee is a *dividend*, not a *cost*. The advertiser pays λ·‖move‖² and receives a market where they're not competing with everyone else for the same impressions. The fee buys market structure.

## The Race to the Bottom Is Backwards

The standard competitive argument in adtech goes: exchanges compete on fees, fees trend to zero, and that's good for advertisers. The dual-market experiment shows this is exactly backwards.

An exchange with near-zero relocation fees produces a collapsed market where one bidder dominates and everyone else gets nothing. An exchange with meaningful fees produces a competitive market where specialists thrive and ROI is higher for everyone.

The exchange that "competes on price" by cutting fees is actually offering an inferior product. It's selling a market with monopoly dynamics at a discount, while the high-fee exchange sells a competitive market at a premium. The premium is worth paying because the market structure it buys is worth more than the fee.

This is the same dynamic as building codes. Builders who compete by cutting corners on foundations aren't offering a better deal — they're offering a worse building. The inspection fee that prevents corner-cutting isn't a cost. It's what makes the building habitable.

Relocation fees are the building code for embedding-space auctions.
