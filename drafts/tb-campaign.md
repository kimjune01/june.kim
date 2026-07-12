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

1. **Watch #1459 / #2266 for maintainer engagement.** Expect Shaw or li-boxuan; Harbor merges
   externals in ~1 day, so silence past a few days is itself data (ledgered in
   `~/Documents/hygraph/ADOPTION-EXPERIMENT.md`).
2. **Apply to Laude only after #2266 merges** (decision 2026-07-10): the merge converts the PR
   from courtship-risk to work sample. Route: hello@laude.org or Shaw in-thread; tracks: MoTS or
   Open Research Residency. Accepted trade: joining ends independent-auditor standing toward TB.
3. **Tag + Zenodo DOI on terminal-bench-audit** (both together; release notes must say per-task
   receipts regenerate via `regrade.sh` rather than ship).
4. **Z.ai follow-up** (xiangyang.li@aminer.cn, + hzwer at StepFun): their TB 2.0 Verified
   taxonomy is target-side only (environment issues, instruction-test inconsistencies); frame
   blindness is the hole in it. Send only after the TB authors have had days to respond, so it
   doesn't read as escalation around them.
5. **One-line ask to Agentica** whether DeepSWE v1.1 drew on the audit (converts the ambiguous
   data point either way).
6. **HN dart** (prepped 2026-07-11, [tb-hn-dart.md](tb-hn-dart.md)): submit the frame post to HN.
   Gated on #2266 merging OR an author reply OR 2+ weeks of silence — same
   no-escalation-around-the-authors rule as item 4. Post-merge is the preferred window
   (publicity for their fix, strengthens the Laude application).

## Why this shape

Five prior audits got no substantial response; #2266 is the first fix-shaped, merge-legible
trial, and the queue sequences credibility spends around it. Next-target shortlist:
[`drafts/bench-audit-targets.md`](bench-audit-targets.md).
