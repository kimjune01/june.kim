---
layout: post
title: "Adtech: The Convergence"
tags: coding
---

*Part of a series: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap) · [Keywords Are Tiny Circles](/keywords-are-tiny-circles) · [It Costs Money to Move](/relocation-fees) · [An Open Letter to CloudX](/letter-to-cloudx)*

---

The pieces of embedding-space advertising are being built independently by groups that don't talk to each other. Academics publish auction mechanisms for LLM-native ads. Industry labs deploy embedding infrastructure at scale. Standards bodies draft TEE specifications. Platform companies launch walled-garden ad products. Each group is solving a piece of the same problem without referencing the others' work.

This post is a map. It surveys who is working on what, where the threads connect, and what nobody is saying yet.

## The Auction Mechanism

Three recent papers tackle the core question: how do you run an auction when the inventory is an LLM conversation rather than a keyword slot?

**Hajiaghayi et al. (2024)** at Google Research and the University of Maryland proposed [Ad Auctions for LLMs via Retrieval Augmented Generation](https://arxiv.org/abs/2406.09459), published at NeurIPS 2024. Their model treats each discourse segment of an LLM response as an auction opportunity. Ads are probabilistically retrieved based on bid and relevance through a RAG framework, maximizing a "logarithmic social welfare" objective that balances efficiency and fairness with incentive-compatible pricing. The retrieval step *is* the allocation mechanism — relevance scoring in the RAG pipeline and auction allocation collapse into one operation.

**Zhao et al. (2025)** at Alibaba's Taobao & Tmall Group introduced [LLM-Auction](https://arxiv.org/abs/2512.10551), the first generative auction where the LLM itself serves as the allocation rule. Rather than selecting from pre-existing ad slots, the system integrates auction outcomes into LLM generation using an Iterative Reward-Preference Optimization (IRPO) algorithm. The auction object shifts from discrete ad slots to the distribution over LLM outputs — the model's response *is* the ad allocation. This is also the approach that is structurally impossible to audit. The allocation rule is baked into the model weights. No advertiser can verify why their ad was or wasn't shown. No user can verify that response quality wasn't traded for revenue. The platform can optimize for whatever it wants and call it "relevance" — and nobody outside the company can prove otherwise.

Both papers build on foundations laid by **Liu et al. (2021)** in [Neural Auction](https://arxiv.org/abs/2106.03593), published at KDD 2021. Their Deep Neural Auctions (DNAs) use differentiable relaxations of discrete sorting to enable end-to-end auction learning. The system was deployed in Taobao's production advertising, demonstrating that learned auction mechanisms can outperform hand-designed ones at scale. Neural Auction didn't target LLM conversations — it targeted e-commerce display — but it established that embedding-space representations and neural network-based allocation can replace the hand-crafted rules of traditional auctions.

All three operate in continuous vector space rather than over discrete keyword sets. The auction clears at a point in embedding space, not at a keyword string. This is the same structure described in the [power diagram formulation](/power-diagrams-ad-auctions) from this series: `score(x) = log(bid) - distance² / σ²`, where the winner at any point is the advertiser with the highest bid-adjusted proximity. The academic work validates the core premise — auctions can operate natively in embedding space — while leaving the exchange infrastructure and trust layers as open problems.

## The Infrastructure

The embedding infrastructure for ad targeting already exists. It was built for recommendation systems, not auctions, but the technical substrate is the same.

**Twitter/X** published [TwHIN](https://arxiv.org/abs/2202.05387) (El-Kishky et al., KDD 2022), embedding entities from Twitter's heterogeneous information network — users, content, advertisers — where edges encode interactions like follows, engagements, and ad clicks. These embeddings serve as features across the platform's recommendation pipeline, including ad ranking, account recommendations, and search. Separately, Twitter/X's [SplitNet architecture](https://blog.x.com/engineering/en_us/topics/infrastructure/2019/splitnet-architecture-for-ad-candidate-ranking) uses a two-tower model for ads specifically: user features and ad features are fed into separate deep networks, producing dense embeddings whose dot product determines relevance. The two-tower pattern — embed both sides of a marketplace into the same space, match by proximity — is now the default architecture for large-scale ad systems.

**Criteo** has built the most commerce-specific embedding infrastructure in the industry. Their [CLEPR model](https://medium.com/criteo-engineering/leveraging-commerce-data-for-outcome-based-relevancy-in-agentic-recommendation-systems-717d62589ec3) (Contrastive Language Embedding for Product Retrieval) is a 120M-parameter two-tower bi-encoder fine-tuned on organic click data, reporting a 37% improvement in outcome-based relevancy over zero-shot text encoders from the MTEB leaderboard (MiniLM, Gemma, Qwen). Their [DeepKNN](https://www.criteo.com/blog/optimizing-advertising-performance-with-advanced-machine-learning-and-vector-database-technology/) vector database engine already powers their retargeting recommendations. What's missing is an auction mechanism that operates on these embeddings — Criteo still routes through categorical programmatic pipes.

**OpenAI** began [testing ads in ChatGPT](https://openai.com/index/our-approach-to-advertising-and-expanding-access/) on February 9, 2026 — the first production ad system inside a major LLM conversation product. Ads appear below answers for Free and Go tier users ($0 and $8/month), clearly labeled as sponsored. OpenAI claims no influence on response content and no user data sold to advertisers. Internal revenue targets: [$1B in free-user monetization for 2026](https://techcrunch.com/2026/02/09/chatgpt-rolls-out-ads/). This is a closed system — OpenAI controls targeting, pricing, and allocation. The auction mechanism, if there is one, is not public.

The gap between infrastructure and auction design is the subject of [The $200 Billion Bottleneck](/embedding-gap) in this series. Every company listed above uses embeddings internally but collapses them to IAB taxonomy categories at the protocol boundary. The embedding — the thing that captures the difference between "vaguely curious about running" and "needs marathon training shoes by next week, has flat feet" — gets destroyed at exactly the moment the auction needs it.

## The Trust Layer

TEE (Trusted Execution Environment) attestation is entering advertising from three directions, each with a different trust model.

**Google** uses TEEs in the [Privacy Sandbox](https://github.com/privacysandbox/protected-auction-services-docs/blob/main/trusted_services_overview.md) to keep user data opaque during ad targeting. The Protected Audience API (formerly FLEDGE) runs Key/Value services and bidding/auction services inside cloud TEEs. The service code is open source and externally verifiable, and the [architectural reference](https://github.com/googleads/conf-data-processing-architecture-reference/blob/main/docs/TrustedExecutionEnvironmentsArchitecturalReference.md) specifies that even operators with admin privileges cannot access the data being processed. Users trust that their data stays private. Advertisers and publishers still trust Google to run the auction fairly. TEEs for privacy, not transparency.

**IAB Tech Lab** published a [whitepaper on TEEs in digital advertising](https://www.iab.com/wp-content/uploads/2025/04/IAB_Trusted_Execution_Environments_Whitepaper_April_2025.pdf) in April 2025, arguing that enclaves create a verifiable data processing environment that supports regulatory compliance and protects consumer privacy. The framing is privacy-first, aligned with Google's approach. The whitepaper is significant because it signals that the industry's standard-setting body recognizes TEEs as infrastructure, not a niche experiment.

**Mozilla** takes a third approach through [Anonym](https://blog.mozilla.org/en/advertising/using-trusted-execution-envrionments-for-advertising-use-cases/), its ad-tech subsidiary. Anonym uses Intel SGX enclaves on Microsoft Azure to process encrypted data from both advertisers and ad networks. Partner data is decrypted only inside the enclave, processed according to pre-approved algorithms, anonymized with differential privacy, and destroyed when the enclave spins down. Their [Transparency Portal](https://blog.mozilla.org/en/advertising/anonym-transparency-portal/) lets partners review algorithms before execution. Still privacy-oriented, but with an explicit transparency mechanism that the other approaches lack.

**CloudX** is the only ad exchange using TEEs for auction transparency rather than data privacy. [OpenAuction](https://github.com/cloudx-io/openauction) runs clearing code inside AWS Nitro Enclaves with the auction logic open-sourced in Go. The enclave's attestation document proves to every bidder that the published code — and only the published code — processed their bid. The auction itself is what's made transparent. DSPs don't trust the exchange on faith. They verify the attestation.

A scoring function like `log(bid) - distance² / σ²` is only trustworthy if the exchange proves it's evaluating it correctly. Open-weight embedding models (Nomic, BGE, GTE) provide the complement: any participant can verify the embedding step independently by running the same model on the same input. The exchange doesn't need to run embeddings inside the enclave — the auction is what needs attestation. The [Keywords Are Tiny Circles](/keywords-are-tiny-circles) post develops this argument in detail.

## The Discoverability Crisis

The channels that small businesses use to find customers are failing simultaneously.

SEO is collapsing under AI Overviews. A [Seer Interactive study](https://www.dataslayer.ai/blog/google-ai-overviews-the-end-of-traditional-ctr-and-how-to-adapt-in-2025) of 3,119 queries across 42 organizations found that organic CTR dropped 65% on queries where AI Overviews appeared — from 1.76% to 0.61%. Paid CTR fell 68%. Zero-click searches — where the user gets their answer without clicking any result — now account for [roughly 60% of queries](https://www.semrush.com/blog/ai-search-seo-traffic-study/). Individual publishers [report losses ranging from 25% to 90%](https://digiday.com/media/google-ai-overviews-linked-to-25-drop-in-publisher-referral-traffic-new-data-shows/) depending on their topic.

Social media selects for spectacle over expertise. A physical therapist who specializes in climbers' finger injuries — a real service that real people need — spends her evenings filming TikTok hooks instead of studying biomechanics. The content grind rewards click-through rates and average-percentage-viewed, not domain knowledge. Cory Doctorow's [enshittification thesis](https://doctorow.medium.com/big-techs-attention-rents-fe97ba3fad90) describes the structural dynamic: platforms first serve users, then exploit users for advertisers, then exploit advertisers to extract all remaining value. The [attention economy](https://www.promarket.org/2025/12/05/everything-enshittified-all-at-once/) produces platforms that optimize for engagement rather than connection.

Ben Thompson argued in [*Google, Nvidia, and OpenAI*](https://stratechery.com/2025/google-nvidia-and-openai/) (December 2025) that "ChatGPT should obviously have an advertising model" — not just for revenue, but because "advertising would make ChatGPT a better product" by capturing purchase signals that create a richer understanding of individual users. He called OpenAI's refusal to launch an ads product three years after ChatGPT's debut "a dereliction of business duty." Thompson's Aggregator Theory framework predicts that the company with the most unique users, monetized through advertising, commoditizes its suppliers and wins.

The standards bodies see it too. IAB Tech Lab [formed the Content Monetization Protocols (CoMP) Working Group](https://iabtechlab.com/press-releases/iab-tech-lab-forms-ai-content-monetization-protocols-comp-working-group-to-set-ai-era-publisher-monetization-standards/) in August 2025, inviting OpenAI, Anthropic, Google, Meta, and Perplexity to develop standards for publisher monetization in the AI era — covering content crawl management, LLM discovery, and monetization models. The working group's existence is an institutional acknowledgment that the chatbot is becoming the primary internet interface and that no monetization standard exists for it.

The question looming over all of this: when the buyer's agent is an LLM processing embedding vectors rather than a person scanning banner ads, what does the auction mechanism need to look like? The auction needs to operate in the space where the AI actually represents intent.

## The Missing Piece

Each group has a piece:

- **Academics** have auction mechanisms that work in embedding space (Hajiaghayi et al., Zhao et al., Liu et al.)
- **Industry labs** have production-grade embedding infrastructure for intent matching (Criteo, Twitter/X, Google)
- **Standards bodies** have TEE specifications and working groups for AI-era monetization (IAB Tech Lab, Google Privacy Sandbox)
- **Platform companies** have the inventory and the users (OpenAI, Google, Perplexity)
- **One exchange** has TEE attestation for auction transparency (CloudX)
- **Open-weight model maintainers** have verifiable embedding infrastructure (Nomic, BGE, GTE)

Nobody has assembled the complete architecture. No published system combines TEE-attested auctions + embedding-space allocation + open-weight model verification + mechanism design that handles the geometric properties of continuous space. The academic papers assume a trusted auctioneer. The industry infrastructure assumes categorical targeting at the protocol boundary. The TEE work focuses on privacy rather than auction transparency. The platform companies are building walled gardens.

And nobody is framing high-resolution targeting as infrastructure for human connection.

The niche businesses described in the [open letter](/letter-to-cloudx) — the physical therapist for climbers, the financial planner for freelance translators, the ADHD math tutor — can't exist at keyword resolution. Their audience is too small and too specific to win a broad auction. At embedding resolution, they can [plant a flag](/buying-space-not-keywords) at exactly their niche and reach exactly the people who need them. That's not advertising as interruption. That's advertising as introduction — a direct line between one person's problem and another person's expertise.

The discoverability collapse is the forcing function. When SEO dies, social media selects for spectacle, and the chatbot becomes the primary internet interface, the question isn't whether LLM conversations will carry ads. They already do. The question is whether the ad layer operates at keyword resolution — reproducing the same low-resolution targeting in a new medium — or at embedding resolution, where the geometry can actually match a person's need to another person's expertise.

## What Comes Next

The convergence is happening whether anyone coordinates it or not. The academic mechanisms will improve. The infrastructure will scale. The standards will eventually follow the market. The question is whether the result is another walled garden — OpenAI's closed ad system, opaque and unverifiable — or an open, auditable system where every participant can verify the scoring function, the embeddings, and the allocation.

The technical pieces exist. Embedding-space auctions have been demonstrated in peer-reviewed work. Two-tower architectures serve billions of ad requests daily. TEE attestation runs in production. Open-weight embedding models produce verifiable coordinates. [Relocation fees](/relocation-fees) solve the stability problem that frictionless continuous auctions create. [Keywords coexist as a special case](/keywords-are-tiny-circles) — zero regression for existing demand.

Publishers need revenue as SEO collapses. Advertisers want higher-resolution targeting. Exchanges want new inventory categories. Small businesses need discoverability channels that don't require content grinds. The only participants whose incentives *don't* align are the platform companies that benefit from opaque, proprietary ad systems — the ones building walled gardens.

Someone needs to assemble the pieces. The [open letter](/letter-to-cloudx) makes the concrete case for who and how.

---

*Previously: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap) · [Keywords Are Tiny Circles](/keywords-are-tiny-circles) · [It Costs Money to Move](/relocation-fees) · [An Open Letter to CloudX](/letter-to-cloudx). Written with help from Claude Opus 4.6.*
