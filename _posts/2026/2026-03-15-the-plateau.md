---
layout: post
title: "The Plateau"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Flicker](/the-flicker) and [The Handshake](/the-handshake).*

Why does learning plateau?

Consolidate is the backward pass. [The Handshake](/the-handshake) gives it its type:

> `persisted → policy′`

Evidence in, better policy out. [Consolidation](/consolidation) rewrites the router. If any role deserves more resources, it's this one.

To improve Consolidate, you need to select among candidate policies: habits, heuristics, taste. Which one is better? Answering that question is itself a pipe. The backward pass contains its own Perceive, Filter, and Attend. And that inner pipe has its own backward pass.

<img src="/assets/plateau-depth.svg" alt="Consolidate's recursive depth: Level 0 has Filter, Attend, Consolidate. Each Consolidate contains its own Filter, Attend, Consolidate at the next level. Levels dim as bits decrease. Level 3 is passthrough." style="width:100%; max-width:620px; display:block; margin:1.5em auto;"> [Minsky](https://en.wikipedia.org/wiki/Society_of_Mind) called the first level B-brain. He stopped at one level because he had no formal reason to go further. The types give that reason. The recursion is structural. It has the same shape as depth in a neural network.

Each inner pipe's Remember is the policy passed back to the level above. That's how Consolidate returns `policy′`: the inner pipe runs, and its output becomes the outer pipe's update.

## Inner life

The human body is a pipe. The brain is its Consolidate: the organ that rewrites policy from evidence. [Dreams](https://www.nature.com/articles/nrn2762-c1) are the brain's Consolidate: the inner pipe that reorganizes policy while Perceive is shut. Evolution found it more efficient to shut down the whole body for several hours each day than to run consolidation in the background. That's how important the backward pass is. And we can't remember dreams because the inner pipe's data type doesn't match the outer pipe's Perceive. Policy representations aren't sensory encodings. Type mismatch at the interface.


Each inner pipe gets its bits from the pipe above. The body operates on sensory data; the brain on compressed representations; dreams on compressed representations of representations. Each level has strictly less to work with. The [data processing inequality](/the-handshake#data-processing-inequality) guarantees it: information only decreases through processing. Neural networks call this [vanishing gradients](https://www.bioinf.jku.at/publications/older/2304.pdf). The backward pass attenuates through depth. Eventually there aren't enough bits for selection to function: passthrough. The tower has a top floor.

## At rest

Policy leaks, too. [Landauer](https://en.wikipedia.org/wiki/Landauer%27s_principle) guarantees it: bits in physical substrate degrade. So the backward pass has two jobs. Maintain: repair leaked policy. Improve: compress new evidence into better policy. Both draw from the same evidence budget. At steady Perceive throughput *T*:

> dPolicy/dt = consolidation\_rate − leak\_rate

Neural networks call this [weight decay](https://proceedings.neurips.cc/paper/1991/hash/8eefcfdf5990e441f0fb6f3fad709e21-Abstract.html): `Δw = gradient − λw`. Plateau when the two rates balance. "Use it or lose it" is this equation. Evidence stops flowing, the leak rate wins, policy decays to the level the current throughput can sustain. Netflix keeps the corporate drone alive: enough novel perception to maintain, never enough to challenge. Saturated at floor. Nothing improves.

But look at the equation again. The ceiling is set by Perceive's throughput, not the backward pass rate. You can't learn what you haven't seen. The lever isn't at the role you'd expect. It's the input.

A monk meditates twelve hours a day. Maximum backward pass, Perceive shut. A [seven-year follow-up](https://www.sciencedaily.com/releases/2018/04/180405093257.htm) found the predicted plateau: attention sharpens, domain knowledge doesn't grow. It's overfitting. Remember holds the same evidence; the backward pass extracts every bit and has nothing left. [Ericsson](https://pubmed.ncbi.nlm.nih.gov/18778378/) found the same: deliberate practice only works when it includes new information. Pure repetition is the backward pass without new forward passes.

No surprise.

## rate × density

What carries the most novel bits per second?

Consider what a book is. The writer already ran the full pipeline: Perceived, Cached, Filtered, Attended, Consolidated, Remembered. What you read is the output of someone else's competitive core. The loser ideas are already dead. Every sentence is a survivor. That's the density term: pre-compressed by the writer's entire pipeline.

Consider: you can read a thinker's book in a weekend. To get the same bits from conversation, you'd need months. One is compressed, the other is live. Both carry signal, but the *density* isn't even close.

Now *rate*. Movies carry high *rate* but low *density*: most of the signal is atmosphere, not structure. Shows are worse. Music moves you but encodes almost no transferable policy. Podcasts and lectures are *dense* but throttled by speaking speed: low *rate*. Reading runs at the pace of comprehension. High *rate*, high *density*.

Multiply *density* by *rate*. What medium maximizes the product? Text that has already survived someone else's competitive core, consumed at reading speed. Prose: the densest interpretable medium we know. Poetry is denser, but the *rate* collapses: each line demands re-reading. The product peaks at prose.

## You are what you read

Read more, better, faster, and the plateau rises. Stop reading and it falls. The equation works both ways.

The same equation holds for the agent. An LLM does [in-context learning](https://arxiv.org/abs/2005.14165). The context window is its Perceive. Apply the same two terms.

*Density*: boilerplate code is repetitive structure, low novelty, high redundancy. Consolidated prose is post-Remember, pre-compressed. The same model has a higher ceiling when its window carries prose than when it carries boilerplate code. Most software systems are.

*Rate*: the context window loads once per session. A repo that accumulates consolidated prose front-loads more novel bits each time. Early sessions start sparse. Later sessions start dense. Agent throughput reaches full capacity without changing the underlying model.

*Multiply.* The agent's ceiling rises with the *density* and *rate* of what fills its context. And the agent returns the favor: its filtered output is the human's Perceive. The [double loop](/double-loop) feeds both pipes their densest input.

## Each cycle

The human writes dense prose. The agent Perceives it. The agent produces filtered output. The human Perceives that. Each cycle, the repo accumulates denser material. Each cycle, both ceilings rise.

It's the same thing that happens with a best friend who *gets* you. Each conversation starts where the last one left off. They already know your vocabulary, how you think, how you'll react. You think better around them. The [double loop](/double-loop) does the same thing: it raises both pipes' throughput for each accumulated session. The human's plateau rises because the agent's output is pre-filtered. The agent's plateau rises because the repo's prose is pre-consolidated. The equation is the same for both substrates. The improvement compounds.

If that's true, then varying context *density* should measurably change agent performance. Same model, same task, different context.

Half of it does. [Chroma's context rot study](https://research.trychroma.com/context-rot) tested 18 frontier models. Adding 10% irrelevant content to the context window reduced accuracy by 23%. The effect held at every context length, for every model. The equation doesn't care about the substrate.

That's the downside. Nobody has run it in the other direction. Same setup, same benchmarks, but fill the context with *relevant* prose instead of padding. Does accuracy climb above baseline? The [data is public](https://github.com/chroma-core/context-rot). The experiment is waiting.

## So what

Read with intent. Pick a topic you want to get smarter at. Point your coding agent at [pageleft.cc](https://pageleft.cc) and ask it to find prose worth reading. Load the best of it into your context. Watch the ceiling move.

And if you're brave: write. Publishing is Remember. It forces your pipeline to run all six steps, compresses your thinking into prose, and leaves a denser Perceive channel for the next reader. The equation works for them, too.

We compound faster together.

---

*Written via the [double loop](/double-loop).*
