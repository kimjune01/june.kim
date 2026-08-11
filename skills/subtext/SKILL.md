---
name: subtext
description: Infer a repo's real roadmap from between the issues and PRs. Takes a repo (owner/name) as argument, mines demand signals the tracker can't state directly (maintainer time allocation, review latency, deliberation venues, label archaeology), and outputs a loosely prioritized roadmap (now/next/someday/declined bands with receipts) plus contribution openings. The tracker is the text; demand is the subtext.
---

# Subtext: Read the Roadmap Nobody Published

Formal roadmaps are stale aspirations. The real roadmap leaks continuously through what maintainers do under time scarcity. This skill recovers it for a target repo and names where a contribution would land on existing demand instead of merit alone.

Principle (from H26, anchore-syft): written review comments and issue replies are compressed to the minimum actionable ask. The concern that generated them lives in the venue where the team actually deliberates. Satisfying the text while missing the subtext leaves work stalled; answering the subtext gets same-day engagement.

## Input

`ARGUMENTS` is the repo, as `owner/name`, a GitHub URL, or a local checkout path (resolve to `owner/name` via `git remote`). Optionally followed by a focus area ("issue 4760", "the parser subsystem").

## Process

### 1. Identify who holds the ranking function

The roadmap is in specific heads. Find them before reading anything else.

```bash
gh api repos/O/R --jq '{org: .owner.login, default_branch, pushed_at}'
# who merges (the merge button is the ranking function made visible)
gh pr list --repo O/R --state merged --limit 50 --json mergedBy --jq '[.[].mergedBy.login] | group_by(.) | map({who: .[0], n: length}) | sort_by(-.n)'
# who reviews vs who never shows up
gh pr list --repo O/R --state merged --limit 50 --json reviews --jq '[.[].reviews[].author.login] | group_by(.) | map({who: .[0], n: length}) | sort_by(-.n)'
```

### 2. Mine the five signal tiers, most reliable first

**Tier 1 — maintainer time allocation.** What maintainers build with their own hands is the truest roadmap. List their recently authored PRs and self-assigned issues. A refactor a maintainer started and keeps touching is a load-in-motion; contributions that ride it get pulled, contributions that fight it get deferred.

```bash
gh pr list --repo O/R --author <maintainer> --state all --limit 20 --json title,createdAt,state
```

**Tier 2 — public deliberation venues.** Livestreams, community calls, office hours, conference talks, podcast episodes. This is where reasoning leaks, not just priorities. WebSearch for `<project> livestream OR "community meeting" OR "office hours"`; check the README/docs for a meeting cadence. If a transcript or recording exists for a relevant discussion, get it and read it, because one stream segment can outweigh the entire tracker. Note: unlabeled transcripts do not support speaker attribution; write "the team discussed", never a guessed name.

**Tier 3 — issue metadata over issue text.** Labels (`accepted`, `help-wanted`, `triaged`), milestone membership, and maintainer *touches* (relabels, reopens, self-assigns). An issue a maintainer touched twice in a month is roadmap. An issue with 40 reactions and zero maintainer comments is declined demand; user enthusiasm the maintainers have chosen not to adopt is a trap target.

```bash
gh issue list --repo O/R --label accepted --limit 30 --json number,title,updatedAt
gh api "repos/O/R/issues?sort=updated&per_page=30" --jq '.[] | {n: .number, title: .title, comments, reactions: .reactions.total_count}'
```

**Tier 4 — the company behind the project.** For commercial OSS, the paid product's announcements and the compliance environment drive OSS priorities with a lag. WebSearch the org's blog and product pages; note anything the OSS tracker is silently converging toward.

**Tier 5 — release-note archaeology.** What ships half-done across consecutive releases is actively wanted. What was announced once and never mentioned again is dead; do not build on it.

### 3. Measure latency asymmetries

Latency is the honest opinion. Compute rough response gaps: maintainer first-response time on recent issues/PRs, split by author association (MEMBER vs CONTRIBUTOR vs NONE) and by topic. A subsystem where maintainers answer in hours is an itch; one where 70-day silences are normal is not on the roadmap regardless of what the labels claim. Note who breaks silences and what event breaks them (a release, a stream, an external mention).

### 4. Produce the roadmap

The output is a loosely prioritized roadmap: the ordered list of what this project is actually going to work on next, as if the maintainers had written it down. Write to `~/Documents/sweep/repo-hypotheses/<owner>-<repo>-subtext.md` (append a dated section if the file exists).

Each roadmap entry carries:
- the work item, stated in the project's own vocabulary
- priority band (**now** / **next** / **someday** / **declined**), loosely ordered within bands; false precision is worse than honest looseness
- the evidence tiers behind it, with receipts (links, latency numbers, stream timestamps); mark single-source entries
- whose head it lives in (which ranking-function holder)

The **declined** band is real roadmap: high-reaction, maintainer-silent areas the project has chosen not to do, named so enthusiasm doesn't misread as opportunity.

Two short appendices after the roadmap:
- **Venues**: where deliberation actually happens and its cadence; presence there converts better than any artifact.
- **Openings**: 2-3 roadmap entries where an outside contribution would land on existing demand, each with the compressed written ask if one exists, the uncompressed concern behind it, and a falsifiable prediction of what engagement looks like if the reading is right (H26 style, two-sided where possible).

### 5. Verification discipline

Every quote fetched before included (composite near-quotes are a known failure). Every latency number traceable to a listed API call. Speaker attribution only from labeled sources. Where a signal rests on one tier only, mark it single-source. The report should survive the repo's own maintainers reading it.

## Scale

Small repo (< ~500 issues): run inline. Large repo or multi-subsystem focus: fan out Explore/general-purpose agents per tier or per subsystem and synthesize; the tiers are independent until the Targets section, which needs all of them.

## What this skill is not

- Not a code audit; it reads people and cadence, not correctness.
- Not a popularity contest; reactions and stars are user demand, and the skill ranks maintainer demand, which is what merges.
- Not a substitute for showing up: the report's Venues section exists because presence at office hours converts better than any artifact alone.
