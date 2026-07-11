---
variant: post-medium
title: "Hiring Is Evals"
tags: methodology, epistemology
---

Technical hiring is a mess of confusion. Resume screens grep for tech-stack nouns. Recruiters pattern-match on school and employer names. ATS filters run literal keyword search. Everyone knows these are proxies; the whole apparatus runs on hope that keyword density and credential prestige correlate with what anyone actually wants. The confusion runs deeper than disagreement about the answer. Nobody has stated the question. What is the measurement supposed to measure?

## Kinda sorta works

Ask around and you get the folk remedies: referrals, networks, vibe checks. All of them beat the keyword grep, and each works for a reason worth stating in measurement terms. A referral, at its best, is a prior evaluation on the real task distribution, transferred by trust: someone who watched the candidate do the actual job vouches for them. But "referral" is one label covering signals with radically different likelihood ratios, direct observation at one end and a former classmate at the other, recorded identically. A network is the same mechanism with weaker signal: adjacency to good work instead of observed work. A vibe check is an unstructured human-judge eval. High variance, uncalibrated, biased, and at least sampling behavior live instead of grepping artifacts.

The pattern: every folk remedy that works, works by getting closer to observing the candidate doing the job. None scale, none are fair, and nobody can say why they work, so they can't be improved, only ritually repeated.

## An excellent bar

Ask an org how it knows its hiring works and you get circular validation. We have excellent people because we have an excellent bar. How do we know the bar is excellent? Look at our excellent people. The process grades itself against its own output. False negatives are invisible by construction; false positives get absorbed as "not a culture fit." In evals terms, this is a benchmark whose only validation is its own leaderboard. No held-out ground truth, no way to be wrong.

And someone did check. Google studied tens of thousands of interviews, compared interviewer scores from the loop it was then running against job performance, and found [zero relationship](https://www.ere.net/articles/googles-weird-interview-questions-a-complete-waste-of-time) within its own hires, the only people it could study. Laszlo Bock, who ran People Operations, called the brainteasers "a complete waste of time." The one org famous enough to close the loop closed it, got zero, and the industry kept copying the loop anyway.

## Everyone knew

The evals world ran the same tautology in public, recently, and it ended differently. Everyone knew SWE-bench Verified, the standard benchmark for AI coding ability, was contaminated. It kept getting reported in model cards and launch posts because it was the number everyone else reported. It took until February 2026 for OpenAI to [deprecate it](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) as saturated and highly contaminated. A model reproduced the exact gold patch from a short problem snippet plus the task ID, and every frontier model tested showed task-specific contamination. The candidate had memorized the answer key, and the interviewers kept asking the questions for two more years, because those were the questions everyone asked.

The audit's second finding is the one hiring should study harder. Of 138 difficult tasks examined, at least 59.4% had material test or design problems: hidden checks that rejected correct solutions for not being the maintainer's preferred implementation. That is the other interview failure mode, a hidden rubric grading resemblance to the interviewer's answer, dressed up as outcome grading. Contamination inflates some candidates; underspecified grading rejects correct ones. Both were live in the same benchmark and the same interview loop.

*Nobody gets fired for hiring IBM, until someone does.* Running the standard loop is defensible rather than valid. Defensibility is a social property. It holds until the day it doesn't, with no warning, because the thing that would warn you is the measurement nobody is doing. And the market can't correct what it can't attribute: firms see slow hiring and regretted attrition, but nothing traces those aggregates back to the instrument, so the loop survives every bad outcome it causes.

## What a good bench has to have

One property above the others, then four in tension. The interview loop fails all five.

- *Validity*, the zeroth property: does the score support the inference you're making from it? An instrument can be repeatable, discriminating, cheat-proof, and cheap while consistently measuring the wrong thing. That is the LeetCode story in one sentence.
- *Determinacy.* Run the eval twice, get the same answer. [interviewing.io's data](https://interviewing.io/blog/technical-interview-performance-is-kind-of-arbitrary-heres-the-data) shows only about a quarter of engineers perform consistently from interview to interview, [holding at a thousand-plus interviews](https://interviewing.io/blog/after-a-lot-more-data-technical-interview-performance-really-is-kind-of-arbitrary). A designed eval reports an estimate and its variance; the interview loop reports a verdict. The variance splits, too: some is the judge, some is the candidate's day. Double-grading fixes the first; multiple items average out the second.
- *Discriminating power.* Scores must spread the population; a bench everyone aces measures nothing. LeetCode items discriminated in 2012 and are saturated now. The prep industry compressed the distribution until it separates the prepped from the unprepped, which was never the construct.
- *No cheating.* Contamination resistance. The question bank is public (Glassdoor, Blind, prep courses); the answer key is memorizable. See: SWE-bench Verified.
- *Efficiency.* Signal per dollar, per hour. Onsites burn five engineer-hours per candidate for a verdict with the reliability of a coin lean. Work trials get closer to the construct but cost more, a tradeoff evals people price deliberately and hiring prices by folklore.

The properties are in tension. The most discriminating instrument is rarely the cheapest; the most cheat-proof is rarely the most determinate. A designed eval chooses its tradeoffs on purpose. The interview loop never chose; it accreted.

## Same pathologies, better names

The thesis: hiring is a benchmark evaluation problem, and every pathology you find auditing an AI benchmark already exists in interviews. Benchmark people have names and fixes for them; software hiring runs as if nobody does. The crosswalk:

| Hiring | Agent evals |
|---|---|
| Candidate with tools of the job | System under test (model + scaffold) |
| Interview question | Benchmark task |
| Interview loop | Eval harness |
| Interviewer | Grader / judge |
| Leaked questions (Glassdoor, Blind) | Contamination |
| Interview prep industry | Training on the test set |
| Everyone aces LeetCode | Saturation |
| Referral | Prior eval on the real task distribution |
| Vibe check | Unstructured human-judge eval |
| Work trial | Held-out realistic task set |
| Job performance | Criterion measure (constructed) |
| Same verdict from different interviewers | Determinacy (inter-rater reliability) |
| Redesigning the loop on taste | Shipping an unvalidated bench |
| Retiring a stale question | Benchmark versioning |
| DP ladder (how far they climbed) | Graded checkpoints, partial credit |
| Time to verified completion | Outcome-gated latency |
| Offer/funnel metrics | Leaderboard reporting without audit |
| Rejected great candidates | False negatives nobody measures |

Two rows strain, kept on purpose. Job performance is a criterion you construct, never a label waiting to be collected. Every proxy is confounded by manager, team, and project, and the same person succeeds under one manager and fails under another, so the construct is really candidate-times-environment. And false negatives are darker in hiring than in benchmarking, because a bench can re-run a rejected output and hiring can't re-run a rejected career.

## Bock closed the loop

The obvious objection, and it's correct as far as it goes: a field already measured all this. Industrial-organizational psychology has spent a century here, on construct and criterion validity, inter-rater reliability, structured interviews, work samples, adverse impact. [Schmidt and Hunter](https://doi.org/10.1037/0033-2909.124.2.262) ranked selection methods by predictive validity decades ago, and work samples and structured interviews sat at the top then too. Evals didn't discover measurement.

What the objection misses: IO psych measured, published, and was ignored. Published validity coefficients don't make rigor *defensible*, because psychometricians aren't the employers anyone cargo-cults. "Implement whatever Bock recommends in the literature" has been the winning move for a decade, and almost nobody plays it. The edge was never secret. It was published, replicated at scale on Google's own data, and left on the table, because implementing it was expensive and cargo-culting the leaked loop was defensible. The antagonist here isn't a missing science. It's the implementation gap between what selection science established and what software companies do, and the agent era just made that gap newly expensive.

## The bar decays

Hiring managers are too timid to change a bar that used to work. And it likely did work: the loop that found great people in 2015 was measuring something, before the prep industry absorbed it. This is benchmark decay. SWE-bench Verified was a decent measurement in 2024 too; then the training data caught up, and validity expired while the number kept getting reported. Interview loops decay by the same mechanism, with the prep-course industry as the training-data pipeline. But benchmarks at least get versioned and retired. Nobody versions an interview loop. The timidity reads as prudence but is faithfulness to a measurement whose expiry date passed unnoticed, because nobody was checking.

And the ones who do change the bar have no idea that hiring should be a measurement device. They redesign on taste: whatever the founder hated about their last job's loop, whatever's fashionable this year. No whiteboards! Pair programming! Take-homes! No take-homes! Each redesign swaps one unvalidated instrument for another, and the debate runs entirely on vibes, because nobody has stated what the instrument is supposed to measure or how they'd know if it did. The field oscillates between a stale measurement and no measurement, and calls the oscillation progress.

## The system you hire

Here is the question the old bar can't survive: how do you evaluate a human who's allowed to use the tools available on the job? A SWE-bench score was never a model-only number. It was model-plus-scaffold, and labs report the harness with the score because the same model swings wildly across scaffolds. The deployed unit is human-plus-tools, so that's the unit you measure. An interview that confiscates the tools measures performance in an environment that never occurs on the job.

Interviews ban the tools out of contamination panic ("they'll just ask ChatGPT"), and the panic is correct for the old items. Regurgitating an algorithm discriminated when the artifact was expensive, and measures nothing now that it's free. But the evals response to a saturated item is to write harder items. The harder items are the complement skills: decomposing the task, directing the tool, and verifying (noticing when confident output is wrong). Signal moves from the artifact to the verification behavior. The instrument: seed the task so the assistant confidently produces something subtly wrong, and grade whether the candidate catches it. Uncontaminatable in the useful sense, because prepping for it is the job skill.

One objection survives the panic. The tool may conceal exactly the component capability whose failure becomes catastrophic when the tool is wrong; a candidate can supervise familiar work yet be unable to diagnose a novel failure. But the seeded-bug task *is* a perturbation where the tool is wrong, and it measures recovery, the very capability the objection worries about. What remains legitimate: if the role requires some irreducible solo competence, measure that separately and say why. What's not legitimate is confiscating all tools as a proxy for an unstated requirement.

## The band

![Ranges of task difficulty solvable by human alone, agent alone, and human plus agent; valid interview items live in the band only the composed system can pass, below an open ceiling nobody has reached](/assets/hiring-evals-band.svg)

If the talent you want drives coding agents, the construct is *incremental lift over the standardized agent baseline*: same model, same scaffold, same time and retry budget, with and without this human driving. From that, the item-design rule falls out. A valid item must defeat both components solo. The human can't finish it alone in the time, and the agent can't finish it without the human under the same budget ("cannot one-shot" is the cheap automated pre-screen). The baseline must be real: run the solo agent on each item several times before any candidate sees it, because runs are stochastic and a single cached failure can't separate the candidate's contribution from run variance. Repeated runs cost almost nothing, since no human sits in them. Lift is then read off the ladder: the rungs the pair reaches past the agent's recorded stall point.

Below the band, the item measures prompt-typing. Above the human-solo threshold but agent-solvable, it measures nothing about the human. The ceiling is open: configure an agent to beat [ARC-AGI-3](https://arcprize.org/arc-agi/3) to 100%, which nobody has done. As of March 2026, frontier LLMs score under 1% on the official board while humans solve 100%, and the one team that cleared the public environments used a bespoke multi-agent harness, exactly the configuration skill this item measures. The harness is banned from the official leaderboard, which is fine. The leaderboard measures models; this eval measures the human configuring.

A tempting shortcut to reject: grade the *how* instead. Watch the candidate work, score the process. But process-grading assumes the candidate's methods are a subset of the interviewer's. A grader can only credit methods they recognize. The judge's repertoire becomes the ceiling of the eval, and "is this person good" silently becomes "does this person resemble me." The candidates most worth hiring, the ones with methods the interviewer doesn't have, score worst. This is the standing evals argument for outcome grading: a held-out check is method-agnostic. Process observation belongs downstream of a passed outcome, as color on a hit, never as the reason for a miss. One carve-out: integrity violations fail you anywhere. Fabricating results, or being unable to explain your own solution, is not "a method the interviewer doesn't recognize."

## The ladder

Designing an item in the band, gradeable in a 45-minute slot, is hard, and the old loop solved a version of it. Whiteboard-era interviewers loved dynamic programming for a reason worth stealing: a DP question was one problem with a ladder of checkpoints (brute force → memoized → bottom-up → space-optimized), and how far the candidate climbed was the score. A scalar per item instead of a pass/fail bit. Maximum information per interview-minute. The ladder, not the DP, was the technology.

A fresh task in the band buys something else: Goodharting isn't possible for a candidate who's never seen it. The prep industry optimizes against known item banks; a novel item has no bank. But that kills only training-time Goodharting.

The other kind happens live. The candidate warps behavior toward whatever metric is visible in the room, and every candidate knows interviews are timed before ever seeing your task. Hence the trap in time-to-complete as signal: raw speed anti-selects verification. Under a clock, the winning move is accepting the agent's first confident output, the exact behavior the seeded-bug instrument catches. Novelty can't fix that; metric design has to. A candidate can perform checking without doing it, so the seeded trap has to bite. And the trap can't be a certainty: a candidate told every task hides a bug hunts bugs, which is easier than the job, where failures have low base rates. Mix clean and seeded outputs and grade calibration, flagging the real fault without crying wolf on sound code. Gate the clock on outcomes: time-to-*verified*-completion against held-out checks. Then speed measures fluency of the human-agent loop rather than credulity.

Combined, the agent-era item designs itself: a ladder of verifiable checkpoints (works → survives edge cases → survives the seeded trap → performant), time-to-each-rung recorded. Graded, bounded, outcome-gated, method-agnostic.

Most hiring pipes are content with a pass/fail grader, and a bar answers only one question: clear it? The pipeline needs discrimination at both ends. At the low end, a few minutes of conversational screening is answer-key gradeable, so a recruiter can administer it with no expert judgment. Recall is worthless as a bar now that the agent era made it free, but the screen's construct is cheaper than recall anyway: live, synchronous evidence that a human who can talk about code is present. It's proctored by being conversational, because an agent can't take a phone screen for you in real time without it showing. This is how eval suites stage too: cheap deterministic checks first, expensive agentic evals only for what survives.

At the high end, when three candidates pass for one req, the current loop breaks the tie with vibes. The ladder already produces the ordering: rungs climbed, time per rung, lift over the solo-agent baseline. And the open ceiling means the scale never tops out the way a saturated bench does. The current funnel has it backwards: engineer-hours at the bottom, coin flips at the top.

The band has a property no bar has ever had: it re-versions itself by construction. Every model release moves the floor; yesterday's un-one-shottable item gets one-shotted and retires automatically. The 2015 bar decayed silently because nothing forced a re-check. This bar can't go stale without announcing it, because the floor condition is machine-checkable. Run the LLM on the item and see. Price the cadence: re-versioning at model-release speed sounds brutal, but the check is automated and item-minting is cheap. The alternative isn't a stable bar. It's a bar that goes stale at the same speed and doesn't tell you.

Two bounds on the claim, stated plainly. The floor check automates one decay channel, model saturation; leakage, criterion drift, and adverse impact still need their own monitors. And the band can close: if solo-agent capability converges on composed capability, the band narrows toward nothing. That's the instrument's exit condition. The band's width is the live measure of whether agent-driving is still a scarce skill, and when it closes, the hiring question has changed. No previous bar ever announced its own obsolescence.

## The tooling ports

If the crosswalk holds, it's more than vocabulary: bench-design tools run on hiring. Different constraints, same goals.

- *Floor calibration.* Run the current frontier model against your item before any candidate sees it. One-shotted means below the band; retire it. Automatable, re-runs every model release.
- *Item pipeline.* Every candidate is a leak vector; after enough interviews the seeded-bug task is on Glassdoor. But the item bank is already sitting in the team's repos, uncontaminated and ever-fresh: take yesterday's real bug, revert the fix, hand over the repo. The merged PR is the answer key, the shipped tests are the hidden check, an oracle audited by production and immune to the interviewer's-preferred-implementation failure that broke SWE-bench's. The items sample the actual task distribution of the actual job, which is most of construct validity for free. One judgment the pipeline can't automate: the author has to price the item's domain-knowledge load. A real bug can be hard because the fix demands agent-driving, or hard because it demands three months of tribal context, and only the first belongs to the construct. The floor check can't tell them apart, since the solo agent lacks the context too. An item that's hard for the wrong reason measures tenure, and the author is the only one who knows which kind of hard they're handing over. The repo mints items faster than candidates can leak them. The good ones are assets: an item with proven discrimination stays banked until the contamination sweep finds it on Glassdoor, the floor check catches a new model one-shotting it, or a better item takes its slot. Retirement is by invalidation, never by calendar, and every retirement trigger in that sentence is automated except the last.
- *Reachable author.* The task author is a Slack message away: the engineer who shipped the real fix can calibrate the rubric, adjudicate a surprising-but-correct alternative, and field the appeal when the hidden check rejects something production would have accepted. A bench with a reachable author is a bench whose oracle can be contested, which is the property the whole SWE-bench audit was missing.
- *Contamination sweep.* Search for your own questions. Benches grep training corpora; you grep Glassdoor. Findable means it's measuring prep.
- *Inter-rater calibration.* Two interviewers, same recorded session, compare verdicts. Benches report judge agreement; loops could too, and the number would be embarrassing enough to force rubrics.
- *Item statistics.* Track which questions change decisions and which produce the same verdict for everyone. Kill the dead items. Benches do this arithmetic routinely; loops never do.
- *Held-out validation.* The criterion gets computed occasionally as research and never fed back into the instrument as invalidation. Close the loop: interview score against outcome at one year. Small n, noisy, slow, and still infinitely more than the current sample size of zero. The caveat: this validates only within hires, the selective-labels problem again, so it can't surface false negatives directly. Partial fixes are standard elsewhere. Advance an occasional borderline candidate as an audit sample, track rejects who join through other routes, and report false-negative rates as unidentified rather than pretending to estimate them.

The constraints are real: tiny n per item, no re-runs, and the samples are people, with the fairness and legal weight that carries. They change the engineering the way embedded systems change programming.

And the small-n objection deserves its own break, because it's where a hiring-ops skeptic pushes hardest: "your item statistics are meaningless at twenty candidates a year." Sort the imports by what they consume. Floor calibration and contamination sweeps consume zero candidates; they run against the model and the public internet. Inter-rater calibration spends grader hours and zero candidates. Only item statistics and held-out validation starve at small n, and starving there means reporting wide uncertainty or pooling across orgs, which is still categorically better than not collecting the variable. The constraints don't change the goals, and they don't excuse the current state. Constrained measurement would be respectable. The current state is no measurement.

One more objection: "evals-ifying humans treats people like models." The status quo is the dehumanizing one. The folk remedies that work, referrals and networks, exclude people without networks, and a noisy bar is cruelest to candidates who can't afford ten retries of a coin flip. A validated, determinate instrument is the equalizer; vibes are privilege-laundering.

## Run this loop

Hand the system over assembled, because the assembled version is what converts analogy into proposal. If you own a hiring loop, this is the recommendation:

1. State the construct. What does the score predict, and does it belong to the human, the tool, or the composed system? Incremental lift is one subtest, scoped to agent-driving IC work.
2. Mint items from your own repos: yesterday's real bug with the fix reverted, the merged PR as answer key, the shipped tests as the hidden check. Price each item's domain-knowledge load; hard-because-tribal measures tenure, and the task author is the one who can tell.
3. Floor-calibrate before any candidate and again on every model release: several solo-agent runs per item, same scaffold and budget the candidate will get, stall point recorded.
4. Screen cheap first: a few minutes of live conversation a recruiter can grade against an answer key.
5. Run candidates as human-plus-standard-agent under fixed budgets. Score time-to-verified-completion per rung, as lift past the agent's recorded stall point. Mix clean and seeded outputs, and grade calibration.
6. Double-grade recorded sessions and report judge agreement. Report every verdict as an estimate with variance.
7. Bank items that discriminate; retire on invalidation only (leaked, saturated, or outclassed). Kill items that never change a decision. Track adverse impact.
8. Validate scores against outcomes at one year, selective-labels caveat stated, with an occasional borderline advance as an audit sample.

Two objections remain. *"Strong hires reshape the job; you're benchmarking a task distribution that won't stay fixed."* True, and it bounds the claim. The instrument predicts performance on the job as constituted, and no interview instrument has ever predicted the reshaping. Concede the ceiling; the current loop doesn't clear the floor. *"An optimized hiring benchmark becomes a credentialing exam and recreates the prep industry one level up."* It does, and that's the design working, because the band collapsed the gap [Goodhart's law](https://en.wikipedia.org/wiki/Goodhart%27s_law) lives in. When the metric and the construct coincide, gaming the metric is acquiring the skill. The only way to prep for an item whose floor tracks the frontier model and whose checks demand verified outcomes is to get better at driving agents and verifying their output. A prep industry that trains the construct is called education.

## Who ships it first

Until Google, OpenAI, and Anthropic publish their hiring best practices for technical talent, the industry won't budge. But be clear about which force does what. The driving force is economic: verification keeps getting cheaper relative to trust, and change arrives wherever the curves cross. For a century, actually measuring a candidate cost more than trusting the proxies, so the proxies won. The agent era inverted the ledger on both sides at once. The bench side of verifying got cheap: floor calibration runs without a single candidate, item drafts are model-cheap, an answer-key screen needs no expert judge, re-versioning is automated. The trust signals collapsed: a resume, a portfolio, a take-home are now free to fake. What stayed expensive, the live session, the graders, the validation, was never the blocker. Orgs already pay five engineer-hours per candidate for noise. The crossover is that the same spend can now buy a calibrated instrument. That is what drives the change.

Prestige only sets the timing. Hiring adopts a new *defensible* default when someone everyone cargo-cults mints one. Only the frontier labs qualify: the field that professionalized evals, and the employers whose loops everyone already copies, leaked and secondhand via prep courses. Publishing would replace the leaked copy with the calibrated original.

Which answers the counterexample sitting in this post's own third section. Bock published the null *and* the positive, structured interviews and work samples, the same methods at the top of the validity rankings since Schmidt and Hunter, and the industry adopted neither. Prestige plus proof visibly wasn't enough. The decay section says why: before the agent era, any published loop was self-defeating. A static positive contaminates on contact, because publication feeds the prep industry and the instrument decays into a question bank.

What's newly possible is a loop that survives its own publication, a floor that re-checks on every model release, items that re-mint from the team's repos faster than they can leak. Bock's instrument couldn't survive being copied. This one is designed to be copied. The prediction is about who ships it first, and it's dated. If none of the three has published by the end of 2027, I was wrong about the mechanism, or about who mints defaults.

The emperor has no evals.

<!-- WORKING NOTES (strip before publish)

Parked decisions for June:
- Title vs kicker: currently title "Hiring Is Evals", kicker closes. Emperor-as-title still live.
- "Deprecated on the author's behalf" wrinkle: currently omitted from prose (OpenAI made Verified on Princeton's bench). Reinsert if wanted.
- Personal receipt slot: an interview June ran/took exhibiting a failure mode. No slot currently; strongest candidates: opening or "An excellent bar."
- Scope close line ("the measurement critique extends beyond software hiring; the instrument does not") — currently NOT in prose; add to "Who ships it first" or cut.
- Cross-link to Trust Is a Cache when it ships (crossover engine paragraph).

TODO before publish:
- /table-style the crosswalk.
- Verify/receipt: Symbolica/ARC-AGI-3 primary source; five engineer-hours; coin lean; LeetCode-2012; "nobody versions an interview loop"; everyone-copies-lab-loops; prep-industry-as-decay-cause (dated observable or mechanism flag); Anthropic-loop-leans-work-sample observation.
- Jargon gloss on first use: Goodharting, held-out, saturation, construct, range restriction (crosswalk placement covers some).
- /humanize, /not-but, /flow, /em-dash passes.
- og:image? The band SVG is inline; decide if a social card is wanted.
-->
