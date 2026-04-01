---
variant: post
title: "Memory Compression"
tags: cognition, methodology
---

*Sequel to [Functor Wizardry](/functor-wizardry). Builds on [The Parts Bin](/the-parts-bin) and [Volley](/volley).*

[Functor Wizardry](/functor-wizardry) said I'm the consolidation loop. I read episodes, decide what generalizes, write the procedural post. The cron job is me. That was true. It's becoming less true. Here's how.

### Watch yourself repeat

You edit a blog post. You cut filler, tighten sentences, check rhythm, add hyperlinks. You do it again on the next post. And the next. By the fourth post you notice you're doing the same four operations in the same order. So you write them down: humanize, tighten, readability, flavor. Four skills. Each one is a compressed memory of what you did manually — the episode became a procedure.

Then you notice you always run the four in sequence, send to codex for review, and loop until nothing changes. So you write `/copyedit`, which composes them all and loops to convergence.

| Level | What you did | What you compiled |
|-------|-------------|-------------------|
| 0 | Manual edits | — |
| 1 | Repeated manual patterns | `/humanize`, `/tighten`, `/readability`, `/flavor` |
| 2 | Repeated skill sequences + review loops | `/copyedit` |

Same morphism at every level: watch yourself repeat, compile the repetition. Each level discards the context of the level below and keeps only the pattern. Lossy at every step — the losses are what doesn't generalize.

### The SOAP pipeline

The same thing happened with diagnosis.

I diagnosed [Soar](/diagnosis-soar) manually. Read papers, grepped the repo, mapped components to framework roles, identified gaps, prescribed algorithms from the Parts Bin. That was level 0.

The episodes repeated. Every diagnosis started with reading sources and translating vocabulary. So I wrote `/intake`. Every diagnosis continued with mapping roles and finding gaps. So I wrote `/diagnose`. Every diagnosis ended with consulting the Parts Bin. So I wrote `/prescribe`. Level 1 — three skills compiled from repeated manual patterns.

The skills run in sequence, producing a growing SOAP document:

```
/intake  → S.md (Subjective: what the system says about itself)
/diagnose → O.md + A.md (Objective + Assessment: role mapping, gaps, causal chain)
/prescribe → P.md (Plan: candidate algorithms, triage tiers)
```

The first end-to-end run was the Soar demo. The pipeline found "Consolidate missing → Perceive throttles" without reading the manual diagnosis. But the skills changed during the run. One elicitation answer — "flat mappings are too coarse" — changed the Diagnose spec mid-pipeline:

**Before:** Diagnose mapped each term to a flat role. "Procedural memory = Remember."

**After:** Diagnose maps each term to a role *at a specific stack level*. "Procedural memory = Remember @ Consolidate." A role can be present at one level and missing at another — that's how compound failures hide.

The episode (flat mappings failed) compressed into a procedure change (tower-aware mappings). Four updates like this in one demo. Each one was the same morphism: the skill failed, I noticed the gap, I changed the spec. The pattern ("coverage questions can change downstream specs") is now in the Intake spec. Next time, the skill handles it.

Forge went further. Volley → Merge → Volley was a manual sequence. It became `/forge`. Forge doesn't have a blog post. The episode compressed directly into a procedure, skipping the semantic write-up. This post is the semantic layer catching up to what the procedural layer already compiled. Procedures form faster than explanations.

### Fan-out

When sources are thin — one README and a repo instead of forty years of papers — Intake used to grope in the dark. The manual pattern was: read the code, read the issues, check the Parts Bin for a matching algorithm. Three reading strategies, applied sequentially, often redundantly.

Watching that repetition produced a fan-out step inside Intake. Three parallel agents (code, intent, pattern), shared memory via S.md so they don't duplicate searches, codex filters contradictions, dead ends get structured tombstones. The human only resolves what the agents couldn't.

Fan-out compresses the human's judgment. Instead of resolving fifteen ambiguous mappings, the human resolves five — the rest were obvious once three perspectives converged. The compression is in what the human *doesn't* have to do.

### What you get

A diagnostic pipeline that runs on foreign systems:

1. **`/intake`** reads sources, translates vocabulary, fans out on thin coverage, files claims, then elicits human judgment on ambiguous mappings. Output: `S.md`.
2. **`/diagnose`** builds a tower table (role × stack level), draws architecture SVGs, substantiates every mapping against code, traces causal chains between gaps. Output: `O.md` + `A.md`.
3. **`/prescribe`** consults the Parts Bin, evaluates candidates against the system's constraints, and triages by urgency — critical (stop the bleeding), structural (enable healing), rehabilitative (long-term health). Output: `P.md`.

Every level of the stack needed the [same contracts](/functor-wizardry) to compose. I didn't add them because the theory said to. I added them because the skill kept breaking without them.

### What's next

The diagnostic stack is one level deep. The SOAP orchestration — run intake, then diagnose, then prescribe, gating checkpoints — is still manual. That's the next compression target.

The raw material is accumulating. `/worklog` appends a timestamped entry after every session — the episodic store, growing. The Soar demo produced twenty worklog entries across two days. The diagnostic skills improved four times from those entries. But I'm still the one reading the log, noticing the pattern, and updating the skill. The epmem exists. The compression doesn't run yet.

That's where Soar was. Three stores, all functional, no consolidation loop. The episodes accumulated. The patterns were in there. Nobody wrote the cron job. And Consolidate is the hardest contract to fulfill — for reasons that deserve their own post.

---

*Written via the [double loop](/double-loop).*
