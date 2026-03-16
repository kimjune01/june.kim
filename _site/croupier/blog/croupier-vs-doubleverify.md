# Croupier vs DoubleVerify: Verification Is Not Attribution

*March 2026 | Croupier Blog*

DoubleVerify processes over 8 trillion media transactions per year. Their pitch: we verify that your ads were seen by real humans in brand-safe environments. They charge a CPM fee — roughly $0.50-$2.00 per thousand impressions verified.

In March 2025, Adalytics published a 240-page report showing DV missed 21% of bot visits in their sample. The bots were "declared bots" operating from known data center IPs — the easiest category to detect. DV's stock dropped 36% in a day.

But even if DV caught every bot perfectly, it wouldn't solve the attribution problem. Verification and attribution are different questions.

## What DoubleVerify Does

DV operates at two stages:

**Pre-bid:** Targeting segments inside DSPs that block fraud or unsafe content before the advertiser bids. The goal is to avoid buying garbage impressions.

**Post-bid:** Verification tags that fire alongside ads to measure viewability (was the ad in the viewport?) and detect bots (was the viewer human?). Brand safety classification checks whether the page content is appropriate.

DV tells you: "This impression was viewable, the traffic was human, and the content was brand-safe." It does not tell you: "This impression led to a conversion."

## Where Verification Falls Short

**It misses fraud.** The Adalytics report documented systematic detection failures. IAS labeled confirmed bot traffic as valid human visitors 77% of the time. These weren't sophisticated adversaries — they were declared bots from known data centers. If verification can't catch the easy cases, the hard cases go entirely undetected.

**It serves both sides.** DV and IAS provide services to both advertisers (who want fraud blocked) and publishers/exchanges (who want inventory to pass verification). When verification companies flag too much inventory as fraudulent, they threaten the revenue of the platforms they also serve. The conflict is structural.

**It answers the wrong question.** An impression can pass every verification check — real human, real device, brand-safe page — and still deliver zero value. The viewer scrolled past it. They were on the page for other reasons. The ad was technically viewable but practically invisible. Verification confirms the impression existed. It says nothing about whether the impression worked.

**It doesn't prevent waste.** The ANA found that a typical campaign ran across 44,000 websites. DV can flag the obviously bad ones, but "not fraudulent" and "not brand-unsafe" is a low bar. An AI-generated listicle farm with real human visitors passes verification. It just doesn't convert.

## How Croupier Differs

Croupier doesn't verify impressions. It verifies conversions.

| | DoubleVerify | Croupier |
|---|---|---|
| What it measures | Impression quality (viewability, safety, bot detection) | Conversion provenance (which channel drove this sale) |
| Question answered | "Was this ad seen by a human?" | "Did this channel produce a real conversion?" |
| Who controls it | DV (third-party scores) | Advertiser (own cryptographic signature) |
| What it catches | Bots, unsafe content, non-viewable placements | Non-converting channels |
| What it misses | Non-converting real impressions | Pre-impression quality (brand safety) |
| Pricing | CPM fee per impression verified | Flat monthly relay fee |
| Revenue model conflict | Serves both buyers and sellers | Serves neither (just passes envelopes) |

DV tries to filter bad impressions upstream. Croupier measures real conversions downstream. One is a screen door. The other is a receipt.

## Why Downstream Measurement Is Stronger

A bot farm that generates a million impressions per day will pass some fraction of DV's filters. The industry has spent a decade building better filters, and bot traffic has grown every year — from 25% to 37% of all web traffic in six years. The filters aren't winning.

But bots don't buy things. They don't fill out lead forms with real information. They don't subscribe to SaaS products. If the advertiser measures at the conversion endpoint instead of the impression endpoint, fraud self-selects out.

Issue 1,000 cryptographic coupons to a publisher. If 80 come back with valid signatures attached to real conversions, the channel works. If 0 come back, the channel doesn't — regardless of whether the impressions were "verified." The measurement inherently excludes bots because bots don't convert.

This doesn't catch every kind of fraud. A human click farm that makes real purchases would redeem real coupons. But that's a much more expensive and less scalable fraud than the impression-level bot traffic that currently dominates. Raising the cost of fraud from "run a bot" to "make a real purchase" is itself a significant improvement.

## Do You Need Both?

Verification and attribution solve different problems:

- **Brand safety** — you don't want your brand next to harmful content, even if the placement converts well. This is DV's domain.
- **Performance measurement** — you need to know which channels actually produce results. This is Croupier's domain.

You might run both. Use DV (or IAS, or HUMAN) for pre-bid filtering on brand safety. Use Croupier for conversion-level attribution.

But if you had to choose one, consider this: a verified impression that doesn't convert costs you money. An unverified channel that converts at 8% makes you money. Performance measurement is closer to the revenue event.

The ad industry has spent billions on verifying impressions. It might be time to start verifying conversions instead.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
