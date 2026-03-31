---
name: synopsis
description: File a claim into the cached synopsis document in the subject's own vocabulary. Dedupes against existing entries, files by the subject's own structure, and maintains the S (Subjective) section. Called by Intake per-claim, not as a standalone pipeline stage.
argument-hint: <translated-claim>
allowed-tools: Read, Edit, Write, Grep, Bash, Skill
---

# Synopsis: File into Cache

Dedupe and file a single claim into the synopsis document, preserving the subject's own vocabulary.

## Theory

- **SOAP note (S)**: [SOAP Notes: Soar](/soap-notes-soar) — Synopsis writes the Subjective section. The SOAP note is the cache document, growing through the pipeline. Diagnose adds O and A, Prescribe adds P.
- **Subjective = the subject's words.** S.md uses the foreign system's terminology, not framework-speak. This keeps the subjective record clean — when we present it, there is no confusion between what the system says about itself and our interpretation. The framework translation lives in the Intake cache (internal working state) and surfaces at O.md (Objective), where the observer applies the lens.

## Input

A claim from Intake:
- Original claim (quoted or paraphrased, in the system's own vocabulary, with source citation)
- Proposed framework translation (stored in Intake's cache, NOT written to S.md)
- Source pointer (URL, page, section)

## Process

1. **Read the current synopsis.** If the `soap/` directory doesn't exist yet, create it. The synopsis is `soap/S.md` — the Subjective section.
2. **Dedupe via union-find.** Check if a semantically similar claim is already filed. If so, union the two — the representative displays in the synopsis, but both wordings and both source pointers survive as members. Provenance is preserved, not overwritten. Convergent evidence = set size > 1.
3. **File by topic.** Add the claim under the system's own structural category (e.g., "Decision Cycle," "Memory Systems," "Learning Mechanisms" — whatever the subject calls it). Do NOT file by framework role. If the system doesn't have a clear category, file under "Other."
4. **Update the glossary.** If the claim introduces a new system term, add it to the glossary with a proposed framework role mapping — clearly labeled as a hypothesis, not a conclusion. The glossary is a translation table for Diagnose to consume, not a statement of fact.
5. **Write in the subject's voice.** Use the system's own terms: "elaboration," "chunking," "working memory," "impasse." Not "Perceive," "Cache," "Consolidate." S.md should read like the system describing itself. **When the subject has no word for something** (e.g., the absence of a batch learning pass), describe the observable behavior ("all learning fires within the decision cycle; no background thread exists") — do not import analyst vocabulary ("no consolidation mechanism").
6. **Flag cross-source discrepancies.** If two sources make claims about the same mechanism that differ in specifics, note the discrepancy inline (e.g., "S1 says X; S4 says Y — see #N") and add it to open_questions. Do not silently pick one.
7. **open_questions use the subject's terms.** Framework-level implications (which role a term maps to, whether a role is missing) are deferred to O.md. Open questions in S.md ask about the system's own internal tensions: "Does elaboration include operator proposal?" not "Where does the Filter/Attend boundary fall?"

## Validation (codex volley)

After Intake signals all claims are filed, Synopsis validates the complete S.md via `/codex`. This is a Filter step — it catches errors the per-claim filing process can't see.

### What codex checks

Send S.md to codex with this prompt context:
- S.md must use the SUBJECT's own vocabulary, not the analyst's framework
- Claims should have traceable provenance (section/page for papers, file/function for code)
- Glossary contains PROPOSED mappings — confidence should reflect actual certainty
- Cross-source discrepancies should be flagged, not silently resolved

### What to fix

Apply codex's findings directly:
1. **Framework leaks**: rewrite in observable behavior, not analyst terms
2. **Weak provenance**: add specific citations (function names for code, section numbers for papers)
3. **Miscalibrated confidence**: lower to medium if the term does double duty
4. **Missing discrepancies**: flag inline and add to open_questions
5. **open_questions in analyst terms**: rewrite in the subject's vocabulary

### Convergence

Run until codex returns no structural notes. If codex flags the same issue across passes, the Synopsis rules need updating — log it for skill iteration rather than patching S.md by hand.

## Output

`soap/S.md` updated in place. Claims in the subject's vocabulary, organized by the subject's own structure. Glossary with proposed (not concluded) framework mappings. Validated by codex.

## Contract

- **Precondition**: claim with source pointer from Intake
- **Postcondition**: claim is filed exactly once in the subject's own terms; source pointer preserved; glossary current with proposed mappings
- **Idempotency**: filing the same claim twice produces no change (dedupe catches it)
- **No re-entry**: a claim that has passed through the filter chain never re-enters it. Duplicate claims from later sources are caught at dedupe and merged as convergent evidence, not re-translated.
