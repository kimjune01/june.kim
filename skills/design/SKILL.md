---
name: design
description: Design review against the grimoire. Lints UI code, screenshots, or URLs for accessibility, state completeness, spacing, color, transitions, conveyance, and platform conventions.
argument-hint: <target> [--profile web-app|game-ui|component|marketing] [--focus principle1,principle2]
allowed-tools: Read, Glob, Grep, Bash, Edit, WebFetch, Agent
---

# Design Review

Lint → Fix → Re-lint → converge. No human checkpoint between steps for violations and risks. Suggestions are reported but not auto-fixed.

## Process

Lint and re-lint fan out to fresh opus subagents — one per principle, in parallel. Fix and converge stay in the parent. A single long-running opus instance grows overconfident after nailing the first few principles and skims the rest; fresh contexts force rigor on each principle independently. The parent is the only continuity across passes.

**Subagent contract (used in steps 1 and 3):**
- One Agent per principle in the profile's review order, spawned in parallel
- `subagent_type: "general-purpose"`, `model: "opus"`
- Prompt carries: target identifier (path/URL/screenshot), principle name, instruction to read only `references/{principle}.md`, the evidence rules, and the finding format
- Subagent returns findings only. Never fixes.
- Parent consolidates, dedupes cross-principle duplicates (keep the one whose reference file matched best), preserves format

### 1. Lint

**Determine target type.**
- File path → read source code, grep for patterns
- URL → fetch and inspect rendered HTML/CSS
- Screenshot → read the image, describe what you see
- Component name → find it in the codebase, read it and its styles
- Directory → audit the project holistically

**Determine profile.** If not specified, infer from context:
- `web-app` (default) — full pass
- `component` — skip transitions, conventions; focus on states, spacing, a11y
- `game-ui` — conveyance first, a11y later
- `marketing` — skip states, focus on typography, color, spacing

**Fan out.** Spawn one opus subagent per principle in the profile's review order, per the subagent contract above. Parent does not read reference files itself — each subagent loads its own.

**Evidence rules (passed to each subagent).** Before making any claim, inspect the target:
- Source code: grep for state handling, spacing values, color values, ARIA attributes, transition/animation CSS, hardcoded pixels
- Screenshots: describe layout, grouping, contrast, hierarchy, state shown
- URLs: fetch, inspect DOM structure, check contrast, find interactive elements

**Produce findings.** Three classes:

**Violations** — objective or near-objective. Evidence is clear.
- Insufficient contrast ratio
- Missing focus indicators
- Unlabeled interactive elements (no alt, no aria-label)
- Heading order skipped
- Touch target below 48x48dp

**Risks** — likely problems inferred from evidence.
- Form with async submit but no loading/error/success state found
- Hardcoded color values outside a token system
- Ad hoc spacing values (magic numbers, not from a scale)
- No transition between major state changes
- Layout shift risk from dynamic content

**Suggestions** — taste-grounded improvements tied to a principle.
- Primary and secondary actions compete visually
- Information density could benefit from progressive disclosure
- Transition metaphor is inconsistent across the flow
- Empty state lacks guidance on how to start

**Format each finding:**
```
[VIOLATION|RISK|SUGGESTION] Principle: {name}
Evidence: {what you observed}
Why: {what breaks or degrades}
Fix: {specific recommendation}
```

### 2. Fix

Apply fixes for all violations and risks directly. No human checkpoint.

- Violations: fix immediately. Missing aria-label, broken heading order, hardcoded colors outside tokens, missing focus styles — these are mechanical.
- Risks: fix with the specific recommendation from the finding. Missing loading state → add one. Magic spacing → replace with token. No transition → add the simplest one that fits the metaphor.
- Suggestions: report only. These require human judgment. Do not auto-fix.

If a fix requires a design decision the references don't resolve (e.g., which transition metaphor to pick, which color role to assign), halt and ask the user. Don't guess.

### 3. Re-lint

Re-spawn fresh opus subagents per the contract — same profile, same principles, same target. Not the same instances: the previous subagents saw their own findings and are biased toward confirming their prior work. Every pass starts cold.

- Violations and risks from pass 1 should be gone. If any survive, the fix was incomplete — fix again.
- New violations or risks from the fixes themselves → fix those too.
- Suggestions may persist. That's the non-zero floor.

### 4. Converge

If pass 2 is clean (no new violations or risks), report the final state:
- What was fixed (count by class)
- What suggestions remain (for human review)
- If the target was already clean, say so

If pass 2 still produces new violations or risks after fixes, run one more pass (max 3 total). If pass 3 still doesn't converge, halt and return to human with the unconverged state — the target may have structural issues the skill can't resolve.

## Review order by profile

**web-app:** a11y → states → spacing → typography → color → transitions → conventions → conveyance

**component:** a11y → states → spacing → color

**game-ui:** conveyance → states → physics → spacing → color → typography → a11y → transitions

**marketing:** typography → spacing → color → a11y → transitions

## Contract

- **Precondition**: target exists and is inspectable (readable file, fetchable URL, or viewable screenshot)
- **Postcondition**: all violations and risks fixed, suggestions reported, diff traces back to grimoire principles
- **Convergence**: `design(design(x)) == design(x)` after fixes applied. Max 3 passes. Suggestions are the non-zero floor.
- **Failure mode**: if pass 3 still produces new violations/risks, halt and return to human with unconverged state

## Rules

- Every finding must point to observable evidence. No "improve hierarchy" without saying what's wrong and where.
- Don't spawn subagents for principles outside the profile's review order. A component doesn't need platform conventions.
- Don't report the same issue under multiple principles. Pick the most relevant one.
- Accessibility violations are always high severity. They're locked doors, not aesthetic preferences.
- Suggestions must name the principle they're grounded in. "This feels off" is not a finding.
- If the user provides a `--focus`, only lint those principles. Skip the rest.
- If you can't gather evidence for a principle (e.g., no screenshot for contrast), say so and skip it rather than guessing.
- Fixes must not introduce new violations. If they do, the re-lint catches them.
