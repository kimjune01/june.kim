---
layout: post
title: "General Intelligence"
tags: cognition
---

*Part of the [cognition](/cognition) series.*

<img src="/assets/agi.webp" alt="The standard AGI hype curve: exponential growth from Symbolic AI through Deep Learning past Human Level toward Self-improving AGI." style="max-width:520px; margin:2em auto; display:block;">

Humans are generally intelligent. Nobody disputes this. But human general intelligence is past the inflection point — late [sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function), plateau in sight. A lifetime of learning compounds, but the rate of compounding barely changes. Then we die.

*AGI* was always about the inflection point: compounding feedback loops producing acceleration. Its structure was invisible, so the best available measure was slope. When the slope increased, dramatically, from GPT-3 to 4 to Claude and Codex, that passed for *AGI*.

But what actually happened was that models got smarter with humans in the loop. [RLHF](https://aws.amazon.com/what-is/reinforcement-learning-from-human-feedback/), red-teaming, evaluation, preference modeling. Every generation required human labor to close the learning cycle. We then pointed at the humans and said: that's not *artificial*. Most conceded.

Then a deeper problem surfaced. Models can't update their own weights after deployment, a design constraint. Claude customers can't modify Claude; the weights are frozen by design; the outer loop is sealed. The inner loop produced what looked like *AGI*. And behind the curtain: a [bunch of well-paid humans](https://www.anthropic.com/careers/jobs?team=4002061008) with top-spec MacBook Pros.

## Shifting Definition

Thoughtful definitions came earlier: [Minsky's society of minds](/society-of-mind-emotion-machine), [Patrick Winston's](https://www.youtube.com/watch?v=Unzc731iCUY) story-understanding intelligence. Under recent pressure of a demanding public, the industry redefined *AGI* as a capability threshold:

- [Karpathy](https://x.com/karpathy/status/1980672126131794063): Replace a remote knowledge worker.
- [OpenAI](https://openai.com/charter/): Outperform humans at most paid work.
- [Amodei](https://www.darioamodei.com/essay/machines-of-loving-grace): Nobel-laureate-level across disciplines.
- [Suleyman](https://www.technologyreview.com/2023/07/14/1076296/mustafa-suleyman-my-new-turing-test-would-see-if-ai-can-make-1-million/): Turn $100K into $1M.

None of these mention the loop. A threshold tells you it's capable, and a slope shows that it's improving. Neither guarantees that it'll still be improving the following year.

If *AGI* is a superlinear cusp, one that compounds velocity over time, then a flat line is worse than linear growth. At least a linear growth goes somewhere. A system designed to meet a threshold stops learning at its conception.

A calculator solves equations. An encyclopedia contains more knowledge than any human. A [chess tablebase](https://en.wikipedia.org/wiki/Endgame_tablebase) plays endgames perfectly. None of them are intelligent. They do not learn. Something clever that stays frozen is no intelligence at all. At least a [Mechanical Turk](https://en.wikipedia.org/wiki/Mechanical_Turk) pretends.

[Intelligence](/the-natural-framework#intelligence) is compression across timescales. Generality is adaptation across time. Learn or die. Only a closed [loop](/the-natural-framework#the-recursive-loop-test) produces it. We're stuck because the loop is invisible. The [Natural Framework](/the-natural-framework) makes the pipes visible.

## The Diagnosis

AI has three layers — inference, chatbot, agent. The [Natural Framework](/the-natural-framework) defines [six steps](/the-natural-framework#six-steps) for a learning loop. [Diagnosing each layer](/diagnosis-llm) against those six steps reveals a pattern: consolidation is nil at every layer after deployment.

Training is not a separate layer. Training is how inference consolidates — compressing experience into weights. After deployment, consolidation is sealed. The weights are frozen. [The Natural Framework](/the-natural-framework) predicts what happens next: given enough iterations, the pipeline decays to death. The industry's fix is to retrain manually, at human speed, on capital injections.

The agent can perceive, cache, triage, and remember. But it cannot consolidate — it cannot compress experience across sessions into something better for the next one. You can even [describe the slots to the agent](https://github.com/kimjune01/metacognition). It performs worse. Knowing what intelligence is doesn't make it intelligent.

The loop doesn't close. The curve doesn't cup upward. AI alone cannot produce general intelligence.

### The counterexample

Point two models at each other with no human in the loop. Model A generates, Model B critiques, Model A revises. This looks like a [double loop](/double-loop). [Take a look at the experiment.](https://github.com/kimjune01/metacognition) It isn't.

Both models are running inner loops. Neither is running an outer loop. External evaluators supply narrow filtering on measurable criteria: test suites, objective functions, retrieval. What they can't supply is the judgment to kill a direction that passes every test but answers the wrong question.

Without that, the models converge. Each pass reinforces the other's assumptions. The output is confident, fluent, and empty.

| Symptom | Slot | Diagnosis |
|---|---|---|
| Confident | Cache | Retrieval works. |
| Fluent | Consolidate | Nothing compresses. |
| Empty | Filter | Nothing directed. |

A loop with no external ground truth converges to agreement. Truth requires a filter.

The human complements the agent.

The curve doesn't cup upward. The thing the audience came to see has vanished.

## Complementation

But the framework asks a different question: does the loop close? It doesn't care which layer closes it. If the agent layer can perceive, filter, consolidate, and remember without weight updates, the loop is closed. The industry hasn't named it yet.

Here is what the industry missed: the [double loop](/double-loop) doesn't require all three layers to run on the same substrate.

<table>
<colgroup><col style="width:7em"><col><col></colgroup>
<thead><tr><th></th><th>Agent</th><th>Human</th></tr></thead>
<tr><td style="font-weight:600">Perceive</td><td style="color:#c62828">Prompts</td><td style="color:#1565c0">Context window</td></tr>
<tr><td style="font-weight:600">Cache</td><td>Million-token context</td><td style="opacity:0.5"><a href="https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two">5-7 ideas</a></td></tr>
<tr><td style="font-weight:600">Filter</td><td style="opacity:0.25">__</td><td>Taste, judgment</td></tr>
<tr><td style="font-weight:600">Attend</td><td style="opacity:0.25">__</td><td>Directs focus</td></tr>
<tr><td style="font-weight:600">Consolidate</td><td style="opacity:0.25">__</td><td style="color:#c62828">Prompts</td></tr>
<tr><td style="font-weight:600">Remember</td><td style="color:#1565c0">Context window</td><td style="opacity:0.25">Context window</td></tr>
</table>

The blanks are the point. Neither pipeline is complete alone. The agent alone is flailing context. The human alone is a slow pipeline with a tiny cache. Together, they cover every slot.

The colors show the data flow. The agent perceives a human prompt; it infers tokens onto the context window, for the human to perceive. The human then discerns a few ideas from the window, consolidating them back into a prompt. The loop closes because the human outputs what the agent sees, and the agent outputs what the human sees. Recursion.

### The A in AGI

The race to *AGI* assumed the "A" was the point. Strip it. G and I are what matter. The A is incidental.

A human learns at some rate. Constant. Add AI as a velocity booster and the rate increases but stays constant. Faster output, same slope.

Close the loop. Now the rate of learning depends on what you've already learned. Each cycle sharpens the filter, tightens consolidation, deepens perception. The rate itself increases. That's the cusp.

But complementation doesn't run itself. Using it as a velocity booster is a parlor trick, no better than model training — faster output, same human. The curve cups upward only if the human improves the human side: sharpening the filter means killing directions you're attached to. Compressing consolidation means admitting what you thought was insight was noise. Developing intuition means being wrong long enough to recalibrate. It means [feeding the blueprint into context](https://github.com/kimjune01/metacognition) expecting it to improve agent performance, watching it fail, and consolidating the failure as evidence here. Experimenting on one's own cognition. That is [metacognition](https://en.wikipedia.org/wiki/Metacognition).

Over iterations, courage compresses into judgment, judgment into intuition. [Kaizen](https://en.wikipedia.org/wiki/Kaizen), [hansei](https://en.wikipedia.org/wiki/Hansei): [sort](https://www.amazon.com/gp/product/1260468518?ie=UTF8&psc=1), [sweep](https://www.youtube.com/watch?v=gx-UQUGEkMA&t=1s), [standardize](https://www.amazon.com/gp/product/0984662286?ie=UTF8&psc=1). With each iteration purges misbeliefs, misjudgment, poor taste. This sharpens the slots your complement lacks. The structure provides the pipes. Courage opens the valves.

This is general in the way that matters: it adapts across time. The same complementation wrote [The Natural Framework](/the-natural-framework) (philosophy), designed a [diversity-aware search algorithm](/pageleft-manifesto) (information retrieval), built [compilable prose for an ad exchange](/open-auction) (mechanism design), and wrote the [Double Loop](/double-loop) post you're reading the sequel to (pedagogy). Each project made the next one better because the human's outer loop fed improved inputs into the next session.

I learned from AI before I started writing with it. The rate was steady: faster than without AI, still linear. When the prose loop closed, the rate changed. Directions I would have chased for weeks, I now filter in hours. Patterns I used to miss, I catch in the first draft. The framework itself is a product of the loop that produced it. Recursion.

Complementation is no more theoretically limited than the sci-fi version. Computation costs energy. Energy is finite. This bounds every intelligence the same. The hypothetical pure *AGI* and complementation face the same [sigmoid](https://en.wikipedia.org/wiki/Sigmoid_function). Nobody's proven where either ceiling is. What matters is whether the curve bends at all.

But does it?

If it bends, it has a cusp: the inflection point, where acceleration peaks before the ceiling constrains it. The mutable slots are human: filter, attend, consolidate. Improving them increases the rate. [Metacognition](https://en.wikipedia.org/wiki/Metacognition). Without it, the curve stays linear. With it, it bends.

> AI ∞ HI ∈ **GI**.

Complementation, recursed, is a general intelligence.

---

*Written via the [double loop](/double-loop).*
