# Readability: Prosody, Structure, and Pacing

Scan a blog post for rhythm problems, oversized sections, weak titles, and paragraph imbalance. This skill handles the structural layer — how the post *feels* to read aloud — while humanize handles the word layer.

## Process

1. Read the file.
2. Run all four checks below. Report findings as: `L{line}: {check name} — "{quoted text}" → {suggestion}`
3. Present the list. Wait for approval before applying.
4. Apply fixes. Re-read the result. If anything still drags or stumbles, report it.

## Checks

### 1. Prosody

Read sentences aloud in your head. Flag where the rhythm breaks.

**Stress collisions.** Consecutive stressed syllables with no unstressed buffer: "big black block" → "a big dark block." A function word between downbeats fixes it.

**Stress gaps.** Three or more unstressed syllables in a row: "the implementation of the" is a valley. Restructure so stress falls every 2-3 syllables.

**Dangling prepositions.** The sentence dies on "of." Restructure so the final word carries weight.

**Monotonous sentence starts.** 3+ consecutive sentences starting with the same word or structure. Vary the opener: invert, use a dependent clause, start with the object.

**Parallel structure mismatch.** List items that don't match meter. Fix by making items the same shape.

**Run-on mid-register.** Sentences over 20 words where every word is mid-frequency and mid-stress. Try restructuring first: move a strong word to the end, add a colon pivot, or join with a conjunction. Split only when restructuring can't save it.

**Clause ordering for flow.** Each sentence starts where the previous one ended. Given-before-new: the known thing comes first, the new thing lands last. "The team's coverage comes from overlapping T's" flows into "Fixed hours in a release cycle mean depth costs breadth" because coverage → constraint is a natural handoff. Reversing either sentence breaks the thread. When flow and emphasis align, the sentence works on both passes. When they conflict, prefer flow — the reader who stumbles never reaches the punch. Flag sentences where reordering clauses would connect better to the surrounding context. Only flag when the last noun of sentence N-1 and the first noun of sentence N have no semantic connection — that's the gap the reader has to jump. Don't flag deliberate breaks: "but" sentences, parallel structures, or contrast pairs that intentionally start somewhere new.

### 2. Section titles

**Argue, don't label.** "The experiment" is a topic. "Fifteen decisions, one sentence" is an argument. Prefer titles that compress the claim.

**Title–content match.** If the section drifted during editing, the title may no longer fit.

**Rhythm.** 2-5 words. Longer loses punch. One-word titles work only if surprising in context.

**Consistency.** If most titles are "The X" pattern, flag it. Vary: questions, claims, imperatives.

**Hierarchy.** h2 sections should be parallel in scope. Flag imbalance.

### 3. Paragraph sizing

**Target: 2-5 sentences.** Single-sentence paragraphs fine for emphasis (max 2 per post). 6+ sentences usually means two ideas merged.

**Over 5 sentences:** split where the subject shifts.

**3+ single-sentence paragraphs in a row:** bullet-point energy in prose clothing. Make it a list or combine.

**Long sentence alone:** a 40-word sentence standing as a paragraph has no breathing room. Pair it.

### 4. Section sizing

**Target: 2-4 paragraphs.** One-paragraph sections fine for transitions (max 2 per post). 5+ paragraphs usually means two ideas.

**Over 4 paragraphs:** split or merge.

**One-paragraph sections:** does this need its own header, or should it join the previous section?

**Pacing.** Sections should alternate in weight. Flag 3+ heavy sections (4+ paragraphs each) without a breather.

## Dampener

Only flag issues where the fix is clearly better than what's there. Prosody is subjective — if the rhythm works despite breaking a rule, leave it. A technically perfect sentence that loses voice is worse than an imperfect one that sounds like a person.

Rank findings by impact. Report the top findings. Ignore the rest. A second pass should find little or nothing.
