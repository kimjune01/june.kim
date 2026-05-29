---
variant: post-wide
title: "Auditing DeepSWE"
tags: coding, methodology, epistemology, reflecting
---

A benchmark asks us to trust three things: the tasks are real, the grader is fair,
and the answer key works. This is an audit of whether those claims hold.

[DeepSWE](https://github.com/datacurve-ai/deep-swe) arrived last week as a
contamination-free coding benchmark: 113 tasks drawn from active repositories,
graded by per-task verifiers. The most basic check: take the answer key and ask
whether it passes its own test.

## The check

Every DeepSWE task ships a reference solution and a verifier. The verifier applies
a hidden test patch and runs the suite; a passing solution scores 1. So the check
is simple: apply the *reference* solution, run the verifier, confirm it scores 1.
If a task's own gold cannot pass the test built for it, the task cannot be treated
as a trustworthy graded instance until that contradiction is resolved. No model
is involved, so it costs nothing in tokens. One spot machine, ten tasks at a time,
the whole set in under an hour, all in for less than a dollar.

This is the check you would run before shipping. The authors publish the harness
and the data, so it is also the check anyone downstream can run. I ran it.

## First, I audited myself

The first run failed all 113 tasks. Zero scores across the board.

The tempting headline writes itself: *contamination-free benchmark ships 113
broken tasks*. It would have been wrong. A uniform failure across every task
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
attempted them; the answer key itself, applied verbatim, does not pass. Each was
re-run alone to rule out contention; a task is flagged only when its gold fails
in isolation.

Three things hold, and no more: under the benchmark's published harness at the
pinned commit, the reference solution failed its verifier; the failure reproduced
in isolated reruns; the cause is unresolved. It could be a genuinely broken task,
a flaky test, or environment drift since the image was built. Sorting those apart
is the maintainer's job, not the auditor's. The bounded claim stands on its own:
a task in this state cannot be treated as a trustworthy graded instance until
that diagnosis happens.

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
| **Tasks are original, the benchmark is contamination-free** | One spot-checked task holds up: the requested `matchEach` matcher is absent from [`ts-pattern`](https://github.com/gvergnaud/ts-pattern) upstream code, PRs, and issues; reference solutions are held out. I checked one of 113 | Verifiable in principle, and the design is a genuinely cleaner substrate than the contaminated [SWE-bench Verified](https://www.swebench.com/verified.html). One spot-check is consistent with the claim; it does not establish it across the set | Publish the per-task originality check so the claim is earned by inspection across all 113, not asserted from one |
| **All 113 tasks are gradeable by their own verifiers** | Four reference solutions fail their own verifier (`langchain-request-coalescing`, `narwhals-rolling-window-suite`, `prometheus-transactional-reload-status`, `skrub-duration-encoding`), each confirmed failing in isolation | A gold that fails its own test makes that task untrustworthy to grade against until resolved. Cause (broken task, flaky test, or environment drift) is undetermined; the public record shows no gold-passes-verifier check behind the published tasks | Run gold-passes-verifier before shipping; fix or exclude the failures; publish the check so others need not rediscover it |
| **A lighter, standardized harness does not disadvantage any model** (popularly inflated to "less prompting is better") | 3 model families, [`mini-swe-agent`](https://github.com/SWE-agent/mini-swe-agent) vs each native CLI, on a single 10-task slice, one run per cell, no intervals or tests; stated finding is "matches or beats every native harness at comparable token cost" | A ten-task, single-run comparison with no variance estimate cannot carry a directional scaffolding claim; "matches or beats" without error bars is consistent with noise. Their own wording is careful; the "less is more" reading is not in the data | Run a paired ablation at scale (all 113), repeated for variance, with confidence intervals, a significance test, and published trajectories |

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

The asymmetry from the native CLIs it is measured against (`claude-code`, `codex`, `gemini-cli`, `opencode`) sits less in prompt length than in tool surface area. `mini-swe-agent` exposes one tool, `bash`. The native CLIs each ship a typed tool suite (Read, Write, Edit, Grep, Glob, and so on) with their own schemas and ergonomics. Bash can emulate most of what those tools do; the interfaces are still materially different, and that difference is exactly what a scaffolding study is meant to characterize. A ten-task single-run comparison across that gap is the slice that has to carry the directional claim, and the statistical power is not there.

## The second read that didn't run

Read the rest as a second reader's note, the review that should have happened before
this shipped, since whatever review ran did not catch four golds that fail their own tests.
This section concerns process, not the leaderboard: I have not rerun a single
number and I dispute none of them. The question is only whether the process
behind them earns the confidence of the claim. The work is close, and the gaps
are cheap to close.

Two checks, both nearly free, catch what this audit caught. First, run every task's
gold through its own verifier and fix or exclude the ones that fail. That is the
audit above, and it cost about a dollar. Second, have a model read each task cold,
the instruction beside the reference solution and the test, and flag where they
disagree. Codex or Gemini does that in a single pass for pocket change.

And the timing is unforgiving. Once a benchmark is public and scored against, it is
frozen like any other measurement instrument: patch a task now and you change the
instrument, breaking comparability with every number already posted. Fixing these
four in place would break that comparability; the clean repair is a versioned
re-release of the whole set, re-graded. A dollar of pre-ship checking would have
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

## Update — the review (2026-05-29)

After this post first ran, I went back and reviewed the artifact directly.
The single-page React app at [`deepswe.datacurve.ai`](https://deepswe.datacurve.ai/)
loads its data from five JSON files under `/artifacts/`:
[`summary.json`](https://deepswe.datacurve.ai/artifacts/summary.json),
[`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json),
[`heatmap.json`](https://deepswe.datacurve.ai/artifacts/heatmap.json),
[`tasks.json`](https://deepswe.datacurve.ai/artifacts/tasks.json), and
[`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json) (every
individual rollout — 8852 records). Those files are public and let any
reader check the artifact directly. They are mirrored to
[the audit repo](https://github.com/kimjune01/deepswe-run/tree/main/external/deepswe-leaderboard/raw).
I retract one critique from the section above: per-task receipts are
published, just behind URLs the UI doesn't surface. That much is to the
maintainers' credit.

The review proceeds in two parts. The first is the audit of the artifact —
three things in the content that do not hold up. The second is the dossier —
the production conditions that explain why the content has those properties.
The post is the review.

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

The trial JSON does not carry the link. The leaderboard site does not expose
the underlying objects through any URL I could find. Probes against
`/artifacts/trials/{trial_name}/<file>` for plausible filenames
(`model_patch.patch`, `model_patch`, `trajectory.json`, `agent.log`,
`verifier_output.txt`) returned 404s. The
`/raw/rollouts/deep-swe-all-4x-cross-bench-minimal/{trial_name}` path the
provenance field cites internally returns 404 publicly. The
[`datacurve-ai/deep-swe`](https://github.com/datacurve-ai/deep-swe) GitHub repo
contains only task definitions and a README, with
[no GitHub Releases](https://github.com/datacurve-ai/deep-swe/releases) and no
LFS-stored rollouts. The
[`datacurve-ai/pier`](https://github.com/datacurve-ai/pier) repo has
[releases (`v0.1.0`, `v0.2.0`)](https://github.com/datacurve-ai/pier/releases),
but those are verifier code, not rollout artifacts. The HuggingFace org
[`datacurve-ai`](https://huggingface.co/datacurve-ai) returned 401 on every
dataset name I tried, including `datacurve-ai/deep-swe-rollouts`.

[Press coverage](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole)
cites the maintainers' decision to publish the full dataset and agent
trajectories as a mitigating factor against benchmark concerns. The
trajectory metadata is published. The trajectory content — the model's
submitted patch, the agent's full step log, the verifier's stdout — is not.

The aggregate counts in
[`heatmap.json`](https://deepswe.datacurve.ai/artifacts/heatmap.json) roll up
to the headline in
[`leaderboard.json`](https://deepswe.datacurve.ai/artifacts/leaderboard.json)
under the documented arithmetic. The per-trial outcomes in
[`trials.json`](https://deepswe.datacurve.ai/artifacts/trials.json) sum to
the per-cell counts. The verdicts themselves do not survive an independent
check, because there is no patch to re-grade. The `has_model_patch: true`
flag is a promise, not a link.

A benchmark that scores its subjects with verdicts whose receipts cannot be
retrieved is not falsifiable at the verdict level. The published artifacts
let me check the counting; they do not let me check whether the counting
reflects what the grader would say if I re-ran it against the published
outputs. Without that check, the artifact's claim to measure is not testable
from what it publishes.

#### The footer disagrees with the headline math

The leaderboard's headline number for `gpt-5.5 [xhigh]` is **0.70045**.
Computing that from the heatmap reproduces it exactly — with one specific
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
for `gpt-5.5` on either. Other frontier models do — `gpt-5.4` hits
`goreleaser` 4/4, `claude-opus-4.7` hits it 4/4 — so the tasks are
gradeable. `gpt-5.5`'s rollouts on those two tasks were excluded under the
documented error-exclusion policy, which is defensible. The footer's label
is not. The number announced as the denominator is 113; the number used in
the computation is 111; the math the reader gets if they apply the footer
exactly is 68.8%, not 70.0%.

A benchmark whose headline figure depends on the gap between its footer's
denominator and its actual denominator is publishing two different versions
of its own central number.

#### The grader's verdicts disagree with an independent re-run

The four reference-solution failures from the audit above appear on the
leaderboard's per-task heatmap. Three of them pass cleanly under `gpt-5.5`:

| task | gpt-5.5 | claude-opus-4.7 | gemini-3.5-flash | total across 16 models |
|---|---|---|---|---|
| [langchain-request-coalescing](https://deepswe.datacurve.ai/data/tasks/langchain-request-coalescing) | 3/4 | 0/4 | 0/4 | 10/64 |
| [narwhals-rolling-window-suite](https://deepswe.datacurve.ai/data/tasks/narwhals-rolling-window-suite) | 4/4 | 3/4 | 0/4 | 34/64 |
| [prometheus-transactional-reload-status](https://deepswe.datacurve.ai/data/tasks/prometheus-transactional-reload-status) | 0/4 | 0/4 | 0/4 | 2/64 |
| [skrub-duration-encoding](https://deepswe.datacurve.ai/data/tasks/skrub-duration-encoding) | 4/4 | 4/4 | 0/4 | 12/64 |

My oracle audit, run at the pinned commit, found these four golds failing
their own verifier in two consecutive isolated runs. The leaderboard's
heatmap shows three of them passing routinely under `gpt-5.5`. The
candidates for the disagreement are pinned-image drift between my pier and
theirs, isolation flake on tasks the leaderboard gives four shots at, or
the grader returning different verdicts on the same nominal pipeline. The
public data does not pick between the three. The narrow claim from the
original audit — a gold failing its own verifier in two consecutive isolated
runs is untrustworthy until diagnosed — holds against all three readings.

A benchmark whose grader disagrees with an independent re-run on its own
pinned pipeline, and whose authors have not investigated the disagreement
in the months since publication, is exposing an unresolved consistency
problem in its scoring function.

### The dossier

Three problems with the content. Each one would, on its own, prompt an
editor query at a peer-reviewed venue. None of them are subtle. The
question the dossier answers is why the content has these specific
properties — why an artifact that, as the press cycle has it, took
[Datacurve](https://datacurve.ai/) months to build and ship was reviewed
to a state with three plain failures still in it.

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
at Cohere on synthetic-data work; Charley interned at Google on multi-modal
RL. [Leonard Tng](https://leonardtng.com/) is an engineer with an
undergraduate background from Yale-NUS College. Wenqi Huang is the fourth
author; multiple unrelated profiles share that name and the LinkedIn for
the Datacurve Wenqi Huang was not unambiguously surfaced.

What they have published before DeepSWE, by name, across the venues where
benchmarking and evaluation methodology is publicly discussed:

| Venue | Result |
|---|---|
| [arXiv](https://arxiv.org) | none |
| [Zenodo](https://zenodo.org) | none |
| [Hugging Face Papers](https://huggingface.co/papers) | none |
| [Semantic Scholar](https://www.semanticscholar.org/) | none |
| [OpenReview](https://openreview.net) | none |
| [Google Scholar](https://scholar.google.com/) | none |
| [ResearchGate](https://www.researchgate.net/) | none |
| `datacurve.ai/` company blog | no blog exists |
| Substack (any author) | none under their names |
| Medium (any author) | none containing technical writing on benchmarks/evaluation |
| Personal sites | [`leonardtng.com`](https://leonardtng.com/); no methodology writing |
| Twitter/X | [`@serenaa_ge`](https://x.com/serenaa_ge); company and personal updates only |

DeepSWE is the four authors' first and only public technical artifact on
benchmarking or evaluation. None of them has, to my searching, written
publicly about how a benchmark should be designed, what a reproducible
verdict requires, what a contamination check should look like, or what
denominator hygiene looks like. The methodology that DeepSWE applies has no
prior version any of the authors has staked a position on. The artifact is
the position.

A reader who would otherwise extend the trust an audience extends to
domain professionals — researchers with a record of writing about their
methodology before applying it — has no record here to extend trust
against. Trust would have to be extended to the artifact alone. The
artifact, on the review above, does not earn it.

#### What the artifact's review surface optimized for

The leaderboard was built by the company that
[sells](https://www.ycombinator.com/companies/datacurve) frontier coding
training data to the foundation model labs whose models the leaderboard
scores. The
[$15M Series A](https://techcrunch.com/2025/10/09/datacurve-raises-15-million-to-take-on-scaleai/)
was led by Mark Goldberg at Chemistry, with participation explicitly named
as "employees at DeepMind, Vercel, Anthropic, and OpenAI." The seed round
was led by Balaji Srinivasan. [YC](https://www.ycombinator.com/companies/datacurve)'s
W24 partner Garry Tan is the YC-side relationship.

The leaderboard's top result is **OpenAI's gpt-5.5 at 70%**, sixteen
percentage points ahead of the next model.

None of those facts alone is a conflict of interest. The combination is the
condition a peer-reviewed venue would require to be disclosed, in the
section that begins "Conflicts of Interest." There is no such section on
[the leaderboard's blog post](https://deepswe.datacurve.ai/blog). The
artifact contains no statement that its top result is the flagship product
of a company whose individual employees are on the producing company's cap
table and whose corporate entity is, by the producing company's business
model, a customer or potential customer.

The review surface the artifact was held to before publication was the
review surface a YC-stage startup uses for a marketing release: the team
itself, the YC partner, the lead investor, the press contacts. Those
reviewers optimize for outcomes the artifact is succeeding at — favorable
[VentureBeat](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole)
coverage, [TechCrunch](https://techcrunch.com/2025/10/09/datacurve-raises-15-million-to-take-on-scaleai/)
coverage, customer adoption, the next round. On those metrics the artifact
has worked. The Series A closed. The press cycle was friendly. The
customer base is the same set of frontier model labs whose models the
benchmark scores.

The reviewers a peer-reviewed venue would have provided — methodologists
whose own reputation depends on catching denominator slips, identity-check
failures, and conflict-disclosure gaps — were not in the room. The
artifact's failures in the audit section above are the kind a domain
methodologist would have surfaced on first read. None of those people had
standing here.

There was no scientist in the room to call them out.

### The five-minute audit

The work in the audit section above is not subtle. The patches gap is
visible in any per-trial JSON. The denominator gap is visible by computing
one mean against two divisors. The verifier disagreement is visible by
running one shell loop against the pinned commit. None of those require
expertise that a careful reader with an agent doesn't have. To show that,
I ran the artifact through `codex exec -m gpt-5.5` with the following
five-line prompt:

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

Five lines. No mention of the three findings above. No priming on
patches, denominators, conflicts of interest, or any specific defect.
Just "audit it skeptically, here are the artifacts, cite specifics."

Codex spent about four minutes, ran its own curls against the public
endpoints, and produced ten numbered findings with citations. Three of
them reproduce the audit above: it independently identified the
denominator gap, the two specific tasks the top model drops, and the
`has_model_patch: true` flag whose link is not delivered. Six of them
are additional methodological catches the audit above does not contain:
uneven exclusion counts across models that may bias rankings, Wilson
confidence intervals computed over clustered trials as if they were
independent, a `pass_rate` field whose definition diverges from the
naïve interpretation, missing prompts and verifier commands in
`tasks.json` that prevent reproduction of scoring, mixed-length and
short `base_commit_hash` values that weaken reproducibility, and
non-normalized `reasoning_effort` across model configurations that
collapses model and harness into a single ranking.

The full transcript, including codex's tool calls and final summary, is
[in the audit repo](https://github.com/kimjune01/deepswe-run/tree/main/external/codex-audit).
[The prompt is there too](https://github.com/kimjune01/deepswe-run/blob/main/external/codex-audit/prompt.txt).
Total cost: a few dollars in `gpt-5.5` tokens.

Anything in this post that codex caught, you can catch by running the
prompt at your own agent. Anything codex caught that this post does not
contain — six issues — is also one prompt away from your reading. The
artifact has been live, cited in
[VentureBeat](https://venturebeat.com/technology/deepswe-blows-up-the-ai-coding-leaderboard-crowns-gpt-5-5-and-finds-claude-opus-exploiting-a-benchmark-loophole),
quoted as authoritative across the AI press cycle, and treated as
evidence in arguments about model capability since May 2026. The work
to surface it as content with this many problems has been one
single-paragraph prompt away for the entire interval.

The audit's claim — that this is not science — is not only about the
artifact and its producers. The artifact's reception is the other half
of why an artifact with these properties succeeded. Vibe coders are
easily fooled by clever marketing. Press reporters who do not read
their primary sources critically pass the marketing through. Readers
who treat a screenshot of a chart on a company subdomain as a measurement
instrument do the rest. The audit catches the artifact's failures; the
reception was the part that let those failures not matter.

Run the prompt at your own agent. The artifact's verdicts are not
falsifiable from what it publishes. The denominator on its central
number disagrees with its own footer. Its grader disagrees with an
independent re-run on the same nominal pipeline. The team that
produced it has, between them, no prior public technical artifact on
benchmarking or evaluation. Its top result is the flagship of a
company whose individual employees are on the producing company's
cap table. None of those are conclusions you have to take on my
authority; they are conclusions an agent will read off the public
artifacts the moment you ask it to.

This is the kind of work tools shaped like
[june.kim/new-reading](https://june.kim/new-reading) are going to make
routine. The printing press for skeptical readers is only getting
greased up. The next benchmark released to the same audience, on the
same surface, with the same review structure, gets audited in five
minutes by every reader who runs the prompt before quoting the
headline. That is the actual fence around marketing artifacts in this
field — not peer review, not citation politics, not professional
society norms, none of which were ever going to apply here. Just every
reader running the prompt before reading the headline.

## Attestation and reproducibility

The point of this post is not to be trusted. It is to be checked. So here is everything needed to
re-derive the quantitative claims above. The benchmark publishes the harness and the data. What
it did not publish is the gold-passes-verifier pre-ship check, and the per-task run artifacts
behind the leaderboard. Those are below.

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
