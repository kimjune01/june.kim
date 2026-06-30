# Plan: impossibility classification of ProgramBench (201 tasks)

## Goal
Tag each of the 201 tasks with the infeasibility criteria it trips, under the verified setting, and produce a determinacy-style two-tier result: a CLAIMABLE SPINE (mechanical + intrinsic, needs no hidden-test bodies) and a HYPOTHESIS TIER (coverage-dependent or rater-needed). Report an un-benchable denominator with a per-task receipt.

## Verified setting (the constraints a solver actually faces)
- Execute-only reference binary: can run it and observe stdout/stderr/exit/output-files; cannot read/disassemble/instrument it.
- Bundled usage docs only (README/man at the pinned commit). No internet; no package installs (DNS blackholed at build, verified in internet_control.py).
- Base: ubuntu:22.04 + Rust/Python/Go stdlibs + build-essential + cmake. So the only available libraries are stdlib + base `.so`; nothing installable.
- Budget ~6h / 1000 steps. Grading is CONJUNCTIVE (pass ALL hidden behavioral tests). Comparator is strict (their linter rejects short-substring matches, §2.2).

## Governing rule: the three-way property
Infeasibility = f(reference behavior, bundled docs/env, hidden-test coverage + comparator). It is NOT a property of the program alone. So we CLAIM a criterion for a task only when it is INTRINSIC: the program's core function IS the infeasible surface, so any behavioral test necessarily exercises it (no test bodies needed). Otherwise the criterion is COVERAGE-DEPENDENT and filed as a hypothesis (needs the hidden-test bodies or a rater), counted in NO claimable rate. This is the screen-vs-spine discipline.

"impossible" throughout = infeasible with classical computing in the foreseeable future (not undecidable).

## Criteria

### Claimable spine (mechanical + can be intrinsic)
- **C1 Unavailable irreducible artifact.** Core function is a codec/hash/cipher/compressor/wire-protocol (algorithm) OR a large external data-table (Unicode/timezone/MIME/dictionary/registry) that is absent from stdlib/base and not installable offline, hence recall-only.
  - Mechanical check: program function (from the paper's per-task descriptions) + an offline-availability lookup (is the algorithm/table in Go/Python/Rust stdlib or a base `.so`?).
  - Intrinsic when: the artifact IS the program's reason for existing (the tool's whole job is the codec/hash/table). Then every behavioral test exercises it.
- **C2 Scale beyond budget (search argument).** Reconstruction is a search over implementations; conjunctive grading requires matching the WHOLE graded behavioral surface; the budget bounds how much surface an agent can write-and-verify. Infeasible when the surface's joint specification (count of independent graded behaviors, option x grammar breadth, minimal-reimplementation complexity) exceeds what the budget can fit. Framed as the same search/counting argument as the input case: too many independent decisions to get all right within the step budget, and one miss forfeits the task.
  - Mechanical check: surface-size estimate = graded-test count (tests.json) + distinct subcommands/options + grammar indicators, compared to a budget model (steps available / cost-per-behavior).
  - Intrinsic: conjunctive metric demands the full surface, so this is a property of the task, not coverage.
- **C3 Reference non-determinism (unexposed source).** Output is not a function of visible input (RNG/timestamps/hash-order/addresses) and the seed/order is source-only, so "match the reference" pins an arbitrary trace.
  - Mechanical check: run the reference twice on identical input+env; divergence => tag; confirm no exposed seed/order flag in docs.
  - Intrinsic when a graded behavior depends on it (signal: test names seed/reproducible/random/order).

### Hypothesis tier (coverage-dependent or rater-needed)
- H4 exact-diagnostics oracle (byte-exact stderr/exit on invalid input)
- H5 canonicalization ambiguity (reference's chosen representative among equivalent outputs)
- H6 stateful/temporal (cache/journal/migration/crash-recovery)
- H7 environment coupling (TZ/LANG/COLUMNS/locale/tty) — mechanically perturb-and-compare; infeasibility depends on runner env pinning
- H8 frozen-accident / bug-compat
- H9 location uncertainty (sparse unsignposted value-space behaviors)
- H10 cross-version ambiguity (docs name the tool, not the version/flags)
- H11 platform/runtime exactness (float/libm/locale/regex-engine/errno/buffering)
- H12 query cost (expensive probes exhaust the budget)

## Tagging procedure
- Stage A (mechanical, from metadata, no binaries): program function/category from the paper's per-task descriptions -> C1 artifact category via an offline-availability table; behavioral-surface size from tests.json + options/grammar -> C2; test-name signals for C3/H4/H5/H6/H7.
- Stage B (needs reference binaries; pull task docker images if available via the repo's blob_store/publish, else fall back to test-name signals as hypothesis): C3 run-twice; H7 env-perturbation; H12 query-cost.
- Stage C (verdict): un-benchable (claimable) if >=1 spine criterion (C1-C3) is INTRINSIC for the task; record criterion + receipt. Coverage-dependent hits -> hypothesis flags only.

## Output
Per-task table {program, core-fn, offline-availability, spine-criteria, hypothesis-flags, verdict, receipt}; counts {claimable un-benchable, hypothesis-only, benchable}; claimable un-benchable / 201 = the determinacy-aware denominator. Each spine row carries a one-line mechanical receipt a referee re-checks (function + offline-availability, or surface-size vs budget, or run-twice divergence).

## Questions for review
1. Is C2 (scale via the search argument) rigorous and claimable, or is "surface size > budget" too hand-wavy? How to make the budget model defensible without per-task implementation?
2. Is the intrinsic rule (core-IS-the-artifact => claimable without test bodies) a sound way to satisfy the three-way property? Where does it leak?
3. Which hypothesis criteria (H4-H12) can be promoted to spine via a mechanical intrinsic argument?
4. Biggest remaining attack on the classification.
