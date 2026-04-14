# Color Systems
Source: /color-systems

## Use When
- Reviewing color usage in any interface
- Setting up or auditing a color palette or design tokens
- Adding dark mode support
- Checking color accessibility

## Look For
- **Arbitrary hex values**: colors defined as raw hex/rgb with no semantic role
- **Color as sole indicator**: state communicated only through color (error = red, success = green, nothing else)
- **Contrast failures**: text or UI components that don't meet WCAG minimums
- **Palette bloat**: more than 5 active color roles in use
- **Dark mode = inverted light mode**: colors simply inverted rather than independently designed
- **Missing semantic mapping**: no clear primary/secondary/error/surface role assignment

## Common Findings
- violation: Color is the only indicator of error or success state (8% of men are color blind)
- violation: Text contrast below 4.5:1 (normal text) or 3:1 (large text / UI components)
- risk: Dark mode uses same saturation as light mode (too vibrant on dark surfaces)
- risk: Six or more distinct color roles with no clear hierarchy
- suggestion: Map every color to a semantic role (primary, secondary, tertiary, error, surface)

## Evidence Required
- List every color in use and its semantic role (if any)
- Measure contrast ratios for text-on-background and icon/border-on-background pairs
- Check both light and dark modes independently
- Identify any state communicated solely through color; confirm a second channel exists (icon, text, shape)
- Reference: Material Design color system (m3.material.io/styles/color/overview)

## Recommendations
- Define semantic roles: primary (key actions), secondary, tertiary (accent), error, surface
- Normal text: 4.5:1 contrast minimum (WCAG 2.1 SC 1.4.3)
- Large text and UI components: 3:1 minimum (SC 1.4.11)
- Always pair color with a second indicator (icon, label, shape change)
- Dark mode: reduce saturation, adjust surfaces independently, re-test all contrast ratios
- Limit active palette to primary + secondary + error + neutrals unless justified

## Avoid
- Choosing colors for aesthetic preference without checking semantic role and contrast
- Assuming a palette that passes in light mode also passes in dark mode
- Recommending specific brand colors (that's a user decision, not an agent decision)
