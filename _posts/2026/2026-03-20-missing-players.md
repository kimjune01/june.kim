---
layout: post
title: "Missing Players"
tags: vector-space
---

*[MOSAIC](https://arxiv.org/abs/2405.05905) (Duetting et al., 2024) is mechanism-design-complete but market-design-incomplete. A rebuttal. Part of the [Vector Space](/vector-space) series.*

## Money

Chatbot companies are losing money on inference. OpenAI [lost $5 billion on $3.7 billion in revenue](https://epoch.ai/gradient-updates/can-ai-companies-become-profitable) in 2025, with [$14 billion in inference costs](https://web.archive.org/web/20260227151900/https://finance.yahoo.com/news/openais-own-forecast-predicts-14-150445813.html) projected for 2026. Subscriptions have a ceiling. As chatbots grow in capability, so do user expectations, and inference is not getting cheap enough to close the gap. Historically, advertising is the business model that scales with free usage.

Perplexity tried first-party ads, earned [$20K total](https://digiday.com/media/perplexitys-ad-business-hasnt-exactly-been-a-hit/), and [killed them](/perplexity-was-right-to-kill-ads). Anthropic [vowed never to run ads in Claude](https://web.archive.org/web/20260217041818/https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html). OpenAI launched ads at [$60 CPM](https://web.archive.org/web/20260217041818/https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html) with closed targeting logic no one outside OpenAI can audit. No consensus on how to do this without destroying trust.

MOSAIC is the best paper on LLM ad auctions I've found. The platform samples `M` candidate responses from a generation LLM, then reweights them by advertiser reward functions `r_i(x,y)`. A KL penalty `τ` against a reference LLM anchors output to the ad-free baseline. Rochet (1987) payments enforce strategyproofness via cyclic monotonicity (Theorem 5.1). It doesn't model the user. Four consequences follow.

### The chatbot selects the ad

MOSAIC's Algorithm 1 runs inside the chatbot: sample candidates from `π_gen`, score them by `Σ r_i(x,y)`, return `y` from a softmax over aggregate advertiser reward. The chatbot becomes both the user's agent and the advertiser's agent. This dual agency is the failure mode Perplexity discovered when it [killed its ad business](/perplexity-was-right-to-kill-ads) after $20K in total revenue.

The conflict lives in *who runs the selection*. MOSAIC's mechanism is incentive-compatible for advertisers. It says nothing about who the user trusts to run it.

### `τ` is not free

MOSAIC's objective:

> `J(π) = E[Σ r_i(x,y)] − τ D_KL(π ‖ π_ref)`

The paper says `τ` "enables the auctioneer to balance producing replies closer to the reference LLM or with higher reward for the advertisers." It treats `τ` as exogenous — a knob the platform turns. It isn't free.

I [swept the equivalent parameter](/the-price-of-relevance) in embedding-space auctions (the log base maps directly to `τ`) and the tradeoff is monotonic: higher relevance weight improves user outcomes at the cost of revenue, no free lunch. The curve is smooth enough to pick a point, but the paper doesn't model what constrains that choice.

User participation elasticity binds `τ` from below. If the platform sets `τ` too low, responses drift too far and users switch platforms. [Gomes (2014)](https://ideas.repec.org/a/bla/randje/v45y2014i2p248-272.html) formalized this for two-sided markets: the optimal quality weight is always above the pure revenue-maximizer's choice because the platform has to retain the demand side. The viable region for τ may be narrow enough to collapse the revenue model entirely. The paper doesn't ask.

### Strategyproof isn't trustworthy

Theorem 5.1 proves truthful reporting is dominant under Rochet payments, but a truthful auction is not a verifiable auction. Strategyproofness covers what advertisers *bid*. It says nothing about what the platform *ran*. Did it apply the published `τ`? Use the advertiser's actual reward function? Or quietly relax the KL penalty? This ambiguity is where ad fraud lives — [$84 billion per year](https://www.juniperresearch.com/research/fintech-payments/fraud-identity/ad-fraud-lost-to-fraud/) by Juniper Research's estimate.

Definition 3.1 guarantees truthful reporting is dominant "no matter what the others do." But it only constrains *what* advertisers report, not *who* gets to report. Strategyproofness optimizes the wrong margin — honest bidding by unvetted participants.

## The missing player

MOSAIC models three players: the platform, the advertisers, and the mechanism. It doesn't model the user. [Switching is a few clicks away](/three-levers). If OpenAI pushes `τ` too low — too aggressive, too personal, users leave for the platform that doesn't steer its answers.

Consider the optimal strategy without a user in the model: crank `τ` to zero and maximize ad revenue per query. Nothing in MOSAIC's constraints prevents it. The mechanism is strategyproof all the way down to the point where every response is an ad. In a market where users can multi-home across ChatGPT, Claude, and Gemini in the same browser session, the captive-user assumption breaks first.

## Closing the gaps

No single patch closes these gaps. Fixing `τ` doesn't fix selection. Fixing selection doesn't produce receipts. Producing receipts doesn't vet participants. The gaps are coupled because they share a root cause: the user isn't in the model.

Once the user is a player who can walk away, the architecture follows: [externalized selection](/perplexity-was-right-to-kill-ads), [attested execution](/attested-attribution), [scoring in sealed hardware](/power-diagrams-ad-auctions), [admission control](/proof-of-trust). These are governance layers. MOSAIC solves truthful bidding inside the mechanism; adoption depends on trust outside it. It's a theorem looking for a market.

---

*Written via the [double loop](/double-loop).*
