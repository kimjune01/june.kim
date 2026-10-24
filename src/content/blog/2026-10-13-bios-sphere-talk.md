---
variant: post
title: "Bios Sphere Talk"
---

There's a lot of talk about how we can make better agents. But these agents aren't exactly reliable. If they were perfect, us software engineers would be writing compilable prose all day without looking at the compiled code. For now, we still have to check agent outputs in code reviews. You can ask other agents to review, but even the review agents still output slop and junk sometimes. But we're not going back to manual coding, that would be like going back to the stone age. So how do we maintain quality in agent outputs?

To find out, I needed more agentic experience and experiment samples. So I went out looking for the problems in open source. The issues were on github, and PRs needed to be reviewed by maintainers on real projects. What would it take to get these coding agents to pass maintainers' scrutiny?

Experiment Setup:

![oss-exp-1](/assets/oss-exp-1.png)

I set up a coding factory that scans Github for other peoples' issues, fix them, then open PRs. It would find an appropriately complex issue, solve it, then make a PR. I was tokenmaxxing my way to learn what gets PRs merged. 

![bios-exp-pr-trust](/assets/bios-exp-pr-trust.png)

I didn't really know how Open Source worked, so this is how my first PRs came across. I was asking maintainers to trust that my code is legit because it works! It's their job to do the rest of the work after "I" write the code, right? No. If you are throwing stuff like this over the fence and hoping for the best, stop. Get some help. I've been there, and I got fired for this.

This approach doesn't work because these PRs are harder to review than they are to write. Putting out bad PRs is a net negative contribution on your team. The merge rate on these shotgun PRs were about 40%. 

It turns out that sometimes the code is wrong! So I set up a code review agent that checked over the production agent. I wanted to hop onto the future of software. Until the review agents started messing up, too. I mandated that tests fail before on main, and pass on branch. But it turns out that the review agents never ran the tests! So I set up another agent who was supposed to do software QA, even using checklists. I even asserted that it produce a hash of the test output as a part of its run. But sometimes it would fabricate the hash out of nowhere, just to pass the deterministic gate that I set up as a part of the pipe. 

![oss-exp-2](/assets/oss-exp-2.png)

Yes, my software factory was catching more mistakes but I could never really be sure if they were fully reliable. I am babysitting these agents. What was I doing wrong? Could I ever trust these ephemeral coding agents who pat themselves on the back when they think they're done? How do I trust these agents? 

How do I trust agents when they confidently lie, cheat, make mistakes, then disappear. They will never be fully deterministic genies that do the job perfectly. The only way to get reliable results is to rely on the results and not the agent. Could this be the lesson? That the work should stand on its own? Demand that your agent produce evidence and proof of its work rather than a confidence score. Confidence scores are lies. 

What's the difference between trust and evidence? 

![trust-chain](/assets/trust-chain.png)

Trust is fragile because it's only as strong as its weakest link. You might trust your coworkers, but do you trust their trust in agents? Trust decays. And when stuff breaks in prod, investigations have to be repeated and attribution turns into a blame game. 

![evidence-pointer](/assets/evidence-pointer.png)

When you have evidence, you no longer have a chain of attestations. If anybody can verify it independently, it doesn't matter who said it, so you can leave them out of the picture. If your agents can't provide evidence to back up their claims, it's worse than useless.

So what is evidence? 

![claim-procedure](/assets/claim-procedure.png)

Evidence is a tuple of a claim and its procedure. You need both. A claim without verification steps is untrue, and a procedure without a claim is meaningless. When a claim is presented, it must be falsifiable and verifiable. Think of the scientific method and why it works better than a vibe check. It includes a procedure for reproducibility so that the conclusion can be drawn if the same procedures are followed. I call this verifiable knowledge.

![github-sankey](/assets/github-sankey.png)

Here's an example of verifiable knowledge. I got over 100 PRs merged to other peoples' github repos since May. You can either believe me or ask your agent to verify. My handle kimjune01. Github has an API that your agent can query. Your agent can help you write this query and you can copy paste it into a terminal so that there is no agent involved when it's run. 

Before you checked it, you didn't know for sure whether my claim is true or not. It's true to me, but that didn't matter to you. I'm just a guy talking on stage. Knowledge is subjective. My job as a stranger is to give you the means to check for yourself. Just like me, your agent is a stranger, too. You should ask your agent to provide a procedure to verify its work independently, to assemble the evidence tuple. That's how you know your agent is done. Never trust your agents. They don't care about you.

![openhands-pr](/assets/openhands-pr.png)

So hopefully by now I've convinced you that evidence is a better measure of agent output than a vibe check. Since I adopted it, my merge rate has increased to about 80%. For evidence, check OpenHands Github repo. They are the most AI-forward open source repo that I know of. Every one of their PRs contains both the claim and its verification procedure. 

![division-of-labor](/assets/division-of-labor.png)

Us humans should be doing what we're good at. Describing problems to motivate agents; managing scope and interface boundaries; aligning agents to the goal of your organization. Agents can do what they're great at: writing code and tests; gathering and presenting evidence; investigating faults using that evidence. We are not substitutes to the machine. We complete one another.

So if verifiable knowledge is applied to humans and agents alike, you will start acting like open source maintainers, keeping a high quality bar and trusting noone.

You may think that this is common sense, like how we learned the scientific method in high school. But providing verifiable knowledge with every PR is a bar raiser for the whole team. When you expect evidence from each other, you'll have higher quality and less rework. You will make mistakes easier to catch, and merge fewer mistakes to prod. 

I wish I could talk to you more about agents, open source, epistemology and methodology, but I'd rather save time for questions. 

