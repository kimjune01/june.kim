<!-- NOTE TO JUNE: revise into your own voice and verify every number against WORK_LOG.md /
RESULTS.md before posting. The "I drafted this with AI help and rewrote it" line is only honest
if you actually rewrite it. No links in a first post — repo/DOI go in the FIRST COMMENT block.
Title swappable. The arc traces the real worklog: two false summits, both killed by your own controls. -->

# I tried to reverse-engineer the new-user filter, and talked myself into two wrong answers first

**Epistemic status:** Discovery-stage, and a confession of two reversals. I reached an exciting conclusion, then a second one, and my own controls killed both. The claim I'm left with is smaller and I think solid; one sub-result is a non-significant artifact I'll show you. Code, data, the preregistration, and a log of every wrong turn are in the first comment.

I tried to post here for the first time in March. The submission was a write-up of a context-compaction idea, and it was mostly a pointer to the post and its repo. A moderator rejected it, and the reason stuck with me:

> submissions from new users that are mostly just links to papers on open repositories (or similar) have usually indicated either crackpot-esque material, or AI-generated speculation. It's possible that this one is totally fine.

He added that readers here won't follow a stranger's link without a reason to, so the format was discouraged without a summary or excerpts. I read that as a register problem, rewrote the thing looser, and resubmitted. A second moderator rejected that one too, for unclear writing and as borderline spam, with a parenthetical that turned out to be the whole story for me later: new-user content written with AI assistance is also rejected. I decided the lesson was tone, that somewhere between stiff and chatty was a register a newcomer is allowed and I'd missed it twice. All I'd wanted was to share a few ideas about making AI reason more carefully.

But the rejections had already told me the real thing, and it was not about tone. Both moderators were saying, under the surface, that they could not afford to read my ideas closely enough to tell whether they were any good, or AI-generated, or crackpot, so they fell back on cheap proxies: a link from an unknown name, prose that reads as machine-made. One of them said it outright, that it was possible my post was totally fine, but checking wasn't worth the time. The gate was not judging my ideas. It could not. It was reading cheap signals that stand in for judging them. So rather than guess at the register a third time, I got curious about a different question: what can a gate that cannot afford to verify actually read, and can it really tell AI-mediated writing from the real thing? My first instinct was to ask for the rules and build a checklist of what LW writing looks like. That instinct is exactly backwards. A checklist is a thing you optimize against, and the moment you name the features you've handed the answer key to the adversary, including yourself. So instead I built a lineup: show a detector several real LW paragraphs and one candidate, ask which is the odd one out, many times over. It has to induce the pattern from examples; the criteria stay implicit.

I put my own rejected post through it first. The result wasn't uniform. The framing paragraphs and the conclusion lit up red; the technical middle, the part that just explained the mechanism, read as native. The "I'm writing a post" parts got flagged. The "here is how the thing works" parts didn't. First hint that the filter wasn't reading tone evenly. It was reading which paragraphs were doing work.

Then I fed it raw, unedited AI prose on a canonical alignment topic, mesa-optimization. I expected it to light up. It slipped through near the floor. **First summit:** the filter isn't detecting AI at all, it reads topic-fit. Write on something the community cares about and you're in, no matter who or what wrote it. That felt like the answer, and it was a relief, because it meant the gate was about substance of topic, not provenance.

A second result seemed to hand me a cheap fix on top of it. I took one of my drafts and added the visible furniture of an LW post: an epistemic-status line, footnoted caveats, the nested parentheticals. Detection dropped by what looked like six orders of magnitude. Rewriting the topic made it worse, and laying on rationalist vocabulary made it worse still (it read as caricature), but structure, structure was the lever. **Second summit:** I had my workflow. Draft, add the LW furniture, pass.

Both were wrong, and my own checks are what killed them.

I ran a harder test: take one paragraph and revise it against the detector fourteen times, rotating what I changed each round, polish, roughness, add the markers, strip the markers, make it personal, make it strange. All fourteen got caught. Then the control: a real LW paragraph I had never used as a candidate, through the same gauntlet. It passed six times out of six. Whatever the detector reads, it was not the surface I kept editing.

That sent me back to the two summits, and both fell.

"It reads topic-fit, not provenance" was a misread of the word *passes*. The AI prose on mesa-optimization scored below the fail threshold, but it sat well above the floor that real LW writing lands at. It was being caught, just more quietly, because the canonical topic made the detector less confident. Below the bar is not the same as in-distribution. I had confused "not flagged hard enough to fail" with "looks real."

"Structure is the lever" did not survive the arithmetic. The six-orders-of-magnitude drop, once you undo how I was scoring it, was a ten-out-of-a-hundred shift on one post. The actual test on that pair comes out at p=0.13. Not significant. And I had generated each variant from the previous one, so the "structure" version had simply been through fewer rounds of AI rewriting than its neighbors. That's a confound, not a finding. The costume never worked. I had been measuring my own editing pipeline and calling it a property of prose.

What's left after both summits collapse is smaller and more stubborn, and I'll claim it at the size the evidence supports. In my setup, the detector caught my pipeline's prose and kept catching it through every edit I'd reach for to disguise it, while a real LW control paragraph passed. I cannot separate "it detects AI in general" from "it detects the fingerprints of my particular generate-and-revise loop," so the honest claim is the narrow one: naive surface revision did not launder my AI-mediated prose past this detector, and the harder I pushed, the worse I did.

The practical upshot still reverses the plan I started with. I came in wanting the workflow "draft, run the gate, revise until it passes." I could not find it. The obvious version failed, because the signal the gate read was not on the surface I was editing. Maybe a cleverer loop exists; what I can report is that the naive one did not work, and the move that did was writing native from the start.

One thread I'm still pulling, offered as a conjecture with a hole in it. If a gate reads substance instead of surface, then "edit until you pass" stops being a cheat, because the only edit that passes is one that makes the work better. Style you can push sideways forever; substance moves one way. When I ran the writer against the gate over rounds, the two seemed to settle rather than escalate. But I have not measured "better" with anything independent of the gate I was optimizing against, and until I do that sentence is a hypothesis, not a result. I'm naming the hole on purpose.

There is a deeper limit under all of this, and it is the one that matters most, because it is not about my sample size. A detector only ever sees what it catches. Prose that genuinely slips past is, by definition, the prose it never flags, so it never shows up as a data point. That is why I can tell you the obvious revision loop failed but cannot tell you no loop works: a workflow that produced undetectable prose would be silent, indistinguishable from someone just writing native. You count the bullet holes in the planes that came back. The blind spot shrinks if you add independent checks, a second detector, human readers, whether the post actually gets upvoted, but it never closes, because prose that passes every check at once still looks exactly like the real thing to every check at once. So a gate can report what it caught and never what it missed, and anything that passes is, to the gate, identical whether it earned its way in or laundered its way in. The only thing that can see into that blind spot is a measure from outside the gate, and even that only narrows it. That is the same reason a model that learns to pass a safety eval is invisible to the eval: certification from a gate is, in the end, trusting silence.

Last, since this is a post about telling what wrote something, I will tell you how this one was made rather than let you wonder. The ideas, the experiments, and the writing are mine; I used a model to pressure-test the argument and help organize it, and I rewrote and verified every line and vouch for all of it. I am saying so because a post about provenance that hid its own would be the exact failure it describes, and because your own policy asks for it. You should not take my word for any of this regardless: the checkable part is in the first comment, the code, the data, the preregistration, and the log of every wrong turn above, including the two I walked you through. Re-run the lineup. If I am wrong, you will find me wrong in your own hands.

I'm still new here, and I expect this post gets judged by the same filter that turned away the first two. After all of it, that seems exactly right.

---

## FIRST COMMENT (post right after; links allowed here)

Code, data, preregistration, and the full results, including the worklog of every wrong turn:

- Repo: github.com/kimjune01/lesswrong-voice-gate
- Archived (DOI): doi.org/10.5281/zenodo.20765320
- The detection pipeline and LLM-writing policy this responds to are linked in the repo's RELATED-WORK file.

Third-party LessWrong and Hacker News samples are referenced, not redistributed (data/SOURCES.md); they remain their authors' copyright. Don't take my reading on faith. Re-run the lineup.
