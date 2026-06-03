---
name: triage
description: Score one issue and decide what to do with it — investigate / drop / surface / defer. Per-issue, not per-repo. Single decision in seconds; no fan-out, no nested investigations. The output feeds the investigate inbox.
argument-hint: <repo>#<issue>
allowed-tools: Bash, Read, Write
---

# Triage: One Issue, One Decision

You were invoked on a single issue. Score it, apply the kill list, emit a structured decision, exit. **No spawning sub-agents, no calling /investigate, no scanning the rest of the repo.** Fast is the contract — target ≤30 seconds.

This skill is the scoring station between sift (which surfaces candidates) and investigate (which builds the hypothesis graph). The streaming pipeline runs ONE invocation per issue; batching across a repo is a different shape that this skill no longer does.

## Input

`<repo>#<issue>` — e.g. `pingcap/tidb#68400`. Sift's deposit already passed cheap filters and the LLM judge; your job is the per-issue context check: maintainer engagement signals, repro quality, kill-list match, scoring against the rubric.

## What to fetch

One `gh` call. Title, body, labels, comments count, recent maintainer comments. Don't crawl history; if it isn't visible in the issue view, it's not relevant to a 30-second decision.

```bash
gh issue view <issue> --repo <repo> --json title,body,labels,state,author,assignees,commentsCount,createdAt,updatedAt,comments
```

## Score

| Signal | Score | Rationale |
|--------|-------|-----------|
| Maintainer commented after issue created | 8 | Active engagement |
| Maintainer-filed (issue author is maintainer) | 7 | They want it fixed |
| Recent issue (≤ 7 days) | 6 | First-mover position |
| Clear repro (code fence / stack trace / steps) | 5 | Machine-leverage |
| Labeled "bug" or equivalent | 4 | Maintainer-confirmed kind |
| "good first issue" or "help wanted" | 2 | Penalty risk: fast claimers race us |
| No body / vague | -3 | Nothing to test |

Multiple signals add. Threshold for INVESTIGATE: ≥ 5.

## Kill list (any one of these → DROP)

| Kill signal | Reason |
|---|---|
| Needs hardware you don't own (GPU, embedded, specific OS) | Can't reproduce |
| Feature request with no maintainer endorsement | Inventing problems |
| Design proposal / RFC | Architecture is maintainer's call |
| Vague, no repro, no error | Nothing to test |
| Marked closed / fixed on master | Already done |
| Someone else has an open PR on this issue | Don't compete |
| Tracking / milestone / meta-issue | Not actionable |
| Heuristic / perf tuning with no benchmark | Can't validate |
| Net-addition perf optimization | "We never trade complexity for speed" |
| Requires off-platform discussion (Discord, email) | Pipeline only speaks GitHub |
| Non-English issue body | Operator can't engage |

## Decision

One of:
- **investigate** — score ≥ 5, no kill signal. Enqueue to investigate inbox.
- **drop** — kill signal matched, OR score < 5 with no fixable shape.
- **surface** — needs human attention before automation can decide (ambiguous policy question, sensitive area, possible duplicate).
- **defer** — cooldown active per `sweep retro params --repo <repo>`, OR repo recently auto-evicted.
- **env-blocked** — the issue describes a perturbation surface the
  substrate doesn't carry: Tumbleweed/NixOS-only repro, mobile or
  desktop GUI (Safari, Chrome, native app), specific GPU/embedded
  hardware, runtime+heavydep combo not in the fat image (Julia 1.12 +
  Enzyme, CUDA, ROS), or any "no perturbation surface" verdict you'd
  reach during investigation anyway. Use this when the env-block is
  visible from the issue body alone — emitting it at triage time
  evicts the whole repo, sparing every future card from the same
  repo. If unclear, prefer `investigate`; switch will catch real
  env-block downstream via `env-blocked` signal too.

## Write the attestation

Before emitting the decision event, write a per-issue attestation file at `~/.sweep/attestations/triage/<owner>__<repo>__<issue>.md`. This lets future invocations dedup — the harness checks for the file before invoking /triage, so a repeated call returns cached without burning subscription tokens.

Shape:

```markdown
---
decision: <investigate|drop|surface|defer>
score: <int>
reason: <short tag>
ts: <iso8601 UTC>
---

# Triage: <owner>/<repo>#<issue>

**Title:** <issue title>

**Why this decision:** <one to three sentences naming the concrete signals — labels, maintainer comment, repro shape, kill-list match.>

**Considered signals:**
- <bullet per relevant scoring entry, e.g. "Maintainer commented (Apr 5)">
- <bullet per kill check evaluated>
```

Use `mkdir -p` to ensure the directory exists. Write the file before the `sweep observe event` call so the attestation is durable even if the event log write fails.

## Emit the decision

Every decision logs a structured event so retro can join across stages. **Always emit, even on drop**:

```bash
sweep observe event triage_decision \
  repo="<repo>" pr=<issue> \
  decision=<investigate|drop|surface|defer> \
  reason="<short tag — e.g. 'kill:feature_request', 'score:8', 'cooldown'>" \
  score=<int>
```

If decision is `investigate`, enqueue:

```bash
sweep investigate enqueue --repo <repo> --issue <issue> --reason "<one sentence: why this passes>"
```

That writes to `~/.sweep/inbox/investigate.jsonl` and signals InvestigateActor. /investigate itself runs in a separate downstream actor — not from here.

## Exit

Return a one-line summary to stdout for the human reader:

```
<decision> <repo>#<issue> score=<n> reason=<tag>
```

That's the whole skill. Score, decide, emit, enqueue if investigate, exit. The hypothesis graph belongs to /investigate; the worktree belongs to /investigate; the PR push belongs to /drip. Triage's only job is the structured per-issue decision.

## Output contract (machine-readable, REQUIRED)

After all narration, the **last printed line** must be a single JSON object matching this schema. The downstream wrapper (`sweep.skill_result.shim`) parses this to drive observability and routing — without it, the wrapper falls back to brittle stdout-tail heuristics or marks your run as `triage_no_attestation`.

```json
{
  "decision":      "drop | surface | investigate | defer | env-blocked",
  "score":         0,
  "reason":        "short string, ≤200 chars",
  "rejected":      false,
  "reject_reason": null
}
```

Set `"rejected": true` with a `reject_reason` when you cannot fulfill the job (missing repo context, malformed issue ref, ambiguous target). A rejected job is routed to `~/.sweep/inbox/rejected.jsonl` for operator review instead of being ack'd as decided. Rejection is distinct from `decision: "drop"` — drop means "I evaluated and chose to skip"; rejection means "I couldn't evaluate at all."

Print the JSON as the literal last line (no trailing prose, no markdown fence). Example:

```
… (narration above) …
investigate kimjune01/sweep#42 score=8 reason=clear-repro
{"decision":"investigate","score":8,"reason":"clear repro, single-file fix shape","rejected":false,"reject_reason":null}
```
