---
layout: post
title: "Perplexity Was Right to Kill Ads"
tags: vector-space
---

Perplexity [killed ads](https://web.archive.org/web/20260307185249/https://www.macrumors.com/2026/02/18/perplexity-abandons-ai-advertising/) in February 2026. Total ad revenue: [$20,000](https://digiday.com/media/perplexitys-ad-business-hasnt-exactly-been-a-hit/). The ad sales head left.

Their CEO's reasoning was simple: *a user needs to believe this is the best possible answer.* The moment a chatbot shows an ad it selected, that belief is gone. Did it recommend that product because it's best, or because someone paid?

He was right. But the real problem ran deeper than he thought.

## The Conflict

Perplexity *selected* the ads. When the chatbot platform runs its own ad system, it becomes both the user's agent and the advertiser's agent. That dual role is a structural conflict. No amount of labeling or visual separation fixes it.

OpenAI is demonstrating this in real time. [Ads at $60 CPM](https://web.archive.org/web/20260217041818/https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html), $200K minimum buy, targeting logic closed. No one outside OpenAI can verify how ads are selected or whether ad revenue influences answers. The gap between their inference costs ([$14 billion projected](https://web.archive.org/web/20260227151900/https://finance.yahoo.com/news/openais-own-forecast-predicts-14-150445813.html)) and ad revenue guarantees increasing pressure to extract more from every query. First-party ads start polite and get worse — that's [enshittification](https://web.archive.org/web/20251011164132/https://doctorow.medium.com/big-techs-attention-rents-fe97ba3fad90) applied to a new medium.

Perplexity saw the trajectory and pulled the plug. Correct.

But the conflict lives in the architecture, and it survived the revenue cut.

## The Obvious Fix and Its Problem

The obvious fix is to externalize the auction. The chatbot answers questions. A separate exchange runs the ads. This is how the web works: publishers route inventory through exchanges, not their own ad systems.

A chatbot doing this can honestly say: *we don't select ads. We don't know what ad you'll see. Our answers are independent of advertising.*

Except the exchange now sees your users' queries.

Embeddings encode intent. A query embedding for *my marriage is falling apart, should I see a therapist?* contains information the user didn't consent to share with an ad exchange. Embeddings can be [approximately reversed](https://arxiv.org/abs/2310.06816). Sending query embeddings to a third party is a privacy leak dressed up as an API call.

First-party ads create a conflict of interest. Externalized ads create a privacy leak. Either way, trust breaks.

## Run the Auction Inside

The solution is to run the external auction on the chatbot's own infrastructure, in a sealed enclave.

A trusted execution environment is a hardware enclave that proves what code is running inside it. AWS Nitro Enclaves, Intel SGX, AMD SEV. The key property: even the machine's operator can't see what's happening inside, and anyone can verify what code executed.

The architecture:

1. The chatbot embeds the query on its own infrastructure. The embedding never leaves.
2. A TEE enclave on that infrastructure receives the embedding and the exchange's advertiser bids.
3. The [scoring function](/power-diagrams-ad-auctions) runs inside the enclave: `score = log(bid) - distance² / σ²`.
4. The enclave returns only the winning ad and its price. The exchange never sees the query embedding.
5. Remote attestation proves to every participant that the published scoring function (and only that function) executed.

The user's query stays on the chatbot's infrastructure. The exchange provides demand without accessing supply. The chatbot gets ad revenue without a conflict of interest. The user gets a cryptographic guarantee instead of a promise.

This is not hypothetical. [CloudX](https://github.com/cloudx-io/openauction) runs TEE-attested auctions today in AWS Nitro Enclaves with open-sourced clearing code. They auction mobile app installs on keywords. The [extension](/letter-to-cloudx) to embedding-space scoring is three optional fields: `embedding`, `embedding_model`, `sigma`.

## What Perplexity Got Wrong

Perplexity correctly identified that first-party ads are incompatible with a trusted answer engine. The mistake was concluding that *all* ads are incompatible.

The conflict lives in the chatbot selecting the ad. Seal the selection in an enclave with attested code, and the chatbot can honestly say its answers are independent of advertising, because the ad system runs in hardware it can't access.

A sealed auction preserves trust, funds inference, and lets the chatbot [stay out of it](/ask-first). The remaining question is who selects the ads, and whether you can prove it.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
