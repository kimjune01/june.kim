---
variant: post-paper
title: "Generalize or Specialize? Retaining Reusable Skills for World-Model Agents"
tags: methodology, cognition
autonumber: true
---

*Position / survey draft. Agents that act in a world increasingly write their own skills, growing a library of reusable abstractions and planning over it. The hard part is not proposing a skill but deciding which to retain, and that retention criterion forces a choice between generality and specialization. It is an eviction problem, the oldest one in systems. A bounded store, read far more than written, keeps either what is used most or what is dear to recompute, and two communities that rarely cite each other answer with exactly these: compression (description length), which keeps what recurs, and planning utility (Minton's macro utility problem), which keeps what pays off. We make them directly comparable. They are *empirically near-equivalent wherever reuse tracks search-value*, the regime standard Blocksworld occupies, where either keeps the same library and each field succeeds with its own. They diverge most sharply on *rare-but-critical abstractions*, the specialists compression cannot see, the regime we conjecture long-horizon world-model agents inhabit, where today's ever-growing skill libraries weigh nothing against carrying cost. The contribution is the map of where the two criteria agree and the corner where they part.*

## Introduction

Agents now write their own skills. Given an environment, a language model will propose, code, and store reusable behaviors, growing a skill library it plans over; Voyager is the canonical case. This was read as a glimpse of recursive self-improvement: an agent that accumulates its own capabilities should compound them. It has not proven so simple. A library that only grows is not a library that improves. Past some size, more skills mean more to match, retrieve, and confuse, and the agent slows under the weight of what it has learned. The hard part was never proposing a skill, which a language model does fluently, but deciding which to retain. This retention criterion is the organizing question here.

The choice it forces is between generality and specialization, and it is older and wider than language-model agents: HTN learners, program-induction systems, and hierarchical reinforcement learners all grow and prune the same kind of library under other names. Two criteria recur across these literatures, which rarely cite each other: compression (minimum description length), which keeps what recurs, the general and broadly reusable skill; and planning utility (Minton's macro utility problem), which keeps what pays off, including the rare specialist that cracks one hard case and is invisible to frequency. The contribution is the map of where they agree and where they part, and the split is, mechanically, cache eviction: what a library keeps versus what it evicts.

This is an opinionated map rather than a systematic review. It draws on five lineages, macro-operator and explanation-based learning, grammar induction, HTN-method learning, hierarchical-RL option discovery, and program-library and LLM skill-library learning, and reads them through one lens: the propose-then-keep decomposition. Where it surveys, it credits originators; where it argues a position, that the retention criterion is load-bearing and that long-horizon agents will need a utility one, it marks the claim as such, and the advocacy stays visible and separable from the map.

**Contributions.** (1) a common notation for abstraction-library learning over a world model; (2) a taxonomy comparing HTN learning, grammar induction, HRL option discovery, and program-library learning by their *proposal mechanism* and *selection pressure*; (3) a controlled experiment that reconciles two literatures at the level of the computation, mapping where the compression and utility retention criteria empirically coincide and where they diverge; (4) the gaps the map reveals and an open problem: whether long-horizon world-model agents operate in the divergence corner, where their ever-growing skill libraries would need a utility retention pressure rather than compression.

## Problem Formulation: Abstraction as Library Learning

Let `D = {τ₁…τ_N}` be a corpus of successful behavior traces, each `τ = (s₀, a₀, s₁, …, s_T)` generated under a world model `M : S × A → S` over primitive actions `A`. By *world model* we mean any predictive model that supports counterfactual evaluation of action sequences: symbolic transition rules, a learned neural simulator, a DSL interpreter, or an LLM-mediated state predictor.

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

They are three ways of pricing an abstraction against its carrying cost: representational length, posterior probability, or expected use-time value. But only the utility criterion prices *use-time value* directly; compression and the Bayesian prior price encoding length and bet that it tracks value. The library is useful only insofar as it changes planning over `M`.

## Proposal Mechanisms: Generating Candidate Abstractions

The oldest proposal mechanism is **goal regression**. HTN-Maker (Hogg, Muñoz-Avila, and Kuter) regresses a goal backward through the suffix of a solved trace; the surviving conditions become a method's precondition, the spanned actions its expansion. It required *annotated tasks*, and CURRICULAMA (Li, Nau, Roberts, and Fine-Morris, 2024) removed that by deriving the tasks as planning landmarks. Earlier HTN-by-observation systems make the proposal step explicitly observational: Nejati, Langley, and Könik's, and CaMeL (Ilghami and colleagues, which learns method preconditions for a given structure).

A second mechanism is **pattern mining**: treat each trace as a symbol sequence and extract recurring substrings. Hérail and Bit-Monnot's structure learner uses the GoKrimp algorithm (Lam and colleagues) to promote frequent patterns to synthetic tasks, consolidated in Hérail's 2024 thesis. A third is **program search**: DreamCoder (Ellis and colleagues) searches a DSL for task solutions, then mines its own programs. A fourth, the crudest, is **enumeration**: Hérail and Bit-Monnot's 2022 paper generated whole models by partitioning the action set.

None of this is new; it descends from macro-operator acquisition ([Fikes, Hart, and Nilsson; STRIPS MACROPS](https://www.sciencedirect.com/science/article/abs/pii/0004370272900513)), explanation-based learning (DeJong and Mooney; Minton's PRODIGY), and Soar's chunking of impasse resolution into rules (Laird, Rosenbloom, and Newell). The same shape recurs in grammar induction: [SEQUITUR](https://jair.org/index.php/jair/article/view/10192) (Nevill-Manning and Witten) replaces repeated digrams with nonterminals, RePair (Larsson and Moffat) builds straight-line grammars by pair replacement, ADIOS (Solan and colleagues) induces significant patterns. The proposal step takes many forms but shares one tendency: it is generous, always offering more abstractions than are worth keeping.

## Selection Pressures: Which Abstractions to Retain

A substantial subset of systems keep by **compression**. DreamCoder retains a routine only when it lowers the joint description length of library and programs; Stitch (Bowers and colleagues) makes the same selection roughly an order of magnitude faster. Hérail and Bit-Monnot score whole HTN models by an explicit MDL metric and mine patterns by GoKrimp's most-compressing-first rule. In grammar induction the grammar size *is* the objective.

A second subset keeps by **use-time utility**. Minton's work on the utility problem in PRODIGY kept a learned control rule only when its estimated search-time savings beat its matching cost, the first explicit statement that learned structure has a carrying cost.

Much of hierarchical reinforcement learning uses **neither**. The options framework (Sutton, Precup, and Singh) defines temporally extended actions without a discovery rule; option-discovery methods then propose subgoals from bottlenecks (McGovern and Barto; Şimşek and Barto's betweenness), spectra (Machado and colleagues' [eigenoptions](https://arxiv.org/abs/1703.00956)), reachability (Konidaris and Barto's [skill chaining](https://proceedings.neurips.cc/paper/2009/hash/e0cf1f47118daebc5b16269099ad7347-Abstract.html)), diversity or empowerment (Eysenbach and colleagues' [DIAYN](https://arxiv.org/abs/1802.06070)), or differentiable return (Bacon, Harb, and Precup's [Option-Critic](https://arxiv.org/abs/1609.05140)). Only the description-length branch, PolicyBlocks (Pickett and Barto) and LOVE (Jiang and colleagues), matches the compression thesis, and only Jinnai and colleagues price planning time directly; the rest are genuine counterpoints. One caveat the table cannot fully capture: across much of this branch, proposal and selection collapse into a single objective. Options are induced and retained by the same discovery rule, with the count fixed in advance, so the "retention pressure" column here names the inducing objective rather than a separate retention step. The clean propose-then-keep split is itself more a property of the symbolic and program-library lineages than of the differentiable ones.

## A Taxonomy of Abstraction Learners

The table is the map, and the choice of axes is the argument. The conventional cuts through this literature run by representation, symbolic versus neural, or by domain, planning versus reinforcement learning versus program synthesis; both keep the communities apart and hide the convergence. The claim here is that the load-bearing axis is neither, but the retention criterion. Along that axis, HTN learners, grammar inducers, and program-library systems share a cell, while methods that share a representation fall on opposite sides. The framing is the contestable part, and it is the contribution: an agent can list these systems, but deciding that the right cut is along retention pressure rather than representation is a claim that must be staked. Each row carries one *proposal* and one *retention* pressure; where a retention pressure is absent, the row records it.

| Lineage | System | World model | Proposal | Retention pressure | Type |
|---|---|---|---|---|---|
| Macro / EBL | MACROPS (Fikes+ 1972) | symbolic | generalize solved plan | none → utility problem | proposal-only |
| Macro / EBL | PRODIGY (Minton 1988) | symbolic | EBL on solved instances | search utility − match cost | utility-explicit |
| Macro / EBL | Soar chunking | symbolic | chunk impasse resolution | none (architectural) | accumulation |
| Grammar | SEQUITUR | sequence | repeated-digram replacement | grammar size (2 constraints) | compression-explicit |
| Grammar | RePair | sequence | most-frequent-pair replacement | grammar size | compression-explicit |
| Grammar | ADIOS | sequence | significant-pattern detection | statistical significance | other-objective |
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
| HRL | min-time options (Jinnai+ 2019) | MDP | option-set search | planning-time reduction | utility-explicit |
| Program | DreamCoder / EC (Ellis+) | DSL | program search | Bayesian / MDL library | compression-explicit |
| Program | Stitch (Bowers+ 2023) | DSL | corpus-guided abstraction | description length | compression-explicit |
| Program | BPL (Lake+ 2015) | generative program | hierarchical parts | Bayesian prior | Bayesian-compression-like |
| LLM agent | Voyager (Wang+ 2023) | LLM / sim | LLM skills from feedback | none (ever-growing) | accumulation-without-pruning |
| LLM agent | DEPS (Wang+ 2023) | LLM / sim | LLM plan decomposition | none | accumulation |
| LLM agent | Reflexion (Shinn+ 2023) | LLM | stored verbal reflection | none (append) | accumulation-without-pruning |
| LLM agent | ExpeL (Zhao+ 2024) | LLM | extracted insights | weak heuristic | weak-keep |

The pattern is not "everyone compresses." Compression (or a Bayesian prior that behaves like it) dominates grammar induction, program induction, and the recent HTN line; explicit utility appears in EBL; HRL is split, with most option-discovery using other objectives entirely; and the LLM/world-model agents mostly have *no* retention pressure. The honest claim is the disjunction: durable libraries need *some* retention pressure, and these are the recurring forms.

## The Mechanism: Retention as Cache Eviction

Naming the mechanism brings in a fifth field, one that solved this problem decades before the others yet is cited by none of them. A library read far more often than it is written, with a budget on what it can hold, is a cache, and deciding what to retain is cache eviction. The two retention criteria are the two classic eviction families. Compression is LFU: evict what is accessed least, keep what recurs. Utility is cost-aware eviction, [Greedy-Dual-Size](https://www.usenix.org/conference/usits-97/cost-aware-www-proxy-caching-algorithms) and its frequency-weighted form [GDSF](https://www.semanticscholar.org/paper/Improving-WWW-Proxies-Performance-with-Greedy-Dual-Cherkasova/275f66e845043217d5c37328b5e71a178302469f), where an item's "cost" is its miss penalty, the work redone without it, which is exactly the search a missing abstraction forces. [Belady's](https://dl.acm.org/doi/10.1147/sj.52.0078) optimal policy, evict what is needed farthest in the future, is the ideal both approximate. Cognitive science split the same way: human memory tracks frequency and recency as a rational estimate of future need ([Anderson and Schooler](https://journals.sagepub.com/doi/abs/10.1111/j.1467-9280.1991.tb00174.x)), yet also preferentially retains high-value items independent of how often they recur ([Castel and colleagues](https://link.springer.com/article/10.3758/BF03194325)), the two eviction criteria and their divergence in one memory system.

Caching has already produced this result. Cost-aware eviction beats pure frequency precisely when item costs are heavy-tailed, a few objects far dearer than the rest, and coincides with it when cost tracks frequency. That is the agreement-versus-divergence boundary of the next section, mapped in web proxies in the 1990s; caching learned the same lesson by negative example, as LFU prevailed until cost-aware policies displaced it on heterogeneous workloads. The abstraction-library setting adds one thing caching lacks: composition. Classical eviction (Belady, GDSF) prices independent items, but abstractions build on each other, so retention here is eviction over a dependency graph, where discarding one item changes the cost of the rest. This is the one point at which the analogy genuinely breaks, and it is open: the eviction literature has little to say about caches whose items compose. The retention criterion, and the condition under which its two forms part, carry over regardless.

## A Controlled Comparison: When Compression Suffices, and When It Must Price Utility

The compression and utility branches are separate literatures. On a controlled domain they are directly comparable, and that comparison is the object of this section. Each candidate skill abstracts one task segment with two *independent* properties: a frequency `f`, the fraction of tasks needing it, and a hardness `h`, the segment's blind-search cost (`B^h` model-rollouts if unabstracted). All segments share a description length, so an MDL retention rule's gain is proportional to `f` alone; compression is blind to hardness by construction, while a utility retention rule scores `f · B^h`. This is a mechanism demonstration, not an effect-size estimate: a space of any significant size needs both kinds of skill at once, the frequent general abstractions compression keeps and the rare specialists only a utility rule sees, so a criterion that prices one alone leaves the other half uncovered. Equal description lengths make MDL exactly frequency-ranking, which isolates the mechanism; in practice a skill's encoding length grows with its expansion, so real MDL is a noisy proxy for hardness rather than blind to it, and the correlation sweep below and Blocksworld restore the realistic case. Under a carrying-cost budget `K` (a larger library also raises the per-step matching floor `B + |L|`), MDL keeps the `K` most frequent skills, utility the `K` highest-`f · B^h`. Expected held-out planning cost is exact, with no Monte-Carlo noise.

With `B = 4`, 30 candidate skills, and budget `K = 10` (frequency and hardness uncorrelated):

| retention rule | library size | held-out planning cost |
|---|---|---|
| no-library | 0 | 10356 |
| accumulate-all | 30 | 265 |
| frequency / MDL keep | 10 | 8739 |
| **utility keep** | **10** | **831** |

No library is far worse, by orders of magnitude. But a retention rule alone does not fix it: MDL and a naive frequency cutoff barely improve on no library, spending the budget on frequent-but-easy skills and leaving the rare-hard segments uncovered. Only a utility rule recovers, keeping the abstractions that actually cut search, an order of magnitude below MDL and close to the unbudgeted accumulate-all baseline at a fraction of its library size. The retention criterion, not the act of keeping, carries the result.

Whether that gap appears is conditional, and the condition is the contribution. Sweeping the correlation `ρ` between frequency and hardness against the budget `K` traces a phase boundary: utility's advantage runs up to roughly 28× where hard skills are rare and uncorrelated with frequency, and collapses toward parity as `ρ → 1`, where the frequent skills *are* the hard ones and compression selects them anyway.

<figure style="margin:1.6em auto;">
<img src="/assets/phase-diagram.png" alt="Heatmap of log10(MDL planning cost / utility planning cost) over frequency–hardness correlation (x) and library budget (y); bright where utility wins, dark on the right where the two agree." style="width:100%; height:auto; border-radius:3px;" />
<figcaption style="text-align:center; font-size:13px; color:#666; margin-top:0.4em;">Bright = utility beats compression. The advantage fills the rare-and-uncorrelated regime and vanishes on the right, where frequency tracks hardness and compression picks the hard skills for free. Exact expected cost, averaged over 16 skill populations per cell.</figcaption>
</figure>

So compression is a sound retention criterion exactly where statistical regularity tracks search value, and it fails precisely on the rare-but-critical abstraction it cannot see. Minton's utility problem and the MDL criterion are one picture: two prices on the same carrying cost, agreeing when frequency and difficulty align and diverging when they do not.

The same ablation in a standard planning domain confirms the boundary is real, not an artifact of the synthetic setup. In Blocksworld, with macro-operators mined from solved plans and planning cost measured as nodes expanded by greedy best-first search, the two retention rules nearly coincide and the gap widens over the tested sizes: utility beats MDL by 1.08× at five blocks, 1.18× at six, and 1.37× at seven, as deeper deadlocks make the rare search-saving macro matter more (mean expanded nodes with no library rise from 6.8 to 24.3 over the same range). Standard Blocksworld sits in the agreement corner, where frequency tracks search-value, and drifts toward divergence as the domain hardens. It is the kind of domain where a compression retention rule has served the symbolic lineages well. (Code, figure, and the Blocksworld harness: the `mine-then-keep` repository.)

## Open Problems and Future Directions

The map makes three absences visible. The first is an empty column: every LLM and world-model skill-library agent in the taxonomy pairs the strongest proposal mechanism with no retention criterion at all. Voyager's library is ever-growing by design, Reflexion appends, and none weighs an abstraction's reuse value against its carrying cost. The agents with the richest world models are those with no mechanism for discarding what they learn, and a [comprehensive survey of world models](https://arxiv.org/abs/2411.14499) (ACM Computing Surveys, 2025) already names the abstract, high-level action layer as an open problem in its own right. That layer *is* a learned abstraction library: the field built the proposal half and left selection to accretion, with a [recent wave](https://arxiv.org/abs/2605.12039) of evolving skill graphs and self-improving libraries only beginning to treat management as a problem.

The field has already learned this lesson once. The utility problem Minton named in 1988, that a planner hoarding learned macros can spend more time matching them than they save, became a central reason macro-operator and explanation-based systems had to control what they kept. Soar's chunking could produce "expensive chunks" whose match cost degraded performance ([Tambe, Newell, and Rosenbloom](https://link.springer.com/article/10.1007/BF00117107)). And learned-method sets can still grow without obvious payoff: CURRICULAMA reports method count and planning time climbing in Blocks World, Logistics, and Rover. Each case is the same shape: unmanaged accumulation turning a learned library from an asset into a tax. The result survives in the field's collective experience more than in any single paper's abstract, and accounts for much of why the older symbolic lineages developed a retention criterion at all. The skill-library agents have rebuilt the accumulation without the corresponding control, and are positioned to relearn the result at scale.

The second absence is an untested assumption, and clearing it requires adjudicating two tempting readings. Compression rewards what recurs, but whether learned library items are reused at all is not automatic: a [recent evaluation](https://arxiv.org/abs/2410.20274) finds reported library-learning gains that trace to self-correction rather than reuse. Statistical regularity is a proxy for value, and the proxy can fail on its own terms. The second read is to take the bottleneck-option literature as already showing that rare skills carry outsized worth. It does not: diverse-density and betweenness subgoals are selected for sitting central or common on successful paths, so the work establishes leverage, not a rare-use, high-value separation. Only the line that prices planning time directly (Jinnai and colleagues) speaks to the frequency-value gap at all. So using bottleneck-option results as evidence for a rare-but-critical tail is a category slip; that research solves a different problem well.

The third absence is a methodological blind spot: the retention criterion is seldom ablated. The controlled comparison above is one of few, and it runs on a synthetic domain and Blocksworld, not a live agent.

These converge on one open problem, and it turns on a contingent fact: whether the value in an open-ended agent's skills concentrates in rare-but-critical abstractions, the heavy tail where compression and utility part. The structure is generic rather than exotic. A passport is used a few times a decade and is indispensable on each, and a rule that keeps what you use often deletes it first. Value and frequency are independent axes, a point already settled for experience, where [prioritized replay](https://arxiv.org/abs/1511.05952) keeps the rare important transitions over the common ones, and settled earlier still in cognitive science: [complementary learning systems](https://pubmed.ncbi.nlm.nih.gov/7624455/) theory (McClelland, McNaughton, and O'Reilly) holds that no single learner both extracts shared structure and retains sparse specifics, which is why the brain pairs a generalizing neocortex with a specific-storing hippocampus, the learning systems [Kumaran, Hassabis, and McClelland](https://web.stanford.edu/~jlmcc/papers/KumaranHassabisMcC16CLSUpdate.pdf) argue an intelligent agent needs. The general library and the rare specialist are that pairing under a planning budget; planning utility is the retention criterion that catches the specialist, the objective [Jinnai and colleagues](https://proceedings.mlr.press/v97/jinnai19a/jinnai19a.pdf) optimize directly. Whether a real agent's library inherits this shape is unmeasured, so we leave it open. But the analogy fixes the prior: a planner whose hardest sub-problems are rare bottlenecks, the one deadlock-breaking maneuver, the unlock that opens a region, learns its highest-value skills exactly where compression is blind. If so, the agents accumulating libraries today are keeping the wrong half.

Three steps would close it: extend the controlled comparison to a more combinatorial domain such as Logistics, and to larger Blocksworld, to trace the full agreement-to-divergence drift; measure the value-versus-frequency distribution of a real skill-library agent's abstractions directly; and ablate retention criteria in a live world-model agent over a long horizon. Our own grid-puzzle agent, a learned simulator with a decomposition library grown by proposal-then-compression, is the intended vehicle for the last.

## Conclusion

Two communities that rarely cite each other have been computing nearly the same library: compression and utility coincide wherever reuse tracks difficulty, the regime standard Blocksworld occupies, where either rule keeps the same library and each field succeeds with its own. They part only on the rare-but-critical abstraction, the corner we conjecture the newest agents occupy and the one their accreting libraries cannot keep. This map is one lens among others, and a survey's framing can ossify a field as easily as clarify it; the lens earns its place only if it makes the retention criterion visible as a choice rather than an accident, and names the single measurement that would settle which choice long-horizon agents need.

## References

- Anderson, Schooler. [Reflections of the Environment in Memory](https://journals.sagepub.com/doi/abs/10.1111/j.1467-9280.1991.tb00174.x). *Psychological Science* 2(6), 1991.
- Bacon, Harb, Precup. [The Option-Critic Architecture](https://arxiv.org/abs/1609.05140). AAAI, 2017.
- Belady. [A Study of Replacement Algorithms for a Virtual-Storage Computer](https://dl.acm.org/doi/10.1147/sj.52.0078). *IBM Systems Journal* 5(2), 1966.
- Berlot-Attwell, Rudzicz, Si. [Library Learning Doesn't: The Curious Case of the Single-Use 'Library'](https://arxiv.org/abs/2410.20274). 2024.
- Bowers, Olausson, Wong, Grand, Tenenbaum, Ellis, Solar-Lezama. [Top-Down Synthesis for Library Learning](https://mlb2251.github.io/stitch.pdf) (Stitch). POPL, 2023.
- Cao, Irani. [Cost-Aware WWW Proxy Caching Algorithms](https://www.usenix.org/conference/usits-97/cost-aware-www-proxy-caching-algorithms) (GreedyDual-Size). USITS, 1997.
- Castel, Benjamin, Craik, Watkins. [The Effects of Aging on Selectivity and Control in Short-Term Recall](https://link.springer.com/article/10.3758/BF03194325). *Memory & Cognition* 30(7), 2002.
- Cherkasova. [Improving WWW Proxies Performance with Greedy-Dual-Size-Frequency Caching Policy](https://www.semanticscholar.org/paper/Improving-WWW-Proxies-Performance-with-Greedy-Dual-Cherkasova/275f66e845043217d5c37328b5e71a178302469f) (GDSF). HP Labs TR, 1998.
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
- Kumaran, Hassabis, McClelland. [What Learning Systems do Intelligent Agents Need? Complementary Learning Systems Theory Updated](https://web.stanford.edu/~jlmcc/papers/KumaranHassabisMcC16CLSUpdate.pdf). *Trends in Cognitive Sciences* 20(7), 2016.
- Laird, Rosenbloom, Newell. Chunking in Soar: The Anatomy of a General Learning Mechanism. *Machine Learning* 1, 1986.
- Lake, Salakhutdinov, Tenenbaum. Human-Level Concept Learning through Probabilistic Program Induction (BPL). *Science* 350, 2015.
- Lam, Mörchen, Fradkin, Calders. Mining Compressing Sequential Patterns (GoKrimp). *Statistical Analysis and Data Mining* 7(1), 2014.
- Larsson, Moffat. Off-Line Dictionary-Based Compression (RePair). *Proceedings of the IEEE* 88(11), 2000.
- Li, Nau, Roberts, Fine-Morris. [Automatically Learning HTN Methods from Landmarks](https://arxiv.org/abs/2404.06325) (CURRICULAMA). 2024.
- Machado, Bellemare, Bowling. [A Laplacian Framework for Option Discovery in Reinforcement Learning](https://arxiv.org/abs/1703.00956) (eigenoptions). ICML, 2017.
- McClelland, McNaughton, O'Reilly. [Why There Are Complementary Learning Systems in the Hippocampus and Neocortex](https://pubmed.ncbi.nlm.nih.gov/7624455/). *Psychological Review* 102(3), 1995.
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
