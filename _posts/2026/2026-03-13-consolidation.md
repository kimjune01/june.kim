---
layout: post
title: "Consolidation"
tags: coding cognition
---

*Part of the [cognition](/cognition) series.*

[Salience](/salience) solved retrieval. The cache returns max-volume-k moments when coordination queries. But it left a loose thread: "the store may compact old clusters or drop stale moments, but that's housekeeping, not policy." [Perception Pipe](/perception-pipe) left another: "the hippocampus replays salient experiences during sleep, and the ones that survive replay get written to cortex as long-term memory."

Housekeeping that runs offline, processes winners from past competitions, and writes the survivors to a different store. That's not housekeeping. That's the fifth layer.

## What keeps winning

Run the salience cache for a day. Some moments win once and never surface again. Others keep appearing: the same deployment pattern, the same error class, the same architectural constraint. Each retrieval is independent. The DPP doesn't know that it selected similar moments yesterday. But the pattern is real.

Three moments from different sessions: "AGPL requires derivative works to share source." "Copyleft is irrevocable." "CC BY-SA derivatives inherit the obligation." Each won its own competition against different candidates. Together they form something none of them say individually: *copyleft propagates through compilation*. That's not in any episode. It's a schema, a structure that emerges from co-activation across episodes.

## Complementary learning systems

[McClelland, McNaughton, and O'Reilly (1995)](https://doi.org/10.1037/0033-295X.102.3.419) proposed that the brain runs two learning systems. The hippocampus stores fast: one exposure is enough. The neocortex learns slow: statistical regularities across many episodes, acquired through interleaved replay. Neither works alone. Fast storage without slow consolidation produces a pile of episodes with no structure. Slow learning without fast storage can't capture anything new.

The transfer happens offline. During sleep, the hippocampus replays recent episodes to the neocortex. The neocortex detects co-occurrence patterns across replays and forms schemas. [Tompary and Davachi (2017)](https://doi.org/10.1016/j.cub.2017.05.041) showed this is not summarization. Overlapping memories that share structure get reorganized into shared representations in the medial prefrontal cortex. The schema changes how future episodes are encoded. Once you have "copyleft propagates through compilation," new episodes about license compliance get filed under the schema instead of stored as isolated events.

Sleep deprivation degrades judgment before it degrades perception. You can still see. You can't consolidate what you saw into patterns that inform the next decision. The episodes pile up with no schemas to organize them.

## The architecture

The salience cache is the hippocampus: fast writes, competitive retrieval, everything addressable. Consolidation is the neocortex: slow learning, pattern detection, offline.

The design constraint: schemas are additive. Raw episodes stay in the cache forever. A schema is a new node that links to its source episodes, not a summary that replaces them. "Copyleft propagates through compilation" doesn't delete the three episodes it emerged from. It sits alongside them. Future queries can match the schema directly, and when they do, the source episodes become reachable through it.

Over-merging is the failure mode. If consolidation is too aggressive, schemas absorb their sources and the store loses specificity. The cache becomes a pile of vague abstractions with no grounding. The constraint is: if you can't trace a schema back to the episodes that formed it, the merge was lossy and wrong.

The process:

1. After N retrieval rounds, scan for co-activation patterns. Which moments kept winning together?
2. Clusters that co-activated above a threshold become schema candidates.
3. For each candidate: extract what the members share. That shared structure is the schema.
4. Insert the schema as a new node with links to its source episodes.
5. The schema enters the DPP on its own merits. Same embedding space, same competition.

This runs on its own clock. Not synchronous with retrieval. Not triggered by any single query. [LIDA](https://doi.org/10.1109/TAMD.2013.2277589) got the ordering right: consolidation happens after the conscious broadcast, not before. You act first, then consolidate. Sleep, not reflex.

## What's solved, what's not

[Perception Pipe](/perception-pipe) said "the consolidation problem is largely solved" and pointed at [Mem0](https://github.com/mem0ai/mem0) and [Zep](https://www.getzep.com/). Half right. The storage is commodity. Zep's [Graphiti](https://github.com/getzep/graphiti) builds temporal knowledge graphs from episodes. [GraphRAG](https://arxiv.org/abs/2404.16130) does community detection and summarization over entity graphs. Both handle the mechanics of storing, linking, and retrieving.

What neither solves is the selection. Which clusters earn schema status? The competitive process that decides *this pattern matters, that one doesn't* is the same inhibitory mechanism from every other layer. [Perception Pipe](/perception-pipe) runs it on incoming events. [Salience](/salience) runs it on retrieval candidates. Consolidation runs it on clusters. Same geometry, different timescale. Moments compete in milliseconds. Schemas compete over days.

## Five layers

The pipeline:

1. **Perceive** — [Caret Recorder](/caret-recorder) captures raw screen activity as semantic units.
2. **Structure** — [Moments](/moments) segments events into composable chunks.
3. **Filter** — [Perception Pipe](/perception-pipe) runs competitive inhibition. Winners suppress losers.
4. **Attend** — [Salience](/salience) retrieves max-volume-k via DPP. Diverse, not redundant.
5. **Consolidate** — schemas form offline from repeated co-activation. Additive, never lossy.

Residual connections throughout: raw episodes stay addressable at every layer. Schemas add structure. The original signal is never destroyed.

I never read [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762). I started from "how does a person turn lived attention into publishable prose" and arrived here. The architecture is the same.

| Transformer | Cognition pipeline |
|---|---|
| Tokenization | Caret Recorder — raw signal to discrete units |
| Positional encoding | Moments — temporal structure over tokens |
| Softmax attention | Perception Pipe — normalized competition across all candidates |
| Multi-head attention | Salience + DPP — attend to diverse subspaces, not redundant copies |
| Feed-forward layers | Consolidation — offline compression into higher-level features |
| Residual connections | Raw episodes stay addressable; schemas are additive |

Vaswani et al. derived it from sequence-to-sequence translation. This series derived it from lived experience. Same destination, no shared path. The convergence suggests the architecture is not an engineering choice. It's what information processing looks like when you need to perceive, filter, attend, and consolidate, regardless of substrate.

One difference. A transformer consolidates into frozen weights behind an API. This pipeline consolidates into [open prose](/open-prose). The feed-forward output is public. Attention goes in. [Canon](/canon) comes out.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
