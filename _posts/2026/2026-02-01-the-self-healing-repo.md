---
layout: post
title: Self-healing Repo
tags: coding
---

| ![bug-cycle](/assets/bug-cycle.png) |
|:--:|
| A lifecycle of a production bug |

The traditional way to detect, triage, fix, and deploy bugs involved humans at every step. But now that AI agents are faster better bug-fixers, do we need all those checkpoints? The cycle time for a bugfix is somewhere between a week and a day, with teams boasting next-day bugfixes as an accomplishment.

But if the bug has an obvious fix, can we just let an agent fix it?

| ![auto-cycle](/assets/auto-cycle.png) |
|:--:|
| 3x less human |

With this setup, without loss of quality, bugfixes can be shipped about 3x faster, sometimes as fast as minutes. Shipping bug-free code is impossible, but deploying self-fixing code is well within reach. It does require that telemetry be set up for unambiguous error reporting, however.


| ![auto-fixer](/assets/auto-fixer.png) |
|:--:|
| Auto-fix agent running on lambda |

What can be done by an agent, should be done by an agent. Save your time and attention. Delegate & approve. Once you trust it enough, permit it to merge to main, and auto-deploy. 