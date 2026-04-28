---
variant: post-medium
title: "The Hypothesis Graph"
tags: cognition, methodology
---

*Part of the [cognition](/cognition) series. Sequel to [Evidence has a trajectory](/evidence-has-a-trajectory).*

---

The [previous post](/evidence-has-a-trajectory) argued that p-values compress evidence into a scalar, losing the temporal structure. E-values don't. You can peek at every observation, stop whenever you want, and the error guarantee holds. The trajectory of your evidence is free. Four bins (converge, diverge, oscillate, chaos) tell you how to read it.

A science that produces a boolean (reject or don't) is strictly less interesting than one that also produces hypotheses. A p-value is a verdict: the experiment terminates and nothing points forward. An e-value trajectory is a story. It rose, stalled, oscillated, broke, and the shape contains the next question: conclusions *and* the next experiment to run. Strictly more output from the same input.

There's a structure to what happens after you classify. Not a new one. It's been running for centuries, in lab notebooks, differential diagnoses, debugging sessions. Here's what I see.

### Knowledge is a graph with a frontier

[Belief is the edge of knowing](/belief-is-the-edge-of-knowing). Knowledge is the territory you've mapped. Belief is the boundary: claims you're acting on but haven't tested. The frontier is where belief meets the unknown: edges pointing to experiments nobody has run.

Every experiment is a node, where what you learned is its content and open questions become edges pointing outward. Call it the hypothesis graph.

A mechanic taps the alternator and the engine stalls. That's a node, and it generates two edges: test the battery, test the voltage regulator. The frontier advanced.

A doctor orders bloodwork and sees elevated troponin. That's a node. It generates edges: echocardiogram, stress test, catheterization. The shape of the result (not just "elevated" but *how* elevated, *how fast* it rose, *whether it's still rising*) determines which edges exist.

Every diagnostician reads the shape, not the result. The shape tells them where the frontier is.

<img src="/assets/hypothesis-graph.svg" alt="The hypothesis graph: existing knowledge fades above, current classification branches into validated edges and killed tests, kill conditions generate fresh frontier nodes below" style="max-width: 500px; margin: 1.5em auto; display: block;" />

### The algorithm already running

The structure is the same everywhere:

1. Pick a frontier node. (Choose what to test next.)
2. Perturb the system. (Run the experiment.)
3. Classify the response. (Read the shape.)
4. Generate edges. (The shape names the open questions.)
5. Repeat until the frontier stops expanding.

Nobody invented this. Doctors call it differential diagnosis. Engineers call it fault isolation. Toddlers call it playing.

I went looking for the mechanism in the sensemaking literature. [Weick](https://en.wikipedia.org/wiki/Sensemaking) calls the loop enactment, [Klein](https://en.wikipedia.org/wiki/Recognition-primed_decision) recognition-primed decision, [Boyd](https://en.wikipedia.org/wiki/OODA_loop) OODA. They describe it in prose but never name the mechanism: how does the shape of a result generate the next question?

### Kill conditions generate edges

The [previous post](/evidence-has-a-trajectory) described four trajectory bins: converge, diverge, oscillate, chaos. The [experiment](https://github.com/kimjune01/e-value-trajectory) classifies them using a kill-condition decision tree:

1. Test for monotone trend. If it fails → skip to periodicity.
2. If monotone, test curvature. Decelerating → convergent. Constant → divergent.
3. Test for spectral peaks. Narrow peak → oscillatory.
4. Test for aperiodic structure → aperiodic.
5. Nothing triggered → null.

Here's what I noticed. Each test that fires produces a label. Each test that *misfires* produces a hypothesis, an edge pointing to an experiment that would resolve it.

"Monotone trend detected, curvature indeterminate" → *Is this system decelerating or drifting?* Run a longer experiment.

"Spectral peak detected but broad" → *Is this a noisy cycle or colored noise?* Test at a different frequency.

"Nothing triggered" → *Null, or wrong perturbation site?* Test a different node.

The failure mode names the next hypothesis, and that's the edge-generation mechanism. Same structure as [The Proof Manual](/the-proof-manual): when induction fails because the residual loses structure, the failure mode names the escalation: try a potential method. A trend test can't distinguish acceleration from deceleration? Check curvature. Kill conditions are the universal edge-generation rule. Doctors learn them by apprenticeship, mathematicians by getting stuck. Nobody seems to have written it down.

| Classification | What it tells you | What to try next |
|---|---|---|
| Convergent | Something absorbed the perturbation | Test a different node |
| Divergent | This is load-bearing, no backup | Test what depends on it |
| Oscillatory | Two subsystems fighting | Test the interface |
| Aperiodic | Input exceeds architecture capacity | Decompose differently |

### Why e-values

Each node uses a different instrument, measures a different quantity, tests a different hypothesis. You can't add fish counts to temperature readings. You can't combine p-values from adaptive experiments without inflating error.

E-values compose: their product remains valid even when each experiment was chosen based on the last ([Grünwald et al., 2024](https://academic.oup.com/jrsssb/article/86/5/1091/7623686)). The composed trajectory across all nodes carries the system's dynamics, weighting each stream by its informativeness. Good diagnosticians already do this. The math confirms it.

The [experiment](https://github.com/kimjune01/e-value-trajectory) tested this. Five sensor streams (normal, Poisson, exponential, Bernoulli, lognormal) sharing a weak forcing signal, each individually undetectable. Composed e-values classified the forcing pattern at F1 = 0.996 across four bins (convergent, divergent, oscillatory, aperiodic). Standardized sums: 0.478. Individual streams: 0.279. Composition reveals shared forcing that individual streams miss because the likelihood ratio weights each stream by its informativeness. Fisher information weighting gives the informative experiments more say.

### Null results aren't empty

In the p-value framework, a null result is a dead end. You failed to reject. You move on.

But the e-value trajectory of that null has a shape. The trajectory didn't grow, but *how* it didn't grow is diagnostic:

- **Oscillating null:** the effect waxes and wanes. You tested at the wrong timescale. Edge: test at a different frequency.
- **Converging null:** there was an early signal that decayed. The system compensated. Edge: test the compensating mechanism.
- **Trending-then-reversed null:** the effect is real but transient. Edge: test the reversal point.
- **Flat null:** genuinely nothing. Dead end.

Only the flat null is a dead end. The other three are edges, lost in the compression to "fail to reject."

### Failed replications aren't ambiguous

A "failed replication" in the p-value framework is a single bit: the original said yes, the replication said no. Was the original wrong? Was the replication underpowered? Did the system change? The boolean can't say.

The e-value trajectories of both experiments constrain the answer. If the replication oscillates where the original was monotone, the system changed because something introduced feedback. If the replication converges where the original diverged, something is now compensating, and matching shapes with lower amplitude mean the effect is real but weaker.

How they disagree constrains *why* they disagree, and that constraint is the next hypothesis. Trajectories carry evidence about the mechanism of disagreement. Booleans don't.

### Fixpoint

The graph converges when every frontier edge points to a node already tested and stably classified. No new questions. That's a fixpoint.

Does this always happen? If every reachable node is visited, classifications are consistent, and composed e-values preserve the regime's signature, the sequence converges to the true map. Anytime validity means you can check at every node without inflating error.

I don't have a theorem. I have the observation that good diagnosticians do this and converge. The pieces exist: [Chernoff](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-30/issue-3/Sequential-Design-of-Experiments/10.1214/aoms/1177706205.full) proved adaptive experiment selection converges, [He & Geng](https://jmlr.org/papers/v9/he08a.html) proved adaptive interventions recover causal structure, [Grünwald](https://academic.oup.com/jrsssb/article/86/5/1091/7623686) proved e-values compose across adaptive experiments. No published theorem connects them. One would formalize what practitioners already do.

### Not a proposal

An observation.

The algorithm already runs. Every time a doctor reads a lab result and decides what to order next, every time an engineer sees a fault and decides what to probe, every time a scientist gets a null and decides whether to replicate, redesign, or move on. [Science on trial](/science-on-trial) described the protocol: prereg, red-team, work log, publish all. This post describes what the protocol protects: the edge-generation loop that advances the frontier.

[Popper](https://www.cambridge.org/core/journals/dialogue-canadian-philosophical-review-revue-canadienne-de-philosophie/article/idea-of-a-logic-of-discovery/5E31DF041E9E6B5D31EA79C6C06B065E) was right that there's no logical method of having new ideas from nothing. But they don't come from nothing; they come from the shape of what the last experiment told you. The failure mode of the current test names the next hypothesis. That's not creativity, that's structure.

For any system you can perturb, the hypothesis graph decomposes it. Each perturbation produces a node, each classification generates edges, and the edges name the next perturbations. The graph expands until it covers the system's structure, or until you hit a boundary you can't perturb past.

The limits are real. You need perturbation access (can't poke what you can't reach). You need independence between streams (correlated sensors weaken composition). You need identifiability (some systems look the same under all perturbations). Within those limits, the algorithm can converge. Outside them, it tells you where you're stuck and why, which is itself an edge.

Engineered systems are fully within the limits. You built the feedback loops. You know the graph. Every unexpected state is a free perturbation, every test failure is a node, and every failure mode is an edge. The hypothesis graph is how engineered complexity becomes legible: one perturbation at a time, with the kill condition telling you where to cut next.

The frontier isn't a metaphor. It's the set of edges pointing to experiments nobody has run. The p-value answers a question. The e-value trajectory answers it and asks the next one. Strictly more science from the same experiment.
