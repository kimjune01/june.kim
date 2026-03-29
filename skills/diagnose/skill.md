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

1. **Read the sources.** If given a reading list, read each linked source. If given a repo, survey the module structure.
2. **Map to roles.** For each of the six roles (Perceive, Cache, Filter, Attend, Remember, Consolidate), identify the system's corresponding component. Use the system's own terminology — don't force the framework's language where it doesn't fit.
3. **Draw the architecture.** Produce SVG diagrams mapping the system onto the six roles, recursively. Start with the top-level pipeline. Then for each component that is itself a pipeline (e.g., each memory system, each learning module), map *that* onto the six roles and draw it. Recurse as deep as the source material allows — stop when a component is atomic or opaque. Use the template style from [diagnosis-soar](/diagnosis-soar): solid boxes for strong roles, dashed for weak/missing, dim for present-but-broken. The diagrams are the diagnostic instrument — gaps that hide in prose are visible in the picture, and gaps in subpipes compound into system-level failures.
4. **Substantiate against code.** For each role mapping, grep the source for the specific mechanism. Quote the relevant code or documentation. If the role is claimed but not implemented, flag it.
5. **Identify gaps.** Which roles are missing? Which are present but broken (e.g., grows without bound, no eviction, no consolidation loop)? Which are strong?
6. **Write O (Objective).** `soap/O.md` — one section per role with SVG diagrams, code quotes, and doc references. The evidence, not the judgment.
7. **Write A (Assessment).** `soap/A.md` — role-by-role assessment (strong / weak / missing). Summary at the top naming the broken roles.

## Output

- `soap/O.md`: SVG diagrams (top-level + subpipes), code evidence, doc references
- `soap/A.md`: role assessments, summary of broken roles

## Contract

- **Precondition**: synopsis document with glossary mapping system terminology → framework roles, or access to source code
- **Postcondition**: every assessment is substantiated by a code quote or doc reference
- **Does not**: prescribe fixes (that's Prescribe) or prioritize which broken role is the root cause (that's the human checkpoint)
- **Checkpoint contract**: after Diagnose, the human is cross-examined — not "does this look right?" but "which broken role, if fixed, would improve the others?" and "is this the root cause or a symptom of something deeper?" The skills deliver evidence. The checkpoint elicits judgment.
- **Idempotency**: diagnosing the same system twice produces the same role mapping
