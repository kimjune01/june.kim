# Results

## Resolution of the five fully admitted claims

| Claim | Result | Evidence in next 10-K |
|---|---|---|
| UPS domestic volume trajectory | Unresolved | The annual filing reports a full-year decline and describes Q3 recovery after labor negotiations, but does not reproduce a quarterly growth sequence sufficient to test both halves of the compound claim. |
| UPS domestic fuel-surcharge revenue falls | Stood test | UPS reports 2023 fuel-surcharge revenue decreased by $1.0 billion. |
| UPS international volume trajectory | Unresolved | The annual filing reports full-year domestic and export volume declines, but not enough quarterly values to test H1-negative plus H2-improvement as specified. |
| One FedEx fully implemented in June 2024 | Reformulated / partial | The next filing says “full legal implementation” was effective June 1, 2024, while also saying network integration and optimization were ongoing. The original “full implementation” did not distinguish legal from operational completion. |
| FedEx begins new segment reporting in Q1 FY2025 | Stood test | The next filing states that Federal Express and FedEx Freight constitute the reportable segments beginning in Q1 FY2025. |

Result: **2 stood, 0 cleanly failed, 1 was reformulated/partially resolved, and 2 were unresolved.** This is too small for inference, but enough to expose flaws in the first rubric.

## Descriptive checks on non-admitted claims

- FedEx forecast FY2024 capital expenditures of “approximately $5.7 billion”; actual expenditures were $5.176 billion, an error of -$524 million (-9.2%). With no ex-ante tolerance, this cannot honestly be called true or false.
- FedEx forecast FY2024 business-optimization costs of “approximately $500 million”; actual costs were $582 million, an error of +$82 million (+16.4%). Again, “approximately” prevents adjudication.
- FedEx said FY2024 operating income would improve because of DRIVE. Operating income did improve and management repeated the DRIVE attribution, but repetition by the claimant is not an independent causal test. Only the outcome component stood.
- The next FedEx 10-K did not separately resolve the forecast of approximately $275 million in annualized European-realignment savings beginning in FY2024.

## What the pilot changed

The original four-part admission rule was too permissive. A later public filing being *capable in principle* of resolving a claim is not enough. The revised rule should require:

1. a named observable;
2. a numeric boundary or unambiguous categorical outcome;
3. a deadline;
4. a named disclosure and cadence already known to report the observable; and
5. an identity rule preventing the observable or project scope from being renamed at resolution.

Compound claims should be split before admission. Causal claims require evidence independent of management's repeated attribution.

## Cheapest next decisive test

Before testing returns, have two independent coders apply the revised admission rule to the same 50 candidate sentences. If agreement is poor, the score is not yet a trustworthy instrument. If agreement is high, estimate whether low-admission firms subsequently have more forecast misses or claim reformulations than high-admission firms, controlling first for simpler textual baselines.

---

# Reliability extension

## Method

We then selected 50 sentences with a fixed seed (`20260902`) from the 2023-filed 10-Ks of UPS, FedEx, and J.B. Hunt. A deterministic text filter found sentences containing forward-looking markers; balanced sampling selected 17 FedEx, 17 J.B. Hunt, and 16 UPS sentences. This is a sample of *candidate* claims, not all prose and not a representative estimate of filing-wide prevalence.

Two independent coders classified every sentence on eight binary fields without seeing each other's work. The strict admission rule required an empirical forward claim, observable, boundary, deadline, known resolution source, and stable identity.

## Independent agreement

| Field | Raw agreement | Cohen's kappa |
|---|---:|---:|
| Empirical claim | 88% | 0.76 |
| Forward claim | 96% | 0.92 |
| Observable | 82% | 0.58 |
| Boundary | 76% | 0.54 |
| Deadline | 100% | 1.00 |
| Known resolution source | 88% | 0.69 |
| Identity stability | 88% | 0.50 |
| **Final admission** | **96%** | **0.81** |

Both coders admitted six sentences, disagreeing on only two final labels. However, agreement alone concealed one shared rubric violation: both admitted an amortization forecast qualified by “approximately,” even though the rule explicitly rejected unbounded approximations.

We clarified three rules and independently recoded the affected items:

- `approximately`, `around`, and `about` fail without a numeric tolerance;
- `persist` and `continue` fail unless the comparison level and required duration are stated;
- stable identity requires the same metric label/unit or an immutable counted event.

Both coders then rejected all three affected items. The final conservative intersection contains four admitted claims: 4/50 candidate sentences (8%; Wilson 95% interval 3.2%–18.8%) and 4/25 sentences both coders recognized as forward claims (16%; 6.4%–34.7%). These intervals describe this fixed pilot sample only.

## Resolution of the four conservatively admitted claims

| Company | Frozen claim | Result | Later disclosure |
|---|---|---|---|
| UPS | Fuel prices decrease in 2023 | Stood | UPS reported decreases in jet fuel, diesel, and gasoline prices. |
| FedEx | Make $800 million of voluntary pension contributions in FY2024 | Stood | FedEx reported $800 million of FY2024 voluntary contributions. |
| UPS | Transition-services revenue declines in 2023 | Stood | UPS reported a $386 million reduction. |
| UPS | Retire six MD-11 aircraft from operational use during 2023 | **Failed** | UPS reported only two retired by December 31, 2023, then anticipated nine more in 2024. |

Three of four claims stood and one failed. The 75% survival rate has a Wilson 95% interval of 30.1%–95.4%, far too wide to support a population claim or trading inference.

## Reasonable conclusion

The pilot supports a narrow proposition: **truth admission can be coded reproducibly enough to continue investigating, but admissible 10-K claims are sparse and the component ontology is not yet stable.** Final admission agreement was strong, while boundary and identity judgments were only moderate. Strict wording also rejects forecasts that investors routinely interpret, such as “approximately $5.7 billion”; that is philosophically coherent but may discard useful probabilistic information.

The pilot does **not** establish predictive validity, causal validity, or alpha. Four resolved claims cannot distinguish a useful epistemic signal from ordinary forecast specificity. A return backtest now would be storytelling.

The next warranted experiment is a preregistered scale pilot: roughly 30–50 firms in one sector, two filing years, claim extraction frozen before resolution, dual coding, and comparisons against specificity, tone, filing change, and management guidance baselines. The first endpoint should be subsequent claim failure/reformulation, not returns. Only incremental prediction on that endpoint earns a market test.

## Reproduction artifacts

- `sample-50.json`: frozen sample
- `coder-a.json`, `coder-b.json`: independent labels
- `agreement.json`: agreement statistics
- `build_sample.py`, `agreement.py`: deterministic scripts
- `test_build_sample.py`, `test_agreement.py`: tests

Tests: `uv run --with pytest pytest -q tmp/truth-admission-pilot/test_build_sample.py tmp/truth-admission-pilot/test_agreement.py`

Source filings: [UPS 2022 10-K](https://www.sec.gov/Archives/edgar/data/1090727/000109072723000006/ups-20221231.htm), [UPS 2023 10-K](https://www.sec.gov/Archives/edgar/data/1090727/000109072724000008/ups-20231231.htm), [FedEx FY2023 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017023033201/fdx-20230531.htm), [FedEx FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1048911/000095017024083577/fdx-20240531.htm), [J.B. Hunt 2022 10-K](https://www.sec.gov/Archives/edgar/data/728535/000143774923004530/jbht20221231_10k.htm), and [J.B. Hunt 2023 10-K](https://www.sec.gov/Archives/edgar/data/728535/000143774924005368/jbht20231231_10k.htm).
