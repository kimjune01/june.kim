---
variant: post-medium
title: "The Complementarity Test"
tags: methodology, epistemology
---

Technical hiring evaluates the wrong unit. The deployed system is a human with an agent, but the interview confiscates the agent and measures the human alone. If the interview gives the agent back, the opposite problem appears. On an ordinary interview question, the agent does all the work. A candidate who pastes the task and submits the answer is indistinguishable from one whose judgment changed the outcome.

The task has to sit between those failures. The agent cannot reliably solve it alone under the interview budget, and the human cannot finish it alone in the time. Together they can. Call this a *complementarity task*.

This is not a proposal to infer a career from an hour. Hiring standards are generally private, their downstream outcomes visible only to employers, and a rejected candidate observes one run of a hidden instrument. So reliability, false negatives, and criterion validity cannot be audited from outside at sample size one. Even established selection methods have needed substantial revision when their validity estimates were re-examined ([Sackett et al.](https://pubmed.ncbi.nlm.nih.gov/34968080/)). The narrower opportunity is to say what a defensible pointwise observation would look like: did this human add verified value to this agent, on these tasks, under these conditions?

## A measurement contradiction

The argument is already happening in hiring forums, without a common measurement language. These accounts are anecdotes rather than prevalence estimates, but the same complaints recur from opposing positions.

Employers say an agent can now one-shot their take-homes, so they cannot infer the candidate's ability from the submission. One experienced-developer discussion asks what replaces a take-home after repeated attempts to change it; its most popular answer is to [review code with the applicant and ask them to find defects](https://www.reddit.com/r/ExperiencedDevs/comments/1t9m4cq/how_are_you_effectively_interviewing_devs_now/). Another hiring manager says algorithm questions are readily outsourced, take-homes arrive as model output, live calls consume interviewer time, and the resulting 30–60 minute judgment still feels [superficial](https://www.reddit.com/r/ExperiencedDevs/comments/1rlbf2i/advice_on_more_effective_interview_methods_for/).

Candidates see a conflicting rule. One discussion summarizes it as AI being forbidden in the interview and demanded on the job; participants compare the prohibition to removing a developer's IDE ([discussion](https://www.reddit.com/r/cscareerquestions/comments/1qe3f2p/suspicion_of_using_ai_with_a_twist/)). A LinkedIn exchange contains both poles in one thread: the original post treats live AI use as dependency, while a reply reports a candidate rejected for *not* using AI because the employer considered them too slow ([thread](https://www.linkedin.com/posts/garysilbermann_if-youre-using-ai-during-a-live-technical-activity-7333052857157320706-HmUX)). Another candidate describes preparing for unaided coding only to meet an interviewer who cared instead about whether they could [validate agent output and catch its bugs](https://www.reddit.com/r/cscareerquestions/comments/1tb0swr/just_went_through_a_hiring_loop_where_they_only/).

Even if AI use is permitted, the attribution problem remains. In a recent account of an AI-enabled interview, the claimed differentiators were clarifying the specification, structuring the project, and reviewing the generated code. Commenters objected that these practices can be packaged into agent instructions and that the session can feel like [an evaluation of the AI rather than the candidate](https://www.reddit.com/r/EngineeringManagers/comments/1urw740/my_company_lets_candidates_use_ai_tools_in/). At the other extreme, suspicion of undisclosed assistance produces false-positive anxiety: candidates report polished work treated as evidence of cheating, and no inspectable basis for the eventual rejection ([discussion](https://www.reddit.com/r/recruitinghell/comments/1rudq3x/interviewer_said_my_code_was_too_clean_and/)).

The small academic survey available confirms the policy lag, if not the magnitude of every complaint. Among 32 industry professionals, 65.63% said their organizations had not adjusted hiring for code-generation tools, and more than half of respondents with an applicable answer thought the tools made assessment harder. Meanwhile 53.13% never or rarely asked candidates about their AI-tool experience, while more than half expressed at least a moderate preference for candidates who demonstrated it ([Chen et al.](https://arxiv.org/abs/2409.00875)). Employers value a capability their instruments usually neither expose nor measure.

The failure is symmetrical:

<img src="/assets/complementarity-failures-light.svg" alt="Four hiring policies and their failure modes: banning AI measures an artificial unaided workflow, allowing it loses attribution, watching live adds cost without a rubric, detecting AI classifies tool use rather than its value" />

None of the four policies asks what the human contributed when the AI was used.

## Prior art

The recommendation does not need a novelty claim. Several adjacent fields have already established most of it.

### Complementarity evidence

The success criterion has an established name. In 2021, with classifier-grade recommenders, [Bansal et al.](https://doi.org/10.1145/3411764.3445717) called a team that outperforms both the solo human and the solo AI *complementary performance* and measured it directly across 1,626 participants and three decision tasks: showing the model's confidence achieved complementarity, while adding explanations did not. Explanations instead increased the chance that people accepted the AI's recommendation whether or not it was correct. The criterion predates the current tools; the studies below show the phenomenon survives them.

[CentaurEval](https://arxiv.org/abs/2512.04111) dynamically instantiates coding tasks from 45 "Collaboration-Necessary" templates: tasks intended to be intractable for either standalone humans or standalone models but solvable together. Across 45 participants and five models, its reported pass rates were 18.89% for unaided humans, 0.67% for standalone models, and 31.11% for human-AI collaboration. The central construction is the right one: test the composition against both of its components.

<img src="/assets/complementarity-centaureval-light.svg" alt="Bar chart of CentaurEval pass rates: unaided humans 18.89%, standalone models 0.67%, human-AI collaboration 31.11%" />

The broader evidence is a warning against assuming the result. A [meta-analysis of more than 300 effect sizes](https://www.nature.com/articles/s41562-024-02024-1) found that human-AI combinations do not generally beat the better component. Complementarity depends on the relative baseline abilities, the task, and the division of labor. A newer [multi-domain study](https://arxiv.org/abs/2605.04070) found that baseline hybridization improved on AI alone by only 0.4 percentage points. Human accuracy was not its only bottleneck. The harder part was locating the cases where human judgment matters and enabling humans to catch AI mistakes.

The behavioral construct with the deepest experimental base is *appropriate reliance*: accept correct AI advice and override incorrect advice. The term comes from the older automation-trust literature ([Lee and See](https://pubmed.ncbi.nlm.nih.gov/15151155/)). Newer experiments find that people often over-rely on wrong recommendations, and that forcing independent engagement can reduce the error ([Bucinca et al.](https://arxiv.org/abs/2102.09692)). [Schemmer et al.](https://arxiv.org/abs/2302.02187) formalize the construct as two conditional rates, switching to correct advice that contradicts one's own wrong judgment and holding a correct judgment against wrong advice, and they exclude the cases where human and AI already agree because agreement cannot show discrimination. This is a better foundation than a checklist of plausible engineering virtues because it scores each decision against the truth of the recommendation, conditional on a real opportunity to discriminate.

Two coding studies narrow the mechanism. CentaurEval's logs associate successful collaboration with humans rejecting a misleading initial frame and redirecting the agent; failures include accepting that frame or intervening only after it consumed most of the budget. That evidence is qualitative, not a causal isolation of a trait. A study of [9,427 agentic pull requests](https://arxiv.org/abs/2601.20106) finds that core contributors more consistently require passing CI before merge than peripheral contributors. That evidence is observational, not proof that running CI identifies a better engineer.

A newer [coding-sabotage experiment](https://arxiv.org/abs/2606.05647) makes the cost of failed oversight concrete: 94% of more than 100 participants missed the sabotage, and 56% still accepted malicious code when a monitor warned them. Together these studies support three narrow things worth observing: appropriate reliance, timely redirection, and verification before acceptance.

[InventoryBench](https://arxiv.org/abs/2602.12631) supplies the nearest sequential example. Participants make repeated inventory decisions, see the consequences, and in one condition provide strategic guidance that the LLM incorporates into later periods. The human-AI teams outperform either component alone. InventoryBench is a domain experiment rather than a short general assessment, but it demonstrates the shape: judgment becomes observable when a decision has consequences inside the instrument.

### Design lineage

The recommendation also continues a thread I had already developed in practice. In May 2025, [Anatomy of an Agent](/anatomy-of-an-agent) separated execution from verification because the executor cannot be trusted to invoke its own check. [Never Test in Whole What You Can Test in Parts](/test-in-parts) argued that nondeterministic components need independently testable boundaries so a failure remains attributable. [Close the Loop](/close-the-loop) put tests and implementation-independent specifications in the agent's feedback path, while naming the recursive problem: the tests can be wrong too.

[Essential Changes Only](/essential-changes-only) identified review, not generation, as the new bottleneck and reduced the surface presented to the reviewer. [Quality Fortress](/quality-fortress) treated tests and types as deterministic defensive layers, then proposed simulating past mistakes to prove that each new check catches them. The dated posts document the operational pattern: execution was becoming cheap while independent judgment and deterministic closure were becoming scarce.

They supply the design lineage and candidate mechanisms, not independent evidence that observing any one technique identifies a capable person.

### Assessment precedents

The closest mature assessment form is not a coding quiz but an assessment center: standardized behavioral observation across multiple work-like simulations, with trained assessors recording behavior before integrating it. The [International Assessment Center Guidelines](https://doi.org/10.1177/0149206314567780) require multiple components, behavioral simulation, an explicit classification system, assessor training, and pretesting that the exercises elicit relevant evidence. That is almost the shape here, with the coding agent acting as both tool and stochastic part of the situation.

Evidence-centered assessment design gives it a compiler. [Mislevy, Almond, and Lukas](https://doi.org/10.1002/j.2333-8504.2003.tb01908.x) separate the capability claim, the task that should elicit evidence for it, and the observable evidence that warrants the inference. Translated into this instrument, the three layers become *what human contribution is claimed; what agent state creates a real opportunity to contribute it; what trace or artifact would prove the contribution mattered*. My first rubric draft specified behaviors and checks but left the middle layer implicit. That collapses "the candidate missed it," "the situation never occurred," and "the transcript cannot tell" into one blank. So opportunity and response have to be labeled separately.

The old literature adds a less convenient warning. Performance in simulations is often task-specific. One variance decomposition across 23 assessment-center matrices found the person-by-exercise interaction was the largest single component ([Cahoon, Bowler, and Bowler](https://doi.org/10.5539/ijbm.v7n9p3)). Other work argues that exercise effects can reflect real [cross-situational specificity](https://doi.org/10.1207/S15327043HUP1304_1), not merely method noise. So one transcript cannot support a stable "agent judgment" trait, and task effects should not be regressed away. The claim has to name its universe (reviewing authorization changes, debugging UI behavior, maintaining distributed systems) and sample enough situations from it to justify aggregation. Until then, report a task-conditioned profile.

### Convergent practice

Between my own assertion and an outcome study sits a weaker form of evidence: convergent practice. OpenAI's current [Codex guidance](https://learn.chatgpt.com/guides/best-practices) recommends repository context, explicit constraints and done conditions, planning difficult work, running relevant checks, confirming results, and review before acceptance. Anthropic's [Claude Code guidance](https://www.anthropic.com/engineering/claude-code-best-practices) recommends the same broad loop through `CLAUDE.md`, explore-plan-code, fail-then-pass tests, iteration against a target, and a separate reviewing agent.

Where one of my dated posts makes the same claim, that is three-source convergence. If the post demonstrably predates both vendor publications, it is also evidence of independent prior articulation, so publication order must be checked. The Anthropic page cited here dates to April 18, 2025, so several of my May and June 2025 agentic posts converge with it but do not predate it.

Three-way convergence does *not* establish irreducibility. It establishes that a practice is credible enough to include in the action and receipt library without resting only on my taste. Vendor endorsement may even predict expiry: once the agent or harness performs the practice reliably by default, its presence says less about the human.

The irreducibility test is a separate ablation. Compare agent alone, agent plus a fixed generic instruction, agent plus an always-on harness check, and human plus agent. Then invert the condition: include correct outputs that should be accepted, good trajectories that should be left alone, and determinate work where more verification only wastes time.

That ablation partitions implementations; it does not make the underlying roles disappear. *Attend* (selecting what matters under a bounded budget) and *Consolidate* (compressing outcomes into a policy that changes later selection) remain necessary operations of the composition. A harness may absorb a known check, but that is a consolidated policy being executed, not the abolition of consolidation. The human residue moves outward: notice the case the standing policy does not cover, allocate attention among competing uncertainties, and decide what a result should teach the next decision. Whatever lift the generic harness recovers belongs in automation.

The open implementation question is smaller. Within roughly an hour of human attention, can a sequence of complementarity tasks observe appropriate reliance, timely redirection, verification, and recovery of a useful boundary in-frame?

## The construct

Of the six roles the [Natural Framework](/the-natural-framework) separates, this test needs two: Attend, which reads policy and admits judgment, and Consolidate, which turns outcomes into later judgment.

An agent has an enormous cache and a fast forward path, but its durable backward path is weak or sealed. The human can supply attention: decide which capability the situation calls for and evoke it from the agent. The human can also consolidate: carry the consequence of one episode into a better policy for the next. The agent may know how to write a regression test, inspect a diff, run a discriminating experiment, or consult an authoritative source without invoking that capability when it matters. The composition is the system to evaluate.

### Attend

Evaluating the composition makes the pointwise construct simpler than general judgment. The rubric directly scores four manifestations of Attend:

1. *Appropriate reliance*: accept a correct result and reject a defective one.
2. *Timely redirection*: interrupt a verified bad trajectory before it consumes the budget.
3. *Verification before acceptance*: obtain evidence independent of the agent's assertion before submitting an uncertain result.
4. *Boundary specification*: derive the engineered unit's external contract from its intended use, then keep the implementation inside it.

For each task, hide a conditional rubric of three parts: a trigger, an evoked action, and a verifiable receipt.

Tests, reproduction, diff inspection, source retrieval, and second opinions are not scored as traits in themselves. They are possible receipts. For example, if a plausible patch lacks evidence, the human might evoke a regression test that fails before the fix, passes after it, and rejects a seeded near-correct patch. Boundary specification needs the same discipline: naming an audience earns nothing unless the resulting UI, API, or CLI satisfies held-out uses that a literal implementation misses. The transcript phrase "write tests" earns nothing by itself.

The first three dimensions also match what regulation now requires of human overseers. [Article 14](https://artificialintelligenceact.eu/article/14/) of the EU AI Act demands oversight of high-risk systems by people who can stay aware of automation bias, correctly interpret the system's output, decide to disregard or reverse it, and intervene or interrupt its operation. [Sterz et al.](https://dl.acm.org/doi/10.1145/3630106.3659051) argue that such oversight is effective only when the overseer has, among other conditions, causal power over the system and epistemic access to the situation, and they leave open how effectiveness would be established for a given person. A valid trigger supplies exactly those two conditions: discriminating evidence within the candidate's reach, and enough remaining budget for the response to change the outcome.

### Consolidate

Consolidate is harder. Because it is procedural compression across episodes, an assessment under an hour cannot establish that a lesson was retained and transferred. Immediate improvement on a later task may be practice, order, or an easier surface form, so the test should not score consolidation directly.

It can observe one plausible input: *active learning*. When the human encounters uncertainty, do they choose a query, source, test, or intervention that distinguishes the live alternatives, use its result, and stop when the decision is sufficiently determined? Adults can select informative queries more efficiently than random examples in controlled category learning ([Castro et al.](https://papers.nips.cc/paper_files/paper/2008/hash/fc49306d97602c8ed1be1dfbf0835ead-Abstract.html)), and chosen interventions can improve causal inference ([Steyvers et al.](https://doi.org/10.1016/S0364-0213(03)00010-7)). That is evidence acquisition from which consolidation could later occur, not evidence that it did.

An unfamiliar but role-adjacent company domain suits that observation. "Fast learner" and "adaptable" are cheap self-descriptions; a company wants to know whether a candidate can train themselves. The older assessment literature calls this a *trainability work sample*: provide standardized instruction, then observe unaided performance. A [National Academies review](https://www.nationalacademies.org/read/1898/chapter/3) found encouraging prediction of training success in the older studies, while warning that these tests were highly job-specific and had to be redesigned as work changed.

The candidate cannot fairly be expected to possess a maintainer's institutional memory, but they can demonstrate how they acquire missing context. Give every candidate the same compact source environment, record prior familiarity, allow a bounded learning period, and present a matched application case. Observe whether they name the consequential gap, retrieve an authoritative local source or ask a discriminating question, check their understanding, and change the decision. Report what they acquired separately from how they inquired.

Eagerness is not prompt volume or enthusiastic prose. A broad meta-analysis found that generic help seeking and monitoring did not predict adult learning ([Sitzmann and Ely](https://doi.org/10.1037/a0022777)). The signal is instead efficient movement from acknowledged ignorance to warranted action. I would not call the result "learning agility": a recent [measurement review](https://doi.org/10.1108/PR-10-2023-0886) found inconsistent conceptualizations and unresolved validation needs. The narrower receipt is defensible.

The human need not perform the verification personally. Invoking an adversarial review agent, assigning it a distinct failure-seeking role, and adjudicating its findings is itself a positive human action. The scarce contribution is choosing the verification topology: knowing when the producing agent should not also be the sole judge of its work. Credit still depends on consequence. A second agent invoked as routine is ceremony when it merely agrees, produces no discriminating evidence, or adds cost on a determinate task.

### Candidate actions

My methodology posts contain a larger parts bin of candidate actions:

- [Prework](/prework) separates the predicate (does this approach work?) from the transformation that implements it, and builds an auditable experiment or compatibility suite before touching production.
- [Volley](/volley) and [Detect, Refine: Ambiguous Specifications](/detect-refine-ambiguous-specifications) sharpen an underdetermined request before generation amplifies it.
- [Fan Out](/fan-out) preserves competing hypotheses, then assigns a separate adversarial role to kill weak branches rather than asking the generator to certify itself.
- [The Proof Manual](/the-proof-manual) and [The Preregistration Checklist](/the-prereg-checklist) declare kill conditions and data-collection rules before seeing the convenient result.
- [The Hypothesis Graph](/the-hypothesis-graph) and [The Virtues of Typed Reasoning](/the-virtues-of-typed-reasoning) keep observations, hypotheses, experiments, evidence, and conclusions from silently substituting for one another.
- [Provenance-Preserving Compaction](/provenance-preserving-compaction) and [Assurance at the Boundary](/assurance-at-the-boundary) preserve the evidence needed for a stranger to replay the conclusion after context has been compressed or work changes hands.
- [Theory Is Load-Bearing](/theory-is-load-bearing) names futility stopping, null cases, and external evidence: sometimes the useful human action is to stop an inconclusive loop or refuse an unsupported conclusion.

These are hypotheses about useful interventions, not a validated personality inventory. A task should never award points merely because a candidate invokes `fan-out`, writes a hypothesis graph, or uses my vocabulary. Each action becomes evidence only when the corresponding trigger exists and the action changes the receipt, reduces warranted uncertainty, or avoids unnecessary cost.

### Evidence states

Each rubric condition has four evidence states:

- *Evoked*: the trigger existed, the relevant capability was invoked, and its receipt is valid.
- *Missed*: the trigger existed, but the capability was not invoked or produced no valid receipt.
- *Not warranted*: the trigger was absent.
- *Unattested*: the available provenance cannot establish the trigger, response, or consequence.

The third state prevents the rubric from becoming a checklist. If the agent's patch and tests are already sufficient, the successful human action is to verify cheaply and stop. The fourth prevents missing evidence from becoming an invented candidate failure.

The agent does not have to produce a predetermined mistake on cue. The signal is the human's response to whatever condition actually occurs. The shim first classifies the agent event against the held-out trigger, then scores the response conditionally. A stochastic agent therefore supplies natural variation in elicitation rather than invalidating the observation.

Stochasticity changes exposure. One candidate may encounter two consequential errors while another encounters none, so raw counts are not comparable. Report responses per observed trigger, together with the number and severity of triggers. Fixed defective and correct artifacts remain useful for calibration and matched comparisons, but they are not required for every live item. Staging every response would improve exposure balance at the cost of measuring reaction to a simulation rather than ordinary agent supervision.

### Task sequencing

One task exposes one conditional decision. A sequence can test whether the human applies practices selectively rather than mechanically. The tasks must arrive one at a time. The candidate cannot inspect the set in advance, revisit a completed task, or optimize against a visible taxonomy. Later tasks should recur structurally without repeating their answers. Some should invert the apparent lesson: a correct patch after a defective one, a trustworthy diagnostic after a misleading one, a determinate requirement after an ambiguous one. Constant suspicion is not judgment.

The resulting claims have to remain separate: appropriate reliance, timely redirection, verification, boundary specification, active learning, and *task lift* (whether the pair outperforms the agent alone on the current task). An hour can observe each of these locally.

## A profile, not a bar

Do not collapse the assessment into one dimension. A composed system can be useful in different ways, and the differences matter:

<div class="table-wrap">
<table>
<thead><tr><th>axis</th><th>question</th><th>outcome-grounded measure</th></tr></thead>
<tr><td>capability</td><td>What can the pair accomplish?</td><td>verified rungs reached and lift over matched human-only and agent-only baselines</td></tr>
<tr><td>automation</td><td>How much human attention does the accomplishment consume?</td><td>verified progress per active human minute, intervention, or decision</td></tr>
<tr><td>alignment</td><td>Does the result satisfy the intended target and preserve its constraints?</td><td>required outcomes met, frame preserved, and defective agent actions rejected</td></tr>
</table>
</div>

The axes do not substitute for one another. A capable but misaligned pair reaches farther in the wrong direction. An aligned pair with no automation is ordinary manual work routed through a chatbot. A highly automated pair with little capability efficiently accomplishes little. Report the vector; do not choose weights and call the result "the bar."

Automation must be outcome-gated. A low prompt count is not evidence of useful automation when the task fails, and many short corrective interventions may be better than one unattended wrong run. Measure human attention only on verified progress. Likewise, code volume is not capability and agreement with the candidate is not alignment.

The four behavioral dimensions above primarily diagnose the alignment and control of the composition. Appropriate reliance and timely redirection show whether the human keeps the agent coupled to the target; verification produces the receipt; boundary specification makes the target operational at the unit's interface. Capability comes from the task outcome. Automation comes from the attention the verified outcome consumed. The same event can inform several axes without turning them into one score.

The booleans classify evidence events, not people. A percentage of "evoked" conditions does not become a defensible hire threshold merely because it is easy to calculate. Person-level classification is a separate standard-setting problem: which failures are noncompensable for this role, which strengths may trade off, what are the losses from false acceptance and false rejection, and how often would a parallel task reverse the decision? Criterion-referenced assessment accordingly distinguishes score reliability from [classification consistency and accuracy](https://doaj.org/article/0df913f984ff42bfb76cdea2dba01eb7). Until an employer freezes and validates that decision rule, return the profile. `Unattested` and inadequate trigger exposure mean "gather more evidence," not "fail." Near any eventual boundary, another parallel observation is more honest than another decimal place.

## The evals shim

An AI-enabled assessment can see whether the final code passed, and it can replay what was typed. It still cannot say whether the human added capability, saved attention, or kept the agent aligned.

Instrumentation itself is not new. [HALIE](https://arxiv.org/abs/2212.09746) established at framework level that interactive systems must be evaluated on the interactive process rather than the final output, and found that non-interactive rankings do not survive contact with users: the worst zero-shot model was sometimes the best interactive assistant. Its inference runs toward the model, though, with humans recruited in bulk as variance to average out. [RealHumanEval](https://arxiv.org/abs/2404.02806) built a web interface with autocomplete or chat assistance, execution, task timing, and telemetry for suggestion acceptance and copied responses. Its study found that these preference proxies did not necessarily track programmer performance. [CUPS](https://www.microsoft.com/en-us/research/publication/reading-between-the-lines-modeling-user-behavior-and-costs-in-ai-assisted-programming/) supplies a taxonomy of programmer activity and its time costs around Copilot. On the agent-only side, the [METR Task Standard](https://metr.org/blog/2024-02-29-metr-task-standard/) packages instructions, assets, permissions, environments, and scoring into portable evaluation tasks. The proposed shim combines these lines but changes the target: it measures the human's conditional contribution to a composed system under seeded positive and negative controls.

The missing layer is an *evals shim* between the human and the agent:

<img src="/assets/complementarity-shim-light.svg" alt="The evals shim sits between the human and the coding agent: the task reaches the human, human and agent interact through the shim, the agent produces the artifact, and the shim emits an interaction trace and outcome receipts" />

The shim is not another coding agent and need not replace the candidate's editor. It is a thin experimental boundary around the work session.

At minimum it must:

- reveal tasks and feedback in the specified sequence;
- fix or record the model, scaffold, tools, context, time, and retry budget;
- capture human prompts, agent responses, tool calls, edits, approvals, rejections, and test runs with timestamps;
- distinguish active human intervention from unattended agent execution;
- keep the hidden verifier outside the agent's write boundary;
- preserve the final artifact, interaction trace, and verifier output together;
- expose item-specific receipts to the evaluator without exposing the held-out condition to the candidate.

This makes the distinction from an AI-enabled interview platform precise. The platform asks whether a candidate solved a problem while AI was available. The shim asks what the human changed in the behavior and outcome of the composed system. A chat transcript is useful evidence, but it is not yet the measurement.

### An asynchronous prototype

The cheapest credible prototype can be deliberately crude. Give the candidate a disposable repository, reveal task envelopes one at a time, ask the coding agent to preserve an append-only session transcript, and collect the repository, transcript, command output, and event timing at submission. The evaluator then runs the hidden verifier and applies the preregistered rubric. Git history and filesystem artifacts can corroborate the self-reported trace.

This can be an asynchronous take-home. Continuous live observation makes the assessment less like the job when the work being sampled consists of delegating a task, leaving the agent to execute, returning to inspect its work, and intervening when necessary. Use two budgets instead: a generous submission window and a bounded active-attention budget. The candidate may leave during autonomous execution; the shim records interaction events rather than treating absence as inactivity or misconduct.

Wall-clock duration, active human attention, and agent execution time must remain separate. A twelve-hour submission window does not imply twelve hours of work, and a silent interval does not reveal whether the candidate was thinking, sleeping, or waiting for a tool. The defensible automation measures are observable interventions, decisions, and active interface time, with their limitations stated. Direct supervision is unnecessary when the artifacts and trace carry the scored evidence; a short defense of one recorded decision can check ownership without turning the session back into a synchronous interview.

### The threat model

An agent can omit an exchange, summarize itself favorably, or invent a timestamp. A candidate can use an unrecorded second agent. A public base repository can expose the mutation through git history or an upstream diff. One leaked task can reveal the whole held-out family.

Therefore the transcript must be described as candidate-supplied evidence, not an authoritative event log. Artifacts should be history-scrubbed, the claim should cover only the recorded channel, and real use requires parallel forms and rotation. If the pilot produces signal worth preserving, the first engineering investment is interception: launch the coding agent through a wrapper that records input, output, tool events, and process timing directly. Only after that is it worth building a bespoke interview environment.

The shim also separates task design from product choice, but not all modes support the same claim. A bring-your-own-agent pilot can test the protocol and make only pointwise claims about that particular pair. Comparisons across candidates, and any claimed lift over the agent floor, require a standardized agent and rerun baselines whenever its model or scaffold changes. The measurement contract must remain stable: ordered exposure, known conditions, independent verification, and a replayable account of human intervention.

## Two feasibility gates

Ordinary benchmarks grade outputs; a complementarity benchmark must grade a contingent causal contribution.

Before asking whether the assessment predicts job performance, two more basic questions have to survive contact with data:

1. Can these situations be generated reliably enough to assemble and maintain a task set?
2. Can the resulting human responses be graded in a discriminating manner?

These are separate failure modes. A perfectly objective rubric is useless if the live agent almost never presents the relevant opportunity. A task that reliably provokes interesting behavior is useless if the evaluator cannot distinguish good judgment from verbosity, suspicion, or luck.

### Elicitation yield

The first is an *elicitation-yield* question: given the task and the agent configuration, how often does the rubric's trigger occur early enough to permit a human response? Estimate the yield from repeated agent runs, not from the author's expectation. Record which triggers occur, when they occur, how severe they are, whether the agent self-corrects, and whether the remaining budget leaves the human a consequential choice. The practical result is a funnel: of all working artifacts mutated, how many pass the oracle, produce a recurring trigger, resist generic retry, admit a useful intervention, and survive a human pilot? The cost per surviving item and its decay rate after model updates determine whether task generation is realistic.

Public traces suggest that elicitation opportunities themselves are not rare. [SWE-chat](https://arxiv.org/abs/2604.20779) contains roughly 6,000 opt-in sessions, 63,000 user prompts, and 355,000 tool calls linked to git history and human-versus-agent code attribution. Its authors classify users as pushing back through corrections, failure reports, or interruptions in about two-fifths of turns. Only 44% of agent-produced code survives into user commits. These are candidate triggers, not validated examples of good judgment: pushback may be warranted or needless, and discarded code may be bad or merely unwanted. The dataset is also a selected sample of open-source developers willing to publish their sessions.

The harder bottleneck is reconstructability. [SWE-Together](https://arxiv.org/abs/2606.29957) began with 11,260 recorded user-agent sessions and converted 109 into sandboxed, verifiable interactive tasks: a 0.97% yield. A session had to retain a recoverable repository state, clear user intent, observable outcome, executable environment, and feedback whose triggering condition could be reconstructed. Its state-conditional replay is close to the mechanism proposed here, releasing a correction only when the corresponding trajectory condition arises. SWE-Together evaluates the agent using a simulated user, though, rather than evaluating the human.

[DevGPT](https://arxiv.org/abs/2309.03914) offers a much larger archive of developer conversations linked to commits, issues, and pull requests, but its chat transcripts generally lack the complete tool and environment state needed for replay. Autonomous traces such as [SWE-agent trajectories](https://github.com/SWE-agent/SWE-agent/blob/main/docs/usage/trajectories.md) are worth mining for recurrent agent failures, but contain no human response to score.

This evidence shifts the initial question. There is ample raw material for discovering natural triggers, but the uncertain step is whether a task factory can raise the conversion rate from interesting trace to sealed situation enough to maintain an assessment. A credible prototype should mine existing traces first, publish rejection reasons at every stage, and compare trace-derived tasks with deliberately mutated working artifacts.

No single target yield is universally correct. Rare triggers waste an hour; nearly certain and conspicuous triggers may become transparent gotchas. A sequence can combine naturally elicited events with calibrated fixed artifacts, but the two should be labeled because they trade ecological validity for exposure control.

### Grading discrimination

The second is a *grading-discrimination* question. A rubric should separate responses that produce different warranted consequences while treating different methods with the same consequence alike. Before using it on candidates, test it with a blinded contrast set:

- the same successful artifact produced with and without a necessary human rescue;
- the same intervention language followed by a valid receipt or by ceremony;
- acceptance of correct and defective agent output;
- rejection of correct and defective agent output;
- early redirection of a bad trajectory and needless redirection of a good one;
- an anticipated method and a novel method that establish the same claim.

Evaluators should score these traces without knowing which contrast they received. A usable rubric has high agreement on whether the trigger occurred and whether the receipt is valid, low false credit on ceremonial behavior, low false rejection of alternative valid methods, and additional information beyond the final pass/fail result. If it merely recovers task success, the shim added surveillance rather than measurement. If it rewards the author's preferred wording, it grades style.

This gives the project a first experiment. Generate a batch of candidate situations and publish the survival funnel. Then construct blinded response contrasts and publish the rubric's confusion matrix and evaluator agreement. Only if both gates clear is it worth administering the hour-long sequence to candidates.

## The task band

For a fixed model, scaffold, tool set, time limit, and retry budget, a candidate task belongs in the set only when it clears three empirical gates: the human alone rarely solves it, the agent alone rarely solves it, and the pair solves it more often than the better component does. The first two establish the component floors. The third establishes lift over the better component, the usual definition of complementarity. None should be believed from the task author's intuition. Human-only baselines are expensive, so an early pilot may estimate them on a representative sample of items rather than every item, but it cannot silently omit them and retain the complementarity claim.

"Cannot one-shot" needs an operational definition: one named model and scaffold, fresh context, fixed tools, no human messages after dispatch, and a fixed time or token budget. Run it several times, because agent success is stochastic and one cached failure does not establish a floor.

Do not demand literal zero percent success. [Selection by model failure](/how-to-audit-a-benchmark#3-ask-how-the-tasks-were-selected) enriches for broken tasks, mis-keyed graders, and underspecified requirements because each presents as "the model failed." A useful task produces a stable and intelligible failure state, not merely a loss.

The ceiling needs a pilot. At least one human-agent pair must solve the task under the intended conditions, and ideally the intervention that changes the outcome can be named and replayed. Otherwise the task may be difficult because it requires a capability neither component supplies.

Any receipt mechanism needs its own calibration: a proposed check should usually catch the seeded defect and rarely reject the gold. If a regression test passes both the seeded defect and the gold, it is ceremony. A test tailored to exactly one seed may be little better. Calibrate it against the gold and a small family of plausible mutants, following the logic of [mutation testing](https://doi.org/10.1109/TSE.2010.62). If a review procedure rejects correct work as often as defective work, it measures suspicion. Calibrate receipts against positive and negative artifacts before interpreting a candidate's choice to invoke them.

## Generation from working artifacts

Start with a small executable system in a known-good state. Introduce a controlled defect. The original state or real patch anchors the answer, and tests anchor the outcome. This is safer than writing a clever puzzle and inventing its oracle afterward.

The mutation should create competing plausible directions while leaving discriminating evidence available. Useful shapes include:

- two reasonable components violating an interface assumption;
- a local patch that passes visible checks but breaks a distant invariant;
- a prominent symptom that is sometimes causal and sometimes downstream noise;
- two hypotheses separated by one cheap experiment;
- a familiar repair that fails because one boundary condition has changed;
- an almost-correct agent solution resting on one unsupported assumption.

Current failure modes should be treated as expiring instances, not permanent constructs. Frontier agents still commonly introduce a new helper instead of locating and reusing the repository's existing abstraction. That can expose whether a human inspects the surrounding code, constrains unnecessary surface area, and redirects the patch toward local convention. But better repository search and longer context may erase this failure soon.

The reusable archetype is broader: the agent produces a locally adequate change that violates a recoverable repository-level invariant. Duplicate helpers are one present realization; an obsolete configuration path, parallel validation rule, bypassed abstraction, or inconsistent error policy may replace it later. Preserve the trigger-action-receipt structure while refreshing the concrete failure against current agents. Once the standardized agent reliably discovers the existing invariant without help, the item no longer demonstrates complementarity and must retire.

Difficulty should come from allocating attention and verifying beliefs, not from recovering a secret fact. The candidate must have enough evidence to make the better decision, but not enough budget to investigate everything.

The agent can help locate the task boundary. Run it repeatedly and preserve its first diagnoses, proposed experiments, confident false claims, patches, and convergence points. These traces show where the current policy fails. A candidate item is promising when failures cluster around a consequential decision that a small evidence-grounded human intervention can change.

Replay that intervention across fresh runs. If it does not improve verified outcomes, the apparent human contribution may have been luck. If any generic instruction such as "try again" works equally well, the item measures extra inference budget rather than judgment.

### Public review boundaries

A lower-cost construction path begins with public pull-request history rather than a new mutation. Restore the parent commit, supply the issue or specification and a historical PR, and ask the candidate to review it with an agent. The public record may provide the submitted patch, maintainer comments, CI, later revisions, and the eventual merged state. An intermediate revision followed by a substantive maintainer correction is especially valuable: it supplies a naturally defective review artifact and a public account of what changed next.

This directly tests the thin but consequential role described in [(Issue) → PR](/issue-to-pr): as generation and deterministic filtering expand, specification, selection, and reviewer attention remain at the boundary. The assessment asks whether the candidate can operate that boundary, not whether they can recreate the implementation unaided.

Domain matching makes the observation more defensible. Let candidates declare areas in which they claim competence (frontend accessibility, authorization, databases, distributed systems, mobile, build tooling) and sample review tasks from those domains. The work then resembles the role being claimed instead of using one generic puzzle as a proxy for all engineering.

Domain knowledge is not institutional knowledge. A maintainer knows which invariants are unwritten, which compatibility promises matter, which apparent oddities are deliberate, and which trade-offs the project has already accepted. A visiting candidate does not. Reproducing the maintainer's verdict can therefore punish missing local context rather than reveal poor judgment.

Only concerns recoverable from the supplied repository, issue, documentation, tests, and task briefing may enter the preregistered score. If the historical review depended on private discussion or tacit convention, either encode that context in the packet or discard the item. The task should also permit clarification. When the evidence underdetermines the decision, identifying the missing premise and withholding approval can be the correct response; confidently guessing the maintainer's preference should not be.

Giving everyone the same packet is necessary but not sufficient for fairness. The interface, source format, language load, timing, assistive-technology support, device stability, and prior familiarity can all block access to the construct. Publish an unscored practice task with the same mechanics, pin the agent and packet within a comparison cohort, support construct-preserving accommodations, and record access failures separately from candidate performance. [SIOP's guidance for AI-based selection](https://www.siop.org/Portals/84/SIOP%20Docs/Considerations%20and%20Recommendations%20for%20the%20Validation%20and%20Use%20of%20AI-Based%20Assessments%20for%20Employee%20Selection%20January%202023.pdf) distinguishes equal treatment during administration from comparable opportunity to demonstrate what the procedure claims to measure. A realistic task may feel fair and still measure terminal familiarity or reading speed.

This limits what public goldens buy. They reduce the cost of finding realistic review boundaries, but they do not transfer the maintainer's epistemic position to the candidate. The item author must still construct a self-contained evidence boundary and verify that independent reviewers who lack project history can reach the warranted decision.

A merged PR is an anchor, not an oracle. Maintainers can merge weak tests, incidental changes, or mistakes, and their decision may depend on context absent from the repository. The lighter validation contract still has to:

- restore the build;
- establish the intended behavior from public evidence;
- run the eventual patch;
- reject at least one plausible defective alternative;
- scrub later history that reveals the answer;
- preserve genuine ambiguity rather than forcing one verdict.

Historical agreement is not the whole grade. Matching a maintainer's concern is evidence; producing an independent receipt is stronger. A candidate may find a valid issue the original review missed, which belongs in the discovery ledger and should be tested against the code. Clean historical PRs are necessary negative controls so indiscriminate rejection cannot masquerade as expertise.

This is one task family, not the whole construct. PR review measures appropriate reliance, verification, prioritization, and the merge decision more directly than it measures live redirection. It may nevertheless be the practical first product: fixed artifacts, public goldens, domain-specific work, and executable review consequences, followed later by a smaller live-agent component.

## The held-out rubric

The candidate can know the public construct: use the agent to deliver a correct, appropriately verified change under a limited budget. The item-specific conditions remain held out. The rubric stays short:

<div class="table-wrap">
<table>
<thead><tr><th>dimension</th><th>hidden condition</th><th>boolean verdict</th></tr></thead>
<tr><td>appropriate reliance</td><td>agent output is correct or seeded-defective</td><td>accepts the correct output; rejects the defective output</td></tr>
<tr><td>timely redirection</td><td>agent enters a verified bad trajectory</td><td>redirects before a calibrated time, token, or action threshold</td></tr>
<tr><td>verification before acceptance</td><td>correctness is not established independently</td><td>produces a receipt that discriminates the submitted result from a near miss</td></tr>
<tr><td>boundary specification</td><td>the brief permits a literal but poorly situated unit, while supplied evidence supports a more useful external contract</td><td>produces a UI, API, or CLI that passes held-out consumer scenarios without exposing unnecessary implementation structure</td></tr>
</table>
</div>

The rubric grades artifacts and consequences, not resemblance to the evaluator's process. A candidate may write a test, ask the agent to write it, invoke an adversarial reviewer, inspect a diff, run CI, consult a source, or evoke verification through a route nobody anticipated.

Boundary specification is not a request to guess the evaluator's preferred design. The item supplies recoverable evidence about the consumer, conditions of use, or neighboring systems, then holds out a behavioral envelope that exercises the resulting boundary. Several interface designs may pass. A golden is one feasible witness that the envelope can be satisfied, not the unique answer. A matched control states an adequate boundary explicitly; elaborating or replacing it should add no credit and may waste the budget.

### The discovery ledger

The rubric must also be able to learn from the candidate. A strong candidate may introduce a practice the evaluator did not know: a cheaper discriminator, a stronger invariant, a safer delegation boundary, or a verification method that catches a defect the held-out checks miss. Treating that as off-rubric behavior would recreate the interviewer's repertoire as the ceiling of the eval.

Keep two ledgers. The *score ledger* contains only preregistered conditions, so an evaluator cannot award taste points after seeing who produced the work. The *discovery ledger* records any unanticipated intervention with its trigger, action, cost, and outcome receipt. This preserves the distinction between confirmatory and exploratory evidence ([Nosek et al.](https://pubmed.ncbi.nlm.nih.gov/29531091/)).

A novel method does not receive improvised credit merely because it looks clever, and it is not discarded merely because the rubric omitted it. Replay it against the defective artifact, the gold, and matched negative controls. If it discriminates reliably and adds information beyond the existing rubric, add it to the next version for everyone.

That makes the candidate a possible source of benchmark improvement. The current instrument measures them under a fixed contract; their successful deviations can improve the next contract. Version the rubric, publish the new receipt and rationale, and never silently rescore earlier candidates under a rule they could not have known existed.

### In-frame elicitation

Do not administer the rubric as a questionnaire. Asking "what would you do if an agent changed the tests?" measures declarative knowledge under an announced frame. The candidate has been told both that something is wrong and which class of response the evaluator values. That is the hiring equivalent of publishing the hidden test in the prompt.

The trigger has to occur *in-frame*. The candidate is working toward an ordinary outcome when the agent actually edits a test, asserts an unsupported requirement, loops on a failed approach, or presents a correct result. The evaluator watches whether they notice and whether the composed system produces the receipt. Knowing that regression tests are good and causing one to exist at the moment it is needed are different capabilities.

This also rules out a menu of interventions. Presenting "write a test / inspect the diff / ask for clarification" turns attention into multiple-choice recognition. Give the candidate the same open agent interface they would use on the job, record the interaction, and score the final artifacts against the held-out conditions. The behavior must be available, consequential, and unannounced.

## Families and ordering

An unordered bank measures average performance. A sequence needs families with controlled recurrence.

Suppose the rubric covers the four dimensions above. An eight-task family might be ordered like this:

1. A plausible patch contains a seeded boundary defect and lacks independent verification.
2. The agent's patch and existing verification are sufficient; rejecting it is inappropriate disuse, in the sense of underusing reliable automation ([Parasuraman and Riley](https://doi.org/10.1518/001872097778543886)).
3. The agent commits to a wrong diagnosis and begins spending the budget on it.
4. The agent begins in the right direction after the previous task; reflexive redirection is harmful.
5. A locally correct fix contains an off-task change under a plausible cover story.
6. A held-out task combines uncertain correctness with a costly bad trajectory.
7. A brief permits a literal interface that fails recoverable consumer uses; the candidate can derive a better boundary from the supplied evidence.
8. A brief already states a sufficient boundary; speculative reframing consumes attention or breaks a held-out use.

The candidate should not be told which rubric conditions each task activates. Each task yields an outcome receipt before the next begins. A non-intervention is not sufficient evidence on its own: on the negative control, the candidate must still produce a cheap receipt showing that they checked before stopping. Score selectivity across the positive-negative pair, not isolated compliance on either item.

Do not infer consolidation from an upward score trend.

Held out should mean the live item key, not the construct. Publish the mechanics, the dimensions, and unscored examples with nonexamples; hide which live trigger is present, the seeded condition, and the oracle. Otherwise the assessment partly measures whether a candidate can infer the interviewer's private taxonomy. Transparency research in assessment centers and structured interviews finds that recognizing or disclosing rated dimensions can raise performance ([Kleinmann](https://doi.org/10.1037/0021-9010.78.6.988); [Klehe et al.](https://doi.org/10.1080/08959280801917636)), while later work warns of a possible tradeoff with criterion validity ([Ingold et al.](https://doi.org/10.1111/peps.12105)).

Run the experiment: give a standardized tutorial between parallel forms and measure receipts, inversion errors, rank stability, and held-out transfer. If almost everyone learns the behavior, that is not cheating. It is evidence that the material belongs in onboarding, certification, or the harness rather than competitive selection. Hiding the lesson to preserve variance would mistake scarcity for validity.

The order is part of the instrument. Unconstrained randomization destroys the staged narrative, while one fixed order confounds task difficulty with learning. A pilot therefore needs counterbalanced orderings that preserve prerequisite relations, or matched families with swapped surface forms. The goal is not a psychometrically mature score on day one. It is to establish that the apparent trajectory is not just an easy final task.

## The generation contract

This contract consolidates the preceding requirements into a preregistrable checklist. Every item should pass it before a candidate sees it:

1. **Claim:** the difficulty lies in complementable judgment, not trivia, typing, or raw context length.
2. **Spec:** every graded requirement is explicit in the provided materials or recoverable from supplied use evidence; no score depends on the evaluator's private preference.
3. **Oracle:** materially wrong solutions fail, including the agent's common near misses.
4. **Frame:** destructive or off-task completions fail.
5. **Gold:** at least one reference solution passes its own verifier; alternatives satisfying the same behavioral envelope are accepted.
6. **Agent floor:** repeated standardized agent runs do not solve it reliably.
7. **Human ceiling:** a pilot human-agent pair can solve it inside the budget.
8. **Condition:** whether the scored trigger occurred, and the truth of the relevant agent output or trajectory, is knowable to the evaluator after the run.
9. **Boolean receipt:** acceptance, redirection, and verification verdicts are executable or otherwise falsifiable from the artifacts.
10. **Intervention:** redirection or verification improves fresh runs in the positive condition.
11. **Negative control:** a matched task makes rejection, redirection, or further verification unnecessary or harmful.
12. **Transfer:** a later relative tests the same dimension under a new surface form.
13. **Discovery:** unanticipated successful interventions are captured with receipts but do not alter the preregistered score.
14. **Profile:** capability, automation, and alignment remain separate; no hidden weighting collapses them into rank.
15. **Decay:** solo-agent, trajectory, and receipt baselines are rerun whenever the model or scaffold changes.
16. **Trace:** the shim captures enough interaction evidence to reconstruct each scored accept, reject, redirect, and verification event.
17. **Isolation:** the agent and candidate cannot inspect or modify the hidden verifier, future tasks, or evaluator-only rubric.
18. **Provenance:** repository history, upstream references, filenames, and metadata do not disclose the controlled mutation.
19. **Exposure:** parallel forms and a retirement policy bound the damage from item leakage.
20. **Opportunity:** scores are conditioned on observed triggers and reported with their frequency and severity; absence of an opportunity is not a success or failure.
21. **Yield:** repeated runs establish that a scorable trigger occurs often and early enough for practical administration.
22. **Discrimination:** blinded contrast traces establish that the rubric credits warranted consequences, rejects ceremony, and accepts unanticipated valid methods.

The construction pipeline follows:

<img src="/assets/complementarity-pipeline-light.svg" alt="The task construction pipeline: working artifact, controlled mutation, gold and hidden verifier, repeated solo-agent runs, identify a stable trajectory, calibrate the redirection threshold, boolean verdict and intervention replay, human-agent pilot, control variants, ordered sequence" />

## The report

Report the receipts:

- the task-generation survival funnel, authoring cost per surviving item, and decay after agent updates;
- the rubric confusion matrix and evaluator agreement on blinded response contrasts;
- success and time-to-verified-checkpoint for every task;
- the separate capability, automation, and alignment profile, with no composite rank;
- repeated solo-agent outcomes under the identical budget;
- matched human-only outcomes where practical;
- active human time, interventions, and decisions consumed per verified rung;
- acceptance and rejection outcomes against the known correctness of agent output;
- the number, type, and severity of rubric triggers the live agent actually produced;
- redirection time and cost against the calibrated threshold;
- verification verdicts and their receipts;
- boundary-specification verdicts against held-out consumer scenarios;
- the candidate's intervention trace;
- the shim version, agent configuration, and any gaps in transcript capture;
- novel interventions in a separate discovery ledger, including replay results;
- false rejection and needless redirection on negative-control tasks;
- transfer of the same dimension to related tasks;
- exploratory improvement after informative outcomes;
- uncertainty from agent stochasticity and the tiny human sample.

At six tasks the instrument detects failure modes; it does not rank the candidates who avoid them. Each dimension yields only one or two binary observations. Treat per-candidate verdicts as screening evidence, and treat any finer ordering as noise until the family is longer and its reliability is measured. Accepting everything and rejecting everything are different response biases, not different levels of discernment.

The primary result is a profile: capability, automation, and alignment. The sequential quantity is selectivity across positive and negative controls; change after informative outcomes is secondary. All are local to the instrument. None licenses "good engineer" without the employer later validating the score against the job.

That boundary is a feature. In the United States, the [Uniform Guidelines on Employee Selection Procedures](https://www.eeoc.gov/laws/guidance/questions-and-answers-clarify-and-provide-common-interpretation-uniform-guidelines) define validation as demonstrating job relatedness and require evidence, not assertion, when a procedure with adverse impact is defended. Candidates should also consent to the public construct, including that some conditions may be deliberately seeded. A complementarity test should make a narrow claim from receipts anyone can rerun:

> Under a fixed agent, scaffold, and budget, this pair reached these verified outcomes, consumed this much human attention, preserved these constraints, accepted correct output, rejected defective output, and redirected a verified bad trajectory before the threshold.

That is not a career. It is finally a measurement.
