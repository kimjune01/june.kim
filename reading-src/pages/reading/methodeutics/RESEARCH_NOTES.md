# Methodeutics: Research Notes

Full lineage from Peirce (1878) to Ramdas (2023). Organized chronologically within five eras.

## I. Foundations (1878–1939)

| Year | Figure | Key work | Contribution to methodeutics |
|------|--------|----------|------------------------------|
| 1878 | **Peirce** | "Deduction, Induction, and Hypothesis" | Named abduction. Three modes are irreducible. |
| 1879 | **Peirce** | "Economy of Research" | Optimal experiment selection by marginal utility/cost. Predates Wald by 65 years. |
| 1884 | **Peirce & Jastrow** | First randomized experiment | Predates Fisher's formalization of randomization by 40 years. |
| 1902 | **Peirce** | Carnegie Application | Named methodeutic as the third branch of logic. |
| 1908 | **Peirce** | "A Neglected Argument" | Musement: free contemplation as the pre-logical source of abductive hypotheses. |
| 1913 | **Peirce** | "Essay toward Improving Reasoning" | Uberty/security tradeoff. Abduction: highest uberty, lowest security. |
| 1933 | **Kolmogorov** | *Grundbegriffe* | Axiomatized measure-theoretic probability. The framework Shafer-Vovk deliberately replace. |
| 1934 | **Popper** | *Logik der Forschung* | Denied discovery has a logic. Context of discovery vs. context of justification. Everyone after him reacts to this claim. |
| 1937 | **de Finetti** | "La prévision" | Grounded probability in coherent betting. Exchangeability theorem. Philosophical ancestor of testing-by-betting. |
| 1938 | **Dewey** | *Logic: The Theory of Inquiry* | Carried Peirce's theory of inquiry into the mainstream. Logical forms arise within inquiry, not prior to it. |
| 1939 | **Ville** | Doctoral thesis | Martingale betting strategies. Ville's inequality: nonneg supermartingale starting at 1 exceeds 1/α with prob ≤ α. Direct foundation of e-values. |

## II. The Statistical Revolution (1940–1970)

| Year | Figure | Key work | Contribution |
|------|--------|----------|--------------|
| 1925/35 | **Fisher** | *Design of Experiments* | Formalized p-values, randomization, significance testing. What e-values replace. |
| 1933 | **Neyman-Pearson** | "Most Efficient Tests" | Type I/II errors, power, likelihood ratio test. The LR is ancestor of the e-value. |
| 1945 | **Pólya** | *How to Solve It* | Codified heuristic reasoning. Distinguished demonstrative from plausible reasoning. Lakatos and Schoenfeld build on this. |
| 1945/47 | **Wald** | *Sequential Analysis* | First break from fixed-horizon testing. SPRT: optimal testing requires adaptive stopping. Connection to Peirce's economy of research is striking. |
| 1953 | **Doob** | *Stochastic Processes* | Formalized martingale theory. Bridge between Ville (1939) and Wald/Robbins. |
| 1954 | **Pólya** | *Mathematics and Plausible Reasoning* | Named patterns of plausible inference: analogy, generalization, specialization. |
| 1956 | **Robbins** | "Empirical Bayes" | Learn the prior from data across problems. The power of the sequence. |
| 1958 | **Hanson** | *Patterns of Discovery* | Rehabilitated abduction after Popper. Observation is theory-laden. Reopened the philosophical space. |
| 1965 | **Harman** | "Inference to the Best Explanation" | Coined IBE. Argued induction is a special case of abduction, inverting the traditional hierarchy. |
| 1967 | **Darling & Robbins** | "Confidence Sequences" | Confidence intervals valid at all stopping times. Width grows as √(log log n / n). Direct precursor to anytime-valid inference. |

## III. The Discovery Turn (1976–1994)

| Year | Figure | Key work | Contribution |
|------|--------|----------|--------------|
| 1976 | **Lakatos** | *Proofs and Refutations* | Mathematical knowledge grows through conjecture → counterexample → concept-revision. The "guilty lemma" names the next refinement. Closest precedent to "shape of failure names next experiment." |
| 1976 | **Lai** | "On Confidence Sequences" | Extended Darling-Robbins with mixture techniques. Bridge to modern SAVI. |
| 1977 | **Laudan** | *Progress and Its Problems* | Scientific rationality = problem-solving effectiveness, not truth-approximation. Gives a metric for methodeutic. |
| 1977/83 | **Lenat** | AM, Eurisko | Meta-abduction: system discovers new heuristics for discovering. Hit a wall from insufficient background knowledge. |
| 1983 | **Shapiro** | *Algorithmic Debugging* | Diagnosis as systematic elimination through computation tree. |
| 1985 | **Schoenfeld** | *Mathematical Problem Solving* | Expert investigation requires control knowledge — metacognitive strategies for what to try next. The human version of Kelly (1996). |
| 1987 | **Simon & Langley** | *Scientific Discovery* | BACON, DALTON, GLAUBER — AI programs that rediscovered scientific laws. First computational proof that discovery can be mechanized. |
| 1987 | **Reiter** | "Diagnosis from First Principles" | Model-based diagnosis: conflicts → hitting sets → diagnoses. Structure of failure identifies the component. |
| 1987 | **de Kleer & Williams** | "Diagnosing Multiple Faults" / GDE | Sequential diagnosis: computes which measurement maximally discriminates remaining candidates. Information-theoretic experiment selection. Closest pre-hypothesis-graph system to "shape of failure names next experiment." |
| 1988/99 | **Hintikka** | *Inquiry as Inquiry* | Interrogative model: investigation is a game between Inquirer and Nature. Next question depends on previous answers. Philosophical precursor to adaptive experimental design. Explicitly connected to Peirce's abduction. |
| 1989 | **Thagard** | "Explanatory Coherence" / ECHO | Evaluative complement to generative abduction. Competing explanations assessed by coherence constraints. |
| 1990 | **Peng & Reggia** | *Abductive Inference Models* | Parsimonious covering theory. Probabilistic formalization of Reiter's logical framework. |
| 1991 | **Bylander et al.** | "Complexity of Abduction" | Proved abduction is NP-hard in general. Explains why practical systems need heuristics and why bi-abduction's compositionality was a breakthrough. |
| 1991/04 | **Lipton** | *Inference to the Best Explanation* | Fullest philosophical treatment. Loveliest vs. likeliest distinction. Made IBE respectable for formal researchers. |
| 1993 | **Hobbs et al.** | "Interpretation as Abduction" | Weighted abduction for NLU (TACITUS). Language understanding is abductive. Extended abduction beyond diagnosis. |
| 1994 | **Josephson & Josephson** | *Abductive Inference* | Six generations of abduction machines. Connected computational abduction back to Peirce. |

## IV. Formalization (1996–2009)

| Year | Figure | Key work | Contribution |
|------|--------|----------|--------------|
| 1996 | **Kelly** | *The Logic of Reliable Inquiry* | **The key figure.** Formalized methodeutic using topological learning theory. Proved inquiry methods have convergence guarantees. Ockham's razor is necessary for cycle-optimal convergence. At CMU, same department as Ramdas. |
| 2000 | **Pearl** | *Causality* | Do-calculus: formal language for intervention. Without Pearl, hypothesis graph edges can't distinguish correlation from causation. |
| 2001 | **Shafer & Vovk** | *Probability and Finance* | Game-theoretic probability. Made Ville's 1939 betting insight into a complete foundation. |
| 2001/09 | **Magnani** | *Abductive Cognition* | Eco-cognitive model. Sentential, model-based, and manipulative abduction. Bridges philosophical and computational traditions. |
| 2009 | **Calcagno et al.** | "Bi-Abduction" (POPL) | Compositional abduction at scale (Facebook Infer). Sidesteps NP-hardness through local reasoning. |

## V. The E-Value Revolution (2019–2024)

| Year | Figure | Key work | Contribution |
|------|--------|----------|--------------|
| 2019 | **Shafer & Vovk** | *Game-Theoretic Foundations* | Full mathematical foundation for game-theoretic probability. |
| 2020 | **O'Hearn** | "Incorrectness Logic" (POPL) | Under-approximation: every reported bug carries a reachability witness. Security/uberty independently rediscovered as over- vs. under-approximate proof rules. |
| 2020 | **Wasserman, Ramdas, Balakrishnan** | "Universal Inference" | Split LRT: valid tests for any parametric model without regularity conditions. Bridge between classical and e-value methods. |
| 2021 | **Howard, Ramdas et al.** | "Confidence Sequences" | Nonparametric, finite-sample, time-uniform confidence sequences. Estimation counterpart of e-processes. |
| 2021 | **Vovk & Wang** | "E-values" (*Annals of Statistics*) | Formal definition. E-values combine by averaging under arbitrary dependence. The algebraic advantage over p-values. |
| 2021 | **Shafer** | "Testing by Betting" | Philosophical argument: replace p-values with bet outcomes. Optional continuation — always gather more data without invalidation. What Peirce's self-correcting inquiry requires. |
| 2023 | **Grünwald** (with de Heide & Koolen) | "Safe Testing" | REGROW criterion. Optimal e-values via reverse information projection. Type I error control regardless of stopping rules. |
| 2023 | **Ramdas et al.** | SAVI paper | Consolidation. Unified the four 2019 papers. Traces lineage: Ville → Wald → Robbins/Darling → Lai → Shafer-Vovk → 2019 renaissance. |
| 2024 | **Zilberstein et al.** | "Outcome Separation Logic" (POPL) | Tri-abduction: extends bi-abduction to branching programs. Abduction generalized to branching futures. |

## Key lineages

### The betting line (evidence framework)
```
de Finetti (1937) → Ville (1939) → Doob (1953) → Wald (1947)
→ Robbins/Darling (1967) → Lai (1976) → Shafer-Vovk (2001)
→ Howard/Ramdas (2021) → Vovk-Wang (2021) → Grünwald (2023)
→ Ramdas SAVI (2023)
```

### The abduction line (hypothesis generation)
```
Peirce (1878) → Hanson (1958) → Harman (1965) → Lakatos (1976)
→ Shapiro (1983) → Reiter (1987) → de Kleer (1987)
→ Josephson (1994) → Kelly (1996) → Calcagno (2009)
→ Zilberstein (2024)
```

### The discovery line (can machines investigate?)
```
Pólya (1945) → Simon/Langley (1987) → Lenat (1977/83)
→ Thagard (1989) → Josephson (1994) → Kelly (1996)
```

### The philosophical line (is there a logic of discovery?)
```
Peirce (1902) → Popper (1934, denied it) → Dewey (1938)
→ Hanson (1958) → Hintikka (1988) → Kelly (1996, proved it)
→ Lipton (2004) → Magnani (2009)
```

## The thesis in one paragraph

Peirce named abduction (1878) and methodeutic (1902) but couldn't formalize either. Popper (1934) declared formalization impossible. Dewey (1938) and Hanson (1958) kept the inquiry tradition alive philosophically. Fisher (1925) formalized induction as statistics but fixed the horizon. Wald (1947) broke the horizon with sequential analysis. Robbins (1967) gave us confidence sequences. Meanwhile, Reiter (1987) and de Kleer (1987) showed that the structure of a failure names the next experiment — mechanized abduction for engineered systems. Kelly (1996) proved that inquiry methods can converge reliably, formalizing what Peirce could only assert. Calcagno (2009) made abduction scale via compositionality. Finally, Vovk-Wang (2021) and Ramdas (2023) gave the evidence framework: e-values compose across adaptive experiments, so the kind of sequential, theory-driven investigation that methodeutics describes is now statistically valid at every stopping point. The textbook connects these threads.

## Biggest gap we discovered

**Kevin Kelly (1996)** — *The Logic of Reliable Inquiry*. Uses topological learning theory to prove convergence guarantees for inquiry methods. This is the formalization of Peirce's methodeutic that nobody in the statistics or CS community seems to know about. He's at CMU, same department as Ramdas. The connection between Kelly's convergence theory and Ramdas's e-value framework appears to be undrawn.
