---
name: bug-hunt
description: Send codex on an adversarial bug hunt. Runs to convergence — fix, re-hunt, repeat until zero new bugs. Draws on avionics IV&V practices.
argument-hint: [spec-file or scope description]
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Agent, AskUserQuestion
---

# Bug Hunt

Adversarial review by codex (GPT-5.4), iterated to convergence. Independent Verification & Validation — the reviewer has no stake in the implementation.

## Input

One of:
- A spec file (e.g., `docs/agent-participation.md`) — codex reviews implementation against it
- A scope description (e.g., "the auth module") — codex reviews that code
- Nothing — codex reviews recent changes (`git diff main...HEAD`)

## Process

### 1. Scope

Identify the files under review. If a spec exists, read it. If reviewing recent changes, run `git diff --name-only main...HEAD` to find touched files.

### 2. Hunt

Send codex on a bug hunt via stdin pipe:

```bash
cat <<'PROMPT_EOF' | codex exec --full-auto -m gpt-5.4 -
<prompt here>
PROMPT_EOF
```

The prompt must include:
- The scope (which files to read)
- The spec (if one exists) — codex reads it, not us
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

Send codex again with an updated prompt that lists ALL previously found bugs (fixed and deferred) and instructs:
- Do NOT re-report anything from previous rounds
- Do NOT report deferred items
- Find NEW bugs only
- If zero: write convergence message

### 6. Repeat

Loop steps 3–5 until codex reports zero new bugs. That's convergence.

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
- Codex will eventually leave scope to find bugs — that's the convergence signal
- Common mode assumptions are the highest-value findings but the hardest to prompt for
