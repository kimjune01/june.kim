---
layout: post
title: Command Line for Work
tags: coding
image: "/assets/cowork-recruit.png"
---

| ![dev-pdca](/assets/dev-pdca.png) |
|:--:|
| A typical workflow for devs, pre-Claude-Code. |

See, think, do, review. Every responsibility in a business can be described this way. Everything from code, databases, budgets, marketing campaigns, and product. If the data is tokenized and [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)-able, it can be given to an agent for automation. 

| ![cc-workflow](/assets/cc-workflow.png) |
|:--:|
| The same workflow, implemented as a `skill`. <br> See *[error_review](/error-review)* for details |

| ![technical-user](/assets/technical-user.png) |
|:--:|
| Developers and technical users are ditching the GUI for the CLI |

LLMs have been around, but why now? Workflow automation were promised as the AI dream, but what's new is data availability and model reliability. Until now, humans had to specify where to source the data, how to shape it for LLM consumption, the steps to manipulate it, and the resulting action; all in a web GUI dashboard. This is silly, because it can be done by LLM just by asking in chat.

The formula is simple: give an agent access to the data, describe the steps you desire, and allow it to take actions on your behalf. If the agent can inspect the outputs of their actions, then it can [close the loop](/close-the-loop) on its errors and perform the workflow to completion. 

Combine B2B integrations with [skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), inside [Claude Cowork](https://claude.com/blog/cowork-research-preview), and the magic of Claude Code is no longer restricted to developers.

| ![cowork-acc](/assets/cowork-acc.png) <br> ![cowork-ads](/assets/cowork-ads.png) <br> ![cowork-recruit](/assets/cowork-recruit.png)|
|:--:|
| If it's possible for developers, how about for everyone else? |

The broader implication is startling. If we switch to direct API access, that deprecates dashboards, UI designers, most of B2B SaaS vendors, layers of management, among other BS corporate overhead. We'll be forced to become leaner and focus on actual problems for real human beings instead of serving the cogs and gears of optimizing the B2B sales cycle.

| ![power-user](/assets/power-user.png) |
|:--:|
| Will power users ditch dashboards for Cowork? |
