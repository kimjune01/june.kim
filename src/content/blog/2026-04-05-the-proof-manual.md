---
variant: post-medium
title: "The Proof Manual"
tags: methodology, epistemology
---

For agents: load [`proof-manual.yml`](https://github.com/kimjune01/june.kim/blob/master/src/data/proof-manual.yml).

---

You have a conjecture. You try induction. It doesn't work. Now what?

Most people try induction again, harder. [Schoenfeld (1985)](https://www.cambridge.org/core/books/mathematical-problem-solving/71E357D32C51F5B4BB279C244ACA6E2F) filmed this: one technique, ridden to exhaustion, consuming the entire session. He called it the wild goose chase. Novices and experts know the same techniques. The difference is control — knowing when to switch and what to switch to.

He never specified *what*. This manual does. It doesn't prove your theory right. It makes it faster for it to be wrong.

## The procedure

1. Revalidate the problem's status against dated primary sources. Repeat this before claiming novelty; “open” is not stable metadata.
2. Formalize the claim and its quantifier order. Decide what would count as a witness, bound, construction, or impossibility; then let later-bound objects depend adversarially on every earlier choice.
3. Decompose it into lemmas. Separate the structural problem from the local calculations.
4. Classify each lemma by claim and domain, then look up candidates in the [grid](/data/proof-manual.yml). Scan the whole row, not just your first instinct.
5. Retrieve analogues. Look for the same shape in another theorem or domain.
6. Check kill conditions and symmetries. Cross off the dead techniques before you start.
7. Try the survivors in parallel when you can. Verify each step, not just the conclusion, and record the verification grade.
8. Diagnose the failures. Repair the statement, invent a missing lemma, change domains, or escalate to the technique the failure names.
9. Repeat until the proof closes or the conjecture breaks.

This is the proof loop:

```
status → formalize → decompose → retrieve → generate → search
  ↑                                                   ↓
  └────────── mutate ← diagnose ← verify ─────────────┘
```

A stale status check can waste the whole loop: a proof may have appeared after problem selection, or a newer theorem may make the chosen route obsolete. Record the query date, theorem statement, and primary source—not just “believed open.” Literature discovery is not a new proof, but failing to do it can turn genuine proof search into accidental reproduction.

Quantifier order deserves the same treatment. To test (\(\exists D\,\forall d\ge D\,\forall v\)), choose (\(v\)) *after* seeing (\(d\)); never test only a fixed collection of (\(v\)) while increasing the grid. Uniform discretization claims are especially vulnerable because the object can scale with the denominator and hide between every sampled point.

Then audit the conclusion for operational content. “There exists a relation permitting descent” is not a lemma until the permitted transformation and its preserved invariant are stated. If the bare relation exists for every object in the domain, the adjective is carrying the entire proof and the hypothesis cannot yet be tested.

The techniques are old. What changed is how quickly a mathematician—or an agent—can generate, reject, repair, and recombine them. Control is no longer just knowing what to try next. It is managing the loop.

## Verification has levels

“The solver says UNSAT” is not the same result as a proof a stranger can check.

| Grade | What you have | What can still fail |
|---|---|---|
| Witness | An explicit construction or counterexample | It may not match the intended statement |
| Verdict | A solver returns SAT / UNSAT | Tool bugs, encoding errors, irreproducible state |
| Replay | A pinned command reproduces the verdict | The same tool may repeat the same mistake |
| Certificate | An independent checker verifies a proof artifact | The formal statement may still be wrong |
| Semantic match | A human checks formal statement against intended claim | Nothing mechanical closes this gap |

Verification also perturbs the search. Proof logging, named clauses, and assumption tracking can make a terminating solve time out. That timeout is not evidence against the claim; it is an instrumentation failure. Record it as `unknown`, then change the verifier or reduce the instance. Never compress `unknown` into `false`.

A certificate verifies the formula it receives, including any symmetry breaks, cuts, or derived clauses—not the claim that those strengthenings are sound. Record a proof that each added constraint preserves every hypothetical counterexample. Otherwise a perfectly checked `UNSAT` result may certify only an accidentally stronger problem.

## Kill conditions

The part nobody writes down.

| Technique | Kill condition | Escalate to |
|---|---|---|
| Induction | Residual loses structure | Potential method |
| Contradiction | ¬P doesn't interact with structure | Direct construction |
| Greedy | Local progress destroys substructure | Potential method |
| Pigeonhole | Same-size sets, need witness not existence | Probabilistic method |
| Probabilistic method | E[X]<1, or dependencies, or need witness | Second moment → LLL → derandomization |
| Spectral | Semiring without eigenvalues | Embed-solve-pullback |
| IVT / fixed point | Discrete or non-compact domain | Sperner, simplicial Brouwer |
| Invariant | No separating invariant visible | Reduction |
| Potential method | No monotone potential | Game equilibrium |
| Diagonalization | Uncountable candidates | Reduction |
| Solver verdict | No independently checkable certificate | Proof-producing solver → independent checker |
| Proof logging | Instrumented search no longer terminates | Reduce instance → export certificate |
| Strengthened encoding | Symmetry break or derived clause lacks a preservation proof | Prove implication → certify augmented formula |
| Moment / spectral summary | Same summary, different target behavior | Higher-order structure → exact representation |
| Uniform discretization | The object may scale with the chosen grid | Height-sensitive bound → fixed-object compactness |
| Structural certificate | The certificate is automatic; an adjective hides the missing step | Define the transformation → prove invariant preservation |

The kill at step N names the technique at step N+1.

## Symmetry mismatch

If your problem lacks a symmetry your technique assumes, the technique produces a valid-looking argument with a hidden gap.

| You assume | It's actually | What dies |
|---|---|---|
| Undirected | Directed | Union-find, spanning trees |
| Transitive | Non-transitive | Reachability composition |
| Time-independent | Time-dependent | Static data structures |
| Commutative | Non-commutative | Abelian group tools |
| Local | Global | Heuristics, distributed algorithms |
| Linear | Nonlinear | Superposition, spectral decomposition |

## Embed-solve-pullback

When nothing in your domain works, change the domain.

| Source → Target | What you gain | What you risk |
|---|---|---|
| Combinatorics → 3-SAT | Exponential search | Clause structure artificial |
| Discrete → Geometry | Convexity, separation | Rounding loses feasibility |
| Nonlinear → Linear (LP/SDP) | Poly-time solvers | Integrality gap |
| Time domain → Frequency | Convolution → multiplication | Localization lost |
| Graph → Algebra (spectral) | Eigenvalue bounds | Semiring has no spectral theory |

The risk is always the same: the pullback doesn't preserve the constraints.

## The lineage

Every technique exists because its parent died on a specific problem:

```
Exhaustion (Archimedes)
  kill: can't handle infinite processes
  └→ Limits (Cauchy, Weierstrass)
     kill: need compactness for existence
     └→ Compactness arguments (Bolzano-Weierstrass)
        kill: need topology beyond R^n
        └→ General topology

Counting (Euler)
  kill: exact counts intractable
  └→ Generating functions
     kill: coefficients hard to extract
     └→ Analytic combinatorics (Flajolet)
        kill: need asymptotics not exact
        └→ Probabilistic method (Erdős, Alon & Spencer)

Diagonalization (Cantor)
  kill: need self-reference formalized
  └→ Incompleteness (Gödel)
     kill: need computation model
     └→ Undecidability (Turing)
        kill: need quantitative hardness
        └→ Complexity lower bounds (Cook, Karp)
```

A student who only knows induction will never try a potential method. One who knows potential methods exist *because* induction kills residual structure will reach for the right tool.

## Why it works

Every proof decomposes into compositions of six [type constructors](https://leanprover.github.io/theorem_proving_in_lean4/dependent_type_theory.html):

| Constructor | What it proves |
|---|---|
| Π (dependent function) | ∀, implication |
| Σ (dependent pair) | ∃, witness |
| Inductive type | Recursion, cases |
| Match | Case analysis, induction |
| Quotient | Equivalence |
| Truncation | Non-constructive existence |

The grid's rows map to these: existence = Σ, impossibility = Π→False, construction = Σ with computability. This explains the target shape, but not the whole search. A failed proof may be a type error; it may also be a missing lemma, an unproductive decomposition, a bad formalization, or a search budget spent in the wrong branch. Lean can reject an invalid proof term. It cannot tell you whether you stated the right theorem or searched the right neighborhood.

That distinction matters more now that proof generation is abundant. Verification answers *is this derivation valid?* The manual answers *what should we try, what did the failure teach us, and how should we change the search?*

Pick your stuck conjecture. Run the procedure. If the manual doesn't surface a technique you haven't tried, it's incomplete — [tell me what's missing](https://github.com/kimjune01/june.kim/blob/master/src/data/proof-manual.yml).

---

*Inspired by [The Parts Bin](/the-parts-bin).*
