---
variant: post-wide
title: "Investigate"
tags: methodology, coding
---

*Part of the [methodology](/methodology) series. Sequel to [Abduction](/abduction).*

Software engineering encodes two of the [three modes](/modes-of-reason). Deduction: type checkers, provers, linters. Induction: test suites, benchmarks, CI. [Abduction](/abduction), the third mode, stays manual. A human reads the profile, stares at the flame graph, and has a hunch. What if the hunch had a pipeline?

Coding agents can write code, run tests, and ship PRs. They still need a human to decide *what to fix*. [Abduction](/abduction) argued the primitive is encodable. This post is the encoding. Five stations, one loop. A pipeline from "something is slow" to a mergeable PR, mechanized abduction at the hinge.

### Shape

<div style="max-width:85%; margin:2em auto;">
<img src="/assets/img/investigate-pipeline.svg" alt="Investigate pipeline: Hypothesis, Prework, Benchmark, Bug hunt, Ship. Kill conditions feed back into the hypothesis graph." style="width:100%; display:block;">
</div>

Each station produces a self-contained artifact. Any station can stop and the output stands alone: diagnosis, experiment repo, measurement, convergence report, PR. The [contract](/functor-wizardry) is simple: each station writes everything the next station needs. No hidden state.

The loop is the mechanism. Kill conditions from downstream stations re-enter the [hypothesis graph](/the-hypothesis-graph). The [e-value classification](/evidence-has-a-trajectory) names what happens next: divergent follows the edge, convergent refines, oscillatory splits, chaotic redesigns.

### Hypothesize

Start with a question about a system you can perturb. Isolate the buggy subregion before you fan out (the [delta-debugging](https://en.wikipedia.org/wiki/Delta_debugging) instinct): trace from the symptom to the smallest set of components that could produce it, then [fan out](/fan-out) competing hypotheses inside that region. Fan out in proportion to your uncertainty about where and why: when isolation already pins one cause, a single thread beats parallel hypotheses that only re-derive it. For each one: perturb, measure, classify the [trajectory shape](/evidence-has-a-trajectory), prune. [Abduction](/modes-of-reason) proposes, deduction traces consequences, induction tests. The graph deepens until the [frontier](/belief-is-the-edge-of-knowing) closes or you redirect.

A good investigation attacks its own premise first; if it survives, you weren't adversarial enough.

*Example: I assumed tinygrad's LLaMA gap was realize overhead from novel graph shapes. The investigation killed that premise. The [symbolic JIT](https://github.com/tinygrad/tinygrad/pull/15097) handles varying shapes without recompilation. The gap was elsewhere.*

### Prework

When a surviving hypothesis implies a code change, build the [prework](/prework) before touching production: reference implementation, candidate fix as a pure function, compatibility suite, extraction script that confirms the bug exists in the target.

The extraction script is the derisk. If it doesn't confirm the bug, the diagnosis was wrong. Re-enter the hypothesis graph.

*Example: `extract.py` dumped the generated Metal kernel and showed stride-32768 in the inner loop. 87% of every cache line wasted. The bug was confirmed, not hypothetical.*

### Benchmark

Implement the minimal fix, measure before and after, and classify the benchmark trajectory as you would any [e-value](/evidence-has-a-trajectory):

- **Divergent improvement** on all tested cases → proceed.
- **Oscillatory** (helps some cases, hurts others) → the fix is too coarse. Re-enter the hypothesis graph. Split.
- **No improvement** → the diagnosis was wrong. Re-enter the hypothesis graph.

The oscillatory case is the most valuable. It means you found a real lever but applied it too broadly. The split produces a simpler, more targeted fix.

*Example: removing GROUP on the reduction axis improved contiguous weights by 74% but regressed transposed weights (nn.Linear) by 25%. Oscillatory. The split revealed that the improvement came from wider UPCAST, not GROUP removal.*

### [Bug hunt](/bug-hunt)

Two reviewers from different model families, iterated to convergence. The first catches structural issues, the second logic bugs. Zero new findings = converged.

If the hunt kills the fix, the kill condition is a new observation. Classify it and re-enter the [hypothesis graph](/the-hypothesis-graph). This is mechanized adversarial abduction: the reviewer generates hypotheses, not just verdicts.

*Example: Gemini flagged that nn.Linear transposes its weights. The kill condition re-entered the graph as an oscillatory observation, split the hypothesis, and the surviving fix was one number instead of two.*

### Ship

The only station requiring human approval. Everything before it is local and reversible. A PR triggers CI on someone else's hardware and occupies reviewer attention.

Before creating: check for existing PRs. [Git blame](/prework) the changed line. Deliberate design choice? Address the author's reasoning. Inherited default nobody tuned? Say so.

*Example: the [value was copied](https://github.com/tinygrad/tinygrad/commit/8c6299bced) from `kernel.py` in a file move a year ago. The TODO said "adjust/tune." Nobody did. [One number, one line, one file.](https://github.com/tinygrad/tinygrad/pull/16072)*

### Cost

I spent an hour on [prework](/prework); the regression it caught would have cost trust. The experiment repo gives you both sides of an oscillatory result; the compatibility suite proves the fix is safe; the benchmark table makes the PR description three lines instead of three paragraphs.

### Scale

One agent, one repo, one fix. Ten agents, ten repos, ten fixes. No shared state between runs. The [monoidal contract](/functor-wizardry) makes them independent.

But the real end state isn't humans pointing agents at problems. It's agents noticing the problems themselves. A benchmark drifts. A latency percentile creeps. The system spins up an investigation, classifies the trajectory, builds the experiment repo, benchmarks the fix, runs adversarial review. The [three modes](/modes-of-reason) in a closed loop: observation produces theory, theory produces experiment, experiment produces observation.

### Vision

The human's role narrows to one artifact: **VISION.md**. Not tool configuration. Project philosophy. "The compiler replaces the kernel library." "No vendor primitives." "BEAM should find it." A pipeline that reads VISION.md knows to reject its own custom kernel before the maintainer has to. It knows to adjust the heuristic's defaults instead.

If the hypothesis graph converges, the benchmark is divergent, the bug hunt finds nothing, the compatibility suite passes, and the fix aligns with VISION.md: what's the human adding at the gate?

The [scientific method](/modes-of-reason), which was always personal and sequential, becomes continuous and autonomous. The third mode isn't manual anymore.

---

*The tinygrad case: [experiment repo](https://github.com/kimjune01/tinygrad-matvec-experiment), [PR #16072](https://github.com/tinygrad/tinygrad/pull/16072). The [full hypothesis graph](https://github.com/kimjune01/tinygrad-matvec-experiment/blob/master/HYPOTHESIS_GRAPH.md) has the evidence trail. The [/investigate skill](https://github.com/kimjune01/june.kim/tree/master/skills/investigate) runs in [Claude Code](https://claude.com/claude-code).*
