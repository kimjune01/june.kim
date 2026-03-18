---
layout: post-wide
title: "Contributing to Gemini CLI"
tags: coding
---

*Builds on [Union-Find Compaction](/union-find-compaction). Implementation: [gemini-cli fork](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction). Spec and experiment: [union-find-compaction-for-gemini-cli](https://github.com/kimjune01/union-find-compaction-for-gemini-cli).*

Ninety minutes into a session. The agent has your codebase in context, your test failures explained, your refactor halfway done. You've been trading messages for an hour and the work is good. Then you glance at the status bar.

![Context left until auto-compact: 0%](/assets/auto-compact-0.png)

Twenty seconds of spinner. Two LLM calls. Your conversation history becomes a paragraph. The summarizer keeps what it thinks matters and drops the rest. When you ask about the refactor you were just discussing, the agent apologizes. It doesn't remember. You write a bootstrap prompt, start a new session, and spend ten minutes re-explaining what the last session already knew.

This is flat compression. Gemini CLI summarizes the oldest 70% of your conversation into a single snapshot. It works. It also forces all older context through one bottleneck, which drops whatever the summarizer didn't prioritize.

I'd been circling this problem for months. The stack:

1. [Manual Context Compaction](/manual-context-compaction) — the pain. Dump context to markdown before the window fills.
2. [Context Synthesis is Quadratic](/context-synthesis-is-quadratic) — the theory. Long contexts degrade faster than linear because synthesis is pairwise.
3. [The Natural Framework](/the-natural-framework) — a cognition model. How memory, retrieval, and compression relate.
4. [Diagnosis LLM](/diagnosis-llm) — the diagnostic. Flat summary destroys provenance, expandability, and selective retrieval.
5. [The Parts Bin](/the-parts-bin) — union-find as a candidate fix sitting in the parts bin.
6. [Union-Find Compaction](/union-find-compaction) — the prototype. Clusters by topic, each with its own summary.

The prototype preserved more detail in isolation. The question was whether the idea survived contact with a real codebase. Real API costs, real latency constraints, and real implementation complexity.

## v1: wrong on every count

The first attempt translated the prototype directly. Every `union()` call triggered an LLM summarization. The implementation was faithful to the spec. The spec was wrong.

120 messages, 10 clusters. Each graduation merges with the nearest cluster (nearest by cosine similarity of TF-IDF embeddings). Each merge calls the summarizer. That's ~80 LLM calls per conversation. Flat uses 2. The cost ratio was 5.2x. The latency was worse. The recall improvement didn't materialize either. All three preregistered hypotheses failed.

The prototype proved the idea could improve recall. The real system proved the naive implementation erased that advantage under actual cost constraints. Every merge re-summarized an ever-growing cluster from scratch. Message 90 triggers a merge that re-reads messages 1 through 89. Message 91 re-reads 1 through 90. At 120 messages, the quadratic cost surfaced immediately.

## v2: deferred summarization

The fix was to stop summarizing during merges entirely.

`union()` becomes structural. It updates parent pointers, merges children lists, recomputes centroids. No LLM call. It tracks what changed in a dirty map: for each cluster root, the list of texts that need to be summarized together. A singleton's raw content. A previously-clean cluster's cached summary plus the new raw messages that joined.

A concrete example: messages 1-20 form three clusters. Message 21 arrives, gets embedded locally, and joins the nearest cluster by similarity. The cluster is marked dirty. No summarizer call. Later, in the background, `resolveDirty()` takes the cluster's old summary plus message 21's raw text and produces a new summary in one LLM call.

Side by side:

```
Flat (current):
  [All old messages] → LLM summarize → LLM verify → single snapshot + recent 30%
  Blocking: 20-30s spinner. Two LLM calls per compression event.

Union-find (v2):
  append(msg)       <1ms    Embed locally, push to hot zone, graduate if needed.
  render()          <0.1ms  Return cached summaries + hot zone verbatim.
  resolveDirty()    ~4s     Batch-summarize dirty clusters in background.
```

Flat discards original messages after compression. Union-find keeps them. Every cluster links back to its sources through parent pointers. If a summary drops a detail, you can expand the cluster and recover the original text.

The overlap window makes this work in practice. Two thresholds: `graduateAt=26` and `evictAt=30`. When a message graduates into the forest, it stays in the hot zone for another ~4 messages. By the time it evicts, `resolveDirty()` has already run in the background during the main LLM call. The user doesn't wait and the summaries stay current.

## The experiment

I preregistered three hypotheses before running anything. Written down, committed, timestamped. Not because I expected a journal to review it, but because it's too easy to move the goalposts after seeing results.

12 real GitHub issue conversations. 120 messages each. 8 factual questions per conversation, generated from the uncompressed content, scored by a blinded LLM judge. Flat compression runs contemporaneously on the same data. McNemar's test on discordant pairs.

<div class="results-table" markdown="1">

| Hypothesis | Result | Details |
|---|---|---|
| Latency | **PASS** | append p95 = 0.33ms, render p50 = 0.006ms |
| Cost | **PASS** | 0.79x flat. Cheaper, not just "within 2x" |
| Recall | Trending | +8.3pp (30.2% vs 21.9%), p=0.136 |

</div>

<style>
.results-table table { font-size: 12px !important; min-width: 0 !important; width: auto !important; margin: 1em auto !important; }
.results-table th { background: #f0f0f0 !important; }
</style>

35 summarizer calls across 12 conversations. v1 would have made 960. Flat made 24. The O(n) architecture works.

The recall signal is there but the test is underpowered. 96 questions across 12 conversations, p=0.136. Union-find won 8 conversations, tied 2, lost 2. One conversation (Next.js className mismatch) went 50% union-find vs 0% flat. Another went the other way. A larger study would tell us whether this signal is real.

Limitations worth stating: the questions are LLM-generated and the judge is an LLM. This is directionally useful but noisy. The test domain is GitHub issue threads only. And the summarizer was Flash Lite, not the production model. These results motivate further investigation, not a ship decision.

## Submitting

Feature-flagged behind an experiment flag. Backward compatible. 89/89 tests passing. No migration required. Existing conversations untouched.

The [issue](https://github.com/google-gemini/gemini-cli/issues/22877) has a results table, links to the implementation branch, links to the reproducible experiment harness. The spec repo has the preregistration, the raw data, the latency CSVs. A reviewer can go as deep as they want.

It's a large change. Three new files, three modified files. That goes against the small-incremental-PR norm. But you can't ship the forest without the embedder, or the context window without the forest. It's one feature with tightly coupled components. The feature flag makes it dormant by default.

A prototype blog post doesn't get someone's attention. [Ideas can't find other ideas](/pageleft-manifesto). To have a shot, it had to be a full implementation: feature-flagged, tested, experimentally validated, ready to merge. I used to work at Google. I know the level of rigor they expect before looking at a change this size.

Even then, the issue sat in triage with zero comments. Google projects have internal roadmaps. External contributions of this scope get deprioritized. A reviewer can reasonably say "it's cheaper and faster but you haven't proven it remembers more."

## What I'd tell someone attempting this

Pick a project where the maintainers have explicitly asked for help. A contributing guide that says PRs welcome is boilerplate. The real signal is whether external PRs get reviewed within a week. Check the closed PR list before investing.

Preregister your experiment even if nobody will read it. Especially if nobody will read it. The discipline changes how you build. You can't add a hypothesis after seeing results. You can't retroactively weaken a pass criterion. v1 failed all three hypotheses. That's information. Without preregistration, I'd have been tempted to reframe it as "exploratory" and cherry-pick the one conversation where union-find won by 50pp.

Feature-flag everything. It turns "please merge my alternative architecture" into "please let me add a flag that does nothing by default." The conversation shifts from "should we adopt this" to "is this safe to ship dormant."

Build the experiment harness before you need it. When v1 failed, I could rerun the same 12 conversations on v2 within 6 minutes. The harness cost an afternoon. It saved me from arguing with feelings about whether v2 was actually better.

## Honest accounting

The methodology has its own stack:

1. [General Intelligence](/general-intelligence) — models can't update their own weights. The human closes the learning loop.
2. [Double Loop](/double-loop) — quality control. Write, generate, evaluate, rewrite.
3. [Vibelogging](/vibelogging) — prose as specification. The blog posts are build instructions for an LLM.

All artifacts were produced with LLM assistance. The code, the prose, the experiment harness, this post. The human contribution is the architecture decisions, the preregistration discipline, the willingness to throw out v1 and start over. The LLM wrote the code. I decided what code to write.

One artifact worth calling out: the [work log](https://github.com/kimjune01/union-find-compaction-for-gemini-cli/blob/master/WORK_LOG.md). LLMs lose context between sessions. The work log is how the next session catches up: why v1 failed, what the overlap window is, why `_dirtyInputs` exists. It's a lab notebook for multi-session LLM collaboration. Without it, every new conversation starts from scratch. With it, the LLM picks up where it left off in minutes instead of re-deriving everything from the code.

A trick that pairs with this: before context runs out, ask the LLM to write the prompt that starts the next session. It still has the full conversation in memory. It knows what was decided, what's pending, and what failed. The bootstrap prompt it generates is better than anything you'd write from memory, because it has access to context you've already forgotten. Here's the actual bootstrap prompt from the session that ran the v2 experiment:

```
This session is being continued from a previous conversation that
ran out of context. The summary below covers the earlier portion.

v1 implementation that failed all 3 hypotheses. Design evolution
through multiple iterations (blocking render → overlap window).
contextWindow.ts rewritten for v2: Forest.union() synchronous,
Forest._dirtyInputs tracking, resolveDirty() async. ContextWindow
uses graduateAt/evictAt with _graduatedIndex. 45 tests written
first (TDD), all passing. chatCompressionService updated.

Pending: Run the v2 experiment using the provided Gemini API key.
The command would be:
GEMINI_API_KEY=... npx tsx experiment/v2/run-v2-experiment.ts
```

The next session read this, picked up exactly where the previous one left off, and ran the experiment within minutes. The work log accumulates these handoffs. Each session extends it; the next session reads it back.

The feature might never ship. The issue might never get triaged.

If it does, I'll never have to write a bootstrap prompt again.

---

*Written via the [double loop](/double-loop). All artifacts: [spec repo](https://github.com/kimjune01/union-find-compaction-for-gemini-cli), [implementation branch](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction), [issue](https://github.com/google-gemini/gemini-cli/issues/22877).*
