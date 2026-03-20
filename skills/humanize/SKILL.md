---
name: humanize
description: Scan blog posts for AI writing tics and missed opportunities for human voice. Reports subtractions (AI patterns to remove) and additions (wordplay, arc, and claims to strengthen).
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, AskUserQuestion
---

# Humanize: AI Pattern Scan for Blog Posts

Scan a post for AI writing tics and missed opportunities for human voice.

## Process

1. Read the file
2. **Subtract:** Scan for every AI pattern below. Report each instance as: `L{line}: {pattern name} — "{quoted text}"`
3. **Add:** Scan for wordplay opportunities, arc issues, and unsubstantiated claims. Report each as: `L{line}: {opportunity name} — "{quoted text}" → {suggestion}`
4. Present both lists. **Commit the file before applying any fixes** so the human can review the diff and revert mistakes.
5. **Judgment call:** if every finding is clear Filter-level work (em dashes, filler, negative parallelisms, restated points), apply fixes directly. If any finding touches argument structure, voice, or is ambiguous, wait for the user to approve.
6. Apply fixes. Preserve the argument; cut the padding; add the voice. Balance flow and punch: longer sentences build momentum, short ones land the point. A post that's all short sentences reads like a telegram. A post that's all long ones reads like a textbook.
6. Re-read the result. If anything still reads as AI or feels flat, report it.

## Patterns

**Em dash overuse.** More than 1 per post is a tell. Replace with periods, commas, colons, or restructure. Count every `—` in the file.

**Negative parallelisms.** "Not X but Y", "It's not just X, it's Y", "isn't X; it's Y." Define things by what they are. The negation half is almost always dead weight. Alternatives: "More than X", "Beyond X", or just state Y directly. Even legitimate uses now read as generated.

**Restated points.** Same idea said 2-3 ways. Keep the best, kill the rest. Watch for recap paragraphs that summarize what the previous section argued, and closing sentences that echo the opening of their own paragraph. The closing sentence should advance, not echo. A new *angle* on the same idea is reinforcement, not restatement.

**Rule of three.** Three parallel items are a tell. Check whether the list is honest or performative. If the argument already landed, state the strongest claim and stop. A triple where each item carries genuinely distinct information is fine.

**AI vocabulary.** Additionally, crucial, delve, enhance, fostering, garner, highlight (verb), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant. Flag any occurrence.

**Copula avoidance.** "Serves as", "stands as", "represents", "functions as" instead of "is" or a direct verb. "Serves as the filter" → "is the filter". "Functions as a gate" → "gates".

**Synonym cycling.** Calling the same thing by a different name every sentence to avoid repetition. Just use the same word.

**Superficial -ing clauses.** Participial phrases tacked onto sentences for fake depth: "highlighting...", "underscoring...", "showcasing...", "ensuring...", "reflecting..."

**Filler.** "In order to" (→ "to"), "it is important to note that" (→ delete), "has the ability to" (→ "can"), "due to the fact that" (→ "because"). "The question is/was whether" (→ ask it directly or just state the next sentence). "Worth calling out/noting/mentioning" (→ delete, just say it). See also /tighten for broader compression patterns (dead weight, redundant modifiers, nominalizations).

**Throat-clearing.** Sentences that announce what's about to be said instead of saying it. Examples: "To give you something concrete to react to, here's X" (→ just say X). "The short version:" (→ delete). "Here's why" (→ just argue). "The framework says X" (→ just state X). Editorializing ("No disagreement here", "The parallel is clear") and trailing softeners ("curious whether...") are variants. The test: does the sentence add information or just the author's confidence that information is coming?

**Inflated significance.** "Pivotal moment", "setting the stage", "marks a shift", "indelible mark", "evolving landscape". If the sentence works without the inflation, cut it.

**Monotonous rhythm.** See /readability (prosody § monotonous sentence starts). Flag here only if it reads as an AI pattern rather than a rhythm problem.

**Stock metaphors.** Dead metaphors that add no meaning the sentence doesn't already carry: "shaky ground", "solid ground", "paves the way", "opens the door", "at the end of the day", "tip of the iceberg", "game changer", "double-edged sword", "level the playing field", "move the needle", "circling this problem". If the sentence works without the metaphor, replace it with the specific claim.

**Format mismatch.** Prose doing work another format handles better. Side-by-side comparison → table. Parallel "X does Y" claims across subjects → table or list. [Cognitive fit](https://doi.org/10.1111/j.1540-5915.1991.tb00344.x): argument stays prose, comparison becomes a table. Only flag when the mismatch is clear (three or more items compared in a paragraph). Two items in a sentence is fine.

## Additions

**Wordplay.** Scan for missed opportunities: terms with double meanings that fit the argument, section titles that could land harder, closing lines that could echo an earlier phrase with a twist. Flag opportunities; suggest specific rewrites. Puns, double entendres, and repurposed jargon all count. Don't force it.

**Arc (foreshadow/recall).** Do the opening and closing connect? The last line should recall the first, reframe the title, or close a loop the reader didn't notice was open. Flat two-word closers ("Small, but real.") assert closure instead of earning it. Exception: a short closer that echoes an earlier line earns its brevity. Also: does the title earn its meaning by the end? For full arc analysis, use /arc-check.

**Unsubstantiated claims.** Flag any factual or causal claim that lacks a citation, a link, or a concrete example. Opinions and arguments are fine without sourcing. Empirical claims ("X% of Y do Z", "studies show", "the data suggests") need a link or a qualifier like "in my experience." If a claim is presented as fact but is actually the author's hypothesis, flag it for reframing.

**Slang and voice injection.** Scan for places where formal phrasing can become casual without forcing it. The test: does the swap sound like a person thinking out loud? If a reader notices the informality, it's forced. Targets: (1) Abstract motivations → rhetorical questions. (2) Multi-clause descriptions → blunt summaries. (3) Jargon → plain equivalent when the formal term isn't load-bearing. Leave technical terms that carry precision no slang can match. A second pass should find nothing to add.

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and the [humanizer](https://github.com/blader/humanizer) skill by @blader.
