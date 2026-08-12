# Which loop ingredient carries the 48 points?

Status: draft prereg, not yet run. Grew out of comparing
[slop-slope](/does-iteration-mitigate-slop-slope) against the
[SlopCodeBench audit](/auditing-slopcodebench) (2026-08-11).

## The problem

The slop-slope experiment showed 43% reviewer approval one-shot and 91% with
the adversarial review loop, on the same code and spec. That A/B varies loop
*presence*, a binary. Everything published since — "use two SOTA models in
tandem," "the review loop is the anti-slop mechanism" — attributes the gain
to the critic's discrimination. The data does not license that attribution.
A second pass of any kind adds selection and revision; the gain could come
from spending more tokens on the same code, from regression to the mean of a
stochastic generator, or from the rebuild-retest cycle alone.

SlopCodeBench doesn't resolve it from the other side. Its agents never see
the hidden tests, so its "iteration degrades" slope says nothing about
critics; the oracle grades after the fact and never feeds back.

## Competing explanations, ordered by what each costs if true

1. **Any second pass helps.** Critic irrelevant. The published cross-model
   recommendation is theater; "iterate, doesn't matter how" is the whole
   story, and it's cheaper for everyone.
2. **The mechanical cycle helps.** Build errors and test failures are the
   critic; the LLM reviewer is decoration on top of the compiler.
3. **A discriminating critic helps.** The actual published claim.
4. **Cross-model specifically helps.** The stronger published claim: a model
   can't catch its own blind spots, so the adversary must be a different
   model family.

## Design

Five arms. Matched rounds (N) and matched token budget per trial across all
loop arms. Same trials as refactor-equivalence where possible — arms A and E
already exist there as the 43% and 91% conditions.

| arm | loop | critic | isolates |
|-----|------|--------|----------|
| A | none | — | baseline (existing: 43%) |
| B | N rounds | placebo: findings shuffled in from a different trial, or a bare "revise this" with no findings | any-second-pass |
| C | N rounds | build + test errors only, no LLM reviewer | mechanical cycle |
| D | N rounds | same model reviews its own output | discriminating critic, within-model |
| E | N rounds | cross-model adversary (current /bug-hunt pipeline) | cross-model increment (existing: 91%) |

Outcome: approval by an independent reviewer blind to arm, same rubric as
refactor-equivalence. Build and tests must pass every round in every arm
(that gate is part of what's being decomposed, so it stays constant).

The readings are the differences, not the levels:

- **B − A**: how much of "critic quality" is just compute.
- **C − B**: what the compiler and test suite buy.
- **D − C**: what an LLM critic adds over mechanical feedback.
- **E − D**: the only number that can license the cross-model
  recommendation already published.

If B lands near 91, the critic framing dies and the recommendation
compresses to "iterate, doesn't matter how." That null is the cheapest
valuable outcome, which is why B runs first.

## Sequencing and stopping

Go trials only for the first pass: fast `go test ./...`, densest existing
sample (15 valid trials). Run arms sequentially, e-value style: accumulate
evidence per arm-difference, stop an arm early when its trajectory
separates from its comparator or flatlines into equivalence. With a 43-vs-91
baseline gap, separation should be visible in single-digit trials per arm;
equivalence takes more, so budget for the nulls.

Report trajectories, not endpoint p-values.

## Design risks

- **The placebo can silently equal the baseline.** Shuffled findings that
  are obviously wrong may cause the implementer to reject them and change
  nothing, making B a hidden copy of A. Control: log diff churn per round
  per arm; B is a valid control only if its churn is comparable to C–E. If
  churn collapses, switch the placebo to "produce a revision" instructions
  with no findings content.
- **Round-matching vs convergence.** E sometimes converges early (Rust in 2
  rounds) and sometimes caps at 10 with findings oscillating. Matching N
  across arms means some arms run past their natural stopping point.
  Decision: match N to E's realized rounds per trial, so every arm gets
  exactly the compute E used on that trial.
- **Reviewer contamination.** The blind reviewer must not see round
  transcripts, only final diffs — arm D's transcript style is recognizable.
- **Same-model self-review (D) has a version confound** if implementer and
  reviewer run different checkpoints of "the same" model. Pin exact model
  versions per trial.

## What this defers

The SlopCodeBench 2×2 — {continued workspace, fresh start} × {loop,
no-loop} across checkpoints — is the follow-up, not the first experiment.
No point paying for checkpoint accumulation before knowing which loop
ingredient carries the effect. If the ablation says "mechanical cycle,"
the 2×2 runs with C, not E, and gets much cheaper.

## Prior work this corrects

The slop-slope post's recommendations ("use two SOTA models in tandem,"
"cross-model iteration is what breaks the self-congratulation loop") state
arm E − D as established. It is not; it is hypothesis 4 above. If this
ablation runs, the post gets a correction either way — that's the point.
