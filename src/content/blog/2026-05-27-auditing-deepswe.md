---
variant: post-wide
title: "Auditing DeepSWE"
tags: coding, methodology, epistemology, reflecting
---

A benchmark asks us to trust three things: the tasks are real, the grader is fair,
and the answer key works. This is an audit of the third.

[DeepSWE](https://github.com/datacurve-ai/deep-swe) arrived last week as a
contamination-free coding benchmark: 113 tasks drawn from active repositories,
graded by per-task verifiers. Good work, and making the rounds. The most basic
check there is: take the answer key, and ask whether it passes its own test.

## The check

Every DeepSWE task ships a reference solution and a verifier. The verifier applies
a hidden test patch and runs the suite; a passing solution scores 1. So the check
is simple: apply the *reference* solution, run the verifier, confirm it scores 1.
If a task's own gold answer cannot pass the test built for it, the task is not
gradeable. No model is involved, so it costs nothing in tokens. One spot machine,
ten tasks at a time, the whole set in under an hour, all in for less than a dollar.

This is the check you would run before shipping. It is also the check nobody
downstream can run, unless the authors publish the harness and the data to
reproduce it.

## First, I audited myself

The first run failed every single task. All 113 came back with no score.

The tempting headline writes itself: *contamination-free benchmark ships 113
broken tasks*. It would also have been wrong. A uniform failure across every task
is never 113 independent defects; it is one fault in the thing they share, my
harness. The grading framework brings up its sandbox with `docker compose`, and
the bare [Amazon Linux](https://aws.amazon.com/linux/) image I provisioned ships Docker without the Compose plugin.
So every task errored before it reached the verifier.

I installed the plugin, added an assertion so the gap fails loudly next time, and
re-ran. I suspected my own setup before I suspected theirs. That is the only
reason the rest of this is worth reporting.

## What the corrected run found

With the harness correct, the goldens started passing, one after another, exactly
as they should. Then a few did not.

The reference solutions for four of the 113 tasks fail their own verifiers:
`langchain-request-coalescing`, `narwhals-rolling-window-suite`,
`prometheus-transactional-reload-status`, and `skrub-duration-encoding`. No agent
attempted them. The answer key itself, applied verbatim, does not pass the test
the benchmark grades against. Each is confirmed by re-running it alone, which rules
out contention; a task is flagged only when its gold fails in isolation.

I want to be precise about what this does and does not establish. Three things
hold, and no more: under the benchmark's published harness at the pinned commit,
the reference solution failed its verifier; the failure reproduced in isolated
reruns; and the cause is unresolved. It could be a genuinely broken task, a flaky
test, or environment drift since the image was built. Sorting those apart is the
maintainer's job, not the auditor's. A reproducible failure under the published
harness is a complete report; the diagnosis belongs to whoever shipped the task.
The bounded claim stands on its own: a task in this state cannot be treated as a
trustworthy graded instance until that diagnosis happens.

## Where these failures live

A score implies a clean function: model and task in, pass or fail out. Between them
sits an authored apparatus, namely task selection, the instruction, the held-out
test, the reference solution, the acceptance criteria, and the environment. A gold
that fails its own verifier is two of those pieces in contradiction. An answer key
asserted correct but never run against its own test is, in the precise sense, a
confabulation: a plausible artifact nobody checked. Which piece confabulated, and
whether by authoring or by drift, is the maintainer's to determine.

## The audit at a glance

| Claim | Observation | Analysis | Recommendation |
|---|---|---|---|
| **Tasks are original, the benchmark is contamination-free** | Spot-check holds: the requested `matchEach` matcher is absent from [`ts-pattern`](https://github.com/gvergnaud/ts-pattern) upstream code, PRs, and issues; reference solutions are held out | Verifiable per task, and a genuinely cleaner substrate than the contaminated [SWE-bench Verified](https://www.swebench.com/verified.html). The claim survives inspection | Keep it, and publish the per-task originality check so the claim is earned by inspection, not asserted |
| **All 113 tasks are gradeable by their own verifiers** | Four reference solutions fail their own verifier (`langchain-request-coalescing`, `narwhals-rolling-window-suite`, `prometheus-transactional-reload-status`, `skrub-duration-encoding`), each confirmed failing in isolation | A gold that fails its own test makes that task untrustworthy to grade against until resolved. Cause (broken task, flaky test, or environment drift) is undetermined; the public record shows no gold-passes-verifier check behind the published tasks | Run gold-passes-verifier before shipping; fix or exclude the failures; publish the check so others need not rediscover it |
| **A lighter, standardized harness does not disadvantage any model** (popularly inflated to "less prompting is better") | 3 model families, [`mini-swe-agent`](https://github.com/SWE-agent/mini-swe-agent) vs each native CLI, on a single 10-task slice, one run per cell, no intervals or tests; stated finding is "matches or beats every native harness at comparable token cost" | Ten tasks at single-run with no variance estimate cannot carry a directional scaffolding claim; "matches or beats" without error bars is consistent with noise. Their own wording is careful; the "less is more" reading is not in the data | Run a paired ablation at scale (all 113), repeated for variance, with confidence intervals, a significance test, and published trajectories |

## The second read that didn't run

Read the rest as a second reader's note, the review that should have happened before
this shipped. On the evidence, it did not. This is a note about method, not findings:
I have not rerun a single leaderboard number and I dispute none of them. The question
is only whether the process behind them earns the confidence of the claim. The work
is close, and the gaps are cheap to close.

Two checks, both nearly free, catch what this audit caught. First, run every task's
gold through its own verifier and fix or exclude the ones that fail. That is the
audit above, and it cost about a dollar. Second, have a model read each task cold,
the instruction beside the reference solution and the test, and flag where they
disagree. Codex or Gemini does that in a single pass for pocket change. Given four
golds that contradict their own tests, I doubt the second pass happened.

And the timing is unforgiving. Once a benchmark is public and scored against, it is
frozen like any other measurement instrument: patch a task now and you change the
instrument, breaking comparability with every number already posted. So these four
cannot simply be fixed in place. The honest repair is a full versioned iteration,
the whole set re-released and re-graded. A dollar of pre-ship checking would have
spared that, which is the real cost of skipping it.

There is a cheaper route, and it is open even now: claim less. A benchmark that
labels its limits, that the tasks are not all gold-verified and that the harness
comparison is a ten-task pilot, asks only for the trust it has earned. A caveat
costs nothing and breaks no comparability.

So the note is short. Before shipping, run the answer key against its own test and
let a second reader catch the contradictions. After shipping, if those checks were
skipped, say so in the limitations. Either way, publish the runs so the next reader
does not have to find the cracks. You should do better, and the cheapest version of
better is plain: it is fine to ship unfinished work, but not to call it finished
when it is not.

## Attestation and reproducibility

The point of this post is not to be trusted. It is to be checked. So here is everything needed to
re-derive every number above. That is the reproducibility the benchmark did not publish.

**What ran.** The `oracle` agent applies each task's own reference solution, then the task's own
verifier grades it through [Pier](https://github.com/datacurve-ai/pier) `0.2.0`, unmodified. No model
is involved, so model cost is zero. Subject: `datacurve-ai/deep-swe` pinned at commit
**`2f0f4125`** (tasks can change after publication; this is the exact version audited), all 113 tasks.
Compute: one spot `m7i.8xlarge` in `us-west-2`, ten tasks in parallel, under one dollar, 2026-05-27.

**Protocol.** Preregistered: the procedure was fixed and committed before the run. Pass 1 grades all
113 in parallel; pass 2 re-runs every non-passing task **sequentially and alone**, so a resource
hiccup can never be reported as a defect. A task is flagged only when its gold fails in isolation. The
first run failed all 113 because of a missing `docker compose` plugin on my own box, disclosed above;
that fault was fixed before the run that produced these numbers.

**Reproduce it.**

```bash
git clone https://github.com/datacurve-ai/deep-swe && cd deep-swe && git checkout 2f0f4125
uv tool install datacurve-pier            # 0.2.0; needs docker + the docker compose v2 plugin
for t in tasks/*/; do pier run -p "$t" --agent oracle --env docker; done
# reward.txt == 1 means the gold passes its own verifier; != 1 flags a defect
```

**Pointers.** Preregistration, the audit harness (`provision_oracle_ec2.sh`, `box_audit.sh`), the full
per-task verdict ledger (`oracle_audit_ec2.jsonl` plus the sequential re-confirmation), and the
confirmed defect list are all at
[github.com/kimjune01/deepswe-run](https://github.com/kimjune01/deepswe-run), frozen at tag
`audit-v1`. Take the commit pin, re-run the loop, and check me.
