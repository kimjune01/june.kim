---
layout: post
title: Speed in Slop
tags: coding
image: "/assets/fix-fast.png"
---

As product builders, our performance should be attributed to the value that our product yields to its users. But beecause there's no direct measure, we resort to proxy ones such as velocity and error rate. Although we'd like to ship bug-free code, the only way to achieve that is to anticipate and test every scenario. That's way too slow and still, there's no guarantee. 

So what's the alternative? Ship fast, and break things. More importantly, to fix things even faster. In [/error_review](/error-review), I demonstrate a method to extend the deployment pipeline such that errors in prod are automatically detected, fixed, and brought to human review. 

When it takes way longer to manually review and verify code than it is to ask Claude to generate them, it is natural to maintain the same standard as before, when admitting subpar code to production. But when we adjust for the impact reduction that automatic error mitigation provides, does that change the equation?

| ![verify-lite](/assets/verify-lite.png) |
|:--:|
| When errors happen more often but they're fixed quickly, you ship at double the speed. |

Obviously, in a life-critical application such as [administering doses of X-ray to patients](https://en.wikipedia.org/wiki/Therac-25), a mistake could mean the end of life for both the patient and the business. But in a B2B SaaS where the worst thing that could happen is to ruin an HR lady's or a finance bro's afternoon, the risk can be offset with free credits or subscription extensions. 

Even the most successful products allow bugs in production. Cursor, Anthropic, and OpenAI's new features are often buggy and full of slop. But because they're fixed quickly, few notice nor care.

After the bugs are fixed, [remediation](/remediation) such as tests or CI improvements should be enacted to bolster your [quality-fortress](/quality-fortress), to reduce the likelihood of the same bugs being shipped in the future. For routine additions, planning docs and verification docs should be updated. 

Craft code feels good but it doesn't scale. [Close the loop](/close-the-loop) on the development cycle, then unleash the artificial intelligence at max speed.

| ![fix-fast](/assets/fix-fast.png) |
|:--:|
| With less verification effort, things break more often. In exchange for volatility, you ship more product. |

For a startup whose business is yet to be proven, upset customers are signs of validation. For a startup in the growth phase, negative impact for existing users is offset by the positive impact for future users – users yet to be captured by the extra features.

