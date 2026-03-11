---
layout: post
title: Caret Recorder
tags: projects
---

You saw something on your screen an hour ago—a link, a snippet, a decision someone made in a call—and now you can't find it. You know it happened. You just don't know which of your thirty open apps it was in.

Most tools in this space take screenshots every few seconds and OCR them later. You get a searchable timeline of pixels. But pixels don't know that you were in a code review, or that the Slack thread you were reading had three unread replies, or that the modal you dismissed had a specific error message. The visual record is lossy the moment you need to act on it.

Caret Recorder captures screen and system audio continuously in the background while a Swift sidecar traverses the accessibility tree of whatever app is in the foreground. Thirteen app-specific parsers (browser tabs, messaging threads, video calls, etc.) log what's on screen semantically—not just visually. The result is video segments paired with a structured JSONL stream of what you were actually doing.

It lives in the macOS menu bar as a colored dot. Gray for idle, red for recording, green when publishing to a room over LiveKit. No dock icon, no visible window, no friction.

[GitHub](https://github.com/kimjune01/caret-recorder)
