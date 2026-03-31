# Fan-out: Diverge, Converge, Extend

Generate k hypotheses in parallel, volley each with codex to convergence, prune the failures, extend the survivors.

## When to use

When the problem has multiple plausible approaches and you don't know which one will land. Research questions, theorem attempts, design alternatives, architectural choices.

## Process

1. **Fan out.** Launch k Claude subagents in parallel, each exploring a different hypothesis, approach, or formulation. Each gets the same context and a distinct angle. Use `run_in_background: true` for all.

2. **Converge.** For each subagent result, volley it to codex for adversarial review:
   ```
   cat <<'PROMPT_EOF' | codex exec -
   [result + "Is this correct? Is this novel? Is this trivial? What breaks it?"]
   PROMPT_EOF
   ```
   If codex finds issues, fix and re-volley. Two rounds max per candidate.

3. **Prune.** Kill candidates that:
   - Codex proved wrong
   - Codex showed are known results under new names
   - Failed to produce a concrete statement after two rounds
   Report what died and why. The failures are information.

4. **Extend.** Take the survivors and launch a second fan-out: deeper computation, adversarial edge cases, generalization attempts. Each survivor gets its own subagent. Repeat the converge/prune cycle.

5. **Report.** Present the surviving results ranked by novelty and strength. Include the pruning log so the human can see what was tried and rejected.

## Shared memory

Fan-out subagents share a **research log** (specified by the user or defaulting to `_drafts/{topic}.md`). The log borrows structure from `/synopsis`: claims filed with provenance, convergent evidence merged, dead ends preserved.

Format each entry as:
```
### H{n}: {hypothesis name} ({model}, {status})

**Verdict:** {one line}

**Claims:**
- {claim} [{provenance: subagent model, codex round if validated}]
- {claim} [{provenance}]

**Dead if applicable:** {cause of death, which codex round killed it}

**Open questions:** {follow-ups the human hasn't addressed}
```

Rules:
- Each subagent reads the current log before starting. Later subagents see earlier findings.
- When a subagent produces a result, write it to the log immediately.
- **Convergent evidence:** if two subagents independently reach the same claim, note the convergence. That claim is stronger.
- **Contradictions:** if two subagents contradict, note the contradiction and flag for human Attend.
- The log is the deliverable. A reader should reconstruct the full funnel from it alone.

## Rules

- Claude generates, codex filters. Never reverse the roles.
- Use `model: "opus"` for fan-out subagents (hypothesis generation is judgment, not bulk work). Use codex for convergence (adversarial filtering).
- Each subagent gets a concrete, computable task. "Explore this direction" is too vague. "Compute this quantity on this example and check whether it matches this prediction" is right.
- Never suppress failures. A well-characterized dead end is worth more than an untested hypothesis.
- The human Attends between cycles. Present the prune results and let them redirect before the next fan-out.
- Label every claim's provenance: which subagent generated it, which codex round validated it.
- Two fan-out/prune cycles max per invocation. More than that and the context gets stale.

## The funnel property

The fan-out tree is a funnel, not an explosion. Each verification cycle prunes branches and lowers σ² on the survivors. Breadth shrinks, depth grows. After n cycles with survival rate p, you have k·pⁿ branches — geometrically decaying toward convergence. The telescope narrows as it lengthens.

This means:
- Cycle 1 should be broad (k=3-5) and shallow (concrete but quick computations)
- Cycle 2 should be narrow (survivors only) and deeper (adversarial edge cases, generalization)
- If a verification step is mechanizable (e.g., computing a cycle sum, checking a bound), the subagent can auto-prune without human Attend
- If a verification step requires judgment (is this interesting? is this the right question?), stop and present to the human
- The session is done when branches stop surviving or the human redirects

## Parameters

- `k`: number of parallel hypotheses (default 3)
- `depth`: number of fan-out/prune cycles (default 1, max 2)
- `adversarial`: whether to run codex in adversarial mode or sniff mode (default adversarial)

## Example

```
/fan-out k=3 "What is the right cut notion for tropical sheaves on event graphs?"
```

Launches three subagents:
1. Path-capacity cut
2. Potential barrier / distance-decorated separator
3. Equalizer/coequalizer formulation

Each result volleyed to codex. Survivors extended with harder examples. Failures logged with exact obstruction.
