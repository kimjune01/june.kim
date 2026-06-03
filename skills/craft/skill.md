---
name: craft
description: Implementation phase for SWE-bench instances. You generate the patch from the recon handoff; a codex subagent challenges it; the gate arbitrates. Loops until FAIL_TO_PASS tests pass. On audit re-entry, narrows a fix that regressed. Stops when gate is green or the attempt budget is exhausted.
argument-hint: <instance-id>
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Craft: Patch Implementation for Bench

Take the recon diagnosis, draft the fix, let codex challenge it, loop on gate feedback. The fix is done when the gate says the FAIL_TO_PASS tests pass — not when your reasoning says so, and not when codex is satisfied.

**You generate, codex filters, the gate arbitrates.** Never reverse those roles. You hold the tools (box helper, gate) and the recon context; codex is a fresh-eyes adversary with no memory of the diagnosis, so it catches the leaps you can't see. The gate is the final word over both of you.

## Environment

Code lives in an offline Docker container, reached only through the helper the adapter names (e.g. `box-sh '<cmd>'`). The helper already `cd`s to the repo root — **do not prepend `cd`**; run commands from root. Edit files through the helper (sed/python3/patch inside it).

Run the gate with the helper the adapter names (e.g. `gate`) — it runs the project's official test command and prints the result for the FAIL_TO_PASS tests. **Gate is the arbiter. Your analysis of the code is not.**

`codex` runs locally (it is NOT in the offline container — it cannot read the repo or run the gate). You bridge it: pull the relevant file contents via the box helper, paste them into the codex prompt, get its critique, and you apply and gate the result. No internet, no `gh` otherwise — implement from the recon diagnosis alone.

## The codex volley (craft's adversary)

codex is the structural filter on your patch. Send it the failing test, the recon root cause, and your proposed diff; ask what's wrong. Pipe via stdin to avoid quoting issues:

```bash
cat <<'PROMPT_EOF' | codex exec -
This patch is meant to make a failing test pass without breaking others. Be direct — what's wrong, what's missing, what breaks. No preamble.

FAILING TEST (must pass):
<test source>

RECON ROOT CAUSE:
<one paragraph from the handoff>

RELEVANT SOURCE (current, from the repo):
<file contents you pulled via the box helper>

PROPOSED DIFF:
<your unified diff>
PROMPT_EOF
```

Rules of the volley:
- **You draft first.** codex reviews a concrete diff, not an empty prompt. Don't ask codex to write the fix from scratch; ask it to break the one you wrote.
- **Fold in what's load-bearing, gate the rest.** codex's structural catches (missed call site, wrong branch, broken invariant) are cheap to act on. Don't chase stylistic notes. When you and codex disagree, the gate settles it — run it.
- **Always volley — before the first gate run, and again on every gate failure.** Don't gate a fix codex hasn't seen, and don't revise after a failure without showing codex the gate output. A clean codex pass before gating saves a wasted cycle; a codex read of any gate failure narrows the cause. codex sees every diff and every red gate, not just the ones that puzzle you.
- **codex is a filter, not an oracle.** It has no access to the container and no memory of recon. A codex "looks good" is not resolution — only the gate is. One volley per gate attempt (plus the pre-gate draft review); the content converges in 2-3 rounds (see [the volley](https://june.kim/volley)), so later rounds are mostly confirmation.

## Input

The recon handoff — provided **inline in the adapter prompt** (the driver injects it). Extract:
- The root cause + edit sites (recon's primary diagnosis)
- Any **competing hypotheses** (recon couldn't decide between two explanations and left them for you to resolve against the gate)
- Open questions

If the handoff has a competing-hypotheses section, those edit sites are *hypotheses*, not facts. Try the cheapest decisive one first; the gate outcome tells you which branch was right.

Also given: the FAIL_TO_PASS list, and on re-entry an AUDIT KILL REPORT.

## Output

Container edits that persist for /audit (same container). The driver captures `git diff` at the end — your job is to leave the working tree in the fixed state. Append your gate-loop nodes to the hypothesis graph the adapter names.

## Process

### Phase 1: Read the handoff

Read the inline handoff. If an edit site is ambiguous, read the file via the box helper and resolve before editing. Do not implement against ambiguity — resolve first. For competing hypotheses, pick the cheapest one to test first.

### Phase 2: Enumerate before editing

For every edit site, confirm location: `grep -rn "<pattern>" .`. Code may differ from what recon described; if so, re-read and update your plan.

**Enumerate-before-applying:** any substitution (rename, replace, API change) at N locations — grep to find all N, apply in one pass, grep again to confirm zero remaining.

### Phase 3: Draft, volley, apply

1. **Draft** the minimal fix for every edit site recon named, as a unified diff. "Minimal" = the smallest change that makes FAIL_TO_PASS pass without breaking existing tests.
   - Do not: add features, refactor unrelated code, add error handling for impossible scenarios, add comments explaining what the code does.
   - Do: cover exactly the edit sites; handle every location grep found.
2. **Volley** the drafted diff with codex (see "The codex volley" above) before touching the container. Fold in the load-bearing catches.
3. **Apply** the revised diff to the container via the box helper.

### Phase 4: Gate loop

Run the gate.

**If gate passes:** stop — the working tree is the output. (A green gate ends the loop even if codex still has notes — the gate outranks codex.)

**If gate fails:** read the output and classify the trajectory (the e-value shape names your next move):

| Gate trajectory | Meaning | Next move |
|---|---|---|
| **Convergent (stuck)** | same error persists | the fix isn't reaching the right path — was the edit too shallow? wrong file? |
| **Divergent (progress)** | error changed, points at the real problem | follow the new evidence — you're closer |
| **Oscillatory (regression)** | a previously-passing test now fails | the fix is too broad — narrow it |
| Compile/syntax error | mechanical | fix and re-run |

Volley every gate failure with codex (paste the gate output + current diff, ask why it fails) before revising. Then revise and re-run. **Max 8 gate iterations.** If you exhaust them without green, leave the best partial fix in the tree and note the last gate failure in the graph document.

### Phase 5: Reopen recon when the hypothesis is wrong

If after **3 gate iterations** the same error persists (convergent-stuck) and the root cause looks different from what recon said, stop implementing. Write `HYPOTHESIS WRONG: <what the gate evidence actually points at>` to the graph document and print `NOT-RESOLVED — re-diagnose`. The driver routes this back to recon rather than letting you burn the remaining budget on a wrong diagnosis.

## Audit re-entry (narrow mode)

When the adapter includes an **AUDIT KILL REPORT** flagging a **PASS_TO_PASS regression** (FAIL_TO_PASS already pass, but the fix broke something), recon was right — the fix is just too broad. Do NOT re-diagnose:

1. Read which PASS_TO_PASS test regressed and its error.
2. Find the part of your fix that touches that test's code path. The regression is oscillatory evidence: your change has two modes, one helps, one hurts.
3. Narrow the fix so it addresses the FAIL_TO_PASS path without touching the regressed path (guard the condition, scope the change tighter).
4. Run gate. The contract is BOTH: FAIL_TO_PASS pass AND the regressed test passes again.

## Rules

- **Gate is the arbiter.** "I believe the fix is correct" is not a stopping condition, and neither is "codex approved." Gate green is.
- **You generate, codex filters.** Never reverse: don't have codex write the patch and yourself rubber-stamp it. You hold the recon context and the tools; codex breaks your draft.
- **Resolution is the FAIL_TO_PASS tests, not tests you choose.** Run the gate, not a test you picked.
- **No scope creep.** Touch only the edit sites recon named, plus locations the enumerate step found.
- **Competing hypotheses are tested, not stacked.** When recon left two options, validate against the gate cheapest-first — don't apply both branches at once.
- **8 gate iterations max**; re-diagnose handoff at 3 if stuck on a wrong hypothesis.
- **Append the graph, never truncate.** Your gate-loop nodes are part of the crash-recovery trail.
- **Leave the tree fixed.** The driver captures `git diff` — the working tree state IS your output.
