---
variant: post
title: "Diffusive Phenomenology"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Consolidation Codec](/consolidate-codec).*

### The decode loop

You are not watching the present. You are watching the output of an iterative refinement process that ran on sensory data from several milliseconds ago.

The brain doesn't render a scene in one pass. Raw signal arrives, and the system runs multiple denoising iterations on the same buffer — each pass sharpening the prediction, integrating priors, resolving ambiguity — until the result is coherent enough to act on. Transformers do it with attention layers, diffusion models with denoising steps. Each pass doesn't add new data. It refines the existing signal using the learned model.

More passes, sharper output, more temporal lag. The tradeoff is universal: **refinement costs latency.** The system trades temporal accuracy for perceptual quality. You're always observing the past. The question is how much past you can afford to process before you need to act.

### GOP override

The [consolidation codec](/consolidate-codec) introduced the GOP — the group of pictures that determines how often the system stores a full keyframe versus a delta. In normal operation, the GOP is long. Most of your Tuesday is P-frames: low resolution, efficiently compressed, reconstructible but not vivid. The scene-change detector fires occasionally when something breaks the pattern.

Focus is manual GOP override. The conscious system says: store more keyframes right now.

This happens automatically in crisis. Fall off a bike and time slows down. Not because the clock changed — because the scene-change detector is screaming. Nothing in the model predicts what's happening next. Every frame is novel. Every frame gets keyframed. The GOP drops to minimum. Maximum I-frame rate.

The memory of the fall is vivid and long because you stored more I-frames per second than normal. In playback, more keyframes means more temporal resolution, which the brain reads as more elapsed time. The sampling rate went up. The clock didn't change. The codec did.

### Subjective time is keyframe density

The entire subjective-time literature maps onto GOP:

**Time flies when you're having fun.** Engaged but predictable. Long GOP, efficient compression, few keyframes. The experience feels fast because the model is good — few scene changes, few forced I-frames. In retrospect, the period collapses: no keyframes to anchor recall.

**Time drags in the moment.** Novel, uncertain, high alertness. Short GOP, many keyframes. High storage cost, high temporal resolution. Each moment feels distinct because each moment is an I-frame.

**A week-long trip feels like a month in memory.** Every day was novel. Short GOP throughout. Dense keyframes survived consolidation. A boring afternoon vanishes for the opposite reason — no I-frames, so nothing anchored the P-frames through eviction.

The standard explanation for these effects is "attention" or "novelty." The codec vocabulary makes it mechanical: keyframe rate determines storage density, storage density determines recall resolution, recall resolution determines subjective duration. No metaphysics required.

### The focus knob

Athletes train to shorten the decode loop — fewer refinement iterations, faster action, lower perceptual quality but faster response. A tennis player returning a serve doesn't have time for a high-quality B-frame. They act on a coarse decode.

Meditation lengthens the decode loop deliberately. More iterations per frame, higher perceptual resolution, deliberate temporal lag. The instruction "pay attention to your breath" is a manual I-frame trigger: force a keyframe on something the default policy would encode as a P-frame.

Flow states are adaptive GOP at its best. The model is so well-matched to the environment that few I-frames are needed — the P-frames are accurate, the predictions hold. Compression is high. The system processes more with less storage. Time flies because the codec is efficient, not because the system is disengaged.

### Sensemaking and scene-change detection

At the individual level, sensemaking is B-frame construction on episodic memory. Something happened. You have a few vivid keyframes. You fill in the narrative between them — constructing a coherent story from sparse observations and bidirectional context. "What actually happened" is the output of a denoising process, not a retrieval.

At the group level, a community shares sparse keyframes (observations, events, data points) and collectively constructs B-frames (narratives, theories, norms) to fill the gaps. The quality depends on the scene-change detector.

A witch hunt is B-frame construction with a locked prior. The denoiser converges on a fixed point that was determined before the data arrived. New I-frames that contradict get rejected as noise. The GOP is infinite — no new keyframes are allowed to break the chain. Every observation confirms the existing narrative because the system refuses to force a scene change.

The scientific method is B-frame construction with forced I-frame insertion. An experiment is a manufactured keyframe — a new observation designed specifically to test whether the generated frames hold up. Falsification is the scene-change detector: if the new I-frame doesn't match the predicted B-frame, force a new GOP. Reset the narrative. Start a new chain.

A denoiser without a scene-change detector is a confabulation engine. It will always produce coherent output. Coherence isn't correctness.

### What this is

Induction. Not proof. The codec vocabulary came from [consolidation](/consolidate-codec), where I/P structure is demonstrated in [working code](https://github.com/SoarGroup/Soar/pull/578). The extensions here — subjective time as keyframe density, focus as GOP override, sensemaking as B-frame construction — are pattern matches. They're specific enough to be wrong, which makes them useful as leads. Whether they're more than leads is an empirical question.

The testable claim: systems with adaptive GOP (variable keyframe rate based on scene-change detection) should produce episodic stores with the same temporal-density patterns that humans report. Dense keyframes during novelty, sparse keyframes during routine, and subjective duration that tracks keyframe count rather than clock time.

---

*Written via the [double loop](/double-loop).*
