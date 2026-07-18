---
variant: post-medium
title: "Auditing MirrorCode"
subtitle: "A carefully built benchmark that measures scoped reimplementation and partial recall, sold as autonomous whole-program creation. Pros, cons, and a receipt for every claim."
tags: methodology, epistemology
---

[MirrorCode](https://arxiv.org/abs/2606.30182) (Epoch AI and METR) hands an AI an execute-only binary plus its docs and asks it to rebuild the whole program, graded byte-exact against the reference. The headline: *"the largest software project AI can complete on its own."* I ran it through the [how-to-audit checklist](/how-to-audit-a-benchmark). Every claim below links to a receipt in the [audit repo](https://github.com/kimjune01/mirrorcode-audit), which is re-runnable end to end.

**Verdict in one line:** a well-built instrument that measures scoped *reimplementation from a working oracle*, partly via *recall* of these specific public programs, and is marketed as autonomous *creation*. The engineering is good. The claim on the number is not.

*Disclosure: I applied for a role at Epoch AI, which co-produced MirrorCode. This audit uses only public artifacts and is re-runnable; every claim below traces to a cited receipt, so it stands or falls independent of me. My own [check 4](/how-to-audit-a-benchmark) says a producer's relationships are a conflict when the artifact is asked to be science, and that rule applies to the auditor too.*

## At a glance

| Pro | Con |
|---|---|
| Cheat-proofing is *enforced*, not asserted | The title measures a different thing than the metric |
| I/O-only grading dodges the frame problem | "A human would take weeks/months" is unmeasured belief |
| Ran a human baseline and a contamination screen | 17 of 25 targets are screen-positive for memorization |
| Selection drained the recall surface (2 vs 21) | 2 targets are recall by construction |
| Not saturated; real headroom left | The receipts that would settle it weren't shipped |
| The paper body is candid about limits | "Entire program" flattens heterogeneous units |

## Pros: what it gets right

An audit that only dunks is a press release. MirrorCode is better-built than most, on several axes better than the [six benchmarks](/how-to-audit-a-benchmark) I audited before it. [Full credit, sourced →](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/04_what_it_gets_right.md)

- **Cheat-proofing is real.** Four isolated containers, scoring where the agent can't reach it, and an execute-only reference [enforced with seccomp-BPF + Landlock + `RLIMIT_CORE=0`](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/04_what_it_gets_right.md) that blocks every byte-read path to the binary. ProgramBench only *assumed* execute-only; MirrorCode closes the holes, and its scoring isolation defeated a live Gemini binary-wrap cheat.
- **I/O-only grading sidesteps the frame sin.** The oracle is `(stdout, stderr, exit)`, not final environment state, so the destructive-completion trap that [sank Terminal-Bench](/terminal-bench-frame) can't arise.
- **It did the two things most benchmarks skip:** [a human baseline and a memorization screen](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/04_what_it_gets_right.md). Both incomplete, both commendable to attempt.
- **Its selection drained the recall surface.** A [complete per-target read](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/06_per_target.md) finds **2 recall targets out of 25**, against ProgramBench's [21 of 201](/programbench-measures-recall). No hash, image, or media target survives. That is a real result of careful selection.
- **Not saturated.** 8 of 25 targets were never solved to 100% and the large ones sit near zero, so the instrument still discriminates at the frontier.
- **The paper body is honest.** It concedes the code is piecemeal, "would not be merged," and that the results don't show AI can do arbitrary implementation work. The overreach is in the title, not the methods section.

## Cons: where the claim outruns the metric

- **Construct validity: the title measures a different thing.** MirrorCode sells autonomous whole-program builds; the metric scores *reimplementation from a live reference oracle*. The number is precise about something narrower than the title names. [The gap, laid out →](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/00_construct_validity.md)
- **The human-labor claim is belief, not measurement.** Every "a human would take weeks/months" is *"we believe,"* from four contributors with a sevenfold spread and no completed baseline. The targets are open-source programs, so their [git histories anchor the real labor](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/01_human_labor.md): creation runs to tens of developer-weeks, while MirrorCode's own baseline puts *reimplementation* at days. The marketing evokes the first and measures the second.
- **Two targets are recall by construction** (below), so a pass means recalling a spec, not reconstructing it. [Witnesses →](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md)
- **Two-thirds of targets are contaminated, and the recall share is unquantifiable.** MirrorCode's own screen flags [17 of 25 targets as screen-positive](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/03_how_much_is_recall.md) for memorization. Whether recall inflates the 56% headline cannot be computed from released data, because the join that would show it was never published.
- **The receipts that would settle it weren't shipped.** The per-task, per-model outcome grid *is* a figure in the paper, so [publishing it as data would cost almost nothing](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md), yet the run records aren't public. It's a choice, not a budget.
- **"Entire program" flattens heterogeneous units.** `cal` and `uuidparse` are tiny tools inside util-linux; `bib2json` is one format pair of pandoc. [Each scope is legitimate, but the aggregate phrase hides how different the tested surfaces are.](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/00_construct_validity.md)

## The two recall witnesses

These are the whole recall count, and each carries a re-fetchable receipt. [Per-target audit →](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/06_per_target.md)

- **`brotlid`** decodes a bundled Brotli stream to exact bytes. That needs the RFC-7932 decoder and its ~120 KB static dictionary, neither in the docs nor derivable from the visible examples. MirrorCode defends it as "fully determined by the documented format," which [conflates the RFC with the bundled docs](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md).
- **`mailauth arc-seal`** must emit an exact RSA-SHA256 signature. Reproducing those bytes requires RSA, SHA-256, and the ARC canonicalization rules from the spec. [Receipt →](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md)

## What would fix it

MirrorCode's question is three: how large a program, how much faster than a human, and how reliably. Collapsing them into "56%" is the problem. The [constructive fix](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/05_recommendation.md) is a preregistered **size × time-to-success × whole-task-success profile**: whole-task success and time-to-success plotted against program size, failures censored rather than dropped, contamination split out, uncertainty shown so a pretty curve can't fake precision. Wall-clock is the capability axis, not dollars, since a model's compute is negligible against a human SWE's time. The audit couldn't compute it because the run records aren't public, so the finding is a request: run it.

## Per-target, all 25

The [complete read](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/06_per_target.md) gives every target a verdict and sweeps the [full rejection taxonomy](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/06_per_target.md) from the prior audits (recall, implementation-pinned render, undiscoverable entry point, self-capturing golden, scale, the non-determinism family). What fires: **2 recall, 7 scale/complex, 13 clean, 3 private unread.** Everything else is absent or neutralized by the non-determinism screen and the selection away from reverse-engineering targets. The one whole-benchmark caveat: every gold output is the reference's own I/O, a self-capturing oracle with no independent contract check.

## The fine print

The [audit](https://github.com/kimjune01/mirrorcode-audit) is one-sided by design: a witness proves a defect; "no witness found" is not a clearance. Every quantitative claim traces to a cited paper section, a public repo file, or a re-runnable script; per-cell figure reads are labeled as such. The recall column is verified from the graded I/O; the memorization and solve columns are figure reads, exact only in aggregate. Corrections are welcome, and re-derivable against the receipts. MirrorCode is a good instrument for a real capability. It measures a narrower thing than its title, in the direction that makes the headline more impressive.
