---
variant: post-medium
title: "(PR) → merged"
tags: coding, projects, pageleft
---

*Sequel to [(Issue) → PR](/issue-to-pr). The contributor side ships PRs with receipts; this is what runs on the maintainer side to read them.*

That function. PR comes in, merge or close, with the maintainer's confidence calibrated by evidence the maintainer didn't have to produce themselves. Everything else is plumbing.

## The asymmetry

Right now my pipeline has 167 open PRs across 138 organizations. Of those 167, exactly 7 have *any* review activity at all. Five with changes-requested that I've already responded to and that the reviewer hasn't looked at again. Two approved, awaiting merge. Everything else — 160 PRs — sits at zero engagement. Not rejected. Not merged. Not commented on. Not even looked at.

This is not because the PRs are bad. They have green CI, hypothesis graphs, attestation files, line citations, falsifiable claims. They fix real bugs maintainers filed themselves. They're better-documented than 80% of human PRs to the same repos. The merge rate where review actually happens is 55% — calibrated to the target where each outcome teaches something.

The other 60% of my work sediments. Sixty percent of every test I write, every receipt I synthesize, every Gemini volley I run, every commit I shape — sediments. The maintainer never reads it. The PR doesn't get rejected because rejecting takes attention; it gets ignored because ignoring is free. By month three the maintainer has forgotten the tab exists.

This isn't a me problem. The same arithmetic plays out for every cold contributor. Solo maintainer has thirty review minutes per day against a queue that grows faster than thirty minutes can clear. The contributor cost that used to act as a quality filter — having to spend four hours writing a PR meant you were probably serious — collapsed when AI made writing PRs nearly free. Supply went up tenfold. Demand for review didn't move. The market clears at "ignored," because that's the cheapest action a rational maintainer can take when the input distribution is ruined.

The waste at scale is staggering. Imagine the aggregate of every contributor across every OSS repo writing fixes that will never be read. Multiply by 365 days. That's the deadweight loss of an unpriced attention market with no filter. Bug fixes that exist, in tests-pass-real-issue-fixed form, sitting in queues nobody opens. Every one of them is queue relief a maintainer would benefit from if they could afford to evaluate it.

## Why pricing doesn't fix it

The naive economist answer is to price the bottleneck. Let contributors pay for queue position. Let maintainers charge per review minute. Watch the market clear.

We know how this story ends because we ran it on the open web for twenty years. Adverse selection: the contributors willing to pay are the ones who can't get reviewed on merit. Crowding out: maintainer-contributor relations collapse into contractor-customer relations. Capture by capital: AWS outbids indie devs on every PR. And money doesn't expand capacity — it just decides who gets through. Same total throughput, worse distribution.

What worked on the open web was relationship-based attention. Substack didn't say "pay for likes." It said "pay for direct relationship with this writer." Receipts are the OSS analog: the contributor produces something that demonstrates standing without prior trust, the maintainer reads it cheaply and decides. Not payment for review — credibility that earns review.

## The broken cell

[The Natural Framework](/the-natural-framework) finds the same six-stage pipeline running everywhere information gets processed: perceive, cache, filter, attend, consolidate, transmit. When one stage breaks, the rest dim downstream. Google's filter has no redundancy inhibition, so attend becomes top-k by PageRank, and ten content farms survive. Adtech filters by willingness to pay, so attend becomes "highest bidder wins," and consolidate becomes frequency caps as bandage.

OSS PR review has the same broken cell. The filter is CI: tests pass, formatter happy, types clean. Mechanical correctness, no quality. Every PR that compiles enters the maintainer's queue regardless of whether it duplicates an existing one, fits the maintainer's priorities, or comes from a contributor who's ever had a PR merged here. Attend then becomes "top-k by recency" or "PRs that mentioned me." That's not a filter; that's a coin flip with status anxiety.

The maintainer's response — sediment everything below threshold — is rational allocation. The 60-silent-PR tail isn't system failure; it's the system telling everyone "this is not important enough to anyone." Optimizing the maintainer side without fixing the input distribution just lets more low-importance work through.

## (PR) → merged, factored

Pick the four stages that compose into the function:

```
filter → test → reason → human judge
```

`filter` is mechanical and free. Duplicate-detection by diff hash. Contributor reputation lookup. Diff-size sanity vs the repo's own merge norm. AI-policy compliance. Receipts present at all? Reject takes microseconds and never spends LLM tokens.

`test` runs the test command the contributor claims fails on main and passes on the branch. If their claim holds, the strongest signal a maintainer can want is on the table. If it doesn't, the receipt was a lie and the PR moves to suspect.

`reason` is a SOTA model reading the diff, the test result, and the contributor's hypothesis graph. It writes one paragraph: what this PR is, what evidence supports it, what the risk is. The maintainer reads thirty seconds of synthesis instead of twenty minutes of diff.

`human judge` is the maintainer. They merge, they close, they ask for changes. They never delegate the final call. The function ends with their decision.

Each stage is ten times more expensive than the prior. A PR that fails filter costs nothing. A PR that fails test costs runner minutes. A PR that survives to reason costs cents. A PR that reaches human judge costs the maintainer's attention, which is the expensive thing the whole system exists to conserve. **Sedimentation at every stage is correct behavior.** Most PRs should never reach reason, let alone human.

## Kanban, all the way down

Each stage is a CI workflow that fires on a label. Filter labels `immune:test-pending` on success or `immune:reject` on failure. Test triggers on `immune:test-pending`, labels `immune:reason-pending` or `immune:test-failed`. Reason triggers on `immune:reason-pending`, labels `immune:trusted` / `immune:suspect` / `immune:needs-human`. The maintainer triggers on whichever label tells them this PR is worth their attention.

The whole system is a kanban board. Each PR is a card. Each label is a column. CI workflows pull cards forward when the upstream column has work. Maintainers pull cards backward by removing labels. WIP limits are enforced by `immune:wip-<run-id>` locks, max one stage active per PR. The maintainer's GitHub PR list IS the board — sort by label, filter by column, see the work-in-progress at a glance. No Jira, no Trello, no separate dashboard. The Toyota Production System mapping is exact: pull-not-push, visible WIP, stop-the-line, kaizen between cycles.

Kanban is just actor model computing wearing coveralls. Toyota didn't invent the actor model; they discovered it with hands instead of types. Every TPS principle is the actor contract translated into manufacturing terms — bounded local state, explicit message passing, mailboxes as buffers, supervisor restarts on failure. Hewitt's actor papers (1973) ran ten years after Ohno's TPS was already shipping cars off the line. Same insight, two domains.

## The PR list is the only inventory

immune writes no cache file, no reputation database, no local history. Every artifact is visible in GitHub's standard UI: labels, comments, PR metadata. Reputation lookups query the gh API live. The maintainer can audit the entire pipeline state by reading their PR list. **Anything immune knows, the maintainer can see.**

This is the load-bearing design property. The competitive landscape (devin, copilot enterprise, codiumai, greptile) all violate it — they need a SaaS backend, a hosted database, a "trust us" surface. immune doesn't, because labels are sufficient state. GitHub's label API is atomic per-PR; that's all the concurrency primitive a kanban-board-as-state needs.

## The wedge

Free as in beer. Open as in source. Share-alike as in copyleft. Network-obligated as in AGPL. Code under [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.txt), prose under [CC-BY-SA-NS](/cc-by-sa-ns) — the network-clause variant of CC-BY-SA that closes the SaaS loophole CC-BY-SA leaves open. A company that takes immune, tweaks it for their hosted offering, and serves it from their cloud must publish their fork. The cloud-loophole doesn't apply.

Why this matters: every prior maintainer-side filtering attempt has been killed by the move where someone takes the open-source version, wraps it in a service, captures the contributor base, and never publishes back. AGPL on the orchestration code prevents that for the actions. CC-BY-SA-NS on the spec prose prevents it for the receipt format itself. The receipts-discipline pattern stays a commons whether it's installed as a CI action, wrapped in a cloud service, or repackaged for enterprise.

No billing, no data leakage, bring your own tokens. PR contents go only to (a) the LLM provider you configured with your key and (b) GitHub itself. Nothing is sent to a kimjune01-controlled endpoint. There is no telemetry, no analytics. The action runs in your runner; it phones nowhere.

## The symmetry

[Sweep](https://github.com/kimjune01/sweep) is the contributor-side pipeline: scan repos, pick actionable issues, investigate via hypothesis graph, implement TDD, QA via Gemini volley, ship with embedded receipts. It's been running for weeks; the merge rate sits at 55%, calibrated to the 50% target where each outcome teaches something falsifiable.

immune is the same pipeline, run backwards. Sweep's perceive is "scan repos for issues"; immune's perceive is "incoming PR webhook." Sweep's filter is ai-policy + body-count + saturation; immune's filter is duplicate + reputation + policy. Sweep's attend is hypothesis graph + adversarial volley; immune's attend is replay test + LLM synthesis. Sweep's transmit is "ship a PR with receipts"; immune's transmit is "label a verdict the maintainer can read."

Together they close the loop. What sweep produces, immune consumes. What immune accepts, the maintainer reviews. Each pipeline runs the same six morphisms; they compose end-to-end into a closed loop where receipts are produced and validated under the same contract.

## What it isn't

immune doesn't decide. immune doesn't merge. immune doesn't close PRs unless the maintainer explicitly opted into `gate` mode and the rejection happened at filter (no LLM in the loop). The model writes synthesis, not policy. The maintainer is always the final stage.

immune doesn't punish good contributors. The mechanical filter is calibrated against the repo's own merge norm — what worked here before. Reputation lookup uses GitHub's own merge history, no third-party score. A first-time contributor with a clean fix gets the same treatment as a regular; the difference is the regular's prior receipts compound, so they get faster attention.

immune doesn't replace the maintainer. The whole point is to give the maintainer back time to spend on the calls that matter — the architectural choices, the boundary cases, the tone in code review. Mechanical evaluation goes to the action; judgment stays with the human.

## The bet

Receipts-discipline as a norm. The contributor-side pipeline (sweep) produces them. The maintainer-side pipeline (immune) validates them. When enough maintainers run a receipt-validating gate, contributor pipelines have a real incentive to produce real receipts. The norm becomes self-enforcing: pipelines without receipts get sedimented, pipelines with receipts get reviewed. The bar rises until the average AI PR is better than the average human PR, because the human PR doesn't carry receipts and never had to.

That's the endgame. Not "AI replaces maintainers." Not "AI floods OSS with slop." Maintainers reading second-order receipts to allocate the only finite resource — their attention — toward the contributions that actually move the project forward. Every other contribution sediments, which is correct.

`(PR) → merged`. That function, made cheap.

---

*[immune is open source](https://github.com/kimjune01/immune). Code AGPL-3.0, prose [CC-BY-SA-NS](/cc-by-sa-ns). Drop the action into `.github/workflows/` and watch your queue stop filling with noise.*

*Written with Claude Opus 4.7 via [Claude Code](https://claude.ai/claude-code). The pipeline that writes this post is the same shape as the pipeline it's about.*
