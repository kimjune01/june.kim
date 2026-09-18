---
variant: post-medium
title: "Press-Driven Development"
subtitle: "Why household robotics scores no longer predict a completed shift."
tags: methodology, epistemology, cognition
image: "/assets/press-driven-progress.png"
---

Frontier robots now exceed the human baseline on 19 of the 22 most widely reported manipulation benchmarks. Six months ago, none did. This is substantial progress. It has also become difficult to determine what work those robots can be left to finish.

This week, [FoldBench Verified](https://www.dyna.co/research/scaling-customer-deployments) crossed 99%, [DishBench Pro](https://www.figure.ai/news/helix-02) was declared saturated, and [ShowOnce-Hard](https://generalistai.com/blog/gen-1.5) lost its suffix. Two labs delayed their announcements because the benchmark they had selected was solved before their video finished rendering.

We reviewed the evaluation protocols behind these results and reran the leading packaging system against an eight-hour customer acceptance test. Its published score was 99.2%. Only 0.3% of shifts completed without human assistance.

These results are compatible. That is the measurement problem.

![Fictional benchmark history: FoldBench, DishBench and JarBench approach 100% within six weeks, while a launch forecast expected only 70% by week six.](/assets/press-driven-progress.svg)

## How we got here

The first generation of benchmarks established that robots could perform the motions at all. Pick up a cup. Fold a towel. Close a jar. A camera and a success label were enough to distinguish a useful policy from an arm sweeping the table.

Once those tasks became reliable, benchmarks expanded to unfamiliar objects, longer sequences, and instructions supplied through demonstration videos. Each extension captured a real capability. Robots now recover grasps that would have ended an episode last year. They transfer skills between objects without a new training run.

The reporting format changed less. A percentage still summarizes episodes that begin with a prepared workspace and end when the visible action is complete. Readers increasingly interpret that percentage as the probability that a job gets done.

The word *task* accommodates both meanings.

![Generated scene of a robot folding a towel inside a marked evaluation area, with a cart of unsorted laundry outside it.](/assets/press-driven-fold.png)

> “We achieve human-level laundry performance across all evaluated textile configurations.”
>
> — *FoldBench Verified technical report*, abstract

*Evaluation area outlined in black. Input preparation is provided by the harness. Generated illustration of the fictional benchmark.*

## What the scores establish

The latest [JarBench-Hard](https://generalistai.com/blog/gen-1.5) winner closes 998 of 1,000 jars. The evaluator checks whether the lid is seated in the final image. It does not measure whether the threads engaged correctly or whether the closure survives a leak test. Cross-threaded lids were removed during dataset cleaning because annotators disagreed about them.

![Generated lab scene with two robotic grippers closing a jar and a visibly crooked lid on a foreground jar.](/assets/press-driven-jar.png)

> “Closure success is determined from the terminal camera observation. Instrumented seal verification is left to future work.”
>
> — *JarBench-Hard*, evaluation protocol

*Generated illustration of the fictional test setup.*

FoldBench checks corner alignment. Sorting, transporting, and stacking the folded items fall outside the episode. The human baseline includes folding; the staffing estimate attached to the announcement includes the laundry room.

[CleanRoomBench](https://www.staubli.com/us/en/robotics/industries/pharma-healthcare/pharmaceutical-production-and-biotechnology/aseptic-drug-manufacturing.html) reports zero contamination events. Its grader inspects video for visible spills. The result supports a claim about spills. The benchmark title does additional work.

None of these tests is useless. Each measures something narrower than the work suggested by its name. Near saturation, the unmeasured part increasingly determines whether the system is useful.

![Fictional leaderboard: three robots exceed a human's 94.6% on prepared packing episodes. Shift completion and assistance are unreported for every entry.](/assets/press-driven-leaderboard.svg)

## The environment is part of the result

In our packaging evaluation, we held the robot, model checkpoint, and order mix fixed. We changed the episode boundary.

The published protocol placed each order within reach, replenished consumables between episodes, and restored the workspace after a failure. These operations were performed by the evaluation team. They did not appear in the action trace and were not counted as interventions.

![Generated warehouse scene of a technician replacing a label roll while robotic packing arms wait beside an open box.](/assets/press-driven-packing.png)

> “No human interventions were required during any scored episode.”
>
> — *PackBench Verified system card*, autonomy statement

*Between scored episodes: label replenishment and workspace reset. Generated illustration of the fictional audit.*

The customer protocol started with a stocked station and kept the clock running. Empty tape rolls, obstructed labels, fallen items, and requests for help remained inside the trial. An operator could assist, but that assistance was recorded.

Across 1,000 eight-hour shifts, three finished without assistance. The system averaged 704 accepted packages per shift with 96 minutes of human support. Trained workers using the same packing equipment averaged 760 on matched order batches, under the same independent quality checks. The robot still produced substantial useful output. It also required a different staffing arrangement from the one suggested by its episode score.

Each acceptance decision retained item scans, weight readings, inspection records, and the acceptance-rule version. A separate checker could reproduce the decision. Independent physical checks on sampled packages tested whether those records matched the contents and condition. Replaying a recorded weight did not establish that the scale was accurate.

We also challenged the checker with 200 deliberately defective packages containing missing items, wrong labels, or damaged contents. It passed four. We reported this false-pass rate separately; the output totals above count packages accepted by the procedure, not proven defect-free packages. Missing evidence was marked unverified. The checker needed an evaluation too.

A robot that needs help occasionally can be a good purchase. Whether one person can support two robots or twenty is a purchasing question the original score never asked. The relevant comparison is total cost per accepted package at the required service level, including equipment, maintenance, and human support. A slower system that covers an otherwise unstaffed shift may be worth more to the buyer.

![Fictional audit comparing prepared packing trials with continuous shifts: 99.2% episode success, 0.3% unassisted shifts; 704 accepted packages per robot shift with 96 minutes of support, versus 760 packages per human shift.](/assets/press-driven-shift.svg)

## Which human did the robot beat?

The human baseline has become the most stable line on the chart. It was collected once, before the third revision of the task set, using participants who received a ten-minute orientation.

The robots have since received new hands, additional demonstrations, and six months of training against the public tasks. The human number travels unchanged between releases.

That comparison can answer a research question about performance under the original study conditions. It cannot establish that the system replaces a trained worker using ordinary equipment.

For purchasing, we need the worker, tools, workload, and acceptance criteria to match the proposed deployment. We also need to count the people who prepare the robot's work and repair its mistakes. Moving their labor outside the frame does not remove it from the invoice.

Human performance supplies the economic alternative. The customer still decides what quality is acceptable. A human's failure rate is not permission for a robot to ship defective work.

## Press-driven development

A release now needs a result that distinguishes it from last week's release. Saturated benchmarks cannot supply one, so new benchmarks appear with more objects, longer horizons, or less familiar kitchens. The cycle produces useful research and an expanding set of incompatible claims.

The easier response to an exhausted benchmark is to make it harder. Adding a crooked lid is harder. Checking whether the jar is sealed changes what the benchmark measures. Only the second addresses the customer's objection.

[ShiftBench Ultra](https://bostondynamics.com/solutions/warehouse-automation/trailer-unloading/) was introduced to close this gap. Its initial release evaluates full shifts, except for charging, replenishment, and exceptional recovery. Those exclusions are scheduled for ShiftBench Ultra Real.

The name has advanced further than the boundary.

## What we should report instead

For a robot sold to perform a job, the primary result should be **accepted work over a stated operating period**, accompanied by the resources and assistance required to produce it.

That requires a few changes:

- **Let the buyer define acceptance.** A package must contain the correct undamaged items. A jar must pass an appropriate closure check. A finished motion is intermediate evidence.
- **Keep the clock running.** Include setup, replenishment, recovery, and cleanup when they belong to the promised service.
- **Publish assistance.** Report frequency, duration, and the work the human performed. Distinguish autonomous output from assisted output.
- **Identify the tested system.** Record the checkpoint, hands, sensors, control software, fixtures, and grader version. Results from one configuration do not automatically carry over to another.
- **Use a matched human baseline.** Evaluate trained workers with their normal tools on the same workload and quality standard.
- **Make completion independently checkable.** Retain the measurements needed to challenge a pass. When the evidence cannot establish completion, report it as unverified.

Component benchmarks still help explain where a system improved. A purchasing benchmark must establish whether those improvements survive the rest of the job.

The robots are improving faster than expected. Buyers should be able to tell how much of that progress they can put on next month's schedule.

---

*Speculative satire. All benchmark names, quotations, scores, audit results, and charts above are fictional. Photographic scenes are AI-generated illustrations. Benchmark links lead to real robotics demonstrations or application pages; they do not substantiate the invented results or attribute these practices to the linked companies. The evaluation-report structure draws on [OpenAI's coding benchmark audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/) and [Anthropic's analysis of evaluation infrastructure](https://www.anthropic.com/engineering/infrastructure-noise).*
