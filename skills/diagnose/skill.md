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

1. **Read the sources.** If given a synopsis (`soap/S.md`), read it including the glossary and elicitation results. If given a repo, survey the module structure. Respect elicitation confidence: high/medium answers are trusted; low = competing hypotheses; unsure = insufficient evidence.
2. **Map to roles (tower-aware).** For each of the six roles (Perceive, Cache, Filter, Attend, Remember, Consolidate), identify the system's corresponding component. **Mappings must specify stack level, not just role.** A flat "X = Remember" is insufficient — the correct label is "X = Remember @ top" or "X = Remember @ Consolidate" (meaning: Remember inside the Consolidate stack). A role can be present at one stack level and missing at another — this is how compound failures emerge. Use the system's own terminology alongside the tower-aware label.
3. **Build the tower table.** Before drawing diagrams, produce a mapping table:

   | System term | Role | Stack | Evidence | Confidence |
   |-------------|------|-------|----------|------------|
   | working memory | Cache | top | ... | high |
   | procedural memory | Remember | Consolidate | ... | low |
   | BLA | Filter | Remember | ... | high |

   Confidence inherits from elicitation where available. For new mappings (not covered by elicitation), Diagnose assigns its own confidence with rationale. The table is the primary diagnostic instrument — gaps are visible as empty cells at specific stack levels.
4. **Draw the architecture.** Produce SVG diagrams mapping the system onto the six roles, recursively. Start with the top-level pipeline. Then for each component that is itself a pipeline (e.g., each memory system, each learning module), map *that* onto the six roles and draw it. Recurse as deep as the source material allows — stop when a component is atomic or opaque. Solid boxes for strong roles, dashed for weak/missing, dim for present-but-broken. The diagrams are the diagnostic instrument — gaps that hide in prose are visible in the picture, and gaps in subpipes compound into system-level failures.
5. **Substantiate against code.** For each role mapping, grep the source for the specific mechanism. Quote the relevant code or documentation. If the role is claimed but not implemented, flag it.
6. **Identify gaps (tower-aware).** Which roles are missing *at which stack level*? A system can have Remember at the top level (stores exist) but lack Remember @ Consolidate (no persistent store for learned parameters). It can have Filter at the top level (production conditions) but lack Filter @ Remember (no eviction policy). Gaps at lower stack levels propagate upward — a missing role inside Consolidate breaks Consolidate at the top level, even if the mechanism nominally exists.
7. **Write O (Objective).** `soap/O.md` — tower table, SVG diagrams (top-level + subpipes), code quotes, and doc references. The evidence, not the judgment.
8. **Write A (Assessment).** `soap/A.md` — role-by-role assessment at each stack level (strong / weak / missing). **Causal chain**: trace how gaps at lower stack levels propagate to top-level failures. Summary at the top naming the broken roles and the propagation path.

## Output

- `soap/O.md`: SVG diagrams (top-level + subpipes), code evidence, doc references
- `soap/A.md`: role assessments, summary of broken roles

## Contract

- **Precondition**: synopsis document (`soap/S.md`) with glossary, elicitation results, and proposed role mappings — or direct access to source code
- **Postcondition**: every assessment is substantiated by a code quote or doc reference; every mapping specifies stack level
- **Does not**: prescribe fixes (that's Prescribe) or prioritize which broken role is the root cause (that's the human checkpoint)
- **Checkpoint contract**: after Diagnose, the human is cross-examined — not "does this look right?" but "which gap at which stack level, if filled, would unblock the others?" and "does the causal chain match your understanding of the system's actual failure mode?" The skills deliver evidence. The checkpoint elicits judgment.
- **Idempotency**: diagnosing the same system twice produces the same role mapping
