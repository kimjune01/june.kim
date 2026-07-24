# PPC Science: r/PPC field research

Research date: 2026-07-13

## Question

How do PPC practitioners describe what is broken in their data, and what repairs do they propose, before translating their language into an accounting or scientific framework?

## Method

I searched public r/PPC threads using four topic strata:

1. offline conversions and qualified leads;
2. discrepancies among ad platforms, GA4, CRM, and revenue;
3. spam, duplicate, or low-quality conversion signals;
4. incrementality, holdouts, and attribution limits.

The coded sample contains 20 distinct threads published from 2020 through July 2026. Search and coding occurred on July 13, 2026. Threads were chosen to cover the four strata, not randomly sampled, so theme counts describe this corpus rather than r/PPC as a whole. Search ranking, deleted material, low-vote comments, unverifiable practitioner identities, promotional replies, and likely AI-written posts or comments all limit the evidence.

The unit of analysis is a thread, including disagreements in its comments. Codes overlap.

## Coded sample

| # | Thread | Context | Failure stated by practitioners | Repair stated by practitioners | Tension or dissent |
|---|---|---|---|---|---|
| 1 | [Offline Conversions for Qualified Leads](https://www.reddit.com/r/PPC/comments/1mb2gg7) | Google lead gen | Form fills give spam and qualified leads equal labels | Capture GCLID; upload qualified, SQL, and customer stages; keep definitions consistent | Deep labels improve quality but may lack volume |
| 2 | [Offline conversions for local business](https://www.reddit.com/r/PPC/comments/1upkcsl) | Local services | Calls and forms include non-buyers; valuable sales remain secondary | Make money-producing offline outcomes primary; raw calls/forms secondary; attach value | Double counting and loss of bidding history worry the operator |
| 3 | [Resources for uploading offline conversions](https://www.reddit.com/r/PPC/comments/1s2t3c1) | $40K lead-gen outcome | Business value exists outside the ad account | Upload click ID, conversion name, value, consent; define “qualified” first | Implementation knowledge is the immediate constraint |
| 4 | [Enhanced Conversions vs GCLID imports](https://www.reddit.com/r/PPC/comments/1rg3fd8) | B2B/high-volume Google | Identity matching and deterministic click matching are confused; match coverage is partial | Prefer GCLID when reliably captured; use hashed identity to recover missing matches | Deterministic precision competes with coverage and consent limits |
| 5 | [Qualified leads as primary](https://www.reddit.com/r/PPC/comments/14m2801) | Lead gen | Raw leads are noisy; closed-won is sparse and delayed | Test intermediate stages and weighted values | A weaker, frequent signal can outperform a stronger, sparse one |
| 6 | [Manually qualify leads](https://www.reddit.com/r/PPC/comments/1r2kqcy) | Spam-heavy lead gen | The platform rewards junk because form fill is primary | Upload qualified leads; retain raw forms for observation; use answered call or booked appointment when volume is low | The thread itself drew suspicion as AI mining; threshold claims were unsupported |
| 7 | [Qualified offline conversions at campaign level](https://www.reddit.com/r/PPC/comments/1hwlb5q) | CallRail lead gen | Manual qualified outcomes are not steering bids | Assign expected values; automate from CRM; promote deep outcome when volume permits | Practitioners disagree on which funnel stage carries enough signal |
| 8 | [Offline conversions useful for Search Ads?](https://www.reddit.com/r/PPC/comments/1jb4yfl) | B2B search | Search generates consumer or low-quality leads that never become business | Upload qualified opportunities, contract values, and sales | Performance-improvement claims are anecdotal and sometimes promotional |
| 9 | [Only qualified leads back to Google](https://www.reddit.com/r/PPC/comments/1g5699g) | Google lead gen | Algorithm optimizes every form fill | Store click ID; upload qualified leads; make raw forms secondary | Removing the high-volume proxy too early can destabilize bidding |
| 10 | [Low-quality conversions and Smart Bidding](https://www.reddit.com/r/PPC/comments/1uup4rz) | Lead gen, 2–6 week sales lag | Campaign winners reverse when matched to customers and revenue | Score CRM stages, retract junk, assign progressive values, optimize at deepest viable stage | Sales must produce labels; signal quality, volume, and delay trade off |
| 11 | [Google, Meta and GA4 never agree](https://www.reddit.com/r/PPC/comments/1u96xti) | Cross-platform reporting | Systems count different events, windows, dates, and view-through claims | Use platform figures for platform bidding, backend for realized revenue, and a separate model for comparison | Some commenters still treat a large gap as a tracking defect; no single number serves every decision |
| 12 | [GA4 vs Google Ads conversions](https://www.reddit.com/r/PPC/comments/1i83efw) | Google measurement | The same named event produces different counts | Align count settings, attribution, and windows | Several answers normalize disagreement rather than seek reconciliation |
| 13 | [Two GA4 reports do not match](https://www.reddit.com/r/PPC/comments/1lvkg9z) | GA4 reporting | Reports inside one product disagree; browser loss reduces coverage | Compare with CMS sales; use server-side tracking and enhanced conversions | GA4 itself is rejected as a source of truth by one practitioner |
| 14 | [GA4 and Ads import mismatch](https://www.reddit.com/r/PPC/comments/1s2bt8g) | Imported GA4 event | Even a shared source event diverges after platform attribution | Align filters, windows, and counting settings | Commenters disagree whether the counts should match at all |
| 15 | [GA4 conversions not importing](https://www.reddit.com/r/PPC/comments/1catgbo) | UK ecommerce | GA4 revenue greatly exceeds imported Google Ads revenue | Enhanced conversions and lower tROAS were tried | Operator remains unable to locate the failure; tooling does not expose the path |
| 16 | [Settings that quietly ruin data](https://www.reddit.com/r/PPC/comments/1tuxlp6) | Mixed lead-gen audits | Click-to-call, page views, duplicate conversions, and low-quality leads masquerade as outcomes | Compare platform conversions with CRM quality, revenue, duplicates, and sales-team observations | Reservations and completed calls are still proxies for realized value |
| 17 | [Spam and fake lead checklist](https://www.reddit.com/r/PPC/comments/1mcq3nv) | Google lead gen | Bots and partner traffic poison automated bidding | Exclude bad periods, remove weak inventory, and return CRM quality labels | Repairs mix traffic policy, form design, and outcome data; data is not always the root cause |
| 18 | [CTV incrementality headaches](https://www.reddit.com/r/PPC/comments/1qqefj3) | Streaming TV | View-through and modeled conversions cannot establish lift | Judge total revenue in geo holdouts; add MMM after enough history | Practitioners dispute bot prevalence, appropriate funnel role, and what counts as proof |
| 19 | [SEM brand incrementality](https://www.reddit.com/r/PPC/comments/iflbae) | Brand search/video | Geo tests produced implausible results | Use holdout markets and downstream brand-search or MQL lift | Clients reportedly prefer click attribution; scale and spillover impair tests |
| 20 | [First-click attribution](https://www.reddit.com/r/PPC/comments/1r05wce) | Multi-channel acquisition | First-click history is missing and data-driven attribution is opaque | Some propose incrementality or probabilistic tools; others accept last-click as the only observable link | The thread rejects the premise that a click model can recover the customer journey |

## Emergent practitioner categories

### 1. Label depth versus learning speed

This is the dominant problem in the sample. Practitioners want the deepest available business outcome, but Smart Bidding needs frequent and timely labels. A closed sale is valid but sparse and late; a form fill is abundant but weak. Their recurring solution is an intermediate label such as qualified lead, answered call, booked appointment, SQL, or completed application, sometimes with progressive values for later stages.

Their operative question is not “what is the true outcome?” It is “what is the deepest outcome that still gives the algorithm enough signal?”

### 2. The join is understood but fragile

Practitioners repeatedly describe the same chain: click ID or hashed identity enters through the landing page, persists in CRM, receives a later stage or value, and returns through an offline-conversion import. They know how the join should work. Threads exist because capture, consent, CRM fields, attribution windows, match errors, manual uploads, and API changes make it unreliable.

The repair they request is often operational reliability, not a new attribution theory.

### 3. Different instruments serve different decisions

The discrepancy threads do not converge on one source of truth. A common doctrine is:

- backend or CRM for realized sales and revenue;
- platform metrics for steering that platform’s bidding;
- GA4 or another model for cross-channel reporting.

Practitioners often regard non-matching totals as expected because the instruments use different windows and credit rules. They investigate large or sudden gaps as tracking failures. This is closer to instrument calibration than ledger reconciliation.

### 4. Optimization dominates inquiry

Most repairs send improved labels back into Google or Meta so automated bidding can find more buyers. Practitioners discuss the data primarily as training signal. Few ask to export treatment assignment, reproduce the platform model, or estimate a counterfactual outside the platform.

They know the outcome label is bad. Their daily mandate is usually to improve the optimizer, not to make the causal claim auditable.

### 5. Causal practice exists at the edge

The incrementality threads distinguish attributed conversions from incremental conversions and recommend geo holdouts, total-outcome measurement, MMM, or on/off tests. They also report implausible estimates, insufficient scale, spillover, long ramp times, and clients who prefer click attribution.

The corpus supports a causal-methods subgroup inside PPC. It does not support calling every PPC practitioner a causal scientist.

### 6. Sales operations co-produces the data

Lead quality is not observable inside the ad account. A sales team or CRM process must define qualification, record stages consistently, retract junk, and attach revenue. Several threads locate the bottleneck with the client’s sales process, form design, response time, or CRM hygiene rather than the ad platform.

PPC data quality is partly an organizational interface problem.

## Theme counts

Counts below are overlapping thread-level codes in this 20-thread purposive sample.

| Code | Threads |
|---|---:|
| Proxy outcome differs from qualified or realized business outcome | 13 |
| Proposed repair uploads deeper CRM/offline outcomes | 12 |
| Signal quality conflicts with volume or delay | 8 |
| Join, match, import, or tracking reliability problem | 10 |
| Multiple systems disagree by construction or configuration | 5 |
| Backend/CRM used to evaluate realized business outcome | 6 |
| Explicit causal or incrementality distinction | 4 |
| Holdout, on/off, or geo experiment proposed or discussed | 3 |
| Client or organizational constraint blocks better measurement | 5 |

These counts should not be generalized beyond the corpus. Their value is comparative: outcome-label and feedback-loop problems dominate the selected practitioner discussions; causal identification is present but much less frequent.

## What practitioners appear to know

The sample supports these claims:

1. Practitioners know a conversion action is a chosen label, not automatically a business outcome.
2. They know automated bidding optimizes the label supplied, including spam and low-value proxies.
3. They know the label must be joined to downstream CRM or transaction state.
4. They know deduplication, stable qualification criteria, timing, and sufficient sample volume affect learning.
5. They know platform, analytics, and backend totals answer different questions.
6. A subset knows attribution does not identify incrementality and uses external experiments when budget and client appetite permit.

The sample does not establish that practitioners demand a complete scientific dataset. Their preferred solution is usually a better feedback loop into the existing platform.

## Implication for “PPC Science”

The original thesis, “PPC professionals are advertising scientists working with the worst data,” is too broad as an empirical conclusion.

The field evidence supports a narrower formulation:

> PPC practitioners run sequential interventions against business outcomes, and they understand the feedback signal better than the reporting interface suggests. Their central measurement problem is choosing and reliably returning an outcome label that is deep enough to represent value, yet frequent and fast enough to train the optimizer. A smaller part of the profession also tests incrementality, usually against organizational and statistical resistance.

That formulation preserves the scientific analogy without attributing a causal standard the whole profession does not claim.

## Next field step

Reddit reveals vocabulary and recurring problems, but purchasing demand requires interviews or observed buying behavior. Interview prompts should follow practitioner categories rather than introduce ours:

1. What conversion does bidding optimize today, and what business outcome do you actually care about?
2. Why did you choose that funnel stage?
3. What prevents you from using a deeper stage?
4. Where does the click-to-outcome join fail most often?
5. Which system do you use for bidding, reporting, and realized revenue, and why?
6. When have the apparent channel winners changed after joining CRM or revenue data?
7. Have you run a holdout or incrementality test? What made it possible or prevented it?
8. What have you bought, built, or staffed to improve this process?
