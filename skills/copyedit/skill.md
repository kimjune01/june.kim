---
name: copyedit
description: Run humanize → tighten → readability → flavor → codex → sharpen in a loop until convergence. The mechanical pass before line editing.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Glob, Bash, Skill, WebSearch, WebFetch
---

# Copyedit

Humanize → tighten → readability → flavor → codex → sharpen, in a loop. Repeat until a pass finds nothing to fix.

## Process

Each skill step runs as an opus subagent with access to the skill definition and the post. **Apply-first workflow:** commit the file before starting, then apply all fixes directly. Don't present proposals for approval. After each step, report what changed (count + notable edits). The user reviews the result and tells you what to roll back. The commit lets them inspect the before/after diff and revert anything.

1. Read the file. Note the word count. **Commit the current state** so the user has a clean diff baseline.
2. **Humanize.** Launch an opus subagent with the humanize skill definition. Apply all fixes directly. Report count and notable changes.
3. **Tighten.** Launch an opus subagent with the tighten skill definition on the *result of step 2*. Apply all fixes directly. Report count.
4. **Readability.** Launch an opus subagent with the readability skill definition on the *result of step 3*. Apply all fixes directly. This step catches the staccato that tighten creates and adds flow back. Report count.
5. **Em-dash pass.** Run `/em-dash` on the file. Apply all dead-weight verdicts directly. Report count.
6. **Prosody pass.** Launch an opus subagent focused on rhythm: sentence length monotony, stress collisions, weak endings, monotonous sentence starts, run-on mid-register, missing beats, conjunction flow. Apply fixes directly. Report count.
7. **Flavor.** Launch an opus subagent to scan for unlinked pop culture refs, proper nouns, named theories, historical figures. It searches the web and returns proposed links. Apply all links directly.
8. **Codex review.** Send the current state to codex (`/codex`). Apply feedback you agree with directly. Report what you applied and what you skipped (with reasons for skipping). If codex flags low credence on a claim, launch a research subagent to substantiate before dismissing or applying.
9. **Sharpen.** Launch an opus subagent with the sharpen skill definition. Apply lazy-hedge fixes directly. This step especially matters right after codex, because the instinctive way to apply codex's overclaim fixes is to stack qualifiers, and stacked qualifiers turn prose to mush. See [feedback_narrow_and_bold.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_narrow_and_bold.md).
10. **Convergence check.** Launch a humanize subagent on the result. If it finds anything, go back to step 2. If a third round still produces substantive changes, stop and flag for the user. Otherwise, report final word count vs original and stop.

## Rules

- Each skill's full criteria apply. This skill composes them, it doesn't simplify them.
- **Apply everything. Don't ask.** The user sees the diff and rolls back what they don't like. This is faster and puts the judgment where it belongs: on the result, not on proposals.
- Don't over-compress. The "a bit" qualifier on tighten is load-bearing. Two passes to convergence, not ten.
- Don't over-sharpen either. A little hedging in the final draft is fine; sharpen's fixed point is a non-zero hedge floor, not a hedge-free utopia.
- Report what changed at each step, concisely. Don't repeat the full skill output — just the count and notable fixes.
- Code blocks, tables, and front matter are pass-through. Don't touch them.
- Every step in the loop must satisfy the monoidal contract: `step(step(x)) == step(x)` after ~2 passes for arbitrary x. Tighten, humanize, and sharpen all use the same structural mechanism (finite pattern set + non-regenerating rewrites), with tighten adding "a bit" damping on top and sharpen adding a narrow-preserving invariant. Skills that fail this contract create drift operators and should not be added to the loop.
