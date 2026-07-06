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

**Signal weighting (read first).** As of 2026 the durable tell is *structure and co-occurrence*, not single words: frontier prose reads clean sentence by sentence, so detection moved up to document shape, formatting reflexes, and density. Don't call a passage AI-ish on one hit. Tiers: *hard flag* = tool/channel leakage (raw markdown in a non-markdown channel); *high* = repeated bold-lead bullets, stacked staged-framing labels, dense participial tails; *medium* = false ranges, hedge stacks, tricolon-by-count, uniform sentence length; *low* (supporting only) = individual vocabulary items, a lone em dash, a single correlative pair. Still flag low-signal items, but weight by clustering, not occurrence.

**Em dash overuse.** Em dashes in prose are a tell; the budget is 0. Reference-list separators (`[link](url) — description`) are exempt because they're typographic, not rhetorical. Workflow: replace every prose `—` with the right substitute (period for beat, colon for definition, comma for aside, parens for parenthetical), apply all replacements in one pass, then surface the batch as a numbered list with line + before/after so the user can elicit a revert on any line where the em dash earned its weight. Don't elicit one at a time; bunch them. Count every prose `—` in the file before and after. (As a *detector* signal the em dash weakened in 2026, since vendors discount it alone and models added suppression; the function migrated to colon-pivots and rhetorical fragments, so strip those too.)

**Negative parallelisms.** "Not X but Y", "It's not just X, it's Y", "isn't X; it's Y." Define things by what they are. The negation half is almost always dead weight. The plain inline form is burned; the 2026 escalation is the fragmented variants, so catch them too: the period-separated countdown ("Not X. Not Y. Just Z."), "the question isn't X, it's Y", "less about X, more about Y", the tail-contrastive ("X rather than Y", "X instead of Y", "X over Y") whenever the Y half is just not-X padding, and correlative pairs ("not only X but also Y", "both X and Y"). "Rather than" is the sneakiest: it reads as neutral comparison, so it survives passes that catch "not"; flag it when Y restates the negation of X and carries no independent content. This is the most-discussed AI tell of 2026 (its corporate-doc incidence roughly quadrupled 2023-2025).

**This pattern slips past LLM scans (including this one) more than any other** — LLMs are blind to their own training distribution. For exhaustive coverage, defer to [/not-but](~/skills/not-but/SKILL.md), which uses deterministic grep for detection and a dedicated triage subagent for the earned-vs-dead-weight call. Run /not-but after /humanize as a forced check, or invoke it directly. /humanize still flags obvious instances opportunistically, but /not-but is authoritative. Every cut /not-but applies surfaces in /humanize's post-apply report (step 8) as undo-able by line number; cuts the orchestrator flagged for reservation get a `⚠` so they catch the user's eye first.

When triaging in /humanize standalone, match by shape not wording: subject + negative copula + complement, then same-subject + positive copula + alternative. Tense/number variations (is/are/was/were/will be/has been/becomes/feels/seems/sounds); same-sentence (semicolon, comma, em dash) and cross-sentence forms ("This isn't about X. ... It's about Y."); tail-attached negation ("X — not Y", "X, not Y"); and parallel paragraph openings where one paragraph denies and the next asserts.

**Concession-rebuttal stacking.** Three or more `X is great, but Y is wrong with it` constructions in adjacent paragraphs or list items. AI's go-to template for review-style comparisons — each item gets a positive trait then a "but" rebuttal. If three or more in a row, restructure as a comparison table or trim to the single sharpest item. The repeated rhythm is the tell, even when each individual sentence is fine.

**Restated points.** Same idea said 2-3 ways. Keep the best, kill the rest. Watch for recap paragraphs that summarize what the previous section argued, and closing sentences that echo the opening of their own paragraph. The closing sentence should advance, not echo. A new *angle* on the same idea is reinforcement, not restatement.

**Textual self-reference (meta-discourse).** Prose narrating its own container instead of its subject. The principle: the reader's purpose fixes the basis, and a sentence *about the text* falls outside it — it's the variable the goal made irrelevant, kept on the page anyway. Models emit it reflexively ("In this section we will", "As discussed above", "It is worth noting that this chapter"). Three subtypes:
- *Recall-burden cross-reference*: "Chapter 4 left a debt", "as we saw earlier", "recall that", "the previous section showed" — forces the reader to reload a passage they may not hold. In a linked collection, convert it to a hyperlink on the relevant noun (`<a href=...>eight names</a>`), not a prose recap; the edge belongs in the graph, not re-narrated. Standalone, cut and state the idea directly.
- *Container-naming*: "this chapter", "this section", "in this post", "the book", "the next chapters" used to orient. Drop the deixis; an idea doesn't need its location announced. ("here" for self-voicing is fine — "the entire thesis here" — but "the entire thesis of this chapter" is not.)
- *Rhetorical-structure narration*: "Note the X, because the chapter ends on it", "which is the whole point", "Hold that; the closing section spends it". Announces the move instead of making it; the emphasis should live in *what you do with the thing*, not a label saying it matters.
Grep: `\b(this|the|previous|next|last) (chapter|section|post|book|essay)\b`, `\bchapter \d+\b`, `\b(as|recall) (we|you) (saw|noted|discussed)\b`, `\bwhich is the (whole|entire) point\b`. Earned cases: one or two genuine signposts in a long document (not one per section); a deliberate callback that pays off an earlier setup. Default to cut — the tic is density. The argument-level cousin (self-recap, re-derivation, scaffolding) is /trim's territory; this entry catches the sentence-level tells.

**Enumerative symmetry (filibuster + tricolon).** A triple is fine; the tell is symmetry by *mold or count*, and it only fires on density. Two subtypes. (a) *Repeated prefix/mold* (the filibuster): "its own X, its own Y, its own Z"; "no X, no Y, no Z"; "the X of A, the X of B, the X of C." The prefix pads rhetoric without meaning; drop it (one prefix up front, then bare items) or vary the mold. (b) *Rule-of-three/five by count*: lists landing on exactly 3 or 5 items with no content reason, or 2+ tricolons clustered in a paragraph ("fast, scalable, and intuitive"). A lone tricolon is genuine; the signal is clustering. Earned prefix cases exist (a meaningful equivalence, e.g. cross-language parallels); default to filibuster until proven otherwise.

**AI vocabulary.** Additionally, crucial, delve, enhance, fostering, garner, highlight (verb), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant. Plus the clusters that hardened through 2026: inflated verbs (elevate, utilize, facilitate, streamline, harness, leverage), dramatic nouns (realm, journey, beacon, cornerstone), and decorative connectors (moreover, furthermore, consequently, hence) gluing sentences that don't need gluing. 2026 index words: *underscore*, *intricate*, *meticulous*, *intricacies* have overtaken *delve* (underscore rose >10,000% in academic corpora). These are low-signal individually; flag, but weight by density, not single occurrence.

**Copula avoidance.** "Serves as", "stands as", "represents", "functions as" instead of "is" or a direct verb. "Serves as the filter" → "is the filter". "Functions as a gate" → "gates".

**Synonym cycling.** Calling the same thing by a different name every sentence to avoid repetition. Just use the same word.

**Participial summary tail.** The marquee grammatical fingerprint of 2026: main clause + comma + present participle that bolts on vague significance. "..., making it easier to...", "..., ensuring...", "..., highlighting the importance of...", "..., enabling...", "..., reflecting...", "..., cementing...", "..., demonstrating...". Models emit these at 2-5x the human rate and they survive paraphrase. Grep: `,\s+(making|ensuring|highlighting|emphasizing|underscoring|reflecting|showcasing|allowing|enabling|contributing|cementing|solidifying|marking|demonstrating|reinforcing)\b`. The tail almost always says nothing the main clause didn't; cut it or promote it to a real second clause.

**Filler.** "In order to" (→ "to"), "it is important to note that" (→ delete), "has the ability to" (→ "can"), "due to the fact that" (→ "because"). "Worth calling out/noting/mentioning" (→ delete, just say it). See also /tighten for broader compression patterns (dead weight, redundant modifiers, nominalizations).

**Staged framing (announce or dramatize instead of state).** The shared tell: a phrase adds theatrical structure without adding reasoning, evidence, or specificity. Single use is style; repeated use is the tic. Test: does it add information or just the author's confidence that information is coming? All subtypes are fixed the same way (drop the frame, state the thing; if the point can't stand without the scaffold, fix the argument):
- *Throat-clearing* (pre-hoc): announces what's coming. "To give you something concrete, here's X", "The short version:", "Here's why", plus editorializing ("The parallel is clear").
- *Deferred conclusion* (post-hoc): explains the argument back. "That told me X", "The takeaway:", "What this means is Z", "The pattern: ...".
- *Suspense label*: a dramatizing colon-label bolted in front of real content. "The catch:", "The kicker:", "The twist:", "Here's the thing:", "The thing is:". The *personal-investment* variant uses emphasis in place of a fixed label, announcing that the author cares before delivering the content: "the thing I haven't stopped thinking about:", "what struck me was", "the part that stuck with me", "here's what I keep coming back to", "the thing that got me". Drop it and state the finding; your investment shows in what you do with the thing. ("But"/"Except" usually does the same work; bare field labels "Repro:", "Fix:" are fine.)
- *Fragment hook*: a self-posed mini-question answered curtly. "The result? Devastating.", "And honestly?".
- *Question framing*: the word *question* standing in for content. "The question is whether X", "the real question is", "the X in question", "X is a separate question", "the second question is", predicate-nouned claims ("it's a definite-assignment question" → "that turns on definite assignment"). Repeated "... question" across a passage is the strongest signal. Treat every non-quoted "question" as a hit unless it is a term of art the domain owns ("question of fact", "the question presented", a named term like "the line-drawing question" built from a court's own words); fix by naming the content ("in question" → delete; "is a separate question" → "is separate"; "the authorship question" → "authorship" or "the authorship analysis").
- *Canned opener*: stock preamble before the noun, hiding at paragraph/section starts. "In today's landscape", "In an era of X", "When it comes to X", "At its core".
- *Aphoristic closer*: a pseudo-profound quotable final turn, often fused with negative parallelism ("Ultimately, the real question isn't what AI can do, it's what we do with it"). The dangerous one: it survives a surface pass.

**Service-desk register.** Chatbot-assistant politeness leaking into prose: eager-volunteering openers ("Happy to X", "I'd be happy to", "I'm glad to", "Feel free to", "Let me know if") and softener offers ("curious to hear/see", "curious whether", "hope this helps", "just my two cents"). They perform helpfulness instead of stating the thing. Replace with a plain offer or claim: "Happy to send a patch" → "I can send a patch"; "curious whether you'd take this" → "would you take this?" or just make the proposal. Sycophantic openers are the chat-native form: "Great question", "You're absolutely right", "Excellent point", RLHF flattery to strip on sight. Strongest tell at the end of a message, where the assistant signs off in-character.

**Hedge stacking.** Stacked qualifiers that defer conviction: "while this may vary, generally speaking, in most cases..."; both-sides framing ("on one hand... on the other...") with no commitment; correlative-crutch density (maybe / kind of / actually / honestly clustered). A single hedge is human; the tell is stacking and refusing a stance. Claude-family prose leans hedge-then-reassure.

**Inflated significance.** "Pivotal moment", "setting the stage", "marks a shift", "indelible mark", "evolving landscape". If the sentence works without the inflation, cut it.

**Monotonous rhythm / low burstiness.** Uniform sentence length and complexity, the statistical signal detectors weight most (humans mix short and long and use fragments). See /readability (prosody) and /flow. Flag here when it reads as an AI pattern, not just a rhythm issue.

**Stock metaphors.** Dead metaphors that add no meaning the sentence doesn't already carry: "shaky ground", "solid ground", "paves the way", "opens the door", "at the end of the day", "tip of the iceberg", "game changer", "double-edged sword", "level the playing field", "move the needle", "circling this problem", and the reflexive *mirror/reflection* image for abstractions ("holds up a mirror to", "a reflection of"). If the sentence works without the metaphor, replace it with the specific claim.

**"Load-bearing" ban.** Never use "load-bearing" figuratively; it is reserved for literal physical load (a wall, a beam). Every figurative hit gets swapped for a term that names the necessity directly, and the replacement must vary across hits so the fix doesn't mint a new tic: "essential", "decisive", "indispensable", "operative", "the crux", "the hinge", "the premise everything downstream rests on", "does the real work", "without it the argument fails", "necessary". Do not substitute a synonym that re-imports the load metaphor ("carries the weight", "bears the argument", "weight-bearing").

**Formatting tells.** Structure substituting for thought, the decisive 2026 surface (word-level prose now reads clean, so shape is where models leak). (a) *Format mismatch*: prose doing a table's job, a side-by-side comparison or parallel "X does Y" claims across 3+ subjects → table ([cognitive fit](https://doi.org/10.1111/j.1540-5915.1991.tb00344.x): argument stays prose, comparison becomes a table). Two items in a sentence is fine. (b) *Bold-lead bullet stack*: "**Header:** one tidy sentence" repeated 3+ times, the defining 2026 visual fingerprint, each bullet looking finished while the reasoning underneath is thin; build the argument in prose. Grep: `^\s*[-*]\s+\*\*[^*]+\*\*:`. (c) *Markdown leakage* (hard flag): literal `**bold**` or stray `---` rules in a channel that doesn't render markdown (email, plaintext); no human types `**` in a Gmail body. (d) *Emoji headers/bullets* (🔹✅🚀): decorative hierarchy; flag on density or channel-mismatch.

**False range / false inclusivity.** Templates that sound comprehensive with no detail: "from X to Y to Z" as a spectrum that isn't on any scale ("from innovation to implementation to cultural transformation"); "whether you're X, Y, or simply Z" reader-inclusivity bait. State the actual span or cut.

## Additions

**Wordplay.** Scan for missed opportunities: terms with double meanings that fit the argument, section titles that could land harder, closing lines that could echo an earlier phrase with a twist. Flag opportunities; suggest specific rewrites. Puns, double entendres, and repurposed jargon all count. Don't force it.

**Arc (foreshadow/recall).** Do the opening and closing connect? The last line should recall the first, reframe the title, or close a loop the reader didn't notice was open. Flat two-word closers ("Small, but real.") assert closure instead of earning it. Exception: a short closer that echoes an earlier line earns its brevity. Also: does the title earn its meaning by the end? For full arc analysis, use /arc-check.

**Unsubstantiated claims.** Flag any factual or causal claim that lacks a citation, a link, or a concrete example. Opinions and arguments are fine without sourcing. Empirical claims ("X% of Y do Z", "studies show", "the data suggests") need a link or a qualifier like "in my experience." If a claim is presented as fact but is actually the author's hypothesis, flag it for reframing.

**Slang and voice injection.** Scan for places where formal phrasing can become casual without forcing it. The test: does the swap sound like a person thinking out loud? If a reader notices the informality, it's forced. Targets: (1) Abstract motivations → rhetorical questions. (2) Multi-clause descriptions → blunt summaries. (3) Jargon → plain equivalent when the formal term isn't doing necessary work. Leave technical terms that carry precision no slang can match. A second pass should find nothing to add.

**First-person presence.** When a post is about the author's project, opinion, or lived experience but uses "I" fewer than ~5 times per 1000 words, the voice has drifted to documentation. Re-personalize: "It produces X" → "I made it produce X"; "The framework requires Y" → "I had to specify Y when I built it." First-person anchors claims to specific events, lets doubts and motivations surface, and puts the writer on the hook for what they say. Skip when the genre is genuinely third-person (analytical reportage, abstract observation); apply when the post is the author's own work, opinion, or thought.

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and the [humanizer](https://github.com/blader/humanizer) skill by @blader.
