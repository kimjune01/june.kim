---
variant: post-medium
title: "Facsimile Response"
tags: cognition, methodology
---

My grandmother tells me never to open the oven while the cake is rising.

She learned to bake with an oven that lost heat quickly. Opening its heavy door at the wrong moment could collapse the cake. I inherit the instruction but not the oven. It arrives intact, long after the condition that produced it has disappeared.

The instruction still sounds reasonable. Opening the door accomplishes nothing. Waiting costs little. The cakes come out fine. Every success appears to confirm the rule.

At work, an alert wakes an engineer. She restarts the service and the alert clears. The next engineer finds the command in a runbook:

```text
When this alert fires, restart the service.
```

The runbook does not contain the afternoon when the first engineer traced the problem to a memory leak. It does not say which version was running, what traffic looked like, or which other fixes she considered. The situation and its explanation have been compressed into a trigger and a response.

Months later the same alert begins firing for a different reason. The restart still clears it temporarily. Automation makes the response faster and more reliable while the underlying fault compounds.

Nothing irrational has happened. Each person followed evidence inherited from someone with more direct experience.

## From example to rule

The same compression appears in hiring.

A manager hires three excellent people from the same university. The university becomes a positive signal. Other managers adopt it because the first manager has a strong team. Eventually the company recruits there deliberately, interviews more of its graduates, and hires more of them.

The result is now everywhere: successful employees keep coming from the university.

What traveled between managers was easy to transmit:

> Graduates from here do well.

What did not travel was harder to state. Perhaps one recruiter had learned where the strongest students gathered. Perhaps the first three shared a professor, an internship, or a reason for joining this particular company. Perhaps the manager was unusually good at developing junior employees. The visible attribute crossed the boundary. Its causal neighborhood did not.

Then the rule changes the evidence available to the company. Fewer candidates from elsewhere receive interviews. The organization cannot observe the performance of people it never hired. Repetition makes the original inference appear increasingly empirical because the inference now produces the population used to confirm it.

## Success can hide damage

Sometimes the response changes its environment slowly enough that its early successes are real.

For much of the twentieth century, a fire was something to extinguish. Each suppression protected trees, buildings, and people that day. But frequent fire is part of some ecosystems. Excluding it can allow dense vegetation and dead fuel to accumulate. The National Park Service now describes how suppressing all fires in Yosemite changed forests and could make later fires more severe; its current practice includes prescribed fire and managed wildfire alongside suppression ([NPS](https://www.nps.gov/yose/learn/nature/fireecology.htm)).

```text
fire → suppress it → immediate danger falls
```

The response worked. Repeating it changed what fire would mean next time.

The space shuttle program produced a more concentrated version of the same failure. Foam had struck shuttles on earlier flights without destroying them. The mission returned; the anomaly became familiar; continued success made the risk feel bounded. The Columbia Accident Investigation Board later treated this normalization of deviance as part of the organizational history of the disaster. Its report found that a foam strike was the accident's direct physical cause and examined how earlier anomalies had become accepted ([CAIB report](https://sma.nasa.gov/SignificantIncidents/assets/columbia-accident-investigation-board-report-volume-1.pdf)).

The lesson is not that the engineers lacked evidence. They had repeated observations:

```text
foam strike → shuttle returns
foam strike → shuttle returns
foam strike → shuttle returns
```

The observations were true. Their compression was fatal.

No single repetition announces that a boundary has been crossed. The next cake rises. The service recovers. The graduate performs well. The fire goes out. The shuttle returns.

The action looks most reasonable immediately before it fails.

## Facsimile response

I call this a **facsimile response**.

One agent encounters a situation, acts, and obtains an acceptable result. Another agent does not receive the original situation. It receives a representation: a story, example, rule, pattern, policy, demonstration, or runbook. The second agent recognizes the representation and reproduces the response.

```text
original situation → response → outcome
          ↓ lossy transmission
represented situation → copied response
```

The copied action is not a perfect copy either. It is an executable likeness, containing enough of the earlier act to repeat it somewhere else.

This may be the cheapest useful compression available between agents:

> When it looks like this, do what worked before.

No causal model must be shared. The receiver need not understand the original search, rejected alternatives, local constraints, or mechanism. Recognition and imitation are enough.

Most of the time, that is a feature.

We would be helpless if every cook had to rediscover baking chemistry, every engineer had to rediscover the service, and every child had to personally test which warnings deserve attention. Induction lets finite creatures reuse experience. Facsimile response lets that experience cross agent boundaries through channels too narrow for its full history.

The danger is not that the response is unreasonable. The danger is that its misuse looks exactly like its proper use.

## The invisible boundary

Every compressed response has a domain in which it remains useful. But the compression rarely contains a complete description of that domain. If it did, it might cost as much to transmit as the experience it replaced.

The receiver therefore matches on what survived the channel:

- the cake is rising;
- the alert has this name;
- the candidate attended this university;
- there is a fire;
- foam struck the shuttle.

Resemblance substitutes for the omitted causal structure.

When the hidden conditions remain stable, the response keeps working. When they change, the receiver cannot necessarily tell. The old oven and the new oven present the same cake. A memory leak and a deadlocked dependency can produce the same alert. Two candidates can share a university without sharing what made the earlier hires succeed.

Worse, repetition may suppress the evidence that could expose the difference. Nobody opens the oven. Nobody leaves the service running long enough to diagnose it. Nobody hires the counterexample. Every successful response strengthens the association while narrowing the opportunity to learn whether something else would have worked.

This is where induction becomes an inductive leap. Not when we learn from repetition, but when the repeated response becomes evidence that the compressed conditions still hold.

> A facsimile response copies what survived while discarding the conditions that made it work.

## Trial is not the alternative

The answer is not to reject inherited responses and test everything ourselves.

That would discard the economy that made the response valuable. Trials cost time, attention, material, and sometimes lives. Many actions are irreversible. We cannot build two bridges and collapse one, run a second childhood, or replay five years of a company under another strategy.

The common objection to iteration begins here: trial is too expensive.

But this assumes that the trial must be the size of the final decision. Usually we need something smaller. Not proof of the whole theory—just an observation capable of changing the next action.

Before changing the commute, leave fifteen minutes later twice. Before rewriting the service, replace one boundary. Before expanding the hiring rule, hide university names from a sample. Before rearranging a public room, move loose chairs and watch where people return them. Before preserving the recipe, bake two spoonfuls of batter.

The question is not:

> Can we afford to test the whole decision?

It is:

> What is the smallest action that could tell us this situation is not the old one?

This is economy of search. The facsimile response remains the default. A cheap trial checks its boundary.

## Buy disagreement

The observation will usually be a proxy. Chair movement is not belonging. Interview performance is not future contribution. Test coverage is not correctness. Felt confidence is not safety.

That is enough. A proxy need not decide the question. It only needs to discriminate cheaply between possibilities that imply different next actions.

The trick is to remember that the eval is another compression. Optimize it hard enough and it can separate from what we care about—the family of failures described by [Goodhart's law](https://arxiv.org/abs/1803.04585). The proxy needs [a leash](/the-leash): limited authority, occasional comparison with later outcomes, and a stopping point.

An individual feeling can also be a cheap proxy. Shared feeling is expensive. A community must assemble attention, language, discussion, status negotiation, and some treatment of disagreement. It cannot convene over every inherited response or proposed alternative.

Reusable evals amortize that judgment. Many agents can run a cheap check independently, reserving communal attention for results that are ambiguous, consequential, or surprising. The eval does not replace judgment. It decides where expensive judgment may be worth buying.

The attitude is neither “repeat the rule” nor “question everything.” Both waste information. It is:

> Use the inherited response, then spend some of its savings on the cheapest useful disagreement with it.

Often the rule wins. Good—the compression remains useful. Sometimes it loses before a larger commitment. Better. And sometimes the world reveals a difference that neither the inherited response nor its critic represented. That is the fruitful result: contact with the world has enlarged the vocabulary of the search.

Induction deserves its place as one of our cheapest ways to learn and transmit action. Its danger comes from the same economy. The response crosses between agents more easily than its warrant.

So keep the recipe, the runbook, the pattern, and the rule. Just leave enough slack for the present situation to say that it is not a facsimile of the past.
