---
layout: post
title: "The Plateau"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Flicker](/the-flicker) and [The Handshake](/the-handshake).*

Why does learning plateau?

Consolidate is the step that determines whether you get smarter. [The Handshake](/the-handshake) gives it its type:

> `(policy, [ranked]) → policy′`

A function and evidence in, a better function out. [Consolidation](/consolidation) rewrites the router. If any step deserves more resources, it's this one.

To improve Consolidate, you need to select among candidate policies: habits, heuristics, taste. Which one is better? Answering that question is itself a pipe. Consolidate contains its own Perceive, Filter, and Attend. And that inner pipe has its own Consolidate.

<img src="/assets/plateau-depth.svg" alt="Consolidate's recursive depth: Level 0 has Filter, Attend, Consolidate. Each Consolidate contains its own Filter, Attend, Consolidate at the next level. Levels dim as bits decrease. Level 3 is passthrough." style="width:100%; max-width:620px; display:block; margin:1.5em auto;"> Minsky called the first level B-brain. He stopped at one level because he had no formal reason to go further. The types give that reason. The recursion is structural.

Each inner pipe's Remember is the policy passed back to the level above. That's how Consolidate returns `policy′`: the inner pipe runs, and its output becomes the outer pipe's update.

## Inner life

The human body is a pipe. The brain is its Consolidate: the organ that rewrites policy from evidence. [Dreams](https://www.nature.com/articles/nrn2762-c1) are the brain's Consolidate: the inner pipe that reorganizes policy while Perceive is shut. Evolution found it more efficient to shut down the whole body for several hours each day than to run consolidation in the background. That's how important this step is. And we can't remember dreams because the inner pipe's data type doesn't match the outer pipe's Perceive. Policy representations aren't sensory encodings. Type mismatch at the interface.


Each inner pipe gets its bits from the pipe above. The body operates on sensory data; the brain on compressed representations; dreams on compressed representations of representations. Each level has strictly less to work with. The [data processing inequality](/the-handshake#data-processing-inequality) guarantees it: information only decreases through processing. Eventually there aren't enough bits for selection to function: passthrough. The tower has a top floor, and Consolidate is a slow dial with a hard ceiling.

## At rest

Policy leaks, too. Landauer guarantees it: bits in physical substrate degrade. So Consolidate has two jobs. Maintain: repair leaked policy. Improve: compress new evidence into better policy. Both draw from the same evidence budget. At steady Perceive throughput *T*:

> dPolicy/dt = consolidation\_rate − leak\_rate

Plateau when the two rates balance. "Use it or lose it" is this equation. Evidence stops flowing, the leak rate wins, policy decays to the level the current throughput can sustain. Netflix keeps the corporate drone alive: enough novel perception to maintain, never enough to challenge. Saturated at floor. Nothing improves.

But look at the equation again. The ceiling is set by Perceive's throughput, not Consolidate's quality. The lever isn't the step you'd expect. It's the input.

A monk meditates twelve hours a day. Maximum Consolidate: the inner pipe running at full power, Perceive shut, all resources dedicated to policy refinement. The framework predicts a plateau, not transcendence. A [seven-year follow-up](https://www.sciencedaily.com/releases/2018/04/180405093257.htm) found exactly that: meditation benefits plateau even in the most dedicated practitioners. Attention sharpens, but domain knowledge doesn't grow. Novel evidence stopped arriving. The dial is cranked, but the ceiling is set by what comes in, not by how hard you think. [Ericsson](https://pubmed.ncbi.nlm.nih.gov/18778378/) found the same for deliberate practice: it only works when it includes new information and external feedback. Pure repetition is consolidation without Perceive.

No surprise.

## rate × density

Prose is post-Remember. The writer already ran the full pipeline: Perceived, Cached, Filtered, Attended, Consolidated, Remembered. What you read is the output of someone else's competitive core. The losers are already dead. Every sentence is a survivor. Prose maximizes both terms of the ceiling. *Novel*: only survivors, pre-compressed by the writer's pipeline. *Per unit time*: language encodes more structure per second than any sensory channel. Reading is faster than listening, denser than watching. The densest interpretable medium because the math demands it.

Read more, better, faster, and the plateau rises. Stop reading and it falls. The equation works both ways.

The same holds for the agent. An LLM does in-context learning; the context window is its Perceive. Dense prose in context means high novelty per token. Boilerplate code is repetitive structure, low novelty, high redundancy. The same model thinks sharper when its window carries prose than when it carries boilerplate. A repo full of consolidated prose is a persistent Perceive channel: every session starts with prior loops already loaded. Early sessions fumble. Later sessions are sharp from the first message. The repo learned. The agent returns the favor — its filtered output is the human's Perceive. The [double loop](/double-loop) feeds both pipes their densest input.

The digital variant swaps the bottleneck, not the equation. Model weights don't leak. But consolidation rate is a function of *novelty*, not volume. Another pass over the same data is redundant evidence. The model plateaus when Perceive runs out of new bits. Same equation, different term goes to zero. Same plateau, regardless of substrate.

If the equation holds for neurons and for weights, then varying context density should measurably change agent performance. That's a prediction.

---

*Written via the [double loop](/double-loop).*
