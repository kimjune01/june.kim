---
layout: post
title: "Context Density"
tags: cognition coding
---

*Part of the [cognition](/cognition) series. Builds on [The Plateau](/the-plateau).*

[The Plateau](/the-plateau) argues that prose is the densest interpretable medium, pre-compressed by the writer's full pipeline. If that's true, it should be testable: compress the context, measure whether accuracy holds.

I ran the experiment. It didn't work. But the null pointed somewhere better.

## The setup

[Chroma's context rot study](https://research.trychroma.com/context-rot) tested 18 frontier models and found that adding 10% irrelevant content to the context window reduced accuracy by 23%. Padding hurts. Nobody had tested the inverse: does compressing the relevant context help?

I reused their pipeline. Same dataset ([LongMemEval](https://arxiv.org/abs/2410.10813)), same GPT-4.1 judge, same eval harness. Ran it backward. Question-blind, deletion-only compression: the compressor sees the context but not the question, removes redundancy, preserves propositions. If prose is dense, half the tokens should carry the full signal.

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

The focused context averaged 275 tokens. Compressing that to 133 just removes signal. The dataset authors had already selected only the relevant conversation turns. There was nothing left to cut.

The interesting experiment, compressing 114K tokens to 57K, wasn't feasible. Flash Lite couldn't handle 114K tokens at baseline (20% accuracy), and spending $25 on a stronger model wasn't justified after the focused-context result.

The stopping rule worked as designed: Step 1 clearly supported H₀, so I stopped.

The experiment measured density in tokens. But the insight came from a table.

## What the table showed

While writing [Caches All the Way Down](/caches-all-the-way-down), I put two tables side by side: the computing stack and the biology stack. Same columns, same six roles. The moment both tables were on screen, the contrast jumped out: biology's tower is shorter but brighter (fewer dim cells). Computing's tower is taller but dimmer.

That observation triggered a cascade — contrast → question → hypothesis — faster than I could articulate it. My visual cortex did the diff in parallel. No sequential reading required.

I couldn't have gotten that from prose. Two paragraphs describing the same comparison would carry more propositions per token, but process slower. The table let me see the relationship between rows, not individual rows.

Each format optimizes for a different processor. [Paivio (1986)](https://global.oup.com/academic/product/mental-representations-9780195066661) established that humans maintain independent verbal and visual-spatial systems. Information encoded in both is recalled better than information in either alone. [Sweller (1988)](https://doi.org/10.1016/0364-0213(88)90023-7) showed each channel has limited capacity, so distributing across channels increases effective bandwidth.

| Format | Processor | Strength |
|---|---|---|
| Prose | Language (sequential) | Argument |
| Lists | Scanning (parallel) | Filtering, skimming |
| Tables | Visual (spatial) | Comparison |
| Diagrams | Visual (structural) | Relationships |
| Code | Pattern matching | Implementation |
| Equations | Symbolic | Proof |
| Dashboards | Temporal (diff) | Monitoring |

[Vessey (1991)](https://doi.org/10.1111/j.1540-5915.1991.tb00344.x) called this *cognitive fit*: performance is best when the representation matches the task. Spatial tasks (comparison, trends) are better served by graphs and tables. Symbolic tasks (precise value lookup) are better served by text. When the format mismatches the task, performance degrades. She reconciled years of contradictory graphs-vs-tables research with one insight: it depends on the task.

Nobody reads a BI report as prose. That's cognitive fit, not laziness.

## Match the format to the processor

Prose is the densest medium for *complementation*: filling the gap between what the reader knows and what they need to know, one proposition at a time. Sequential attention is the right tool when the reader needs to follow a chain of reasoning.

But the densest *document* uses all the channels. [Mayer (2009)](https://doi.org/10.1017/CBO9780511811678) meta-analyzed the effect: words plus pictures outperform words alone with a median effect size of d = 1.39. The catch: arbitrary mixing hurts. The formats must match the content, and they must be spatially integrated ([Chandler & Sweller, 1991](https://doi.org/10.1080/07370008.1991.9649028)).

The recommendation: for each section of a document, pick the format that matches the kind of attention it demands. Argument in prose. Comparison in tables. Trends in sparklines. Don't default to uniform prose when a table would let the reader's visual cortex do the work.

We write for two audiences now. An LLM reads everything as tokens. Multimodal models can process images, but slowly and expensively compared to a human glancing at a table. The format advantage is overwhelmingly human. So every document has two readers with different optimal formats: the human who benefits from mixed format, and the model that just wants dense tokens.

This experiment tested prose → prose compression, which is the LLM's perspective. Four decades of cognitive psychology already tested the human perspective. The null pointed somewhere useful: density isn't just about fewer tokens. It's about the right tokens in the right format for the right processor.

## The cusp

Format selection is a [Filter](/perception-pipe) decision: which processor should this information route to? A comparison routed to the language processor wastes sequential attention on work the visual cortex does for free. A proof routed to a diagram wastes spatial bandwidth on work that needs symbolic manipulation.

When I write with [skills](/double-loop), they automate Filter-level work — cut filler, flag restated points, check the arc. Format matching is the same kind of work: reject the wrong medium before the reader has to. A tighten pass catches redundant words. A format pass catches redundant *processing* — information forced through a channel that can't handle it efficiently.

Better format matching makes prose writing faster, because you stop writing prose where a table belongs. It makes attention easier, because each section arrives through the channel that processes it cheapest. And it fills one more cell in the [framework](/the-natural-framework): the Filter role applied not to content but to presentation.

Every dim cell filled is a step toward [general intelligence](/general-intelligence). Most of those cells are in Consolidate. This one is in Filter. Small, but real.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
