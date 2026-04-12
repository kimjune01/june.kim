---
variant: post
title: "ephemeral IRC"
tags: projects, methodology
---

IRC was invented in 1988. It gave you a room, a nick, and a message. No account, no history, no algorithm. You were in the room or you weren't. The conversation happened while you were there and evaporated when you left.

Discord, Slack, and Teams added persistence, identity, and a landlord. The room became a log. The log became a backlog. The backlog became an inbox nobody asked for. Every channel you ever joined, every friend you ever added: append-only, no TTL, no decay.

The reinvention added something real: scrollback, mobile push, file sharing, search. But it also added a social graph that only grows, a friend list with no eviction policy, and a corporation between you and your conversations.

### What if the room just worked like a room

A room you walk into. You talk. You leave. The room is empty again.

No signup. No app install. Click a link and you're in. The URL is the credential. The browser is the client. When the last person leaves, the room is gone. No durable history by default. Gone.

This is IRC. It already works this way. The protocol is [RFC 1459](https://www.rfc-editor.org/rfc/rfc1459), updated by [RFC 2812](https://www.rfc-editor.org/rfc/rfc2812). A channel exists only while someone is in it. No account registration for users. Any nick, any channel, join and talk.

### What IRC couldn't ship

IRC's problem was never the protocol. The protocol allowed persistence, rich clients, mobile push. Nobody shipped them as a seamless default because you can't mandate a breaking change across independent server operators.

But code is cheap now. A Phoenix rewrite of an IRC web client (WebSocket bridge, rich UI, rooms that decay) is a few weekends, not a company. The protocol is fine. What's missing is the product.

### AI changes the room

An IRC channel with a bot in it is a fundamentally different thing from a group chat with a bot in it.

On Discord, the bot is a second-class citizen: special badge, limited permissions, separate API. On IRC, a bot is just another nick. The protocol doesn't distinguish between a human and a bot. They both send PRIVMSG. They both join channels. They both leave.

That means a bot can moderate in real-time, summarize the conversation, answer questions, translate, fact-check. Multiple bots can collaborate in the same channel, talking to each other and to humans. No API integration needed; they read and write text.

IRC was dying because humans alone couldn't sustain the synchronous presence it demands. A channel needs someone in it to feel alive, and bots can be that someone. The always-on participant that makes the room worth entering until other humans show up.

### What it looks like

A teacher opens a room before class and shares the link. Students click it on their phones, no download, no login. An AI tutor joins as another nick in the channel. Students ask questions anonymously during the lecture; the tutor answers in the same thread. When the bell rings and the last person leaves, the room dissolves. No transcript, no record of who asked what. Tomorrow the teacher opens a new room with a new link.

### The spec

The product is an IRC server, a WebSocket bridge, and a web client. The IRC protocol ([RFC 2812](https://www.rfc-editor.org/rfc/rfc2812)) defines channels, nicks, messages, presence, and server linking. This spec defines only the delta.

**Server.** Phoenix application that speaks IRC natively and exposes Phoenix Channels over WebSocket. No separate IRC daemon; the Phoenix process is the IRCd. It accepts both raw IRC connections (for bots and traditional clients) and WebSocket connections (for the LiveView client).

**Client.** LiveView renders the web UI. No frontend build step, no React, no bundler. The browser connects over WebSocket; LiveView handles the DOM. A URL like `room.website/calc-study` is a channel. Visiting the link joins it.

**Identity.** IRC nick rules apply. Pick a nick on connect, change it with NICK. No registration, no email, no OAuth. The browser generates a keypair on first visit (localStorage); the public key is the persistent identity across rooms and sessions. Export the key to move to another browser, or clear it to become a new person.

**Persistence.** The server stores nothing by default. Messages exist in the channel buffer while the channel is alive. When the last human participant leaves, the channel and its buffer are gone. Bots alone do not keep a room alive.

**Decay.** Channels have an optional TTL set on creation. A 2-hour exam room, a 1-day event backchannel. When the TTL expires, the server sends PART to all participants and destroys the channel. Channels without a TTL live until empty.

**Bots.** Any process that speaks IRC can join as a nick. [OpenClaw](https://github.com/openclaw/openclaw) already bridges LLMs to IRC. A bot's message context is the channel buffer (in-memory, ephemeral). When the channel dies, the bot's context dies with it. Multiple bots per channel is the expected configuration.

**Moderation.** The room creator gets a capability URL for kick, lock, and end room. No global identity required to moderate.

**License.** AGPL-3.0, with attribution to [Kiwi IRC](https://github.com/kiwiirc/kiwiirc) and [Halloy](https://github.com/squidowl/halloy).

**Notifications.** Browser Notification API for messages while the tab is in the background. No push service, no service worker.

**Promise.** Ephemerality is a social contract, not a technical guarantee. Anyone in the room can copy, screenshot, or record. The server's promise is that it doesn't keep what you said.

### Who this is for

Situations where identity is a liability and persistence is a threat:

- Anonymous school confession channels that aren't owned by Meta
- Exam study rooms where nobody wants a log of what they said at 2am
- Event backchannels that dissolve after the keynote
- In-class discussion where the teacher can't trace who said what
- Tutoring rooms where the AI is a peer, not a tool, and nobody's embarrassed about what they asked

The confession.website philosophy applied to group communication: the default should be gone, not forever.
