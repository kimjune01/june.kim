---
layout: post
title: "Open Prose"
tags: cognition pageleft
---

*Part of the [cognition](/cognition) series.*

The cognition series built a pipeline: [perceive](/caret-recorder), [structure](/moments), [forget](/learn-to-forget), [attend](/salience). The pageleft series built the distribution layer: [index by meaning](/pageleft), [rank by peer value](/canon), [license irrevocably](/free-as-in-fire). Both series ask the same question: what form of knowledge stays legible when the systems underneath change?

Prose. Specifically: prose that a human can read without specialized tools, that a machine can compile across framework generations, and that anyone can legally fork without negotiation. That's the definition of durable I'm using. Everything below is the argument for why prose is the only artifact that satisfies all three.

## 30 out of 31

[Slop detection](/slop-detection) proved that a SOTA model can structurally review prose. Not for style. For structure: argument dependency chains, falsifiable claim density, specificity ratio, interchangeability. The experiment went 30/31 before an adversary specifically trained against the rubric pushed the classifier below its confidence threshold.

If prose is reviewable, it gets the same workflow: draft, review, revise, merge. The quality gates already exist. A [humanizer](/writing-with-claude) strips generation artifacts. An arc checker verifies argument structure. A slop detector catches structural fingerprints. Three automated passes before a human reads the first word. Code review for text, running today.

## Prose compiles to code

[Vibelogging](/vibelogging) showed that blog posts are build instructions. The entire vector-space series compiled to a [working ad exchange](https://github.com/kimjune01/vectorspace-adserver) in a weekend: auction math, privacy architecture, billing model, publisher UX, go-to-market. The prose was the spec. The code was the artifact.

Papers lock knowledge in PDFs behind paywalls. You can cite them but you can't compile them. Model weights are opaque: you can run inference but you can't read what they encode, fork their reasoning, or rebuild from them. Code rots. Dependencies break and APIs deprecate. Prose survives all three failure modes. The vector-space blog posts should still be readable in ten years. Point the next decade's coding agent at them and the code rebuilds. The spec outlasts the artifact it produces.

## Prose generates itself from attention

The cognition series is the spec for a pipeline that turns screen time into writing. [Caret Recorder](/caret-recorder) captures what's on screen through accessibility-tree parsing. [Moments](/moments) structures perception into semantic units. [Learn to Forget](/learn-to-forget) argued that the missing primitive is competitive inhibition: a race where winners suppress losers, not a priority queue. [Salience](/salience) implements the competition as a cache. Memory consolidation is commodity; the hard problem was deciding what to forget.

The human reads. The pipeline writes. The quality gates review. Then the human approves or rejects, and the loop closes. The bottleneck was never ideas. It was the transcription cost between noticing something and writing about it.

That pipeline is private. It runs on one person's screen, filters one person's perception, drafts from one person's attention. The output is prose. The moment that prose is published under CC BY-SA and indexed by [PageLeft](/pageleft), it stops being private. One person's cognition becomes a commons artifact: linkable, citable, compilable, findable by anyone else's pipeline. The license is what converts private cognition output into public infrastructure.

## A third category

Academia writes papers that sit behind paywalls, get cited but not built, and die when the grant runs out. The incentive is publication count. A paper that nobody implements is still a successful paper, and that's the system working as designed.

Open source starts with code. The README explains what the code does. The docs explain how to use it. The writing serves the artifact.

Open prose starts with ideas. The writing *is* the artifact. The code serves the writing. A blog post that specifies an architecture precisely enough for a coding agent to implement it one-shot is a different object from a paper or a README. Readable by a stranger, compilable by a machine, reviewable by a model, licensed so anyone can build on it. Papers inform. Code executes. Open prose does both.

## Copyleft makes the loop self-sustaining

CC BY-SA on prose. AGPL on code. The license turns a personal blog into infrastructure. [Free as in Fire](/free-as-in-fire) made the commitment irrevocable. [PageLeft](/pageleft) indexes it by meaning. [Canon](/canon) tracks what the index contains and what it's missing.

The threat model is straightforward. A company scrapes your blog to train a model and gives nothing back. Someone forks your architecture and closes the code. A platform shuts down and your posts vanish. Share-alike prevents enclosure. The license survives the platform. Semantic indexing means discovery doesn't depend on any single host.

Someone else's cognition pipeline finds this post through PageLeft. They build on it. Their derivative carries the same license forward. The ideas propagate without the original author maintaining anything. No server to keep running, no dependency to update. The prose just sits there, compilable, forkable, searchable. The copyleft obligation ensures every fork stays open.

Perception produces moments. Competition selects what matters, and the survivors become prose. The prose compiles to code. Copyleft keeps it open. Semantic indexing makes it findable. The next person's pipeline discovers it and the loop runs again. Each step requires the one before it.

Two series. One category. Open prose.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
