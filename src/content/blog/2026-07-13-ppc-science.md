---
variant: post-medium
title: "PPC Science"
tags: vector-space
---

A PPC professional forms a hypothesis, assigns a treatment, observes a response, and moves the next dollar toward the treatment that worked. Change the audience, hold the creative fixed. Change the landing page, hold the bid fixed. Split traffic, wait, measure, update. The laboratory runs continuously, and every failed experiment costs real money.

This is advertising science.

It is conducted with some of the worst scientific data still tolerated in a trillion-dollar industry.

The treatment record comes from the platform selling the treatment. The outcome begins as a pixel firing, may become a form fill, may eventually become a qualified lead in a CRM, and may become money months later in a different system. The join key is a query parameter somebody remembered to save. Treatment definitions change with the auction. Outcome definitions change with the campaign settings. The control group is whoever the platform did not happen to reach. The instrument reports its own success.

Then the scientist is asked for ROAS by Friday.

## The field diagnosis

PPC professionals already know what is broken. You can recover the diagnosis from the repairs they repeat.

Capture the gclid before it disappears. Carry it through the hidden form field. Store it on the CRM contact. Deduplicate the browser pixel against the server event. Score the lead. Upload the qualified stage. Upload closed-won. Pass the revenue value. Reverse the conversion when the customer refunds. Reconcile Google Ads against GA4, the CRM, Stripe, and the bank. Pick a source of truth. Explain why none of the totals match.

This is not a collection of tracking tricks. It is a vernacular theory of measurement.

| What the practitioner says | What the scientist means |
|---|---|
| Feed back qualified leads, not form fills | Improve the validity of the outcome label |
| Preserve the click ID | Maintain unit-level linkage from treatment to outcome |
| Deduplicate pixel and CAPI | Prevent repeated observations |
| Track refunds and chargebacks | Observe the outcome at its final horizon |
| Standardize conversion actions | Hold the dependent variable's definition fixed |
| Compare Ads, CRM, and Stripe | Reconcile instruments against the business ledger |
| Exclude brand search | Reduce selection bias from demand that already existed |
| Run a geo holdout | Construct a counterfactual |
| Wait for conversion lag | Account for right-censored outcomes |
| Stop calling it after twelve conversions | Admit the test has no power |

The vocabulary is different because the work grew out of operations, not a statistics department. The method is recognizable.

## They are asking for the rows

The claim is visible in current job descriptions, where companies specify the data they wish the channels produced.

Standard Bots wants a [Performance Marketing Lead](https://jobs.ashbyhq.com/standardbots/ae201278-1885-492d-b907-a9c810645e01) to connect advertising platforms to HubSpot so the algorithms learn from real business outcomes rather than form fills, and to measure the funnel from impression to closed-won. Viktor's [Founding Head of Search Acquisition](https://jobs.ashbyhq.com/viktor/5956d1bf-9159-4fc9-9a02-a710c334b84b) must upload offline conversions tied to closed-won, not lead volume, and read the raw data in SQL. Katana asks its [Senior Acquisition Manager](https://jobs.ashbyhq.com/katana/51b7810d-d7ab-4ee2-b25e-923271f75f1a) to connect low-level attribution events to SQL and closed-won records "so you know which programs are real."

Those are not retail networks observing purchases inside their own stores. They are ordinary inbound businesses buying search and social traffic, losing the thread at the boundary between ad platform and sales system, and hiring a human to sew it back together.

The most explicit specification comes from Tradeify's [Marketing Data Engineering Lead](https://jobs.ashbyhq.com/tradeify/ad7d2d2d-de25-4a21-aa76-403e21576799). The role joins Google and Meta spend, web behavior, product use, and checkout transactions in a warehouse. It defines identity rules, event taxonomies, purchases, refunds, and chargebacks; handles deduplication and idempotency; monitors the pipelines; and turns ambiguous business questions into data contracts. That is not a dashboard job. It is the construction of an experimental dataset.

Upside's [Senior Marketing Analytics Manager](https://jobs.ashbyhq.com/upside/59da723c-f8b9-4463-8808-6f957154bb78) completes the specification: improve event tracking, identity stitching, attribution signals, and channel taxonomies, then run A/B tests, multivariate tests, and lift studies with statistical rigor. Keurig Dr Pepper compresses the observational half into one rule in its [Media Measurement Manager](https://careers.keurigdrpepper.com/es/trabajo/frisco/media-measurement-manager/42849/93272582624) posting: *verified exposure + verified sale = attributed sale*. Causal lift is a separate pillar.

Across different companies and titles, the requested table has the same columns: treatment, unit, outcome, value, time, provenance. The requested controls have the same names: stable definitions, deduplication, traceability, reconciliation, experimental integrity.

They are asking for scientific data.

## The optimization trap

The industry has noticed half the problem. Google and Meta accept offline conversions, qualified leads, and value signals. Call-tracking products connect a keyword to a phone conversation. Attribution vendors join ad spend to CRM stages, Stripe payments, refunds, and lifetime value. Better labels make the bidding algorithm better.

That is useful. It is not yet science.

An optimizer needs a reward signal. A scientist needs a record of how the signal was produced. An optimizer can learn that customers resembling this customer produce more revenue. A scientist must still ask whether showing the ad changed the probability of revenue. An optimizer is rewarded for prediction under the platform's current policy. A scientist needs identification beyond that policy.

The plumbing therefore runs in the wrong direction for inquiry. The advertiser improves a label in its own books, uploads the label into the platform, and receives a better bid decision. What comes back is a report. The row went in; the model's treatment assignment, joins, exclusions, and counterfactual did not come out.

This is why platform optimization can improve while advertiser knowledge does not. The machine gets a higher-quality dependent variable. The scientist still cannot reproduce the result.

## What good data would contain

PPC science does not require perfect identity or a universal source of truth. Science routinely works across imperfect instruments. It requires that the imperfections be visible.

For a direct-response experiment, the minimum useful record is boring:

1. A stable identifier for the experimental unit.
2. The treatment the unit was eligible to receive.
3. The treatment actually delivered, with time and version.
4. A comparable record for units not treated.
5. The observed downstream outcome, including its final value and reversals.
6. The rule joining treatment to outcome.
7. The transformations, exclusions, and missingness between source and analysis.
8. The assignment procedure, so selection can be distinguished from effect.

Today's stack supplies fragments. The platform has eligibility, auction, and delivery. The advertiser has qualification, sale, margin, refund, and retention. The PPC practitioner has a spreadsheet, a click ID, and a weekly meeting where the fragments are made to sound like a result.

No statistical technique repairs a treatment record it cannot inspect. No attribution model manufactures a control group. No beautiful dashboard makes a form fill into revenue.

## The compensating scientist

This explains an odd feature of the profession. PPC work is described as campaign management, but much of the actual labor is instrument maintenance. Tag audits. Naming conventions. Negative keywords. CRM mappings. Conversion imports. Discrepancy explanations. Lead-quality meetings with Sales. Sheets that connect click IDs to opportunities. Small scripts that discover the webhook stopped firing eleven days ago.

The practitioner is not merely operating the experiment. The practitioner is compensating for the missing laboratory.

That labor has a testable shape. If the diagnosis is right, experienced PPC operators should independently converge on the same repairs: downstream outcome labels, persistent join keys, server-side events, deduplication, conversion governance, reconciliation, holdouts, and skepticism toward platform ROAS. The convergence should appear across agencies, in-house teams, lead generation, ecommerce, SaaS, calls, and bookings. It should become more pronounced as spend, conversion lag, and distance between lead and revenue increase.

The claim can be falsified. Sample the field's troubleshooting corpus. Code the failure location and proposed repair. If practitioners mostly complain about creative, bidding, and interface friction, the accounting diagnosis is overstated. If mature accounts accept platform conversions as adequate scientific evidence, it is wrong. If better downstream records do not change budget decisions or experimental conclusions, the missing rows are not the binding constraint.

But if the same data repairs recur across the profession, the workarounds become evidence. The people closest to the experiments have been specifying the missing instrument all along.

PPC professionals are advertising scientists. Their methods are not primitive. Their laboratory is.

*Part of the [Vector Space](/vector-space) series.*
