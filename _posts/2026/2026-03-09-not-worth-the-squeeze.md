---
layout: post
title: "Not Worth the Squeeze"
image: "/assets/not-worth-the-squeeze.jpg"
tags: vector-space
---

![Not Worth the Squeeze](/assets/not-worth-the-squeeze.jpg)

"What if a publisher games the coupons?"

Fair question. [Don Marti](https://blog.zgp.org/ad-supported-piracy/) raised the specific version: a fraudulent publisher uses surveillance data to identify a high-intent buyer, routes them through a junk site, stamps a coupon, and claims credit for a conversion that was going to happen anyway. The coupon is real but the attribution is stolen. This is the same attack [cookies already suffer from](/adtech-from-1887), except cookies are worse because anyone can overwrite the tracking parameter at any point, invisibly. Coupons at least make the issuance auditable.

A valid attack. The cryptographic coupon protocol is sound, but a side channel remains unmitigated. Web security solved this problem class twenty years ago.

## The Attack

This is already happening with cookies. Browser extensions like [Honey](/adtech-from-1887) silently overwrite affiliate cookies at checkout, stealing credit from the publisher who actually drove the sale. The coupon version would look like this:

1. A fraudulent publisher buys surveillance data to identify a user who just searched for "running shoes."
2. The user visits the publisher's junk site. The site loads an ad tag with a coupon from Nike's campaign.
3. The user later buys shoes on nike.com. The coupon gets redeemed.
4. The junk site claims credit for the conversion.

The coupon signature is valid and the cryptography held, but the fraud happened upstream. The junk site was never supposed to have that coupon book in the first place. "Better than cookies" is a low bar. We need actual defenses.

## Same Playbook

Web security never solved anything with one mechanism.

[HTTPS](https://developer.mozilla.org/en-US/docs/Glossary/HTTPS) didn't stop phishing. [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) didn't stop XSS. [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) didn't stop injection. Each layer raised the cost of attack. The stack of imperfect layers makes most attacks unprofitable, and that's the point.

Attribution security works the same way. Stack layers until fraud costs more than it pays.

## The Layers

### CSP → Issuance Policy

[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy) tells browsers which sources are authorized to load scripts and resources. Anything not on the allowlist gets blocked.

So issuance policy does the same for coupons. When an advertiser creates a campaign on the [croupier](/croupier), they declare which publishers are authorized to distribute their coupon books. The relay only releases books to publishers on the list. A junk site not on Nike's allowlist never receives the coupons. No coupons, no stamps, no claim. The attack dies at step 2.

**Blocks:** unauthorized distribution. A junk site can't claim coupons it never received.

### Token Binding → Device Binding

[Token Binding](https://www.rfc-editor.org/rfc/rfc8471) ties a security token to the TLS connection's private key. A stolen token is useless on a different connection.

But what if an authorized publisher's coupons get intercepted? Device binding ties the coupon to the device that saw the ad. The browser generates a keypair. The coupon is signed against the public key. At conversion, the device proves possession of the private key. A fraudster who intercepts coupon data can't replay it from a different device. The coupon is non-transferable.

**Blocks:** coupon theft. Stolen coupon data is worthless without the device's private key.

### Double-Spend Prevention → Single Attribution

Digital currencies solved the double-spend problem: one coin, one transaction. The first valid claim wins, and the network rejects duplicates.

Yet even on the right device, multiple publishers could present coupons for the same sale. Single attribution applies the double-spend rule to conversions: one conversion, one coupon wins. If multiple publishers present coupons for the same sale, engagement quality breaks the tie: time on site, scroll depth, interaction sequence. A redirect through a junk site produces a thin engagement signal. A podcast listener who clicks a show-notes link and browses for ten minutes produces a rich one. The [lemons become obvious](/receipts-please).

**Blocks:** credit splitting. One conversion, one winner, and the evidence decides who.

## The Stack

Each layer is individually imperfect. Together, they multiply the cost.

| Layer | What the fraudster must defeat |
|---|---|
| Issuance Policy | Get on the advertiser's allowlist |
| Device Binding | Compromise the user's device key |
| Single Attribution | Beat a legitimate publisher's engagement signal |

All three have [production precedent](https://developer.apple.com/documentation/AdAttributionKit) today. To run the original attack, a fraudster must defeat all three simultaneously. That means:

- Convince a real brand you're a legitimate publisher to get allowlisted
- Steal a cryptographic key from the user's device
- Generate engagement so convincing it beats the publisher who actually earned the click

For a coupon worth a few dollars. Or you could just run a [click farm](#click-farms) for pennies per tap. The sophisticated attack is more expensive than the dumb one, and the dumb one is already the cheapest fraud left standing. The attack has collapsed into honest behavior.

## Open Questions

Three more layers would strengthen the stack, but each has unsolved engineering problems.

**Content Binding** ([SRI](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) for coupons) would tie each coupon to the hash of the ad creative, so a publisher can't stamp a coupon without loading the real ad. But advertisers run hundreds of variants through dynamic creative optimization and A/B tests. How do you hash a creative that changes per impression?

**Attribution Logs** ([Certificate Transparency](https://certificate.transparency.dev/) for coupons) would log every batch to an append-only Merkle ledger, making off-book issuance detectable. But CT handles ~10 billion certificates total. Programmatic ad serving does hundreds of billions of impressions per day. And CT works because Chrome mandates it. Who mandates an ad issuance log when the incumbents benefit from opacity?

**Engagement Proofs** ([ZK proofs](https://en.wikipedia.org/wiki/Zero-knowledge_proof) for viewability) would let a browser prove the user actually saw and interacted with the ad without revealing who they are. But ZK proof generation on every impression costs battery and latency. And once you publish what counts as "engagement," that definition becomes the new attack surface.

**<a id="click-farms"></a>Click farms.** Real humans on real devices, tapping through ads for pennies. Every deployable layer checks out: the coupon was issued to an authorized publisher, the device key matches, and the engagement signal is real. The interaction happened. It just wasn't genuine interest. No cryptographic layer can catch this because the signals are real.

If you make it expensive enough for them to cheat, they won't. But "expensive enough" still has open engineering.

---

*Part of the [Vector Space](/vector-space) series.*
