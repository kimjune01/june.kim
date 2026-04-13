---
variant: post-medium
title: "GUI Before Computers"
tags: design
---

The strongest test for a UI principle is whether it existed before screens. If a rule about interface design was discovered in a psychology lab in the 1920s and still applies to a React app in 2026, it's not a best practice. It's perceptual physics. No framework can break it because no framework invented it.

### The physics

**Gestalt principles (1920s).** Wertheimer, Koffka, and Köhler studied how humans group visual information. Proximity: things near each other look related. Similarity: things that look alike seem grouped. Closure: the eye completes incomplete shapes. Continuity: the eye follows smooth paths. Layout grids, card groups, and navigation clusters all rely on these forces whether the designer names them or not. They're not design guidelines. They're how vision works.

**Fitts's Law (1954).** Paul Fitts measured pointing speed with physical styli and found that the time to reach a target is a function of distance and size. Larger, closer targets are faster to hit. This is why primary actions are big buttons, the Mac menu bar is pinned to the screen edge (infinite height = instant target), and mobile tap targets need minimum sizes. The constants change per device, but the law transferred to mice, touchscreens, and VR controllers.

**Hick's Law (1952).** William Edmund Hick measured choice reaction time with lamp-and-key tests: decision time increases logarithmically with the number of options. Effective menus are shallow because of this. Settings screens need hierarchy because of this. "Just add another option" is never free — the cost of each additional choice diminishes, but never reaches zero.

**Miller's Law (1956).** Working memory holds roughly 7±2 chunks. George Miller published this in one of the most cited papers in psychology. It's why phone numbers have segments, why wizards have steps, and why dumping 30 items on screen without grouping overwhelms users. Chunking is the workaround — group items and each group becomes one chunk.

**Affordances (Gibson, 1979).** James Gibson formalized affordances in *The Ecological Approach to Visual Perception*: the actions an environment permits. A flat surface affords sitting. A handle affords pulling. Don Norman brought the term into design in 1988, and later clarified with *signifiers* — the cues that communicate the affordance. The distinction matters: a door has an affordance (pushable) but might lack a signifier (no plate, no handle). Most "bad UI" is a signifier problem, not an affordance problem.

**Signal-to-noise ratio (Shannon, 1948).** Every element on screen either carries information or obscures it. Claude Shannon formalized this in information theory; Tufte applied it to charts as the "data-ink ratio" in 1983. The analogy isn't exact — visual clutter isn't channel noise — but the design implication holds: remove what doesn't carry signal. Unnecessary gridlines, decorative gradients, chrome that doesn't communicate state. Tufte called it chartjunk.

**Principle of least surprise (~1960s).** If a component behaves differently from what the user expects, the user's mental model breaks. The earliest formal reference is a 1967 PL/I programming bulletin, but the cognitive basis — that prediction error is costly — predates computing entirely. Swap the cancel and confirm buttons and watch users flinch.

### The opinions that held up

These emerged in the computer era. They're not physics — they're design judgments. But they've survived 30+ years of platform churn, which is its own kind of evidence.

**Shneiderman's 8 golden rules (1986).** Consistency, feedback, reversal, user control, error prevention, among others. Published in *Designing the User Interface*. Forty years later, every one still applies. The language aged well because Shneiderman wrote about human cognition, not about any particular technology.

**Norman's design principles (1988).** *The Design of Everyday Things* introduced visibility, feedback, constraints, mapping, consistency, and affordances to a popular audience. Norman revised the book in 2013, adding signifiers and refining the conceptual model. The revision is notable: he admitted the original affordance framing was too loose and tightened it. A principle set that self-corrects is more trustworthy than one that doesn't.

**Nielsen's 10 heuristics (1994).** Derived from factor analysis of 249 usability problems. The heuristics are durable because they mostly restate older cognitive constraints: feedback, recognition over recall, consistency, error prevention and recovery. These are the most widely cited heuristics in the field. But they've also been diluted — "aesthetic and minimalist design" gets invoked to justify any design preference, which is a sign the heuristic is too broad to constrain.

**Doherty threshold (1982).** Doherty and Thadani at IBM showed that response times under 400ms kept users in sustained mental flow. Above that, attention fragments. The 400ms number has held across terminals, desktop apps, web pages, and mobile — not derived from neuroscience, but replicated across enough contexts to function as a constant.

**Tognazzini's first principles (2003).** Bruce Tognazzini, who designed the original Mac human interface, published 23 principles including anticipation, autonomy, and latency reduction. Less cited than Nielsen, more comprehensive. The standout: *explorable interfaces* — design so users navigate by landmark, not by memorized routes. That's Gestalt continuity from 80 years earlier.

### What needs translation

These principles held up in substance but their framing aged.

**"Match between system and real world" (Nielsen #2).** The kernel is right: use the user's language and concepts, not system internals. But "real world" implied a shared physical metaphor — leather textures for a notepad, a trash can for deletion. The better formulation: match the user's mental model. A banking app still says "transfer" and "balance," not `POST /transactions`. That's the principle doing its job; the skeuomorphic framing was just one way to apply it.

**"Help and documentation" (Nielsen #10).** The heuristic was never "users love manuals." It was: help should be findable, task-focused, and concise. But the framing implies documentation is a normal part of the experience. For routine tasks, if users need docs, the interface has a problem. For complex tools — Photoshop, Blender, dev tools — documentation is legitimate. The translation: teach in context; document complexity, not routine use.

**"Reduce short-term memory load" (Shneiderman #8).** This is Miller's Law restated as a design rule. It held up, but invoking Shneiderman adds no explanatory power beyond citing Miller directly. The physics subsumes the opinion.

### The filter

If a principle predates computers, trust it. It survived because it describes perception, not preferences.

This post covers the spatial and static side — what the eye does with a single frame. Two dimensions it doesn't cover: how transitions carry meaning over time ([Life Is in the Transitions](/life-is-in-the-transitions)) and who gets locked out when perception varies ([Accessibility Not Optional](/accessibility-not-optional)).

If a principle is from the computer era but has held up for 30+ years across platforms, treat it as load-bearing. Test before removing.

If a principle is younger than the current framework, it might be fashion. It might also be genuine discovery. The way to tell: does it reduce to one of the older principles, or does it say something new? "Cards improve scannability" reduces to proximity, similarity, enclosure, and chunking — cite the originals. "Skeleton loaders feel faster than spinners" probably reduces to feedback and perceived latency. If it reduces, the older principle is load-bearing. If it's genuinely new, it needs time.

The point is not that old principles are automatically correct. The point is that age is evidence. A principle that survived paper forms, factory controls, aircraft cockpits, terminals, desktops, phones, and headsets is probably describing the user, not the medium.
