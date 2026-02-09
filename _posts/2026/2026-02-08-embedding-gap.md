---
layout: post
title: "The $200 Billion Bottleneck: Why LLM Advertising Is Stuck in Keyword Space"
tags: coding
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the research; Claude surveyed the landscape, analyzed the protocol gap, and drafted prose.*

*A follow-up to [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions)*

---

There are now at least half a dozen startups racing to become the DoubleClick of AI advertising. I've been tracking this space since writing about power diagrams as an auction mechanism for continuous embedding space, and after surveying the landscape, I'm struck by something: nobody is actually building what they need to build.

Every company in this space — the startups, the incumbents, the LLM platforms themselves — is working around the same bottleneck. They all know that LLM conversations encode richer intent signals than keywords ever did. They all talk about "contextual targeting" and "understanding user intent." But when the ad actually needs to be served, every single one of them collapses the continuous, high-dimensional embedding space down to discrete categories and runs a standard auction. The richness gets thrown away at the exact moment it matters most.

This post is about the specific technical gap, who's doing what, and what it would actually take to close it.

## The Players

### Startups Building Ad Networks for AI

**Kontext** ($10M seed, M13/Torch Capital) is the furthest along. Founded in 2023 by Andrej Kiska, they generate ads in real-time using the host app's own LLM to analyze conversation context. They're integrated with PubMatic, an SSP, which means their inventory is accessible through standard programmatic pipes. Their investor Torch Capital explicitly describes them as building "the AppLovin / TradeDesk / DoubleClick of the GenAI era." Publishers include DeepAI, Pixel Chat, Liner. Advertisers include Amazon, Uber, Canva. They report 3-5% CTR at $2-4 CPMs.

**ZeroClick** ($55M, same investors who backed Honey to its $4B PayPal exit) takes a different approach. Founded by Ryan Hudson, the name is literally a nod to DoubleClick. They call themselves a "reasoning-time ad network" — advertiser context gets injected into the LLM's reasoning process *before* the answer is generated, not appended afterward. The ad becomes part of the answer. They claim 10,000+ advertisers including Walmart, Amazon, Target.

**Koah Labs** ($5M seed, Forerunner) targets the long tail of AI apps — the Luzias and DeepAIs of the world, especially in markets where subscription models don't work. Already live in several apps, claiming 7.5% CTR. Their pitch: we're the AdMob for AI chatbots.

### Incumbents Extending Existing Infrastructure

**PubMatic** routes AI chatbot inventory through its existing exchange via its partnership with Kontext. Their EVP explicitly said he doesn't see the channel as "very different from the general programmatic benefits." This is the incumbent mental model: AI chat is just another supply source in existing pipes.

**Criteo** is repositioning its massive commerce dataset (720M daily active users, billions of SKUs) as the data layer for LLM product recommendations. They've built an MCP server so LLMs can query Criteo's product data during response generation. The business model is still undefined.

**Seedtag** is the most technically interesting incumbent. They've been doing embedding-based contextual advertising on the open web for years, using what they call "neuro-contextual" targeting. Their AI uses embeddings to model interest, emotion, and intent. They claim 3.5x higher neural engagement versus non-contextual ads. They have the closest thing to actual embedding-space infrastructure, but they're applying it to display and CTV on the open web, not to ads inside LLM conversations.

### LLM Platforms Building Walled Gardens

**OpenAI** is testing ads in ChatGPT for free/Go tier users. Internal documents show $1B in "free user monetization" targets for 2026, growing to $25B by 2029. They hired Fidji Simo (ex-Instacart CEO, who scaled that company's ad business) to run applications. Built-in checkout with Shopify, Etsy, Walmart. This will almost certainly be a closed system.

**Google** already has ads in AI Overviews and AI Mode. They have the infrastructure and won't need a third party.

**Perplexity** tried ads in November 2024, paused accepting new advertisers by October 2025. They generated $20,000 in ad revenue out of $34M total in 2024. The ad sales head departed. They've essentially admitted the ad model doesn't work yet at their scale.

## What Everyone Is Actually Doing

Here's the thing that ties all of these together: **at the moment an auction needs to clear, every single one of them falls back to categorical targeting.**

When PubMatic says they're routing Kontext's AI chatbot inventory through programmatic pipes, what they mean concretely is: someone analyzes the conversation, classifies it into IAB content taxonomy categories (roughly 700 discrete labels like "Sports > Basketball" or "Technology > Computing"), stuffs those categories into an OpenRTB bid request, and sends it to DSPs who bid on categories the same way they've bid on categories for fifteen years.

The continuous embedding — the thing that captures the gradations between "I'm vaguely curious about running" and "I need marathon training shoes by next week and my knees hurt" — gets collapsed into a single label before it enters the auction. The entire signal advantage of embedding-based understanding gets destroyed at the protocol boundary.

## The Protocol Bottleneck

The root cause is OpenRTB, the protocol that the $200B+ programmatic advertising market runs on.

OpenRTB is maintained by the IAB Tech Lab. It defines the bid request format — the JSON object that an exchange sends to DSPs when an impression becomes available. The content targeting lives in categorical fields. There is literally no field for an embedding vector. You cannot express "this impression lives at coordinates [0.23, -0.41, 0.87, ...] in a 768-dimensional intent space." You cannot express an advertiser's value function as a region in that space. The protocol cannot represent the thing that makes LLM conversations valuable for targeting.

The bid request looks like this:

```json
{
  "site": { "cat": ["IAB7-1", "IAB17-18"] },
  "device": { "type": "mobile" },
  "geo": { "country": "US", "region": "NY" },
  "user": { ... },
  "imp": { "bidfloor": 0.50 }
}
```

That `cat` field — a handful of category labels from a fixed taxonomy — is the totality of what the protocol can express about what the conversation is about.

Will OpenRTB be updated? Probably not, for structural reasons. The IAB is a trade body whose members are the existing adtech companies. The spec evolves by committee consensus. Adding an embedding field is technically trivial — it's just a new array in the JSON. But it would break the entire downstream ecosystem. Every DSP has campaign management built around categorical targeting. Every reporting system aggregates by category. Every brand safety tool classifies by category. And the incumbents on the committee would be voting to destroy their own competitive advantage — their optimization moats are built on categorical signals.

What's more likely is one of three outcomes:

1. **Extension**: The IAB adds an optional `embedding` field as a supplementary signal alongside categories. DSPs ignore it if they want. Embeddings become just another feature in existing optimization, not a new auction paradigm. The power diagram geometry never happens.

2. **Parallel spec**: Someone writes a new protocol specifically for AI conversation inventory, coexisting with OpenRTB.

3. **De facto standard**: A dominant player builds an embedding-based system, everyone conforms to their implementation, and the IAB eventually standardizes what already exists.

History suggests option 3. Google didn't wait for the IAB to standardize programmatic — they built DoubleClick Ad Exchange and everyone conformed. Header bidding was standardized by Prebid.js after publishers had already adopted it. The protocol follows market power, not the other way around.

## What the Replacement Looks Like

The embedding-based bid request would carry a dense vector alongside standard metadata:

```json
{
  "embedding": [0.23, -0.41, 0.87, ...],
  "embedding_spec": "v1.0",
  "geo": { "country": "US", "region": "NY" },
  "device": { "type": "mobile" },
  "publisher": "chatgpt",
  "imp": { "bidfloor": 0.50 }
}
```

Everything outside the embedding field is basically OpenRTB as-is. Geo, device, time, language — these stay as structured metadata fields. The embedding represents only the semantic content and intent of the conversation. This is the right separation: the embedding captures *what the conversation is about*, the metadata captures *context about the user and session*. Different kinds of information, no reason to force them into the same representation.

The actual hard problems in the protocol are:

**Embedding alignment.** Different LLM platforms produce different embedding spaces. The protocol needs to define a common space, or a standard mapping between platform-specific spaces. Without this, an advertiser's value function means different things on different platforms, and the cross-platform exchange concept collapses.

**Value function representation.** How advertisers express what they want. Instead of bidding on categories, they'd specify a center point, a spread, and optionally directional preferences — essentially defining a region they value in embedding space. The simplest version: an isotropic Gaussian `v(x) = b · exp(-||x - c||² / σ²)`. More expressive: anisotropic Gaussians or Gaussian mixtures. The protocol needs to standardize a vocabulary of allowed function shapes.

**Auction mechanism.** Winner determination changes from "highest bid on this category" to "evaluate overlapping value functions at this point in embedding space." When value functions are isotropic Gaussians with shared spread, the resulting partition of space is a power diagram — a well-studied geometric structure with clean properties. (I wrote about this in detail in the [previous post](/power-diagrams-ad-auctions).)

**Latency.** Can you clear a geometric auction in the ~100ms window that programmatic requires? For the isotropic case with spatial indexing, yes — O(log N) winner determination. For mixture-of-Gaussian value functions, the computational cost scales with the number of mixture components, but precomputation helps.

## What Happens Next

The most likely near-term path:

1. OpenAI launches ads with a proprietary system, probably keyword/category-based initially because that's what their hired adtech people know how to build.
2. Kontext and ZeroClick continue growing as ad networks for the long tail, each with bespoke publisher integrations.
3. Someone — possibly Seedtag leveraging their existing embedding infrastructure, possibly a new entrant, possibly one of the startups pivoting — builds the first embedding-native exchange.
4. That exchange demonstrates a measurable performance advantage (higher CTR, better conversion, lower waste) over categorical targeting in AI conversations.
5. The performance delta pulls in advertiser demand.
6. The IAB eventually standardizes whatever the winning implementation looks like.

The race isn't to build the biggest ad network. It's to define the coordinate system.

---

*I write about the intersection of mechanism design and AI systems. Previously: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions). If you're working on this problem, I'd like to hear from you — june@june.kim.*
