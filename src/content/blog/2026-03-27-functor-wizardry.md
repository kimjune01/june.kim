---
variant: post-wide
title: "Functor Wizardry"
tags: cognition, methodology
---

*Part of the [cognition](/cognition) and [methodology](/methodology) series. Builds on [The Parts Bin](/the-parts-bin) and [Volley](/volley).*

<div style="max-width:560px; margin:1.5em auto; aspect-ratio:16/9;">
<iframe width="100%" height="100%" src="https://www.youtube.com/embed/GFiWEjCedzY" frameborder="0" allowfullscreen style="border-radius:8px;"></iframe>
</div>
<p style="text-align:center; font-style:italic; margin-top:-0.5em;">Using coding agents in 2026</p>

What does the wizard know that the apprentice doesn't? Mickey in [Fantasia](https://en.wikipedia.org/wiki/Fantasia_%281940_film%29) knows the broom's interface: carry water, pour water. Enough to start the work, not enough to stop it. He chops the broom in half; now two brooms carry water. The spell multiplies but never converges.

The wizard knows when the spell is done. Carry water *until the basin is full*, then stop. Run it twice, the basin is still full; no basin overflow.

What makes a spell fill instead of flood? What the spell sees and remembers between casts.

### Three arts

Long-term memory comes in [three kinds](https://en.wikipedia.org/wiki/Long-term_memory):

- **Semantic**: what is true. Facts, theories, domain knowledge.
- **Procedural**: how to act. Workflows, recipes, compiled skills.
- **Episodic**: what happened. War stories, debugging sessions, outcomes.

[Soar](/diagnosis-soar) built all three stores. Two composed naturally, but distilling episodes into knowledge [remained an open problem](/diagnosis-soar#the-forgetting-asymmetry). Their broom carried water but never learned when to stop.

> episodes → knowledge → procedures

This blog has all three. The [Natural Framework](/the-natural-framework) is semantic memory: the theory, the substrate. The [Parts Bin](/the-parts-bin) and [Volley](/volley) are procedural memory: spells in the [grimoire](/double-loop) that tell an agent how to act. The [Diagnosis](/diagnosis-soar) and the [gemini-cli war story](/volley#four-hours-eight-files) are episodic memory: what happened, what worked, what broke. Much like Soar, consolidation still remains manual. Writing is my consolidation step: episodes → knowledge → procedures. Failed incantations never make the grimoire. It only keeps what worked.

### Spells, not scrolls

A scroll is read. A spell is cast.

<table style="margin:1em auto; font-size:14px; width:auto;">
<tr><td><strong>Semantic</strong></td><td><a href="/the-natural-framework">Natural Framework</a></td><td>the theory</td></tr>
<tr><td><strong>Procedural</strong></td><td><a href="/the-parts-bin">Parts Bin</a>, <a href="/volley">Volley</a>, <a href="/blind-blind-merge">Merge</a></td><td>the spells</td></tr>
<tr><td><strong>Episodic</strong></td><td><a href="/diagnosis-soar">Diagnosis: Soar</a>, <a href="/volley#four-hours-eight-files">gemini-cli</a></td><td>the war stories</td></tr>
</table>

Each procedural post behaves like a spell: it preserves structure while turning one kind of artifact into another. Category theory calls this a [functor](https://en.wikipedia.org/wiki/Functor).

[Framework](/the-natural-framework) takes a broken system and names the broken roles. [Parts Bin](/the-parts-bin) takes those roles and prescribes candidates. [Volley](/volley) sharpens candidates into testable specs. [Merge](/blind-blind-merge) turns specs into implementations. Volley again cleans implementations into PRs.

Cast them in sequence on a foreign system, and each spell's output becomes the next spell's input:

<div style="max-width:min(90vw, 100%); margin:1.5em auto;">
<img src="/assets/spell-pipeline.svg" alt="Functor pipeline: Framework (broken system → diagnosed role) → Parts Bin (→ candidate) → Volley (→ sharp spec) → Merge (→ draft impl) → Volley (→ clean PR) → Ship." style="width:100%; display:block;">
</div>

Functors compose: if F: A → B and G: B → C, then G∘F: A → C is also a functor. The whole pipeline from "broken system" to "merged PR" is itself a functor. Each intermediate functor is idempotent: run Volley twice on a converged spec, same spec. Diagnose the same broken slot twice, same candidate. Idempotency composes, so the pipeline is idempotent too: run the whole thing twice, same PR.

Each step has a stopping condition, and stopping conditions compose. That's what makes a spell fill instead of flood. An approximate [reflector](https://ncatlab.org/nlab/show/reflective+localization) is good enough: different agents may fill the basin to different levels, but each run converges. A spell that converges without babysitting is a spell you can delegate.

### Foreign ground

Semantic memory lives in the subject's substrate; procedural and episodic memory live in the agent's. Soar's smem is entirely foreign to me; I learned the theory from papers. But my pmem (the methodology posts) and epmem (past debugging episodes) form a functor over that foreign ground.

Four days on Soar: [Framework](/the-natural-framework) identified the broken roles. [Parts Bin](/the-parts-bin) prescribed graph coarsening and temporal composition. [Volley](/volley) sharpened those into a spec with testable claims. [Blind, blind, merge](/blind-blind-merge) synthesized the implementation. Volley again cleaned it into [demonstration PRs](https://github.com/SoarGroup/Soar/pull/578). Each postcondition fed the next precondition. The pipeline ran on a 40-year-old architecture I'd never touched because the functors preserve structure across domains. The [gemini-cli fix](/volley#four-hours-eight-files) was the same pipeline on a different substrate: foreign codebase, three interacting bugs, four hours. Expertise is deep smem in one domain. Intelligence is pmem + epmem that form a functor over any smem.

### The circle

The three memory types compose under consolidation:

- Episodes consolidate into semantic knowledge (epmem → smem)
- Semantic knowledge shapes procedures (smem → pmem)
- Procedures generate new episodes (pmem → epmem)

Composition is associative: consolidate the gemini-cli episode into semantic knowledge, then harden that into the Volley procedure. Or consolidate episode and knowledge together, then harden. Same output either way. The grouping doesn't matter; only the sequence does. The identity is null consolidation: nothing learned, memory passes through. That's a [monoid](https://en.wikipedia.org/wiki/Monoid).

The blog demonstrates the full cycle. The gemini-cli episode (epmem) consolidated into "volley converges in two rounds" (smem), which consolidated into the Volley workflow post (pmem), which generates new episodes every time someone runs it on the next bug. The circle closes.

Soar's monoid was incomplete. The smem → pmem morphism worked (compilation). The epmem → smem morphism was missing (no consolidation loop). A monoid with a broken multiplication isn't a monoid. It's a set with no structure. The stores existed but couldn't compose.

### The spec the math wrote

The pipeline works. The functor composes. The monoid closes, for me, manually, through the [double loop](/double-loop). But one morphism is missing, and the category theory writes its spec.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/spell-monoid.svg" alt="Memory monoid: epmem → smem → pmem → epmem. The epmem → smem morphism is missing (dashed). Three constraints: existence (monoid requires it), convergence (must be idempotent), interface ((epmem, pmem) → pmem′)." style="width:100%; display:block;">
</div>

Three constraints fall out of the math:

1. **Existence.** The monoid says epmem → smem → pmem must compose, or the cycle breaks.
2. **Convergence.** Run consolidation twice, the methodology doesn't change. Without idempotency, a system that improves its own procedures oscillates.
3. **Interface.** `(epmem, pmem) → pmem′`. Episodes and existing procedures in, better procedures out.

The [Natural Framework](/the-natural-framework) gives the interface; category theory gives the behavioral spec.

The theory is load-bearing, but four of five functors have empirical results. Soar tests Framework and Parts Bin (both became [viable PRs](https://github.com/SoarGroup/Soar/pull/578)). Gemini-cli tests Volley and Merge (PR passed review, zero revisions). One functor remains: consolidation. If it gets built and doesn't converge, the theory is wrong. That's what makes it a theory, not a retrospective.

The Fantasia metaphor was never a metaphor. Mickey lacked the morphism that made his invocations converge.

A spell is a convergent functor: a procedure whose output feeds another procedure's input without flooding the basin. A grimoire is procedural memory: the store of spells that survived contact with episodes. A wizard is someone who knows which morphisms compose.

What remains is to build the missing morphism: the consolidate spell that turns episodes into better spells.

---

*Written via the [double loop](/double-loop).*
