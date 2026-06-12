# Introducing a data structure in a paper: the acceptable range and scope

*Fan-out synthesis (3 convergent reviewers, opus) → codex adversarial pass. Purpose: decide how much machinery §3 (the hypothesis graph) needs, by mapping floor → ceiling and locating our venue (cs.AI + cs.SE).*

---

## TL;DR

There is a canonical skeleton every data-structure introduction shares, and a **range** of how heavily each part is developed. The floor is stricter than "a struct + an example" (below it, reviewers see a *file format* or a *rebranding*); the ceiling is the full algorithms/PL treatment (numbered invariants, complexity proofs, lower bounds). A focal structure in a mainline cs.AI/cs.SE paper sits in the **middle**: one named invariant, operation semantics with per-op preservation, one running example, a comparison table, an "isn't this just X?" rebuttal, and **one central claim of value** — which need *not* be an asymptotic number. For the hygraph, that claim is a **Local Replay Auditability** theorem (audit stays local to a node and its kill-edge, no whole-history replay), not a forced big-O and not "compression" on its own.

---

## 1. The canonical skeleton (what all three reviewers independently reached)

In order:

1. **Cost model / constraints first.** Name the resource you optimize, or the set of desiderata you need *simultaneously*, and show no prior structure clears all of them. The structure is shaped by a stated cost model, never introduced abstractly. (B-tree = disk I/O; Bloom = space-vs-error; CRDT = convergence-without-coordination; Bw-tree = "lock-free + cache-efficient + flash-friendly, no prior index gives all three.")
2. **The structure in one breath, then a NAMED INVARIANT** stated as a standalone contract — the intellectual core. Hard (B-tree balance, union-by-rank), statistical (skip-list levels), asymmetric (Bloom one-sided error), or by-construction (Merkle identity = H(content)).
3. **Operations as a small named set**, each with a signature and a one-clause argument that it **preserves the invariant**. CLRS does this with FIXUP case analysis and loop invariants; Okasaki with a shape predicate enforced by a "smart constructor"; Merkle by construction.
4. **One central claim of value** (the punchline). A complexity theorem (α(n), O(log_m n)), an error-probability derivation, a trade-off, or — legitimately — a *soundness* theorem.
5. **One running worked example, traced** through the operations, showing the hard case (a split to the root, a path compression, a kill that generates a non-obvious successor).
6. **Positioning vs alternatives** (often a table on the cost axis), plus an explicit **"isn't this just X?" rebuttal** for the nearest neighbor.

Deep pattern: **constraints → invariant → primitives+preservation → punchline → drawn example → comparison/rebuttal.** The invariant and the one central claim are non-negotiable.

---

## 2. The range: floor → middle → ceiling

| Dimension | **Floor** (means-to-an-end; workshop/tool/systems-secondary) | **Middle** (focal structure, cs.AI/cs.SE) | **Ceiling** (structure IS the contribution; algorithms/PL) |
|---|---|---|---|
| Invariant | one, in prose | one, named + stated as a contract | several numbered invariants, each *used* later |
| Operation semantics | prose pre/post | signatures + per-op preservation argument | typed signatures + pre/postconditions + smart constructors |
| Punchline | one nontrivial *consequence* of the invariant | one formal property (soundness/locality) + empirical evidence | complexity theorem(s) + proofs, often a matching lower bound |
| Complexity | none, if cost isn't asymptotic | informal cost in the *real* register (audit/trust), per op | worst-case or amortized, proven (banker/physicist) |
| Example | one, with state changes | one, threaded through *every* operation | multiple; hard cases and adversarial inputs |
| Positioning | a short paragraph | a comparison table + nearest-neighbor rebuttal | exhaustive related work + rebuttals to several neighbors |

**Floor (codex-corrected, stricter than "ADT + prose invariant").** The genuine minimum before a reviewer stops seeing "a format with a fancy name":

1. **Clear abstraction boundary** — what is *inside* the structure vs external metadata/artifacts.
2. **A named invariant** — one contract it always maintains.
3. **Operation *semantics*** — pre/postconditions or equivalent prose, not just names.
4. **A nontrivial consequence** of the invariant — something a user can *do* because it holds.
5. **Nearest-neighbor distinction** — why it is not merely a log, table, DAG, schema, provenance record, or TMS.
6. **One worked example** showing state changes.

Omit (3) or (4) → it reads as a **file format**. Omit (5) → it reads as **rebranding**. These two are the failure boundaries.

**Venue map.** *No quantified result at all* is acceptable only in softer venues (workshops, demos, tool papers, experience reports, dataset/schema papers, some HCI/CSCW) **or** when the structure is secondary to the paper's main claim. If the structure is *focal* in a mainline cs.AI/cs.SE paper, "no formal property" reads weak — you need a crisp formal property **plus** empirical evidence.

---

## 3. The punchline: one claim of value, not necessarily a number

The reviewers' "every data-structure paper has exactly one punchline number" is **overstated**. Corrected rule:

> A new structure needs one central claim of value, but that claim need not be asymptotic, numeric, or singularly quantified.

Algorithms papers usually want a theorem (time, space, lower bound, amortization). Systems/AI/SE papers may introduce a structure on a **non-asymptotic** claim if it supports a workflow, audit protocol, reproducibility guarantee, explainability regime, or empirical practice — *if stated sharply*.

**Substituting soundness for big-O is legitimate, with precedent:**

- **Proof-Carrying Code** (Necula, POPL 1997): the value is not a faster structure; an untrusted producer ships a proof a consumer independently checks. Acceptance is framed around checkable safety, not asymptotics. [dl.acm.org/doi/10.1145/263699.263712]
- **Certificate Transparency / Merkle logs** (RFC 9162): the property is append-only public auditability; Merkle *consistency proofs* show a later tree extends an earlier one. [datatracker.ietf.org/doc/html/rfc9162]
- **W3C PROV**: the contribution is a *model* for representing derivation (activities, agents, interchange), not a complexity result. [w3.org/TR/prov-overview]
- **ATMS / TMS** (Doyle 1979; de Kleer 1986): the nearest neighbor, but a *comparison target*, not shelter — it maintains justified belief under assumptions, it does not bind falsifiable hypotheses to replayable trials.

A **Replayability/Audit Soundness Theorem** is paper-grade *only if its terms are defined* (what "replay," "trial record / manifest completeness," "classification," "local evidentiary basis" mean). A theorem over undefined terms is the trap.

---

## 4. The #1 way these sections fail review: novelty collapse

> Reviewers decide the "new data structure" is just a provenance log / labeled DAG / workflow trace / TMS with new names.

It happens when the paper *names components* but never proves a distinctive invariant or an operation-level consequence. **Antidote: make the invariant do work.** Show, concretely, that a provenance log records *what happened*, a TMS records *belief dependencies*, a search tree organizes *exploration* — but this structure binds **falsifiable claims to replayable trials under kill-generated edges, with an append-only, distrust-auditable contract.** That sentence is the contribution; everything else is scaffolding for it.

---

## 5. Over-engineering: the ceiling you should NOT reach for cs.AI/cs.SE

Drop / avoid (reads as inflation in this venue):

- Lower bounds.
- Heavy amortized analysis unless operations have genuinely interesting scaling.
- Multiple numbered invariants unless each is *used* downstream.
- PL-style smart constructors unless implementation safety is central.
- Category-theory / logic machinery to make a DAG look sophisticated.
- Treating every field of the record as part of the formal model.
- More than one theorem unless the second is a direct **corollary**.
- Grand "general-purpose graph formalism" claims.
- Any formalism *before* the reader has seen the worked example.

The target is **"formal enough to prevent rebranding"** — no more.

---

## 6. Recommendation for the hygraph (§3)

**Where it sits: the middle.** Our current §3 already has the constraints-first opening (six constraints at once) and a CRUD operation list — the right backbone (template steps 1 and 4 of the operation set). What to add, in priority order:

1. **Per-constraint failure of alternatives.** For each of the six constraints, name which existing structure fails it (TMS/ATMS, search/proof tree, provenance/lineage log, vector-DB/RAG memory, plain agent scratchpad). Reviewers want to *see* that no prior structure clears all six, not be told.
2. **A comparison table.** Rows: hygraph, TMS/ATMS, provenance/lineage, plain agent memory/RAG, search tree. Columns = the six constraints (replayable-by-stranger, falsifiable-node, edge-from-kill, monotone/append-only, credence-typed-by-mode, prunable). This does the positioning *and* pre-empts novelty collapse.
3. **State the replay invariant as a standalone contract**, Merkle-style (soundness by construction), before any operation:
   > **Replay invariant.** Every node is reconstructible, by a stranger who does not trust the author, from its recorded trial alone (exact command + observed outcome + mode-typed credence).
4. **Each operation: signature → body → one-clause preservation argument.** create / query+replay / classify / edge-from-kill / prune. Make `append-node` a **smart constructor**: a node is admissible *only if* its trial replays, so the invariant holds by induction over reachable graphs. Give `edge-from-kill` the most space — it is the one genuinely novel operation.
5. **The punchline = Local Replay Auditability** (renamed from "Local Audit Soundness" per the 2nd codex sniff — "soundness" invites "sound w.r.t. *what* semantics?"; we only claim recorded-predicate-matched-recorded-outcome, so it is *auditability*, not soundness, unless fully parameterized). Not "compression" on its own:
   > **Local Replay Auditability.** Audit obligations stay local to a node and its kill-edge; an auditor verifies any single classification by re-running one recorded trial, without reconstructing the whole inquiry history.

   **Two replay levels (the distinction that "saves the paper"):** *Strong replay* = re-execute the command, reproduce the outcome — holds for deterministic shells, pinned tests, compilers/type-checkers, containerized runs (and our Verus lead case: pinned toolchain, forced-fresh fingerprinted builds). *Artifact replay* = verify the recorded transcript/hash, rerun only the deterministic predicate over it — claim this for LLM-driven trials, live APIs, retrieval; the command is a *provenance event*, not a reproducible computation. State the degradation explicitly. The honest core contribution: **local replay/audit obligations for LLM inquiry memory**, strong→artifact as LLMs/live systems enter.

   **Invariant tightenings (codex):** state I1 (replay) *conditional* on a captured environment (tool/model versions, seeds, corpus, network state); I2 (verdict=predicate(outcome)) is non-circular only if the predicate is *predeclared* and the gate is a versioned deterministic evaluator (record a **gate hash**); I3 (credence≤cap(mode)) is a *governance* invariant, not calibration; I4 (edge-from-kill) — say whether *witness* edges exist too. Add I5 (tamper-evident/append-only identity) and I6 (gate reproducibility = a named deterministic evaluator, not the LLM). Keep it *operational*, not a theorem that only holds under engineering assumptions.
   This is the hygraph's analogue of the Merkle audit path and PCC's checkable certificate — a legitimate, venue-appropriate headline that is *not* a forced big-O.
6. **Pruning as a corollary**, not a separate theorem: *pruning preserves replayability for retained nodes and preserves negative evidence via kill-edge summaries.* (Frame `prune` as a frontier-set operation — it changes what is *live*, never deletes from the persistent structure, so the append-only invariant is untouched.)
7. **Three explicit "isn't this just X?" rebuttals** (the exposed flanks):
   - **TMS/ATMS:** nodes are belief-status (IN/OUT) under logical justification and *non-monotone* (beliefs flip); hygraph nodes are hypotheses bound to a *recorded trial*, edges are *empirical kills* not deductive support, the structure is *monotone/append-only*, and the trust model is *replay by a distrusting stranger* (TMS trusts the author's justifications).
   - **Provenance log:** records *what happened* (flat lineage); hygraph adds *typed credence* and *kill-generated* structure.
   - **Search / proof tree:** a search tree finds, a proof tree justifies; the hygraph is *both at once* because the search path *is* the justification (every step was a trial), edges are empirical, and it is a graph closed under kills.
8. **One running example threaded through every operation** — the dead-light debugging inquiry (hypothesis "the bulb is dead" → exact command "swap in a fresh bulb" → observed outcome → kill → edge-from-kill names the next hypothesis → prune → surviving frontier). Reuse the *same* example for all six operations; systems readers track one example and lose a rotating cast.
9. **Honest cost register.** State what is guaranteed **by construction** (replayability of command+outcome; idempotent kills) vs **conventional** (the credence-mode label depends on honest tagging). Reviewers read the *absence* of this honesty as hand-waving.

**Do not:** force an asymptotic theorem, write multiple numbered invariants, import Okasaki's amortized machinery (wrong fit for a monotone, no-rebalance structure), or claim a general-purpose graph formalism.

---

## 7. Funnel log (provenance)

### H1: classic in-memory DS papers (opus) — survived
**Claims** (skip lists/Pugh, union-find/Tarjan+CLRS, B-tree/Bayer-McCreight, Bloom, Fenwick, hash tables):
- The skeleton is cost-model → baseline failure → invariant → primitives+cost → punchline → drawn example → comparison. [H1]
- "Exactly one punchline number" per paper. [H1] — **revised by codex** to "one central claim of value, not necessarily numeric."
- The invariant is the contribution; lead with the cost model. [H1, convergent with H2/H3]

### H2: persistent/functional + textbook conventions (opus) — survived
**Claims** (Okasaki PFDS, CLRS template, HAMT/Bagwell, ropes, Merkle):
- Operations-first / motivation-by-contrast; **named invariant as a standalone contract before any operation**; per-op invariant-preservation discipline. [H2, convergent with H1/H3]
- Immutability/monotonicity is *sold as a feature*: append-only → tamper-evident/auditable (Merkle); monotone + idempotent → confluence → lock-free parallel agents (CRDT/confluent persistence). [H2]
- The **Merkle "untrusting stranger verifies via an audit path"** pattern is our closest kin and strongest opening. [H2] — codex confirmed with PCC / Cert-Transparency / PROV precedents.
- Don't force amortized analysis on a monotone structure; the transferable Okasaki idea is the **smart constructor** + honesty about which guarantees are by-construction. [H2]

### H3: systems / distributed DS papers (opus) — survived
**Claims** (LSM, CRDT/Shapiro, Bw-tree, ART, learned indexes, TMS/ATMS, provenance):
- Systems rhetoric = **"N constraints at once, no prior structure satisfies all," + per-constraint failure of alternatives + comparison table + explicit "isn't this just X?" rebuttal.** [H3, convergent with H1]
- A **quantified cost claim is load-bearing** in systems papers — but codex narrowed this: a *formal property* (not necessarily quantified) plus empirical evidence suffices when the cost model is auditability.
- **TMS/ATMS is the most dangerous nearest neighbor**; the four distinctions (belief vs trial-bound hypothesis; deductive vs empirical-kill edge; non-monotone vs monotone; author-trusted vs stranger-replayable) must be written out. [H3]
- Headline cost claim should be **"audit is per-node and local, not global."** [H3] — codex elevated this to the recommended punchline (**Local Replay Auditability**).

### Codex convergence round (adversarial) — refinements adopted
- "One punchline *number*" → "one central claim of value, may be non-numeric."
- Floor raised to the 6-item minimum; *file format* (omit op-semantics/consequence) and *rebranding* (omit nearest-neighbor) are the named failure boundaries.
- Soundness-for-big-O is legitimate **with precedent** (PCC, Cert Transparency, PROV); ATMS is comparison-target not shelter.
- Punchline for us: **Local Replay Auditability**, pruning as a corollary; "compression" alone is too vague unless it states exactly what pruning preserves.
- #1 failure = **novelty collapse**; antidote = make the invariant do work.

**Convergence strength:** all three independent reviewers reached invariant-first + per-op preservation + one running example + comparison table + "isn't this just X?" rebuttal + don't-force-big-O. Codex did not overturn any convergent claim; it sharpened the punchline and raised the floor.

### Codex sniff round 2 (framing: data structure vs protocol; replay) — adopted
Triggered by two author doubts: "no clean way to turn each node into a structured invariant" (it's LLM-flavored) and "it's more like a protocol that happens to share the data structure."
- **The skeleton/payload split is real and citable, not a dodge** — the claim is "hygraph makes claims auditable by binding *opaque abductive content* to *executable evidence envelopes*." Precedents: CT (opaque entries + Merkle audit; closest for monotonicity), PROV (provenance edges w/o semantic truth; closest for edge-from-kill), Git (blobs + content-addressed structure), PCC (untrusted code + checkable certificate).
- **Protocol/contract framing STRENGTHENS** the contribution, *if* the title/abstract don't promise a pure theoretical graph structure then deliver a logging discipline. Phrase: "a persistent semantic-memory structure whose safety properties are defined by the writer/verifier protocol that maintains it." (Our title already names the protocol — safe.)
- **Rename the punchline** Local Audit Soundness → **Local Replay Auditability** (above).
- **Two replay levels** (strong vs artifact) is the load-bearing honesty; the Verus lead case is strong replay.
- **Invariant set** tightened to I1-conditional, I2-predeclared+gate-hash, I3-governance, I4-witness-edge-question, +I5 tamper-evident, +I6 gate-reproducibility.
- **Residual reviewer attacks** enumerated (novelty / semantics-gap / replay / LLM-dependence / evaluation / overformalization) with one-line answers each.
- **Deepest risk = replay** under nondeterminism (LLM gen, live APIs, retrieval); answer = artifact replay + explicit degradation. The semantics gap ("you verify the envelope, not the hypothesis") is ACCEPTED, not contested: the system audits *evidential warrant, not truth*.
