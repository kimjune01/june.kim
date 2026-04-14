# Accessibility
Source: /accessibility-not-optional

## Use When
- Reviewing any user-facing interface
- Always. This is not conditional. Accessibility is checked on every review.

## Look For
- **Contrast ratios**: text below 4.5:1, large text or UI components below 3:1
- **Touch targets**: interactive elements smaller than 48x48dp (Material) or 44x44pt (Apple)
- **Focus indicators**: missing or invisible focus rings on keyboard navigation
- **Semantic HTML**: divs and spans used where buttons, links, headings, landmarks belong
- **ARIA misuse**: ARIA roles on elements that already have native semantics, or missing ARIA on custom widgets
- **Motion**: animations with no `prefers-reduced-motion` support
- **Color alone**: state communicated only through color with no secondary indicator
- **Missing alt text**: images without text alternatives

## Common Findings
- violation: Interactive element has no visible focus indicator
- violation: Custom widget built from divs with no ARIA role or keyboard handler
- violation: Image conveys information but has no alt text or empty alt on decorative image that isn't aria-hidden
- violation: Touch target under 48x48dp
- risk: Animations play regardless of reduced-motion preference
- risk: Form errors indicated only by red border (no icon, no text)
- suggestion: Replace div-with-onclick with semantic button element

## Evidence Required
- Measure contrast ratios with a tool (browser devtools, Colour Contrast Analyser)
- Tab through the entire interface with keyboard only; document where focus is lost or invisible
- Inspect DOM for semantic elements vs div/span with event handlers
- Check `prefers-reduced-motion` media query presence in CSS/JS
- Verify every image has appropriate alt text (informative) or is marked decorative
- Reference: WCAG 2.1 (w3.org/WAI/standards-guidelines/wcag/), Material accessibility foundations

## Recommendations
- Contrast: 4.5:1 for normal text, 3:1 for large text and non-text UI components
- Touch targets: minimum 48x48dp with adequate spacing between targets
- Focus: visible focus ring on all interactive elements, test with keyboard-only navigation
- Semantics: use native HTML elements (button, a, input, nav, main, h1-h6) before ARIA
- Motion: wrap animations in `@media (prefers-reduced-motion: no-preference)`
- Color: always pair with icon, text label, or shape change
- Alt text: describe the information the image conveys, not the image itself

## Avoid
- Treating accessibility as a separate pass ("we'll add it later")
- Reporting only contrast issues while ignoring keyboard navigation and semantics
- Recommending ARIA as a first resort over semantic HTML
- Saying "good enough" — this is the one area where partial compliance locks people out
