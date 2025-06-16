---
layout: post
title: Software is made of people
tags: reflecting
image: "/assets/mark-14-torpedo-.jpg"
---

It's easy to attribute a production bug or a regression to lines of code, but it's never the root cause. Poor software quality is a symptom of a development environment that allowed it to occur in the first place. Even with agentic coding, software doesn't write itself; the root cause is always human.

In retrospect, it's obvious that lack of testing yields poor quality. Consider the tragedy of [Mark 14 torpedo in WW2](https://en.wikipedia.org/wiki/Mark_14_torpedo#:~:text=The%20Mark%2014%20torpedo%20had%20four%20major%20flaws.,failed%20to%20detonate%20the%20warhead.). The Navy never live-fire tested the toepedoes before being deployed to the submarines of the Pacific theater for _not wanting to expend $10,000 per torpedo_. It was an unfortunate case of _trust me bro_ that caused approximately ~5000 misfires during the first two years of its deployment. Had they been reliable, the Imperial Japanese would have been crippled much sooner. 

| ![mark-14-torpedo](/assets/mark-14-torpedo.jpg) |
|:--:|
| [Read more about the scandal here](https://www.warhistoryonline.com/instant-articles/mark-14-torpedo-scandal.html) |


But the engineers and the leaders in charge of those torpedoes weren't stupid. If you were in the meeting room, you'd better be prepared to be interrogated about delaying its deployment and wasting 10,000 1941 dollars per test. 

![torpedo-people](/assets/torpedo-people.webp)

Ultimately, those torpedoes failed because the leaders tolerated bad engineering practices. Likewise, poor-quality software is because of poor-engineer behavior; poor-engineer behavior happens because it's allowed to manifest during development.

In a way, software development is an extension of people development. If tests are allowed to be skipped regularly, no more will be written. If engineers are allowed to push to prod without tests, comms, review or documentation; then knowledge will be silo'd and he'll be the hero to fix the bugs (that he caused) down the line. 

> Without guidance or control from leadership, quality standards will degrade to the lowest one of the bunch.

Holding quality standards doesn't mean being pedantic about rule-based systems full of red tape. It can be a set of principles or guidelines. It can be shared goals or cultural values. Ideally, it comes from engineering leadership (formal or not) that takes responsibility:

- Veto poor behavior
- Reward good behavior
- Publically acknowledge best practices
- Hold people accountable
- Set communication protocols / expectations

It's an attempt at shaping the ideal engineer to conform to the most appropriate one for the product being built. In the absence of authority, it's the individual engineer's responsibility to escalate these concerns.

Sooner or later, the owners end up paying the product punishment for the quality sins committed. Leadership must stay vigilant to pay respects to software quality. That means hearing concerns from experienced engineers who warn against skipping tests. If bad things happen like they said it would, it's not prophesy — it's pattern matching.