---
layout: post
title: "Biotech Diagnosis"
tags: cognition methodology
---

*Part of the [cognition](/cognition) series. Pre-registration, data, and code: [github.com/kimjune01/universal-diagnosis](https://github.com/kimjune01/universal-diagnosis)*

Three predictions. Three biotech companies. One framework. Head-to-head with Martin Shkreli.

---

## The idea

Every biotech company is a learning loop for its molecule. The drug goes through trials. The company reads the results, decides what to change, and writes those changes back — new trial design, new endpoints, new manufacturing. That's the backward pass. The [Natural Framework](/the-natural-framework) calls it the consolidate stack.

Most analysts diagnose the drug: will it work? That's the forward pass. They look at a snapshot — this trial, this endpoint, this p-value. The framework diagnoses the trajectory: is the company learning? Is the same failure recurring? Is the consolidate stack functional?

Two companies can have identical Phase 3 results and opposite outcomes, depending on whether the company's backward pass is working.

But a functional consolidate stack is necessary, not sufficient. It also needs cache (cash) and runway (time). A company that reads its failures perfectly and knows exactly what to change is still dead if it can't fund the next iteration. Cash is the timer on a broken forward pass. The consolidate stack decides *what* to do next; the cash decides *whether* it gets to.

## The evidence

We diagnosed five companies from Shkreli's public positions. Two retrospective (outcome known), three prospective (outcome unknown). Four parallel search agents per company, two independent merges, mechanical scoring. [Pre-registered](https://github.com/kimjune01/universal-diagnosis/blob/master/prereg.md) before any diagnosis.

### Run 0: Retrospective (demonstration)

**CAPR (Capricor Therapeutics)** — Shkreli shorted. Said HOPE-3 "will not work."

The temporal graph tells a different story. Four iterations: ALLSTAR (MI, failed) → HOPE-1 (DMD, pivoted) → HOPE-2 (IV, signal) → HOPE-3 (Phase 3, confirmed). The company changed the indication, the delivery route, the dose, and the endpoints across four trials. The consolidate stack was functional. ALLSTAR's failure class (wrong indication) didn't recur.

Framework: **dying_pivoted, PASS.** Shkreli diagnosed a snapshot. The framework diagnosed a trajectory.

Result: HOPE-3 positive (PUL v2.0 p=0.029, LVEF p=0.041). Stock +440%. Shkreli admitted "bad call." **Framework correct.**

**QURE (uniQure)** — Shkreli was long. Sold November 2025.

AMT-130 topline was positive (cUHDRS 75% slowing, p=0.003). The drug works. But the FDA reversed its prior agreement on external controls — first privately (November 2025), then publicly, calling the data "distorted" and "manipulated" (March 2026). Stock -84%.

The temporal graph shows why: FDA published guidance in October 2022 explicitly discouraging external controls for neurodegenerative gene therapies. uniQure built their entire BLA strategy on external controls anyway. When the FDA enforced its own published rules, management fought back instead of pivoting. The read_outcomes pipe was broken — the company couldn't read regulatory signals it didn't want to hear.

Framework: **dying_dying.** Shkreli got out before the break, but for unrelated reasons. **Framework would have caught the trajectory.**

### Run 1: Prospective (real predictions)

These are live. Outcome unknown. Published March 20, 2026.

**SPRB (Spruce Biosciences)** — BLA submission for TA-ERT by December 31, 2026.

The molecule is mature (7 years, 22 patients, BTD). The company is new — acquired it from bankrupt Allievex after its own lead program failed. Consolidate stack is fragile (going concern, $48.9M cash) but functional (reading FDA feedback, hiring commercial leadership).

Framework: **dying_pivoted, PASS.** Shkreli: bull. We agree on direction, disagree on reasoning. He says "drug will be approved" (forward pass). We say "company is executing despite stress" (consolidate stack). The risk: PPQ batch slip → cash crisis. The molecule has outlived two prior companies.

**ATYR (aTyr Pharma)** — New sarcoidosis trial announced by September 30, 2026.

EFZO-FIT Phase 3 missed primary (steroid dose, p=0.33) but hit secondaries (KSQ-Lung p=0.048). The drug works on quality-of-life endpoints. The trial measured the wrong thing. FDA Type C meeting mid-April 2026.

Framework: **dying_pivoted, PASS.** Shkreli: bear ("really bad drug"). He's wrong on mechanism — the drug works, the endpoint was wrong. The framework predicts the company will pivot because the consolidate stack is functional: honest read of the miss, constructive FDA engagement, no panic pivot. Inverse of QURE — same kind of FDA pushback, opposite management response.

**INMB (INmune Bio)** — CORDStrom MAA to UK MHRA by September 30, 2026.

Both programs missed primaries (CORDStrom EBDASI p=0.15 favoured placebo; XPro1595 Phase 2 ITT miss). Both pivoting to secondaries. BLA already slipped 12 months. Going concern. CEO transition mid-crisis.

Framework: **dying_pivoted, FAIL.** Shkreli: bear. We agree on direction but for different reasons. He says the company is worthless. We say the consolidate stack rewrites narratives faster than it ships filings. The temporal pattern — primary miss → secondary salvage → timeline slip — predicts another delay. Both merge instances agreed unanimously.

## What the framework adds

An analyst looks at a drug. The framework looks at the company's learning loop.

| | Analyst view | Framework view |
|---|---|---|
| CAPR | Drug won't work (Shkreli) | Company is learning — trajectory predicts PASS |
| QURE | Drug works, buy (Shkreli) | Company can't read feedback — trajectory predicts collapse |
| ATYR | Drug is bad (Shkreli) | Endpoint was wrong, company will pivot |
| INMB | Company is worthless (Shkreli) | Pattern predicts timeline slip, not death |

The predictions are binary, timestamped, and mechanically scored. The reasoning is structural — which stack is broken, which pipe changed status, whether the same failure class recurred. No judgment calls in the scoring.

### Where we agree, we're more confident

This is the [blind-blind-merge](/blind-blind-merge) principle. When two independent systems — one diagnosing the forward pass (Shkreli), one diagnosing the backward pass (the framework) — arrive at the same direction from different reasoning, the convergence is stronger signal than either alone.

| Company | Framework | Shkreli | Agreement? | Confidence |
|---------|-----------|---------|------------|------------|
| SPRB | PASS | Bull | Yes | Higher — both say the molecule carries the company |
| ATYR | PASS | Bear | **No** | Framework's edge case — we disagree on mechanism |
| INMB | FAIL | Bear | Yes | **Highest** — independent convergence from different analyses |

INMB is our strongest call. The framework says "pattern recurrence, timeline slip." Shkreli says "worthless company." Different reasoning, same direction. ATYR is where we diverge — and that's where the framework is most tested.

The scorecard updates when catalysts resolve. ATYR and INMB by September 30, 2026. SPRB by December 31, 2026.

## Method

Each diagnosis: four parallel search agents (two forward pass, two backward pass), different data sources, semi-blind. Top two selected, merged independently by two instances of GPT-5.4 into SOAP notes. If merges disagree, first merge is primary. Human reviews but doesn't synthesize. [Full protocol](https://github.com/kimjune01/universal-diagnosis/blob/master/prereg.md).

The temporal graph is modeled as a sequence-based dynamic graph ([Peters et al., 2019](https://link.springer.com/article/10.1007/s00224-018-9876-z)). Each event is a public record with an archival date. The graph grows one event at a time. No pre-defined eras — the evidence builds the timeline.

The framework is the [Natural Framework](/the-natural-framework). The consolidate heuristic: check for trauma recurrence. `count(similar_failures) > 1` = broken consolidate stack.

---

## Hypothesis: vol mispricing from broken read_outcomes

The framework surfaces a second-order prediction that no analyst framework produces.

When the read_outcomes pipe is broken — management systematically overframes ambiguous data — the market's information about the company's information is wrong. Implied volatility is calibrated to management's framing. If the framing is systematically optimistic, expectations narrow, and any ambiguous outcome produces a larger surprise than the market prices. Realized vol should exceed implied vol around catalyst dates.

**Testable methodology:**
1. For each company, identify catalyst dates (trial readouts, FDA actions, earnings with pipeline updates)
2. Pull 30-day implied volatility from listed options before each catalyst
3. Measure realized volatility in the 5-day window around the catalyst
4. Compute the realized/implied ratio per event
5. Segment by framework diagnosis: broken read_outcomes vs. functional read_outcomes
6. Test: do companies with broken read_outcomes have higher realized/implied ratios?

**Qualitative evidence from this pilot:**
- **CAPR**: management said "no significant deficiencies" at mid-cycle review (May 2025). CRL two months later. Stock cratered. Realized > implied?
- **QURE**: management said FDA aligned on accelerated approval (December 2024). FDA reversed eleven months later. Stock -49% in one day, eventually -84%. Realized > implied?
- **ATYR**: management framed Phase 3 miss around secondaries in the same press release. Stock -83% in one day. Realized > implied?

The directional prediction isn't "stock goes up" or "stock goes down." It's "the surprise will be bigger than the market expects" — because the company's own self-assessment is unreliable. That's a long vol position, not a directional bet.

This is a hypothesis, not a finding. The backtest requires historical options data we haven't pulled. But the framework generates the hypothesis mechanically — any company diagnosed with broken read_outcomes is a candidate for vol mispricing around its next catalyst.

---

*Scorecard will be updated at [github.com/kimjune01/universal-diagnosis](https://github.com/kimjune01/universal-diagnosis) as catalysts resolve.*
