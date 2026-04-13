---
name: forge
description: Turn a prescription into a clean PR with no human intervention. Runs Volley (sharpen spec) → Merge (implement) → Hunt (verify) → Volley (clean PR) as a single pipeline.
argument-hint: <prescription-document>
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent
---

# Forge: Prescription to Clean PR

Volley → Merge → Hunt → Volley. No human checkpoint between steps.

## Theory

- **SOAP note (P, continued)**: [SOAP Notes: Soar](/soap-notes-soar) — Prescribe writes the barebones Plan. Forge expands it: Volley sharpens sketch → detailed spec, Merge expands spec → implementation, Volley cleans implementation → PR. The Plan section grows from candidates to code.

## Input

The `soap/` directory, specifically `soap/P.md` (polished). Forge reads the Plan as its problem.md.

## Process

1. **Volley (sharpen).** Take the prescription's implementation sketch and sharpen it into a spec with testable claims. Converge in two rounds — if the spec doesn't stabilize, the prescription was underspecified (fail back to human).
2. **Merge (implement).** Blind-blind-merge. Two models (opus + codex), same spec, separate directories. Compare implementations, pick the structurally stronger one per component, synthesize. See Merge Tactics below.
3. **Hunt (verify).** Send codex (`codex exec --full-auto -m gpt-5.4`) on a bug hunt against the merged implementation. Codex reads the spec and the code, reports bugs (logic errors, spec violations, integration seams, security issues, edge cases) to a findings file. Fix all valid findings. Re-hunt until codex reports zero new bugs — convergence, not a fixed number of passes.
4. **Volley (clean).** Review the implementation against the spec. Clean up naming, remove dead code, ensure tests pass. Converge in two rounds. The output is a PR-ready branch.

## Merge Tactics

### Default: single-scope blind-blind

Two agents (opus + codex), same spec, same scope. Each writes to a separate directory. Compare, pick the better design per component, synthesize into one.

```
opus  ──→ dir-a/ ──┐
                    ├──→ compare ──→ merge
codex ──→ dir-b/ ──┘
```

### Split-scope: frontend/backend separation

When the spec has a clean boundary between scopes (e.g. server-side vs client-side, API vs UI), split into two independent specs and run blind-blind on each scope. Four agents total, two per model.

```
opus  ──→ server (/tmp/…-opus-server)   ──┐
codex ──→ server (/tmp/…-codex-server) ──┤──→ compare server ──┐
                                                                ├──→ merge all
opus  ──→ client (/tmp/…-opus-client)  ──┤──→ compare client ──┘
codex ──→ client (/tmp/…-codex-client) ──┘
```

**When to use split-scope:** the spec defines distinct modules with a documented interface between them (PubSub topics, API endpoints, shared data structures). Each scope's agents can assume the other scope's API exists without implementing it.

**Cross-scope bugs:** the per-scope comparisons catch bugs within each scope (TOCTOU races, missing guards, wrong patterns). Bugs that only emerge at the integration boundary (mismatched return types, duplicate suffixes, defensive guards against missing functions) are caught during the merge step, which has context across all scopes.

### Directory isolation

Always use separate directories. Copy the repo to `/tmp/project-{agent}-{scope}` for each agent. Worktrees collapse — the second agent overwrites the first.

## Output

A clean branch with implementation, tests, and a PR description. Ready for `gh pr create`.

## Contract

- **Precondition**: `soap/P.md` polished, with substantiated algorithm candidates and implementation sketches
- **Postcondition**: branch passes tests, PR description traces back to prescription, diff matches spec
- **Idempotency**: forging the same prescription twice produces the same PR
- **Failure mode**: if Volley doesn't converge in two rounds at either step, halt and return to human with the unconverged state. Hunt runs until zero new bugs, not a fixed number of passes.
