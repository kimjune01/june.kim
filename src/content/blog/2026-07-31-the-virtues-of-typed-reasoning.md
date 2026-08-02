---
variant: post
title: The Virtues of Typed Reasoning
tags: reflecting, epistemology, methodology
---

I like prose. I've written a lot of it. The nice thing about prose is that you can say anything.

That's also the problem.

You can start a paragraph with an observation, turn it into a hypothesis halfway through, and end with a causal conclusion. If the writing flows well enough, nobody notices the [type conversion](/type-the-question). Sometimes not even the writer.

> Accuracy went up when we added retrieval, which shows that the model needed more knowledge.

The first half is an observation. The second half is a hypothesis. Maybe retrieval added knowledge. Maybe it changed the prompt length, tool behavior, sampling, or where the model paid attention. The sentence compiles anyway.

Prose has no [type checker](/internal-reasoning-of-prose-compiler).

### Type safety for thought

In programming, we give things types because not every value should do every job. A string that looks like a date is still a string. A user ID and a payment ID are both strings, and mixing them up ruins your weekend.

Reasoning has types too:

| Type | Its job | Common type error |
|:--|:--|:--|
| Observation | Record what happened | Explanation smuggled in as description |
| Hypothesis | Propose a possible explanation | Confidence presented as evidence |
| Prediction | Say what should happen if the hypothesis is right | Written after seeing the result |
| Experiment | Separate one hypothesis from another | Test merely compatible with both |
| Evidence | Support or kill within the test boundary | Failure to reject treated as proof |
| Conclusion | State what we're willing to act on for now | Generalized beyond its evidence |

These are not different names for the same blob of text. Each type does a different job. An observation can't explain itself. A hypothesis can't verify itself. A test that [fails to reject the null](/evidence-has-a-trajectory) doesn't prove the null. A conclusion doesn't get to outlive all of its evidence.

Most bad reasoning is a [type error](/type-iii-error).

Correlation cast to causation. Confidence cast to evidence. A benchmark score cast to general intelligence. A missing test cast to a passing one. An idea repeated until it gets cast to a fact.

Good prose hides these casts better than bad prose. Confidence, detail, citations, and technical vocabulary can make a claim easier to accept, but none of them change what the claim is entitled to do.

> Eloquent prose cannot substitute for epistemic entitlement.

You don't need to draw a graph in every meeting. Start by translating the phrases people already use:

| When someone says | Translate it to | What it still owes |
|:--|:--|:--|
| "We saw..." | Observation | Source, scope, and repeatability |
| "The data shows..." | Observation plus an inference | Name the inference and its alternatives |
| "I think..." | Hypothesis | A prediction that could be wrong |
| "This means..." | Interpretation | A test that separates it from other meanings |
| "We proved..." | Claim of verification | The check, boundary, and result |
| "There's no evidence..." | Nothing found by the stated search | A test designed to establish absence or equivalence |
| "Everyone agrees..." | Reported consensus | Independent evidence, if truth matters |
| "I'm confident..." | Confidence report | Nothing; confidence is not evidence |
| "We should..." | Recommendation | Evidence plus values, costs, and risk tolerance |

The left column is how reasoning arrives. The middle column is what it is. The right column is what it still owes.

### Meetings already have type systems

This is not the first attempt to inject epistemology into a meeting. In 1970, Kunz and Rittel proposed [IBIS](https://escholarship.org/uc/item/5cj786v8), a grammar of issues, positions, and arguments for group decisions. [Dialogue Mapping](https://cognexus.org/id41.htm) applies it by translating everyday meeting-speak into questions, ideas, pros, and cons on a shared screen. Toulmin separated arguments into claims, grounds, warrants, qualifiers, backing, and rebuttals. [Six Thinking Hats](https://www.debono.com/) separates facts, feelings, risks, benefits, ideas, and process so a group doesn't confuse one mode for another. Intelligence analysts use [Analysis of Competing Hypotheses](https://www.cia.gov/resources/csi/static/955180a45afe3f5013772c313b16face/Tradecraft-Primer-apr09.pdf) to array evidence against alternatives instead of collecting support for a favorite.

Each one types conversation to prevent a familiar failure. The addition here is a promotion rule: no move inherits a stronger epistemic entitlement just because it was spoken well. An observation can become evidence only through a declared inference and test. A hypothesis can become a conclusion only by surviving the checks that its type owes. The meeting can stay conversational as long as its claims can't skip the line.

### Give disagreements an address

When two people disagree through prose, they write more prose. One publishes a paper, another a rebuttal, then the first a response. Now you have three documents, and the disagreement is somewhere inside all of them.

Typed reasoning gives the disagreement an address.

You can accept the observation but reject the [causal edge](/borrowed-vocabulary-for-the-hypothesis-edge). You can accept the experiment but reject the measurement. You can say that a result supports the hypothesis but doesn't witness it.

The disagreement gets smaller without getting less important.

An [audit](/how-to-audit-a-benchmark) shouldn't ask you to trust the auditor instead. It should show you the exact claim, what it depends on, and what would kill it. If the audit is wrong, you should be able to point at the first broken edge.

The best rebuttal is not *trust me bro*. It's *run this*.

### Corrections should propagate

Say a benchmark [fixes its estimator](/auditing-deepswe-v1-1) and the headline number changes. What else needs to change?

In prose, somebody has to remember every conclusion that used the old number. It's hiding in a paper, a blog post, a leaderboard, a launch announcement, or the collective memory of Twitter. Corrections get published, but they don't propagate.

In a typed graph, dependency is an edge. If the measurement dies, you can find everything downstream. Some conclusions have other evidence and survive. Others go back to being open hypotheses.

This is how package managers already work. If a dependency breaks, we don't reread every package description and vibe out what might be affected. We traverse the graph.

Why should knowledge have worse dependency management than JavaScript?

### Find the experiment you're missing

A flat ablation table tells you which arms scored higher. It doesn't tell you why.

If two changes both improve accuracy, do they work independently? Are they two ways of doing the same thing? Does one only work when the other is present? Is the lift from the mechanism you care about or a harness side effect?

When the hypotheses, predictions, and experiments are separate types, the missing experiment shows up as a hole. Two hypotheses explain the same observation and nothing in the graph separates them.

That's the job of the [hypothesis graph](/the-hypothesis-graph-semantic-memory-methodeutics). Use it to decide what to try next while it's still cheap to change your mind. The pretty diagram falls out afterward.

The dead branches matter too. Without them, the next researcher proposes the same attractive explanation and pays to kill it again. A record of only the winner throws away everything that cost something to kill.

### Types have vices too

Putting a claim in a box doesn't make it true. Give it an ID, three citations, a confidence score, and a green checkmark. It can still be nonsense.

Types can also freeze the wrong worldview. Early research is messy because the right distinctions haven't been discovered yet. If the schema comes first, anything that doesn't fit looks invalid. When the schema and the anomaly conflict, bet on the anomaly.

And typed reasoning is more work. Prose lets an author leave dependencies implied. A graph makes you expose them one by one. That's not free.

### Division of labor

So types shouldn't replace prose. Prose is where we explain motivation, context, history, uncertainty, and why anybody should care. It's also where half-formed ideas get enough room to become good ones.

Types do a different job. They preserve commitments.

Prose is the interface to a mind. Types are the interface between inquiries.

### Selection pressure

Typed reasoning isn't cheaper today. Somebody has to name the types and draw the edges, so prose wins for a thought used once. But inquiries accumulate. Agents have finite context windows, researchers forget why they believed something, and teams reconstruct dependencies whenever work changes hands. The longer the inquiry lives, the more expensive implicit reasoning becomes.

Software followed the same path. Types looked like overhead when one programmer could hold the whole program in his head. As programs grew beyond one mind, the compiler became cheaper than the meeting. If typed reasoning preserves the prose and adds checkable structure, then it strictly dominates prose alone for long-lived, collaborative inquiry. The remaining obstacle is the cost of typing, and agents will keep driving that cost down because context and verification remain expensive.

Thought doesn't have to become neat. Discovery can stay vague, associative, and full of bad ideas. The constraint appears at the boundary: before one inquiry can become another inquiry's dependency, its reasoning has to arrive in a form the next one can check. If typed reasoning is more efficient at that boundary, adoption is not a matter of taste. Something under pressure to think across time will eventually select for it.

### Show your work

Giving a reasoning move a type means accepting a limit on what it can claim.

This is what I saw. This is what I think explains it. This is what should happen if I'm right. This is the test I ran. This is what survived. This is what would change my mind.

Prose lets reasoning travel. Types make it arrive with its obligations intact.
