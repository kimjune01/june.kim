---
variant: post
title: "Diffusive Phenomenology"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [The Consolidation Codec](/consolidation-codec).*

You are not watching the present. You are watching the output of an iterative refinement process that ran on sensory data from [a few hundred milliseconds ago](https://pubmed.ncbi.nlm.nih.gov/11074267/).

The brain doesn't render a scene in one pass. Raw signal arrives, and the system runs multiple denoising iterations on the same buffer until the result is coherent enough to act on. Transformers do it with attention layers, [diffusion models](https://en.wikipedia.org/wiki/Diffusion_model) with denoising steps. Each pass doesn't add new data. It refines the existing signal using the learned model.

More passes, sharper output, more temporal lag. At the limit, *refinement costs latency.* You're always observing the past. How much past can you afford to process before you need to act?

### Focus overrides the GOP

The [consolidation codec](/consolidation-codec) introduced the **GOP** — the **[group of pictures](https://en.wikipedia.org/wiki/Group_of_pictures)** that determines how often the system stores a full keyframe versus a delta. In normal operation, the GOP is long. Most of your Tuesday is [P-frames](https://en.wikipedia.org/wiki/Video_compression_picture_types): low resolution, efficiently compressed, reconstructible but not vivid. The [scene-change detector](https://en.wikipedia.org/wiki/Shot_transition_detection) fires when something breaks the pattern.

Focus is manual GOP override. The conscious system says: store more keyframes right now.

This happens automatically in crisis. Fall off a bike and time slows down. Not because the clock changed — because the scene-change detector is screaming. Nothing in the model predicts what's happening next. Every frame is novel. Every frame becomes a keyframe. The GOP drops to minimum. Maximum I-frame rate.

The memory of the fall is vivid and long because you stored more I-frames per second than normal. The sampling rate went up. The clock didn't change. The codec did.

### Subjective time is keyframe density

The entire subjective-time literature maps onto GOP:

*Time flies when you're having fun.* Engaged but predictable. Long GOP, efficient compression, few keyframes. It feels fast because the model is good — few scene changes, few forced I-frames. In retrospect, the period collapses: no keyframes to anchor recall.

*Time drags in the moment.* Novel, uncertain, high alertness. Short GOP, many keyframes. High storage cost, high temporal resolution. Each moment feels distinct because each moment is an I-frame.

*A week-long trip feels like a month in memory.* Every day was novel. Short GOP throughout. Dense keyframes survived consolidation. A boring afternoon vanishes for the opposite reason — no I-frames, so nothing anchored the P-frames through eviction.

### Shorten or lengthen the loop

Athletes train to shorten the decode loop — fewer refinement iterations, faster action, lower perceptual quality but faster response. A tennis player returning a serve doesn't have time for a high-quality B-frame; they act on a coarse decode.

Meditation lengthens the decode loop deliberately. More iterations per frame, higher perceptual resolution. "Pay attention to your breath" is a manual I-frame trigger: force a keyframe on something the default policy would encode as a P-frame.

[Flow states](https://en.wikipedia.org/wiki/Flow_(psychology)) are adaptive GOP at its best. The model is so well-matched to the environment that few I-frames are needed — the P-frames are accurate, the predictions hold. The system processes more with less storage. Time flies because the codec is efficient.

### Sensemaking runs the encoder late

Everything above happens in real time: encoding, keyframing, compression. Sensemaking happens after — promoting P-frames to I-frames retroactively, using context you didn't have in the moment.

Something happened. You have sparse P-frames from real time. Sensemaking goes back and keyframes some of them: reconstructs full snapshots from fragments, locks in "what actually happened." The result feels like memory retrieval. It's memory encoding, running late.

At the group level, a community shares sparse observations and collectively decides which ones to keyframe. The quality depends on the scene-change detector.

A witch hunt locks which P-frames get promoted. The prior was fixed before the data arrived. Contradicting observations get rejected as noise. Every frame confirms the narrative because the system refuses to force a scene change.

The scientific method manufactures observations to force the promotion. An experiment is a synthetic keyframe that tests whether the existing frames hold up. [Falsification](https://en.wikipedia.org/wiki/Falsifiability) is the scene-change detector: if the new keyframe breaks the chain, force a new GOP. Reset the narrative.

Sensemaking without a scene-change detector is a [confabulation](https://en.wikipedia.org/wiki/Confabulation) engine. It will always produce coherent output. Coherence isn't correctness.

### What this is

Induction. Not proof. The codec vocabulary came from [consolidation](/consolidation-codec), where I/P structure is demonstrated in [working code](https://github.com/SoarGroup/Soar/pull/578). The extensions here (subjective time as keyframe density, focus as GOP override, sensemaking as retroactive keyframing) are pattern matches. They're specific enough to be wrong, which makes them useful as leads. Whether they're more than leads is an empirical question.

The testable claim: systems with adaptive GOP (variable keyframe rate based on scene-change detection) should produce episodic stores with the same temporal-density patterns that humans report. Dense keyframes during novelty, sparse keyframes during routine, and subjective duration that tracks keyframe count rather than clock time.

You're still watching the replay.

---

*Written via the [double loop](/double-loop).*
