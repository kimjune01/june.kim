---
variant: post-medium
title: "Auditing JevBench"
subtitle: "Its calibration score penalizes exact answers to its probability questions."
tags: methodology, epistemology, coding
---

Applying [JevBench's](https://github.com/fstandhartinger/jevbench/tree/f8ce71361165846101d02ebc83ad44e47ae44fc3) scoring functions to exact gold responses on its public hard tier produces a calibration score of **97.0**. The same responses receive 100% accuracy and 100% probability fidelity. The difference comes from treating uncertainty about an event as uncertainty about answering the question correctly.

All 31 system rows' score arithmetic reproduces from the supplied aggregates, and the repository's 68 tests pass. I followed my [benchmark audit checklist](/how-to-audit-a-benchmark) at commit `f8ce713`, using results revision **v1.2.7**. That snapshot ranks 26 systems over 534 decisions for each complete run. The calibration defect concerns what the formula measures.

Benchmark Heaven maintains JevBench independently and explicitly disclaims affiliation with Jev's maker, TypeSafe. The benchmark evaluates models that return a typed decision from a piece of state and a bounded question, ideally with probabilities over the allowed answers. [Rerunnable probes and receipts.](/assets/jevbench-audit/REPRODUCE.md)

## Two meanings of 65 percent

The public question `hard-opus-b-probability-02` asks an incident-response team for root-cause probabilities based on a table of past outages. The new alert followed no recent deployment. Twenty historical incidents share that property: four came from bad pushes, thirteen from an upstream provider and three from hardware.

The answer key gives the corresponding probabilities as **20%, 65%, 15%**. Its most likely cause is the upstream provider. [Task and gold.](https://github.com/fstandhartinger/jevbench/blob/f8ce71361165846101d02ebc83ad44e47ae44fc3/datasets/public/hard.jsonl)

The probability that the provider caused the incident is 65% under the supplied reference distribution. Confidence that thirteen divided by twenty is the correct calculation can be 100%. The quantities have different targets.

The [calibration code](https://github.com/fstandhartinger/jevbench/blob/f8ce71361165846101d02ebc83ad44e47ae44fc3/jevbench/summarize.py) uses the largest returned probability as confidence in the selected label. Here that label matches the key, so the calculation compares 0.65 with a correctness value of 1. It counts the remaining 0.35 as underconfidence, although that uncertainty is part of the correct answer.

The composite calibration score averages two components. One measures agreement between confidence and label correctness using expected calibration error. The other measures fidelity to the gold probability distribution using total variation distance. On this item, the first rewards more certainty; the second rewards preserving the stated uncertainty.

Applying the official formula to this item alone gives:

| Returned probabilities | Label correct | Distance from gold | Calibration score |
|---|---:|---:|---:|
| 20%, 65%, 15%: exact gold | Yes | 0 | 65.0 |
| 0%, 100%, 0%: unsupported certainty | Yes | 0.35 | 82.5 |

This is a controlled probe of the objective, not a statistical estimate of calibration from one observation. It also does not show that sharpening every answer would improve the leaderboard: the two components use different denominators across the full suite.

The same mismatch appears across the full public hard set. All ten probability items receive their exact gold distributions; the other 101 receive one-hot gold labels. Every label passes and every probability distribution matches its target, yet the calibration score is **97.0023**. [Probe output.](/assets/jevbench-audit/audit-results.json)

## Composite scoring

Jev ranks first on the JevBench Score and third on its weighted-accuracy view, behind GPT-5.6 Luna and DeepSeek. The overall score combines accuracy, calibration, speed and cost through a geometric mean. Each transformed axis has 25% weight. [Formula.](https://github.com/fstandhartinger/jevbench/blob/f8ce71361165846101d02ebc83ad44e47ae44fc3/jevbench/composite_v12.py)

A model that returns labels without probabilities has no calibration score, which the composite treats as zero and then floors to one. A hypothetical classifier scoring 100 on accuracy, speed and cost would therefore reach **31.6 out of 100** overall. This is a consequence of the formula, not an observed error rate.

Nonproduction endpoint latencies are doubled, with another 0.15 seconds added to the benchmark authors' own servers. The authors clearly disclose that this adjustment approximates production load rather than measures it. Some self-hosted models are priced using estimated hosted tariffs. The resulting board compares models, deployment conditions and economic assumptions together.

The score changed after measurement, as the [revision history](https://github.com/fstandhartinger/jevbench/blob/f8ce71361165846101d02ebc83ad44e47ae44fc3/README.md) records. The work-in-progress score had three axes and assigned half its capability weight to hard tasks. The final score has four axes and assigns 30% of its accuracy weight to hard tasks. Earlier views remain available.

## Model configurations

The [shipped results](https://github.com/fstandhartinger/jevbench/blob/f8ce71361165846101d02ebc83ad44e47ae44fc3/results/v1.2/jevbench-v1.2-results.json) report accuracy and latency by tier, with cost averaged across the full run:

| Configuration | Hard accuracy, 220 tasks | Hard median latency | Dollars per 1,000 decisions, all 534 tasks |
|---|---:|---:|---:|
| Jev 1.13.0 | 74.1% | 0.672 s | $0.0399 |
| Gemini 3.1 Flash-Lite | 75.0% | 0.788 s | $0.2638 |
| DeepSeek V4.1 Flash, thinking default | 95.0% | 3.148 s | $0.5937 |

DeepSeek's hard-tier result counts eight failed responses as wrong. It has 209 correct answers and three incorrect answers among the remaining responses. Jev gets 163 correct and Gemini 165. Compared with Jev, Gemini gains two correct decisions and DeepSeek gains forty-six.

Jev is about fifteen times cheaper than the tested DeepSeek configuration, which the artifact labels **thinking default**. The adapter asks for a JSON probability for every option. Reported hard-tier output usage averages about 1,753 tokens per decision.

The cost and accuracy of DeepSeek with thinking disabled and a short constrained label remain unmeasured here. The published comparison does not include that configuration, and I have not run it.

Across all 534 decisions, Jev has 468 correct answers and DeepSeek 511. Using the costs for that same cohort, DeepSeek costs **$0.554 more per thousand decisions** and returns **80.5 more correct answers per thousand**. Dividing the cost difference by the accuracy difference gives **$0.00688 per additional correct answer**, about 0.69 cents. This calculation treats errors equally and excludes latency, retries and downstream costs; it is not the benchmark's tier-weighted accuracy score.

## Published artifacts

The checkout contains **231 of the 534 task texts**. These comprise 48 easy, 72 standard and 111 hard items. The other 303 are held out or imported, including all 146 judge items.

For Jev, Gemini and DeepSeek, the [public per-task file](https://github.com/fstandhartinger/jevbench/blob/f8ce71361165846101d02ebc83ad44e47ae44fc3/results/v1.2/jevbench-v1.2-per-task.json) contains a verdict code and rounded latency. It does not contain the selected label, probability vector, request or response. Fuller records are shipped for another entrant, but not these three.

The supplied data supports recounting verdict codes and reproducing the composite from aggregate calibration numbers. Without the responses, I cannot inspect the primary models' incorrect answers or reconstruct their calibration metrics. Regrading their distributions under a different interpretation is also unavailable.

The benchmark's runner captures responses and their hashes outside the public repository. The missing public-item responses are separate from the withheld task texts: releasing the former would not require releasing the latter.

## Separate phishing comparison

The Haiku comparison comes from a [different benchmark](https://github.com/anisselbd/jev-phishing-bench/tree/1d56e8c64d029a9554a0874e2ef2901ed196e230), on 2,000 phishing and legitimate emails. Haiku is absent from the JevBench snapshot above.

That study reports **62.6% accuracy for Jev and 81.3% for Haiku 4.5** on the direct verdict. Both kinds of error rise with Jev: phishing recall falls from 76.4% to 43.2%, while the false-positive rate rises from 13.8% to 18.0%. Its published confusion matrices reproduce those percentages; its raw responses are not shipped, so this is an arithmetic check of reported results.

At its reported list prices, choosing Jev saves **$0.424 per thousand emails while adding 187 errors** on that balanced dataset. That is about **0.23 cents saved per additional error**.

The same study reports higher accuracy after extracting five signals and fitting a classifier. Jev reaches 95.0% against Haiku's 93.2% on an internal holdout, with reported paired p = 0.063. The dataset's construction informed the signal questions, and the holdout analysis followed the initial exploration. I did not examine independent external validation of that pipeline.

## Validation and limits

All 231 public keys pass the scorer when encoded as one-hot answers, though that checks compatibility rather than the semantic truth of each key. Malformed probability maps fail closed in the mutations I ran. The aggregate score arithmetic and all 26 ranks agree. The authors disclose their deployment assumptions, their nonaffiliation with TypeSafe and earlier cost corrections.

The hard questions were model-authored and cross-reviewed. The stated 95% human performance is an authoring target, not a measured human baseline. I found no proven miskeyed label and performed no exhaustive semantic adjudication. The calibration witness proves a mismatch between a requested quantity and its evaluation; it does not prove that fixing it changes the winner.

## Discussion

**I would start with DeepSeek V4.1 Flash. It would take more evidence to convince me to choose Jev.** On this measured mix, DeepSeek costs about $0.55 more per thousand decisions and returns about 81 additional correct answers. The accuracy difference is substantial; the absolute price difference is small. For work whose errors require human review or correction, less than a cent per additional correct answer is a modest premium.

That sets the burden of proof for choosing Jev. I would want evidence from the intended workload that its accuracy is acceptable and that its lower cost or latency materially improves the application. Naming a possible use case does not supply that evidence. Neither does a large cost ratio when both absolute prices are low. Until that comparison exists, the measured accuracy advantage gives me a reason to prefer DeepSeek.

This is a default under uncertainty, not a finding that DeepSeek wins on every workload. Its observed result already includes thinking cost. Disabling thinking might improve its economics, but the accuracy of that cheaper configuration remains unmeasured here. Jev's composite first place does not resolve either question.

Separating distribution fidelity from confidence calibration would make JevBench's probability scores easier to interpret. Publishing public-item responses would make them independently checkable. Adding the optimized cheap-model baseline would make the cost comparison more complete. Show the measured accuracy, price and latency together, and let the application set the acceptable error rate. The overall rank assigns a value to mistakes that the buyer still has to determine.

*Receipts:* [audit script](/assets/jevbench-audit/audit.py), [results and hashes](/assets/jevbench-audit/audit-results.json), [reproduction instructions](/assets/jevbench-audit/REPRODUCE.md). This audit uses the pinned public artifacts and makes no new model calls. The findings have not yet received a maintainer response.
