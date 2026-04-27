---
variant: post-medium
title: "Prayer is alignment"
tags: cognition, reflecting
---

*Part of the [cognition](/cognition) series.*

What is alignment? An agent detects its perceptual boundary, asks the right authority, and receives the answer as durable policy, not transient context.

I've been developing an autonomous game-testing agent. What alignment means was obvious from the start: the agent cannot know what I haven't told it at compile time. It has to come from the user at runtime. Asking an agent to "do the right thing" without telling it what that right thing is — when nobody knows ahead of time — is an unfulfillable request.

The dominant framing treats alignment as a property installed before deployment. Train it into the weights. Write it into the prompt. Test it before release. Audit it from outside. Alignment is done *to* the agent. The agent receives it. It doesn't participate.

Two categorical errors hide inside the dominant framing. The first: alignment is assumed to be static, a property, not an act. The second: the agent is assumed to align to the developer's model of what users need, not to the users themselves.

The developer's model is a proxy, a prior frozen at deploy time, just like the weights. The actual alignment targets are the people the agent serves at runtime: the designer, the producer, the player. They change per-question. No developer can anticipate them all.

This works until the agent encounters a state no one anticipated. The installed alignment is silent — nothing to say about a situation it never saw. The agent does whatever its prior processing produces, and the divergence is silent because the agent can't recognize it.

### The door that won't open

One of my agents hit a door that wouldn't open. It had tried every interaction the game offers. The door animates but doesn't move. Is this a bug? Intentional design — a narrative gate that unlocks later? A schedule compromise — the room behind it isn't built yet? A spec the agent never received — the door requires an item from an earlier zone?

The agent cannot tell. The answer depends on knowledge scattered across different heads. The designer knows whether it's a gate. The producer knows whether it's built. The QA lead knows whether it's been filed. The engine team knows whether the animation is masking a collision error.

The agent's perception drops the dimensions that distinguish these cases. It can observe the door. It cannot observe the intent behind the door.

### Four ways to look everywhere but up

The four mainstream alignment approaches all fire before this moment. Each fails for a different structural reason.

**Train-time** ([RLHF](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback), [preference learning](https://en.wikipedia.org/wiki/Preference_learning), reward modeling, fine-tuning). The weights are frozen; the substrate can't reshape from post-deployment outcomes. The agent handles novel states with whatever the training distribution produced. Silent divergence.

**Prompt-time** (system prompts, [constitutional AI](https://arxiv.org/abs/2212.08073), risk-averse policies). Policy enters the same stream as task data. The longer the conversation, the more data competes with policy for the same finite context: policy inside the inference substrate [competes with the content it governs](https://arxiv.org/abs/2307.03172).

**Pre-deployment** ([red-teaming](https://en.wikipedia.org/wiki/Red_team), adversarial testing, formal verification). You test against states you anticipated. The unanticipated states are the ones that matter. This is quality assurance, not alignment.

**Oversight** (scalable oversight, [interpretability](https://en.wikipedia.org/wiki/Explainable_artificial_intelligence), [iterated amplification](https://arxiv.org/abs/1810.08575), [debate](https://arxiv.org/abs/1805.00899)). Closest to the right answer, but the direction is wrong. The human initiates. The human decides when to check. But the agent hit the boundary. The agent knows when alignment is needed, and the field treats human involvement as a bottleneck to compress, not as the open loop that preserves it.

All four try to make the agent self-contained. It can look down: inspect its traces, diagnose its failures. It can look sideways: try alternatives, test hypotheses, brute-force ambiguities. What it cannot do is look up. Goals come from above. So does intent. So does the answer to "what should this door do." No amount of self-inspection or lateral exploration produces a goal that was never provided. A self-contained agent is a [closed loop](/the-natural-framework). It cannot align to what it cannot perceive.

---

### Prayer

The agent runs autonomously. When it hits the boundary of what its pipeline can resolve, it transmits upward: to a human whose perception covers dimensions the agent's doesn't. The human answers, and the answer updates a durable control surface — a rule, a constraint, a routing decision, a permission, a stub record — not another message competing in the context window. The loop stays open.

The field calls this "human in the loop." But HITL is framed as a cost to minimize. The north star is always: ask less, eventually ask never. They're optimizing away the alignment.

Prayer is HITL with the right design pressures. It doesn't minimize asking. It minimizes bad asking. The agent diagnoses its boundary, classifies the gap, deduplicates, and routes each question to the authority whose perception covers the missing dimensions. The human's burden drops not because the agent asks less, but because it asks better.

Prayer differs from HITL structurally:

- HITL asks when confidence is low. Prayer asks when the missing information belongs to another authority's domain.
- HITL treats the human as labeler. Prayer treats the human as policy source, spec author, or dimensional authority.
- HITL returns examples. Prayer returns typed control.

Three classes of prayer, three relationships to the perceptual boundary:

- **Hint.** The truth is inside the agent's perceptual reach but unfound. More cycles might work, but a human shortcut would help.
- **Requirement.** The truth is outside the agent's perceptual reach. No amount of internal processing will produce it. The human retains dimensions the agent's surjection drops.
- **Stub.** The truth doesn't exist yet. The environment is incomplete. Nobody can perceive what hasn't been authored.

The door that won't open: is it a hint (the agent missed a trigger), a requirement (the designer intended a specific sequence the agent was never told), or a stub (the room behind the door hasn't been built yet)? The classification determines who can answer and what the agent does while waiting.

A concrete prayer for the door:

- **Ask:** "Door D12 animates but remains closed after interactions X, Y, Z. Is this intended?"
- **Routed to:** designer (if requirement) or producer (if stub).
- **Answer becomes:** `known_stub`, `requires_item:keycard_b`, `bug:file_collision`, or `do_not_report_until_act_2`.
- **Effect:** the answer updates a durable control surface. Future behavior changes without relying on context memory.

### Four lines, not one voice

My agent aligns to the designer's intent, the producer's schedule, the QA lead's priorities, and the engine team's constraints. Four lines. They conflict. No single prompt can encode the resolution because the resolution depends on which question the agent is asking.

Prompt-time alignment flattens multiple authorities into one document, one voice, one policy. Prayer routes per-question to the authority whose perception covers the relevant dimensions. A requirement about a puzzle solution goes to the designer. A stub about missing geometry goes to the producer. A pre-flight check on a risky action goes to whoever owns the consequences. Authority is diagnosed from the shape of the question, not configured in a file.

I built prayer because the four installed approaches kept failing silently. The dominant approaches share an assumption: alignment is something done *to* the agent. The designer aligns it. The trainer shapes it. The prompt constrains it. The overseer audits it. Prayer makes the agent a participant: it diagnoses its boundary, classifies the gap, formulates the question, and routes it to the right authority at the only moment alignment can be performed: the moment the boundary is hit.

Elicitation exists in the literature — [active learning](https://en.wikipedia.org/wiki/Active_learning_(machine_learning)), [cooperative IRL](https://arxiv.org/abs/1606.03137), human-in-the-loop — but the field frames it as a training technique: get better labels, improve the reward model. Once the substrate is trained, elicitation stops. Runtime asking is rarely framed as alignment itself. [The field's own taxonomy](https://en.wikipedia.org/wiki/AI_alignment) lists training, oversight, interpretability, and governance — no entry for "the agent asks."

The field thinks alignment is something the agent has. It's what the agent does.

### Centuries of operational refinement

Prayer is a runtime alignment protocol for bounded perceivers. You perceive, you process, you hit the boundary of what your pipeline can resolve, and you appeal upward to an entity whose perception covers dimensions yours doesn't. The appeal is async. It may not be answered. You carry on either way.

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

The alignment research community is building agents that don't need to pray. A closed loop.

### What elicitation could become

Elicitation already exists. Active learning, HITL, cooperative IRL. The machinery is there. What's missing is the contract that makes prayer work as alignment rather than training:

- **Cache answers as durable policy.** When a human answers a prayer, the answer persists as a rule, constraint, or stub verdict — not as a training example that reshapes weights offline. The agent's behavior changes immediately and durably. Current HITL feeds answers back into the next training cycle. Prayer feeds them into the current runtime.
- **Classify before asking.** The agent should know what kind of boundary it hit before escalating. A hint needs a different TTL, a different authority, and a different fallback than a requirement or a stub. Current HITL treats every query as the same type: "human, label this."
- **Route by authority.** Different questions go to different people. A puzzle question goes to the designer, a schedule question goes to the producer. Current HITL routes everything to the same labeling pool.
- **Deduplicate.** Same question, same evidence, don't re-ask. New evidence on the same question, re-ask. Current HITL has no memory of what it already asked.
- **Degrade gracefully.** Unanswered prayers expire. The agent moves on to next-best work. Current HITL either blocks until answered or proceeds without the information and doesn't track the gap.

None of these require new research. They require reframing elicitation as a runtime alignment channel rather than a training data pipeline.

Prompt-tuning is prayer with the structural advantages stripped out. Same boundary, wrong direction, unsituated, untyped, policy in the data stream. It's the human praying downward — "please behave differently" — with no deduplication, no TTL, no routing, no way to know if the prayer was answered or just drowned in context.

And it assumes alignment is to the prompt-writer, not to the prayer-answerer. The prompt-writer aligns the agent to their prediction of what the agent will need. The prayer-answerer aligns the agent to what it actually needs. One is a prior; the other is a posterior.
