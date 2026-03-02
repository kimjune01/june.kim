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

**Email** was a signal of personal attention. Someone sat down and wrote you a message. AI-generated cold outreach now produces personalized emails at zero marginal cost — your name, your company, a reference to your latest blog post, a plausible ask. Indistinguishable from a real email. Open rates collapse because the rational response to any message from a stranger is to assume it's automated.

**DMs** are following email. LinkedIn is already there. Twitter DMs are heading there. Every message from an unknown account is synthetic until proven otherwise.

**Keyword ad position** was a signal of budget, which was a weak proxy for legitimacy. A company that can afford $80/click on "plumber Bloomington" is probably a real business. But the signal is about *spending capacity*, not *relevance*. The [plumber with the biggest overhead](/the-plumber-test) wins, not the one who fixes your problem.

**Behavioral targeting** was a signal of *who you are*, assembled from surveillance. Don Marti [argued](https://blog.zgp.org/perfectly-targeted-advertising-would-be-perfectly-worthless/) that this signal is perfectly worthless — a retargeted ad tells you "this company knows you visited their website." That carries zero information about their quality, trustworthiness, or fit. And the surveillance infrastructure that produces it is increasingly restricted: Apple's ATT, cookie deprecation, GDPR enforcement.

The pattern is the same in every case. A signal emerges. It carries real information. The cost of faking it drops. Noise floods the channel. The signal becomes indistinguishable from the noise. The channel dies as an information source and survives only as a tax — something you endure, not something you trust.

## What Survives

Word of mouth. Doc Searls had sewage in his basement. He asked his neighbors. They sent him the guys with the truck. The match was perfect because the signal — a personal recommendation from someone with nothing to gain — is expensive to fake. You'd need to befriend Doc's neighbors and plant the recommendation. That doesn't scale.

Word of mouth is the only signal that has never been killed by cheap faking. It survives precisely because it's expensive: real relationships, real experience, real reputation built over time. You can't automate it without destroying it.

But it doesn't scale. It works for Doc in Bloomington because he has neighbors who know a plumber. It doesn't work for the person who just moved there.

## The Cost of Faking

Every dead signal shares one property: the cost of producing a fake is lower than the cost of producing the real thing.

| Signal | Real cost | Fake cost | Status |
|---|---|---|---|
| Backlink from MIT | Years of credible research | $5 on Fiverr | Dead |
| Amazon review | Buy product, use it, write honestly | $0.50 per review from a farm | Dead |
| Personal email | Think about recipient, write specifically | GPT + scraper, zero marginal cost | Dying |
| LinkedIn DM | Genuine professional interest | Automated sequence, pennies | Dead |
| Keyword ad position | Budget to outbid competitors | Budget to outbid competitors | Signal of spending, not quality |
| Behavioral targeting | Surveillance infrastructure | N/A — the signal itself is worthless | Restricted |

The only surviving signal — word of mouth — has a fake cost that's prohibitively high: infiltrate someone's social network and plant a credible recommendation. That's why it survives. Not because it's better. Because it's expensive to counterfeit.

## Position as Signal

An advertiser's position in embedding space is a new kind of signal. Not "this company paid the most" (keyword bid). Not "this company knows who you are" (behavioral targeting). Not "other people liked this" (reviews). Instead: *this company declared that it does this specific thing, and has held that position at a cost.*

The [relocation fee](/relocation-fees) is what makes it a signal. Without fees, position is free to declare and free to change — you'd get the same gaming that killed every other signal. Every advertiser would cluster at the densest traffic point, position would carry no information, and the embedding space would reproduce keyword crowding at higher resolution. That's [Hotelling drift](/synthetic-friction), and the simulation proves it happens in every cluster tested.

With fees, position becomes a credible commitment. The climbing PT who positions at "rock climbing finger pulley rehabilitation" is saying: I do this specific thing, and I've put capital behind that claim. Moving to the generic "physical therapy" position would cost her the relocation fee, the accumulated [tenure discount](/stay-or-pay), and the bond she posted on entry. The cost of faking — declaring a position you don't actually occupy — scales with the distance between where you claim to be and where you belong.

| Signal | Real cost | Fake cost | Mechanism |
|---|---|---|---|
| Embedding position | Describe what you actually do | Relocation fee + tenure loss + bond | Position is expensive to fake by construction |

The entry bond prices the option to create a fake identity. The tenure discount creates an asset that's destroyed by repositioning. The relocation fee makes every unit of drift cost money. The [identity binding](/stay-or-pay) prevents resetting the cost by creating a new account. Stack these and the cost of faking a position is designed to exceed the benefit — not because of moderation, not because of detection, but because the economic mechanism makes noise expensive.

This is the structural difference. Every dead signal relied on external enforcement — platform moderation, review detection algorithms, spam filters — to keep the cost of faking high. The enforcement always loses because the fakers iterate faster than the filters. Embedding position doesn't rely on detection. The cost is built into the mechanism. You don't need to catch the faker. You need the fee to exceed the benefit of faking. If it does, the rational move is to position honestly.

## Not a Filter. A Price.

Spam filters try to detect fake emails after they're sent. Review algorithms try to detect fake reviews after they're posted. SEO penalties try to detect content farms after they rank. Detection is a losing game because the arms race favors the attacker — the cost of circumventing detection is always falling.

The relocation fee isn't a filter. It's a price. You don't detect drift and punish it. You charge for it. The advertiser who wants to move from "climbing PT" to "general physical therapy" can do it — it costs λ · d². The advertiser who wants to position at the densest traffic point despite selling something niche can do it — it costs λ · d² every time the position doesn't match their actual business.

Prices work where filters fail because prices don't need to distinguish real from fake. They make both pay. The honest advertiser pays a small fee for a small adjustment. The gaming advertiser pays a large fee for a large misrepresentation. The mechanism is indifferent to intent. It charges by distance.

This is a Pigouvian tax on noise. Carbon taxes don't detect which emissions are "real" and which are "wasteful." They charge for all of them and let the cost sort it out. The relocation fee charges for all position changes and lets the economics sort it out. Honest positioning is cheap. Dishonest positioning is expensive. No classifier needed.

## The Quiet Ad

Every signal death made the internet louder. SEO slop fills search results. Fake reviews crowd out real ones. AI cold emails flood inboxes. Engagement bots inflate metrics. The noise is the product of zero-cost faking.

An embedding-space ad is quiet. It doesn't appear unless you're nearby. It doesn't appear at all unless [you ask](/ask-first). The advertiser can't shout louder by spending more — the scoring function is `log(bid) - distance²/σ²`, and the log compresses bid differences while distance dominates. A 10x bid overcomes very little distance. The loudest voice doesn't win. The closest expertise does.

The [model can't see the ads](/model-blindness). The conversation isn't steered. The indicator brightens as you approach a region of expertise, and dims as you leave. No interruption, no injection, no disguise.

This is what a signal looks like when it's designed from scratch in an environment where every previous signal has been killed by noise. Not louder. Not more targeted. Not more personalized. Just: positioned honestly, held at a cost, verified by hardware, and silent until asked.

The internet's signals are dead because faking them became free. The last signal is the one where faking is expensive by construction.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
