---
name: intake
description: Read sources on a foreign system, translate claims into Natural Framework terminology, and stream each into Synopsis for filing. Perceive + Filter in a tight loop — the buffer clears as new bits arrive.
argument-hint: <system-name-or-url>
allowed-tools: Read, Grep, Glob, Bash, Agent, Skill, WebFetch, WebSearch
---

# Intake: Foreign System Translation

Read sources on a foreign system, translate into framework-speak, and file incrementally via Synopsis.


## Theory

- **The six roles**: [The Natural Framework](/the-natural-framework) — Intake translates foreign vocabulary into these six roles. The quality of the translation determines whether Synopsis can file mechanically and whether Diagnose has clean input.
- **Streaming architecture**: [Caret Recorder](/caret-recorder) — perceive per-item, filter per-item, clear the buffer before the next item. By the time you've finished reading, the cache is already built.

## Input

A system name, URL, paper link, or repo path. The user may also provide initial reading material.

## Process

For each source:

1. **Read.** Fetch or open the source. Extract key claims, architecture decisions, and stated limitations. For code sources, cite file paths and function/symbol names — `run_soar.cpp` is not enough; `do_one_top_level_phase()` in `Core/SoarKernel/src/decision_process/run_soar.cpp` is. **For repositories**: also scan notable PRs (merged and rejected). PRs reveal design decisions, debates, and rejected alternatives that don't survive in the final code. Use `gh pr list --state all --limit 100 --json title,body,state,labels` or search for PRs touching key subsystems. Filter for PRs that changed architecture, added/removed learning mechanisms, or debated design trade-offs. Rejected PRs are especially valuable — they document paths not taken.
2. **Translate.** For each claim, produce a translation record:
   - `source`: source ID and section/page reference
   - `original`: the claim in the system's own vocabulary (quoted or paraphrased)
   - `system_term`: the foreign term being translated (e.g., "elaboration," "chunking")
   - `mapped_roles`: one or more framework roles. If ambiguous, list all candidates with a rationale for each — do not force a single choice. Ambiguous mappings are resolved at elicitation, not here. **Ambiguity triggers**: a term participates in two functionally distinct operations (e.g., RL both updates policy *and* biases selection), or the term spans two phases of the system's own processing.
   - `rationale`: why this mapping (one sentence)
   - `confidence`: high / medium / low. **Calibration**: if the term does double duty across distinct functions, confidence cannot be high for a single-role mapping — mark medium and flag as ambiguous.

   E.g., "Soar's 'elaboration' → Cache (parallel feature extraction) with competing hypothesis Cache+Filter (operator proposal as relevance gate)."
3. **File.** Call Synopsis with the original claim (in the subject's vocabulary) and source pointer. Synopsis files it under the system's own structural categories, not framework roles. The translation record stays in Intake's cache — it informs the glossary's proposed mappings and feeds the elicitation quiz, but does not overwrite the subject's words in S.md.

Repeat across all sources. By the time Intake finishes, the synopsis document is already built — in the subject's own terms.

## Output

1. **`soap/S.md`** — built incrementally by calling the Synopsis skill (`/synopsis`) per translated claim. Synopsis handles dedupe, filing by role, and glossary updates.
2. **Completion report** — after all sources are processed, report to the user: sources processed, claims filed, ambiguous translations queued for elicitation, any sources that were inaccessible (`blocked`).
3. **Elicitation quiz** — the mandatory Attend step (see below). Pipeline does not advance to Diagnose until the human completes the quiz.

If Synopsis is unavailable or `soap/S.md` cannot be written, Intake stops and reports the failure. Do not buffer claims in conversation context as a workaround.

## Elicitation (Attend — mandatory)

The agent does Perceive (read sources) and Cache+Filter (translate, dedupe, file). But mapping foreign vocabulary to framework roles is a judgment call. The agent proposes candidates; the human selects. This step is Attend — without it, the pipeline emits unattended Cache. **If the human is unavailable, the pipeline stops. There is no fallback.**

### What to quiz

1. **Ambiguous translations.** For each entry in the glossary's "ambiguous mappings" table, present the competing role assignments and ask the human to select. These are the claims where error propagates fastest to Diagnose.
2. **Single-source structural claims.** For each claim with no convergent evidence (only one source), ask the human to confirm or dispute. Single-source claims are the weakest links.
3. **Coverage.** Ask whether any system term was missed or any translation should be reversed.

### How to score

Each answer gets a confidence tag from the human: **high**, **medium**, **low**, or **unsure**.

- **high** — oracle is confident. Diagnose can trust this translation.
- **medium** — oracle leans one way but could be wrong. Diagnose should note uncertainty but proceed.
- **low** — oracle is guessing. Diagnose must treat this as `competing_hypotheses` and examine the source directly.
- **unsure** — oracle has no signal. Diagnose must treat this as `insufficient_evidence`.

### What to record

Write an `## elicitation` section to `soap/S.md` (replacing any prior elicitation section on re-run) with:
- Each question asked
- The human's answer and confidence tag
- Derived oracle reliability: fraction of answers at high or medium confidence

Oracle reliability below 50% is a stop signal — the translations are too uncertain for Diagnose to proceed without re-examining sources.

## Contract

- **Postcondition**: every claim in the synopsis traces back through a translated claim to an original source; elicitation section records oracle confidence per ambiguous translation
- **Does not**: evaluate claims or identify gaps (that's Diagnose)
- **Idempotency**: running Intake twice on the same sources produces the same synopsis. Elicitation section is replaced (not appended) on re-run, keyed by question content.
