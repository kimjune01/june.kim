---
variant: post
title: "Licenses Are Functors"
tags: pageleft, cognition
---

Software licenses have algebraic structure. Not metaphorically. The operations are [composition](/reading/category-theory/milewski-01/) and [aggregation](/reading/category-theory/milewski-05/), and they behave like a [semiring](/reading/category-theory/milewski-06/).

## The derivation category

Every derivative work has a source. Milewski wrote a blog post. I [translated it to Python](/reading/category-theory/). Someone forks my translation. Each step is a morphism in a category where the objects are works and the arrows are derivations.

Derivations compose: if A derives from B and B derives from C, then A derives from C. Every work has an identity derivation (itself, unmodified). That's a [category](/reading/category-theory/milewski-01/).

## The obligation functor

A license is a [functor](/reading/category-theory/milewski-07/) from the derivation category to a category of obligations. It maps each work to a set of permissions, and each derivation arrow to a rule for how those permissions propagate.

CC BY maps every derivation to one obligation: credit the source. The functor preserves composition: if A derives from B derives from C, credit both B and C.

CC BY-SA maps every derivation to two obligations: credit the source, and license the derivative the same way. The share-alike clause is the [natural transformation](/reading/category-theory/milewski-10/) that makes the obligation recursive.

[CC BY-SA-NS](/cc-by-sa-ns) adds a third: credit, share-alike, and if you serve the derivative over a network, share the source. Same functor, one more component.

## The semiring

Combine two works as a derivative and the stricter license absorbs (CC BY-SA ⊗ MIT = CC BY-SA, a [lattice](/reading/category-theory/milewski-03/) join); bundle them side by side and each keeps its own license (a [product](/reading/category-theory/milewski-05/)).

Join for derivation, product for aggregation. [Semiring](/reading/category-theory/milewski-06/).

The algebra is the same one that governs [type-level arithmetic](/reading/category-theory/milewski-06/):

| License | Semiring role | Rule |
|---|---|---|
| AGPL | [absorber](/reading/category-theory/milewski-06/) | AGPL ⊗ anything = AGPL |
| MIT | one | contributes no obligation |
| Public domain | zero | absorbs nothing |

## Kleisli obligations

Derivation isn't deterministic. A coding agent reads a blog post and produces one of many possible implementations. The output is nondeterministic: `derive : Work → M(Work)`, where M is the monad of possible derivatives.

That makes the derivation chain a [Kleisli category](/reading/category-theory/milewski-04/). The license functor lifts through Kleisli composition the same way the Writer monad carries a log. Each derivation step appends its license constraint. The obligation accumulates.

CC BY-SA through Kleisli composition is [Canon](/canon). The share-alike obligation propagates forward through the chain, regardless of which specific derivative the agent produced. The nondeterminism is in the code. The obligation is in the license. The functor carries the second through the first.

| License | Functor behavior | [Information loss](/reading/info-theory/shannon-06/) |
|---|---|---|
| AGPL | lossless (full source required) | zero |
| CC BY-SA | preserves openness | low |
| MIT | forgets everything except credit | high |
| Public domain | constant functor (no obligation) | total |

Permissiveness is information loss. The [data processing inequality](/reading/info-theory/shannon-06/) applies: the functor can't create obligations that weren't in the source. Copyleft preserves. Permissive loses.

## Canon compounds

[Canon](/canon) is the CC BY-SA functor applied to a growing derivation graph. Copyleft is [irrevocable](/the-press), so the graph can only grow. The functor maps the growth of the corpus to the growth of the obligation surface. It scales with the category it acts on.

[PageLeft](/pageleft-manifesto) is the index of the image. It stores what the functor produces: copyleft works, their derivation chains, their attribution edges. Search over the image, and you search over the obligation graph.

---

*Every link above goes to a runnable [REPL](/reading/category-theory/) where you can modify the example. The vocabulary is not decorative.*
