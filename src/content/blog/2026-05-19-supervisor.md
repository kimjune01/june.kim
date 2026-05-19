---
variant: post-wide
title: "Supervisor"
tags: coding, cognition, methodology, epistemology
---

*Sequel to [Encoding Expertise](https://june.kim/encoding-expertise).*

[Encoding Expertise](https://june.kim/encoding-expertise) ended with one classifier hoisted clean. A skill with a five-stratum shell (precondition, postcondition, CLI tools, cache, residue) wrapped around a thin LLM nucleus. The skill produces three outputs at runtime (certain, ambiguous, false-known), and the two non-certain outputs route to the operator: ambiguous to inbox, false-known to andon. The operator disambiguates or names the broken assumption, and the substrate gains one new structural artifact.

The mechanism works, but the operator is the bottleneck. Every inbox card disambiguated is a decision about *how* to encode the mistake (precondition or cache key? tighter enum or new postcondition?). Every andon named is the same kind of decision pointed the other way. After enough cards those decisions form a pattern, and the pattern is the same shape as the classification problem the skill solves: a structured event in, a finite set of encoding-update buckets out, an irreducible residue. The encoder becomes another skill.

Watch the shape. Three andons fire over a week: *"model said shipped, branch wasn't there."* The operator's encoding decision each time is the same: add a `gh branch-exists` CLI tool the actor calls before the model fires, and the false-known disappears. After the third andon the supervisor doesn't need the operator to make this call. It can spot the repetition, propose the CLI tool, verify the tool would have prevented each historical occurrence (replay against the andon log), and ship the encoding. The operator never has to write that branch.

## The supervisor

The supervisor is an actor whose inbox is downstream actors' attention outboxes (inbox cards, andon events, assertion violations) and whose outboxes are encoding-update messages back into those shells. Same primitive as the skill. Same three outputs: encodable (ship the update), ambiguous (escalate), false-encoding (caught by the idempotence wall when a previously-passing case starts failing). Same five strata: only consider patterns with N≥3 occurrences (precondition), check that the proposed predicate compiles and the CLI invocation exists (CLI tool), replay against the historical log without breaking past decisions (postcondition), don't re-propose an encoding already rejected (cache), punt to the human on "should this be encoded at all" (residue).

The supervisor needs one input the skill doesn't: an **explicit goal**, stated as a single sentence, that disambiguates everything ambiguous it sees. Sweep's goal is *find interesting work without abandoning any reviewed PR.* Given that, a pattern that increases trivial-fix throughput is un-encodable (drifts away from the goal); a pattern that catches an abandonment risk is urgent-encodable. The goal is the gradient: every ambiguous decision asks *does shipping this encoding serve the stated goal better than escalating?* The LLM nucleus has a prompt; the supervisor has a goal. Same role, one level up. This is also the alignment lever: where [RLHF](https://arxiv.org/abs/2203.02155) and [Constitutional AI](https://arxiv.org/abs/2212.08073) (Bai et al., 2022) push values into the model's weights via gradient updates, the supervisor takes values as an explicit specification and lets the encoding loop drive the policy to a fixed point that satisfies them. Different substrate, same problem.

The nearest neighbors in the literature compile failure feedback into something, but not into deterministic structure. [Reflexion](https://arxiv.org/abs/2303.11366) compiles into verbal self-criticism in memory. [Voyager](https://arxiv.org/abs/2305.16291) compiles into a growing library of LM-authored skills (still prompts). [TextGrad](https://arxiv.org/abs/2406.07496) compiles into textual gradient updates on the prompt. [GPTSwarm](https://arxiv.org/abs/2402.16823) compiles into edge weights on an agent graph. The supervisor here compiles into preconditions, postconditions, CLI dispatches, and cache keys: deterministic artifacts that fire without the model. Same loop shape, different terminal substrate. The difference matters because deterministic artifacts pay no model freight on subsequent calls and replay exactly against historical decisions, and exact replay is what the idempotence wall requires.

The LLM's new job is to build the expert system around each classifier. The skill in *Encoding Expertise* had a human doing this slowly, decision by decision; the supervisor has the LLM doing it at machine speed, the same operation one level up.

## Eliciting the human

The supervisor doesn't only react to cards the operator surfaces. Once it has a goal, it can also *elicit*. The supervisor identifies what it doesn't know with high enough impact to ask about, formulates the narrowest question that would resolve the uncertainty, and sends that question to the operator's inbox. The operator answers; the supervisor encodes the answer; the policy moves toward its fixed point one decision faster than it would have through passive surfacing alone.

This inverts the operator's role. Without elicitation, the operator routes PRs (broad, repetitive, high-volume); with it, the operator answers narrow questions about edge cases the supervisor isolated (focused, rare, high-leverage). The human becomes a queryable oracle, not a manual classifier. Volume drops by an order of magnitude; the value of each remaining decision rises by the same factor, because the supervisor only asks when it can't decide on its own and the asking is shaped to maximize what it learns from the answer. This is [active learning](https://en.wikipedia.org/wiki/Active_learning_(machine_learning)) applied at the encoding layer: the supervisor selects which mistakes to investigate, not which inputs to classify.

The elicited questions become first-class artifacts. They go through the same idempotence wall as proposed encodings (does the answer replay against history?). They're cached (don't ask the same question twice). They're rate-limited against the operator's attention budget (the human-attention principle applies to elicitation too). And the questions themselves are evidence for the supervisor's residue: an elicited question that the operator can't easily answer is a sign the local context is genuinely fuzzy, not under-encoded.

## The cascade

The cascade reads cheapest first: **precondition → expert system → LLM call → supervisor → human.** Each layer protects the next from work the next would do worse and more expensively. Cards flow down the pipe; each one descends through the layers until one of them claims it. Lessons flow up the same pipe in the opposite direction: every operator decision at the top becomes an encoding update somewhere below, every andon at the bottom becomes a proposed remediation that climbs through the supervisor toward the layer that owns the broken assumption. Two temporal axes on the same staircase. The cascade is the runtime; the encoding loop is the slower clock running counter to it. The downward-only version is familiar from multi-agent supervisor frameworks like [LangGraph](https://www.langchain.com/blog/langgraph-multi-agent-workflows) (2024) and [AutoGen](https://arxiv.org/abs/2308.08155) (2023); the upward "operational incident becomes structural lower-layer code" loop is the missing half.

Each layer asserts on things that shouldn't happen under its assumptions. The precondition asserts the input shape. The expert system asserts that the CLI tool's answer matches the trigger signal. The LLM wrapper asserts that the model returned a value the postcondition can validate. The supervisor asserts that a proposed encoding replays cleanly. The human's "this shouldn't have reached me" is the final assertion. Violations percolate the same way runtime ambiguity does: they hit the supervisor first, which runs its three-output classifier and ships an encoding when it can. Only the residue reaches the human. The cascade protects the operator at the top of the queue as much as it protects the LLM at the bottom.

## Two axes

The substrate's mature shape is a two-dimensional grid. Rows are recursive layers; columns are strata. The LLM lives only in the rightmost column at every row. Everything to its left is encoded:

| | Identity | Legal moves | Live state | Repeats | Residue |
|---|---|---|---|---|---|
| **Skill** | precondition (code branch) | postcondition enum | CLI tool | input-hash cache | LLM call |
| **Supervisor** | N≥3 occurrence threshold | encoding-action enum | compile check + replay | rejected-proposal cache | LLM call |
| **Supervisor²** | (same shape, one level up) | (same shape) | (same shape) | (same shape) | LLM call |
| **Human** | "this isn't classifiable" | "out of scope" | (none needed) | (none needed) | judgment |

The grid converges asymptotically, provided the interface between layers is clean. The cleanliness is concrete, not aspirational: the [actor model](https://en.wikipedia.org/wiki/Actor_model) already specifies it. Inbox in, named outboxes out, one per terminal state, no shared state, no side channels, no globals. The skill's three outputs route to distinct outboxes, never coerced into one. Ambiguous lands on inbox with operator-actionable context. False-known fires andon with the assumption named. The supervisor reads those outboxes as its inbox and writes encoding updates as its outboxes. Every level uses the same primitive.

Dirty channels hide the corrections; the shell can't learn what it can't see. Coerced outputs lose the distinction between "I don't know" and "I think I know," and the encoder can't tell whether to widen the input or tighten the assumption. Prompt patches don't replay against history; the idempotence wall isn't there to catch overfit. With clean interfaces the updates compose: every inbox card surfaces a piece of the problem's true shape the guess was missing, every andon surfaces a piece where the guess was wrong, every encoding update bends the shell closer. The supervisor automates the bending.

## Dynamic substrate

A dynamic language helps more than the theory lets on. Python lets the substrate accept new branches, schema entries, and CLI dispatches at runtime, no rebuild, no redeploy. [Erlang's hot code swap](https://www.erlang.org/doc/system/release_handling.html) is the older, stronger form. A statically built substrate batches the encoding loop into release cycles, collapsing the supervisor's edge: by the time the encoding lands, the assertion that motivated it has fired thirty more times.

## What's left

The supervisor compresses the second hoist: encoding work that used to fall on the operator now ships from a process that runs at substrate speed. The operator answers narrow elicited questions instead of routing everything by hand. Count how often the operator's inbox fires before and after the supervisor goes live on the same workload: if the ratio isn't roughly an order of magnitude, the supervisor's threshold or goal is wrong. But the supervisor still waits for mistakes (local mistakes, or local elicitations) to feed its encoding loop. The substrate suffers each pattern at least a few times before the encoding lands. The next hoist is to skip even that wait: feed the supervisor whatever public corpus the world already provides. That's [the next post](/asymptote-learning).
