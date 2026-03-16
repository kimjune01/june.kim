# Why Your Ad Attribution Numbers Are Wrong

*March 2026 | Croupier Blog*

You check your ad dashboard every morning. ROAS looks healthy. Conversions are up. CPAs are within target. Everything is fine.

Except the numbers are self-reported by the platform selling you the impressions.

## The Fox Guards the Henhouse

Google Ads reports Google Ads performance. Meta Ads reports Meta Ads performance. Each platform runs its own measurement, its own attribution model, and its own reporting dashboard. The entity selling you inventory is the same entity telling you how well it performed.

This isn't a conspiracy theory. It's an incentive structure. When the seller also controls the measurement, there is no external check on accuracy.

The ANA's 2023 programmatic transparency study found that only 36 cents of every programmatic dollar entering a DSP reached end consumers. The rest disappeared into intermediary fees, non-viewable placements, and made-for-advertising sites. Most advertisers never saw this breakdown because they relied on platform-reported metrics.

## What Gets Miscounted

Attribution errors compound in several ways:

**View-through inflation.** A platform counts a "view" and then claims credit for any conversion within a window — even if the user never noticed the ad. A 24-hour view-through window on a high-traffic network captures enormous amounts of organic conversions.

**Cross-device guessing.** Platforms use probabilistic models to link devices. User sees an ad on mobile, converts on desktop — the platform claims the attribution. The accuracy of these models is not auditable by the advertiser.

**Last-click wars.** Multiple platforms claim credit for the same conversion. An advertiser running Google, Meta, and TikTok ads simultaneously will see all three platforms take credit for overlapping conversions. Add them up and your attributed conversions exceed your actual sales.

**MFA dilution.** Performance Max and similar black-box products blend premium and junk inventory. The advertiser sees aggregate performance. A campaign running across 44,000 websites (per the ANA study) includes sites the advertiser has never heard of and would never choose.

## The Numbers Don't Add Up

A common exercise: export attributed conversions from every platform you advertise on. Sum them. Compare to your actual revenue.

If the total attributed conversions are 30-50% higher than real conversions, your attribution is counting duplicates. If you can't reconcile them at all, the platforms are operating on incompatible definitions of what counts.

This isn't a rounding error. It's a structural feature of siloed measurement. Each platform optimizes its own attribution model to make itself look good.

## What Independent Measurement Looks Like

The alternative is advertiser-side measurement — attribution that the advertiser controls, not the platform.

This means the proof of attribution originates with the advertiser and travels through the ad channel, rather than being reported back by the channel.

Cryptographic attribution does this with signed tokens. The advertiser issues a batch of signed coupons to a publisher. The publisher embeds one per impression. At conversion, the customer presents the coupon and the advertiser verifies their own signature. No platform dashboard involved. The advertiser counts their own receipts.

Publisher A redeems 80 out of 1,000 coupons — 8% conversion rate. Publisher B redeems 1 out of 1,000 — 0.1%. These numbers belong to the advertiser. No intermediary reported them.

## Getting Started

You don't have to replace your existing ad stack to start measuring independently.

1. **Run a parallel test.** Issue cryptographic coupons alongside your existing campaigns. Compare coupon-verified conversions to platform-reported conversions.
2. **Start with one channel.** Pick your highest-spend publisher partnership and measure it with coupons for 30 days.
3. **Look for the gap.** The difference between platform-reported and coupon-verified conversions tells you exactly how much your attribution is inflated.

[Croupier](https://github.com/kimjune01/croupier) provides the relay infrastructure for running cryptographic coupon campaigns. The advertiser issues sealed coupon books, the publisher pulls them, and the relay never sees the contents.

The goal isn't to distrust every platform. It's to have your own numbers.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
