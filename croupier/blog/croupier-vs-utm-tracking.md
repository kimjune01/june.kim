# Croupier vs UTM Tracking: Why Signed Tokens Beat Plain-Text Parameters

*March 2026 | Croupier Blog*

UTM parameters are the most widely used attribution system in digital advertising. Every marketer has appended `?utm_source=facebook&utm_medium=cpc&utm_campaign=spring_sale` to a URL. Google Analytics reads these parameters and credits the traffic source.

UTMs are also trivially forgeable. They're plain-text strings in a URL that anyone can copy, modify, or inject. That's the problem Croupier solves.

## How UTM Attribution Works

The advertiser appends UTM parameters to their campaign URLs. When someone clicks the link and lands on the site, Google Analytics (or any analytics tool) reads the parameters and associates the session with that traffic source. If the visitor converts, the conversion is attributed to the UTM source.

There is no verification. No signing. No proof that the UTM parameter was placed by the advertiser or the publisher it claims to represent. The parameter is a label, not a receipt.

## Where UTMs Break

**Anyone can write them.** A fraudster can create a link with `utm_source=premium_publisher` and drive bot traffic through it. The analytics dashboard shows conversions from "premium_publisher." The advertiser pays for traffic they didn't ask for and can't distinguish from real.

**Browser extensions overwrite them.** The Honey scandal showed this at industrial scale. At checkout, Honey replaced affiliate tracking parameters with its own. The creator who drove the sale lost attribution because the last URL parameter wins. UTMs have the same vulnerability.

**They fragment easily.** UTMs are case-sensitive. `utm_source=Facebook` and `utm_source=facebook` create two separate traffic sources in your reports. Studies show up to 40% of attribution is lost to poor UTM persistence and inconsistent naming.

**They reveal campaign strategy.** UTMs are visible in the URL bar. Competitors can see your campaign names, source labels, and targeting structure just by clicking your ads.

**They don't survive ad blockers or consent rejection.** In privacy-conscious markets, 30-50% of traffic is lost when users reject tracking consent. The UTM parameter may arrive, but the analytics tool can't store it.

## How Croupier Differs

Croupier replaces the UTM with a cryptographically signed token — a coupon that rides in the same position (a URL query parameter) but has fundamentally different properties.

| Property | UTM Parameter | Croupier Coupon |
|---|---|---|
| Format | Plain-text string | Cryptographically signed token |
| Issued by | Anyone (manually typed) | Advertiser (private key) |
| Verified by | Nobody (read-only label) | Advertiser (signature check) |
| Forgeable | Yes, trivially | No (requires private key) |
| Overwritable | Yes (last write wins) | No (signature is bound to issuer) |
| Reveals strategy | Yes (visible in URL) | No (opaque blob) |
| Proves causation | No (correlation only) | Yes (signed proof of issuance) |

The coupon is the same shape as a UTM tag — a query parameter appended to a URL. Publishers embed it the same way. The customer's click carries it to the conversion page. But at conversion, the advertiser checks the cryptographic signature instead of reading a plain-text label.

If the signature is valid, the conversion is attributed. If not, it's discarded. No ambiguity. No fragmentation. No spoofing.

## What You Keep

Switching from UTMs to cryptographic coupons doesn't mean throwing away your analytics stack. You keep:

- **Campaign structure.** The advertiser defines campaigns when issuing coupon books. The books are labeled, not the tokens.
- **Channel comparison.** Issue separate coupon books per publisher. Count redemptions per book. Publisher A: 8% conversion. Publisher B: 0.2%.
- **Google Analytics.** You can run UTMs alongside coupons during a transition period. Compare platform-reported conversions to coupon-verified conversions. The gap tells you how much your current attribution is inflated.

## What You Gain

- **Forgery-proof attribution.** A signed token can't be faked without the advertiser's private key.
- **Hijack resistance.** No browser extension can overwrite a cryptographic signature. The Honey attack vector doesn't exist.
- **Advertiser-controlled measurement.** You count your own redemptions. No platform reports its own performance to you.
- **Privacy by design.** The coupon identifies the channel, not the person. The batch is the anonymity set.

## Getting Started

The migration path is straightforward:

1. **Generate a signing key.** Standard RSA or ECDSA.
2. **Issue coupon books per campaign.** Deposit them with the [Croupier relay](https://github.com/kimjune01/croupier).
3. **Publishers pull and embed.** One token per ad impression, appended as a query parameter.
4. **Add a verification snippet.** A few lines of code at your conversion endpoint that checks the signature.
5. **Run in parallel.** Keep UTMs active while you build confidence in coupon-verified numbers.

UTMs were a reasonable solution in 2005 when the web was simpler and tracking wasn't adversarial. In 2026, they're a plain-text honor system in an environment full of forgery. The fix is the same shape — a URL parameter — with cryptographic proof behind it.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
