---
variant: post
title: "Red-Teaming Human-Likeness"
tags: methodology
---

How do you write prose that does not trip a human's bot alarm?

For me, the practical genre was pull request prose. When I was developing
`sweep`, the coding pipeline that turns issues into PRs, it had to write bodies
that blended into a maintainer's inbox. Not "sound human" in the abstract.
Sound right here: this repo, this maintainer, this template.

Before I understood that, I tried to stuff as much attestation into the PR body
as I could. Reasoning traces, test receipts, dead hypotheses, links to the
investigation graph. I wanted the maintainer to see the work. Instead I made
the prose illegible to the human who had to review it.

The uncomfortable lesson from the [sweep hypothesis graph](https://github.com/kimjune01/sweep/blob/master/HYPOTHESIS_GRAPH.md)
was that the failure usually was not code or reason. It was writing style. A
sound PR could still look like a drive-by bot: wrong title shape, too much
trace, diff summary instead of root cause, response cadence that made the
reviewer ask whether there was a human in the loop. The audit trail belonged in
the artifacts; the PR body had to be the human interface. So before opening a
PR, `sweep` learned to compare its title and body against recently merged PRs
from the same repo, then rewrite when the candidate stuck out.

What was I actually testing? Chameleon.

Chameleon took me a while to feel. I kept wanting the judge to be the clever
part, but the useful trick was simpler: don't tell it what to look for. The
tempting move is to write a checklist: ban em dashes, demand "why not what,"
require receipts, forbid generic phrasing. But once the checklist is visible,
the detector becomes a style guide for the thing it was supposed to catch. A
lineup is harder to game because the standard is local. The question changes
from "does this have human features?" to "does this belong with these five
nearby humans?" The judge has to infer the local shape fresh each round.

That worked well enough on PR descriptions to tempt the larger question: could
the same method red-team human-likeness in long-form prose?

I wanted to post to LessWrong, and one of my past submissions had been flagged
as "not obviously not spam." I wanted criteria for my own human writing to pass
its AI-slop filter. LessWrong was the hardest public taste gate I knew how to
test. Its public
[LLM-writing policy](https://www.lesswrong.com/posts/KXujJjnmP85u8eM6B/policy-for-llm-writing-on-lesswrong)
names the moderation side: meet the site's quality standard, avoid stereotypical
assistant prose, and have a human vouch for it. That is closer to a maintainer
review than an English class.

So I tried the same shape again.

The procedure stayed simple. Put one candidate paragraph next to five real
LessWrong paragraphs. Match openings against openings, evidence against
evidence, conclusions against conclusions. Shuffle the labels. Ask which one is
least like the others. Score only the choice, then read the reason after the
fact.

The first thing I learned was that "this sounds unlike LessWrong" is too coarse
to help. Unlike how? Topic? Structure? Register? Community texture?

I changed one thing at a time. Reframe the topic through a LessWrong-native
lens. Add familiar structure: epistemic status, footnoted caveats, parenthetical
asides. Shift the register. Real LessWrong paragraphs had to pass. Obvious
outsider prose had to fail. Clever prompts mattered less than controls.

Then came the part that felt most like writing PR prose: the revise loop.

A candidate paragraph went into the same lineup repeatedly. After each failure,
I used the reason to revise it. Too polished? Make it rougher. Too generic? Add
lived detail. Missing community texture? Add links, names, edits, asides, and
local jargon. Too marker-heavy? Strip it back. Try few-shot examples. Stop
inventing toy claims and use real research.

The candidate kept getting caught.

At first, I wanted that to mean I had found a strong AI prose detector. Surface
mimicry failed. Few-shot LessWrong imitation failed. Even LLM articulation of
real human research failed.

Maybe the detector looked strong because I kept feeding it things that were easy
for it to hate.

The controls broke the story.

A genuine human paragraph, written years before modern LLMs, also got flagged
as having "AI cadence" when it sat outside the LessWrong distribution. A fresh
real LessWrong post from outside the 30-post pool got flagged four times out of
five. More outsider LessWrong posts pushed the false-positive rate near three
quarters. Informal, anecdotal, specific prose passed more often; formal,
polished, abstract prose got called AI-like.

What kind of AI detector flags a human paper introduction as AI? What kind of
human-likeness test passes casual in-group prose and fails formal outsider
prose? Maybe one that was never testing humanity in the first place.

That was the lesson I needed the red team to teach me. You do not stop when the
detector catches the thing you hoped it would catch. You keep going until it
catches the wrong thing.

The diagnosis I ended up trusting was narrower: the detector was reading
stylistic distance from a small in-group pool. The axes were polish, community
register, and obvious AI-meta cues. Those correlate with LLM output, but they
are not authorship. They also catch formal academic human prose, outsider prose,
and legitimate posts that lack the local texture of the sample pool.

The method that got me there was simple in retrospect: hide the rubric, match
local examples, perturb one thing at a time, and keep hunting false positives
after the detector starts looking good. In that sense, the red team worked. It
did not give me the detector I wanted. It told me what the detector was actually
measuring.

That last part is the hard part. Once a detector catches the thing you dislike,
you want to believe it. The red team has to keep asking the socially awkward
question: who else does it catch?

This loops back to the PR problem in a way I still find uncomfortable. Blending
in is real. Maintainers have local norms, and violating them creates work for
the person whose attention you are borrowing. I still want `sweep` to match the
repo's voice and read the official policy files before touching the maintainer's
inbox. That is part of being a polite guest.

But "does this blend in?" is not the same question as "was this written by a
human?" The first is manners and context. The second is an authorship claim. A
lineup can help with the first while badly overclaiming the second.

Human-likeness is not a property I now trust a small-pool detector to measure.
Ask whether text looks like the humans already in your pool and you mostly
measure conformity. You will catch machine text because machine text is polished
and generic. You will also catch humans who are polished, formal, adjacent, new,
or simply not from the local dialect.

The funny part is that this is also why public taste gates are fragile. If the
positive samples and official policy are public, a motivated writer can learn
the local shape. LessWrong's later
[policy update](https://www.lesswrong.com/posts/nQWavk9mnwcv6ScMR/new-lesswrong-editor-also-an-update-to-our-llm-policy/)
made that explicit from another angle: the problem was not just AI use, but the
recognizable style of AI-assistant prose. The gate does not disappear; it turns
into a writing curriculum. By the end, I had not built a clean AI detector. I
had built a description of what makes an essay feel situated, legible, and worth
reading.

How can you tell if this post was written by a human or a bot?

Does it matter?
