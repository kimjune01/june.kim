---
variant: post-medium
title: "Type the question"
tags: methodology, cognition, coding, reflecting
---

March 2020. Public health agencies around the world had the same question: what happens if we shut down? Much of the early modeling reached for statistical extrapolation of case counts and deaths. The forecasts came back fast and confident. Many were structurally wrong, not because the statistics were sloppy, but because the question was not the kind a curve-fitting model can answer.

The default working idiom of statistics, the version most people learn first and reach for under deadline, estimates parameters of a fixed distribution from a sample. The distribution is assumed to sit still; the sample, not to perturb the system. Time, when it appears, is another column to compute averages over. The field has more sophisticated branches that relax these assumptions, but the default idiom is what gets reached for first, and it did not match what March 2020 actually was.

March 2020 was a feedback loop with delays. Deaths rise, fear rises, behavior changes, transmission drops, deaths fall, fear falls, behavior reverts, transmission rises, deaths rise. There is no fixed distribution to sample from — only a system that responds to the fact that you are watching it, and the response *is* the phenomenon. You can fit a regression to early-March case counts and get a tidy number with a confidence interval. The number is computable. It is also structurally beside the point. The model has no way to flag the difference, because it has no concept of the difference.

What the model was missing is the right **data structure** for the question. The question was about a dynamical system. Dynamical systems live in phase space, evolve under differential equations, and are reasoned about by sketching the geometry of their trajectories. None of that is in a regression. You cannot fix a regression by being smarter inside it. You have to switch to a different mathematical object.

## Methodology is a type system

This, I think, is what the methodological canon has been about for four hundred years. It is a sequence of **data structures**, each capable of holding a different shape of question, each with its own operations. Three carry most of the weight in modern empirical work:

- **Statistics** gives you a bag of samples plus an assumed distribution. Supported operations: estimate parameters, compute intervals, test distributional hypotheses. [Tukey](https://en.wikipedia.org/wiki/John_Tukey) is the saint of doing this honestly at the *exploratory* stage. The broader canon runs through [Fisher](/reading/scientific-method/fisher-1935/), Neyman, and Box, who build the inferential machinery. The slogan that escaped Tukey's work is *look at the data*.
- **Pearl-style causal inference** gives you a directed acyclic graph plus observational or interventional data. Supported operations: identify causal effects, derive sufficient adjustment sets, compute counterfactuals when the graph admits them. The phrase that circulates in the methods literature is Miguel Hernán's [*draw your assumptions before your conclusions*](https://harvardonline.harvard.edu/course/causal-diagrams-draw-your-assumptions-your-conclusions); my shorter version is *draw the DAG*.
- **Dynamical systems** gives you a state vector evolving under differential equations. Supported operations: find fixed points, classify stability, sketch phase portraits, predict trajectories under perturbation. [Poincaré](https://en.wikipedia.org/wiki/Henri_Poincar%C3%A9) founded this way of reasoning in the 1890s when he gave up on closed-form solutions to the [three-body problem](https://en.wikipedia.org/wiki/Three-body_problem) and started reasoning about the geometry of trajectories instead; [Strogatz](https://en.wikipedia.org/wiki/Steven_Strogatz) teaches the modern working version, and [Kermack–McKendrick](https://en.wikipedia.org/wiki/Kermack%E2%80%93McKendrick_theory) adapted it to epidemic dynamics in the 1920s. The slogan, when it has one, is *draw the phase portrait*.

Each structure can answer questions the others structurally cannot. Each one will also *silently fail* when you ask it the wrong kind of question. This is the move that took me until this afternoon to see clearly. *When a published finding is confidently wrong rather than just noisy, the failure is often a type error: someone fed a model a data structure whose shape didn't match the question they were asking.*

## Empirical methods have no compiler

A type error in programming is what happens when you try an operation that does not make sense for the data structure you have. Adding a string to an integer. Indexing into a number. Calling a method on null. In a typed language the compiler catches it. In a dynamic language the runtime crashes or returns an obviously wrong result with a stack trace. In every case, the system tells you the question does not fit the shape of the thing you asked it about.

Empirical methodology has no compiler. When you feed a sample-from-distribution structure to a statistical model and ask it a causal question, the math does not refuse. It returns *something*. The answer is garbage, but no error is raised.

The [replication crisis](/reading/scientific-method/ioannidis-2005/) has many causes: publication bias, p-hacking, underpower, measurement problems, researcher degrees of freedom, and outright fraud all do real work. Running alongside them is a more basic one: an entire field's analyses do not type-check, and no one tells anyone. People who would never add a string to an integer happily compute Pearson correlations and publish them as treatment effects. They get away with it because nobody ran the type checker on the question first. There is no type checker.

Each framework's slogan is an imperative to externalize the structure before you trust the output. *Look at the data* means inspect the input before you trust the type. *Draw the DAG* means declare your causal assumptions so they can be audited. *Draw the phase portrait* means sketch the trajectories so the dynamics can be checked. Three frameworks, one move: *externalize the data structure so it can be checked*.

## ML scales the type error

Modern machine learning is the worst possible place for this insight to land. Deep learning models fit any function you put in front of them. They will fit a static-distribution structure to a dynamical question and report regularities that vanish the moment the system shifts regime. They will fit an associational structure to a causal question and report effects that disappear under intervention. Scaling laws make the answers more confident. They do not make them right.

*Rigor is about typing the input.* Step zero is asking what shape your question has and which data structure can hold it. Almost nobody is taught to make this choice consciously. It gets made anyway, by default, based on whichever framework the analyst learned first. The default is almost always statistics, because that is what introductory courses teach and journal reviewers expect. So statistical models get fed causal and dynamical and feedback questions, and the models return numbers, and the numbers go into papers, and nobody flags the type mismatch because the field has no language for it.

Step zero: type the question. The rest of the methodology is downstream of that, and so are you.
