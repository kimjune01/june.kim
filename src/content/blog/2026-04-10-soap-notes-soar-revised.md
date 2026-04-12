---
variant: post-medium
title: "Revised SOAP Notes: Soar"
tags: cognition, methodology
---

*Correction to my [prior SOAP notes](/soap-notes-soar). Part of the [cognition](/cognition) series.*

I met with [John Laird](https://en.wikipedia.org/wiki/John_E._Laird) on April 9th. I presented my [diagnosis](/diagnosis-soar): missing merging in the long-term declarative stores, five dominoes falling from it, three PRs to fix it. He rejected the core premise.

He was right. I was wrong.

## What I got wrong

My prior diagnosis read [Derbinsky & Laird (2013)](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563) and ran the inference backwards. Their paper builds forgetting for working memory and procedural memory. The safety requirement R4 says: only forget WMEs that have a backup in semantic memory. Smem is the stable backing store that makes WM forgetting safe.

I read R4 as a bottleneck. If smem were richer, auto-populated from episodic memory, then R4 would cover more WMEs, more could be forgotten, and the whole system would scale. I built a domino chain from that reading: narrow perception → throttled input → bounded forgetting → unbounded episodic growth. Three PRs followed.

But D&L 2013 never makes that argument. They treat R4's scope as adequate. They don't call for smem or epmem eviction. The discussion doesn't mention it. The future work doesn't mention it. The "scaling wall" was my extrapolation, not their finding.

Worse, my mental model was structurally wrong. I imagined a unified graph where episodic edges accumulate into semantic nodes. Laird pointed out that smem and epmem have completely different data structures: smem stores graph structures, epmem stores WM snapshots as deltas. Smem is populated from working memory by deliberate agent action, not derived from epmem. [Figure 6](https://arxiv.org/abs/2205.03854) says it plainly: semantic memory's source of knowledge is "Existence in Working memory."

I treated a safety constraint as a scaling bottleneck. I confused which memory was the problem. WM is the bottleneck, not smem. I prescribed a pipeline between two stores that aren't structurally compatible. Three PRs retired.

## What Laird actually says is missing

Laird's self-assessment in [§10](https://arxiv.org/abs/2205.03854) is clear. Real-time operation: "yes, yes" — with millions of items. Scaling is not the problem. What's missing:

- **Semantic learning** ([§10, item 7](https://arxiv.org/abs/2205.03854)): "there are still types of architectural learning that are missing, such as semantic learning."
- **Bootstrap** ([§10, p.20](https://arxiv.org/abs/2205.03854)): "What I feel is most missing from Soar is its ability to 'bootstrap' itself up from the architecture and a set of innate knowledge into being a fully capable agent across a breadth of tasks."
- **Stochastic-substate chunking** ([§4, p.10](https://arxiv.org/abs/2205.03854)): planned but unshipped after four years.

These are gaps by Laird's own accounting. I identified the first two, then attached them to the wrong architectural intervention.

## What we agreed on

We did not agree on my architectural diagnosis. We did agree on the missing instrument: evals.

My PRs had no empirical claim attached. They didn't say which agents should improve, which workloads should scale, or what regression would count against the proposal. An eval harness would have forced my proposals into predictions: after enriching smem, agents should retain task performance while reducing working-memory load or decision latency on specified workloads. I had no such result. Without that, the PRs were architecture-shaped guesses.

## The meta-diagnosis

The broken loop isn't inside Soar's memory architecture. It's in the project's contributor-learning loop — what I'd call the organizational [Consolidate](/natural-framework): the process by which proposed changes become predictions, measurements, and accepted improvements.

Soar is a mature C++ system with tightly coupled modules. There is no benchmark suite for cognitive metrics, no eval harness for agent-level behavior, no contributor guidelines that map proposed changes to testable claims. Without that signal, the only alternative is meetings — and nothing is cheaper than sample data that runs at compute time. Experimental branches start and don't land. PRs open and close. Mechanisms remain plausible instead of becoming measured progress.

The next useful contribution is not another memory mechanism. It is a way to tell whether a memory mechanism helped.

## A transfer eval

So I built one. The harness generates random [Blocks World](https://en.wikipedia.org/wiki/Blocks_world) tasks, trains a chunking agent on a set of them, then tests whether the learned chunks transfer to new tasks. Three conditions: trained-transfer (chunks from training), fresh baseline (no prior learning), and no-learning control (chunking disabled).

```
  Seed  Condition             Success   Transfer DCs  Chunks  Transfer Ratio
  ----------------------------------------------------------------------------
     0  trained-transfer      6/6                 18       5          +0.571
     0  fresh-baseline        6/6                 42       -               -
     1  trained-transfer      6/6                 18       4          +0.280
     1  fresh-baseline        6/6                 25       -               -
     2  trained-transfer      6/6                 19       5          +0.424
     2  fresh-baseline        6/6                 33       -               -
     3  trained-transfer      6/6                 28       2          +0.569
     3  fresh-baseline        6/6                 65       -               -
     4  trained-transfer      6/6                 23       4          +0.635
     4  fresh-baseline        6/6                 63       -               -
```

Chunking cuts transfer task decision cycles by 28–64%. The measurement is automatic, deterministic, and runs in seconds. This is the signal my PRs should have been tested against. An architectural change that improves this ratio is earning its place. One that doesn't is an architecture-shaped guess.

The [harness](https://github.com/SoarGroup/Soar) is a Python script wrapping Soar's existing CLI. It generates tasks, runs agents, parses stats, and compares conditions. No new infrastructure required.

---

*Revised SOAP analysis based on [Laird (2022)](https://arxiv.org/abs/2205.03854), [Derbinsky & Laird (2013)](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563), the [Soar source](https://github.com/SoarGroup/Soar), and a meeting with John Laird on 2026-04-09. Written via the [double loop](/double-loop).*
