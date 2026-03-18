*Part of the [cognition](/cognition) series.*

In software, we say "everything's a wrapper." An ORM wraps SQL, which wraps disk I/O, which wraps silicon. Each layer exposes the same four verbs (create, read, update, delete) and delegates to the layer below. Wrappers all the way down.

But CRUD is only the Remember interface. Store, retrieve, update, delete: that's the API to the persistent store. When we say "wrapper" we're seeing one role out of [six](/the-natural-framework) and calling it the whole thing.

## The rest of the pipeline

SQL has `WHERE` (Filter) and `ORDER BY` (Attend). The ORM above it has scopes (Filter) and eager loading (Attend). The API above that has authorization (Filter) and pagination (Attend). The frontend above that has conditional rendering (Filter) and sort/highlight (Attend).

Every layer re-implements the full pipeline over the data from the layer below. We say "just a wrapper" because Remember looks identical at every level. The other roles look different, so we don't notice the repetition.

## The computing stack

Digital computing is the clearest case because we built it from the floor up. The entire hardware-software stack is the Cache tower made visible, each level adding capacity until the full pipeline emerges.

<div class="table-wrap">
<table>
<thead>
<tr>
<th style="background:#f0f0f0">Level</th>
<th style="background:#f0f0f0">Cache capacity</th>
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
<td style="color:#c62828"><a href="https://en.wikipedia.org/wiki/Transistor" style="color:inherit">Transistor</a></td>
<td>1 bit</td>
<td>Voltage</td>
<td>—</td>
<td>Threshold gate</td>
<td>—</td>
<td>—</td>
<td>—</td>
</tr>
<tr>
<td style="color:#e65100"><a href="https://en.wikipedia.org/wiki/Logic_gate" style="color:inherit">Logic gate</a></td>
<td>few bits</td>
<td>Input lines</td>
<td style="color:#c62828">Transistors</td>
<td>Boolean function</td>
<td>—</td>
<td>—</td>
<td>Output line</td>
</tr>
<tr>
<td style="color:#f9a825"><a href="https://en.wikipedia.org/wiki/Arithmetic_logic_unit" style="color:inherit">ALU</a></td>
<td>word</td>
<td>Operands, opcode</td>
<td style="color:#e65100">Logic gates, registers</td>
<td>Overflow, flags</td>
<td class="dim">Opcode selects operation</td>
<td>—</td>
<td>Result register</td>
</tr>
<tr>
<td style="color:#2e7d32"><a href="https://en.wikipedia.org/wiki/Central_processing_unit" style="color:inherit">CPU</a></td>
<td>KB (L1)</td>
<td>Fetch instruction</td>
<td style="color:#f9a825">ALUs, pipeline stages</td>
<td>Branch prediction</td>
<td class="dim">Scheduling, out-of-order</td>
<td class="dim">Branch predictor learns</td>
<td>Register file, L1 cache</td>
</tr>
<tr>
<td style="color:#00838f"><a href="https://en.wikipedia.org/wiki/Operating_system" style="color:inherit">OS</a></td>
<td>GB (RAM)</td>
<td>Interrupts, I/O</td>
<td style="color:#2e7d32">CPUs, memory hierarchy</td>
<td><a href="https://en.wikipedia.org/wiki/Cache_replacement_policies">Cache eviction</a></td>
<td class="dim">Scheduler dispatch</td>
<td class="dim">Defrag, compaction</td>
<td>Filesystem, swap</td>
</tr>
<tr>
<td style="color:#1565c0"><a href="https://en.wikipedia.org/wiki/Database" style="color:inherit">Database</a></td>
<td>TB (disk)</td>
<td>Query arrives</td>
<td style="color:#00838f">OS filesystem, B-trees</td>
<td>WHERE clause</td>
<td>ORDER BY, LIMIT</td>
<td class="dim">VACUUM, reindex</td>
<td>The table on disk</td>
</tr>
<tr>
<td style="color:#6a1b9a">Backend</td>
<td>app memory</td>
<td>Request arrives</td>
<td style="color:#1565c0">Database, ORM</td>
<td>Auth, validations</td>
<td>Pagination, sorting</td>
<td class="dim">Schema migrations</td>
<td>Database write</td>
</tr>
<tr>
<td style="color:#bf360c">Frontend</td>
<td>viewport</td>
<td>User event</td>
<td style="color:#6a1b9a">Backend responses, DOM</td>
<td>Conditional rendering</td>
<td>Sort, highlight, focus</td>
<td class="dim">User preferences</td>
<td>localStorage, DOM state</td>
</tr>
<tr>
<td style="color:#558b2f"><a href="https://en.wikipedia.org/wiki/Containerization_(computing)" style="color:inherit">Container</a></td>
<td>image layers</td>
<td>Build context</td>
<td style="color:#bf360c">Applications, runtime</td>
<td>.dockerignore, multi-stage discard</td>
<td>Layer ordering for cache hits</td>
<td class="dim">Image optimization</td>
<td>Image in registry</td>
</tr>
<tr>
<td style="color:#c62828"><a href="https://en.wikipedia.org/wiki/Kubernetes" style="color:inherit">Kubernetes</a></td>
<td>cluster</td>
<td>Desired state, metrics</td>
<td style="color:#558b2f">Containers, <a href="https://etcd.io/">etcd</a></td>
<td><a href="https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/">Admission controllers</a>, resource quotas</td>
<td>Scheduler: affinity, constraints</td>
<td><a href="https://kubernetes.io/docs/concepts/extend-kubernetes/operator/">Operator</a> reconciliation loops</td>
<td>Cluster state</td>
</tr>
<tr>
<td style="color:#e65100"><a href="https://en.wikipedia.org/wiki/Autoscaling" style="color:inherit">Autoscaler</a></td>
<td>fleet</td>
<td>CPU, memory, request rate</td>
<td style="color:#c62828">Kubernetes clusters</td>
<td>Cooldown periods, min/max bounds</td>
<td>Scaling policy: which pool, how much</td>
<td>Policy tuning from history</td>
<td>The running fleet</td>
</tr>
</tbody>
</table>
</div>

The transistor row: one bit, pure threshold gating, no Attend, no Consolidate. The bool store. The autoscaler row: full pipeline across a fleet. Each row between them added capacity, and each time it crossed a threshold, another role filled in.

Nobody designed it this way. Engineers at each level solved their local problem ("hold more items, select among them, rank the survivors") and arrived at the same pipeline independently. Add storage, and Filter and Attend follow.

## The biological stack

The same tower in a person's energy storage. Each level caches the level below.

<div class="table-wrap">
<table>
<thead>
<tr>
<th style="background:#f0f0f0">Level</th>
<th style="background:#f0f0f0">Cache capacity</th>
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
<td style="color:#c62828"><a href="https://en.wikipedia.org/wiki/Adenosine_triphosphate" style="color:inherit">ATP</a></td>
<td>1 bond</td>
<td>Substrate arrives</td>
<td>—</td>
<td><a href="https://en.wikipedia.org/wiki/Enzyme_specificity">Enzyme lock-and-key</a></td>
<td>—</td>
<td>—</td>
<td>—</td>
</tr>
<tr>
<td style="color:#e65100"><a href="https://en.wikipedia.org/wiki/Mitochondrion" style="color:inherit">Mitochondrion</a></td>
<td>many ATP molecules</td>
<td>Pyruvate, O₂</td>
<td style="color:#c62828">ATP molecules</td>
<td><a href="https://en.wikipedia.org/wiki/Mitochondrial_membrane_potential">Membrane potential</a> threshold</td>
<td class="dim"><a href="https://en.wikipedia.org/wiki/Uncoupling_protein">Uncoupling proteins</a></td>
<td>—</td>
<td>ATP output rate</td>
</tr>
<tr>
<td style="color:#f9a825"><a href="https://en.wikipedia.org/wiki/Cell_(biology)" style="color:inherit">Cell</a></td>
<td><a href="https://en.wikipedia.org/wiki/Glycogen">glycogen</a> granules</td>
<td>Glucose, insulin signal</td>
<td style="color:#e65100">Mitochondria</td>
<td>Metabolic gating (<a href="https://en.wikipedia.org/wiki/Hexokinase">hexokinase</a>)</td>
<td>Energy allocation across processes</td>
<td><a href="https://en.wikipedia.org/wiki/Gene_expression">Gene expression</a></td>
<td>Glycogen, protein</td>
</tr>
<tr>
<td style="color:#2e7d32"><a href="https://en.wikipedia.org/wiki/Liver" style="color:inherit">Liver</a></td>
<td>~100g glycogen</td>
<td>Blood glucose, hormones</td>
<td style="color:#f9a825">Cells, <a href="https://en.wikipedia.org/wiki/Hepatocyte">hepatocytes</a></td>
<td><a href="https://en.wikipedia.org/wiki/Glucokinase">Glucokinase</a> threshold</td>
<td><a href="https://en.wikipedia.org/wiki/Glycogenesis">Glycogenesis</a> vs <a href="https://en.wikipedia.org/wiki/Gluconeogenesis">gluconeogenesis</a></td>
<td>Metabolic adaptation</td>
<td>Blood glucose level</td>
</tr>
<tr>
<td style="color:#00838f"><a href="https://en.wikipedia.org/wiki/Adipose_tissue" style="color:inherit">Adipose</a> / <a href="https://en.wikipedia.org/wiki/Muscle_atrophy#Cachexia" style="color:inherit">muscle</a></td>
<td>kg of fat, kg of protein</td>
<td>Insulin, excess energy</td>
<td style="color:#2e7d32">Liver, circulating glucose</td>
<td><a href="https://en.wikipedia.org/wiki/Lipogenesis">Lipogenesis</a> threshold</td>
<td>Which depots to mobilize</td>
<td><a href="https://en.wikipedia.org/wiki/Set_point_(body_weight)">Set point</a> adjustment</td>
<td>Fat mass</td>
</tr>
<tr>
<td style="color:#1565c0"><a href="https://en.wikipedia.org/wiki/Mammal" style="color:inherit">Mammal</a></td>
<td>total reserves</td>
<td>Hunger, satiety signals</td>
<td style="color:#00838f">Adipose, muscle</td>
<td><a href="https://en.wikipedia.org/wiki/Ghrelin">Ghrelin</a>, <a href="https://en.wikipedia.org/wiki/Leptin">leptin</a>, appetite regulation</td>
<td>Meal choice, macronutrient balance</td>
<td>Metabolic adaptation, <a href="https://en.wikipedia.org/wiki/Gut_microbiome">microbiome</a></td>
<td>Body composition</td>
</tr>
</tbody>
</table>
</div>

ATP: one phosphate bond, pure enzyme gating. The bool store. The mammal row: full pipeline with hunger, choice, and metabolic adaptation. Same tower. Capacity grows, roles fill in. Evolution built each level because the one below couldn't manage energy at the scale above.

Two substrates. Same staircase. Each level's Cache is the level below, and each added enough capacity for another role to fill in. The shape repeats because the constraint forces it. The constraint also forces it to stop.

## The tower has a floor

By induction on storage capacity.

*Base case.* A Cache with one bit of storage is a [boolean](https://en.wikipedia.org/wiki/Boolean_data_type). Pass or reject. Selection requires at least two items; one slot has nothing to compare. The only operation is threshold gating: a single `if`. No Attend (nothing to rank), no Consolidate (nothing to learn). The pipeline collapses to Filter alone.

*Inductive step.* A Cache at depth *d* with capacity *S* may contain a sub-pipeline whose sub-Cache at depth *d+1* has capacity *S'*. [Boundary 1](/the-natural-framework) applies: the sub-Cache must fit inside the parent, so *S'* < *S* by [pigeonhole](https://en.wikipedia.org/wiki/Pigeonhole_principle). Strictly decreasing.

*Termination.* Capacity is a natural number. A strictly decreasing sequence of naturals terminates. It reaches 1 bit. The tower has finite depth.

How deep is the universe's cache? As deep as physics allows — down to whatever distinction is smallest. A qubit. A Planck bit. The bool store at the bottom of everything.

<img src="/assets/cache-tower.svg" alt="Three nested pipelines — CPU, ALU, Logic Gate — each Cache zooms into the full pipeline of the level below. At the bottom, transistors reduce to a bool store: 0 or 1. The tower terminates." style="width:100%; max-width:620px; display:block; margin:1.5em auto;">

[The Handshake](/the-handshake) proves the analogous result for Consolidate: induction on bit budget, with the [data processing inequality](https://en.wikipedia.org/wiki/Data_processing_inequality) as the decreasing measure, terminating at passthrough. Cache's tower uses storage capacity instead, terminating at the bool store. Same structure, different measures. Consolidate is about compression. Cache is about capacity.

## Bool stores in the wild

At the floor of every Cache tower, you should find a bool store doing threshold gating. And you do.

*Ion channels:* open or closed. One bit. Voltage threshold gates molecules through. No ranking, no learning. Pure Filter.

*Transistors:* on or off. Voltage above threshold passes the signal. Below, it blocks.

*MHC binding:* fits or doesn't. [Antigen presentation](https://en.wikipedia.org/wiki/Antigen_presentation) at the molecular level is a shape match — binding affinity is graded, but the groove either holds the peptide or releases it. Ranking among candidates happens one level up, where limited surface slots force selection among the fragments that passed.

Each is a Cache collapsed to a boolean. The prediction: below a bool store, no further self-similarity. You can't have a sub-pipeline inside an `if` statement. If you found something smaller than a bool still doing selection, the argument would be falsified. But a bool is the minimum unit of distinction.

## The AI stack

The same tower for AI. Read the dim cells.

<div class="table-wrap">
<table>
<thead>
<tr>
<th style="background:#f0f0f0">Level</th>
<th style="background:#f0f0f0">Cache capacity</th>
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
<td style="color:#c62828">Weight</td>
<td>1 float</td>
<td>Gradient</td>
<td>—</td>
<td>Learning rate threshold</td>
<td>—</td>
<td>—</td>
<td>—</td>
</tr>
<tr>
<td style="color:#e65100"><a href="https://en.wikipedia.org/wiki/Artificial_neuron" style="color:inherit">Neuron</a></td>
<td>~hundreds of weights</td>
<td>Input vector</td>
<td style="color:#c62828">Weights</td>
<td><a href="https://en.wikipedia.org/wiki/Rectifier_(neural_networks)">ReLU</a>, activation</td>
<td>—</td>
<td class="dim">Backprop (offline, sealed)</td>
<td>Activation output</td>
</tr>
<tr>
<td style="color:#f9a825"><a href="https://en.wikipedia.org/wiki/Attention_(machine_learning)" style="color:inherit">Attention head</a></td>
<td>~millions params</td>
<td>Query, key, value</td>
<td style="color:#e65100">Neurons</td>
<td><a href="https://en.wikipedia.org/wiki/Softmax_function">Softmax</a> masking</td>
<td>Attention scores</td>
<td class="dim">Training (sealed)</td>
<td>Weighted value</td>
</tr>
<tr>
<td style="color:#2e7d32"><a href="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)" style="color:inherit">Block</a></td>
<td>attention heads</td>
<td>Residual input</td>
<td style="color:#f9a825">Attention heads</td>
<td><a href="https://en.wikipedia.org/wiki/Layer_normalization">Layer norm</a></td>
<td>Multi-head selection</td>
<td class="dim">Training (sealed)</td>
<td>Block output</td>
</tr>
<tr>
<td style="color:#00838f">Model</td>
<td>billions of params</td>
<td>Token sequence</td>
<td style="color:#2e7d32">Blocks, <a href="https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)#KV_cache" style="color:inherit">KV cache</a></td>
<td class="dim">No input gating</td>
<td class="dim">No diversity enforcement</td>
<td class="dim">Training (sealed)</td>
<td>Next token</td>
</tr>
<tr>
<td style="color:#1565c0">Context window</td>
<td>~128K tokens</td>
<td>User prompt, tool results</td>
<td style="color:#00838f">Model</td>
<td class="dim">Minimal redundancy inhibition</td>
<td class="dim">Recency bias, no DPP</td>
<td class="dim">Ephemeral — dies with the session</td>
<td>Response</td>
</tr>
<tr>
<td style="color:#6a1b9a"><a href="https://en.wikipedia.org/wiki/Intelligent_agent" style="color:inherit">Agent</a></td>
<td>context + tools</td>
<td>Task, codebase</td>
<td style="color:#1565c0">Context windows</td>
<td class="dim">File selection heuristics</td>
<td class="dim">Context window selection</td>
<td class="dim">Skill creation, memory files</td>
<td>Completed task</td>
</tr>
<tr>
<td style="color:#bf360c">Swarm</td>
<td>fleet of agents</td>
<td>Workload</td>
<td style="color:#6a1b9a">Agents</td>
<td class="dim">Task routing</td>
<td class="dim">Load balancing</td>
<td class="dim">No shared learning</td>
<td class="dim">No collective memory</td>
</tr>
</tbody>
</table>
</div>

The forward pass is well-optimized at the bottom: softmax is genuine Filter, attention scores genuine Attend. But Consolidate is dim at every level. Training is sealed, so the model learns nothing from its conversation and the context window dies with the session. The agent's memory files are a bandage, not a schema.

Above the model level, almost everything is dim. The context window has minimal redundancy inhibition; every token gets in until the window is full. The agent selects files by heuristic, not competition. The swarm has no shared memory, no collective consolidation.

The computing stack filled in its dim cells over sixty years. The biology stack filled them in over four billion. The AI stack is a few years old and it shows. The dim cells are the roadmap.

## The diagnostic

Active Consolidate within a Cache means there's at least one more level below. Passthrough means you've hit the floor. The [query optimizer](https://en.wikipedia.org/wiki/Adaptive_query_optimization) learns from execution statistics, so it contains another pipeline. Ion channels don't learn. The gate is the gate.

Every thin wrapper that's genuinely CRUD passthrough either stays thin (it was at the floor, with nothing to learn) or grows filter and attend logic (it was above the floor, and usage pressure forced the missing roles in). Every ORM starts thin. The ones above the floor never stay that way.

It's not wrappers all the way down. It's pipelines — until you hit the bool.

---

*Written via the [double loop](/double-loop). More at [pageleft.cc](https://pageleft.cc).*
