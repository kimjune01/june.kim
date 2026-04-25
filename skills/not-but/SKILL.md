---
name: not-but
description: Find and remove "not X but Y" / "isn't X; it's Y" / "X — not Y" constructions. Deterministic grep for detection (no LLM blind spot), the not-but subagent for triage, apply edits for dead-weight cases, flag earned ones.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Bash, Agent
---

# Not-but: Negative-Parallelism Hunter

LLMs have a structural blind spot for their own patterns. "Not X but Y" is the most common AI tic and the slipperiest one — pattern-matching by another LLM misses it as often as the original write did. This skill uses **deterministic grep for detection** (no blind spot) and an LLM only for **triage** (where judgment is needed).

Sister skill to `/humanize`. Where humanize scans broadly across many patterns, this drills on the one pattern that slips past humanize most often.

## Process

1. Read the file at the given path. Note the word count.

2. **Detect (deterministic).** Run grep with these patterns. Each captures a distinct shape of negation. Run them all; collect every hit with line number and matched line:

   ```bash
   FILE="<file_path>"

   # Same-sentence: subject + not + complement, then pivot
   grep -nE '\b(is|are|was|were|am|be|been)\s+not\s+\w+[;,—]\s*(it|they|that|this|but)\b' "$FILE"

   # Cross-sentence opener: "It's not...", "This isn't...", "That's not..."
   grep -nE "\b(It'?s not|This isn'?t|That'?s not|There is no|There are no)\b" "$FILE"

   # Tail-attached negation: "X — not Y" or "X, not Y"
   grep -nE '[—,]\s*not\s+\w+' "$FILE"

   # "Not just / only / merely / simply" intensifiers
   grep -nE '\bnot (just|only|merely|simply)\b' "$FILE"

   # Contracted negative copulas (often pivot cross-sentence)
   grep -nE "\b(isn'?t|aren'?t|wasn'?t|weren'?t)\b" "$FILE"
   ```

   Skip hits inside fenced code blocks, tables (lines starting with `|`), HTML tags, and frontmatter. Deduplicate by line number.

3. **Triage (subagent).** Dispatch to the `not-but` subagent (defined in `~/agents/not-but.md`, or fallback to `general-purpose` if not registered). Pass:
   - The file path
   - The deduplicated list of hits with line numbers and matched lines
   - The rubric: *can the sentence be replaced by just stating Y, with no loss of meaning?*

   The subagent reads context, applies the rubric, and returns per-hit verdicts (earned vs dead-weight) with proposed rewrites for the dead-weight cases. The subagent does NOT apply edits.

4. **Apply.** Three different decisions, three different sources of authority. The skill enforces this separation because it is the source of the skill's value.

   - **Cut decision (mechanical).** Once the subagent verdicts a hit as dead-weight, the negation goes. No re-litigation by the orchestrator. Letting the orchestrator re-judge re-introduces the LLM blind spot the deterministic detection was designed to defeat — the orchestrator has read the full document, built attachment to the prose, and will rationalize "actually this one is earned" more often than the rubric warrants.
   - **Phrasing of the affirmation (orchestrator discretion).** The subagent's proposed rewrite is a draft. The orchestrator has the full document context the subagent didn't and can refine wording, merge adjacent fixes, restructure sentence boundaries, match surrounding rhythm — anything *except* restoring the negation. Taste lives here.
   - **Re-classification as earned (user only).** Not the orchestrator's call. If the orchestrator genuinely thinks a dead-weight verdict is wrong, surface it in the report — not in the apply — so the user makes the final call.

   Then `Edit` the file. Each dead-weight hit gets cut; the affirmation reads however the orchestrator's judgment lands.

5. **Report** (designed to feed /humanize's earn-back surface):
   - Before/after word count
   - Count of hits: dead-weight, earned, false-positive
   - **Applied cuts** as a numbered list. Each entry: line number, original text, applied rewrite. Cuts where the orchestrator had reservations get marked with `⚠` to draw the eye first.
   - Earned cases (with line numbers) so the user can override.

   When /not-but runs under /humanize, /humanize uses the applied-cuts list to build its post-apply earn-back report and offer `undo N` (or `undo 2,4,7`) to restore specific cuts. When /not-but runs standalone, present the same list as the final output and accept the same undo affordance directly.

6. **Verify**: re-grep after edits. Hits remaining should match the earned list. Anything else means a false-negative in the apply step — note for skill iteration.

## Composability

- **Standalone**: `/not-but <file>` for any file.
- **Inside `/copyedit`**: invoke after `/humanize` as a forced check. Negative parallelism slips past humanize often enough that a deterministic, dedicated step earns its slot in the loop.
- **Batch mode**: pass a directory; greps run across every prose file at once, subagent triages each file independently.

## Why deterministic detection

The patterns are aligned with the LLM's training distribution, so they read as natural to the LLM scanning for them. A regex has no aesthetic preference. False positives are fine — the triage step filters them. False negatives are not — and grep doesn't have any.

The /cord vs /cord-human contrast (referenced in `/humanize`) is the calibration set: re-running this skill on `src/content/blog/2026-02-18-cord.md` should converge it toward `src/content/blog/2026-02-21-cord-human.md` on the negation axis.

## Pattern catalog (what the regexes target)

- `is/are not X; it's Y` (same-sentence)
- `isn't X. It's Y` (cross-sentence)
- `not X but Y`
- `X — not Y` (tail-attached em dash)
- `X, not Y` (tail-attached comma)
- `not just X — Y too`
- `not only X but also Y`
- `not merely X` / `not simply X`
- `there is no X. The Y is...` (paragraph-scope negation-then-assertion)
