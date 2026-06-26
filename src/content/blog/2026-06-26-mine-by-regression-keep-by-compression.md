---
variant: post-paper
title: "Mine, Then Keep: Acquiring Reusable Abstractions for World-Model Planning"
tags: methodology, cognition
autonumber: true
---

*Position / survey draft. Planning over primitive actions is expensive even with a good world model, so agents learn reusable abstractions over behavior, then keep only some. Across HTN learning, macro-operator and explanation-based learning, grammar induction, program-library induction, and hierarchical reinforcement learning, this takes one shape: a candidate-generation move and a keep-criterion. We take two keep-criteria from communities that rarely cite each other, compression (description length) and planning utility (Minton's macro utility problem), and make them directly comparable. The two are *empirically near-equivalent across much of standard planning*, which is why both fields succeed with their own rule. They diverge most sharply on *rare-but-critical abstractions*: the regime we conjecture long-horizon world-model agents inhabit, where today's ever-growing skill libraries keep nothing at all. The contribution is the map of where the two criteria agree and the corner where they part.*

## Introduction

Planning directly over primitive actions is expensive even with a perfect world model, because the branching swamps any search. So agents that plan, whether symbolic HTN planners, program-induction systems, hierarchical reinforcement learners, or the new LLM agents with skill libraries, learn an abstraction layer and plan over that instead. Acquiring the layer raises a question each field answers in isolation and few state aloud: of the many abstractions experience offers, which do you keep? This keep-criterion is the organizing question here. Two answers recur across literatures that rarely cite each other, compression (keep what shortens the description of past behavior) and planning utility (keep what reduces future search), and the contribution is the map of where they agree and where they part.

A word on what this is. This is an opinionated map, not a systematic review. It draws on five lineages, macro-operator and explanation-based learning, grammar induction, HTN-method learning, hierarchical-RL option discovery, and program-library and LLM skill-library learning, and reads them through one lens: the propose-then-keep decomposition. Where it surveys, it credits originators; where it argues a position, that the keep-criterion is load-bearing and that long-horizon agents will need a utility one, it says so, so the advocacy stays visible and separable from the map.

**Contributions.** (1) a common notation for abstraction-library learning over a world model; (2) a taxonomy comparing HTN learning, grammar induction, HRL option discovery, and program-library learning by their *proposal mechanism* and *selection pressure*; (3) a controlled experiment that maps where the compression and utility keep-criteria empirically coincide and where they diverge, reconciling two literatures at the level of the computation; (4) the gaps the map reveals and an open problem: whether long-horizon world-model agents operate in the divergence corner, where their ever-growing skill libraries would need a utility keep-pressure rather than compression.

## Problem Formulation: Abstraction as Library Learning

Let `D = {τ₁…τ_N}` be a corpus of successful behavior traces, each `τ = (s₀, a₀, s₁, …, s_T)` generated under a world model `M : S × A → S` over primitive actions `A`. By *world model* I mean any predictive model that supports counterfactual evaluation of action sequences: symbolic transition rules, a learned neural simulator, a DSL interpreter, or an LLM-mediated state predictor.

A candidate abstraction `c` has an interface (a task head, option, program type, or macro name), an applicability condition `pre(c)`, an expansion `body(c)` in primitives or other abstractions, and a carrying cost `κ(c)` for storing, matching, and maintaining it. A library `L` is a set of abstractions; given `L`, each trace rewrites to a derivation `z ∈ Rewrite(τ; L)` that reconstructs `τ` under `M`. Write the rewritten corpus `Z_L(D)`.

Three objective families recur for choosing `L`:

```
Compression / MDL:   L* = argmin_L  [ bits(L) + bits(Rewrite(D; L)) ]
Bayesian library:    L* = argmax_L  [ log p(D | L, M) + log p(L) ]      with  p(L) ∝ e^(−λ·K(L))
Use-time utility:    L* = argmax_L  [ E_q benefit(q; L, M) − cost(L) ]
```

- **Compression / MDL.** Keep an abstraction only when the library plus the re-expressed corpus encodes in fewer bits.
- **Bayesian library prior.** With a prior penalizing library size and a likelihood rewarding compact rewrites, this reduces to an MDL-like trade-off.
- **Use-time utility.** Benefit is search-node or planning-time reduction (or return improvement) on future queries `q`; cost includes matching, retrieval, and interference.

They price different things: representational length, posterior probability, or expected use-time value. But all instantiate one rule: *retain an abstraction only when its reuse value exceeds its carrying cost.* The library is useful only insofar as it changes planning over `M`.

## Proposal Mechanisms: Generating Candidate Abstractions

The oldest proposal mechanism is **goal regression**. HTN-Maker (Hogg, Muñoz-Avila, and Kuter) regresses a goal backward through the suffix of a solved trace; the surviving conditions become a method's precondition, the spanned actions its expansion. It required *annotated tasks*, and CURRICULAMA (Li, Nau, Roberts, and Fine-Morris, 2024) removed that by deriving the tasks as planning landmarks. Earlier HTN-by-observation systems make the proposal step explicitly observational: Nejati, Langley, and Könik's, and CaMeL (Ilghami and colleagues, which learns method preconditions for a given structure).

A second mechanism is **pattern mining**: treat each trace as a symbol sequence and extract recurring substrings. Hérail and Bit-Monnot's structure learner uses the GoKrimp algorithm (Lam and colleagues) to promote frequent patterns to synthetic tasks, consolidated in Hérail's 2024 thesis. A third is **program search**: DreamCoder (Ellis and colleagues) searches a DSL for task solutions, then mines its own programs. A fourth, the crudest, is **enumeration**: Hérail and Bit-Monnot's 2022 paper generated whole models by partitioning the action set.

None of this is new. It descends from macro-operator acquisition ([Fikes, Hart, and Nilsson; STRIPS MACROPS](https://www.sciencedirect.com/science/article/abs/pii/0004370272900513)), explanation-based learning (DeJong and Mooney; Minton's PRODIGY), and Soar's chunking of impasse resolution into rules (Laird, Rosenbloom, and Newell). The same shape recurs in grammar induction: [SEQUITUR](https://jair.org/index.php/jair/article/view/10192) (Nevill-Manning and Witten) replaces repeated digrams with nonterminals, RePair (Larsson and Moffat) builds straight-line grammars by pair replacement, ADIOS (Solan and colleagues) induces significant patterns. The proposal step has many faces and one habit: it is generous, and will always offer more abstractions than you should keep.

## Selection Pressures: Which Abstractions to Keep

A substantial subset of systems keep by **compression**. DreamCoder retains a routine only when it lowers the joint description length of library and programs; Stitch (Bowers and colleagues) makes the same selection roughly an order of magnitude faster. Hérail and Bit-Monnot score whole HTN models by an explicit MDL metric and mine patterns by GoKrimp's most-compressing-first rule. In grammar induction the grammar size *is* the objective.

A second subset keeps by **use-time utility**. Minton's work on the utility problem in PRODIGY kept a learned control rule only when its estimated search-time savings beat its matching cost, the first explicit statement that learned structure has a carrying cost.

Much of hierarchical reinforcement learning uses **neither**. The options framework (Sutton, Precup, and Singh) defines temporally extended actions without a discovery rule; option-discovery methods then propose subgoals from bottlenecks (McGovern and Barto; Şimşek and Barto's betweenness), spectra (Machado and colleagues' [eigenoptions](https://arxiv.org/abs/1703.00956)), reachability (Konidaris and Barto's [skill chaining](https://proceedings.neurips.cc/paper/2009/hash/e0cf1f47118daebc5b16269099ad7347-Abstract.html)), diversity or empowerment (Eysenbach and colleagues' [DIAYN](https://arxiv.org/abs/1802.06070)), or differentiable return (Bacon, Harb, and Precup's [Option-Critic](https://arxiv.org/abs/1609.05140)). Only the description-length branch, PolicyBlocks (Pickett and Barto) and LOVE (Jiang and colleagues), matches the compression thesis; the rest are genuine counterpoints.

## A Taxonomy of Abstraction Learners

The table is the map, and the choice of axes is the argument. The conventional cuts through this literature run by representation, symbolic versus neural, or by domain, planning versus reinforcement learning versus program synthesis; both keep the communities apart and hide the convergence. The claim here is that the load-bearing axis is neither, but the keep-criterion. Cut along it and HTN learners, grammar inducers, and program-library systems share a cell, while methods that share a representation fall on opposite sides. The framing is the contestable part, and it is the contribution: an agent can list these systems, but deciding the right cut is along keep-pressure rather than representation is a claim someone has to stake. Each row gets one *proposal* and one *keep* pressure; where a keep pressure is absent, the row says so.

| Lineage | System | World model | Proposal | Keep pressure | Type |
|---|---|---|---|---|---|
| Macro / EBL | MACROPS (Fikes+ 1972) | symbolic | generalize solved plan | none → utility problem | proposal-only |
| Macro / EBL | PRODIGY (Minton 1988) | symbolic | EBL on solved instances | search utility − match cost | utility-explicit |
| Macro / EBL | Soar chunking | symbolic | chunk impasse resolution | none (architectural) | accumulation |
| Grammar | SEQUITUR | sequence | repeated-digram replacement | grammar size (2 constraints) | compression-explicit |
| Grammar | RePair | sequence | most-frequent-pair replacement | grammar size | compression-explicit |
| Grammar | ADIOS | sequence | significant-pattern detection | statistical / MDL-like | compression-like |
| Grammar | GoKrimp (Lam+) | sequence DB | candidate patterns | most-compressing (MDL) | compression-explicit |
| HTN | HTN-Maker | symbolic | goal regression (annotated) | subsumption / redundancy | proposal + syntactic prune |
| HTN | CaMeL (Ilghami+) | symbolic | precondition learning | n/a (structure given) | proposal-only |
| HTN | by observation (Nejati+ 2006) | symbolic | observe executions | none explicit | proposal-only |
| HTN | CURRICULAMA (2024) | symbolic | regression + landmarks | none new (unbounded growth) | accumulation |
| HTN | enumeration (Hérail+ 2022) | symbolic | partition enumeration | whole-model MDL | compression-explicit |
| HTN | structure learner (Hérail+ 2023) | symbolic | GoKrimp + regression | MDL (per-pattern + model) | compression-explicit |
| HRL | options (Sutton+ 1999) | MDP | given / defined | n/a (framework) | framework |
| HRL | PolicyBlocks (Pickett+ 2002) | MDP | shared policy fragments | description length | compression-like |
| HRL | betweenness (Şimşek+ 2009) | MDP graph | centrality subgoals | graph centrality | other-objective |
| HRL | eigenoptions (Machado+ 2017) | MDP | Laplacian eigenvectors | spectral | other-objective |
| HRL | Option-Critic (Bacon+ 2017) | learned | differentiable options | policy-gradient return | other-objective |
| HRL | DIAYN (Eysenbach+ 2018) | learned | diversity skills | mutual information | other-objective |
| HRL | LOVE (Jiang+ 2022) | learned | variational segmentation | info cost on skills | compression-like |
| Program | DreamCoder / EC (Ellis+) | DSL | program search | Bayesian / MDL library | compression-explicit |
| Program | Stitch (Bowers+ 2023) | DSL | corpus-guided abstraction | description length | compression-explicit |
| Program | BPL (Lake+ 2015) | generative program | hierarchical parts | Bayesian prior | Bayesian-compression-like |
| LLM agent | Voyager (Wang+ 2023) | LLM / sim | LLM skills from feedback | none (ever-growing) | accumulation-without-pruning |
| LLM agent | DEPS (Wang+ 2023) | LLM / sim | LLM plan decomposition | none | accumulation |
| LLM agent | Reflexion (Shinn+ 2023) | LLM | stored verbal reflection | none (append) | accumulation-without-pruning |
| LLM agent | ExpeL (Zhao+ 2024) | LLM | extracted insights | weak heuristic | weak-keep |

The pattern is not "everyone compresses." Compression (or a Bayesian prior that behaves like it) dominates grammar induction, program induction, and the recent HTN line; explicit utility appears in EBL; HRL is split, with most option-discovery using other objectives entirely; and the LLM/world-model agents mostly have *no* keep pressure. The honest claim is the disjunction: durable libraries need *some* keep pressure, and these are the recurring forms.

## A Controlled Comparison: When Compression Suffices, and When It Must Price Utility

The compression and utility branches are usually separate literatures. On a controlled domain they are directly comparable, and the comparison is the point. Each candidate skill abstracts one task segment with two *independent* properties: a frequency `f`, the fraction of tasks needing it, and a hardness `h`, the segment's blind-search cost (`B^h` model-rollouts if unabstracted). All segments share a description length, so an MDL keep-rule's gain is proportional to `f` alone; compression is blind to hardness by construction, while a utility keep-rule scores `f · B^h`. Under a carrying-cost budget `K` (a larger library also raises the per-step matching floor `B + |L|`), MDL keeps the `K` most frequent skills, utility the `K` highest-`f · B^h`. Expected held-out planning cost is exact, with no Monte-Carlo noise.

With `B = 4`, 30 candidate skills, and budget `K = 10` (frequency and hardness uncorrelated):

| keep rule | library size | held-out planning cost |
|---|---|---|
| no-library | 0 | 10356 |
| accumulate-all | 30 | 265 |
| frequency / MDL keep | 10 | 8739 |
| **utility keep** | **10** | **831** |

No library is catastrophic. But a keep rule alone does not fix it: MDL and a naive frequency cutoff barely improve on no library, spending the budget on frequent-but-easy skills and leaving the rare-hard segments uncovered. Only a utility rule recovers, keeping the abstractions that actually cut search, an order of magnitude below MDL and close to the unbudgeted accumulate-all baseline at a fraction of its library size. The keep-criterion carries the result, not merely keeping.

Whether that gap appears is conditional, and the condition is the contribution. Sweeping the correlation `ρ` between frequency and hardness against the budget `K` traces a phase boundary: utility's advantage runs up to roughly 28× where hard skills are rare and uncorrelated with frequency, and collapses toward parity as `ρ → 1`, where the frequent skills *are* the hard ones and compression selects them anyway.

<figure style="margin:1.6em auto;">
<img src="/assets/phase-diagram.png" alt="Heatmap of log10(MDL planning cost / utility planning cost) over frequency–hardness correlation (x) and library budget (y); bright where utility wins, dark on the right where the two agree." style="width:100%; height:auto; border-radius:3px;" />
<figcaption style="text-align:center; font-size:13px; color:#666; margin-top:0.4em;">Bright = utility beats compression. The advantage fills the rare-and-uncorrelated regime and vanishes on the right, where frequency tracks hardness and compression picks the hard skills for free. Exact expected cost, averaged over 16 skill populations per cell.</figcaption>
</figure>

So compression is a sound keep-criterion exactly where statistical regularity tracks search value, and it fails precisely on the rare-but-critical abstraction it cannot see. Minton's utility problem and the MDL criterion are one picture: two prices on the same carrying cost, agreeing when frequency and difficulty align and diverging when they do not.

The same ablation in a standard planning domain confirms the boundary is real, not an artifact of the synthetic setup. In Blocksworld, with macro-operators mined from solved plans and planning cost measured as search nodes expanded, the two keep-rules nearly coincide and the gap widens monotonically with difficulty: utility beats MDL by 1.08× at five blocks, 1.18× at six, and 1.37× at seven, as deeper deadlocks make the rare search-saving macro matter more (the no-library cost rises from 6.8 to 24.3 nodes over the same range). Standard Blocksworld sits in the agreement corner, exactly where frequency tracks search-value, and drifts toward divergence as the domain hardens. This is where the surveyed HTN systems live, and it is why a compression keep-rule has served them. (Code, figure, and the Blocksworld harness: the `mine-then-keep` repository.)

## Open Problems and Future Directions

The map makes three absences visible. The first is an empty column: every LLM and world-model skill-library agent in the taxonomy pairs the strongest proposal mechanism with no keep-criterion at all. Voyager's library is ever-growing by design, Reflexion appends, and none weighs an abstraction's reuse value against its carrying cost; CURRICULAMA reports the symbolic version of the same symptom, method count and planning time climbing without convergence. The agents with the richest world models are the ones that have not yet learned to forget, and a [comprehensive survey of world models](https://arxiv.org/abs/2411.14499) (ACM Computing Surveys, 2025) already names the abstract, high-level action layer as an open problem in its own right. That layer *is* a learned abstraction library: the field built the proposal half and left selection to accretion, with a [recent wave](https://arxiv.org/abs/2605.12039) of evolving skill graphs and self-improving libraries only beginning to treat management as a problem.

This is a lesson the field has already bought once. Macro-operator learning largely stalled on exactly this, the utility problem Minton named in 1988: a planner that hoards learned macros spends more time matching them than they save. Soar's chunking produced "expensive chunks" that slowed the architecture (Tambe, Newell, and Rosenbloom); HTN-Maker's descendants still report method counts that climb without converging. Each time, unmanaged accumulation turned a learned library from an asset into a tax, a result that lives in the field's memory more than in any single paper's abstract, and is most of why the older symbolic lineages grew a keep-criterion at all. The skill-library agents have rebuilt the accumulation without the brake, and are placed to relearn the result at scale.

The second absence is an untested assumption, and clearing it means adjudicating two tempting reads. Compression keepers treat description length as evidence of useful abstraction, but the two come apart: a [recent evaluation](https://arxiv.org/abs/2410.20274) finds library-learning gains that do not trace to reuse at all, so description length is a proxy for value, not value. And it is tempting to read the bottleneck-option literature as already showing that rare skills carry outsized worth. It does not. Betweenness and diverse-density subgoals sit on many successful trajectories, so they tend to be *high*-frequency, and that work optimizes leverage, not the frequency-value gap; only the line that prices planning time directly (Jinnai and colleagues) speaks to the gap at all. The rare-but-high-value tail is therefore unestablished, and reading options research as support for it is a category slip. The third absence is a methodological blind spot: the keep-criterion is seldom ablated. The controlled comparison above is one of few, and it runs on a synthetic domain and Blocksworld, not a live agent.

These converge on one open problem, and it turns on a contingent fact: whether the value in an open-ended agent's skills concentrates in rare-but-critical abstractions, the heavy tail where compression and utility part. By analogy the structure is not exotic but generic. A passport is used a few times a decade and is indispensable on each, and a rule that keeps what you use often deletes it first. The principle runs deeper than household clutter: an organism reproduces only a handful of times in a life, and that handful carries the entire quantity selection optimizes for. Frequency-based and compression-based keeping is the rule that throws away the passport and counts only the meals. Value and frequency are independent axes, a point already settled for experience, where [prioritized replay](https://arxiv.org/abs/1511.05952) keeps the rare important transitions over the common ones; planning utility is the keep-criterion that catches the rare-critical skill, the objective [Jinnai and colleagues](https://proceedings.mlr.press/v97/jinnai19a/jinnai19a.pdf) optimize directly. Whether a real agent's library inherits this shape is unmeasured, so we leave it open. But the analogy fixes the prior: a planner whose hardest sub-problems are rare bottlenecks, the one deadlock-breaking maneuver, the unlock that opens a region, learns its highest-value skills exactly where compression is blind. If so, the agents accumulating libraries today are keeping the wrong half.

Three steps would close it: extend the controlled comparison to a more combinatorial domain such as Logistics, and to larger Blocksworld, to trace the full agreement-to-divergence drift; measure the value-versus-frequency distribution of a real skill-library agent's abstractions directly; and ablate keep-criteria in a live world-model agent over a long horizon. My own grid-puzzle agent, a learned simulator with a decomposition library grown by proposal-then-compression, is the intended vehicle for the last.

## Conclusion

Two communities that rarely cite each other have been computing nearly the same library: compression and utility coincide wherever reuse tracks difficulty, which is most of standard planning, and that is why both fields succeed with their own rule. They part only on the rare-but-critical abstraction, the corner the newest agents appear to occupy and the one their accreting libraries cannot keep. This map is one lens among possible ones, and a survey's framing can ossify a field as easily as clarify it; the lens earns its place only if it makes the keep-criterion visible as a choice rather than an accident, and names the single measurement that would settle which choice long-horizon agents need.

## References

- Bacon, Harb, Precup. [The Option-Critic Architecture](https://arxiv.org/abs/1609.05140). AAAI, 2017.
- Berlot-Attwell, Rudzicz, Si. [Library Learning Doesn't: The Curious Case of the Single-Use 'Library'](https://arxiv.org/abs/2410.20274). 2024.
- Bowers, Olausson, Wong, Grand, Tenenbaum, Ellis, Solar-Lezama. [Top-Down Synthesis for Library Learning](https://mlb2251.github.io/stitch.pdf) (Stitch). POPL, 2023.
- DeJong, Mooney. Explanation-Based Learning: An Alternative View. *Machine Learning* 1(2), 1986.
- Ellis, Wong, Nye, Sablé-Meyer, Morales, Hewitt, Cary, Solar-Lezama, Tenenbaum. [DreamCoder: Growing Generalizable, Interpretable Knowledge with Wake-Sleep Bayesian Program Learning](https://arxiv.org/abs/2006.08381). 2021.
- Eysenbach, Gupta, Ibarz, Levine. [Diversity Is All You Need: Learning Skills without a Reward Function](https://arxiv.org/abs/1802.06070) (DIAYN). ICLR, 2019.
- Fikes, Hart, Nilsson. [Learning and Executing Generalized Robot Plans](https://www.sciencedirect.com/science/article/abs/pii/0004370272900513) (STRIPS MACROPS). *Artificial Intelligence* 3, 1972.
- Hérail, Bit-Monnot. [Learning Operational Models from Demonstrations: Parameterization and Model Quality Evaluation](https://icaps22.icaps-conference.org/workshops/HPlan/papers/paper-06.pdf). ICAPS HPlan Workshop, 2022.
- Hérail, Bit-Monnot. [Leveraging Demonstrations for Learning the Structure and Parameters of Hierarchical Task Networks](https://journals.flvc.org/FLAIRS/article/view/133327). FLAIRS, 2023.
- Hérail. [Learning Hierarchical Models from Demonstrations for Deliberate Planning and Acting](https://laas.hal.science/tel-04692640). PhD thesis, Université de Toulouse, 2024.
- Hogg, Muñoz-Avila, Kuter. [HTN-MAKER: Learning HTNs with Minimal Additional Knowledge Engineering Required](https://cdn.aaai.org/AAAI/2008/AAAI08-151.pdf). AAAI, 2008.
- Ilghami, Nau, Muñoz-Avila, Aha. CaMeL: Learning Method Preconditions for HTN Planning. AIPS, 2002.
- Jiang, Liu, Eysenbach, Kolter, Finn. [Learning Options via Compression](https://proceedings.neurips.cc/paper_files/paper/2022/hash/8567a53e58a9fa4823af356c76ed943c-Abstract-Conference.html) (LOVE). NeurIPS, 2022.
- Jinnai, Abel, Hershkowitz, Littman, Konidaris. [Finding Options that Minimize Planning Time](https://proceedings.mlr.press/v97/jinnai19a.html). ICML, 2019.
- Konidaris, Barto. [Skill Discovery in Continuous Reinforcement Learning Domains using Skill Chaining](https://proceedings.neurips.cc/paper/2009/hash/e0cf1f47118daebc5b16269099ad7347-Abstract.html). NeurIPS, 2009.
- Laird, Rosenbloom, Newell. Chunking in Soar: The Anatomy of a General Learning Mechanism. *Machine Learning* 1, 1986.
- Lake, Salakhutdinov, Tenenbaum. Human-Level Concept Learning through Probabilistic Program Induction (BPL). *Science* 350, 2015.
- Lam, Mörchen, Fradkin, Calders. Mining Compressing Sequential Patterns (GoKrimp). *Statistical Analysis and Data Mining* 7(1), 2014.
- Larsson, Moffat. Off-Line Dictionary-Based Compression (RePair). *Proceedings of the IEEE* 88(11), 2000.
- Li, Nau, Roberts, Fine-Morris. [Automatically Learning HTN Methods from Landmarks](https://arxiv.org/abs/2404.06325) (CURRICULAMA). 2024.
- Machado, Bellemare, Bowling. [A Laplacian Framework for Option Discovery in Reinforcement Learning](https://arxiv.org/abs/1703.00956) (eigenoptions). ICML, 2017.
- McGovern, Barto. Automatic Discovery of Subgoals in Reinforcement Learning using Diverse Density. ICML, 2001.
- Minton. [Quantitative Results Concerning the Utility of Explanation-Based Learning](https://cdn.aaai.org/AAAI/1988/AAAI88-100.pdf) (PRODIGY). AAAI, 1988.
- Nejati, Langley, Könik. Learning Hierarchical Task Networks by Observation. ICML, 2006.
- Nevill-Manning, Witten. [Identifying Hierarchical Structure in Sequences: A Linear-Time Algorithm](https://jair.org/index.php/jair/article/view/10192) (SEQUITUR). *JAIR* 7, 1997.
- Pickett, Barto. [PolicyBlocks: An Algorithm for Creating Useful Macro-Actions in Reinforcement Learning](https://marcpickett.com/papers/pickettICML2002.pdf). ICML, 2002.
- Schaul, Quan, Antonoglou, Silver. [Prioritized Experience Replay](https://arxiv.org/abs/1511.05952). ICLR, 2016.
- Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao. [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366). NeurIPS, 2023.
- Şimşek, Barto. Skill Characterization Based on Betweenness. NeurIPS, 2008.
- Solan, Horn, Ruppin, Edelman. Unsupervised Learning of Natural Languages (ADIOS). *PNAS* 102(33), 2005.
- Sutton, Precup, Singh. Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning (options). *Artificial Intelligence* 112, 1999.
- Tambe, Newell, Rosenbloom. The Problem of Expensive Chunks and Its Solution by Restricting Expressiveness. *Machine Learning* 5, 1990.
- *Understanding World or Predicting Future? A Comprehensive Survey of World Models*. [ACM Computing Surveys](https://arxiv.org/abs/2411.14499), 2025.
- Wang, Xie, Jiang, Mandlekar, Xiao, Zhu, Fan, Anandkumar. [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291). 2023.
- Wang, Cai, Liu, Ma, Liang. Describe, Explain, Plan and Select (DEPS). NeurIPS, 2023.
- [SkillGraph: Skill-Augmented Reinforcement Learning for Agents via Evolving Skill Graphs](https://arxiv.org/abs/2605.12039). 2026.
- Zhao, Huang, Xu, Lin, Liu, Huang. [ExpeL: LLM Agents Are Experiential Learners](https://arxiv.org/abs/2308.10144). AAAI, 2024.

---

*Open items: extend the external-validity sweep to a more combinatorial domain (Logistics) and larger Blocksworld to trace the full agreement-to-divergence drift, and an ARC-AGI-3 within-game cross-level demonstration of the live agent; tighten the HRL coverage into its own subsection; and position against a specific venue (ICAPS HPlan, GenPlan, or an ICLR/NeurIPS world-models workshop).*
