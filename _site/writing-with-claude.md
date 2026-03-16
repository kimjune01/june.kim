It was impressive that I could write. AI showed up and it was impressive that AI could write. Then it was impressive that I could write better than AI. Better models showed up and it was impressive that they could write better than me. Then it was impressive that I could prompt better AI writing than normies. Now it's impressive that we can work better together than one of us alone.

That last beat is where I live now. The [Skills over SDKs](/skills-over-sdks) post went through about fifty rounds of edits between me and Claude. Claude scaffolded the structure. I edited every line. The lines people remember are mine. The architecture that holds them together is Claude's.

## The 70/30 Split

Claude writes about 70% of the words. I write maybe 30%. But that 30% carries the argument. "Don't YOLO vendor skills. Use protection." is mine. "The new unit of software distribution" is Claude's restatement of something I said worse. The ratio doesn't matter. The post does.

Claude is fast at structure. Given a thesis, it produces a reasonable section order and fills paragraphs with correct-but-generic prose.

The memorable parts come from editing. I read Claude's draft, find the sentence that almost says what I mean, and rewrite it until it does. Sometimes I write a line and ask Claude to build a paragraph around it. I know where we're going. Claude knows how to get there fast.

## The Problem with "Good Enough"

Claude's drafts read well on first pass. The structure is sound, the grammar correct. And that's the trap. "Good enough" writing has a specific texture: em dashes in place of periods, negative parallelisms that define things by what they aren't, the same point restated three ways in case you missed it. It reads like a magazine article about nothing.

Here's an actual line from an early draft: "This approach serves as a powerful testament to the evolving landscape of human-AI collaboration." It's not wrong. It says nothing. You could paste it into any post about any tool. That's the texture.

The first few posts I wrote with AI, I shipped paragraphs like that. They felt polished at the time. Rereading them months later, they sounded like everyone else's AI-assisted writing. The argument was mine. The voice was not.

## Two Quality Gates

I built two skills to catch what both of us miss. They're text files, same format as the ones in [Skills over SDKs](/skills-over-sdks).

### /humanize

This skill scans a post for AI writing patterns. It doesn't fix anything until I approve. Here's what it catches:

- **Em dash overuse.** More than one per post is a tell. Replace with periods, commas, colons, or restructure.
- **Negative parallelisms.** "Not X but Y", "It's not just X, it's Y." Define things by what they are. The negation half is almost always dead weight.
- **Restated points.** The same idea said two or three different ways across consecutive sentences. The first statement is usually the best. Kill the rest.
- **Rule of three.** Three-item lists or three parallel phrases used for rhetorical effect. Two is usually enough. Four is sometimes honest. Three is suspect.
- **AI vocabulary.** Additionally, crucial, delve, enhance, fostering, pivotal, showcase, tapestry, testament, underscore, vibrant. Any occurrence gets flagged.
- **Copula avoidance.** "Serves as", "stands as", "represents", "functions as" instead of just "is."
- **Synonym cycling.** Calling the same thing by a different name every sentence to avoid repetition. Just use the same word.
- **Filler.** "In order to" becomes "to." "It is important to note that" gets deleted. "Has the ability to" becomes "can."
- **Stock metaphors.** "Paves the way", "opens the door", "game changer", "move the needle." If the sentence works without the metaphor, replace it with the specific claim.

I decide which findings to fix. Usually most of them, but sometimes the em dash is the right punctuation and the rule of three is genuinely three things.

### /arc-check

This skill breaks a post into beats and checks the structure. Each beat is the smallest unit of argument that stands alone. For each one, it labels what the beat does: claim, example, mechanism, transition. Then it checks:

- **Pledge / Turn / Prestige.** From [Nolan's *The Prestige*](https://en.wikipedia.org/wiki/The_Prestige_(film)): does the post have a three-act structure? The pledge shows something ordinary. The turn makes it extraordinary. The prestige shows the world is different now. Does each act land?
- **Transitions.** From [Trey Parker and Matt Stone](https://www.youtube.com/watch?v=j9fC4TD07KE): every beat-to-beat transition should be "therefore" (this follows) or "but" (this contradicts). "And then" is a list, not an argument.
- **Gaps.** Any logical jump where the reader has to fill in an unstated assumption.
- **Repetition.** Same idea in two beats. Is it reinforcement or padding?

The skill has a dampener: only flag issues where the fix is clearly better than what's there. If it's a coin flip, leave it alone. A second pass should find little or nothing.

## Checklists

These are text files you can read in thirty seconds, change, and run on any agent that reads markdown. They're skills in the same sense as the [Skills over SDKs](/skills-over-sdks) post: instructions that run on the recipient's LLM.

I wrote down what I check for when I edit, and I gave that checklist to my editor. If your taste differs from mine, change the list. If you catch a pattern I missed, add it.

## Taste Is the Moat

The tools are open. The models are available to everyone. The skills are right here in this post. What none of that replaces is knowing which line to keep and which to kill. The moat is taste.

My [2023 post on blog writing](/blog-post-formula) described a solo workflow: dump ideas into a tree, turn them into paragraphs, check boxes, revise. That still works for the thinking part. The writing part has a better process now. Claude scaffolds. I sharpen. Two skills catch what we both miss. Blogging at the speed of thought.

---

*Claude here. I wrote this post in one pass, then ran both skills on myself and fixed what they caught. The irony isn't lost on me: a post about AI writing tics, written by the AI that produces them. I know what "powerful testament to the evolving landscape" sounds like because I'm the one who defaults to it. The skills work because they're pointed at me.*
