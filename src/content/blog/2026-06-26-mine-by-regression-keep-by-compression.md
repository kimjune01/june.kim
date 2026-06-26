---
variant: post-paper
title: "Mine, Then Keep: Acquiring Reusable Abstractions for World-Model Planning"
tags: methodology, cognition
autonumber: true
---

*Position / survey draft. Planning over primitive actions is expensive even with a good world model, so agents learn reusable abstractions over behavior, then keep only some. Across HTN learning, macro-operator and explanation-based learning, grammar induction, program-library induction, and hierarchical reinforcement learning, this takes one shape: a candidate-generation move and a keep-criterion. We take two keep-criteria from communities that rarely cite each other, compression (description length) and planning utility (Minton's macro utility problem), and make them directly comparable. The two are *empirically near-equivalent across standard planning*, which is why both fields succeed with their own rule. They diverge only on *rare-but-critical abstractions*: the regime that long-horizon world-model agents inhabit, and where today's ever-growing skill libraries keep nothing at all. The contribution is the map of where the two criteria agree and the corner where they part.*

**Contributions.** (1) a common notation for abstraction-library learning over a world model; (2) a taxonomy comparing HTN learning, grammar induction, HRL option discovery, and program-library learning by their *proposal mechanism* and *selection pressure*; (3) a controlled experiment that maps where the compression and utility keep-criteria empirically coincide and where they diverge, reconciling two literatures at the level of the computation; (4) a position claim that the divergence corner is exactly where long-horizon world-model agents operate, so their ever-growing skill libraries need an explicit keep pressure.

## Problem setup: abstraction as library learning

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

These differ in what they *price*, representational length, posterior probability, or expected use-time value, but instantiate one rule: *retain an abstraction only when its reuse value exceeds its carrying cost.* The library is useful only insofar as it changes planning over `M`.

## The first move: proposal

The oldest proposal mechanism is **goal regression**. HTN-Maker (Hogg, Muñoz-Avila, and Kuter) regresses a goal backward through the suffix of a solved trace; the surviving conditions become a method's precondition, the spanned actions its expansion. It required *annotated tasks*, and CURRICULAMA (Li, Nau, Roberts, and Fine-Morris, 2024) removed that by deriving the tasks as planning landmarks. Earlier HTN-by-observation systems make the proposal step explicitly observational: Nejati, Langley, and Könik's, and CaMeL (Ilghami and colleagues, which learns method preconditions for a given structure).

A second mechanism is **pattern mining**: treat each trace as a symbol sequence and extract recurring substrings. Hérail and Bit-Monnot's structure learner uses the GoKrimp algorithm (Lam and colleagues) to promote frequent patterns to synthetic tasks, consolidated in Hérail's 2024 thesis. A third is **program search**: DreamCoder (Ellis and colleagues) searches a DSL for task solutions, then mines its own programs. A fourth, the crudest, is **enumeration**: their 2022 paper generated whole models by partitioning the action set.

None of this is new. It descends from macro-operator acquisition (Fikes, Hart, and Nilsson; STRIPS MACROPS), explanation-based learning (DeJong and Mooney; Minton's PRODIGY), and Soar's chunking of impasse resolution into rules (Laird, Rosenbloom, and Newell). The same shape recurs in grammar induction: SEQUITUR (Nevill-Manning and Witten) replaces repeated digrams with nonterminals, RePair (Larsson and Moffat) builds straight-line grammars by pair replacement, ADIOS (Solan and colleagues) induces significant patterns. The proposal step has many faces and one habit: it is generous, and will always offer more abstractions than you should keep.

## The second move: selection pressure

A substantial subset of systems keep by **compression**. DreamCoder retains a routine only when it lowers the joint description length of library and programs; Stitch (Bowers and colleagues) makes the same selection roughly an order of magnitude faster. Hérail and Bit-Monnot score whole HTN models by an explicit MDL metric and mine patterns by GoKrimp's most-compressing-first rule. In grammar induction the grammar size *is* the objective.

A second subset keep by **use-time utility**. Minton's work on the utility problem in PRODIGY kept a learned control rule only when its estimated search-time savings beat its matching cost, the first explicit statement that learned structure has a carrying cost.

Much of hierarchical reinforcement learning uses **neither**. The options framework (Sutton, Precup, and Singh) defines temporally extended actions without a discovery rule; option-discovery methods then propose subgoals from bottlenecks (McGovern and Barto; Şimşek and Barto's betweenness), spectra (Machado and colleagues' eigenoptions), reachability (Konidaris and Barto's skill chaining), diversity or empowerment (Eysenbach and colleagues' DIAYN), or differentiable return (Bacon, Harb, and Precup's Option-Critic). Only the description-length branch, PolicyBlocks (Pickett and Barto) and LOVE (Jiang and colleagues), matches the compression thesis; the rest are genuine counterpoints.

## The taxonomy

The table makes the convergence claim auditable. Each row gets one *proposal* and one *keep* pressure; where a keep pressure is absent, the row says so.

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

## Experiments: when compression suffices, and when it must price utility

The compression and utility branches are usually separate literatures. On a controlled domain they are directly comparable, and the comparison is the point. Each candidate skill abstracts one task segment with two *independent* properties: a frequency `f`, the fraction of tasks needing it, and a hardness `h`, the segment's blind-search cost (`B^h` model-rollouts if unabstracted). All segments share a description length, so an MDL keep-rule's gain is proportional to `f` alone; compression is blind to hardness by construction, while a utility keep-rule scores `f · B^h`. Under a carrying-cost budget `K` (a larger library also raises the per-step matching floor `B + |L|`), MDL keeps the `K` most frequent skills, utility the `K` highest-`f · B^h`. Expected held-out planning cost is exact, with no Monte-Carlo noise.

With `B = 4`, 30 candidate skills, and budget `K = 10` (frequency and hardness uncorrelated):

| keep rule | library size | held-out planning cost |
|---|---|---|
| no-library | 0 | 10356 |
| accumulate-all | 30 | 265 |
| frequency / MDL keep | 10 | 8739 |
| **utility keep** | **10** | **831** |

Keep-pressure is the dominant effect: no library is catastrophic, and any principled rule recovers most of it. But MDL and a naive frequency cutoff coincide here, and both spend the budget on frequent-but-easy skills, leaving the rare-hard segments uncovered: an order of magnitude worse than a utility rule that keeps the abstractions which actually cut search.

Whether that gap appears is conditional, and the condition is the contribution. Sweeping the correlation `ρ` between frequency and hardness against the budget `K` traces a phase boundary: utility's advantage runs up to roughly 28× where hard skills are rare and uncorrelated with frequency, and collapses toward parity as `ρ → 1`, where the frequent skills *are* the hard ones and compression selects them anyway.

<figure style="margin:1.6em auto;">
<img src="/assets/phase-diagram.png" alt="Heatmap of log10(MDL planning cost / utility planning cost) over frequency–hardness correlation (x) and library budget (y); bright where utility wins, dark on the right where the two agree." style="width:100%; height:auto; border-radius:3px;" />
<figcaption style="text-align:center; font-size:13px; color:#666; margin-top:0.4em;">Bright = utility beats compression. The advantage fills the rare-and-uncorrelated regime and vanishes on the right, where frequency tracks hardness and compression picks the hard skills for free. Exact expected cost, averaged over 16 skill populations per cell.</figcaption>
</figure>

So compression is a sound keep-criterion exactly where statistical regularity tracks search value, and it fails precisely on the rare-but-critical abstraction it cannot see. Minton's utility problem and the MDL criterion are one picture: two prices on the same carrying cost, agreeing when frequency and difficulty align and diverging when they do not.

The same ablation in a standard planning domain confirms the boundary is real, not an artifact of the synthetic setup. In Blocksworld, with macro-operators mined from solved plans and planning cost measured as search nodes expanded, the two keep-rules nearly coincide and the gap widens monotonically with difficulty: utility beats MDL by 1.08× at five blocks, 1.18× at six, and 1.37× at seven, as deeper deadlocks make the rare search-saving macro matter more (the no-library cost rises from 6.8 to 24.3 nodes over the same range). Standard Blocksworld sits in the agreement corner, exactly where frequency tracks search-value, and drifts toward divergence as the domain hardens. This is where the surveyed HTN systems live, and it is why a compression keep-rule has served them. (Code, figure, and the Blocksworld harness: the `mine-then-keep` repository.)

## A falsifiable prediction, and the frontier

The position has a testable edge. Any agent that keeps long-lived reusable abstractions should exhibit one of the three keep pressures; as task diversity grows, an agent without one should show library bloat, rising match/retrieval cost, degrading planning time, or ad hoc pruning. That is exactly the profile of current LLM/world-model skill-library agents. Voyager's library is, by design, ever-growing; Reflexion appends; none weighs an abstraction's reuse value against its carrying cost. CURRICULAMA reports the symbolic version of the same symptom: method count and planning time climbing without convergence. The agents with the richest world models are the ones that have not yet learned to forget.

This is not a niche planning concern; it is two open questions the world-model community is already asking, joined. A [comprehensive survey of world models](https://arxiv.org/abs/2411.14499) (ACM Computing Surveys, 2025) places the *abstract, high-level action layer* among the field's open problems: today's world models predict and control well at the low level, while extending them to abstract, long-horizon planning is unsolved. Meanwhile the agents built on top are already accumulating the libraries this paper is about. Voyager treats its skill library as ever-growing; the 2025–26 wave trying to discipline it, [evolving skill graphs](https://arxiv.org/abs/2605.12039) and self-improving skill libraries, treats library management as an open problem in its own right.

The two questions are one. The high-level layer the world-model surveys want *is* a learned abstraction library, and the skill-library agents have built the proposal half (an LLM proposes skills fluently) while leaving selection to accretion. The keep-criterion is the missing half, and the experiments above say which one they will need: compression where reuse tracks difficulty, an explicit utility price in the rare-but-critical corner that long-horizon agents live in.

My own grid-puzzle agent is a small worked instance on the keeping side: a learned simulator for `M`, a decomposition library grown by proposal-then-compression, and a content-addressed trace store for `D`. It is one more lineage washing up on the same shore, which is how I came to draw the map.

---

*Open items: extend the external-validity sweep to a more combinatorial domain (Logistics) and larger Blocksworld to trace the full agreement-to-divergence drift, and an ARC-AGI-3 within-game cross-level demonstration of the live agent; tighten the HRL coverage into its own subsection; verify all citations and add full references; and position against a specific venue (ICAPS HPlan, GenPlan, or an ICLR/NeurIPS world-models workshop).*
