---
layout: post
title: "Model Blindness"
tags: adtech
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched prior art and drafted prose.*

*Part of the [adtech](/adtech) series.*

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

This is a stronger claim than "our answers are independent of advertising." It's: our answers *can't* be dependent on advertising because the model has no access to the ad system. Architectural impossibility, not a promise.

Perplexity killed ads because first-party selection destroyed trust. OpenAI kept ads and ate the trust damage. Model blindness is the third option: run ads and preserve trust, because the model generating your answer provably doesn't know the ads exist.

## The Infrastructure Exists

The components for this are in production. The integrated system is not.

**TEE-attested auctions.** [CloudX](https://github.com/cloudx-io/openauction) runs ad auctions inside AWS Nitro Enclaves with open-source clearing code. Their three-zone architecture — untrusted host, trust boundary, and sealed enclave — enforces that even if the host is fully compromised, encrypted bids can't be decrypted and auction state can't be manipulated. PCR measurements prove the exact code running inside the enclave. This is the template for how you'd run an ad auction that no one — not the platform, not the exchange operator, not the cloud provider — can tamper with.

**GPU-isolated inference.** The [NVIDIA H100](https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus-for-secure-and-trustworthy-ai/) supports confidential computing with a hardware TEE. Data transfers between CPU and GPU are encrypted through bounce buffers. In TEE mode, the GPU operates in full isolation. Performance overhead for typical LLM queries is below 5%. You can run model inference inside a sealed enclave at production speed.

**Confidential inferencing platforms.** [Azure confidential inferencing](https://techcommunity.microsoft.com/blog/azureconfidentialcomputingblog/azure-ai-confidential-inferencing-technical-deep-dive/4253150) provides end-to-end prompt protection with AMD SEV-SNP enclaves. Containers run in sandboxed environments with read-only filesystems and limited outbound communication. Prompts are encrypted and can only be decrypted within the inferencing TEE. The model developer, service operator, and cloud provider are all excluded from accessing sensitive data.

**Browser-side TEE auctions.** Google's [Protected Audience API](https://github.com/privacysandbox/protected-auction-services-docs/blob/main/trusted_services_overview.md) runs ad auctions inside TEEs at scale — bidding and auction services in Nitro Enclaves and GCP Confidential Space, with open-source binaries that external parties can verify. This is the closest production analogue: an ad system that runs alongside content generation without the content-generation system seeing bid data or selection logic.

**Information flow control.** Academic work on [information flow control for ML pipelines](https://arxiv.org/abs/2311.15792) provides the theoretical framework: treat ad content as a restricted information class, enforce one-directional flow at the architecture level, and use retrieval boundaries to ensure the model only surfaces information it's authorized to access. The separation isn't ad hoc — it follows established principles for controlling data flow in multi-component systems.

The conversation enclave runs the model. The ad enclave runs the auction. Attestation proves they share no state. Each component exists in production individually. Assembling them is engineering, not research.

## The Trust Chain

Four links. Every one verifiable.

1. **Verifiable intent matching.** [Open-weight embedding models](/the-convergence) with published hashes. Anyone can reproduce the embedding and verify the auction scored it correctly.
2. **Verifiable auction execution.** A [sealed TEE enclave](/perplexity-was-right-to-kill-ads) running attested code. The scoring function is published, audited, and cryptographically proven to be what executed.
3. **Model independence.** The chatbot provably cannot access the ad system. Separate enclaves, one-directional data flow, attested separation. The answers can't be biased by advertising because the model doesn't know advertising exists.
4. **User-initiated impressions.** No ad appears without a deliberate action. The [user asks first](/ask-first).

Break any link and you're back to the same extractive ad layer wearing a new interface. Hold all four and you have advertising that the chatbot can honestly ignore, the user can honestly consent to, and the advertiser can honestly pay for.

---

*Part of the [adtech](/adtech) series. june@june.kim*
