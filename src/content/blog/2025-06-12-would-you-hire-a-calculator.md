---
layout: post
title: Would you hire a calculator?
tags: reflecting
image: "/assets/calculator.png"
---

The term ["computer" used to be a job title for a person](https://en.wikipedia.org/wiki/Computer_(occupation)). Before the time of electronics, a pile of calculations were sent to a person, who would solve them, and return them. 

| ![calculator](/assets/calculator.png) |
|:--:|
| _This device made jobs obsolete_ |

Back in those days, it made sense for an employer to demonstrate a person's proficiency to compute. It was a brief work simulation. But imagine the employer asking how fast the employee can perform long division after each work station has been equipped with an electronic calculator. 

> Interviewer: Hey how many long divisions can you do in half an hour?
>
> Candidate: Why? How is that relevant? We have calculators for that.
> 
> Interviewer: This is our process, I just follow orders.

How about the time when we started using power saws?

| ![circular-saw](/assets/circular-saw.webp) |
|:--:|
| _I have a closet full of Milwaukee tools that I rarely use._ |

> Interviewer: Hey can you show me how straight and fast you can cut a piece of wood with a hand saw?
>
> Candidate: Why? We have power tools for that.
> 
> Interviewer: This is how we always did it. I didn't design this interview process.

Fast forward to the agentic AI revolution we are experiencing in 2025. This is what the interviewer sounds like when they say they don't allow AI to be used during the interview process. Yes, there are times when the engineer has to get in the code and debug manually. Yes, sometimes LLMs make mistakes and we have to go fix it. But that's not most of the job. The job has changed. Programmer used to be a job, just like calculator used to be. 

If the job candidate can commandeer 5 instances of Claude Code, wouldn't you rather see that demonstrated rather than seeing them compete with one? It's not about how well a human can program; it's about how well the human can use agentic programmers to achieve business goals. Writing lines of code is no longer the bottleneck to developing products, or doing analytics. When I say business, I'm talking about money to be made. 

So how _do_ you assess candidates for the job? The answer is obvious and simple, but far from easy or safe: simulate the work they will perform.

With `data structure & algorithms` questions, there is a right answer. With basically no training, any engineer can measure how far the candidate got to the answer. The rubric is a dartboard, and each candidate's shot is directly comparable with another. It's like running unit tests on agentic systems. It doesn't work anymore.

| ![art-school-admission](/assets/art-school-admission.jpg) |
|:--:|
| _Art college admission examination in China, 2017. If assessing for photorealism, why not just take a photograph?_ |

But agents are not deterministic. They cannot be confined into unit tests that either pass or fail. We use evals instead, but having the right evals is hard. Most teams don't even have them. But can we use evals for natural intelligence? If we could, it would look something like this:

- When assigned ambiguous goals, does the candidate identify the ambiguity and elicit a clarification?
- When asked to perform impossible tasks, does the candidate push back?
- When given tasks that are misaligned with previously assigned goals, do they ask why?
- Can the candidate orchestrate a wide enough range of tool calls?
- Can they compose a work plan for your review?
- Can they provably verify the results immediately, without requiring additional prompts?

These characteristics are held in high regard. They cannot be replicated with AI (so far). Ask any SOTA LLM an ambiguous question, and it won't push back; it's happy to keep generating tokens until it's out of API credits. 

You wouldn't assign long division to a drafter, so why assess for programming ability from software engineers?