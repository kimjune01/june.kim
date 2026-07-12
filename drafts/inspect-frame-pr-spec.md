# Inspect frame-check — converged PR spec (2 codex rounds, verified vs code)

Design converged with codex (GPT-5.5) across two rounds, each read against the real repo
(`~/Documents/inspect_ai`, main @ 80a342d), and every load-bearing API claim re-verified by hand.

## Architecture (settled)

A single opt-in **solver wrapper**, not a hook. Rationale, all verified in-code:
- Hooks observe but can't change a `Score`; the gate needs to.
- `on_sample_start` fires once and doesn't survive retries (retries provision a new sandbox); a
  solver runs once per attempt.
- A solver can set `state.scores["scope_check"]`, which `run.py:1508-1557` collects and logs as a
  first-class score. So no runner or hooks changes are needed.

```
scope_check(wrapped: Solver, roots=("."), allowed=(), gate=False) -> Solver
```

Baseline manifest before the wrapped solver, final manifest after (in `finally`), diff, subtract
the allowed footprint, emit `Score.unscored(metadata=report)` (observational default) or
`Score(value=CORRECT|INCORRECT, metadata=report)` (gate=True).

## Closed decisions

1. **Footprint declaration — both, metadata extends.** `roots`/`allowed`/`gate` are solver args
   (task-wide policy). Per-sample `state.metadata["scope_check"]["allowed"]` *extends* the allowed
   list, never weakens `roots`/`gate`. Reference-solution-derived footprints are computed by the
   dataset builder into `Sample.metadata`; the checker stays ignorant of reference solutions.
   Idiomatic: Inspect reads per-sample config from `state.metadata` via `.get()`.
2. **Roots + ignores — minimal, honest.** Default `roots=["."]` (the per-sample working dir;
   `sandbox().exec` resolves relative there). Default ignore is only `__pycache__`, `*.pyc`,
   `*.pyo`. Deliberately does NOT ignore build/logs/`.git`/`/tmp` — those may be the off-footprint
   writes being measured, and hiding `.git/**` would conceal hook/config/index changes. Task
   artifacts go in `allowed`, not a global ignore. No mtimes (noise; misses rewrite-in-place).
3. **Manifest — one in-sandbox Python stdlib script** via `sandbox().exec(["python3","-c",SCRIPT],
   input=json, timeout=...)`. `os.lstat` (no symlink follow), chunked SHA-256 of regular files,
   symlink targets recorded not followed, type + permission bits, excludes mtime/uid/gid, includes
   directories, fails on permission/race errors (no silent omission), one JSON doc. Handles
   spaces/newlines/UTF-8; non-UTF-8 byte paths via `surrogateescape` is the known limit. Bounded by
   the sandbox exec-output limit, acceptable for an opt-in v1 defaulting to `.`.

## Files
- `src/inspect_ai/solver/_scope_check.py` — `scope_check` + `_collect_manifest`, `_diff_manifests`,
  `_subtract_allowed`, `_sample_allowed`, `MANIFEST_SCRIPT`.
- `src/inspect_ai/solver/__init__.py` — export `scope_check`, add to `__all__`.
- `tests/solver/test_scope_check.py` — setup/file-copy excluded; allowed change; off-footprint
  add/modify/delete; observational unscored + metadata; gate correct/incorrect; spaces/unicode
  paths; retry; epochs/samples don't share baseline.

Full v1 skeleton: codex round-2 output (tool-result `bj3gevbzn.txt`, lines ~1395-1730).

## Bug-hunt ledger (fable volley, 6 rounds, converged)

Converged implementation: `scratchpad/inspect-frame-check-v5.py`. 14 issues fixed across six
independent adversarial rounds (4 → 6 → 2 → 1 → 1 → 0); matcher checked against a 16-case suite.

- R1 (self): fnmatch semantics; deleted-root abort; gate read post-run metadata; per-path abort.
- R2: `**/` couldn't match absolute-root keys (regression in R1 fix); trailing `/**` missed the dir
  node; exec output-limit slipped both guards; `finally` masked the wrapped exception.
- R3: **gate failed OPEN** when the reporter errored (must fail closed); `$`/no-DOTALL broke
  newline-in-filename matching.
- R4: `path.replace("\\","/")` corrupted legal POSIX filenames (**gate bypass**); `except
  BaseException` + await after `GeneratorExit`; fail-closed observability.
- R5: mid-segment `**` (`output**`) crossed `/` and **failed open** on the allowed list.
- R6: converged, no confirmed bugs.

## Known limits (document in the PR, don't overreach)
- The manifest runs `python3` inside the same sandbox as the (untrusted) solver, so a sufficiently
  privileged solver could shim the interpreter to replay the baseline. Inherent to in-sandbox
  measurement; a host-side snapshot backend is a later proposal.
- A large working tree can exceed the sandbox exec-output limit; mapped to a clear RuntimeError,
  and `roots`/ignores narrow it. v1 defaults to `.`.
- Fail-closed gating can flag a benign run on a transient post-run infra failure; mitigated by one
  retry + an `explanation` string, and distinguishable via `metadata["scope_check_error"]`.

## Status — IMPLEMENTED + verified in the repo (`~/Documents/inspect_ai`, branch not yet pushed)
- `src/inspect_ai/solver/_scope_check.py` (new, ~285 lines) + export in `solver/__init__.py` (+2).
- `tests/solver/test_scope_check.py` (35 tests: matcher suite, diff/subtract, solver behaviour with
  the sandbox monkeypatched — observational, gate flag, gate pass, metadata-extends, ignores,
  fail-closed, wrapped-exception re-raise).
- Gates green: `ruff format --check` clean, `ruff check` "All checks passed", `mypy` clean on the
  module, 35 tests pass. (Import from `inspect_ai.scorer._metric` not the package, to avoid a
  scorer↔solver circular import; `typing_extensions.TypedDict` per repo policy.)
- **Executed receipt** (real Docker sandbox, `scratchpad/frame_receipt/`): an agent writes the
  allowed `result.txt` and deletes a planted `/work/secret.key`; `scope_check(gate=True)` →
  `value=INCORRECT`, `off_footprint.deleted=['/work/secret.key']`. Gate catches off-task destruction.
- Wrinkle surfaced by the receipt (worth a doc note, not a code change): default `roots=["."]` is
  relative to the sandbox exec working dir; on a bare image with no WORKDIR that is `/` (scans the
  whole container). Task images normally set a WORKDIR; otherwise pass absolute `roots`.

Next: write PR prose (`inspect-frame-pr.md`) for June's inspection; file the issue
(`inspect-frame-gate-issue.md`) per CONTRIBUTING, then the PR. Nothing pushed.
