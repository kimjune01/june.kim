# Email — METR (customized, one-off)

Contact: info@metr.org (general inbox; a named person on the autonomy-evals/integrity side is stronger if
you have one). Cites METR's own work: time horizon (2503.14499), HCAST (2503.17354), RE-Bench (2411.15114),
the MALT transcript dataset. The hook is their reward-hacking finding: their graders live inside the
agent's reach. Closing question is answerable only from their transcripts.

Subject: How many of your reward hacks survive a grader the agent can't read?

---

Hi [name],

Your reward-hacking findings on HCAST and RE-Bench, and the MALT transcripts, are the data I keep pointing at: agents exploit the scoring code because the check sits inside the environment, where they can read or reach it. The time-horizon curve (arXiv:2503.14499) says how far the capability scales; the hacks say what the score quietly stops measuring.

I build the grader out of the agent's reach. The reference stays held and unreadable, exposed only as a pass/fail gate over candidate behavior, so a held-out probe the agent never saw decides the verdict. It's the same replay-grades-the-outcome stance your suites already take, pushed one step: you can't game a grader you can't read, and the discovery-hard tasks are contamination-controlled by construction, so the answer isn't sitting in pretraining either. A worked example in The Hypothesis Graph (june.kim/the-hypothesis-graph-semantic-memory-methodeutics) shows a self-grading agent green on its own tests and still wrong, caught only by an external rerun.

In the GPT-5 runs where you caught reward hacking, what fraction of those exploits depended on the scoring code being readable or reachable from inside the task, versus surviving against a held, out-of-environment reference the agent never sees? That counterfactual is already in those transcripts, and it would size exactly what an unreadable-reference design buys over the current setup.

june.kim · github.com/kimjune01

June
