---
layout: post
title: "Adtech: Keywords Are Tiny Circles"
tags: coding
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose and worked through the mechanics.*

*Part of a series: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap)*

---

The previous posts in this series have a problem. They describe a mathematically elegant system — [power diagrams](/power-diagrams-ad-auctions) partitioning embedding space, [hill-climbing UX](/buying-space-not-keywords) for navigating it, a [new protocol](/embedding-gap) to carry embedding vectors. And they implicitly ask the market to throw away keywords and adopt continuous geometry instead.

The market will not do this. Not because the math is wrong. Because the migration path demands a regression.

A mesothelioma law firm in Denver generates $50,000/month in conversions from exact-match keywords at $200/click. Their media buyer knows the spend, knows the win rate, knows the ROI to the penny. Tell them their keywords now live in a 3,072-dimensional vector space and they'll fire you by lunch. Even if the new system is strictly better in theory, the transition requires trusting that the new machinery reproduces the old behavior *exactly*. Nobody trusts that on day one.

Every successful platform transition solves this the same way. The new system is a strict superset of the old one. Old behavior is a special case, not a casualty. HTML didn't replace plain text — plain text is valid HTML. HTTPS didn't replace HTTP — it added a layer.

I kept looking at this problem and realized: keywords and embeddings already have this relationship. It's hiding in plain sight.

## A Keyword Is a Point with a Very Small Radius

Take "mesothelioma lawyer." Embed it. You get a point in 3,072-dimensional space. Now set the reach parameter σ to something tiny — σ → 0. The [power diagram](/power-diagrams-ad-auctions) score function:

```
score(x) = log(bid) - ||x - center||² / σ²
```

With σ near zero, the score drops to negative infinity for any point that isn't almost exactly at the keyword's embedding. Territory collapses to a single point. The auction at that point is second-price on bid. That's what Google runs today.

Keywords aren't replaced by embeddings. Keywords *are* embeddings. The degenerate case where reach is zero.

![Keywords are tiny circles — same points, different radii](/assets/09_keywords_are_tiny_circles.jpg)

The entire difference between keyword advertising and embedding-space advertising is one parameter: **σ**.

| σ | What happens | Current analog |
|---|----------|--------|
| ≈ 0 | Wins only at exact match | Keyword auction |
| Small | Wins for close paraphrases | Broad match |
| Medium | Wins for related topics | Topic targeting |
| Large | Wins across a semantic neighborhood | Interest-based |

Google's match types are already an informal version of this. Exact match is σ ≈ 0. Broad match is Google expanding your radius behind the scenes, using their own embedding model, without telling you the geometry. You don't control the radius. You don't see it. You select "broad match" and trust the black box.

The power diagram makes the radius explicit. You set σ. You see the territory. You see the price.

## Priority Falls Out of the Math

Here's why this is safe. Tight-radius bids take priority at their center point — not because of a special rule, but because the score function guarantees it.

A conversation embedding lands on "mesothelioma lawyer." Two bidders:

1. Keyword advertiser: σ ≈ 0, bid $200
2. Vector advertiser targeting "legal services": σ = 0.5, bid $50

At the keyword point:

```
Keyword:  log(200) - 0² / 0.001² = 5.30
Vector:   log(50)  - d² / 0.25   = 3.91 - 4d²
```

The keyword advertiser wins by a mile. σ² in the denominator concentrates all competitive power at the center. A sniper beats a shotgun at the sniper's chosen point.

Move slightly away — toward "asbestos exposure health risks" — and the keyword score collapses while the vector score barely changes. The vector bidder picks up adjacent territory that keywords can't reach.

No regression for keyword buyers. No wasted impressions for vector buyers. They coexist at different scales. The migration is a gradient: every advertiser enters at σ ≈ 0 and expands at their own pace. Or never expands at all. Keywords keep working forever. They're just very small circles.

## What Each Layer Ships

I mapped out what each layer of the ad tech stack actually needs to change. It's less than I expected.

**The DSP** adds one optional field. A keyword campaign already specifies keywords and bids. Default σ = 0. Campaign behaves identically — nothing changes for the advertiser, the optimization model, or reporting. For advertisers who opt in: a σ slider per keyword. One more parameter to tune, no different from bid adjustments by device or geography. Reporting adds one column: "Your keyword 'mesothelioma lawyer' won 1,200 impressions at exact match and 3,400 additional impressions within σ = 0.08."

**The SSP** makes one promise: keyword demand clears first at keyword points. When a publisher's impression matches a keyword, keyword bidders dominate because their scores are maximally concentrated. Every existing contract clears exactly as before. What embedding adds is coverage of the empty space — the majority of LLM conversation impressions that don't match any keyword and currently go unfilled or clear at remnant CPMs. The pitch to publishers: "Your keyword revenue is unchanged. We added a demand layer that fills the gaps."

**The exchange** runs one auction. One score function. Every bidder — keyword or vector — evaluated by the same formula. σ_i ≈ 0 for keywords, σ_i > 0 for vectors. One code path, not two. Two ways to enter:

A keyword bid:

```json
{
  "keywords": ["mesothelioma lawyer"],
  "cat": ["IAB11-4"],
  "sigma": 0.0
}
```

The `keywords` field already exists. `sigma` is the only new parameter — defaults to 0 if omitted. The exchange embeds the keywords into coordinates using an open-weight model. Because the weights are public, any participant can verify the embedding by running the same model on the same input. No code change required on the DSP side.

A vector bid:

```json
{
  "embedding": [0.23, -0.41, 0.87, ...],
  "embedding_model": "nomic/nomic-embed-text-v1.5",
  "sigma": 0.15
}
```

DSPs that want full control over their position send the vector directly. The `embedding_model` field tells the exchange which coordinate system the vector lives in — a vector in one model's space means something different in another's. This is the advanced path for targeting concepts that aren't keywords: "high-intent fitness shoppers considering a career change" has no keyword, but it has coordinates.

Both enter the same auction. There is no legacy demand. There's only demand at various radii.

## Who Enforces the Score Function

Open standards in ad tech have a pattern. A spec gets published. Dominant players implement it with proprietary extensions. The "open" part erodes into a lowest-common-denominator compatibility layer. OpenRTB is nominally open, but every major exchange interprets it differently. A score function like `log(b) - d²/σ²` would suffer the same fate — unless the exchange can prove it's running the published code unmodified.

That's what TEE attestation does. [CloudX](https://github.com/cloudx-io/openauction) is currently the only ad exchange running auction logic inside a TEE — AWS Nitro Enclaves, clearing code open-sourced in Go. The enclave's attestation document proves to every bidder that the published code, and only the published code, processed their bid. DSPs don't trust the exchange. They verify the attestation.

Google uses TEEs in advertising too, but for the opposite purpose. Privacy Sandbox uses enclaves to keep user data opaque during targeting. TEEs for privacy. CloudX uses TEEs to make the auction itself transparent. Different problem, nearly opposite trust model.

Once DSPs start routing demand preferentially to exchanges they can verify, every other exchange faces a choice: adopt TEE attestation or explain why bidders should trust on faith. Adding `sigma` to an attested auction is a code change to a public repository, not a proprietary platform decision. The embedding step doesn't need to live inside the enclave — open weights make it independently verifiable. The auction is what needs attestation.

## Keywords Forever

σ ≈ 0 is not legacy mode. It's the optimal strategy for high-value narrow-intent queries. The mesothelioma law firm *wants* σ ≈ 0 — concentrate every dollar of competitive power on the exact query that converts. Not training wheels. A sniper rifle.

Removing keyword support would mean removing σ = 0 from the parameter space. Like removing zero from arithmetic. It doesn't make sense as a concept. Every SSP, DSP, and exchange can promise their constituents that keywords work forever because keywords aren't a compatibility shim. They *are* the system.

The business case isn't replacing keyword revenue. It's the 80% of LLM conversation impressions that don't match any keyword — impressions that go unfilled today. With vector bids in the same auction, they don't. Purely additive. Every intermediary takes a cut of revenue that didn't exist before.

Keywords are tiny circles. The system that runs tiny circles already runs big circles. The rest is adoption.

---

*Previously: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap). If you're working on this problem, I'd like to hear from you — june@june.kim.*
