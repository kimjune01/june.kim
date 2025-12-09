---
layout: post
title: Quality Fortress
tags: coding
image: "/assets/defense-layers.png"
---

No amount of care or effort is enough to ship bug-free software, but you can always get closer. Then the question becomes how much effort to allocate to prevention vs. mitigation. Fight Club explains this well:

<iframe width="560" height="315" src="https://www.youtube.com/embed/SiB8GVMNJkE?si=pBf9CBiEDPsjCZ3n" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

> Cost allocation to preventing bugs ~= Cost of bugs in prod * probability of occurrance

The engineer's default answer to this formula is tests: unit tests, integration tests, e2e tests. But tests are only one layer of defense against bugs. As the cost of writing tests goes down, we can afford to add more layers.

I like to think of tests and type checks as static layers of defense. Deterministic layers that you set up once and forget about.

| ![fortress](/assets/fortress.webp) |
|:--:|
| Krak des Chevalier, 11th century Syria |

With Claude and agents, we can automate parts that were relegated to human code reviews, too. These are semi-active layers that used to be assigned to QA interns. I like to think of these as Bloons TD monkeys that i set up and watch them defend.

<iframe width="560" height="315" src="https://www.youtube.com/embed/1KGJVOVUl10?si=9xhSD0QJpiviKLHE&amp;start=102" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe> 

As the cost of defense goes down, we should ramp up the layers of defense and their intensity.

![defense-layers](/assets/defense-layers.png)