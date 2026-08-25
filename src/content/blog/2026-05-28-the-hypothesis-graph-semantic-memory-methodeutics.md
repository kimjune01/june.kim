---
variant: post-paper
autonumber: true
title: "The Hypothesis Graph: A Verifiable Semantic Memory for Coding Agents"
tags: methodology, epistemology, coding
keywords: hypothesis graph, methodeutics, abductive inference, agent memory, cognitive architectures, LLM agents, provenance, auditability, falsifiability, machine epistemics, post-cutoff evaluation
---

*Receipt: [the shared-memory experiment](https://github.com/kimjune01/hypothesis-graph-handoff-experiment), including preregistrations, retained failures, and replication. Prior archived version: [doi.org/10.5281/zenodo.21939861](https://doi.org/10.5281/zenodo.21939861) (CC BY-SA 4.0).*

## Abstract {-}

Coding agents lose the warrant behind their conclusions: later agents receive prose or verdicts, then must either trust them or reconstruct the work. This paper introduces the **hypothesis graph**, a shared semantic memory whose nodes bind claims to replayable trials and whose edges record dependency, refutation, and revision. The model proposes hypotheses; the harness checks and stores them. In a bounded fail-closed experiment, the protocol preserved its declared invariants over 14,967 completely explored states and 39,288 transitions. A SQLite implementation matched an independent model across 20 frozen comparisons, passed six forced race and lease-boundary schedules and two pre-commit crash probes, and killed seven source mutants. The graph is not claimed to deepen reasoning. Its supported contribution is orthogonal: it lets verified work persist, move between agents, and fail closed when a worker submits stale or unsupported knowledge.

## Introduction {#introduction}

In coding agents, the LLM is wrapped in a harness: the verification, testing, and memory a software task needs. The field building these is moving up a level of abstraction, from the model to the harness. Roychoudhury et al. (2025) reframe the goal as *programming with trust*, arguing that deployment turns on verification, testing, and analysis built into the agent rather than on raw generation ([arXiv:2502.13767](https://arxiv.org/abs/2502.13767)). Liu et al. (2024) survey agents for software engineering and organize the field around those same missing pieces ([arXiv:2409.02977](https://arxiv.org/abs/2409.02977)); Yehudai et al. (2025) add that scoring final outputs misses the reasoning and failure causes inside a run, and call for trajectory-level assessment ([arXiv:2503.16416](https://arxiv.org/abs/2503.16416)); Wang et al. (2025) survey agentic-programming systems and list persistent, structured memory among the open challenges ([arXiv:2508.11126](https://arxiv.org/abs/2508.11126)).

A patch passes the visible tests, but that's not enough: passing certifies only the cases the tests cover. An over-narrow patch passes them and is wrong off-suite. Confirming it means reconstructing the reasoning the agent never recorded, at a cost approaching that of producing it, so the work shifts from writing to checking. Code review is the bottleneck.

When reasoning is discarded, each run rebuilds context from scratch. Even where agent memory adopts the cognitive-architecture lineage, as CoALA (Sumers et al. 2024) does in mapping it onto Soar (Laird 1987) and ACT-R, the semantic slot stores facts rather than a falsifiable structure, so the search is discarded once a patch passes. At best, a trail of blobs is saved as provenance.

We were promised a junior developer with near-infinite patience. All we got was tool calls in a loop: a cracked-up amnesiac contractor, leaving mistakes for maintainers to review.

Here we give the agent a trail of **verifiable knowledge**. The **hypothesis graph** is shared semantic memory for an inquiry. A fix arrives with what was tried, what failed, and what remains supported. Each consequential claim carries a trial a stranger can rerun. The model still reasons; the harness decides what may enter shared memory.

The contribution is a memory protocol, not a claim about deeper reasoning. The model proposes; the harness records dependencies, checks receipts, versions accepted knowledge, and refuses stale updates. This makes the graph useful even when it does not change what any one model can solve.

## The hypothesis graph {#hygraph}

### Requirements {#requirements}

A useful semantic memory for inquiry must clear five requirements at once:

- **Holds hypotheses.** Stores a hypothesis still under consideration, where prose, skill libraries, and retrieval keep only verified facts and established chunks: the hypothesis-shaped gap none of them fills.
- **Refutable by test.** Each claim carries a kill condition: the executable test that can prove it wrong.
- **Independently verifiable.** A stranger verifies a conclusion by rerunning its recorded trial, instead of re-deriving the reasoning or taking the author's word.
- **Persistent memory.** The trail persists past the context window rather than being discarded once a patch passes.
- **Fails closed.** A stale, invalid, or unsupported result cannot silently become current knowledge or unlock dependent work.

The first four are representational requirements compared below. Fail-closed behavior belongs to the update protocol and is tested separately in §(right-regime).

| Structure | Holds hypotheses | Includes tests | Independently verifiable | Persistent memory |
|-------------------------------|:-------:|:------:|:------------:|:--------:|
| **Hypothesis graph** (this work) | ✓ | ✓ | ✓ | ✓ |
| Truth-maintenance (Doyle 1979; de Kleer 1986) | ✓ | ◐ | ◐ | ◐ |
| Provenance / lineage (W3C PROV, Moreau et al. 2013) | ◐ | ◐ | ◐ | ✓ |
| Search + proof tree (Clarke et al. 2000; Solar-Lezama et al. 2006) | ✓ | ◐ | ◐ | ◐ |
| Argumentation (Dung 1995; Modgil & Prakken 2014) | ✓ | ◐ | ◐ | ◐ |
| Event-sourced log / ReAct trace (Yao et al. 2023) | ✓ | ◐ | ◐ | ✓ |

*The middle two columns are verification; the outer two are the hypothesis-shaped gap and retention. Fail-closed publication is not inferred from this table.*

An LLM is what finally fills it. Filling the graph takes a reasoner that reads a surprising failure, proposes candidate causes in open vocabulary, and turns each into an executable test, with no hand-built domain model. Classical inference engines could do this only inside a formalism encoded by hand, which is why the slot stayed a research program; the LLM populates it across arbitrary codebases, which is what makes the structure practical here.

### Graph semantics {#graph-semantics}

The graph uses two explicit edge types. An **inquiry edge** records how one failed hypothesis suggested its successor. A **dependency edge** records which accepted claims a conclusion currently relies on; these are the edges used for joins and invalidation. A **node** is a claim bound to a declared trial. While open, it records the command and kill condition. Once classified, it also records the observed outcome, verdict, and credence earned by the reasoning mode.

> **Replay invariant.** Every committed conclusion is reconstructible from its recorded trial: the exact command, observed outcome, verdict, and credence cap. The checker and recorded environment remain trusted.

The contract holds on the node's mechanical skeleton; the hypothesis prose the node also carries falls outside it, by design. The prose is the part an auditor would otherwise have to trust, and the recorded trial is what replaces trusting it, so the invariant draws its line exactly where checkability begins. The guarantee is narrow and named: the command, outcome, and verdict are checkable, while the mode label that caps a credence is a convention the writer is trusted to apply honestly.

### Operations {#operations}

Five operations maintain the structure, each defined with the one-clause argument that it preserves the invariant, the way a balanced tree's insert is defined to restore balance:

- **Create** (a smart constructor), append an open node: abduction writes a hypothesis, its kill condition, and the exact trial that will test it ("the bulb is dead", trial `swap in a fresh bulb`). *Preservation*: an open node claims no verdict yet, so it cannot enter verified memory.
- **Read / replay**: ask which hypotheses are open, or reconstruct a committed conclusion by rerunning its trial. This replaces trust in the worker's unsupported verdict with trust in the declared checker and environment. *Preservation* is vacuous because read mutates nothing.
- **Classify** (the update): a trial's outcome marks its node *killed* or *witnessed* and caps its credence at the mode that earned it, a verdict written once. *Preservation*: classify appends a verdict and never edits the recorded trial, so the node still replays to the same outcome.
- **Link** (edge-from-kill): the manner of a hypothesis's death may suggest the next hypothesis (the live replacement bulb shifts attention to the dimmer, trial `bypass the dimmer to the wall`). *Preservation*: link only appends, and each successor begins open under Create's rule.
- **Prune**: a dead branch leaves the working frontier while its record stays in place. *Preservation* is trivial, prune is a frontier-set operation that changes what is *live* and deletes nothing, so every pruned node replays exactly as before.

![A hypothesis graph, two nodes and the edge between them, on the dead-light inquiry. The bulb hypothesis is killed by a cheap trial (swap in a fresh bulb, still dark); its death names the next node, the dimmer, which a second trial witnesses (bypass it to the wall, the light comes on). Each node binds a hypothesis to a trial, an observed outcome, and a credence capped by the mode that earned it: abduction proposes and stays low, induction is test-backed and rises. Every node rebuilds from its recorded trial, so an auditor replays the structure instead of trusting it.](/assets/hypothesis-graph-anatomy.svg)

### Auditability {#auditability}

The invariant yields a local audit property:

> **Local Replay Auditability.** Any single conclusion is checkable by rerunning that node's recorded trial, without reconstructing the inquiry or trusting the worker's unsupported verdict. The checker and recorded environment remain inside the trusted boundary.

This is, for inquiry, the analogue of a certificate a consumer checks without trusting the producer, and like the Merkle audit path or proof-carrying code, its value rests on a contract; a complexity bound is beside the point.

Two grades of it matter. Where the trial is a deterministic command over pinned inputs, replay is *strong*: re-execution reproduces the recorded outcome, as in the fail-closed experiment (§(right-regime)). Where the trial runs a model or live service, replay is *artifact-level*: the recorded output is preserved and a deterministic predicate is rerun over it. Pruning leaves both untouched: a branch drops from the working frontier but remains in the record.

### Knowledge maintenance {#knowledge-maintenance}

The nodes are ordinary; what is novel is the edge semantics. A search tree finds; a proof tree justifies. The hypothesis graph is both at once, because the search path *is* the justification: every step was a trial.

It sits at the confluence of older lineages: truth-maintenance and model-based diagnosis (de Kleer 1986; Reiter 1987; de Kleer & Williams 1987), sequential experimental design (Wald 1947; Vovk & Wang 2021), abstract argumentation (Dung 1995), and counterexample-guided refinement (CEGAR, Clarke et al. 2000; CEGIS, Solar-Lezama et al. 2006). Refinement is the closest kin: a counterexample *is* a kill that names the next experiment, the hypothesis graph's defining edge. What is novel is running it over an *open* hypothesis space abduced in domain vocabulary. Replayability stands in for the sound abstraction a closed setting supplies for free, with completeness as the price the open move forfeits (§(lineage)).

The near neighbors each hold part of this and source the rest from outside themselves. A truth-maintenance system (Doyle 1979; de Kleer 1986) maintains belief status under assumptions, but the empirical trial and the kill-generated successor are external conventions. Provenance (W3C PROV, Moreau et al. 2013) records replayable activities, yet does not decide which hypothesis comes next. And the ReAct trace (Yao et al. 2023), the strongest mundane baseline, is an append-only log whose continuation policy the controller decides and the record never holds.

What the hypothesis graph adds is their composition in one append-only object: an open-domain hypothesis, its executable trial, its kill condition, and the successor that kill names. That object belongs to the verifiable family whose value is a contract rather than a complexity bound, certificate transparency (Laurie et al., RFC 9162), proof-carrying code (Necula 1997), content-addressed provenance: a data structure paired with the protocol that writes and checks it.

### Semantic memory {#semantic-memory}

This is the data structure for *testable* inquiry, and its entire power is the perturbation surface. Strip the ability to poke the system and read an outcome, and the same shape degrades into a plausibility tree, which is the confabulation failure mode it exists to prevent. Intuition is not verifiable from outside, so inquiry that has to be checked trades it for an explicit perturbation surface. The hypothesis graph is the verifiable serialization reasoning compiles to, so it can be checked by someone who does not trust you. Proof is to intuition as the hypothesis graph is to inquiry: not the thinking, the residue of the thinking that survives a stranger's replay.

That residue is what the memory typology calls the `smem`: persistent, typed, queryable, and owned by the harness rather than the model. A second agent need not inherit the whole conversation. It can enter at an open node with that node's objective, direct dependencies, versions, and receipts. Independent branches can proceed concurrently; a changed root invalidates only what depends on it. The graph in the field work is one markdown file per inquiry. The scheduler experiment makes these update rules explicit.

## Shared memory that fails closed {#right-regime}

The graph's useful claim is not that it makes a model think harder. It is that one agent's checked work can become another agent's working memory without losing the conditions under which that work was earned.

That boundary is dangerous. A worker may return late, repeat an old result, use a changed dependency, or disappear halfway through publication. In ordinary notes, the receiving agent has to notice. In the graph, the protocol notices: a claim names its version and parent versions, carries a receipt checked against frozen work, and enters memory only through an atomic publication. If any entitlement is stale or missing, nothing downstream unlocks. Refusing progress is safe.

### The experiment {#memory-experiment}

We tested this mechanism on a small diamond graph, `R→A,B; A,B→J`, with two workers and a separate SQLite implementation. The reference model was declarative rather than copied from the scheduler. The trusted boundary included the checker, root authority, scheduler process, SQLite, clock, operating system, and storage; workers were allowed to crash, retry, delay, duplicate, corrupt, and reorder their calls.

The experiment was deliberately bounded. This is a mechanism demonstration, not a significance study.

| Evidence layer | Frozen result |
|---|---:|
| Complete protocol exploration | 14,967 states; 39,288 transitions; zero violations |
| Independent model–SQLite conformance | 20 comparisons across ten dispositions; zero mismatches |
| Forced schedules | six race and lease-boundary schedules passed |
| Process interruption | two pre-commit deaths reopened to the complete prior state |
| Mutation sensitivity | seven source mutants executed and were killed |

The exact schedules covered same-node double claim, both orders of publication versus root update, and publication immediately before, exactly at, and immediately after lease expiry. The mutations removed the checks we say matter: receipt validation, version entitlement, expiry, claim exclusivity, exact invalidation, and atomic publication. An unchanged replication produced the same result.

The first confirmatory run did not pass. One malformed mutant failed during test collection, and the harness initially mistook any nonzero exit for a killed mutant. We retained the failure, changed the rule so only an executed assertion failure counts, froze the follow-up, and reran it. That correction is part of the receipt, not an inconvenience hidden behind the final table.

### Shared entry points {#shared-entry}

The graph also makes handoff smaller and concurrency cleaner. On one frozen DAG, three workers received different open nodes within 8 ms and shared 3.4 seconds of actual overlap. Each entered through a mechanically generated packet containing only its objective, direct prerequisites, versions, receipts, and output contract; each packet was less than half the size of the full chronological notes.

This did **not** produce a meaningful wall-time speedup, and we do not claim one. The demonstrated benefit is structural: independent work can start without transferring the whole inquiry, while joins remain locked until their declared dependencies verify. When a root changed during work, the scheduler invalidated exactly its descendants and preserved the independent branch.

### What the result supports {#memory-result}

The result supports one narrow claim:

> A versioned, receipt-checked hypothesis graph can serve as shared semantic memory that fails closed: stale or unsupported worker output is rejected rather than silently becoming current knowledge.

“Can” matters. Complete exploration covered one frozen protocol model, not every implementation. The SQLite evidence covered a transition-complete basis and targeted adversarial schedules, not all possible storage failures. The checker itself remains trusted. Nothing here establishes Byzantine tolerance, semantic correctness of a bad specification, or better underlying model reasoning.

The value is still substantial. *Verifiable Knowledge* gives a claim its receipt. The hypothesis graph adds dependency, version, and invalidation structure, so that receipt can travel across agents without becoming an unsupported assertion. One paper defines what may count as knowledge; this one defines how such knowledge is shared and revised.

## Actionable epistemology {#epistemics}

Knowing is an act that changes which claims one is entitled to use. This is the subject of *Verifiable Knowledge*; the property that matters here is that a verdict carries a receipt another agent can check. In the Hypothesis Graph, knowledge has the following properties:

- **Three states.** Witnessed has passed its declared predicate; killed has failed it; open is *untrue*, a conjecture awaiting its test. These are the states of the entitlement ledger developed in *Verifiable Knowledge*, scoped here to one node and its kill edge.
- **Credence.** A node carries a credence capped by the mode that earned it, low for abduction, higher once tested (Ramsey 1926), the step a bare LLM skips when it emits uniform confidence with no propagation along the chain.
- **Survived belief.** A node counts as knowledge only after withstanding a trial, a verificationist criterion (Ayer 1936), indexed to the stakes of acting on it. Before trial, a claim is a hypothesis.
- **Dependency connections.** Each conclusion records the claims on which its current entitlement depends.

With each round of inquiry the dependency boundary sharpens. With each successful trial, a claim earns only the confidence its declared predicate supports.

![A claim and its trial as one record. Left, the claim: a load resting on a span, *this bridge holds the load*. Right, the trial: a toothpick-and-gumdrop model bridge bearing a steel weight across two supports. Photo: Oregon Department of Transportation, CC BY 2.0.](/assets/bridge-trial-light.svg)

This is one more projection of the protocol *Verifiable Knowledge* sets out, from where the agent stands, and its payoff is transfer. Paired with its trial, a node carries its warrant across intact; handed on the author's word, only the verdict crosses and the warrant is re-derivable from scratch.

A coding agent can already run a test. What it lacked was a protocol for carrying the result beyond one context without reducing its warrant to “trust me.” With the protocol, another agent can reuse the result, replay it, or see that it has gone stale.

## Methodeutics: a discipline of inquiry {#grounding}

A store of causal knowledge needs reasoning to be encoded into it. How can reasoning become mechanical enough for encoding? The insight, the leap to a candidate cause, stays with the model, but the harness needs a method to stage reasoning. Reasoning then becomes mechanical the way a proof is, through the discipline of checking ideas. In a precise and limited sense the harness stages and checks reasoning mechanically, everything but the leap, which it can only trigger. This discipline, Peirce called **inquiry**.

His *Illustrations of the Logic of Science* (1878) and *Pragmatism as the Logic of Abduction* (1903) type the operations of inquiry into three irreducible modes.

- **Abduction** generates explanatory hypotheses for surprising observations: *what would, if true, make this no longer surprising?*
- **Deduction** derives testable predictions from hypotheses: *if this hypothesis holds, what follows?*
- **Induction** tests predictions against evidence: *does the evidence accord with the prediction?*

![The three modes as one cycle: Observation → Theory (abduction), Theory → Experiment (deduction), Experiment → Observation (induction).](/assets/modes-of-reason-triangle-light.svg)

No single mode carries a belief to its grade. Abduction proposes content but does not test it; induction tests but introduces no new explanatory content; deduction traces consequences but invents nothing. The credence a node ends up with is what traversing all three earns it, and that is what it means to call the modes typed: each is fixed by what it can't do.

This is where readers balk: why is *abduction* responsible for theory? Isn't that deduction's job? No. Deduction neither generates the theory nor proves it; it unfolds the hypothesis into the predictions it must answer for. The theory was abduced, the predictions deduced, and induction does the testing.

Keep them separate and each does its one job; collapse them and you get familiar failure modes:

- **Confirmation bias**: induction without abductive alternatives
- **Confabulation**: abduction without inductive grounding
- **Free-association**: no typed mode at all

That collapse is exactly what modern LLM agents do by default, since a single forward pass proposes, predicts, evaluates, and rationalizes in undifferentiated prose. Methodeutics, Peirce's term for the methodology of inquiry, is how to conduct the typed-mode loop well. Encoded as skills, it constructs and maintains the `smem`.

*Modes of reason and the irreducible three.* Around the act of testing, philosophy of science built an apparatus of real rigor: Bacon's induction (1620), Popper's falsifiability (1934), Meehl's "soft science" critique (1967), Pearl's causal calculus (2009). Justification got its method, every step of it. But it begins one step too late, taking the hypothesis as given and filing its origin under inspiration. The discipline built an epistemology of justification and little of discovery. Peirce named the missing operation, abduction; the discipline still filed the origin of hypotheses under inspiration. The harness gives it a first-class typed slot and triggers it, though the leap itself stays the model's.

## Methodeutics, applied {#application}

Putting the theory to work means generating hypotheses as typed nodes the harness can test, instead of trusting whatever a model guesses.

*The surprise has a primitive, and it is a diff.* What the harness manufactures is not the hypothesis but the discrepancy that provokes one: a before snapshot, an after snapshot, and the perturbation that flipped, read as figure against the ground that held (Rubin's Gestalt terms). Separation logic calls the frame-inference half of this *bi-abduction* and scaled it to real codebases in Facebook Infer (Calcagno et al. 2009; O'Hearn 2019), borrowing Peirce's word for an operation that is not his abduction: it localizes where belief and code diverge, the surprise, and leaves the leap to what would explain it unmade. `inquire` works at the simplest level: one before/after diff, the frame inferred from the symptom. The extensions to branches and compositional cases are in the [lineage appendix](#lineage).

The "XOR" used throughout is shorthand for that separation: the figure (what the fix must change) held apart from the ground (the frame that stays invariant). Where bi-abduction infers the frame to make a proof go through, the harness fires the same split as a check, computing the symmetric difference against a known-good oracle and keeping only the cases it flags. The XOR is the surprise, not the leap: it marks what a hypothesis must explain, and the explaining stays the model's.

![Bi-abduction on a dead fixture. With dimmer, fixture, and bulb all intact, the static scene names no suspect; the perturbation bypasses the dimmer to the wall, and the XOR isolates the figure (the dimmer) from the ground (fixture and bulb).](/assets/bi-abduction-dimmer.svg)

*Directed graphs as reasoning representation.* Pearl 1988 (*Probabilistic Reasoning in Intelligent Systems*; Bayesian networks as DAGs of dependencies); Pearl 2000/2009 (*Causality*; structural causal models, d-separation, do-calculus). Pearl's lineage was built for causal-structure inference; our data structure (typed nodes, directed edges) puts it to hypothesis representation. The difference from a Bayesian network is one of kind, and runs deeper than dropped probabilities. A Bayes net conditions over a fixed variable set and propagates probability along edges of dependence; the hypothesis graph abduces its nodes as the inquiry runs, its edges genealogical, a dead hypothesis naming its successor rather than a conditional dependence. A Bayes net is justification over a space it is handed; the hypothesis graph generates the space.

![The hypothesis graph for the dead fixture. Abduction fans the observation into four typed candidate nodes; mechanical kill predicates fire on three (the socket, fixture, and bulb each cleared by a cheap test), the dimmer node is witnessed by the bypass and closes the last open hypothesis, and deduction derives the fix. Typed nodes, directed edges, all three modes in one inquiry.](/assets/hypothesis-graph-fixture.svg)

Isn't generating that space just debugging? It is, and debugging has been automated for decades: spectrum-based fault localization, statistical and delta debugging, model-based diagnosis, and search-based program repair are mature fields (Jones et al. 2002; Liblit et al. 2005; Zeller & Hildebrandt 2002; Reiter 1987; Le Goues et al. 2012; Monperrus 2018). Debugging tools already automate the loop; what is new is that the hypothesis graph persists it. Every engineer, and every repair tool, runs some version of abduce a cause, kill it on evidence, witness the survivor, derive the fix. But the engineer runs it in their head, and the tools, whatever logs they keep, do not persist the search as a typed, replayable hypothesis graph.

We implement this loop as a tool. *abductor* ([github.com/kimjune01/abductor](https://github.com/kimjune01/abductor)) externalizes the surprise, the diff generation, outside the context window, so a model has to represent the rule instead of tabulating the case in front of it: it enumerates a space wider than the model's hypothesis, calibrates each case against a known-good baseline, and exposes one pass/fail gate, with the answer key held outside the model's view. A failing case is a counterexample that forces the next fix, the model's own leap, and the search records itself as the hypothesis graph, fixes as nodes and counterexamples as edges.

## The methodeutic harness {#method}

How do epistemology and debugging become an agentic harness? The loop that writes the graph needs four things:

- **Iteration.** One pass can't be trusted, so the loop re-enters on failure.
- **Deterministic oracle.** A model can't be trusted to catch its own bias, so the check comes from outside the weights.
- **Three modes of reasoning.** Abduction, deduction, and induction stay typed and separate, each capped at its own confidence.
- **Semantic memory.** The reasoning is recorded into the hypothesis graph and survives the context window.

Concretely, this is a skill with a tool call in a loop: the outer deterministic driver invokes an agent via the `inquire` skill, who accesses the deterministic `abductor` tool. It mechanizes the surprise, the diff the model would otherwise have to compute by hand.

![The `inquire` skill: Peirce's three modes as a procedure that writes the hypothesis graph. Induction fires a deterministic kill or witness with no model arbitrating. `implement` and `attest`, which read the survivors and verify the patch, follow below.](/assets/inquire-skill.svg)

### The inquiry frame {#inquiry-frame}

We recast each issue as an inquiry on an engineered system: a failure trace, a codebase, a root cause to find, and an intervention that must not regress the rest of the system. Code is the right substrate for the hypothesis graph because it combines three properties that other inquiry domains rarely bring together:

- **Reproducible**: same input yields same output, modulo controlled nondeterminism
- **Deterministic**: causal lines from input to behavior are mechanical
- **Perturbable**: single-line and single-function diffs are cheap to apply and fully observable

Because those three hold together, kill conditions over code are exact executions.

One trial settles the predicate in this regime. In code the per-case response is mechanically observable, so a single passing test on a captured diff is a complete verdict that the diff satisfies the executable predicate for that case. Behaviors the predicate does not cover remain out of scope. Where verdicts are aggregated, the right summary is counts and denominators rather than confidence intervals: per-case verdicts are exact, and aggregating them is bookkeeping.

The three Peircean modes are how `inquire` builds the graph, each node typed by the mode that established it and capped at that mode's confidence:

| Mode | What `inquire` does | Confidence |
|------------|---------------------------------------------------|---------|
| **Abduction** | Proposes candidate root causes from the observed failure; writes hypothesis nodes with falsifiable predicates and kill conditions (read-only) | low |
| **Deduction** | Traces each hypothesis's consequences through the code to localize the suspect set | high |
| **Induction** | Tests survivors with cheap read-only experiments (prints, intermediate data) | moderate |

`implement` then writes the surviving hypothesis, with an adversarial challenger critiquing the diff against the spec. `attest` runs the test suite, takes the grader's pass/fail verdict, and emits a re-entry route (`inquire`, `implement`, or `none`) from a fixed verdict→route table. The driver parses the verdict and the route; both are mechanical, and no model decides termination.

### Hypothesis graph output {#recon-output}

`inquire` emits the hypothesis graph: the structured-analysis document that precedes the patch. Kill conditions are mechanical predicates over the evidence trajectory, so a node dies when its predicate fires and not before. The graph persists across iterations; re-entry adds nodes rather than overwriting. The frontier closes only when every open hypothesis is killed (a test refutes it) or witnessed (a test confirms it).

A committed node is a conclusion, and an inquiry that reaches one rarely runs straight. Following the `inquire` skill on a real bug, a single hypothesis flips across all three modes and a kill before it settles:

> abduction → deduction → kill → abduction → deduction → induction → deduction → induction ⇒ induction

*An in-flight inquiry trace, illustrative: Sonnet 4.6 following the `inquire` skill on the python-dotenv `find_dotenv` v1.0.1 regression (a real, reproducible bug, every command run). The active hypothesis cycles through all three modes and a kill before the inquiry settles; a committed graph records only the terminal node (induction) and discards this sequence. Full trace: [recon-inflight-dotenv.md](https://june.kim/assets/recon-inflight-dotenv.md).*

### Deterministic gating {#gating}

The control loop is standard: the driver routes on `attest`'s verdict under a bounded attempt budget, and a failure re-enters `inquire` with the updated graph rather than retrying the patch. The hypothesis graph doubles as the loop's checkpoint, so dead branches are not silently proposed again.

### Artifact availability {#artifact}

All code and data are openly available. The shared-memory experiment of §(right-regime) lives at [github.com/kimjune01/hypothesis-graph-handoff-experiment](https://github.com/kimjune01/hypothesis-graph-handoff-experiment) under AGPL-3.0-or-later. It retains the preregistrations, failed first confirmation, independent model, source mutants, crash probes, raw counts, replication, and result hypothesis graph.

## Discussion {#discussion}

### Memory is an entitlement, not a fact dump

Most agent memory asks *what text should be retrieved?* The hypothesis graph asks a prior question: *what is this agent entitled to rely on?* A claim is current only at a declared version, under declared parent versions, with a receipt for the work actually claimed. Retrieval can then be ordinary and cheap because validity is not left to the reader's intuition.

This is the connection to *Verifiable Knowledge*. A receipt makes one claim checkable. The graph makes many such claims maintainable. Dependency edges say what a revision withdraws; version vectors distinguish current knowledge from history; atomic publication prevents half-written conclusions from entering shared state.

The guarantee is modest but practical. Bad input does not become good because it is structured. A trusted checker can still encode the wrong predicate. What the protocol prevents is narrower: stale or unsupported output entering as verified shared knowledge.

### Concurrency follows from addressability

Concurrency is not a separate trick added to the graph. It follows from explicit open nodes and joins. Workers can claim independent nodes without receiving the whole history. A join opens only when its parents verify. Less context crosses each boundary because the graph supplies a clean entry point: objective, direct prerequisites, receipts, and output contract.

The demonstration showed real overlap but no material speedup. Addressability and safe concurrency are structural properties; speed depends on branch cost, startup, contention, and the critical path. This paper claims the former and leaves the latter open.

### Accountability survives the author

A prose handoff asks the next agent to trust the previous one. A graph handoff asks it to check a receipt or observe that the claim is no longer current. This changes the unit of trust from an author to a piece of work.

Local replay is the smallest form of that accountability. Selective invalidation is the compositional form: when a premise changes, dependent conclusions lose entitlement while independent work survives. The graph is useful not because every node is true forever, but because it records when a node may be used and what would make it stop being usable.

## Related work {#related-work}

### Agent memory and handoff {#rw-swebench}

Memory surveys distinguish episodic traces, semantic facts, and procedural skills, but persistent agent systems often store prose or retrieved chunks without an executable validity rule. CoALA (Sumers et al. 2024) supplies the cognitive-architecture vocabulary; AriGraph (Anokhin et al. 2024) supplies a graph-shaped memory precedent; provenance systems supply lineage; truth-maintenance systems supply dependency-directed revision. The hypothesis graph combines these around a narrower node contract: a claim, its dependency versions, and a replayable trial.

The practical baseline is not no memory. It is a strong structured handoff: objective, state, evidence, decisions, and next steps. Such a handoff can be excellent. What it lacks natively is mechanical admission, versioned entitlement, atomic publication, and transitive invalidation. The shared-memory experiment isolates those protocol properties rather than asking a language-model judge which memo reads better.

### Agent scaffolds and SE-agent harnesses {#rw-scaffolds}

Surveys and position papers place verification, analysis, and persistent structured memory at the harness layer (Roychoudhury et al. 2025; Liu et al. 2024; Wang et al. 2025). OpenHands, SWE-agent, and AutoCodeRover are ReAct-pattern coding loops; Voyager is a close loop-shape precedent, with tested skills where this work stores falsifiable claims.

Two adjacent systems split the contribution differently. Theorem-of-Thought types abductive, deductive, and inductive reasoning within a query but does not maintain a persistent memory across inquiries. Cognitive Memory Manager extracts a typed DAG from completed trajectories and promotes patterns to skills. This work writes the graph during inquiry and uses failed trials and changed versions to route what may happen next.

The distinction is not that graph-shaped memory is new by itself. The contribution is the semantic contract placed on its nodes and updates: replayable warrant, explicit dependency, versioned reuse, and fail-closed publication.

### Typed reasoning and graph-structured memory {#typed-memory}

**IDEA** (He et al. 2025, ACL Findings, [arXiv:2408.10455](https://arxiv.org/abs/2408.10455)) explicitly cites Peirce and uses the three modes in an interactive rule-learning benchmark. **ADI** (Gilda & Gilda 2026, [arXiv:2604.15727](https://arxiv.org/abs/2604.15727)) gives an explicit Peircean tripartite protocol with epistemic layers over a symbolic knowledge graph; near-simultaneous with this draft and the most conceptually adjacent prior work. Both target reasoning domains outside SE.

The hypothesis graph sits at the intersection of three lineages: cognitive-architecture memory (Soar / ACT-R / EPIC), LLM-agent memory systems (CoALA / AriGraph / Mem0 / Zep), and typed-belief representations (CausaLab / BeliefMem / Theorem-of-Thought / CMM). The hypothesis graph adopts the Soar memory typology directly as its slot vocabulary, adding only the specific content of the `smem` slot: Peirce-typed, kill-conditioned, designed for LLM prose read/write. Adjacent work: **Kirk, Wray & Laird 2023** ([AAAI](https://ojs.aaai.org/index.php/AAAI-SS/article/download/27690/27463/31741)), an LLM-port of the Soar lineage; **CoALA** (Sumers et al. 2023/24, [arXiv:2309.02427](https://arxiv.org/abs/2309.02427)); **AriGraph** (Anokhin et al. 2024/25, [arXiv:2407.04363](https://arxiv.org/abs/2407.04363)), the closest precedent for graph-structured LLM-agent memory; **CausaLab** (Yang et al. 2026, [arXiv:2605.26029](https://arxiv.org/abs/2605.26029)); **BeliefMem** (Liao et al. 2026, [arXiv:2605.05583](https://arxiv.org/abs/2605.05583)), strong adjacent on uncertain alternatives with mechanical update.

**CMM** (Khalid & Arora 2026, [OpenReview](https://openreview.net/pdf?id=yCsHQnvvWY); a day before this draft) is the closest comparison: the same persistent typed DAG of reasoning artifacts, but observe-and-consume (it types a trajectory post hoc and graduates skills) where ours is perturb-and-falsify (kills fire live, the graph routes the run). The directions are opposite and complementary, the ~385 committed graphs in `sweep/repo-hypotheses/` exactly the corpus its graduation pipeline could consolidate.

Four 2026 systems each carry one component this work combines; what is new here is the *join*; each piece already exists in one of them. **FVDebug** ([arXiv:2510.15906](https://arxiv.org/abs/2510.15906)) builds an actual hypothesis graph for debugging, with a frontier and accumulated evidence, but selects the next node by asking the model, the arbiter this work removes. **From Hypotheses to Factors** ([arXiv:2604.26747](https://arxiv.org/abs/2604.26747)) runs the same perturb-and-falsify loop, falsifiable hypotheses behind a deterministic engine over an append-only trace, locked to quantitative finance where this work claims the general semantic-memory substrate. **Portable Agent Memory** ([arXiv:2605.11032](https://arxiv.org/abs/2605.11032)) is the nearest provenance memory, a Merkle-DAG that cites the Soar lineage and makes every node reconstructible by content-addressing, but it certifies *integrity* (the recorded bytes are untampered) where the replay invariant here certifies *warrant* (the node still survives its trial). And the provenance survey **From Agent Traces to Trust** ([arXiv:2606.04990](https://arxiv.org/abs/2606.04990)) enumerates exactly the relations this work mechanizes, Support, Contradict, Invalidate, and names "how provenance quality should be evaluated" as an open problem; the hypothesis graph is one answer, with replay as the quality bar and the kill condition as an executable edge rather than a descriptive label.

The experiment adds an update rule to this comparison. A claim is not merely stored or assigned confidence: it is admitted with a receipt and dependency versions, then becomes historical when those dependencies change. This is the difference between graph-shaped storage and graph-maintained knowledge.

A second cluster treats truth and uncertainty as first-class rather than a downstream score: **NARS**, **OpenCog's AtomSpace/PLN**, **Nanopublications** (Groth et al. 2010), and, closest in time, **Traxia** ([arXiv:2606.08256](https://arxiv.org/abs/2606.08256)), converging on these primitives two days after *Truth Is Buildable* (2026-06-04). Where each stops short of a replayable, kill-conditioned entitlement ledger is adjudicated in *Verifiable Knowledge*, the paper that owns the epistemology. What is specific *here* is the data structure: none makes that meaning the **semantic contract of a memory node**, truth operationalized by replayable edge structure rather than a stored label or textual provenance record.

> *Production LLM memory systems with graph variants (Zep/Graphiti, Mem0), staged-hypothesis selection in science agents, deterministic gating in adjacent settings, and reflective memory systems (Reflexion, DebugMate) are surveyed in the appendix; they are adjacent on particular axes but do not change the comparison spine.*

## Limitations {#limitations}

*The result is bounded.* Complete exploration covers one small declarative graph to depth 6. The SQLite implementation is checked by a frozen conformance basis, forced schedules, crash points, and mutants, not by exhaustive exploration of SQLite itself. “Can fail closed” is supported; “hypothesis graphs are generally safe” is not.

*The checker is trusted.* A receipt establishes only the predicate the checker implements. A wrong specification can be checked perfectly and remain wrong. Root authority, scheduler code, SQLite, the operating system, clock, hash behavior, and storage are also inside the trusted boundary.

*The memory is small and per-inquiry.* Retrieval quality, compaction, cross-repository accumulation, permissioning, and long-term storage repair remain untested.

*Concurrency is demonstrated, not accelerated.* Three workers overlapped on independent nodes, but wall time improved by only 1.83%. The graph creates safe entry points and dependency-aware joins; it does not guarantee useful speedup.

*The comparison to prose is incomplete.* Bounded graph packets were smaller than full chronological notes, but a careful human can curate equally good packets. The demonstrated advantage is mechanical generation and validity tracking.

*How to refute this.* The fail-closed claim dies if an explored state violates an invariant, a model–SQLite projection diverges, a pre-commit death leaves partial state, or a declared mutant survives. The checks and the retained failed confirmation are public.

## Future work {#future-work}

The next work should test scale only where scale changes the mechanism.

- **Larger shared graphs.** Increase depth, shared descendants, and simultaneous root changes until projection or invalidation cost becomes material.
- **Long-lived memory.** Test retrieval, compaction, and selective forgetting across many inquiries without weakening receipt or dependency semantics.
- **Strong handoff baselines.** Compare graph packets with equally informative curated packets on resumption, duplicated work, and stale-claim inheritance.
- **Adversarial authority.** Move root admission and parts of checking outside the trusted boundary, then state the stronger fault model precisely.
- **Interchange format.** Specify the abstract data type independently of this scheduler so different agents can publish and consume the same receipt-bearing nodes.
- **Ecological concurrency.** Use tasks whose expensive intermediate results dominate startup and coordination overhead; measure speed only after safety continues to hold.

## Conclusion {#conclusion}

A coding agent does not need another place to put prose. It needs memory that distinguishes a reusable result from an unsupported assertion.

The hypothesis graph supplies that distinction. A node binds a claim to a receipt and dependency versions. The graph admits it atomically, exposes independent entry points, and withdraws dependent knowledge when a premise changes. In the bounded experiment, this protocol survived complete model exploration, independent implementation comparisons, forced races, process deaths, and targeted source mutations.

The claim is deliberately simple: a versioned, receipt-checked hypothesis graph can serve as shared semantic memory that fails closed. It does not make a model reason better. It makes checked work easier to carry forward without forgetting why it was trusted.

## Availability and reproducibility {#availability}

- **Shared-memory experiment.** [github.com/kimjune01/hypothesis-graph-handoff-experiment](https://github.com/kimjune01/hypothesis-graph-handoff-experiment): preregistrations, scheduler, independent model, bounded explorer, conformance basis, races, crash probes, mutations, retained failure, replication, and result hypothesis graph. AGPL-3.0-or-later.
- **Field corpus.** Approximately 385 per-inquiry graphs at [`kimjune01/sweep/repo-hypotheses/`](https://github.com/kimjune01/sweep).
- **Companion papers.** [*Verifiable Knowledge*](/verifiable-knowledge) defines the receipt-bearing knowledge unit; [*What Cannot Be False Cannot Be True*](/what-cannot-be-false-cannot-be-true) supplies its falsifiability boundary.
- **Paper.** This markdown source is canonical. The DOI above identifies the prior archived version; this revision should receive a new versioned deposit after its PDF is rebuilt.

**Reproducibility invitation.** Re-run the frozen explorer, conformance traces, crash probes, and source mutants. A counterexample retracts every claim that depends on the failed invariant; the result graph names those dependencies explicitly.

## LLM collaboration disclosure {-}

LLMs produced the field graphs and helped design, implement, and review the shared-memory experiment. Mechanical checks, SQLite state, and the independent model held every experimental verdict. The prose was drafted and revised with Anthropic's Claude and OpenAI's Codex from human-authored outlines and session notes; the claims, methodology, and publication decisions are the author's.

## Acknowledgments {-}

We thank John Laird for comments that improved the paper's framing and abstract.

## References {-}

Works cited above, consolidated. Entries for which the text or the *Extended intellectual lineage* gives only a short name or arXiv identifier are listed at that detail rather than filled out, so nothing here is reconstructed beyond what the paper states. The author's companion essays are listed separately under *Availability and reproducibility* as lineage, not as entitlement.

- Abdaljalil et al. (2025). *Theorem-of-Thought*: typed abductive/deductive/inductive reasoning agents. arXiv:2506.07106.
- Agarwal (2026). *Refute-or-Promote*: adversarial defect discovery. arXiv:2604.19049.
- Aleithan et al. (2024). *SWE-Bench+*: a manual audit of SWE-bench (solution leakage and weak tests).
- Anokhin et al. (2024/25). *AriGraph*: knowledge-graph memory for LLM agents. arXiv:2407.04363.
- Anthropic / Sumers, T., Yao, S., Narasimhan, K. & Griffiths, T. (2023/24). "Cognitive Architectures for Language Agents" (CoALA). arXiv:2309.02427.
- Bacon, F. (1620). *Novum Organum*.
- Bylander et al. (1991). On the computational complexity of abduction. *Artificial Intelligence* 49.
- Calcagno, C., Distefano, D., O'Hearn, P. & Yang, H. (2009). Compositional shape analysis by means of bi-abduction. *POPL*. (Facebook Infer.)
- Chroma (2025). Context rot: degradation of in-context reasoning with input length.
- Clarke, E., Grumberg, O., Jha, S., Lu, Y. & Veith, H. (2000). Counterexample-guided abstraction refinement (CEGAR). *CAV*.
- *Confucius Code Agent* (2025). arXiv:2512.10398.
- Cousot, P. & Cousot, R. (1977). Abstract interpretation. *POPL*.
- de Kleer, J. (1986). "An Assumption-based Truth Maintenance System." *Artificial Intelligence* 28.
- de Kleer, J. & Williams, B. (1987). Diagnosing multiple faults (the General Diagnostic Engine). *Artificial Intelligence* 32.
- Deng et al. (2025). *SWE-bench Pro*. arXiv:2509.16941.
- Dewey, J. (1929). *The Quest for Certainty*. Minton, Balch & Co.
- Doyle, J. (1979). "A Truth Maintenance System." *Artificial Intelligence* 12.
- Dung, P. M. (1995). "On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games." *Artificial Intelligence* 77. (Abstract argumentation frameworks.)
- Feynman, R. (1974). "Cargo Cult Science." Caltech commencement address.
- *From Agent Traces to Trust* (2026): a provenance survey for agent reasoning. arXiv:2606.04990.
- *From Hypotheses to Factors* (2026): perturb-and-falsify over an append-only trace in quantitative finance. arXiv:2604.26747.
- *FVDebug* (2025): a hypothesis graph for debugging with model-selected nodes. arXiv:2510.15906.
- Gilda, S. & Gilda (2026). *ADI*: a Peircean tripartite protocol over a symbolic knowledge graph. arXiv:2604.15727.
- Goertzel, B., Iklé, M., Goertzel, I. & Heljakka, A. (2008). *Probabilistic Logic Networks*. Springer. (OpenCog / PLN.)
- *GradleFixer* (2025). arXiv:2510.08640.
- Groth, P., Gibson, A. & Velterop, J. (2010). "The Anatomy of a Nanopublication." *Information Services & Use* 30.
- He et al. (2025). *IDEA*: interactive rule learning with the three Peircean modes. ACL Findings. arXiv:2408.10455.
- Jain et al. (2024). *LiveCodeBench*: temporal-holdout (post-cutoff) evaluation.
- Jones, J., Harrold, M. J. & Stasko, J. (2002). Spectrum-based fault localization. *ICSE*.
- Kamoi et al. (2024). "When Can LLMs Actually Correct Their Own Mistakes?" A critical survey of self-correction: self-generated feedback fails, reliable external feedback works. *TACL*. arXiv:2406.01297.
- Khalid & Arora (2026). *Cognitive Memory Manager* (CMM): a typed-node DAG mined from agent execution. OpenReview yCsHQnvvWY.
- Kimball, A. W. (1957); Tukey, J. W. The Type III error: a precise answer to the wrong question.
- Kirk, J., Wray, R. & Laird, J. (2023). An LLM port of the Soar lineage. *AAAI Spring Symposium*.
- Laird, J., Newell, A. & Rosenbloom, P. (1987). *Soar*: an architecture for general intelligence. *Artificial Intelligence* 33.
- Laurie, B., et al. *Certificate Transparency*. RFC 9162.
- Le Goues, C., Nguyen, T., Forrest, S. & Weimer, W. (2012). GenProg: search-based program repair. *IEEE TSE*.
- Liang et al. (2023/24). *Multi-Agent Debate*. arXiv:2305.19118.
- Liblit, B., Naik, M., Zheng, A. X., Aiken, A. & Jordan, M. I. (2005). Statistical debugging. *PLDI*.
- Liao et al. (2026). *BeliefMem*: candidate sets with Noisy-OR probabilistic update. arXiv:2605.05583.
- Liu et al. (2024). A survey of LLM-based agents for software engineering. arXiv:2409.02977.
- Meehl, P. (1967). "Theory-Testing in Psychology and Physics: A Methodological Paradox." *Philosophy of Science* 34.
- Modgil, S. & Prakken, H. (2014). The ASPIC+ framework for structured argumentation. *Argument & Computation* 5.
- Monperrus, M. (2018). "Automatic Software Repair: A Bibliography." *ACM Computing Surveys* 51.
- Moreau, L., et al. (2013). *PROV-DM*: the W3C provenance data model.
- Necula, G. (1997). "Proof-Carrying Code." *POPL*.
- O'Hearn, P. (2019). "Incorrectness Logic." *POPL* (separation logic).
- *OpenAI* (2026). SWE-bench Verified audit (February 2026): flawed tests and exact-gold-patch reproduction; recommends Pro.
- *ORACLE-SWE* (2026): ablating the oracle and specification signals that leak through a task. arXiv:2604.07789.
- Pearl, J. (1988). *Probabilistic Reasoning in Intelligent Systems*. Morgan Kaufmann. (Bayesian networks as DAGs.)
- Pearl, J. (2000/2009). *Causality: Models, Reasoning, and Inference*. Cambridge University Press.
- Peirce, C. S. (1878). *Illustrations of the Logic of Science*. *Popular Science Monthly*. (The three-mode taxonomy of inquiry.)
- Peirce, C. S. (1903). *Pragmatism as the Logic of Abduction* (Harvard Lectures on Pragmatism).
- *POPPER* (2025): agentic sequential hypothesis testing under e-value control. arXiv:2502.09858.
- Popper, K. (1934/1959). *The Logic of Scientific Discovery*.
- *Portable Agent Memory* (2026): a Merkle-DAG provenance memory citing the Soar lineage. arXiv:2605.11032.
- Ramsey, F. P. (1926). "Truth and Probability." In *The Foundations of Mathematics* (1931).
- Reiter, R. (1987). "A Theory of Diagnosis from First Principles." *Artificial Intelligence* 32.
- Roychoudhury, A., et al. (2025). Programming with trust: verification, testing, and analysis built into the agent. arXiv:2502.13767.
- Solar-Lezama, A., et al. (2006). Counterexample-guided inductive synthesis (CEGIS). *ASPLOS*.
- Stroebl, B., et al. (2025). *HAL*: a cost-transparent agent leaderboard.
- *SLUMP* (2026): an underspecified-by-design coding benchmark. arXiv:2603.17104.
- *SWE-Effi* (2025): effectiveness from scaffold-model synergy. arXiv:2509.09853.
- *SWE-rebench* (2025): post-cutoff filtering as a contamination strategy.
- *SWT-Bench* (2024): grading generated tests by fail-on-original then pass-after-golden-patch. arXiv:2406.12952.
- *Traxia* (2026): agent-native scientific publishing. arXiv:2606.08256.
- Vovk, V. & Wang, R. (2021). "E-values: Calibration, combination, and applications." *Annals of Statistics* 49.
- Wald, A. (1947). *Sequential Analysis*. Wiley.
- Wang, P. (2013). *Non-Axiomatic Logic: A Model of Intelligent Reasoning*. World Scientific. (NARS.)
- Wang et al. (2023). *Voyager*: an open-ended embodied agent with a skill library. arXiv:2305.16291.
- Wang et al. (2024). *OpenHands* (formerly OpenDevin): an open platform for AI software developers.
- Wang et al. (2025). A survey of agentic-programming systems (persistent structured memory as an open challenge). arXiv:2508.11126.
- Wang, X., Pradel, M. & Liu (2026). Plausible patches that pass tests yet diverge from developer intent. *ICSE*.
- Yang et al. (2024). *SWE-agent*: agent-computer interfaces for software engineering.
- Yang et al. (2026). *CausaLab*: an evolving structural causal model in a DSL. arXiv:2605.26029.
- Yao, S., et al. (2023). *ReAct*: synergizing reasoning and acting in language models.
- Yehudai et al. (2025). Trajectory-level assessment of agents. arXiv:2503.16416.
- Zeller, A. & Hildebrandt, R. (2002). "Simplifying and Isolating Failure-Inducing Input" (delta debugging). *IEEE TSE* 28.
- Zhang et al. (2024/25). *AutoCodeRover*: autonomous program improvement.
- Zilberstein, N., Saliling & Silva, A. (2024). Outcome Separation Logic; tri-abduction for branch composition. arXiv:2305.04842.

## Extended intellectual lineage {.appendix} {#lineage}

*Foundational sources grounding §(grounding), §(epistemics), §(hygraph), and §(related-work), collected here so Related Work stays focused on contemporary systems.*

### Peircean inquiry and the philosophy of science

- **Peirce 1878** (*Illustrations of the Logic of Science*): the original three-mode taxonomy.
- **Peirce 1903** (*Pragmatism as the Logic of Abduction*): abduction as the only mode that introduces new content.
- **Bacon 1620** (*Novum Organum*); **Popper 1934** (*The Logic of Scientific Discovery*): falsification as the inductive-side constraint.
- **Ramsey 1926** (*Truth and Probability*): operational credence as betting odds; the hypothesis graph's node-level semantics descends from this work.
- **James 1907**; **Dewey 1929**: the pragmatist commitment that truth is inseparable from action.
- **Meehl 1967**; **Feynman 1974** ("Cargo Cult Science"): the difference between rigor-shaped activity and actual rigor, the standard §(right-regime) holds itself to.
- **Kimball 1957; Tukey**: the Type III error, the exact answer to the wrong question; a reminder that a perfectly checked receipt can still encode the wrong predicate.

### The hypothesis graph's structural ancestors

- **de Kleer 1986** (assumption-based truth-maintenance systems): persistent dependency structures over beliefs with mechanical retraction; the TMS keeps consistency where the hypothesis graph keeps *trials*, and a TMS justification is not replayable by a stranger.
- **Dung 1995** (abstract argumentation frameworks): attack relations between claims as first-class structure; the hypothesis graph's kill edges are attack edges bound to executions rather than arguments.
- **Wald 1947** (sequential testing) and **Vovk & Wang 2021** (e-values): the sequential-evidence framing that shaped `inquire`'s diagnostic stance. No accumulator is deployed: the code under test is deterministic, so the gate routes on the binary grader verdict (§(gating)).
- **Pearl 1988; 2000/2009**: DAGs as the substrate for structured belief and causal-structure inference; this work borrows the typed-node/typed-edge form and leaves the probabilistic semantics behind.
- **Zeller & Hildebrandt 2002** (delta debugging): the canonical demonstration that mechanical perturbation of code is a productive inference primitive; optimization-shape where the hypothesis graph is methodology-shape.
- **Reiter 1987** (*A theory of diagnosis from first principles*) and **de Kleer & Williams 1987** (the General Diagnostic Engine): model-based diagnosis as conflict sets, minimal hitting-set diagnoses, and entropy-minimizing choice of the next measurement. The hypothesis graph runs this abductive loop but over an open, LLM-generated hypothesis space rather than a fixed component model, and its "where to perturb next" is the GDE measurement-selection problem handed to the reasoner. Reiter's hitting sets are the theory of how multiple kills jointly localize a cause.
- **Clarke et al. 2000** (counterexample-guided abstraction refinement, CEGAR), **Solar-Lezama et al. 2006** (counterexample-guided inductive synthesis, CEGIS), and **Cousot & Cousot 1977** (abstract interpretation): the closest formal kin to the hypothesis graph's loop, in which a counterexample *is* a kill that names the next refinement. The hypothesis graph generalizes that loop from a closed abstraction domain or synthesis grammar to an open hypothesis space, which forfeits the completeness and sound-by-construction refinement that closure buys (the open-world relevance boundary is undecidable in general, reducing to Rice's theorem) and recovers soundness only per node, through replay. Two pieces of their machinery are unported and natural to inherit: the real-versus-spurious counterexample check (a principled test of whether a kill is genuine or an artifact) and widening (a principled stop that over-approximates with stated precision loss, the formal form of declaring an inquiry's trajectory oscillatory and committing to the general shape).

### Bi-abductive and compositional inference

- **Calcagno et al. 2009**: compositional shape analysis via bi-abduction; Facebook Infer as the industrial-scale instance of typed-mode inference on real code.
- **O'Hearn 2019**: separation logic and incorrectness logic.
- **Zilberstein, Saliling & Silva 2024** ([arXiv:2305.04842](https://arxiv.org/abs/2305.04842)): Outcome Separation Logic; tri-abduction for branch composition.
- **Bylander et al. 1991**: abductive computational complexity.
