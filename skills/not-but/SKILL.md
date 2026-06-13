---
name: not-but
description: Find and defuse "not X but Y" / "isn't X; it's Y" / "X — not Y" constructions. Deterministic grep for detection (no LLM blind spot), the not-but subagent for triage. Cut dead-weight negations; recast non-iconic earned contrasts with a varied substitute palette (keep the contrast, change the construction); keep only iconic thesis lines literal.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Bash, Agent
---

# Not-but: Negative-Parallelism Hunter

LLMs have a structural blind spot for their own patterns. "Not X but Y" is the most common AI tic and the slipperiest one — pattern-matching by another LLM misses it as often as the original write did. This skill uses **deterministic grep for detection** (no blind spot) and an LLM only for **triage** (where judgment is needed).

Sister skill to `/humanize`. Where humanize scans broadly across many patterns, this drills on the one pattern that slips past humanize most often.

**The construction is a tell even when the contrast is real.** Human readers are turned off by the *shape* of "not X but Y" regardless of whether the X-versus-Y distinction is load-bearing. This is the insight that makes the skill more than a filler-cutter: a triage that stops at "earned vs dead-weight" leaves a dense paper riddled with earned negations that still read as machine-written. So triage has **three** outcomes, not two:

- **Dead-weight** — the negation is filler; Y stands alone. Cut it.
- **Iconic** — a thesis line whose force *is* the antithesis ("True and false are not opposites but siblings"). Keep the literal construction. These are rare; protect them.
- **Earned-but-varyable** — the contrast is real and must survive, but the syntax should change. This is the COMMON case in argumentative prose. Keep the contrast, recast the construction. Never delete the distinction.

The earned-but-varyable bucket is the skill's main yield on already-tight prose, where almost everything triages as "earned" under the old two-way rubric and nothing gets fixed. The density of the construction is the tell, not any single instance.

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
   - The rubric, in two questions: (1) *Can the sentence be replaced by just stating Y, with no loss of meaning?* If yes → **dead-weight**. (2) If no (the contrast is real), *is this a thesis line whose whole force is the antithesis?* If yes → **iconic** (keep literal); if no → **earned-but-varyable** (recast the construction, keep the contrast). Most real contrasts in dense prose are varyable, not iconic.

   The subagent reads context, applies the rubric, and returns a per-hit verdict of **dead-weight / iconic / earned-but-varyable** (see the three outcomes above). Pass it two more things:
   - **The iconic-keep list** for this document, if known (the handful of thesis lines whose antithesis is the point). When unknown, instruct the subagent to nominate them conservatively and default everything else to varyable.
   - **The substitute palette** (below), with the standing instruction: for every dead-weight AND every earned-but-varyable hit, propose a recast; vary the device across hits so the fix does not migrate the tic onto one replacement.

   The subagent returns, per hit: the verdict, and for dead-weight/varyable hits a proposed recast naming which palette device it used. The subagent does NOT apply edits.

   **The substitute palette** (keep the contrast, change the construction; the point is variety, so no single device should dominate):
   - positive recast that implies the contrast ("X is no new metaphysics. It specifies...")
   - period split / "X. It is Y" / "X; it is Y"
   - "instead of", "as opposed to", "in contrast to"
   - subordinating clause: "while X, Y" / "X while leaving Y untouched" / "where X, Y"
   - "without Ying", "with no Y", "never Y" (single negated tail, milder than the full antithesis)
   - "though no more Y", "less X than Y", "more than X; it is Y"
   - full negated clause: "It does not mean Y" / "None attests Y"
   - AVOID defaulting to **"rather than"** — it is itself an overused contrastive in argumentative prose, so leaning on it just moves the tell. Check the document's existing "rather than" count first.

4. **Apply.** Three different decisions, three different sources of authority. The skill enforces this separation because it is the source of the skill's value.

   - **Change decision (mechanical).** Once the subagent verdicts a hit as dead-weight or earned-but-varyable, the literal "not X but Y" construction goes. Dead-weight → cut the negation; varyable → recast it via the palette. No re-litigation by the orchestrator. Letting the orchestrator re-judge re-introduces the LLM blind spot the deterministic detection was designed to defeat — the orchestrator has read the full document, built attachment to the prose, and will rationalize "actually this one reads fine" more often than the rubric warrants.
   - **Phrasing of the recast (orchestrator discretion).** The subagent's proposed rewrite is a draft. The orchestrator has the full document context the subagent didn't and can refine wording, merge adjacent fixes, restructure sentence boundaries, match surrounding rhythm, and — for varyable hits — swap one palette device for another to keep the document's overall device mix diverse. The one rule: do not restore the bare "not X but Y" shape. Taste lives here. (A recast that would be clunkier than the original is the one exception: kick it back to KEEP and note why. A varyable verdict is not a mandate to make the prose worse.)
   - **Re-classification as iconic (user only).** Not the orchestrator's call. If the orchestrator genuinely thinks a varyable verdict should be left literal (a thesis line the subagent missed), surface it in the report — not in the apply — so the user makes the final call.

   Then `Edit` the file. Dead-weight hits lose the negation; varyable hits get the recast; iconic hits stand. Across the varyable set, watch the aggregate: if three recasts in a row used "; it is", vary the third.

5. **Report** (designed to feed /humanize's earn-back surface):
   - Before/after word count
   - Count of hits: dead-weight, earned-but-varyable, iconic, false-positive
   - **Applied changes** as a numbered list. Each entry: line number, original text, applied rewrite, and (for varyable hits) the palette device used. Changes where the orchestrator had reservations get marked with `⚠` to draw the eye first.
   - A one-line **device tally** for the varyable set (e.g. "period-split ×3, in-contrast-to ×2, never ×2, ...") so over-reliance on one substitute is visible at a glance.
   - Iconic (kept-literal) cases, with line numbers, so the user can override.

   When /not-but runs under /humanize, /humanize uses the applied-cuts list to build its post-apply earn-back report and offer `undo N` (or `undo 2,4,7`) to restore specific cuts. When /not-but runs standalone, present the same list as the final output and accept the same undo affordance directly.

6. **Verify**: re-grep after edits. The "not X but Y" hits remaining should match the iconic kept-literal list (varyable hits are recast into other shapes, so they drop out of the grep; tail-attached "X, not Y" milder forms may remain by design). A leftover that is neither iconic nor an intended mild tail means a false-negative in the apply step — note for skill iteration.

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
