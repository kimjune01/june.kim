---
variant: post-wide
title: "The Prereg Checklist"
tags: methodology
---

*Part of the [methodology](/methodology) series.*

Every thinker in the [scientific method](/reading/scientific-method/) collection diagnosed a failure mode. A pre-registration that survives all twenty-two questions has been stress-tested against four centuries of mistakes.

This is written for humans and agents. An agent running an investigation should answer these questions before it touches the data, changes a prompt, expands a sample, or summarizes results. The point is not ceremony; it is to prevent the investigation from becoming adaptive in ways the final report hides.

Each question comes from a thinker's core insight, ordered by the arc: empiricists first, then systematizers, falsificationists, causal inference, crisis and repair, and finally the trail. A pre-registration doesn't need to answer every question, but every skipped question should be marked with a reason.

### The questions

| # | Source | Question | What it catches |
|---|--------|----------|-----------------|
| 1 | [Bacon](/reading/scientific-method/bacon-1620/) | Are you observing the phenomenon systematically, or cherry-picking instances that fit? | Idol of the cave: selection bias in your sample |
| 2 | [Bacon](/reading/scientific-method/bacon-1620/) | Is your data collection procedure fixed before you see results? | Idol of the tribe: fitting the method to the outcome |
| 3 | [Descartes](/reading/scientific-method/descartes-1637/) | What assumptions, if false, would invalidate the conclusion? | Unexamined premises hiding behind "obvious" framing |
| 4 | [Hume](/reading/scientific-method/hume-1739/) | What mechanism connects your observations to the general claim? If you only have correlation, say so. | Inductive leap without a causal story |
| 5 | [Hume](/reading/scientific-method/hume-1739/) | Would the conclusion survive on a different population, dataset, task distribution, or environment? | Generalizing from a selected sample to "the world" |
| 6 | [Mill](/reading/scientific-method/mill-1843/) | Are you varying one thing and holding the rest constant? | Confounded comparisons |
| 7 | [Mill](/reading/scientific-method/mill-1843/) | What is your control? Does it isolate the treatment from "any change at all"? | Missing or inadequate control condition |
| 8 | [Chamberlin](/reading/scientific-method/chamberlin-1890/) | What competing explanations would produce the same result? Are you testing between them? | Confirmation bias: only one hypothesis on the table |
| 9 | [Peirce](/reading/scientific-method/peirce-1878/) | Did the hypothesis come before the data, or did you infer it from the same observations you're now using as evidence? | Abductive retrofit: generating and "confirming" on the same dataset |
| 10 | [Fisher](/reading/scientific-method/fisher-1935/) | Is assignment to conditions randomized, or could a confound explain the difference? | Systematic bias in treatment assignment |
| 11 | [Popper](/reading/scientific-method/popper-1934/) | What specific observation would make you say "the hypothesis is wrong"? | Unfalsifiable claims dressed as predictions |
| 12 | [Popper](/reading/scientific-method/popper-1934/) | Is the falsification bar high enough to be informative, or is it set where success is easy? | Weak predictions that can't fail |
| 13 | [Kuhn](/reading/scientific-method/kuhn-1962/) | What assumptions does your field, benchmark, or task definition make invisible? What result would they prevent you from noticing? | Invisible assumptions of the field |
| 14 | [Platt](/reading/scientific-method/platt-1964/) | Does this experiment exclude at least one alternative, or does every outcome confirm? | Experiments that cannot distinguish between theories |
| 15 | [Meehl](/reading/scientific-method/meehl-1967/) | Is your prediction specific enough that more data makes the test harder, not easier? | The crud factor: in soft domains, everything correlates with everything, so directional predictions succeed trivially at scale |
| 16 | [Feynman](/reading/scientific-method/feynman-1974/) | How would you fool yourself? What's the most likely way the result is an artifact of the method? | Cargo cult rigor: the form of a test without the honesty |
| 17 | [Pearl](/reading/scientific-method/pearl-2000/) | Is your claim causal? If so, what is the intervention, and can you rule out confounders? | Causal language without a causal design |
| 18 | [Ioannidis](/reading/scientific-method/ioannidis-2005/) | Given your sample size, flexibility, and prior probability, what's the chance a positive result is actually true? | Underpowered studies with researcher degrees of freedom |
| 19 | [Mayo](/reading/scientific-method/mayo-2018/) | Could your test pass even if the hypothesis is false? How severe is the test? | Passing an easy test and calling it evidence |
| 20 | [Gwern](/reading/scientific-method/integrity/) | Will you publish the full trail — data, nulls, exclusions, prompt iterations, failed pilots, scoring changes, analysis forks — or only what confirms? | Goodharting the method by curating what's visible |
| 21 | [Gwern](/reading/scientific-method/registered-prediction/) | Are your predictions timestamped and specific enough to be scored? | Vague predictions that can be claimed as correct after the fact |
| 22 | [Ramdas](/reading/scientific-method/ramdas-2023/) | If you plan to peek at results or expand the sample, does your evidence measure remain valid? | Optional stopping and sequential testing without anytime-valid guarantees |

### How to use this

Before registering, walk through all twenty-two questions with the prereg open. For each one, write down the answer or write "skipped — [reason]." The exercise takes thirty minutes and catches the failures that feel obvious in retrospect.

Not all questions are equal. Questions 11 and 16 (Popper and Feynman) are the most likely to surface fatal problems. For alternatives you hadn't considered, question 8 (Chamberlin) is the sharpest. Question 9 (Peirce) catches the most common form of self-deception: inferring a hypothesis from the data and then "confirming" it on the same data. Question 15 (Meehl) catches tests that get easier with more data — the opposite of what a good test does. Question 20 (Gwern) is the one most often skipped and most often regretted.

A pre-registration that cannot name what would refute the hypothesis is not registering an experiment; it is registering a story. One that won't publish the trail is asking readers to trust the part least deserving of trust: the filtered final narrative.

### The arc, compressed

Bacon: observe, don't speculate. Hume: your observations don't prove what you think. Mill: isolate the cause. Chamberlin: consider alternatives. Peirce: did the hypothesis come before the data? Popper: name what would refute you. Meehl: is your prediction specific enough that scale makes the test harder? Feynman: name how you'd fool yourself. Pearl: is the causal claim justified? Ioannidis: is the power adequate? Mayo: is the test severe? Gwern: publish the trail.

Each exists because someone skipped it, got a wrong answer, and spent decades correcting the mistake.

---

*Derived from the [scientific method](/reading/scientific-method/) collection.*
