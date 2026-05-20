---
name: bug-hunt
description: Send independent adversaries on a bug hunt — a structural pass then a logic-tracing pass, from different model families, iterated to convergence (fix, re-hunt, repeat until zero new bugs). Falls back to a Sonnet adversary when external models are unavailable or contaminated.
argument-hint: [spec-file or scope description]
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Agent, AskUserQuestion
---

# Bug Hunt

Adversarial review by two independent adversaries, iterated to convergence. Independent Verification & Validation — the adversary has no stake in the implementation.

The **structural adversary** catches structural issues (missing baselines, overclaims, architectural gaps). The **logic adversary** catches logic bugs (inverted boolean conditions, decision tree errors, spec-to-code mismatches). Run the structural adversary to convergence first, then the logic adversary on its approved result. If the logic adversary finds bugs, fix and re-run the structural adversary to verify the fix didn't introduce regressions, then the logic adversary again. Converged = both approve with zero new findings.

**Adversary selection.** The adversary's value is independence: prefer different model families for the two passes (different priors catch different bugs; same-family review shares blind spots). For contamination-controlled work, the adversary must also be **cutoff-clean** relative to the system under review — a reviewer that post-dates the code could "know" the intended fix and leak it into the verdict.

**Fallback to Sonnet.** When external adversary CLIs are unavailable, OR when contamination control rules them out (frontier external models often post-date the system under review), fall back to a **Sonnet adversary** (Claude alone, pinned to a clean-cutoff Sonnet). Same-family review is weaker on diversity — flag that in the verdict — but it preserves cleanliness and availability. Two clean adversaries from different families is ideal; one clean adversary beats two contaminated ones.

## Input

One of:
- A spec file (e.g., `docs/agent-participation.md`) — the adversary reviews implementation against it
- A scope description (e.g., "the auth module") — the adversary reviews that code
- Nothing — the adversary reviews recent changes (`git diff main...HEAD`)

## Process

### 1. Scope — the diff defines the blast radius

Read the actual diff under review (`git diff main...HEAD`, or the specific fix being validated), not just the file names. The changed lines are the center; the **blast radius** is that code plus what it touches: callers of changed functions, code that reads state the diff now writes differently, and the control-flow paths the change newly reaches or newly skips. Scope the hunt to that radius.

Two in-scope finding types when validating a fix:
- **Regression** — behavior that worked before the diff and is now wrong.
- **Incompleteness** — the bug the diff targets isn't fully fixed (another path still exhibits it).

Out of scope: pre-existing bugs unrelated to the diff. Finding them neither validates nor invalidates the fix; note them separately if worth it, but don't chase them — that's scope creep that starves the verdict on the change.

(Two modes: **fix-validation** — a diff is under review, scope = blast radius, as above. **full-surface** — a spec or whole module is under review, scope = all of it. If a spec exists or no diff is given, you're in full-surface mode; otherwise fix-validation. The convergence note about "leaving scope" below applies only to full-surface.)

### 2. Hunt

Send the adversary on a bug hunt via stdin pipe. External adversary CLI:

```bash
cat <<'PROMPT_EOF' | <adversary-cli> -
<prompt here>
PROMPT_EOF
```

Sonnet-adversary fallback (external unavailable or contaminated): dispatch a subagent pinned to a clean-cutoff Sonnet (its own agent type), given the same prompt and the system-under-test access (e.g. via the project's shell helper), web tools disabled.

The prompt must include:
- The scope (which files to read)
- The spec (if one exists) — the adversary reads it, not us
- What to look for:
  - **Logic bugs** — race conditions, missing guards, wrong return types
  - **Spec violations** — does the code match the spec?
  - **Integration seams** — do components actually connect correctly? (topics, event names, data shapes, return type mismatches)
  - **Security** — token leakage, missing validation, bypass paths
  - **Edge cases** — what happens on disconnect, nick change, double revoke, etc.
  - **Common mode assumptions** — beliefs the spec and implementation share that might be wrong (Knight & Leveson's root cause for correlated failures in N-version programming)
  - **Resource cleanup** — do all lifecycle paths clean up state? (ETS, PubSub, monitors, timers)
- Output format: write findings to a file (e.g., `docs/bug-hunt.md` or append a new section)
- Instruction to run `mix test` / `npm test` / equivalent and report failures
- Instruction to write "Zero new bugs found. Hunt converged." if nothing found

### 3. Triage

Read the findings. For each bug:
- **Fix** if it's a real bug with clear impact
- **Defer** if it's a design decision or feature gap, not a bug — note it with rationale
- **Reject** if it's a false positive or re-report — don't fix

Ask the user before deferring anything severity:high.

### 4. Fix

Fix all accepted bugs. Run tests. Commit.

### 5. Re-hunt

Send the adversary again with an updated prompt that lists ALL previously found bugs (fixed and deferred) and instructs:
- Do NOT re-report anything from previous rounds
- Do NOT report deferred items
- Find NEW bugs only
- If zero: write convergence message

### 6. Repeat

Loop steps 3–5 until the adversary reports zero new bugs. That's convergence.

**Halt condition:** if the hunt hasn't converged after the fix-count stops decreasing for 3 consecutive rounds at the same count, halt and report to the user. The implementation may have structural issues the spec didn't anticipate.

## Prompt template

Round 1:
```
Bug hunt. Read [spec file] for the contract. Read [file list] for the implementation.

Find bugs: logic errors, spec violations, integration seams, security issues, edge cases, resource cleanup gaps, and common mode assumptions.

For each bug: describe it precisely, cite file and function, explain the impact, suggest a fix (don't fix it).

Write findings to [output file]. Run [test command] and report failures.

If zero bugs found, write: "# Bug Hunt Round 1\n\nZero new bugs found. Hunt converged."
```

Round N:
```
Bug hunt round N. Previous rounds found and fixed M bugs. Find NEW bugs only.

Previously found (do NOT re-report): [list all bugs from all rounds]
Intentionally deferred (do NOT report): [list deferred items]

If zero new bugs: write "# Bug Hunt Round N\n\nZero new bugs found. Hunt converged." to [output file]
```

## What makes this different from /codex

`/codex` is a single-pass review that reports feedback for the user to act on. `/bug-hunt` is a multi-pass adversarial loop that fixes bugs and re-hunts until convergence. The reviewer is independent (different model), the loop is automated, and the stopping criterion is empirical (zero new findings), not a fixed number of passes.

## Empirical notes

- Typical convergence: 3–10 rounds
- Bug counts decrease but not monotonically — fixes introduce new surface area
- Late rounds find concurrency races, resource leaks, error branch gaps, input validation edges
- The adversary will eventually leave scope to find bugs — in **full-surface** mode that's the convergence signal. In **fix-validation** mode it's the opposite: once findings leave the blast radius (pre-existing, unrelated bugs), the in-radius hunt has converged — stop, don't chase them.
- Common mode assumptions are the highest-value findings but the hardest to prompt for
