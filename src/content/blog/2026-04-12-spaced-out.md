---
variant: post
title: "Spaced Out"
tags: design
---

Spacing is [Gestalt proximity](/gui-before-computers) operationalized. Things near each other look related. Things far apart look separate. Every margin, padding, and gap decision is a proximity decision.

Equal spacing creates ambiguity. If the gap between a label and its input equals the gap between two fields, grouping becomes harder to parse. The eye can't tell what belongs to what. Unequal spacing *is* the hierarchy.

### The decision ladder

Use the smallest gap for parts of the same control. A middle gap for sibling controls. A larger gap between groups. The largest gap between sections.

```css
:root {
  --sp-1: 4px;
  --sp-2: 8px;
  --sp-3: 12px;
  --sp-4: 16px;
  --sp-5: 24px;
  --sp-6: 32px;
}

.form-field {
  display: grid;
  gap: var(--sp-1); /* label belongs to input */
}

.form {
  display: grid;
  gap: var(--sp-4); /* fields are siblings */
}

.section {
  margin-block: var(--sp-6); /* sections are separate */
}
```

Six tokens is often enough for a small site. The numbers matter less than the ordering: if two things are semantically closer, their gap should be visually smaller than the gap around the group.

### The scale

A spacing scale prevents "CSS whack-a-mole," where adjusting one margin to fix one gap breaks another gap. Most spacing should come from the scale. Exceptions for optical correction (icon nudges, baseline alignment, hairline borders) should be rare and named.

Material Design uses 8dp layout increments, with typography and smaller elements aligning to 4dp.

### Key ingredients for an agent

- **Base unit.** 4px or 8px. Every spacing value is a multiple.
- **Vertical rhythm.** Line height and paragraph spacing share the base unit with the layout grid. Butterick recommends paragraph spacing at 50-100% of body text size.
- **Responsive layouts.** Preserve grouping intent, not numeric ratios. On mobile, two-column layouts collapse, section gaps shrink, margins change. The proximity relationships should survive even when the numbers don't.
- **Whitespace is signal.** Empty space between groups communicates "these are separate." Removing whitespace to "fit more" destroys the grouping information.

### Operational guides

- [Material Design layout](https://m3.material.io/foundations/layout/understanding-layout/spacing) — 8dp grid, systematic spacing
- [Tailwind spacing tokens](https://tailwindcss.com/docs/theme) — practical constrained scale via `--spacing-*` namespace
- [Butterick's Practical Typography](https://practicaltypography.com) — line height, margins, and paragraph spacing for text
