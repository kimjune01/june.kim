---
layout: post
title: Persistent Agents
tags: coding
---

2025 was the year of agents. What is an agent? The concensus was that agents are tool calls in a loop.

| ![agent-anatomy](/assets/agent-anatomy.png) |
|:--:|
| **Anatomy of an Agent** |

But that wasn't a satisfying definition. Although it was capable of performing tasks, it wasn't enough to reliably fulfill job functions. It had to be told when to start, couldn't remember stuff, and sometimes required copy-pasting the output. And its performance depended on what tools you gave it, and the architecture around memory and architecture. 

What makes humans more useful than 'AI agents' today is that they're capable of holding onto context for the long-term and adapt to shifting needs of the master. This can be solved with different kinds of memory. To date, these kinds of memory are useful in combination: 

- Database: good for remembering many of the same kinds of things
- Filesystem: good for large chunks of hierarchically organized text
- RAG: semantic similarity for unorganized chunks of text repository
- MCP: procedural memory, deterministic
- Skills: procedural memory, flexible

Other tools are default expected for an agent to be useful. Claude Code's capabilities also include web search and writing to own memory. And if you give it tools, it will also incur side effects outside of its environment, such as making PRs and writing emails.

| ![persistent-agent](/assets/persistent-agent.png) |
|:--:|
| A persistent agent with tools to do the whole job |

So as our expectations grow, so should the products that we build. If it's a sales agent, it should have CRM access. If it's an executive assistant agent, it should have access to email, calendar, and reminders. It should be able to wake up on interval or on events, to incur an effect in the world outside of its sandbox, like scheduling meetings.

This vision is what inspired me to build [Skillomatic](https://skillomatic.technology/) but it is just a piece of tech without a problem to solve for now. [Composio](https://composio.dev/) does it better for enterprise. They call it 'hands for agents'. On the consumer side, [OpenClaw](https://openclaw.ai/) is making the rounds on social media that explores this next generation of agents.

In the near future, I expect that an agent be able to create other agents, experiment with variations for A/B testing. It will mutate, evolve, grow. It might already be happening.
