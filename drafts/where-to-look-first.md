# Where to look first: published demand

The rule this file enforces: only serve a want someone has already published. A fix for a filed issue is welcome; the same fix, unasked, is an intrusion. Every surface below is a place where eval-world states its demand out loud, so your diagnostic instinct lands the way your 111 merged PRs did and not the way the cold audits did.

Ordered by how often it fires:
- **Tier 1, harness issue trackers** — the daily engine. Your proven channel, and every merged fix warms a team that hires eval engineers.
- **Tier 2, job reqs** — the periodic high-value shot. A posting is an org's filed issue.
- **Tier 3, stated limitations** — the occasional bonus, demand printed in a paper.

Verify repo paths before relying on them; a couple of these orgs migrated recently (flagged inline).

---

## Tier 1 — eval-harness issue trackers (check daily)

First, a gate: only trackers where **maintainers actually respond** count. A repo that dumps code and lets issues and PRs sit (OpenAI's OSS is the classic case) has no *served* demand, so a PR there rots like a cold audit. Check the recent-PR merge cadence before investing.

For each: open the issues tab, filter by labels `help wanted`, `good first issue`, `bug`, and **prioritize issues the maintainer filed themselves** — a self-filed issue is the strongest admission of pain on the page. Run `/subtext <org>/<repo>` on each to surface demand the labels don't state. A merged PR here is simultaneously your winning move, your credential, and a warm intro to the org that maintains it.

| Repo | Maintained by (= hiring org) | Notes |
|---|---|---|
| `UKGovernmentBEIS/inspect_ai` | AISI / Meridian | The framework. Confirm org hasn't moved to a Meridian namespace. |
| `UKGovernmentBEIS/inspect_evals` | AISI / Meridian (Alexandra Abbas) | Eval **content** repo — most construct-validity-relevant. Best single target. |
| `harbor-framework/harbor` | Laude (Alex Shaw) | Moved from `laude-institute/*`. Very active. |
| `harbor-framework/terminal-bench` | Laude | Your existing campaign (harbor#2266) lives near here. |
| `EleutherAI/lm-evaluation-harness` | EleutherAI | High issue volume, stable, welcoming to outside PRs. |
| `swe-bench/SWE-bench` | SWE-bench team | Migrated from `princeton-nlp` (old links redirect). |
| `All-Hands-AI/OpenHands` | All Hands AI | Dominant open coding-agent scaffold, MIT, ~82k stars, very active. Ships its own **benchmark-evaluation harness** (SWE-bench + many others), so construct-validity/harness issues live here — your content, not just adjacent. All Hands co-built Mistral's Devstral. Strong Tier 1. |
| `humanlayer/humanlayer` | HumanLayer (YC F24, Dex Horthy) | Agent-orchestration / coding-agent IDE+SDK, Apache-2.0, ~11k stars, active. Agent-tooling adjacent, not a pure eval harness — a contribution-and-relationship surface more than an eval-content one. `12-factor-agents` and `agentcontrolplane` are the other live repos. |

Confirm before adding: METR's public eval repos (they migrated off `vivaria` onto Inspect — find the current wrapper), and any public Epoch benchmarking repo (they run on Inspect).

---

## Tier 2 — job reqs (check weekly; subscribe, don't check)

A posting states the exact pain and lands in a channel whose job is to answer you. Read each as an issue and tailor the contribution to what it names. Links rotate — set alerts rather than bookmarking.

Org boards (from the outreach queue):
- Scale SEAL — labs.scale.com/jobs , scale.com/careers
- OpenAI — openai.com/careers (filter "evals")
- METR — jobs.lever.co/metr
- Vals AI — jobs.ashbyhq.com/vals-ai
- Anthropic — job-boards.greenhouse.io/anthropic (filter "eval")
- Mistral — jobs.lever.co/mistral
- Cohere — jobs.ashbyhq.com/cohere
- Epoch AI — jobs.lever.co/epoch-ai
- Arena (ex-LMArena) — jobs.ashbyhq.com/arena

Aggregators:
- HN monthly "Who is hiring" thread (your `/hn-feed` already polls HN)
- 80,000 Hours job board — jobs.80000hours.org
- aisafety.jobs

---

## Tier 3 — stated limitations & solicited feedback (check as you read)

Demand printed in prose. Lower frequency, but unambiguous invitations.
- The **Limitations** and **Future work** sections of benchmark papers — the authors listing, in print, what they know is weak.
- RFCs, roadmap threads, GitHub Discussions, and maintainer Discords/Zulips where someone asks "how should we handle X."
- A maintainer publicly conceding "we know X is broken." That sentence is a filed issue.

---

## The bridge move (for a problem you found that nobody published)

Don't audit it at them. Ask a question that lets *them* file the issue. "Does Pro's grader handle deletion?" invites the maintainer to concede the gap in their own words. The moment they do, your finding is voiced demand and your help is welcome. You convert manufactured demand into stated demand by making them the author of the complaint.

---

## Weekly loop

- **Daily-ish:** scan Tier 1 trackers, pick one or two published/maintainer-filed issues, PR them.
- **Weekly:** sweep Tier 2 boards + the HN hiring thread for new reqs; apply, attaching the matching audit as evidence, not as the pitch.
- **As you read:** log any Tier 3 limitation you spot against the repo it belongs to.

The point is never to go find demand. It is to stand where demand gets published and serve it when it appears.
