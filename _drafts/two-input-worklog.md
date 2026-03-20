---
layout: post
title: "Two-Input Workflow: Work Log"
tags: cognition coding
---

## Setup

**Date:** 2026-03-19

**Goal:** Apply the two-input workflow from [The Spec Is a Hypothesis](/the-spec-is-a-hypothesis) to a production system (gemini-cli), using codex (GPT-5.4) as the blind implementer.

**Three inputs for codex:**
1. **Ground truth** — `gemini-cli-experiment/` (fresh fork of upstream `google-gemini/gemini-cli`, main branch)
2. **Prose spec** — `union-find-compaction-for-gemini-cli/transformation-design.md`
3. **Prototype** — `union-find-compaction/compaction.py` (Python, framework-independent)

**What codex does NOT see:**
- The previous TypeScript implementation (`kimjune01/gemini-cli:feat/union-find-compaction`)
- The ten bugs found in code review
- The twenty spec revisions

**Codex's requested workflow** (from pre-experiment consultation):
1. Contradiction-finding pass before implementation
2. Authority rules: when spec conflicts with code, which wins?
3. Compact prompt shape: Goal / New architecture / Ground truth / Authority / Change boundary / Watch for

**Experiment question:** Does the structured two-input approach (prose spec + existing source + prototype, with contradiction-finding) produce fewer bugs than the original lossy pipeline?

---

## Step 1: How should codex elicit design decisions?

Asked codex (blind, before seeing any inputs) how it would surface ambiguities in a one-shot contradiction-finding pass.

**Codex's process:** Read TS ground truth first (invariants), prose spec second (conflicts), Python prototype last (existence proof, not truth). Produce a structured resolution document — not discussion — with four buckets:
1. Contradiction — sources disagree
2. Missing decision — no source defines it
3. Hidden invariant — behavior exists in code but isn't stated
4. Implementation-risk assumption — inferable but dangerous to guess

Each item is a forced-choice question with options and a risky default. No open-ended questions — every question names exact code paths and observable behavior.

**Codex wants 15+ decisions resolved upfront.** Categories: scope/ownership, terminology, algorithm semantics, correctness boundaries, ordering/stability, state/persistence, performance, failure handling, concurrency, compatibility/rollout, observability, test oracle.

**Compare to DESIGN_DECISIONS.md** (written by Claude during the prototype): 15 decisions, heavy overlap with codex's categories. But codex also flags things the original doc missed: ordering stability, failure handling, observability.

**The tension:** Codex wants full upfront resolution. The blog post argues the spec is a hypothesis — over-specifying before implementation is the same lossy pipeline, just front-loaded.

**Proposed authority rule instead:** "No regressions, UX improvement." This collapses most decisions: existing behavior is correct unless the spec explicitly changes it. Code wins on invariants, spec wins on the blocking path.

**Risk:** Decisions about new code paths (concurrency, message edits) aren't covered by "no regressions" because those paths don't exist yet. Those are exactly the ones that bit the prototype (10 bugs).

**Decision:** Try it lean. Send the three inputs with just the authority rule. See how many decisions codex still needs to force.

---

## Step 2: Contradiction-finding pass

Sent codex the three inputs with authority rule: "No regressions, UX improvement. Existing behavior is correct unless the spec explicitly changes it. Code wins on invariants. Spec wins on the blocking path."

Codex read TS ground truth first, then explored `geminiChat.ts`, `client.ts`, `config.ts`, `chatRecordingService.ts`, and `turn.ts` to establish invariants before comparing against the spec and prototype. Used 72,594 tokens.

**10 issues surfaced** (only ones the authority rule doesn't resolve):

| ID | Type | Issue |
|----|------|-------|
| `uf-entrypoint` | contradiction | Spec wants always-on `append()`/`render()`, but integration only swaps inside overflow-time `compress()`. Is union-find always-on, compression-only, or hybrid? |
| `uf-history-shape` | hidden invariant | Spec returns clusters as user messages, but current compression uses synthetic user + model envelope. What `Content[]` shape must union-find return? |
| `existing-session-routing` | missing decision | What condition forces flat mode for existing conversations when config says union-find? |
| `state-persistence` | contradiction | Spec promises cross-session clusters, but chat resets replace the `GeminiChat` object and recording schema has no forest storage. |
| `timestamp-source` | hidden invariant | Spec assumes per-message timestamps, but live `Content[]` doesn't carry them. |
| `hook-contract` | contradiction | Current `PreCompress` fires on every compression attempt; spec redefines it to fire on merge-triggering graduations. |
| `failure-backoff` | missing decision | Flat has explicit failure/backoff path; union-find background summarization has no defined retry suppression. |
| `background-scheduling` | missing decision | Spec assumes `resolveDirty()` runs during main LLM wait, but call graph only defines pre-request compression. |
| `incremental-ingest-key` | hidden invariant | Migration sketch relies on stable message IDs, but `Content` entries don't have them. |
| `content-serialization` | risky assumption | No defined serialization from structured `Content` to cluster text for embeddings and summaries. |

**Observation:** 10 issues vs 15 in the original `DESIGN_DECISIONS.md`. The authority rule collapsed 5+ decisions (hot zone size, model routing, recall threshold, test dataset, max cold clusters, merge threshold, retrieval strategy). The remaining 10 are structural — they can't be resolved by "no regressions" because they involve new code paths or type-level constraints the current system doesn't have.

**Next:** Human pushed back — "these are really in the weeds." Asked codex to self-triage.

---

## Step 3: Codex self-triage

Asked codex: "Of your 10 issues, which ones do you actually need the human to decide? Which can you resolve yourself by reading the code and following the authority rule?"

**Codex's answer: "Need from the human before coding: none."**

All 10 self-resolved under the authority rule:

| ID | Codex's resolution |
|----|-------------------|
| uf-entrypoint | Preserve current hybrid (manual `/compress` + auto threshold) |
| uf-history-shape | Hide union-find behind existing `Content[]` boundary |
| existing-session-routing | Fall back to flat when union-find state is missing |
| state-persistence | In-memory only for v1, no cross-session |
| timestamp-source | Use what exists, else ingest order |
| hook-contract | Don't expand, conform to current PreCompress |
| failure-backoff | Reuse existing compression failure behavior |
| background-scheduling | No new scheduler, run from current trigger path |
| incremental-ingest-key | Derive from session + turn order |
| content-serialization | Reuse existing text extraction (`historyExportUtils.ts`) |

Only potential escalation: if code forces a persisted on-disk format change.

**Key insight:** The authority rule ("no regressions, UX improvement") collapsed all 10 decisions. Codex's first pass frontloaded them as forced-choice questions because it was asked to. When pushed to be pragmatic, it recognized every one was answerable from the code + rule. The contradiction-finding pass was valuable not for the decisions it surfaced, but for forcing codex to read the ground truth deeply before writing code.

**Observation vs the original pipeline:** The original lossy pipeline (extract → design → implement) never did this pass. The 10 bugs found in code review were exactly the kind of hidden invariants codex just catalogued (history shape, hook contracts, failure backoff, serialization). Whether codex avoids those bugs during implementation is the experiment.

---

## Step 4: Implementation

Sent codex the full implementation task in `--full-auto` mode with all three inputs, the authority rule, the 10 self-resolved decisions, and explicit file structure instructions.

**Codex created 6 new files and modified 5 existing ones (492 lines added):**

| File | Role |
|------|------|
| `contextWindow.ts` (444 lines) | Forest (union-find), ContextWindow (hot/cold), cosine similarity, merge logic |
| `embeddingService.ts` (73 lines) | TF-IDF embedder with `embed()` / `embedQuery()` separation |
| `clusterSummarizer.ts` (47 lines) | LLM-based cluster summarization via `BaseLlmClient` |
| `contextWindow.test.ts` | 10 tests: graduation, overlap, embedQuery, dirty resolution, config validation |
| `embeddingService.test.ts` | 2 tests: vocabulary mutation, query isolation |
| `clusterSummarizer.test.ts` | 2 tests: prompt formatting, fallback on empty response |

**Modified files:**
- `chatCompressionService.ts` — dual-path: `compress()` dispatches to `compressWithFlat()` or `compactWithUnionFind()` based on `config.getCompressionConfig().strategy`
- `config.ts` — `CompressionConfig` interface with `strategy`, `hotSize`, `maxColdClusters`, `mergeThreshold`
- `geminiChat.ts` — `ContextWindow` state on the chat object, cleared on `setHistory()`/`clearHistory()`
- `chatCompressionService.test.ts` — 2 new union-find tests (snapshot fallback, tool truncation)
- `config.test.ts` — compression config defaults test

**Notable implementation choices:**
- `contentToContextString()` serializes structured `Content` to text for embeddings — handles text, functionCall, functionResponse
- Snapshot detection: falls back to flat if history contains `<state_snapshot>` and no ContextWindow exists
- `resolveDirty()` is fire-and-forget with `.catch()` logging — runs after render, doesn't block
- `drainMergeCount()` tracks merges for hook firing — only fires PreCompress when merges actually happened
- Ingest tracking via `contextWindowIngestedCount` on GeminiChat — avoids re-ingesting on repeated compression calls

**Codex could not run tests** — `node_modules` not installed in the fresh fork.

---

## Step 5: First test run

Installed dependencies, ran all tests.

**3 failures out of 46 tests:**

1. **`promptId` not defined** — `compactWithUnionFind()` used `promptId` but parameter was named `_promptId`. Variable name bug in the snapshot fallback path.
2. **Truncation marker not found** — union-find path serialized Content to text, losing the `Output too large.` marker from `truncateHistoryToBudget()`.
3. **Stale summary guard timeout** — test used deferred promise pattern but `resolveDirty()` deadlocked.

**Bug classification:**
- Bug 1: typo (below the function signature — the boundary from the blog post)
- Bug 2: serialization loss (content-serialization decision — one of the 10 codex catalogued)
- Bug 3: concurrency guard (the exact class of bug that hit the prototype)

---

## Step 6: Bug fixes

Sent codex the 3 failures. Fixed all three:
- Renamed `_promptId` → `promptId` usage
- Preserved raw `output`/`content` strings in tool response serialization
- Fixed `resolveDirty()` stale-root detection to avoid deadlock

**46 tests passing (4 test files, 0 failures).**

**Running comparison to original pipeline:**

| Metric | Original pipeline | Two-input workflow |
|--------|------------------|--------------------|
| Bugs found in first code review | 10 | 3 |
| Bug types | type contracts, concurrency, API surface | typo, serialization, concurrency |
| Decisions needed from human | 15 (DESIGN_DECISIONS.md) | 0 (authority rule resolved all) |
| Spec revisions | 20 | 0 (spec unchanged) |
| Implementation passes | 1 + fix cycle | 1 + 1 fix pass |

**Early observation:** 3 bugs vs 10. The contradiction-finding pass caught the categories but not the instances. Codex catalogued "content-serialization" as a risk, then hit exactly that bug. The concurrency guard (stale summary) reappeared — same class of bug as the prototype, suggesting this is genuinely hard regardless of workflow.

**Next:** Code review to find bugs codex's tests didn't catch.

---

## Step 7: Cross-implementation review

Showed codex both implementations side by side: its own (two-input workflow) and Claude's (original lossy pipeline). Asked for honest comparison.

**Codex's verdict: "Claude's is the better prototype. Yours is the better product integration."**

**5 bugs codex found in its own code:**
1. `resolveDirty()` stale fallback degrades to raw concatenation — permanently loses summary quality
2. Empty LLM summary → silently drops cluster content (falls back to single root message)
3. Summarizer errors uncaught → poisons entire resolve pass
4. All output flattened to `role: 'user'` — loses assistant/tool turn structure (major behavioral regression)
5. Pre-compress hooks under-fire (only on merges vs every compression attempt)

**6 bugs codex found in Claude's code:**
1. Non-persistent ContextWindow (rebuilt every call) defeats deferred summarization design
2. `await resolveDirty()` after render adds latency without improving output
3. Ingestion too lossy — tool names only, drops arguments and payloads
4. Hot-zone remapping fragile — `hotCount` vs Content count mismatch
5. No `<state_snapshot>` guard for existing conversations
6. `getCentroid()` doesn't canonicalize through `find()`

**Comparison to original code review:** The original code review found 10 bugs. Codex's self-review found 5 in its own code + 6 in Claude's. The bug *types* overlap: serialization loss, concurrency guards, lifecycle management. But codex's bugs are different *instances* — it avoided the prototype's specific bugs (embed() mutation, dirty-array race) while introducing new ones (flatten-to-user, uncaught summarizer errors).

**The key architectural divergence:** Codex persisted the ContextWindow on GeminiChat. Claude didn't. This is the biggest difference and it came from codex's contradiction-finding pass — it catalogued `state-persistence` as a decision and resolved it to "in-memory, on the chat object." Claude's pipeline never surfaced that question because the spec assumed persistence was handled elsewhere.

**Running totals:**

| | Original pipeline (Claude) | Two-input workflow (Codex) |
|---|---|---|
| Bugs at first test run | 10 | 3 |
| Bugs found in cross-review | 6 | 5 |
| Total unique bugs | 16 | 8 |
| Human decisions required | 15 | 0 |
| Architectural miss | Non-persistent ContextWindow | Flatten-to-user output |

---

## Discussion

**The authority rule did more work than the contradiction-finding pass.** Codex surfaced 10 issues, then self-resolved all of them once pushed to be pragmatic. The pass was useful as forced deep reading, not as a decision gate. Codex's own preferred workflow (frontload decisions) was the wrong call for codex.

**Both implementations missed at the same boundary — but different sides of it.** Claude dropped the ContextWindow lifetime (above the function signature — architectural). Codex dropped the Content structure (below the function signature — type-level). The spec defined neither. The blog post predicted this boundary but couldn't prevent it.

**The bug count halved, but the bug class didn't change.** Serialization loss, concurrency guards, lifecycle management — same categories, different instances. The two-input workflow reduced the surface area but didn't eliminate the failure mode.

**Codex is a better product integrator, Claude was a better prototyper.** Codex persisted state, added config, handled fallbacks. Claude preserved Content structure and caught summarizer failures. Prose carries architecture (codex's strength), code carries constraints (Claude's strength).

---

## Step 8: Claude's turn

Repeating the experiment with Claude (Opus) as the implementer, same directive. Claude subagent is blind — subagents don't inherit conversation context. It has not seen codex's implementation, the cross-review, or any of the discussion. Same conditions as codex: three inputs, authority rule, self-resolved decisions.

**Claude subagent results:** 80 tests passing (28 existing + 52 new), zero regressions. Modified only `chatCompressionService.ts` (no config or geminiChat changes). Created all 3 new service files + tests.

**Notable choices:**
- ContextWindow persisted on `ChatCompressionService._contextWindows` map (keyed by promptId), not on GeminiChat
- `<context_summaries>` XML wrapper for cold output
- Hot messages remapped from original `Content` objects (preserves roles/tool structure)
- Summarizer catches errors inside `resolveDirty()`, leaves dirty for retry
- `CompressionStrategy` enum instead of config string
- `compress()` API extended with optional `compressionStrategy` parameter
- Timestamps carried forward in dirty-input collection

---

## Step 9: Three-way comparison (codex as reviewer)

Showed codex all three implementations side by side. Asked for honest ranking.

**Codex's ranking: A > B > C**

| | A (original pipeline) | B (codex, two-input) | C (claude subagent, two-input) |
|---|---|---|---|
| Rank | 1st | 2nd | 3rd |
| Strength | Cleanest core, best history preservation | Best ingestion, best persistence model | Best error retry, best timestamp handling |
| Critical bug | Non-persistent ContextWindow, render-before-resolve | Flatten everything to `role: 'user'` | Broken incremental ingestion, wrong persistence key |

**Where all three agree** (likely correct):
- Union-find with path compression and union-by-rank
- Weighted centroid merge
- Hot/cold overlap model with graduate→evict lifecycle
- Synchronous append/render, async resolveDirty
- embedQuery() to prevent corpus contamination
- Hard cap with force-merge closest pairs

**Each one's unique contribution:**
- A: simplest concurrency guard (array-identity), preserves original Content for hot zone
- B: richest Content→text serialization, persistent ContextWindow on chat object, defensive `.catch()` on background work
- C: catches summarizer errors per-cluster (doesn't poison batch), carries timestamps into dirty inputs, shares cosineSimilarity utility

**Each one's unique bug:**
- A: rebuilds ContextWindow every call (defeats persistence), renders before resolving (wasted latency)
- B: flattens all output to synthetic user messages (destroys roles), stale fallback degrades to raw concatenation
- C: broken `alreadyAdded` logic (never re-ingests), keyed by promptId (wrong lifetime), drops force/failure parameters

**The surprise:** Codex ranked the original pipeline first — the one that had 10 bugs in the initial code review. The two-input implementations tried harder (persistence, config, richer ingestion) but introduced integration regressions the simpler implementation avoided. "Best minimality" was A's advantage.

**Interpretation:** The two-input workflow produced more ambitious implementations (both B and C attempted persistence, config, richer serialization). The original pipeline produced a more conservative one that stayed closer to the existing code's contracts. Ambition introduced bugs at the integration boundary. Conservatism left architectural gaps unfilled.

---

## Step 10: Synthesis (D)

Codex absorbed Claude subagent's improvements into its own implementation:
- Preserved original hot Content objects (fixed flatten-to-user)
- Cold summaries wrapped in user+model envelope (matches flat compression)
- Per-cluster error catching in resolveDirty() (leaves dirty for retry)
- Removed stale-root fallback that degraded to raw concatenation
- Single-message skip in ClusterSummarizer
- Timestamps in dirty-input collection
- PreCompress hook fires on every compression attempt

50 tests passing after fix pass (stale-summary guard timeout recurred, fixed with single-flight guard).

---

## Step 11: Fresh judge (codex, no prior context)

Fresh codex instance ranked all four implementations:

**Ranking: D > A > C > B**

| | D (synthesis) | A (original) | C (claude subagent) | B (codex first pass) |
|---|---|---|---|---|
| Rank | 1st | 2nd | 3rd | 4th |
| Verdict | "Least bad candidate" | "Simpler, less stateful" | "Not shippable" | "Least production-ready" |

**New bug found in D:** Persistent-window ingestion drift — cached ContextWindow only appends, but truncateHistoryToBudget recomputes on each call. Window can diverge from actual history when truncation boundary moves.

**Key finding:** The synthesis loop (implement → cross-review → absorb → re-judge) moved D from 2nd to 1st place. One round of cross-pollination between two blind implementations produced the best result. Neither implementation alone was shippable; the combination was closest.

**The double loop in action:** B had the right architecture (persistence, config, rich ingestion) but wrong integration (flatten-to-user). C had the right defensive patterns (error retry, timestamp preservation, Content preservation) but wrong plumbing (broken ingestion, wrong key). D got both by reading both.

---

## Step 12: Absorbing the original implementation

Fed codex the original pipeline's implementation (from `kimjune01/gemini-cli:feat/union-find-compaction`) and asked it to cherry-pick improvements into the synthesized version.

**Three improvements absorbed:**
1. ClusterSummarizer: try/catch around `generateContent()`, falls back to joined raw messages instead of bubbling failures into compaction
2. contentToContextString: returns `''` for empty Content, ingestion skips those entries (prevents placeholder strings from contaminating embeddings)
3. Render query path: tolerates empty derived query

53 tests passing after absorption. The original pipeline's strength (defensive error handling, edge case coverage) continues to complement the synthesis's strength (architecture, persistence, config).

**Final state:** The synthesized implementation has now absorbed improvements from all three sources: codex's architecture, Claude subagent's defensive patterns, and the original pipeline's error handling. Three passes of cross-pollination.

---

## Step 13: Blog post — "Blind, Blind, Merge"

Published at [june.kim/blind-blind-merge](https://june.kim/blind-blind-merge). Tagged `methodology coding`.

Key claims:
- The authority rule ("no regressions, UX improvement") displaced 15 design decisions with one sentence
- Different models fail on different sides of the same boundary (structural diversity > stochastic diversity)
- The synthesis (pushout) ranked closest to production; neither blind implementation shipped alone
- Prior art: AlphaCode, self-consistency, branch-solve-merge all use stochastic diversity. This uses structural diversity.
- Parts bin connection: Attend operation with explicit redundancy control, like a portfolio solver with different models instead of different seeds

Evidence repos published:
- [Synthesis](https://github.com/kimjune01/gemini-cli/tree/feat/union-find-compaction-v2) (commit `04d6451d9`)
- [Codex blind](https://github.com/kimjune01/gemini-cli-codex)
- [Claude blind](https://github.com/kimjune01/gemini-cli-claude)

---

## Step 14: Deploy script fix

`_site/` was tracked in git. Every post change rebuilt every HTML file (nav links), triggering 800+ file uploads to S3 on every deploy. Fixed:
- Added `_site/` to `.gitignore`, removed from git tracking
- Replaced git-diff-based deploy with `aws s3 sync --size-only`
- Removed `_site/` commit step from deploy script
- Deploys now take seconds and upload only size-changed files

---

## Step 15: Preregistration v3

Published [PREREGISTRATION-V3.md](https://github.com/kimjune01/union-find-compaction-for-gemini-cli/blob/master/PREREGISTRATION-V3.md). Documents that the implementation is the blind-blind-merge synthesis (not the single-Claude build v2 preregistered). Pins to commit `04d6451d9`. Hypotheses unchanged from v2.

---

## Step 16: Experiment run (v3)

Fixed measurement bug: harness was not calling `resolveDirty()` before scoring recall. Union-find had 0 LLM calls in the first run — was testing unsummarized raw content. Fixed per prereg protocol: "append all messages, then call `render()` + `resolveDirty()` at end of conversation."

**Results (with resolveDirty):**

| Hypothesis | Verdict | Detail |
|---|---|---|
| H1 Recall | FAIL | 25.0% → 32.3% (+7.3pp), McNemar p=not significant |
| H2 Latency | PASS | p95 = 0.3ms (target <100ms) |
| H3 Cost | PASS | 0.79x flat (union-find *cheaper*) |

**H1 detail:**
- McNemar's: both correct 19, flat only 5, union only 12, neither 60
- Effect size +7.3pp but underpowered at n=96 (prereg acknowledged ~200 needed)
- 7 of 12 conversations favored union-find, 3 favored flat, 2 tied

**H3 detail:**
- Flat: 24 calls, ~144k tokens total
- Union-find: ~32 calls, ~114k tokens total
- Ratio: 0.79x — union-find uses fewer tokens despite more calls (smaller per-cluster summaries vs full-history summarization)

**H2 detail:**
- Append p95: 0.3ms (three orders of magnitude under target)
- All append and render operations synchronous, no LLM calls on blocking path

**Per tuning policy:** H1 missed. 2 parameter changes allowed (merge threshold, retrieval k). Effect size is promising but test is underpowered. Decision pending.

**Elapsed:** 6.2 minutes, 452 API calls, 734,779 tokens.

---

## Step 17: Tuning H1

Per prereg tuning policy: max 2 parameter changes for H1.

**Tuning change 1: merge threshold 0.15 → 0.10** (less aggressive merging)

Hypothesis: too-aggressive merging loses detail. More clusters → more granular summaries → better recall.

Result: flat 27.1%, union 27.1% (+0.0pp). **Worse than baseline.** Less merging scattered information across too many small clusters. Each cluster summary was too thin to answer questions.

**Tuning change 2: merge threshold 0.15 → 0.20** (more aggressive merging)

Hypothesis: more merging → fewer, larger clusters → richer summaries → better recall.

Result: flat 28.1%, union 29.2% (+1.0pp). **Worse than baseline.** More merging compressed too much — lost the detail the summaries needed.

**Tuning summary:**

| Threshold | Flat | Union-find | Diff |
|---|---|---|---|
| 0.15 (baseline) | 25.0% | 32.3% | +7.3pp |
| 0.10 (change 1) | 27.1% | 27.1% | +0.0pp |
| 0.20 (change 2) | 28.1% | 29.2% | +1.0pp |

The baseline (0.15) was the best configuration. Both tuning changes made recall worse. Per prereg tuning policy: tuning budget exhausted, accept result.

**Final verdict (v3):**
- H1 Recall: FAIL (+7.3pp, not significant, underpowered at n=96)
- H2 Latency: PASS (p95 = 0.3ms)
- H3 Cost: PASS (0.79x flat)
- Claim strength: "Not supported" for H1. Per prereg decision rules: "H1 ❌ H2a ✅ H3 ✅ → Better append UX, comparable cost. Document; note H1 power limitation."

**Observation:** Union-find recall was higher in 7 of 12 conversations, tied in 2, lower in 3. The effect is consistent in direction but the test lacks power. The prereg acknowledged this: "96 question-answer pairs likely underpowered for 5pp effect size (~200 needed for 80% power)."

**Revert merge threshold to 0.15.** That's the configuration that ships.
