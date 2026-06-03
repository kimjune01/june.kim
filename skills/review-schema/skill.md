---
name: review-schema
description: Build a hypothesis graph of a repo's review culture. Induces gates (instant-reject checks), signals (quality gradient), and tiebreaker (maintainer taste) from PR history. Gate before /triage.
argument-hint: <repo> [--override "signal: line_delta"] [--manual]
allowed-tools: Read, Write, Edit, Bash, Agent, AskUserQuestion
---

# Review Schema

Build a hypothesis graph of a repo's review culture. Each gate, signal, and tiebreaker is a hypothesis about what the maintainer checks — with evidence, counterexamples, confidence, and a falsification condition. Every PR outcome updates the graph.

## The data structure

Three layers, each a set of hypotheses:

```
gates:      [tests, ci]                              # binary pass/fail, checked first
signals:    [diff_size, line_delta, code_clarity]     # gradient, checked after gates pass
tiebreaker: simplification                           # taste — wins when signals are ambiguous
```

**Gates** are hypotheses about mechanical rejection. "H: this repo rejects PRs without tests." Falsified by a PR merged without tests. Confidence rises with each rejection that cites missing tests; drops with each counterexample.

**Signals** are hypotheses about quality gradient. "H: smaller diffs merge faster." Falsified by large diffs that merge faster than small ones. Each carries a distribution from merged PRs.

**Tiebreaker** is the weakest hypothesis — hardest to induce, easiest to falsify. "H: the maintainer values simplification over performance." Evidence comes from praise language on merged PRs, but praise often masks the real decision driver. Mark confidence honestly.

## Input

A GitHub repo (`owner/repo` or local path with `origin` remote). Optional:
- `--override "gate: rebase"` — manually add a gate/signal/tiebreaker
- `--manual` — skip induction, build the schema interactively from what you already know

## Output

Review schema written to `~/.sweep/repos/<owner>-<repo>/review-schema.md`:

```markdown
# Review Schema: tinygrad/tinygrad

Induced from 47 merged PRs + 12 reviewed-and-rejected PRs (2026-04 to 2026-05).

## Gates

### tests
- type: hard
- confidence: high
- evidence: #123, #141, #155 rejected citing missing tests (hotz: "not enough regression tests")
- counterexamples: #160 docs-only merged without tests
- falsification: a code-change PR merged without tests
- rule: code behavior changes need regression tests. Docs, refactors, build fixes may not.

### ci
- type: hard
- confidence: high
- evidence: no PR merged with red CI in sample
- counterexamples: none
- falsification: a PR merged with failing checks

## Signals

### diff_size
- confidence: high
- distribution: median 23 lines, p25 11, p75 52, p90 89
- interpretation: PRs under ~100 lines merge faster unless authored by maintainers
- falsification: merge time uncorrelated with diff size over next 20 PRs

### line_delta
- confidence: medium
- distribution: 68% of merges net-negative or zero
- evidence: `sz.py` tracked in CI, negative deltas merged faster
- falsification: net-positive PRs merge at the same rate

### code_clarity
- confidence: medium
- evidence: merged PRs have minimal descriptions — the diff reads without context
- falsification: PRs with detailed descriptions merge faster

## Tiebreaker

### simplification
- confidence: low
- evidence: praise language in #122, #139 ("clean", "nice", "simple")
- note: sparse evidence. Maintainers may praise style while merging for correctness or urgency.
- falsification: a PR that adds complexity beats a simplifying PR on the same problem

## Process depth: shallow
- external complex merges: 0 in sample (only trivial external PRs merged)
- review engagement: single-comment close on 11/12 rejected PRs
- time-to-decision: median <2 minutes on external PRs
- substantive feedback on rejections: rare ("I don't understand" without follow-up)
- falsification: an external contributor merges a >50 line PR after multi-round review
- fit: pipeline should produce only obvious, tiny PRs. Investigation depth is wasted.
```

## Process

### 1. Gather PR history

Parse `repos.jsonl` (last-action-wins per repo) for this repo's `last_fetched` timestamp. On first run, fetch the full window. On subsequent runs, fetch only what's new. After fetching, append a `fetch` event with the new timestamp.

```bash
# First run: full window
gh pr list --repo <repo> --state merged --limit 50 --json number,title,author,additions,deletions,files,reviewDecision,reviews,comments,mergedAt,body
gh pr list --repo <repo> --state closed --limit 30 --json number,title,author,additions,deletions,files,reviews,comments,closedAt,body,mergedAt

# Subsequent runs: incremental (--search filters by date)
gh pr list --repo <repo> --state merged --search "merged:>YYYY-MM-DD" --json number,title,author,additions,deletions,files,reviewDecision,reviews,comments,mergedAt,body
gh pr list --repo <repo> --state closed --search "closed:>YYYY-MM-DD" --json number,title,author,additions,deletions,files,reviews,comments,closedAt,body,mergedAt
```

After fetching, append a `last_fetched` entry to `repos.jsonl`:
```jsonl
{"ts":"2026-05-09T...","action":"fetched","repo":"owner/repo","last_fetched":"2026-05-09T..."}
```

The JSONL is the cache. PR history doesn't change retroactively. Only fetch what's new.

**Filter closed PRs.** Only keep reviewed-and-rejected: PRs where a maintainer left review comments before closing. Exclude:
- `mergedAt != null` (merged, not rejected)
- Author-closed with no review comments (abandoned, not rejected)
- Bot PRs (dependabot, renovate, etc.)
- Duplicates / superseded (author opened a replacement PR)
- Stale PRs closed by stalebot

The remaining set is PRs the maintainer actively rejected. These are the useful negative examples.

**Recency weighting.** Last 3–6 months matter most. Older PRs are context, not signal, unless volume is low.

### 2. Induce gates

Scan rejected PRs and review comments for rejection patterns.

| Pattern in review comments | Gate hypothesis |
|---|---|
| "needs tests", "add a test", "no regression test" | `tests` |
| "CI is red", "fix CI", "checks failing" | `ci` |
| "rebase", "merge conflicts", "out of date" | `rebase` |
| "too large", "split this up" | `max_diff_size` |
| "not the right approach", "wrong direction" | `alignment` — **skip the issue entirely**. Pre-discussion means politics. Not worth it. |

Also check non-comment sources:
- CI config (required checks = hard gates enforced by GitHub, not just maintainer preference)
- PR templates (required sections = expected evidence)
- CONTRIBUTING.md (stated policy)

**Confidence assignment:**
- `high` — 3+ explicit rejections citing this pattern, or enforced by CI/GitHub settings
- `medium` — 1–2 rejections, or inferred from merged PR norms (all merged PRs have tests, but nobody explicitly asked for them)
- `low` — inferred from absence or sparse evidence. Needs user validation.

**Counterexamples.** For each gate hypothesis, actively look for merged PRs that violate it. A gate with counterexamples is softer than one without. Note the counterexample category (docs-only, maintainer-authored, trivial fix).

### 3. Induce signals

Analyze merged PRs for the quality gradient.

- **diff_size**: compute median, p25, p75, p90 of `additions + deletions`
- **line_delta**: compute `additions - deletions` distribution. What fraction are net-negative?
- **description_length**: do merged PRs have long descriptions or minimal ones?
- **test_ratio**: lines of test code vs lines of implementation
- **time_to_merge**: fast merges share characteristics — but control for author (maintainer self-merges are fast regardless of quality)
- **files_touched**: single-file PRs vs multi-file — which merge faster?

**Author normalization.** Separate maintainer-authored PRs from external contributions. Maintainers merge their own PRs with different standards.

Drop signals that don't discriminate after normalization.

### 4. Induce tiebreaker

Read maintainer comments on merged PRs. Look for praise language:

- "clean", "simple", "elegant" → candidate: **simplification**
- "fast", "nice perf", "good numbers" → candidate: **performance**
- "great tests", "thorough" → candidate: **correctness**
- "needed this", "finally", "been wanting" → candidate: **demand**

The most frequent praise category is the candidate tiebreaker. If evidence is sparse or contradictory, mark confidence `low` and validate with user. If no praise language found, mark tiebreaker `unknown`.

### 5. Check unstated gates

Eight categories. Each is a deduction — check the hypothesis against PR history. The categories are finite; the test is mechanical.

| Gate | Hypothesis | Test | Kill signal |
|---|---|---|---|
| **Standing** | outsiders without history can't merge complex PRs | has a first-time contributor merged a >20 line PR? | no → gate exists |
| **Volume** | too many PRs too fast triggers rejection | has any contributor been warned about volume or frequency? | yes → gate exists. Check review comments for "slow down", "too many", "flooding" |
| **AI detection** | AI-looking prose triggers rejection | do review comments mention "AI", "generated", "ChatGPT", "LLM"? | yes → gate exists |
| **Domain ownership** | certain code areas reject external PRs | are external merges concentrated in specific directories? Do some dirs have zero external merges? | yes → gate exists for those dirs |
| **Philosophy** | the repo has unstated values that override technical merit | do rejections cite principles? ("we never trade X for Y", "not how we do things") | yes → gate exists. Record the principle. |
| **In-group** | core team PRs reviewed differently than outsider PRs | compare time-to-merge and review depth: core vs external, same PR size | significant difference → gate exists |
| **Timing** | merge rate varies with release cycle or maintainer bandwidth | are there dead periods where nothing merges? Do merges cluster? | yes → gate exists. Note the pattern. |
| **Channel** | contribution process requires off-platform communication | does CONTRIBUTING.md or review comments reference Discord, Slack, mailing list, "discuss first"? | yes → gate exists. Pipeline can't pass it — kill the repo. |
| **Hiring** | PRs are auditions, not contributions — maintainer is evaluating the person, not the patch | do maintainers reference hiring, team fit, or "show me you understand"? Are merged external contributors later hired or given commit access? | yes → gate exists. Pipeline can't audition — kill the repo. |

For each gate that exists, write it to the schema with evidence and confidence. Gates that don't exist get marked `absent` — that's a positive signal.

### 6. Assess process depth

Score how deep the repo's review process goes. This determines whether the pipeline's output (investigation-backed PRs) is compatible with the repo's intake capacity.

**Depth signals** (from the PR history already gathered):

```bash
# External contributor merges (the key query)
# From merged PRs: filter where author is NOT in maintainer/collaborator set
# Then: how complex were they? (additions+deletions, files touched, review rounds)

# Review engagement depth
# From merged PRs: count review comments per PR, count review rounds (back-and-forth)
# From closed PRs: did maintainers give substantive feedback or just close?
```

Score each:

| Signal | Depth+ | Shallow+ |
|---|---|---|
| External contributors merged complex PRs (>50 lines) | yes | no external merges, or only trivial ones |
| Review threads have multi-round back-and-forth | 2+ rounds common | single comment or silent merge |
| Maintainers ask follow-up questions | yes | close without engaging |
| Time-to-decision on external PRs | >1 hour median | <5 minutes (glance-merge or glance-close) |
| Rejected PRs get substantive feedback | explains what's wrong | just closes |

**Gate automation** (detectable from GitHub API):

```bash
# Branch protection rules
gh api repos/<owner>/<repo>/branches/main/protection --jq '{
  required_reviews: .required_pull_request_reviews.required_approving_review_count,
  required_checks: .required_status_checks.contexts,
  codeowners: .required_pull_request_reviews.require_code_owner_reviews
}'
```

| Signal | Automated gates | Human-bottleneck gates |
|---|---|---|
| Required review count | 1+ required reviewers | 0 (maintainer reviews at will) |
| Required status checks | CI checks block merge | CI is advisory, maintainer overrides |
| CODEOWNERS | review routed by file path | one person reviews everything |
| Branch protection | enforced by GitHub | no protection rules |

Automated gates decouple throughput from one person's attention. The pipeline should prefer repos where the gates are in the infrastructure, not in one person's head.

**Process depth score:**
- `deep` — automated gates, external complex PRs merge, multi-round reviews, substantive rejections. Pipeline's output fits. High throughput capacity.
- `moderate` — some automated gates, some external merges, some engagement. Pipeline should size down.
- `shallow` — no automated gates, one person is the gate. Glance-merge/glance-close. Throughput and latency capped at maintainer's attention budget. Only obvious, tiny PRs pass.

Write `process_depth` to the schema with evidence. `/sift` reads this to filter repos.

### 6. Write schema

Write to `~/.sweep/repos/<owner>-<repo>/review-schema.md` with the full hypothesis graph: evidence, counterexamples, confidence, and falsification conditions. Log what was induced. Don't block on user validation — the schema is a hypothesis, and PR outcomes will update it.

### 6. Validate (optional, not a gate)

If running interactively (not inside `/sweep`), present the induced schema and ask: "Does this match your experience? What's missing or wrong?" Accept overrides.

If running inside `/sweep`, skip validation entirely. The pipeline doesn't wait. User can override later with `/review-schema --manual <repo>`.

**Fallback to manual mode:** If fewer than 10 usable PRs (merged + reviewed-and-rejected), switch to `--manual`. Not enough data to induce — ask the user directly.

## Integration

- `/triage` reads the schema before scoring. Items that require evidence the schema can't provide (e.g., hardware benchmarks when the gate is `perf_evidence`) get deprioritized.
- `/triage` agents shape candidate PRs to match the schema: pass all gates, optimize for signals, aim for the tiebreaker.
- `/drip` tone matching reads the schema's signal layer. Description length, title format, level of detail come from the signals.
- `/drip` test gate maps to the schema's gate layer.
- `/retro` updates the schema after each PR outcome. Merged → evidence for current hypotheses. Rejected for unexpected reason → new gate hypothesis. Schema drift detected → re-induce.

## Manual mode

`/review-schema --manual <repo>` — skip induction, build from what you know:

1. "What gets a PR instantly rejected on this repo?"
2. "What do good PRs look like? Small diff? Tests? Benchmarks?"
3. "When two PRs are equally good, what makes the maintainer pick one over the other?"

Three questions, three layers. Write the schema from answers. Mark all confidence `low — user-reported, not induced`.

## When to run

- Before first `/triage` on a new repo
- After a ban, warning, or pattern of rejections (re-induce — the schema may have drifted)
- After `/retro` flags a shift in merge patterns

## Rules

- **The schema is a hypothesis graph.** Every entry is a hypothesis about review culture, not ground truth. Evidence, counterexamples, confidence, falsification condition — all required.
- **Induce, don't assume.** The schema comes from the repo's own history. Absence of review comments is not evidence of absence — check CI config, templates, and merged PR norms.
- **Filter your negative examples.** Closed-without-merge is noisy. Only PRs with review comments from maintainers count as rejections.
- **Every PR outcome updates the graph.** Merged → evidence. Rejected for predicted reason → confirmation. Rejected for unpredicted reason → new hypothesis. The schema evolves.
- **Mark confidence honestly.** When evidence is weak, say so. The tiebreaker will almost always be `low` confidence — that's fine. A weak hypothesis is better than no hypothesis.
- **Don't block the pipeline.** Induce, write, proceed. Validation is optional and never a gate. The schema updates itself from PR outcomes — wrong hypotheses die on contact with reality.
