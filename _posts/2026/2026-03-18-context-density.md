---
layout: post
title: "Context Density"
tags: cognition coding
---

*Part of the [cognition](/cognition) series. Builds on [The Plateau](/the-plateau).*

[The Plateau](/the-plateau) argues that prose is the densest interpretable medium — pre-compressed by the writer's full pipeline. If that's true, it should be testable: compress the context, measure whether accuracy holds.

I ran the experiment. It didn't work. Here's what I learned.

## The setup

[Chroma's context rot study](https://research.trychroma.com/context-rot) tested 18 frontier models and found that adding 10% irrelevant content to the context window reduced accuracy by 23%. Padding hurts. Nobody had tested the inverse: does compressing the relevant context help?

I reused their pipeline — same dataset ([LongMemEval](https://arxiv.org/abs/2410.10813)), same GPT-4.1 judge, same eval harness — and ran it backward. Question-blind, deletion-only compression: the compressor sees the context but not the question, removes redundancy, preserves propositions. If prose is dense, half the tokens should carry the full signal.

[Full protocol and data.](https://github.com/kimjune01/context-density)

## The result

306 questions, Gemini Flash Lite, focused context.

| Condition | Accuracy | Mean tokens |
|---|---|---|
| Baseline (full context) | 73.9% | 275 |
| Compressed (50%) | 19.0% | 133 |
| Random deletion (50%) | 16.7% | 160 |

Compression destroyed the signal. And it barely outperformed random deletion — 19% vs 17%. At this budget, intelligent compression is indistinguishable from coin-flipping which tokens to keep.

The full-context arm (114K tokens, N=5) was too small and the model too weak (20% baseline) to tell us anything. I stopped the experiment at Step 2.

## Why it failed

The focused context averaged 275 tokens. Compressing 275 tokens to 133 isn't removing redundancy; it's removing signal. The dataset authors had already selected only the relevant conversation turns. There was nothing left to cut.

The interesting experiment — compressing 114K tokens to 57K — wasn't feasible. Flash Lite couldn't handle 114K tokens at baseline (20% accuracy), and spending $25 on a stronger model wasn't justified after the focused-context result.

The stopping rule worked as designed: Step 1 clearly supported H₀, so I stopped.

## The deeper question

While writing [Caches All the Way Down](/caches-all-the-way-down), I put two tables side by side — the computing stack and the biology stack. Same columns, same six roles. The moment both tables were on screen, the contrast jumped out: biology's tower is shorter but brighter (fewer dim cells). Computing's tower is taller but dimmer.

That observation triggered a cascade — contrast → question → hypothesis — faster than I could articulate it. My visual cortex did the diff in parallel. No sequential reading required.

I couldn't have gotten that from prose. Two paragraphs describing the same comparison would have been denser in propositions per token, but slower to process. The table let me see the *relationship between rows*, not just the rows themselves.

Prose is sequential. Tables are spatial. Diagrams are structural. Dashboards are temporal. Each format optimizes for a different kind of attention:

- *Language processor*: sequential argument. Prose wins.
- *Visual processor*: structural comparison. Tables and diagrams win.
- *Temporal processor*: change detection over time. Dashboards and sparklines win.

People prefer dashboards for business intelligence. Nobody reads a BI report as prose. The reason is channel selection, not laziness — the visual cortex processes comparison faster than the language cortex processes description.

## Prose is for complementation

Prose is the densest medium for *complementation* — filling the gap between what the reader knows and what they need to know, one proposition at a time. It's the best format for argument, for narrative, for persuasion. Sequential attention is the right tool when the reader needs to follow a chain of reasoning.

But complementation isn't ingestion. The densest *document* isn't uniform prose. It's mixed-format, matched to the kind of attention each section demands. Argument in prose. Comparison in tables. Relationships in diagrams. Trends in sparklines.

The context-density experiment tested prose → prose compression. The more interesting experiment — the one the null points toward — would test format transformation: same propositions, different channel. Can a table carry the same information as a paragraph in fewer tokens *and* higher accuracy? Not because the tokens are denser, but because the format matches the processor.

That's a different experiment. The current one earned its null. The next one has a sharper question.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
