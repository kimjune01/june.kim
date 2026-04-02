# Pugmire Files — Parts Bin Additions

Algorithms surfaced from Calvin Pugmire's email (2026-04-02) on semantic memory in Soar.
Goal: decompose each system into named algorithms and classify for the Natural Framework Parts Bin.

**Method:** Seven systems decomposed by parallel subagents, each searching source code and primary literature. Round 1 classified systems; round 2 (this document) classifies algorithms. Codex (GPT-5.4) reviewed round 1 and caught contract drift — corrections applied throughout.

---

## Master Table: All Named Algorithms by Parts Bin Cell

Organized by Role × Data Structure. **Bold** = novel (original to the system). *Italic* = borrowed from prior work.

### Perceive

| Data Structure | Algorithm | System | Provenance |
|---------------|-----------|--------|------------|
| Flat | *Activation Noise (Logistic)* | ACT-R | Anderson & Lebiere 1998 |
| Tree | *Standardizing Apart (alpha-renaming)* | TRESTLE | Robinson 1965 |
| Tree→Flat | **Flattener** | TRESTLE | MacLellan 2016 |
| Tree→Graph | **SubComponentProcessor** | TRESTLE | MacLellan 2016 |

### Cache

| Data Structure | Algorithm | System | Provenance |
|---------------|-----------|--------|------------|
| Flat | *Welford's Online Algorithm* | TRESTLE/Cobweb | Welford 1962 |
| Flat | *Helmholtz Enumeration (fantasy generation)* | DreamCoder | Dayan, Hinton et al. 1995 |
| Tree | **Create operator** (new singleton node) | Cobweb | Fisher 1987 |
| Partial Order | *Event Calculus (Mueller variant)* | DCEC* | Kowalski & Sergot 1986; Mueller 2006 |
| Sequence | **Independent Rule Learning (IRL)** | CLARION | Nosofsky 1994; integrated by Sun 1997 |

### Filter

| Data Structure | Algorithm | System | Provenance |
|---------------|-----------|--------|------------|
| Flat | *Retrieval Threshold (step gate)* | ACT-R | Anderson 1993 |
| Flat | *Partial Matching (linear similarity penalty)* | ACT-R | Anderson & Lebiere 1998 (from Shepard 1987) |
| Flat | *LogSumExp Match Score* | ACT-R Blending | Standard (Gibbs 1902); applied by Lebiere 1999 |
| Flat | *Category Utility / Partition Utility* | Cobweb | Gluck & Corter 1985 (inner term: Gini 1912) |
| Flat | *Cobweb/3 Gaussian CU* | TRESTLE/Cobweb | McKusick & Thompson 1990 |
| Flat | *BLA forgetting wrapper* | Soar | Derbinsky & Laird 2011 (formula: Anderson 1990) |
| Flat | **Rule Extraction (positivity gate)** | CLARION | Sun, Peterson & Merrill 1996 |
| Flat | **Information Gain measure** | CLARION | Lavrac & Dzeroski 1994; applied by Sun 1997 |
| Flat | *MDL / Bayesian model selection* | DreamCoder | Rissanen 1978 |
| Tree | *Hindley-Milner type unification* | DreamCoder | Hindley 1969, Milner 1978 |
| Tree | *Incorporate operator* (sort into best child) | Cobweb | Kolodner 1984 / Lebowitz 1987; adapted by Fisher 1987 |
| Tree | *Natural deduction proof system* | DCEC* | Gentzen 1935 |
| Tree | *Inference schemata R4-R11, R15* | DCEC* | Original to DCEC* line 2008-2017 |
| Flat↔Tree | **Shadowing reduction** | DCEC* | Govindarajulu & Bringsjord 2017 |
| Flat | *SNARK (resolution + paramodulation)* | DCEC* | Stickel, SRI ~1990s |
| Flat | *SPASS (superposition calculus)* | DCEC* | Weidenbach, MPI ~1996 |
| Partial Order | **`means` operator** | DCEC* | Govindarajulu & Bringsjord 2017 |
| Partial Order | **DDE compliance predicate** | DCEC* | Govindarajulu & Bringsjord 2017 |

### Attend

| Data Structure | Algorithm | System | Provenance |
|---------------|-----------|--------|------------|
| Flat | *Boltzmann/Softmax/Luce choice rule* | ACT-R, CLARION | Luce 1959 / Boltzmann 1868 |
| Flat | *Weighted-Sum Integration* (cross-level) | CLARION | Ensemble methods; cognitive application by Sun 1997 |
| Flat | *Hungarian (Kuhn-Munkres)* | TRESTLE | Kuhn 1955 / Munkres 1957 |
| Graph | *Spreading Activation (fan-effect)* | ACT-R/Soar | Anderson 1983 (from Quillian 1967, Collins & Loftus 1975) |
| Graph | *Steepest-Descent Hill Climbing (swap neighborhood)* | TRESTLE | Classical; swap formulation by MacLellan 2016 |
| Tree | *Best-first type-guided enumeration* | DreamCoder | Ellis et al. 2018 |
| Tree | *Inference schemata R13, R14* (intention/action selection) | DCEC* | Original to DCEC* 2017 |
| Sequence | *Soar episodic retrieval* (cue-based ranking over temporal index) | Soar | Derbinsky & Laird, AGI 2009 |

### Remember

| Data Structure | Algorithm | System | Provenance |
|---------------|-----------|--------|------------|
| Flat | *Frequency estimation (MLE count update)* | Cobweb | Standard statistics |
| Sequence | *Power-law decay summation (BLA)* | ACT-R/Soar | Anderson 1990 (from Ebbinghaus 1885) |
| Tree | *Cobweb tree insertion* | Cobweb/TRESTLE | Fisher 1987 |

### Consolidate

| Data Structure | Algorithm | System | Provenance |
|---------------|-----------|--------|------------|
| Flat | **Blended Weighted Average** (Nadaraya-Watson) | ACT-R Blending | Nadaraya 1964, Watson 1964; applied by Lebiere 1999 |
| Flat | *Base-Level Learning equation* | ACT-R | Anderson 1990 |
| Tree | *Merge operator* (combine two siblings) | Cobweb | Fisher 1987 |
| Tree | *Split operator* (promote children) | Cobweb | Fisher 1987 |
| Tree | **Fragment Grammar Induction** (greedy MDL + anti-unification by enumeration) | DreamCoder | O'Donnell 2015 + Ellis et al. 2018 |
| Tree | *Inside-Outside algorithm* (EM for PCFGs) | DreamCoder | Baker 1979 |
| Tree | *Anti-unification* (virtue learning) | DCEC* ext. | Plotkin 1970; applied by Govindarajulu et al. 2018 |
| Graph (DAG) | **Version Space Compression** (n-step inverse beta-reduction + beam search) | DreamCoder | **Ellis et al. PLDI 2021** (core contribution) |
| Embedding Space | *QBP (Q-Learning-Backpropagation)* | CLARION | Watkins 1989 + Rumelhart 1986; combined by Sun 1997 |
| Embedding Space | *Top-Down Assimilation* | CLARION | Anderson ACT* 1983; implicit mechanism in CLARION |
| Embedding Space | *DreamCoder sleep-fantasy* (retrain recognition model) | DreamCoder | Helmholtz Machine (Dayan et al. 1995) |
| Partial Order | **Rule Generalization** (IG-based expansion on generality lattice) | CLARION | Sun et al. 2001 |
| Partial Order | **Rule Specialization** (IG-based shrinking on generality lattice) | CLARION | Sun et al. 2001 |
| Partial Order/Embedding | *Dissimilarity Minimization* (weighted 1-medoid / Fréchet mean) | ACT-R Blending | Fréchet 1948; applied by Lebiere 1999 |

---

## Corrections from Round 1

| Round 1 claim | Correction | Source |
|--------------|------------|--------|
| Cobweb = Consolidate × Tree | Cobweb spans 5 roles. Tree insertion = Remember. Merge/Split = Consolidate. CU = Filter. Incorporate = Filter. Create = Cache. | Cobweb agent |
| TRESTLE = Cache × Tree | Dual-phase: structure mapping = Cache (Hungarian + hill climbing = Attend). Sort = same as Cobweb (Remember + Filter + Consolidate). Three Perceive preprocessors. | TRESTLE agent |
| BLA = Filter × Flat | Dual-use formula. As forgetting wrapper = Filter. As scoring term in IBLT = part of Attend pipeline. As access-history tracker = Remember × Sequence. | BLA agent |
| ACT-R Blending = Attend × Flat | Blending's synthesis methods (weighted average, dissimilarity minimization) break the Attend contract. They produce synthetic chunks never stored. Closer to Consolidate. Softmax step is Attend; blending step is not. | Blending agent, codex |
| DCEC* = Consolidate × Partial Order | DCEC* is almost entirely Filter. No agent loop, no write-back, no policy update. It's a verification/constraint layer. Only Consolidate component (anti-unification) is from the 2018 virtue ethics extension, not core. | DCEC* agent |
| Episodic retrieval = Remember × Sequence | Remember = persistence. Cue-based retrieval with ranking = Attend × Sequence. | Codex |
| DreamCoder "E-graph refactoring" | Not E-graphs. Version spaces with inverse beta-reduction — a distinct data structure (DAG, not equality saturation graph). | DreamCoder agent |
| DreamCoder sleep-fantasy = Consolidate | Fantasy generation = Cache (indexes synthetic training data). Retraining the recognition model from those fantasies = Consolidate. | DreamCoder agent |
| CLARION RER = Consolidate × Flat | Rule Extraction itself = Filter (go/no-go gate). Rule Generalization/Specialization = Consolidate × Partial Order (traverse generality lattice). QBP = Consolidate × Embedding Space. | CLARION agent |

---

## New Cells and Notable Additions

### Genuinely new Parts Bin entries (not previously listed)

| Cell | Algorithm | Why it's distinct from existing entries |
|------|-----------|----------------------------------------|
| **Consolidate × Partial Order** | CLARION Rule Generalization/Specialization | Traverses generality lattice via IG. Existing entry "Lattice learning" is thin. These are concrete, implemented algorithms with named provenance. |
| **Consolidate × Graph (DAG)** | DreamCoder Version Space Compression | n-step inverse beta-reduction. No existing entry for Consolidate over DAGs specifically. |
| **Filter × Partial Order** | DCEC* `means` operator, DDE compliance predicate | Deontic gating over temporally ordered events. No existing Filter × Partial Order entry. |
| **Cache × Partial Order** | Event Calculus (Mueller variant) | Temporal indexing of fluents/events. Existing "Transitive closure (thin)" is different. |
| **Attend × Sequence** | Soar episodic retrieval | Cue-based ranking over temporal index. Corrected from Remember × Sequence. |

### Strongest additions to existing cells

| Cell | Algorithm | Why it's worth listing alongside existing entries |
|------|-----------|--------------------------------------------------|
| Consolidate × Flat | CLARION Rule Extraction + Blended Value (Nadaraya-Watson) | Structure extraction and kernel regression — mechanistically distinct from gradient descent |
| Consolidate × Tree | Cobweb Merge/Split, Fragment Grammar Induction, Inside-Outside | Incremental tree restructuring, program library compression, grammar EM — three distinct mechanisms |
| Filter × Flat | BLA forgetting, Retrieval Threshold, Partial Matching, Rule Extraction gate, IG measure, MDL scoring | Six distinct gating mechanisms with different signals (decay, threshold, similarity, positivity, information gain, description length) |
| Attend × Flat | Softmax/Luce, Weighted-Sum Integration, Hungarian | Three distinct ranking/selection mechanisms |

---

## Meta-findings

1. **Systems are not algorithms.** Every system decomposed into 6-10 named algorithms spanning 3-6 roles. The Parts Bin should never list a system name — only algorithm names.

2. **The same formula can serve different roles.** BLA is Remember (tracking access history), Filter (forgetting wrapper), or part of Attend (scoring term) depending on the enclosing procedure. Role belongs to the procedure, not the formula.

3. **Blending breaks the Attend contract.** Softmax retrieval is Attend. Blended weighted average is Consolidate (synthesizes a value never stored). The blending module straddles two roles — the ranking step is Attend, the synthesis step is Consolidate.

4. **DCEC\* is Filter, not Consolidate.** No agent loop, no write-back. It's a verification layer designed to be embedded in other architectures. The sole Consolidate component (anti-unification) is from an extension paper.

5. **Cobweb spans five roles.** A single algorithm that appears monolithic actually has Cache (create), Filter (incorporate, CU), Attend (CU ranking), Remember (count update, tree insertion), and Consolidate (merge, split) — all within one incremental insertion operation.

6. **ACT-R is a Bayesian retrieval engine assembled from off-the-shelf parts.** Every component (power-law decay, spreading activation, softmax, partial matching) is borrowed from statistics/psychophysics/choice theory. The innovation is the rational analysis framework that derives *why* they compose.

7. **CLARION's generality lattice earns Consolidate × Partial Order.** Unlike DCEC* (which was misclassified), CLARION's rule generalization/specialization genuinely traverses a partial order and writes back to the rule store, reshaping future action selection.

---

## Open questions for the Zoom call

1. **Calvin's synthesis approach.** He's not proposing one algorithm — he's composing across architectures. Which specific algorithm from each architecture does he plan to port into Soar? The composition itself is the research question.

2. **Cobweb/TRESTLE for Soar SMem.** Cobweb's incremental concept formation maps naturally onto semantic memory. But Soar's SMem currently has no merge/split operators — it's append-only. Adding Cobweb's Consolidate operators (merge, split) to SMem would give it the restructuring capacity it lacks.

3. **CLARION's rule extraction for Soar.** Soar has chunking (EBC) but no bottom-up rule extraction from subsymbolic patterns. CLARION's RER is the closest analogue. Could a similar extraction mechanism operate on Soar's RL-updated operator preferences?

4. **DreamCoder's version space compression for Soar.** Soar's chunking produces rules but never compresses them. DreamCoder's library compression (extract common sub-programs, add as new primitives) is exactly the operation Soar's procedural memory lacks.
