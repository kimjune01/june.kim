---
layout: post
title: "Perception Pipe"
tags: coding cognition
---

*Part of the [cognition](/cognition) series.*

I built a recorder and a coordinator. [Caret Recorder](/caret-recorder) captures what's on screen, structures it through accessibility-tree parsing, and logs it semantically. [Cord](/cord) decomposes goals into parallel agent trees with filtered context. I thought connecting them was a data structure problem.

I asked Claude to check my guess against the neuroscience. My guess was wrong, and the correction opened up something I haven't built yet.

## The gap

You're reading a PR review. Low priority. Then a Slack message arrives about a production incident in that same service. The PR review you already "processed" retroactively becomes urgent. Its importance updated without you re-perceiving it. You didn't search for the connection. The connection found you.

Piping Caret Recorder into Cord is just plumbing. Plumbing doesn't decide *what matters right now*. What connects perception to action in human cognition is the mechanism that surfaces relevance. Cognitive scientists call it *salience*: the computational process that decides *this, not that, right now*.

So I needed a salience layer between them. The question was what shape it should take.

## The wrong guess

I assumed it's a priority queue.

A stack would mean the last thing in is the first thing processed. That's interrupts, and interrupts destroy flow. A plain queue would mean first-in-first-out, which ignores that something you saw twenty minutes ago can suddenly become the most important thing when new context arrives.

A priority queue seemed right. A heap where the priority function is continuously re-evaluated. New perception re-weights what's already there. The HIPAA reading from an hour ago was decaying. Then someone asks about health data compliance and it jumps back to the top without being re-observed.

Clean CS metaphor. Poll the most salient item, process it, re-sort.

## What the research says

The guess held up in parts. [Bisley and Goldberg (2010)](https://doi.org/10.1146/annurev-neuro-060909-152823) showed that the lateral intraparietal area maintains priority maps: continuously updated representations of salience across the visual field. Salience *is* continuously re-evaluated. [Van Hamme and Wasserman (1994)](https://doi.org/10.1037/0097-7403.20.3.219) demonstrated retrospective revaluation: new information changes the learned importance of previously observed cues, even without re-exposure. The retroactive re-weighting is real.

[Richards and Frankland (2017)](https://doi.org/10.1016/j.neuron.2017.04.037) argued in *Neuron* that forgetting is a feature, not a failure. It prevents overfitting, explicitly analogized to regularization in machine learning. And the [ACT-R](https://doi.org/10.1037/0033-295X.111.4.1036) spreading activation model, one of the most replicated findings in cognitive science, confirms that current perception drives memory retrieval via similarity. What you're looking at right now reshapes what you can recall.

All of that validated the intuition. But the data structure was wrong.

## Winner kills all

[Desimone and Duncan (1995)](https://doi.org/10.1146/annurev.ne.18.030195.001205) proposed biased competition theory: visual objects don't queue up for processing. They compete simultaneously in parallel, and the winner suppresses the losers through mutual inhibition. Items actively race each other, and losing means being actively pushed down.

This distinction matters because of what [Anderson, Bjork, and Bjork (1994)](https://doi.org/10.1037/0278-7393.20.5.1063) found: retrieval-induced forgetting. The act of retrieving one memory actively suppresses competing memories. Recalling "banana" from the category "fruit" makes it *harder* to later recall "orange." The selection and the forgetting are the same inhibitory mechanism.

In a priority queue, you pop the top item and the rest sit there unchanged. In the brain, popping the top item *damages* the runners-up. You can't model that with a heap.

It's closer to a softmax over activation values than a heap with pop operations. All candidates evaluated simultaneously, winners amplified, losers suppressed. Weighted competition across all candidates at once, where the weights are a function of similarity to the current query. This sounds like transformer self-attention, but a [2025 preprint](https://doi.org/10.1101/2025.01.22.634394) argues it's not: transformers lack the inhibitory executive control that makes biological competition work. The suppression in biased competition is active. Transformer attention just re-weights.

## If this is right

Retrieval without inhibition causes interference: everything stays equally available and nothing is useful. [Stan Franklin](https://en.wikipedia.org/wiki/Stan_Franklin) understood this decades ago. His [LIDA](https://doi.org/10.1109/TAMD.2013.2277589) architecture implements [Global Workspace Theory](https://doi.org/10.1016/S1364-6613(00)01819-2) with competitive coalitions as a first-class mechanism: perception forms coalitions, they compete, a winner gets broadcast to all modules, losers are actively suppressed. This is Desimone and Duncan's biased competition, built into a complete cognitive cycle. LIDA is the direct theoretical ancestor of what I'm describing. But the technology is dated. The framework never left the lab.

What has been deployed models the excitatory half and ignores the inhibitory half. [Generative Agents](https://doi.org/10.1145/3586183.3606763) (Park et al. 2023) score memories by recency, importance, and relevance, but nothing is ever deleted or suppressed. The memory stream only grows. [MemGPT](https://arxiv.org/abs/2310.08560) pages context in and out like an OS managing virtual memory, but the eviction is LLM-driven, not competitive. RAG retrieves everything above a similarity threshold. Agent frameworks coordinate tasks in parallel. I think the reason AI assistants plateau is that none of them forget. The missing primitive across the entire stack might be competitive inhibition.

If a salience layer between Caret Recorder and Cord were a priority queue, you'd poll the most important item, hand it to an agent, re-sort, repeat. Sequential. Clean. Wrong.

The competitive model would evaluate all candidates in parallel. The current perception biases the competition. Items similar to your current focus get amplified. Items dissimilar get suppressed. And that suppression *is* the decay.

The salience layer would re-weight all candidates simultaneously on every new perception event. The query is "what is the human doing right now." The candidates are everything in the decaying memory. The output is a distribution: some things become more available, most things become less, and the ones that become less are, functionally, being forgotten. The simplest damping mechanism: feed that distribution back to perception. Salience filters what Caret Recorder bothers to structure next. You turn a blind eye to what lost the competition. That's focus.

Context windows are short-term memory. But what happens to the things that win competition repeatedly? In the brain, the hippocampus replays salient experiences during sleep, and the ones that survive replay get written to cortex as long-term memory. Most of what happened today doesn't make it to tomorrow. More competitive inhibition, running offline.

LIDA gets the ordering right. In its cognitive cycle, memory consolidation happens *after* the conscious broadcast, not before. The competition decides what matters, action executes, and then the broadcast updates all memory systems simultaneously. We are agents of our memory and perception. Cognition sits between them. Upstream, it filters what perception bothers to structure. Downstream, it filters what memory bothers to keep. Selective perception and selective memory, both driven by the same competitive process.

An agent system needs the same ordering. Short-term memory is the working set that salience maintains during a session. Long-term memory is the decisions, patterns, and preferences that persist across sessions because they won enough rounds of competition to earn consolidation. The consolidation layer is close to commodity. [Mem0](https://github.com/mem0ai/mem0) handles automatic extraction, consolidation, and decay. [Zep](https://www.getzep.com/) builds temporal knowledge graphs that track how facts change over time. The consolidation problem is largely solved. The competition problem is not.

You can't be surprised by a connection if you're still consciously holding everything. Forgetting is what makes discovery possible.

## Where this leads

[Vibelogging](/vibelogging) is the claim that prose is source code. You write spec-depth blog posts, an agent reads them, working software comes out. Human writes, machine executes.

If the architecture I'm describing worked, it would invert that. Perception watches you work: reading papers, prototyping auction math, arguing about privacy models in Slack. Salience identifies which of those moments were design decisions, the things that survived competition and suppressed their alternatives. Coordination spawns agents to draft spec-depth prose from those surviving moments.

The blog would write itself from your behavior. You wouldn't sit down to write the post that specifies the scoring function. You'd *do* the scoring function: research, prototype, argue, decide. The salience layer would already know which moments were the real decisions because those are the ones that won the competition. The losers decayed. The winners would *be* the spec.

Suppression is curation. The inhibitory process that lets you think clearly is the same one that could let a system extract a clear specification from a messy trail of work.

The [Vector Space](/vector-space) series is the first reference implementation of a compilable vibelogging artifact. Thirty-odd blog posts that specify an entire ad exchange, from [auction math](/power-diagrams-ad-auctions) to [privacy architecture](/ask-first) to [publisher UX](/publisher-ux). An agent reads the blog and produces a working system. That artifact was written manually. If this hypothesis holds, the next one wouldn't have to be.

## The next layer

Assembly replaced machine code. C replaced assembly. Python replaced C. Each layer still had you writing instructions for the computer. [Vibelogging](/vibelogging) was the first layer where the human writes for humans, prose at spec depth, and an agent handles the rest. But you still sat down to write. If competitive inhibition can do the curation, there's a layer beyond that:

1. **Code**: you write instructions for the machine.
2. **Vibelogging**: you write prose, the agent writes code.
3. **Automated vibelogging**: you work, the system writes the prose, the agent writes the code.

Code requires you to think in the machine's terms. Prose requires you to think clearly. Work just requires you to think.

And if the system participates in your cognition, agents' results flow back into the perception stream, your priorities shift, new relevance emerges, new tasks spawn.

That loop looks like it spirals. Output triggers perception triggers salience triggers coordination triggers more output. What prevents it? The same mechanism the post is about. Each pass through the cycle, competitive inhibition prunes. The winners from the last round compete against the winners from this round, and most of them lose. The loop dampens because forgetting is built into every step.

## What I'd build

Perception → Salience (parallel competition) → Coordination (spawn/fork) → Memory (consolidation).

Four layers, in that order. Coordination before memory. What you do determines what you remember. LIDA's cognitive cycle encodes this: the conscious broadcast triggers action selection and memory updates simultaneously, but the competition that decides *what gets broadcast* precedes both. Memory is downstream of cognition, not upstream.

I'm not the first to propose these layers. Franklin spent decades on LIDA, the only cognitive architecture with genuine competitive coalitions as a first-class mechanism alongside perception, action selection, and memory consolidation. He got the architecture right. It never shipped. Franklin died in January 2023, and the project appears dormant. [OpenCog](https://hyperon.opencog.org/) has all four layers on paper too, with economic attention networks for competitive filtering. After eighteen years of development, it's still pre-production.

The pattern is consistent: systems that deploy all four layers never ship. [SOAR](https://soar.eecs.umich.edu/) has been deployed in military simulations and robotics for decades, but it drops competitive salience entirely. [Letta](https://docs.letta.com/) has real users and funding, but drops perception and salience both. The systems that ship succeed by simplifying. The ones that keep the competitive layer never leave the lab.

So maybe I'm wrong. Maybe the competitive salience layer costs more than it's worth in a practical system, and scoring and ranking is good enough. Caret Recorder handles perception. Cord handles coordination. Memory is pluggable: pick Mem0 or Zep and consolidation is handled. The open problem is salience, and the open question is whether it needs to be competitive at all.

Both hypotheses are falsifiable. For competition: build two systems, one with competitive inhibition between memory candidates and one with scoring and ranking alone. If the scoring system surfaces equally relevant context with no more interference, competitive inhibition is overhead and the queue was fine all along. For ordering: if memory precedes cognition, the retrieval policy must be rule-based. Recency weights, similarity thresholds, fixed decay curves, all decided by the developer. If cognition precedes memory, the intelligent process decides what's worth keeping. Build both. If the rule-based retrieval system performs as well as the cognition-driven one, the ordering doesn't matter.

The correction from queue to competition at least points in a direction. The queue says: process items one at a time, in order of importance. Competition says: everything races at once, and the winners suppress the rest. Build the race, not the heap.

This hypothesis is dedicated to Stan Franklin (1931–2023), who got there first.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched citations and drafted prose.*
