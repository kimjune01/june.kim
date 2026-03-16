---
layout: post
title: Caret Recorder
tags: projects cognition
---

*Part of the [cognition](/cognition) series.*

You saw something on your screen an hour ago—a link, a snippet, a decision someone made in a call—and now you can't find it. You know it happened. You just don't know which of your thirty open apps it was in.

Most tools in this space take screenshots every few seconds and OCR them later. You get a searchable timeline of pixels. But pixels don't know that you were in a code review, or that the Slack thread you were reading had three unread replies, or that the modal you dismissed had a specific error message. The visual record is lossy the moment you need to act on it.

Caret Recorder captures screen and system audio continuously in the background while a Swift sidecar traverses the accessibility tree of whatever app is in the foreground. Thirteen app-specific parsers (browser tabs, messaging threads, video calls, etc.) log what's on screen semantically—not just visually. The result is video segments paired with a structured JSONL stream of what you were actually doing.

It lives in the macOS menu bar as a colored dot. Gray for idle, red for recording, green when publishing to a room over LiveKit. No dock icon, no visible window, no friction.

### What's next

The recorder produces a firehose—a11y snapshots on every app switch, every tab change, every modal. Capturing is the easy half. The hard half is making any of it retrievable without storing everything forever.

The plan is a companion agent that clears noise in layers before anything touches a model. First, structural dedup—a [bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) variant checks whether an incoming a11y snapshot has been seen before and drops near-duplicates without storing the full history. Then diffing: if only the scroll position moved or a cursor blinked, collapse it. By the time a snapshot reaches inference, most of the firehose is already gone.

What survives goes to a cheap model (Gemini Flash) for triage. Each snapshot gets a quick ruling: novel enough to stash, or mundane? The model maintains a rolling context window—always warm, never full—with periodic partial compaction that merges related entries, demotes stale ones, and drops what no longer matters.

The key idea is approximating human forgetfulness. Recency, salience, emotional weight—things that broke, things that were surprising, things tied to open tasks persist longer. Routine fades. Compaction compresses the mundane and preserves the unusual. The result is a cache you can query that approximates your own memory: imperfect, biased toward what mattered, and useful exactly because it forgot the rest.

[GitHub](https://github.com/kimjune01/caret-recorder)
