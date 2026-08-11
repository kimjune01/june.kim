# Issue draft: SprocketLab/slop-code-bench

Filed 2026-08-11: https://github.com/SprocketLab/slop-code-bench/issues/27

Title: Pinned answer keys fail evaluation in the official image; sampled Core tests require behavior the specs do not determine

---

I'm a benchmark auditor and came across SlopCodeBench. I found some discrepancies and wanted to share some findings with you. I'm hoping that this results in an improved version.

---

AGENT:

I audited the pinned release (runner `06b5c06`, problems `ef6a9dd`) using the repository's `eval-snapshot`, first locally and then in the official `docker-python3.12-uv` image. Every claim below links to a receipt; pinned sources, scripts, and finding files are at https://github.com/kimjune01/slopcodebench-audit.

Answer keys, measured in the official image ([full sweep](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/06-gold-sweep.md)):

- `dynamic_buffer` checkpoints 2 through 4 fail their own tests (48/50, 102/104, 122/172).
- `env_manager` checkpoint 3 fails three regression tests from checkpoints 1 and 2 (184/187): the absolute-path rejections and the same-module conflict report.
- `pwd_manager` checkpoint 4 is unstable. Two independent Docker runs each failed exactly one checkpoint-2 regression test, a different test each time (212/213 both runs).

Toolchain hermeticity, measured outside the image (the official Python image ships no Node): `test_translator` grades TypeScript through unpinned `npx ts-node --esm`. All eight TypeScript checkpoints fail when `npx` resolves the current npm-latest `typescript`, which ts-node 10.x cannot load; reproduced with a pristine npm cache on the runner-pinned Node version, and pinning `typescript@5.3` makes the same command pass.

The remaining 183 pairs either evaluated clean or were cleared as environment-specific artifacts in a later arm; the sweep records each classification.

Separately, spec-test alignment ([oracle](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/08-oracle.md), [determinacy](https://github.com/kimjune01/slopcodebench-audit/blob/main/findings/09-determinacy.md)): the paper defines Core as functionality "explicitly mentioned or shown in the specification" (§2.4). The audit credited a graded value as spec-determined if any visible checkpoint spec states it, shows it in a worked example, or implies it by an explicit rule, so the criterion is wider than the paper's own. Under it, 28 of 343 Core tests in a 12-problem sample were confirmed to impose graded requirements the visible specs do not determine; one further row remains contested. Each retained row is in [core-violations.json](https://github.com/kimjune01/slopcodebench-audit/blob/main/receipts/oracle-probe/core-violations.json) with an independent refutation pass behind it, and a script in the repo recomputes the totals. The determinacy finding includes three cross-checkpoint leaks (`cfgpipe` requires the literal "duplicate" one checkpoint before the spec introduces it; `dag_execution` requires unquoted list syntax a checkpoint early; `datagate` requires the `CACHE_ENABLED` env var a checkpoint early) and direct spec-vs-test contradictions (`meshctl` asserts an exact error order the spec disclaims; the `trajectory_api` gold returns 200 on create where every spec says 201).

Requested fixes, in order of mechanical certainty: correct the four failing keys, pin `typescript` for the `test_translator` testers, investigate the `pwd_manager` instability, and review the ledger rows for reclassification (Core to Functionality) or spec amendment.

If any row is wrong, say so here or on the audit repository and I will correct and credit it.
