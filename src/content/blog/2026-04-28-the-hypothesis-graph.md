---
variant: post-medium
title: "The Hypothesis Graph"
tags: cognition, methodology
---

*Part of the [cognition](/cognition) series. Sequel to [Evidence has a trajectory](/evidence-has-a-trajectory).*

---

The [previous post](/evidence-has-a-trajectory) argued that p-values compress evidence into a scalar, losing the temporal structure. E-values don't — you can peek at every observation, stop whenever you want, and the error guarantee holds. The trajectory comes free. Four bins (converge, diverge, oscillate, chaos) tell you how to read it.

A science that produces a boolean (reject or don't) is strictly less interesting than one that also produces hypotheses. A p-value is a verdict: the experiment terminates and nothing points forward. An e-value trajectory is a story — it rose, stalled, oscillated, broke — and its shape contains the next question: conclusions *and* the next experiment to run. Strictly more output from the same input.

There's a structure to what happens after you classify — one that's been running for centuries, in lab notebooks, differential diagnoses, debugging sessions. Here's what I see.

### Knowledge is a graph with a frontier

[Belief is the edge of knowing](/belief-is-the-edge-of-knowing). Knowledge is the territory you've mapped; belief is the boundary — claims you're acting on but haven't tested. The frontier is where belief meets the unknown: edges pointing to experiments nobody has run.

Every experiment is a node: what you learned is its content; open questions become edges pointing outward. Each edge pointing to a potential experiment is a hypothesis. Call it the **hypothesis graph**.

#### A stalling engine

When a mechanic taps the alternator and the engine stalls, that's an experiment and it generates two hypothesis edges: test the battery, test the voltage regulator. The frontier advanced.

<div style="max-width: 600px; margin: 1em auto;">
<img src="/assets/hypothesis-graph.svg" alt="The hypothesis graph: existing knowledge fades above, current classification branches into validated edges and killed tests, kill conditions generate fresh frontier nodes below" />
</div>

The graph says what to do next: swap in a known-good wire and test the circuit. That's the perturbation. You can only decompose as far as you can isolate. For automobile electronics, signals are linear in an acyclic system — three bins suffice (converge, diverge, oscillate) and chaos can't occur. But what about a nonlinear system with feedback?

#### A web server under load

A web application under load is nonlinear with feedback loops everywhere. Perturb it and all four bins show up:

- **Convergence:** add a server to the pool. Traffic redistributes, CPU drops, response times settle back to baseline.
- **Divergence:** a database replica falls behind. Queries reroute to the primary, which saturates. Connection pools exhaust, health checks fail, more nodes get pulled. Cascade until outage.
- **Oscillation:** the autoscaler adds pods when CPU spikes, removes them when it drops, overshoots both ways. The system cycles with a period set by the cooldown timer. SREs call it thrashing.
- **Chaos:** a retry storm across dozens of microservices with jittered backoff, combined with a cache stampede on expiry. A single GC pause in one service cascades unpredictably through the dependency chain. The response-time trace is aperiodic.

<div style="max-width: 720px; margin: 1em auto;">
<img src="/assets/hypothesis-graph-web.svg" alt="Hypothesis graph for a web system under load: perturbation branches into convergent (add server), divergent (cascade failure), oscillatory (autoscaler thrashing), and chaotic (retry storm) responses" />
</div>

Same graph structure, all four bins occupied. The mechanic's three-bin graph was the easy case. This is the general one.

### The algorithm already running

The structure is the same everywhere:

1. Pick a frontier node. (Choose what to test next.)
2. Perturb the system. (Run the experiment.)
3. Classify the response. (Read the shape.)
4. Generate edges. (The shape names the open questions.)
5. Repeat until the frontier stops expanding.

This is common sense. Doctors call it diagnosis. Engineers call it debugging. Toddlers call it playing.

I went looking for the mechanism in the sensemaking literature. [Weick](https://en.wikipedia.org/wiki/Sensemaking) calls the loop enactment; [Klein](https://en.wikipedia.org/wiki/Recognition-primed_decision), recognition-primed decision; [Boyd](https://en.wikipedia.org/wiki/OODA_loop), OODA. They describe the loop in prose but never name the mechanism: how does the shape of a result generate the next question?

### Shape is classifiable

A p-value is a scalar; the shape is gone. An e-value trajectory is a time series, and time series have shapes. Every trajectory does one of four things ([Milnor, 1985](https://link.springer.com/article/10.1007/BF01217730); [Strogatz, 2014](https://en.wikipedia.org/wiki/Nonlinear_Dynamics_and_Chaos)):

<table style="max-width:500px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:7em"><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Settling</th><th style="background:#f0f0f0">Non-settling</th></tr></thead>
<tr><td><strong>Bounded</strong></td><td>Convergence</td><td>Oscillation (periodic) / Chaos (aperiodic)</td></tr>
<tr style="background:#f8f8f8"><td><strong>Unbounded</strong></td><td>—</td><td>Divergence</td></tr>
</table>

Four bins of triage, no gaps, no overlaps. Because the partition is exhaustive, each test eliminates at least one bin. Four bins, at most four tests to classify. Every elimination narrows what's left and points to the most informative next experiment. The shape *is* the edge-generation mechanism; it just requires keeping the temporal structure that p-values throw away.

<div style="max-width: 720px; margin: 1em auto;">
<img src="/assets/pvalue-vs-evalue.svg" alt="Same data, two pipelines: p-value produces a scalar and stops; e-value trajectory produces a classification and generates hypothesis edges" />
</div>

The [previous post](/evidence-has-a-trajectory) described four bins for this classification: converge, diverge, oscillate, chaos. The question was whether the classification works on composed e-value trajectories from heterogeneous experiments.

### Kill conditions generate edges

I [built a classifier](https://github.com/kimjune01/e-value-trajectory) that assigns these bins using a kill-condition decision tree:

1. Test for monotone trend. If it fails → skip to periodicity.
2. If monotone, test curvature. Decelerating → convergent. Constant → divergent.
3. Test for spectral peaks. Narrow peak → oscillatory.
4. Test for aperiodic structure → aperiodic.
5. Nothing triggered → null.

Here's what I noticed: each test that fires produces a label, but each test that *misfires* produces a hypothesis — an edge pointing to an experiment that would resolve it.

"Monotone trend detected, curvature indeterminate" → *Is this system decelerating or drifting?* Run a longer experiment.

"Spectral peak detected but broad" → *Is this a noisy cycle or colored noise?* Test at a different frequency.

"Nothing triggered" → *Null, or wrong perturbation site?* Test a different node.

The failure mode names the next hypothesis — that's the edge-generation mechanism. Same structure as [The Proof Manual](/the-proof-manual): when induction fails because the residual loses structure, the failure mode names the escalation. A trend test can't distinguish acceleration from deceleration? Check curvature. Kill conditions are the universal edge-generation rule. Doctors learn them by apprenticeship; mathematicians, by getting stuck. Nobody has written it down.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:7em"><col><col style="width:10em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Classification</th><th style="background:#f0f0f0">What it tells you</th><th style="background:#f0f0f0">What to try next</th></tr></thead>
<tr><td>Convergent</td><td>Something absorbed the perturbation</td><td>Test a different node</td></tr>
<tr style="background:#f8f8f8"><td>Divergent</td><td>This is load-bearing, no backup</td><td>Test what depends on it</td></tr>
<tr><td>Oscillatory</td><td>Two subsystems fighting</td><td>Test the interface</td></tr>
<tr style="background:#f8f8f8"><td>Aperiodic</td><td>Input exceeds architecture capacity</td><td>Decompose differently</td></tr>
</table>

### Why e-values

Each node uses a different instrument, measures a different quantity, tests a different hypothesis. You can't add fish counts to temperature readings, and you can't combine p-values from adaptive experiments without inflating error.

E-values compose: their product remains valid even when each experiment was chosen based on the last ([Grünwald et al., 2024](https://academic.oup.com/jrsssb/article/86/5/1091/7623686)). The composed trajectory carries the system's dynamics, weighting each stream by its informativeness. Good diagnosticians already do this; the math confirms it.

The [experiment](https://github.com/kimjune01/e-value-trajectory) tested this. Five sensor streams (normal, Poisson, exponential, Bernoulli, lognormal) sharing a weak forcing signal, each individually undetectable. Composed e-values classified the forcing pattern at F1 = 0.996 across four bins (convergent, divergent, oscillatory, aperiodic). Standardized sums: 0.478; individual streams: 0.279. Composition reveals shared forcing that individual streams miss because the likelihood ratio weights each stream by its informativeness — Fisher information weighting gives informative experiments more say.

### Null results aren't empty

In the p-value framework, a null result is a dead end: you failed to reject, so you move on.

But the e-value trajectory of that null has a shape. The trajectory didn't grow, but *how* it didn't grow is diagnostic:

- **Oscillating null:** the effect waxes and wanes. You tested at the wrong timescale. Edge: test at a different frequency.
- **Converging null:** there was an early signal that decayed. The system compensated. Edge: test the compensating mechanism.
- **Trending-then-reversed null:** the effect is real but transient. Edge: test the reversal point.
- **Flat null:** genuinely nothing. Dead end.

Only the flat null is a dead end. The other three are edges, lost in the compression to "fail to reject."

### Failed replications aren't empty

A "failed replication" in the p-value framework is a single bit: the original said yes, the replication said no. Was the original wrong? Was the replication underpowered? Did the system change? The boolean can't say.

The e-value trajectories of both experiments constrain the answer. If the replication oscillates where the original was monotone, something introduced feedback; if it converges where the original diverged, something is now compensating. Matching shapes with lower amplitude mean the effect is real but weaker.

How they disagree constrains *why* they disagree, and that constraint is the next hypothesis. Trajectories carry evidence about the mechanism of disagreement; booleans don't.

### Fixed point

The graph converges when every frontier edge points to a node already tested and stably classified — no new questions. Mathematicians call this a [fixed point](https://en.wikipedia.org/wiki/Fixed_point_(mathematics)) (where f(x) = x, the map returns what you gave it); computer scientists call it a [fixpoint](https://en.wikipedia.org/wiki/Fixed-point_combinator) (where a computation stabilizes and halts). Same idea from two angles: the system has nothing left to say.

If every reachable node is visited, classifications are consistent, and composed e-values preserve the regime's signature, the sequence converges to the true map — anytime validity lets you check at every node without inflating error.

I don't have a theorem — I'm just showing you that good diagnosticians converge. The pieces exist: [Chernoff](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-30/issue-3/Sequential-Design-of-Experiments/10.1214/aoms/1177706205.full) proved adaptive experiment selection converges, [He & Geng](https://jmlr.org/papers/v9/he08a.html) proved adaptive interventions recover causal structure, [Grünwald](https://academic.oup.com/jrsssb/article/86/5/1091/7623686) proved e-values compose across adaptive experiments. No published theorem connects them. One would formalize what practitioners already do.

### An observation

Suppose the algorithm for revealing follow-up hypotheses doesn't exist. The absence of structure must mean that hypotheses are randomly generated, and their order, arbitrary. But we observe that the knowledge graph of science does expand, and our attention drives connections from one experiment to another. It's proof that the algorithm for coming up with new hypotheses from experiments must exist.

[Popper](https://www.cambridge.org/core/journals/dialogue-canadian-philosophical-review-revue-canadienne-de-philosophie/article/idea-of-a-logic-of-discovery/5E31DF041E9E6B5D31EA79C6C06B065E) was right that there's no logical method of having new ideas from nothing. But they don't come from nothing; they come from the shape of the last experiment. The failure mode of the current test points to the next hypothesis. [Science on trial](/science-on-trial) described the protocol that protects this loop: prereg, red-team, work log, publish all.

For any system you can perturb, the hypothesis graph decomposes it. Each perturbation produces a node, whose classification generates edges that point to the next perturbations. The graph expands until it covers the system's structure, or until there's a boundary you can't perturb past.

The classification is limited to where you have:

- perturbation access (can't poke what you can't reach)
- independence between streams (correlated sensors weaken composition)
- identifiability (some systems look the same under all perturbations)

Within those limits, the algorithm converges. Outside them, it tells you where you're stuck and why, which is itself an edge.

Engineered systems are the best case. You have perturbation access and partial design knowledge. Every unexpected state is a free perturbation, every test failure is a node, and every failure mode is an edge. The hypothesis graph is how engineered complexity becomes legible: one perturbation at a time, with the kill condition telling you where to cut next.

If the thought process can be encoded, it can be scaled and repeated. The hypothesis graph encodes it: perturb, classify the shape, follow the edge. An agent that runs this loop doesn't need intuition; it needs perturbation access and a classifier.

If we can poke it, we know how to know.
