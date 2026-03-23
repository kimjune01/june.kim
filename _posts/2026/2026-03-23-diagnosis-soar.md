---
layout: post-wide
title: "Diagnosis: Soar"
tags: cognition
---

*Part of the [cognition](/cognition) series. Applies the diagnostic from [Diagnosis LLM](/diagnosis-llm) to the [Soar cognitive architecture](https://soar.eecs.umich.edu/).*

Soar is among the most ambitious artifacts in computer science. Where most AI research optimizes a single capability, John Laird and his collaborators spent forty years building the whole mind — taking Allen Newell's challenge literally, designing a unified theory of cognition as a working program ([Laird, 2022, §intro](https://arxiv.org/abs/2205.03854)). The result is an architecture of extraordinary internal coherence: every module earns its place, every mechanism connects to the others through a single central hub, and the decision cycle elegantly stages parallel rule firing into sequential action.

The [Natural Framework](/the-natural-framework) offers a second opinion — not on whether Soar works (it does, remarkably well), but on where the architecture's own growth edges are.

The diagnosis is based on Laird's [2022 introduction](https://arxiv.org/abs/2205.03854), the [Gentle Introduction](https://web.eecs.umich.edu/~soar/sitemaker/docs/misc/GentleIntroduction-2006.pdf) (Lehman, Laird, & Rosenbloom, 2006), and correspondence with Laird.

## Observations

Soar is not one pipeline. It is a set of interacting task-independent modules ([§1, p.2](https://arxiv.org/abs/2205.03854)). Figure 1 of Laird (2022) shows the structure: four memories (Procedural, Semantic, Episodic, Symbolic Working Memory), four learning modules (Chunking, RL, Semantic Learning, Episodic Learning), three processing components (Preference Memory, Decision Procedure, Operator selection), the Spatial-Visual System, and Embodiment (Perception, Motor).

Each module is its own stack with its own six roles. The decision cycle is the top-level pipeline that orchestrates them. Diagnosing Soar means diagnosing each stack individually.

<div style="max-width:90vw; margin:1.5em auto;">
<img src="/assets/soar-composition.svg" alt="Soar composition diagram" style="width:80%; display:block; margin:0 auto;">
</div>

### The Decision Cycle (top-level pipeline)

> All five forward roles functional. Elaboration rules compute abstractions and propose operators ([§2.2.1–2.2.2](https://arxiv.org/abs/2205.03854)). Evaluation rules create better/worse/best/worst/numeric preferences ([§2.2.3](https://arxiv.org/abs/2205.03854)); the fixed decision procedure processes rejections first, ranks survivors only if needed ([§2.3](https://arxiv.org/abs/2205.03854)). Soft-max available for numeric preferences ([§5, fn.5](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-decision-cycle.svg" alt="Decision Cycle" style="width:100%; display:block;">
</div>

The elaboration phase fires rules in parallel waves — "a common progression that starts with a wave of elaboration rule firings, followed by a wave of operator proposal, and finally a wave of operator evaluation" ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). These waves are causally dependent: evaluation can't fire until proposals exist. Laird confirmed in correspondence that "the results of this overall phase would be exactly the same if the roles were split and run sequentially." The framework predicts staging; Soar implements it through causal dependencies. Same result, different mechanism.

### Symbolic Working Memory (Cache stack)

> Healthy Cache. Working memory "maintains an agent's situational awareness, including perceptual input, intermediate reasoning results, active goals, hypothetical states, and buffers" ([§1, p.2](https://arxiv.org/abs/2205.03854)). Justification-based truth maintenance ([§2.2, p.5](https://arxiv.org/abs/2205.03854)) is a well-designed Filter: I-supported structures retract automatically when their creating rule no longer matches. The nil cells are expected — Cache doesn't rank, Cache doesn't learn.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-working-memory.svg" alt="Working Memory" style="width:100%; display:block;">
</div>

### Procedural Memory (Cache stack)

> The only store with a functional Consolidate. The RETE processes only changes to working memory — "rules fire only once for a specific match to data in working memory (this is called an *instantiation*)" ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). The nil Attend is correct by design: all matched instantiations fire in parallel. Rules don't compete. Operators do. Chunking ([§4](https://arxiv.org/abs/2205.03854)) and RL ([§5](https://arxiv.org/abs/2205.03854)) both write to this store.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-procedural.svg" alt="Procedural Memory" style="width:100%; display:block;">
</div>

### Semantic Memory (Cache stack)

> Five of six cells functional. Retrieval uses "a combination of base-level activation and spreading activation to determine the best match, as used originally in ACT-R" ([§6, p.12](https://arxiv.org/abs/2205.03854)). Base-level activation biases by recency and frequency; spreading activation biases toward concepts linked to currently active working memory structures. But: "Soar does not have an automatic learning mechanism for semantic memory, but an agent can deliberately store information at any time" ([§6, p.13](https://arxiv.org/abs/2205.03854)). The store grows only by hand or preloading (WordNet, DBpedia).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-semantic-memory.svg" alt="Semantic Memory" style="width:100%; display:block;">
</div>

### Episodic Memory (Cache stack)

> Five of six cells functional. "A new episode is automatically stored at the end of each decision" ([§7, p.13](https://arxiv.org/abs/2205.03854)). "Soar minimizes the memory overhead of episodic memory by storing only the changes between episodes" ([§7, p.13](https://arxiv.org/abs/2205.03854)). But "memory does grow over time, and the cost to retrieve old episodes slowly increases as the number of episodes grows" ([§7, p.13](https://arxiv.org/abs/2205.03854)). Episodic learning "does not have generalization mechanisms" ([§7, p.13](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-episodic-memory.svg" alt="Episodic Memory" style="width:100%; display:block;">
</div>

### Spatial-Visual System (Cache stack)

> Five forward cells functional. "An agent uses operators to issue commands to SVS that create *filters*" that "automatically extract symbolic properties" ([§8, p.14](https://arxiv.org/abs/2205.03854)) — top-down control of what gets symbolized. "SVS supports hypothetical reasoning...through the ability to *project* non-symbolic structures into SVS" ([§8, p.14](https://arxiv.org/abs/2205.03854)). Laird confirmed in correspondence: "There is filtering at this phase as well." The image memory system is "still experimental" ([§9.2, Figure 6](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-svs.svg" alt="SVS" style="width:100%; display:block;">
</div>

### Chunking (Consolidate stack)

> Five of six cells functional. Chunking "compiles the processing in a substate into rules that create the substate results" ([§4, p.9](https://arxiv.org/abs/2205.03854)). It "back-traces through the rule that created them" ([§4, p.10](https://arxiv.org/abs/2205.03854)) to find superstate conditions. EBBS — "explanation-based behavior summarization" ([§4, p.10](https://arxiv.org/abs/2205.03854)) — ensures chunks are correct and as general as possible. But "chunking requires that substate decisions be deterministic...Therefore, chunking is not used when decisions are made using numeric preferences" ([§4, p.10](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-chunking.svg" alt="Chunking" style="width:100%; display:block;">
</div>

Laird has the right plan: "We have plans to modify chunking so that such chunks are added to procedural memory when there is sufficient accumulated experience to ensure that they have a high probability of being correct" ([§4, p.10](https://arxiv.org/abs/2205.03854)). Gate chunking on RL convergence. The implementation doesn't exist yet.

### Reinforcement Learning (Consolidate stack)

> Five of six cells functional. "RL modifies selection knowledge so that an agent's operator selections maximize future reward" ([§5, p.11](https://arxiv.org/abs/2205.03854)). "RL in Soar applies to every active substate" — hierarchical RL is a natural fit ([§5, p.12](https://arxiv.org/abs/2205.03854)). But "it has parameters for learning rates and discount rates, which are fixed at agent initialization" ([§5, fn.5](https://arxiv.org/abs/2205.03854)). RL does not tune its own hyperparameters.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-rl.svg" alt="RL" style="width:100%; display:block;">
</div>

### Semantic Learning (Consolidate stack)

> The weakest stack. Three of six cells missing. "An agent can deliberately store information at any time" ([§6, p.13](https://arxiv.org/abs/2205.03854)) but there's no relevance gating, no prioritization, no self-update. It's a raw `store()` call. Laird himself rates semantic learning as still "missing" among "types of architectural learning" ([§10, item 7, p.18](https://arxiv.org/abs/2205.03854)).

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-semantic-learning.svg" alt="Semantic Learning" style="width:100%; display:block;">
</div>

### Episodic Learning (Consolidate stack)

> Automatic but undiscriminating. "A new episode is automatically stored at the end of each decision" ([§7, p.13](https://arxiv.org/abs/2205.03854)). "An agent can further limit the costs of retrievals by explicitly controlling which aspects of the state are stored, usually ignoring frequently changing low-level sensory data" ([§7, p.13](https://arxiv.org/abs/2205.03854)). But no mechanism discriminates which episodes are worth keeping.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/soar-episodic-learning.svg" alt="Episodic Learning" style="width:100%; display:block;">
</div>

## What Soar gets right

Before diagnosing the gaps, it's worth naming what the architecture achieves that no competitor matches.

**The impasse mechanism is a work of engineering.** When knowledge is insufficient to select or apply an operator, Soar doesn't crash or randomize — it creates a substate and reasons about the gap ([§3, p.7](https://arxiv.org/abs/2205.03854)). The same decision cycle runs recursively in the substate, with full access to all reasoning and memory capabilities. This single mechanism unifies planning, hierarchical task decomposition, metacognition, and deliberate operator evaluation without separate meta-processing modules ([§3.3, p.9](https://arxiv.org/abs/2205.03854)). Most architectures bolt these on. Soar derives them.

**The decision cycle stages Filter before Attend without naming them.** Elaboration rules fire in causally dependent waves — elaboration, then proposal, then evaluation ([§2.2, p.5](https://arxiv.org/abs/2205.03854)). The decision procedure processes reject preferences first; if sufficient, it stops without ranking ([§2.3, p.6](https://arxiv.org/abs/2205.03854)). This is the staging the Natural Framework predicts, achieved through causal dependencies rather than separate phases. The architecture arrived at the right answer by engineering, not by theory.

**Chunking is the cleanest backward pass in any cognitive architecture.** It backtraces through the dependency chain, identifies which superstate conditions were necessary, and writes a production rule that fires directly next time ([§4, p.9–10](https://arxiv.org/abs/2205.03854)). Deliberation compiles into reaction. EBBS ensures the learned rule is correct relative to the substate reasoning and as general as possible without being over-general ([§4, p.10](https://arxiv.org/abs/2205.03854)). No other architecture has a compiler this principled.

**The combinations are unique.** Soar is the only architecture where ([§9.3, p.17](https://arxiv.org/abs/2205.03854)):
- RL learns retrievals from episodic memory (Gorski & Laird, 2011)
- Mental imagery simulates actions to detect collisions that inform RL (Wintermute, 2010)
- Chunking compiles planning into evaluation rules, then RL tunes the initial values (Laird, 2011)
- Episodic memory, metareasoning, and chunking combine for one-shot learning of operator evaluation knowledge (Mohan, 2015)

These aren't individual features. They're emergent from the architecture — the decision cycle, working memory, and the impasse mechanism make them composable.

**Real-time with millions of knowledge elements.** Soar achieves a decision cycle of ~50ms even with millions of rules, facts, and episodes ([§10, item 3, p.18](https://arxiv.org/abs/2205.03854)). The RETE network's incremental matching and episodic memory's delta-based storage keep costs proportional to change, not to total knowledge.

**Demonstrated in real systems, not just toy domains.** Over the years, Soar agents have been embodied in real-world robots, computer games, and large-scale distributed simulation environments ([§intro, p.1](https://arxiv.org/abs/2205.03854)). These include:
- **Rosie**: learns new tasks from real-time natural language instruction, acquires task structures interactively, the most capable demonstration of Soar's learning integration ([§10, item 2, p.18](https://arxiv.org/abs/2205.03854); Lindes, 2022)
- **Real-world robots**: over 20 Soar-controlled robots with real-time decision-making, planning, and spatial reasoning via SVS ([§10, item 4, p.18](https://arxiv.org/abs/2205.03854))
- **Large-scale military simulations**: agents incorporating real-time decision-making, planning, natural language understanding, metacognition, theory of mind, and mental imagery ([§intro, p.1](https://arxiv.org/abs/2205.03854); Stearns, 2021)
- **Human behavior modeling**: detailed cognitive models that predict human performance (Schatz et al., 2022)
- Some agents have run uninterrupted for 30 days ([§10, item 9, p.19](https://arxiv.org/abs/2205.03854))

Laird rates Soar on 16 capabilities derived from Newell (1990): 8 as "yes," 5 as "partial," and 2 as "no" ([§10, p.20](https://arxiv.org/abs/2205.03854)). These aren't aspirational — they are demonstrated in deployed agents across domains.

The forward pass works. The question is the backward pass.

## The pattern

Every Cache stack has a functional forward pass. Every Consolidate stack is missing its own Consolidate.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:12em"><col style="width:6em"><col style="width:6em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Stack</th><th style="background:#f0f0f0">Type</th><th style="background:#f0f0f0">Forward pass</th><th style="background:#f0f0f0">Consolidate</th></tr></thead>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Decision Cycle</a></td><td>Top-level</td><td>Functional</td><td>Partial</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Symbolic Working Memory</a></td><td>Cache</td><td>Functional</td><td>Nil (expected)</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Procedural Memory / RETE</a></td><td>Cache</td><td>Functional</td><td>Functional</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Semantic Memory</a></td><td>Cache</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Episodic Memory</a></td><td>Cache</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">SVS / Perceptual LTM</a></td><td>Cache</td><td>Functional</td><td>Partial</td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Chunking</a></td><td style="font-style:italic">Consolidate</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Reinforcement Learning</a></td><td style="font-style:italic">Consolidate</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Semantic Learning</a></td><td style="font-style:italic">Consolidate</td><td>Functional</td><td><strong>Missing</strong></td></tr>
<tr><td><a href="https://arxiv.org/abs/2205.03854">Episodic Learning</a></td><td style="font-style:italic">Consolidate</td><td>Functional</td><td><strong>Missing</strong></td></tr>
</table>

Procedural memory is the only store with a functional backward pass. Chunking and RL both write to it. Semantic memory, episodic memory, and perceptual LTM have no automatic learning mechanism that writes back to them.

This is Laird's own assessment ([§10, p.20](https://arxiv.org/abs/2205.03854)): "What I feel is most missing from Soar is its ability to 'bootstrap' itself up from the architecture and a set of innate knowledge into being a fully capable agent across a breadth of tasks." The framework names the gap: every Consolidate stack is missing its own Consolidate. The inner loops work. The outer loop doesn't exist.

## Triage

<ol>
<li style="font-weight:700">Semantic Memory has no backward pass. The most important store grows only by hand. <a href="https://arxiv.org/abs/2205.03854">§6, p.13</a></li>
<li style="font-weight:600; color:#333">Episodic Memory has no generalization. The write-ahead log never compacts. <a href="https://arxiv.org/abs/2205.03854">§7, p.13</a></li>
<li style="font-weight:400">Chunking cannot compose with RL. The determinism requirement walls off stochastic selection from the compiler. <a href="https://arxiv.org/abs/2205.03854">§4, p.10</a></li>
<li style="font-weight:400">Semantic Learning is three-sixths missing. No filter, no attend, no consolidate. <a href="https://arxiv.org/abs/2205.03854">§6</a>; <a href="https://arxiv.org/abs/2205.03854">§10, p.18</a></li>
<li style="color:#888">Episodic Learning records without discrimination. <a href="https://arxiv.org/abs/2205.03854">§7, p.13</a></li>
<li style="color:#888">RL does not tune itself. Fixed hyperparameters. <a href="https://arxiv.org/abs/2205.03854">§5, fn.5</a></li>
<li style="color:#aaa">Forward pass at every level: functional. No action needed.</li>
</ol>

## SOAP Notes

### 1. Semantic Memory consolidation

*Subjective.* Semantic memory "encodes facts that an agent 'knows' about itself and the world" and "serves as a knowledge base that encodes general context-independent world knowledge, but also specific knowledge about an agent's environment, capabilities, and long-term goals" ([§6, p.12](https://arxiv.org/abs/2205.03854)). Retrieval uses activation from ACT-R ([§6, p.12](https://arxiv.org/abs/2205.03854)).

*Objective.* "Soar does not have an automatic learning mechanism for semantic memory, but an agent can deliberately store information at any time" ([§6, p.13](https://arxiv.org/abs/2205.03854)). Can be "initialized with knowledge from existing curated knowledge bases (such as WordNet or DBpedia) and/or built up incrementally by the agent during its operations" ([§6, p.13](https://arxiv.org/abs/2205.03854)). Base-level activation metadata updates automatically, but this biases retrieval — it doesn't create new knowledge.

*Assessment.* Semantic memory is a database with no ETL pipeline. The retrieval engine is sophisticated (activation-based, context-sensitive). The ingestion path is a raw INSERT. The missing piece is the batch job that reads from episodic memory (the event log) and writes regularities to semantic memory (the knowledge base). Laird acknowledges semantic learning is still "missing" among architectural learning types ([§10, item 7, p.18](https://arxiv.org/abs/2205.03854)).

*Plan.* An episodic-to-semantic consolidation module:
1. **Trigger**: idle time, goal completion, or episode accumulation threshold.
2. **Read**: query EPMEM for recent episodes within a context window.
3. **Detect**: find co-occurring structures, recurring operator sequences, stable features across episodes.
4. **Write**: create new SMEM graph structures encoding the detected regularities.
5. **Verify**: on next retrieval, check the generalization against new episodes. Decay activation on generalizations that don't match.

### 2. Chunking–RL composition

*Subjective.* Chunking "is a learning mechanism that converts deliberate, sequential reasoning into parallel rule firings" ([§4, p.9](https://arxiv.org/abs/2205.03854)). RL "modifies selection knowledge so that an agent's operator selections maximize future reward" ([§5, p.11](https://arxiv.org/abs/2205.03854)). Together they should cover the full learning space.

*Objective.* "Chunking requires that substate decisions be deterministic so that they will always create the same result. Therefore, chunking is not used when decisions are made using numeric preferences" ([§4, p.10](https://arxiv.org/abs/2205.03854)). The two mechanisms share working memory but their learning products don't feed each other.

*Assessment.* Laird has the right plan: "We have plans to modify chunking so that such chunks are added to procedural memory when there is sufficient accumulated experience to ensure that they have a high probability of being correct" ([§4, p.10](https://arxiv.org/abs/2205.03854)). Gate chunking on RL convergence. This is one Consolidate stack reading from another's output.

The deeper issue is that Chunking has no backward pass on itself. EBBS ([§4, p.10](https://arxiv.org/abs/2205.03854)) improved chunk quality but doesn't prune the chunk store. Chunks accumulate.

*Plan.* Two changes:
1. **RL-gated chunking**: as Laird describes, allow chunking when RL preferences converge below a variance threshold.
2. **Chunk review**: periodically evaluate chunk utility. Chunks that never fire can be retracted. This is Consolidate for the Consolidate stack.

### 3. Episodic discrimination

*Subjective.* "A new episode is automatically stored at the end of each decision" ([§7, p.13](https://arxiv.org/abs/2205.03854)). Agents can "limit the costs of retrievals by explicitly controlling which aspects of the state are stored" ([§7, p.13](https://arxiv.org/abs/2205.03854)).

*Objective.* At ~50ms per decision cycle ([§10, item 3, p.18](https://arxiv.org/abs/2205.03854)), that's 20 episodes per second, 72,000 per hour. "The cost to retrieve old episodes slowly increases as the number of episodes grows, whereas the time to retrieve recent episodes remains constant" ([§7, p.13](https://arxiv.org/abs/2205.03854)). Episodic learning "does not have generalization mechanisms" ([§7, p.13](https://arxiv.org/abs/2205.03854)).

*Assessment.* The missing cell is Attend. An importance signal — computed from reward, impasse resolution, or state novelty — would let the agent record high-value episodes at full fidelity and routine episodes at reduced fidelity or not at all.

*Plan.* Add an importance gate to Episodic Learning:
1. **Novelty detector**: compare current state to recent episodes. High delta = novel = worth recording.
2. **Reward proximity**: episodes near reward events get full fidelity.
3. **Impasse resolution**: episodes where an impasse was resolved contain the reasoning that worked.
4. **Routine suppression**: states that match recent episodes within a similarity threshold are skipped or stored at reduced fidelity.

---

*Diagnosis based on Laird (2022), "[Introduction to the Soar Cognitive Architecture](https://arxiv.org/abs/2205.03854)." All section references cite this paper unless noted as correspondence. Written via the [double loop](/double-loop).*
