---
variant: post
title: "Avionics-Grade Software on a Chat App Budget"
tags: coding, methodology
---

I built a chat feature last week using four AI agents in parallel. Two models, two scopes, blind to each other. Then I merged the best parts and sent a third model to find bugs. It found 27 across 10 rounds. Every one was real.

I didn't plan to rediscover avionics engineering. I was just trying to ship agent participation for [Hangout](https://github.com/kimjune01/hangout) — letting users bring AI agents into ephemeral chat rooms. The spec had a clean server/client split, so I ran two agents per side: Claude and GPT-5.4, same spec, separate directories. Compare, pick the better design per component, merge.

This is called N-version programming. Airbus has been doing it since the A320. Their flight control computers run software written by separate teams, in different languages, from the same spec. If the computers disagree, the system votes.

I didn't know that when I started. I just wanted two opinions.

## The merge caught structural bugs

Claude's server-side implementation used a wildcard PubSub subscription (`"channel:*"`) that Phoenix PubSub doesn't support. It silently received nothing. The tests passed because they never exercised the cleanup path. GPT-5.4's version subscribed per-room, correctly.

GPT-5.4's implementation serialized token creation through a GenServer, preventing a time-of-check-to-time-of-use race on the one-agent-per-nick constraint. Claude wrote directly to ETS — fast, but two concurrent requests could both pass the uniqueness check.

Claude nested the SSE context event under a `"contract"` key, cleanly separating machine-readable constraints from LLM instructions. GPT-5.4 put everything flat. I took Claude's structure.

The merge wasn't "pick a winner." It was component-level synthesis: GPT-5.4's token module, Claude's API design, GPT-5.4's mention detection, both test suites combined.

## Both agents made the same mistake

Both client-side implementations independently added a `function_exported?` guard around `ChannelServer.agent_message/3` — a runtime check for whether the server-side function existed yet. Same defensive instinct, same wrong answer. The function exists. It will always exist. They both hedged because they each only saw half the spec.

In 1986, Knight and Leveson ran the definitive experiment on N-version programming. Twenty-seven teams independently implemented the same missile defense spec. Over a million test cases, they found that 50% of faults were correlated across versions. The root cause wasn't that the teams were similar. It was that the specification was ambiguous. Different teams hit the same ambiguity and made the same wrong assumption.

The `function_exported?` bug is Knight and Leveson's finding in miniature. The spec said "Agent B should assume Agent A's API exists." Both agents read that and thought: but what if it doesn't? The spec was clear; the agents' training data taught them to be defensive anyway. Same training data, same mistake. Common mode failure.

The fix wasn't better agents. It was a tighter spec. And the catch came not from the blind-blind comparison (which only compared within scope), but from the merge step, which had context across both scopes.

## The bug hunt didn't converge for nine rounds

After the merge, I sent GPT-5.4 on a bug hunt: read the spec, read the code, find everything wrong. It found seven bugs. I fixed them and sent it again. Five more. Fixed, re-sent. Two more. Then four. Then three. Then two, two, two, one, zero.

Twenty-seven bugs total. The trend wasn't monotonic — round 4 spiked because round 3's fixes introduced new surface area. Every fix is a new place to have bugs. The hunt had to chase its own tail before the fixes stopped generating new issues.

The bugs got progressively subtler. Round 1 found a return type mismatch that crashed the UI. Round 6 found concurrent ETS races exploitable only by parallel requests. Round 9 found that dedup and rate-limit tables leaked memory after token revocation because cleanup only touched the main token table.

All tests passed from the start. The test suite caught nothing the bug hunt found.

## This is IV&V

NASA's Independent Verification & Validation facility in Fairmont, West Virginia reviews all Class A and B mission software. The reviewing team is technically, managerially, and financially independent from the developers. They get the same requirements and perform their own analysis.

My bug hunt is the same pattern. The reviewing model is technically independent (different architecture, different training). It sees the same spec. It has no organizational bias toward the implementation — no sunk cost, no schedule pressure, no ego.

Traditional IV&V does one pass. I ran ten. Not because I planned to, but because it kept finding things. The stopping criterion isn't a number of passes. It's empirical: zero new findings. A fixed point.

## The economics changed

DO-178C is the FAA's standard for airborne software. At the highest level (DAL A, for catastrophic failure), verification consumes 50–75% of total effort. Productivity drops to 3–12 lines of code per day. Cost: $25–100 per line.

Normal software skips all of this because the economics don't justify it. Nobody runs MC/DC coverage analysis on a chat app. Nobody maintains bidirectional requirements traceability matrices. Nobody hires a separate team to independently verify a feature that lets users paste URLs into rooms.

But the reason those practices are expensive is that they require human reviewers, human test designers, human traceability maintainers. Agents aren't humans. They don't get bored on round 9. They don't wave through a bug because it's 4pm on Friday. They don't have organizational loyalty to the codebase.

The practices that transfer best are the ones that were always mechanically sound but economically prohibitive:

- **N-version programming** at build time, not runtime. Merge the best parts instead of voting. Discard the losing implementation.
- **IV&V to convergence.** Not one pass — iterate until zero new findings.
- **Common mode failure analysis.** Explicitly hunt for assumptions that both the spec and implementation share. That's where Knight and Leveson's correlated failures live.
- **MC/DC test generation.** Every boolean condition shown to independently affect the outcome. An agent can parse every decision, generate the n+1 test cases, and run them. DAL-A coverage for minutes of compute.

## What I actually did

I wrote a spec for 40 minutes. That was the real work — the Attend. Then I said "go" and made five decisions over two hours: choose the process, choose the models, fix or defer each bug class, push for zero, deploy.

The agents did everything else. Four implementations, two comparisons, one merge, ten rounds of review, twenty-seven bug fixes, compiled, tested, deployed. The 40 minutes of spec writing prevented more bugs than any of it — Knight and Leveson's finding again. Specification quality drives outcome quality. The agents are as good as the spec you give them.

The method is old. The economics are new. And the economics change what's worth doing.
