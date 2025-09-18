---
layout: post
title: Manual Context Compaction
tags: reflecting
image: "/assets/bad-puzzle.png"
---

I've been using Claude Code for about two months daily. Here's one lesson I learned along the way to prevent going in circles, improve output quality and fight context rot when driving it.

![compact claude](/assets/compact-claude.png)

Running long, serious sessions will often result in auto compaction, where it will run out of context length and force a summarization step before continuing onto the next prompt. When that happens, it means your average context utilization is over 50%, reaching 100%. Optimal context utilization for best results is 20-40%. 

| ![bad-puzzle](/assets/bad-puzzle.png) |
|:--:|
| Garbage in, garbage out |

If everything in the session context is relevant to your upcoming task, then running `/compact` may work, but there's a better way. Instead of moving a large context from one session into a smaller context in another, documenting into a markdown file will produce durable memory that can be shared with other developers. Try the following:

> `Document the research you just did into a markdown file` 
>
> `Write down what we tried and why it didn't work, and possible next steps into a file`
>
> `Turn this discussion into a spec file for an MVP`

Then, `/clear` context, and ask it to `take a look at the auth architecture docs` to recall memory as to prime it. Now, you have a super compact, reusable context that can be committed into the codebase. 

| ![good-puzzle](/assets/good-puzzle.png) |
|:--:|
| Solving a puzzle is easier without the wrong pieces |

When working with a long-running task that spans multiple sessions, it's helpful to keep a work plan, get Claude to update between each step, and clear context without fear of amnesia. 