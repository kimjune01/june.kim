---
variant: post-medium
title: "Game UI Lessons"
tags: design
---

Nobody needs to play a videogame. There's no utility to fall back on — no bank account, no tax filing, no work email that forces you to stay. The interface is the entire product. A player who doesn't enjoy the first five minutes alt-tabs and never comes back. No sunk cost, no data lock-in, no switching cost. The only moat is how the game feels.

This makes game UI the most brutally competitive design environment that exists. Apps compete for a purchase. Games compete for every second of attention against other games that are also pure interface. Bad game UI doesn't survive long enough to ship a sequel. The result: games solved onboarding, conveyance, feedback, and novice-to-expert scaling decades ago — because they couldn't afford not to. Apps lean on utility and never have to.

The gap isn't talent. It's that game UI research rarely crosses into product design literature. Games get filed under "entertainment" and their innovations stay there.

### The quest system

WoW's quest system is the gold standard for onboarding. Not because it's fun (though it is), but because it solves every conveyance problem that app onboarding gets wrong.

**Goal clarity.** "Kill 10 boars" is unambiguous. The quest log tracks progress with a counter. You always know what's done and what's left. Most app onboarding says "set up your profile" with no indication of scope, progress, or completion.

**Effort calibration.** Each quest is scoped to 5-15 minutes and matched to your current level. The difficulty curve is tuned so you're never overwhelmed and never bored. App onboarding dumps everything at once — connect your accounts, invite your team, customize your dashboard, watch a tutorial — with no sense of ordering or effort.

**Conveyance.** The quest giver has a `!` above their head. The minimap shows objective markers. Breadcrumb quests lead you to the next hub. You never have to ask "where do I go?" Most apps drop you on a dashboard after signup and hope you figure it out.

**Chaining.** Finishing one quest unlocks the next. The chain creates momentum — you're always one step from the next reward. App onboarding has no chain. After the setup wizard, you're on your own.

**Dopamine.** Completion sound, XP bar animation, reward popup. The feedback loop is instant and specific. App onboarding either ends silently or shows a generic "You're all set!" with no sense of what you just achieved.

**Progressive disclosure.** Early quests teach one mechanic at a time. "Talk to this NPC" teaches navigation. "Use this ability" teaches combat. "Craft this item" teaches the crafting system. Each quest is a single lesson. App onboarding tries to teach everything in a tooltip carousel that nobody reads.

**Hub-and-spoke.** Quest hubs give you 3-5 quests at once, all in the same area. You batch related tasks efficiently and return for rewards. The pattern maps directly to a task dashboard — but most dashboards lack the spatial grouping and the return-for-reward loop.

### Beyond quests

The quest system isn't the only thing games got right.

**Cooldown indicators.** Circular progress overlays on abilities, showing when an action becomes available again. Now ubiquitous outside games — Uber's driver ETA, food delivery tracking, upload progress. Games formalized the pattern; apps borrowed it.

**HUD minimalism.** Breath of the Wild hides interface elements when you're not using them. The HUD fades in on demand. This is signal-to-noise applied to temporal visibility — show information when it's relevant, hide it when it's not. Most apps show everything all the time.

**Tutorialization through environment.** Dark Souls teaches mechanics through level design, not text. A weak enemy near a bonfire teaches you combat safely. A narrow bridge teaches you about falling. The environment *is* the tutorial. The equivalent in apps: design the first-run experience so the interface teaches itself through use, not through overlays.

**Health bars and progress visualization.** Games perfected showing "how much is left" — health, mana, XP, durability, cooldowns. Every progress bar, loading indicator, and completion percentage in product design descends from this. Games had to get it right because the player dies if they misread it.

**Inventory management.** Diablo's grid system, Resident Evil's tetris inventory — these are spatial reasoning problems turned into UI. The lesson: when users manage many items, give them a spatial metaphor, not just a list. File managers, email clients, and project boards all benefit from this insight but rarely apply it as well as games do.

### Novice-to-expert in one interface

Slay the Spire never explains itself. It demonstrates. The first combat has no tutorial overlay, no tooltip carousel. You draw cards, you see energy, you drag a card onto an enemy, a damage number flies off. The interface teaches through play.

A new player sees: a hand of cards, an enemy with a health bar, an icon showing its next move. Everything needed to act is visible. An expert sees the same screen and reads it as damage math, deck thinning probability, energy economy, relic synergies. The depth was always there. The UI just didn't force it on you before you were ready.

The game uses animation, pointer highlights, and immediate visual feedback to teach each mechanic at the moment you encounter it — not before, not after, not in a separate help screen.

The techniques:

**Enemy intent icons.** The enemy telegraphs its next action with a simple icon (sword for attack, shield for defend). Beginners read this literally. Experts use it to calculate optimal card sequencing across multi-turn combat. Same information, two levels of interpretation.

**The map.** A branching path with node icons: combat, elite, shop, rest, event. New players pick the path with fewer skulls. Experts read the map as a resource management puzzle — how much health can I trade for gold to afford the relic that enables my build? Same visual, different depth.

**Card tooltips on hover.** Beginners read them to learn what cards do. Experts hover to check exact numbers for damage math. No "simple mode" vs "advanced mode." The tooltip serves both because the information is layered: the name and art convey the concept, the text conveys the mechanics, the numbers convey the math.

**Ascension levels.** After winning, the game unlocks harder modifiers one at a time. Each ascension adds exactly one new constraint. This is progressive disclosure applied to difficulty — the game teaches you what "harder" means in increments, so you always understand what changed. App settings could learn from this: don't dump 50 toggles on a power user. Unlock complexity as they demonstrate they need it.

The lesson for product design: expert and novice don't need different interfaces. They need the same interface with information that rewards deeper reading.

### Provenance

These ideas have a literature. It just doesn't get read outside game design.

Raph Koster's *A Theory of Fun* (2004) made the foundational argument: fun is learning. Games are pattern-recognition machines. When the brain stops finding new patterns, it gets bored. This is the cognitive basis for progressive disclosure — not a UX heuristic, but a consequence of how brains work.

Jesse Schell's *The Art of Game Design* (2008) introduced over 100 "lenses" for evaluating a design, drawn from psychology, architecture, music, film, and mathematics. The lenses aren't game-specific. They apply to any experience where someone interacts with a system.

Steve Swink's *Game Feel* (2008) named "juiciness" — the excessive feedback that makes actions feel significant. Real-time control + simulated space + polish. This is why a button click in a well-made app feels different from the same button in a bad one. Swink formalized what the [transitions post](/life-is-in-the-transitions) calls temporal coherence.

Celia Hodent's *The Gamer's Brain* (2017) is the direct bridge. Hodent was UX director at Epic Games during Fortnite and has a PhD in cognitive psychology. She maps game UX to neuroscience — perception, attention, memory, motivation — and treats game interfaces as applied cognitive science. This is the book that takes game UI seriously as design research.

### The corruption

"Gamification" took the surface and missed the depth. Points, badges, leaderboards — the dopamine loop stripped of everything that made it work. No conveyance. No progressive disclosure. No effort calibration. No teaching through play. Just extrinsic rewards bolted onto interfaces that were already bad.

The term is so polluted that citing it hurts any serious argument about learning from games. The lesson was never "add game mechanics to apps." It was: games solved these problems first because players leave immediately if the interface fails. The discipline came from the constraint, not from the points.

### The agent instruction

When designing onboarding, task flows, or progress systems, check whether games solved the same problem. They usually did. The quest system alone provides a template: clear goal, calibrated effort, visible progress, chained rewards, one lesson per step.

Take the best lessons from the harshest design environment and transplant them onto everything else that can use them. Games can't survive on utility. Everything else can — which is exactly why everything else settles for worse UI.
