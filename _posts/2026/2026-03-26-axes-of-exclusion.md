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

Three small embeddings instead of one big one. Each field goes through a shared sentence encoder (e.g., `all-MiniLM-L6-v2`, d=384, projected down to 128 per field). The protocol enforces the factorization at input time.

This sidesteps one of the hardest parts of factorization: discovering the axes after the fact. The advertiser already gave you the partition when they filled in the form.

The tradeoff: embedding fields separately loses cross-field meaning. "Sports injury rehab" alone carries less context than the full positioning statement. The situation modifies the what. Whether the loss breaks axis-aligned exclusion is empirical. One experiment away from an answer.

### Trees over axes

A tree over the **what** axis clusters advertisers by service type: "sports rehab," "divorce mediation," "roof repair" land in different branches. Separate trees over **who** and **situation** cluster by audience and qualifier. Each tree is a hierarchical k-means (k ≈ 16 per level, depth 3-4, yielding ~4K-65K leaf nodes).

Publisher exclusion becomes axis-aligned:

- A mental health blog excludes branches on the **what** tree: gambling, predatory lending, alcohol. Doesn't touch **who** or **situation**. Therapy services, wellness apps, financial literacy — all pass, because the service is appropriate even though the content is sensitive.
- A kids' learning site excludes branches on the **who** tree: anything targeting adults. Service type can be broad — educational toys, tutoring, healthy snacks, children's books all pass. The audience is the constraint, not the category.
- A political news site excludes certain **situation** branches — campaign-season qualifiers — to avoid appearing partisan. Service and audience are fine.

Each exclusion checks one 128-dimensional embedding. One-third the dimensions, one-third the cost, and axes that don't apply get skipped entirely.

Storage per publisher: a set of excluded node IDs per axis tree (sorted array or roaring bitmap). A publisher with ten exclusion rules across three axes stores maybe a hundred node IDs. At query time, route the ad's embedding down each tree; if any visited node appears in the exclusion set, reject.

### Conjunctions and the gray zone

One-axis exclusion is clean when the publisher means "no X regardless of context." But some exclusions are conjunctive: "no crypto for minors" means exclude the intersection of a **what** branch (crypto) and a **who** branch (minors).

Conjunctive exclusions check two axes: **what** first (is this crypto?), then **who** only if that matches (is the audience minors?). Stored as a pair `(what_node_id, who_node_id)` — the second check fires only if the first hits. The first axis prunes most candidates; the second refines.

Then there's the gray zone. A financial planning ad on a depression recovery blog might even help. But it's not *relevant* in the way a therapy service ad would be. The publisher doesn't want to block it. They want to shape what gets through.

How does a publisher set exclusions? Two paths. First: browse the tree, which is labeled with representative positioning statements at each node, and mark branches to exclude. Second: provide example ads they'd reject. The system maps each example to its tree node and marks the lowest common ancestor at the appropriate depth — tight cluster of examples means a deep, surgical exclusion; scattered examples mean a shallow, broad one.

Axis-aligned exclusion handles the hard cases: things the publisher will never tolerate. That's editorial, not learned. But the gray zone needs a softer boundary.

### Shaping the gate

[Three Levers](/three-levers) defined τ as the publisher's relevance floor: ads within τ distance of the query enter the auction. τ is a sphere. Same radius in every direction. The axes prune *what* kind of ad gets through. τ controls *how relevant* the survivors must be. But τ can't tell directions apart.

A health chatbot shows a yoga mat ad next to a conversation about back pain. Users click. Then a pain clinic ad clears the same threshold. Same distance from the query, different direction entirely. Users bounce. The publisher tightens τ. Now the yoga mat ad gets filtered too.

The [PID controller](/set-it-and-forget-it) that tunes τ already sees what it needs: which ads caused bounces, which got clicks, the embedding vectors of both. All that directional information gets thrown away. A bounce tightens the sphere uniformly. *Where* the match was good or bad? Discarded.

A diagonal approximation fixes this. Replace `‖q − c‖²` with `Σ_j m_j (q_j − c_j)²` where **m** is a per-publisher weight vector: 384 parameters, same cost as the sphere. Some semantic directions matter more to this publisher than others.

### Two loops

The publisher sets [one number](/set-it-and-forget-it): "10% of conversations should include a recommendation." A PID controller adjusts τ to hit that target. A second, slower loop adjusts M from the same click/bounce stream. PID controls *how much* filtering; M controls *where*. τ responds in minutes, M shifts over days.

M doesn't have to start cold. Before going live, the publisher swipes through borderline query-ad pairs for twenty minutes. "Would you show this ad next to this conversation?" Yes or no. A few hundred labels pre-shape the diagonal. The online loop refines from there. With a bootstrapped M, the publisher can loosen τ: further out in trusted directions, tight in untrusted, before serving a single impression.

Clicks conflate relevance with creative quality. Bounces conflate bad matches with slow load times. Three safeguards keep M honest: regularization toward I (sparse dimensions stay near 1), update caps (no single impression warps the metric), and daily decay (weights drift back toward 1).

Each weight starts at 1 and drifts where signal concentrates. [ITML](https://jmlr.org/papers/v8/davis07a.html) (Davis et al., 2007) works: online, KL-regularized toward I, O(d) per update when diagonal. If diagonal proves too blunt: M = D + VVᵀ. Low-rank term (k = 5) captures correlated directions. But start diagonal. Earn the complexity.

### Three filters, one pipeline

**[Credibility](/proof-of-trust) → hard prune (axes) → soft gate (M) → auction.** Three per-publisher filters, different timescales. Credibility gates which advertisers enter the system. Exclusion bitfields are set at onboarding and rarely change. The gate learns continuously from engagement.

The compound filter is stronger than any single layer. Axes remove the obviously bad ads cheaply, so the gate only sees tolerable candidates. It doesn't waste signal on gambling-on-a-recovery-site; axes handled that. It spends its budget on subtle distinctions: which wellness ads click, which financial services feel predatory. Each filter can be looser because the others backstop it.

All three run publisher-side during [phase one](/ask-first) matching, before any embedding enters the [TEE](/monetizing-the-untouchable). The exchange never sees M, the clicks that shaped it, or the conversations it filters. The enclave only sees what survives. Inside the gate, the [scoring function](/three-levers) runs unchanged: `score_i(x) = log(b_i) − ‖x − c_i‖² / σ_i²`. M is editorial; the auction is the auction. Keeping them apart preserves the [power diagram](/power-diagrams-ad-auctions) geometry and VCG guarantees.

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

The tree has thousands of nodes, not millions. Rebuilds are offline and infrequent. The publisher runs three 128-dim tree traversals with bitfield lookups during [phase one](/ask-first) matching, before any data leaves their servers.

### What gets through

The depression recovery blog runs ads. A therapist's positioning — "evidence-based talk therapy for adults managing depression and anxiety" — clears the **what** axis. The other axes are open. The ad enters the auction, wins on relevance, and the reader sees a therapist who specializes in what they're dealing with. No gambling ads slip through. The exclusion bitfield caught those before the auction started.

The kids' learning channel gets its revenue back. An educational toy company — "hands-on STEM kits for elementary-age kids who learn by building" — clears every axis. Adult-targeting ads are pruned at the **who** tree. The compound filter lets the channel set tight audience exclusions without sacrificing reach on service type. Trust and revenue stop being a tradeoff.

| | Before (category labels) | With the protocol |
|---|---|---|
| **Granularity** | One label per video | Per-publisher, per-axis, per-branch |
| **Exclusion** | Category blocklist | Semantic tree with bitfield lookups |
| **Gray zone** | Block or allow | Learned directional weights (M) |
| **Advertiser reach** | Broad / phrase / exact | [Per-axis σ](/keywords-are-tiny-circles) vector |
| **Signal** | Content classification | Positioning embeddings + engagement |
| **Publisher control** | Choose from platform categories | Browse tree, swipe examples, set thresholds |
| **Auction** | Platform-controlled | [Scoring function](/three-levers) unchanged inside [TEE](/monetizing-the-untouchable) |
| **Filter placement** | Platform-side | Publisher-side, before the TEE |

Character.ai, Woebot, every mental health chatbot sitting on [untouchable inventory](/monetizing-the-untouchable): they can't use category blocklists because every conversation is "sensitive content." Axes let them exclude almost everything on **what** while letting therapists, crisis services, and wellness apps through. The tightest exclusion surface is also the most valuable.

Trust stays because exclusions are precise; revenue stays because everything else gets through. Permissive by default, surgical where it matters.

---

*Part of the [Vector Space](/vector-space) series. Written via the [double loop](/double-loop).*

*Adjacent work: per-query learned distance functions in [image retrieval](https://research.google/pubs/pub41900), [low-rank Mahalanobis learning](https://papers.nips.cc/paper/8369-fast-low-rank-metric-learning-for-large-scale-and-high-dimensional-data), [probabilistic retrieval thresholds](https://aclanthology.org/2025.emnlp-industry.161/), publisher-aware ad weighting in [patents](https://patents.google.com/patent/US9911135B2/en), [embedding-native ad retrieval](https://www.microsoft.com/en-us/research/publication/uni-retriever-towards-learning-the-unified-embedding-based-retriever-in-bing-sponsored-search/) at Bing, [ITML](https://jmlr.org/papers/v8/davis07a.html).*
