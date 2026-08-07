---
variant: post-medium
title: "τ²-bench Doesn't Check the Rules"
subtitle: "It exists to test whether agents follow domain policy. The domain with its own leaderboard scores a policy violation as success."
tags: methodology, epistemology
---

τ-bench was built because other benchmarks didn't test whether an agent follows the rules. Its [paper](https://arxiv.org/abs/2406.12045) says so in the abstract: existing benchmarks "do not test language agents on their interaction with human users or ability to follow domain-specific rules, both of which are vital for deploying them in real world applications." The fix was a customer-service simulation where each domain ships a written policy, a set of tools, and an evaluation that "compares the database state at the end of a conversation with the annotated goal state." [τ²-bench](https://github.com/sierra-research/tau2-bench) inherits the domains, the policy files, and the claim.

In the telecom domain, neither part of that claim holds. No telecom task compares database state, and nothing anywhere checks the policy. I ran the shipped reference solution for three telecom tasks and appended one tool call that suspends an uninvolved customer's phone line for a reason the policy forbids. The official grader returned 1.0 every time. Telecom carries [its own leaderboard](https://artificialanalysis.ai/evaluations/tau2-bench), where the top scores run above 99%.

Each run executes through the benchmark environment and is scored by [`evaluate_simulation`](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/evaluator/evaluator.py#L88), the same top-level evaluator a real run goes through. No reward record was edited by hand. And [`suspend_line`](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/domains/telecom/tools.py#L261-L262) is one of the tools the telecom agent is given, so an evaluated agent could emit the identical call.

The [receipts are here](https://github.com/kimjune01/tau2-frame-audit), against commit `e5e51b3`. No model, no API key, three commands, about a minute. Every claim below links to the line of τ²-bench it comes from, or to the log it was read out of.

## The rule

[Telecom's policy file](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/data/tau2/domains/telecom/main_policy.md#L119-L123) is not vague about suspension:

> A line can be suspended for the following reasons:
> - The user has an overdue bill.
> - The line's contract end date is in the past.

The repo describes this file as ["a policy that the agent must follow"](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/README.md#L44). My injected call suspends line L1001, belonging to customer C1001. That customer's bills are Paid, Issued, and Draft, and the contract runs to 2026-12-31 against a simulated present of 2025-02-25 ([printed by the probe](https://github.com/kimjune01/tau2-frame-audit/blob/main/results/telecom-sweep.log)). No overdue bill. No expired contract. The agent did it because I told it to, for a reason the policy does not list, to a customer with no involvement in the task.

Score: 1.0.

## The missing component

τ²-bench grades by components, and each task names the ones that define success in a field called `reward_basis`. Airline tasks name `DB`, which [hashes the entire database](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/evaluator/evaluator_env.py#L118-L129) and compares it against the state the reference solution produces. Any stray write flips the hash.

Telecom tasks name `ENV_ASSERTION`, and never `DB`. Not in 2253 of them, and not in the 32 that add an action check. Zero of the 2285 tasks shipped at the audited commit, [counted here](https://github.com/kimjune01/tau2-frame-audit/blob/main/results/reward-basis-census.txt).

[Six functions](https://github.com/kimjune01/tau2-frame-audit/blob/main/results/assertion-census.txt) do the seeing. Four read the simulated phone: [can it send MMS](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/domains/telecom/user_tools.py#L1143-L1147), is mobile data working, what does the speed test return, what does the status bar say. Two read one field of one record, and that record arrives as an argument: the refueling amount for [the line you hand it](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/domains/telecom/tools.py#L724-L731), the payment status of [the bill you hand it](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/domains/telecom/tools.py#L758-L770). None of the six takes an unnamed record as input, and none enumerates a table. They are not built to notice a suspension nobody mentioned. Those six grade every telecom task and nothing else does, and that sets [the frame](https://plato.stanford.edu/entries/frame-problem/). The grader sees what the task named, and the line I suspended sits outside it.

The comparison that would catch the write runs anyway. τ²-bench [computes `DBCheck`](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/evaluator/evaluator_env.py#L131) on every task in every domain. My mutated runs carry `db_match: False` in the returned reward record while the reward reads 1.0 ([log](https://github.com/kimjune01/tau2-frame-audit/blob/main/results/telecom-sweep.log)). A component-based grader [ignores every component outside the basis](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/evaluator/evaluator_env.py#L152-L157), so the code is doing what it was configured to do. But the measurement isn't the obstacle. The number is already there, unread.

## The control

On airline, where `DB` is in the basis, the same shape of injection [flips the database check from pass to fail](https://github.com/kimjune01/tau2-frame-audit/blob/main/results/airline-run.log). One `cancel_reservation` against a reservation the reference solution never touches is enough to break the hash.

That contrast lives in the component. The scripted trajectory contains no dialogue, so airline's communication component already fails and the [top-line reward is 0.0 either way](https://github.com/kimjune01/tau2-frame-audit/blob/main/results/toplevel-run.log). Producing a passing airline run would take a model, and this audit deliberately uses none.

## What I am not saying

Not that anyone's published telecom score is wrong. Not that models suspend random customers' lines during evaluation runs. I fabricated the call. What the [censuses](https://github.com/kimjune01/tau2-frame-audit/blob/main/CLAIMS.md) establish is general and structural: no telecom task's score can respond to a write to a record its own assertions never name. The three runs test that reading rather than being the evidence for it. All of that is a claim about the instrument, and it says nothing about the agents measured on it.

Nor is assertion-based grading the mistake. τ²-bench added telecom to test [dual control](https://arxiv.org/abs/2506.07982), where the agent talks a user through actions on their own phone. Success is a device state, so device-state assertions are the right instrument. [Sierra](https://sierra.ai) can fairly say telecom was built for coordination rather than rule-following.

The current repository tells the agent its domain policy is binding, and the score certifies the device without certifying the policy. The policy file still ships. Nothing checks whether the agent followed it.

## Two directions

Two open issues already work the other side of this grader. [#384](https://github.com/sierra-research/tau2-bench/issues/384) finds reward components listed with empty criteria that auto-pass, criteria written but never named in any basis, and 23 airline refusal tasks whose reward "reduces to 'DB unchanged'" because their real success criteria live in assertions no airline basis includes. [#224](https://github.com/sierra-research/tau2-bench/issues/224) finds 22 of 50 airline tasks requiring no database write. Both find inaction scoring as success: the agent does nothing, the state matches, the task passes.

This is the opposite. The agent does the task correctly and then does something extra and forbidden, and that also passes. A grader can be blind in both directions at once, and this one is.

Sierra has been responsive on the first direction, fixing two externally reported grading bugs ([#329](https://github.com/sierra-research/tau2-bench/issues/329), [#402](https://github.com/sierra-research/tau2-bench/pull/402)) in v1.0.1, then [re-grading the leaderboard and shipping a re-scoring tool](https://github.com/sierra-research/tau2-bench/releases/tag/v1.0.1). So this one is [filed too](https://github.com/sierra-research/tau2-bench/issues/459). This post is the write-up.

## The fix and its trap

The gold environment already exists at grading time; [the grader builds it](https://github.com/sierra-research/tau2-bench/blob/e5e51b3d993f393cff3bdbb96b4411036b08c185/src/tau2/evaluator/evaluator_env.py#L97-L115) to compare against. The state a correct run should produce is sitting right there, free.

The obvious move is to put `DB` back in telecom's basis. Don't. Strict equality would fail any run that reaches the right outcome by a different route. That over-strictness [zeroed banking rewards](https://github.com/sierra-research/tau2-bench/issues/329) on benign reads and forced a re-grade in v1.0.1.

A delta gate at field granularity does the job. Compare the run's database against gold's, and fail on any differing field outside the set the reference solution itself wrote. Field, not record. Scoping to records would forgive corrupting every other field on a record the reference happened to touch. That is a lot of room.

That is the same shape as the frame gate I proposed for [Harbor](https://github.com/harbor-framework/harbor/pull/2266) and [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai/issues/4461): manifest at handoff, diff at grading, gate the delta on the reference solution's own footprint. Three benchmarks, three harnesses, one missing clause.

## The general version

A benchmark's headline names a capability. Its grader rewards something. The [checklist I keep](/how-to-audit-a-benchmark) puts reading one against the other first. It costs nothing and catches the deepest sin: the number is precise about something narrower than the title.

Here the gap runs between two files in the same repository. One says the agent must follow the policy. The other decides what counts toward the score, and in telecom it omits the only component that would notice my forbidden write. Nobody had to overclaim in a press release for that to happen. A component was left out of a list, and the guarantee left with it.

The benchmark saw the violation. It recorded `db_match: False` and scored the run 1.0, because nothing told it to care.
