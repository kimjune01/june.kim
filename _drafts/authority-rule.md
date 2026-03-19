---
layout: post
title: "Blind, Blind, Merge"
tags: methodology coding
---

*Builds on [The Spec Is a Hypothesis](/the-spec-is-a-hypothesis).*

Spec, code, iterate. Everyone knows the third step is where the time goes. Ten bugs in code review. Twenty spec revisions. Fifteen design decisions before the LLM could even start. The [previous post](/the-spec-is-a-hypothesis) identified the boundary -- prose carries architecture, code carries constraints. It stopped there.

Two frontier models exist. I ran both.

## The experiment

[Union-find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) context compaction for [Gemini CLI](https://github.com/google-gemini/gemini-cli). Three inputs for the implementer:

1. The existing TypeScript source (ground truth)
2. A prose transformation spec (the hypothesis)
3. A working [Python prototype](https://github.com/kimjune01/union-find-compaction) (existence proof)

First run: the original pipeline. Extract existing behavior into prose, design a transformation spec, hand it to an LLM. Working implementation, all tests passing. Then code review found ten bugs. Twenty spec revisions. Two weeks of back and forth.

Second and third runs: [GPT-5.4 (Codex)](https://github.com/openai/codex) and Claude Opus, separately. Neither saw the other's output. Same three inputs, same one-sentence directive:

> No regressions, UX improvement. Existing behavior is correct unless the spec explicitly changes it. Code wins on invariants. Spec wins on the blocking path.

That's the authority rule. It replaced fifteen design decisions with one sentence.

## Fifteen decisions, one sentence

Before the authority rule, Codex wanted fifteen design decisions resolved upfront. Hot zone size. Model routing. Merge threshold. Timestamp format. Persistence strategy. Failure backoff. Hook contracts. Content serialization.

When pushed to be pragmatic -- "which of these do you actually need from me?" -- every one collapsed. Existing behavior is correct, so no regressions. New behavior must improve UX, so spec wins on the blocking path. Everything else: read the code, follow the rule.

Zero human decisions. Both implementers started coding.

## Complementary failures

The two blind implementations made complementary mistakes.

| | Codex (GPT-5.4) | Claude Opus |
|---|---|---|
| *Got right* | Persistent state, config-driven tuning, rich serialization, query-aware retrieval | Per-cluster error recovery, timestamp preservation, original Content objects for hot messages |
| *Got wrong* | Flattened all output to `role: 'user'`, destroyed conversation structure | Broke incremental ingestion, wrong persistence key, dropped failure-handling params |

Different models fail on different sides of the same boundary. Neither was shippable. Both were necessary.

## The synthesis

<img src="/assets/img/authority-rule-workflow.svg" alt="Authority rule workflow: three inputs plus authority rule feed two blind LLMs, cross-review finds contradictions, synthesis absorbs best of both, fresh judge ranks the result" style="width:100%; max-width:960px;"/>

The fourth implementation absorbed the best of both: Codex's architecture with Claude's defensive patterns. A fresh reviewer (blind to the history) ranked the four versions:

1. *Synthesis* -- closest to production
2. *Original pipeline* -- simplest, fewest structural mistakes
3. *Claude (blind)* -- good patterns, broken plumbing
4. *Codex (blind)* -- good architecture, broken integration

The surprise: the original pipeline ranked second. The conservative implementation that never read the existing source had fewer structural mistakes than either blind implementation that did. Ignorance was protective. Ambition created more surface area for bugs. But neither blind implementation was wasted, because the synthesis couldn't exist without both.

The value lived in the loop between implementations.

## What it cost

| | Original pipeline | Blind, blind, merge |
|---|---|---|
| *Wall clock* | ~2 weeks | 1 afternoon |
| *Human decisions* | 15 | 0 |
| *Spec revisions* | 20 | 0 |
| *Bugs remaining* | 10 | 1 (ingestion drift) |

More LLM work. Far less human work. You're paying for the subscriptions anyway.

## The last mile

The bug class didn't change across any implementation: serialization loss, concurrency guards, lifecycle management. Every implementation hit bugs at boundaries the spec didn't define. The authority rule reduced the surface area, and the synthesis loop caught more instances. But the failure mode is structural: prose can't carry type contracts, and no amount of process eliminates that boundary.

The contradiction-finding pass was valuable for forcing deep reading before writing code. Every risk it catalogued, it later hit a specific instance of. It knew where to look.

This methodology gets you closer to the finish line faster. The last mile is still code review by someone who understands both the architecture and the type system. Blind, blind, merge -- then a human looks at what's left.

## The recipe

Three phases: build the inputs, run two blind implementations, merge the best parts.

*Phase 1: Build the inputs.*

Write a prose spec. The prose carries architecture, intent, and the *why* behind design choices. Without it, the LLM will infer intent from the code and get it wrong -- code tells you what the system does, never what it should do. The spec is the hypothesis the implementation tests against.

Then build a prototype from the spec. Any language, any framework. Depending on what you're applying to the codebase, this could be a standalone implementation or an [experiment](https://github.com/kimjune01/union-find-compaction/blob/master/EXPERIMENT.md) that validates the design. Either way, it proves the algorithm works and encodes decisions the prose left abstract: merge thresholds, similarity functions, lifecycle details. The Python prototype in this experiment was ~300 lines.

Finally, write the authority rule. One sentence that says what wins when the inputs conflict. Ours was: "No regressions, UX improvement." Without it, the LLM will ask you to resolve every ambiguity upfront. Or worse, guess.

*Phase 2: Blind, blind.*

Give two LLMs the same four inputs simultaneously: prose spec, prototype, legacy codebase, authority rule. No lossy extraction step. Run a contradiction-finding pass first, then push back: "Which of these do you actually need from me?" Most will collapse under the authority rule. Let both implement blind.

*Phase 3: Merge.*

Cross-review: show each implementation the other. Surface contradictions. Synthesize the best parts. One more review pass to verify.

The human decides what to build and what wins when things conflict. The LLMs figure out the rest.

---

*Full receipts in the [work log](/two-input-worklog).*
