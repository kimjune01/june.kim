---
variant: post
title: "97% on SWE-bench Verified"
tags: coding, methodology
---

97% on SWE-bench Verified, artifacts public:

[github.com/kimjune01/swebench-verified](https://github.com/kimjune01/swebench-verified)

The exact number is **426 / 438 eligible**, or **426 / 500** across the full Verified set. The repo accounts for the gap: 44 `sphinx-doc` instances that cannot run airgapped, and 18 documented bad instances. The scoreboard comes from committed official grader summaries rather than prose.

The denominator is the important part. Every run lands in `results/`, win or loss. Re-runs are only for external faults: box death, serialization bugs, co-tenant contention. Reasoning losses stay losses.

This is a leaderboard configuration rather than a clean science claim. SWE-bench Verified is contaminated for modern models, including the ones used here. The repo says that plainly. Treat it as an inspectable artifact: frozen skills, visible logs, official `swebench.harness.run_evaluation` reports, and an append-only record.

The pipeline is three skills in a loop:

- `recon`: reproduce and localize.
- `craft`: patch and challenge the patch.
- `audit`: run the full suite and route failures.

<iframe
  width="560"
  height="315"
  src="https://www.youtube.com/embed/gRVjAtPip0Y"
  title="YouTube video player"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  referrerpolicy="strict-origin-when-cross-origin"
  allowfullscreen>
</iframe>

The claim is simple: here is the trail.
