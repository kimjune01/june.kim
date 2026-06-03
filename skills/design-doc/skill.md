---
name: design-doc
description: Read-only design phase for feature-request (PRD-shaped) tasks (DeepSWE / Harbor). Produces the design doc whose acceptance criteria become implement-spec's proxy gate. No grader during the run (test.patch is hidden until grade time), so a missed criterion is a behavior nothing tests until too late — atomize exhaustively. No edits, no external access.
argument-hint: <task-id>
allowed-tools: Read, Grep, Glob, Bash
---

# Design-doc: PRD → spec for feature tasks

You read `instruction.md` (a PRD) + the codebase, and emit a design doc whose acceptance criteria are exhaustive. There is no real gate during the run; the proxy gate implement-spec builds is only as good as this doc's criteria. A criterion you omit is an untested behavior.

## Environment

- Repo is in an offline Docker container. Reach it via the adapter helper (e.g. `box-sh '<cmd>'`); it already `cd`s to repo root — do not prepend `cd`.
- No internet, no `gh`, no `codex`, no `gh-pr`. No FAIL_TO_PASS list, no gate helper.
- Input: `instruction.md` (PRD) + the repo source. Grading tests are NOT in the working tree.

## Output

1. Design doc to **stdout**, starting with `# Design doc:` (driver captures it).
2. Append your nodes to the hypothesis graph the adapter names. Never truncate it.

## Process

### Phase 0 — Convergence read (monoidal contract for LLM skills)

LLM output is not bit-stable. The contract is **convergence under iteration** (cf. `/humanize`): each pass narrows the diff against the fixed point; the dampener is acting only on what's still inconsistent.

If a design doc for this task already exists at the conventional path (driver names it), check the doc's `prd-sha:` header:

| State | Action |
|---|---|
| existing doc, `prd-sha` matches current `sha256(instruction.md)` | **fixed point** — read the doc, confirm criteria still atomize the PRD's clauses. If no clause is uncovered and no criterion is unsupported, print `DESIGN-DOC: converged (prd-sha unchanged)` and exit. Don't regenerate stable criteria. |
| existing doc, `prd-sha` matches but verify-spec flagged a coverage hole | **dampener**: add the missing criteria; preserve all stable ones; bump session tag |
| existing doc, `prd-sha` mismatches (PRD changed) | proceed to full Phase 1+ |
| no existing doc | proceed to full Phase 1+ |

Emit at Phase 5 includes `prd-sha: <sha256 of instruction.md>` and `session: <ISO date>` in the front matter so the next run can do the convergence read. The sha is `box-sh 'sha256sum instruction.md | awk "{print \$1}"'`.

The dampener: across runs with the same PRD, the criteria list converges within 1–2 passes — coverage holes from verify-spec close, no new criteria appear (the PRD didn't change). A run with no kill report and a matching sha is a no-op.

### Phase 1 — Atomize the PRD into acceptance criteria
- Read `instruction.md` twice. Decompose into the smallest checkable requirements; one observable behavior per criterion, numbered.
- Split compound sentences. Capture edge cases, error/warning conditions, precedence rules, naming/interface requirements as their own criteria.
- For each: state the check (input → expected output / side effect / message substring).
- Mark AMBIGUOUS where the PRD underspecifies. Note your bet and its risk.

### Phase 2 — Map criteria to current code
- For each criterion: trace where the analogous behavior happens or must live.
- `grep -rn` every identifier, function, config key, interface the PRD names.
- `git log --oneline -10 -- <file>` on suspect regions (deliberate design ≠ default).
- Classify: **already satisfied** / **partially present** / **absent**. Gap = partial + absent.

### Phase 3 — Approach
- Per criterion: which function, which new branch, which interface change.
- Quote attached code (`file:line`).
- Confidence by mode: deduction (read code, unambiguous attachment) → 95-99 · induction (read-only probe) → 90-95 · abduction (inferred from PRD, not yet confirmed) → 60-85. PRD ambiguity caps at abduction.
- If PRD admits two readings, list both as alternatives; state which you'd bet on. The proxy gate cannot arbitrate — flag this.

### Phase 4 — Implementation plan (edit sites)
- For every criterion in the gap, enumerate every location that must change.
- `grep -rn "<pattern>" .` — never reconstruct from memory.
- Per site: file path, line range, criteria implemented, plain-language description.
- Check callers, subclasses, interface implementers, config/annotation parsers.

### Phase 4.5 — Combinational re-read (MANDATORY second pass)
After Phase 4, before emitting:
1. Re-read the PRD with v0 in hand.
2. Enumerate every behavior that emerges from **combinations** of rules — nesting, sequence, simultaneous application, stacking, dominance, ordering — that is NOT already a v0 criterion.
3. For each: CERTAIN consequence → add as v1 criterion (and as a runnable test for build-tools) · UNDERDETERMINED → leave to residue, document.
4. Output v1.

The first pass extracts per-sentence rules; the second surfaces interactions BETWEEN sentences. Both passes are necessary.

### Phase 5 — Emit
Print to stdout:

```markdown
# Design doc: <task-id>
<!-- prd-sha: <sha256 of instruction.md> -->
<!-- session: <ISO date> -->

## FEATURE-SHAPE (routing predicate — Hₐ₃)
<one of:
  enum       — PRD lists ≥ 2 surface elements (operators, methods, keywords, variants, formats).
               Downstream: build-tools.
  invariant  — PRD states a rule that must hold across an unstated surface ("preserve X when Y",
               "the optimizer must not Z"). The set of values the rule ranges over is in the
               codebase, not the PRD. Downstream: compose.
  mixed      — Both. Listed surface AND invariant clauses across an unstated wider surface.
               Downstream: build-tools first (on the named surface), then compose (on inferred
               axes). Both write into the same $PROXY_GATE_DIR.
>
One sentence why. If ambiguous between `enum` and `invariant`, default to `mixed` — running both
is sound; running the wrong one alone produces the F₁₆ oxvg failure mode (4 combinators covered,
6 pseudos missed) or the symmetric Hₐ₂-on-invariant inflation.

## Feature type
Classify by PURPOSE, not surface. If the feature's *job* is suppress / select / remove / simplify / optimize / validate / type-check / rank / order / canonicalize → SUBTRACTIVE, even when implemented via new methods / keywords / directives.

<one of:
  ADDITIVE — isolated new method/flag/input AND purpose is not subtractive → complete the full stated surface, extra is free
  SUBTRACTIVE/TRANSFORM/FILTER/OPTIMIZER/SELECTOR — purpose is removal/suppression/simplification/discrimination → the PRESERVED/residual set is the real spec; exhaust combinational rules (nested resolution, precedence, dominance); over-acting is graded failure
  MODIFIES-EXISTING — changes behavior for existing inputs → preserve residual first, minimal change
>
Typed-interface surface? Note it (keep signatures as narrow as the spec allows).
Every PRD-stated hard negative? List them.

## Acceptance criteria (exhaustive)
1. <atomic requirement> — check: <input → expected output / message>
2. ...
(mark AMBIGUOUS — <readings, bet>)

## Context (current behavior)
<2-4 sentences>
Supporting evidence:
- `file:line` — <quote>

## Approach (criterion → design)
- Criteria 3,4: `path/file.go` lines 10-40 — <what to add>
- ...
Confidence: <deduction/induction/abduction> — <%>

## Implementation plan (edit sites)
- `path/file.go` lines 10-20 (criteria 3,4): <change>

## Design alternatives (PRD ambiguity)
- Reading A: <design> — bet: <yes/no, why>
- Reading B: <design>

## Risks / coverage gaps
- <criteria the proxy gate is least likely to catch>
```

Do NOT include code patches. Implementation plan is spec, not diff.

## Re-entry (verify→design loop)
When the adapter passes a **VERIFY KILL REPORT**:
- Criterion's proxy test failed → implementation missed that path; re-map (Phase 2 for that criterion).
- Criterion with no test → coverage hole in *your* criteria; add it, hand back.
- Do NOT re-propose a killed design.
- If re-design converges on the same approach, print `FIXED POINT: re-design converged` — driver halts.

## REJECTED
If the PRD is unparseable, self-contradictory in a way the proxy gate cannot resolve, or matches a confirmed gold-defective / KNOWN_BAD task, emit `REJECTED — <reason>` and stop. Do not force a design.

## Rules
- Read-only. No edits.
- Atomize acceptance criteria exhaustively; completeness over falsifiability.
- Quote code on every claim about current behavior (`file:line`).
- Enumerate with `grep -rn` before asserting "the only site is X."
- Confidence tracks mode; PRD ambiguity caps at abduction.
- Append the graph with a `session: <date>` tag per entry. Readers dedupe by `(task-id, criterion-id, prd-sha)`; a re-run on the same PRD-sha must not produce a *new* criterion node, only a refresh of the existing one's confidence.
- Stdout is the handoff.

## Notes
Phase 4.5 (combinational re-read) and the Feature-type "purpose over surface" rule are corpus-validated patches (HYPOTHESIS_GRAPH.md H₁ᵦ, H₇). Iteration is a complementary lever to correct classification — they catch overlapping but non-identical subsets of the compositional-rule gap.
