---
name: sift
description: Sift through candidates surfaced by /scout — fetch issues, screen for receipts, deposit survivors into /triage's inbox. Dedupes against ~/.sweep/seen/issues.txt to avoid resurfacing. Renamed from /prospect (and earlier /actionable).
argument-hint: [--dry-run]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Sift

Sift through scout's candidates for work worth doing. Start from intent, not repos. Renamed from `/prospect` (and earlier `/actionable`) — same shape, name better describes the role (filter through noise to find value worth extracting, hand off to /triage).

Work worth doing is anything the maintainer wants done — bugs are a subset. The full space is **desirable improvements**: bugs, planned features, roadmap items, conformance gaps, performance targets, doc holes. The common thread is maintainer pre-commitment: they signaled they want this, nobody's doing it, and the acceptance criteria are readable.

## What makes a good candidate

An item where:
1. **Maintainer signaled intent** — they opened it, commented, labeled it, added it to a milestone, listed it in a roadmap, pinned it, or wrote "PRs welcome"
2. **Receipts of reasoning are producible** — the work can be defended with a hypothesis graph (reasoning trace) and test attestations (evidence). The real outcomes are value delivered to maintainers and learning extracted by the pipeline. Both are unmeasurable. Merge rate is the most legible proxy, but optimizing the proxy is Goodhart.
   
   When a category of work hits high merge rate, that's a signal it's saturated, not a signal to do more of it. Saturation means the pipeline isn't learning anymore and the maintainer isn't getting marginal value beyond the obvious. The mix should ratchet toward harder work over time, the same way the detector floor ratchets up. Two tracks coexist:
   - **Standing track** (mechanical fixes): high merge rate, low learning signal, low marginal value once a few have shipped per repo. Use sparingly at cold-tier repos to establish standing, then move on.
   - **Learning track** (hypothesis-rich PRs): bugs with reproducers needing investigation, behavior disputes, performance regressions, conformance failures, architectural choices with measurable answers. Lower merge rate but every outcome — merge or close — teaches something falsifiable. Prefer this track.
   
   Diff size doesn't gate. Information-content does. Pick work where the maintainer gains real queue relief and the pipeline gains real evidence about what it can and can't do. Watch the merge rate, but don't optimize for it.
   
   **Calibration target: 50% merge rate.** Under shifting constraints (the criterion keeps ratcheting up), 50% is the rate that maximizes outcome entropy — each PR is genuinely uncertain, so each merge or close delivers the maximum bit of learning. Above 50% means the bar is too low (we're picking saturated work). Below 50% means over-reach (the work is wrong or the standing isn't there). Hold the rate near 50% by ratcheting difficulty up as the pipeline gets better. Same principle as active learning's uncertainty sampling: label the uncertain examples first because they teach the most.
3. **Nobody's working on it** — no assigned contributor, no open PR addressing it
4. **The repo has a harness** — CI + bench that gives a definitive yes/no before you submit
5. **Estimated fix fits the merge ceiling** — check the repo's merged PR size distribution (from review schema or retro). If the median external merge is ~30 lines and the fix looks like 500+, score it down hard. Prior PRs at 10-50x the merge ceiling don't land regardless of quality.

**Failure paths produce receipts too.** An investigation that can't reproduce the bug isn't waste. The hypothesis graph (here's what we tried, here's why each branch failed) plus a recommendation to close (or to mark "needs more info") is a real contribution to the maintainer's queue. Don't filter out issues just because reproduction looks uncertain — investigate, document, and either ship a fix or post the receipts and recommend close. Both outcomes reduce the issue backlog. The only true waste is investigating without producing artifacts.

### Intent signals (strongest to weakest)

| Signal | Where to find it | Strength |
|---|---|---|
| Maintainer opened the issue | Issue author = repo owner/collaborator | Very strong — they defined the problem |
| Milestone assignment | `gh issue view --json milestone` | Strong — scheduled, not aspirational |
| Roadmap / tracking issue | Pinned issues, `ROADMAP.md`, `TODO.md`, project boards | Strong — published plan |
| `enhancement` + maintainer comment | Issue labels + comment authors | Medium — acknowledged want |
| `help wanted` / `contributions welcome` | Issue labels | Medium — explicit invitation |
| `planned` / `accepted` / `next-release` labels | Issue labels | Medium — intent without urgency |
| `CONTRIBUTING.md` listing areas of help | Repo docs | Weak — general, not specific |
| `good first issue` | Issue labels | Weak — high competition, but standing-builder |

Bugs with reproducers are the safest entry point. Roadmap items with specs are the highest-leverage. Features without maintainer endorsement are noise — inventing problems.

## Sources

Only other people's repos. Never your own — you don't need a pipeline to work on your own code.

### 1. Repos you've already contributed to

```
gh api graphql -f query='{ viewer { contributionsCollection { pullRequestContributions(first: 100) { nodes { pullRequest { repository { nameWithOwner } } } } } } }'
```

Filter: not owned by you, still active, has open issues, not on cooldown. You have context, the maintainer knows your name.

### 2. Adjacent repos (expand from what works)

For repos with high merge rates, check the same org, same dependency graph, same topic tags. Retro says what "good" looks like — actionable finds more of it.

### 3. Cold search (multiple strategies)

Keyword trawling alone fails for niche skillsets. Use all of these:

**a. Label search (broad sweep)**
```
gh search issues --label "good first issue" --language <lang> --sort created --limit 200
gh search issues --label "help wanted" --language <lang> --sort created --limit 200
gh search issues --label "enhancement" --label "accepted" --language <lang> --sort created --limit 100
gh search issues --label "planned" --language <lang> --sort created --limit 100
```
Cast wide — 200 results per language per label. Score by issue quality. At 1000 slots, false positives are cheap; false negatives are expensive.

**b. Intent search (roadmap mining)**

Find items the maintainer already wants done — not just bugs, but planned improvements, conformance gaps, and accepted enhancements.

```bash
# Milestone items with no assignee — scheduled work nobody's claimed
gh api "repos/OWNER/REPO/milestones" --jq '.[].number' | while read ms; do
  gh api "repos/OWNER/REPO/issues?milestone=$ms&assignee=none&state=open&per_page=20" \
    --jq '.[] | "\(.number) \(.title)"'
done

# Pinned issues — maintainer's priorities
gh api "repos/OWNER/REPO/issues?state=open&per_page=100" \
  --jq '[.[] | select(.labels[]?.name | test("tracking|roadmap|planned|accepted|meta"))] | .[] | "\(.number) \(.title)"'

# Tracking issues with unchecked items
gh api "repos/OWNER/REPO/issues?state=open&per_page=50" \
  --jq '.[] | select(.body | test("- \\[ \\]")) | "\(.number) \(.title)"'
```

Roadmap files (`ROADMAP.md`, `TODO.md`, project boards) are also intent signals but aren't API-searchable across repos. Check them per-repo after the repo enters the roster.

**d. GitHub trending**
```
gh api /search/repositories?q=stars:>1000+pushed:>$(date -v-7d +%Y-%m-%d)&sort=updated&per_page=100
```
Active high-star repos. Filter for open good-first-issues. These repos have review bandwidth.

**e. Dependency graph traversal**
For repos where you've merged PRs, check their dependency tree:
```
gh api repos/OWNER/REPO/dependency-graph/sbom
```
Upstream dependencies often share maintainers. If you have standing in `ruff`, check `astral-sh/uv`, `astral-sh/ty`, etc.

**f. "Used by" expansion**
GitHub shows repos that depend on a project. High-star dependents of projects you've contributed to are warm leads — you understand the dependency.

**g. Topic cluster search**
```
gh search repos --topic=parser --topic=formatter --language=Go --sort=stars --limit 50
gh search repos --topic=linter --topic=type-checker --language=Python --sort=stars --limit 50
```
Find repos in the same domain as your highest-merge repos.

**h. Overwhelmed maintainer search (maintainer-first)**

Instead of "what's broken," ask "who needs help." Search for solo maintainers with popular repos and growing issue backlogs. The issue is secondary — any bug on their queue is welcome.

Profile: personal account (not org), top contributor has >80% of recent commits, open issues growing, last external PR was merged (proving they accept contributions).

```bash
# Search for CLI/TUI tools by personal accounts with issue backlogs
gh api search/repositories -X GET \
  -f "q=topic:cli stars:>200 pushed:>$(date -v-30d +%Y-%m-%d)" \
  -f "sort=updated" -f "per_page=20" \
  --jq '.items[] | "\(.full_name) (\(.stargazers_count)★, \(.open_issues_count) issues)"'
```

For each candidate, verify the solo-maintainer signal:
```bash
# Check if top contributor dominates
gh api "repos/OWNER/REPO/contributors?per_page=5" --jq '.[0].contributions, .[1].contributions // 0'
# Check if external PRs merge
gh pr list --repo OWNER/REPO --state merged --limit 5 --json author --jq '[.[] | .author.login] | unique'
```

Solo maintainer + popular tool + issue backlog + merge history = high-receptivity target. These maintainers appreciate the small stuff — cosmetic fixes, error messages, edge cases — because they don't have time for it themselves.

**Big repos are fine.** The pipeline has landed PRs on godot (90k★), pytorch (90k★), hyper, VictoriaMetrics, envoy, and polars. Large repos with active CI and clear contribution norms are often *easier* — they have established review processes, fast CI, and maintainers who expect external PRs. The constraint is merge ceiling (diff size vs repo norms), not repo size or star count. A 10-line fix on a 50k★ repo is more likely to merge than a 500-line fix on a 500★ repo.

**Retro note (2026-05-09):** Compiler/optimizer niche is too narrow for generic labels. But general bug fixes, error messages, and docs span all domains. The pipeline's skillset is "read code, find root cause, write fix" — not limited to compilers. Expand the search to any well-maintained repo with mechanical acceptance criteria.

**Retro note (2026-05-10):** Maintainer-first search found pvolok/mprocs (2.5k★, 65 issues, solo Rust maintainer) via ecosystem graph from existing roster repos. Issue-first search misses repos where the maintainer hasn't labeled issues yet.

**Retro note (2026-05-10):** Maintainer-first repos have 50-100+ open issues — pick the *easiest*, not the most interesting. On mprocs (65 issues) and onecli (228 issues), triage agents picked domain-heavy bugs (config-vs-state, security defaults) and gemini killed both. The maintainer doesn't need you to redesign their state model. They need the 30 boring items off their plate: typos, error messages, missing edge cases, doc fixes. For first contribution to a solo-maintainer repo, filter issues by estimated complexity ≤10 lines and labels like `docs`, `error-message`, `typo`, `good-first-issue`. Standing first, ambition second.

**Retro note (2026-05-14):** Standing tier unlocks ambition. Cold repos still need mechanical first contributions. But once standing exists (3+ merges, no warnings, recent reviewer engagement), the hypothesis-graph format itself is the gate, not diff size. A 200-line refactor with H0/H1/H2 + perturbations + evidence is more contributable than a 5-line typo at a hostile repo. The reader of the PR is the hypothesis graph; reviewers who accept that format absorb larger work because the graph reduces their review cost. Use the warm/hot tier to take on architecturally substantive issues that still close cleanly under investigation. Tier table:

| Standing | Issue criteria |
|---|---|
| Cold (0-2 merges) | mechanical only, ≤30 lines, label-tagged (`good first issue`, `bug`, `docs`) |
| Warm (3+ merges, no warnings) | hypothesis-graph-tractable bugs and maintainer-acknowledged features, ≤150 lines |
| Hot (5+ merges, recent positive review) | architecturally substantive issues with a closeable graph, no hard line cap; bug-hunt unlocked |

## What to skip

- Items with no maintainer response — until they engage, you don't know if they want it done
- Items with active discussion or assigned contributors — someone's on it
- **Issues with an existing open PR** — always run `gh pr list --repo OWNER/REPO --search "KEYWORD" --state open` before scoring. If a PR exists and was updated in the last 30 days, skip. If stale (>30 days, no reviews), note as opportunity to pick up the stalled work. Retro 2026-05-09: gemini-cli #25693 and #25689 both had competing PRs (#25728, #25729) that triage agents discovered only after full investigation.
- Feature requests with no maintainer endorsement — inventing problems, not solving them
- Issues that need hardware you don't have — can't verify
- **Fix exceeds merge ceiling** — if the estimated diff is >3x the repo's median merged PR size for external contributors, skip. A 2000-line feature on a repo that merges 30-line fixes is dead on arrival.
- **Repos with `process_depth: shallow`** in their review schema — the pipeline produces investigation-backed PRs. Shallow-review repos can't absorb them. Only add shallow repos if the issue is trivial enough that investigation depth is unnecessary (1-line fix, obvious bug, failing test with known cause).
- **Bot-magnet issues** — run `~/.sweep/bin/body-count <repo> <issue-number>`. If verdict is `"skip"` (3+ distinct unmerged authors), the issue is a honeypot. The signal isn't "nobody solved it yet," it's "the maintainer is tired of closing these."
- **AI policy repos** — run `~/.sweep/bin/ai-policy <owner/repo>`. If `detected: true`, don't add to roster. Unless `--dry-run`, run `~/.sweep/bin/offer-slop-filter <owner/repo>` — it checks the banlist, dedupes against existing issues, opens the slop filter issue from the template, and logs to candidates.jsonl. One script, idempotent. In dry-run, log the candidate but don't open the issue.
- **GUI/TUI application repos** — skip repos where the primary artifact is a graphical or terminal UI application. These require visual verification the agent can't do and have opinionated render architectures (dirty flags, event loops, frame limiters) that resist automated fixes. Libraries that provide UI primitives (ratatui, egui) are borderline — fixes may be testable. But apps built on them (jellyfin-tui, terminal dashboards, desktop apps) are out. jellyfin-tui taught this: bug-hunt diagnosed correctly, pipeline still pushed wrong fix, maintainer said "ai slop."

## Output

Updated `~/.sweep/repos.jsonl`. Log additions and removals to `~/.sweep/actionable/candidates.jsonl`.

## Diversity selection

Don't just rank by quality and take the top-k. That clusters — you'd end up with 10 Python ML repos. The pipeline learns faster from diverse repos than correlated ones.

After scoring candidates, select the final set using DPP-style diversity. Each candidate repo gets a feature vector:

| Feature | Why it matters |
|---|---|
| Language | different toolchains, different review norms |
| Domain | ML, systems, web, infra, devtools |
| Process depth | mix of shallow and deep tests different hypotheses |
| Org size | solo maintainer vs large team, different dynamics |
| Issue type | bugs, perf, correctness, docs |
| **Hypothesis gap** | which of H0-H6 does this repo test that existing repos don't? |

**Hypothesis-driven selection (retro 2026-05-09):** The pipeline is an experiment, not a merge optimizer. Each repo is a perturbation. Select repos that fill gaps in the hypothesis coverage, not just feature-vector distance. Ask "which hypothesis does this test?" before "will this merge?" Specifically: fast-review repos test H3 (pacing), solo maintainers test H2/H5, AI-friendly repos test H4. A repo that fills a hypothesis gap is worth more than a high-merge-probability repo that duplicates an existing condition.

**Selection:** diversify strategies, not just results. Each parallel agent uses a **different search strategy** — one does label search, one does trending, one does dependency graph, one does topic clusters. Strategy diversity prevents correlated search spaces.

### d20 stochastic search

Three dice, three axes. Roll all three, build the query, fetch results, filter deterministically. No learning, no posterior, no feedback loop. The dice don't learn — you can't overfit a d20.

```bash
# Roll 3 queries (each is a d12 × d8 × d6 = 576 combinations)
python3 ~/.sweep/bin/roll-search.py 3
```

Dice tables live in `~/.sweep/bin/roll-search.py`:
- **d12 Language:** rust, go, python, typescript, cpp, java, csharp, kotlin, ruby, zig, swift, lua
- **d8 Signal:** unassigned bugs, silent bugs, discussed bugs, good-first-issue, help-wanted, upvoted bugs, kind/bug, broad bugs
- **d6 Sort+Size:** updated+mid, updated+small, reactions+large, created+any, comments+mid, updated+large

Each roll outputs a query + sort. Search with REST:
```bash
python3 ~/.sweep/bin/roll-search.py 3 | while IFS=$'\t' read -r query sort; do
  gh api search/issues -X GET -f "q=$query" -f "sort=${sort#sort:}" -f per_page=30 \
    --jq '.items[] | "\(.repository_url | split("/")[-2:]|join("/")) #\(.number) \(.title)"' 2>/dev/null
done
```

**Three rolls per invocation.** Each /actionable run rolls the dice three times, producing three independent queries. Results are pooled, deduped against `repos.jsonl`, then filtered deterministically (competing PRs, maintainer responsiveness, hypothesis coverage, merge ceiling, AI policy).

**Re-roll on empty.** If a roll returns zero new repos (all already in roster or filtered out), re-roll that leg. Max 3 re-rolls per leg. If still empty, that leg produced nothing — move on.

**No jitter, no weighting, no memory.** The dice are uniform. The filter is deterministic. The exploration comes from the dice. The quality comes from the filter. They don't talk to each other.

## Standing-gated bug hunt

When standing is high enough on a repo (3+ merged PRs, no warnings, no cooldown), the pipeline unlocks a new mode: run `/bug-hunt` on the repo blind — no issue required. Find bugs the maintainer doesn't know about, open the issue yourself, fix it yourself.

This is the endgame. The issue is your hypothesis. The PR is your fix. Your standing means the maintainer trusts your judgment about what's worth fixing.

**Threshold:** 3+ merged PRs on the repo, no active cooldown, no warnings in retro log. Check via drip queue history.

**Process:** spawn a `/bug-hunt` agent on the repo. If it finds something, open an issue with a reproducer, then file the fix as a separate PR linked to the issue. Same pipeline — issue-first — but you're creating the issue instead of claiming one.

**Risk:** this is exactly what got you banned on tinygrad — finding bugs without standing. The threshold gate prevents that. Don't skip it.

## Process

1. Read `~/.sweep/repos.jsonl` and `~/.sweep/retro-params/*.jsonl`. **Read `~/.sweep/banlist.txt` — these repos are permanently banned. Never add, investigate, or re-add a banned repo. The banlist is human-edited only.**
2. Score active repos. Drop dormant ones. Respect cooldowns.
3. For repos above the standing threshold (3+ merges), run standing-gated bug hunt.
4. Search for issues: contributed repos, then adjacent, then cold.
5. Score candidates by issue quality × repo fit.
6. Select final set via diversity selection (quality × distance in feature space).
7. Write updated `repos.jsonl` and `candidates.jsonl`.

## Eviction policy

The roster grows. It shouldn't grow forever. Evict repos that aren't producing value.

**Eviction triggers** (check on every actionable tick):

| Trigger | Threshold | Action |
|---|---|---|
| No activity in 7 days | latest `repos.jsonl` entry for this repo > 7d old, no open PRs, no pending items | re-evaluate; if nothing changed upstream, evict |
| No merged PR in 30 days | last merge > 30d ago | evict |
| All issues KILLED or BLOCKED | zero PENDING or CONFIRMED items | evict |
| Cooldown active with no end date | permanent ban | evict |
| Three consecutive rejections | 3 closed-without-merge in a row | evict |
| Repo archived or deleted upstream | `gh repo view` fails | evict |
| Process depth downgraded to shallow | retro reclassified after rejections | evict |

**Eviction means:** status → `evicted` in `repos.jsonl`. Drip queue drains naturally (don't abandon open PRs). State files kept in `~/.sweep/repos/<owner>-<repo>/` for reference. The repo can be re-added manually with `--add` but doesn't come back automatically.

**Soft eviction (demotion):** repos that aren't evicted but aren't producing get deprioritized. If a repo has open issues but no progress in 14 days, it drops below new candidates in the ranking. It stays on the roster but stops getting agent time until something changes (new issue, maintainer activity, retro parameter update).

## Rules

- **Respect cooldowns.** If retro says cooldown, don't add the repo.
- **1000 slots is effectively infinite.** At ~20 active repos, we're at 2% capacity. Add liberally — eviction handles pruning. Don't handpick; screen wide, let the pipeline surface what works.
- **Never your own repos.** Filter out repos where you are the owner. The pipeline is for contributing to other people's projects.
- **Add directly as `ready`.** No `pending_review` gate. Cold repos go straight to `ready` status. Eviction prunes repos that don't produce — the gate is downstream, not upstream.
- **Issue-first.** Don't add a repo unless there's a specific issue worth investigating. Repos without actionable issues are noise.
- **Mundane is fine.** Doc fixes, error messages, edge case handling — the agent doesn't get bored. Easy merges build contributor trust that makes harder PRs land later. Don't skip "good first issue" just because it's boring.
- **`--dry-run`** reports changes without writing.
