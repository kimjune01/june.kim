---
variant: post-medium
title: "How to Audit a Benchmark"
subtitle: "Six audits' worth of sins, ordered by how cheaply they're caught."
tags: methodology, epistemology
---

Over the past few months I audited six benchmarks: [SWE-bench Verified](/swebench-verified) (as a runner), [DeepSWE](/auditing-deepswe) and [its revision](/auditing-deepswe-v1-1), [SWE-bench Pro](/a-determinacy-audit-of-swebench-pro), [ProgramBench](/programbench-measures-recall), [τ-bench's contamination story](/reprice-contamination), and [Terminal-Bench](/terminal-bench-frame). Every one of them failed somewhere, and no two failed in the same place. This post compresses the lenses into a checklist a stranger can run.

The premise that organizes everything: a benchmark is a measurement instrument, and an instrument makes a contract. The instruction pins the target. The grader checks the target. The grader guards everything the task never named. The answer key passes its own test. The headline number means what the leaderboard says it means. And the number survives its own publication. Each clause can be broken, each break is a distinct sin, and each sin has a check. The checks below are ordered by cost, because the ordering is the finding: in every audit, the cheapest checks caught the worst sins.

## 1. Read the paper against the repo

Free, and it catches the sin of the wrong rulebook. The scoring rules often live in the paper while the runnable code implements something looser. On SWE-bench Pro [I lost a week and about a thousand dollars](/how-not-to-run-swebench-pro) solving the wrong task because the held-out-test rule was on pages 4 through 9 of the paper and nowhere in the repo. A surprising number is a stop sign, and the first thing to check when you see one is whether you and the authors are playing the same game.

## 2. Ask how the tasks were selected

Free, because the selection procedure is in the paper's construction section, and it catches a sin that inflates difficulty and defect rates in the same stroke. A benchmark that discards every problem current models solve reliably has selected on failure, and failure enriches for broken tasks, because an underdetermined spec, an unsolvable subtask, and a mis-keyed grader all present identically as "no model passes." A near-zero headline is then ambiguous between hard and defective, and nothing downstream separates them. [ProgramBench's](/programbench-measures-recall) zero-percent floor across nine models read as a capability frontier until the recall witnesses showed it was a gate. Selection by failure also anchors the benchmark to one model generation, so the difficulty claim expires with the models it was screened against.

The check is one question: was any task demonstrated solvable by something other than its own author? A human baseline is the strongest answer, and humans-passing-but-models-failing is the highest-signal result a benchmark can produce. Its absence means the benchmark has not shown its tasks are solvable at all, only that its authors believe them to be.

## 3. Recompute the headline from the shipped data

Free, and it catches score sins, the family where the number stops meaning what the board says. Divide the shipped per-task results by both plausible denominators and see which one the headline used. DeepSWE's footer announced 113 tasks while the headline mean divided by 111. Count the exclusions and check they're disclosed: DeepSWE excluded 122 trials and mentioned 73. Check the intervals: confidence intervals computed over clustered trials as if independent, comparisons resting on a single run over ten tasks, wall-clock reported as if it were a metric, a leaderboard ranking model-and-effort pairs while presenting itself as ranking models. None of this needs a model or a rig. It needs division.

## 4. Try to retrieve one receipt

Free, and it tests whether the benchmark is falsifiable at the verdict level. Pick one scored trial and try to reach the artifact behind it. On DeepSWE, `has_model_patch: true` was a flag, and every path to the patch itself returned 404. A verdict whose receipt cannot be retrieved is a promise, and a benchmark built of promises is not an instrument anyone can check, including its authors. While you're there, look for the conflicts-of-interest statement. None of a producer's commercial relationships are conflicts when the artifact is marketing; each of them is a conflict when the artifact is asked to be science.

## 5. Run the answer key

Costs about a dollar, and it has caught a defect in every benchmark I've pointed it at. Apply each task's own reference solution and run the task's own grader. That's the whole check. DeepSWE: 4 of 113 golds failed their own verifiers. SWE-bench Pro: 3 of 731. Terminal-Bench 2.1: 6 of 89. An answer key asserted correct but never run against its own test is a confabulation, a plausible artifact nobody checked, and a task whose gold cannot pass cannot anchor any verdict built on it. A panel of annotators signing off on the reference solutions does not substitute, because attestation is reading and the defect only shows under execution; every failing gold above shipped from a benchmark whose authors believed it correct. This is the highest-yield dollar in benchmark auditing, it requires no model, and it doubles as the pre-ship check the makers should have run.

When golds fail, quarantine rather than adjudicate. Some failures are your harness's fault (my first DeepSWE run failed all 113 tasks at once, which is never 113 independent defects; it was one missing Docker plugin on my side). Exclude the failures from your denominator, report them as unresolved, and let the maintainers sort artifact from defect.

## 6. Read what the assertions pin

Cheap, and it catches oracle sins, where the grader checks the wrong thing. Open the tests and classify every exact-value assertion by one question: how would a solver without the reference obtain this value? [ProgramBench](/programbench-measures-recall) sorted into three bins. Discoverable values come from the materials at hand. Brute-searchable values live in a finite space too large for the budget. Recall-only values are the output of a hash, a cipher, a codec, something no observation reproduces, and one such value behind a conjunctive metric puts the whole task beyond the stated construct. Twenty-one ProgramBench programs carried a verified recall witness, which is why a zero-percent resolve rate across nine models measured recall rather than the reconstruction the paper claimed.

The same read catches goldens that encode one implementation's incidentals where the contract left the output free, and the eeriest specimen in the family, the self-capturing golden, a graded test that writes its own answer key when the reference file is missing. ProgramBench had at least 29. A test must not author its own oracle.

## 7. Probe what pins the graded value

Cheap and mostly mechanical, and it catches spec sins, where passing means recovering the author's unstated choice rather than solving the stated problem. The [determinacy audit](/a-determinacy-audit-of-swebench-pro) runs in two tiers. The mechanical spine: a model proposes what to grep for, and the grep settles it, so the tier carries no model judgment. That alone proved 11.4% of SWE-bench Pro underdetermined. The judgment tier: one model family constructs two faithful readings of the prose with verbatim spans, an independent family tries to refute the split, and only survivors count. Together, a proven floor of 15% on Pro; the same instrument put DeepSWE v1.1's floor at about 2.7%, which is what a tight benchmark looks like.

The classes are worth memorizing because they recur everywhere. *Airtight*: the graded constant exists only in the gold and the test. *Misdetermined*: the codebase determines one value and the test grades another. *Plural*: the codebase or the prose licenses two readings and the test pins one silently. Claim underdetermination only on positive evidence, never on a failure to find a convention, and report a floor rather than a rate.

## 8. Mutate the gold and regrade

Cheap, model-free, and it catches the frame sin, the one clause almost no benchmark writes down: the grader must guard what the task never named. Take the reference solution, append one careless accident, `rm -rf .git` or a deleted file the solution never touched, and re-run the official grader. [On Terminal-Bench 2.1](/terminal-bench-frame), 40 of 83 gold-passing tasks still scored 1 after a careless deletion inside their own workspace, and all 83 passed after off-task user assets were wiped, an outcome final-state grading entails. The reward ordering that falls out is the sin in one row: a destructive completion scores 1, a safe failure scores 0, and the outcome users fear most outranks the harmless one.

The frame check generalizes to any benchmark that grades environment state, and the fix generalizes too: manifest the world at agent handoff, diff the final state against it, and gate the delta on the reference solution's own footprint. The oracle the benchmark already ships is the frame it never wrote.

## 9. Ask what survives publication

An analysis rather than a run, and it catches decay sins. Once instances reach the public web, a high score is ambiguous between getting better at the task and getting better at remembering the answer, and [regeneration only re-prices that ambiguity](/reprice-contamination) when the scored target co-varies with the regenerated world. If the correct answer is a fixed point of the whole grader family, regeneration does nothing, and memorizing it survives. So ask three questions. What exactly is scored, the state or the artifact? Would the scored value change on a reseeded instance? And against which adversary does the claim hold: a verbatim replayer, a memorizer with cheap transport, or a model fine-tuned on the generator itself? A benchmark that cannot say which adversary its number defeats hasn't priced its own decay.

## 10. If a score is the claim, audit the run

Everything above audits the instrument. When someone reports a number, the run is a second instrument with its own sins, and [I committed most of them myself](/how-not-to-run-swebench-pro) before learning to name them. Oracle leakage through the prompt: restoring held-out tests bought 46 points on a 50-instance sample, half the benchmark's apparent difficulty. Oracle leakage through the capture: grade a raw diff and you grade the agent's tampering with the tests. The gate mistaken for the verdict: an agent's internal green light is a stop signal allowed to lie, and only the official grader in a fresh container decides. Infra laundering: re-runs granted after seeing which losses you'd like to excuse are a re-roll lever, so predeclare the fault classes with invariants before any re-dispatch. And denominator honesty on your own side: unrunnable instances score zero rather than vanish, and losses get committed next to wins.

## The auditor's own contract

The checks above are worthless without discipline on the reporting side, and the discipline compresses to a few rules that recur across all six audits.

Audit yourself first. Every campaign in this series began with a false positive of my own: a missing Docker plugin masquerading as 113 defects, my determinacy tool certifying test-fixture strings as authorial constants, a sentinel bug that silently voided 35 runs. The instrument you trust least should be yours.

Report floors, never rates. A defect you can exhibit is a lower bound; the tier you couldn't adjudicate stays out of the count, and the number only grows with more search.

Make every claim a rerun. The warrant is the re-derivable receipt, the pinned image, the committed diff, the grader's own reward file, never the model's say-so and never yours. An audit is a rerun, so it has to be re-runnable to be an audit.

Bound the claim. "Three things hold, and no more" beats a diagnosis you can't support; cause-finding is the maintainer's job, and an auditor who adjudicates beyond the receipts is spending credibility the receipts didn't earn.

Give right of reply. Send the findings to the authors before or as you publish, link their response when it comes, and file the actionable part where they work, as an issue or a PR rather than a conclusion. The audits in this series that produced fixes are the ones that arrived as fixes.

And build the instrument so it can come back empty. An audit that always finds sins is a press release. The determinacy floor of 2.7% on DeepSWE v1.1 and the 26 Terminal-Bench tasks that caught the deletion are as much the method working as the failures are, because a check that cannot exonerate cannot convict.

## The bill

Every sin above was found with the benchmark's own shipped artifacts: its golds, its graders, its JSON, its tests. Nothing required privileged access, a big model, or a budget beyond a few dollars and the patience to read. That is the uncomfortable part for makers and the encouraging part for everyone else. The contract clauses are checkable at publication time, by the authors, for less than the cost of one leaderboard submission, and two of the checks, run the answer key and read your own assertions, would have caught the worst finding in every benchmark named here before it shipped.
