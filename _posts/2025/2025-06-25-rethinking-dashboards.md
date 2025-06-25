---
layout: post
title: Rethinking Dashboards
tags: reflecting
image: "/assets/reverie-ux.png"
---

B2B SaaS had a strong run for over a decade. But for a long time, I had an aversion to working on those because I don't like making dashboards. The interesting parts were the data, and its brutalist presentation in rows and columns, charts and graphs offered no creative freedom. I'll feel stuck, like in [Office Space](https://www.youtube.com/watch?v=Fy3rjQGc6lA). 

Can it be made better? When users pay for B2B dashboards, the GUI is not what they're paying for; they're paying for the data and the insights within. They'd rather be building sales relationships or think about competitive strategy rather than wrestle with a spreadsheet or a dashboard. Can the value propopsition of data presentation be made better with a chat interface?

| ![cursor-for](/assets/cursor-for.jpg) |
|:--:|
| YC 2025 batch of *Cursor for X* startups |

This is the premise behind the __Cursor for x__ startups. LLMs are powerful, and data is useful. What if you made one work for the other? 

| ![cursor-ui](/assets/cursor-ui.png) |
|:--:|
| Cursor's UI |

Let's take a look at what makes Cursor the posterchild of success:

- Familiar traditional UI in the center
- Unobtrusive Chat UI
- Context Transparency
- Agentic

| ![v0-dissection](/assets/v0-dissection.png) |
|:--:|
| V0's contextual AI. [V0 by Vercel](https://v0.dev/) |

User expectation flipped with ChatGPT, and sooner or later, those expectations will carry over to B2B SaaS dashboards, too. Wherever there's a SQL query or a dataviz being presented, there will be an expectation for a natural language interface. Why should any user bother learn your dashboard dropdowns and filter menus unnecessarily?

| ![dashboard-use-case](/assets/dashboard-use-case.png) |
|:--:|
| Is search-filter-sort-export the best way to answer these questions? |

This screenshot is from a B2B SaaS marketing website under the "Use case" section. It already assumes that users already know the questions to ask at the dashboard! If most of their users can't use excel to extract the data they need, then they can't be trusted to learn to use a dashboard, either. In the case of supply chain data, no quantity of glam can be sprinkled on the GUI to help me navigate to the prospect nuggets. 

![reverie-ux](/assets/reverie-ux.png)

What's the most natural interface for applying an LLM assistant for a dashboard of rows and columns? Each row, column, or list can be contextualized for a user query. Combined with the power of LLMs and MCPs, follow-up actions can be made in the same UI.

![reverie-ux-2](/assets/reverie-ux-2.png)

Whether LLM interfaces are a good idea for current year may be up to debate, but the trend is clear. Coders are enjoying the benefit, and it's only a matter of time that these interfaces are turned to requirements. B2B SaaS dashboards providing insights to the customers' data are cooked, but SaaS's who own the data will have to pivot to becoming data brokers. In a few years, it will be in the form of MCP servers, but until then, Cursor for Dashboards are the transitional UX. 
