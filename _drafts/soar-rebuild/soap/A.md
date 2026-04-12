---
system: Soar
target: SoarGroup/Soar
stage: production/legacy
intake_input: ./S.md (finalized 2026-04-10, elicitation complete)
diagnose_input: ./O.md (updated 2026-04-10)
assessment_run: 2026-04-10
assessment_status: final — reflects finalized S.md, updated O.md, and elicitation Q1-Q4
upstream_ref: origin/development @ f65f626e4 (2026-03-05) — SoarGroup/Soar
---

# Soar — Assessment

*Human judgment on the evidence. Direct, honest, actionable.*

## 1. Procedural honesty note

**What has human override.** The Q1 semantic-learning gap reading is a human override of S.md's default. The user overrode S.md's (c) underdetermined default to (a) gap, citing C71 ("there are still types of architectural learning that are missing, such as semantic learning") and the 2026-04-09 meeting with Laird. This is the user's judgment, not a finding grounded by S/O alone.

**What evidence this assessment runs on.** S.md finalized 2026-04-10 with S1 (Laird 2022) read in full, S2 (Derbinsky & Laird 2013) read cold and filed as C74-C83, S5 (source code) partially grepped, S6 (meeting correspondence) filed as paraphrased claims C90-C92. Elicitation Q1-Q4 answered by the user. S3 (Gentle Introduction) and S4 (manual) not read; declared non-load-bearing for this assessment.

**What this assessment is entitled to do.** Record what /diagnose sees in the evidence. Classify observations. Record human overrides faithfully. Name the diagnosis. It is not entitled to name mechanisms or algorithms — that is /prescribe territory.

## 2. Errors in the prior A.md

The prior A.md (second draft, 2026-04-09) diagnosed missing architectural mechanisms. It was wrong in three ways:

1. **The single-clock thesis was a hypothesis without ground.** It was a human-input hypothesis under test that was never confirmed or disconfirmed by evidence. The elicitation supersedes it: Q4 identifies the broken role as organizational Consolidate, not architectural clock design. The thesis is retired — not because it was disproven, but because the organizational-level diagnosis is more actionable and better supported by the meeting evidence (S6).

2. **The causal chain double-counted.** Three manifestations (Q1 gap, Q4 write-time commit, Q5 stochastic restriction) were presented as independent findings traceable to a single root. Codex caught this in the first draft; the second draft acknowledged it but kept the structure. The new diagnosis does not need a causal chain — the three gaps are real observations that do not require a unifying architectural root cause to be actionable.

3. **Prescription mixed into assessment.** The forced-optimization appendix, the clock-splitting direction, and the constraint set all belonged to a prescription framing that assumed "which mechanism to add" was the right question. The elicitation says the right question is "how to evaluate whether a mechanism is an improvement."

The prior A.md's role-by-role tower table and its code-level observations remain valid as O.md content. The interpretive layer built on top of them — the thesis, the causal chain, the C55 alternative reading — is retired.

## 3. Diagnosis: broken organizational Consolidate

### What Soar has

Soar has real architectural gaps that Laird himself acknowledges:

- **C71: Semantic learning is missing.** Laird lists it explicitly as a type of architectural learning that is still absent (S1 §10 item 7).
- **C67: Stochastic-substate chunking is planned but unshipped.** Laird states plans to extend chunking to handle stochastic substates "when there is sufficient accumulated experience to ensure that they have a high probability of being correct." Four years later, upstream has not implemented this.
- **C72: Bootstrap is what Laird feels is most missing.** "Without a human to closely guide it, Rosie is unable to get very far on its own."

These are Laird's own words. They are not disputed.

### What the prior intake got wrong

The prior intake (2026-03-23 diagnosis-soar) correctly identified some of these gaps but prescribed wrong fillers:

- **epmem-to-smem consolidation** was proposed as the Q1 filler. Laird rejected it at the 2026-04-09 meeting: smem and epmem have structurally different data models (C90-C91), and smem is populated by deliberate cognition, not derived from epmem (C92). The prior intake's mental model — a unified graph where episodic edges accumulate into semantic nodes — does not match the architecture.
- **D&L 2013 extrapolation** was used to motivate smem/epmem eviction (PRs #578-580). D&L 2013 does not claim smem/epmem eviction is needed. The paper builds forgetting for WM and procedural memory only (C74). Smem is the stable backup store that makes WM forgetting safe (C76-C77). The extrapolation from "WM forgetting is needed" to "smem eviction is needed" was a categorical error.
- **PR #577's EMA criterion** was presented as the Q5 filler. The direction is architecturally adjacent to Laird's C67 plan, but the criterion (stability via EMA-of-|ΔQ|) is not what Laird specified (correctness via accumulated experience). It needs empirical evidence before it can be considered. Held, not retired.

### The root problem

The root problem is not "which mechanism to add." It is "how to evaluate whether a mechanism is an improvement."

The prior intake produced three PRs (#578-580) that were based on wrong assumptions. PR #577 has a defensible direction but an unvalidated criterion. In neither case did the contributor have a way to prove the change was an improvement, and in neither case did the maintainer have a way to verify it. The 2026-04-09 meeting confirmed this: after many failed attempts at diagnosis-level alignment, the one point of convergence between June and Laird was the need for evals.

This is a broken organizational Consolidate. In Natural Framework terms: the project's own learning loop — the mechanism by which contributor effort gets filtered, evaluated, and integrated into the substrate — is not functioning. Effort goes in; there is no signal that tells anyone whether the effort improved the system or damaged it.

### Speculation on root cause

Monolith ossification. The Soar codebase is a 40-year-old C++ monolith with tight module couplings. There is no quantitative feedback signal (benchmark suite, regression tests on cognitive metrics, eval harness for agent-level behavior). There is no qualitative feedback signal (contributor guidelines that map proposed changes to testable predictions). Without either signal, a contributor cannot distinguish a real improvement from a plausible-sounding mistake, and a maintainer cannot distinguish a valuable PR from a well-intentioned one.

This is speculation, not a finding. But it is consistent with the evidence: the experimental chunking and memory consolidation branches referenced in `debug_code/debug.h:9` existed and did not land in mainline. The prior intake's PRs were closed or held. Laird's own planned C67 modification has not shipped in four years. The pattern is: attempts are made, attempts do not land, and there is no eval infrastructure to tell anyone why.

## 4. Prescription target

**Evals, not mechanisms.** Build the measurement before building the mechanism.

The prescription should produce an eval harness that provides hill-climbing signal to contributors. Until that exists, any proposed mechanism — whether it is epmem-to-smem consolidation, stochastic-substate chunking, or something else — cannot be validated. The prior intake's failure is the proof: architecturally plausible proposals based on wrong assumptions, with no way to detect the error before presenting them to the maintainer.

What "evals" means concretely is /prescribe territory. A.md's job is to name the target, not to design it.

## 5. Retirements

### Retired: single-clock thesis

The hypothesis that Soar's single decision-cycle clock is the root cause of its Consolidate gaps. It was a human-input hypothesis that was never grounded by S/O evidence. It is superseded by the organizational-level diagnosis. The code-level observations that motivated it (every Consolidate operation runs at decision-cycle rate, no background threads in upstream) remain valid as O.md findings. The interpretive layer (this is because of a missing clock split, and the fix is to add one) is retired.

### Retired: forced-optimization appendix

The argument that clock splits at rate-mismatched interfaces are forced optimizations in classical computing. It was framing material for a prescription direction (give Consolidate a clock of its own) that is no longer the prescription target. The appendix remains in `prescribe_input.md` §3 for historical reference but should not be consumed by /prescribe.

### Retired: C55 alternative reading

The analysis of whether Soar's Consolidate gaps are better explained by the single-clock thesis or by C55's single-mechanism commitment. Both readings were attempts to find an architectural root cause. The organizational-level diagnosis makes the architectural-root-cause question moot for prescription purposes. C55 remains a valid observation about Soar's design philosophy; it is just not load-bearing for the prescription.

### Retired: PRs #578, #579, #580

Closed 2026-04-10 with documented wrongful assumptions. D&L 2013 extrapolation, epmem-to-smem pathway unsupported, scaling motivation retired.

### Held: PR #577

Direction aligned with Laird's C67 planned feature. Criterion unvalidated. Needs empirical evidence. This is exactly the kind of PR that an eval harness would help evaluate.

## 6. Hard constraints inherited by /prescribe

From prescribe_input.md, still valid:

1. **Do not assume epmem-to-smem consolidation is the filler for Q1.** Laird rejected it on architectural grounds (C90-C92). The prior intake's pathway is closed.

4. **Do not motivate on scaling-is-bottleneck grounds.** The Q3 elicitation retired the D&L 2013 extrapolation. Laird rates real-time operation "yes, yes" (C69) and diverse knowledge at "tens of millions" (C70).

The remaining constraints from prescribe_input.md (2, 3, 5-8) were tied to the mechanism-level prescription framing and are retired along with it. Constraint 3 (EMA criterion for PR #577) remains relevant if /prescribe produces evals that could validate or invalidate PR #577's criterion.

## 7. What this assessment does not claim

- No specific mechanism for any gap. /prescribe territory.
- No claim that the single-clock thesis was wrong — only that it is moot for prescription purposes.
- No claim about SVS. S1 §8 partially read (C89); not load-bearing.
- No claim that C55 is wrong — only that the architectural-root-cause question is not the right question for this prescription cycle.
- No claim about what evals should look like. That is /prescribe's job.

---

*Final assessment, based on S.md finalized 2026-04-10, O.md updated same day, elicitation Q1-Q4, and the 2026-04-09 meeting with John Laird paraphrased by June Kim. The prescription target is evals, not mechanisms. Written via the [double loop](/double-loop).*
