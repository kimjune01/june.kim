---
name: qa
description: Adversarial code review on a single fix branch — codex (structural) and gemini (logic) volley until convergence or budget. The harness picks the entry, runs the test attestation, and records the verdict; the skill only does the LLM-shaped review.
argument-hint: <repo> [--entry BRANCH] [--budget SECONDS] [--dry-run]
allowed-tools: Read, Write, Edit, Bash, Glob, Skill
---

# QA: Adversarial Code Review

You were invoked by the harness with a prompt describing what to review and a fix branch checked out in a worktree. Run codex (structural) and gemini (logic) as adversarial reviewers on the diff. Report verdicts. Stop.

The harness owns everything that isn't LLM-shaped: queue state, schema, entry selection, idempotency, budget timing, status appends, gate validation, resume after timeout. Don't reimplement it in this skill. The CLI is the contract.

## The CLI is the harness

| What you need | How to get it |
|---|---|
| Diff and branch context | The harness has already checked out the branch in `$worktree`. `git diff` against base. |
| Test attestation (fail-on-master / pass-on-fix) | `sweep qa test --repo … --branch … --worktree … --test-cmd …` |
| Run one codex round | `sweep qa codex --repo … --branch … --worktree …` |
| Run one gemini round | `sweep qa gemini --repo … --branch … --worktree … --round N` |
| End-to-end on one entry (no Temporal) | `sweep qa full --repo … --branch … --worktree … --test-cmd …` |
| Record the verdict | The composer (`qa_one_entry` / `sweep qa full`) writes the gate line. Don't append jsonl by hand. |

If a CLI call rejects your input, **read the error and fix the input** — don't paper over it in the skill prompt. That's the [skills-lack-determinism](https://june.kim/skills-lack-determinism) loop: deterministic guardrails return useful errors, the agent closes the loop. If the error reveals a missing CLI affordance, add it to `sweep qa` rather than encoding the workaround here.

## The LLM-shaped part

What the skill actually contributes — the part the CLI can't do — is framing the two reviewers and reading their verdicts.

**Codex (structural):**
> Review this fix as a maintainer of `<repo>` seeing it for the first time. Find structural problems: missing edge cases, wrong abstractions, scope creep, hidden coupling, missed invariants. Don't comment on style. Verdict: `pass` / `reject` / `revise`. If `revise`, list specific changes.

**Gemini (logic):**
> Trace the logic in this diff. Find: inverted boolean conditions, off-by-one errors, missed branches, race conditions, type confusions. The fix must be correct, not just plausible. Verdict: `pass` / `reject` / `revise`.

Round loop, per reviewer:
- `pass` → done.
- `revise` → apply codex's revise suggestions (auto), surface gemini's revise notes (don't auto-apply — gemini is better at logic traces than rewrites). Re-run test attestation. Re-send.
- `reject` → stop the loop for that reviewer, continue the other.

Convergence: stop on `pass`, on round 3, or when the harness signals budget. The composer records the final verdict; the skill doesn't write jsonl.

**Both reviewers see the same diff.** Don't shape the prompt to one model's strengths — the point of two reviewers is independent blind spots.

**Never edit the diff to satisfy a reviewer if it changes the issue's intent.** A reviewer asking for a change the issue's commenter didn't ask for is scope creep; surface it to the human, don't fold it in.

## Fallback when codex is unavailable

If `sweep qa codex` returns a credit/quota error, fall back to an Opus subagent playing the structural-reviewer role with the same framing. The composer records `codex_provenance: "opus-fallback"` so the retro can separate real-codex outcomes. Codex credits restore 2026-05-17; remove this path after retro confirms parity.

If gemini is stubbed (no subscription), the composer records `gemini_first/last = "stubbed"`. The downstream hook will block the PR — that's the contract, not a bug to work around.

## What this skill does not do

- Pick the next entry. (`sweep` does — the skill is handed one.)
- Read or write the drip-queue jsonl directly. (The composer does.)
- Decide whether to ship. (`/drip` does, downstream.)
- Create PRs. Ever. (Hooks will block; only `/drip` creates PRs.)
- Manage WIP, budget, takt, idempotency, resume. (Harness concerns. If you need to influence them, add a CLI flag, don't write rules in this file.)

## Standalone use

The CLI is the interface. Any process that calls `sweep qa full` (or composes `sweep qa test` + the codex/gemini steps) substitutes for this skill. Manual reviewers, external CI signals, alternative reviewer pairs all plug into the same composer.

## Output contract (machine-readable, REQUIRED)

After all narration, the **last printed line** must be a single JSON object matching this schema:

```json
{
  "verdict":       "pass | fail | needs_human",
  "issues_found":  [],
  "reason":        "short string, ≤200 chars",
  "rejected":      false,
  "reject_reason": null
}
```

`verdict=pass` means both adversaries converged on "ship it" and the test attestation is intact. `fail` means at least one substantive bug found that blocks. `needs_human` means non-substantive concerns that need operator judgment (maintainer-style mismatch, ambiguous bug). `issues_found` is an array of short strings; empty when verdict=pass.

Set `rejected=true` with a `reject_reason` when QA cannot run (missing worktree, unrunnable tests, broken branch — distinct from "tests failed," which is `verdict=fail`). Rejected jobs route to `~/.sweep/inbox/rejected.jsonl` for operator review.

Print the JSON as the literal last line, no trailing prose, no markdown fence.
