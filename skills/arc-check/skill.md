---
name: arc-check
description: Break a blog post into beats, check the arc, flag problems, suggest fixes. Don't change anything until the user approves.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, Glob, AskUserQuestion
---

# Arc Check

Break a post into beats. Check the arc. Flag what's off. Suggest fixes. Always wait for human approval before changing the file.

## Prerequisites

1. **The user must provide arc direction.** Arc-check requires the human's intended pledge, turn, and prestige. If the user invokes this skill without specifying what the arc should be, or with incoherent direction, **reject the invocation.** Ask: "What's the pledge, turn, and prestige?" This is a Filter step: reject work that lacks human Attend.
2. **Commit before applying.** Before touching the file, commit its current state so the human can inspect the before/after diff and revert if needed.

## What to do

1. Read the file.
2. Break it into **beats** — the smallest unit of argument that stands alone (usually a paragraph, sometimes two). For each: `B{n} (L{start}-L{end}): {what this beat does}`. Label each beat however makes sense (claim, example, objection, mechanism, transition, whatever fits).
3. Read the beat sequence and write up what works and what doesn't.

   **Structure (whole arc):**
   - **Pledge / Turn / Prestige**: The **pledge** shows the problem. The **turn** reveals the insight. The **prestige** shows the world is different now. Does each act land? Is the turn surprising enough? Does the prestige feel earned?
     - A strong pledge doesn't prove the problem with data — it makes the reader feel what they already know.
     - If you have to convince them the system is broken, the pledge is weak.
     - Story and absurdity land harder than statistics.
   - **Arc**: does tension build and resolve? Does the reader feel the problem before getting the solution?
   - **Theme**: does the post stay on topic? Does any theme appear, disappear, then reappear without justification?

   **Local (beat-to-beat):**
   - **Transitions (therefore/but)**: every transition should be "therefore" (this follows) or "but" (this contradicts). Flag any "and then" — sequential without logical connection.
   - **Logic**: does each beat follow from the last? Does the reader need information they haven't been given yet? Could any beat be cut without breaking the chain?
   - **Gaps**: any logical jump where the reader has to fill in an unstated assumption?

   **Cross-cutting:**
   - **Repetition**: same idea in two beats — reinforcement or padding?
   - **Internal links**: do references to other posts appear at the right moment? Any premature references or missed connections?
   - **Internal contradictions**: does a claim in one beat conflict with another? Does a mechanism described early get violated later? Flag both beats and quote both sides. Includes contradictions with linked posts.
4. If the order should change, suggest alternatives. Show the new sequence, say what it fixes, say what it costs. If the current order is best, say so and move on.
5. On approval: rearrange, smooth transitions between moved sections, don't rewrite beat content. Re-read and flag anything that feels forced.

## Dampener

Only flag issues where the fix is clearly better than what's there. If it's a coin flip, leave it alone. A mediocre sentence that's in the right place beats a good sentence that creates a new transition problem.

Rank every finding by how much the post improves if you fix it. Report the top few. Ignore the rest. The goal is convergence: a second pass on a fixed post should find little or nothing.
