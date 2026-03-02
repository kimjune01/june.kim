---
layout: post
title: "The $200 Billion Bottleneck"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the research; Claude surveyed the landscape, analyzed the protocol gap, and drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

After writing about [power diagrams for ad auctions](/power-diagrams-ad-auctions), I started tracking the companies actually trying to sell ads inside LLM conversations. There are at least half a dozen startups racing to become the DoubleClick of AI advertising. What struck me: nobody is running auctions in embedding space.

Every company — startups, incumbents, LLM platforms — knows that embeddings encode richer intent signals than keywords ever did. They all talk about "contextual targeting" and "understanding user intent." But when the ad actually needs to be served, every single one collapses the continuous embedding down to discrete categories and runs a standard keyword-style auction. The richness gets thrown away at the exact moment it matters most.

## The Players

### Startups

**Kontext** ($10M seed, M13/Torch Capital) is furthest along. Founded 2023 by Andrej Kiska, they generate ads in real-time using the host app's LLM to analyze conversation context. Integrated with PubMatic for programmatic. Their investors call them "the AppLovin / TradeDesk / DoubleClick of the GenAI era." Publishers include DeepAI, Pixel Chat, Liner. Advertisers include Amazon, Uber, Canva. 3-5% CTR at $2-4 CPMs.

**ZeroClick** ($55M, same investors who backed Honey to its $4B PayPal exit). Ryan Hudson's "reasoning-time ad network" — advertiser context gets injected into the LLM's reasoning *before* the answer is generated, not appended after. The ad becomes part of the answer. 10,000+ advertisers including Walmart, Amazon, Target.

**Koah Labs** ($5M seed, Forerunner) targets the long tail of AI apps — the Luzias and DeepAIs, especially markets where subscriptions don't work. 7.5% CTR. Their pitch: we're AdMob for AI chatbots.

### Incumbents

**PubMatic** routes AI chatbot inventory through its existing exchange via Kontext. Their EVP said he doesn't see the channel as "very different from the general programmatic benefits." To them, AI chat is just another ad slot — not a fundamentally different kind of inventory.

**Criteo** is repositioning its commerce dataset (720M daily active users, billions of SKUs) as the data layer for LLM recommendations. They built an MCP server so LLMs can query their product data during response generation. Business model still undefined.

**Seedtag** is the most interesting technically. They've been doing embedding-based contextual advertising on the open web for years — "neuro-contextual" targeting that models interest, emotion, and intent. 3.5x higher engagement versus non-contextual. They have the closest thing to actual embedding-space infrastructure, but they're applying it to display and CTV, not LLM conversations.

### Walled Gardens

**OpenAI** is testing ads in ChatGPT for free/Go tier users. Internal targets: $1B in "free user monetization" for 2026, $25B by 2029. Hired Fidji Simo (scaled Instacart's ad business) to run applications. Built-in checkout with Shopify, Etsy, Walmart. Almost certainly a closed system.

**Google** already has ads in AI Overviews and AI Mode. They don't need a third party.

**Perplexity** tried ads November 2024, paused new advertisers by October 2025. $20,000 in ad revenue out of $34M total in 2024. Ad sales head departed. The ad model doesn't work yet at their scale.

## Everyone Falls Back to Categories

Here's what ties all of these together: **at the moment an auction needs to clear, every one falls back to categorical targeting.**

"Routing AI chatbot inventory through programmatic pipes" concretely means: analyze the conversation, classify it into ~700 IAB taxonomy labels like "Sports > Basketball" or "Technology > Computing," stuff those into an OpenRTB bid request, send to DSPs who bid on categories the same way they've been bidding for fifteen years.

The continuous embedding — the thing that captures the difference between "I'm vaguely curious about running" and "I need marathon training shoes by next week and my knees hurt" — gets collapsed into a single label before entering the auction. The entire embedding — intent level, specificity, price sensitivity — gets destroyed at the protocol boundary.

## The Protocol Problem

The root cause is OpenRTB, the protocol the $200B+ programmatic market runs on.

The IAB Tech Lab maintains it. The bid request format has categorical fields for content targeting. There's no field for an embedding vector. You can't express "this impression lives at coordinates [0.23, -0.41, 0.87, ...] in a 768-dimensional intent space." The protocol can't carry an embedding vector — the thing that actually makes LLM conversation targeting better than keywords.

```json
{
  "site": { "cat": ["IAB7-1", "IAB17-18"] },
  "device": { "type": "mobile" },
  "geo": { "country": "US", "region": "NY" },
  "user": { ... },
  "imp": { "bidfloor": 0.50 }
}
```

That `cat` field is everything the protocol can say about what the conversation is about.

Will OpenRTB get updated? Probably not. The IAB is a trade body whose members are the existing adtech companies. Adding an embedding field is technically trivial — just a new array in the JSON. But it would break every DSP's campaign management, every reporting system, every brand safety tool. The incumbents on the committee would be voting to destroy their own optimization moats.

Three likely outcomes:

1. **Extension**: Optional `embedding` field alongside categories. DSPs ignore it if they want. Embeddings become just another feature, not a new paradigm.

2. **Parallel spec**: Someone writes a new protocol for AI conversation inventory.

3. **De facto standard**: A dominant player builds an embedding-based system, everyone conforms, the IAB eventually standardizes what already exists.

History says option 3. Google didn't wait for the IAB — they built DoubleClick Ad Exchange and everyone conformed. Prebid.js standardized header bidding after publishers had already adopted it. Protocol follows market power, not the other way around.

## What the Replacement Looks Like

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

Everything outside the embedding field is basically OpenRTB as-is. The embedding captures *what the conversation is about*. The metadata captures *context about user and session*. Different information, no reason to force it into the same representation.

The hard problems:

**Embedding alignment.** Different platforms produce different embedding spaces. The protocol needs a common space, or standard mappings between them. Without this, an advertiser's value function means different things on different platforms and cross-platform exchange collapses.

**Value functions.** Instead of bidding on categories, advertisers specify a center, spread, and directional preferences — a region in embedding space. Simplest version: isotropic Gaussian `v(x) = b · exp(-||x - c||² / σ²)`. More expressive: anisotropic or mixtures. The protocol needs to standardize what shapes are allowed.

**Auction clearing.** "Highest bid on this category" becomes "evaluate overlapping value functions at this point." For isotropic Gaussians, the result is a [power diagram](/power-diagrams-ad-auctions) with clean properties.

**Latency.** Can you clear a geometric auction in ~100ms? Isotropic case with spatial indexing: yes, O(log N). Mixtures scale with components, but precomputation helps.

## What Happens Next

1. OpenAI launches ads with a proprietary system, probably keyword/category-based initially because that's what their adtech hires know how to build.
2. Kontext and ZeroClick keep growing as ad networks for the long tail, each with bespoke integrations.
3. Someone — possibly Seedtag leveraging existing embedding infrastructure, possibly a new entrant — builds the first embedding-native exchange.
4. That exchange shows a measurable performance advantage over categorical targeting in AI conversations.
5. The performance delta pulls in advertiser demand.
6. The IAB eventually standardizes whatever won.

The race isn't to build the biggest ad network. It's to define the coordinate system.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
