# Statistics: an interactive introduction

Status: sixteen-chapter introductory course implemented, 2026-09-22. Interactive practice also reaches all nine OpenIntro chapters. Reader sessions and the optional extensions below remain future work.

## Current implementation

- The statistics index and chapters follow the calculus textbook’s format: shared `Layout`, `ChapterTable`, `Neighbors`, and `PrevNext`; standard headings, source lines, callout utilities, and reference tables. Activity controls retain their behavior within the shared book styling. Contextual links connect the course to the companion probability textbook. A shared sixteen-chapter manifest powers the outline, progress labels, and previous/next links.

- Original foundational chapters: describing data, samples, sampling bias and assignment, sampling distributions and the CLT, confidence intervals, and null-model testing. Each has two questions with answer-specific feedback, definitions in context, a concluding formal idea, and a new-context application.
- Culminations now include definitions, relationships, and theorems. The CLT chapter explicitly distinguishes the fixed population, observations per sample, repetitions, standard error, and the theorem’s assumptions. Simulation illustrates the theorem rather than proving it.
- Added reusable activities for salaries/outliers, town sampling, treatment assignment, sample means from three population shapes, interval coverage, and a one-sided exact binomial comparison. Integrated relevant activities into OpenIntro 1–2 and 4–7.
- Added conditional-probability counts to OpenIntro 3, adjustable least-squares lines and an influential point to OpenIntro 8, and a logistic probability/odds explorer to OpenIntro 9. These include transfer questions and expandable formal summaries.
- Added direct, topic-matched StatQuest links near the end of 24 chapters, using [Josh Starmer’s official video index](https://statquest.org/video_index.html). The sampling-design chapter has no forced match. Videos supplement the text and do not gate progress or load third-party embeds.
- Corrected small-sample mean inference to use t critical values with stated assumptions, replaced the old modular-arithmetic “random” sampling/assignment, qualified causal and R-squared claims, and repaired unsupported Scheme operations. All 34 existing Scheme examples now execute with the installed interpreter.
- Verification: supplied-randomness model tests, UI behavior tests, independent SciPy checks of the Welch/paired examples, TypeScript, all-site Vitest (61 checks before removing temporary tests), reading build (534 pages), sixteen-chapter navigation checks, local links and anchors across all 26 statistics pages, and Chrome interaction/layout checks. Removed the new temporary test files after they passed, per the author’s preference; retained pre-existing tests.
- The university continuation adds classroom surveys, experiment design, A/B randomization, independent and paired t inference, errors and power, chi-square/ANOVA, regression inference, and a study-reading capstone. The A/B and paired-means activities are reused in OpenIntro 6 and 7. jStat supplies reference-distribution CDFs and quantiles; simulation remains explicit and local.
- An optional later extension is pooled versus group-specific regression in OpenIntro 9. Reader sessions remain necessary before making claims about learning effectiveness.
- Local implementation only; not deployed.

## Pilot implementation

- Added `/reading/statistics/chance/` and `/reading/statistics/repeated-experiments/`, with a spinner, repeated-coin experiment, saved comparisons, six explanatory questions, and interactive symbolic summaries.
- Updated the landing page to expose the beginner path and all nine existing chapters. Repaired chapter 5→6 navigation and the OpenIntro source links; added links back into the pilot.
- Used Danielle Navarro’s *Learning Statistics with R* (CC BY-SA 4.0) as a model for conversational, concrete instructional prose. The new chapters include credit and licensing, with independently written examples and questions.
- Components live in `src/components/statistics/`; `reading-src/components` is an existing symlink to `src/components`. Pure simulation functions live in `reading-src/lib/statistics/`.
- Verified simulation accounting, setting resets, comparison alignment, feedback/retry behavior, and server-rendered SVG titles with tests. Checked TypeScript and the reading build, and exercised the pilot in Chrome at desktop and phone widths, in light and dark themes.
- Informal sessions with beginner readers remain to be done. No learning-effectiveness claim is inferred from automated checks. The pilot has not been deployed.

## Purpose

Make `/reading/statistics/` approachable for readers who know everyday arithmetic but have no statistics or programming background. The existing chapters introduce definitions and computational procedures quickly; readers need concrete experiences that give those definitions meaning.

Add a beginner sequence of short, guided experiments, then connect it to the nine existing OpenIntro chapters. Improve those chapters with targeted activities and feedback as the sequence grows. Learning should come from making predictions, manipulating examples, interpreting results, and applying the idea in a different setting.

The culmination of a section or chapter is an earned formal idea: a definition, a symbolic representation, a relationship, or a theorem that compresses what the reader has learned. Following the ending of [General Intelligence](../src/content/blog/2026-03-14-general-intelligence.md), the expression should feel earned: familiar experiences become something compact enough to remember and use in the next chapter. This is a user-directed design principle; the research below does not independently establish the effectiveness of this particular reveal pattern.

## University introductory-course scope

The guided path extends through a typical first university statistics course, with interpretation and basic experiment design as the endpoint. The first nine chapters establish the foundations, including a student-survey chapter between averages and sampling. The continuation applies them to studies with real decisions. Use OpenIntro Statistics’ core sequence as a coverage reference, not a claim of equivalence to a credit-bearing course.

| Chapter | Question and activity | Earned idea |
| --- | --- | --- |
| 4. Student surveys | Draw students, switch between numerical and categorical variables, change histogram bins, and add an outlier. | Frequency tables, five-number summaries, IQR, sample standard deviation, and the distinction between description and inference. |
| 10. Planning an experiment | Design a classroom comparison; choose the assignment unit, allocation, outcome, and analysis rule. | The independent unit, random assignment, comparison, and prespecified measurement determine what a causal claim supports. |
| 11. Comparing proportions | Collect an A/B experiment and shuffle its group labels under a no-effect model. | Difference in proportions; a two-sided randomization p-value; effect size versus evidence. |
| 12. Comparing means | Compare independent groups, then preserve or break the pairing of repeated measurements. | Welch and paired t procedures; standard error and interval depend on the design. |
| 13. Errors and power | Repeat studies while varying true effect, sample size, and significance threshold; examine multiple testing. | Type I/II errors, power, and a planned error rate. |
| 14. Beyond two groups | Change categorical counts and the separation of three numerical groups. | Chi-square and ANOVA compare observed variation with a null model; an omnibus result does not identify every difference. |
| 15. Relationships and prediction | Fit a line, add an influential observation, and inspect slope uncertainty. | Correlation, regression, residuals, and the distinction between association, prediction, and causation. |
| 16. Reading a study | Interpret a classroom experiment from design through effect, interval, p-value, and limitations. | A defensible conclusion combines study design, effect size, uncertainty, and context. |

Each chapter retains the calculus book’s shared layout and navigation, contextual probability-textbook links, relevant StatQuest videos, and feedback on transfer questions. Inferential procedures name their assumptions; simulations and constructed examples are labeled. Core coverage includes one-sample inference, two proportions, independent and paired means, categorical counts, ANOVA, and simple regression. Multiple and logistic regression remain optional continuations.

Acceptance: a reader can state a null and alternative, distinguish a one- from two-sided question, interpret a p-value without reversing the conditioning, report an effect with uncertainty, recognize dependent observations, choose a basic comparison method, and propose a randomized experiment with a clear unit, outcome, and stopping rule.

## Learning outcomes

A reader finishing the introduction should be able to:

- Distinguish a model's probability from the frequency observed in a finite experiment.
- Identify numerical and categorical variables; describe student-survey data with frequency tables, histograms, center, quartiles, and spread; explain what a summary leaves out.
- Distinguish a population, a sample, an individual measurement, and an estimate.
- Explain why increasing a random sample's size reduces sampling variability but does not repair a biased selection process.
- Explain the Central Limit Theorem and its assumptions; interpret repeated estimates and confidence-interval coverage without confusing them with the distribution of individual measurements.
- Explain a simulation-based test as comparing observed evidence with what a specified null model produces.
- Interpret p-values, confidence intervals, power, and practical importance separately; choose basic proportion, mean, paired, categorical, and regression procedures with their assumptions.
- Design a randomized comparison with an explicit experimental unit, control, primary outcome, stopping rule, and analysis that respects pairing or clustering.
- Explain the chapter's concluding idea in ordinary language, connect it to the experiment, and use it in a fresh example.

For each outcome, write a prediction prompt, an explanation, and a transfer question before implementing the activity. A transfer question changes the setting while preserving the statistical idea.

## Book structure

The landing page presents two clearly labeled routes:

1. **Start here: statistics through experiments.** The new beginner sequence, ordered by prerequisites.
2. **Go deeper: OpenIntro chapters.** All nine existing chapters, with their current URLs and chapter identities preserved.

Each introductory chapter ends with a relevant OpenIntro link. Each OpenIntro chapter links back to the specific introductory experience that prepares the reader for it. Introduce terms in context and add a small “Words you met” recap; definitions remain visible and linkable after the activity.

Proposed introductory routes live directly under `/reading/statistics/` with descriptive slugs. Only completed chapters appear in navigation. Keep the separate `/reading/probability/` book as an optional mathematical continuation.

## The section pattern

Use this as an authoring guide, with room for variation:

1. **Orient:** one concrete question and enough explanation to understand the controls.
2. **Predict:** a quick choice or estimate; invite a reason when useful. Predictions can be skipped.
3. **Experiment:** one main control initially, an obvious action button, and a result whose meaning is visible.
4. **Explain:** connect what happened to the question, including ordinary random variation. Introduce one or two terms at a time.
5. **Check:** after selected sections, ask a short question with explanation for every answer.
6. **Compress:** toward the end of a section or chapter, name or state the definition, relationship, notation, or theorem that gathers the experiences the reader now understands.
7. **Transfer:** let the reader unpack or use that representation in a different context, making it a tool for the next learning cycle.

Target roughly 5–10 minutes for a chapter's main path as an initial design hypothesis, to be checked with readers. Allow additional exploration. Keep formal derivations and runnable code in optional deeper sections.

## Earned formal ideas

Every new chapter must have an authored culmination. Choose its form to suit the discovery; a theorem such as the Central Limit Theorem is as meaningful an arrival as a formula. A substantial section may have its own smaller one when the concept is ready. Plan this representation when planning the activity, so the interaction teaches the meaning of its parts.

Present the culmination as a quiet moment of arrival: “You can now write this.” Use standard statistical notation where it fits; a compact diagram can express a relationship better than a formula. Introduce it late enough to mean something, then leave it available as a reference.

The presentation has four parts:

1. A short reminder of what the reader discovered.
2. The compact expression, assembled from familiar quantities or relationships.
3. A plain-language reading, with each symbol linked to a quantity or action in the experiment.
4. A fresh example that checks whether the reader can expand the shorthand back into reasoning.

For example, after repeatedly pooling salaries and dividing the total equally, reveal the mean first as “total salary / number of people,” then as `x̄ = (x₁ + … + xₙ) / n`, and finally as `x̄ = (1/n) Σᵢ₌₁ⁿ xᵢ`. Selecting the summation highlights all the salaries; selecting `n` highlights the count. Give unfamiliar notation its own explanation. The reader earns a useful compression through understanding, while the explanation remains available regardless of quiz performance.

Activities should sit beside the explanation they support. Show real results in the activity's conclusion where useful. A theorem reveal must distinguish observation from proof and give its assumptions; simulations illustrate a theorem rather than establish it.

### Proposed chapter culminations

| Chapter | Earned idea | What the reader should be able to unpack |
| --- | --- | --- |
| Probability and Events | `P(A) = p`, illustrated by `P(blue) = 0.5` | `A` names the event, and `p` describes its chance under the model; it is distinct from the observed fraction. |
| Random Variables and Distributions | `X = number of heads in one round`, then `p̂ = X/n`, beside the histogram | One round produces one value of `X`; dividing by coins per round gives the observed proportion. The hat marks an estimate, not a new true probability. |
| Center and Spread | `x̄ = (1/n) Σᵢ₌₁ⁿ xᵢ`, accompanied by contrasting datasets with equal means | Each measurement, addition, count, and division corresponds to something the reader manipulated; the formula compresses center while omitting shape. |
| Populations and Samples | `population (μ) → sample → estimate (x̄)` | `μ` is the target population mean; `x̄` is computed from the sampled observations. New samples can change the estimate without changing the target. |
| Sampling Bias and Random Assignment | A population-to-sample diagram with the selection rule explicitly on the arrow; a separate treatment-assignment diagram | Selection determines who is represented. Treatment assignment answers a different question. Increasing the selected sample size does not remove the selection rule. |
| Sampling Distributions and the Central Limit Theorem | **Central Limit Theorem**, with the standard-error relationship as supporting notation | For independent, identically distributed observations with finite positive variance, standardized sample means approach a standard normal distribution as sample size grows. The population itself does not become normal. More repetitions reveal the sampling distribution; larger samples change it. |
| Confidence Intervals | `estimate ± margin of error`, expanded into the particular interval formula used in the activity | This summarizes the symmetric interval construction just explored; repeated intervals have a stated coverage under its assumptions. It is not a universal formula for every kind of interval. |
| Hypothesis Tests and p-Values | `p-value = Pₕ₀(result at least as extreme as observed)`, paired with a shaded null-distribution diagram | The probability is computed under the specified null model and chosen extremeness rule; it is not the probability that the null is true. |

Use a running, chapter-local collection of these representations as the recap. In later chapters, reuse familiar symbols and allow their earlier explanation to be reopened. Existing OpenIntro chapters should likewise culminate in meaningful notation when their activities are revised; start from their established formulas and build the experience that makes those formulas legible.

### Acceptance criteria for a culmination

- The preceding activity gives meaning to every essential part of the representation.
- New glyphs receive explicit readings: for example, “x-bar,” “sum,” and “n measurements.”
- A reader can identify which elements belong to the model, the observed data, or an estimate.
- Mathematical conditions and the limits of the compression are stated next to it.
- Mapping symbols to the experiment works with keyboard/touch and text, without relying solely on hover, motion, or color.
- A learner can access the completed representation and explanation without earning a score or running a fixed number of trials.
- The final check includes interpreting or applying the representation, rather than copying its shape.

## New chapter sequence

The terms below are distributed across sections, not introduced in a single opening paragraph.

| Chapter / proposed slug | Main experience | Terms introduced | Understanding check | Deeper chapter |
| --- | --- | --- | --- | --- |
| 1. Probability and Events `chance` | Predict a spinner result, change its colored areas, spin once and then many times. Follow with an independent fair-coin streak example. | Outcome, event, trial, probability, observed frequency, independence | Does a 50% chance promise exactly five heads in ten flips? Does a streak alter the next independent flip? | OpenIntro 3 |
| 2. Random Variables and Distributions `repeated-experiments` | Choose coins per round. Watch one round become one histogram entry, then accumulate many rounds. Compare counts and proportions. | Random variable, frequency, distribution | Explain the difference between more coins per round and more rounds. Transfer to proportions of defective items in batches. | OpenIntro 4 |
| 3. Center and Spread `describing-data` | Inspect a small crowd and its data table; group attributes, move numerical dots, add an extreme salary, and build two datasets with equal means. | Observation, variable, numerical/categorical, mean, median, spread | Choose a useful summary for skewed salaries and explain why equal averages need not describe similar groups. | OpenIntro 1–2 |
| 4. Populations and Samples `samples` | Reveal a sample from a hidden town. Estimate an average, enlarge the sample, then reveal the population and compare. | Population, sample, parameter, statistic, estimate | Identify which number describes the population and which was calculated from the observed sample. | OpenIntro 1, 5 |
| 5. Sampling Bias and Random Assignment `sampling-fairly` | Compare a random town sample with one recruited near a basketball court. Separately, compare self-selected and randomized treatment groups in a simulated study. | Selection bias, random sampling, random assignment, association, confounding | Can a large biased sample remain wrong? Which design helps generalize to a population, and which helps estimate a causal effect? | OpenIntro 1 |
| 6. Sampling Distributions and the Central Limit Theorem `estimates-vary` | Draw a sample, calculate its mean, leave one dot on a second plot, and repeat. Compare sample sizes with fixed axes. | Sampling variability, sampling distribution, standard error | Distinguish the spread of individual heights from the spread of sample means. | OpenIntro 5, 7 |
| 7. Confidence Intervals `intervals` | Generate intervals from repeated samples of a simulated population; reveal the fixed truth and count coverage. Change sample size and confidence level separately. | Confidence interval, confidence level, coverage | Identify what the long-run coverage statement describes; distinguish an interval for a mean from a range of individual values. | OpenIntro 5–7 |
| 8. Hypothesis Tests and p-Values `testing-a-claim` | Observe a suspicious coin, specify a fair-coin model, simulate comparable experiments, and count outcomes at least as extreme. | Null model, test statistic, p-value, significance threshold, false positive | Explain why a small p-value is not the probability that the null is true. Transfer to an A/B comparison. | OpenIntro 5–6 |

Chapter 5 contains two separately introduced activities: sampling and treatment assignment must not become interchangeable in the reader's mental model. Split it into two shorter chapters if beginner sessions show overload.

## Pilot: build the coin experiment first

The first implementation delivers chapters 1 and 2 as a coherent beginner entry point. This exercises the teaching pattern and the user's original coin-distribution idea before expanding the book.

### Chapter 1 experience

- Begin with a spinner whose event area visibly represents a probability. Pair a percentage with the equivalent number from 0 to 1.
- Separate the model setting from the observed result: “Chance of blue: 50%” and “Blue so far: 7 of 10.”
- Offer one spin and a batch of spins. Preserve the accumulated results until reset or a model change.
- Explain that a short run need not match the model. Never promise that every additional trial moves the frequency closer to the probability.
- Use a short independent-coin example for streaks, with feedback that names the independence assumption.
- End with a new context, such as drawing colored counters with replacement.
- Culminate in `P(A) = p`, with the event linked to the spinner region and the probability linked to its size. Keep the observed frequency visibly separate.

### Chapter 2 experience

- Label controls **Coins per round** and **Rounds to run**; introduce them sequentially.
- Animate one small round and show how its head count adds exactly one histogram entry. Large batches update quickly without animating every flip.
- Start with a fixed fair-coin probability. Offer bias changes only after the basic experiment is understood.
- Offer head-count and proportion views with explicit units. For fair independent coins, absolute count spread grows with coins per round while proportion spread shrinks; comparisons must make the unit change clear.
- More rounds estimate the same outcome distribution more clearly; they do not change the theoretical distribution. More coins per round change the distribution being studied.
- When coins per round or coin bias changes, start a clearly labeled new experiment. Never silently pool incompatible results. Preserve a previous run only through an explicit comparison feature.
- Example check: “You keep 10 coins per round and run 1,000 more rounds. What changes?” Feedback distinguishes the underlying distribution from how well its frequencies are represented.
- Assemble `p̂ = X/n` from a completed round's head count and coin count. Let the reader connect that result to its position in the proportion histogram and then use it for a different batch-size example.

### Pilot acceptance criteria

- Every histogram entry corresponds to a complete round, and its frequency total matches the displayed completed-round count.
- Probability 0 and 1 produce the corresponding deterministic outcomes.
- Reset and setting changes leave no stale or mislabeled results.
- Every quiz answer has authored explanatory feedback; correct answers also receive an explanation.
- A reader can skip a prediction, retry a check, or read an explanation without a score gate.
- Keyboard users can operate all controls, receive feedback, and obtain the chart's key information in text.
- The main experience works on a narrow phone screen and in both site themes; reduced-motion preferences are respected.
- Static chapter text still explains the concept when the interactive component has not loaded.
- Each chapter ends with its symbolic culmination, an accessible explanation of the symbols, and a transfer question.

## Feedback and question design

Use two or three well-chosen checks per chapter as an initial editorial target. Place them after substantial ideas, rather than after every paragraph.

- Give each question a named learning objective and each distractor a specific misconception. Avoid trick wording and obviously implausible answers.
- Let a reader choose an answer, then explicitly check it. Show why that answer works or fails, and state the correct principle clearly.
- Allow unlimited retries and an immediate “See explanation” option. Retrying should not hide feedback already received.
- Prefer a nearby “Try it” experiment when it genuinely helps explain an answer.
- Treat predictions as tentative hypotheses. Random outcomes may contradict a sensible prediction; feedback must not grade a probabilistic forecast by whether one run happened to match it.
- Include occasional explanations in the reader's own words, without requiring automated text grading.
- Revisit earlier ideas in later chapters, using changed contexts. Immediate success after feedback is practice, not evidence of lasting learning.
- Use hand-authored feedback for the first version. Accounts, scoring systems, leaderboards, and adaptive tutoring can wait until there is a demonstrated reader need.

## Improving the existing OpenIntro chapters

Add one focused activity to each chapter over time, with a concrete motivating question and explicit links to the beginner sequence. Reuse the same components so related chapters reinforce the same models.

| Existing chapter | Proposed improvement |
| --- | --- |
| 1. Introduction to Data | Crowd/table exploration and sampling-design comparisons; replace illustrative modular-arithmetic selection with valid seeded random sampling. |
| 2. Summarizing Data | Movable dot plot for outliers, center, and spread, with numerical input as an alternative to dragging. |
| 3. Probability | Spinner for events; filtered two-way counts for conditional probability and base rates. |
| 4. Distributions | Repeated-coin experiment and observed-versus-model comparison; retain named distributions as the deeper explanation. |
| 5. Foundations for Inference | Linked population, sample, estimate, and interval views; simulation-based null comparison. |
| 6. Inference for Proportions | A/B experiment varying sample size and effect, with clear assumptions and a decision question. |
| 7. Inference for Means | Paired versus unpaired measurements, with uncertainty visualized. |
| 8. Simple Linear Regression | Adjustable fitted line with residuals and squared-error feedback; show outlier influence. |
| 9. Multiple and Logistic Regression | Compare pooled and group-specific relationships, then a probability curve responding to a predictor. |

Address known content and navigation issues during the relevant phase:

- List chapters 6–9 on the statistics landing page and restore the next link from chapter 5 to chapter 6.
- Verify and correct the OpenIntro links currently pointing to `/book/operating-systems/`, and check source attribution.
- Replace the landing-page bell curve caption that calls a central population range a confidence interval.
- Revise the small-sample mean examples in chapter 5 that use a 1.96 cutoff with an estimated standard deviation. Use an appropriate method and state its assumptions.
- Review blanket claims about causation and observational studies; explain what random assignment provides and where causal assumptions enter.
- Review existing probability and inference definitions as the corresponding activities are added. This is a targeted accuracy pass, not a claim that the current chapters have been comprehensively audited.

## Implementation approach

Use the existing Astro reading site and React integration. Keep prose and navigation in Astro, with independently hydrated React activities. No separate application is needed.

Proposed locations:

- `reading-src/components/statistics/`: activity components and shared question UI.
- `reading-src/lib/statistics/`: pure simulation and summary functions, with injectable random sources for repeatable tests.
- `reading-src/pages/reading/statistics/<slug>/index.astro`: new chapters.
- A small shared chapter manifest if needed to keep the index and previous/next links consistent.

Start with a question component, spinner, coin-round experiment, and a simple symbolic-summary presentation. Keep the symbolic summary statically readable; enhance it with links between the symbols and experiment where useful. Choose accessible equation rendering within the existing site when the first formula needs it. Extract shared chart primitives only when a second activity needs them. Use SVG and accessible text summaries for the initial small charts. Keep rendering deterministic before hydration; generate random outcomes in response to user actions.

Simulation requirements:

- Fresh randomness during normal exploration; seeded or supplied sequences for tests and explicitly labeled replay examples.
- Real random variation, including inconvenient outcomes. Explanations must work without secretly rerolling until the expected lesson appears.
- Explicit distinction between sample size, repetition count, and model parameters.
- Bounded batch sizes, responsive updates, and cancellation if later activities require long runs.
- Sampling procedures appropriate to the scenario, including stated replacement rules.
- Stable scales in comparisons, clear units, visible numerical summaries, and no reliance on color alone.

## Delivery sequence

### Phase 1 — Pilot and entry point (implemented)

Write chapter 1–2 learning objectives, culminating representations, questions, explanations, and behavior tests. Build the feedback component, symbolic summaries, spinner, and repeated-coin experiment. Add the beginner route to the index, list the nine existing chapters, repair chapter navigation, and address the landing-page/source-link issues.

Deliverable: two complete chapters that a beginner can use without programming knowledge.

### Phase 2 — Data and sampling (introductory chapters and initial integration implemented)

Build chapters 3–5, carrying the same town/crowd dataset through description, estimation, and selection bias. Add random-assignment comparison as a separate section. Integrate the resulting activities into OpenIntro 1–2 and correct their affected examples.

Deliverable: a continuous path from probability to describing and collecting data.

### Phase 3 — Inference (introductory chapters and initial integration implemented)

Build chapters 6–8 and integrate the reusable activities into OpenIntro 4–7. Review inference wording, small-sample procedures, interval coverage, and null-model definitions together with the visuals.

Deliverable: a complete beginner route ending at inference, with coherent links into formal methods.

### Phase 4 — Relationships and deeper practice (initial activities implemented; reader refinement pending)

Add conditional-probability activities and the regression interactions for OpenIntro 3, 8, and 9. Add a few later questions that revisit earlier concepts in new contexts. Adjust chapter boundaries and explanations using reader feedback.

Deliverable: the interactive approach extends across the full statistics book.

Each phase should be independently usable. Reassess the next phase after the pilot rather than committing to a large component framework up front.

## Verification and learning evaluation

Follow the repository's test-first approach for implementation: write failing behavior tests, implement the smallest coherent slice, run the relevant checks, then commit the passing slice. The author permits removing new temporary tests after they pass rather than maintaining a test suite for every chapter; retain existing repository tests.

Meaningful automated checks include supplied-random-sequence outcomes, sample-without-replacement uniqueness, histogram accounting, mean/median edge cases, parameter-change resets, and question feedback state. Avoid flaky tests that require an unseeded simulation to land near a target percentage.

Use existing Vitest tooling. Run a TypeScript check for new TS/TSX code and the reading-site build. Confirm available TypeScript/Astro checking tooling during the first implementation slice, since the current package manifest has no explicit typecheck script. Run `pnpm run build:reading` for route/integration validation. Before any dev server, check ports 12345 and 12346.

Manually verify phone layout, keyboard operation, chart summaries, screen-reader feedback, reduced motion, light/dark themes, and chapter navigation. Check that graph axes and language match the underlying model.

For formative evaluation, try the pilot with 3–5 willing readers unfamiliar with statistics. Ask them to think aloud, then answer fresh questions without reopening the explanation. Initial revision signals:

- Can at least 4 of 5 readers distinguish coins per round from number of rounds?
- Can at least 4 of 5 explain why ten fair flips need not split evenly?
- Can readers operate the controls without coaching and interpret what one bar represents?
- Can readers explain `P(A)` and `p̂ = X/n` in their own words and identify their parts in a new example?
- Which terms or feedback messages still require an extra explanation?

These are practical usability targets, not statistically reliable estimates of teaching effectiveness. If possible, revisit one concept with a fresh question several days later. Begin with direct observation; site-wide behavioral analytics are not required for the pilot.

## Research basis

These sources support the design direction; they do not validate this particular book before it is tried with readers.

- [OpenIntro Statistics](https://www.openintro.org/book/os/) and its [simulation-based introductory course](https://www.openintro.org/book/ims/): coverage and sequencing references for the university continuation. New prose and activities are independently authored.
- [ASA GAISE College Report (2016)](https://www.amstat.org/docs/default-source/amstat-documents/gaisecollege_full.pdf): conceptual understanding, purposeful technology, active learning, predictions, and assessment.
- [Carvalho and colleagues: predict–explain–observe–explain](https://www.cmu.edu/teaching/teaching-as-research/carvalho.html): a modest exam benefit in a 75-student psychology-course study; an adaptable pattern rather than direct evidence about this statistics site.
- [Podolefsky, Moore, and Perkins: implicit scaffolding](https://arxiv.org/abs/1306.6544): design framework and interview evidence for using controls, cues, constraints, and feedback to support exploration.
- [Butler and Roediger (2008)](https://link.springer.com/article/10.3758/MC.36.3.604): feedback improves retention and reduces retention of incorrect multiple-choice alternatives.
- [Asher and Carvalho (2026)](https://link.springer.com/article/10.1007/s10648-025-10103-6): practice with feedback in regression learning; explanatory feedback and prior knowledge matter for generalization.
- [Seeing Theory](https://seeing-theory.brown.edu/basic-probability/): a close interaction-design precedent. Use as inspiration, independently authoring the chapters and activities.
- [General Intelligence](../src/content/blog/2026-03-14-general-intelligence.md): the author's requested framing for consolidation and a concluding expression that compresses the preceding argument. An editorial reference, separate from the empirical pedagogy sources.

## Decisions to revisit after the pilot

- Whether the two activities in “Sampling Bias and Random Assignment” need separate chapters.
- Whether readers want optional local progress memory; no account is needed for the proposed path.
- Whether advanced readers prefer embedded code immediately after each activity or in a chapter-end section.
- Whether the introductory route needs further prerequisite explanations for fractions, percentages, or reading graphs.

These decisions now inform reader testing and a later refinement pass. The current implementation is usable locally; publication remains separate.
