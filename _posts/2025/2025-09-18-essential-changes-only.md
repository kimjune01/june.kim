---
layout: post
title: Essential Changes Only
tags: coding
---

> Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away. 
> 
> _Antoine de Saint-Exupéry_


LLMs are incredibly quick to generate code that makes it work. Sometimes it takes many prompts and nudges to get there, but eventually, you can get code to pass tests or pass some human criteria. Now, the bottleneck is no longer in generating code, but in reviewing it. So the only option is to make code easy to review, and to maintain less of it.

| ![232-changes](/assets/232-changes.png) |
|:--:|
| Would you please review my PR? |

It's tempting to believe Claude Code when it says it's `production ready` and `ready for human review`, but don't be fooled. 

![absolutely-right](/assets/absolutely-right.png)


Here's the trick that I use to trim down my PRs to its essence:

1. Write a short PR description
2. Clear context
3. Trim irrelevant changes from PR

One or two rounds of trimming removes excess logging, testing scripts, temporary docs, and files that shouldn't have been included in the first place. You may also come to realize that it should have been 2 PRs instead of 1. Other prompts that also work well is `look for overengineering, excessive code, irrelevant changes`.

When PRs are easy to review, it's faster to merge, and everyone's happy.