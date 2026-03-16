# What Is Cryptographic Ad Attribution?

*March 2026 | Croupier Blog*

Cryptographic ad attribution is a method of measuring advertising performance using signed tokens instead of cookies or tracking pixels. The advertiser issues the tokens, the publisher distributes them, and the customer carries them to the point of conversion. No intermediary reports the results — the advertiser verifies their own signatures.

## The Problem It Solves

Digital ad attribution has depended on cookies and pixels since the 1990s. The publisher fires a pixel. The platform drops a cookie. At conversion, the advertiser's tracking code checks for the cookie and credits the channel.

This model has three structural weaknesses:

1. **Cookies can be overwritten.** Any browser extension, toolbar, or script with access to the cookie jar can swap the tracking value. The PayPal Honey scandal showed this at scale.
2. **Pixels can be spoofed.** Bot traffic triggers impression and click pixels at industrial scale. The advertiser pays for events that never involved a human.
3. **The platform self-reports.** The entity selling impressions is the same entity measuring their effectiveness. There is no independent audit.

Cryptographic attribution addresses all three by moving the proof of attribution from the platform to the advertiser.

## How It Works

The mechanism borrows from the oldest form of ad attribution: the coupon.

**1. Issue.** The advertiser generates a batch of cryptographically signed tokens — digital coupons. Each token carries the advertiser's signature but reveals nothing about the customer or the offer value.

**2. Distribute.** The advertiser deposits the coupon book with a relay service. The publisher pulls the book and embeds one token per ad impression. The token rides in a query parameter, the same shape as a UTM tag.

**3. Carry.** The customer's device carries the token from the ad to the conversion event. No server-side redirect. No cookie. The token is a signed blob attached to the ad click URL.

**4. Verify.** At conversion, the customer's device presents the token. The advertiser checks their own signature. If it's valid, the conversion is attributed to the publisher who distributed that coupon book. If not, it's discarded.

The advertiser counts how many tokens came back from each publisher. Publisher A: 80 out of 1,000 redeemed (8%). Publisher B: 3 out of 1,000 (0.3%). Those are the advertiser's numbers, generated from their own cryptographic signatures.

## The Cryptography

Two primitives make this work:

**Public-key signatures.** The advertiser signs each token with their private key. Anyone can verify the signature with the public key, but only the advertiser can create it. A forged token fails verification. This is the same math behind HTTPS certificates — proven, standardized, fast.

**Blind signatures.** Invented by David Chaum in 1983, blind signatures let the advertiser sign a token without seeing its contents. The publisher can verify "this is a real token from a real advertiser" without the advertiser learning which specific token went to which impression. The batch is the anonymity set.

The IETF standardized this pattern in RFC 9578 (Privacy Pass). Apple uses it for Private Click Measurement in Safari. Brave uses it for anonymous ad confirmations. The building blocks are production-grade.

## What Each Party Sees

Cryptographic attribution enforces selective disclosure by math, not by policy:

| Party | What they see | What they don't see |
|---|---|---|
| Advertiser | Redemption count per publisher, conversion rate | Which individual redeemed which token |
| Publisher | "This is a real offer from a real advertiser" | Offer value, customer identity |
| Customer | The discount or offer | Which publisher they came from (after redemption) |
| Relay (Croupier) | Envelope counts | Token contents, signatures, conversion data |

No party has the full picture. Privacy is structural, not contractual.

## How It Compares

| | Cookie-based | Platform pixel | Cryptographic coupon |
|---|---|---|---|
| Who issues | Platform | Platform | Advertiser |
| Who measures | Platform | Platform | Advertiser |
| Hijackable | Yes (cookie overwrite) | Yes (pixel spoofing) | No (signature verification) |
| Privacy model | Policy (can be changed) | Policy (can be changed) | Math (can't be changed) |
| Requires trust in | Platform | Platform | Cryptography |

## Getting Started

The infrastructure for cryptographic attribution is simple:

1. **Generate a signing key.** Standard RSA or ECDSA key pair.
2. **Sign a batch of tokens.** A few lines of code using any crypto library.
3. **Deposit the coupon book.** Push the batch to a relay like [Croupier](https://github.com/kimjune01/croupier).
4. **Publisher pulls and embeds.** One token per impression, appended as a query parameter.
5. **Verify at conversion.** Check the signature at your conversion endpoint.

A proof-of-concept implementation exists in about 250 lines of TypeScript. The relay adds managed hosting, uptime, and integrations on top.

The math has been production-grade for 40 years. The ad industry just hasn't used it yet.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
