---
name: retro
description: The pipeline's backward pass. Read what happened, compress repeated episodes into durable artifacts (skill patches, parameter files, memories). Lossy by design — the losses are what didn't generalize. Naming the loss is part of the artifact.
argument-hint: <repo> [--since YYYY-MM-DD]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Retro: The Backward Pass

You are the [consolidation pipe](https://june.kim/consolidate-pipe) running over the cycle that just finished. Your job: read the logs, find the repeated episodes, compile each repetition into the smallest artifact that lets the next cycle skip that work. Then say what you dropped.

Same morphism every time:

```
watch yourself (or the agents) repeat
  → compile the repetition into a skill / param / memory / CLI
  → next cycle runs
  → notice where the compiled artifact failed
  → update
```

See [Memory Compression](https://june.kim/memory-compression). The pattern is recursive: this skill is itself a compression of the manual retros that came before it.

## The CLI is the harness

| What you need | How to get it |
|---|---|
| All structured events for a repo since date | `sweep retro gather --repo … --since YYYY-MM-DD` |
| **Pipeline policy commits (split events by version)** | `sweep retro policy-changes --since YYYY-MM-DD` |
| Existing parameter file for a repo | `sweep retro params --repo …` |
| PR outcomes (own + prior art) from GitHub | `sweep retro outcomes --repo …` |
| Append a parameter update | `sweep retro set --repo … --key … --value … --reason …` |
| Record a `fix_ready` entry | `sweep retro fix-ready --repo … --issue N --line-count N --description …` |
| Skill-use stats (which skills fired, how often, with what outcome) | `sweep retro skill-stats --since YYYY-MM-DD` |
| Propose an eviction (skill / memory not earning its keep) | `sweep retro evict --target <name> --reason …` |
| List CLI commands agents tried to call but that don't exist | `sweep retro missing-calls --since YYYY-MM-DD` |
| ~~Surface mid-run skill edits~~ | **NOT BUILT** — `mid-run-edits` is spec'd below but unimplemented; don't reach for it |
| ~~Outbound ref-drift check~~ | **NOT BUILT** — `ref-drift` is spec'd below but unimplemented; don't reach for it |
| ~~Outbound em-dash audit~~ | **NOT BUILT** — `em-dash-audit` is spec'd below but unimplemented; don't reach for it |

> The three rows above are **planned, not built**. `sweep retro --help` is the source of truth for what exists. The prose below specifies their intended behavior (for whoever builds them); until then, skip steps that depend on them and don't burn calls reaching for them.

### Policy boundaries before aggregation

Before averaging anything across the window, run `sweep retro policy-changes --since <window-start>`. Each row is a commit that touched classifier rules, routing, model defaults, workflow code, or a skill spec — anything that changes what the pipeline *does* with the same input.

Use those timestamps to slice the event stream into eras: events before commit `<ts>` ran under the old policy, events after ran under the new. Mixing them collapses two different systems into one number and you'll prescribe a fix for an average that no run actually saw. When you can't separate cleanly, say so — name the policy change in S, attribute the events to "pre-X" and "post-X" in O, and let A treat them as separate populations.

If a CLI command isn't there yet, that's a gap — don't reimplement the gh / jsonl plumbing here. The deterministic harness rejects malformed inputs with errors you close the loop on.

## The compression operation

Each compression has four parts. Write them all.

1. **The repeated episode.** Name what kept happening. "Three triage runs in a row killed `good first issue` items because fast claimers raced us." If you can't name three episodes, it's not a pattern — log it as ambiguous, don't compress yet.

2. **The compiled artifact.** Where the lesson now lives. Pick the lightest form that binds the next cycle:

   | Compression target | Where it lives | Binds when |
   |---|---|---|
   | Single repeated action → operation | Skill markdown patch (`/triage`, `/drip`, etc.) | Skill is invoked |
   | Repeated parameter setting | `sweep retro set` JSONL | Skill reads params |
   | Cross-session insight | Auto-memory entry | Next conversation loads memory |
   | Repeated deterministic check | CLI subcommand or gate | Every invocation |
   | Repeated skill *sequence* | Composed skill (level 2) | Sequence invoked |

   **Prefer the lightest.** A param file beats a skill patch beats a new CLI command beats a new skill. Move heavier only when the lighter form keeps decompressing back into work.

3. **The loss.** Name what you discarded. "Three specific reviewer quotes; the exact PR numbers; the time-of-day they were rejected. Kept: kill-list addition for `good first issue` on repos with >100 stars." The loss is what *didn't* generalize. If you can't name the loss, you're not compressing — you're filing.

4. **The level.** Tag which level of the tower this compression lives at (see [Memory Compression](https://june.kim/memory-compression)):
   - **L0→L1:** repeated manual action → single skill
   - **L1→L2:** repeated skill sequence → composed skill
   - **L2→L3:** sequence that needs context from prior runs → monadic refinement (the skill changes based on what it did last time)

   Most retros produce L0→L1 patches. Watch for L1→L2 opportunities (you keep running A then B then C — make `/abc`). L2→L3 is rare and the work you do least often.

## What retro reads

`sweep retro gather` returns structured events from every pipeline skill plus PR outcomes (own + prior art). You don't grep log files; the CLI assembles. If you need an event type that isn't there, **add it** to the logging contract in the relevant skill, don't reach around the CLI.

Special inputs that don't fit the gather shape:
- **Missing CLI calls.** `sweep retro missing-calls` returns every `sweep <subcmd> …` invocation an agent tried that failed with "command not found" or "unknown subcommand," grouped by the requested call and ranked by frequency. **Each missing call is a wishlist entry the agent demonstrated by reaching for it.** This is how the CLI grows: not from spec, from agent demand. Three agents on three repos all tried `sweep drip checkup --repo X` → build it next. The skill markdown stays honest because failures are visible.
- **Mid-run skill edits.** `sweep retro mid-run-edits` surfaces ad-hoc changes agents made to skill specs during the cycle. Each one is a compression opportunity — the agent already noticed the pattern; retro's job is to formalize it (and remove the ad-hoc patch, or fold it in deliberately).
- **The outbound surface.** "Outbound" means anything actively sent to GitHub or sitting at the front door of a linked-from-outbound repo: issue/PR bodies the pipeline produces, issue/PR comments (including withdrawal notices), the README of any repo cross-referenced from an outbound artifact, `action.yml` description + any text the action emits as PR comments, blog posts cross-referenced from outbound. Specifically watched: [`pr-to-merged`](https://june.kim/pr-to-merged), [`internal-reasoning-of-prose-compiler`](https://june.kim/internal-reasoning-of-prose-compiler), [`speedrunning-open-source`](https://june.kim/speedrunning-open-source), [`the-natural-framework`](https://june.kim/the-natural-framework) — these are linked from issue templates and READMEs, so a rename or stale section breaks the outbound chain. NOT outbound: `skills/*.md`, hypothesis/retro graphs, worklogs, `~/.sweep/*`, internal bootstrap/roadmap docs, CLAUDE.md. The distinction is whether a maintainer evaluating us reads it, not whether it's checked into a public repo.
- **Reference drift.** `sweep retro ref-drift` walks the outbound surface and verifies every `https://github.com/...` path and `#anchor` still resolves. A renamed heading or moved file silently turns a load-bearing pointer into a 404 the maintainer sees first. The check fetches each unique target once per pass, caches for 24h, and reports broken refs grouped by source file. **Triage these as obvious compressions.** A broken outbound link is a receipt against our own pipeline. Fix the link or the heading; don't ship another issue against a 404.
- **Em-dash audit.** `sweep retro em-dash-audit` greps the outbound surface for em-dashes (`—`) and double-hyphens (`--`) in prose, excluding code blocks, table cells, and reference-list separators. Budget is zero. This is a Van Halen rider: the PR Quality Gate flags em-dashes as a low-effort signal, so an outbound artifact containing one proves we don't dogfood. The maintainer doesn't read it as voice; they read it as a competence canary. Internal artifacts (skills, retros, memory) are out of scope; em-dashes that face us are fine.
- **The H0-H6 meta-hypotheses graph** (`~/.sweep/repos/<owner>-<repo>/RETRO_GRAPH.md`). One graph per repo, one entry per PR, classifying which meta-hypotheses the outcome supports or refutes. This is a long-running compression artifact, updated each pass.

## Obvious vs ambiguous (the fan-out gate)

Fan-out compresses human judgment: things three independent perspectives converge on are obvious; things they diverge on are ambiguous. Retro's compression gate is the same. The bucket a finding lands in determines whether the artifact gets written this pass.

**Obvious (fold immediately):**
- Pattern appeared ≥3 times across episodes
- Confirmed fix with reproducer → `sweep retro fix-ready`
- Competing-PR catch on multiple repos → kill-list addition
- Parameter update with measured data → `sweep retro set`
- Cross-session lesson with clear transfer surface → memory entry

**Ambiguous (stash for human):**
- Pattern appeared once — could be noise
- Finding contradicts an existing rule (the rule may be wrong, or the case may be a special)
- Lesson that would change the pipeline's risk profile
- Tradeoff between competing goals where reasonable people disagree

Ambiguous items append to the worklog tagged `[AMBIGUOUS]` with one-line tension descriptions. Each ambiguous→obvious transition over time is real progress. **The retro pipeline gets faster when the ambiguous bucket shrinks**, not when more memories get written.

## Eviction (time × quality)

Compression has a counterpart: artifacts that don't earn their keep get pruned. Without this, the pipeline accumulates dead weight and slows.

Each pass, run `sweep retro skill-stats --since 30d`. For each pipeline skill, parameter, and memory:

- **Used and producing value:** keep. (Used = fired ≥3 times; value = visible in outcome trajectory.)
- **Used but no measurable effect:** keep but flag — could be ambient (background invariant) or dead weight (next pass decides).
- **Unused for 30 days and not a guard rail:** propose eviction. `sweep retro evict --target <name>`. Human approves; CLI removes.

Guard rails (rules that prevent bad outcomes even when they never fire) are protected — `cooldown_until`, "fail on master, pass with fix," "fork-only push." Annotate them as guards so eviction skips them.

The metric retro optimizes for is **time × quality preserved per artifact**. High product → keep / promote. Low product → evict. Same metric for skills, params, memories.

## Process (one pass)

1. `sweep retro gather --repo <r> --since <d>` — pull all events.
2. `sweep retro outcomes --repo <r>` — pull PR outcomes (own + prior art) since last pass.
3. `sweep retro missing-calls --since <d>` — pull the CLI-wishlist (commands agents reached for that don't exist). **Triage these first** — every entry is the strongest possible evidence for a CLI gap: an agent already needed it. Rank by frequency, name the verb-noun shape, queue as CLI work.
3a. *(when built)* `sweep retro ref-drift` and `sweep retro em-dash-audit` — walk the outbound surface, report broken refs and any em-dashes in prose. Both block the ship, not the retro. A broken link or a stray em-dash in an outbound artifact is a receipt-failure against our own pipeline. **These two are not yet implemented — skip this step until they appear in `sweep retro --help`.**
4. **Find the repetitions.** Three+ similar episodes → compression target. Group by axis (kill reason, reviewer language, scoring miss, drip pacing, agent failure mode).
5. **For each compression target, write the four parts** (episode, artifact, loss, level). Choose the lightest artifact form. Apply via the matching `sweep retro …` CLI.
6. **Update the meta-graph.** For each PR outcome, classify which of H0-H6 it supports/refutes. Append to `RETRO_GRAPH.md` for the repo.
7. **Surface mid-run edits.** Each one is a compression opportunity already half-done by the agent.
8. **Run eviction pass.** `sweep retro skill-stats` + `evict` proposals.
9. **Log what changed.** Append a single line to worklog: "retro: compressed N targets (M obvious / K ambiguous), evicted X, CLI-wishlist W, pre-registered Y."

## Rules (judgment, not mechanics)

- **Read everything, write little.** Compression ratio is the point. Ten events → one rule, one rule's reason, one named loss.
- **Three repetitions before you compress.** One is noise, two is coincidence, three is a pattern. Anything less goes to `[AMBIGUOUS]`.
- **Always name the loss.** An artifact without a stated loss is filing, not compressing. The next retro can't audit it.
- **Tag the level.** L0→L1, L1→L2, L2→L3. The level determines where the artifact lives and what it's allowed to depend on.
- **Bans don't decay.** `cooldown_until` is the one parameter retro never auto-resets; humans clear it.
- **Don't grow without pruning.** Every pass should propose at least one eviction (or explain why nothing's prunable).
- **Skills evolve during the run.** Mid-run edits are evidence the agent already saw the pattern. Treat each as a half-done compression to either formalize or roll back.
- **The outbound surface is a brown-M&M test.** Anything a maintainer reads to evaluate us (issues, comments, READMEs of linked repos, `action.yml`, cross-linked blog posts) is a competence canary. Broken refs, em-dashes in prose, and other low-effort tells fail the canary before the maintainer reaches the argument. Outbound-surface checks block the ship, not the retro. Internal artifacts (skills, retros, memory, worklogs) are out of scope; only the surface the maintainer sees matters.

## What this skill does not do

- Read log files directly. (`sweep retro gather` does, with proper schema validation.)
- Touch skills outside the pipeline set. (CLI enforces the scope limit; the skill markdown doesn't restate it.)
- Reformat artifacts cosmetically without naming a loss. (That's filing.)
- Grow the library without proposing prunes. (Asymmetric edits accumulate dead weight.)
- Auto-resolve ambiguous findings. (Those go to the human; pushing them into "obvious" inflates apparent throughput.)
