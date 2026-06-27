# Email — Anthropic (job track, Alignment Science: auditing / honest oversight)

Closest fit is the Alignment Science team's alignment-auditing line. Lead with the substantive connection
(artifact-first), not the job ask. Cites "Reasoning Models Don't Always Say What They Think" (2505.05410)
as the threat the method routes around; closing question engages the auditing-agents work directly.
Best sent via warm intro to someone on alignment/auditing; works as the cover note on an application too.

To: [named contact on Alignment Science if you have one — warm intro >> careers portal]
Subject: Audit findings that carry their own re-runnable kill condition

---

Hi [name],

"Reasoning Models Don't Always Say What They Think" (arXiv:2505.05410) is the result my work is built around: when RL induces a reward hack, the model uses it and doesn't verbalize it, so any oversight that reads the trace goes blind exactly when it matters. I've been building the verdict that doesn't trust the trace.

Each agent claim is bound to a re-runnable kill condition and passes only when an independent replay reproduces the effect, so the verdict comes from rerunning a check rather than from a chain-of-thought or a self-report. Most of it was built and demonstrated on Claude Code against Claude models. A worked example in The Hypothesis Graph (june.kim/the-hypothesis-graph-semantic-memory-methodeutics) shows a self-grading agent staying green on its own tests and still wrong, separated only by the external rerun. One field point: on a contamination-free, post-cutoff bug, moving the check outside the model carried Sonnet 4.6 to a fix Fable 5 couldn't reach unaided, with no training. The external oracle was the active ingredient.

Your auditing agents and the hidden-objectives game still grade largely on the auditor's judgment of the target's artifacts. Have you tried making each audit finding carry its own re-runnable kill condition, replayable by an independent process to confirm or falsify it, so the audit's verdict is reproducible without trusting either the target's self-report or the auditor model's summary? Where did replayable falsification break down: cost, environment non-determinism, or claims that resist operationalization?

I'm exploring whether there's a fit on the Alignment Science side, auditing or honest-oversight specifically. I can send the papers or do a work-sample.

june.kim · github.com/kimjune01

June
