---
variant: post
title: "The Action DAG"
tags: coding, methodology
---

> "Having got the representation, something magical has happened. We've got our constraints exposed. And that's why we build representations."
>
> — Patrick Winston, MIT 6.034 Lecture 1

A simulation agent needs to turn goals into API calls. The naive approach: prompt an LLM every time. This works until you run the same simulation twice and realize you're paying for the same reasoning you already did.

The fix is a compound data structure I'm calling a **semantic DAG**: a DAG of decomposition nodes indexed by semantic similarity, entered through multiple roots.

## Structure

Each root is a natural-language goal. Each node decomposes into children. Leaves are API calls. Sub-actions are shared across goals — "click confirm" exists once in the store, referenced by any tree that needs it. The structure is a DAG, not a set of independent trees.

The distinction between goal and action is perspectival — every node is a goal from above and an action from below.

The DAG is queried by intent, not exact key. The planner describes what it wants; an embedding nearest-neighbor lookup retrieves the closest match. Queries hit both roots and one level below, so goals that share sub-actions are disambiguated by their children.

## Resolution

Recursive descent through the matched tree. Four cases:

**Cache hit.** Node's children are populated. Recurse without the LLM.

**Cache miss.** Node's children are absent. The LLM fires once to decompose, writes the result back, then recursion continues.

**Invalidation.** On failure, overwrite the broken node. The parent decomposition stays valid. Re-resolve from the invalidation point only.

**Learning.** Every successful execution writes its resolution trace. Compilation and learning are the same operation: write. The distinction is timing — a miss writes a decomposition speculatively, a success promotes that decomposition into trusted cache.

A fully compiled tree resolves goal-to-API-call with zero LLM calls. A novel goal builds its tree node by node, each miss populating one entry. On the next run, the whole tree is a hit.

### Example

Goal: "buy the cheapest sword." First run, every node is a miss:

1. **"buy the cheapest sword"** → LLM decomposes → ["open shop", "sort by price", "select first", "confirm purchase"]
2. **"open shop"** → LLM decomposes → ["navigate to merchant", "click shop icon"]
3. **"click shop icon"** → leaf, API call. Executes.

Second run, same goal: full cache hit, zero LLM calls. A different goal — "buy the cheapest armor" — hits on "open shop" (shared node), misses only on "select first" (different item category). One LLM call instead of three.

## Properties

**Context scoping.** Each simulation environment gets its own DAG. Same action in different environments, different states — different entries. Adding a new domain is a data problem: seed or learn new roots, reuse shared nodes within that domain.

**Parallelism.** Independent children at any decomposition level can resolve concurrently.

**Self-healing.** A broken leaf doesn't corrupt the tree. Invalidate the node, re-decompose from that point. If the failure is local, everything above stays valid. If repeated failures suggest the parent decomposition was wrong, invalidation propagates upward.

**Failure modes.** Wrong nearest neighbor, stale subtree after environment change, overgeneralized shared node. The embedding layer is approximate — thresholding and fallback to LLM decomposition are necessary, not optional.

## Prior art

This is a compound. Each ingredient exists:

- **HTN planning** (Erol, Hendler & Nau 1994) — hierarchical task decomposition into primitive operators.
- **Soar chunking** (Laird, Rosenbloom & Newell 1986) — compiled procedural memory from successful problem-solving traces.
- **Case-based reasoning** (Kolodner 1993) — similarity-indexed retrieval of past solutions.
- **Voyager** (Wang et al. 2023) — embedding-indexed skill library for open-ended LLM agents.

Patrick Winston taught goal trees and problem reduction in [MIT 6.034](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/), building on Slagle (1963) and Nilsson (1971). His thesis was that choosing the right representation exposes the constraints and the rest falls into place.

Each ingredient above covers one axis. HTN gives the decomposition structure. Soar gives compilation-by-write-back. CBR gives similarity retrieval. Voyager gives the embedding index over LLM-generated skills. The compound — persistent, similarity-indexed, recursively-resolvable, self-healing, LLM-as-JIT-compiler — is what I haven't seen elsewhere.

## Two parts

In [parts bin](/the-parts-bin) terms, the semantic DAG splits cleanly into two roles:

1. **Embedding filter** — similarity lookup over DAG nodes to retrieve the right subtree. This is the CBR / Voyager axis. It lives in Filter × embedding_space.

2. **HTN cache** — the decomposition tree itself, with JIT compilation on miss and write-back on success. This is the HTN / Soar axis. It lives in Cache × tree.

The filter finds the right tree. The cache resolves it. Neither is novel alone. The compound is.
