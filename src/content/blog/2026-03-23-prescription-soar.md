---
layout: post-wide
title: "Prescription: Soar"
tags: cognition
---

*Part of the [cognition](/cognition) series. Follows the [Diagnosis](/diagnosis-soar) and [SOAP Notes](/soap-notes-soar).*

The [diagnosis](/diagnosis-soar) found four constraints. Each has a known relief. This post provides the algorithmic detail, pulling from the [parts bin](/the-parts-bin). The first three are things to build; the last section describes what opens up when they're in place.

## Episodic-to-semantic merge

The primary operation. Read recurring patterns from episodes and write them as semantic generalizations. Merged semantic entries replace the episodes they were extracted from. The merged entry *is* the knowledge. A [demonstration PR](https://github.com/SoarGroup/Soar/pull/578) implements merge and eviction.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Before</th><th style="background:#f0f0f0">After</th></tr></thead>
<tr><td><strong>SMEM</strong></td><td>Grows only by agent command or preloading</td><td>Grows automatically from experience</td></tr>
<tr><td><strong>EPMEM</strong></td><td>Episodes accumulate without bound</td><td>Regularities extracted, episodes compacted</td></tr>
<tr><td><strong>Transfer</strong></td><td>Agent re-learns spatial layouts per task</td><td>Recurring layouts written to SMEM, available across tasks</td></tr>
<tr><td><strong>Rosie</strong></td><td>Needs human guidance for every new domain</td><td>Generalizes from prior task episodes autonomously</td></tr>
<tr style="background:#f9f9f9"><td><strong>Contract</strong></td><td colspan="2"><em>Semantic memory reflects what the agent has experienced, beyond what it was told.</em></td></tr>
</table>

### Sequences of graph snapshots

EPMEM stores episodes as change-deltas indexed by decision cycle number ([§7, p.13](https://arxiv.org/abs/2205.03854)). That's a **sequence** of **graph snapshots**: each episode is a set of WME changes, and each WME is a node in an attribute-value graph.

SMEM stores graph structures in SQLite ([§6, p.12](https://arxiv.org/abs/2205.03854)). The target is a graph database rather than a flat one. The architecture diagram (Laird, 2022, Fig. 1) shows smem as a tree, and the [implementation](https://soar.eecs.umich.edu/soar_manual/06_SemanticMemory/) stores parent-child relationships. Merging must produce hierarchy at multiple scales instead of a single flat target.

The [parts bin](/the-parts-bin) maps this to two cells:

<table style="max-width:500px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Stage</th><th style="background:#f0f0f0">Sequence</th><th style="background:#f0f0f0">Graph</th></tr></thead>
<tr><td style="font-style:italic">Consolidate</td><td>Temporal composition<br><span style="font-size:11px; color:#666">Casteigts et al. 2019</span></td><td>Graph coarsening<br><span style="font-size:11px; color:#666"><a href="https://arxiv.org/html/2402.03358v4">survey, 2024</a></span></td></tr>
</table>

Soar's episodes are sequences of graphs, so both operations apply: coarsening operates within each snapshot, composition operates across them. [CLARION](https://en.wikipedia.org/wiki/CLARION_(cognitive_architecture))'s Rule-Extraction-Refinement does something analogous at the implicit→explicit boundary ([Sun, 2016](https://homepages.hass.rpi.edu/rsun/folder-files/clarion-intro-slides.pdf)). No cognitive architecture does it at the episodic→semantic boundary.

### Graph coarsening

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-coarsen-compose.svg" alt="Graph coarsening shrinks each snapshot; temporal composition finds stable structures across windows" style="width:100%; display:block;">
</div>

Collapse co-occurring nodes within a single snapshot into supernodes while preserving structural properties ([graph reduction survey, 2024](https://arxiv.org/html/2402.03358v4)). Each episode's WME graph gets smaller: attribute-value pairs that always co-occur merge into a single supernode. The coarsened snapshot is what enters the temporal composition window.

### Composition + test

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-temporal-compose.svg" alt="Temporal composition: older snapshots fade, compose+test extracts stable structure" style="width:100%; display:block;">
</div>

[Casteigts et al. (2019)](https://link.springer.com/article/10.1007/s00224-018-9876-z) model temporal data as a sequence of static graphs G₁, G₂, ..., Gδ. Two abstract operations:

- **Compose**: combine snapshots over an interval (union of structures, transitive closure of co-occurrence)
- **Test**: check whether the composed result satisfies a property (recurring structure, stable feature, frequent operator sequence)

Any parameter computable through compose + test runs in O(δ) operations, which is optimal (Casteigts et al., 2019). The framework is generic: swap the compose and test functions, compute a different regularity.

Compose at different δ windows to build a tree of abstractions: short δ yields low-level entries, medium δ yields structural patterns, long δ yields domain heuristics. This matches smem's existing tree structure and [Zep](https://arxiv.org/abs/2501.13956)'s three-tier hierarchy (episodic → semantic → community subgraphs).

For Soar:

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Soar implementation</th></tr></thead>
<tr><td>Compose</td><td>Union of WME structures across episodes in a window. Co-occurring attribute-value pairs accumulate counts.</td></tr>
<tr><td>Test</td><td>Does the composed structure meet a frequency threshold? Has this operator sequence appeared in ≥ <em>k</em> episodes?</td></tr>
<tr><td>Write</td><td>Create new SMEM graph structure encoding the regularity. Set initial base-level activation from frequency count.</td></tr>
<tr><td>Trigger</td><td>Goal completion, idle time, or episode accumulation threshold. The architectural equivalent of sleep.</td></tr>
</table>

[Zep](https://arxiv.org/abs/2501.13956) (Rasmussen, 2025) implements a similar episodic→semantic pipeline for LLM agents, with community detection as a third tier. Soar's SMEM already has the graph database and activation-based retrieval; the missing piece is the consolidation loop.

## Episodic eviction

Episodes whose regularities have been merged into semantic memory are redundant. The semantic entry already contains what mattered, so eviction incurs no reconstruction debt.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Before</th><th style="background:#f0f0f0">After</th></tr></thead>
<tr><td><strong>Storage</strong></td><td>Every decision cycle → episode</td><td>Only novel/important cycles stored at full fidelity</td></tr>
<tr><td><strong>Volume</strong></td><td>72,000 episodes/hour, unbounded</td><td>Fraction stored, bounded by importance threshold</td></tr>
<tr><td><strong>Retrieval</strong></td><td>Old episode cost grows with total count</td><td>Smaller store, faster retrieval</td></tr>
<tr><td><strong>Quality</strong></td><td>Routine episodes dilute the store</td><td>DPP thinning ensures stored episodes are diverse</td></tr>
<tr style="background:#f9f9f9"><td><strong>Contract</strong></td><td colspan="2"><em>Retrieval cost stays proportional to important episodes, instead of total decision cycles.</em></td></tr>
</table>

Eviction alone trades match cost for reconstruction cost. Derbinsky & Laird's own data (2013, Fig. 4) shows reconstruction latency breaking the 50ms threshold even at d=0.5, because reconstruction from episodic memory scales with working-memory size at encoding time (2013, §3). Multi-tier eviction compounds the problem: WM reconstructs from smem, smem from epmem, each hop consuming budget. Merging avoids the chain entirely. Compress N episodes into one semantic entry, and the sources become redundant.

### Write-time discrimination

Not all episodes are worth storing. The simplest approach is **surprise-based gating**: store an episode when its content deviates significantly from predictions. [Isele & Cosgun (AAAI 2018)](https://cdn.aaai.org/ojs/11595/11595-13-15123-1-2-20201228.pdf) identified four criteria for selective experience replay: surprise (high TD error), reward, distribution matching, and coverage maximization.

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Signal</th><th style="background:#f0f0f0">Implementation</th></tr></thead>
<tr><td>Relevance</td><td>Reward proximity (positive or negative), impasse resolution, operator application that changed the goal stack.</td></tr>
<tr><td>Similarity</td><td>WME overlap with recent episodes. High overlap = routine. Low overlap = novel.</td></tr>
<tr><td>Gate</td><td>Episodes with high relevance and low similarity to recent episodes are stored at full fidelity. Routine episodes are stored at reduced fidelity or skipped.</td></tr>
</table>

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-episodic-gate.svg" alt="Episodic discrimination: decision cycle → importance score → DPP gate → novel episodes stored at full fidelity, routine episodes skipped" style="width:100%; display:block;">
</div>

For agents that encounter many similar surprising episodes (e.g., repeated failures at the same task), a periodic **[DPP](https://en.wikipedia.org/wiki/Determinantal_point_process)-based thinning** pass ensures the stored set stays diverse. This separates the hot path (surprise gate, cheap, per-cycle) from the batch operation (DPP thinning, periodic, ensures diversity). Neuroscience supports this two-phase model: synaptic tagging marks salient episodes at encoding time; sharp-wave ripples during sleep selectively consolidate them ([Science, 2024](https://www.science.org/doi/10.1126/science.adk8261)).

### Fewer episodes, faster consolidation

Eviction and consolidation reinforce each other. Discrimination reduces the volume; consolidation reads the survivors and compresses them into semantic knowledge.

## Semantic maintenance with back-invalidation

Merged semantic entries should decay if they stop matching incoming episodes. Base-level activation handles the common case. The hard case is cross-tier coherence.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Before</th><th style="background:#f0f0f0">After</th></tr></thead>
<tr><td><strong>SMEM</strong></td><td>Hand-built, static, no eviction</td><td>Grows from experience, decays by activation, maintains provenance</td></tr>
<tr><td><strong>Coherence</strong></td><td>R4 assumes smem is stable</td><td>Back-invalidation propagates eviction across tiers</td></tr>
<tr><td><strong>Provenance</strong></td><td>None: smem entries are opaque</td><td>Every generalization traces to its source episodes</td></tr>
<tr style="background:#f9f9f9"><td><strong>Contract</strong></td><td colspan="2"><em>Semantic memory is self-maintaining: grows from experience, decays when experience contradicts it, and never orphans dependent structures silently.</em></td></tr>
</table>

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-back-invalidation.svg" alt="Three-tier back-invalidation: WM forgets under R4, smem entry evicted, orphaned WME flagged" style="width:100%; display:block;">
</div>

### The R4 coherence problem

Derbinsky & Laird's working-memory forgetting policy has a requirement that makes cross-tier coupling explicit: **R4 dictates that the mechanism only removes elements from working memory that augment objects in semantic memory** (2013, §5). The rationale: you can only safely forget what you can reconstruct. Today this is benign because smem rarely changes. But with automatic learning and eviction, smem changes actively. Every smem deletion can orphan WMEs that were "safely" forgotten from working memory under R4. The WME is gone, its backup is gone, reconstruction fails silently.

### Union-find forest over smem

A [union-find forest](/union-find-compaction) over smem entries gives the structure needed for both provenance and coherence. Parent pointers trace each semantic entry back to its source episodes, and each episode forward to the semantic entry it contributed to. The pointers serve double duty:

- **`find`**: "where did this generalization come from?" (provenance)
- **Reverse links**: "which semantic entries depend on this episode?" (coherence)
- **`union`**: links a new episode to the matching cluster and updates the centroid
- **`expand`**: reinflates a merged entry from sources if the merge turns out wrong (recoverability)

The pointers *are* the cross-tier coherence mechanism. No separate dependency tracker required for the common case. Union-find's parent pointers are plain integers, compatible with smem's existing SQLite schema and with the JTMS dependency links already in working memory. No new pointer type is needed; the forest threads through the same identifier space. The [union-find compaction](/union-find-compaction) experiment implements this structure for a different domain (embedding deduplication) and confirms that `find`, `union`, and `expand` compose without a separate index.

### Back-invalidation protocol

The hard case: evicting a semantic entry breaks R4's reconstruction guarantee for any WMEs forgotten under it ([domino 2](/diagnosis-soar#the-dominoes)). Before evicting:

1. Walk the reverse pointers to find WMEs forgotten under R4 that depend on this smem entry
2. If any exist, either promote them back to working memory or accept the loss
3. If the smem entry was the root of a union-find tree, propagate invalidation to child entries

This is a [cache coherence](https://en.wikipedia.org/wiki/Cache_coherence) problem. The existing JTMS mechanism already handles dependency-driven retraction within working memory; the missing wiring is back-invalidation across the tier boundary. Union-find pointers provide that wiring without a separate JTMS installation.

### Structural redundancy via tree inclusion

BLA handles staleness — entries that haven't been accessed decay. But an actively retrieved entry can still be redundant if a richer entry structurally contains it. After a merge produces a new smem entry, check whether existing entries are structurally dominated: entry B is redundant if B's graph [embeds into](https://epubs.siam.org/doi/abs/10.1137/S0097539791218202) A's via tree inclusion ([Kilpeläinen & Mannila, 1995](https://epubs.siam.org/doi/abs/10.1137/S0097539791218202)) — same nodes, same parent-child relationships, possibly with extra structure in A. The check is O(|B|·|A|) per pair. After merge, run the dominance check against the union-find cluster's neighbors. Dominated entries are evicted through the back-invalidation protocol above.

The same check applies to procedural memory. A chunk compiled from a richer substate may structurally contain an older chunk's condition tree. Tree inclusion on the condition DAGs identifies not just dead chunks (never fire) but redundant ones (fire but do nothing the dominating chunk doesn't already do).

BLA and tree inclusion are orthogonal: BLA evicts the stale, tree inclusion evicts the subsumed. Both feed into back-invalidation.

## RL-gated chunking

Chunking requires deterministic substate results, but RL uses stochastic selection. The two cannot compose ([§4, p.10](https://arxiv.org/abs/2205.03854)). Laird's planned fix: gate chunking on RL convergence. A [demonstration PR](https://github.com/SoarGroup/Soar/pull/577) exists.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Before</th><th style="background:#f0f0f0">After</th></tr></thead>
<tr><td><strong>Chunking</strong></td><td>Disabled when RL drives the decision</td><td>Fires once RL preferences converge</td></tr>
<tr><td><strong>RL</strong></td><td>Numeric preferences tuned but never compiled</td><td>Stable policies compiled to production rules</td></tr>
<tr><td><strong>Speed</strong></td><td>RL computation every decision cycle</td><td>Converged decisions fire as direct rule matches</td></tr>
<tr><td><strong>Forgetting</strong></td><td>RL rules can't be safely forgotten</td><td>Compiled chunks are reconstructible; RL rules become forgettable</td></tr>
<tr style="background:#f9f9f9"><td><strong>Contract</strong></td><td colspan="2"><em>Any stable decision policy, whether discovered by deliberation or by RL, eventually compiles into a direct rule.</em></td></tr>
</table>

### Posterior convergence gate

Track the **exponential moving average of Q-value changes** for each RL rule. When the EMA drops below a threshold, the preference has stabilized. This requires no architectural modification to Soar's RL, just a monitoring wrapper.

The [stochasticity requirement](/the-natural-framework#attend) derives from [Landauer's principle](https://en.wikipedia.org/wiki/Landauer%27s_principle): deterministic selection can't explore, so any system with a real Attend stage must inject noise. But Consolidate needs deterministic input to compile. The tension is physical rather than architectural:

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Natural Framework</th><th style="background:#f0f0f0">Soar</th></tr></thead>
<tr><td><strong>Attend</strong></td><td>Must be stochastic (derived)</td><td>RL exploration is stochastic (observed)</td></tr>
<tr><td><strong>Consolidate</strong></td><td>Reads from Remember, writes policy</td><td>Chunking reads substates, writes rules</td></tr>
<tr><td><strong>The gap</strong></td><td>Phase transition required</td><td>Gate required</td></tr>
</table>

The convergence gate *is* the phase transition. Attend starts stochastic, EMA tracks stability, and when it crosses threshold the decision becomes deterministic. Consolidate can finally read it.

ACT-R has the same uncoordinated interaction between utility learning and production compilation. Any architecture with a real Attend and a real Consolidate will hit this wall. The gate is the generic fix.

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Step</th><th style="background:#f0f0f0">Soar implementation</th></tr></thead>
<tr><td>Track</td><td>For each RL rule, maintain an EMA of |ΔQ| across recent updates.</td></tr>
<tr><td>Gate</td><td>When EMA drops below threshold <em>τ</em>, the preference has converged. Flag the decision as deterministic.</td></tr>
<tr><td>Compile</td><td>Chunking fires on the flagged substate. The resulting chunk encodes the converged policy as a production rule.</td></tr>
<tr><td>Continue</td><td>RL keeps running on unconverged decisions. Chunking picks off the stable ones as they settle.</td></tr>
</table>

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-chunking-rl.svg" alt="RL-gated chunking: RL rules → TD updates → variance check → if converged, chunking fires → new production rule" style="width:100%; display:block;">
</div>

### Pruning dead chunks

Chunks accumulate. Soar already has [base-level activation forgetting for procedural memory](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563): rules that never fire lose activation and are eventually forgotten. This handles dead chunks. But BLA can't handle chunks that are *actively wrong*. A chunk compiled from stale knowledge fires confidently in a changed world, keeping its activation high.

Two detection mechanisms:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Signal</th><th style="background:#f0f0f0">Detection</th><th style="background:#f0f0f0">Response</th></tr></thead>
<tr><td>Trauma recurrence</td><td><code>count(similar_failures) > 1</code> — same impasse recurs despite a chunk that should prevent it.</td><td>Retract chunk, re-enter substate, rechunk.</td></tr>
<tr><td>Reward drift</td><td>EMA of |ΔQ| spikes after stability. <a href="https://dl.acm.org/doi/10.1145/1150402.1150423">ADWIN</a>: variable-length window, bounded false-positive rate.</td><td>Flag chunk, re-enter substate, rechunk.</td></tr>
</table>

The gate that says "stable enough to compile" is the same gate that says "no longer stable, recompile." Composition without pruning is another append-only store.

## What opens up

The three reliefs above build the drain. Everything below follows as a side effect.

**Novel composition.** With bounded stores, newly perceived memories compose with old ones. A spatial layout merged from 50 episodes combines with a fresh navigation failure to synthesize an operator proposal that neither would produce alone. Merged semantic entries participate alongside fresh percepts in the elaboration phase. No new mechanism is needed. The elaboration phase, the impasse mechanism, and chunking already do this. They just need a bounded cache to work with.

**Wider perception.** Derbinsky & Laird's robot throttled perception because the drain didn't work ([domino 1](/diagnosis-soar#the-dominoes)). R4 restricted what could leave working memory to what was backed up in semantic memory. With automatic semantic learning, R4's scope expands. Newly perceived categories get merged into smem, making their WMEs forgettable. The drain opens, so the valve can open. The architecture no longer needs to pre-symbolize everything or "usually ignor[e] frequently changing low-level sensory data" ([§7, p.13](https://arxiv.org/abs/2205.03854)).

**Filtering between elaboration and selection.** A testable hypothesis rather than a known algorithm. Soar's forward pass treats elaboration and selection as causally dependent phases with no explicit filter between them ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). A novelty gate (a frequency counter that passes novel WMEs and suppresses redundant ones) could change the architecture's effective Perceive throughput. The [parts bin](/the-parts-bin) has the components (change-point detection, truth maintenance); their composition within Soar's decision cycle is uncharted.

## Giving back

The prescription draws from the parts bin. Soar gives back. Six algorithms from Soar's architecture are now in the [parts bin](/the-parts-bin):

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:10em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Algorithm</th><th style="background:#f0f0f0">Parts bin cell</th><th style="background:#f0f0f0">What it does</th></tr></thead>
<tr><td>RETE network</td><td>Cache × graph</td><td>Incremental pattern matching. Processes WME deltas, caches partial match state. Pays for change instead of total knowledge.</td></tr>
<tr><td>Truth maintenance</td><td>Filter × graph</td><td>I-supported structures auto-retract when their creating rule unmatches. Data-driven, no explicit delete.</td></tr>
<tr><td>Staged preferences</td><td>Attend × flat</td><td>Reject-first, rank-survivors via <a href="https://github.com/SoarGroup/Soar/blob/development/Core/SoarKernel/src/decision_process/decide.cpp"><code>run_preference_semantics()</code></a>. Process prohibit/reject before better/worse/best.</td></tr>
<tr><td>EBC/Chunking</td><td>Consolidate × tree</td><td>Backtrace through dependency tree, identify necessary conditions, compile deliberation into production rule.</td></tr>
<tr><td>Delta-bar-delta</td><td>Consolidate × flat</td><td>Per-production adaptive learning rate. Each rule gets its own alpha, updated on every RL update.</td></tr>
<tr><td>Delta episodic storage</td><td>Remember × sequence</td><td>Store only changes between snapshots. Interval representation for persistent elements.</td></tr>
</table>

---

*Based on Laird (2022), "[Introduction to the Soar Cognitive Architecture](https://arxiv.org/abs/2205.03854)"; Derbinsky & Laird (2013), "[Effective and efficient forgetting of learned knowledge](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563)"; Casteigts et al. (2019), "[Computing Parameters of Sequence-Based Dynamic Graphs](https://link.springer.com/article/10.1007/s00224-018-9876-z)"; Rasmussen (2025), "[Zep: A Temporal Knowledge Graph Architecture](https://arxiv.org/abs/2501.13956)"; the [parts bin](/the-parts-bin); the [union-find compaction](/union-find-compaction) experiment; and the [Natural Framework](/the-natural-framework). Written via the [double loop](/double-loop).*
