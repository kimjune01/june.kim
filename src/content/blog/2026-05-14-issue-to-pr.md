---
variant: post-medium
title: "(Issue) → PR"
tags: pageleft, coding
---

Sweep and triage work. The pipeline scans open issues across 200 OSS repos, picks ones worth fixing, opens a fork, runs a hypothesis graph against the bug, implements with TDD, sends the diff to two adversarial reviewers, ships the PR, handles pushback, and either merges or learns from the closure. End to end, no human in the orchestration loop.

The receipts are public. [184 hypothesis graphs](https://github.com/kimjune01/sweep/tree/master/repo-hypotheses) committed and dated. 47 PRs merged this month. One pushback today: an [Envoy](https://www.envoyproxy.io/) maintainer flagged a clock-discontinuity concern. The pipeline tested the claim against Envoy's own JWT and OAuth2 code, found four file-line citations of the same trade-off resolved the same way, and posted a two-line response with the hypothesis graph linked. Maintainer hasn't replied. The position holds without further input from me.

Today, [scverse/pertpy](https://github.com/scverse/pertpy/pull/970) had two security-shaped bugs in a fix I'd already shipped. The pipeline's QA volley caught them on re-review, regenerated the fix, attested the patch, and pushed back to the same PR branch. I read the report afterward and approved the comment.

This will become the ordinary thing. Autonomous PR submission works end-to-end on bug-fix-shaped issues at 200-500 star repos. Nobody noticed because the receipts arrived without ceremony. The [skills](https://github.com/kimjune01/sweep) arrived without ceremony too.

### The detector

The pipeline is orchestration shape, not raw model power. The hypothesis-graph format does the cognitive work: claim, perturbation, classify, follow the edge. Volley discipline catches what one model misses. Patience keeps standing. Receipts can't be faked by lazy agents.

These are shapes. Shapes are distillable.

Training data isn't capped at what my pipeline produced. Every merged PR in git history is a graph waiting to be replayed: take the parent commit, simulate the investigation that found the canonical fix, save the trace. The 184 are receipts; the corpus is unlimited. Format as JSONL, fine-tune a 7B model on next-node prediction, pair it with a sniff-guard classifier trained on the same merge/close corpus. The agent generates PRs, the detector predicts whether each would merge, the agent rewrites until the detector clears. Both run on a MacBook.

This is Karpathy's [cognitive core](https://x.com/karpathy/status/1937902205765607626) at the smallest scale. Strip world knowledge, keep reasoning shape, bolt on tools (code search, test runner, gh CLI, escalation to Opus when uncertain). The model doesn't need to know React is a JS library; it needs to know that when the test fails, the next perturbation is to read the failing assertion, classify whether the bug is in the implementation or the test, and follow the right edge.

The detector is the durable half. Models commoditize on an eighteen-month cycle; calibrated detectors trained on per-repo merge corpora don't, because every repo is its own taste, and the corpus only grows. Train the detector on today's merged corpus, it enforces today's standards on tomorrow's PRs. Tomorrow's merged corpus reflects the new floor. Next iteration enforces that. Same dynamic that gave us `-Wall` then `-Wextra` then `-Werror`. Untyped JS then TypeScript then `strict: true`. AI didn't lower the floor. It moved the floor from implicit to explicit and turned it into something every maintainer can install.

Same move spam filters made for mailmerge in the late 90s. Cheap mass email broke the inbox until recipients shipped free filters; the medium recovered, and mailmerge became infrastructure. Recipients build filters, not senders.

The bench is the stepping stone.

### Local

Every dev runs the agent and detector locally.

You write prose specifying what you want. The local agent fans out, generates twenty PR variants in parallel, the detector filters; only variants predicted to merge survive. You see a slate of curated suggestions, pick one, write more prose. Your machine is your dev team. The job stops being syntax and becomes spec-writing and selection.

Code becomes a build artifact of prose, the way assembly became a build artifact of C in the 1970s. You don't write assembly anymore unless the compiler can't handle it. You won't write code anymore unless the local agent can't handle it. The category of "things the agent can't handle" shrinks every quarter.

Why host agents with network latency and frontier-model rates when a distilled one does 90% of the work locally? When it can't, it escalates by handing the attested hypothesis graph to SOTA. The graph is the interface; the gradient runs one direction.

Reviewer attention stays the bottleneck, but the PRs reaching maintainers are pre-filtered against the public floor. The pipeline I run today is the externalized prototype: a single-dev version operating on other people's repos, because that's where the historic merge data lives. The local-army version is the same machinery aimed inward. Two artifacts make it real: a small model trained on hypothesis-graph shape, and a detector trained on what your repos actually merge. Both exist in proto form. Distillation is the engineering work that ships them.

[PageLeft](/pageleft) will be waiting to index the prose.
