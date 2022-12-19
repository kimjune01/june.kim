---
layout: post
title: Jumping the Technical Interview Hoop
tags: coding
---


![flaming-motorcycle-jump](flaming-motorcycle-jump.webp)

> Literally me, interviewing at Google, circa 2017

Five years ago, I had just finished my computer science degree at university. I wanted to work in California to double my income compared to working in Canada, and the biggest hurdle to reach that goal was to pass a series of interviews; several of which was the dreaded technical interview. I had disdain towards it and any company that employed it to assess candidates. But it became obvious that if I wanted to get into these companies, it was up to me to jump the hoops, because they wouldn't lower it for me.

Further reading: [Your Job Shaped Code](https://kennethbruskiewicz.substack.com/p/your-job-shaped-code) by [Kenneth](https://www.linkedin.com/in/kenneth-bruskiewicz-98569256/)

Today, technical whiteboard-style interviews are still the norm. For remote jobs, the whiteboard is replaced by a soullesss text editor shared in real-time. The hoop remains the same shape, and the income difference between those who can jump it and those who cannot, are still roughly double. The typical advice from [/r/cscareeradvice](https://www.reddit.com/r/cscareeradvice/) is still to grind leetcode and hope for a question previously seen. However, having been on the other side of the table, the problem-solving part ios only one of four rubric points assessed by the conductor. It's not enough to have solved the problem.

What else is on that rubric? The interviewer doesn't actually care about you getting a job, or your personality, or what you ate for breakfast that day. They only assess your performance as objectively as they can. The dimensions assessed are: 
- Coding
- Data Structures & Slgorithms
- Design (rate only if assessed)
- Comprehension & Communication
- Efficacy
- Tests Code (optional)
- Systems Design (optional)

When you fail the interview, you will not get feedback on your performance. You'll just get an email from HR saying that you're 'not a good fit' for the team. On the flipside, once you apply again the following year, the interviewer will not know how many times you have failed. Unlike a university application, you get more than one shot at it. And with each failure, lessons can be learned to be applied in the next application.


### Problem

> To pass the technical interview for getting the Software Engineer (SWE) job while spending the least amount of time being unemployed

### Solution

> Understand the the interview rubric
> Gain mastery of the process that would check all the boxes in that rubric
> Practice with direct actionable feedback
> Learn lessons from each failure for the next iteration


## The process

The whiteboard interview is a performance with an audience of one. It's a show to put on that tells a story of your competence. Every interview is like every other, with a different main character, the problem. Rehearsing the 45-minute narrative can be done before, and each performance itself is another round of rehearsal for the next performance. As long as you keep improving each round, you will eventually pass the interview. 

You’ll have about 45 minutes with the interviewer. Ideally, this will be a collaborative effort but in the worst case, they are simply tasked with interviewing you. They probably have something better to do, and may not even want to help you with solving the problem. This is why you must be prepared to take the driver’s seat and convince them that you deserve a ‘Hire’ check.  Ultimately, they want a clear signal to complete their interview assessment form.

Simply solving the problem is not enough; you need to verify with the interviewer that it’s solved. Fortunately for you, the interviewer already knows the answer to the problem and all you need to do is ask if the interviewer is confident in your solution! This leaves no room for ambiguity to the interviewer of your success.

There is more than one way to get this guarantee, but to take a lesson from TDD (Test-driven development), I recommend writing the tests first. This accomplishes several things:

- You fully understand the problem. Tests are an alternative to asking clarification questions, where the interviewer is happy to pass or fail the test.
- You demonstrate your testing chops. Tests are required to be checked in with the code in many companies, and having this trait will make you stand out.
- You speedrun through the verification stage. If your tests cover enough cases, then passing the tests guarantees that your code is a working solution.
 
Understanding the problem must not be overlooked. The most common pitfall for beginner candidates is to solve the wrong problem. The tricky interviewer may never interrupt the candidate when making a mistake. Each step towards understanding the problem must be verified against the interviewer. Likewise, verifying your pseudocode solution and coded solution will prevent any backtracking while you traverse towards the solution. 

See more about the why and how to pseudocode [here](https://builtin.com/data-science/pseudocode)

> Pseudocode helps you reqlize possible problems or design flaws in the algorithm earlier in the development stage, which saves you more time and effort on fixing bugs and avoiding errors down the road.

The easiest way to prevent backtracking is to ask simple questions to the interviewer about your work. Each stage of effort you exert should be demarcated by a series of checkpoints. In other words, each stage is a mini while-loop with the checkpoint as the invariant, (lookup what a variant is: https://en.wikipedia.org/wiki/Loop_variant). Keep your iteration cycles tight and you will never fall into the rabbit hole of doom.

Let’s walk through each of the stages of the interview, and what to ensure before moving onto the next stage.

### 🙋Introduction & smalltalk

The first couple minutes is to get comfortable in the interview. Here, you can build rapport with the conductor. They might ask some variation of the “Tell me about yourself” question, where you will briefly talk about your proudest work. 

Then, the interviewer will provide the coding problem.

Explain how you will progress through the interview. 1) Tests, 2) Pseudocode, 3) Code, 4) Verify

State the goal being convincing the interviewer of your ability to solve the problem.
This boosts the interviewer’s confidence in your ability.

#### Checkpoint: Verify the success condition

Ask the interviewer if executing your plan would satisfy their expectations.

> Will the solution be sufficient if the function replaces the emojis that are bounded by either whitespace, newline or beginning/end of text?

> Would you be convinced that I’ve solved the problem if it passes the tests with edge cases I’m about to provide?

### ❓Understand the problem

Ask clarifying questions to get a grasp of question scope, as it might not be clear when the interviewer establishes it. 

Ask for test cases if they have any.

Write passing and failing tests to help with better understanding. 

#### Checkpoint: Ask the interviewer

if these tests would be sufficient. If not, then here is an opportunity to ask for what other edge cases would need to be covered. 

> The code I am going to write will cover general test cases, however, here are few edge cases that might not run. It would take a lot of time to figure those out, should my solution aim for those given the time limit?

### 🗣️Solve the problem via pseudocode 

If the code runs, use it to your advantage by running it frequently with failing tests. 

If the code doesn’t run, then be the compiler and run the pseudocode manually, talking out loud. 

E.g.
```
For each emoji pair, 
….check the input text if the emoji is in it 
….if so, check if it passes the whitespace/newline/boundary conditions
….If so, replace it.
```

#### Checkpoint: Test your pseudocode

Get confirmation from the conductor with each test expectation.

Ask for test cases that you may have missed
If you fail any tests, iterate on your solution.

### ⚒️Code your solution

Ask if syntax matters. If it does, then write one line at a time so that you don't backtrack. 
Break down your solution into named functions For clarity, see [Sprout Method](https://www.june.kim/sprout-method)
Write quick tests for your components and comment invariants if helpful


#### Checkpoint: Test your code

If runtime available, just run your test suite.
If not, then go through each of the positive and negative test cases manually. It can feel tedious, but go through each line of code as if you were the computer.

### ↔️Confirm solution with conductor

Ask the conductor if the written code is satisfactory. Also ask if performance is important. If so, address performance issues for space and complexity, with varying runtime/memory tradeoffs if relevant. 

If tests are right, and the code passes tests, then it’s done. You probably won’t have time to optimize for the faster runtime, but mentioning how it could be done is a bonus.

## Practice

During the interview, optimize for signal and clarity. If you communicate effectively, then the hints and clues will come naturally from the interviewer. It’s not about the solution, it’s about demonstrating your ability to make a convincing solution.

### Additional Resources

- [Pramp](https://www.pramp.com/)
- [Leetcode](https://leetcode.com/) - I recommend doing about 50 easy problems until the problems get familiar.
- [Technical Interview Cheat Sheet](https://github.com/tsiege/Tech-Interview-Cheat-Sheet)
- Ask me for the Google rubric
- Your friends that are also pursing the same goals
- If you don't have friends, ask me to find you a peer. june@june.kim

### Get Involved

I'm looking for help in getting the word out. I want to help people pass technical interviews. If you are in a hurry, I can help you directly with an income share agreement and get you that job ASAP. If you have skills that can help me turn this idea into a business, then we can exchange value that way.
