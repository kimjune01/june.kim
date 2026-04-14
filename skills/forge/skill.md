---
name: forge
description: Turn a spec into a clean PR with no human intervention. Runs Volley (sharpen spec) → Merge (implement) → Hunt (verify) → Volley (clean PR) as a single pipeline.
argument-hint: <spec-or-path> [--build CMD] [--test CMD]
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, Agent
---

# Forge: Spec to Clean PR

Volley → Merge → Hunt → Volley. No human checkpoint between steps.

## Theory

- **SOAP note (P, continued)**: [SOAP Notes: Soar](/soap-notes-soar) — Prescribe writes the barebones Plan. Forge expands it: Volley sharpens sketch → detailed spec, Merge expands spec → implementation, Volley cleans implementation → PR. The Plan section grows from candidates to code.

## Input

Forge accepts a spec from any source:

1. **SOAP prescription** — `soap/P.md` or a path to any prescription document. Richest input: algorithm candidates, implementation sketches, substantiated claims.
2. **Inline spec** — a description passed as the argument. Forge treats it as the starting sketch for Volley to sharpen.
3. **File path** — any `.md` file containing a spec, feature request, or problem statement.

If no argument is given, forge checks for `soap/P.md` and uses it if present. Otherwise it fails with a usage hint.

### Toolchain detection

Forge infers build and test commands from the project root unless overridden:

| Marker | Build | Test |
|--------|-------|------|
| `Makefile` | `make` | `make test` |
| `package.json` | `pnpm build` | `pnpm test` |
| `mix.exs` | `mix compile` | `mix test` |
| `Cargo.toml` | `cargo build` | `cargo test` |
| `go.mod` | `go build ./...` | `go test ./...` |
| `pyproject.toml` | `uv build` | `uv run pytest` |

Override with `--build CMD` and `--test CMD` in the argument. When overridden, use those commands verbatim — no inference.

## Process

0. **Preflight.** Before spending agent time, verify forge has everything it needs. Check each item and report a summary to the user. If any item is missing or ambiguous, ask — don't guess.

   **Checklist:**
   - [ ] **Spec exists and is actionable.** Read the spec (file or inline). It must describe *what* to build, not just *what's wrong*. A problem statement without a solution direction is underspecified — ask the user to add one or point to a prescription.
   - [ ] **Scope is bounded.** The spec should touch a finite set of files/modules. If it implies changes across the whole codebase or is open-ended ("improve performance"), ask the user to narrow it.
   - [ ] **Build command resolves.** Detect or confirm the build command. Run it once to verify the project builds clean *before* any changes. If the build is already broken, stop — forge can't distinguish its own breakage from pre-existing breakage.
   - [ ] **Test command resolves.** Detect or confirm the test command. Run it once. If tests don't pass, stop — same reason.
   - [ ] **No uncommitted changes.** `git status` must be clean. Forge creates branches and commits; uncommitted work would get tangled.
   - [ ] **Scope strategy decided.** Single-scope or split-scope? If the spec has a clean module boundary, recommend split-scope and confirm.

   If all items pass, print the resolved config (spec source, build cmd, test cmd, scope strategy) and proceed. No confirmation needed — the checklist *is* the gate.

1. **Volley (sharpen).** Take the spec and sharpen it into testable claims. Converge in two rounds — if the spec doesn't stabilize, it was underspecified (fail back to human).
2. **Hunt (spec).** Before writing any code, hunt the spec itself. Send the sharpened spec to codex with the relevant source files as context. Look for: internal contradictions, assumptions that don't match the codebase (wrong API shapes, nonexistent modules, stale interfaces), underspecified edges that will force implementation guesses. Fix the spec, re-hunt, repeat until zero new findings. A spec bug that survives this step propagates through every downstream step.
3. **Merge (implement).** Blind-blind-merge. Two models (opus + codex), same spec, separate directories. Compare implementations, pick the structurally stronger one per component, synthesize. See Merge Tactics below.
4. **Hunt (code).** Run `/bug-hunt` against the merged implementation with the spec as input. See the bug-hunt skill for the full protocol — adversarial codex review iterated to convergence. If a bug traces back to a spec defect that survived step 2, fix the spec first, then re-merge from the corrected spec rather than patching the implementation.
5. **Volley (clean).** Review the implementation against the spec. Clean up naming, remove dead code, ensure tests pass. Converge in two rounds. The output is a PR-ready branch.

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

- **Precondition**: a spec — either `soap/P.md`, a file path, or inline text. Must be specific enough for Volley to sharpen into testable claims in two rounds.
- **Postcondition**: branch passes tests, PR description traces back to spec, diff matches spec
- **Idempotency**: forging the same prescription twice produces the same PR
- **Failure mode**: if Volley doesn't converge in two rounds at either step, halt and return to human with the unconverged state. Hunt runs until zero new bugs, not a fixed number of passes.
