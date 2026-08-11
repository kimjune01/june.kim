# Inspect validation API — scoping draft (pre-greenlight)

Drafted 2026-08-06 from a same-day repo survey. Target: `UKGovernmentBEIS/inspect_ai` (and the
inspect_evals register). The deliverable from `bench-audit-targets.md` rank 1: an eval-author
validation API (oracle execution, scorer determinism/totality, answer-key/dataset integrity,
CLI preflight without a model run). Checks 6–8 of
[how-to-audit-a-benchmark](/how-to-audit-a-benchmark) turned into a primitive.

Nothing here is filed. Each item below is a separate greenlight.

## Standing context (what's already in flight there)

- **Issue #4461** (frame gate, filed 2026-07-10): still OPEN, **unlabeled** — neither `accepted`
  nor `deferred`. Their CONTRIBUTING promises triage within ~7 days; it has been 27.
- **Draft PR #4462** (`scope_check`, implemented + receipted): OPEN, zero maintainer response.
  Their stale bot closes non-draft PRs at 60 days of inactivity; drafts appear exempt, verify
  before converting.
- **HarperZ9** commented on #4461 (2026-07-17) offering independent validation fixtures. Account
  created 2016, 81 followers, coherent accountability-tooling bio — reads human, unlike
  koriyoshi2041. Unanswered. June to judge before any reply.

## What changed since the July assessment (survey 2026-08-06)

The repo is more active than ever (209 PRs merged in 30 days, weekly releases, 168 open issues
after aggressive triage) but the contribution surface hardened:

1. **PR gate.** New contributors (no prior merged PR) must start from an issue a maintainer
   labeled `accepted`; unlinked PRs are auto-closed by `.github/scripts/pr_gate.py`. PRs against
   `deferred` issues auto-close regardless of tier. Established contributors (≥1 merged
   non-trivial PR) may open direct PRs, max 4.
2. **Extensions redirect.** CONTRIBUTING explicitly pushes scorers, tools, and tooling additions
   out of core to the extensions listing (inspect.aisi.org.uk/extensions.html). A validation API
   pitched as core will likely be triaged "build it as an extension."
3. **AI-disclosure requirement.** AI-assisted PRs need an "Agent review disclosure" section and
   per-line understanding (their #4712).
4. **inspect_evals no longer accepts eval code.** New evals go through a bot-driven "Inspect
   Evals Register" (issue + commit-pinned source; automated schema checks plus an *agentic*
   review that statically verifies a `@task` exists, imports resolve, description matches).
   That runnability check is a static, weaker version of this validation API — the demand
   signal exists in their own pipeline, the executable tooling doesn't.

Consequence: **a cold core-feature PR is dead on arrival.** Two viable paths, not exclusive:

- **Path A — extension package** (`inspect-validate` or similar): hooks API + registry
  introspection are first-class (`src/inspect_ai/hooks/_hooks.py`, entry-point registration),
  so the whole preflight can ship with zero core changes, then be listed in their extensions
  index. No permission needed from AISI to exist; adoption is the risk.
- **Path B — accepted-issue flow into core**: file (or attach to) an issue, wait for the
  `accepted` label, then PR. Slower, gated on triage that is currently demonstrably behind,
  but lands where METR (time-horizon tasks, Hawk), Epoch (Benchmarking Hub), and AISI all run.

Adjacent open issues to attach to rather than duplicate: #3770 (verification taxonomy on
`@scorer`, unlabeled), #4567 (normalized scorer failure policy, **accepted**, maintainer-owned),
#4695 (warn on silent self-grading, **accepted** + good-first-issue), #4136 (unseeded
model-graded scorers), #4206 (eval-reliability toolkit), #4696 (grade-pattern accepts 'P' when
partial_credit off, accepted).

## The primitive (phase 1 scope, unchanged in substance)

A preflight that runs over an Inspect task **without a model**:

1. **Oracle execution** — run the reference solution (scripted solver or `mockllm/model` with
   canned outputs) through the task's own scorer; a task whose gold can't pass can't anchor a
   verdict. Check 6, the highest-yield dollar.
2. **Scorer determinism/totality** — score the same transcript twice (and across `inspect
   score` re-scoring, their #679 shows sandbox-dependent scorers break there); flag unseeded
   model-graded scorers (#4136) and partial-credit pattern leaks (#4696).
3. **Answer-key/dataset integrity** — sample-ID uniqueness, target-field presence/type, choices
   consistency for multiple-choice, glob'd file targets exist.
4. **CLI preflight** — `inspect-validate <task>` running 1–3 plus import/construction smoke,
   suitable for eval-repo CI. (Core has no `--dry-run`; `inspect list tasks` is import-smoke
   only.)

The frame gate (#4461/#4462) becomes check 5 of the same package if core placement stalls.

## Itemwise menu (greenlight each separately)

| # | item | cost | risk | blocked by |
|---:|---|---|---|---|
| 1 | Build Path A: `inspect-validate` extension package implementing checks 1–4, receipted against 2–3 real evals from inspect_evals (find one failing gold in the wild = the demo) | days | adoption, not merge | nothing |
| 2 | Submit the package to their extensions listing + one issue proposing the preflight pattern, linking receipts | hours | triage silence | 1 |
| 3 | Establish contributor standing cheaply: take an `accepted` good-first-issue (#4695 warn-on-silent-self-grading is squarely in the validation lane) and land one small PR | ~a day | low | nothing |
| 4 | Attach the scorer-determinism piece to maintainer-owned accepted issue #4567 as a comment with a concrete proposal, not a new issue | hours | scope capture by maintainer | nothing |
| 5 | Nudge #4461: one comment noting the 7-day triage promise at 27 days, neutral tone, no follow-up after | minutes | reads as pushy; violates let-PRs-rot unless June counts a broken triage SLA as inbound-adjacent | June's call |
| 6 | Reply to HarperZ9 accepting the fixture offer (after June verifies the account) | minutes | engaging a farmer | June's call |

Recommended order if all greenlit: 3 (standing) → 1 (package + receipts) → 2 + 4 (surface it).
Items 5–6 are judgment calls with the policy leaning against 5.

## Why this is still rank 1

METR migrated off Vivaria onto Inspect (time-horizon suite, 228 tasks; sjawhar is on Inspect's
qualified-contributor list), Epoch's Benchmarking Hub is built on it, AISI runs it. One accepted
primitive — or one adopted extension — touches every eval those three run. The register's
agentic runnability check proves they already want a weak form of this; the pitch is executable
checks where they have static ones.
