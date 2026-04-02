---
name: prescribe
description: Look up the Parts Bin for algorithms that fill diagnosed broken roles. Produces a prescription document mapping each broken role to candidate algorithms with implementation sketches.
argument-hint: <diagnosis-document>
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch
---

# Prescribe: Parts Bin Lookup

For each broken role in a diagnosis, find candidate algorithms from the Parts Bin.

## Theory

- **The lookup table**: [The Parts Bin](/the-parts-bin) — row = data type, column = pipeline stage. Each cell holds candidate algorithms. Without this, Prescribe has nothing to consult.
- **SOAP note (P)**: [SOAP Notes: Soar](/soap-notes-soar) — Prescribe adds the Plan section, completing the clinical record.

## Input

A diagnosis document (output of Diagnose) identifying broken or missing roles.

## Process

1. **Read the diagnosis.** Extract the broken roles from `soap/A.md`, including their stack levels and the causal chain. Roles are tower-aware (e.g., "Consolidate @ Remember", not just "Consolidate"). Read development stage from S.md metadata.
2. **Elicit constraints.** Before consulting the Parts Bin, ask the human: "What's cheap? What's expensive? What's stable? What changes? What's the deployment constraint?" Record the answers. These constraints narrow the Parts Bin search — the Bin is a lookup table, not a shopping catalog. If S.md already contains constraint information (from development stage or elicitation), confirm rather than re-ask.
3. **Consult the Parts Bin (constrained).** Read the parts bin grid (`src/data/parts-bin.yml` or [the-parts-bin](/the-parts-bin)). For each broken role, find the row (data type) and column (stage) that matches. **Filter candidates through the constraints from step 2 before evaluating.** Skip algorithms that violate hard constraints (e.g., batch processing in a real-time system, new infrastructure for a PoC). Multiple gaps may map to the same algorithm — that's a signal to merge them.
4. **Evaluate survivors.** For each candidate that passes constraint filtering: does it address the specific failure mode described in the diagnosis? Is it the simplest thing the constraints allow? Flag candidates that require architectural changes vs. those that can be added incrementally.
5. **Sketch the implementation.** For each viable candidate, write a 3–5 line description of how it would integrate with the existing system. Reference specific modules or files from the diagnosis.
6. **Triage.** Organize prescriptions by urgency, not by role or dependency:
   - **Critical** — stop the bleeding. Changes that relieve the acute symptom using existing infrastructure. No new subsystems. Ship first.
   - **Structural** — enable healing. Infrastructure that the rehabilitative algorithms need. Ships after Critical earns trust.
   - **Rehabilitative** — build long-term health. Algorithms that run inside the new infrastructure. Ships last.

   Candidates that address the same code path at different urgencies should be split: the inline/immediate part is Critical, the batch/periodic part is Rehabilitative. Candidates from different broken roles that touch the same code path should be merged.
7. **Specify composition constraints.** Which prescriptions must run before which at runtime (dependency order), independent of triage tier. E.g., "promote to persistent store before evicting from cache."
8. **Write P (Plan).** `soap/P.md` — one section per candidate algorithm (not per broken role), organized by triage tier. Each section: failure mode (from A.md), candidate algorithm, implementation sketch, expected outcome. Followed by dependency order and composition constraints. **Include a "Design Evolution" section** recording each reframe that occurred during the session: what was proposed, what constraint or insight killed it, and what replaced it. The reader should see why simpler alternatives were chosen, not just the final prescription.
9. **Codex sniff.** Before presenting to the human, send P.md to codex. Apply obvious improvements directly (missing composition constraints, triage ordering issues, weak implementation sketches). Present only ambiguous or debatable points to the human alongside the checkpoint questions. **If codex is unavailable**, try Gemini as the reviewer. If neither is available, perform a self-review pass applying the same criteria. Log which reviewer was used or skipped.

## Output

`soap/P.md`: prescriptions organized by triage tier (Critical → Structural → Rehabilitative), with dependency order and composition constraints.

## Contract

- **Precondition**: diagnosis document with substantiated role assessments
- **Postcondition**: every prescribed algorithm exists in the Parts Bin or has a cited source
- **Does not**: implement the fix (that's Forge) or evaluate whether the fix is worth doing (that's the human checkpoint)
- **Checkpoint contract**: after codex sniff, the human is cross-examined — "does the prescribed algorithm address the root cause identified at the last checkpoint, or just the symptom?" and "is this implementable within the system's constraints, or does it require architectural changes the maintainers won't accept?"
- **Idempotency**: prescribing from the same diagnosis produces the same candidates

## Convergence

After writing P.md, re-read A.md and P.md together. Does every broken role in A.md have a prescription or an explicit `non_actionable` flag? Do the triage tiers and composition constraints hold up? Does the dependency order have gaps? If anything is missing, run another pass on steps 3-8. Report deltas each pass. **Hard stop at 10 passes** — if still changing, the skill is oscillating. Stop, report what's fluctuating, and let the human decide.
