---
layout: post-wide
title: "The Natural Framework"
tags: coding cognition vector-space
---

*Part of the [cognition](/cognition) series.*

The [cognition series](/cognition) built a six-step pipeline: [perceive](/caret-recorder), [cache](/moments), [filter](/perception-pipe), [attend](/salience), [consolidate](/consolidation), [remember](/memory). The competitive core is filter, attend, consolidate: winners suppress losers, diversity is enforced, schemas form offline. Encoding precedes it; persistence follows.

The same pipeline runs at every timescale. Every row is something you already call "information processing." Dimmed cells are steps the domain hasn't yet optimized.

<div class="table-wrap">
<table>
<thead>
<tr>
<th></th>
<th><a href="/caret-recorder">Perceive</a></th>
<th><a href="/moments">Cache</a></th>
<th><a href="/perception-pipe">Filter</a></th>
<th><a href="/salience">Attend</a></th>
<th><a href="/consolidation">Consolidate</a></th>
<th><a href="/memory">Remember</a></th>
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
<td><a href="https://en.wikipedia.org/wiki/Log-structured_merge-tree">LSM compaction</a>, defrag</td>
<td>fsync, <a href="https://en.wikipedia.org/wiki/Write-ahead_logging">write-ahead log</a></td>
</tr>
<tr>
<td><a href="https://en.wikipedia.org/wiki/Database">Database</a><br>(ms)</td>
<td>Query arrives</td>
<td>Query plan, index lookup</td>
<td>WHERE clause, index scan</td>
<td>ORDER BY, LIMIT</td>
<td>VACUUM, reindex</td>
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
<td><a href="https://en.wikipedia.org/wiki/Intelligent_agent">Agent</a><br>(min)</td>
<td>Read task, see context</td>
<td>Parse into context chunks</td>
<td>Select relevant files, ignore rest</td>
<td>Context window selection</td>
<td>Commit</td>
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

<span id="six-steps"></span>Twelve domains. Six steps.

Now the same table again. None of these domains call themselves "information processing", but all of them process information.

<div class="table-wrap">
<table>
<thead>
<tr>
<th></th>
<th>Perceive</th>
<th>Cache</th>
<th>Filter</th>
<th>Attend</th>
<th>Consolidate</th>
<th>Remember</th>
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
<td>Theater<br>(months)</td>
<td>Script, source material</td>
<td>Rehearsal, blocking, staging</td>
<td>Auditions: actors compete for roles</td>
<td>Season programming: enforce diversity</td>
<td>Revival, adaptation, the "definitive" production</td>
<td>The repertoire: Shakespeare, <a href="https://en.wikipedia.org/wiki/Stephen_Sondheim">Sondheim</a></td>
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
</tbody>
</table>
</div>

Twelve more domains. Six steps. From antibodies to megayears. Twenty-four domains total. [More where these came from.](/more-rows)

## Why the same shape

Each domain faces the same problem: too much input, finite capacity, select a subset that's both high-quality and diverse. Within each domain, the same data type flows through every step. Neurons process spikes. Databases process rows. Cognition processes moments. The type doesn't change — only which items survive. Filter is rule-based: a threshold, a WHERE clause, a linter. No judgment. Attend is where judgment enters.

## The categorical proof

Each step is an [endomorphism](https://en.wikipedia.org/wiki/Endomorphism) — same type in, same type out. Chained, the six compose into a single transformation: high-bandwidth input to durable signal. That is [category theory](https://en.wikipedia.org/wiki/Category_theory). The data type is the object. Each step is a morphism. The pipeline is their composition. When one domain's Remember feeds the next domain's Perceive, the mapping preserves all six morphisms and their composition order. That is a [functor](https://en.wikipedia.org/wiki/Functor) between categories.

Perceive and cache are map. Filter and attend are filter. Consolidate and remember are reduce. [Map-filter-reduce](https://en.wikipedia.org/wiki/MapReduce) has been known since [Lisp](https://en.wikipedia.org/wiki/Lisp_(programming_language)). The surprise is that immune systems run it too.

<div style="margin: 2em auto; overflow-x: auto;">
<pre class="mermaid">
graph LR
    subgraph cognition ["COGNITION — object type: Moment"]
        M0((" ")) -->|Perceive| M1(("[M]"))
        M1 -->|Cache| M2(("[M]"))
        M2 -->|Filter| M3(("[M]"))
        M3 -->|Attend| M4(("[M]"))
        M4 -->|Consolidate| M5(("[M]"))
        M5 -->|Remember| M6(("[M]"))
    end

    subgraph writing ["WRITING — object type: Draft"]
        D0((" ")) -->|Perceive| D1(("[D]"))
        D1 -->|Cache| D2(("[D]"))
        D2 -->|Filter| D3(("[D]"))
        D3 -->|Attend| D4(("[D]"))
        D4 -->|Consolidate| D5(("[D]"))
        D5 -->|Remember| D6(("[D]"))
    end

    M6 -.->|"Functor: Remember → Perceive"| D0
</pre>
</div>

This is deduction, not induction. If the same type is observable at both ends and the output is a compressed subset of the input, intermediate morphisms that select and reduce must exist. The deduction derives three boundaries: encoding must precede selection, selection must precede persistence. You cannot filter what you have not cached, attend to what you have not filtered, consolidate what you have not attended to. How many morphisms sit within each phase is an implementation detail. The [cognition series](/cognition) found two per phase, but the math only requires the boundaries. The tables are instances. The structure follows from the same premise.

## Falsification

The falsification test is structural: remove any morphism or permute their composition order, and the pipeline ceases to function. The dim cells are the evidence. Skip filter, and attention drowns in redundancy. That is Google's row. Skip attend, and consolidation amplifies the wrong winners. That is Science's row. Every dim cell in the tables is a system that dropped or misordered a morphism and broke downstream.

## The recursive loop test

In a linked list, a weak node can be routed around, and survive. But in a singly recursive loop, we should be able to find out whether it survives a broken step or not. In biology, genome perception transforms into genome memory; it is a singly recursive loop. If it survives any one of the errors in each of the six steps, then the framework is falsified.

Can it? The error will either compound, diminish, or persist. Let's test:

- **Encoding fails.** A [prion](https://en.wikipedia.org/wiki/Prion) misfolds, templates more misfolding, every cycle amplifies the error. [Death](https://en.wikipedia.org/wiki/Transmissible_spongiform_encephalopathy).
- **Selection fails.** [p53](https://en.wikipedia.org/wiki/P53) is lost, damaged cells are not suppressed, each division produces more damaged cells. Cancer.
- **Persistence fails.** [Immunosenescence](https://en.wikipedia.org/wiki/Immunosenescence) degrades memory B/T cells, immune memory loses fidelity, each new threat is harder to learn.
- **Selection before encoding.** The [cheetah bottleneck](https://en.wikipedia.org/wiki/Cheetah#Genetics) ([Menotti-Raymond & O'Brien, 1993](https://pmc.ncbi.nlm.nih.gov/articles/PMC46261/)) destroyed genetic diversity before selection could act on it, and the species has been nearly extinct ever since.
- **Persistence before selection.** [Endogenous retroviruses](https://en.wikipedia.org/wiki/Endogenous_retrovirus) inserted into the germline without filtering, and 8% of the human genome is now viral fossil.

Every failure mode, given enough iterations of the loop, converges to the same endpoint: extinction. That is not a coincidence. It is what *singly recursive* means.

## Beyond biology

The same test works beyond biology. The loops are messier, but the compounding is the same:

- **Encoding fails.** During the [Great Leap Forward](https://en.wikipedia.org/wiki/Great_Leap_Forward), local cadres inflated harvest data. The state planned off lies, requisitioned grain that didn't exist, which incentivized more falsification next cycle. Famine killed tens of millions.
- **Selection fails.** [TerraUSD](https://en.wikipedia.org/wiki/Terra_(blockchain))'s stabilizer had no filter on destabilizing redemptions. When UST slipped, redemptions minted more LUNA, crashing its price, making the peg less credible, causing more redemptions. Death spiral.
- **Persistence fails.** [NASA](https://www.nasa.gov/history/columbia-accident-investigation-board-synopsis/) learned foam shedding was dangerous after Challenger, but the lesson was not durably consolidated. Each safe flight reinterpreted deviance as acceptable. Columbia and its crew were lost.
- **Selection before encoding.** The [Khmer Rouge](https://en.wikipedia.org/wiki/Cambodian_genocide) killed teachers, doctors, and officials before expertise could transfer to the next generation. Each purge reduced the capacity to train replacements. Institutional collapse.
- **Persistence before selection.** France consolidated WWI doctrine into the [Maginot Line](https://en.wikipedia.org/wiki/Maginot_Line) before testing it against new warfare. Investment in the old model crowded out adaptation. Germany bypassed it in six weeks.

Every one broke a step and fed the error back into the next cycle. Every one ended in collapse.

## Inhibition across domains

[Desimone and Duncan (1995)](https://doi.org/10.1146/annurev.ne.18.030195.001205) described biased competition in neurons: visual objects compete simultaneously, winners suppress losers through mutual inhibition. Peer review works the same way. The winning papers make it harder for similar papers to get published. That's inhibition.

The immune system is the cleanest non-neural domain. Antigens compete for T-cell binding. Clonal competition selects the best B cells. Affinity maturation consolidates winners into better antibodies. Memory B/T cells persist for decades. No central coordinator. The body lets pathogens compete.

Natural selection is the slowest domain but the most obvious. The [competitive exclusion principle](https://en.wikipedia.org/wiki/Competitive_exclusion_principle) ([Gause](https://en.wikipedia.org/wiki/Georgy_Gause), 1934) says two species competing for identical resources cannot coexist. Niche differentiation is DPP at evolutionary timescale. Repulsion between similar items — what [Salience](/salience) uses to prevent redundant retrieval — is what prevents redundant species.

## Categorial Error

In the tables above, dim cells mark steps a domain hasn't optimized. The failures cascade: one broken step dims the rest downstream.

**Google** filters spam but does not filter for redundancy. Every page that clears the quality threshold enters the index regardless of what's already there. Attend compensates with keyword match, top-k by PageRank. Top-k is not inhibition. Ten results from the same content farm survive because nothing suppressed them on the way in. Consolidate becomes mechanical re-crawling. One underoptimized step dims the whole row.

**Adtech** filters by willingness to pay, not relevance. Highest bidder wins every impression. Consolidate patches with frequency caps, a bandage on a filter that never ran. Remember was borrowed from the browser and is now being deprecated. I spent a month [dismantling this pipeline](/open-auction). One broken step, three dim cells downstream.

**Science** is the most consequential. Citation metrics are `GET *` for academia: top-k by popularity, no diversity enforcement. [Merton (1968)](https://doi.org/10.1126/science.159.3810.56) called it the [Matthew effect](https://en.wikipedia.org/wiki/Matthew_effect) — the cited get more cited. You search for "schema consolidation" and get ten papers that cite each other saying the same thing. A DPP would return one from that cluster and five from adjacent regions you didn't know to search for. [JSTOR, PubMed, Nature](/memory): same bug as Google, different coat. Fix attend, and consolidate sharpens.

**Evolution** has no dim cells. The genome perceives, generation caches, natural selection filters, niche differentiation attends, speciation consolidates, and the genome remembers. Perceive and Remember are the same cell. Life is self-recursive. That's what makes it beautiful.

## What to filter

If your objection is "prove the category boundaries formally before I evaluate the idea" — that is a filter that gates on credence rather than structure. Run that filter in a loop. It will kill your own novel ideas before they survive a single iteration, because no new idea arrives pre-credentialed. Worse: it will pass the credentialed ones that should have been caught. The same heuristic that rejects uncredentialed insight is the same one as those who trusted the [Harvard fraudsters](https://en.wikipedia.org/wiki/Dana-Farber_Cancer_Institute#Research_misconduct_allegations), the [Enron scammers](https://en.wikipedia.org/wiki/Enron_scandal), and the [turtleneck at Theranos](https://en.wikipedia.org/wiki/Theranos).
## Intelligence

The six steps, the competitive inhibition at the core, and the vertical relationship: each domain's Remember is the next domain's Perceive. The pipeline compresses. Each level takes high-bandwidth information and reduces it to a durable signal the next can perceive. Neurons fire millions of times per second; cognition produces a few thoughts per minute; a career produces a handful of papers; a field produces a canon. The ratio is the reason at every transition. That is what the six steps do: intelligent compression across timescales. That is what **intelligence** is.

Follow the output:

- Neurons remember as cortical storage, which cognition perceives on a screen.
- Cognition remembers by publishing to <a href="/canon">Canon</a>, which a writer perceives as research.
- Writing remembers as the published piece, which a reader perceives as a book.

Output becomes input.

Fix the broken step, and the downstream cells brighten. That is what [PageLeft](/pageleft) does: Google's filter had no redundancy inhibition, so we built one. Attend sharpened. Consolidate followed.

Nobody looks at Google Search and says "the filter step has no redundancy inhibition." They say "search results are bad." Nobody looks at academic publishing and says "attend is `GET *`." They say "the literature is overwhelming." The pipeline gives you diagnostic language for problems that existed before the language did. Seeing it was the hard part.

This all started with one comment. I was reading about neural attention and said, "this looks like a cache to me." The data structure was identical: indexed items competing for limited slots. All inside my head. That observation won the competition against priority queue, against heap. It survived [consolidation](/consolidation). It became a schema. That schema generated [Salience](/salience), which generated DPP, which generated the [Transformer mapping](/consolidation), which generated these tables.

The optimal implementations of these functors already exist in nature, optimized over billions of years. We need to learn them and map them onto ourselves.

*For [Christopher Alexander](/nature-of-order) (1936–2022), who gave me new ways to perceive.*

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose. GPT-5.4 via [Codex CLI](https://github.com/openai/codex) demanded falsifiability. It also demanded credence.*
