---
layout: post-wide
title: "The Handshake"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Natural Framework](/the-natural-framework) and [General Intelligence](/general-intelligence). This post is the formal backbone of the series. It's dense by design. [The Parts Bin](/the-parts-bin) is where the formalism becomes practical.*

### Claim

The six steps are not a metaphor. They have a natural home in category theory: morphisms inside a monad, constrained by the data processing inequality. [The Natural Framework](/the-natural-framework) derives all six steps from temporal flow and bounded storage: three steps by existence proof at the boundaries, three more by corollary. The derivation narrows the space; domains across disciplines fill it. This post formalizes the composition: contracts, budget, and the inductive argument for survival.

### Category

Objects are measurable spaces (information states). Morphisms are Markov kernels (stochastic maps). This is the Kleisli category of the Giry monad, the category **Stoch** ([Fritz 2020](https://arxiv.org/abs/1908.07021)).

The Giry monad G is the endofunctor. It maps measurable spaces to spaces of probability distributions. η (unit) is the Dirac delta: a deterministic state is a special case of a probabilistic one. μ (join) is integration: averaging over uncertainty about uncertainty yields uncertainty.

The six steps compose as morphisms inside this monad. The individual steps don't need to be endofunctors. They need to be structure-preserving morphisms.

### Contracts

Not all morphisms are equal. Each step in the pipeline carries a postcondition, a structural guarantee on the output:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col style="width:14em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Step</th><th style="background:#f0f0f0">Type</th><th style="background:#f0f0f0">Guarantee</th></tr></thead>
<tr><td>Perceive</td><td style="white-space:nowrap">raw → encoded</td><td>Parseable by next step. Injects new bits.</td></tr>
<tr><td>Cache</td><td style="white-space:nowrap">encoded → indexed</td><td>Retrievable by key.</td></tr>
<tr><td>Filter</td><td style="white-space:nowrap">indexed → selected</td><td>Strictly smaller. Losers suppressed, winners forwarded.</td></tr>
<tr><td>Attend</td><td style="white-space:nowrap">(policy, selected) → ranked</td><td>Ordered, diverse, bounded. Survivors are dissimilar.</td></tr>
<tr><td>Consolidate</td><td style="white-space:nowrap">(policy, ranked) → policy′</td><td>Lossy. Update must include selection on candidates.</td></tr>
<tr><td>Remember</td><td style="white-space:nowrap">policy′ → persisted</td><td>Retrievable on next cycle's Perceive.</td></tr>
</table>

<div style="max-width:1100px; margin:1.5em auto;">
<img src="/assets/handshake-pipeline.svg" alt="Six-step pipeline: Perceive → Cache → Filter → Attend → Consolidate → Remember, with interface types at each handshake point and a feedback trace from Remember to Perceive." style="width:100%; display:block;">
</div>

A morphism that preserves its contract through composition is *contract-preserving*. It belongs in the pipeline. One that doesn't is an arbitrary self-map. It breaks downstream.

Compaction reorganizes a cache but guarantees nothing about future processing. Consolidation guarantees the system changes. Wrong morphism type, same slot.

The contracts encode a second axis: which store. Perceive, Cache, and Filter operate on the data stream. Attend reads a separate policy store ([Corollary 2](/the-natural-framework#six-steps)). Consolidate writes it. The separation is derived: if policy shares a pool with data, variance corrupts the governing criterion within one iteration.

Four claims follow from the contracts:
1. **If contracts match, algorithms are swappable.** Interface programming. Defensible now.
2. **If any contract is broken, the loop will die.** Necessary condition. By induction on cycle count.
3. **If all contracts are satisfied with sufficient fidelity, the loop survives.** Sufficient condition. That is the budget.
4. **If an operation degrades its postcondition under iteration, it is a near-miss.** The instability argument from Corollary 2 generalizes: any morphism whose postcondition fails under self-composition will break the loop. Iteration stability is the test.

### Why this order

[The Natural Framework](/the-natural-framework) derives six necessary roles. The handshake makes them stages: each postcondition is the next step's precondition. Rearrange and the contracts break.

- Consolidate before Attend: writing policy before reading it. Criteria update on unevaluated data. Noise persisted.
- Attend before Filter: policy applied to unfiltered input. Signal drowns in volume.
- Filter before Cache: selecting from what hasn't been stored. No index, no comparison across items.

The typed interfaces force the order. Roles with typed interfaces in a fixed order are stages. That is the handshake: the postcondition of step N is the precondition of step N+1. The name is the proof.

### Data processing inequality

The order is fixed. The question is whether the ordered pipeline survives iteration. The constraint: for a Markov chain X → Y → Z, mutual information satisfies I(X;Z) ≤ I(X;Y). Each intermediate step can only decrease what downstream knows about the original input. The pipeline is a cascade of such maps.

The lossy steps (Filter, Attend, Consolidate) each reduce what the output retains about the raw input. Cache and Remember can be lossless; the pipeline's net loss comes from the competitive core.

<div style="max-width:875px; margin:1.5em auto;">
<img src="/assets/handshake-budget.svg" alt="Information budget: bars showing bits retained at each step. Perceive and Cache are lossless (blue), Filter, Attend, and Consolidate are lossy (red), Remember is lossless (blue)." style="width:100%; display:block;">
</div>

The loop survives only because Perceive injects new bits from the environment. Without new input, a lossy loop compounds information loss per cycle. A closed lossy loop dies. That is the named constraint that makes the budget visible.

A step that fails its contract leaks information faster than Perceive can replenish it. This deficit compounds; the loop degrades. A step that preserves its contract retains signal through each pass. The budget balances; the loop survives.

### Iteration-fidelity trade-off

The budget can balance in different ways. Few steps with high retention, or many steps with low retention. The heuristic: step count × per-step fidelity must clear the survival threshold. Diffusion models: a thousand cheap denoising steps, each with a weak guarantee. Human cognition: a few expensive passes. Sleep consolidation is one cycle, deeply lossy, deeply structural.

Fidelity measures retention per pass. Iteration stability is whether the postcondition survives re-application. They are distinct, and they can come apart. Top-k retains most bits but converges to a fixed point: same winners every cycle, diversity dead by cycle two. The loop survives informationally while Attend degrades. That is not starvation. It is homogenization: a different failure mode with a different budget requirement. An iteration-stable operation preserves its postcondition under re-application: sort a sorted list, still sorted. MMR a diverse slate, still diverse. [The Parts Bin](/the-parts-bin) uses this as the formal test for near-misses.

Rate-distortion theory provides the analogy: each morphism has a distortion cost (bits leaked) and a rate (bits retained). Baez, Fritz, & Leinster (2011) formalized entropy in categorical terms. Connecting it to iterated pipelines is the next step. The framework diagnoses which step is broken. The prescription: strengthen fidelity, or add iterations. Two knobs, one budget.

### Biased competition is a morphism

The budget gets spent in the competitive core: Filter, Attend, Consolidate. The mechanism inside that core has a name. [Desimone & Duncan (1995)](https://doi.org/10.1146/annurev.ne.18.030195.001205) described biased competition: stimuli compete for neural representation, top-down bias resolves the competition. [The Natural Framework](/the-natural-framework) derives the same separation: control must be independent of data (Corollary 2), stored separately (Corollary 3), and applied through a read interface (Attend). Desimone & Duncan observed it in neurons. The derivation shows it must exist in any bounded selective system.

The formalization came later, piecewise. [Reynolds & Heeger (2009)](https://doi.org/10.1016/j.neuron.2009.01.002) gave a normalization model, [Boerlin & Bhatt (2011)](https://arxiv.org/abs/1108.1277) gave a spike-coding model. Nobody placed biased competition inside a category.

Filter and Attend are the morphisms that implement biased competition. Filter suppresses losers (guarantee: output strictly smaller). Attend ranks survivors with lateral inhibition (guarantee: winners are dissimilar). One candidate model for the diversity guarantee is the [Determinantal Point Process](https://arxiv.org/abs/1207.6083), a probability distribution over subsets that assigns higher weight to diverse selections. DPPs are well-defined probability measures on subsets.

The proposed formalization: define Filter → Attend as a Markov kernel whose output distribution is a DPP over the selected subset. The DPP handles diversity. Ordering and boundedness are additional structure.

DPPs are defined over finite sets, and the set changes each cycle. The iteration-stability objection asks: does the DPP kernel compose stably with itself? It does not need to. If Perceive injects sufficiently novel items into the ground set each cycle, the DPP operates on a genuinely different finite set, not the same set reprocessed. The composition is not DPP ∘ DPP over a fixed set. It is DPP applied to a fresh set drawn from fresh input. The iteration-stability of the *diversity guarantee* reduces to the diversity of the *input stream*.

This is a stronger claim than the information budget alone. Loop survival requires quantity of new information: enough bits to offset the lossy core. Diversity survival requires variety of new information: enough novel items in the ground set that the DPP kernel has dissimilar candidates to select from. An echo chamber satisfies the first and violates the second. The loop runs, the budget balances, but the ground set homogenizes until DPP diversity enforcement becomes vacuous. Same winners every cycle, by a different mechanism than top-k convergence. This connects to the third death condition: decaying input includes not just shrinking volume but shrinking variety.

Three open directions:
1. **Biased competition as categorical morphism.** Formalize Desimone & Duncan's mechanism as a Markov kernel inside Stoch. Define the kernel, the output space, the conditioning variables.
2. **DPP as contract.** DPPs have been applied to recommendation, summarization, and sampling. Using them as the *postcondition* of a morphism in a cognitive pipeline, the contract that a step preserves diversity through composition, is a new application.
3. **Information accounting of competition.** Every suppressed loser costs bits. Defining which mutual information, under what coupling, and why subtraction is the right operation. That is the problem.

### Trace

Joyal, Street, Verity (1996): traced monoidal categories. The feedback loop (Remember → Perceive) has the structure of a categorical trace: output feeds back as input. The correct typing depends on how environment and internal state interact: what feeds back, what enters from outside, what exits as behavior. Formalizing this requires specifying those components and verifying that the resulting morphism satisfies the trace axioms in Stoch.

In the simpler view: ignore the environment boundary, and the six-step composition is a self-map in Stoch, a Markov chain on information states. But bare Markov chains never worked for cognition: n-grams plateau, PageRank has no taste.

What was missing is attention: a diversity-enforcing morphism that selects and repels. Whether the iterated chain converges, cycles, or diverges depends on conditions (irreducibility, aperiodicity, contractivity) that must be verified per domain. These are the right questions.

Cogito ergo sum: a closed loop with zero new input. A lossy self-map iterated without fresh bits from the environment compounds information loss per cycle. The man in the box goes insane, then dies. It illustrates the framework by failing: the loop structure is intact but the budget is negative.

### Falsification test

The trace predicts the closed loop. The falsification test predicts the broken step. Take a known-alive system. Identify a step whose contract was lost. Observe.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Step replaced</th><th style="background:#f0f0f0">Self-map substituted</th><th style="background:#f0f0f0">System</th><th style="background:#f0f0f0">Outcome</th></tr></thead>
<tr><td>Perceive</td><td>Prion — no guarantee on protein encoding</td><td>Biology</td><td>Death</td></tr>
<tr><td>Filter</td><td>p53 loss — no guarantee on which cells survive</td><td>Biology</td><td>Cancer</td></tr>
<tr><td>Remember</td><td>Immunosenescence — no guarantee on memory fidelity</td><td>Biology</td><td>Decay</td></tr>
<tr><td>Perceive</td><td>Great Leap Forward — falsified harvest data</td><td>Society</td><td>Famine</td></tr>
<tr><td>Filter</td><td>TerraUSD — no filter on destabilizing redemptions</td><td>Finance</td><td>Death spiral</td></tr>
<tr><td>Remember</td><td>NASA Columbia — lesson not durably consolidated</td><td>Engineering</td><td>Catastrophe</td></tr>
</table>

Every case is multi-causal. But in each, a contract was lost, and the loss compounded rather than self-correcting. The vocabulary names the dominant failure mode.

### Three death conditions

1. **Broken step.** A morphism loses its contract. Signal leaks faster than Perceive replenishes. (Prion, cancer, TerraUSD.)
2. **Closed loop.** Perceive is sealed. Zero credits. (Cogito, frozen weights.)
3. **Decaying input.** Perceive is open but the environment degrades. Credits shrink per cycle. The loop structure is intact, every step preserves its contract, but the source dries up. The system doesn't break; it starves. (Sensory deprivation, dying ecosystem, echo chamber, agent trained on stale data.)

The information budget constrains all three: the budget must balance, the credits must exist, and the credits must not decay. The deficit is the diagnosis.

### Type check

The death conditions apply within a single domain. The next question is whether the structure translates across domains. Eilenberg & Mac Lane (1945): functors preserve composition. If domain A (neurons) and domain B (immune system) both implement six morphisms with compatible type signatures, the mapping between them is a candidate functor: object map, morphism map, composition preservation. Verifying this requires defining both categories explicitly. The vocabulary makes the translation precise enough to attempt.

Prior art:
- Phillips & Wilson (2010) — categorical cognition, representations not flow
- Coecke (2010) — DisCoCat, syntax → semantics functors, meaning not processing
- Rosen (1991) — (M,R)-systems, biological closure, not pipeline composition
- Spivak (2013) — operad of wiring diagrams, composable modules, not cognitive
- Bradley (2021) — enriched categories of language, probability as hom-objects, semantics not processing
- Desimone & Duncan (1995) — biased competition, empirical mechanism, no math
- Reynolds & Heeger (2009) — normalization model of attention, quantitative but not categorical

The gap we see: the sequential processing pipeline as morphisms in a Markov category with traced feedback across domains. Phillips did representations. Coecke did meaning. Rosen did closure. Bradley did semantics. Desimone & Duncan did mechanism. This is flow.

### Hard question, answered

Research asks: "construct η and μ explicitly and prove the monad laws." The Giry monad provides them. Dirac delta and integration. These are well-defined, natural, and have clear information-processing interpretations. The monad laws hold for the Giry monad. This is proven mathematics (Giry 1982).

The six steps are morphisms inside the Giry monad's Kleisli category. The composition argument is by induction. Base case: one cycle. Six contract-preserving morphisms compose; each postcondition matches the next precondition; Remember's output matches Perceive's input.

Inductive step: if cycle *n* preserves all contracts, cycle *n+1* preserves them, because contract preservation is a property of each morphism, not of the cycle count. The derivation in [The Natural Framework](/the-natural-framework) provides the base case: roles of this shape must exist. The induction shows that if they compose once, they compose forever. The data processing inequality provides the constraint. The falsification test is the contrapositive: replace one contract, observe death.

### Objections

**"These are just state transformers, not categorical morphisms."**
State transformers with no contract are arbitrary self-maps. The distinction between a morphism that preserves postconditions and one that doesn't is the distinction between a loop that lives and one that dies.

Stoch provides the ambient category: measurable spaces and Markov kernels. The contracts (parseable, retrievable, diverse, etc.) are semantic predicates imposed on top, not structure that Stoch itself encodes. Formalizing them requires further refinement: a subcategory, a fibration, or a logical relation. The vocabulary is precise enough to diagnose. The existence proofs and induction proof are complete. Formalizing the contracts as categorical structure is the remaining work.

**"Survival does not prove the monad laws."**
Correct. The monad laws hold for the Giry monad independently (Giry 1982). Survival is evidence that the six steps compose well within the monad: the information budget balances. The monad is the container; the steps are the contents.

**"The biology/society examples are cherry-picked."**
The framework predicts: a singly recursive loop with a broken step is more likely to compound than self-correct, because the broken postcondition feeds a broken precondition on the next cycle.

Every historical failure is multi-causal. The prediction is falsifiable: find a singly recursive loop where a broken contract self-corrects without external repair. The theory was induced from a decade of [reflecting](/reflecting) posts: observations about teams, organizations, and systems that broke the same way. The math came after, not before.

**"Real systems persist first, then compact later. Logs, databases, brains."**
Those systems are stacked pipes operating on different types.

A database "persists" a row, but the row is Cache in the larger pipeline. The CRM's Remember is the customer relationship, not the database record. A log "persists" events, but that's Cache for the monitoring pipe. The actual Remember is the alert rule or the postmortem finding. The brain's sensory trace "persists" briefly, but that's Cache. The actual Remember is consolidated long-term memory. Every "persist first, compact later" example, under analysis, is Cache at one level being confused with Remember at a higher level. The type mismatch is the tell: if the thing being persisted is a representation rather than the final entity, it's Cache, not Remember.

**"Consolidate is lossy; Remember is lossless. But persistence is never truly lossless."**
Lossless means lossless relative to the compressed representation. Consolidate changes the representation (lossy). Remember persists whatever Consolidate outputs without further transformation (lossless relative to its input). The contract is "no additional loss at this step." Remember is not a separate store; it is the historically shaped substrate, the part of the medium that carries the system's past forward. DNA, the connectome, the published archive. Still an endomorphism, same type in and out, but with the longest time constant. Timescale is the diagnostic; the contract is the definition.

**"Filter and Attend could be one step."**
They operate on different stores. Filter gates the data stream: does this item pass the criterion? Attend reads the policy store and applies it: given the survivors, which are worth pursuing? One is per-item admissibility. The other is slate-level ranking with diversity. Merging them conflates "does it pass?" with "how does it relate to everything else that passed?" Those are different questions with different inputs. [The Parts Bin](/the-parts-bin) catalogs operations for each. The catalogs do not overlap.

Every interface in the pipeline is a handshake. The postcondition of one step is the precondition of the next. What remains is to fill the slots.

*Continued in [The Parts Bin](/the-parts-bin).*

---

*Written via the [double loop](/double-loop).*
