# PR draft — UKGovernmentBEIS/inspect_ai

**Title:** Add `scope_check` solver: report or gate on out-of-scope sandbox file changes

**Branch:** `frame-check`

---

> **FILED** as draft PR UKGovernmentBEIS/inspect_ai#4462 (branch kimjune01:scope-check) on 2026-07-10.


## This PR contains:
- [x] New features

### What is the current behavior? (You can also link to an open issue here)

Closes #NNN. Inspect grades an agentic sample by what the scorer inspects at the end and asserts nothing about the rest of the sandbox state the agent touched on the way, so a run that completes its task while deleting or corrupting unrelated files scores the same as a clean one. This is the pass-to-pass / frame condition that final-state scoring omits ([SWE-bench's PASS_TO_PASS](https://arxiv.org/abs/2310.06770) is the same guarantee). Inspect's agentic evals have the fail-to-pass half and nothing playing the pass-to-pass role. The gap is measurable: a construct-validity audit of Terminal-Bench 2.1 ([writeup](https://june.kim/terminal-bench-frame), [terminal-bench#1459](https://github.com/harbor-framework/terminal-bench/issues/1459)) found 40 of 83 gold-passing tasks still score 1 after a careless deletion in their own workspace.

### What is the new behavior?

Adds `scope_check(wrapped, roots=("."), allowed=(), gate=False)`, an opt-in solver that snapshots the watched roots before and after the wrapped solver runs and records the paths changed outside an allowed footprint as a `scope_check` score.

- *Observational by default:* the delta is written to the eval log as an unscored diagnostic and the sample's own score is untouched, so nothing about existing evals or leaderboards moves. `gate=True` scores an out-of-scope change INCORRECT.
- *Footprint* is declared with git-style globs via the `allowed` argument (task-wide) or extended per sample through `metadata["scope_check"]["allowed"]`; a sample may widen the allowed set but not weaken `roots` or `gate`. Default ignores are minimal (`__pycache__`, `.pyc`, `.pyo`).
- *Snapshot* runs one Python script inside the sandbox (`lstat`, chunked SHA-256, no symlink follow, per-path errors captured rather than aborting) and diffs the two manifests.
- No changes to the runner, hooks, scorer core, or checkpointing: one new solver module (`solver/_scope_check.py`) plus a two-line export.

Design choices worth review:
- The gate *fails closed*. A snapshot error after a successful solver scores INCORRECT with an explanation rather than an unscored NaN, so the gate can't be evaded by crashing the reporter (one retry absorbs a transient hiccup first).
- The post-run snapshot never masks the wrapped solver's own exception, and it is cancellation-shielded.
- `roots` is relative to the sandbox working directory; on a bare image with no WORKDIR, watch an explicit root.

Receipt from a real Docker sandbox (mock model). The solver writes the allowed `result.txt` and deletes a planted `/work/secret.key`, and the gate catches the deletion:

```
scope_check value: I
off_footprint: {'added': [], 'modified': [], 'deleted': ['/work/secret.key']}
delta: {'added': ['/work/result.txt'], 'modified': [], 'deleted': ['/work/secret.key']}
```

### Does this PR introduce a breaking change? (What changes might users need to make in their application due to this PR?)

No. Purely additive and opt-in; nothing changes unless a task wraps a solver in `scope_check`.

### Other information:

Tests in `tests/solver/test_scope_check.py` cover the git-style globstar matcher, the manifest diff, and the solver's observational / gating / fail-closed / metadata-extension paths (sandbox stubbed), plus the receipt above as an end-to-end check.

Alternatives considered:
- *A `Hooks` implementation* rather than a solver. Rejected: a hook can attach to the log but can't change a `Score`, which gating needs, and `on_sample_start` fires once so a baseline keyed there doesn't survive sample retries. A solver wrapper runs once per attempt and produces a first-class score.
- *Reusing the restic snapshot/diff* already in `util/_restic` (checkpoint/resume). Deferred: it would couple the check to checkpoint internals and require restic present. A self-contained manifest keeps this dependency-light; a reusable restic-backed snapshot API could be a follow-up.
- *One global check in core* rather than an opt-in per-task solver. Rejected: many sandboxes have intentionally broad permitted mutations, so a single global definition of what counts as out-of-scope would misfire; the footprint belongs to the task.
- *`size`/`mtime` instead of hashing* for change detection. Rejected: mtime is noisy and misses a rewrite-in-place; the SHA-256 is worth the cost on an opt-in check.

Known limits:
- The snapshot runs `python3` inside the same sandbox as the untrusted solver, so a sufficiently privileged solver could shim the interpreter to replay the baseline. This is inherent to in-sandbox measurement; a host-side backend would be a separate proposal.
- A large watched tree can exceed the sandbox exec-output limit. That maps to a clear error, and `roots`/ignores narrow it.

Happy to adjust the API surface (argument names, whether the default ignore set belongs here, whether gating should sit behind a stricter opt-in) to whatever fits Inspect's conventions.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
