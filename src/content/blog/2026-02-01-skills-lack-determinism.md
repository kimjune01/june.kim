---
layout: post
title: Skills Lack Determinism
tags: coding
---

![mistakes](/assets/mistakes.png)

LLMs are marvelous, so we want it to repeat the tasks, so we make skills out of our chat history. You can do this easily with Claude Code/Cowork, which is already equipped with a skill builder. Just as I had expected computers to act reliably, I also expected the same with skills. But from my experience with skills like `/deploy` and `/error-review`, it worked _most of the time_. 

I was also working on a `skill-builder` skill for Skillomatic, when I noticed that the rules that I specified in the builder were being ignored. I addressed this issue in the past, [Don't LLM what you can code](/dont-lang-what-you-can-math). The fix here isn't to add angry capital letters and threaten with dying children of leukemia that would be saved otherwise. It's to just add some code that the skill will invoke via MCP or cli.

![skill-mcp](/assets/skill-mcp.png)

The code that runs can enforce parameters, validating them and returning errors otherwise. With helpful error messages, the agent can then [close the loop](/close-the-loop) and try again until it gets it right. This is the #1 reason to be thorough with error-handling in MCPs. In my case, the skill was decomposed into `compose-skill.md` and `submit_skill` MCP.

Skills and MCPs aren't direct substitutes. They can complement each other.