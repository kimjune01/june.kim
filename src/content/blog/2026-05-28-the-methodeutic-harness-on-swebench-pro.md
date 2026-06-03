---
variant: post-paper
autonumber: true
title: "Draft: The Methodeutic Harness on SWE-bench Pro"
subtitle: "A typed hypothesis-graph inquiry, deterministically gated and audited end to end"
tags: methodology, epistemology, coding
---

*[Download PDF](/assets/methodeutic-harness-paper.pdf) · arxiv-shape preprint, rebuilt from this source. · [Results, code, and receipts](https://github.com/kimjune01/swebench-pro), reproducible in one prompt.*

## Abstract {-}

Reasoning can be encoded at the harness layer, and the encoding is typing: the modes of inquiry and the hypotheses they produce live in a typed data structure a deterministic engine runs. We present a *methodeutic harness* (methodeutic is Peirce's term for the methodology of inquiry): `inquire` builds that hypothesis graph by abduction, deduction, and induction, `implement` writes the surviving hypothesis, and `attest` verifies against the official grader, all enclosed by a deterministic gate that no model arbitrates. The same frozen harness resolves **694 of 728 (95.3%)** of SWE-bench Pro under the official grader; with the entire model pair swapped to open-weight models, it still resolves **678 of 728 (93.1%)** at ~12.6× lower cost. Against the strongest bare model on the standardized scaffold, the harness adds 31 to 37 points, past anything reasoning-budget scaling buys: the lift is a property of the harness, measured on a fixed model with and without the structure. (The open-weight rate is partly recall-inflated and is read as cost and portability, not capability; §(open-weight-run).) Every claim ties to a committed receipt (per-instance trajectory, captured diff, gate trace, cost ledger), and a random sample reproduces in one prompt. In deployment the same lineage merged 81 agent-authored PRs into 73 cold repositories at a 50.6% maintainer merge rate. No training, fine-tuning, or GPUs.

## Introduction {#introduction}

> We want AI agents that can discover like we can, not which contain what we have discovered.
>
> — Richard S. Sutton, *The Bitter Lesson* (2019)

In 2026, reasoning is the capability frontier for large language models, and coding is both high-value and definitively measured: a patch passes its tests or it does not. SWE-bench Pro is the standard ruler: resolve rate on real GitHub issues. Leaderboards compare models within a controlled minimal harness. But do harnesses themselves matter to performance?

Ask how to make a model reason better, and the answer is always *more*: more parameters, more data, more training compute, or the inference dial cranked from low to high to xhigh and ultrathink. Reasoning is marketed as performance you can buy, and the bill is large. It is graded the way it is sold, by the inductive property of inference alone: a score on a held-out set. And such benchmarks saturate: SWE-bench Verified did, and OpenAI, which created it, [stopped reporting the score](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) earlier this year, recommending SWE-bench Pro instead. Reasoning is the part that transfers; an inductive number on an aged bench cannot separate it from recall.

That leaves two responses. One keeps scoring reasoning inductively and minting fresh benchmarks to outrun the saturation; when the latest state-of-the-art models score lower on each fresh bench, the entire industry is unsurprised. The other encodes reasoning itself and generalizes beyond induction. This paper hoists reasoning up to the harness layer: a typed inquiry over a persistent hypothesis-graph memory, enclosed by a deterministic gate that no model arbitrates. The models propose, critique, and implement inside this structure, but the deterministic complement owns the state, the evidence record, and the decision to continue, branch, commit, or stop.

Two traditions have approached this from opposite sides and stalled. One is LLM-agent work, which keeps rebuilding harness memory under the name "memory systems," drawing its citations from the post-2020 literature and largely missing the lineage that already worked the problem. The other is cognitive architecture. Soar (Laird 1987) and ACT-R built that lineage, the typed semantic / procedural / episodic memory and the mechanical operations over it, but for want of a general inference engine at its core, it stayed a research program.

This paper marries them: a cognitive architecture in the Soar lineage with an LLM as its inference component. The hypothesis graph fills the `smem` slot, the pipeline-stage skills fill `pmem`, the per-run trajectories fill `epmem` (§(typed-memory)); the model plugs into typed memory and a deterministic controller rather than sitting at the seat of reasoning. Harness engineering is then no longer incidental scaffolding; it is the architecture.

However, neither of the traditions built the missing piece: a place to put hypotheses under consideration. Today it has nowhere to live, since prose context is lossy, skill libraries store verified code rather than falsifiable claims, and vector retrieval indexes established chunks. Here, that substrate is the **hypothesis graph**, and it is typed. Peirce (1878, 1903) identified three modes of reasoning: abduction, deduction, and induction. Each is a first-class node type, falsification criteria are executable edge predicates, and routing and gating are deterministic graph operations. The graph is just a markdown file: no RAG, no database, zero dependencies. Working one issue at a time, the markdown carries to any repo size. Too much of the field reaches for new data structures where none is needed (§(limitations)).

What makes the hypothesis graph an instrument of inquiry is methodeutics, Peirce's methodology of inquiry. It is a reasoning harness built on the pragmatist lineage, the philosophers who studied how inquiry works rather than what any one inquiry concluded. What it encodes is method, and method is what transfers to novel problems. It supplies the typed contract that weds the memory lineage to the model: the three modes become stage-typed read/write contracts over the graph, and the model does its work inside them.

At the frontier of industry, an extra point of performance costs on the order of billions: a training generation, or the inference dial cranked to xhigh and ultrathink for single-digit returns (§(discussion)). For the harness, it is about zero. The harness spends more compute per task, but the higher solve rate offsets it. None of it came from a training run, and the open-weight run (§(open-weight-run)) shows the inference core itself is a commodity.

## Baseline comparison {#central-comparison}

Two kinds of players set the terms in agentic coding benchmarks: the labs that train the models and the benchmark makers who score them. The lab needs a measure and a marketing signal; the benchmark maker needs a control: the harness held fixed, to compare models against each other. SWE-bench Pro serves those needs with scientific rigor. But the rigor demands controlling for the variable that matters most to end users: the harness.

<figure>
  <img src="/assets/methodeutic-attribution.svg" alt="Grouped bar chart of SWE-bench Pro resolve rate. Three bare models on the standardized SWE-Agent scaffold: Sonnet 4.5 at 43.6 percent, GPT-5.5 at 58.6 percent, Opus 4.7 at 64.3 percent. Two configurations of this methodeutic harness: open-weight at 93.1 percent, frontier at 95.3 percent. The harness bars stand about thirty points above the tallest bare-model bar." />
  <figcaption><strong>Figure.</strong> Resolve rate on SWE-bench Pro. Bare models run on the standardized SWE-Agent scaffold (official <a href="https://labs.scale.com/leaderboard/swe_bench_pro_public">Scale board</a>, 250-turn; Sonnet 4.5 at 43.6 ± 3.6); the harness runs the same tasks. It clears the best bare model, board-leader Opus 4.7, by 31 to 37 points, well past the ~20-point spread across model tiers. An anchor, not a clean control: the harness adds structure and a larger turn budget, and the bare figures are vendor/board-reported on differing scaffolds (reading below). Claude Mythos (a vendor-reported 77.8% on Pro) is excluded: unavailable to the public.</figcaption>
</figure>

Skepticism is warranted. Isn't the model just doing all the work? If you attribute it all to the strongest model present, GPT-5.5 (the stronger model, never the generator) scores **~58.6%** bare on Pro; the strongest on the whole board, Opus 4.7, **~64.3%**. This harness resolves **95.3%**, **31 to 37 points above the controlled minimal harness**, with the mechanical reasoning running on the *weaker* model. No reasoning budget from top labs closes a gap that size: the effort dial lifts a fixed model about five points (Anthropic's own [Opus 4.5 effort curve](https://www.anthropic.com/claude-opus-4-5-system-card), low to high effort, ~75 → ~81 on SWE-bench Verified at triple the output tokens, Fig. 1.1.2.A); the harness lifts the same model thirty. Model strength is a small lever here; the harness is the large one.

Hold the model fixed and the shape returns from the other side: standard SWE-Agent with Sonnet 4.5 scores ~43.6%, this harness ~95.3%. Both are ReAct loops with full test-execution feedback. The baseline is a *minimal harness* in the usual sense (a ReAct loop with a goal statement); this harness is the same loop with structure on top, so testing is held constant and the gap excludes "we run tests and they don't."

## Attribution and attestation {#claim}

So what earns the gap, and what proves it?

The structure it adds: a typed abductive inquiry stage *before* the act loop, plus two verification separations a bare loop lacks. Critique runs through a *separate blind challenger* rather than generator self-critique, and *attestation is separated from the testing agent*, so the model that ran the tests does not declare the verdict. Each, in our experience, helps on its own; we isolate none here, and the harness spends a larger turn budget besides. So read the leg as an anchor, not a clean control: it bounds *this system* against the standard one, not *any one separation* against none.

We do not attribute the lift to any specific part of the harness: the typed inquiry stage, the blind challenger, the deterministic gate, the outer loop. The run rules one out: the outer loop is not the driver. Most wins land on the first pass, re-entry recovers only a small tail (§(results)), so the lift lives in the single-pass machinery, not the iteration. Decomposing the rest is a clean per-component ablation (fixed model, fixed budget, each piece on and off), and future work. The artifact-level claim needs no hedge: across two model pairs, frontier and open-weight, a cheap and fully auditable harness, not the model tier, clears the best bare model by 31 to 37 points on SWE-bench Pro, past anything reasoning scaling reaches, receipts committed.

<figure>
  <svg viewBox="-30 0 1015 360" role="img" aria-label="Sankey flow of 728 eligible SWE-bench Pro instances: 694 resolve and 34 do not; of the resolved, 602 are solved on the first pass, 46 are recovered by the outer loop, and 46 predate trajectory capture." style="max-width:760px; width:100%; height:auto; margin:1em auto; display:block; font-family:system-ui,-apple-system,sans-serif;">
    <polygon points="86,20 330,20 330,306 86,306" fill="#1d4ed8" opacity="0.16"/>
    <polygon points="86,306 330,314 330,328 86,320" fill="#64748b" opacity="0.22"/>
    <polygon points="346,20 560,20 560,268 346,268" fill="#1d4ed8" opacity="0.30"/>
    <polygon points="346,268 560,276 560,295 346,287" fill="#60a5fa" opacity="0.30"/>
    <polygon points="346,287 560,303 560,322 346,306" fill="#94a3b8" opacity="0.28"/>
    <rect x="70" y="20" width="16" height="300" fill="#334155"/>
    <rect x="330" y="20" width="16" height="286" fill="#1d4ed8"/>
    <rect x="330" y="314" width="16" height="14" fill="#94a3b8"/>
    <rect x="560" y="20" width="16" height="248" fill="#1d4ed8"/>
    <rect x="560" y="276" width="16" height="19" fill="#60a5fa"/>
    <rect x="560" y="303" width="16" height="19" fill="#cbd5e1"/>
    <g fill="#334155" font-size="12.5">
      <text x="64" y="174" text-anchor="end">728 eligible</text>
      <text x="338" y="14" text-anchor="middle" fill="#1d4ed8" font-weight="600">Resolved · 694</text>
      <text x="338" y="343" text-anchor="middle" fill="#64748b">Not resolved · 34</text>
      <text x="584" y="148" text-anchor="start" fill="#1d4ed8" font-weight="600">Solved on the first pass · 602</text>
      <text x="584" y="289" text-anchor="start">Recovered by the outer loop · 46</text>
      <text x="584" y="316" text-anchor="start" fill="#64748b">Trajectory not captured · 46</text>
    </g>
  </svg>
  <figcaption><strong>Figure.</strong> Where the 728 eligible Pro instances land. The first methodeutic pass carries <strong>602</strong> wins; the deterministic outer loop converts another <strong>46</strong> first-pass misses (about 7% of graded wins), and 46 further wins predate trajectory capture. The loop is recovery, not a grind. First-pass and recovered counts are over the 648 wins with captured trajectories (§(results)).</figcaption>
</figure>

The headline claim: under one frozen harness, this system resolves more of SWE-bench Pro at a lower audited per-instance cost than any prior method we could find. This is falsifiable, and becomes fully unconditional once the Pro artifact is DOI-pinned (§(provenance)). No method documented in our comparative literature search (§(search)), known to us, has *demonstrated* with equivalent receipts a higher SWE-bench Pro official-harness resolve rate at a lower audited per-instance dollar cost, reproducibly under one frozen harness, than the one presented here.

We do not attest; our harness does. Our own part is merely a pointer: to the passing patches, the runtime logs, and the worklog we kept while running the harness through the bench. Inside the deterministic outer loop no patch advances until its tests pass, and the committed patch is itself the attestation it hands the grader: a re-gradable artifact the grader re-runs without us. Trust transfers down the chain by construction, never resting on our word. Three receipts, three independent attestors.[^verified]

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:9.5em"><col><col style="width:13em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Receipt</th><th style="background:#f0f0f0">Evidence</th><th style="background:#f0f0f0">Attestor</th></tr></thead>
<tr><td>Pro (preregistered)</td><td>terminal: 694 / 728 = 95.3%, 0 incomplete, whole eligible set graded</td><td>Scale's official grader, re-runs the committed patch</td></tr>
<tr><td>OSS PR merge rate</td><td>81 merged across 73 cold repos, 50.6%, GraphQL-verifiable</td><td>adversarial maintainers who merged</td></tr>
<tr><td>Economic cost</td><td>~$5.14/instance frontier, ~$0.41 open-weight (cash far lower on flat subscriptions); ledger published</td><td>anyone, recomputing at public API rates</td></tr>
</table>

[^verified]: SWE-bench Verified (426 / 438 eligible, Zenodo-DOI'd, trajectories and diffs committed) is the prior-generation baseline: saturated and contaminated, it ports cleanly but no longer discriminates, so it stands here as history rather than a primary receipt. Same harness, same official-grader discipline.

The two properties that matter are *demonstrated* (we publish the trail that makes the numbers auditable) and *reproducibility on both benches* under one artifact.

## Theoretical grounding: methodeutics {#grounding}

Peirce's *Illustrations of the Logic of Science* (1878) and *Pragmatism as the Logic of Abduction* (1903) type the operations of inquiry into three modes that are not interchangeable.

- **Abduction** generates explanatory hypotheses for surprising observations: *what would, if true, make this no longer surprising?*
- **Deduction** derives testable predictions from hypotheses: *if this hypothesis holds, what follows?*
- **Induction** tests predictions against evidence: *does the evidence accord with the prediction?*

<figure>
  <img src="/assets/modes-of-reason-triangle-light.svg" alt="Triangle of the three Peircean modes: Observation to Theory (abduction), Theory to Experiment (deduction), Experiment to Observation (induction). Three modes, three edges, one self-correcting cycle." style="max-width:528px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> The three modes as one cycle: Observation → Theory (abduction), Theory → Experiment (deduction), Experiment → Observation (induction). <code>inquire</code> traverses all three before any code is written; a partial traversal is a partial inquiry.</figcaption>
</figure>

No single mode carries a belief to its grade. Abduction proposes content but does not test it; induction tests but introduces no new explanatory content; deduction traces consequences but invents nothing. The credence a node ends up with is what traversing all three earns it, and that is what it means to call the modes typed: each is fixed by what it can't do. Deduction is where readers balk: why is *abduction* responsible for theory? Isn't that deduction's job? No. Deduction doesn't generate the theory, and it doesn't prove it either; it sets out the conditions under which the theory could be tested. It unfolds the hypothesis into the predictions it must answer for. The theory was abduced, the predictions deduced, and induction does the testing. Keep them separate and each does its one job; collapse them and you get familiar failure modes:

- **Confirmation bias**: induction without abductive alternatives
- **Confabulation**: abduction without inductive grounding
- **Free-association**: no typed mode at all

That collapse is exactly what modern LLM agents do by default, since a single forward pass proposes, predicts, evaluates, and rationalizes in undifferentiated prose.

Where a single forward pass collapses the modes, methodeutics holds them apart. It is Peirce's term for the methodology of inquiry: how to conduct the typed-mode loop well. The framework draws on a dispersed lineage of primary sources, cited here directly rather than through any secondary work.

*Modes of reason and the irreducible three.* The three modes come from Peirce (1878, 1903). Around the act of testing, philosophy of science built an apparatus of real rigor: Bacon's induction (1620), Popper's falsifiability (1934), Meehl's "soft science" critique (1967), Pearl's causal calculus (2009). Justification got its method, every step of it. But it begins one step too late, taking the hypothesis as given and filing its origin under inspiration. Ask where the hypotheses come from, and the rigor goes quiet: the discipline that trusts nothing on authority trusting this on faith. Peirce alone named the operation, abduction, and was ignored. The harness is the first to run it as a first-class typed mode.

*Pragmatist credence.* Ramsey 1926 (*Truth and Probability*; subjective probability, the Dutch Book argument, belief as betting odds); James 1907 (*Pragmatism*; truth as what works); Dewey 1929 (*The Quest for Certainty*; truth as warranted assertibility). The node-level semantics of the hypothesis graph descends from this lineage.

## Methodeutics, applied {#application}

Abduction completes the trichotomy as an idea. Putting it to work is another matter. How do you generate a hypothesis, and where do you hold it? A diff, in a typed graph.

*Bi-abduction, tri-abduction, and compositional inference.* The primitive under abduction is a diff: a before snapshot, an after snapshot, the flip as figure and what held as ground, Rubin's Gestalt terms. Arity grows from there, from unary (one before/after pair, one frame) to bi-abduction (the frame inferred autonomously: Calcagno et al. 2009, O'Hearn 2019, scaled industrially in Facebook Infer) to tri-abduction (a diff across branches: Zilberstein et al. 2024, [*Outcome Separation Logic*](https://arxiv.org/abs/2305.04842)). `inquire` sat at the unary-to-bi rung, a single before/after diff with the frame inferred from the symptom; tri-abduction sits a rung above what this benchmark exercise required.

<figure>
  <img src="/assets/bi-abduction-dimmer.svg" alt="Bi-abduction as a diff: a dead light with three intact suspects (dimmer, fixture, bulb), the cause invisible. Bypassing the dimmer straight to the wall restores the light, so the XOR isolates the dimmer as the figure (the fault) and exonerates fixture and bulb as the ground (the frame)." style="max-width:720px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> Abduction as a diff, on a perturbable system. The symptom is a light fixture unresponsive to switch input, and it underdetermines its cause: dimmer, fixture, and bulb are all intact, so the static scene names no suspect. The perturbation manufactures the second snapshot, bypassing the dimmer to the wall, and the XOR isolates the figure (the dimmer) from the ground (fixture and bulb). Generating that diff is the abductive act; induction follows, convicting the dimmer once the light returns.</figcaption>
</figure>

*Inspiration for `inquire`'s diagnostic stance.* Wald 1947 (sequential testing) and Vovk & Wang 2021 (e-values) shaped how `inquire` treats diagnosis as evidence accumulating toward a hypothesis. No accumulator is deployed: the code under test is deterministic, so the gate routes on the binary grader verdict (§(gating)).

*Directed graphs as reasoning representation.* Pearl 1988 (*Probabilistic Reasoning in Intelligent Systems*; Bayesian networks as DAGs of dependencies); Pearl 2000/2009 (*Causality*; structural causal models, d-separation, do-calculus). Our data structure (typed nodes, directed edges) applies Pearl's lineage to hypothesis representation rather than causal-structure inference.

*Working instantiations of the loop in different fields.* Calcagno et al. 2009 (Facebook Infer, bi-abductive shape analysis at industrial scale); Arjovsky et al. 2019 (Invariant Risk Minimization, tri-abductive figure-ground splitting under environment variation); Wang et al. 2023 (Voyager, observe→hypothesize→test→commit in Minecraft with a skill library, untyped at the node level). Adjacent and parallel work (IDEA, ADI, CMM, AriGraph, CausaLab, CoALA, and others) is treated in §(related-work).

<figure>
  <img src="/assets/hypothesis-graph-fixture.svg" alt="A hypothesis graph for the dead-fixture inquiry. The observation (light won't turn on) fans by abduction into four typed hypothesis nodes: no electricity from socket, dimmer switch broken, fixture dysfunctional, bulb expired. Three are killed by mechanical predicates (outlets live, lights on wall, lights elsewhere); the dimmer node is witnessed (bypass works) and closes as induction at 96 percent." style="max-width:720px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> The hypothesis graph for the dead fixture. Abduction fans the observation into four typed candidate nodes; mechanical kill predicates fire on three (the socket, fixture, and bulb each cleared by a cheap test), the dimmer node is witnessed by the bypass and closes the frontier, and deduction derives the fix. Typed nodes, directed edges, all three modes in one inquiry.</figcaption>
</figure>

Isn't this just debugging? Yes, precisely. It has simply never been typed into a data structure inside an inference engine. Every engineer runs this loop, abduce a cause, kill it on evidence, witness the survivor, derive the fix; but in their head, the modes collapsing into one undifferentiated pass. The harness gives the loop a typed substrate, the hypothesis graph, and a deterministic engine to run it, so a model executes the inquiry.

*Composition over the hypothesis graph.* Three of the lineages above enter through separate roles. The **structural skeleton** is Pearl's DAG (above): we borrow the typed-node/typed-edge form and leave the probabilistic semantics (conditional independence, do-calculus) behind. Nodes are typed hypotheses; edges encode dependence and the kill conditions that fire on evidence. Termination rests on the deterministic gate (budget, attempt count, verdict; §(gating)), not on graph topology.

The **node semantics** is credence (Ramsey 1926; James 1907; Dewey 1929). Each hypothesis-graph node carries a *belief* at a credence level, capped by its reasoning mode and continuous, not a fact. Confident confabulation, high confidence on a node that hasn't earned it, is the failure mode the stage-typing and kill conditions jointly prevent. The reasoning-mode label types *what kind* of belief the node carries; the credence types *how much*.

The **update semantics** is the binary test verdict, written back to the active hypotheses as a kill or witness, together with a re-entry route the driver follows (§(gating)). Pearl's skeleton, Ramsey's credence, and a deterministic verdict→route update: three primitives, three roles, one data structure. The operational form is in §(recon-output).

## Method {#method}

<figure>
  <img src="/assets/methodeutic-harness.svg" alt="The SWE-bench Pro harness. Inquire builds the hypothesis graph (smem) by abduction, deduction, and induction, typing each node by the mode that established it; implement reads the surviving hypotheses, derives a patch under cross-family adversarial challenge, and emits it to attest; attest runs the official harness, emits a binary verdict and a re-entry route, and writes a kill or witness classification back to the graph; the deterministic gate routes on the verdict, the route, attempt count, and budget. Off-box capture commits the per-instance provenance artifact (trajectories, graph, diff, gate trace, grader output, cost ledger) to the public repo." />
  <figcaption><strong>Figure.</strong> The methodeutic harness used on SWE-bench Pro. <code>inquire</code> builds the hypothesis graph by Peirce's three inquiry modes (abduction, deduction, induction), typing each node by mode; <code>implement</code> writes the patch, <code>attest</code> verifies; the gate is finite-state with no model call; the outer loop re-enters <code>inquire</code> with an updated graph rather than retrying the patch.</figcaption>
</figure>

Throughout, the three stages are `inquire`, `implement`, and `attest`; the frozen artifact's code, file paths, and route literals spell them `recon`, `craft`, and `audit`.

### The inquiry frame {#inquiry-frame}

We recast each SWE-bench instance as an inquiry on an engineered system: a failure trace, a codebase, a root cause to find, and an intervention that must not regress the rest of the system. Run this way, the agent discovers like a software engineer can: it abduces a cause from the failure, traces it through the code, and tests it before it writes anything.

Code is the right substrate for this data structure because it combines three properties that other inquiry domains rarely combine:

- **Reproducible**: same input yields same output, modulo controlled nondeterminism
- **Deterministic**: causal lines from input to behavior are mechanical
- **Perturbable**: single-line and single-function diffs are cheap to apply and fully observable

Because those three hold together, hypotheses about code can be tested by cheap mechanical perturbations and falsified by deterministic predicates; kill conditions are not approximations; they are executions.

One instance settles the predicate in this regime. Statistics infers causal relationships from noisy populations, but in code the per-instance response is mechanically observable, so a single passing test on a captured diff is a complete verdict that the diff satisfies the executable benchmark predicate for that instance. That verdict speaks to the predicate alone: behaviors it doesn't cover are out of scope, and we report only what it checks, which is what the grader checks. Medicine needs populations because individual responses are noisy; the per-instance check here does not. So the paper reports counts, denominators, and per-repo breakdowns rather than confidence intervals or significance tests: per-instance verdicts are exact, and aggregating them is bookkeeping. Aggregate claims across repos, benches, or run-order remain empirical, and are caveated where they appear. Portability to substrates where the per-instance response is not mechanically observable is open.

The three Peircean modes are how `inquire` builds the hypothesis graph, each node typed by the mode that established it and capped at that mode's confidence:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:7em"><col><col style="width:6.5em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Mode</th><th style="background:#f0f0f0">What <code>inquire</code> does</th><th style="background:#f0f0f0">Confidence</th></tr></thead>
<tr><td><strong>Abduction</strong></td><td>Proposes candidate root causes from the observed failure; writes hypothesis nodes with falsifiable predicates and kill conditions (read-only)</td><td>low</td></tr>
<tr><td><strong>Deduction</strong></td><td>Traces each hypothesis's consequences through the code to localize the suspect set</td><td>high</td></tr>
<tr><td><strong>Induction</strong></td><td>Tests survivors with cheap read-only experiments (prints, intermediate data)</td><td>moderate</td></tr>
</table>

`implement` then writes the surviving hypothesis, with an adversarial challenger critiquing the diff against the spec. `attest` runs the test suite, takes the grader's pass/fail verdict, and emits a re-entry route (`inquire`, `implement`, or `none`) from a fixed verdict→route table. The driver parses the verdict and the route; both are mechanical, and no model decides termination.

### Hypothesis graph as inquiry output {#recon-output}

`inquire` emits a hypothesis graph document, the structured analysis that precedes the patch. Its structure is the three-pillar synthesis built in §(application): Pearl's directed-graph skeleton, credence node semantics, and the grader's verdict→route update (§(gating)). Because the code under test is deterministic, one run settles each predicate, so no evidence accumulator is needed.

Kill conditions are mechanical predicates over the evidence trajectory, not model preferences, so a node dies when its predicate fires and not before. The graph persists across iterations; re-entry adds nodes rather than overwriting. The frontier closes only when every leaf is killed or witnessed.

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

The graph is a single strong node, the common shape on this benchmark: the gold tests name the missing surface, so abduction generates the diff in one move and needs no fan of competing hypotheses. The node carries the mode that *closed* the inquiry, not the one that opened it. An investigation flip-flops between modes as evidence arrives; here it opens abductive (the gap is the hypothesis) and closes deductive (tracing the four sites confirms it), so the node reads `deduction, 99%`. After the fact we read that conclusion off the committed graph, not a tape of its in-flight modes: we see where the inquiry landed, not the abductive leap that started it. Implement writes the four-part fix, and the blind challenger earns its separation here. It caught that the first draft never invoked `Config.validate()`, because `Load` only runs the validators attached to fields; implement then added the explicit call. The deterministic gate reads the binary test verdict and nothing else:

```
=== GATE F2P 2/2 PASSED ===   TestJSONSchema ✅   TestLoad ✅
PASS_TO_PASS regressions: none
VERDICT: RESOLVED   RE-ENTER: none
```

No model arbitrates that verdict; the grader's pass/fail decides, and `attest` re-runs it against the live patch (two files, +80 lines) before recording the win. `RE-ENTER: none` is the first pass closing the frontier, which is how roughly 93% of wins resolve (§(results)); the remaining ~7% route back to `inquire` for another pass through the same gate that here declines to fire.

That committed node is the conclusion, and an inquiry that reaches one rarely runs straight. Following the same `inquire` skill on an unrelated bug, a single hypothesis flips across all three modes and a kill before it settles:

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

### Blind-blind pushout at the hypothesis stage {#blind-blind}

Two frontier models from different families receive the same evidence pack with no cross-visibility, and each produces a hypothesis independently. A third pass extracts the disagreements, not the agreements: the disagreement becomes the next node in the graph; the agreement is recorded but not actionable. Adversarial filtering operates at hypothesis time, while the worktree is still untouched, rather than at patch time where the diff is already written. Sampling stochasticity alone produces real divergence even within a single model; cross-family divergence compounds it with architectural and training-corpus differences. Both are signal.

### Deterministic gating {#gating}

The gate is the driver routing on two lines `attest` prints, not a model call. `attest` ends every pass with `VERDICT: <RESOLVED|NOT_RESOLVED|PARTIAL>` and `RE-ENTER: <inquire|implement|none>`, assigned from a fixed table (`skills/audit/skill.md`): all `FAIL_TO_PASS` green with no regression resolves and re-enters nothing; a regression routes to `implement` to narrow the fix; a partial or ineffective patch routes to `inquire` to re-diagnose; an empty patch routes to `implement`. Because the code under test is deterministic, one test run settles each predicate; the verdict is dispositive in a single read and no sequential-evidence accumulator is needed.

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

One harness-enforced override applies: a regression gets a single narrow `implement` attempt, and if the next pass routes to `implement` again the driver overrides it to `inquire`. A regression that will not narrow means the approach itself conflicts with a `PASS_TO_PASS` test, and grinding `implement` would retry the same edit. No stage decides its own termination; the verdict and route are mechanical, the budget is fixed, and re-running the same `attest` output through the driver yields the same routing. The logic is published and frozen by the same tag as the rest of the artifact.

One distinction the gate makes sharp. The `attest` agent's `VERDICT` is its reading of the in-container test gate, and it serves only to route the loop. The bench score is computed separately: the official SWE-bench grader (`driver/pro_pilot.py:official_grade`) is re-run on the captured patch after the loop ends, and the headline 694/728 is that grader's verdict, not the agent's. A misread route can waste a re-entry; it cannot manufacture a scored win. No model sits in the routing gate, and no model scores the bench.

### Outer-loop iteration {#outer-loop}

`attest` failures do not retry the patch. They route back to `inquire` with the trajectory classification and the updated graph. `implement` sees a different node-set on re-entry rather than the same node twice. The attempt budget per instance is bounded. Budget exhaustion counts as a clean termination without convergence, and the loop treats it as a verdict. No peek at held-out tests at any point in the loop. The gate's inputs are local to the instance and the agent's own run.

<figure>
  <img src="/assets/wallclock-per-instance.svg" alt="Histogram of wall-clock minutes per instance across the 728 eligible SWE-bench Pro instances. Bars: 5 to 10 minutes 168 instances, 10 to 15 minutes 305 (the peak), 15 to 20 minutes 137, 20 to 30 minutes 58, 30 to 60 minutes 31, 60-plus minutes 29. One peak around 10 to 15 minutes with a thin right tail." style="max-width:560px; width:100%; height:auto; margin:1em auto; display:block;" />
  <figcaption><strong>Figure.</strong> Wall-clock per instance, all 728 eligible Pro instances. One peak at 10–15 min (median ~13 min; 84% finish inside 5–20 min), then a thin tail of heavy repos and craft-hangs on large suites. The outer loop's re-entries would show as a second, slower mode; too few instances re-enter to populate one, so the distribution stays single-peaked.</figcaption>
</figure>

### Fault classification (operator-side) {#fault-classification}

Pre-registered fault classes cover environment-induced failures: auth outage, quota exhaustion, infra timeouts. These are platform faults, distinct from reasoning losses. Classification triggers on fault-window membership, not on instance verdict. Wins inside the window get re-run alongside losses. The protocol disallows any reclassification rule that lets a losing run be retried while a winning run stands; that asymmetry is exactly the loss-laundering it forbids.

### One-shot held-out discipline {#held-out}

The public set may be iterated through the outer loop and re-run on platform fault. The held-out set is graded once on a frozen artifact, with no per-instance feedback consumed as an iteration signal; the held-out grade is treated as an oracle, never a stopping signal. The artifact that earns the submission hash is the submission. Local-green/official-red is structurally impossible because the hash binds the captured prediction to the run that earned it.

### Preregistration and freeze {#prereg}

The artifact is frozen by an annotated git tag (`prereg-pro-v1`); every scored-run artifact cites the freeze SHA. A new tag opens a new worklog with the failure class that justified the restart named explicitly. v1 is the first scored tag.

### Provenance contract {#provenance}

Per-instance trajectories (agent sessions for each pipeline stage) are captured off-box on a polling cadence. A hypothesis graph document, captured diff, grader output, and gate trace are committed per instance, alongside a per-box ledger and cost provenance. A run earns headline status only when full provenance is published; scores alone are insufficient.

## Experimental setup {#setup}

### Datasets and eligibility {#datasets}

Two benches run under one frozen harness. **SWE-bench Verified** is a curated subset, saturated (top public submissions resolve >85% as of mid-2026) and training-cutoff-contaminated for current frontier models. OpenAI, which created Verified, [stopped reporting the score](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) in February 2026 after finding frontier models reproduce its gold patches verbatim, so the score now measures recall; it recommends Pro instead. We use Verified as a baseline that the loop ports cleanly, with companion repo `swebench-verified` and a frozen artifact under Zenodo DOI. **SWE-bench Pro** is the live contamination-resistant tier with a public/held-out split across different repos, and it is the primary validation surface. Both runs use the official harness; no bespoke graders. Defect lists are documented per bench (`KNOWN_BAD.md`) and cover bench defects only, never our failures; the eligible set is the full set minus documented defects.

The two-bench design dissociates bench saturation (Verified) from loop generality (Pro). Same loop, two contamination regimes, two independent provenance trails. If the loop carries from one to the other at comparable per-repo rates, the assembly is not bench-specific.

### Execution {#execution}

Fixed run order, no early stopping. Whole-set evaluation on a multi-box fleet with per-instance isolation. Dynamic coordination with fault-tolerant resume across box reprovisioning.

### Models and roles {#models}

No training, no fine-tuning, no reinforcement learning, no in-context demonstrations from prior instances. Frontier models are queried at their published checkpoints; the harness contains no learned weights of its own.

*Stage executors.* No stage calls the model bare. Each one invokes the provider's shipped agentic CLI: the Sonnet generator runs inside Claude Code, the GPT-5.5 challenger inside codex, and in the open-weight run the generator runs inside Cursor (Composer is itself an agent). Each of these is a ReAct loop of the vendor's own, with its own tools, file access, and turn budget. The methodeutic harness is therefore a typed meta-loop over off-the-shelf vendor agents: `inquire`, `implement`, and `attest` each delegate to one, and the harness owns only the typed stage contracts, the hypothesis graph, and the deterministic gate between them.

Two consequences follow. The baseline comparison (§(central-comparison)) holds the executor class constant, since the bare baseline is a ReAct loop of the same kind (full test-execution feedback) without the typed meta-structure, so the lift is the structure rather than a more capable inner loop. And subscription-mode replication (§(cost-envelope)) works because these CLIs are the consumer products (Claude Max, codex, Cursor) the operator already pays for.

Generator and challenger are drawn from current frontier families, deliberately cross-family to avoid mode collapse on a single training prior. Models are pluggable: the methodeutic harness and smem operate over any pair of capable frontier models with structured-output and tool-use support. We freeze the specific model versions used for this run's reproducibility, but no part of the methodology is specific to a particular model. Auth source is not part of the frozen artifact; billing mechanism is orthogonal to evaluation discipline.

Two configuration details worth disclosing, since reasoning budget is itself a labeled axis on the public boards (`[high]`, `[max]`, `[xhigh]`). The **Sonnet 4.5 generator** ran with **extended thinking enabled** (Claude Code's interleaved thinking; thinking blocks appear throughout the committed session logs), at Claude Code's default level rather than a pinned budget. The **`implement` challenger** (codex GPT-5.5) ran with **`reasoning_effort` unset (reasoning = none)**, no extended-reasoning budget, per the `turn_context` of every committed rollout. We did **not** pin or match these budgets to the comparison boards' labeled settings, so any cross-board comparison carries an uncontrolled reasoning-budget variable; the magnitude argument in §(discussion) is what bounds it (reasoning scaling is a single-digit lever, far short of the headline lift). Separately, that the challenger arbitrates with its reasoning *off* is a point against a model-deliberation reading of the gate.

*Prior-instance information boundary.* For each scored bench instance, the loop reads only artifacts derived from that instance's failing-test reproduction and its own in-cycle writes; no other instance's hypothesis graphs, trajectories, or solutions enter the model context. Pattern reuse exists at the harness-design level (typed stages, kill-condition vocabulary, gate transition table), not at the per-instance prompt level.

### Grading {#grading}

Official harness only; no bespoke graders. Bench defects are noted in one line per instance; no per-instance forensic analysis that risks becoming bench-specific tuning.

### Cost and replication envelope {#cost-envelope}

Two replication modes are validated in this work, and this run uses both in parallel. *Subscription mode*: a single frontier-vendor consumer subscription (~$200/month) covers the run at a multi-week pace, gated by per-window quota. Marginal cost at the boundary is zero; time cost is weeks. Used for the codex challenger throughout this run, and for the Sonnet generator in the early window before the API switch. *API mode*: pay-as-you-go API access at the published rate, economic Sonnet-leg cost ~$4.73 per instance (~$3.4k across the Pro run), ~$5.14 for the full frontier pair; the observed cash across the brief API window ran lower under subscription subsidy (full per-leg derivation in `COST_BASIS.md`). The two modes compose: the recorded ledger here is Sonnet API + codex subscription; a pure-API replicator pays Sonnet-side at this rate plus the vendor's published rate for the codex side. Faster, capacity-bounded by the fleet's box count rather than the quota window.

Compute requirements outside the model are minimal. The harness runs on commodity Linux boxes (we used 4× small EC2 instances during the API window): no GPU, no curated training data, no offline pipeline. Per-instance dollars and wall-time are committed to the ledger alongside the verdict and the trajectory, so replicators can audit what the run cost in real currency.

A consumer subscription, a low-four-figure API budget for the frontier pair (~$3.7k economic), or about $300 for the open-weight-generator pair puts replication within reach of graduate students, independent researchers, and small teams.

### Open-weight robustness run {#open-weight-run}

The same frozen harness was rerun **on Pro** with an **open-weight generator**: **Cursor Composer 2.5**, which [Cursor states](https://cursor.com/blog/composer-2-5) is a fine-tune of Moonshot's open-weight **Kimi K2.5** (Modified MIT), paired with **Gemini Flash 3.5** as the challenger. Composer is one instance of the open-weight class, not the point. The point is that the generation lift, `inquire` and `implement`, where the tokens and the reasoning concentrate, runs on weights anyone can download and self-host; the challenger only critiques the diff, a small fraction of the work, so Flash sits in as the next-cheapest model class rather than a second frontier model. The run is open-weight where it counts. The cross-family adversarial property (§(blind-blind)) is preserved (Cursor/Moonshot × Google), and Pro is the contamination-resistant tier where the ablation is most informative.

**The result.** The open-weight-generator pair resolved **678 / 728 = 93.1%** under the official grader, against the frontier pair's 95.3% on the same eligible set: a **2.2-point gap**, at a median **8.4 min** per instance (faster as well as cheaper). That gap is ~16 of 728 instances, and the raw open-weight rate is partly recall-inflated: a gold-overlap audit puts the open-weight model's *genuine* resolve at about three-quarters, with the contamination caveat detailed in "What it is and isn't," below. Even discounted, the cheap-model run clears the strongest bare model on Pro, and the harness-layer thesis rests on the frontier run regardless, and a little contamination in one ablation does not move it. The raw rate landing in the pre-registered "holds at a comparable rate" band (`PREREGISTRATION-cheap-ablation.md`) shows the harness ports across model pairs.

**Cost.** At public API rates the open-weight-generator pair runs **~$0.41 per instance** (economic basis; the open-weight generator priced at its open-weight Kimi K2.5 base rate), against the frontier pair's **~$5.14**: roughly **12.6× cheaper** for those 2.2 points of resolve (full line-by-line derivation in the artifact's `COST_BASIS.md`). The operator's actual cash was lower still: the Composer generator ran marginal-zero on an already-held Cursor subscription, and the Gemini Flash challenger cost about **$44 in metered API tokens across all 728 instances**, so a replicator who already pays for Cursor reproduces the full open-weight Pro run for roughly the price of the Flash side. External anchors agree on the regime: SWE-rebench prices Composer 2.5 at ~$0.23/problem, and HAL's cheapest SWE-bench agents (the cheapest of them open-weight) run under ten cents a task ([Stroebl et al. 2025](https://arxiv.org/abs/2510.11977)). The accessibility consequence is the headline: the full 728-instance Pro set replicates on a single consumer subscription, no frontier-vendor budget required. The orchestration is the value, and it ports onto self-hostable open weights.

**What it is and isn't.** This is a model-pair swap, not a clean single-factor isolation: family, capability, training cutoff, and cost-per-instance all change at once (Anthropic+OpenAI → Cursor/Moonshot+Google), with cross-family adversarial filtering held fixed; the clean per-factor ablations remain future work (§(limitations), §(future-work)). It also carries a contamination caveat we surface rather than bury. A gold-overlap audit ([`gold_divergence.py`](https://github.com/kimjune01/swebench-pro/blob/main/driver/gold_divergence.py)) finds ~23% of the open-weight wins reproduce gold's changed lines at high overlap, against ~2% for the frontier pair. The matches are not forced (on those same instances the frontier pair wins with a different patch), and the asymmetry is the tell: a weaker model reproducing the human gold patch more often than stronger ones points to recall, not capability or task-forcing (you do not reproduce a 187-line gold diff by being terse). So Composer recalls gold on a meaningful fraction of Pro instances, as expected of a model trained on public repositories, and its raw rate is partly recall-inflated. Discount the entire near-gold tail and the harness still carries the cheap model to ~three-quarters genuine resolve (~71 to 76%), above the strongest bare model on Pro (Opus 4.7, 64.3%). None of this touches the thesis: the harness-layer claim rests on the frontier clean run (§(results)) and the harness-versus-bare lift on a fixed model, where recall is equally available to both sides and cancels. The open-weight run is a cost-and-portability ablation, and a contaminated cheap model resolving ~three-quarters of Pro *genuinely* is still the harness doing the work. The run carries the same provenance contract as the headline run (per-instance trajectories, captured diffs, gate traces, cost ledger) and ships under the same Zenodo DOI: one bundle, two model-pair runs on Pro.

## Reported metrics {#metrics}

> Because the official grader returns deterministic per-instance verdicts (§(inquiry-frame)), the paper reports counts, denominators, and per-repo breakdowns rather than fitting aggregate significance tests. Per-instance verdicts are exact for the executable predicate; aggregation is bookkeeping. Cross-bench and cross-repo comparisons are presented as empirical claims, not inferential statistics, and are caveated where they appear.

### What the tables contain (per-bench) {#tables}

Counts of WIN, LOSS, and INCOMPLETE for each bench, with denominator (eligible set = full set minus documented `KNOWN_BAD.md` defects at the freeze SHA). Per-repo rows record repo, instance count, WIN, LOSS, INCOMPLETE, mean cost per instance, and median wall-time. Aggregating across repos is a weighted average over uneven coverage; we report the per-repo table as the honest read and let aggregation be a derived computation the reader can do. The cost ledger commits per-instance dollars and wall-time alongside the trajectory; replicators can audit the total run cost down to the instance. Hypothesis-graph metrics per terminal instance include graph depth at termination, frontier-closure status (closed or budget-exhausted), count of kill-conditions fired, and count of nodes added across all outer-loop iterations. The gate-routing distribution reports the frequency of each gate output (`continue-into-implement`, `re-enter-inquire`, `terminate-success`, `terminate-budget-exhausted`); the deterministic gate's behavior is itself a reportable property.

### Treatment of incomplete and faulted instances {#incomplete}

Fault classes (§(fault-classification)) are `AUTH_OUTAGE`, `QUOTA_EXHAUSTED`, `INFRA_TIMEOUT`, `CRAFT_HANG`. Classification triggers on temporal-window membership regardless of instance verdict; wins inside the window get re-run alongside losses, and asymmetric re-runs are forbidden. Each faulted instance gets one re-run; terminal verdicts stand, and faulted-again rows remain `INCOMPLETE` in the final ledger. Out-of-window verdicts stand: no reclassification of a real-output verdict on grounds of post-hoc inspection. `INCOMPLETE` gets its own column alongside `WIN` and `LOSS` rather than being folded into a denominator-mangling adjustment, so the reader sees the bounded honest cost of the run.

### Two-bench reading {#two-bench}

For each repo present in both eligible sets, we report the per-repo Verified count and Pro count with denominators. We present both numbers per repo side by side, and leave whether the assembly carries to the reader's interpretation. We do not report Wilson CIs, paired tests, or equivalence procedures. The per-instance verdicts are deterministic; aggregation is bookkeeping. A reader who wants confidence intervals can compute them from the published counts.

### Independent re-grade {#re-grade}

Two independent re-grades were run, each applying the captured diff plus the **unmodified** official harness on a clean container with no agent re-run, confirming or refuting the original WIN per instance. On the **frontier run**, six cross-language WINs (3 Go / 2 Python / 1 TS) reproduced **6/6** RESOLVED, a spot-check against a trivial capture bug. On the **open-weight run**, a **60-WIN stratified sample** (across all repos) re-graded on a clean independent grader reproduced **60/60, 0 flips** (`driver/regrade_wins.py`; separate ledger `runs/scored/regrade_win.jsonl`, originals untouched). Both validate the *reproducibility* of the recorded WINs (the captured diff really passes the official grader), not test *coverage* (a weak fail-to-pass set can still pass). Same-grader re-grade is deterministic, so 0 flips on the 60-sample implies ~0 across the rest; a full independent re-grade of all WINs is feasible and unrun.

### Open-weight robustness run (§(open-weight-run)) {#open-weight-metrics}

Same counts, same tables, computed independently for the open-weight run (Composer 2.5 generator + Flash challenger). The Sonnet+codex per-instance verdict and the open-weight per-instance verdict are reported side by side for each instance in the intersection. The disagreement count is read directly; no statistical procedure applied.

### Current results {#results}

*Verified (closed, public).* 426 / 438 eligible WIN under the official grader. Denominator-explicit; per-repo table committed to the `swebench-verified` repo's `results/` directory; Zenodo DOI pins the frozen artifact. The full 500-instance Sankey (eligible 438 = 500 − 44 sphinx-doc offline-infeasible − 18 documented `KNOWN_BAD.md` defects) is in the companion README.

*Pro (terminal, frozen tag `prereg-pro-v1`).*
- **694 WIN / 34 LOSS = 95.3%** on 728 eligible (731 dataset instances − 3 gold-patch defects excluded pre-run and documented). **0 INCOMPLETE**: the whole eligible set carries a terminal verdict, graded in one measurement.
- **Most wins are first-pass.** Of the 694 wins, 648 carry a complete captured trajectory; among those, the first `inquire` → `implement` → `attest` pass carries **~93%** (602) and re-entry recovered the remaining **~7%**. The 46 wins outside that set keep their committed diffs and official verdicts; only the per-pass trajectory is incomplete, so they sit outside this ratio. First-pass is *not* implement-and-check: that single pass still runs abductive `inquire`, building the hypothesis graph before any code, then `implement` and `attest`. So the stat rules out **re-entry** as the lever and says nothing about the within-pass graph, which every win uses; the cross-loop layer is a small recovery tail; the within-pass machinery is where the result is made (§(central-comparison)).
- Run span ~3.5 days (first dispatch 2026-05-27, last verdict 2026-05-30), through three provider-credential stalls and a mid-run Max-subscription → paid-API billing switch, with 0 instances lost.
- Per-repo (11 public repos): ten of eleven resolve at 92.3% or above; NodeBB is the lone outlier at 74.4% and contributes 11 of the 34 losses. Per-repo W/L, %win, and runtime quantiles are committed.
- **No development-overfit signal.** The harness was iterated on Verified (all Python) before this run; if that overfit the pipeline, the development language should resolve *higher*. It resolves lower: Python (dev language) 94.7% versus non-Python (Go/TS/JS, never touched in development) 95.7%. The strongest language (Go, 98.6%) and the weakest (JS/NodeBB, 74.4%) are both novel. The freeze does not defend against overfit here; this direct check does.
- **All 34 losses have non-empty captured patches**: every loss is the loop producing a fix the official tests rejected, not failing to produce one. A by-hand read of the diffs (a provisional characterization, not a re-grade) puts the true *capability*-loss count below 34: at least one is a verified serialization defect (capture stripped the diff's string-literal quotes, making it unparseable, a manufactured false loss), ~4 are capture/serialization defects, and the leading band (~19) is gate-vs-official-mismatch *candidates*, where the local audit was satisfied but the official grader rejected, where a stricter audit gate, not necessarily a smarter model, might close the gap, though some may be genuine capability misses until a re-grade confirms. These hand-read categories are a provisional split, not a measured one, and are not yet claimed to exhaust the 34.
- **Independent re-grade spot-check: no binding leak.** Six cross-language WINs, re-graded from the committed diffs on fresh containers under the unmodified official grader with no agent re-run, all six reproduced RESOLVED (6/6).

The per-instance Pro artifact bundle (trajectories, captured diffs, gate traces, and cost ledger for all 728) is committed at the frozen tag; the Zenodo DOI pinning it is forthcoming, on the same publication discipline as the Verified artifact (§(provenance)).

The provisional 2026-05-28 snapshot read 97.0% on the 402 early-order instances, but the final number is lower, just as that snapshot's own projection anticipated: the heavy tail (NodeBB and the harder repos) sat in the then-ungraded remainder, and grading it pulled the rate down to 95.3%.

*Pro (open-weight-generator pair, terminal, frozen tag `prereg-pro-v1-cheap`).* The same frozen harness with the model pair swapped to **Composer 2.5** (Kimi K2.5 fine-tune) generator + **Gemini Flash 3.5** challenger resolved **678 / 728 = 93.1%** under the same official grader: a **2.2-point gap** below the frontier pair, at median **8.4 min** per instance and economic **~$0.41/instance** (~12.6× cheaper than the frontier pair; §(open-weight-run)). Per-instance trajectories, captured diffs, gate traces, and cost ledger are committed under the shared bundle (`runs/flash-composer/`); a 60-WIN stratified re-grade of this run reproduced **60/60, 0 flips**. Read against the scaffold control (§(central-comparison)): the model-pair swap moves the rate two points while the scaffold swap moves it about fifty, so the harness is the dominant lever. This is a scaffold-vs-scaffold comparison against a public attested baseline, not a clean isolation of individual harness components (those ablations are future work, §(future-work)).

*Cost (Pro ledger).* The portable figure is the **economic** basis, every leg priced at public API rates including cache: **~$5.14 per instance** for the frontier pair (Sonnet 4.5 leg ~$4.73 + GPT-5.5 ~$0.42), against ~$0.41 for the open-weight-generator pair. The operator's actual cash was far lower: most legs ran on flat subscriptions (Claude Max, codex) at ~$0 marginal, only ~310 Sonnet instances were billed to API ($813.52), plus ~$58 EC2, so marginal cash was ≈ **$870**. Cash and economic are different bases, kept separate; the full per-leg derivation and the cash-vs-economic reconciliation are in the artifact's `COST_BASIS.md`, and the per-instance ledger is committed alongside the trajectories.

*Verification cost.* Verification doesn't require re-running the full bench. A representative re-grade sample (the §(re-grade) protocol uses N = 20 stratified-random WINs) costs ~$3 × N at the observed Sonnet-API rate: ~$60 for the planned re-grade. The bar to audit this work is API access, an AWS account (or equivalent compute), and discretionary spend in the tens of dollars.

*OSS deployment trace.* **81 PRs merged across 73 cold repositories** (codebases the operator does not own and the models held no training priors for, 0 self-owned, median merged diff 49 lines) under adversarial maintainer grading; a **50.6% merge rate** (81 of 160 decided PRs = merged / merged+closed-unmerged under the `sweep` campaign tag). That rate is a floor on correctness, not an estimate of it: a close-reason audit found only ~8 of the 79 closures were rejections on the merits, the rest no-AI policies, AI discrimination, author withdrawals, and duplicates, so the share of *correct* fixes runs well above 50%. 67% positive maintainer engagement on 65 issues filed since the slop-filter campaign start (engagement = reproduce-confirmed, assigned, or commented as actionable). The frozen ledger ships in the artifact (`pr-receipts.jsonl` + `pr-receipts.VERIFY.md`) and stays GraphQL-verifiable against live GitHub; the per-failure-mode breakdown is in the committed OSS hypothesis graph. ~380 hypothesis graphs publicly committed in `sweep/repo-hypotheses/` are the upstream funnel from which submissions are drawn.

*Operator role in the deployment trace.* No human-authored code in any of the 81 merged PRs, no prompt-level steering during the runs, and no human curation of which issues to work on. The harness samples *issues* (not repos) at random from a universe defined as filed issues on ≥200-star open OSS repos across roughly 9 languages, then runs `inquire` / `implement` / `attest` autonomously, writes the patch and PR body, and submits. The full deployment story (slop-filter campaign, drip discipline, maintainer-pushback evolution) is in the companion post [Speedrunning Open Source](/speedrunning-open-source). Issue-first sampling matters: every attempted instance is a problem someone filed because they wanted it fixed, which sidesteps the failure mode of repo-first sampling (pick a codebase, contrive work for it). The human role is strictly upstream (define the harness, define the sampling universe) and operational (kick off runs, manage cost), not authorial, not directive, not selective. The 50.6% merge rate is the rate at which adversarial maintainers accept *agent-selected, agent-authored, agent-submitted* code into codebases the operator does not maintain, on problems the operator did not pick.

## Limitations {#limitations}

Could the models have trained on these repos? Public Pro is training-cutoff-contaminated for both model families used, a property of the bench shared by all submitters, not an isolation of method as the cause. Our own holdout is weaker still than Scale's: different commits, same repos. Cross-repo generalization to Pro's held-out partition therefore stays untested locally. What we can do, we do: training-cutoff math for both models is published explicitly, with per-instance date overlaps disclosed.

One-shot held-out discipline is verifiable only at submission time. The submitter-side invariant (no held-out feedback in the artifact) is necessary but not sufficient. The run is cost-bounded; heavy repos may be under-represented or over-budgeted depending on order, with cost and time logged per instance.

Selection of generator and challenger families is a hyperparameter we do not ablate. The ablation that would isolate the loop's effect (with vs without the typed-mode constraint, on one fixed model) is a separate clean-room study. Because no training or fine-tuning occurs, pretraining-cutoff contamination is the channel most directly auditable from the artifact (cutoffs vs instance dates). Other channels (leaderboard feedback, harness tuning, known-bad-list leakage, retry policy, run-order effects) are handled by §(fault-classification)–§(provenance) (preregistration, frozen harness, one-shot held-out, published failure list, frozen run order).

The smem is small. Hypothesis graphs in this work are per-instance, and cross-instance memory accumulation remains future work, so the smem proposal is tested only in its simplest non-trivial regime. That regime does carry a deflationary point worth stating plainly: the memory here is a single markdown file, not a vector store or a graph database, and it was never the bottleneck at any repo size in the eligible set. Whether a heavier store earns its keep is a question for cross-instance scale, not for per-instance inquiry.

*Causal attribution.* The open-weight robustness run (§(open-weight-run)) has terminated. On raw resolve, swapping the *entire* frontier pair for open-weight models on a byte-identical harness costs only 2.2 points (95.3% → 93.1%). But a gold-overlap audit shows the open-weight rate is partly recall (~18 to 23% of its wins reproduce gold; §(open-weight-run)), so that 2.2 understates the genuine model-tier gap, which is ~17 to 22 points once the recall tail is discounted. The model tier is therefore not negligible. What the run does establish at factor level is narrower and still strong: a byte-identical harness lifts even a cheap, self-hostable model to ~three-quarters genuine resolve, far above any bare model, so the *harness lift* is largely model-independent even though absolute capability is not. Separating *which* harness component earns that lift is unaddressed: the ~50-point lift over the bare standardized baseline still bundles structure, generic agent-engineering, and the generator's thinking-on config (§(models)). The magnitude argument (§(discussion)) shows reasoning scaling cannot account for a lift this size; separating structure from generic agent-engineering is the per-factor ablation (typed-mode on/off, blind-blind on/off, gate determinism on/off), which remains future work (§(future-work)).

## Discussion {#discussion}

> Both surfaces are closed. Verified: 426 / 438 eligible, frozen, Zenodo-DOI'd, public. Pro: 694 / 728 eligible = 95.3%, 0 incomplete, whole eligible set graded under the official grader at frozen tag `prereg-pro-v1`. Pro landed about 2 points below Verified (97.3%); the per-repo and loss readings below say where the gap lives.

The harness ports cleanly to industrial code across both contamination regimes, each with full per-instance provenance: captured diffs, trajectories, and cost ledger committed. Verified is public and Zenodo-DOI'd; the Pro bundle is committed at the frozen tag with its DOI forthcoming. The hypothesis-graph smem records typed inquiry decisions per run (kill conditions fired, verdicts and routes recorded); whether those records prove reusable across instances and across benches remains future work at cross-instance scope. The deterministic gate produces reviewable termination traces: an external auditor can replay its decision against the captured trajectory and budget, and the routing is reconstructible from the evidence trace alone.

Does the Peircean framing do any real work, or is it decoration? Reproducibility comes from the captured trace, the frozen artifact, the deterministic gate, and the verdict and route feeding it, not from Peirce. Peirce names the contract vocabulary and makes it legible; but it is the mechanical enforcement (stage contracts that reject mode-freelancing inputs, captured trajectories with hypothesis-graph snapshots, finite-state gate logic, deterministic verdict-to-routing mapping) that lets the run replay.

We designed the composition for principled reasons. Its hypothesis-graph shape (Peirce-typed nodes, kill-conditioned edges, disjoint stage read/write contracts, model-free gates) closes known failure modes of LLM agents: mode collapse, confabulation, unauditable revision, vibes-based termination. The design rationale is independently inspectable from the artifact, and Verified shows the design clears industrial code at a 97.3% eligible rate. Pro then replicates it within about 2 points (95.3%), across a repo set with zero overlap with the development surface, and the gap is concentrated, not regime-wide. Nine of eleven Pro repos resolve above 95%; the deficit lives almost entirely in NodeBB (74.4%). The development-overlap check is the decisive one: the development language (Python) resolves *lower* than the never-developed languages (Go/TS/JS), so the Verified→Pro gap is not contamination-regime asymmetry leaking through; it tracks per-repo difficulty. At the per-repo level the assembly reads as bench-agnostic and contamination-regime-agnostic, with NodeBB the one repo that names where the harness is weakest.

Could reasoning scaling account for a lift this size? Bolting reasoning onto a fixed model is a single-digit lever on this bench: Sonnet 4.5 moves 77.2 → 82 on Verified with parallel test-time compute (~5 points), and extended-thinking deltas are the same order. The harness lift over the same model's bare standardized Pro score is ~50 points (43.6 → 95.3), an effect an order larger than any reasoning-budget delta, so it is not a reasoning artifact. This bounds the confound without isolating the cause: the ~50 bundles the typed-inquiry structure, generic agent-engineering (turn budget, tools, retries), and the generator's thinking-on configuration (§(models)), measured against a thinking-off and contaminated baseline. Separating the methodeutic structure from generic agent-engineering is the per-component ablation scoped in §(future-work). A mechanistic interpretation of the gap, and a qualitative read of the open-weight run's committed hypothesis graphs, are offered in the [repository's speculative analysis](https://github.com/kimjune01/swebench-pro/blob/main/docs/DISCUSSION.md#speculative-analysis-why-the-lever-is-the-harness) and labeled there as speculation.

The OSS PR record (81 merged across 73 cold repos, 50.6% merge rate, adversarial maintainer graders; GraphQL verifiers pinned at `kimjune01/kimjune01@paper-2026-05-28/README.md`, since the profile README itself drifts) reports what the harness does on contact with non-curated codebases. The receipt is *agent-selected, agent-authored, agent-submitted* (§(results), and the longer story in [Speedrunning Open Source](/speedrunning-open-source)): the harness samples issues at random from a 200-star-floor universe across ~9 languages and runs the full loop without human keystrokes in the diff or natural-language steering during operation; the human role is harness-design and operations. This closes at once the four reviewer reflexes that dismiss agent-coding demos: cherry-picked issues, fabricated problems, vibe-coded patches, developer-assist authorship. The ~380 publicly committed hypothesis graphs at `kimjune01/sweep/repo-hypotheses/` are the deployment trace: skip verdicts, dead-end paths, engage decisions. This is ecological; the deployment surface lacks a within-instance comparator, and isolating the typed-mode constraint requires the per-factor ablations scoped in §(future-work), though the model-tier contribution is already bounded at two points by the now-terminal open-weight robustness run (§(open-weight-run)). The merge rate is well above the AI-slop floor visible in the same pinned commit's slop table for contemporaneous unstructured attempts.

Portability follows from the no-training stance. The harness contains no learned weights of its own; anyone with frontier-model API access can clone the repo, swap in their model pair, and run the loop without training compute, curated datasets, or GPU resources. Weights are pluggable; the cost envelope (§(cost-envelope)) fits inside an individual researcher's discretionary spend.

One peripheral note on bench infrastructure: held-out validity is partly a function of who gets graded. Published access rubrics (the way submission formats are published) would strengthen Pro's claim to be community infrastructure. We offer this as a structural observation.

One further structural observation, on token efficiency. The per-instance cost and token ledger (§(results)) translates to substantially fewer tokens per resolved instance than vendor-published agent runs at comparable resolve rates on Pro-class instances: the per-instance ledger committed alongside the trajectories lets a reader compute the comparison directly at API-published per-token rates. Token efficiency at this scale appears as a harness-level property in this artifact, not a model property; the underlying models are the same frontier checkpoints anyone else calls. The lever is orchestration craft, and the artifact that carries it is a markdown file plus pinned dependencies, distributable at git-clone latency.

A practitioner recommendation falls out of the two model-pair runs. For the class of problems SWE-bench Pro represents, a cheap model in the methodeutic harness is cost-effective: the open-weight Composer 2.5 configuration (§(open-weight-run)) resolves 93.1% at ~$0.41 per task, and even discounting its recall tail it genuinely resolves ~three-quarters, far above any bare model. But the raw two-point margin to the frontier pair understates what escalation buys: on contamination-free problems the genuine-capability gap is ~17 to 22 points (§(open-weight-run)), concentrated in the hard tail. So default to the cheap model for cost-sensitive work on well-trodden code; escalate to a frontier generator for novel problems and the heavy repos, where recall does not carry the cheap model. The harness stays constant; the model is the dial, and the dial matters more on genuinely new problems than the raw Pro rates suggest.

## Related work {#related-work}

### SWE-bench, contamination, and cost transparency {#rw-swebench}

The SWE-bench family defines the Verified / Pro lineage, official harness, and contamination-resistant tier design. **SWE-rebench** ([swe-rebench.com](https://swe-rebench.com/)) uses post-cutoff filtering as a parallel contamination strategy and publishes per-problem cost figures (e.g., Cursor Composer 2.5 at $0.23/problem), used here as the price anchor for the open-weight robustness run in §(open-weight-run). **HAL** (Holistic Agent Leaderboard; [Stroebl et al. 2025](https://arxiv.org/abs/2510.11977), ICLR 2026) is the third-party, cost-aware agent leaderboard, built explicitly because agent evaluations rarely report cost; it publishes accuracy-vs-cost Pareto frontiers across nine benchmarks and is the nearest infrastructural precedent for this paper's cost-transparency stance. Its cheapest SWE-bench agents run under ten cents per task, the cheapest of them open-weight, corroborating §(open-weight-run)'s cost regime from an independent harness. HAL commits all agent logs (2.5B tokens of model calls) and its harness code, the most transparent release among these precedents; this paper's receipts go one level finer, to the per-instance re-gradeable verdict (captured diff plus official grader output per task), where a reader reproduces a single number rather than inspecting the aggregate.

**Adaptive data analysis** (Dwork et al.) provides formal grounding for held-out-budget discipline. The **official SWE-bench experiments repo** ([github.com/swe-bench/experiments](https://github.com/swe-bench/experiments/)) requires `trajs/`, `logs/`, `patch.diff`, `report.json`, and `test_output.txt` per submitted instance, establishing the minimum publication norm; our provenance contract extends it with gate traces, hypothesis graphs, and cost ledger. The **Nilenso SWE-bench Pro trajectory analysis** ([nilenso.github.io/swe-bench-pro-cost-token-time-analysis](https://nilenso.github.io/swe-bench-pro-cost-token-time-analysis/reference.html)) reports deterministic intent classification, exit statuses, structural markers, and cost/error signals across four frontier models on Pro; closest precedent on Pro cost transparency, short of a per-instance dollar ledger. The **Datacurve DeepSWE leaderboard** reports median per-trial cost for frontier models on Pro-class instances (e.g., GPT-5.5 at ~$5.80/trial median); journalism-level cost data, short of a structured ledger.

### Agent scaffolds, embodied loops, and SE-agent harnesses {#rw-scaffolds}

SWE-bench-targeted agent harnesses include OpenHands (Wang et al. 2024), SWE-agent (Yang et al. 2024), and AutoCodeRover (Zhang et al. 2024/25). These are methodological neighbors with different scaffold trade-offs; none implements Peirce-typed stage contracts or a kill-conditioned hypothesis-graph memory. **Voyager** (Wang et al. 2023) is the closest loop-shape precedent: embodied observe→hypothesize→test→commit in Minecraft. We adopt the loop shape, type its stages with Peircean modes, substitute kill-conditioned hypothesis graph for skill library (falsifiable belief in place of verified code), and re-substrate to industrial code. **Invariant Risk Minimization** (Arjovsky et al. 2019) is tri-abductive figure-ground splitting under environment variation; a third witness to the loop pattern from distributional generalization. **SWE-Replay** (2026) evaluates a test-time scaling method across Verified, Pro, and Multilingual; adjacent on cross-bench evaluation, runs without a frozen-artifact preregistration.

Two concurrent developments arrived independently at adjacent points in the same design space, each carrying one of the two structural components this paper composes. Naming them explicitly is the cleanest way to state the contribution: **Theorem-of-Thought** ([Abdaljalil et al. 2025](https://arxiv.org/abs/2506.07106)) is a multi-agent framework that types reasoning into abductive, deductive, and inductive specialist agents per query: the typed-cycle component, run without a persistent typed memory across cycles. **Cognitive Memory Manager** ([Khalid & Arora, ACM CAIS AgentSkills 2026](https://openreview.net/forum?id=yCsHQnvvWY)) extracts a typed-node DAG ("reasoning graph") by observing agent execution and mines it for recurring patterns to promote to portable SKILL.md files: the typed-graph component, run without a methodeutic harness driving the writes. Neither work is a precedent in the lineage sense; each is a sibling reaching one of the two halves independently. That three labs converged on these decompositions without coordination is itself the structural evidence: typed reasoning and typed memory are landing as natural primitives in this design space. Provenance for the framing developed here is timestamped on the project blog (see [The Hypothesis Graph](https://june.kim/the-hypothesis-graph) and [Evidence has a trajectory](https://june.kim/evidence-has-a-trajectory)).

What this paper composes: the methodeutic harness **writes** the typed graph prospectively (with kill conditions ahead of evidence and a verdict written back at attest time), the harness **reads** the graph to drive the next move, and a deterministic gate closes the cycle on the attest verdict and route rather than model self-judgment. Same graph primitive as CMM, opposite epistemological direction: CMM's graph is descriptive (mined from traces); the one here is generative (it routes the run). Same Peircean typing as ToT, pinned to persistent nodes that survive across cycles rather than dissolved per query. The composition is what the bench result is testing.

Table 1 lays out the cell-by-cell comparison spine for the systems treated below in §(typed-memory); the prose adds nuance the table can't carry.

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

<figcaption style="text-align:center; font-size:12px; color:#666; margin-top:-0.5em;"><strong>Table 1.</strong> Comparison spine for adjacent typed-reasoning and graph-memory LLM-agent systems. Cell terseness is by design; prose nuance in §(typed-memory). Adversarial filtering and termination are separately tabled in §(adversarial-termination).</figcaption>

### Typed reasoning and graph-structured memory {#typed-memory}

**IDEA** (He et al. 2025, ACL Findings, [arXiv:2408.10455](https://arxiv.org/abs/2408.10455)), *Enhancing the Rule Learning Ability of Large Language Model Agent through Induction, Deduction, and Abduction*, explicitly cites Peirce and uses the three modes in an interactive LLM-agent rule-learning benchmark. **ADI** (Gilda & Gilda 2026, [arXiv:2604.15727](https://arxiv.org/abs/2604.15727), April 17 2026), *Structured Abductive-Deductive-Inductive Reasoning for LLMs via Algebraic Invariants*, gives an explicit Peircean tripartite protocol with epistemic layers (L0/L1/L2) over a symbolic knowledge graph; near-simultaneous with this paper's draft and the most conceptually adjacent prior work. Both target reasoning domains outside SE (rule learning, algebraic invariants); this paper targets SE agents on real industrial code under benchmark and adversarial-maintainer evaluation. Table 1 carries the cell-by-cell methodological diff.

The hypothesis-graph assembly sits at the intersection of three lineages: cognitive-architecture memory (Soar / ACT-R / EPIC), LLM-agent memory systems (CoALA / AriGraph / Mem0 / Zep), and typed-belief / falsifiability representations (CausaLab / BeliefMem / Theorem-of-Thought / CMM). This paper adopts the decades-old Soar memory typology (semantic / procedural / episodic) directly as its slot vocabulary (the hypothesis graph fills the `smem` slot, pipeline-stage skills fill `pmem`, captured trajectories fill `epmem`), adding only the specific content of the `smem` slot (Peirce-typed, kill-conditioned, designed for LLM prose read/write). Adjacent LLM-agent work:

- **Kirk, Wray & Laird 2023** ([AAAI](https://ojs.aaai.org/index.php/AAAI-SS/article/download/27690/27463/31741)): Soar/ITL agent queries an LLM and encodes into Soar-shaped memory; LLM-port of the Soar lineage.
- **CoALA** (Sumers et al. 2023/24, [arXiv:2309.02427](https://arxiv.org/abs/2309.02427)): cognitive-architecture framework for language agents with modular memory.
- **AriGraph** (Anokhin et al. 2024/25, [arXiv:2407.04363](https://arxiv.org/abs/2407.04363)): knowledge-graph world models for LLM agents in TextWorld; closest precedent for graph-structured LLM-agent memory.
- **CausaLab** (Yang et al. 2026, [arXiv:2605.26029](https://arxiv.org/abs/2605.26029)): LLM agents maintain evolving structural-causal-model hypotheses in a DSL; strong adjacent on persistent inspectable hypothesis representation.
- **BeliefMem** (Liao et al. 2026, [arXiv:2605.05583](https://arxiv.org/abs/2605.05583)): candidate conclusions with non-LLM Noisy-OR updates; strong adjacent on uncertain alternatives + mechanical update.
- **Theorem-of-Thought** (Abdaljalil et al. 2025, [arXiv:2506.07106](https://arxiv.org/abs/2506.07106)): abductive / deductive / inductive *agents* produce traces structured into formal reasoning graphs; the strongest Peirce-mode adjacent, but modes operate at the agent/trace level rather than typing persistent-memory nodes.

**CMM** (Khalid & Arora 2026, *From Observed Reasoning to Stable Skills*, Agent Skills '26, [OpenReview](https://openreview.net/pdf?id=yCsHQnvvWY); published one day before this draft) is the closest contemporary precedent on typed-DAG coding-agent memory and warrants its own comparison. CMM captures coding-agent execution into a typed DAG (seven node types: HYPOTHESIS / INVESTIGATION / DISCOVERY / PIVOT / DEAD_END / SOLUTION / CONTEXT_LOAD), graduates recurring patterns into stable `SKILL.md` files under a human-approval gate, and serves them to future runs.

*Convergent role, categorically different runtimes.* Both systems converge on the same role for memory: a persistent, typed, queryable DAG of reasoning artifacts. The runtimes diverge on agency. CMM is **observe-and-consume**: an external coding agent perturbs, CMM types the trajectory post-hoc, future runs consume the graduated skills. Our loop is **perturb-and-falsify**: implement applies the patch, attest runs the test, kill conditions fire mechanically during the live inquiry. CMM extracts and serves; our harness *is* the actor. CMM applies types at extraction time at the consumption layer; we apply types at write time at the production layer (each stage mechanically rejects mode-freelancing inputs). Same data structure, opposite epistemological direction.

*Cold-start vs prior session history.* CMM's demonstrated advantage in its published case study depends on six months of one developer's prior sessions, with graduation thresholds of 3+ sessions per project-scoped pattern. Our loop operates on previously-unseen instances cold, with zero per-developer tuning. Different evaluation regimes; the asymmetry is the contribution of memory format, not memory quality.

*Complementary by construction.* The ~380 hypothesis graphs publicly committed in `sweep/repo-hypotheses/` are exactly the kind of structured corpus CMM's graduation algorithm could ingest to extract specialized per-repo skills. A future system could chain them: our loop produces structured inquiry traces across many instances; CMM's graduation pipeline consolidates those traces into developer-or-repo-specific skills. Table 1 (above) carries the cell-by-cell methodological diff on typing locus, persistent structure, edge update, and gate; this prose covers the temporal nuance the table can't.

> *Production LLM memory systems with graph variants (Zep/Graphiti, Mem0), staged-hypothesis selection in science agents (DeepScientist), domain-specific hypothesis swarms (drug discovery), deterministic gating in adjacent settings (MemLineage, ROE Gate, Certifying-Risks, FVA-RAG, GHS-TDA), and reflective memory systems (Reflexion, DebugMate, Potpie) are surveyed in the appendix. They are adjacent in particular axes but do not change the cell-by-cell comparison spine above.*

### Adversarial filtering and termination {#adversarial-termination}

Table 2 compares adversarial multi-model setups on stage of operation, visibility regime, and cross-family use.

<div class="table-wrap">
<table class="relwork-table" style="margin:1em auto; font-size:13px; border-collapse:collapse; line-height:1.35;">
<colgroup><col style="width:18em"><col style="width:11em"><col style="width:14em"><col style="width:13em"><col style="width:11em"></colgroup>
<thead><tr><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">System</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Domain</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Stage operated at</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Visibility regime</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Cross-family</th></tr></thead>
<tr><td>Multi-Agent Debate (Liang et al. 2023/24, <a href="https://arxiv.org/abs/2305.19118">arXiv:2305.19118</a>)</td><td>General reasoning</td><td>Patch / answer stage</td><td>Open (cross-visibility)</td><td>Single model family</td></tr>
<tr><td>Refute-or-Promote (Agarwal 2026, <a href="https://arxiv.org/abs/2604.19049">arXiv:2604.19049</a>)</td><td>Defect discovery</td><td>Review stage</td><td>Asymmetric context</td><td>Yes</td></tr>
<tr class="ours"><td>This work</td><td>SE (industrial code)</td><td>Pre-patch hypothesis stage</td><td>Blind pushout (no cross-visibility)</td><td>Yes (Sonnet + GPT-5.5)</td></tr>
</table>
</div>

<figcaption style="text-align:center; font-size:12px; color:#666; margin-top:-0.5em;"><strong>Table 2.</strong> Adversarial multi-model filtering: comparison axes are stage and visibility, where this work occupies the pre-patch / blind cell.</figcaption>

Table 3 compares termination disciplines. The axes are *what* the system reads to stop, *how* it stops, and the scope at which the stopping decision lives.

<div class="table-wrap">
<table class="relwork-table" style="margin:1em auto; font-size:13px; border-collapse:collapse; line-height:1.35;">
<colgroup><col style="width:18em"><col style="width:14em"><col style="width:18em"><col style="width:11em"></colgroup>
<thead><tr><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">System</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Stopping signal</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Mechanism</th><th style="background:#f0f0f0; padding:4px 8px; text-align:left;">Scope</th></tr></thead>
<tr><td>λ_A: Typed Lambda Calculus for LLM Agent Composition (2026, <a href="https://arxiv.org/abs/2604.11767">arXiv:2604.11767</a>)</td><td>Bounded fixpoint</td><td>Type-theoretic termination proof</td><td>Composition-level</td></tr>
<tr><td>SafetyDrift (2026, <a href="https://arxiv.org/abs/2603.27148">arXiv:2603.27148</a>)</td><td>Absorbing state</td><td>Markov-chain risk analysis</td><td>Trajectory-level</td></tr>
<tr class="ours"><td>This work</td><td>Attest verdict + re-entry route</td><td>Deterministic finite-state gate over (verdict, route, attempts, budget)</td><td>Per-instance</td></tr>
</table>
</div>

<figcaption style="text-align:center; font-size:12px; color:#666; margin-top:-0.5em;"><strong>Table 3.</strong> Agent-termination disciplines. The verdict-routed gate this paper deploys sits at the per-instance scope on the attest verdict and route, where neighboring work sits at composition- or trajectory-level on type-theoretic or risk-analytic signals.</figcaption>

## Future work {#future-work}

Six directions follow from this work.

- **Held-out submission** under the same artifact and one-shot discipline.
- **Cross-instance smem accumulation:** letting the hypothesis graph grow across instances within a repo, then across repos within a domain; the current work tests the smem at per-instance scope.
- **Clean-room ablation** on post-cutoff instances (SWE-rebench), with and without the typed-mode constraint on one fixed model, to isolate the loop's effect on the rate.
- **Skill-level retros:** which stages of the loop carry which kinds of wins, and targeted skill freezes for follow-on benches.
- **Cyclic hypothesis graphs:** relaxing Pearl's acyclicity to stay faithful to cyclically-causal inquiry (cascading failure, retry storms), with termination resting on the gate rather than on graph topology; every graph committed here is acyclic, so the affordance is unexercised in this corpus and its treatment is developed separately.
- **How is it *not* good enough:** the symmetric question to this paper's *how is it this good*. The gate's one job is to decide termination, and on the 34 losses it terminated runs whose captured patch did not resolve, so characterizing those terminations (budget-exhausted versus re-entry-exhausted, and whether a richer gate would recover any) reads where the gate's discipline trades wins for reproducibility.

The methodeutic-harness IR is not SWE-bench-specific. Any benchmark with falsifiable predicates and deterministic per-instance verdicts (HumanEval, MATH, theorem-proving suites, ARC, formal verification tasks, structured-output extraction) admits the same shape: abduction generates candidates, deduction derives an intervention, induction runs the predicate, the hypothesis graph carries belief, the deterministic gate routes on the verdict. SWE-bench is only the workload demonstrated here; the IR itself ports.

Beyond SWE-bench, the harness is one chapter of a broader program: a compiler from prose to executable agent behavior, of which the methodeutic harness is the intermediate representation, the hypothesis graph the typed memory, and skills the compiled units. The program is developed at length in the [methodeutics textbook](https://june.kim/reading/methodeutics); *"compiler"* is used descriptively, in the LLVM (Lattner & Adve 2004) and DSPy (Khattab et al. 2023) lineage of typed pipelines from specification to reproducible behavior. In the LLVM / GCC tradition where a compiler is built with itself, elements of this harness were developed by applying earlier versions to its own design tasks ([the longer treatment](https://june.kim/investigation)); the published receipts are from the post-bootstrap frozen artifact.

## Availability and reproducibility {#availability}

- **Repositories.** github.com/kimjune01/swebench-pro and github.com/kimjune01/swebench-verified.
- **Frozen artifact.** Git tag `prereg-pro-v1`, SHA committed in the worklog.
- **Preregistration.** `PREREGISTRATION.md` at the freeze SHA.
- **Provenance artifacts.** Per-instance trajectories, hypothesis graphs, captured diffs, gate traces, and cost ledger under `runs/scored/artifacts/`.
- **OSS deployment trace.** Public corpus of ~380 hypothesis graphs at `kimjune01/sweep/repo-hypotheses/`, one per investigated issue across 46+ repositories. PR-level outcomes (merged / closed-unmerged / open) are pinned at `kimjune01/kimjune01@paper-2026-05-28` (the profile README itself drifts; the pinned commit is the citable artifact).
- **OSS metrics are recomputable, not asserted.** Every numeric claim in the deployment trace (merge rate, repo count, issue reception) ships alongside the **GitHub GraphQL query** that produces it. A skeptic with any GitHub token can paste the query into the GraphQL explorer and recompute the number in under a minute. No statistic is presented without its verifier. This is the same anti-grift mechanism as the bench's per-instance provenance, ported to the wild-deployment surface.
- **Replication budget.** Economic ~$5.14/instance for the frontier pair (~$3.7k across the Pro bench) or ~$0.41 for the open-weight-generator pair (~$300), at public API rates; or a single consumer subscription plus patience. See §(cost-envelope).
- **Companion textbook.** A reader-facing synthesis of the same dispersed lineage is available at june.kim/reading/methodeutics. The paper's argument rests on the primary sources cited in §(grounding) and §(related-work), not on the synthesis; the textbook is a navigation aid, not authority.
- **Public-provenance trail.** Dated blog posts at june.kim establishing the framework: *Theory is load-bearing* (2026-03-17), *The proof manual* (2026-04-05), *Type the question* (2026-04-08), *Evidence has a trajectory* (2026-04-27), *The hypothesis graph* (2026-04-28), *Abduction* (2026-05-04), *Modes of reason* (2026-05-04). These predate CMM (2026-05-26) and ADI (2026-04-17) and establish parallel rather than derivative development.
- **PDF.** Arxiv-shape build at [/assets/methodeutic-harness-paper.pdf](/assets/methodeutic-harness-paper.pdf). Rebuilt from the markdown source by `scripts/build-paper-pdf.sh`; the source is canonical.
- **DOI.** [placeholder: Zenodo paper-DOI distinct from the software-DOI.]
- **License.** Skills are released free and openly under **CC-BY-SA-NS** (see [june.kim/cc-by-sa-ns](https://june.kim/cc-by-sa-ns)). Repo-level terms in `LICENSE.md`. The harness, the skills, the trajectories, the hypothesis graphs, the gate logic: all freely available for inspection, replication, modification, and reuse under attribution + share-alike + no-spam terms. No paywall, no gated access, no enterprise tier; the harness an outsider clones is the same harness that produced the published numbers.

**Reproducibility invitation.** *Nullius in verba.* The repository, per-instance trajectories, hypothesis graphs, gate traces, captured diffs, and cost ledger are public. The harness runs end-to-end on a frontier-vendor subscription or under ~$2k of API spend per bench (§(cost-envelope)). Replication does not require institutional credentials or enterprise access. Doubts about specific instances, regrades, or methodological claims should be filed as issues against the repository; confirmed corrections fold into the next versioned artifact.

## LLM collaboration disclosure {-}

Per current ethics norms for AI-assisted scientific writing, LLMs enter this work in two distinct roles.

*Subject of study.* The harness under evaluation (§(method), §(setup)) uses frontier LLMs as the generator and challenger; this is the paper's object of inquiry, with model versions, billing mode, and provenance disclosed in §(models) and the published artifact.

*Writing aid.* The prose was drafted with Anthropic's Claude (Opus 4.8) from a human-authored outline, then edited for sharpening, tightening, and lint passes. The claims, citations, numeric results, methodology, and argument structure are the author's. No LLM served as peer reviewer or decided what to publish.

## Acknowledgments {-}

We thank John Laird for endorsing this submission.

## Novelty and comparative search protocol {.appendix} {#search}

- **Why this section exists.** Several claims in this paper take the form *"we found no prior X."* Such claims are only as honest as the search they rest on. This section publishes the queries so readers can re-run the search and either confirm the gap or find what we missed.
- **Sources searched.** Google Scholar; arXiv (cs.LG, cs.AI, cs.CL, cs.SE); ACL Anthology; OpenReview; GitHub code and repository search; public SWE-bench leaderboard and submission archives.
- **Queries by claim.**
  - **Peircean SE-agent loop.** *"Peirce" "LLM agent" abduction deduction induction software engineering*; *"Peircean" "LLM agents" abduction deduction induction*; *"abduction deduction induction" "LLM agent" "software engineering"*; *"Peirce" "SWE-bench" agent*; *"code agent" "abduction" "deduction" "induction" LLM*.
  - **Hypothesis-graph agent memory.** *"hypothesis graph" "LLM agent" memory*; *"belief graph" "LLM agent" memory hypothesis*; *"knowledge graph" "LLM agent" "hypothesis" "memory"*; *"AriGraph" "knowledge graph world models" "episodic memory" "LLM agents"*.
  - **Blind multi-model hypothesis-stage filtering.** *"multi-agent" "code" "hypothesis" "SWE-bench"*; *"multi-model" "code agent" "disagreement"*; *"blind" "multi-agent" "code review" LLM*; *"ensemble" "LLM agents" "software engineering" "SWE-bench"*.
  - **Trajectory-shape termination gates.** *"LLM agent" termination criteria trajectory*; *"finite state" "LLM agent" "termination"*; *"sequential testing" "LLM agents" stopping rules*.
  - **Full per-instance provenance on SWE-bench Pro.** *SWE-bench Pro leaderboard submissions trajectories cost ledger*; *"SWE-bench Pro" "trajectory" "cost"*; *"SWE-bench Verified" "trajectories" "cost ledger"*; *site:github.com "swe-bench-pro" "trajs"*.
  - **Two-bench validation under one frozen artifact.** *"SWE-bench Verified" "SWE-bench Pro" "same" "scaffold"*; *"SWE-bench Pro" "Verified" "frozen" "artifact"*; *"SWE-bench Pro" "SWE-bench Verified" "cross-bench"*.
  - **Sub-$1k Pro replication and per-instance cost ledger.** *"SWE-bench Pro" "cost per instance"*; *"SWE-bench Pro" "cost ledger"*; *"SWE-bench" "cost-per-instance" "leaderboard"*; *"SWE-rebench" cost per problem*.
- **Caveats.** The search is best-effort and bounded by visible-web indexing; private industry work, in-preparation manuscripts, and non-indexed venues are not covered. Discoveries of overlapping prior work post-publication should be reported as issues against the repository for citation update.

### Comparative search supporting the headline claim

The headline claim, *no method documented has proved a higher SWE-bench resolve rate at a lower audited per-instance cost with equivalent receipts*, requires a comparative search separate from the novelty search above. The queries below are scoped specifically to that claim. The bar for *equivalent receipts* is: published per-instance trajectories, captured diffs, gate or evaluator traces, cost ledger, and reproducible run conditions.

**Sources searched.** SWE-bench Verified leaderboard ([github.com/swe-bench/experiments](https://github.com/swe-bench/experiments/)); SWE-bench Pro official page ([scaleapi.github.io/SWE-bench_Pro-os/](https://scaleapi.github.io/SWE-bench_Pro-os/)); SWE-rebench public reports ([swe-rebench.com](https://swe-rebench.com/)); Nilenso Pro trajectory analysis; OpenHands, SWE-agent, AutoCodeRover, Aider, Devin reports; venturebeat / techcrunch reporting on Pro/Datacurve / DeepSWE; arXiv recent submissions tagged SWE-bench; vendor blogs (Anthropic, OpenAI, Google) on agent benchmark performance.

**Queries.**
- *"SWE-bench Verified" "per-instance" cost trajectories*; *"SWE-bench Pro" leaderboard "cost" "trajectories"*; *"SWE-bench" submission "cost ledger"*.
- *"SWE-bench" "cost per instance" submission diff trajectory*; *"swebench" submission reproducible cost*.
- *OSS PR merge rate LLM agent maintainer-graded benchmark*; *agent-produced pull request acceptance rate*.
- *"SWE-bench Verified" 95% 96% 97% top resolve rate trajectories cost*; *Pro leaderboard top resolve rate cost*.

**Candidate audit (against the receipt bar).** Each top public submission or comparable report is checked for: published per-instance trajectories (T), captured diffs (D), evaluator/gate traces (G), per-instance cost ledger (C), reproducible frozen artifact (R), and resolve rate at or above the rate this paper reports on the same bench (Rate). Receipt-bar columns are *present* (✓), *partial* (~), or *absent* (·). A row that doesn't combine all six is not a refutation of the headline.

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
<tr><td>Datacurve / DeepSWE reporting (VentureBeat)</td><td>Pro-class</td><td class="c">·</td><td class="c">·</td><td class="c">·</td><td class="c">~</td><td class="c">·</td><td>N/A (journalism)</td><td>Reports e.g. GPT-5.5 ~$5.80/trial median (roughly this work's frontier per-instance economic rate of ~$5.14, and ~14× the open-weight-generator pair). Journalism-level cost data, short of a structured ledger.</td></tr>
<tr><td>SWE-rebench public reports</td><td>rebench</td><td class="c">~</td><td class="c">~</td><td class="c">·</td><td class="c">✓</td><td class="c">~</td><td>Below ours</td><td>Strong cost transparency (Cursor Composer 2.5 at $0.23/problem); reported resolve rates below the rates this paper documents on Verified.</td></tr>
<tr class="ours"><td><strong>This work: Verified</strong></td><td>Verified</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td>426 / 438 eligible (97.3%)</td><td>Companion repo <code>swebench-verified</code>; Zenodo DOI; gate traces and cost ledger committed.</td></tr>
<tr class="ours"><td><strong>This work: Pro</strong></td><td>Pro</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td class="c">✓</td><td>terminal 694/728 = 95.3%, 0 incomplete; open-weight-generator pair 678/728 = 93.1%</td><td>Same frozen harness; whole eligible set graded in one measurement. Two model pairs (frontier + open-weight, ~12.6× cheaper) under one bundle. Artifact committed at frozen tag; Zenodo DOI forthcoming (§(provenance)).</td></tr>
</table>
</div>

**Reading.** No row above this paper's two rows combines all six receipt-bar columns and a resolve rate at or above the rates this paper documents on the same bench. The headline survives as long as that table reads this way.

**Caveat.** Top-line resolve rates above the receipt bar may exist in private submissions or in submissions whose receipt set we have not been able to verify; the headline is bounded by what we documented. A citation showing a stronger combined receipt is the cleanest refutation.

## Extended intellectual lineage {.appendix} {#lineage}

*The foundational sources below ground the lineage summarized in §(grounding) and §(related-work); they are collected here rather than in the body so Related Work stays focused on contemporary systems.*

### Peircean inquiry and the philosophy of science

- **Peirce 1878** (*Illustrations of the Logic of Science*, Popular Science Monthly): the original three-mode taxonomy of abduction, deduction, and induction.
- **Peirce 1903** (*Pragmatism as the Logic of Abduction*, Harvard lectures): abduction as the only mode that introduces new content.
- **Bacon 1620** (*Novum Organum*): induction as a typed primitive.
- **Popper 1934** (*The Logic of Scientific Discovery*): falsification as the inductive-side constraint.
- **Ramsey 1926** (*Truth and Probability*; in *The Foundations of Mathematics and other Logical Essays*, 1931): operational credence as betting odds, the Dutch Book argument, subjective probability as the substrate for graded belief. The hypothesis graph's node-level semantics descends from this work.
- **James 1907** (*Pragmatism: A New Name for Some Old Ways of Thinking*) and **Dewey 1929** (*The Quest for Certainty*): pragmatist commitment that truth is inseparable from action; the stakes-indexing of belief follows from this commitment.
- **Meehl 1967**: soft-science methodological critique that anticipates many of the failure modes our typing constrains.
- **Feynman 1974** ("Cargo Cult Science"): informal but substantive on the difference between rigor-shaped activity and actual rigor.

### Bi-abductive and compositional inference; failure isolation

- **Calcagno et al. 2009**: compositional shape analysis via bi-abduction; Facebook Infer as the industrial-scale instance of typed-mode inference on real code.
- **Bylander et al. 1991**: abductive computational complexity.
- **O'Hearn 2019**: separation logic and incorrectness logic, the modern compositional-inference scaffolding.
- **Noam Zilberstein, Saliling & Silva 2024** ([arXiv:2305.04842](https://arxiv.org/abs/2305.04842)): Outcome Separation Logic; Theorem 5.1 establishes soundness of tri-abduction for branch composition under effects, extending bi-abduction from sequential to branching.
- **Zeller & Hildebrandt 2002** (*Simplifying and Isolating Failure-Inducing Input*, IEEE TSE; building on Zeller 1999): delta debugging. An optimization-side adjacent: given a failure-inducing input, isolate the minimal failure-inducing subset by binary-search-shaped perturbation. The hypothesis graph in this work is methodology-shape; delta debugging is optimization-shape; both rely on the reproducible / deterministic / perturbable properties of code (§(inquiry-frame)). Worth citing as the canonical demonstration that mechanical perturbation of code is a productive inference primitive.

### Sequential evidence (inspiration for `inquire`)

- **Wald 1947** (sequential testing) and **Vovk & Wang 2021** (*E-values: Calibration, combination, and applications*, Annals of Statistics): the sequential-evidence framing that shaped `inquire`'s diagnostic stance, treating diagnosis as evidence accumulating toward a hypothesis. No e-value accumulator is deployed in the harness; the code under test is deterministic, so the gate routes on the binary grader verdict (§(gating)).

### Directed acyclic graphs as reasoning representation

- **Pearl 1988** (*Probabilistic Reasoning in Intelligent Systems*): Bayesian networks as DAGs of probabilistic dependencies. The foundational application of DAGs to structured belief representation.
- **Pearl 2000/2009** (*Causality: Models, Reasoning, and Inference*): structural causal models, d-separation, do-calculus. DAGs as the substrate for causal-structure inference.
- The hypothesis graph in this work adapts Pearl's representation primitive for a different purpose. We borrow the typed-node/typed-edge form, but the semantics over it are not Pearl's: nodes are typed *hypotheses about engineered systems under inquiry*, not probabilistic dependencies between random variables or causal relations between exposures and outcomes.
