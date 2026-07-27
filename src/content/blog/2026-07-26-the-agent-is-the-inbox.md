---
title: "The agent is the inbox"
tags: coding, agents
---

The standard recipe begins with the model and works outward: give an LLM tools, add memory, put a loop around it, then add human approval once it becomes dangerous. This produces a capable process with no boundary where every external influence can be enumerated, audited, or replayed.

Begin with the inbox instead.

Independent stacks have already built three quarters of this, each under a different name, and none of them treats the inbox as the boundary.

## The convergence

[Cloudflare's Agents SDK](https://developers.cloudflare.com/agents/concepts/agent-class/) says it outright. Agents *are* Durable Objects. One live instance per unique name, addressable from anywhere by `getAgentByName()`, holding its own SQL state and its own alarm-backed schedule. That is identity, private state, placement-independent addressing, and a timer that can message you back later.

[Temporal](https://docs.temporal.io/develop/python/workflows/message-passing) gives a long-lived workflow a durable mailbox. A signal is recorded in workflow history, so a worker that crashes between delivery and handling replays it on recovery. [Restate](https://restate.dev/) and [DBOS](https://www.dbos.dev/) journal the same guarantee against a key or a Postgres row. The industry spent 2025 and 2026 rediscovering that an agent needs an identity whose message log survives the process.

[A2A](https://a2a-protocol.org/latest/specification/), now at v1 under the Linux Foundation, publishes an agent card at a well-known URL and moves Messages that drive a Task through a lifecycle. Two of its states exist for a task waiting on something outside the agent, `input_required` and `auth_required`, and long-running results return over a stream or a registered webhook. [MCP](https://modelcontextprotocol.io/) had already made the same discovery move for tools.

[CoALA](https://arxiv.org/abs/2309.02427) supplies the memory partition. Sumers, Yao, Narasimhan, and Griffiths split a language agent's memory into working, episodic, semantic, and procedural. They imported the division from [Soar](https://doi.org/10.1016/0004-3702(87)90050-6) and [ACT-R](https://act-r.psy.cmu.edu/) rather than inventing a new one. [Letta](https://www.letta.com/blog/sleep-time-compute/) then runs consolidation as its own process. A sleep-time agent edits the primary agent's in-context memory blocks while the primary idles.

## The tell

LangChain shipped [Agent Inbox](https://github.com/langchain-ai/agent-inbox), described as "an inbox UX for interacting with human-in-the-loop agents." A [LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts) node calls `interrupt()` and the graph checkpoints against its persistence layer. A structured request then lands in something that looks like Gmail, where a person can accept, edit, respond, or ignore.

Traffic runs the other way too. [OpenClaw](https://en.wikipedia.org/wiki/OpenClaw) ships no interface of its own. The self-hosted personal agent crossed 100,000 GitHub stars in its first week in late January, and you reach it through Signal, iMessage, Discord, or Telegram. Its users went hunting for somewhere it could receive mail under its own name, and [AgentMail](https://agentmail.to/) sells exactly that: email inboxes created by API call, for agents. Its CEO told TechCrunch that signups [tripled the week OpenClaw broke and quadrupled in February](https://techcrunch.com/2026/03/10/agentmail-raises-6m-to-build-an-email-service-for-ai-agents/).

Give a person an agent to supervise and the interface converges on an inbox, because human attention was already addressed that way. Give an agent a life of its own and the first thing it needs is an address where messages can arrive while it is not running.

Yet across all of these stacks the inbox shows up as a property of the pause or as a channel integration. Each stack defines the participant as something else: a class, a graph node, a durable object, a task. The system is made of agents, and the person is a callback registered at the dangerous parts.

Invert it. Make the inbox the definition and the person stops being a special case.

## Actor, inbox, agent

An actor is the entity addressed by a logical inbox. Every external influence arrives as a message. The actor alone reduces those messages against private state and decides what to do next. The message may come from a human, an LLM, another actor, a timer, or the environment; initiative belongs to none of them by default.

```text
actor = logical inbox + private state + transition policy
```

The inbox is the boundary. The graph between inboxes can be arbitrary. Hewitt, Bishop, and Steiger fixed these properties in 1973 in *[A Universal Modular ACTOR Formalism for Artificial Intelligence](https://cir.nii.ac.jp/crid/1570572699086497152)*, and Gul Agha's 1986 *[Actors](https://mitpress.mit.edu/9780262010924/actors/)* developed them into a model of distributed computation.

Here, an agent is an actor whose transition policy may invoke an LLM. The model is a cognitive resource inside the boundary, not the boundary itself.

<div style="max-width:760px;margin:1.5em auto 2.5em;">
<img src="/assets/agent-inbox-boundary.svg" alt="Human, actor, timer, and environment messages converge on an actor's logical inbox. Inside the actor, private state and a transition policy produce outgoing messages and effects." style="width:100%;display:block;">
</div>

## One transition

Each turn has a small contract; the goal arrives in the message or persists in private state:

```text
(previous state, goal, message)
    -> (proposed action, desired next state)
```

The proposal is not the effect. A deterministic layer validates it against authority, policy, budget, criticality, and the procedure's observation contract. The LLM may propose a transition. It does not author the test the transition must pass.

An executor performs the effect. An observer records what actually happened. The difference between desired and actual state becomes another message. A rejected proposal does too.

<div style="max-width:760px;margin:1.5em auto 2.5em;">
<img src="/assets/agent-transition-loop.svg" alt="An agent transition flows from message through decision, gate, execution, observation, and comparison. The discrepancy between desired and actual state feeds back into the next decision." style="width:100%;display:block;">
</div>

The split separates decision from execution without pretending decisions must be deterministic. Decide, gate, execute, observe, and compare are observable activities inside one actor. They need independent actor boundaries only when they require their own address, private state, or authority.

The procedure owns the observation contract: the desired condition, source of evidence, evaluation time, and tolerated discrepancy. A chess engine queries the win condition at every ply, and a reinforcement-learning environment hands back a reward. Success in real activity is rarely immediately queryable. The signal may arrive hours or weeks later, be confounded by other interventions, or remain ambiguous.

Until then the transition remains an in-flight experiment in the [hypothesis graph](/the-hypothesis-graph-semantic-memory-methodeutics/): prediction, intervention, observation window, and current status. A timer or environmental event delivers evidence as a new message and the actor resolves, rejects, or revises the hypothesis. Otherwise the human becomes the system's missing comparator, repeatedly checking whether reality resembles the agent's claim.

## Three regimes

The transition policy is where a supervisor lives. It matches the current situation against known classes and routes by confidence and consequence:

```text
known class, stable procedure      -> deterministic action
recognized class, judgment needed -> LLM action
novel, conflicting, or critical   -> human action
```

<div style="max-width:760px;margin:1.5em auto 2.5em;">
<img src="/assets/agent-supervisor-learning.svg" alt="A supervisor routes situations by class, confidence, novelty, and criticality to deterministic, LLM, or human action. Evidence from all three returns through a backward pass to improve matching and procedure." style="width:100%;display:block;">
</div>

Criticality changes the thresholds. An irreversible action takes a hard human gate even when the match is confident. A reversible, low-risk action runs immediately and enters a soft review queue with a veto window. Human judgment is therefore both an execution regime and a gate on machine proposals. Both arrive through a human actor's inbox.

The matcher can learn online. A human acceptance, rejection, preference, or correction is a local label, available immediately to the next similar case. Consolidation happens later. Repeated corrections become exemplars, then candidate procedures, then shadow executions, then soft-gated defaults, and finally deterministic actions where the class proves stable.

The direction of travel is:

```text
human -> LLM-assisted -> deterministic
```

The arrow moves one situation class at a time. Classes that prove stable get absorbed, and the rest keep arriving through the gate. Judgment transfers piecewise, and elicitation is the mechanism. Those local labels are judgment moved out of a person and into a place the matcher can reach, so the quality of elicitation sets the speed of the arrow.

## The cache

The shape of the cache determines which situations the supervisor can recognize. A vector database bolted onto a chat loop is one retrieval mechanism against one partition:

- episodic memory preserves transitions and their evidence;
- procedural memory preserves policies, gates, and learned routines;
- semantic memory consolidates the current model of the world, including unresolved hypotheses and in-flight experiments.

This is the partition CoALA imported from Soar and ACT-R, and it predates the current stack by forty years. Soar organized general intelligence around goals, problem spaces, impasses, productions, and learning from resolved subgoals. ACT-R organized cognition through interacting modules, buffers, declarative chunks, and procedural productions. Calling the result an "agent memory system" mistakes one organ for the architecture that makes it useful.

The [hypothesis graph paper](/the-hypothesis-graph-semantic-memory-methodeutics/) develops the semantic-memory role. The graph represents what the system currently believes, disputes, and still awaits. Episodic memory retains the individual transition and its later evidence; the graph keeps their live epistemic relationship addressable across the delay.

Retrieval decides which prior situations appear equivalent, which procedure is trusted, which experiments remain open, and which discrepancies become visible. Cache contents are knowledge. Schemas, consolidation rules, retrieval policies, and the partition among memory systems are architectural commitments. The model can change while that learned organization persists.

## The andon

The supervisor's operating discipline comes from a lineage older than any of this. [Toyota describes *jidoka*](https://global.toyota/en/company/vision-and-philosophy/production-system/) as machinery detecting an abnormality and stopping instead of requiring a person to watch it continuously; andon makes that abnormality visible, while just-in-time constrains inventory to expose the condition of the flow. TPS treats automation, human judgment, work-in-process, and learning as one operating system.

The factory is the flow of activities that repeatedly converts demand into verified outcomes. The physical deployment is supporting structure. Stable takt and deliberate WIP limits make that flow observable. Queue growth reveals a constraint. Rework reveals defects. Human-inbox growth reveals a missing procedure or a misplaced gate. Blind autoscaling conceals all three by adding capacity before the queue registers the abnormality.

An andon is the structured message that names the discrepancy and summons the appropriate judgment. Human attention is the scarcest inventory on the line. Spending it should leave a durable change, or the line demands the same withdrawal again.

The backward pass here is not gradient descent. It converts operating evidence into changes in matching, procedure, policy, interface, or system boundary. Reinforcement learning may optimize bounded supervisory choices such as routing, model selection, WIP, or scheduling. Deterministic constraints retain authority over safety and irreversible effects.

## Scale-free

Nothing in *inbox, private state, transition policy* fixes a size, a latency, or a substrate. The definition holds for a handler that runs for forty milliseconds behind an HTTP endpoint, for a workflow that lives six weeks, for a team, and for one person with an email address. What varies is the timescale of the reduction and the authority attached to the address.

Delegation becomes symmetric. An agent requesting approval from a person and a person assigning work to an agent are the same operation with the roles swapped. Agent Inbox and Gmail are the same object rendered twice, once for the supervisor and once for the supervised. There is no human-in-the-loop feature to build, because the human was never in the loop; the human is a node in the graph with a slower transition policy and more authority.

Deployment stops determining the programming model. None of this initially requires cloud infrastructure. A local durable workflow engine, Python workers, a database, model APIs, and a TUI are enough to test:

- whether the activity produces value;
- whether transitions are specified;
- whether actual state is observable;
- where gates belong;
- whether intervention improves the system.

[Sweep](https://github.com/kimjune01/sweep) runs on exactly that. A Temporal supervisor moves contribution work through stations, every gate leaves a hashed receipt, a failed postcondition halts the line, and whatever the operator owes waits in a human inbox under the station table.

Each workflow identity owns an inbox and state while agents of the same class share a task queue. Workers spread across processes and machines later without changing the model. Scale gets added along an existing execution boundary when queue latency, isolation, or recovery justify it.

The graph crosses organizations without waiting for a new protocol. My actor sends to your actor. Whether yours reduces the message with a model, a procedure, or a person on Tuesday morning stays private behind your address.

That is what AgentMail is selling. Its three headline features are identity, communication, memory. An address, asynchronous threaded messages, and durable private state the agent can search later. Someone rebuilt three quarters of the actor definition and took $6M for it, because email was the only substrate already carrying all three that required nobody to adopt anything.

## The missing language

The quarter left over is the transition policy, and email makes a poor runtime for one. Messages are untyped. Identity is bolted on downstream through DKIM and SPF. There is no authority model and no delivery semantics worth the name. A2A specifies all of that and contains no humans. So the industry now holds one substrate that reaches every participant and cannot express a contract, and another that expresses contracts and reaches only machines. The distance between them is the missing programming model.

That model composes the [four schools of programming](/four-schools-of-programming/):

- actors provide identity, inboxes, and private state;
- functional transformations propose the next transition;
- declarative constraints define admissibility and success;
- imperative activities change the world.

Current frameworks expose pieces of this under names such as agents, memory, tools, graphs, guardrails, human-in-the-loop, evaluation, and observability. Products will be built around each piece because pieces can be sold. The programming model will take longer.

The components exist and ship today. The next decade goes to systems fumbling with the wrong boundaries until repeated operational failures reveal the stable primitives. The language arrives afterward, extracted from working cognitive architectures the way Erlang was extracted from telecom.

> An operational cognitive architecture can be expressed as a graph of inbox-defined actors that propose, gate, execute, observe, and learn state transitions under mixed human and machine initiative.

Until the language arrives, begin with the inbox.
