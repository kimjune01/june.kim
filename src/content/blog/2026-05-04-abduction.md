---
variant: post-wide
title: "Abduction"
tags: methodology, epistemology
---

*Part of the [cognition](/cognition) series. Sequel to [Modes of Reason](/modes-of-reason).*

A mechanic taps the alternator and the engine stalls. Two hypotheses fire: test the battery, test the voltage regulator. Nobody taught the mechanic a hypothesis-generation algorithm. The shape of the failure named the next experiment.

If no mechanism for generating deliberate follow-up hypotheses exists, every intuition would arrive at random, in arbitrary order. But science's knowledge graph keeps expanding, and attention drives connections between experiments. So the mechanism is real. Can we formalize and encode it?

### The logical primitive

Two samples, one before and one after, and a diff. What flipped is figure; what held is ground. If that operation is encodable, the loop closes.

Every car on the road already runs this. [OBD-II](https://en.wikipedia.org/wiki/On-board_diagnostics#OBD-II) reads sensor states, diffs against expected values, and generates fault codes: the mechanic's intuition, mechanized since 1996. But OBD-II is hardcoded: the fault tree is hand-authored, the hypotheses enumerated in advance. The primitive works; it just never left the engine bay. The same abstraction that tells a mechanic "test the alternator next" is what ML has no general interface for.

The intuition underneath is **diff**: snapshot before, snapshot after, XOR. The prefixes are degrees of freedom:

- Unary diff (one before, one after) → one frame
- Bi-abduction → infer frame autonomously from observation
- Incorrectness → flip polarity (attend to failure, not success)
- Tri-abduction → diff across branches (cause vs counterfactual)

Each step adds an operand. One snapshot pair → one frame. Two pairs (actual and counterfactual) → one causal edge. N pairs across N branches → a typed subgraph. The pattern stays diff; the arity grows. Everything past the minimal diff is optimization: more samples ([Ernst/Daikon](https://dl.acm.org/doi/10.1145/302405.302467)), autonomous frame inference ([bi-abduction](https://dl.acm.org/doi/10.1145/1480881.1480917)), flipped polarity ([incorrectness](https://dl.acm.org/doi/10.1145/3371078)), branching ([tri-abduction](https://arxiv.org/abs/2305.04842)). The primitive already works at two samples.

### Bi-abduction

<div style="margin: 2em auto;">
<img src="/assets/bi-abduction.svg" alt="Bi-abduction: before and after snapshots of an engine, XOR produces figure (alternator changed) and ground (battery, fuel, spark unchanged)" />
</div>

---

### Tri-abduction

<div style="margin: 2em auto;">
<img src="/assets/tri-abduction.svg" alt="Tri-abduction: fork from shared start into two branches — tap alternator (engine stalls) vs tap radiator (engine runs), converging into a causal edge" />
</div>

### Three witnesses

[Infer](https://fbinfer.com/) (Facebook, from [Calcagno et al. 2009](https://dl.acm.org/doi/10.1145/1480881.1480917)): bi-abduction running in production on millions of lines of code. Formal observation + formal goal → formal hypothesis. The primitive, deployed.

[Voyager](https://arxiv.org/abs/2305.16291) (Wang et al. 2023): GPT-4 observes failure, proposes a fix, self-verifies, commits to a skill library. The loop closes on its own. 180 verified skills in Minecraft. LLM as abduction engine.

[IRM](https://arxiv.org/abs/1907.02893) (Arjovsky et al. 2019): invariant feature separation across training environments. Use environment variation as the lever to force figure/ground separation. The ML field's version, closest to scaling.

Three fields, three encodings, zero cross-citation. [Peirce](https://archive.org/details/pragmatismasprin0000peir) named the genus in 1903. Everyone else described their species.

### The monad move

Instead of arguing whether SOAR's chunking and bi-abduction are "the same operation," encode abduction as a typed primitive and run it. Let results settle the debate. The artifact is the crosswalk.

`abduct_candidates(observation, target) → list[Candidate]`. The test is both the evidence and the argument.

### The missing mode

[The Bitter Lesson](http://www.incompleteideas.net/IncsightBlurb/SBLPblurb.html) says general methods leveraging computation beat hand-engineered knowledge. The lesson is right. It's about induction. Scale the data, scale the compute, let the model find the pattern. The entire scaling-laws era is mode two applied.

But induction doesn't generate hypotheses. It generalizes from examples someone already chose. The question of *which* experiment to run next, *which* data to collect, *which* perturbation to try. That's outside the lesson's frame. Induction scales within a research program. Abduction generates research programs.

Every capability curve is a sigmoid. The market prices the steep part and extrapolates a line. When the curve flattens, the marginal return on scaling induction drops. The mechanism that finds the *next* sigmoid: the next architecture, the next question, the next perturbation that starts a new curve. That's mode three. ML has deduction (type checkers, provers) and induction (everything since the perceptron). The third mode is the gap.

What happens when you point it at a human playthrough, or ten thousand RL rollouts?

---

## Edit (2026-07-03): I had the primitive backwards

I identified abduction with the diff, and that was wrong. The diff, figure against ground, XOR, is real, but it is not the abductive act. It is the *surprise*: the place where what I believed and what the world returned diverge. That is the input to abduction, the counterexample, not the leap that answers it. Peirce's schema is the surprising fact C observed, A would explain C, so suspect A. The diff hands you C. Abduction is the guess at A, and no operation above delivers A.

The word fooled me. "Bi-abduction" in separation logic (Infer) is a term of art for inferring a missing frame. It is not Peirce's abduction, and building an arity ladder on the shared word welded two different things together. Most of the species I listed are the surprise machinery, the localization that shows where belief and world part. Voyager is the exception, and it is the exception because the leap lives in the model, unspecified, where it has to.

`abduct_candidates(observation, target) → list[Candidate]` is the eager mistake in one line. It promises to hand back the candidate list. When the search space is not enumerable, no function does. You guess wildly and rank, and the economy of research runs one level down, inside the generation, governing which wild guesses survive. The ranking you can partly write down: cost, testability, breadth. The plausibility call under it, *this one smells right*, you cannot, and it recedes another level each time you reach for it. Whatever I managed to mechanize turned out to be deduction or induction. The residue that resists is abduction.

What still stands is the missing mode. Induction generalizes from examples someone already chose; abduction generates the programs and finds the next sigmoid. That claim survives untouched. I just had the primitive inside out: the diff detects the surprise, and abduction is the leap I cannot reduce to a diff.
