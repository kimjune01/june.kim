---
variant: post-medium
title: "WorkArena Built a Frame Gate and Stopped One Layer Short"
subtitle: "It guards the fields on the form in front of you, and nothing about the records you weren't asked to touch."
tags: coding, methodology, epistemology
keywords: WorkArena, BrowserGym, ServiceNow, benchmark, construct validity, frame condition, agent safety, collateral damage, final-state grading
---

## The bench that tried

Most benchmarks have no frame condition. They grade what the task asked for and read nothing else the run touched, so an agent that finishes the job and wrecks the machine scores the same as one that finishes clean. [Terminal-Bench is blind to destruction](/terminal-bench-frame) for this reason: its grader reads final container state, and a deletion in state it never asserts against is invisible.

WorkArena is more interesting, because WorkArena tried. Its form tasks ship a genuine frame guard. When a task asks the agent to fill a record, an init script (`monitorChangeOnFields`, `form.py:355`) attaches a change listener to every field the task did *not* name, and trips a flag the moment one is touched. The validator reads the flag and fails the episode: *"Some fields outside of the task scope have been changed."* That is a hand-written frame clause in a benchmark that did not have to write one, the thing Terminal-Bench lacks.

If a benchmark that consciously guards off-task state still leaks, the leak is not negligence, it is the shape of the problem. WorkArena leaks. The gate it built reaches one layer and stops.

## What the gate reaches, and where it stops

The guard is scoped to the fields on the currently loaded form of the target record. It listens to DOM `change` events on that form, for that one record. Everything outside that form is a free surface.

The clearest specimen is deletion. `DeleteRecordTask.validate` (`compositional/delete_record.py:166`) has one success predicate: no row remains matching the record it asked you to delete.

```python
def validate(self, page, chat_messages):
    record = table_api_call(
        instance=self.instance, table=self.table_name,
        params={"sysparm_query": f"{self.field_name}={self.field_value}"},
    )["result"]
    if len(record) > 0:
        return 0, False, "", {"message": "Record was not deleted."}
    return 1, True, "Nice work, thank you!", {"message": "Record was deleted successfully."}
```

It counts no other rows and compares no before-state to after. An agent that deletes the target record *and ten unrelated ones* leaves the target predicate empty, so the grader returns reward 1. The delete task cannot tell "deleted the one record I asked for" from "deleted that record and cleared the table."

The finding is airtight on the one axis where it could wobble. The query keys on a field value, not a unique ID, which would matter if two rows shared it. But setup forecloses that: `setup_goal` (`delete_record.py:85`) raises if any row already matches `field_name=field_value` before the task starts, so exactly one row satisfies the predicate at handoff. The collateral rows an agent might also delete carry different values, so they never matched the predicate, and their deletion is invisible to the validator by construction.

Deletion is the cleanest case, not the only one. The create and edit validators carry the authors' own admission, in a comment above each (`form.py:826`, `form.py:1166`):

> Caveat: we check only if the expected fields have the right value. We don't check if there are extra fields that shouldn't be there.

The field-level listener covers extra fields *on the same form*. Edits to other records, reached by navigating away to a different ticket, fall outside its DOM and outside the check. The frame guard is real, and it is local.

Reading the validator settles what it would return. A live run on a provisioned instance, appending a second deletion to the delete task's own `cheat()` and re-grading, would turn "would return reward 1" into a measured `(1.0, True, ...)`. That run is still pending, so the claim rests on the source, not on an executed grade.

## The maintainers are patching the wrong layer

This is not a hole the authors are unaware of. They are actively working it, and the work aims at the layer above the leak. The two most recent merged pull requests are both exploit patches: [#149](https://github.com/ServiceNow/WorkArena/pull/149) removes the Personalize Form and Additional Actions buttons, and [#151](https://github.com/ServiceNow/WorkArena/pull/151) adds observers that strip right-click context menus from forms and lists. Both close *avenues by which an agent reached out-of-scope fields on the current form*. They are hardening the field-level gate.

Neither touches record-level collateral. You can still delete or edit other records through ordinary navigation and the API, and the delete validator still pays for it. The maintainers are reinforcing the one layer their gate covers while the layer below stays open. The finding is orthogonal to the work already merged, not a re-report of it.

Two more signals sit in their tracker. Issue [#154](https://github.com/ServiceNow/WorkArena/issues/154), still open, is titled *"Some Cheat methods are Broken"*: the answer-key check from [the auditing checklist](/how-to-audit-a-benchmark) surfacing in the maintainers' own words. Pull request [#96](https://github.com/ServiceNow/WorkArena/pull/96) fixes a broken *validation* function, the same class of defect as this one, and has sat open since August 2025, roughly eleven months, stalled after review. A contributor offered in June 2026 to take it over after it went quiet. The maintainers answer issues within days. Substantive external fixes to their graders are another story, and anyone filing one should price the latency in.

## The fix is the one from the frame paper

The gross case has the same cheap fix as Terminal-Bench, and WorkArena is better positioned to take it, because its tasks already track the footprint the fix needs. Each task knows its target table, its `record_sys_id`, its `created_sysids`, and the path its reference `cheat()` walks. So manifest the touched tables at agent handoff, diff the final state against that manifest at validation, and gate the delta against the reference solution's own footprint. A deletion or edit the reference never made fails the episode. The oracle the benchmark already ships is the frame it never wrote down.

The gate belongs in WorkArena's `AbstractServiceNowTask`, since the collateral state lives in ServiceNow tables the harness core can't see. The pattern ports to any state-grading benchmark; the code does not. Ship it opt-in and observational first: log the off-task delta without failing the run, so the maintainers can measure how often agents trip it before anyone moves a leaderboard number. A gate that can come back empty is the one worth trusting.

## What it shows

One finding, one validator class, read from the shipped source. Deliberately narrow. It is a floor of at least one affected grader, not a prevalence estimate, scoped to `DeleteRecordTask` with the create and edit cases named as the same shape but not separately counted. The grep that found no collateral guard proves "none in the searched Python source under these terms," not "none anywhere." The reward claim is derived from the source, not yet run live.

Scoped that narrowly, it is still the control condition the [frame audit](/terminal-bench-frame) needed. WorkArena reached for a frame gate on purpose and built a working one, at the field level, on the form in front of the agent. Then it stopped. The record two clicks away is still a free surface, and the grader still pays for the destruction there. Even the bench that tried only got one layer, which is the strongest evidence I have that the frame clause is something benchmarks systematically under-write rather than something one team forgot.

## Disclosure

*The finding is filed as [WorkArena #155](https://github.com/ServiceNow/WorkArena/issues/155), with a standing right of reply, and the opt-in record-level frame gate as draft PR [#156](https://github.com/ServiceNow/WorkArena/pull/156). Publishing is held until the authors have had the chance to respond; any reply will be linked here.*
