---
layout: post-wide
title: "Diagnosis LLM"
tags: cognition
---

*Part of the [cognition](/cognition) series.*

The [Natural Framework](/the-natural-framework) defines [six roles](/the-natural-framework#six-steps): perceive, cache, filter, attend, remember (forward stages), and consolidate (reads from Remember, writes to the substrate). Every learning system runs some subset. The question is which roles are dysfunctional.

## Observations

AI has three layers. Inference: transform tokens. Chatbot: transform context. Agent: transform prompts. But the chatbot isn't a separate pipeline. It's the agent's Cache and part of Perceive.

<div style="max-width:90vw; margin:1.5em auto;">
<img src="/assets/agi-loop.svg" alt="Three layers — Inference, Chatbot, Agent — each with five forward roles and Consolidate as backward pass. Inference's Consolidate is sealed (Training). Chatbot has four nils. Agent has Consolidate prompted." style="width:100%; display:block;">
</div>

### Inference
- Perceive: functional. Embed maps tokens to vectors.
- Cache: functional. Positional encoding indexes by position.
- Filter: functional. Softmax scores and suppresses.
- Attend: functional. Multi-head attention selects across subspaces.
- Remember: read-only. Weights loaded every pass, never updated during inference.
- Consolidate: functional. Training is the backward pass. RLHF, red-teaming, evaluation — [humans are the crontab](https://www.anthropic.com/careers/jobs?team=4002061008). Fires per model update, not per session.

### Chatbot (= agent's Cache + Perceive)
- Perceive: functional. Splits the conversation into turns. The agent's Perceive relies on this.
- Cache: functional. Token context accumulates in the window. This IS the agent's Cache.
- Filter: nil. Expected. Cache doesn't filter.
- Attend: nil. Expected. Cache doesn't rank.
- Remember: nil. Expected. Session ends. The agent's Remember (filesystem) persists across sessions.
- Consolidate: nil. Expected. Cache doesn't learn.

### Agent
- Perceive: functional. Tool calls, build errors, test output.
- Cache: functional. Context window holds the prompt.
- Filter: shallow. Triage on pass/fail. No filter on direction.
- Attend: reactive. Responds to what happens. Cannot set direction.
- Remember: functional. Filesystem persists across sessions. The cache for Consolidate exists.
- Consolidate: no backward pass. Can create skills when prompted. No trigger, no schedule, no async loop that reads from Remember.

## Triage

<ol>
<li style="font-weight:700">Agent consolidate: no backward pass. Remember caches experiences; nothing reads them back.</li>
<li style="font-weight:600; color:#333">Agent attend: reactive. Cannot set direction.</li>
<li style="font-weight:400">Agent filter: shallow. No filter on direction.</li>
<li style="color:#888">Inference consolidate: functional but human-triggered. Training is the backward pass. Fires per model update, not per session.</li>
<li style="color:#888">Inference remember: read-only during inference. Updated only when Consolidate fires (training).</li>
<li style="color:#aaa">Chatbot: not a separate pipeline. It's the agent's Cache (context window) and part of Perceive (turn splitting). The four nil cells are expected, not broken. <a href="/union-find-compaction">Union-find</a> is a cache upgrade.</li>
</ol>

## Why the chatbot is Cache

The chatbot's four nil cells are not dysfunction. They are what Cache looks like: store and retrieve, nothing more. The chatbot has no policy store because Cache doesn't need one. It accumulates context in the window (Cache) and splits the conversation into turns (Perceive). Filter, Attend, Remember, and Consolidate belong to the agent, not the chatbot.

[Union-find compaction](/union-find-compaction) is a cache upgrade: better provenance, recoverability, and incremental updates for the context window. It's still Cache. It reorganizes the store (`VACUUM`) without changing how the agent processes. The missing role is still Consolidate: the cron job that reads from Remember and writes new procedures.

The SOAP notes below are what building the missing roles looks like.

## SOAP Notes

### 1. Agent consolidate

*Subjective.* The agent has CRUD access to many forms of procedural memory: [MCP servers](https://modelcontextprotocol.io/), [skills](https://docs.anthropic.com/en/docs/claude-code/slash-commands), [CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory), agents.md, memory.md, scripts, tool definitions.

*Objective.* It never writes back without being asked. It stores [CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory) when prompted. It does not prune, update, or delete stale entries. It can create [skills](https://docs.anthropic.com/en/docs/claude-code/slash-commands) — the only procedure that writes procedures — but only when directed to. [Compaction](/union-find-compaction) upgrades Cache (`VACUUM`), not Consolidate. Skill creation is Consolidate: it changes how the agent processes the next session. The forward pass works. Experiences persist in the filesystem (Remember is the RESTful interface; the store exists). But no backward pass reads from that store to update the substrate. The cron job is defined but never scheduled. The agent never sleeps; always tires.

*Assessment.* The agent can create skills, and skills are procedural memory: they change how the agent filters, attends, and responds in future sessions. That makes skill creation the backward pass. But the agent has no async loop. Neural networks fire backprop after every forward pass. Sleep fires consolidation on a biological clock. Inference has humans as its crontab (RLHF, training). The agent fires Consolidate only when the user says "please make a skill now." [The Flicker](/the-flicker) is that: one backward pass, fired by hand. The bottleneck is not capability but the missing trigger. Inference solved it by hiring humans to schedule the backward pass. The agent hasn't. There is no dataset to aid decision support, no procedure to obtain one, no repository of heuristics or experiments to reference. The entire scientific process is missing. Previous chatbots generated A/B test data, but that data went to inference training, not to personalized procedural memory. The agent is unable to adapt to the engineer.

*Plan.* Build the async backward pass. Six components:
1. **Event logger** — perceive user edits, rejections, and approvals.
2. **Decision log** — cache structured records of each user decision in Remember.
3. **A/B test harness** — filter skill variants against the log, reject losers.
4. **Red-team scorer** — attend by running adversarial scoring in the background, pick the winner.
5. **Skill mutator** — the backward pass: read from the decision log, write CRUD operations to procedural memory.
6. **Trigger** — schedule or event that fires the backward pass. End-of-session review, threshold of accumulated decisions, or idle time. The equivalent of sleep.

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
