# PPC thin filter: competitive scan

Research date: 2026-07-13

## Product definition tested

The proposed thin filter performs four jobs:

1. capture an inbound form, call, or chat together with its ad identity;
2. classify the inquiry as spam, irrelevant, valid, qualified, or higher-value;
3. attach a stage and optionally a value;
4. return that event to Google Ads, Meta, or another ad platform for bidding.

## Finding

This is an existing product category, although it is fragmented. WhatConverts is the closest direct competitor found. CallRail offers a strong call-specific implementation. Ruler Analytics and several CRMs or connectors close the loop after a human or CRM workflow supplies the label. Google and Meta increasingly provide the destination goals and transport, and Google now provides a narrow form-native qualification feature.

The open question is therefore not whether anyone has built the loop. It is whether current products classify website-form submissions accurately, transparently, and cheaply enough for PPC operators who do not want to adopt a larger attribution or CRM suite.

## Supply map

| Supplier | Captures identity and inbound | Creates the quality label | Returns it to ad platform | Scope | Competitive significance |
|---|---|---|---|---|---|
| [WhatConverts](https://www.whatconverts.com/offline-conversion-tracking-for-agencies-clients/) | Calls, forms, chats; captures GCLID and lead context | Yes. Lead Intelligence uses user-defined rules to score, qualify, value, or disqualify leads | Yes, automatic Google Ads offline conversions | Lead tracking and attribution suite, agency-oriented | Closest direct incumbent. Its public description nearly matches the proposed loop |
| [CallRail Conversion Signals](https://www.callrail.com/blog/callrail-debuts-conversion-signals-to-improve-ad-targeting) | Calls and their acquisition source | Yes. Conversational AI detects requested and booked appointments | Yes, outcomes can be integrated into Google Ads | Primarily phone conversations | Direct incumbent for call-heavy local services, but not a general form-content filter |
| [Ruler Analytics](https://www.ruleranalytics.com/blog/ppc/google-ads-offline-conversions/) | Tracks click IDs, forms, calls, chats, CRM journey | Usually no. Qualification is represented by CRM stages such as MQL and SQL | Yes, sends stage and revenue events through offline conversion APIs | Attribution and revenue analytics | Covers the loop but generally consumes an organizational label rather than independently creating it |
| [Google Ads qualifying responses](https://support.google.com/google-ads/answer/17050941) | Google-hosted Search lead forms | Yes, but only by explicit qualifying answers chosen in the form | Native qualified-lead conversion goal | Google-hosted Search forms only | Platform encroachment on the thinnest rule-based version; does not classify arbitrary website forms after submission |
| [Google Enhanced Conversions for Leads](https://support.google.com/google-ads/answer/7012522) | Captures/matches GCLID and hashed first-party identifiers | No. Advertiser or CRM defines qualified and converted events | Native Google import and bidding feedback | Google Ads | Commoditizes identity matching and transport, not classification |
| [Meta conversion leads](https://www.facebook.com/business/ads/ad-objectives/lead-generation/lead-ads-with-forms) | Meta lead ID and CRM matching | No. Business/CRM supplies the downstream successful-conversion event | Native through Conversions API | Meta lead generation | Commoditizes the destination and learning objective, while leaving qualification upstream |
| [LeadsBridge](https://support.leadsbridge.com/hc/en-us/articles/44150618725652-How-do-I-build-a-bridge-with-Facebook-Conversion-Leads) | Maps Meta lead IDs into CRM workflows | No. Sends a chosen CRM stage, such as MQL | Yes, through Meta Conversions API | Integration middleware | Transport competitor rather than classifier |
| [OCT](https://www.offlineconversionstracking.com/) | Intercepts forms and stores GCLID | Manual: user marks converted and enters value | Produces Google-ready CSV | Lightweight Google-only tool | Demonstrates demand for a very small product, but leaves qualification to the operator |
| [Convertss](https://www.convertss.com/) | Captures click IDs and form/chat leads | Limited: manual, CRM webhook, or form-value trigger | Google, Meta, TikTok, and Bing | Lightweight multichannel loop | Close on transport and triggers; public material does not establish substantive post-submission classification |
| [CRMxDream](https://www.crmxdream.com/) | CRM stores the ad identity and sales flow | Human sales qualification | Google and Meta events | CRM for digital marketing | End-to-end operationally, but qualification belongs to telecallers rather than an independent filter |
| [Confilead](https://app.confilead.com/) | Central inbox for Google and Meta ad leads | Sales-quality workflow and score | Advertises ad feedback | Ad-lead operating layer | Very close emerging entrant; public page does not make automated classification quality clear |

## What is already commoditized

- GCLID capture and enhanced identity matching;
- qualified-lead and converted-lead goal types;
- CRM-to-platform event transport;
- manual stage changes and rule-based triggers;
- call transcription and appointment detection;
- form questions that disqualify a prospect before submission.

Building only a click-ID store plus an offline-conversion uploader would enter a mature integration market.

## Where a narrower opening may remain

The least clearly supplied element is a cross-platform, post-submission classifier for arbitrary website forms that:

- works without replacing the advertiser's form or CRM;
- distinguishes spam, irrelevant inquiries, existing customers, vendors, job seekers, and plausible prospects from the form's free text and metadata;
- lets the operator inspect, correct, and version the classification policy;
- learns from later human or CRM corrections;
- preserves deterministic click identity and returns provisional or revised labels quickly;
- exposes delivery failures and the exact event accepted by each platform;
- serves small PPC teams without requiring an attribution suite or enterprise sales process.

That is narrower than “offline conversion tracking.” It is also narrower than generic predictive lead scoring: its buyer, latency requirement, output vocabulary, and destination are defined by the PPC feedback loop.

## Falsifiers for the remaining opening

The opportunity weakens materially if customer research shows any of the following:

1. WhatConverts' rule engine already handles website-form qualification accurately enough at an acceptable price.
2. The information present at submission is insufficient; only a phone conversation or later sales interaction can determine quality.
3. Businesses cannot agree on a stable qualification definition, so classification remains a sales-management service rather than software.
4. Qualified-lead volume is too low for ad bidding, making the returned label useful only for reporting.
5. PPC practitioners prefer changing form questions, keywords, geography, or inventory over operating a downstream classifier.
6. Google or Meta absorbs arbitrary-form qualification into their native lead products.
7. Classification errors poison bidding more severely than raw-form noise, making operators unwilling to automate the label.

## Best next comparison

A product test should begin by giving the same historical lead set to a PPC operator, WhatConverts, and a proposed semantic classifier. Compare:

- agreement with the operator's final labels;
- false-positive rate on qualified leads;
- time from submission to returned event;
- percentage of leads retaining a usable platform identity;
- correction and audit effort;
- accepted event rate at Google and Meta;
- price and setup time.

Without outperforming the incumbent on that concrete task, the thin filter is a feature rather than an independent product.
