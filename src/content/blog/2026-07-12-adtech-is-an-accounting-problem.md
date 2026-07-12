---
variant: post-medium
title: "Adtech Is an Accounting Problem"
tags: vector-space
---

Settling an ad bill is simple in principle. Spend per campaign in the left column, tagged arrivals in the right column, join on the click ID, and one sumproduct later you have revenue per campaign. A business owner can build it in an afternoon, and most of the afternoon is formatting. It is an accounting identity. Nothing in it is a model.

So why does an incrementality industry charge [fifty thousand dollars a year and up](https://www.mediaplanningtool.com/measured) to answer "did my ads work," why do [a hundred-plus courses](https://www.classcentral.com/subject/conversion-tracking) teach conversion tracking, and why did an agency lead spend months [fishing Google click IDs out of CallRail URL columns by hand](https://www.reddit.com/r/PPC/comments/1qdh4z8/is_it_possible_to_track_callrail_converted_call/)?

Because neither column holds still, and the right one is written by the parties being graded.

## Seven ledgers, one sale

One customer clicks an ad and buys something. Count the books that record it.

1. **The seller's delivery report** (the Google Ads or Meta dashboard) claims the conversion on its own attribution window and under its own dedup rules, increasingly as a modeled estimate booked alongside the observed records. The platform invoices for clicks at auction prices, so this is not the bill. It is the goods receipt. The seller writes it.
2. **The second opinion** (GA4) records the same conversion as a different number. Google's ads ledger and Google's analytics ledger disagree with each other, and [Google's own help center](https://support.google.com/google-ads/answer/13881741) maintains a page explaining why the two can never balance: different count dates, different attribution, different definitions of the event.
3. **The call log** (CallRail) knows the call happened and was scored qualified, and its export has no click ID. The join key to ledger one is missing by design.
4. **The sales ledger** (the CRM) is the only book that knows whether the lead became money, and it knows nothing about which ad, unless somebody plumbed a webhook to carry the click ID across.
5. **The bookkeeper's summary** (the agency's monthly report) is a curated projection of ledger one, prepared by a party whose fee survives on the ambiguity.
6. **The last-touch claimant** (the affiliate network) keeps a ledger that can be rewritten at the checkout moment, as [146,000 stores](https://ecomscout.com/reports/paypal-honey-dataset) discovered when the Honey extension collected credit on their sales without any affiliate agreement at all.
7. **The bank statement** is the one honest book, and it only knows money out.

![One sale recorded in seven disagreeing ledgers](/assets/seven-ledgers-light.svg)

Seven books, one event, no two agree. The point is not that anyone is sloppy. The point is that every player keeps single-entry books about the same transactions. Inside each firm there is double-entry, there are controls, there are auditors. Between the firms, where the money actually moves, there are no shared entries at all.

Nobody's ledger is anyone else's counterparty record, and there is no trial balance for the industry, because the books share no key, no window, and no definition of the event. Advertisers already talk about this in exactly these terms: in a [2026 CIMM survey](https://cimm-us.org/wp-content/uploads/2026/03/CIMM-4As-Advertisers-Perspectives-on-the-State-of-Measurement-Full-Report-March-2026.pdf), the line they gave researchers was "the platforms grade their own homework."

If you run ads and reconciling them feels like a personal failure, this is the absolution: the books don't reconcile by construction. A consultant who wired his own reconciliation harness out of Ads API pulls and CRM exports [compressed it into one line](https://www.reddit.com/r/Google_Ads/comments/1upmu16/any_codexclaude_skills_for_google_ads/): "'Configured' and 'proven with a recent lead' are not the same thing."

## Cooked books and marked models

Auditing splits every wrong number [by intent: error or fraud](https://www.iaasb.org/publications/isa-240-revised-auditor-s-responsibilities-relating-fraud-audit-financial-statements). Adtech has real fraud at industrial scale. Click farms, bot impressions, made-for-advertising arbitrage, [roughly $84 billion a year](https://fraudblocker.com/ad-fraud-data-facts) of intentional fake entries, hunted by an entire vendor tier: DoubleVerify, CHEQ, HUMAN. Hunted, not stopped. A click costs nothing to fake, so detection is a permanent arms race, and $84 billion is the steady state with the hunters at full employment. The durable defense against fake entries was never better detection; it is [settling on events that cost the faker real money](/adtech-from-1887), which is where this post ends up anyway.

The platforms' disease is different, and it has a name from finance. Marking to model is ordinary practice; every bank carries [Level 3 assets](https://en.wikipedia.org/wiki/ASC_820) whose value is an estimate. What finance learned from [Enron](https://en.wikipedia.org/wiki/Enron_scandal) was not to abolish the mark but to cage it: a hierarchy that flags which numbers are estimates, disclosure of the model's inputs, independent verification of the model itself. A modeled conversion is a Level 3 estimate with no cage. No flag distinguishes it from an observed record, no inputs are disclosed, no outside party verifies the model, and the modeler is the counterparty whose bidding system spends your budget against the estimate.

| | Fraud | Mark-to-model |
|---|---|---|
| Entry | fabricated event | estimate booked as a record |
| Author | third parties | the platform itself |
| Policed by | DoubleVerify, CHEQ, HUMAN | nobody |
| Example | click farms, Honey | modeled conversions |

Be precise about what this means: the numbers are not unfalsifiable. [eBay famously falsified them](https://www.nber.org/papers/w20171): it turned off paid search in holdout markets and watched sales barely move. Geo holdouts do this routinely.

What the numbers are is unauditable entry by entry. Falsification works only in aggregate, and it costs fifty thousand dollars an attempt. The incrementality tier is the market price of a single falsification test. That is what missing source documents cost. Not "you can never know." "Knowing anything costs a study."

## The receiving dock advertising used to have

The claim here is not that advertising never had controls. Advertising invented the delivery audit. Advertisers founded the [Audit Bureau of Circulations](https://en.wikipedia.org/wiki/Audit_Bureau_of_Circulations) in 1914 to independently verify publisher-claimed circulation. Broadcast ran on notarized affidavits of performance: a station officer attesting, under oath, that the spots aired, and agencies paid against the affidavit rather than the station's say-so. An attested goods receipt, decades before anyone said adtech.

Digital kept more of this than the horror stories suggest. The [MRC accredits](https://blog.google/products/ads/transparency-choice-ads-measurement/) Google's clicks, served impressions, viewability, and invalid-traffic filtering. DoubleVerify and IAS measure rendering from outside. Ad servers on the buy side produce independent impression counts, and discrepancy reconciliation with contractual thresholds and makegoods is standard on guaranteed buys.

Now read what that list covers.

| Question | Control | Status |
|---|---|---|
| Was the ad delivered? | MRC accreditation, verification vendors, makegoods | audited |
| Did a conversion happen? | your CRM, your bank statement | your own books |
| Which ad touched it? | a click ID, if it survives the journey | unjoined |
| Did the ad cause it? | holdout experiments | $50k per answer |

Delivery is audited. Conversion claims are not. Conversion claims are what the money follows.

The metric that tCPA spends against, the metric renewals are justified by, the metric these seven ledgers disagree about, lives in rows two and three, and no accreditation touches it. MRC accredits the impression; nobody accredits the conversion.

Regulators are not the missing cavalry here, and the reason is structural. Enforcement needs an evidence surface, and the visible interface is the only place adtech generates one, so the FTC's advertising docket is labels, disclosures, and consent.

Two attacks on the counting layer, one congressional and one judicial, mark the frontier. In 1963 the Harris hearings caught ratings services fabricating figures, and the industry pre-empted regulation by founding [what became the MRC](https://www.mediaratingcouncil.org/about-mrc/history-of-mrc), whose audit perimeter froze at what 1964 could verify (delivery) and never moved. In 2018 advertisers sued Meta over a [Potential Reach metric inflated 200 to 400 percent](https://www.cohenmilstein.com/case-study/dz-reserve-et-al-v-facebook/); eight years later there is no verdict, and the metric at issue is still only an audience estimate, not the outcome ledger. The enforcement frontier is the auditability frontier. Receipts don't compete with regulation; they are its prerequisite.

I can report what this enforcement regime pays out at the end of its pipeline, because it paid me this year. The Facebook Consumer Privacy User Profile Litigation, the [Cambridge Analytica case](https://en.wikipedia.org/wiki/Facebook%E2%80%93Cambridge_Analytica_data_scandal), $725 million, the largest privacy class-action settlement in U.S. history, eight years from filing to my inbox. My share came to $42.03, in two installments: $35.30 in October, and a residual $6.73 in June.

Note the craft: the administrator ran a multi-round distribution with a true-up to get my forty-two dollars exactly right, which is more reconciliation than the industry it was punishing applies to [a trillion dollars a year](https://www.warc.com/content/feed/global-advertising-to-top-1-trillion-in-2024-as-big-five-attract-most-spending/8558). I have the receipts. They're the only ones this industry has ever sent me. The residual cheque landed eight days after Google moved offline-conversion uploads into its new API: litigation cycles in eight years, and the counting layer redesigns itself in a quarter.

## If corporate finance worked like adtech

Port the norms over and watch them in daylight.

Your supplier's delivery confirmation is written by the supplier. There is an independent inspector at the loading dock, but the metric your renewal depends on is "units that increased your profit," and that number the supplier calculates itself by a method it doesn't disclose, and updates while you sleep.

The bank sends no statement for the account that matters. It sends a performance dashboard where the figure is modeled, the model's inputs are the bank's, and the dashboard's own help page explains why it will never match your books.

The performance calculation that decides your biggest vendor's renewal is defined by that vendor, and the definition changes via a help-center article.

Quarterly close: your controller downloads seven CSVs with no shared key, and the reconciliation procedure is a YouTube course, updated whenever the counterparty renames a column.

No officer ever certifies the outcome numbers. Delivery gets audited, contracts get signed, makegoods happen. The figure the money actually follows carries no attestation and no restatement, because there is no record to restate.

This arrangement has been tried. British railway companies self-reported earnings to distant shareholders, and the scandals that followed put mandatory audit into the [Companies Act 1900](https://en.wikipedia.org/wiki/Companies_Act_1900). Corporate finance doesn't work like adtech because controls made honesty cheaper than fraud. Same species, different instruments.

## The platforms' defense

The platforms have a defense, and most of it is true. Conversions happen in systems they cannot observe. ATT and GDPR destroyed the identifiers that carried the join, and modeling is the legally compelled patch; Meta's conversion modeling is explicitly an ATT response. Deterministic records are not automatically truer: tags fail, CRM stages are dirty, uploads arrive biased. The models are validated against observed conversions and confidence-thresholded. Real-time bidding cannot wait for audited revenue. And independent verifiers cannot be handed user-level data, because privacy constraints are real, not a convenient excuse.

Concede all of it. Two things survive every concession.

First: the models are validated by the modeler. Nothing in the defense explains why the platform should be the sole producer, validator, reporter, and spender of the estimate that decides its own revenue. In any other industry that sentence is a segregation-of-duties finding, and the audit ends early.

Second: the privacy argument assumes the join must be identity. Historically it was, so privacy and auditability came to feel like a tradeoff. They aren't one. A [blind-signature coupon](/adtech-from-1887) proves a conversion happened and which batch it came from, without identifying the customer to anyone, including the advertiser. That is more privacy than hashed-email matching inside a black box, not less, and it is auditable by anyone holding the batch's public record. The platforms' best argument is an artifact of the receipt never having been designed.

## Modeling is what you do without receipts

Multi-touch attribution, media mix models, incrementality studies: inference machinery. The industry does statistics because the accounting is impossible, and calls it methodology.

The platforms' response to the missing join has been to move the join inside. Enhanced Conversions matches hashed identity within Google's systems. On [June 15, 2026](https://ads-developers.googleblog.com/2026/05/changes-to-offline-click-conversion.html), offline-conversion uploads migrated to the Data Manager API. Stated precisely: nothing was exported away, and the advertiser keeps its own records. What the payer loses is the ability to recompute the match. The books stay on both sides; the reconciliation moved inside one of them.

Modeling has a legitimate home: optimization. Bid on models, learn on models. What a model cannot be is the source document the money follows.

And the same boundary runs the other way: a receipt proves the touch and the conversion, never the cause. Receipts don't replace incrementality testing. They give it inputs that haven't been tampered with, because you cannot run causal inference on forged data. Source documents constrain the model; they cannot replace the counterfactual.

## The curriculum teaches feeding, not auditing

There is an empirical check on everything above: what the industry teaches itself.

[MeasureSchool](https://measureschool.com/offline-conversion-tracking/), Analytics Mania, and every mid-tier agency publish complete guides, on top of the hundred-plus listed courses. An education industry that size is a pain receipt: nobody teaches a hundred courses on a solved problem.

Now read the syllabus: it is upload-side, all the way down. Capture the click ID. Store it on the CRM contact. Fire the webhook on the lifecycle change. Push your conversion truth into the platform, so its bidding optimizes against better data. Course after course teaches the advertiser to feed the black box more accurately. A reconciliation course, one that teaches checking what the platform claims against your own books, I could not find. If one exists, send it to me. At this scale, its absence is the point either way.

The syllabus also has a shelf life, and Google sets it. Enhanced conversions replaced click-ID-only imports. The settings merged in April 2026. The API path moved in June. Every flagship tutorial carries an "updated for 2026" because the platform keeps invalidating the textbook. A procedure has to track the platform's renames forever. A receipt is true regardless.

## The channel with no books

Everything above describes the web, where the audit that survives works off one assumption: there is an artifact. A page that can be crawled, a tag that can be wrapped, a pixel that can be verified. The MRC's viewability standard, DoubleVerify's measurement, an archived screenshot: all of it inspects the artifact from outside.

An ad inside an AI conversation has no artifact. The impression is a sentence in a private chat. There is no page to crawl, no tag to wrap, no third-party script inside the answer. Even the delivery-side audit, the half advertising still has, sees nothing here.

The field evidence is young and already self-graded. [Koah](https://www.adweek.com/media/koah-adsense-for-chatgpt-series-a/) calls itself AdSense for GenAI, raised over twenty million dollars on the pitch, and [reports](https://www.prnewswire.com/news-releases/koah-launches-adsense-for-genai--monetization-standard-for-ai-chat-apps-302550115.html) a 7.5% click-through rate, four times the industry standard, with CPMs four to five times other platforms. Every number is self-reported, and there is no verification surface on which an independent number could stand. Nothing to accredit, nothing to wrap, nothing to crawl.

Nobody has defined the units, either: what is an impression inside a generated answer? The brand was named? Recommended? Compared favorably? The line between a labeled placement and a paid answer is a field in the network's server. OpenAI, selling ads inside ChatGPT, promises [answers stay independent](/impressions-and-clicks), a promise checkable by no one outside OpenAI.

The closest thing this channel has to an auditor is synthetic prompt monitoring, which polls the model with test questions. That is not auditing the books. That is calling the store to ask if your ad ran.

None of this is technically inevitable, which is exactly the point. The old channel's receiving dock was demolished; this one was never poured. And nothing outside the conversation can inspect a conversation, so the only audit this channel can ever have is one designed into the payload. The receipt rides in the answer or it doesn't exist.

| | Web | AI conversation |
|---|---|---|
| Artifact | page, tag, pixel | a sentence in a private chat |
| Delivery audit | MRC-accredited | none |
| Conversion claims | taken on faith | taken on faith |
| Retrofit | periscope possible | the receipt rides in the answer, or nothing |

The old channel audits delivery and takes conversion claims on faith. The new one takes both on faith.

## The boring fix

Accounting problems are not solved by smarter statistics. They are solved by controls so boring nobody writes think-pieces about them: source documents, counterparty records that agree by construction, independence of the counter from the counted.

You can run the frame today, without anyone's permission. Treat the bank statement and the CRM as your only books, and everything platform-side as unaudited counterparty claims. Label modeled numbers as estimates in your own client reporting; that is the flag the platforms omit. Budget one falsification test a year, a real holdout, and treat it as the audit fee.

And ask the question the frame generates on its own. Every company past a certain size has a controller, the person whose job is that the books be true. Who is the advertiser's controller for media spend?

The instruments for the full fix exist and are old. A [cryptographically signed coupon](/adtech-from-1887) is a receiving report: signed by the advertiser at issuance, presented at conversion, verifiable by anyone, and scoped honestly, since it proves the touch and the redemption and never the cause.

![Three-way match in corporate finance versus adtech's one-way match](/assets/one-way-match-light.svg)

A [per-batch public ledger](/croupier) is a shared trial balance: batch sizes and redemption counts on public record, with arithmetic anyone can replay. Two parties, one record, nothing to reconcile, because the entry is the counterparty record. Accounting scholarship has proposed the same shape for reconciliation in general, recording each transaction once on a shared ledger that both parties' books then consume ([Gomaa et al., 2023](https://publications.aaahq.org/jeta/article-abstract/20/1/59/183/The-Creation-of-One-Truth-Single-Ledger-Entries)); advertising is the industry that needs it most and has it least.

Two ratchets make this more than a proposal. [Transparency is irreversible](/transparency-is-irreversible): the first channel that offers an outcome-side receiving report forces every other channel to explain to a CFO why it won't, and CFOs already believe in the three-way match; nobody has to sell them the concept, only the dock. And the buyer is becoming software. Ad buying is going agentic, with agent-to-agent auction protocols already in draft, and "trust me" is a rhetorical form. It does not parse for a buying agent evaluating machine-checkable claims. Automation on top of unreconciled books doesn't fix them; it launders them faster, and the agents' owners will figure that out. In an agent-mediated market, receipts stop being a preference and become a protocol requirement.

An ad channel is a claim about what happened to money. The first channel whose claim checks itself is a different kind of ledger.

---

*Every quote and figure here was checked against its original source.*

*Part of the [Vector Space](/vector-space) series.*
