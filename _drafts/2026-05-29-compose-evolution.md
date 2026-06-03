---
variant: post-wide
title: "How the Compose Skill Was Born"
tags: coding, methodology, llm, epistemology, overfitting
draft: true
---

> ROUGH DRAFT. Notes-shaped, narrative-tight in places, telegraphic in others. The through-line is *overfitting is absolutely possible in this regime, and a skill that produces structurally-correct output isn't the same as a skill whose case has been earned.* Compose is the worked example. The methodology section pulls out the defenses.

The big meta-lesson of the project so far, stated cleanly because everything else in this post is a consequence of it: **overfitting is absolutely possible in this regime.** "This regime" means LLM-driven harness iteration where a discipline can be encoded as skill prose, dispatched against a substrate, produce structurally-correct artifacts, and *look like it works* — without the artifact earning the right to claim it generalizes. The defense isn't more discipline. The defense is the verification on the verification, the machinery-vs-case confidence split, the receipt artifact that makes the discipline's work auditable, and the refusal to let "the skill exists" silently become "the skill is necessary."

The compose skill is the cleanest example because its gap is widest. Built on a corpus-grounded failure mode. Architecturally clean. First measurement produced a 28-element surface matrix from one file in the codebase, then trimmed to 8 SOUND+LIVE tests. Then the targeted ablations missed exactly what the build-tools gate missed — at which point the skill's case looked broken, until the verification-on-the-verification said: the mutations are inert at the canonical level, the gap was illusory, the skill's case is *unfound*, not earned. Machinery confidence 82. Case confidence 30. Both numbers in the project's hypothesis graph. Neither in the README.

## The moment the skill was needed

It is 2026-05-27 ~23:59. The feature pipeline (`design-doc → build-tools → implement-spec → verify-spec`) had just been patched with `build-tools`' interface-enumeration sub-phase — write one test per PRD-listed element when the PRD enumerates a flat surface. The discipline had worked on kysely (71% breadth substrate, 6/6 mutants caught) and opa (50% path substrate, 6/6 caught via the iteration sub-phase filling the enumeration sub-phase's gaps).

Now a substrate that should *expose* the discipline's limits: `oxvg-structural-selector-preservation`. F₁₂ classified it 40% compositional; the PRD is five sentences of pure prose, no operators, no method lists, no keywords. The blind subagent ran:

```
9 criteria (7 certain + 2 routed-to-residue for ambiguity)
8 proxy tests; SOUND + LIVE
0 per-element tests; 0 spurious-enum splits
```

The interface-enumeration sub-phase had **correctly stayed silent**. There were no PRD listings to expand. The discriminating-test sub-phase carried the gate's design — each test atomized one PRD clause and built paired discriminating inputs against a named plausible-wrong impl.

Discipline-gate behavior: correct. The skill's predicate worked exactly as designed.

Then the targeted ablations:

| Mutation | Class | Proxy catches? |
|---|---|---|
| M-first-child | structural pseudo | MISSED |
| M-nth-child | structural pseudo | MISSED |

Two structural-pseudo mutations slipped past the gate. The agent's surface inference stopped at four combinator axes (descendant, child, adjacent-sibling, general-sibling) — the things the PRD's word "structure-dependent" cued. It never enumerated the structural pseudos (`:first-child`, `:nth-child`, `:last-child`, `:only-child`, `:nth-last-child`, `:empty`) because the PRD never named them. But oxvg's selector engine in `parcel_selectors/parser.rs` *handles them all*. The invariant must hold across them too.

**The gap shape named the missing discipline.** For invariant-shaped PRDs, the surface is not enumerated in the PRD; it has to be inferred from the codebase's existing supported axes. The interface-enumeration discipline enumerates surfaces the PRD already lists. Whatever fills the new gap enumerates surfaces the PRD *implies* via the invariant — by reading the codebase to find every axis the invariant must hold across.

This is the moment a hypothesis got registered: *there exists a separable discipline for invariant-shaped PRDs that reads the codebase to infer the surface where the invariant must hold.*

Notice what's happening at this layer. A specific failure on a specific substrate names a specific missing discipline. The hypothesis is locatable; the substrate that originated it is referenceable; the next step is buildable.

That layer is also exactly where the overfit risk starts. The two ablation mutants that motivated the whole skill came from the experimenter, not the canonical suite. The "gap" they revealed lived only in the experimenter's head. The discipline-to-be was about to be built on what would turn out, hours later, to be an illusion.

## Why a separate skill, not a sub-phase

The choice was deliberate and recorded:

> Composer as a separate skill, not a build-tools sub-phase. Reasoning:
> 1. Load-bearing step is structurally different (codebase surface inference vs PRD listing read).
> 2. Sharing Phase 2 with interface-enumeration risks the prose-overload that an earlier review caught on Phase 4.

The build-tools file at that moment was already carrying five disciplines layered as prose. Stacking a sixth that *reads the codebase* (vs reading the PRD) would dilute the single-axis cognitive frame each sub-phase needs to fire correctly. The right architectural decomposition: two sibling skills with a routing predicate, monoidally composable.

The naming hesitation is in the lineage too — `compose` because it's a sibling of `build-tools`, not because the skill itself composes things. The skill composes *test pairs across an inferred surface*. The meta-property — skills composable in either order, monoidally — came later as its own hypothesis.

## The routing predicate

The discipline needed a trigger. The earlier predicate guess — gate routing on canonical-test class — had already been refuted by `opa-rego-rule-profiling`, which the corpus classifier scored path-dominant 50% / breadth 0% but whose PRD is enumeration-rich (17 EvalProfile methods + parallel nil-receiver behaviors). The agent ran the enumeration discipline anyway, caught 6/6 mutants. The discipline-trigger predicate is NOT the canonical-test class. It's the PRD's shape — observable from the agent's own first read.

Concretizing it was a single change to `design-doc/skill.md` Phase 5:

```
FEATURE-SHAPE: enum | invariant | mixed
```

Where:
- `enum` → the PRD lists ≥ 2 named elements somewhere. Route to **build-tools**.
- `invariant` → the PRD has "preserve / must hold / when X then Y" clauses across surfaces it doesn't enumerate. Route to **compose**.
- `mixed` → both. Route to **build-tools** for the named slice, then **compose** for the inferred slice.

Two properties that matter:

1. **Observable from PRD alone.** No privileged access. The agent reads `instruction.md` and decides.
2. **Routing is advisory; each skill's Phase 0 self-classifies on the PRD and self-no-ops on wrong-shape input.** Misrouting is recoverable, not fatal. The cost of a wrong route is a no-op, not a corrupted manifest.

## The build

`skills/compose/skill.md` was written as a six-phase pipeline. The phases mirror build-tools but pivot on a different load-bearing artifact: `surface-matrix.md`.

```
Phase 0 — Self-classify + convergence read (monoidal contract for LLM skills)
Phase 1 — Triage criteria (certain → gate, ambiguous → residue)
Phase 2 — Surface inference (THE LOAD-BEARING STEP)
Phase 3 — Spurious-axis check (sister to spurious-enumeration)
Phase 4 — Build paired control/perturbation tests
Phase 5 — Cross-family adversary review (typed-acceptance protocol)
Phase 6 — Emit manifest
```

The load-bearing artifact looks like this:

```
## Axis: structural selector kind
- descendant combinator (` `)  — file.rs:120 match arm
- child combinator (`>`)       — file.rs:121 match arm
- adjacent-sibling (`+`)       — file.rs:122 match arm
- general-sibling (`~`)        — file.rs:123 match arm
- :first-child                 — file.rs:380 match arm
- :last-child                  — file.rs:381 match arm
- :only-child                  — file.rs:382 match arm
- :nth-child(...)              — file.rs:386 prefix-match arm
- :nth-last-child(...)         — file.rs:387 prefix-match arm
- :empty                       — file.rs:383 match arm
```

The matrix is intentionally heavy. It makes surface inference *legible*. The operator, adversary, or a re-entry pass can audit "did we look in the right place?" by reading one file. Without it, surface inference is invisible and ungrounded — exactly the F₁₆ failure mode on oxvg, where the agent did infer four combinators but had no artifact saying "and here are the axes we considered and excluded," so the missing pseudos weren't even visible as gaps.

Each axis element gets a **confidence mark**: deduction (the implementation visibly handles it) or abduction (PRD invariant implies it should hold but no implementation pin yet). Deduction axes go straight to the gate; abduction axes need an extra sanity check before becoming gate tests.

Each test in the gate is **paired**: a CONTROL input where the invariant holds trivially, and a PERTURBATION input where, if the invariant fails for this axis element, a different observable appears. The pair structure makes mutation thinking explicit — the "perturbation" IS the plausible wrong shape. A paired test that doesn't distinguish a plausible-wrong impl is dead weight.

## First measurement: machinery works

The first blind run on the substrate that named the discipline:

```
First blind compose run on oxvg-structural-selector-preservation:

- FEATURE-SHAPE = invariant (chosen correctly)
- Surface matrix: 6 axes, 28 elements with provenance to
  parcel_selectors-0.28.2/parser.rs (combinators, NthType variants
  including all 11 structural pseudos, functional pseudos, attribute
  operators, external anchor, locality)
- Initial draft: 28 paired tests
- Phase 3 trim: 8 SOUND+LIVE tests
  (agent dropped 20 axes because gold-vs-pre-fix produced behaviorally
  equivalent outputs on those axes)
```

The agent inferred a 28-element surface from one file in the codebase, then trimmed 20 axes whose semantics produced behaviorally-equivalent gold-vs-pre-fix outputs. Phase 3's spurious-axis check fired correctly.

Then the gate against the originating mutants:

| Mutation | Compose proxy catches? |
|---|---|
| M-first-child | MISSED |
| M-nth-child | MISSED |

The same two mutations the build-tools gate missed. First reading: "compose's Phase 3 trimmed too aggressively." The skill's case looked broken.

This is the load-bearing moment. The natural narrative — "discipline missed; build a stronger version" — is the overfit attractor. It's where the project's earlier overfitting accumulated: a session that anchored on bandit (an outlier 42% compositional task) had built five disciplines targeting the second-largest class, all confirmed on the anchor, and only refuted at the population layer when a cross-substrate sweep classified the corpus and found breadth, not compositional, was the dominant class.

The defense against the same shape recurring here is a single check that costs ~30 seconds.

## The correction: experimenter's H₈

Before recording the gap as real, a verification step nobody had thought to run on the original gap claim:

> Run the candidate mutations against the canonical suite first.

Result: canonical (10 hidden tests) also passes both mutations 10/10. The "mutations" don't observably change canonical behavior. Gold's `is_structure_sensitive_selector` isn't reached by canonical's selector shapes. The mutations are **inert at the canonical level**.

That changes everything. The compose gate's "miss" wasn't a coverage gap — there was nothing to catch. Phase 3's trim was correct soundness logic. The original gap on oxvg was a phantom; the mutations were inert from the start; nobody had verified.

This is the **experimenter's H₈** — the same discrimination-on-the-experiment-itself the discipline asks the agent to apply to its tests, now caught at the meta-layer. The discipline says: *for each test, name the plausible-wrong impl and ensure inputs distinguish it.* The corresponding meta-rule: *for each ablation, ensure the mutation observably changes canonical behavior on the canonical suite, not just on a hand-built test.*

It was the second occurrence in the session. The first was an opa mutation (`HotRules []` instead of `nil`) which was a no-op in Go's nil-slice semantics. Both times the "gap" wasn't real because the mutation wasn't observable. Both times the verification on the verification caught it.

What was preserved after the correction:

- Compose machinery confidence: **~82** (skill produces structurally correct surface-matrix.md + manifest + paired tests + SOUND+LIVE gate on first try, on a representative invariant-shape PRD)
- Compose case confidence: **~30** (the oxvg gap claimed previously was inert mutations; the composer is built but its load-bearing necessity hasn't been earned on this substrate)

The honest residue: *machinery built, case unfound*. Don't overclaim. The skill's evidence base must be re-found on a task where invariant-axis mutations are actually canonical-load-bearing. oxvg is not that task.

This is what overfitting in this regime looks like, caught at the meta-layer. The discipline was about to be banked as "demonstrated on a real substrate." It wasn't. The substrate was contributing nothing to the demonstration; the experimenter had been measuring against a hand-built test that didn't reach the canonical suite. The cost of catching it: 30 seconds of canonical-suite execution. The cost of not catching it: a year of "compose works because oxvg" in every project summary.

## The monoidal contract

A few hours after compose was built, an audit pass tightened the skill family into a contract:

```
build-tools ∘ compose ≈ compose ∘ build-tools   (on mixed-shape inputs)
compose ∘ compose ≈ compose                       (idempotent re-run)
build-tools ∘ build-tools ≈ build-tools           (idempotent re-run)
On wrong-shape input: identity (clean no-op)
```

Each skill gained a **Phase 0 self-classify**:

```
Sniff rule (symmetric across skills):
- enum-count = PRD listings of ≥ 2 named elements.
- invariant-count = PRD "preserve / must hold / when X then Y" clauses
  across unstated surfaces.
- applies if invariant-count ≥ 1 AND enum-count = 0.
- partially-applies if both > 0.
- does-not-apply if invariant-count = 0.
```

Each skill's emit phase rewrote from "write manifest" to "merge manifest" — detect the other skill's slice via `*.applied: true` and merge into a shared `proxy_gate.criteria` list. The manifest schema gained two slices (`build_tools` and `compose`) plus a union `proxy_gate` that downstream tooling reads agnostically.

Notable, and not buried: the asserted contract is *not yet measured*. The contract is written in skill prose. A skill that says "merge" but actually overwrites would silently violate the contract; only an end-to-end double-dispatch test catches it. Until that runs, the monoidality is asserted but not earned. Same shape as the experimenter's H₈ correction: writing "monoidal" in skill prose doesn't make the implementation behave that way.

## What the compose skill currently knows about itself

The skill exists. It runs. Its first measured run produced a structurally correct artifact pipeline. Its claimed-originating gap turned out to be a phantom from un-verified ablations. Its monoidal contract is asserted in prose, not verified by double-dispatch. **The skill is built but it has not yet earned the right to exist on the corpus.**

That residue is in the hypothesis graph, in the lessons log, in the worklog. It is not in the README. The discipline is to keep the gap visible — to not let "the skill exists" silently become "the skill is necessary" without measurement. The cost of overfitting in this regime is that a skill written from prose, dispatched against a substrate that produces correct-looking output, gets locked in as load-bearing and starts paying its complexity tax in every future iteration. The defense is the confidence split that holds machinery and case separately.

## The methodology pattern

The compose skill's story is one instantiation of a pattern that recurs across this project. The defense against overfitting at the LLM-skill layer is structural, not heroic. Each property below is a guard against a specific overfit shape.

**Failure-driven skill genesis.** A skill is born from a *specific named failure mode* on a specific substrate. The originating failure carries the discipline's name and the hypothesis is registered in the graph before the skill file is written. If the genesis can't be stated as a specific failure, the skill probably shouldn't be built — the discipline doesn't have a measurable trigger. Guards against: building disciplines for hypothetical problems.

**Architectural choice is decision-recorded.** "Should this be a separate skill or a sub-phase?" is a decision made with falsifiable rationale, recorded in the lessons log. The rationale is referenceable later; if the architecture is wrong, the recorded reason narrows what to revise. Guards against: post-hoc rationalization of architectural drift.

**Routing predicate is observable from the agent's own first read.** Skills that fire conditionally need their trigger to be locatable without privileged access. Build the predicate on what the agent can see, not on metadata only the operator has. Guards against: privileged-information leakage into the discipline's trigger.

**Routing is advisory; self-classify is load-bearing.** Each skill's Phase 0 re-classifies on the PRD and self-no-ops on wrong-shape input. The cost of a wrong route is a no-op, not a corrupted manifest. Guards against: cascade failures from one skill's misclassification.

**Load-bearing artifact ≠ load-bearing skill.** The artifact that makes the skill's work *legible* is its load-bearing component. For compose: `surface-matrix.md`. The test file is the output; the surface matrix is the receipt. Without the receipt, the discipline's work is invisible and ungrounded. Guards against: undebuggable opaque artifacts.

**First measurement on the originating substrate.** The first blind run goes on the substrate that named the discipline. The confirmation/refutation must distinguish *machinery soundness* from *case necessity*. A skill can produce structurally correct output on a substrate where it wasn't needed. Guards against: conflating "skill produces correct artifacts" with "skill catches the originating gap."

**The verification on the verification.** Before recording a gap as real, run the candidate mutation against the canonical suite. If canonical passes too, the mutation is inert and the gap is illusory. Costs ~30 seconds per ablation; has caught two phantom gaps in this project. Guards against: the experimenter's H₈, which is the single largest overfit-attractor at the meta-layer.

**Honest residue beats overclaimed confidence.** Split confidence into machinery and case. Machinery confidence is what the skill produces structurally; case confidence is whether the substrate proved the skill was necessary. Compose currently sits at machinery-82 / case-30. The case-30 is *load-bearing for the project's honesty* — without it, "we built compose" silently becomes "we proved compose is necessary," which the evidence doesn't yet support. Guards against: the silent confidence inflation that turns prose into headline numbers.

**Contract assertions are prose-only until measured.** The monoidal contract is in skill prose. It is not yet verified. Same shape as the experimenter's H₈ at the experimenter layer: don't trust your own claim about your own skill until you've run the measurement that would falsify it. Guards against: structural claims that look like theorems but are decorations.

**The skill is published as built + as not-yet-earned.** The deliverable is the skill *plus* its honest residue. A reader who would otherwise overclaim from "skill exists" is corrected by the graph's own self-report. Guards against: downstream consumers (other agents, other operators, future-self) inheriting a confidence the evidence doesn't support.

## What the same pattern looks like at the task layer

The same defenses work for per-task discipline iteration, not just per-skill architectural decomposition. A recent partial run on a different model pair surfaced a parallel instance:

- **Failure-driven discipline genesis:** an axis-crossing discipline born from a Composer impl that scored 96.2% on the hidden suite, where the failures were specifically cross-axis cases like `all & B602` collapsing the `all`-token sentinel into the intersection's empty-set sentinel.
- **Architectural choice recorded:** added as a sub-phase in build-tools, not a separate skill (the load-bearing step is the same shape as the existing enumeration discipline).
- **First measurement on the originating substrate:** Composer-as-build-tools w/ patched skill produced 51 tests including 6 axis-crossing tests, 2 of which caught the same impl bugs the hidden suite caught.
- **Verification on the verification:** ran the patched gate against patched impl, found 7 of 9 fail-on-original tests were SPECULATION — they fail on a correct impl too. The discipline caught structural gaps but produced its own overfit residue at proxy-author time.
- **Honest residue:** a new hypothesis named explicitly stating that procedural disciplines converge slowly; full speculation elimination via prose alone is infeasible.
- **Cross-substrate verification:** the discipline structurally transfers to a different feature class (additive abort-wiring on a TypeScript codebase) at n=2.

Same loop. Same defenses. Same overfit attractors avoided by the same checks. The fact that the pattern runs at both layers — per-task discipline iteration and per-skill architectural decomposition — is the methodological point worth stealing.

## Closing

The compose skill is, as of this writing, a worked example of the methodology more than of itself. Its machinery is sound. Its case is honestly unfound. Its monoidal contract is asserted, not measured. Its existence-in-the-pipeline is the residue of a hypothesis registered, a discipline built, a first measurement run, a phantom gap caught at the meta-layer, and a refusal to overclaim despite the architectural work being done.

If a future operator finds a substrate where invariant-axis mutations are canonical-load-bearing — where the codebase supports an axis the PRD never names AND the hidden test actually exercises that axis — compose's case confidence will move from 30 to evidence. Until then, the residue stays in the graph and the README stays quiet.

Overfitting in this regime is the natural attractor. A discipline that produces structurally-correct output on the substrate that named it, with no canonical-suite verification, is exactly the shape that would otherwise lock in. The methodology's promise is that the project's confidence stays bounded by what's been measured, not by what's been written. The cost of that promise is the bookkeeping. The payoff is that the residue stays visible and the next operator inherits an honest hypothesis graph instead of a pile of prose contracts.
