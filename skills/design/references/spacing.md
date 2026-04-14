# Spacing Systems
Source: /spaced-out

## Use When
- Reviewing layout spacing, margins, padding, or gap values
- A layout feels "off" but individual elements look fine
- Setting up or auditing a spacing scale / design tokens

## Look For
- **Equal spacing ambiguity**: gap between label and input equals gap between fields (grouping lost)
- **No scale**: spacing values are arbitrary px numbers with no system (4, 7, 13, 19, 22)
- **Base unit violations**: values that aren't multiples of the base unit (4px or 8px)
- **Hierarchy inversion**: gap within a group is larger than gap between groups
- **Whitespace removal**: spacing reduced to "fit more" at the cost of grouping clarity
- **Responsive breakage**: grouping relationships lost on mobile (items that were grouped now equidistant)

## Common Findings
- violation: Label-to-input gap equals field-to-field gap (proximity ambiguity)
- violation: No consistent spacing scale; values are ad hoc per component
- risk: Section gaps and group gaps are the same size (hierarchy flattened)
- risk: Responsive layout collapses columns but keeps desktop spacing ratios
- suggestion: Establish a 6-token scale (e.g., 4/8/12/16/24/32px) and apply consistently

## Evidence Required
- Extract all spacing values (margin, padding, gap) from the component or page
- Check if values conform to a consistent scale (multiples of base unit)
- Compare intra-group gaps vs inter-group gaps vs section gaps
- Test at mobile breakpoints: do proximity relationships survive the collapse?

## Recommendations
- Base unit: 4px or 8px. Every spacing value is a multiple
- Scale: ~6 tokens is enough for most sites (e.g., 4/8/12/16/24/32)
- Within a control: smallest gap (label to input)
- Between siblings: medium gap (field to field)
- Between groups: larger gap
- Between sections: largest gap
- Vertical rhythm: line-height and paragraph spacing should share the base unit
- Paragraph spacing: 50-100% of body text size (Butterick)
- Optical corrections (icon nudges, baseline alignment) are exceptions; name them

## Avoid
- Prescribing exact pixel values without checking the existing scale
- Treating whitespace as wasted space
- Adjusting one margin without checking how it affects adjacent grouping relationships
