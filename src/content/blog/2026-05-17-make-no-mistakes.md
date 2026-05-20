---
variant: post-wide
title: "Make No Mistakes"
tags: coding, methodology
---

*Sequel to [Skills Lack Determinism](https://june.kim/skills-lack-determinism) and [Don't LLM What You Can Code](https://june.kim/dont-lang-what-you-can-math).*

Agents fuck it up all the time. They:

- hallucinate function names, file paths, and CLI flags that don't exist
- emit structured output that *almost* validates: wrong field, extra key, JSON wrapped in prose, preamble before the payload, apology after it
- write attestations that lie: claim the test ran when it didn't, claim the file was edited when it wasn't
- return confidently wrong answers: fabricated decision, well-formed, no hedge, no signal that the model should have rejected the job
- claim "done" on N items after processing N−2: silent partial completion, no error, no count mismatch
- drift: yesterday's prompt yielded clean output, today's same prompt yields the same shape one time in three, and the dashboard doesn't move because the parser is too kind
- silently truncate: read a 40k-token file into a 32k window, drop the tail, analyze the partial view, return a "complete" answer
- get prompt-injected by retrieved content: an issue body or a file the agent reads contains instructions that overwrite its own
- save artifacts to shitty filenames (`output.txt`, `final-FINAL-v2.json`, the timestamp-no-context special) and drop them in the wrong directory, so the reader gets yesterday's, or none, or six
- spin up scratch workspaces (worktrees, temp dirs, sandboxes) and never clean them up; disk fills, branch lists balloon, the next run inherits state it didn't create
- spawn subprocesses that eat the rate limit silently
- burn the day's token budget on one runaway task because nothing capped the per-job spend
- wedge inside a long call and can't dig themselves out
- take destructive actions on routine-looking prompts: `rm -rf`, force-push, `DROP TABLE`, `git reset --hard`, no confirmation
- race another actor for the same inbox message, both act, downstream sees double
- re-run the same job and create a duplicate PR, a second comment, a third row: no idempotency, no notice of prior state
- read a file, think for a while, write back over edits that happened in between: lost updates from stale-state writes
- lose messages without telling you what happened to them
- leave half-written files and unacked work behind when killed mid-flight

You can't stop them fucking up. The worker is a language model, and the output distribution shifts under cost, prompt drift, and weather.

The field has tried. Most attempts to fix this work on the model, making the agent itself more reliable. Here's the rough inventory of what's been tried and where each falls short:

- **Prompt engineering.** The field's name for "rewrite the prompt until the output looks better." No measurement, no failure model, no controlled variable, no rollback when the new prompt regresses on the cases the old one handled. It is vibes with a `.md` file. The fact that we call it engineering should embarrass us.
- **Ralph loops** (self-review, iterate to convergence). Converge on a self-consistent answer that may be self-consistently wrong. The critic shares the author's blind spots.
- **Multi-agent / blind-merge / debate.** Fan out, take majority or merge dissent. Helps with variance, doesn't help when all agents share a bias (same model family, same training data, same prompt-injection susceptibility).
- **LLM-as-judge.** A separate model scores the output. The judge is gameable, the judge has biases, and the judge's "looks good" correlates with the author's "looks good" more than either correlates with truth.
- **Peer review / adversarial volley across model families** (codex + gemini, GPT + Claude). Genuinely better; catches different errors per family. Still misses what both families miss, and the volley itself is expensive enough to skip under pressure.
- **Constitutional AI / RLHF / self-critique training.** Moves the average. Tail failures persist; the failures you actually need to catch are the ones the training didn't see.
- **Alignment.** The entire research program of teaching the model to want what you want. A multi-billion-dollar bet that the right gradient updates will produce a worker that doesn't need a supervisor. Toyota tried this in the 1970s with "let's just hire workers who never make mistakes." It's why they invented jidoka instead.
- **Retrieval-augmented generation.** Grounds the model in real documents. Fixes hallucinated facts, leaves hallucinated reasoning intact.
- **Structured output / JSON mode / function calling.** Constrains the shape. Catches "almost validates," leaves "well-formed and wrong" untouched. Schema compliance is necessary, not sufficient.
- **Tool-use guardrails / allowlists.** Restrict what the agent can call. Reduces blast radius. Doesn't address why it tried the wrong thing.
- **Test-driven loops** (write test → run → feed failure back). Works where tests are cheap to write and ground truth is well-defined. Most production decisions aren't testable that way.
- **Reflection / "check your work" prompts.** Agents are bad at self-eval; the prompt that produced the error is the same prompt that's now grading it.
- **Reasoning models / extended thinking.** More compute on the inside. Helps reasoning quality, doesn't help the boundary where the answer meets the rest of the system.
- **N-sampling and consensus.** N parallel runs, majority wins. Expensive. Fixes variance, not systematic error.
- **Human in the loop on every action.** Works, doesn't scale, defeats the automation.

Every attempt above tries to make the model output more trustworthy. More training, more critics, more sampling, more reasoning. The implicit theory: an unreliable worker can be made reliable from the inside.

Step back. Are agents different from humans, reliability-wise? Humans hallucinate (we call it misremembering). Humans capitulate under social pressure. Humans skip steps and claim they didn't. Humans write `final-FINAL-v2.docx`. Humans take destructive actions on routine-looking prompts. The error spectrum is shockingly similar; the rates differ on which axis, but neither party is reliable on its own.

So how do we ever have factories that ship near-defect-free products daily? Not by hiring more careful humans. Not by training the workers to want what management wants. By building a *process* (kanban, andon, jidoka, poka-yoke, standardized work, supplier separation) that makes individual unreliability irrelevant at the aggregate. The worker on a Toyota line in 1985 was no more virtuous than one in a 1970 Detroit plant. The output was orders of magnitude better because the process caught what the worker missed.

Whose advice should we take on reliability, then? Code artisans whose method is "be more careful" and vibe coders whose method is "ship it, see what breaks"? Or the lineage that solved this exact problem at scale, in physical reality, with workers who had hands and got tired and made mistakes and were paid not to be replaced by ones who didn't?

You can't make the model trustworthy. You can make its boundary observable. Build a wrapper that makes every fuck-up loud, local, and recoverable. The fuck-ups don't go away; they stop cascading.

This post is nine transplantable patterns for that wrapper. Written first for agents that will drop these into another codebase: each trick is stated as *invariant + mechanism + failure-prevented*, no language, no library. Written second for curious humans: the patterns aren't new, just newly applied. Their lineage is two of the deepest answers anyone has given to *how do you build reliable systems out of unreliable parts*, and they were sitting there waiting for the moment the unreliable part became a language model.

A *skill* is a prompt that shells out to a model. A *skill actor* is the durable worker that wraps one. It owns observability, throttling, rejection routing, and recovery. The skill writes prose. The actor keeps the line running.

The same answer shows up in the most reliable software we have. Ericsson's AXD301 telecom switch hit nine 9s of uptime (about 31 milliseconds of downtime per year) running Erlang/OTP. WhatsApp served 450 million users with around 50 engineers and ran 2 million TCP connections per server on the same stack; that's what Facebook bought in 2014. Discord moves billions of messages a day on Elixir, which is Erlang's runtime with nicer syntax. Klarna, Goldman Sachs's pricing systems, Bet365's live trading: same lineage. None of these are research projects. They are the production systems other production systems envy.

What's under the hood is the actor model: encapsulated processes, message-passing mailboxes, *let it crash*, and supervision trees where the supervisor never does the work it supervises. Joe Armstrong's PhD thesis was titled *[Making reliable distributed systems in the presence of software errors](https://erlang.org/download/armstrong_thesis_2003.pdf).* The premise was that errors are not exceptional; they are continuous, and the architecture must assume them. Same premise as Toyota's. Different industry, same answer.

Two lineages converge here. [Hewitt's actor model](https://en.wikipedia.org/wiki/Actor_model) (1973) and its industrial-strength descendant Erlang/OTP. [Toyota's Production System](https://en.wikipedia.org/wiki/Toyota_Production_System) (1948 onward) and its global descendants. Invented forty years apart by people who never read each other, applied to wildly different substrates (humans on a line, processes on a VM), and they converge on the same primitives:

| Toyota Production System | Actor model / Erlang-OTP | Shared principle |
|---|---|---|
| Kanban pull signal | Message send to mailbox | Demand-driven flow, no upstream push |
| Workstation | Actor / process | Encapsulated state, no shared memory |
| Andon cord | Supervisor-detected crash | Anyone can stop the line; failure is loud |
| Jidoka (autonomation) | "Let it crash" + supervisor restart | Defects halt the unit, not the system |
| Poka-yoke | Pattern-matched message contract | Wrong-shape input can't enter the next stage |
| Genchi genbutsu | Per-process logs, no shared mutable state | Go to the actual site to see ground truth |
| Heijunka (leveling) | Per-actor quota / budget share | Smooth load across roles, no starvation |
| Reject bin (defective vs wrong-part) | `{error, Reason}` tuple | Failures carry their cause forward |
| Standardized work | gen_server / gen_statem behaviours | Common skeleton, local variation |
| Supplier separation | Process isolation | One station's failure doesn't corrupt the next |

Both answer the same question: *how do you build a reliable system out of unreliable parts that must keep working while parts fail?* Skill actors add a third unreliable part, a language model whose output distribution shifts under cost, prompt drift, and weather.

The math textbook is the third witness. A pipeline is a composition of skills; composition is only well-defined when each skill is a [monoid](https://en.wikipedia.org/wiki/Monoid) endomorphism on the shared cache: associative under chaining, with an identity (the no-op skill), and idempotent enough that `skill(skill(x)) == skill(x)` after a small bounded number of passes. Without that fixed-point contract, composition becomes a drift operator: every additional skill in the chain moves the artifact further from where any single skill would have left it, and the pipeline's behavior is no longer a function of its parts. The category-theoretic name is a *reflective subcategory* of converged artifacts; the practical name is *the pipeline doesn't diverge when you add a step.* TPS calls this standardized work. OTP calls it the gen_server contract. Mathematicians wrote it down a century earlier and called it associativity. Three independent derivations of the same primitive.

The nine tricks below are what an actor must provide so the monoidal contract on its skill holds under an unreliable model.

## 1. Artifact-first, stdout-shim-second, heuristic-third

**Invariant:** the skill's decision lives in a written artifact, not in stdout.
**Mechanism:** skill writes a file (attestation, decision JSON, hypothesis graph). Actor reads the file. On missing file, fall back to a cheaper model that extracts the schema from stdout. On that failing, fall back to a regex on the tail.
**Prevents:** model paraphrase, prepended preambles, and cost-driven truncation from being misread as a decision. Artifact existence is binary; stdout always parses into *something*.

## 2. Subprocess blind spots: the PATH shim

**Invariant:** every external API call made by anything the actor spawns is attributed to the actor.
**Mechanism:** prepend a shim directory to the spawned process's `PATH`. Inject the actor's identity into its environment. The shim, named identically to the real tool, records the call against the actor and execs the real binary.
**Prevents:** subprocesses-of-subprocesses (typical when a skill calls another CLI that calls APIs) vanishing from rate-limit accounting. Counts at the receiving dock; the supplier's claim doesn't count.

## 3. Per-actor budget shares via ambient identity

**Invariant:** each actor consumes only its declared share of a shared rate limit.
**Mechanism:** each actor declares a percentage of the global limit. Current actor identity travels through the call stack as an ambient context value (contextvar, AsyncLocalStorage, process dictionary, whatever the runtime offers), not as a threaded argument. The PATH shim from trick 2 and every wrapped client read this ambient.
**Prevents:** whoever-runs-first-eats-most under shared limits. Attribution without plumbing.

## 4. Three-tier jidoka with hysteresis

**Invariant:** the line throttles before it stops, and recovers below where it stopped.
**Mechanism:** three thresholds on a single utilization signal: `throttle` (slow intake), `andon` (pause the line), `recover` (clear the andon). `recover < andon` by a deliberate dead band.
**Prevents:** flapping at the boundary. Without hysteresis, automatic recovery oscillates around the trigger.

## 5. The supervisor paradox

**Invariant:** the loop that can wedge cannot be the loop that unwedges it.
**Mechanism:** the auto-clear runs on an independent daemon. It forces a fresh read of the gating signal, re-evaluates, and clears the andon when the signal allows.
**Prevents:** a worker stuck inside a long call from firing its own recovery. The worker's failure mode is precisely what disables its recovery. First instinct is always to put the recovery check at the top of the same loop. Resist.

## 6. Inbox-boundary pause, not mid-flight kill

**Invariant:** pausing the line stops new pulls; in-flight work completes.
**Mechanism:** the pause check fires *before* the actor pulls the next message from its inbox. Skills that started, finish. New messages stay queued.
**Prevents:** half-written artifacts, unacked messages, ambiguous external state. Stop issuing kanban cards; don't shoot the operator mid-motion. Pause is not kill.

## 7. Rejection as a third outcome

**Invariant:** `decided | errored | rejected` are distinct. None coerces into another.
**Mechanism:** a skill returns one of three. `rejected` carries a `reject_reason` ("wrong-shape input," "missing context," "out of scope"). Rejections route to a separate inbox for human review; they are neither acked-and-forgotten nor counted against error budgets.
**Prevents:** rejected jobs poisoning either the decision stats (counted as "no") or the alerting (counted as errors). Defective-part bin and wrong-part bin sit on different shelves for a reason.

## 8. Interface accounting: every drop has a reason

**Invariant:** for every interface boundary, `in == out + screened + pending`. Leak is the gap; target is zero.
**Mechanism:** instrument each boundary with five counters: `in`, `out`, `screened` (filtered with a recorded reason), `pending` (still in an inbox), `leak` (the residual). Alert on nonzero leak.
**Prevents:** silent message loss. Slow processing is not loss. Reasoned filtering is not loss. Unexplained disappearance is, and an unexplained gap is the only alert worth firing on the funnel.

## 9. Compliance counters that close the shim loop

**Invariant:** the inspection step does not silence upstream pressure.
**Mechanism:** the shim from trick 1 emits three counters per skill: `clean_fast` (parsed without help), `normalized` (shim had to extract), `fallback` (heuristic kicked in). Surface them as percentages with sample size on the same dashboard as the skill's other metrics.
**Prevents:** the shim hiding skill drift. Without the counters, normalized output masks producer-side regressions; with them, growing `normalized` flags drift and growing `fallback` flags shim failure. The shim hides the bug; the counters surface the hiding. Both are necessary.

---

Stack the nine and you have a skill actor: a durable worker that observes its own boundary, throttles before it stops, recovers from outside itself, distinguishes rejected from errored, accounts for every message, and surfaces its own drift. That object is the prerequisite. The actor side underwrites the monoidal contract on the skill side: artifact-first (1) is what makes a skill's output replayable, rejection-as-third-outcome (7) is what keeps the identity element pure, interface accounting (8) is what makes associativity checkable. Without the actor, the contract is a wish. With it, the contract is enforced.

Once the unit holds, composition follows. Two skill actors chained share a mailbox; their joint behavior is a skill actor. The fixed-point property carries through composition because each component had it. Pipelines are monoids of skill actors. Larger systems are monoids of pipelines. The whole stack is associative all the way up, which is why you can rearrange stages without rewriting the runtime, and why the same supervisor tree works at every scale.

And here is the prestige. The list of things people ship as their next AI-in-production initiative (observability, cost attribution, rate-limit governance, drift detection, audit trails, replayability, blast-radius containment, graceful degradation, backpressure, idempotency, fault isolation, recovery without lost work) is already present in the composed object. Not as add-ons. As consequences of the contract. The artifact-first invariant is the audit trail. The PATH shim is cost attribution. Budget shares are rate-limit governance. Three-tier jidoka is backpressure and graceful degradation. The supervisor paradox is fault isolation. Inbox-boundary pause is recovery without lost work. Rejection-as-third-outcome is drift detection at the input. Interface accounting is observability. Compliance counters are drift detection at the output. Every item on the production wishlist is already paid for at the unit; composition inherits them all because monoids preserve their generators' properties.

You don't bolt production-readiness onto a pipeline of skill actors. You get it the moment the unit is correct. That is the difference between an engineering primitive and a feature checklist, and it's why three lineages that never spoke converged on the same one.

The composition doesn't stop there. The monoidal contract is scale-free: a skill actor is a monoid, a pipeline of skill actors is a monoid, a fleet of pipelines is a monoid, an organization of fleets is a monoid. The same associativity, the same identity, the same fixed-point under repeated application, at every level. There is no scale at which the primitive stops working and a new architecture has to take over. Toyota proves this in physical reality: one workstation, one cell, one line, one plant, one global production system, all running the same kanban-andon-jidoka discipline that holds on a single station. OTP proves it in software: one process, one supervision tree, one node, one cluster, all running the same let-it-crash discipline. The skill actor inherits the same property because the contract is the same. Whatever you compose, you can compose again. The ceiling is set by the substrate, not the primitive.

Nothing here is invented. The Toyota Production System, Erlang/OTP, and basic algebra each derived the same primitive from a different starting point, separated by decades and disciplines, and they agree because the problem is the same: build a reliable composition out of unreliable parts. The worker now happens to talk. That's the only update. Take their advice over vibes. Get the unit right and the pipeline falls out.
