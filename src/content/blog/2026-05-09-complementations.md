---
variant: post-medium
title: "Complementations"
tags: cognition
---

People point their AI at open source repos and contribute. PRs with passing CI, repos they don't own, multiple projects, no compensation. Some get merged. Some get "DO NOT SUBMIT AI SLOP." They keep going.

I found them in the graveyard. GitHub PR comments are searchable. The rejection language is consistent: "AI slop", "do not use AI", "I'm not reading anything written by AI." Behind each rejection, a diff that passed CI. Code correct. Prose wrong.

But the graveyard is just one source. The signal is readable without looking at rejections:

1. PRs with passing CI on repos they don't own
2. Contributions across multiple projects
3. No visible compensation — no bounty, no contract, no employer mandate
4. Depth: investigations, bug finds, performance work

Excess attention, tooling good enough to give away, interests adjacent to the repos they contribute to. Early.

One of them. [14 PRs to tinygrad in 48 hours](/sweep-and-triage#case-study-tinygrad), one merged, the rest more instructive than a year of reading. Built a [pipeline](https://github.com/kimjune01/sweep) that finds issues, investigates them, shapes PRs to match the review culture, ships one at a time. Runs while I sleep.

## What complementation means

Neither pipeline is complete alone. The AI perceives, caches, triages, and transmits; the human filters, attends, and consolidates. Together they [cover every slot](/general-intelligence#complementation). Each cycle sharpens the next. The curve cups upward.

These people figured that out by shipping PRs and getting rejected and shipping more. The proof of work is the contribution history. The diffs.

## The index

A reading list. People who use AI openly, contribute to open source, and leave a public trail. Proof of work: PRs with passing CI. No self-nomination. No leaderboard. No score.

If you're on this list and want off, open an issue or email me. If you should be on it, the diffs will speak for themselves.

| Who | Writes at | About |
|---|---|---|
| [karlb](https://github.com/karlb) | [karl.berlin](https://www.karl.berlin) | LLMs + simpler software |
| [nooscraft](https://github.com/nooscraft) | [noos.blog](https://noos.blog) | AI-assisted PRs, agent news |
| [Puppo](https://github.com/Puppo) | [delpuppo.net](https://blog.delpuppo.net) | local vs cloud AI |
| [pdurlej](https://github.com/pdurlej) | [pdurlej.pl](https://pdurlej.pl) | AI workflows, prompt engineering |
| [imran-siddique](https://github.com/imran-siddique) | [imransiddique.com](https://imransiddique.com) | agentic architecture, safety |
| [cakebaker](https://github.com/cakebaker) | [danielhofstetter.com](https://danielhofstetter.com) | Rust coreutils, reads 500+ books |
| [nielskaspers](https://github.com/nielskaspers) | [nielskaspers.com](https://nielskaspers.com) | AI-powered dev, Claude skills |
| [kimjune01](https://github.com/kimjune01) | [june.kim](https://june.kim) | cognition, contribution pipeline |

## How the crawler works

The first crawler searched for rejection language — "AI slop", "do not use AI" — in PR comments. It found drama, not the population. 62% of candidates failed manual audit: employer repos, own projects, no real external footprint.

The second crawler starts from repos, not people. It pulls recent merged PRs from projects where external contributors can land real fixes — [astral-sh/uv](https://github.com/astral-sh/uv), [servo](https://github.com/servo/servo), [fastify](https://github.com/fastify/fastify), [triton-lang](https://github.com/triton-lang/triton), and two dozen others. For each PR, it scores depth: a regression test or benchmark scores higher than a README edit. A root-cause explanation scores higher than a dependency bump. Authors are aggregated across repos. Anyone contributing to only their own repos or their employer's repos is excluded.

AI-assistance evidence — commit footers like "Generated with Claude Code", agent config files in repos, blog posts about AI workflows — is noted but not required. Many strong contributors don't disclose their tools.

A second pass searches for maintainer praise instead of rejection: "good catch," "nice investigation," "thanks for the reproduction." These find competent outsiders the rejection search misses entirely.

The filter: merged PRs on repos they don't own or work at, across multiple projects or deep in one, no visible compensation, real technical depth. The [crawler](https://github.com/kimjune01/june.kim/blob/master/scripts/complementations-crawler-v2.sh) and [data](https://github.com/kimjune01/june.kim/blob/master/data/complementations.jsonl) are public.
