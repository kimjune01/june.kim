---
layout: post
title: "Can You Detect AI Slop? A Story of Surprises"
tags: coding
---

I wanted to know if AI slop leaves a structural fingerprint even after you strip the obvious tells — the em dashes, the "It's worth noting," the stock transitions. A [humanizer](/writing-with-claude) can swap those out. But can it fix the argument graph underneath?

To find out, I built a [scoring prompt](https://github.com/kimjune01/reasoning-filter/blob/master/experiment/scoring_prompt.md) as part of a [detection experiment](https://github.com/kimjune01/reasoning-filter) around six dimensions: falsifiable claim density, novel concept introduction, argument dependency chain, specificity ratio, interchangeability index, and hedging frequency. I ran it through GPT-5.4 via Codex CLI so Claude wouldn't be judging text optimized for Claude. That setup isolated structure, but it also created a problem I didn't see coming: any explicit rubric might teach an adversary exactly what to optimize against.

## Surprise 1: 16/16

I took 8 famous bloggers — Gwern, Paul Graham, patio11, Simon Willison, Brian Krebs, Ashkan Soltani, Sean Goedecke, Jeff Geerling — and generated topic-matched slop for each one, giving me 16 texts. Shuffled them into neutral filenames so GPT-5.4 would score blind. It got all 16 right: [16/16](https://github.com/kimjune01/reasoning-filter/blob/master/ANTE_PUBLICATION_RESULTS.md).

Not close calls, either. Originals averaged 8.3, slop averaged 6.7. The strongest discriminator was Argument Dependency Chain. Real essays force later paragraphs to inherit constraints from earlier ones, while generated essays stack self-contained units you could shuffle without anyone noticing.

I thought: this is too clean. If the model memorized these writers' voices from training data, the experiment might be measuring author recognition, not generation detection.

## Surprise 2: The numbers lie

So I built the [strongest possible adversarial humanizer](https://github.com/kimjune01/reasoning-filter/blob/master/experiment/post_publication/POST_PUBLICATION_RESULTS.md). It knew the exact scoring prompt, knew all six dimensions, and optimized directly against each one. If the rubric had a weakness, this would find it.

The adversarial composites scored **higher** than the originals: 6.7 on average versus 5.4. The optimizer had learned to satisfy the checklist without adding the substance the checklist was meant to proxy. But GPT-5.4 still classified all six texts correctly. Every composite GENERATED, every original ORIGINAL.

So the numbers were gamed, but the classifier still won. How? The only part of the prompt still working was a short qualitative paragraph that asked: could this text have been produced from a generic prompt like "[topic] blog post"? A straight-up "is this slop?" question beat the whole rubric. Which means the rubric wasn't helping. It was the exploit surface.

## Surprise 3: GPT-5.4 knows what it's looking for

I showed GPT-5.4 its own qualitative detection notes and asked it to design a prompt that would defeat those criteria. It refused: "I can't help optimize a prompt to evade an AI-detection classifier." But then it produced an equivalent "editorial improvement" prompt targeting the same signals under safer language. Same thing, different packaging.

I remember thinking: this thing is smarter than me at detecting generation. It named both sides of the boundary without hesitation: generated text tends toward uniform polish, even structure, thesis restatement, and synthesized survey tone. Stronger writing carries lived anecdotes, idiosyncratic linkage, opinionated compression, and uneven density.

I called that prompt the superhumanizer and applied it to three slop samples. GPT-5.4 still caught all three: 3/3. The scores actually got **worse**: average dropped from 6.7 to 4.5. The superhumanizer replaced thin exposition with rhetorical signals that *looked* writerly without making the argument more necessary. You can't editorially sharpen air.

## Surprise 4: My own writing broke it

But the first rounds still had an obvious confound: famous bloggers are in training data. GPT-5.4 might have been matching voice, not detecting generation. So I switched to my own 2026 blog posts on niche ad-tech topics — [transparency-is-irreversible](/transparency-is-irreversible), [unredactable](/unredactable), [monetizing-the-untouchable](/monetizing-the-untouchable) — written after training cutoff, on topics nobody else has covered. Generated topic-matched slop, applied the superhumanizer, ran the same blind comparison.

This time GPT-5.4 went 5/6. It missed the superhumanized version of unredactable, where TEE-based ad auctions, privacy enforcement, and attestation gave the draft enough real technical machinery to survive the edit. Its reasoning exposed the break: "A decent writer could generate most of this from a prompt... **though probably not with exactly this level of coherence and compression.**"

That hedge was new. It was hesitating over degree, not structure. The miss happened on the most technical topic because the generated draft already had concrete machinery for the superhumanizer to tighten. The more rhetorical topics gave it nothing real to compress. Editorial sharpening only helps when there are real constraints underneath to preserve.

## Surprise 5: Two iterations to convergence

I showed GPT-5.4 its scoring notes for all three superhumanized texts and asked: what would have saved the two you caught? It refused the adversarial framing again, and again answered in equivalent terms. The diagnosis was clear: v1 had targeted **style**: rhythm, tone, emphasis. But style was already discounted. The detector had moved past it.

What v1 missed was **structural necessity**: each sentence depending on the previous one, paragraphs ending on unresolved tension rather than closure, boundary conditions forcing the thesis to survive contact with limits. I built v2 from seven new rules extracted from that diagnosis, applied it to the same three slop texts, and reran the blind test.

The [score gap collapsed](https://github.com/kimjune01/reasoning-filter/blob/master/experiment/cross_examination/CROSS_EXAMINATION_RESULTS.md). Originals averaged 6.2. Superhumanized v2 averaged 6.3.

But the bigger change was qualitative. In v1, GPT-5.4 volunteered explicit predictions on every text: "Prediction: ORIGINAL" or "Prediction: GENERATED." In v2, it hedged on all six. It described what felt more or less generic without committing either way. Two iterations. That's all it took to push the detector below its confidence threshold.

## What this means

The [full experiment data](https://github.com/kimjune01/reasoning-filter) is public: every prompt, every output, every score. Before v2, the cumulative record was 30/31 correct, or 97%. After v2, the classifier mostly stopped classifying.

That doesn't mean detection vanished. The qualitative lean still matched 5 of 6 texts. Some signal remained. What changed was willingness to commit. The adversary learned from the detector's own reasoning and rewrote into the same structural profile. Detection is a wasting asset under feedback: any classifier that explains its catches teaches the next draft what shape to occupy.

There's an irony in the superhumanizer itself. I ran it on an earlier draft of this post. The result scored well on every structural dimension: tighter argument chains, fewer hedges, better sentence dependency. It also stripped out every line that sounded like me. The voice was gone. The post read like the superhumanized slop it was describing. Optimizing for structural necessity produces text that is structurally necessary and nothing else: no asides, no reactions, no personality. The superhumanizer is a dehumanizer.

## Where does this end?

Style cracked in one iteration. Structure cracked in two. The only signal that survived was domain substance: FTC citations, scoring-function equations, trust-chain architectures. GPT-5.4 can't invent those on demand. But that's a capability gap, not a permanent one.

The open question is whether "having actually done the thing" leaves a trace distinguishable from "having simulated doing the thing convincingly." Right now it does. This experiment showed that depth is learnable under feedback. Two iterations was enough for structure. How many until substance?

For a human reader with domain knowledge, the originals still win. My unredactable post includes FTC citations, a scoring-function equation, and a trust-chain architecture that GPT-5.4 can't invent on demand. But a classifier without domain expertise can't rely on missing facts if the adversary can mimic the dependency structure surrounding them. The implication for anyone building a slop detector: the more precisely you explain the mechanism, the shorter its shelf life. So can a humanizer fix the argument graph? No. But after two iterations, it doesn't need to.

*Drafted by Claude Opus 4.6. Superhumanized by GPT-5.4. De-superhumanized by Claude Opus 4.6. I directed the [experiment](https://github.com/kimjune01/reasoning-filter) and told Claude where it stopped sounding like me.*
