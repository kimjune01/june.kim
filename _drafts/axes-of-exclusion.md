---
layout: post
title: "Axes of Exclusion"
tags: vector-space
---

*Part of the [Vector Space](/vector-space) series. Builds on [Marketing-Speak Is the Protocol](/marketing-speak-is-the-protocol).*

### The filter nobody built

A therapist wants to advertise on a depression recovery blog. YouTube says no — the content mentions suicide, so it's not "advertiser-friendly." The right advertiser, the right audience, and the filter blocks the match. The blog loses revenue. The therapist loses reach. The reader doesn't find help.

A children's learning channel gets demonetized because a video discusses bullying. An educational toy company would pay a premium for that audience. The binary label can't distinguish "content about a hard topic" from "content that's unsafe for advertisers." So it blocks everything.

Every ad platform has this filter. YouTube's is a binary label on content. Advertisers pick from coarse category blocklists. The tools are blunt because the architecture is blunt: one label per video, one blocklist per advertiser, no publisher-specific preferences.

The real constraint is per-publisher. A mental health blog needs to exclude gambling and predatory lending with high precision because a single bad ad erodes trust built over years. But therapy services, wellness apps, and financial literacy should get through. A kids' learning site needs tight filtering on audience, loose on service type.

Lexical filtering can't express this. "Gambling" blocks the casino resort's restaurant ad. "Debt" blocks the financial literacy course. The filter operates on surface tokens, not meaning. Semantic filtering could know the difference, but in high-dimensional embedding space, regions are expensive to define and evaluate at scale.

The missing piece is better constraints.

### Three axes, three embeddings

[Marketing-speak is the protocol](/marketing-speak-is-the-protocol) established that both sides speak in positioning statements: **what** we do, for **who**, in what **situation**. A positioning statement has three semantic axes. Embed each field independently:

- **What** (service type): "sports injury rehab" → d₁ ≈ 128 dims
- **Who** (audience): "competitive athletes" → d₂ ≈ 128 dims
- **Situation** (qualifier): "need to keep training through recovery" → d₃ ≈ 128 dims

Three small embeddings instead of one big one. The protocol enforces the factorization at input time.

This sidesteps one of the hardest parts of factorization: discovering the axes after the fact. The advertiser already gave you the partition when they filled in the form.

The tradeoff: embedding fields separately loses cross-field meaning. "Sports injury rehab" alone carries less context than the full positioning statement. The situation modifies the what. Whether the loss breaks axis-aligned exclusion is empirical. One experiment away from an answer.

### Trees over axes

A tree over the **what** axis clusters advertisers by service type: "sports rehab," "divorce mediation," "roof repair" land in different branches. Separate trees over **who** and **situation** cluster by audience and qualifier.

Publisher exclusion becomes axis-aligned:

- A mental health blog excludes branches on the **what** tree: gambling, predatory lending, alcohol. Doesn't touch **who** or **situation**. Therapy services, wellness apps, financial literacy — all pass, because the service is appropriate even though the content is sensitive.
- A kids' learning site excludes branches on the **who** tree: anything targeting adults. Service type can be broad — educational toys, tutoring, healthy snacks, children's books all pass. The audience is the constraint, not the category.
- A political news site excludes certain **situation** branches — campaign-season qualifiers — to avoid appearing partisan. Service and audience are fine.

Each exclusion checks one 128-dimensional embedding. One-third the dimensions, one-third the cost, and axes that don't apply get skipped entirely.

Storage per publisher: a sparse bitfield over each axis tree. A publisher with ten exclusion rules across three axes stores maybe a hundred node IDs.

### Conjunctions and the gray zone

One-axis exclusion is clean when the publisher means "no X regardless of context." But some exclusions are conjunctive: "no crypto for minors" means exclude the intersection of a **what** branch (crypto) and a **who** branch (minors).

Conjunctive exclusions check two axes: **what** first (is this crypto?), then **who** only if that matches (is the audience minors?). The first axis prunes most candidates; the second refines.

Then there's the gray zone. A financial planning ad on a depression recovery blog might even help. But it's not *relevant* in the way a therapy service ad would be. The publisher doesn't want to block it. They want to shape what gets through.

Axis-aligned exclusion handles the hard cases: things the publisher will never tolerate. That's editorial, not learned. But the gray zone needs a softer boundary that learns from clicks and bounces which directions to tighten. That's [the gate](/shape-of-the-gate), the twin of this post. Axes prune the branches. The gate shapes what remains.

### Three filters, one pipeline

**[Credibility](/proof-of-trust) → hard prune (axes) → [soft gate](/shape-of-the-gate) → auction.** Three per-publisher filters, different timescales. Credibility gates which advertisers enter the system. Exclusion bitfields are set at onboarding and rarely change. The gate learns continuously from engagement, and all three use the same factored axes.

The compound filter is stronger than any single layer. Axes remove the obviously bad ads cheaply, so the gate only sees tolerable candidates. It doesn't waste signal on gambling-on-a-recovery-site; axes handled that. It spends its budget on subtle distinctions: which wellness ads click, which financial services feel predatory. Each filter can be looser because the others backstop it.

### Reach along each axis

[Marketing-speak is the protocol](/marketing-speak-is-the-protocol) mentioned [σ](/keywords-are-tiny-circles) — the reach parameter that controls how broadly an advertiser matches. With factored embeddings, σ becomes a vector:

- **σ_what** = large: "I'm broadly a rehab clinic, match me to anything sports-medicine-adjacent"
- **σ_who** = small: "I specifically serve competitive athletes, not weekend joggers"
- **σ_situation** = large: "Any situation — pre-surgery, post-injury, maintenance, whatever"

Per-axis σ maps to tree depth. Large σ matches at shallow levels (wide), small σ only at deep levels (narrow). The advertiser controls reach along each axis independently.

Google Ads has broad match, phrase match, and exact match: three settings that control query interpretation, not semantic reach. Per-axis σ is more expressive. An advertiser can be broad on service type, narrow on audience, and broad on situation, all at once. Keywords can't do this because keywords don't have axes.

### Brand identity doesn't churn

Positioning statements are brand identity. They change quarterly, not hourly. The fast-moving part is the query side (user intent).

New advertisers go into a buffer, filtered by brute-force similarity to exclusion examples until the next tree rebuild. By the time they're high-volume, they're in the tree.

The tree has thousands of nodes, not millions. Rebuilds are offline and infrequent. Serving is three 128-dim tree traversals with bitfield lookups. Fast enough to run pre-auction.

### What gets through

The depression recovery blog runs ads. A therapist's positioning — "evidence-based talk therapy for adults managing depression and anxiety" — clears the **what** axis. The other axes are open. The ad enters the auction, wins on relevance, and the reader sees a therapist who specializes in what they're dealing with. No gambling ads slip through. The exclusion bitfield caught those before the auction started.

The kids' learning channel gets its revenue back. An educational toy company — "hands-on STEM kits for elementary-age kids who learn by building" — clears every axis. Adult-targeting ads are pruned at the **who** tree. The compound filter lets the channel set tight audience exclusions without sacrificing reach on service type. Trust and revenue stop being a tradeoff.

The money that blunt filtering left on the table comes back. Every match that a binary label blocked now clears the axes, passes [the gate](/shape-of-the-gate), and enters an auction. Trust stays because exclusions are precise. Revenue stays because everything else gets through. Permissive by default, surgical where it matters.

Positioning format → factorized embeddings → axis trees → exclusion bitfields → [soft gate](/shape-of-the-gate) → auction. [Marketing-speak](/marketing-speak-is-the-protocol) is the protocol that makes the combination work.

---

*Part of the [Vector Space](/vector-space) series. Written via the [double loop](/double-loop).*
