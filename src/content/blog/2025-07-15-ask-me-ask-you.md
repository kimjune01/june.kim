---
layout: post
title: Ask me ask you
tags: coding
image: "/assets/ask-me-ask-you.png"
---

| ![ask-me-ask-you](/assets/ask-me-ask-you.png) |
|:--:|
| [Watch the scene on Youtube](https://www.youtube.com/embed/bkDhtH24oDM?si=dnEWXLQYchmhyYbA) |

As LLMs' ability to write code and test whiz past engineers, our ability to express specifications in natural language has overtaken coding as the primary skill in development. The source of truth in an application is no longer the code or tests. The new source is the specification. See [The New Code — Sean Grove, OpenAI](https://www.youtube.com/watch?v=8rABwKRsec4&t=547s).

If a binary can be compiled from source code, the code is valuable, and the binary is disposable. And if the code can be generated from specification, then the specification is valuable and the code is disposable. 

Then how do you write a spec? 

I proposed BDD and cucumber files as one format to help bridge the gap. See [BDD 101: Gherkin By Example](https://automationpanda.com/2017/01/27/bdd-101-gherkin-by-example/) for a primer. This works for a user-facing application, and LLMs know what this is. But BDD files require a level of detail and structure that impedes free flow of thought. What's the best way to extract a garbled mess of a vision in my head into something that a computer can understand?


| ![interrogation](/assets/interrogation.avif) |
|:--:|
| The ideal interface for writing specs is a video game dialog |

To write a spec, ask your coding agent to make a markdown or cucumber file, with a few sentences describing your vision. It will hallucinate and fill in the blanks, as it should. But _before_ asking it to implement the spec, simply ask:

> Ask me questions about the spec one section at a time, so I can approve it

It will reveal gaps in your thought. After it looks complete, you can do a linting step to refine it.

> Think critically about the spec, about inconsistencies and ambiguities. How can it be made better?

Only then, ask it to come up with a work plan. Ask it to ask you about the plan, too.

LLMs are incredible, and we'll never catch up to what it's good at. Elicitation is the collaboration mode that extends creavitity beyond our limits.