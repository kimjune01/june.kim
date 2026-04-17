---
variant: post
title: "Union Found"
tags: cognition, coding
---

*Part of the [cognition](/cognition) series. Builds on [Union-Find Compaction](/union-find-compaction) and [Consolidation Codec](/consolidation-codec).*

Every coding agent rebuilds understanding from scratch. Claude Code, Gemini CLI, Cursor, Copilot — they have project memory, rules files, indexed repos. What they don't have is the understanding that comes from *doing the work*: which approaches failed, which modules are entangled, which tests are flaky and why. That's the most valuable artifact a coding session produces, and the only one that vanishes.

Code persists in git. Decisions persist in commit messages. Understanding persists nowhere.

### The wrong direction

The industry response is to make sessions cheaper: better compaction, larger windows, faster summarization. Spin up, do a thing, discard. More sessions per person, each one disposable.

[Kiro](https://kiro.dev/) and the spec-driven tools try the opposite: pre-structure context so the agent doesn't have to discover it. Write specs, write rules, define the plan — top-down persistence through human labor.

Both treat context as an input to manage. One optimizes throughput; the other front-loads curation. Neither accumulates from the work itself.

The question worth asking: "why does understanding die when the session ends?"

### Sessions are the wrong primitive

A session is a container. Understanding grows inside it, bounded by a window and a clock. When the container closes, understanding dies. The next container starts empty.

This is backwards. The session should be a *window* into something larger — a persistent store that grows across sessions, across agents, across people. The session reads from the store and writes back. Close the window, the store remains.

The data structure already exists. [Union-find compaction](/union-find-compaction) organizes messages into equivalence classes with provenance. `find()` traces a summary back to its sources. `union()` merges related understanding. Parent pointers are integers. The forest serializes to disk and deserializes next session with clusters intact.

The [PR](https://github.com/google-gemini/gemini-cli/pull/24736) implementing this inside Gemini CLI is the first step. It runs in-memory for a single compression pass, but the data structure doesn't care whether it was built in one session or a hundred.

### What persistence unlocks

Save the forest between sessions. What follows:

**No cold start.** Prior conversations arrive as pre-merged clusters. The agent doesn't rediscover that the auth module has a hidden null invariant. It already knows — the cluster is in the forest from the session that found it.

**Shared context.** Two agents working the same repo feed the same forest. Agent A discovers a race condition in the payment flow. Agent B, working a different feature, queries the forest and routes around it. They never communicated directly. The forest is the medium.

**Branching.** Fork the forest for a speculative conversation. The fork inherits all context. If the speculation is useful, merge back. If not, discard. Git semantics for understanding.

### From sessions to repos

One person's persistent forest is useful. A repo-wide forest changes how teams onboard.

New contributor clones the repo. Their agent inherits the forest. Not docs — docs rot because maintaining them is work. The forest grows because using the codebase *is* maintaining it. Every session adds to it. Every agent that discovers "this test is flaky because of a timezone dependency" writes that to the forest, and no future agent or contributor wastes time on it again.

Open source is where this compounds. Every contributor's agent sessions feed one shared forest. Tribal knowledge stops living in maintainers' heads. Maintainer gets hit by a bus — the forest survives.

That's a new kind of record. Code is what the software *is*. Git history is what *changed*. The forest is what's *understood*. No codebase has that today.

### Meetings are a bug

Meetings exist because context is trapped in people's heads. "Let me catch you up." "What's the status of X?" "Why did we decide Y?" — context synchronization, humans acting as the transport layer for shared understanding.

If the forest holds what every agent and teammate has discovered, the standup is redundant. The sync meeting is redundant. The "can you walk me through this" Slack thread is redundant. You query the forest.

AI meeting notetakers are a patch on the same bug: lossy compression of something that shouldn't be ephemeral. The fix isn't better notes — it's shared persistent memory that accumulates from actual work.

### A product category

Managed forests open a product surface:

| Concern | What it means |
|---|---|
| Access control | Public forest for open source, private forest for company fork, shared ancestor |
| Pruning | Stale understanding is worse than none — someone manages signal-to-noise |
| Forking and merging | Same semantics as git, but for understanding |
| Querying | Not just similarity — "what do we know about this module," "what's been tried and failed" |

The management interface is a slider and a mode picker:

<div style="max-width:min(90vw, 520px); margin:1.5em auto;">
<img src="/assets/forest-controls.svg" alt="Forest control panel: retention slider (90 days), shared toggle, three stats (messages, clusters, contributors). That's it." style="width:100%; display:block;">
</div>

Clustering parameters (merge threshold, cluster cap, retrieval depth) are convention — the optimal values depend on the data structure, not the project. What teams actually configure is retention and access. **Private**: one person's forest. **Readonly**: agents can query but not write — safe for untrusted or new contributors. **Shared**: full read-write for the team. Retention controls how long unqueried clusters survive. Everything else is defaults. Unlike git, there's no new interface to learn. No commands, no workflow changes. The agent reads from the forest and writes to it automatically. The user just gets better agents.

The whole thing fits in a single SQLite database. Parent pointers, cluster summaries, TF-IDF vectors — all integers and short strings. A repo-wide forest for a mid-size team costs less than a coffee per month to host. The complexity is in the data structure, not the infrastructure. Same reason git won.

Git solved "code is trapped on one person's machine." GitHub built a product category on top. The forest solves "understanding is trapped in one session's context window." The same category exists on top of the forest.

Every company is about to have dozens of agents working their codebase simultaneously. They need shared memory. Existing tools (Zep, mem0) store facts in knowledge graphs or vector stores. None preserve provenance. None merge incrementally. They're databases, not forests.

### The primitive

Union-find is the right data structure because it's append-friendly, mergeable, and cheap. `find()` and `union()` are near-O(1) amortized. Parent pointers are integers that serialize trivially. The implementation uses a local TF-IDF embedder for clustering and an LLM for per-cluster summaries — lightweight, not zero. What matters is the provenance spine: every summary traces back to its sources, and the forest grows incrementally instead of reprocessing the full history.

The [experiment](/union-find-compaction) showed 8–18pp better factual recall than flat summarization at high compression pressure. That's the in-session case. Cross-session, it compounds: every session starts with the accumulated understanding of every prior session, and every discovery is incremental rather than redundant.

Spec-driven approaches ask humans to pre-structure context. The forest accumulates it from actual work. Bottom-up beats top-down because emergent understanding — the hidden invariant, the flaky test, the undocumented constraint — is what nobody puts in a spec.

### What's next

The Gemini CLI PR ships the in-memory forest. Next is persistence: serialize to disk, load on session start. Then shared forests: multiple agents, one repo, one store. Each step is independently useful. Together they're infrastructure that doesn't exist yet.

People hate collaborating because the overhead is brutal. Syncing context is work. Documenting decisions is work. Onboarding someone new is work. The forest eliminates the work of collaboration without eliminating the collaboration. What's left is the good part — building things together.

The session is a window. The forest is the memory. Build the forest.

---

*Written via the [double loop](/double-loop).*
