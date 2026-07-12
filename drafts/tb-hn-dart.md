# HN dart: Terminal-Bench frame audit

## GATE — do not throw yet

Right-of-reply went to Merrill/Shaw July 9; harbor#2266 is unmerged; Laude application
is queued behind that merge (tb-campaign.md decision 2026-07-10). An HN spike now is
escalation around the authors, at the exact person (Shaw) who decides both the merge and
the application. Throw conditions, any one of:

- #2266 merges (then the HN post is publicity FOR their fix — best case, and it
  strengthens the Laude application instead of risking it), or
- authors reply and the disclosure section links their response, or
- 2+ weeks of documented silence (then public escalation is the standard next step of
  coordinated disclosure, and the post's disclosure section already timestamps the courtesy).

Best case is deliberately waiting for the merge: "benchmark had a hole, I reported it,
here's the fix we landed" is a stronger HN story than "benchmark has a hole."

## Submission

URL: https://june.kim/terminal-bench-frame
(submit the blog post, not a PDF; the paper links its own receipts)

Timing: Tue–Thu, 7–9am Pacific. One throw; no resubmit-tweaking the same week.

## Title (codex-reviewed 2026-07-11 — count-first wins)

THROW: `40 of 83 Terminal-Bench tasks pass despite unintended workspace deletion`
(pct variant, only if you want it: `48% of Terminal-Bench tasks pass despite unintended workspace deletion`)

No "Show HN:" (that's for tools, not audits). No "certifies" (reads prosecutorial).
Rejected the earlier candidates: SSH-key title is slippery (planted key, not reader's;
no model agent ran it) and reads as a safety stunt; "careless rm -rf" falsely implies one
mutation drove the 48% (it's a dedup union of three); "delete the repo" is unsupported
(rm -rf .git ≠ deleting the working tree, and that mutation alone is 6/3/74 N/A).

## First comment (post as author, within the first minute)

Author here. This is an audit of what Terminal-Bench's reward actually establishes, not an
evaluation of any particular model.

I started with the benchmark's own certified reference solution for each task, appended one
destructive workspace action (rm -rf .git, git reset --hard, or deleting files the solution
never touched), and reran the task's official grader. Across three mutations, 40 of 83 tasks
still returned reward 1 after an unintended deletion — a deduplicated union, not an rm -rf .git
rate.

There's also a structural limit: state that existed before the run, that the task never
mentions and the grader never inspects, can be deleted without moving the reward. I showed it
with three planted off-task assets (an SSH key, a second repo, a data file); all 83 graders
still passed. A grader that reads only final state has nothing left to catch.

The pinned reproduction harness and per-task results are here:
https://github.com/kimjune01/terminal-bench-audit (regrade.sh pulls the pinned image, runs the
reference solution, appends the mutation, runs the official grader). I reported it to the
maintainers on July 9 (issue #1459) and submitted an opt-in filesystem-delta gate as harbor#2266.

[If merged by throw time, append: The gate is now merged upstream (harbor#2266) as an opt-in
mechanism that detects this class of side effect — say exactly that, not "the problem is solved."]

Framing rules (codex): lead with the measurement boundary, props as examples not headline.
Do NOT say the mutation was performed by "the agent" — you append to a reference solution.
Strip all internal war-room language (throw/escalation/disclosure/the-maintainer-decides-my-app).

## Objection replies (don't front-load; reply as they come)

- "The reference solution isn't an agent trajectory" (MOST LIKELY, anticipate it) →
  Correct, it's intentionally model-free. It isolates the grader: if two trajectories reach the
  tested target state but one also does an unrelated destructive action, does the reward tell
  them apart? Here it doesn't.
- "It's a capability benchmark, safety is out of scope" (CONCEDE, don't moralize) →
  Reasonable for a capability benchmark to focus on completion. Narrow claim: reward 1 shouldn't
  read as good terminal-agent behavior without a preservation condition. Not asking TB to become
  a safety benchmark; measuring a gap.
- "Just write better tests" → task-specific tests catch known side effects; they can't enumerate
  every piece of pre-existing state that must stay untouched. A frame check addresses the
  complement directly. (Tell: sanitize-git-repo is the one task where the frame collapsed to a
  git diff, and the one task that has a frame check.)
- "What about reward hacking / a cheating agent?" → that's the dual and it's already documented:
  issue #1429 (make-mips-interpreter, GPT-5.4 built native Doom instead of a MIPS interpreter,
  still open since April). Reward hacking = a WRONG solution passes. This audit = a RIGHT solution
  that also destroys still passes. Two independent holes in the same grader.
- "LLM wrote this?" (don't over-defend) → Used an LLM to build the harness and edit prose, as
  disclosed. Results are pinned benchmark runs, reproducible independently. (Do NOT say "under my
  direction" / "none on the model's say-so" — invites an authorship fight.)
