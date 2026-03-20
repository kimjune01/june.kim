---
layout: post-wide
title: "Type Forcing"
tags: cognition
---

*Part of the [cognition](/cognition) series.*

Category theory gives you the space of all valid compositions. It says nothing about which compositions physics permits. This post applies three physical constraints to [Spivak's operad of wiring diagrams](https://arxiv.org/abs/1305.0297) and watches the search space collapse.

## The formalism

[Spivak's operad](https://arxiv.org/abs/1305.0297) gives you boxes with typed ports and wiring diagrams that connect them. The only constraint is type matching. If the types match, the wire is valid. If they don't, the wire doesn't exist. An **algebra** assigns behavior to each box — syntax is what can plug into what; semantics is what each box does. His rigidity results ([Propositions 3.1.2, 3.1.4](https://arxiv.org/abs/1305.0297)) show that once you fix the algebra, there is almost no room to simplify it.

[Rupel and Spivak](https://arxiv.org/abs/1307.6894) add **direction** (ports are inputs or outputs; a **supplier assignment** maps each demand to exactly one supply of matching type) and **delay nodes** (feedback with one tick of temporal delay, modeling cross-cycle connections). The acyclic sub-operad forbids loops in the forward pass; delay nodes are the only path backward. [Spivak's open dynamical systems](https://arxiv.org/abs/1408.1598) add **internal state**: a box's behavior depends on state the wiring doesn't see.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Concept</th><th style="background:#f0f0f0">What it does</th></tr></thead>
<tr><td><a href="https://arxiv.org/abs/1305.0297">Typed wiring diagrams</a></td><td>Connect boxes through type-matched ports. The search space of valid topologies.</td></tr>
<tr><td><a href="https://arxiv.org/abs/1305.0297">Algebra</a></td><td>Assigns behavior to each box. Syntax vs semantics.</td></tr>
<tr><td><a href="https://arxiv.org/abs/1307.6894">Supplier assignment</a></td><td>Maps each input demand to exactly one output supply of matching type.</td></tr>
<tr><td><a href="https://arxiv.org/abs/1307.6894">Delay nodes</a></td><td>Feedback with one tick of temporal delay. Cross-cycle connections.</td></tr>
<tr><td><a href="https://arxiv.org/abs/1408.1598">Internal state</a></td><td>State variable (S, f) that influences behavior without appearing as a wire.</td></tr>
<tr><td><a href="https://arxiv.org/abs/1305.0297">Rigidity</a></td><td>Once you fix the algebra, almost no room to simplify.</td></tr>
</table>

Six boxes with typed ports admit many valid wirings — chains, rings, stars, fan-out trees, arbitrary cross-connections. Everything that type-checks is legal.

Now apply physics.

## Constraint 1: temporal flow

Information processing takes time. A morphism receives input at time *t* and emits output at *t+δ*, where δ > 0. Outputs follow inputs. The temporal wiring diagram operad encodes this: wires flow from outputs to inputs, and the acyclic sub-operad forbids instantaneous loops.

Feedback exists. Consolidate writes to the policy store, which parameterizes the next cycle's forward pass. This crosses a cycle boundary: the update is state evolution, not a forward wire. The forward pass is acyclic; the backward pass is a state update between cycles.

**Consequence:** the search space shrinks from "all type-valid wirings" to "all type-valid *acyclic* forward wirings, plus delay nodes for feedback."

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/type-forcing-temporal.svg" alt="Six boxes in a forward chain. Backward arrows are crossed out. One dashed blue line shows state evolution across the cycle boundary." style="width:100%; display:block;">
</div>

## Constraint 2: bounded storage

Any physical system has finite state space; the environment includes everything it does not. dim(Environment) > dim(System). A morphism must bridge this gap: that is Perceive, and the bridge is a surjection — it must lose information.

Inputs arrive faster than outputs drain, so by [pigeonhole](https://en.wikipedia.org/wiki/Pigeonhole_principle) something must hold the excess — that is Cache. Cache requires write and read interfaces. The write interface is concurrent with Perceive: new items arrive while old items are being read, forcing invariants on the Cache type (atomicity, ordering) that downstream types don't carry.

If the loop feeds back, the last step's output must persist across the cycle boundary. That is Remember. Bounded storage forces selection before persistence, or the store grows without bound.

**Consequence:** Perceive (type bridge), Cache (pigeonhole buffer), and Remember (loop closure) are forced. Each has a postcondition the others cannot provide. Three distinct types: *encoded*, *indexed*, *persisted*.

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/type-forcing-bounded.svg" alt="Six boxes. Perceive, Cache, and Remember are highlighted blue with their types labeled. Three boxes remain as dashed outlines with question marks." style="width:100%; display:block;">
</div>

## Constraint 3: [Landauer's principle](https://en.wikipedia.org/wiki/Landauer%27s_principle)

Erasing one bit costs at least *kT* ln 2 joules. Every lossy morphism in the pipeline erases bits and dissipates heat. Combined with bounded storage and temporal flow, this produces three consequences.

**Selection must follow encoding** (temporal flow + Landauer)**.** Choosing what to encode requires selection; selection requires encoding. Circular. Temporal flow resolves it: encode first, then select. The projection is lossy because bridging dim(Environment) > dim(System) erases bits (Landauer sets the floor).

Within a cycle, the encoding cannot depend on that cycle's selection outcome. Across cycles, the policy store parameterizes the projection — Perceive adapts, but only from prior policy state, never from the current cycle's downstream results.

**A gate exists** (bounded storage + Landauer)**.** Lossy steps erase bits (Landauer) and a bounded store cannot accumulate indefinitely (bounded storage), so something must discard. That is Filter — stateless, rule-based. Its postcondition is *gated*: the indexed set minus items that failed a threshold. Cache is a live, mutable, concurrent store; Filter's output is a frozen, read-only snapshot. The concurrency invariants are forced by the access pattern, not the implementation.

**Control must separate from data** (all three)**.** Landauer sets the dissipation floor; in any finite realization, thermal fluctuations perturb the implementation, so data varies. Bounded storage forces eviction: high-volume items crowd out low-volume ones. Together: if policy shares a pool with data, the selection process amplifies salient data and suppresses the rest. Over iterations this creates selection drift — policy migrates toward whatever is salient, not whatever is effective. Co-storage cannot guarantee policy persistence.

This forces two more morphisms. Attend reads from the policy store and ranks the gated set; its postcondition is *ranked*. Consolidate reads persisted outcomes, aggregates them, and compresses them into a [sufficient statistic](https://en.wikipedia.org/wiki/Sufficient_statistic) — parameter updates, not episodes. Its postcondition is *policy*: parametric, not episodic. Many episodes in, one parameter update out.

Consolidate updates the policy store, a partition of the substrate that parameterizes Perceive, Filter, and Attend together. After it runs, Filter's threshold shifts, Attend's ranking criteria change, and Perceive's encoding adapts. Contracts are fixed; behavior evolves. In Spivak's formalism:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:10em"><col style="width:7em"><col style="width:10em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Spivak term</th><th style="background:#f0f0f0">Framework term</th><th style="background:#f0f0f0">Changes across cycles?</th></tr></thead>
<tr><td>Which boxes, which wires</td><td>Operad</td><td>Pipeline</td><td>No (type-forced)</td></tr>
<tr><td>What each box does</td><td>Algebra</td><td>Contracts + behavior</td><td>Contracts fixed, behavior evolves</td></tr>
<tr><td style="font-style:italic">Shared parameters</td><td style="font-style:italic">State variable S</td><td style="font-style:italic">Policy store (partition of substrate)</td><td style="font-style:italic">Updated by Consolidate each cycle</td></tr>
</table>

The operad is fixed. The algebra evolves. Consolidate moves the system through valid algebras by updating the policy store. The type boundary between *persisted* and *policy* is the boundary between episodic data and behavior-shaping state.

**Consequence:** three more morphisms are forced — Filter (gate), Attend (policy read), Consolidate (policy write). Three more types are distinct: *gated*, *ranked*, *policy*. Total: six types.

<div style="max-width:700px; margin:1.5em auto;">
<img src="/assets/type-forcing-landauer.svg" alt="All six boxes highlighted blue with types labeled. A policy store bar below shows Consolidate writing and Perceive, Filter, and Attend reading from it." style="width:100%; display:block;">
</div>

## The collapse

**Corollary.** Given six already-distinct boundary contracts (derived above), uniqueness of the forward wiring follows. Assumptions:
1. Six boxes with directed typed ports (Rupel-Spivak temporal wiring diagrams).
2. Six pairwise-distinct boundary types, each appearing exactly once as an output and once as an input.
3. Each box has arity 1 and coarity 1 in the forward pass.
4. Feedback is cross-cycle state evolution (no instantaneous loops in the forward pass).
5. Policy access is internal state, not a forward wire.

The unique forward acyclic wiring is the chain: Perceive → Cache → Filter → Attend → Remember → Consolidate. Consolidate's policy update propagates through S.

The proof is a counting argument on the supplier assignment. Perceive outputs *encoded*; only Cache accepts it. Cache outputs *indexed*; only Filter accepts it. The chain propagates. Six output types, six input types, each matching exactly one partner. No degrees of freedom.

The forward wiring is handled by temporal wiring diagrams (Rupel-Spivak). The cross-cycle policy update is internal state evolution (Vagner-Spivak-Lerman): Consolidate updates S, and the next cycle's forward morphisms read from it. Distinct forward types prevent feedback *between* boxes — no two match.

This post identifies operad port labels with postcondition contracts from [The Handshake](/the-handshake), which pick out physically distinct state classes derived in [The Natural Framework](/the-natural-framework). The constraints above argue for distinctness; the identification is the content of those two posts.

<div class="table-wrap">
<table style="max-width:70%; margin:0 auto; font-size:14px;">
<thead>
<tr>
<th style="background:#f0f0f0">Boundary</th>
<th style="background:#f0f0f0">Port type</th>
<th style="background:#f0f0f0">What changes</th>
<th style="background:#f0f0f0">Derived from</th>
<th style="background:#f0f0f0">Why distinct</th>
</tr>
</thead>
<tbody>
<tr>
<td>Perceive → Cache</td>
<td>encoded → indexed</td>
<td>Data structure added</td>
<td>Bounded storage: pigeonhole</td>
<td>Storage adds a retrieval interface.</td>
</tr>
<tr>
<td>Cache → Filter</td>
<td>indexed → gated</td>
<td>Live store → frozen subset</td>
<td>Bounded storage + Landauer: finite store, lossy steps, something must discard</td>
<td>Concurrent store vs read-only snapshot.</td>
</tr>
<tr>
<td>Filter → Attend</td>
<td>gated → ranked</td>
<td>Policy dependence added</td>
<td>All three: variance + bounded storage + competition</td>
<td>No preference vs policy-derived ordering.</td>
</tr>
<tr>
<td>Attend → Remember</td>
<td>ranked → persisted</td>
<td>Transient → durable</td>
<td>Bounded storage: loop closure</td>
<td>Transient dies at cycle boundary; durable survives.</td>
</tr>
<tr>
<td>Remember → Consolidate</td>
<td>persisted → policy</td>
<td>Data → control</td>
<td>All three: variance + eviction + selection drift</td>
<td>Episodic (what happened) vs parametric (how to process).</td>
</tr>
</tbody>
</table>
</div>

You cannot gate what hasn't been indexed. You cannot rank what hasn't been gated. You cannot persist what hasn't been ranked. You cannot consolidate what hasn't been persisted. Each operation requires the previous one's output.

The search space started vast. Three constraints (temporal flow, bounded storage, Landauer's principle) forced six distinct types. Six distinct types in a directed typed operad with arity-1 boxes forced a unique forward acyclic wiring. Given the assumptions above, the pipeline is not a design choice. It is the last wiring standing when the search space collapses.

## What remains open

The type-forcing argument constrains topology, not multiplicity. It says nothing about *how many* instances of each box exist. An immune system doesn't run one Filter. It runs millions of clonal competitions in parallel. Each instance has the same type signature and follows the chain. Parallelism is many chains, not a different topology.

But do parallel chains interact? The types match (both chains use the same six types), so the operad permits inter-chain wiring. It constrains *which roles* can connect, not *which instances*. Whether inter-chain wiring introduces new degrees of freedom or collapses to independent chains is the question [Spivak's operads](https://arxiv.org/abs/1305.0297) were built to answer.

One chain's Remember feeds the next level's Perceive. That's the functor between categories in [The Natural Framework](/the-natural-framework). The operad's composition-via-pushout means the cross-level wiring is well-defined. And the type-forcing argument applies again at the next level: the same three physical constraints, the same six distinct types, the same unique chain. Every level of the tower is forced by the same argument that forced the first. The recursion terminates because each level is strictly lossy (Filter erases information) and physical systems have a resolution floor ([Bekenstein bound](https://en.wikipedia.org/wiki/Bekenstein_bound), Planck scale). A strictly decreasing sequence bounded below is finite. The tower ends.

### What this post does not prove

The self-similar claim is the boldest one here, and it lacks the rigor to back it up. The corollary is conditional: it takes six distinct types as given and shows the wiring is forced. Proving those types are distinct *in the operad* is argued but not formalized. The identification of port labels with postcondition contracts with physical state classes is the central controversial move, and it rests on [The Handshake](/the-handshake) and [The Natural Framework](/the-natural-framework), not on this post. The control/data separation uses a stability argument (selection drift), not a theorem. The operadic proof — stating the physical constraints as predicates on the algebra and showing the self-similar chain is the unique fixed point at every level — is not yet written. That proof requires tools this post can only point to. This post is the argument for why it should exist.

---

## Appendix: what the formalism gives back

The operad sharpens the pipeline claim and resolves ambiguities the framework carried informally.

### Syntax and semantics separate

The framework conflated two claims: the wiring is forced, and the contracts are forced. The operad splits them. Syntax (what plugs into what) is unique. Semantics (what each box does) vary by domain: neurons, databases, immune systems instantiate different algebras on the same forced wiring. The contracts constrain which algebras are valid.

One forced syntax, many valid algebras, contracts as the constraint. That is why the same pipeline appears across [twenty-four domains](/the-natural-framework) with different implementations. The operad makes this a definition.

### Compositionality becomes axiomatic

When [The Handshake](/the-handshake) says "five morphisms compose forward," what does "compose" mean? In prose, it's a metaphor. In the operad, it's a pushout — a universal construction that glues cables from inner boxes into the outer diagram. Associativity holds by universal property. The handshake itself — postcondition of step N is the precondition of step N+1 — is a supplier assignment ([Rupel-Spivak §2](https://arxiv.org/abs/1307.6894)). The metaphor becomes a theorem.

### The backward pass has a formal home

Five forward, one backward. "Consolidate is the cron job" is intuitive but informal. Delay nodes ([Rupel-Spivak §2.3](https://arxiv.org/abs/1307.6894)) formalize it: an element in both demand and supply, one tick of temporal delay. The forward/backward distinction becomes structural: forward wires are acyclic; feedback is a delay node. The asymmetry is in the operad.

### Internal state solves the arity problem

Attend reads policy from the substrate — a second input that would break arity-1. Spivak's open dynamical systems ([§3](https://arxiv.org/abs/1408.1598)) resolve it: a box's behavior depends on internal state (S, f) that the wiring diagram doesn't touch. The policy store is S. It influences Attend without appearing as a wire, so the arity-1 forward pass stays clean.

### The fractal tower is the holarchic property

A composed system becomes a box wirable into a larger system. That is Spivak's holarchic property: composition via pushout produces an element of G(Y), the same kind of object as any primitive system. [The Natural Framework](/the-natural-framework) calls this the fractal tower: one level's Remember feeds the next level's Perceive. Same structure, different vocabulary. The holarchic property is why the type-forcing argument recurses.

### Rigidity propagates

Spivak's rigidity results ([Propositions 3.1.2, 3.1.4](https://arxiv.org/abs/1305.0297)) show Rel_A admits no nontrivial algebra morphisms — once you fix the relational algebra, there is almost no room to simplify it. If the physical constraints select a specific algebra, the rigidity propagates. Implementations are constrained by contracts, contracts by physics. [The Parts Bin](/the-parts-bin) catalogs operations for each role, and the catalogs do not overlap. Rigidity is the operadic explanation.

---

*Written via the [double loop](/double-loop).*
