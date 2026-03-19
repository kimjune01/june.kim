---
layout: post
title: "Blind, Blind, Merge"
tags: methodology coding
---

*Builds on [The Spec Is a Hypothesis](/the-spec-is-a-hypothesis).*

The spec-is-a-hypothesis workflow had a gap. The blog post identified the boundary -- prose carries architecture, code carries constraints -- and stopped there. Ten bugs in code review. Twenty spec revisions. Fifteen design decisions written before implementation. The human was doing the LLM's job.

## The experiment

Same task, same inputs, different workflow. Union-find context compaction for [Gemini CLI](https://github.com/google-gemini/gemini-cli). Three inputs for the implementer:

1. The existing TypeScript source (ground truth)
2. A prose transformation spec (the hypothesis)
3. A working [Python prototype](https://github.com/kimjune01/union-find-compaction) (existence proof)

First run: the original pipeline. Extract existing behavior into prose, design a transformation spec, hand it to an LLM. The LLM produced a working implementation. Code review found ten bugs. The spec got revised twenty times.

Second and third runs: two blind implementations using the workflow below. GPT-5.4 (Codex) and Claude Opus, separately. Neither saw the other's output. Same three inputs, same one-sentence directive:

> No regressions, UX improvement. Existing behavior is correct unless the spec explicitly changes it. Code wins on invariants. Spec wins on the blocking path.

That's the authority rule.

## What the authority rule replaced

Before the authority rule, the implementer wanted fifteen design decisions resolved upfront. Hot zone size. Model routing. Merge threshold. Timestamp format. Persistence strategy. Failure backoff. Hook contracts. Content serialization.

When pushed to be pragmatic -- "which of these do you actually need from me?" -- every one collapsed. The authority rule answered them all. Existing behavior is correct (no regressions). New behavior must improve UX (spec wins on the blocking path). Everything else: read the code, follow the rule.

Zero human decisions. Both implementers started coding.

## Neither implementation shipped alone

The two blind implementations made complementary mistakes.

Codex built the better architecture: persistent state on the chat object, config-driven tuning, rich Content serialization, query-aware retrieval. But it flattened all output to synthetic `role: 'user'` messages, destroying the original conversation structure. A major integration regression.

Claude built the better defensive patterns: per-cluster error recovery in background summarization, timestamp preservation in dirty-input collection, original Content objects preserved for hot messages. But it broke incremental ingestion, keyed persistence to the wrong identifier, and dropped failure-handling parameters from the API contract.

Each one got right what the other got wrong. Neither was shippable.

## The synthesis loop

<img src="/assets/img/authority-rule-workflow.svg" alt="Authority rule workflow: three inputs plus authority rule feed two blind LLMs, cross-review finds contradictions, synthesis absorbs best of both, fresh judge ranks the result" style="width:100%; max-width:960px;"/>

The fourth implementation absorbed the best of both: Codex's architecture with Claude's defensive patterns. A fresh reviewer (blind to the history) ranked the four versions:

1. **Synthesis** -- closest to production
2. **Original pipeline** -- simplest, fewest structural mistakes
3. **Claude (blind)** -- good patterns, broken plumbing
4. **Codex (blind)** -- good architecture, broken integration

The value lived in the loop between implementations.

## The methodology

1. **Give the LLM all inputs simultaneously.** Existing source (ground truth), prose spec (hypothesis), and prototype (existence proof). No lossy extraction step.
2. **State the authority rule.** One sentence: what wins when they conflict. This replaces the design decisions document.
3. **Run a contradiction-finding pass.** Let the LLM catalogue risks. Then push back: "Which of these do you actually need from me?" Most will collapse.
4. **Run two blind implementations.** Different LLMs, same inputs, same rule. They will make complementary mistakes.
5. **Cross-review.** Show each implementation the other. Surface contradictions, not preferences.
6. **Synthesize.** Absorb the best parts. One more review pass to verify.

The human decides what to build and what wins when things conflict. The LLMs figure out the rest.

## What it costs

Three implementations and two review passes for one feature. That sounds expensive until you compare it to the alternative: one implementation, ten bugs, twenty spec revisions, fifteen design decisions, and a code review cycle that taught the spec things it didn't know.

The synthesis loop front-loads the cost. The original pipeline back-loads it.

## What it doesn't fix

The bug class didn't change across any implementation. Serialization loss. Concurrency guards. Lifecycle management. Every implementation hit bugs at boundaries the spec didn't define. The authority rule reduced the surface area. The synthesis loop caught more instances. But the failure mode is structural: prose can't carry type contracts, and no amount of process eliminates that boundary.

The contradiction-finding pass was valuable for forcing deep reading before writing code. Every risk it catalogued, it later hit a specific instance of. It knew where to look.

This methodology gets you closer to the finish line faster. The last mile is still code review by someone who understands both the architecture and the type system. Blind, blind, merge -- then a human looks at what's left.

---

*Full receipts in the [work log](/two-input-worklog).*
