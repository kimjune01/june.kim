---
layout: post
title: "The Work Log"
tags: methodology coding
---

*Part of the [methodology](/methodology) series. Builds on [Double Loop](/double-loop) and [Consolidation](/consolidation).*

> "I wasted 25 percent of my time in useless meetings." — [Dilbert](https://dilbert.com/search_results?terms=Useless+Meetings)

Why do we go to meetings? To coordinate. To learn what everyone else is doing. To catch mistakes before they compound. Why do we hate them? Because the bandwidth is terrible. A standup conveys maybe 200 words of context per person. A retro captures what people remember, not what happened. A code review shows the *what* but rarely the *why not*. We sit through an hour to extract ten minutes of signal.

The coordination matters. The learning matters. The format doesn't.

## What if the sync happened without you?

LLMs read and write at 100x your speed. They already draft your code, your tests, your commit messages. What if they also kept the record?

A work log. A live, append-only transcript of decisions and their reasons, written by the agent *during* the work. Timestamped. Structured. Machine-readable. Documentation is a finished artifact written after the fact. The work log is the raw record written *during* it.

The agent writes it as a byproduct of doing the work. No extra effort. No "I should write this down." It's already written down because the agent's reasoning *is* the log.

## What goes in

Each entry records what happened and why.

"Fixed the bug" is a commit message. "The control-loop bug happened because graduation triggers on message count while summarization triggers on tokens. Two thresholds on different axes that never align." That's a work log entry. The diagnosis matters more than the fix. The fix is in the code. The diagnosis is nowhere else.

Failures go in. Especially failures. "Sonnet flagged 8 issues, applied fixes, broke the embedder. Reverted." That's a lesson no commit message carries. No retro would surface it either. By next Friday, nobody remembers the detail.

## What the team gets

If everyone's agent produces a work log, catching up to each other becomes a reading problem. And machines are better at reading than humans are at meeting.

An agent reads ten work logs overnight and extracts:

- What patterns keep failing across the team
- What each person learned that others haven't encountered yet
- Where two people solved the same problem differently
- Which decisions were made under assumptions that later proved wrong

That's [consolidation](/consolidation) across minds. The full reasoning history, unfiltered by memory or meeting fatigue, cross-referenced with conflicts flagged.

A standup is 200 words per person. A work log is the entire reasoning chain. The agent reading it can process all ten before your coffee is ready.

## Evidence

The [union-find compaction](https://github.com/kimjune01/union-find-compaction-for-aider) project produced a 21-step work log across multiple sessions. It tracked 7 rounds of codex review, a control-loop bug that unit tests missed, and a live debugging session where the feature wouldn't trigger despite passing all tests. Without the log, each session would have rebuilt context from git history. With it, each session started at the current step.

The [metacognition](https://github.com/kimjune01/metacognition) experiment produced a longer log across 4 rounds. It caught a deduplication bug that invalidated an entire run, a $10 data loss from missing disk persistence, and a search strategy that improved pass rates from 1% to 14%. Each lesson carried forward because the log held the diagnosis, not just the fix.

## Monday morning

An agent read all ten work logs over the weekend. It didn't summarize status. It extracted *methodology*.

From one log: "Unit tests passed but the feature never triggered in production. Root cause: the test mocks bypassed the real tokenizer, so the control loop never fired. Lesson: integration tests must use real tokenizers, not word-count mocks." From another: "Piped experiment output to `head`, which sent SIGPIPE and killed the process early. Made this mistake three times. Lesson: never pipe long-running experiments." From a third: "LLM reviewer flagged 8 issues, applied fixes, broke the embedder. The IDF formula change made `log(1) = 0`. Lesson: LLMs are bad at reviewing code they're seeing for the first time. Use a different model for review than for writing."

Three people. Three lessons about *how to work*. Each one cost hours to learn. Without the work log, each lesson lives in one person's head, surfaces as a vague "be careful with mocks" in a retro, and fades. With it, the agent distills the pattern and everyone levels up.

That's the real unlock. The boring coordination (who's working on what, what's blocked, what shipped) happens while everyone sleeps. The agenda writes itself. But the meeting itself becomes something different: sharing methods, not status. "Here's a pattern three of you hit this week. Here's what worked. Here's what didn't." People discussing *how to get better at the work*, not the work itself.

Nobody dreads that meeting. People have more fun at work when they're learning. The work log is a communication channel that doesn't need Slack pings or TPS reports. It just needs the agent to keep writing while you keep working.

---

*Written via the [double loop](/double-loop).*
