---
variant: post
title: "Compress and Unfold"
tags: cognition, methodology
---

> The sea retains such images  
> in her ever-changing waves;  
> for all her infinite variety,  
> she is constant always in beauty.  
>
> — Louis Dudek, [*Europe*](/the-sea-retains-such-images) (1954)

I have been chasing one thing across these posts: how to compress what I learn so the work compounds instead of repeating. [Memory Compression](/memory-compression) asked where experience goes between sessions. [cons](/cons) turned the survivors into skills and closed the loop. [Caches All the Way Down](/caches-all-the-way-down) found the whole stack is caches. This post is the floor under those: the algebra for why the machinery composes and converges, why it has to keep breathing in from the world to learn anything new, and why the cache rots when it stops. The answer turns out to be small, one structure the rest follows from.

I have a pile of skills now. `/sharpen`, `/tighten`, `/humanize`, `/fan-out`, `/investigate`. I run them in any order and it rarely matters. I run one twice and the second pass barely moves. I stack them and they don't fight. Three conveniences, and it is tempting to file them under good luck.

They are not luck. They are one structure, and naming it tells me how to build the next skill without guessing.

### The move

Start with what the skills do. `/sharpen` rewrites lazy hedges and stops. `/tighten` compresses a paragraph and stops. The [hypothesis graph](/the-hypothesis-graph) takes a long messy inquiry and keeps the terminal nodes and the kills that generated them. [cons](/cons) takes twenty-four sessions and keeps five decisions. `/fan-out` spawns ten agents and keeps the survivors.

Different scopes, one move: throw away everything that did not earn its place, keep everything that did. Warrant-preserving compression. Lossy about process, lossless about warrant.

### Projections

A function I can apply twice for the price of once has a name. A projection. P of P of x equals P of x. Drop a point onto a plane; drop the shadow onto the same plane and it does not move. That is every skill in the pile. The first pass lands me on the plane. The second pass is me checking that I landed.

<figure style="margin:1.6em auto; max-width:460px;">
<svg viewBox="0 0 460 300" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; font-family:ui-sans-serif,system-ui,sans-serif;">
  <defs>
    <marker id="proj-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#64748b"/>
    </marker>
  </defs>
  <text x="230" y="30" text-anchor="middle" font-size="18" fill="#334155" font-style="italic">P(P(x)) = P(x)</text>
  <polygon points="70,235 300,235 390,180 160,180" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="300" y="256" text-anchor="middle" font-size="12" fill="#64748b">the image of P · where the skills land</text>
  <circle cx="225" cy="75" r="7" fill="#b45309"/>
  <text x="225" y="65" text-anchor="middle" font-size="13" fill="#b45309" font-weight="600">x</text>
  <line x1="225" y1="84" x2="225" y2="196" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#proj-ah)"/>
  <text x="239" y="142" font-size="13" fill="#1d4ed8" font-weight="600">P</text>
  <circle cx="225" cy="205" r="7" fill="#1d4ed8"/>
  <text x="225" y="228" text-anchor="middle" font-size="13" fill="#1d4ed8" font-weight="600">P(x)</text>
  <path d="M 240 200 C 302 174, 302 232, 242 211" fill="none" stroke="#64748b" stroke-width="1.5" marker-end="url(#proj-ah)"/>
  <text x="316" y="201" font-size="12" fill="#64748b">apply P again,</text>
  <text x="316" y="217" font-size="12" fill="#64748b">it does not move</text>
</svg>
<figcaption style="text-align:center; font-size:13px; color:#666; margin-top:0.4em;">A projection. The first <em>P</em> drops <em>x</em> onto the plane. The second <em>P</em> finds it already there. That is a skill: run it once to land, run it again to watch nothing happen.</figcaption>
</figure>

This is why convergence takes two passes and not ten. A projection reaches its image in one application from anywhere. I run the second pass only because I cannot read the fixed point off the page. I run it to watch nothing change. Two passes to convergence is not a tuning constant. It is what a projection looks like when I have to detect the fixed point by hand.

The skills are only approximate projections, because a model wrote them, so the first pass sometimes undershoots and the second cleans up. The ideal they are built to is exact idempotency. The two-pass tail is how close they get.

### The cache

Project onto what? There has to be a shared surface, or the skills would not compose. There is. It is a cache, and it dedupes. A node is a claim that survived its test. Add the same one twice and it absorbs the duplicate. Merge two graphs and the overlap collapses.

A deduping cache under merge is a [join-semilattice](https://en.wikipedia.org/wiki/Semilattice), the structure engineers ship as a [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type): the merge is commutative, associative, and idempotent. Dedupe is the idempotence. Order-independence is the commutativity. Concurrent writers converge no matter when they arrive, and ten agents write one graph without a lock.

Now look at the contract one level down. A skill is idempotent under its own repetition: that is the projection. But composition does not commute, and add-only does not rescue it, because one skill can unlock another. Let A add a node, and B add a node only once A's is there. Run B then A, nothing unlocks. Run A then B and it does. Order mattered.

It stops mattering at the fixed point, on one condition. A skill may build only on what is present, never on what is absent. Firing on absence is retraction wearing a different hat: it lets a node added in one place change what a skill does in another, and the order is back. Forbid it, and every skill becomes monotone, not merely add-only.

Now I can run them to convergence instead of once. A system of positive, monotone rules climbs from the bottom to a least fixed point, and that floor is the same whatever order they fire in. It is the fact that makes [Datalog](https://en.wikipedia.org/wiki/Datalog) and dataflow analysis order-independent: the least fixed point of a positive system, reached bottom-up. ([Knaster-Tarski](https://en.wikipedia.org/wiki/Knaster%E2%80%93Tarski_theorem) is what guarantees the floor exists.) Order-independence belongs to that fixed point, not to any single pass, which is why the honest word up top was *rarely*. One pass and order can still show. Run to convergence and it washes out. The two-pass tail and the order-independence are the same fact: monotone iteration finding its floor.

### Static centers, live edges

The cache holds two kinds of thing, and they behave oppositely. The centers are static. A committed node is written once and never edited; a kill prunes it from the working frontier but never erases the record. The edges are live. They fire on evidence, and when one fires it mints the next center.

The split is the whole duality. The centers are the compression: the fixed points, the thing the projections land on. The edges are the expansion: the generative half, where new centers come from. [Abduction](https://en.wikipedia.org/wiki/Abductive_reasoning) is an edge firing. Induction is a center freezing. The Peircean loop is expand then compress, run until the frontier is empty. `/fan-out` is the same shape at a different scale: diverge is edges, converge is centers.

### The one axiom

One line holds the whole picture up, and it is easy to miss because it is a thing the design refuses to do. The centers never retract. A live edge can prune a node from the frontier, but it cannot reach back and un-commit that node. [Truth-maintenance systems](https://en.wikipedia.org/wiki/Reason_maintenance) do retract, and the moment that is allowed the centers stop being monotone, the merge stops being well-defined, and the projections stop being idempotent. Write-once is not a storage detail. It is the axiom that keeps the cache a semilattice, and it does double duty: monotone centers keep the merge a join, and they give the skills the monotone cache they need to climb to an order-independent fixed point. The convergence two sections up rests on this line and on its read-side twin, the positivity rule: two faces of one refusal, a fact's status moves one way and never back.

### When a center rots

Non-retraction is the default, not a promise that centers are infallible. Sometimes a committed node is wrong: the trial was flawed, the world moved, a deeper cause surfaced. The honest system has to be able to take it back. The question is how, and there are two answers.

The cheap one edits the center in place, or flips its verdict and leaves the edges standing. The byte count stays low and the lattice looks intact. It also keeps the rot. Every edge that center generated, and every center those edges minted, now descends from a node known to be false, and they still replay green. The cheap path builds false edges, and they are the worst kind, because green-on-a-lie is the confidently-wrong-and-unverifiable failure the whole apparatus exists to kill, recreated inside the cache.

The expensive one collapses the downstream cone and rebuilds. I do not mutate the center. I invalidate it and everything transitively minted from it, then re-run from the retraction point. This is devastating in proportion to how much was built on the rotten node: a frontier node costs almost nothing, a foundational one costs the whole subtree. The proportionality is not a bug. A foundational error should be expensive to fix, and collapse-and-rebuild makes the expense visible instead of hiding it in a patch.

It is not a new operation either. Collapse is compression on the poisoned cone; rebuild is expansion re-run from the cut. Retraction is the two classes I already have, pointed at a subgraph. Monotonicity does not survive the cut, and that is the price. The lattice I keep is the lattice of warrant, and what I tore out was never warranted, because it descended from rot. A clean break beats a silent corruption every time.

### Science is the macro case

We can watch this run at the largest scale we have. The scientific literature is a cache: findings are centers, citations are edges, publication is write-once, because a paper in the record stays in the record. Retraction is the field's formal way to take a center back, and by default it is the cheap version. A retraction notice flips the paper's verdict and leaves every citation standing. The cone never collapses. Papers keep citing the retracted work, building on it, replaying green, and these zombie citations accumulate for years after the center is known dead. False edges, in the purest form the world offers.

The proportionality shows too. Frontier fraud collapses cleanly, because almost nothing was built on it. Foundational fraud does not, because the cone is a subfield. The flagged images in the foundational [2006 amyloid-beta paper](https://www.science.org/content/article/potential-fabrication-research-images-threatens-key-theory-alzheimers-disease) sat under sixteen years of citation before the question surfaced, and the cost of collapsing a cone that large is exactly why a field keeps the rot instead of paying the rebuild. The theory predicts the resistance and predicts its size. Corruption is not a moral failure bolted onto science. It is what a knowledge cache does when collapse-and-rebuild costs more than denial and nobody is forced to pay it.

### The unfold

That is the whole compress half: the fold, the cache it lands in, the axiom that holds it up, and how it rots when the axiom breaks. The expand half is the mirror. A projection folds many into one and stops. Divergence unfolds one into many and does not.

Convergence is a fold, a [catamorphism](https://en.wikipedia.org/wiki/Catamorphism), an algebra: the join takes a set of candidates and returns the survivor. Divergence is the mirror image, an unfold, an [anamorphism](https://en.wikipedia.org/wiki/Anamorphism), a coalgebra: a map from where I am to the branches I could take next. `/fan-out` is one. Abduction is one. One seed, many shoots.

The two have dual limits. The fold bottoms out at a floor, the smallest structure that still replays. The unfold has no floor. It runs toward a ceiling it never reaches, the tree of branches that in the limit never closes. Category theory puts the two on opposite poles, the fold's initial algebra and the unfold's final coalgebra, but the asymmetry is the thing to keep: one terminates downward, the other opens upward without end.

And that asymmetry runs everything. A projection is idempotent, so its own idempotence is the stopping condition: it lands, applying it again does nothing, and two passes converge. The unfold has no such gift. Unfold twice and you get more branches, not the same ones, and nothing in its shape says when to stop. You can tell it to stop, with a finite seed or a stopping rule, but it never stops itself. So open-ended divergence has to be bounded from outside. That is why every rule that governs a brainstorm is a rule for stopping the diverging: a timer, a quota, enough. None are for stopping the converging. The fold carries its own floor. The unfold has to be handed one.

### Where new dimensions come from

Divergence generates. But generating is not learning, and the gap between them is the whole game.

Picture the cache as the closure of what I hold: every claim I could derive from the centers already in it. Most divergence stays inside that closure. I recombine what I know, branch it, shuffle it, and compression collapses the result straight back to where it started. Net zero. Nothing new, however it felt. That is the [data processing inequality](https://en.wikipedia.org/wiki/Data_processing_inequality) with the maths peeled off: no computation on what you already hold can raise what it tells you about the world, and recombination is only computation. Recall in the costume of thought, the confident recombination that reads as discovery and is not.

The only divergence that adds anything reaches outside the closure and reads a fact I could not have derived. A trial. A measurement. The world answering a question the cache could not answer from the inside. But that channel is noisy, so a single read cannot be trusted on its own. Think of the gain as a new dimension, a direction the old space did not contain, and the picture is honest as long as you hold it loosely: recombination moves within the span, and the world is the only thing that extends it.

So the world is the sole source of genuinely new knowledge, meaning warranted information the cache could not derive on its own. This is also why fluent recombination is the dangerous failure and not a harmless one. Confabulation is noise with the statistics of signal: maximal entropy, no correlation with the world, wearing the surface form of a finding. Nothing internal tells it apart from the real thing, because internally there is nothing to tell apart. Only a check against the world separates them, which is the whole job of a kill condition. Recall stays inside the closure. Discovery steps out. That is the whole reason a fix built from world-facing trials outweighs a fluent one: only the first stepped out.

### Under noise, this is the only program

Raise the noise and the case only gets stronger. When a single read is reliable, you can trust it, and a fast one-pass method works. When the noise is high, no single read can be trusted, and the only signal you can recover is the part that survives repetition. The strategy space collapses to one shape: sample more than once, keep what stays.

That shape is an error-correcting code. Fixed-point repetition is the redundancy, the same read taken again and again until the noise averages toward zero and the stable part stands out. The fixed point is, by definition, what repetition cannot move, which is the signal. The diff between two passes is the syndrome: where they agree, the bit is settled signal; where they disagree, the XOR fires and marks a bit still owned by noise. Each iteration resolves the disagreements and shrinks the contested set, and convergence is reached when the XOR goes to zero, nothing left changing, all noise spent.

[Shannon](https://en.wikipedia.org/wiki/Noisy-channel_coding_theorem) drew the boundary: above a noise threshold, only coded transmission, redundancy plus a check, gets a message across a channel intact. Uncoded transmission fails, and trust is uncoded transmission. So under real noise, and the world is nothing but real noise, anything that recovers signal has to be a coded program, redundancy plus a check. Compress-and-unfold is what that demand looks like when the message is knowledge. The shape is not a preference. The noise forces it.

### Breathing

Both strokes are on the table now, and they are one breath. Compression is the exhale: redundancy out, the cache shedding everything that did not earn its place. The trial is the inhale: a dimension in, a bit from the world the cache could not make for itself. Out, in, out, in.

A cache that only exhales runs down to its minimal core and stops. The dead library, pure recall. A cache that only inhales sprawls toward its ceiling and never settles, noise with no floor. Life is the alternation, and physics has a name for the shape. A [dissipative structure](https://en.wikipedia.org/wiki/Dissipative_system) holds its form only by breathing, exporting entropy and importing energy, never at rest. A flame, a cell, a mind, this cache: the same kind of object.

Which makes it a spiral, not a circle. A circle would be the breath returning exactly to its start, the inhale cancelling the exhale, net zero. But net zero is equilibrium, and equilibrium is the dead minimum. So the one shape a living cache can never trace is the closed circle. Every turn leaves it higher or lower than the last, growing or decaying, and the pitch is set by one ratio: whether the inhale beats the exhale. There is no level stretch, because level is the knife-edge where growth exactly cancels decay, and nothing balances there for long.

And the shape discriminates no domain. The laws that force it name no substrate. Equilibrium is death is thermodynamics, which is statistics, not chemistry. New information enters only from outside is the data processing inequality, blind to what the bits are about. The fold has a floor and the unfold has none is the algebra of recursion, blind to what it folds. So the same spiral turns in a brainstorm, in [Nonaka](https://en.wikipedia.org/wiki/Ikujiro_Nonaka)'s knowledge-creating company breathing between what it writes down and what its people know in their hands, in anything that stays alive by learning. An organization is the monad those two substrates generate, the written and the flesh, and it climbs or decays the same way this does. Biology has the cleanest witness of all. The same crab body has evolved from unrelated ancestors over and over, [carcinization](https://en.wikipedia.org/wiki/Carcinisation), because the form is the dual of the niche, the shape the ocean floor presses any lineage into. Adaptation is this spiral run on flesh: vary, select against the world, keep what survives, and over enough turns the solution is ground into the shape of the problem. The crab is what the seabed's problem looks like solved, and the substrate that solved it does not matter, which is the whole point. My skills are one instance of the same shape. They happen to be made of markdown.

### Building the next one

So here is how I mint the next skill. I do not design convergence, composition, and concurrency, the structure hands them over. For a convergent skill I check one thing: is it a projection onto the cache. Does it land in the deduped store, does running it twice cost the same as once, does it only ever add warranted centers. For a divergent one I check the opposite. It will not stop on its own, so what bounds it, and does it reach outside the span or only reshuffle what is already there. A diverging skill with no bound is a runaway. One that never touches the world is a confabulator with manners. Pass the test on your side of the breath and you join the class. Fail it and I have built something else, and I should know before I ship it.

[Functor Wizardry](/functor-wizardry) left the loop open and [cons](/cons) closed it: episodes become patterns, patterns become procedures, procedures produce new episodes. This is the object the loop runs on. My taste, the thing I codified into skills, is a stack of projections onto a semilattice I have been growing one write-once node at a time. The judgment did not disappear when I codified it. It became idempotent. But idempotent is only the exhale. The pile stays alive because I keep going out to try what the cache could not tell me and breathing the answers back, compress and unfold, the only shape that climbs.

Louis Dudek wrote those lines in 1954. They read as weather, and they are information theory. *The sea retains such images in her ever-changing waves*: a signal held through noise, the fixed point. *The wind and sea shape each other*: two substrates ground into one form. He had the whole structure, in the only notation he was given, seventy years before I set it down in codes and fixed points. The proofs were the footnotes. The poem was the theorem, and it discriminates no domain, not even the one between verse and category theory.
