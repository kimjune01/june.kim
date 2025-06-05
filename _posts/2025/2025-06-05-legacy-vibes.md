---
layout: post
title: Legacy Vibes
tags: coding
---

One common sentiment I've been hearing about agentic coding such as Claude Code is that it's great for greenfield projects but doesn't work on legacy code. Yes, if you were to give the same instructions you'd use for a fresh project to the legacy codebase, then it will flounder and throw false positives all day. 

| ![claude-fail](/assets/claude-fail.png) |
|:--:|
| _It does not, in fact, handle failures gracefully._ |

Developers often complain that it takes more time to review the shitty code written by AI than it takes for them to write it themselves. I get where that comes from, too. But how do you ignore the immense power that is the junior dev with the speed of a thousand typewriters? It's unfair (in current year) to expect that a machine will conform to us and our ways of working. We have to adapt to it. 

By claiming that your codebase is agentic-code-hostile, you're also admitting that it would take a long time for a new developer to get onboarded. What an LLM can't read in an hour, a human can't read in several weeks. So what does a senior engineer do to accomodate?

| ![legacy-code-wide](/assets/legacy-code-wide.png) |
|:--:|
| _Working Effectively with Legacy Code (2004)_ |

My immediate thought was to apply the lessons from the elders. During the days of hand-crafted code, actual humans had to read every line and apply changes manually. The TLDR of the book _Legacy Code_ is to treat all untested code as legacy code. Though it doesn't hurt to have someone know how things work, it's more scalable to document it as working, readable tests. The absence of tests in an established codebase is a form of job security for the engineer. 

> The better the code is tested, the easier it is to replace the programmer. 

I had the fortune of being able to use Claude Code on a legacy codebase this week. I could live-test these ideas and gain real-life experience with other engineers who opposed the idea. As a startup, they were even opposed to the idea of writing tests. In the days before agentic coding, it would take double the lines of code to publish the same feature if you wrote tests. But that equation has changed, because now it takes only a few extra seconds for Claude Code to pump out the tests. If you're still refusing to write tests, you're just allowing the human to stay in the loop. Close the loop by feeding back the errors from tests ([Then the code writes itself](/then-the-code-writes-itself)). 

So if agentic code requires testing, how to test legacy code without clean interfaces? It may be tempting to refactor a bit before shimming in the tests between the modules, but there's no way to be sure what got broken along the way. First do no harm. Test what interfaces exist. If you have a client-server architecture, there must be an API interface in between. Test that before changing anything inside.

As a new engineer thrown into a legacy codebase, I don't know what output to expect from each endpoint. All I know is what it outputs today. 

![living-documentation](/assets/living-documentation.png)

This is a testing harness. It covers all the API endpoints. Complete with auth and websocket implementation. It's vibe coded in two days. In it, a human can input anything into the parameters and the backend will spit out the results live. It offers the following benefits:

- Failure attribution in debugging – no more detective work with every bug
- Documentation
- Live monitoring
- Easier to visualize module separation
- **New feature verification**

Imagine that a new engineer joined your team and asked you for an approval on a Pull Request, but with a catch: you can't look at the code, only the file names. What would it take for the newbie to prove that it's a safe change to merge? What kind of verification gymastics would they need to do to show you that the code is legit? This is the bar you set for code that AI writes.

| ![blurry-pr](/assets/blurry-pr.png) |
|:--:|
| _Can't look at the code_ |

The agentic coder can write code faster than you can read it. You shouldn't hamper its output for your lack of reading skills. If all you can do is what files it changed, but you are still responsible for its output, it's faster to verify the net effect than to scrutinize code quality. Who cares if the variable names are a little whacky, if it's internally consistent? It knows how to lint, typecheck, and performance-optimize better than you, anyway. 

Every human dev with access to agentic coding has to play tech lead now. If you don't catch up, you'll be competing with AI instead of leading it.















