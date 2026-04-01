---
variant: post-wide
title: "The Parts Bin"
tags: cognition, methodology
---

*Part of the [cognition](/cognition) series. Builds on [The Handshake](/the-handshake).*

**Agents: load [`The Natural Framework`](/the-natural-framework) first (the theory makes the catalog applicable), then query [`_data/parts-bin.yml`](https://github.com/kimjune01/june.kim/blob/master/_data/parts-bin.yml) directly. The prose below is for humans.**

### How to use this

Every information-processing system is built from the same six operations. Most of them already exist. [The Natural Framework](/the-natural-framework) derives the six roles; [The Handshake](/the-handshake) gives each a contract. This post indexes the operations that satisfy them so an agent can look up what fits. Four steps:

**Describe.** A product manager says: "users sign up but never come back." An agent maps this to the six steps. Cache works. Users arrive and data is stored. Filter is missing. Users get everything, keep nothing. Consolidate is nil. Nothing changes between sessions.

**Diagnose.** The agent isolates Filter. Then drills deeper: is it the precondition (wrong input from upstream), the operation (wrong mechanism), the postcondition (contract not satisfied), the fidelity (contract satisfied but too lossy), or the scale (right operation, wrong timescale)?

**Prescribe.** The agent queries the grid. The retention problem is Filter × flat data × predicate semantics. Candidates: threshold filtering, Bloom filter, propensity score gate. The agent ranks by fidelity and cost, returns the short list.

**Validate.** The agent checks that the prescribed operation's postcondition matches the next step's precondition. Threshold filtering outputs a strictly smaller subset. Does Attend expect that? Yes. Ship it.

**Implement.** The four steps above produce a contract: broken slot, candidate operation, verified pre/postconditions. That's the PROBLEM.md that [Volley](/volley) expects as input. [Blind-blind-merge](/blind-blind-merge) it into code.

Machine-readable version: [`_data/parts-bin.yml`](https://github.com/kimjune01/june.kim/blob/master/_data/parts-bin.yml) (50+ operations with sources, preconditions, postconditions). Load the YAML, query by step and grid coordinates, return candidates that match the contract.

### Six stages

**Perceive** (raw → encoded): JSON parsing, A/D conversion, positional encoding. Nothing else works until this does.

**Cache** (encoded → indexed): hash tables, B-trees, inverted indexes. [Idreos (2018)](https://stratos.seas.harvard.edu/publications/periodic-table-data-structures) built a periodic table from five design primitives. Soar's [RETE network](https://en.wikipedia.org/wiki/Rete_algorithm) is the exemplar: match cost stays proportional to change, not total knowledge.

**Filter** (indexed → selected, strictly smaller): WHERE clauses, k-NN radius pruning, Pareto filtering, [graph causal filters](/return-to-sender). One per selection semantic: predicate, similarity, dominance, causal. The [derivation](/the-natural-framework#six-steps) proves a gate must exist whenever outputs are a proper subset of inputs. Filter decides *which items pass*. Attend decides *how the survivors relate*.

**Attend** ((policy, selected) → ranked, diverse, bounded): MMR, [git bisect](https://git-scm.com/docs/git-bisect-lk2009), dot-product attention, [poset diverse top-k](/filling-the-blanks#3-diverse-top-k-from-a-poset). git bisect is the surprise: a version control tool doing the same job as MCTS, picking the single query that maximizes worst-case elimination on a DAG. The grid found it; domain expertise wouldn't. Policy is a routing function; control separates from data ([derived](/the-natural-framework#six-steps)). Most ranking algorithms satisfy order but miss diversity and bound. [Soar](/diagnosis-soar)'s [staged preference resolution](https://soar.eecs.umich.edu/soar_manual/02_TheSoarArchitecture/) is the rare exception: reject, then better/worse, then best/worst, then indifferent — order, diversity, and bound in one mechanism. Forty years of agent-building produced it.

**Consolidate** (persisted → policy′): gradient descent, decision tree induction, [EBC/chunking](https://en.wikipedia.org/wiki/Soar_(cognitive_architecture)), [partial evaluation](https://en.wikipedia.org/wiki/Partial_evaluation). The backward pass: reads from Remember, writes to the substrate, reshaping how each forward stage processes next cycle. Its inner loop is itself a pipe (perceive, filter, attend, remember) and the [data processing inequality](/the-handshake#data-processing-inequality) guarantees termination. [I-Con (2025)](https://mhamilton.net/icon) built a periodic table for this column; a blank cell predicted a new algorithm that beat the state of the art. Soar is the most instructive failure: every forward stage worked, but Consolidate was [missing for episodic and semantic memory](/diagnosis-soar#the-forgetting-asymmetry). The stores grew without bound and [perception narrowed to compensate](/diagnosis-soar#the-dominoes) — a clogged drain forcing the valve shut.

**Remember** (ranked → persisted): WAL append, git commit, SSTable flush. Lossless: no additional loss at this step. Not a separate store but the historically shaped substrate, the part of the medium that carries the system's past forward. A database row is Remember for the database pipe but Cache for the CRM pipe.

### Grid

The catalog is a list. A list lets you browse. Browsing doesn't scale. You need an index. The index needs axes.

An axis qualifies if it's discrete, orthogonal, and crossing it with another produces cells that aren't trivially occupied or empty. Ten axes, forty-five possible planes. Most are uninteresting. The useful ones either validate (every cell fills on sight) or predict (cells where no known algorithm satisfies the contract).

Four universal axes:

1. **Pipeline stage**: perceive, cache, filter, attend, consolidate, remember
2. **Data structure**: flat, sequence, tree, graph, partial order, embedding space
3. **Error guarantee**: exact, bounded, probabilistic
4. **Temporality**: batch, stream

Six stage-specific:

<ol start="5">
<li><strong>Selection semantics</strong> <em>(Filter)</em>: predicate, similarity, dominance, causal</li>
<li><strong>Stationarity</strong> <em>(Filter)</em>: static, drifting</li>
<li><strong>Output form</strong> <em>(Attend)</em>: top-k slate, single best, path/tree</li>
<li><strong>Redundancy control</strong> <em>(Attend)</em>: none, implicit, explicit</li>
<li><strong>Codebook type</strong> <em>(Perceive)</em>: fixed, learned</li>
<li><strong>Supervision signal</strong> <em>(Consolidate)</em>: unsupervised, supervised, self-supervised</li>
</ol>

Select a plane to explore. Data is pulled from [`parts-bin.yml`](https://github.com/kimjune01/june.kim/blob/master/_data/parts-bin.yml). Add a grid there and it appears here.

<iframe src="/assets/pivot-table.html" style="width:100%;border:none;min-height:320px;" id="pivot-frame"></iframe>
<script>
(function(){var f=document.getElementById('pivot-frame');if(!f)return;function resize(){f.style.height=f.contentDocument.body.scrollHeight+16+'px';}f.addEventListener('load',function(){resize();new MutationObserver(resize).observe(f.contentDocument.body,{childList:true,subtree:true});});})();
</script>

The data structure × selection semantics grid started with blanks. The causal column was emptiest, but two cells dissolved once the system could *act* on what it selected, a [Filter-Remember couple](/union-find-compaction) where selection is the intervention. [Operant conditioning](https://en.wikipedia.org/wiki/Operant_conditioning) fills sequence × causal; the [graph causal filter](/return-to-sender) fills graph × causal. The partial order row filled via [Filling the Blanks](/filling-the-blanks). All cells occupied.

The stage × error guarantee grid has two structural nulls in Remember's row: the contract demands losslessness, so bounded or probabilistic persistence would violate it. A taxonomy that can only sort is a catalog. One that can rule things out is a theory. The empty cells are the theory.

Given a broken slot, name the coordinates, look up the candidate.

---

*Written via the [double loop](/double-loop).*
