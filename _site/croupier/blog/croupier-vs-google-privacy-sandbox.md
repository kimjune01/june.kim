# Croupier vs Google Privacy Sandbox: Why the Browser Shouldn't Own Attribution

*March 2026 | Croupier Blog*

Google's Privacy Sandbox was supposed to be the post-cookie future of ad attribution. Chrome would handle attribution natively — matching ad impressions to conversions inside the browser with differential privacy to protect user identity.

In October 2025, Google retired it due to low adoption. But the failure is instructive. The problem wasn't the technology. It was the architecture: giving the browser vendor control over attribution when the browser vendor is also the world's largest ad platform.

## What Privacy Sandbox Promised

The Attribution Reporting API registered "attribution sources" (ad clicks and views) and "triggers" (conversions) inside Chrome. Event-level reports provided limited bits of conversion data with randomized noise. Summary reports aggregated across users inside a Trusted Execution Environment (TEE).

The privacy properties were real. Individual users couldn't be tracked. Conversion data was noised. Aggregation happened in a secure enclave.

## Why It Failed

**Google controlled every layer.** The browser decided what got attributed. Google set the noise levels. Google ran the TEE. The advertiser received a report and had to trust it. There was no way to independently verify the raw data — it only existed decrypted inside Google's enclave.

**It only worked in Chrome.** Safari and Firefox had already blocked third-party cookies and had no reason to adopt Google's API. Attribution that only works in one browser isn't attribution — it's a platform feature.

**It favored Google ads.** The system was "virtually guaranteed to over-value Google ads" because it dealt with Google's ecosystem and assumed that an ad shown meant the ad drove the sale. The attribution logic ran inside the product sold by the company being measured.

**Nobody adopted it.** Google reversed course on cookie deprecation in July 2024, removing the forcing function. Without mandatory cookie removal, ad networks had no reason to migrate to a Google-controlled API. The Privacy Sandbox APIs became optional alternatives rather than mandatory replacements.

## The Deeper Problem

Privacy Sandbox failed not because privacy-preserving attribution is impossible, but because the industry rejected an architecture where the largest ad seller also controlled the measurement infrastructure.

This is the same conflict that exists in every self-reporting system. Google Ads reports Google Ads performance. Meta Ads reports Meta Ads performance. Privacy Sandbox formalized this conflict into a browser API and expected competitors to adopt it.

## How Croupier Differs

Croupier's architecture eliminates the conflict by putting the advertiser in control of attribution.

| | Google Privacy Sandbox | Croupier |
|---|---|---|
| Who controls attribution? | Google (browser) | Advertiser (signing key) |
| Where does attribution run? | Inside Chrome's TEE | At advertiser's conversion endpoint |
| Can advertiser verify raw data? | No (only aggregated, noised reports) | Yes (verify own signatures) |
| Cross-browser? | No (Chrome only) | Yes (token is a URL parameter) |
| Cross-platform? | No (browser only) | Yes (works in apps, email, podcasts) |
| Privacy mechanism | Differential privacy (noise) | Blind signatures (unlinkability) |
| Depends on browser vendor? | Yes | No |
| Status | Dead (retired Oct 2025) | Active |

The privacy properties are different too. Privacy Sandbox added noise to make individual conversions probabilistic — you couldn't be sure any single conversion really happened. Croupier uses blind signatures to make conversions unlinkable — each conversion definitely happened (valid signature), but the advertiser can't link it to a specific user. Certainty about the event, privacy about the person.

## What Privacy Sandbox Got Right

The diagnosis was correct. Third-party cookies are a surveillance tool. Attribution should work without cross-site tracking. Users deserve privacy by default.

But the prescription — "trust Google's browser to handle attribution in a way that's fair to Google's competitors" — was never viable. Firefox and Safari declined. The EU flagged the antitrust implications. Advertisers questioned why they should trust Google's black box.

The right architecture separates the attribution infrastructure from the ad-selling business. The relay that passes coupon books doesn't sell ads. The advertiser who verifies signatures doesn't depend on the relay. The browser doesn't need to understand attribution at all — it just passes a URL parameter.

## The Open Standard Alternative

Privacy Sandbox tried to replace an open web standard (cookies) with a proprietary browser API. It was a closed replacement for an open problem.

Croupier builds on an actual open standard: Privacy Pass (RFC 9578), ratified by the IETF. The token format is standardized. The blind signature math is standardized. Anyone can implement it.

If a single company controls the standard, adoption depends on trusting that company. If the standard is open, adoption depends on the math. The math has been proven since 1983.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
