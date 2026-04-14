# Game UI Lessons
Source: /game-ui-lessons

## Use When
- Evaluating overall UX quality of an app that competes for discretionary attention
- Reviewing onboarding, feedback loops, or novice-to-expert progression
- Justifying investment in UI polish ("juiciness") to stakeholders

## Look For
- **No survival pressure**: app relies on utility lock-in instead of interface quality
- **Onboarding as info dump**: everything taught at once via text, not through progressive interaction
- **Flat feedback**: every action gets the same response regardless of significance
- **No expertise gradient**: interface is equally overwhelming to novice and expert
- **Missing juiciness**: actions feel inert (no animation, no sound, no microinteraction)
- **Gamification instead of conveyance**: points/badges bolted on without teaching through use

## Common Findings
- violation: First-run drops user on a feature-dense dashboard with no guided path
- violation: Destructive action (delete, send) has same feedback weight as trivial action (copy)
- risk: Interface has no progressive disclosure — all complexity visible from first interaction
- risk: "Gamification" layer (streaks, badges) without underlying conveyance or effort calibration
- suggestion: Design first-run as a single-mechanic tutorial (one lesson per step)
- suggestion: Scale feedback to action consequence (toast for copy, confirmation for delete, celebration for milestone)

## Evidence Required
- Complete the first-run experience and document: how many concepts are introduced at once?
- List every action and its feedback: is feedback immediate? Specific? Proportional?
- Check if the same interface serves novice and expert without a mode switch
- Identify any "gamification" features and check if they have conveyance underneath
- Reference: Koster (fun = learning), Swink (juiciness), Hodent (cognitive load in game UI)

## Recommendations
- Teach through interaction, not text overlays or tooltip carousels
- One mechanic per tutorial step (Dark Souls pattern)
- Feedback proportional to consequence (Slay the Spire: damage numbers, XP ticks, reward popups)
- Layer information so depth is available but not forced (card tooltips serve both novice and expert)
- Progressive disclosure through unlocking, not through hiding in settings
- HUD minimalism: show contextual information when relevant, hide when not (Breath of the Wild)

## Avoid
- Recommending gamification (points, badges, leaderboards) without conveyance fundamentals
- Treating polish/juiciness as optional — in discretionary-attention products, it's structural
- Assuming app utility excuses poor interface quality
