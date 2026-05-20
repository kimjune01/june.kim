---
variant: post-wide
title: "Asymptote Learning"
tags: coding, cognition, methodology, epistemology
---

*Sequel to [Encoding Expertise](https://june.kim/encoding-expertise) and [Supervisor](https://june.kim/supervisor).*

Two hoists in. [Encoding Expertise](https://june.kim/encoding-expertise) pulled the deterministic strata out of the LLM call and left a thin residual nucleus. [Supervisor](https://june.kim/supervisor) replaced the operator's manual encoding work with an actor one level up, same primitive, automating the encoding loop. What's left is the substrate still suffering each pattern a few times before the encoding lands. Even with the supervisor running hot, the local mistake log is the only feedstock the encoder consumes.

That's the third bottleneck, and the third hoist is to skip it.

## The corpus

Once the ratchet works, the bottleneck is no longer mechanism. It's sample acquisition. The supervisor needs observed mistakes to encode against, and waiting for the operator to suffer each one locally is slow. The good news: GitHub is a public corpus of post-review PR life, refreshed continuously and free to query. Every merged PR is a sample of a successful classification path. Every closed-without-merge is a sample of an unsuccessful one. Every reviewer comment, every CI rerun, every back-and-forth thread is the operator's decision made by somebody else and recorded.

So you feed the supervisor that corpus. The supervisor reads ten thousand merged PRs and notices what their state-transitions look like; it proposes encodings drawn from patterns the public substrate already exhibits. The local idempotence wall filters: proposals must replay cleanly against the substrate's history. Survivors ship. Proposals that contradict local taste are rejected, as if they had been bad encodings of local mistakes. Local context still has the final say (the supervisor's explicit goal disambiguates), but the supervisor needn't wait for the operator to ack ten "shipped-with-caveats" cards before the postcondition lands. The corpus often shows the answer first.

[SWE-bench](https://arxiv.org/abs/2310.06770) (Jimenez et al., ICLR 2024) gave the field the corpus-with-executable-validation idea: GitHub issue/PR pairs as a benchmark where proposed fixes get replayed against the original test suite. [Learning to Commit](https://arxiv.org/abs/2603.26664) (2026) is closer still: chronological splits, attempts on historical issues, oracle-diff comparison, distilled reusable patterns. The idempotence wall here is stricter than either: a proposed encoding must replay correctly against *every* historical operator decision on the local substrate, not just produce a passing test. Strict replay keeps the corpus from imposing public taste on a local context that intentionally diverges.

This is the move. The ratchet has to exist first; without idempotence and clean interfaces, corpus data just produces noise. With it, the substrate skips most of the local suffering: any pattern public history already demonstrates gets encoded from the corpus, not from the operator's last bad day. Local mistakes are reserved for what the corpus is silent on, where local context genuinely matters. Stream a thousand PRs from a comparable public repo through the supervisor on day one before the operator has seen any of them, and encodings the operator would have built over months should land in the shell that afternoon, with the idempotence wall pre-filtering anything that contradicts your local taste.

## The asymptote

Stacking three hoists produces a system that learns from local mistakes, automates the learning, and bootstraps it from public history. The encoded shell at each recursion level bends monotonically toward the shape of the problem; the LLM nucleus at each level shrinks toward what's left.

The asymptote: **the encoded shell *is* the shape of the problem, and the LLM nucleus is exactly the dimension where the problem has no shape.** The mature stack is a problem-shaped shell at each recursion level with a thin LLM at every level filling the holes the shape leaves. [Neuro-symbolic surveys](https://www.ijcai.org/Proceedings/2020/688) argue for hybrid decomposition; continual-learning and tool-use papers argue that adaptation matters; none state this as the asymptotic property that follows once the encoding loop has clean interfaces and enough time. The contribution is to name expert-system construction as an online encoding loop with replay-gated transfer from public decision corpora, and to identify its asymptote.

## Generalization

The construction depends on PRs and GitHub only in the example. Any classification problem with these properties admits the same encoding chain: a clean structured interface in, a finite partition out, an invariant that every event reaches a terminal bucket, two attention channels for misclassification (ambiguous and false-known), and a substrate writeable enough to receive encoding updates at runtime. Given those, the encoding loop drives the system to a *policy fixed-point:* a function from inputs to buckets that the next encoding pass leaves unchanged. The monoidal contract from [Make No Mistakes](https://june.kim/make-no-mistakes) is the formal reason it converges: generalized online learning, where the policy has a fixed point because the substrate that implements it is a monoid under composition. Classification is the cleanest case, but ranking, scheduling, dispatching, routing, and any other partition-valued decision under uncertainty share the same structure.

Which lets us land a definition with no mysticism left in it: **expertise is a complicated policy at its fixed point.** An expert is someone whose encoded shell has converged on the problem they work; the residue they hand to intuition is the part no further encoding could compress. Expertise isn't a substance the expert possesses; it's the trace of the procedure that produced them, terminated. Encoding expertise is that procedure, run on purpose.

## Lineages

Three lineages converged in *Make No Mistakes*; two more join across this trilogy. Toyota's [poka-yoke](https://en.wikipedia.org/wiki/Poka-yoke) is the precondition. OTP's pattern-matched message contract is the postcondition. The monoidal contract of the algebra textbook is the idempotence wall. The human-attention principle is the meter that turns observed mistakes into structural learning. The engineer's [remediation](https://june.kim/remediation) discipline separates "patch and pray" from "build the remedy in." The [actor model](https://en.wikipedia.org/wiki/Actor_model) provides the clean interface for free. The LLM is the new ingredient; the encoding chain is the recipe that lets the new ingredient sit inside the old structure.

Get the unit right, get the interface clean, let the encoding loop run, feed it whatever corpus the world already provides, and on its own the substrate becomes the negative space of the problem.

## The shell is the proof

This is why expert systems stayed popular for forty years after the AI-winter eulogies. They never went away; they got renamed. Every line of every app you use every day is a record of someone, or a group of someones, deciding what the machine should do in some specific scenario, accreted slowly through years of bug reports and feature requests and incident reviews. The Stripe dashboard is the encoded fixed point of "what should an operator be able to do with a payment." The hospital admissions form, the compliance checklist, the CRM workflow, the support macro, the deploy script: each is a complicated policy at the local fixed point its maintainers reached. The encoding loop in this trilogy is the same procedure, automated. The LLM's new role isn't to replace the expert. It's to build the expert system, one classifier at a time, at machine speed.

Step back far enough and the inductive close lands: this is what expertise has always been, in the precise sense the title uses. The trilogy's expertise is the category expert systems encode: systematic rule-application across scenarios that decompose into named cases and named decisions. Each of the following is the kind of judgment that admits expert-system encoding when the inputs are structured, the buckets are finite, and the historical decisions are replayable:

- Customer support triage
- Bug routing and incident severity assignment
- KYC and AML screening
- Insurance claims first-pass
- Medical billing coding
- Legal contract redline
- Content moderation against named policies
- Hospital admission triage
- Loan adjudication
- Helpdesk tier-1
- Peer-review desk screening
- Sales lead qualification

Many still burn an operations team's attention on repetitive routing. Several have public or accessible corpora of prior decisions (closed tickets, regulatory filings, jurisprudence, triage logs) the supervisor can read from. All are the same shape as the PR-routing the operator was doing by hand in the first essay, in a different uniform.

This is the category the trilogy encloses. By contrast, the radiologist's eye, the violinist's hands, the novelist's chapter: those run on substrates the encoding loop does not reach. Humans built the in-category expert systems slowly, one decision at a time, over forty years. The supervisor builds them fast.

And it builds them on a substrate the alternative loop cannot. The same corpus that would feed reinforcement learning or supervised fine-tuning to produce opaque weights feeds the supervisor to produce structural code instead. Same data, different substrate, different artifact:

| | RL / SFT | Supervisor encoding loop |
|---|---|---|
| **Output substrate** | weight matrices | structural code (preconditions, postconditions, CLI dispatches, cache keys) |
| **Interpretability** | post-hoc tooling on opaque weights | architectural, built in |
| **Long tail** | hundreds of examples to weakly learn a rare pattern; never enough data for once-a-year cases | one operator decision asserts a rule the shell honors forever |
| **Operator control** | retrain to change behavior | edit, roll back, adjudicate per artifact |
| **Provenance** | gradient-buried | source, date, validation history on every artifact |
| **Failure mode** | silent miscalibration on the long tail | replay mismatch, visible diff |

No amount of fine-tuning ships a git-blameable artifact. No amount of post-hoc interpretability tooling on RL weights gives the operator what the supervisor gives them by construction: a structural object they can read, edit, roll back, and adjudicate one decision at a time. Where RL gives you a fuzzy policy that mostly works and silently doesn't, the supervisor gives you a structural one that either matches the historical decision log or doesn't, with the diff visible.

Which is as precise as a definition gets. If we can encode the procedure and arrive at an artifact of the same form across that list, we have enclosed the category the list defines: not all expertise, but the kind expert systems were always for. Expertise, in that sense, is no longer a fuzzy folk term; it is named by what builds it. The shell is the proof; it has been the proof all along.
