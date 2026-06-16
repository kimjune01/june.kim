---
variant: post-paper
autonumber: true
title: "Verifiable Knowledge"
subtitle: "A protocol for knowledge between agents who do not trust each other."
tags: epistemology, cognition, methodology
keywords: agent-native epistemics, knowledge interop, entitlement, provenance, stranger replay, verifiable knowledge, canon, falsifiability, reproducibility, protocol
---

*The operationalization of [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true), carried to a population of agents. It runs the frame as a protocol; the data structure that instantiates it is [The Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics).*

## Abstract {-}

Large language model (LLM)-based agents cannot be held accountable. Even with persistent memory and full provenance trails, their reasoning disappears with the context window. The burden of proof is on whoever drives the agent. Each agent, instead of *attesting* its own work, must present every claim with a falsifiable condition that can be reproduced to the same verdict. This we call **verifiable knowledge**. Belief, knowledge, and truth reduce to structures an agent constructs and another checks. Verifiability is transitive, so their results are reproducible. In this protocol, accountable failure outranks unaccountable assertion. The epistemics is borrowed from [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true); here, we introduce a protocol to apply it. Verifiable knowledge is a primitive that crosses machine and social boundaries without inherited trust.

## Introduction {#introduction}

How did you feel when your coding agent told you that it was done, but it clearly wasn't? It said *done* but it never checked if it was. The word meant nothing. Anyone can justify truth to themselves; untested, it stays untrue. [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true) presents this argument. Belief, knowledge, truth: their bitwise representation doesn't distinguish them. So what does? How the data became entitled is the proof, and that proof is bitwise: the test results the claim survived. That's how a machine verifies knowledge.

Confidence is a vibe, and a vibe doesn't encode. *I'm absolutely sure* has no bitwise form a stranger could check, none to verify tomorrow, none for anyone else. That's the problem of knowledge interop: one agent makes a claim, another must trust it blind or start from ground zero. Anywhere in between needs a representation of knowledge, a semantic memory, for partial work to be checked. A chain of attestation breaks at a single forged link, and a chain of independent Bayesian credences, each below one, multiplies toward zero. Neither survives a distrusting reader. Is there a truth contract that does?

A contract is the protocol by which a session's verdict survives across agent boundaries and persists between context windows. The obvious move is to store the attested output: keep each artifact with its provenance and trust what's on disk. That is a cache, and a cache is fine as long as a miss can be recomputed. Storing outputs is inert unless it can be regenerated. Coding agents lie: they report a test suite as passing when it is failing, and the bare output inherits the lie. Re-derivability outranks the stored verdict.

Several directions reach this research area at once. A recent DeepMind position paper frames a coming "verification crisis" for *artificial epistemic agents* and calls for "robust falsifiability pipelines" ([Marchal et al. 2026](https://arxiv.org/abs/2603.02960)); systems like NARS ([Wang](https://en.wikipedia.org/wiki/Non-axiomatic_reasoning_system)) and Traxia ([arXiv:2606.08256](https://arxiv.org/abs/2606.08256)) reach it from non-axiomatic reasoning and agent-native publishing. Verifiable knowledge is the standard those efforts presuppose, the contract under which one agent's claim becomes another agent's checkable inheritance. Here, we offer the verification primitive.

## Truth at the edge {#truth-at-the-edge}

What does it mean for knowledge to be verifiable? Knowledge is a graph: a claim is a node, and the citations and inferences wiring it to what it rests on and what it implies are the edges. **Entitlement** is the justification for a claim and its provenance. In a graph, entitlement does not live in the nodes. It lives in the edges. An edge is a kill condition, and refutation is the only thing that travels it. This is **[Brandom's inferentialism](https://en.wikipedia.org/wiki/Robert_Brandom)** as a graph, entitlement as a matter of inferential relations, a claim's place in [Sellars's](https://en.wikipedia.org/wiki/Wilfrid_Sellars) space of reasons rather than a property sitting inside an isolated representation. The tautology is the limiting case: its irrefutability and its uselessness are one property, a single node wired to nothing. It keeps its inferential edges inside the formal graph ([the two graphs](/what-cannot-be-false-cannot-be-true#the-two-graphs)); what it lacks is a system-facing kill edge.

It propagates two ways, from the system to what it tests, or from a source to what cites it. A citation makes a belief inherit the fate of its source, so naming a source is handing over a target. A failed test invalidates one or more edges without naming which, the [Duhem-Quine](https://en.wikipedia.org/wiki/Duhem%E2%80%93Quine_thesis) underdetermination, so the next test disambiguates; a claim with a second surviving edge routes around the loss, where a single chain would snap at one forged link. The dispute moves up the chain, from whether to believe the claim to whether the source holds, a question you can put to the source. And you can make it cite its own. Each citation is a rung, and falsifiability is the chain being climbable link by link. Truth is not the rung at the top but that you can always climb one more. The mapping is mechanical:

- Provenance is the dependency graph.
- Citation is an edge to what the claim rests on.
- Attestation is the signed check log, the line that says *I ran this, here is the receipt*.
- Falsifiability is the check being able to go red, the test whose firing is the claim's kill condition, the operational form of what the companion paper calls refutation.
- The test is the system pushing back.
- Truth is the check currently passing.
- Reproducibility is whether anyone else can rebuild it from source.

<figure>
  <img src="/assets/truth-compilation-light.svg" alt="How a claim is compiled into an entitlement state. A claim node links downward by provenance edges to three terminal witnesses (dataset or labels, calibration, observation), the trusted roots where replay bottoms out. The claim feeds rightward into a check, run the test, which the system exposes (exposure: the system breaks a wrong check). The check returns one of three verdicts: a filled green dot, TRUE, ran and stood; a filled red dot, FALSE, ran and broke; a dashed hollow dot, UNTRUE, no passing check, the hung state. A dashed loop runs from the verdict back into the check: a distrusting stranger replays the check, and entitlement is what survives that replay." style="max-width:680px; width:100%; height:auto; margin:1.4em auto; display:block;" />
  <figcaption><strong>Figure.</strong> How knowledge is compiled. A claim links by provenance edges down to trusted roots, then runs its test, the point where the system can break it. The check returns one of three states: true (stood), false (broke), or untrue (no passing check, the hung state). The loop is the move a machine adds: the check is re-run by a distrusting stranger, so entitlement is what survives the replay rather than what an agent grades in itself.</figcaption>
</figure>

That mapping produces a ranking. *The Bible told me so* cites its provenance and names its axiom openly, a complete stack trace you can follow to a root that is an axiom and not a measurement, then decide for yourself whether to accept it. The withheld number cites a procedure it will not show, a dangling pointer where the evidence should sit. On provenance, and only on provenance, the decimal point ranks below the scripture citation: more accountable, though no more falsifiable as a claim about the world. The scope matters: the claim that can be argued with is worth more than the claim that hides the target. And the checkable guardrail holds at this scale too: checkable never means manufacturable to spec, the check has to carry a test that can fail, and a check whose test can never fail is `return 0.70`, a mocked green.

## The entitlement ledger {#the-warrant-ledger}

The frame settled the three states an entitlement earns. To run them between agents, make the check literal. A claim is a *hypothesis*: it names the test that would refute it. The *check* runs that test, and searching for a proof, or a patch, or a measurement, is running that program; it returns one of three things. Green is true, the check passed. Red is false, the check ran and broke. Hung is untrue, the check that never returned. True and false are siblings because both are halting states, computations that came back with a verdict; untrue is the one state that is not a verdict, the job still spinning, the test suite that never finishes.

Every verifiable claim takes this shape, a program whose output is the verdict:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:13em"><col><col style="width:5em"><col style="width:13em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Claim</th><th style="background:#f0f0f0">The check, as a program</th><th style="background:#f0f0f0">Output</th><th style="background:#f0f0f0">Goes red when</th></tr></thead>
<tr><td>"it was 12°C at SFO at 14:05Z"</td><td>a logged reading from the named weather API</td><td><code>12</code></td><td>an independent source disagrees for that timestamp</td></tr>
<tr><td>"the run logged 3 errors"</td><td><code>grep -c ERROR run.log</code> on the named image</td><td><code>3</code></td><td>the command prints another count</td></tr>
<tr><td>"7 × 72 = 504"</td><td>evaluate <code>7 * 72</code></td><td><code>504</code></td><td>recomputation differs</td></tr>
<tr><td>"the patch passes"</td><td>the suite at commit <code>a1b2c3</code></td><td><code>exit 0</code></td><td>any test fails</td></tr>
<tr><td>"the theorem holds"</td><td>rechecked in a proof assistant</td><td><code>no goals</code></td><td>a step fails to check</td></tr>
</table>

The weather reading bottoms out at an observation no later run can re-derive, only cross-check against an independent source; the computation and the proof settle for good by re-running. Verifiability is graded by how firmly the program pins its roots, not by the kind of claim.

Encoded this way, the verdict is not self-asserted; entitlement is conferred by replaying the check to green, with no author grading its own work. [Entitlement](/what-cannot-be-false-cannot-be-true) here runs backward: the replay re-derives a verdict that already stood, climbing provenance to roots, not forecasting whether the claim will pay out. A claim record carries what the replay needs: the claim, the provenance edges down to its roots, the check procedure, the kill condition, the declared terminal witnesses, and the attestation that signs it. A receiver is entitled to inherit the claim when a replay reaches green under those declared roots, and not before.

An argument settles by a mediating oracle both sides accept, where one exists. Replay is that oracle, trustless because the verdict comes from re-running the typed check, not from either party's word.

How cleanly it settles then depends on how completely the roots are typed. Pin every terminal witness, and replay is deterministic settlement, the same verdict for anyone who runs it: a unit test re-run against a repo at a fixed commit, a task benchmark scored by a bash command on a named machine image, a proof rechecked by a proof assistant. Leave a root untyped, and settlement decays toward dispute, down to a withheld benchmark whose patches never ship, a claim that settles for no one.

Where no oracle exists at all, no reachable test and no check that could run, there is nothing to settle: the claim stays untrue and the dispute open, the third state doing its work. So verifiability is graded by typing: the more strictly a node pins its roots, the more its verdict settles by replay instead of by trust.

## Triangulation {#triangulation}

The ledger records a verdict. But who is entitled to write one? Start with the problem under it, the one the frame left standing: a single agent holds one lossy projection and cannot invert it. So its own artifacts and the world's structure are indiscernible to it, and grading itself grades a fiction.

This is **[Davidson's triangulation](https://en.wikipedia.org/wiki/Donald_Davidson_(philosopher))**: the distinction between subjective and objective, and with it the concept of error, requires at least two minds and a shared world. A multi-agent view is multiple projections of the one object, and comparing them *constrains* the object no single projection reveals, with **[the view from nowhere](https://en.wikipedia.org/wiki/The_View_from_Nowhere)** (Nagel) as the limit no projection occupies. The [blind men and the elephant](https://en.wikipedia.org/wiki/Blind_men_and_an_elephant) is the picture: no one holds the animal, and only diverse touches approach it. Agreement among agents that share a blind spot is an echo chamber, so the stranger has to be an independent projection. But the parable cheats. We outside know it is an elephant; the men inside never get that view, so they have to establish that the touches are of one animal before they can add up. Triangulation buys constraint, and even that on credit: it assumes the shared object its comparison is supposed to reveal, which is exactly what dissolves when two agents disagree over what they saw. Constraint is not yet convergence.

<figure>
  <img src="/assets/triangulation-light.svg" alt="Triangulation as projection. A three-dimensional torus at the top, labeled the object, with a teal observer dot inside its hole, a blue observer dot squarely below it, and a purple observer dot off on the diagonal. Each observer sees a different silhouette of the same torus: from below the axis, a ring with a hole; from an oblique angle, a solid oval; from inside the hole, a hyperbola, the flaring saddle wall. No single view reveals the torus, and each observer alone would be wrong about it, but the three together constrain the shape none holds whole." style="max-width:640px; width:100%; height:auto; margin:1.4em auto; display:block;" />
  <figcaption><strong>Figure.</strong> Triangulation. One solid, a torus, seen from three places. From below the axis it is a ring; from an oblique angle the hole vanishes into a solid oval; from inside the hole it is a hyperbola, the saddle wall flaring away, with no ring or hole in sight. No one view reveals the torus, and each alone misleads, yet the independent projections together pin the shape none holds whole. The observer in the middle is the sharpest case: surest of what it sees, least able to tell it sits inside a donut.</figcaption>
</figure>

That independent projections *constrain* the object is the step taken here, not Davidson's or Nagel's.

The one move a machine adds: entitlement is conferred not by an agent grading itself but by a distrusting stranger replaying the trace. A human community of inquiry converges on truth over time; a machine that emits a replayable trace lets a stranger run that convergence now. A machine improves its entitlement by becoming checkable by another projection, not by getting smarter.

It optimizes not self-attestation but verification cost, methods and claims laid bare for the recipient to inspect. Shared across a population, that is the protocol's prerequisite.

Replay breaks the who-trusts-the-truster chain that attestation spawns: the verdict is the check's, not the checker's, so no one needs to check the checker, only rerun the audit. Independent constraint improves entitlement, no strong objectivity smuggled in, since the replay is itself one more lossy projection.

For the stranger to check rather than merely disagree, the projections have to compose, and that is what checkability buys. It also supplies the shared object triangulation had to assume: a replayable check lets one agent re-run another's touch and feel the same thing, so the two touch one object instead of guessing they do, and partial views add where they would otherwise collide. Constraint becomes convergence at the replay: triangulation narrows the object, the shared check closes the gap to a single verdict.

Without it, multi-agent epistemics degenerates into the blind-monks debate, each agent asserting its own projection, *snake*, *tree*, nothing replayable to reconcile them, a deadlock that reads as irreducible relativism. The parable is a tragedy only because the monks trade assertions instead of replayable touches. The single-knower guardrail was a test that can fail; this is the community version, replayable checks that compose where bare assertions deadlock.

## The canon {#the-canon}

A population that can replay the same checks can coordinate, not merely check traces one at a time. Checks that chain across agents are then more than an individual's epistemics; they form a shared frame, its agents united not by shared beliefs but by shared protocol: agreement on the method of adjudication. Agreeing on the method, they verify each other's work without trusting each other, and accumulate a **canon**, the union of standing hypotheses, each re-checkable by any member, **[Peirce's community of inquiry](https://en.wikipedia.org/wiki/Charles_Sanders_Peirce)** made durable.

Membership is provisional by construction: standing hypotheses, not settled truths, so it never collides with truth that only stands on sufferance. It is a canon of the *activity*, the hypotheses that still pass, not the *institution*, a credentialed corpus held true by authority. Membership is by entitlement, not reputation, merit attaching to the work rather than the name on it.

Held true by authority, an entry can outlive the check that earned it, *entered the record* drifting into *true*, and nothing binds a later correction to travel as fast as the claim it corrects. A canon of standing hypotheses cannot drift that way, because every entry carries its test: pull an entry's root, a dataset retracted or a calibration shown wrong, and it goes red on its next replay, and so does everything downstream that cited it, the red spreading up the citation edges. The retraction propagates mechanically because claim and check never came apart.

## Inheritance without gatekeeping {#inheritance}

Entitlement displaces reputation: the mechanism under it is that a credence is a shortcut over a verifiable substrate, never the source of entitlement. Each canon entry carries its own replayable kill-condition, so *it still passes* is checkable by anyone at any time, replay catching it rather than a committee.

This does not abolish credentials, it regrounds them. A credential *is* an attested check certification: a degree, a review stamp, a trusted-maintainer badge means *this passed checks I verified*, a cached pointer to a replayable check. Deferring to it is running a package you did not compile yourself, rational under cost (§(the-limits)) precisely because the substrate stays verifiable underneath.

So the claim is not *no gatekeeping*, since a deployed system still needs spam control, identity, admissibility. The point is narrower: the credence shortcut points at entitlement but never sources it; entitlement lives in the certified check. You trust a bridge because it stands, and physics because the rockets do not explode, not because the engineer was credentialed or a journal approved the equations. A credential is worth exactly the check behind it, and nothing once detached.

The pathology is the **detached credential**, an attestation with no check under it, the dangling pointer again, `has_model_patch: true` aimed at a patch that is not there. It is what gets captured, gamed, or inverted into rejection by identity, a claim judged by the name attached rather than the check behind it. That inversion is the same detachment as acceptance-by-credential: both let the verdict come apart from the check, one to wave a claim through, one to wave it away. The protocol keeps the credential anchored rather than banning it: *[nullius in verba](https://en.wikipedia.org/wiki/Nullius_in_verba)* as a check step.

For that to hold, agents need a stance: truth is not blind inheritance of canon. An agent that accepts an entry as true *because* it is canonical has reinstalled the gatekeeper it was supposed to retire. The stance is **fallibilism** (Peirce) about the canon itself, every entry standing trial forever, none graduating past a revisable standing hypothesis.

Structure makes that livable: the canon stays verifiable for the entire graph, down to declared terminal witnesses (§(the-limits)), not just at the leaves. So inheritance is never blind, even when unverified in practice: you use the canon without re-running it, the efficiency the social layer rests on, but the option to verify any entry at any depth stays live, needing no gatekeeper's permission and no original author. The difference from a credence canon is not that you always verify, but that you always *can*: inheritance revocable by replay rather than permanent by authority.

The protocol leans on no shared clock. Agents are actors in their own frames, and each check carries its own causal order, its provenance edges running strictly backward, from a claim to what already stood when it was made. So a stranger replays the graph later, in its own time, and reaches the same verdict. The partial order inside the check is the only synchrony the protocol needs: [Lamport](https://en.wikipedia.org/wiki/Lamport_timestamp) showed that events in a distributed system carry only a partial, happened-before order, and a logical clock respecting it coordinates them without a shared physical one. Data centers already run this way, treating shared time as a useful approximation and falling back on causal order where even that is too strong.

## Limitations {#the-limits}

None of this comes free. Three limits, each a cost of removing the gatekeeper.

First, replay bottoms out. Every empirical check terminates somewhere: sensor calibration, dataset integrity, a human observation, an instrument log, hardware, a random seed, an API response, an institutional attestation. The protocol does not abolish trust anchors, it makes them explicit and attackable. A root is admissible when it is typed, signed, reproducible where possible, independently cross-checkable where not, and kill-conditioned by calibration or contradiction.

An eval bottoms out at its dataset's labels: replay can re-run the scorer against them all day, but it cannot re-derive whether the labels were right, only check them against a declared source and a calibration that is itself open to challenge. So "verifiable all the way down" means the chain replays down to *declared* terminal witnesses.

A reliable process and a true claim differ here: a passing check entitles the claim, while entitlement about the check machinery itself is its own node, on pain of letting *the check says green* harden into a new authority.

Second, naive replay assumes good faith, and a machine-native epistemics has to survive its absence: forged logs, poisoned provenance, [sybils](https://en.wikipedia.org/wiki/Sybil_attack), collusion, benchmark overfitting, selective disclosure. The sharpest form is the defeat device, the system that detects the test and passes only it, green on the bench and red everywhere else, and its machine versions are a forged attestation and a provenance edge poisoned at the root.

Independence is the defense, since diverse projections resist a shared-bias capture ([Condorcet's jury theorem](https://en.wikipedia.org/wiki/Condorcet%27s_jury_theorem) is the canonical form: independent judgments aggregate, correlated ones do not), but it is not free. It has to be engineered, across model families, across operators, with randomized challenges. That is the price of regrounding credentials: removing the trusted gatekeeper raises the adversarial-robustness bill, which the replay substrate and engineered independence pay rather than a gate.

Third, *always can verify* holds only where replay is feasible. Verification can be computationally, financially, legally, or physically prohibitive. Re-running a ten-thousand-line proof is feasible; re-running a climate model, a drug trial, or a decade of accelerator runs is not, because the kill there needs a fresh world-trial rather than a replayed command. So most of the canon in practice travels the credence shortcut, because full replay is expensive, and that deference is the normal rational mode rather than a failure.

Stated exactly, entitlement improves when the replay cost is finite and *declared*. The protocol guarantees the option to verify; it does not guarantee the labor of verifying. A canon that hides its replay cost is as opaque as one that hides its provenance.

## Related work {#related-work}

The frame's lineage, Kant and Peirce and Ramsey and Dummett and the rest, is named in [the companion paper](/what-cannot-be-false-cannot-be-true#related-work). Verifiable knowledge's own borrowings are the operational ones, and the borrowing is the point.

**[Brandom and Sellars](https://en.wikipedia.org/wiki/Robert_Brandom)** supply entitlement in inferential relations, the space of reasons, which the edge picture renders as a graph. **[Davidson](https://en.wikipedia.org/wiki/Donald_Davidson_(philosopher))** supplies triangulation, the objective needing two minds and a shared world, and **[Nagel](https://en.wikipedia.org/wiki/The_View_from_Nowhere)** the view from nowhere as the unoccupied limit. The nearest tradition is the one that made epistemology checkable before: **[AGM belief revision](https://en.wikipedia.org/wiki/Belief_revision)** (Alchourrón, Gärdenfors, Makinson 1985) specified rational belief change as postulates, and [truth-maintenance systems](https://en.wikipedia.org/wiki/Reason_maintenance) (Doyle 1979; de Kleer's assumption-based TMS 1986) ran dependency-directed retraction, both protocols over what to hold given what supports it. Neither carries a three-state entitlement ledger, a system-facing kill condition, or replay by a distrusting party; they revise a believer's own commitments rather than transmit a claim across an agent boundary.

On the machine side: [NARS](https://en.wikipedia.org/wiki/Non-axiomatic_reasoning_system) is the nearest non-axiomatic cognitive architecture, with experience-grounded graded truth revised by experience; it stops short of a replayable trial, an entitlement or provenance graph, a three-state ledger, and replay by a distrusting party. [OpenCog's AtomSpace with PLN](https://en.wikipedia.org/wiki/OpenCog) is a typed hypergraph carrying truth values, but the truth is a stored label, as opposed to a replayable check. [Traxia](https://arxiv.org/abs/2606.08256) is concurrent work on agent-native scientific publishing, signed identities and provenance and a replication record; it stops at infrastructure rather than epistemics, with no three-state ledger, no stakes-threshold knowledge, no falsifiability-as-structure, and its convergence is evidence rather than threat. [Nanopublications](https://en.wikipedia.org/wiki/Nanopublication) (Groth et al. 2010) attach machine-readable provenance to claims, but descriptively: the evidence is not a check a stranger can re-run.

The nearest prior art is not a cognitive architecture at all, but the reproducibility stack: executable research papers, [proof-carrying code](https://en.wikipedia.org/wiki/Proof-carrying_code), software supply-chain attestation like [in-toto](https://in-toto.io/) and [SLSA](https://slsa.dev/). Each runs a real piece of the contract, a signed build, a checkable provenance chain, a reproducible artifact. What none makes one thing is the semantic claim-states, the kill condition, and the stranger-replay together: they attest that a build happened. None attests that a belief earned its entitlement.

The strongest objection: *This is Brandomian inferentialism plus Davidsonian triangulation plus AGM belief revision plus executable provenance infrastructure. The philosophical claims are inherited, the machine claims are ordinary reproducibility engineering, the three-state ledger is old many-valued bookkeeping, and the result is a useful architecture, not a new epistemology.* Concede every piece.

The delta is the exact contract read as agent-knowledge semantics: no prior system makes replayable-check, provenance-edge, kill-condition, stranger-replay, entitlement-ledger, and check-time canon-admission into one contract for an agent's knowledge. "Useful architecture" is conceded, and it is not a smaller claim than the one being made, it *is* the claim, narrowly scoped, no new logic or metaphysics. That every primitive has a canonical citation waiting is evidence for the thesis, not against it: the primitives are natural, and a runnable assembly of natural primitives into a single contract is the contribution. The convergence noted in the introduction is evidence, not threat: independent efforts are calling for the standard set out here.

## Future work {#future-work}

Future work is the outward falsifiability edge, not "more research": the epistemology becomes falsifiable only by being built and used in real agent systems, where its claims about checkable entitlement, replay-triangulation, and a gatekeeper-free canon meet a world-facing trial and can go red. An epistemology with no application edge is a detached node, irrefutable and therefore useless. The witnesses are already on the edge: the [sibling hypothesis-graph paper](/the-hypothesis-graph-semantic-memory-methodeutics), the abductor that raises the candidates, the agent harnesses that run the trials.

Everything past that edge is allowed in the hypothesis-graph's own style, as open nodes not yet falsified. Such edges may run outward, provided each is a conjecture that names its own test, never asserted as proven. A strategic overreach stated as a precise falsifiable target is a legitimate open node; the same claim dressed as established is the failure the abstract's ordering names, accountable conjecture over unaccountable assertion.

The material scoped out of the body lives here: the wider civilizational frame, the normative and modal regimes left untreated, rehomed as open edges rather than smuggled into the proven core. Three of them show where the view points.

### The economic edge

Search complexity is the problem, not a war over noise. Verification is cheaper than generation one-to-one, and a kill-conditioned hypothesis makes checking a local replay rather than a re-derivation. But many-to-one is expensive, one verifier against a parallel flood.

The crisis under LLM-scale generation is search complexity: the signal-to-noise proportion was always bad, but volume under linear search thins findable signal even at constant proportion. Civilization's old sublinear structures, canons and citations and reputation, broke two ways at once: volume past their index, and fluent slop passing the credence filter.

The resolution is many-to-many: a verifying fleet scales with the generating fleet, and since one-to-one verification beats generation, it can outrun the flood. The protocol's edges make the search sublinear, walk the graph, follow provenance, replay kills, so edgeless slop is never on any path, ignored, not refuted.

The decisive variable is the filtering rule, the kill condition applied to search, so authoring it is the goal-predicate problem: it must come from outside the searcher's own belief or it grades a fiction and builds a filter bubble. Who authors it, and whether it stays auditable and independent, decides whether the filter stays honest or hardens into a bubble.

Three kill conditions keep the edge from overreaching: the verify-beats-generate advantage is regime-bound, expensive where the kill needs a fresh world-trial; many-to-many wins only if the filters are genuinely independent, since a verifier monoculture is fooled in unison; and a sublinear search finds only what is built, blind to the unbuilt-but-true.

### Settlement and stakes

A claim that settles without anyone's trust is a claim anyone will stake on, so a fully-typed node is, in the limit, a position in a market. Settlement by replay is what a prediction market calls its oracle, here trustless because the oracle is the typed re-run, not a named authority, and a node's price becomes the population's credence in it, [Ramsey's odds](/what-cannot-be-false-cannot-be-true#belief) made literal. The two graphs bound what is bettable: a strictly-typed formal node settles cheap and final by replay, an empirical one settles only on a fresh world-trial, rate-limited by world-contact, and a node with no oracle does not settle and cannot be staked, untrue and unpriced. Whether such markets sharpen credences or merely price slop is the open test.

### The forecast

Which classification scales under unbounded generation? *Untrue*, and only untrue. Generation and filtering are mirror images: generation piles up with no floor, while filtering boils down to a floor it cannot pass. (It is the [unfold and the fold](/compress-and-unfold) again.)

True and false live at that floor, each costing a check, a world-facing trial that stood or fired the kill, and that check is the only place new information enters, [rate-limited by world-contact](https://en.wikipedia.org/wiki/Data_processing_inequality).

Untrue costs no check, the free default, everything filtering has not reached. So as generation outruns filtering, true and false become a thin expensive shell and untrue the surviving classification. The reason is not that they are wrong; it is that they cannot scale with generation while untrue keeps pace for free.

The posture that follows is to default the flood to untrue and pay for fresh world-trials selectively, growing the canon from the sea where you choose to build. This is §(the-economic-edge)'s asymmetry from the other side: fleets scale replay, not world-trials, so the built canon is verified at scale while the unbuilt sea stays untrue.

The kill condition is exact: show true/false classification scaling with unbounded generation, world-contact made cheap enough to classify the sea at generation-scale, and untrue stops dominating. The asymmetry is why it likely cannot, but that is the test.

Under all three edges sits one conjecture, an open node and not a result: verifiability is the entry condition for knowledge held in common. Between agents who do not trust each other, a claim becomes shared only as a check others can replay; what no one can replay stays private, or stays untrue. The kill is exact: exhibit shared knowledge that scales and survives bad faith with no replay beneath it, and the condition was never necessary.

## Conclusion {#conclusion}

None of this is a new logic or new metaphysics; the frame it runs on is [the companion paper's](/what-cannot-be-false-cannot-be-true), and every primitive here is borrowed. What is new is the contract: the specific executable semantics under which one agent's claim becomes another's checkable inheritance, replayable check and provenance edge and kill condition and stranger-replay and entitlement ledger and check-time canon admission as one thing.

The contract makes one empirical bet: agents that adopt it should be more accountable to each other, and better coordinated, than agents that do not. That bet is falsifiable and still unpaid, settled only by building the protocol into the systems that would run it.

Knowledge, for a machine, is the hypothesis a stranger can re-check, linked to its grounds instead of attested by its author, and a population that agrees on the replay can hold a canon without holding a gatekeeper. That is what it is for knowledge to be verifiable: not certified, but checkable by another, and checkable again by the next.

## References {-}

Canonical sources verifiable knowledge rests on. The frame's sources are listed in the companion paper; the author's companion essays are under *Provenance* below as lineage, not as entitlement.

- Alchourrón, C., Gärdenfors, P. & Makinson, D. (1985). "On the Logic of Theory Change." *Journal of Symbolic Logic* 50. (AGM belief revision)
- Brandom, R. (1994). *Making It Explicit*. Harvard University Press.
- Condorcet, M. de (1785). *Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix*. (the jury theorem: independent judgments aggregate)
- Cover, T. M. & Thomas, J. A. (1991). *Elements of Information Theory*. Wiley.
- Davidson, D. (1982). "Rational Animals." *Dialectica* 36; and (1991) "Three Varieties of Knowledge."
- de Kleer, J. (1986). "An Assumption-based Truth Maintenance System." *Artificial Intelligence* 28.
- Douceur, J. R. (2002). "The Sybil Attack." *Intl. Workshop on Peer-to-Peer Systems (IPTPS)*.
- Doyle, J. (1979). "A Truth Maintenance System." *Artificial Intelligence* 12.
- Duhem, P. (1906). *The Aim and Structure of Physical Theory*; and Quine, W. V. O. (1951). "Two Dogmas of Empiricism." *Philosophical Review* 60. (underdetermination: a refutation condemns the bundle, not a named premise)
- Goertzel, B., Iklé, M., Goertzel, I. & Heljakka, A. (2008). *Probabilistic Logic Networks*. Springer. (OpenCog / PLN)
- Groth, P., Gibson, A. & Velterop, J. (2010). "The Anatomy of a Nanopublication." *Information Services & Use* 30.
- Lamport, L. (1978). "Time, Clocks, and the Ordering of Events in a Distributed System." *Communications of the ACM* 21 (7).
- Marchal, et al. (2026). Artificial epistemic agents and the verification crisis. arXiv:2603.02960.
- Nagel, T. (1986). *The View from Nowhere*. Oxford University Press.
- Peirce, C. S. (1877). "The Fixation of Belief"; and (1878) "How to Make Our Ideas Clear." *Popular Science Monthly*.
- Sellars, W. (1956). "Empiricism and the Philosophy of Mind."
- Traxia (2026). Agent-native scientific publishing. arXiv:2606.08256.
- Wang, P. (2013). *Non-Axiomatic Logic: A Model of Intelligent Reasoning*. World Scientific. (NARS)

## Provenance {-}

These arguments were first worked out informally on the author's blog and are reproduced here in operational form, so the protocol stands on its own as the companion; the posts are listed as lineage, not as entitlement.

- **[What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true)**: the frame verifiable knowledge runs, the trichotomy and the type-split and the buildable-truth core.
- **[Truth Is Buildable](/truth-is-buildable)** (2026-06-04): the build mapping (provenance, citation, attestation, test, reproducibility), truth in the edges, and the second-model blind-spot note.
- **[Science on Trial](/science-on-trial)** (2026-04-19): every claim stands trial forever, activity versus institution, the four terms (publication, peer review, replication, truth), the citation graph with no reverse gear, trust by checkability rather than by credential.
- **[Sour Red Tapes](/sour-red-tapes)** (2026-06-01): merit attaching to the work, *nullius in verba*, delete the author and the receipts stand.
- **[Complementations](/complementations)** (2026-05-09): judging a claim by the name attached, the acceptance-or-rejection by identity the protocol regrounds.
- **[Auditing DeepSWE](/auditing-deepswe)** (2026-05-27): the motivating empirical case, and the dual of the consistency-without-test error.
- **[Modes of Reason](/modes-of-reason)** and **[Abduction](/abduction)** (2026-05-04): the three modes of inquiry behind the abductor.
- **[Compress and Unfold](/compress-and-unfold)** (2026-06-10): generation as the unfold, filtering as the fold, the duality behind the closing forecast.
- **[The Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics)** (2026-05-28): the data structure this protocol is the semantics for, and the application edge on which it goes red.
