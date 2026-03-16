*Part of the [cognition](/cognition) series. Builds on [The Natural Framework](/the-natural-framework), [General Intelligence](/general-intelligence), and [The Handshake](/the-handshake).*

> Every chatbot that compacts stalls the entire conversation to do it. But does it need to?

Every chatbot has the same context problem: conversations grow, the window doesn't. When it fills up, the system summarizes and discards. Run a cheap model over everything outside a hot window, truncate to budget. The summary replaces the source. Traceability, expandability, selective retrieval: all gone.

Compression is coarse. The summary replaces every source, so it can't trace a claim back to the original message.

<div style="max-width:72vw; margin:1.5em auto;">
<img src="/assets/union-find-compaction.svg" alt="Chatbot layer from Diagnosis LLM: today's flat summary in Cache destroys provenance, four nil cells downstream. Union-find fixes Cache and Remember." style="width:100%; display:block;">
</div>

*Chatbot layer from [Diagnosis LLM](/diagnosis-llm). Full diagnostic: six steps, three layers, nine dysfunction cells.*


## A convenient fix

[Union-find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) has been around for half a century. [Tarjan (1975)](https://doi.org/10.1145/321879.321884) proved its amortized cost: `find` (follow parent pointers to root, compress path) and `union` (merge two trees, balance by rank), both near-O(1). Fast, and it never forgets which elements belong together.

The insight: use union-find as the provenance spine for context compaction. Each message starts as a singleton. Similar messages merge into equivalence classes. Each `union` is a cheap LLM call: take two small summaries, produce one. The calls were going to happen anyway. The contribution is routing them through a structure that gives you amortized lookup and canonical roots for free. Five properties follow:

1. **Provenance.** Every summary traces back to its source messages through `find()`. You can audit any summary.
2. **Recoverability.** `expand(root_id)` reinflates a cluster back to its sources. Raw messages stay addressable through the parent pointers. Flat summarization discards them.
3. **Incremental.** Messages graduate one at a time. Each graduation is near-O(1). No batch stall, no latency spike. Flat summarization reprocesses the entire history at once.
4. **Cheaper.** Each `union` feeds a small cluster (5–20 messages) to the summarizer. Smaller prompts, smaller models. Haiku produced good per-cluster summaries.
5. **Persistent.** The forest serializes naturally. Parent pointers are just integers. Save it, load it next session, clusters intact.

### Compound cache

The implementation splits context into two zones:

**Hot** — the last 10 messages, served raw. When the window overflows, the oldest message graduates to cold.

**Cold** — everything older, managed by the union-find forest. On graduation, the new message keeps its timestamp, gets a TF-IDF vector (cheap, local, accurate enough), and is compared against cluster centroids by cosine similarity. Above a merge threshold (0.15), it joins that cluster via `union`; below, it starts a new singleton. A hard cap (default 10 clusters) forces the closest pair to merge when exceeded. Centroids update as weighted averages.

That's the write path. The read path: vectorize the incoming message, find the nearest e-class root, inject that cluster's summary alongside the hot window. Unlike RAG, the summaries are pre-merged at write time. Context stays bounded.

Eviction from a flat summary already happened, invisibly, at compression time. Eviction from a structure with provenance is a policy choice. That choice is deferred here: storage grows monotonically, the forest only adds nodes, and the underlying store accumulates indefinitely. Eventually you drop stale clusters or archive old source messages.

## Experiment

> [github.com/kimjune01/union-find-compaction](https://github.com/kimjune01/union-find-compaction) — code, data, and full trial logs. The [git history](https://github.com/kimjune01/union-find-compaction/commits/main) shows the thought process: each trial's design decisions, what changed between iterations, and why.

Does union-find compaction actually preserve more detail than flat summarization, given the same token budget? If not, the provenance argument is academic. If so, everyone gets better recall, and lineage comes free.

A synthetic 200-message DevOps conversation, seeded with 40 verifiable facts. Same cheap summarizer (Haiku), same budget, same retrieval machinery for both methods. A strict LLM judge scores binary recall: "PostgreSQL 16.2" counts, "PostgreSQL" doesn't. McNemar's test on discordant pairs. Seven trials.

### Results

<div class="results-table" markdown="1">

| # | Config | Flat | UF | p |
|---|---|---:|---:|---:|
| 1 | Haiku, 50 | 90% | 90% | 1.000 |
| 2 | Haiku, 200 | 65% | 82% | **0.039** |
| 3 | Sonnet, 200 | 70% | 78% | 0.453 |
| 4 | Haiku, 200, retrieval | 68% | 82% | 0.180 |
| 5 | Haiku, 200, tuned | 62% | 80% | 0.065 |
| 6 | Haiku, 200, timestamps | 72% | 90% | 0.092 |
| 7 | Haiku+Sonnet, 200 | 75% | 90% | 0.070 |

</div>

<style>
.results-table table { font-size: 12px !important; min-width: 0 !important; width: auto !important; margin: 1em auto !important; }
.results-table th { background: #f0f0f0 !important; }
</style>

At low compression (50 messages), no difference. At 200 messages, UF leads by 8–18pp across every trial. Trial 2 is the only one that clears significance (p = 0.039, McNemar's); the rest are directional but underpowered at n = 40. Trial 7 mimics production: cheap model summarizes, expensive model answers. The expensive model can't recover facts the cheap summary already dropped.

### What flat drops

Flat summarization preserves headline facts (PostgreSQL 16.2, bcrypt auth) and drops footnote facts: the scrape interval, the cron schedule, the webhook path, the filterable attribute count. The details that distinguish reading the conversation from getting a briefing.

Why? Flat summarization compresses 200 messages into one block. The model decides what matters in a single pass. Footnotes lose. Union-find compresses per-cluster, 5–20 messages each. The cron schedule doesn't compete against the database version. They live in different clusters.

### Honest accounting

One significant trial out of seven. The consistent 15–18pp directional advantage is suggestive but underpowered. A larger study (200+ paired questions) would resolve it.

The statistical case matters less than the architectural one.

## Unlock

Flat summarization is a shredder. Union-find compaction is a filing system. The shredder is intermittent, intrusive, and slow. The filing system runs continuously and remembers where things came from.

The forest serializes as parent pointers — just integers. Save it, load it next session, clusters intact. Three things follow:

**No sidebar.** Prior conversations arrive as pre-merged clusters, not a blank window. No pinned notes, no "as we discussed last time."

**Multiplayer.** Two people feed the same forest. Both can query it. Shared memory without shared prompts.

**Branching.** Fork the forest for a what-if conversation. The fork inherits all context. Git branches for conversations.

The idea to use union-find for compaction came from [the parts bin](/the-parts-bin) — a catalog of operations indexed by contract. Match the contract, find the operation. The bin has more gaps than entries. What's in the other gaps?

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
