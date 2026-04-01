---
name: soap
description: Run the full diagnostic pipeline on a foreign system. Intake → Diagnose → Prescribe, with mandatory human gates between each step. Skipping a step is not allowed.
argument-hint: <system-name-or-url>
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, Skill, WebFetch, WebSearch
---

# SOAP: Diagnostic Pipeline

Run Intake → Diagnose → Prescribe on a foreign system. Each step produces a file. Each transition requires human judgment. The pipeline does not skip steps.

## Process

### Step 1: Intake → S.md

Run `/intake <target>`. Intake reads sources, translates vocabulary, fans out on thin coverage, files claims, and elicits human judgment on ambiguous mappings.

**Gate:** Intake includes its own elicitation. S.md is not complete until the human has answered the mapping questions. Do not proceed to Step 2 until S.md has an `## elicitation` section with oracle reliability ≥ 50%.

**Verify before advancing:**
- [ ] S.md exists with source_list, glossary, claims, open_questions
- [ ] Elicitation section present with confidence tags
- [ ] Oracle reliability ≥ 50%

---

### Step 2: Diagnose → O.md

Run `/diagnose`. Diagnose reads S.md, builds the tower table, draws architecture SVGs, substantiates mappings against code, and identifies gaps. Produces O.md.

**Gate:** Diagnose stops after writing O.md and presents checkpoint questions to the human. The human's answers determine the causal chain direction, distinguish blind spots from design choices, and identify anything missing from the tower table.

**Verify before advancing:**
- [ ] O.md exists with tower table, SVG diagrams, code evidence
- [ ] Human has answered the O→A elicitation questions

---

### Step 3: Diagnose → A.md

Diagnose writes A.md incorporating the human's answers from Step 2. Role-by-role assessment, causal chain, gap summary.

**Gate:** Present A.md to the human. Ask: "Does this assessment match your understanding? Is the root cause correctly identified?"

**Verify before advancing:**
- [ ] A.md exists with assessments, causal chain, gap summary
- [ ] Human has confirmed or corrected the assessment

---

### Step 4: Prescribe → P.md

Run `/prescribe`. Prescribe reads A.md, consults the Parts Bin, evaluates candidates, and triages by urgency (Critical / Structural / Rehabilitative).

**Gate:** Present P.md to the human. Ask: "Does the triage order match the system's actual constraints? Is the root intervention correct, or does it address a symptom?"

**Verify before advancing:**
- [ ] P.md exists with prescriptions organized by triage tier
- [ ] Dependency order and composition constraints specified
- [ ] Human has confirmed or corrected the triage

---

### Done

SOAP complete. Four files in `soap/`: S.md, O.md, A.md, P.md. Each one traces back to the previous. Every human gate is recorded in the files (elicitation in S.md, checkpoint answers in A.md, triage confirmation in P.md).

## Rules

- **No skipping.** Step N does not start until Step N-1 is verified. If the human is unavailable, the pipeline stops at the current gate.
- **No backfilling.** If Step 2 reveals that S.md is missing something, go back to Step 1 and update S.md. Do not patch O.md to compensate.
- **One question at a time** at every gate. Don't dump the full checkpoint quiz.
- **Record everything.** Every human answer goes into the relevant file. A reader should reconstruct the full decision trail from the SOAP files alone.
- **Log every skill run.** Append a one-liner to `soap/surprises.md` when each skill completes, even if nothing surprising happened. This grounds the surprises in temporal order.

  ```
  ## Run log

  - 2026-04-01 14:00 — /intake on Soar: 90 claims, 6 sources, 7 ambiguous mappings
  - 2026-04-01 14:30 — /diagnose on Soar: 5 gaps across 3 stack levels, root cause found
  - 2026-04-01 15:00 — /prescribe on Soar: 5 prescriptions, 3 triage tiers
  ```

- **Log surprises.** Append to `soap/surprises.md` whenever anything unexpected happens: a skill spec that needed changing, a mapping that broke assumptions, a codex finding that contradicted the pipeline's output, a human answer that redirected the diagnosis. Format:

  ```
  ### [step] [timestamp] — [one-line summary]
  **Expected:** what the skill/pipeline predicted
  **Found:** what actually happened
  **Action:** what changed (skill spec update, backtrack, new open question)
  ```

  Surprises are the I-frames for a future consolidation pass. The run log provides the P-frames between them. Together they reconstruct the full episode.

## Convergence

Each skill converges individually (self-check loop, hard stop at 10 passes). Codex sniffs before every human gate, fixing obvious issues so the human only Attends ambiguities. The composed pipeline converges because:

1. Each skill's postcondition matches the next skill's precondition
2. Each skill is individually convergent
3. Human gates prevent error propagation — a bad S.md gets caught at elicitation, not passed silently to Diagnose

Running `/soap` twice on the same system with the same human answers produces the same four files.

## Contract

- **Precondition**: a system to diagnose (name, URL, repo path, or reading material)
- **Postcondition**: four SOAP files, each with human-verified gates, traceable back to original sources
- **Does not**: implement fixes (that's Forge) or decide whether fixes are worth doing
- **Stability**: the pipeline is stable under composition — converged inputs produce converged outputs at every stage
