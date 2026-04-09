---
name: sharpen
description: Rewrite lazy hedges as bold narrow claims. Converges under repeated application.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep
---

# Sharpen

Rewrite lazy hedges as bold narrow claims. Leave the real ones alone.

A lazy hedge is a soft word standing in for a limit the writer could have named. "A surprising fraction of X." "One important slice of X." "Arguably X." Places where the writer could have said exactly who, what, when, or how, and instead said *sort of*. /sharpen finds those and rewrites them. It does not touch hedges that carry real uncertainty or preserved scope.

Why the skill exists: when codex catches an overclaim, the instinctive fix is to stack qualifiers, and stacked qualifiers turn prose to mush. The right move is to narrow the claim *and* state the narrow version boldly, letting concrete examples do the fence-work. See [feedback_narrow_and_bold.md](~/.claude/projects/-Users-junekim-Documents-june-kim/memory/feedback_narrow_and_bold.md).

## Principles

**Converges under repeated application.** Same monoidal contract as humanize and tighten: a finite pattern set, rewrite rules that do not regenerate what they consume, a scalar norm (the hedge count from the pattern list) that tracks progress across passes. `sharpen(sharpen(x)) == sharpen(x)` after at most two passes.

**The narrow-preserving invariant is the single rule.** Every rewrite must preserve or tighten the scope of the claim. None may widen it. If no rewrite shape fits without widening, leave the hedge alone.

**A little hedging is OK.** The fixed point is a non-zero floor, not hedge-free prose. Real uncertainty earns a hedge. The skill's job is to clean the *lazy* ones, not to flatten every soft word.

**If unsure, leave alone.** Borderline cases are what the user is for. A successful run is "rewrote 6 obvious lazy hedges, left 9 borderline ones alone."

## Pattern list

**Soft quantifiers:** "a surprising fraction of," "a lot of," "some of," "much of," "most of what X is about."

**Category-introducing softeners:** "one important slice of X," "one recurrent failure mode in X," "one of the failure modes of X."

**Epistemic softeners:** "arguably," "perhaps," "it could be said that," "in some sense," "mostly," "roughly," "somewhat" (when damping rather than expressing a degree).

**Superlative softeners:** "one of the most X ever" with no comparison, "extraordinarily X" with no support.

**Structural throat-clearing:** "it is often the case that," "it is important to note that," "it is worth mentioning that."

**Not on the list (leave alone):** contrastive narrowings ("not X. Y."), named fence examples ("Sweden, for example..."), scoped conditionals ("when X is Y, Z"), mathematical qualifiers ("at most α," "up to rounding"), citation hedges ("the paper argues that X"), genuine first-person uncertainty marks, and hedges inside a paragraph whose narrowing is already doing heavy lifting.

## Rewrite shapes

- **Restructure into a declarative.** Fold the narrowing into a sentence whose scope is defined rather than qualified. *"A surprising fraction of methodological disasters are type errors"* → *"When a published finding is confidently wrong rather than just noisy, the failure is almost always a type error."*

- **Example as fence.** Replace the adverb with a specific named case. Names are stronger fences than adverbs because they are verifiable. *"Many governments reached for curve-fitting"* → *"The IHME team's early model was a curve-fitting exercise; Imperial Report 9 was not."*

- **Narrow-then-declare.** Explicit negation of the wider claim, then the bold narrow version as a separate sentence. *"Most of what gets called alignment is this problem"* → *"AI alignment is broader than this. The failure mode that connects most directly to this essay is type-mismatch at scale."*

## Report

Counts, not narratives. Hedges before, hedges after, rewrites applied, hedges left alone with one-line reasons.
