---
variant: post-medium
title: "Benchmark-Driven Development"
subtitle: "Why household robotics scores no longer predict a completed shift."
tags: methodology, epistemology, cognition
image: "/assets/press-driven-progress.png"
---

Frontier robots now exceed the human baseline on 19 of the 22 most widely reported manipulation benchmarks. Six months ago, none did. It remains difficult to determine what work those robots can be left to finish.

Recent releases exceed 99% on [FoldBench Verified](https://www.dyna.co/research/scaling-customer-deployments) and approach the scoring ceiling on [DishBench Pro](https://www.figure.ai/news/helix-02). Results on [ShowOnce-Hard](https://generalistai.com/blog/gen-1.5) suggest that the improvement extends to tasks specified through a single demonstration. Several benchmarks saturated months ahead of projections.

We reviewed the evaluation protocols behind these results and reran the leading packaging system against an eight-hour customer acceptance test. Its published score was 99.2%. Only 0.3% of shifts completed without human assistance.

These results are compatible.

![Benchmark history: FoldBench, DishBench and JarBench approach 100% within six weeks, while a launch forecast expected only 70% by week six.](/assets/press-driven-progress.svg)

## The spending behind the scores

By Q4 2027, quarterly customer spending on general-purpose robotics reached $112 billion, up from $7 billion in Q1 of the same year. Hardware accounted for $57 billion; site integration, operation, and support accounted for the remaining $55 billion. These figures cover purchases and services, excluding venture funding, announced orders, and conventional fixed-purpose automation.

![Quarterly robotics spending rises from $7 billion in Q1 2027 to $112 billion in Q4 2027, illustrated with robots and industry logos.](/assets/benchmark-driven-spending.png)

Procurement teams use public scores to shortlist vendors for site trials. A few percentage points can determine which system gets tested.

Buyers need forecasts of usable output and ongoing costs. A benchmark that only ranks prepared episodes can move money without reducing purchasing uncertainty.

## How we got here

The first generation of benchmarks established that robots could perform the motions at all. Pick up a cup. Fold a towel. Close a jar. A camera and a success label were enough to distinguish a useful policy from an arm sweeping the table.

Once those tasks became reliable, benchmarks expanded to unfamiliar objects, longer sequences, and instructions supplied through demonstration videos. Robots now recover grasps that would have ended an episode last year. They transfer skills between objects without a new training run.

The reporting format changed less. A percentage still summarizes episodes that begin with a prepared workspace and end when the visible action is complete. Readers increasingly interpret that percentage as the probability that a job gets done.

The word *task* accommodates both meanings.

![A robot folding a towel inside a marked evaluation area, with a cart of unsorted laundry outside it.](/assets/press-driven-fold.png)

> “We achieve human-level laundry performance across all evaluated textile configurations.”
>
> — *FoldBench Verified technical report*, abstract

*Evaluation area outlined in black. Input preparation is provided by the harness.*

## What the scores establish

The latest [JarBench-Hard](https://generalistai.com/blog/gen-1.5) winner closes 998 of 1,000 jars. The evaluator checks whether the lid is seated in the final image. It does not measure whether the threads engaged correctly or whether the closure survives a leak test. Cross-threaded lids were removed during dataset cleaning because annotators disagreed about them.

![Lab scene with two robotic grippers closing a jar and a visibly crooked lid on a foreground jar.](/assets/press-driven-jar.png)

> “Closure success is determined from the terminal camera observation. Instrumented seal verification is left to future work.”
>
> — *JarBench-Hard*, evaluation protocol

FoldBench checks corner alignment. Sorting, transporting, and stacking the folded items fall outside the episode. The human baseline includes folding; the staffing estimate attached to the announcement includes the laundry room.

[CleanRoomBench](https://www.staubli.com/us/en/robotics/industries/pharma-healthcare/pharmaceutical-production-and-biotechnology/aseptic-drug-manufacturing.html) reports zero contamination events. Its grader inspects video for visible spills. The benchmark title does additional work.

![Leaderboard: three robots exceed a human's 94.6% on prepared packing episodes. Shift completion and assistance are unreported for every entry.](/assets/press-driven-leaderboard.svg)

*Prepared episodes, fixed order mix. Dashes indicate unreported results.*

## The environment is part of the result

In our packaging evaluation, we held the robot, model checkpoint, and order mix fixed. We changed the episode boundary.

The published protocol placed each order within reach, replenished consumables between episodes, and restored the workspace after a failure. The evaluation team performed these operations outside the action trace, so they were not counted as interventions.

![Warehouse scene of a technician replacing a label roll while robotic packing arms wait beside an open box.](/assets/press-driven-packing.png)

> “No human interventions were required during any scored episode.”
>
> — *PackBench Verified system card*, autonomy statement

*Between scored episodes: label replenishment and workspace reset.*

The customer protocol started with a stocked station and kept the clock running. Empty tape rolls, obstructed labels, fallen items, and requests for help remained inside the trial. An operator could assist, but that assistance was recorded.

Across 1,000 eight-hour shifts, three finished without assistance. The system averaged 704 accepted packages per shift with 96 minutes of human support. Trained workers using the same packing equipment averaged 760 on matched order batches, under the same independent quality checks.

Each acceptance decision retained item scans, weight readings, inspection records, and the acceptance-rule version. A separate checker could reproduce the decision. Independent physical checks on sampled packages tested whether those records matched the contents and condition. Replaying a recorded weight did not establish that the scale was accurate.

We also challenged the checker with 200 deliberately defective packages containing missing items, wrong labels, or damaged contents. It passed four. We reported this false-pass rate separately; the output totals above count packages accepted by the procedure, not proven defect-free packages. Missing evidence was marked unverified.

Whether one person can support two robots or twenty is a purchasing question the original score never asked. The relevant comparison is total cost per accepted package at the required service level, including equipment, maintenance, and human support. A slower system that covers an otherwise unstaffed shift may be worth more to the buyer.

![Audit comparing prepared packing trials with continuous shifts: 99.2% episode success, 0.3% unassisted shifts; 704 accepted packages per robot shift with 96 minutes of support, versus 760 packages per human shift.](/assets/press-driven-shift.svg)

## Which human did the robot beat?

The human baseline has become the most stable line on the chart. It was collected once, before the third revision of the task set, using participants who received a ten-minute orientation.

The robots have since received new hands, additional demonstrations, and six months of training against the public tasks. The human number travels unchanged between releases. The maintainers declined to repeat the human trials because updating the baseline would compromise comparability with previous announcements.

For purchasing, we need the worker, tools, workload, and acceptance criteria to match the proposed deployment. We also need to count the people who prepare the robot's work and repair its mistakes. Moving their labor outside the frame does not remove it from the invoice.

Human performance supplies the economic alternative. The customer still decides what quality is acceptable. A human's failure rate is not permission for a robot to ship defective work.

## What we should report instead

For a robot sold to perform a job, the primary result should be **accepted work over a stated operating period**, accompanied by the resources and assistance required to produce it.

- **Let the buyer define acceptance.** A package must contain the correct undamaged items. A jar must pass an appropriate closure check. A finished motion is intermediate evidence.
- **Keep the clock running.** Include setup, replenishment, recovery, and cleanup when they belong to the promised service.
- **Publish assistance.** Report frequency, duration, and the work the human performed. Distinguish autonomous output from assisted output.
- **Identify the tested system.** Record the checkpoint, hands, sensors, control software, fixtures, and grader version. Results from one configuration do not automatically carry over to another.
- **Use a matched human baseline.** Evaluate trained workers with their normal tools on the same workload and quality standard.
- **Make completion independently checkable.** Retain the measurements needed to challenge a pass. When the evidence cannot establish completion, report it as unverified.

Buyers should be able to tell how much of that progress they can put on next month's schedule.

## Benchmarks that remain unsolved

- **ShiftBench Full.** Finish an eight-hour shift at the quoted cost. No submission passes both the physical and accounting checks.
- **DiaperBench.** Change a diaper without spreading its contents. Training on clean diapers has not transferred to production.
- **BrushBench.** Brush teeth without injuring gums. The grader measures duration; plaque removal is out of scope.
- **SandwichBench.** Make the sandwich the user wanted. Generalization to “less mayonnaise” remains unsolved.
- **CycleBench.** Cycle to the shops and back with the groceries. Bicycle theft is classified as an infrastructure failure.
- **IntimacyBench.** Make love with a consenting adult who wants to repeat it. Retrying until success violates the protocol.

The human baseline is under appeal.
