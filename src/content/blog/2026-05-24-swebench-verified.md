---
variant: post
title: "85% on SWE-bench Verified, 97% of eligible"
tags: coding, methodology
---

Against the full 500-instance Verified set: **426 / 500, 85.2%**. Against the eligible pool I could actually run: **426 / 438, 97.3%**. Both numbers are real; the gap between them is the honest part of this post. Artifacts public:

[github.com/kimjune01/swebench-verified](https://github.com/kimjune01/swebench-verified)

The 62-instance gap is **44 `sphinx-doc`** instances (tox-based, cannot run airgapped) and **18 documented bad instances** (broken Docker envs, gold patches that fail to grade, or coverage too weak to trust). The full set reconciles exactly: 426 resolved + 12 attempted-but-unresolved + 44 sphinx unrun + 18 known-bad excluded = 500. The scoreboard comes from committed official grader summaries rather than prose.

The denominator is the important part. Every run lands in `results/`, win or loss. Re-runs are only for external faults: box death, serialization bugs, co-tenant contention. Reasoning losses stay losses.

This is a leaderboard configuration rather than a clean science claim. SWE-bench Verified is contaminated for modern models, including the ones used here. The repo says that plainly. Treat it as an inspectable artifact: frozen skills, visible logs, official `swebench.harness.run_evaluation` reports, and an append-only record.

The pipeline is three skills in a loop. `recon` reads the failing test and localizes; `craft` writes the patch and has a codex subagent attack it; `audit` runs the full suite and routes a non-resolved verdict back to whichever stage was wrong.

<svg viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg" style="width:100%;margin:1.5em 0;display:block">
  <style>
    text { font-family: monospace; font-size: 14px; fill: currentColor; }
    .sub { font-size: 11px; opacity: 0.7; }
    rect { fill: none; stroke: currentColor; stroke-width: 1; }
    line, path { stroke: currentColor; stroke-width: 1; fill: none; }
    polygon { fill: currentColor; }
  </style>
  <defs>
    <marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <polygon points="0,0 6,3 0,6"/>
    </marker>
  </defs>
  <rect x="20" y="50" width="120" height="44"/>
  <text x="80" y="70" text-anchor="middle">recon</text>
  <text x="80" y="85" text-anchor="middle" class="sub">reproduce + localize</text>
  <rect x="200" y="50" width="120" height="44"/>
  <text x="260" y="70" text-anchor="middle">craft</text>
  <text x="260" y="85" text-anchor="middle" class="sub">patch + codex attack</text>
  <rect x="380" y="50" width="120" height="44"/>
  <text x="440" y="70" text-anchor="middle">audit</text>
  <text x="440" y="85" text-anchor="middle" class="sub">full suite + route</text>
  <line x1="140" y1="72" x2="196" y2="72" marker-end="url(#a)"/>
  <line x1="320" y1="72" x2="376" y2="72" marker-end="url(#a)"/>
  <path d="M440,94 C440,150 80,150 80,98" marker-end="url(#a)"/>
  <text x="260" y="143" text-anchor="middle" class="sub">non-resolved: re-enter at the stage that was wrong</text>
</svg>

The official grader is the only verdict. The number below is not prose I am asking you to trust; it is re-derivable from the committed logs by the leaderboard's own `analysis.get_results`:

| Repository | Resolved | Repository | Resolved |
|---|---|---|---|
| scikit-learn | 32 / 32 | pytest | 18 / 19 |
| pydata/xarray | 22 / 22 | sympy | 70 / 75 |
| seaborn | 2 / 2 | astropy | 15 / 22 |
| flask | 1 / 1 | pylint | 7 / 10 |
| django | 223 / 231 | psf/requests | 4 / 8 |
| matplotlib | 32 / 34 | sphinx-doc | 0 / 44 |

`sphinx-doc` is a clean 0/44: it is tox-based and cannot run airgapped, so it scores zero rather than vanishing from the denominator. That is the whole ethos in one row.

## I submitted it. I expect to be rejected.

I opened a pull request to the [SWE-bench leaderboard](https://github.com/SWE-bench/experiments) with the full bundle: predictions, per-instance logs and traces, and a `results` block that regenerates from the logs.

As of November 18, 2025, Verified submissions require an author "affiliated with an academic institution or established research lab" plus an arXiv preprint or technical report. I have neither. I am an independent researcher with a blog and an append-only repo.

I submitted anyway, and I said so on the record in the PR. The policy exists to keep the board rigorous, transparent, and reproducible. My artifact is more inspectable than the leaderboard usually requires: every losing run is committed, the exclusions are committed, the skills are frozen and tagged, and the score regenerates from the logs by the leaderboard's own `analysis.get_results`. If that gets rejected on affiliation, the rejection is the more interesting artifact than the merge would have been. It marks exactly where the gate stops measuring the work and starts measuring the letterhead.

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
