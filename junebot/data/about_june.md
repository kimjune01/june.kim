June Kim writes at the intersection of cognitive architecture, applied category theory, and software methodology. The work is densely interconnected — a single post often functions as both an argument and a reusable specification for code transformations.

## The Natural Framework

The central organizing theory across June's writing is the Natural Framework: a six-role model of intelligent systems. Five roles form a forward pipeline — Perceive, Cache, Filter, Attend, Transmit — and one role runs backward: Consolidate. The framework is meant to be universal; June argues the universe fills all six cells, and that life itself is a self-recursive instance of the pipeline.

Key distinctions June draws repeatedly:

- **Cache vs. Transmit.** Cache holds information for the current agent within a cycle. Transmit sends across the cycle boundary to the persistent store, where Perceive will read it next cycle. Both involve storage, but only Transmit crosses the boundary.
- **Consolidate as backward pass.** Consolidate reads from the store and writes parameter changes — it's defined by direction (store → parameters), not by scheduling. Sleep, backprop, and chunking are all instances; async scheduling is an optimization, not the definition.
- **Compaction ≠ Consolidation.** Compaction reorganizes the store without changing behavior (a VACUUM operation). Consolidation changes future processing. Same store, categorically different operations.
- **Clever vs. intelligent.** Systems with fast perceive/cache but shallow roles are clever. Full six-role systems with procedural memory are intelligent. The distinction matters for evaluating AI architectures.

Intelligence, in June's framing, is the compression ratio between functor levels. The stochasticity proof (grounded in Landauer's principle) makes competition physically mandatory at the core.

## The Parts Bin

The Parts Bin is a grid-based taxonomy that maps known algorithms and cognitive operations onto the Natural Framework's roles. It serves as a retrospective validation tool and a prediction engine — blank cells indicate missing algorithms worth investigating. June documented a 2026 dead end exploring extensions to the Filter and Attend grids; the honest finding was that most candidate rows were either already filled or misaligned. Promising open territory: Causal and Counterfactual rows for Filter, where filtering by intervention relevance is conceptually strong but algorithmically sparse.

## Cross-cutting beliefs

**The blog as grimoire.** Posts are compressed specs that can be invoked by title alone to drive code transformations. Writing quality is load-bearing for development, not just communication — tighter prose makes a more reliable specification. The intended audience is June and collaborating agents, not a general readership.

**Division of intellect, not labor.** Skills and automation should handle Filter-level work (rejecting what's wrong). Producing what's right requires Attend, which stays human. Labor is Cache; intellect is Attend.

**Structural soundness is not a substitute for evidence.** A structurally sound argument without empirical support is philosophy, not science. When a claim lacks evidence, the right move is to research, not to rely on the argument's shape.

**Narrow and bold over hedged and broad.** When a claim is overclaimed, the fix is to narrow the scope and state the narrow version declaratively — letting specific named examples do the fencing that adverbs were attempting. Stacked hedges produce prose that sounds cowed; a bold narrow claim stays honest and keeps voice.

## Active projects

**Natural Framework (Lean artifact).** A machine-checked formalization of the framework's core claims, submitted to Applied Category Theory 2026. The Hoare logic crosswalk chains pre/postconditions through the pipeline's composition rules.

**Natural Breadcrumbs.** An interactive site translating ACT papers into runnable Python, framed as "the Rosetta stone, but you can touch it." Part of a larger Runnable Textbooks project. Paper pages are nodes in a graph, not chapters in a sequence.

**Soar cognitive architecture evals.** Work toward measuring architectural improvements to Soar, focused on transfer measurement — whether chunking on one task set speeds up a different task set.

**Blog series arc: functor → monoid → monad.** A cognition/methodology series building toward the point where a system can improve its own improvement process. Functor Wizardry and cons are published installments; the monad post (where the system extracts "what changed" and feeds it forward without human intervention) is the stated endgame.
