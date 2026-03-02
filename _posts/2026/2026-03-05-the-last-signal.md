---
layout: post
title: "The Last Signal"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

Every signal on the internet is dying the same death. The cost of faking it dropped below the cost of producing the real thing. Once that happens, the signal is worthless — not because it was bad, but because you can't tell the real from the fake. The market for quality collapses. Akerlof called this the lemons problem in 1970. It's now the operating condition of every channel on the internet.

## The Kill List

**PageRank** was a signal of peer endorsement. A link from MIT to your research page meant something — a human at a credible institution decided your work was worth citing. SEO farms industrialized link production. By 2025, the first page of Google for most commercial queries is content written to rank, not content written to inform. The signal died when the cost of producing a backlink dropped below the cost of earning one.

**Reviews** were a signal of customer experience. A five-star review on Amazon meant someone bought the product and liked it. Fake review farms [produce thousands per day](https://www.ftc.gov/news-events/news/press-releases/2023/06/ftc-proposes-new-rule-combat-fake-reviews-testimonials) at pennies each. The FTC fined companies for it. The reviews kept coming. Amazon deletes millions annually and the problem grows faster than the enforcement. You can't trust a stranger's review because you can't tell if the stranger exists.

**Organic social** was a signal of genuine interest. A share or a like meant a person chose to amplify your content. Engagement bots, follow-for-follow networks, and algorithmic feeds turned the channel into pay-to-play. The signal died when platforms optimized for engagement over authenticity — and then AI-generated content made the floor of production quality indistinguishable from the ceiling.

**Phone calls** were a signal of urgency. Someone picked up a device and demanded your real-time attention. Americans got [55 billion robocalls in 2023](https://www.robokiller.com/robocall-insights). The rational response to an unknown number is to not answer. An entire communication channel — real-time voice between humans — is dead for strangers.

**Direct messages** were a signal of personal attention. Someone sat down and wrote you a message. AI-generated cold outreach now produces personalized emails and DMs at zero marginal cost — your name, your company, a reference to your latest blog post, a plausible ask. Indistinguishable from a real message. The rational response to anything from a stranger is to assume it's automated. LinkedIn is already there. Email is close. Twitter DMs are next.

**Keyword ad position** was a signal of budget — a weak proxy for legitimacy. The [plumber with the biggest overhead](/the-plumber-test) wins, not the one who fixes your problem.

**Behavioral targeting** was a signal of *who you are*, assembled from surveillance. Don Marti [argued](https://blog.zgp.org/perfectly-targeted-advertising-would-be-perfectly-worthless/) that this signal is perfectly worthless — a retargeted ad tells you "this company knows you visited their website." That carries zero information about their quality, trustworthiness, or fit. And the surveillance infrastructure that produces it is increasingly restricted: Apple's ATT, cookie deprecation, GDPR enforcement.

Same pattern every time. A signal carries real information. The cost of faking it drops below the cost of producing the real thing. The channel floods with noise and dies.

## What Survives

Word of mouth. Doc Searls had [sewage in his basement](/the-plumber-test). He asked his neighbors. They sent him the guys with the truck. The match was perfect because faking it would require infiltrating his social network and planting a recommendation. That doesn't scale — but it's the only signal that has never been killed, because it's the only one that's expensive to counterfeit.

| Signal | Real cost | Fake cost | Status |
|---|---|---|---|
| Backlink from MIT | Years of credible research | $5 on Fiverr | Dead |
| Amazon review | Buy product, use it, write honestly | $0.50 per review from a farm | Dead |
| Personal message | Think about recipient, write specifically | GPT + scraper, zero marginal cost | Dying |
| Keyword ad position | Budget to outbid competitors | Budget to outbid competitors | Signal of spending, not quality |
| Word of mouth | Real relationship, real experience | Infiltrate a social network | Alive, doesn't scale |

## Position as Signal

An advertiser's position in embedding space is a different kind of signal: *this company declared that it does this specific thing, and has held that position at a cost.*

Without [relocation fees](/relocation-fees), position is free to declare and free to change — every advertiser clusters at the densest traffic point, and the signal carries no information. That's [Hotelling drift](/synthetic-friction).

With fees, position becomes a credible commitment. The climbing PT at "rock climbing finger pulley rehabilitation" has put capital behind that claim. Moving to generic "physical therapy" would cost her the relocation fee, the accumulated [tenure discount](/stay-or-pay), and the bond she posted on entry. The cost of faking scales with the distance between where you claim to be and where you belong.

Every dead signal relied on external enforcement — moderation, detection algorithms, spam filters — to keep faking expensive. The enforcement always loses because fakers iterate faster than filters. Embedding position doesn't rely on detection. The [entry bond](/stay-or-pay) prices the option to create a fake identity. The tenure discount creates an asset destroyed by repositioning. The relocation fee charges for every unit of drift. The cost is the mechanism.

## Not a Filter. A Price.

The relocation fee isn't a filter. It's a price. You don't detect drift and punish it. You charge for it — λ · d² for every move. Prices don't need to distinguish real from fake. They make both pay. The honest advertiser pays a small fee for a small adjustment. The gaming advertiser pays a large fee for a large misrepresentation. The mechanism is indifferent to intent. It charges by distance.

Carbon taxes don't detect which emissions are wasteful. They charge for all of them. Honest positioning is cheap. Dishonest positioning is expensive. No classifier needed.

## The Quiet Ad

Every signal death made the internet louder. SEO slop fills search results. Fake reviews crowd out real ones. AI cold emails flood inboxes. Engagement bots inflate metrics. The noise is the product of zero-cost faking.

An embedding-space ad is quiet. It doesn't appear unless you're nearby. It doesn't appear at all unless [you ask](/ask-first). The scoring function is `log(bid) - distance²/σ²` — the log compresses bid differences while distance dominates. A 10x bid overcomes very little distance. The closest expertise wins, not the loudest voice.

The [model can't see the ads](/model-blindness). The conversation isn't steered. The indicator brightens as you approach a region of expertise, and dims as you leave.

Positioned honestly, held at a cost, verified by hardware, silent until asked. The last signal is the one where faking is expensive by construction.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
