# Union-Find for LLM Context Compaction

Every LLM chatbot has the same context problem: conversations grow, the window doesn't. The standard fix is flat summarization. Run a cheap model over everything outside a recent window, replace the originals with the summary. Lossy, all-or-nothing, and the whole conversation stalls while the summarizer runs.

I built and tested an alternative: use [union-find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) (disjoint-set forests) to group similar messages into equivalence classes and summarize per-cluster instead of per-conversation. The structure gives you provenance, recoverability, and incremental updates for free.

## How it works

Each message starts as a singleton set. The context window splits into two zones:

**Hot zone:** the last ~10 messages, served verbatim. When the window overflows, the oldest message graduates to the cold zone.

**Cold zone:** managed by a union-find forest. On graduation, the message gets a TF-IDF vector and is compared against existing cluster centroids by cosine similarity. Above a merge threshold (0.15), it joins that cluster via `union`; below, it starts a new singleton. A hard cap (default 10 clusters) forces the closest pair to merge when exceeded.

Each `union` triggers a cheap LLM call: take two small summaries (5–20 source messages), produce one. These are the same summarization calls you'd make anyway — the difference is routing them through a structure that preserves parent pointers.

On the read path: vectorize the incoming user message, find the nearest cluster root, inject that cluster's summary alongside the hot window. Unlike RAG, the summaries are pre-merged at write time. Context stays bounded.

What you get over flat summarization:

1. **Provenance.** Every summary traces back to its source messages through `find()`.
2. **Recoverability.** `expand(root_id)` reinflates a cluster back to its sources. Flat summarization discards them.
3. **Incremental.** Messages graduate one at a time. Near-O(1) amortized per graduation ([Tarjan 1975](https://doi.org/10.1145/321879.321884)). No batch stall.
4. **Cheaper.** Small clusters mean smaller prompts. In the experiment below, Haiku-class models produced adequate per-cluster summaries.
5. **Persistent.** Parent pointers are just integers. Save them, load them next session, clusters intact.

## Experiment

Does this actually preserve more detail than flat summarization, given the same token budget?

**Setup:** A synthetic 200-message DevOps conversation, seeded with 40 verifiable facts (specific version numbers, cron schedules, webhook paths, config values). Same cheap summarizer (Claude Haiku), same token budget, same retrieval machinery for both methods. A strict LLM judge scores binary recall — "PostgreSQL 16.2" counts, "PostgreSQL" doesn't. McNemar's test on discordant pairs. Seven trials varying model, conversation length, and retrieval strategy.

**Results:**

| Trial | Config | Flat recall | UF recall | p (McNemar) |
|---|---|---:|---:|---:|
| 1 | Haiku, 50 msgs | 90% | 90% | 1.000 |
| 2 | Haiku, 200 msgs | 65% | 82% | **0.039** |
| 3 | Sonnet, 200 msgs | 70% | 78% | 0.453 |
| 4 | Haiku, 200, +retrieval | 68% | 82% | 0.180 |
| 5 | Haiku, 200, tuned | 62% | 80% | 0.065 |
| 6 | Haiku, 200, +timestamps | 72% | 90% | 0.092 |
| 7 | Haiku+Sonnet, 200 | 75% | 90% | 0.070 |

At low compression (50 messages), no difference — both methods fit comfortably. At 200 messages, union-find leads by 8–18 percentage points across every trial. Trial 2 is the only one that clears statistical significance (p = 0.039); the rest are directional but underpowered at n = 40 paired questions.

**What flat drops:** Flat summarization preserves headline facts (the database version, the auth method) and drops footnote facts (the scrape interval, the cron schedule, the webhook path). The model decides what matters in a single pass, and footnotes lose. Union-find compresses per-cluster, so the cron schedule doesn't compete against the database version. They survive in different clusters.

**Honest accounting:** One significant trial out of seven. The consistent directional advantage is suggestive, but a larger study (200+ paired questions) would be needed to confirm it. I think the architectural properties matter more than the recall numbers.

## What this enables

The forest serializes as parent pointers. Because the structure is just integers, it's trivial to persist, share, or fork.

**Cross-session memory.** Prior conversations arrive as pre-merged clusters. No pinned notes, no "as we discussed last time."

**Multiplayer context.** Two people feed the same forest. Both query it. Shared memory, one structure.

**Branching.** Fork the forest for a what-if conversation. The fork inherits all context. Conversations grow; now the window can grow back.

## Code

Full implementation, synthetic data, and trial logs: [github.com/kimjune01/union-find-compaction](https://github.com/kimjune01/union-find-compaction). The [git history](https://github.com/kimjune01/union-find-compaction/commits/main) shows each trial's design decisions, what changed between iterations, and why.

Longer writeup with diagrams on [my blog](https://june.kim/union-find-compaction).
