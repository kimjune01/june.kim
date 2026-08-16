# Lonely Runner Conjecture — hypothesis graph

Date: 2026-08-16  
Status: open inquiry; no proof or new mathematical result claimed  
Method: [The Proof Manual](/the-proof-manual) recorded using the replay contract from [The Hypothesis Graph](/the-hypothesis-graph-semantic-memory-methodeutics)

## Target

For distinct nonzero integer speeds `v_1, ..., v_n`, prove that there is a real `t` such that

```text
||t v_i|| >= 1/(n+1)  for every i,
```

where `||x||` is the distance from `x` to the nearest integer.

The general conjecture remains open. Integer speeds suffice after normalization. The strongest recent work also reduces every fixed `n` to a finite check, but the bound remains too large for a naive search.

Sources:

- Malikiosis, Santos, and Schymura, “Linearly-exponential checking is enough for the Lonely Runner Conjecture and some of its variants”: https://doi.org/10.1017/fms.2025.10107
- Perarnau and Serra, “The Lonely Runner Conjecture turns 60”: https://arxiv.org/abs/2409.20160
- Rosenfeld, “The lonely runner conjecture holds for eight runners”: https://arxiv.org/abs/2509.14111
- Blanco, Criado, and Santos, “Coloopless zonotopes and counterexamples to the Shifted Lonely Runner Conjecture”: https://arxiv.org/abs/2603.24784

## Graph

```text
H0  original LRC is open and correctly normalized
 |
 +--H1  first-moment / union-bound proof reaches 1/(n+1)
 |    KILLED: it stops at 1/(2n)
 |       |
 |       +--H2  forced pairwise overlap closes the gap
 |              OPEN: overlap depends on arithmetic relations among speeds
 |
 +--H3  prove a phase-shifted version, then specialize
 |    KILLED: the shifted conjecture has counterexamples
 |       |
 |       +--H4  common phase is load-bearing arithmetic structure
 |              WITNESSED
 |
 +--H5  generic continuous covering methods suffice
      KILLED: they discard the common-phase/divisibility structure
         |
         +--H6  embed into a modular set-cover obstruction
                WITNESSED for the eight-runner strategy
                   |
                   +--H7  every complete bad-residue cover forces enough
                          prime divisibility to contradict the size bound
                          PARTIALLY TESTED
                             |
                             +--H8  paper's 1/(k-1) cover threshold is usable
                             |       KILLED: contradicts a published fixture
                             |
                             +--H9  corrected finite predicate becomes UNSAT
                                     for large enough p at k=8
                                     WITNESSED for p=47,53,59,61,67 only
```

## Nodes

### H0 — The selected target is genuinely open

- Mode: induction from current literature
- Hypothesis: the general Lonely Runner Conjecture remains unresolved as of 2026-08-16, while fixed small cases and finite-checking reductions are known.
- Kill condition: a dated primary source proves or disproves the general formulation.
- Trial: inspect the current survey and the 2025–2026 papers listed under Sources; compare their theorem statements with the target above.
- Observed outcome: the survey calls the general problem open; subsequent papers prove bounded-runner cases, finite reduction, or disprove shifted variants, not the original general conjecture.
- Verdict: witnessed at artifact-replay grade.
- Credence: high, capped below certainty because literature status can change.

### H1 — A first-moment argument proves the conjectured threshold

- Mode: deduction
- Hypothesis: viewing time `t` as uniform on `[0,1)` and bounding bad times by measure proves the threshold `1/(n+1)`.
- Kill condition: the total bad-set measure bound is at least `1` at that threshold.
- Trial:

  ```text
  Let B_i(delta) = {t in [0,1): ||v_i t|| < delta}.
  Multiplication by nonzero integer v_i preserves uniform measure mod 1,
  so mu(B_i(delta)) = 2 delta.
  Therefore mu(union_i B_i(delta)) <= 2 n delta.
  Substitute delta = 1/(n+1): 2n/(n+1) > 1 for n > 1.
  ```

- Observed outcome: the bound proves only `delta < 1/(2n)`; it cannot reach `1/(n+1)`.
- Verdict: killed at strong-replay grade.
- Credence: deductive.
- Edge generated: H2. The exact deficit says the next proof must exploit overlap among the bad sets rather than their individual measures.

### H2 — Arithmetic overlap among bad sets closes the factor-two gap

- Mode: abduction
- Hypothesis: inclusion–exclusion, Fourier coefficients, or another correlation argument can show that the periodic bad sets overlap enough to leave an uncovered time at `delta = 1/(n+1)`.
- Kill condition: construct normalized speed families whose overlap statistics obey no uniform inequality stronger than the first-moment bound, or show that the required inequality implies a known false shifted statement.
- Trial: derive or retrieve a lower bound on intersections `mu(B_i intersect B_j)` that survives all distinct normalized integer speed vectors and is strong enough, after inclusion–exclusion, to force `mu(union_i B_i) < 1`.
- Observed outcome: not run to completion. Pairwise overlap depends on gcd and ratio structure; no uniform bound was established in this inquiry.
- Verdict: open.
- Credence: low; proposed, not tested.
- Edge if killed by uncontrolled higher-order dependence: move from global inclusion–exclusion to residue-class decomposition and H6.

### H3 — Prove the independently phase-shifted statement

- Mode: abduction
- Hypothesis: the proof should survive replacing each constraint by `||v_i t + s_i|| >= 1/(n+1)` for arbitrary phases `s_i`; the original follows by setting every `s_i = 0`.
- Kill condition: one counterexample to the shifted formulation.
- Trial: inspect the theorem statements and explicit constructions in Blanco, Criado, and Santos (2026), arXiv:2603.24784.
- Observed outcome: explicit counterexamples exist to the shifted Lonely Runner Conjecture starting at `n = 5`.
- Verdict: killed at artifact-replay grade.
- Credence: high.
- Edge generated: H4. The common phase in the original problem is load-bearing and must remain visible in any embedding.

### H4 — Common phase is load-bearing structure

- Mode: induction
- Hypothesis: a viable proof must use the fact that all bad intervals are centered on the common arithmetic condition `v_i t in Z`, rather than treating them as arbitrary periodic arcs.
- Kill condition: prove the original statement using only properties invariant under independent translations of the bad sets.
- Trial: compare the original and shifted formulations. Any argument invariant under independent translations would prove both; H3 records counterexamples to the shifted form.
- Observed outcome: translation-invariant information cannot suffice.
- Verdict: witnessed at strong-replay grade, conditional on the cited shifted counterexamples.
- Credence: deductive from H3.
- Edge generated: preserve congruence, gcd, and divisibility data in the next representation.

### H5 — Generic continuous covering machinery is sufficient

- Mode: abduction
- Hypothesis: compactness, convexity, or generic circle-covering bounds prove the target without arithmetic information about the speeds.
- Kill condition: the proposed machinery is invariant under independent phase shifts or sees only interval lengths.
- Trial: erase the centers of the sets `B_i` and retain only their measures and periodicity. Check whether the resulting data distinguishes the original formulation from H3's false shifted formulation.
- Observed outcome: it does not distinguish them.
- Verdict: killed as a standalone route; continuous tools may still participate after an arithmetic embedding.
- Credence: moderate.
- Edge generated: H6, embed the obstruction into modular residues while preserving common phase.

### H6 — Modular set cover exposes a finite obstruction

- Mode: induction from a published construction
- Hypothesis: for suitable rational test times, failure of loneliness becomes a finite set-cover problem whose complete covers force divisibility constraints on a minimal counterexample.
- Kill condition: the discretization loses a possible real-time witness, or the cover certificate has no implication for the integer speeds.
- Trial: replay the reformulation in Rosenfeld (2025), especially the bad-residue cover and prime-divisibility lemmas used for eight runners; compare it with the finite-checking theorem of Malikiosis, Schymura, and Santos.
- Observed outcome: this route yields a computer-assisted proof for eight runners by forcing enough primes to divide the product of the speeds to contradict an independent upper bound.
- Verdict: witnessed for the bounded case at artifact-replay grade; not established uniformly in `n`.
- Credence: high for the cited case, low for generalization.
- Edge generated: H7.

### H7 — Complete residue covers force enough divisibility uniformly

- Mode: abduction
- Hypothesis: for every `n`, sufficiently many moduli `p` have the property that a complete bad-residue cover forces `p | product_i v_i`, or a stronger condition such as multiple divisible speeds or a forced prime power. The accumulated divisibility then exceeds the finite-checking upper bound for a minimal counterexample.
- Kill condition: exhibit arbitrarily large `n` and admissible complete covers avoiding enough independent prime divisors, or prove that the forced-prime product grows too slowly relative to the minimal-counterexample bound.
- Trial:

  1. Formalize Rosenfeld’s constrained set-cover predicate for symbolic `n` and modulus `p`.
  2. Enumerate small `(n,p)` instances with a certificate-producing SAT or exact-cover solver.
  3. Classify failures by their residue and gcd structure.
  4. Test candidate strengthenings: prime powers, at least two speeds divisible by `p`, or interacting moduli.
  5. Compare the certified divisor-product lower bound against the published upper bound on a minimal counterexample.

- Observed outcome: not run. This is the surviving frontier, not a result.
- Verdict: open.
- Credence: low.

### H8 — The printed `1/(k-1)` coverage threshold is the intended predicate

- Mode: deduction plus differential replay
- Hypothesis: Section 6 of Rosenfeld’s source can be implemented literally: `v` covers `j` when `||jv/((k+1)p)|| < 1/(k-1)`.
- Kill condition: the literal predicate produces an admissible cover for a `(k,p)` pair the same paper reports as having no cover.
- Trial:

  ```text
  uv run --with pytest --with z3-solver pytest -q drafts/test_lonely_runner_h7.py

  For k=3, p=7, D=28, test the candidate {1,2,3} at threshold 1/(k-1)=1/2.
  It covers every j in {1,...,14}; for each omitted candidate,
  gcd(28, the other two candidates)=1.
  ```

- Observed outcome: `{1,2,3}` is an admissible complete cover under `1/(k-1)`, but the paper reports that the required no-cover property holds for `k=3` and every prime `p >= 7`. The main lemma itself uses the lonely threshold `1/(k+1)`.
- Verdict: killed at strong-replay grade. The experiment therefore uses `1/(k+1)`. This appears to be a typographical error in the paper’s cover definition; it is not a defect in the main lemma.
- Credence: high.
- Edge generated: H9. Validate the corrected formalization against both a published working case and a published exception before exploring new instances.

### H9 — The corrected finite predicate becomes UNSAT for larger moduli at `k=8`

- Mode: induction from finite exact experiments
- Hypothesis: with nine runners (`k=8` nonzero relative speeds), admissible complete covers disappear once `p` is sufficiently large.
- Kill condition: find admissible complete covers for arbitrarily larger tested primes, or fail to reproduce the published lower-`k` fixtures.
- Trial implementation: `drafts/lonely_runner_h7.py`, tested by `drafts/test_lonely_runner_h7.py` under Python 3.13 and Z3 5.1.0.
- Encoding:

  - one Boolean variable per candidate residue in `1,...,floor((k+1)p/2)`, excluding multiples of `p`;
  - exactly `k` selected residues;
  - one coverage clause per rational test time;
  - for every prime `q | (k+1)p`, at least two selected residues are nonzero modulo `q`. This is equivalent to `gcd(D, all selected residues except any one)=1`.

- Calibration outcome:

  - `k=3,p=7`: UNSAT, matching a published working modulus;
  - `k=6,p=17`: SAT, matching a published exception;
  - `k=6,p=17` witness is replayed by the test suite.

- New finite outcomes for `k=8`:

  | p | Verdict | Replay artifact |
  |---:|:---|:---|
  | 11 | SAT | `(1,3,4,5,6,7,9,43)` |
  | 13 | SAT | `(1,3,4,5,6,9,15,21)` |
  | 17 | SAT | `(1,9,22,38,40,49,58,71)` |
  | 19 | SAT | `(1,5,6,7,9,45,54,72)` |
  | 23 | SAT | `(1,7,9,27,36,45,54,63)` |
  | 29 | SAT | `(1,8,9,18,27,45,72,99)` |
  | 31 | SAT | `(1,7,9,45,54,72,81,126)` |
  | 37 | SAT | `(1,8,9,27,36,45,63,117)` |
  | 41 | SAT | `(1,7,9,45,54,63,72,99)` |
  | 43 | SAT | `(1,7,9,45,54,63,72,117)` |
  | 47 | UNSAT | deterministic Z3 replay, 25.885 s in the recorded run |
  | 53 | UNSAT | deterministic Z3 replay |
  | 59 | UNSAT | deterministic Z3 replay |
  | 61 | UNSAT | deterministic Z3 replay |
  | 67 | UNSAT | deterministic Z3 replay, 25.154 s in the recorded run |

- Observed outcome: a sharp tested transition occurs between `p=43` and `p=47`. Every tested prime through `43` admits a cover; every completed test from `47` through `67` is UNSAT.
- Verdict: witnessed only for the listed finite instances. SAT rows have compact independently replayable witnesses. UNSAT rows currently have deterministic solver replay but no exported proof certificate, so their replay grade is weaker.
- Credence: high for SAT witnesses; moderate-high for UNSAT runs; low for extrapolation to all `p >= 47`.
- Edge generated: H10 — export checkable UNSAT certificates and search for the structural reason the transition occurs at `47`.

### H10 — A structural obstruction explains the `k=8` transition

- Mode: abduction
- Hypothesis: for `k=8`, every admissible complete cover at sufficiently large `p` violates either a coverage clause or the “two nonmultiples per prime divisor” gcd condition for a small, classifiable family of residues.
- Kill condition: UNSAT cores vary without a stable residue/gcd pattern across larger primes, or SAT witnesses reappear.
- Trial:

  1. Label every coverage and gcd clause and extract UNSAT cores for `p=47,53,59,61,67`.
  2. Minimize the cores and normalize them under `v -> D-v` and multiplication by units modulo `D`.
  3. Intersect the normalized cores across moduli.
  4. Attempt to state the shared core as a symbolic counting or divisibility lemma.
  5. Export an independently checkable proof certificate for each finite UNSAT result.

- Observed outcome: not run.
- Verdict: open frontier.
- Credence: low.

## What the graph established

1. The elementary measure branch recovers `1/(2n)` and dies by an exact factor-two deficit.
2. The failure generates a concrete need: control overlap, not individual bad-set size.
3. The tempting shifted generalization is false; common-phase arithmetic is therefore load-bearing.
4. A generic covering proof cannot work alone if it forgets that arithmetic.
5. The strongest surviving branch is a modular set-cover certificate that converts coverage into divisibility.
6. The printed set-cover threshold fails differential replay; `1/(k+1)` matches the lemma and published fixtures.
7. At `k=8`, the corrected finite predicate is SAT through `p=43` and UNSAT for the completed tests `p=47,53,59,61,67`.
8. The next falsifiable research node is H10. No general theorem or new Lonely Runner case was proved.

## Frontier

- Primary: extract and compare UNSAT cores for the tested `k=8` moduli, then export proof certificates.
- Secondary: extend the prime scan beyond `67`, with explicit timeouts recorded as `unknown`, never as `UNSAT`.
- Secondary: return to H2 only with an overlap inequality that explicitly depends on gcd/ratio data and therefore respects H4.
- Pruned: first-moment-only proofs, independently shifted formulations, and embeddings that retain only interval lengths.
