---
layout: post-wide
title: "Prescription: Soar"
tags: cognition
---

*Part of the [cognition](/cognition) series. Follows the [Diagnosis: Soar](/diagnosis-soar).*

The [diagnosis](/diagnosis-soar) found one systematic gap: procedural memory is the only store with a backward pass. Semantic memory, episodic memory, and perceptual LTM have no automatic learning mechanism that writes back to them. Chunking and RL are excellent compilers. They just don't reach the other stores.

The prescription pulls from the [parts bin](/the-parts-bin): existing algorithms, matched to Soar's data structures, that fill the missing Consolidate cells.

## 1. Episodic→Semantic consolidation

Semantic memory "does not have an automatic learning mechanism" ([§6, p.13](https://arxiv.org/abs/2205.03854)). Episodes accumulate in EPMEM without generalization ([§7, p.13](https://arxiv.org/abs/2205.03854)). The missing operation: read episodes, detect regularities, write compressed knowledge to SMEM.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Before</th><th style="background:#f0f0f0">After</th></tr></thead>
<tr><td><strong>SMEM</strong></td><td>Grows only by agent command or preloading</td><td>Grows automatically from experience</td></tr>
<tr><td><strong>EPMEM</strong></td><td>Episodes accumulate without bound</td><td>Regularities extracted, episodes compacted</td></tr>
<tr><td><strong>Transfer</strong></td><td>Agent re-learns spatial layouts per task</td><td>Recurring layouts written to SMEM, available across tasks</td></tr>
<tr><td><strong>Rosie</strong></td><td>Needs human guidance for every new domain</td><td>Generalizes from prior task episodes autonomously</td></tr>
<tr style="background:#f9f9f9"><td><strong>Contract</strong></td><td colspan="2"><em>Semantic memory reflects what the agent has experienced, not just what it was told.</em></td></tr>
</table>

### Sequences of graph snapshots

EPMEM stores episodes as change-deltas indexed by decision cycle number ([§7, p.13](https://arxiv.org/abs/2205.03854)). That's a **sequence** of **graph snapshots**: each episode is a set of WME changes, and each WME is a node in an attribute-value graph.

SMEM stores graph structures in SQLite ([§6, p.12](https://arxiv.org/abs/2205.03854)). The target is a graph database.

The [parts bin](/the-parts-bin) maps this to two cells:

<table style="max-width:500px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Stage</th><th style="background:#f0f0f0">Sequence</th><th style="background:#f0f0f0">Graph</th></tr></thead>
<tr><td style="font-style:italic">Consolidate</td><td>Grammar induction</td><td>GNN training</td></tr>
</table>

Grammar induction detects recurring patterns in sequences. GNN training learns representations over graphs. For Soar's symbolic graph structures, the closer fit is **graph coarsening**: collapse groups of co-occurring nodes across episodes into supernodes while preserving structural properties ([graph reduction survey, 2024](https://arxiv.org/html/2402.03358v4)). CLARION's Rule-Extraction-Refinement does something analogous at the implicit→explicit boundary ([Sun, 2016](https://homepages.hass.rpi.edu/rsun/folder-files/clarion-intro-slides.pdf)). No cognitive architecture does it at the episodic→semantic boundary.

### Composition + test

[Casteigts et al. (2019)](https://link.springer.com/article/10.1007/s00224-018-9876-z) model temporal data as a sequence of static graphs G₁, G₂, ..., Gδ. Two abstract operations:

- **Compose**: combine snapshots over an interval (union of structures, transitive closure of co-occurrence)
- **Test**: check whether the composed result satisfies a property (recurring structure, stable feature, frequent operator sequence)

Any parameter computable through compose + test runs in O(δ) operations, which is optimal (Casteigts et al., 2019). The framework is generic: swap the compose and test functions, compute a different regularity.

For Soar:

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-temporal-compose.svg" alt="Temporal composition: episodes G₁...Gδ → compose (union + count) → test (freq ≥ k?) → new SMEM fact" style="width:100%; display:block;">
</div>

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Soar implementation</th></tr></thead>
<tr><td>Compose</td><td>Union of WME structures across episodes in a window. Co-occurring attribute-value pairs accumulate counts.</td></tr>
<tr><td>Test</td><td>Does the composed structure meet a frequency threshold? Has this operator sequence appeared in ≥ <em>k</em> episodes?</td></tr>
<tr><td>Write</td><td>Create new SMEM graph structure encoding the regularity. Set initial base-level activation from frequency count.</td></tr>
<tr><td>Trigger</td><td>Goal completion, idle time, or episode accumulation threshold. The architectural equivalent of sleep.</td></tr>
</table>

### Prior art: Zep

[Zep](https://arxiv.org/abs/2501.13956) (Rasmussen, 2025) implements this pipeline for LLM agents with three hierarchical subgraph tiers:

1. **Episodic subgraph**: raw episodes stored losslessly with dual timestamps
2. **Semantic subgraph**: entities and relations extracted from episodes, resolved against existing graph nodes
3. **Community subgraph**: clusters of strongly-connected semantic entities, summarized at a higher level

Entity extraction + resolution produces the semantic subgraph. Label propagation clusters it into communities, extending incrementally as new episodes arrive. Soar's SMEM already has the graph database and activation-based retrieval.

### Verification

New SMEM structures should decay if they don't match future episodes. Base-level activation already biases retrieval by recency and frequency ([§6, p.12](https://arxiv.org/abs/2205.03854)). A generated structure that is never retrieved will naturally lose activation. One addition: on retrieval, compare the generalization against the current episode. If it contradicts, mark for review. This closes the loop.

## 2. Chunking–RL composition

Chunking requires deterministic substate results, but RL uses stochastic selection. The two cannot compose ([§4, p.10](https://arxiv.org/abs/2205.03854)). Laird's planned fix: gate chunking on RL convergence.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Before</th><th style="background:#f0f0f0">After</th></tr></thead>
<tr><td><strong>Chunking</strong></td><td>Disabled when RL drives the decision</td><td>Fires once RL preferences converge</td></tr>
<tr><td><strong>RL</strong></td><td>Numeric preferences tuned but never compiled</td><td>Stable policies compiled to production rules</td></tr>
<tr><td><strong>Speed</strong></td><td>RL computation every decision cycle</td><td>Converged decisions fire as direct rule matches</td></tr>
<tr><td><strong>Chunks</strong></td><td>Accumulate without review</td><td>Dead chunks detected by trauma recurrence, retracted</td></tr>
<tr style="background:#f9f9f9"><td><strong>Contract</strong></td><td colspan="2"><em>Any stable decision policy, whether discovered by deliberation or by RL, eventually compiles into a direct rule.</em></td></tr>
</table>

### Posterior convergence gate

The simplest convergence test: track the **exponential moving average of Q-value changes** for each RL rule. When the EMA drops below a threshold, the preference has stabilized. This requires no architectural modification to Soar's RL, just a monitoring wrapper. A Bayesian posterior over Q-values would give a full uncertainty estimate, but it requires changing how Soar stores RL values from point estimates to distributions. EMA is sufficient.

ACT-R's production compilation + utility learning is the closest parallel in another architecture, but there too the interaction is uncoordinated: compilation fires whenever two productions fire in sequence, regardless of whether utility values have stabilized. The gating idea is novel.

For Soar:

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

Chunks accumulate. EBBS improved chunk quality ([§4, p.10](https://arxiv.org/abs/2205.03854)) but nothing prunes the store. The parts bin suggests **prototype condensation** again: periodically scan the chunk store, identify rules that never fire (dead code) or that are superseded by more specific rules, and retract them.

The trigger is the [trauma recurrence heuristic](/diagnosis-biotech): `count(similar_failures) > 1` signals a bad chunk. If the same impasse type recurs despite a chunk that should prevent it, the chunk is wrong. Retract and rechunk.

## 3. Episodic discrimination

Every decision cycle produces an episode ([§7, p.13](https://arxiv.org/abs/2205.03854)). At ~50ms per cycle ([§10, item 3, p.18](https://arxiv.org/abs/2205.03854)), that's 72,000 episodes per hour. Retrieval cost grows with total count.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Before</th><th style="background:#f0f0f0">After</th></tr></thead>
<tr><td><strong>Storage</strong></td><td>Every decision cycle → episode</td><td>Only novel/important cycles stored at full fidelity</td></tr>
<tr><td><strong>Volume</strong></td><td>72,000 episodes/hour, unbounded</td><td>Fraction stored, bounded by importance threshold</td></tr>
<tr><td><strong>Retrieval</strong></td><td>Old episode cost grows with total count</td><td>Smaller store, faster retrieval</td></tr>
<tr><td><strong>Quality</strong></td><td>Routine episodes dilute the store</td><td>DPP thinning ensures stored episodes are diverse</td></tr>
<tr style="background:#f9f9f9"><td><strong>Contract</strong></td><td colspan="2"><em>Retrieval cost stays proportional to important episodes, not total decision cycles.</em></td></tr>
</table>

### DPP importance gate

The simplest approach is **surprise-based gating**: store an episode when its content deviates significantly from predictions. [Isele & Cosgun (AAAI 2018)](https://cdn.aaai.org/ojs/11595/11595-13-15123-1-2-20201228.pdf) identified four criteria for selective experience replay: surprise (high TD error), reward, distribution matching, and coverage maximization. For write-time gating in Soar:

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

For agents that encounter many similar surprising episodes (e.g., repeated failures at the same task), a periodic **DPP-based thinning** pass can ensure the stored set stays diverse. This separates the hot path (surprise gate, cheap, per-cycle) from the batch operation (DPP thinning, periodic, ensures diversity). Neuroscience supports this two-phase model: synaptic tagging marks salient episodes at encoding time; sharp-wave ripples during sleep selectively consolidate them ([Science, 2024](https://www.science.org/doi/10.1126/science.adk8261)).

### Fewer episodes, faster consolidation

Treatments 1 and 3 reinforce each other. Discrimination reduces the volume; consolidation reads the survivors and compresses them into semantic knowledge.

## Four cells, four algorithms

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:8em"><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Treatment</th><th style="background:#f0f0f0">Parts bin cell</th><th style="background:#f0f0f0">Soar module</th><th style="background:#f0f0f0">Effect</th></tr></thead>
<tr><td>Episodic→Semantic</td><td>Graph coarsening</td><td>EPMEM → SMEM</td><td>World knowledge grows from experience</td></tr>
<tr><td>RL-gated chunking</td><td>EMA convergence gate</td><td>RL rules → production rules</td><td>Stochastic selection compiles to deterministic rules</td></tr>
<tr><td>Chunk review</td><td>Trauma recurrence</td><td>Procedural memory</td><td>Dead and wrong chunks retracted</td></tr>
<tr><td>Episodic discrimination</td><td>Surprise gate + DPP thin</td><td>Episodic Learning</td><td>Store fewer, better episodes</td></tr>
</table>

None of these require new architectural commitments. The algorithms exist. The modules exist. The triggers are straightforward.

And yet.

## The wall behind the walls

Gate chunking on RL convergence. Consolidate episodes into semantic knowledge. Discriminate what's worth remembering. Soar would be a more complete architecture. It would still need a human.

Laird says it plainly: "Without a human to closely guide it, Rosie is unable to get very far on its own, especially in being unable to learn new abstract symbolic concepts on its own" ([§10, p.20](https://arxiv.org/abs/2205.03854)). Rosie is Soar's most capable agent. It learns sixty tasks from natural language instruction. It needs an instructor for every one.

This isn't a failure of Rosie. It's a pattern. TacAir-Soar's 8,000 rules were written by engineers. PROPS takes declarative rule descriptions authored by people. Every successful Soar agent in the [appendix](https://arxiv.org/abs/2205.03854) has a human somewhere in the causal chain, providing knowledge that the architecture cannot generate from experience alone.

Soar treats this as a development-time dependency, something to be engineered away with the next learning mechanism. Laird knows better. His own assessment: "What I feel is most missing from Soar is its ability to 'bootstrap' itself up from the architecture and a set of innate knowledge into being a fully capable agent" ([§10, p.20](https://arxiv.org/abs/2205.03854)). Forty years of evidence supports the stronger reading: the human is load-bearing.

### Complementation first

The research program has been: build the autonomous agent, then optionally add human interaction. Instructo-Soar and Rosie add a teacher, but as one application among many. The architecture doesn't require it.

What if the order is reversed?

Step one: **complementation**. Human and agent, each filling the other's gaps. The agent has speed, consistency, parallel rule firing, tireless processing; the human has judgment, novel category formation, the ability to say "this is what matters." Neither is intelligent alone. Together they are.

Step two: **bootstrap**. Use that composite intelligence to study what it does. Compress its patterns. Gradually move capabilities from the human side to the agent side. Chunking already does this at the substate level: compile deliberation into direct rules. The same principle, applied at the architecture level: compile human guidance into autonomous capability.

Soar's forty-year trajectory suggests that generating the knowledge to fill these cells requires more intelligence than any single agent has demonstrated. If the architecture can't generate it alone, it has to borrow it. The only place it currently exists at the required level is people. Solving complementation first isn't a retreat from autonomy. It's the path to it.

Soar already has the mechanism. An impasse means "I don't have enough knowledge." A substate means "go get it." What if the default resolution of certain impasses was "ask the human"? Not as a fallback. As a first-class architectural response.

Chunking would compile the answer. The agent never asks the same question twice. Over time, fewer impasses reach the human. The boundary moves.

The four prescriptions above are correct. They fill real gaps. But they're step two. Step one is acknowledging that the human who has always been there, quietly making every Soar agent work, belongs in the architecture.

## What flows back

The prescription draws from the parts bin. Soar gives back. Six algorithms from Soar's architecture are now in the [parts bin](/the-parts-bin):

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:10em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Algorithm</th><th style="background:#f0f0f0">Parts bin cell</th><th style="background:#f0f0f0">What it does</th></tr></thead>
<tr><td>RETE network</td><td>Cache × graph</td><td>Incremental pattern matching. Processes WME deltas, caches partial match state. Pays for change, not total knowledge.</td></tr>
<tr><td>Truth maintenance</td><td>Filter × graph</td><td>I-supported structures auto-retract when their creating rule unmatches. Data-driven, no explicit delete.</td></tr>
<tr><td>Staged preferences</td><td>Attend × flat</td><td>Reject-first, rank-survivors. Process prohibit/reject before better/worse/best. Exit early if rejection resolves it.</td></tr>
<tr><td>EBC/Chunking</td><td>Consolidate × tree</td><td>Backtrace through dependency tree, identify necessary conditions, compile deliberation into production rule.</td></tr>
<tr><td>Delta-bar-delta</td><td>Consolidate × flat</td><td>Per-production adaptive learning rate. Each rule gets its own alpha, updated on every RL update.</td></tr>
<tr><td>Delta episodic storage</td><td>Remember × sequence</td><td>Store only changes between snapshots. Interval representation for persistent elements.</td></tr>
</table>

Soar's largest contribution is forty years of evidence for the ordering constraint. Every agent in the appendix is a data point: the right mechanisms, assembled by a human. Together they produced intelligent behavior that neither could produce alone. That's complementation. It was always complementation. The architecture just didn't have a name for it.

---

*Based on Laird (2022), "[Introduction to the Soar Cognitive Architecture](https://arxiv.org/abs/2205.03854)"; Casteigts et al. (2019), "[Computing Parameters of Sequence-Based Dynamic Graphs](https://link.springer.com/article/10.1007/s00224-018-9876-z)"; Rasmussen (2025), "[Zep: A Temporal Knowledge Graph Architecture](https://arxiv.org/abs/2501.13956)"; the [parts bin](/the-parts-bin); and the [Natural Framework](/the-natural-framework). Written via the [double loop](/double-loop).*
