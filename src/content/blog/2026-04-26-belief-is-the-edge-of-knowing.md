---
variant: post-medium
title: "Belief is the edge of knowing"
tags: cognition, reflecting
image: "/assets/minesweeper-guessing.png"
---

*Part of the [cognition](/cognition) series.*

<figure style="max-width:300px; margin:1em auto;">
<img src="/assets/minesweeper-guessing.png" alt="Minesweeper board with multiple 50:50 guesses. The blue square is 20:80, does not touch a 50:50, and is on an edge — it might be an opening." style="width:100%; display:block; image-rendering:pixelated;"/>
<figcaption style="font-size:13px; color:#666; margin-top:0.5em;">Multiple 50:50 guesses. The fifth strategy opens a "random" square. On Expert the blue square is 20:80, does not touch a 50:50 and is on an edge so might be an opening. <a href="https://minesweepergame.com/strategy/guessing.php"><strong>Source</strong></a>.</figcaption>
</figure>

When I say *'I know my keys are in my pocket,'* I don't mean it in the philosophical sense. I mean: I'm confident enough to reach in without bracing for absence. If they're not there, I update without fuss. The "knowledge" was always belief past a threshold.

This is how cognition works, and the philosophical picture (Knowledge as [Justified True Belief](https://en.wikipedia.org/wiki/Justified_true_belief), distinct from mere Belief) gets it backwards. There is no tier above belief. There's only confidence, varying continuously, and the threshold for calling something "knowledge" is set by what you're willing to act on given the stakes. Cognition architectures (cogarch) who conflate the two bind themselves in contradiction.

### No boolean truth

The line between knowledge and belief runs from Plato through Gettier, never settled. Fiction makes this explicit. In [Blade Runner](https://www.youtube.com/watch?v=NoAzpa1x7jU), Deckard reaches for a memory he can't verify. His reality, though false, was a useful projection. If you've played Minesweeper enough, you'll come across covered squares of probabilistic outcomes. You click the square with the least lethal probability. Both Deckard and your Minesweeper clicks act on confidence past a threshold.

All cognition operates on lossy projections. The retina projects 3D into 2D into spike patterns. The tokenizer projects characters into integers into vectors. Every modality strips dimensions and loses resolution. All access to reality is mediated. [Plato's prisoners](https://en.wikipedia.org/wiki/Allegory_of_the_cave) had the shape right. The modern version drops the exit: no escape from the cave, only different projections, some more useful than others. Pretending otherwise is playing omniscience.

Lossy projections cannot yield boolean truth about what they project. Within a projection's own basis, *'this pixel is red, by this color model'* can be definitively true. But *'the world contains red'* is a claim about world-as-projected, not world-as-such. There is no world-as-such available; only world-as-projected. *Truth is internal-to-projection.*

If so, any claim grading itself against ground truth is grading against a fiction. The [pragmatist tradition](https://en.wikipedia.org/wiki/Pragmatism) saw this. [James](https://en.wikipedia.org/wiki/William_James), [Peirce](https://en.wikipedia.org/wiki/Charles_Sanders_Peirce), [Dewey](https://en.wikipedia.org/wiki/John_Dewey) made truth inseparable from action. [Correspondence theory](https://en.wikipedia.org/wiki/Correspondence_theory_of_truth) gave way to what works. A claim works or it doesn't. Belief is what you'd act on. Knowledge is belief past a stakes-dependent action threshold. *Knowledge is contextually indexed.* The same belief is knowledge in one context and mere belief in another.

[Ramsey](https://en.wikipedia.org/wiki/Frank_Ramsey_(mathematician)) put this operationally: a belief is what you'd bet on, and its strength is the odds. The threshold for calling it "knowledge" is the odds at which you'd bet, given the stakes. Low stakes: act on weak beliefs. High stakes: demand stronger ones. *'I know my keys are in my pocket'* crosses the action threshold for low-stakes motion. If your life depended on the answer, you'd downgrade to *'let me check.'*

### What breaks without it

A cogarch built on this epistemology has specific structural requirements. Each earns its place by what breaks if it's missing.

<table style="max-width:700px; margin:1em auto; font-size:14px;">
<colgroup><col style="width:18em"><col></colgroup>
<thead><tr><th style="background:#f0f0f0">Requirement</th><th style="background:#f0f0f0">Consequence of not implementing</th></tr></thead>
<tr><td>Non-boolean <a href="https://en.wikipedia.org/wiki/Credence_(statistics)">credence</a></td><td>Updates too coarse, system crashes on contradictions</td></tr>
<tr style="background:#f8f8f8"><td>Confidence must be preserved across processing stages</td><td>Graded beliefs become boolean at consolidation, confident confabulation</td></tr>
<tr><td>Calibration</td><td>Confidence diverges from empirical frequency, decisions weighted wrong</td></tr>
<tr style="background:#f8f8f8"><td>Knowledge and belief must not have categorically different epistemic status</td><td>Two-tier brittleness, upper tier breaks first under contradiction</td></tr>
<tr><td>Action commitment must scale with stakes</td><td>Same belief commits the same regardless of risk, catastrophic over-commitment</td></tr>
<tr style="background:#f8f8f8"><td>Beliefs must be revisable</td><td>Contradictions accumulate, no learning from being wrong</td></tr>
<tr><td>Beliefs must track environmental change</td><td>Stale knowledge, eventual mis-prediction</td></tr>
<tr style="background:#f8f8f8"><td>Perception must be testable</td><td>Perception cannot be calibrated; confidence flatlines and drift goes undetected</td></tr>
<tr><td>Perception must be actively tested over time</td><td>Confidence stops elevating once active probing stops; calibration locks at the last-probed state</td></tr>
<tr style="background:#f8f8f8"><td>Second-order beliefs must be testable</td><td>System trusts its own meta-claims uncritically, blind to introspection failure</td></tr>
</table>

Each failure mode is specific. Anything removable without consequence is a design choice, not a requirement. The two perception rows look redundant but aren't: the first demands that a test for accuracy exist; the second demands it actually fire. Perception that *could* be tested but never is degrades as silently as untestable perception.

### LLMs fail the table

An LLM alone produces text with uniform apparent confidence regardless of underlying uncertainty. No calibration layer, no confidence propagation through inference, no distinction between *'I'm certain'* and *'I'm completing the next plausible token.'* The field calls this "[hallucination](https://en.wikipedia.org/wiki/Hallucination_(artificial_intelligence))." The accurate term is [**confident confabulation**](https://en.wikipedia.org/wiki/Confabulation): output delivered with high apparent confidence, ungrounded in currently available evidence.

It doesn't disqualify LLMs as cognition, but rather, a diagnosis. The LLM is a powerful component, but one without the surrounding architecture the table demands. Confidence isn't carried across the inference chain, so graded beliefs become boolean at the output layer. The system can't say *'I'm at 0.3 on this'* because its action threshold isn't stake-indexed; it's fixed at *'produce the next plausible token, always.'* To qualify, the model should be accompanied by confidence propagation in its output.

### Knowledge is a derived predicate

Instead of *'I know X,'* a cogarch built this way outputs *'I believe X with confidence `c`, and at the prevailing stakes, `c` exceeds the action threshold.'* Knowledge becomes a derived predicate: a label applied to belief that has crossed a context-dependent line.

Humans don't verbalize confidence levels. We hold them and act on them. The commitment lives internally: confidence propagates everywhere, stakes parameterize the threshold, and "knowledge" falls out when confidence exceeds it.

You reach into your pocket. The keys are there. Was that knowledge, or was that a belief that stopped updating?
