# After Third-Party Cookies: Attribution Without Tracking

*March 2026 | Croupier Blog*

Google delayed third-party cookie deprecation in Chrome four times before settling on a prompt-based opt-out model in 2025. Safari and Firefox blocked them years ago. The industry has spent half a decade preparing for a world without third-party cookies, and most of the proposed replacements recreate the same problems in new packaging.

## What's Actually Changing

Third-party cookies let ad platforms track users across websites. Visit a shoe store, see shoe ads on a news site. The cookie connects the two visits.

Browsers are removing this capability because users didn't consent to cross-site tracking and regulators (GDPR, CCPA) increasingly require consent that most sites can't meaningfully obtain.

But the advertiser's real need was never to track users across the web. It was to know which ad channels drove conversions. Tracking was the implementation, not the goal. Attribution was the goal.

## The Replacement Landscape

The industry's responses fall into a few categories:

**Cohort-based approaches (Topics API, formerly FLoC).** Group users into interest categories. The browser reports "this user is interested in running shoes" rather than a unique identifier. Advertisers target cohorts instead of individuals. But cohorts still require the browser to profile the user. The privacy gain is marginal — the surveillance moves from individual to group-level.

**Server-side tracking.** Move the tracking pixel from the browser to the server. Harder for ad blockers to stop, but the same architecture: the platform reports its own numbers. Server-side tracking solves a technical problem (browser restrictions) without solving the trust problem (self-reported metrics).

**Data clean rooms.** Advertisers and publishers upload first-party data to a neutral environment for matching. This works for large brands with significant first-party datasets but requires sharing customer data with a third party, which is what privacy regulation was trying to prevent.

**Probabilistic fingerprinting.** Infer identity from browser characteristics, IP addresses, and behavioral signals. Explicitly banned by most browser vendors and regulators. A non-starter for any compliant operation.

**Privacy Sandbox (Attribution Reporting API).** Google's browser-mediated attribution. The browser itself becomes the attribution engine, reporting aggregate conversions with noise added for privacy. Better than cookies, but the browser vendor controls the measurement infrastructure. If that vendor is also the largest ad platform, the conflict of interest shifts rather than disappears.

## What's Missing

Every replacement above keeps the same directional flow: information goes from the user's browser to the ad platform, and the platform reports results back to the advertiser.

The advertiser is still a passenger. They receive reports. They don't generate proof.

The alternative is to flip the direction. Instead of the platform reporting "we showed your ad and it converted," the advertiser issues a signed token that travels with the ad and comes back at conversion. The advertiser verifies their own signature. No platform report needed.

## Bearer Attribution

The concept is old. Coca-Cola used numbered coupons in 1887. The customer carried the proof from the ad to the point of sale. The advertiser counted redemptions per publication.

Cryptographic coupons are the digital version. The advertiser signs a batch of tokens. The publisher embeds one per impression. The customer's device carries it. At conversion, the advertiser checks the signature. Publisher A converts at 8%. Publisher B at 0.2%.

No cookie required. No cross-site tracking. No browser API dependency. The token is a signed blob in a URL parameter — it works in any browser, any app, any environment that can pass a query string.

This is why it survives cookie deprecation: it never depended on cookies in the first place.

## Privacy Without Compromise

The privacy properties of cryptographic coupons are stronger than any cookie replacement:

- **No user tracking.** The token identifies the channel, not the person. The advertiser learns "Publisher A converts at 8%" but can't identify which individual redeemed which token.
- **No browser profiling.** No cohorts, no fingerprinting, no interest categories. The browser doesn't need to know anything about the user's ad preferences.
- **No data sharing.** The advertiser and publisher never exchange customer data. The coupon is the join between impression and conversion.
- **Blind relay.** The infrastructure that passes coupon books between parties never reads the contents. [Croupier](https://github.com/kimjune01/croupier) is built this way — it moves sealed envelopes without opening them.

The math enforces the privacy. Not a policy, not a terms-of-service clause, not a browser setting that can be changed in the next update.

## What To Do Now

If you're planning for a post-cookie world:

1. **Stop rebuilding the cookie.** Solutions that replicate cross-site tracking with different technology will face the same regulatory and browser resistance.
2. **Invest in first-party measurement.** The advertiser who controls their own attribution is not affected by browser changes.
3. **Test cryptographic attribution.** Run a parallel campaign with signed tokens alongside your existing setup. Compare the results.

The cookie is going away because it was a surveillance tool repurposed for attribution. The replacement should be an attribution tool that doesn't require surveillance.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
