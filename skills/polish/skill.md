---
name: polish
description: Run the full prose convergence pipeline on a blog post. Composes humanize → codex → tighten → readability → flavor, repeating until no changes. Single invocation, fixed-point output.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Glob, Bash, Agent, Skill, AskUserQuestion
---

# Polish: Prose Convergence Pipeline

Compose the prose skills into a single endofunctor. Run to fixed point.

## Theory

- **Fixed-point convergence**: [Double Loop](/double-loop) — "a bit" dampens each skill to idempotency. Two iterations to convergence. If a third round still changes things, the post has structural issues Polish can't fix.

## Input

A prose file path — blog post, SOAP note section, or any cached document. Polish runs after every skill that writes prose, not just at the end. Each section of the SOAP note gets polished before the next skill reads it.

## Process

For each round:

1. **Humanize.** Scan for AI writing tics, apply subtractions and additions.
2. **Codex review.** Send to GPT-5.4 for structural feedback. Apply improvements.
3. **Tighten.** Compress each paragraph without losing argument.
4. **Readability.** Check prosody, structure, pacing.
5. **Flavor.** Scan for unlinked references, suggest hyperlinks.

After each round, diff the result against the input. If the diff is empty or trivial (whitespace, punctuation only), the pipeline has converged. Stop.

Expected: two rounds to convergence. If a third round still produces substantive changes, flag for human review — the post may have structural issues that the pipeline is oscillating around rather than converging on.

## Output

The post file, edited in place. A summary of changes per round.

## Contract

- **Precondition**: post exists and has been through at least one human editing pass
- **Postcondition**: all five skills report no further changes (fixed point)
- **Idempotency**: running Polish on a converged post produces no changes
- **Failure mode**: if round 3 still produces changes, halt and ask the human
