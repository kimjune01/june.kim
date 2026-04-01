---
variant: post
title: "Missing Players"
tags: vector-space
---

*[MOSAIC](https://arxiv.org/abs/2405.05905) (Soumalias, Curry & Seuken, 2025) is the best paper on LLM ad auctions I've found. The mechanism design is clean. The deployment assumptions are not. Part of the [Vector Space](/vector-space) series.*

## What MOSAIC gets right

Chatbot inference [costs more than it earns](https://epoch.ai/gradient-updates/can-ai-companies-become-profitable). Advertising is the business model that scales with free usage. But how do you run an ad auction over generated text without destroying the product?

MOSAIC starts from a genuine insight: the RLHF objective already has the right shape. Replace human feedback reward with aggregate advertiser reward, keep the KL penalty against a reference LLM, and the entire alignment literature transfers. The optimal policy has a closed form (Peters & Schaal, 2007). The objective:

> `J(π) = E[Σ r_i(x,y)] − τ D_KL(π ‖ π_ref)`

The allocation rule is elegant. Sample `M` candidate replies from a generation LLM, score each by advertiser reward functions `r_i(x,y)`, return one via importance-weighted softmax. No fine-tuning. No model weights. API access only. With a context-aware LLM, twenty candidates match the theoretical optimum.

The payment rule is the real contribution. The allocation is a softmax, the gradient of LogSumExp. It's convex in advertiser reports. Convexity gives cyclic monotonicity. Cyclic monotonicity gives Rochet (1987) payments. Theorem 5.1: truthful reporting is a dominant strategy for every advertiser, for any finite set of candidates, *before* the allocation converges. VCG can't do this here (Section 3.2) because it needs the exact optimum, which is intractable over token sequences.

The social welfare offset (Lemma 5.2) aligns each advertiser's utility with their marginal contribution. Without it, low-relevance advertisers free-ride and dilute the pool. And inherent competition against `π_ref` means even a single advertiser competes against the ad-free baseline. No reserve price needed.

The theorems are correct. If the assumptions hold, the mechanism works.

## Seven assumptions that don't hold

Every one traces back to the same root. A user who can switch platforms in one click constrains everything below.

### 1. Inference is expensive

MOSAIC requires `M · (L + n + 1)` forward passes per query: `M` candidate generations of `L` tokens each, plus evaluation against `n` advertiser reward functions and the reference LLM. The paper's best case is `M = 20` with a context-aware LLM (Appendix C.6). That's roughly 5× the compute of a single query.

At OpenAI's reported [$60 CPM](https://web.archive.org/web/20260217041818/https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html) and an estimated [$0.01–0.03 per query](https://epoch.ai/gradient-updates/can-ai-companies-become-profitable) in inference cost, the auction overhead alone eats most of the ad revenue per impression. The surplus has to cover both the baseline query and the 4× overhead. At current unit economics, it doesn't.

### 2. `τ` is untuneable

The paper treats `τ` as a knob the platform turns: "enables the auctioneer to balance producing replies closer to the reference LLM or with higher reward for the advertisers." It isn't free.

I [swept the equivalent parameter](/the-price-of-relevance) in embedding-space auctions and the tradeoff is monotonic: higher relevance weight improves user outcomes at the cost of revenue. The curve is smooth enough to pick a point, but the paper doesn't model what constrains that choice.

User participation elasticity binds `τ` from below. Advertiser participation binds it from above: set `τ` too high, and advertiser influence approaches zero, so nobody pays. [Gomes (2014)](https://ideas.repec.org/a/bla/randje/v45y2014i2p248-272.html) formalized this for two-sided markets: the optimal quality weight is always above the pure revenue-maximizer's choice because the platform has to retain both sides. The feasible region may be empty.

### 3. Output is erratic

The mechanism's output depends on which `M` candidates get sampled from `π_gen`. Different draws, different winners. Corollary 4.1 proves convergence *in the limit* as `M → ∞`. At finite `M`, an advertiser paying real money sees variance: the same query, same bids, different response. The paper's importance-sampling variance (Lemma A.2) shrinks as `1/M`, but `M` is constrained by assumption 1.

Traditional ad auctions are deterministic: same bids, same winner. Advertisers buy predictability. A media buyer who can't forecast impressions can't commit budget. MOSAIC's stochasticity makes the product unsellable before it makes it suboptimal.

### 4. Ads are unattributable

The ad is woven into the generated response. No click, no impression boundary, no discrete ad unit. Algorithm 1 returns one reply. The user sees text, not a placement. Did the advertiser's reward function influence the response? By how much? The mechanism doesn't produce a receipt.

Strategyproofness (Theorem 5.1) covers what advertisers *bid*. It says nothing about what the platform *ran*. Did it apply the published `τ`? Use the advertiser's actual reward function? Or quietly relax the KL penalty? Without a verifiable execution trace, the advertiser can't tell. Definition 3.1 guarantees truthful reporting is dominant "no matter what the others do." It only constrains what advertisers report, not what the platform executes.

### 5. Incumbents have a moat

Inherent competition against `π_ref` sounds fair. Every advertiser competes against the ad-free baseline. But `π_ref` already encodes brand frequency from its training data. Ask most LLMs "what's the best image editor?" and the baseline response mentions Adobe before anything else. A new entrant's reward function has to overcome that prior. The "no reserve price needed" feature becomes an advantage for whoever the training corpus already favors.

The context-aware variant (`π_con`) partially addresses this by injecting advertiser descriptions into the generation prompt. But `π_con` still generates from `π_ref`'s weights. The startup gets one shot at overcoming a prior built on billions of tokens of incumbent mentions.

### 6. Advertisers are adversarial

MOSAIC aggregates advertiser rewards additively: `r(x,y) = Σ r_i(x,y)`. The softmax over this sum produces one reply that tries to satisfy everyone. The paper doesn't address what happens when advertisers are direct competitors.

Coca-Cola and Pepsi both bid on "best soda." Their reward functions pull in opposite directions. The mechanism faithfully sums them, and the output either mentions both (satisfying neither) or picks one stochastically (back to assumption 3).

Worse, a truthful reward function can encode negative preferences: "my reward is high when my competitor's brand doesn't appear." Strategyproofness guarantees this is reported honestly. It doesn't prevent it.

Traditional ad auctions handle this with category exclusivity and competitive separation rules. MOSAIC's allocation has no such structure. The paper's implicit answer is that the softmax will sort it out. In practice, adversarial rewards in a sum degrade output quality for the user, which triggers assumption 7.

### 7. The user can leave

MOSAIC models three players: the platform, the advertisers, and the mechanism. It doesn't model the user. [Switching is a few clicks away](/three-levers).

Consider the optimal strategy without a user in the model: set `τ` to zero and maximize ad revenue per query. Nothing in MOSAIC's constraints prevents it. The mechanism is strategyproof all the way down to the point where every response is an ad. When users multi-home across ChatGPT, Claude, and Gemini in one browser session, the captive-user assumption breaks first.

Perplexity learned this empirically. It tried first-party ads, earned [$20K total](https://digiday.com/media/perplexitys-ad-business-hasnt-exactly-been-a-hit/), and [killed them](/perplexity-was-right-to-kill-ads). Anthropic [vowed never to run ads in Claude](https://web.archive.org/web/20260217041818/https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html). The market has already voted on how much steering users will tolerate. The answer is close to none.

## The chain

These seven aren't independent. The user can leave (7), which constrains `τ` (2), which limits revenue, which can't cover the inference overhead (1). Erratic output (3) and missing attribution (4) make the product unsellable to advertisers even within the feasible `τ` range. Adversarial rewards (6) degrade output quality, which accelerates user exit. Incumbent advantage (5) thins the advertiser pool to players who don't need the mechanism.

## The alternative

MOSAIC's core mistake is baking advertising into inference. Every assumption follows from that choice: the auction runs inside the generation loop, so it multiplies compute, introduces variance, hides attribution, and gives the platform unchecked control over `τ`.

Advertising doesn't have to work that way. A chatbot already captures [user intent during conversation](/intent-extraction). The user says what they want, in their own words, before any ad auction fires. That intent signal is richer than a search query and cheaper than twenty candidate generations. Embed it, and it becomes a point in the same [space advertisers already occupy](/buying-space-not-keywords). The [auction runs there](/power-diagrams-ad-auctions), not inside the generation loop.

Run the auction *after* the response, on the intent extracted *during* the conversation, and every assumption changes. Inference cost is zero — the conversation already happened. `τ` disappears because the response isn't steered. Output is deterministic and attribution is trivial: the ad is a separate object the user either saw or didn't. Competitors get discrete placements, not blended text. The user stays because the product wasn't degraded.

The mechanism design is clean. The generation loop it runs in is not.

---

*Written via the [double loop](/double-loop).*
