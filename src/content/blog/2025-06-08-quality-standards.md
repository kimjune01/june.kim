---
layout: post
title: Quality Standards
tags: reflecting
image: "/assets/the-bar.png"
---

Force push, no tests; ship now, fix later. It's every day at startups, desperate for users and revenue, to justify subpar engineering. Tech debt isn't always bad, but it catches up soon enough and engineers are drown in it. 

| ![the-bar](/assets/the-bar.png) |
|:--:|
| _The bar is set high. Some jump over; others bend backwards under._ |

Recently, unit tests and smoke tests I wrote got ignored in CI and commented out, for a migration to land. Its consequences weren't noticed at first — because if it works, who cares? This was the attitude shared by the CTO of this startup. Honestly, I'd be ok with it too, if restoring the tests was queued up for tomorrow. It never happened.

I joined another company, and it happened again. This time, I had my entire testing and documentation suite get force-pushed over instead of resolving a code formatting merge conflict. I quit the next day.

![surprise](/assets/surprise.png)

This led to a bleak realization that no matter how hard I engineer, how obvious I make the quality standards, lack of leadership will inevitably degrade quality to nonexistence. Yes, it was my responsibility to bring up the topic of quality standards. But should I have taken it further by making it a hill to die on? No. Life is too short to work under apathetic leadership.

If you're not convinced that quality comes from management, let's run a thought experiment. What would you get if you took the leadership from high-quality manufacturing to low-quality employees? This was actually demonstrated by the NUMMI plant. See [How Toyota Turned Around GM’s Worst Factory](https://www.youtube.com/watch?v=ZjxZ2Eh9GrA). It's a famous business case study.

Everyone says they care about software quality, but when it comes to deciding between fixing broken tests and shipping new features, the mask slips away. Do you know of a way to test leadership for their attitude towards quality? Let me know.

