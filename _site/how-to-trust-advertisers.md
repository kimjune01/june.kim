A scammer reads this series and sees opportunity. The auction is open. No gatekeeper approves advertisers. So they spin up an account, position themselves near "rash that won't go away," and sell snake oil to people who need a dermatologist.

The snake oil costs pennies. Lard and menthol, package design from Nano Banana Pro. The real dermatologist has malpractice insurance, a lease, staff, years of training. The scammer has more money left over for ads. In any auction, the scammer has a [built-in cost advantage](https://web.archive.org/web/20240228162943/https://blog.zgp.org/when-can-deceptive-sellers-outbid-honest-sellers-for-ad-impressions/). The [keyword tax](/keyword-tax) that legitimate specialists pay is the snake oil seller's profit margin.

![Trust signals](/assets/how_to_trust_advertisers.jpg)

This is the obvious objection to an open ad protocol. And it's the right objection.

## Open Systems Collapse

Rory Sutherland calls this the [doorman effect](https://www.mfpwealthmanagement.co.uk/blog/doorman-fallacy-rory-sutherland). An automatic door is more efficient than a doorman. But the doorman's real job was never opening the door. It was the miscellaneous, hard-to-measure work that makes a building run: helping guests, watching the street, handling problems before they escalate. The signal — that you're entering a place with standards — is downstream from the decision to hire someone for that work. Replace the doorman with an automatic door and you gain efficiency but lose everything the doorman actually did, and the signal disappears with it. Auction-based advertising did exactly this: it replaced editorial selection with an auction and gained efficiency but lost the built-in cost that made advertising harder for scammers than for legitimate businesses.

Open systems without trust mechanisms don't stay useful. Email was designed fully open. By the mid-2000s, [roughly 90% was spam](https://www.statista.com/statistics/420391/spam-email-traffic-share/). The Android Market launched with minimal review. By 2011, [malware-infected apps](https://arstechnica.com/information-technology/2011/03/google-remotely-wipes-malware-laden-apps-from-android-phones/) were being remotely wiped from users' phones. Akerlof won the Nobel Prize for describing this: when buyers can't observe quality, bad sellers drive out good ones, and [the market unravels](https://ideas.repec.org/a/oup/qjecon/v84y1970i3p488-500..html).

Pure openness fails. The scammers arrive faster than the legitimate participants, and the legitimate participants leave.

## Gatekeepers Get Captured

So you add a gatekeeper. Google reviews advertisers. The App Store reviews apps. Amazon reviews sellers.

[Lizzeri (1999)](https://www.jstor.org/stable/2556078) proved that a monopoly certification intermediary will strategically under-reveal quality information, because partial revelation maximizes the certifier's profit. The gatekeeper's incentive isn't to protect users. It's to extract rent from the gate.

Google demonstrates this. Scam ads for fake customer service numbers, counterfeit products, and phishing sites run constantly. Google [removed 5.5 billion ads](https://blog.google/technology/safety-security/how-we-fought-bad-ads-scams-and-misinformation-2023/) in 2023, which means 5.5 billion got far enough to need removal. Meanwhile, [more than 50%](https://web.archive.org/web/20250918041138/https://searchengineland.com/small-businesses-compete-google-ads-462009) of small businesses say they've been priced out of Google Ads entirely. The gatekeeper lets scammers through (they increase competition, which raises prices) and blocks legitimate businesses (opaque policy rejections with no recourse).

Don Marti [put it precisely](https://web.archive.org/web/20260101192249/https://blog.zgp.org/advertising-personalization-good-for-you/): the intermediaries with the most incentive to allow dishonest advertisers are the only ones in a position to filter them out. In the [DOJ's antitrust case](https://www.justice.gov/atr/case/us-and-plaintiff-states-v-google-llc-2023), Google's own A/B test data showed practices like "Last Look" and "Project Poirot" diverted hundreds of millions from competing exchanges. The gatekeeper extracted rent from legitimate participants. That's not a failure of execution. That's what monopoly gatekeeping produces.

## The Middle Ground Fails Too

Requiring credentials outsources gatekeeping to licensing boards, which are government-run monopolies that restrict supply and protect incumbents. A traditional healer with 30 years of community trust has no license. A self-taught financial advisor serving immigrants in their language has no CFP. And credentials don't catch the scam anyway: the snake oil seller isn't claiming to be a licensed dermatologist. They're selling a product. No license required.

Automated review is an arms race. Train a classifier on known scams, flag new ones. The scammer adjusts the landing page, resubmits. Ad fraud is an [$84 billion problem](https://www.juniper.net/research/press/ad-fraud-losses-will-exceed-172-billion-2028). And the platform trains the classifier, decides the threshold, and profits from borderline cases. The threshold drifts toward revenue.

Performance bonds sound promising, but [Ostrom's graduated sanctions](https://www.cambridge.org/core/books/governing-the-commons/7AB7AE11BADA84409C34815CC288CD79) (proportional consequences for violations) require observing the violation. The ad exchange is structurally blind to outcomes. It sees a bid, scores it, picks a winner. Did the product work? Was the user harmed? The exchange doesn't know. You can't forfeit a bond for fraud you can't see.

Embeddings don't help either. In keyword advertising, a scammer bids on "dermatologist" and competes head-on with actual dermatologists. In embedding space, the scammer positions near "rash that won't go away" (low-information, vulnerable) and avoids "contact dermatitis differential diagnosis" (expert, can evaluate). The geometric precision that makes embedding-space auctions [better for specialists](/relocation-fees) makes them better for scammers too.

Changing the underlying data structure from keywords to embeddings doesn't change the gatekeeping problem.

## The Protocol Doesn't Solve Fraud

HTTP doesn't prevent phishing. TCP doesn't prevent malware. SMTP didn't prevent spam. None of them solved fraud at the protocol layer. The solutions came from other layers: SPF/DKIM/DMARC, browser padlock icons, search engine reputation scoring. The protocol stayed open. Trust was layered on top, competitively, with no single authority.

The ad auction protocol should follow the same pattern. The [scoring function](/power-diagrams-ad-auctions) `log(bid) - distance² / σ²` runs inside a [TEE](/perplexity-was-right-to-kill-ads). It matches by meaning. It has no opinion about legitimacy. Fraud prevention happens at other layers. The [trust chain](/the-last-ad-layer) verifies that the auction ran honestly.

> The protocol is open, the auction is honest, and nobody reviews advertisers before they enter. How do you keep the snake oil seller from winning the auction?

## Piggybacking on Payments

The exchange can't observe outcomes. But payment networks can.

When the snake oil doesn't work, the buyer disputes the charge. Visa sees the chargeback. The merchant's chargeback rate goes up. The payment processor flags or drops them. The enforcement comes from the person who was actually harmed.

The mechanic: an advertiser connects their payment processor as part of onboarding (Plaid, Stripe, Square, Clover). Merchant account age, transaction volume, chargeback rate. These are graduated trust signals that no gatekeeper grants. They accumulate from real commerce. A business with three years of clean payment history and a 0.1% chargeback rate is almost certainly legitimate. Thousands of customers paid and didn't complain. That's a stronger signal than any approval process, and the hard work of verification already happened at the payment network. The ad exchange doesn't need to build a trust infrastructure from scratch. It piggybacks on one that Visa, Stripe, and Square have been refining for decades.

KYC through payment auth is friction. But it's more open than whatever Google's internal reviews are offering. The traditional healer with no PT license but 30 years of clean payment history has a stronger trust signal than any credential.

## The Composite Signal

Payment history is the strongest single signal, but a business operating in public leaves traces across many systems, each independently verifiable, none requiring a gatekeeper:

| Signal | What it proves | Examples |
|---|---|---|
| Payment processor | Revenue is real, chargebacks are low | Stripe, Square, Plaid |
| Reviews | Customers exist and are satisfied | Google Business Profile, Yelp, Trustpilot |
| E-commerce platform | Sales volume, seller ratings | Shopify, Amazon, Etsy |
| Web presence | Site has real traffic, has existed for years | WHOIS, Google Search Console |
| Booking platform | Appointments are real, clients book regularly | Zocdoc, Mindbody, Calendly |
| Accounting | Revenue, invoices, payment history | QuickBooks, Xero via [Codat](https://docs.codat.io/) |
| Business registration | Business exists, files taxes | [Middesk](https://docs.middesk.com/home), Dun & Bradstreet |

No single signal is conclusive. In aggregate, they're expensive to fake. A fake business with a three-year-old domain, clean Stripe history, 200 Google reviews, Shopify sales data, and a QuickBooks P&L? That's a real business. The cost of faking legitimacy at scale approaches the cost of actually being legitimate.

A new legitimate business isn't signal-zero. They still have a bank account, a payment processor that did its own KYC, and a business registration. The signal is weaker, not absent. Weaker signal means a lower trust tier: less prominent placement until the history builds. That's how email deliverability works for new domains. You don't get blocked. You start in the spam folder and earn your way to the inbox.

DNS itself is a trust signal. SPF works by publishing a TXT record declaring which servers can send email on behalf of a domain. The same pattern applies: an advertiser publishes a DNS TXT record declaring their embedding position and exchange affiliations. Anyone can look it up (`dig TXT example.com`) without asking a gatekeeper. It's decentralized, verifiable, and piggybacks on infrastructure that's been running since 1983.

One signal is unique to embedding-space auctions: semantic consistency between the advertiser's declared position and their public footprint. The exchange embeds the advertiser's website using the same model the auction already runs. A real climbing PT's site lands near "finger pulley rehab." A snake oil seller's thin landing page doesn't. Anyone can verify the match: embed the site, check the cosine similarity. The geometry creates a cost gradient that favors depth over deception.

## Zero Scams Is Not the Goal

Magazine advertising had two qualities that made it naturally fraud-resistant: targeting was general enough that any audience included norms enforcers alongside targets, and advertising was persistent enough that publishers who accepted dishonest ads suffered reputational consequences. Auction-based advertising stripped both qualities. The open protocol needs substitutes, and the layered trust signals above provide them. Payment history and review platforms are persistent reputational records. Platform competition means chatbots that surface scammy suggestions lose users.

Every system with gatekeepers still has scammers. Google Ads, the App Store, Amazon. All have review processes. All have fraud. The question isn't how to get to zero. It's whether layered trust signals achieve a comparable scam rate at lower gatekeeping cost.

- **Payment signals are harder to game than ad review.** A three-year clean chargeback history can't be fast-forwarded.
- **Competing exchanges create selection pressure.** An exchange with a high scam rate loses platform partners. The [NYSE vs. NASDAQ precedent](https://corpgov.law.harvard.edu/2018/12/28/stock-exchanges-and-shareholder-rights-a-race-to-the-top-not-the-bottom/) shows competing exchanges race to the top on governance, not the bottom.
- **Platform competition protects users.** The chatbot that surfaces scammy suggestions loses users to one that doesn't.
- **Transparency enables auditing.** In an open protocol with TEE-attested auctions, anyone can analyze advertiser behavior and flag patterns. In Google's closed system, scam patterns hide.

Customers are responsible for discrimination, not the middlemen. But the system's job is to give them the tools. The composite signal, the credential badges, the semantic consistency check: these help users evaluate what they're being shown. The protocol doesn't decide for them. It surfaces the evidence.

Enrons and Bankman-Frieds will have their moments. That's the cost of living in a free society with other humans. The open protocol accepts a nonzero scam rate and makes it tolerable through competing trust signals at every layer. That's the same tradeoff email made. Email still has spam. Email still works.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched prior art, drafted prose, and pushed back on its own proposals until they stopped being gatekeeping in disguise.*

*Part of the [Vector Space](/vector-space) series.*
