---
variant: post-paper
title: "Local Replay Auditability: Verification That Returns a Check"
tags: coding, epistemology, methodology
---

## Abstract

Verification systems usually return a score, label, or Boolean. That output can steer an agent, but a later auditor cannot distinguish a confident-but-wrong output from a truthful one without rerunning the system from the start. This paper introduces **local replay auditability**: instead of returning a static truth value, return a check whose execution returns the truth value. Every consequential, machine-checkable claim an agent makes is stored with its check. Nodes bind claims to checks, and edges record how a failed check motivates the next claim. We instantiate the mechanism for coding agents and demonstrate it on a post-cutoff compiler bug. Verification becomes a persistent research artifact rather than a transient reward signal.

## A Boolean verdict does not compose

What is verification? It is often modeled as a Boolean property of a produced result. The verdict serves as checkpoint and feedback for the producing agent. But agents and context windows are ephemeral. After the session ends, verification flattens to a record. A downstream agent cannot identify which property was checked or rerun the check after a dependency changes.

Coding agents make this failure concrete. A patch that passes a visible suite may still encode the wrong boundary. The verdict says tests passed, but not which tests. Authority arrives without an inspectable boundary.

Reviewers face the inverse problem. A trajectory records tool calls and prose, but rarely says which claim each command tested or which outcome would have killed that claim. Verifying the final patch can require reconstructing the entire inquiry. When checking costs as much as producing, review becomes rubber-stamping.

Local replay auditability changes the verifier's return type. Instead of returning only a Boolean, it returns a check that produces the Boolean when run against the artifact. The record binds a claim to that check, the observed outcome, and the check's provenance. A later consumer can rerun one conclusion without trusting the agent, trusting a stored label, or reconstructing the trajectory.

The experiment below witnesses the mechanism on a post-cutoff Verus compiler bug. Eighteen self-attested Codex runs plateau at a narrow fix. Three Fable 5 self-attested controls land wide but incorrect. With an external comparator, Fable 5 and Sonnet 4.6 both match the merged human fix's behavior on all eight committed probes.

## The verifier returns an executable constraint

Conventional verification consumes an artifact and returns a scalar:

```python
def verify(artifact: Artifact) -> bool: ...
```

Local replay auditability returns the executable check:

```python
Check = Callable[[Artifact], bool]

def verify(artifact: Artifact) -> Check: ...
```

The check may include a concrete input, expected behavior, pinned dependencies, and the command that compares the artifact against that expectation. The current agent can use its Boolean result immediately. A later agent can apply the same check to a revised artifact.

A visible test suite returns tests, but the producer authors them and may grade its own interpretation. A hidden test adjudicates independently, but only its Boolean escapes. The test that did the adjudicating never enters the record. Local replay auditability requires both independence and persistence.

The verifier need not cover the entire artifact. It must produce one relevant check whose source is independent of the candidate. That check may come from an external comparator, a separately maintained invariant, or a human-approved artifact. Each source terminates in a fact of reality or a named human; a model's say-so is neither.

| | Returns a Boolean | Returns a check |
|---|---|---|
| After the run | verdict dissolves into the trajectory | check persists with its claim |
| Upstream change | staleness is undetectable | rerun separates live from stale |
| Audit | reconstruct the trajectory | rerun one check |
| Failure | a penalty to descend | a counterexample naming the next hypothesis |

The check gives verification memory. It outlives the attempt that ran it.

## The graph organizes returned checks

The harness organizes checks using the [Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics). Each node binds a live hypothesis to its kill condition, exact check, observed outcome, and open, witnessed, or killed verdict. A refutation edge records how a failed check motivates the next candidate. The graph supplies organization; the check supplies verification.

Without the graph, verifying a conclusion means interrogating the agent or reconstructing its trajectory. With it, each step binds a claim to a trial a reviewer can rerun without the agent's cooperation.

Replay comes in two grades. Deterministic commands over pinned inputs support strong replay. Model or live-service calls support artifact-level replay, where an auditor verifies the recorded output and reruns a deterministic predicate over it.

## Returned checks change the boundary

We tested whether an external comparator changes the solution an agent reaches on Verus issue #2219. The issue opened in March 2026 after the solving models' reported knowledge cutoffs. The maintainer's first patch, #2230, handled only the surface case. PR #2501 later merged a general fix. The experiment treated #2501's behavior on committed probes as the reference boundary.

### The bug

Verus is a deductive verifier for Rust. Issue #2219 is an unsoundness: a ghost expression of type `!` is erased before compilation and does not actually diverge, yet it triggers rustc's never-type edge prune. Verus drops a live control-flow edge, skips reachable code behind it, and verifies a program it owes a rejection.

Two programs look identical at the `!` token but require opposite verdicts. A ghost call's never-typed value disappears before runtime, so code behind it executes. A genuine runtime terminator ends the path, so proof code behind it never runs. The narrow fix keys on the surface token. The general fix handles the whole class of uninhabited types.

![The #2219 unsoundness as a causal chain. A ghost-erased uninhabited return and genuine runtime divergence are identical at the token and opposite in required handling.](/assets/verus-2219-unsoundness.svg)

The bug resists shallow search. The fault sits four steps up the causal chain from the wrongly accepted program, and the project's suite passes both narrow and general fixes. The suite cannot see the distinction the fix must make.

### Ablation

Before each loop, the protocol preregistered one sentence: testing X, predict Y, refuted by Z. Six self-attested prompt methods ran three times each in the Codex workflow. Three additional Fable 5 controls used strong, weak, and prompt-matched self-attestation.

The external condition used a comparator that enumerated cases and added divergence goldens derived from the merged human fix. The model received only per-case pass or fail. It never received the reference build, its diff, or the governing predicate.

| Method | Enumeration | Kill conditions | External check source |
|---|:---:|:---:|:---:|
| minimal or neutral prompt | no | no | no |
| site-enumeration prompt | yes | no | no |
| abduction prompt | no | yes | no |
| hypothesis-graph prompt | no | yes | no |
| self-verifier harness | yes | yes | no |
| external-gate harness | yes | yes | yes |

The graph did not produce a capability lift by itself. Persistence serves a different claim: the trace stays reviewable after the run. Check source was the intervention of interest, although model, harness, and budget differences prevent a clean causal estimate.

![The ablation as a causal diagram. Model, loop, bug, and graph stay fixed across arms; only the verdict source varies.](/assets/verus-2219-lift-mechanism.svg)

### Observed boundaries

All 18 Codex runs plateaued short of the general boundary. The three Fable controls reached a wider boundary but over-rejected valid divergence. With a corrected gate covering the divergence side, Fable 5 and Sonnet 4.6 matched the merged human fix on all eight committed probes. A protocol-matched Codex rerun still failed the divergence-preserve case.

| Model and check source | Observed boundary |
|---|---|
| Codex, 18 self-attested runs | narrow, no general fix |
| Fable 5, self-attested | wide but incorrect |
| Sonnet 4.6, self-attested | narrow, matched #2230 |
| Sonnet 4.6, external comparator | behavior of #2501 on committed probes |
| Fable 5, external comparator | behavior of #2501 on committed probes |
| Codex, external comparator | failed the divergence-preserve probe |

The [`hygraph-mechanism`](https://github.com/kimjune01/hygraph-mechanism) archive contains the preregistration, rebuild-confirmed dataset, regrade script, captured diffs, and graph and gate traces. The standalone gate is archived as [`abductor`](https://github.com/kimjune01/abductor).

This single task supplies a mechanism witness: externally constrained workflows crossed a boundary the self-attested workflows did not.

## The check carries more than its verdict

Without the comparator, the agent proposes a patch, writes compatible tests, and confirms its own interpretation. With it, an independently maintained constraint acts first. A failed check kills the current hypothesis, and the manner of failure names the next one.

A self-verifying Fable run built a 6,684-case generator and widened it to 7,026 variants. It still mislabeled the decisive boundary because it graded against its own predicate. Without the comparator, Fable and Sonnet miss in opposite directions. With it, both land on the same reference behavior. More search does not correct opposite errors onto one target; an external answer key does.

The gate's coverage remains both lever and limit. Its uninhabited cases pushed models beyond the narrow patch. Its first version lacked a divergence-preserve shape, so the resulting fix stayed wide but incorrect. Adding that golden let two models reach the shipped boundary, while Codex still failed to implement the distinction.

Returning the trial frees a later agent from trusting the earlier model or execution. It can rerun the check, inspect the failure, and continue from the killed node. The next inquiry begins where the last one verifiably stood.

## Five questions remain

1. Does local replay reduce reviewer time relative to trajectories and prose summaries?
2. How often do external checks change a patch rather than confirm it?
3. Which sources remain independent enough to escape correlated model errors?
4. Does preserving killed hypotheses reduce repeated mistakes across runs?
5. Where no replayable artifact exists, can a timestamped human attestation stand in for the check?

Benchmarks should measure off-suite behavior and audit time, replay success, and the distance between self-attested and externally verified solutions.

## Replay can still test the wrong property

Agents may overfit, detect the evaluation environment, forge logs, or exploit a weak comparator. Pinned artifacts and independent execution improve the evidence. They do not guarantee that the check measures the property the claim is about.

Replay also costs something. Recording every trivial claim would bury reviewers in low-value checks. A practical harness should allocate verification by stakes and preserve only claims that affect the solution boundary.

Finally, the evidence is existence-grade: one audited divergence on one instance. The architecture earns confidence only through fully preregistered, multi-task comparisons with strong baselines.

## From verification signals to verification artifacts

Hidden tests already separate patch generation from evaluation, but the check normally disappears after grading. Trajectory replay re-executes a whole recorded run. Local replay instead reruns one claim's trial.

The distinction matters whenever an institution publishes a verdict without its derivation. OpenAI later estimated that roughly 30% of SWE-bench Pro tasks were broken and retracted its recommendation, but the underlying pipeline and labels were not released. A reader could not reproduce the conclusion. The verdict shipped without its check. A companion [public audit](/a-determinacy-audit-of-swebench-pro) proves a smaller floor with per-task receipts a stranger can rerun.

The companion Hypothesis Graph work owns the representation and multi-agent coordination claim. This paper does not claim that graph structure caused the lift. Here the graph organizes externally sourced checks; the contribution is the verifier interface that returns the check instead of discarding it.

## Conclusion

Reliable coding agents need checks they cannot freely write for themselves. Local replay auditability makes those checks the verifier's return value and binds each one to the claim it adjudicates. The Boolean steers the current run. The returned check lets anyone reproduce the verdict.

A later agent inherits a constraint it can rerun rather than a claim it must trust. The case study witnesses the mechanism: a human-derived divergence check moved models beyond the solution reached by self-attested arms while withholding the implementation answer. A transient judgment becomes an executable, composable research artifact. It enlightens whoever runs it.

## Availability

- [`hygraph-mechanism` experiment and regrade archive](https://github.com/kimjune01/hygraph-mechanism) · [Zenodo](https://doi.org/10.5281/zenodo.20754118)
- [`abductor` external gate](https://github.com/kimjune01/abductor) · [Zenodo](https://doi.org/10.5281/zenodo.20738162)
- [Hypothesis Graph companion paper](/the-hypothesis-graph-semantic-memory-methodeutics)
- [Verifiable Knowledge companion paper](/verifiable-knowledge)
