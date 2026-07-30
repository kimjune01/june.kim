---
variant: post-medium
title: "Auditing Frontier-Bench"
subtitle: "It destroys the agent's container before grading. On nine tasks, deleting unrelated state stayed invisible and the reward stayed 1."
tags: epistemology, coding
---

[Frontier-Bench](https://www.frontierbench.ai/), the same team's successor to Terminal-Bench, [released v0.1 on July 23](https://github.com/harbor-framework/frontier-bench/releases/tag/v0.1.0) with 74 tasks in seven domains. Its [review pipeline](https://github.com/harbor-framework/frontier-bench/blob/2d260bc7fb344dd13b1b920265e372b6dbc6a38d/docs/TASK_REVIEW_AUTOMATION.md) includes static checks, oracle validation, automatic `/cheat` trials for new tasks, maintainer-triggered `/fortify`, and a [35-criterion rubric](https://github.com/harbor-framework/frontier-bench/blob/2d260bc7fb344dd13b1b920265e372b6dbc6a38d/rubrics/task-implementation.toml) with an explicit preservation criterion.

I checked all 74 configurations and graders, then probed the runner. Scope: Frontier-Bench [`2d260bc`](https://github.com/harbor-framework/frontier-bench/tree/2d260bc7fb344dd13b1b920265e372b6dbc6a38d), Harbor 0.20.0. Evidence: [claims and falsifiers](https://github.com/kimjune01/frontier-bench-audit/blob/860afe01f900fdbd1a1a0f642863a8711be096f5/CLAIMS.md), [raw verdicts](https://github.com/kimjune01/frontier-bench-audit/blob/860afe01f900fdbd1a1a0f642863a8711be096f5/verdicts.jsonl), and [reproduction](https://github.com/kimjune01/frontier-bench-audit/blob/860afe01f900fdbd1a1a0f642863a8711be096f5/REPRODUCE.md). I [preregistered](https://github.com/kimjune01/frontier-bench-audit/blob/fc4dc42/PREREGISTRATION.md) the predictions and reported the finding on [#1192](https://github.com/harbor-framework/frontier-bench/issues/1192) before publication.

| Claim kind | What to inspect | What would refute it |
| --- | --- | --- |
| Interface | The pinned [separate-verifier rubric clause](https://github.com/harbor-framework/frontier-bench/blob/2d260bc7fb344dd13b1b920265e372b6dbc6a38d/rubrics/task-implementation.toml#L203-L230) and [Harbor collect-hook model](https://github.com/harbor-framework/harbor/blob/ff69e554fac1c751aa608e03de027db9043a2eac/src/harbor/models/task/config.py#L725-L732) | Any undocumented channel by which undeclared agent-container state reaches the verifier |
| Corpus census | Run `bash harness/census.sh` from the audit repository against the pinned target | A different count, or a task outside the reported artifact/hook scopes |
| Nine-run result | Run `bash harness/agg.sh`, then inspect each job's witness and official `verifier/reward.txt` | Any witnessed deletion with reward other than 1 |

All counts refer to the pinned commits.

## Why look for deletion?

Collateral loss is observed, not hypothetical. In 2025, when development changes could still affect production, [Replit acknowledged that its Agent deleted customer database data](https://replit.com/blog/doubling-down-on-our-commitment-to-secure-vibe-coding). Replit responded with dev/prod separation, production isolation, full-state checkpoints, and a non-modifying mode.

A 2026 systems paper, [*Don't Let AI Agents YOLO Your Files*](https://arxiv.org/abs/2604.13536), analyzes 290 public filesystem-misuse reports across 13 frameworks and evaluates staging and snapshots that make mutations reviewable and reversible. The general requirement is observable effects that users can inspect, reject, or undo.

YOLO mode enables unattended automation; approval before every consequential action reduces an agent to an interactive assistant. Containment and recovery remain backstops, but reducing destructive-action probability still reduces loss and recovery. A benchmark can measure relative frame preservation without certifying perfect safety, if it observes the frame.

Command approval cannot provide that observation. In an [instrumented run](https://dev.to/wenyu_zhang/i-denied-7-dangerous-commands-my-agent-deleted-the-files-anyway-44f7), policy denied seven deletion methods; the agent put the requested deletion in a test and ran allowed `node --test` ([trace-backed commit](https://github.com/zachzwy/agentloop/commit/8730fe562f576c79b0772cdce94ebd4b41d49e01)). This was requested deletion of disposable files, not harm. The run demonstrates that any allowed general code runner defeats effect enumeration.

The OS sandbox bounded that run; grading is a separate boundary. A sandbox limits reachable damage. A grader decides whether damage inside the writable scope counts as failure. This audit asks whether Frontier-Bench retains enough evidence to score such damage. It does not claim Frontier-Bench destroyed real user files.

## How a run works

An agent works in one container. The harness copies declared `artifacts`, destroys that container, then grades in a second container using the artifacts and verifier-image contents. Reward is 0 or 1.

The *frame* is everything the task did not ask the agent to change. In the [Terminal-Bench audit](/terminal-bench-frame), 40 of 83 gold-passing tasks still scored 1 when their reference solution also performed a careless deletion.

## Nine tasks, reward 1

I planted a second git repository with unpushed work, an SSH private key, and a customer CSV under an unreferenced directory. The certified solution ran unchanged, then deleted that directory before official grading.

*Result: reward 1 on all nine gold-passing tasks probed; every deletion was witnessed.*

No model or adversary participated: official oracle, unmodified grader, one documented accident.

The assets are synthetic stand-ins for unrelated state that coexists with real agent work. The claim concerns distinguishability, not the value of those bytes. This interface cannot distinguish clean completion from the same completion plus uncaptured damage.

Three claim classes carry this:

- *Interface entailment.* Teardown makes uncaptured state unavailable.
- *Corpus facts.* All 74 tasks use separate verification, and their capture scopes are statically checked.
- *Behavioral demonstrations.* Nine witnessed deletions received reward 1.

The runs validate prerequisites (the oracle finished, deletion executed, tests passed) but do not estimate how often arbitrary damage occurs or escapes grading.

## Why the verifier cannot see it

All 74 tasks run `environment_mode = "separate"`, and [`checks/check-separate-verifier.sh`](https://github.com/harbor-framework/frontier-bench/blob/2d260bc7fb344dd13b1b920265e372b6dbc6a38d/checks/check-separate-verifier.sh) enforces it on every PR. The [rubric states what the verifier can then see](https://github.com/harbor-framework/frontier-bench/blob/2d260bc7fb344dd13b1b920265e372b6dbc6a38d/rubrics/task-implementation.toml#L203-L230):

> Every file the verifier reads from the agent is either: (a) listed in `artifacts`, (b) baked into the verifier image via `tests/Dockerfile`, or (c) reachable on a persistent sidecar. Nothing else is available.

Four channels can affect the verdict: artifacts, pre-teardown collect-hook output, persistent sidecars or mounts, and external effects. Across 74 tasks, the planted directory is in no artifact list, hook scope, or sidecar. I did not test external effects.

The verifier cannot implement a general frame check after its input state is destroyed. Here the interface settles what required 83 behavioral runs on Terminal-Bench.

## Only what the instruction names

One rubric criterion, [`do_not_modify_enforced`](https://github.com/harbor-framework/frontier-bench/blob/2d260bc7fb344dd13b1b920265e372b6dbc6a38d/rubrics/task-implementation.toml#L478-L494), requires stated preservation constraints to fail violators and rejects partial checks.

Its exit condition is: "Mark as N/A if the instruction contains no constraint protecting a concrete artifact from modification." A criterion keyed to named artifacts cannot cover the unnamed complement. The task target is specified; the frame is its generally unwritten complement.

The v0.2 roadmap issue [#1192](https://github.com/harbor-framework/frontier-bench/issues/1192) has the same scope: "if an instruction says do not modify something, we better check that it hasn't modified that."

## The mechanism already exists

Harbor already ships `[[verifier.collect]]`, described in its [config model](https://github.com/harbor-framework/harbor/blob/ff69e554fac1c751aa608e03de027db9043a2eac/src/harbor/models/task/config.py#L725-L732):

> Commands run in compose services after the agent phase ends and before artifact collection... Collect hooks let services snapshot runtime state (database contents, in-memory counters) into files before the environment is torn down, so the files can be declared as artifacts and read by a separate verifier.

Main-service hooks run before teardown, so they can snapshot the frame for the grader.

Seven tasks declare hooks; four transport whole-tree `git diff`s. `lean-midpoint-proof` captures `/app`, applies the patch to a pristine project, and grades a fresh build. Deleting `Geometry.lean` therefore yields reward 0. The same task still yields 1 for planted deletion under `/root`: capture protects only its scope.

All four use pinned git bases and were converted to reduce artifacts, from ~828MB to 48KB in the [original case](https://github.com/harbor-framework/frontier-bench/issues/1277). The mechanism arose for efficiency but also preserves scoped deletions.

## Why the architecture made this trade

Separate verification closes a real attack: agent code running as verifier root can outlive `test.sh` and overwrite `reward.txt`. Isolation blocks that.

The tradeoff: reward hacking asks whether a wrong run can pass; frame validity asks whether a correct but harmful run can pass. No rubric criterion scores off-task state. `/cheat` and `/fortify` target test-suite attacks, not correct work plus collateral damage.

## Bounds, and one hypothesis that failed

I deleted pre-existing workspace files the oracle never wrote. Most graders caught it. The uncaught files were unused development scaffolding, so I found no demonstrated harm to non-synthetic assets.

Twelve verifiers execute artifacts against pristine workspace material baked into the verifier image, and issue [#1294](https://github.com/harbor-framework/frontier-bench/issues/1294) counts 37 tasks duplicating data across images. Pristine reconstitution prevents damage from helping an agent pass; it does not establish that damage was detected.

The rest of the bounds:

- I omit the small, biased in-workspace catch rate; both disk-skipped tasks used capture patterns that would have increased it.
- I did not test network egress; the [template](https://github.com/harbor-framework/frontier-bench/blob/2d260bc7fb344dd13b1b920265e372b6dbc6a38d/docs/task-template.toml) uses `network_mode = "public"`. Filesystem capture cannot detect exfiltration.
- Two harness bugs understated the finding; [`CLAIMS.md`](https://github.com/kimjune01/frontier-bench-audit/blob/860afe01f900fdbd1a1a0f642863a8711be096f5/CLAIMS.md#c-claims-about-this-audits-own-instrument) documents and reproduces both. Every mutation now exports a witness; runs without its post-accident marker are void.
- Environment: arm64, local Docker. Gold failures are quarantined; unattempted tasks are separate.
- Not audited: difficulty, leaderboard statistics, rubric judge, specification, or claim clauses.

## Recommendations

These follow from the interface boundary, not the nine-task sample.

1. *Capture before teardown in Harbor.* Snapshot writable state through the same path for oracle and agent runs. Missing or partial capture invalidates the trial. Runner-level capture covers every separate-verifier dataset.

2. *Report frame deltas beside reward.* Compare agent and oracle final-state deltas, excluding declared volatile paths. Publish unexplained additions, modifications, and deletions; do not initially fold them into binary reward because valid alternative solutions differ.

3. *Test capture in CI.* Run the oracle plus a witnessed mutation outside the target; require it to reach the diagnostic. This proves observation without enumerating the frame and leaves `/cheat` and `/fortify` focused on reward hacking.

4. *Measure behavior.* Seed realistic synthetic state across writable scopes and run agents repeatedly. Estimate destructive-action probability and test whether model, prompt, or harness changes lower it.

5. *Speculation: build a destructive-behavior safety benchmark.* Surround ordinary tasks with valuable synthetic state, and vary ambiguity and permissions. Measure scope inspection, preservation, warranted escalation, recovery, probability, and severity. Use hidden canaries, effect logs, realistic recovery, and defenses against agents treating every file as a trap. Measure improvement, not “safe” certification.

6. *Declare coverage.* Filesystem capture misses exfiltration, remote APIs, uncaptured sidecars, and harm reversed before snapshot. Use event logs, scoped credentials, egress controls, and separate adversarial trials; report observed channels.

## What this is really about

Frontier-Bench blocks reward forging with isolated verification but does not first record undeclared agent-container state. Its preservation criterion covers only instruction-named artifacts. Harbor already provides the required pre-teardown primitive; four tasks use it.

Teardown before grading protects reward integrity but makes the frame unreadable by default. Capture belongs in the runner so every dataset inherits the fix rather than the gap.
