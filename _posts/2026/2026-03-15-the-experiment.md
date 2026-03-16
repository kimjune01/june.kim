---
layout: post
title: "The Experiment"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds the consolidation harness described in [Consolidation](/consolidation).*

The [diagnosis](/diagnosis-llm) found the broken cell. Claude Code has a `create-skill` capability: the only procedure that writes procedures. That's Consolidate. The machinery exists. The initiative doesn't. The agent never says "I notice I keep doing this. I should make it a skill."

This post builds the harness that makes it automatic.

## The algorithm

Track which action sequences repeat with user approval across sessions. When a pattern recurs above threshold, condense it into a skill. Score the skill against a mutation. Winner survives. Two iterations to convergence, per the [slop detection result](/slop-detection).

Three agents, three roles:

- **Codex (GPT-5.4)** scores skill variants against the contract. The A/B test.
- **Claude Code** creates and mutates skills. The mutator.
- **Human** approves or rejects consolidated skills. The Attend.

The division matters. Codex scores because it's a different model with different biases. Claude mutates because it wrote the skill in the first place. The human approves because consolidation without Attend is cancer: a procedure that writes procedures without selection pressure produces tumors.

## Ground truth

The test corpus is git history. Every post in the [cognition series](/cognition) went through [three quality gates](/writing-with-claude): `/humanize` strips AI writing tics, `/arc-check` verifies argument structure, `/tighten` compresses without losing voice. The git diff after each pass is ground truth: what the human actually accepted.

The diff is a better teacher than the skill. The skill says "flag em dashes." The diff says "the human cut this em dash and kept that one." The difference is context. Context is what the skill needs to learn.

## Round 1: disposable analogies

Codex read the current `/humanize` skill and the ground truth diff from [Set It and Forget It](/set-it-and-forget-it). It proposed one mutation: add a "disposable analogies" pattern.

The evidence: the human had cut a thermostat analogy ("the same mechanism that keeps a thermostat from oscillating...") and replaced it with three words. "Overshoot, correct, settle." The analogy added length without adding inference. The literal version was clearer.

Both variants ran on a held-out post ([PageLeft](/pageleft-manifesto)). The mutation didn't fire. The test post had no disposable analogies. Same recall, same precision. Current skill won on parsimony.

| Variant | Recall | Precision | Notes |
|---|---|---|---|
| Current | 5/7 | 5/9 | Em dash detection drove 4/5 true positives |
| +Disposable analogies | 5/7 | 5/9 | New pattern didn't fire on held-out post |

The mutation was real. The thermostat analogy was genuinely disposable. But one occurrence doesn't justify a new rule. The pattern goes on the watch list. If it fires on a second post, it earns its place.

## The fixed point operator

A skill that runs repeatedly needs a dampener. Without one, each pass compresses further until the output collapses. "Tighten every paragraph" converges to a single word. "Tighten every paragraph a bit" converges in two passes.

The qualifier "a bit" is a fixed point operator. It dampens the skill to idempotency: the second pass finds almost nothing to cut. This is the convergence mechanism for skill mutation. Mutations that overshoot get corrected by the dampener on the next evaluation. The qualifier is the Filter on the Filter.

## What the experiment proved

The harness works. Codex reads ground truth, proposes a mutation, scores both variants on held-out data. The loop is mechanical. It doesn't require human judgment to run, only human judgment to approve.

But the scoring revealed something the experiment didn't set out to find. The skill's misses aren't pattern failures. "Hardy's partition theory" became "Hardy's theory." "But what if they could?" became "But what if they could be found?" Those are line edits. They require hearing the sentence, not matching a rule.

The skill automates Filter. It rejects what's wrong. Producing what's right requires Attend. That stays with the human. The experiment didn't close the gap between Filter and Attend. It measured it.

## What remains

The next mutation should target precision. Four false positives per post is too many. Rule-of-three and stock-metaphor thresholds fire on legitimate uses. The dampener principle applies: tighten the threshold "a bit" until the false positive rate converges.

The harness is [open](https://github.com/kimjune01/AGI). The ground truth is in the [git history](https://github.com/kimjune01/kimjune01.github.io). The [skills are published](/writing-with-claude). Anyone can run the loop.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
