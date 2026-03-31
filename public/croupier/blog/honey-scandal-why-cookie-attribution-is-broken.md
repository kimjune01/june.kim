# The Honey Scandal Proves Cookie Attribution Is Broken

*March 2026 | Croupier Blog*

<iframe width="560" height="315" src="https://www.youtube.com/embed/vc4yL3YTwWk" frameborder="0" allowfullscreen></iframe>

In December 2024, MegaLag published a 23-minute investigation that blew up the affiliate marketing industry. PayPal's Honey browser extension — promoted by MrBeast, MKBHD, Linus Tech Tips, and thousands of other creators — was silently replacing affiliate tracking cookies at checkout. The creator who drove the sale got nothing. Honey took the commission.

This wasn't a bug. It was the business model.

## What Honey Did

When a customer clicks an affiliate link from a creator's video and lands on a merchant site, the merchant drops a tracking cookie that credits the creator. If the customer eventually buys, the creator earns a commission.

Honey's browser extension activated at checkout. When users clicked "Apply Coupon," Honey deleted the creator's tracking cookie and injected its own — even when no coupon was actually applied. The last cookie wins. Honey was always last.

In one documented test, Honey diverted a $35 NordVPN commission while giving the user 89 cents worth of "Honey Gold" rewards points. The creator got zero.

Honey had sponsored roughly 5,000 videos across 1,000 YouTube channels, accumulating 7.8 billion views. The creators promoting Honey were funding the tool that was stealing from them.

## The Lawsuits Piled Up

<iframe width="560" height="315" src="https://www.youtube.com/embed/4H4sScCB1cY" frameborder="0" allowfullscreen></iframe>

On December 29, 2024, LegalEagle (Devin Stone) filed a class-action lawsuit against PayPal, with Sam Denby of Wendover Productions and Ali Spagnola as principal plaintiffs. Stone estimated Honey may have stolen billions from creators over the five years since PayPal acquired it.

Days later, GamersNexus filed a separate class action:

<iframe width="560" height="315" src="https://www.youtube.com/embed/IKbFBgNuEOU" frameborder="0" allowfullscreen></iframe>

25 lawsuits were consolidated in California federal court. The first amended complaint was dismissed without prejudice in November 2025 — the court said plaintiffs hadn't proven their entitlement to the commissions. In January 2026, they came back with a 101-page second amended complaint, including actual merchant contracts with Bergdorf Goodman documenting exact commission percentages and qualifying link definitions.

The case is still active. No settlement.

## It Wasn't Just Honey

The scandal exposed a pattern. Capital One Shopping was hit with the same allegations in January 2025. A class action was filed on behalf of TechSource (3.87M subscribers) and ToastyBros (750K+ subscribers), alleging identical cookie-replacement commission theft. Capital One settled for $4 million in December 2025.

Then Rakuten. Four separate complaints were filed in February 2025, alleging Rakuten's own browser extension used hidden browser tabs to spoof affiliate links. The company that policed affiliates was running the same play.

By January 2026, Rakuten had removed Honey from its affiliate network, cutting Honey off from approximately 2,000 retail partners including Walmart, Sephora, Dyson, and Lego. Impact.com suspended Honey as well.

## The Real Problem

Every one of these cases exploits the same vulnerability: last-click cookie attribution. Whoever writes the cookie last gets paid. A browser extension that activates at checkout will always be last.

This isn't a flaw in Honey's code. It's a flaw in the attribution model. Any software with browser permissions can do the same thing. The cookie is a mutable value in a shared space. It was never designed to be tamper-proof.

MegaLag's Part 3 investigation, released December 2025, alleged Honey even incorporated code to evade detection by affiliate network compliance testers — a "selective standdown" system that adjusted behavior based on user profiling:

<iframe width="560" height="315" src="https://www.youtube.com/embed/qCGT_CKGgFE" frameborder="0" allowfullscreen></iframe>

## What Would Fix It

The cookie needs to be replaced with something that can't be overwritten by a third party.

Cryptographic attribution does this by replacing the cookie with a signed token. The advertiser issues a batch of tokens, the publisher distributes them, and the customer's device carries the token to the conversion event. The advertiser verifies their own signature. No cookie jar. No last-click race. No browser extension can forge the advertiser's signature.

This is the approach Coca-Cola used in 1887 with paper coupons. The digital version uses blind signatures — cryptographic primitives that have been production-grade since David Chaum's 1983 paper. The IETF standardized the token format in RFC 9578 (Privacy Pass).

The Honey scandal isn't an anomaly. It's the logical endpoint of cookie-based attribution. The fix isn't better policing of browser extensions. It's an attribution model where overwriting isn't possible.

[Croupier](https://github.com/kimjune01/croupier) is the blind relay that moves these sealed coupon books between advertisers and publishers. It never sees the tokens. It just passes envelopes.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
