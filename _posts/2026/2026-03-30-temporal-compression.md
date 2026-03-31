---
layout: post
title: "Temporal Compression"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Consolidation Codec](/consolidate-codec). Extended in [Timekeeping Parameter](/timekeeping-parameter). Technical detail: [reading section](https://june.kim/reading/temporal-compression/). For agents and reviewers: [CROSSWALK.md](https://github.com/kimjune01/junekim-reading/blob/master/src/pages/temporal-compression/CROSSWALK.md).*

Three fields study directed dependency graphs with time-ordered composition. Across 37 searches on Google Scholar, Semantic Scholar, and the open web, combining terms from all three fields in every pairwise combination, I found zero cross-citations between any two of them.

**Video codecs** (empirical): I-frames store complete states. P-frames store deltas. Error accumulates through the chain. I-frames reset it. Rate-distortion optimization balances bits against reconstruction quality. The dependency structure is a DAG, treated as an engineering artifact.

**Temporal graph theory** (theoretical): A journey is a time-respecting path where each edge departs after the previous one arrives. Reachability is not transitive. 13 temporal connectivity classes determine which operations are possible. Temporal spanners preserve journey distances up to a stretch factor. The dependency structure is a DAG, treated as a formal object.

**Sheaf cohomology on directed networks** (mathematical): The coboundary operator maps activations to prediction errors. Hodge decomposition separates removable error from irreducible error. Duality gaps arise when local consistency fails to globalize. The dependency structure is a DAG, treated as a cell complex.

Same object. Different operations. Different vocabulary. No shared literature.

Time is a semiring, decomposable under compression, stable under composition. That's the claim. The rest of this post is the evidence.

### The one genuine parallel

Chain fragility. In temporal graphs, a journey breaks when timing fails to compose. In codecs, a P-frame chain breaks when a reference is lost. In sheaves, local sections fail to extend globally when exactness fails. Three triggers, one structural pattern: sequential dependency over a time-ordered DAG where breaking any link severs the tail.

### The operator dictionary

| Codec | Temporal graph | Sheaf | Shared meaning |
|---|---|---|---|
| prediction residual | — | coboundary δ⁰ | Per-edge error |
| irreducible error | — | H¹ | Error no choice can remove |
| I-frame | snapshot graph | clamped sub-complex | Checkpoint that resets dependencies |
| P-frame | edge delta | 1-cochain | Delta from reference |
| chain break | journey break | exactness failure | Sequential dependency severed |
| R-D optimization | — | — | Bits vs. quality |
| — | foremost / fastest / shortest | — | Path optimality criteria |
| — | connectivity class | — | 13 classes, strict inclusion |
| — | — | Hodge decomposition | Removable + irreducible split |

The blanks are the open problems.

### Three missing theorems

**1. R-D bounds for journey observables.** Given a bit budget, what is the minimum distortion in journey metrics? Codecs have the R-D framework. TVGs have the journey formalism. The combination is open.

**2. Temporal sheaves.** Define a cellular sheaf on a temporal event graph with tropical coefficients. Does the sheaf-theoretic max-flow/min-cut yield a meaningful temporal reachability result? [Krishnan's Theorem 5.12](https://arxiv.org/abs/1409.6712) works over semirings. Time is a semiring: min is "first to arrive," + is "accumulate delay." The theorem applies. As of March 2026, nobody has checked.

**3. Checkpoint spacing from H¹.** On a prediction DAG, [Seely's](https://arxiv.org/abs/2511.11092) coboundary produces edgewise residuals and Hodge decomposition splits them into removable and irreducible components. What checkpoint spacing keeps the irreducible component below a quality threshold? Codec engineers solve this operationally. The theorem is missing.

### The bridge

The contribution is not new mathematics. Three fields study the same structure. Each field's operations would extend the others. Nobody has said this because the three communities don't share venues.

The codec engineer's I-frame reset is the topologist's clamped sub-complex. The TVG theorist's chain fragility is the sheaf theorist's exactness failure. The vocabulary barrier is the obstacle, not the mathematics.

---

*Written via the [double loop](/double-loop).*
