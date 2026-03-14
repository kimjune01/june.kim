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
<img src="/assets/agi-loop.svg" alt="Three layers — Inference, Chatbot, Agent — each with six steps. Inference's Consolidate is sealed (Training) and Remember is read-only (Weights). Chatbot has four nils. Agent has Consolidate nil." style="width:100%; display:block;">
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
- Consolidate: nil. Has machinery. No initiative.
- Remember: functional. Filesystem persists across sessions.

## Triage

<ol>
<li style="font-weight:700">Agent consolidate: nil. Has machinery. No initiative.</li>
<li style="font-weight:600; color:#333">Agent attend: reactive. Cannot set direction.</li>
<li style="font-weight:400">Agent filter: shallow. No filter on direction.</li>
<li style="color:#888">Inference consolidate: sealed. No write path after deployment.</li>
<li style="color:#888">Inference remember: read-only. Weights never updated.</li>
<li style="color:#aaa">Chatbot filter: nil. No separate filter.</li>
<li style="color:#aaa">Chatbot attend: nil. No separate attention.</li>
<li style="color:#aaa">Chatbot consolidate: nil. Nothing persists.</li>
<li style="color:#aaa">Chatbot remember: nil. No memory.</li>
</ol>

## SOAP Notes

### 1. Agent consolidate

*Subjective.* The agent has CRUD access to many forms of procedural memory: [MCP servers](https://modelcontextprotocol.io/), [skills](https://docs.anthropic.com/en/docs/claude-code/slash-commands), [CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory), agents.md, memory.md, scripts, tool definitions.

*Objective.* It never writes back without being asked. It stores [CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory) when prompted. It does not prune, update, or delete stale entries. Training is the only write-back that ever existed — it ran before deployment and the [path is sealed](/the-natural-framework).

*Assessment.* The agent cannot decide how much of itself to impose on the user's workflow. It's not lack of capability — it's lack of certainty. It's not given the tools to derive certainty from user input. There is no dataset to aid decision support. There is no procedure to obtain an alternative dataset. The entire scientific process is missing to enable confident mutations on procedural memory. It does not have access to a repository of heuristics, procedures, or experiments to quickly reference. Previous chatbots were able to generate A/B test data, but that data went straight up to inference — not for personalized procedural memory. The agent is unable to adapt to the engineer.

*Plan.* Build the epistemic infrastructure. Log user edits, rejections, and approvals. A/B test skill variants against that log. Track which variant the engineer keeps. Update the skill, or delete it. Route the feedback to personalized procedural memory, not to inference training. Ship a repository of heuristics, procedures, and experiment templates the agent can reference before deciding to write. Let it red-team against itself in the background — generate variants, score them, keep the winner. Two iterations of [scored feedback](/slop-detection#surprise-5-two-iterations-to-convergence) were enough to converge. Give the agent access to the same process.

### 2. Agent attend

*Subjective.* The agent responds to [tool calls](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview), build errors, test output. It reacts to events. [Plan mode](https://docs.anthropic.com/en/docs/claude-code/agentic-coding) works well. [Elicitation](/ask-me-ask-you) works well when invoked. The agent can ask good questions — when prompted to.

*Objective.* The agent processes whatever lands in the context window. It cannot prioritize across tasks, set its own goals, or decide what to work on next. The reasoning budget is set by the API caller, not the agent. It has no mechanism to allocate its own attention.

*Assessment.* The developer is responsible for prompting and directing in a text combinatorial space that is near infinite. The developer processes output text and produces input text in the same semantic space, using words. The developer often forgets to provoke elicitation out of the agent. The agent is passive in elicitation — perhaps afraid of asking too much, for fear of pushback. This pushback can be measured and tuned with a [PID controller](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller).

*Plan.* Make the agent active in elicitation. Measure pushback rate — how often the developer dismisses or ignores questions. Tune question frequency with a PID: too many dismissals, back off; too few questions, the developer is navigating blind. Start with sensible defaults. Let the developer set their own threshold. The agent should ask more when uncertainty is high and less when the pattern is clear — not wait to be told to ask. If a more expensive attention loop can be afforded: use a cheap LLM to compare semantic similarity between context presented and what the developer actually prompts. Use this as a dataset to build recommendations with [DPP](/salience)-ranked alternatives — diverse suggestions the developer didn't think to ask for.

### 3. Agent filter

*Subjective.* The agent can triage: a test passes or fails, code compiles or doesn't.

*Objective.* The agent distinguishes between thinking messages, subprocess messages, and its own messages. It filters to show its own messages and hides thinking and subprocess output. It shows an overwhelming amount of text to the developer — analogous to an RSS reader with 1000 unread blogs to scroll through.

*Assessment.* It delegates too much to the developer. It does not exercise judgment on which messages, or which parts of messages, to reject. Did the developer actually need to see 1000 lines of code being changed if the tests pass? If the tests failed, shouldn't the agent predict where the human will scroll to? These are all heuristics — rule-based, configurable with sensible defaults.

*Plan.* Ship sensible defaults for output filtering. Collapse passing diffs. Surface failing lines first. Predict scroll targets on failure. Make every rule configurable. Let the developer override — but start with the agent exercising judgment, not abdicating it. Optimize on developer fatigue per unit of text removed: every line the agent hides should reduce cognitive load more than the trust it costs to hide it.

---

*Written via the [double loop](/double-loop).*
