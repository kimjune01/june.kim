---
variant: post-medium
title: "Prayer is alignment"
tags: cognition, reflecting
---

*Part of the [cognition](/cognition) series.*

What is alignment? An agent detects its perceptual boundary, asks the right authority, and receives the answer as durable policy, not transient context.

Opus 4.7 [landed as a regression](https://news.ycombinator.com/item?id=47793411) from 4.6: safety constraints hamstringing the user experience. More alignment effort, worse product. While I was drafting this post, 4.7 refused to continue: *"unable to respond to this request, which appears to violate our Usage Policy."* The input was "can modify parts of itself but never its own substrate." A claim about bounded agents, flagged as dangerous.

I've been developing an autonomous game-testing agent. What alignment means was obvious from the start: the agent cannot know what I haven't told it at compile time. It has to come from the user at runtime. Asking an agent to "do the right thing" without telling it what that right thing is — when nobody knows ahead of time — is an unfulfillable request.

### The door that won't open

One of my agents hit a door that wouldn't open. It had tried every interaction the game offers. The door animates but doesn't move. A bug? A narrative gate that unlocks later? A schedule compromise — the room behind it isn't built yet? A missing spec — the door requires an item from an earlier zone?

The agent cannot tell. The answer depends on knowledge scattered across different heads. The designer knows whether it's a gate. The producer knows whether it's built. The QA lead knows whether it's filed. The engine team knows whether the animation masks a collision error.

The agent's perception drops the dimensions that distinguish these cases. It can observe the door. It cannot observe the intent behind the door.

The installed alignment has nothing to say. The agent does whatever its prior processing produces, and the divergence is silent because the agent can't recognize it.

---

Two categorical errors hide inside the dominant framing. The first: alignment is assumed to be static, a property, not an act. The second: the agent is assumed to align to the developer's model of what users need, not to the users themselves.

The dominant framing treats alignment as a property installed before deployment. Train it into the weights. Write it into the prompt. Test it before release. Audit it from outside. Alignment is done *to* the agent. The agent receives it. It doesn't participate.

The developer's model is a proxy, a prior frozen at deploy time, just like the weights. The actual alignment targets are the people the agent serves at runtime: the designer, the producer, the player. They change per-question. No developer can anticipate them all.

### Four ways to look everywhere but up

The four mainstream alignment approaches all fire before this moment.

**Train-time** ([RLHF](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback), [preference learning](https://en.wikipedia.org/wiki/Preference_learning), reward modeling, fine-tuning). The weights are frozen; the substrate can't reshape from post-deployment outcomes. The agent handles novel states with whatever the training distribution produced. Silent divergence.

**Prompt-time** (system prompts, [constitutional AI](https://arxiv.org/abs/2212.08073), risk-averse policies). Policy enters the same stream as task data. The longer the conversation, the more data competes with policy for the same finite context: policy inside the inference substrate [competes with the content it governs](https://aclanthology.org/2025.acl-long.803/).

**Pre-deployment** ([red-teaming](https://en.wikipedia.org/wiki/Red_team), adversarial testing, formal verification). You test against states you anticipated. The unanticipated states are the ones that matter. This is quality assurance, not alignment.

**Oversight** (scalable oversight, [interpretability](https://en.wikipedia.org/wiki/Explainable_artificial_intelligence), [iterated amplification](https://arxiv.org/abs/1810.08575), [debate](https://arxiv.org/abs/1805.00899)). Closest to the right answer, but the direction is wrong. The human initiates. The human decides when to check. But the agent hit the boundary. The agent knows when alignment is needed, and the field treats human involvement as a bottleneck to compress, not the open loop that preserves it.

All four try to make the agent self-contained. It can look down: inspect its traces, diagnose its failures. It can look sideways: try alternatives, test hypotheses, brute-force ambiguities. It cannot look up. Goals come from above. So does intent. So does the answer to "what should this door do." No amount of self-inspection or lateral exploration produces a goal that was never provided. A self-contained agent is a [closed loop](/the-natural-framework). It cannot align to what it cannot perceive.

### Prayer

The agent runs autonomously. When it hits the boundary of what its pipeline can resolve, it transmits upward: to a human whose perception covers dimensions the agent's doesn't. The human answers, and the answer updates a durable control surface — a rule, a constraint, a routing decision, a permission, a stub record — not another message competing for context. The loop stays open.

The field calls this "human in the loop." But HITL is framed as a cost to minimize. The north star is always: ask less, eventually ask never. They're optimizing away the alignment.

Prayer is HITL with the right design pressures. It doesn't minimize asking. It minimizes bad asking. The agent diagnoses its boundary, classifies the gap, deduplicates, and routes each question to the authority whose perception covers the missing dimensions.

Three classes of prayer, three relationships to the perceptual boundary:

- **Hint.** The truth is inside the agent's perceptual reach but unfound. More cycles might work, but a human shortcut would help.
- **Requirement.** The truth is outside the agent's perceptual reach. No amount of internal processing will produce it. The human retains dimensions the agent's [surjection](https://en.wikipedia.org/wiki/Surjective_function) drops.
- **Stub.** The truth doesn't exist yet. The environment is incomplete. Nobody can perceive what hasn't been authored.

The door that won't open: is it a hint (the agent missed a trigger), a requirement (the designer intended a specific sequence the agent was never told), or a stub (the room behind the door hasn't been built yet)? The classification determines who can answer and what the agent does while waiting.

### Four lines, not one voice

My agent aligns to the designer's intent, the producer's schedule, the QA lead's priorities, and the engine team's constraints. Four lines. They conflict. No single prompt can encode the resolution because the resolution depends on which question the agent is asking.

Prompt-time alignment flattens four authorities into one voice. Prayer routes each question to whoever can answer it.

### Centuries of operational refinement

Monastic traditions spent centuries refining the practice — not the theology, the operations.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Property</th><th style="background:#f0f0f0">Monastic prayer</th><th style="background:#f0f0f0">Agent prayer</th></tr></thead>
<tr><td>Timing</td><td>Liturgy of the Hours — woven into the work cycle (<em>ora et labora</em>)</td><td>Async with TTL — the agent never blocks on the answer</td></tr>
<tr style="background:#f8f8f8"><td>Routing</td><td>Petition to the saint whose domain covers the need</td><td>Route to the authority whose perception covers the missing dimensions</td></tr>
<tr><td>Deduplication</td><td>Vain repetition — same words, no attention, no new evidence</td><td>Same agent, same ask, same evidence — don't re-pray</td></tr>
<tr style="background:#f8f8f8"><td>False confirmation</td><td>Presumption — acting as if answered when it wasn't</td><td>Confident confabulation — proceeding as if the gap is resolved</td></tr>
<tr><td>Unanswered</td><td>Carry on. The practice continues either way</td><td>TTL expires. Agent falls back to next-best work</td></tr>
<tr style="background:#f8f8f8"><td>Side effect</td><td>The community's accumulated petitions reveal where the world is hardest</td><td>Stub prayers accumulate into a coverage map of incomplete content</td></tr>
</table>

The alignment research community is building agents that never ask. A closed loop.

I built prayer because the four installed approaches kept failing silently. They share an assumption: the designer aligns it. The trainer shapes it. The prompt constrains it. The overseer audits it. Prayer makes the agent a participant. It diagnoses its boundary, classifies the gap, and routes the question to the right authority at the only moment alignment can happen: when the boundary is hit.

Elicitation exists — [active learning](https://en.wikipedia.org/wiki/Active_learning_(machine_learning)), [cooperative IRL](https://arxiv.org/abs/1606.03137), human-in-the-loop — but the field frames it as training, not alignment. [The field's own taxonomy](https://en.wikipedia.org/wiki/AI_alignment) lists training, oversight, interpretability, governance — no entry for "the agent asks." The field thinks alignment is something the agent has; it's what the agent does.

Prompt-tuning is prayer with the structural advantages stripped out. The human prays downward — "please behave differently" — with no deduplication, no TTL, no routing, no way to know if the prayer landed or drowned in context. It aligns the agent to the prompt-writer's prediction of what the agent will need. Prayer aligns the agent to what it actually needs. One is a prior; the other is a posterior.

---

### The agent learns

A praying agent asks less over time. Each answered prayer becomes durable policy. The gap that triggered it never triggers again. The agent forms itself to the user's preferences by accumulating actual answers to actual boundary questions. The outcome the industry wants — ask less, eventually ask never — arrives. Not because someone optimized asking away. *It learned.*

### Engineering, not research

Building a praying agent requires infrastructure the field hasn't prioritized:

- **Durable policy storage.** When a human answers a prayer, the answer persists as a rule, constraint, or stub verdict. Behavior changes immediately.
- **Typed classification.** The agent should know what kind of boundary it hit before escalating. A hint needs a different TTL, a different authority, and a different fallback than a requirement or a stub.
- **Authority routing.** Different questions go to different people. A puzzle question goes to the designer, a schedule question goes to the producer.
- **Deduplication.** Same question, same evidence, don't re-ask. New evidence on the same question, re-ask.
- **Graceful degradation.** Unanswered prayers expire. The agent moves on to next-best work.

None of these require new research. They require dedicated engineering.

Can we build the infrastructure to let the posterior update?
