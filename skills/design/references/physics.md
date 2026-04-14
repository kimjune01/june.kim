# Perceptual Physics
Source: /gui-before-computers

## Use When
- Reviewing any visual layout, component grouping, or interaction pattern
- Evaluating whether a design principle is load-bearing or fashion
- Justifying or challenging a design decision with evidence

## Look For
- **Proximity violations**: related elements spaced the same as unrelated ones (Gestalt)
- **Target size**: primary actions that are small or far from the cursor's resting position (Fitts)
- **Choice overload**: menus or settings with 10+ ungrouped options (Hick)
- **Memory overload**: screens showing 10+ unchunked items simultaneously (Miller)
- **Missing signifiers**: interactive elements with no visual cue they're tappable/clickable (Norman)
- **Noise**: decorative elements that carry no information (Shannon/Tufte)
- **Surprise**: controls that behave differently from platform or positional convention (least surprise)

## Common Findings
- violation: Button too small or too far from input it confirms (Fitts)
- violation: Settings page is a flat list of 20+ toggles with no grouping (Hick + Miller)
- risk: Cards look identical but behave differently on click (similarity + least surprise)
- suggestion: Remove gridlines/borders that don't separate meaningful groups (signal-to-noise)
- suggestion: Group related controls closer together, increase gap to unrelated ones (proximity)

## Evidence Required
- Measure actual px distances between related vs unrelated elements
- Count options at each decision point
- Identify every interactive element and its visual signifier
- List decorative elements and state what information each carries (if none, it's noise)

## Recommendations
- Apply Gestalt grouping: proximity for related items, similarity for same-type items
- Minimum tap targets: 44x44pt (Apple), 48x48dp (Material)
- Chunk long lists into groups of 3-5 with visible separators
- Ensure every interactive element has a distinct signifier (shape, color, cursor change)
- Remove elements that don't carry information or communicate state

## Avoid
- Citing "clean design" or "minimalism" without specifying which signal-to-noise problem it solves
- Invoking Fitts's Law for elements that aren't primary actions
- Treating these principles as style preferences rather than perceptual constraints
