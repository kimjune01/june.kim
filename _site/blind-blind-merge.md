*Builds on [The Spec Is a Hypothesis](/the-spec-is-a-hypothesis).*

Spec, code, iterate. Everyone knows the third step is where the time goes. Ten bugs in code review. Twenty spec revisions. Fifteen design decisions before the LLM could even start. The [previous post](/the-spec-is-a-hypothesis) identified the boundary -- prose carries architecture, code carries constraints. It stopped there.

Two frontier models exist. I ran both.

## The experiment

[Union-find](https://en.wikipedia.org/wiki/Disjoint-set_data_structure) context compaction for [Gemini CLI](https://github.com/google-gemini/gemini-cli). Three inputs for the implementer:

1. The existing TypeScript source (ground truth)
2. A prose transformation spec (the hypothesis)
3. A working [Python prototype](https://github.com/kimjune01/union-find-compaction) (existence proof)

First run: the original pipeline. Extract existing behavior into prose, design a transformation spec, hand it to an LLM. Working implementation, all tests passing. Then code review found ten bugs. Twenty spec revisions. Two days of back and forth.

Second and third runs: [GPT-5.4 (Codex)](https://github.com/openai/codex) and Claude Opus 4.6, separately. Neither saw the other's output. Same three inputs, same one-sentence directive:

> No regressions, UX improvement. Existing behavior is correct unless the spec explicitly changes it. Code wins on invariants. Spec wins on the blocking path.

That's the authority rule. It displaced fifteen design decisions with one sentence.

## Fifteen decisions, one sentence

Before the authority rule, Codex wanted those decisions resolved upfront. Hot zone size. Model routing. Merge threshold. Timestamp format. Persistence strategy. Failure backoff. Hook contracts. Content serialization.

When pushed to be pragmatic -- "which of these do you actually need from me?" -- every one collapsed. Existing behavior is correct, so no regressions. New behavior must improve UX, so spec wins on the blocking path. Everything else: read the code, follow the rule.

Zero human decisions. Both implementers started coding.

## Complementary failures

The two blind implementations made complementary mistakes.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:7em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Codex (GPT-5.4)</th><th style="background:#f0f0f0">Claude Opus 4.6</th></tr></thead>
<tr><td><em>Got right</em></td><td>Persistent state, config-driven tuning, rich serialization, query-aware retrieval</td><td>Per-cluster error recovery, timestamp preservation, original Content objects for hot messages</td></tr>
<tr><td><em>Got wrong</em></td><td>Flattened all output to <code>role: 'user'</code>, destroyed conversation structure</td><td>Broke incremental ingestion, wrong persistence key, dropped failure-handling params</td></tr>
</table>

Different models fail on different sides of the same boundary. Neither was shippable. Both were necessary.

## The Method: Blind, Blind, Merge

<div style="max-width:1080px; margin:1em auto;">
<img src="/assets/img/authority-rule-workflow.svg" alt="Authority rule workflow: three inputs plus authority rule feed two blind coding agents, cross-review finds contradictions, synthesis absorbs best of both, fresh judge ranks the result" style="width:100%;"/>
</div>

The fourth implementation is the [pushout](https://en.wikipedia.org/wiki/Pushout_(category_theory)): Codex's architecture merged with Claude's defensive patterns along their shared inputs. A fresh reviewer (blind to the history) ranked the four versions:

1. *Synthesis* -- closest to production
2. *Original pipeline* -- simplest, fewest structural mistakes
3. *Claude (blind)* -- good patterns, broken plumbing
4. *Codex (blind)* -- good architecture, broken integration

The surprise: the original pipeline ranked second. It never read the existing source, yet it had fewer structural mistakes than either blind implementation. Ignorance was protective. Ambition created more surface area for bugs. But the synthesis couldn't exist without both.

The value lived in the loop between implementations.

## What it cost

<table style="max-width:490px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:9em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Spec, code, iterate</th><th style="background:#f0f0f0">Blind, blind, merge</th></tr></thead>
<tr><td><em>Wall clock</em></td><td>~2 days</td><td>1 hour</td></tr>
<tr><td><em>Human decisions</em></td><td>15</td><td>0</td></tr>
<tr><td><em>Spec revisions</em></td><td>20</td><td>0</td></tr>
<tr><td><em>Bugs remaining</em></td><td>10</td><td>1 (ingestion drift)</td></tr>
</table>

More LLM work. Far less human work. You're paying for the subscriptions anyway.

## The last mile

The bug class didn't change across any implementation: serialization loss, concurrency guards, lifecycle management. Every implementation hit bugs at boundaries the spec didn't define. The authority rule shrank the surface area. The synthesis loop caught more instances. But the failure mode is structural: prose can't carry type contracts, and no amount of process eliminates that boundary.

The contradiction-finding pass was valuable for forcing deep reading before writing code. Every risk it catalogued, it later hit. It knew where to look.

This methodology gets you closer to the finish line faster. The last mile is still code review by someone who understands both the architecture and the type system. Blind, blind, merge -- then a human looks at what's left.

## Why does it work?

The prose spec carries the *why*. Code tells you what the system does, never what it should do. Without the spec, the LLM guesses intent. It guesses wrong.

The prototype encodes decisions the prose left abstract: merge thresholds, similarity functions, lifecycle details. This could be a standalone implementation or an [experiment](https://github.com/kimjune01/union-find-compaction/blob/master/EXPERIMENT.md). Ours was ~300 lines of Python.

The authority rule collapses ambiguity. One sentence that says what wins when the inputs conflict. Leave it out and the LLM asks you to resolve every decision upfront. Or worse, guesses.

And two models instead of one? Different training, different blind spots. They fail on different sides of the same boundary. You can't get that from running the same model twice.

---

*Written via the [double loop](/double-loop). For more, see [work log](/work-log).*
