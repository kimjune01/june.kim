---
name: ship
description: Create PRs from dripped entries. Human-gated. Only runs when invoked or when sweep is not in dry mode.
argument-hint: [<repo>] [--list] [--all]
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Ship: PR Creation

Take `dripped` entries (quality gates passed) and create PRs. This is the only skill that runs `gh pr create`. Everything upstream is autonomous; this step is human-gated.

## Why

The pipeline runs while you sleep. Gates pass, branches get validated, entries accumulate as `dripped`. Nothing goes public until you say so. `/ship` is the publish button.

## Monoidal contract

| Input | Output | Valid alone? |
|-------|--------|--------------|
| Dripped entries (JSONL) | PRs created | Yes — ships from any dripped source |

**Identity:** ship on a queue with no `dripped` entries is a no-op.

**Composition:** `ship; ship = ship` — idempotent. Already-shipped entries stay shipped.

**Pipeline composition:** `ship(drip(triage(repo)))`. Drip gates; ship publishes. Each is idempotent. The queue file is the checkpoint.

## Commands

### (no argument)

Ship the next `dripped` entry across all repos, respecting org gate (1 per org).

### `<repo>`

Ship the next `dripped` entry for a specific repo.

### `--list`

Show all `dripped` entries ready to ship. For each: repo, branch, issue, gate verdicts.

### `--all`

Ship all `dripped` entries that pass the org gate. Use when you're watching and want to flush the queue.

## Process

1. **Preflight.** `gh auth status`. Fail fast on auth issues.
2. **Read drip queues.** Scan `~/.sweep/drip-queue/*.jsonl` for entries with status `dripped`.
3. **Org gate.** For each dripped entry, check if the org already has a shipped PR open. If so, skip (report as org-blocked). `max_open_per_org` defaults to 1.
4. **Repo status gate (hard block).** Run `~/.sweep/bin/repo-status <owner/repo>`. If verdict is not `"clear"`, skip immediately. Do not create PR. Covers denylist, permanent eviction, cooldown, and rejection cooldown in one call. Learned from immich#28375/28377 — shipped twice to an evicted repo.
5. **AI policy check (hard block).** Run `~/.sweep/bin/ai-policy <owner/repo>`. If `detected: true`, evict the repo and skip. Checks CONTRIBUTING.md, AGENTS.md, and org-level `.github` files. This is the last line of defense — actionable and triage should have caught it, but ship verifies.
6. **Banlist (enforced by hook, not by ship).** `~/.sweep/banlist.txt` is checked by the `gate-pr-create.sh` PreToolUse hook. If the repo is banned, `gh pr create` is blocked at the system level. Ship doesn't need to check — the hook is the enforcement. But ship should still skip banned repos early to avoid wasting time on push + gate file prep.
6. **Verify gate attestation.** Load `~/.sweep/gates/<owner>-<repo>.gate`. Check:
   - `codex_verdict` is `"pass"`
   - `test_attestation` is present and non-empty
   - If any field is missing, empty, or not `"pass"`: mark entry back to `triaged` in the drip queue (so `/qa` and `/drip` re-run on the next tick), log the reason, skip. This is the feedback loop: ship validates what drip stamped.
5. **Create PR.**
   - Read the PR title and body from the gate attestation file (drip wrote them during the gate sequence).
   - `gh pr create --repo <repo> --title <title> --body <body> --head <user>:<branch>`
   - Update entry: status -> `shipped`, shipped_at -> now, pr_number -> result.
6. **Report.** What was shipped, what was sent back to drip, what's org-blocked.

## Rules

- **Human-gated.** Ship only runs when the user invokes it, or when sweep is running without `--dry-run`.
- **Org gate still applies.** One open PR per org at a time. Ship respects the same pacing as drip.
- **No quality gates.** Those already ran in `/drip`. Ship trusts the gate attestation file.
- **Fork only.** PRs are created with `--head <user>:<branch>`. Never push to upstream.
- **Idempotent.** Running `/ship` twice ships at most one entry per org per run.
- **Gate file required.** No gate attestation file = no PR. The attestation is the proof that drip ran.

## Failure behavior

- **Auth fails:** stop immediately, report.
- **Gate file missing or incomplete:** mark entry back to `triaged`, report. `/qa` and `/drip` re-run on the next tick.
- **PR creation fails (permissions):** mark `status: "error"`, report the `gh` error. Don't retry.
- **Branch not on fork remote:** skip, report. Drip should have pushed it.
- **Org-blocked:** skip, report which org and which PR is blocking.

## Integration with sweep

Sweep's `--dry-run` flag controls whether ship runs on the pipeline tick:
- `--dry-run` (or sleeping mode): pipeline tick runs drip but skips ship. Entries accumulate as `dripped`.
- No flag (active mode): pipeline tick runs both drip and ship. Entries flow through automatically.

The user can always run `/ship` manually regardless of the sweep mode.
