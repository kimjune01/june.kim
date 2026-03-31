# Croupier vs AppsFlyer: Why Mobile Attribution Still Trusts the Wrong Party

*March 2026 | Croupier Blog*

AppsFlyer is the market leader in mobile attribution. Their SDK sits inside your app, captures install and in-app events, and matches them against ad engagement data to determine which campaign drove each install. Billions of events daily. Thousands of app companies depend on it.

But AppsFlyer has a structural problem it can't fix: it depends on self-reported data from the ad networks it's supposed to measure.

## How AppsFlyer Works

You integrate AppsFlyer's SDK into your app. When a user installs and opens the app, the SDK fires an event to AppsFlyer's servers. AppsFlyer's attribution engine then matches this install against click and impression data from ad networks.

For most smaller networks, AppsFlyer uses its own tracking links — it sees the click, records the device ID, and matches it to the install. This works reasonably well.

The problem is Self-Reporting Networks (SRNs).

## The SRN Problem

Meta, Google, TikTok, and Snap are Self-Reporting Networks. They don't allow AppsFlyer to place tracking links in their ad units. Instead, when AppsFlyer notifies them of an install, the SRN checks its own records and reports back whether it showed an ad to that device.

AppsFlyer never sees the raw click or impression data from these networks. It receives a claim: "Yes, we showed an ad to this device before they installed." AppsFlyer applies its own attribution logic and deduplication, but the input data from the biggest networks is a black box.

As one industry analysis put it: "Members aren't privy to how Facebook decides what to take credit for."

Meta, Google, and TikTok represent the majority of mobile ad spend. The measurement partner that's supposed to arbitrate between advertisers and networks can't independently verify the data from the networks that matter most.

## Attack Vectors

Mobile attribution fraud is an industry:

- **Click injection.** Malware on the device detects when an app is being installed and fires a fake click just before the install completes, claiming credit.
- **SDK spoofing.** Fraudsters reverse-engineer the SDK communication protocol and send fake install events from non-existent devices.
- **Device farms.** Real devices, real installs, but done at scale by workers or automation to collect install bounties.

AppsFlyer's Protect360 catches some of these. But it's an arms race — fraud evolves, detection catches up, fraud adapts. The fundamental architecture hasn't changed: a third party collects signals and makes a judgment call about who gets credit.

## How Croupier Differs

Croupier doesn't arbitrate between competing claims. The advertiser issues signed tokens, the publisher distributes them, and the advertiser verifies their own signature at the conversion endpoint.

| | AppsFlyer | Croupier |
|---|---|---|
| Who decides attribution? | AppsFlyer (with SRN self-reported inputs) | Advertiser (signature verification) |
| Can the ad network inflate claims? | Yes (SRNs report their own data) | No (network can't forge advertiser's signature) |
| Click injection possible? | Yes (common attack vector) | No (token must be validly signed before distribution) |
| SDK spoofing possible? | Yes (protocol can be reverse-engineered) | No (can't forge cryptographic signature) |
| Requires SDK? | Yes (in-app SDK) | No (token in URL parameter) |
| Pricing | Per-conversion fee ($0.03-0.06) | Flat monthly relay fee |

The key architectural difference: AppsFlyer sits between the advertiser and the network, accepting data from both sides and making a judgment. Croupier doesn't sit between anyone. The advertiser issues the proof. The customer carries the proof. The advertiser verifies the proof. No intermediary makes an attribution decision.

## The Trust Gap

When you use AppsFlyer, you trust:

1. **AppsFlyer** to correctly match installs to ad engagement
2. **Self-Reporting Networks** to honestly report which devices they showed ads to
3. **The SDK** to not be spoofed or manipulated
4. **Protect360** to catch fraud that exploits any of the above

When you use Croupier, you trust:

1. **Cryptography** — that your signature can't be forged without your private key

The trust surface shrinks from four fallible entities to one mathematical property. Blind signatures have been proven secure since 1983. Privacy Pass (RFC 9578) standardized the token format. These aren't experimental — Apple, Brave, and Cloudflare run them in production.

## Where AppsFlyer Still Wins

AppsFlyer provides a full suite of mobile marketing tools that Croupier doesn't attempt:

- **Deep linking** — routing users to specific in-app content
- **Audience segmentation** — grouping users by behavior and campaign
- **SKAdNetwork / AdAttributionKit integration** — Apple-mandated attribution
- **Fraud analytics dashboard** — visualizing fraud patterns
- **Cohort analysis** — LTV by acquisition source

If you need a mobile marketing platform, AppsFlyer does a lot. But if the question is "which network actually drove this install, and can I prove it?" AppsFlyer's answer depends on trusting the networks it measures. Croupier's answer depends on math.

## Running a Parallel Test

The simplest way to evaluate: run cryptographic coupons alongside your AppsFlyer attribution for one campaign.

Issue a coupon book for a specific publisher. Have them embed tokens in their ad click URLs. At conversion (app install or in-app event), verify the signature at your endpoint.

Compare AppsFlyer's attributed installs for that publisher to coupon-verified installs. If the numbers match, your attribution is accurate. If AppsFlyer shows 1,000 installs and coupons verify 400, the gap is the question you need to answer.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
