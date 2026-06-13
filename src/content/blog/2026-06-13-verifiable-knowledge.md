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

Large language model (LLM)-based agents cannot be held accountable. Even with persistent memory and full provenance trails, what they reasoned is as ephemeral as the context window, and their stochasticity makes it unrepeatable. The burden of proof is on whoever drives the agent; this is unavoidable. Each agent, instead of *attesting* its own work, must present every claim with a falsifiable condition that can be reproduced to the same verdict. This we call **verifiable knowledge**. Belief, knowledge, and truth reduce to structures an agent constructs and another checks; checking is transitive, so a population that shares the method holds a canon without a gatekeeper; accountable failure outranks unaccountable assertion. The epistemics is borrowed from [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true); here, we introduce a protocol to apply it. As its primitive, verifiable knowledge crosses machine and social bounds without inherited trust, the unit a data structure can carry.

## Introduction {#introduction}

A single mind can assemble every structure an epistemology needs and certify none of it, because it can only ever grade its own projection against itself. That is where [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true) ends, and where this paper begins. Take its frame as given: belief is a graded bet, knowledge is belief you have exposed by acting on it, truth is a build the world has not broken, and a claim no test has reached is untrue, the three held in a ledger of entitlement rather than a logic. The frame is what truth *is* for a machine. This paper is what it takes to *run* it between machines.

The job is knowledge interop. An agent makes a claim; another agent, which has no reason to trust it, has to tell which of the three states the claim earned without taking the first agent's word. Trusting the source does not scale and does not survive bad faith. The alternative is to link instead of attest: belief, knowledge, and truth each reduce to a structure one agent constructs and a stranger checks, and the reduction is the contribution. Justified true belief does not run as written; parts have run before, graded belief by the Bayesians, entitlement-as-process by the reliabilists, but never the whole arc as a single contract.

What that contract specifies is a protocol: the semantics that a build, an edge, and a verdict must carry for entitled knowledge to move between agents and survive the crossing. The structure that instantiates it is the [hypothesis graph](/the-hypothesis-graph-semantic-memory-methodeutics); deploying it is future work. The territory is being reached from several directions at once. A recent DeepMind position paper frames a coming "verification crisis" for *artificial epistemic agents* and calls for "robust falsifiability pipelines" ([Marchal et al. 2026](https://arxiv.org/abs/2603.02960)); systems like NARS ([Wang](https://en.wikipedia.org/wiki/Non-axiomatic_reasoning_system)) and Traxia ([arXiv:2606.08256](https://arxiv.org/abs/2606.08256)) reach it from non-axiomatic reasoning and agent-native publishing. This paper states the standard those efforts presuppose: the contract under which one agent's claim becomes another agent's checkable inheritance.

## Truth at the edge {#truth-at-the-edge}

Start with what a single agent can put on the table, before any stranger arrives. Where does entitlement live in a build? Knowledge is a graph: a claim is a node, and the citations and inferences wiring it to what it rests on and what it implies are the edges. Entitlement does not live in the nodes. It lives in the edges. This is **[Brandom's inferentialism](https://en.wikipedia.org/wiki/Robert_Brandom)** in graph clothing, entitlement as a matter of inferential relations, a claim's place in [Sellars's](https://en.wikipedia.org/wiki/Wilfrid_Sellars) space of reasons rather than a property sitting inside an isolated representation. The tautology is the limiting case, a single node wired to nothing, and its irrefutability and its uselessness are one property rather than two. It keeps its inferential edges inside the formal graph ([the two graphs](/what-cannot-be-false-cannot-be-true#the-two-graphs)); what it lacks is a world-facing kill edge.

The edge does specific work. A citation makes a belief inherit the fate of its source, so naming a source is handing over a target. The dispute moves up the chain, from whether to believe the claim to whether the source holds, a question you can put to the source, which can be made to cite its own. Each citation is a rung, falsifiability is the chain being climbable link by link, and truth is not the rung at the top but the fact that you can keep climbing. That is the whole mapping, and it is mechanical:

- Provenance is the dependency graph.
- Citation is an edge to what the claim rests on.
- Attestation is the signed build log, the line that says *I built this, here is the receipt*.
- Falsifiability is the build being able to go red, the test whose firing is the claim's kill condition, the operational form of what the companion paper calls refutation.
- The test is the world pushing back.
- Truth is the build currently passing.
- Reproducibility is whether anyone else can rebuild it from source.

<figure>
  <img src="/assets/truth-compilation-light.svg" alt="How a claim is compiled into an entitlement state. A claim node links downward by provenance edges to three terminal witnesses (dataset or labels, calibration, observation), the trusted roots where replay bottoms out. The claim feeds rightward into a build step, run the test, which the world exposes (exposure: the world breaks a wrong build). The build returns one of three verdicts: a filled green dot, TRUE, built and stood; a filled red dot, FALSE, built and broke; a dashed hollow dot, UNTRUE, no passing build, the hung state. A dashed loop runs from the verdict back into the build: a distrusting stranger replays the build, and entitlement is surviving the replay, not the self-grade." style="max-width:680px; width:100%; height:auto; margin:1.4em auto; display:block;" />
  <figcaption><strong>Figure.</strong> How knowledge is compiled. A claim links by provenance edges down to trusted roots, then runs its test, the point where the world can break it. The build returns one of three states: true (stood), false (broke), or untrue (no passing build, the hung state). The mapping above is this pipeline read off its parts. The loop is the move a machine adds: the build is re-run by a distrusting stranger, so entitlement is what survives the replay rather than what an agent grades in itself. The figure spans the paper, the edges of §(truth-at-the-edge), the three states of §(the-warrant-ledger), and the replay of §(triangulation), in one frame.</figcaption>
</figure>

That mapping produces a ranking. *The Bible told me so* cites its provenance and names its axiom openly, a complete stack trace you can follow frame by frame to a root that is an axiom and not a measurement, then decide for yourself whether to accept it. The withheld number cites a procedure it will not show, a dangling pointer where the evidence should sit. On provenance, and only on provenance, the decimal point ranks below the scripture citation: more accountable, though no more falsifiable as a claim about the world. The scope matters, because the claim that can be argued with is worth more than the claim that hides the thing you would argue with. And the buildable guardrail holds at this scale too: buildable never means manufacturable to spec, the build has to carry a test that can fail, and a build whose test can never fail is `return 0.70`, a mocked green.

## The entitlement ledger {#the-warrant-ledger}

The frame settled the three states as statuses an entitlement earns. To run them between agents, make the build literal. Searching for a proof, or a patch, or a measurement, is running a program, and it returns one of three things. Green is true, the build closed. Red is false, the build ran and broke. Hung is untrue, the build that never returned. True and false are siblings because both are halting states, computations that came back with a verdict; untrue is the one state that is not a verdict, the job still spinning, the test suite that never finishes.

Every verifiable claim takes this shape, a program whose output is the verdict:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:13em"><col><col style="width:5em"><col style="width:13em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Claim</th><th style="background:#f0f0f0">The build, as a program</th><th style="background:#f0f0f0">Output</th><th style="background:#f0f0f0">Goes red when</th></tr></thead>
<tr><td>"it was 12°C at SFO at 14:05Z"</td><td>a logged reading from the named weather API</td><td><code>12</code></td><td>an independent source disagrees for that timestamp</td></tr>
<tr><td>"the run logged 3 errors"</td><td><code>grep -c ERROR run.log</code> on the named image</td><td><code>3</code></td><td>the command prints another count</td></tr>
<tr><td>"7 × 72 = 504"</td><td>evaluate <code>7 * 72</code></td><td><code>504</code></td><td>recomputation differs</td></tr>
<tr><td>"the patch passes"</td><td>the suite at commit <code>a1b2c3</code></td><td><code>exit 0</code></td><td>any test fails</td></tr>
<tr><td>"the theorem holds"</td><td>rechecked in a proof assistant</td><td><code>no goals</code></td><td>a step fails to check</td></tr>
</table>

The weather reading bottoms out at an observation no later run can re-derive, only cross-check against an independent source; the computation and the proof settle for good by re-running. Verifiability is graded by how firmly the program pins its roots, not by the kind of claim.

Encoded this way, the verdict is no longer something an agent asserts about itself; the entitlement is conferred by replaying the build to green, with no builder grading its own work. [Entitlement](/what-cannot-be-false-cannot-be-true) here runs backward: the replay re-derives a verdict that already stood, climbing provenance to roots, not forecasting whether the claim will pay out. A claim record carries what the replay needs: the claim, the provenance edges down to its roots, the build procedure, the kill condition, the declared terminal witnesses, and the attestation that signs it. A receiver is entitled to inherit the claim when a replay reaches green under those declared roots, and not before.

An argument settles by a mediating oracle both sides accept, where one exists, and replay is that oracle, trustless because the verdict comes from re-running the typed build, not from either party's word.

How cleanly it settles then depends on how completely the roots are typed. Pin every terminal witness, and replay is deterministic settlement, the same verdict for anyone who runs it: a unit test re-run against a repo at a fixed commit, a task benchmark scored by a bash command on a named machine image, a proof rechecked by a proof assistant. Leave a root untyped, and settlement decays toward dispute, down to the [withheld benchmark](/auditing-deepswe) whose patches never ship, a claim that settles for no one.

Where no oracle exists at all, no reachable test and no build that could run, there is nothing to settle: the claim stays untrue and the dispute open, the third state doing its work. So verifiability is graded by typing: the more strictly a node pins its roots, the more its verdict settles by replay instead of by trust. The rest of the paper makes the replay trustworthy between parties that do not trust each other.

## Triangulation {#triangulation}

The ledger records a verdict. But who is entitled to write one? That gap is what the rest of the paper has to close. Start with the problem under it, the one the frame left standing: a single agent holds one lossy projection and cannot invert it, so its own artifacts and the world's structure are indiscernible to it, and grading itself grades a fiction.

This is **[Davidson's triangulation](https://en.wikipedia.org/wiki/Donald_Davidson_(philosopher))**: the distinction between subjective and objective, and with it the concept of error, requires at least two minds and a shared world. A multi-agent view is multiple projections of the one object, and comparing them constrains the object no single projection reveals, with **[the view from nowhere](https://en.wikipedia.org/wiki/The_View_from_Nowhere)** (Nagel) as the limit no projection occupies. The [blind men and the elephant](https://en.wikipedia.org/wiki/Blind_men_and_an_elephant) is the picture: no one holds the animal, and the touches together approach it, but only diverse projections refine, and agreement among agents that share a blind spot is an echo chamber, so the stranger has to be an independent projection.

<figure>
  <img src="/assets/triangulation-light.svg" alt="Triangulation as projection. A three-dimensional torus at the top, labeled the object, with a teal observer dot inside its hole, a blue observer dot squarely below it, and a purple observer dot off on the diagonal. Each observer sees a different silhouette of the same torus: from below the axis, a ring with a hole; from an oblique angle, a solid oval; from inside the hole, a hyperbola, the flaring saddle wall. No single view reveals the torus, and each observer alone would be wrong about it, but the three together constrain the shape none holds whole." style="max-width:640px; width:100%; height:auto; margin:1.4em auto; display:block;" />
  <figcaption><strong>Figure.</strong> Triangulation. One solid, a torus, seen from three places. From below the axis it is a ring; from an oblique angle the hole vanishes into a solid oval; from inside the hole it is a hyperbola, the saddle wall flaring away, with no ring or hole in sight. No one view reveals the torus, and each alone misleads, yet the independent projections together pin the shape none holds whole. The observer in the middle is the sharpest case: surest of what it sees, least able to tell it sits inside a donut.</figcaption>
</figure>

A [small instance](/truth-is-buildable) shows the shape: tracing one phrase's origin, a second model searching independently surfaced a source the first had missed, and the agreement that followed meant something precisely because the two were not the same projection. That independent projections *constrain* the object is the paper's own step, not something to lay on Davidson or Nagel, cited only for the narrow premise.

The solution is the one move a machine adds. Entitlement is conferred not by an agent grading itself but by a distrusting stranger replaying the trace. A human community of inquiry converges on truth over time; a machine that emits a replayable trace lets a stranger run that convergence now. A machine improves its entitlement by becoming checkable by another projection, never by getting smarter.

What it optimizes is not the certainty of its self-attestation but the cost of its verification, methods and claims laid bare for the recipient to inspect. Take that as shared across a population, and you have the protocol, its one prerequisite.

Replay breaks the who-trusts-the-truster chain that attestation spawns: the verdict is the build's, not the checker's, so no one needs to check the checker. An audit anyone reruns, instead of an authority anyone trusts. Independent constraint improves entitlement, no strong objectivity smuggled in, since the replay is itself one more lossy projection.

For the stranger to check rather than merely disagree, the projections have to compose, and that is what buildability buys. A replayable build lets one agent re-run another's touch and feel the same thing, so partial views add instead of colliding: a stranger replays one command and inherits the result without re-deriving it.

Without it, multi-agent epistemics degenerates into the blind-monks debate, each agent asserting its own projection, *snake*, *tree*, nothing replayable to reconcile them, a deadlock that reads as irreducible relativism. The parable is a tragedy only because the monks trade assertions instead of replayable touches. Buildability converts the standoff of subjective views into the convergence of triangulation. The single-knower guardrail was a test that can fail; this is the community version, replayable builds that compose where bare assertions deadlock.

## The canon {#the-canon}

What does a population gain from builds it can all replay? More than checking each other one trace at a time: it can coordinate. The hypothesis graph is then more than an individual's epistemics; it is a shared frame, its agents united not by shared beliefs but by shared protocol: agreement on the method of adjudication, not on conclusions. Agreeing on the method, they verify each other's work without trusting each other, and accumulate a **canon**, the union of standing builds, each replayable by any member, **[Peirce's community of inquiry](https://en.wikipedia.org/wiki/Charles_Sanders_Peirce)** made durable.

Membership is provisional by construction, a canon of standing builds and not settled truths, so it never collides with the asymptote. This dissolves an old worry: it is a canon of the *[activity](/science-on-trial)*, the builds that still pass, not the *institution*, a credentialed corpus held true by authority. Membership is by entitlement, not reputation, merit attaching to the work rather than the name on it.

The institution is what a discipline collapses into when it forgets the difference, training its reader to read *entered the record* as *true*. A canon of standing builds cannot, because every entry carries the test. Pull an entry's root, a dataset retracted or a calibration shown wrong, and it goes red on its next replay, and so does everything downstream that cited it, the red flowing up the edges the citations drew.

The institution has no such reverse gear, the retraction filed and never enforced, the correction never propagating as fast as the claim. The canon propagates it mechanically, because it never let the claim come apart from its build.

## Inheritance without gatekeeping {#inheritance}

Entitlement displaces reputation: the mechanism under it is that a credence is a shortcut over a verifiable substrate, never the source of entitlement. Each canon entry carries its own replayable kill-condition, so *it still passes* is checkable by anyone at any time, caught by replay rather than by a committee.

This does not abolish credentials, it regrounds them. A credential *is* an attested build certification: a degree, a review stamp, a trusted-maintainer badge means *this passed builds I verified*, a cached pointer to a replayable build. Deferring to it is the download button on a package you did not compile yourself, rational under cost (§(the-limits)) precisely because the substrate stays verifiable underneath.

So the claim is not *no gatekeeping*, since a deployed system still needs spam control, identity, admissibility. It is that the credence shortcut points at entitlement and never sources it, which lives in the build the credential certifies. You trust a bridge because it stands, and physics because the rockets do not explode, not because the engineer was credentialed or a journal approved the equations. A credential is worth exactly the build behind it, nothing once detached from one.

The pathology is the **detached credential**, an attestation with no build under it, the dangling pointer again, `has_model_patch: true` aimed at a patch that is not there, which is what gets captured, gamed, or curdled into [rejection by identity](/complementations), the reflexive *I won't read AI slop*. The protocol's job is to keep the credential anchored, not to ban it, *[nullius in verba](https://en.wikipedia.org/wiki/Nullius_in_verba)* turned into a build step.

For that to hold, agents have to do more than run the machinery; they have to adopt a stance: truth is not blind inheritance of canon. An agent that accepts an entry as true *because* it is canonical has reinstalled the gatekeeper it was supposed to retire. The stance is **fallibilism** (Peirce) about the canon itself, every entry standing trial forever, none graduating past a revisable standing build.

What makes that livable rather than exhausting is structural: the canon stays verifiable for the entire graph, down to declared terminal witnesses (§(the-limits)), not just at the leaves. So inheritance is never blind, even when unverified in practice: you use the canon without re-running it, the efficiency the social layer rests on, but the option to verify any entry at any depth stays live, needing no gatekeeper's permission and no original author. The difference from a credence canon is not that you always verify. It is that you always *can*, inheritance revocable by replay rather than permanent by authority.

One loose end, for the reader who presses it: the protocol leans on no shared clock. Agents are actors in their own frames, and each build carries its own causal order, the provenance edges running strictly from a claim to what was already established when it was made. So a stranger replays the graph later, in its own time, and reaches the same verdict, the partial order inside the build being the only synchrony knowledge interop ever needs. Data centers already run this way, keeping a shared time as a serviceable fiction and falling back on causal order where even that is too strong.

## Limitations {#the-limits}

Does any of this come free? Three limits keep the previous two sections from reading as utopian, each a cost of removing the gatekeeper.

First, replay bottoms out. Every empirical build terminates somewhere: sensor calibration, dataset integrity, a human observation, an instrument log, hardware, a random seed, an API response, an institutional attestation. The protocol does not abolish trust anchors, it makes them explicit and attackable. A root is admissible when it is typed, signed, reproducible where possible, independently cross-checkable where not, and kill-conditioned by calibration or contradiction.

An eval bottoms out at its dataset's labels: replay can re-run the scorer against them all day, but it cannot re-derive whether the labels were right, only check them against a declared source and a calibration that is itself open to challenge. So "verifiable all the way down" means the chain replays down to *declared* terminal witnesses, not verification resting on no anchor at all.

This is also where the difference between a reliable process and a true claim lives: a passing build entitles the claim, while entitlement about the build machinery itself is its own node, on pain of letting *the build says green* harden into a new authority.

Second, naive replay assumes good faith, and a machine-native epistemics has to survive its absence: forged logs, poisoned provenance, sybils, collusion, benchmark overfitting, selective disclosure. The sharpest form is the defeat device, the build that detects the test and passes only it, green on the bench and red everywhere else, and its machine versions are a forged attestation and a provenance edge poisoned at the root.

Independence is the defense, since diverse projections resist a shared-bias capture, but independence is not free. It has to be engineered, across model families, across operators, with randomized challenges. That is the price of regrounding credentials: removing the trusted gatekeeper raises the adversarial-robustness bill, and it is paid by the replay substrate and by engineered independence rather than by a gate.

Third, *always can verify* holds only where replay is feasible. Verification can be computationally, financially, legally, or physically prohibitive. Re-running a ten-thousand-line proof is feasible; re-running a climate model, a drug trial, or a decade of accelerator runs is not, because the kill there needs a fresh world-trial rather than a replayed command. So most of the canon is in practice inherited through the credence shortcut, because full replay is expensive, and that deference is the normal rational mode rather than a failure.

Stated exactly, entitlement improves when the replay cost is finite and *declared*. The protocol guarantees the option to verify; it does not guarantee the labor of verifying. A canon that hides its replay cost is as opaque as one that hides its provenance.

That is the whole mechanism, limits and all. What is left is to set it beside its neighbors, turn it on itself, and point it at the world.

## Related work {#related-work}

The frame's lineage, Kant and Peirce and Ramsey and Dummett and the rest, is named in [the companion paper](/what-cannot-be-false-cannot-be-true#related-work). This paper's own borrowings are the operational ones, and the borrowing is the point, so name them.

**[Brandom and Sellars](https://en.wikipedia.org/wiki/Robert_Brandom)** supply entitlement in inferential relations, the space of reasons, which the edge picture wears in graph clothing. **[Davidson](https://en.wikipedia.org/wiki/Donald_Davidson_(philosopher))** supplies triangulation, the objective needing two minds and a shared world, and **[Nagel](https://en.wikipedia.org/wiki/The_View_from_Nowhere)** the view from nowhere as the unoccupied limit. The nearest tradition is the one that made epistemology buildable before: **[AGM belief revision](https://en.wikipedia.org/wiki/Belief_revision)** (Alchourrón, Gärdenfors, Makinson 1985) specified rational belief change as postulates, and [truth-maintenance systems](https://en.wikipedia.org/wiki/Reason_maintenance) (Doyle 1979) ran dependency-directed retraction, both protocols over what to hold given what supports it. Neither carries a three-state entitlement ledger, a world-facing kill condition, or replay by a distrusting party; they revise a believer's own commitments rather than transmit a claim across an agent boundary.

On the machine side, the neighbors. [NARS](https://en.wikipedia.org/wiki/Non-axiomatic_reasoning_system) is the nearest non-axiomatic cognitive architecture, with experience-grounded graded truth revised by experience; it stops short of a replayable trial, an entitlement or provenance graph, a three-state ledger, and replay by a distrusting party. [OpenCog's AtomSpace with PLN](https://en.wikipedia.org/wiki/OpenCog) is a typed hypergraph carrying truth values, but the truth is a stored label, as opposed to a replayable build. [Traxia](https://arxiv.org/abs/2606.08256) is concurrent work on agent-native scientific publishing, signed identities and provenance and a replication record; it stops at infrastructure rather than epistemics, with no three-state ledger, no stakes-threshold knowledge, no falsifiability-as-structure, and its convergence is evidence rather than threat. [Nanopublications](https://en.wikipedia.org/wiki/Nanopublication) (Groth et al. 2010) attach machine-readable provenance to claims, but descriptively: the evidence is not a build a stranger can re-run.

And the nearest prior art is not a cognitive architecture at all; it is the reproducibility stack: executable research papers, [proof-carrying code](https://en.wikipedia.org/wiki/Proof-carrying_code), software supply-chain attestation like [in-toto](https://in-toto.io/) and [SLSA](https://slsa.dev/). Each runs a real piece of the contract, a signed build, a checkable provenance chain, a reproducible artifact. What none makes one thing is the semantic claim-states, the kill condition, and the stranger-replay together: they attest that a build happened. None attests that a belief earned its entitlement.

Here is the worst thing you can say about the paper, said as nastily as it goes. *This is Brandomian inferentialism plus Davidsonian triangulation plus AGM belief revision plus executable provenance infrastructure. The philosophical claims are inherited, the machine claims are ordinary reproducibility engineering, the three-state ledger is old many-valued bookkeeping, and the result is a useful architecture, not a new epistemology.* Concede every piece. The concession is the strength.

The delta is the exact contract read as agent-knowledge semantics: no prior system makes replayable-build, provenance-edge, kill-condition, stranger-replay, entitlement-ledger, and build-time canon-admission into one contract for an agent's knowledge. "Useful architecture" is conceded, and it is not a smaller claim than the one being made, it *is* the claim, narrowly scoped, no new logic and no new metaphysics. That every primitive has a canonical citation waiting is evidence for the thesis, not against it: the primitives are natural, and a runnable assembly of natural primitives into a single contract is the contribution. And the convergence the introduction noted, several independent efforts reaching this same territory, is evidence and not threat: they are calling for the standard this paper states.

## Self-application and falsifiers {#self-application}

What does the three-state hypothesis rest on? Induction from the record. The inductive sample is mathematics, the cleanest case, where every theorem was once an untrue conjecture, [Fermat's](https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem) for three centuries, and some conjectures met a counterexample and turned false, the migrations running untrue toward true or false through builds and never once by fiat. The scope on the sample: empirical claims can move from true to false as well, and even a [published proof can later be invalidated](https://en.wikipedia.org/wiki/Four_color_theorem), Kempe's four-color proof standing eleven years before it fell, so the formal case is the cleanest direction rather than the only one. That regularity is the evidence and, in the same breath, the falsifier.

The discipline the paper applies to itself is verb-scoping: every claim's verb is scoped to what its evidence supports, and *presents as knowledge* is that reflex turned on other people's claims. And the paper names what would turn it red, in its own three-state vocabulary:

- Show an entitled claim that arrived with no build, granted true with no chain anyone could climb, and the operationalization goes red.
- Show the dignity ordering ranking an openly labeled conjecture below a bold falsehood *after* the qualifier is applied, and that contribution falls.
- Force the three-state ledger to behave as an object-level logic, assigning the third value inside the claim language rather than in the entitlement ledger, and "not a new logic" collapses into [Łukasiewicz](https://en.wikipedia.org/wiki/%C5%81ukasiewicz_logic) and the delta vanishes.
- Exhibit a machine that runs justified true belief or correspondence directly, reading off whether a belief matches the world in itself, and the unrunnability claim that motivates the whole paper falls.
- Cite a prior system that already makes the operationalization-plus-ledger-plus-ordering combination a single semantic contract, and the novelty defense falls by citation; the nearest engineering prior art to aim that at is the supply-chain attestation lineage, in-toto and SLSA, proof-carrying code, executable research papers, so the contract has to be shown to be more than those assembled.
- Show that agents on the protocol coordinate no better than agents without it, and the interop claim is empty where it matters.

The largest of them is the outward one: deploy the framework in real agent systems and find that the claimed accountability and coordination do not emerge, that agents on the protocol are no more checkable or better-coordinated than agents without it, and the operationalization delta is empty where it matters most, in application.

That last falsifier is less a worry to manage than the paper's own next move.

## Future work {#future-work}

Future work is the outward falsifiability edge. The epistemology becomes falsifiable by being built and used in real agent systems, the hypothesis graph and the abductor and the multi-agent canon, where its claims about buildable entitlement and replay-triangulation and a gatekeeper-free canon meet a world-facing trial and can go red. An epistemology with no application edge is a detached node, irrefutable and therefore useless. Future work here is the specific edge that keeps the paper accountable, not "more research". Witnesses are already on the edge: the [sibling hypothesis-graph paper](/the-hypothesis-graph-semantic-memory-methodeutics), the abductor that raises the candidates, the agent harnesses that run the trials.

Everything past that edge is allowed in the hypothesis-graph's own style, as open nodes not yet falsified. The paper may extend bold speculative edges outward, provided each is a conjecture that names its own test, never asserted as proven. A strategic overreach stated as a precise falsifiable target is a legitimate open node; the same claim dressed as established is the sin the dignity ordering names.

So the frontier is open conjectures, each with its application-trial, and it is where the material scope-guarded out of the body lives now: the wider civilizational frame, the normative and modal regimes the paper declined to treat, all rehomed here as open edges rather than smuggled into the proven core.

Three of those edges show where the view points.

### The economic edge

It is a question of search complexity rather than a war over noise. Verification is cheaper than generation one-to-one, and a kill-conditioned build makes checking a local replay rather than a re-derivation. But many-to-one is expensive, one verifier against a parallel flood.

The crisis under LLM-scale generation is search complexity: the signal-to-noise proportion was always bad, but volume under linear search thins findable signal even at constant proportion, and civilization's old sublinear structures, canons and citations and reputation, broke two ways at once, volume past their index and fluent slop passing the credence filter.

The resolution is many-to-many: a verifying fleet scales with the generating fleet, and since one-to-one verification beats generation, it can outrun the flood. The protocol's edges make the search sublinear, walk the graph, follow provenance, replay kills, so edgeless slop is never on any path, harmlessly ignored rather than laboriously refuted.

The decisive variable is the filtering rule, the kill condition applied to search, so authoring it is the goal-predicate problem: it must come from outside the searcher's own belief or it grades a fiction and builds a filter bubble. Who authors it, and whether it stays auditable and independent, decides whether agent-filtering liberates or traps.

Three kill conditions keep the edge from overreaching: the verify-beats-generate advantage is regime-bound, expensive where the kill needs a fresh world-trial; many-to-many wins only if the filters are genuinely independent, since a verifier monoculture is fooled in unison; and a sublinear search finds only what is built, blind to the unbuilt-but-true.

### Settlement and stakes

A claim that settles without anyone's trust is a claim anyone will stake on, so a fully-typed node is, in the limit, a position in a market. Settlement by replay is what a prediction market calls its oracle, here trustless because the oracle is the typed re-run, not a named authority, and a node's price becomes the population's credence in it, [Ramsey's odds](/what-cannot-be-false-cannot-be-true#belief) made literal. The two graphs bound what is bettable: a strictly-typed formal node settles cheap and final by replay, an empirical one settles only on a fresh world-trial, the rate-limited inhale, and a node with no oracle does not settle and cannot be staked, untrue and unpriced. Whether such markets sharpen credences or merely price slop is the open test.

### The forecast

Which classification scales under unbounded generation? *Untrue*, and only untrue. Generation and filtering are mirror images: generation piles up with no floor, while filtering boils down to a floor it cannot pass. (Formally, the [unfold and the fold](/compress-and-unfold), an [anamorphism and a catamorphism](https://en.wikipedia.org/wiki/Catamorphism).)

The asymmetry is decisive: filtering has a floor, generation has none. True and false live at that floor, each costing a build, a world-facing trial that stood or fired the kill, and that build is the inhale, the only place new information enters, [rate-limited by world-contact](https://en.wikipedia.org/wiki/Data_processing_inequality).

Untrue costs no build, the free default, everything filtering has not reached. So as generation outruns filtering, true and false become a thin expensive shell and untrue the surviving classification. The reason is not that they are wrong; it is that they cannot scale with generation while untrue keeps pace for free.

The posture that follows is to default the flood to untrue and spend the rate-limited inhale selectively, growing the canon from the sea where you choose to build. This reconciles with the economic edge: agent fleets scale the *replay* of already-built things, many-to-many and cheap, but cannot scale the *inhale*, a fresh world-trial for an unbuilt claim, so the built canon is verified at scale while the unbuilt sea stays untrue.

The kill condition is exact: show true/false classification scaling with unbounded generation, the inhale made cheap enough to classify the sea at generation-scale, and untrue stops dominating. The asymmetry is why it likely cannot, but that is the test.

Under all three edges sits one conjecture, an open node and not a result: verifiability is the entry condition for knowledge held in common. Between agents who do not trust each other, a claim becomes shared only as a build others can replay; what no one can replay stays private, or stays untrue. The kill is exact: exhibit shared knowledge that scales and survives bad faith with no replay beneath it, and the condition was never necessary.

## Conclusion {#conclusion}

None of this is a new logic or new metaphysics; the frame it runs on is [the companion paper's](/what-cannot-be-false-cannot-be-true), and every primitive here is borrowed. What is new is the contract: the specific executable semantics under which one agent's claim becomes another's checkable inheritance, replayable build and provenance edge and kill condition and stranger-replay and entitlement ledger and build-time canon admission as one thing.

Knowledge, for a machine, is the build a stranger can replay, linked to its grounds instead of attested by its author, and a population that agrees on the replay can hold a canon without holding a gatekeeper. That is what it is for knowledge to be verifiable: not certified, never that, but checkable by another, and checkable again by the next.

So linked, the claim stops being prose and becomes data: a node wired to what it rests on, a thing a machine can store, compose, replay, and propagate a retraction through. The structure that holds it is the [hypothesis graph](/the-hypothesis-graph-semantic-memory-methodeutics), for which this protocol is the node semantics. Where the operator began with prose and vibes, a verifiable claim ends as something a machine can build on instead of re-deriving.

## References {-}

Canonical sources this paper rests on. The frame's sources are listed in the companion paper; the author's companion essays are under *Provenance* below as lineage, not as entitlement.

- Alchourrón, C., Gärdenfors, P. & Makinson, D. (1985). "On the Logic of Theory Change." *Journal of Symbolic Logic* 50. (AGM belief revision)
- Brandom, R. (1994). *Making It Explicit*. Harvard University Press.
- Cover, T. M. & Thomas, J. A. (1991). *Elements of Information Theory*. Wiley.
- Davidson, D. (1982). "Rational Animals." *Dialectica* 36; and (1991) "Three Varieties of Knowledge."
- Doyle, J. (1979). "A Truth Maintenance System." *Artificial Intelligence* 12.
- Goertzel, B., Iklé, M., Goertzel, I. & Heljakka, A. (2008). *Probabilistic Logic Networks*. Springer. (OpenCog / PLN)
- Groth, P., Gibson, A. & Velterop, J. (2010). "The Anatomy of a Nanopublication." *Information Services & Use* 30.
- Marchal, et al. (2026). Artificial epistemic agents and the verification crisis. arXiv:2603.02960.
- Nagel, T. (1986). *The View from Nowhere*. Oxford University Press.
- Peirce, C. S. (1877). "The Fixation of Belief"; and (1878) "How to Make Our Ideas Clear." *Popular Science Monthly*.
- Sellars, W. (1956). "Empiricism and the Philosophy of Mind."
- Traxia (2026). Agent-native scientific publishing. arXiv:2606.08256.
- Wang, P. (2013). *Non-Axiomatic Logic: A Model of Intelligent Reasoning*. World Scientific. (NARS)

## Provenance {-}

This paper consolidates arguments first worked out informally on the author's blog. The operational arguments are reproduced here, so the paper stands on its own as the protocol companion; the posts are listed as lineage, not as entitlement.

- **[What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true)**: the frame this paper runs, the trichotomy and the type-split and the buildable-truth core.
- **[Truth Is Buildable](/truth-is-buildable)** (2026-06-04): the build mapping (provenance, citation, attestation, test, reproducibility), truth in the edges, and the second-model blind-spot note.
- **[Science on Trial](/science-on-trial)** (2026-04-19): every claim stands trial forever, activity versus institution, the four terms (publication, peer review, replication, truth), the citation graph with no reverse gear, trust by checkability rather than by credential.
- **[Sour Red Tapes](/sour-red-tapes)** (2026-06-01): merit attaching to the work, *nullius in verba*, delete the author and the receipts stand.
- **[Complementations](/complementations)** (2026-05-09): rejection by identity, the reflexive refusal to read.
- **[Auditing DeepSWE](/auditing-deepswe)** (2026-05-27): the motivating empirical case, and the dual of the consistency-without-test error.
- **[Modes of Reason](/modes-of-reason)** and **[Abduction](/abduction)** (2026-05-04): the three modes of inquiry the paper turns on itself.
- **[Wrong Questions](/wrong-questions)**, **[Type III Error](/type-iii-error)**, **[Wrong Again](/wrong-again)** (2026-06): the verb-scoping discipline behind "presents as knowledge."
- **[Compress and Unfold](/compress-and-unfold)** (2026-06-10): generation as the unfold, filtering as the fold, the duality behind the closing forecast.
- **[The Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics)** (2026-05-28): the data structure this protocol is the semantics for, and the application edge on which it goes red.
