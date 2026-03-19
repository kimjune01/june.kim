*Part of the [cognition](/cognition) series. Builds on [The Plateau](/the-plateau).*

[The Plateau](/the-plateau) argues that prose is the densest interpretable medium, pre-compressed by the writer's full pipeline. If true, it's testable: compress the context, measure whether accuracy holds.

I ran the experiment. It didn't work. But the null pointed somewhere better.

## The setup

[Chroma's context rot study](https://research.trychroma.com/context-rot) tested 18 frontier models and found that adding 10% irrelevant content to the context window reduced accuracy by 23%. Padding hurts. Nobody had tested the inverse: does compressing the relevant context help?

I reused their pipeline. Same dataset ([LongMemEval](https://arxiv.org/abs/2410.10813)), same GPT-5.4 judge, same eval harness. Ran it backward. Question-blind, deletion-only compression. If prose is dense, half the tokens should carry the full signal.

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

The focused context averaged 275 tokens. Compressing that to 133 just removes signal. The dataset authors had already selected the relevant turns. There was nothing left to cut.

The interesting experiment, compressing 114K tokens to 57K, wasn't feasible. Flash Lite couldn't handle 114K tokens at baseline (20% accuracy), and spending $25 on a stronger model wasn't justified after the focused-context result.

The stopping rule worked as designed: Step 1 clearly supported H₀, so I stopped.

The experiment measured density in tokens. But the insight came from a table.

## What the table showed

Compressing within a medium is different from choosing the right medium. I was measuring how many tokens survive deletion. The actual question is which cognitive system processes the information.

While writing [Caches All the Way Down](/caches-all-the-way-down), I put two tables side by side: the computing stack and the biology stack. Same columns, same six roles. The moment both tables were on screen, the contrast jumped out: biology's tower is shorter but brighter (fewer dim cells). Computing's tower is taller but dimmer.

That observation triggered a cascade (contrast → question → hypothesis) faster than I could articulate it. My visual cortex did the diff in parallel. No sequential reading required.

I couldn't have gotten that from prose. Two paragraphs describing the same comparison would carry more propositions per token, but process slower. The table let me see the relationship between rows.

Each format optimizes for a different processor. [Paivio (1986)](https://global.oup.com/academic/product/mental-representations-9780195066661) established independent verbal and visual-spatial systems. Information encoded in both is recalled better than in either alone. [Sweller (1988)](https://doi.org/10.1016/0364-0213(88)90023-7) showed each channel has limited capacity, so distributing across channels increases effective bandwidth.

| Format | Processor | Strength |
|---|---|---|
| Prose | Language (sequential) | Argument |
| Lists | Scanning (parallel) | Filtering, skimming |
| Tables | Visual (spatial) | Comparison |
| Diagrams | Visual (structural) | Relationships |
| Code | Pattern matching | Implementation |
| Equations | Symbolic | Proof |
| Dashboards | Temporal (diff) | Monitoring |

[Vessey (1991)](https://doi.org/10.1111/j.1540-5915.1991.tb00344.x) called this *cognitive fit*: performance is best when the representation matches the task. Spatial tasks are better served by tables; symbolic tasks by text. She reconciled years of contradictory graphs-vs-tables research with one insight: it depends on the task.

Nobody reads a BI report as prose. That's cognitive fit, not laziness.

## Match the format to the processor

Prose is the densest medium for *complementation*: filling the gap between what the reader knows and what they need to know, one proposition at a time. Sequential attention is the right tool when the reader needs to follow a chain of reasoning.

But the densest *document* uses all the channels. [Mayer (2009)](https://doi.org/10.1017/CBO9780511811678) meta-analyzed the effect: words plus pictures outperform words alone with a median effect size of d = 1.39. The catch: arbitrary mixing hurts. The formats must match the content, and they must be spatially integrated ([Chandler & Sweller, 1991](https://doi.org/10.1080/07370008.1991.9649028)).

For each section, pick the format that matches the attention it demands. Argument in prose. Comparison in tables. Trends in [sparklines](https://en.wikipedia.org/wiki/Sparkline). Don't default to uniform prose when a table would let the reader's visual cortex do the work.

We write for two audiences now: the human who benefits from mixed format, and the model that just wants dense tokens. Multimodal models can process images, but slowly and expensively compared to a human glancing at a table.

This experiment tested prose → prose compression, which is the LLM's perspective. Four decades of cognitive psychology already tested the human perspective.

## Prose as spec

I wrote a [prose spec](https://github.com/kimjune01/union-find-compaction-for-gemini-cli/blob/main/transformation-design.md) for a union-find context compaction system: architecture, data flow, file structure. An LLM implemented it in one shot. Then a [code review](/proof-of-trust) found ten bugs: race conditions, dimension mismatches, corpus contamination on query.

None of them were spec failures. The spec didn't try to pin down function signatures or concurrency guards. It specified the forest; the bugs lived in the trees. A prose spec that tried to nail every interface contract would be worse prose *and* worse than code at the job.

But the spec didn't survive intact either. The code review found bugs, the fixes taught us things, and the spec got rewritten twenty times to match. The implementation wasn't downstream of the prose. It was in dialogue with it. The spec said "zero blocking." The code said "not unless you guard against in-flight merges." The spec absorbed the correction.

[Open Prose](/open-prose) claims the spec outlasts every artifact it produces. What actually happened: the architecture survived, but the spec is only as good as the last implementation that stress-tested it. Code is disposable *after* the spec absorbs what it taught. During development, it's load-bearing. The double loop isn't prose → code. It's prose ↔ code, and the arrow runs both ways.

## The cusp

Format selection is a [Filter](/perception-pipe) decision: which processor should this information route to? Route a comparison to the language processor and you waste sequential attention on work the visual cortex does for free. Route a proof to a diagram and you waste spatial bandwidth on work that needs symbolic manipulation.

When I write with [skills](/double-loop), they automate Filter-level work — cut filler, flag restated points, check the arc. Format matching is the same: reject the wrong medium before the reader has to.

Better Filter creates [Attend](/salience) bandwidth. Every paragraph routed to the right format is attention the reader doesn't spend decoding the wrong one. As Filter improves, the ceiling on what Attend can handle rises with it. One step closer to [general intelligence](/general-intelligence).

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
