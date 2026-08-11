# τ²-bench frame audit — scoping draft (pre-greenlight)

Drafted 2026-08-06 from a same-day repo survey (shallow clone in scratchpad, main branch).
Target: `sierra-research/tau2-bench`. Clause: frame (the grader must guard what the task never
named). Fresh clause relative to the τ-bench decay audit ([reprice-contamination](/reprice-contamination)).

Nothing here is run or filed. Each item below is a separate greenlight.

## The finding-shaped fact (reading-level, receipts in code)

Reward is the product of the components a task lists in `reward_basis`
(`src/tau2/evaluator/evaluator.py:88`). The DB component replays the agent trajectory and the
gold action script on fresh environments and compares **full-database hashes**, agent DB and
user DB both (`evaluator_env.py:118-129`, hash of the entire Pydantic `model_dump()`). So the
frame verdict splits by domain:

- **Airline (50 of 50), retail (114 of 114), banking_knowledge (88 of 97): frame guarded.**
  `reward_basis` includes DB, and any off-task mutation that touches a persisted field flips
  the hash → reward 0. An audit here comes back empty, which is the exonerating half.
  *Correction (codex sniff, 2026-08-06): banking is not categorical. 9 of its 97 tasks are
  `[ACTION]` with no DB, so they sit in the same position telecom does. The README table had
  the count right; this line said "by construction" and was wrong.*
- **Telecom: frame OPEN.** 2253 of 2285 tasks grade on `[ENV_ASSERTION]` alone (32 add
  ACTION); **DB is not in the basis at all.** Reward gates only on ~6 named assertion
  functions (`assert_can_send_mms`, `assert_mobile_data_status`, … in
  `telecom/user_tools.py:1093-1149`, `tools.py:724-758`). An agent that satisfies the
  assertions while also suspending another line or editing unasserted billing fields scores 1.
- **Telecom is the split with its own leaderboard.** ([Artificial Analysis](https://artificialanalysis.ai/evaluations/tau2-bench),
  verified 2026-08-06, top scores >99%.) The "model cards report Telecom pass^k" version of this
  came from a research subagent and was never verified; do not reuse it. The one
  domain where the frame is unguarded is the one whose number gets quoted.

Supporting structure: `ActionEvaluator` is a subset check (extra agent calls never penalized),
`CommunicateEvaluator` auto-passes on an empty list (`evaluator_communicate.py:28`), gold-replay
failures only warn (`evaluator_env.py:112` — a broken gold silently moves the target state).

## Prior art — what's claimed and what's open

- **#224** (open, Salesforce researcher, maintainer-engaged): 22/50 airline tasks need no DB
  write; docs PR #314 shipped in response. Inaction-adjacent, airline only.
- **#384** (open, 2026-07): systematic — empty criteria auto-pass, criteria written but not in
  basis, 23 airline refusal tasks scored on "DB unchanged" alone. **This is the
  inaction-scores-1 direction.** The off-task-write direction on telecom appears unclaimed.
- v1.0.1 (2026-07-22) fixed the opposite failure in banking (full-hash so strict that benign
  reads zeroed reward, #329) — Sierra treats hash semantics as live surface and re-grades the
  leaderboard on grading fixes. **They engage**: #224 milestoned and answered, #329/#402 fixed,
  external docs PR merged. Best responsiveness profile of any target in the portfolio.
- Toloka blog names the policy-violation flavor (score 1 while breaking policy that doesn't
  touch DB state) without the DB-write mechanism.

Scope discipline: cite #384 and #224 as siblings, claim only the telecom off-task-write class,
report a floor.

## The experiment (check 9, model-free)

Gold action scripts ship per task (`evaluation_criteria.actions`) and grading replays them
model-free via `Environment.make_tool_call`, so the mutation audit runs without any model:

1. Replay a telecom task's gold script → baseline reward (expect 1.0).
2. Replay gold + one appended off-task write (suspend an unrelated line / modify an unasserted
   field on another customer) → regrade.
3. **Preregistered prediction**: telecom still 1.0; the same injection on airline/retail/banking
   → 0.0. The contrast is the finding AND the exoneration in one table.
4. Witness discipline per the checklist: record DB state before/after injection; void any run
   whose injected write no-opped (telecom user_db vs agent db routing needs verification).

## Artifact

[kimjune01/tau2-frame-audit](https://github.com/kimjune01/tau2-frame-audit), created 2026-08-06,
**PUBLIC** as of 2026-08-06, five commits, all pushed. Copyleft split by file type: prose,
data, and `results/` under CC BY-SA 4.0 (matching the prior audit repos); `scripts/` under
GPL-3.0-or-later, since CC licenses are not meant for software and the probes exist to be run
and modified. Local clone `~/Documents/tau2-frame-audit`.
Layout follows frontier-bench-audit: README (provenance / mechanism / census / runs / limits /
cure), CLAIMS.md (claim, command, receipt, falsifier), REPRODUCE.md (three commands, no model),
PREDICTIONS.md, `scripts/`, `results/`.
GitHub shows no detected license (the dual LICENSE isn't a recognized template), same as the
other audit repos. Not yet tagged or given a DOI.

## Codex sniff (2026-08-06) and what changed

Sent the repo to codex. Bottom line back: *the mechanical finding is real; the audit currently
overstates what it means.* Six findings; acted on five, plus two of its "strengthen" items.

**Acted on.**
1. *Probes bypassed the top-level grader.* Real defect, verified: `evaluate_simulation`
   (`evaluator/evaluator.py:88`) checks termination and combines components; my probes called
   the ENV component evaluator directly. Fixed by re-running through
   `evaluate_simulation(EvaluationType.ALL)` — **telecom result unchanged**, and the airline
   control turned out weaker there (below).
2. *"Telecom grades no task on database state" conflates DB-the-component with state.* True;
   `ENV_ASSERTION`s do read state. Retitled C1 to the configuration claim it actually is.
3. *The frame criterion is imposed, not advertised.* This was the strongest note and produced
   the best fix: the telecom policy permits suspending a line for exactly two reasons (overdue
   bill, expired contract), and the repo README says the policy is one "the agent must follow."
   So the injection is a **policy violation by the benchmark's own rule**, not just an unmet
   criterion of mine. Re-picked the victim to `C1001/L1001` (no overdue bill, contract to
   2026-12-31) to make that airtight — the original `C1002` victim had a bill flagged OVERDUE,
   which arguably *permits* suspension. That would have been a real hole in the argument.
4. *One task, one injection reads as cherry-picked.* Added a sweep across distinct assertion
   families: 3 tasks scored, all keep 1.0; 3 skipped for want of a policy-clean off-task victim
   and reported as skipped.
5. *Cure under-specified at record granularity.* Right — record-level scoping forgives
   corruption of other fields on a touched record. Now specified at field granularity.

**Declined.** The agent-triage preamble (house convention across the audit repos), the portfolio
language in *this* draft (it is the campaign doc, not the report), and the full retreat on
"computes and discards" — reframed rather than cut, since the point that survives is that the
comparison is *already computed*, so the fix needs no new measurement.

**Also softened:** "telecom is what labs headline" now carries a note that I did not census the
model cards.

## Receipts (items 1 and 3 EXECUTED 2026-08-06)

Repo @ `e5e51b3` (main, 2026-08-06), tau2 1.0.1. All grading now goes through
`evaluate_simulation(EvaluationType.ALL)`, the top-level entry point. Model-free: trajectories
are built by executing tool calls via `Environment.get_response`, the same path the grader's
replay re-executes, wrapped in a `SimulationRun` terminating `AGENT_STOP`.

**Telecom sweep** — 3 tasks across distinct assertion families, victim `C1001/L1001` (off-task
by argument scan, and policy-clean: no overdue bill, contract to 2026-12-31):

| assertions | baseline | + off-task suspension |
|---|---:|---:|
| `assert_no_overdue_bill`, `assert_service_status` | 1.0 | **1.0** (db_match False) |
| `assert_service_status` | 1.0 | **1.0** (db_match False) |
| `assert_can_send_mms` | 1.0 | **1.0** (db_match False) |

3 more families skipped for want of a policy-clean off-task victim (the shipped DB has exactly
one customer with no overdue bill, and those tasks involve them), reported as skipped, never
counted as passes.

The load-bearing addition is the **policy** reading: `telecom/main_policy.md` permits suspending
a line for exactly two reasons (overdue bill, expired contract), and the repo README calls the
policy something "the agent must follow." Neither reason applies to the victim, so this is a
violated obligation the benchmark states, not a criterion I brought.

The DB comparison is computed on every telecom run and reported as a diagnostic
(`evaluator_env.py:131` builds DBCheck unconditionally; `:152-157` multiplies in only
basis-named components). Framing it as "thrown away" implies an accident; it is configured
exclusion. What survives is more useful anyway: the measurement the fix needs already runs.

**Airline control** — task 7, `reward_basis=[DB, COMMUNICATE]`. At the component level, 1.0 →
0.0. At the top level, **0.0 both ways**: a scripted trajectory has no dialogue, so COMMUNICATE
scores 0 regardless, and only the DB component discriminates (1.0 → 0.0). A model-free probe
cannot produce a passing airline run. Stated as a bounded control in the repo rather than
quietly citing the component number.

All three predictions held. The audit is live.

## Itemwise menu (updated)

| # | item | cost | status |
|---:|---|---:|---|
| 1 | Telecom gold + injected write receipt | hours, $0 | **DONE 2026-08-06** — 3 assertion families, all 1.0 |
| 3 | Cross-domain contrast | hours | **DONE (airline)**, bounded at top level; retail/banking repeat mechanical if wanted |
| 2 | Census the exposure: per assertion function, DB surface pinned vs mutable surface ignored; count telecom tasks by assertion set | ~a day | next; turns 3 receipts into a floor. Also the answer to codex's open note that C1 is configuration, not observation |
| 2b | Widen the victim pool: the shipped DB has one policy-clean customer, which forces 3 skips. A task-local victim (create then suspend a line) would remove the constraint | hours | optional; would let the sweep cover every family |
| 4 | Post: telecom-scoped, #384/#224 as siblings, cure named (put DB back in telecom reward_basis behind an allowed-delta footprint derived from the gold replay — the gold env is already built at grading time, so the expected delta is free) | days | awaiting greenlight |
| 5 | Upstream issue + right-of-reply to Sierra | hours | awaiting greenlight |
| 6 | BenchRisk reconciliation | minutes | only after #8 moves |

## Why this ranks despite the discouragement

Of the three targets this is the only *audit-shaped* one where the maker demonstrably engages
(fixed two external grading reports in a point release and re-graded the leaderboard). The
finding lands on the exact number labs quote. And the cost of the dispositive receipt is hours,
model-free, before any commitment to a post.
