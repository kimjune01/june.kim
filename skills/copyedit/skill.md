---
name: copyedit
description: Run humanize → tighten → readability → flavor → codex → sharpen in a loop until convergence. The mechanical pass before line editing.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Glob, Bash, Skill, WebSearch, WebFetch
---

# Copyedit

Humanize → tighten → readability → flavor → codex → sharpen, in a loop. Repeat until a pass finds nothing to fix.

## Process

Each skill step runs as an opus subagent with access to the skill definition and the post. Subagents report proposed changes — they don't edit the file directly. The orchestrator merges results between steps, applying mechanical fixes and flagging judgment calls for the user.

1. Read the file. Note the word count.
2. **Parallel scan: humanize + tighten + readability.** Launch three opus subagents simultaneously, each reading its own skill definition from `/Users/junekim/.claude/skills/{humanize,tighten,readability}/skill.md` and the post. Each returns proposed changes with exact original text, proposed replacement, and rationale. Merge results: apply non-conflicting mechanical fixes, resolve overlaps by preferring the more specific proposal, flag argument-touching changes for the user.
3. **Flavor.** Launch an opus subagent to scan for unlinked pop culture refs, proper nouns, named theories, historical figures. It searches the web and returns proposed links. Apply all links directly.
4. **Codex review.** Send the current state to codex (`/codex`). Apply feedback you agree with directly. Present only the ambiguous or debatable points to the user for judgment. If codex flags low credence on a claim, launch a research subagent to substantiate before dismissing or applying.
5. **Sharpen.** Launch an opus subagent with the sharpen skill definition. It returns proposed hedge compressions. Apply lazy-hedge fixes directly. This step especially matters right after codex, because the instinctive way to apply codex's overclaim fixes is to stack qualifiers, and stacked qualifiers turn prose to mush. See [feedback_narrow_and_bold.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_narrow_and_bold.md).
6. **Convergence check.** Launch a humanize subagent on the result. If it finds anything, go back to step 2. If a third round still produces substantive changes, stop and flag for the user — the post may have structural issues the pipeline is oscillating around. Otherwise, report final word count vs original and stop.

## Rules

- Each skill's full criteria apply. This skill composes them, it doesn't simplify them.
- Apply fixes directly. Only pause for user approval when a fix touches argument structure or voice.
- Don't over-compress. The "a bit" qualifier on tighten is load-bearing. Two passes to convergence, not ten.
- Don't over-sharpen either. A little hedging in the final draft is fine; sharpen's fixed point is a non-zero hedge floor, not a hedge-free utopia.
- Report what changed at each step, concisely. Don't repeat the full skill output — just the count and notable fixes.
- Code blocks, tables, and front matter are pass-through. Don't touch them.
- Every step in the loop must satisfy the monoidal contract: `step(step(x)) == step(x)` after ~2 passes for arbitrary x. Tighten, humanize, and sharpen all use the same structural mechanism (finite pattern set + non-regenerating rewrites), with tighten adding "a bit" damping on top and sharpen adding a narrow-preserving invariant. Skills that fail this contract create drift operators and should not be added to the loop.
