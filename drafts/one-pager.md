# Verifiable agent reasoning — project & person one-pager

Reusable source text. Forms and emails pull from here. Edit the bracketed lines once and reuse.

## The person (bio block)

June Kim, independent researcher on AI agent epistemics, verification, and coding-agent reliability,
based in Canada.
[One line of background you're willing to stand on — e.g. "prior: <role/field>" or "SFU-affiliated".
Leave out if you'd rather the work carry it.] Works in public: papers, code, and reproducible
experiments at june.kim and github.com/kimjune01.

Short version (for email signatures / one-liners):
*June Kim — independent researcher, verifiable AI agent reasoning. june.kim · github.com/kimjune01*

## The problem (one paragraph)

AI agents are handed consequential autonomy faster than we can verify their reasoning. A patch passes
the visible tests and is wrong off-suite; a model reports a suite as green when it is red. Output-level
checks miss this, and the reasoning that would expose it disappears with the context window. The
check on an agent today is usually its own report, which can be wrong, overconfident, or
sandbagging, with no external way to tell.

## The work (one paragraph)

I build the substrate that makes agent reasoning externally checkable, at the harness layer, with no
retraining. The **hypothesis graph** is a semantic memory whose nodes are testable claims and whose
edges are the conditions that refute them; every conclusion is reconstructible by a stranger who reruns
its recorded trial. **Verifiable Knowledge** extends this to populations of agents that do not trust
each other: a claim becomes shared knowledge only as a check another agent can re-run. The verdict comes
from re-running a typed check; the model's word carries no weight, so a model cannot pass by merely asserting
success; the check has to be independently satisfiable.

## The evidence (inspectable, reproducible)

- **Worked mechanism demos** (`abductor`: github.com/kimjune01/abductor, walked through in *The Hypothesis
  Graph*): inquiries (`leap_year`, `natural_sort`) where a
  self-grading agent plateaus on a hypothesis green on every visible test, and the gate's coverage drags it
  to a bespoke rule it can't recall from memory. Contamination-free *by construction*, deterministic: the
  oracle-gap mechanism with no case selection.
- **The mechanism result (Verus #2219)**: a contamination-free, post-cutoff bug where an independent
  replay caught what the model's own report missed. Externalizing the check let a weaker model
  (Sonnet 4.6) reach a fix the strongest released model (Fable 5) could not reach on its own. Established by a
  preregistered factorial (six arms × three variants, ~18 runs), so it rests on more than a single trial. This is a
  two-tier capability lift of the safety-aligned kind: it comes entirely from external verification, no
  training, so the same replayable check that lifts the model is what lets a distrusting party catch the
  error. Preregistered, regradeable. DOI 10.5281/zenodo.20754118.
- **SWE-bench Pro: 95.3% (694/728)** under the official grader, with the tests available as the solving
  oracle (not hidden). DOI 10.5281/zenodo.20691978. Read it precisely: this measures spec-to-code
  *translation*, which is largely solved; it says nothing about my harness's *discovery* ability, which the visible-test
  setting can't test. The methodology is committed and auditable; the honest read of the number is the
  point, and it's what motivates the discovery work below.
- **Iteration experiment**: one-shot 43% → iterative 91% PR-approval, 27 merged PRs, 9 real repos.
- **Open-source tooling**: `abductor` (github.com/kimjune01/abductor) and the `inquire` skill, plus reproducible repos for the bench, audit, and mechanism experiment.

## The ask

[$75,000] for [9–12 months] of full-time independent work, plus modest compute/API [~$5k]. Deliverables:
(1) harden the harness into an adoptable open standard; (2) build the discovery benchmark the field
lacks; (3) scale the mechanism evidence beyond n=1, reporting the null regime honestly; (4) prototype
cross-agent replay. Everything ships public and reproducible, as the existing artifacts already do.

## Why now

A DeepMind-led paper argues that artificial epistemic agents must demonstrate robust falsifiability and
external trust architecture (Marchal et al. 2026), the property this substrate supplies. The window to
set it as an open standard, rather than a closed per-vendor feature, is open now.

## Links

- Papers (preprints): *The Hypothesis Graph* (june.kim/the-hypothesis-graph-semantic-memory-methodeutics),
  *Verifiable Knowledge* (june.kim/verifiable-knowledge),
  *What Cannot Be False Cannot Be True* (june.kim/what-cannot-be-false-cannot-be-true)
- Code & data: github.com/kimjune01 (abductor, swebench-pro, swebench-pro-audit, hygraph-mechanism)
- Archived: Zenodo DOIs above, each reproducible from committed inputs
