---
variant: post-medium
title: "StarCraft 2 Is the Ideal Benchmark"
tags: cognition
image: "/assets/sc2-benchmark.jpg"
---

In 2012, a convolutional neural network won the [ImageNet Large Scale Visual Recognition Challenge](https://en.wikipedia.org/wiki/ImageNet#ImageNet_Challenge) by a margin that ended the debate. [AlexNet](https://en.wikipedia.org/wiki/AlexNet) didn't invent deep learning; [Hinton](https://en.wikipedia.org/wiki/Geoffrey_Hinton)'s group had been publishing for years. What changed was the stage. One number, one leaderboard, one undeniable comparison. The field reorganized within months.

AlexNet is remembered as the breakthrough. ImageNet made it visible.

### Real work, invisible results

Soar has planning, online learning, means-ends analysis, chunking, interactive task learning. The [Thor-Soar](https://soar.eecs.umich.edu/) agent navigates a kitchen, cooks food, and learns new tasks from instruction. It perceives through three levels of vision, plans with iterative deepening and temporal reasoning, and learns by chunking over look-ahead.

That's real. And nobody outside this community knows.

The first problem is *legibility*. Thor-Soar results appear against Thor-Soar baselines in Thor-Soar papers read by Thor-Soar researchers. The broader AI community can't tell whether Soar competes with neural methods on anything, because the results never share a scoreboard. Neural nets became undeniable because improvement was visible on shared benchmarks, year after year. Cognitive architectures had papers.

The second problem is *self-measurement*. When Soar gets a new learning mechanism or version release, "did it help?" resists easy answers. Each group runs their own eval on tasks designed to show the improvement. We can't even tell ourselves whether we're making progress.

The third problem is *isolation*. Soar, [ACT-R](https://en.wikipedia.org/wiki/ACT-R), [CLARION](https://en.wikipedia.org/wiki/CLARION_(cognitive_architecture)), [LIDA](https://en.wikipedia.org/wiki/LIDA_(cognitive_architecture)): each operates on separate benchmarks, publishes in separate venues, and measures against separate baselines. No honest way to compare architectures against each other, let alone against neural methods. The field fragments instead of accumulating.

One benchmark fixes all three.

### Machine speed or nothing

ImageNet worked because anyone could download it and run it. No lab, no robot, no custom simulator. A group with a good idea and a commodity GPU could produce a result the entire field had to take seriously.

Cognitive architectures need the same property: machine speed on commodity hardware. Not a robotics platform. Nobody is downloading and printing robots. Not a household simulator with a custom task ontology. A platform anyone can access, where experiments run fast enough to iterate, and results mean something to people who've never heard of Soar.

### StarCraft 2

SC2 demands real cognition: partial observability, real-time decisions, long-horizon planning, opponent modeling, resource management, multi-scale reasoning from unit micro to global strategy. Go has planning depth but no partial observability, no real-time pressure, no resource management. Atari has real-time perception but no opponent modeling and no long-horizon strategy. SC2 requires all six simultaneously.

It runs at machine speed. [PySC2](https://github.com/google-deepmind/pysc2) and the [SC2 API](https://github.com/Blizzard/s2client-proto) exist: thousands of experiments per day on a laptop. There's precedent, too: [SORTS](https://cdn.aaai.org/ojs/18783/18783-52-22481-1-10-20210929.pdf) (Wintermute, Xu, and Laird) won two of three categories at the AIIDE 2006 RTS competition using Soar's attention, perceptual grouping, and hierarchical task decomposition. [Soar-SC](https://github.com/bluechill/Soar-SC) later connected Soar to Brood War with spatial reasoning via SVS. The interface works. The question is how far we push it.

SC2 also exposes the axis where cognitive architectures hold a structural advantage.

[AlphaStar](https://www.nature.com/articles/s41586-019-1724-z) reached Grandmaster level. It also trained on millions of games with a population of agents competing against each other for weeks. A cognitive architecture that adapts mid-game, or across five games instead of five million, demonstrates something categorically different: a different kind of intelligence, measured on the same task.

- *Learning speed.* How many games to adapt to a new opponent's strategy? A system that learns in real-time, from one game, does something RL cannot.

- *Adaptation.* When the opponent switches strategies, does the agent notice and respond because it *reasons* about what changed?

- *Explainability.* After the game, can the agent say what it learned? Neural nets produce win rates; cognitive architectures produce rationales. Both playing the same game makes the difference visible.

The goal: demonstrate that learning actually happens: visibly, measurably, in a domain the world already understands.

### What one benchmark buys

- *External legibility.* The ML community already knows SC2. A Soar agent that adapts mid-game on a public leaderboard produces a result anyone can interpret. No translation needed, no "well, in our eval framework..." caveats. One game, one number, one comparison.

- *Internal engineering.* A stable benchmark turns every architectural change into a measurable experiment. Did episodic memory improve adaptation speed? Run SC2, compare the curve. Did chunking changes affect planning depth? Run SC2, measure. Every release gets a number; progress becomes cumulative instead of anecdotal. ImageNet did this for CNNs: dropout, batch norm, residual connections, each validated against the same task. The benchmark turned intuitions into engineering.

- *Cross-community challenge.* Same scoreboard for every cognitive architecture. Soar, ACT-R, CLARION: bring your agent, run the games, publish the results. When results go public, the question shifts from "is architecture X making progress?" to "which architecture learns fastest, and what does that tell us about the mind?"

- *Built-in generalization.* Three races, six matchups, each strategically distinct. Terran vs. Zerg plays nothing like Protoss vs. Protoss. An agent that handles multiple matchups demonstrates transfer, and the test is built into the game. No second dataset, no held-out distribution.

- *No ceiling.* Kitchen task benchmarks can be beat. Lexical processing benchmarks can be beat. You solve them, move on, and the benchmark dies. ImageNet itself saturated: top-5 error dropped below human performance and the leaderboard stopped driving progress. SC2 resists saturation because it's adversarial: every improvement invites a counter-strategy; every counter-strategy demands further adaptation. The benchmark stays hard because the opponent distribution evolves.

### The ladder already exists

[AI Arena](https://aiarena.net/) runs a live SC2 bot ladder with regular tournaments, public Elo, and thousands of matches. Most bots are hand-coded expert systems: scripted builds, hardcoded responses, no learning. A cognitive architecture agent could enter tomorrow.

The honest worry: what if we lose to expert systems? Good. That's informative. An agent that loses to scripts in month one and beats them in month six tells a better story than a paper claiming victory on a private benchmark. The learning curve *is* the result.

We're not protecting a market cap. We can afford to lose, learn, and improve in public. The ladder is a lab notebook.

And it's fun. You build an agent, put it on the ladder, and watch it play. It does something you didn't anticipate, disappointing or flabbergasting, and you learn either way. That's why people got into cognitive architecture: to build something that thinks and watch it try. SC2 lets you do that every afternoon.

### Build the stage first

There's no agent to demo yet. The highest-leverage thing the cognitive architecture community could do right now is agree on a benchmark.

ImageNet created AlexNet. The benchmark came first. The breakthrough followed because the stage was already built: every year the leaderboard updated, every year the gap between "promising research direction" and "the future of AI" narrowed, until one result closed it.

Cognitive architectures are waiting for that result. But you can't have an AlexNet moment without an ImageNet.

If Soar is intelligence encoded, it should prove it, or lose trying. Build the stage; see who shows up.

### Slides

<iframe src="https://docs.google.com/presentation/d/1vooxr8rQZ8v4avJSixzYVClh_PaDEQ9Cwc4omZOTLCM/embed?start=false&loop=false&delayms=3000" frameborder="0" width="700" height="422" allowfullscreen="true"></iframe>
