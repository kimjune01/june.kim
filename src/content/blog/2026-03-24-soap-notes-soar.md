---
variant: post-wide
title: "SOAP Notes: Soar"
tags: cognition
---

*Part of the [cognition](/cognition) series. Follows the [Diagnosis](/diagnosis-soar). See also: [Prescription](/prescription-soar) for algorithmic detail on each step.*

The [diagnosis](/diagnosis-soar) found a single root cause: missing merging in the long-term declarative stores. Five dominoes fall from it. This note summarizes the causal chain and prescribes a plan.

#### Subjective

"What I feel is most missing from Soar is its ability to 'bootstrap' itself up from the architecture and a set of innate knowledge into being a fully capable agent across a breadth of tasks" ([§10, p.20](https://arxiv.org/abs/2205.03854)). Learning rate is low: chunking can't compose with RL ("chunking is not used when decisions are made using numeric preferences," [§4, p.10](https://arxiv.org/abs/2205.03854)), semantic learning is missing ([§10, item 7, p.18](https://arxiv.org/abs/2205.03854)), episodic learning doesn't generalize ([§7, p.13](https://arxiv.org/abs/2205.03854)).

Separately, scaling degrades. "Cognitive models of complex, protracted tasks can accumulate large amounts of knowledge, and the computational performance of existing architectures degrades as a result" ([Derbinsky & Laird, 2013, §1](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563)). Derbinsky & Laird call this the *utility problem*: more knowledge harms problem-solving performance (2013, §1). A hard real-time constraint binds the two complaints. The decision cycle must stay under 50ms for real-time operation (Derbinsky & Laird, 2013, §3), and without forgetting, "episodic-memory retrievals are not tenable for a model that must reason with this amount of acquired information, as the maximum required processing time exceeds the reactivity threshold of 50 ms" (2013, §5.2). Low learning rate and degraded scaling have been investigated separately: the Consolidate stack for the first, Cache for the second.

#### Objective

Soar's Consolidate is more sophisticated than that of any other cognitive architecture proposed to date. Chunking is a principled compiler with correctness guarantees ([§4, p.9–10](https://arxiv.org/abs/2205.03854)). RL supports Q-learning, SARSA, eligibility traces, and per-production learning rates via delta-bar-delta ([§5, p.11–12](https://arxiv.org/abs/2205.03854)). The decision cycle achieves ~50ms with millions of knowledge elements ([§10, item 3, p.18](https://arxiv.org/abs/2205.03854)). Cache is optimized for its size: the RETE network matches rules incrementally against only the changes to working memory. But the cache does not evict from its long-term stores.

Derbinsky & Laird ([2013](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563)) proved forgetting is essential. Without it, a robot exceeded the 50ms threshold within an hour. They built forgetting for working memory and procedural memory. Episodic and semantic memory have no forgetting, no eviction, no capacity bound. Both grow without limit.

#### Assessment

The root cause is missing merging in the long-term declarative stores. Eviction alone trades match cost for reconstruction cost. Derbinsky & Laird's own data (2013, Fig. 4) shows reconstruction latency breaking the 50ms threshold even with single-tier WM forgetting at d=0.5, because reconstruction from episodic memory scales with working-memory size at encoding time (2013, §3). Multi-tier eviction compounds the problem: WM reconstructs from smem, smem from epmem, each hop consuming budget.

Merging avoids the chain entirely. Compress N episodes into one semantic entry, and the sources become redundant. The merged entry *is* the knowledge.

The mechanism that blocks merging is R4: Derbinsky & Laird's working-memory forgetting policy only removes elements backed up in semantic memory (2013, §5). Semantic memory has no automatic learning; it grows only by hand or preloading. So the forgettable perceptual bandwidth is bounded by what a human pre-loaded. Everything downstream follows.

Semantic memory is a hierarchical store. The architecture diagram (Laird, 2022, Fig. 1) shows it as a tree, and the [implementation](https://soar.eecs.umich.edu/soar_manual/06_SemanticMemory/) stores graph structures with parent-child relationships in SQLite. But without automatic learning, the tree is hand-built and static. Merging should produce hierarchy at multiple scales: short-window compositions yielding low-level facts (room X connects to room Y), longer windows yielding structural generalizations (building layout, navigation heuristics). A flat merge target would lose the structure that makes smem useful for spreading activation in the first place.

The right merge structure depends on the memory type. Episodic memory has temporal ordering. [Temporal graph coarsening](https://link.springer.com/article/10.1007/s00224-018-9876-z) (Casteigts et al., 2019) respects that ordering with compose + test over time windows. Semantic memory is an unordered store of facts; a [union-find forest](/union-find-compaction) could cluster similar entries incrementally, merging near-duplicate smem objects into equivalence classes. Union-find gives provenance (trace any generalization back to its source episodes via `find`) and recoverability (`expand` reinflates a merged entry if the merge turns out wrong). Both produce trees, but for different reasons: Casteigts builds a tree of temporal abstractions, union-find builds a forest of similarity clusters.

*Cache fills with stale data.* Derbinsky's robot accumulated 12,000 WMEs of old map data; with forgetting, working memory held ~2,000 (2013, Fig. 3). But forgetting only works for objects in smem (R4). Anything perceived outside that vocabulary accumulates without bound.

*Perception is throttled as a consequence.* R4 restricts what leaves rather than what enters. But WMEs that can't leave accumulate, and the RETE scales linearly with WM size. So agents compensate: they "usually ignor[e] frequently changing low-level sensory data" ([§7, p.13](https://arxiv.org/abs/2205.03854)). SVS requires deliberate filter commands ([§8, p.14](https://arxiv.org/abs/2205.03854)). The input valve is kept closed because the drain only works for pre-symbolized input.

*Elaboration becomes pollution.* Elaboration rules fire in parallel waves, proposing operators from whatever is in working memory ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). The RETE matches indiscriminately. It doesn't distinguish a fresh percept from a stale WME that should have been evicted. Without eviction, the growth phase has no end. Stale chunks keep firing on stale WMEs, proposing operators for situations that no longer exist.

The matching semantics guarantee this: elaboration promotes everything it matches, and without eviction, what it matches includes accumulated junk.

The open question is how much this degrades *task performance*, not whether it happens. Derbinsky & Laird's experiments confirm the scaling degradation (decision time grows past the 50ms threshold), but their tasks were short enough that stale proposals may not have swamped live ones. In longer-running agents with changing environments, stale operator proposals compete with current ones at the preference stage. The 30-day agents ([open question 1](/diagnosis-soar#appendix-open-questions)) would be the test case. The practical remedy is manual reset, which is an admission that the cache can't maintain itself.

*Consolidate starves.* Chunking needs novel impasses; RL needs diverse states to converge; and without varied episodes, episodic consolidation can't extract regularities. What matters is *novel state coverage*: the number of distinct states the agent visits.

A throttled perceiver that visits 100 distinct rooms feeds RL better than an open perceiver that revisits the same 10 rooms 1000 times. The drain problem ([domino 1](/diagnosis-soar#the-dominoes)) degrades novelty in two ways: accumulated WMEs crowd the RETE, slowing the cycle, reducing how many states the agent visits per hour; and the vocabulary restriction means whole categories of state distinctions never enter working memory at all. The backward pass can't fix what the forward pass won't deliver.

#### Plan

Build merging; eviction follows as a side effect.

1. **Episodic-to-semantic merge**: the primary operation. Read recurring patterns from episodes and write them as semantic generalizations. [Temporal graph coarsening](https://link.springer.com/article/10.1007/s00224-018-9876-z) (Casteigts et al., 2019) is the algorithm: compose episode snapshots over a window, test for frequency, write surviving structures to SMEM. Compose at different δ windows to build a tree of abstractions: short δ yields low-level entries, medium δ yields structural patterns, long δ yields domain heuristics. This matches smem's existing tree structure and [Zep](https://arxiv.org/abs/2501.13956)'s three-tier hierarchy (episodic → semantic → community subgraphs). The merged semantic entry replaces the episodes it was extracted from, so there is no reconstruction chain — the architectural equivalent of sleep consolidation. See the [prescription](/prescription-soar) for the full compose + test specification.
2. **Episodic eviction**: episodes whose regularities have been merged into semantic memory are redundant. Evict by base-level activation, biased to retain episodes near reward, impasse resolution, or state novelty. Cap store size. Unlike standalone eviction, merged episodes leave no reconstruction debt.
3. **Semantic maintenance with back-invalidation**: merged semantic entries should decay if they stop matching incoming episodes. Base-level activation handles the common case. A [union-find forest](/union-find-compaction) over smem entries gives the structure needed for both provenance and coherence: parent pointers trace each semantic entry back to its source episodes, and each episode forward to the semantic entry it contributed to. The pointers serve double duty: `find` answers "where did this generalization come from?" and the reverse links answer "which semantic entries depend on this episode?" When a new episode arrives, `union` links it to the matching cluster and updates the centroid. When evicting a merged entry, `expand` reinflates it from sources if needed. The pointers *are* the cross-tier coherence mechanism. No separate dependency tracker required for the common case. The hard case remains: evicting a semantic entry breaks R4's reconstruction guarantee for any WMEs forgotten under it ([domino 2](/diagnosis-soar#the-dominoes)). Before evicting, back-invalidate via the reverse pointers: check whether forgotten WMEs depend on it, and either promote them back to working memory or accept the loss.
4. **RL-gated chunking**: compose chunking with RL. Gate chunking on RL convergence so converged stochastic knowledge compiles into deterministic rules ([demonstration PR](https://github.com/SoarGroup/Soar/pull/577)). Compiled chunks are reconstructible from substates, so the RL rules that generated them become safely forgettable under the existing procedural forgetting policy. The same reconstructibility principle behind R4. Composition unblocks forgetting. Prune chunks whose conditions no longer match any WME in working memory or semantic memory; composition without pruning is another append-only store.
5. **Novel composition**: with room in the cache, newly perceived memories can compose with old ones to synthesize diverse operator sets for elaboration and chunking. Merging allows efficiency, efficiency allows diversity, and diversity allows functional Consolidate.
6. **Two-tier cache contract**: separate filter from attend with an explicit contract, allowing more perceived bits to enter based on heuristics. A deduplication-like filter, a frequency counter that passes novel WMEs and suppresses redundant ones, gates admission to the hot tier. Worth testing whether a filter contract between elaboration and selection changes the architecture's effective Perceive throughput.
7. **Open the input valve**: with merging and filtering in place, the stores can handle richer perception. The architecture no longer needs to pre-symbolize everything or ignore low-level sensory data. The ceiling moves from what a human hand-codes into the rule base to what the agent can perceive and retain.

---

Derbinsky & Laird hit the memory growth wall in 2013 and built the drain for two stores. The two long-term declarative stores are still without one. The drain they need is merging: compress episodes into semantic entries, and eviction follows. The sources are redundant, the stores stay bounded, and reconstruction debt drops to zero. Until the stores can merge what they accumulate, the input valve stays closed, and the architecture's ceiling is set by what a human hand-codes into the rule base.

Soar has always grown by hitting the wall and building through it. This is the next one.

## Mapping to the Natural Framework

For readers familiar with the [Natural Framework](/the-natural-framework), the mapping is nearly one-to-one:

<table style="max-width:500px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Soar</th><th style="background:#f0f0f0">Framework</th><th style="background:#f0f0f0">Notes</th></tr></thead>
<tr><td>Input</td><td>Perceive</td><td>Input-link, SVS perception</td></tr>
<tr><td>Working Memory</td><td>Cache</td><td>WME graph, central hub</td></tr>
<tr><td>Elaboration</td><td>Filter</td><td>Situation elaboration + operator proposal</td></tr>
<tr><td>Selection</td><td>Attend</td><td>Operator evaluation + decision procedure</td></tr>
<tr><td>Output</td><td>Remember</td><td>Output-link, LTM store commands</td></tr>
<tr><td>Learning</td><td>Consolidate</td><td>Chunking, RL, semantic/episodic learning</td></tr>
</table>

The framework's formal treatment, including the proof that these six roles are obligatory, is at [The Natural Framework](/the-natural-framework).

---

*Based on the [Diagnosis](/diagnosis-soar) and [Prescription](/prescription-soar). Sources: Laird (2022), "[Introduction to the Soar Cognitive Architecture](https://arxiv.org/abs/2205.03854)"; Derbinsky & Laird (2013), "[Effective and efficient forgetting of learned knowledge](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563)"; Casteigts et al. (2019), "[Computing Parameters of Sequence-Based Dynamic Graphs](https://link.springer.com/article/10.1007/s00224-018-9876-z)." Written via the [double loop](/double-loop).*
