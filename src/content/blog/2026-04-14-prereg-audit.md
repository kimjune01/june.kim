---
variant: post-wide
title: "Pre-Registration Audit"
tags: methodology
---

*Part of the [methodology](/methodology) series.*

Every thinker in the [scientific method](/reading/scientific-method/) collection diagnosed a failure mode. A pre-registration that survives all twenty questions has been stress-tested against four centuries of mistakes.

Each question comes from a specific thinker's core insight. The questions are ordered by the arc: empiricists first, then systematizers, falsificationists, causal inference, crisis and repair, and finally the trail. A pre-registration doesn't need to answer every question — but it should know which ones it's skipping and why.

### The questions

| # | Source | Question | What it catches |
|---|--------|----------|-----------------|
| 1 | [Bacon](/reading/scientific-method/bacon-1620/) | Are you observing the phenomenon systematically, or cherry-picking instances that fit? | Idol of the cave: selection bias in your sample |
| 2 | [Bacon](/reading/scientific-method/bacon-1620/) | Is your data collection procedure fixed before you see results? | Idol of the tribe: fitting the method to the outcome |
| 3 | [Descartes](/reading/scientific-method/descartes-1637/) | What are you taking on faith? List every assumption that, if wrong, would invalidate the conclusion. | Unexamined premises hiding behind "obvious" framing |
| 4 | [Hume](/reading/scientific-method/hume-1739/) | What mechanism connects your observations to the general claim? If you only have correlation, say so. | Inductive leap without a causal story |
| 5 | [Hume](/reading/scientific-method/hume-1739/) | Would the conclusion survive if you ran it on a different population? | Generalizing from a selected sample to "the world" |
| 6 | [Mill](/reading/scientific-method/mill-1843/) | Are you varying one thing and holding the rest constant? | Confounded comparisons |
| 7 | [Mill](/reading/scientific-method/mill-1843/) | What is your control? Does it isolate the treatment from "any change at all"? | Missing or inadequate control condition |
| 8 | [Chamberlin](/reading/scientific-method/chamberlin-1890/) | What competing explanations would produce the same result? Are you testing between them? | Confirmation bias: only one hypothesis on the table |
| 9 | [Fisher](/reading/scientific-method/fisher-1935/) | Is assignment to conditions randomized, or could a confound explain the difference? | Systematic bias in treatment assignment |
| 10 | [Popper](/reading/scientific-method/popper-1934/) | What specific observation would make you say "the hypothesis is wrong"? | Unfalsifiable claims dressed as predictions |
| 11 | [Popper](/reading/scientific-method/popper-1934/) | Is the falsification bar high enough to be informative, or is it set where success is easy? | Weak predictions that can't fail |
| 12 | [Kuhn](/reading/scientific-method/kuhn-1962/) | What paradigm are you working inside? What would you be unable to see from within it? | Invisible assumptions of the field |
| 13 | [Platt](/reading/scientific-method/platt-1964/) | Does this experiment exclude at least one alternative, or does every outcome confirm? | Experiments that cannot distinguish between theories |
| 14 | [Feynman](/reading/scientific-method/feynman-1974/) | How would you fool yourself? What's the most likely way the result is an artifact of the method? | Cargo cult rigor: the form of a test without the honesty |
| 15 | [Pearl](/reading/scientific-method/pearl-2000/) | Is your claim causal? If so, what is the intervention, and can you rule out confounders? | Causal language without a causal design |
| 16 | [Ioannidis](/reading/scientific-method/ioannidis-2005/) | Given your sample size, flexibility, and prior probability, what's the chance a positive result is actually true? | Underpowered studies with researcher degrees of freedom |
| 17 | [Mayo](/reading/scientific-method/mayo-2018/) | Could your test pass even if the hypothesis is false? How severe is the test? | Passing an easy test and calling it evidence |
| 18 | [Gwern](/reading/scientific-method/integrity/) | Will you publish the full trail — data, nulls, exclusions, prompt iterations, failed pilots — or only what confirms? | Goodharting the method by curating what's visible |
| 19 | [Gwern](/reading/scientific-method/registered-prediction/) | Are your predictions timestamped and specific enough to be scored? | Vague predictions that can be claimed as correct after the fact |
| 20 | [Ramdas](/reading/scientific-method/ramdas-2023/) | If you plan to peek at results or expand the sample, does your evidence measure remain valid? | Optional stopping and sequential testing without anytime-valid guarantees |

### How to use this

Before registering, walk through all twenty questions with the prereg open. For each one, write down the answer or write "skipped — [reason]." The exercise takes thirty minutes and catches the failures that feel obvious in retrospect.

The questions are not all equal. Questions 10 and 14 (Popper and Feynman) are the most likely to surface fatal problems. Question 8 (Chamberlin) is the most likely to surface alternatives you hadn't considered. Question 18 (Gwern) is the one most often skipped and most often regretted.

A pre-registration that fails question 10 — cannot name what would refute it — is not an experiment. A pre-registration that fails question 18 — won't commit to publishing the full trail — is not trustworthy regardless of how rigorous the design looks.

### The arc, compressed

Bacon: observe, don't speculate. Hume: your observations don't prove what you think. Mill: isolate the cause. Chamberlin: consider alternatives. Popper: name what would refute you. Feynman: name how you'd fool yourself. Pearl: is the causal claim justified? Ioannidis: is the power adequate? Mayo: is the test severe? Gwern: publish the trail.

Each question exists because someone ran an experiment without asking it and got a wrong answer that took decades to correct.

---

*Derived from the [scientific method](/reading/scientific-method/) collection.*
