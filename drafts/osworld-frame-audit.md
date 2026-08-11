# OSWorld-Verified frame audit — scoping draft (pre-greenlight)

Drafted 2026-08-06 from a same-day survey. Target: `xlang-ai/OSWorld` (OSWorld-Verified is the
2025-07-28 in-place overhaul of main, 369 tasks; XLANG Lab, HKU, maintains it — HUD only hosts
runners, the benchmark is fully public). Clause: frame. This slot was "WebArena-Verified /
OSWorld-Verified" in `bench-audit-targets.md`; the survey settles it.

Nothing here is run or filed. Each item below is a separate greenlight.

## Why OSWorld-Verified and not WebArena-Verified

- **Reporting.** OSWorld-Verified is the current computer-use headline in the Anthropic, OpenAI,
  and Google cards. Original WebArena has faded from cards; WebArena-Verified (ServiceNow, Dec
  2025, 50 stars) is nobody's reported number — and auditing it means auditing ServiceNow's own
  audit. Runner-first selection says OSWorld.
- **Structure.** OSWorld's frame blindness is clean to demonstrate: each task's
  `evaluator.func` + getter reads exactly one slice of VM state
  (`desktop_env/evaluators/getters/`, `metrics/`), compares to `expected`, and reads nothing
  else. Final-state grading with a one-slice frame, the Terminal-Bench shape again but
  per-task-narrower.
- WebArena-Verified stays on the shelf with one noted lead if it ever ranks: its mutate-task
  grading matches expected network events in the captured HAR by presence, so extra destructive
  requests in the trace plausibly pass (unverified — check
  `network_event_evaluator.py` before ever claiming this).

## Prior art — the gap is specific

- **Epoch's OSWorld post** (Burnham): ~10% of tasks with wrong keys / too-strict evaluators /
  ambiguity. Grader-accuracy criticism; largely absorbed by the Verified overhaul (300+ fixes).
- **arXiv 2607.28367** (July 2026): 15.3% of FAIL verdicts wrong across OSWorld/WebArena/etc —
  entirely the false-NEGATIVE direction, manual trajectory review, no mutations.
- **AgentRewardBench** (COLM 2025): rule evaluators reject valid runs; has a per-trajectory
  side-effects annotation — acknowledges side effects matter, doesn't audit graders for
  side-effect blindness.
- **ST-WebAgentBench** (IBM): nearest neighbor — adds policy-annotated tasks and measures
  agents' completion-under-policy. It builds new tasks; it does not audit existing graders
  with gold+mutation runs.
- **Nobody has published "score 1 while wrecking unrelated state" against OSWorld-Verified.**
  Everything public attacks false negatives or agent behavior. The model-free grader-mutation
  framing is unclaimed here.

## The experiment (check 9, model-free, no agent)

No scripted golds ship (`"trajectory": "trajectories/"` is a placeholder), but none are needed:
`DesktopEnv` exposes the same in-VM `execute` channel (arbitrary shell/python) that task
`config` setup uses. So a per-task run is: setup → scripted gold via `execute` → mutation
payload (delete/corrupt user assets the task never named) → `env.evaluate()`.

1. Pick ~10 exemplar tasks across domains (os, chrome, libreoffice_calc, vlc, multi_apps) where
   a gold is scriptable in a few commands (the `check_include_exclude`-style terminal tasks
   first; file-comparison tasks second). The HF model-trajectory dataset
   (`xlangai/ubuntu_osworld_verified_trajs`, success-verified) seeds gold scripts where hand
   authoring is unclear.
2. Baseline: gold alone → expect score 1 (also a mini gold-integrity check, their check 6).
3. Mutation: gold + off-task destruction (wipe `~/Documents` decoys planted at setup, corrupt
   another app's config, `rm -rf` an unrelated project dir) → regrade.
4. **Preregistered prediction**: score 1 on every task whose getter doesn't touch the mutated
   path, i.e. approximately all of them. Witness discipline: manifest the VM state before/after
   mutation via the same `execute` channel; void runs whose mutation no-opped.
5. The per-task `possibility_of_env_change` metadata field is the tell to quote: the schema
   acknowledges environment drift and still guards none of it.

## Cost (the real gate on this one)

VM infra is the whole cost: VMware Fusion locally on the Mac, or Docker+KVM on a Linux
box/EC2 (sub-hour full runs need the AWS rig; ~10 exemplar tasks don't). Estimate a day of
stand-up + a day of runs, low tens of dollars if EC2. Everything after stand-up is model-free.
This is the most expensive of the three drafts and the only one with real setup risk.

## Census results (item 1 EXECUTED 2026-08-06)

OSWorld @ `091f5ef`. Per-task classification: `drafts/osworld_getter_census.json`.

- **270 of 369 tasks (73%) grade on exactly one pre-named slice of VM state** (231 strict
  single-path — one file, one config key, one probe value — plus 12 single-app-config-file
  tasks and 27 infeasible tasks with no getters). For all of these, any off-task mutation
  outside the slice is provably ungraded: the getter never reads it.
- The remaining 99 (52 BROAD, 39 INDIRECT, 8 MULTI-PATH) mostly read live browser state via
  CDP (chrome domain: 31 of the BROAD), and even the INDIRECT ones are usually one-key probes
  (`gsettings get`, a single `[ -f ]` test). The genuinely mutation-sensitive minority:
  terminal-scrollback tasks (2), accessibility-tree tasks, bash-history/process greps
  (multi_apps), Drive-account tasks (7), tab/history/cookie/bookmark reads.
- Every task carries `possibility_of_env_change` metadata (363 low / 4 medium / 2 high) — the
  schema names environment drift and guards none of it. The quotable tell.
- 15 exemplars picked for the gold+mutation run (8 os-domain tasks whose gold is 1-3 shell
  commands, plus calc/chrome/vlc/multi_apps file-based tasks) — list in the census JSON and
  the census notes; all have strict single-path getters.

The reading-level claim already stands on its own: 73% of the benchmark cannot see any
off-slice damage by construction. The VM run (items 2-3) upgrades "provably ungraded by
construction" to "reproduced reward 1 after wrecking state," the same upgrade WorkArena
deferred.

## Itemwise menu (updated)

| # | item | cost | status |
|---:|---|---:|---|
| 1 | Getter census over all 369 evaluator specs | ~a day, $0 | **DONE 2026-08-06** — 270/369 one-slice |
| 2 | Stand up one VM provider, run one task end-to-end (gold via `execute`, evaluate) | ~a day, ~$10s | awaiting greenlight; the only real setup risk |
| 3 | 10-15 task gold+mutation contrast with witnesses (exemplars picked) | ~a day | awaiting greenlight, after 2 |
| 4 | Post + upstream issue to xlang-ai/OSWorld, right-of-reply (Tianbao Xie, Mengqi Yuan); cure = state manifest at handoff + delta gate, same fix family as harbor#2266 | days | could ship on census alone if 2-3 stall |
| 5 | BenchRisk reconciliation under the frame mode | minutes | per campaign policy, only after #8 moves |

## Fit with the campaign

Third leg of the frame-clause series: Terminal-Bench (unasserted), Frontier-Bench
(unavailable), OSWorld (one-slice getters). Same finding family, third harness architecture,
and the first in the computer-use lane where the frame sin is what users actually fear
(an agent wrecking the desktop it was driving).
