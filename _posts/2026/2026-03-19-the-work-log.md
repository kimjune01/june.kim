---
layout: post
title: "The Work Log"
tags: methodology coding
---

*Part of the [methodology](/methodology) series. Builds on [Double Loop](/double-loop) and [Consolidation](/consolidation).*

> What if your team could learn from each other's mistakes without sitting through meetings?

Every LLM session dies. The context window fills, the conversation ends, and everything learned — every dead end, every pivot, every "oh wait, that's the wrong approach" — evaporates. The next session starts from zero.

The work log fixes this. Append-only, machine-written, machine-read. Not documentation. Not a summary. A timestamped transcript of decisions and their reasons, written by the agent *during* the work.

## What goes in

Each entry records what happened and why. Not just "fixed the bug" but "the control-loop bug happened because graduation triggers on message count while summarization triggers on tokens — two thresholds on different axes that never align." The diagnosis matters more than the fix. The fix is in the code. The diagnosis is nowhere else.

Failures go in too. Especially failures. "Sonnet flagged 8 issues, applied fixes, broke the embedder. Reverted. The IDF formula change made `log((1+1)/(1+1)) = 0` for single-document terms." That's a lesson no commit message carries.

## Three properties

**Resumability.** A new session reads the log and picks up mid-project. Not "remind me what we were doing" but "Step 14 completed, Step 15 blocked on X." The agent doesn't need to re-derive the project state from code archaeology.

**Shareability.** A different agent — or a human — reads the same log and gets the full reasoning chain. Not just the current state of the code, but why it looks the way it does and what was tried before.

**Consolidation.** Patterns emerge across entries that no single session saw. Seven rounds of codex review produced a through-line: the same class of bug (control-loop misalignment) appeared in three different forms. Only the log connected them.

## The team unlock

This is where it gets interesting. Humans share knowledge through meetings, pair programming, code review, documentation. All low-bandwidth. A standup conveys maybe 200 words of context per person. A code review conveys the *what* but rarely the *why not*.

Work logs change the economics. If everyone on the team produces one — or more precisely, if everyone's agent produces one — then catching up to each other's capabilities becomes a reading problem, not a communication problem. An agent can synthesize ten work logs overnight and extract:

- What patterns keep failing across the team
- What each person learned that others haven't encountered yet
- Where two people solved the same problem differently and one solution was better
- Which decisions were made under assumptions that later proved wrong

That's not a standup. That's consolidation across minds. The bandwidth between humans is 200 words per meeting. The bandwidth between work logs is the entire reasoning history, machine-readable, cross-referenceable.

## What this replaces

Not documentation. Documentation is a finished artifact written for future readers. The work log is a live record written for future sessions. Documentation says "here's how it works." The work log says "here's how we got here and what we tried that didn't work."

Not commit messages. Commit messages are per-change. The work log is per-project. "Fixed token-aware graduation" is a commit message. "The graduation threshold was too high because the gemini-cli design assumed a different timing model — messages accumulate during long LLM calls, not during user think time" is a work log entry.

Not sprint retros. Retros happen every two weeks and capture what people remember. The work log captures what actually happened, in real time, including the things nobody would remember to mention.

## The format

It doesn't need to be fancy. Markdown with timestamps and step numbers. The structure that matters:

- **What happened** (decision, failure, discovery)
- **Why** (the reasoning, not just the outcome)
- **What changed** (commits, files, config)
- **What's next** (so the next session knows where to start)

The agent writes it. The human reviews it. Same [double loop](/double-loop) that works for prose — the agent does the labor of recording, the human does the judgment of what matters.

## Evidence

This project produced a 19-step work log across multiple sessions. It tracked 7 rounds of codex review, a control-loop bug that unit tests missed, a parallel implementation experiment (codex vs Claude), and a live debugging session where the feature wouldn't trigger in production despite passing all tests. Without the log, each session would have re-derived context from git history. With it, each session started at the current step.

The metacognition project produced an even longer log across 4 experimental rounds. It caught a deduplication bug that invalidated an entire run, a $10 data loss from missing disk persistence, and a search strategy that improved pass rates from 1% to 14%. Each lesson was applied to the next round because the log carried the diagnosis forward.

## The question

If ten engineers each produce work logs, and an agent reads all ten overnight, what does the team know on Monday that it didn't know on Friday?

The answer is: everything each person learned, cross-referenced against everything everyone else learned, with conflicts flagged and patterns extracted. Not filtered through memory, meeting fatigue, or "I forgot to mention." The full reasoning history of the team, consolidated.

That's not a productivity tool. That's a different kind of team.

---

*Written via the [double loop](/double-loop).*
