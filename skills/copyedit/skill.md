---
name: copyedit
description: Run humanize → tighten → readability → flavor → codex in a loop until convergence. The mechanical pass before line editing.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Glob, Bash, Skill, WebSearch, WebFetch
---

# Copyedit

Humanize → tighten → readability → flavor → codex review, in a loop. Repeat until a pass finds nothing to fix.

## Process

1. Read the file. Note the word count.
2. **Humanize.** Scan for AI patterns (em dashes, negative parallelisms, restated points, rule of three, filler, throat-clearing). Apply all clear Filter-level fixes directly. Flag anything that touches argument structure for the user.
3. **Tighten.** Compress every paragraph a bit. Cut dead weight, redundant modifiers, nominalizations, throat-clearing. Then re-read for choppy runs and restore flow with conjunctions where natural. Target 10-20% compression on prose paragraphs over 30 words.
4. **Readability.** Check prosody, section titles, paragraph sizing, section sizing, bold/italic. Apply fixes liberally, especially prosody.
5. **Flavor.** Scan for unlinked pop culture refs, proper nouns, named theories, historical figures. Research links with WebSearch. Apply all links directly.
6. **Codex review.** Send the current state to codex (`/codex`). Apply feedback you agree with directly. Present only the ambiguous or debatable points to the user for judgment. If codex flags low credence on a claim, research it before dismissing or applying.
7. **Convergence check.** Re-read the result. Run humanize scan again. If it finds anything, go back to step 2. If a third round still produces substantive changes, stop and flag for the user — the post may have structural issues the pipeline is oscillating around. Otherwise, report final word count vs original and stop.

## Rules

- Each skill's full criteria apply. This skill composes them, it doesn't simplify them.
- Apply fixes directly. Only pause for user approval when a fix touches argument structure or voice.
- Don't over-compress. The "a bit" qualifier on tighten is load-bearing. Two passes to convergence, not ten.
- Report what changed at each step, concisely. Don't repeat the full skill output — just the count and notable fixes.
- Code blocks, tables, and front matter are pass-through. Don't touch them.
