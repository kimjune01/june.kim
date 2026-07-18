---
variant: post-medium
title: "Auditing MirrorCode"
subtitle: "A carefully built benchmark that measures scoped reimplementation and partial recall, sold as autonomous whole-program creation. A receipt for every claim."
tags: methodology, epistemology
---

[MirrorCode](https://arxiv.org/abs/2606.30182) ([Epoch AI](https://epoch.ai/) and [METR](https://metr.org/)) hands an AI an execute-only binary plus its docs and asks it to rebuild the whole program, graded byte-exact against the reference. The headline: *"the largest software project AI can complete on its own."* I ran it through the [how-to-audit checklist](/how-to-audit-a-benchmark).

Full audit, re-runnable, with a receipt for every claim: https://github.com/kimjune01/mirrorcode-audit

MirrorCode is a well-built instrument that measures scoped *reimplementation from a working oracle*, partly via *recall* of [published specs the artifact can't teach](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md) and of [these specific programs](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/03_how_much_is_recall.md), and is marketed as autonomous *creation*.

## What it gets right

MirrorCode is better-built than most, on several axes better than the [six benchmarks](/how-to-audit-a-benchmark) I audited before it. [Full credit, sourced.](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/04_what_it_gets_right.md)

- *Cheat-proofing is real.* Four isolated containers, scoring where the agent can't reach it, and an execute-only reference [enforced with seccomp-BPF, Landlock, and `RLIMIT_CORE=0`](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/04_what_it_gets_right.md) that blocks every byte-read path to the binary, and the scoring isolation defeated a live Gemini binary-wrap cheat.
- *I/O-only grading sidesteps the frame sin.* The oracle is `(stdout, stderr, exit)`, not final environment state, so the destructive-completion trap that [sank Terminal-Bench](/terminal-bench-frame) can't arise.
- *It did the two things most benchmarks skip:* [a human baseline and a memorization screen](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/04_what_it_gets_right.md). Both incomplete, both worth attempting.
- *Selection drained the recall surface.* A [complete per-target read](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/06_per_target.md) finds 2 recall targets out of 25, and none is a hash, image, or media target.
- *Not saturated.* 8 of 25 targets were never solved to 100%, and the large ones sit near zero, so the instrument still discriminates at the frontier.
- *The paper body is candid.* It concedes the code is piecemeal, "would not be merged," and that the results don't show AI can do arbitrary implementation work. The overreach is in the title, not the methods section.

## Some claims outrun the metric

- *Construct validity.* MirrorCode sells autonomous whole-program builds. The metric scores *reimplementation from a live reference oracle*, something narrower than the title names. [The gap, laid out.](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/00_construct_validity.md)
- *The human-labor claim is unmeasured belief.* Every "a human would take weeks/months" is *"we believe,"* from four contributors with a sevenfold spread and no completed baseline. The targets are open-source, so their [git histories anchor the real labor](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/01_human_labor.md). Creation runs to tens of developer-weeks, while MirrorCode's own baseline puts reimplementation at days. The marketing evokes the first and measures the second.
- *Two targets are recall by construction* (below), so a pass means recalling a spec rather than reconstructing it. [Witnesses.](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md)
- *Contamination, unquantifiable.* MirrorCode's own screen flags [17 of 25 targets as screen-positive](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/03_how_much_is_recall.md) for memorization. Whether recall inflates the 56% headline cannot be computed from released data, because the join that would show it was never published.
- *The receipts weren't shipped.* The per-task, per-model outcome grid is a figure in the paper, so [publishing it as data would cost almost nothing](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md). The run records still aren't public.
- *"Entire program" flattens heterogeneous units.* `cal` and `uuidparse` are tiny tools inside util-linux. `bib2json` is one format pair of pandoc. [Each scope is legitimate, but the aggregate phrase hides how different the tested surfaces are.](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/00_construct_validity.md)

## The two recall witnesses

Each carries a re-fetchable receipt. [Per-target audit.](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/06_per_target.md)

- *`brotlid`* decodes a bundled Brotli stream to exact bytes. That needs the [RFC-7932](https://www.rfc-editor.org/rfc/rfc7932.html) decoder and its ~120 KB static dictionary, neither in the docs nor derivable from the visible examples. MirrorCode defends it as "fully determined by the documented format," which [conflates the RFC with the bundled docs](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md).
- *`mailauth arc-seal`* must emit an exact RSA-SHA256 signature. Reproducing those bytes requires RSA, SHA-256, and the ARC canonicalization rules from the spec. [Receipt.](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/02_recall_and_verifiability.md)

## What I'd report instead

MirrorCode asks three questions: how large a program, how much faster than a human, and how reliably. Collapsing them into "56%" is the problem. The [constructive fix](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/05_recommendation.md) is a preregistered size-by-time-by-success profile. Plot whole-task success and time-to-success against program size, censor failures rather than dropping them, split out contamination, and show uncertainty so the curve can't imply precision it lacks.

<svg viewBox="0 0 680 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;margin:1.6em auto;display:block" role="img" aria-label="An illustrative profile: whole-task success against wall-clock to a full solve, one cluster per program-size bucket (small, medium, large). Success falls and uncertainty grows with size. The frontier is drawn as a bootstrap band rather than a line, and each point carries a Wilson interval on success and a bootstrap interval on time.">
  <style>
    .ax{stroke:#999;stroke-width:1}
    .gr{stroke:#e8e8e8;stroke-width:1}
    .lbl{font-family:ui-monospace,Menlo,monospace;fill:#555;font-size:12px}
    .tk{font-family:ui-monospace,Menlo,monospace;fill:#888;font-size:11px}
    .cap{font-family:ui-monospace,Menlo,monospace;fill:#666;font-size:11px}
    .s{stroke:#2d7d2d;fill:#2d7d2d}
    .m{stroke:#c0803a;fill:#c0803a}
    .l{stroke:#2b6cb0;fill:#2b6cb0}
  </style>
  <line class="gr" x1="90" y1="177.5" x2="620" y2="177.5"/>
  <line class="ax" x1="90" y1="45" x2="90" y2="310"/>
  <line class="ax" x1="90" y1="310" x2="620" y2="310"/>
  <text class="tk" x="84" y="49" text-anchor="end">100%</text>
  <text class="tk" x="84" y="181" text-anchor="end">50%</text>
  <text class="tk" x="84" y="313" text-anchor="end">0</text>
  <text class="lbl" x="28" y="178" text-anchor="middle" transform="rotate(-90 28 178)">whole-task success</text>
  <text class="lbl" x="355" y="336" text-anchor="middle">wall-clock to a full solve (log)</text>
  <path d="M95,62 C250,72 420,150 615,248 L615,300 C420,244 250,120 95,96 Z" fill="#999" fill-opacity="0.12"/>
  <line class="s" x1="175" y1="58" x2="225" y2="58" stroke-width="1.4"/>
  <line class="s" x1="200" y1="48" x2="200" y2="68" stroke-width="1.4"/>
  <circle class="s" cx="200" cy="58" r="4"/>
  <line class="m" x1="335" y1="164" x2="425" y2="164" stroke-width="1.4"/>
  <line class="m" x1="380" y1="136" x2="380" y2="192" stroke-width="1.4"/>
  <circle class="m" cx="380" cy="164" r="4"/>
  <line class="l" x1="490" y1="289" x2="600" y2="289" stroke-width="1.4"/>
  <line class="l" x1="545" y1="262" x2="545" y2="305" stroke-width="1.4"/>
  <circle class="l" cx="545" cy="289" r="4"/>
  <circle class="s" cx="470" cy="60" r="4"/><text class="tk" x="481" y="64">small programs</text>
  <circle class="m" cx="470" cy="80" r="4"/><text class="tk" x="481" y="84">medium</text>
  <circle class="l" cx="470" cy="100" r="4"/><text class="tk" x="481" y="104">large</text>
  <text class="cap" x="355" y="362" text-anchor="middle">Illustrative. Success and time by program size, the shape to report in place of one number.</text>
  <text class="cap" x="355" y="378" text-anchor="middle">The frontier is a bootstrap band, not a line; bars are Wilson (success) and bootstrap (time) intervals.</text>
</svg>

Wall-clock is the capability axis, not dollars, since a model's compute is negligible against a human SWE's time. The audit can't build this profile, because the run records aren't public. So the ask is the smaller one: publish the per-task, per-model results that already sit in the paper as a figure, and validate or dispute the findings against the repo.

## Per-target, all 25

The [complete read](https://github.com/kimjune01/mirrorcode-audit/blob/main/findings/06_per_target.md) gives every target a verdict and sweeps the full rejection taxonomy from the prior audits: recall, implementation-pinned render, undiscoverable entry point, self-capturing golden, scale, and the non-determinism family. The tally across all 25: 2 recall, 7 scale, 13 clean, 3 private unread.

<svg viewBox="0 0 680 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;margin:1.6em auto;display:block" role="img" aria-label="A grid of 25 cells, one per MirrorCode target, colored by verdict: 13 clean, 7 scale, 2 recall (brotlid and mailauth), and 3 private targets left unread.">
  <style>
    .c{fill:#2d7d2d} .s{fill:#c0803a} .r{fill:#c0392b} .u{fill:#b3b3b3}
    .lg{font-family:ui-monospace,Menlo,monospace;fill:#444;font-size:13px}
    .cap{font-family:ui-monospace,Menlo,monospace;fill:#666;font-size:11px}
  </style>
  <rect class="c" x="44" y="36" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="92" y="36" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="140" y="36" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="188" y="36" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="236" y="36" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="44" y="84" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="92" y="84" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="140" y="84" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="188" y="84" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="236" y="84" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="44" y="132" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="92" y="132" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="140" y="132" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="s" x="188" y="132" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="s" x="236" y="132" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="s" x="44" y="180" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="s" x="92" y="180" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="s" x="140" y="180" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="s" x="188" y="180" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="s" x="236" y="180" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="r" x="44" y="228" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="r" x="92" y="228" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="u" x="140" y="228" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="u" x="188" y="228" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="u" x="236" y="228" width="40" height="40" rx="6" fill-opacity="0.9"/>
  <rect class="c" x="320" y="44" width="14" height="14" rx="3"/><text class="lg" x="342" y="56">clean · 13</text>
  <rect class="s" x="320" y="74" width="14" height="14" rx="3"/><text class="lg" x="342" y="86">scale · 7</text>
  <rect class="r" x="320" y="104" width="14" height="14" rx="3"/><text class="lg" x="342" y="116">recall · 2 · brotlid, mailauth</text>
  <rect class="u" x="320" y="134" width="14" height="14" rx="3"/><text class="lg" x="342" y="146">private, unread · 3</text>
  <text class="cap" x="160" y="300" text-anchor="middle">Every MirrorCode target as one cell, colored by verdict.</text>
</svg> Everything else is absent in the public set or neutralized by the non-determinism screen and the selection away from reverse-engineering targets. One whole-benchmark caveat remains. Every gold output is the reference's own I/O, a self-capturing oracle with no independent contract check.

## One-sided by design

The [audit](https://github.com/kimjune01/mirrorcode-audit) is one-sided by design: a witness proves a defect, and "no witness found" is not a clearance. Every quantitative claim traces to a cited paper section, a public repo file, or a re-runnable script, with per-cell figure reads labeled as such. The recall column is verified from the graded I/O, while the memorization and solve columns are figure reads, exact only in aggregate. Corrections are welcome, and re-derivable against the receipts. MirrorCode is a good instrument for a real capability. It measures a narrower thing than its title, and the narrowing favors the headline.

*Disclosure: I applied for a role at Epoch AI, which co-produced MirrorCode. This audit uses only public artifacts and is re-runnable, so every claim traces to a cited receipt and stands or falls independent of me. My own [check 4](/how-to-audit-a-benchmark) says a producer's relationships are a conflict when the artifact is asked to be science, and that rule applies to the auditor too.*
