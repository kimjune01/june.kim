---
layout: post-wide
title: "The Parts Bin"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Handshake](/the-handshake).*

### How to use this

[The Natural Framework](/the-natural-framework) derives six roles. [The Handshake](/the-handshake) gives each a contract. This post is the catalog of operations that satisfy them and the grids that index them. An agent uses it in four steps:

**Describe.** A product manager says: "users sign up but never come back." An agent maps this to the six steps. Cache works. Users arrive and data is stored. Filter is missing. Users get everything, keep nothing. Consolidate is nil. Nothing changes between sessions.

**Diagnose.** The agent isolates Filter. Then drills deeper: is it the precondition (wrong input from upstream), the operation (wrong mechanism), the postcondition (contract not satisfied), the fidelity (contract satisfied but too lossy), or the scale (right operation, wrong timescale)?

**Prescribe.** The agent queries the taxonomy. Filters by: matching precondition, matching postcondition, sufficient fidelity, compatible scale. Returns a ranked list of candidate operations from across domains. "Your Filter slot needs: output strictly smaller, criterion applied uniformly. Candidates from the parts bin, ordered by fidelity and cost."

**Validate.** The agent checks that the prescribed operation's postcondition matches the next step's precondition. If not, it flags the interface mismatch before you build it.

Machine-readable version: [`_data/parts-bin.yml`](https://github.com/kimjune01/june.kim/blob/master/_data/parts-bin.yml). Load the YAML, query by step and grid coordinates, return candidates that match the contract.

### Catalog

Each entry is an operation: input in, output out. If the precondition and postcondition match the contract, the operation fits the slot. Filter decides per-item admissibility. Attend decides how admitted items relate to each other: order, diversity, and bound are slate-level properties.

**Perceive** (raw → encoded) — the column every system gets right, because nothing else works until it does.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td>Lexical analysis</td><td>Raw byte stream</td><td>Token sequence, parseable</td></tr>
<tr><td>Parsing (LL/LR)</td><td>Token stream, conforms to grammar</td><td>AST with explicit structure, traversable</td></tr>
<tr><td>JSON parsing</td><td>Raw string, well-formed</td><td>Structured object, addressable by key</td></tr>
<tr><td>A/D conversion</td><td>Continuous analog signal</td><td>Discrete samples, quantized</td></tr>
<tr><td><a href="https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf">SIFT descriptor extraction</a></td><td>Raw pixel grid</td><td>Keypoint descriptors, matchable</td></tr>
<tr><td><a href="/filling-the-blanks#8-streaming-tokenizer">Streaming tokenizer</a></td><td>Text stream + merge threshold + window size</td><td>Token IDs, backward-compatible, bounded retokenization</td></tr>
</table>

**Cache** (encoded → indexed) — the most studied column. [Idreos (2018)](https://stratos.seas.harvard.edu/publications/periodic-table-data-structures) built a periodic table from five design primitives.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td>Hash indexing</td><td>Records with stable keys</td><td>Keyed index, exact retrieval by key</td></tr>
<tr><td>B-tree index construction</td><td>Records with ordered keys</td><td>Balanced index, retrieval + range queries</td></tr>
<tr><td>Trie insertion</td><td>String keys over finite alphabet</td><td>Prefix-indexed, retrieval by string or prefix</td></tr>
<tr><td>Inverted index construction</td><td>Tokenized corpus with document IDs</td><td>Posting lists, retrieval by term</td></tr>
<tr><td>LSM-tree flush</td><td>Sorted runs in memory</td><td>Persistent key-value index, retrievable after compaction</td></tr>
<tr><td>Skip-list indexing</td><td>Ordered entries</td><td>Probabilistic index, O(log n) retrieval</td></tr>
</table>

**Filter** (indexed → selected, strictly smaller) — gates the data store, where most systems use exact predicates. The [derivation](/the-natural-framework#six-steps) proves a gate must exist whenever outputs are a proper subset of inputs.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td>Predicate selection (WHERE)</td><td>Indexed relation + boolean predicate</td><td>Subset matching predicate, strictly smaller</td></tr>
<tr><td>Range query</td><td>Ordered index + interval bounds</td><td>Subset within interval, strictly smaller</td></tr>
<tr><td>Threshold filtering</td><td>Scored items + threshold t</td><td>Subset meeting threshold, strictly smaller</td></tr>
<tr><td>Regex extraction</td><td>String corpus + pattern</td><td>Matching spans retained, non-matches discarded</td></tr>
<tr><td>k-NN radius pruning</td><td>Metric index + query + radius r</td><td>Subset within radius, strictly smaller</td></tr>
<tr><td>Pareto filtering</td><td>Candidates with objective vectors</td><td>Non-dominated subset, strictly smaller</td></tr>
<tr><td><a href="/filling-the-blanks#4-spillover-adjusted-causal-segments">Spillover-adjusted causal filter</a></td><td>Time-series segments + treatment + kernel bandwidth</td><td>Segments with significant direct effect, FDR ≤ α</td></tr>
<tr><td><a href="/filling-the-blanks#5-stochastic-dominance-over-subtrees">Subtree stochastic dominance</a></td><td>Tree + subtree nodes + leaf scores</td><td>Non-dominated subtrees, FDR ≤ α</td></tr>
<tr><td><a href="/filling-the-blanks#6-order-context-similarity">Order-context similarity filter</a></td><td>Poset + query + similarity threshold</td><td>Items with Jaccard context overlap ≥ τ</td></tr>
<tr><td><a href="/filling-the-blanks#7-embedding-space-causal-filtering">Embedding causal filter</a></td><td>Embeddings + treatment + outcomes + kernel bandwidth</td><td>Items with significant direct effect net of cannibalization, FDR ≤ α</td></tr>
<tr><td><a href="/filling-the-blanks#1-residualized-dominance">Residualized dominance</a></td><td>Overlapping communities + objective vectors</td><td>Non-dominated after factoring out shared substructure</td></tr>
<tr><td><a href="/filling-the-blanks#2-closure-level-causal-effects">Closure-level causal filter</a></td><td>Poset + outcomes + treatment closures</td><td>Nodes with significant closure-level effect, FDR ≤ α</td></tr>
</table>

**Attend** ((policy, selected) → ranked, diverse, bounded) — reads the policy store: given the survivors, which are worth pursuing? Policy is a function; it routes data. Control separates from data ([derived](/the-natural-framework#six-steps)). Most ranking algorithms satisfy order but miss diversity and bound.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td><a href="https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf">MMR re-ranking</a></td><td>Candidates + relevance scores + similarity measure</td><td>Top-k ordered, diversity penalized, bounded</td></tr>
<tr><td><a href="https://arxiv.org/abs/1207.6083">DPP top-k selection</a></td><td>Candidates + relevance weights + similarity kernel</td><td>Top-k ranked, mutually dissimilar, bounded</td></tr>
<tr><td><a href="https://link.springer.com/chapter/10.1007/978-3-642-12275-0_11">xQuAD re-ranking</a></td><td>Candidates + relevance + subtopic coverage</td><td>Top-k ordered, aspect coverage explicit, bounded</td></tr>
<tr><td>Submodular maximization</td><td>Candidates + submodular utility (relevance + coverage)</td><td>Top-k greedy-ranked, diminishing-return diversity, bounded</td></tr>
<tr><td>Diversified beam search</td><td>Stepwise expansions + diversity penalty</td><td>Top-b retained, non-redundant alternatives, bounded</td></tr>
<tr><td><a href="/filling-the-blanks#3-diverse-top-k-from-a-poset">Poset diverse top-k</a></td><td>Poset + relevance scores + λ</td><td>Top-k ordered, order-context diversity, bounded</td></tr>
</table>

Near-misses (diagnostic counterexamples):
- *Quicksort / Mergesort*: order only. No diversity, no bound.
- *Top-k selection*: bounded, no diversity.
- *PageRank*: ranking, no diversity, no bound.

**Consolidate** (persisted → policy′) — the backward pass. Reads from Remember (which caches the ranked output) and writes to the substrate, reshaping how each forward stage processes on the next cycle. Consolidate's inner loop is itself a pipe: it perceives outcomes, filters which ones matter, attends to rank them, and remembers the update. The same catalog applies inside. If the parts bin has a blank at attend × partial order, any Consolidate operating on partial orders inherits that blank. The [data processing inequality](/the-handshake#data-processing-inequality) guarantees termination: each inner level costs at least one bit, so the recursion bottoms out at passthrough.

[I-Con (2025)](https://mhamilton.net/icon) built a periodic table for this column. A blank cell predicted a new algorithm that beat the state of the art.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td>Gradient descent update</td><td>Loss contributions + current weights</td><td>Weights updated, future predictions altered</td></tr>
<tr><td>Bayesian posterior update</td><td>Prior parameters + weighted observations</td><td>Posterior compressed, future inference altered</td></tr>
<tr><td>K-means update</td><td>Weighted points + codebook size k</td><td>k prototypes replacing many points, lossy</td></tr>
<tr><td>Incremental PCA</td><td>Observations in high dimension</td><td>Low-rank basis, future projection altered</td></tr>
<tr><td>Decision tree induction</td><td>Ranked labeled examples</td><td>Compact rule set, future classification altered</td></tr>
<tr><td>Prototype condensation</td><td>Ranked candidates + compression budget</td><td>Small exemplar set, lossy approximation for future matching</td></tr>
</table>

**Remember** (ranked → persisted) — the last forward stage. Lossless relative to its input: no additional loss at this step. Remember also serves as the cache for Consolidate: ranked outcomes are stored here, and Consolidate reads from them asynchronously. Remember is not a separate store. It is the historically shaped substrate, the part of the medium that carries the system's past forward. A database row is Remember for the database pipe but Cache for the CRM pipe. A log entry is Remember for the logger but Cache for the monitoring pipe.

If the thing being persisted is a representation rather than the final entity, it's Cache at this level, not Remember. The discipline: list write operations only.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td>WAL append + fsync</td><td>Serialized state record</td><td>Durable on crash, recoverable next cycle</td></tr>
<tr><td>Transaction commit</td><td>Validated write set</td><td>Persisted, visible for future reads</td></tr>
<tr><td>Git object write + commit</td><td>Content-addressed objects + manifest</td><td>Durable commit graph, retrievable by hash</td></tr>
<tr><td>Checkpoint serialization</td><td>In-memory model/state</td><td>Persisted checkpoint, loadable on next run</td></tr>
<tr><td>Copy-on-write snapshot commit</td><td>Consistent compressed state image</td><td>Persistent snapshot, addressable by version</td></tr>
<tr><td>SSTable flush</td><td>Immutable key-value run in memory</td><td>Durable on-disk run, retrievable by key</td></tr>
</table>

### Grid

The catalog is a list. A list lets you browse. Browsing doesn't scale. You need an index. The index needs axes.

Take **Filter**. Two axes, selection semantics vs. error guarantee:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Exact</th><th style="background:#f0f0f0">Bounded approximation</th><th style="background:#f0f0f0">Probabilistic</th></tr></thead>
<tr><td><strong>Predicate</strong></td><td>WHERE, range query</td><td>Threshold filtering (soft margin)</td><td><a href="https://en.wikipedia.org/wiki/Bloom_filter">Bloom filter</a></td></tr>
<tr><td><strong>Similarity</strong></td><td>Exact NN pruning</td><td>k-NN radius pruning</td><td><a href="https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/">LSH filtering</a></td></tr>
<tr><td><strong>Dominance</strong></td><td>Pareto filtering</td><td>ε-dominance filtering</td><td>Stochastic dominance</td></tr>
</table>

Every cell fills. The axes validate.

**Attend.** Output form vs. redundancy control:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">None</th><th style="background:#f0f0f0">Implicit</th><th style="background:#f0f0f0">Explicit</th></tr></thead>
<tr><td><strong>Top-k slate</strong></td><td>Heap top-k</td><td>Beam search</td><td>MMR, DPP top-k, xQuAD</td></tr>
<tr><td><strong>Single best</strong></td><td>argmax</td><td>Tournament selection</td><td>Simulated annealing, CMA-ES</td></tr>
<tr><td><strong>Path/tree</strong></td><td>Dijkstra, A*</td><td>MCTS</td><td><a href="https://arxiv.org/abs/1111.2249">Portfolio solvers</a></td></tr>
</table>

Given a broken slot, name the coordinates, look up the candidate. For blank cells and finer grids, see [The Missing Parts](/the-missing-parts).

---

*Written via the [double loop](/double-loop).*
