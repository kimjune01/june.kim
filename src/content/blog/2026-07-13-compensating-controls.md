---
variant: post-medium
title: "Compensating Controls"
tags: vector-space
---

An advertiser hands a platform money. The platform runs the ads, counts what the ads sold, and reports the count. The counting happens in a back room the buyer never enters, and the one doing the counting is the one getting paid on the result. The advertiser knows what he paid and what he sold; the platform knows what it delivered and what it claims credit for. Everything in between, the auction, the delivery, the crediting, runs out of sight, and no document from that opaque middle is held by both sides. That is [an accounting problem](/adtech-is-an-accounting-problem).

Accounting has a word for what happens next. A control is a check the books run on the business, like matching invoices to deliveries before paying them. When an auditor finds one missing, the client rarely fixes it, because fixing it means changing the system that everyone's job depends on. Instead the client adds a *compensating control*, a second process that watches the gap the first one left open. Auditors accept compensating controls with a known caveat: they cost more than the control they substitute for, they degrade as the system changes, and they never quite close the gap.

The missing control makes a testable prediction. There should exist an industry of compensating controls, sized in proportion to the gap, each vendor selling a substitute for a document that ordinary commerce generates for free. The industry exists. Here is the inventory.

![The compensating-control stack: seven tiers of vendors narrowing upward like an unfinished tower, standing over a dashed void where the settlement receipt should be](/assets/compensating-controls-tower-light.svg)

## The stack

Different tiers substitute for different documents. What unites them is the reason each document is missing: no event in this chain generates a record that both sides hold.

*Impression inspection.* DoubleVerify and Integral Ad Science sell verification that ads were viewable, non-fraudulent, and brand-safe. Between them they bill roughly [$1.3 billion a year](https://digiday.com/media-buying/ad-verifications-duarchy-touts-ai-to-wall-stret-amid-expansion-plans/) ([DV investor filings](https://ir.doubleverify.com/financials/quarterly-results/default.aspx), [IAS Q3 2025](https://www.sec.gov/Archives/edgar/data/1842718/000184271825000107/q325earningsrelease.htm)). The document they substitute for is a delivery record the buyer could check himself. A warehouse gets one with every pallet; it's called a receiving report, and nobody pays a duopoly a billion dollars a year to guess whether the truck arrived.

*Inspection of the inspectors.* In March 2025 Adalytics published a [240-page report](https://www.adexchanger.com/platforms/verification-providers-missed-easy-to-spot-bots-says-adalytics-what-went-wrong/) documenting ads served between 2019 and 2025 to bots that declared themselves as bots, in accounts paying for bot filtration. DoubleVerify [disputes the findings](https://doubleverify.com/doubleverifys-response-to-adalytics-march-28-givt-report/). Whoever is right, note the layer's existence: a forensic researcher auditing the verification vendors, one level up the same tower, substituting for the same missing document.

*Attribution referees.* Mobile measurement partners (AppsFlyer, Adjust, Branch) and the multi-touch attribution vendors exist because every platform attributes conversions to itself and the claims sum to more than the sales. The MMP is a privately hired referee for credit disputes. The document it substitutes for is a conversion record both counterparties sign: a settlement receipt.

*Experiment platforms.* [Haus, Measured, Sellforte](https://segmentstream.com/blog/articles/top-10-incrementality-testing-tools) and their cohort sell geo-holdout experiments. A geographic split is the one experiment the platform cannot referee, because it runs in the world, outside the platform's reporting. Advertisers pay six figures to buy back information the channel deleted at the moment of sale, a few aggregate bits per quarter.

*Models instead of rows.* Marketing mix modeling died with the spreadsheet era and came back after [ATT](https://en.wikipedia.org/wiki/App_Tracking_Transparency). Google now ships [Meridian](https://developers.google.com/meridian) and Meta ships [Robyn](https://facebookexperimental.github.io/Robyn/), both open source. An MMM is a regression fitted over aggregates, a model standing in for books. The two companies holding the row-level data give away tools for modeling around its absence.

*Join-key plumbing.* A cottage industry ([Able CDP](https://www.ablecdp.com/blog/stripe-conversion-tracking), [Tracklution](https://www.tracklution.com/learn/stripe-conversion-tracking/), the server-side tagging consultancies) exists to hand-carry the gclid from the click through the funnel to the charge, because the channel does not carry its own join key to settlement. Every tool in this layer points the same direction: capture attribution data and upload it into the platform's books. I could not find one that pulls the platform's claims and checks them against the seller's ledger; the reconciliation direction is unoccupied.

*Unpaid reconciliation labor.* Under the commercial layers sits the free one. Spend an hour in [r/PPC's archives](https://old.reddit.com/r/PPC/search?q=%22source+of+truth%22&restrict_sr=on&t=year) and you find the same thread monthly: Meta says 374 leads, Google Ads says 71, GA4 says 110, whose number goes in the client report? The community's answers are hand-rolled sheets joining gclids to CRM rows, and a doctrine of picking one source of truth and defending it. This is reconciliation performed by hand, per account, forever, by the people the stack was supposed to serve.

## The audits

The layers above are recurring, but twice the industry paid for the one-off version, an actual forensic reconciliation.

ISBA and PwC traced UK programmatic spend end to end in [2020](https://www.isba.org.uk/system/files/media/documents/2020-12/executive-summary-programmatic-supply-chain-transparency-study.pdf): 12% of impressions could be matched from advertiser to publisher, and 15% of spend was an "unknown delta" attributable to no party. The [2022 restudy](https://videoweek.com/2023/01/18/programmatic-advertisings-unknown-delta-drops-to-three-percent-in-second-isba-pwc-study/), after two years of data standardization, matched 58% and shrank the delta to 3%. Read that as good news, carefully. Reconciliation is achievable, but it took a trade body, PwC, and years of coordination, and it runs about twice a decade. Double-entry bookkeeping does the equivalent nightly.

The ANA's [2023 study](https://www.ana.net/content/show/id/pr-2023-06-programmaticstudy) put numbers on the open-web pool: $88 billion in spend, [$22 billion of it waste](https://www.adexchanger.com/online-advertising/the-ana-releases-its-second-transparency-report-hits-the-open-web-as-25-waste/), and $0.36 of each DSP dollar reaching a consumer.

On the attribution side, [Blake, Nosko and Tadelis](https://onlinelibrary.wiley.com/doi/10.3982/ECTA12423) switched off eBay's brand-search ads and watched the traffic arrive anyway. [Gordon et al.](https://pubsonline.informs.org/doi/10.1287/mksc.2018.1135) ran Meta's own lift experiments against observational attribution and found the observational numbers overstated lift by multiples. eBay cut nine figures of spend; it was auditing its own books. The industry-level findings moved nothing, because an aggregate finding has no owner. Each study was absorbed as demand generation for the next layer of the stack.

## The demolition

Suppose the conversion event carried its own proof: a settlement record that advertiser and channel both hold, generated at the moment the money moves, checkable without trusting either party. [The croupier design](/vector-space) is one construction; a payment processor countersigning the charge would be another. The construction is direct-response by design; brand advertising buys attention with no settlement event, and keeps its models.

Rerun the inventory against that record and the tower comes down, because every tier substituted for a document nobody held, and now both sides hold it. Nothing is left to inspect, no credit claim needs a referee, no join key needs hand-carrying, no sheet needs reconciling, and the forensic audit that took PwC two years shrinks to a nightly batch job.

The causal layer survives. A receipt proves the conversion happened and cleared, but it does not prove the ad caused it. Geo-holdouts still answer the incrementality question, cheaper and higher-powered once the outcome variable stops being disputed, but a receipt is bookkeeping, and no amount of bookkeeping substitutes for a counterfactual.

The compensating-control industry is real, its invoices are public, and its annual bill is a lower bound on the price of one missing document. The stack doesn't need another layer. It needs a base that doesn't require the stack.

*Part of the [Vector Space](/vector-space) series.*
