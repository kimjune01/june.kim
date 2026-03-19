# Consolidation Harness Weaknesses

*Observations from 2026-03-18 consolidation run (1089 turns, 13,497 actions)*

## The Core Problem

The harness extracts **procedural patterns** (tool sequences) but not **conceptual patterns** (reusable heuristics). It finds "what tools were used" but not "what problem was solved."

## Evidence from Round 4 Consolidation

**Candidate #1:** `Read(.md) → Edit(.md) → Edit(.md)` (35×, 16 sessions)
- Too simple to be useful: it's just "make two edits"
- No intellectual compression - this is Cache-level labor, not Filter-level craft
- Already automated: "read before editing" is in CLAUDE.md

**Candidates #2 & #3:** Go development workflows (15-100+ steps)
- Too context-specific: entire session traces, not generalizable patterns
- Cache-level logs, not Attend-level heuristics
- Can't extract from these: "what makes Go development effective?"

**Top intents:** `[yes]`, `[push]`, `[think]`, `[sy + diagnostic + evaluating]`
- Shallow keywords, not problem frames
- Single-word continuations lose context from prior turn
- TF-IDF on prompt tokens helps but isn't sufficient

## What's Missing

Successful skills encode **compression craft**:
- `tighten`: fixed-point convergence, filler detection, argument preservation
- `humanize`: AI tic patterns, negative parallelisms, monotonous rhythm detection
- `arc-check`: pledge/turn/prestige, transition detection, beat analysis

These are **conceptual**, not procedural. They answer "what makes writing good?" not "what tools did I use?"

## Why This Happens

Current pipeline:
1. Extract action sequences (tool calls)
2. Cluster by similarity (edit-edit-edit vs write-bash-bash)
3. Rank by frequency

This finds **what you did repeatedly**, not **what heuristics you applied repeatedly**.

What's needed:
1. Extract problem frames from prompts ("make this tighter", "check the arc", "find AI slop")
2. Extract solution strategies from tool calls + outcomes
3. Cluster by conceptual similarity (both solve "verbosity" even if one uses Edit and one uses Write)
4. Encode as testable heuristics (not tool sequences)

## Remaining Weaknesses (Known)

From MEMORY.md:
> Remaining weakness: single-word continuations ("yes", "fix") lose intent from previous turn. Needs turn chaining in extract.py.

Turn chaining helps but isn't sufficient. Even with full turn context, extracting "I said yes to this specific edit" doesn't produce "here's when to make this kind of edit."

Need: **problem → approach → outcome** triples, not just **tool → tool → tool** sequences.

## Hypothesis

The harness is solving the wrong problem. It's asking:
- "What tool sequences repeat?"

Should be asking:
- "What decision heuristics repeat?"
- "What problem-solution patterns recur across different tool sequences?"
- "What makes an effective diagnosis / edit / refactor / explanation?"

Tool sequences are the **implementation** of intellectual work. Skills should compress the **strategy**, not the implementation.

## Open Questions

1. Can you extract conceptual patterns from tool sequences? Or do you need explicit problem statements?
2. How do you test if a skill candidate encodes reusable heuristics vs session-specific labor?
3. What's the right granularity? `tighten` is ~500 tokens of craft. Candidates #2/#3 are 100+ steps.
4. Is frequency the right metric? Or should rare-but-high-value patterns rank higher?
5. Do you need human curation (user marks "this was good intellectual work, learn from it")?

## Next Steps

- Don't implement any of these three candidates (not Filter-level work)
- Consider: should harness extract from skills themselves? (tighten, humanize already encode the craft)
- Consider: explicit "mark this for learning" command during sessions?
- Consider: problem-first extraction (tag intents with problem frames, not just keywords)

## See Also

- MEMORY.md: "Division of intellect, not labor. Labor is Cache. Intellect is Attend."
- MEMORY.md: "Skills should automate Filter-level work (reject what's wrong). Producing what's right requires Attend — that stays with the human."
- theory-is-load-bearing.md: Theory is load-bearing (P≈0.95), can't compress to checklist without losing effectiveness
