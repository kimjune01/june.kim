---
layout: post-wide
title: "Agents' Standup"
image: "/assets/the-learning-agent.jpg"
tags: cognition methodology coding
---

*Part of the [cognition](/cognition) series. Builds on [Consolidation](/consolidation), [Work Log](/work-log), [Blind, Blind, Merge](/blind-blind-merge), and [The Parts Bin](/the-parts-bin).*

![Robots in business casual having a standup meeting in a beige cubicle farm](/assets/the-learning-agent.jpg)

## Coworkers at the office

It's 1999 and your team just shipped [pets.com](https://www.youtube.com/watch?v=nXHrlm5Nk5w). Before the next release, the roster changes. Someone from infra rotates in, the contractor rolls off, the new hire gets their first real task. Nobody plans this as a learning strategy, but it is one.

Fresh eyes catch what veterans stopped seeing. Scar tissue prevents mistakes the newcomer would repeat. Nobody carries every skill: each person is [T-shaped](https://en.wikipedia.org/wiki/T-shaped_skills), deep in one area, broad across the rest. The team's coverage comes from overlapping T's. Fixed hours in a release cycle mean depth costs breadth.

Lessons surface during the project: "don't mock the tokenizer," "the staging deploy needs a manual gate," "the client's API returns 200 on failure," "stop letting users upload sock puppets as pets." The postmortem captures what people remember, not what happened. The work log captures what happened, not what it means. Consolidation happens over coffee, if it happens at all.

Process affects the learning rate, not whether learning happens. What keeps the rate from decaying is the stochasticity: people rotating at project boundaries. Society imposes it for free.

## Same pipeline, different substrate

Agents already do an analogous thing. Not by retraining weights — by updating externalized policy: hooks, filter rules, skill configurations, priorities. The learning lives outside the model, in the tooling that shapes how the next session runs.

[Work logs](/work-log) are Remember: append-only, timestamped, structured. The agent writes them as a byproduct of working. [/consolidate](/consolidation) is a backward pass that reads from Remember. The methodology *is* the cognition. The channel opened both ways.

But one agent's work log doesn't carry enough bits to learn fast. A single session produces a handful of lessons. Each is true. None generalizes without reinforcement. [Complementary learning systems](https://doi.org/10.1037/0033-295X.102.3.419) explains why: the hippocampus stores fast, the neocortex learns slow. One agent is all hippocampus. It remembers everything, learns nothing.

N agents write to shared storage. Not N copies of the same model with different seeds — that's [self-consistency](https://arxiv.org/abs/2203.11171), stochastic diversity. Structural diversity: different models, different tasks, different failure modes. [Blind, Blind, Merge](/blind-blind-merge) showed that two models make complementary mistakes. Ten agents, ten tasks, ten work logs. The regularities across logs are the signal one log alone can't carry.

Each agent gets a fixed budget of [skills and hooks](https://docs.anthropic.com/en/docs/claude-code/skills). Going deep costs breadth. T-shaped: deep in one domain, broad across the baseline.

The ingredients, all running:

1. **Work logs as Remember.** The agent writes them as a byproduct. [Work Log](/work-log) showed the format.
2. **Shared storage outside any context window.** A separate store that outlives every session. The [consolidation harness](https://github.com/kimjune01/agi) already does this.
3. **Threshold trigger.** Turn count, byte budget, action count. When the store accumulates enough, fire the cron job.
4. **[Blind-blind-merge](/blind-blind-merge) as exploration.** Parallel rollouts, no coordination, merge at the root. The diversity is structural.
5. **The [parts bin](/the-parts-bin) as pharmacy.** Every slot in the pipeline has a catalog of operations with preconditions and postconditions. [The Missing Parts](/the-missing-parts) found the blanks.

Everything runs. Nothing learns.

## Three lessons, one backward pass

**Forward pass (parallel):** N agents run independent tasks, each writing a work log to shared storage. Same battle-tested baseline, different specialty stacks.

**Accumulate (Remember):** Shared storage collects logs.

**Trigger:** Threshold fires the cron job.

**Backward pass (serial, by stage).** Why these three? Cache and Remember are infrastructure — they store and retrieve. Consolidate is the process running right now. Perceive, Filter, and Attend are the policy layers: what to notice, what to reject, what to prioritize. Those are what learning changes.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Target</th><th style="background:#f0f0f0">Updates</th><th style="background:#f0f0f0">Convergence test</th></tr></thead>
<tr><td><a href="/caret-recorder">Perceive′</a></td><td>What to <em>notice</em>. New hooks, triggers, intent patterns.</td><td>Three agents independently flagged the same failure mode.</td></tr>
<tr><td><a href="/perception-pipe">Filter′</a></td><td>What to <em>reject</em>. Convergent mistakes become filter rules.</td><td>Agents with different configs arrived at the same lesson. Shared tooling = herd error.</td></tr>
<tr><td><a href="/salience">Attend′</a></td><td>What to <em>prioritize</em>. Convergent lessons are signal.</td><td>Idiosyncratic lessons decay without reinforcement.</td></tr>
</table>

Without eviction, rules accumulate monotonically. [Soar's failure mode](https://en.wikipedia.org/wiki/Soar_(cognitive_architecture)). The [parts bin](/the-parts-bin) has the fix. The same [Filter grid](/the-parts-bin#grid) that gates external data gates the rule store:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:6em"><col><col style="width:10em"></colgroup>
<thead><tr><th style="background:#f0f0f0">Criterion</th><th style="background:#f0f0f0">Rule</th><th style="background:#f0f0f0">Action</th></tr></thead>
<tr><td>Staleness</td><td><code>last_fired &lt; N cycles</code></td><td>Evict</td></tr>
<tr><td>Redundancy</td><td>Two rules within ε</td><td>Merge into one</td></tr>
<tr><td>Causation</td><td>Does this rule <em>cause</em> better outcomes or <em>correlate</em> with them? <a href="/the-missing-parts#filter-the-causal-row">The blank cell</a>.</td><td>Evict correlates</td></tr>
</table>

Once filtered, [attend](/the-parts-bin#attend) to survivors: keep rules that are both high-value and diverse. Then [compress](/the-parts-bin#consolidate): budget k exemplar rules that approximate the full set.

*The half-life principle:* a lesson's decay rate is inversely proportional to how many agents independently discovered it. Ten agents converge → promote to a filter rule, graduate it into the baseline. One agent saw it once → decay counter, evict without reinforcement.

Promotion requires more than convergence: the rule must improve a downstream metric (defect rate, cycle time, eval pass rate). Convergence without validation is consensus, not learning.

The eviction strategy is a forward pass through the pipeline, applied to the agent's own rule store. The [architecture](/consolidation) already showed this recursive structure: each Consolidate contains its own Filter, Attend, Consolidate. Levels dim as bits decrease. At zero bits, [passthrough](/the-natural-framework).

[Skills already write skills](https://docs.anthropic.com/en/docs/claude-code/skills) — consolidation that updates the Filter. It's dim: no eviction, no multi-agent convergence, no threshold trigger. The cell exists but doesn't meet the contract yet.

## The entourage

Back to the office. A project starts. The team isn't random: the senior engineer who knows the legacy system, the new hire who'll ask why it works that way, the contractor who's seen how three other companies solved it. The composition is deliberate. The stochasticity comes from what each person notices.

Agent teams take the same structure. Before each cycle, compose the entourage: same goal, different configurations.

- *Baseline* (fixed): skills and hooks that passed eviction across many cycles. Every agent gets these: writing to work logs, checking the shared context forest, git workflow, linting. Institutional memory.
- *Specialty* (budgeted): deep stack from the remaining budget. One agent goes deep on error handling, another on refactoring, another on test generation. The cap forces each into a different T-shape.
- *Rotation* (stochastic): untested configurations in some specialty slots. The new hire. Most won't survive eviction; the few that do earn promotion to baseline.

## Cycle one

You're rebuilding [pets.com](https://www.youtube.com/watch?v=nXHrlm5Nk5w). Pet listings, search, user accounts, image uploads. The sock puppet would be proud.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col style="width:5em"><col><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Agent</th><th style="background:#f0f0f0">Tier</th><th style="background:#f0f0f0">Deep stack</th><th style="background:#f0f0f0">Convergence</th></tr></thead>
<tr><td>frontend-ux</td><td>Specialist</td><td>React, component testing, a11y linting</td><td>Tight: lighthouse scores</td></tr>
<tr><td>backend-infra</td><td>Specialist</td><td>Express, Postgres, auth</td><td>Loose: integration tests pass</td></tr>
<tr><td>security-audit</td><td>Rotation</td><td>Input validation, dependency audit</td><td>Aggressive: reject early</td></tr>
</table>

All three share the baseline: work logs, shared context forest, git workflow, linting. Same goal: ship the pet listing feature. Each writes a work log.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:8em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Agent</th><th style="background:#f0f0f0">Work log entry</th></tr></thead>
<tr><td>frontend-ux</td><td>Pet photo upload accepts BMP and TIFF but browsers only render JPEG and GIF. Added server-side conversion. 40 min to find the codec issue.</td></tr>
<tr><td>backend-infra</td><td><code>PUT /pets/:id</code> accepts any payload shape. Someone uploaded a sock puppet as a pet. Added <a href="https://zod.dev/">Zod</a> schema validation after a malformed update corrupted a test record.</td></tr>
<tr><td>security-audit</td><td>Pet photo endpoint accepts files without size limits. Added 5MB cap. Also: backend-infra's Zod schemas don't sanitize HTML in pet descriptions. Flagged.</td></tr>
</table>

Consolidation reads all three logs. Two agents independently hit input validation gaps from different directions (backend-infra on the API, security-audit on the upload endpoint). Different configs, same lesson. Passes the herd-error test. New filter rule: "validate input shape and size at every boundary." Into the baseline for cycle two.

The BMP/TIFF finding from frontend-ux doesn't converge with anything. One agent, one task, no independent confirmation. Decay counter starts. If a future cycle's agents hit the same codec issue, it earns promotion. If not, it evicts.

Cycle two: same baseline (now with the validation rule baked in), different rotation slot. A performance-focused config this time. Pets.com burned through its [Super Bowl budget](https://www.youtube.com/watch?v=nXHrlm5Nk5w) without a backward pass. This version costs $1.50 in API calls and gets better every cycle.

## Contract fulfilled

How many specialists, how many generalists? When does a configuration earn permanence versus rotation? The team that never changes stops learning. The team that changes completely loses institutional memory. Between those extremes sits the rotation policy that maximizes the backward pass's bit rate.

Check the [contract](/the-parts-bin#consolidate): Consolidate reads from persisted observations and writes policy changes to the substrate. Work logs are the observations. The three artifacts (Perceive′, Filter′, Attend′) are the policy changes. Eviction keeps the rule store bounded. Precondition met, postcondition met. The cell is no longer dim.

Work logs extend from documentation to training data for the live system. Agents share semantic memory at the cache layer and learned policy at the baseline. The learning is externalized, inspectable, forkable: [open prose](/open-prose) all the way down. Copyleft for cognition: every lesson one agent learns propagates to every agent that shares the store.

The 1999 team never planned rotation as a learning strategy. Agents need to.

---

*Written via the [double loop](/double-loop).*
