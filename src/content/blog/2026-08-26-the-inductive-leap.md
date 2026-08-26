---
variant: post-medium
title: "The Inductive Leap"
tags: cognition, methodology
---

You try something. It works. You try it again. It works again. Soon you stop calling it a trial and start calling it a rule.

This is usually reasonable. I take the same route to work because it has usually been fast. I salt the onions before the tomatoes because the dish has usually turned out better. I put the important sentence first because readers have usually stayed with me. Experience would be useless if it could not travel from one situation to the next.

The trouble begins when a memory of success becomes a claim about necessity.

```text
This worked here.
This has worked often.
This is how it works.
This is how it must work.
```

Each sentence is only a little stronger than the one before it. The distance accumulates quietly. By the last sentence, a trail through the world has become a law governing the world.

I call that distance the inductive leap.

## Induction is compression

Induction is not a mistake. It is how finite creatures reuse experience.

The world presents more cases than anyone can remember. We compress them: this restaurant is reliable, this interview question is revealing, this library is well designed, this kind of apology works. The compressed rule lets us act without reopening the entire history that produced it.

That is its virtue. It is also its loss.

The rule does not carry every condition of its successes. My route was fast during summer, before the school reopened. The onions tasted better in three dishes cooked with the same pan. The opening sentence helped essays selected by the same audience. Compression drops context so that a lesson can travel.

History compounds the loss. We usually encounter the practices that persisted, the companies that survived, the buildings still standing, and the advice remembered by people for whom it worked. Failures leave fewer descendants and fewer advocates. This is [survivorship bias](https://pmc.ncbi.nlm.nih.gov/articles/PMC9930538/): selecting on survival can make a trait associated with persistence look like its cause.

Read backward, a survivor's path looks unusually sensible. Each choice seems to prepare the next. But history is not a single path. Many causes converge on every outcome, while many nearby attempts disappear before they can enter the story. The visible trail may be evidence for a good procedure. It is not the procedure itself.

Induction compresses the trail. The leap forgets that it was compressed.

## The ordinary leap

The leap rarely announces itself as philosophy. It appears in ordinary advice.

A manager hires three excellent employees from the same university and adds the university to the hiring rubric. A team ships two successful features after long planning cycles and concludes that planning produced the success. A cook follows a grandmother's recipe exactly because every deviation is said to ruin it. A programmer survives one painful rewrite and declares that rewrites always fail.

Each belief contains evidence. None identifies the cause by itself.

The university may have supplied good candidates, or one recruiter may have known how to find them there. Planning may have helped, or the successful projects may have been the only ones important enough to receive long planning. The recipe may encode chemical constraints, or it may preserve ingredients that disappeared two generations ago. The rewrite may have failed because of its size rather than because replacement is inherently worse than repair.

The leap turns a result into an explanation. Once the explanation settles into practice, it also changes what can be observed. The hiring rubric produces more graduates from that university. The planning process attaches itself to every important project. Nobody cooks the forbidden variation. Nobody attempts a small rewrite.

The rule then appears to confirm itself because it has suppressed its alternatives.

## Trial is said to be expensive

Whenever I propose iteration, someone objects that trial is expensive.

Often it is. We cannot build two bridges and collapse one. We cannot run a second childhood with different parents. A company cannot replay the same five years under another strategy. Irreversible actions deserve more care than a slogan about experimentation can provide.

But this objection quietly assumes that the trial must be the size of the final decision.

A trial need not reproduce the entire outcome. It needs to distinguish between the explanations that would change the next action.

Before changing the commute, leave fifteen minutes later on two ordinary mornings. Before rewriting the service, replace one boundary and observe what breaks. Before adopting the hiring rule, hide the university names from a batch of applications. Before doubling a recipe, cook two spoonfuls with different ratios. Before rearranging a public room, move loose chairs and watch where people put them back.

None of these trials proves a universal claim. That is not their job. Each purchases a small amount of information before a larger commitment.

The relevant question is not:

> Can we afford to test the whole decision?

It is:

> What is the smallest action that would make us choose differently?

This is economy of search. A good trial is not merely cheap. It is discriminating: different live explanations predict different observations. If every possible result leaves the decision unchanged, the trial is ceremony. If one small result can kill an expensive path, the trial may be worth much more than it costs.

## Trials are fruitful

We often describe trials as verification. First produce the idea; then check whether it works.

That understates their value. A trial can reveal a dimension that the idea did not contain.

Move the chairs and discover that the problem was glare, not distance. Mask the university and discover that reviewers infer prestige from internships instead. Replace one software boundary and discover that the supposed module shares a database transaction with four others. Change the recipe and discover that everyone was preserving the old order because one obsolete stove heated unevenly.

The result does more than accept or reject a proposal. It changes the space of proposals.

This is the fruitfulness of trial: the world can answer in vocabulary we did not supply. Deduction cannot do that from inside a fixed model. Induction can suggest where to look, but another summary of past cases still inherits their categories. Contact with the world can produce a new distinction.

That is why I resist replacing trials with confidence, experience, or consensus. Those are useful caches of earlier contact. They are not new contact.

## A proxy is enough

The cheap observation will rarely be the thing we ultimately care about.

Chair movement is not belonging. Interview performance is not future contribution. Click-through is not reader understanding. Test coverage is not software correctness. These are proxies: observable signals that sometimes move with a harder objective.

A proxy does not need to decide the question to be useful. It only needs to change our odds cheaply enough to improve the next choice.

The trick is remembering what it is.

Optimize a proxy hard enough and it can separate from its objective. This is the family of failures commonly gathered under [Goodhart's law](https://arxiv.org/abs/1803.04585). Empirical work on learned reward models finds the same hump: optimizing the proxy initially improves the intended result, then eventually makes it worse as optimization travels beyond the region where the relationship was learned ([Gao et al., 2023](https://arxiv.org/abs/2210.10760)). I have called the necessary bound [the leash](/the-leash).

Feeling is a proxy too. So are expert judgment, community agreement, a customer survey, and a unit test. Calling one subjective and another objective hides their common structure. The useful differences are operational: What does the signal cost? Can different people obtain it independently? Does it still correlate with later outcomes? What would make us stop trusting it?

An individual impression may be nearly free. A shared impression is not. To discover how a community feels, its members must attend, discuss, negotiate status and language, and somehow aggregate disagreement. A community cannot convene over every candidate it might reject.

A reusable eval amortizes some of that judgment. The community pays to define an imperfect test; many people can then run it independently before consuming communal attention. The eval should filter or rank candidates, not declare truth. Ambiguous and consequential decisions can still rise to slower judgment.

Cheap proxies make more trials possible. The leash keeps their cheapness from becoming authority.

## Induction should open the next trial

There is no escape from induction. Even choosing a trial depends on beliefs inherited from previous trials. The demand for evidence can itself become a delaying ritual, especially when action is reversible and the cost of waiting is real.

My objection is narrower: induction should propose the next move, not close the search.

A useful rule carries its own looseness. It says where it has worked, what it ignores, what cheap observation might weaken it, and how much commitment should occur before looking again. Confidence may rise with repeated success, but the cost of checking can fall too. Once a practice matters enough to copy widely, designing a reusable eval may be cheaper than repeatedly assembling communal conviction.

The attitude is neither “trust the process” nor “question everything.” Questioning everything spends attention as carelessly as questioning nothing. The attitude is economic:

> Preserve accumulated knowledge, then buy the cheapest useful disagreement with it.

Sometimes the inherited rule wins immediately. Good. The trial has earned us confidence at low cost. Sometimes it loses. Better: it has prevented a larger commitment. And sometimes the world returns an answer that neither side knew how to ask for. That is the richest result, because the search now has somewhere new to go.

## A note on where this came from

I learned much of this attitude by reading Christopher Alexander. In [*The Timeless Way of Building*](/timeless-way-of-building), he describes a fundamental process: begin with the whole before you, make a local change, see whether it deepens the whole, and continue from the changed state. [His procedure applies patterns sequentially to a partially defined whole](https://library.uniteddiversity.coop/Ecological_Building/The_Timeless_Way_of_Building_Complete.pdf#page=375). It taught me to see design as unfolding rather than execution of a finished plan.

I first tried to make him the antagonist of this essay. That was an inductive leap of my own. He described trial, revision, evolving communal pattern languages, and even bad patterns dying out. My memory had preserved his confident examples more vividly than his procedural qualifications.

The remaining disagreement is smaller. Where Alexander sometimes trusted cultivated feeling to avoid prohibitively extensive experiments, I want to ask whether the experiment can be redesigned. Feeling may still judge the result. It need not bear the entire search cost.

That question no longer belongs mainly to Alexander. It belongs anywhere inherited success is used to avoid fresh contact with the world.
