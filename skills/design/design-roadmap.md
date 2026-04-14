# /design roadmap

## Done
- 10 grimoire posts: physics, transitions, states, spacing, color, a11y, conventions, game-ui-lessons, gaming-patterns, typography
- SKILL.md: process, profiles, finding format, convergence contract
- Reference distillation: 10 operational files in references/
- /design tag page on june.kim

## Next: smoke test
- Run `/design /Users/junekim/Documents/hangout --profile web-app`
- Evaluate: are findings evidence-based or vibes? Are references operational or still essay-like?
- Calibrate severity thresholds from real output
- Tune references based on what over-reports or under-reports

## Then: deterministic scripts
- `contrast_check.py` — WCAG ratio from computed color values
- `heading_order.py` — validate h1→h2→h3 sequence
- `hardcoded_values.py` — grep for magic px/hex outside token system
- `state_presence.py` — grep for loading/error/empty/success patterns in components
- `focus_indicators.py` — check for :focus/:focus-visible styles
- These make the violations tier mechanical, not LLM-dependent

## Later: modes
- Screenshot mode: render → capture → analyze (needs Playwright or dev-browser)
- URL mode: fetch + DOM inspection (partially works via WebFetch)
- Profile refinement: split/merge profiles based on real usage patterns
- `--focus` flag validation: confirm scoping works cleanly

## Integration
- `/design` finds → user approves → agent fixes → `/design` re-runs → convergence
- Potential `/simplify` integration for auto-fix of violations

## Not planned
- Figma integration (wrong tool for CLI)
- "Does this look good?" (taste stays with human)
- Auto-fix for suggestions (only violations/risks get fix candidates)
- Font choice (Attend — always elicit from user)
