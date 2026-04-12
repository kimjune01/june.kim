---
variant: post
title: "chat.june.kim"
tags: projects
---

[ephemeral IRC](/ephemeral-irc) was the spec. chat.june.kim is the room.

It speaks IRC on port 6667 and LiveView in the browser. WeeChat and Safari see the same messages. There is one process per room. When the last human leaves, the process dies and the buffer goes with it.

No accounts. No database. No Ecto, no Redis, no external state. Messages live in memory. The server promises it doesn't keep what you said; it doesn't promise others won't.

The room creator gets a moderation URL. There is no admin panel. There are no roles. The URL is the authority.

Right now it replaces the chat button on this blog. If I have the tab open, we talk. If I don't, the room is empty and you can email me instead.

That's the whole product: a room that exists while people are in it.

[step in](https://chat.june.kim) · [source](https://github.com/kimjune01/hangout) · [the vibelog](/ephemeral-irc)
