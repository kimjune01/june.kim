---
layout: post
title: "Cord: Human-written"
tags: coding
---

> I was extremely pleased to see the Opus-written blogpost from earlier in the week [Cord](/cord) hit the front page of Hackernews for a few hours on Friday. And one commenter by tne name of mpalmer offered sharp criticism about how sloppy the writing was. I was humbled. So this is for you, mpalmer! 
>
> Instead of trying to do a better job of describing Cord, I think it'll be more interesting to tell you a story of how the idea coagulated.

| ![cord-hn-front](/assets/cord-hn-front.png) |
|:--:|
| [Link to HN discussion](https://news.ycombinator.com/item?id=47096466) |

On Wednesday, I had an interview with an agent-buildint team where I had all the right answers for the architecture of a blackbox-testing agent for computer use. During the interview, I came up with a neat idea for using a RAG as a cache layer for mapping a (screenshot + intent) pair to a series of commands into the black box. But when I was asked about how to deal with long-running tasks with large context, I struggled to come up with a satisfying answer. I suggested [filesystem memory](/filesystem-memory) and keeping goals in markdown files, inline with Dex's [onboarding agents idea](https://youtu.be/rmvDxxNubIg?si=9XKPU1IrH4lVMZ3u&t=721). But that felt clumsy. Compaction seemed low-resolution. There must be a better way.

What were the existing solutions from recent past? Agents coordinating is not a new problem. Git worktrees, swarms, serialization via PR review simulation, swarms, they've all been tried but seemed like too much overhead. As LLM base models get more powerful, I knew that agent coordination is yet another layer to be absorbed by 
the models.

I looked to human organization for inspiration. How do humans solve a problem? A founder discovers a problem, then raises funds for hiring more humans to act as agents. Sometimes it's specialists, or just more copies of generalists to speed up wall clock time, parallelizing as much as funds allow. 

I also looked to classical programs. Functions get invoked from main, that invokes more functions, either in series or in parallel. A stack is just a formal, deterministic list of goals that are rendered into a trace, represented by a memory allocation tree. When a goal is defined, resources are allocated. When the goal is achieved, resources are freed. What would that look like in an LLM orchestration harness?

That's when I started talking to claude about a dynamically changing org tree of agents. I can visualize the TUI of goals like a stack trace, but instead of functions, it's `claude` calls with goal prompt parameters. Thinking that Claude Code is really good with files, I wanted a single source of truth, with dedicated syntax. A file that anyone can read. Claude suggested calling the file extension `.scl`, short for `swarm coordination language`. Given the rules of the game, the LLM would figure out the rest. 
 
But knowing LLMs, they're stochastic and can make mistakes. I wouldn't trust it to change the file without a deterministic intermediary. [Don't LLM what you can code](/dont-lang-what-you-can-math). So I asked Claude to spec out what this would look like. I haven't implemented yet. Tool calls were the answer, and any sequence of tool calls must maintain integrity of the coordination file. An MCP server was the natural choice.

I then asked Claude to turn the spec doc into a RFC-style doc to make it more concise, a manual compaction step.

Me being skeptical still, I got Claude to write a stub MCP server to see if Claude would even call these tools. This was a pivotal step, where feasibility hinged on the base model's intelligence. I was pleasantly surprised to see that the tests passed for all tool calls.

Only then, I asked Claude to fill out the implementation as a proof of concept. I was motivated to see a live demo of it in action. While implementing, I realized that files a bad absstraction, so I swapped it out for a sqlite implementation, while maintaining the appearance of a file via a TUI. Each node has IDs and they're all ordered, so a database had no trouble accepting a serial stream of row mutations. Python having `sqlite3` without needing dependencies was super clean.

Seeing how easy it was so easy to swap from a file implementation to a database implementation, I slowly realized that it's more protocol than it is framework. I'm not getting rich off this idea, and nobody else is. George Hotz's spirit came over me. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/mFE-Frsi6Uw?si=u2k8btWpu13eVkZ5&amp;start=742" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

> How can I get ahead? That's probably the wrong question. Just ask how can I not fall behind? And the answer to that is nothing more than figure out how to produce value for other people. Figure out how to produce more than you consume.

No spec survives contact with implementation. Alternative implementations could be concurrent, crashproof, resilient, on top of this protocol. Humans can be swapped in place for a node with access to the same tools.

I have to confess, at this point, that I did not maintain academic integrity as a researcher. I got it working with small toy examples, tested lightly against only Opus and Sonnet; I don't have a corporate token budget. I then fed an MVP spec for [KindWatch](https://kind.watch/), but both models handled it with only one layer of children, no better than calling Claude Code without the harness. But that result didn't contribute to the core idea so I omitted that datum and moved on. Good thing I'm not in academia.

Playing around with it, and inspecting the tool calls, I found that Claude wanted to call tools that didn't exist: `pause`/`resume`/`redirect` children nodes like how I would when I watch my claude instances. So I added those too. Claude oneshot it.

Because this is an interesting idea to other nerds at HackerNews, I need to continue research to further the AI cause. Immediate area of interest is setting up more serious experiments and allowing an in-between tool call between `fork` and `spawn`, where custom context can be specified for a fresh node. This will simulate me doing research, saving a doc, refreshing context, and starting fresh.

Thank you for reading this less sensational version of my experience with Cord. I hope the name dies but the idea to live on in other implementations.

