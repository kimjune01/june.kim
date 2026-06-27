# Funding strategy — verifiable agent reasoning

Independent research funding for the Hypothesis Graph / Verifiable Knowledge program.
Constraints: runway in months (fast vehicles), independent/remote preferred.

Based in Canada. Doesn't affect eligibility (LTFF, Manifund, CAF, Open Phil all fund globally). Tax: grants are foreign-source income, taxable in Canada; for US payers (Manifund) file a W-8BEN to claim the Canada–US treaty and avoid US withholding. Asks below are USD ($75k USD ≈ $103k CAD).

## The asset, in funder terms

A deployable, training-free accountability mechanism for AI agents, arriving as a DeepMind-led paper
argues that artificial epistemic agents must demonstrate robust falsifiability and external trust
architecture (Marchal et al. 2026, arXiv:2603.02960), the property this mechanism supplies. Three things
a funder pays for:

1. **A mechanism**: reasoning externalized to a replayable structure at the harness layer,
   checkable by a party that does not trust the author. Defeats model self-grading.
2. **Evidence**: Verus #2219, contamination-free and post-cutoff. Externalizing the check carried a
   weaker model to a fix the strongest released model could not reach: a two-tier capability lift, and
   the safety-aligned kind, since it comes from external verification with no training. The same
   replayable check that lifts the model is what lets a distrusting party catch its error. Archived,
   regradeable (Zenodo DOIs).
3. **Working artifacts**: abductor + inquire skill, open source, with worked examples and DOIs. Not a plan; a thing that runs.

## The credibility anchor (the broader body of work)

The epistemics is the bet; the benchmark discipline is what earns the right to make it. Two
months of public, reproducible output behind the program:

- **SWE-bench Pro: 95.3% (694/728)**, public split, official grader — *with the tests available as the
  solving oracle (not hidden)*. So this is a translation ceiling, not a discovery result: it shows
  spec-to-code translation is largely solved, while leaving the harness's discovery ability untested. Cite it that
  way or not at all. The value is the committed, auditable methodology (source-only capture,
  fresh-container grading, ~$870 all-in). DOI 10.5281/zenodo.20691978.
- **SWE-bench Verified: 426/500 (97.3% of eligible)**, per-task grader reports committed.
- **The iteration experiment**: one-shot 43% → iterative 91% PR-approval across 27 merged PRs in
  9 real repos (Go/TS/Rust). Same code, same spec; only the review loop differs. A clean result on
  where the real bottleneck sits.
- **A determinacy audit** of all 728 Pro tasks showing today's benchmarks measure translation,
  not discovery. This is the gap deliverable 2 fills.
- **Range**: cognitive architecture (Soar async), compiler autotuning (tinygrad, 52 trials vs
  BEAM's 193, 1.85x), plus published null results. Signals rigor; nothing here is cherry-picked.

The pitch line: *this is the person who ran a coding benchmark with auditable discipline, showed that its
95% measures translation rather than discovery, and then built the mechanism for the discovery problem
that number hides.* The honesty about the number is itself the credibility.

## Targets, in order of when to fire

| Funder | Why | Speed | Ask size | Status |
|---|---|---|---|---|
| **LTFF (EA Funds)** | funds independent AI-safety researchers; light app; rolling | weeks | $60–90k / 9–12mo | fire first |
| **Manifund** | public, regrantor-driven, fast; doubles as visibility | weeks | $20–60k bridge | parallel, same text |
| **Cooperative AI Foundation** | narrow fit: the new $10M agent-infrastructure fund (reputation/commitment protocols), not the core cooperation agenda; verification ≠ cooperation until an incentive argument is added | slower | larger | queue 2nd, reframe |
| **Open Philanthropy** | funds scalable oversight / agent verification directly | slow | larger | after LTFF lands (social proof) |
| **SFF / Foresight / ARIA** | safety-adjacent, varied cycles | varied | varied | optional backup |
| **CIFAR / Mila / Vector / Amii** | Canadian; affiliate/visiting routes give institutional cover + compute | slow | institutional | queue later |

## Theory of impact (the LTFF crux)

As agents take on consequential autonomy, the bottleneck becomes *trust without verification*:
output-level checks pass while the reasoning is wrong (over-narrow patches, confabulation,
sandbagged self-reports). This is a scalable-oversight problem. The hypothesis graph makes agent
reasoning externally checkable at the harness layer, at no training cost, shifting the burden of
proof outside the agent. Verifiable Knowledge extends it to populations of agents that don't trust
each other. Verifiable reasoning is a prerequisite for safely delegating to agents; independent
replay is the defense against the self-grading / defeat-device failure mode safety work worries about.

## Job track (parallel, slower clock)

Apply with the papers as portfolio, in place of a generic résumé.
- **Anthropic** (alignment / agents / evals) — built on Claude Code, about agent reliability + oversight. Most on-the-nose.
- **METR / Apollo / Redwood** — trajectory-level oversight is their language.
- **Cognition / Cursor** — harness-layer capability-lift result is a hiring signal (less safety-framed).

A live LTFF grant strengthens every one of these conversations. US roles: as a Canadian, the TN visa (USMCA) is the fast path in: no lottery, no cap.
