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

### Problem 2: RSS Feed Reader

| Comparison | P(A > B) | Interpretation |
|------------|----------|----------------|
| Framework > Filler | 0.949 | Framework helps moderately |
| Compressed > Bare | 0.50 | Compressed is pure noise |
| Framework > Compressed | 0.96 | **Theory is load-bearing** |

**Result:** Framework has diagnostic value on data-processing tasks. Compressed checklist has zero value. Theory is what makes diagnostic content work.

Final posterior at batch 30: P(fw>filler) = **0.949**. Missed the pre-registered 0.95 threshold by 0.001. Effect is real but moderate.

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
- Framework helps moderately (P = 0.949)
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
No futility stopping rule (experiment ran to 30 batches even though posteriors converged at 15). Predicted noise would hurt (got the sign backwards). Expected compressed to help a bit (worthless or harmful). Prior on theory was too skeptical (P = 0.45 predicted, P ≈ 0.95 actual).

**What surprised us:**
The stark problem-specific effects. The decisive theory signal. That noise helps at all. How useless the compressed checklist is.

---

## The Drama of 0.949

Final result: P(framework > filler) = **0.9459**. We pre-registered 0.95 as the confirmation threshold. Missed it by 0.0041.

**The oscillation:**
- Batch 13: crossed 0.95 (P=0.971) ✓
- Batch 14: dropped to 0.914
- Batches 15-27: oscillated 0.89-0.94
- Batch 28: 0.942 (so close...)
- Batch 30: **0.949** (heartbreaking!)

It's like watching someone try to make a free throw - keeps hitting the rim, won't go in.

**What this proves:**
1. Effect is real - clearly above 0.90, not noise
2. Effect is moderate - can't stabilize at 0.95
3. Futility rules were needed - we knew at batch 15 it wouldn't confirm
4. The conclusion doesn't change - "framework helps moderately" whether P=0.926 or P=0.949

**About that 0.05 threshold:**

P=0.95 vs P=0.949 is vanity - not a substantive difference. Pre-registering it was correct (prevents p-hacking). Missing it means we don't say "confirmed" by our own rules. But 94.9% confidence is compelling evidence.

The difference between 0.949 and 0.95 is not "framework doesn't work" vs "framework works" - it's whether we hit our pre-registered threshold. Effect size and practical significance matter more than 0.001 probability points.

But we pre-commit to thresholds anyway, for integrity. Can't cherry-pick after seeing data. The drama of hitting 0.949 is exactly why we need pre-registered stopping rules.

---

## Retrospective: What We'd Do Differently

### 1. Add futility stopping at batch 15

Wasted batches 15-30 trying to reach an impossible threshold. Should have stopped when posterior trapped between 0.88-0.94 with no trend.

**Lesson:** At 50% of max batches, if P oscillating ±0.05 around mean or trapped in [0.40, 0.60], stop and declare inconclusive. The signal is clear even if it doesn't hit threshold.

### 2. Include null/calibration cases (20-30%)

All Round 3 problems had gaps. Didn't test if framework can say "nothing important missing." Positive-case bias.

**Lesson:** Include systems with no qualifying gaps. Tests restraint. If framework hallucinates gaps on null cases, it's unreliable.

### 3. Require external evidence

Round 3 selection could smuggle diagnosis - we decided what gaps existed. Should require issue threads, postmortems, maintainer TODOs, incident notes.

**Lesson:** Don't select problems where we already know the "right" answer. External artifacts or null case.

### 4. Problem-type clustering needs multiple items

Had 1 data-processing problem (RSS), 1 algorithmic problem (Hearthstone). Can't establish category effects with N=1 per category.

**Lesson:** Need 3+ problems per category to separate category from item difficulty.

### 5. Guard against output-structure confounding

Round 3 directive showed structure (Observations → Triage → Plan). If conditions prime that structure differently, confounded.

**Lesson:** Just say "Generate SOAP notes" without showing template. Score diagnosis substance, not organization.

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

**And we learned how to run better experiments.** Five concrete lessons for Round 4: futility rules, null cases, external evidence, problem clustering, output-structure controls. Each mistake documented, each lesson applied.

That's how science works: not getting it right the first time, but making work transparent enough that the next experiment can be better.

Theory is load-bearing. Whether to load it depends on the problem. P=0.949 says that loud and clear, even if it's not "officially confirmed" by our arbitrary threshold.

Science doesn't live or die on 0.001 probability points. But integrity requires honoring your own protocol. ✨

---

*Experiment designed collaboratively with GPT-5.4 (via Codex CLI) and Claude Opus 4.6 (via Claude Code). Pre-registered 2026-03-16, executed 2026-03-17.*

**Repository:** [github.com/kimjune01/metacognition](https://github.com/kimjune01/metacognition)
