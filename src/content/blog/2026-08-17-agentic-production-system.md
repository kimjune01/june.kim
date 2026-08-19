---
variant: post-medium
title: "Agentic Production System"
tags: coding, methodology
image: "/assets/sweep-cockpit.png"
---

Add another component, and quality rises while cost explodes. Remove one, and cost falls while defects escape. This is the production problem with agents: the model is stochastic, tools fail, APIs return stale state, tests can pass without running, and a human cannot watch every transition. Redundancy's only move is to multiply the same unreliable parts.

I met this problem while building [Sweep](https://github.com/kimjune01/sweep), an autonomous pipeline for contributing fixes to open-source projects. It finds maintainer-acknowledged bugs, investigates them, writes a failing test and minimal fix, runs adversarial review, verifies the result, and submits a pull request at a pace the maintainer can absorb. It grew in three stages: first PRs ([Speedrunning Open Source](/speedrunning-open-source)), then a loop that makes the PRs ([Sweep & Triage](/sweep-and-triage)), then a factory that runs many loops in the shape of a graph. This post is about the factory, and the abstraction it stands on: unreliable agents producing reliable output.

Every station was fallible. A reviewer could approve its own mistake. GitHub could return yesterday's state. A workflow engine could reliably retry an operation that should never have happened.

The standard production advice arrives as a checklist: add evals for quality, guardrails for security, tracing for observability, human approval for consequential actions, and cheaper models or caches for cost. Agent guidance and surveys keep converging on those categories ([LangChain](https://www.langchain.com/state-of-agent-engineering), [OWASP](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [NIST](https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai)). Sweep eventually used every one of them.

The checklist does not say how they compose. An eval can certify the wrong behavior. A guardrail can stop one destructive command while upstream agents flood the queue. A trace can preserve everything and teach nothing. Human approval can turn automation into a faster way to generate inspection work. A cheaper model can produce waste at a lower unit price. Each control improves a component while leaving the production system undesigned.

The missing questions are operational: who authorizes work to enter the line, how far a defect can travel, which evidence must survive each handoff. A list of controls does not supply the relations among them.

These are production questions, not new properties of language models. The Toyota Production System has spent more than half a century integrating their answers through trial, failure, and daily refinement. Agent engineering is beginning to rebuild the same ideas under names like orchestration, guardrails, observability, and human-in-the-loop. We should not reinvent a production system one component at a time.

For a while, the most reliable output was the bill.

## The bill

Sweep used different models in three roles. Cheap models handled frequent classification and test scaffolding. Stronger models investigated bugs and reviewed decisions. Independent models checked one another at handoffs. The arrangement looked like ordinary model routing: spend more where judgment is hard, less where a small model suffices.

The API had already shut itself off twice for running out of credits. Then I counted the receipts: eight in twenty-four hours, ninety dollars each, every one titled “Auto-recharge credits.” Agent subprocesses were charging API credits instead of using the authenticated subscription. Routing them correctly stopped the cash bleed ([incident and fix](https://github.com/kimjune01/sweep/commit/881930d0fea63efece7bf8c7a0ea25ddbc4ef9d4)).

That changed who charged me; it did not reduce how much work the system performed.

The pipeline was still asking GitHub the same questions repeatedly and refreshing slow-moving state on every display read. It polled every open pull request to find the few that changed, and upstream agents created work without regard for the downstream queue. A cheaper redundant call is still redundant. A cached bad decision is still bad. Moving inference onto a subscription converts marginal cost into a capacity ceiling; it does not remove waste.

The problem was not the price of intelligence. It was overproduction.

## An agentic production system

The answer came from the Toyota Production System. TPS begins from the same joint objective: high quality, low cost, short lead time. Its two pillars are *jidoka* and *Just-in-Time*. Jidoka stops when an abnormality appears, so defects do not continue downstream; Just-in-Time makes only what is needed, when it is needed, in the amount needed. Toyota describes both as methods for eliminating waste rather than trading quality against efficiency ([Toyota](https://global.toyota/en/company/vision-and-philosophy/production-system/)). Applied to LLM work, TPS becomes an *agentic production system*: agents perform the work, deterministic controls bound it, observability exposes the process, and a human process engineer continuously improves the line.

Jidoka began with [Sakichi Toyoda's loom](https://www.toyota-industries.com/company/history/toyoda_sakichi/), which stopped itself when a thread broke. Automation no longer required a person to stare at the machine, and the loom no longer produced defective cloth. Just-in-Time made the next process withdraw only what it needed from the previous one, with kanban carrying the authorization to produce its replacement. Toyota took the idea from the supermarket, where a sold item creates the replenishment signal ([Toyota virtual plant](https://global.toyota/en/company/plant-tours/production-system/)).

Sweep is the same system under stochastic labor. Its stations are agents, APIs, test environments, classifiers, and maintainers; the part they pass along is an issue becoming an investigation, a patch, and finally a pull request. None can be trusted alone, so the line must expose abnormalities, limit inventory, preserve evidence, and make the next station authorize the previous one's work.

The human is the process engineer. Each intervention should make a class of failure cheaper, more visible, or impossible on the next run. It should ratchet the line rather than rescue one item.

Quality belongs to the customer, not the station that produced the work. Each station must satisfy the next process, ending with the external customer: a maintainer deciding whether the patch is worth accepting. An agent's confidence, a reviewer's approval, a passing internal metric, and even a merge are evidence about quality, not its definition.

But quality improves only when the work is inspectable. The process engineer must be able to move from an outcome back through the process that produced it, inspect the actual evidence, and change the standard.

TPS divides the problem:

| TPS principle | Question for an agentic production system |
|---|---|
| Just-in-Time and pull | Should this work exist yet? |
| Jidoka and poka-yoke | How far can a defect travel? |
| Standardized work | What contract does this station currently follow? |
| Visual management | Where are quality and cost escaping now? |
| Genchi genbutsu | What does the evidence at the producing station show? |
| Kaizen | How does this incident permanently improve the next run? |

This is not a metaphor laid over the code afterward. The repository's operating nouns are `kanban`, `andon`, `waste`, `WIP`, `pull`, `retro`, `actor`, and `station` ([README](https://github.com/kimjune01/sweep#architecture)). The git history records the system acquiring them as each new kind of waste appeared.

## Pull

A push system tells every available agent to stay busy. Search finds a hundred issues, triage fills a queue, investigators produce patches, and submission becomes somebody else's congestion problem. Parallelism looks like throughput until the last finite resource appears.

For Sweep, that resource was maintainer attention. Fourteen pull requests in forty-eight hours produced one merge and escalating warnings. Technically strong patches were still inventory when the maintainer could not absorb them ([case study](/sweep-and-triage#case-study-tinygrad)).

That made an open PR into inventory, not output. I capped publication at one PR per organization. The drip station could publish another only when the downstream organization had capacity, and upstream search ran only when its consuming queues had room ([implementation](https://github.com/kimjune01/sweep/commit/bf696e046bfefa0d0c63c260302aef71989e76d9)).

That is pull production: downstream activity signals what upstream may produce ([Lean Enterprise Institute](https://www.lean.org/lexicon-terms/pull-production/)). A kanban is authorization to produce or move one item; without the signal, nothing moves ([Lean Enterprise Institute](https://www.lean.org/lexicon-terms/kanban/)). Sweep's typed actor message is that signal.

![The line as a graph: parts flow downstream toward the maintainer while kanban authorization flows upstream, with loops for reinvestigation and maintainer concerns](/assets/sweep-pull-pipeline.svg)

The limit also makes failure legible. When twenty agents share a large queue, a blocked item disappears into averages. With one-piece flow, the item that does not move is the problem in front of you.

## Jidoka

An agent can report success with complete confidence. Sweep once shipped a test that never executed because the local environment silently skipped it. The production side saw “0 tests failed” and called the run a pass. CI later failed, and the maintainer found the defect.

The response was not a stronger instruction to check carefully. I added a deterministic verifier that rejects a run unless the expected test executed and passed. The model may still write `pass`; the parser overrides it. No valid attestation, no push ([gate and incident](https://github.com/kimjune01/sweep/commit/1f071d98381ed47b0b0d4dc6ede146c980ede440)).

Every activity applies the same pattern: assert the postcondition, halt the producing actor on failure, display the andon, and do not resume until the cause is repaired ([implementation](https://github.com/kimjune01/sweep#andon-postcondition-failures-halt-the-line)).

Toyota calls this jidoka: detect an abnormality, stop immediately, prevent more defective output, and free the person from watching the machine. The andon tells the person where intervention is needed ([Toyota](https://global.toyota/en/company/vision-and-philosophy/production-system/#jidoka)). Sweep's corresponding rule is:

> Pulling the cord is just a test that runs in production.

TPS is testing in production, and the payoff is learning rate rather than latency. Every halt is a sample from the real distribution, and retro turns the sample into a countermeasure. When real consequences are too expensive to learn from, the same line can run on an evals set that outputs to nowhere. Every gate, receipt, and halt still exercises, and nothing ships. That is the checklist's eval, composed: synthetic demand for the whole line, a dojo that bootstraps the controls until failures are affordable in production.

The human role changes: a process engineer does not approve every tool call or watch an agent reason. They specify the boundary condition, inspect the evidence when it breaks, find the producing process, and encode the countermeasure.

## Receipts

Independent model review appears to solve unreliable judgment: ask Codex, ask Gemini, accept only agreement. But the producing agent can claim it called either reviewer, summarize the response incorrectly, or reuse a verdict after the code changes.

Sweep therefore separates a verdict from its evidence. Review artifacts are captured, hashed, and pinned to the code they examined; the publication gate verifies the receipt rather than trusting the producing agent's report ([receipts and attestations](https://github.com/kimjune01/sweep#receipts-and-attestations)).

A receipt cannot make the reviewer correct; it makes the contribution attributable, immutable, and independently inspectable. That gives the process engineer a path back to the work itself: what the reviewer saw, what it said, and which code the judgment covered. Reliability moves from the component to the relation between claim, artifact, and gate.

The same rule determines when not to use a model at all, because a decidable question does not need judgment. A behavioral claim about a patch may require an adversarial reviewer. Whether a named test ran is a parsing problem. Replacing the latter with another LLM adds variance and cost without adding judgment. This is poka-yoke: mistake-proof the decidable boundary, and reserve models for classifications whose uncertainty is irreducible.

## Waste attribution

Once the line ran unattended, “API usage” was too coarse a metric. Calls outside the central wrapper were invisible, so the aggregate could say the system was healthy while one actor exhausted the shared allowance.

I tagged every GitHub call with its actor and assigned each actor a budget share; an actor that crosses its limit pulls its own andon. Attribution exposed repeated work the aggregate concealed ([accounting and cache policy](https://github.com/kimjune01/sweep/commit/28412afd97a10a16aba30b363209b00516128d4e)). GitHub's own limits made the resource finite ([GitHub](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)).

The budget then gained jidoka: throttle before exhaustion, halt on projected overrun, resume only after returning to a safe range ([control policy](https://github.com/kimjune01/sweep/commit/dc9941a5ac02327e479d58516f8965fdd11fed0e)). The question changed from “How many requests remain?” to “Which station produced the waste, and why was it allowed to continue?”

Caching followed the same principle. Reads share observations with freshness matched to the decision; writes never enter the cache ([cache design](https://github.com/kimjune01/sweep/commit/8f92652ca07576499fda676fd594559d4d709262)).

The largest latency win came from refusing fresh work on a read path. A display that performed network refreshes took 84 seconds; reading maintained state reduced it to 0.15 seconds ([measurement and fix](https://github.com/kimjune01/sweep/commit/0182289517fb1b6de0fff0422db2d13bd3fe9581)). Event-driven classification later replaced repeated full scans ([pipeline](https://github.com/kimjune01/sweep#pipeline)).

A software engineer would file these under caching policy, refresh strategy, retry limits, and backpressure. [Ohno's waste categories](https://www.lean.org/lexicon-terms/seven-wastes/) name them more precisely:

- A re-fetched observation is overprocessing.
- Eager refresh is overproduction.
- An unbounded retry is defective inventory recirculating.
- An unbounded queue is work made before the next station requested it.
- A dashboard that performs production work is a machine activated by inspection.
- A shared budget without station attribution hides the source of waste.

Cost is the accumulated waste of the flow that called the model.

## Observability

A trace earns its cost when repeated failures can be attributed to the station that produces them. Sweep records events and per-actor counters; its cockpit shows pressure, and workflow history opens the evidence behind it. Observability is the process engineer's instrument panel ([observability](https://github.com/kimjune01/sweep#observability--events-counters-cursor)).

![The cockpit: each station's queue, in-flight work, production rate, trend, and oldest waiting item](/assets/sweep-cockpit.png)

*Genchi genbutsu* has to work at different strata of detail. “Go and see” cannot mean standing beside an LLM, and it cannot stop at a dashboard assembled from its own summaries. The digital gemba must preserve a route from the condition of the whole line to the actual object that produced the signal:

| Stratum | What the process engineer sees | Question |
|---|---|---|
| Line | Flow, WIP, cost, lead time, outcomes | Where is the abnormality? |
| Station | Actor budget, queue, retries, halts, verdict distribution | Which process produced it? |
| Item | Issue, prompt, tool calls, diff, test output, review artifact, receipt | What actually happened? |

Visual management starts the investigation at the cheapest level. A line-level signal points to a station; the station points to an item; the item carries enough provenance to reproduce the judgment. Toyota uses genchi genbutsu for the same reason: improvement depends on learning and problem-solving at the site rather than decisions from detached reports ([Toyota](https://global.toyota/en/detail/11234406/)).

This stratification reconciles scale with inspection. Recording every token without a line-level view produces an archive nobody reads. Reporting only aggregate success rates hides the defects needed for kaizen. Sweep keeps both the compression and the path back down. Inspectability improves quality because every abnormal outcome can become a process experiment instead of an anecdote.

## Kaizen

The line is not yet its own process engineer.

A supervisor agent can enforce a control plan once the quality characteristic, limit, and response are specified. It can count API calls, stop an actor at its budget, verify that a test name appeared, and route a failed gate. It is not yet reliable enough to decide what output quality means, whether the metric still represents it, or which process experiment would improve it without moving the defect somewhere less visible.

Sweep learned this boundary repeatedly. “Zero tests failed” was a valid measurement of the wrong event. Merge rate measured acceptance, and it is queryable to the digit: since April, [93 of 212 decided pull requests](https://github.com/search?q=author%3Akimjune01+-user%3Akimjune01+is%3Apr+created%3A%3E%3D2026-04-01&type=pullrequests) merged. But it confounded patch quality with maintainer attention, contributor standing, repository policy, and submission pace. The subscription move reduced cash expense while resource consumption continued. Optimizing any one of those numbers makes its dashboard greener while making the production system worse.

TPS requires judgment after metric collection: is this one bad item, or did the process produce it? Statistical process control gives that judgment a vocabulary, distinguishing isolated special causes from common causes built into the process ([ASQ](https://asq.org/quality-resources/control-chart), [NIST](https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc12.htm)). Experimental design sharpens the next step by varying process factors deliberately and specifying the response before the result arrives ([NIST](https://itl.nist.gov/div898/handbook/pri/section1/pri11.htm)). These are instruments inside the process engineer's work, not alternative production systems.

TPS assigns this work to human wisdom. Toyota's own account is explicit: machines can detect abnormalities and execute the current standard, but they cannot implement their own kaizen. People first understand the work, remove waste, define the abnormal condition, and build that judgment into the machine ([Toyota](https://global.toyota/en/company/vision-and-philosophy/production-system/#jidoka)). The current agent supervisor belongs on the machine side of that boundary.

The human process engineer therefore owns four judgments:

1. **Quality:** choose an output measure tied to the customer rather than an internal proxy.
2. **Diagnosis:** decide whether a failure is an incident or evidence about the process.
3. **Experiment:** change a controlled factor, preserve comparison, and specify in advance what result would warrant adoption.
4. **Ratchet:** encode a successful countermeasure as a gate, budget, route, cache policy, or standard for future runs.

Agents can gather evidence, propose hypotheses, implement variants, and replay the measurement. They cannot yet be the final judge of an experiment whose output they produced and whose quality function they selected. Letting them judge collapses production, inspection, and process engineering into the same unreliable component.

Sweep enforces the split in code. The attestation writer records what ran and cannot import the verifier, because a producer that just spent minutes capturing a test run converges on “looks good to me”; pride is the failure mode ([producer/judge split](https://github.com/kimjune01/sweep/commit/c56991fff6538a81d8c51b613036bbc5e88f07fa)). The supervisor's improvement loop is propose-only: it clusters recurring patterns, replays each proposal against the labeled decision history with the agent blinded from the recorded action, and stages the survivors as cards for me ([propose-only supervisor](https://github.com/kimjune01/sweep/commit/083a3b6adae7a9e5a2442c70630a78fda732af11)).

`retro` reads that evidence and turns failures into prescriptions, one [A3-shaped page](https://www.lean.org/lexicon-terms/a3-report/) per incident: problem, cause, countermeasure. A prescription may change code, a skill, a cache policy, a gate, a budget, or a routing rule. The commit is the durable learning; the retro file is only its staging area. Clearing an andon without changing its producing condition restores flow but improves nothing. The completed loop is:

> observe the line → locate the producing process → encode a countermeasure → measure the next run

This is how quality ratchets. A silent test skip became a deterministic gate. Invisible traffic became per-actor accounting. Repeated polling became event-driven classification. Each incident survives as a constraint on future behavior, so the system does not depend on the human remembering the lesson.

But retros can overproduce too. If agents generate lessons faster than the process engineer can consolidate them, the improvement queue becomes a graveyard. I capped pending retros at two; a third halts the forward pass until I attend to one. The line's production rate is bounded by its learning rate ([retro pager](https://github.com/kimjune01/sweep#retro-pager--soap-one-pagers-the-backward-pass)).

This is standardized work without freezing the standard. Lean standardized work defines the current sequence, pace, and minimum in-process inventory, then makes that baseline the object of kaizen ([Lean Enterprise Institute](https://www.lean.org/lexicon-terms/standardized-work/)). Sweep's skills and typed activities are the current standard. Events expose deviations. Retro proposes a countermeasure. Git history records which countermeasures survived.

The repository therefore tells a different story from a static architecture diagram. Its history moves from timers to demand pull, verbal verdicts to hashed receipts, model judgment to deterministic gates, and human surveillance to process engineering. TPS is not the layout of Sweep. It is the update rule by which Sweep became itself.

## Line reliability

No component became reliable alone.

The model still confabulates. A test can still be wrong. A reviewer can still miss a defect. A cache can still be stale. A workflow can still retry. A human can still clear the wrong alarm. Sweep does not solve these by stacking enough fallible judges to reach certainty.

It decides what each failure is allowed to cost.

A bad hypothesis may consume one investigation slot, not the whole queue. A failed postcondition stops one station before the defect travels. A stale observation may render a dashboard approximate, but a publication gate refreshes the state it depends on. A reviewer verdict cannot detach from the artifact and commits it examined. A runaway actor consumes its declared share before it pulls its own andon. A lesson cannot pile up beyond the process engineer's capacity to incorporate it. A maintainer receives one pull request, not everything the agents could produce.

In steady state, the line halts several times an hour, and each halt resolves within minutes. TPS treats the opposite condition as its own abnormality: *no problem is problem*. A quiet andon means defects are traveling. An abnormality caught at its producing station costs minutes; a defect that reaches the maintainer costs standing.

Toyota describes the purpose of its two pillars as delivering quickly, at low cost, and with high quality, all at once ([Toyota](https://global.toyota/en/company/vision-and-philosophy/production-system/)). The apparent tradeoff dissolves because defects and cost share a cause: uncontrolled production.

When every component is unreliable alone, do not ask which one to trust.

Instrument the line. Find where it fails. Change the process so it cannot fail the same way at the same cost twice.
