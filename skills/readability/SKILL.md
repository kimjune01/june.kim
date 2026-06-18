---
name: readability
description: Document shape and pacing — section titles, emoji H1s, paragraph and section sizing, bold vs italic, opening orientation. Sentence-level rhythm and cohesion live in /flow; the word layer in /humanize.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, AskUserQuestion
---

# Readability: Structure and Pacing

Scan a post for oversized sections, weak titles, paragraph imbalance, and orientation gaps — how the post is *shaped* on the page. Sentence-level rhythm and between-sentence cohesion belong to `/flow`; the word layer belongs to `/humanize`. This skill handles everything above the sentence.

## Process

1. Read the file.
2. Run the six checks below.
3. Apply fixes directly. These are damped: once a title, a split, or a bold/italic call lands, it settles.
4. Re-read. If a section still drags or a paragraph still sprawls, fix it.

## Checks

### 1. Section titles

**Argue, don't label.** "The experiment" is a topic. "Fifteen decisions, one sentence" is an argument. Prefer titles that compress the claim.

**Title–content match.** If the section drifted during editing, the title may no longer fit.

**Rhythm.** 2-5 words. Longer loses punch. One-word titles work only if surprising in context.

**Consistency.** If most titles are "The X" pattern, flag it. Vary: questions, claims, imperatives.

**Hierarchy.** h2 sections should be parallel in scope. Flag imbalance.

### 2. Emoji H1s

**Lightweight diagrams.** When a paragraph explains a relationship that a line of emojis could show at a glance, the emoji H1 is simpler than both the paragraph and an SVG. Flag paragraphs where a reader would understand faster from a few glyphs than from the prose.

**When to suggest.** The concept is visual and compact enough to read in one line. If it needs spatial layout (cycles, grids, hierarchies), it needs an SVG. If it fits in a breath, emojis work.

**Format.** H1 heading, mostly emojis. Arrows or `vs.` when the relationship needs them. No prose. The line *replaces* a paragraph; it doesn't caption one.

### 3. Paragraph sizing

**Target: 2-5 sentences.** Single-sentence paragraphs fine for emphasis (max 2 per post). 6+ sentences usually means two ideas merged.

**Over 5 sentences:** split where the subject shifts.

**3+ single-sentence paragraphs in a row:** bullet-point energy in prose clothing. Make it a list or combine.

**Inline enumerations.** A sentence with 3+ comma-separated items (especially with parenthetical details per item) scans faster as a bulleted list. Flag sentences like "X (detail), Y (detail), Z (detail), and more" — the reader's eye is already parsing vertically. Convert to a list. This applies especially to: sequences of named examples with annotations, pipeline stages with descriptions, and evidence lists with citations. (Weigh against rhetorical momentum: a deliberate rapid-fire cascade — "it kept winning, and winning, and winning" — sometimes earns the run-on. When in doubt, surface the choice.)

**Long sentence alone:** a 40-word sentence standing as a paragraph has no breathing room. Pair it.

### 4. Section sizing

**Target: 2-4 paragraphs.** One-paragraph sections fine for transitions (max 2 per post). 5+ paragraphs usually means two ideas.

**Over 4 paragraphs:** split or merge.

**One-paragraph sections:** does this need its own header, or should it join the previous section?

**Pacing.** Sections should alternate in weight. Flag 3+ heavy sections (4+ paragraphs each) without a breather.

### 5. Bold vs italic

**Bold is for definitions and terms of art.** A word is bold when the reader needs to learn it: a new concept, a named pattern, a key distinction. Bold says "remember this."

**Italic is for emphasis.** Stress within a sentence, a qualifier, a tone shift. Italic says "hear this differently."

**Flag non-definition bolds.** If the bolded phrase isn't introducing a term or labeling a structural element (list item, table header), swap to italic or remove. Excessive inline bold makes everything look like a heading and nothing stands out.

### 6. Opening orientation

The first sentence of the document, and of each major section, must land a concrete anchor a target reader can grasp *without already knowing the document's vocabulary*. Lead with what the thing is, what it does, or the stakes, in plain words; defer specialized terms until the reader is grounded. The test: would a smart non-specialist get past sentence one? (A real reader of a dense research README stopped before the first sentence ended, because the opener was three jargon terms deep with no hook.)

**Translate, then name.** When a term is jargon to the target reader, give the plain version first and attach the name after, not the reverse. "Guess the cause, write a fix, test it, throw the guess out if it fails," *then* "that discipline is called methodeutics," reads; "applied methodeutics, Peirce's term for…" as the opener loses the reader who needed the plain version.

**Scope.** If the concrete anchor already exists later in the piece, this is a reorder: move the buried hook up (squarely in scope). If no plain anchor exists at all, flag that the opening needs one, but do not invent claims; surfacing a missing hook is the human's or /sharpen's call, not a fabrication.

## Cross-skill policies

- **Em-dash budget: 0 in prose.** Reference-list separators (`[link](url) — description`) are exempt because they're typographic, not rhetorical. Do not introduce em-dashes in titles or body prose. Use commas, parens, colons, or sentence breaks instead.

- **Clarity, not casualness.** Legibility means the reader reaches the content, not that the content is softened. Never trade a precise term for a friendlier but vaguer one; a plain word that loses the technical meaning is worse than the jargon it replaced. The fix for an alienating opener is to *orient* the reader (lead concrete, translate-then-name), not to dumb the substance down.

## Aggression by check

All six checks here are **damped**. Once they land, they're settled — a second pass should find little. This is the opposite of `/flow`, whose prosody and cohesion passes are uncapped and keep finding things. Run the structural checks once, decisively, and move on.

The one check with a reorder/flag boundary is **opening orientation**: moving a buried hook up is in scope and you should just do it; inventing a hook that doesn't exist is not, and that goes to /sharpen or the human.

Pacing and sizing are judgment calls about the *shape* of the argument, not its wording — when a split or merge would change which ideas sit together, surface it rather than deciding silently.
