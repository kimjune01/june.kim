---
variant: post
title: "ephemeral.website"
tags: projects
---

Nothing on the internet disappears. You post a photo, delete it, and a CDN edge node in Virginia still has the bits. Cache invalidation is a two-word joke with no punchline. The protocol doesn't want to forget, and neither does anyone downstream of it.

Voice is different. You say something to someone, the air moves, and it's over. There's no cache. No replication. No Wayback Machine. Conversation has always been ephemeral, and we never thought to fix that.

So I built a website that works like a conversation.

Record or upload audio, name a link, share it. One listen. Forward-only, no rewind, no replay. Pause too long and a 15-second countdown starts. When it hits zero, the S3 object is deleted and the URL 404s. The 404 is indistinguishable from "never existed."

[ephemeral.website](https://ephemeral.website) · [source](https://github.com/kimjune01/ephemeral.website)
