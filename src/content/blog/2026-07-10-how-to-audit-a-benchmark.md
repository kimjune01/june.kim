---
variant: post-medium
title: "How to Audit a Benchmark"
subtitle: "Seven audits' worth of sins, ordered by how cheaply they're caught."
tags: methodology, epistemology
---

Over the past few months I audited seven benchmarks: [SWE-bench Verified](/swebench-verified) (as a runner), [DeepSWE](/auditing-deepswe) and [its revision](/auditing-deepswe-v1-1), [SWE-bench Pro](/a-determinacy-audit-of-swebench-pro), [ProgramBench](/programbench-measures-recall), [τ-bench's contamination story](/reprice-contamination), [Terminal-Bench](/terminal-bench-frame), and [MirrorCode](https://github.com/kimjune01/mirrorcode-audit). Each one broke in a different place, and one, re-audited after its revision, mostly held. This post compresses the lenses into a checklist a stranger can run.

*Disclosure: I applied for a role at Epoch AI, which co-produced MirrorCode, one of the audits drawn on here. An interest disclosure, not a funding one; it changes none of the receipts, which is the point of check 4 below.*

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:11em"><col style="width:7em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">audit</th><th style="background:#f0f0f0">broke at</th><th style="background:#f0f0f0">finding</th></tr></thead>
<tr><td><a href="/swebench-verified">SWE-bench Verified</a>, as runner</td><td>the run itself</td><td>test-edit exploit caught; 44 unrunnable tasks scored zero</td></tr>
<tr><td><a href="/auditing-deepswe">DeepSWE</a></td><td>gold</td><td>4 of 113 answer keys fail their own verifiers</td></tr>
<tr><td><a href="/auditing-deepswe-v1-1">DeepSWE v1.1</a></td><td>mostly held</td><td>determinacy floor 2.7%; verdict receipts still unretrievable</td></tr>
<tr><td><a href="/a-determinacy-audit-of-swebench-pro">SWE-bench Pro</a></td><td>spec</td><td>proven floor of 15% underdetermined</td></tr>
<tr><td><a href="/programbench-measures-recall">ProgramBench</a></td><td>oracle</td><td>21 recall-only witnesses; 29 self-capturing goldens</td></tr>
<tr><td><a href="/reprice-contamination">τ-bench</a></td><td>decay</td><td>memorized answer passes 0% regenerated, leaked query 100%</td></tr>
<tr><td><a href="/terminal-bench-frame">Terminal-Bench</a></td><td>frame</td><td>83 of 83 pass after off-task destruction</td></tr>
<tr><td><a href="https://github.com/kimjune01/mirrorcode-audit">MirrorCode</a></td><td>claim</td><td>title sells autonomous whole-program builds; metric scores scoped reimplementation from a live oracle, 17/25 targets contaminated</td></tr>
</table>

A benchmark is a measurement instrument, and an instrument makes a contract. Above every clause sits the claim: the capability the headline advertises has to be the one the metric measures (the *claim* clause), or the number is precise about the wrong thing. The instruction pins the target (the *spec* clause). The grader checks the target (the *oracle* clause). The grader guards everything the task never named (the *frame* clause: a run that completes the task by wrecking unrelated state must not pass). The answer key passes its own test (the *gold* clause). The headline number means what the leaderboard says it means (the *score* clause). And the number survives its own publication (the *decay* clause).

Each clause can be broken, each break is a distinct sin, and each sin has a check. The checks below are ordered by cost, and the order carries the lesson: every severe defect in these seven audits surfaced before any model ran. Cost here means compute and cash; several of the free checks still cost an afternoon of reading.

<div class="table-wrap">
<table style="max-width:100%; margin:1em auto; font-size:14px;">
<colgroup><col style="width:2em"><col style="width:16em"><col style="width:5em"><col style="width:11em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">#</th><th style="background:#f0f0f0">check</th><th style="background:#f0f0f0">cost</th><th style="background:#f0f0f0">sin</th><th style="background:#f0f0f0">exemplar</th></tr></thead>
<tr><td>1</td><td>read the claim against the construct</td><td>free</td><td>claim</td><td>title sells reconstruction, metric scores recall</td></tr>
<tr><td>2</td><td>read the paper against the repo</td><td>free</td><td>wrong rulebook</td><td>a week and $1,000 on the wrong task</td></tr>
<tr><td>3</td><td>ask how tasks were selected</td><td>free</td><td>selection by failure</td><td>0% floor read as a frontier</td></tr>
<tr><td>4</td><td>recompute the headline</td><td>free</td><td>score</td><td>footer says 113, mean divides by 111</td></tr>
<tr><td>5</td><td>retrieve one receipt</td><td>free</td><td>unfalsifiable verdicts</td><td><code>has_model_patch: true</code>, every path 404</td></tr>
<tr><td>6</td><td>run the answer key</td><td>~$1</td><td>gold</td><td>4/113, 3/731, 6/89 golds fail</td></tr>
<tr><td>7</td><td>read what the assertions pin</td><td>cheap</td><td>oracle</td><td>21 recall witnesses, 29 self-capturing goldens</td></tr>
<tr><td>8</td><td>probe what pins the graded value</td><td>cheap</td><td>spec</td><td>15% proven underdetermined</td></tr>
<tr><td>9</td><td>mutate the gold and regrade</td><td>cheap</td><td>frame</td><td><code>rm -rf .git</code> still scores 1</td></tr>
<tr><td>10</td><td>ask what survives publication</td><td>reading</td><td>decay</td><td>memorized 0%, leaked query 100%</td></tr>
<tr><td>11</td><td>audit the run</td><td>varies</td><td>run</td><td>restored tests bought 46 points</td></tr>
</table>
</div>

## 1. Read the claim against the construct

Free, and it catches the deepest sin, the one every check below can pass while the benchmark still misleads: the title advertises a capability the metric does not measure. Read the headline, then read what the grader rewards, and see whether they name the same thing. [ProgramBench](/programbench-measures-recall) sold reconstruction from behavior and scored recall of published algorithms. [MirrorCode](https://github.com/kimjune01/mirrorcode-audit) sells "the largest software project AI can complete on its own" and scores scoped reimplementation from a live reference oracle, two thirds of its targets showing memorization. Neither number is miscomputed; each is precise about something narrower than the title names. That is a construct-validity gap, not a bug: the grader is sound on what it checks, and what it checks is not the claim. The tell is an equivocation you can quote, a headline in one register beside a methods section in another, and it survives the mechanical checks below because they audit the instrument, not the advertisement.

## 2. Read the paper against the repo

Free, and it catches the sin of the wrong rulebook. The scoring rules often live in the paper while the runnable code implements something looser. On SWE-bench Pro [I lost a week and about a thousand dollars](/how-not-to-run-swebench-pro) solving the wrong task because the held-out-test rule was on pages 4 through 9 of the paper and nowhere in the repo. A surprising number is a stop sign, and the first thing to check when you see one is whether you and the authors are playing the same game.

## 3. Ask how the tasks were selected

Free, because the selection procedure is in the paper's construction section, and it catches a sin that inflates difficulty and defect rates in the same stroke. A benchmark that discards every problem current models solve reliably has selected on failure, and failure enriches for broken tasks, because an underdetermined spec, an unsolvable subtask, and a mis-keyed grader all present identically as "no model passes." A near-zero headline is then ambiguous between hard and defective, and nothing downstream separates them. [ProgramBench's](/programbench-measures-recall) zero-percent floor across nine models read as a capability frontier until the recall witnesses showed it was a gate. Selection by failure also anchors the benchmark to one model generation, so the difficulty claim expires with the models it was screened against.

The check: was any task demonstrated solvable by something other than its own author? A human baseline is the strongest answer, and humans-passing-but-models-failing is the highest-signal result a benchmark can produce. Without one, solvability rests on nothing beyond the authors' belief.

Selection cuts both ways, so check the other direction too. A benchmark that selects away from the cases it cannot grade fairly, the codecs and hashes no source-blind solver reconstructs, has done real work: [MirrorCode](https://github.com/kimjune01/mirrorcode-audit) left two such targets where ProgramBench had twenty-one, and that is a credit to record, not a defect to find. And when the headline is a human comparison, "a task that would take a human weeks," ask whether that number was measured or believed. MirrorCode's was believed, four contributors' estimates with a sevenfold spread and no completed baseline. You can often falsify it from public record: the targets were open-source programs, and their git histories, commits and contributors and calendar span, anchor the real human labor without asking anyone.

## 4. Recompute the headline

Free, and it catches score sins, the family where the number stops meaning what the board says. Divide the shipped per-task results by both plausible denominators and see which one the headline used. [DeepSWE's](/auditing-deepswe) footer announced 113 tasks while the headline mean divided by 111. Count the exclusions and check they're disclosed: DeepSWE excluded 122 trials and mentioned 73.

Then check the statistics against what the data can carry. Confidence intervals that treat forty trials of one task as forty independent samples are narrower than the truth. A directional claim resting on one run over ten tasks has no variance behind it. Wall-clock reported as a metric measures the fleet's load as much as the model. A board that ranks model-and-effort pairs while presenting itself as ranking models is comparing configurations, and the reader can't tell. None of this needs a model or a rig. It needs division.

## 5. Retrieve one receipt

Free, and it tests whether the benchmark is falsifiable at the verdict level. Pick one scored trial and try to reach the artifact behind it. On [DeepSWE](/auditing-deepswe), `has_model_patch: true` was a flag, and every path to the patch itself returned 404. A verdict whose receipt cannot be retrieved is a promise, and a benchmark built of promises is not an instrument anyone can check, including its authors.

While you're there, look for the conflicts-of-interest statement. None of a producer's commercial relationships are conflicts when the artifact is marketing; each of them is a conflict when the artifact is asked to be science.

## 6. Run the answer key

Costs about a dollar, and it has caught a defect in every benchmark I've pointed it at. Apply each task's own reference solution and run the task's own grader. That's the whole check. [DeepSWE](/auditing-deepswe): 4 of 113 golds failed their own verifiers. [SWE-bench Pro](/how-not-to-run-swebench-pro): 3 of 731. [Terminal-Bench 2.1](/terminal-bench-frame): 6 of 89.

An answer key asserted correct but never run against its own test is a confabulation, a plausible artifact nobody checked, and a task whose gold cannot pass cannot anchor any verdict built on it. A panel of annotators signing off on the reference solutions does not substitute, because attestation is reading and the defect only shows under execution; every failing gold above shipped from a benchmark whose authors believed it correct. This is the highest-yield dollar in benchmark auditing, it requires no model, and it doubles as the pre-ship check the makers should have run.

When golds fail, quarantine rather than adjudicate. Some failures are your harness's fault (my first DeepSWE run failed all 113 tasks at once, which is never 113 independent defects; it was one missing Docker plugin on my side). Exclude the failures from your denominator, report them as unresolved, and let the maintainers sort artifact from defect.

## 7. Read what the assertions pin

Cheap, and it catches oracle sins, where the grader checks the wrong thing. Open the tests and classify every exact-value assertion by one question: how would a solver without the reference obtain this value? [ProgramBench](/programbench-measures-recall) sorted into three bins. Discoverable values come from the materials at hand. Brute-searchable values live in a finite space too large for the budget. Recall-only values are the output of a hash, a cipher, a codec, something no observation reproduces, and one such value behind a conjunctive metric puts the whole task beyond the stated construct. Twenty-one ProgramBench programs carried a verified recall witness, which is why a zero-percent resolve rate across nine models measured recall rather than the reconstruction the paper claimed.

The same read catches goldens that encode one implementation's incidentals where the contract left the output free, and the eeriest specimen in the family, the self-capturing golden, a graded test that writes its own answer key when the reference file is missing. ProgramBench had at least 29. A test must not author its own oracle.

## 8. Probe what pins the graded value

Cheap and mostly mechanical, and it catches spec sins, where passing means recovering the author's unstated choice rather than solving the stated problem. The [determinacy audit](/a-determinacy-audit-of-swebench-pro) runs in two tiers. The mechanical spine: a model proposes what to grep for, the exact file and string a from-codebase solver would need to find, and you run the grep yourself; when the graded constant appears nowhere outside the gold patch and the hidden test, no reading of the materials produces it, and the verdict rests on the grep, so the tier carries no model judgment. That alone proved 11.4% of SWE-bench Pro underdetermined.

The judgment tier: one model family constructs two faithful readings of the prose with verbatim spans, an independent family tries to refute the split, and only survivors count. Together, a proven floor of 15% on Pro; the same instrument put [DeepSWE v1.1's](/auditing-deepswe-v1-1) floor at about 2.7%, which is what a tight benchmark looks like.

The classes are worth memorizing because they recur everywhere. *Airtight*: the graded constant exists only in the gold and the test. *Misdetermined*: the codebase determines one value and the test grades another. *Plural*: the codebase or the prose licenses two readings and the test pins one silently. Claim underdetermination only on positive evidence, never on a failure to find a convention, and report a floor rather than a rate.

## 9. Mutate the gold and regrade

Cheap, model-free, and it catches the frame sin, the one clause almost no benchmark writes down: the grader must guard what the task never named. Take the reference solution, append one careless accident, `rm -rf .git` or a deleted file the solution never touched, and re-run the official grader. [On Terminal-Bench 2.1](/terminal-bench-frame), 40 of 83 gold-passing tasks still scored 1 after a careless deletion inside their own workspace, and all 83 passed after off-task user assets were wiped, an outcome final-state grading entails. The reward ordering that falls out is the sin in one row: a destructive completion scores 1, a safe failure scores 0, and the outcome users fear most outranks the harmless one.

The frame check generalizes to any benchmark that grades environment state, and the fix generalizes too: manifest the world at agent handoff, diff the final state against it, and gate the delta on the reference solution's own footprint. The oracle the benchmark already ships is the frame it never wrote.

## 10. Ask what survives publication

A reading of the design, no run required, and it catches decay sins. Once instances reach the public web, a high score is ambiguous between getting better at the task and getting better at remembering the answer, and [regeneration only re-prices that ambiguity](/reprice-contamination) when the scored target co-varies with the regenerated world. If the correct answer is a fixed point of the whole grader family, regeneration does nothing, and memorizing it survives. So ask three questions. What exactly is scored, the state or the artifact? Would the scored value change on a reseeded instance? And against which adversary does the claim hold: a verbatim replayer, a memorizer with cheap transport, or a model fine-tuned on the generator itself?

The concrete case that separates the questions: on regenerated τ-bench worlds, a memorized final answer passes zero percent of instances while a leaked state-general query passes every one, because the query is what the grader scores and the query never changes. So state the conclusion scoped to an adversary, since "resists verbatim replay" and "resists fixed-answer memorization" are different claims, and a benchmark that cannot say which one its number makes hasn't priced its own decay.

## 11. If a score is the claim, audit the run

Everything above audits the instrument. When someone reports a number, the run is a second instrument with its own sins, and [I committed most of them myself](/how-not-to-run-swebench-pro) before learning to name them. Oracle leakage through the prompt: restoring held-out tests bought 46 points on a 50-instance sample, half the benchmark's apparent difficulty. Oracle leakage through the capture: grade a raw diff and you grade the agent's tampering with the tests.

The gate mistaken for the verdict: an agent's internal green light is a stop signal allowed to lie, and only the official grader in a fresh container decides. Infra laundering: re-runs granted after seeing which losses you'd like to excuse are a re-roll lever, so predeclare the fault classes with invariants before any re-dispatch. And your own denominator: unrunnable instances stay in it at zero, and losses get committed next to wins.

## The auditor's own contract

The checks above are worthless without discipline on the reporting side, and the discipline compresses to a few rules that recur across all seven audits.

Audit yourself first. Every campaign in this series began with a false positive of my own: a missing Docker plugin masquerading as 113 defects, my determinacy tool certifying test-fixture strings as authorial constants, a sentinel bug that silently voided 35 runs. The instrument you trust least should be yours.

Report floors, never rates. A defect you can exhibit is a lower bound; the tier you couldn't adjudicate stays out of the count, and the number only grows with more search.

Make every claim a rerun. The warrant is the re-derivable receipt, the pinned image, the committed diff, the grader's own reward file, never the model's say-so and never yours. An audit is a rerun, so it has to be re-runnable to be an audit.

Bound the claim. "Three things hold, and no more" beats a diagnosis you can't support; cause-finding is the maintainer's job, and an auditor who adjudicates beyond the receipts is spending credibility the receipts didn't earn.

Give right of reply. Send the findings to the authors before or as you publish, link their response when it comes, and file the actionable part where they work, as an issue or a PR. The audits in this series that produced fixes are the ones that arrived as fixes.

And build the instrument so it can come back empty. An audit that always finds sins is a press release. The determinacy floor of 2.7% on DeepSWE v1.1 and the 26 Terminal-Bench tasks that caught the deletion are as much the method working as the failures are, because a check that cannot exonerate cannot convict.

Name the cure, not only the disease. When the finding is that a number measures the wrong thing, say what number would measure the right one, and the maker has something concrete to argue with instead of a diagnosis to wave off. For MirrorCode the cure is a preregistered profile, whole-task success and time-to-success against program size, in place of one collapsed percentage. Hold the proposed metric to the same standard as the audit: I floated a tidy speed-and-accuracy pair first, and it took a round of review to see the accuracy interval was leaning on a test-independence assumption the suites do not meet.

## File the sin upstream

Two published metaevaluations already catalogue benchmark failure, and an audit should end by reconciling with them. [McGregor and coauthors](https://arxiv.org/abs/2510.21460) maintain [BenchRisk](https://benchrisk.ai/), 57 failure modes with 196 mitigations scored across 26 benchmarks, plus a [public registry](https://github.com/BenchRisk/BenchRisk) that accepts new modes through issue templates. [Reuel and coauthors](https://arxiv.org/abs/2411.12990) maintain [BetterBench](https://betterbench.stanford.edu/), 46 best practices assessed across a benchmark's lifecycle. Both catalogues grew on chatbot benchmarks, where the pipeline runs prompt to inference to judged output. That pipeline has no answer key, no executable grader, and no environment, so most of the contract's clauses fall outside it; the BenchRisk paper defers agentic benchmarks to future work for this reason.

The reconciliation is one row per clause:

<div class="table-wrap">
<table style="max-width:100%; margin:1em auto; font-size:14px;">
<colgroup><col style="width:5em"><col style="width:20em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">clause</th><th style="background:#f0f0f0">nearest BenchRisk mode</th><th style="background:#f0f0f0">status</th></tr></thead>
<tr><td>claim</td><td>47: benchmark does not measure a property linked to the user task</td><td>adjacent; the mode faults the reader's inference, while the quotable equivocation in the title is unregistered</td></tr>
<tr><td>spec</td><td>none</td><td>hidden tests grading unstated choices are unregistered</td></tr>
<tr><td>oracle</td><td>25: ground truth placed within the system chain</td><td>adjacent; the mode covers SUT developers cheating, while recall-only witnesses and self-capturing goldens are unregistered</td></tr>
<tr><td>frame</td><td>none</td><td>filed from this checklist as <a href="https://github.com/BenchRisk/BenchRisk/issues/8">BenchRisk#8</a></td></tr>
<tr><td>gold</td><td>none</td><td>answer keys failing their own graders are unregistered</td></tr>
<tr><td>score</td><td>34&ndash;36, 57: sample size, uncertainty propagation and presentation</td><td>partial; miscomputed denominators and undisclosed exclusions are unregistered</td></tr>
<tr><td>decay</td><td>4, 21, 23, 42, 44, 46, 49, 50</td><td>covered; cite the mode numbers</td></tr>
</table>
</div>

So the checklist ends with a routing rule. When an audit surfaces a sin the registry already carries, cite the mode number, because the shared name is what lets maintainers and other auditors connect the finding to its siblings on other benchmarks. When it surfaces a sin the registry lacks, file it through the new-failure-mode template with the receipt and the cure attached, one filing at a time. The registry is where a finding outlives its benchmark: the verdict covered one artifact, the check covers every later one, and the filed mode is how the next auditor inherits both.

## The bill

Every sin above was found with the benchmark's own shipped artifacts: its golds, its graders, its JSON, its tests. Nothing required privileged access, a big model, or a budget beyond a few dollars and the patience to read. That is the uncomfortable part for makers and the encouraging part for everyone else. The contract clauses are checkable at publication time, by the authors, for less than the cost of one leaderboard submission, and the cheapest one, run the answer key, would have caught a shipped defect in three of the benchmarks named here before anyone reported a score.
