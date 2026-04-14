# Platform Conventions
Source: /platform-conventions

## Use When
- Reviewing a design that ships on a specific platform (iOS, Android, web, desktop, CLI, email)
- Navigation, gesture, or interaction patterns feel "off" without a clear violation
- Cross-platform app needs to decide which conventions to follow

## Look For
- **iOS violations**: missing back-swipe gesture, non-standard tab bar, custom nav that breaks nav stack mental model
- **Android violations**: missing bottom nav, non-Material component patterns, back button doesn't work as expected
- **Web violations**: links not underlined or distinguishable, non-standard form controls, broken browser back
- **CLI violations**: non-composable output (not pipe-friendly), missing --help, destructive ops without --force flag
- **Email violations**: width over 600px, CSS that won't inline, layout dependent on `<style>` tags
- **Cross-platform mismatch**: platform-specific pattern used on wrong platform (iOS swipe-back on Android)

## Common Findings
- violation: iOS app uses hamburger menu instead of tab bar for primary navigation
- violation: CLI tool outputs mixed data/messages to stdout (breaks piping)
- violation: Web app disables browser back button or breaks history state
- risk: Cross-platform app follows one platform's conventions and alienates the other's users
- risk: Email layout relies on CSS grid or flexbox (Outlook uses Word renderer)
- suggestion: Check the platform's published guidelines for the specific component in question

## Evidence Required
- Identify the target platform(s)
- Load the corresponding guideline:
  - iOS: Apple HIG (developer.apple.com/design/human-interface-guidelines)
  - Android/cross-platform: Material Design (m3.material.io)
  - Windows: Fluent Design (learn.microsoft.com)
  - Web: WCAG as floor, then chosen design system
  - CLI: clig.dev
  - Email: caniemail.com for feature support
- Compare the specific interaction pattern against the platform's documented convention
- For cross-platform: use the intersection of platform conventions

## Recommendations
- Native apps: follow the platform's full guideline set
- Cross-platform apps: follow patterns all platforms agree on; avoid platform-specific gestures
- Web apps: WCAG as floor, pick a consistent design system above it
- CLI: stdout for data, stderr for messages; --help for usage; --force for destructive ops
- Email: 600px max width, table layout, inline styles, design for images-off

## Avoid
- Assuming web conventions apply to native apps or vice versa
- Citing platform conventions without checking the actual published guideline
- Treating "least surprise" as universal — it's a function of platform context
