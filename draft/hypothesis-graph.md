---
variant: post-medium
title: "The Hypothesis Graph"
tags: cognition, methodology
---

*Part of the [cognition](/cognition) series. Sequel to [Evidence has a trajectory](/evidence-has-a-trajectory).*

---

A science that produces a boolean — reject or don't — is strictly less interesting than a science that produces hypotheses alongside its conclusions.

A p-value is a verdict. You run the experiment, compute the number, decide. The experiment terminates. Nothing points forward.

An e-value trajectory is a story. It rose, stalled, oscillated, broke. The shape of that story contains the next question. A science built on trajectories doesn't just produce conclusions. It produces conclusions *and* the next question to investigate. Strictly more output from the same input.

[Popper](https://www.cambridge.org/core/journals/dialogue-canadian-philosophical-review-revue-canadienne-de-philosophie/article/idea-of-a-logic-of-discovery/5E31DF041E9E6B5D31EA79C6C06B065E) said there is no logical method of having new ideas. [Witten](https://www.kyotoprize.org/en/science-helps-us-understand-the-world-better/) said the hardest thing about research is finding the right question. They're describing something that already happens — scientists generate hypotheses constantly. They just can't say how.

I think there's a structure to it. Not a new one. One that's been running for centuries, implicit in every lab notebook, every differential diagnosis, every debugging session. I'm going to try to describe what I see.

### Knowledge is a graph with a frontier

[Belief is the edge of knowing](/belief-is-the-edge-of-knowing). Knowledge is the territory you've mapped. Belief is the boundary — the claims you're acting on but haven't fully tested. The frontier is where belief meets the unknown: edges pointing to experiments nobody has run.

Every experiment is a node. The result — what you learned — is the node's content. The open questions it generates are the edges pointing outward.

A mechanic taps the alternator and the engine stalls. That's a node. It generates two edges: test the battery, test the voltage regulator. Those edges point to experiments that haven't happened yet. The frontier advanced.

A doctor orders bloodwork and sees elevated troponin. That's a node. It generates edges: echocardiogram, stress test, catheterization. The shape of the result — not just "elevated" but *how* elevated, *how fast* it rose, *whether it's still rising* — determines which edges exist.

This is what every diagnostician does. They don't just read the result. They read the shape of the result, and the shape tells them where the frontier is.

### The algorithm that's already running

The structure is the same everywhere:

1. Pick a frontier node. (Choose what to test next.)
2. Perturb the system. (Run the experiment.)
3. Classify the response. (Read the shape.)
4. Generate edges. (The shape names the open questions.)
5. Repeat until the frontier stops expanding.

Nobody invented this. Doctors call it differential diagnosis. Engineers call it fault isolation. Scientists call it the scientific method. Mechanics call it troubleshooting. Toddlers call it playing.

The sensemaking literature gives it names — Weick calls it enactment, Klein calls it recognition-primed decision, Boyd calls it OODA. They describe it in prose. None of them describe the edge-generation mechanism: how does step 3 produce step 4? How does the shape of a result name the next question?

### Kill conditions generate edges

The [previous post](/evidence-has-a-trajectory) described four bins for classifying a trajectory: converge, diverge, oscillate, chaos. The [experiment](https://github.com/kimjune01/e-value-trajectory) built a classifier that assigns one of these labels using a kill-condition decision tree:

1. Test for monotone trend. If it fails → skip to periodicity.
2. If monotone, test curvature. Decelerating → convergent. Constant → divergent.
3. Test for spectral peaks. Narrow peak → oscillatory.
4. Test for aperiodic structure → aperiodic.
5. Nothing triggered → null.

Each test that fires produces a label. Each test that *fails* produces a reason. That reason is an open question — an edge pointing to an experiment that would resolve it.

"Monotone trend detected, curvature indeterminate" → *Is this system decelerating or drifting?* Run a longer experiment.

"Spectral peak detected but broad" → *Is this a noisy cycle or colored noise?* Test at a different frequency.

"Nothing triggered" → *Genuinely null, or wrong perturbation site?* Test a different node.

The failure mode names the next hypothesis. This is the edge-generation mechanism. It's the same structure as [The Proof Manual](/the-proof-manual): in mathematics, when induction fails because the residual loses structure, the failure mode names the escalation — try a potential method. In diagnosis, when a trend test fails because it can't distinguish acceleration from deceleration, the failure mode names the next test — check curvature. Kill conditions are the universal edge-generation rule. Doctors learn them by apprenticeship. Mathematicians learn them by getting stuck. It was always an algorithm. Nobody wrote it down.

| Classification | What it tells you | What to try next |
|---|---|---|
| Convergent | Something absorbed the perturbation | Test a different node |
| Divergent | This is load-bearing, no backup | Test what depends on it |
| Oscillatory | Two subsystems fighting | Test the interface |
| Aperiodic | Input exceeds architecture capacity | Decompose differently |

### Null results aren't empty

A null result in the p-value framework is a dead end. You failed to reject. You move on.

But the e-value trajectory of that same experiment has a shape. A null result means the trajectory didn't grow — but *how* it didn't grow is diagnostic:

- **Oscillating null:** the effect waxes and wanes. You tested at the wrong timescale. Edge: test at a different frequency.
- **Converging null:** there was an early signal that decayed. The system compensated. Edge: test the compensating mechanism.
- **Trending-then-reversed null:** the effect is real but transient. Edge: test the reversal point.
- **Flat null:** genuinely nothing. Dead end.

One of these is a dead end. The other three are edges. The p-value framework sees all four as the same: "fail to reject." Three research programs are lost in the compression.

### Failed replications aren't ambiguous

A "failed replication" in the p-value framework is a single bit: the original said yes, the replication said no. Was the original wrong? Was the replication underpowered? Did the system change? The boolean can't say.

The e-value trajectories of both experiments carry the answer. If the replication oscillates where the original was monotone, the system changed — something introduced feedback. If the replication converges where the original diverged, something is now compensating. If the shapes match but the amplitude is lower, the effect is real but weaker.

The shape of the disagreement diagnoses *why* they disagree. That diagnosis is the next hypothesis. The replication crisis isn't just about whether effects are real. It's about what changed when they stopped being real. The trajectories carry that information. The booleans don't.

### Why e-values

Each node in the graph uses a different instrument, measures a different quantity, tests a different hypothesis. You can't add fish counts to temperature readings. You can't combine p-values from adaptively chosen experiments without inflating error.

E-values compose. The product of e-values from independent experiments is a valid e-value, even when you chose each experiment based on the previous result ([Grünwald et al., 2024](https://academic.oup.com/jrsssb/article/86/5/1091/7623686)). The composed trajectory across all nodes carries the system's dynamics — and the guarantee holds because the supermartingale property doesn't care how you chose your experiments.

This isn't a coincidence. E-values are denominated in evidence. Like money, they have a common unit that lets you add contributions from different sources. A fish count and a temperature reading can't be summed. Their likelihood ratios can. The likelihood ratio is the exchange rate between different kinds of data and a single currency of evidence.

The [experiment](/evidence-has-a-trajectory) showed this: five heterogeneous streams, individually undetectable, composed e-values at 99.6% classification accuracy across all four bins. The likelihood ratio weights each stream by its informativeness — Fisher information weighting, which is just a fancy name for "pay more attention to the more informative experiment." That's what good diagnosticians already do. The math just proves they're right.

### The frontier stops expanding

The graph converges when every frontier edge points to a node that's already been tested and classified stably. No new questions are generated. That's a fixpoint.

Does this always happen? The argument is: if you visit every reachable node, and the classification is consistent (correct label with probability approaching 1 as evidence accumulates), and the composed e-values preserve the regime's signature, then the sequence of classifications converges to the true map. The e-value's anytime validity means you can check at every node without inflating error.

I don't have a theorem. I have the observation that this is what good diagnosticians do, and they converge. The convergence isn't guaranteed by any formal property they can name. It's guaranteed by the structure of the algorithm they're executing without knowing they're executing it.

The pieces exist in the literature — [Chernoff](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-30/issue-3/Sequential-Design-of-Experiments/10.1214/aoms/1177706205.full) proved adaptive experiment selection converges. [He & Geng](https://jmlr.org/papers/v9/he08a.html) proved adaptive interventions recover causal structure. [Grünwald](https://academic.oup.com/jrsssb/article/86/5/1091/7623686) proved e-values compose across adaptive experiments. [Kevrekidis](https://www.sciencedirect.com/science/article/abs/pii/S0167278902007388) showed perturbations find regime boundaries. Nobody has connected them into one theorem. But the algorithm they describe is the same algorithm that every diagnostician runs. The theorem would just prove what practitioners already know works.

### What I'm describing

Not a proposal. An observation.

The algorithm already runs. It runs every time a doctor reads a lab result and decides what to order next. Every time an engineer sees a fault and decides what to probe. Every time a scientist gets a null result and decides whether to replicate, redesign, or move on. [Science on trial](/science-on-trial) described the protocol — prereg, red-team, work log, publish all. This post describes the thing the protocol is trying to protect: the edge-generation loop that advances the frontier. The decisions aren't random. They follow from the shape of the evidence. The shape generates the question. The question selects the next experiment.

If knowledge is a graph with a frontier, and belief is the edge of knowing, then this algorithm — pick a frontier node, perturb, classify the shape, generate edges, repeat — is how the frontier expands. It's been running for as long as people have investigated things. Popper was right that there's no logical method of having new ideas *ex nihilo*. But the next idea doesn't come from nothing. It comes from the shape of what the last experiment told you. The failure mode of the current test names the next hypothesis.

The e-value trajectory makes this legible. The p-value hides it. That's the whole difference. Not a better test. A test that shows you what to do next.
