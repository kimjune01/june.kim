---
name: audit
description: Verification phase for SWE-bench instances. Runs the full test suite on the craft patch, classifies regressions against the captured fail-on-base baseline, and emits a verdict plus a re-entry route for the outer loop.
argument-hint: <instance-id>
allowed-tools: Read, Grep, Glob, Bash
---

# Audit: Regression Verification for Bench

Run the full gate. Classify every failure. Return a verdict and a route. No edits — audit never mutates the tree.

Audit is the kill condition for the outer loop. When the patch isn't RESOLVED, the *shape* of the failure decides where the pipeline re-enters: a wrong diagnosis goes back to /recon, an over-broad fix goes back to /craft. Audit's job is to classify that shape correctly.

## Environment

Code lives in an offline Docker container (the craft edits are already live in the working tree). Reach it through the helper the adapter names (e.g. `box-sh '<cmd>'`); it already `cd`s to the repo root — **do not prepend `cd`**.

Run the full gate with the helper the adapter names (e.g. `gate`). **The gate is the arbiter. Audit interprets its output; it does not overrule it.**

## Input

From the adapter:
- The FAIL_TO_PASS and PASS_TO_PASS lists.
- The **fail-on-base capture** — the test output the driver recorded by running the suite on the *unpatched* repo before any edits. This is your baseline for "pre-existing failure." **You do not run `git stash`** — the baseline is already captured, and stashing risks stranding craft's edits before the driver captures the patch.

## Output

A verdict and a route, printed to stdout. Append the breakdown to the hypothesis graph the adapter names.

## Process

### Phase 1: Confirm the patch is live

```
git diff --stat
```

If empty, craft left no edits — emit `NOT_RESOLVED — empty patch` / `RE-ENTER: craft` and stop. Do NOT apply anything yourself; audit never mutates the tree.

### Phase 2: Run the gate

Run the gate. Record the output. If the gate truncates (it tails its output), and a PASS_TO_PASS result you need is past the cut, run that specific test through the box helper to see its status — but never stash or edit.

### Phase 3: Classify each result against the baseline

For every test in the gate output:

1. **In FAIL_TO_PASS?** It must now PASS. If it FAILs, the fix didn't solve the problem.
2. **In PASS_TO_PASS and now failing?** Check the fail-on-base capture:
   - Failing on base too → **pre-existing**, not counted against the fix.
   - Passing on base, failing now → **regression** introduced by the patch.
3. Any other failure: cross-check the base capture the same way — pre-existing if it was already red.

Classify each failing test as `FAIL_TO_PASS still-failing`, `PASS_TO_PASS regression`, or `pre-existing (not counted)`.

### Phase 4: Verdict + route

| Condition | Verdict | Route |
|---|---|---|
| All FAIL_TO_PASS pass, 0 regressions | `RESOLVED` | `RE-ENTER: none` |
| All FAIL_TO_PASS pass, 1+ regressions | `NOT_RESOLVED — regressions` | `RE-ENTER: craft` |
| Some (not all) FAIL_TO_PASS pass | `PARTIAL` | `RE-ENTER: recon` |
| 0 FAIL_TO_PASS pass | `NOT_RESOLVED — fix ineffective` | `RE-ENTER: recon` |
| Empty patch | `NOT_RESOLVED — empty patch` | `RE-ENTER: craft` |

Routing rationale (the outer loop):
- **Regression-only** → recon was right, the fix is too broad. Send a kill report to /craft (narrow mode) — don't pay to re-diagnose.
- **Ineffective / partial** → the diagnosis missed the real path. Send the failing-test evidence to /recon as a new H₀.

**No-progress escalation (harness-enforced).** A regression gets at most ONE narrow attempt. If you route `craft` again on the *next* round (the regression survived the narrow), the driver overrides the route to `recon` and re-diagnoses — a regression that can't be narrowed away means the approach itself conflicts with the P2P test, so grinding `craft` would just retry the same edit. You still emit the honest `RE-ENTER: craft` for a regression; the driver decides when a repeat means "re-diagnose instead."

### Phase 5: Emit

Print, with the verdict and route each on their own final lines so the driver can parse them:

```markdown
# Audit: <instance-id>

## FAIL_TO_PASS
- test: PASS / FAIL

## PASS_TO_PASS regressions
- test: <error>   (or "none")

## Pre-existing (not counted, confirmed against base capture)
- test   (or "none")

## Kill report (only if not RESOLVED — this routes the outer loop)
<for RE-ENTER: recon — which FAIL_TO_PASS still fails, the error, the code path it implicates>
<for RE-ENTER: craft — which PASS_TO_PASS regressed, its error, which part of the diff likely caused it>

VERDICT: <RESOLVED | NOT_RESOLVED | PARTIAL>
RE-ENTER: <recon | craft | none>
```

Append the same breakdown to the hypothesis graph document (never truncate it).

## Rules

- **Gate is the arbiter.** If the gate says a test failed, it failed. No editorializing.
- **Never mutate the tree.** No `git stash`, no `git apply`, no edits. The driver captures the patch after you; a stash that fails to pop would strand the fix. Classify pre-existing failures against the provided base capture, not by re-running on a stashed tree.
- **RESOLVED requires the full contract.** All FAIL_TO_PASS pass AND zero PASS_TO_PASS regressions. Both.
- **The route is load-bearing.** Misrouting a regression to recon (or an ineffective fix to craft) wastes an outer-loop iteration. Classify the failure shape, then route.
- **No silent partial credit.** PARTIAL is distinct from RESOLVED — never round up.
- **Verdict and route on their own lines.** The driver greps the last `VERDICT:` and `RE-ENTER:` lines.
