---
layout: post
title: "Zero Comments"
tags: coding methodology
---

*Builds on [Union-Find Compaction](/union-find-compaction). Implementation: [gemini-cli fork](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction). Spec and experiment: [union-find-compaction-for-gemini-cli](https://github.com/kimjune01/union-find-compaction-for-gemini-cli).*

Ninety minutes into a session. The agent has your codebase in context, your test failures explained, your refactor halfway done. Then you glance at the status bar.

![Context left until auto-compact: 0%](/assets/auto-compact-0.png)

Twenty seconds of spinner. Your conversation history becomes a paragraph. You ask about the refactor. The agent doesn't remember. You start a new session and spend another minute re-explaining what the last one already knew.

This is flat compression. Gemini CLI summarizes the oldest 70% into a single snapshot. It works, but it forces everything through one bottleneck that drops whatever the summarizer prompt didn't prioritize.

I'd been brewing on this for months. The stack:

1. [Manual Context Compaction](/manual-context-compaction) — the pain. Dump context to markdown before the window fills.
2. [Context Synthesis is Quadratic](/context-synthesis-is-quadratic) — the theory. Long contexts degrade faster than linear because synthesis is pairwise.
3. [The Natural Framework](/the-natural-framework) — a cognition model. How memory, retrieval, and compression relate.
4. [Diagnosis LLM](/diagnosis-llm) — the diagnostic. Flat summary destroys provenance, expandability, and selective retrieval.
5. [The Parts Bin](/the-parts-bin) — union-find as a candidate fix sitting in the parts bin.
6. [Union-Find Compaction](/union-find-compaction) — the prototype. Clusters by topic, each with its own summary.

The [prototype](/union-find-compaction) proved that compaction UX and permanent erasure can be fixed while preserving just as much detail. Would it survive a real codebase? Real API costs, real latency, real implementation complexity. I built it, tested it, and submitted it to Google.

## Vibelogging in prod

This is [vibelogging](/vibelogging) applied to a real codebase. Before writing any code, I wrote the spec as prose:

> 1. Extract the current system from the codebase
> 2. Describe it in plain language
> 3. Verify the prose matches the code (no-delta checkpoint)
> 4. Write a systems comparison
> 5. Write a transformation design
> 6. Elicit every design decision, least to most uncertain
> 7. Preregister hypotheses
> 8. Hand the spec to an LLM and implement

One-shot. The LLM read the transformation spec and produced the full system: forest, embedder, summarizer, context window, dual-path dispatch, feature flag. 75 tests passing, zero type errors.

## v1: wrong on every count

The tests passed, but the spec was wrong.

The spec assumed ~10 merges per conversation. Reality: ~80, because every `union()` call triggered an LLM summarization. That's ~80 LLM calls per conversation. Flat uses 2. Cost ratio: 5.2x. Latency was worse. Recall didn't improve. All three preregistered hypotheses failed.

Every merge re-summarized an ever-growing cluster from scratch. Message 90 re-reads messages 1 through 89. Message 91 re-reads 1 through 90. Quadratic.

## v2: lazy summarization

I didn't fix the code. I fixed the spec. That is how compilers work: you fix the source, not the binary.

I pointed out the architectural fix. The LLM edited the spec: added warnings describing what went wrong, rewrote eight sections of the prose. Then a fresh session read the updated spec and produced v2. I didn't even have to look at the code.

| | Flat | Union-find v2 |
|---|---|---|
| Append | N/A | <1ms |
| Render | N/A | <0.1ms |
| Compress | 20-30s | ~4s |
| LLM calls | 2 per event | 1 per cluster |
| Originals | Discarded | Kept |

## The experiment

I preregistered three hypotheses before running anything. Written down, committed, timestamped. Not for a journal, but because it's too easy to move the goalposts after seeing results.

12 real GitHub issue conversations. 120 messages each. 8 factual questions per conversation, generated from the uncompressed content, scored by a blinded LLM judge. Flat compression runs on the same data. McNemar's test on discordant pairs.

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

## Submitting

Feature-flagged behind an experiment flag. 89/89 tests passing. Existing conversations untouched.

The [issue](https://github.com/google-gemini/gemini-cli/issues/22877) links to the implementation branch, the experiment harness, and the spec repo with preregistration, raw data, and latency CSVs. A reviewer can go as deep as they want.

Three new files, three modified files. That goes against the small-incremental-PR norm, but you can't ship the forest without the embedder or the context window without the forest. One feature, tightly coupled. The feature flag makes it dormant by default.

A prototype blog post doesn't get someone's attention. [Ideas can't find other ideas](/pageleft-manifesto). To have a shot, it had to be a full implementation: feature-flagged, tested, experimentally validated, ready to merge. I used to work at Google so I know the level of rigor they expect before looking at a change this size.

Even then, the issue sat in triage with zero comments. Google projects have internal roadmaps. External contributions of this scope get deprioritized. A reviewer can reasonably say "it's cheaper and faster but you haven't proven it remembers more."

## Honest accounting

The methodology has its own stack:

1. [General Intelligence](/general-intelligence) — models can't update their own weights. The human closes the learning loop.
2. [Double Loop](/double-loop) — quality control. Write, generate, evaluate, rewrite.
3. [Vibelogging](/vibelogging) — prose as specification. The blog posts are build instructions for an LLM.

Without this methodology, I couldn't have shipped a feature this size. The spec repo, the implementation, the experiment, and the submission took about five and a half hours start to finish. All artifacts were produced with LLM assistance: the code, the prose, the experiment harness, this post. The LLM wrote the code. I decided what code to write. Code is disposable. The prose is what accumulates.

The [work log](https://github.com/kimjune01/union-find-compaction-for-gemini-cli/blob/master/WORK_LOG.md) made multi-session work possible. LLMs lose context between sessions. The work log is how the next session catches up: why v1 failed, what the overlap window is, why `_dirtyInputs` exists. Without it, every new conversation starts from scratch. With it, the LLM picks up in minutes.

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

The feature might never ship. But if it does, I'll never have to write a bootstrap prompt again.

---

*Written via the [double loop](/double-loop). All artifacts: [spec repo](https://github.com/kimjune01/union-find-compaction-for-gemini-cli), [implementation branch](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction), [issue](https://github.com/google-gemini/gemini-cli/issues/22877).*
