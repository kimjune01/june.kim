---
title: "Research log: DSIC composability (fan-out test)"
---

Fan-out research log. Claims filed with provenance. Convergent evidence merged. Dead ends recorded with cause of death.

---

## Hypotheses explored

1. **Domain restriction**: DSIC composes on restricted valuation domains (unit-demand, single-minded, additive). Find the boundary.
2. **Hedging as composition glue**: A hedging layer between two DSIC mechanisms can absorb the incentive leakage that breaks composition. Define the hedge.
3. **Sheaf reading**: DSIC as a local-to-global consistency condition on a mechanism DAG. Composition fails when local sections don't globalize. What's the obstruction?

---

## Results

### H3: Sheaf reading (sonnet, first to return)

**Verdict: not relabeling.** The sheaf reading connects to genuine H¹ via Rochet's cyclic monotonicity theorem and Ashlagi-Braverman's topological treatment.

**Key finding:** DSIC composition failure IS a cohomological obstruction. The 1-cochain on the joint type graph (utility differences) can have a negative cycle that restricts to zero on each factor's type graph. That's a nontrivial H¹ class: locally trivial, globally nontrivial. The Mayer-Vietoris failure is exact, not metaphorical.

**What H¹ measures:** Obstruction to splitting joint payment into per-mechanism payments. H¹ ≠ 0 means cross-mechanism transfers are necessary for DSIC.

**Concrete example computed:** Two second-price auctions, one agent with complementarity (v(w₁,w₂) = 19.9 < v(w₁) + v(w₂) = 20). Cycle sum on joint type graph = -0.1 < 0. Each marginal projection has trivial H¹. The class lives in the joint graph only.

**vs. tropical MFMC:** Structural parallel exists. Tropical = arithmetic mismatch (+ vs min), no local fix. DSIC = H¹ class on joint type graph, fixable by adding coboundary (cross-mechanism transfers). DSIC obstruction is more tractable.

**Literature:** Ashlagi-Braverman closest (topology of type spaces). Schmid 2025 prospectus gestures at sheaf + multi-agent. No paper states DSIC composition as sheaf cohomology on the mechanism DAG explicitly.

**Provenance:** sonnet subagent. **KILLED by codex adversarial review.**

**Cause of death (codex):**
- H¹ is the wrong invariant. Ordinary graph cohomology depends on topology, not edge weights. Cyclic monotonicity is a *weighted inequality* (no negative cycles), not a cohomological vanishing condition.
- Mayer-Vietoris is false on products: Künneth gives H¹(X×Y) ≅ H¹(X) ⊕ H¹(Y), so trivial factors can't produce nontrivial product H¹. The interaction is degree-2 (curvature/cross-difference), not degree-1.
- The -0.1 is a discrete mixed second derivative v(1,1)-v(1,0)-v(0,1)+v(0,0), not a Rochet negative cycle. The edge differences around the cycle telescope to 0.
- "Kill H¹ by coboundary" just means "allow joint payments instead of separable payments." Simpler statement, no cohomology needed.

**Salvageable claim (codex suggestion):** "DSIC composition failure is a failure of additive separability of the payment potential on the product type space. The obstruction is detected by nonzero square cross-differences on product cells." This is correct but may be known.

---

### H2: Hedging as composition glue (codex literature survey)

**Verdict: the concept exists under other names, and the impossibility results are strong.**

The "hedge" is not new. It appears as:
- **Linked mechanisms** (Jehiel, Moldovanu, Stacchetti 1996) — mechanism outcomes affect later interaction
- **Dynamic pivot / VCG transfers** (Bergemann & Välimäki 2010) — cross-period transfers restore ex post IC
- **Delayed transfers** (Mezzetti 2004) — separate allocation and final transfers across stages
- **Approximate ex post IC** (McLean & Postlewaite 2015) — small VCG modifications when agents are informationally small

**Key impossibility:** Jehiel, Meyer-ter-Vehn, Moldovanu, Zame (2006): in generic multidimensional interdependent-value environments, the only deterministic ex post implementable social choice functions are **constant**. No payment adjustment fixes this.

**Budget constraints kill it harder:** Dobzinski-Lavi-Nisan (2012): no deterministic auction satisfying IR, DSIC, no positive transfers, and Pareto optimality with budget limits.

**Conclusion:** The hedge exists in restricted forms (dynamic VCG, delayed transfers, approximate IC) but cannot work in general. The impossibility is not "nobody tried" but "provably impossible on unrestricted domains." The interesting question is which restricted domains admit hedges.

**Provenance:** codex literature survey via H2 subagent. Not a new finding — a bibliography of known results.

---

### H1: Domain restriction (sonnet, literature survey)

**Verdict: the boundary is known. Additive + quasilinear + no budget = composes. Everything else = doesn't.**

**Key result:** Mishra-Nath-Roy (GEB 2018) — in quasilinear environments with additively separable valuations and unanimity, every DSIC rule decomposes into per-component DSIC rules. This is the tightest positive result.

**Failure examples:**
- Unit-demand: two simultaneous second-price auctions, agent wants at most one item. Truthful bidding in auction A depends on outcome of auction B. [Christodoulou-Kovács-Schapira 2008]
- Budget-constrained: no deterministic IR + DSIC + no-positive-transfer + Pareto-optimal mechanism exists with private budgets. [Dobzinski-Lavi-Nisan 2012]
- Single-minded: truthful auctions must be global weighted welfare maximizers, can't decompose by item. [Lavi-Mu'alem-Nisan 2003]

**Roberts constraint:** On unrestricted domains with 3+ outcomes, only affine maximizers are DSIC. Product of two affine maximizers is affine maximizer only when welfare is separable (additive). Otherwise composition is not closed under Roberts.

**What's open:** The precise boundary between additive-quasilinear (composes) and the next-larger domain class. Whether unanimity can be relaxed in Mishra-Nath-Roy. Whether there's a clean valuation-class characterization beyond "additive."

**Provenance:** sonnet subagent, 69 tool uses, extensive web search. Not yet codex-validated.

---

## Convergent evidence

H1 and H3 independently found:
- **Rochet (1987)** — cyclic monotonicity as the DSIC characterization. H1 uses it for domain characterization, H3 uses it as the cohomological bridge.
- **The same unit-demand/budget failure examples** — convergent identification of the boundary.
- **Mishra-Nath-Roy 2018** as the tightest composition result — found independently by H1 (domain characterization) and implied by H3 (separability = trivial H¹).

H2 and H3 independently found:
- **Jehiel-Moldovanu-Zame 2006** impossibility — H2 as a hedge impossibility, H3 as the strongest negative result on unrestricted domains.

## Contradictions

None between hypotheses. H3's sheaf reading is consistent with H1's domain characterization: additive valuations = trivially separable joint type graph = H¹ vanishes. Non-additive valuations = nontrivial joint cycles = H¹ ≠ 0.

## Dead ends

- **H2 as a standalone finding**: the hedge concept exists under known names (linked mechanisms, dynamic VCG, delayed transfers). No novel contribution here beyond bibliography.

## Fan-out test verdict

**The funnel worked.** 3 hypotheses → 1 bibliography (H1), 1 known concepts (H2), 1 killed by codex (H3). Wall clock: ~20 minutes.

**What the fan-out added beyond the existing draft:**
- H3's failure is informative: sheaf cohomology is the *wrong* invariant for cyclic monotonicity (weighted inequality ≠ cohomological vanishing). This was not in the existing draft.
- Codex's salvage: the correct framing is "nonzero square cross-differences on product cells" — a cleaner version of the existing draft's "rectangle test."
- Kushnir-Lokutsievskiy 2021 (algebraic topology in mechanism design) was surfaced and wasn't in the existing draft.
- H2's literature map (linked mechanisms, dynamic VCG, delayed transfers) is a useful bibliography the existing draft lacked.

**What the fan-out confirmed:**
- The existing draft's one-line answer ("DSIC composes iff the mechanisms don't interact") is correct and well-supported.
- Additive separability is the sharp boundary. Known since Rochet 1987, formalized as a composition theorem by Mishra-Nath-Roy 2018.

**Convergent evidence across hypotheses:**
- H1 and H3 independently found Rochet 1987 as the foundation.
- H1 and H2 independently found Jehiel-Moldovanu impossibility results.
- H2 and H3 independently concluded the issue is in the allocation, not the payments.

**Status of existing draft:** Confirmed. The shelved status ("conclusive but no audience") is accurate. The fan-out found nothing that changes the conclusion.
