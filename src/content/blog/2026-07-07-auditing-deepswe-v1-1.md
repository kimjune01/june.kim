---
variant: post-wide
title: "Auditing DeepSWE v1.1"
tags: coding, methodology, epistemology, reflecting
---

*A follow-up to [Auditing DeepSWE](/auditing-deepswe). Published 2026-07-07.*

In May I audited [DeepSWE](https://github.com/datacurve-ai/deep-swe), a contamination-free
coding benchmark, and found four of its 113 reference solutions failing their own
verifiers: `langchain-request-coalescing`, `narwhals-rolling-window-suite`,
`prometheus-transactional-reload-status`, and `skrub-duration-encoding`. A gold that
cannot pass the test built for it cannot be trusted until the contradiction is resolved.
[The audit](/auditing-deepswe) left the diagnosis to the maintainers, where it belonged.

On June 14, 2026, they shipped [DeepSWE v1.1](https://deepswe.datacurve.ai/blog/deepswe-v1-1),
a re-graded revision. Credit where it lands: the release closes most of the technical gaps
that audit opened, and it closes them at the mechanism rather than with a caveat. v1 is now
marked frozen; v1.1 is the live leaderboard.

The scoring changed. v1 graded on the test process's exit code; v1.1 grades specific
test node IDs, splitting fail-to-pass from pass-to-pass, and runs the committed code
in a clean isolated environment. The maintainers' own note says they "fixed dependency
drift and removed flaky tests on some tasks." That is the diagnosis the audit left to
them, carried out.

The four golds are the tell. The published
[v1&#8596;v1.1 delta](https://deepswe.datacurve.ai/artifacts/v1.1/v1-delta.json) leaves the
pooled pass rate almost flat (0.509 &#8594; 0.518) while all four flagged tasks climb:

<div class="table-wrap">
<table style="max-width:720px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:18em"><col><col><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">task</th><th style="background:#f0f0f0">v1 (exit-code)</th><th style="background:#f0f0f0">v1.1 (node-id)</th><th style="background:#f0f0f0">&#916;</th><th style="background:#f0f0f0">attempts (v1&#8594;v1.1)</th></tr></thead>
<tr><td><code>narwhals-rolling-window-suite</code></td><td style="white-space:nowrap">30%</td><td style="white-space:nowrap">95%</td><td style="white-space:nowrap">+65</td><td style="white-space:nowrap">40&#8594;40</td></tr>
<tr><td><code>skrub-duration-encoding</code></td><td style="white-space:nowrap">22%</td><td style="white-space:nowrap">60%</td><td style="white-space:nowrap">+38</td><td style="white-space:nowrap">49&#8594;40</td></tr>
<tr><td><code>langchain-request-coalescing</code></td><td style="white-space:nowrap">14%</td><td style="white-space:nowrap">28%</td><td style="white-space:nowrap">+13</td><td style="white-space:nowrap">49&#8594;40</td></tr>
<tr><td><code>prometheus-transactional-reload-status</code></td><td style="white-space:nowrap">2.5%</td><td style="white-space:nowrap">12.5%</td><td style="white-space:nowrap">+10</td><td style="white-space:nowrap">40&#8594;40</td></tr>
</table>
</div>

Read the two with an unchanged attempt count first. `narwhals` and `prometheus` are
graded over the same 40 rollouts in both versions, so the grader is the only thing that
moved, and they still climb +65 and +10. `langchain` and `skrub` also shed attempts
(49 to 40), so read those two as directional. Either way, a re-grade that lifts the
flagged tasks by 10 to 65 points while holding the aggregate within a point of itself
was mis-scoring correct solutions on exactly those tasks. The audit's narrow claim, that
a gold failing its own verifier is untrustworthy until diagnosed, resolved the way a real
defect resolves for three of the four. An independent gold rerun (see the ledger below)
confirms `langchain`, `narwhals`, and `skrub` now pass their own verifiers, while
`prometheus`'s reference solution still fails, breaking 10 of its 82 pass-to-pass tests.

The statistics improved on two fronts. The confidence intervals were the weakest numbers
in v1: Wilson intervals over clustered attempts treated as independent, off a single run.
v1.1 reports run-to-run variance across repeated whole-benchmark passes
(`ci_method: "95% run-to-run: SE across repeated whole-benchmark passes"`), the variance
the "one run, no error bars" critique asked for. And the leaderboard now carries a
per-config attempted count instead of a fixed 113 divisor, so the denominator drift is
visible in the data rather than masked by a false footer, though not gone: one config is
still scored over 111 of the 113 tasks. Wall-clock time, unreliable across providers, was
dropped.

Run the same five-minute check on the new release. Pointed at the v1.1
artifacts, the same skeptical [codex](https://github.com/openai/codex) prompt the original
audit used still surfaces disclosure and consistency defects the grading fix left
untouched. [`heatmap.json`](https://deepswe.datacurve.ai/artifacts/v1.1/heatmap.json)
charts 8 models where the leaderboard ranks 10, dropping `claude-sonnet-5` and `glm-5-2`
from the grid without a note. The stated rule that agent timeouts score as failures is
contradicted by trial rows carrying `error_category: "agent_timeout"` next to
`passed: true` and reward 1. The blog accounts for 73 Fable rollouts lost to a provider
suspension but not the other 49 excluded trials in
[`trials.json`](https://deepswe.datacurve.ai/artifacts/v1.1/trials.json). And node-id
scoring is not checkable from what ships: each trial names its `ctrf.json` and `reward.json`
without publishing their contents, and `has_model_patch` stays a boolean with no link behind
it, so a reader still cannot re-derive a single verdict.

What v1.1 does not touch is the part that was never a grading bug. The
public-reproducibility-versus-contamination tradeoff is structural and unchanged: a
re-grade does not extend the contamination-free half-life. And the release adds no
conflicts-of-interest statement. The scoring debt is paid; the disclosure debt is not.

One more dimension, and it comes out clean. I pointed my
[determinacy auditor](https://github.com/kimjune01/determinacy) at all 113 tasks, the same
tool that put a proven 15% underdetermination floor on SWE-bench Pro. A determinacy defect is
the inverse of a broken grader: the test is fine, but the spec does not pin the behavior it
grades, so a correct-but-different fix scores zero. It is the one class of defect the node-id
re-grade cannot touch. The adjudicated floor is 3 of 111 tasks, about 2.7%: one where the test
demands the exact string `currentcolor` while the codebase spells it `currentColor`, and two
where the repo itself makes the graded choice two conflicting ways. Each is one clone-and-grep
to check. That is several times tighter than Pro's mined-PR tasks, and it is to the authors'
credit. Writing 113 specs precise enough that an adversarial audit finds almost nothing
underdetermined is hard, and they did it.

Two honest notes on that number. This is a census of all 113, so there is no
confidence interval to report: the count is exact, a lower bound that only grows with more
search. And the audit turned up a bug in my own tool, which was certifying underdetermination
on test-fixture strings rather than free authorial constants. Two of five raw candidates were
fixture echoes; I fixed the tool, re-ran, and kept only what survives an independent grep. The
receipts, the adjudication, and the fix are in the
[audit repo](https://github.com/kimjune01/deepswe-run/tree/main/results/determinacy).

The ledger, at a glance. Each status was checked against the v1.1 artifacts this week, and I
ran an independent gold-passes-verifier rerun on native amd64: 112 of the 113 golds pass their
own verifier under v1.1. The receipts are in the
[audit repo](https://github.com/kimjune01/deepswe-run/tree/main/results/v1.1).

<div class="table-wrap">
<table style="max-width:100%; margin:1em auto; font-size:14px;">
<colgroup><col style="width:22em"><col style="width:6em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">v1 finding</th><th style="background:#f0f0f0">v1.1</th><th style="background:#f0f0f0">what changed</th></tr></thead>
<tbody>
<tr><td colspan="3" style="background:#e8e8e8; font-weight:600">Grading, statistics, comparability</td></tr>
<tr><td>Four reference golds fail their own verifiers</td><td style="color:#9a6700; white-space:nowrap">◑ 3 of 4</td><td>My v1.1 oracle rerun: <code>langchain</code>, <code>narwhals</code>, <code>skrub</code> golds now pass; <code>prometheus</code> still fails (10 pass-to-pass regressions). No new broken golds: 4/113 &#8594; 1/113</td></tr>
<tr><td>Grader disagrees with an independent re-run</td><td style="color:#0a7d33; white-space:nowrap">✓ fixed</td><td>Same re-grade; the disagreement was the coarse exit-code scoring</td></tr>
<tr><td>Confidence intervals treat clustered trials as independent, off one run</td><td style="color:#0a7d33; white-space:nowrap">✓ fixed</td><td>Run-to-run variance across repeated whole-benchmark passes</td></tr>
<tr><td>Wall-clock reported as a metric</td><td style="color:#0a7d33; white-space:nowrap">✓ fixed</td><td>No longer reported on the board; the <code>duration_seconds</code> fields remain in the data</td></tr>
<tr><td>Footer denominator (113) disagrees with the math (111)</td><td style="color:#9a6700; white-space:nowrap">◑ partly</td><td>Per-config counts now published and self-consistent; the global footer still reads 113 while one config ran 111</td></tr>
<tr><td>"Lighter harness matches or beats" rests on 10 tasks, one run</td><td style="color:#9a6700; white-space:nowrap">◑ partly</td><td>Repeated passes add variance; the native-vs-mini ablation itself is not re-run</td></tr>
<tr><td><code>reasoning_effort</code> not normalized across models</td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td>Still mixed (<code>null</code> to <code>xhigh</code>); the board ranks model-and-effort pairs</td></tr>
<tr><td colspan="3" style="background:#e8e8e8; font-weight:600">Disclosure and reproducibility</td></tr>
<tr><td>Verdict receipts not retrievable (<code>has_model_patch</code> a flag, not a link)</td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td>Still a boolean; <code>ctrf.json</code>/<code>reward.json</code> contents unshipped, so no verdict re-derives</td></tr>
<tr><td><code>tasks.json</code> too thin to audit scoring</td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td>Still no full prompt, hidden tests, or node IDs</td></tr>
<tr><td>Exclusions uneven and only partly disclosed</td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td>122 trials excluded, 73 disclosed; the other 49 unmentioned</td></tr>
<tr><td>Short / malformed <code>base_commit</code> hashes</td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td>Unchanged: two 7-char SHAs, one 39-char string</td></tr>
<tr><td>No conflicts-of-interest statement</td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td>None added; the producing entity sells to the labs it ranks</td></tr>
<tr><td colspan="3" style="background:#e8e8e8; font-weight:600">Structural and context</td></tr>
<tr><td>Public reproducibility vs contamination half-life</td><td style="color:#666; white-space:nowrap">— inherent</td><td>A re-grade cannot extend the contamination-free window</td></tr>
<tr><td>Spec determinacy (are the tasks underspecified?)</td><td style="color:#0a7d33; white-space:nowrap">✓ clear</td><td>Independent audit finds a ~2.7% floor; the specs are tight</td></tr>
<tr><td colspan="3" style="background:#e8e8e8; font-weight:600">New in v1.1, open</td></tr>
<tr><td>Heatmap charts 8 of 10 ranked models</td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td><code>claude-sonnet-5</code> and <code>glm-5-2</code> dropped from the grid</td></tr>
<tr><td>Trials scored <code>pass</code> while flagged <code>agent_timeout</code></td><td style="color:#b3261e; white-space:nowrap">✗ open</td><td>The documented timeout rule is contradicted by the data</td></tr>
</tbody>
</table>
</div>

The through-line holds in both directions, and it is not a story about bad work. The
engineering is strong: the grading debt closed fast once it was named with receipts, and the
specs were tight from the start. The skill is all there. Only the disclosure is missing. The self-audit
habit did not arrive with the fix, which is why the same five-minute pass still finds work, and
the conflicts the bench owes its readers cost nothing to state and remain unwritten.

A tight to-do list, keystone first, closes what remains. None of it is exotic; each ask is
already a norm somewhere.

1. Ship a reproducible verdict bundle. Per trial, publish the model patch, the `ctrf.json`
   report, and the reward, plus a manifest pinning the task repo commit, verifier image digest,
   node IDs, scoring script, and timeout and exclusion policy. The patch and report let a reader
   inspect a verdict; the manifest is what lets a third party re-run it. This costs almost
   nothing, because the harness already writes these files on every run: grading these tasks
   myself, Pier emitted `model.patch`, `ctrf.json`, and `reward.json` per trial unprompted.
   Publishing them uploads artifacts that already exist; no new instrumentation is needed. It is
   also the ecosystem norm DeepSWE departed from:
   [SWE-bench's experiments repo](https://github.com/SWE-bench/experiments) ships per-instance
   `patch.diff`, `report.json`, and `test_output.txt` in a public bucket, and
   [MLPerf](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)
   rules that a result which cannot be replicated is not valid.
2. Disclose every excluded trial, with reasons: 122 were excluded, the blog names 73. Trial
   reporting settled this long ago. [CONSORT](https://jamanetwork.com/journals/jama/fullarticle/2832868)
   requires reporting losses and exclusions with reasons; the
   [NeurIPS checklist](https://neurips.cc/Conferences/2021/PaperInformation/PaperChecklist) asks
   which subset reproduces. The data is already logged, so this is cheap.
3. Add one conflicts-of-interest sentence: the producing entity sells training data to the labs
   whose models top the board. [ICML 2026](https://icml.cc/Conferences/2026/AuthorInstructions)
   states plainly that evaluating a model from the authors' employer must be disclosed;
   [ICMJE](https://www.icmje.org/disclosure-of-interest/) ties public trust to it. It costs a
   sentence and breaks no comparability.
4. Publish the full task materials in `tasks.json`: the prompt, the hidden tests, and the node
   IDs, so a reader can see what was graded.
5. Fix the scoring contradiction first, then the hygiene. Trial rows flagged `agent_timeout` are
   scored as passes, which contradicts the stated rule: a real scoring bug, and it outranks the
   cosmetic fixes that follow. Then the full 40-character `base_commit` SHAs, a same-effort
   comparison, the heatmap's two missing models, and the footer's 113 that is really 111.

*Receipts.* The v1.1 artifact snapshots, a per-claim re-derivation, and the full codex
transcript are in the audit repo at
[github.com/kimjune01/deepswe-run](https://github.com/kimjune01/deepswe-run/tree/main/results/v1.1).
Take the snapshots, re-run the commands, and check me.
