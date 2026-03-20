---
name: tighten
description: Compress each paragraph without losing argument. Cut filler, merge redundant sentences, shorten.
argument-hint: <file_path>
allowed-tools: Read, Edit, Grep, AskUserQuestion
---

# Tighten: Paragraph Compression

Compress every paragraph in a post. Preserve the argument; cut the slack. Do not fix anything until the user approves.

## Process

1. Read the file
2. Tighten every paragraph a bit. Apply directly. The qualifier "a bit" is load-bearing: compress conservatively, err toward keeping voice.
3. Readability pass: re-read the result for choppy runs. Where two or more consecutive short sentences share a subject or a causal relationship, join them with a conjunction ("and", "but", "so", "because", "which"), a semicolon, or a rhetorical question that bridges them. Tightening creates telegram prose; this pass restores flow. Only add conjunctions where the join is natural. If the staccato is intentional (landing a point, building rhythm), leave it.
4. Re-read. Report final word count vs original.

## What to cut

**Dead weight.** "The fact that", "in terms of", "there is/are...that", "it should be noted that", "essentially", "basically" → delete or restructure.

**Redundant modifiers.** If the adjective doesn't change the noun's meaning, cut it. "Completely eliminate" → "eliminate".

**Throat-clearing.** See /humanize for the full pattern list. Cut sentences that announce what the next sentence will say.

**Double-barreled phrases.** "Each and every" → "every". "First and foremost" → "first". Pick one.

**Passive → active.** "The playbook was updated by Grove" → "Grove updated the playbook". Keep passive only when the actor is unknown or irrelevant.

**Nominalizations.** "Make a decision" → "decide". "Provide an explanation" → "explain". Let the verb work.

**Hedge stacking.** One hedge per claim. Two hedges signal the writer doesn't believe their own sentence.

**Prepositional chains.** 2+ consecutive prepositional phrases is a compression opportunity.

## What to keep

**Voice.** Short punchy sentences that land a point. Fragments used for rhythm. The author's distinctive patterns. Compression should sharpen voice, not flatten it.

**Precision.** Technical terms, specific numbers, named examples. These are load-bearing. A tight paragraph with vague claims is worse than a loose paragraph with precise ones.

**Rhythm.** A paragraph that alternates long and short sentences has a pulse. Don't compress a long sentence that's earning its length by building momentum for the short sentence that follows.

**Transitions.** "But" and "therefore" are structural. Don't cut them. "However" can usually become "but". "Additionally" can usually be cut entirely (the new sentence is already additional by appearing).

## Targets

Aim for 10-20% compression on prose paragraphs. Tables, code blocks, and lists are already tight. If a paragraph is already under 30 words, leave it alone. If a paragraph is over 80 words, it's the highest-priority target.

## Dampener

Only propose cuts where the compressed version is clearly better. If compression loses nuance, rhythm, or voice, leave the paragraph alone. Report "already tight" and move on. The goal is fewer words carrying the same weight, not fewer words carrying less.
