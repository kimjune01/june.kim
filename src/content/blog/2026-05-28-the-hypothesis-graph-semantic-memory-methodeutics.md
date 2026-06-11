---
variant: post-paper
autonumber: true
title: "The Hypothesis Graph: Semantic Memory Written by Methodeutics"
subtitle: "Merit attaches to the work, not the doer."
tags: methodology, epistemology, coding
keywords: hypothesis graph, methodeutics, abductive inference, agent memory, cognitive architectures, LLM agents, provenance, auditability, falsifiability, machine epistemics, post-cutoff evaluation
---

*[Download PDF](/assets/methodeutic-harness-paper.pdf) · arxiv-shape preprint, rebuilt from this source. · Receipts: [the bench run](https://github.com/kimjune01/swebench-pro) · [the determinacy audit](https://github.com/kimjune01/swebench-pro-audit) · [the mechanism experiment](https://github.com/kimjune01/hygraph-mechanism), each reproducible from its own committed artifacts.*

## Abstract {-}

On one undiagnosed, uncontaminated open-source bug, a language-model agent built a sound, general fix, verified on a clean build, with every reasoning step recorded and replayable. The bug is post-cutoff data: discovery through reason, not recall. The warrant is the inquiry's provenance, not the model's word for it. That is what Sutton's challenge asks. The instrument is the **hypothesis graph**: a typed, persistent semantic memory whose nodes are falsifiable hypotheses bound to trials and whose edges are kill conditions that fire on evidence. It is written by **methodeutics**, Peirce's abduction, deduction, and induction run as a mechanical pipeline with a deterministic gate no model arbitrates, on epistemic grounds inherited from the pragmatists. The graph turns a machine's answer into an auditable trail a hostile reader replays instead of a verdict they must trust. One object answers across the questions it touches, agent memory, provenance, and the epistemics of machine reasoning: the hypothesis graph as the unit of accountable agent reasoning, where merit attaches to the work instead of the ephemeral agent.

## Introduction {#introduction}

> We want AI agents that can discover like we can, not which contain what we have discovered.
>
> — Richard S. Sutton, [*The Bitter Lesson*](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) (2019)

In 2026, reasoning is the capability frontier for large language models, and coding is where it is tested most sharply: a patch passes or it does not. Three pains run underneath the progress, and the applied-AI literature is converging on them at once. Agent work keeps rebuilding memory from scratch: even where it reaches for the cognitive-architecture lineage, as CoALA (Sumers et al. 2024) does in mapping language-agent memory onto Soar (Laird 1987) and ACT-R, it leaves the semantic slot a place to store facts rather than a structure that can be falsified. Verification is in crisis: fluent generation yields confident, unfalsifiable output, source-authority is failing as a trust signal, and a recent DeepMind position paper calls for "robust falsifiability pipelines" by name (Marchal et al. 2026). And discovery has no operational test: a model's unaided output gives no way to separate a genuine discovery from recombined recall, which is the challenge the epigraph sets.

This paper is about where an agent's reasoning should live so that it can be checked, and none of those traditions built the missing piece: a place to hold a hypothesis *under consideration*. Prose context is lossy, skill libraries store verified code rather than falsifiable claims, and vector retrieval indexes established chunks. Cognitive architecture defined the typed memory slots but, for want of a general inference engine at the core, stayed a research program; LLM-agent work has the inference engine and keeps filling the semantic slot with facts. The gap between them is hypothesis-shaped.

The hypothesis graph fits it. It is a typed semantic memory of an inquiry in progress: candidate causes as nodes, falsification conditions as edges, every belief carrying the mode that earned it and the trial that can re-earn it. It is a data structure at the harness layer, just a markdown file: no RAG, no database, zero dependencies (§(hygraph)). It fills the semantic-memory slot (`smem`); the methodeutic skills fill procedural memory (`pmem`); the per-run trajectories fill episodic memory (`epmem`); the model plugs in as the inference component, a reasoner inside a method it does not own. The model does the reasoning, as it always did. The structure holds that reasoning, types it, and keeps it replayable after the context window that produced it is gone.

The contribution is one level down from the answer: a machine producing a fix and, with it, an **attested chain of mechanical reasoning** to reach it, each step a node bound to a recorded trial, each belief typed by the mode that earned it, the whole chain a thing a stranger replays rather than a verdict they are asked to trust. On a problem the model has never seen, that chain terminates in a fix that did not exist until the inquiry built it. The sharpest evidence is a single such case (§(right-regime)): an open, maintainer-stuck compiler bug, post-cutoff and so impossible to recall, where the graph's fix generalizes and a strong minimal agent's does not, a difference invisible to every test the project ships and settled by a receipt any reader can rerun. Discovery, not recall, witnessed and replayable.

So the paper claims four things:

1. **A data structure**: the hypothesis graph and the methodeutic skills that write it, filling the semantic-memory slot of a cognitive architecture for coding agents (§(hygraph), §(application)).
2. **A mechanism finding**: in the regime that matters (undiagnosed, uncontaminated, no cheap oracle), the hygraph produces a fix absent from the reachable corpus, a witnessed instance of reasoning beyond documented corpus recall. The claim is existence-grade and nothing more: not that the method reliably discovers or routinely beats strong agents, but that one case exists whose public trace warrants the word where no benchmark verdict could (§(right-regime)).
3. **An epistemic reframe** this lineage was always pointing at: agents should not be trusted, they should be accountable, and the hygraph is the ledger that makes them so (§(discussion)).
4. **A performance record and a benchmark gap**: how the assembly does on the field's standard benchmark, and why no benchmark can grade what it does. The work is diagnostic, and as scope grows so does ambiguity, until the task outgrows the clean oracle a benchmark needs; no bench we know of stays both diagnostic and verifiable (§(results), §(attribution), §(audit)).

The paper works at two levels. The systems contribution is the instrument; the epistemology is what the instrument makes possible: a position on what makes a claim checkable, what agents owe the people who act on their outputs, and where merit attaches. The instrument is concrete; the epistemological claim is primary; the paper is built so the latter survives exactly where the benchmark result nulls.

This work is unincentivized public research. Its only standing is the auditable trail: every claim above ties to a committed receipt, the nulls included.

## The hypothesis graph {#hygraph}

The motivation is a set of constraints the data structure must satisfy at once. The semantic-memory slot stayed empty for decades because they pull against each other, and no single structure met them together:

- **Hold the unproven.** Store hypotheses still under test, not only verified facts, the one thing prose, skill libraries, and retrieval all drop.
- **Search and justify in one object.** Record how an answer was found and stand as the proof that it holds, two jobs usually split between a search tree and a proof tree.
- **Open vocabulary, machine-checkable.** Accept causes proposed in the domain's own words, yet bind each to an executable trial a machine can rerun.
- **Outlive the window, replay without the author.** Survive the context that produced it and stay reconstructible by a stranger who does not trust whoever wrote it.
- **Self-extend with no controller.** Let a dead hypothesis name the next one, so the structure grows itself with nothing external deciding where to look.
- **Low-cost.** No database, no index: a file the harness owns, so every inquiry keeps one.

The component that can finally satisfy them together is the LLM. Filling the graph takes a reasoner that reads a surprising failure, proposes candidate causes in open vocabulary, and turns each into an executable test, with no hand-built domain model. Classical inference engines could do this only inside a formalism encoded by hand, which is why the slot stayed a research program; the LLM is the first general reasoner that populates it across arbitrary codebases. As far as we know, this is the first time the slot is filled by a general inference engine rather than a domain encoding.

The structure meets all six with three pieces, a node, an edge, and one invariant. A **node** is a claim bound to a trial: a hypothesis, the perturbation that tests it stated as an exact command, the observed outcome, and a credence typed by the reasoning mode that established it. An **edge** is generated by a kill condition: the manner of a hypothesis's death names the next hypothesis, so the structure is self-extending, with no external controller deciding where to look. The **soundness invariant** is replayability: every node must be reconstructible from its recorded trial by someone who does not trust the author. As a data structure it exposes a small, CRUD-like set of operations:

- **Create**, append a node: abduction writes a hypothesis with its kill condition and the trial that will test it. Nodes append; nothing is overwritten.
- **Read**, query and replay: ask which hypotheses are still open, and reconstruct any node from its recorded trial without trusting the author. Replay is the load-bearing one.
- **Update**, classify: a trial's outcome marks its node killed or witnessed and caps its credence at the mode that earned it, a verdict written once.
- **Link**, generate-edge-from-kill: the manner of a hypothesis's death names the next hypothesis, so an update spawns the next node and the structure extends itself.
- **Delete**, prune: dead branches leave the working frontier, while their record stays replayable.

<figure>
  <img src="/assets/hypothesis-graph-anatomy.svg" alt="A hypothesis graph as a two-node linked list, on the dead-light inquiry. The first node, an abduction (the bulb is dead), records its trial (swap in a fresh bulb), its outcome (still dark), and a credence of 50 percent capped by its mode; it is killed. An edge generated by that kill (generate-edge-from-kill) names the next node. The second node, an induction (the dimmer switch is broken), records its trial (bypass the dimmer to the wall), its outcome (the light comes on), and a credence of 96 percent that is test-backed; it is witnessed. The footer states the replay invariant: every node rebuilds from its recorded trial, by a reader who need not trust the author." style="max-width:600px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> A hypothesis graph, two nodes and the edge between them, on the dead-light inquiry. The bulb hypothesis is killed by a cheap trial (swap in a fresh bulb, still dark); its death names the next node, the dimmer, which a second trial witnesses (bypass it to the wall, the light comes on). Each node binds a hypothesis to a trial, an observed outcome, and a credence capped by the mode that earned it: abduction proposes and stays low, induction is test-backed and rises. Every node rebuilds from its recorded trial, so a reader replays the structure instead of trusting it.</figcaption>
</figure>

The nodes are ordinary; what is novel is the edge semantics. A search tree finds; a proof tree justifies. The hygraph is both at once, because the search path *is* the justification: every step was a trial. It sits at the confluence of three older lineages: truth-maintenance systems (de Kleer 1986), sequential experimental design (Wald 1947; Vovk & Wang 2021), and abstract argumentation (Dung 1995). The pair none of them combine is kills that generate the next experiment and replayability as a first-class invariant (§(lineage)).

The scope must be stated honestly or the claim dissolves. This is the data structure for *testable* inquiry, and its entire power is the perturbation surface. Strip the ability to poke the system and read an outcome, and the same shape degrades into a plausibility tree, which is the confabulation failure mode it exists to prevent. It is also not how minds run. Minds run on simulation, fast and compressive and intuitive, but a simulation is not verifiable from outside, so inquiry that has to be checked trades it for an explicit perturbation surface. The hygraph is the verifiable serialization reasoning compiles to, so it can be checked by someone who does not trust you. Proof is to intuition as the hygraph is to inquiry: not the thinking, the residue of the thinking that survives a stranger's replay.

In the memory typology, this is the `smem`: persistent, typed, queryable, and owned by the harness rather than the model. Those same properties make it an interface for agent interop: because the structure is typed and external, a second agent, a later run, or a human auditor reads and writes against one contract and can rerun any node rather than trust it (§(discussion)). The graph in this work is one markdown file per inquiry. It was never the bottleneck at any repo size in the eligible set, a deflationary point against the field's reflex to reach for vector stores and graph databases where none is needed (§(limitations)).

## Theoretical grounding: methodeutics {#grounding}

The procedure that writes the hygraph is encoded method, living in the harness rather than the weights. Unlike tool calls in a loop, it separates the modes that earn a belief. Peirce named them before any of us were born.

His *Illustrations of the Logic of Science* (1878) and *Pragmatism as the Logic of Abduction* (1903) type the operations of inquiry into three modes that are not interchangeable.

- **Abduction** generates explanatory hypotheses for surprising observations: *what would, if true, make this no longer surprising?*
- **Deduction** derives testable predictions from hypotheses: *if this hypothesis holds, what follows?*
- **Induction** tests predictions against evidence: *does the evidence accord with the prediction?*

<figure>
  <img src="/assets/modes-of-reason-triangle-light.svg" alt="Triangle of the three Peircean modes: Observation to Theory (abduction), Theory to Experiment (deduction), Experiment to Observation (induction). Three modes, three edges, one self-correcting cycle." style="max-width:528px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> The three modes as one cycle: Observation → Theory (abduction), Theory → Experiment (deduction), Experiment → Observation (induction). <code>inquire</code> traverses all three before any code is written; a partial traversal is a partial inquiry.</figcaption>
</figure>

No single mode carries a belief to its grade. Abduction proposes content but does not test it; induction tests but introduces no new explanatory content; deduction traces consequences but invents nothing. The credence a node ends up with is what traversing all three earns it, and that is what it means to call the modes typed: each is fixed by what it can't do. Keep them separate and each does its one job; collapse them and you get familiar failure modes:

- **Confirmation bias**: induction without abductive alternatives
- **Confabulation**: abduction without inductive grounding
- **Free-association**: no typed mode at all

That collapse is exactly what modern LLM agents do by default, since a single forward pass proposes, predicts, evaluates, and rationalizes in undifferentiated prose. Methodeutics, Peirce's term for the methodology of inquiry, is how to conduct the typed-mode loop well. Encoded as skills, it is the `pmem` of this architecture: the procedural memory whose job is to construct and maintain the `smem`.

*Modes of reason and the irreducible three.* The three modes come from Peirce (1878, 1903). Around the act of testing, philosophy of science built an apparatus of real rigor: Bacon's induction (1620), Popper's falsifiability (1934), Meehl's "soft science" critique (1967), Pearl's causal calculus (2009). Justification got its method, every step of it. But it begins one step too late, taking the hypothesis as given and filing its origin under inspiration. The discipline built an epistemology of justification and none of discovery. Peirce alone named the operation, abduction, and was ignored. The harness runs it as a first-class typed mode.

*Pragmatist credence.* Ramsey 1926 (*Truth and Probability*; subjective probability, the Dutch Book argument, belief as betting odds); James 1907 (*Pragmatism*; truth as what works); Dewey 1929 (*The Quest for Certainty*; truth as warranted assertibility). The node-level semantics of the hygraph descends from this lineage.

Put the two together, Peirce's modes as the operations and the pragmatists' credence as what a node believes and how strongly. In a precise and limited sense, the harness then encodes what it means to reason: not a theory of mind, but a mechanical discipline of inquiry standing on the epistemic grounds this lineage built. That is the claim the rest of the paper tests, and the ground it is tested on.

## Methodeutics, applied {#application}

Abduction completes the trichotomy as an idea. Putting it to work is another matter. How do you generate a hypothesis, and where do you hold it? A diff, in a typed graph.

*Bi-abduction, tri-abduction, and compositional inference.* The primitive under abduction is a diff: a before snapshot, an after snapshot, the flip as figure and what held as ground, Rubin's Gestalt terms. Arity grows from there, from unary (one before/after pair, one frame, the ground held fixed) to bi-abduction (the frame inferred autonomously: Calcagno et al. 2009, O'Hearn 2019, scaled industrially in Facebook Infer) to tri-abduction (a diff across branches: Zilberstein et al. 2024, [*Outcome Separation Logic*](https://arxiv.org/abs/2305.04842)). `inquire` worked at the unary-to-bi level, a single before/after diff with the frame inferred from the symptom.

<figure>
  <img src="/assets/bi-abduction-dimmer.svg" alt="Bi-abduction as a diff: a dead light with three intact suspects (dimmer, fixture, bulb), the cause invisible. Bypassing the dimmer straight to the wall restores the light, so the XOR isolates the dimmer as the figure (the fault) and exonerates fixture and bulb as the ground (the frame)." style="max-width:720px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> An example of bi-abduction. The symptom is a light fixture unresponsive to switch input, and it underdetermines its cause: dimmer, fixture, and bulb are all intact, so the static scene names no suspect. The perturbation manufactures the second snapshot, bypassing the dimmer to the wall, and the XOR isolates the figure (the dimmer) from the ground (fixture and bulb). Generating that diff is the abductive act; induction follows, convicting the dimmer once the light returns.</figcaption>
</figure>

*Directed graphs as reasoning representation.* Pearl 1988 (*Probabilistic Reasoning in Intelligent Systems*; Bayesian networks as DAGs of dependencies); Pearl 2000/2009 (*Causality*; structural causal models, d-separation, do-calculus). Our data structure (typed nodes, directed edges) applies Pearl's lineage to hypothesis representation rather than causal-structure inference.

<figure>
  <img src="/assets/hypothesis-graph-fixture.svg" alt="A hypothesis graph for the dead-fixture inquiry. The observation (light won't turn on) fans by abduction into four typed hypothesis nodes: no electricity from socket, dimmer switch broken, fixture dysfunctional, bulb expired. Three are killed by mechanical predicates (outlets live, lights on wall, lights elsewhere); the dimmer node is witnessed (bypass works) and closes as induction at 96 percent." style="max-width:720px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> The hypothesis graph for the dead fixture. Abduction fans the observation into four typed candidate nodes; mechanical kill predicates fire on three (the socket, fixture, and bulb each cleared by a cheap test), the dimmer node is witnessed by the bypass and closes the last open hypothesis, and deduction derives the fix. Typed nodes, directed edges, all three modes in one inquiry.</figcaption>
</figure>

Isn't this just debugging? Yes, precisely. It has simply never been typed into a data structure inside an inference engine. Every engineer runs this loop, abduce a cause, kill it on evidence, witness the survivor, derive the fix; but in their head, the modes collapsing into one undifferentiated pass. The harness gives the loop a typed substrate, the hygraph, and a deterministic engine to run it, so a model executes the inquiry and a stranger can replay it.

*Composition over the hypothesis graph.* Three lineages enter through separate roles. The **structural skeleton** is Pearl's DAG: typed nodes, directed edges, the probabilistic semantics left behind. The **node semantics** is credence (Ramsey 1926; James 1907; Dewey 1929): each node carries a belief at a credence level, capped by its reasoning mode, continuous rather than boolean. Confident confabulation, high confidence on a node that hasn't earned it, is the failure mode the stage-typing and kill conditions jointly prevent. The **update semantics** is the binary test verdict, written back to the active hypotheses as a kill or witness, together with a re-entry route the driver follows (§(gating)). Pearl's skeleton, Ramsey's credence, a deterministic verdict→route update: three primitives, three roles, one data structure.

## The harness {#method}

<figure>
  <img src="/assets/inquire-skill.svg" alt="The inquire skill. An observation, a surprising fact or failure trace, enters the methodeutic loop. Abduction proposes typed hypotheses, each with a kill condition (what would, if true, make this no longer surprising). Deduction derives a falsifiable prediction, the exact trial each hypothesis must survive. Induction runs that trial against the world: a refutation fires the kill, a confirmation marks the node witnessed, and the predicate is deterministic with no model arbitrating it. Each mode writes typed nodes into the hypothesis graph (smem), each node typed by the mode that set it and capped at that mode's credence, and the loop re-enters abduction with the updated graph until one node is witnessed and deduction derives the fix. The skill is named for Peirce's inquiry, the engine of discovery, not mere investigation." style="max-width:720px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> The <code>inquire</code> skill: Peirce's three modes as a procedure (<code>pmem</code>) that writes the hypothesis graph (<code>smem</code>). Abduction proposes hypotheses with kill conditions, deduction derives the trial each must survive, induction runs it and fires a deterministic kill or witness with no model arbitrating. Each node is typed by the mode that set it, the credence cap travels with the type, and the loop re-enters with the updated graph until a node is witnessed. <code>implement</code> and <code>attest</code>, which read the survivors and verify the patch, follow below.</figcaption>
</figure>

Throughout, the three stages are `inquire`, `implement`, and `attest`; the frozen artifact's code, file paths, and route literals spell them `recon`, `craft`, and `audit`.

### The inquiry frame {#inquiry-frame}

We recast each issue as an inquiry on an engineered system: a failure trace, a codebase, a root cause to find, and an intervention that must not regress the rest of the system. Code is the right substrate for the hygraph because it combines three properties that other inquiry domains rarely combine:

- **Reproducible**: same input yields same output, modulo controlled nondeterminism
- **Deterministic**: causal lines from input to behavior are mechanical
- **Perturbable**: single-line and single-function diffs are cheap to apply and fully observable

Because those three hold together, hypotheses about code can be tested by cheap mechanical perturbations and falsified by deterministic predicates; kill conditions are not approximations; they are executions.

One trial settles the predicate in this regime. In code the per-case response is mechanically observable, so a single passing test on a captured diff is a complete verdict that the diff satisfies the executable predicate for that case. That verdict speaks to the predicate alone: behaviors it doesn't cover are out of scope, a boundary that §(right-regime) shows is exactly where the differences live. Where such verdicts are aggregated, the right summary is counts and denominators rather than confidence intervals: per-case verdicts are exact, and aggregating them is bookkeeping.

The three Peircean modes are how `inquire` builds the graph, each node typed by the mode that established it and capped at that mode's confidence:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:7em"><col><col style="width:6.5em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Mode</th><th style="background:#f0f0f0">What <code>inquire</code> does</th><th style="background:#f0f0f0">Confidence</th></tr></thead>
<tr><td><strong>Abduction</strong></td><td>Proposes candidate root causes from the observed failure; writes hypothesis nodes with falsifiable predicates and kill conditions (read-only)</td><td>low</td></tr>
<tr><td><strong>Deduction</strong></td><td>Traces each hypothesis's consequences through the code to localize the suspect set</td><td>high</td></tr>
<tr><td><strong>Induction</strong></td><td>Tests survivors with cheap read-only experiments (prints, intermediate data)</td><td>moderate</td></tr>
</table>

`implement` then writes the surviving hypothesis, with an adversarial challenger critiquing the diff against the spec. `attest` runs the test suite, takes the grader's pass/fail verdict, and emits a re-entry route (`inquire`, `implement`, or `none`) from a fixed verdict→route table. The driver parses the verdict and the route; both are mechanical, and no model decides termination.

### Hypothesis graph as inquiry output {#recon-output}

`inquire` emits the hygraph: the structured-analysis document that precedes the patch. Kill conditions are mechanical predicates over the evidence trajectory, not model preferences, so a node dies when its predicate fires and not before. The graph persists across iterations; re-entry adds nodes rather than overwriting. The frontier closes only when every open hypothesis is killed (a test refutes it) or witnessed (a test confirms it).

A committed node is a conclusion, and an inquiry that reaches one rarely runs straight. Following the `inquire` skill on a real bug, a single hypothesis flips across all three modes and a kill before it settles:

<figure>
  <div style="display:flex; flex-wrap:wrap; align-items:center; gap:5px; font-size:12px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; margin:0.6em 0; line-height:2;">
    <span style="padding:2px 8px; border-radius:10px; background:#fef3c7; color:#b45309;">abduction</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#dbeafe; color:#1d4ed8;">deduction</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#fee2e2; color:#dc2626; text-decoration:line-through;">kill</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#fef3c7; color:#b45309;">abduction</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#dbeafe; color:#1d4ed8;">deduction</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#dcfce7; color:#15803d;">induction</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#dbeafe; color:#1d4ed8;">deduction</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#dcfce7; color:#15803d;">induction</span><span style="color:#cbd5e1;">→</span>
    <span style="padding:2px 8px; border-radius:10px; background:#dbeafe; color:#1d4ed8;">deduction</span>
    <span style="color:#94a3b8; font-weight:600;">⇒</span>
    <span style="padding:2px 8px; border-radius:10px; background:#1d4ed8; color:#fff;">induction · 93%</span>
  </div>
  <figcaption><strong>Figure.</strong> An in-flight inquiry trace, illustrative: Sonnet 4.5 following the <code>inquire</code> skill on the <code>python-dotenv</code> <code>find_dotenv</code> v1.0.1 regression (a real, reproducible bug, every command run). The active hypothesis cycles through all three modes and a kill before the inquiry settles; a committed graph records only the terminal node (<code>induction · 93%</code>), not this sequence. Full trace: <a href="/assets/recon-inflight-dotenv.md">recon-inflight-dotenv.md</a>. Not a frozen Pro instance.</figcaption>
</figure>

### Blind cross-model challenge at the hypothesis stage {#blind-blind}

Two frontier models from different families receive the same evidence pack with no cross-visibility, and each produces a hypothesis independently. A third pass extracts the disagreements, not the agreements: the disagreement becomes the next node in the graph; the agreement is recorded but not actionable. Adversarial filtering operates at hypothesis time, while the worktree is still untouched, rather than at patch time where the diff is already written. Sampling stochasticity alone produces real divergence even within a single model; cross-family divergence compounds it with architectural and training-corpus differences. Both are signal.

### Deterministic gating and the outer loop {#gating}

The control loop is standard. `attest` prints a verdict and a re-entry route from a fixed table; the driver routes on those two lines with no model in the decision and under a bounded attempt budget; a failure re-enters `inquire` with the updated graph rather than retrying the patch, so the hygraph doubles as the loop's checkpoint and no dead branch is re-proposed. The gate's reliance on a cheap test oracle is not incidental: §(attribution) shows it does most of the work the bench number seems to credit to diagnosis.



## Procedure {#setup}

The right place to measure the hygraph is where a benchmark cannot reach: an undiagnosed bug with no cheap oracle and a genuinely hidden cause. That regime is not a corner case, it is most of software. Every issue tracker is a backlog of undiagnosed problems waiting on the one expensive step a benchmark never exercises; flux #1613 sat for weeks at 41 comments with its maintainers stuck, which is what undiagnosed looks like in the wild. The mechanism experiment ([github.com/kimjune01/hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism)) reconstructs that regime under control and runs the ablation a benchmark cannot: same model, same loop, the methodology the only variable, an existence-proof burden rather than a population rate.

**Two arms, one variable.** Each bug is solved twice on the same model. The minimal arm is an adapted mini-SWE-agent, the industry-recognized minimal scaffold, running its verbatim prompts with no diagnosis artifact. The graph arm adds the methodeutic `inquire` stage and hands `implement` the resulting hypothesis graph. Nothing else differs, so any gap is the methodology's.

**The oracle is the issue's essence, not the PR's test.** Grading uses an essence oracle authored from the upstream issue text and graded red-at-base / green-on-gold, never the merged PR's shipped test (which the pipeline would have written for itself, re-creating the bench's over-credit) and never a self-authored check (self-audit went 4/4 false-green against the real grader in prior work). Both arms see a pass/fail run-handle, never the assertion bodies, so neither can pattern-match the test.

**Contamination control.** The graph is the treatment, so its contamination does not cancel in the differential the way the shared solve-model's does. The graph is therefore regenerated blind by a model whose training cutoff predates the fix (Opus 4.7, a January 2026 cutoff against May 2026 fixes), so the diagnosis cannot be recall.

**The hunt and its preregistration.** Candidates were drawn first from the deployment pipeline's merged-PR pool, then beyond it to open, pipeline-skipped bugs, with blind-graph size as a cheap leading indicator of diagnostic depth. The existence bar is strict: the minimal arm must fail the essence oracle where the graph arm passes, on a bug with real diagnostic branching. One procedural lesson the experiment applied to itself: the first loops ran as inductions with no per-loop deductive rung, so each null fed a fresh abduction instead of testing a stated prediction. The protocol now preregisters one sentence per loop, testing X, predict Y, refuted by Z, before any arm runs (`METHODOLOGY-preregistration.md`).

## Results {#right-regime}

Nine pilots ran under this protocol: eight nulls and one divergence. The score is honest and uncomfortable in both directions.

**Eight nulls.** On bugs from the merged-PR pool and beyond it, the minimal baseline kept succeeding: a 5-line CLI fix in 91 seconds (qrtool #695), the deepest graph in the pool out-reasoned in two minutes (slang-server #310), a real clear()/ingestion data race in an LSM storage engine the pipeline had skipped as too complex (fjall #287), a decoration-leak the minimal agent localized unaided (bat #3710). Two findings explain the nulls without excusing them. First, a **selection artifact**: the deployment pipeline's own triage skill scores reproducibility up and fast-paths easy bugs around the graph (its rule, verbatim: "a 1-line fix with a confirmed reproducer doesn't need a hypothesis graph"), so the merged pool is precisely the subset where the pipeline says the graph is unneeded. Second, **baseline reach**: a frontier model in a minimal loop now diagnoses and fixes most reproducible bugs unaided, so the band where diagnostic structure changes a pass/fail verdict is eaten from below by model capability and routed around from above by triage. The deployment merge rate inherits this: the 81 merged PRs (§(bench)) were never graph-dependent, a minimal prompt digs the few levels most of them need.

**One audited divergence.** flux-rs/flux #1613, an open, maintainer-stuck composite-sort bug in a refinement type checker, 41 comments, no fix. Both arms produced patches that verify the reported program and pass the full 965-test compiletest suite with zero failures; by every test the project ships, both fixes are done. They are not the same fix. The minimal arm gated its repair on a shape coincidence (an ADT carrying a function-sort field), incidental to validity. The graph arm dumped the solver constraints, located the live obligation (a `FoldLocal` equality at the setter call site), and repaired the cause: track the field origin of a mutable borrow and write the callee's post-state back to the borrowed place. A receipt discriminates where the suite cannot: a structurally identical valid program with integer components instead of a function component. The graph arm's fix verifies it; the minimal arm's fix rejects it with the original error. Both correctly reject an unsound twin, so the minimal fix is not broken; it is over-narrow, a confident false positive the project's own tests can never catch. The divergence reproduces across model families: rerun with Sonnet 4.5 in both arms against the same oracle, the split is identical, one bug now witnessed on two independent models. The Sonnet minimal arm is worse still, over-narrow like the first but also unsound, accepting an invalid program that every other arm, including its own graph counterpart, rejects. The advantage tracks the methodology, not the model. The graph ran 19 nodes, recorded three of its own corrections in-trail (a stale-binary catch, a first fix it refuted with its own probe, an over-broad propagation the suite caught), and every load-bearing node was replayed on a pristine base build before any of this was claimed. The hardened fix is in front of the flux maintainers with the residual honestly flagged, and the full trail is public at tag `flux-1613-trail-v1`. A maintainer merge would close the case with the same certification this experiment treats as gold everywhere else: the merge is the attestation. Until it lands, the case stands on the replayed receipts alone, and the hunt for further cases continues under the preregistered protocol.

<figure>
  <img src="/assets/flux-1613-two-arm.svg" alt="The flux #1613 divergence. The same model in the same loop, methodology the only variable, splits into two arms. The graph arm dumped the solver constraints, located the live obligation (a FoldLocal equality at the setter call site), and repaired the cause; the minimal arm gated its repair on a shape coincidence (an ADT carrying a function-sort field), incidental to validity. Both fixes pass the full 965-test compiletest suite and the reported program, so by every test the project ships both are done. The receipt discriminates off-suite: on a soundness twin (integer components, structurally identical and valid) the graph fix verifies it and the minimal fix rejects it with the original error; both reject an unsound twin, so the minimal fix is not broken, it is over-narrow, a confident false positive the suite can never catch. The advantage is invisible to the oracle, settled only by a receipt; the public trail is flux-1613-trail-v1, 19 nodes with three self-corrections, every load-bearing node replayed on a pristine base build." style="max-width:760px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> The flux #1613 divergence. Same model, same loop, methodology the only variable. Both fixes pass everything the project ships; they part only at an off-suite receipt, where the graph arm's cause-level repair verifies a structurally identical valid program and the minimal arm's shape-coincidence fix rejects it. The minimal fix is not broken, it is over-narrow, a confident false positive no shipped test can catch. The advantage is correctness invisible to the oracle, settled by a receipt any reader reruns.</figcaption>
</figure>

### What the existence proof establishes

An existence proof needs one witness, and flux #1613 is it: there exists a real, maintainer-stuck bug on which the methodology produced a materially better, still-sound fix than a strong minimal agent on the same model, with reasoning auditable at arbitrary depth. No rate is claimed; the claim does not need one. What the cross-model replication adds is attribution, not frequency: the same contrast on a second model family puts the difference on the methodology rather than any one model's quirks, one instance witnessed twice. And here recall is impossible: the bug is post-cutoff data. For the controlled run the graph was regenerated blind by a model that also predates the fix, and the resolution was absent from the reachable corpus when the weights were frozen. The witness then carries a stronger reading than a better patch: discovery through reason, the fix built rather than recalled, assembled one verified step at a time from world-facing trials. That is the discharge of the epigraph's challenge that agents discover rather than carry forward what we have already discovered. It survives the only test that matters for a discovery claim, replay: every load-bearing node re-runs on a pristine base build, so a stranger reconstructs the act instead of trusting the report. Reproducibility here is the example's property, not the bench's, and that is what lets one witness carry the weight a rate used to. What the witness fixes is the shape of the mechanism's value: the advantage did not appear as pass-versus-fail on the original bug; it appeared as correctness invisible to the oracle, settled only by a receipt.

## The bench, bounded {#bench}

The assembly was also run on SWE-bench Pro, and resolved 95.3% of the public split under the official grader. That number is not a property of the harness or the method. It is a property of oracle availability: on the public split the failing tests are visible, the gate iterates against them, and any competent coding agent handed that signal reaches the mid-nineties. The oracle bracket prices it exactly (§(oracle-bracket)). Leading with this number was a mistake; correcting it is why the bench is cornered here, after the result that bears on the method. Every choice follows one goal: making the run attributable, so a skeptic can pin the result on the harness or rule it out. The disciplines live as receipts in the repository rather than as prose here: preregistration and an annotated freeze tag (`PREREGISTRATION.md`), eligibility against documented bench defects (`KNOWN_BAD.md`), official-grader-only verdicts, infrastructure fault classes predeclared with invariants so recovery cannot become a re-roll lever, per-instance provenance (trajectory, hypothesis graph, captured diff, gate trace, cost ledger), and a doubt-by-doubt guide for hostile readers (`FOR_SKEPTICS.md`, `OBJECTIONS.md`). The operational story, including everything that went wrong on the way to an honest number, is the companion field guide [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro).

### Models and the oracle boundary {#models}

No training, no fine-tuning, no learned weights in the harness. Each stage invokes a vendor's shipped agentic CLI (Claude Code for the Sonnet 4.5 generator, codex for the GPT-5.5 challenger, Cursor in the open-weight run), so the harness is a typed meta-loop over off-the-shelf agents, owning only the stage contracts, the hygraph, and the gate between them. The generator ran with extended thinking on; the challenger arbitrated with reasoning off, a point against a model-deliberation reading of the gate. For each scored instance the loop reads only that instance's own artifacts; no other instance's graphs, trajectories, or solutions enter the context.

The boundary that matters most: on the public split the bench's `FAIL_TO_PASS` tests are visible, and the frozen harness's in-container gate executes them as its stop signal (their names as budget control, their bodies never in the model's prompt). The standardized leaderboard scaffold is denied them by design. That difference is the dominant attribution channel (§(oracle-bracket)), and the held-out split removes even the names, so nothing in this paper's public-split numbers transfers to the private set. Swapping the entire model pair to open weights ported the result with no structural change, evidence the harness is not vendor-specific; that run's near-gold tail discounts as recall, with the details in the repo.

### The number, with receipts {#results}

The texture behind the rate is committed, not narrated: the whole eligible public set graded with 0 incomplete at frozen tags `prereg-pro-v1` and `prereg-pro-v1-cheap`, per-repo tables (ten of eleven repos above 92%), the first-pass/re-entry split (~93% of trajectory-captured wins resolve on the first pass), the development-overfit check (the development language resolves *lower* than the never-touched languages), re-grades that reproduce (6/6 frontier cross-language, 60/60 open-weight stratified, 0 flips, ~$3 per WIN to audit), and all 34 losses carrying non-empty rejected patches. Start at the repository scoreboard ([github.com/kimjune01/swebench-pro](https://github.com/kimjune01/swebench-pro)).

*OSS deployment trace.* **81 PRs merged across 73 cold repositories** at a **50.6%** merge rate under adversarial maintainer grading: agent-selected issues, agent-authored patches, agent-submitted PRs, zero human keystrokes in any diff, and only ~8 of 79 closures rejections on the merits. The ledger stays GraphQL-verifiable (`pr-receipts.jsonl`); ~385 hypothesis graphs from the same campaign are public at [`kimjune01/sweep/repo-hypotheses/`](https://github.com/kimjune01/sweep); the narrative is [Speedrunning Open Source](/speedrunning-open-source).

Two receipts, two independent attestors:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:9.5em"><col><col style="width:13em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Receipt</th><th style="background:#f0f0f0">Evidence</th><th style="background:#f0f0f0">Attestor</th></tr></thead>
<tr><td>Pro (preregistered)</td><td>terminal: 694 / 728 = 95.3%, 0 incomplete, whole eligible set graded</td><td>Scale's official grader, re-runs the committed patch</td></tr>
<tr><td>OSS PR merge rate</td><td>81 merged across 73 cold repos, 50.6%, GraphQL-verifiable</td><td>adversarial maintainers who merged</td></tr></table>

We do not attest; the receipts do. No method documented in our comparative search (§(search)) has demonstrated, with equivalent receipts, a higher SWE-bench Pro official-grader resolve rate under one frozen harness. That claim is about the artifact and its auditability, and it survives the attribution below. What does not survive is any reading of the rate as evidence for the method.

### Three limits on the number {#central-comparison}

Three readings the number does not support, stated before the attribution rather than after:

- **Not a leaderboard number.** The board ranks models through one fixed scaffold; this run holds the model roughly fixed and rebuilds the scaffold. A harness number has no slot on a model board by construction.
- **Not a held-out number.** The public split is the audition; Pro's private split removes even the test names, so the gate must go blind there, and nothing in this paper predicts that result.
- **Not an isolation of the method.** The within-pass `implement`→gate refinement loop, the vendor inner agents, the thinking-on generator config, and the gate's oracle access all ride along. The next section separates them.

### Attribution: where the lift lives {#attribution}

The attribution decomposes the gap channel by channel. Each cut is preregistered or receipt-committed in the repository, including one retracted estimate and its worklog trail; the paper keeps the findings.

<table style="max-width:760px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:17em"><col style="width:15em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Channel</th><th style="background:#f0f0f0">Cut</th><th style="background:#f0f0f0">Effect on Pro resolve</th></tr></thead>
<tr><td>Gate access to the visible tests</td><td>oracle bracket, n=50</td><td><strong>~46 points</strong> (50% floor → 96% ceiling)</td></tr>
<tr><td>Peircean prompt vocabulary</td><td>M vs G vs T, n=38/36</td><td><strong>null</strong> (CIs straddle zero)</td></tr>
<tr><td>Directed diagnostic perturbation</td><td>deprived arm, n=110</td><td>+0.105 on underdetermined-cause stratum only; threshold-level</td></tr>
<tr><td>Entire diagnosis stage (the smem)</td><td>minimal-prompt arm, n=34</td><td><strong>~1 point</strong>, resting on two instances</td></tr>
<tr><td>Model pair (frontier → open-weight)</td><td>pair swap, n=728</td><td>2.2 points raw; ~17–22 genuine after recall discount</td></tr>
</table>

### The oracle bracket {#oracle-bracket}

The largest channel is the one the original design held constant and therefore could not see. On a preregistered 50-instance random sample, an implement-only loop with no oracle access floors at **50%**; restoring the bench's tests for the gate to iterate against raises the ceiling to **96%** ([`PREREGISTRATION-baseline-replication.md`](https://github.com/kimjune01/swebench-pro/blob/main/docs/PREREGISTRATION-baseline-replication.md), [the bracket](https://github.com/kimjune01/swebench-pro/blob/main/docs/HYPOTHESIS_GRAPH-pro-harness.md)). Forty-six points sit between those arms, bought by oracle access, not by the same models reasoning harder; the floor sits near the bare-model board scores (43.6–64.3%), the ceiling at the headline. The companion posts reached this conclusion first ([Precisely Wrong](/type-iii-error), [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro)).

### Given the oracle, the rest adds almost nothing {#attribution-verdict}

Measured against that oracle, every remaining channel barely moves, and they tell one story. The methodeutic prompt vocabulary scores no better than generic rigor or the bare task (null, CIs straddle zero). Deleting the whole diagnosis stage, a minimal prompt with no graph handed only the problem and the failing tests, lands near **94%**, about a point under the full harness: the minimal prompt reaching the number is the attribution made plain. The aimed diagnostic probe buys only a threshold-level sliver, and only where the text does not determine the cause, because the gate's cheap, trustworthy verdict lets blind try-and-check substitute for aimed diagnosis; that substitution is the falsifiable handle, degrade the gate and the deprived arm should worsen, which is the regime the mechanism experiment runs (§(right-regime)). The model pair, the lever leaderboards rank, moves the raw rate two points. So the answer to *how well does the method work* is: not on this bench, because the bottleneck here is not diagnosis. The full per-channel statistics, one retracted estimate and its worklog trail included, live in the repository ([swebench-pro](https://github.com/kimjune01/swebench-pro)).

### The benchmark gap {#audit}

The deeper reason the number says nothing about the method: a benchmark is the wrong instrument for this. SWE-bench Pro measures spec-conformance, where the requirement is handed over and there is nothing to diagnose, so the typed, diagnostic reasoning the hygraph encodes is precisely what it cannot see. A determinacy audit of the task set bears that out. The nulls of §(attribution) are not the method failing; they are what a true mechanism looks like on an instrument blind to it, a matter of applicability, not fault.

## Discussion {#discussion}

### Attributed nulls and the typing protocol

The discipline that bounds the bench number (§(bench)) is the same one that makes a null publishable: preregistration, freeze, official-grader-only verdicts, per-instance provenance. These nulls publish *attributed*, each arriving with the mechanism that produced it, the gate compensating, the spec handed over, the lottery fraction. An unexplained null says stop; an attributed null says where to point the next instrument.

Does the Peircean framing do any real work, or is it decoration? On this bench, the honest answer is now: as *rhetoric*, decoration (§(attribution-verdict)); as *protocol*, load-bearing. The prompt ablation measured whether the vocabulary makes a single diagnosis smarter, and it does not. What it could not measure is interop. A hygraph written in one context window must be read in another, by a different model, a parallel agent, or a human auditor, and the mode labels are what make a node interpretable without the context that birthed it: abduction marks a belief as proposed-untested, induction marks it as test-backed, and the credence cap travels with the type. Loose vocabulary produces graphs only their author's window can interpret, and those die with it. The Peircean typing is the wire format that lets the smem be shared across compactions, across agents, and across the trust boundary to the auditor, and the common vocabulary is the protocol for verifying each other's work: a peer that reads `induction, test-backed, here is the command` can rerun the command, where a peer that reads loose prose can only believe it or not.

This resolves the apparent tension with the prompt null rather than sitting beside it. A protocol does nothing on its own on any individual instance, the same way a wire format makes no single message smarter, so a per-instance ablation measuring the vocabulary against loose prose *should* read null, and did. The protocol's value accrues across instances, where it gains the property the whole paper is after: accountability becomes transitive. When every node speaks the same typed contract, agent B can verify agent A's kill by rerunning it, agent C can build on B's verification without re-running A, and a human auditor can enter the chain at any link; the warrant flows down the chain with the receipts, never resting on any link's word. Loose vocabulary caps accountability at one hop, the author vouching for their own graph. A common protocol lets verification compose: that is what 385 graphs in one vocabulary are for, and the precondition for everything §(future-work) builds on them.

### The trace is the contribution

The reframe this work forced is the one its epistemology was always pointing at. The bench treats an agent as a scorer of verdicts. The hygraph treats an agent as a builder of claims. Everything that survived the demolition lives on that second reading, and each virtue below is one face of it.

Name the enemy first, because every block below is aimed at the same one: the output that is **confidently wrong and impossible to verify**. The flux minimal arm is that enemy caught in the act. On the second model it shipped a fix that passed all 965 of the project's tests by the agent's own check and that *accepted invalid programs the type checker is supposed to reject*: suite-green and unsound at once. Nothing the project ships could catch it, the agent reported done, and only the recorded inquiry, replayed against an off-suite discriminator, exposed it. This is the failure mode that scales with capability rather than away from it, the one fluent generation produces by default; this work met it everywhere it looked (the over-narrow fix, the 4/4 false-green self-audit, the recall-inflated resolve rate). Trust is the default mode of consuming agent output, and the substitution this paper asks of its audience is exact: accountability in place of trust, line by line, machine-checkable. The contrast is the whole argument. The minimal agent offered a verdict: suite green, done. The graph agent offered a ledger: nineteen nodes, each a hypothesis, an exact command, an observed outcome, and the edge the result generates. You audit a ledger line by line, and at no point do you extend credit. The fix was knowable as better *without trusting the thing that produced it*, and that property, not the win, is the durable result.

**Truth is buildable, and the graph is the build.** On the view developed in [Truth Is Buildable](/truth-is-buildable), a true claim is a structure assembled from sources: provenance is the dependency graph, citation is an edge, attestation is the signed build log, falsifiability is the build being able to go red, and truth is the build currently passing. The hygraph mechanizes that picture one claim at a time. A node without a replayable trial is not a low-quality node; it is not a node, the same way an uncheckable number is not a measurement. A resolve rate, even an honest one, is a verdict over 728 builds the reader cannot climb. A hygraph is the climbable chain. By the paper's own epistemology, the second artifact carries more truth per byte than the first.

**The asymmetry engine.** A fabricated reasoning trace is expensive to sustain, because every fabricated node has to survive a replay the author does not control. A confident narrative is cheap to invent, because nothing in it is pinned to a procedure. The minimal arm's over-narrow fix is the cheap kind: it reads as finished, and reading it harder never reveals the flaw; the receipt reveals it in one command. Verification is not a tax on the method. It is the method. The same asymmetry governs failure: a trusted oracle that fails is a betrayal and leaves you nothing, while a truth-builder that fails leaves a trail that names the failed node. The flux graph recorded its own three mistakes, in advance, as kills that generated its next edge, each correction itself a replayable trial. One method hides its errors inside confidence. The other spends them as fuel.

**Persistence: out of the window, with no half-life.** Replay's second payoff is survival. The context window is the machine's working memory: fast, wide, and mortal. Chain-of-thought lives there and evaporates with it. The hygraph is reasoning that climbed out before the window closed, demonstrated at our own expense when a build box died mid-investigation and only the externalized graph and patch survived to be resumed. Writing was always this move; what the graph adds is that the externalized form is not merely readable later but *re-runnable* later, and the discipline that makes it real is self-sufficiency: every node carries its own reconstitution, or it only looks like it outlasts the window until you try to resume. The same property runs forward in time. Trust weakens with the witness and dies with the memory; a replayable trial copies without loss and survives as long as one copy does. The honest scope: the logical content has no half-life, while the runnable form inherits the half-life of its apparatus (our graphs replay only while flux builds, z3 runs, and the SHAs resolve), so provenance approaches eternal as replay approaches first principles. And what it preserves is not truth but *checkability*, which is stronger: a false claim backed by trust launders itself clean as the witnesses die; a false claim backed by provenance stays caught, forever. Provenance is not eternal truth. It is eternal vigilance.

**Trust versus accountability.** *Nullius in verba*, extended to the machine: take nobody's word, not even the silicon's; check its receipts. To a maintainer, a coding agent is a nobody, and so is its operator, and when receipts are attached it does not matter: a red-on-master, green-with-fix test plus a soundness twin plus a clean suite reads identically whoever submits it. Merit discriminates no substrate. The 81 merged PRs are the ecological witness: adversarial strangers accepted agent-authored code at 50.6% on the strength of attached evidence, not attached reputation. This is a principled direction for what alignment can mean: not a trustworthy agent we then believe, but an accountable one whose every claim is bound to a test a hostile party can rerun. When a recent DeepMind position paper on *artificial epistemic agents* warns that verification by source authority is collapsing into a "verification crisis" and calls for "robust falsifiability pipelines" whose claims are "structured in a way that allows them to be proven wrong" (Marchal et al. 2026, [arXiv:2603.02960](https://arxiv.org/abs/2603.02960)), it names the need; the hygraph is the mechanism, and the kill condition is precisely what structures a claim to be provable wrong. Reliability is the same epistemics accumulated: you never arrive at trust, you arrive at a body of attestations too large and too redundant to doubt, which is a different and better place to stand. The guarantee stays narrow and real. Everything *attested* is checkable; nothing guarantees that everything *relevant* is attested, and choosing what must be on the ledger is exactly where human judgment stays load-bearing.

**The equilibrium looks like accounting, and Enron is the precedent.** Alignment will not resolve to one answer. The working anticipation is a control regime in the shape accounting reached after its own confidently-wrong-and-unverifiable era: standards (GAAP), independent audit, and the three-way match, where no payment clears unless the purchase order, the receiving report, and the invoice agree, no single party trusted to hold more than one leg. The agent analog is already this harness's shape: no claim clears unless the proposer's claim, the recorded trial, and an independent replay agree, and the generator never grades its own work. [Enron](https://en.wikipedia.org/wiki/Enron_scandal) is the lesson about the alternative: self-attestation scales smoothly right up until the catastrophe that legislates the controls after the fact. Note what this view of alignment is not. Benches operationalize alignment as obedience and conformance, and the audit shows it (§(audit)): three quarters of the tasks grade transcription of a handed spec, the rest grade recovery of an unstated choice. Agency is neither. An agent facing underspecified prose can guess and conform (the lottery), refuse, or exercise agency: elicit the missing decision, make the call, and declare it with receipts. Benches score only the first; the control regime above is built for the third (§(future-work)).

**Merit attaches to the work, not the doer.** Under all of the above sits a separation humans rarely make. We route praise and blame to doers, for lack of vocabulary and social norms that could route them to the work, and the conflation was affordable while only humans produced work, because the doer was a serviceable proxy for the work's quality. It is not affordable now. An agent can produce a thousand artifacts of any quality overnight; judging them by their author runs exactly backwards, and judging the author by replaying the artifacts is the only direction that scales. Merit, read precisely, is what survives the shift: the warrant a piece of work carries in itself, checkable without reference to who or what produced it. The hygraph is vocabulary for that norm, a unit of work that ships with its own evidence; the receipts-first PR is its social practice; the maintainer who merges on the ledger alone is its early adopter. This paper is, deliberately, a declaration of the norm in a searchable venue: praise the work, blame the work, replay the work. The doer earns standing only as the accumulation of work that survived.

**Legibility, revisited.** The legibility question from the introduction completes here. A benchmark number is legible to people who will never read a trace, and that reach is worth something; it is how this work got read at all. But the number is the artifact a reader can do the least with. It cannot be perturbed, cannot be replayed, cannot surprise anyone into a rival hypothesis. The flux trail can: a reader who suspects the graph arm got lucky can run the receipt, construct a new discriminator, attack a node. The bench result is an answer. The live example is an instrument, and instruments are what inquiry actually accumulates.

### What the structure unlocks

A data structure earns its keep by what it unlocks. Five affordances follow, in ascending order of consequence, and the first four set up the last.

*Parallel agents, shorter wall-clock.* The graph is monotone: nodes append, kills are idempotent. Parallel agents can therefore latch onto one shared graph lock-free, fan out across rival hypotheses, and re-verify each other's kills instead of trusting them, with transitive accountability (above) as the precondition that makes the fan-out safe. A prose summary must be re-parsed into independent units before anything can be dispatched; the graph ships pre-factored. Named, not yet run (§(future-work)).

*Model-provider independence.* The smem lives in the harness, in plain markdown, behind typed contracts any capable model can read and write. The pair-swap run is the witness: the entire model pair changed and the structure ported wholesale (§(models)). Reasoning that accumulates in a vendor's context window is a liability; reasoning that accumulates in a substrate you own is an asset.

*Accountability.* Every claim ships with its replay; the whole discussion above is this affordance unpacked.

*Alignment.* Trust displaced by audit: an agent whose every claim binds to a test a hostile party can rerun does not need to be believed to be used.

*Discovery, in Sutton's sense, and the claim the other four exist to support.* The epigraph closes here. A model's unaided output gives no way to tell discovery from recall: fluent text arrives with no record of how it was reached, and recombination of training data is indistinguishable on its face from inquiry into the world. The hygraph supplies what is missing, an externally checked update at every step: each node is anchored to a fresh trial of the world, so the route from question to fix is a sequence of falsifiable commitments rather than a forward pass. The flux fix was absent from the reachable corpus until the inquiry built it, on an issue its own maintainers were stuck on. That is reasoning beyond documented corpus recall, and a creative act by a definition precise enough to argue with: a novel, sound, useful solution absent from the reachable sources under the contamination audit, produced under documented constraints and surviving a stranger's replay. Each clause is a receipt, not a flourish, and a skeptic who rejects the word should say which clause fails. Agents that contain what we have already discovered recall; an agent that can build and survive a hypothesis graph discovers. Sutton asked for the second kind, and flux #1613 is one of them, witnessed.

## Related work {#related-work}

### Construct validity and contamination {#rw-swebench}

The SWE-bench family defines the Verified / Pro lineage, official harness, and contamination-resistant tier design. **SWE-Bench+** (Aleithan et al. 2024) manually audited the original bench: 32.67% solution leakage, 31% weak tests. **OpenAI's February 2026 audit** found a majority of audited Verified tasks have flawed tests and that frontier models reproduce exact gold patches; it stopped reporting Verified and recommends Pro. **Wang, Pradel & Liu** (ICSE 2026) show plausible patches pass tests yet diverge from developer intent; their axis is patches that pass but are wrong, ours (§(audit)) is tasks whose materials do not determine which passing behavior is intended. **ORACLE-SWE** ([arXiv:2604.07789](https://arxiv.org/abs/2604.07789)) quantifies the same handover, ablating the oracle and specification signals that leak through a task and measuring the resulting drop; **SLUMP** ([arXiv:2603.17104](https://arxiv.org/abs/2603.17104)) opens on the identical premise, that benchmarks supply the full specification upfront while real coding does not, and answers it by building an underspecified-by-design benchmark. This paper parts from both on the verdict: they treat handover as a defect to fix with a better benchmark, while the determinacy audit (§(audit)) draws it as a category boundary, a spec-conformance instrument cannot be tuned into a measure of diagnostic inquiry because the two are different types. **SWE-rebench** uses post-cutoff filtering as a parallel contamination strategy; **LiveCodeBench** (Jain et al. 2024) is the origin of post-cutoff (temporal-holdout) evaluation, and the standard objection to it applies here too, that training cutoffs are porous because RL post-training and inference-time retrieval can surface later content. The witnessed case (§(right-regime)) is built against exactly that objection: the fix was absent from the reachable corpus at solve time, and for the controlled run the graph was regenerated by a model whose weights predate it, so neither porosity nor retrieval supplies the answer. **HAL** (Stroebl et al. 2025) is the third-party cost-aware agent leaderboard and the nearest infrastructural precedent for this paper's cost-transparency stance; this paper's receipts go one level finer, to the per-instance re-gradeable verdict. The official **swe-bench/experiments** repo requires `trajs/`, `logs/`, `patch.diff`, `report.json` per submitted instance, the minimum publication norm our provenance contract extends with gate traces, hypothesis graphs, and a cost ledger.

### Agent scaffolds and SE-agent harnesses {#rw-scaffolds}

SWE-bench-targeted harnesses include OpenHands (Wang et al. 2024), SWE-agent (Yang et al. 2024), and AutoCodeRover (Zhang et al. 2024/25), all built on the ReAct pattern (Yao et al. 2023); none implements Peirce-typed stage contracts or a kill-conditioned hypothesis-graph memory. **Voyager** (Wang et al. 2023) is the closest loop-shape precedent: embodied observe→hypothesize→test→commit, with a skill library where this work holds falsifiable claims. **SWE-Effi** ([arXiv:2509.09853](https://arxiv.org/abs/2509.09853)) is the sharpest published counter-position: effectiveness emerges from scaffold-model synergy rather than residing in the scaffold alone. This paper now agrees from the other direction, with the synergy named: on Pro the binding pair is gate × oracle, and neither scaffold typing nor model tier moves the number more than about two points once that pair is in place.

Two concurrent developments arrived independently at adjacent points, each carrying one of the two components this paper composes. **Theorem-of-Thought** ([Abdaljalil et al. 2025](https://arxiv.org/abs/2506.07106)) types reasoning into abductive, deductive, and inductive specialist agents per query: the typed cycle, without a persistent typed memory across cycles. **Cognitive Memory Manager** ([Khalid & Arora 2026](https://openreview.net/forum?id=yCsHQnvvWY)) extracts a typed-node DAG by observing agent execution and mines it for patterns to promote to skills: the typed graph, mined descriptively where ours is generative (it routes the run). That three labs converged on these decompositions without coordination is itself structural evidence that typed reasoning and typed memory are landing as natural primitives. Provenance for the framing here is timestamped on the project blog ([The Hypothesis Graph](https://june.kim/the-hypothesis-graph), [Evidence has a trajectory](https://june.kim/evidence-has-a-trajectory)).

Convergence forces a vocabulary question, and this paper answers it by pointing rather than claiming. The trichotomy the siblings reach for is Peirce's (1878, 1903). Theorem-of-Thought builds abductive, deductive, and inductive agents while citing no pragmatist anywhere in its reference list (checked against its [v2 source](https://arxiv.org/html/2506.07106v2): forty-four uses of the mode words, zero occurrences of Peirce, pragmatism, James, Dewey, or Ramsey), so the field's citation graph for its own typing is incomplete, a dangling pointer where the lineage should sit. §(grounding) and §(lineage) wire the vocabulary to its sources, and the dated posts above timestamp this lineage's use of the hypothesis-graph primitive. Interop (§(discussion)) will force one wire vocabulary on this design space, and the candidate that is mode-complete, a century and a half stable, and already carrying the credence semantics the nodes need does not require anyone to invent it.

<style>
.relwork-table td { padding: 6px 8px; vertical-align: top; border-bottom: 1px solid #eee; }
.relwork-table tr.ours td { background: #fafaf5; font-weight: 500; }
</style>
<div class="table-wrap">
<table class="relwork-table" style="margin:1em auto; font-size:13px; border-collapse:collapse; line-height:1.35;">
<colgroup><col style="width:14em"><col style="width:9em"><col style="width:14em"><col style="width:16em"><col style="width:13em"></colgroup>
<thead><tr><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">System</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Domain</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Reasoning-mode typing</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Persistent structure & update</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Termination gate</th></tr></thead>
<tr><td>Voyager (Wang et al. 2023)</td><td>Minecraft</td><td>None</td><td>Skill library; test-validated graduation</td><td>Test-pass on skill</td></tr>
<tr><td>IDEA (He et al. 2025)</td><td>Interactive rule learning</td><td>Peirce-cited, agent-level</td><td>Working rule set</td><td>None explicit</td></tr>
<tr><td>ADI (Gilda & Gilda 2026)</td><td>Algebraic invariants</td><td>Peirce, layered (L0/L1/L2)</td><td>Symbolic knowledge graph</td><td>None explicit</td></tr>
<tr><td>AriGraph (Anokhin et al. 2024)</td><td>TextWorld</td><td>None</td><td>Knowledge graph (entities, relations, episodes)</td><td>None explicit</td></tr>
<tr><td>CausaLab (Yang et al. 2026)</td><td>Causal discovery</td><td>Causal-typed (SCM)</td><td>Evolving structural causal model in a DSL</td><td>None explicit</td></tr>
<tr><td>BeliefMem (Liao et al. 2026)</td><td>Partial-observability QA</td><td>None</td><td>Candidate set; Noisy-OR probabilistic update</td><td>Probabilistic threshold</td></tr>
<tr><td>Theorem-of-Thought (Abdaljalil et al. 2025)</td><td>General reasoning</td><td>Peirce, agent-level</td><td>Formal reasoning graph</td><td>NLI-guided Bayesian coherence</td></tr>
<tr><td>CMM (Khalid & Arora 2026)</td><td>SE (coding agents)</td><td>7 trajectory roles, extraction-time</td><td>Typed DAG; confidence decay</td><td>Human approval + retrieval-validated threshold</td></tr>
<tr class="ours"><td>This work</td><td>SE (industrial code)</td><td>Peirce, enforced at write time per stage</td><td>Hypothesis graph; mechanical kill predicates on the audit verdict</td><td>Deterministic finite-state</td></tr>
</table>
</div>

<figcaption style="text-align:center; font-size:12px; color:#666; margin-top:-0.5em;"><strong>Table 1.</strong> Comparison spine for adjacent typed-reasoning and graph-memory LLM-agent systems. Cell terseness is by design; prose nuance in §(typed-memory).</figcaption>

### Typed reasoning and graph-structured memory {#typed-memory}

**IDEA** (He et al. 2025, ACL Findings, [arXiv:2408.10455](https://arxiv.org/abs/2408.10455)) explicitly cites Peirce and uses the three modes in an interactive rule-learning benchmark. **ADI** (Gilda & Gilda 2026, [arXiv:2604.15727](https://arxiv.org/abs/2604.15727)) gives an explicit Peircean tripartite protocol with epistemic layers over a symbolic knowledge graph; near-simultaneous with this paper's draft and the most conceptually adjacent prior work. Both target reasoning domains outside SE.

The hygraph sits at the intersection of three lineages: cognitive-architecture memory (Soar / ACT-R / EPIC), LLM-agent memory systems (CoALA / AriGraph / Mem0 / Zep), and typed-belief representations (CausaLab / BeliefMem / Theorem-of-Thought / CMM). This paper adopts the Soar memory typology directly as its slot vocabulary, adding only the specific content of the `smem` slot: Peirce-typed, kill-conditioned, designed for LLM prose read/write. Adjacent work: **Kirk, Wray & Laird 2023** ([AAAI](https://ojs.aaai.org/index.php/AAAI-SS/article/download/27690/27463/31741)), an LLM-port of the Soar lineage; **CoALA** (Sumers et al. 2023/24, [arXiv:2309.02427](https://arxiv.org/abs/2309.02427)); **AriGraph** (Anokhin et al. 2024/25, [arXiv:2407.04363](https://arxiv.org/abs/2407.04363)), the closest precedent for graph-structured LLM-agent memory; **CausaLab** (Yang et al. 2026, [arXiv:2605.26029](https://arxiv.org/abs/2605.26029)); **BeliefMem** (Liao et al. 2026, [arXiv:2605.05583](https://arxiv.org/abs/2605.05583)), strong adjacent on uncertain alternatives with mechanical update.

**CMM** (Khalid & Arora 2026, [OpenReview](https://openreview.net/pdf?id=yCsHQnvvWY); published one day before this paper's first draft) warrants its own comparison. Both systems converge on the same role for memory: a persistent, typed, queryable DAG of reasoning artifacts. The runtimes diverge on agency. CMM is observe-and-consume: an external agent perturbs, CMM types the trajectory post hoc, future runs consume graduated skills. Our loop is perturb-and-falsify: kills fire mechanically during the live inquiry, and the graph routes the run. Same data structure, opposite epistemological direction, and complementary by construction: the ~385 graphs committed in `sweep/repo-hypotheses/` are exactly the corpus CMM's graduation pipeline could consolidate into per-repo skills.

Four 2026 systems each carry one component this work combines, which sharpens what is novel here: the *join*, not any single piece. **FVDebug** ([arXiv:2510.15906](https://arxiv.org/abs/2510.15906)) builds an actual hypothesis graph for debugging, with a frontier and accumulated evidence, but selects the next node by asking the model, the arbiter this work removes. **From Hypotheses to Factors** ([arXiv:2604.26747](https://arxiv.org/abs/2604.26747)) runs the same perturb-and-falsify loop, falsifiable hypotheses behind a deterministic engine over an append-only trace, locked to quantitative finance where this work claims the general semantic-memory substrate. **Portable Agent Memory** ([arXiv:2605.11032](https://arxiv.org/abs/2605.11032)) is the nearest provenance memory, a Merkle-DAG that cites the Soar lineage and makes every node reconstructible by content-addressing, but it certifies *integrity* (the recorded bytes are untampered) where the replay invariant here certifies *warrant* (the node still survives its trial). And the provenance survey **From Agent Traces to Trust** ([arXiv:2606.04990](https://arxiv.org/abs/2606.04990)) enumerates exactly the relations this work mechanizes, Support, Contradict, Invalidate, and names "how provenance quality should be evaluated" as an open problem; the hygraph is one answer, with replay as the quality bar and the kill condition as an executable edge rather than a descriptive label.

> *Production LLM memory systems with graph variants (Zep/Graphiti, Mem0), staged-hypothesis selection in science agents, deterministic gating in adjacent settings, and reflective memory systems (Reflexion, DebugMate) are surveyed in the appendix; they are adjacent on particular axes but do not change the comparison spine.*

### Adversarial filtering and termination {#adversarial-termination}

<div class="table-wrap">
<table class="relwork-table" style="margin:1em auto; font-size:13px; border-collapse:collapse; line-height:1.35;">
<colgroup><col style="width:18em"><col style="width:11em"><col style="width:14em"><col style="width:13em"><col style="width:11em"></colgroup>
<thead><tr><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">System</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Domain</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Stage operated at</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Visibility regime</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Cross-family</th></tr></thead>
<tr><td>Multi-Agent Debate (Liang et al. 2023/24, <a href="https://arxiv.org/abs/2305.19118">arXiv:2305.19118</a>)</td><td>General reasoning</td><td>Patch / answer stage</td><td>Open (cross-visibility)</td><td>Single model family</td></tr>
<tr><td>Refute-or-Promote (Agarwal 2026, <a href="https://arxiv.org/abs/2604.19049">arXiv:2604.19049</a>)</td><td>Defect discovery</td><td>Review stage</td><td>Asymmetric context</td><td>Yes</td></tr>
<tr class="ours"><td>This work</td><td>SE (industrial code)</td><td>Pre-patch hypothesis stage</td><td>Blind challenge (no cross-visibility)</td><td>Yes (Sonnet + GPT-5.5)</td></tr>
</table>
</div>

<figcaption style="text-align:center; font-size:12px; color:#666; margin-top:-0.5em;"><strong>Table 2.</strong> Adversarial multi-model filtering: this work occupies the pre-patch / blind cell. Termination disciplines (λ_A's type-theoretic proofs, SafetyDrift's absorbing states) sit at composition or trajectory scope where this work's verdict-routed gate sits per-instance.</figcaption>

Closest in spirit is **POPPER** ([arXiv:2502.09858](https://arxiv.org/abs/2502.09858)), which runs agentic sequential hypothesis tests under e-value error control, the same sequential-testing machinery this project's `inquire` workflow uses to classify evidence. POPPER terminates statistically, on an error-rate bound over a population of tests; this work terminates mechanically, on a deterministic kill predicate over a single binary verdict, and persists the outcome as replayable memory where POPPER's tests are ephemeral.

## Limitations {#limitations}

*The mechanism evidence is existence-grade.* One audited divergence, on one instance, in a program that was not preregistered when it ran. The pilots' nulls are confounded by a selection artifact we can name but not yet remove (the triage fast-path), and the localization-hard band where the mechanism should live has not been decisively tested; its one strong candidate did not reproduce at HEAD. Nothing here is a rate.

*The audit's two tiers carry different burdens.* The mechanical spine (11.4%) is re-derivable by grep; the two-expert tier rests on a stated standard, adversarially verified (κ = 0.52, all disagreement skeptic-stricter), and 63 screen-flagged candidates are excluded as rater-pending. The proven floor is a floor.

*The bench numbers are public-split numbers.* Pro's public repos predate both model families' cutoffs; the gold-overlap audit bounds frontier reproduce-gold at ~2%, but our holdout is weaker than Scale's (different commits, same repos), and the held-out submission has not been made. The gate's oracle access does not exist on the private split.

*Essence oracles are authored.* The mechanism experiment's graders are written from upstream issue text by the operator's pipeline, mitigated by red-at-base/green-on-gold walls and by the merged fix's external attestation, not eliminated.

*The smem is small and per-instance.* Hypothesis graphs in this work are one markdown file per inquiry; cross-instance accumulation is untested. That carries its own deflationary point: the file was never the bottleneck at any repo size, so heavier stores need to earn their keep at cross-instance scale, not per-instance.

*How to refute this.* The central claims are built to fail loudly, so here is where to push, each against a committed artifact a hostile reader runs rather than a promise. The discovery claim dies if the flux receipt fails to replay, or if one discriminating program shows the graph arm's fix wrong where the minimal arm's is right: the mechanism evidence returns to zero cases, and both patches with the oracle are committed at `flux-1613-trail-v1`. The methodology claim dies if, as audited cases accumulate under the preregistered protocol, the minimal arm matches the graph arm everywhere a receipt can see: the smem is then redundant even where it was built to matter, and that null is the next paper, named as this thesis's own falsifier in the mechanism README. The attribution dies if the oracle bracket fails to replicate from its preregistered sample. The discovery word itself is defined to be argued with, clause by clause (§(discussion)); a skeptic who rejects it should name the clause that fails.

*Generator staleness.* The checkpoints are fixed (Sonnet 4.5 era). Baseline reach was already eating the mechanism's band during the pilots, and newer models eat further. The mechanism claim survives only in the regime where verification, not generation, is the bottleneck, which is also the regime the discussion argues is the one that matters.

## Future work {#future-work}

The program reorganizes around the smem, in order of leverage.

- **The preregistered mechanism hunt.** The flux divergence defines the target band: localization-hard, verification-bottlenecked bugs where the symptom sits far from the cause and the suite cannot see the difference between fixes. Each loop now carries its deductive rung before it runs: testing X, predict Y, refuted by Z (`METHODOLOGY-preregistration.md`, `CANDIDATES-localization-hard.md`). Three to five audited existence cases, or the committed null, is the next paper.
- **The hygraph as a type.** Specify the abstract data structure independently of this harness: operations (perturb-and-classify, generate-edge-from-kill, prune, replay), the soundness invariant (every node reconstructible from its recorded trial), and a serialization any agent can emit. The goal is an interchange format for auditable reasoning, so that "show your work" becomes a machine-checkable demand rather than a rhetorical one.
- **Grade the trace, not just the patch.** Bench design follows from the audit: report determinacy-aware denominators; build instruments whose oracle is expensive or absent and whose causes are hidden, because that is where method separates from reach; and score submissions on replayability, so a suite-green over-narrow fix (§(right-regime)) stops being indistinguishable from a root-cause one.
- **Elicitation for underspecified prose.** The audit's proven underdetermined fraction has a correct agent response that no current bench can score: elicit the missing decision from the human who holds it, instead of recovering the author's unstated choice by guess. The hygraph gives elicitation a natural home: an underdetermined choice is an open node whose kill condition is a human answer, typed and waiting, so the question an agent asks becomes as auditable as the patch it writes. Designing instruments that reward pinning the spec before building, rather than scoring the lottery, is open work the determinacy tool's labels make tractable.
- **Receipts-first contribution as the deployment lane.** The flux submission is the template: fix, discriminating receipt, soundness twin, full suite, replayable graph, residual flagged to the experts. Agent PRs are drowning in justified slop suspicion; the trace is the antidote, because it converts "trust my patch" into "audit my ledger." Scaling that lane (and measuring maintainer response to trace-backed PRs against the 50.6% baseline) tests attestation-displacing-trust ecologically. The first maintainer merge of a trace-backed fix on a maintainer-stuck issue is the lane's golden ticket: an adversarial expert accepting the work on its ledger, with the doer invisible to the verdict.
- **Cross-instance smem accumulation.** Let the graph grow across instances within a repo, then across repos within a domain; the current work tests the smem only at per-instance scope.
- **Concurrent diagnosis over a shared graph.** The hygraph is monotone (nodes append, kills are idempotent), so parallel agents can read and write it lock-free, a conflict-free blackboard for the inquiry layered over git's blackboard for the code. Because kills are test-backed, an agent can re-verify a peer's elimination rather than trust it blind: the verifiable encoding's payoff in the multi-agent setting is trust between agents, the same displacement the discussion argues for between agents and humans.
- **Held-out submission.** Pro's private split removes the visible oracle, which after §(oracle-bracket) makes it the honest test of the gate-blind harness, not a formality. We expect a substantially lower number there and regard predicting it in print as part of the discipline.

Beyond SWE-bench, the harness is one chapter of a broader program: a compiler from prose to executable agent behavior, of which the methodeutic skills are the procedural memory, the hygraph the typed semantic memory, and the deterministic gate the runtime check. The program is developed at length in the [methodeutics textbook](https://june.kim/reading/methodeutics); *compiler* is used descriptively, in the LLVM (Lattner & Adve 2004) and DSPy (Khattab et al. 2023) lineage of typed pipelines from specification to reproducible behavior.

## Conclusion {#conclusion}

The challenge in the epigraph was restated in 2026 with the missing ingredient named, and the answer is the same shape as the question. The hypothesis graph is the *something more*: a typed, replayable file that lets a language model evaluate what it generates and retain what survives, and flux #1613 is one witnessed run of it. The mapping onto Sutton's three steps, variation, evaluation, and selective retention, is [its own short post](/suttons-recipe-for-discovery).

> We need true creativity and we need true discovery. Generative AI ... will never get us there. For these, we need something more.
>
> — Richard S. Sutton, [*AI creativity & discovery*](https://www.youtube.com/watch?v=K5LAFEjTlBA) (SAIR workshop on Science for AI, 2026)

## Availability and reproducibility {#availability}

- **Repositories.** [github.com/kimjune01/swebench-pro](https://github.com/kimjune01/swebench-pro) (the bench run; frozen tags `prereg-pro-v1`, `prereg-pro-v1-cheap`), [github.com/kimjune01/swebench-verified](https://github.com/kimjune01/swebench-verified) (prior-generation baseline, Zenodo-DOI'd), [github.com/kimjune01/swebench-pro-audit](https://github.com/kimjune01/swebench-pro-audit) (the determinacy audit; every claim one row in `CLAIMS.md`, all 728 verdicts in `COVERAGE.md`, mechanical spine re-derivable by grep), [github.com/kimjune01/determinacy](https://github.com/kimjune01/determinacy) (the audit as a portable tool for any SWE-bench-shaped bench; SWE-rebench run included), [github.com/kimjune01/hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism) (the mechanism experiment; flux trail frozen at `flux-1613-trail-v1`).
- **Provenance artifacts.** Per-instance trajectories, hypothesis graphs, captured diffs, gate traces, and cost ledger under `runs/scored/artifacts/`; preregistrations at the freeze SHAs; the OSS ledger (`pr-receipts.jsonl`) with the GraphQL query that recomputes every number it asserts.
- **OSS deployment trace.** ~385 hypothesis graphs at [`kimjune01/sweep/repo-hypotheses/`](https://github.com/kimjune01/sweep), one per investigated issue; PR-level outcomes pinned at `kimjune01/kimjune01@paper-2026-05-28`.
- **Replication.** Boxes, budget, the per-instance cost ledger (`COST_BASIS.md`), and the step-by-step rerun live in the run repo and the field guide [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro), not narrated here.
- **Companion writing.** The instrument story and field guide: [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro). The error this paper corrects, from the inside: [Precisely Wrong](/type-iii-error). The epistemology the discussion rests on: [Truth Is Buildable](/truth-is-buildable). Dated provenance posts establish parallel rather than derivative development: *Theory is load-bearing* (2026-03-17), *The proof manual* (2026-04-05), and *Type the question* (2026-04-08) predate ADI (2026-04-17); *Evidence has a trajectory* (2026-04-27) and *The Hypothesis Graph* (2026-04-28) predate CMM (2026-05-26).
- **PDF.** Arxiv-shape build at [/assets/methodeutic-harness-paper.pdf](/assets/methodeutic-harness-paper.pdf), rebuilt from this markdown source by `scripts/build-paper-pdf.sh`; the source is canonical.
- **DOI.** Verified artifact: Zenodo-DOI'd. Pro bundle and this paper: [placeholder: Zenodo DOIs pending.]
- **License.** Skills released under **CC-BY-SA-NS** ([june.kim/cc-by-sa-ns](https://june.kim/cc-by-sa-ns)); repo-level terms in each `LICENSE.md`. The harness an outsider clones is the same harness that produced the published numbers.

**Reproducibility invitation.** *Nullius in verba.* Every number in this paper is recomputable from committed artifacts: the bench verdicts by re-running the official grader on captured diffs, the audit's mechanical spine by grep, the flux divergence by replaying the receipt programs against both committed patches. Doubts should be filed as issues against the relevant repository; confirmed corrections fold into the next versioned artifact, as the retraction noted in §(attribution-verdict) and the reversal this version reports already have.

## LLM collaboration disclosure {-}

LLMs enter this work in three roles. *Subject of study*: the harness under evaluation uses frontier LLMs as generator and challenger, with versions, billing mode, and provenance disclosed in §(models) and the artifacts. *Instrument*: model pairs adversarially verify the audit's two-expert tier (one constructs, an independent family refutes) and blind-judge the mechanism pilots, always with the mechanical layer (grep, grader, replay) holding the verdict. *Writing aid*: the prose was drafted and revised with Anthropic's Claude (Opus 4.8 and Fable 5) from human-authored outlines and session notes; the claims, methodology, numbers, and argument structure are the author's. No LLM decided what to publish.

## Acknowledgments {-}

We thank John Laird for endorsing this submission, and the flux maintainers for engaging with a stranger's receipts on their hardest open issue.

## Novelty and comparative search protocol {.appendix} {#search}

- **Why this section exists.** Several claims in this paper take the form *"we found no prior X."* Such claims are only as honest as the search they rest on. This section publishes the queries so readers can re-run the search and either confirm the gap or find what we missed.
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

The artifact claim (§(results)), *no method documented has demonstrated a higher SWE-bench Pro resolve rate with equivalent receipts*, requires a comparative search. The bar for *equivalent receipts*: published per-instance trajectories, captured diffs, gate or evaluator traces, cost ledger, and reproducible run conditions.

**Candidate audit (against the receipt bar).** Each top public submission or comparable report is checked for: published per-instance trajectories (T), captured diffs (D), evaluator/gate traces (G), per-instance cost ledger (C), reproducible frozen artifact (R), and resolve rate at or above this paper's on the same bench. Receipt-bar columns are *present* (✓), *partial* (~), or *absent* (·).

<style>
.receipt-table td { padding: 6px 8px; vertical-align: top; border-bottom: 1px solid #eee; }
.receipt-table td.c { text-align: center; padding: 6px 4px; }
.receipt-table tr.ours td { background: #fafaf5; }
</style>
<div class="table-wrap">
<table class="receipt-table" style="margin:1em auto; font-size:13px; border-collapse:collapse; line-height:1.35;">
<colgroup><col style="width:18em"><col style="width:5em"><col style="width:1.5em"><col style="width:1.5em"><col style="width:1.5em"><col style="width:1.5em"><col style="width:1.5em"><col style="width:10em"><col style="width:22em"></colgroup>
<thead><tr><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Submission / report</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Bench</th><th style="background:#f0f0f0; padding:4px 4px; text-align:center;" title="trajectories">T</th><th style="background:#f0f0f0; padding:4px 4px; text-align:center;" title="captured diffs">D</th><th style="background:#f0f0f0; padding:4px 4px; text-align:center;" title="gate/evaluator traces">G</th><th style="background:#f0f0f0; padding:4px 4px; text-align:center;" title="cost ledger">C</th><th style="background:#f0f0f0; padding:4px 4px; text-align:center;" title="reproducible artifact">R</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Rate ≥ ours</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Notes</th></tr></thead>
<tr><td>Official <code>swebench/experiments</code> repo (multiple top entries)</td><td>Verified</td><td class="c">✓</td><td class="c">✓</td><td class="c">·</td><td class="c">·</td><td class="c">~</td><td>Various</td><td>Minimum publication norm: trajs/logs/patch.diff/report. No gate traces, no cost ledger.</td></tr>
<tr><td>Top vendor leaderboard entries (Claude Code, OpenHands, SWE-agent, AutoCodeRover)</td><td>Verified</td><td class="c">~</td><td class="c">~</td><td class="c">·</td><td class="c">·</td><td class="c">·</td><td>Reported below 97%</td><td>Submissions report numbers; reproducible bundles and cost ledgers rarely published.</td></tr>
<tr><td>SWE-bench Pro official page (Scale)</td><td>Pro</td><td class="c">~</td><td class="c">~</td><td class="c">·</td><td class="c">·</td><td class="c">·</td><td>N/A (curator)</td><td>Uncapped cost (250-turn limit). No per-instance cost ledger.</td></tr>
<tr><td>Nilenso Pro trajectory analysis</td><td>Pro</td><td class="c">~</td><td class="c">·</td><td class="c">·</td><td class="c">~</td><td class="c">·</td><td>N/A (third-party)</td><td>Cost/token/time analysis across four frontier models. Not a submission.</td></tr>
<tr><td>SWE-rebench public reports</td><td>rebench</td><td class="c">~</td><td class="c">~</td><td class="c">·</td><td class="c">✓</td><td class="c">~</td><td>Below ours</td><td>Strong cost transparency (Cursor Composer 2.5 at $0.23/problem).</td></tr>
<tr class="ours"><td><strong>This work: Verified</strong></td><td>Verified</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td>426 / 438 eligible (97.3%)</td><td>Companion repo <code>swebench-verified</code>; Zenodo DOI; gate traces and cost ledger committed.</td></tr>
<tr class="ours"><td><strong>This work: Pro</strong></td><td>Pro</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td>694/728 = 95.3%; open-weight pair 678/728 = 93.1%</td><td>Same frozen harness, whole eligible set, 0 incomplete; two model pairs under one bundle. Public-split, gate-oracle regime: an artifact claim, not a leaderboard claim (§(central-comparison)).</td></tr>
</table>
</div>

**Reading.** No row above this paper's two rows combines all six receipt-bar columns and a resolve rate at or above this paper's on the same bench. The claim survives as long as the table reads this way, and a citation showing a stronger combined receipt is the cleanest refutation.

## Extended intellectual lineage {.appendix} {#lineage}

*Foundational sources grounding §(grounding), §(hygraph), and §(related-work), collected here so Related Work stays focused on contemporary systems.*

### Peircean inquiry and the philosophy of science

- **Peirce 1878** (*Illustrations of the Logic of Science*): the original three-mode taxonomy.
- **Peirce 1903** (*Pragmatism as the Logic of Abduction*): abduction as the only mode that introduces new content.
- **Bacon 1620** (*Novum Organum*); **Popper 1934** (*The Logic of Scientific Discovery*): falsification as the inductive-side constraint.
- **Ramsey 1926** (*Truth and Probability*): operational credence as betting odds; the hygraph's node-level semantics descends from this work.
- **James 1907**; **Dewey 1929**: the pragmatist commitment that truth is inseparable from action.
- **Meehl 1967**; **Feynman 1974** ("Cargo Cult Science"): the difference between rigor-shaped activity and actual rigor, the standard §(attribution) holds itself to.
- **Kimball 1957; Tukey**: the Type III error, the exact answer to the wrong question; the failure mode the determinacy audit (§(audit)) is built to prevent, examined in the companion post [Precisely Wrong](/type-iii-error).

### The hygraph's structural ancestors

- **de Kleer 1986** (assumption-based truth-maintenance systems): persistent dependency structures over beliefs with mechanical retraction; the TMS keeps consistency where the hygraph keeps *trials*, and a TMS justification is not replayable by a stranger.
- **Dung 1995** (abstract argumentation frameworks): attack relations between claims as first-class structure; the hygraph's kill edges are attack edges bound to executions rather than arguments.
- **Wald 1947** (sequential testing) and **Vovk & Wang 2021** (e-values): the sequential-evidence framing that shaped `inquire`'s diagnostic stance. No accumulator is deployed: the code under test is deterministic, so the gate routes on the binary grader verdict (§(gating)).
- **Pearl 1988; 2000/2009**: DAGs as the substrate for structured belief and causal-structure inference; this work borrows the typed-node/typed-edge form and leaves the probabilistic semantics behind.
- **Zeller & Hildebrandt 2002** (delta debugging): the canonical demonstration that mechanical perturbation of code is a productive inference primitive; optimization-shape where the hygraph is methodology-shape.

### Bi-abductive and compositional inference

- **Calcagno et al. 2009**: compositional shape analysis via bi-abduction; Facebook Infer as the industrial-scale instance of typed-mode inference on real code.
- **O'Hearn 2019**: separation logic and incorrectness logic.
- **Zilberstein, Saliling & Silva 2024** ([arXiv:2305.04842](https://arxiv.org/abs/2305.04842)): Outcome Separation Logic; tri-abduction for branch composition.
- **Bylander et al. 1991**: abductive computational complexity.
