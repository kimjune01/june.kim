---
variant: post-medium
title: "The Spark Did It"
tags: cognition, methodology
---

A spark starts a wildfire.

We find the campfire, power line, cigarette, or machine that threw it. Now we know the cause. Assign fault, remove the ignition source, and prevent the same spark next time.

The account is not wrong. Without that spark, this fire may not have started at that moment.

But the same spark fell yesterday and went out.

The spark explains the timing. It does not explain the scale.

~~~text
ignition
  + dry fuel
  + accumulated brush
  + wind
  + terrain
  + combustible buildings
  + constrained evacuation
  + limited response capacity
  → disaster
~~~

Calling the spark *the cause* compresses this field into its final visible event. The last edge in the graph receives the explanatory weight of the whole graph.

That compression suggests a response:

~~~text
spark → fire → extinguish it
~~~

The response works. Flames disappear. People and buildings survive. The next fire receives the same response, and it works again. Each success makes suppression more reasonable.

This is where the trouble begins.

## It keeps working

Induction is one of the cheapest ways to learn.

When a situation resembles one we have encountered, repeat the action that worked. We do not need a complete causal model. We need only recognize enough of the situation to retrieve a response.

The response crosses between agents just as cheaply:

> When you see fire, put it out.

A firefighter can teach it to a recruit. A manager can write it into policy. A generation can inherit it from the one before. The original fire, rejected alternatives, and surrounding conditions do not need to cross the channel. The trigger and action are enough.

Bayesian inference strengthens the lesson. If suppression repeatedly prevents immediate loss, another success should increase our confidence that suppression will prevent immediate loss again:

~~~text
P(suppression works | visible fire) goes up
~~~

This is a rational update. The observations are real.

But it is easy to update a stronger claim without noticing:

~~~text
P(fire is the problem | visible fire) goes up
~~~

The first claim concerns a response. The second concerns a cause.

Fire may be the present danger while also being part of the system that prevented a worse future danger. In some ecosystems, frequent low-intensity fires reduce accumulated fuel. Suppressing them can allow dense vegetation and dead material to build. The National Park Service now describes how excluding fire altered Yosemite's forests and could make later fires more severe. Its current practice combines suppression near people and infrastructure with prescribed fire and managed wildfire where conditions permit ([NPS](https://www.nps.gov/yose/learn/nature/fireecology.htm)).

The earlier response still worked. Repeating it changed what the next fire would mean.

That is what makes the error difficult to see. There is no obviously foolish decision. No update is necessarily irrational. The fire goes out, the evidence favors the response, and the policy earns another success.

It works until a hidden difference matters.

## Facsimile response

I call this a **facsimile response**.

One agent encounters a situation, acts, and obtains an acceptable result. Another agent does not receive the situation itself. It receives a representation: a story, example, rule, pattern, policy, or demonstration. The second agent recognizes the representation and reproduces the response.

~~~text
original situation → response → outcome
          ↓ lossy transmission
represented situation → copied response
~~~

The same agent can do this across time. Memory transmits a compressed situation to a future self.

Facsimile response is not a defect. We would be helpless if every person had to rediscover every action from first principles. It is fast, transmissible, and often correct. Its danger comes from the same economy: the response crosses the boundary more easily than its warrant.

What survives is visible: there was a spark, there was a fire, and suppression stopped it. What disappears is the causal neighborhood: how much fuel was present, why it accumulated, what the fire would have done, which people and structures were exposed, and whether suppression changes the next fire.

A facsimile response matches on the information that survived transmission. Resemblance substitutes for the omitted causes.

This is the inductive leap—not learning from repetition, but allowing the success of a response to stand in for knowledge of its cause.

## The same event, another cause

The same visible event can be produced by different causal graphs.

One fire spreads because high winds carry embers. Another spreads through dense ground fuel. Another moves from house to house because the structures themselves burn. All present as flames. All initially call for water, evacuation, and containment. The emergency response need not settle the difference before acting.

Remediation does.

I have previously separated [response, recovery, and remediation](/remediation):

~~~text
response     → stop the present failure
recovery     → restore the previous state
remediation  → alter the next situation
~~~

Response can operate on the visible event. Remediation must identify which relations produced its scale. Otherwise we rebuild the same conditions, improve our ability to suppress the same symptom, and call ourselves safer.

Finding a cause outside the established model requires abduction. Bayesian inference reallocates confidence among causes the model already represents. Abduction proposes that the hypothesis space is incomplete:

~~~text
Bayesian inference:
Which known cause is now more likely?

Abduction:
What cause have we not represented?
~~~

If the missing cause has a low but nonzero prior, evidence can revive it through ordinary updating. If it is absent from the model, no amount of updating within that model can discover it. The unexplained remainder must first be preserved long enough for someone to name another possibility.

That is socially expensive. A new cause does not merely compete with an established explanation. It implies that earlier successes may have been misread. For people whose competence, authority, or identity rests on that explanation, the proposal can feel less like a hypothesis than an accusation.

Dismissal is cheap. Abduction needs institutional help.

## Give doubt a job

The old office of the devil's advocate is one such design.

Its official name was the **Promoter of the Faith**, formalized under Pope Sixtus V in 1587 for canonization proceedings. The officer prepared arguments against raising a candidate to sainthood, including apparently slight objections. Admiration, testimony, institutional momentum, and shared belief all pushed toward assent; the Church gave resistance an office ([Catholic Encyclopedia](https://www.newadvent.org/cathen/01168b.htm)).

This was historically a juridical adversary, not a philosopher of abduction. But its most useful function was larger than opposition. It authorized someone to ask whether the same evidence admitted another cause without requiring personal disloyalty to the community.

Adversarial review asks:

> Is this conclusion supported?

Abductive review also asks:

> What else could have produced this evidence?

A devil's advocate should not merely argue that the spark was elsewhere. The role should introduce a missing branch into the causal graph.

## Preserve the graph

Alternative causes are cheap to invent and mostly wrong. Institutional permission to propose them is not enough. Their claimed relations must be exposed to evidence.

Accident investigation supplies another organizational form. After Columbia was destroyed, its investigation board did not stop at the foam strike that breached the shuttle's wing. It examined budgets, schedule pressure, communication barriers, organizational history, and reliance on past success instead of testing. The board wrote that NASA's management practices were as much a cause of the accident as the foam ([CAIB report](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20030066167.pdf)).

The point was not to replace one root cause with another. It was to recover a causal graph:

~~~text
foam strike → breach → loss during re-entry

past safe returns ────────┐
schedule and cost pressure ├→ acceptance of foam risk
communication barriers ───┘
~~~

The physical chain explains how the vehicle failed. The organizational branches explain why that chain was allowed to remain possible.

An investigation protects this work by separating it from immediate response. Firefighters must suppress the fire; investigators must preserve evidence that suppression and cleanup would otherwise destroy. Operational leaders must restore service; an independent reviewer needs permission to question the policies, incentives, and prior successes of those same leaders.

Independence does not make the resulting graph true. It keeps some candidate edges from being removed for operational or social convenience.

## Verify the edges

A causal diagram can become another persuasive story. Drawing more arrows is not remediation.

Each important edge needs an observation that could disagree with it:

~~~text
Does reducing ground fuel change fire intensity?
Do different building materials change propagation?
Does prescribed burning reduce later fuel without causing another harm?
Does suppression here protect people without increasing future exposure?
~~~

The National Park Service's fire-monitoring program shows the shape of the work. Teams measure plots before and after prescribed burns, follow them over time, and sometimes use untreated control plots to distinguish fire effects from climate, moisture, grazing, and other causes. The agency's handbook explicitly recommends controls when managers need to attribute an observed change to prescribed fire rather than another factor ([NPS Fire Monitoring Handbook](https://www.nps.gov/orgs/1965/upload/fire-effects-monitoring-handbook.pdf)).

The trial does not need to reproduce a catastrophic wildfire. It needs to test one consequential relation cheaply enough to improve the next decision.

That is economy of search:

> What is the smallest action that could tell us this edge is wrong?

Proxies are unavoidable. Fuel depth is not community survival. A monitoring plot is not a forest. A controlled burn is not a wind-driven urban fire. The test earns bounded influence, not authority. Its value is that different people can run it, compare results, and learn where the relationship stops holding.

## Beyond the spark

An organization capable of remediation needs several distinct acts:

1. **Respond** to the visible danger without pretending the response explains it.
2. **Preserve** evidence that recovery would erase.
3. **Authorize abduction** so causes outside the established model can enter.
4. **Map the causal graph** rather than crown a single root cause.
5. **Verify important edges** with the cheapest discriminating trials available.
6. **Change the substrate** and observe what the change does over time.

None of this discounts induction. Facsimile response remains the economical default. Put out the fire. Reuse what worked. Trust accumulated experience enough to act.

Just do not mistake the success of suppression for an explanation of combustion.

The spark starts the fire. The landscape makes it a disaster.
