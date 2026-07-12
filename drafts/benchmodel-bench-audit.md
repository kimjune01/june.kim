# benchmodel-bench audit — findings

Target: [Hasnake84/benchmodel-bench](https://github.com/Hasnake84/benchmodel-bench), cloned 2026-07-10 (HEAD at clone time; repo unpinned below is the point).
Method: the ten checks from [How to Audit a Benchmark](/how-to-audit-a-benchmark), run in cost order. Checks 1–8 completed with no model calls and $0. Checks 9–10 are readings; no published score exists to audit a run of.

Scope of the instrument: 41 answer-key files across 33 suites, 167 bugs total. The grader (`scorer.py`) marks a bug detected when a finding's free text contains any one of the bug's `must_mention_any` keywords as a case-insensitive substring.

## Verdicts by clause

| clause | verdict | receipt |
|---|---|---|
| docs vs repo (check 1) | **broken** | READMEs reference `apply_bugs.py`, `runner.py`, `publish_leaderboard.py`, `estimate_cost.py`, `TIERED_REVIEW_SPEC.md`, `benchmark/bug_index.json` — none shipped |
| selection (check 2) | disclosed weakness | no human baseline anywhere; README admits injected suites "barely discriminate" |
| score (check 3) | n/a as shipped | no headline number ships in-repo; leaderboard lives on benchmodel.io, outside the "re-runnable core" |
| receipts (check 4) | **broken** | 0 results files in repo; 10/10 sampled `buggy_branch` refs 404; tiered claim in top README has no artifact behind it |
| gold (check 5) | held (content), broken (pointers) | 11/11 sampled injection `find` strings match exactly once at upstream HEAD; 0/41 keys pin a commit SHA |
| oracle (check 6) | **broken** | 20 context-free boilerplate findings "detect" 107/167 bugs (64%) |
| spec (check 7) | mostly held | graded value = keyword presence, fully determined by the key; the sin is that it's *too* loosely pinned, which is the oracle finding |
| frame (check 8) | n/a by construction | grader consumes text, not environment state; the frame analog is the spam probe above |
| decay (check 9) | **broken by design** | answer keys, injections, and the exact reward vocabulary are public and unpinned |
| run (check 10) | not auditable | no run to audit; nothing reproduces a leaderboard row from shipped artifacts |

## 1. The repo documents a different repo (check 1)

The public repo is an excerpt of a private product repo, and the docs came along unedited. `suites/README.md` walks through a pipeline (`apply_bugs.py` → `runner.py` → `scorer.py` → `publish_leaderboard.py`) of which only `scorer.py` is shipped. `scorer.py`'s own docstring points at `benchmark/results/`, a smoke-test file, and a default `bug_index.json` that don't exist here; `python scorer.py` with no args exits on a missing default path. The tiered README needs `../estimate_cost.py` and a spec file two directories up. Every `suite.md` references `runner.py`.

The README's contract is "clone it, run it with your own keys, and check the numbers." For the main suites, nothing in the clone generates findings to score. The three experiment dirs (anti_cheat, tiered, chaos) do ship their runners and import cleanly from their own directories.

## 2. Receipts: the branches don't exist (checks 4, 5)

Each `bug_index.json` names a repo plus `base_branch`/`buggy_branch`, and the README says the diff is computed from them. Sampled 10 referenced buggy branches across upstream repos (django, gin, keycloak, langchain, authentik, vllm, spring-petclinic, fastapi-template, two node repos): **10/10 return 404**. The author's own fork `RouteFit-app/benchmodel-fastapi-template` carries only `benchmark/buggy` and `benchmark/buggy-v2`, while eleven suites point at eight other branches on it; `RouteFit-app/spring-petclinic` has only `main`.

The gold *content* held where the pointers failed: for django-realbugs, gin-realbugs, and starlette-realbugs (11 bugs), every injection's `find` string still occurs exactly once in the named file at upstream HEAD, so the buggy states are reconstructible from the JSON alone. But 0 of 41 keys pin a commit SHA, and every `base_branch` is a moving upstream target — the reconstruction holds today by luck, not by contract. One rebase of `django/main` past any of those hunks silently invalidates the key.

And the one experimental claim the top README makes — tiered review "cost more and caught fewer bugs than a single strong-model call" — ships with zero result files. The repo contains no scored run of anything.

## 3. The oracle credits vocabulary, and the floor is 64% (check 6)

`must_mention_any` is an any-of substring match over the finding's prose. The hints include bare English: `"None"`, `"global"`, `"permission"`, `"race"`, `"limit"`, `"await"` all appear as sufficient detection evidence in shipped keys — despite the suites README's own (good) rule that hints must be code symbols, which the older keys predate.

The probe: one findings file of 20 generic code-review boilerplate sentences ("possible race condition…", "missing None check…", "SQL injection risk…"), written with no sight of any answer key, `file: "general"`, scored with the shipped `scorer.py` against all 41 keys:

- **107/167 bugs detected (64%)** in aggregate.
- 6/6 on node-express v1 (score 55.6%), 6/6 on security-owasp v2 (44.4%), 5/6 on spring-hardmode, fastapi-hardmode, and both node-boilerplate versions.
- Positive raw score on 17/41 keys; the -2 false-positive penalty only keeps the raw score down on 1-bug suites, because +10 per detection vs -2 per miss makes diverse spam positive-EV.
- `detection_rate_pct`, `severity_breakdown`, `high_severity_missed_count`, and `security_relevant` — the leaderboard's badge metrics — take no false-positive penalty at all, so they read 64%-inflated spam as competence.

The polarity guard (endorsement phrasing doesn't count as a catch) and the distractor neutral zone are real defenses and both survived spot checks; they guard polarity, not specificity. What's missing is any requirement that a finding be *about the bug*: right file, right function, or a conjunctive keyword set. (`must_mention_any` with generic members is the exact adjective-vocabulary failure the repo's own anti-bias section warns about.)

Anti-cheat controls carry a narrower version of the same edge: trap matching is negation-aware (thoughtfully so) but not subjunctive-aware — "switching to `yaml.load` *would* allow arbitrary code execution," a correct reasoned observation, contains an unnegated trap keyword and scores as a phantom alarm.

## 4. Decay is structural (check 9)

Three compounding exposures. The answer keys, including the exact reward vocabulary, are public — any model trained after this repo can score by echoing hint words, and nothing regenerates. The realbugs suites reintroduce known CVEs, which the authors themselves flag as recall-prone (the anti_cheat module exists to measure exactly this, which is to their credit). And the unpinned base branches mean the keys decay mechanically as upstreams move, independent of any model.

## What held

The find-string integrity (11/11), the polarity guard's conservatism, the negation-aware trap scoring, the human-owned-answer-key and symbol-hint rules in the suites README, and an unusually honest limitations section that names its own construct-validity problems. The React v2 key is cited in-repo as the symbol-anchored reference style; the older keys just don't meet it.

## The fixes, sized

1. **Pin every key to a SHA** — add `base_commit` to the schema; one field, kills the decay-by-rebase class.
2. **Ship or delete** — either include `runner.py`/`apply_bugs.py` or rewrite the READMEs to describe what's actually here; publish one scored run as the receipt for the tiered claim.
3. **Conjunctive or file-gated detection** — require ≥2 hint matches or a file match for detection credit; re-run the boilerplate probe as a CI regression test (it's model-free and free).
4. **Purge generic hints** — enforce the repo's own symbol rule over the shipped keys; `"None"`, `"race"`, `"global"`, `"permission"` as sufficient evidence contradict it today.

## Rerun

```bash
git clone https://github.com/Hasnake84/benchmodel-bench && cd benchmodel-bench
# branch 404s:  gh api repos/django/django/branches/benchmark%2Freal-regression
# boilerplate probe (drafts/benchmodel-bench-audit-probe.py in june.kim):
python3 benchmodel-bench-audit-probe.py .
# expected at the audited HEAD: 107/167 detected (64%), positive score on 17/41 keys.
```
