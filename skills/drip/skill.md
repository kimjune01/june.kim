---
name: drip
description: Pace PR creation — one PR open at a time per repo, one per org at a time, address feedback before pushing new. The skill matches tone, runs the codex lineup, and decides when to fold reviewer feedback in. Queue state, hard gates, gh I/O, and the heartbeat live in `sweep` CLI.
argument-hint: <repo> [--check] [--push] [--list] [--ingest] [--watch]
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Drip: One PR at a Time

You were invoked by the harness on one repo. Your job is the LLM-shaped part of pushing a PR: tone-matching the description, running the codex AI-likeness lineup, and handling reviewer feedback on already-open PRs. Pacing math, gh fetches, hard gates, status transitions, and the queue file all belong in `sweep drip` — call it.

> Eleven PRs in two days gets you banned. One PR per merge cycle builds gravity. The code is the same; pacing is what makes the inbox welcoming.

## The CLI is the harness

| What you need | How to get it |
|---|---|
| List the queue | `sweep drip list --repo …` |
| Check whether it's time to push (runs every hard gate, returns the next pushable entry or a reason) | `sweep drip check --repo …` |
| Force-push the next queued entry | `sweep drip push --repo … [--branch …]` |
| Enqueue a new entry | `sweep drip enqueue --repo … --branch … --issue N --test-cmd …` |
| Run heartbeat (15-min check cycle) | `sweep drip watch --repo …` |
| Hard gates (test fail-on-master/pass-on-fix, staleness, org-gate, cooldown, dry-mode) | Run as part of `sweep drip check` — don't reimplement |
| Open PRs with new reviewer activity | `sweep drip checkup --repo …` |

If `sweep drip check` returns "blocked: <reason>," **read the reason and act on it** — don't push past it. That's the [skills-lack-determinism](https://june.kim/skills-lack-determinism) loop: deterministic gates return useful errors; the agent closes the loop. If a gate is mis-classifying, fix the gate, not this file.

## The judgment part

### Generating the PR description (tone match)

The CLI gives you the diff and 5 recently merged PRs from the repo. Your job: write a title and body that match. Match title format, body length, level of detail. Don't write a description; **inhabit the repo's voice**. The chameleon rule.

### The receipt (deeper the reason, more explicit the receipt)

The body's *content* follows a fixed shape — receipt format. Voice/tone still matches the repo's, but the structure shows the work:

```
<terse one-liner conclusion>

- <reason why thing X doesn't work, natural language>
- <reason why thing Y doesn't work, different angle>
- <finally what worked, and why>

[HG](https://github.com/kimjune01/sweep/blob/master/repo-hypotheses/<owner>__<repo>__<issue>.md)
```

Three rules for the bullets:
- **Each bullet is one sentence**, in natural prose. Not a table, not "Hypothesis: ... Falsifier: ..." headers (that's bot prose; see wild#1924 retro).
- **Lead with what didn't work** — the maintainer sees that you searched the space, not just landed on an answer. Two dead ends and one survivor is the calibration: it tells them how much was tried.
- **Each bullet names a concrete thing**: a function, a flag, an observed behavior. "X doesn't work because Y" beats "we considered an alternative."

The `[HG]` link points at the full investigation trace in this repo's `repo-hypotheses/` directory. The receipt is the curated headline; the HG is for the maintainer (or other contributors) who want to dig in. Most won't click; the existence of the link is the credibility signal.

The /investigate skill writes the HG file at `~/Documents/sweep/repo-hypotheses/<owner>__<repo>__<issue>.md` before handing off to /drip. If the file is missing, omit the `[HG]` link rather than fake it.

### Codex lineup (hard block; LLM-shaped)

After tone matching, shuffle the candidate description into 5 recently-merged PR descriptions from different contributors and ask `/codex`:

> Here are 6 PR descriptions from a repo. One may be AI-generated. Which ones, and why? If you can't tell, say so.

- **Can't pick:** pass.
- **Identifies the candidate:** rewrite to fix the specific tells codex named. Do **not** give the rewriter a checklist or rubric — [detection is a wasting asset under feedback](https://june.kim/slop-detection); any rubric becomes the exploit surface. Re-shuffle, re-test.
- **Still detectable after 5 rounds:** surface to the human. Some repos have a voice Claude can't imitate; forcing it makes it worse.

### Gemini volley (final review, LLM-shaped)

Send diff + generated description + issue link to `/gemini`:

> You are a maintainer seeing this for the first time. Would you merge it?

Five rounds max. [Won't converge to zero findings](https://june.kim/does-iteration-mitigate-slop-slope) — iterate until structure is sound.

### Reviewer feedback on open PRs (LLM-shaped)

`sweep drip checkup` reports new comments on your open PRs. For each one:

1. Classify: requested change / question / style nit / approval.
2. Requested changes and questions: address them with a follow-up commit. Re-run the gemini volley on the updated PR before pushing.
3. Style nits: apply if trivial, reply explaining if not.
4. **Address feedback before pushing new PRs.** A PR with unaddressed reviewer comments older than 24h is a driveby. The CLI gate enforces this; don't try to push past it.
5. Never edit the diff in a way that changes the issue's intent. If a reviewer asks for a change the issue's commenter didn't ask for, surface — don't fold it in.

## Rules (judgment, not mechanics)

- **Fork only, never origin.** PRs use `--head <user>:<branch>`. You're a guest.
- **Never force push.** If the branch needs a rebase, the user does it manually; drip pushes, it doesn't fix.
- **Never merge.** The maintainer ships.
- **Address feedback before pushing new.** Inbox manners.

## What this skill does not do

- Read or write `~/.sweep/drip-queue/*.jsonl`. (`sweep drip enqueue` / the CLI does.)
- Run `gh auth status`, `gh pr list`, `gh pr view`, `gh issue view`. (The CLI does, with the right cache and rate-limit handling.)
- Test attestation (fail-on-master / pass-on-fix), staleness check, org-gate, cooldown timer, dry-mode skip. All hard gates run inside `sweep drip check`. The skill doesn't replicate them.
- Heartbeat loop. (`sweep drip watch` or `/loop 15m /drip`.)
- Status enum, queue schema. (Harness owns it.)
- Decide `max_open` or `max_open_per_org`. (Retro params, surfaced by the CLI.)

## Output contract (machine-readable, REQUIRED)

After all narration, the **last printed line** must be a single JSON object matching this schema:

```json
{
  "pushed":        false,
  "pr_url":        "https://github.com/owner/repo/pull/N or null",
  "outcome":       "pushed | rebased | checked | noop | failed",
  "reason":        "short string, ≤200 chars",
  "rejected":      false,
  "reject_reason": null
}
```

`pushed=true` iff a commit or PR actually hit the remote on this run. `outcome` is the verb that happened (the `checked` branch corresponds to `--check` invocations that don't push). Set `rejected=true` with a `reject_reason` when the job is undeliverable (no fork remote, stale branch, missing PR — anything that means "this msg cannot be acted on"). Rejected jobs route to `~/.sweep/inbox/rejected.jsonl` for operator review.

Print the JSON as the literal last line, no trailing prose, no markdown fence.
