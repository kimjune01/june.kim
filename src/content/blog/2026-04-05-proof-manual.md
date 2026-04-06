---
variant: post
title: "The Proof Manual"
tags: methodology, cognition
---

# The Proof Manual

**For agents:** load [`proof-manual.yml`](/data/proof-manual.yml).

---

You have a conjecture. You try induction. It doesn't work. Now what?

Most people try induction again, harder. [Schoenfeld (1985)](https://www.cambridge.org/core/books/mathematical-problem-solving/71E357D32C51F5B4BB279C244ACA6E2F) filmed this: one technique, ridden to exhaustion, consuming the entire session. He called it the wild goose chase. Novices and experts know the same techniques. The difference is **control** — knowing when to switch and what to switch to.

He never specified *what*. This manual does. It doesn't prove your theory right. It makes it faster for it to be wrong.

## The procedure

1. **Classify.** What are you proving? (Existence, uniqueness, upper bound, lower bound, impossibility, construction, equivalence.) What domain? (Discrete, continuous, algebraic, geometric, probabilistic.)
2. **Look up.** The [grid](/data/proof-manual.yml) gives candidates for your cell. Scan the row — not just your first instinct.
3. **Check kill conditions.** For each candidate, check whether its failure modes apply to your problem. Cross off the dead ones *before you start*.
4. **Check symmetries.** Does your problem lack a symmetry the technique assumes? If yes, the technique fails silently — the argument looks right but has a hidden gap.
5. **Try the survivors.** Work the top candidate. When it dies, the failure mode names the next one.

That's it. The rest of this post is the reference material for each step.

## Kill conditions

Every proof technique has characteristic failure modes. They're the part nobody writes down.

**Induction.** Kills: residual loses structure. Subproblem isn't the same type as the original. → Try **potential method**.

**Contradiction.** Kills: the negation doesn't interact with the structure. You assume ¬P and nothing useful follows. → Try **direct construction**.

**Greedy.** Kills: each step constrains future steps. Local progress destroys substructure. �� Try **potential method**.

**Pigeonhole.** Kills: objects and containers are the same size. Assignment isn't well-defined. You get existence but needed construction. → Try **probabilistic method**.

**Probabilistic method.** Kills: expected count < 1 → try **second moment**. Dependencies too strong → try **Lovász local lemma**. Need explicit witness → try **derandomization**.

**Spectral.** Kills: algebra doesn't support eigenvalues (tropical semiring, non-commutative ring). Relevant quantity isn't spectral. → Try **embed-solve-pullback** into a domain with spectral theory.

**IVT / fixed point.** Kills: discrete domain. Non-compact domain. Discontinuous function. → Try **combinatorial** analogs (Sperner, Brouwer via simplicial).

**Invariant.** Kills: no invariant separates achievable from unachievable. If you don't see it quickly, it's not there. → Try **reduction**.

**Potential method.** Kills: dynamics aren't monotone. Decrease per step too small. → Try **game equilibrium**.

**Diagonalization.** Kills: candidate space uncountable. Defeat function not computable. → Try **reduction**.

Each arrow (→) is a step on the **escalation ladder**: the kill condition at step N names the technique at step N+1.

## Symmetry mismatch

The silent killer. If your problem lacks a symmetry your technique assumes, the technique produces a valid-looking argument with a hidden gap.

| You assume | It's actually | What dies |
|---|---|---|
| Undirected | Directed | Union-find, spanning trees |
| Transitive | Non-transitive | Reachability composition |
| Time-independent | Time-dependent | Static data structures |
| Commutative | Non-commutative | Abelian group tools |
| Local | Global | Heuristics, distributed algorithms |
| Linear | Nonlinear | Superposition, spectral decomposition |

Check symmetries before picking a technique.

## Embed-solve-pullback

When nothing in your domain works, change the domain. Map the problem somewhere with stronger tools, solve it there, pull back.

| Source → Target | What you gain | What you risk |
|---|---|---|
| Combinatorics → 3-SAT | Exponential search | Clause structure artificial |
| Discrete → Geometry | Convexity, separation | Rounding loses feasibility |
| Nonlinear → Linear (LP/SDP) | Poly-time solvers | Integrality gap |
| Time domain → Frequency | Convolution → multiplication | Localization lost |
| Graph → Algebra (spectral) | Eigenvalue bounds | Semiring has no spectral theory |

The risk is always the same: **the pullback doesn't preserve the constraints.**

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

A student who only knows induction will never try a potential method. A student who knows potential methods were invented *because* induction kills residual structure will reach for the right tool.

## Why it works

Every proof decomposes into compositions of six [type constructors](https://leanprover.github.io/theorem_proving_in_lean4/dependent_type_theory.html):

| Constructor | What it proves |
|---|---|
| **Π** (dependent function) | ∀, implication |
| **Σ** (dependent pair) | ∃, witness |
| **Inductive type** | Recursion, cases |
| **Match** | Case analysis, induction |
| **Quotient** | Equivalence |
| **Truncation** | Non-constructive existence |

The grid's rows map to these: existence = Σ, impossibility = Π→False, construction = Σ with computability. The techniques in each cell are canonical ways to build that type. The kill conditions are type errors — your proof term doesn't inhabit the target type.

This is what happens when you formalize in Lean. The type checker rejects your proof for the exact reasons the kill conditions predict. The manual is a type checker for proof strategy, run by a human instead of a compiler.
