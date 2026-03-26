---
layout: post
title: "Shape of the Gate"
tags: vector-space
---

Publishers need control over which ads reach their users. The [scoring function](/three-levers) gives them [τ](/set-it-and-forget-it) — a relevance threshold. Ads within τ distance of the query enter the auction. The rest are filtered.

τ is a sphere. Same radius in every direction.

A kids' education site runs the system for a month. A college savings ad clears the threshold — relevant to parents, adjacent to education. Users click. Then a sports betting ad clears the same threshold. Same distance from the query, different direction entirely. Users bounce. The publisher tightens τ. Now the college savings ad gets filtered too.

This is the sphere's failure mode. A health site cares intensely about the difference between wellness and pharmaceuticals but barely distinguishes cooking from gardening. A tech blog needs precision on crypto versus fintech but treats all lifestyle content as flat. Every publisher has directions they care about and directions they don't. τ can't tell them apart. Tighten it to block the bad direction and you lose the good one. Loosen it to keep the good one and the bad one leaks through.

The [PID controller](/set-it-and-forget-it) that tunes τ already sees the data it would need to do better. It sees which ads caused bounces and which got clicks. It sees the embedding vectors of both query and ad. Right now it throws the directional information away. A bounce tightens the sphere uniformly. That directional signal — which part of embedding space the match was good or bad in — is the difference between "ads are too irrelevant" and "ads are irrelevant *in this specific way*."

The natural fix is an ellipsoid — tight where the publisher's audience rejects, loose where they accept. But a general ellipsoid in 384 dimensions is 150,000 parameters. No publisher has the data, and exact membership testing at auction latency looks intractable.

It doesn't have to be exact. A diagonal approximation — one weight per dimension, 384 parameters — is a weighted L2 norm. Same cost as the sphere. It can't capture every correlation, but it captures the common case: some semantic directions matter more to this publisher than others. Start as a sphere. Get smarter.

## One Lever, Two Loops

The publisher already sets [one number](/set-it-and-forget-it): "10% of conversations should include a recommendation." A PID controller adjusts τ to hit that target.

A second, slower loop adjusts M — the diagonal metric. Same click/bounce stream, different job. PID controls *how much* filtering. M controls *where*. They don't fight because they operate on different timescales: τ responds in minutes, M shifts over days. τ compensates for short-term distortion M introduces. M reduces the variance τ has to absorb.

The publisher never sees M. One number in, smarter filtering out.

## Bootstrapping

M doesn't have to start cold. Before going live, surface borderline query–ad pairs — real or generated — for human review. "Would you show this ad next to this article?" A few hundred labels pre-shape the diagonal. The online loop refines from there.

With a bootstrapped M, the publisher can loosen τ. The sphere forces a tradeoff: safety or reach. The pre-shaped ellipsoid breaks it — further out in trusted directions, tight in untrusted ones, before serving a single impression.

## The Dirty Signal

Clicks conflate relevance with creative quality. Bounces conflate bad matches with slow load times. If M learns aggressively, it becomes a CDN-performance proxy, not a relevance boundary.

Three safeguards. Regularization toward I: dimensions with sparse signal stay near 1. Update caps: no single impression warps the metric. Daily decay: weights drift back toward 1, so seasonal shifts don't permanently reshape the filter.

M handles cases the publisher *can't anticipate*. A blocklist handles the cases they *can* — editorial stances that engagement data won't express.

## The Metric

Each weight starts at 1 and drifts based on where bounces and clicks concentrate. [ITML](https://jmlr.org/papers/v8/davis07a.html) (Davis et al., 2007) is one viable algorithm — online, KL-regularized toward I, O(d) per update in the diagonal case. Online logistic regression or per-dimension EMAs work too. The algorithm matters less than the structure: diagonal, regularized, online, decayed.

If diagonal proves too blunt: M = D + VVᵀ. Low-rank term (k = 5) captures correlated directions. 2,304 parameters. But start diagonal. Earn the complexity.

## Where M Lives

M is a pre-auction filter. Inside the gate, the [scoring function](/three-levers) runs unchanged: `score_i(x) = log(b_i) − ‖x − c_i‖² / σ_i²`. M is the publisher's editorial boundary. The auction is the auction. Keeping them apart preserves the [power diagram](/power-diagrams-ad-auctions) geometry and VCG guarantees.

The gate's shape determines which ads compete. Better-shaped gates mean the right ads get through — better matches, fewer bounces, [VCG payments](/one-shot-bidding) that reflect genuine relevance instead of geometric accidents. The welfare gain isn't more competition; it's better-sorted competition.

There's a harder question underneath: how much irrelevance is a publisher willing to tolerate for revenue? That tradeoff depends on direction and degree — exactly what M can inform but shouldn't decide. A separate lever, and a separate post.

---

*Part of the [Vector Space](/vector-space) series.*

*Adjacent work: per-query learned distance functions in [image retrieval](https://research.google/pubs/pub41900), [low-rank Mahalanobis learning](https://papers.nips.cc/paper/8369-fast-low-rank-metric-learning-for-large-scale-and-high-dimensional-data), [probabilistic retrieval thresholds](https://aclanthology.org/2025.emnlp-industry.161/), publisher-aware ad weighting in [patents](https://patents.google.com/patent/US9911135B2/en), [embedding-native ad retrieval](https://www.microsoft.com/en-us/research/publication/uni-retriever-towards-learning-the-unified-embedding-based-retriever-in-bing-sponsored-search/) at Bing, [ITML](https://jmlr.org/papers/v8/davis07a.html).*
