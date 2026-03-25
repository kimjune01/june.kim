---
layout: post-wide
title: "Diagnosis: Soar"
tags: cognition
---

*Part of the [cognition](/cognition) series. See also: [SOAP Notes: Soar](/soap-notes-soar) and [Prescription: Soar](/prescription-soar).*

Soar is among the most ambitious artifacts in computer science. Where most AI research optimizes a single capability, John Laird and his collaborators spent forty years building the whole mind, taking Allen Newell's challenge literally ([Laird, 2022, §intro](https://arxiv.org/abs/2205.03854)). Every module earns its place, every mechanism connects through a single central hub, and the decision cycle stages parallel rule firing into sequential action. Soar works.

The diagnosis is based on Laird's [2022 introduction](https://arxiv.org/abs/2205.03854), the [Gentle Introduction](https://web.eecs.umich.edu/~soar/sitemaker/docs/misc/GentleIntroduction-2006.pdf) (Lehman, Laird, & Rosenbloom, 2006), [Derbinsky & Laird (2013)](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563) on forgetting in Soar, the [open-source implementation](https://github.com/SoarGroup/Soar) and its [manual](https://soar.eecs.umich.edu/soar_manual/), and correspondence with Laird.

## Observations

Soar is not one pipeline. It is a set of interacting task-independent modules ([§1, p.2](https://arxiv.org/abs/2205.03854)). Figure 1 of Laird (2022) shows the structure: five memories (Procedural, Semantic, Episodic, Symbolic Working Memory, Perceptual LT Memory), a Preference Memory buffer between elaboration and the decision procedure, four learning modules (Chunking, RL, Semantic Learning, Episodic Learning), the Decision Procedure, the Spatial-Visual System, and Embodiment (Perception, Motor).

Each module has its own knowledge representation, retrieval mechanism, and learning method (Figure 6, [§9.2, p.17](https://arxiv.org/abs/2205.03854)). The decision cycle is the top-level pipeline that orchestrates them. Diagnosing Soar means diagnosing each module individually.

<div style="max-width:90vw; margin:1.5em auto;">
<img src="/assets/soar-composition.svg" alt="Soar composition diagram" style="width:80%; display:block; margin:0 auto;">
</div>

## What Soar gets right

**The impasse mechanism is a work of engineering.** When knowledge is insufficient to select or apply an operator, Soar creates a substate and reasons about the gap ([§3, p.7](https://arxiv.org/abs/2205.03854)). The same decision cycle runs recursively in the substate, with full access to all reasoning and memory capabilities. This single mechanism unifies planning, hierarchical task decomposition, metacognition, and deliberate operator evaluation ([§3.3, p.9](https://arxiv.org/abs/2205.03854)). Most architectures bolt these on. Soar derives them.

**The decision cycle stages elaboration before selection.** Elaboration rules fire in causally dependent waves: situation elaboration, then operator proposal, then operator evaluation ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). Evaluation rules create reject, better/worse, best/worst, and numeric preferences that determine which proposed operator should be selected ([§2.2.3, p.6](https://arxiv.org/abs/2205.03854)). The [decision procedure](https://soar.eecs.umich.edu/soar_manual/02_TheSoarArchitecture/) processes these in a fixed eight-step sequence: require, collect acceptable, prohibit, reject, *then* better/worse, best, worst, indifferent. Rejection before ranking, confirmed in [`run_preference_semantics()`](https://github.com/SoarGroup/Soar/blob/development/Core/SoarKernel/src/decision_process/decide.cpp).

The architecture arrived at this answer through forty years of building agents that had to work. Soar started in 1983 as a problem-solving architecture. The early agents exposed what was missing: no way to learn from deliberation (chunking was added), no way to handle uncertainty in selection (RL was added in 2005), no way to remember facts or experiences (semantic and episodic memory were added in 2006–2008), no way to reason about space (SVS was added). Each addition came from running into a wall while building a real agent, then extending the architecture to get past it.

**Chunking is the cleanest learning mechanism in any cognitive architecture.** It backtraces through the dependency chain, identifies which superstate conditions were necessary, and writes a production rule that fires directly next time ([§4, p.9–10](https://arxiv.org/abs/2205.03854)). Deliberation compiles into reaction. EBBS ensures the learned rule is correct relative to the substate reasoning and as general as possible without being over-general ([§4, p.10](https://arxiv.org/abs/2205.03854)). Among cognitive architectures, this is the most principled compiler.

**The combinations are unique.** Soar is the only architecture where ([§9.3, p.17](https://arxiv.org/abs/2205.03854)):
- RL learns retrievals from episodic memory (Gorski & Laird, 2011)
- Mental imagery simulates actions to detect collisions that inform RL (Wintermute, 2010)
- Chunking compiles planning into evaluation rules, then RL tunes the initial values (Laird, 2011)
- Episodic memory, metareasoning, and chunking combine for one-shot learning of operator evaluation knowledge (Mohan, 2015)

These emerge from the architecture. The decision cycle, working memory, and the impasse mechanism make them composable.

**Real-time with millions of knowledge elements.** Soar achieves a decision cycle of ~50ms even with millions of rules, facts, and episodes ([§10, item 3, p.18](https://arxiv.org/abs/2205.03854)). The RETE network's incremental matching and episodic memory's delta-based storage keep costs proportional to change, not to total knowledge.

**Demonstrated in real systems.** Over the years, Soar agents have been embodied in real-world robots, computer games, and large-scale distributed simulation environments ([§intro, p.1](https://arxiv.org/abs/2205.03854)). These include:
- **Rosie**: learns new tasks from real-time natural language instruction, acquires task structures interactively, the most capable demonstration of Soar's learning integration ([§10, item 2, p.18](https://arxiv.org/abs/2205.03854); Lindes, 2022)
- **Real-world robots**: over 20 Soar-controlled robots with real-time decision-making, planning, and spatial reasoning via SVS ([§10, item 4, p.18](https://arxiv.org/abs/2205.03854))
- **Large-scale military simulations**: agents incorporating real-time decision-making, planning, natural language understanding, metacognition, theory of mind, and mental imagery ([§intro, p.1](https://arxiv.org/abs/2205.03854); Stearns, 2021)
- **Human behavior modeling**: detailed cognitive models that predict human performance (Schatz et al., 2022)
- Some agents have run uninterrupted for 30 days ([§10, item 9, p.19](https://arxiv.org/abs/2205.03854))

Laird rates Soar on 15 capabilities derived from Newell (1990) and later extensions: 8 as "yes," 5 as "partial," and 2 as "no" ([§10, p.17–20](https://arxiv.org/abs/2205.03854)). These are demonstrated in deployed agents across domains.

### The Decision Cycle (top-level pipeline)

> All five forward phases functional. Elaboration rules compute abstractions and propose operators ([§2.2.1–2.2.2](https://arxiv.org/abs/2205.03854)). Evaluation rules create reject, better/worse, best/worst, and numeric preferences ([§2.2.3](https://arxiv.org/abs/2205.03854)). The fixed [decision procedure](https://soar.eecs.umich.edu/soar_manual/02_TheSoarArchitecture/) processes rejects before ranking, then chooses a single operator or declares an impasse ([§2.3](https://arxiv.org/abs/2205.03854)). Soar supports Q-learning, SARSA, and eligibility traces for numeric preferences ([§5, fn.5](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-decision-cycle.svg" alt="Decision Cycle" style="width:100%; display:block;">
</div>

The elaboration phase fires rules in parallel waves: "a common progression that starts with a wave of elaboration rule firings, followed by a wave of operator proposal, and finally a wave of operator evaluation" ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). Evaluation can't fire until proposals exist. Laird confirmed in correspondence that "the results of this overall phase would be exactly the same if the roles were split and run sequentially." Causally dependent, not explicitly sequenced.

### Symbolic Working Memory (memory)

> Working memory "maintains an agent's situational awareness, including perceptual input, intermediate reasoning results, active goals, hypothetical states, and buffers" ([§1, p.2](https://arxiv.org/abs/2205.03854)). Justification-based truth maintenance ([§2.2, p.5](https://arxiv.org/abs/2205.03854)) provides automatic retraction: I-supported structures retract when their creating rule no longer matches. Working memory doesn't rank and doesn't learn. That's by design.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-working-memory.svg" alt="Working Memory" style="width:100%; display:block;">
</div>

### Procedural Memory (memory)

> The only store with automatic learning. The RETE processes only changes to working memory — "rules fire only once for a specific match to data in working memory (this is called an *instantiation*)" ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). No selection among rules: all matched instantiations fire in parallel. Rules don't compete. Operators do. Chunking ([§4](https://arxiv.org/abs/2205.03854)) and RL ([§5](https://arxiv.org/abs/2205.03854)) both write to this store.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-procedural.svg" alt="Procedural Memory" style="width:100%; display:block;">
</div>

### Semantic Memory (memory)

> Five of six phases functional. Retrieval uses "a combination of base-level activation and spreading activation to determine the best match, as used originally in ACT-R" ([§6, p.12](https://arxiv.org/abs/2205.03854)). Base-level activation biases by recency and frequency; spreading activation biases toward concepts linked to currently active working memory structures. But: "Soar does not have an automatic learning mechanism for semantic memory, but an agent can deliberately store information at any time" ([§6, p.13](https://arxiv.org/abs/2205.03854)). The store grows only by hand or preloading (WordNet, DBpedia). The [implementation](https://soar.eecs.umich.edu/soar_manual/06_SemanticMemory/) has activation-based ranking for retrieval but no eviction. Nothing is ever removed.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-semantic-memory.svg" alt="Semantic Memory" style="width:100%; display:block;">
</div>

### Episodic Memory (memory)

> Five of six phases functional. "A new episode is automatically stored at the end of each decision" ([§7, p.13](https://arxiv.org/abs/2205.03854)). "Soar minimizes the memory overhead of episodic memory by storing only the changes between episodes" ([§7, p.13](https://arxiv.org/abs/2205.03854)). But "memory does grow over time, and the cost to retrieve old episodes slowly increases as the number of episodes grows" ([§7, p.13](https://arxiv.org/abs/2205.03854)). Episodic learning "does not have generalization mechanisms" ([§7, p.13](https://arxiv.org/abs/2205.03854)). The [implementation](https://soar.eecs.umich.edu/soar_manual/07_EpisodicMemory/) confirms it: "The current episodic memory implementation does not implement any episodic store dynamics, such as forgetting." No max-episode count, no eviction policy, no capacity bound. The [source](https://github.com/SoarGroup/Soar/blob/development/Core/SoarKernel/src/episodic_memory/episodic_memory.cpp) declares removal structures (`epmem_id_removal_map`) but never populates them. The store is append-only. At ~50ms per decision cycle, that's 72,000 episodes per hour into an unbounded SQLite store.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-episodic-memory.svg" alt="Episodic Memory" style="width:100%; display:block;">
</div>

### Spatial-Visual System (memory)

> Five forward phases functional. "An agent uses operators to issue commands to SVS that create *filters*" that "automatically extract symbolic properties" ([§8, p.14](https://arxiv.org/abs/2205.03854)). Top-down control of what gets symbolized. "SVS supports hypothetical reasoning...through the ability to *project* non-symbolic structures into SVS" ([§8, p.14](https://arxiv.org/abs/2205.03854)). Laird confirmed in correspondence: "There is filtering at this phase as well." The image memory system is "still experimental" ([§9.2, Figure 6](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-svs.svg" alt="SVS" style="width:100%; display:block;">
</div>

### Chunking (learning)

> Five of six phases functional. Chunking "compiles the processing in a substate into rules that create the substate results" ([§4, p.9](https://arxiv.org/abs/2205.03854)). It "back-traces through the rule that created them" ([§4, p.10](https://arxiv.org/abs/2205.03854)) to find superstate conditions. EBBS — "explanation-based behavior summarization" ([§4, p.10](https://arxiv.org/abs/2205.03854)) — ensures chunks are correct and as general as possible. But "chunking requires that substate decisions be deterministic...Therefore, chunking is not used when decisions are made using numeric preferences" ([§4, p.10](https://arxiv.org/abs/2205.03854)). In the [source](https://github.com/SoarGroup/Soar/blob/development/Core/SoarKernel/src/decision_process/decide.cpp), numeric indifferent preferences are marked with `NOTHING_DECIDER_FLAG`, preventing them from entering the OSK structures that feed chunking.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-chunking.svg" alt="Chunking" style="width:100%; display:block;">
</div>

Laird has the right plan: "We have plans to modify chunking so that such chunks are added to procedural memory when there is sufficient accumulated experience to ensure that they have a high probability of being correct" ([§4, p.10](https://arxiv.org/abs/2205.03854)). Gate chunking on RL convergence. The implementation doesn't exist yet.

### Reinforcement Learning (learning)

> Five of six phases functional. "RL modifies selection knowledge so that an agent's operator selections maximize future reward" ([§5, p.11](https://arxiv.org/abs/2205.03854)). "RL in Soar applies to every active substate," a natural fit for hierarchical RL ([§5, p.12](https://arxiv.org/abs/2205.03854)). Global learning rate and discount rate are "fixed at agent initialization" ([§5, fn.5](https://arxiv.org/abs/2205.03854)). Delta-bar-delta mode adapts per-production learning rates automatically, but the global parameters and exploration strategy are static.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-rl.svg" alt="RL" style="width:100%; display:block;">
</div>

### Semantic Learning (learning)

> Not yet autonomous. Three of six phases are agent-directed, not architectural. "An agent can deliberately store information at any time" ([§6, p.13](https://arxiv.org/abs/2205.03854)) but there's no relevance gating, no prioritization, no self-update. It's a raw `store()` call. Laird himself rates semantic learning as still "missing" among "types of architectural learning" ([§10, item 7, p.18](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-semantic-learning.svg" alt="Semantic Learning" style="width:100%; display:block;">
</div>

### Episodic Learning (learning)

> Automatic but undiscriminating. "A new episode is automatically stored at the end of each decision" ([§7, p.13](https://arxiv.org/abs/2205.03854)). "An agent can further limit the costs of retrievals by explicitly controlling which aspects of the state are stored, usually ignoring frequently changing low-level sensory data" ([§7, p.13](https://arxiv.org/abs/2205.03854)). But no mechanism discriminates which episodes are worth keeping.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-episodic-learning.svg" alt="Episodic Learning" style="width:100%; display:block;">
</div>

## Forward pass works, backward pass doesn't

Every memory module has a functional forward pass. Every learning module is missing its own learning mechanism.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:12em"><col style="width:6em"><col style="width:6em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Stack</th><th style="background:#f0f0f0">Type</th><th style="background:#f0f0f0">Forward pass</th><th style="background:#f0f0f0">Learning</th></tr></thead>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Decision Cycle</a></td><td>Top-level</td><td>Functional</td><td>Partial</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Symbolic Working Memory</a></td><td>Memory</td><td>Functional</td><td>Nil (expected)</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Procedural Memory / RETE</a></td><td>Memory</td><td>Functional</td><td>Functional</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Semantic Memory</a></td><td>Memory</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Episodic Memory</a></td><td>Memory</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">SVS / Perceptual LTM</a></td><td>Memory</td><td>Functional</td><td>Partial</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Chunking</a></td><td style="font-style:italic">Learning</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Reinforcement Learning</a></td><td style="font-style:italic">Learning</td><td>Functional</td><td>Partial (delta-bar-delta)</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Semantic Learning</a></td><td style="font-style:italic">Learning</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Episodic Learning</a></td><td style="font-style:italic">Learning</td><td>Functional</td><td><strong>Missing</strong></td></tr>
</table>

These gaps share a single root cause.

## The forgetting asymmetry

Derbinsky & Laird ([2013](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563)) proved that forgetting is essential to Soar's scaling. Without it, a robot exploring a building exceeded the 50ms decision-cycle threshold within an hour as working memory grew past 12,000 elements. With base-level activation forgetting, working memory stayed at ~2,000 elements and decision time stayed under budget. In Liar's Dice, memory grew as a power law without forgetting, reaching 1,800MB after 40,000 games. With forgetting, it stabilized at ~400MB while maintaining task performance.

They built forgetting for working memory and procedural memory. They never built it for episodic or semantic memory.

The [manual](https://soar.eecs.umich.edu/soar_manual/07_EpisodicMemory/) confirms it: "The current episodic memory implementation does not implement any episodic store dynamics, such as forgetting." The [source](https://github.com/SoarGroup/Soar/blob/development/Core/SoarKernel/src/episodic_memory/episodic_memory.cpp) declares removal structures (`epmem_id_removal_map`) but never populates them. Semantic memory has no forgetting discussion at all. Both stores grow without bound.

This asymmetry is the root cause. Everything else is dominoes.

## The dominoes

**1. Perception stays narrow.** **R4 dictates that the mechanism only removes elements from working memory that augment objects in semantic memory** (Derbinsky & Laird, 2013, §5). You can only safely forget what you can reconstruct. But semantic memory has no automatic learning ([§6, p.13](https://arxiv.org/abs/2205.03854)). It grows only by hand or preloading.

R4 doesn't block perception. Nothing prevents new WMEs from entering working memory. What R4 blocks is the drain: anything perceived outside the semantic vocabulary can't be forgotten, so it accumulates. The RETE scales linearly with WM size (Derbinsky & Laird, 2013, §3). Growing WM pushes decision time past the 50ms threshold. So agents compensate, "usually ignor[ing] frequently changing low-level sensory data" ([§7, p.13](https://arxiv.org/abs/2205.03854)) as a scaling necessity. The bottleneck is at the drain. A clogged drain forces you to close the valve.

Compare:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col style="width:10em"><col style="width:10em"><col style="width:8em"></colgroup>
<thead><tr><th style="background:#f0f0f0">System</th><th style="background:#f0f0f0">Input</th><th style="background:#f0f0f0">Working memory</th><th style="background:#f0f0f0">Compression</th></tr></thead>
<tr><td>Human</td><td>~10 Mbit/s<br><span style="font-size:12px; color:#666">optic nerve, <a href="https://pubmed.ncbi.nlm.nih.gov/16860738/">Koch et al. 2006</a></span></td><td>~200 bits<br><span style="font-size:12px; color:#666">7±2 chunks in WM, <a href="https://psycnet.apa.org/record/1957-02914-001">Miller 1956</a></span></td><td style="font-weight:bold">50,000 : 1</td></tr>
<tr><td>Soar</td><td>pre-symbolized<br><span style="font-size:12px; color:#666">input-link, SVS filters</span></td><td>2,000–12,000 WMEs<br><span style="font-size:12px; color:#666">grows without bound, <a href="https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563">D&L 2013</a></span></td><td style="font-weight:bold">~1 : 1</td></tr>
</table>

The brain's input bandwidth is enormous because its working memory is disciplined. Forgetting is aggressive at every level. [Lateral inhibition](https://doi.org/10.1085/jgp.39.5.651) in the retina compresses ~126 million photoreceptors into ~1.2 million optic nerve fibers before signals leave the eye ([Barlow, 1961](https://en.wikipedia.org/wiki/Efficient_coding_hypothesis)). Only [5–10% of synapses onto thalamic relay cells are retinal](https://doi.org/10.1098/rstb.2002.1161); the rest is cortical feedback and modulatory gating ([Sherman & Guillery, 2002](https://doi.org/10.1098/rstb.2002.1161)). [Sleep consolidation](https://doi.org/10.1038/nrn2762) rewrites cortical representations offline ([Diekelmann & Born, 2010](https://doi.org/10.1038/nrn2762)). Soar's input is narrow because its working memory is not. The architecture pre-symbolizes input and throttles what enters. Real-time performance costs the agent its peripheral vision.

The ceiling is set by the input, and the input is set by the stores' ability to forget.

**2. Semantic memory can't maintain itself.** The working-memory forgetting policy assumes semantic memory is the backup: "forgotten working-memory knowledge may be recovered via deliberate reconstruction from semantic memory" (Derbinsky & Laird, 2013, §5). But the backup itself has no forgetting, no automatic learning, and no capacity bound. It grows only by hand or preloading ([§6, p.13](https://arxiv.org/abs/2205.03854)). The store that everything else depends on for recovery can't shed and can't grow.

This creates a catch-22. Adding eviction to semantic memory undermines the safety of the existing mechanism. Derbinsky & Laird flag the risk: "our forgetting policy does admit a class of reasoning errors wherein the contents of semantic memory are changed so as to be inconsistent with decayed WMEs" (2013, §5.2). Today this is a minor edge case because smem rarely changes. But with automatic learning and eviction, smem changes actively. Every smem deletion can orphan WMEs that were "safely" forgotten from working memory under R4. The WME is gone, its backup is gone, reconstruction fails silently. Making the cold tier dynamic requires coordinating eviction across tiers, a [cache coherence](https://en.wikipedia.org/wiki/Cache_coherence) problem. The existing JTMS handles dependency-driven retraction within working memory; the missing wiring is back-invalidation across the tier boundary.

**3. Chunking and RL can't compose.** "Chunking requires that substate decisions be deterministic...Therefore, chunking is not used when decisions are made using numeric preferences" ([§4, p.10](https://arxiv.org/abs/2205.03854)). That looks like a learning problem, two learning mechanisms that can't talk to each other. It partly is. The composition gap is real regardless of perception: RL-updated rules "encode expected-utility information...and cannot be regenerated if the rule is removed" (Derbinsky & Laird, 2013, §6), while chunked rules *can* be regenerated from substates. Without composition, RL rules can't be safely forgotten, and chunked rules can't incorporate reward. That's a learning problem.

But there's a second, domain-dependent effect. RL converges when it covers enough of the state space. In small, fixed domains — Liar's Dice, structured games — RL converges fine with throttled perception; Derbinsky & Laird's agents reached 75–80% win rates within 10K games (2013, §6.1). In open-ended domains where the state space grows with perceptual scope, throttled perception starves RL of the diversity it needs; decisions stay stochastic longer than necessary; chunking stays locked out. Laird's plan — gate chunking on RL convergence ([§4, p.10](https://arxiv.org/abs/2205.03854)) — is the right mechanism. In fixed domains, convergence happens and the gate opens. In open-ended domains, convergence requires throughput, and throughput is capped by domino 1.

**4. Episodic memory grows without bound.** 72,000 episodes per hour, no eviction, no discrimination, retrieval cost linear in store size. The standard mitigation is to throttle what gets recorded, which circles back to domino 1.

**5. The agent can't bootstrap.** Laird ([§10, p.20](https://arxiv.org/abs/2205.03854)): "What I feel is most missing from Soar is its ability to 'bootstrap' itself up from the architecture and a set of innate knowledge into being a fully capable agent across a breadth of tasks." This is the same class of problem as every other domino: cache invalidation.

When chunking compiles a substate into a production rule, the chunk claims its place in procedural memory and stays. Procedural forgetting uses base-level activation, but activation tracks *invocation*, not *efficacy*. A chunk that fires every cycle on stale pattern matches stays warm; a chunk that would be useful in a novel situation but hasn't been triggered decays. This is a property of the BLA model itself, inherited from ACT-R (Anderson et al., 2004). Soar's chunking makes the consequence acute: chunks that match the old environment crowd the RETE. The agent solves old problems forever.

An efficacy-based activation signal would fix this, but it requires ground truth. RL rules have reward. Chunked rules have substate correctness. Elaboration rules have neither. There's no general "was this firing useful?" signal for a production that proposes an operator that might not get selected. Until such a signal exists, the practical lever is eviction by composition: once RL-gated chunking compiles a converged rule, the RL rule that generated it becomes reconstructible and can be safely forgotten under the existing BLA policy. The practical signal is *reconstructibility*, the same principle behind R4. Prune what you can rebuild.

Rosie learns new tasks from instruction, but only tasks that fit the operator schemas a human pre-built. The perceptual vocabulary is fixed by what's in semantic memory (domino 1), and the procedural vocabulary is fixed by chunks that never expire. Learning without forgetting is maladaptation. The agent either resets manually or calcifies around its early experience.

Forty years of ambition built every module. The one operation that would connect the long-term stores, merging, is still missing. The full assessment and plan are in the [SOAP note](/soap-notes-soar).

## Appendix: Open questions

Questions this diagnosis cannot answer from the paper, manual, or source code alone.

1. **The 30-day agents.** At 72,000 episodes per hour, a 30-day run accumulates ~52 million episodes ([§10, item 9, p.19](https://arxiv.org/abs/2205.03854)). How was retrieval cost managed in practice? Was episodic memory disabled?

2. **Dynamic world, static chunks.** EBBS guarantees chunk correctness relative to the substate reasoning at compile time. In long-running agents with changing environments, have chunks been observed firing incorrectly after environmental change?

3. **Partial evaluation.** Chunking specializes general substate reasoning to known superstate conditions and produces a residual program (the chunk) that runs without interpretation. [Futamura (1971)](https://en.wikipedia.org/wiki/Partial_evaluation) described the same operation for programming languages a decade before Soar. Has the connection been explored?

4. **Capability count.** The paper says "In reviewing these 16 items" ([§10, p.20](https://arxiv.org/abs/2205.03854)) but lists 15 after excluding Newell's constraints 8 and 11–13. Which count is correct?

---

*Diagnosis based on Laird (2022), "[Introduction to the Soar Cognitive Architecture](https://arxiv.org/abs/2205.03854)," and Derbinsky & Laird (2013), "[Effective and efficient forgetting of learned knowledge](https://www.sciencedirect.com/science/article/abs/pii/S1389041712000563)." All section references cite the 2022 paper unless noted. Written via the [double loop](/double-loop).*
