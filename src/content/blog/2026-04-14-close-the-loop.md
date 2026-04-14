---
variant: post
title: "Close the Loop"
tags: design
---

A button that says "Copy agent URL" is clickable, works correctly, and copies the URL to the clipboard. A user looked at it and didn't know it was a button. It looked like a label. The fix was obvious once named: show the URL as selectable text, put a 📋 icon beside it. The icon is the signifier. The text is the content. The ✓ that replaces the icon for one second is the confirmation.

Three things, three jobs: what to act on, how to act, and proof it worked. That's the loop.

### The two gulfs

[Don Norman](https://en.wikipedia.org/wiki/Don_Norman) described two gaps in the action cycle. The **gulf of execution** is the distance between what the user wants to do and what the interface lets them do. The **gulf of evaluation** is the distance between what the system did and whether the user can tell.

The copy button had a small execution gulf — clicking it worked. It had a large evaluation gulf — the only feedback was the button text changing from "Copy agent URL" to "✓ copied" and back. If you weren't watching the button at the moment of click, you missed it. If you were watching, the text change looked the same as the resting state because both were unstyled text in the same position.

Most broken interfaces have one gulf or the other. A cryptic icon has a wide execution gulf — users don't know what to do. A silent mutation has a wide evaluation gulf — users don't know what happened. The worst interfaces have both.

### Seven stages, three checkpoints

Norman's [seven stages of action](https://en.wikipedia.org/wiki/Seven_stages_of_action) describe the full cycle:

1. **Goal** — what the user wants (copy this URL)
2. **Plan** — how they'll do it (click the copy thing)
3. **Specify** — which action exactly (that button? that text?)
4. **Perform** — do it (click)
5. **Perceive** — see the result (did anything change?)
6. **Interpret** — understand it (the ✓ means copied)
7. **Compare** — does it match the goal? (is the URL on my clipboard?)

Design failures cluster at three checkpoints. **Specify** fails when the user can't find the right control — that's discoverability, the execution gulf. **Perceive** fails when the system responds but the user can't see it — that's feedback, the evaluation gulf. **Compare** fails when the user sees feedback but can't tell if it means success — that's ambiguity.

The copy button failed at specify (looked like a label) and perceive (text swap was too subtle). Two failures on the same control.

### Slips and mistakes

Norman distinguished two error types. A **slip** is the right intention, wrong action — you meant to click copy but hit the adjacent button. A **mistake** is the wrong intention — you thought "Copy agent URL" was a heading explaining the section, not an interactive element.

Slips are motor errors. Fix them with spacing, sizing, and [Fitts's Law](/gui-before-computers). Mistakes are model errors. Fix them with better signifiers, better [state visibility](/state-complete), and consistent patterns.

The copy button was a mistake in Norman's sense. The user's mental model was "this is a label." The system's model was "this is a button." The models diverged because the signifier was missing.

### Inline confirmation

The strongest feedback for lightweight actions is **inline confirmation** — the trigger itself shows the result. The 📋 becomes ✓ for one second, then reverts. No toast, no modal, no banner.

This works because it closes the evaluation gulf at the point of attention. The user's eyes are already on the thing they clicked. Moving confirmation to a toast in the corner forces a saccade — the eyes leave the action site to find the feedback. For a copy action that takes 50ms, that saccade is the entire interaction.

Inline confirmation has limits. It works for actions that are instant, low-consequence, and self-evident on success. Copy, bookmark, follow. It fails for actions that take time (show a progress indicator), have consequences (show what changed), or need proof (show a receipt). Match the feedback to the consequence, not to the action.

[State Complete](/state-complete) covers which states need distinct representations. This post covers the loop between them — how the user gets from action to confirmation and back to ready.

### The audit

For any interactive element, ask three questions:

**Can the user tell what to do?** Is the action visible, labeled, and distinguishable from non-interactive content? Does it follow a pattern the user has seen before? A 📋 icon on a code block is a pattern. A text-styled button that says "Copy agent URL" is not.

**Can the user tell it worked?** Is there feedback, and is it at the point of attention? Does it appear within 100ms? Does it persist long enough to register but not long enough to block the next action?

**Can the user tell what it means?** Does the feedback map to the goal? A ✓ after copy means success. A ✓ after delete could mean "deleted" or "confirmed for deletion." Ambiguous feedback is worse than no feedback because it closes the evaluation gulf with the wrong answer.

If any answer is no, the loop is open. Close it.

### Reference implementations

- [Stripe Dashboard](https://dashboard.stripe.com) — API keys shown as masked text with a copy icon. Click copies, icon briefly shows ✓. The pattern this post is about.
- [GitHub](https://github.com) — clone URL field with clipboard button. Same pattern, consistent across every copyable element.
- [NetNewsWire](https://github.com/Ranchero-Software/NetNewsWire) (MIT) — swipe actions give inline visual feedback (color + icon) before committing. No confirmation dialog for read/unread because the action is reversible and the feedback is visible.
