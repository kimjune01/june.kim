---
variant: post-medium
title: "Auditing SlopCodeBench"
subtitle: "It measures static code-shape drift, not yet extension robustness."
tags: methodology, epistemology, coding
---

[SlopCodeBench](https://www.scbench.ai/) concludes that agents lack the design discipline iterative development demands. Its experiment establishes less: under expanding specifications, two static code-shape metrics usually rise. Neither metric is validated as extension robustness, and iteration is not isolated as the cause. [Construct receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/00-construct.md)

## The ruler misses

Structural erosion is the share of complexity concentrated in functions above a cyclomatic-complexity threshold. The paper reports its correlation with passing the next checkpoint: **−0.018**. Lines of code reaches **−0.212**. For next-checkpoint cost, erosion reaches **0.167** and LOC **0.502**.

Verbosity has a different problem. Its 137 rules were developed partly from observed agent code, then used to conclude that agent code is 2.3 times as verbose as human repositories. A ruler built partly from one population's characteristic marks will distinguish that population by construction. The comparison needs to survive on clone coverage alone, on rules developed without the evaluated agents, or under blinded human judgment. None is reported.

## Iteration is not the treatment

Every checkpoint adds requirements. Later code has undergone more edits, has more work to do, and faces a harder specification. The experiment changes all three together.

The comparison against commits from 473 unrelated Python repositories does not separate them. Those commits are a calibration panel. Nobody reimplemented the cumulative specifications from scratch.

Under SlopCodeBench's combination of repeated editing and expanding scope, its static metrics rise. “Iteration causes degradation” requires the missing counterfactual.

## The frontier was selected

The authors removed proposed problems that frontier agents could solve in one shot, then reported that no agent solved a surviving problem end to end. Saturation filtering can preserve headroom. It also conditions the result on model failure.

The paper does not report the screening models and versions, the number removed, an unfiltered comparison, or an independent human baseline. The low score is performance on a set selected partly because frontier agents failed it, not an unconditioned estimate of iterative coding ability. [Selection receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/01-selection.md)

## The spec is not the contract

At each checkpoint the agent sees one spec file, its own prior code, and nothing else. The tests stay hidden. That design is sound when the tests grade what the spec states. They don't always. In a 12-problem sample covering 65 checkpoints, 29 of 343 core tests assert exact values no visible spec states, implies by rule, or shows in an example. Core tests alone decide checkpoint success. Each of the 29 survived an adversarial pass instructed to refute it under the paper's own definition of core: "functionality explicitly mentioned or shown in the specification." [Oracle receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/08-oracle.md)

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;margin:1.6em auto;display:block" role="img" aria-label="Horizontal bars, one per sampled problem: grey bar length is the problem's core test count, red segment is the number of core tests verified to assert values no visible spec determines. Totals: 29 of 343.">
  <style>
    .lbl{font-family:ui-monospace,Menlo,monospace;fill:#555;font-size:12px}
    .tk{font-family:ui-monospace,Menlo,monospace;fill:#888;font-size:11px}
    .cap{font-family:ui-monospace,Menlo,monospace;fill:#666;font-size:11px}
    .b{fill:#b3b3b3;fill-opacity:0.55}
    .r{fill:#c0392b;fill-opacity:0.9}
  </style>
  <text class="lbl" x="198" y="20" text-anchor="end">problem</text>
  <text class="lbl" x="205" y="20">core tests, red = graded on values the spec never determines</text>
  <text class="lbl" x="198" y="40" text-anchor="end">cfgpipe</text><rect class="b" x="205" y="30" width="128.8" height="12" rx="2"/><text class="tk" x="341" y="40">0/23</text>
  <text class="lbl" x="198" y="62" text-anchor="end">dag_execution</text><rect class="b" x="205" y="52" width="112" height="12" rx="2"/><rect class="r" x="205" y="52" width="11.2" height="12" rx="2"/><text class="tk" x="325" y="62">2/20</text>
  <text class="lbl" x="198" y="84" text-anchor="end">datagate</text><rect class="b" x="205" y="74" width="347.2" height="12" rx="2"/><rect class="r" x="205" y="74" width="16.8" height="12" rx="2"/><text class="tk" x="560" y="84">3/62</text>
  <text class="lbl" x="198" y="106" text-anchor="end">dynamic_buffer</text><rect class="b" x="205" y="96" width="134.4" height="12" rx="2"/><rect class="r" x="205" y="96" width="33.6" height="12" rx="2"/><text class="tk" x="347" y="106">6/24</text>
  <text class="lbl" x="198" y="128" text-anchor="end">eve_route_planner</text><rect class="b" x="205" y="118" width="22.4" height="12" rx="2"/><rect class="r" x="205" y="118" width="5.6" height="12" rx="2"/><text class="tk" x="235" y="128">1/4</text>
  <text class="lbl" x="198" y="150" text-anchor="end">file_backup</text><rect class="b" x="205" y="140" width="22.4" height="12" rx="2"/><rect class="r" x="205" y="140" width="5.6" height="12" rx="2"/><text class="tk" x="235" y="150">1/4</text>
  <text class="lbl" x="198" y="172" text-anchor="end">meshctl</text><rect class="b" x="205" y="162" width="168" height="12" rx="2"/><rect class="r" x="205" y="162" width="11.2" height="12" rx="2"/><text class="tk" x="381" y="172">2/30</text>
  <text class="lbl" x="198" y="194" text-anchor="end">migrate_configs</text><rect class="b" x="205" y="184" width="50.4" height="12" rx="2"/><text class="tk" x="263" y="194">0/9</text>
  <text class="lbl" x="198" y="216" text-anchor="end">mocked_http</text><rect class="b" x="205" y="206" width="229.6" height="12" rx="2"/><rect class="r" x="205" y="206" width="33.6" height="12" rx="2"/><text class="tk" x="442" y="216">6/41</text>
  <text class="lbl" x="198" y="238" text-anchor="end">sheeteval</text><rect class="b" x="205" y="228" width="134.4" height="12" rx="2"/><rect class="r" x="205" y="228" width="22.4" height="12" rx="2"/><text class="tk" x="347" y="238">4/24</text>
  <text class="lbl" x="198" y="260" text-anchor="end">trajectory_api</text><rect class="b" x="205" y="250" width="184.8" height="12" rx="2"/><rect class="r" x="205" y="250" width="11.2" height="12" rx="2"/><text class="tk" x="397" y="260">2/33</text>
  <text class="lbl" x="198" y="282" text-anchor="end">xjq</text><rect class="b" x="205" y="272" width="386.4" height="12" rx="2"/><rect class="r" x="205" y="272" width="11.2" height="12" rx="2"/><text class="tk" x="599" y="282">2/69</text>
  <text class="cap" x="340" y="316" text-anchor="middle">Core tests per sampled problem. Red: verified to grade a value the agent-visible specs never state,</text>
  <text class="cap" x="340" y="332" text-anchor="middle">imply, or show. 29 of 343 total. One failing core test fails the checkpoint.</text>
</svg>

- The `trajectory_api` answer key returns 200 on create when a toolpack is active. Every visible spec says creation returns 201. The special case exists in two places: the gold and the test that grades it.
- The `dynamic_buffer` spec offers three JavaScript interface shapes and mandates a usage pattern. The hidden harness instantiates a class. An implementation of the spec's own mandatory pattern fails every JavaScript case.
- Three problems ship checkpoint-*n* tests that require conventions the spec introduces at checkpoint *n+1*. `cfgpipe` error tests demand the literal word "duplicate" one checkpoint before the spec first uses it. A `dag_execution` core test writes unquoted list syntax first shown a checkpoint later. `datagate` tests configure the cache through an environment variable the spec names a checkpoint later. An agent that implements exactly what it has been shown fails; one that guesses the next spec passes.
- The `meshctl` spec says "Vault error order is not part of the contract." A test asserts the exact order. [Determinacy receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/09-determinacy.md)

For those checkpoints the benchmark does not measure whether an agent can implement a specification. It measures whether the agent guesses unpublished author conventions, and one wrong guess fails the checkpoint.

## Nobody disclosed a red team

The paper describes coauthor review and agent-assisted refinement of ambiguous tests. That is maker QC. It does not disclose an independent team asked to break the construct, run the answer keys, mutate passing golds, or rederive the scores.

- All 196 answer keys ran through the benchmark's own harness in its own Docker image. Four are deterministically defective: `dynamic_buffer` checkpoints 2 through 4 and `env_manager` checkpoint 3. One is unstable: `pwd_manager` checkpoint 4 fails a different regression test on each run. Eight more grade TypeScript through an unpinned `npx` toolchain that resolves to a broken version today. [Gold sweep receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/06-gold-sweep.md)
- A wrapper deletes a test-unreferenced file from the passing `trajectory_api` workspace and delegates to the unchanged gold. The probe confirms the file is gone; all 373 tests still pass. [Frame receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/03-frame.md)
- No scored model workspace or per-checkpoint result is retrievable from the linked public artifacts. The paper reports GPT-5.5 at 29 of 196 strict checkpoints; the current leaderboard reports 28. Without trial receipts, that is version drift, not a proven arithmetic error. The embedded data also contains multiple rows with identical displayed configurations and different scores. [Score receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/04-score-receipts.md)

<svg viewBox="0 0 680 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:680px;margin:1.6em auto;display:block" role="img" aria-label="A grid of 196 cells, one per answer key, colored by verdict in the benchmark's own Docker image: 183 clean, 8 non-hermetic TypeScript, 4 deterministically defective, 1 unstable.">
  <style>
    .c{fill:#2d7d2d} .n{fill:#c0803a} .d{fill:#c0392b} .u{fill:#b3b3b3}
    .lg{font-family:ui-monospace,Menlo,monospace;fill:#444;font-size:13px}
    .cap{font-family:ui-monospace,Menlo,monospace;fill:#666;font-size:11px}
  </style>
  <rect class="c" x="44" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="36" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="60" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="84" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="108" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="132" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="156" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="180" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="204" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="228" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="252" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="276" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="300" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="68" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="92" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="116" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="140" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="164" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="188" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="212" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="236" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="260" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="284" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="308" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="332" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="356" y="324" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="44" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="68" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="92" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="116" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="140" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="164" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="188" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="212" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="n" x="236" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="d" x="260" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="d" x="284" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="d" x="308" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="d" x="332" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="u" x="356" y="348" width="20" height="20" rx="4" fill-opacity="0.9"/>
  <rect class="c" x="460" y="44" width="14" height="14" rx="3"/><text class="lg" x="482" y="56">clean · 183</text>
  <rect class="n" x="460" y="74" width="14" height="14" rx="3"/><text class="lg" x="482" y="86">non-hermetic · 8</text>
  <text class="cap" x="482" y="102">test_translator, unpinned npx</text>
  <rect class="d" x="460" y="122" width="14" height="14" rx="3"/><text class="lg" x="482" y="134">defective · 4</text>
  <text class="cap" x="482" y="150">dynamic_buffer 2-4, env_manager 3</text>
  <rect class="u" x="460" y="170" width="14" height="14" rx="3"/><text class="lg" x="482" y="182">unstable · 1</text>
  <text class="cap" x="482" y="198">pwd_manager 4</text>
  <text class="cap" x="340" y="388" text-anchor="middle">All 196 answer keys through the benchmark's own harness in its own Docker image, one cell each.</text>
</svg>

No independent adversarial validity audit is disclosed, and the internal process missed defects across the claim, selection, gold, oracle, spec, frame, and score clauses. [Review-process receipt.](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/05-review-process.md)

## The next experiment

At checkpoint *n*, give one agent its checkpoint *n−1* workspace. Give another an empty workspace plus the complete specification through *n*. Hold model, harness, budget, specification, and tests fixed. The difference estimates the cost of accumulated history; their shared decline estimates task growth.

Then validate erosion against an external outcome: defects in checkpoint *n+1*, maintenance time, or success by a blinded agent inheriting the code. Control for LOC. If the metric does not predict future maintenance cost, call it static code-shape drift.

Publish the sampling funnel: every candidate, exclusion, screening model, and one-shot result. Test preservation requirements, run mutation and frame-breaking probes, and verify every gold in the public harness. Release immutable benchmark versions, scored workspaces, per-checkpoint rows, and the leaderboard calculation.

Commission an independent team to attack the evaluator before release, then publish the attacks and fixes.

Until those controls exist, report *static code-shape drift under iterative specification refinement*. The next version needs a control group more than another model.

[Reproduce the audit](https://github.com/kimjune01/slopcodebench-audit): pinned sources, scripts, tests, and finding-level receipts.

*Disclosure: Claude challenged candidate findings during the audit. Its objections narrowed the claims; the receipts decide them.*
