*Part of the [cognition](/cognition) series.*

The [cognition series](/cognition) found six roles in information processing: [perceive](/caret-recorder), [cache](/moments), [filter](/perception-pipe), [attend](/salience), [consolidate](/consolidation), [remember](/memory). Five run forward as stages: perceive, cache, filter, attend, remember. Consolidate reads from remember and writes to the substrate, reshaping how each stage processes on the next cycle. The competitive core is filter and attend: winners suppress losers, diversity is enforced. Consolidate is how the substrate learns.

The same pipeline runs at every timescale. Every row is something you already call "information processing." Dimmed cells are steps the domain hasn't yet optimized.

<div class="table-wrap">
<table>
<thead>
<tr>
<th style="background:#f0f0f0"></th>
<th style="background:#f0f0f0"><a href="/caret-recorder">Perceive</a></th>
<th style="background:#f0f0f0"><a href="/moments">Cache</a></th>
<th style="background:#f0f0f0"><a href="/perception-pipe">Filter</a></th>
<th style="background:#f0f0f0"><a href="/salience">Attend</a></th>
<th style="background:#f0f0f0"><a href="/consolidation">Consolidate</a></th>
<th style="background:#f0f0f0"><a href="/memory">Remember</a></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Neuron">Neurons</a><br>(μs)</td>
<td><a href="https://en.wikipedia.org/wiki/Sensory_transduction">Sensory transduction</a></td>
<td>Feature extraction (<a href="https://en.wikipedia.org/wiki/Visual_cortex">V1, V2</a>)</td>
<td>Biased competition (<a href="https://doi.org/10.1146/annurev.ne.18.030195.001205">Desimone &amp; Duncan</a>)</td>
<td><a href="https://en.wikipedia.org/wiki/Winner-take-all_(computing)">Winner-take-all</a></td>
<td>Synaptic strengthening (<a href="https://en.wikipedia.org/wiki/Long-term_potentiation">LTP</a>)</td>
<td>Long-term cortical storage</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Operating_system">Operating System</a><br>(ns)</td>
<td>Interrupt, I/O event</td>
<td>Parse, deserialize</td>
<td><a href="https://en.wikipedia.org/wiki/Cache_replacement_policies">Cache eviction</a> (LRU vs LFU)</td>
<td class="dim">Scheduler dispatch</td>
<td class="dim"><a href="https://en.wikipedia.org/wiki/Log-structured_merge-tree">LSM compaction</a>, defrag</td>
<td>fsync, <a href="https://en.wikipedia.org/wiki/Write-ahead_logging">write-ahead log</a></td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Database">Database</a><br>(ms)</td>
<td>Query arrives</td>
<td>Query plan, index lookup</td>
<td>WHERE clause, index scan</td>
<td>ORDER BY, LIMIT</td>
<td class="dim">VACUUM, reindex</td>
<td>The table on disk</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Large_language_model">Inference</a><br>(ms)</td>
<td>Tokenize input</td>
<td><a href="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)">Positional encoding</a></td>
<td><a href="https://en.wikipedia.org/wiki/Attention_(machine_learning)">Softmax attention</a></td>
<td>Multi-head attention</td>
<td class="dim"><a href="https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets">Training</a> (sealed)</td>
<td class="dim">Frozen weights</td>
</tr>
<tr>
<td><a href="/cognition">Cognition</a><br>(s)</td>
<td>Caret Recorder captures screen</td>
<td>Moments segments into chunks</td>
<td>Perception Pipe</td>
<td>Salience + <a href="https://arxiv.org/abs/1207.6083">DPP</a></td>
<td>Schema formation offline</td>
<td>Publish to <a href="/canon">Canon</a></td>
</tr>
<tr>
<td>Writing Prose<br>(hours)</td>
<td>Read, research, encounter</td>
<td>Outline, organize into beats</td>
<td><a href="https://www.themarginalian.org/2014/10/03/arthur-quiller-couch-art-of-writing/">Kill your darlings</a></td>
<td>Select what survives the draft</td>
<td>Edit: each pass tightens</td>
<td>The published piece</td>
</tr>
<tr>
<td>Writing Code<br>(hours)</td>
<td>Read files, see errors</td>
<td>Parse into <a href="https://en.wikipedia.org/wiki/Abstract_syntax_tree">AST</a>, resolve types</td>
<td>Linter, type checker, tests</td>
<td>Code review, select the approach</td>
<td>Refactor</td>
<td>Push to repo</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Intelligent_agent">AI Agent</a><br>(min)</td>
<td>Read task, see context</td>
<td>Parse into context chunks</td>
<td class="dim">Select relevant files, ignore rest</td>
<td class="dim">Context window selection</td>
<td class="dim">Create skill</td>
<td>Push to production</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Advertising_technology">Adtech</a><br>(ms)</td>
<td>Bid request, user context</td>
<td>User profile, intent signals</td>
<td class="dim"><a href="https://en.wikipedia.org/wiki/Vickrey_auction">Second-price auction</a>, highest bid wins</td>
<td class="dim">Highest bidder wins, no diversity</td>
<td class="dim">Frequency caps, retargeting</td>
<td class="dim">Cookie-based, being deprecated</td>
</tr>
<tr>
<td><a href="/vector-space">Vector Space</a><br>(ms)</td>
<td><a href="/market-position-json">Positions</a> arrive, embedded</td>
<td>Indexed for auction</td>
<td><a href="/open-auction">Cosine gate</a>, nearest-neighbor</td>
<td><a href="/one-shot-bidding">VCG</a> selects on relevance × bid</td>
<td><a href="/three-levers">Relocation fees</a>, <a href="/receipts-please">receipts</a></td>
<td>Content-addressed <a href="/market-position-json">positions</a></td>
</tr>
<tr>
<td>Google<br>(hours)</td>
<td>Googlebot crawls</td>
<td>Index, parse HTML</td>
<td class="dim">No redundancy inhibition</td>
<td class="dim">Keyword match, top-k by <a href="https://en.wikipedia.org/wiki/PageRank">PageRank</a></td>
<td class="dim">Re-crawl on schedule</td>
<td>The index</td>
</tr>
<tr>
<td><a href="/pageleft">PageLeft</a><br>(hours)</td>
<td>Crawler discovers pages</td>
<td>Paragraph chunking, embed</td>
<td>Ingestion filter: freshness, inhibition</td>
<td>Search with DPP reranking</td>
<td>Quality compounds, PageRank converges</td>
<td><a href="/canon">Canon</a> grows</td>
</tr>
</tbody>
</table>
</div>

<span id="six-steps"></span>Twelve domains. Six roles.

Now the same table again. None of these domains call themselves "information processing", but all of them process information.

<div class="table-wrap">
<table>
<thead>
<tr>
<th style="background:#f0f0f0"></th>
<th style="background:#f0f0f0">Perceive</th>
<th style="background:#f0f0f0">Cache</th>
<th style="background:#f0f0f0">Filter</th>
<th style="background:#f0f0f0">Attend</th>
<th style="background:#f0f0f0">Consolidate</th>
<th style="background:#f0f0f0">Remember</th>
</tr>
</thead>
<tbody>
<tr>
<td>Comedy<br>(hours)</td>
<td>Read the room, current events</td>
<td>Premises, setups, organize into bits</td>
<td>Open mic: weak jokes die on stage</td>
<td><a href="https://en.wikipedia.org/wiki/Tight_five">Tight five</a>: finite stage time</td>
<td>Bits refined, callbacks link the set</td>
<td>The special, the body of work</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Immune_system">Immune</a><br>(days)</td>
<td><a href="https://en.wikipedia.org/wiki/Antigen">Antigen</a> encounter</td>
<td>Antigen presentation (<a href="https://en.wikipedia.org/wiki/Major_histocompatibility_complex">MHC</a>)</td>
<td><a href="https://en.wikipedia.org/wiki/Clonal_selection">Clonal competition</a></td>
<td><a href="https://en.wikipedia.org/wiki/Affinity_maturation#Selection">Affinity selection</a></td>
<td><a href="https://en.wikipedia.org/wiki/Affinity_maturation">Affinity maturation</a></td>
<td><a href="https://en.wikipedia.org/wiki/Immunological_memory">Memory B/T cells</a></td>
</tr>
<tr>
<td>Journalism<br>(days)</td>
<td>Tips, sources, breaking event</td>
<td>Interview, fact-check, outline</td>
<td>Editorial meeting: stories compete for space</td>
<td>Front page: finite above-the-fold</td>
<td>Follow-up, series, investigative deep-dive</td>
<td>The archive, the public record</td>
</tr>
<tr>
<td>Hiring<br>(weeks)</td>
<td>Resumes, referrals, work samples</td>
<td>Recruiter screen, scorecards, interview loop</td>
<td>Reject mismatches, downselect slate</td>
<td>Final debrief, compare across dimensions</td>
<td>Reference checks, leveling, calibration</td>
<td>Employee record, team composition, alumni graph</td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Venture_capital">VC</a><br>(months)</td>
<td>Pitches, market signals, founder histories</td>
<td>Memo, market map, diligence</td>
<td>Pass on most deals</td>
<td>Portfolio construction, category balance</td>
<td>Board learning, thesis updates</td>
<td><a href="https://en.wikipedia.org/wiki/Capitalization_table">Cap table</a>, portfolio, pattern library</td>
</tr>
<tr>
<td>Music<br>(months)</td>
<td>Hear influences, find sounds</td>
<td>Demos, arrangements, track sketches</td>
<td>Band votes, <a href="https://www.youtube.com/watch?v=jg1WUOxY6Cg">producer kills tracks</a></td>
<td>Tracklist: sequence and pacing</td>
<td>Mixing, mastering, the final cut</td>
<td>The album, the catalog</td>
</tr>
<tr>
<td>Publishing<br>(months)</td>
<td>Proposals, manuscripts, trends</td>
<td>Developmental edit, outline, positioning</td>
<td>Acquisitions rejects, editorial culling</td>
<td>Catalog selection, seasonal list balance</td>
<td>Copyedit, revisions, packaging</td>
<td>Published book, the <a href="https://en.wikipedia.org/wiki/Backlist">backlist</a></td>
</tr>
<tr>
<td>Architecture<br>(years)</td>
<td>Site, client needs, codes, context</td>
<td>Program, plans, massing, schematic design</td>
<td>Alternatives killed by budget, code, use</td>
<td>Final scheme, room adjacencies, circulation</td>
<td>Design development, construction documents</td>
<td>The building itself</td>
</tr>
<tr>
<td>Science<br>(years)</td>
<td>Observe phenomena</td>
<td>Formalize hypotheses</td>
<td><a href="https://en.wikipedia.org/wiki/Peer_review">Peer review</a>: papers compete for slots</td>
<td class="dim">Citation, agenda-setting</td>
<td>Review papers, textbooks synthesize</td>
<td>Curricula, canon of knowledge</td>
</tr>
<tr>
<td>Law<br>(decades)</td>
<td>Dispute arises</td>
<td>Pleadings, briefs, arguments</td>
<td><a href="https://en.wikipedia.org/wiki/Adversarial_system">Adversarial process</a></td>
<td>Selection of controlling <a href="https://en.wikipedia.org/wiki/Precedent">precedent</a></td>
<td>Appellate synthesis, restatements</td>
<td><a href="https://www.law.cornell.edu/wex/stare_decisis">Stare decisis</a></td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Evolution">Evolution</a><br>(Myr)</td>
<td>The <a href="https://en.wikipedia.org/wiki/Genome">genome</a></td>
<td>Generation</td>
<td><a href="https://en.wikipedia.org/wiki/Natural_selection">Natural selection</a></td>
<td><a href="https://en.wikipedia.org/wiki/Niche_differentiation">Niche differentiation</a></td>
<td><a href="https://en.wikipedia.org/wiki/Speciation">Speciation</a></td>
<td>The <a href="https://en.wikipedia.org/wiki/Genome">genome</a></td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Universe">Universe</a><br>(t<sub>P</sub>)</td>
<td><a href="https://en.wikipedia.org/wiki/Fundamental_interaction">Force</a></td>
<td><a href="https://en.wikipedia.org/wiki/Mass%E2%80%93energy_equivalence">Mass-energy</a> (E=mc²)</td>
<td><a href="/the-natural-framework">The Natural Framework</a></td>
<td><a href="https://en.wikipedia.org/wiki/God">God</a></td>
<td><a href="https://en.wikipedia.org/wiki/Thermodynamics">Thermodynamics</a></td>
<td><a href="https://en.wikipedia.org/wiki/Fundamental_interaction">Force</a></td>
</tr>
</tbody>
</table>
</div>

Twelve more domains. Six roles. From antibodies to Planck time. Twenty-four domains total. [More where these came from.](/more-rows)

## Why the same shape

Each domain faces the same problem: too much input, finite capacity, select a subset that's both high-quality and diverse. Within each domain, the same data type flows through every step. Neurons process spikes. Databases process rows. Cognition processes moments. The type doesn't change — only which items survive. Filter is rule-based: a threshold, a WHERE clause, a linter. No judgment. Attend is where judgment enters. Consolidate reads from remember and writes to the substrate: lossy compression that reshapes how each stage processes on the next cycle, propagating from outcome to cause. [Compaction](https://en.wikipedia.org/wiki/Log-structured_merge-tree) reorganizes the cache without changing the system.

## Inhibition across domains

[Desimone and Duncan (1995)](https://doi.org/10.1146/annurev.ne.18.030195.001205) described biased competition in neurons: visual objects compete simultaneously, winners suppress losers through mutual inhibition. Peer review works the same way. The winning papers make it harder for similar papers to get published. That's inhibition.

The immune system is the cleanest non-neural domain. Antigens compete for T-cell binding. Clonal competition selects the best B cells. Affinity maturation consolidates winners into better antibodies. Memory B/T cells persist for decades. No central coordinator. The body lets pathogens compete.

Natural selection is the slowest domain but the most obvious. The [competitive exclusion principle](https://en.wikipedia.org/wiki/Competitive_exclusion_principle) ([Gause](https://en.wikipedia.org/wiki/Georgy_Gause), 1934) says two species competing for identical resources cannot coexist. Niche differentiation is DPP at evolutionary timescale. Repulsion between similar items — what [Salience](/salience) uses to prevent redundant retrieval — is what prevents redundant species.

## The categorical proof

Each role is a [morphism](https://en.wikipedia.org/wiki/Morphism) — a structure-preserving map between information states. Five compose forward into a single transformation: high-bandwidth input to durable signal. The sixth, Consolidate, flows backward through the substrate, reshaping parameters from outcome to cause. That is [category theory](https://en.wikipedia.org/wiki/Category_theory). The information states are the objects. Each role is a morphism with a [postcondition](/the-handshake#morphisms-with-guarantees-vs-arbitrary-self-maps) — a structural guarantee on its output. The forward pipeline is their composition. When one domain's Remember feeds the next domain's Perceive, the mapping preserves all six morphisms and their composition order. That is a [functor](https://en.wikipedia.org/wiki/Functor) between categories.

Perceive and Cache are map. Filter and Attend are filter. Remember is reduce. Consolidate is the gradient — the backward pass that reshapes the map. [Map-filter-reduce](https://en.wikipedia.org/wiki/MapReduce) has been known since [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)). The surprise is that immune systems run it too.

<div style="max-width:63vw; min-width:320px; margin:1.5em auto; overflow-x:auto;">
<img src="/assets/functor-pipeline.svg" alt="Two pipelines — Cognition (object type: Moment) and Writing (object type: Draft) — each with six roles. A dashed arrow from Cognition's Remember to Writing's Perceive shows the functor relationship." style="width:100%; display:block;">
</div>

This is deduction, not induction. The boundaries follow from temporal flow.

The full derivation is machine-checked in [Lean 4](https://github.com/kimjune01/natural-framework). Five physics axioms, both boundary arguments, the three corollaries, ten removal tests, the stochasticity chain, the handshake composition, the coupling lemma, and the induction are all formally verified. The only gap is pigeonhole (which needs Mathlib); everything else compiles.

**Boundary 1: encoding before selection.** The pipeline receives raw input from the environment. A system is defined by its boundary: no boundary, no inside, no outside, no system. The boundary creates a type difference. Any physical system has finite state space; the environment includes everything the system does not. dim(E) > dim(I). A morphism must bridge them: that is Perceive. The bridge is a surjection — it must lose information.

That loss is not free. [Landauer's principle](https://en.wikipedia.org/wiki/Landauer%27s_principle): erasing one bit costs at least *kT* ln 2 joules. Lossy encoding erases bits, so it has a thermodynamic floor. You cannot encode everything. You must choose what to encode — but choosing is selection, and selection requires encoding first. Circular dependency. The only resolution is temporal: encode first with a cheap, fixed, lossy projection (the retina, the tokenizer, the microphone), then select from the encoded set. Perceive is always cheap because it cannot afford to be expensive: you have not selected yet, so you do not know what is worth spending energy on.

Now: the six roles are temporal morphisms, input at time *t*, output at time *t+δ*, where *δ* > 0. Perceive receives multiple inputs (environment and Remember's feedback). Remember emits at most one output at a time. Inputs arrive faster than outputs drain. By the pigeonhole principle, something must hold them. That is a data structure. A data structure for multiple items requires a write interface (storage) and a read interface (retrieval). Those are Cache's two operations. Cache must exist. You cannot select from what you have not stored. Encoding before selection.

**Boundary 2: selection before persistence.** If the loop feeds back, the last step's output must persist across the cycle boundary. That persistence morphism is Remember. Consolidate is lossy; Remember is lossless. If you persist before selecting, you persist everything, and the store grows without bound. Bounded storage forces selection before persistence.

Remember is the morphism that writes processed data to the store. The store is the substrate itself: the part of the medium that carries the system's past forward. DNA *is* the substrate. The connectome *is* the substrate. Destroying the substrate ends the medium all six roles run on. A meteor does not break a pipeline stage; it vaporizes the substrate. The pipeline was working until there was nothing left to run it.

The claim is inductive between iterations only: if the substrate constrains the next cycle's Perceive durably enough that the loop runs again, the composition holds. Remove it and the loop has nothing to perceive against. Remember is still an endomorphism, same type in and out, but with the longest time constant: persistent constraints must outlast the cycle they regulate. Timescale is the diagnostic. The contract is the definition: outputs that constrain future processing across cycles. A rock is slow but carries no system history. A genome is slow and carries every cycle that kept on happening.

**Corollary 1: the competitive core exists.** If output follows input with delay *δ* > 0, a policy decides when to release. *δ* = 0 is passthrough. *δ* = ∞ is suppression. Any system where outputs are a proper subset of inputs over time exhibits *δ* = some: a selection policy exists. That policy is Filter. The competitive core is not a design choice. It is forced by selective output.

**Corollary 2: control separates from data.** Nothing prevents policy from being encoded as data in principle. But data has variance (proven above). If policy shares a pool with data, the competitive process cannot distinguish them — it amplifies what matches current perception and suppresses the rest. One iteration and the policy is corrupted by the process it governs. Self-encoding is a fixed point that variance makes unstable. Even sharing a store is fatal: bounded storage forces eviction, and high-volume data evicts low-volume policy. Therefore policy and data must be different types. The contract is a property of the morphism, not the data flowing through it.

**Corollary 3: Consolidate and Attend exist.** The policy store from Corollary 2 is independent of the data store. It needs a write interface and a read interface. Attend is the read interface: it reads policy from the substrate and applies it to data in the forward pass. Consolidate is the write interface: it reads from Remember (which caches ranked outcomes) and compresses them into policy updates, propagating parameter changes from outcome to cause. The forward data path has five stages. The backward path is Consolidate.

Boundary 1 derives Perceive (type bridge) and Cache (pigeonhole). Boundary 2 derives Remember (loop closure). The corollaries derive Filter, Attend, and Consolidate. Five roles compose as forward stages. The sixth, Consolidate, reads from Remember and writes to the substrate. The derivation forces roles of this shape: a buffer, a gate, a policy reader, a policy writer. The [cognition series](/cognition) found these six across every domain it examined. Two independent lines of evidence converge on the same structure.

**Why "natural."** The proofs assume only temporal flow, bounded storage, and selective output. Energy satisfies the same premises: it flows through morphisms, storage costs resources, no consumption is 100% efficient. Energy is a data type. The same structure is forced for anything that flows through a bounded selective system in nature.

But the functor itself is a thing in nature. It occupies space, consumes energy, exists in time. The premises apply to the functor, not just to what flows through it.

**Stochasticity is not optional.** Proof by contradiction. Assume zero variation across a population of functors running the same pipeline. The population is either increasing, decreasing, or steady. If steady at zero output — dead, nothing to prove. If steady at nonzero output — every functor has a beginning, so equilibrium was reached from a prior state with nonzero delta. For the population to be uniform *now*, every functor must have converged to identical behavior without exchanging information about what to converge *to*. If increasing or decreasing — every functor must change at identical rates and times, requiring identical initial conditions and inputs. Thermodynamics breaks all three cases. The pipeline is lossy — Boundary 1 proves Perceive is a surjection, and selection erases the losers. [Landauer's principle](https://en.wikipedia.org/wiki/Landauer%27s_principle): erasing one bit costs at least *kT* ln 2 joules, dissipated as heat. Heat is stochastic. Every lossy step dissipates heat. Heat introduces variation. No physical process produces identical copies. Therefore: stochasticity is not assumed. It is imposed by physics. (This chain — Landauer to finite states to pigeonhole to collision to determinism-forces-error — is [formally verified](https://github.com/kimjune01/natural-framework), modulo the pigeonhole step which needs Mathlib.)

**Variation percolates.** Stochasticity at level *n* creates population variation. Those functors' outputs are the data types at level *n−1*. If the data types are themselves functors, variation at *n* is population variation at *n−1*. The reverse holds too: diverse inputs from below produce diverse outputs above. The induction works both directions. Variation propagates through every functor boundary.

**Uniformity is fatal.** A functor that enforces uniformity by policy kills variation at its level. Without variation, filter has nothing to select, attend has no diversity to enforce, consolidate has nothing to compress. The pipeline stalls. No output. For a self-recursive loop, no output is death. Death percolates up: the uniformity-enforcing functor loses its substrate. With enough iterations, it dies too. The competitive core is the price of existing.

## Falsification

The falsification test is structural: remove any morphism or permute their composition order, and the pipeline ceases to function. Three death conditions cover the internal failures: a broken step (a role fails), a closed loop (no new input), or decaying input (the source degrades). The dim cells are the evidence. Skip filter, and attention drowns in redundancy. That is Google's row. Skip attend, and consolidation amplifies the wrong winners. That is Science's row. Every dim cell in the tables is a system that dropped or misordered a morphism and broke downstream.

The three death conditions are exhaustive for pipeline failures, but substrate destruction is a precondition failure. The asteroid that killed the dinosaurs did not break a pipeline stage; every role was firing until impact. What ended was the substrate that carried the genome forward. The framework diagnoses how systems kill themselves. Substrate destruction is how systems get killed.

## Categorial Error

In the tables above, dim cells mark steps a domain hasn't optimized. The failures cascade: one broken step dims the rest downstream.

**Google** filters spam but does not filter for redundancy. Every page that clears the quality threshold enters the index regardless of what's already there. Attend compensates with keyword match, top-k by PageRank. Top-k is not inhibition. Ten results from the same content farm survive because nothing suppressed them on the way in. Consolidate becomes mechanical re-crawling. One underoptimized step dims the whole row.

**Adtech** filters by willingness to pay, not relevance. Highest bidder wins every impression. Consolidate patches with frequency caps, a bandage on a filter that never ran. Remember was borrowed from the browser and is now being deprecated. I spent a month [dismantling this pipeline](/open-auction). One broken step, three dim cells downstream.

**Science** is the most consequential. Citation metrics are `GET *` for academia: top-k by popularity, no diversity enforcement. [Merton (1968)](https://doi.org/10.1126/science.159.3810.56) called it the [Matthew effect](https://en.wikipedia.org/wiki/Matthew_effect) — the cited get more cited. You search for "schema consolidation" and get ten papers that cite each other saying the same thing. A DPP would return one from that cluster and five from adjacent regions you didn't know to search for. [JSTOR, PubMed, Nature](/memory): same bug as Google, different coat. Fix attend, and consolidate sharpens.

**Evolution** has no dim cells. The genome perceives, generation caches, natural selection filters, niche differentiation attends, speciation consolidates, and the genome remembers. Perceive and Remember are the same cell. Consolidate lives inside that cell: speciation is the genome reshaping its own selection parameters. The genome is not a record stored inside the organism; it *is* the historically shaped substrate, every cycle that kept on happening persisting as the constraint on the next. Life is self-recursive because the substrate is the memory. The Universe row has the same structure: force perceives and force remembers. Genome→genome, force→force.

## The recursive loop test

In a linked list, a weak node can be routed around, and survive. But in a singly recursive loop, we should be able to find out whether it survives a broken step or not. In biology, genome perception transforms into genome memory; it is a singly recursive loop. If it survives any one of the errors in each of the six roles, then the framework is falsified.

Can it? The error will either compound, diminish, or persist. Let's test:

- **Encoding fails.** A [prion](https://en.wikipedia.org/wiki/Prion) misfolds, templates more misfolding, every cycle amplifies the error. [Death](https://en.wikipedia.org/wiki/Transmissible_spongiform_encephalopathy).
- **Selection fails.** [p53](https://en.wikipedia.org/wiki/P53) is lost, damaged cells are not suppressed, each division produces more damaged cells. Cancer.
- **Persistence fails.** [Immunosenescence](https://en.wikipedia.org/wiki/Immunosenescence) degrades memory B/T cells, immune memory loses fidelity, each new threat is harder to learn.
- **Selection before encoding.** The [cheetah bottleneck](https://en.wikipedia.org/wiki/Cheetah#Genetics) ([Menotti-Raymond & O'Brien, 1993](https://pmc.ncbi.nlm.nih.gov/articles/PMC46261/)) destroyed genetic diversity before selection could act on it, and the species has been nearly extinct ever since.
- **Persistence before selection.** [Endogenous retroviruses](https://en.wikipedia.org/wiki/Endogenous_retrovirus) inserted into the germline without filtering, and 8% of the human genome is now viral fossil.

Every failure mode, given enough iterations of the loop, converges to the same endpoint: extinction. That is not a coincidence. It is what *singly recursive* means. In category theory, the six roles are morphisms inside the [Giry monad](https://en.wikipedia.org/wiki/Giry_monad) — the monad of probability distributions. The recursive feedback has the structure of a [trace](https://en.wikipedia.org/wiki/Traced_monoidal_category); formalizing it requires specifying how environment and internal state interact. [The Handshake](/the-handshake) gives the proof.

## Beyond biology

The same test works beyond biology. The loops are messier, but the compounding is the same:

- **Encoding fails.** During the [Great Leap Forward](https://en.wikipedia.org/wiki/Great_Leap_Forward), local cadres inflated harvest data. The state planned off lies, requisitioned grain that didn't exist, which incentivized more falsification next cycle. Famine killed tens of millions.
- **Selection fails.** [TerraUSD](https://en.wikipedia.org/wiki/Terra_(blockchain))'s stabilizer had no filter on destabilizing redemptions. When UST slipped, redemptions minted more LUNA, crashing its price, making the peg less credible, causing more redemptions. Death spiral.
- **Persistence fails.** [NASA](https://www.nasa.gov/history/columbia-accident-investigation-board-synopsis/) learned foam shedding was dangerous after Challenger, but the lesson was not durably consolidated. Each safe flight reinterpreted deviance as acceptable. Columbia and its crew were lost.
- **Selection before encoding.** The [Khmer Rouge](https://en.wikipedia.org/wiki/Cambodian_genocide) killed teachers, doctors, and officials before expertise could transfer to the next generation. Each purge reduced the capacity to train replacements. Institutional collapse.
- **Persistence before selection.** France consolidated WWI doctrine into the [Maginot Line](https://en.wikipedia.org/wiki/Maginot_Line) before testing it against new warfare. Investment in the old model crowded out adaptation. Germany bypassed it in six weeks.

Every one broke a step and fed the error back into the next cycle. Every one ended in collapse.

## What to filter

If your objection is "prove the category boundaries formally before I evaluate the idea" — that is a filter that gates on credence rather than structure. Run that filter in a loop. It will kill your own novel ideas before they survive a single iteration, because no new idea arrives pre-credentialed. Worse: it will pass the credentialed ones that should have been caught. The same heuristic that rejects uncredentialed insight is the same one as those who trusted the [Harvard fraudsters](https://en.wikipedia.org/wiki/Dana-Farber_Cancer_Institute#Research_misconduct_allegations), the [Enron scammers](https://en.wikipedia.org/wiki/Enron_scandal), and the [turtleneck at Theranos](https://en.wikipedia.org/wiki/Theranos).

## What remains

The six roles, the competitive inhibition at the core, and the vertical relationship: each domain's Remember is the next domain's Perceive. The pipeline compresses. Each level takes high-bandwidth information and reduces it to a durable signal the next can perceive. Neurons fire millions of times per second; cognition produces a few thoughts per minute; a career produces a handful of papers; a field produces a canon. The ratio is the reason at every transition. The word we have for that is **intelligence**.

Follow the output:

- Neurons remember as cortical storage, which cognition perceives on a screen.
- Cognition remembers by publishing to <a href="/canon">Canon</a>, which a writer perceives as research.
- Writing remembers as the published piece, which a reader perceives as a book.

Output becomes input.

Fix the broken step, and the downstream cells brighten. That is what [PageLeft](/pageleft) does: Google's filter had no redundancy inhibition, so we built one. Attend sharpened. Consolidate followed.

Nobody looks at Google Search and says "the filter step has no redundancy inhibition." They say "search results are bad." Nobody looks at academic publishing and says "attend is `GET *`." They say "the literature is overwhelming." The pipeline gives you diagnostic language for problems that existed before the language did. Seeing it was the hard part.

This all started with one comment. I was reading about neural attention and said, "this looks like a cache to me." The data structure was identical: indexed items competing for limited slots. All inside my head. That observation won the competition against priority queue, against heap. It survived [consolidation](/consolidation). It became a schema. That schema generated [Salience](/salience), which generated DPP, which generated the [Transformer mapping](/consolidation), which generated these tables.

The optimal implementations of these candidate functors already exist in nature, optimized over billions of years. We need to learn them and map them onto ourselves.

Stochasticity is physically mandatory for anything that persists. So is the competitive core, and the pipeline — five forward stages, one backward pass that reads from Remember and writes to the substrate — is the minimal structure for running it. Intelligence is the compression ratio between functor levels: what Perceive receives versus what Remember emits. Life is the self-recursive pipeline, Perceive and Remember in the same cell: the substrate constraining its own next perception. Genome→genome. Force→force. Compressing, selecting, persisting. The substrate is the memory.

If this functor is nature itself, iterating the universe at each Planck time, its variation-enforcing policy is the price of its vast existence. The Universe row fills all six cells. Force perceives, mass-energy caches, the natural framework filters, God attends, thermodynamics consolidates, force remembers. The loop closes. The universe is alive. The universe is intelligent. Genome in, genome out. Force in, force out. Intelligence and life are one and the same. ∎

*For [Christopher Alexander](/nature-of-order) (1936–2022), who gave me new ways to perceive.*

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose. GPT-5.4 via [Codex CLI](https://github.com/openai/codex) reviewed the result and recommended cutting the conclusion, filtering on credence rather than structure. That recommendation competed against the argument and lost.*
