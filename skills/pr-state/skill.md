---
name: pr-state
description: Read GitHub for live PR state, classify each open authored PR, and deliver one message per PR to the matching downstream actor's inbox (qa, investigate, drip, retro). OTP-style routing — pr-state is the dispatcher.
argument-hint: [--repo owner/repo] [--from-queue] [--limit N] [--bucket NAME] [--dry-run]
allowed-tools: Read, Write, Bash, Glob
---

# PR State

Read every open PR you've authored from GitHub, classify each into the next-action bucket, and write one message per PR to the matching downstream actor's inbox.

## OTP framing

Each skill in the pipeline is an actor with a mailbox. The mailbox is an append-only JSONL file at `~/.sweep/inbox/<actor>.jsonl`. The actor reads its mailbox on each takt and processes one message (WIP=1).

`pr-state` is the **dispatcher** between GitHub (the world) and the pipeline (the actors). It has no inbox of its own — its input is `gh`. Its output is N inboxes.

```
GitHub (gh)
   |
   v
[ pr-state ] --classify--> [ qa.inbox ]          --> /qa takt
                       \-> [ investigate.inbox ] --> /investigate takt
                       \-> [ drip.inbox ]        --> /drip takt
                       \-> [ retro.inbox ]       --> /retro batch (no-op messages go here for the audit trail)
```

The actor never reaches into another actor's state. Skills communicate only by appending to mailboxes.

## Monoidal contract

| Input | Output | Valid alone? |
|-------|--------|--------------|
| `gh` open-PR set (live) + optional drip-queue context | `~/.sweep/pr-state.jsonl` snapshot per PR + `~/.sweep/PR_STATE.md` rendered punch list | Yes — read-only classifier, no state mutated upstream |

**Identity:** if no open PRs match the filter, write a snapshot saying so and exit. No-op on empty input.

**Composition:** `pr-state(pr-state(x)) == pr-state(x)` for the same live `gh` state. The classifier is a pure function of (gh response, drip-queue state, clock). Repeat invocations within the same minute produce identical classifications.

**Preconditions:** `gh auth status` passes. `~/.sweep/drip-queue/` may or may not exist — pr-state degrades gracefully without it.

## Buckets

Each PR lands in exactly one bucket. Order matters: the first matching rule wins.

| Bucket | Trigger | Next action |
|--------|---------|-------------|
| **close** | Competing PR merged (`superseded`), or maintainer review state is `CHANGES_REQUESTED` with explicit close-this-PR language in the latest review body, or our drip-queue entry has `status: "superseded"` | Human reviews, decides to close. Never auto-closes (see rule below). |
| **investigate** | `reviewDecision == "CHANGES_REQUESTED"`, or maintainer left a comment with a question (`?` in body, `authorAssociation` is `MEMBER`/`OWNER`/`COLLABORATOR`) and we haven't replied since | Spawn `/investigate` or address manually. |
| **rebase** | `mergeable == "CONFLICTING"`, or PR base branch advanced > 50 commits since PR head's merge-base | `git pull --rebase`, force-push, re-trigger CI. |
| **qa** | Any CI check has `conclusion == "FAILURE"`, or our gate attestation is missing/older than 24 h while PR is still open | Re-run `/qa` on the entry. |
| **ship** | `reviewDecision == "APPROVED"` + `mergeable == "MERGEABLE"` + all CI checks `SUCCESS` + no open conversations | Maintainer can merge. Optional ping after 48 h of inactivity. |
| **wait** | None of the above — recently opened (< 24 h), no maintainer activity yet, CI green or pending | No action. The world hasn't responded yet. |

**Tie-breakers between buckets** (in priority order, stop at first match):

1. **close** (terminal state — overrides everything)
2. **investigate** (reviewer is asking something — answer first)
3. **rebase** (mechanical block — fix before anything else)
4. **qa** (our gate failed — re-verify before pinging)
5. **ship** (ready)
6. **wait** (default)

If the bucket is ambiguous (e.g., approved but CI failing), the higher-priority bucket wins. CI failing on an approved PR → **qa**, not **ship**.

## Input

- (no args) — classify every open PR authored by the current GitHub user across all repos.
- `--repo owner/repo` — classify only this repo's open PRs.
- `--from-queue` — classify only PRs referenced in `~/.sweep/drip-queue/*.jsonl` with `status: "open"`. Use when you only care about the pipeline's PRs, not manual ones.
- `--limit N` — cap the number of PRs fetched (default 50, max 200).
- `--bucket NAME` — after classification, print only PRs in this bucket. `--bucket close` is the common one.

## Routing — bucket → inbox

Each bucket has a single destination. pr-state appends one message per classified PR to the destination mailbox. Bucket and inbox are not the same axis — `close` and `ship` both route to drip because drip is the actor that handles "advance an open PR's status."

| Bucket | Destination inbox | Message intent |
|--------|-------------------|----------------|
| **close** | `~/.sweep/inbox/drip.jsonl` | "this PR should be closed — competing PR merged or maintainer asked" |
| **investigate** | `~/.sweep/inbox/investigate.jsonl` | "a reviewer is asking a question — read it, decide a response" |
| **rebase** | `~/.sweep/inbox/drip.jsonl` | "this PR needs a rebase against base before anything else can happen" |
| **qa** | `~/.sweep/inbox/qa.jsonl` | "gates are stale or CI failed — re-attest" |
| **ship** | `~/.sweep/inbox/drip.jsonl` | "approved + green — maintainer can merge; optional ping after 48 h" |
| **wait** | `~/.sweep/inbox/retro.jsonl` | "no action; audit trail only" |

The intent field in each message names what the receiver should do:

```jsonl
# ~/.sweep/inbox/qa.jsonl (appended by pr-state)
{"ts":"2026-05-14T17:45:00Z","from":"pr-state","intent":"reattest","repo":"sharkdp/bat","pr":3734,"branch":"zsh-color-never","signals":{"ci":"failing","check":"Test stable on windows-latest"},"reason":"CI failure on windows","msg_id":"prstate-2026-05-14T17:45:00Z-sharkdp-bat-3734"}

# ~/.sweep/inbox/drip.jsonl
{"ts":"...","from":"pr-state","intent":"close","repo":"hyperium/hyper","pr":4002,"reason":"superseded by #4067","msg_id":"..."}
{"ts":"...","from":"pr-state","intent":"ship","repo":"hyperium/hyper","pr":4068,"reason":"approved + green CI","msg_id":"..."}

# ~/.sweep/inbox/investigate.jsonl
{"ts":"...","from":"pr-state","intent":"respond","repo":"...","pr":...,"reviewer":"...","comment_url":"...","reason":"maintainer asked a question","msg_id":"..."}
```

**Mailbox contract:**
- Append-only. Receivers read latest-per-`msg_id`; senders never edit.
- `msg_id` is `<sender>-<ts>-<repo-slug>-<pr>` — deterministic, deduplicates re-sends.
- `from` names the sender actor. The receiver uses it to route audit/retro records.
- `intent` is the action verb. Each receiver advertises which intents it consumes (e.g., qa consumes `reattest`).

**Idempotence:** if pr-state runs twice in the same minute, the second run produces messages with the same `msg_id` (the `ts` is rounded to minute, not second, for snapshot stability). Receivers MUST dedupe on `msg_id` — first delivery wins, subsequent ones are no-ops. This is the OTP "at-least-once delivery, idempotent receiver" pattern.

**Receiver ack (optional, recommended):** when an actor processes a message, it appends `{"ts":"...","from":"qa","intent":"ack","msg_id":"...","outcome":"..."}` to `~/.sweep/inbox/_acks.jsonl`. pr-state and retro read acks for backpressure and post-mortem. No ack = receiver is down or the message is unprocessable; surface to human.

## Snapshot (human-readable view)

In addition to delivering to inboxes, pr-state writes one snapshot for humans:

`~/.sweep/PR_STATE.md` — rendered from the same classifications. Rebuilt every run.

```markdown
# PR State — 2026-05-14 17:45 UTC

## close (1) → drip
- hyperium/hyper#4002 — superseded by #4067 (merged 2026-05-13)

## investigate (3) → investigate
- sharkdp/bat#3734 — windows test failing on edge case "color=never with explicit decorations"
- ...

## qa (2) → qa
## rebase (0) → drip
## ship (5) → drip
## wait (11) → retro (audit only)
```

The snapshot is a courtesy render. The mailboxes are the contract. If the snapshot is stale, the mailboxes are still authoritative.

## Process

### 1. Preflight

1. `gh auth status` — fail fast.
2. Determine the working set:
   - Default: `gh search prs --author "$(gh api user --jq .login)" --state open --limit <limit> --json repository,number,title,url,createdAt,updatedAt,author,headRefName,baseRefName`
   - `--repo`: `gh pr list --repo <repo> --author "@me" --state open --json ...`
   - `--from-queue`: read `~/.sweep/drip-queue/*.jsonl`, take entries with `status: "open"` (latest per branch), use `(repo, pr_number)` pairs.

### 2. Fetch live state per PR

For each PR, call once:

```
gh pr view <pr> --repo <repo> --json state,mergeable,reviewDecision,reviews,statusCheckRollup,isDraft,comments,headRefOid,baseRefOid,updatedAt
```

Batch concurrently up to 5 at a time. `gh` rate-limits get triggered around 30 req/min; 5-way parallelism with ~3 PRs/min average is safe.

If a `gh pr view` fails (transient), skip the PR, log to `~/.sweep/pr-state-errors.log`, continue. Don't abort the run.

### 3. Classify

For each PR, evaluate the bucket rules in priority order. Stop at the first match.

**Signals to extract:**
- `review`: `reviewDecision` (`APPROVED` / `CHANGES_REQUESTED` / `REVIEW_REQUIRED` / null)
- `mergeable`: `MERGEABLE` / `CONFLICTING` / `UNKNOWN`
- `ci`: derived from `statusCheckRollup`. `failing` if any `conclusion == "FAILURE"`, `pending` if any not yet `COMPLETED`, `green` if all `SUCCESS`, `unknown` otherwise.
- `activity_h`: hours since `updatedAt`.
- `maintainer_question`: did a `MEMBER`/`OWNER`/`COLLABORATOR` comment after our latest commit, and does the comment body contain `?`? Boolean.
- `competing_pr`: optional. Skip in v1 — needs a separate `gh search` call per PR. Add later if `close` bucket under-fires.
- `gate_stale_h`: optional. From `~/.sweep/gates/<owner>-<repo>.gate` mtime. Skip if file missing.

**Rule application:** plain `if/elif` chain matching the priority table above. Record the matching rule's identifier in `reason` so the audit log is debuggable.

### 4. Deliver to inboxes

For each classified PR, build a message with `msg_id` = `pr-state-<minute-rounded-ts>-<owner>-<repo>-<pr>`. Append it to the inbox named by the bucket → inbox table. `--dry-run` prints the messages to stdout instead.

Ensure `~/.sweep/inbox/` exists. Each inbox file (`qa.jsonl`, `investigate.jsonl`, `drip.jsonl`, `retro.jsonl`) is created on first delivery.

### 5. Render snapshot

Rebuild `~/.sweep/PR_STATE.md` from the same classifications. Group by bucket → inbox, sort within a bucket by `activity_h` ascending. The snapshot is for humans; downstream actors read the inboxes.

### 6. Report

To stdout, print a one-line summary per bucket with counts and destination inbox. If `--bucket NAME` is set, print the full filtered list.

## Rules

- **Read-only.** pr-state never edits PRs, never closes, never pushes, never invokes `/qa` or `/investigate`. It classifies; humans and other skills act.
- **Don't recommend closing stale PRs.** Per the user's standing rule: stale + no review is a signal to ping or rebase, not close. The **close** bucket fires only on hard signals (maintainer asked, competing PR merged), never on age alone.
- **Idempotent within a minute.** Same `gh` response + same drip-queue state → same classification. Snapshots are timestamped so the jsonl grows, but reading the latest-per-PR gives a stable view.
- **Append-only state.** Never edit prior lines. State derives from the latest line per `(repo, pr)`.
- **Auth first.** `gh auth status` before any other work.
- **Composable with sweep.** The `--monitor` tick can fire `/pr-state` as its read pass. The classifier output becomes the work queue for the next pipeline tick (qa bucket → `/qa`, investigate bucket → `/investigate`, etc.).

## Composition with the rest

```
gh (the world)
   |
   v
[ pr-state ] --intent=reattest--> [ qa.inbox ]          --> /qa takt (WIP=1)
              --intent=respond--> [ investigate.inbox ] --> /investigate
              --intent=close---->  [ drip.inbox ]       --> /drip
              --intent=rebase-->   [ drip.inbox ]       --> /drip
              --intent=ship---->   [ drip.inbox ]       --> /drip
              --intent=audit-->    [ retro.inbox ]      --> /retro batch
```

Each downstream actor consumes intents from its inbox:

- **`/qa`** consumes `intent: "reattest"` — re-run gates on a PR whose CI failed or whose attestation is stale.
- **`/investigate`** consumes `intent: "respond"` — read the reviewer's comment, decide a response.
- **`/drip`** consumes `intent: "close" | "rebase" | "ship"` — advance the PR's status (close, force-push rebase, or no-op while waiting for merge).
- **`/retro`** consumes `intent: "audit"` — append the wait-bucket entry to the rolling audit trail. No action taken; only history kept.

Acks flow back to `~/.sweep/inbox/_acks.jsonl`. pr-state's next tick reads acks to detect backpressure (e.g., qa.inbox unread for >30 min → surface to human).

## Failure modes

- **`gh search` returns nothing:** write an empty snapshot, render an empty PR_STATE.md, exit 0.
- **`gh pr view` rate-limited:** lower concurrency, retry once with 30 s backoff. If still failing, log and skip.
- **PR has no CI configured:** `ci = "unknown"`. Treat as green for bucket purposes — absence of failure isn't failure.
- **Drip-queue jsonl exists but PR not found there:** classify on `gh` data alone. The drip queue is a hint, not the source of truth.
- **`statusCheckRollup` is null on a brand-new PR:** `ci = "pending"`. Bucket: **wait**.
- **`mergeable == "UNKNOWN"`:** GitHub hasn't computed it yet. Treat as `MERGEABLE` for classification (don't promote to rebase on uncertainty).

## Standalone use

Any actor that wants work routed to it can declare its inbox path and the intents it consumes. pr-state delivers; the actor processes on its own takt. The mailbox JSONL schema is stable:

```jsonl
{"ts":"...","from":"<sender>","intent":"<verb>","msg_id":"<deterministic>","repo":"...","pr":...,"...":"..."}
```

A one-shot `/pr-state --bucket close --dry-run` prints the messages it would deliver — useful for sanity-checking the close bucket without firing actual notifications.
