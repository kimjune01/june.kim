---
variant: post-wide
title: "Soar Already Does Async"
tags: cognition
---

Soar tells itself a sync story. Everything happens inside the decision cycle:

- Input
- Propose
- Decide
- Apply
- Output

One tick, one clock, one context. New learning mechanisms must fit inside that cycle. [Laird's](https://laird.engin.umich.edu/) recent draft on semantic-memory learning requirements makes it explicit:

- Incremental and continuous.
- Synchronized with the decision cycle.
- Per-cycle cost bounded, proportional to working-memory changes.

The story is already false in the repo.

## What I mean by async

Async here means work whose logical cause and execution are separated across decision cycles: queued, scheduled, or resumed later. Like a microwave: press, walk away, ding. A priority queue is an ordering data structure. A priority queue keyed by a future cycle and drained when that cycle arrives is a scheduler. A substate that suspends a computation until a result bubbles up has coroutine-like shape. The argument is about shape. Implementation identity sits a level below.

## The anchor: WMA forgetting

`working_memory_activation.cpp` runs a priority queue of decay elements keyed by the cycle each WME is predicted to fall below the forgetting threshold. Three functions carry the scheduler:

- `wma_forgetting_add_to_p_queue` — enqueue a WME for future forgetting.
- `wma_forgetting_update_p_queue` — drain items whose cycle has arrived.
- `wma_forgetting_estimate_cycle` — predict the cycle at which a WME will fall below threshold.

Events are queued on a future cycle and drained when the cycle arrives. That is a scheduler.

## Other kernel evidence

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:22em"><col><col><col style="width:6em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Location</th><th style="background:#f0f0f0">Mechanism</th><th style="background:#f0f0f0">Used for</th><th style="background:#f0f0f0">For learning?</th></tr></thead>
<tr><td><code>smem_activation.cpp</code> (<code>lti_calc_base</code>, <code>smem_max_cycle</code>, history tables)</td><td>clock + historical-access table</td><td>base-level activation decay</td><td>No</td></tr>
<tr style="background:#fafafa"><td><code>episodic_memory.h:606, :627</code></td><td><code>std::priority_queue&lt;epmem_pedge*&gt;</code>, <code>std::priority_queue&lt;epmem_interval*&gt;</code></td><td>priority-ordered retrieval traversal</td><td>No</td></tr>
<tr><td><code>smem_structs.h:73–86</code></td><td>three priority-ordered queues:<ul><li><code>smem_prioritized_weighted_cue</code></li><li><code>smem_prioritized_activated_lti_queue</code></li><li><code>smem_prioritized_lti_traversal_queue</code></li></ul></td><td>spreading activation and weighted cue processing</td><td>No</td></tr>
<tr style="background:#fafafa"><td><code>run_soar.cpp</code> (<code>timers_decision_cycle_phase</code>)</td><td>per-phase wall-clock timers</td><td>profiling the decision cycle</td><td>No</td></tr>
</table>

These rows are priority-ordered traversal: scheduler-shaped data structures that stay within a single cycle.

## Program-level evidence (Thor-Soar)

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:16em"><col><col><col style="width:6em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Location</th><th style="background:#f0f0f0">Convention</th><th style="background:#f0f0f0">Used for</th><th style="background:#f0f0f0">For learning?</th></tr></thead>
<tr><td>Thor-Soar <code>^future-events</code></td><td>scheduled event record in working memory</td><td>predicting microwave cook completion</td><td>No</td></tr>
<tr style="background:#fafafa"><td>Thor-Soar <code>^ms-remaining</code></td><td>countdown attribute on activated object</td><td>tracking external-world dynamics</td><td>No</td></tr>
<tr><td>Thor-Soar <code>^real true/false</code></td><td>clock selector flag on the world structure</td><td>distinguishing real from look-ahead time</td><td>No</td></tr>
<tr style="background:#fafafa"><td>Thor-Soar <code>^internal-simulation true</code></td><td>substate flag</td><td>running a separate simulated world in look-ahead</td><td>No</td></tr>
</table>

These are Soar programs, though they look like kernel mechanisms. One serious Soar application already needs to model future time, separate clocks, and coroutine-like suspended contexts, and builds them on the architectural affordances (substates, attribute structures) the kernel provides. Whether these conventions generalize to other programs or deserve kernel promotion is a separate question.

Combined: Soar has a scheduler (WMA forgetting), priority-ordered traversal (epmem and smem retrieval), separated clocks and future-event records (Thor-Soar programs), and coroutine-like suspension (look-ahead substates). The architectural affordances for ordered, cycle-indexed, context-suspending work are in the source.

Used everywhere except learning.

## The learning function

Soar's learning mechanisms (chunking, RL preference learning, `smem store` writes, automatic epmem recording) all fire synchronously on the decision cycle. Chunking compiles rules at impasse resolution. RL updates preferences when reward arrives. `smem store` writes when a rule action fires. Epmem records each cycle. Each listens to a present-tense trigger. None runs offline against past episodes to modify the substrate.

The missing edge is `epmem → pmem`. No direct kernel path connects a recorded episode to a procedural rule. For one to influence a rule, it must be retrieved into working memory, an impasse must arise, and chunking must fire on the resulting trace. That is not a path; it is a raffle ticket.

Adding a queue is the same pattern as WMA forgetting:

1. Each decision cycle, drain up to N items from a consolidation priority queue.
2. Each item is an episode, or a compressed trace, selected by some policy: recency, surprise, reward, coverage.
3. The drain either writes to semantic memory via the existing `smem store` machinery (with open questions about identity and provenance of offline writes) or synthesizes procedural rules (a harder problem, needing a replay-into-subgoal mechanism or a new inductive compiler).

Same shape as `wma_forgetting_update_p_queue`: a scheduled queue, drained once per cycle, bounded by a configurable N. It satisfies the per-cycle-bounded requirement by construction, provided per-item dequeue work is bounded.

The queue removes the decision-cycle objection to running bounded consolidation work. Rule induction remains a separate problem. The hard objection is semantic: what justifies a rule learned outside the current impasse context, where the trace that authorized it has already been torn down? That is the real research problem, and it hides behind the event-loop question until the event-loop question is out of the way.

## The operating system problem

A priority queue drained on a clock is an event loop. Substates are a call stack (push on impasse, pop on result), and chunking runs the compile pass when a frame returns. Half the runtime is already there. The missing half is a dispatch queue: an offline drain that pulls episodes, writes structures, and has no current cycle to attach to.

This pattern is common outside cognitive architectures. Apple's [GCD](https://en.wikipedia.org/wiki/Grand_Central_Dispatch) and [libdispatch](https://github.com/swiftlang/swift-corelibs-libdispatch) provide it at the OS level. Python exposes it through [asyncio](https://docs.python.org/3/library/asyncio.html). [Node's event loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) is the sharpest case for this argument: a single-threaded runtime with async semantics throughout, which is exactly the shape Soar would need. Single-clock architectures do not rule out async. Soar's sync-only commitment is a choice, not a constraint, and the half-reinvented runtime in the kernel is evidence that the choice is already leaky.

Soar committed to a single clock. That is its identity. But the seam around that commitment is open on the retrieval, forgetting, environment-modeling, and look-ahead sides. It is closed only on the learning side.

## The philosophical choice

The sync-vs-async question is not whether to add async to Soar. The shape is already in the kernel, documented in the source. The question is why it is legal for forgetting but not for learning. That argument must be made on architectural grounds: the machinery exists, the priority queues compile, and Laird's own requirements doc accepts linear memory cost as the acceptable ceiling for semantic memory. Architecture is the remaining fence.

Either offline consolidation violates a core architectural invariant that has to be defended explicitly, or it is an engineering path that has not been taken. Those are different claims. The source rules out the easy version — that Soar has no machinery for bounded, queued, cycle-indexed work.

The third position, which is where Soar sits today, is that learning is sync because learning has always been sync, and the scheduler in the attic is for something else.
