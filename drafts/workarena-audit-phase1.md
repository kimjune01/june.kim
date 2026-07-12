# WorkArena audit — Phase 1 (reading-level receipts)

Target: ServiceNow/WorkArena @ HEAD (clone 2026-07-09). Commit of the two exploit PRs: #149 (2026-01-22), #151 (2026-02-03).

## Phase 0 (verified by hand)
- **O oracle** = 3. 18 `cheat()` + paired `validate()` across atomic (`form.py`, `list.py`, `service_catalog.py`, `knowledge.py`) and compositional tasks. Mutation/regrade interface present.
- **Ow owner** — split. WorkArena-as-merge-home ≈ 1.5–2: external PRs merge only when trivial (ollmer #20 install line, Megh-Thakkar #51 README banner, dvattk #92); substantive external fixes stall ~9–13 mo (#83/#104/#80) or close (#99). **Nearest precedent = #96 (validator-correctness fix, our exact class) open ~11 mo, stalled post-review, issue #94 shows a takeover offer.** BUT issues get answered fast (aldro61 replied to #154 in 2 days, 2026-06). BrowserGym-as-merge-home ≈ 2.5–3: many external logins merged (recursix/TLSDC/xhluca/ryanhoangt/…), amanjaiswal73892 active maintainer. → File finding as WorkArena *issue* (read reliably), fix as BrowserGym *PR* (better odds, correct home). Also note: issue #154 "[Bug]: Some Cheat methods are Broken" = our check #5 in their own tracker. No CONTRIBUTING.md in either repo.
- **H harness home** = 3. Package under `src/browsergym/` → BrowserGym/AgentLab; one gate covers WorkArena + WebArena-* + MiniWoB.
- **L leaderboard** = 2–3. README routes eval through AgentLab → HF space ServiceNow/browsergym-leaderboard (RUNNING, mod 2026-04).
- Verdict: **GO**.

## The frame gate WorkArena *does* ship (the AppWorld-class contrast)
`form.py:355-372` `monitorChangeOnFields`: init script adds a DOM `change` listener to every `input/select/textarea` whose field name is NOT in `self.protected_fields`; first off-scope change sets `window.WORKARENA_BAD_FIELD_CHANGED`. `validate()` reads it (`form.py:844-853`, `1190-1199`) and returns reward 0. **This is a real frame gate.** Its reach:
- Scope: fields on the *currently loaded form* of the *target record*.
- Mechanism: client-side DOM `change` events only.

## What the gate does NOT reach (reading-level; source-dispositive for the delete claim)
1. **Record-level collateral — no guard found in the searched source.** Grep for `collateral|snapshot|state_diff|manifest|unrelated|other record|extra record` (`--include=*.py`, excl. tests): zero matches. Supports "no such guard in the searched Python source under these terms," not "no collateral protection whatsoever" (a guard could use other terms or live outside scope). Confirmed at the runner layer: BrowserGym `env.py:545` calls `task.validate()` and returns its reward; `_task_validate` (`env.py:363-378`) only restores page/history if validate navigated — no independent DB correctness check. Teardown runs later on reset/close and cannot revise a returned reward.
2. **DeleteRecordTask.validate (`compositional/delete_record.py:166-178`) — lead finding.** Success predicate: *no row remains matching `field_name=field_value`*. It counts no other rows and compares no pre/post state. So the shipped grader **would return reward 1** on a run that deletes the target **plus N unrelated rows** (assuming the target predicate ends empty and this validator is the operative grader). *Would*, not *did* — live reproduction is a later upgrade, not required for the source-audit claim. **Uniqueness is enforced at setup**: `setup_goal` (`delete_record.py:85-88`) raises if any row already matches `field_name=field_value`, so exactly one row satisfies the target predicate at task start; collateral rows carry different field values, never matched the predicate, and their deletion is invisible to `validate()` by construction. Scope the finding to `DeleteRecordTask` and call it *one confirmed validator false-positive class / a floor of at least one affected validator*, not a prevalence estimate.
3. **EditRecordTask.validate (`form.py:1162-1258`)** + **GenericNewRecordTask.validate (`form.py:822-934`)** both carry the authors' own caveat (`form.py:826-831`, `1166-1171`): *"we check only if the expected fields have the right value. We don't check if there are extra fields."* Field monitor covers same-form fields; edits to **other records** (navigate away, edit a different ticket/user) are outside the listener's DOM and unchecked.
4. **CompositionalTask.validate (`compositional/base.py:215-262`)** validates subtasks sequentially; composite is only as frame-safe as its weakest subtask. Delete subtasks contribute no collateral check.

## Diff against the maintainers' own exploit PRs (the service)
- **#149** removes UI avenues: Personalize Form / Additional Actions / Add content / More Options buttons.
- **#151** adds MutationObservers removing right-click context menus on form + list (Configure/Export/Show Matching/Filter Out/Assign to me).
- Both harden the **field-level, same-form** avenue — they plug ways an agent reached out-of-scope *fields on the current form*. **Neither addresses record-level collateral** (deleting/editing *other* records via legitimate navigation + API). My finding is **orthogonal and additive**, not a re-report of #149/#151. The reactive avenue-by-avenue patching is itself evidence the field monitor is known-incomplete.

## Status / scope decision (codex-checked, gpt-5.6, session 019f4a35)
- Codex cloned upstream (WorkArena @ a772230, BrowserGym @ 9e779f0), confirmed the reading, and confirmed the runner adds no DB check and teardown can't revise reward.
- **Source is dispositive for the delete finding.** A live ServiceNow instance is NOT required to publish; it only upgrades "the shipped grader would return 1" → "we reproduced reward 1 in a running benchmark." Deferred, not blocking.
- **First publishable receipt = the single DeleteRecordTask over-deletion case**, scoped in title + conclusion. Edit/create collateral cases are follow-up coverage for a benchmark-wide claim, not needed for the narrow delete receipt and not worth delaying it.
- Still needs a live instance IF/WHEN upgrading: #5 (run every gold), #8 executed (append off-task deletion to the gold `cheat()`, re-run `validate()`, capture the raw reward tuple), #2 human-solvability via `human_eval/`.
- Lead framing (per June): the delete over-deletion case.
