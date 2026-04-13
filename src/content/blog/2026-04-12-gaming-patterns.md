---
variant: post-wide
title: "Gaming Patterns"
tags: design
---

Reference companion to [Game UI Lessons](/game-ui-lessons). The argument is there. The patterns are here.

### Rosetta stone

The same concepts exist in both worlds. Different vocabulary.

| Game design | SaaS/product design | What it actually is |
|---|---|---|
| Conveyance | Discoverability / affordances | Interface communicates what to do without instruction |
| Quest | Onboarding flow / checklist | Scoped task with clear goal and reward |
| Aha! moment | Aha! moment | One term that survived the crossing |
| Activation | Activation | Same |
| Progressive disclosure | Progressive disclosure | Same, but games do it through play, apps do it through UI patterns |
| XP / level up | Completion metrics / milestones | Visible progress toward mastery |
| Quest chain | User journey / funnel | Sequenced tasks where each unlocks the next |
| Breadcrumb quest | Contextual guidance / tooltips | Nudge toward the next action at the moment of need |
| Hub-and-spoke | Task dashboard / home screen | Central location with multiple available actions |
| Difficulty curve | Effort calibration | Matching task complexity to user skill |
| Juiciness / game feel | Microinteractions / polish | Excessive feedback that makes actions feel significant |
| HUD | Dashboard / status bar | Persistent information overlay |
| Cooldown indicator | Progress indicator / loading state | Visual countdown until action is available |
| Enemy intent icon | System status / preview | Telegraphing what happens next |
| Ascension / New Game+ | Power user features / admin mode | Unlocking complexity after demonstrating mastery |
| Tutorial level | First-run experience | Controlled environment that teaches by doing |
| Inventory | File manager / inbox / project board | Spatial management of many items |
| Loot / reward popup | Success state / confirmation | Immediate feedback on completion |
| Respawn / checkpoint | Undo / autosave / error recovery | Safe reversal of mistakes |

The SaaS world independently arrived at many of these through analytics and A/B testing (see [Userpilot's Product Adoption School](https://userpilot.com/product-adoption-school-userpilot/)). Games got there first through player behavior and survival pressure.

### Conveyance

Game design has a word that product design lacks: *conveyance*. It means: how the interface communicates what you can do, should do, and just did, without explicit instruction.

The `!` above a WoW quest giver is conveyance. The damage number that flies off an enemy in Slay the Spire is conveyance. The weak enemy placed next to a Dark Souls bonfire is conveyance. The cooldown overlay filling back up on an ability is conveyance. The XP bar ticking upward after a kill is conveyance.

Product design calls these things "affordances," "feedback," "discoverability," "onboarding." Game design calls them all one thing because they serve one function: the player should never have to ask "what just happened?" or "what do I do next?" If they do, conveyance failed.

The difference between a game with good conveyance and one without it is the difference between an interface that teaches through use and one that requires a manual. Every pattern below is a conveyance pattern. Some convey available actions. Some convey progress. Some convey state. All of them answer questions the user didn't have to ask.

### The quest system

WoW's quest system is the gold standard for onboarding. Not because it's fun (though it is), but because it solves every conveyance problem that app onboarding gets wrong.

**Goal clarity.** "Kill 10 boars" is unambiguous. The quest log tracks progress with a counter. You always know what's done and what's left. Most app onboarding says "set up your profile" with no indication of scope, progress, or completion.

**Effort calibration.** Each quest is scoped to 5-15 minutes and matched to your current level. The difficulty curve is tuned so you're never overwhelmed and never bored. App onboarding dumps everything at once (connect your accounts, invite your team, customize your dashboard, watch a tutorial) with no sense of ordering or effort.

**Conveyance.** The quest giver has a `!` above their head. The minimap shows objective markers. Breadcrumb quests lead you to the next hub. You never have to ask "where do I go?" Most apps drop you on a dashboard after signup and hope you figure it out.

**Chaining.** Finishing one quest unlocks the next. The chain creates momentum. You're always one step from the next reward. App onboarding has no chain. After the setup wizard, you're on your own.

**Dopamine.** Completion sound, XP bar animation, reward popup. The feedback loop is instant and specific. App onboarding either ends silently or shows a generic "You're all set!" with no sense of what you just achieved.

**Progressive disclosure.** Early quests teach one mechanic at a time. "Talk to this NPC" teaches navigation. "Use this ability" teaches combat. "Craft this item" teaches the crafting system. Each quest is a single lesson. App onboarding tries to teach everything in a tooltip carousel that nobody reads.

**Hub-and-spoke.** Quest hubs give you 3-5 quests at once, all in the same area. You batch related tasks efficiently and return for rewards. The pattern maps directly to a task dashboard, but most dashboards lack the spatial grouping and the return-for-reward loop.

### Patterns that crossed over

**Cooldown indicators.** Circular progress overlays on abilities, showing when an action becomes available again. Now ubiquitous outside games: Uber's driver ETA, food delivery tracking, upload progress. Games formalized the pattern; apps borrowed it.

**HUD minimalism.** Breath of the Wild hides interface elements when you're not using them. The HUD fades in on demand. [Signal-to-noise](/gui-before-computers) applied to temporal visibility: show information when it's relevant, hide it when it's not. Most apps show everything all the time.

**Tutorialization through environment.** Dark Souls teaches mechanics through level design, not text. A weak enemy near a bonfire teaches you combat safely. A narrow bridge teaches you about falling. The environment *is* the tutorial. The equivalent in apps: design the first-run experience so the interface teaches itself through use, not through overlays.

**Health bars and progress visualization.** Games perfected showing "how much is left": health, mana, XP, durability, cooldowns. Every progress bar, loading indicator, and completion percentage in product design descends from this. Games had to get it right because the player dies if they misread it.

**Inventory management.** Diablo's grid system, Resident Evil's tetris inventory. Spatial reasoning problems turned into UI. The lesson: when users manage many items, give them a spatial metaphor, not just a list.

### Novice-to-expert in one interface

Slay the Spire never explains itself. It demonstrates. The first combat has no tutorial overlay, no tooltip carousel. You draw cards, you see energy, you drag a card onto an enemy, a damage number flies off. The interface teaches through play.

A new player sees: a hand of cards, an enemy with a health bar, an icon showing its next move. Everything needed to act is visible. An expert sees the same screen and reads it as damage math, deck thinning probability, energy economy, relic synergies. The depth was always there. The UI just didn't force it on you before you were ready.

The game uses animation, pointer highlights, and immediate visual feedback to teach each mechanic at the moment you encounter it. Not before, not after, not in a separate help screen.

**Enemy intent icons.** The enemy telegraphs its next action with a simple icon (sword for attack, shield for defend). Beginners read this literally. Experts use it to calculate optimal card sequencing across multi-turn combat. Same information, two levels of interpretation.

**The map.** A branching path with node icons: combat, elite, shop, rest, event. New players pick the path with fewer skulls. Experts read the map as a resource management puzzle — how much health can I trade for gold to afford the relic that enables my build? Same visual, different depth.

**Card tooltips on hover.** Beginners read them to learn what cards do. Experts hover to check exact numbers for damage math. No "simple mode" vs "advanced mode." The tooltip serves both because the information is layered: the name and art convey the concept, the text conveys the mechanics, the numbers convey the math.

**Ascension levels.** After winning, the game unlocks harder modifiers one at a time. Each ascension adds exactly one new constraint. This is progressive disclosure applied to difficulty — the game teaches you what "harder" means in increments, so you always understand what changed.
