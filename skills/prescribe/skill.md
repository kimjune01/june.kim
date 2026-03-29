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

1. **Read the diagnosis.** Extract the list of broken roles and their assessments.
2. **Consult the Parts Bin.** Read the [parts bin](/the-parts-bin) grid. For each broken role, find the row (data type) and column (stage) that matches. Identify candidate algorithms in that cell.
3. **Evaluate candidates.** For each candidate: does it address the specific failure mode described in the diagnosis? Is it implementable within the system's constraints? Flag candidates that require architectural changes vs. those that can be added incrementally.
4. **Sketch the implementation.** For each viable candidate, write a 3–5 line description of how it would integrate with the existing system. Reference specific modules or files from the diagnosis.
5. **Write P (Plan).** `soap/P.md` — one section per broken role. Each section: role, failure mode (from `soap/A.md`), candidate algorithm, implementation sketch, expected outcome.

## Output

`soap/P.md`: one section per broken role, each with candidate algorithm and implementation sketch.

## Contract

- **Precondition**: diagnosis document with substantiated role assessments
- **Postcondition**: every prescribed algorithm exists in the Parts Bin or has a cited source
- **Does not**: implement the fix (that's Forge) or evaluate whether the fix is worth doing (that's the human checkpoint)
- **Checkpoint contract**: after Prescribe, the human is cross-examined — "does the prescribed algorithm address the root cause identified at the last checkpoint, or just the symptom?" and "is this implementable within the system's constraints, or does it require architectural changes the maintainers won't accept?"
- **Idempotency**: prescribing from the same diagnosis produces the same candidates
