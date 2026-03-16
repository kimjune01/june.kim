![The bottleneck](/assets/embedding_gap.jpg)

After writing about [power diagrams for ad auctions](/power-diagrams-ad-auctions), I started tracking the companies actually trying to sell ads inside LLM conversations. There are at least half a dozen startups racing to become the DoubleClick of AI advertising. What struck me: no production ad exchange is running auctions in embedding space.

Every company on this list talks about "contextual targeting" and "understanding user intent." But when the ad actually needs to be served, nearly all of them run a standard keyword-style auction. The gap between what they promise and what the protocol can carry is the story.

## The Players

### Startups

**[Kontext](https://www.adweek.com/programmatic/pitch-deck-kontext-raises-10-million-funding-ads-in-ai-chatbots/)** ($10M seed, M13/Torch Capital) is furthest along. Founded 2023 by Andrej Kiska, they generate ads in real-time using the host app's LLM to analyze conversation context. Integrated with PubMatic for programmatic. Their investors call them "the AppLovin / TradeDesk / DoubleClick of the GenAI era." Publishers include DeepAI, Pixel Chat, Liner. Advertisers include Amazon, Uber, Canva. 3-5% CTR at $2-4 CPMs.

**[ZeroClick](https://www.adexchanger.com/commerce/honey-co-founder-ryan-hudson-has-a-new-plan-for-an-ai-ad-network/)** ($55M, same investors who backed [Honey](https://en.wikipedia.org/wiki/PayPal_Honey) to its $4B PayPal exit). Ryan Hudson's "reasoning-time ad network": advertiser context gets injected into the LLM's reasoning *before* the answer is generated, not appended after. The ad becomes part of the answer. 10,000+ advertisers including Walmart, Amazon, Target.

**Koah Labs** ($5M seed, Forerunner) targets the long tail of AI apps, the Luzias and DeepAIs, especially markets where subscriptions don't work. 7.5% CTR. Their pitch: we're AdMob for AI chatbots.

### Incumbents

**[PubMatic](https://en.wikipedia.org/wiki/Pubmatic)** routes AI chatbot inventory through its existing exchange via Kontext. Their EVP said he doesn't see the channel as "very different from the general programmatic benefits." To them, AI chat is just another ad slot, not a fundamentally different kind of inventory.

**[Criteo](https://en.wikipedia.org/wiki/Criteo)** is repositioning its commerce dataset (720M daily active users, billions of SKUs) as the data layer for LLM recommendations. They built an MCP server so LLMs can query their product data during response generation. Business model still undefined.

**Seedtag** is the most interesting technically. They've been doing embedding-based contextual advertising on the open web for years, with "neuro-contextual" targeting that models interest, emotion, and intent. 3.5x higher engagement versus non-contextual. They have the closest thing to actual embedding-space infrastructure, but they're applying it to display and CTV, not LLM conversations.

### Walled Gardens

**OpenAI** is testing ads in ChatGPT for free/Go tier users. Internal targets: $1B in "free user monetization" for 2026, $25B by 2029. Hired [Fidji Simo](https://en.wikipedia.org/wiki/Fidji_Simo) (scaled Instacart's ad business) to run applications. Built-in checkout with Shopify, Etsy, Walmart. Almost certainly a closed system.

**Google** already has ads in AI Overviews and AI Mode. They don't need a third party.

**Perplexity** tried ads November 2024, paused new advertisers by October 2025. $20,000 in ad revenue out of $34M total in 2024. Ad sales head departed. The ad model doesn't work yet at their scale.

## Everyone Falls Back to Categories

Here's what ties all of these together: **at the moment an auction needs to clear, every one falls back to categorical targeting.**

"Routing AI chatbot inventory through programmatic pipes" concretely means: analyze the conversation, classify it into ~700 IAB taxonomy labels like "Sports > Basketball" or "Technology > Computing," stuff those into an OpenRTB bid request, send to DSPs who bid on categories the same way they've been bidding for fifteen years.

The continuous embedding (the thing that captures the difference between "I'm vaguely curious about running" and "I need marathon training shoes by next week and my knees hurt") gets collapsed into a single label before entering the auction. The entire embedding gets destroyed at the protocol boundary. The cost goes beyond efficiency. [Sahni & Nair (2020)](https://academic.oup.com/restud/article-abstract/87/3/1529/5583745) showed experimentally that when ads are well-matched, disclosing "this is a paid ad" *increased* engagement by 77%. Consumers treat a precise match as a quality signal. [Sahni & Zhang (2024)](https://link.springer.com/article/10.1007/s11129-023-09270-z) found that reducing ad prominence actually decreased overall search usage, because relevant ads fill information gaps the organic algorithm can't. The signal that categories destroy is the signal that makes ads worth clicking.

## The Protocol Problem

The root cause is [OpenRTB](https://github.com/InteractiveAdvertisingBureau/openrtb), the protocol the $200B+ programmatic market runs on.

The [IAB Tech Lab](https://iabtechlab.com/) maintains it. The bid request format has categorical fields for content targeting. There's no field for an embedding vector. You can't express "this impression lives at coordinates [0.23, -0.41, 0.87, ...] in a 768-dimensional intent space." The protocol can't carry an embedding vector — the thing that actually makes LLM conversation targeting better than keywords.

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

Will OpenRTB get updated? Probably not. The IAB is a trade body whose members are the existing adtech companies. Adding an embedding field is technically trivial, just a new array in the JSON. But it would break every DSP's campaign management, every reporting system, every brand safety tool. The incumbents on the committee would be voting to destroy their own optimization moats.

Three likely outcomes:

1. **Extension**: Optional `embedding` field alongside categories. DSPs ignore it if they want. Embeddings become just another feature.

2. **Parallel spec**: Someone writes a new protocol for AI conversation inventory.

3. **De facto standard**: A dominant player builds an embedding-based system, everyone conforms, the IAB eventually standardizes what already exists.

History says option 3. Google didn't wait for the IAB. They built [DoubleClick Ad Exchange](https://www.adexchanger.com/ad-exchange-news/it-wasnt-a-job-it-was-a-cult-the-definitive-oral-history-of-doubleclick/) and everyone conformed. [Prebid.js](https://docs.prebid.org/overview/intro-to-header-bidding.html) standardized header bidding after publishers had already adopted it. Protocol follows market power, not the other way around.

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

**Value functions.** Instead of bidding on categories, advertisers specify a region in embedding space: a center point with spread, optionally stretched along preferred directions. Simplest version: isotropic Gaussian `v(x) = b · exp(-||x - c||² / σ²)`. More expressive: anisotropic or mixtures. The protocol needs to standardize what shapes are allowed.

**Auction clearing.** "Highest bid on this category" becomes "evaluate overlapping value functions at this point." For isotropic Gaussians, the result is a [power diagram](/power-diagrams-ad-auctions#power-diagrams) with clean properties.

**Latency.** Can you clear a geometric auction in ~100ms? Isotropic case with spatial indexing: yes, O(log N). Mixtures scale with components, but precomputation helps.

## What Happens Next

1. OpenAI launches ads with a proprietary system. It will almost certainly be keyword/category-based at first — that's what their adtech hires know how to build.
2. Kontext and ZeroClick keep growing as ad networks for the long tail, each with bespoke integrations.
3. Someone builds the first embedding-native exchange. Seedtag has the closest existing infrastructure; a new entrant has fewer legacy constraints. Either way, it happens.
4. That exchange demonstrates a measurable lift over categorical targeting in AI conversations — and the lift is large enough to move budgets.
5. The IAB eventually standardizes whatever won.

The real race is to define the coordinate system.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the research; Claude surveyed the landscape, analyzed the protocol gap, and drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
