---
layout: post-wide
title: "Embedding Pipe"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Parts Bin](/the-parts-bin).*

### The pipe

An embedding pipeline processes items through six stages. Each stage has a contract. The machine-readable catalog is in [`_data/parts-bin.yml`](https://github.com/kimjune01/june.kim/blob/master/_data/parts-bin.yml) under `data_structure: embedding_space`.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0">Stage</th><th style="background:#f0f0f0">What it does</th><th style="background:#f0f0f0">Common implementations</th></tr></thead>
<tr><td><strong>Perceive</strong></td><td>Produce vectors from raw input</td><td><a href="https://arxiv.org/abs/2103.00020">CLIP</a>, sentence transformers, contrastive learning</td></tr>
<tr><td><strong>Cache</strong></td><td>Maintain a searchable index over vectors</td><td><a href="https://huggingface.co/papers/1603.09320">HNSW</a>, IVF-PQ, ball tree</td></tr>
<tr><td><strong>Filter</strong></td><td>Retrieve a candidate set, strictly smaller than the index</td><td>c-ANN search, ε-approximate range search</td></tr>
<tr><td><strong>Attend</strong></td><td>Rerank and diversify under a budget</td><td><a href="https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf">MMR</a>, k-center / farthest-first traversal</td></tr>
<tr><td><strong>Consolidate</strong></td><td>Update the embedding model or retrieval policy from outcomes</td><td>Triplet-loss fine-tuning, online k-means, <a href="https://papers.nips.cc/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c0067e7-Abstract.html">Growing Neural Gas</a></td></tr>
<tr><td><strong>Remember</strong></td><td>Persist artifacts across runs (index, model, metadata)</td><td>FAISS index serialization, product quantization, checkpoint save</td></tr>
</table>

Cache builds and searches the live index. Remember persists it to disk so the next run doesn't start from scratch. Cache is the in-memory structure. Remember is the durable snapshot.

### Filter grid

Embedding space Filter, selection semantics × error guarantee. The similarity row is the strongest. Predicate and dominance are secondary. Causal is an open research direction.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">Exact</th><th style="background:#f0f0f0">Bounded</th><th style="background:#f0f0f0">Probabilistic</th></tr></thead>
<tr><td><strong>Similarity</strong></td><td>Exact k-NN</td><td>c-ANN (cover tree, HNSW)</td><td>LSH ANN</td></tr>
<tr><td><strong>Predicate</strong></td><td>Metric range search</td><td>ε-approximate range search</td><td>LSH range query</td></tr>
<tr><td><strong>Causal</strong></td><td style="background:#fff3cd" colspan="3"><em>Open: geometry-aware interference estimation (<a href="https://www.econometricsociety.org/publications/econometrica/2022/01/01/causal-inference-under-approximate-neighborhood-interference">Leung 2022</a>) and FDR-controlled causal selection (<a href="https://doi.org/10.1515/jci-2023-0059">Duan et al. 2024</a>) exist separately. No known composition for embedding-distance-defined interference with bounded FDR.</em></td></tr>
</table>

### Attend grid

Embedding space Attend. The top-k row is where agents spend most of their time.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<thead><tr><th style="background:#f0f0f0"></th><th style="background:#f0f0f0">No diversity</th><th style="background:#f0f0f0">Implicit</th><th style="background:#f0f0f0">Explicit</th></tr></thead>
<tr><td><strong>Top-k slate</strong></td><td>k-NN retrieval</td><td>MMR</td><td>k-center / farthest-first</td></tr>
<tr><td><strong>Single best</strong></td><td>1-NN</td><td>Medoid</td><td>Farthest-point sampling</td></tr>
</table>

### Example: article feed

A concrete embedding pipe for surfacing fresh articles from an RSS-like feed:

1. **Perceive**: embed each new article with a sentence transformer.
2. **Cache**: add to an HNSW index.
3. **Filter**: for each candidate, compute distance to nearest existing article in the corpus. Reject if below a novelty threshold (density-based filtering).
4. **Attend**: from survivors, pick top-k by relevance × diversity using MMR. The similarity penalty is cosine distance in the embedding space.
5. **Consolidate**: track which articles the user reads. Fine-tune the embedding or adjust the novelty threshold.
6. **Remember**: serialize the HNSW index and read-history to disk.

The Filter step inverts the usual ANN query: instead of finding items *close* to a query, it rejects items close to *existing coverage*. The Attend step is standard MMR. The Consolidate step closes the loop.

### How embedding space differs from flat

Flat pipelines process records by attribute. Embedding pipelines process records by position in a learned space. The dominant primitives shift:

- **Cache**: key-based lookup → geometric index (HNSW, IVF)
- **Filter**: predicate scan → proximity retrieval (ANN)
- **Attend**: score-based ranking → coverage-aware diversification (MMR, k-center)
- **Consolidate**: parameter update → space reshaping (metric learning)

Embedding pipelines also use predicate filtering (metadata filters alongside ANN), but the geometric operations are the ones that distinguish the pipe.

---

*Written via the [double loop](/double-loop).*
