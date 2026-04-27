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
7. Re-read the result. If anything still reads as AI or feels flat, report it.
8. **Post-apply report (earn-back).** Every cut gets listed as a numbered item: line number, original text, applied rewrite. Flag with `⚠` any cut where the orchestrator had reservations — those are the cases most likely to want reverting. The user can reply `undo N` (or `undo 2,4,7`) to restore specific cuts. Earn-back sits in the report, not blocking the apply. This is the user's safety hatch: the deterministic detection cut things assertively; the report gives every cut back to the user as undo-able.

## Batch mode

When given a directory instead of a single file, or when running a targeted pass on one pattern across many files:

1. **Grep first.** Use Grep with a regex for the target pattern across all files in the directory. This surfaces every instance at once.
2. **Triage the hits.** Sort each match into "earns it" (the pattern carries genuine meaning) or "dead weight" (the negation/filler half can be cut). Report both lists so the user sees the judgment calls.
3. **Batch-fix the dead weight.** Apply all clear fixes. Leave the earned ones alone.
4. Verify the build.

## Patterns

**Em dash overuse.** More than 1 per post is a tell. Replace with periods, commas, colons, or restructure. Count every `—` in the file.

For exhaustive coverage, defer to [/em-dash](~/skills/em-dash/SKILL.md), which uses deterministic grep for detection and a dedicated triage subagent for the earned-vs-dead-weight call. Run /em-dash after /humanize as a forced check, or invoke it directly. /humanize still flags obvious instances opportunistically, but /em-dash is authoritative. Unlike /not-but, /em-dash is flag-only — it doesn't apply edits, because picking the right replacement punctuation (comma vs period vs colon vs parens) reshapes rhythm in ways the orchestrator should weigh against surrounding sentences. /em-dash's report attaches to /humanize's post-apply earn-back report (step 8) as additional flagged candidates for the user to apply by line number.

**Negative parallelisms.** "Not X but Y", "It's not just X, it's Y", "isn't X; it's Y." Define things by what they are. The negation half is almost always dead weight.

**This pattern slips past LLM scans (including this one) more than any other** — LLMs are blind to their own training distribution. For exhaustive coverage, defer to [/not-but](~/skills/not-but/SKILL.md), which uses deterministic grep for detection and a dedicated triage subagent for the earned-vs-dead-weight call. Run /not-but after /humanize as a forced check, or invoke it directly. /humanize still flags obvious instances opportunistically, but /not-but is authoritative. Every cut /not-but applies surfaces in /humanize's post-apply report (step 8) as undo-able by line number; cuts the orchestrator flagged for reservation get a `⚠` so they catch the user's eye first.

When triaging in /humanize standalone, match by shape not wording: subject + negative copula + complement, then same-subject + positive copula + alternative. Tense/number variations (is/are/was/were/will be/has been/becomes/feels/seems/sounds); same-sentence (semicolon, comma, em dash) and cross-sentence forms ("This isn't about X. ... It's about Y."); tail-attached negation ("X — not Y", "X, not Y"); and parallel paragraph openings where one paragraph denies and the next asserts.

**Concession-rebuttal stacking.** Three or more `X is great, but Y is wrong with it` constructions in adjacent paragraphs or list items. AI's go-to template for review-style comparisons — each item gets a positive trait then a "but" rebuttal. If three or more in a row, restructure as a comparison table or trim to the single sharpest item. The repeated rhythm is the tell, even when each individual sentence is fine.

**Restated points.** Same idea said 2-3 ways. Keep the best, kill the rest. Watch for recap paragraphs that summarize what the previous section argued, and closing sentences that echo the opening of their own paragraph. The closing sentence should advance, not echo. A new *angle* on the same idea is reinforcement, not restatement.

**Triple prefix (the filibuster).** A triple itself is fine. A triple where each item shares a repeated prefix or grammatical mold is the tell — it sounds like a politician filibustering: "its own X, its own Y, its own Z"; "no X, no Y, no Z"; "for X, for Y, for Z"; "the X of A, the X of B, the X of C." The repeated prefix pads the rhetoric without adding meaning. Drop it (one "its own" up front, then three bare items) or vary the mold so the parallel breaks. Earned cases exist (a repeated prefix that demonstrates a meaningful equivalence, e.g. cross-language parallels), but the default presumption is filibuster until proven otherwise.

**AI vocabulary.** Additionally, crucial, delve, enhance, fostering, garner, highlight (verb), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant. Flag any occurrence.

**Copula avoidance.** "Serves as", "stands as", "represents", "functions as" instead of "is" or a direct verb. "Serves as the filter" → "is the filter". "Functions as a gate" → "gates".

**Synonym cycling.** Calling the same thing by a different name every sentence to avoid repetition. Just use the same word.

**Superficial -ing clauses.** Participial phrases tacked onto sentences for fake depth: "highlighting...", "underscoring...", "showcasing...", "ensuring...", "reflecting..."

**Filler.** "In order to" (→ "to"), "it is important to note that" (→ delete), "has the ability to" (→ "can"), "due to the fact that" (→ "because"). "The question is/was whether" (→ ask it directly or just state the next sentence). "Worth calling out/noting/mentioning" (→ delete, just say it). See also /tighten for broader compression patterns (dead weight, redundant modifiers, nominalizations).

**Throat-clearing.** Sentences that announce what's about to be said instead of saying it. Examples: "To give you something concrete to react to, here's X" (→ just say X). "The short version:" (→ delete). "Here's why" (→ just argue). "The framework says X" (→ just state X). Editorializing ("No disagreement here", "The parallel is clear") and trailing softeners ("curious whether...") are variants. The test: does the sentence add information or just the author's confidence that information is coming?

**Deferred conclusion.** "That told me X." "That's the point: Y." "What this means is Z." "The takeaway: W." "The pattern: ..." The AI explaining its own argument back to the reader after the fact. Just state the conclusion. If the argument doesn't land without the scaffold, fix the argument, not the framing. Subform of throat-clearing, but post-hoc rather than pre-hoc — and worth flagging separately because it sneaks past the throat-clearing check by appearing to deliver content.

**Inflated significance.** "Pivotal moment", "setting the stage", "marks a shift", "indelible mark", "evolving landscape". If the sentence works without the inflation, cut it.

**Monotonous rhythm.** See /readability (prosody § monotonous sentence starts). Flag here only if it reads as an AI pattern rather than a rhythm problem.

**Stock metaphors.** Dead metaphors that add no meaning the sentence doesn't already carry: "shaky ground", "solid ground", "paves the way", "opens the door", "at the end of the day", "tip of the iceberg", "game changer", "double-edged sword", "level the playing field", "move the needle", "circling this problem". If the sentence works without the metaphor, replace it with the specific claim.

**Format mismatch.** Prose doing work another format handles better. Side-by-side comparison → table. Parallel "X does Y" claims across subjects → table or list. [Cognitive fit](https://doi.org/10.1111/j.1540-5915.1991.tb00344.x): argument stays prose, comparison becomes a table. Only flag when the mismatch is clear (three or more items compared in a paragraph). Two items in a sentence is fine.

## Additions

**Wordplay.** Scan for missed opportunities: terms with double meanings that fit the argument, section titles that could land harder, closing lines that could echo an earlier phrase with a twist. Flag opportunities; suggest specific rewrites. Puns, double entendres, and repurposed jargon all count. Don't force it.

**Arc (foreshadow/recall).** Do the opening and closing connect? The last line should recall the first, reframe the title, or close a loop the reader didn't notice was open. Flat two-word closers ("Small, but real.") assert closure instead of earning it. Exception: a short closer that echoes an earlier line earns its brevity. Also: does the title earn its meaning by the end? For full arc analysis, use /arc-check.

**Unsubstantiated claims.** Flag any factual or causal claim that lacks a citation, a link, or a concrete example. Opinions and arguments are fine without sourcing. Empirical claims ("X% of Y do Z", "studies show", "the data suggests") need a link or a qualifier like "in my experience." If a claim is presented as fact but is actually the author's hypothesis, flag it for reframing.

**Slang and voice injection.** Scan for places where formal phrasing can become casual without forcing it. The test: does the swap sound like a person thinking out loud? If a reader notices the informality, it's forced. Targets: (1) Abstract motivations → rhetorical questions. (2) Multi-clause descriptions → blunt summaries. (3) Jargon → plain equivalent when the formal term isn't load-bearing. Leave technical terms that carry precision no slang can match. A second pass should find nothing to add.

**First-person presence.** When a post is about the author's project, opinion, or lived experience but uses "I" fewer than ~5 times per 1000 words, the voice has drifted to documentation. Re-personalize: "It produces X" → "I made it produce X"; "The framework requires Y" → "I had to specify Y when I built it." First-person anchors claims to specific events, lets doubts and motivations surface, and puts the writer on the hook for what they say. Skip when the genre is genuinely third-person (analytical reportage, abstract observation); apply when the post is the author's own work, opinion, or thought.

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and the [humanizer](https://github.com/blader/humanizer) skill by @blader.

**Reference contrast (calibration set):** [/cord](https://june.kim/cord) is AI-written; [/cord-human](https://june.kim/cord-human) is the same author's human rewrite of the same project. Reading them side by side surfaces every pattern above in context. When tuning this skill, re-run it on `src/content/blog/2026-02-18-cord.md` and check that the diff converges toward `src/content/blog/2026-02-21-cord-human.md` without overshooting (the human version is not pattern-free; it has typos, long winding sentences, and other features the skill should not strip).
