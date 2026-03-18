---
layout: post-wide
title: "Contributing to Gemini CLI"
tags: coding
---

*Builds on [Union-Find Compaction](/union-find-compaction). Implementation: [gemini-cli fork](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction). Spec and experiment: [union-find-compaction-for-gemini-cli](https://github.com/kimjune01/union-find-compaction-for-gemini-cli).*

> I implemented union-find compaction in Gemini CLI. It produced a cheaper, lower-latency architecture with a positive recall signal. It did not produce a clean win.

Gemini CLI compresses conversations by summarizing the oldest 70% into a single snapshot. Two LLM calls, a 20-30 second spinner, and then your conversation history is a paragraph. It works. It also forces all older context through one bottleneck summary, which drops whatever the summarizer didn't think was important.

The [prototype](/union-find-compaction) established that hierarchical compaction could preserve more detail in isolation. Instead of one flat summary, messages cluster by topic, each cluster keeps its own summary, and retrieval pulls relevant clusters rather than the whole blob. The question was whether the idea survived contact with a real codebase: real API costs, real latency constraints, and implementation complexity.

## v1: wrong on every count

The first attempt translated the prototype directly. Every `union()` call triggered an LLM summarization. The implementation was faithful to the spec. The spec was wrong.

120 messages, 10 clusters. Each graduation merges with the nearest cluster (nearest by cosine similarity of TF-IDF embeddings). Each merge calls the summarizer. That's ~80 LLM calls per conversation. Flat uses 2. The cost ratio was 5.2x. The latency was worse. The recall improvement didn't materialize either. All three preregistered hypotheses failed.

The prototype proved the idea could improve recall. The real system proved the naive implementation erased that advantage under actual cost constraints. Every merge re-summarized an ever-growing cluster from scratch. Message 90 triggers a merge that re-reads messages 1 through 89. Message 91 re-reads 1 through 90. At 120 messages, the quadratic cost surfaced immediately.

## v2: deferred summarization

The fix was to stop summarizing during merges entirely.

`union()` becomes structural. It updates parent pointers, merges children lists, recomputes centroids. No LLM call. It tracks what changed in a dirty map: for each cluster root, the list of texts that need to be summarized together. A singleton's raw content. A previously-clean cluster's cached summary plus the new raw messages that joined.

A concrete example: messages 1-20 form three clusters. Message 21 arrives, gets embedded locally, and joins the nearest cluster by similarity. The cluster is marked dirty. No summarizer call. Later, in the background, `resolveDirty()` takes the cluster's old summary plus message 21's raw text and produces a new summary in one LLM call.

Three operations, three latency profiles:

```
append(msg)       <1ms    Synchronous. Embed locally, push to hot zone, graduate if needed.
render()          <0.1ms  Synchronous. Return cached summaries + hot zone verbatim.
resolveDirty()    ~4s     Async. Batch-summarize dirty clusters in background.
```

The overlap window makes this work. Two thresholds: `graduateAt=26` and `evictAt=30`. When a message graduates into the forest, it stays in the hot zone for another ~4 messages. By the time it evicts, `resolveDirty()` has already run in the background during the main LLM call. Under this design, the user doesn't wait and the summaries stay current.

If this held up, CLI agents could keep longer working memory without adding latency or cost.

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

The issue sat in triage with zero comments. Google projects have internal roadmaps. External contributions of this scope get deprioritized. A reviewer can reasonably say "it's cheaper and faster but you haven't proven it remembers more."

## What I'd tell someone attempting this

Pick a project where the maintainers have explicitly asked for help. A contributing guide that says PRs welcome is boilerplate. The real signal is whether external PRs get reviewed within a week. Check the closed PR list before investing.

Preregister your experiment even if nobody will read it. Especially if nobody will read it. The discipline changes how you build. You can't add a hypothesis after seeing results. You can't retroactively weaken a pass criterion. v1 failed all three hypotheses. That's information. Without preregistration, I'd have been tempted to reframe it as "exploratory" and cherry-pick the one conversation where union-find won by 50pp.

Feature-flag everything. It turns "please merge my alternative architecture" into "please let me add a flag that does nothing by default." The conversation shifts from "should we adopt this" to "is this safe to ship dormant."

Build the experiment harness before you need it. When v1 failed, I could rerun the same 12 conversations on v2 within 6 minutes. The harness cost an afternoon. It saved me from arguing with feelings about whether v2 was actually better.

## Honest accounting

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

The feature might never ship. The issue might never get triaged. But the work stands on its own: a reproducible demonstration that union-find compaction is cheaper and faster than flat summarization, with a positive recall signal that needs a bigger sample to confirm. Anyone can fork the repo, rerun the experiment, and verify.

If union-find compaction ships, I'll never have to write a bootstrap prompt again.

---

*Written via the [double loop](/double-loop). All artifacts: [spec repo](https://github.com/kimjune01/union-find-compaction-for-gemini-cli), [implementation branch](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction), [issue](https://github.com/google-gemini/gemini-cli/issues/22877).*
