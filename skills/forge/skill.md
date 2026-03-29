---
name: forge
description: Turn a prescription into a clean PR with no human intervention. Runs Volley (sharpen spec) → Merge (implement) → Volley (clean PR) as a single pipeline.
argument-hint: <prescription-document>
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent
---

# Forge: Prescription to Clean PR

Volley → Merge → Volley. No human checkpoint between steps.

## Theory

- **SOAP note (P, continued)**: [SOAP Notes: Soar](/soap-notes-soar) — Prescribe writes the barebones Plan. Forge expands it: Volley sharpens sketch → detailed spec, Merge expands spec → implementation, Volley cleans implementation → PR. The Plan section grows from candidates to code.

## Input

The `soap/` directory, specifically `soap/P.md` (polished). Forge reads the Plan as its problem.md.

## Process

1. **Volley (sharpen).** Take the prescription's implementation sketch and sharpen it into a spec with testable claims. Converge in two rounds — if the spec doesn't stabilize, the prescription was underspecified (fail back to human).
2. **Merge (implement).** Blind, blind, merge. Synthesize the implementation from the converged spec. Write code, tests, and any necessary configuration. The spec is the contract — don't improvise beyond it.
3. **Volley (clean).** Review the implementation against the spec. Clean up naming, remove dead code, ensure tests pass. Converge in two rounds. The output is a PR-ready branch.

## Output

A clean branch with implementation, tests, and a PR description. Ready for `gh pr create`.

## Contract

- **Precondition**: `soap/P.md` polished, with substantiated algorithm candidates and implementation sketches
- **Postcondition**: branch passes tests, PR description traces back to prescription, diff matches spec
- **Idempotency**: forging the same prescription twice produces the same PR
- **Failure mode**: if Volley doesn't converge in two rounds at either step, halt and return to human with the unconverged state
