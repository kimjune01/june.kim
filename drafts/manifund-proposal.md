# Manifund proposal — draft

Public, regrantor-driven, fast. Punchier than LTFF; written to be read by non-specialists scrolling
a feed. Same core as the one-pager, compressed.

## Title

Make AI agents' reasoning checkable by someone who doesn't trust them

## Summary (the one-liner shown in lists)

A training-free harness that records an agent's reasoning as testable, replayable claims, so anyone can
re-run the check instead of trusting the model's word. Demonstrated on a contamination-free bug to catch
what the model's own report passed; now scaling to an open standard and a discovery benchmark.

## What's the problem?

Agents are getting consequential autonomy faster than we can check their reasoning. A patch passes the
visible tests and is wrong everywhere else; a model says the suite is green when it's red. The only check
on an agent today is usually the agent's own report, and a model that grades itself can be wrong,
overconfident, or sandbagging, with no external way to tell. The reasoning that would expose it vanishes
with the context window.

## What's the solution?

Move the check outside the model. The hypothesis graph records each step of an agent's reasoning as a
claim bound to an executable trial, so any conclusion can be rebuilt by a stranger who reruns the recorded
test. The verdict comes from the check, never the model, so a self-grading failure can't pass itself. It's a
harness-layer change: no retraining, usable by any coding agent today.

## What's the evidence it works?

- See the mechanism in a worked example (`abductor`, github.com/kimjune01/abductor): a self-grading agent
  plateaus on a fix that passes every visible test, then the external check drags it to the true rule it
  couldn't recall. Contamination-free by construction, deterministic, no case selection.
- On a contamination-free, post-cutoff bug, externalizing the check carried a weaker model to a fix the
  strongest released model could not reach alone: a two-tier capability lift, and the safety-aligned kind,
  since it comes from external verification with no training. The same replayable check that lifts the
  model is what lets a distrusting third party catch an error the agent's own report would have passed.
  Preregistered, regradeable, DOI-archived.
- The same program scored 95.3% on SWE-bench Pro under the official grader, but I'll be precise about it:
  the tests were available as the solving oracle, so that number measures spec-to-code translation (largely
  solved), not discovery. The methodology is fully committed and auditable. The honest read of that number
  is exactly why the discovery benchmark below needs to exist.
- Open-source tooling (`abductor`, the `inquire` skill) and Zenodo DOIs, each reproducible from committed inputs.

## What will the money do?

Tranched, so one regrantor can make the first move and the rest can co-fund:

- **$10k:** the confirmatory contrast on new contamination-free bugs, plus the discovery-benchmark MVP.
  Concretely it covers token costs for the runs and two months of personal expenses to do the work. The
  cheapest experiment that tells us whether the Verus result generalizes.
- **$30k:** the above, plus harden the harness so a second team can run it without me.
- **$75k:** 9–12 months full-time, all of the above, the full discovery benchmark current benchmarks
  can't measure, and a cross-agent replay prototype.

Every tranche ends in a public, reproducible artifact. The first dollar buys the n=1→n=5 de-risking, not
a runway top-up.

## Who am I?

June Kim, independent researcher on AI agent verification, based in Canada. I work fully in the open: three Zenodo DOIs,
each reproducible from committed inputs; a determinacy audit of all 728 SWE-bench Pro tasks; and a clean
iteration result, one-shot 43% → iterative 91% PR-approval across 27 merged PRs in 9 real repos
(Go/TS/Rust). Everything is at june.kim and github.com/kimjune01. I design for a distrusting auditor by
default, the property this project makes standard.

## Risks / what could fail

The oversight effect is shown on one bug, selected for eligibility (contamination-free, post-cutoff) and
fixed before the run, so the open question is whether it generalizes. It may
not, and I'll report that if it doesn't. The cross-agent replay layer is the unproven edge. Honest failure
of these is a real outcome of the grant. Reporting it is part of the work.
