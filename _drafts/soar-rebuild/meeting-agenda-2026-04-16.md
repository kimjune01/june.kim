# Semantic Memory in Soar — Group Meeting, April 16, 2026

Attendees: John Laird, Steven Jones, Calvin Pugmire, Yongjia Wang, June Kim

## 1. Quick updates from each researcher (15 min, ~3 min each)

- Calvin: cohesifying theories (ACT-R, Clarion, TRESTLE, etc.) into Soar
- Yongjia: Semantic Programs — standalone memory layer, evaluation approach
- June: correction of prior diagnosis, eval harness built
- Steven / John: any new developments

## 2. Eval harness demo (10 min)

John asked in the first email: "how we might evaluate and compare alternative implementations." I built a tool for this.

**soar-eval** wraps Soar's existing test agents, captures per-test quantitative stats, and diffs two builds.

Demo: upstream vs PR #577 on ChunkingTests (19 agents).

```
BW_Hierarchical_Look_Ahead    decisions           66 → 46    -30%
                               production_firings  651 → 340  -48%
                               wm_max              679 → 235  -65%
                               productions_chunks    3 → 1    changed
```

Zero regressions on any other agent.

Key design: visibility (raw numbers) is separated from decision (maintainer policy). The harness reports facts. The maintainer decides what matters.

## 3. How this helps compare our approaches (10 min)

Proposal: each researcher writes a test agent that exercises their proposed semantic learning mechanism. The harness measures all of them on the same terms.

- Same metrics: decisions, firings, WM, chunks, retrieval latency
- Same protocol: run on upstream as baseline, run on branch as candidate
- Same policy: maintainer configures what counts as improvement

This gives the group a shared instrument. Individual approaches stay independent; the measurement is common.

Yongjia's question about standalone vs in-Soar evaluation: the harness handles the in-Soar layer. Standalone evaluation is a reasonable first step that feeds into this.

## 4. Discussion (15 min)

1. **What should a semantic learning test agent look like?** What task requires semantic learning that current Soar can't do?

2. **Policy configuration.** What metrics does the group care about? What's noise?

3. **How do we compare fundamentally different approaches?** Calvin's is rule-integration, Yongjia's is a relational layer, June's prior approach was structural. Can one harness measure all three, or do we need domain-specific evals?

4. **PR process.** Should proposed changes come with test agents and eval data?

## 5. Next steps (5 min)

- Each researcher defines one test agent that demonstrates their approach
- Run all through the harness against upstream
- Reconvene with data
