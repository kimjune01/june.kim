---
variant: post-medium
title: "Temporal Compression"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Consolidation Codec](/consolidate-codec). Extended in [Timekeeping Parameter](/timekeeping-parameter). Technical detail: [reading section](https://june.kim/reading/temporal-compression/). For agents and reviewers: [CROSSWALK.md](https://github.com/kimjune01/junekim-reading/blob/master/src/pages/temporal-compression/CROSSWALK.md).*

*A codec engineer keeps talking about how his video chains break. A graph theorist keeps talking about how her journeys don't compose. A topologist keeps talking about how his local sections won't globalize. Same complaint, three accents. None of them cites the other two.*

*The finding: on temporal event graphs, time accumulates along paths like a commodity but selects across paths like a potential. The tropical semiring encodes both operations, but the naive tropical analogue of max-flow/min-cut treats them as dual. They're not. That distinction is the paper inside this crosswalk.*

---

Three fields study directed dependency graphs with time-ordered composition. Across 37 searches on Google Scholar, Semantic Scholar, and the open web, combining terms from all three fields in every pairwise combination, I found zero cross-citations between any two of them.

**Video codecs** (empirical): I-frames store complete states. P-frames store deltas. Error accumulates through the chain. I-frames reset it. Rate-distortion optimization balances bits against reconstruction quality. The dependency structure is a DAG, treated as an engineering artifact.

**Temporal graph theory** (theoretical): A journey is a time-respecting path where each edge departs after the previous one arrives. Reachability is not transitive. 13 temporal connectivity classes determine which operations are possible. Temporal spanners preserve journey distances up to a stretch factor. The dependency structure is a DAG, treated as a formal object.

**Sheaf cohomology on directed networks** (mathematical): The coboundary operator maps activations to prediction errors. Hodge decomposition separates removable error from irreducible error. Duality gaps arise when local consistency fails to globalize. The dependency structure is a DAG, treated as a cell complex.

Same object. Different operations. Different vocabulary. No shared literature.

Time is a semiring, decomposable under compression, stable under composition. That's the claim. The rest of this post is the evidence.

### The one genuine parallel

Chain fragility. In temporal graphs, a journey breaks when timing fails to compose. In codecs, a P-frame chain breaks when a reference is lost. In sheaves, local sections fail to extend globally when exactness fails. Three triggers, one structural pattern: sequential dependency over a time-ordered DAG where breaking any link severs the tail.

### The operator dictionary

<table style="max-width:700px; width:100%; margin:1.5em auto; font-size:14px; border-collapse:collapse;">
<colgroup><col style="width:22%"><col style="width:22%"><col style="width:22%"><col></colgroup>
<thead>
<tr><th style="background:#f0f0f0; padding:0.6em 0.8em; text-align:left">Codec</th><th style="background:#f0f0f0; padding:0.6em 0.8em; text-align:left">Temporal graph</th><th style="background:#f0f0f0; padding:0.6em 0.8em; text-align:left">Sheaf</th><th style="background:#f0f0f0; padding:0.6em 0.8em; text-align:left">Shared meaning</th></tr>
</thead>
<tr><td style="padding:0.6em 0.8em">Prediction residual</td><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em">Coboundary δ⁰</td><td style="padding:0.6em 0.8em">Per-edge error</td></tr>
<tr style="background:#fafafa"><td style="padding:0.6em 0.8em">Irreducible error</td><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em">H¹</td><td style="padding:0.6em 0.8em">Error no choice can remove</td></tr>
<tr><td style="padding:0.6em 0.8em">I-frame</td><td style="padding:0.6em 0.8em">Snapshot graph</td><td style="padding:0.6em 0.8em; white-space:normal">Clamped sub-complex</td><td style="padding:0.6em 0.8em">Checkpoint that resets dependencies</td></tr>
<tr style="background:#fafafa"><td style="padding:0.6em 0.8em">P-frame</td><td style="padding:0.6em 0.8em">Edge delta</td><td style="padding:0.6em 0.8em">1-cochain</td><td style="padding:0.6em 0.8em">Delta from reference</td></tr>
<tr><td style="padding:0.6em 0.8em">Chain break</td><td style="padding:0.6em 0.8em">Journey break</td><td style="padding:0.6em 0.8em">Exactness failure</td><td style="padding:0.6em 0.8em">Sequential dependency severed</td></tr>
<tr style="background:#fafafa"><td style="padding:0.6em 0.8em">R-D optimization</td><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em">Bits vs. quality</td></tr>
<tr><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em; white-space:normal">Foremost / fastest / shortest</td><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em">Path optimality criteria</td></tr>
<tr style="background:#fafafa"><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em">Connectivity class</td><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em">13 classes, strict inclusion</td></tr>
<tr><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em; opacity:0.3">—</td><td style="padding:0.6em 0.8em; white-space:normal">Hodge decomposition</td><td style="padding:0.6em 0.8em">Removable + irreducible split</td></tr>
</table>


### Three theorems not in the literature

#### R-D bounds for journey observables

Given a bit budget, what is the minimum distortion in journey metrics? Codecs have the R-D framework. TVGs have the journey formalism. Timestamp coarsening achieves rates below lossless with controlled journey distortion, but the converse stalls: journeys couple across intervals, so a tight lower bound remains open. [Worked through here.](/reading/temporal-compression/ch-04)

#### Temporal sheaves

Define a cellular sheaf on a temporal event graph with tropical coefficients. Does the sheaf-theoretic max-flow/min-cut yield a meaningful temporal reachability result? [Krishnan's Theorem 5.12](https://arxiv.org/abs/1409.6712) works over semirings. Time is a semiring: min is "first to arrive," + is "accumulate delay." [I checked.](/reading/temporal-compression/ch-04) The naive tropicalization breaks: on a 4-vertex event graph, the cut capacity is 1 but the flow value is 2. The obstruction is structural — tropical flows are potentials, not conserved commodities, and no local edge-based cut notion can restore duality. A global potential-barrier cut does restore it, but that's a different theorem.

#### Checkpoint spacing from H¹

On a prediction DAG, [Seely's](https://arxiv.org/abs/2511.11092) coboundary produces edgewise residuals and Hodge decomposition splits them into removable and irreducible components. What checkpoint spacing keeps the irreducible component below a quality threshold? Surprise: checkpoints *increase* dim H¹, not decrease. The right quantity is residual norm under drift, not cohomological dimension. The closed form gives optimal spacing L* ≈ √(2λ/(σ²d)) in the nearly-unitary regime, recovering what codec engineers already do operationally. [Derivation.](/reading/temporal-compression/ch-05)

### The bridge

The vocabulary barrier is the obstacle, not the mathematics. If it falls, codec engineers get a formal theory of chain fragility. Graph theorists get a decomposition of temporal error into removable and irreducible components. Topologists get a billion hours of video as empirical validation.

Three fields, one structure, zero cross-citations. I'm fixing that.

---

*Written via the [double loop](/double-loop).*
