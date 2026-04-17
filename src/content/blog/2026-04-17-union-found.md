---
variant: post
title: "Union Found"
tags: cognition, coding
---

*Part of the [cognition](/cognition) series. Builds on [Union-Find Compaction](/union-find-compaction) and [Consolidation Codec](/consolidation-codec).*

Every coding agent rebuilds understanding from scratch. Claude Code, Gemini CLI, Cursor, Copilot — they have project memory, rules files, indexed repos. What they lack is the understanding that comes from *doing the work*: which approaches failed, which modules are entangled, which tests are flaky and why. That's the most valuable artifact a coding session produces, and the only one that vanishes.

Code persists in git. Decisions persist in commit messages. Understanding persists nowhere.

### The wrong direction

The industry response is to make sessions cheaper: better compaction, larger windows, faster summarization. Spin up, do a thing, discard. More sessions per person, each one disposable.

[Kiro](https://kiro.dev/) and the spec-driven tools try the opposite: pre-structure context so the agent doesn't have to discover it. Write specs, write rules, define the plan — top-down persistence through human labor.

Both treat context as an input to manage. One optimizes throughput; the other front-loads curation. Neither accumulates from the work itself.

Why does understanding die when the session ends?

### Sessions are the wrong primitive

A session is a container. Understanding grows inside it, bounded by a window and a clock. When the container closes, understanding dies. The next container starts empty.

This is backwards. The session should be a *window* into something larger — a persistent store that grows across sessions, across agents, across people. The session reads from the store and writes back. Close the window, the store remains.

Sharing the data structure is a `pnpm i` or a `uv install` away. [Union-find compaction](/union-find-compaction) organizes messages into equivalence classes with provenance. `find()` traces a summary back to its sources. `union()` merges related understanding. Parent pointers are integers. The forest serializes to disk and deserializes next session with clusters intact.

The [PR](https://github.com/google-gemini/gemini-cli/pull/24736) implementing this inside Gemini CLI is the first step. It runs in-memory for a single compression pass, but the data structure doesn't care whether it's built in one session or a hundred.

### What persistence unlocks

Save the forest between sessions. What follows:

**No cold start.** Prior conversations arrive as pre-merged clusters. The agent doesn't rediscover that the auth module has a hidden null invariant. It already knows — the cluster is in the forest from the session that found it.

**Shared context.** Two agents working the same repo feed the same forest. Agent A discovers a race condition in the payment flow. Agent B, working a different feature, queries the forest and routes around it. They never communicated directly. The forest is the medium.

**Branching.** Fork the forest for a speculative conversation. The fork inherits all context. If the speculation is useful, merge back. If not, discard. Git semantics for understanding.

### From sessions to repos

One person's persistent forest is useful. A repo-wide forest changes how teams onboard.

New contributor clones the repo. Their agent inherits the forest. Not docs. [Docs rot](https://link.springer.com/article/10.1007/s11219-009-9075-x) because maintaining them is work. The forest grows because using the codebase *is* maintaining it. Every session adds to it. Every agent that discovers "this test is flaky because of a timezone dependency" writes it to the forest. No future contributor wastes time on it again.

Open source is where this compounds. Every contributor's agent sessions feed one shared forest. Tribal knowledge stops living in maintainers' heads.

That's a new kind of record. Code is what the software *is*. Git history is what *changed*. The forest is what's *understood*. No codebase has that today.

### Meetings are a bug

I built an eval harness for [Soar](/soap-notes-soar-revised) last month. Paid only enough attention to ship it — how it was implemented, what metrics it tracked, none of that survived a week of working on other things. Someone asked about it in a meeting and I stumbled. The answer wasn't in my head anymore; it was in my agent's context from when I'd done the work. Had they asked my agent, they'd have gotten a more sophisticated answer than I could give.

[Meetings exist](https://hbr.org/2017/07/stop-the-meeting-madness) because context is trapped in people's heads. "Let me catch you up." "What's the status of X?" "Why did we decide Y?" — context synchronization, with humans as the transport layer for shared understanding.

If the forest holds what every agent and teammate has discovered, the standup is redundant. So is the sync meeting. So is the "can you walk me through this" Slack thread. You query the forest.

AI meeting notetakers are a patch on the same bug: lossy compression of something that shouldn't be ephemeral. The fix isn't better notes. It's shared persistent memory that accumulates from actual work.

### What it feels like to use

A managed forest is a very very smart whiteboard. It has four concerns:

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

Clustering parameters (merge threshold, cluster cap, retrieval depth) are convention — optimal values depend on the data structure, not the project. Teams configure retention and access. **Private**: one person's forest. **Readonly**: agents query but don't write — safe for untrusted or new contributors. **Shared**: full read-write for the team. Retention controls how long unqueried clusters survive; everything else is defaults.

Unlike git, there's no new interface to learn — no commands, no workflow changes. The agent reads from the forest and writes back automatically. The user gets better agents.

The whole thing fits in a single SQLite database. Parent pointers, cluster summaries, [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) vectors — all integers and short strings. A repo-wide forest for a mid-size team costs less than a coffee per month to host. The complexity is in the data structure, not the infrastructure.

Git solved "code is trapped on one person's machine." The forest solves "understanding is trapped in one session's context window."

The dream is pair-vibing in the same context window. Two people on two different models — one on Claude, one on GPT, one on a local model, whatever each of them likes — writing to the same forest over the same repo. The forest holds what both of them have figured out. Bring-your-own-model, share-one-context. The session is where you work; the forest is where you meet.

Union-find's merges are associative, commutative, order-independent. Two sessions writing in parallel converge the way a conversation does — no referee, no arbitration meeting. When two claims contradict, both get filed with provenance. The reader judges, same as now.

### The primitive

Union-find is the right data structure because it's append-friendly, mergeable, and cheap. `find()` and `union()` are near-O(1) amortized. The implementation uses a local TF-IDF embedder for clustering and an LLM for per-cluster summaries — lightweight, not zero. What matters is the provenance spine: every summary traces back to its sources, and the forest grows incrementally instead of reprocessing the full history.

The [experiment](/union-find-compaction) showed 8–18pp better factual recall than flat summarization at high compression pressure. That's the in-session case. Cross-session, it compounds: every session starts with what every prior session learned, and every discovery is incremental rather than redundant.

Spec-driven approaches ask humans to pre-structure context. The forest accumulates it from actual work. Bottom-up beats top-down because emergent understanding — the hidden invariant, the flaky test, the undocumented constraint — is what nobody puts in a spec.

### What's next

The Gemini CLI PR ships the in-memory forest. Next is persistence: serialize to disk, load on session start. Then shared forests: multiple agents, one repo, one store. Each step is independently useful. Together they're infrastructure that doesn't exist yet.

People hate collaborating because [the overhead is brutal](https://queue.acm.org/detail.cfm?id=3595878). Syncing context is work. Documenting decisions is work. Onboarding someone new is work. Every collaboration is a chain of encode/decode steps, and the human↔human one is both the lossiest and the slowest — you translate understanding into prose, I wait for the meeting, I decode prose into a mental model; half of what you knew is gone and it took days. The forest keeps context in the agent's native format. Thoughts cross that boundary at session speed. Remove the worst link and the whole chain improves. Prose still happens — blog posts, docs, talks — on a different clock, for different jobs. You still direct your agent. You still evaluate what it produces.

Thoughts should travel at the speed of thought; writing should travel at the speed of writing.

This post is the same bug. I encoded it; you're decoding it. Some of what was sharper in the chat that produced this didn't survive the write-up. The forest is how you skip the round trip.

The session is a window. The forest is the memory. Build the forest.

---

*Written via the [double loop](/double-loop).*
