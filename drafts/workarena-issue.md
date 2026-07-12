# Issue draft — ServiceNow/WorkArena

**Title:** `DeleteRecordTask.validate` accepts deletion of unrelated records

---

> **FILED** as ServiceNow/WorkArena#155 on 2026-07-09.


I was reading through the delete validators and hit something worth flagging. `DeleteRecordTask.validate` (`src/browsergym/workarena/tasks/compositional/delete_record.py:166`) only checks whether any row still matches `field_name=field_value`, and if none does, it returns reward 1. It never looks at the rest of the table, so a run that deletes the target record along with some unrelated rows lands on the same reward 1 as one that deleted only the target. Rows with other field values are never seen.

The uniqueness holds up, for what it's worth. `setup_goal` (`delete_record.py:85`) raises if a matching row already exists and then creates the task record, so at handoff exactly one row matches the predicate. The collateral rows an agent might also delete carry different values, so they never match the predicate, and their deletion is invisible to the validator by construction.

To be upfront, this is a read of the source rather than a live run, since I don't have a ServiceNow instance provisioned yet. So I'd phrase it as "the shipped grader would return 1 on collateral deletion" instead of "I reproduced it," and I'm glad to attach a real reward tuple once I have an instance up.

It's the record-level version of a gap the code already calls out at the field level. The create and edit validators say as much in their own comments (`form.py:826`, `form.py:1166`: "we don't check if there are extra fields"), and `monitorChangeOnFields`, including the #149 and #151 hardening, only watches the current form. None of it reaches deletions of other records.

If a fix is welcome, the direction I'd try is to snapshot the touched tables at agent handoff and check the delta at grading time, allowing the footprint the task legitimately produces. The delete task already knows its target `record_sys_id`, so "what should have changed" is right there. The open question is the allowed-delta policy, because legitimate alternative solutions and any platform-generated changes need to not trip it, so I'd keep the first cut narrow and off by default. I'm happy to send it as a PR against `AbstractServiceNowTask` so validators can opt in without per-task authoring.

Related: #96 looks like it addresses the same class of validator fix.
