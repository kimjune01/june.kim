# From a p=47 obstruction to the nine-runner theorem

Status: research draft, 2026-08-16. The local p=47 result below is one independently checked obstruction. A later literature recheck found that the nine-runner case had already been proved twice in late 2025. I subsequently replayed the complete 39-prime sieve from Trakulthongchai's proof. This is a reconstruction of a known theorem, **not** a novelty claim or a proof of the general Lonely Runner Conjecture.

## Correction before the mathematics

I selected nine runners as an open target from stale context. It was not open. Trakulthongchai announced proofs for nine and ten runners in November 2025; Rosenfeld independently announced a different nine-runner proof days later. Both have revised 2026 manuscripts. The mistake is methodological, not cosmetic: problem status is a time-dependent premise and must be rechecked against dated primary sources before a novelty claim.

The attempted proof search was still useful. Its p=47 certificate independently cross-checks the boundary mechanism, and its first fourteen prime obstructions agree with the published sieve. But “I reproduced part of the proof before finding it” is not “I solved an open problem.”

## Result

Let (D=9cdot47=423). There is no set of eight distinct residues

\[
S\subseteq \{1,\ldots,211\}\setminus47\mathbb Z
\]

such that

1. deleting any one element leaves a set whose gcd with (423) is (1); and
2. for every (j\in\{1,\ldots,211\}), some (v\in S) satisfies

\[
\left\|\frac{jv}{423}\right\|<\frac19.
\]

This verifies the (k=8,p=47) instance of Rosenfeld's finite obstruction. Assuming the already-established eight-runner case, Rosenfeld's prime-divisor lemma then implies:

> If a nine-runner counterexample exists, (47) divides the product of its eight relative speeds.

It does not say which speed is divisible by (47), and it does not rule out a counterexample by itself.

## Reduction

The candidates are not divisible by (47), so the deletion-gcd condition has only one active prime: (3). It is equivalent to requiring at least two selected speeds not divisible by (3).

Classify each speed by (g=\gcd(v,9)\in\{1,3,9\}), and write (u,t,h) for the number in each class. The special test time (j=47) is covered exactly when (9\mid v), so (h\ge1). The gcd condition gives (u\ge2). Hence only (u=2,\ldots,7) require examination.

Multiplication by a unit modulo (423) permutes the test times and preserves coverage, distinctness, and gcd classes. We may therefore normalize one selected unit speed to (1).

## The nine-phase fibers

Write a full residue as (j=r+a47), where (r\in\mathbb Z/47\mathbb Z) and (a\in\mathbb Z/9\mathbb Z). On each fiber:

- (g=1): a speed covers two phases when (r\ne0), and one phase when (r=0). The phase difference is (\pm v^{-1}\pmod9).
- (g=3): a speed covers either no phase or one complete congruence class modulo (3).
- (g=9): a speed covers either all nine phases or none.

These patterns retain the overlap information lost by marginal counts, pair intersections, and single Fourier characters.

## Exhaustion by unit count

| Unit count | Method | Outcome | Verification grade |
|---:|---|---|---|
| (u=2) | Necessary three-phase fiber CNF | UNSAT | DRUP independently verified by `drat-trim` |
| (u=3) | Exact normalized CNF plus proved phase-1 clause | UNSAT | DRUP independently verified by `drat-trim` |
| (u=4) | 208,104 phase-feasible nonunit choices + exact completion | no completion | exhaustive replay |
| (u=5) | 37,214 nonunit triples + exact completion | no completion | exhaustive replay |
| (u=6) | 1,311 nonunit pairs + exact completion | no completion | exhaustive replay |
| (u=7) | 23 nonunit choices + exact completion | no completion | exhaustive replay |

The high-unit verifier uses fixed-size bitsets, an incidence-capacity bound, and a packing bound from uncovered points with pairwise-disjoint sets of possible covering speeds. Every pruning rule is one-sided: it only rejects a state when the remaining slots provably cannot cover the residual set.

The source, tests, compressed CNFs, DRUP proofs, checksums, and replay commands live in `/Users/junekim/Documents/lonely-runner`.

## Semantic scope

The DRUP checker proves the augmented CNFs inconsistent. Separate mathematical arguments are still required for the augmentations:

- the corrected bad-time threshold is (1/(k+1)=1/9);
- the gcd condition reduces to (u\ge2);
- unit normalization preserves all hypothetical covers;
- (j=p) forces (h\ge1);
- the fiber clauses used in the (u=2,3,4) branches are necessary.

Each implication is recorded in the hypothesis graph and replayed where finite. The cover definition printed as (1/(k-1)) in the implementation section of the available Rosenfeld source conflicts with the preceding lemma and its claimed equivalence; (1/(k+1)) is the threshold used here.

## Resolution of the nine-runner case

The explicit minimal-counterexample product bound is

\[
B=\left(\frac{36^7}{8}\right)^8
=84765698874878218361067180729674171436543015292348049288994557831877912686493696.
\]

Trakulthongchai's proof makes the required computation tractable by lifting improper covers through moduli (p), (3p), and (9p). I replayed the author's unmodified verifier for the 39-prime set

```text
47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227,
229, 233, 239, 241
```

For every prime, the final improper set was empty and all intermediate cardinalities matched the published receipt. Hence every hypothetical counterexample's speed product is divisible by

\[
\prod_{p\in S}p
=19570880530831227159611114469289180443865177656785618176063821114999202895619850591,
\]

which is about (230.882) times larger than (B). The finite-checking bound and prime-divisor lemma therefore contradict the existence of a minimal counterexample. This reconstructs the published proof that the Lonely Runner Conjecture holds for nine runners.

The complete local audit—including the pinned source commit, hashes, 39 intermediate rows, exact arithmetic test, and trust boundary—is in `/Users/junekim/Documents/lonely-runner/artifacts/nine-runner-sieve-audit.md`. The computation is independent replay, not a proof-producing certificate. Rosenfeld's separate prime-power proof provides corroboration through a materially different refinement.

## References

- Hugo Rosenfeld, [*The lonely runner conjecture holds for eight runners*](https://arxiv.org/abs/2509.14111), 2025.
- Tanupat Trakulthongchai, [*Nine and ten lonely runners*](https://arxiv.org/abs/2511.22427), revised 2026.
- Matthieu Rosenfeld, [*The lonely runner conjecture holds for nine runners*](https://arxiv.org/abs/2512.01912), revised 2026.
- Perarnau and Serra, [*The Lonely Runner Conjecture turns 60*](https://arxiv.org/abs/2409.20160), 2024.
- Malikiosis, Santos, and Schymura, [*Linearly-exponential checking is enough for the Lonely Runner Conjecture and some of its variants*](https://doi.org/10.1017/fms.2025.10107), 2025.
