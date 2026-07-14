---
variant: post-medium
title: "PPC Science"
tags: vector-space
---

A PPC professional changes an audience, creative, landing page, bid, or budget. Then they observe a response and move the next dollar. The cadence resembles experimental science: intervene, measure, update. But most PPC work optimizes a system; only some identifies what the advertising caused.

The treatment record comes from the platform selling the treatment. The outcome begins as a pixel firing. It may become a form fill, a qualified lead in a CRM, and eventually money in a different system. A query parameter somebody remembered to save becomes the join key. Treatment definitions change with the auction. Campaign settings change outcome definitions. Whoever the platform did not happen to reach becomes the control group. The instrument reports its own success.

Then the scientist is asked for ROAS by Friday.

## The field diagnosis

PPC professionals reveal the diagnosis through the repairs they repeat.

Capture the gclid before it disappears. Carry it through the hidden form field. Store it on the CRM contact. Deduplicate the browser pixel against the server event. Score the lead. Upload the qualified stage. Upload closed-won. Pass the revenue value. Reverse the conversion when the customer refunds. Reconcile Google Ads against GA4, the CRM, Stripe, and the bank. Pick a source of truth. Explain why none of the totals match.

These tracking tricks form a practical theory of the outcome label.

| What the practitioner says | What the repair changes |
|---|---|
| Feed back qualified leads, not form fills | Make the optimization target resemble business value |
| Preserve the click ID | Keep the acquisition event joined to the later outcome |
| Deduplicate pixel and CAPI | Prevent repeated observations |
| Track refunds and chargebacks | Observe the outcome at its final horizon |
| Standardize conversion actions | Hold the dependent variable's definition fixed |
| Compare Ads, CRM, and Stripe | Reconcile instruments against the business ledger |
| Exclude brand search | Reduce selection bias from demand that already existed |
| Run a geo holdout | Construct a counterfactual |
| Wait for conversion lag | Account for right-censored outcomes |
| Stop calling it after twelve conversions | Admit the test has no power |

The vocabulary grew out of operations. Though the method is recognizable, causal inference does not follow from plumbing.

In a purposive review of twenty r/PPC threads, the dominant question was how to choose the deepest outcome still frequent and fast enough for automated bidding. Form fills are abundant but weak; closed-won revenue is valid but sparse and late. Practitioners settled between them: qualified lead, answered call, booked appointment, MQL, SQL, or completed application. The trade-off appears in discussions of [qualified leads as the primary conversion](https://www.reddit.com/r/PPC/comments/14m2801), [low-quality conversions under Smart Bidding](https://www.reddit.com/r/PPC/comments/1uup4rz), and [offline imports for qualified leads](https://www.reddit.com/r/PPC/comments/1mb2gg7).

Their requested repair is thin. Receive the inquiry, decide whether it is real and relevant, and preserve the click identity. Then return a label and perhaps a value to the bidding system.

## The jobs ask for deeper joins

Standard Bots wants a [Performance Marketing Lead](https://jobs.ashbyhq.com/standardbots/ae201278-1885-492d-b907-a9c810645e01) to connect advertising platforms to HubSpot so the algorithms learn from real business outcomes rather than form fills, and to measure the funnel from impression to closed-won. Viktor's [Founding Head of Search Acquisition](https://jobs.ashbyhq.com/viktor/5956d1bf-9159-4fc9-9a02-a710c334b84b) must upload offline conversions tied to closed-won, not lead volume, and read the raw data in SQL. Katana asks its [Senior Acquisition Manager](https://jobs.ashbyhq.com/katana/51b7810d-d7ab-4ee2-b25e-923271f75f1a) to connect low-level attribution events to SQL and closed-won records "so you know which programs are real."

These are inbound businesses hiring people to repair the boundary between ad platform and sales system.

Tradeify's [Marketing Data Engineering Lead](https://jobs.ashbyhq.com/tradeify/ad7d2d2d-de25-4a21-aa76-403e21576799) joins Google and Meta spend with web behavior, product use, and checkout transactions in a warehouse. The role defines identity rules and event taxonomies for purchases, refunds, and chargebacks. It handles deduplication and idempotency, then turns business questions into data contracts. The result is an experimental dataset.

Upside's [Senior Marketing Analytics Manager](https://jobs.ashbyhq.com/upside/59da723c-f8b9-4463-8808-6f957154bb78) improves event tracking, identity stitching, attribution signals, and channel taxonomies, then runs A/B, multivariate, and lift tests. Keurig Dr Pepper's [Media Measurement Manager](https://careers.keurigdrpepper.com/es/trabajo/frisco/media-measurement-manager/42849/93272582624) follows one observational rule: *verified exposure + verified sale = attributed sale*. Causal lift remains separate.

Across titles, the same columns recur: acquisition event, lead, downstream stage, value, and time. Measurement roles add provenance, stable definitions, deduplication, reconciliation, and experimental integrity. The first set supports optimization; the second can support inference.

## The optimization trap

Existing products perform much of the repair. [WhatConverts](https://www.whatconverts.com/offline-conversion-tracking-for-agencies-clients/) captures calls, forms, chats, and click identity. It applies qualification rules and returns selected conversions to Google Ads. [CallRail](https://www.callrail.com/blog/callrail-debuts-conversion-signals-to-improve-ad-targeting) detects requested and booked appointments from calls. [Ruler Analytics](https://www.ruleranalytics.com/blog/ppc/google-ads-offline-conversions/) returns CRM stages and revenue. Google lets advertisers mark answers in [Google-hosted Search forms](https://support.google.com/google-ads/answer/17050941) as qualifying responses, and its [offline-conversion documentation](https://support.google.com/google-ads/answer/7012522) instructs advertisers to capture the gclid, store it with the prospect, and return later outcomes.

This is the thin filter practitioners describe. A prospect, rule, conversation model, salesperson, CRM stage, or invoice supplies the label. The process spans the form, tracking software, sales operation, CRM, and platform.

It is useful. It still does not establish causation.

An optimizer needs a reward signal. A scientist needs its provenance and must still ask whether the ad changed the probability of revenue. Prediction under the platform's policy is not identification beyond it.

The plumbing runs inward. The advertiser improves and uploads a label, then receives a bid decision and report. The row goes in; treatment assignment, joins, exclusions, and counterfactual do not come out. Platform optimization can improve without improving advertiser knowledge.

The advertiser pays for the click and absorbs bad leads. It discovers their value, maintains the join, and returns the result. That result supplies the reward signal to Smart Bidding, which [Google says sets bids for every auction using millions of signals](https://support.google.com/google-ads/faq/10286469). Google also [determines which ads show through that auction](https://support.google.com/google-ads/answer/6366577). The same company operates the bidder, auction, and market.

Better labels can reduce waste and improve advertiser profit. They can also raise bids and transfer some gain to the auction operator. The workflow alone does not identify the incidence. It does reveal the conflict: private facts about customer value enter a bidder and auction controlled by the seller.

The thin filter serves the advertiser, but sends better proprietary information to Google. After labeling the intervention, the advertiser receives decisions without a portable model or auditable account of how the label changed them.

Google has repeatedly incorporated market information into a private model, degraded the surface through which participants inspected it, and returned an automated answer. That pattern supplies a reference class for this workflow.

Publishers supplied pages and links; Google built the index, then moved answers onto its own surface. In a study of 68,879 searches, [Pew found](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/) that AI summaries reduced clicks to traditional results from 15% of visits to 8%, while only 1% clicked a source inside the summary. [The information remained useful after the reading surface disappeared](/impressions-and-clicks).

Advertising followed the same pattern. Google moved targeting and bidding into private models while reducing inspectable records. Google says the [Performance Max placement report](https://support.google.com/google-ads/answer/11465047) is for brand safety, not comprehensive performance analysis; unlike newer channel-level reports, placement-level reporting does not attach clicks, cost, or conversions to each site. In 2022, Google [removed all App campaign placement data](https://ads-developers.googleblog.com/2022/02/important-changes-to-placement.html) from several API reports. [Smart Bidding still evaluates auction-time context](https://support.google.com/google-ads/answer/10964872), including signal combinations advertisers cannot reproduce. Participants contribute more information and receive fewer readable records.

Offline conversions fit the pattern. The advertiser labels the outcome; Google returns a bid. Between them, the reading surface disappears. The advertiser cannot inspect what the model learned, how allocation changed, or whether the result could have been bought more cheaply.

The direct evidence establishes information enclosure and conflicted delegation. Participant-produced information becomes private coordination, the reading surface withdraws, and dependence on the model increases. Google's repeated strategy makes rent extraction the leading explanation, but the evidence does not isolate this loop's additional rent. Measuring that incidence would require advertiser profit, price, and counterfactual-channel data that neither platform reporting nor the practitioner sample supplies.

## What good data would contain

PPC science does not require perfect identity or one truth. It requires visible imperfections.

For a direct-response experiment, the minimum useful record is boring:

1. A stable identifier for the experimental unit.
2. The treatment the unit was eligible to receive.
3. The treatment actually delivered, with time and version.
4. A comparable record for units not treated.
5. The observed downstream outcome, including its final value and reversals.
6. The rule joining treatment to outcome.
7. The transformations, exclusions, and missingness between source and analysis.
8. The assignment procedure, so selection can be distinguished from effect.

The platform has eligibility, auction, and delivery. The advertiser has qualification, sale, margin, refund, and retention. The practitioner has a spreadsheet, click ID, and meeting where fragments become a result.

No statistical technique repairs a treatment record it cannot inspect. No attribution model manufactures a control group. No beautiful dashboard makes a form fill into revenue.

## The compensating scientist

PPC is described as campaign management, but much of its labor maintains instruments. That labor includes tag audits, naming conventions, CRM mappings, conversion imports, discrepancy explanations, lead-quality meetings, join sheets, and scripts that discover a dead webhook.

The practitioner is not merely operating the experiment. The practitioner is compensating for the missing laboratory.

The diagnosis predicts convergence on downstream labels, persistent join keys, server-side events, deduplication, conversion governance, reconciliation, holdouts, and skepticism toward platform ROAS. Convergence should strengthen as spend, conversion lag, and distance from lead to revenue increase.

The first field sample supports an outcome-label and feedback-loop problem, not profession-wide demand for causal identification. If better downstream records do not change bidding or budgets, even that diagnosis is overstated.

The workarounds specify the repair: an outcome deep enough to represent value, yet frequent and fast enough to train the optimizer. A smaller part of the profession tests incrementality.

The practitioner repairs the label and preserves the join. Google uses that label inside a bidder it operates in an auction it monetizes. Better measurement may create value for both. The advertiser cannot inspect how much value it created, how the model used that value, or how the gain was divided.

*Part of the [Vector Space](/vector-space) series.*
