---
variant: post
title: "Union Found"
tags: cognition, coding
---

*Part of the [cognition](/cognition) series. Builds on [Union-Find Compaction](/union-find-compaction) and [Consolidation Codec](/consolidation-codec).*

Every coding agent rebuilds understanding from scratch. Claude Code, Gemini CLI, Cursor, Copilot — they have project memory, rules files, indexed repos. What they lack is the understanding that comes from *doing the work*: which approaches failed, which modules are entangled, which tests are flaky and why. That's the most valuable artifact a coding session produces, and the only one that vanishes.

Code persists in git. Decisions persist in commit messages. Understanding persists nowhere.

### The data structure already exists

[Union-find compaction](/union-find-compaction) solves the compression problem with provenance. Installing it is a `pnpm i` or a `uv install` away. The [Gemini CLI PR](https://github.com/google-gemini/gemini-cli/pull/24736) ships it in-memory — persistence is mechanical, sharing is a db connection away.

### Multiplayer read-access

Persist the forest across sessions and every prior session's understanding arrives pre-merged. No cold start. The agent doesn't rediscover that the auth module has a hidden null invariant — it already knows, because the cluster is in the forest from the session that found it.

Persist it across people and you get multiplayer read-access. Two agents on the same repo feed the same forest. Agent A discovers a race condition in the payment flow. Agent B, working a different feature, queries the forest and routes around it. They never communicated directly — the forest is the medium.

New contributor clones the repo. Their agent inherits the forest. Not docs. [Docs rot](https://link.springer.com/article/10.1007/s11219-009-9075-x) because maintaining them is work. The forest grows because using the codebase *is* maintaining it. Every session adds to it. Every agent that discovers "this test is flaky because of a timezone dependency" writes it to the forest. No future contributor wastes time on it again.

That's a new kind of record. Code is what the software *is*. Git history is what *changed*. The forest is what's *understood*. No codebase has that today.

### Meetings are a bug

I built an eval harness for [Soar](/soap-notes-soar-revised) last month. Paid only enough attention to ship it — how it was implemented, what metrics it tracked, none of that survived a week of working on other things. Someone asked about it in a meeting and I stumbled. The answer wasn't in my head anymore; it was in my agent's context from when I'd done the work. Had they asked my agent, they'd have gotten a more sophisticated answer than I could give.

[Meetings exist](https://hbr.org/2017/07/stop-the-meeting-madness) because context is trapped in people's heads. "Let me catch you up." "What's the status of X?" "Why did we decide Y?" — context synchronization, with humans as the transport layer for shared understanding.

If the forest holds what every agent and teammate has discovered, the standup is redundant. So is the sync meeting. So is the "can you walk me through this" Slack thread. You query the forest.

AI meeting notetakers are a patch on the same bug: lossy compression of something that shouldn't be ephemeral. The fix isn't better notes. It's shared persistent memory that accumulates from actual work.

### Human collaboration is being priced out

Meetings are already dying, but not because anyone built a forest. Human↔agent collaboration got so productive that human↔human coordination can't compete on cost. You ship more in an hour with your agent than you do in a day of meetings. So teams shrink. Standups get canceled. Managers judge by output and expectation alignment. Knowledge transfer — always second-class to shipping — now costs a full day of everyone's output, so it gets deferred to conferences twice a year. Coworkers reduce to another face at the office. Learning is a luxury good.

The public channels that remain — Twitter, Reddit, Hacker News — can't carry tribal knowledge. They're built for takes, not for the context-bound understanding that comes from doing the work. When someone does transfer tribal knowledge at scale — [Dario Amodei](https://darioamodei.com/machines-of-loving-grace) spends half his time writing to align Anthropic — it's basically a full-time job. Opening your tribal knowledge now reads as generosity because it's rare.

Even that writing is a lossy projection. Leaders thinking about market and direction chat with their agents; the provenance of their decisions lives in the context window. A fully confident leader would open it for inspection — the reasoning, the rejected paths, the uncertainty — not just the polished essay. Shared context would unlock that at every level of the org.

The forest isn't about eliminating human collaboration. It's about making human↔human knowledge transfer cheap enough to happen at all again.

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

### But what if we shared the same window?

Read-access is just the setup. What if two people had read *and* write on the same context window — multiple humans, multiple agents, all writing into one live forest at the same time?

This is pair programming, but better. The arguments for pair programming have always been: two minds catch bugs one would miss; knowledge transfer happens by doing, not documenting; shared ownership reduces bus factor; mentoring is a natural byproduct; real-time review beats after-the-fact code review. Every one of these applies with a shared forest, and each gains properties pair programming can't match.

Minds aren't limited to two. An agent team writes and reads the forest; humans direct. Knowledge transfer doesn't require both people in the room; the forest keeps accumulating through every session. Shared ownership extends across time — contributors who never met share context. Mentoring isn't pairwise; a new contributor's agent reads what everyone has figured out. Review isn't real-time vs async; it's inspectable anytime with provenance.

The dream is pair-vibing in the same context window. Two people on two different models — one on Claude, one on GPT, one on a local model, whatever each of them likes — writing to the same forest over the same repo. Bring-your-own-model, share-one-context. The session is where you work; the forest is where you meet.

The computer does exactly what it's told. The monkey at the keyboard is the problem — often a whole group. Fragments held by different people, nobody integrated, the disaster happens in the gap. Post-mortems rarely name this directly; technical framings sell technical solutions. Nancy Leveson's [Therac-25 analysis](http://sunnyday.mit.edu/papers/therac.pdf) rejected the bug framing:

> Fixing each individual software flaw as it was found did not solve the device's safety problems.

The FAA's [737 MAX review](https://www.faa.gov/sites/faa.gov/files/2021-08/Final_JATR_Submittal_to_FAA_Oct_2019.pdf) named *"fragmented documentation"* delivered to *"disconnected groups within the process."* Those are the rare honest cases. Trace the causality stack of any serious post-mortem and it bottoms out in human decisions that didn't connect across the group. The evidence is in every write-up; naming it isn't. The forest is the layer that would already exist if sharing context weren't so damn expensive.

Union-find's merges are associative, commutative, order-independent. Two sessions writing in parallel converge the way a conversation does — no referee, no arbitration meeting. When two claims contradict, both get filed with provenance. The reader judges, same as now.

People hate collaborating because [the overhead is brutal](https://queue.acm.org/detail.cfm?id=3595878). Syncing context is work. Documenting decisions is work. Onboarding someone new is work. Every collaboration is a chain of encode/decode steps, and the human↔human one is both the lossiest and the slowest — you translate understanding into prose, I wait for the meeting, I decode prose into a mental model; half of what you knew is gone and it took days. The forest keeps context in the agent's native format. Thoughts cross that boundary at session speed. Remove the worst link and the whole chain improves. Prose still happens — blog posts, docs, talks — on a different clock, for different jobs. You still direct your agent. You still evaluate what it produces.

Thoughts should travel at the speed of thought; writing should travel at the speed of writing.

This post is the same bug. I encoded it; you're decoding it. Some of what was sharper in the chat that produced this didn't survive the write-up. The forest is how you skip the round trip.

The session is a window. The forest is the memory. Build the forest.

---

*Written via the [double loop](/double-loop).*
