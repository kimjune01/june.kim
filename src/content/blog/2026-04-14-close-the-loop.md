---
variant: post
title: "Close the Loop"
tags: design
---

A button that says "Copy agent URL" is clickable, works correctly, and copies the URL to the clipboard. A user looked at it and didn't know it was a button. It looked like a label. The fix was obvious once named: show the URL as selectable text, put a 📋 icon beside it. The icon is the signifier. The text is the content. The ✓ that replaces the icon for one second is the confirmation.

Three things, three jobs: what to act on, how to act, and proof it worked. That's the loop.

### The two gulfs

[Don Norman](https://en.wikipedia.org/wiki/Don_Norman) described two gaps in the action cycle. The **gulf of execution** is the distance between what the user wants to do and what the interface lets them do. The **gulf of evaluation** is the distance between what the system did and whether the user can tell.

The copy button had a small execution gulf. Clicking it worked. It had a large evaluation gulf. The only feedback was the button text changing from "Copy agent URL" to "✓ copied" and back. If you weren't watching the button at the moment of click, you missed it. If you were watching, the text change looked the same as the resting state because both were unstyled text in the same position.

Most broken interfaces have one gulf or the other. A cryptic icon has a wide execution gulf: users don't know what to do. A silent mutation has a wide evaluation gulf: users don't know what happened. The worst interfaces have both.

### Three checkpoints

Norman's [seven stages of action](https://en.wikipedia.org/wiki/Seven_stages_of_action) describe the full cycle from goal to evaluation. For interface review, they reduce to three checkpoints. **Specify**: can the user find the right control? **Perceive**: can they see the result? **Compare**: can they tell if the result means success?

The copy button failed at specify (looked like a label) and perceive (the button didn't add feedback, it replaced its own identity with feedback). Two failures on the same control.

### Slips and mistakes

Norman distinguished **slips** (right intention, wrong action) from **mistakes** (wrong intention). Slips are motor errors: you meant to click copy but hit the adjacent button. Fix with spacing, sizing, [Fitts's Law](/gui-before-computers). Mistakes are model errors: you thought "Copy agent URL" was a heading, not a button. Fix with signifiers, [state visibility](/state-complete), consistent patterns. The copy button was a mistake. The user's model said "label." The system's model said "button." The signifier was missing.

### Inline confirmation

The strongest feedback for lightweight actions is **inline confirmation** — the trigger itself shows the result. The 📋 becomes ✓ for one second, then reverts. No toast, no modal, no banner.

This works because it closes the evaluation gulf at the point of attention. The user's eyes are already on the thing they clicked. Moving confirmation to a toast in the corner forces a saccade — the eyes leave the action site to find the feedback. For a copy action that takes 50ms, that saccade is the entire interaction.

Inline confirmation has limits. It works for actions that are instant, low-consequence, and self-evident on success: copy, save draft, favorite, mark read, pin. It fails for actions that take time (show a progress indicator), have consequences (show what changed), or need proof (show a receipt). Match the feedback to the consequence, not to the action.

### The audit

For any interactive element, ask three questions:

**Can the user tell what to do?** Is the action visible, labeled, and distinguishable from non-interactive content? Does it follow a pattern the user has seen before? A 📋 icon on a code block is a pattern. A text-styled button that says "Copy agent URL" is not.

**Can the user tell it worked?** Is there feedback, and is it at the point of attention? Does it appear within 100ms? Does it persist long enough to register but not long enough to block the next action?

**Can the user tell what it means?** Does the feedback map to the goal? A ✓ after copy means success. A ✓ after delete could mean "deleted" or "confirmed for deletion." Ambiguous feedback is worse than no feedback because it closes the evaluation gulf with the wrong answer.

If any answer is no, the loop is open. Close it.
