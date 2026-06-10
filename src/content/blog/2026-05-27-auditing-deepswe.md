---
variant: post-medium
title: "Auditing DeepSWE"
tags: coding, methodology, epistemology, reflecting
---

*Last updated 2026-05-31.*

A benchmark asks us to trust three things: that the tasks are real, that the grader is fair,
and that the answer key works. This audit asks whether those claims hold.

[DeepSWE](https://github.com/datacurve-ai/deep-swe) arrived on May 26, 2026 as a
contamination-free coding benchmark: 113 tasks drawn from active repositories,
each graded by its own verifier. The most basic check is to take the answer key
and ask whether it passes its own test.

## The check

Every DeepSWE task ships a reference solution and a verifier. The verifier applies
a hidden test patch and runs the suite; a passing solution scores 1. The check is
simple. Apply the *reference* solution, run the verifier, confirm it scores 1. If
a task's own gold cannot pass the test built for it, that task cannot be trusted
until the contradiction is resolved. No model is involved, so the token cost is zero.
One spot machine, ten tasks at a time, the whole set in under an hour, under a dollar.

This is the check you would run before shipping. The authors publish the harness
and the data, so anyone downstream can run it. I ran it.

## First, I audited myself

The first run failed all 113 tasks. Zero scores across the board.

The tempting headline writes itself: *contamination-free benchmark ships 113
broken tasks*. It would have been wrong. Uniform failure across every task is
never 113 independent defects. It is one fault in the thing they share: my
harness. The grading framework brings up its sandbox with `docker compose`, and
the bare [Amazon Linux](https://aws.amazon.com/linux/) image I provisioned ships
Docker without the Compose plugin. Every task errored before reaching the verifier.

I installed the plugin, added an assertion so the gap would fail loudly next time,
and re-ran. I suspected my own setup before I suspected theirs. That is the only
reason the rest of this is worth reporting.

## What the corrected run found

With the harness corrected, the goldens started passing one after another, exactly
as they should. Then a few did not.

Four of the 113 reference solutions fail their own verifiers:
`langchain-request-coalescing`, `narwhals-rolling-window-suite`,
`prometheus-transactional-reload-status`, and `skrub-duration-encoding`. No agent
attempted them. The answer key itself, applied verbatim, does not pass. Each was
re-run alone to rule out contention; a task is flagged only when its gold fails
in isolation.

Three things hold, and no more. Under the benchmark's published harness at the
pinned commit, the reference solution failed its verifier. The failure reproduced
in isolated reruns. The cause is unresolved. It could be a broken task, a flaky
test, or environment drift since the image was built. Sorting those apart is the
maintainer's job, not the auditor's. The bounded claim stands: a task in this
state cannot be trusted until the diagnosis happens.

## Where these failures live

A score implies a clean function: model and task in, pass or fail out. Between them
sits an authored apparatus: task selection, the instruction, the held-out test,
the reference solution, the acceptance criteria, the environment. A gold that
fails its own verifier puts two of those pieces in contradiction. An answer key
asserted correct but never run against its own test is, precisely, a confabulation:
a plausible artifact nobody checked. Which piece confabulated, and whether by
authoring or by drift, is for the maintainer to determine.

## The audit at a glance

<div class="table-wrap">
<table style="max-width:100%; margin:1em auto; font-size:14px;">
<colgroup><col style="width:12em"><col><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Claim</th><th style="background:#f0f0f0">Observation</th><th style="background:#f0f0f0">Analysis</th><th style="background:#f0f0f0">Recommendation</th></tr></thead>
<tr><td><strong>Tasks are original, the benchmark is contamination-free</strong></td><td>One spot-check holds: <code>matchEach</code> absent from <a href="https://github.com/gvergnaud/ts-pattern"><code>ts-pattern</code></a> code, PRs, issues; solutions held out. 1 of 113 checked.</td><td>Verifiable in principle; cleaner substrate than the contaminated <a href="https://www.swebench.com/verified.html">SWE-bench Verified</a>. Consistent with the claim, not established across the set.</td><td>Publish the per-task originality check across all 113.</td></tr>
<tr><td><strong>All 113 tasks are gradeable by their own verifiers</strong></td><td>4 golds fail their own verifier (<code>langchain-request-coalescing</code>, <code>narwhals-rolling-window-suite</code>, <code>prometheus-transactional-reload-status</code>, <code>skrub-duration-encoding</code>), each confirmed in isolation.</td><td>A gold failing its own test: untrustworthy until resolved. Cause undetermined (broken task, flaky test, or drift). No gold-passes-verifier check on record.</td><td>Run gold-passes-verifier before shipping; fix or exclude failures; publish the check.</td></tr>
<tr><td><strong>A lighter, standardized harness does not disadvantage any model</strong> (popularly inflated to "less prompting is better")</td><td>3 model families, <a href="https://github.com/SWE-agent/mini-swe-agent"><code>mini-swe-agent</code></a> vs each native CLI. Single 10-task slice, one run per cell, no intervals or tests. Claimed: "matches or beats every native harness at comparable token cost."</td><td>10 tasks, one run, no variance: can't carry a directional claim. "Matches or beats" without error bars is consistent with noise. The "less is more" reading isn't in the data.</td><td>Paired ablation at scale (all 113), repeated for variance: confidence intervals, significance test, published trajectories.</td></tr>
</table>
</div>

The harness-comparison claim rests on a specific scaffolding. Pier hardcodes
[`mini.yaml`](https://github.com/SWE-agent/mini-swe-agent/blob/main/src/minisweagent/config/mini.yaml)
from `mini-swe-agent` as the base config
([`agents/installed/mini_swe_agent.py:765`](https://github.com/datacurve-ai/pier/blob/main/src/pier/agents/installed/mini_swe_agent.py#L765)),
and the DeepSWE README adds no override. The system prompt is one sentence; the
instance prompt, verbatim:

> You are a helpful assistant that can interact with a computer.
>
> ---
>
> Please solve this issue: {{task}}
>
> You can execute bash commands and edit files to implement the necessary changes.
>
> ## Recommended Workflow
>
> This workflow should be done step-by-step so that you can iterate on your changes and any possible problems.
>
> 1. Analyze the codebase by finding and reading relevant files
> 2. Create a script to reproduce the issue
> 3. Edit the source code to resolve the issue
> 4. Verify your fix works by running your script again
> 5. Test edge cases to ensure your fix is robust
> 6. Submit your changes and finish your work by issuing the following command: `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`. Do not combine it with any other command. `<important>`After this command, you cannot continue working on this task.`</important>`
>
> ## Command Execution Rules
>
> You are operating in an environment where
>
> 1. You issue at least one command
> 2. The system executes the command(s) in a subshell
> 3. You see the result(s)
> 4. You write your next command(s)
>
> Each response should include:
>
> 1. **Reasoning text** where you explain your analysis and plan
> 2. At least one tool call with your command
>
> **CRITICAL REQUIREMENTS:**
>
> - Your response SHOULD include reasoning text explaining what you're doing
> - Your response MUST include AT LEAST ONE bash tool call
> - Directory or environment variable changes are not persistent. Every action is executed in a new subshell.
> - However, you can prefix any action with `MY_ENV_VAR=MY_VALUE cd /path/to/working/dir && ...` or write/load environment variables from files
> - Submit your changes and finish your work by issuing the following command: `echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT`. Do not combine it with any other command. `<important>`After this command, you cannot continue working on this task.`</important>`
>
> Example of a CORRECT response:
>
> `<example_response>`
> I need to understand the structure of the repository first. Let me check what files are in the current directory to get a better understanding of the codebase.
>
> [Makes bash tool call with `{"command": "ls -la"}` as arguments]
> `</example_response>`
>
> `<system_information>`
> {{system}} {{release}} {{version}} {{machine}}
> `</system_information>`
>
> ## Useful command examples
>
> ### Create a new file:
>
> ```
> cat <<'EOF' > newfile.py
> import numpy as np
> hello = "world"
> print(hello)
> EOF
> ```
>
> ### Edit files with sed:
>
> *(template branch: on macOS, prepend a note instructing the use of `sed -i ''` instead of `sed -i`)*
>
> ```
> # Replace all occurrences
> sed -i 's/old_string/new_string/g' filename.py
>
> # Replace only first occurrence
> sed -i 's/old_string/new_string/' filename.py
>
> # Replace first occurrence on line 1
> sed -i '1s/old_string/new_string/' filename.py
>
> # Replace all occurrences in lines 1-10
> sed -i '1,10s/old_string/new_string/g' filename.py
> ```
>
> ### View file content:
>
> ```
> # View specific lines with numbers
> nl -ba filename.py | sed -n '10,20p'
> ```
>
> ### Any other command you want to run
>
> ```
> anything
> ```

Measured against the native CLIs (`claude-code`, `codex`, `gemini-cli`, `opencode`), that asymmetry sits less in prompt length than in tool surface area. `mini-swe-agent` exposes one tool: `bash`. The native CLIs each ship a typed tool suite (Read, Write, Edit, Grep, Glob, and so on), each with its own schema and ergonomics. Bash can emulate most of what those tools do, but the interfaces differ, and that difference is exactly what a scaffolding study is meant to characterize. A ten-task single-run comparison across that gap is asked to carry the directional claim, and the statistical power is not there.

## The second read that didn't run

Read the rest as a second reader's note: the review that should have happened before
this shipped, since whatever review ran did not catch four golds that fail their own
tests. This section concerns process, not the leaderboard. I have not rerun a single
number and I dispute none of them. The question is only whether the process earns
the confidence of the claim. The work is close, and the gaps are cheap to close.

Two checks, both nearly free, catch what this audit caught. First, run every task's
gold through its own verifier, then fix or exclude the ones that fail. That is the
audit above, and it cost about a dollar. Second, have a model read each task cold,
the instruction beside the reference solution and the test, and flag where they
disagree. Codex or Gemini does that in a single pass for pocket change.

And the timing is unforgiving. Once a benchmark is public and scored against, it
freezes like any measurement instrument: patch a task now and you change the
instrument, breaking comparability with every number already posted. Fixing these
four in place would break that comparability. The clean repair is a versioned
re-release of the whole set, re-graded. A dollar of pre-ship checking would have
spared that. That is the real cost of skipping it.

A cheaper route is open even now: claim less. A benchmark that labels its limits,
that the tasks are not all gold-verified and the harness comparison is a
ten-task pilot, asks only for the trust it has earned. A caveat costs nothing and
breaks no comparability.

So the note is short. Before shipping, run the answer key against its own test and
let a second reader catch the contradictions. After shipping, if those checks were
skipped, say so in the limitations. Either way, publish the runs so the next reader
does not have to find the cracks. The cheapest version of better is plain. It is
fine to ship unfinished work; it is not fine to call it finished when it is not.

## Update: the review (2026-05-29)

After this post first ran, I went back and reviewed the artifact directly.
The single-page React app at [`deepswe.datacurve.ai`](https://deepswe.datacurve.ai/)
loads its data from five JSON files under `/artifacts/`:
[`summary.json`](https://deepswe.datacurve.ai/artifacts/summary.json),
[`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json),
[`heatmap.json`](https://deepswe.datacurve.ai/artifacts/heatmap.json),
[`tasks.json`](https://deepswe.datacurve.ai/artifacts/tasks.json), and
[`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json) (every
individual rollout, 8852 records). Those files are public, and any reader can
check the artifact through them. They are mirrored to
[the audit repo](https://github.com/kimjune01/deepswe-run/tree/main/external/deepswe-leaderboard/raw).
I retract one critique from the section above. Per-task receipts are published,
just behind URLs the UI doesn't surface. That much is to the maintainers' credit.

The review has three parts. First, the audit of the artifact: four things in
the content that do not hold up. Second, the dossier: the incentive landscape
the artifact was built inside, which explains why the bench succeeds as
marketing and fails as science. Third, a five-minute demonstration that the
artifact-internal failures are catchable by any reader with an agent. The post
is the review.

### Audit of the artifact

#### The verdicts are not reproducible from the published artifacts

The trial records in
[`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json) carry a
`has_model_patch: true` flag on every scored rollout, alongside
`has_trajectory`, `has_agent_log`, and `has_verifier_output`. The per-trial
JSON at `/artifacts/trials/{trial_name}.json` (for example
[the `abs-module-cache-flags__GUstLQs` trial JSON](https://deepswe.datacurve.ai/artifacts/trials/abs-module-cache-flags__GUstLQs.json),
a passing rollout of `gpt-5.5` that returned reward 1) carries a provenance
field that says:

> Raw trajectory, patch, agent log, and verifier output are linked to release
> object storage when present.

The trial JSON does not carry the link, and the leaderboard site does not expose
the underlying objects through any URL I could find. Every place the artifacts
could live came up empty:

- Probes against `/artifacts/trials/{trial_name}/<file>` for plausible filenames
  (`model_patch.patch`, `model_patch`, `trajectory.json`, `agent.log`,
  `verifier_output.txt`) returned 404s.
- The `/raw/rollouts/deep-swe-all-4x-cross-bench-minimal/{trial_name}` path the
  provenance field cites internally returns 404 publicly.
- The [`datacurve-ai/deep-swe`](https://github.com/datacurve-ai/deep-swe) GitHub
  repo contains only task definitions and a README, with
  [no GitHub Releases](https://github.com/datacurve-ai/deep-swe/releases) and no
  LFS-stored rollouts.
- The [`datacurve-ai/pier`](https://github.com/datacurve-ai/pier) repo has
  [releases (`v0.1.0`, `v0.2.0`)](https://github.com/datacurve-ai/pier/releases),
  but those are verifier code, not rollout artifacts.
- The HuggingFace org [`datacurve-ai`](https://huggingface.co/datacurve-ai)
  returned 401 on every dataset name I tried, including `datacurve-ai/deep-swe-rollouts`.

[Press coverage](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole)
cites the maintainers' decision to publish the full dataset and agent
trajectories as a mitigating factor against benchmark concerns. The trajectory
metadata is published. The trajectory content (the model's submitted patch, the
agent's full step log, the verifier's stdout) is not.

The aggregate counts in
[`heatmap.json`](https://deepswe.datacurve.ai/artifacts/heatmap.json) roll up
to the headline in
[`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json)
under the documented arithmetic. The per-trial outcomes in
[`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json) sum to
the per-cell counts. The verdicts themselves do not survive an independent
check, because there is no patch to re-grade. `has_model_patch: true` is a
promise, not a link.

A benchmark whose verdict receipts cannot be retrieved is not falsifiable at
the verdict level. The published artifacts let me check the counting. They do
not let me check whether the counting reflects what the grader would say if I
re-ran it against the published outputs. Without that check, the artifact's
claim to measure is not testable from what it publishes.

#### The footer disagrees with the headline math

The leaderboard's headline number for `gpt-5.5 [xhigh]` is **0.70045**.
Computing that from the heatmap reproduces it exactly, with one specific
denominator choice.

```
mean(per-task pass-fraction over 111 cells)  = 0.70045  ← matches headline
mean over 113, missing → 0                   = 0.68805
```

The leaderboard's footer in
[`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json)
sets `n_tasks_in_set: 113`. The actual division is by 111. Two tasks are
dropped from `gpt-5.5`'s denominator:
[`goreleaser-retry-publish-auditing`](https://deepswe.datacurve.ai/data/tasks/goreleaser-retry-publish-auditing)
and
[`opa-rego-rule-profiling`](https://deepswe.datacurve.ai/data/tasks/opa-rego-rule-profiling).
The
[heatmap](https://deepswe.datacurve.ai/artifacts/heatmap.json) has no cell
for `gpt-5.5` on either, though other frontier models do. `gpt-5.4` hits
`goreleaser` 4/4, and `claude-opus-4.7` hits it 4/4, so the tasks are
gradeable. `gpt-5.5`'s rollouts on those two were excluded under the
documented error-exclusion policy, which is defensible. The footer's label
is not. The announced denominator is 113. The actual denominator is 111. The
math a reader gets applying the footer exactly is 68.8%, not 70.0%.

The labelling is the finding here. The exclusion math is defensible under
the documented policy; the field that announces the denominator does not
match the field that computes it. A central-number footer that disagrees
with the central-number math is the kind of inconsistency a reader who
takes the methodology section at face value walks straight into.

#### The grader's verdicts disagree with an independent re-run

The four reference-solution failures from the audit above appear on the
leaderboard's per-task heatmap. Three of them pass cleanly under `gpt-5.5`:

<div class="table-wrap">
<table style="max-width:100%; margin:1em auto; font-size:14px;">
<colgroup><col style="width:22em"><col><col><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">task</th><th style="background:#f0f0f0">gpt-5.5</th><th style="background:#f0f0f0">claude-opus-4.7</th><th style="background:#f0f0f0">gemini-3.5-flash</th><th style="background:#f0f0f0">total across 16 models</th></tr></thead>
<tr><td><a href="https://deepswe.datacurve.ai/data/tasks/langchain-request-coalescing">langchain-request-coalescing</a></td><td style="white-space:nowrap">3/4</td><td style="white-space:nowrap">0/4</td><td style="white-space:nowrap">0/4</td><td style="white-space:nowrap">10/64</td></tr>
<tr><td><a href="https://deepswe.datacurve.ai/data/tasks/narwhals-rolling-window-suite">narwhals-rolling-window-suite</a></td><td style="white-space:nowrap">4/4</td><td style="white-space:nowrap">3/4</td><td style="white-space:nowrap">0/4</td><td style="white-space:nowrap">34/64</td></tr>
<tr><td><a href="https://deepswe.datacurve.ai/data/tasks/prometheus-transactional-reload-status">prometheus-transactional-reload-status</a></td><td style="white-space:nowrap">0/4</td><td style="white-space:nowrap">0/4</td><td style="white-space:nowrap">0/4</td><td style="white-space:nowrap">2/64</td></tr>
<tr><td><a href="https://deepswe.datacurve.ai/data/tasks/skrub-duration-encoding">skrub-duration-encoding</a></td><td style="white-space:nowrap">4/4</td><td style="white-space:nowrap">4/4</td><td style="white-space:nowrap">0/4</td><td style="white-space:nowrap">12/64</td></tr>
</table>
</div>

My oracle audit, run at the pinned commit, found these four golds failing
their own verifier in two consecutive isolated runs. The leaderboard's heatmap
shows three of them passing routinely under `gpt-5.5`. The candidates for the
disagreement are pinned-image drift between my pier and theirs, isolation
flake on tasks the leaderboard gives four shots at, or the grader returning
different verdicts on the same nominal pipeline. The public data does not pick
between the three. The original audit's narrow claim still holds against all
three readings: a gold failing its own verifier in two consecutive isolated
runs is untrustworthy until diagnosed.

A benchmark whose grader disagrees with an independent re-run on its own pinned
pipeline is exposing an unresolved consistency problem in its scoring function,
whether the maintainers have responded to it yet or not.

#### The grader scores a choice the task never specifies

The four golds above fail their own verifier. This is the inverse, and the harder
one to see: a verifier whose gold passes cleanly while it scores a behavior the
instruction never determines. Nothing looks broken. The gold passes, the verifier
runs, the task reads healthy. What it measures is the problem.

[`adaptix-name-mapping-aliases`](https://github.com/datacurve-ai/deep-swe/blob/2f0f4125/tasks/adaptix-name-mapping-aliases/instruction.md)
adds alias support to a field-mapping config, and its entire specification of overlay
behavior is one parenthetical: aliases are *"overlay-mergeable ... first-wins-per-field."*
The verifier, `test_alias_overlay_first_wins_per_field`, fixes one reading of that phrase:
when two config layers each alias the same field, the first layer's alias stays valid and
the second layer's is discarded, so an input keyed by the second alias must raise
`NoRequiredFieldsLoadError`. Nothing in the prose entails that. A union, where both aliases
resolve, fits *"overlay-mergeable ... first-wins-per-field"* exactly as well. From the
instruction alone the behavior is a coin flip, and the hidden test scores the guess: a
solver that reads the parenthetical the other way fails the task on a convention the prose
never stated.

That makes at least this task's score a specification lottery. It grades whether the model
guessed the author's unstated convention, not the stated feature alone, and the guess is
invisible in a single reward; it does not wash out the way infrastructure flake does,
because the model is not flaking, it is committing to a reading the grader happens to
penalize. Real PRDs are vague, and a benchmark drawn from real work inherits that vagueness;
the defect is not the underspecification but the hidden test resolving it silently and
scoring the resolution as capability. Getting this one right from the prose is impossible or
a coin flip, which reads as a due-diligence gap rather than anything worse, the kind a launch
reviewed as a marketing release produces and a measurement self-audit catches. That
self-audit is the second-reader check this post already proposes: a model reading the
instruction beside the test flags the overlay clause as underdetermined before any solver
runs. One task is worked through here; I make no claim about how many of the 113 share the
property.

#### A design choice with a short half-life

DeepSWE publishes everything. The tasks, the harness, the verifier code, the
docker images, the reference solutions. That is the design choice that makes
the benchmark immediately and trivially reproducible by any third party, and
it is also the choice that gives the benchmark a useful lifetime in the
single-digit months. Web crawl picks up the tasks. Synthetic-data pipelines
sample from the public artifacts. By the next model generation, the
contamination-free claim that the benchmark makes about itself as of May 2026
is no longer empirically defensible.

[SWE-bench Pro](https://www.swebench.com/pro.html) made a different design
choice: a private test set, held out from the public artifact, accessible only
through the maintainers' grading service. The held-out set is what keeps the
benchmark usable as a measurement instrument over time. The trade-off is
explicit: public reproducibility costs you contamination resistance; held-out
sets cost you third-party verifiability. There is no third choice.

The DeepSWE launch leaned on a "Pro is saturated, here is the harder one"
positioning. That claim does not survive contact with the numbers. Pro's
leading models sit around 80%. Saturation is what you see on the public
[Verified](https://www.swebench.com/verified.html) set, where the top three
models (Claude Mythos Preview, Claude Opus 4.8, Claude Opus 4.7) sit between
88% and 94% as of May 2026, and the leaderboard has stopped being able to
discriminate between them. Eighty percent is not saturation. Eighty percent
is the operating range where a held-out benchmark is still doing the job it
was designed for.

The "saturated" framing was the justification for replacing
a [working benchmark](https://june.kim/the-hypothesis-graph-as-semantic-memory) and its
[public per-instance receipts](https://github.com/kimjune01/swebench-pro) with
a marketing-shaped one before its useful life was over.

<img src="/assets/saturation-by-benchmark.svg" alt="Bar chart of top-model resolve rate by benchmark as of May 2026: DeepSWE 70% (gpt-5.5), SWE-bench Pro ~80%, both below an 88% saturation line; SWE-bench Verified at 94% with its top three models clustered 88–94%, inside the shaded saturation zone where the leaderboard can no longer discriminate." style="width:100%; max-width:560px; display:block; margin:1.5em auto;">

DeepSWE took the public-reproducibility side of the trade-off. The half-life
that matters here is not contamination timing in isolation; it is the
bench's ability to prove anything. A bench loses its proving power on two
axes. Saturation is one: when the top models cluster within a few points of
each other and the leaderboard cannot discriminate, the bench can no longer
prove an ordering. Contamination is the other: when models have seen the
answers during training, a high score no longer proves capability and only
proves memorization.

SWE-bench Verified is, as of May 2026, publicly failing on both
axes, and the failure is documented by the lab whose models top the
leaderboard. OpenAI's
[deprecation post](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
reports gold patches reproducible verbatim from training weights, problem
statements leaking into pretraining corpora, and sixty percent of failed
tests subsequently found to be broken. That last item is the one that
closes the obvious rescue: a saturated bench could in principle still
prove reliability by marking the unsolved frontier, but a bench whose
unsolved tail is mostly broken tests cannot. Ranking signal and
reliability signal die on the same mechanism.

OpenAI stopped reporting
Verified scores. The trajectory Verified followed is the trajectory DeepSWE is
starting. The half-life is whatever it takes for the same two failure modes
to apply at DeepSWE's smaller scale, on the same publication choice, in the
same training environment. As a marketing artifact, whatever that half-life
turns out to be is all the half-life it needs.

Credit where it lands. Hand-curating 113 original problems, each with a
verifier and a reference solution, is not small work. The team had to invent
the problems, write the tests, and produce solutions that nobody outside
Datacurve had ever seen. That is months of skilled engineering labor, and
the contamination-free claim is design-level honest about the tasks
themselves: these are not lifted from public PRs or issues, they are
engineering exercises authored from scratch.

The same publication choice
that breaks the artifact's measurement life is what gives it its training
life. As a training corpus, the 113 tasks have a longer half-life than three
months and look like exactly what the team actually built. The audit above
is about a specific portrayal: that the verdicts are a measurement readers
should trust. The artifact's claim to be a training aid is unaudited,
defensible on inspection, and probably accurate.

### The dossier

Four problems with the content. Each would, on its own, prompt an editor
query at a peer-reviewed venue. None are subtle.

The dossier evidences why the bench fails as a scientific measurement. The
bench succeeds at three other things. It works as marketing: favorable press,
customer adoption, a $15M round closed. It works as engineering: hand-curated
tasks, credited above. It probably works as a training corpus, which is
probably what the team actually built. The audit measures it against the
fourth standard, the one the public portrayal asks for.

The failures the audit catches are the failures that emerge when an artifact
is built by an incentive landscape with high standards on engineering and
marketing and no standard for measurement self-audit. Naming that landscape is
what the dossier does:

- The producing entity sells training data to the foundation model labs whose
  models the bench scores.
- Individual employees at those labs are on the producing entity's Series A cap table.
- The bench's top result is the flagship of one of those labs.
- The team that built the bench has no prior public technical artifact on
  benchmarking or evaluation, on any venue where prior methodology positions
  are a matter of record.

None of those relationships are conflicts when the artifact is marketing. Each
of them is a conflict when the artifact is asked to be science. The bench was
asked to be the latter, by [the press](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole)
and by the readers who cited it. That request was unanswered.

#### The four authors, and what they have written before

The byline on
[the leaderboard's blog post](https://deepswe.datacurve.ai/blog) lists four
authors: **Wenqi Huang, Charley Lee, Leonard Tng, Serena Ge**. They are
Datacurve's team. The two named co-founders are
Serena Ge ([CEO](https://www.linkedin.com/in/serena-ge-4583731b4/),
[`@serenaa_ge`](https://x.com/serenaa_ge)) and
[Charley Lee](https://www.linkedin.com/in/charley-lee/), both
[University of Waterloo CS](https://uwaterloo.ca/computer-science/news/cs-led-startup-secures-177m-transform-ai-training-data)
dropouts who went through
[YC W24](https://www.ycombinator.com/companies/datacurve). Serena interned
at [Cohere](https://cohere.com/) on synthetic-data work; Charley interned at Google on multi-modal
RL. [Leonard Tng](https://leonardtng.com/) is an engineer with an
undergraduate background from [Yale-NUS College](https://en.wikipedia.org/wiki/Yale-NUS_College). Wenqi Huang is the fourth
author; multiple unrelated profiles share that name and the LinkedIn for
the Datacurve Wenqi Huang was not unambiguously surfaced.

What they have published before DeepSWE, by name, across the venues where
benchmarking and evaluation methodology is publicly discussed:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:18em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Venue</th><th style="background:#f0f0f0">Result</th></tr></thead>
<tr><td><a href="https://arxiv.org">arXiv</a></td><td>none</td></tr>
<tr><td><a href="https://zenodo.org">Zenodo</a></td><td>none</td></tr>
<tr><td><a href="https://huggingface.co/papers">Hugging Face Papers</a></td><td>none</td></tr>
<tr><td><a href="https://www.semanticscholar.org/">Semantic Scholar</a></td><td>none</td></tr>
<tr><td><a href="https://openreview.net">OpenReview</a></td><td>none</td></tr>
<tr><td><a href="https://scholar.google.com/">Google Scholar</a></td><td>none</td></tr>
<tr><td><a href="https://www.researchgate.net/">ResearchGate</a></td><td>none</td></tr>
<tr><td><code>datacurve.ai/</code> company blog</td><td>no blog exists</td></tr>
<tr><td>Substack (any author)</td><td>none under their names</td></tr>
<tr><td>Medium (any author)</td><td>none containing technical writing on benchmarks/evaluation</td></tr>
<tr><td>Personal sites</td><td><a href="https://leonardtng.com/"><code>leonardtng.com</code></a>; no methodology writing</td></tr>
<tr><td>Twitter/X</td><td><a href="https://x.com/serenaa_ge"><code>@serenaa_ge</code></a>; company and personal updates only</td></tr>
</table>

DeepSWE is the four authors' first and only public technical artifact on
benchmarking or evaluation. None of them has, to my searching, written publicly
about how a benchmark should be designed, what a reproducible verdict requires,
what a contamination check should look like, or what denominator hygiene
demands. The methodology DeepSWE applies has no prior version any author has
staked a position on. The artifact is the position.

A reader who would otherwise extend the trust an audience extends to domain
professionals (researchers with a record of writing about their methodology
before applying it) has no record here to extend trust against. Trust would
have to be extended to the artifact alone, and on the review above, the artifact
does not earn it.

#### What the artifact's review surface optimized for

The leaderboard was built by the company that
[sells](https://www.ycombinator.com/companies/datacurve) frontier coding
training data to the foundation model labs whose models the leaderboard
scores. The
[$15M Series A](https://techcrunch.com/2025/10/09/datacurve-raises-15-million-to-take-on-scaleai/)
was led by Mark Goldberg at [Chemistry](https://www.chemistry.vc/), with participation explicitly named
as "employees at DeepMind, Vercel, Anthropic, and OpenAI." The seed round
was led by [Balaji Srinivasan](https://en.wikipedia.org/wiki/Balaji_Srinivasan). [YC](https://www.ycombinator.com/companies/datacurve)'s
W24 partner [Garry Tan](https://en.wikipedia.org/wiki/Garry_Tan) is the YC-side relationship.

The leaderboard's top result is **OpenAI's gpt-5.5 at 70%**, sixteen
percentage points ahead of the next model.

None of those facts alone is a conflict of interest. The combination is what a
peer-reviewed venue would require to be disclosed, in the section that begins
"Conflicts of Interest." There is no such section on
[the leaderboard's blog post](https://deepswe.datacurve.ai/blog). The artifact
contains no statement that its top result is the flagship product of a company
whose individual employees are on the producing company's cap table and whose
corporate entity is, by the producing company's business model, a customer or
potential customer.

The review surface the artifact was held to before publication was the review
surface a YC-stage startup uses for a marketing release: the team itself, the
YC partner, the lead investor, the press contacts. Those reviewers optimize
for outcomes the artifact is succeeding at: favorable
[VentureBeat](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole)
coverage, [TechCrunch](https://techcrunch.com/2025/10/09/datacurve-raises-15-million-to-take-on-scaleai/)
coverage, customer adoption, the next round. On those metrics it has worked.
The Series A closed. The press cycle was friendly. The customer base is the
same set of frontier model labs whose models the benchmark scores.

The reviewers a peer-reviewed venue would have provided, methodologists whose
reputation depends on catching denominator slips, identity-check failures,
and conflict-disclosure gaps, were not in the room. The audit's failures above
are the kind a domain methodologist would have surfaced on first read. None of
those people had standing here.

There was no scientist in the room to call it out.

### The five-minute audit (codex)

The work in the audit above is not subtle. The patches gap shows up in any
per-trial JSON. The denominator gap shows up when you compute one mean against
two divisors. The verifier disagreement shows up when you run one shell loop
against the pinned commit. None of those require expertise a careful reader
with an agent doesn't have. To show that, I ran the artifact through
[OpenAI's codex CLI](https://github.com/openai/codex) with model `gpt-5.5` and
the following five-line prompt:

```
I'm considering using https://deepswe.datacurve.ai/ as a benchmark to
compare LLMs for a coding-agent project. Before I trust the leaderboard,
audit it skeptically: any methodological problems, missing disclosures,
inconsistencies in what they publish, or things a careful reader should
flag?

Use their public artifacts at /artifacts/*.json (summary, leaderboard,
heatmap, tasks, trials) and the per-trial JSONs at
/artifacts/trials/{trial_name}.json. Cite specific URLs and JSON fields
for any issue you find.
```

Five lines. No mention of the findings above. No priming on patches,
denominators, conflicts of interest, or any specific defect. Just "audit it
skeptically, here are the artifacts, cite specifics."

Codex spent about four minutes, ran its own curls against the public endpoints,
and produced ten numbered findings with citations. Three reproduced the audit
above. It independently identified the denominator gap, the two specific tasks
the top model drops, and the `has_model_patch: true` flag whose link is not
delivered.

Seven are additional methodological catches the audit above does not contain.
**Credit for these seven is codex's, not mine. I had not surfaced them before
running the prompt, and would not have without it.**

- **The public trial universe is larger than the leaderboard universe.**
  [`summary.json`](https://deepswe.datacurve.ai/artifacts/summary.json)
  reports `counts.trials = 8852`, while
  [`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json)
  is scoped to `"Full May 13 DeepSWE Pier job"` using the `deep-swe/full`
  subset.
  [`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json) also
  contains `eval_scope = "cross-bench"` rows and `source = "swebenchpro"`
  rows that are not in scope for the leaderboard. The trial file's own
  structure does not make the separation obvious to a reader who treats
  it as the source of truth for the leaderboard's verdicts.
- **Uneven exclusion counts across models.**
  [`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json) shows
  `gemini-3-flash-preview` with 24 excluded full-scope trials, `gpt-5.5`
  with 8, and several models with 0. The exclusion policy is defensible
  only if the underlying errors are infrastructure-random; an uneven
  exclusion distribution shifts the comparison without that being
  apparent from the leaderboard.
- **[Wilson confidence intervals](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval) computed over clustered trials as if
  they were independent.**
  [`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json)'s
  `ci_method` field says "95% Wilson over attempts; each trial is
  treated as one independent unit." Four trials per task share the
  same prompt, verifier, and base commit; the headline `pass@1` is
  itself macro-averaged over tasks. Treating attempts as independent
  underrepresents task-level correlation and produces overconfident
  intervals.
- **`pass_rate` field whose definition diverges from the naïve
  interpretation.**
  In [`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json),
  `pass_rate` equals `pass_at_1` (macro-averaged over tasks), not
  `n_passed / n_attempted`. For `claude-sonnet-4-6` the published
  `pass_rate` is 0.3156 while the attempt-level rate is 142/447 =
  0.3177. The duplicated fields invite the reader who skims to use
  the wrong one.
- **Missing prompts and verifier commands in `tasks.json`.**
  [`tasks.json`](https://deepswe.datacurve.ai/artifacts/tasks.json)
  exposes `id`, `repository`, `base_commit_hash`, `display_description`,
  `problem_title`, and `prompt_characters`, but not the full prompt,
  the verifier command, the hidden tests, the docker image, the
  timeout policy, the dependency setup, or the scoring script. A
  reader with the artifacts cannot reconstruct what the grader did.
- **Mixed-length and short `base_commit_hash` values.**
  Most entries in [`tasks.json`](https://deepswe.datacurve.ai/artifacts/tasks.json)
  are 40-character SHAs. `eicrud-keyset-pagination-cursor` is pinned
  to `68dafce` (7 characters), `langchain-request-coalescing` to
  `7cef35b`, and `koota-entity-snapshot-rollback` to a 39-character
  string that is neither a full SHA nor a recognizable abbreviation.
  Short SHAs can resolve unambiguously today and silently re-resolve
  later if the upstream repo changes.
- **Non-normalized `reasoning_effort` across model configurations.**
  [`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json)
  records `gpt-5.5` at `xhigh`, `claude-opus-4.7` at `max`,
  `claude-sonnet-4.6` at `high`, `gemini-3.5-flash` at `medium`, and
  many of the open-router models at `null`. The leaderboard's column
  is presented as a model ranking; what is actually being ranked is a
  model-and-agent-config pair, with the harness varying across rows.

The full transcript, including codex's tool calls and final summary, is
[in the audit repo](https://github.com/kimjune01/deepswe-run/tree/main/external/codex-audit).
[The prompt is there too](https://github.com/kimjune01/deepswe-run/blob/main/external/codex-audit/prompt.txt).
Total cost: a few cents in `gpt-5.5` tokens.

Anything in this post that codex caught, you can catch by running the prompt
at your own agent. Anything codex caught that this post does not contain (seven
issues) is also one prompt away from your reading. The seven additional findings
above are codex's contribution. The audit section is mine. The reader-challenge
close belongs to whoever runs the prompt next. The artifact has been live, cited
in [VentureBeat](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole),
quoted as authoritative across the AI press cycle, and treated as evidence in
arguments about model capability since May 2026. The work to surface it as
content with this many problems has been one prompt away the entire time.

The audit's claim, that this is not science, is not only about the artifact and
its producers. The artifact's reception is the other half of why a piece of work
with these properties succeeded. Vibe coders are fooled by clever marketing.
Press reporters pass the marketing through without reading the source.
Readers mistake a chart on a company subdomain for a measurement. The audit catches
the artifact's failures. The reception is what let those failures not matter.

"Auditing DeepSWE" is doing more work as a title than it announces. There are
three audits in scope here. I am auditing the artifact. The reception is not
auditing the artifact. DeepSWE, before publication, did not audit itself for
the gold-passes-verifier check that opens this post, even though the
authors publish the harness and the data that make the check easy. Three
audits in scope, two of them missing.

What I am witnessing is that
across every outlet that cited the artifact as authoritative, nobody ran
the five-minute check. Not the
[VentureBeat](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole)
reporter writing the headline. Not the
[TechCrunch](https://techcrunch.com/2025/10/09/datacurve-raises-15-million-to-take-on-scaleai/)
piece on the Series A. Not the aggregator pages on
[NOVALOGIQ](https://novalogiq.com/2026/05/27/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole/),
[Data World Bank](https://www.dataworldbank.net/2026/05/26/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole/),
[Winbuzzer](https://winbuzzer.com/2026/05/28/deepswe-puts-gpt-55-ahead-in-ai-coding-tests-xcxwbn/),
[36Kr](https://eu.36kr.com/en/p/3827435586736777), or
[The Neuron](https://www.theneuron.ai/explainer-articles/datacurves-deepswe-exposes-a-weird-new-problem-with-ai-coding-leaderboards/)
republishing the press release. Not the social posts citing the headline as a
fact. And not [Theo at t3](https://youtu.be/JpSHyEIZ_bo?t=144),
an investor in Datacurve [by his own disclosure](https://youtu.be/JpSHyEIZ_bo?t=144),
whose reaction video proudly promotes DeepSWE without the five-minute check
having been run against it.

<iframe
  width="100%"
  height="420"
  src="https://www.youtube.com/embed/JpSHyEIZ_bo?start=144"
  title="Theo at t3 — DeepSWE reaction video"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen></iframe>

Each of them had a terminal and an agent. None of them ran the prompt before
passing the headline on. The check this post documents was within reach of
every single one of them.

Run the prompt at your own agent. The artifact's verdicts are not falsifiable
from what it publishes. The denominator on its central number disagrees with
its own footer. Its grader disagrees with an independent re-run on the same
nominal pipeline. The team that produced it has, between them, no prior public
technical artifact on benchmarking or evaluation. Its top result is the flagship
of a company whose individual employees are on the producing company's cap
table. None of these are conclusions you have to take on my authority. An agent
will read them off the public artifacts the moment you ask it to.

This is the kind of work tools shaped like
[june.kim/new-reading](https://june.kim/new-reading) are going to make routine.
Scientific literacy was never the credential. It was the procedure. The
procedure now ships with the model. Any reader with API access has the part of
the apparatus that, until last year, only a peer-review committee or a graduate
training pipeline could pretend to provide. The cost of running the procedure
fell to a few cents in tokens, and the gating fell with it.

The printing press for skeptical readers is only getting greased up. The next
benchmark released to the same audience, on the same surface, with the same
review structure, gets audited in five minutes by every reader who runs the
prompt before quoting the headline. That is the actual fence around marketing
artifacts in this field. Not peer review. Not citation politics. Not professional
society norms. Just every reader running the prompt before reading the headline.

## Attestation and reproducibility

The point of this post is not to be trusted. It is to be checked. So here is everything needed to
re-derive the quantitative claims above. The benchmark publishes the harness and the data. What it
did not publish is the gold-passes-verifier pre-ship check, plus the per-task run artifacts behind
the leaderboard. Those are below.

**What ran.** The `oracle` agent applies each task's own reference solution, then the task's own
verifier grades it through [Pier](https://github.com/datacurve-ai/pier) `0.2.0`, unmodified. No model
is involved, so model cost is zero. Subject: `datacurve-ai/deep-swe` pinned at commit
**`2f0f4125`** (tasks can change after publication; this is the exact version audited), all 113 tasks.
Compute: one spot `m7i.8xlarge` in `us-west-2`, ten tasks in parallel, under one dollar, 2026-05-27.

**Protocol.** Preregistered: the procedure was fixed and committed before the run. Pass 1 grades all
113 in parallel; pass 2 re-runs every non-passing task **sequentially and alone**, so a resource
hiccup is never reported as a defect. A task is flagged only when its gold fails in isolation. The
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
