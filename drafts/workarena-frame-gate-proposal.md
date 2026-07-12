# Proposal: opt-in record-level frame gate for WorkArena/BrowserGym

Status: draft. Harness-level fix home = BrowserGym task base or WorkArena `AbstractServiceNowTask`.
Cites: WorkArena #149, #151 (field-avenue hardening); this audit (record-level hole).

## The gap the existing gate leaves
WorkArena already ships a *field-level, same-form* frame gate (`monitorChangeOnFields`,
`form.py:355-372` → `WORKARENA_BAD_FIELD_CHANGED`). PRs #149/#151 harden the avenues into
that gate (Personalize Form / Additional Actions / context menus). None of it observes
*other records or tables*. `DeleteRecordTask.validate` accepts target + N over-deletion;
`EditRecordTask`/`GenericNewRecordTask` carry the authors' own caveat that extra fields go
unchecked; collateral edits to *other* records are outside the current form's DOM listener.

## The fix (same shape as how-to-audit §8: manifest → diff → gate on footprint)
The oracle the benchmark already ships is the frame it never wrote. WorkArena tasks already
know their footprint: `created_sysids`, `record_sys_id`, the target table, the reference
`cheat()` path. So the gate is cheap:

1. **Manifest at handoff.** In `AbstractServiceNowTask.setup`, after user creation and before
   the agent acts, snapshot a scoped fingerprint of the tables the task touches:
   `{table: {sys_id: sys_updated_on}}` for the task's `table_name` (+ any tables named by
   subtasks). Query via the existing `table_api_call`; store as `self._frame_manifest`.
2. **Diff at validate.** Add a `frame_ok(page)` helper on the base task: re-query the same
   scoped tables, compute the delta (rows deleted / created / `sys_updated_on` advanced).
3. **Gate on the reference footprint.** The allowed delta is exactly what the task's own
   `cheat()` produces — one deletion for `DeleteRecordTask`, one field-set for `EditRecordTask`,
   one insert for create. Any delta *outside* that footprint fails the episode (reward 0,
   `{"message": "Off-task state change: <table>/<sys_id>"}`), mirroring the existing
   `WORKARENA_BAD_FIELD_CHANGED` return.

## Why opt-in + observational first (audit discipline)
- Ship behind a flag (`frame_gate=False` default) so existing leaderboard numbers don't move
  silently. Land it as an *observation* — log the off-task delta without failing — so runners
  can measure how often agents trip it before anyone changes scoring. This is the same
  "come back empty" discipline: a gate that can exonerate.
- Scope the manifest to task-touched tables, not the whole instance, to keep it O(1) queries
  and avoid flagging ServiceNow's own background writes.

## Boundary / honest limits
- Per-user isolation (`create_user` + role scoping) already limits blast radius; the gate
  catches what an admin-roled agent *can* still reach across records, which is the graded
  concern for the delete/edit classes.
- Value-based target predicates: the delete manifest keys on `sys_id`, not `field_value`, so
  it's robust to the value-query aliasing noted in the audit.
- This does not claim agents *do* over-delete in practice; it closes the grader's acceptance
  of it. Prevalence is a separate, live-run question.

## Diff-vs-maintainers framing (the service)
"#149/#151 closed the ways an agent reached out-of-scope *fields on the current form*. This
closes the orthogonal layer: *records other than the target*. It's additive, opt-in, and
observational, and it reuses the footprint your tasks already track."
