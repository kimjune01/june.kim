---
layout: post
title: Context Synthesis is Quadratic
tags: coding
image: "/assets/quadratic.png"
---

Regardless of the context limit, LLM performance degrades drops off like a cliff after hitting a wall. This is called [Context Rot](https://research.trychroma.com/context-rot). For fact-finding tasks(aka Needle in a Haystack problem), the search space for a fact grows linearly with context, but for synthesis tasks such as logic, the search space grows quadratically with context. 

Take for example, a tuple of facts with a clear semantic link:

> Tennis is exercise
>
> Exercise is healthy
>
> ∴ Tennis is healthy

The relation is trivial to derive when only two facts are presented into context. But as the number of facts grows, the pairs between each explode in number:

![quadratic](/assets/quadratic.png)

For as long as we live in the classical computing era, we should expect performance for synthesis tasks to drop off by 29% for each doubling of context. More so for tasks that require more than two factoids.

```
The derivative of √x is 1/(2√x)

When x doubles, √x increases by a factor of √2 ≈ 1.414. So the square root function grows more and more slowly as x increases.

For the derivative specifically: when you double x, the derivative gets divided by √2. This means the rate of change decreases by about 29% with each doubling.
```
Current LLM architecture for monolith context is bounded by this theoretical limit. Clear your context often, folks.
