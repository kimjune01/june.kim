---
variant: post
title: "Junebot"
tags: projects
---

People tell me my blog is hard to read. They're right. Every post is a spec. No warm-up, no warm-down — an agent can invoke it cleanly. What makes it good prompt material makes it rough reading.

I have a dual audience mandate. Every post has to read well to a human *and* compose cleanly as a prompt. The audience is both: me-pointing-an-agent, and someone-scrolling-on-their-phone. Both usual fixes are bad. Dilute with stories, and the prompt stops composing. Fork per audience, and I'm writing the same idea five times for five imagined readers.

Then two numbers flipped.

|                              | 2022 ([GPT-3](https://en.wikipedia.org/wiki/GPT-3)) | today ([Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6)) |
|------------------------------|------|-------|
| input, per million tokens    | $20  | $3    |
| cached reads, per million    | —    | $0.30 |
| 50k-token prefix, per turn   | ~$1  | ~$0.015 |

A price threshold opens a third resolution. I ship the dense canonical version once, and let a cheap model translate on demand. The spec stays sharp. The reader gets the version they need. The bot can misread, but the canonical post is one scroll away.

So I built a chat box for the bottom of this post. Its name is junebot. It can pull any post and any page in /reading on demand. Ask it to explain this post like you're tired. Ask in plain English. Ask what it means for your actual project. It unpacks the density, in my voice.

All public: [junebot source](https://github.com/kimjune01/june.kim/tree/master/junebot).

The grimoire needed a translator. It's live. Try it below.
