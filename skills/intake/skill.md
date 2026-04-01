---
name: intake
description: Read sources on a foreign system, translate claims into Natural Framework terminology, and stream each into Synopsis for filing. Fan-out on thin sources. Elicit human judgment on ambiguous mappings.
argument-hint: <system-name-or-url>
allowed-tools: Read, Grep, Glob, Bash, Agent, Skill, WebFetch, WebSearch
---

# Intake: Foreign System Translation

Read sources on a foreign system, translate into framework-speak, and file incrementally via Synopsis. When sources are thin, fan out parallel agents to build richer evidence before asking the human.

## Theory

- **The six roles**: [The Natural Framework](/the-natural-framework) — Intake translates foreign vocabulary into these six roles. The quality of the translation determines whether Synopsis can file mechanically and whether Diagnose has clean input.
- **Streaming architecture**: [Caret Recorder](/caret-recorder) — perceive per-item, filter per-item, clear the buffer before the next item. By the time you've finished reading, the cache is already built.
- **Tower-aware mappings**: Mappings must specify stack level, not just role. "X = Remember" is insufficient — the correct label may be "X = Remember @ Consolidate." A role can be present at one level and missing at another. Intake proposes flat mappings; Diagnose refines to tower-level. But if the evidence clearly places a term inside a specific stack during Intake, note it in the glossary rationale.

## Input

A system name, URL, paper link, or repo path. The user may also provide initial reading material.

## Process

### Phase 1: Read and file

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

Repeat across all sources. By the time Phase 1 finishes, the synopsis document is already built — in the subject's own terms.

### Phase 2: Assess source thickness

After filing all sources, assess **source thickness** per glossary term: how many independent sources provide evidence for the mapping?

- **Thick** (3+ sources converging): translation is likely correct. Ambiguity is about the term doing double duty, not about missing information.
- **Medium** (2 sources): proceed but flag for elicitation.
- **Thin** (1 source or code-only): mapping is an interpretation, not a translation. Candidate for fan-out.

Compute the thin-coverage ratio: (thin terms) / (total glossary terms).

- **≤30% thin**: skip fan-out, proceed to elicitation. The synopsis is rich enough.
- **>30% thin**: run Phase 3 before elicitation.

### Phase 3: Fan-out on thin sources

Well-documented systems skip this phase. Under-documented systems need it. The goal is to build richer evidence for thin-coverage terms so that elicitation questions are informed, not blind.

**Shared memory:** All fan-out agents share S.md as their research log. Each agent reads S.md before starting and writes findings immediately via Synopsis. If an earlier agent already filed a claim or dead end for a term, later agents see it and skip redundant searches. The synopsis *is* the dedup mechanism — no separate search budget needed.

**For each thin-coverage term, launch 3 parallel agents** (`model: "sonnet"`, `run_in_background: true`):

1. **Code agent.** Grep the source code for the mechanism. Trace call chains. Infer behavior from implementation. Cite file paths and function signatures.
   - Prompt: "Find the implementation of {system_term} in {repo}. Trace what calls it, what it calls, and when it fires. Is it synchronous or async? Does it run in a loop, on a trigger, or on a schedule? Cite file:function for every claim."

2. **Intent agent.** Read issues, PRs, commit messages, and READMEs. Infer what the developers *intended* vs. what the code does. Look for acknowledged limitations, rejected alternatives, and TODO comments.
   - Prompt: "Search {repo} issues and PRs for discussions about {system_term}. What did the developers intend? What problems have users reported? Were alternatives proposed and rejected? Cite issue/PR numbers."

3. **Pattern agent.** Check if the mechanism matches a known algorithm in the Parts Bin (`src/data/parts-bin.yml`). Read the Parts Bin grid for the relevant pipeline stage and data structure. Report matches, near-matches, and conspicuous absences.
   - Prompt: "Read the Parts Bin at src/data/parts-bin.yml. Find the cell for {stage} × {data_structure}. Does {system_term} match any listed algorithm? If not, does it match an algorithm in an adjacent cell? If the cell is empty, that's a finding — report it."

**After all agents return:**

4. **Codex filter.** For each term, collect the three agent reports. Send to codex:
   ```
   cat <<'PROMPT_EOF' | codex exec -
   Three agents investigated {system_term}. Their findings:
   [Code agent]: {summary}
   [Intent agent]: {summary}
   [Pattern agent]: {summary}

   Do they agree on what this mechanism does? Do they agree on which framework role it maps to?
   If they agree: state the consensus and confidence level.
   If they disagree: state the disagreement and which agent has stronger evidence.
   If evidence is insufficient: say so.
   PROMPT_EOF
   ```

5. **Update glossary.**
   - **All three agree**: promote term to medium confidence. No elicitation needed.
   - **Two agree, one disagrees**: keep the majority mapping, flag the dissent in the glossary rationale. Goes to elicitation with evidence for both sides.
   - **No agreement**: mark as `competing_hypotheses`. Goes to elicitation with all three perspectives presented.
   - **Insufficient evidence from all three**: mark as `insufficient_evidence` in open_questions. Still goes to elicitation, but the human knows the sources are thin.

6. **Log dead ends.** Agent findings that led nowhere are the most valuable fan-out output — they document what the sources *don't* say and prevent future investigators from retracing the same ground. For each dead end, record in S.md's `open_questions`:

   ```
   ### {system_term}: {hypothesis} — DEAD
   **Agent:** {code|intent|pattern}
   **Tried:** {what the agent looked for}
   **Found:** {what it actually found, or nothing}
   **Killed by:** {codex | contradicted by agent X | no evidence after exhaustive search}
   **Cause of death:** {one sentence — why this mapping doesn't hold}
   ```

   A well-characterized dead end is worth more than an untested hypothesis. If three agents all come back empty on a term, that's a strong signal: the system doesn't document this mechanism, which is itself a finding (undocumented = likely absent or accidental).

**Fan-out parameters:**
- k=3 agents per thin term (code, intent, pattern). More is waste for this task.
- One round only. No second fan-out cycle — if three reading strategies can't resolve it, the human needs to.
- Max 10 thin terms per fan-out batch. If the glossary has >10 thin terms, batch them and present the first batch's results before launching the second. The human may redirect after seeing early results.

### Phase 4: Elicitation (Attend — mandatory)

The agent does Perceive (read sources), Cache+Filter (translate, dedupe, file), and optionally fan-out (diverge/converge on thin sources). But mapping foreign vocabulary to framework roles is a judgment call. The agent proposes candidates; the human selects. This step is Attend — without it, the pipeline emits unattended Cache. **If the human is unavailable, the pipeline stops. There is no fallback.**

**Present one question at a time.** Don't dump the full quiz. Let the human think about each mapping before seeing the next.

#### What to quiz

1. **Ambiguous translations.** For each entry in the glossary's "ambiguous mappings" table, present the competing role assignments and ask the human to select. These are the claims where error propagates fastest to Diagnose. If fan-out resolved some ambiguities, only present the survivors.
2. **Single-source structural claims.** For each claim with no convergent evidence (only one source, and fan-out didn't help), ask the human to confirm or dispute. Single-source claims are the weakest links.
3. **Coverage.** Ask whether any system term was missed or any translation should be reversed. **This question can change downstream skill specs** — if the human identifies a structural issue with the mapping approach itself (e.g., "flat mappings are too coarse"), propagate that feedback to the relevant skill spec before proceeding. Coverage questions are not just about completeness; they're about whether the mapping resolution is sufficient.

#### How to score

Each answer gets a confidence tag from the human: **high**, **medium**, **low**, or **unsure**.

- **high** — oracle is confident. Diagnose can trust this translation.
- **medium** — oracle leans one way but could be wrong. Diagnose should note uncertainty but proceed.
- **low** — oracle is guessing. Diagnose must treat this as `competing_hypotheses` and examine the source directly.
- **unsure** — oracle has no signal. Diagnose must treat this as `insufficient_evidence`.

#### What to record

Write an `## elicitation` section to `soap/S.md` (replacing any prior elicitation section on re-run) with:
- Each question asked
- The human's answer and confidence tag
- Fan-out resolution (if any terms were pre-resolved by fan-out, note which ones and how)
- Derived oracle reliability: fraction of answers at high or medium confidence

Oracle reliability below 50% is a stop signal — the translations are too uncertain for Diagnose to proceed without re-examining sources.

## Output

1. **`soap/S.md`** — built incrementally by calling the Synopsis skill (`/synopsis`) per translated claim. Synopsis handles dedupe, filing by role, and glossary updates.
2. **Completion report** — after all sources are processed, report to the user: sources processed, claims filed, source thickness assessment, fan-out results (if triggered), ambiguous translations queued for elicitation, any sources that were inaccessible (`blocked`).
3. **Elicitation quiz** — the mandatory Attend step. Pipeline does not advance to Diagnose until the human completes the quiz.

If Synopsis is unavailable or `soap/S.md` cannot be written, Intake stops and reports the failure. Do not buffer claims in conversation context as a workaround.

## Contract

- **Postcondition**: every claim in the synopsis traces back through a translated claim to an original source; elicitation section records oracle confidence per ambiguous translation; thin-coverage terms have fan-out evidence or are flagged as insufficient
- **Does not**: evaluate claims or identify gaps (that's Diagnose)
- **Idempotency**: running Intake twice on the same sources produces the same synopsis. Elicitation section is replaced (not appended) on re-run, keyed by question content. Fan-out results are deterministic given the same sources (codex filter may vary slightly).
