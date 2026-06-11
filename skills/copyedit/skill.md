---
name: copyedit
description: Run humanize → tighten → readability → flavor → codex → sharpen in a loop until convergence. The mechanical pass before line editing.
argument-hint: <file_path> [--script]
allowed-tools: Read, Edit, Grep, Glob, Bash, Skill, WebSearch, WebFetch, Agent
---

# Copyedit

Two modes, same pipeline (humanize → tighten → readability → flavor → codex → sharpen). The user picks.

| Mode | Invocation | Shape | When |
|------|------------|-------|------|
| **Inline (default)** | `/copyedit <file>` | Orchestrator runs each step itself by launching one subagent per step, applying fixes between steps, and reporting each step's deltas to the user in real time. | The user wants to watch the pipeline and intervene per step. Good for new posts where surprises matter. |
| **Scripted** | `/copyedit <file> --script` | Orchestrator launches one subagent per round that runs all six steps end-to-end and edits in place. Convergence decided by `diff -q` against the round's snapshot. Zero diff = converged. | The user trusts the pipeline and wants the deltas not the play-by-play. Good for late-stage drafts and re-runs. |

Both modes share the same step definitions and the same monoidal contract. Default to inline if the flag is absent.

## Inline mode

1. Read the file. Note word count.
2. **Humanize.** Launch an opus subagent with the humanize skill definition and the post. It returns proposed changes. Apply mechanical fixes directly, flag argument-touching changes for the user. Re-read.
3. **Tighten.** Same shape: subagent with the tighten skill, apply fixes, re-read.
4. **Readability.** Same shape.
5. **Flavor.** Subagent scans for unlinked pop culture refs, proper nouns, named theories, historical figures. Web-search for canonical URLs. Apply links.
6. **Codex review.** Send current state to codex (`codex exec`, default model). If rate-limited, try gemini. If both unavailable, skip with a note. Apply feedback you agree with directly. Bunch ambiguous reservations for the user.
7. **Sharpen.** Subagent with the sharpen skill, apply lazy-hedge fixes directly. Narrow-preserving invariant: rewrites must not widen claims. Especially important right after codex.
8. **Convergence check.** Launch a humanize subagent on the result. If it finds anything substantive, go back to step 2. Hard cap at 5 rounds; if round 5 still produces substantive changes, flag oscillation and stop.
9. **Final report.** Word count delta + step-by-step summary of what changed.

The orchestrator reports each step's deltas to the user as it goes. The user can interject at any step.

## Scripted mode (`--script`)

1. **Set up snapshot dir.** Make a per-run temp dir: `SNAPDIR=$(mktemp -d -t copyedit.XXXXXX)`. Snapshots live in `$SNAPDIR/r{N}.md`, NEVER next to the source file. The source-file directory stays clean (no `.copyedit-r*.md` siblings polluting `_drafts/` or `src/content/blog/`).

2. **Snapshot r0.** Copy the source file to `$SNAPDIR/r0.md`. Note word count.

3. **Launch round-N subagent.** One opus subagent runs the full six-step pipeline end-to-end on the source file, edits in place, and returns. The subagent does not loop and does not decide convergence.

4. **Diff.** Run `diff -q $SNAPDIR/r{N-1}.md <source-file>`. Exit 0 = converged. Exit 1 = the round produced changes.

5. **Snapshot.** If non-zero diff, copy current source file to `$SNAPDIR/r{N}.md`, increment N, go to step 3.

6. **Hard cap at 5 rounds.** If round 5 still produces non-zero diff, flag oscillation and stop. The pipeline is not a fix for structural issues; surface the snapshot dir for the user to inspect.

7. **Final report.** Word count delta from r0 to final. Number of rounds. The `$SNAPDIR` path so the user can diff any pair or delete the dir when they're done. Bunched reservations from each round's codex step.

### Subagent prompt (scripted mode, per round)

Verbatim prompt the orchestrator gives the subagent, with `<FILE_PATH>` filled in:

> Run the copyedit pipeline once on `<FILE_PATH>`. Six steps, serial, edit in place. Do not loop; the orchestrator handles convergence based on diff.
>
> 1. **Humanize.** Apply `/Users/junekim/.claude/skills/humanize/SKILL.md` patterns. Em-dash budget is 0 in prose (reference-list separators OK). Apply all mechanical fixes directly.
> 2. **Tighten.** Apply `/Users/junekim/.claude/skills/tighten/SKILL.md`. "A bit" damping: don't over-compress.
> 3. **Readability.** Apply `/Users/junekim/.claude/skills/readability/SKILL.md`. Prosody, structure, pacing.
> 4. **Flavor.** Apply `/Users/junekim/.claude/skills/flavor/skill.md`. Web-search for canonical URLs and apply hyperlinks inline.
> 5. **Codex review.** Send the current file to codex (`codex exec "..."`, default model). If codex is rate-limited, try gemini (`/Users/junekim/.claude/skills/gemini/skill.md`). If both unavailable, skip and note. Apply feedback directly. Bunch judgment-call reservations.
> 6. **Sharpen.** Apply `/Users/junekim/.claude/skills/sharpen/skill.md`. Narrow-preserving invariant.
>
> Pass-through (don't touch): front matter, code blocks, markdown tables, SVG/img tags, reference lists at the bottom of the post.
>
> Return a terse summary: word count delta, what was substantively changed at each step, any reservations bunched. Do not decide whether to loop.

## Rules (both modes)

- Each step's full skill criteria apply. This pipeline composes them; it does not simplify them.
- Apply fixes directly. Only pause for user approval when a fix touches argument structure or voice.
- Don't over-compress (tighten's "a bit" qualifier is load-bearing). Don't over-sharpen (the fixed point is a non-zero hedge floor). Don't over-casualize: the pipeline's job is legibility, not informality. Never trade a precise term for a friendlier-but-vaguer one; a plain word that loses the technical meaning is worse than the jargon. Clarity means the reader reaches the content, not that the content is softened.
- Code blocks, tables, front matter, SVGs, and reference lists are pass-through.
- Em-dash policy: 0 in prose, reference-list separators OK. Surface revert candidates as a numbered list (bunched, not one-at-a-time).
- Every step satisfies the monoidal contract: `step(step(x)) == step(x)` after ~2 passes. Convergence in 1-2 rounds is normal; 3+ means structural issues.

## Snapshot cleanup (scripted mode)

Snapshots live in a temp dir under `$TMPDIR` (e.g. `/var/folders/.../copyedit.XXXXXX/` on macOS). The OS reaps them eventually. Report the path in the final summary so the user can diff any pair or `rm -rf` the dir when done. Don't write snapshots next to the source file — that pollutes content directories and Astro/Jekyll/etc. content collections.

## Why two modes

Inline lets the user watch the pipeline run, intervening per step when something surprising surfaces. Good for new posts where the deltas are interesting in themselves.

Scripted hides the play-by-play and decides convergence by objective diff. Good for late-stage drafts where the user wants to know "did it change anything, and what" without watching each subagent's report scroll by. The user also gets per-round snapshots as an audit trail; they can diff any pair after the fact to see what each round did.

Both modes share the same step definitions and the same monoidal contract. The difference is who decides convergence: in inline, the orchestrator decides via humanize's introspection after step 7; in scripted, the orchestrator decides by diff against a snapshot.
