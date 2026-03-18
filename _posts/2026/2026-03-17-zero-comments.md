---
layout: post-wide
title: "Zero Comments"
tags: coding
---

*Builds on [Union-Find Compaction](/union-find-compaction). Implementation: [gemini-cli fork](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction). Spec and experiment: [union-find-compaction-for-gemini-cli](https://github.com/kimjune01/union-find-compaction-for-gemini-cli).*

Ninety minutes into a session. The agent has your codebase in context, your test failures explained, your refactor halfway done. Then you glance at the status bar.

![Context left until auto-compact: 0%](/assets/auto-compact-0.png)

Twenty seconds of spinner. Two LLM calls. Your conversation history becomes a paragraph. The summarizer keeps what it thinks matters and drops the rest. You ask about the refactor. The agent apologizes. It doesn't remember. You write a bootstrap prompt, start a new session, and spend ten minutes re-explaining what the last session already knew.

This is flat compression. Gemini CLI summarizes the oldest 70% into a single snapshot. It works, but forces everything through one bottleneck that drops whatever the summarizer didn't prioritize.

I'd been circling this problem for months. The stack:

1. [Manual Context Compaction](/manual-context-compaction) — the pain. Dump context to markdown before the window fills.
2. [Context Synthesis is Quadratic](/context-synthesis-is-quadratic) — the theory. Long contexts degrade faster than linear because synthesis is pairwise.
3. [The Natural Framework](/the-natural-framework) — a cognition model. How memory, retrieval, and compression relate.
4. [Diagnosis LLM](/diagnosis-llm) — the diagnostic. Flat summary destroys provenance, expandability, and selective retrieval.
5. [The Parts Bin](/the-parts-bin) — union-find as a candidate fix sitting in the parts bin.
6. [Union-Find Compaction](/union-find-compaction) — the prototype. Clusters by topic, each with its own summary.

The [prototype](/union-find-compaction) proved that compaction UX and permanent erasure can be fixed while preserving just as much detail. The question was whether it survived a real codebase: real API costs, real latency, real implementation complexity. I built it, tested it, and submitted it to Google.

## v1: wrong on every count

The first attempt translated the prototype directly. Every `union()` call triggered an LLM summarization. The implementation was faithful to the spec. The spec was wrong.

120 messages, 10 clusters. Each merge calls the summarizer. That's ~80 LLM calls per conversation. Flat uses 2. Cost ratio: 5.2x. Latency was worse. Recall didn't improve. All three preregistered hypotheses failed.

The prototype proved the idea could improve recall. The real system erased that advantage under actual cost constraints because every merge re-summarized an ever-growing cluster from scratch. Message 90 re-reads messages 1 through 89. Message 91 re-reads 1 through 90. Quadratic.

## v2: lazy summarization

The fix was to stop summarizing during merges entirely.

`union()` becomes structural: update parent pointers, merge children lists, recompute centroids. No LLM call. A dirty map tracks what changed: for each cluster root, the texts that need summarizing together.

Messages 1-20 form three clusters. Message 21 arrives, gets embedded locally, joins the nearest cluster. Marked dirty. Later, `resolveDirty()` takes the cluster's old summary plus message 21's raw text and produces a new summary in one LLM call.

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

Flat discards original messages after compression. Union-find keeps them. Every cluster links back to its sources, so if a summary drops a detail, you expand the cluster and recover the original text.

The overlap window makes this work. Two thresholds: `graduateAt=26` and `evictAt=30`. When a message graduates into the forest, it stays in the hot zone for ~4 more messages. By the time it evicts, `resolveDirty()` has already run in the background. The user doesn't wait.

## The experiment

I preregistered three hypotheses before running anything. Written down, committed, timestamped. Not for a journal, but because it's too easy to move the goalposts after seeing results.

12 real GitHub issue conversations. 120 messages each. 8 factual questions per conversation, generated from the uncompressed content, scored by a blinded LLM judge. Flat compression runs contemporaneously on the same data. McNemar's test on discordant pairs.

<div class="results-table" markdown="1">

| Hypothesis | Result | Details |
|---|---|---|
| Latency | **PASS** | append p95 = 0.33ms, render p50 = 0.006ms |
| Cost | **PASS** | 0.79x flat. 21% cheaper |
| Recall | Trending | +8.3pp (30.2% vs 21.9%), p=0.136 |

</div>

<style>
.results-table table { font-size: 12px !important; min-width: 0 !important; width: auto !important; margin: 1em auto !important; }
.results-table th { background: #f0f0f0 !important; }
</style>

35 summarizer calls across 12 conversations. v1 would have made 960. Flat made 24.

The recall signal is there but underpowered. 96 questions, p=0.136. Union-find won 8 conversations, tied 2, lost 2. The evidence is consistent with a moderate recall gain or noise; not strong enough to claim improvement.

The questions are LLM-generated and the judge is an LLM. The test domain is GitHub issue threads only, and the summarizer was Flash Lite, not the production model. These results motivate investigation, not a ship decision.

## Submitting

Feature-flagged behind an experiment flag. 89/89 tests passing. Existing conversations untouched.

The [issue](https://github.com/google-gemini/gemini-cli/issues/22877) links to the implementation branch, the experiment harness, and the spec repo with preregistration, raw data, and latency CSVs. A reviewer can go as deep as they want.

Three new files, three modified files. That goes against the small-incremental-PR norm, but you can't ship the forest without the embedder or the context window without the forest. One feature, tightly coupled. The feature flag makes it dormant by default.

A prototype blog post doesn't get someone's attention. [Ideas can't find other ideas](/pageleft-manifesto). To have a shot, it had to be a full implementation: feature-flagged, tested, experimentally validated, ready to merge. I used to work at Google. I know the level of rigor they expect before looking at a change this size.

Even then, the issue sat in triage with zero comments. Google projects have internal roadmaps. External contributions of this scope get deprioritized. A reviewer can reasonably say "it's cheaper and faster but you haven't proven it remembers more."

## Honest accounting

The methodology has its own stack:

1. [General Intelligence](/general-intelligence) — models can't update their own weights. The human closes the learning loop.
2. [Double Loop](/double-loop) — quality control. Write, generate, evaluate, rewrite.
3. [Vibelogging](/vibelogging) — prose as specification. The blog posts are build instructions for an LLM.

Without this methodology, I couldn't have shipped a feature this size. The spec repo, the implementation, the experiment, and the submission took about five and a half hours start to finish. All artifacts were produced with LLM assistance: the code, the prose, the experiment harness, this post. The LLM wrote the code. I decided what code to write.

One artifact worth calling out: the [work log](https://github.com/kimjune01/union-find-compaction-for-gemini-cli/blob/master/WORK_LOG.md). LLMs lose context between sessions. The work log is how the next session catches up: why v1 failed, what the overlap window is, why `_dirtyInputs` exists. Without it, every new conversation starts from scratch. With it, the LLM picks up in minutes.

A trick that pairs with this: before context runs out, ask the LLM to write the prompt that starts the next session. It still has full context, so the bootstrap prompt it generates is better than anything you'd write from memory.

<details><summary>The actual bootstrap prompt from the session that ran the v2 experiment</summary>

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

The next session read this, picked up where the previous one left off, and ran the experiment within minutes.

</details>

The feature might never ship. The issue might never get triaged.

If it does, I'll never have to write a bootstrap prompt again.

---

*Written via the [double loop](/double-loop). All artifacts: [spec repo](https://github.com/kimjune01/union-find-compaction-for-gemini-cli), [implementation branch](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction), [issue](https://github.com/google-gemini/gemini-cli/issues/22877).*
