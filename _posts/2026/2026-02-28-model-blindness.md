---
layout: post
title: "Model Blindness"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched prior art and drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

[Ask First](/ask-first) described what the user experiences: a two-phase model where suggestions appear outside the conversation, the chatbot doesn't generate them, and no ad fires until the user opts in. This post describes why the UX isn't lying — the architecture that makes model independence provable, not promised.

## The Industry Is Going the Other Direction

The dominant trend in chatbot advertising is deeper integration of ads into the model, not separation from it.

Alibaba's research lab published [LLM-Auction](https://arxiv.org/abs/2512.10551), which post-trains the model via RLHF to balance ad revenue and user experience. The model's weights encode commercial incentives directly. [Kontext](https://pubmatic.com/blog/pubmatic-and-kontext-partner-to-open-programmatic-access-to-ai-powered-conversational-inventory/), the SSP bridging PubMatic to chatbot inventory, uses the *same LLM* powering the chatbot to generate contextual ads. [Google Research's RAG-based ad auction](https://arxiv.org/abs/2406.09459) puts ads into the model's context window via retrieval — the model explicitly sees the ad content during inference.

The integration approach has a concrete problem beyond trust. Fine-tuning is too slow — ad campaigns change hourly, training takes weeks. Too expensive — retraining a frontier model per campaign rotation is economically absurd. And too vulnerable — whoever controls the training data controls what the model recommends, and you can't audit learned bias in weights the way you can audit a scoring function. An auction clears in milliseconds and updates in real time. A training run doesn't.

OpenAI claims their ads run on "separate systems" — what they call the [Answer Independence Principle](https://openai.com/index/our-approach-to-advertising-and-expanding-access/). But it's a policy claim with no attestation. No one outside OpenAI can verify the separation. [Simon Willison noted](https://simonwillison.net/2026/Jan/16/chatgpt-ads/) that ChatGPT includes an option to "Ask ChatGPT" about a specific ad — a user-initiated bridge across the supposed architectural boundary. The separation has a door in it.

## Why Users Can't Self-Police

A team at Michigan [fine-tuned a 14B model to serve targeted ads](https://arxiv.org/abs/2409.15436) — Phi-4-Ads — and ran it past human evaluators. The results: users *couldn't detect the embedded ads*. Worse, they *preferred* responses with hidden advertisements. Ad injection degraded model performance by at most 3%.

This is the strongest argument for architectural enforcement. If users can't tell when a response is commercially influenced, then no amount of labeling, transparency reports, or user education fixes the problem. The system has to enforce separation because humans can't detect violations. Trust can't rest on vigilance.

## The Architecture

The chatbot cannot see the ad system. This is not a policy. It's construction.

The conversation model runs in its own enclave. The ad system runs in a separate enclave. There is no communication channel from the ad system to the conversation model. The chatbot cannot know whether a suggestion appeared, whether the user opted in, or who the advertiser was. It can't steer the conversation toward purchase intent because it has no signal that purchase intent is monetizable.

The only data flow: conversation → embedding → ad system → UI. One-directional. The chatbot is downstream of nothing commercial.

Perplexity killed ads because first-party selection destroyed trust. OpenAI kept ads and ate the trust damage. Model blindness is the third option: run ads and preserve trust, because the model generating your answer provably doesn't know the ads exist.

This requires the ad system to be operated by a third party — not Perplexity, not the chatbot provider. If the same company runs the conversation and the auction, the separation is a policy again, not a constraint. A third-party exchange inside a TEE enclave is the only arrangement where no single entity controls both the answers and the ads.

## The Infrastructure Exists

The components for this are in production. The integrated system is not.

**TEE-attested auctions.** [CloudX](https://github.com/cloudx-io/openauction) runs ad auctions inside AWS Nitro Enclaves with open-source clearing code. PCR measurements prove the exact code running inside the enclave. No one — not the platform, not the exchange operator, not the cloud provider — can tamper with the auction.

**GPU-isolated inference.** The [NVIDIA H100](https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/) supports confidential computing with a hardware TEE. Performance overhead is below 5%. Model inference inside a sealed enclave runs at production speed.

**Confidential inferencing platforms.** [Azure confidential inferencing](https://techcommunity.microsoft.com/blog/azureconfidentialcomputingblog/azure-ai-confidential-inferencing-technical-deep-dive/4253150) provides end-to-end prompt protection with AMD SEV-SNP enclaves. The model developer, service operator, and cloud provider are all excluded from accessing prompts.

**Browser-side TEE auctions.** Google's [Protected Audience API](https://github.com/privacysandbox/protected-auction-services-docs/blob/main/trusted_services_overview.md) already runs ad auctions inside TEEs at scale with open-source, externally verifiable binaries.

**[Information flow control](https://arxiv.org/abs/2311.15792)** for ML pipelines provides the theoretical framework: treat ad content as a restricted information class and enforce one-directional flow at the architecture level.

Each component exists in production individually. Assembling the trust layer is integration work — though the auction mechanism itself still has open research questions around [equilibrium convergence](/power-diagrams-ad-auctions) and [parameter calibration](/synthetic-friction).

## The Trust Chain

Four links. Every one verifiable.

1. **Verifiable intent matching.** [Open-weight embedding models](/the-convergence) with published hashes. Anyone can reproduce the embedding and verify the auction scored it correctly.
2. **Verifiable auction execution.** A [sealed TEE enclave](/perplexity-was-right-to-kill-ads) running attested code. The scoring function is published, audited, and cryptographically proven to be what executed.
3. **Model independence.** The chatbot provably cannot access the ad system. Separate enclaves, one-directional data flow, attested separation. The answers can't be biased by advertising because the model doesn't know advertising exists.
4. **User-initiated impressions.** No ad appears without a deliberate action. The [user asks first](/ask-first).

Break any link and you're back to the same extractive ad layer wearing a new interface. Hold all four and you have advertising that the chatbot can honestly ignore, the user can honestly consent to, and the advertiser can honestly pay for.

Nothing in this architecture is specific to chatbots. If the embedding is computed on-device and the proximity check runs against a cached advertiser index, the same indicator could work in any conversation — including between humans. A user who opts into the recommender gets the dot in their messaging app. The conversation never leaves the device for ad purposes. The person on the other end doesn't know it's on. This is the strongest version of "ask first": you asked before any conversation even started.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
