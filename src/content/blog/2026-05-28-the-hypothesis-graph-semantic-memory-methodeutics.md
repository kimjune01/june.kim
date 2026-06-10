---
variant: post-paper
autonumber: true
title: "The Hypothesis Graph: Semantic Memory Written by Methodeutics"
subtitle: "Merit attaches to the work, not the doer."
tags: methodology, epistemology, coding
---

*[Download PDF](/assets/methodeutic-harness-paper.pdf) · arxiv-shape preprint, rebuilt from this source. · Receipts: [the bench run](https://github.com/kimjune01/swebench-pro) · [the determinacy audit](https://github.com/kimjune01/swebench-pro-audit) · [the mechanism experiment](https://github.com/kimjune01/hygraph-mechanism), each reproducible from its own committed artifacts.*

## Abstract {-}

We report a witnessed, replayable case. On a single undiagnosed, guaranteed-uncontaminated open-source bug, a language-model agent built a sound, general fix, verified on a clean build, with every load-bearing reasoning step recorded and re-runnable by a stranger. The fix existed nowhere in the agent's training corpus and the conditions were built to rule out direct recall, so the case is existence-grade evidence of discovery rather than recall: the agent built knowledge it did not already contain, the thing Sutton's challenge asks of it. The instrument that makes the case checkable is the **hypothesis graph** — a typed, persistent semantic memory whose nodes are falsifiable hypotheses bound to recorded trials and whose edges are kill conditions, written by **methodeutics**, Peirce's abduction, deduction, and induction encoded as a mechanical pipeline with a deterministic gate that no model arbitrates. It is a discipline for inquiry on epistemic grounds inherited from the pragmatists, and it turns a machine's answer into a sequence of falsifiable commitments a hostile reader replays instead of a verdict they are asked to trust. We also ran the field's standard benchmark, SWE-bench Pro, and scored 95.3%; a resolve rate compresses hundreds of inquiries into one number that is barely legible and teaches nothing, and controlled ablations and a determinacy audit show the benchmark is structurally blind to the mechanism the case demonstrates. The number is the least insightful artifact here. The epistemic unit that is legible is the replayable work product, and the norm this paper declares follows from it: merit attaches to the work, not the doer.

## Introduction {#introduction}

> We want AI agents that can discover like we can, not which contain what we have discovered.
>
> — Richard S. Sutton, *The Bitter Lesson* (2019)

In 2026, reasoning is the capability frontier for large language models, and coding is its definitive measure: a patch passes its tests or it does not. This paper is about where an agent's reasoning should live so that it can be checked. The proposal is a data structure at the harness layer. The hypothesis graph is a typed semantic memory of an inquiry in progress: candidate causes as nodes, falsification conditions as edges, every belief carrying the mode that earned it and the trial that can re-earn it. The model does the reasoning, as it always did. The structure holds that reasoning, types it, and keeps it replayable after the context window that produced it is gone.

What this paper reports is what holding reasoning that way buys. Pattern-matching a bug a model has seen before is old news, and no benchmark score changes that. The contribution is one level down: a machine producing not just an answer but an **attested chain of mechanical reasoning** to reach it — each step a node bound to a recorded trial, each belief typed by the mode that earned it, the whole chain a thing a stranger replays rather than a verdict they are asked to trust. And on a problem the model has never seen, that chain terminates in a fix that existed nowhere until the inquiry built it: discovery, not recall. The rest of the paper is the argument that this is real, that it survives a hostile reader, and that the field's standard instrument cannot see it.

Two traditions approached this substrate from opposite sides and stalled. LLM-agent work keeps rebuilding harness memory under the name "memory systems," citing the post-2020 literature and missing the lineage that already worked the problem. Cognitive architecture built that lineage: Soar (Laird 1987) and ACT-R defined the typed semantic / procedural / episodic memory and the mechanical operations over it, but for want of a general inference engine at the core, it stayed a research program. This paper marries them. The hygraph fills the semantic-memory slot (`smem`); the pipeline-stage skills fill procedural memory (`pmem`); the per-run trajectories fill episodic memory (`epmem`). The LLM plugs in as the inference component, a reasoner inside a method it does not own.

Neither tradition built the missing piece: a place to put hypotheses *under consideration*. Prose context is lossy, skill libraries store verified code rather than falsifiable claims, and vector retrieval indexes established chunks. The hygraph is that place, and it is just a markdown file: no RAG, no database, zero dependencies (§(hygraph)).

We tested the assembly the way the field tests everything: on the standard ruler. SWE-bench Pro is the contamination-resistant benchmark OpenAI now recommends in place of the saturated Verified. We ran the whole eligible public set under one frozen harness and the official grader, twice, with the entire model pair swapped between runs, and committed a receipt for every instance: trajectory, hypothesis graph, captured diff, gate trace, cost ledger (§(setup)). The numbers came back high: 95.3% with a frontier pair, 93.1% with the entire model pair swapped to open weights (§(results)).

The high numbers do not credit the mechanism. An oracle bracket, a prompt ablation, a whole-stage deletion, and a determinacy audit of all 728 tasks converge on one verdict: on this bench, the lift belongs to the gate's access to a cheap and trustworthy oracle, plus generic agent engineering; the typed inquiry the harness exists to encode is structurally unmeasurable here (§(attribution), §(audit)). The bench hands over the specification on roughly three quarters of its tasks, so there is nothing to diagnose, and grades an unstated authorial choice on a proven tenth, which no diagnosis can recover. The nulls are not a failure of the experiment. They are the predicted signature of a diagnosis mechanism pointed at a bench with no diagnosis in it.

Benchmark performance is widely treated as a prerequisite for legibility, and it may still be one for reach. But a resolve rate is the least insightful artifact this work produced: a number that compresses 728 inquiries into one digit pair cannot surprise anyone into a hypothesis. It is also a depreciating asset. A benchmark score rests on trust in the benchmark, and that trust is being withdrawn industry-wide as saturated rulers turn out full of flawed tests, OpenAI's own audit retiring Verified for exactly that reason; the number is worth less each quarter it ages. A replayed trace is the opposite kind of asset, its warrant does not decay, because a stranger re-runs it instead of trusting it. A live example that can be abducted on can, and the work eventually produced one (§(right-regime)): an open, maintainer-stuck compiler bug, guaranteed uncontaminated, where the graph arm's fix generalizes and the minimal arm's does not, the difference invisible to every test the project ships and settled by a receipt any reader can rerun. The fix it produced existed nowhere in the corpus — output outside the convex hull of the model's training distribution, witnessed discovery rather than recall, a creative act by some definition, and the nearest thing this work offers to discharging the epigraph: an agent that discovers, not one that contains what we have already discovered. The bench bought attention. The example carries the insight.

So the paper now claims, in order of confidence — though importance runs the other way, the artifact being the most certain and the least interesting, the mechanism finding the least certain and the point:

1. **An artifact**: the bench numbers, bounded precisely (public split, source-only capture, official grader, gate access to the visible tests), with receipts that survive a hostile reader (§(results)).
2. **An attribution**: where the lift actually lives, channel by channel, including the one our own design held constant and therefore could not see at first (§(attribution)).
3. **An instrument finding**: SWE-bench Pro is a spec-conformance bench with a measurable underdetermined fraction, and no benchmark of that shape can measure typed inquiry (§(audit)).
4. **A mechanism finding, existence-grade and the one that matters most**: in the regime a bench cannot construct (undiagnosed, uncontaminated, no cheap oracle), the hygraph produces a fix that existed nowhere in the corpus, a witnessed instance of reasoning beyond corpus synthesis. Rare in frequency, decisive in kind, and visible precisely where every benchmark instrument is blind: fix generality, soundness, and a reasoning trace auditable at arbitrary depth (§(right-regime)).
5. **A reframe** this lineage was always pointing at: agents should not be trusted; they should be accountable, and the hygraph is the ledger that makes them so (§(discussion)).

The paper reads at two levels, and saying so up front is cheaper than letting a reader discover it mid-argument. On its surface it is an AI-systems contribution: it fills one of the three memory slots of a cognitive architecture, the semantic one, for coding agents, and reports what happened when the assembly met the standard benchmark. At its foundation it is epistemology: a position on what makes a claim checkable, what agents owe the people who act on their outputs, and where merit attaches. The surface reading is the smaller one, and the paper is structured so that the foundation survives exactly where the surface result nulls.

This work is unincentivized public research. Its only standing is the auditable trail: every claim above ties to a committed receipt, the nulls included.

## The hypothesis graph {#hygraph}

The hygraph is the focal object of this paper, so we define it before the procedure that writes it.

A **node** is a claim bound to a trial: a hypothesis, the perturbation that tests it stated as an exact command, the observed outcome, and a credence typed by the reasoning mode that established it. An **edge** is generated by a kill condition: the manner of a hypothesis's death names the next hypothesis, so the structure is self-extending, with no external controller deciding where to look. The **soundness invariant** is replayability: every node must be reconstructible from its recorded trial by someone who does not trust the author. The operations of the type are perturb-and-classify, generate-edge-from-kill, prune, and the load-bearing one, replay.

What is novel is not the nodes but the edge semantics. A search tree finds; a proof tree justifies. The hygraph is both at once, because the search path *is* the justification: every step was a trial. It sits at the confluence of three older lineages — truth-maintenance systems (de Kleer 1986), sequential experimental design (Wald 1947; Vovk & Wang 2021), and abstract argumentation (Dung 1995) — and the pair none of them combine is kills that generate the next experiment and replayability as a first-class invariant (§(lineage)).

The scope must be stated honestly or the claim dissolves. This is the data structure for *testable* inquiry, and its entire power is the perturbation surface. Strip the ability to poke the system and read an outcome, and the same shape degrades into a plausibility tree, which is the confabulation failure mode it exists to prevent. It is also not how minds run: minds reason fast, compressive, intuitive, mostly without explicit perturbation. The hygraph is the verifiable serialization reasoning compiles to in order to be checked by someone who does not trust you. Proof is to intuition as the hygraph is to inquiry: not the thinking, the residue of the thinking that survives a stranger's replay.

In the memory typology, this is the `smem`: persistent, typed, queryable, and owned by the harness rather than the model. The graph in this work is one markdown file per inquiry. It was never the bottleneck at any repo size in the eligible set, a deflationary point against the field's reflex to reach for vector stores and graph databases where none is needed (§(limitations)).

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
  <img src="/assets/methodeutic-harness.svg" alt="The SWE-bench Pro harness. Inquire builds the hypothesis graph (smem) by abduction, deduction, and induction, typing each node by the mode that established it; implement reads the surviving hypotheses, derives a patch under cross-family adversarial challenge, and emits it to attest; attest runs the official harness, emits a binary verdict and a re-entry route, and writes a kill or witness classification back to the graph; the deterministic gate routes on the verdict, the route, attempt count, and budget. Off-box capture commits the per-instance provenance artifact (trajectories, graph, diff, gate trace, grader output, cost ledger) to the public repo." />
  <figcaption><strong>Figure.</strong> The harness used on SWE-bench Pro. <code>inquire</code> builds the hygraph by Peirce's three inquiry modes, typing each node by mode; <code>implement</code> writes the patch, <code>attest</code> verifies; the gate is finite-state with no model call; the outer loop re-enters <code>inquire</code> with an updated graph rather than retrying the patch.</figcaption>
</figure>

Throughout, the three stages are `inquire`, `implement`, and `attest`; the frozen artifact's code, file paths, and route literals spell them `recon`, `craft`, and `audit`.

### The inquiry frame {#inquiry-frame}

We recast each SWE-bench instance as an inquiry on an engineered system: a failure trace, a codebase, a root cause to find, and an intervention that must not regress the rest of the system. Code is the right substrate for the hygraph because it combines three properties that other inquiry domains rarely combine:

- **Reproducible**: same input yields same output, modulo controlled nondeterminism
- **Deterministic**: causal lines from input to behavior are mechanical
- **Perturbable**: single-line and single-function diffs are cheap to apply and fully observable

Because those three hold together, hypotheses about code can be tested by cheap mechanical perturbations and falsified by deterministic predicates; kill conditions are not approximations; they are executions.

One instance settles the benchmark predicate in this regime. In code the per-instance response is mechanically observable, so a single passing test on a captured diff is a complete verdict that the diff satisfies the executable benchmark predicate for that instance. That verdict speaks to the predicate alone: behaviors it doesn't cover are out of scope, a boundary that §(right-regime) shows is exactly where the interesting differences live. The paper therefore reports counts, denominators, and per-repo breakdowns rather than confidence intervals: per-instance verdicts are exact, and aggregating them is bookkeeping.

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

**Worked example.** A representative first-pass win on SWE-bench Pro: `flipt-io/flipt` instance `292fdaca`, scored `WIN` ("official RESOLVED") in `runs/scored/run.jsonl`, with the `inquire`, `implement`, and `attest` transcripts and the captured patch committed under `runs/scored/artifacts.tar.zst`. The failing tests will not compile. Abduction does the first work, and here it is just generating the diff: the gap between what the tests demand and what the code supplies. The suite wants `cfg.Version == "1.0"`; the struct has no such field, the schema no such property, the testdata no such files. That gap *is* the hypothesis, *the versioning feature was never implemented*, and it names its own patch in four pieces. The committed node records where that drill-down concluded:

```markdown
H₀: the configuration-versioning feature was never implemented
  Mode: deduction.  Confidence: 99%.
  Observation: compile fails, `cfg.Version undefined` at config_test.go:450.
  Evidence: Config struct has no Version field (config.go:40-48); the JSON
    schema lists no version property (flipt.schema.json:8-34); the tests
    expect cfg.Version == "1.0" and reject "2.0"; testdata/version/*.yml absent.
  Predicted fix: add the field, a validate() that rejects any non-"1.0"
    version, the schema property, and the two testdata files.
  Falsification: if those four changes do not turn the tests green, H₀ is wrong.
```

The graph is a single strong node, and that shape is the bench talking. The gold tests name the missing surface, so abduction generates the diff in one move and needs no fan of competing hypotheses. We read this at the time as the common shape of the workload. It was the first appearance of the instrument finding this paper now centers: a task that hands over its specification leaves the smem nothing to hold (§(audit)).

Implement writes the four-part fix, and the blind challenger earns its separation here. It caught that the first draft never invoked `Config.validate()`, because `Load` only runs the validators attached to fields; implement then added the explicit call. The deterministic gate reads the binary test verdict and nothing else:

```
=== GATE F2P 2/2 PASSED ===   TestJSONSchema ✅   TestLoad ✅
PASS_TO_PASS regressions: none
VERDICT: RESOLVED   RE-ENTER: none
```

No model arbitrates that verdict, and `attest` re-runs it against the live patch (two files, +80 lines) before recording the win. `RE-ENTER: none` is the first pass closing the frontier, which is how roughly 93% of wins resolve (§(results)).

That committed node is a conclusion, and an inquiry that reaches one rarely runs straight. Following the same `inquire` skill on an unrelated bug, a single hypothesis flips across all three modes and a kill before it settles:

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

### Deterministic gating {#gating}

The gate is the driver routing on two lines `attest` prints, not a model call. `attest` ends every pass with `VERDICT: <RESOLVED|NOT_RESOLVED|PARTIAL>` and `RE-ENTER: <inquire|implement|none>`, assigned from a fixed table (`skills/audit/skill.md`): all `FAIL_TO_PASS` green with no regression resolves and re-enters nothing; a regression routes to `implement` to narrow the fix; a partial or ineffective patch routes to `inquire` to re-diagnose; an empty patch routes to `implement`. Because the code under test is deterministic, one test run settles each predicate; the verdict is dispositive in a single read and no sequential-evidence accumulator is needed.

This cheap, trustworthy verdict has a second role beyond attestation, and the attribution program found it load-bearing: it is what lets blind try-and-check substitute for aimed diagnostic perturbation, and on the public split of this bench it is what lets a no-diagnosis arm match the full pipeline (§(attribution)).

The driver reads those two lines and routes the next stage, bounded by an attempt budget. In pseudocode (full parser: [`driver/rung5_driver.py`](https://github.com/kimjune01/swebench-pro/blob/main/driver/rung5_driver.py)):

```text
verdict ← attest's last VERDICT line    # RESOLVED | NOT_RESOLVED | PARTIAL
route   ← attest's last RE-ENTER line   # inquire | implement | none

if verdict is RESOLVED and route is none:
    stop (win)
else if attempts have reached the budget:
    stop (budget exhausted)
else:
    re-enter the stage named by route
```

One harness-enforced override applies: a regression gets a single narrow `implement` attempt, and if the next pass routes to `implement` again the driver overrides it to `inquire`. No stage decides its own termination; the verdict and route are mechanical, the budget is fixed, and re-running the same `attest` output through the driver yields the same routing.

One distinction the gate makes sharp. The `attest` agent's `VERDICT` is its reading of the in-container test gate, and it serves only to route the loop. The bench score is computed separately: the official SWE-bench grader (`driver/pro_pilot.py:official_grade`) is re-run on the captured patch after the loop ends, and the headline 694/728 is that grader's verdict, not the agent's. A misread route can waste a re-entry; it cannot manufacture a scored win. No model sits in the routing gate, and no model scores the bench.

### Outer-loop iteration {#outer-loop}

`attest` failures do not retry the patch. They route back to `inquire` with the trajectory classification and the updated graph. `implement` sees a different node-set on re-entry rather than the same node twice. The recoveries resume from a compressed, kill-marked checkpoint rather than a re-read transcript, so the loop does not re-propose dead branches or re-ingest a stale, sometimes near-context-limit window. This retryability is a role the smem plays that prose context cannot: a save-checkpoint for the outer loop. The attempt budget per instance is bounded; budget exhaustion counts as a clean termination without convergence. No peek at held-out tests at any point in the loop.



## Procedure {#setup}

Every choice follows one goal: making the run attributable, so a skeptic can pin the result on the harness or rule it out. The disciplines live as receipts in the repository rather than as prose here: preregistration and an annotated freeze tag (`PREREGISTRATION.md`), eligibility against documented bench defects (`KNOWN_BAD.md`), official-grader-only verdicts, infrastructure fault classes predeclared with invariants so recovery cannot become a re-roll lever, per-instance provenance (trajectory, hypothesis graph, captured diff, gate trace, cost ledger), and a doubt-by-doubt guide for hostile readers (`FOR_SKEPTICS.md`, `OBJECTIONS.md`). Two benches ran under one frozen harness: saturated Verified as the porting baseline (426/438 eligible, Zenodo-DOI'd, companion repo `swebench-verified`) and contamination-resistant Pro as the primary surface. The operational story, including everything that went wrong on the way to an honest number, is the companion field guide [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro).

### Models and the oracle boundary {#models}

No training, no fine-tuning, no learned weights in the harness. Each stage invokes a vendor's shipped agentic CLI (Claude Code for the Sonnet 4.5 generator, codex for the GPT-5.5 challenger, Cursor in the open-weight run), so the harness is a typed meta-loop over off-the-shelf agents, owning only the stage contracts, the hygraph, and the gate between them. The generator ran with extended thinking on; the challenger arbitrated with reasoning off, a point against a model-deliberation reading of the gate. For each scored instance the loop reads only that instance's own artifacts; no other instance's graphs, trajectories, or solutions enter the context.

The boundary that matters most: on the public split the bench's `FAIL_TO_PASS` tests are visible, and the frozen harness's in-container gate executes them as its stop signal (their names as budget control, their bodies never in the model's prompt). The standardized leaderboard scaffold is denied them by design. That difference is the dominant attribution channel (§(oracle-bracket)), and the held-out split removes even the names, so nothing in this paper's public-split numbers transfers to the private set.

### Open-weight robustness run {#open-weight-run}

The same frozen harness, the model pair swapped wholesale to open weights: Composer 2.5 ([per Cursor](https://cursor.com/blog/composer-2-5), a fine-tune of Moonshot's open-weight Kimi K2.5) generating, Gemini Flash 3.5 challenging, the cross-family adversarial property (§(blind-blind)) preserved.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:13em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Pro, same frozen harness</th><th style="background:#f0f0f0">Frontier pair</th><th style="background:#f0f0f0">Open-weight pair</th></tr></thead>
<tr><td>Generator</td><td>Sonnet 4.5</td><td>Composer 2.5 (Kimi K2.5)</td></tr>
<tr><td>Challenger</td><td>GPT-5.5</td><td>Gemini Flash 3.5</td></tr>
<tr><td>Resolved (/728)</td><td>694 = 95.3%</td><td>678 = 93.1%</td></tr>
<tr><td>Median wall-clock</td><td>12.8 min</td><td>8.4 min</td></tr></table>

The raw open-weight rate is partly recall: a gold-overlap audit ([`gold_divergence.py`](https://github.com/kimjune01/swebench-pro/blob/main/driver/gold_divergence.py)) finds ~23% of its wins reproduce gold's changed lines, against ~2% for the frontier pair, and a weaker model reproducing the human patch more often than stronger ones is the signature of recall, not capability. Discount the whole near-gold tail and the harness still carries the open-weight model to roughly three-quarters genuine resolve. The run reads as portability, never capability, and ships under the same provenance contract in the same bundle.

## Results: the number, bounded {#results}

### What the number is {#tables}

**694 / 728 = 95.3%** with the frontier pair and **678 / 728 = 93.1%** with the open-weight pair, on the whole eligible public set, 0 incomplete, under the official grader, at frozen tags `prereg-pro-v1` and `prereg-pro-v1-cheap`. The texture is committed, not narrated: per-repo tables (ten of eleven repos above 92%), the first-pass/re-entry split (~93% of trajectory-captured wins resolve on the first pass), the development-overfit check (the development language resolves *lower* than the never-touched languages), re-grades that reproduce (6/6 frontier cross-language, 60/60 open-weight stratified, 0 flips, ~$3 per WIN to audit), and all 34 losses carrying non-empty rejected patches. Start at the repository scoreboard ([github.com/kimjune01/swebench-pro](https://github.com/kimjune01/swebench-pro)).

*OSS deployment trace.* **81 PRs merged across 73 cold repositories** at a **50.6%** merge rate under adversarial maintainer grading: agent-selected issues, agent-authored patches, agent-submitted PRs, zero human keystrokes in any diff, and only ~8 of 79 closures rejections on the merits. The ledger stays GraphQL-verifiable (`pr-receipts.jsonl`); ~385 hypothesis graphs from the same campaign are public at [`kimjune01/sweep/repo-hypotheses/`](https://github.com/kimjune01/sweep); the narrative is [Speedrunning Open Source](/speedrunning-open-source).

Two receipts, two independent attestors:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:9.5em"><col><col style="width:13em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Receipt</th><th style="background:#f0f0f0">Evidence</th><th style="background:#f0f0f0">Attestor</th></tr></thead>
<tr><td>Pro (preregistered)</td><td>terminal: 694 / 728 = 95.3%, 0 incomplete, whole eligible set graded</td><td>Scale's official grader, re-runs the committed patch</td></tr>
<tr><td>OSS PR merge rate</td><td>81 merged across 73 cold repos, 50.6%, GraphQL-verifiable</td><td>adversarial maintainers who merged</td></tr></table>

We do not attest; the receipts do. No method documented in our comparative search (§(search)) has demonstrated, with equivalent receipts, a higher SWE-bench Pro official-grader resolve rate under one frozen harness. That claim is about the artifact and its auditability, and it survives the attribution below. What does not survive is any reading of the rate as evidence for the method.

### What the number is not {#central-comparison}

<figure>
  <img src="/assets/methodeutic-attribution.svg" alt="Grouped bar chart of SWE-bench Pro resolve rate. Three bare models on the standardized SWE-Agent scaffold: Sonnet 4.5 at 43.6 percent, GPT-5.5 at 58.6 percent, Opus 4.7 at 64.3 percent. Two configurations of this methodeutic harness: open-weight at 93.1 percent, frontier at 95.3 percent. The harness bars stand about thirty points above the tallest bare-model bar." />
  <figcaption><strong>Figure.</strong> Resolve rate on SWE-bench Pro: bare models on the standardized scaffold (official <a href="https://labs.scale.com/leaderboard/swe_bench_pro_public">Scale board</a>) beside this harness's two runs. The bars are not the same game. The harness's gate executes the public split's visible tests as its stop signal; the standardized scaffold is denied them by design. The oracle bracket (§(oracle-bracket)) attributes nearly the whole visual gap to that access. The chart scales the artifact; it ranks nothing.</figcaption>
</figure>

Three things the 95.3% is not, stated before the attribution rather than after:

- **Not a leaderboard number.** The board ranks models through one fixed scaffold; this run holds the model roughly fixed and rebuilds the scaffold. A harness number has no slot on a model board by construction.
- **Not a held-out number.** The public split is the audition; Pro's private split removes even the test names, so the gate must go blind there, and nothing in this paper predicts that result.
- **Not an isolation of the method.** The within-pass `implement`→gate refinement loop, the vendor inner agents, the thinking-on generator config, and the gate's oracle access all ride along. The next section separates them.

## Attribution: where the lift lives {#attribution}

The attribution decomposes the gap channel by channel. Each cut is preregistered or receipt-committed in the repository, including one retracted estimate and its worklog trail; the paper keeps the findings.

<table style="max-width:760px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:17em"><col style="width:15em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Channel</th><th style="background:#f0f0f0">Cut</th><th style="background:#f0f0f0">Effect on Pro resolve</th></tr></thead>
<tr><td>Gate access to the visible tests</td><td>oracle bracket, n=50</td><td><strong>~46 points</strong> (50% floor → 96% ceiling)</td></tr>
<tr><td>Peircean prompt vocabulary</td><td>M vs G vs T, n=38/36</td><td><strong>null</strong> (CIs straddle zero)</td></tr>
<tr><td>Directed diagnostic perturbation</td><td>deprived arm, n=110</td><td>+0.105 on underdetermined-cause stratum only; threshold-level</td></tr>
<tr><td>Entire diagnosis stage (the smem)</td><td>craft-only, n=34</td><td><strong>~1 point</strong>, resting on two instances</td></tr>
<tr><td>Model pair (frontier → open-weight)</td><td>pair swap, n=728</td><td>2.2 points raw; ~17–22 genuine after recall discount</td></tr>
</table>

### The oracle bracket {#oracle-bracket}

The largest channel is the one the original design held constant and therefore could not see. On a preregistered 50-instance random sample, an implement-only loop with no oracle access floors at **50%**; restoring the bench's tests for the gate to iterate against raises the ceiling to **96%** ([`PREREGISTRATION-baseline-replication.md`](https://github.com/kimjune01/swebench-pro/blob/main/docs/PREREGISTRATION-baseline-replication.md), [the bracket](https://github.com/kimjune01/swebench-pro/blob/main/docs/HYPOTHESIS_GRAPH-pro-harness.md)). Forty-six points sit between those arms, bought by oracle access, not by the same models reasoning harder; the floor sits near the bare-model board scores (43.6–64.3%), the ceiling at the headline. The companion posts reached this conclusion first ([Precisely Wrong](/type-iii-error), [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro)). The remaining ablations ask what the structure adds given the oracle. Channel by channel: almost nothing.

### The prompt is inert {#prompt-ablation}

Harness byte-identical, only the diagnosis prompt varied: methodeutic **M**, a generic-rigor steelman **G** authored by a third-party model told to win, and a task-only floor **T**. Scored on diagnosis recall against the gold patch, recon-only, the arms are indistinguishable (M − G −0.012, G − T +0.035, both CIs straddling zero; n=38/36). The methodeutic vocabulary reads no better than generic rigor, and generic rigor no better than the bare task; prompt wording is excluded as the channel.

### Directed perturbation, and the gate's second role {#perturbation}

One channel bites, conditionally. Cutting the aimed diagnostic probe costs +0.105 on issues whose cause is *not* statically determined from the text (threshold-level: the preregistered frame clears its bar, the stricter McNemar lands just over at p = 0.057) and nothing on issues where it is, with eleven gate-confirmed existence cases and the predicted specificity by cause class carrying more weight than the borderline aggregate. An earlier, larger estimate was retracted as infrastructure contamination; the full trail is in the worklog.

Why does removing directed perturbation cost so little? Because the deterministic gate substitutes, in its second role. Directed perturbation's only advantage is query efficiency: one aimed experiment instead of many blind ones to tell rival hypotheses apart. Blind try-and-check gathers the same information by trial, but only if each trial is cheap and its result trustworthy, which is exactly what the gate supplies. The twist worth stating plainly: the gate was held constant across both arms as a controlled-for covariate, so the very thing we fixed to keep the ablation clean is the channel that routes around the cut. It sharpens into a falsifiable differential prediction: degrade the gate (flaky tests, no oracle, expensive evaluation) while perturbation stays absent, and the deprived arm should worsen more. The regime that flips the result is gate-present versus gate-absent. §(right-regime) runs it.

### Pricing the diagnosis stage {#craft-only}

If the gate substitutes for the probe inside diagnosis, does it substitute for the whole stage? The **craft-only** arm deletes `recon` entirely: no graph, no typed inquiry; `implement` gets the raw problem statement and the failing tests. Determined causes: Δ = +0.000 (n=18). Underdetermined: Δ = +0.062 (n=16), the entire effect one instance, the two clear divergences splitting in opposite directions (no diagnosis beat a wrong one on one instance and lost to a good one on another). Reweighted to the population, craft-only lands near **94%** against the full harness's 95.3%. On this bench, the smem is redundant on the bulk and matters, if at all, on a sliver the benchmark cannot resolve.

### The attribution verdict {#attribution-verdict}

Sum the channels. The oracle buys ~46 points. The vocabulary buys nothing. The aimed probe buys a threshold-level sliver on one stratum. The whole diagnosis stage prices at about one point. The model pair, the lever the leaderboards exist to rank, moves the raw rate two points. So the answer to *how well does the method work* is: not on the most popular coding bench, because the bottleneck there is not diagnosis. Why the bench has no diagnosis in it has a mechanical answer (§(audit)), and where the bottleneck *is* diagnosis is the world (§(right-regime)).

## The instrument: a determinacy audit of SWE-bench Pro {#audit}

A benchmark score is only as meaningful as the determinacy of its tasks: if the materials a solver receives do not pin the behavior the hidden test grades, passing is not evidence of solving the stated problem but of recovering an unstated choice by other means. We audited all **728 public Pro tasks** against that standard, as a companion artifact with its own receipts ([github.com/kimjune01/swebench-pro-audit](https://github.com/kimjune01/swebench-pro-audit)): every graded behavior checked against the prose and the live codebase at the base commit, grep-certified witnesses, blind two-family adversarial verification for the judgment-bearing tier. The audit is self-authored and costs nothing epistemically to cite: each row is a pointer to an ambiguity a hostile reader re-derives by grep, nothing taken on our word.

<table style="max-width:740px; margin:1em auto; font-size:14px;">
<colgroup><col><col style="width:6em"><col style="width:6em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Label</th><th style="background:#f0f0f0; text-align:right">count</th><th style="background:#f0f0f0; text-align:right">of 728</th></tr></thead>
<tr><td>Spec-given: ENTAILED (478) + DETERMINED-codebase (78)</td><td style="text-align:right">556</td><td style="text-align:right">77%</td></tr>
<tr><td><strong>Proven underdetermined</strong>: mechanical spine (83, grep-re-derivable) + two-expert splits (26, adversarially verified)</td><td style="text-align:right">109</td><td style="text-align:right">15.0%</td></tr>
<tr><td>Screen-flagged, rater-pending, excluded from every claim</td><td style="text-align:right">63</td><td style="text-align:right">9%</td></tr>
<tr><td>Gold-fails-grader / feature-mismatch defects</td><td style="text-align:right">3 / ≥1</td><td style="text-align:right"></td></tr>
</table>

The audit attributes the attribution. Take the two tiers together:

- On the **~77% that is spec-given** (entailed plus determined-codebase), there is no hidden cause. The task is conformance: transcribe the handed requirements into the named surface. Abduction has nothing to abduce, the hygraph degenerates to the single transcription node the flipt worked example showed (§(recon-output)), and a gate-equipped iteration loop is the right tool, which is why deleting the diagnosis stage cost nothing there.
- On the **proven 11.4–15.0% that is underdetermined**, the information the test grades is absent from everything the solver legitimately reads. No diagnosis, however typed, can recover what is not there; those instances are a lottery, and a lottery rewards recall, guessing, or oracle access, never inquiry.

(A terminology guard, since the same word does double duty: the ablation strata of §(perturbation) classify *cause*-determinacy in the issue text, the audit classifies *task*-determinacy in the materials; the first asks how hard the diagnosis is, the second whether there is one at all.)

The conclusion is structural, and it indicts no one's honesty: a spec-conformance bench with a cheap visible oracle and a measurable lottery fraction cannot measure a diagnosis mechanism, whoever runs it. The nulls of §(attribution) are what a true mechanism looks like when measured on an instrument that cannot see it.

What the audit says about the bench's own standards is a side note here, and that work is already done elsewhere for readers who want to dig: the feature-mismatch class where prose and graded behavior are simply disjoint (`flipt-io_358e13bf` asks for snapshot-cache deletion; the test grades a CSRF default), the **specification lottery** reading (a raw Pro percentage conflates solving the stated problem with recovering the author's unstated choice, and wants a determinacy-aware denominator), and the portable tool that re-runs the whole audit on any SWE-bench-shaped dataset ([**determinacy**](https://github.com/kimjune01/determinacy); SWE-rebench already run, only the grep-provable floor claimed). This paper needs only the fraction that explains its nulls.

## The right instrument {#right-regime}

### The regime and the reconstruction

The gate-compensation mechanism predicts where the smem should matter: where the oracle is expensive or absent and the cause is genuinely hidden. That regime is not a corner case; it is most of software. Every issue tracker is a backlog of undiagnosed problems, each filed by someone who wanted it fixed and waiting on the one expensive step the bench never exercises; flux #1613 sat for weeks at 41 comments with its maintainers stuck, which is what undiagnosed looks like in the wild. We had already been running in this regime: the deployment lineage (§(results)) works real filed issues: no handed spec (the symptom is whatever a bug reporter wrote), no cheap oracle at solve time (the grader is a human maintainer), real diagnosis required (the cause is hidden in a cold codebase). The mechanism experiment ([github.com/kimjune01/hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism)) reconstructs that regime under control and runs the ablation Pro made meaningless: same model, same loop, the methodology the only variable, an existence-proof burden rather than a population rate.

The design earns three guards Pro taught us. The oracle is the issue's *essence*, authored from the upstream issue text and graded red-at-base / green-on-gold, never the PR's shipped test (the pipeline's own TDD homework, which would re-create Pro's over-credit) and never a self-authored check (self-audit went 4/4 false-green against the real grader in prior work). The baseline is an adapted mini-SWE-agent, the industry-recognized minimal scaffold, with its verbatim prompts. And the graph is regenerated blind by a model whose training cutoff predates the fix, because the graph is the treatment and generator contamination does not cancel in the differential the way craft-model contamination does.

### Nine pilots: eight nulls, one divergence

The score is honest and uncomfortable in both directions:

- **Eight nulls.** On bugs from the merged-PR pool and beyond it, the minimal baseline kept succeeding: a 5-line CLI fix in 91 seconds, the deepest graph in the pool out-reasoned in two minutes, a real clear()/ingestion data race in an LSM storage engine that the pipeline itself had skipped as too complex, a 41-comment refinement-type-checker bug. Two findings explain the run of nulls without excusing them. First, a **selection artifact**: the deployment pipeline's own triage skill scores reproducibility up and fast-paths easy bugs around the graph (its rule, verbatim: "a 1-line fix with a confirmed reproducer doesn't need a hypothesis graph"), so the merged pool is precisely the subset where the pipeline says the graph is unneeded. Second, **baseline reach**: a frontier model in a minimal loop now diagnoses and fixes most reproducible bugs unaided, so the band where diagnostic structure can change a pass/fail verdict is being eaten from below by model capability and routed around from above by triage.
- **One audited divergence.** flux-rs/flux #1613, an open, maintainer-stuck composite-sort bug in a refinement type checker, 41 comments, no fix. Both arms produced patches that verify the reported program and pass the full 965-test compiletest suite with zero failures; by every test the project ships, both fixes are done. They are not the same fix. The minimal arm gated its repair on a shape coincidence (an ADT carrying a function-sort field), incidental to validity. The graph arm dumped the solver constraints, located the live obligation (a `FoldLocal` equality at the setter call site), and repaired the cause: track the field origin of a mutable borrow and write the callee's post-state back to the borrowed place. A receipt discriminates where the suite cannot: a structurally identical valid program with integer components instead of a function component. The graph arm's fix verifies it; the minimal arm's fix rejects it with the original error. Both correctly reject an unsound twin, so the minimal fix is not broken; it is over-narrow, a confident false positive the project's own tests can never catch. The graph ran 19 nodes, recorded three of its own corrections in-trail (a stale-binary catch, a first fix it refuted with its own probe, an over-broad propagation the suite caught), and every load-bearing node was replayed on a pristine base build before any of this was claimed. The hardened fix is in front of the flux maintainers with the residual honestly flagged, and the full trail is public at tag `flux-1613-trail-v1`. A maintainer merge would close the case with the same certification this experiment treats as gold everywhere else: the merge is the attestation. Until it lands, the case stands on the replayed receipts alone, and the hunt for further cases continues under the preregistered protocol.

### What the existence proof establishes

An existence proof needs one witness, and flux #1613 is it: there exists a real, maintainer-stuck bug on which the methodology produced a materially better, still-sound fix than a strong minimal agent on the same model, with reasoning auditable at arbitrary depth. No rate is claimed; the claim does not need one. What the witness fixes is the shape of the mechanism's value: the advantage did not appear as pass-versus-fail on the original bug, it appeared as correctness invisible to the oracle, settled only by a receipt. That is also the experiment's own lesson applied to itself: eight loops ran as inductions with no per-loop deductive rung, so every null retrofitted into a new abduction instead of testing one; the program now preregisters one sentence per loop (testing X, predict Y, refuted by Z) before any arm runs (`METHODOLOGY-preregistration.md`).

## Discussion {#discussion}

### What survives of the bench result

The artifact stands, bounded. A frozen, fully auditable harness resolved 95.3% of public Pro under the official grader, and the same structure, the entire model pair swapped to open weights, carried 93.1%. The receipts discipline (preregistration, freeze, fault classes with invariants, official-grader-only verdicts, per-instance provenance) is what lets a null be published attributed rather than buried, which is the strongest argument for the discipline we know how to make. These nulls publish *attributed*: each arrives with the mechanism that produced it (the gate compensating, the spec handed over, the lottery fraction). An unexplained null says stop; an attributed null says where to point the next instrument.

Does the Peircean framing do any real work, or is it decoration? On this bench, the honest answer is now: as *rhetoric*, decoration (§(prompt-ablation)); as *protocol*, load-bearing. The prompt ablation measured whether the vocabulary makes a single diagnosis smarter, and it does not. What it could not measure is interop. A hygraph written in one context window must be read in another, by a different model, a parallel agent, or a human auditor, and the mode labels are what make a node interpretable without the context that birthed it: abduction marks a belief as proposed-untested, induction marks it as test-backed, and the credence cap travels with the type. Loose vocabulary produces graphs only their author's window can interpret, and those die with it. The Peircean typing is the wire format that lets the smem be shared across compactions, across agents, and across the trust boundary to the auditor, and the common vocabulary is the protocol for verifying each other's work: a peer that reads `induction, test-backed, here is the command` can rerun the command, where a peer that reads loose prose can only believe it or not.

This resolves the apparent tension with the prompt null rather than sitting beside it. A protocol does nothing on its own on any individual instance, the same way a wire format makes no single message smarter, so a per-instance ablation measuring the vocabulary against loose prose *should* read null, and did. The protocol's value accrues across instances, where it gains the property the whole paper is after: accountability becomes transitive. When every node speaks the same typed contract, agent B can verify agent A's kill by rerunning it, agent C can build on B's verification without re-running A, and a human auditor can enter the chain at any link; the warrant flows down the chain with the receipts, never resting on any link's word. Loose vocabulary caps accountability at one hop, the author vouching for their own graph. A common protocol lets verification compose: that is what 385 graphs in one vocabulary are for, and the precondition for everything §(future-work) builds on them.

### The trace is the contribution

The reframe this work forced is the one its epistemology was always pointing at. The bench treats an agent as a scorer of verdicts. The hygraph treats an agent as a builder of claims. Everything that survived the demolition lives on that second reading, and each virtue below is one face of it.

Name the enemy first, because every block below is aimed at the same one: the output that is **confidently wrong and impossible to verify**. Fluent generation produces it by default, this work met it everywhere it looked (the suite-green over-narrow fix, the 4/4 false-green self-audit, the recall-inflated resolve rate), and it is the failure mode that scales with capability rather than away from it. Trust is the default mode of consuming agent output, and the substitution this paper asks of its audience is exact: accountability in place of trust, line by line, machine-checkable. The flux divergence shows the substitution at work. The minimal agent offered a verdict: suite green, done. The graph agent offered a ledger: nineteen nodes, each a hypothesis, an exact command, an observed outcome, and the edge the result generates. You audit a ledger line by line, and at no point do you extend credit. The fix was knowable as better *without trusting the thing that produced it*, and that property, not the win, is the durable result.

**Truth is buildable, and the graph is the build.** On the view developed in [Truth Is Buildable](/truth-is-buildable), a true claim is a structure assembled from sources: provenance is the dependency graph, citation is an edge, attestation is the signed build log, falsifiability is the build being able to go red, and truth is the build currently passing. The hygraph mechanizes that picture one claim at a time. A node without a replayable trial is not a low-quality node; it is not a node, the same way an uncheckable number is not a measurement. A resolve rate, even an honest one, is a verdict over 728 builds the reader cannot climb. A hygraph is the climbable chain. By the paper's own epistemology, the second artifact carries more truth per byte than the first.

**The asymmetry engine.** A fabricated reasoning trace is expensive to sustain, because every fabricated node has to survive a replay the author does not control. A confident narrative is cheap to invent, because nothing in it is pinned to a procedure. The minimal arm's over-narrow fix is the cheap kind: it reads as finished, and reading it harder never reveals the flaw; the receipt reveals it in one command. Verification is not a tax on the method. It is the method. The same asymmetry governs failure: a trusted oracle that fails is a betrayal and leaves you nothing, while a truth-builder that fails leaves a trail that names the failed node. The flux graph recorded its own three mistakes, in advance, as kills that generated its next edge, each correction itself a replayable trial. One method hides its errors inside confidence. The other spends them as fuel.

**Persistence: out of the window, with no half-life.** Replay's second payoff is survival. The context window is the machine's working memory: fast, wide, and mortal. Chain-of-thought lives there and evaporates with it. The hygraph is reasoning that climbed out before the window closed, demonstrated at our own expense when a build box died mid-investigation and only the externalized graph and patch survived to be resumed. Writing was always this move; what the graph adds is that the externalized form is not merely readable later but *re-runnable* later, and the discipline that makes it real is self-sufficiency: every node carries its own reconstitution, or it only looks like it outlasts the window until you try to resume. The same property runs forward in time. Trust weakens with the witness and dies with the memory; a replayable trial copies without loss and survives as long as one copy does. The honest scope: the logical content has no half-life, while the runnable form inherits the half-life of its apparatus (our graphs replay only while flux builds, z3 runs, and the SHAs resolve), so provenance approaches eternal as replay approaches first principles. And what it preserves is not truth but *checkability*, which is stronger: a false claim backed by trust launders itself clean as the witnesses die; a false claim backed by provenance stays caught, forever. Provenance is not eternal truth. It is eternal vigilance.

**Trust versus accountability.** *Nullius in verba*, extended to the machine: take nobody's word, not even the silicon's; check its receipts. To a maintainer, a coding agent is a nobody, and so is its operator, and when receipts are attached it does not matter: a red-on-master, green-with-fix test plus a soundness twin plus a clean suite reads identically whoever submits it. Merit discriminates no substrate. The 81 merged PRs are the ecological witness: adversarial strangers accepted agent-authored code at 50.6% on the strength of attached evidence, not attached reputation. This is a principled direction for what alignment can mean: not a trustworthy agent we then believe, but an accountable one whose every claim is bound to a test a hostile party can rerun. Reliability is the same epistemics accumulated: you never arrive at trust, you arrive at a body of attestations too large and too redundant to doubt, which is a different and better place to stand. The guarantee stays narrow and real. Everything *attested* is checkable; nothing guarantees that everything *relevant* is attested, and choosing what must be on the ledger is exactly where human judgment stays load-bearing.

**The equilibrium looks like accounting, and Enron is the precedent.** Alignment will not resolve to one answer. The working anticipation is a control regime in the shape accounting reached after its own confidently-wrong-and-unverifiable era: standards (GAAP), independent audit, and the three-way match, where no payment clears unless the purchase order, the receiving report, and the invoice agree, no single party trusted to hold more than one leg. The agent analog is already this harness's shape: no claim clears unless the proposer's claim, the recorded trial, and an independent replay agree, and the generator never grades its own work. Enron is the lesson about the alternative: self-attestation scales smoothly right up until the catastrophe that legislates the controls after the fact. Note what this view of alignment is not. Benches operationalize alignment as obedience and conformance, and the audit shows it (§(audit)): three quarters of the tasks grade transcription of a handed spec, the rest grade recovery of an unstated choice. Agency is neither. An agent facing underspecified prose can guess and conform (the lottery), refuse, or exercise agency: elicit the missing decision, make the call, and declare it with receipts. Benches score only the first; the control regime above is built for the third (§(future-work)).

**Merit attaches to the work, not the doer.** Under all of the above sits a separation humans rarely make. We route praise and blame to doers, for lack of vocabulary and social norms that could route them to the work, and the conflation was affordable while only humans produced work, because the doer was a serviceable proxy for the work's quality. It is not affordable now. An agent can produce a thousand artifacts of any quality overnight; judging them by their author runs exactly backwards, and judging the author by replaying the artifacts is the only direction that scales. Merit, read precisely, is what survives the shift: the warrant a piece of work carries in itself, checkable without reference to who or what produced it. The hygraph is vocabulary for that norm, a unit of work that ships with its own evidence; the receipts-first PR is its social practice; the maintainer who merges on the ledger alone is its early adopter. This paper is, deliberately, a declaration of the norm in a searchable venue: praise the work, blame the work, replay the work. The doer earns standing only as the accumulation of work that survived.

**Legibility, revisited.** The confession from the introduction completes here. A benchmark number is legible to people who will never read a trace, and that reach is worth something; it is how this work got read at all. But the number is the artifact a reader can do the least with. It cannot be perturbed, cannot be replayed, cannot surprise anyone into a rival hypothesis. The flux trail can: a reader who suspects the graph arm got lucky can run the receipt, construct a new discriminator, attack a node. The bench result is an answer. The live example is an instrument, and instruments are what inquiry actually accumulates.

### The prestige

A data structure earns its keep by what it unlocks, and the unlock is the part of this work we find most interesting: the [third act of the trick](https://en.wikipedia.org/wiki/The_Prestige_(film)), where what was pledged comes back as something more. Five affordances, each with its honest status.

*Parallel agents, shorter wall-clock.* The graph is monotone: nodes append, kills are idempotent. Parallel agents can therefore latch onto one shared graph lock-free, fan out across rival hypotheses, and re-verify each other's kills instead of trusting them, with transitive accountability (above) as the precondition that makes the fan-out safe. A prose summary must be re-parsed into independent units before anything can be dispatched; the graph ships pre-factored. Named, not yet run (§(future-work)).

*Model-provider independence.* The smem lives in the harness, in plain markdown, behind typed contracts any capable model can read and write. The pair-swap run is the witness: the entire model pair changed and the structure ported wholesale (§(open-weight-run)). Reasoning that accumulates in a vendor's context window is a liability; reasoning that accumulates in a substrate you own is an asset.

*Accountability.* Every claim ships with its replay; the whole discussion above is this affordance unpacked.

*Alignment.* Trust displaced by audit: an agent whose every claim binds to a test a hostile party can rerun does not need to be believed to be used.

*Discovery, in Sutton's sense.* The epigraph completes here. A model's unaided output is bounded by the convex hull of its training distribution: interpolation, however fluent. Each hygraph node is anchored to a fresh trial of the world, so the graph is a procedure for stepping outside that hull one verified step at a time. The flux fix existed nowhere until the inquiry built it, on an issue its own maintainers were stuck on. Agents that contain what we have discovered recall. An agent that can build and survive a hypothesis graph discovers.

## Related work {#related-work}

### SWE-bench, contamination, and construct validity {#rw-swebench}

The SWE-bench family defines the Verified / Pro lineage, official harness, and contamination-resistant tier design. **SWE-Bench+** (Aleithan et al. 2024) manually audited the original bench: 32.67% solution leakage, 31% weak tests. **OpenAI's February 2026 audit** found a majority of audited Verified tasks have flawed tests and that frontier models reproduce exact gold patches; it stopped reporting Verified and recommends Pro. **Wang, Pradel & Liu** (ICSE 2026) show plausible patches pass tests yet diverge from developer intent; their axis is patches that pass but are wrong, ours (§(audit)) is tasks whose materials do not determine which passing behavior is intended. **SWE-rebench** uses post-cutoff filtering as a parallel contamination strategy and publishes per-problem cost. **HAL** (Stroebl et al. 2025) is the third-party cost-aware agent leaderboard and the nearest infrastructural precedent for this paper's cost-transparency stance; this paper's receipts go one level finer, to the per-instance re-gradeable verdict. The official **swe-bench/experiments** repo requires `trajs/`, `logs/`, `patch.diff`, `report.json` per submitted instance, the minimum publication norm our provenance contract extends with gate traces, hypothesis graphs, and a cost ledger.

### Agent scaffolds and SE-agent harnesses {#rw-scaffolds}

SWE-bench-targeted harnesses include OpenHands (Wang et al. 2024), SWE-agent (Yang et al. 2024), and AutoCodeRover (Zhang et al. 2024/25), all built on the ReAct pattern (Yao et al. 2023); none implements Peirce-typed stage contracts or a kill-conditioned hypothesis-graph memory. **Voyager** (Wang et al. 2023) is the closest loop-shape precedent: embodied observe→hypothesize→test→commit, with a skill library where this work holds falsifiable claims. **SWE-Effi** ([arXiv:2509.09853](https://arxiv.org/abs/2509.09853)) is the sharpest published counter-position: effectiveness emerges from scaffold-model synergy rather than residing in the scaffold alone. This paper now agrees from the other direction, with the synergy named: on Pro the binding pair is gate × oracle, and neither scaffold typing nor model tier moves the number much once that pair is in place.

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

## Limitations {#limitations}

*The mechanism evidence is existence-grade.* One audited divergence, on one instance, in a program that was not preregistered when it ran. The pilots' nulls are confounded by a selection artifact we can name but not yet remove (the triage fast-path), and the localization-hard band where the mechanism should live has not been decisively tested; its one strong candidate did not reproduce at HEAD. Nothing here is a rate.

*The audit's two tiers carry different burdens.* The mechanical spine (11.4%) is re-derivable by grep; the two-expert tier rests on a stated standard, adversarially verified (κ = 0.52, all disagreement skeptic-stricter), and 63 screen-flagged candidates are excluded as rater-pending. The proven floor is a floor.

*The bench numbers are public-split numbers.* Pro's public repos predate both model families' cutoffs; the gold-overlap audit bounds frontier reproduce-gold at ~2%, but our holdout is weaker than Scale's (different commits, same repos), and the held-out submission has not been made. The gate's oracle access does not exist on the private split.

*Essence oracles are authored.* The mechanism experiment's graders are written from upstream issue text by the operator's pipeline, mitigated by red-at-base/green-on-gold walls and by the merged fix's external attestation, not eliminated.

*The smem is small and per-instance.* Hypothesis graphs in this work are one markdown file per inquiry; cross-instance accumulation is untested. That carries its own deflationary point: the file was never the bottleneck at any repo size, so heavier stores need to earn their keep at cross-instance scale, not per-instance.

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

## Availability and reproducibility {#availability}

- **Repositories.** [github.com/kimjune01/swebench-pro](https://github.com/kimjune01/swebench-pro) (the bench run; frozen tags `prereg-pro-v1`, `prereg-pro-v1-cheap`), [github.com/kimjune01/swebench-verified](https://github.com/kimjune01/swebench-verified) (prior-generation baseline, Zenodo-DOI'd), [github.com/kimjune01/swebench-pro-audit](https://github.com/kimjune01/swebench-pro-audit) (the determinacy audit; every claim one row in `CLAIMS.md`, all 728 verdicts in `COVERAGE.md`, mechanical spine re-derivable by grep), [github.com/kimjune01/determinacy](https://github.com/kimjune01/determinacy) (the audit as a portable tool for any SWE-bench-shaped bench; SWE-rebench run included), [github.com/kimjune01/hygraph-mechanism](https://github.com/kimjune01/hygraph-mechanism) (the mechanism experiment; flux trail frozen at `flux-1613-trail-v1`).
- **Provenance artifacts.** Per-instance trajectories, hypothesis graphs, captured diffs, gate traces, and cost ledger under `runs/scored/artifacts/`; preregistrations at the freeze SHAs; the OSS ledger (`pr-receipts.jsonl`) with the GraphQL query that recomputes every number it asserts.
- **OSS deployment trace.** ~385 hypothesis graphs at [`kimjune01/sweep/repo-hypotheses/`](https://github.com/kimjune01/sweep), one per investigated issue; PR-level outcomes pinned at `kimjune01/kimjune01@paper-2026-05-28`.
- **Replication.** Boxes, budget, the per-instance cost ledger (`COST_BASIS.md`), and the step-by-step rerun live in the run repo and the field guide [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro), not narrated here.
- **Companion writing.** The instrument story and field guide: [How Not to Run SWE-bench Pro](/how-not-to-run-swebench-pro). The error this paper corrects, from the inside: [Precisely Wrong](/type-iii-error). The epistemology the discussion rests on: [Truth Is Buildable](/truth-is-buildable). Dated provenance posts establish parallel rather than derivative development: *Theory is load-bearing* (2026-03-17), *The proof manual* (2026-04-05), and *Type the question* (2026-04-08) predate ADI (2026-04-17); *Evidence has a trajectory* (2026-04-27) and *The Hypothesis Graph* (2026-04-28) predate CMM (2026-05-26).
- **PDF.** Arxiv-shape build at [/assets/methodeutic-harness-paper.pdf](/assets/methodeutic-harness-paper.pdf), rebuilt from this markdown source by `scripts/build-paper-pdf.sh`; the source is canonical.
- **DOI.** Verified artifact: Zenodo-DOI'd. Pro bundle and this paper: [placeholder: Zenodo DOIs pending.]
- **License.** Skills released under **CC-BY-SA-NS** ([june.kim/cc-by-sa-ns](https://june.kim/cc-by-sa-ns)); repo-level terms in each `LICENSE.md`. The harness an outsider clones is the same harness that produced the published numbers.

**Reproducibility invitation.** *Nullius in verba.* Every number in this paper is recomputable from committed artifacts: the bench verdicts by re-running the official grader on captured diffs, the audit's mechanical spine by grep, the flux divergence by replaying the receipt programs against both committed patches. Doubts should be filed as issues against the relevant repository; confirmed corrections fold into the next versioned artifact, as the retraction in §(perturbation) and the reversal this version reports already have.

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

The artifact claim (§(tables)), *no method documented has demonstrated a higher SWE-bench Pro resolve rate with equivalent receipts*, requires a comparative search. The bar for *equivalent receipts*: published per-instance trajectories, captured diffs, gate or evaluator traces, cost ledger, and reproducible run conditions.

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
