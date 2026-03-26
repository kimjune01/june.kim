---
layout: post
title: "Shape of the Gate"
tags: vector-space
---

[Axes of exclusion](/axes-of-exclusion) handle the hard cases: ads a publisher will never tolerate. What passes the hard filter still needs a relevance gate. The [scoring function](/three-levers) gives publishers [τ](/set-it-and-forget-it), a relevance threshold: ads within τ distance of the query enter the auction.

τ is a sphere. Same radius in every direction.

A health chatbot shows a yoga mat ad next to a conversation about back pain. Users click. Then a pain clinic ad clears the same threshold. Same distance from the query, different direction entirely. Users bounce. The publisher tightens τ. Now the yoga mat ad gets filtered too.

Health is where this hurts most. The semantic space is dense with adjacent-but-dangerous directions: wellness ↔ supplements ↔ pharmaceuticals ↔ addiction treatment ↔ mental health. A nutrition ad is welcome; a weight-loss drug ad is a liability. Both live near "managing my health."

Every publisher has directions they care about and directions they don't. τ can't tell them apart. Tighten it to block the dangerous direction and you lose the safe one.

## The Wasted Signal

The [PID controller](/set-it-and-forget-it) that tunes τ already sees what it needs: which ads caused bounces, which got clicks, the embedding vectors of both. All that directional information gets thrown away. A bounce tightens the sphere uniformly. *Where* the match was good or bad? Discarded.

An ellipsoid would fix this: tight where the audience rejects, loose where they accept. But a full ellipsoid in 384 dimensions is 150,000 parameters. No publisher has the data.

A diagonal approximation does. One weight per dimension, 384 parameters, same cost as the sphere. It won't capture every correlation, but it captures the common case: some semantic directions matter more to this publisher than others. Start as a sphere. Get smarter.

## One Lever, Two Loops

The publisher already sets [one number](/set-it-and-forget-it): "10% of conversations should include a recommendation." A PID controller adjusts τ to hit that target.

A second, slower loop adjusts M, the diagonal metric, from the same click/bounce stream. PID controls *how much* filtering; M controls *where*. τ responds in minutes, M shifts over days. τ compensates for distortion M introduces; M reduces the variance τ has to absorb.

One number in, smarter filtering out.

## Twenty minutes of swipes

M doesn't have to start cold. Before going live, the publisher sits down for twenty minutes and swipes through borderline query–ad pairs, real or generated. "Would you show this ad next to this conversation?" Yes or no. A few hundred labels pre-shape the diagonal. The online loop refines from there.

With a bootstrapped M, the publisher can loosen τ. The sphere forces a tradeoff: safety or reach. The pre-shaped ellipsoid breaks it. Further out in trusted directions, tight in untrusted, before serving a single impression.

## The Dirty Signal

Clicks conflate relevance with creative quality. Bounces conflate bad matches with slow load times. If M learns aggressively, it becomes a CDN-performance proxy instead of a relevance boundary.

Three safeguards. Regularization toward I: dimensions with sparse signal stay near 1. Update caps: no single impression warps the metric. Daily decay: weights drift back toward 1, so seasonal shifts don't permanently reshape the filter.

## Earn the complexity

Each weight starts at 1 and drifts where bounces and clicks concentrate. Serving cost is one multiply per dimension, same as the sphere. The learning runs offline. [ITML](https://jmlr.org/papers/v8/davis07a.html) (Davis et al., 2007) works: online, KL-regularized toward I, O(d) per update when diagonal. Per-dimension EMAs work too. The algorithm matters less than the structure: diagonal, regularized, online, decayed.

If diagonal proves too blunt: M = D + VVᵀ. Low-rank term (k = 5) captures correlated directions. 2,304 parameters. But start diagonal.

M handles cases the publisher *can't anticipate*. [Axis-aligned exclusion](/axes-of-exclusion) handles the cases they *can* — editorial stances that engagement data won't express. Hard prune first, soft gate second. Axes remove the obvious cases, so M only sees ads worth learning about. Each filter can be looser because the other backstops it.

## Where M Lives

M lives publisher-side. The publisher computes it from their own engagement data and applies it locally during [phase one](/ask-first) matching, before any embedding enters the [TEE](/monetizing-the-untouchable). The exchange never sees M, the clicks that shaped it, or the conversations it filters. Axes and gate both run on the publisher's own infrastructure. The enclave only sees what survives.

M is a pre-auction filter. Inside the gate, the [scoring function](/three-levers) runs unchanged: `score_i(x) = log(b_i) − ‖x − c_i‖² / σ_i²`. The separation is the point: M is editorial, the auction is the auction. Keeping them apart preserves the [power diagram](/power-diagrams-ad-auctions) geometry and VCG guarantees.

The gate's shape determines which ads compete. Better shapes mean better matches, fewer bounces, and [VCG payments](/one-shot-bidding) that reflect relevance instead of geometric accidents.

How much irrelevance a publisher tolerates for revenue depends on direction and degree — exactly what M informs but shouldn't decide. A separate lever, a separate post. This one just shapes the gate.

---

*Part of the [Vector Space](/vector-space) series.*

*Adjacent work: per-query learned distance functions in [image retrieval](https://research.google/pubs/pub41900), [low-rank Mahalanobis learning](https://papers.nips.cc/paper/8369-fast-low-rank-metric-learning-for-large-scale-and-high-dimensional-data), [probabilistic retrieval thresholds](https://aclanthology.org/2025.emnlp-industry.161/), publisher-aware ad weighting in [patents](https://patents.google.com/patent/US9911135B2/en), [embedding-native ad retrieval](https://www.microsoft.com/en-us/research/publication/uni-retriever-towards-learning-the-unified-embedding-based-retriever-in-bing-sponsored-search/) at Bing, [ITML](https://jmlr.org/papers/v8/davis07a.html).*
