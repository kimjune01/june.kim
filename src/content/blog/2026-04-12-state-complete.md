---
variant: post
title: "State Complete"
tags: design
---

The [transitions post](/life-is-in-the-transitions) covers how to move between states. This post covers which states must exist. Scott Hurff formalized five UI states in 2015; Vince Speelman expanded them to nine in 2017. The set below draws from both.

Many interfaces are designed as if only two states exist: the happy path and nothing. The user loads data successfully or stares at a blank screen. They submit a form or get an unhandled error. Transitions between states can be beautiful, but if the states themselves are incomplete, coherence breaks.

### The minimum set

For any view that reads, writes, or syncs with external systems, audit at least six states. Each answers a different user question. Skipping any creates a gap the user falls into.

**Empty.** *"Am I in the right place?"* The view has no data yet. Not an error, not loading. The user hasn't created anything, or the query returned zero results. This state needs to communicate: you're in the right place, here's how to start. A blank screen communicates nothing.

**Loading.** *"Is it working?"* Data is being fetched. Skeleton screens work when the shape of the content is known. Spinners or progress text work for unpredictable waits. Nielsen's guideline: under 100ms feels instant, under 1 second maintains flow, above 1 second needs an indicator. Silence in the gap feels like failure.

**Partial.** *"What can I trust?"* Some data loaded, some didn't. A list where three items rendered and two failed. A form where the address autocomplete timed out but the rest works. Most interfaces treat this as either full success or full failure. Neither is true. Never discard valid data because adjacent data failed. Show what you have, flag what's missing.

**Error.** *"What happened, and what can I do?"* Something broke. If the user can fix it, say how. If they can't, say what the system is doing and whether retrying helps. "Something went wrong" is the UI equivalent of a shrug. Good game UI avoids this during play because a confused player quits.

**Success.** *"Did it finish?"* The action completed. Confirmation should match consequence and reversibility. A copied link needs a small toast. A paid invoice needs durable proof, next steps, and a receipt. Game UI celebrates success with [juiciness](/game-ui-lessons) proportional to effort. Most apps give every action the same green checkmark.

**Offline / degraded.** *"What still works?"* The network is gone or slow. Is existing data readable? Are edits queued? Are destructive actions blocked? Is sync status visible? Can the user recover without duplicate work? Mobile made this state impossible to ignore.

### The audit

For any view, ask: what does the user see in each of these six states? If the answer for any state is "I don't know" or "the same as another state," that's a gap. Empty and loading should not look the same. Error and offline should not look the same. Each state is a different answer to a different question.

### Reference implementations

- [Actual](https://github.com/actualbudget/actual) (MIT) — local-first budgeting forces handling of empty, loading, partial sync, offline, validation. Every state matters because money is involved.
- [Hugging Face Chat UI](https://github.com/huggingface/chat-ui) (Apache-2.0) — streaming message states: pending, streaming, failed, retried, tool-running, tool-failed.
- [Hoppscotch](https://github.com/hoppscotch/hoppscotch) (MIT) — API client with request/response lifecycle states: loading, success, error, timeout, auth failure.

### The agent instruction

Check state completeness before checking transitions. A beautiful transition into a blank screen is still a blank screen. Enumerate the six states for every interactive view. Flag any that are undefined or collapsed into another.

[Conveyance](/gaming-patterns) applies to every state, not just the happy path. Empty conveys "here's how to start." Error conveys "here's what to fix." Loading conveys "the system is working." If any state fails to convey, the interface fails silently.
