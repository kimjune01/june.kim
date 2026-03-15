---
layout: post-wide
title: "The Parts Bin"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Handshake](/the-handshake).*

### Near-misses

[The Handshake](/the-handshake) defines six contracts — each step has a precondition and a postcondition. The CS textbook is full of operations that almost satisfy them. *Almost* is the diagnosis.

PageRank is the first specimen. Its postcondition says "ranked by authority" but the Attend contract requires diversity and a bound. It made a lot of money regardless. A broken step doesn't kill instantly; it compounds. Google bolted on re-ranking, topic diversity, and freshness signals over two decades: incremental upgrades toward a contract-preserving morphism, one patch at a time.

Quicksort is the second specimen. It satisfies order — the most visible guarantee. But the Attend contract also requires diversity (survivors are dissimilar) and boundedness (output is finite top-k, not a total order). Quicksort is the default because order is the only guarantee most systems measure.

Most familiar algorithms are near-misses. They satisfy some guarantees but not all. Noticing which guarantee is missing. That's the diagnostic power.

### Diagnostic resolution

The monad is the container — it doesn't break. What breaks is a morphism's postcondition. What cascades is the composition. Step N+1's precondition is step N's postcondition. A correct algorithm with a broken precondition is a correct algorithm that produces garbage.

Governance operates at zero resolution. It can't see the interface, so it replaces the whole composition: fire everyone, rewrite from scratch, new system. Expensive. The framework increases resolution: instead of "the system is broken," the diagnosis is "Attend's diversity guarantee is missing." The parts bin increases it further: instead of "Attend is broken," the prescription is "this is a top-k sort where you need MMR re-ranking." Swap one operation, same slot, contract restored.

The most efficient fix requires the most precise name. The most feared enemy is one who cannot be named. The handshake is a naming system.

[Diagnosis LLM](/diagnosis-llm) took a couple of hours. Three layers, six steps each, SOAP notes with six-component plans. That precision came from the framework — not domain expertise in ML. Before germ theory: "the patient has bad air." After: "*streptococcus*, here's penicillin." The framework is the microscope. The handshake is why the microscope works.

### Agent

The framework is the diagnostic manual. The parts bin, once ordered, is the pharmacy. The handshake is why the prescriptions compose. What would it look like to use them systematically?

**Describe.** A product manager says: "users sign up but never come back." An agent maps this to the six steps. Cache works. Users arrive and data is stored. Filter is missing. Users get everything, keep nothing. Consolidate is nil. Nothing changes between sessions.

**Diagnose.** The agent isolates Filter. Then drills deeper: is it the precondition (wrong input from upstream), the operation (wrong mechanism), the postcondition (contract not satisfied), the fidelity (contract satisfied but too lossy), or the scale (right operation, wrong timescale)?

**Prescribe.** The agent queries the taxonomy. Filters by: matching precondition, matching postcondition, sufficient fidelity, compatible scale. Returns a ranked list of candidate operations from across domains. "Your Filter slot needs: output strictly smaller, criterion applied uniformly. Candidates from the parts bin, ordered by fidelity and cost."

**Validate.** The agent checks that the prescribed operation's postcondition matches the next step's precondition. If not, it flags the interface mismatch before you build it.

The doctor doesn't need to understand category theory. They need to read the contracts — precondition, postcondition, fidelity. The handshake is the pharmacology. The taxonomy is the PDR. The agent is the resident who can look things up fast.

### Catalog

The full catalog follows. Each entry is an operation — input in, output out — not a data structure. If the precondition and postcondition match the contract, the operation fits the slot. Filter decides per-item admissibility: does this item pass the criterion? Attend decides how admitted items relate to each other: order, diversity, and bound are slate-level properties.

**Perceive** (raw → encoded) — the column every system gets right, because nothing else works until it does.

| Operation | Precondition | Postcondition |
|---|---|---|
| Lexical analysis | Raw byte stream | Token sequence, parseable |
| Parsing (LL/LR) | Token stream, conforms to grammar | AST with explicit structure, traversable |
| JSON parsing | Raw string, well-formed | Structured object, addressable by key |
| A/D conversion | Continuous analog signal | Discrete samples, quantized |
| SIFT descriptor extraction | Raw pixel grid | Keypoint descriptors, matchable |

**Cache** (encoded → indexed) — the most studied column. [Idreos (2018)](https://stratos.seas.harvard.edu/publications/periodic-table-data-structures) built a periodic table from five design primitives.

| Operation | Precondition | Postcondition |
|---|---|---|
| Hash indexing | Records with stable keys | Keyed index, exact retrieval by key |
| B-tree index construction | Records with ordered keys | Balanced index, retrieval + range queries |
| Trie insertion | String keys over finite alphabet | Prefix-indexed, retrieval by string or prefix |
| Inverted index construction | Tokenized corpus with document IDs | Posting lists, retrieval by term |
| LSM-tree flush | Sorted runs in memory | Persistent key-value index, retrievable after compaction |
| Skip-list indexing | Ordered entries | Probabilistic index, O(log n) retrieval |

**Filter** (indexed → selected, strictly smaller) — the column where most systems use exact predicates and nothing else.

| Operation | Precondition | Postcondition |
|---|---|---|
| Predicate selection (WHERE) | Indexed relation + boolean predicate | Subset matching predicate, strictly smaller |
| Range query | Ordered index + interval bounds | Subset within interval, strictly smaller |
| Threshold filtering | Scored items + threshold t | Subset meeting threshold, strictly smaller |
| Regex extraction | String corpus + pattern | Matching spans retained, non-matches discarded |
| k-NN radius pruning | Metric index + query + radius r | Subset within radius, strictly smaller |
| Pareto filtering | Candidates with objective vectors | Non-dominated subset, strictly smaller |

**Attend** (selected → ranked, diverse, bounded) — the column CS almost never fills correctly. Most ranking algorithms satisfy order but miss diversity and bound.

| Operation | Precondition | Postcondition |
|---|---|---|
| MMR re-ranking | Candidates + relevance scores + similarity measure | Top-k ordered, diversity penalized, bounded |
| DPP top-k selection | Candidates + relevance weights + similarity kernel | Top-k ranked, mutually dissimilar, bounded |
| xQuAD re-ranking | Candidates + relevance + subtopic coverage | Top-k ordered, aspect coverage explicit, bounded |
| Submodular maximization | Candidates + submodular utility (relevance + coverage) | Top-k greedy-ranked, diminishing-return diversity, bounded |
| Diversified beam search | Stepwise expansions + diversity penalty | Top-b retained, non-redundant alternatives, bounded |

Near-misses (diagnostic counterexamples):
- *Quicksort / Mergesort*: order only — no diversity, no bound.
- *Top-k selection*: bounded — but no diversity.
- *PageRank*: ranking — but no diversity, no bound.

**Consolidate** (ranked → compressed, changes future processing) — [I-Con (2025)](https://mhamilton.net/icon) built a periodic table for this column. A blank cell predicted a new algorithm that beat the state of the art.

| Operation | Precondition | Postcondition |
|---|---|---|
| Gradient descent update | Loss contributions + current weights | Weights updated, future predictions altered |
| Bayesian posterior update | Prior parameters + weighted observations | Posterior compressed, future inference altered |
| K-means update | Weighted points + codebook size k | k prototypes replacing many points, lossy |
| Incremental PCA | Observations in high dimension | Low-rank basis, future projection altered |
| Decision tree induction | Ranked labeled examples | Compact rule set, future classification altered |
| Prototype condensation | Ranked candidates + compression budget | Small exemplar set, lossy approximation for future matching |

**Remember** (compressed → persisted) — the strongest column. The discipline is to list write operations, not storage systems.

| Operation | Precondition | Postcondition |
|---|---|---|
| WAL append + fsync | Serialized state record | Durable on crash, recoverable next cycle |
| Transaction commit | Validated write set | Persisted, visible for future reads |
| Git object write + commit | Content-addressed objects + manifest | Durable commit graph, retrievable by hash |
| Checkpoint serialization | In-memory model/state | Persisted checkpoint, loadable on next run |
| Copy-on-write snapshot commit | Consistent compressed state image | Persistent snapshot, addressable by version |
| SSTable flush | Immutable key-value run in memory | Durable on-disk run, retrievable by key |

### Grid

The catalog is a list. A list lets you browse. Browsing doesn't scale — you need an index. The index needs axes.

Take **Filter**. Lay operations on two axes — selection semantics vs. error guarantee:

|  | Exact | Bounded approximation | Probabilistic |
|---|---|---|---|
| **Predicate** | WHERE, range query | Threshold filtering (soft margin) | *?* |
| **Similarity** | Exact NN pruning | k-NN radius pruning | LSH filtering |
| **Dominance** | Pareto filtering | *?* | *?* |

The empty cells are predictions. Probabilistic predicate filtering: a randomized classifier used as a gate, with a known false-positive rate. Bounded dominance: approximate Pareto filtering that trades exactness for speed in high dimensions. Each empty cell is a typed interface with known neighbors.

Take **Attend**. Lay operations on output form vs. redundancy control:

|  | None | Implicit | Explicit |
|---|---|---|---|
| **Top-k slate** | Heap top-k | Beam search | MMR, DPP top-k, xQuAD |
| **Single best** | argmax | Tournament selection | *?* |
| **Path/tree** | Dijkstra, A* | MCTS | *?* |

The right column is sparse. CS built ranking algorithms for decades and almost never baked redundancy control into the postcondition. It was bolted on after. The gap predicts: concurrent stochastic tree search. Spawn threads with different random seeds; stochasticity encourages divergence. Budget kills at deadline; the final selection picks the best from a diverse pool. Portfolio SAT solvers do this. Biological evolution does this with mutation rate as the stochastic dial.

The grid narrows the search space enough that a dart throw produces a plausible candidate. Mendeleev didn't synthesize germanium. He drew the grid, pointed at the gap, and said "something goes here with these properties."

### Future work

The parts bin has order we haven't discovered yet. Within each column, operations form a spectrum — ordered by guarantee strength, cost, determinism, scale. Like genes classified by observable function rather than nucleotide sequence, morphisms are classified by their contracts rather than their implementation. These gaps will predict operations that should exist but haven't been built yet. The periodic table didn't just organize chemistry. It created it.

- **Order the parts bin.** Identify the minimal orthogonal dimensions (fidelity, cost, determinism, scale, reversibility) and order each column. Find the gaps. Predict the missing operations.
- **Build the diagnostic agent.** Describe → Diagnose → Prescribe → Validate, backed by the ordered taxonomy.
- Formalize in Haskell: define the six morphisms as Kleisli arrows in the Giry monad, test composition with QuickCheck
- String diagrams: visualize the pipeline in Stoch using the Markov category graphical calculus ([Cho & Jacobs 2019](https://arxiv.org/abs/1709.00322))
- Enrichment: track bits per step using Bradley's enriched category framework ([Bradley 2021](https://arxiv.org/abs/2106.07890))
- Operads (Spivak 2013): extend from linear pipelines to fan-in/fan-out agent architectures

---

*Written via the [double loop](/double-loop).*
