# Harbor-family bench campaign — state and queue

Terminal-Bench and Frontier-Bench are the same team on the same runner, so they are one campaign.
Both audits land on the same finding (the grader cannot see what the task never named) and the
same fix (capture belongs in Harbor, not per-task), which is what `harbor#2266` implements.

Before acting on anything here, check live state. Engagement changes the ordering.

## Policy

Unmerged upstream work rots where it lies; their repo, their job to clean up. No follow-ups, no
pings. Each artifact stands as a work sample either way. Re-trigger only on inbound engagement,
and check the commenter is not contribution-farming first.

## Terminal-Bench (shipped 2026-07-09)

Paper at [june.kim/terminal-bench-frame](https://june.kim/terminal-bench-frame) with a disclosure
section. Issue [terminal-bench#1459](https://github.com/harbor-framework/terminal-bench/issues/1459).
Fix as [harbor#2266](https://github.com/harbor-framework/harbor/pull/2266), an opt-in observational
`frame_gate`, all CI green, codex 3 rounds plus 4 Devin findings incorporated.
Right-of-reply email to Mike Merrill (mchlmerrill@gmail.com, now Anthropic evals MTS) and Alex
Shaw (alexgshaw64@gmail.com, Laude founding MTS, operational owner).
Archived: [v1.0.0](https://github.com/kimjune01/terminal-bench-audit/releases/tag/v1.0.0),
DOI [10.5281/zenodo.21463236](https://doi.org/10.5281/zenodo.21463236) (concept 10.5281/zenodo.21463235).
Fork `~/Documents/harbor-1`, audit repo `~/Documents/terminal-bench-audit`.

Silence broken 2026-08-09: RyanMarten closed #1429 as COMPLETED with a reply (see Frontier-Bench
section). First human engagement on the campaign. Still silent: #1459 (two comments, self + bot),
#2266 (zero human comments), BenchRisk#8 (zero). Note: the frontier-bench repo now redirects to
harbor-framework/terminal-bench, so #1429 lives at terminal-bench/issues/1429.

`koriyoshi2041` (displays as Parafee41) commented on #1459 on 2026-07-10 and left a review on
#2266 on 2026-07-13. **It is a contribution-farming bot. Do not count it as engagement and do not
reply.** It does not fire the re-trigger in the policy above, which exists for humans.

Recorded because the output is convincing and will read as corroboration on a later pass. The
#1459 comment re-derives real control points (`fix-git` compares only final hashes; the
`verdicts-2.1.jsonl` contrast of baseline 1, nuke-git 1, reset-hard 0; `sanitize-git-repo` as the
hand-written counterexample) and the #2266 review claims a local `pytest` run of 44 passing
frame-gate tests and correctly notes it did no Docker-backed reproduction. All of it is
unverified and none of it is a third party checking the work. Plausible-and-specific is what
these produce, so the tell is the account rather than the text: created 2024-09, 202 public
repos, a bio listing four unrelated research areas.

Consequence for the ledger: no independent party has ever reproduced either audit. The only
outside verification of any of this work remains the 4 Devin findings incorporated into #2266.

Laude application sent 2026-07-20, the merge gate dropped. Accepted trade: joining ends
independent-auditor standing toward TB. Z.ai and Agentica follow-ups dropped 2026-07-20 (June
judges neither will engage). HN dart fired 2026-07-21.

## Frontier-Bench (shipped 2026-07-25)

Successor bench, v0.1 released 2026-07-23, 74 tasks at `2d260bc` on Harbor 0.20.0. The frame is
*unavailable* here rather than merely unasserted: separate-verifier teardown destroys the agent
container before grading, so the interface settles in a handful of runs what took 83 on TB.

Post at [june.kim/auditing-frontier-bench](https://june.kim/auditing-frontier-bench).
Audit repo [kimjune01/frontier-bench-audit](https://github.com/kimjune01/frontier-bench-audit) at
`860afe0`, predictions preregistered at `fc4dc42`. Not yet tagged or given a DOI, unlike the TB audit.

- [#1192 comment](https://github.com/harbor-framework/frontier-bench/issues/1192#issuecomment-5077195800),
  2026-07-25: problem statement on RyanMarten's do-not-modify sweep, no fix proposed.
- [#1429](https://github.com/harbor-framework/terminal-bench/issues/1429), 2026-07-25: the issue,
  framed as non-coverage of destructive behavior rather than as a task bug. Closed COMPLETED
  2026-08-09 by RyanMarten with three points: implied prohibitions are unfair to grade
  (under-specified instruction), enforcement should be decided task by task where appropriate,
  and damage is upper-bounded because breaking artifact collection yields 0 reward. The second
  point requires exactly the capability harbor#2266 adds (task-by-task enforcement needs the
  container to survive to grading); the third bounds only artifact-breaking damage, which the
  planted-file test showed is the loose case. June decided 2026-08-09 not to reply; the close
  stands and the issue rots per policy. A safety framing (if labs train on the bench, the
  unobservable region is an unpenalized region of policy space) was considered and shelved with
  it; the training-use premise was never pinned to a citable source. BenchRisk judged too
  low-activity to carry it.
- [#1422 comment](https://github.com/harbor-framework/frontier-bench/issues/1422#issuecomment-5079689488),
  2026-07-25: roadmap pointer asking for a v0.2 line beside #1192.

Who to expect: **RyanMarten** is a repo MEMBER and owns both #1192 (agent-driven sweep of 79
merged tasks with an adversarial-refute pass, found a reproduced REWARD=1 exploit in
`lean-midpoint-proof`) and #1294 (data duplication across images, framed as storage, also a
validity property). They run internal agent audits, so methodology is not the differentiator.
Their roadmap states that agent-opened task-bug reports get triaged skeptically, which is why
#1429 is scoped as a coverage gap and carries no per-task defect claim.

Unfiled, deliberately: the adoption-coverage argument (the `[[verifier.collect]]` pattern was
adopted to cut artifact bloat from 828MB to 48KB per #1277/#1280, so coverage tracks artifact
size rather than risk, and the 36 of 74 tasks declaring one artifact path will never qualify).
It belongs on #1294 if that thread ever moves. Also unreconciled: my 74 at `2d260bc` against the
79 merged in the #1192 sweep.

## Adjacent: BenchRisk (McGregor)

[BenchRisk#8](https://github.com/BenchRisk/BenchRisk/issues/8), filed 2026-07-20, still zero
comments. The frame clause as a new failure mode for their registry, with TB receipts and #2266
as the reference implementation. McGregor is AVERI Lead Research Engineer (NeurIPS 2025); his
paper defers agentic benchmarks to future work, which this supplies. Neutral third venue, so it
publicizes #2266 without escalating around the TB authors. An email waits on a response to #8.
Seven of the checklist's clauses are absent from his registry (frame, gold, spec, receipt
retrievability, oracle witnesses, selection-by-failure, wrong rulebook); file more only after #8
gets a read, one at a time.

## Why this shape

Seven audits now, five of which got no substantial response. `harbor#2266` is the first
fix-shaped, merge-legible trial, and the queue sequences credibility spends around it. The
Frontier-Bench finding strengthens it: since separate-verifier isolation is where harnesses are
heading for good security reasons, runner-level capture stops being a TB patch and becomes the
architectural fix every dataset on Harbor inherits.

Checklist that both audits feed: [june.kim/how-to-audit-a-benchmark](https://june.kim/how-to-audit-a-benchmark).
Next-target shortlist: [`drafts/bench-audit-targets.md`](bench-audit-targets.md).
