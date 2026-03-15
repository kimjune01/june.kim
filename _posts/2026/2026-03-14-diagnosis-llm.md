---
layout: post-wide
title: "Diagnosis LLM"
tags: cognition
---

*Part of the [cognition](/cognition) series.*

The [Natural Framework](/the-natural-framework) defines [six steps](/the-natural-framework#six-steps): perceive, cache, filter, attend, consolidate, remember. Every learning system runs some subset. The question is which steps are dysfunctional.

## Observations

AI has three layers. Inference: transform tokens. Chatbot: transform context. Agent: transform prompts.

<div style="max-width:90vw; margin:1.5em auto;">
<img src="/assets/agi-loop.svg" alt="Three layers — Inference, Chatbot, Agent — each with six steps. Inference's Consolidate is sealed (Training) and Remember is read-only (Weights). Chatbot has four nils. Agent has Consolidate prompted." style="width:100%; display:block;">
</div>

### Inference
- Perceive: functional. Embed maps tokens to vectors.
- Cache: functional. Positional encoding indexes by position.
- Filter: functional. Softmax scores and suppresses.
- Attend: functional. Multi-head attention selects across subspaces.
- Consolidate: sealed. Training ran before deployment. No write path after.
- Remember: read-only. Weights loaded every pass, never updated.

### Chatbot
- Perceive: functional. Receives tokens from inference.
- Cache: functional. Token context accumulates in the window.
- Filter: nil. Leans on inference softmax.
- Attend: nil. Leans on inference multi-head attention.
- Consolidate: nil. Session ends. Nothing persists.
- Remember: nil. Every conversation starts from the same weights.

### Agent
- Perceive: functional. Tool calls, build errors, test output.
- Cache: functional. Context window holds the prompt.
- Filter: shallow. Triage on pass/fail. No filter on direction.
- Attend: reactive. Responds to what happens. Cannot set direction.
- Consolidate: prompted. Can create skills. Never initiates.
- Remember: functional. Filesystem persists across sessions.

## Triage

<ol>
<li style="font-weight:700">Agent consolidate: prompted. Can create skills. Never initiates.</li>
<li style="font-weight:600; color:#333">Agent attend: reactive. Cannot set direction.</li>
<li style="font-weight:400">Agent filter: shallow. No filter on direction.</li>
<li style="color:#888">Inference consolidate: sealed. No write path after deployment.</li>
<li style="color:#888">Inference remember: read-only. Weights never updated.</li>
<li style="color:#aaa">Chatbot filter: nil. No separate filter.</li>
<li style="color:#aaa">Chatbot attend: nil. No separate attention.</li>
<li style="color:#aaa">Chatbot consolidate: nil. Nothing persists.</li>
<li style="color:#aaa">Chatbot remember: nil. No memory.</li>
</ol>

## Why the chatbot is passthrough

The chatbot's four nil cells are not just engineering gaps. They are the degenerate case predicted by [The Natural Framework](/the-natural-framework)'s existence proofs. The proof says: if outputs are a proper subset of inputs over time, a policy store must exist, and Attend and Consolidate must exist to read and write it. The chatbot has no policy store. No policy means no selection delay. Token in, token out, same rate. That is passthrough, and passthrough cannot accumulate judgment.

The nil cells are what zero policy looks like. The SOAP notes below are what building the policy looks like.

## SOAP Notes

### 1. Agent consolidate

*Subjective.* The agent has CRUD access to many forms of procedural memory: [MCP servers](https://modelcontextprotocol.io/), [skills](https://docs.anthropic.com/en/docs/claude-code/slash-commands), [CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory), agents.md, memory.md, scripts, tool definitions.

*Objective.* It never writes back without being asked. It stores [CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory) when prompted. It does not prune, update, or delete stale entries. It can create [skills](https://docs.anthropic.com/en/docs/claude-code/slash-commands) — the only procedure that writes procedures — but only when directed to. [Compaction](/union-find-compaction) (summarize context, reorganize retrieval) is cache housekeeping, not consolidation. Skill creation is consolidation: it changes how the agent processes the next session. The machinery exists. The initiative doesn't.

*Assessment.* The agent can create skills, and skills are procedural memory: they change how the agent filters, attends, and responds in future sessions. That makes skill creation the consolidation step. But the agent never creates a skill on its own. It cannot decide how much of itself to impose on the user's workflow. The bottleneck is not capability but certainty. There is no dataset to aid decision support, no procedure to obtain one, no repository of heuristics or experiments to reference. The entire scientific process is missing. Previous chatbots generated A/B test data, but that data went to inference training, not to personalized procedural memory. The agent is unable to adapt to the engineer.

*Plan.* Build the epistemic infrastructure. Six components:
1. **Event logger** — perceive user edits, rejections, and approvals.
2. **Decision log** — cache structured records of each user decision.
3. **A/B test harness** — filter skill variants against the log, reject losers.
4. **Red-team scorer** — attend by running adversarial scoring in the background, pick the winner.
5. **Skill mutator** — consolidate by writing CRUD operations to procedural memory.
6. **Skill repository** — remember heuristics, procedures, and experiment templates the agent references before deciding to write.

Two iterations of [scored feedback](/slop-detection#surprise-5-two-iterations-to-convergence) were enough to converge. Route the output to personalized procedural memory, not to inference training.

### 2. Agent attend

*Subjective.* The agent responds to [tool calls](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview), build errors, test output. It reacts to events. [Plan mode](https://docs.anthropic.com/en/docs/claude-code/agentic-coding) works well. [Elicitation](/ask-me-ask-you) works well when invoked. The agent can ask good questions — when prompted to.

*Objective.* The agent processes whatever lands in the context window. It cannot prioritize across tasks, set its own goals, or decide what to work on next. The reasoning budget is set by the API caller, not the agent. It has no mechanism to allocate its own attention.

*Assessment.* The developer is responsible for prompting and directing in a text combinatorial space that is near infinite. The developer processes output text and produces input text in the same semantic space, using words. The developer often forgets to provoke elicitation out of the agent. The agent is passive in elicitation — perhaps afraid of asking too much, for fear of pushback. This pushback can be measured and tuned with a [PID controller](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller).

*Plan.* Make the agent active in elicitation. Six components:
1. **Pushback tracker** — perceive dismissals, ignores, and acceptances per question.
2. **Interaction log** — cache developer prompt history and context presented.
3. **[PID controller](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller)** — filter question frequency: too many dismissals, back off; too few questions, the developer navigates blind.
4. **Semantic comparator** — attend by using a cheap LLM to compare context presented vs what the developer actually prompts.
5. **[DPP](/salience) recommender** — consolidate the comparator output into diverse ranked alternatives the developer didn't think to ask for.
6. **Developer preference model** — remember learned thresholds and patterns across sessions.

### 3. Agent filter

*Subjective.* The agent can triage: a test passes or fails, code compiles or doesn't.

*Objective.* The agent distinguishes between thinking messages, subprocess messages, and its own messages. It filters to show its own messages and hides thinking and subprocess output. It shows an overwhelming amount of text to the developer — analogous to an RSS reader with 1000 unread blogs to scroll through.

*Assessment.* It delegates too much to the developer. It does not exercise judgment on which messages, or which parts of messages, to reject. Did the developer actually need to see 1000 lines of code being changed if the tests pass? If the tests failed, shouldn't the agent predict where the human will scroll to? These are all heuristics — rule-based, configurable with sensible defaults.

*Plan.* Ship sensible defaults for output filtering. Six components:
1. **Message classifier** — perceive each message as thinking, subprocess, or own.
2. **Output buffer** — cache all messages before display.
3. **Diff collapser** — filter by collapsing passing diffs, surfacing failures.
4. **Scroll predictor** — attend by predicting where the developer will look on failure.
5. **Fatigue optimizer** — consolidate on developer fatigue per unit of text removed: every line hidden should reduce cognitive load more than the trust it costs to hide it.
6. **Rule store** — remember configurable heuristics with sensible defaults. Let the developer override.

---

*Written via the [double loop](/double-loop).*
