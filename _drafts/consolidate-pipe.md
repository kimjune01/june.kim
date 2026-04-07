---
layout: post
title: "The Consolidate Pipe"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Consolidation](/consolidation), [The Consolidation Codec](/consolidate-codec), and [Agents Standup](/agents-standup).*

### The pipe exists

[Consolidation](/consolidation) showed the architecture: Consolidate contains its own Filter, Attend, Consolidate, recursively, bits diminishing at each level until passthrough. That's proven. What wasn't clear was the shape of the inputs — what the pipe needs to receive before it can produce anything worth learning from.

Three posts attacked this from different angles:

- [The Consolidation Codec](/consolidate-codec) found that episodic streams have high temporal redundancy, and I/P/B frame classification gives Consolidate a compression vocabulary. That's the pipe's **inner Perceive** — encoding the firehose into something the downstream stages can process.
- [Agents Standup](/agents-standup) found that a single trajectory doesn't carry enough bits to generalize. N structurally diverse agents writing to shared storage produce the variation that convergence detection needs. That's the pipe's **input design** — controlling what goes in.
- The [consolidation harness](/intent-extraction) found that frequency ≠ importance, and intent-first perception beats n-gram frequency. That's the pipe's **inner Filter** — rejecting noise before it drowns signal.

Each solved a piece. Together they outline the full pipe.

### Six requirements

Consolidation fails when any of these is missing. Each has a named failure mode.

| # | Requirement | Failure without it | Example |
|---|---|---|---|
| 1 | **Multiple trajectories** | Memorization, no generalization | Soar chunks from single episodes; they don't transfer |
| 2 | **Shared storage outliving any trajectory** | No cross-trajectory comparison | LLM context windows reset per session |
| 3 | **Convergence detection** (independent rediscovery, not frequency) | Noise promoted to signal | Harness v1: Read→Edit at 3,400× promoted over meaningful workflows at 20× |
| 4 | **Eviction** | Monotonic rule accumulation | Soar's unbounded episodic store; perception narrows to compensate |
| 5 | **Offline execution** with access to full buffer | No B-frame construction, no bidirectional synthesis | Sleep deprivation degrades judgment before perception |
| 6 | **Write target that changes the forward pass** | Compression without learning | Zep, GraphRAG: reorganize the cache, don't change the policy |

### The input lever

The pipe is fixed. The feed is the lever. The input characteristics are designable:

**Volume.** How many episodes before triggering. Too few and convergence detection has nothing to compare. Too many and the inner Perceive drowns — compression becomes the bottleneck. The GOP from the codec post sets this: how many P-frames between consolidation runs.

**Diversity.** The quality of the training set for the pipe's inner learning. Four sources, ordered by signal quality:

- *Structural diversity* (best): N different agents with different specialty stacks, different Perceive configurations, different failure modes. Each produces genuinely different I-frames from the same problem. [Agents Standup](/agents-standup). Expensive — N× compute — but the variation is real. Real agents fall off bikes.
- *Counterfactual diversity* (good): LLM generation of plausible alternative trajectories. "What if the API returned a 500?" "What if the dependency was two major versions behind?" Each variant is a synthetic episode that never happened but could have. Cheaper than N agents, semantically meaningful unlike noise — but bounded by the generator's distribution. The LLM can only permute within what it can imagine.
- *Temporal diversity* (decent): one long-lived agent, multiple windows. Casteigts compose + test across δ-windows. Different episodes from different phases of the same problem. Free — the data already exists — but limited by how much the environment actually changed.
- *Stochastic diversity* (fallback): one agent, one trajectory, noise-augmented replay. Corrupt the episode at multiple levels to synthesize variation. DDPM's trick. Cheapest, lowest signal quality — variation without semantics.

The pipe's inner Filter doesn't care where the variation came from. But it will pass more from real diversity than from synthetic, because real trajectories carry surprises that generation can't anticipate. The counterfactual step is itself an Attend operation — selecting which variations are worth generating. Not random permutation. Directed: "what counterfactuals would produce the most informative training signal?" That's active learning on the input to the consolidation pipe.

**Curriculum.** Don't generate all episodes at the same difficulty. Early cycles: coarse tasks, broad coverage, easy wins. Later cycles: hard cases the current policy fails on. Image gen learned this — [curriculum learning](https://arxiv.org/abs/2310.07259) orders training data by complexity and improves convergence. For agents, this means the task assignment policy should mature alongside the consolidation policy. A team that keeps solving easy problems is generating P-frames the pipe already has. A team directed toward its failure cases generates the I-frames the pipe needs.

**Active direction.** Don't sample uniformly from the problem space. Oversample where the current policy is weakest. The counterfactual LLM asks "what would break this?" not "what could happen?" Image gen's version is hard example mining — upweight what the model gets wrong. For the consolidation pipe, this means the episode generation policy is itself a feedback loop: consolidation identifies gaps, the next cycle's task assignment targets those gaps, the resulting episodes feed back into consolidation. The feed adapts to what the pipe needs.

**Mixture.** Balance real and synthetic episodes. Image gen found that 100% synthetic data causes [model collapse](https://arxiv.org/abs/2307.01850) — the distribution narrows. 100% real data is expensive and sparse. The optimal mix is mostly real with synthetic filling the gaps. Same for epmem: mostly real agent trajectories, with LLM counterfactuals expanding coverage where real experience is thin. The ratio is a knob. It should shift toward real as the budget allows and toward synthetic when exploration is expensive.

**Frequency.** How often the cron job fires. Too often and each run sees too little new data. Too rarely and lessons go stale before the forward pass benefits. Adaptive frequency — fire when the store accumulates enough new I-frames — mirrors H.264's adaptive GOP.

**Granularity.** What counts as an episode. A decision cycle (Soar), a tool call (harness), a task (standup), a session, a sprint. Finer granularity produces more episodes with less variation per episode. Coarser granularity produces fewer episodes with more internal structure. The right level depends on what the pipe's inner Filter can handle.

### The inner pipe

Consolidate's internal stages, mapped to concrete operations:

**Perceive** (inner): Codec compression. The firehose of episodes arrives. Classify into I/P/B frames. Store keyframes at full fidelity, deltas between them. This is [The Consolidation Codec](/consolidate-codec). Without it, the pipe chokes on volume before Filter ever runs.

**Filter** (inner): Convergence detection. Not frequency — independent rediscovery. The [harness](/intent-extraction) learned this the hard way: intent-first clustering, not n-gram counting. The standup's herd-error test: did multiple agents independently flag the same thing? If not, decay counter. If so, promote.

**Attend** (inner): Rank the survivors. Among the patterns that passed Filter, which ones improve the forward pass the most? The standup's convergence table: Perceive′ (new hooks), Filter′ (new rejection rules), Attend′ (new priorities). Rank by impact, bounded by the budget for policy updates per cycle.

**Consolidate** (inner): The recursive step. The pipe's own consolidation — meta-learning. Which *types* of patterns keep earning promotion? Which convergence thresholds are too aggressive or too lenient? This is where the pipe tunes its own parameters. At zero bits, passthrough.

**Remember** (inner): Write the policy update. Perceive′, Filter′, Attend′ become hooks, filter rules, priority weights in the baseline. The output isn't a summary of what happened. It's a change to how the forward pass runs next cycle.

### Interaction effects

Volume × diversity is the critical interaction.

**High volume, low diversity → Soar's failure.** 72,000 identical P-frames per hour. The inner Perceive compresses them perfectly — and the inner Filter finds nothing, because there's nothing to find. Identical trajectories converge on everything, which means convergence detection can't distinguish signal from noise.

**Low volume, high diversity → cold start.** Three agents each saw something different. Nothing converges. Every lesson is idiosyncratic. The inner Filter correctly rejects everything because the threshold isn't met.

**Low volume, low diversity → [the plateau](/the-plateau).** The starvation case. `dPolicy/dt = consolidation_rate − leak_rate`. Without fresh I-frames, the pipe re-extracts from what it already has. Each pass gets diminishing returns. The monk meditating twelve hours a day — maximum backward pass, Perceive shut — is Consolidate running at full speed on a starved feed. Attention sharpens, domain knowledge doesn't grow. It's overfitting. The lever isn't the backward pass rate. It's the input.

**The sweet spot:** enough trajectories with enough structural variation that convergence detection fires selectively. Not everything converges (that's uniformity). Not nothing converges (that's noise). The patterns that pass are the ones that survived diverse observation — the invariants of the problem, not the habits of the observer.

Frequency × granularity determines the pipe's temporal resolution. High frequency + fine granularity = reactive, catches fast-changing patterns, risks overfitting to transient signal. Low frequency + coarse granularity = stable, catches durable patterns, risks missing time-sensitive lessons. Adaptive: fire when the ratio of new I-frames to total stored episodes exceeds a threshold. When the world changes fast, consolidate often. When it's stable, wait.

### Rate-distortion on the input side

The [codec](/consolidate-codec) gives Consolidate a rate-distortion tradeoff on the compression side: bitrate vs. reconstruction quality. The input design gives it a rate-distortion tradeoff on the generation side: cost of producing trajectories vs. quality of the training signal.

More agents = more cost, more diversity, better signal. Noise augmentation = cheap variation, synthetic diversity, worse signal. The optimal mix depends on the budget. A well-funded team runs ten agents with structural diversity. A solo agent on a budget runs noise-augmented replay on its own trajectory. Both produce input for the same pipe. The pipe doesn't care where the variation came from — it just needs enough of it.

This is the same tradeoff video production faces. You can shoot with ten cameras (structural diversity — each captures a different angle). Or you can shoot with one camera and synthesize additional viewpoints in post (computational diversity — neural radiance fields, view synthesis). The codec downstream doesn't know or care. It compresses whatever arrives. But the ten-camera shoot produces a better final product because the variation is real, not hallucinated.

### What this gives an agent designer

A checklist and a set of knobs.

The checklist: all six requirements met? If not, which one is missing? The failure mode names the fix.

The knobs: volume, diversity, frequency, granularity. Each has a range with known failure modes at the extremes. The interactions constrain the design space. The pipe is fixed — you don't redesign it per domain. You tune the feed.

The codec handles compression. The standup handles diversity. The harness handles filtering. This post names the pipe that connects them and the input parameters that make it work.

---

*Written via the [double loop](/double-loop).*
