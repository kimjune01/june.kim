---
layout: post
title: "Missing Players"
tags: vector-space
---

*[MOSAIC](https://arxiv.org/abs/2405.05905) (Soumalias, Curry & Seuken, 2025) is the best paper on LLM ad auctions I've found. The mechanism design is clean. The deployment assumptions are not. Part of the [Vector Space](/vector-space) series.*

## What MOSAIC gets right

Chatbot companies are losing money on inference. OpenAI [lost $5 billion on $3.7 billion in revenue](https://epoch.ai/gradient-updates/can-ai-companies-become-profitable) in 2025, with [$14 billion in inference costs](https://web.archive.org/web/20260227151900/https://finance.yahoo.com/news/openais-own-forecast-predicts-14-150445813.html) projected for 2026. Subscriptions have a ceiling. Advertising is the business model that scales with free usage. The question is how to run an ad auction over generated text without destroying the product.

MOSAIC's answer starts from a genuine insight: the RLHF objective already has the right shape. Replace human feedback reward with aggregate advertiser reward, keep the KL penalty against a reference LLM, and the entire alignment literature transfers. The optimal policy has a closed form (Peters & Schaal, 2007). The objective:

> `J(π) = E[Σ r_i(x,y)] − τ D_KL(π ‖ π_ref)`

The allocation rule is elegant. Sample `M` candidate replies from a generation LLM, score each by advertiser reward functions `r_i(x,y)`, return one via importance-weighted softmax. No fine-tuning. No model weights. API access only. With a context-aware generation LLM, twenty candidates are enough to match the theoretical optimum.

The payment rule is the real contribution. The allocation is a softmax — the gradient of a LogSumExp — which is convex in advertiser reports. Convexity gives cyclic monotonicity. Cyclic monotonicity gives Rochet (1987) payments. Theorem 5.1: truthful reporting is a dominant strategy for every advertiser, for any finite set of candidates, *before* the allocation converges. VCG can't do this here (Section 3.2) because it needs the exact optimum, which is intractable over token sequences.

Two more things worth noting. The social welfare offset (Lemma 5.2) aligns each advertiser's utility with their marginal contribution — without it, low-relevance advertisers free-ride and dilute the pool. And inherent competition against `π_ref` means even a single advertiser competes against the ad-free baseline. No reserve price calibration needed.

This is careful, technically strong work. The theorems are correct. The architecture is implementable. If the assumptions hold, the mechanism works.

## Six assumptions that don't hold

### 1. Inference is expensive

MOSAIC requires `M · (L + n + 1)` forward passes per query: `M` candidate generations of `L` tokens each, plus evaluation against `n` advertiser reward functions and the reference LLM. The paper reports convergence at `M = 20` with a context-aware LLM — roughly five LLM queries of compute per user query (Appendix C.6).

That's a 5× multiplier on inference cost for a business that's already [losing money on every query](https://epoch.ai/gradient-updates/can-ai-companies-become-profitable). The ad revenue has to cover not just the baseline inference but the auction overhead. At OpenAI's reported [$60 CPM](https://web.archive.org/web/20260217041818/https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html), the margin math is tight before the multiplier and negative after it.

### 2. `τ` is untuneable

The paper treats `τ` as a knob the platform turns: "enables the auctioneer to balance producing replies closer to the reference LLM or with higher reward for the advertisers." It isn't free.

I [swept the equivalent parameter](/the-price-of-relevance) in embedding-space auctions and the tradeoff is monotonic: higher relevance weight improves user outcomes at the cost of revenue. No free lunch. The curve is smooth enough to pick a point, but the paper doesn't model what constrains that choice.

User participation elasticity binds `τ` from below. Advertiser participation binds it from above — set `τ` too high, and advertiser influence approaches zero, so nobody pays. [Gomes (2014)](https://ideas.repec.org/a/bla/randje/v45y2014i2p248-272.html) formalized this for two-sided markets: the optimal quality weight is always above the pure revenue-maximizer's choice because the platform has to retain both sides. The feasible region may be narrow enough to collapse the revenue model entirely.

### 3. Output is erratic

The mechanism's output depends on which `M` candidates get sampled from `π_gen`. Different draws, different winners. Corollary 4.1 proves convergence *in the limit* as `M → ∞`. At finite `M`, an advertiser paying real money sees variance: the same query, same bids, different response. The paper's importance-sampling variance (Lemma A.2) shrinks as `1/M`, but `M` is constrained by assumption 1.

Traditional ad auctions are deterministic: same bids, same winner. MOSAIC's stochasticity makes it hard for advertisers to predict what they're buying. That's a sales problem before it's a theory problem.

### 4. Ads are unattributable

The ad is woven into the generated response. There's no click, no impression boundary, no discrete ad unit. Algorithm 1 returns one reply — the user sees text, not a placement. Did the advertiser's reward function influence the response? By how much? The mechanism doesn't produce a receipt.

Strategyproofness (Theorem 5.1) covers what advertisers *bid*. It says nothing about what the platform *ran*. Did it apply the published `τ`? Use the advertiser's actual reward function? Or quietly relax the KL penalty? This ambiguity is where ad fraud lives — [$84 billion per year](https://www.juniperresearch.com/research/fintech-payments/fraud-identity/ad-fraud-lost-to-fraud/) by Juniper Research's estimate. Definition 3.1 guarantees truthful reporting is dominant "no matter what the others do." It only constrains what advertisers report, not what the platform executes.

### 5. Incumbents have a moat

Inherent competition against `π_ref` sounds fair — every advertiser competes against the ad-free baseline. But `π_ref` already knows the big brands. A reference LLM trained on the internet assigns high probability to "use Photoshop for image editing" and near-zero to a startup nobody's heard of. The new entrant's reward function fights against the prior. The "no reserve price needed" feature is a moat for whoever the training data already favors.

The context-aware variant (`π_con`) partially addresses this by injecting advertiser descriptions into the generation prompt. But `π_con` still generates from `π_ref`'s weights. The startup's description gets one shot at overcoming a prior built from billions of tokens of incumbent brand mentions.

### 6. The user can leave

MOSAIC models three players: the platform, the advertisers, and the mechanism. It doesn't model the user. [Switching is a few clicks away](/three-levers).

Consider the optimal strategy without a user in the model: set `τ` to zero and maximize ad revenue per query. Nothing in MOSAIC's constraints prevents it. The mechanism is strategyproof all the way down to the point where every response is an ad. In a market where users multi-home across ChatGPT, Claude, and Gemini in the same browser session, the captive-user assumption is the first thing that breaks.

Perplexity learned this empirically. It tried first-party ads, earned [$20K total](https://digiday.com/media/perplexitys-ad-business-hasnt-exactly-been-a-hit/), and [killed them](/perplexity-was-right-to-kill-ads). Anthropic [vowed never to run ads in Claude](https://web.archive.org/web/20260217041818/https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html). The market has already voted on how much steering users will tolerate. The answer is close to none.

## The theorem and the market

These six aren't independent. The user can leave (6), which constrains `τ` (2), which limits revenue, which can't cover the inference overhead (1). Erratic output (3) and missing attribution (4) make the product unsellable to advertisers even within the feasible `τ` range. Incumbent advantage (5) thins the advertiser pool to players who don't need the mechanism.

No single patch closes the gaps. Fixing `τ` doesn't fix attribution. Fixing attribution doesn't fix cost. Reducing cost doesn't fix fairness. They're coupled because they share a root cause: the user isn't in the model.

Once the user is a player who can walk away, the architecture changes: [externalized selection](/perplexity-was-right-to-kill-ads) so the chatbot isn't dual-agent, [attested execution](/attested-attribution) so advertisers can verify what ran, [scoring in sealed hardware](/power-diagrams-ad-auctions) so the platform can't quietly relax `τ`, [admission control](/proof-of-trust) so the participant pool is vetted. These aren't patches on MOSAIC. They're the governance layers a market needs before any mechanism — however clean — can run inside it.

MOSAIC solves truthful bidding. Deployment requires trust. The theorem is correct. The market doesn't exist yet.

---

*Written via the [double loop](/double-loop).*
