---
name: diagnose
description: Map a foreign system onto the Natural Framework's six roles. Identifies which roles are present, which are broken or missing, and substantiates each claim against source code or documentation.
argument-hint: <reading-list-or-system-path>
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, WebFetch
---

# Diagnose: Framework Role Mapping

Map a foreign system onto the Natural Framework's six roles and identify what's broken.

## Theory

- **The six roles**: [The Natural Framework](/the-natural-framework) — the mapping template. Every component maps onto Perceive, Cache, Filter, Attend, Remember, Consolidate.
- **Reference implementation**: [Diagnosis: Soar](/diagnosis-soar) — recursive mapping depth, SVG technique, and the standard of substantiation. Read this before running Diagnose on a new system.
- **SOAP note (O + A)**: [SOAP Notes: Soar](/soap-notes-soar) — Diagnose adds Objective (code evidence, SVGs) and Assessment (role evaluation) to the SOAP note started by Synopsis.

## Input

A synopsis document (output of Intake) or a direct path to the system's source code/documentation.

## Process

1. **Read the sources.** If given a synopsis (`soap/S.md`), read it including the glossary, elicitation results, and development stage metadata (`stage:`). If given a repo, survey the module structure. Respect elicitation confidence: high/medium answers are trusted; low = competing hypotheses; unsure = insufficient evidence. **Read development stage before classifying any gaps** — a PoC missing Consolidate is on-schedule, not broken.
2. **Map to roles (tower-aware).** For each of the six roles (Perceive, Cache, Filter, Attend, Remember, Consolidate), identify the system's corresponding component. **Mappings must specify stack level, not just role.** A flat "X = Remember" is insufficient — the correct label is "X = Remember @ top" or "X = Remember @ Consolidate" (meaning: Remember inside the Consolidate stack). A role can be present at one stack level and missing at another — this is how compound failures emerge. Use the system's own terminology alongside the tower-aware label.
3. **Build the tower table.** Before drawing diagrams, produce a mapping table:

   | System term | Role | Stack | Evidence | Confidence |
   |-------------|------|-------|----------|------------|
   | working memory | Cache | top | ... | high |
   | procedural memory | Remember | Consolidate | ... | low |
   | BLA | Filter | Remember | ... | high |

   Confidence inherits from elicitation where available. For new mappings (not covered by elicitation), Diagnose assigns its own confidence with rationale. The table is the primary diagnostic instrument — gaps are visible as empty cells at specific stack levels.
4. **Draw the architecture.** Produce SVG diagrams mapping the system onto the six roles, recursively. Start with the top-level pipeline. Then for each component that is itself a pipeline (e.g., each memory system, each learning module), map *that* onto the six roles and draw it. **Actively probe for towers:** for each node that receives multiple inputs and produces a structured output, ask: is this node itself a pipeline? If yes, map its sub-roles. Don't rely on noticing — force the question for every candidate node. Recurse until a component is atomic or opaque. Solid boxes for strong roles, dashed for weak/missing, dim for present-but-broken. The diagrams are the diagnostic instrument — gaps that hide in prose are visible in the picture, and gaps in subpipes compound into system-level failures.
5. **Substantiate against code.** For each role mapping, grep the source for the specific mechanism. Quote the relevant code or documentation. If the role is claimed but not implemented, flag it.
6. **Classify gaps through constraints.** Before labeling anything as broken or missing, read the development stage from S.md metadata. Then classify each empty cell in the tower table:
   - **Expected gap** — absent because the system hasn't reached this stage yet (PoC, prototype). Note it but don't diagnose it as a failure.
   - **Design choice** — deliberately omitted. The system's constraints make this role unnecessary or impossible. Note the constraint.
   - **Blind spot** — absent without justification. This is the actual diagnostic finding.

   Which roles are missing *at which stack level*? A system can have Remember at the top level (stores exist) but lack Remember @ Consolidate (no persistent store for learned parameters). It can have Filter at the top level (production conditions) but lack Filter @ Remember (no eviction policy). Gaps at lower stack levels propagate upward — a missing role inside Consolidate breaks Consolidate at the top level, even if the mechanism nominally exists.
7. **Write O (Objective).** `soap/O.md` — tower table, SVG diagrams (top-level + subpipes), code quotes, and doc references. The evidence, not the judgment.
8. **Codex sniff.** Before presenting to the human, send O.md to codex. Apply obvious improvements directly (weak code citations, missing tower table entries, SVG inconsistencies). Present only ambiguous or debatable points to the human alongside the elicitation questions. **If codex is unavailable**, try Gemini as the reviewer. If neither is available, perform a self-review pass applying the same criteria. Log which reviewer was used or skipped.
9. **Elicit assessment.** O.md is the evidence. The human interprets it. **Default to open questions** — they surface things the diagnostician didn't anticipate. Only offer multiple choice if the human asks for structure. Ask:
   - "What do you see in the tower table that surprises you — or that's missing?"
   - "Where do you think the causal chain starts?"
   - "Which gaps are deliberate design choices?"
   - "What else should I know about this system's constraints?"

   Present one question at a time. Record answers with confidence tags (high/medium/low/unsure), same as Intake elicitation.
10. **Write A (Assessment).** `soap/A.md` — role-by-role assessment at each stack level (strong / weak / missing), incorporating the human's answers from step 8. **Causal chain**: trace how gaps at lower stack levels propagate to top-level failures, with the causal direction confirmed by the human. Summary at the top naming the broken roles and the propagation path.

## Output

- `soap/O.md`: tower table, SVG diagrams (top-level + subpipes), code evidence, doc references
- `soap/A.md`: role assessments informed by human elicitation, causal chain, summary of broken roles

## Contract

- **Precondition**: synopsis document (`soap/S.md`) with glossary, elicitation results, and proposed role mappings — or direct access to source code
- **Postcondition**: every assessment is substantiated by a code quote or doc reference; every mapping specifies stack level; A.md incorporates human judgment from the O→A elicitation
- **Does not**: prescribe fixes (that's Prescribe) or prioritize which broken role is the root cause without human input
- **Gate contract**: O.md is written first and presented to the human. A.md is written only after the human has answered the elicitation questions. The elicitation is the Attend step that turns evidence into judgment. **If the human is unavailable, write O.md and stop. Do not write A.md without elicitation.**
- **Idempotency**: diagnosing the same system with the same elicitation answers produces the same O.md and A.md

## Convergence

After writing O.md, re-read S.md and O.md together. Are there glossary terms without tower table entries? Code evidence that contradicts a mapping? Gaps visible in the SVGs that aren't called out? If yes, run another pass on steps 2-7. If no, converged. Report deltas each pass. After writing A.md, same check: does the causal chain account for all gaps in O.md? **Hard stop at 10 passes** — if still changing, the skill is oscillating. Stop, report what's fluctuating, and let the human decide.
