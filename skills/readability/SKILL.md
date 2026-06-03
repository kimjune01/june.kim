# Readability: Prosody, Structure, and Pacing

Scan a blog post for rhythm problems, oversized sections, weak titles, and paragraph imbalance. This skill handles the structural layer — how the post *feels* to read aloud — while humanize handles the word layer.

## Process

1. Read the file.
2. Run all six checks below.
3. Apply all fixes directly. Prosody fixes especially — be liberal with these. If a sentence sounds better restructured, restructure it.
4. Report what changed. Re-read the result. If anything still drags or stumbles, fix it.

## Checks

### 1. Prosody

Read sentences aloud in your head. Flag where the rhythm breaks. **Scope: word-shuffling only.** Reorder existing words and clauses. Add or drop function words (articles, prepositions, conjunctions) to fix stress patterns. Do not swap content words. Do not change verbs. Do not introduce em-dashes (the em-dash budget is 0 in prose; see *Cross-skill policies* below). If a fix requires substituting a different verb, that's a taste call, not a rhythm fix — leave it for /sharpen or the human.

**Stress collisions.** Consecutive stressed syllables with no unstressed buffer: "big black block" → "a big dark block." A function word between downbeats fixes it.

**Stress gaps.** Three or more unstressed syllables in a row: "the implementation of the" is a valley. Reorder so stress falls every 2-3 syllables.

**Dangling prepositions.** The sentence dies on "of" or "for" or "to." Restructure so the final word carries weight. Restructure means *reorder the same words*, not *find a stronger word*.

**Buried actors (cleft + passive).** Find the actor in the sentence and move it to subject position. *"It's what every framework is scrambling to bolt on"* (cleft) → *"Every framework is scrambling to bolt it on."* *"The bug was caused by a race condition"* (passive) → *"A race condition caused the bug."* Identify the doer; make it the subject. This is a reordering, not a word substitution. Keep the cleft when the topic genuinely sits in the predicate (*"It's not the algorithm that matters, it's the data"*) or when the actor is unknown or irrelevant (*"The file was deleted overnight"* — by whom doesn't matter).

**Monotonous sentence starts.** 3+ consecutive sentences starting with the same word or structure. Vary the opener: invert, use a dependent clause, start with the object. Reorder; don't substitute.

**Parallel structure mismatch.** List items that don't match meter. Fix by making items the same shape using the existing words.

**Contrast pairs as separate sentences.** Two consecutive sentences with the same structure that say opposite things ("X does A. Y does B.") often read stronger joined by a semicolon. The semicolon signals the contrast is intentional; the period makes it look accidental. Flag when the parallel is exact enough that a semicolon would land the opposition in one breath.

**Run-on mid-register.** Sentences over 20 words where every word is mid-frequency and mid-stress. Try restructuring first: move a strong word to the end, add a colon pivot, or join with a conjunction. Split only when restructuring can't save it. Word substitution is off-limits.

**Clause ordering for flow.** Each sentence starts where the previous one ended. Given-before-new: the known thing comes first, the new thing lands last. "The team's coverage comes from overlapping T's" flows into "Fixed hours in a release cycle mean depth costs breadth" because coverage → constraint is a natural handoff. Reversing either sentence breaks the thread. When flow and emphasis align, the sentence works on both passes. When they conflict, prefer flow — the reader who stumbles never reaches the punch. Flag sentences where reordering clauses would connect better to the surrounding context. Only flag when the last noun of sentence N-1 and the first noun of sentence N have no semantic connection — that's the gap the reader has to jump. Don't flag deliberate breaks: "but" sentences, parallel structures, or contrast pairs that intentionally start somewhere new.

#### What this check is NOT

- **Not power-verb-over-copula.** That's a substance change. If a sentence reads better with a different verb, leave it for /sharpen or a human pass. Readability changes *order*, not *vocabulary*.
- **Not voice tightening.** "Sweep takes" → "Sweep eats" is a taste call, not a rhythm fix.
- **Not introducing em-dashes.** Em-dash budget is 0 in prose throughout the pipeline.
- **Not adding new content words** for image or impact.

The skill should make the same words read better in the same order, sometimes with the order shuffled. Anything more is out of scope.

### 2. Section titles

**Argue, don't label.** "The experiment" is a topic. "Fifteen decisions, one sentence" is an argument. Prefer titles that compress the claim.

**Title–content match.** If the section drifted during editing, the title may no longer fit.

**Rhythm.** 2-5 words. Longer loses punch. One-word titles work only if surprising in context.

**Consistency.** If most titles are "The X" pattern, flag it. Vary: questions, claims, imperatives.

**Hierarchy.** h2 sections should be parallel in scope. Flag imbalance.

### 3. Emoji H1s

**Lightweight diagrams.** When a paragraph explains a relationship that a line of emojis could show at a glance, the emoji H1 is simpler than both the paragraph and an SVG. Flag paragraphs where a reader would understand faster from a few glyphs than from the prose.

**When to suggest.** The concept is visual and compact enough to read in one line. If it needs spatial layout (cycles, grids, hierarchies), it needs an SVG. If it fits in a breath, emojis work.

**Format.** H1 heading, mostly emojis. Arrows or `vs.` when the relationship needs them. No prose. The line *replaces* a paragraph; it doesn't caption one.

### 4. Paragraph sizing

**Target: 2-5 sentences.** Single-sentence paragraphs fine for emphasis (max 2 per post). 6+ sentences usually means two ideas merged.

**Over 5 sentences:** split where the subject shifts.

**3+ single-sentence paragraphs in a row:** bullet-point energy in prose clothing. Make it a list or combine.

**Inline enumerations.** A sentence with 3+ comma-separated items (especially with parenthetical details per item) scans faster as a bulleted list. Flag sentences like "X (detail), Y (detail), Z (detail), and more" — the reader's eye is already parsing vertically. Convert to a list. This applies especially to: sequences of named examples with annotations, pipeline stages with descriptions, and evidence lists with citations.

**Long sentence alone:** a 40-word sentence standing as a paragraph has no breathing room. Pair it.

### 5. Section sizing

**Target: 2-4 paragraphs.** One-paragraph sections fine for transitions (max 2 per post). 5+ paragraphs usually means two ideas.

**Over 4 paragraphs:** split or merge.

**One-paragraph sections:** does this need its own header, or should it join the previous section?

**Pacing.** Sections should alternate in weight. Flag 3+ heavy sections (4+ paragraphs each) without a breather.

### 6. Bold vs italic

**Bold is for definitions and terms of art.** A word is bold when the reader needs to learn it: a new concept, a named pattern, a key distinction. Bold says "remember this."

**Italic is for emphasis.** Stress within a sentence, a qualifier, a tone shift. Italic says "hear this differently."

**Flag non-definition bolds.** If the bolded phrase isn't introducing a term or labeling a structural element (list item, table header), swap to italic or remove. Excessive inline bold makes everything look like a heading and nothing stands out.

### 7. Opening orientation

The first sentence of the document, and of each major section, must land a concrete anchor a target reader can grasp *without already knowing the document's vocabulary*. Lead with what the thing is, what it does, or the stakes, in plain words; defer specialized terms until the reader is grounded. The test: would a smart non-specialist get past sentence one? (A real reader of a dense research README stopped before the first sentence ended, because the opener was three jargon terms deep with no hook.)

**Translate, then name.** When a term is jargon to the target reader, give the plain version first and attach the name after, not the reverse. "Guess the cause, write a fix, test it, throw the guess out if it fails," *then* "that discipline is called methodeutics," reads; "applied methodeutics, Peirce's term for…" as the opener loses the reader who needed the plain version.

**Scope.** If the concrete anchor already exists later in the piece, this is a reorder: move the buried hook up (squarely in readability's wheelhouse). If no plain anchor exists at all, flag that the opening needs one, but do not invent claims; surfacing a missing hook is the human's or /sharpen's call, not a fabrication.

## Cross-skill policies

- **Em-dash budget: 0 in prose.** Reference-list separators (`[link](url) — description`) are exempt because they're typographic, not rhetorical. Do not introduce em-dashes in body prose for pacing, parenthetical asides, or contrast pivots. Use commas, parens, colons, or sentence breaks instead. This policy lives in `/humanize`'s patterns section; readability must honor it because the pipeline runs solo on this skill too.

- **Word-shuffling only.** Reorder existing words and add/drop function words. Don't swap content words. Substance changes belong to `/sharpen` or human judgment.

- **Clarity, not casualness.** Legibility means the reader reaches the content, not that the content is softened. Never trade a precise term for a friendlier but vaguer one; a plain word that loses the technical meaning is worse than the jargon it replaced. The fix for an alienating opener is to *orient* the reader (lead concrete, translate-then-name), not to dumb the substance down.

## Aggression by check

Prosody is **uncapped**. The other checks have natural ceilings; prosody does not. Read every sentence aloud. If any sentence has a stress collision, a stress gap, a dangling preposition, a buried actor, a copula where a power verb would carry, or a clause order that breaks the given-before-new flow, rewrite it. Default to restructuring. The fail mode is leaving a clunky sentence alone because "it's technically grammatical." A clunky sentence the reader has to re-read is a cost; the cost compounds across the post.

A single readability pass should apply prosody fixes at a rate of roughly one per two or three sentences, not three or four per document. The count scales with length: a 1500-word post yields dozens, a 6000-word paper yields *more*, never fewer. If your pass found fewer than ten prosody changes on anything past a few paragraphs, you read too generously. Go again, this time committing to read aloud and edit on every stumble.

**Excuses that mean you under-read.** Each of these is the timidity prior talking, not a real reason to leave a stumble alone. Name it and override it:

- *"The document is long / dense / already heavily edited."* Length scales the fix count *up*: more sentences, more stumbles. Prior editing for argument, structure, and word choice is orthogonal to prosody. "Polished" describes substance; rhythm is a separate, uncorrelated pass, so a much-revised paragraph can have every sentence un-tuned. Dense technical prose is the *most* prone to buried actors and dangling tails, not exempt from them. Density is content; rhythm is delivery.
- *"It's a judgment call, so I'll flag it instead of fixing it."* Within word-shuffling scope, the judgment is yours to make *and apply*. The diff is the review. Applying a fix and showing it is not the same as deciding for the human; do not silently downgrade "this needs a decision" into "this needs the human's decision" and leave the sentence alone. Flag only what genuinely exceeds the scope (a content-word swap, a claim change), not what merely requires you to choose.
- *"It's technically grammatical."* Grammatical and clunky are independent. The reader re-reads a grammatical stumble at the same cost as an ungrammatical one.

**The symmetric failure is just as real: do not manufacture fixes to hit a count.** Ten is a *smell, not a quota*. "Fewer than ten" means re-read suspiciously, not produce ten. A genuinely clean sentence stays clean; restructuring prose that was already right to look productive is the same miscalibration pointed the other way, and it *damages* the text. The target is *every real stumble fixed and none invented*. If an honest read-aloud of a well-tuned section finds three, three is the answer — provided you actually read it aloud and didn't wave it through. Both directions are failures: leaving a stumble because you're timid, and inventing one because you're chasing a number. The skill wants your ear, not your compliance.

The other five checks (titles, emoji H1s, paragraph sizing, section sizing, bold/italic) are damped. Once they land, they're settled. A second pass on those should find little.

Prosody can keep finding things across multiple passes and that is fine. Restructuring sentence N often surfaces a rhythm problem in sentence N+1 that was masked by the worse sentence next to it. The pipeline's monoidal contract holds at the post level (eventually the prose stops needing fixes) but prosody's per-pass ceiling is *the rhythm of the post*, not *one and done*.

A technically perfect sentence that loses voice is worse than an imperfect one that sounds like a person, but most prosody fixes improve both. When in doubt, restructure.
