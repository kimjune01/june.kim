*Part of the [cognition](/cognition) series. Builds on [The Handshake](/the-handshake).*

### Near-misses

[The Natural Framework](/the-natural-framework) derives six steps from temporal flow and bounded storage. [The Handshake](/the-handshake) gives each step a contract: precondition and postcondition. The CS textbook is full of operations that almost satisfy them. *Almost* is the diagnosis.

PageRank is the first specimen. Its postcondition says "ranked by authority" but the Attend contract requires diversity and a bound. It made a lot of money regardless. A broken step doesn't kill instantly; it compounds.

Google bolted on re-ranking, topic diversity, and freshness signals over two decades: incremental upgrades toward a contract-preserving morphism, one patch at a time.

Quicksort is the second specimen. It satisfies order, the most visible guarantee. But the Attend contract also requires diversity (survivors are dissimilar) and boundedness (output is finite top-k, not a total order). Quicksort is the default because order is the only guarantee most systems measure.

Most familiar algorithms are near-misses. They satisfy some guarantees but not all. The formal test is iteration stability: run the full loop — Perceive through Remember and back — and observe which postcondition degrades. Diversity is the guarantee iteration kills first, because without repulsion between winners the same cluster dominates every cycle. Noticing which guarantee fails under iteration: that's the diagnostic power.

Degenerate cases are the other edge. A chatbot has no policy store: nil Filter, nil Attend, nil Consolidate, nil Remember. Token in, token out, same rate. That is passthrough, predicted by the [existence proofs](/the-natural-framework#six-steps) when policy is zero.

Union-find has no selection: every element is kept, partitions only merge, the structure grows monotonically. No competitive core, no lossy step, no compression. Both are useful. Neither learns.

### Diagnostic resolution

The monad is the container — it doesn't break. What breaks is a morphism's postcondition. What cascades is the composition. The derivation forces contracts of this shape, and the [induction proof](/the-handshake#hard-question-answered) shows they compose forever if they compose once.

Step N+1's precondition is step N's postcondition. A correct algorithm with a broken precondition is a correct algorithm that produces garbage.

Governance operates at zero resolution. It can't see the interface, so it replaces the whole composition: fire everyone, rewrite from scratch, new system. Expensive. The framework increases resolution: instead of "the system is broken," the diagnosis is "Attend's diversity guarantee is missing." The parts bin increases it further: instead of "Attend is broken," the prescription is "this is a top-k sort where you need MMR re-ranking." Swap one operation, same slot, contract restored.

The most efficient fix requires the most precise name. The most feared enemy is one who cannot be named. The handshake is a naming system.

[Diagnosis LLM](/diagnosis-llm) took a couple of hours. Three layers, six steps each, SOAP notes with six-component plans. That precision came from the framework, not domain expertise in ML. Before germ theory: "the patient has bad air." After: "*streptococcus*, here's penicillin." The framework is the microscope. The handshake is why the microscope works.

### Agent

The framework is the diagnostic manual. The parts bin, once ordered, is the pharmacy. The handshake is why the prescriptions compose. What would it look like to use them systematically?

**Describe.** A product manager says: "users sign up but never come back." An agent maps this to the six steps. Cache works. Users arrive and data is stored. Filter is missing. Users get everything, keep nothing. Consolidate is nil. Nothing changes between sessions.

**Diagnose.** The agent isolates Filter. Then drills deeper: is it the precondition (wrong input from upstream), the operation (wrong mechanism), the postcondition (contract not satisfied), the fidelity (contract satisfied but too lossy), or the scale (right operation, wrong timescale)?

**Prescribe.** The agent queries the taxonomy. Filters by: matching precondition, matching postcondition, sufficient fidelity, compatible scale. Returns a ranked list of candidate operations from across domains. "Your Filter slot needs: output strictly smaller, criterion applied uniformly. Candidates from the parts bin, ordered by fidelity and cost."

**Validate.** The agent checks that the prescribed operation's postcondition matches the next step's precondition. If not, it flags the interface mismatch before you build it.

The doctor doesn't need to understand category theory. They need to read the contracts: precondition, postcondition, fidelity. The handshake is the pharmacology. The taxonomy is the PDR. The agent is the resident who can look things up fast.

### Catalog

The full catalog follows. Each entry is an operation: input in, output out. If the precondition and postcondition match the contract, the operation fits the slot. Filter decides per-item admissibility: does this item pass the criterion? Attend decides how admitted items relate to each other: order, diversity, and bound are slate-level properties.

**Perceive** (raw → encoded) — the column every system gets right, because nothing else works until it does.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td>Lexical analysis</td><td>Raw byte stream</td><td>Token sequence, parseable</td></tr>
<tr><td>Parsing (LL/LR)</td><td>Token stream, conforms to grammar</td><td>AST with explicit structure, traversable</td></tr>
<tr><td>JSON parsing</td><td>Raw string, well-formed</td><td>Structured object, addressable by key</td></tr>
<tr><td>A/D conversion</td><td>Continuous analog signal</td><td>Discrete samples, quantized</td></tr>
<tr><td><a href="https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf">SIFT descriptor extraction</a></td><td>Raw pixel grid</td><td>Keypoint descriptors, matchable</td></tr>
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
</table>

**Attend** ((policy, selected) → ranked, diverse, bounded) — reads the policy store: given the survivors, which are worth pursuing? Policy is a function; it routes data. Control separates from data ([derived](/the-natural-framework#six-steps)). Most ranking algorithms satisfy order but miss diversity and bound.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Operation</th><th style="background:#f0f0f0">Precondition</th><th style="background:#f0f0f0">Postcondition</th></tr></thead>
<tr><td><a href="https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf">MMR re-ranking</a></td><td>Candidates + relevance scores + similarity measure</td><td>Top-k ordered, diversity penalized, bounded</td></tr>
<tr><td><a href="https://arxiv.org/abs/1207.6083">DPP top-k selection</a></td><td>Candidates + relevance weights + similarity kernel</td><td>Top-k ranked, mutually dissimilar, bounded</td></tr>
<tr><td><a href="https://link.springer.com/chapter/10.1007/978-3-642-12275-0_11">xQuAD re-ranking</a></td><td>Candidates + relevance + subtopic coverage</td><td>Top-k ordered, aspect coverage explicit, bounded</td></tr>
<tr><td>Submodular maximization</td><td>Candidates + submodular utility (relevance + coverage)</td><td>Top-k greedy-ranked, diminishing-return diversity, bounded</td></tr>
<tr><td>Diversified beam search</td><td>Stepwise expansions + diversity penalty</td><td>Top-b retained, non-redundant alternatives, bounded</td></tr>
</table>

Near-misses (diagnostic counterexamples):
- *Quicksort / Mergesort*: order only. No diversity, no bound.
- *Top-k selection*: bounded, no diversity.
- *PageRank*: ranking, no diversity, no bound.

**Consolidate** ((policy, ranked) → policy′) — the write interface to the policy store. Contains its own inner loop: mutate, score, select. The outer pipe cannot observe this loop directly — policy is not the data type of Perceive. It can only notice that Attend's behavior changed.

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

**Remember** (policy′ → persisted) — the strongest column. Lossless relative to its input: the contract is "no additional loss at this step." A database row is Remember for the database pipe but Cache for the CRM pipe. A log entry is Remember for the logger but Cache for the monitoring pipe.

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
<tr><td><strong>Predicate</strong></td><td>WHERE, range query</td><td>Threshold filtering (soft margin)</td><td style="opacity:0.7"><strong>??</strong></td></tr>
<tr><td><strong>Similarity</strong></td><td>Exact NN pruning</td><td>k-NN radius pruning</td><td><a href="https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/">LSH filtering</a></td></tr>
<tr><td><strong>Dominance</strong></td><td>Pareto filtering</td><td style="opacity:0.7"><strong>??</strong></td><td style="opacity:0.7"><strong>??</strong></td></tr>
</table>

The empty cells are predictions. Probabilistic predicate filtering: a randomized classifier used as a gate, with a known false-positive rate. Bounded dominance: approximate Pareto filtering that trades exactness for speed in high dimensions. Each empty cell is a typed interface with known neighbors.

Take **Attend**. Lay operations on output form vs. redundancy control:

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">None</th><th style="background:#f0f0f0">Implicit</th><th style="background:#f0f0f0">Explicit</th></tr></thead>
<tr><td><strong>Top-k slate</strong></td><td>Heap top-k</td><td>Beam search</td><td>MMR, DPP top-k, xQuAD</td></tr>
<tr><td><strong>Single best</strong></td><td>argmax</td><td>Tournament selection</td><td style="opacity:0.7"><strong>??</strong></td></tr>
<tr><td><strong>Path/tree</strong></td><td>Dijkstra, A*</td><td>MCTS</td><td style="opacity:0.7"><strong>??</strong></td></tr>
</table>

The right column is sparse. CS built ranking algorithms for decades and almost never baked redundancy control into the postcondition. It was bolted on after.

The gap predicts: concurrent stochastic tree search. Spawn threads with different random seeds; stochasticity encourages divergence. Budget kills at deadline; the final selection picks the best from a diverse pool. [Portfolio SAT solvers](https://arxiv.org/abs/1111.2249) do this. Biological evolution does this with mutation rate as the stochastic dial.

The grid narrows the search space enough that a dart throw produces a plausible candidate. Mendeleev didn't synthesize germanium. He drew the grid, pointed at the gap, and said "something goes here with these properties."

### Future work

The parts bin has order we haven't discovered yet. Within each column, operations form a spectrum. The proof provides the axes: iteration stability (Corollary 2), fidelity (data processing inequality), variation introduced (stochasticity proof), store (Corollary 2), and thermodynamic cost (Landauer). Scale and reversibility are properties of the domain row, not the operation. Like genes classified by observable function rather than nucleotide sequence, morphisms are classified by their contracts rather than their implementation. These gaps will predict operations that should exist but haven't been built yet. The periodic table didn't just organize chemistry. It created it.

The [derivation](/the-natural-framework) establishes contracts. Two things are ready now:

- **Order the parts bin.** The derived dimensions — iteration stability, fidelity, variation, store, cost — provide the axes for each column. Find the gaps. Predict the missing operations. Three columns already have periodic tables: Filter and Attend above, Cache from [Idreos (2018)](https://stratos.seas.harvard.edu/publications/periodic-table-data-structures), Consolidate from [I-Con (2025)](https://mhamilton.net/icon). Perceive and Remember remain.
- **Build the diagnostic agent.** Describe → Diagnose → Prescribe → Validate, backed by the ordered taxonomy.

Three need formalization work. The existence proofs and types are defined; the composition proofs are sketched:

- Formalize in Haskell: define the six morphisms as Kleisli arrows in the [Giry monad](https://ncatlab.org/nlab/show/Giry+monad), test composition with [QuickCheck](https://hackage.haskell.org/package/QuickCheck)
- String diagrams: visualize the pipeline in Stoch using the Markov category graphical calculus ([Cho & Jacobs 2019](https://arxiv.org/abs/1709.00322))
- Enrichment: track bits per step using Bradley's enriched category framework ([Bradley 2021](https://arxiv.org/abs/2106.07890))

One needs new theory. The derivation is for linear pipelines only:

- Operads ([Spivak 2013](https://arxiv.org/abs/1305.0196)): extend from linear pipelines to fan-in/fan-out agent architectures

Every gap in the bin is an *almost* that hasn't been named yet.

---

*Written via the [double loop](/double-loop).*
