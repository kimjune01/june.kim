---
variant: post-medium
title: "Consolidation Codec"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Consolidation](/consolidation) and [Prescription: Soar](/prescription-soar).*

### The contract

Consolidate reads from the store, finds patterns across episodes, and writes policy changes back to the substrate. Its contract is: many episodes in, fewer parameters out. The episodes shrink; the policy improves. Every cycle that adds experience without consolidating it grows the store linearly.

Soar hit this wall. 72,000 episodes per hour, unbounded. Retrieval cost scaled with total count. The [diagnosis](/diagnosis-soar) was clear: the forward pass worked, but Consolidate was missing for episodic and semantic memory. The stores grew without bound and perception narrowed to compensate — a clogged drain forcing the valve shut.

Every system that stores episodes faces the same curve. Soar built [chunking](https://en.wikipedia.org/wiki/Soar_(cognitive_architecture)). Transformers use gradient descent. Zep builds temporal knowledge graphs. Each one works. None share vocabulary.

### The stream

Look at what Consolidate actually receives. Episodes arrive in sequence. Each episode is a snapshot of state paired with the policy that produced it. Between consecutive episodes, most of the state is identical. The policy changes even less frequently — it updates only when Consolidate itself runs, which is offline, periodic, asynchronous. A deployment that handles ten requests is ten episodes. Nine of them share the same policy and nearly the same state.

This is a stream with high temporal redundancy. Video codecs compress exactly this kind of signal — consecutive frames share most of their content and the interesting information lives in the deltas.

### I-frames, P-frames, B-frames

A video codec doesn't store every frame at full fidelity. It classifies frames into three types:

**I-frame** (intra-coded): a complete snapshot. Self-contained. Expensive to store but requires no context to decode. You can seek directly to any I-frame.

**P-frame** (predicted): a forward diff from the previous reference frame. Stores only what changed. Cheap, but depends on the chain — lose a frame and everything downstream breaks.

**B-frame** (bidirectional): references both a past and a future frame. Most compressed, but requires lookahead. Only possible when you can buffer.

The codec's GOP (group of pictures) structure determines the pattern: how many P-frames between I-frames, where B-frames go, how long the dependency chain runs before the next keyframe resets it. GOP is a policy. It balances compression ratio against random access, error resilience, and decode cost.

### Worked example: Soar PR [#578](https://github.com/SoarGroup/Soar/pull/578)

Soar's EPMEM stores episodes as change-deltas indexed by decision cycle number. Each delta records what changed in working memory since the last cycle. In codec terms: every episode is a P-frame. The system never produces I-frames — there's no operation that collapses a window of deltas into a self-contained snapshot. The P-frame chain grows to 72,000 entries per hour with no keyframes to anchor it. Retrieval means reconstructing state by replaying the chain from the beginning.

The [demonstration PR](https://github.com/SoarGroup/Soar/pull/578) adds two operations: consolidation and eviction. In codec terms:

| Codec concept | Soar parameter | What it does |
|---|---|---|
| **GOP length** | `consolidate-interval` (default: 100) | How many P-frames between I-frame extraction runs |
| **I-frame extraction** | compose + test over `_now` table | Union of constant WMEs active across the window. Continuous presence ≥ `consolidate-threshold` → write to smem as a self-contained snapshot |
| **P-frame eviction** | `consolidate-evict-age` | Delete episode rows older than this. Safe because the I-frame (smem entry) already holds what mattered |
| **Scene-change detection** | `consolidate-threshold` (default: 10) | WMEs must persist for this many consecutive episodes to qualify. Transient state doesn't make the keyframe |

Before the patch: GOP = ∞. Every frame is a P-frame. No keyframes, no eviction, no chain-breaking. Retrieval cost is O(n) in total experience.

After: GOP = 100. Every 100 episodes, the system scans for stable structure, writes it as a self-contained smem entry (I-frame), and evicts the P-frames that are now reconstructible. Retrieval cost stays proportional to important episodes, not total decision cycles.

The algorithm is [Casteigts et al.'s](https://link.springer.com/article/10.1007/s00224-018-9876-z) compose + test framework from temporal graph theory. The vocabulary to recognize it as a keyframe extractor — GOP, I-frame, eviction — came from video codecs. Neither field talks to the other. The same compression geometry, discovered independently.

### Forgetting as bitrate adaptation

Under memory pressure, a codec drops frames in a specific order:

1. **B-frames first.** Most dependent, most reconstructible. Losing them costs detail but preserves structure.
2. **P-frames next.** Reconstruct from nearest I-frame. Losing them costs continuity between keyframes.
3. **I-frames last.** Self-contained. Losing one means losing an entire segment with no recovery.

This suggests a forgetting policy for episodic stores. Routine episodes — minor variations on a known pattern — are P-frames. They're the first to drop because they're reconstructible from the nearest keyframe. Distinctive episodes — novel states that share little with their neighbors — are I-frames. They persist longest because nothing else can reconstruct them.

The drop order isn't a metaphor for forgetting. It's a compression strategy that any system under memory pressure can apply: degrade resolution before coverage, lose detail before structure.

### GOP as consolidation policy

The GOP structure is itself a parameter. How often to keyframe? The answer depends on how fast the state changes.

**Stable environments** → long GOP. Few I-frames, many P-frames. Most of the state is the same between episodes. Compression is high.

**Volatile environments** → short GOP. Frequent I-frames. The state changes too fast for long dependency chains. Store full snapshots because you can't predict what persists.

**Mixed environments** → adaptive GOP. Scene-change detection triggers an I-frame. Between scene changes, P-frames accumulate. H.264 does this: monitor frame similarity, and when it drops below a threshold, force a keyframe. The threshold is the consolidation policy.

### The same geometry elsewhere

Git stores diffs (P-frames) anchored by snapshots at pack boundaries (I-frames). Gradient descent stores parameter updates (P-frames) anchored by checkpoints (I-frames). Neither uses the codec vocabulary, but both arrived at the same structure:

| | I-frame | P-frame | GOP trigger |
|---|---|---|---|
| **Soar** ([PR #578](https://github.com/SoarGroup/Soar/pull/578)) | smem entry via compose + test | WME change-delta | every 100 episodes |
| **Git** | pack snapshot | commit diff | pack-objects heuristic |
| **SGD** | checkpoint | parameter update | epoch boundary |

Three systems, three substrates, independently converging on I/P structure with a periodic keyframe trigger. Three examples don't prove universality, but any system accumulating sequential diffs faces the same design choices. Video compression has forty years of engineering on those choices. The algorithms may not port directly — the distortion metric for episodic memory isn't PSNR — but the words travel even when the implementations don't.

### Storage and learning

The codec gives Consolidate a storage layer — episode format, compression scheme, GOP policy, forgetting order, random access — but not the full contract. An I-frame is a snapshot, not a schema. The step from "compressed episodes" to "updated policy" is where domain-specific work begins.

### The third frame type

I/P is the demonstrated claim. The Soar PR implements it. But video codecs have a third frame type, and it points somewhere interesting.

B-frames reference both past and future. They're only constructible offline, when the system has buffered enough of the stream to look in both directions. They produce the highest compression — and they generate frames that aren't literal copies of anything in the input.

This looks like what happens when the forward pass stops running. Close your eyes: the stream of I-frames from perception cuts off. What remains is the buffer. The system runs on stored representations, referencing both past episodes and anticipated structure, resolving noise into coherent signal. Children see images form out of the noise. Diffusion models do the same thing computationally — iterative denoising from bidirectional reference toward a coherent frame.

The pattern recurs at every layer where the system fills in what it doesn't directly observe:

- **Vision**: foveal capture is a tiny I-frame. Peripheral vision is filled in from the mental model — approximate, low-bitrate, generated.
- **Hearing**: the [phonemic restoration effect](https://en.wikipedia.org/wiki/Phonemic_restoration_effect). Replace a phoneme with noise; listeners hear the word intact. The system generates the missing frame from context.
- **Memory**: vivid experiences persist as I-frames. The story between them is reconstructed — which is why eyewitness testimony is unreliable. Most of what people "remember" was never stored.

Each of these looks like B-frame construction: synthesizing a coherent signal from sparse keyframes and bidirectional context. If I-frames are what was observed and P-frames are what changed, B-frames are what the system generates to fill the gaps.

This is speculation, not theorem. We don't have a PR for B-frame consolidation. But the lead is specific enough to test: if episodic systems that only do I/P compression plateau in quality while systems that add bidirectional synthesis (diffusion, bidirectional attention, sleep-dependent memory consolidation) surpass them, the codec vocabulary would have predicted it. The frame type that requires offline access to both temporal directions might be where storage becomes learning.

---

*Written via the [double loop](/double-loop).*
