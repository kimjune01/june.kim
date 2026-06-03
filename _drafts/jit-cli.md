---
variant: post
title: "JIT CLI"
tags: coding, methodology
---

*Builds on [Skills Lack Determinism](https://june.kim/skills-lack-determinism), [Don't LLM what you can code](https://june.kim/dont-lang-what-you-can-math), and [Memory Compression](https://june.kim/memory-compression).*

Agents hallucinate API surfaces. They invent function names, CLI flags, subcommands that don't exist. The conventional response is to suppress: tighter tool definitions, grounding, RAG, prompts that scold. The hallucinations are treated as a defect.

Invert. The hallucination is the spec.

When an agent reaches for `sweep drip checkup --repo X` and the command doesn't exist, the agent has just done unpaid design work. It predicted the verb-noun shape a reasonable user would expect. It ranked that shape by reaching for it. The reach is a vote. Multiple reaches across multiple runs are a ranked build queue, free.

You only have to log it.

### The bricks version

You're writing a skill markdown. The skill needs to push a PR, check open issues, read a queue. The natural move is to define the CLI first. `sweep drip push`, `sweep drip check`, `sweep retro params`. Then write the skill against the spec. Every command exists when the skill runs. Clean.

It's also bricks. You committed to CLI shape before the skill needed it. The flags you chose for `--repo`, `--branch`, `--test-cmd`, `--prompt` got picked from imagination, not from the friction of use. Half will reshape after first run. The other half won't be reached at all.

[Don't LLM what you can code](https://june.kim/dont-lang-what-you-can-math) said: don't bake conditionals into prompts. The dual: don't bake imagined CLI shapes into skills.

### The pottery version

Write the skill against the CLI you wish existed. If `sweep drip checkup --repo X` doesn't exist yet, write the skill calling it anyway. Make the harness log every missing reach. The most frequent missing calls *are* the build queue.

```bash
$ sweep drip nopebogus
Usage: sweep drip [OPTIONS] COMMAND [ARGS]...
$ sweep missing
# 1 distinct missing calls
  [  1×] sweep drip nopebogus
           reason: No such command 'nopebogus'.
```

The error path is the spec channel. [Skills Lack Determinism](https://june.kim/skills-lack-determinism) said: rules don't bind until they're code with error messages. Here the rule is *this affordance should exist*, and the binding is the log entry that proves an agent reached for it. The agent [closes the loop](https://june.kim/close-the-loop) by retrying, escalating, or routing around. Either way the harness owns the truth.

### Hallucination as profile

Most LLM design pipelines treat hallucination as noise to filter. JIT CLI treats it as profile data.

The model has a prior over what API the world should have. That prior comes from millions of CLIs it's seen during training. When it reaches for `sweep drip checkup`, it's drawing on every `npm audit`, `kubectl get`, `git log` it's ever seen, and predicting the shape that would fit the pattern. The prediction is grounded in distribution, not just imagination. That's why the hallucinations cluster around shapes that *would* be ergonomic if they existed.

Hallucinations of facts are still defects. Hallucinations of *affordances in a surface you own* are predictions worth harvesting. The distinction is who owns the truth. For facts, the world does, and the model can be wrong about it. For your CLI, you do, and the model's prediction is a vote you can choose to ratify.

The harvesting cost is one missing-calls log and a `sweep missing` reader. Both are trivial. The payoff is a CLI surface that grows from real demand without any of the spec-meeting overhead.

### The wish well

Implicit reaches carry syntactic signal: the shape of the call the agent imagined. They don't carry reasons. The agent was trying to do work, not file a feature request, so the harness only sees what got tried, not why.

Pair the implicit log with an explicit channel.

```bash
$ sweep wish "sweep drip cooldown-stats --repo X" \
    --reason "would help diagnose why drip is paused on a repo we expect activity from"
```

`sweep wish` files a deliberate request: the shape the agent wants plus the reason it wants it. Both channels feed the same wishlist; explicit votes weight more (3× per wish, 1× per reach) because a stated reason is signal the implicit channel can't carry.

The two channels answer different questions. *What did the agent try?* (implicit). *What would the agent build, and why?* (explicit). Neither subsumes the other. The shape that piles up implicit reaches is the high-frequency demand. The shape that earns one wish with a sharp reason is the high-leverage demand. Build for both.

LLMs are typically better at the explicit channel than the implicit one. They guess command shapes from distribution, sometimes plausibly, sometimes not. They articulate "I wish I could X because Y" almost always coherently. The wish channel routes around the syntactic-guess limitation by letting the natural-language reasoning land directly in the log.

### Why this is JIT

JIT compilers don't compile every code path ahead of time. They run the program, profile the hot paths, and compile those. Cold code stays interpreted. Warm code gets a baseline compile. Hot code gets aggressive optimization. Profile-guided optimization uses real call traces to decide what's worth specializing.

CLI growth maps onto every level.

*Cold.* The skill mentions a verb the agent rarely reaches for. Stays as markdown.

*Warm.* Agent reaches a few times. Wishlist surfaces it. You build a skeleton.

*Hot.* Agents reach often. You add flags, gates, error handling.

*Inline cache.* The wishlist log learns the common shape `(verb, options)` of each call site. Frequency ranks what to specialize next.

*Profile-guided.* The count is the profile. You don't guess what's worth building. The trace tells you.

*Deoptimization.* A JIT throws away specialized code when an assumption breaks. The pipeline's analog is eviction: affordances that stopped earning their keep get pruned.

Same structure, different altitude. JIT specializes hot code paths in a running program. JIT CLI specializes the verb shapes agents reach for.

### The deeper lineage

The JIT framing makes the mechanism legible. The principle is older.

Christopher Alexander watched buildings get used and noticed paths wore through the lawns where the architect didn't draw them. The right move was to pave where the wear was, not where the drawing said. *Form follows wear.* JIT CLI is the same operator on a different material. Agents wear paths through an affordance space. The harness logs the wear. You pave where the log accumulates.

Toyota called this kanban pull. Downstream stations emit cards when they want capacity. Upstream sends capacity to where the cards are. Missing-call log entries are the same cards.

[Memory Compression](https://june.kim/memory-compression) gives a third reading. Each level of the tower compresses repeated episodes. Manual edits become `/tighten`. Repeated skill sequences become `/copyedit`. JIT CLI is the same morphism applied to CLI verbs. Each repeated reach is an episode, three reaches is a pattern, the pattern compiles into a `sweep` subcommand. Watch yourself repeat. Compile the repetition. The "yourself" is the agent. The watching is automatic.

### The practical move

Write the skill markdown calling whatever verbs feel right. Don't strip out the ones whose CLI doesn't exist. Don't comment them with TODO. Don't add a "if the CLI doesn't exist yet" branch. Make the call.

When the call fails, the harness logs the call.

When the shape isn't even guessable but the need is, the agent files `sweep wish "..." --reason "..."` and the wish lands in the same wishlist with a 3× vote weight.

When you sit down to add capacity, read `sweep missing`. Build the top N. Re-run. The log refills with calls that became cold once the warm ones got built, plus new ones the skill discovered now that earlier reaches succeed.

The CLI grows from below. Agents demonstrate need by reaching or wishing. The harness logs both. You build what the demand names.

### What stays imagined

JIT compilation doesn't eliminate all ahead-of-time work. The interpreter, the instruction set, the calling convention all exist before the program can run at all.

JIT CLI has the same baseline. The harness's interception mechanism, the log format, the wishlist reader, the explicit wish writer. You build those once because nothing else can JIT until they exist.

After that, everything is reactive.

The harness is the substrate. The CLI is what grows on it. The skills are what call into it. The agents are who reach. Each layer up is more emergent than the layer below: rigid substrate, pliable affordances, dynamic calls, stochastic agents. Same shape as the [Natural Framework](https://june.kim/the-natural-framework). JIT is what links them.

---

*The first version of this post was drafted by [Claude](https://june.kim/double-loop), against a CLI that didn't fully exist when the conversation started. The wishlist filled itself up as we went.*
