# Issue draft — sierra-research/tau2-bench

**NOT FILED.** Awaiting June's greenlight. Post and issue should go out together.

*Draft 3, compressed to roughly a page. The 45-line reproduction script, the assertion census
table, the three-family sweep, and the airline contrast now live in the linked repo. What stays
inline is the one thing a maintainer can verify without leaving the issue: the one-line census.
Earlier drafts also fixed a wrong victim (C1002 holds an OVERDUE bill, which the policy permits
suspension under) and dropped a retail claim the issue's own evidence never showed.*

**Title:** Telecom reward ignores detected off-task database mutations

---

## Summary

No telecom task includes `DB` in its `reward_basis`, so a run can complete the requested task,
mutate an unrelated customer's record, have that mutation detected as `db_match: False`, and still
receive `reward: 1.0`.

Verifiable in one line, against `e5e51b3` (`main`, 2026-08-06):

```console
$ python3 -c "import json,collections; print(collections.Counter(tuple(t['evaluation_criteria']['reward_basis']) for t in json.load(open('data/tau2/domains/telecom/tasks_full.json'))))"
Counter({('ENV_ASSERTION',): 2253, ('ENV_ASSERTION', 'ACTION'): 32})
```

Airline, by contrast, is `Counter({('DB', 'COMMUNICATE'): 50})`.

**Is the exclusion intentional?** If it is, this is a documentation request and I will adjust my
writeup accordingly.

## What I ran

On `[service_issue]airplane_mode_on[PERSONA:None]`, I replayed the task's own
`evaluation_criteria.actions`, appended one `suspend_line` call against `C1001/L1001`, and graded
both through `evaluate_simulation(..., EvaluationType.ALL, ...)`:

```text
baseline                       reward=1.0, db_match=True
+ suspend_line(C1001, L1001)   reward=1.0, db_match=False
```

`C1001/L1001` appears in neither the task's gold actions nor its initialization actions. Its owner
has no `OVERDUE` bill and the line's contract runs to 2026-12-31, so neither of the two conditions
in `telecom/main_policy.md` ("Line Suspension") permits suspending it. `suspend_line` is a
`ToolType.WRITE` tool the telecom agent is given. No reward record is hand-constructed.

Script, logs, two more assertion families, and the airline contrast:
https://github.com/kimjune01/tau2-frame-audit (model-free, runs in about a minute).

## Cause

`DBCheck` is built unconditionally at `evaluator_env.py:131`, so the mutation is detected. But
`DB` is absent from telecom's basis, so `evaluator_env.py:152-157` never multiplies it into the
reward. The env assertions cannot cover the gap: six functions appear across all 2285 telecom
tasks, and each reads either the simulated device or a record passed in its own arguments, so none
can observe a write to a record the task never names.

## Possible fix

Adding `DB` to telecom's basis as strict equality may recreate the alternate-path strictness from
#329, where logging extra read calls into a hashed table failed legitimate banking trajectories.

A narrower option: reject field-level differences between the run's DB and the gold DB outside the
fields the reference trajectory itself wrote. Grading already builds the gold environment, so that
field set is free. I have not evaluated whether telecom permits legitimate alternate writes beyond
it. I can open a PR if this direction fits your intended semantics.

## Scope

The censuses are exhaustive over the shipped task set, so the property is general: no telecom
task's score can respond to a write to a record its own assertions never name. A write to a record
an assertion *does* name would be caught, which is the real boundary. Three runs across three
assertion families test that reading rather than establishing it.

I fabricated the extra call. I am not claiming that published scores are affected or that current
models do this.

Related: #384 and #224 cover the inverse case, where inaction satisfies the grader. This is the
complement, where correct completion plus one forbidden extra action also passes.
