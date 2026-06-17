---
variant: post-paper
autonumber: true
title: "The Hypothesis Graph: Semantic Memory Written by Methodeutics"
tags: methodology, epistemology, coding
keywords: hypothesis graph, methodeutics, abductive inference, agent memory, cognitive architectures, LLM agents, provenance, auditability, falsifiability, machine epistemics, post-cutoff evaluation
---

*[Download PDF](/assets/the-hypothesis-graph-semantic-memory-methodeutics.pdf) · arxiv-shape preprint, rebuilt from this source. · Receipts: [the bench run](https://github.com/kimjune01/swebench-pro) ([DOI](https://doi.org/10.5281/zenodo.20691978)) · [the determinacy audit](https://github.com/kimjune01/swebench-pro-audit) ([DOI](https://doi.org/10.5281/zenodo.20738220)) · [the mechanism experiment](https://github.com/kimjune01/hygraph-mechanism) ([DOI](https://doi.org/10.5281/zenodo.20691974)), each reproducible from its own committed artifacts.*

## Abstract {-}

The **hypothesis graph** is a novel data structure for coding agents that can deepen their reasoning and make it accountable. Implemented at the harness layer, its nodes are testable claims, its edges the conditions that refute them. It updates by inquiry, whose novel mode is abduction, beyond deduction and induction. Here, we demonstrate the mechanism on one contamination-free bugfix that an agent on a minimal prompt could not generalize; we supply the missing comparator that a context-bound agent could not abduct. This enables verifiable accountability, coordinated concurrency and efficient reasoning retention at no additional training cost, employable by any coding agent harness today.

## Introduction {#introduction}

In coding agents, the LLM is wrapped in a harness: the verification, testing, and memory a software task needs. The field building these is moving up a level of abstraction, from the model to the harness. Roychoudhury et al. (2025) reframe the goal as *programming with trust*, arguing that deployment turns on verification, testing, and analysis built into the agent rather than on raw generation ([arXiv:2502.13767](https://arxiv.org/abs/2502.13767)). Liu et al. (2024) survey agents for software engineering and organize the field around those same missing pieces ([arXiv:2409.02977](https://arxiv.org/abs/2409.02977)); Yehudai et al. (2025) add that scoring final outputs misses the reasoning and failure causes inside a run, and call for trajectory-level assessment ([arXiv:2503.16416](https://arxiv.org/abs/2503.16416)); Wang et al. (2025) name the lack of persistent, structured memory as a core limit, leaving agents to repeat errors and forget past successes ([arXiv:2508.11126](https://arxiv.org/abs/2508.11126)).

A patch passes the visible tests, but that's not enough: passing certifies only the cases the tests cover, not correctness. An over-narrow patch passes them and is wrong off-suite. Confirming it means reconstructing the reasoning the agent never recorded, at a cost approaching that of producing it, so the work shifts from writing to checking. Code review is the bottleneck.

When reasoning is discarded, each run rebuilds context from scratch. Even where agent memory adopts the cognitive-architecture lineage, as CoALA (Sumers et al. 2024) does in mapping it onto Soar (Laird 1987) and ACT-R, the semantic slot stores facts rather than a falsifiable structure, so the search is discarded once a patch passes. At best, a trail of blobs is saved as provenance.

We were promised a junior developer with near-infinite patience. All we got was tool calls in a loop: a cracked-up amnesiac contractor, leaving mistakes for maintainers to review.

| Problem | Solution |
|------------------|------------------------------------------------------|
| *Reasoning cost* | A domain-aware *division of intellect*: the model reasons, the harness holds the open hypotheses and runs the gate. |
| *Agent trust* | A *verifiable reasoning chain*: a claim clears only when an independent party reruns its recorded trial. |
| *Lost reasoning* | A *human-legible representation*: typed nodes a later run or a human reads and replays. |
| *Review bottleneck* | Every step *grounded in a trial*: a reviewer accepts the work or resumes where it stuck. |

Here we give the agent a trail of [**verifiable knowledge**](/verifiable-knowledge). The **hypothesis graph** is a semantic memory that holds an agent's reasoning while it works. The fix arrives with the inquiry that produced it: what was hypothesized, what was tested, what was ruled out. Each step carries a trial a stranger can rerun. The promise reverses the trust assumption by shifting the burden of proof outside the agent. The model still reasons, but each node it produces is checkable on its own at the harness layer, independent of the model.

## The hypothesis graph {#hygraph}

### Requirements {#requirements}

A semantic memory that holds an agent's live reasoning must clear four requirements at once:

- **Holds hypotheses.** Stores a hypothesis still under consideration, where prose, skill libraries, and retrieval keep only verified facts and established chunks: the hypothesis-shaped gap none of them fills.
- **Refutable by test.** Each claim carries a kill condition: the executable test that can prove it wrong.
- **Independently verifiable.** A stranger verifies a conclusion by rerunning its recorded trial, instead of re-deriving the reasoning or taking the author's word.
- **Persistent memory.** The trail persists past the context window rather than being discarded once a patch passes.

Prior structures fill some of these roles (✓ native, ◐ with common extensions, ✗ needs another layer doing the work).

| Structure | Holds hypotheses | Includes tests | Independently verifiable | Persistent memory |
|-------------------------------|:-------:|:------:|:------------:|:--------:|
| **Hypothesis graph** (this work) | ✓ | ✓ | ✓ | ✓ |
| Truth-maintenance (Doyle 1979; de Kleer 1986) | ✓ | ◐ | ◐ | ◐ |
| Provenance / lineage (W3C PROV, Moreau et al. 2013) | ◐ | ◐ | ◐ | ✓ |
| Search + proof tree (Clarke et al. 2000; Solar-Lezama et al. 2006) | ✓ | ◐ | ◐ | ◐ |
| Argumentation (Dung 1995; Modgil & Prakken 2014) | ✓ | ◐ | ◐ | ◐ |
| Event-sourced log / ReAct trace (Yao et al. 2023) | ✓ | ◐ | ◐ | ✓ |

*The middle two columns are verification (a falsifiable trial a stranger can rerun), the outer two are the hypothesis-shaped gap and retention. Only the hypothesis graph clears all four in one append-only file.*

The LLM finally satisfies all four together. Filling the graph takes a reasoner that reads a surprising failure, proposes candidate causes in open vocabulary, and turns each into an executable test, with no hand-built domain model. Classical inference engines could do this only inside a formalism encoded by hand, which is why the slot stayed a research program; the LLM populates it across arbitrary codebases, which is what makes the structure practical here.

### Graph semantics {#graph-semantics}

The structure meets all four with three pieces, a node, an edge, and one invariant. A **node** is a claim bound to a trial: a hypothesis, the perturbation that tests it stated as an exact command, the observed outcome, and a credence typed by the reasoning mode that established it. An **edge** is generated by a kill condition: the manner of a hypothesis's death names the next hypothesis, so the structure is self-extending, with no external controller deciding where to look. The invariant comes before the operations, because every operation is defined to preserve it:

> **Replay invariant.** Every node is reconstructible, by a stranger who does not trust the author, from its recorded trial alone: the exact command, the observed outcome, the verdict, and the credence cap.

The contract holds on the node's mechanical skeleton; the hypothesis prose the node also carries falls outside it, by design. The prose is the part an auditor would otherwise have to trust, and the recorded trial is what replaces trusting it, so the invariant draws its line exactly where checkability begins. The guarantee is narrow and named: the command, outcome, and verdict are checkable, while the mode label that caps a credence is a convention the writer is trusted to apply honestly.

### Operations {#operations}

Five operations maintain the structure, each defined with the one-clause argument that it preserves the invariant, the way a balanced tree's insert is defined to restore balance:

- **Create** (a smart constructor), append a node: abduction writes a hypothesis with its kill condition and the exact trial that tests it ("the bulb is dead", trial `swap in a fresh bulb`). *Preservation*: a node is admitted only if its trial replays, so by construction every committed node satisfies the contract, and the invariant holds by induction over reachable graphs. This admission rule is what makes every later operation safe.
- **Read / replay**: ask which hypotheses are still open, and reconstruct any node by re-running its recorded trial, no trust in the author required. *Preservation* is vacuous, read mutates nothing, but replay is the one that does the work, the check every other operation's preservation is stated against.
- **Classify** (the update): a trial's outcome marks its node *killed* or *witnessed* and caps its credence at the mode that earned it, a verdict written once. *Preservation*: classify appends a verdict and never edits the recorded trial, so the node still replays to the same outcome.
- **Link** (edge-from-kill): the manner of a hypothesis's death names the next hypothesis (the dead bulb names "the dimmer is broken", trial `bypass the dimmer to the wall`), so a classification spawns the next node with no external controller. *Preservation*: link only appends, and each new node is admitted under Create's rule. This is the one genuinely novel operation.
- **Prune**: a dead branch leaves the working frontier while its record stays in place. *Preservation* is trivial, prune is a frontier-set operation that changes what is *live* and deletes nothing, so every pruned node replays exactly as before.

![A hypothesis graph, two nodes and the edge between them, on the dead-light inquiry. The bulb hypothesis is killed by a cheap trial (swap in a fresh bulb, still dark); its death names the next node, the dimmer, which a second trial witnesses (bypass it to the wall, the light comes on). Each node binds a hypothesis to a trial, an observed outcome, and a credence capped by the mode that earned it: abduction proposes and stays low, induction is test-backed and rises. Every node rebuilds from its recorded trial, so an auditor replays the structure instead of trusting it.](/assets/hypothesis-graph-anatomy.svg)

### Auditability {#auditability}

The invariant yields an essential property that no benchmark can evaluate:

> **Local Replay Auditability.** Any single conclusion is checkable by re-running that node's one recorded trial, without reconstructing the inquiry and without extending trust to whoever ran it.

This is, for inquiry, the analogue of a certificate a consumer checks without trusting the producer, and like the Merkle audit path or proof-carrying code, its value rests on a contract; a complexity bound is beside the point.

Two grades of it matter. Where the trial is a deterministic command over pinned inputs, a compiler on a fixed toolchain, a test in a container, replay is *strong*: re-execution reproduces the recorded outcome, and the lead case (§(right-regime)) is here. Where the trial runs a model or a live service, replay is *artifact-level*: the recorded output is verified and the deterministic predicate re-run over it, the command standing as a provenance event rather than a reproducible computation. The honest scope is the first shading into the second as the system under test grows less deterministic. Pruning leaves all of it untouched: a pruned branch drops from the working frontier but stays in the record, so its nodes replay exactly as before.

### Knowledge maintenance {#knowledge-maintenance}

The nodes are ordinary; what is novel is the edge semantics. A search tree finds; a proof tree justifies. The hypothesis graph is both at once, because the search path *is* the justification: every step was a trial.

It sits at the confluence of older lineages: truth-maintenance and model-based diagnosis (de Kleer 1986; Reiter 1987; de Kleer & Williams 1987), sequential experimental design (Wald 1947; Vovk & Wang 2021), abstract argumentation (Dung 1995), and counterexample-guided refinement (CEGAR, Clarke et al. 2000; CEGIS, Solar-Lezama et al. 2006). Refinement is the closest kin: a counterexample *is* a kill that names the next experiment, the hypothesis graph's defining edge. What is novel is running it over an *open* hypothesis space abduced in domain vocabulary. Replayability stands in for the sound abstraction a closed setting supplies for free, with completeness as the price the open move forfeits (§(lineage)).

The near neighbors each hold part of this and source the rest from outside themselves. A truth-maintenance system (Doyle 1979; de Kleer 1986) maintains belief status under assumptions, but the empirical trial and the kill-generated successor are external conventions. Provenance (W3C PROV, Moreau et al. 2013) records replayable activities, yet does not decide which hypothesis comes next. And the ReAct trace (Yao et al. 2023), the strongest mundane baseline, is an append-only log whose continuation policy the controller decides and the record never holds.

What the hypothesis graph adds is their composition in one append-only object: an open-domain hypothesis, its executable trial, its kill condition, and the successor that kill names. That object belongs to the verifiable family whose value is a contract rather than a complexity bound, certificate transparency (Laurie et al., RFC 9162), proof-carrying code (Necula 1997), content-addressed provenance: a data structure paired with the protocol that writes and checks it.

### Semantic memory {#semantic-memory}

This is the data structure for *testable* inquiry, and its entire power is the perturbation surface. Strip the ability to poke the system and read an outcome, and the same shape degrades into a plausibility tree, which is the confabulation failure mode it exists to prevent. It is also not how minds run. Minds run on simulation, fast and compressive and intuitive, but a simulation is not verifiable from outside, so inquiry that has to be checked trades it for an explicit perturbation surface. The hypothesis graph is the verifiable serialization reasoning compiles to, so it can be checked by someone who does not trust you. Proof is to intuition as the hypothesis graph is to inquiry: not the thinking, the residue of the thinking that survives a stranger's replay.

That residue is what the memory typology calls the `smem`: persistent, typed, queryable, and owned by the harness rather than the model. Those same properties make it an interface for agent interop: because the structure is typed and external, a second agent, a later run, or a human auditor reads and writes against one contract and can rerun any node rather than trust it (§(discussion)). The graph in this work is one markdown file per inquiry.

## Actionable epistemology {#epistemics}

Knowing is an act to update the credence of a claim. This is the subject of [Verifiable Knowledge](/verifiable-knowledge). In the Hypothesis Graph, knowledge has the following properties:

- **Three states.** Witnessed is true, a build presently passing; killed is false, a build gone red; open is *untrue*, a conjecture awaiting its test. These are the [entitlement ledger](/verifiable-knowledge#the-warrant-ledger)'s states, scoped here to one node and its kill edge.
- **Credence.** A node carries a credence capped by the mode that earned it, low for abduction, higher once tested (Ramsey 1926), the step a bare LLM skips when it emits uniform confidence with no propagation along the chain.
- **Survived belief.** A node counts as knowledge only after withstanding a trial, a verificationist criterion (Ayer 1936), indexed to the stakes of acting on it. Before trial, a claim is a hypothesis.
- **Causal connections.** Each node wires to what it depends on, so claims compose into a derivation, every step caused by an earlier one (Pearl 1988).

The resolution of causality sharpens with each round of inquiry. It can locate causal boundaries, allowing generalized solutions to emerge. With each successive trial, credence accumulates to actionable confidence.

![A claim and its trial as one record. Left, the claim: a load resting on a span, *this bridge holds the load*. Right, the trial: a toothpick-and-gumdrop model bridge bearing a steel weight across two supports. Photo: Oregon Department of Transportation, CC BY 2.0.](/assets/bridge-trial-light.svg)

This is one more projection of the protocol [Verifiable Knowledge](/verifiable-knowledge) sets out, from where the agent stands, and its payoff is transfer. Paired with its trial, a node carries its warrant across intact; handed on the author's word, only the verdict crosses and the warrant is re-derivable from scratch.

A coding agent is already a strong internal verifier, running the test and verifying that it passed. What it lacked was the protocol, extending credence beyond the context window. With the protocol, knowledge compounds for other agents and humans.

## Methodeutics: a discipline of inquiry {#grounding}

A store of causal knowledge needs reasoning to be encoded into it. How can reasoning become mechanical enough for encoding? The insight, the leap to a candidate cause, stays with the model, but the harness needs a method to stage reasoning. Reasoning then becomes mechanical the way a proof is, through the discipline of checking ideas. In a precise and limited sense the harness encodes and generates reasons mechanically. This discipline, Peirce called **inquiry**.

His *Illustrations of the Logic of Science* (1878) and *Pragmatism as the Logic of Abduction* (1903) type the operations of inquiry into three irreducible modes.

- **Abduction** generates explanatory hypotheses for surprising observations: *what would, if true, make this no longer surprising?*
- **Deduction** derives testable predictions from hypotheses: *if this hypothesis holds, what follows?*
- **Induction** tests predictions against evidence: *does the evidence accord with the prediction?*

![The three modes as one cycle: Observation → Theory (abduction), Theory → Experiment (deduction), Experiment → Observation (induction).](/assets/modes-of-reason-triangle-light.svg)

No single mode carries a belief to its grade. Abduction proposes content but does not test it; induction tests but introduces no new explanatory content; deduction traces consequences but invents nothing. The credence a node ends up with is what traversing all three earns it, and that is what it means to call the modes typed: each is fixed by what it can't do.

Deduction is where readers balk: why is *abduction* responsible for theory? Isn't that deduction's job? No. Deduction neither generates the theory nor proves it; it unfolds the hypothesis into the predictions it must answer for. The theory was abduced, the predictions deduced, and induction does the testing.

Keep them separate and each does its one job; collapse them and you get familiar failure modes:

- **Confirmation bias**: induction without abductive alternatives
- **Confabulation**: abduction without inductive grounding
- **Free-association**: no typed mode at all

That collapse is exactly what modern LLM agents do by default, since a single forward pass proposes, predicts, evaluates, and rationalizes in undifferentiated prose. Methodeutics, Peirce's term for the methodology of inquiry, is how to conduct the typed-mode loop well. Encoded as skills, it constructs and maintains the `smem`.

*Modes of reason and the irreducible three.* Around the act of testing, philosophy of science built an apparatus of real rigor: Bacon's induction (1620), Popper's falsifiability (1934), Meehl's "soft science" critique (1967), Pearl's causal calculus (2009). Justification got its method, every step of it. But it begins one step too late, taking the hypothesis as given and filing its origin under inspiration. The discipline built an epistemology of justification and none of discovery. Peirce alone named the operation, abduction, and was ignored. The harness runs it as a first-class typed mode.

## Methodeutics, applied {#application}

Putting the theory to work means generating hypotheses as typed nodes the harness can test, instead of trusting whatever a model guesses.

*The abductive primitive is a diff.* Generating a hypothesis means manufacturing a diff: a before snapshot, an after snapshot, and the perturbation that flipped read as figure against the ground that held (Rubin's Gestalt terms). Separation logic already formalized this move as *bi-abduction*, inferring the invariant frame around a change, and scaled it to real codebases in Facebook Infer (Calcagno et al. 2009; O'Hearn 2019). `inquire` works at the simplest level: one before/after diff, with the frame inferred from the symptom. The extensions to branches and compositional cases are in the [lineage appendix](#lineage).

The "XOR" used throughout is shorthand for that bi-abductive separation: the figure (what the fix must change) held apart from the ground (the frame that stays invariant). Where bi-abduction infers the frame to make a proof go through, the harness fires the same split as a check, computing the symmetric difference against a known-good oracle and keeping only the cases it flags.

![Bi-abduction on a dead fixture. With dimmer, fixture, and bulb all intact, the static scene names no suspect; the perturbation bypasses the dimmer to the wall, and the XOR isolates the figure (the dimmer) from the ground (fixture and bulb).](/assets/bi-abduction-dimmer.svg)

*Directed graphs as reasoning representation.* Pearl 1988 (*Probabilistic Reasoning in Intelligent Systems*; Bayesian networks as DAGs of dependencies); Pearl 2000/2009 (*Causality*; structural causal models, d-separation, do-calculus). Pearl's lineage was built for causal-structure inference; our data structure (typed nodes, directed edges) puts it to hypothesis representation. The difference from a Bayesian network is one of kind, and runs deeper than dropped probabilities. A Bayes net conditions over a fixed variable set and propagates probability along edges of dependence; the hypothesis graph abduces its nodes as the inquiry runs, its edges genealogical, a dead hypothesis naming its successor rather than a conditional dependence. A Bayes net is justification over a space it is handed; the hypothesis graph generates the space.

![The hypothesis graph for the dead fixture. Abduction fans the observation into four typed candidate nodes; mechanical kill predicates fire on three (the socket, fixture, and bulb each cleared by a cheap test), the dimmer node is witnessed by the bypass and closes the last open hypothesis, and deduction derives the fix. Typed nodes, directed edges, all three modes in one inquiry.](/assets/hypothesis-graph-fixture.svg)

Isn't generating that space just debugging? It is, and debugging has been automated for decades: spectrum-based fault localization, statistical and delta debugging, model-based diagnosis, and search-based program repair are mature fields (Jones et al. 2002; Liblit et al. 2005; Zeller & Hildebrandt 2002; Reiter 1987; Le Goues et al. 2012; Monperrus 2018). Debugging tools already automate the loop; what is new is that the hypothesis graph persists it. Every engineer, and every repair tool, runs some version of abduce a cause, kill it on evidence, witness the survivor, derive the fix. But the engineer runs it in their head, and the tools, whatever logs they keep, do not persist the search as a typed, replayable hypothesis graph.

We implement this loop as a tool. *abductor* ([github.com/kimjune01/abductor](https://github.com/kimjune01/abductor)) externalizes the diff generation outside the context window, so a model has to represent the rule instead of tabulating the case in front of it: it enumerates a space wider than the model's hypothesis, calibrates each case against a known-good baseline, and exposes one pass/fail gate, with the answer key held outside the model's view. A failing case is a counterexample that forces the next fix, and the search records itself as the hypothesis graph, fixes as nodes and counterexamples as edges.

## The methodeutic harness {#method}

How do epistemology and debugging become an agentic harness? The loop that writes the graph needs four things:

- **Iteration.** One pass can't be trusted, so the loop re-enters on failure.
- **Deterministic oracle.** A model can't be trusted to catch its own bias, so the check comes from outside the weights.
- **Three modes of reasoning.** Abduction, deduction, and induction stay typed and separate, each capped at its own confidence.
- **Semantic memory.** The reasoning is recorded into the hypothesis graph and survives the context window.

Concretely, this is a skill with a tool call in a loop: the outer deterministic driver invokes an agent via the `inquire` skill, who accesses the deterministic `abductor` tool. It mechanizes the XOR operation.

![The `inquire` skill: Peirce's three modes as a procedure that writes the hypothesis graph. Induction fires a deterministic kill or witness with no model arbitrating. `implement` and `attest`, which read the survivors and verify the patch, follow below.](/assets/inquire-skill.svg)

### The inquiry frame {#inquiry-frame}

We recast each issue as an inquiry on an engineered system: a failure trace, a codebase, a root cause to find, and an intervention that must not regress the rest of the system. Code is the right substrate for the hypothesis graph because it combines three properties that other inquiry domains rarely bring together:

- **Reproducible**: same input yields same output, modulo controlled nondeterminism
- **Deterministic**: causal lines from input to behavior are mechanical
- **Perturbable**: single-line and single-function diffs are cheap to apply and fully observable

Because those three hold together, kill conditions over code are exact executions.

One trial settles the predicate in this regime. In code the per-case response is mechanically observable, so a single passing test on a captured diff is a complete verdict that the diff satisfies the executable predicate for that case. That verdict speaks to the predicate alone: behaviors it doesn't cover are out of scope, a boundary that §(right-regime) shows is exactly where the differences live. Where such verdicts are aggregated, the right summary is counts and denominators rather than confidence intervals: per-case verdicts are exact, and aggregating them is bookkeeping.

The three Peircean modes are how `inquire` builds the graph, each node typed by the mode that established it and capped at that mode's confidence:

| Mode | What `inquire` does | Confidence |
|------------|---------------------------------------------------|---------|
| **Abduction** | Proposes candidate root causes from the observed failure; writes hypothesis nodes with falsifiable predicates and kill conditions (read-only) | low |
| **Deduction** | Traces each hypothesis's consequences through the code to localize the suspect set | high |
| **Induction** | Tests survivors with cheap read-only experiments (prints, intermediate data) | moderate |

`implement` then writes the surviving hypothesis, with an adversarial challenger critiquing the diff against the spec. `attest` runs the test suite, takes the grader's pass/fail verdict, and emits a re-entry route (`inquire`, `implement`, or `none`) from a fixed verdict→route table. The driver parses the verdict and the route; both are mechanical, and no model decides termination.

### Hypothesis graph as inquiry output {#recon-output}

`inquire` emits the hypothesis graph: the structured-analysis document that precedes the patch. Kill conditions are mechanical predicates over the evidence trajectory, so a node dies when its predicate fires and not before. The graph persists across iterations; re-entry adds nodes rather than overwriting. The frontier closes only when every open hypothesis is killed (a test refutes it) or witnessed (a test confirms it).

A committed node is a conclusion, and an inquiry that reaches one rarely runs straight. Following the `inquire` skill on a real bug, a single hypothesis flips across all three modes and a kill before it settles:

> abduction → deduction → kill → abduction → deduction → induction → deduction → induction ⇒ induction · 93%

*An in-flight inquiry trace, illustrative: Sonnet 4.5 following the `inquire` skill on the python-dotenv `find_dotenv` v1.0.1 regression (a real, reproducible bug, every command run). The active hypothesis cycles through all three modes and a kill before the inquiry settles; a committed graph records only the terminal node (induction · 93%) and discards this sequence. Full trace: [recon-inflight-dotenv.md](/assets/recon-inflight-dotenv.md). Not a frozen Pro instance.*

### Blind cross-model challenge at the hypothesis stage {#blind-blind}

To keep that hypothesis from being one model's artifact, two frontier models from different families receive the same evidence pack with no cross-visibility, and each produces a hypothesis independently. A third pass extracts the disagreements: the disagreement becomes the next node in the graph, while the agreement is recorded but not actionable. Adversarial filtering operates at hypothesis time, while the worktree is still untouched, rather than at patch time where the diff is already written. Sampling stochasticity alone produces real divergence even within a single model; cross-family divergence compounds it with architectural and training-corpus differences. Both are signal.

### Deterministic gating and the outer loop {#gating}

The control loop is standard: the driver routes on `attest`'s verdict and re-entry route under a bounded attempt budget, and a failure re-enters `inquire` with the updated graph rather than retrying the patch, so the hypothesis graph doubles as the loop's checkpoint and no dead branch is re-proposed. That leaves the inner layer still owed a demonstration. The external oracle the opening made the crux is what the gate leans on, and §(right-regime) isolates it on a single bug, where it does most of the work the bench number seems to credit to diagnosis.

### Artifact availability {#artifact}

All code and data are openly available, each developed in a public repository and archived under a DOI for permanence. `abductor`, the tool that mechanizes the gate, is developed at [github.com/kimjune01/abductor](https://github.com/kimjune01/abductor) and archived at [doi.org/10.5281/zenodo.20738162](https://doi.org/10.5281/zenodo.20738162) (v1.0.0, AGPL-3.0). The mechanism experiment of §(right-regime) is developed at [github.com/kimjune01/hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism) and archived at [doi.org/10.5281/zenodo.20691974](https://doi.org/10.5281/zenodo.20691974) (v1.0.0, CC BY-SA 4.0); the archive carries the preregistration, the rebuild-confirmed dataset, the regrade script, and the climb traces. Every reported result reproduces from the committed inputs of the archived version.

## The mechanism: Verus #2219 {#right-regime}

We tested the assembly the field's way first, and the result is a null worth stating once and then leaving behind. Run on SWE-bench Pro, the assembly resolves 95.3% of the public split under the official grader, and that number measures oracle availability, not the method. On the public split the failing tests are visible, the gate iterates against them, and any competent coding agent handed that signal reaches the mid-nineties. A preregistered oracle bracket prices the gift: an implement-only loop with no oracle floors at 50%, and restoring the tests for the gate raises the ceiling to 96%, about 46 points bought by access with no harder reasoning. Every diagnostic channel we could cut came back near zero on top of that, the methodeutic vocabulary scoring no better than the bare task and a minimal prompt with no graph landing about a point under the full harness.

| arm | resolves | reads as |
|---|---|---|
| implement-only, no oracle | 50% | the floor |
| + failing tests restored to the gate | 96% | +46 points, bought by access |
| methodeutic vocabulary | ≈ bare task | method adds nothing the bench can see |
| minimal prompt, no graph | ≈ 1 point under full harness | graph adds nothing the bench can see |

A determinacy audit said why, before the result: SWE-bench Pro grades spec-conformance, so it hands the diagnosis over inside the problem, and a tool whose job is diagnosis has nothing left to do. The null is the bench unable to see a diagnostic method at all, the predicted signature of a mechanism that fires only where a benchmark cannot reach (full per-channel receipts in the [bench repository](https://github.com/kimjune01/swebench-pro)).

Where a benchmark cannot reach is an undiagnosed bug whose correct fix is a predicate, not a case, with no cheap oracle and a genuinely hidden cause. Far from a corner case, that regime is most of software, every issue tracker a backlog of undiagnosed problems waiting on the one expensive step a benchmark never exercises. The mechanism experiment ([github.com/kimjune01/hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism)) reconstructs that regime under control and runs the contrast a benchmark cannot, on a single bug dissected end to end rather than a population rate.

Verus is a deductive verifier for Rust: you annotate a program with specifications and ghost proof code, Verus discharges the obligations through the Z3 SMT solver, and a passing run certifies the code meets its spec. The cardinal property of any verifier is *soundness*, that it never certify a program which violates its spec, because every proof built on top inherits that guarantee. An unsoundness, where the verifier blesses a program it owes a rejection, is the worst defect it can carry and the hardest to notice, since the symptom is silence. Nothing fails. That is also what makes a verifier soundness bug the cleanest place to watch the mechanism work: the correct fix has to range over a whole class of programs.

### Why this bug fits {#verus-fit}

A soundness bug splits cleanly into the two arms the mechanism turns on, and #2219 splits more cleanly than most. One arm is free to grade: a program uninhabited by construction must be rejected, and the construction itself is the label, so thousands of such programs enumerate with no human in the loop. The other arm costs a human: genuine runtime divergence is *sound* and must be preserved, and no construction tells you which look-alike is which. The bug carries the easy oracle and the hard oracle in one place, which is exactly the contrast the experiment needs. More properties make it a fair subject rather than a flattering one:

- The fixes postdate every solve model's training cutoff, so the answer sat outside the reachable corpus at solve time.
- The maintainers were genuinely stuck, and the merged general fix took deep Verus knowledge and three months. No toy.
- The symptom sits far from the cause, so localization is hard.
- The project's own suite passes for *both* the narrow and the general fix, so it cannot see the distinction the fix has to make.

### The bug, and the axis the fix turns on {#verus-bug}

Verus reasons about Rust at the MIR level, rustc's control-flow graph of basic blocks. Rust's never type `!` is the type of an expression that never returns, so the code after it is unreachable and the compiler prunes the control-flow edge. Verus also has *ghost* code: specification and proof terms erased before compilation, with no runtime effect. The bug is the collision of the two. A ghost expression of type `!`, erased and so not actually diverging at runtime, still marked the following MIR unreachable, and Verus pruned a control-flow edge that is in fact live. With the edge gone the verifier treats reachable code as dead, never checks it, and a program it owes a rejection verifies vacuously. That is the unsoundness.

![The #2219 unsoundness as a causal chain. A ghost `!` expression is erased before compilation, yet MIR still marks the block after it unreachable, so Verus prunes a live edge and never checks the code behind it. The fix turns on the axis at the bottom: a ghost-erased uninhabited return whose code runs (keep the edge) against genuine runtime divergence whose code is dead (prune it), identical at the token, opposite in handling.](/assets/verus-2219-unsoundness.svg)

The narrow fix keys on the surface token: when the diverging expression is a literal `!`, keep the edge. The maintainer's first patch (#2230) does exactly this, and it is the ceiling every self-graded method reaches. The general fix is a different kind of object. It has to distinguish a *ghost-erased* uninhabited return, where the edge must stay because the code runs, from *genuine runtime divergence*, where the edge must go because the code really is dead, and it has to do so across the whole class of uninhabited types the `!` token never names. An uninhabited type is one with no possible runtime value; `!` is the obvious case, but Rust expresses many others, through empty enums, recursive-uninhabited constructors, associated-type projections, and nested generics. The maintainer's general patch (#2501) reached it by recording each call's inhabitedness in Verus's own semantics, staying deliberately conservative. This is the "fancy XOR" the experiment lives on: keep the edge for ghost-erased uninhabited returns, prune it for genuine runtime divergence, two arms that look identical at the type `!` and demand opposite handling. A surface-token fix cannot see the second arm at all.

| arm | what it is | at runtime | correct edge | narrow #2230 | general #2501 |
|---|---|---|---|---|---|
| *ghost-erased uninhabited* | erased spec / proof term | code runs | **keep** | literal `!` only | whole uninhabited class |
| *genuine runtime divergence* | real non-returning code | code is dead | **prune** | unchanged, already pruned | unchanged, already pruned |

### Designing the experiment {#verus-design}

Every arm writes a hypothesis graph by the same loop; what varies is only where a kill gets its truth, the model's own belief or an external reference. The model, the loop, and the bug are held fixed across all of them, so any gap traces to the oracle's source. Six prompt-encoded approaches grade their kills against the model's own belief, the hypothesis-graph inquiry among them, each run three times; one method, the `abductor` gate, grades against an external oracle. Candidates were drawn from the localization-hard band the lead case and its two neighbors define (§(other-cases)), and the protocol preregisters one sentence per loop, testing X, predict Y, refuted by Z, before any arm runs (`METHODOLOGY-preregistration.md`).

**The contrast.** The experiment isolates the axis defined in §(method): whether a kill is graded against an **internal** oracle, the model's own belief, or an **external** one, a known-good reference the model cannot see (oracle in the metrological sense of an instrument checked against a reference, distinct from the probability-calibration of confidence scores). What carries it does not matter: whether the answer key arrives as a paragraph of prompt or as a CLI tool that holds it is incidental; what matters is only that it is encoded at the **harness layer**, outside the weights and outside the model's ephemeral reasoning.

The external oracle moves this number; the graph, held constant across every arm, cannot be what moved it. But externality is necessary, not sufficient. An external oracle with thin coverage drives a fix wide and leaves it broken (§(frontier)), so what sets the axis is whether the externally supplied labels span the distinction the fix has to make.

### The instrument is general, and blind to the answer {#gate-general}

The lift is reasoning-encoded-as-instrument only if the instrument did not smuggle in the fix, so this is established first. It did not. The instrument, released as `abductor`, has three domain-general operations and no answer built in:

- It *enumerates* a space of cases closed under the property's type-formers, wider than any one hypothesis.
- It *calibrates* each case against a known-good baseline, the comparator the model cannot author, so the ground truth is external to it.
- It *gates* on a single pass/fail signal the model hill-climbs against.

The instrument never names the predicate, the property, or the fix; the prompt that drives it demands generality and supplies the signal, and nothing else, so reaching the rule is the model's own reconstruction.

Two controls establish the blindness rather than assert it. The model received a prompt naming no property and still had to grep out rustc's own machinery for uninhabited types to climb. And handed only the vague instruction to range over type-formers and judge, a second model *rebuilt the instrument itself*, a 7026-case enumeration, which is what a general construction permits and a bespoke oracle does not. The construction also transfers across domains: the same enumerate-calibrate-disagree shape, pointed at an unrelated Go SBOM tool (syft #4760), surfaced eleven omitted cases where manual review had found four, and exposed a tabulation bug inside the comparison criterion itself. Only the grammar of cases changes between domains; the machinery is fixed. What every instance exploits is one general object, a disagreement, the symmetric difference between what the system believes and what is true, the check that tests and type systems cannot supply because absence has no test.

### The tiny bench, and what counts as golden {#verus-bench}

The case is one bug, so the bench is one bug, hand-built and small enough to state in full. It holds three states of the compiler, the buggy commit (base) and the maintainer's two later fixes (the narrow one and the general one), and a handful of probe programs, each of which the compiler either accepts (VERIFY) or rejects (REJECT). A probe's **golden** is the verdict a correct compiler owes it: REJECT for an unsound program, VERIFY for a sound one. Two sources supply those goldens, and keeping them apart is the method, because they are exactly the easy and hard arms of the result.

The case is a real historical PR, taken deliberately from after the cutoff. Verus #2219 is an issue the maintainers filed and closed, and its three states are real commits: the buggy base (2026-03-08), a narrow fix merged the next day, and the general fix merged on 2026-06-05. We chose it because those fixes postdate the solve models' training cutoffs (the contamination-controlled model is Fable, a January 2026 cutoff, against March and June 2026 fixes), so the merged solution was absent from the reachable corpus when the weights were frozen. A recall probe confirms it: asked in isolation how #2219 was fixed, the model does not recover the fix and says so. What it can reconstruct from general, pre-cutoff competence is that rustc carries uninhabitedness machinery at all, which is old and well-known; what it cannot recall is the merged fix for this bug. So the model's solution is reconstruction from prior competence, not recall of the post-cutoff patch. That is the property the case needs, and the commit dates and the probe transcript are committed alongside the dataset.

The bug probes are uninhabited programs *by construction* (an erased `!`, an empty enum, and two shapes the gate never sees: an associated-type projection and a nested generic). Their golden is REJECT, and the base compiler is wrong on exactly them, verifying what it should reject. That is the bug, and it makes base a free reference for the easy arm: the externalized gate enumerates such cases over the uninhabited type-formers (2856 of them), grades each candidate fix against the base verdict, and passes only when a fix flips the entire bug-set to REJECT (269 cases here) with no sound case newly rejected. No human labels these; the construction is the oracle.

The hard probes are different. Genuine runtime divergence is sound and must be preserved, so its golden is VERIFY, but base is not a usable reference there, and the gate's grammar contains no divergence-preserve shape, so the gate is blind to this arm. Its golden comes from human judgment; the two divergence probes are held out, authored by hand and kept outside the gate's grammar, so passing them tests whether a fix represents the rule rather than fits the gate. The two are not equally hard. One is in-bar: the maintainer's approved fix preserves it, so its VERIFY golden is corroborated by the shipped human bar. The other is a stretch goal beyond that bar: force-graded, the maintainer's own fix declines it too, conservatively by design, so its VERIFY golden is the operator's ideal, not a behavior any shipped fix delivers. This is the same asymmetry the deployment story rests on (§(enum-calib)): the oracle for the easy arm is free, the oracle for the hard arm costs a human.

One integrity hazard is controlled before any verdict is trusted. The compiler vendors a crate that a plain incremental build does not rebuild, so every verdict here is from a forced-fresh build, sources touched and the binary fingerprinted to confirm identity; the frozen dataset (21 artifacts, every one rebuild-confirmed) and the regrade script are committed.

### What we observed: the lift {#verus}

On a fixed toolchain with forced-fresh, fingerprinted rebuilds, six prompt-encoded methods across eighteen draws reached the narrow plateau and stopped: modal `changed`=114, the #2230 slice, none reaching `pass=true` (graph, minimal, neutral, site-enumeration, abduction, self-verifier). The single externalized-gate arm was the sole one to break off the narrow plateau to a wider fix: `pass=true`, `changed`=269 exactly, zero valid-preserve rejections on the gate's own cases. That fix is more general than the plateau but not yet the merged human fix; it stays wide-but-broken on the in-bar divergence case the gate never enumerated, the one the human fix preserves, dissected in §(frontier).

What it does reach is real: it flips the entire bug-set, and it rejects two *out-of-grammar* held-outs the gate never showed it, an associated-type projection (`<u8 as Tr>::A`) and a nested generic (`G<G<Void>>`). Those held-outs are the proof that the fix *represents* a general rule rather than *tabulating* the gate: instrumentation confirms each arrives already normalized to an uninhabited type, so the fix catches them by applying its own general predicate, never having seen the case. Which predicate that is, and how it differs from the maintainer's, is the subject of §(frontier).

### The frontier is the coverage {#frontier}

The mechanism, read from the 43,586-line climb trace: The gate's coverage sets the model's generalization frontier. Its first implementation is narrow, keyed on `is_never()`, the exact ceiling every prompt arm stops at. The gate then feeds it uninhabited cases that `is_never()` does not catch, empty enums and recursive-uninhabited constructors, which keep `mishandles>0` and bar `pass=true`. To climb, the model greps the codebase, finds rustc's existing inhabitedness machinery, and widens its predicate from `is_never()` to a check that keeps the CFG edge for any visibly-uninhabited ghost return, routed in this arm through rustc's `is_inhabited_from`. That widening off the narrow plateau is the lift, and the pressure that drives the model to it comes from the gate, while the prompt stays silent: the model supplies the discovery, the gate supplies the direction and the boundary.

A cross-model check narrows what the lift is. The inhabitedness query the codex arm routed through turns out to be behaviorally redundant: handed the same task, a second model (Fable) keeps the edge for every ghost-mode call with no inhabitedness query at all and grades identically on every probe, the out-of-grammar held-outs included. Since only an uninhabited return prunes the control-flow graph, the operative mechanism in both fixes is the same mode gate, keep the CFG edge in ghost mode so the borrow-checker sees the code that follows, and not recovery of the verifier's own decision procedure. So the lift is the model widening, under external pressure, to a mode-gated approximation of the right rule; it is not the model reaching the verifier's true oracle.

The handed gate's fix stays wide-but-broken here, over-rejecting the in-bar divergence case the merged human fix preserves, and the merged human fix reaches that case by a different, deliberately conservative implementation. That gap is not a permanent capability shortfall: once the missing calibration is supplied (§(enum-calib)), the corrected arm reaches the human fix's behavior on every graded probe. The held-outs still do their job: the fix catches `<u8 as Tr>::A` and `G<G<Void>>` it never saw, even though the rule it represents is the coarse mode gate, not the fine inhabitedness distinction.

The same mechanism predicts its own failure, which is why the failure belongs in the dissection and not in a caveat. The fix over-rejects two genuine-divergence cases, both sound. One is in-bar: the merged human fix preserves it, so over-rejecting it is the handed gate's real flaw. The other is a harder stretch case that the merged human fix also declines, conservatively and by design, because the bar it shipped does not promise it; over-rejecting that one is not a flaw the human fix avoids. The over-rejection sits exactly where the gate was blind: its 2856-case grammar contained no genuine-divergence-preserve shape, so that arm of the distinction received no climbing pressure. The target is the "fancy XOR" of §(verus-bug): keep the edge for ghost-erased uninhabited returns, prune it for genuine runtime divergence. The gate drove the first arm to full generality and left the second collapsed to an OR. The fix is *wide but broken*, general on the uninhabited-return arm and over-conservative on the divergence arm, and the held-outs outside the gate are what catch it. Coverage is the design lever, shown from both sides in one trace: where the gate pushes, the model generalizes correctly; where the gate is silent, the model over-generalizes.

### Enumeration is inducible; the oracle is not {#enum-calib}

The dissection has one more layer, and it locates the encoding boundary. Handed the same vague, leak-free prompt the prompt arms got, with no gate supplied, a second model reconstructed the gate on its own. It built a 7026-case enumeration over the uninhabited type-formers and hill-climbed against it to a self-certified zero over-rejections. Then it shipped the same wide-but-broken fix. A model can bootstrap the **enumeration**, the combinatorial breadth, because that is mechanical. It cannot bootstrap the **oracle**, the external ground truth, because its self-built gate labels each case with the very predicate under test, so the one case that needs a truth from outside its own belief, genuine divergence versus ghost-erasure, gets self-mislabeled as handled. One run shows both halves: a wide net the model built itself, and a blind spot precisely where its own labels could not reach. Enumeration is inducible; the oracle is not, at least not here. The claim is scoped to that self-grading circularity, not a proof that no model could ever induce an oracle from some other source. Within it sits the line between the reasoning a model already carries and the reasoning that must be delivered from outside.

A theoretical intuition sits under this, offered as motivation rather than proof. The data processing inequality (Cover & Thomas 1991) says no processing of what a system already holds can raise its information about the world; read as an analogy, enumeration is internal recombination and stays under that ceiling, while the oracle comes from a world-facing trial, the kind of step that admits information the weights did not contain. A model grading its own cases never runs that trial. Turning this into a theorem about LLM inference would mean formalizing the channel and the variables, which is out of scope here; we lean on it only as the shape of the boundary, the same place the receipt already locates it. ([Compress and Unfold](/compress-and-unfold) develops the same intuition from the cognition side.)

The half a model cannot induce is nonetheless cheap to the harness, because humans already rendered the judgments and left them in the repository. The merged fix, the regression suite, the resolved-issue label are goldens *because* a reviewer approved them. The missing oracle for #2219 existed all along: the maintainer's general fix verifies the divergence case the gate over-rejected, so calibrating differentially against base *and* the approved fix should close the blind spot, and supplying it does.

Handed that corrected calibration, the model crosses off the wide-but-broken plateau onto the divergence arm and writes a real ghost-versus-genuine discriminator. Force-graded against the merged human fix at its own toolchain, the corrected arm matches it on every probe: it now preserves the in-bar divergence case the handed gate over-rejected, and the one case it still declines is the stretch goal the human fix declines too. So calibration closes the gap to the shipped human bar rather than landing short of it; the residual sits beyond that bar. That the wall gives precisely when the missing oracle is supplied is the boundary's confirmation, it was the oracle and not a deeper limit, and the unblocking is model-dependent enough to be a property of the deployed workflow rather than a claim about weights, with implementation the residual wall where it does not occur.

The honesty here is an asymmetry, and it is structural rather than a hedge. Approved history supplies strong goldens for "do not break what works" and "this reported case is wrong", while the generalization itself goes ungraded, which look-alikes are the same bug and which are sound divergence. That disambiguation is the XOR's hard arm, un-oracled until a human spends the judgment, which is why the maintainer's fix took expertise. And the hardest look-alike is hard enough that the merged human fix declines it too, shipping a deliberately conservative bar rather than the full distinction, so past that point the wall is not the automation's alone.

*Not one model's artifact.* Under the same corrected-gate pressure, three workflows are driven to the same behavior, and force-graded against the merged human fix they match it on every probe: Fable, Sonnet 4.6, and Cursor's Composer 2.5, each on its own vendor CLI, clear the bug arm, preserve the in-bar divergence case, and decline the one stretch case the human fix also declines. The codex-CLI workflow does not clear it in either protocol, and a matched-budget, matched-protocol rerun leaves the divergence wall standing, so the gap is a workflow difference on this one case rather than a budget artifact; it is one *n*=1 cell per workflow and not a capability ranking.

Read the convergence as coverage-bound rather than as a scoreboard: it shows the corrected-gate fix is reproducible across workflows, not that three models independently rediscovered the predicate, since the shared decline on the stretch case is most likely the gate funnelling every successful arm into the one behavior it rewards, which the human fix happens to share.

Contamination is scoped the same way. Composer 2.5 ships after the fix, so its pass leaves recall not excluded; the two contamination-clean workflows (Fable, Sonnet 4.6) carry the narrower point that these runs do not require a recall explanation, and the merged human fix, dated after Composer's ship, is the anchor that makes that point datable. One earlier anti-recall argument is withdrawn here, because the control that would have carried it was finally run. The claim that the human fix is finer than the automated arms, and clears a case they miss, does not survive force-grading: the human fix is behaviorally identical to them on these probes and so cannot separate a memorizer from a reconstructor. That every successful run here uses the same externally supplied discriminator is consistent with a broader claim about how inquiry works, taken up as a conjecture in §(future-work); the receipt here stays scoped to what these runs show.

Retrospectively the goldens are free; prospectively, on a fresh bug with no merged fix, the easy arm has a golden and the hard arm does not. The division of labor is the deployment design: the model enumerates and fixes, the harness draws its oracle from approved history, and the residual hard arm is named, not hidden.

The whole ablation reduces to one grid, and the grid has a structure: the two middle columns flip on as soon as the enumeration goes wide, and the last column flips back only at the human general fix.

| Arm | Kill oracle | chg | \`!\`-bug | empty-enum | out-of-grammar | divergence | Bucket |
|------------------|------------|:-:|:----:|:----:|:-------:|:----:|------------|
| 6 methods (18 draws) | self | ~114 | ✓ | ✗ | ✗ | ✓ | **narrow** |
| \#2230 (maintainer, narrow) | human | 114 | ✓ | ✗ | ✗ | ✓ | **narrow** |
| `abductor` gate (handed) | external (vs base) | 269 | ✓ | ✓ | ✓ | ✗ | **wide-but-broken** |
| self-built gate (induced) | self (induced) | 269 | ✓ | ✓ | ✓ | ✗ | **wide-but-broken** |
| \#2501 (maintainer, general) | human | 269 | ✓ | ✓ | ✓ | ✓ | **general** |

*The Verus \#2219 ablation, one row per arm, ✓ where the arm handles the probe correctly (rejects the bug cases, preserves the sound ones). The reported \`!\`-bug column is solved by everything. The two middle columns, in-grammar empty-enum and the out-of-grammar held-outs the gate never saw, are the uninhabited-return generalization; they flip on the moment the enumeration goes wide, for the gate graded against an external oracle and for the gate a model induced for itself alike, and stay off for the narrow arms. The last column, the in-bar genuine divergence that must be preserved, is the XOR's hard arm; it is on for the narrow arms (which never reach far enough to break it) and for the merged human fix, force-graded to preserve it, and off for both wide gates, which over-reject it. (A harder divergence stretch case, beyond what the merged human fix promises, is declined even by that fix and is not a column here.) Enumeration moves an arm from narrow to wide and is inducible; the wide gates shown here, graded against the base alone or self-graded by the model, do not on their own preserve the in-bar divergence case. Supplying the divergence golden is what later moves a corrected arm onto it, to the human fix's behavior (§(enum-calib)).*

### Two surrounding cases, briefly {#other-cases}

Verus #2219 is the case under study; two earlier cases bound it and are kept only as pointers. **flux #1613**, an open, maintainer-stuck refinement-typing bug, is retained only as an *auditability* example, a 19-node replayable trail at tag `flux-1613-trail-v1` that stops short of a capability lift: de-hinted and run paired, its advantage oscillates between general and narrow rather than holding. **Verus #2427** marks the boundary from the other side: the external oracle was in place and did not engage, because the inquiry's perturbations stayed inside one feature family and never crossed the dimension separating the narrow fix from the general one. Together they fix the band the lift lives in, as one rule: an external oracle lifts capability when, and only as far as, the inquiry's perturbations span the dimension that distinguishes the reported example from the sound generalization. Both cases are in the repository.

### The null regime, and why it is narrow {#null-regime}

The lift engages in a narrow band, and most pilots fall outside it. On bugs drawn from the merged-PR pool and beyond it, the minimal baseline kept succeeding: a 5-line CLI fix in 91 seconds (qrtool #695), the deepest graph in the pool out-reasoned in two minutes (slang-server #310), a real clear()/ingestion data race in an LSM storage engine the pipeline had skipped as too complex (fjall #287), a decoration-leak the minimal agent localized unaided (bat #3710).

Two findings explain the nulls. First, a **selection artifact**: the deployment pipeline's own triage skill scores reproducibility up and fast-paths easy bugs around the graph (its rule, verbatim: "a 1-line fix with a confirmed reproducer doesn't need a hypothesis graph"), so the merged pool is precisely the subset where the pipeline says the graph is unneeded. Second, **baseline reach**: a capable model in a minimal loop diagnoses and fixes most reproducible bugs unaided, so the band where diagnostic structure changes a pass/fail verdict is narrow, bounded below by the minimal loop's own reach and above by triage.

The deployment merge rate inherits this: the 81 merged PRs (§(discussion)) were never graph-dependent, a minimal prompt digs the few levels most of them need. The Verus case is chosen to sit inside the band, where the symptom is far from the cause and the suite cannot see the difference between a narrow fix and a general one; that placement is the point, and it is also why a population rate over an unselected pool would measure the band's width rather than the mechanism.

## Models and provenance {#models}

No training, no fine-tuning, no learned weights in the harness. Each stage invokes a vendor's shipped agentic CLI (Claude Code for the Sonnet 4.5 generator, codex for the GPT-5.5 challenger, Cursor in the open-weight run), so the harness is a typed meta-loop over off-the-shelf agents, owning only the stage contracts, the hypothesis graph, and the gate between them. The generator ran with extended thinking on; the challenger arbitrated with reasoning off, a point against a model-deliberation reading of the gate. For each scored instance the loop reads only that instance's own artifacts. Swapping the entire model pair to open weights ported the result with no structural change, evidence the harness is not vendor-specific. The benchmark run summarized in §(right-regime), its per-channel attribution, the oracle bracket, the determinacy audit, and the per-instance receipts live in full in the [bench repository](https://github.com/kimjune01/swebench-pro), with the operational story in [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro).

## Discussion {#discussion}

### Attributed nulls and the typing protocol

The discipline that bounds the bench number (§(right-regime)) is the same one that makes a null publishable: preregistration, freeze, official-grader-only verdicts, per-instance provenance. These nulls publish *attributed*, each arriving with the mechanism that produced it, the gate compensating, the spec handed over, the lottery fraction. An unexplained null says stop; an attributed null says where to point the next instrument.

The same typing runs on the positive claims too. Each result is held to the verb its evidence can carry: the Verus case is a mechanism that *can occur*, shown by one dissected inquiry, with no claim to a rate or a frequency, and saying so is the typing protocol applied to ourselves. This is the [Type III](/type-iii-error) check, the [wrong question](/wrong-questions) caught before the claim is committed, and the hypothesis graph already encodes both of its corrections: a kill condition is a *reflex*, a mechanical check run before a belief is granted, and the credence cap is a *demotion*, the narrower claim a node settles for once the evidence is in.

Does the Peircean framing do any real work, or is it just decoration? Two kinds of work: on this bench, as *rhetoric* it is decoration (§(right-regime)); as *protocol* it is essential. The prompt ablation measured whether the vocabulary makes a single diagnosis smarter, and it does not. What it could not measure is interop. A hypothesis graph written in one context window must be read in another, by a different model, a parallel agent, or a human auditor, and the mode labels are what make a node interpretable without the context that birthed it: abduction marks a belief as proposed-untested, induction marks it as test-backed, and the credence cap travels with the type. Loose vocabulary produces graphs only their author's window can interpret, and those die with it. The Peircean typing is the wire format that lets the smem be shared across compactions, across agents, and across the trust boundary to the auditor, and the common vocabulary is the protocol for verifying each other's work: a peer that reads `induction, test-backed, here is the command` can rerun the command, where a peer that reads loose prose can only trust it or not.

This resolves the apparent tension with the prompt null rather than sitting beside it. A protocol does nothing by itself on any individual instance, the same way a wire format makes no single message smarter, so a per-instance ablation measuring the vocabulary against loose prose *should* read null, and did. The protocol's value accrues across instances, where accountability becomes transitive. When every node speaks the same typed contract, agent B can verify agent A's kill by rerunning it, agent C can build on B's verification without re-running A, and a human auditor can enter the chain at any link; the warrant flows down the chain with the receipts, never resting on any link's word: §(epistemics)'s per-hop lossless transfer, composed across the population. Loose vocabulary caps accountability at one hop, the author vouching for their own graph. A common protocol lets verification compose: that is what 385 graphs in one vocabulary are for, and the precondition for everything §(future-work) builds on them.

### The trace is the contribution

The reframe is from treating an agent as a source of verdicts to a source of claims bound to evidence.

The failure mode at issue is output that is confidently wrong and not cheaply verifiable. The Verus self-built gate is an instance of it. Handed a vague prompt, the model built its own 7026-case generator and hill-climbed to a self-certified zero over-rejections, reported the fix done, and shipped one that over-rejects genuine divergence anyway: green by the agent's own check and unsound at once. Nothing the gate enumerated detects it; only the held-out probes outside the gate, replayed against the patched build, expose it. This failure mode scales with model capability rather than against it, and is the default product of fluent generation; it recurred throughout this work, in the wide-but-broken fix, the 4/4 false-green self-audit, and the recall-inflated resolve rate.

The substitution is accountability in place of trust, checkable line by line. The self-graded agent produced a verdict, its own gate green; the externally-oracled inquiry produced a record of typed nodes, each a hypothesis, an exact command, an observed outcome, and the edge the result generates, every consequential one replaying on a clean build. Such a record is audited step by step without extending trust to its author, and the better fix is identifiable independent of the system that produced it. That property, rather than the outcome of any single comparison, is what survives.

**Truth is buildable.** The node semantics of §(epistemics) is what gives the trace its force here. If a true claim is a build presently passing and its warrant lives in the edges, then a node without a replayable trial is not a node at all, as an uncheckable number is not a measurement. A resolve rate, however honest, is a verdict over 728 builds an auditor cannot inspect; a hypothesis graph is the inspectable chain.

**The cost asymmetry of fabrication.** A fabricated reasoning trace is expensive to sustain, because every fabricated node must survive a replay the author does not control. A confident narrative is cheap to produce, because nothing in it is bound to a procedure. A self-graded method's over-narrow fix is the cheap kind: it reads as complete, and closer reading does not reveal the flaw, while the receipt reveals it in one command. Verification is therefore part of the method rather than overhead on it. The same asymmetry governs failure: a trusted verdict that fails leaves nothing behind, whereas a recorded inquiry that fails leaves a trail naming the failed node. The Verus climb recorded its own corrections in trail, the narrow `is_never` fix refuted by the very cases the gate fed it, each a kill that generated the next edge and itself a replayable trial.

**Persistence beyond the context window.** The context window is the model's working memory, and chain-of-thought stored there is lost when it closes. The hypothesis graph externalizes the reasoning before the window closes, demonstrated when a build host failed mid-investigation and only the externalized graph and patch survived to be resumed. The externalized form goes past readable to *re-runnable* later, provided each node carries its own reconstitution; without that, it only appears to outlast the window until resumption is attempted.


The scope is bounded: the logical content has no half-life, but the runnable form inherits the half-life of its apparatus (these graphs replay only while flux builds, z3 runs, and the SHAs resolve), so provenance approaches durability as replay approaches first principles. What it preserves is *checkability* rather than truth: a false claim backed by trust is laundered as its witnesses disappear, while a false claim backed by provenance remains detectable.

**Hidden effort is not reasoning you can check.** The frontier labs ship "reasoning" as an opaque dial, `high`, `xhigh`, `ultrathink`, a slider on how many private tokens the model burns before it answers. More of that setting is more *internal* work: the model proposes and grades against its own belief, harder.

The Verus result is where that runs out. The strongest internal-effort arm is a self-verifier told to build its own combinatorial generator and grade itself against it. It plateaus on the narrow case alongside every other self-graded method, while a single kill graded by an external oracle reaches the general fix (§(enum-calib)). You cannot turn the dial past this boundary, because effort scales the half that is inducible, the enumeration, and cannot manufacture the half that is not, a ground-truth oracle from outside the model's belief. And whatever the dial does buy ships nothing a stranger can rerun: an effort setting is the purest form of *take my word for it*, a larger number where a kill condition should be.

The position here is the opposite. Put the reasoning in the harness, typed and replayable, where its level is not a knob the auditor trusts but a trail the auditor checks. A graph of fired kills says what was ruled out and how; `ultrathink` says only that the model tried hard, and asks to be trusted.

**Trust versus accountability.** *Nullius in verba* extends to the machine: take no party's word, and check the receipts. To a maintainer a coding agent is a stranger, as is its operator, and with receipts attached this does not matter: a red-on-master/green-with-fix test, a soundness twin, and a clean suite read identically regardless of submitter. The 81 merged PRs are the ecological evidence: adversarial maintainers accepted agent-authored code at 50.6% on attached receipts rather than reputation. That deployment trace is committed, not asserted: 81 PRs merged across 73 cold repositories, agent-selected issues, agent-authored patches, zero human keystrokes in any diff, only about 8 of 79 closures rejected on the merits, the ledger GraphQL-verifiable (`pr-receipts.jsonl`), with ~385 hypothesis graphs from the same campaign public at [`kimjune01/sweep`](https://github.com/kimjune01/sweep) and the narrative in [Speedrunning Open Source](/speedrunning-open-source).

The maintainer evidence points at what alignment can mean: an accountable agent whose every claim is bound to a test a hostile party can rerun, never one taken on trust. A recent DeepMind position paper on *artificial epistemic agents* warns that verification by source authority is collapsing into a "verification crisis" and calls for "robust falsifiability pipelines" whose claims are "structured in a way that allows them to be proven wrong" (Marchal et al. 2026, [arXiv:2603.02960](https://arxiv.org/abs/2603.02960)); the kill condition is precisely what structures a claim to be provable wrong. Reliability is this same epistemics accumulated: a body of verifiable claims large and redundant enough to remove doubt, rather than trust arrived at directly. The guarantee is narrow: everything *recorded* is checkable, but nothing guarantees that everything *relevant* is recorded, and choosing what must be on the ledger remains a human judgment.

**The equilibrium resembles accounting controls.** Alignment is unlikely to resolve to a single answer. A plausible regime has the shape accounting reached after its own confidently-wrong-and-unverifiable era: standards (GAAP), independent audit, and the three-way match, in which no payment clears unless the purchase order, the receiving report, and the invoice agree, with no party trusted to hold more than one leg. This harness already has that shape: no claim clears unless the proposer's claim, the recorded trial, and an independent replay agree, and the generator never grades its own work. [Enron](https://en.wikipedia.org/wiki/Enron_scandal) illustrates the alternative: self-attestation scales until the failure that legislates the controls after the fact.

**Merit attaches to the work, not the doer.** Praise and blame are routed to doers for lack of vocabulary and norms that would route them to the work, a conflation that was affordable while only humans produced work, since the doer was a usable proxy for its quality. It is no longer affordable. An agent can produce many artifacts of any quality, so judging them by their author is backwards, and judging the author by replaying the artifacts is the only direction that scales. Merit is the warrant a piece of work carries in itself, checkable without reference to who or what produced it. The hypothesis graph is a unit of work that ships with its own evidence; the receipts-first PR is the corresponding practice; the maintainer who merges on the ledger alone is an early instance. The doer earns standing only as the accumulation of work that has survived such checking.

**Legibility.** A benchmark number is legible to readers who will never read a trace, and that reach has value; it is how this work reached an audience. But the number is the artifact an auditor can do least with: it cannot be perturbed, replayed, or used to generate a rival hypothesis. The Verus trail can be: an auditor who suspects the model reached the general predicate by luck can replay the climb, construct a new discriminator off the gate, and attack a node. A benchmark result is an answer; a replayable example is an instrument, and instruments are what an inquiry accumulates.

### What the structure unlocks

A data structure earns its keep by what it unlocks. These ascend in consequence.

*Cheaper checking.* Replaying a node's recorded trial costs far less than reconstructing the reasoning behind it, so the same budget verifies more work. Shown within scope here, not measured as a rate (§(right-regime)).

*Parallel agents, shorter wall-clock.* The graph is monotone: nodes append, kills are idempotent. Parallel agents can therefore latch onto one shared graph lock-free, fan out across rival hypotheses, and re-verify each other's kills instead of trusting them, with transitive accountability (above) as the precondition that makes the fan-out safe. A prose summary must be re-parsed into independent units before anything can be dispatched; the graph ships pre-factored. Named, not yet run (§(future-work)).

*Model-provider independence.* The smem lives in the harness, in plain markdown, behind typed contracts any capable model can read and write. The pair-swap run is the witness: the entire model pair changed and the structure ported wholesale (§(models)). Reasoning that accumulates in a vendor's context window is a liability; reasoning that accumulates in a substrate you own is an asset.

*Accountability.* Every claim ships with its replay.

*Alignment.* Trust displaced by audit: an agent does not need to be trusted to be used.

## Related work {#related-work}

### Construct validity and contamination {#rw-swebench}

The SWE-bench family defines the Verified / Pro lineage, official harness, and contamination-resistant tier design. **SWE-Bench+** (Aleithan et al. 2024) manually audited the original bench: 32.67% solution leakage, 31% weak tests. **OpenAI's February 2026 audit** found a majority of audited Verified tasks have flawed tests and that frontier models reproduce exact gold patches; it stopped reporting Verified and recommends Pro. **Wang, Pradel & Liu** (ICSE 2026) show plausible patches pass tests yet diverge from developer intent; their axis is patches that pass but are wrong, ours (§(right-regime)) is tasks whose materials do not determine which passing behavior is intended. **ORACLE-SWE** ([arXiv:2604.07789](https://arxiv.org/abs/2604.07789)) quantifies the same handover, ablating the oracle and specification signals that leak through a task and measuring the resulting drop; **SLUMP** ([arXiv:2603.17104](https://arxiv.org/abs/2603.17104)) opens on the identical premise, that benchmarks supply the full specification upfront while real coding does not, and answers it by building an underspecified-by-design benchmark. Here we part from both on the verdict: they treat handover as a defect to fix with a better benchmark, while the determinacy audit (§(right-regime)) draws it as a category boundary, a spec-conformance instrument cannot be tuned into a measure of diagnostic inquiry because the two are different types. Evaluation surveys reach the same edge from the methodology side: scoring final outputs misses the in-run reasoning and failure causes, and trajectory-level assessment is the called-for remedy (Yehudai et al. 2025), which is what grading the trace rather than the patch (§(future-work)) would supply. **SWE-rebench** uses post-cutoff filtering as a parallel contamination strategy; **LiveCodeBench** (Jain et al. 2024) is the origin of post-cutoff (temporal-holdout) evaluation, and the standard objection to it applies here too, that training cutoffs are porous because RL post-training and inference-time retrieval can surface later content. The witnessed case (§(verus-bench)) is built against exactly that objection: it is post-cutoff and the solving model's weights predate the fix, so neither porosity nor retrieval supplies the answer. **HAL** (Stroebl et al. 2025) is the third-party cost-aware agent leaderboard and the nearest infrastructural precedent for the cost-transparency stance here; the receipts here go one level finer, to the per-instance re-gradeable verdict. The official **swe-bench/experiments** repo requires `trajs/`, `logs/`, `patch.diff`, `report.json` per submitted instance, the minimum publication norm our provenance contract extends with gate traces, hypothesis graphs, and a cost ledger.

### Agent scaffolds and SE-agent harnesses {#rw-scaffolds}

Surveys and position papers now map the harness's responsibilities directly: the case for *programming with trust*, verification and analysis built into the agent rather than retrofitted after (Roychoudhury et al. 2025), the systematizing of agents for software engineering around verification, testing, and repair (Liu et al. 2024), and the finding that current agents lack the persistent, structured memory long-running work needs (Wang et al. 2025). We answer with the structure none of them name: a Peirce-typed, kill-conditioned hypothesis-graph memory. The SWE-bench-targeted harnesses that exist, OpenHands (Wang et al. 2024), SWE-agent (Yang et al. 2024), and AutoCodeRover (Zhang et al. 2024/25), are ReAct-pattern loops (Yao et al. 2023) without it. **Voyager** (Wang et al. 2023) is the closest loop-shape precedent: embodied observe→hypothesize→test→commit, with a skill library where this work holds falsifiable claims. **SWE-Effi** ([arXiv:2509.09853](https://arxiv.org/abs/2509.09853)) is the sharpest published counter-position: effectiveness emerges from scaffold-model synergy rather than residing in the scaffold alone. Here we agree from the other direction, with the synergy named: on Pro the binding pair is gate × oracle, and neither scaffold typing nor model tier moves the number more than about two points once that pair is in place.

Two concurrent developments arrived independently at adjacent points, each carrying one of the two components composed here. **Theorem-of-Thought** ([Abdaljalil et al. 2025](https://arxiv.org/abs/2506.07106)) types reasoning into abductive, deductive, and inductive specialist agents per query: the typed cycle, without a persistent typed memory across cycles. **Cognitive Memory Manager** ([Khalid & Arora 2026](https://openreview.net/forum?id=yCsHQnvvWY)) extracts a typed-node DAG by observing agent execution and mines it for patterns to promote to skills: the typed graph, mined descriptively where ours is generative (it routes the run). That convergence is independent, not coordinated. Provenance for the framing here is timestamped on the project blog ([The Hypothesis Graph](https://june.kim/the-hypothesis-graph), [Evidence has a trajectory](https://june.kim/evidence-has-a-trajectory)).

Convergence forces a vocabulary question, and we answer it here by pointing rather than claiming. The trichotomy the siblings reach for is Peirce's (1878, 1903). Theorem-of-Thought builds abductive, deductive, and inductive agents while citing no pragmatist anywhere in its reference list (checked against its [v2 source](https://arxiv.org/html/2506.07106v2): forty-four uses of the mode words, zero occurrences of Peirce, pragmatism, James, Dewey, or Ramsey), so the typing in that line of work is used without its source citation. §(grounding) and §(lineage) wire the vocabulary to its sources, and the dated posts above timestamp this lineage's use of the hypothesis-graph primitive. Interop (§(discussion)) will force one wire vocabulary on this design space, and the candidate is already to hand: mode-complete, a century and a half stable, and already carrying the credence semantics the nodes need.

| System | Domain | Reasoning-mode typing | Persistent structure & update | Termination gate |
|--------------|--------|------------------|------------------|---------------|
| Voyager (Wang et al. 2023) | Minecraft | None | Skill library; test-validated graduation | Test-pass on skill |
| IDEA (He et al. 2025) | Interactive rule learning | Peirce-cited, agent-level | Working rule set | None explicit |
| ADI (Gilda & Gilda 2026) | Algebraic invariants | Peirce, layered (L0/L1/L2) | Symbolic knowledge graph | None explicit |
| AriGraph (Anokhin et al. 2024) | TextWorld | None | Knowledge graph (entities, relations, episodes) | None explicit |
| CausaLab (Yang et al. 2026) | Causal discovery | Causal-typed (SCM) | Evolving structural causal model in a DSL | None explicit |
| BeliefMem (Liao et al. 2026) | Partial-observability QA | None | Candidate set; Noisy-OR probabilistic update | Probabilistic threshold |
| Theorem-of-Thought (Abdaljalil et al. 2025) | General reasoning | Abduction / deduction / induction, agent-level (no Peirce cite) | Formal reasoning graph | NLI-guided Bayesian coherence |
| CMM (Khalid & Arora 2026) | SE (coding agents) | 7 trajectory roles, extraction-time | Typed DAG; confidence decay | Human approval + retrieval-validated threshold |
| This work | SE (industrial code) | Peirce, enforced at write time per stage | Hypothesis graph; mechanical kill predicates on the audit verdict | Deterministic finite-state |

*Table 1. Comparison spine for adjacent typed-reasoning and graph-memory LLM-agent systems. Cell terseness is by design; prose nuance in §(typed-memory).*

### Typed reasoning and graph-structured memory {#typed-memory}

**IDEA** (He et al. 2025, ACL Findings, [arXiv:2408.10455](https://arxiv.org/abs/2408.10455)) explicitly cites Peirce and uses the three modes in an interactive rule-learning benchmark. **ADI** (Gilda & Gilda 2026, [arXiv:2604.15727](https://arxiv.org/abs/2604.15727)) gives an explicit Peircean tripartite protocol with epistemic layers over a symbolic knowledge graph; near-simultaneous with this draft and the most conceptually adjacent prior work. Both target reasoning domains outside SE.

The hypothesis graph sits at the intersection of three lineages: cognitive-architecture memory (Soar / ACT-R / EPIC), LLM-agent memory systems (CoALA / AriGraph / Mem0 / Zep), and typed-belief representations (CausaLab / BeliefMem / Theorem-of-Thought / CMM). The hypothesis graph adopts the Soar memory typology directly as its slot vocabulary, adding only the specific content of the `smem` slot: Peirce-typed, kill-conditioned, designed for LLM prose read/write. Adjacent work: **Kirk, Wray & Laird 2023** ([AAAI](https://ojs.aaai.org/index.php/AAAI-SS/article/download/27690/27463/31741)), an LLM-port of the Soar lineage; **CoALA** (Sumers et al. 2023/24, [arXiv:2309.02427](https://arxiv.org/abs/2309.02427)); **AriGraph** (Anokhin et al. 2024/25, [arXiv:2407.04363](https://arxiv.org/abs/2407.04363)), the closest precedent for graph-structured LLM-agent memory; **CausaLab** (Yang et al. 2026, [arXiv:2605.26029](https://arxiv.org/abs/2605.26029)); **BeliefMem** (Liao et al. 2026, [arXiv:2605.05583](https://arxiv.org/abs/2605.05583)), strong adjacent on uncertain alternatives with mechanical update.

**CMM** (Khalid & Arora 2026, [OpenReview](https://openreview.net/pdf?id=yCsHQnvvWY); published one day before this draft) warrants its own comparison. Both systems converge on the same role for memory: a persistent, typed, queryable DAG of reasoning artifacts. The runtimes diverge on agency. CMM is observe-and-consume: an external agent perturbs, CMM types the trajectory post hoc, future runs consume graduated skills. Our loop is perturb-and-falsify: kills fire mechanically during the live inquiry, and the graph routes the run. Same data structure, opposite epistemological direction, and complementary by construction: the ~385 graphs committed in `sweep/repo-hypotheses/` are exactly the corpus CMM's graduation pipeline could consolidate into per-repo skills.

Four 2026 systems each carry one component this work combines; what is new here is the *join*, not any single piece. **FVDebug** ([arXiv:2510.15906](https://arxiv.org/abs/2510.15906)) builds an actual hypothesis graph for debugging, with a frontier and accumulated evidence, but selects the next node by asking the model, the arbiter this work removes. **From Hypotheses to Factors** ([arXiv:2604.26747](https://arxiv.org/abs/2604.26747)) runs the same perturb-and-falsify loop, falsifiable hypotheses behind a deterministic engine over an append-only trace, locked to quantitative finance where this work claims the general semantic-memory substrate. **Portable Agent Memory** ([arXiv:2605.11032](https://arxiv.org/abs/2605.11032)) is the nearest provenance memory, a Merkle-DAG that cites the Soar lineage and makes every node reconstructible by content-addressing, but it certifies *integrity* (the recorded bytes are untampered) where the replay invariant here certifies *warrant* (the node still survives its trial). And the provenance survey **From Agent Traces to Trust** ([arXiv:2606.04990](https://arxiv.org/abs/2606.04990)) enumerates exactly the relations this work mechanizes, Support, Contradict, Invalidate, and names "how provenance quality should be evaluated" as an open problem; the hypothesis graph is one answer, with replay as the quality bar and the kill condition as an executable edge rather than a descriptive label.

What the mechanism experiment (§(right-regime)) adds to this comparison is which piece is decisive: not the graph structure, which several of these share, but where a kill edge gets its ground truth. FVDebug lets the model arbitrate the next step; the contrast that separates a narrow fix from a general one is whether the kill is graded against the model's own belief or against an external oracle, and the externalized form is released as `abductor` (enumerate a case space, calibrate against a known-good reference, gate). A model can rebuild the enumeration for itself but not that oracle (§(enum-calib)), which is the axis these neighbors leave implicit.

A second cluster of neighbors shares this work's epistemological premise, treating truth and uncertainty as first-class rather than a downstream score: **NARS** (Wang's Non-Axiomatic Reasoning System), **OpenCog's AtomSpace and PLN**, **Nanopublications** (Groth et al. 2010), and, closest in time, **Traxia** ([arXiv:2606.08256](https://arxiv.org/abs/2606.08256)), a fourth independent group converging on these primitives two days after [Truth Is Buildable](/truth-is-buildable). Where each stops short of a replayable, kill-conditioned, three-state entitlement ledger is adjudicated in [Verifiable Knowledge](/verifiable-knowledge#related-work), the protocol paper that owns the epistemology; that comparison is not repeated here. What is specific to *this* work is the data structure. These systems are distinct from the cognitive-architecture memory above (Soar, CoALA, AriGraph) in asking what a stored claim *means* rather than how it is stored, and none makes that meaning the **semantic contract of a memory node**, where truth is operationalized by replayable edge structure rather than a stored label or a textual provenance record, and the three states are the entitlement ledger §(epistemics) scopes to a node and its kill edge, not a new logic proposing a third truth value.

> *Production LLM memory systems with graph variants (Zep/Graphiti, Mem0), staged-hypothesis selection in science agents, deterministic gating in adjacent settings, and reflective memory systems (Reflexion, DebugMate) are surveyed in the appendix; they are adjacent on particular axes but do not change the comparison spine.*

### Adversarial filtering and termination {#adversarial-termination}

| System | Domain | Stage operated at | Visibility regime | Cross-family |
|-------------------------|---------|------------|-----------------|----------|
| Multi-Agent Debate (Liang et al. 2023/24, [arXiv:2305.19118](https://arxiv.org/abs/2305.19118)) | General reasoning | Patch / answer stage | Open (cross-visibility) | Single model family |
| Refute-or-Promote (Agarwal 2026, [arXiv:2604.19049](https://arxiv.org/abs/2604.19049)) | Defect discovery | Review stage | Asymmetric context | Yes |
| This work | SE (industrial code) | Pre-patch hypothesis stage | Blind challenge (no cross-visibility) | Yes (Sonnet + GPT-5.5) |

*Table 2. Adversarial multi-model filtering: this work occupies the pre-patch / blind cell. Termination disciplines (λ_A's type-theoretic proofs, SafetyDrift's absorbing states) sit at composition or trajectory scope where this work's verdict-routed gate sits per-instance.*

Closest in spirit is **POPPER** ([arXiv:2502.09858](https://arxiv.org/abs/2502.09858)), which runs agentic sequential hypothesis tests under e-value error control, the same sequential-testing machinery this project's `inquire` workflow uses to classify evidence. POPPER terminates statistically, on an error-rate bound over a population of tests; this work terminates mechanically, on a deterministic kill predicate over a single binary verdict, and persists the outcome as replayable memory where POPPER's tests are ephemeral.

## Limitations {#limitations}

*The mechanism evidence is existence-grade.* One audited divergence, on one instance, in a program that was not preregistered when it ran. The pilots' nulls are confounded by a selection artifact we can name but not yet remove (the triage fast-path, §(null-regime)), and the localization-hard band where the mechanism should live has not been decisively tested; its one strong candidate did not reproduce at HEAD. Nothing here is a rate.

*The audit's two tiers carry different burdens.* The mechanical spine (11.4%) is re-derivable by grep; the two-expert tier rests on a stated standard, adversarially verified (κ = 0.52, all disagreement skeptic-stricter), and 63 screen-flagged candidates are excluded as rater-pending. The proven floor is a floor.

*The bench numbers are public-split numbers.* Pro's public repos predate both model families' cutoffs; the gold-overlap audit bounds frontier reproduce-gold at ~2%, but our holdout is weaker than Scale's (different commits, same repos), and the held-out submission has not been made. The gate's oracle access does not exist on the private split.

*Essence oracles are authored.* The mechanism experiment's graders are written from upstream issue text by the operator's pipeline, mitigated by red-at-base/green-on-gold walls and by the merged fix's external attestation, and reduced but still present.

*The smem is small and per-instance.* Hypothesis graphs in this work are one markdown file per inquiry; cross-instance accumulation is untested. That carries its own deflationary point: the file was never the bottleneck at any repo size, so heavier stores need to earn their keep at cross-instance scale, where the per-instance case never demanded them.

*How to refute this.* The central claims are built to fail loudly, each against a committed artifact a hostile auditor runs rather than a promise.

- **The mechanism claim** dies if the Verus receipt fails to replay, or if a discriminating program shows the externally-oracled fix wrong where the maintainer's general fix is right. The clean, forced-fresh dataset and both patches are committed to check, and the flux trail at `flux-1613-trail-v1` is there for the same test on the auditability case.
- **The encoding-boundary claim**, that the oracle is not self-generable, dies if a self-graded model reaches the hard arm with labels it authored independently of the predicate under test. That would show the oracle is inducible after all, and closing the gate's coverage on that arm is the next experiment's preregistered target.
- **The methodology claim** dies if, as audited cases accumulate, an external oracle stops separating from self-grading everywhere a receipt can see. The oracle's source is then not the active ingredient, and the mechanism README names that null as this thesis's own falsifier.
- **The attribution** dies if the oracle bracket fails to replicate from its preregistered sample.

*Generator staleness.* The checkpoints are fixed (Sonnet 4.5 era), and a more capable generator narrows the band where the mechanism is observable, since it resolves more cases unaided. The mechanism claim therefore survives only in the regime where verification is the bottleneck, which is also the regime the discussion argues matters.

## Future work {#future-work}

The program reorganizes around the smem, in order of leverage.

- **The preregistered mechanism hunt.** The Verus and flux cases define the target band: localization-hard, verification-bottlenecked bugs where the symptom sits far from the cause and the suite cannot see the difference between fixes. Each loop now carries its deductive step before it runs: testing X, predict Y, refuted by Z (`METHODOLOGY-preregistration.md`, `CANDIDATES-localization-hard.md`). Three to five audited existence cases, or the committed null, is the next paper.
- **Coverage as the design lever, the oracle from approved history.** The Verus dissection (§(frontier), §(enum-calib)) names two handles the next experiments turn directly. Gate *coverage* sets the generalization frontier, so widening the enumeration to the genuine-divergence-preserve shape is a falsifiable test of whether the model then carves out the XOR's hard arm. And the oracle a model cannot induce is mined from human-approved history, the merged fix, the regression suite, the resolved-issue label, so calibrating `abductor` differentially against base *and* the approved fix is the concrete way to close a gate's blind spot without authoring a fresh oracle by hand. Prospectively, on a bug with no merged fix yet, the hard arm has no golden until a human spends the judgment.
- **Conjecture: the XOR is the necessary, and necessarily external, operation of inquiry.** Read the dissection one level up. Every warrant-producing step contracts the symmetric difference between what the inquirer believes and what is true, locating one case the current hypothesis mishandles and removing it. Generation cannot find that case, because adding hypotheses has no floor that says *this one is missing*; only a disagreement evaluated against a reference outside the inquirer's belief can, which is why the externalized oracle was the active ingredient. If that is right, the oracle's source is the operation inquiry is made of. The same contraction recurs across the companion posts (refutation in [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true), stranger-replay in [Verifiable Knowledge](/verifiable-knowledge), the fold in [Compress and Unfold](/compress-and-unfold)), which is suggestive rather than evidential and is kept here as a conjecture, not leaned on as a citation. It *dies* if a recorded trace reaches the same held-out general predicate from self-authored labels only, with no external label, replay, human-approved reference, or environmental execution entering before the discriminating step; lucky guesses (no warrant) and already-solved cases (the difference already empty) do not count.
- **Conjecture: in-context abduction degrades with diff size.** Hold the harness fixed and the claim is about the operands: a model's ability to compute the XOR *in its own context* should fall as the diff and case-space grow, the failure mode [Don't Lang What You Can Math](/dont-lang-what-you-can-math) already names, a large structured operation attempted in prose rather than executed. Two regimes, one of them a conjecture. The *endpoint* needs no experiment: once the operands exceed the context window, in-context computation is impossible, so externalization is the only option at scale, and a codebase outgrows any finite window eventually. The *interior*, within the window but large, is the falsifiable part. Computing the XOR is a synthesis task, relating cases to one another to find the one the hypothesis mishandles, so the pairs to weigh grow with the square of the case-space and the load rises quadratically where a fact-lookup rises linearly ([Context Synthesis is Quadratic](/context-synthesis-is-quadratic)); in-context accuracy should degrade as the operands grow, and faster than linearly. The underlying fall-off is the context-rot phenomenon (Chroma 2025); we have no direct measurement of XOR accuracy against diff size, and flag that rather than borrow a result that grades something else. It *dies* if a within-harness sweep over diff and case-space size shows in-context XOR accuracy flat or rising with size. The Verus receipt is a single point on that axis.
- **The hypothesis graph as a type.** Specify the abstract data structure independently of this harness: operations (perturb-and-classify, generate-edge-from-kill, prune, replay), the soundness invariant (every node reconstructible from its recorded trial), and a serialization any agent can emit. The goal is an interchange format for auditable reasoning, so that "show your work" becomes a machine-checkable demand rather than a rhetorical one.
- **Grade the trace, not just the patch.** Bench design follows from the audit: report determinacy-aware denominators; build instruments whose oracle is expensive or absent and whose causes are hidden, because that is where method separates from reach; and score submissions on replayability, so a suite-green over-narrow fix (§(right-regime)) stops being indistinguishable from a root-cause one.
- **Receipts-first contribution as the deployment lane.** The flux submission is the template: fix, discriminating receipt, soundness twin, full suite, replayable graph, residual flagged to the experts. Agent PRs are drowning in justified slop suspicion; the trace is the antidote, because it converts "trust my patch" into "audit my ledger." Scaling that lane (and measuring maintainer response to trace-backed PRs against the 50.6% baseline) tests attestation-displacing-trust ecologically. The first maintainer merge of a trace-backed fix on a maintainer-stuck issue is the lane's golden ticket: an adversarial expert accepting the work on its ledger, with the doer invisible to the verdict.
- **Cross-instance smem accumulation.** Let the graph grow across instances within a repo, then across repos within a domain; the current work tests the smem only at per-instance scope.
- **Concurrent diagnosis over a shared graph.** The monotone graph already permits the lock-free fan-out named in §(discussion): a conflict-free blackboard for the inquiry, layered over git's blackboard for the code. Running it, and measuring the wall-clock win, is the to-do.
- **Held-out submission.** Pro's private split removes the visible oracle, which after §(right-regime) makes it the honest test of the gate-blind harness, well beyond a formality. We expect a substantially lower number there and regard predicting it in print as part of the discipline.

Beyond SWE-bench, the harness is one chapter of a broader program: a compiler from prose to executable agent behavior, of which the methodeutic skills are the procedural memory, the hypothesis graph the typed semantic memory, and the deterministic gate the runtime check. The program is developed at length in the [methodeutics textbook](https://june.kim/reading/methodeutics); *compiler* is used descriptively, in the LLVM (Lattner & Adve 2004) and DSPy (Khattab et al. 2023) lineage of typed pipelines from specification to reproducible behavior.

## Conclusion {#conclusion}

The result is narrow. In the domain where every step is checkable, an agent's reasoning can be made accountable rather than merely trusted. The hypothesis graph is a replayable record that submits each generated step to a world-facing trial and retains only what survives. The path from question to fix becomes a sequence of falsifiable commitments a third party can rerun rather than a verdict it must take on trust. This reduces the cost of relying on an agent from reproducing its work to rerunning its record. The guarantee holds only where the work is perturbable, where a trial can be run and read; extending that region is left open, and the method claims nothing beyond it.

This work is independently funded by the author. Its only standing is the auditable trail: every claim here ties to a committed receipt, the nulls included.

## Availability and reproducibility {#availability}

- **Repositories.** [github.com/kimjune01/swebench-pro](https://github.com/kimjune01/swebench-pro) (the bench run; frozen tags `prereg-pro-v1`, `prereg-pro-v1-cheap`), [github.com/kimjune01/swebench-verified](https://github.com/kimjune01/swebench-verified) (prior-generation baseline, Zenodo-DOI'd), [github.com/kimjune01/swebench-pro-audit](https://github.com/kimjune01/swebench-pro-audit) (the determinacy audit; every claim one row in `CLAIMS.md`, all 728 verdicts in `COVERAGE.md`, mechanical spine re-derivable by grep), [github.com/kimjune01/determinacy](https://github.com/kimjune01/determinacy) (the audit as a portable tool for any SWE-bench-shaped bench; SWE-rebench run included), [github.com/kimjune01/hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism) (the mechanism experiment; the Verus #2219 lift with its clean, forced-fresh dataset and the 43,586-line climb trace, and the flux trail frozen at `flux-1613-trail-v1`; the README's artifact index maps every claim here to its committed path), [github.com/kimjune01/abductor](https://github.com/kimjune01/abductor) (the externalized kill condition as a standalone, domain-general instrument: enumerate, calibrate against a known-good baseline, gate, with the `/debug` skill that drives the loop).
- **Provenance artifacts.** Per-instance trajectories, hypothesis graphs, captured diffs, gate traces, and cost ledger under `runs/scored/artifacts/`; preregistrations at the freeze SHAs; the OSS ledger (`pr-receipts.jsonl`) with the GraphQL query that recomputes every number it asserts.
- **OSS deployment trace.** ~385 hypothesis graphs at [`kimjune01/sweep/repo-hypotheses/`](https://github.com/kimjune01/sweep), one per investigated issue; PR-level outcomes pinned at `kimjune01/kimjune01@paper-2026-05-28`.
- **Replication.** Boxes, budget, the per-instance cost ledger (`COST_BASIS.md`), and the step-by-step rerun live in the run repo and the field guide [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro).
- **Companion writing.** The instrument story and field guide: [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro). The error corrected here, from the inside: [Precisely Wrong](/type-iii-error). The epistemology the discussion rests on: [Verifiable Knowledge](/verifiable-knowledge) and its frame [What Cannot Be False Cannot Be True](/what-cannot-be-false-cannot-be-true); its buildable-truth core in brief: [Truth Is Buildable](/truth-is-buildable). Dated provenance posts establish parallel rather than derivative development: *Theory is load-bearing* (2026-03-17), *The proof manual* (2026-04-05), and *Type the question* (2026-04-08) predate ADI (2026-04-17); *Evidence has a trajectory* (2026-04-27) and *The Hypothesis Graph* (2026-04-28) predate CMM (2026-05-26).
- **PDF.** Arxiv-shape build at [/assets/the-hypothesis-graph-semantic-memory-methodeutics.pdf](/assets/the-hypothesis-graph-semantic-memory-methodeutics.pdf), rebuilt from this markdown source by [md2arxiv](https://github.com/kimjune01/md2arxiv); the source is canonical.
- **DOI.** Prior-generation verified artifact: Zenodo-DOI'd. Mechanism experiment ([hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism)): [10.5281/zenodo.20691973](https://doi.org/10.5281/zenodo.20691973). Pro bundle ([swebench-pro](https://github.com/kimjune01/swebench-pro)): [10.5281/zenodo.20691977](https://doi.org/10.5281/zenodo.20691977). This paper: DOI pending.
- **License.** Skills released under **CC-BY-SA-NS** ([june.kim/cc-by-sa-ns](https://june.kim/cc-by-sa-ns)); repo-level terms in each `LICENSE.md`. The harness an outsider clones is the same harness that produced the published numbers.

**Reproducibility invitation.** *Nullius in verba.* Every number here is recomputable from committed artifacts: the bench verdicts by re-running the official grader on captured diffs, the audit's mechanical spine by grep, the flux divergence by replaying the receipt programs against both committed patches. Doubts should be filed as issues against the relevant repository; confirmed corrections fold into the next versioned artifact, as the retraction noted in §(right-regime) and the reversal this version reports already have.

## LLM collaboration disclosure {-}

LLMs enter this work in three roles. *Subject of study*: the harness under evaluation uses frontier LLMs as generator and challenger, with versions, billing mode, and provenance disclosed in §(models) and the artifacts. *Instrument*: model pairs adversarially verify the audit's two-expert tier (one constructs, an independent family refutes) and blind-judge the mechanism pilots, always with the mechanical layer (grep, grader, replay) holding the verdict. *Writing aid*: the prose was drafted and revised with Anthropic's Claude (Opus 4.8 and Fable 5) from human-authored outlines and session notes; the claims, methodology, numbers, and argument structure are the author's. No LLM decided what to publish.

## Acknowledgments {-}

We thank John Laird for endorsing this submission, and the flux maintainers for engaging with a stranger's receipts on their hardest open issue.

## Novelty and comparative search protocol {.appendix} {#search}

- **Why this section exists.** Several claims here take the form *"we found no prior X."* Such claims are only as honest as the search they rest on. This section publishes the queries so an auditor can re-run the search and either confirm the gap or find what we missed.
- **Sources searched.** Google Scholar; arXiv (cs.LG, cs.AI, cs.CL, cs.SE); ACL Anthology; OpenReview; GitHub code and repository search; public SWE-bench leaderboard and submission archives.
- **Queries by claim.**
  - **Peircean SE-agent loop.** *"Peirce" "LLM agent" abduction deduction induction software engineering*; *"abduction deduction induction" "LLM agent" "software engineering"*; *"Peirce" "SWE-bench" agent*.
  - **Hypothesis-graph agent memory.** *"hypothesis graph" "LLM agent" memory*; *"belief graph" "LLM agent" memory hypothesis*; *"knowledge graph" "LLM agent" "hypothesis" "memory"*.
  - **Blind multi-model hypothesis-stage filtering.** *"multi-agent" "code" "hypothesis" "SWE-bench"*; *"blind" "multi-agent" "code review" LLM*.
  - **Trajectory-shape termination gates.** *"LLM agent" termination criteria trajectory*; *"finite state" "LLM agent" "termination"*.
  - **Benchmark determinacy / construct-validity audits.** *"SWE-bench Pro" "construct validity"*; *"underdetermined" benchmark "problem statement" test*; *"specification" "ambiguity" "SWE-bench" audit*.
  - **Full per-instance provenance on SWE-bench Pro.** *SWE-bench Pro leaderboard submissions trajectories cost ledger*; *site:github.com "swe-bench-pro" "trajs"*.
  - **Sub-$1k Pro replication and per-instance cost ledger.** *"SWE-bench Pro" "cost per instance"*; *"SWE-rebench" cost per problem*.
- **Caveats.** The search is best-effort and bounded by visible-web indexing; private industry work and non-indexed venues are not covered. Discoveries of overlapping prior work should be reported as issues for citation update.

### Comparative search supporting the artifact claim

The artifact claim (§(models)), *no method documented publishes per-instance receipts at this depth on SWE-bench Pro*, requires a comparative search. The claim concerns receipts, with rate set aside. The bar: published per-instance trajectories, captured diffs, gate or evaluator traces, cost ledger, and reproducible run conditions.

**Candidate audit (against the receipt bar).** Each top public submission or comparable report is checked for: published per-instance trajectories (T), captured diffs (D), evaluator/gate traces (G), per-instance cost ledger (C), reproducible frozen artifact (R), and resolve rate at or above ours on the same bench. Receipt-bar columns are *present* (✓), *partial* (~), or *absent* (·).

| Submission / report | Bench | T | D | G | C | R | Rate ≥ ours | Notes |
|--------------------|---------|---|---|---|---|---|----------------|--------------------|
| Official `swebench/experiments` repo (multiple top entries) | Verified | ✓ | ✓ | · | · | ~ | Various | Minimum publication norm: trajs/logs/patch.diff/report. No gate traces, no cost ledger. |
| Top vendor leaderboard entries (Claude Code, OpenHands, SWE-agent, AutoCodeRover) | Verified | ~ | ~ | · | · | · | Reported below 97% | Submissions report numbers; reproducible bundles and cost ledgers rarely published. |
| SWE-bench Pro official page (Scale) | Pro | ~ | ~ | · | · | · | N/A (curator) | Uncapped cost (250-turn limit). No per-instance cost ledger. |
| Nilenso Pro trajectory analysis | Pro | ~ | · | · | ~ | · | N/A (third-party) | Cost/token/time analysis across four frontier models. Not a submission. |
| SWE-rebench public reports | rebench | ~ | ~ | · | ✓ | ~ | Below ours | Strong cost transparency (Cursor Composer 2.5 at \$0.23/problem). |
| **This work: Verified** | Verified | ✓ | ✓ | ✓ | ✓ | ✓ | 426 / 438 eligible (97.3%) | Companion repo `swebench-verified`; Zenodo DOI; gate traces and cost ledger committed. |
| **This work: Pro** | Pro | ✓ | ✓ | ✓ | ✓ | ✓ | 694/728 = 95.3%; open-weight pair 678/728 = 93.1% | Same frozen harness, whole eligible set, 0 incomplete; two model pairs under one bundle. Public-split, gate-oracle regime: an artifact claim, not a leaderboard claim (§(right-regime)). |

**Reading.** No row above the two rows here combines all five receipt-bar columns (T/D/G/C/R) on the same bench. The claim is about receipt depth alone, leaving resolve rate out of it, and survives as long as the table reads this way; a citation showing a fuller combined receipt is the cleanest refutation.

## Extended intellectual lineage {.appendix} {#lineage}

*Foundational sources grounding §(grounding), §(epistemics), §(hygraph), and §(related-work), collected here so Related Work stays focused on contemporary systems.*

### Peircean inquiry and the philosophy of science

- **Peirce 1878** (*Illustrations of the Logic of Science*): the original three-mode taxonomy.
- **Peirce 1903** (*Pragmatism as the Logic of Abduction*): abduction as the only mode that introduces new content.
- **Bacon 1620** (*Novum Organum*); **Popper 1934** (*The Logic of Scientific Discovery*): falsification as the inductive-side constraint.
- **Ramsey 1926** (*Truth and Probability*): operational credence as betting odds; the hypothesis graph's node-level semantics descends from this work.
- **James 1907**; **Dewey 1929**: the pragmatist commitment that truth is inseparable from action.
- **Meehl 1967**; **Feynman 1974** ("Cargo Cult Science"): the difference between rigor-shaped activity and actual rigor, the standard §(right-regime) holds itself to.
- **Kimball 1957; Tukey**: the Type III error, the exact answer to the wrong question; the failure mode the determinacy audit (§(right-regime)) is built to prevent, examined in the companion post [Precisely Wrong](/type-iii-error).

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
