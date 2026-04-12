---
variant: post-medium
title: "Visibility Is Not Decision"
tags: methodology, cognition
---

*Follows the [revised SOAP notes](/soap-notes-soar-revised). Part of the [cognition](/cognition) series.*

I retired three PRs to the [Soar cognitive architecture](https://github.com/SoarGroup/Soar) because they were based on wrong assumptions. The maintainer and I agreed on one thing: the project needed evals. So I built one. What I learned building it had less to do with Soar and more to do with a design error I keep seeing in eval systems.

## The obvious thing to build

The first harness I wrote measured chunking transfer. Generate random [Blocks World](https://en.wikipedia.org/wiki/Blocks_world) tasks, train an agent, test whether learned chunks speed up new tasks. Three conditions: trained-transfer, fresh baseline, no-learning control. Transfer ratios came back positive across every seed: chunking cuts decision cycles by 28–64%.

That confirmed something the Soar group has known for forty years. The measurement loop was new. The finding was not.

The real question was whether the harness could discriminate between two builds. I had a held PR (#577) that changes when chunking fires in RL-driven substates. I ran it. Same numbers on both builds. The test agents didn't exercise the feature under test. The harness had no discriminating power for the one PR that mattered.

## The less obvious thing to build

So I changed direction. Instead of one transfer experiment, I wrapped Soar's existing test suites — 19 chunking agents, 41 semantic memory agents, 53 episodic memory agents — and captured quantitative stats per test: decision cycles, production firings, WM peak, chunks learned. Then I diffed two builds.

The first comparison found the signal:

```
Agent                                          Metric              Base  Candidate   Delta      %
BW_Hierarchical_Look_Ahead                     decisions             66         46     -20  -30.3%
BW_Hierarchical_Look_Ahead                     production_firings   651        340    -311  -47.8%
BW_Hierarchical_Look_Ahead                     wm_max               679        235    -444  -65.4%
BW_Hierarchical_Look_Ahead                     productions_chunks     3          1      -2  -66.7%
```

PR #577 made Blocks World Hierarchical Look-Ahead 30% faster in decisions, 48% fewer rule firings, 65% smaller working memory peak. Zero regressions on any other agent. The harness found the discriminating signal that the transfer experiment missed, because it ran all existing agents instead of one hand-picked one.

But the first version of the comparison layer had a problem.

## The design error

I built the comparison layer to classify each metric change as "improved," "regressed," or "changed." Lower decisions = improved. Higher WM = regressed. Different chunk count = changed (direction unknown). Then a Pareto check: pass if at least one improvement and zero regressions.

The Pareto check failed. Two "regressions" were CPU timing noise: 0.010 → 0.011 seconds and 0.004 → 0.005 seconds. Sub-millisecond jitter on tests that run in single-digit milliseconds. The harness couldn't tell noise from signal because the classification was baked into the measurement.

This is the design error: **the harness was deciding and reporting in the same layer.**

When you mix visibility with decision, two things go wrong. First, noise becomes judgment. A 0.001-second timing fluctuation gets the word "regression" attached to it, and now someone has to argue about whether it's real. Second, contributors learn to optimize the classifier rather than the system. If "fewer decisions" is hardcoded as "improved," you'll get PRs that reduce decision count by doing less work. The metric becomes the target, and Goodhart takes over.

## Separating the concerns

The fix is two layers with a clean interface between them.

**Layer 1: Visibility.** The harness captures facts. Per test, per metric: base value, candidate value, delta, percent change. No classification. No words like "better" or "worse." The output is a table of numbers.

```
python module_eval.py compare --base upstream.json --candidate pr577.json --facts-only
```

This layer is the contributor's tool. You run it, you see what changed, you decide whether your changes did what you intended. The numbers are the numbers. No policy, no threshold, no pass/fail.

**Layer 2: Decision.** A separate, configurable policy that the maintainer controls. Which metrics are "lower is better"? What's the noise floor for CPU timing? Is chunk count directional or neutral? Should a missing test agent count as a regression?

```json
{
  "lower_is_better": ["decisions", "elaboration_cycles", "production_firings", "wm_max"],
  "neutral": ["productions_chunks", "wm_mean"],
  "timing_floor": 0.005
}
```

The policy is a JSON file the maintainer commits to the repo. Contributors can see it, but they don't set it. The Pareto check runs against the policy, not against hardcoded rules. If the maintainer decides chunk count is directional for a specific release, they change the policy. If they decide CPU timing under 5ms is noise, they set a floor. The harness never changes — only the policy does.

This separation does two things.

First, it makes Goodharting harder. The contributor sees the raw numbers (Layer 1) and knows what changed. But they don't control which numbers the maintainer cares about (Layer 2). Optimizing for the classifier doesn't work when the classifier is someone else's configuration file.

Second, it makes scope flexible. A PR that adds a new capability can bring a new test agent. Layer 1 reports the new agent's numbers alongside the existing ones. Layer 2 doesn't penalize the PR for being "unchanged" on existing tests — the maintainer decides whether "positive on new test, unchanged on existing" is sufficient. The policy adapts to the contribution, not the other way around.

## The pattern

This isn't specific to Soar or to cognitive architectures. It's a general pattern for any eval system:

**Instruments measure. Policies decide. Mixing them creates Goodhart targets.**

A CI pipeline that says "coverage must be ≥ 80%" is mixing measurement with decision. The measurement is "coverage is 78.3%." The decision is "78.3% is not enough." When you fuse them, contributors write tests that hit lines rather than test behavior, because the instrument *is* the judge.

A benchmark that says "our model scores 92.1 on X" is an instrument. A benchmark that says "92.1 is state-of-the-art" is mixing instrument with decision. The score is a fact. Whether it matters depends on what X measures, whether X is the right test, and what you're trying to do. The paper that reports the score should not be the same paper that decides it's good enough.

An eval harness that says "decisions went from 66 to 46" is an instrument. An eval harness that says "30% improvement, Pareto pass" is making a decision. The 30% is a fact. Whether it constitutes a pass depends on whether decisions are the right metric, whether 30% is meaningful, and whether the test agent represents the workload you care about. The person who runs the harness should not be the same person who sets the threshold.

In LLM agent development, this separation is what makes eval suites like [SWE-bench](https://www.swebench.com/) useful. The benchmark provides a fixed set of tasks and a binary pass/fail per task — that's the instrument. What score counts as "good enough" for a particular model or application — that's the decision, and it lives outside the benchmark.

## What this means for Soar

The harness I built runs Soar's existing test agents, captures per-test metrics, and diffs two builds. Layer 1 shows the raw numbers. Layer 2 applies whatever policy the maintainer configures. The maintainer can change the policy without changing the harness, and contributors can see exactly what changed without being told whether it's good or bad.

The next step is to run it on more suites — semantic memory, episodic memory, performance tests — and to require that PRs bring their own test agents. A PR without a test agent is an untestable claim. The harness is the infrastructure that makes claims testable. The policy is the maintainer's judgment about which claims matter.

My three retired PRs would have shown "unchanged" on all existing tests, because they were solving a problem that didn't exist. The harness wouldn't have told me they were wrong — but it would have told me they did nothing measurable. That's the floor. The ceiling is when a PR shows a clear signal on a relevant agent, like #577 on BW-Hierarchical-Look-Ahead: 30% fewer decisions, 48% fewer firings, no regressions. The numbers are the argument. The maintainer makes the call.

---

*Built during a re-diagnosis of the [Soar cognitive architecture](https://github.com/SoarGroup/Soar). The harness is at `soar-eval/` in the repo. See [Revised SOAP Notes](/soap-notes-soar-revised) for the correction that prompted it. Written via the [double loop](/double-loop).*
