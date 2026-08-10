---
variant: post-medium
title: "Auditing SlopCodeBench"
subtitle: "It measures static code-shape drift, not yet extension robustness."
tags: methodology, epistemology, coding
---

[SlopCodeBench](https://www.scbench.ai/) concludes that agents lack the design discipline iterative development demands. Its experiment establishes less: under expanding specifications, two static code-shape metrics usually rise. Neither metric is validated as extension robustness, and iteration is not isolated as the cause. [Construct receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/00-construct.md)

## The ruler misses

Structural erosion is the share of complexity concentrated in functions above a cyclomatic-complexity threshold. The paper reports its correlation with passing the next checkpoint: **−0.018**. Lines of code reaches **−0.212**. For next-checkpoint cost, erosion reaches **0.167** and LOC **0.502**.

Verbosity has a different problem. Its 137 rules were developed partly from observed agent code, then used to conclude that agent code is 2.3 times as verbose as human repositories. A ruler built partly from one population's characteristic marks will distinguish that population by construction. The comparison needs to survive on clone coverage alone, on rules developed without the evaluated agents, or under blinded human judgment. None is reported.

## Iteration is not the treatment

Every checkpoint adds requirements. Later code has undergone more edits, has more work to do, and faces a harder specification. The experiment changes all three together.

The comparison against commits from 473 unrelated Python repositories does not separate them. Those commits are a calibration panel. Nobody reimplemented the cumulative specifications from scratch.

Under SlopCodeBench's combination of repeated editing and expanding scope, its static metrics rise. “Iteration causes degradation” requires the missing counterfactual.

## The frontier was selected

The authors removed proposed problems that frontier agents could solve in one shot, then reported that no agent solved a surviving problem end to end. Saturation filtering can preserve headroom. It also conditions the result on model failure.

The paper does not report the screening models and versions, the number removed, an unfiltered comparison, or an independent human baseline. The low score is performance on a set selected partly because frontier agents failed it, not an unconditioned estimate of iterative coding ability. [Selection receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/01-selection.md)

## Nobody disclosed a red team

The paper describes coauthor review and agent-assisted refinement of ambiguous tests. That is maker QC. It does not disclose an independent team asked to break the construct, run the answer keys, mutate passing golds, or rederive the scores.

- The final `dynamic_buffer` answer key fails an applicable Python test. It emits row numbers 101 through 106 where the test requires 1 through 6. The same procedure clears `trajectory_api` at 373 of 373, so this is a demonstrated floor, not a defect rate. [Gold receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/02-gold.md)
- A wrapper deletes a test-unreferenced file from the passing `trajectory_api` workspace and delegates to the unchanged gold. The probe confirms the file is gone; all 373 tests still pass. [Frame receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/03-frame.md)
- No scored model workspace or per-checkpoint result is retrievable from the linked public artifacts. The paper reports GPT-5.5 at 29 of 196 strict checkpoints; the current leaderboard reports 28. Without trial receipts, that is version drift, not a proven arithmetic error. The embedded data also contains multiple rows with identical displayed configurations and different scores. [Score receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/04-score-receipts.md)

No independent adversarial validity audit is disclosed, and the internal process missed defects across the claim, selection, gold, frame, and score clauses. [Review-process receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/05-review-process.md)

## The next experiment

At checkpoint *n*, give one agent its checkpoint *n−1* workspace. Give another an empty workspace plus the complete specification through *n*. Hold model, harness, budget, specification, and tests fixed. The difference estimates the cost of accumulated history; their shared decline estimates task growth.

Then validate erosion against an external outcome: defects in checkpoint *n+1*, maintenance time, or success by a blinded agent inheriting the code. Control for LOC. If the metric does not predict future maintenance cost, call it static code-shape drift.

Publish the sampling funnel: every candidate, exclusion, screening model, and one-shot result. Test preservation requirements, run mutation and frame-breaking probes, and verify every gold in the public harness. Release immutable benchmark versions, scored workspaces, per-checkpoint rows, and the leaderboard calculation.

Commission an independent team to attack the evaluator before release, then publish the attacks and fixes.

Until those controls exist, report *static code-shape drift under iterative specification refinement*. The next version needs a control group more than another model.

[Reproduce the audit](https://github.com/kimjune01/slopcodebench-audit): pinned sources, scripts, tests, and finding-level receipts.

*Disclosure: Claude challenged candidate findings during the audit. Its objections narrowed the claims; the receipts decide them.*
