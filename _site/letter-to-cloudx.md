I've spent the past few weeks writing about [vector-space ad auctions](/power-diagrams-ad-auctions), exploring how embedding geometry can replace keyword matching for LLM conversation inventory. The series kept circling back to an enforcement problem: the auction math only works if every participant can verify the exchange is running the published scoring function unmodified.

You've already built that. [openauction](https://github.com/cloudx-io/openauction) is the only live ad exchange where the auction code is public and the hardware proves it runs unmodified. Meta joined because attestation means they don't have to trust you. The cold start problem most ad tech startups spend years on, solved architecturally on day one.

## Discoverability Is Collapsing

Every lead gen channel for small businesses is failing simultaneously. SEO is dying. AI Overviews cannibalize organic results, and the first page is ads, AI summaries, and Reddit links. Paid search is keyword-resolution, back to the floor where niche businesses can't target precisely enough to compete. Short-form video works but selects for spectacle, not expertise. Referrals don't scale.

A physical therapist who specializes in climbers' finger injuries. A financial planner for freelance translators. These are real services that real people need, run by one or two people whose entire lead generation is an ad click. Right now, their best option is grinding out TikToks on a platform that rewards click-through rates and average-percentage-viewed over meaningful expertise. The physical therapist spends her evenings filming hooks instead of studying biomechanics. The content grind selects for vanity.

These businesses can't survive at keyword resolution. Their audience is too small and too specific to win a broad auction. At embedding resolution, they can [plant a flag](/buying-space-not-keywords) at exactly their niche and reach exactly the people who need them. Describe what you do, set a radius, and the auction matches you to people who need you. The targeting comes from the geometry, not the algorithm's appetite for engagement.

## Where People Are Going

The early internet was good at connecting people. You'd search for something specific, find a forum post by someone who'd solved exactly your problem, and email them. That got buried under AI-generated slop and noise in every channel.

Most people are migrating to AI chatbots as their primary interface to the internet: the place where they ask questions and make decisions. If the ad layer inside that chatbot is just keywords and categories, the same low-resolution targeting follows them there.

If it's embedding-space targeting, the chatbot becomes the primary discovery mechanism for human expertise. A conversation about training for a trail race surfaces a coach who actually specializes in that, not a generic shoe ad. A direct line between one person's problem and another person's expertise. Advertising as introduction.

The infrastructure to make this work is an auction that can operate at embedding resolution, on an exchange that participants can verify. That's what you have.

## The Extension

The case I want to make is narrow: your existing auction infrastructure can support embedding-space targeting with a few optional parameters and zero regressions for existing participants.

Today a bid has a keyword (or category) and a price. The extension adds two optional fields to the bid request:

```js
{
  "keywords": [],
  "cat": ["IAB17-18"],
  "embedding": [0.23, -0.41, 0.87, ...], // "flat-footed runner training for first half-marathon"
  "embedding_model": "nomic/nomic-embed-text-v1.5"
}
```

Both are optional. A bid request that omits them behaves identically to today: keyword match, σ = 0.

**`embedding`** and **`embedding_model`** carry the query's meaning from the publisher to the exchange. A vector in one model's space means something different in another's, so the model field is required when a vector is present. If omitted, the exchange embeds the keywords into coordinates using an open-weight model. Because the weights are public, any participant can verify the embedding independently, so the exchange doesn't need to run it inside the enclave. The auction is what needs attestation.

**`sigma`** is the advertiser's signal, not the publisher's. It controls how far a bid's influence extends from its center point. At σ = 0, the bid wins only at exact match, identical to a keyword bid. The scoring function is `log(bid) - distance² / σ²`. Every existing keyword bid is a bid with σ = 0. No regression. The [math guarantees it](/keywords-are-tiny-circles): tight-radius bids dominate at their center point because the σ² denominator concentrates all competitive power there. Sigma travels with the bid response or is stored on the exchange as part of the advertiser's profile.

DSPs that don't understand embeddings keep bidding on `keywords` and `cat`. Nothing changes for them. DSPs that understand the geometry add `embedding` and `embedding_model` to their bid requests, and `sigma` to their bids. All enter one auction. One code path. Meta's existing campaigns see identical behavior. New embedding-aware demand is purely additive.

## Why This Is Different in Your Exchange

Any exchange could add these fields. What makes your exchange different is that DSPs can verify the scoring function is evaluated correctly.

If a conventional exchange adds `sigma`, every DSP has to trust that the exchange is actually computing `log(bid) - distance² / σ²` and not applying proprietary adjustments, preferred-partner discounts, or opaque quality scores that quietly override the geometry. That trust doesn't exist. It's the reason OpenRTB standards erode: every exchange "implements" the spec differently and nobody can prove otherwise. [Boneh et al. (2010)](https://crypto.stanford.edu/adnostic/) identified this structural problem early: Adnostic moved ad targeting into the user's browser so the ad network couldn't see user interests. It was the first architecture where the party running the match was blind to the inputs. [Prio (Corrigan-Gibbs & Boneh, 2017)](https://arxiv.org/abs/1703.06255) extended the principle to aggregated measurement without exposing individual data, and [Liao, Corrigan-Gibbs & Boneh (2024)](https://petsymposium.org/popets/2024/popets-2024-0104.php) completed the toolkit with private billing via divisible e-cash. Your exchange applies the same principle to auction clearing: the party running the match proves the match was honest.

The embedding step is a separate problem with a separate solution. Open-weight models make it verifiable without attestation. Any participant can take the same input text, run the same model, and check that the exchange produced the correct vector. The embedding is a commodity service; the auction is what needs attestation.

In your exchange, a DSP sending bids, whether keyword or vector, can verify both layers: the enclave proves the scoring function, and the open weights prove the embeddings. No conventional exchange can offer that without rebuilding their infrastructure.

This means if you ship the embedding extension first, every DSP that wants verifiable embedding-space auctions has to route through you. That's a revenue advantage: you take a cut of every impression cleared through the only exchange where the geometry can be trusted.

## Timing

Every LLM conversation costs money; inference isn't free. The long tail of AI chatbots (Luzia, DeepAI, Liner) needs revenue to cover token costs for free users, and ads are the obvious model. ChatGPT has 800 million users. OpenAI is targeting $1B in free-user monetization for 2026. This inventory is growing fast, and no dominant exchange has locked it up yet.

Google doesn't own the exchange layer for third-party LLM conversations yet. The window to establish the standard is the period between "this inventory exists" and "Google has locked it up." Based on how fast Google moved on search (DoubleClick acquisition to dominance: roughly three years), that window is probably 18-36 months.

The other threat is closer. TEE attestation is an infrastructure choice, not a patent. PubMatic, Criteo, and every other incumbent exchange can adopt it. They already have the two-sided network (publishers and DSPs) that takes years to build. If they add attestation to their existing exchanges, they get trust plus network effects.

Your advantage right now is that you have attestation and they don't. That's temporary. What's durable is the two-sided network you build while you're the only attested exchange. The embedding extension accelerates that by creating demand and inventory that incumbents don't serve yet.

The mechanism design is [described in detail](/power-diagrams-ad-auctions) and free to implement. The missing piece is a trusted exchange that can run it verifiably. You have that. The question is whether you convert that head start into network effects before incumbents close the gap.

## What's Further Out

The series also covers [stability mechanisms](/relocation-fees): protocol-level relocation fees to prevent position gaming, open-weight model requirements for verifiable embedding, liquidity dynamics across competing models. These are real problems that will matter at scale, but they're second-order. The first-order question is whether embedding parameters can enter the auction without breaking anything for existing participants. The math says yes. The TEE makes it verifiable.

If the extension works and demand flows in, the stability mechanisms become tractable engineering problems inside the same attested codebase. They don't need to be solved on day one.

## The Ask

This isn't for today. Your mobile app install wedge is the right market to win first; it's where the demand is and where attestation already differentiates you. But the mobile wedge is a beachhead, not a destination. LLM conversation inventory is the territory that opens up next, and it needs an auction that works at embedding resolution.

Adding embedding-space targeting to your existing auction (one new parameter, an open-weight model for keyword conversion, optional raw vector bids for advanced DSPs) is a small change that prepares you for that expansion.

Incumbents can't move fast enough. PubMatic and Criteo are publicly traded companies with quarterly earnings calls and committees that need to approve protocol changes. Embedding-space auctions require an organization that thinks natively in vectors. The speed advantage of an AI-native team, shipping a new scoring function in weeks instead of quarters, is as much a moat as the TEE itself.

The competitive case is real, but the reason to build this is bigger than market share. The ad systems we have now force small businesses onto content treadmills and serve consumers ads that interrupt rather than help. An auction that operates at embedding resolution, verifiably, can connect people who need help to people who can provide it, at exactly the right moment.

If this is wrong, if the extension breaks something I'm not seeing or the market timing is off, I want to hear about it.

---

*Part of the [Vector Space](/vector-space) series. Written with help from Claude Opus 4.6.*
