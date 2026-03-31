---
title: "Theorem Attempts"
---

Notes from computational attempts at the three missing theorems (March 30, 2026). Each theorem was given a concrete small example and asked to produce actual derivations. Results from GPT-5.4 (codex), validated by Claude Opus 4.6.

---

## Theorem 1: R-D bounds for journey observables

**Setup:** Temporal Erdős-Rényi, n vertices, edge probability p per timestep, T timesteps. Distortion = fraction of reachable pairs whose foremost journey stretches by more than factor α.

**What landed:**

*Timestamp coarsening.* Bin timestamps into intervals of width Δ. If Δ ≤ α, distortion is exactly zero and rate drops below lossless:

> R = M · ceil(T/Δ) · h₂(1 - (1-p)^Δ)

This is a clean achievability result: you can compress a temporal graph while preserving all journey durations exactly under the multiplicative metric. For α ≥ 2, you beat lossless rate with zero distortion.

*Random edge dropping.* Retain each edge with probability q. Loose upper bound:

> R(D) ≤ MT · h₂(p · (1-D)^{1/(αT)})

*Converse (lower bound).* Via critical direct contacts at time 1 with no alternate journey by time α:

> R(D) ≥ M · [h₂(p) - h₂(ρD / β_α)]⁺

**Where it got stuck:**

The converse is loose because distortion is global and non-separable. Whether dropping one edge causes distortion depends on the entire graph's alternative journey structure. Pivotality is correlated across edges because journeys share edges. The lower bound only captures direct-contact pivotality. Extending it requires counting families of nearly-independent pivotal temporal paths, and overlap among time-respecting paths destroys the independence needed for a sharp mutual-information argument.

**Entropy of temporal Erdős-Rényi:** H(X) = MT · h₂(p) bits (iid Bernoulli over edge-time slots).

---

## Theorem 2: Tropical sheaves on event graphs

**Setup:** 4 vertices, 6 edges, 3 timesteps. Event graph constructed (6 nodes, 6 edges, DAG). Cellular sheaf with tropical stalks T = R∪{∞}, restriction maps as delay accumulation.

**What landed:**

*Tropical flow = earliest-arrival potential.* H⁰ (global sections) = consistent schedules. Anchored at 0, the unique section on the example is (0, 0, 1, 1, 2, 2). This is a valid computation.

*The duality breaks.* Naive tropical cut: min(1, 1, 2, 2) = 1. Flow value to sink: 2. Max-flow ≤ min-cut reads 2 ≤ 1, which is false.

**The finding:**

The naive tropicalization breaks the duality in the interesting direction. A tropical flow is a potential/schedule, not a conserved commodity. Tropical cut capacity (cheapest edge on the cut) ignores downstream delay accumulation. The standard coboundary cannot be written in the usual form because the tropical semiring has no subtraction.

**What it needs:**

A modified cut notion — tropical potentials rather than tropical sum over cut edges. Krishnan's equalizer-based formulation may handle this, but the concrete computation shows the standard MFMC statement does not transfer naively. The duality gap is real and structural, not an artifact.

**Open question for Krishnan:** Does your Theorem 5.12's equalizer formulation avoid this problem, or does the lack of additive inverses in the tropical semiring create a genuine obstruction?

**UPDATE: Adversarial testing and modified cut attempts (March 30).**

Theorem 4.1 is correct but close to tautological (min < sum for k ≥ 2 positive terms). The real content is not the inequality but the structural observation.

**Impossibility result:** No purely local edge-based cut notion can work. Proof: take the diamond with all weights 1 (flow = 2), change only non-cut edges to weight 100 (flow = 101). Any cut capacity depending only on crossing-edge data assigns the same value to both cases, so it cannot match flow in both. This is a stronger result than the counterexample alone.

**What does work:** The potential barrier / distance-decorated separator. For any edge cut F, define κ(F) = min over (u,v) ∈ F of [d(s,u) + τᵤᵥ + d(v,t)]. This always equals d(s,t) for every separator. Duality is exact, but the dual object is a global potential incorporating distance information from both sides of the cut, not a local edge quantity.

Four cut notions tested:
1. Path-capacity cut: vacuous (collapses to shortest-path length regardless of cut)
2. Potential barrier: works exactly, but dual object is global
3. Equalizer/coequalizer: collapses to potential barrier numerically
4. Bottleneck cut: fails immediately (max_F min_e τ_e ≠ d(s,t))

**Paper structure upgrade:** The paper now has three results, not one:
1. Naive edge-based tropical cut fails (counterexample)
2. No local edge-based cut can work (impossibility, two-graph argument)
3. Global potential barrier restores exact duality (constructive)

---

## Theorem 3: Checkpoint spacing from H¹

**Setup:** Linear chain v₀ → v₁ → ... → vₙ, d-dimensional stalks, weight matrices Wᵢ as restriction maps. Clamped endpoints (v₀ = input, vₙ = target). Computed for n=4, d=2, concrete 2×2 matrices.

**What landed:**

*dim H¹_rel = d for an endpoint-clamped chain.* Always. Independent of chain length or weight matrices.

*With c interior checkpoints, dim H¹_rel = (c+1)d.* Checkpoints INCREASE H¹.

*Irreducible residual norm:*

> ‖r*‖² = (xₙ - Pₙx₀)ᵀ (YᵀY)⁻¹ (xₙ - Pₙx₀)

where Pₙ = Wₙ₋₁ · ... · W₁ (chain product) and Y is built from suffix products.

**The surprise:**

Checkpoints do not reduce H¹. They increase it. Each checkpoint creates an independent segment, each with its own d-dimensional obstruction. Checkpoints cannot improve the minimum irreducible error in the deterministic case — the unconstrained global solve already picks optimal intermediate states.

**The reframing:**

The codec GOP heuristic is recovered only after adding a drift/noise model: x_{i+1} = Wᵢ xᵢ + εᵢ. Under drift, longer segments accumulate more forcing. Checkpoints help because they inject ground-truth data that resets accumulated mismatch, not because they change the topology.

The right quantity is not dim H¹ (which increases with checkpoints) but ‖r*‖ under drift (which decreases with checkpoints). The distinction: checkpoint placement is an optimization problem (minimize total residual norm across segments given a drift model), not a topological one (find sub-complexes where H¹ vanishes).

**The result, restated:**

For a linear prediction chain with per-hop drift εᵢ ~ N(0, σ²I):

- Each segment of length L contributes expected irreducible residual proportional to σ² · f(W₁,...,W_L) where f depends on the spectral properties of the weight matrices
- Optimal checkpoint spacing minimizes total residual across segments
- This recovers the codec heuristic: shorter GOPs for high-motion content (large σ²), longer GOPs for static content (small σ²)

**UPDATE: The spectral quantity has been derived in closed form.**

f(W, n) = tr Gₙ(W) = Σᵢ (1 - μᵢⁿ)/(1 - μᵢ), where μᵢ are eigenvalues of WᵀW.

E[‖r*‖²] = σ² · tr Gₙ(W). Residual grows as a geometric series in the squared singular values.

With checkpoint cost λ, optimal spacing: L* ≈ √(2λ / (σ²d)) in the nearly-unitary regime.

Codec predictions confirmed: higher noise → shorter GOP, poor prediction → shorter GOP. But the relevant quantity is which singular values of W are near or above 1, not the condition number. That's a sharper statement than the engineering heuristic and a correction to the standard intuition.

This is paper-grade. One theorem, one closed-form quantity, one corollary recovering practice, one correction to intuition.

**UPDATE: Tree generalization (March 30).**

For trees, the chain formula is the whole story: total residual = sum over root-to-leaf paths of the chain formula. No cross-terms. Per-leaf quality depends only on depth, not topology.

Fan-out gives a 1/√k amortization factor: L*_fanout ≈ √(2λ/(kσ²d)). One root checkpoint protects all k descendants. Shared ancestors should always be checkpointed before leaves.

The genuinely new phenomenon appears only at DAG reconvergence (diamond), where multiple paths from the same noise source create cross-terms via ‖Σₚ Aₚ‖²_F. The chain result is the whole story for trees. DAGs with reconvergence are where the generalization gets nontrivial.

---

## String compression parallel

All three theorems have analogues in string compression that are already solved:

**Theorem 1 ↔ Lempel-Ziv.** A string is a temporal graph on a path graph (one vertex, self-loops at each timestep). LZ77's sliding window is a GOP. LZ78's dictionary entries are I-frames. The R-D problem for strings (rate-distortion under edit distance or Hamming distance) is well-studied. The converse for strings works because symbol positions are independent conditioned on the dictionary — the pivotality correlation that kills the temporal graph converse is absent in 1D.

**Insight for Theorem 1:** The converse might work if the temporal graph is serialized (edge list sorted by timestamp) and string compression bounds are applied to the serialization. The question is whether the serialization preserves enough journey structure for the distortion functional to remain meaningful.

**Theorem 2 ↔ Grammar compression.** The smallest context-free grammar generating a string is structurally a sheaf: each production rule is a local section, the grammar is a global section iff all rules are consistent, and the compressed size is the number of rules (= dim H⁰). Grammar-based codes achieve entropy rate on ergodic sources. The tropical duality break in Theorem 2 might be resolvable by replacing flow/cut with grammar/parse — the "cut" becomes a partition of the parse tree, not a partition of the graph.

**Theorem 3 ↔ Adaptive dictionary reset.** LZ77 resets its sliding window; LZ78 resets its dictionary. The optimal reset interval balances dictionary size (= checkpoint cost) against match length (= compression efficiency, which degrades as the source statistics drift). This is exactly the checkpoint spacing problem. The difference: string compressors operate on stationary ergodic sources where the drift model is well-characterized. Temporal graphs have richer structure.

**The generalization:** String compression is the one-dimensional case of temporal graph compression. A string is a temporal graph on a path graph. LZ/grammar compression solved the R-D problem for that special case. The three open theorems are the generalization from paths to DAGs with branching temporal structure.

---

## Advisory: what to do next

**Theorem 3 is closest to landing.** The reframing (‖r*‖ under drift, not dim H¹) is clean and computable. Next step: derive f(W₁,...,W_L) in closed form for the iid case (all Wᵢ = W). If f = something involving the condition number of W, write it up.

**Theorem 1 has both achievability and converse.** Achievability: timestamp coarsening preserves all α-stretch journeys at rate below lossless. Converse: the interval transfer tensor (foremost arrival times between all pairs within a checkpoint interval) is exactly i.i.d. across intervals, giving R ≥ K · R_seg(D) via Shannon's converse. Optimal checkpoint spacing: L* ≈ log(n)/log(np), the mixing time of the temporal spreading process. Bounds are tight in the sparse regime, loose in supercritical. The serialization approach (lossy LZ on the flattened string) fails — see below — but the tensor approach succeeds because it preserves journey structure.

**Theorem 2 needs a reformulation before more computation.** The tropical duality break is a finding, not a failure. The question for Krishnan is precise: does his equalizer formulation avoid the problem, or is a different cut notion needed? Don't compute more until the formulation is right.

**The string compression connection should be explored in the next session.** It may unify all three theorems under a single framework: temporal graph compression as generalized string compression on DAGs.

---

## Insight under test: lossy string compression as a search space

P-frame diffs are lossy deltas. Cap the loss at ε per hop. The set of diffs within ε of the true delta is a ball in some metric space. A dictionary (codebook) stores representative diffs — centroids of those balls. Encoding a P-frame becomes nearest-neighbor lookup. That's vector quantization on temporal deltas.

Second-order diffs (diff of diffs) exploit structure in how the deltas themselves change over time. The delta sequence has its own temporal regularity. Compressing it is compressing a derived temporal graph — the "acceleration" graph one level above the "velocity" graph.

**The search space:** Every lossy string compression algorithm with a tunable loss parameter (lossy LZ, lossy grammar compression, rate-constrained dictionary coding) defines a candidate temporal graph compression algorithm when applied to a serialized event graph. The loss parameter maps to journey distortion. The dictionary structure maps to the checkpoint/delta architecture. The algorithm's convergence properties map to the R-D curve.

The space of temporal graph compression algorithms is at least as large as:

> (lossy string compressors) × (temporal graph serializations)

Known good solutions exist in the string compression corner: LZ, grammar codes, Burrows-Wheeler. Each becomes a candidate for temporal graphs via serialization of the event graph. The open question: which serialization preserves enough journey structure for the string compressor's loss guarantee to translate into a journey distortion guarantee?

This reframes Theorem 1's converse problem. Instead of proving R-D bounds directly on temporal graphs (where pivotality correlation kills the argument), prove them on the serialized string (where existing converse theorems apply) and then bound the distortion gap introduced by serialization.

**UPDATE: Serialization approach fails.** Hamming distortion counts corrupted symbols uniformly, but journey distortion depends on *which* symbols are corrupted. One bridge event on every journey means ε ≥ 1/m gives worst-case D* = 1. Serialization order doesn't help — the adversary targets critical events regardless of permutation. Average-case bounds exist (E[D] ≤ ε·E[|J|]) but are weak for long journeys.

The failure points to what a real approach needs: a distortion measure aware of event criticality. Not Hamming on a string, but weighted distortion where the weight is the event load (fraction of journeys through that event). The sheaf connection re-enters here: event criticality is measurable via the coboundary. Events with large harmonic projection are the ones whose corruption breaks journeys. This suggests a sheaf-weighted rate-distortion formulation where the encoding prioritizes high-load events — which is exactly what codec engineers do when they allocate more bits to reference frames.
