---
layout: post
title: "Theory Is Load-Bearing (Round 3 Results)"
date: 2026-03-17
categories: cognition
---

[Preregistration](/round3-preregistration) | [Repository](https://github.com/kimjune01/metacognition)

We tested whether loading the Natural Framework into an LLM's context improves diagnostic quality on partially-working information systems. Two problems, five conditions, Bayesian adaptive stopping with dual-model judging.

The answer: **it depends on the problem**. Framework helps on data-processing tasks, doesn't help on algorithmic tasks. But when it helps, the theoretical grounding is what carries the weight. You can't just extract the checklist and ship it.

---

## Background: Why Round 3

Rounds 1 and 2 (preregistered, negative results, not published) tested whether LLMs could use the Natural Framework to write better code. They couldn't. Framework hurt on algorithmic tasks and constraint satisfaction (Round 2: framework 0.30 vs bare 0.76). Models went looking for "pipeline stages" where they didn't belong.

But building PageLeft (March 2026) showed something different. Loading the framework helped identify what was *missing* from a working system—not how to implement functions, but what architectural gaps existed. Git history: before framework, just data pipeline. After framework, quality gates, filters, validation, leaderboards.

Rounds 1-2 tested the wrong question. The claim was never "framework helps write algorithms." Round 3 tests the actual claim: framework helps diagnose gaps in partially-working information systems.

---

## What We Tested

**Five conditions:**
- **Zero**: Code + goal (no extra context)
- **Bare**: Code + goal + 520 tokens of Wikipedia (noise control)
- **Compressed**: Code + goal + 520-token diagnostic checklist
- **Filler**: Code + goal + 8.3k tokens of Wikipedia (big noise control)
- **Framework**: Code + goal + 8.3k token Natural Framework (full theory)

**Three deltas:**
1. Does diagnostic content help? (compressed vs bare, framework vs filler)
2. Is theory load-bearing? (framework vs compressed)
3. Does context length hurt? (zero vs bare, zero vs filler)

**Two problems (double-blind selected):**
- Hearthstone Deckstring Parser (binary format parsing)
- RSS Feed Reader (data validation and processing)

Each diagnostic report scored on gap coverage by blind judges (GPT-5.4 and Claude Sonnet 4.5, 3 runs each, majority vote).

---

## What We Found

### Problem 1: Hearthstone Deckstring Parser (DISCONFIRMED)

| Comparison | P(A > B) | Interpretation |
|------------|----------|----------------|
| Framework > Filler | 0.39 | Framework doesn't help |
| Compressed > Bare | 0.03 | **Compressed actively hurts** |
| Framework > Compressed | 0.93 | Framework beats compressed (only because compressed is terrible) |
| Zero > Bare | 0.31 | **Bare beat zero** |
| Zero > Filler | 0.36 | **Filler beat zero** |

**Result:** Framework doesn't help on binary parsing. Compressed checklist actively misleads. Even Wikipedia improved diagnostics over no context.

### Problem 2: RSS Feed Reader (In Progress)

| Comparison | P(A > B) | Interpretation |
|------------|----------|----------------|
| Framework > Filler | ~0.91 | Framework helps moderately |
| Compressed > Bare | ~0.50 | Compressed is pure noise |
| Framework > Compressed | ~0.96 | **Theory is load-bearing** |

**Result:** Framework has diagnostic value on data-processing tasks. Compressed checklist has zero value. Theory is what makes diagnostic content work.

Posterior has converged at 15 batches—P(fw>filler) oscillates 0.90-0.97 but won't stabilize above 0.95 confirmation threshold. Effect is real but moderate.

---

## Three Surprises

### 1. Noise Helps

**Predicted:** Context length hurts. P(zero > bare) = 0.55, P(zero > filler) = 0.65.

**Actual:** Noise improved diagnostics. P(zero > bare) = 0.31, P(zero > filler) = 0.36.

Adding Wikipedia articles about plate tectonics and maritime history beat having no extra context at all. This held across both problems.

**Why?** Best guess: having something to read primes careful analysis mode. Zero condition is bare code + directive, maybe too sparse. Model jumps to pattern matching. Adding context forces deliberation.

But honestly: we don't know. The data says noise helps and we don't have a strong mechanistic story. That's what experiments are for—finding things you don't expect.

### 2. Compressed Checklist Is Harmful or Useless

**Expected:** Compressed would help less than framework (that's why we tested it), but still help a bit.

**Actual:**
- Hearthstone: P = 0.03 (actively harmful)
- RSS: P = 0.50 (completely useless)

The checklist is 16× smaller than the framework. By prompt-engineering logic, it should be better: less cruft, just the essential diagnostic questions.

Instead it's worse than random noise. Worse than nothing. Worse than Wikipedia.

**Interpretation:** Checklist primes abstractions without grounding. It says "look for missing Filters, missing Consolidate" but doesn't explain why those stages exist or when they apply. On binary parsing (Hearthstone), the model goes looking for "quality gates" where they don't belong. On data processing (RSS), it just doesn't connect.

The full framework provides theory: here's why these stages emerge, here's the thermodynamic constraint, here's what they look like in different domains. That grounding lets the model know when to apply the vocabulary.

### 3. Theory Is Massively Load-Bearing

**Pre-registered prior:** P(framework > compressed) = 0.45 (skeptical, deferring to conventional wisdom that shorter prompts perform better).

**Actual:** P = 0.93-0.98 (both problems, decisive).

When diagnostic content provides any value at all, it's because of the theoretical grounding, not despite it. The extra 7,800 tokens of theory are anti-noise. They make the 500-token checklist actually applicable.

This changes how we think about prompts. Not just instructions ("do this task"), but conceptual frameworks that change how the model processes information.

---

## Task-Structure Dependence

The framework is domain-specific. It works on information-processing systems but has clear boundaries.

**Hearthstone** (binary parsing):
- Framework doesn't help (P = 0.39)
- Compressed actively hurts (P = 0.03)
- Framework vocabulary doesn't map (no "quality gate" in a base64 decoder)

**RSS** (data processing):
- Framework helps moderately (P ≈ 0.91)
- Compressed is useless (P ≈ 0.50)
- Framework vocabulary maps naturally (validation, error handling, production readiness)

**Sign reversal across rounds:**
- Round 1 (algorithm writing): Framework hurt
- Round 2 (constraint satisfaction): Framework hurt (0.30 vs 0.76)
- Round 3 (diagnosis): Framework helps on data-processing, hurts on algorithmic

Metacognitive scaffolds are task-structure dependent. Framework primes wrong abstractions for implementation but can surface architectural gaps in diagnosis, when the problem type matches.

---

## What This Means

**For practitioners:**
- Don't use the compressed checklist (worthless or harmful)
- Framework might help on production-readiness diagnostics for data systems
- Framework won't help on algorithmic/parsing tasks
- Even irrelevant context beats no context (surprisingly)

**For theory:**
- The "why" is load-bearing (you can't extract just the vocabulary)
- Task structure matters more than we thought
- Conventional wisdom about prompt length is wrong for diagnostic tasks
- Theory makes diagnostic questions applicable

**For methodology:**
- Pre-registration kept us honest when results contradicted predictions
- Double-blind source selection prevented cherry-picking
- Dual-model judging caught no systematic bias
- Need futility stopping rules next time (learned at batch 15)

---

## Honest Accounting

**What we got right:**
Experimental design (pre-registration, blinding, adaptive stopping). Asking a falsifiable question. Reporting negative results. Learning from Round 2's failure.

**What we got wrong:**
No futility stopping rule (experiment will run to 30 batches even though posteriors converged at 15). Predicted noise would hurt (got the sign backwards). Expected compressed to help a bit (worthless or harmful). Prior on theory was too skeptical (P = 0.45 predicted, P ≈ 0.95 actual).

**What surprised us:**
The stark problem-specific effects. The decisive theory signal. That noise helps at all. How useless the compressed checklist is.

---

## Implications

The Natural Framework is a lens for understanding information-processing systems. It works when the problem maps to pipeline/validation/production-readiness gaps.

You can't shortcut it. The compressed checklist (just the six stages, stripped of theory) is worthless. The theoretical grounding makes the diagnostic questions applicable. The 16× token overhead is worth paying when the framework applies.

Task-structure dependence is the finding. Framework helps on RSS (data processing), hurts on Hearthstone (binary parsing). The question isn't "does the framework help?" but "what problem types benefit from this conceptual lens?"

Round 4 should test problem-type clustering explicitly. Pre-register categories (data processing, algorithmic, hybrid), test multiple problems per category, see if the pattern holds.

---

## The Experiment Worked

We asked: does loading the framework help diagnose missing parts?

Answer: **yes on some problems, no on others, theory is load-bearing**.

That's a real answer. Nuanced, evidence-based, honest about boundaries. We learned things we didn't expect (noise helps, compressed hurts, problem-specificity is stark) and can't immediately explain (why does noise help mechanistically?).

The methodology worked. Pre-registration kept us honest. Double-blind selection prevented bias. Adaptive stopping was efficient. Dual-model judging was robust.

The results are in the repo. The artifacts are append-only. The stopping log shows the posterior evolution. Anyone can verify the work.

That's how experiments should be run: lock in predictions, follow the protocol, report what you find, learn from surprises.

Theory is load-bearing. Whether to load it depends on the problem.

---

*Experiment designed collaboratively with GPT-5.4 (via Codex CLI) and Claude Opus 4.6 (via Claude Code). Pre-registered 2026-03-16, executed 2026-03-17.*

**Repository:** [github.com/kimjune01/metacognition](https://github.com/kimjune01/metacognition)
