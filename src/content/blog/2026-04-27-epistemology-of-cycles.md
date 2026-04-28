---
variant: post-medium
title: "Epistemology of cycles"
tags: cognition, reflecting
---

*Part of the [cognition](/cognition) series.*

You run an A/B test. Variant B converts 12% better than A, p < .01, sample size 50,000. You ship B. Obviously.

### A/B tests

A/B testing assumes [stationarity](https://en.wikipedia.org/wiki/Stationary_process) (the treatment effect doesn't change over the test window) and [no interference](https://en.wikipedia.org/wiki/Rubin_causal_model#Stable_unit_treatment_value_assumption) (each unit's outcome is independent of every other unit's assignment). Both reduce to the same thing: no feedback. The treatment enters, the outcome exits, nothing loops back. If the system has feedback, both assumptions are false and the test result is a snapshot of a trajectory you didn't observe.

[Google A/B-tested ad load](https://dl.acm.org/doi/abs/10.1145/2783258.2788583): more ads, more revenue, ship it. Long-term measurement revealed the feedback loop the snapshot missed: users learned to ignore ads, CTR degraded over months, and Google cut mobile ad load by 50%.

[Boeing's MCAS](https://en.wikipedia.org/wiki/Maneuvering_Characteristics_Augmentation_System) read a single sensor snapshot: nose too high, push it down. Correct response, wrong sensor. The system looped: MCAS pushed down, pilots trimmed up, MCAS pushed again. Oscillation. Two subsystems fighting. 346 dead. Nobody was watching the trajectory.

[Vioxx](https://en.wikipedia.org/wiki/Rofecoxib) passed its 9-month trial: fewer GI bleeds than naproxen, ship it. The cardiovascular risk emerged at 18 months, past the trial window. Cumulative thrombotic damage, invisible in the snapshot. [88,000–140,000 excess coronary events](https://doi.org/10.1016/S0140-6736(05)17864-5) before the drug was pulled.

The reductio: "doing drugs made me feel great" is a directional prediction with a two-week window applied to a system with catastrophic positive feedback. The snapshot is true. The trajectory is addiction.

This is [Meehl's structural flaw](/reading/scientific-method/meehl-1967/) at scale. In 1967 he showed that directional predictions in soft psychology corroborate nothing because the crud factor guarantees significance. The same structure (directional prediction, snapshot window, no trajectory) now ships products and drugs. Soft psychology published non-replicable findings. Engineering adopted the epistemology and ships the results.

### Passive vs. active

Statistics is passive. You observe, tabulate, infer. A [p-value](https://en.wikipedia.org/wiki/P-value) is computed at one predetermined moment from a fixed sample. If you peek mid-experiment, the guarantee breaks. The entire framework assumes you watch without touching.

Actuaries need this because they can't cause the events they study. They can't run experiments on deaths. Statistics is the epistemology of observers who can't intervene.

Everyone who can intervene has a better option. Poke the system and watch. A toddler already knows this: poke a tower of blocks, see if it wobbles back (stable), falls (load-bearing), or keeps rocking (interesting). Three bins, no p-value, no pre-registration. We knew the protocol before we had language. Then we grew up and replaced it with snapshots.

[Pearl](/reading/scientific-method/pearl-2000/) formalized the poke. The [do-calculus](https://en.wikipedia.org/wiki/Do-calculus) tells you what happens when you reach in and force a variable to change. But Pearl's framework requires a [directed *acyclic* graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph). Most real systems have feedback. Pearl brought back the poke. He left out the part where the thing pokes back.

### Four bins

Perturb a cyclic system and observe the response. For [linear systems](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors), the eigenstructure determines the outcome: divergence (positive real eigenvalues), convergence (negative real eigenvalues), or oscillation (complex eigenvalues). Nonlinear systems add a fourth class: [chaos](https://en.wikipedia.org/wiki/Chaos_theory), bounded but aperiodic, where the trajectory never settles and never repeats.

Agent is stuck: is it converging slowly (wait), diverging (intervene now), oscillating (two subsystems are fighting, find the conflict), or chaotic (the input space exceeds the architecture's capacity)? Four bins of triage, not four bins of truth. The classification tells you which log to read next.

Each response class constrains the next experiment. Convergence after ablation means redundancy: test a different node. Divergence means you found something load-bearing: test its dependencies. Oscillation means two subsystems are fighting: test the interface. Over iterations, each perturbation-response sharpens the cycle map. You start with domain knowledge and end with tested structure.

### The bet

There's a formal framework that bridges passive statistics and active dynamics: [e-values](https://en.wikipedia.org/wiki/E-value_(statistics)) and [supermartingales](https://en.wikipedia.org/wiki/Martingale_(probability_theory)).

A p-value is a snapshot: collect a fixed sample, compute once, decide. An [e-value](https://arxiv.org/abs/1906.07801) is a trajectory: evidence accumulates over time. You can stop whenever you want, peek whenever you want, and the error guarantee holds. [Anytime-valid inference](https://arxiv.org/abs/2103.06476). The evidence *is* the trajectory.

E-values compose. If experiment A produces evidence $e_1$ and experiment B produces $e_2$, the product $e_1 \times e_2$ is also valid evidence. Sequential experiments compose multiplicatively. The [supermartingale](https://en.wikipedia.org/wiki/Martingale_(probability_theory)#Submartingales,_supermartingales,_and_relationship_to_harmonic_functions) property guarantees it: if you're betting honestly and the null is true, your wealth can't grow on average.

A p-value compresses your evidence into a single number at a single moment. An e-value preserves the trajectory. It represents your confidence at a granularity where the system's dynamics show through.

Point an e-value at a cyclic system and the evidence trajectory inherits the dynamics. Test whether smoking reduces stress: the e-value climbs after each cigarette (relief), falls during withdrawal (stress spikes), climbs on relapse. The oscillation in your confidence *is* the addiction cycle. A two-week snapshot would say "smoking reduces stress, p < .05." The e-value trajectory shows the loop, if the experiment samples across it.

The four-bin classification applies to e-values when the experiment tracks the system's dynamics. E-values are granular enough to transmit what the system is doing without compressing it to a single number. Convergence, divergence, oscillation in your evidence tells you which mode the system is in. P-values destroy this signal. E-values preserve it.

### Where it holds, where it doesn't

Engineered systems: cleanly. You built the feedback loops, you know the graph. [Decompose](https://en.wikipedia.org/wiki/Strongly_connected_component) into cyclic components and the DAG connecting them. Apply Pearl to the acyclic parts, perturbation-response to each cycle. An agent architecture is an engineered system. Every unexpected game state is a free perturbation experiment. The environment *is* the experiment.

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

Two open questions. First: can we read the *shape* of an e-value trajectory to diagnose the system, not just test the hypothesis? Oscillation in your evidence might reveal the cycle before the test converges. Second: the math for classifying iterative sequences already exists (convergence rate, [Lyapunov exponents](https://en.wikipedia.org/wiki/Lyapunov_exponent), stability analysis). Can we apply it to evidence trajectories? I haven't seen it done.
