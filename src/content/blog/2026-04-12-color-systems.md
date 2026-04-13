---
variant: post
title: "Color Systems"
tags: design
---

Color is an elaboration on two principles from [GUI Before Computers](/gui-before-computers): Gestalt similarity (things that look alike seem grouped) and [signal-to-noise](/gui-before-computers) (color that doesn't carry meaning is noise). It's also an [accessibility](/accessibility-not-optional) concern.

### Operational guide

[Material Design's color system](https://m3.material.io/styles/color/overview) is the best operational reference. It defines five semantic color roles: primary (key actions), secondary (less prominent actions), tertiary (accents), error (destructive/failure states), and surface (backgrounds/containers). Each role has tonal variants for different elevations and states.

The key insight: color roles are semantic, not aesthetic. Arbitrary hex values break when you add dark mode, new components, or accessibility requirements. Semantic roles scale because the role stays the same even when the value changes.

### Key ingredients for an agent

- **Semantic roles, not hex values.** Every color maps to a function: primary, secondary, tertiary, error, surface. Brand color can inform primary, but primary means "the most important interactive element."
- **Contrast ratios.** 4.5:1 minimum for normal text (WCAG 2.1 SC 1.4.3). 3:1 minimum for large text and non-text UI components (SC 1.4.11). Test both light and dark modes.
- **Never color alone.** Color must not be the sole indicator of state. Pair with icons, text, or shape. 8% of men have color vision deficiency.
- **Dark mode is its own palette.** Not inverted light mode. Needs adjusted surfaces, reduced saturation, and re-tested contrast ratios.
- **Limit the palette.** Primary, secondary, error plus neutrals covers most interfaces. More than five active color roles is usually noise.

### Reference implementations

- [Now in Android](https://github.com/android/nowinandroid) (Apache-2.0) — Material 3 dynamic color, tonal palettes, dark mode with proper surface adjustment. The reference for semantic color roles in practice.
