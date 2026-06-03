---
name: attest
description: Behavioral gate split out of /qa. Runs fail-on-master/pass-on-fix, routes the card by verdict, and uses the kanban trail to decide 1st-fail (→ investigate) vs 2nd-fail (→ human). Hides the test gate from qa so adversarial pride can't tangle with "did the fix work?"
argument-hint: <repo> [--branch BRANCH]
allowed-tools: Read, Write, Bash
---

# Attest

Verify the fix branch actually fixes the bug. Route the card downstream by outcome. Stop.

The skill is thin because the work is deterministic — `sweep` already owns `test_attestation` (fail-on-master, pass-on-fix). attest's job is *routing*, not LLM-shaped review. qa is the adversarial reviewer; attest is the gate.

## Why split this out of qa

[Hide the gate from the producer](../bbe59971) — pride is the failure mode. qa's identity is "I find structural and logic bugs." When qa also owned the test attestation, qa had a stake in the test outcome. Splitting attest out means qa receives a card that **already passed** the behavioral gate; qa can only opine on code quality, not on whether the fix works. Same shape as hiding attestations from the issue's reporter.

## OTP shape

```
investigate.jsonl → [investigate-actor]
                         |
                  produces fix branch
                         |
                         v
                  attest.jsonl → [attest-actor] ─ pass ─→ qa.jsonl
                         ^                       │
                         |                       ├─ fail (1st) ─→ investigate.jsonl
                         └──── retry ────────────┘
                                                 └─ fail (2nd) ─→ human.jsonl
```

WIP=1, SkillActor (parameterized on `attest_cycle`). No new workflow class.

## Monoidal contract

| Input | Output | Valid alone? |
|-------|--------|--------------|
| `Message{repo, branch, payload, path}` on `attest.jsonl` | `GateAttestation` artifact on disk + one routed message (qa / investigate / human) | Yes — given a worktree, deterministic |

- **Identity:** empty inbox → no-op.
- **Composition:** `attest(attest(card))` for the same `(branch, worktree HEAD)` produces the same `attestation_hash`. The test runs once per (branch, SHA); a re-run with no commit movement reuses the cached artifact.
- **Preconditions:** `msg.repo` and `msg.branch` set. Worktree resolvable via `ensure_worktree`. `infer_test_cmd` returns a non-empty command for the repo.
- **Postconditions:** routed message lands on exactly one downstream inbox. On `pass`, downstream message payload carries `attestation_hash`. On `fail`, downstream message payload carries `attest_failure_reason` (stderr tail).

## 1st-fail vs 2nd-fail — kanban-as-counter

The `Message.path` field is the trail of senders this card has passed through. Each actor that forwards a card sets `new.path = incoming.path + [incoming.sender]`. So if attest is about to process a card whose path already contains `"attest"`, this is at least the second time attest is seeing this card's lineage.

```python
second_look = msg.path.count("attest") >= 1
```

- First look + fail → `investigate.jsonl` (one cheap LLM retry; the bounce-back carries the failure stderr in `payload.attest_failure_reason` so investigate isn't blind)
- Second look + fail → `human.jsonl` (operator decides: scrap, redirect, or hand-fix)

No per-card counter. No cross-inbox reads. The kanban remembers.

## What attest does NOT do

- Adversarial code review. (`/qa` does, downstream, on the `pass` path only.)
- Decide whether the failure is "test wrong" vs "fix wrong" — that's investigate's job on the retry. attest just routes.
- Re-run the test on the qa side. (qa today still re-runs `test_attestation` as a defensive double-check; the `attestation_hash` in the payload is forwarded for future hash-based skip. Optimization, not correctness.)
- Halt the actor on a genuine `test_fails_on_fix`. That's a routable verdict. Halt is reserved for broken substrate (missing toolchain, master test passing, git checkout failure).

## CLI

The harness owns the loop. Standalone invocation for debugging:

```bash
sweep attest run --repo owner/repo --branch fix-xyz
```

Equivalent to depositing one card on `attest.jsonl` and waiting for the actor to process it.

## Output contract

`attest_cycle` returns:

```json
{
  "verdict":   "pass | fail",
  "target":    "qa | investigate | human",
  "second_look": false,
  "attestation_hash": "sha256...",  // only when verdict=pass
  "msg_id":    "..."
}
```
