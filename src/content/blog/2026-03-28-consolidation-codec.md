---
variant: post-medium
title: "Consolidation Codec"
tags: cognition
---

*Part of the [cognition](/cognition) series. Builds on [Consolidation](/consolidation) and [Prescription: Soar](/prescription-soar).*

### The contract

Consolidate reads from the store, finds patterns across episodes, and writes policy changes back to the substrate. Its contract is: many episodes in, fewer parameters out. The episodes shrink; the policy improves. Every cycle that adds experience without consolidating it grows the store linearly.

[Soar](/diagnosis-soar) has consolidation for procedural memory: [chunking](https://en.wikipedia.org/wiki/Soar_(cognitive_architecture)) reads from the decision trace and writes a new production rule, so the impasse that triggered it never fires again. That's a backward pass. But episodic and semantic memory have no equivalent — those stores grow without compression.

Every system that stores episodes faces the same curve. Soar built chunking. Transformers use gradient descent. Zep builds temporal knowledge graphs. Each one works. None share vocabulary.

Video codecs are the shared vocabulary. Forty years of engineering on exactly this compression problem.

### The stream

Episodes arrive in sequence. Each episode is a snapshot of state paired with the policy that produced it. Between consecutive episodes, most of the state is identical. The policy changes even less frequently; it updates only when Consolidate itself runs, which is offline, periodic, asynchronous. A deployment that handles ten requests is ten episodes. Nine of them share the same policy and nearly the same state.

This is a stream with high temporal redundancy. Video codecs compress exactly this kind of signal: consecutive frames share most of their content, and the interesting information lives in the deltas.

### Frame types

A video codec doesn't store every frame at full fidelity. It classifies them by how much context they need:

**I-frame** (intra-coded): a complete snapshot. Self-contained. Expensive to store but requires no context to decode. You can seek directly to any I-frame.

**P-frame** (predicted): a forward diff from the previous reference frame. Stores only what changed. Cheap, but depends on the chain. Lose a frame and everything downstream breaks.

**B-frame** (bidirectional): references both a past and a future frame. Most compressed, but requires lookahead. Only possible when you can buffer.

<div style="max-width:min(90vw, 700px); margin:1.5em auto;">
<img src="/assets/gop-strip.svg" alt="GOP strip: I-frames are tall (3.3 KB), P-frames are short (0.7 KB). Pattern: I P P P I P P P I P P." style="width:100%; display:block;">
</div>

The codec's GOP (group of pictures) structure determines the pattern: how many P-frames between I-frames, how long the dependency chain runs before the next keyframe resets it. GOP is a policy. It balances compression ratio against random access, error resilience, and decode cost.

### Worked example: financial accounting

[Double-entry bookkeeping](https://en.wikipedia.org/wiki/Double-entry_bookkeeping) has been running this pattern since the 15th century. Every transaction is an immutable entry. You never modify a ledger line — you append a correction.

The raw data is the [journal](https://en.wikipedia.org/wiki/General_journal): chronological entries, every debit and credit. The [ledger](https://en.wikipedia.org/wiki/General_ledger) groups entries by account. The [trial balance](https://en.wikipedia.org/wiki/Trial_balance) collapses all accounts to their balances at a point in time. Three [financial statements](https://en.wikipedia.org/wiki/Financial_statement) project different views from the trial balance: the balance sheet (state now), the income statement (changes this period), the cash flow statement (cash-affecting changes only).

That's a multi-stage compression pipeline. Journal → ledger → trial balance → statements. Each stage discards detail and preserves structure.

| Codec concept | Financial accounting | What it does |
|---|---|---|
| **I-frame** | Trial balance (closing) | Full account state. Self-contained, seekable. |
| **P-frame** | Journal entry | An incremental change. Cheap to record, depends on the chain. |
| **GOP trigger** | Closing period (monthly, quarterly, annual) | How many entries accumulate before the next balance. |
| **P-frame eviction** | Archival of closed periods | Move old entries to cold storage. Safe because the trial balance holds what mattered. |
| **Projections** | Balance sheet, income statement, cash flow | Different read models over the same I/P structure. |

Before closing: reconstructing account state replays every journal entry from day one.

After: start from the nearest trial balance and replay only subsequent entries. The three financial statements are projections from the I-frame — different questions answered from the same snapshot.

The closing period is the GOP policy. Monthly closes mean fast lookups but more bookkeeping. Annual closes mean less overhead but slow reconstruction. The tradeoff is identical to video: compression ratio against random access latency.

Software formalized this as [event sourcing](https://en.wikipedia.org/wiki/Event_sourcing): immutable event logs with periodic snapshots. Same structure, same tradeoff, five centuries later.

### Forgetting as bitrate adaptation

Under memory pressure, drop P-frames first. They're reconstructible from the nearest I-frame. I-frames persist longest because nothing else can reconstruct them.

Event sourcing does exactly this: truncate events before the latest snapshot. The snapshot survives. The routine state changes are gone, but the important state is preserved. Degrade resolution before coverage, lose detail before structure.

### GOP as consolidation policy

The GOP structure is itself a parameter. How often to keyframe? The answer depends on how fast the state changes.

**Stable environments** → long GOP. Few I-frames, many P-frames. Most of the state is the same between episodes. Compression is high.

**Volatile environments** → short GOP. Frequent I-frames. The state changes too fast for long dependency chains. Store full snapshots because you can't predict what persists.

**Mixed environments** → adaptive GOP. Scene-change detection triggers an I-frame. Between scene changes, P-frames accumulate. H.264 does this: monitor frame similarity, and when it drops below a threshold, force a keyframe. The threshold is the consolidation policy.

### The same geometry elsewhere

[PostgreSQL's WAL](https://www.postgresql.org/docs/current/wal-intro.html) stores byte-level diffs (P-frames) and periodically writes a checkpoint (I-frame). Recovery replays WAL entries forward from the last checkpoint. Checkpoint frequency trades write amplification against recovery time, the same curve as GOP length against random access.

| | I-frame | P-frame | GOP trigger |
|---|---|---|---|
| **Accounting** | trial balance | journal entry | closing period |
| **PostgreSQL** | checkpoint | WAL entry | `checkpoint_timeout` / `max_wal_size` |
| **Video** | keyframe | predicted frame | scene-change detector |

Three systems, three substrates, independently converging on I/P structure with a periodic keyframe trigger. Any system accumulating sequential state changes faces the same design choices. Video compression has forty years of engineering on those choices. The words travel even when the implementations don't.

### Learning is more than compression

The codec gives Consolidate a storage layer (episode format, compression scheme, GOP policy, forgetting order, random access) but not the full contract. An I-frame is a snapshot, not a schema. Compression alone doesn't update the policy. So where does learning enter?

### The quality signal

The system has a predictive model (pmem). Each episode arrives and the model either predicted it or didn't. The prediction error is the residual: actual minus expected. [Predictive coding](https://en.wikipedia.org/wiki/Predictive_coding) stores only the residual. Everything the model already knew gets suppressed.

Early in the system's life, the model is naive. Most episodes are surprising. The residuals are large. In codec terms, the stream is I-frame-heavy: dense, expensive, full of novel information.

As the model improves, the residuals shrink. Episodes become routine diffs from a good prediction. The stream shifts to P-frame-heavy: sparse, cheap, mostly confirmations. The I-frames that survive are genuinely novel.

<div style="max-width:min(90vw, 700px); margin:1.5em auto;">
<img src="/assets/distribution-shift.svg" alt="Three rows of episode blocks. Cycle 0: mostly tall dark blocks (I-frames, everything novel). Cycle 3: mostly short light blocks with occasional tall dark ones (improving). Cycle n: almost all short light blocks with one rare tall dark block (expert, rare surprise)." style="width:100%; display:block;">
</div>

The distribution shift *is* learning. Not a separate step after compression, but visible in the data itself: the ratio of I-frames to P-frames tracks how much the system understands. A system that stores everything equally has learned nothing. A system that stores almost nothing predicts almost everything.

### The contracting cycle

Better model → smaller residuals → sparser episodes → faster consolidation → better model. Each cycle tightens the prediction. The data gets cheaper to store because it's less surprising. The consolidation gets faster because there's less to process.

This is the data specification for the [monoid](/cons). `cons` describes the structure: episodes → knowledge → procedures → episodes. The codec vocabulary describes what flows through that structure: residuals that shrink as the policy sharpens. The quality measure is prediction error. The trend is monotonic compression toward a system that stores only what it cannot yet predict.

---

*Written via the [double loop](/double-loop).*
