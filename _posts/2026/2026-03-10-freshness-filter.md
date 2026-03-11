---
layout: post
title: "Freshness Filter"
tags: coding
---

I just [built and broke a series of AI slop detectors](/slop-detection). Rubrics, adversarial humanizers, structural scoring. Every formalized detector got gamed. The thing that worked was five lines:

> What percentage of this text's intellectual substance could you reconstruct from your training data alone, given only the topic and a request to write about it?

That's it. Feed it any text, get back a number. In my [tests](https://github.com/kimjune01/reasoning-filter), original writing averaged 74% reconstructable. Superhumanized AI slop averaged 84%. Perfect separation across every pairwise comparison.

## Why this works

AI-generated text is corpus recombination by definition. The model can only output what it's seen, rearranged. Original writing contains residual: ideas, connections, mechanisms, or facts that aren't in the training data. The model knows what it knows. Ask it directly and it tells you.

It's a substance detector. It doesn't care about em dashes, hedge phrases, or sentence structure. A well-written email full of 2016 ideas would score 95%. A rough draft with a genuinely new mechanism would score 60%. The filter catches both slop and unoriginality, which in an inbox are the same problem.

## Why simpler is better

I tested three versions of this prompt:

1. **Full prompt** (4 sections: novel passages, recombined passages, reconstructability %, novelty confidence). Gap: 5.3 points.
2. **Elaborate prompt** (core reconstruction step, residual analysis, ideational vs compositional scoring). Gap: 2.3 points.
3. **Bare prompt** (one question, one number). Gap: 10.0 points.

The elaborate prompt was designed by GPT-5.4 to improve on the full prompt. It made things worse. The reconstruction step anchored the model on its own output, so everything looked equally novel relative to what it had just generated.

This is the same pattern that killed the rubric in the [detection experiment](/slop-detection): the more precisely you formalize the detection logic, the worse it performs. The bare question lets the model use its intuition. The structured prompt forces it through a procedure that flattens the signal.

## How to use it

**Email.** Score incoming messages. Anything above 85% is either AI-generated or saying nothing you couldn't find yourself. If you use Claude Code with the Gmail MCP server, you can ask it to score your unread mail in one shot. Set it up as a cron job and you have a freshness filter running on autopilot.

**Content curation.** Rank by reconstructability. A piece at 65% contains ideas the model hasn't seen. A piece at 90% is a summary of things you could have prompted for.

**Your own writing.** Run your drafts through it. Above 80% means you haven't said anything new yet. The number won't tell you what's missing, but it'll tell you that something is.

## The catch

This filter has a shelf life. If I tell you how it works, and you tell your AI to produce text that scores low on reconstructability, we're back in the [adversarial loop](/slop-detection#surprise-5-two-iterations-to-convergence). Two iterations to convergence.

But there's a difference. The structural superhumanizer could fake argument dependency because dependency is a property of the text. Reconstructability is a property of the model's training data. The model can't inject ideas it hasn't seen. It can make recombination *look* novel, but it can't add information it doesn't have.

That gap will close as models get better. Freshness has a shelf life too.

*Based on experiments in [reasoning-filter](https://github.com/kimjune01/reasoning-filter). Drafted by Claude Opus 4.6. I directed the argument.*
