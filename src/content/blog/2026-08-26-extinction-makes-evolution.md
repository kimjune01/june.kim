---
variant: post-medium
title: "Extinction Makes Evolution"
tags: cognition, reading
---

*For [Christopher Alexander](/nature-of-order), my teacher through writing.*

I learned the fundamental process from Christopher Alexander. Not in person. I read [*The Timeless Way of Building*](/timeless-way-of-building) until it changed what I could see.

Alexander's claim was larger than architecture. A living whole cannot be designed all at once. Start with the whole in front of you. Make one change. Let that change differentiate what is already there. Look again. Then make the next change. A building unfolds in time, each step becoming the ground for the step after it.

He was explicit that this was a procedure. Arrange the patterns in a sequence, take them one at a time, and use each to differentiate the result of the patterns before it. At each step there is a partially defined whole and a next pattern to bring to life. [That is the algorithm he gives in Chapter 20](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=375), not a metaphor I have imposed on it.

Years later I met the same process again through computation.

```text
state
  -> make a possible change
  -> test it against the world
  -> keep what works
  -> continue from the changed state
```

In computer science this resembles hill climbing. Begin at the current state, inspect a nearby move, keep the move that improves the result, and repeat. [That is the entire algorithm: a definition of a neighbor and a function that says which state is better](https://www.cs.uni.edu/~schafer/cohort26/FCCS/lessons/week7/topic7a/t7a_r2_hillclimbing.html). The search does not need a finished blueprint. It needs a present state, a way to generate the next move, and a way to judge whether the move is better.

Alexander supplied all three. The existing whole is the state. A pattern generates the move. The quality without a name judges the result. The process continues one pattern at a time.

This is the strongest version of his idea. It is also where I think the blind spot begins.

## The pattern is not the process

A process disappears while it happens. A building remains.

The finished courtyard does not show the alternatives that were rejected, the arguments that changed the plan, the ownership that constrained it, or the mistakes repaired during construction. It shows only the form that survived. Alexander needed a way to transmit the invisible process, so he gave it visible and verbal forms: patterns, centers, buildings, and later the fifteen properties in *The Nature of Order*.

A pattern compresses experience. It names a recurring context, the forces active there, and a configuration that brings those forces into balance. Alexander called the result both a thing and a process: a description of a living arrangement and a rule for generating one. He also insisted that patterns vary by culture and context; a pattern language for a particular building is a sublanguage of the culture around it. [His early account calls each pattern a current best guess that should improve under fresh evidence](https://www.patternlanguage.com/archive/timeless.html).

This was not cargo culting. Alexander did not tell us to copy an alcove because old buildings contain alcoves. He tried to transmit the process by which an alcove becomes right *here*. In Chapter 20 he asks the builder to recall living examples, attend to what made them work, imagine the pattern in the present place, and omit details that belong to later steps. [Pattern and situation interact to generate the particular form](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=380).

But the compression made cargo culting possible. It is easier to copy the visible answer than to recreate the trial that warranted it. The pattern can travel without the climate, labor, law, ownership, failures, and habits that made it work. What began as the memory of a process becomes a catalog of forms.

The pattern is the trail. It is not the search that left the trail.

## The hidden competition

Hill climbing contains a competitive core. Possible moves compete for one irreversible act. Some are never considered. Some are rejected immediately. One receives the time, money, material, and attention to become real.

Alexander leaves most of this competition inside the word *feeling*.

He argues that analytical descriptions of all the forces are too difficult and that extensive experiments are too expensive. His alternative is holistic judgment: people can feel whether a pattern resolves the forces in a situation. He distinguishes feeling from opinion, taste, and abstract argument, and claims striking agreement when people attend to feeling correctly. [Chapter 15 makes this the empirical test of a pattern](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=278).

That judgment may be real. It is not yet a search procedure.

It does not tell us how many alternatives to generate, how different they should be, which uncertainty to test first, which trial would eliminate the most bad paths, or when another trial costs more than it can teach. It does not separate two distinct questions:

```text
Is this move admissible?
Among the admissible moves, which one deserves the next act?
```

Alexander narrows attention to a single pattern and asks the builder to realize it at full intensity. He explicitly warns against thinking about later patterns while making the present one. He then offers a remarkable guarantee: if the language is ordered correctly, later patterns will fit the structure already produced. [There is no need to compromise between patterns, he writes, because each transforms the existing configuration without disturbing its essentials](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=389).

That is an economy of attention: suppress everything except the present pattern. But it is not an economy of search. It assumes that the language has already performed the hard search, that the order is correct, and that every future conflict can be absorbed without invalidating what came before.

Patterns are cached search. They make yesterday's trials cheap to reuse. They do not tell us how to spend today's finite trial budget.

## The inductive leap

Alexander begins with an observation: traditional towns, religious buildings, farmhouses, gardens, and wild places often possess a coherent life absent from much modern construction. He then claims that behind all successful building and growth lies one invariant process, concrete enough to use as a method. [The opening chapter states both the universality and the operational precision of this process](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=23).

The first statement is an observation. The second is an inductive leap.

History is a DAG. Many actual causes converge on a building: climate, available material, craft, law, land ownership, religious practice, household structure, prior failures, trade, war, and accident. Its telling is a linked list: this pattern followed that pattern, one transformation at a time. The list is portable because it leaves most of the graph behind.

[Survivorship bias](https://pmc.ncbi.nlm.nih.gov/articles/PMC9930538/) compresses it again. A surviving form does not show the lineages that vanished, the buildings that collapsed, the customs that were abandoned, or the people who could not reproduce their way of life. Read backward, every surviving center appears to have prepared the next one. The trail looks like a hill climb because the descents that ended a lineage no longer have descendants from which to speak.

The resulting form may indeed have been produced by local trial. But the form alone cannot establish the search algorithm that produced it. Drift, competition, replacement, catastrophe, repair, and changing environments can leave a coherent survivor too.

Alexander saw the trail and reconstructed a procedure. The procedure is powerful. The inductive leap is the claim that it is the timeless invariant behind every living trail.

## He did describe death

The obvious criticism is too easy: Alexander described preservation but forgot death.

It is also false.

Alexander and his collaborators discarded most of the patterns they initially wrote because some were absurd, some failed empirically, and some were replaced by subtler formulations. [He says this directly while recounting the development of their common language](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=320). He later imagines a shared pool in which patterns are exchanged and replaced, good patterns spread, and “bad patterns die out.” Patterns can become rare, disappear, multiply, or enter the pool for the first time. [His language explicitly evolves](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=333).

The omission is subtler. Death appears as an outcome, not as a described mechanism.

Alexander says that people possess criteria for good and bad patterns, so they will copy good ones and decline to copy bad ones. That sentence hides the competitive core. Which people? Exposed to which alternatives? Paying which costs? How does a pattern that already organized a building, an institution, or a pattern language lose its authority? What else must be reconsidered when a foundational pattern dies?

Candidate rejection is easy. Do not build the proposed alcove. Post-consolidation death is harder. A pattern worked, entered the language, shaped later patterns, and became part of the judgment used in subsequent trials. Then the environment changed.

Now there are only two possibilities:

1. Keep the pattern. The process may preserve a structure that now reduces life.
2. Remove the pattern. Everything that depended on it may need to be tested again.

Alexander names disappearance but gives no dependency-aware procedure for it. His language can forget a pattern through declining use. It cannot say what inherited structure must be reopened when that pattern loses its warrant.

This is cache invalidation. A cached answer is useful while the world that warranted it remains stable. When the world changes, speed becomes error.

## Extinction makes evolution

Alexander himself compares the evolution of pattern languages to genetic evolution. Because patterns can change one at a time, he argues, a shared language can improve cumulatively. He places mutation, copying, disappearance, and inheritance in the same passage. [The biological comparison is his](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=333).

Natural selection is not merely an analogy here. It is an actual process of variation, inheritance, and differential reproduction. Organisms produce more variation than an environment can sustain; inherited differences affect which lineages contribute to the next generation. [The National Academies gives the elementary account as variation followed by selection through differential survival and reproduction](https://www.nationalacademies.org/read/5787/chapter/7).

Strictly, evolution does not require every loser to die, and natural selection is defined more precisely by differential reproduction than literal death. But extinction is not an accident outside evolution. It changes what evolution can subsequently explore. Removing established taxa opens vacancies in ecological space and can enable adaptive radiation among lineages that were previously marginal. [This effect is documented across mass extinctions](https://www.nature.com/articles/s41467-017-00827-7), and experimental work shows that an established specialist can suppress later diversification simply by arriving first. [History changes the available search space](https://www.nature.com/articles/nature05629).

Inheritance lets evolution remember. Extinction keeps that memory from occupying every niche forever.

This is the counterclaim to Alexander's emphasis on structure preservation:

> Extinction makes evolution.

Not by itself. Variation without inheritance cannot compound. Inheritance without selection cannot adapt. But preservation alone is not life. An established form may need to disappear before a previously suppressed form can unfold.

Death does not merely clean up after the process. It changes the next search.

## The theory's own trial

The omission returns at the level of the theory.

Critics of Alexander have repeatedly challenged his movement between subjective feeling and objective fact, the limited testing behind many patterns, the claim to one right way of building, and the tendency for his judgment to override other users' preferences. They have also observed that living places can be made without his patterns and dead places can be made with them. [Dawes and Ostwald organize twenty-eight published criticisms across the conception, documentation, and implementation of his middle-period theory](https://link.springer.com/article/10.1186/s40410-017-0073-1).

These criticisms converge on a problem of falsification. If a design succeeds, it supports the process. If it fails, the execution may have been weak, the pattern may have lacked intensity, the users may have answered with opinion instead of feeling, or modern institutions may have prevented the process from operating. Any of these explanations may be true. But if one is always available, what result would make the governing theory lose?

The reductio is short.

1. A living process must remain answerable to trial.
2. The fundamental process claims to describe how living order is made.
3. If no trial can invalidate the process itself, the process is no longer answerable to its environment.
4. By its own standard, a theory of living order that cannot die is not living.

This does not prove Alexander wrong. It identifies an interface he left hidden. He described a procedure for applying patterns and a social process in which bad patterns disappear. He did not specify the competitive test by which the procedure, its criteria, or its theory should lose warrant.

The fundamental process operates on the building. It must also operate on the process.

## What I inherited

I inherited much of Alexander's stubbornness.

It is easy to see why. He teaches the reader to trust direct perception against systems that have forgotten life. That stubbornness can keep a weak, unfamiliar signal alive long enough to be tested. Without it, every new idea dies under the authority of whatever already occupies the field.

The same stubbornness can protect an established idea from the trial it demands of everything else. A failed test becomes evidence that the tester lacks taste. An institutional constraint becomes lifeless bureaucracy. A criticism becomes proof that the critic cannot see.

I do not want to discard the stubbornness. I want to move it: from preserving conclusions to preserving the process that can replace them.

Alexander made an invisible process visible through buildings. He showed me that order unfolds from a present whole through local acts, and that the history of successful acts can be compressed into patterns and transmitted. Computation showed me the machinery hidden inside trial: finite search, competing alternatives, attention, cached results, dependency, and invalidation. Evolution showed me what accumulated life leaves out when it tells only the story of its survivors.

Alexander taught me how life preserves form. Following his process led me to its counterpart: life remains alive by allowing its forms, its patterns, and even its theories to die.
