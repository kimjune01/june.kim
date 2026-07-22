# Terminal-Bench campaign — state and queue

Shipped July 9, 2026: paper live at [june.kim/terminal-bench-frame](https://june.kim/terminal-bench-frame)
(with disclosure section), issue [terminal-bench#1459](https://github.com/harbor-framework/terminal-bench/issues/1459),
right-of-reply email sent to Mike Merrill (mchlmerrill@gmail.com, now Anthropic evals MTS) and
Alex Shaw (alexgshaw64@gmail.com, Laude founding MTS, the operational owner), and the fix
implemented as [harbor#2266](https://github.com/harbor-framework/harbor/pull/2266) — opt-in
`frame_gate`, observational, all CI green, codex 3 rounds + 4 Devin findings incorporated.
Fork: `~/Documents/harbor-1`. Audit repo: `~/Documents/terminal-bench-audit`.

## Queue, in order

Before acting on any item, check the live state of #1459/#2266 — engagement changes the ordering.

1. Policy (2026-07-20): unmerged upstream work rots where it lies; their repo, their job to
   clean up. No follow-ups, no pings on #1459/#2266. The PR stands as a work sample either way.
   ~~**Watch #1459 / #2266 for maintainer engagement.**~~ Expect Shaw or li-boxuan; Harbor merges
   externals in ~1 day, so silence past a few days is itself data (ledgered in
   `~/Documents/hygraph/ADOPTION-EXPERIMENT.md`).
2. ~~Apply to Laude only after #2266 merges~~ SENT (June emailed Laude directly, reported
   2026-07-20; the merge gate was dropped since the PR stands as a work sample unmerged).
   Accepted trade stands: joining would end independent-auditor standing toward TB.
3. ~~Tag + Zenodo DOI on terminal-bench-audit~~ DONE 2026-07-20: [v1.0.0 release](https://github.com/kimjune01/terminal-bench-audit/releases/tag/v1.0.0),
   DOI [10.5281/zenodo.21463236](https://doi.org/10.5281/zenodo.21463236) (concept 10.5281/zenodo.21463235),
   release notes state receipts regenerate via `regrade.sh`. Archive lines added to repo README + frame post.
   Items 4 (Z.ai) and 5 (Agentica) dropped 2026-07-20: June judges neither will engage. Item 6 (HN dart) already done.
4. **Z.ai follow-up** (xiangyang.li@aminer.cn, + hzwer at StepFun): their TB 2.0 Verified
   taxonomy is target-side only (environment issues, instruction-test inconsistencies); frame
   blindness is the hole in it. Send only after the TB authors have had days to respond, so it
   doesn't read as escalation around them.
5. **One-line ask to Agentica** whether DeepSWE v1.1 drew on the audit (converts the ambiguous
   data point either way).
6. ~~**HN dart**: submit the frame post to HN.~~ FIRED (reported 2026-07-21; the gate on
   #2266 merging OR an author reply OR 2+ weeks of silence was not waited out). Draft removed.

## Adjacent thread: BenchRisk (McGregor)

Filed 2026-07-20: [BenchRisk#8](https://github.com/BenchRisk/BenchRisk/issues/8), the frame
clause as a new failure mode for their registry, with the TB receipts and #2266 as the
mitigation's reference implementation. BenchRisk is McGregor's (AVERI Lead Research Engineer,
NeurIPS 2025 paper); his paper defers agentic benchmarks to future work, which this supplies.
Neutral third venue, so it publicizes #2266 without escalating around the TB authors.
A McGregor email waits on a response to #8 (that response is the trigger; beat 1 writes itself).
Full clause-vs-57-modes mapping: 7 of the checklist's clauses are absent from his registry
(frame, gold, spec, receipt retrievability, oracle witnesses, selection-by-failure, wrong
rulebook); file more only after #8 gets a read, one at a time.

## Why this shape

Five prior audits got no substantial response; #2266 is the first fix-shaped, merge-legible
trial, and the queue sequences credibility spends around it. Next-target shortlist:
[`drafts/bench-audit-targets.md`](bench-audit-targets.md).
