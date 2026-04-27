---
name: em-dash
description: Flag em-dash usage in prose. Deterministic grep for detection, subagent for triage (earned vs dead-weight), report only — no edits applied. Sister skill to /not-but.
argument-hint: <file_path>
allowed-tools: Read, Grep, Bash, Agent
---

# Em-dash: Overuse Flagger

Em-dash overuse is a top LLM tell — second only to negative parallelism in how reliably it betrays AI prose. This skill uses **deterministic grep for detection** (regex doesn't have stylistic preferences) and a subagent for **triage** (where a comma, period, colon, semicolon, or parens would do the job without loss).

**Flag only — no auto-apply.** Em-dashes have more legitimate uses than "not X but Y" does, so the triage rubric carries more weight and the false-positive rate is higher than /not-but's. The user reads the report and decides which to cut. Sister skill to `/not-but`.

## Process

1. Read the file at the given path. Note the word count and total em-dash count.

2. **Detect (deterministic).** Run grep, capturing every em-dash with surrounding context:

   ```bash
   FILE="<file_path>"

   # Every em-dash with line number
   grep -nE '—' "$FILE"
   ```

   Skip hits inside fenced code blocks, tables (lines starting with `|`), HTML tags, frontmatter, and inline code spans. Deduplicate by line number, but record per-occurrence positions when multiple em-dashes share a line.

3. **Triage (subagent).** Dispatch to the `general-purpose` agent (or a registered `em-dash` agent if one exists). Pass:
   - The file path
   - The deduplicated list of hits with line numbers and matched lines
   - The rubric below

   **Rubric:** *Could a comma, period, colon, semicolon, or parens do this job with no loss of meaning, rhythm, or visual jolt?* If yes → dead-weight. If no → earned.

   **Earned categories** (preserve):
   - Parenthetical insertion where commas would be ambiguous (already nested commas in the surrounding clause)
   - Genuine abrupt break or interruption mid-thought (the dash is the *content*)
   - List intro after an independent clause where a colon would feel too formal
   - Attribution dash before a quote source

   **Dead-weight categories** (flag for cut):
   - Soft pause where a period would land harder
   - Comma replacement with no special break needed
   - Setup-and-pivot construction (often co-occurs with /not-but findings)
   - Conversational connector / hedging glue
   - Two em-dashes in one sentence doing different jobs (one is almost always cuttable)
   - Em-dash density >1 per 200 words (mechanical flag — even if each individual case looks defensible, the cumulative rhythm reads AI)

   The subagent returns per-hit verdicts (earned / dead-weight) with a proposed replacement punctuation for each dead-weight case. The subagent does NOT apply edits.

4. **Report.** Numbered list, sorted by line number:

   ```
   {file}: {N} em-dashes in {word_count} words ({density} per 1000)

   Dead-weight ({count}):
   1. L{line}: "{original sentence}"
      → "{suggested rewrite with replacement punctuation}"
      reason: {one-line rubric reason}

   Earned ({count}):
   1. L{line}: "{sentence}"
      reason: {why it earned its dash}

   Ambiguous ({count}):
   1. L{line}: "{sentence}"
      → "{candidate rewrite}"
      reason: {what makes it borderline}
   ```

   Don't apply edits. The user reads the report and decides.

## Composability

- **Standalone**: `/em-dash <file>` for any prose file.
- **Inside `/humanize`**: /humanize's em-dash pattern section defers to this skill the way it defers to /not-but for negative parallelism. /humanize flags obvious instances opportunistically and applies them; /em-dash is the authoritative drill and its flag-only output attaches to /humanize's post-apply earn-back report as additional candidates the user can apply by line number.
- **Pairs with `/not-but`**: setup-and-pivot em-dashes ("X — not Y") often surface in both. Run /not-but first; remaining em-dashes are easier to triage once the pivot cases are gone.

## Why flag-only

Unlike negative parallelism, where the cut decision is mechanical once a hit is verdicted dead-weight, em-dash replacement requires picking the *right* punctuation (comma vs period vs colon vs parens) — and that pick reshapes sentence rhythm in ways the orchestrator should weigh against surrounding sentences. Auto-apply would either pick conservatively (always commas, flattening rhythm) or get it wrong often enough that the user rewrites half the cuts.

The flag-only output respects that the user is the rhythm authority. The skill's job is to surface every em-dash with a verdict and a candidate, so the user spends judgment on phrasing instead of on detection.

## Why deterministic detection

Em-dashes are visually obvious to humans but blend into the LLM's training distribution. A regex has no aesthetic preference. False positives (earned cases flagged for review) are cheap; false negatives (missed em-dashes) defeat the skill's purpose, and grep has none.
