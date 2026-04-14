# Semantic Memory in Soar — Group Meeting, April 16, 2026

Attendees: John Laird, Steven Jones, Calvin Pugmire, Yongjia Wang, June Kim

Draft PR: https://github.com/SoarGroup/Soar/pull/581

## 1. Quick updates from each researcher (15 min, ~3 min each)

- Calvin: cohesifying theories (ACT-R, Clarion, TRESTLE, etc.) into Soar
- Yongjia: Semantic Programs — standalone memory layer, evaluation approach
- June: correction of prior diagnosis, eval harness built and validated
- Steven / John: any new developments

## 2. Eval harness demo (10 min)

John asked in the first email: "how we might evaluate and compare alternative implementations." I built a starting point.

**soar-eval** wraps Soar's existing test agents, captures per-test quantitative stats, and diffs two builds. Validated on:

- ChunkingTests: 19 agents
- SMemFunctionalTests: 38 agents (37 pass, 1 known SQLite assertion)
- EpMemFunctionalTests: 47 agents (all pass)
- PerformanceTests: 15 agents (all pass)

Demo: upstream vs PR #577 on ChunkingTests.

```
BW_Hierarchical_Look_Ahead    decisions           66 → 46    -30%
                               production_firings  651 → 340  -48%
                               wm_max              679 → 235  -65%
                               productions_chunks    3 → 1    changed
```

No regressions on any other agent.

## 3. Design principle: visibility ≠ decision (5 min)

The harness separates what changed from whether it's good.

- **Layer 1 (visibility):** raw deltas per test per metric. `--facts-only` mode.
- **Layer 2 (decision):** a `policy.json` the maintainer owns. Which metrics matter, what noise to ignore, what counts as a regression.

Draft policy included for discussion: timing noise floor at 5ms / 1%, chunk count classified as neutral.

Contributors see the numbers. The maintainer sets the criteria.

## 4. How this helps compare our approaches (10 min)

Proposal: each researcher writes a test agent that exercises their proposed semantic learning mechanism. The harness measures all of them on the same terms.

- Same metrics across all approaches
- Same protocol: upstream baseline vs candidate branch
- Same policy: maintainer configures what counts

Yongjia's question about standalone vs in-Soar evaluation: the harness handles the in-Soar layer. Standalone evaluation is a reasonable first step.

## 5. Discussion (15 min)

1. **What should a semantic learning test agent look like?** What task requires semantic learning that current Soar can't do?
2. **Policy configuration.** Is the draft policy.json reasonable? What would you change?
3. **Comparing different approaches.** Calvin's is rule-integration, Yongjia's is a relational layer. Can one harness measure all three, or do we need domain-specific evals?
4. **PR process.** Should proposed changes come with test agents and eval data?

## 6. Next steps (5 min)

- Each researcher defines one test agent demonstrating their approach
- Run all through the harness against upstream
- Reconvene with data
