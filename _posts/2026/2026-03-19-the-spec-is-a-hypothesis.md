---
layout: post
title: "The Spec Is a Hypothesis"
tags: cognition coding
---

*Part of the [cognition](/cognition) series. Builds on [Vibelogging](/vibelogging) and [Zero Comments](/zero-comments).*

[Vibelogging](/vibelogging) claimed that prose is source code. [Zero Comments](/zero-comments) said "code is disposable. The prose is what accumulates." Both were right for greenfield, where I owned the entire design. Both were wrong when I tried contributing to someone else's codebase. The implementation corrected the spec, not the other way around.

## The pipeline

I wrote a [prose spec](https://github.com/kimjune01/union-find-compaction-for-gemini-cli/blob/main/transformation-design.md) for union-find context compaction in [Gemini CLI](https://github.com/google-gemini/gemini-cli). Three stages:

1. **Extract**: Read the existing `chatCompressionService.ts` (476 lines of TypeScript). Translate its behavior into prose.
2. **Design**: Write a transformation spec. Architecture, data flow, file structure.
3. **Implement**: Hand the spec to an LLM.

The LLM produced a working implementation. All tests passed. Then a [code review](/proof-of-trust) found ten bugs.

## What the code taught the spec

The spec described `resolveDirty()` as a straightforward loop: summarize each dirty cluster, clear the list. The implementation discovered that `union()` can run between awaits, replacing the dirty inputs array mid-flight. The fix: a reference-equality check (`_dirtyInputs.get(root) === inputs`) that discards stale summaries when the array identity changes. No prose description of "batch-summarize dirty clusters" would have surfaced this.

The spec said `render()` uses the embedder to match queries. The implementation revealed that `embed()` mutates the TF-IDF vocabulary, so searching contaminates the corpus. The fix: a separate `embedQuery()` that reads the vocabulary without writing to it. The spec had no reason to distinguish read-path from write-path embedding because that distinction only exists at the type level.

Ten bugs total. Twenty spec revisions to absorb what the fixes taught. The spec did its job: architecture, data flow, file structure. But it couldn't carry type contracts, concurrency guards, or API surface constraints. Those emerged at implementation and flowed *back* into the spec.

## Three translations, compounding loss

The extraction step was the most lossy. Going from working TypeScript with types, error handling, and API contracts to prose is decompilation. You can't round-trip it. Information that lives in the type system has no equivalent in prose.

The design step was less lossy. It was original thinking, not translation. The architecture, the overlap window, the deferred summarization: these originated in prose and survived intact through implementation.

The implementation step was where the accumulated loss surfaced. Every bug lived at a boundary the extraction had dropped: a type signature, a concurrency constraint, an invariant the existing code enforced implicitly.

Vibelogging worked for the [vector-space ad exchange](https://github.com/kimjune01/vectorspace-adserver) because it was greenfield. There was no existing code to extract from, no type contracts to relay, no API surface to match. The spec *was* the system because there was nothing before it.

Contributing to Gemini CLI was different. The existing code carried constraints the prose pipeline couldn't relay. The extraction step tried to make prose do relay work, and that's where the pipeline broke.

It gets worse. After shipping, I ran the same code review on the *existing* flat compression path — the code my spec had extracted from. [Four bugs](https://github.com/google-gemini/gemini-cli/issues/22942). The token accounting compares against the wrong model's context limit. The split point uses `JSON.stringify` length instead of token count. Tool-response truncation silently drops structured fields. Repeated compression leaks temp files without cleanup. Users were already [reporting symptoms](https://github.com/google-gemini/gemini-cli/issues/15225): compression that barely reduces size, context still full after `/compress`, invalid argument errors at 113% capacity. The [maintainers knew](https://github.com/google-gemini/gemini-cli/issues/21890) about the token accounting gap.

The prose spec faithfully captured broken behavior. I never reviewed the extraction source. The hypothesis was built on unverified premises.

## The industry says spec → code

[Spec-driven development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) is the industry's name for this workflow. [GitHub's Spec Kit](https://github.com/github/spec-kit), [Martin Fowler's taxonomy](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), the whole ecosystem: specification is the source of truth, code is the derived output. [Drew Breunig](https://www.dbreunig.com/2026/03/04/the-spec-driven-development-triangle.html) gets closer with his "SDD triangle" where spec, code, and tests form a network rather than a pipeline.

What I experienced was stronger than staying in sync. The implementation *taught* the spec things it didn't know. The code review found constraints the spec couldn't have expressed. The spec got rewritten to absorb new information that only existed in the implementation. Spec → code is the obvious direction. Code → spec is where the learning happens.

## The boundary

Prose carries architecture. Code carries constraints. In practice, the boundary falls near the function signature. It's a useful boundary, not a clean partition.

Above it: what to build, where, why. Prose is the right medium. It's denser than code for intent, readable by both humans and agents, and survives framework changes.

Below it: type contracts, concurrency invariants, API surface, edge cases in vector math. Code is the right medium. It has compilers, type checkers, and tests. Prose has readers.

The ten bugs lived below the line. The spec correctly stopped above it. The code review caught what belonged in code.

## What I do differently now

On greenfield, the workflow hasn't changed. Prose spec, LLM implementation, ship.

On inherited systems, I stop treating prose as a relay format for existing code. The extraction step is where the loss compounds. Instead: read the existing code directly, spec only the new architecture in prose, and keep the types, tests, and API contracts in code from the start. Let the LLM read both the prose spec and the existing source. Two inputs, not a lossy pipeline.

## The correction

[Vibelogging](/vibelogging) said "the writing is the durable artifact. The code never was." That's true when the spec originates the design. It's wrong when the code carries constraints the spec must absorb.

[Zero Comments](/zero-comments) said "code is disposable." Code is disposable *after* the spec absorbs what it taught. During development, it's load-bearing. You don't throw away experiments just because you've published the paper. You throw away experiments that have already been absorbed into the next version of the theory.

The double loop isn't prose → code. It's prose ↔ code. The spec is a hypothesis. The implementation is the experiment. The code review is peer review. And the spec gets revised, like any hypothesis that survives contact with evidence.

---

*Written via the [double loop](/double-loop). Full receipts in the [work log](https://github.com/kimjune01/union-find-compaction-for-gemini-cli/blob/main/WORK_LOG.md).*
