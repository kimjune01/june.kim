# Outreach: Filling the Blanks

## 1. Matteo Magnani (Uppsala University)

**Subject:** Residualized dominance: a different fix for overlapping group skylines

Hi Matteo,

Your 2013 EDBT paper with Inger Assent ("From Stars to Galaxies") named the problem clearly: naive aggregation over overlapping groups makes skyline dominance misleading. Your fix redefines dominance to tolerate overlap.

I tried the other direction: factor the overlap out before comparing. Decompose each community into shared and residual members, run dominance only on the marginals. Reduces to standard group skyline when overlap is empty, to Pareto when groups are singletons.

Writeup and implementation: https://june.kim/filling-the-blanks

Thought you'd want to know someone picked up the thread.

Best,
June Kim
https://june.kim


## 2. Aaditya Ramdas (CMU)

**Subject:** Closure-level causal filtering on partial orders — extending conformal selection

Hi Aaditya,

Your conformal causal selection work with Rina Duan and Larry Wasserman gives a clean bounded-FDR filter for flat data: gate items by treatment effect, control false discoveries. I tried extending it to partial orders.

In a poset where a is a prerequisite for b, treating b forces treating everything below it. The natural treatment unit isn't a single node — it's a downward closure. I defined a closure-level estimand (effect of treating the entire closure of x vs baseline) and worked through identification. The main obstacle is positivity: deep posets have large closures with thin support, so the approach works for shallow hierarchies but may break for deep chains.

Writeup and implementation: https://june.kim/filling-the-blanks (section 2).

Thought you'd want to see someone extending the conformal selection idea in this direction.

Best,
June Kim
https://june.kim


## 3. Ilya Shpitser (Johns Hopkins)

**Subject:** Closure-level causal estimand on partial orders — extending hierarchical interventions

Hi Ilya,

Your 2016 paper with Tchetgen Tchetgen on causal inference with a graphical hierarchy of interventions defined a clean framework: node, edge, and path interventions forming an inclusion hierarchy. The hierarchy is over causal pathways.

I tried a different kind of hierarchy: prerequisite structure. In a poset where a ≤ b means "a must be treated before b," treating b forces treating everything below it. The treatment unit becomes a downward closure, not a single node. I defined a closure-level estimand — the effect of treating ↓{x} vs baseline — and the main obstacle is positivity: deep posets have large closures with thin support.

Writeup and implementation: https://june.kim/filling-the-blanks (section 2).

Thought you'd want to see someone building on the hierarchical interventions idea.

Best,
June Kim
https://june.kim


## 4. Daniel Yekutieli (Tel Aviv University)

**Subject:** Stochastic dominance over subtree CDFs — using hierarchical FDR for tree filtering

Hi Daniel,

Your hierarchical FDR methodology gives a way to control false discoveries when hypotheses are organized on a tree. I used it as the testing backbone for a new definition of tree dominance.

The definition: subtree A dominates subtree B if the empirical distribution of leaf utilities in A first-order stochastically dominates that of B, after depth-normalization. Test each pair with simultaneous confidence bands, organize the pairwise hypotheses on the tree, run your hierarchical FDR top-down.

This fills a gap in a design-space grid I've been building — "dominance filtering on trees" had no algorithm because nobody had defined what subtree dominance means. Writeup and tested implementation: https://june.kim/filling-the-blanks (sketch #5 in the remaining blanks section).

Thought you'd want to see hierarchical FDR applied in this direction.

Best,
June Kim
https://june.kim


## 5. Pavel Chizhov (THWS)

**Subject:** Online tokenization with backward compatibility — building on PickyBPE

Hi Pavel,

Your PickyBPE work showed that selective merging improves tokenization quality over standard BPE. I've been thinking about the online version of the problem: adapting a vocabulary on a stream while guaranteeing backward compatibility.

The sketch: keep an append-only merge DAG where existing token IDs never change. Track candidate merges with streaming heavy-hitters over adjacent pairs. Add a new token only if compression gain exceeds a threshold. Retokenize only inside a rolling checkpoint buffer of size W — older text keeps its old tokenization. This gives three guarantees: online updates, exact backward compatibility, bounded retokenization rate.

Writeup and tested implementation: https://june.kim/filling-the-blanks (sketch #8 in the remaining blanks section).

Thought you'd want to see someone pushing BPE adaptation toward the streaming case.

Best,
June Kim
https://june.kim


## 6. Zuguang Gu (German Cancer Research Center)

**Subject:** Poset diversity selection — generalizing simona's Jaccard similarity

Hi Zuguang,

Your simona package uses Jaccard on ancestor sets to measure similarity between terms in biomedical ontologies. I borrowed that idea for a different purpose: diversified top-k selection from a partial order.

Standard diversity methods (MMR, DPP) assume a metric space, but partial orders only have reachability. I built a similarity kernel from Jaccard on downsets/upsets plus a comparability term, plugged it into an MMR greedy loop. Reduces to pure relevance when the poset is discrete, spreads selections when it's a total order.

Writeup and implementation: https://june.kim/filling-the-blanks (section 3).

Thought you'd want to see your Jaccard-on-ancestors idea used in a new context.

Best,
June Kim
https://june.kim
