---
layout: post
title: "Axes of Exclusion"
tags: vector-space
---

*Part of the [Vector Space](/vector-space) series. Builds on [Marketing-Speak Is the Protocol](/marketing-speak-is-the-protocol).*

### The filter nobody built

A therapist wants to advertise on a depression recovery blog. YouTube says no — the content mentions suicide, so it's not "advertiser-friendly." The therapist is exactly the right advertiser for exactly the right audience, and the platform's filter blocks the match. The blog loses revenue. The therapist loses reach. The reader doesn't find help.

A children's learning channel gets demonetized because a video discusses bullying. An educational toy company would pay a premium for that audience. The binary label can't distinguish "content about a hard topic" from "content that's unsafe for advertisers." So it blocks everything.

Every ad platform has this filter. YouTube's is a binary label on content. Advertisers pick from coarse category blocklists. The tools are blunt because the architecture is blunt: one label per video, one blocklist per advertiser, no publisher-specific preferences.

The real constraint is per-publisher. A mental health blog needs to exclude gambling and predatory lending with high precision. A single bad ad erodes trust built over years. But therapy services, wellness apps, and financial literacy resources should get through. A kids' learning site needs tight filtering on audience, loose filtering on service type. Educational toys, tutoring, healthy snacks, children's books are all fine.

Lexical filtering (keyword blocklists, IAB categories) can't express this. "Gambling" blocks the casino resort's restaurant ad. "Debt" blocks the financial literacy course. The filter operates on surface tokens, not meaning. Semantic filtering would know the difference. But semantic filtering in high-dimensional embedding space has its own problems: distance concentrates, regions are expensive to define, and brute-force comparison is intractable at scale.

The missing piece is better constraints.

### The protocol gives the factorization for free

[Marketing-speak is the protocol](/marketing-speak-is-the-protocol) established that both sides of the market speak in positioning statements: **what** we do, for **who**, in what **situation**. The intent extraction prompt rewrites user language into the same format. A positioning statement has three semantic axes. Embed each field independently instead of collapsing the whole statement into one 768-dimensional vector:

- **What** (service type): "sports injury rehab" → d₁ ≈ 128 dims
- **Who** (audience): "competitive athletes" → d₂ ≈ 128 dims
- **Situation** (qualifier): "need to keep training through recovery" → d₃ ≈ 128 dims

Three small embeddings instead of one big one. The protocol enforces the factorization at input time.

This kills the hardest problem in Kronecker factorization. For arbitrary embeddings, finding the optimal coordinate partition is NP-hard. For positioning statements, the advertiser already gave you the partition when they filled in the form.

### Trees over axes

A tree over the **what** axis clusters advertisers by service type. "Sports rehab," "divorce mediation," "roof repair" land in different branches. A tree over the **who** axis clusters by audience. A tree over the **situation** axis clusters by qualifier.

Publisher exclusion becomes axis-aligned:

- A mental health blog excludes branches on the **what** tree: gambling, predatory lending, alcohol. Doesn't touch **who** or **situation**. Therapy services, wellness apps, financial literacy — all pass, because the service is appropriate even though the content is sensitive.
- A kids' learning site excludes branches on the **who** tree: anything targeting adults. Service type can be broad — educational toys, tutoring, healthy snacks, children's books all pass. The audience is the constraint, not the category.
- A political news site excludes certain **situation** branches — campaign-season qualifiers — to avoid appearing partisan. Service and audience are fine.

Each exclusion checks one 128-dimensional embedding. One-third the dimensions, one-third the cost per comparison, and the ability to skip entire axes when the exclusion doesn't apply.

Storage per publisher: a sparse bitfield over each axis tree. A publisher with ten exclusion rules across three axes stores maybe a hundred node IDs. Megabytes for millions of publishers.

### Conjunctions and the gray zone

One-axis exclusion is clean when the publisher means "no X regardless of context." But some exclusions are conjunctive: "no crypto for minors" means exclude the intersection of a **what** branch (crypto) and a **who** branch (minors).

Conjunctive exclusions require checking two axes — but that's still two cheap 128-dim comparisons, not one expensive joint comparison. The system checks **what** first (is this crypto?), and only if that matches, checks **who** (is the audience minors?). The first axis prunes most candidates; the second axis refines.

Then there's the gray zone. A financial planning ad on a depression recovery blog isn't harmful — it might even help. But it's not *relevant* in the way a therapy service ad would be. The publisher doesn't want to block it. They want to shape what gets through.

Axis-aligned exclusion handles the hard cases: things the publisher will never tolerate regardless of engagement. A recovery site will never serve gambling ads. That's editorial, not learned. But the gray zone — ads that are tolerable in some directions and not others — needs a softer boundary. One that learns from clicks and bounces which semantic directions to tighten and which to loosen. That's [the gate](/shape-of-the-gate), the twin of this post. Axes prune the branches. The gate shapes what remains.

The pipeline: **hard prune (axes) → soft gate → auction**. Two per-publisher filters, different timescales. Exclusion bitfields are set at onboarding and rarely change. The gate learns continuously from engagement. Both use the same factored axes.

The compound filter is stronger than either alone. Axes remove the obviously bad ads cheaply, so the gate only sees ads that are at least tolerable. M doesn't waste its learning budget on gambling-on-a-recovery-site — axes handled that. M spends all its signal on the subtle distinctions: which wellness ads this audience clicks, which financial services feel predatory in this context. Each filter can be individually looser because the other one backstops it. False positive rates multiply: 2% through axes, 5% through the gate, 0.1% compound.

### Per-axis σ

[Marketing-speak is the protocol](/marketing-speak-is-the-protocol) mentioned [σ](/keywords-are-tiny-circles) — the reach parameter that controls how broadly an advertiser matches. With factored embeddings, σ becomes a vector:

- **σ_what** = large: "I'm broadly a rehab clinic, match me to anything sports-medicine-adjacent"
- **σ_who** = small: "I specifically serve competitive athletes, not weekend joggers"
- **σ_situation** = large: "Any situation — pre-surgery, post-injury, maintenance, whatever"

Per-axis σ maps to tree depth on each axis. Large σ means the advertiser is relevant at shallow levels of that tree (wide match). Small σ means they're relevant only at deep levels (narrow match). The advertiser controls their own reach along each semantic axis independently.

Google Ads has broad match, phrase match, and exact match — three settings that control query interpretation, not semantic reach. Per-axis σ is more expressive: an advertiser can be broad on service type, narrow on audience, and broad on situation, all at once. No keyword system can express this because keywords don't have axes.

### Adaptive escalation

Not every routing decision is equally hard. An ad that's obviously "automotive" gets routed in one cheap comparison on the **what** axis. An ad on the boundary between "gaming" and "entertainment" is ambiguous.

The adaptive strategy: at each tree node, compute the **margin** — the contrast between the best and second-best child. If the margin is large, route cheaply. If it's small (ambiguous), escalate to finer comparison before committing.

The gain is concrete: in simulation, with 20% of nodes ambiguous across 6 tree levels, adaptive escalation lifts recall from 0.58 to 0.84 at the same total computational cost. The optimal escalation threshold should be larger near the root — a wrong decision at depth 1 wastes more downstream work than at depth 5.

For the ad system, this means per-publisher escalation thresholds. A publisher with dense exclusions has more ambiguous boundaries and should escalate more often. A permissive publisher rarely needs to escalate. The threshold can be estimated from each publisher's margin distribution in serving logs.

### What the constraints kill

The general theory of high-dimensional search has several impossibility results. The protocol constraints make most of them irrelevant:

| General impossibility | What kills it |
|---|---|
| Coordinate partition is NP-hard | Protocol structures the axes at input time |
| Distance concentrates in high-d | Per-axis σ declares tolerance; 128-d per axis, not 768-d joint |
| Tree search degrades to linear scan | Three 128-d trees degrade slower than one 768-d tree |
| Kronecker rank depends on alignment | Alignment is guaranteed by the protocol format |
| Exclusion surfaces are hard to specify | Axis-aligned exclusion from structured protocol fields |
| Cold-start for new publishers | Exclusions map to shared semantic axes, not learned regions |

Do the axis-separated embeddings actually capture enough of the positioning semantics for axis-aligned exclusion to work? "Sports injury rehab" embedded alone carries less context than "sports injury rehab for competitive athletes who need to keep training." The situation axis modifies the what axis. Embedding them separately might lose the interaction.

The experiment: 20-100K positioning statements, field-separated embeddings vs monolithic. Measure prune rate at fixed false-exclusion rate. Go if >50% candidate pruning at <3% false exclusions.

### Maintenance

Positioning statements are brand identity. They change quarterly, not hourly. The tree over positioning embeddings is nearly static. The fast-moving part is the query side (user intent), not the index side (advertiser positioning).

New advertisers go into a small buffer, filtered by brute-force similarity to publisher exclusion examples until the next tree rebuild (daily or weekly). By the time an advertiser is high-volume, they've been placed in the tree with proper bitfield coverage.

This is cheaper than it sounds. The tree has thousands of nodes, not millions. Rebuilds are offline, parallelizable, and infrequent. The operational cost is dominated by serving, not maintenance, and serving is three 128-dim tree traversals with bitfield lookups — microseconds.

### Co-design

Current ad filtering assembles independent components: an embedding model, an index, a filter, a scoring function. Each optimized in isolation. The filter doesn't know about the index. The index doesn't know about the exclusion criterion.

The protocol changes this. Positioning format → factorized embeddings → axis trees → exclusion bitfields → relevance scores. Each step follows from the previous. Nothing is designed in isolation because the protocol connects everything.

No single component is novel. Per-publisher exclusion, axis-aligned filtering, tree-based indexing, adaptive escalation: each exists somewhere. The combination requires a protocol that factors the input before the embedding does. [Marketing-speak](/marketing-speak-is-the-protocol) is that protocol. The therapist reaches the recovery blog. The toy company reaches the kids' channel.

---

*Part of the [Vector Space](/vector-space) series. Written via the [double loop](/double-loop).*
