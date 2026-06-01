---
variant: post-medium
title: "Sour Red Tapes"
tags: methodology, epistemology
---

> *Nullius in verba.*

I submitted a run to the SWE-bench Verified leaderboard last week. 426 of 500 instances, graded by the official harness, every losing run committed, the score regenerating from the logs with one command. It fails exactly one check. I have no academic affiliation.

The policy, dated November 18, 2025, reads:

> Going forward, we will only accept submissions that meet *all* following requirements:
>
> * Open Research Publication: Submissions must include a link to an arXiv preprint or technical report.
> * Academic/Research Institution Affiliation: At least one author must be affiliated with an academic institution or established research lab (e.g., universities, Google DeepMind, Meta FAIR, Microsoft Research, frontier labs)
>
> So for example, here are prior submissions that...
> * Would still be eligible: OpenHands, SWE-RL, FrogBoss, AutoCodeRover
> * Are no longer eligible: Augment Code, Solver AI, Honeycomb.sh
>
> Rationale: This policy ensures that SWE-bench Verified and Multilingual remains focused on its core mission [...] We want to maintain the benchmark as a venue for advancing the scientific understanding of code generation rather than as a product validation platform.

Source: the [SWE-bench leaderboard submission repo](https://github.com/swe-bench/experiments), README, November 18, 2025.

The reason it gives is the right target: it wants rigor, transparency, reproducibility, a venue for science rather than a product showcase. I take that target seriously. Then I show the gate misses it.

I have argued this twice in the abstract. [Science on Trial](/science-on-trial) separated the things this policy conflates: publication is not peer review is not replication is not truth, and the trail is the only verdict. [Papiermark Credentials](/papiermark-credentials) traced how the credential decoupled from the merit it once tracked, and why AI restores the merit economy first in fields where a verifier can check receipts, software engineering at the front of the line. Both were diagnoses at a distance. This time it is not abstract. I brought the receipts to exactly that field, and I am the one standing at the gate.

## A proxy that decoupled

Affiliation is a proxy for rigor. Most proxies are fine: you reach for a cheap correlate when the real quantity is expensive to measure. This one has come apart from the thing it stands in for, and the policy's own examples prove it.

Hold the allow-list next to the mission. The stated worry is the benchmark becoming a product validation platform. Yet the eligible affiliations name Google DeepMind, Meta FAIR, Microsoft Research, and frontier labs: research labs inside the largest product companies in the field, the ones with the most commercial stake in a benchmark headline. The ineligible names are three smaller coding-agent startups. If the goal were to keep marketing off the board, this allow-list does the opposite. It admits the biggest marketing incentives by name and turns away the small.

So the line the policy actually draws is not research against product. It is incumbent against challenger. Affiliation tracks resources and standing, not commercial incentive, because it waves through exactly the entities with the most reason to optimize for the number.

I am the case that exposes it cleanly. I sell nothing; a blog post and an append-only repo are the whole of it. I am [long contribution and short credential](/papiermark-credentials), so by the board's own stated worry I sit closer to the target than many cases it admits. The gate excludes me and admits the product labs. That is not a rule aimed at product motives. It is a rule aimed at the unaffiliated, wearing the language of one aimed at product motives.

Worse, the policy's own preamble calls the board "a resource for advancing open, reproducible research." So measure me on that. The entire method is public under a copyleft license: the recon, craft, and audit skills in full, every trajectory, every log, every losing run, and a score that any reader regenerates from those logs with one command. I am giving the secret sauce away. Anyone, including the labs the gate admits, can take it and submit.

Now look at what the board actually contains. Nearly half of it, 64 of 135 entries on the board as I write this, ships a closed system: no public scaffold, and you are asked to trust the number on faith. The policy does nothing about this, because it requires open *publication*, a paper, not an open *system*. Under the written requirements, a closed lab with an arXiv link clears the bar untouched. So the gate demands a credential I lack and a paper a closed system can satisfy, while ignoring the one axis I actually maximize. One of the most open and reproducible submissions on the board is being turned away, and it is turned away at the affiliation line, the one line that has nothing to do with openness at all.

So affiliation is not a weak proxy here. It is a false one. A weak proxy points the right way through noise. A false proxy has stopped pointing. Among those it screens out are people who cannot afford to game and have no incentive but the method itself, the exact submitters the stated mission claims to want.

This is [Goodhart](https://en.wikipedia.org/wiki/Goodhart%27s_law) one floor up. Rigor was the target. Affiliation became the measure. Once it is the measure, it measures access.

## If it were about science, it would require a procedure

For a benchmark result, rerunnability is the load-bearing wall. A score nobody can regenerate is an anecdote. So if the board were really about science, the requirement would be obvious: ship a procedure a stranger can run and get your number. The policy requires no such thing, and it says so.

In the policy's own words, the trajectory requirement exists "to provide the community with more insight into how cutting edge methods work without requiring a code release." Read that against the science framing. They ask for a story about the method, explicitly in place of the runnable method. A story is not a procedure. You cannot rerun a story. This is the conflation [Science on Trial](/science-on-trial) is about, arriving as a submission rule: publication standing in for replication.

It gets sharper. The same README admits: "we have also found that the top-performing submissions to SWE-bench typically have not open sourced their code nor been verified." The maintainers know their leaderboard is topped by closed, unverified entries, and they kept accepting them. Verification, the closest thing the leaderboard has to an independent rerun, is optional, not a requirement you must clear.

Now set the two documents side by side. The announcement banner says the board accepts teams "with open source methods and peer-reviewed publications." The requirements below it ask only for affiliation and an arXiv link, and the body explicitly waives code release. The policy cannot agree with itself on whether open methods are required. I resolve the contradiction in the direction it claims to want: open method, runnable procedure, verified score. The gate still stops me, because the line it enforces is the affiliation line, and that line was never about reproducibility.

The apparatus already exists, and the field already uses it. ACM and USENIX award a [Results Reproduced](https://www.acm.org/publications/policies/artifact-review-and-badging-current) badge when an independent committee runs your artifact and recovers the paper's main results: one question, can we rerun this and get your number, and never a question about where you work. Benchmark platforms like [Codabench](https://www.codabench.org/) go further and execute your submitted code server-side, scoring what they ran instead of what you reported. SWE-bench has the harness to do exactly this. Its own grader is what produced my 426.

The objection writes itself: who pays to rerun everyone? Follow the money across three tiers. Generating a run is the costly tier, dominated by model inference, on the order of hundreds to low thousands of dollars for the full five hundred. The submitter pays it. I burned the compute and the model quota, not the maintainers. Re-grading from the committed logs is the next tier and it is effectively free: the grader reruns nothing, it re-reads the test output I shipped and recomputes pass or fail in CPU-seconds. That tier trusts my logs, so it is not yet independent. The independent tier is re-running the official harness from scratch to confirm the patch truly passes, and it is the only one that costs the maintainer real work. It is still cheap. A random-subset spot check of twenty to fifty instances runs in roughly single-digit dollars of inference and a few worker-hours, the same per-instance cost the submitter already paid. None of the three is expensive enough to justify a credential check. A gate cannot plead poverty when the dearest honest verification it could run costs less than lunch.

A program that wanted science would require the procedure and make affiliation irrelevant. This one requires the affiliation and makes the procedure optional. That inversion is the whole tell.

## The thing the gate is actually afraid of

Strip the policy down and the fear underneath it is specific. It is not "an unaffiliated person submitted." It is *a priori knowledge of the instances*: a scaffold that already knows the answers. Hardcoded instance ids. Heuristics keyed to one repo's bug. A patch shaped like the gold patch that arrives in the trajectory without ever being derived from the failing test. A branch that only makes sense if you read the fix first.

Most of those leave a tell in text, and the cleverest leakage is at least auditable from the artifact in a way affiliation never is. Every submission already ships the text the policy requires: the predictions, the per-instance logs, the full trajectories. The dishonesty the gate is reaching for is sitting in the artifact, legible, waiting for someone to read it.

| What the gate fears | What it measures for it | What it could measure |
|---|---|---|
| Smuggled instance priors | Author's affiliation | The trajectory: is the fix derived or pre-loaded? |
| Irreproducible score | A citable paper | `get_results` regenerating the score from the logs |
| Spam volume | Institutional letterhead | An automated pass the repo already runs |

## They already ship the detector

Here is the part that turns this from a complaint into an indictment. The leaderboard repo already audits submissions with code. `analysis/detect_similarity.py`. `analysis/run_sim_detection.py`. `analysis/git_peek_suspicious_commits.py`. These run automated detectors over the same logs and trajectories, today, to catch cross-submission copying and suspicious commits.

They have the inputs, the tooling, and the precedent. They point that tooling at plagiarism between submissions, then fall back to affiliation for the rigor question. But "did this trajectory derive its fix, or did it already know?" is the same class of script they already maintain. An `analysis/detect_instance_priors.py` is a sibling of the three files in that directory, not a research program.

What would it check? Read each trajectory and ask a model the question a skeptical reviewer would ask:

- Does a fix appear before any evidence that would motivate it? A patch that lands without a localizing step is a fix that was known, not found.
- Does the trajectory reference instance ids, repo-specific magic constants, or test names the agent should have had to discover?
- Does the reasoning cite behavior the agent never observed in the container?
- When the same scaffold meets a held-out instance with no public solution, does its trajectory look the same, or does it suddenly lose its footing?

None of this is perfect. An auditor has false positives and an adversary can write cleaner lies. So this flags a submission for review; it does not adjudicate acceptance on its own. But the bar is not perfection. The bar is "better than affiliation," and affiliation catches none of these, while a model reading the trajectory can flag failure modes affiliation cannot even observe.

## A cheap direct measure dominates the proxy

The usual defense of a proxy is triage: you cannot verify everyone, so you take the cheap signal and move on. That holds only while the direct measure is expensive, and it no longer is. Correctness regenerates from the logs in one command; the dishonesty the gate fears reads off the trajectory with a script the repo already runs. So the proxy is not triage anymore. It is a choice to weigh the letterhead over the evidence sitting beside it: the strongest form of false, not merely decoupled from the target but dominated by a direct measure the gatekeeper already owns.

## The field that abolished the gate

The deeper irony is specific to where this is happening. Machine learning is the field that tore the affiliation gate down. It put its papers on arXiv instead of behind journal review. It shipped weights and code instead of asking you to trust a lab's word. It let outsiders reproduce a result on a weekend and post the number. And its sharpest instrument for all of this was the leaderboard, an object built for one purpose: to replace "trust the institution" with "show the score."

A benchmark is the most meritocratic thing the field makes. It does not care who you are. It runs your patch and reports whether the tests pass. That is the whole point.

So watch what the affiliation requirement does. It takes the one artifact designed to be blind to pedigree and bolts pedigree back on. It regresses the leaderboard into the credentialism the leaderboard was invented to abolish. Of all the places to reinstate the gate, this is the field that should know best why the gate came down, and this is the object that least needs it.

## An older name for the gate

There is an older name for this, older than machine learning. When the privilege of knowing is conferred by social standing rather than by the thing known, when a claim is inadmissible until its author has been ordained, we call that a priesthood. Science was founded as the refusal of exactly that. The Royal Society took as its motto [*nullius in verba*](https://en.wikipedia.org/wiki/Nullius_in_verba), on the word of no one: bring the demonstration, not your station, and let anyone present witness it.

A reproducible result is the most anti-clerical object we have ever built. It lets a nobody overturn an authority by rerunning the experiment, and it does not check the nobody's robes first. The affiliation gate reverses the founding move. It rules the claim inadmissible until its author is ordained, and it rules so on the one instrument whose entire purpose was to let the unordained be right.

## The artifact does not ask for trust

I built my run so it would not need a credential. The patches do not ask you to believe they pass; the official grader says so, and you can rerun it. The method changes do not ask you to believe they generalize; they are legible diffs you can judge one by one. The losses do not hide; they are committed next to the wins. Calibration is the disclosure. The whole thing is built to make a reviewer's job cheap, which is exactly what a leaderboard that cares about rigor should want.

Call this sour grapes if you want: a guy who got turned away, now telling you the rule is unfair. But check whether the argument needs me. Delete my submission from the story and every receipt still stands. The allow-list still names the largest product labs while the mission says product is the enemy. The board is still nearly half closed systems. The README still admits its top entries are unverified, still waives code release, still contradicts its own banner on open methods. The detectors still sit unused in `analysis/`. None of that is about my feelings. It was true before I clicked submit, and it stays true whether they answer or not.

What is left, once the science language is stripped off, is red tape. A credential check, stapled onto the one instrument in this field whose entire value was that it never needed one. Red tape always arrives wearing the costume of standards. This time the costume is the word rigor, and the body underneath it is a letterhead.

So I expected a rejection on affiliation, and I said as much in the pull request. I named the credential I lack, offered to run the official grader on any random subset they chose, and said I would close it myself if the rule was firm. That was a week ago. The pull request is still open, the ping unanswered, the direct message unanswered. Not a rejection. A rejection is an answer. This is silence.

The silence is the truer artifact. The charge was that the gate reaches for letterhead instead of reading the evidence beside it. Handed a one-command verification for free, it did not even reach. It declined to read the evidence at all.

There is a last turn I did not expect to write. While I argued over whether this board would read my run, the field that built the board had already left it. In February 2026, three months before I submitted, OpenAI [announced it would stop reporting](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) SWE-bench Verified. Its own audit found that most of the failing tests it checked were flawed, and that every frontier model had been contaminated on the solutions. It pointed everyone to SWE-bench Pro instead. The leaderboard still updates; the field has walked off it. So the affiliation gate, bolted on last November, now guards a board the benchmark's most prominent reporter abandoned by winter. The red tape outlived the thing it was taping shut.

That should bother anyone who cares how science gates itself. The credential was never load-bearing for rigor. The contamination that actually killed the bench is exactly the failure affiliation cannot see and a trajectory audit can: the gate kept the signal that catches nothing and waved through the one that brought the board down. *Nullius in verba*: bring the demonstration, not your station. I brought the demonstration. The station never opened, and by the time I knocked, no one was minding the door.
