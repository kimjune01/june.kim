---
variant: post-wide
title: "Functor Wizardry"
tags: cognition, methodology
---

*Part of the [cognition](/cognition) and [methodology](/methodology) series. Builds on [The Parts Bin](/the-parts-bin) and [Volley](/volley).*

I worked on [Soar](/diagnosis-soar) for four days. Diagnosed memory systems, prescribed algorithms, wrote demonstration PRs. Felt like wizardry. But the intervention point is simple: I point at a spell and say "go."

[The Natural Framework](/the-natural-framework) names the six roles. [The Parts Bin](/the-parts-bin) fills a broken slot. [Volley](/volley) sharpens the prescription into a spec, [blind, blind, merge](/blind-blind-merge) turns the spec into code, then Volley cleans the implementation into a PR. I'm gating the contracts between steps.

That's not a workflow. That's a functor pipeline.

### Three arts

Cognitive architectures distinguish three kinds of long-term store:

- **Semantic** (smem): what is true. Facts, structures, domain knowledge.
- **Procedural** (pmem): how to act. Production rules, compiled skills, workflows.
- **Episodic** (epmem): what happened. Experiences, traces, war stories.

Soar got two out of three. Chunking compiled deliberation into production rules, so procedural memory worked. Semantic and episodic stores existed but [grew without bound](/diagnosis-soar#the-forgetting-asymmetry) because nobody wrote the consolidation loop, and perception narrowed to compensate.

The blog has all three. The Natural Framework is semantic memory, the theory, the substrate. The Parts Bin and Volley are procedural memory, spells in the [grimoire](/double-loop) that tell an agent how to act. The [Diagnosis](/diagnosis-soar) and the [gemini-cli war story](/volley#four-hours-eight-files) are episodic memory: what happened, what worked, what broke. Publishing is the consolidation. Failed incantations never make the grimoire. It only keeps what worked.

### Spells, not scrolls

A scroll is read. A spell is cast. Each post is a spell: a structure-preserving map from one category to another. Category theory calls this a functor.

The Natural Framework maps observations to roles. The Parts Bin maps roles to candidates. Volley maps candidates to specs, merge maps specs to implementations, and Volley maps implementations to clean PRs. Each one preserves the contract chain: postcondition of one matches precondition of the next.

**Each post's output is the next post's input:**

<div style="max-width:min(90vw, 100%); margin:1.5em auto;">
<img src="/assets/spell-pipeline.svg" alt="Functor pipeline: Framework (broken system → diagnosed role) → Parts Bin (→ candidate) → Volley (→ sharp spec) → Merge (→ draft impl) → Volley (→ clean PR) → Ship." style="width:100%; display:block;">
</div>

Functors compose: if F: A → B and G: B → C, then G∘F: A → C is also a functor. The whole pipeline from "broken system" to "merged PR" is itself a functor. Each intermediate functor is idempotent — run Volley twice on a converged spec, same spec. Diagnose the same broken slot twice, same candidate. And since idempotency composes, the pipeline is idempotent too: run the whole thing twice, same PR.

An idempotent endofunctor stable under composition is a [reflective localization](https://ncatlab.org/nlab/show/reflective+localization). The fixed points form a reflective subcategory, and everything else has a unique morphism into it — exactly one way to clean up any artifact ([proof is short](https://ncatlab.org/nlab/show/reflective+localization)).

Three properties come free:

1. **Closed under limits.** Compose two converged specs, the result is already converged. That's why Volley output feeds cleanly into blind-blind-merge.
2. **Free algebras.** You don't need to learn how to use the functor. Applying it is understanding it. Load the post, run the workflow.
3. **Universal property.** The reflector is the best map into the subcategory. Any other path factors through it. The pmem+epmem functor isn't just *a* way to operate on foreign codebases — it's the universal one.

### Foreign ground

Semantic memory lives in the subject's substrate; procedural and episodic memory live in the agent's. Soar's smem is entirely foreign to me — I learned the theory from papers. But my pmem (the methodology posts) and epmem (past debugging episodes) form a functor over that foreign ground.

Four days on Soar: [Framework](/the-natural-framework) identified the broken roles. [Parts Bin](/the-parts-bin) prescribed graph coarsening and temporal composition. [Volley](/volley) sharpened those into a spec with testable claims. [Blind, blind, merge](/blind-blind-merge) synthesized the implementation. Volley again cleaned it into [demonstration PRs](https://github.com/SoarGroup/Soar/pull/578). Each postcondition fed the next precondition. The pipeline ran on a 40-year-old architecture I'd never touched because the functors preserve structure across domains.

The [gemini-cli fix](/volley#four-hours-eight-files): same pipeline, different substrate. Foreign codebase, three interacting bugs, four hours. The functor transferred because it reduces how much domain knowledge you need to internalize. Expertise is deep smem in one domain. Intelligence is pmem + epmem that form a functor over any smem.

### The circle

The three memory types compose under consolidation:

- Episodes consolidate into semantic knowledge (epmem → smem)
- Semantic knowledge consolidates into procedures (smem → pmem)
- Procedures generate new episodes (pmem → epmem)

Composition is associative: consolidate the gemini-cli episode into semantic knowledge, then harden that into the Volley procedure — or consolidate episode and knowledge together, then harden. Same output either way. The grouping doesn't matter; only the sequence does. The identity is null consolidation — nothing learned, memory passes through. That's a [monoid](https://en.wikipedia.org/wiki/Monoid).

The blog demonstrates the full cycle. The gemini-cli episode (epmem) consolidated into "volley converges in two rounds" (smem), which consolidated into the Volley workflow post (pmem), which generates new episodes every time someone runs it on the next bug. The circle closes.

Soar's monoid was broken. The smem → pmem morphism worked (compilation). The epmem → smem morphism was missing (no consolidation loop). A monoid with a broken multiplication isn't a monoid — it's a set with no structure. The stores existed but couldn't compose.

### The spec the math wrote

The pipeline works. The functor composes. The monoid closes, for me, manually, through the [double loop](/double-loop). But one morphism is missing, and the category theory writes its spec.

<div style="max-width:min(67vw, 100%); margin:1.5em auto;">
<img src="/assets/spell-monoid.svg" alt="Memory monoid: epmem → smem → pmem → epmem. The epmem → smem morphism is missing (dashed). Three constraints: existence (monoid requires it), convergence (must be idempotent), interface ((epmem, pmem) → pmem′)." style="width:100%; display:block;">
</div>

The monoid says epmem → smem → pmem must compose. That's the existence constraint: the morphism *must* be built, or the cycle breaks.

The reflective localization says it must be idempotent. Run the consolidation twice, the methodology doesn't change. Without idempotency, the system that improves its own procedures oscillates instead of converging. That's the convergence constraint.

The type signature says `(epmem, pmem) → pmem′`. Episodes and existing procedures in, better procedures out. That's the interface constraint.

The signature comes from the [Natural Framework](/the-natural-framework): Consolidate reads from Transmit (episodes) and writes to the substrate that shapes forward processing (procedures). The constraints come from category theory: monoid demands existence, reflective localization demands convergence. Two theories, orthogonal contributions — one gives the interface, the other the behavioral spec.

The theory is load-bearing, but four of five functors have empirical results. [Soar](/diagnosis-soar) tests Framework (role mapping found the broken slots) and Parts Bin (grid lookup prescribed the algorithms, both became [viable PRs](https://github.com/SoarGroup/Soar/pull/578)). [Gemini-cli](/volley#four-hours-eight-files) tests Volley (spec converged in two rounds) and Merge (PR passed review, zero revisions). Category theory guarantees the composition — test each functor, the pipeline follows. One functor remains: consolidation. If it gets built and doesn't converge, the theory is wrong. That's what makes it a theory, not a retrospective.

Work logs record episodes, diagnoses extract patterns, prescriptions become procedures — epmem → smem → pmem every time I write a post. But I'm the consolidation loop. I read the episodes, decide what generalizes, write the procedural post. The cron job is me.

The [consolidation harness](/the-natural-framework) is a sketch — extracts actions from transcripts, tracks patterns, flags when consolidation is due. But it rejects noise without promoting signal to pmem. Filter without Attend. Which episodes become procedures is still my call.

I have the signature, the contracts, and the convergence guarantee. The spec wrote itself. What's left is one more incantation from the [parts bin](/the-parts-bin).

---

*Written via the [double loop](/double-loop).*
