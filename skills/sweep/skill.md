---
name: sweep
description: Fan out /triage across multiple repos in parallel. One triage per repo, shared cross-repo findings, unified drip queues.
argument-hint: <repos-file-or-list> [--dry-run] [--limit N] [--pipeline] [--monitor]
allowed-tools: Read, Write, Edit, Bash, Agent, Glob
---

# Sweep: Multi-Repo Triage

Run `/triage` across a list of repos in parallel. Each repo gets its own triage agent, its own `TRIAGE_GRAPH.md`, and its own drip queue. Cross-repo findings propagate through a shared `SWEEP_GRAPH.md`.

## Monoidal contract

| Input | Output | Valid alone? |
|-------|--------|--------------|
| Repo list | Per-repo `TRIAGE_GRAPH.md` + `SWEEP_GRAPH.md` + drip queues | Yes — multi-repo triage with cross-refs |

**Identity:** sweep on one repo = triage on that repo. The cross-reference phase produces no edges, `SWEEP_GRAPH.md` contains one repo summary.

**Composition:** `sweep([A]) + sweep([B]) = sweep([A, B])` — per-repo triage is independent, cross-references are post-hoc. Running sweep on a superset re-triages only repos without completed graphs (idempotent).

**Preconditions:** `/review-schema` per repo (induced automatically in Phase 0, no human gate).

## Input

A list of repos, either:
- A file path containing one `owner/repo` per line (e.g., `repos.txt`)
- Inline list: `/sweep tinygrad/tinygrad google-gemini/gemini-cli withastro/compiler`
- `--dry-run` — passed through to each `/triage` invocation
- `--limit N` — max items per repo (passed through to `/triage`)
- `--add <repo>` — add a repo to the sweep. Runs `/review-schema` for it, then starts triage.
- `--remove <repo>` — remove a repo from the sweep. Stops any running triage agent for it, keeps existing results in `~/.sweep/repos/<owner>-<repo>/` for reference. Does not delete drip queues (they drain naturally).

## State file

`~/.sweep/repos.jsonl` tracks the active repo list and per-repo status. Append-only, one event per line, last-action-wins per repo:

```jsonl
{"ts": "2026-05-08T00:00:00Z", "action": "add", "repo": "tinygrad/tinygrad", "status": "triaged", "cooldown_until": "2026-05-22"}
{"ts": "2026-05-09T08:00:00Z", "action": "add", "repo": "astral-sh/ruff", "status": "ready"}
{"ts": "2026-05-09T12:00:00Z", "action": "triage", "repo": "astral-sh/ruff", "status": "triaged"}
{"ts": "2026-05-09T12:00:00Z", "action": "evict", "repo": "python-attrs/attrs", "status": "evicted", "reason": "0 labeled issues"}
```

Actions: `add`, `promote`, `triage`, `evict`. Statuses: `pending_review` → `ready` → `triaged`. Also: `monitoring`, `evicted`.

To read current state: parse all lines, key by repo, take last entry. Filter `action != "evict"` for active repos.

## Output

- Per repo: `TRIAGE_GRAPH.md` and `~/.sweep/drip-queue/<owner>-<repo>.jsonl`
- Cross-repo: `SWEEP_GRAPH.md` in the working directory with cross-references between repos
- Punch list: unified view across all repos, sorted by score

## Process

### Phase 0: Preflight

1. `gh auth status` — fail fast on auth issues
2. Read `~/.sweep/repos.jsonl` if it exists. These are the known repos.

### Phase 1: Fan out (concurrent)

Launch everything in parallel. Don't wait for sift to finish before investigating known repos.

```
# Agent 1: sift (background)
Agent({
  subagent_type: "general-purpose",
  run_in_background: true,
  prompt: "Run /sift. Find new repos, update repos.jsonl.
           For each new repo, run /review-schema.
           Report additions when done."
})

# Agents 2–N: one per repo, full pipeline (background)
for repo in repos.jsonl:
  Agent({
    subagent_type: "general-purpose",
    model: "opus",
    run_in_background: true,
    prompt: "Full triage pipeline for <repo> [--dry-run]:
             1. Fork (gh repo fork --clone=false) if not already forked.
             2. Clone to ~/Documents/<repo-name> if not already cloned.
             3. Scan issues: competing PRs, scoring, kill list.
             4. For the best actionable issue:
                a. Read code, understand the problem, gather relevant file contents.
                b. Send problem + code to /codex: 'Here is issue #N. Here are the relevant files. Implement a minimal fix.' Apply codex's output.
                c. Test gate — fail on master, pass on fix.
                d. Send the fix diff to /gemini: 'Review this fix for logic errors, missed edge cases, inverted conditions.' Hard block — do not proceed if gemini rejects.
             5. git add + git commit (commit at implementation time).
             6. Write branch pointer to ~/.sweep/drip-queue/<owner>-<repo>.jsonl.
             7. Update ~/.sweep/repos/<owner>-<repo>/TRIAGE_GRAPH.md with outcomes.
             The branch IS the artifact. No PR descriptions — drip writes those from the diff at push time."
  })
```

Each agent runs the full pipeline end-to-end: scan → investigate → implement → test → review → queue. The output is a branch pointer in the drip queue, not a document. Agents that only produce TRIAGE_GRAPH.md without branches have not completed the pipeline.

**Model split — opus orchestrates, codex implements, gemini gates:**

Orchestration is token-cheap but judgment-heavy. Opus picks better issues and understands problems deeper — the cost difference vs. sonnet is negligible for scan/read/pick work. The expensive tokens are in implementation, and those go to codex.

| Phase | Model | Role |
|-------|-------|------|
| Scan, pick, read code | **Opus** (agent) | Judgment — issue selection, competing PR analysis, problem understanding |
| Implement fix | **Codex** (GPT-5.5 via `/codex`) | Structural reasoning — writes the actual fix code |
| Quality gate | **Gemini** (3.1 Pro via `/gemini`) | Logic tracing — catches inverted conditions, missed branches |

Steps 4b and 4d are **hard blocks**. A branch without codex implementation + gemini gate is a half-finished artifact. Do not queue it.

Sift searches for new work while triage agents investigate and implement on existing repos. When sift finishes and adds new repos, spawn triage agents for them into the same pool.

### Phase 2: Cross-reference (post-hoc)

After all triage agents complete, scan for shared findings. This is summarization, not live propagation — each triage ran independently.

1. Read each repo's `TRIAGE_GRAPH.md`
2. Look for shared patterns across repos:
   - Same dtype (bf16 issues across repos)
   - Same algorithmic pattern (graph rewrite depth, recursive traversal)
   - Same dependency (LLVM version, CUDA toolkit)
3. Write cross-references to `SWEEP_GRAPH.md`:

```markdown
# Sweep Graph (2026-05-08)

## Cross-repo findings
- bf16 cluster: tinygrad#6909 ↔ tinygrad#11756 ↔ tinygrad#16114 (same dtype, different failure modes)
- graph rewrite depth: tinygrad#13409 (ScatterND) shares root cause pattern with any repo using recursive AST traversal

## Per-repo summaries
### tinygrad/tinygrad
[punch list from triage]

### google-gemini/gemini-cli
[punch list from triage]
```

### Phase 3: Unified punch list

Merge all repos' punch lists into one, sorted by score. Format:

```
READY TO SHIP
  tinygrad/tinygrad #6909 — bf16 autocast (score 3, fix ready)
  gemini-cli #24736 — union-find compaction (score 6, LGTM)

BLOCKED
  tinygrad/tinygrad #13409 — ScatterND (needs scatter primitive)

NO ACTION
  tinygrad/tinygrad #7020 — TinyJit wrong values (already fixed)
```

### Phase 4: Qualify (triage agents produce branches, not descriptions)

Triage agents run the full pipeline per item: `/investigate` (read code, find root cause, write fix, create branch) → `/codex` (structural review) → `/bug-hunt` (adversarial verification). The output is a **branch pointer** in the drip queue, not a prose document:

```jsonl
{"repo": "pallets/click", "branch": "fix-3362-hyphens", "issue": 3362, "test_cmd": "pytest tests/test_formatting.py", "worktree": "/Users/junekim/Documents/click", "status": "queued"}
```

The branch is the artifact. It contains the diff, commits, and test changes. Everything downstream reads from it.

**Commit at implementation time.** Agents must `git add` + `git commit` as the final step of implementation, before writing the drip queue entry. An uncommitted branch is not an artifact — it's a half-finished workspace. The drip queue entry should reference a commit SHA.

**Drip queues are per repo.** Each repo has its own independent queue at `~/.sweep/drip-queue/<owner>-<repo>.jsonl` with its own pacing. One open PR per repo at a time, but multiple repos can have open PRs simultaneously. Getting banned from one repo doesn't affect others.

**Repo clones live in `~/Documents/`.** Fork the repo on GitHub (`gh repo fork --clone=false`), clone to `~/Documents/<repo-name>`, create the fix branch. This is where the code lives — the branch pointer in the drip queue references this local path.

### Phase 5: Quality gates (dry-run runs everything except push)

Dry-run produces mergeable PRs locally. Every gate below runs in both modes — only the push at the end is a remote side effect. The output of dry-run is a local branch in `~/Documents/<repo>` that's ready to push and PR.

For each branch pointer in `~/.sweep/drip-queue/<owner>-<repo>.jsonl`:

1. **Staleness check.** Verify the issue is still open. Check for competing PRs that landed since triage.
2. **Test gate.** Checkout default branch, run test — must fail. Checkout fix branch, run test — must pass.
3. **PR description.** Generate from the real diff + issue context. Tone-match against 5 recent merged PRs from the repo.
4. **Gemini volley.** Send diff + generated PR description + issue link to `/gemini`: "You are a maintainer seeing this for the first time. Would you merge it?" Five rounds max. Gemini is best at tracing logic and catching scope issues.
5. **Codex crosscheck.** Shuffle the generated description into a lineup of 5 real merged PR descriptions. Send to `/codex`: "One may be AI-generated. Which ones, and why?" Codex (GPT-5.5) is the best performer at AI-likeness detection among SOTA models. If identified, rewrite tells only (no checklist). Re-shuffle, re-test. Five rounds max. If still detectable: surface to the human.
6. **Push** (full run only). `git push`, `gh pr create`. In dry-run, log what would be pushed and stop.

PR descriptions are a **drip concern**, not a triage concern. Triage produces branches. Drip generates descriptions from diffs at push time.

For full runs, load drip queues per repo. Each repo gets its own independent drip cadence. One open PR per repo at a time.

### Phase 5: Heartbeat (two crons)

After all phases complete, set up two recurring wake-ups with separated concerns:

```
# Pipeline tick — fast, does work
CronCreate({
  cron: "*/2 * * * *",
  prompt: "/sweep --pipeline. Three mandatory actions every tick — do ALL of them, never skip:
           1. SPAWN 3 TRIAGE AGENTS for untriaged ready repos (model:opus). Always. Pick by: warm leads first, then high-star. Use the opus+codex+gemini model split.
           2. RUN /drip on EVERY unblocked queued branch. Check org gate, then push.
           3. Spawn impl agents for any stalled pipeline (TRIAGE_GRAPH.md but no drip branch).
           'Idle' means ALL THREE are empty: zero ready repos, zero queued branches, zero stalled pipelines. Running agents don't count — spawn more anyway.",
  recurring: true
})

# Monitor tick — slow, checks state
CronCreate({
  cron: "23 * * * *",
  prompt: "/sweep --monitor. Check all open PRs for reviews, comments, CI status, merges, or closures. Run eviction checks. Check competing PRs on blocked items. Update SWEEP_GRAPH.md with any state changes. Max 50 GitHub API calls.",
  recurring: true
})
```

Pass `--dry-run` into both if set on the original invocation. **Always create both crons, even in dry-run.** Dry-run still needs the pipeline to keep cooking — the only thing it skips is remote side effects (no PRs, no pushes).

#### `--pipeline` tick (every 2 minutes)

Fast tick for advancing work. **Keep the work queue saturated.** Don't wait for running agents to finish before spawning new ones — agents are independent.

1. **Spawn triage agents for ALL untriaged ready repos.** Use `model: "opus"`. The number of concurrent agents is dynamic — scale to the work. 30 repos waiting should produce 30 agents, not 3. Pick order: warm leads first, then high-star. Running agents from prior ticks don't reduce the count.
2. **Run `/drip` on every unblocked queued branch.** Check org gate, then push. Branches sitting in the queue are wasted work — push them.
3. **Spawn impl agents** for any stalled pipeline (TRIAGE_GRAPH.md exists but no drip queue branch).
4. **Supervise actor mailboxes.** Sweep is the supervisor for the OTP-style actors (`/qa`, `/investigate`, `/drip`, `/retro`). For each `~/.sweep/inbox/<actor>.jsonl`:
   - Read messages and `~/.sweep/inbox/_acks.jsonl`. Pair by `msg_id`.
   - For each unacked message, compute age = now − msg `ts`.
   - **Stall threshold:** actor's declared takt × 6 (qa: 5 min × 6 = 30 min; investigate: 15 min × 6 = 90 min; drip: 5 min × 6 = 30 min; retro: batch, no stall check).
   - If the oldest unacked message exceeds threshold: spawn the actor once with a prompt referencing that single `msg_id` (the block-qa-batching hook enforces WIP=1 — supervisor restarts are single-message restarts).
   - If still stalled on the next `--pipeline` tick (i.e., same `msg_id` exceeds threshold again after one restart): write a stall record to `SWEEP_GRAPH.md` under a `## Stalled actors` section and stop restarting until human ack. Three restarts on the same message would be a flapping actor, not a stall — surface it.
   - Log every restart and stall to `~/.sweep/sweep-log/<date>.jsonl` with the `msg_id` so retro can mine flap patterns.

5. **Andon — check mailbox depth (boundedness).** Stall detection above is age-based; this is count-based. Run `~/.sweep/bin/inbox-depth --andon-only`. If exit code is 2, an actor's unacked count exceeds its bound (default qa=3, investigate=5, drip=5; override via `~/.sweep/config.json` → `bounds`). Andon response:
   - **Stop dispatch to the overflowing actor.** `/pr-state` must not append new messages to that inbox until depth drops. The supervisor sets an `andon` flag at `~/.sweep/inbox/_andon.jsonl` (one line per andon event with actor + ts + depth); dispatchers read this file and skip blocked actors.
   - **Spawn an extra worker** of the overflowing actor (still WIP=1 per worker — the hook enforces this — so two workers means two single-message processes).
   - **Surface in `SWEEP_GRAPH.md`** under `## Andon` with the actor, depth, bound, and oldest-message ts.
   - The andon clears automatically when `inbox-depth` reports depth ≤ bound on a subsequent tick. Append `{"action":"clear",...}` to `_andon.jsonl`.
5. **"Idle" is rare.** It means ALL FOUR are empty: zero ready repos, zero queued branches, zero stalled pipelines, zero stalled inboxes. If any of these have items, do the work. Don't rationalize inaction.

#### `--monitor` tick (hourly at :23)

Slow tick matching review cadence. Checks external state.

1. Check all open PRs for reviews, comments, CI failures, merges, or closures.
2. Run eviction checks (see below).
3. Check competing PRs on blocked items — competing PR merged? Issue closed? Unblock or kill.
4. Update `SWEEP_GRAPH.md` with any state changes.
5. If a PR was merged: update drip queue status, check if repo has another queued branch to push next.
6. If a PR was rejected: log rejection, check if approach needs revision or issue should be killed.

**Why two crons:** Pipeline work (spawning agents, running tests) completes in minutes. PR reviews take hours to days. Polling PRs every 2 minutes wastes context on "no change" responses. Polling pipeline state hourly delays agent spawning. Each concern runs at its natural cadence.

## Eviction (runs on `--monitor` tick)

The roster grows via `/sift`. Sweep prunes it. Check every heartbeat tick, before launching triage agents.

| Trigger | Action |
|---------|--------|
| All issues KILLED or BLOCKED, no PENDING/CONFIRMED items | evict |
| Cooldown active with no end date (permanent ban) | evict |
| Three consecutive PR rejections, no merges | evict |
| Repo archived or deleted upstream | evict |
| No open items AND no open PRs by user | evict |
| Status is `dormant` for >14 days | evict |

**Eviction means:** status → `evicted` in `repos.jsonl`. Drip queue drains (don't abandon open PRs). State files kept for reference. Repo can be re-added with `--add`.

**Competing-PR eviction:** If the only actionable issue on a repo has a competing open PR, and the repo has no other items, demote to `monitoring`. Don't evict — the competing PR might stall.

**Apply now.** On each `--monitor` tick, scan `repos.jsonl` for eviction triggers before doing anything else. Log evictions to `~/.sweep/sift/candidates.jsonl`.

## Rules

- **Never ask the user.** Sweep runs autonomously. If you have a hunch, act on it. If you're uncertain, skip it and move on. Log what you skipped and why. The user reads the punch list at the end, not a questionnaire in the middle.
- **One triage per repo.** Never mix repos in a single triage run.
- **Cross-pollinate, don't duplicate.** If two repos share a finding, write the cross-reference. Don't investigate the same thing twice.
- **Independent drip queues, shared org gate.** Each repo has its own queue, but repos under the same GitHub org share a maintainer surface. Drip enforces `max_open_per_org` (default 1) — one open PR per org at a time. Getting banned from one repo in an org triggers cooldown on all repos in that org.
- **Idempotent.** Running sweep twice skips repos whose triage is already complete (TRIAGE_GRAPH.md exists with all outcomes filled).
- **Auth first.** Verify access to every repo before launching any agents.
- **All PRs route through /drip.** No direct `gh pr create` during active pipeline runs. 14 manual PRs in 2 days triggered a ban warning. The drip queue exists to prevent this — enforce it.
- **Never recommend closing a stale PR.** No-review age is a signal to ping, rebase, or break up — not to close. Closing destroys optionality. Only recommend closing when a maintainer explicitly rejects it or the approach is superseded by another merged PR.
