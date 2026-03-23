---
layout: post-wide
title: "Prescription: Soar"
tags: cognition
---

*Part of the [cognition](/cognition) series. Follows the [Diagnosis](/diagnosis-soar).*

The [diagnosis](/diagnosis-soar) found one systematic gap: procedural memory is the only store with a backward pass. Semantic memory, episodic memory, and perceptual LTM have no automatic learning mechanism that writes back to them. Chunking and RL are excellent compilers. They just don't reach the other stores.

The prescription pulls from the [parts bin](/the-parts-bin): existing algorithms, matched to Soar's data structures, that fill the missing Consolidate cells. Each treatment maps a known algorithm to a specific Soar module, with the trigger condition, the read source, the write target, and the expected effect.

## 1. Episodic→Semantic consolidation

The highest-priority gap. Semantic memory "does not have an automatic learning mechanism" ([§6, p.13](https://arxiv.org/abs/2205.03854)). Episodes accumulate in EPMEM without generalization ([§7, p.13](https://arxiv.org/abs/2205.03854)). The missing operation: read episodes, detect regularities, write compressed knowledge to SMEM.

### The data structures

EPMEM stores episodes as change-deltas indexed by decision cycle number ([§7, p.13](https://arxiv.org/abs/2205.03854)). That's a **sequence** of **graph snapshots**: each episode is a set of WME changes, and each WME is a node in an attribute-value graph.

SMEM stores graph structures in SQLite ([§6, p.12](https://arxiv.org/abs/2205.03854)). The target is a graph database.

The [parts bin](/the-parts-bin) maps this to two cells:

<table style="max-width:500px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Stage</th><th style="background:#f0f0f0">Sequence</th><th style="background:#f0f0f0">Graph</th></tr></thead>
<tr><td style="font-style:italic">Consolidate</td><td>Grammar induction</td><td>GNN training</td></tr>
</table>

Grammar induction detects recurring patterns in sequences. GNN training learns representations over graphs. For Soar's symbolic architecture, the closer fit is **prototype condensation**: compress many episode-graphs into a small set of exemplar graph structures that capture the regularity.

### The algorithm: composition + test

[Peters et al. (2019)](https://link.springer.com/article/10.1007/s00224-018-9876-z) model temporal data as a sequence of static graphs G₁, G₂, ..., Gδ. Two abstract operations:

- **Compose**: combine snapshots over an interval (union of structures, transitive closure of co-occurrence)
- **Test**: check whether the composed result satisfies a property (recurring structure, stable feature, frequent operator sequence)

Any parameter computable through compose + test runs in O(δ) operations, which is optimal. The framework is generic: swap the compose and test functions, compute a different regularity.

For Soar:

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Soar implementation</th></tr></thead>
<tr><td>Compose</td><td>Union of WME structures across episodes in a window. Co-occurring attribute-value pairs accumulate counts.</td></tr>
<tr><td>Test</td><td>Does the composed structure meet a frequency threshold? Has this operator sequence appeared in ≥ <em>k</em> episodes?</td></tr>
<tr><td>Write</td><td>Create new SMEM graph structure encoding the regularity. Set initial base-level activation from frequency count.</td></tr>
<tr><td>Trigger</td><td>Goal completion, idle time, or episode accumulation threshold. The architectural equivalent of sleep.</td></tr>
</table>

### Prior art: Zep

[Zep](https://arxiv.org/abs/2501.13956) (Rasmussen, 2025) implements exactly this pipeline for LLM agents with three hierarchical subgraph tiers:

1. **Episodic subgraph**: raw episodes stored losslessly with dual timestamps
2. **Semantic subgraph**: entities and relations extracted from episodes, resolved against existing graph nodes
3. **Community subgraph**: clusters of strongly-connected semantic entities, summarized at a higher level

The episodic→semantic step is entity extraction + resolution. The semantic→community step uses label propagation, which extends incrementally as new episodes arrive. Soar's SMEM already has the graph database and the activation-based retrieval. The missing piece is the extraction step: the cron job that reads EPMEM and writes SMEM.

### Verification

New SMEM structures should decay if they don't match future episodes. Base-level activation already biases retrieval by recency and frequency ([§6, p.12](https://arxiv.org/abs/2205.03854)). A generated structure that is never retrieved will naturally lose activation. One addition: on retrieval, compare the generalization against the current episode. If it contradicts, mark for review. This closes the loop.

## 2. Chunking–RL composition

Chunking requires deterministic substate results. RL uses stochastic selection. The two cannot compose ([§4, p.10](https://arxiv.org/abs/2205.03854)). Laird's planned fix: gate chunking on RL convergence.

### The algorithm: Bayesian posterior convergence

The parts bin's Consolidate column includes **Bayesian posterior update**: prior parameters + weighted observations → posterior compressed. The convergence criterion is natural: when the posterior variance falls below a threshold, the distribution has stabilized. The MAP estimate becomes the deterministic value.

For Soar:

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Step</th><th style="background:#f0f0f0">Soar implementation</th></tr></thead>
<tr><td>Track</td><td>For each RL rule, maintain a running variance of numeric preference values across recent updates.</td></tr>
<tr><td>Gate</td><td>When variance drops below threshold <em>τ</em>, the preference has converged. Flag the decision as deterministic.</td></tr>
<tr><td>Compile</td><td>Chunking fires on the flagged substate. The resulting chunk encodes the converged policy as a production rule.</td></tr>
<tr><td>Continue</td><td>RL keeps running on unconverged decisions. Chunking picks off the stable ones as they settle.</td></tr>
</table>

This is one Consolidate stack reading from another's output. RL writes preference weights (its substrate). Chunking reads those weights, detects convergence, and compiles the stable policy into a rule (its substrate). Two backward passes, composed.

### Chunk review: Consolidate for the Consolidate

Chunks accumulate. EBBS improved chunk quality ([§4, p.10](https://arxiv.org/abs/2205.03854)) but nothing prunes the store. The parts bin suggests **prototype condensation** again: periodically scan the chunk store, identify rules that never fire (dead code) or that are superseded by more specific rules, and retract them.

The trigger is the [trauma recurrence heuristic](/diagnosis-biotech): `count(similar_failures) > 1` signals a bad chunk. If the same impasse type recurs despite a chunk that should prevent it, the chunk is wrong. Retract and rechunk.

## 3. Episodic discrimination

Every decision cycle produces an episode ([§7, p.13](https://arxiv.org/abs/2205.03854)). At ~50ms per cycle ([§10, item 3, p.18](https://arxiv.org/abs/2205.03854)), that's 72,000 episodes per hour. Retrieval cost grows with total count. The missing cell is Attend on the write path.

### The algorithm: DPP importance gating

The parts bin's Attend column includes **DPP top-k selection**: candidates + relevance weights + similarity kernel → top-k ranked, mutually dissimilar, bounded. Applied to episodes at write time:

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Signal</th><th style="background:#f0f0f0">Implementation</th></tr></thead>
<tr><td>Relevance</td><td>Reward proximity (positive or negative), impasse resolution, operator application that changed the goal stack.</td></tr>
<tr><td>Similarity</td><td>WME overlap with recent episodes. High overlap = routine. Low overlap = novel.</td></tr>
<tr><td>Gate</td><td>Episodes with high relevance and low similarity to recent episodes are stored at full fidelity. Routine episodes are stored at reduced fidelity or skipped.</td></tr>
</table>

This doesn't require forgetting. It requires discrimination at write time. Important episodes (near reward, near impasse resolution, structurally novel) get full storage. Routine episodes get compressed or dropped. The DPP kernel guarantees that stored episodes are diverse, not just important.

### Connection to consolidation

Episodic discrimination and episodic→semantic consolidation reinforce each other. Discrimination reduces the volume of episodes. Consolidation reads the surviving episodes and compresses them into semantic knowledge. The reduced volume makes consolidation faster and the compressed episodes are higher quality. Two missing cells, one feedback loop.

## Summary

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:8em"><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Treatment</th><th style="background:#f0f0f0">Parts bin cell</th><th style="background:#f0f0f0">Soar module</th><th style="background:#f0f0f0">Effect</th></tr></thead>
<tr><td>Episodic→Semantic</td><td>Consolidate × graph</td><td>EPMEM → SMEM</td><td>World knowledge grows from experience</td></tr>
<tr><td>RL-gated chunking</td><td>Consolidate × sequence</td><td>RL rules → production rules</td><td>Stochastic selection compiles to deterministic rules</td></tr>
<tr><td>Chunk review</td><td>Consolidate × flat</td><td>Procedural memory</td><td>Dead and wrong chunks retracted</td></tr>
<tr><td>Episodic discrimination</td><td>Attend × sequence</td><td>Episodic Learning</td><td>Store fewer, better episodes</td></tr>
</table>

None of these require new architectural commitments. They require existing algorithms applied to existing Soar modules, with triggers that fire the backward pass automatically. Soar has always grown by hitting a wall and building through it. These are the next four walls.

---

*Based on Laird (2022), "[Introduction to the Soar Cognitive Architecture](https://arxiv.org/abs/2205.03854)"; Peters et al. (2019), "[Computing Parameters of Sequence-Based Dynamic Graphs](https://link.springer.com/article/10.1007/s00224-018-9876-z)"; Rasmussen (2025), "[Zep: A Temporal Knowledge Graph Architecture](https://arxiv.org/abs/2501.13956)"; and the [parts bin](/the-parts-bin). Written via the [double loop](/double-loop).*
