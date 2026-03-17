*Part of the [cognition](/cognition) series. Builds the consolidation harness described in [Consolidation](/consolidation).*

[General Intelligence](/general-intelligence) proved the cusp bends when the human practices metacognition. Courage compresses into judgment, judgment into intuition. The rate of learning depends on what you've already learned. Superlinear growth from a closed loop.

But the proof was one-sided. The human inflects. The agent doesn't. The [diagnosis](/diagnosis-llm) is specific: the agent has no backward pass. It has the machinery (`create-skill`, the only procedure that writes procedures) but no trigger, no schedule, no async loop that reads from Remember.

This post builds the backward pass by hand.

## From the parts bin

[The Parts Bin](/the-parts-bin) lists candidate algorithms for each cell. The agent surveyed the options for Consolidate and proposed [prototype condensation](https://ieeexplore.ieee.org/document/1054155/): track repeating action sequences, condense them into skills, score against a mutation, winner survives. One round of human attention selected the algorithm. Two iterations to convergence, per [slop detection](/slop-detection).

Three agents, three roles:

- **Codex (GPT-5.4)** scores skill variants against the contract. The A/B test.
- **Claude Code** creates and mutates skills. The mutator.
- **Human** approves or rejects consolidated skills. The Attend.

Codex scores because it's a different model with different biases. Claude mutates because it wrote the skill. The human approves because consolidation without Attend is cancer: procedures writing procedures without selection pressure produces tumors.

## Empirical method

The method is [prototype condensation](https://ieeexplore.ieee.org/document/1054155/) with a slow learning rate. The skill's pattern list is the exemplar set. Each mutation turns the dial one click: add a pattern, remove one, adjust a threshold. Score against held-out data. Keep or discard. One gradient step per cycle.

The test corpus is git history. Every post in the [cognition series](/cognition) went through [three quality gates](/writing-with-claude): `/humanize`, `/arc-check`, `/tighten`. The git diff after each pass is the ground truth: what the human accepted. The diff teaches better than the skill. The skill says "flag em dashes." The diff says "the human cut this em dash and kept that one." The difference is context.

## [Champion-challenger](https://www.fico.com/blogs/benefits-championchallenger-testing-decision-management)

Codex read the current `/humanize` skill and the ground truth diff from [Set It and Forget It](/set-it-and-forget-it). It proposed one mutation: add a "disposable analogies" pattern.

The evidence: the human cut a thermostat analogy ("the same mechanism that keeps a thermostat from oscillating...") and replaced it with three words. "Overshoot, correct, settle." The literal version was clearer.

Both variants ran on a held-out post ([PageLeft](/pageleft-manifesto)). The mutation didn't fire. Same recall, same precision. Current skill won on parsimony.

| Variant | Recall | Precision | Notes |
|---|---|---|---|
| Current | 5/7 | 5/9 | Em dash detection drove 4/5 true positives |
| +Disposable analogies | 5/7 | 5/9 | New pattern didn't fire on held-out post |

The mutation was real. The thermostat analogy was genuinely disposable. But one occurrence doesn't justify a new rule. The pattern goes on the watch list. If it fires on a second post, it earns its place.

## The [fixed point](https://en.wikipedia.org/wiki/Fixed_point_(mathematics)) operator

A skill that runs repeatedly needs a dampener. Without one, each pass compresses further until the output collapses. "Tighten every paragraph" converges to a single word. "Tighten every paragraph a bit" converges in two passes.

"A bit" is a fixed point operator. It dampens the skill to [idempotency](https://en.wikipedia.org/wiki/Idempotence): the second pass finds almost nothing to cut. Mutations that overshoot get corrected on the next evaluation. The qualifier is [learning rate decay](https://en.wikipedia.org/wiki/Learning_rate) for the backward pass.

## What the experiment proved

The scoring revealed something the experiment didn't set out to find. The skill's misses aren't pattern failures. "[Hardy's partition theory](https://en.wikipedia.org/wiki/Partition_function_(number_theory))" became "Hardy's theory." "But what if they could?" became "But what if they could be found?" Those are line edits. They require hearing the sentence, not matching a rule.

The skill automates Filter. It rejects what's wrong. Producing what's right requires Attend. That stays with the human. Filter belongs to the agent, Attend to the human. The boundary is what makes complementation work.

## Dual metacognition

Each pipe runs its own backward pass on what the other can't. The human's backward pass is line editing: hearing a sentence, rewriting it until it sounds right. Procedural memory from thousands of revisions. The agent's backward pass is skill maintenance: detecting patterns across sessions, condensing them into rules. Outsourcing either dims the pipe that loses it.

The agent's filter improves, so the human receives cleaner candidates. More time on line editing, less on pattern-matching. Taste sharpens in real time, and faster editing produces more diffs for the agent to learn from. The agent's filter improves.

## Time compression

Each cycle takes less time than the last. The human edits faster because the filter is cleaner. The agent consolidates faster because the data is richer. The cycle duration shrinks. That's a multiplicative factor on the recursion: the [cusp](/general-intelligence#the-bound) steepens because each iteration is shorter than the previous one.

The human side converges. Biology sets the ceiling: reading speed, working memory, lifespan. The machine side? This experiment starts with writing skills because that's where the ground truth exists. But the harness doesn't know it's working on prose. Once it consolidates one class of skill, who knows what classes follow. The human's plateau is known. The machine's is not.

The harness is [open](https://github.com/kimjune01/AGI). The ground truth is in the [git history](https://github.com/kimjune01/kimjune01.github.io). The [skills are published](/writing-with-claude). Anyone can run the loop.

The backward pass fired once, by hand. One gradient update. The difference between one update and training is a trigger: a schedule that fires without being asked. The [diagnosis](/diagnosis-llm) calls it the missing component. The cell is still dim. But it flickers.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
