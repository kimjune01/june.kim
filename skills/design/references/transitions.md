# Transition Metaphors
Source: /life-is-in-the-transitions

## Use When
- Reviewing navigation between screens or states
- A UI feels like a "slideshow" or "PowerPoint deck"
- State changes happen instantly with no animation or spatial cue

## Look For
- **Jump cuts**: state changes with no animation, fade, or spatial hint
- **Missing metaphor**: transitions that don't communicate direction (forward/back/layer/mode)
- **Inconsistent metaphor**: mixing spatial (slide) and atmospheric (fade) for same-level navigation
- **No anchor**: every element on screen changes simultaneously, losing spatial context
- **Metaphor present**: check which of the four types is used and whether it's consistent

## Common Findings
- violation: Navigation between sibling screens has no transition at all
- violation: Modal appears instantly with no backdrop fade or slide-up
- risk: Mixing slide-left and fade for same-level navigation (conflicting metaphors)
- suggestion: Add a fixed/anchored element (header, divider, nav bar) to provide spatial continuity
- suggestion: Even 0.15s fade-and-shift is enough to prevent the "slam" effect

## Evidence Required
- Trigger every navigation path and note: does the screen jump-cut or transition?
- Identify which metaphor each transition uses: spatial, anchored, continuous, or atmospheric
- Check if a consistent anchor element persists across state changes
- Measure transition duration (under 100ms reads as instant, 150-350ms is the sweet spot)

## Recommendations
- **Spatial**: nav push/pop, drawers, modals. Content slides from where it "lives"
- **Anchored**: fix one element (header, divider, nav bar) while content changes around it
- **Continuous**: gesture-driven transitions (swipe-to-dismiss, pull-to-refresh, drag-to-resize)
- **Atmospheric**: fade-in for content loading, crossfade for route changes, skeleton shimmer
- Pick one metaphor per navigation level and apply it consistently
- The constraint ("the divider doesn't move") is more valuable than the animation

## Avoid
- Adding animation without a metaphor (decorative motion is noise)
- Requiring `prefers-reduced-motion` users to lose spatial context (use instant position change instead)
- Critiquing transition duration without testing the actual feel
