---
variant: post-medium
title: "Evidence has a trajectory"
tags: cognition, reflecting
---

*Part of the [cognition](/cognition) series.*

Suppose you run an A/B test on two code variants. B converts 12% better than A, p < .01, sample size 50,000. You ship B. Obviously.

### Is measuring believing?

A/B testing assumes two things: [stationarity](https://en.wikipedia.org/wiki/Stationary_process) (the effect doesn't change over the test window) and [no interference](https://en.wikipedia.org/wiki/Rubin_causal_model#Stable_unit_treatment_value_assumption) (each unit's outcome is independent of every other's). Both reduce to: no feedback. The treatment enters, the outcome exits, nothing loops back. If the system has feedback, both assumptions are false. The test result is a snapshot of a trajectory you didn't observe.

#### Google

[A/B-tested ad load](https://dl.acm.org/doi/abs/10.1145/2783258.2788583): more ads, more revenue, ship it. Long-term measurement revealed the feedback loop that the snapshot missed: users learned to ignore ads, CTR degraded over months, and Google cut mobile ad load by 50%.

#### Boeing

[MCAS](https://en.wikipedia.org/wiki/Maneuvering_Characteristics_Augmentation_System) read a single sensor snapshot: nose too high, push it down. Correct response, wrong sensor. The system looped: MCAS pushed down, pilots trimmed up, MCAS pushed again. Oscillation. Two subsystems fighting. 346 dead. Nobody was watching the trajectory.

#### Vioxx

[Passed its 9-month trial](https://en.wikipedia.org/wiki/Rofecoxib): fewer GI bleeds than naproxen, ship it. The cardiovascular risk emerged at 18 months, past the trial window. Cumulative thrombotic damage, invisible in the snapshot. [88,000–140,000 excess coronary events](https://doi.org/10.1016/S0140-6736(05)17864-5) before the drug was pulled.

The reductio: "doing drugs made me feel great" is a directional prediction with a two-week window applied to a system with catastrophic positive feedback. The snapshot is true. The trajectory is addiction.

This is [Meehl's structural flaw](/reading/scientific-method/meehl-1967/) at scale. In 1967 he showed that directional predictions in soft psychology corroborate nothing because the crud factor guarantees significance. The same structure (directional prediction, snapshot window, no trajectory) now ships products and drugs. Soft psychology published non-replicable findings. Engineering adopted the epistemology and ships the results.

### Passive vs. active

Statistics is passive. You observe, tabulate, infer. A [p-value](https://en.wikipedia.org/wiki/P-value) is computed once, at a predetermined moment, from a fixed sample. Peek mid-experiment and the guarantee breaks. The framework assumes you watch without touching.

Actuaries need this because they can't cause the events they study. They can't perturb deaths for experiments. Statistics is the epistemology of observers who can't intervene.

Everyone who can intervene has a better option. Poke the system and watch. A toddler already knows this: poke a tower of blocks, see if it wobbles back (stable), falls (load-bearing), or keeps rocking (interesting). Three bins, no p-value, no pre-registration. We knew the protocol before we had language. Then we grew up and replaced it with snapshots.

[Pearl](/reading/scientific-method/pearl-2000/) formalized the poke. The [do-calculus](https://en.wikipedia.org/wiki/Do-calculus) tells you what happens when you reach in and force a variable to change. But Pearl's framework requires a [directed *acyclic* graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph). Most real systems have feedback. Pearl brought back the poke. He left out the part where the thing pokes back.

### Four bins

Perturb a cyclic system. Observe the response. For [linear systems](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors), the eigenstructure determines the outcome: divergence (positive real eigenvalues), convergence (negative real), or oscillation (complex). Nonlinear systems add a fourth: [chaos](https://en.wikipedia.org/wiki/Chaos_theory), bounded but aperiodic, where the trajectory never settles and never repeats.

Four bins of triage, not four bins of truth.

<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 0.5em; max-width: 500px; margin: 1em auto;">
<img src="/assets/trajectory-convergence.svg" alt="Convergence: perturbation settles back to baseline" />
<img src="/assets/trajectory-divergence.svg" alt="Divergence: perturbation accelerates away" />
<img src="/assets/trajectory-oscillation.svg" alt="Oscillation: perturbation cycles periodically" />
<img src="/assets/trajectory-chaos.svg" alt="Chaos: bounded but aperiodic trajectory" />
</div>

The classification tells you which log to read next.

<table style="max-width:600px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col><col style="width:10em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Response</th><th style="background:#f0f0f0">Diagnosis</th><th style="background:#f0f0f0">Next experiment</th></tr></thead>
<tr><td>Convergence</td><td>Stable. Redundancy or compensation</td><td>Test a different node</td></tr>
<tr style="background:#f8f8f8"><td>Divergence</td><td>Load-bearing. No backup</td><td>Test its dependencies</td></tr>
<tr><td>Oscillation</td><td>Two subsystems fighting</td><td>Test the interface</td></tr>
<tr style="background:#f8f8f8"><td>Chaos</td><td>Input exceeds architecture capacity</td><td>Decompose differently</td></tr>
</table>

Over iterations, each perturbation-response sharpens the cycle map. You start with domain knowledge and end with tested structure.

### The bet

A formal framework bridges passive statistics and active dynamics: [e-values](https://en.wikipedia.org/wiki/E-value_(statistics)) and [supermartingales](https://en.wikipedia.org/wiki/Martingale_(probability_theory)).

A p-value is a snapshot: collect a fixed sample, compute once, decide. An [e-value](https://arxiv.org/abs/1906.07801) is a trajectory: evidence accumulates over time. You can stop whenever you want, peek whenever you want, and the error guarantee holds. [Anytime-valid inference](https://arxiv.org/abs/2103.06476). The evidence *is* the trajectory.

E-values compose. If experiment A produces evidence $e_1$ and experiment B produces $e_2$, the product $e_1 \times e_2$ is also valid evidence. Sequential experiments compose multiplicatively. The [supermartingale](https://en.wikipedia.org/wiki/Martingale_(probability_theory)#Submartingales,_supermartingales,_and_relationship_to_harmonic_functions) property guarantees it: if you're betting honestly and the null is true, your wealth can't grow on average.

A p-value compresses evidence to a single number at a single moment. Why? Because the guarantee demands it. Peek mid-experiment and the false positive rate inflates. So you don't peek. You wait, compute once, and get a scalar. The temporal structure was in the data the whole time. The method threw it away because the math required it.

Anytime validity removes that requirement. You can check at every observation and the error guarantee holds at each one. The trajectory is free — not a bonus feature, but the natural state of evidence that the p-value workflow was artificially suppressing. Pearl said stop observing and intervene. The same logic, one level up: stop compressing your evidence into a scalar and look at it.

This is a mathematical property of the two frameworks, not an empirical finding. A p-value is a lossy compression of evidence over time into a scalar. An e-value stream is evidence over time. The system's dynamics are in the temporal structure. Compress to a scalar and they're gone. Keep the stream and they're there. No experiment needed to see why.

Point an e-value at a cyclic system and the evidence trajectory inherits the dynamics. Test whether smoking reduces stress: the e-value climbs after each cigarette (relief), falls during withdrawal (stress spikes), climbs on relapse. The oscillation in your confidence *is* the addiction cycle. A two-week snapshot would say "smoking reduces stress, p < .05." The e-value trajectory shows the loop, if the experiment samples across it.

The four-bin classification applies directly. E-values preserve a time-indexed evidence process. If the betting strategy is well matched to the perturbation, the trajectory exposes dynamics that a terminal scalar hides. Once you have the trajectory, the bins tell you how to read it: convergence, divergence, oscillation, chaos. Not four possible conclusions — four modes of sensemaking. Each one tells you what kind of system you're dealing with and what to try next.

### Where it holds, where it doesn't

Engineered systems are the best case. You have perturbation access and partial design knowledge. [Decompose](https://en.wikipedia.org/wiki/Strongly_connected_component) into cyclic components and the DAG connecting them. Apply Pearl to the acyclic parts, perturbation-response to each cycle. An agent architecture is an engineered system. Every unexpected game state is a free perturbation experiment. The environment *is* the experiment.

Natural systems with unknown structure: partially. You need causal knowledge to know where one cycle ends and another begins, but cycle-testing is how you're supposed to get causal knowledge. In domains where cycle boundaries are unknown (macroeconomics, climate, cognition at scale), isolation is genuinely hard. The gap isn't theoretical. It's experimental: can you isolate the cycle?

### Fuck around and find out

<table style="max-width:500px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Framework</th><th style="background:#f0f0f0">Method</th><th style="background:#f0f0f0">Sample size</th></tr></thead>
<tr><td>Frequentist</td><td>Fixed</td><td>Fixed</td></tr>
<tr style="background:#f8f8f8"><td>Bayesian</td><td>Fixed</td><td>Variable</td></tr>
<tr><td>E-value</td><td>Variable</td><td>Variable</td></tr>
</table>

Frequentist: lock the method, lock n, compute once. Bayesian: lock the method, let n vary. E-values: change your test, your sampling strategy, your hypothesis mid-stream, and the evidence still composes. The supermartingale guarantee holds regardless. You can't do "fuck around and find out" with a fixed method. You need the freedom to change what you're doing based on what you're learning.

E-values let you buy evidence in installments. Ten small experiments, each isolating one variable, tracked over time. The evidence composes multiplicatively. Each trajectory tells you whether the variable is causal (diverges), confounded (stalls), or cyclically entangled (oscillates). Enough cheap experiments and the trajectories bisect the causal structure.

You run an A/B test. Variant B converts 12% better. You ship B. But did you watch the bet?

Statistics watches. Dynamics pokes. The poke is the knowledge.

### Two open questions

- Can we read the *shape* of an e-value trajectory to diagnose the system, not just test the hypothesis? Oscillation in your evidence might reveal the cycle before the test converges.
- The math for classifying iterative sequences already exists (convergence rate, [Lyapunov exponents](https://en.wikipedia.org/wiki/Lyapunov_exponent), stability analysis). Can we apply it to evidence trajectories? I haven't seen it done.

*After writing this, I ran the experiment. Sequel: [The Hypothesis Graph](/the-hypothesis-graph).*
