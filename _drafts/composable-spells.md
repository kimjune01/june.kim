---
layout: post
title: "Composable Spells"
tags: cognition methodology
---

*Part of the [cognition](/cognition) and [methodology](/methodology) series. Builds on [The Parts Bin](/the-parts-bin) and [Volley](/volley).*

I worked on [Soar](/diagnosis-soar) for four days. Diagnosing memory systems, prescribing algorithms, writing demonstration PRs. It feels like wizardry. But when I look at what I'm actually doing, the intervention point is simple: I point at a blog post and say "go."

[The Natural Framework](/the-natural-framework) tells the agent what the six roles are. [The Parts Bin](/the-parts-bin) tells it which algorithm fills a broken slot. [Volley](/volley) sharpens the prescription into a spec. [Blind, blind, merge](/blind-blind-merge) turns the spec into code. Each post's output is the next post's input. I'm not doing the work. I'm gating the contracts between steps.

That's not a workflow. That's a functor pipeline.

### Three memories

Cognitive architectures distinguish three kinds of long-term memory:

- **Semantic** (smem): what is true. Facts, structures, domain knowledge.
- **Procedural** (pmem): how to act. Production rules, compiled skills, workflows.
- **Episodic** (epmem): what happened. Experiences, traces, war stories.

Soar got two out of three. Procedural memory worked — chunking compiled deliberation into production rules. Semantic and episodic stores existed, but [grew without bound](/diagnosis-soar#the-forgetting-asymmetry) because nobody wrote the consolidation loop. The stores accumulated. Perception narrowed to compensate.

The blog has all three. The Natural Framework is semantic memory — the theory, the substrate. The Parts Bin and Volley are procedural memory — callable specs that tell an agent how to act. The [Diagnosis](/diagnosis-soar) and the [gemini-cli war story](/volley#four-hours-eight-files) are episodic memory — what happened, what worked, what broke. Publishing is the consolidation. Drafts that don't survive the filter are the forgetting.

### Functors, not files

Each post isn't a document. It's a functor: a structure-preserving map from one category to another.

The Natural Framework maps observations to roles. The Parts Bin maps broken roles to candidate algorithms. Volley maps candidates to sharp specs. Blind-blind-merge maps specs to code. Each one preserves the contract chain: postcondition of one matches precondition of the next.

$$\text{Framework} \xrightarrow{\text{roles}} \text{Parts Bin} \xrightarrow{\text{contract}} \text{Volley} \xrightarrow{\text{spec}} \text{Merge} \xrightarrow{\text{code}} \text{Ship}$$

Functors compose. If F: A → B and G: B → C, then G∘F: A → C is also a functor. The composed pipeline from "I see a broken system" to "here's a PR" is itself a functor. And each intermediate functor is idempotent — run Volley twice on a converged spec, you get the same spec. Run the Parts Bin diagnosis twice on the same broken slot, same candidate.

An idempotent endofunctor stable under composition is a [reflective localization](https://ncatlab.org/nlab/show/reflective+localization). The fixed points — converged specs, validated prescriptions, merged PRs — form a reflective subcategory. Everything else has a unique morphism into it. There's exactly one way to clean up any artifact.

Three properties come free:

1. **Closed under limits.** Compose two converged specs, the result is already converged. That's why Volley output feeds cleanly into blind-blind-merge.
2. **Free algebras.** You don't need to learn how to use the functor. Applying it is understanding it. Load the post, run the workflow.
3. **Universal property.** The reflector is the best map into the subcategory. Any other path factors through it. The pmem+epmem functor isn't just *a* way to operate on foreign codebases — it's the universal one.

### The foreign substrate

Here's what makes this practical. Semantic memory lives in the subject's substrate. Procedural and episodic memory live in the agent's. When I work on Soar, the smem is entirely foreign — I didn't write the architecture, I don't maintain the codebase, I learned the theory from papers. But my pmem (the methodology posts) and my epmem (past debugging episodes) form a functor over that foreign substrate.

Four days on Soar: [The Natural Framework](/the-natural-framework) identified the broken roles. [The Parts Bin](/the-parts-bin) prescribed graph coarsening and temporal composition. [Volley](/volley) sharpened the prescription into a spec with testable claims. [Blind, blind, merge](/blind-blind-merge) produced the [demonstration PRs](https://github.com/SoarGroup/Soar/pull/578). Each post's postcondition fed the next post's precondition. The pipeline ran on a 40-year-old architecture I'd never touched because the functors don't care what the substrate is — they preserve structure across domains.

The [gemini-cli fix](/volley#four-hours-eight-files) was the same pipeline, different substrate. Foreign codebase. Three interacting bugs. Four hours. The functor transferred because it doesn't need to internalize the domain — it reduces how much domain internalization is required. That's the difference between intelligence and expertise. Expertise is deep smem in one domain. Intelligence is pmem + epmem that form a functor over any smem.

### The monoid

The three memory types compose under consolidation:

- Episodes consolidate into semantic knowledge (epmem → smem)
- Semantic knowledge consolidates into procedures (smem → pmem)
- Procedures generate new episodes (pmem → epmem)

Composition is associative. Consolidate the gemini-cli episode into semantic knowledge, then consolidate that knowledge into the Volley procedure — or consolidate the episode and the knowledge together, then harden the result into procedure. Same output either way. The grouping doesn't matter; only the sequence does. The identity is null consolidation — nothing learned, memory passes through unchanged. That's a [monoid](https://en.wikipedia.org/wiki/Monoid).

The blog demonstrates the full cycle. The gemini-cli episode (epmem) consolidated into "volley converges in two rounds" (smem), which consolidated into the Volley workflow post (pmem), which generates new episodes every time someone runs it on the next bug. The monoid closes.

Soar's monoid was broken. The smem → pmem morphism worked (chunking). The epmem → smem morphism was missing (no consolidation loop). A monoid with a broken multiplication isn't a monoid — it's a set with no structure. The stores existed but couldn't compose.

### The spec the math wrote

The pipeline works. The functor composes. The monoid closes — for me, manually, through the [double loop](/double-loop). But one morphism is missing, and the category theory writes its spec.

The monoid says epmem → smem → pmem must compose. Without the epmem → smem morphism, you don't have a monoid — you have a set with no structure. That's the existence constraint: the morphism *must* be built, or the cycle breaks.

The reflective localization says it must be idempotent. Run the consolidation twice, the methodology doesn't change. If it's not idempotent, the system that improves its own procedures oscillates instead of converging. That's the convergence constraint.

The type signature says `(epmem, pmem) → pmem′`. Episodes and existing procedures in, better procedures out. That's the interface constraint.

The signature comes from the [Natural Framework](/the-natural-framework): Consolidate reads from Remember (episodes) and writes to the substrate that shapes forward processing (procedures). The constraints come from the category theory: the monoid demands existence, the reflective localization demands convergence. Two theories, orthogonal contributions. One gives the interface, the other gives the behavioral spec.

The theory is load-bearing, but four of five functors have empirical results. The [Soar work](/diagnosis-soar) tests Framework (role mapping identified the broken slots) and Parts Bin (grid lookup prescribed graph coarsening and temporal composition, both turned into [viable PRs](https://github.com/SoarGroup/Soar/pull/578)). The [gemini-cli fix](/volley#four-hours-eight-files) tests Volley (spec converged in two rounds) and Merge (PR passed review, zero revisions). The composition of tested components is guaranteed by the category theory — you don't test the pipeline separately, you test each functor and the math gives you the rest. One functor remains: the consolidation morphism. If it gets built and doesn't converge, the theory is wrong. That's what makes it a theory and not a retrospective.

Work logs record episodes. Diagnoses extract patterns. Prescriptions become procedures. That's epmem → smem → pmem, and it happens every time I write a post. But I'm the consolidation loop. I read the episodes, decide what generalizes, write the procedural post. The cron job is me.

The [consolidation harness](/the-natural-framework) is a sketch. It extracts actions from transcripts, tracks patterns, flags when consolidation is due. But it doesn't close the loop. It's Filter without Attend — it can reject noise, but it can't promote signal to pmem. The judgment about which episodes become procedures is still mine.

Maybe the Attend in the consolidation loop is the last thing you automate. But the spec is tight enough to build against. And any pipe described in code can improve itself, with a little supervision. The supervisor isn't doing the work. They're gating the contracts. That's Attend, not Cache.

---

*Written via the [double loop](/double-loop).*
