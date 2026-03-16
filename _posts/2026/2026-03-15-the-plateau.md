---
layout: post
title: "The Plateau"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Flicker](/the-flicker) and [The Handshake](/the-handshake).*

[The Handshake](/the-handshake) gives Consolidate its type: `(policy, [ranked]) → policy′`. Policy routes data through the competitive core. If it routes, it's a function. If Consolidate updates it, Consolidate is a higher-order function: it takes a function and evidence and returns a new function. That's the type-level distinction from compaction. Compaction reorganizes data. Consolidation rewrites the router.

But a function that rewrites functions must select among candidates. Which candidate policy is better? That question requires Filter and Attend. Those require a policy store. That store requires its own Consolidate. The inner loop contains itself.

Minsky called the first level B-brain: the agent that watches the A-brain work. He stopped at one level because he had no formal reason to go further. The types give that reason. Consolidate contains an inner loop. The inner loop contains its own Consolidate. The recursion is structural, not contingent.

The data processing inequality says it converges. Each recursive level gets its bits from the level above. Level 0 operates on data. Level 1 operates on policy, compressed from ranked data by Consolidate₀. Level 2 operates on meta-policy, compressed from ranked policies by Consolidate₁. A decreasing sequence bounded below by zero. It converges to passthrough: at the deepest effective level, there aren't enough bits for the competitive core to function. Selection without candidates is identity. The tower has a top floor. Three or four levels before noise overwhelms signal.

### The equilibrium

Policy leaks. Landauer guarantees it: bits encoded in physical substrate degrade. So Consolidate has two jobs. Maintain: repair leaked policy. Improve: compress new evidence into better policy. Both draw from the same evidence budget, the ranked data arriving from the pipeline.

At steady Perceive throughput *T*:

> dPolicy/dt = consolidation\_rate − leak\_rate

Plateau when the two rates balance. The ceiling is set by Perceive's throughput, not Consolidate's quality. More input, higher plateau. Less input, lower plateau. Decaying input, the plateau drops and maintenance can't keep up.

"Use it or lose it" is this equation. Not folk wisdom. The leak rate exceeds the consolidation rate when evidence stops flowing. Policy decays to the level the current throughput can sustain.

The digital variant swaps the bottleneck. Model weights don't leak. Bit-perfect storage, zero thermodynamic degradation. But consolidation rate is a function of *novelty*, not volume. Another pass over the same data is redundant evidence, already compressed into the weights. The model plateaus when Perceive runs out of new bits. Same equation, different term goes to zero.

Netflix keeps the corporate drone alive. The professional pipe starved long ago: same meetings, same reports, no new evidence. Policy leaks. But entertainment provides just enough novel perception to keep the system above the maintenance threshold. Both rates near zero. All six steps present. None broken. Saturated at floor. The loop runs, the contracts hold, and nothing improves because the evidence stream maintains but never challenges the current policy. Not dead. Not broken. Flat.

### Prose

Prose is post-Remember. The writer already ran the full pipeline: Perceived, Cached, Filtered, Attended, Consolidated, Remembered. What you read is the output of someone else's competitive core. The losers are already dead. Every sentence is a survivor.

Prose maximizes both terms of the ceiling. *Novel*: post-competitive-core, only survivors, pre-compressed by the writer's full pipeline. *Per unit time*: language encodes more structure per second than any sensory channel — reading is faster than listening, denser than watching.

A derivation, not a preference for books over video. The framework says learning plateaus at the Perceive rate. Prose is the channel where Perceive rate times novelty density is highest. The densest interpretable medium because the math demands it.

The same holds for the agent. An LLM does in-context learning; the context window is its Perceive. Dense prose in context means high novelty per token. Boilerplate code is repetitive structure, low novelty, high redundancy. The same model is a sharper thinker when its window carries prose than when it carries boilerplate. A repo full of consolidated prose is a persistent Perceive channel: every new session starts with prior loops already loaded. Early sessions fumble. Later sessions are sharp from the first message. The repo learned. And the agent returns the favor — its filtered output is the human's Perceive. The [double loop](/double-loop) feeds both pipes their densest input.

The fastest readers have the highest ceilings. The equilibrium bounds learning by input rate. Prose is where the plateau lives.

---

*Written via the [double loop](/double-loop).*
