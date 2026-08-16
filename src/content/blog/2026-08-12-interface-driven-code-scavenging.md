---
variant: post-medium
title: "Interface-Driven Code Scavenging"
tags: coding, methodology
image: "/assets/scavenging-five-gates.png"
---

*Part of the [methodology](/methodology) series. Applies [New Reading](/new-reading) to source code and runs [Verifiable Knowledge](/verifiable-knowledge) as a design protocol.*

I was preparing for a system design interview about a campaign-based notification service. The expected move was boxes and arrows: campaign service, scheduler, queue, workers, ledger, analytics. I kept wondering why I should invent the boxes before checking whether somebody had already built the system.

They had. GitHub held several working implementations, complete with the parts the interview prompt left out. The first step in system design used to be drawing the system. Now it can be searching for one.

This is an old practice with new economics. It has been called *code scavenging*, *copy-based reuse*, *copy-paste-modify*, and [*clone-and-own*](https://gsd.uwaterloo.ca/sites/default/files/2013-csmr-cloning.pdf). Programmers did it before package managers existed.

The formal literature mostly treated it as undisciplined reuse because the expensive part began after the copy. Someone had to understand foreign code, cut it out of its environment, replace its assumptions, test the transplant, and maintain the detached result. Importing a package kept that work upstream.

## Why now

GitHub made implementations searchable. It did not make them absorbable.

A repository match was never a component waiting to be picked up. A single behavior can run through an API handler, three tables, two background jobs, a migration, and a retry state machine. Finding the repository was cheap. Discovering and moving that path was not, so package managers won by preserving the upstream boundary.

Frontier coding agents collapse the costs after discovery. An agent can trace a feature across files, identify its dependency closure, write characterization tests, translate its storage layer, and fit it behind a local interface. None of those operations is new. Carrying the whole sequence through verification at software speed is.

The same capability invites an objection. An agent that can trace and transplant a foreign system can also generate a fresh one, and its priors already describe how familiar systems fail. Priors do help; they let an agent recognize the retry loop, idempotency record, or escape hatch that a clean design would dismiss as clutter.

But a prior samples the space of plausible failures. Working code records the realized ones: which inputs actually arrived, which race actually fired, which external service actually lied. That distribution depends on facts outside the code; it cannot be derived at write time, only encountered. Generation produces hypotheses about failure. Surviving code is evidence of it.

## Scars are evidence

Mature code contains *scar tissue*. Its awkward branches often record incidents that no design document predicted. Its guards encode inputs that once caused damage. Its operational hooks exist because somebody once lacked them at 3 a.m.

The scar documents its own failure mode: a guard beside its commit message, linked incident, and regression test explains what it protects against. A generated guard, even an identical one, arrives without that record, and nobody can tell whether it is necessary or cargo-culted without recreating the incident. Same code, different epistemic status. A clean-sheet implementation acquires this knowledge by reenacting the problem's history: invent, fail, patch, converge on patterns already present elsewhere. When the license permits copying, scavenging transfers part of that learning without the original pain.

Coding agents make producing another implementation cheap; they do not make deployed software cheap, so engineering effort belongs downstream of generation. Verification, integration, observability, and maintenance remain. Reinvention spends the new abundance on generating code, keeps those downstream costs, and risks the same old failures. Scavenging spends it on finding, adapting, and testing an implementation that has already survived some of them.

This is the threshold. Faster generation alone would only accelerate the old boxes-and-arrows process. Cheap comprehension and transformation make a different process viable for non-novel systems. Repositories become a searchable implementation space, and architecture becomes the diff between the desired interface and the closest working system.

## Search implementations before architectures

A system interface partitions the search space better than a box diagram does. By interface I mean the observable contract: inputs, outputs, invariants, forbidden outcomes, and the round trips that must complete. It describes required behavior without prejudging the decomposition. Search each resource and round trip in the interface, then look for a system where they already meet.

For the campaign system, my first search found [Dittofeed](https://github.com/dittofeed/dittofeed). Its repository contains broadcasts, segments, journeys, delivery events, FCM support, Kafka, ClickHouse, Temporal workers, a dashboard, and deployment manifests. [Laudspeaker](https://github.com/laudspeaker/laudspeaker) supplies another implementation of journeys, preferences, send limits, segmentation, and analytics. Neither proves a billion notifications a day; both answer hundreds of design questions that a clean sheet leaves invisible.

The schema tells you what the UI forgot to ask. The worker tells you which states fail halfway through. The migration history tells you which early abstractions broke. The tests tell you what maintainers considered stable. Existing code is an executable archive of design pressure.

That evidence changes the architect's job. Instead of proposing components, the architect finds the system that has already discovered most of them and marks where the requirements force a departure. Architecture begins with a diff.

## Copy the behavior, not the repository

Forking preserves an upstream relationship. A dependency preserves it more tightly. Clone-and-own ends it deliberately.

The unit of reuse is the smallest coherent implementation of a behavior. A scheduler without its idempotency record is not coherent. A delivery worker without its retry classification is not coherent. A campaign table without the transitions that govern it is only a shape. Copy until the behavior closes, then stop.

The receiving system supplies the boundary, and [characterization tests](https://en.wikipedia.org/wiki/Characterization_test) preserve it through the move. An agent can follow the behavior through callers, migrations, and background jobs before cutting. The transplant becomes a graph cut rather than a paste.

Not every scar crosses the cut. The discriminator is whose reality the scar recorded. Guards on shared external surfaces transfer: the push provider that rotates tokens, the timezone rules, the malformed human input. Guards on the donor's private infrastructure answer incidents the receiving system will never have; their cause stayed behind.

Keep the scars whose cause you share. The rest is the machinery a transplant can safely shed.

![The transplant as a graph cut. Inside a donor repository, a dashed cut encloses the coherent behavior: API handler, campaign tables with their state transitions, scheduler with its idempotency record, delivery worker with its retry classes. Scars from shared surfaces, timezone rules and token rotation, cross with the unit; the donor's dashboard and Kafka config stay outside, their scars' causes left behind. Characterization tests carry the unit across the interface into the receiving repository as the largest proven unit that fits.](/assets/scavenging-graph-cut-light.svg)

## Own means own

Clone-and-own trades upstream coordination for local responsibility. Security fixes will not arrive through a version bump. The copied code will not gain new features unless the local team writes them. Upstream scars stop arriving too: incidents the source project will discover next year no longer patch the copy. The recorded source revision keeps observation cheap, though. When the copied behavior touches an evolving external surface, the team can diff upstream and import the scars it would otherwise relearn. Those losses are hidden debt only when the decision is implicit. Made explicit, they are the price of removing upgrade churn, transitive dependencies, architectural coupling, and somebody else's roadmap.

The trade works when the imported behavior is bounded and its failures can be reconstructed. It fails when the code depends on a fast-moving protocol, embeds a security primitive, or carries more machinery than the organization can diagnose and recover. TLS belongs in a dependency. A campaign state machine may not.

License compatibility is another selection constraint. Permissive licenses such as MIT, BSD, and Apache usually fit proprietary absorption when their notices remain. GPL and AGPL may not, and a public repository with no license grants no general permission to copy.

## The pointer replaces the mental model

The usual objection to copied code arrives at 3 a.m. Someone has to understand the system when it breaks. That argument treats a developer's mental model as the only route from failure to recovery.

[New Reading](/new-reading) made the same move for literature: the agent holds the proof; the human holds the pointer. Source code admits the same access pattern. The maintainer does not need to cache the whole system in advance. They need to know where the evidence lives and how to ask for the relevant path.

Prior comprehension is not even the most reliable route. Reading code reveals paths an execution *could* take. Logs and traces record the path it *did* take. A developer may understand every service and still fail to explain an incident when the triggering input, configuration version, queue attempt, or state transition was never recorded. Familiarity decays as code and deployment state change.

A copied system can substitute externalized evidence for prior comprehension. Its boundary carries correlation IDs, structured state transitions, deployed revisions, retry histories, and the inputs needed to replay a failure. Metrics expose pressure before failure. Rollback and fallback contain the damage. An agentic loop can trigger on the local failure, reconstruct the causal path from those records, inspect only the code on that path, patch it, and verify the repair against the replay.

The code can remain opaque. The diagnostic membrane cannot.

## Five operating regimes

The method is not one standard for every environment. Call the environment an operating regime: it fixes the assurance a copied system must buy and the loss it buys that assurance against. Five recur:

- A prototype copies the closest behavioral fit and proves the main round trip. Its assurance comes from cheap reversal because learning matters more than uptime.
- An ordinary production service preserves the largest unit that fits and carries recorded production evidence. Observability, traceability, replay, fallback, and agentic repair substitute for a team carrying the implementation in its head.
- A latency-sensitive service declares what may degrade. Netflix can [return an imperfect recommendation](https://netflixtechblog.com/fault-tolerance-in-a-high-volume-distributed-system-91ab4faae74a) or lower video quality before it interrupts playback. The copied system is judged on the same utility function.
- A system courting irreversible loss is designed from the worst case: follow the path to the loss it cannot undo. Where failure can be contained and replayed, deferred comprehension still works. Where it cannot, prior verification returns.
- A medical device cannot assume that diagnosis will beat harm. Hazard analysis, traceable requirements, controlled changes, and verification remain necessary because the patient cannot be rolled back.

The governing test is whether the recovery horizon is shorter than the harm horizon. When it is, observability and agentic repair can replace comprehension in advance. When it is not, understanding and verification must arrive before deployment.

## The scavenging loop

The loop begins with an interface and a target repository. The interface can be types, an API specification, tests, or precise prose. It needs one end-to-end round trip and the invariants that make a superficially working implementation wrong. The repository supplies the language, framework, infrastructure, and local conventions. An organizational policy can narrow the acceptable licenses.

When the user arrives without an interface, the agent elicits it before searching. The agent asks for five concrete examples: a valid request, its observable result, a forbidden result, the expected scale, and the most important round trip. It turns each answer into a proposed interface clause or acceptance test and returns the contract for correction.

Elicitation ends once the contract can distinguish a satisfactory implementation from an impressive but irrelevant one. It does not need to specify the architecture. Search will discover that.

Low-risk facts never become questions. The agent reads the repository to discover its stack and offers defaults where the user has no preference. For proprietary work, the search defaults to permissive licenses. A consequential product choice still returns to the user. The division keeps elicitation short without letting the agent silently invent the target.

### Wide first, then deep

The search runs from systems to components to snippets. Nouns and verbs from the interface supply the first queries. The round trip supplies the better ones. Product-category names widen the vocabulary: “customer engagement platform” finds implementations that “notification scheduler” misses.

The first pass produces repositories, not conclusions. The second pass verifies the license at the relevant directory, finds the files and migrations behind each required behavior, and traces the storage and runtime assumptions. Repository activity and tests show maintenance; replayable benchmarks and independently cross-checked deployment records show operational evidence. Examples, abandoned demos, unlicensed code, and features locked behind unavailable enterprise directories fall away.

The surviving candidates fit in a small table. Each row names the exact revision and the license. It then records the behaviors already present, the code that implements them, the assumptions they carry, the code still missing, and the maintenance and production evidence the second pass found. Every claim links to the check that earned it. That table is the first human gate, and the design document later carries it into *Candidates* unchanged.

A user can reject a candidate for a constraint the interface failed to express. Otherwise the search proceeds without asking permission at every query.

### The selection function

The winner has the lowest adaptation and ownership cost: the least new code to pass the interface tests, the smallest dependency closure to carry, a compatible license, and a unit the receiving system can diagnose and recover. Stars can break a tie. They cannot establish fit.

One source supplies one whole behavior. A scheduler from one system, a state machine from another, and a ledger from a third create seams that no source has tested. A second source earns entry only where the interface already exposes a clean boundary.

Selection produces a feature-to-file map before it produces code. The map says which source files, migrations, tests, and state transitions implement each interface behavior, where the source does not fit, and which characterization tests a later transplant must pass. The agent now knows what would move and the user knows what the design proposes to adopt.

### The design document

The durable output is one citation-rich design document built from testable claims. The candidate table and feature-to-file map feed it, and a transplant that follows discharges its claims. Unlike an agent transcript, the document stays in the repository and can explain the system after the search context disappears.

Its order follows the evidence:

1. *Interface*: inputs, outputs, invariants, round trips, and forbidden outcomes
2. *Operating regime*: the tolerated failures and the assurance they require
3. *Candidates*: the surviving-candidates table, carried forward unchanged
4. *Interface validation*: the tests or traces showing what each candidate satisfies
5. *Mismatch*: requirements no searched implementation satisfies
6. *Adoption boundary*: the paths selected for copying, retained machinery, and planned adaptations at the edges
7. *Diagnostic membrane*: the logs, traces, metrics, replay, fallback, and agentic repair hooks the plan specifies
8. *Provenance*: notices, source revisions, and the import the transplant would make
9. *Novel design*: only the residual mismatch that survived the search

The document is complete before code moves: every claim carries a check, either already run against a candidate's own repository or planned against the target. A proposed component cannot enter *Novel design* until candidate evaluation shows why existing code cannot satisfy its interface at acceptable adaptation cost. Boxes and arrows can summarize the selected system, but they follow the source evidence.

### The entitlement ledger

The design document is an entitlement ledger, not an agent's attestation that research happened. Each material claim carries four fields:

- *Claim*: “Dittofeed schedules a broadcast without duplicate delivery.”
- *Roots*: the exact source revision, files, migration, fixture, and runtime needed to check it
- *Check*: the test or command another agent can replay
- *Kill condition*: the output that would refute the claim

Every claim follows the same literal template, so another agent can generate and parse them without guessing the shape:

```markdown
- *Claim*: <what the system does, stated as a checkable fact>
- *Roots*: <source revision, files, migrations, fixtures, runtime needed to check it>
- *Check*: <test or command another agent can replay>
- *Kill condition*: <output that would refute the claim>
```

Citations attach where the claims occur. A code claim points to an immutable revision and the exact file or line that supports it. A license claim points to the governing license at that revision. A scale or production claim points to the benchmark, deployment record, or independent report rather than a project homepage. Search-result pages and repository descriptions can discover evidence; they cannot serve as the evidence.

Checks are equally local. The command, fixture, expected output, and execution environment sit beside the claim or in a versioned test the claim names. Another agent must be able to start from the document, run the check without recovering the original conversation, and reach the same verdict.

A replay gives the claim one of three states. Passing claims stand. Failed claims are false and identify the mismatch. Claims with no runnable check remain untrue, however plausible they sound. “Battle-tested” stays untrue until a benchmark, deployment record, or independent source pins down what workload survived. Where direct replay cannot reach an empirical root, an independent cross-check takes its place.

This standard propagates into the final design. “Candidate A lacks frequency capping” needs a repository search or failing acceptance test another agent can repeat. “The copied scheduler handles our load” needs the load-test command, environment, revision, and result. “We must invent this component” stands only after every viable candidate has a recorded failing check against the same interface.

The document survives more than the session. Another agent can re-run its checks, overturn a selection when a root changes, and follow the failed edge into every downstream decision that depended on it. Provenance says where the design came from. Replay says whether it is still entitled.

### Approval

The first complete document is a draft, not authorization to copy. The agent presents its interface, candidate selection, unresolved claims, adoption boundary, and novel residue for review. Human feedback changes the document, changed claims receive new checks, and the cycle repeats. An unresolved claim stays untrue; approval records acceptance of that uncertainty rather than laundering it into fact.

The design phase ends only when the user explicitly approves a named revision of the document. That approved revision becomes the contract for a downstream transplant. Until then, the target repository remains unchanged.

### The transplant

Transplant is optional and downstream. It begins from the approved design revision; a team can stop at the document or proceed when it wants the behavior running.

The source implementation becomes an oracle. The agent runs one complete path through its API, persistence, workers, and output, then captures the behavior in characterization tests. When the source cannot run locally, its tests seed the characterization suite and its call graph exposes the stateful edges. Code whose effects cannot be traced through the target interface does not cross the boundary.

Those tests define the unit of reuse. The agent follows calls inward to the implementation and outward to each assumption required for correctness. Migrations and state transitions cross when the behavior depends on them. Retry classes, idempotency records, and fixtures do too.

The transplant preserves the largest proven unit that fits behind the interface, then removes only what creates demonstrated cost, starting with the scars whose cause stayed behind. Unused machinery is cheaper than breaking the integration evidence that made the source worth copying.

The behavior stays fixed while the edges adapt to the receiving repository. Characterization tests land first. The extracted implementation follows, then local refactors. The repository's own tests and type checks confirm the transplant landed and discharge the *Adoption boundary* and *Diagnostic membrane* claims the document planned.

The import occupies one commit. Its description names the approved design revision, the source repository, and the exact source revision. It also names the copied paths, the applicable license, the retained notices, and the adaptations made during import. Required notices stay with the code. Later changes receive later commits, so the boundary between borrowed history and local history remains inspectable. That discharges *Provenance* from a plan to a record.

### When it breaks

The method has hard stop conditions. The absence of a compatible license ends the search. So does the absence of an implementation covering the core round trip, or a dependency closure too large for the receiving team to own. Cryptography, authentication, and similar security primitives remain dependencies unless independent maintenance offers stronger evidence than upstream maintenance.

A different framework is not a stop condition. Neither is an untidy architecture or a pile of mechanical adaptation. Those are the costs coding agents collapse.

### Five design gates

1. *Intent* (gate: does the elicited interface match the actual need?)
2. *Search* (gate: does the candidate table contain the right implementation?)
3. *Map* (gate: is the selected behavior a coherent, observable ownership boundary?)
4. *Review* (gate: are its claims checkable and its unresolved claims explicit?)
5. *Approval* (gate: does the user authorize this revision as the transplant contract?)

![The scavenging loop as a zigzag between an agent lane and a human lane. Agent work fills the valleys: eliciting the interface, wide-then-deep search producing the candidate table, selection and the feature-to-file map, the design document with its checks, and the feedback loop with re-checked claims. Five gates sit on the human lane: Intent, Search, Map, Review, Approval. After gate five the path exits to an optional transplant, one import commit.](/assets/scavenging-five-gates-light.svg)

Everything between gates is agent work. Human attention stays on intent, selection, ownership, and acceptance.

*Intent* fixes *Interface* and *Operating regime*. *Search* fills *Candidates* and *Interface validation*. *Map* resolves *Mismatch* and plans the *Adoption boundary* and *Diagnostic membrane*. *Review* challenges the ledger and its *Novel design*. *Approval* pins the revision that transplantation may execute.

## Search first

Scale claims come last. If the target says one billion notifications a day, first make one notification complete the round trip from campaign to receipt to dashboard. Then load-test the copied path and replace only the boundary that fails. An unproven scale requirement does not justify discarding every design decision that production code already paid to discover.

I ran an informal version of this loop while building [Caret](https://github.com/kimjune01/caret-recorder), a background screen recorder. Its gapless segment rotation, loopback audio capture, and dock-hiding flags came from GitHub implementations of similar apps. The decisions table in its README is the scar record the method predicts: each row names a failure somebody else had already paid for, down to a dependency that exists only because Chromium writes WebM without duration metadata. The repository lacks the protocol's other half. It has no candidate table, no check beside each claim, and no record of which implementations the patterns crossed from. That last loss is Klint's lost-provenance problem. The import commit exists to prevent it.

[Code scavenging](https://homepages.cwi.nl/~paulk/publications/IFIP98.html/node10.html) was described in 1998 as frequent, underdocumented, and unsupported. A recent study calls the same behavior [copy-based reuse](https://arxiv.org/abs/2409.04830) and finds it common across open-source development. The practice never disappeared. Package ecosystems only made another kind of reuse cheaper for a while.

Copy > invent. Search first, and make invention prove that no working implementation will do.

## Lineage

- Paul Klint, [“Code scavenging”](https://homepages.cwi.nl/~paulk/publications/IFIP98.html/node10.html) (1998). Names the practice: search existing programs for comparable functionality, edit it, and reuse it instead of starting from scratch. It also identifies the lost-provenance problem that the design document and import commit repair.
- Otávio A. L. Lemos et al., [“A Test-Driven Approach to Code Search and Its Application to the Reuse of Auxiliary Functionality”](https://www.sciencedirect.com/science/article/pii/S0950584910002107) (2011). Uses tests as both the search interface and the suitability check. Interface-driven scavenging extends that move from small utility functions to whole system behaviors.
- Matias Martinez, Westley Weimer, and Martin Monperrus, [“Do the Fix Ingredients Already Exist?”](https://arxiv.org/abs/1403.6322) (2014). Measures the redundancy assumption behind automated program repair: many real commits are composed entirely of code that already exists elsewhere. Scavenging bets the same redundancy holds at system scale.
- Mike Fullerton, [“Search for existing solutions before building”](https://agenticdevelopercookbook.com/guidelines/planning/code-quality/reuse-before-build), *The Agentic Developer Cookbook* (2026). States the contemporary agent rule without the cost inversion, provenance ledger, operating regimes, or design-document protocol developed here.
