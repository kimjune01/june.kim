# Encoding the Inquiry Loop into Checkable Structure — Research Map

A research fan-out (codex / GPT-5.5, web-grounded, 6 parallel calls) mapping, for each
component of the Peircean inquiry loop, the SOTA framework that externalizes it into a
checkable/replayable artifact, how mature it is, how it plugs into a per-inquiry markdown
hypothesis graph for coding agents, and the residue that stays irreducibly model-internal.

Frame: a hypothesis graph is a per-inquiry markdown artifact where each node = hypothesis +
exact trial command + observed outcome + verdict + credence, and each edge = a kill condition.
Goal: push each loop component OUT of the opaque model INTO replayable structure. Hard limit
(given): the pure abductive leap — coining the hypothesis / vocabulary — is irreducible; a
grader certifies the *artifact*, never the *generative act*.

---

## Component 1 — Hypothesis generation (abduction): the encodable scaffolding

What's *already* externalized is never the raw leap; it's the scaffolding around it: defining
the hypothesis language, constraining the space, ranking candidates, deriving missing
frames/assumptions, and killing candidates with witnesses.

| Sub-part | SOTA framework | Maturity | How encodable into the graph |
|---|---|---|---|
| Hypothesis space / DSL | [SyGuS](https://sygus.org/) (Alur et al. [PDF](https://www.cis.upenn.edu/~alur/SyGuS13.pdf)); MS [PROSE](https://www.microsoft.com/en-us/research/group/prose/) | Mature research; PROSE industrial-but-narrow | A `hypothesis_space:` block per inquiry: grammar, allowed APIs, type sigs, excluded ops, cost model. A node's hypothesis becomes a concrete DSL term + exact solver command. |
| Structural priors | [DreamCoder](https://royalsocietypublishing.org/rsta/article/381/2251/20220050/) (library learning, weighted grammars) | Strong prototype, not drop-in | `prior:` metadata: grammar weights, learned-library version, ranking score, search budget. "ranked #3 by prior v17; killed by test X." |
| Bi-abduction / frame inference | Meta [Infer](https://fbinfer.com/docs/separation-logic-and-bi-abduction/) (separation logic; [POPL09 PDF](https://ilyasergey.net/CS6217/_static/papers/popl09.pdf)) | **Highly mature, industrial** | Best coding fit: node trial `infer run -- ...`; observation = inferred precondition / null-or-resource warning; edge = "missing frame implies next hypothesis." Turns "maybe this pointer is null" into analyzer output. |
| Abductive logic programming | Kakas/Kowalski/Toni [ALP](https://academic.oup.com/logcom/article-abstract/2/6/719/942121); [s(CASP)](https://github.com/SWI-Prolog/sCASP) | Academically mature, tooling fragmented | Encode repo facts as predicates (`calls/2`, `fails_test/1`); trial = goal-directed query; outcome = minimal abductive explanation. Good for dependency/config hypotheses. |
| Inductive logic programming | [Popper](https://github.com/logic-and-learning-lab/Popper) (learning from failures); Metagol/Aleph | Research-grade, not turnkey on big repos | Propose relational rules ("tests fail when module A imports stale generated file B"); node records examples, background facts, learned clause, validation command; edges = failed clauses. |
| Synthesis from examples | FlashFill/[PROSE](https://github.com/microsoft/prose) ([POPL11](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/popl11-synthesis.pdf)); [Sketch](https://people.csail.mit.edu/asolar/papers/thesis.pdf) | Industrial in narrow domains | Node holds a sketch / examples / SyGuS file; trial = solver invocation; observation = candidate program + test result; kill edge = counterexample. |

**Boundary.** Scaffolding starts once you can write `space / observations / constraints / search /
verdict_rule`. Then abduction is *partly* replayable — a stranger reruns the command and sees why
candidates were proposed, ranked, killed.

**Residue (model-internal):** choosing the vocabulary of the inquiry; deciding which observations
matter; inventing the initial DSL/predicate/sketch; noticing cross-bug analogies; deciding the
current hypothesis space is *wrong*; reframing "fix code" into "fix generated artifact / config /
test oracle / build graph."

---

## Component 2 — Prediction derivation (deduction): the predicted consequence as a checkable object

Pattern: `claim -> oracle/spec/property -> exact command -> expected observable -> kill condition`.
The agent invents H; deduction turns `H => X` into something a stranger can run.

| Mechanism | SOTA | Maturity | Node plug-in |
|---|---|---|---|
| Proof terms / Curry-Howard | [Lean 4](https://lean-lang.org/), Rocq/Coq | Very mature for math; high authoring cost | Predicted consequence = a proof obligation; trial `lake env lean Node42.lean`; kill = any unsolved goal / `sorry` / type error. |
| Formal specs | [TLA+/TLC](https://docs.tlapl.us/), [Dafny](https://dafny.org/), Design-by-Contract | TLA+/Dafny mature; contracts production-practical | Invariant/`ensures` as the predicted consequence; trial = `dafny verify` / TLC run; kill = counterexample trace. |
| Property-based testing | [Hypothesis](https://hypothesis.readthedocs.io/), QuickCheck, [Echidna](https://github.com/crytic/echidna) | **Very mature; shrinks to minimal witness** | Translate H into a property + generators; pin seed/settings; kill = shrunk failing input recorded as witness. Strong replay fit. |
| Refinement types | [LiquidHaskell](https://ucsd-progsys.github.io/liquidhaskell-tutorial/), Scala `refined` | Mature niche (typed/pure code) | Prediction = strengthened type sig; SMT/typechecker is the oracle; kill = failed verification condition + location. |
| Symbolic / concolic execution | [KLEE](https://klee-se.org/), [angr](https://angr.io/), [CrossHair](https://github.com/pschanely/crosshair) | Mature research; path explosion remains | Closest to *deriving* the discriminating trial: solver searches for an input separating H from rivals; kill = concrete `.ktest` replay. |

**Residue:** choosing *which* consequence actually discriminates among rivals; picking the right
abstraction level (proof vs model vs property vs symbolic path vs ordinary test); writing the
semantic bridge from messy behavior to a formal predicate; choosing bounds/generators/mocks;
interpreting flaky/timed-out/solver-incomplete results.

---

## Component 3 — Trial selection: encoding WHY this trial

The encodable target is a *replayable ranking decision*: candidate set + objective + score table +
argmax, stored — not just the chosen trial.

| Prior art | SOTA | Maturity | Encode |
|---|---|---|---|
| Bayesian / optimal experimental design | Rainforth et al. [Modern BED](https://arxiv.org/abs/2302.14545); [Pyro OED](https://docs.pyro.ai/en/dev/contrib.oed.html) | Mature theory, compute-heavy | `selection_rule: maximize EIG`; record latent set, candidates, predictive dist, EIG estimator, seed, cost normalization, argmax. |
| Active learning | Settles [survey](https://burrsettles.com/pub/settles.activelearning.pdf); QBC (Seung 92); [BALD](https://arxiv.org/abs/1112.5745)/[BatchBALD](https://arxiv.org/abs/1906.08158) | Mature in ML labeling; can be myopic | Treat trials as unlabeled items; store prediction vector over `{kill,witness,inconclusive}`; pick max entropy / max committee disagreement. |
| E-values / anytime-valid testing | Vovk & Wang [E-values](https://projecteuclid.org/journals/annals-of-statistics/volume-49/issue-3/E-values-Calibration-combination-and-applications/10.1214/20-AOS2020.full); Ramdas et al. [SAVI](https://projecteuclid.org/journals/statistical-science/volume-38/issue-4/Game-Theoretic-Statistics-and-Safe-Anytime-Valid-Inference/10.1214/23-STS894.full) | **Very mature recent stats**, early adoption | `test_process: e-process`, null/alt, betting strategy, `valid_under_optional_stopping`, stop rule. Lets the agent stop once evidence suffices. |
| Agentic falsification | POPPER, Huang et al. [arXiv](https://arxiv.org/abs/2502.09858) ([GitHub](https://github.com/snap-stanford/POPPER)) | Early prototype | Encode measurable implication + falsification experiment + sequential p/e process + error budget + targeted kill condition. Keep agent-generated implication separate from the valid test. |
| Model-based diagnosis probe selection | de Kleer & Williams [GDE](https://groups.csail.mit.edu/mers/old-site/papers/kle-wil-92.pdf); minimum-entropy probe choice | Old, mature symbolic AI | Direct analogy for debugging: hypotheses = diagnoses, tests = probes; store probability-by-diagnosis, candidate-probe outcome partitions, expected posterior entropy; select min-entropy probe. |

**Residue:** generating the candidate trials at all; estimating likelihoods with no calibration
data; deciding costs/risks/side-effects; recognizing a *missing* hypothesis not in the graph.

---

## Component 4 — Evidence -> credence update: encoding the belief move

The arithmetic of the update can be made fully replayable; the inputs (priors, likelihoods) cannot.
Store the full computation so a stranger recomputes the posterior.

| Framework | SOTA | Maturity | Encode (`credence:` schema) |
|---|---|---|---|
| Bayesian likelihood update | odds form `posterior_odds = prior_odds * BF`, `BF = P(E|H)/P(E|¬H)` ([BDA3](https://sites.stat.columbia.edu/gelman/book/BDA3.pdf)) | **Very mature; best default** | `{type: bayes_factor, prior_p, p_e_given_h, p_e_given_not_h, bayes_factor, posterior_p, recompute: "..."}`. |
| Multi-hypothesis Bayes | normalize over mutually exclusive H ([Stan](https://mc-stan.org/docs/stan-users-guide/)) | Mature for stat models | Store all competing hypotheses + priors + likelihoods + normalizer + posteriors. |
| Version spaces | Mitchell candidate-elimination ([PDF](https://www.ijcai.org/Proceedings/77-1/Papers/048.pdf)) | Clean, brittle under noise | Credence = surviving-set mass: `{prior_candidates, eliminated_by_edge, surviving, posterior_mass_rule}`. Recompute by applying kill predicates. |
| E-process / testing by betting | Ramdas et al. SAVI; Shafer [Testing by Betting](https://arxiv.org/pdf/2308.14959) | Modern, active | Don't call it a posterior unless calibrated: encode as evidence *capital* (e-value, increments, decision rule). |
| Truth maintenance (ATMS) | de Kleer [ATMS](https://cdn.aaai.org/AAAI/1987/AAAI87-033.pdf) | Mature symbolic AI | Credence as support sets: `{type: atms_label, prior_label, justification, nogoods, posterior_label}`. Recompute via justifications + nogood minimization. |
| Dempster-Shafer | Shafer evidence theory; Smets TBM | Mature in fusion, fragile on independence | Masses over hypothesis *subsets* + Dempster combination + Bel/Pl. Use when evidence supports sets, not single H. |

**Residue:** choosing the hypothesis set, priors, likelihoods; deciding source independence; mapping
messy command output to a formal observation `E`; choosing kill/witness thresholds; choosing *what
"credence" even means* (probability vs surviving mass vs betting capital vs ATMS support vs Bel/Pl
interval). Target: make every judgment parameter explicit, named, versioned, recomputable.

---

## Component 5 — Belief-dependency & the kill-edge: encoding the structure of reasons

| Framework | SOTA | Maturity | Encode | Residue |
|---|---|---|---|---|
| Truth maintenance (JTMS) | Doyle 1979 [TMS](https://dspace.mit.edu/handle/1721.1/5733) | Mature classical AI | `depends_on` edges = Doyle-style reasons; when a premise dies, recompute downstream beliefs (no stale conclusions). | Doesn't invent the next hypothesis. |
| ATMS | de Kleer 1986 | Mature design pattern | Each hypothesis valid under an assumption set (OS, dep version, repo state); kill edge records the *minimal inconsistent assumption set*. | Choice of assumption vocabulary is judgment. |
| Abstract argumentation | Dung 1995 [acceptability](https://cse-robotics.engr.tamu.edu/dshell/cs631/papers/dung95acceptability.pdf) | Mature field, niche tooling | Nodes = arguments, kill edges = `attack` relations; grounded/preferred semantics compute which hypotheses stay defensible after counter-evidence. | Doesn't guarantee the attack relation is complete/correctly extracted. |
| CEGAR | Clarke et al. 2000 [CAR](https://www.cs.cmu.edu/~emc/papers/Papers%20In%20Refereed%20Journals/Counterexample-guided%20abstraction%20refinement.pdf) | **Highly mature** | A failed trial = a concrete counterexample; next node = "refine spec/abstraction around this counterexample," not "try random fix." | Abstraction boundary chosen outside the loop. |
| CEGIS / sketching | Solar-Lezama 2008; [CEGIS(T)](https://www.kroening.com/papers/cav2018-synthesis.pdf) | Mature, specialized | Hypothesis = candidate patch; kill edge = counterexample input; next node constrained by accumulated counterexamples. | Grammar/spec are external creative choices. |
| Provenance | W3C [PROV-DM/PROV-O](https://www.w3.org/TR/prov-overview/) | Mature web standard | Node = `prov:Entity`, command = `prov:Activity`, model/tool = `prov:Agent`; `wasGeneratedBy / used / wasDerivedFrom` as Turtle/JSON sidecars. | Records lineage, not truth. |
| Content-addressed / Merkle | Git/[IPFS/IPLD](https://docs.ipfs.tech/concepts/content-addressing/) CIDs | Production-proven | Canonicalize each node's trial record, hash it; parent hashes form a Merkle reasoning DAG; any edit to command/outcome changes the node id + root hash. | Tamper-evidence ≠ semantic validity. |

---

## Component 6 — The trail as a verifiable object

| Framework | SOTA | Maturity | Encode | Residue |
|---|---|---|---|---|
| Proof-carrying code / certifying algorithms | Necula 1997 [PCC](https://dl.acm.org/doi/10.1145/263699.263712) | Mature idea, specialized | Trail root carries a checker + certificate: tests passed, proof obligations discharged, static-analysis report, model-checker witness, minimized repro. Stranger verifies without trusting the agent. | Most coding tasks lack complete specs; cert may cover only regressions/types/tests. |
| Signed attestation | [in-toto / SLSA](https://slsa.dev/spec/v1.0/provenance) | Production-maturing | Treat each trial command as a supply-chain step; sign materials/products/exit/hashes; whole trail = auditable bundle. | Trust boundary: local shell can lie if env is compromised. |
| Process supervision / PRMs | OpenAI [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) | Active ML research | Score each node/edge as triage (was the trial relevant? did verdict follow from observation? was next hypothesis justified?). | PRM judgments are model-internal estimates unless backed by executable checks. |
| Formal / neuro-symbolic traces | [LeanDojo/ReProver](https://arxiv.org/abs/2306.15626), AlphaGeometry, AlphaProof | Strong in math/formal, emerging for coding | Where possible convert hypothesis into a formal obligation (theorem, equivalence proof, invariant, SMT query); node verdict = verifier output, not prose. | Autoformalization is lossy; hardest part is translating repo intent into the right property. |
| Agentic scientific discovery | Sakana [AI Scientist v2](https://arxiv.org/abs/2504.08066) | Experimental; weak formal checkability | Template for end-to-end loop; require every experiment node to carry exact command, data hashes, artifacts, replay script. | Novelty/interpretation stay soft without formal/statistical certificates. |

**Recommended layered architecture (from C5+C6):** (1) Argument/TMS layer (`depends_on / supports /
attacks / killed_by`); (2) CEGAR/CEGIS layer (every death names a counterexample constraining the
next hypothesis); (3) PROV layer (command/inputs/outputs/agent identity); (4) Merkle layer
(content-address each node + whole trail); (5) Certificate layer (final answer carries replay
script + tests/proofs/analysis/attestations); (6) PRM/process layer (optional learned critique,
*never* the root of trust).

---

## Unifying work (2024–2026): verdict

**Nothing already externalizes the whole loop.** No found system gives a per-inquiry, durable,
human-auditable hypothesis graph where every node is reconstructible by a stranger from the recorded
trial alone and edges encode explicit kill conditions. The frontier is split into partial pieces:

- **POPPER** (2025, [arXiv](https://arxiv.org/abs/2502.09858)) — closest to the *falsification core*:
  decomposes free-form hypotheses into measurable implications, designs falsification experiments,
  controls Type-I error sequentially. But it's hypothesis *validation*, not the whole loop, and not a
  replayable reasoning graph for coding agents.
- **AI Scientist v1/v2** (Sakana), **Google AI Co-Scientist** (2025), **Agent Laboratory** (2025),
  **Coscientist** (2023) — automate much of the research *lifecycle*, but the durable artifact is
  paper/code/results/notes, not node-level hypotheses with explicit kill conditions. Mature as demos,
  immature as epistemic audit trails.
- **DiscoveryWorld** (2024) — excellent *benchmark* for full-cycle discovery, but it evaluates agents;
  it doesn't make them externalize inquiry into replayable nodes.
- **LADYBUG** (2025, LLM agent debugger) — closest on *replayable agent traces* (supports
  intervention + re-execution, beyond mere logging), but externalizes execution state, not
  hypothesis/kill-condition structure.
- **SWE-agent, ReAct, Tree-of-Thoughts, Reflexion** — mostly action traces / chain-of-thought /
  memory; hypotheses stay implicit and thoughts aren't independently reconstructible.
- **PRMs / "Let's Verify Step by Step"** — check *steps*, not *inquiries*, and only where rules/
  verifiers exist.

Honest distinction: most "verifiable reasoning trace" work is still trace *logging* or post-hoc
explanation. Very little forces reasoning to be reconstructed *from recorded trials alone*. **The
hypothesis-graph idea appears to be a real gap, not solved under another name.**

---

## Synthesis: where to push next

### Maturity per component (how well the encodable part is already handled)

| Component | Encodable mechanism | State |
|---|---|---|
| 2 Deduction (predicted consequence) | PBT, contracts, refinement types, symbolic exec | **Adequate** — drop-in mature tools; mostly an integration job |
| 5 Kill-edge / dependency | TMS, Dung attacks, CEGAR, PROV, Merkle | **Adequate** — mature primitives, need a markdown schema |
| 6 Trail as object | PCC, in-toto/SLSA, Merkle | **Adequate** — content-addressing + replay script is straightforward |
| 4 Credence update | Bayes odds, version spaces, e-values | **Adequate arithmetic, open elicitation** — recording the computation is easy; the inputs are judgment |
| 1 Abduction scaffolding | DSL/space, Infer bi-abduction, ILP | **Partially open** — DSL design per domain is real work; the leap is the hard limit |
| 3 Trial selection | EIG/BED, e-values, GDE probe selection | **Genuinely open** for LLM agents — theory mature, but likelihoods are uncalibrated guesses in a repo |

### Single highest-leverage thing to encode next: the trial-selection record (Component 3)

It moves the most reasoning into checkable structure per unit effort. Today, *why this command and
not another* is the single biggest unaudited black box in an agent's debugging loop — and it's the
hinge of the whole loop (it's where abduction's output meets deduction's design). The encoding is
cheap and high-yield: a replayable acquisition record stored *next to* the selected trial —

```yaml
trial_selection:
  candidate_set_id: C-014
  candidates_source: generated_from_open_hypotheses   # the leap stays here, fenced
  objective: expected_information_gain_per_cost
  scoring_command: "python tools/rank_trials.py graph.md --objective eig_per_cost --seed 7"
  selected: T2
  selected_score: 0.51
  runner_up: T1
  runner_up_score: 0.42
  kill_edges_targeted: [H2 -> killed_if_stacktrace_changes, H1 -> killed_if_no_repro]
  validity_guard: e_process_optional_stopping
  maturity_note: likelihoods are heuristic; this is a decision aid, not a proof
```

This makes the choice checkable as "given this candidate set, model, objective, and score table,
T2 was the argmax" — auditable and rerunnable — while cleanly *fencing* the irreducible residue
(candidate generation, likelihood estimation) into named fields rather than letting it hide in prose.
It also naturally absorbs the e-value/anytime-valid machinery (the maturest recent statistics here),
which doubles as the Component-4 stop rule. The other adequate components (2, 5, 6) are integration
work on mature tools; trial selection is where the open research and the leverage coincide.

### Where the "encode it" goal may be mistaken

Codex flags one place not to over-externalize: **candidate/hypothesis generation and likelihood
elicitation should stay model-internal** (the hard limit, confirmed from every angle). The model's
implicit prior over "what usually breaks this kind of code" is richer and better-calibrated by
exposure than any hand-built probability table a coding agent could maintain — forcing an explicit
numeric prior/likelihood for every node risks false precision (made-up numbers dressed as rigor) and
slows the loop. The right move is not to compute these in the open but to *name and version* them as
explicit fields (`candidates_source`, `maturity_note: likelihoods are heuristic`) so the residue is
visibly fenced rather than either hidden or faked. Externalize the *arithmetic and the trail*;
leave the *generative guess and its calibration* inside the model, but labeled.

---

## Sources
Six codex/GPT-5.5 web-grounded research calls; per-component raw outputs in
`/tmp/codex_{1..6}.md`. All links above are ones codex surfaced and are reproduced as found.
