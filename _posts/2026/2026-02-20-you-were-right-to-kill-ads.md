---
layout: post
title: "Perplexity Was Right to Kill Ads"
tags: adtech
---

*Part of the [adtech](/adtech) series.*

---

Perplexity [killed ads](https://www.macrumors.com/2026/02/18/perplexity-abandons-ai-advertising/) in February 2026. Total ad revenue: [$20,000](https://digiday.com/media/perplexitys-ad-business-hasnt-exactly-been-a-hit/). The ad sales head left. The trust damage wasn't worth it.

That was the right call. Running first-party ads inside a product people trust for unbiased answers is a contradiction you can't message your way out of. The moment a chatbot shows an ad it selected, every answer becomes suspect. Did the chatbot recommend that product because it's best, or because someone paid? The user can't tell. Anthropic understood this immediately — their Super Bowl ad said it plainly: [ads are coming to AI, but not to Claude](https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html).

The mistake is concluding that the only options are "run ads and lose trust" or "don't run ads and burn cash."

There's a third option. And it turns the chatbot into the supply side of the most valuable ad inventory on the internet.

## The Problem That Won't Go Away

Inference costs money. Perplexity, Claude, Gemini, ChatGPT — every query burns compute. OpenAI's inference bill is projected at [$14 billion for 2026](https://finance.yahoo.com/news/openais-own-forecast-predicts-14-150445813.html). Subscriptions cover power users. Free users — the majority — need a different model.

The venture math doesn't work forever. At some point, every chatbot platform serving free users has to answer: where does the money come from? The three options are subscriptions (ceiling is low — most people won't pay), data licensing (publishers are fighting back), and ads (the only model that scales with usage).

Killing ads doesn't solve the revenue problem. It just delays it.

## Why First-Party Ads Fail

When the chatbot platform runs its own ads, it becomes both the user's agent and the advertiser's agent. That's a conflict of interest, not a feature.

OpenAI's approach makes this visible. They're [testing ads at $60 CPM](https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html) with a $200K minimum buy. The targeting is closed — no one outside OpenAI can verify how ads are selected. The auction mechanics, if there are any, aren't published. Every advertiser who buys in is trusting OpenAI to be fair. Every user who sees an ad is trusting OpenAI not to let revenue influence answers.

That trust is unverifiable. And it degrades over time. The gap between OpenAI's inference costs ($14B) and ad revenue target ($1B) guarantees increasing pressure to extract more from every query. The incentive is to make ads more aggressive, not less. First-party ads start polite and get worse — that's the [enshittification](https://doctorow.medium.com/big-techs-attention-rents-fe97ba3fad90) cycle applied to a new medium.

Perplexity saw this coming and pulled the plug. The question is what they do next.

## Externalize the Auction

The answer is to separate the chatbot from the ad system entirely. The chatbot answers questions. A separate exchange runs the ad auction. The chatbot never selects, prices, or targets ads — it routes inventory to an exchange and displays what comes back.

This is how the web already works. Publishers don't run their own ad auctions. They route inventory through exchanges — Google Ad Exchange, PubMatic, Magnite — that handle targeting, bidding, and clearing. The publisher serves content. The exchange handles ads. Separation of concerns.

A chatbot platform doing this can honestly tell users: we don't run ads. We don't select them. We don't know what ad you'll see until the exchange tells us. Our answers are not influenced by advertising revenue, because we don't control the ad system.

That's a credible claim. Perplexity's "we run ads ourselves" wasn't.

## The Leak in Externalization

There's an obvious problem with routing chatbot queries to an external exchange: the exchange sees your users' queries.

Embeddings encode intent. A query embedding for *my marriage is falling apart, should I see a therapist?* contains information the user did not consent to share with an ad exchange. Embeddings can be [approximately reversed](https://arxiv.org/abs/2310.06816) — the exchange could reconstruct something close to the original text. Sending query embeddings to a third party is a privacy leak dressed up as an API call.

This is the trap. First-party ads kill trust because the platform has a conflict of interest. Externalized ads kill trust because user data leaves the building. Both options are bad.

Unless the auction runs inside the building.

## The Sealed Auction

Trusted execution environments solve this. A TEE is a hardware enclave — a sealed compute environment that proves what code is running inside it. AWS Nitro Enclaves, Intel SGX, AMD SEV. The key property: even the operator of the machine can't see what's happening inside the enclave, and anyone can verify what code is executing.

Here's the architecture:

1. The chatbot embeds the user's query on its own infrastructure. The embedding never leaves.
2. A TEE enclave, running on the chatbot's infrastructure, receives the embedding. The enclave contains the auction's scoring function — published, audited, open-source.
3. Advertiser bids (positions, radii, prices) are loaded into the enclave by the exchange.
4. The scoring function runs: `score = log(bid) - distance² / σ²`. The enclave returns only the winning ad and its price. The exchange never sees the query embedding, the losing bids' scores, or any user data.
5. Remote attestation proves to every participant — the chatbot, the exchange, every advertiser — that the published scoring function is what actually executed. Not "trust us." Verify it.

The user's query stays on the chatbot's infrastructure. The auction executes in a sealed enclave. The exchange provides demand (advertiser bids) without accessing supply (user queries). The chatbot gets ad revenue without a conflict of interest. The user gets a cryptographic guarantee, not a promise.

## One Exchange Already Has This

[CloudX](https://github.com/cloudx-io/openauction) runs TEE-attested auctions today. Their clearing code executes inside AWS Nitro Enclaves with the auction logic open-sourced in Go. Every bidder can verify via remote attestation that the published code — and only the published code — processed their bid.

What CloudX doesn't have is embedding-space scoring. Their auctions clear on keywords and categories, like everyone else. The [extension](/letter-to-cloudx) is small: three optional fields (`embedding`, `embedding_model`, `sigma`) that let advertisers specify a position in vector space and a targeting radius. Keywords keep working as before — a keyword bid is just `sigma = 0`. Zero regression.

CloudX also doesn't have chatbot inventory. They have mobile app install campaigns. The TEE infrastructure is proven. The demand network is growing. What's missing is a chatbot platform willing to be the first supply-side partner.

## What the First Partner Gets

The first chatbot platform to route through an attested exchange gets three things no one else has:

**Ad revenue without trust damage.** The sealed auction architecture lets the platform say — provably, not promissorily — that user queries never leave their infrastructure and that ad selection is independent of answer generation. That's a stronger position than "no ads" (which doesn't pay the bills) and infinitely stronger than "trust us" (which degrades over time).

**No ad team.** No ad sales staff. No advertiser onboarding. No targeting infrastructure. No brand safety tooling. The exchange handles demand. The chatbot handles supply. The TEE handles trust. The chatbot company focuses on what it's good at — answering questions — and lets the exchange do what it's good at — running auctions.

**Protocol leverage.** The first supply-side partner shapes the protocol. What embedding model? What scoring function? What fields in the bid request? What attestation requirements? The exchange and the first chatbot platform negotiate these together. Everyone who comes after adopts what they defined. First-mover advantage in protocols is durable — ask TCP/IP.

## What CloudX Gets

The chatbot platform's queries turn CloudX from a mobile app install exchange into the clearing house for LLM conversation inventory — the most valuable new ad category since mobile.

Chatbot queries are high-intent, conversational, and continuous. *My finger hurts after climbing, should I see a PT?* is not a pageview. It's a declared intent with more targeting signal than any cookie or behavioral profile ever produced. Advertisers will pay premium CPMs for this inventory because the conversion signal is direct — the person said what they need.

CloudX already has the trust infrastructure that makes chatbot platforms comfortable routing through them. The TEE attestation isn't a feature — it's the reason a chatbot platform would choose them over PubMatic or Google Ad Exchange. No other exchange can cryptographically prove the query embedding stayed sealed.

The first chatbot partner provides the supply. CloudX provides the trust. The embedding auction provides the mechanism. The combination creates a marketplace that no participant can build alone.

## The Timing

Perplexity killed ads two weeks ago. They haven't announced what comes next. Anthropic says no ads — but inference costs don't care about brand positioning. Every chatbot platform with a free tier is working on the same problem right now.

The platforms that move first define the architecture. The platforms that wait adopt someone else's terms — probably OpenAI's closed system or Google's, once they extend Ad Exchange to chatbot inventory.

An open, attested exchange is the alternative to both. But it only works if a chatbot platform provides the supply. The exchange can't auction inventory it doesn't have.

The mechanism is [described](/power-diagrams-ad-auctions). The trust infrastructure [exists](https://github.com/cloudx-io/openauction). The [simulation](/keyword-tax) shows the economics work. The sealed auction architecture preserves user trust.

Someone has to plug in first.

---

*Part of the [adtech](/adtech) series. Written with help from Claude Opus 4.6.*
