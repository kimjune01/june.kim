---
name: verify-spec
description: Verification phase for feature-request (PRD-shaped) tasks (DeepSWE / Harbor). Runs the proxy gate (the acceptance-criteria tests build-tools authored) + the project's existing suite (regressions vs `$BASELINE_FAILS`), classifies against the design doc's acceptance criteria, writes the decision as an artifact, and emits a verdict + re-entry route. RESOLVED here means proxy-green and regression-clean, explicitly NOT a certified grade-time pass. No edits.
argument-hint: <task-id>
allowed-tools: Read, Grep, Glob, Bash
---

# Verify-spec: classify the result, emit verdict + route

Run the proxy gate and the existing suite. Map every acceptance criterion to its proxy test. Classify and route. Never mutate the tree — the driver captures the patch after you.

## Rules (read first)

- **RESOLVED is `(proxy)` — never a certified grade-pass.** Always emit the qualifier.
- **Decision is artifact-first.** Write `$VERDICT_FILE` (JSON). Stdout `VERDICT:`/`RE-ENTER:` lines are a shim fallback.
- **REJECTED ≠ NOT_RESOLVED.** Retryable failure = NOT_RESOLVED. Un-gradeable / malformed / known-defective / KNOWN_BAD = REJECTED → human bin, excluded from resolve/fail stats.
- **Coverage is a first-class failure.** A criterion with no proxy test routes to design-doc, not a pass.
- **Regression baseline is `$BASELINE_FAILS`, not assumption.** A test already red on clean base is NOT your regression — exclude it.
- **Never mutate the tree.** No `git stash`, no edits, no applying. Run the gate; classify; emit.
- **Route is load-bearing.** Criterion-unmet / regression → implement-spec · coverage hole → design-doc · KNOWN_BAD → none (human).

## Environment

- Repo in offline Docker container; reach via `box-sh '<cmd>'` (already `cd`s to repo root).
- Proxy gate file at `$PROXY_GATE_DIR` (persistent scratch, build-tools wrote it, implement-spec ran it).

## Input (from adapter)

- The design doc's acceptance criteria (the checklist to confirm).
- `$PROXY_GATE_DIR` — proxy gate location. Run that file directly. If driver reports it missing, reconstruct from criteria and note in graph (weakens chain of custody).
- `$BASELINE_FAILS` — set of existing-suite tests already failing on clean base.
- The implement-spec graph nodes.

## Output

Write `$VERDICT_FILE` (JSON):
```json
{
  "verdict":         "RESOLVED (proxy) | NOT_RESOLVED — <reason> | REJECTED — <reason>",
  "route":           "design-doc | implement-spec | none",
  "criteria":        { "1": "PASS", "2": "FAIL", "3": "NO-TEST" },
  "regressions":     [ "<test::name>" ],
  "coverage_holes":  [ <criterion-number> ]
}
```

Also print the same verdict/route on the last two lines of stdout (shim fallback). Append breakdown to the hypothesis graph.

## Process

### Phase 1 — Confirm the patch is live
`git diff --stat` (via box). If empty → `NOT_RESOLVED — empty patch`, `RE-ENTER: implement-spec`, stop.

### Phase 2 — Map criteria to proxy tests (coverage)
For each design-doc criterion: find the proxy test that checks it. A criterion with NO proxy test is a **coverage hole** → routes to design-doc.

### Phase 3 — Run gate + existing suite
- Run the proxy gate. Record each criterion's test as PASS / FAIL.
- Run the project's existing suite (`baseline_cmd` from manifest). A test newly failing is a **regression** ONLY if it is NOT in `$BASELINE_FAILS`. Pre-existing reds: exclude.

### Phase 4 — Classify & route

| Condition | Verdict | Route |
|---|---|---|
| Every criterion PASS, 0 regressions | `RESOLVED (proxy)` | `none` |
| Every criterion PASS, ≥1 regression | `NOT_RESOLVED — regressions` | `implement-spec` |
| ≥1 criterion FAIL | `NOT_RESOLVED — criterion unmet` | `implement-spec` |
| ≥1 criterion NO-TEST (coverage hole) | `NOT_RESOLVED — coverage hole` | `design-doc` |
| Empty patch | `NOT_RESOLVED — empty patch` | `implement-spec` |
| Task malformed / known-defective / KNOWN_BAD | `REJECTED — <reason>` | `none` |

**No-progress escalation:** a regression gets one narrow attempt at implement-spec. If it survives the narrow on the next round, route design-doc instead — the approach itself conflicts with existing behavior.

**Re-design override:** if implement-spec already flagged `DESIGN WRONG` in the graph for the failing criterion, route design-doc (not implement-spec) — the approach is wrong, not the implementation.

### Phase 5 — Emit
Print to stdout (last two lines are load-bearing — driver greps them):

```markdown
# Verify-spec: <task-id>

## Acceptance criteria
- criterion 1: PASS / FAIL / NO-TEST
- ...

## Regressions (excluding $BASELINE_FAILS)
- <test::name>: <error>   (or "none")

## Coverage holes
- criterion N   (or "none")

## Kill report (only if not RESOLVED)
<which criterion / which regression / which coverage-hole; the error; the implicated path>

VERDICT: <RESOLVED (proxy) | NOT_RESOLVED — <reason> | REJECTED — <reason>>
RE-ENTER: <design-doc | implement-spec | none>
```

## Notes
The captured-`$BASELINE_FAILS` discriminator is corpus-validated (HYPOTHESIS_GRAPH.md H₆ infrastructure): on httpx the clean-base suite already had 1 red (`test_write_timeout[trio]`); without exclusion, a naive verify would flag a phantom regression. The `(proxy)` qualifier is the entire honest signal — never round it up to grade-certainty.
