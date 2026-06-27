# Bench-audit feasibility — fan-out

Can June's two benchmark-audit methods be ported to other labs' published benches? Diverge over 5 candidates, converge with codex, rank, pilot.

## The lens (preconditions both methods need)

- **(A) Determinacy audit** — classify each task by whether the solver's materials (prose + base-commit source) determine the behavior the hidden test grades. Grep-mechanical tiers (airtight / misdetermined / codebase-plural) + adversarial two-expert. Output: model-free % underdetermined, re-runnable receipts. *Done on SWE-bench Pro: 15% floor.*
- **(B) Oracle audit** — apply each task's own gold, run its own verifier, flag golds that fail their own test. Plus denominator hygiene, artifact-reproducibility, five-minute agent audit. *Done on DeepSWE.*
- **Preconditions:** public tasks + per-task gold/reference + runnable verifier + grader scoring a *specific* behavior + per-instance receipts.

## Cycle 1 — diverge (5 agents, opus)

### H1: METR RE-Bench (Medium)
**Verdict:** Only the oracle-gap limb ports; headline finding pre-documented.
- Open (MIT), runnable via Vivaria; reference solutions public but password-gated. [agent]
- **Continuous-score, open-ended → no per-task pass/fail gold.** Oracle gold-passes-verifier and determinacy both fail to port. [agent]
- Oracle-gap/grader-reachability ports strongly and is **confirmed by METR**: in-environment scorer, 30.4% reward-hack rate, Optimize-LLM-Foundry 100% (precompute+cache). So a bare "scorer reachable" finding is *not novel*. [agent]
- Novelty only from per-env line-level scorer enumeration or reference-score-reproduction failures. GPU cost is the tax.

### H2: METR HCAST (Medium-Low)
**Verdict:** Determinacy ports on the public sliver; oracle blocked; held-out majority caps the claim.
- Spec-to-behavior with deterministic `score()` verifiers in public `TaskFamily.py` → **determinacy + grader-reachability port cleanly**. [agent]
- **Gold solutions withheld** (protected) → oracle gold-passes-verifier check largely blocked. [agent]
- Only ~11/78 families (~14%) public; ~86% held out *by design* to protect the time-horizon metric. Audit = method demo on a sliver, cannot indict the measurement. [agent]
- Protected-solution norm conflicts with "re-runnable receipts" output. Welcome only if scoped honestly to the public subset.

### H3: Apollo scheming/sandbagging evals (Low)
**Verdict:** Different tool needed. Gold+verifier doesn't fit behavioral evals.
- No gold patch; verifier is often an **LLM judge reading model-controlled CoT**. Oracle audit's core check has no object. [agent]
- Flagship suites (2412.04984, 2509.15541) not released as runnable code; only eval-awareness (2505.23836) + the inspect_evals Scheming scorers are runnable. [agent]
- Only live port: reframe determinacy *onto the grader* — which verdicts are deterministic/externally-replayable vs judge-bottomed. But Apollo + adjacent work (Goodfire, arXiv:2510.19851) already own that critique. High redundancy/hit-piece risk.

### H4: Cooperative AI Melting Pot (Low) — DEAD
**Verdict:** MARL, no gold, no spec-to-code test. Poor fit.
- Fully open (Apache-2.0) but episodes scored by continuous returns; no gold artifact, no hidden test. Neither method ports. [agent]
- Only honest critique (focal score is gameable / underdetermined by scenario mix) **already published** (arXiv:2509.14485) and compute-heavy to redo. Abandons what makes the toolkit sharp.

### H5: SWE-bench Verified (High feasibility / Medium novelty)
**Verdict:** Identical shape to Pro; strongest as a *companion*, risky as a standalone.
- Fully public (problem_statement + gold patch + test_patch + FAIL_TO_PASS); **both methods port near-directly, existing Pro harness transfers.** Cheapest check = model-free afternoon grep sweep over 500 records. [agent]
- Gold-sweep half pre-empted by OpenAI's deprecation (contamination + ~60% broken failed-tests). [agent]
- Novelty lives in the **construct-validity axis** (orthogonal to OpenAI's contamination story, and contamination-proof because model-free) and in the **cross-benchmark trend**: a determinacy floor on Verified next to Pro's 15% makes underdetermination a property of the SWE-bench *construction recipe*, not one dataset. Standalone "audit of Verified" risks the saturated-target trap; companion-to-Pro is the move.

## Ranking after diverge

1. ~~**SWE-bench Verified (companion to Pro)**~~ — **KILLED (June): Verified is already dead.** OpenAI-deprecated, press cycle spent; even the companion framing reads as auditing a corpse. High feasibility, but the audience reflex ("Verified is dead") swamps the construct-validity wedge. Out.
2. **HCAST public subset** — determinacy-of-grader method demo, honest but capped at ~14%.
3. **RE-Bench** — oracle-gap enumeration, mostly pre-documented, GPU cost.
4. **Apollo (runnable slice)** — grader-determinacy tier-map, high redundancy risk.
5. **Melting Pot** — dead, poor fit.

Structural finding: the toolkit fits **SWE-bench-shaped benches only** (public gold + hidden test). Of the 5 named candidates, the one clean fit (Verified) is dead, and the rest force a contested *reframe* (determinacy-of-the-grader, replayability ledger).

**Open question the diverge exposes:** the toolkit wants a bench that is (a) SWE-shaped (public gold + hidden test), (b) **live and uncontaminated**, (c) not already autopsied. None of the 5 named candidates is all three. The real target is likely a *live* SWE-shaped bench the fan-out didn't enumerate — Terminal-Bench, SWE-Lancer, SWE-bench Multimodal, or a Lean/math bench (gold proof + checker). This is exactly what the codex converge was asked to surface.

## Cycle 2 — converge (codex adversarial)

**Codex verdict** confirms the structural finding and June's "Verified is dead" steer: Verified = high feasibility, low strategic value, companion at most, never flagship. Behavioral evals (Apollo/Melting Pot) force *method drift* off June's core methods. The flagship should be a **live** bench with real verifier structure.

**Codex's pick: Terminal-Bench** (arXiv:2505.07982, [tbench.ai](https://www.tbench.ai/)) — terminal-agent tasks, Dockerized environments, test-based grading; active, cited, **unaudited**. Both methods plausibly port:
- *determinacy:* task prompt + environment + files vs grader behavior.
- *oracle:* gold-passes-verifier on any subset with reference solutions.
- *new angle only this bench offers:* shell/infra nondeterminism, environment/test leakage, overfitting to visible tests.
- *risk to verify on recon:* reference solutions may not be public for enough tasks (oracle partial); tasks may be more operational than issue-spec (determinacy weaker).

Runners-up: **SWE-Lancer** (live, economically framed; depends on whether golds/private tests are exposed) and **SWE-bench Multimodal** (novel "are screenshots sufficient to *determine* behavior?" angle, needs visual rubrics). Lean/math = contrast class only ("formal verifiers have lower determinacy ambiguity"). Pro private set = high value, access-gated, "not a plan" without access.

**Five ways the plan breaks (codex):** (1) Verified produces a boring number; (2) perceived as chasing dead benchmarks — keep a live target in the portfolio; (3) gold-failure vs underdetermination get conflated — keep the three axes distinct; (4) HCAST sliver can't indict the time-horizon metric; (5) Apollo/Melting Pot = method drift.

## Pilot (the survivor)

**Flagship: Terminal-Bench** — the one target that is SWE-shaped *and* live/uncontaminated *and* not yet autopsied.

**Step 0 — recon (hours, model-free, go/no-go):** clone terminal-bench; confirm per-task tests are public; count tasks shipping a reference/gold solution (→ oracle applicability); sample ~20 task prompts for spec-shaped vs operational (→ determinacy applicability); check whether the grader/tests are reachable from inside the agent env (→ oracle-gap). Output: a table on which method ports and at what coverage.

**Step 1 — cheapest first checks:**
- *Oracle:* gold-passes-verifier sweep on every task with a reference solution (DeepSWE-style, ~$0 model cost). Flag any gold failing its own test.
- *Determinacy:* read N task prompts vs their tests; grep-mechanical tiers where a base repo exists; flag tasks whose test grades an unstated choice.
- *Five-minute agent audit:* point an agent at the public artifacts; cite specific inconsistencies (denominator, env nondeterminism, visible-test overfit).

**Step 2 — companion side-table:** Verified determinacy sweep (model-free, existing Pro harness), folded into a SWE-bench-family construct-validity argument. Supporting only, never the headline.

**Discipline:** keep three axes distinct — denominator hygiene / gold-verifier failure / construct validity.
