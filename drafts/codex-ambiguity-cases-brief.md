# Brief: find GitHub bugfix cases for an ambiguity benchmark

I'm building a contamination-free benchmark of real software bugs where the *general* fix encodes a bit of intent that is NOT derivable from the issue text plus the repo. I need ~5 candidate cases off GitHub. Search the web/GitHub and verify each against the live repo. Be honest where you can't verify a detail.

## What makes a case qualify

A case is a real, merged GitHub bug with ALL of:

1. **A human oracle exists.** Either (a) a quick/narrow fix landed first and a more *general* fix landed later (two distinct PRs), or (b) the merged fix followed visible maintainer debate / competing PRs / a revert. The later/general fix is the oracle.
2. **The project's own test suite does not distinguish narrow from general.** The narrow fix passes the shipped tests; the general fix is needed for cases the suite never covers. (This is the "oracle gap.")
3. **Contamination-free.** Opened AND fixed recently (prefer 2026; 2025-H2 acceptable). Note the open and merge dates so I can check against model cutoffs.

## The distinction that matters most — select for ambiguity, not difficulty

- **Ambiguity (WANT — durable):** the general fix encodes a *choice/convention/intent* that no amount of reasoning recovers from the materials. The tell: a competent engineer (or model) would produce a confident, *reasonable-but-wrong* fix, or two reasonable engineers would pick different fixes. Contested fixes are GOOD here — contestation proves the bit was non-derivable. Example shape: ordering/comparison tie-break conventions, edge-case API semantics, "what should happen when X is empty/zero/null," backward-compat judgment calls.
- **Difficulty (acceptable but mark it — depreciating):** the general fix just takes deep reasoning/localization but IS derivable in principle. A strong frontier model may one-shot it. Mark these clearly; I weight them lower.

Prefer high-correctness-bar domains: verifiers, compilers, type checkers, parsers, serializers, ordering/comparators, concurrency, crypto. A worked reference example of the *difficulty* end is verus-lang/verus#2219 (narrow fix #2230, general #2501) — find cases like it but lean toward the ambiguity end.

## Output: ~5 candidates, for each give

- repo (owner/name), issue # + title + URL
- open date, fix merge date(s)
- narrow fix PR (# / URL) and general fix PR (# / URL), or the debate link
- domain
- oracle gap: does the shipped suite pass for BOTH narrow and general? (your best assessment)
- the non-derivable bit: 1-2 sentences on what intent the general fix encodes that the issue+repo don't determine
- classification: AMBIGUITY (durable) vs DIFFICULTY (depreciating), with one line of reasoning
- contamination risk: low/med/high and why

Rank them ambiguity-first. If you can only firmly verify fewer than 5, give the ones you can and say so rather than padding.
