---
variant: post
title: "Platform Conventions"
tags: design
---

The [principle of least surprise](/gui-before-computers) says: match what the user expects. But expects *what*? That depends on where they are. An iOS user expects a back swipe from the left edge. An Android user expects a bottom nav bar. A web user expects underlined links. Violating platform conventions triggers the same flinch as swapping cancel and confirm, except the user can't say why.

Each platform publishes its expectations. These are the context parameters for least surprise.

### Apple — Human Interface Guidelines

[developer.apple.com/design/human-interface-guidelines](https://developer.apple.com/design/human-interface-guidelines)

Opinionated and prescriptive. Covers iOS, macOS, watchOS, tvOS, visionOS. Strong on navigation patterns (tab bars, nav stacks, modal sheets), typography (SF Pro system), spacing, and platform-specific interaction (swipe gestures, Digital Crown, spatial input). The HIG assumes you're building a native app; web apps get less guidance. Recently updated for Liquid Glass, which is controversial — the older principles underneath are still sound.

### Google — Material Design

[m3.material.io](https://m3.material.io)

Component-driven and systematic. Material 3 covers Android, web, and cross-platform. Strong on color systems (dynamic color, tonal palettes), typography scale, elevation/shadow, motion, and accessibility. More permissive than Apple — a system you adapt, not rules you follow. The [accessibility foundations](https://m3.material.io/foundations/accessible-design/overview) are best-in-class. CC-BY 4.0.

### Microsoft — Fluent Design

[learn.microsoft.com/en-us/windows/apps/design](https://learn.microsoft.com/en-us/windows/apps/design/)

Covers Windows, Office, and cross-platform. Fluent emphasizes depth, motion, material, and scale. Less opinionated than Apple, less systematic than Material. Strongest on input modalities — mouse, touch, pen, keyboard, and gamepad all treated as first-class.

### W3C — Web Content Accessibility Guidelines + WAI-ARIA

[w3.org/WAI/standards-guidelines/wcag](https://www.w3.org/WAI/standards-guidelines/wcag/)

See [Accessibility Not Optional](/accessibility-not-optional) for the principles. WCAG is the legal standard; WAI-ARIA fills the gap between semantic HTML and complex widgets.

### CLI — Command Line Interface Guidelines

[clig.dev](https://clig.dev/)

The Butterick of CLIs. Concrete, opinionated, community-maintained. Covers naming (`verb-noun`), flags (`--force` for destructive ops), output (stdout for data, stderr for messages), error handling, color semantics, and composability (pipe-friendly by default). The terminal has conventions as strong as any GUI — `^C` to interrupt, `--help` for usage, `-` for stdin. clig.dev writes them down.

### Email — HTML Email

No single authority. The rendering environment is hostile: Outlook uses Word's HTML engine, Gmail strips `<style>` tags, every client is different. The de facto conventions: 600px max width, table-based layout, inline styles, images-off-by-default design. [Can I Email](https://www.caniemail.com/) is the caniuse.com equivalent. [Mailchimp's email guide](https://templates.mailchimp.com/getting-started/html-email-basics/) and [Email on Acid](https://www.emailonacid.com/blog/article/email-development/email-development-best-practices-2/) are the most practical references. The platform convention for email is: assume nothing works.

### The agent instruction

When linting a design, check which platform it ships on and load the corresponding conventions. A cross-platform app gets the intersection — the patterns that all platforms agree on. A native app gets the full platform spec. A web app gets WCAG as the floor and picks its own conventions above it.

Least surprise is not a universal. It's a function of context.
