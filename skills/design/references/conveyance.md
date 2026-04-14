# Conveyance (Gaming Patterns)
Source: /gaming-patterns

## Use When
- Reviewing onboarding flows, first-run experiences, or feature discovery
- Users need to learn a complex interface without documentation
- Evaluating whether the UI communicates available actions, progress, and state without instruction

## Look For
- **Silent states**: user must guess what just happened (no feedback on action completion)
- **Missing goal clarity**: tasks with no defined scope, progress indicator, or completion signal
- **Effort mismatch**: onboarding dumps all features at once instead of progressive disclosure
- **No chaining**: after completing a task, user gets no pointer to the next step
- **Tooltip dependence**: features explained only through text overlays, not through interaction
- **Flat expertise curve**: same UI for novice and expert with no layered depth

## Common Findings
- violation: User completes signup and lands on empty dashboard with no guidance
- violation: Action completes with no visual/audio feedback (no conveyance of "what just happened")
- risk: Onboarding checklist has 8+ items with no ordering, grouping, or effort estimate
- risk: Feature discovery relies entirely on tooltip carousel that users dismiss
- suggestion: Chain tasks so completing one reveals the next (quest-chain pattern)
- suggestion: Add enemy-intent equivalent: telegraph what the system will do next before it does it

## Evidence Required
- Walk through the first-run experience step by step; document every moment where direction is unclear
- For each user action, check: is there immediate visual feedback? Does it convey what happened?
- Count how many features are exposed simultaneously to a new user
- Check if the interface layers information (novice reads surface, expert reads depth)
- Map the experience against the quest-system checklist: goal clarity, effort calibration, chaining, progressive disclosure, feedback

## Recommendations
- **Goal clarity**: every task should have unambiguous scope and a visible progress indicator
- **Effort calibration**: scope onboarding tasks to 2-5 minutes each, matched to user's current knowledge
- **Chaining**: completing one task should surface the next (not require user to find it)
- **Progressive disclosure**: teach one concept at a time through interaction, not text
- **Feedback**: every action gets immediate, specific feedback proportional to its significance
- **Layered UI**: same screen serves novice and expert (tooltips on hover, advanced info available but not forced)
- **Hub-and-spoke**: group 3-5 related tasks in one location, not scattered across the app

## Avoid
- Recommending "gamification" (points, badges, leaderboards) as a substitute for conveyance
- Conflating progressive disclosure with hiding features behind settings
- Suggesting tutorial overlays when the interface could teach through use
