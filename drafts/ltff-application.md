# LTFF application — draft

Reusable core for LTFF, Manifund, and Cooperative AI. Tuned for LTFF's questions.
Numbers in [brackets] are yours to set. Voice is yours; this is a starting cut to react to.

---

## Project title

Verifiable agent reasoning: an externalized, replayable substrate for checking what AI agents conclude

## One-paragraph summary

AI agents are being handed consequential autonomy faster than we can verify their reasoning. A patch
passes the visible tests and is still wrong off-suite; a model reports a suite as green when it is red.
Output-level checks miss this, and the reasoning that would expose it disappears with the context window.
I have built and demonstrated a mechanism that fixes this at the harness layer, with no model retraining:
the **hypothesis graph**, a semantic memory whose nodes are testable claims and whose edges are the
conditions that refute them, where every conclusion is reconstructible by a stranger who reruns its
recorded trial. On one contamination-free, post-cutoff bug, externalizing this check carried a weaker
model to a fix the strongest released model could not reach on its own: a two-tier capability lift, and
the safety-aligned kind, since it comes from external verification with no training, so the same
replayable check that lifts the model is what lets a distrusting party catch its error. The code is open source and the
result is archived and regradeable. This grant funds turning a working prototype into an adoptable
standard and scaling the evidence from one case to a benchmark the field currently lacks.

## What I will do

The mechanism works on one bug. Funding moves it from demonstration to adoptable public good across four deliverables.

1. **Harden the harness.** Turn `abductor` and the `inquire` skill into an open, documented harness any
   coding-agent stack can adopt: a replayable hypothesis-graph format, a deterministic pass/fail gate,
   and the typed loop that drives an agent through propose, test, refute. Target: a second team can run
   it on their own agent without me.
2. **Build the discovery benchmark.** My audit of all 728 public SWE-bench Pro tasks shows current
   benchmarks measure translation, leaving discovery untested: most tasks are one-shot from the prompt, and a 15% floor
   grades unstated intent that is undiscoverable from the materials. I will build the eval that is missing:
   a set of post-cutoff, discovery-hard bugs with golden verdicts, contamination-controlled by construction.
   This is a public good independent of my mechanism.
3. **Scale the evidence honestly.** The mechanism already stands on two rungs. *Deterministic demos*,
   contamination-free **by construction**: worked inquiries (`leap_year`, `natural_sort`) in `abductor`,
   where a self-grading agent plateaus on a hypothesis green on every visible test, and the
   gate's coverage drags it to a bespoke rule it cannot recall from memory, the oracle-gap mechanism
   isolated, with no case selection at all. *One real-world
   transfer*: a preregistered factorial (six arms × three variants, ~18 runs of 2–4h, parallelized to
   ~18h wall-clock) on a real contamination-free, post-cutoff bug, selected for eligibility and fixed
   before the comparison ran, so it leaves generalization open while ruling out selection on outcome. Funding
   adds the third rung: the *confirmatory* contrast, with-check vs without-check at the selected
   configuration, on a small set of new post-cutoff bugs, reporting where the mechanism engages and,
   equally, where it does not (the null regime). The runs parallelize cleanly; the real cost is curating
   contamination-free cases and the time to run them preregistered. The claim stays falsifiable: an
   oversight effect that survives replication, or it doesn't.
4. **(Stretch) Prototype cross-agent replay.** A claim record one agent writes and another re-checks
   without trusting the author, the "entitlement ledger" from *Verifiable Knowledge*. Droppable to scope
   a smaller grant; the core value lands in deliverables 1–3, and the discovery benchmark (2) is a public
   good that stands even if the central bet fails.

Everything ships as it lands: public repos, archived under DOIs, reproducible from committed inputs, as the
existing artifacts already are.

## Theory of change

The risk this addresses is the loss of oversight as agents act autonomously. Today the check
on an agent is usually its own report, and a model that grades itself can be wrong, overconfident, or
sandbagging, with no external way to tell. Independent replay is the defense: the verdict comes from
re-running a typed check; the model's word does not enter it, so a model cannot pass by merely asserting success;
the check has to be independently satisfiable. This is scalable oversight at the harness layer, available to any deployer today at no
training cost.

The empirical bet is stated and unpaid: agents that externalize their reasoning this way should be more
accountable, and better coordinated, than agents that do not. The Verus result is the first evidence the
mechanism does real work rather than just logging it. The benchmark and the cross-agent prototype are how
the bet gets tested at scale, where it can fail.

Why this matters before it is fashionable: a DeepMind-led paper now argues that artificial epistemic
agents must demonstrate robust falsifiability and external trust architecture (Marchal et al. 2026), the
property this substrate supplies. The window to set it as an open standard, rather than a closed
per-vendor feature, is now.

## Relation to existing oversight work

The closest neighbors are debate, prover-verifier games, process supervision, and externalized-reasoning
oversight. They share the instinct, get the reasoning outside the model, but stop at a transcript a human
or model still has to *trust*. The hypothesis graph differs in one decisive way: each claim is bound
to a typed check an untrusting party *re-runs*, so the verdict is reconstructed, not read. That defense
holds against a model grading its own transcript; reading the transcript does not.

## Track record

I designed the mechanism, built the tooling, ran the experiments, and wrote the three papers, solo and in
public. [Optional: one line of affiliation or background, if you choose to use it; the receipts can carry
it.] The work is reproducible by a stranger:
- *The Hypothesis Graph*, *Verifiable Knowledge*, and *What Cannot Be False Cannot Be True* (preprints at
  june.kim).
- `abductor` (github.com/kimjune01/abductor) and the `inquire` skill, open source, with the
  contamination-free-by-construction worked example inquiries.
- The SWE-bench Pro run (95.3%, official grader), a determinacy audit of all 728 tasks, and the Verus
  mechanism experiment, each its own repo and DOI, reproducible from committed inputs including a
  preregistration and regrade script.
- A clean iteration result: one-shot 43% → iterative 91% PR-approval across 27 merged PRs in 9 real
  repos (Go/TS/Rust), isolating the review loop as the bottleneck.

I work in public and design for a distrusting auditor by default, the same property this grant funds me
to make standard.

## Budget

[$75,000] for [9–12 months], primarily as researcher salary/stipend to work full time. Compute is
genuinely modest: runs are 2–4h and parallelize, so [~$5k] covers the experiments and ablations. The
expensive inputs are researcher time and the curation of contamination-free, post-cutoff cases, which is
the same hard input deliverable 2 (the benchmark) produces at scale. I can scope to a smaller grant by
dropping the stretch cross-agent prototype and narrowing the case set; I can absorb a larger one by
widening both.

## Other funding and conflicts

[Disclose any other applications in flight, including Manifund and Cooperative AI, and any affiliation.]
Applying to Manifund and Cooperative AI in parallel for the same program; will update LTFF if any lands.
