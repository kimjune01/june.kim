# Temporal Compression: A Crosswalk

> **For agents and reviewers.** This document is the source-of-truth backing the [reading section](https://june.kim/reading/temporal-compression/). Every claim in the chapters traces to a citation here. Every citation was fetched and validated against the original paper. If a claim looks wrong, check this file first — the chapter may have simplified. If this file is wrong, [open an issue](https://github.com/kimjune01/junekim-reading/issues).

Video codec theory, temporal graph theory, and sheaf cohomology on directed networks all work on directed dependency graphs with time-ordered composition. Each field has tools the others lack. This document maps the vocabulary, grades the parallels, and states the open problems.

---

## Shared structure

Parallels graded on a three-level rubric: **genuine** (same formal primitive or theorem pattern under relabeling), **moderate** (same structural role but different state space/objective), **forced** (workflow resemblance or metaphor only).

### Event graph / Prediction dependency DAG
Both fields admit DAG representations of temporal dependency. Temporal graph researchers call it a **temporal event graph** (TEG) ([Mellor 2018](https://academic.oup.com/comnet/article/6/4/639/4360827)) or **weighted event graph** ([Kivelä et al. 2018](https://www.nature.com/articles/s41598-018-29577-2)). Codec engineers use a **prediction dependency DAG** for packet or frame dependencies ([Chou & Miao 2006](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ChouM06.pdf)). Closely analogous static DAG representations: the TEG encodes event adjacency under time order; the prediction DAG encodes decode dependencies over packetized data units. The identification is representational, not ontological: same structural pattern, different node semantics. This observation is ours, not made in the cited papers.

### Chain fragility (genuine parallel)
**TVG**: Temporal reachability does not compose transitively. A→B at t₁ and B→C at t₂ only yields A→C if t₂ ≥ t₁ + ζ(e₁, t₁) — arrival must precede next departure, including latency ([Casteigts et al. 2012](https://www.site.uottawa.ca/~flocchin/Papers/tvg-ijpeds.pdf), §4.4). When the timing constraint fails, the journey breaks even though both edges exist.

**Codecs**: P-frame chains break when a reference is lost — every downstream frame becomes undecodable even though the data exists. This is dependency failure under reference loss, not a timing constraint.

**Shared**: Both exhibit fragility of sequential dependency: downstream validity depends on every earlier link in the chain. The failure mechanisms differ — TVG chains break when time-ordering fails to compose; codec chains break when a reference node is lost. The structural pattern (sequential dependency where any break severs the tail) is the same.

**Algebraic analogue**: Krishnan (2014, Theorem 5.12) proves that duality gaps (max-flow < min-cut) arise from failures of exactness in directed sheaf cohomology. "Local consistency fails to globalize" is the structural content of chain fragility in sheaf-theoretic language. (The three-way connection is this crosswalk's reading, not Krishnan's.)

Grading rationale: **genuine**. Both instantiate sequential dependency over a time-ordered dependency graph where tail validity requires every predecessor. The trigger differs; the dependency pattern does not.

### Temporal disconnection ↔ Scene-change detection (forced parallel)
**TVG**: Combinatorial reachability failure; forward composition stops working.

**Codecs**: Statistical change-point in visual prediction; forward prediction stops being useful.

Different failure criteria, different formal objects. The analogy is only at the workflow level: both detect when forward prediction should be abandoned.

### Waiting ↔ Buffering (forced parallel)
**TVG**: Waiting at intermediate vertices when the next edge is not yet available. Bounded waiting changes complexity and expressivity ([Casteigts et al. 2021](https://link.springer.com/article/10.1007/s00453-021-00831-w)).

**Codecs**: B-frame buffering via the decoded picture buffer (DPB) ([Richardson, H.264/AVC](https://www.vcodex.com/h264avc-picture-management/)). DPB exists because decode order, display order, and reference management diverge.

Both involve deferred usability under temporal constraints, but the mathematical objects are not close.

---

## Temporal graph theory (TVG side)

### Formal framework
A temporal graph is a 5-tuple G = (V, E, T, ρ, ζ) where ρ is a presence function and ζ is a latency function. The formalism is edge-time based, not restricted to snapshot sequences. It unifies evolving graphs, temporal networks, and schedule-conforming paths ([Casteigts et al. 2012](https://www.site.uottawa.ca/~flocchin/Papers/tvg-ijpeds.pdf)).

### Journey
A time-respecting path: a sequence of edges where each edge departs after the previous one arrives, t_{i+1} ≥ t_i + ζ(e_i, t_i). Reachability is neither symmetric nor guaranteed to compose transitively.

### Temporal connectivity classes
13 classes with strict inclusion ([Casteigts et al. 2012](https://www.site.uottawa.ca/~flocchin/Papers/tvg-ijpeds.pdf), §5, Figure 4). The paper connects some classes to necessary conditions for particular distributed problems.

### Journey optimality criteria
Three formally distinct objectives:
- **Foremost**: arrive earliest
- **Fastest**: minimize duration
- **Shortest**: minimize hops

([Casteigts et al. 2012](https://www.site.uottawa.ca/~flocchin/Papers/tvg-ijpeds.pdf), §4.5)

### Waiting semantics
Bounded vs. unbounded waiting. Strict vs. non-strict journeys. These choices change complexity results ([Casteigts et al. 2021](https://link.springer.com/article/10.1007/s00453-021-00831-w)).

### Temporal spanners
Sparse subgraphs preserving journey distances up to multiplicative stretch α (called "temporal α-spanners"). Temporal cliques admit sparse spanners ([Casteigts, Peters & Schoeters 2021](https://www.sciencedirect.com/science/article/abs/pii/S0022000021000428)). [Bilò et al. 2022](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2022.19) give upper and lower bounds on spanner size. The optimization target is edge count, not bits.

### Blackout-tolerant spanners
Spanners that remain valid under timestep-wide edge deletion ([Blackout-tolerant spanners, 2023](https://www.sciencedirect.com/science/article/pii/S0022000023001009)).

### Timestamp perturbation
[Enright et al. 2025](https://eprints.gla.ac.uk/341921/) model worst-case reachability change under timestamp perturbation.

### Temporal network compression
[Adhikari et al. 2017](https://homepage.divms.uiowa.edu/~badhikari/assets/doc/papers/CondensingSDM2017.pdf) condense temporal networks while preserving propagation dynamics. [Allen et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11223189/) propose a commutator-based chronology compression method for preserving epidemic dynamics under aggregation. These are heuristic or dynamical-preservation programs, not formal rate-distortion theory.

### Event graphs
Mellor (2018) defines the **temporal event graph (TEG)**, a static DAG encoding event adjacency under time order; DAG-ness is proved in Lemma 3.2. Kivelä et al. (2018) define the **weighted event graph**, which explicitly encapsulates the complete set of δt-constrained time-respecting paths. Mellor's TEG is narrower than Kivelä's construction.

---

## Video codecs side

### Temporal prediction (H.261 → H.264)
H.261 (1988, [ITU-T H.261](https://www.itu.int/rec/T-REC-H.261)) uses intra/inter coding with motion-compensated prediction. MPEG-1 (1993, [ISO 11172-2](https://www.iso.org/standard/22411.html)) adds B-pictures. H.264/AVC (2003, [ITU-T H.264](https://www.itu.int/rec/T-REC-H.264)) adds multiple reference frames, decoded picture buffer management, and rate-distortion optimized mode selection. The dependency structure is engineered as a DAG, not usually treated as a formal mathematical object.

### I-frame / P-frame / B-frame
- **I-frame**: self-contained, no dependencies
- **P-frame**: forward prediction from a reference
- **B-frame**: prediction from past and future references; requires buffering

B-frames have no clean TVG analogue.

### Rate-distortion optimization
Bits vs. reconstruction quality via Lagrangian optimization: min D + λR. Sullivan & Wiegand (1998) systematize this approach for video encoder control, applying the Lagrangian framework of Shoham & Gersho (1988) to hybrid codecs ([Sullivan & Wiegand 1998](https://web.stanford.edu/class/ee398a/handouts/papers/Sullivan%20-%20RD%20Opt%20for%20Video.pdf)). TVG theory has no direct equivalent.

### Packet dependency formalization
[Chou & Miao 2006](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ChouM06.pdf) formalize packet dependencies for rate-distortion optimized streaming. The dependency DAG is taken as input to a scheduling problem, not itself optimized as a compressible object.

### Error accumulation and checkpoint resets
P-frame chains accumulate quantization or prediction error across references. I-frames reset that accumulation. TVG spanners preserve path properties approximately, but they do not model per-hop reconstruction error with explicit reset points.

### Error concealment
Approximate reconstruction when a reference is lost. TVG theory studies deletion and survivability, but not graceful approximate recovery of a missing journey.

### Multi-scale structure
Codecs operate at block, frame, and GOP levels simultaneously. Many temporal network compression papers work on snapshot sequences and treat the snapshot as the atomic unit.

### Static graph compression
[Navlakha et al. 2008](https://dl.acm.org/doi/abs/10.1145/1376616.1376661) propose MDL-based graph summarization with bounded per-node reconstruction error. This is not Shannon rate-distortion theory: no rate-distortion function, no converse bounds. A temporal extension with journey-aware distortion remains open.

---

## Converging from a third direction: algebraic topology on directed networks

Three bodies of work approach directed dependency networks from outside both video codecs and TVG theory. They do not solve the bridge, but they sharpen where it could be built.

### Cellular sheaves on directed graphs (strongest candidate)

Sheaf cohomology provides algebraic tools for distinguishing removable from irreducible edgewise error on directed dependency graphs. This is the closest formal contact point with codec-style predictive error found so far.

**Predictive coding as a sheaf-coboundary system.** [Seely (2025, NeurIPS Workshop)](https://arxiv.org/abs/2511.11092) constructs a cellular sheaf over a computational graph. The coboundary operator

> δ⁰: C⁰ → C¹, where (δ⁰s)\_e = s\_v − W\_e s\_u

maps activations to prediction errors. This has the same algebraic form as motion-compensated subtraction (current frame minus predicted frame). The predictive-coding energy is E = ½‖δ⁰s‖², and inference is diffusion under the sheaf Laplacian L = (δ⁰)ᵀδ⁰.

With clamped inputs/outputs, Seely replaces δ⁰ by a relative coboundary D. Inference minimizes ½‖Dz + b‖². The Hodge decomposition is exact:

> b = (−Dz\*) + r\*, where −Dz\* ∈ im D (removable by inference) and r\* ∈ ker Dᵀ (irreducible)

The first cohomology H¹ = C¹/im δ⁰ ≅ ker(δ⁰)ᵀ captures prediction-error patterns that no choice of activations can eliminate. The learning gradient factorizes as ∂E/∂W\_e = (Hb)\_e · (Gb)\_uᵀ, where H is the harmonic projector and G is a pseudoinverse. "Learning requires both a residual and a source. If either vanishes, the update at edge e is zero."

Two points matter for the codec analogy: the framework is **not restricted to DAGs** (recurrent topologies handled via monodromy operator Φ), and it is **linear networks only**. The prediction step in codecs (subtract motion-compensated reference from current frame) is linear, though the full codec pipeline includes nonlinear stages. The linear restriction aligns with the prediction stage specifically, not end-to-end.

**Network coding sheaves.** [Ghrist & Hiraoka](https://www2.math.upenn.edu/~ghrist/preprints/networkcodingshort.pdf) define a network coding sheaf F on a directed graph X = (V, E). Theorem 8: H⁰(X; F) = valid information flows. Max-flow ≤ min-cut derived via long exact sequence. Proposition 11 (Network Robustness): H⁰\_Z(X; F) = global flows on failure network G\\A; robust iff p⁰ = 0. Proposition 13 (Data Merging via Mayer-Vietoris): local flows merge iff g⁰(σ\_U, σ\_V) = 0. Exact network coding over a field k — no temporal dynamics, no noise.

**Semiring generalization.** [Krishnan 2014](https://arxiv.org/abs/1409.6712) treats sheaves on digraphs as functors from incidence posets into semimodules. Theorem 5.12: sheaf-theoretic MFMC — flow values equal the homotopy limit over cuts; equality when cohomology is exact. Duality gaps = failures of exactness. Works over **semirings** — handles probabilities, capacities, and tropical quantities natively.

**What sheaf theory still does not give**: temporal dynamics in the sheaf structure, rate-distortion, checkpoint/reset formalism.

### Tropical algebra / temporal state machines (quantitative and invariance side)

**Temporal state machines** ([PMC 9792072](https://pmc.ncbi.nlm.nih.gov/articles/PMC9792072/)). The tropical semiring T = (R∪{∞}, min, +) is physically realized as (first-arrival, delay). Key result — **time-translational invariance constraint**: all pure race logic must satisfy f(t₁+δ,...,tₙ+δ) = f(t₁,...,tₙ)+δ. Consequences:

- Raw addition of two time codes is **physically forbidden** by time-translational symmetry.
- Pure temporal logic = tropical linear (min and delay only).
- Tropical multiplication **requires memory** (state). Two-phase: (1) store incoming wavefront, (2) apply stored vector as delays. Order matters — non-commutativity arises from causal ordering of memory write/read.
- This is the formal boundary between stateless temporal composition and stateful computation. DAG structure enforces causal ordering.

**Parametric tropical geometry.** [Joswig et al. 2019](https://arxiv.org/abs/1904.01082) study parametric shortest paths via tropical geometry. Parametric weights (intervals), not temporal dynamics. Should not be cited for temporal state or non-commutativity claims.

### Persistent homology / path homology (weaker than expected)

[Chowdhury & Huntsman 2020](https://arxiv.org/abs/2008.11885) apply path homology to temporal networks through **static digraph snapshots** via sliding time windows, not the temporal structure itself. No stability theorems. No journey or reachability connection.

[Pritam et al. 2025](https://arxiv.org/html/2502.10076v1) classify temporal graphs using persistent homology with **average-timestamp-gap filtrations**. No stability theorems in the algebraic-topology sense. No journey connection.

This literature supplies summary invariants and algebraic tools, but not a temporal-compression theory.

### Speculative synthesis

A cellular sheaf on an event/dependency graph makes prediction error algebraic. Seely provides the operator dictionary:

- activations = 0-cochains
- prediction errors = 1-cochains
- prediction map = coboundary δ⁰
- removable error = image term (im D)
- irreducible error = harmonic/cohomological term (ker Dᵀ = H¹)

Krishnan's semiring generality (Theorem 5.12 works over semirings, so tropical coefficients are algebraically admissible) and the temporal state machines' invariance result (the boundary between tropical-linear and tropical-multiplicative is the boundary between stateless prediction and stateful buffering) strengthen the synthesis.

What remains missing: an encoding family, a distortion functional, a rate constraint, and temporal dynamics in the sheaf structure. Most of the ingredients exist separately; the assembly doesn't.

---

## Computational attempts (March 2026)

Three concrete computations were run against the open problems. Results below.

### Finding 1: Tropical MFMC breaks on event graphs (strongest result)

On a 4-vertex temporal graph, constructing the event graph (6 nodes, 6 edges, DAG) and defining a cellular sheaf with tropical stalks T = R∪{∞}:

- H⁰ (global sections) = earliest-arrival potentials. Unique anchored section: (0, 0, 1, 1, 2, 2).
- Naive tropical cut capacity = min over crossing edges = 1. Flow value to sink = 2. Max-flow > min-cut.
- **The duality breaks** because tropical flows are potentials, not conserved commodities. No subtraction in the tropical semiring means the coboundary cannot be written in standard form.

This is not a failure but a structural finding: Krishnan's Theorem 5.12 (sheaf MFMC over semirings) does not transfer naively to the tropical semiring on event graphs. The "flow" is an earliest-arrival schedule, and the "cut" must be redefined in terms of tropical potentials rather than crossing-edge minima. The obstruction is algebraic (lack of additive inverses), not an artifact of the example.

**Status:** Likely novel and nontrivial. Publishable as a short note if the failure criterion is made precise (counterexample + theorem characterizing when naive tropical cuts fail). Closest existing work: Ghrist-Hiraoka (2011) and [sheaf MFMC over abelian groups (2017)](https://polipapers.upv.es/index.php/AGT/article/download/3371/8705), both in additive/vector-space settings where conservation makes sense.

### Finding 2: Checkpoint spacing formula (known math, new interpretation)

For a linear prediction chain with iid weight matrix W and per-hop Gaussian drift N(0, σ²I):

- dim H¹_rel = d (constant). Checkpoints increase H¹ by d per checkpoint.
- E[‖r*‖²] = σ² · tr Gₙ(W) = σ² · Σᵢ (1 - μᵢⁿ)/(1 - μᵢ), where μᵢ = eigenvalues of WᵀW.
- Optimal checkpoint spacing with cost λ: L* ≈ √(2λ/(σ²d)) in the nearly-unitary regime.
- The relevant spectral quantity is which singular values of W are near/above 1, not the condition number.

**Status:** The mathematics (Green's function on a path with transport and drift) is standard. The codec interpretation (this recovers the GOP heuristic and corrects the condition-number intuition) is new but not sufficient for a standalone paper. Closest: Hansen-Ghrist (2019) on spectral sheaf theory, and standard matrix-weighted graph Laplacian literature.

### Finding 3: R-D achievability via timestamp coarsening (novel direction, shaky converse)

- Achievability: timestamp coarsening into bins of width Δ gives rate below lossless with controlled journey distortion. For the additive-slack interpretation, zero distortion is achievable below lossless rate.
- Converse attempt: the interval transfer tensor (foremost arrival times between all pairs within a checkpoint interval) is i.i.d. across intervals. Shannon converse gives R ≥ K · R_seg(D). Optimal spacing L* ≈ log(n)/log(np).
- **Issue:** journeys couple intervals, so the tensor-level converse does not directly yield end-to-end journey guarantees. The distortion definition needs repair (multiplicative vs. additive slack).
- Serialization approach (lossy LZ on flattened string) fails: Hamming distortion is agnostic to event criticality, so worst-case journey distortion is trivial.

**Status:** Novel direction, probably new at the exact formulation level. Not reviewer-ready. Closest: [Lossy compression of link streams (2020)](https://www.sciencedirect.com/science/article/pii/S0304397518307308), which gives an information-theoretic framework for lossy temporal graph compression but does not use journey-aware distortion.

---

## Open problems (updated)

### 1. Tropical flow-cut duality on event graphs
The naive tropicalization of sheaf MFMC breaks. What is the correct notion of tropical cut on a temporal event graph? Does Krishnan's equalizer formulation (avoiding explicit subtraction) resolve the obstruction, or is a fundamentally different cut notion needed? Characterize the class of semirings for which the sheaf MFMC transfers to event graphs.

### 2. R-D bounds for journey observables
The achievability direction works (timestamp coarsening). The converse needs: (a) a repaired distortion definition (additive slack, not multiplicative stretch), (b) a coupling argument showing the tensor-level converse extends to end-to-end journeys, or (c) a different approach entirely. The lossy link-stream framework of [Lamarche-Perrin (2019)](https://www.sciencedirect.com/science/article/pii/S0304397518307308) is the closest existing work and should be compared.

### 3. Checkpoint spacing on general graphs
The linear chain formula E[‖r*‖²] = σ² · tr Gₙ(W) is known math. The open question is whether it generalizes to non-chain dependency graphs (trees, DAGs with fan-out) in a way that produces nontrivial results. On general graphs, the Green's function structure is richer and the checkpoint placement becomes a combinatorial optimization.

---

## Questions for discussion

1. Where does the event graph ≅ prediction dependency DAG identification break first: B-frame bidirectionality, multi-reference prediction, or weighted event graph δt-semantics?
2. Temporal spanners optimize edge count, codec R-D optimizes bits. Is edge count a defensible proxy for bitrate, or does the encoding family matter fundamentally?
3. Is the lack of per-hop error accumulation in standard TVG a conceptual absence, or a modeling choice from exact/unweighted journey semantics?
4. **[Partially answered]** Seely's sheaf formalism is linear. The checkpoint spacing computation confirms this aligns with codec prediction. The open question is nonlinear extension.
5. **[Answered: no, not naively]** Can Krishnan's flow machinery be lifted to tropical event graphs? The naive lift breaks. Modified cut notions needed.
6. The temporal state-machine invariance constraint draws a formal line between stateless composition and stateful computation. Does this correspond to a known TVG distinction?
7. **[Answered: the duality breaks]** The tropical semiring does not yield a meaningful flow-cut duality via naive tropicalization. The question is now: what cut notion works?

---

## Sources

- Mellor 2018 — https://academic.oup.com/comnet/article/6/4/639/4360827
- Kivelä et al. 2018 — https://www.nature.com/articles/s41598-018-29577-2
- Chou & Miao 2006 — https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ChouM06.pdf
- Casteigts et al. 2012 — https://www.site.uottawa.ca/~flocchin/Papers/tvg-ijpeds.pdf
- Casteigts et al. 2021 — https://link.springer.com/article/10.1007/s00453-021-00831-w
- Casteigts, Peters & Schoeters 2021 — https://www.sciencedirect.com/science/article/abs/pii/S0022000021000428
- Bilò et al. 2022 — https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2022.19
- Blackout-tolerant spanners 2023 — https://www.sciencedirect.com/science/article/pii/S0022000023001009
- Enright et al. 2025 — https://eprints.gla.ac.uk/341921/
- Adhikari et al. 2017 — https://homepage.divms.uiowa.edu/~badhikari/assets/doc/papers/CondensingSDM2017.pdf
- Allen et al. 2024 — https://pmc.ncbi.nlm.nih.gov/articles/PMC11223189/
- Sullivan & Wiegand 1998 — https://web.stanford.edu/class/ee398a/handouts/papers/Sullivan%20-%20RD%20Opt%20for%20Video.pdf
- Navlakha et al. 2008 — https://dl.acm.org/doi/abs/10.1145/1376616.1376661
- Ghrist & Hiraoka — https://www2.math.upenn.edu/~ghrist/preprints/networkcodingshort.pdf
- Krishnan 2014 — https://arxiv.org/abs/1409.6712
- Seely 2025 (NeurIPS Workshop) — https://arxiv.org/abs/2511.11092
- Joswig et al. 2019 — https://arxiv.org/abs/1904.01082
- Temporal state machines — https://pmc.ncbi.nlm.nih.gov/articles/PMC9792072/
- Chowdhury & Huntsman 2020 — https://arxiv.org/abs/2008.11885
- Lamarche-Perrin 2019 — https://www.sciencedirect.com/science/article/pii/S0304397518307308
- Hansen & Ghrist 2019 — https://link.springer.com/article/10.1007/s41468-019-00038-7
- Pritam et al. 2025 — https://arxiv.org/html/2502.10076v1
- Path homologies of motifs — https://appliednetsci.springeropen.com/articles/10.1007/s41109-021-00441-z
- Chacholski et al. 2022 — https://arxiv.org/abs/2012.01033
