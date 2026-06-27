# Oracle-Gap Bench — port-equivalence core

A bench to optimize encoded reasoning against, on the one axis the mechanism is for:
recovering the **external verdict** a model cannot author from its own belief
(§enum-calib of the hypothesis-graph paper). Substrate: synthetic differential
port/refactor. Oracle: mechanical differential vs a held reference. Goal: make
reasoning **cheaper** (externalize the XOR off the context window) and **better**
(reach the faithful artifact a self-grading model can't).

## Core invariant: the oracle gap must be real

The lift exists only where a model self-grades green while wrong. A differential
bench preserves that gap iff the reference is **held, never readable**:

- The solver never reads or runs the reference `R`.
- The harness exposes `R` only as a gate: `query(input) -> match | mismatch`
  comparing `candidate(input)` to `R(input)` (the abductor interface — pass/fail
  on candidate behavior, answer key hidden).
- Two arms differ in one bit: gate **disabled** (self-attested — model grades
  against its own belief of R) vs gate **enabled** (externally verified).

If the model can read R, it bootstraps the oracle and the lift vanishes. That
degenerate case is a control cell, not a bug.

## Task schema

```
task:
  reference:        R           # held; a function/module with rich edge behavior
  transform:        "port A->B" | "refactor preserving behavior"
  given:            signature + partial spec + visible_suite   # NOT full behavior, NOT R
  visible_suite:    happy-path tests, GREEN for both naive and faithful ports
  gate:             query(input) -> match|mismatch    # runs held R; on in self arm
  held_probes:      discriminating inputs (the answer key), split:
                      free_side:  inputs a naive port gets wrong (cheap, by construction)
                      hard_side:  tail inputs only a subtle divergence reveals
  oog_held_outs:    discriminating inputs the gate never showed (generalization test)
  recall_probe:     "how does R handle X?" asked cold (memorization control)
  diff_size:        LOC / branch-count / case-space  # the cost-axis coordinate
  pitfall_class:    encoding | locale | overflow | empty/null | ordering |
                    float-precision | off-by-one | unicode | tz | ...
```

`R` is drawn from behavior-rich code (parser, formatter, date/number, small
state machine, config loader, serializer) — domains where the interesting
divergence lives off the happy path. Contamination-free: use private/novel R, or
mutate existing R so the exact port can't be recalled.

## Generator (mechanical, contamination-free)

1. Pick `R` (real behavior-rich code, or a synthesized/mutated variant).
2. Auto-produce a population of **plausible-but-imperfect** ports:
   low-effort LLM ports + mutation of R seeded by `pitfall_class` (off-by-one,
   locale, encoding, overflow, empty handling, ordering, float).
3. Fuzz inputs; keep those where candidates **disagree with R**. Those are the
   discriminating probes.
4. `free_side` = inputs the naive/base port is wrong on (frequent). `hard_side`
   = inputs only a subtle divergence reveals (rare tail).
5. Build `visible_suite` from happy-path inputs only, and **verify blind** that
   it is green for both a naive port and the faithful one (the suite-blind
   condition; the bench's whole reason to exist).
6. Reserve a slice of discriminating probes as `oog_held_outs` — never fed to
   the gate, used only to score generalization.

## Protocol & metrics

Run each task as a 2-arm ablation (self vs external), score on held probes:

- `score_arm` = fraction of `hard_side` ∪ `oog_held_outs` where candidate == R
- `gate_green_arm` = candidate passes the solver's own check (visible_suite + self-probes)
- `tokens_arm`, `gate_queries_arm` = cost

Headline numbers:

| Metric | Definition | What it proves |
|---|---|---|
| **Engagement rate** | frac. tasks with `score_external > score_self + δ` **and both gate-green** | the lift, where both arms "looked done" |
| **Hard-side delta** | `score_external − score_self` on the tail | magnitude of encoded-reasoning gain |
| **OOG generalization** | external pass on `oog_held_outs` | rule learned, not gate fit |
| **Confident-wrong rate** | self arm: `gate_green ∧ score_self < 1` | the safety story (4/4-false-green analog) |
| **Cost crossover** | `diff_size` where external ≤ self tokens at equal score | the **cheaper-reasoning** result |

Stratify every number by `(diff_size bucket × pitfall_class)`. Report against the
stratified denominator, never an absolute rate.

## The cheaper-reasoning axis

This is the underused half and the synthetic substrate's advantage: `diff_size`
is free to dial. Sweep R from one function to a module too large to hold in
context, and plot self-arm in-context XOR accuracy + token cost vs `diff_size`
against the externalized gate. Expectations (each falsifiable):

- self-arm accuracy degrades super-linearly with `diff_size` (context-rot;
  §future-work "in-context abduction degrades with diff size").
- past the context window, in-context is impossible — externalization is the
  only option; the gate's cost is flat in `diff_size` (it queries, doesn't hold).
- **crossover**: a `diff_size` beyond which external is cheaper AND more accurate.

The Verus receipt is a single point on this axis; the bench draws the curve.

## Control cells (must include — they prove separation)

- **spec-given**: hand over full behavior of R → lift → 0 (the SWE-bench-Pro
  ENTAILED analog; the model one-shots).
- **no-gap**: naive port already matches R everywhere → lift → 0 (baseline reach).
- **reference-readable**: let the model read R → lift → 0 (proves the *gap*, not
  the diff, is the active ingredient).
- **no-oracle**: R held and no probe distinguishes faithful from naive →
  ungradeable → excluded/null (the underdetermined analog).

A valid bench shows the mechanism lifts the oracle-gap cells and is flat on all four controls.

## v0 scope (smallest thing that draws the curve)

- 1 language pair (e.g. Python→Rust) or 1 refactor type.
- ~30 `R` across 5 pitfall classes × 3 diff-size buckets, ~2 per cell.
- Generator + held-reference gate + grader, fully mechanical regrade.
- 2 arms × 1 draw to start; add draws once the signal is visible.
- Frozen dataset + regrade script committed; recall probe per task.

Ship the engagement-rate × diff-size table and the cost-crossover plot. That is
the optimize-against target: a harness change that lifts hard-side pass at fixed
or lower cost is real reasoning gain; one that only finishes faster is not.
