# Cookie Hijacking: What Advertisers and Publishers Should Know

*March 2026 | Croupier Blog*

<iframe width="560" height="315" src="https://www.youtube.com/embed/vc4yL3YTwWk" frameborder="0" allowfullscreen></iframe>

If you run affiliate marketing campaigns, your attribution data might be lying to you. Not because of measurement error — because someone is actively overwriting it.

## What Is Cookie Hijacking?

Cookie hijacking in advertising happens when a third party overwrites the affiliate tracking cookie right before a purchase. The publisher who drove the customer to your site gets nothing. The hijacker gets the commission.

This isn't theoretical. In December 2024, MegaLag exposed how PayPal's Honey browser extension was doing exactly this — injecting affiliate codes at checkout, redirecting commissions away from the creators and publishers who earned them. Linus Tech Tips ended their Honey sponsorship after discovering it across roughly 160 sponsored segments. A class-action lawsuit followed.

The mechanic is simple. Cookie-based attribution assigns credit to whoever set the cookie last. A browser extension that activates at checkout will always be last. The publisher who ran the ad, wrote the review, or produced the video gets erased from the attribution chain.

## Why This Keeps Happening

The problem is the cookie itself. It's a mutable value stored in the browser that any script with the right permissions can read or overwrite. Last-touch attribution means the final write wins.

This is a structural vulnerability, not a bug in any particular extension. As long as attribution depends on a value that third parties can overwrite, hijacking is a rational economic strategy for anyone positioned at the checkout.

Here's what makes it worse: the advertiser often can't tell. Their dashboard shows conversions attributed to an affiliate partner they never chose. The real partner's numbers drop, and neither side has proof of what happened.

## The Scale of the Problem

The Honey case got headlines, but cookie hijacking is widespread:

- **Browser extensions** with millions of installs can inject affiliate codes silently
- **Toolbar software** bundled with downloads has been doing this since the early 2010s
- **Malware and adware** swap tracking parameters across ad networks
- **Coupon sites** that auto-apply codes at checkout routinely overwrite affiliate cookies

The advertiser's conversion report looks fine. Conversions happened. Revenue came in. But the attribution is fiction. The wrong partners get paid, and the right ones leave.

## What Can Be Done

There are a few approaches advertisers and publishers use today:

**Server-side tracking** moves the attribution event off the browser. It's harder to hijack but still depends on the advertiser's tracking infrastructure reporting honestly.

**Sub-ID validation** adds extra identifiers to affiliate links. It catches some hijacking but creates an arms race with extensions that learn to replicate the parameters.

**Contractual restrictions** prohibit affiliates from using browser extensions. Enforcement is manual and slow.

None of these fix the root cause. The attribution signal is still a mutable value that the advertiser doesn't control.

## A Different Architecture

What if attribution didn't depend on cookies at all?

Cryptographic attribution replaces the cookie with a signed token — a coupon issued by the advertiser and carried by the customer's device. The advertiser signs a batch of tokens and hands them to the publisher. The publisher places one in each ad. At conversion, the customer's device presents the token and the advertiser verifies the signature.

No cookie to overwrite. The token is a cryptographic proof that can only be issued by the advertiser and can only be verified by the advertiser. An extension that injects its own code at checkout can't forge the advertiser's signature.

This is the approach behind [Croupier](https://github.com/kimjune01/croupier) — a blind relay that passes sealed coupon books between advertisers and publishers without reading them. The relay never sees the tokens. It just moves envelopes.

## What This Means for Your Campaigns

If you're an advertiser running affiliate or publisher campaigns:

1. **Audit your attribution chain.** Look for sudden drops in partner performance that coincide with coupon extension installs in your customer base.
2. **Compare channels.** If one "affiliate" consistently gets last-touch credit but drives no incremental traffic, investigate.
3. **Consider cryptographic alternatives.** The technology exists today. Privacy Pass (RFC 9578) standardized the token format. Blind signatures have been production-grade since 1983.

Cookie hijacking is a solvable problem. It just requires moving from a model where anyone can overwrite the receipt to one where only the advertiser can issue it.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
