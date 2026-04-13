---
variant: post
title: "Accessibility Not Optional"
tags: design
---

Accessibility doesn't reduce to the other design principles. Gestalt, Fitts, Hick, and Shannon describe how perception works for a typical visual user. Accessibility asks: what about everyone else? It spans [perceptual physics](/gui-before-computers) (contrast, color blindness), motor constraints (keyboard nav, touch targets), law (WCAG, ADA), and ethics. No single framework covers it.

The best practical guide is [Material Design's accessibility foundations](https://m3.material.io/foundations/accessible-design/overview). It's comprehensive, maintained, and CC-BY 4.0. Google writes it as a committee, but the committee did good work here.

Key ingredients for an agent:

- Contrast ratios: 4.5:1 for text, 3:1 for large text and UI components
- Touch targets: 48×48dp minimum
- Focus indicators for keyboard navigation
- Semantic HTML and ARIA roles
- `prefers-reduced-motion` support
- Color not as the sole indicator of state
- Text alternatives for images

The [WCAG guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/) are the legal standard. Material Design translates them into actionable design patterns. Use both: WCAG for compliance, Material for implementation.

This is the one area where "good enough" is not good enough. Every other design principle degrades gracefully — a slightly wrong line height is still readable, a slightly slow transition is still navigable. An inaccessible interface is a locked door.
