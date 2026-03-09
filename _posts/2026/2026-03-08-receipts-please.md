---
layout: post
title: "Receipts, Please"
tags: vector-space
---

![Receipts, Please](/assets/receipts-please.jpg)

Investigative reporters are the reason we know how bad it is. An [Adalytics audit](https://web.archive.org/web/20251217201720/https://adalytics.io/blog/invalid-google-video-partner-trueview-ads) found that 80% of Google's TrueView video ad placements violated its own standards. The [ANA's programmatic transparency study](https://www.ana.net/content/show/id/pr-2023-06-programmaticstudy) found that only 36 cents of every programmatic dollar entering a DSP reached end consumers. Without these audits, advertisers would still be looking at their ROAS dashboards and assuming everything was fine.

[One in five ad impressions](https://www.ana.net/content/show/id/pr-2023-06-programmaticstudy) went to made-for-advertising (MFA) sites. These are not real publications. They are junk websites stuffed with ads, built to collect ad money and nothing else. Think "Top 10 Kitchen Gadgets You Need" pages with no author and no audience. They exist because Google's exchange treats them the same as real publishers.

These are not enterprise brands with in-house media buyers. For most small businesses, leadgen from search is the lifeline. Even if they discovered that half their budget went to AI slop farms, they could not do anything about it. Google is the only option.

## The Lemons Won

Digital advertising looks like a high-margin business. Google Services operates at [35-40% margins](https://web.archive.org/web/20260210013357/https://companiesmarketcap.com/alphabet-google/operating-margin/). In the DOJ antitrust trial, Google's own executives [acknowledged](https://digiday.com/media/the-rundown-u-s-v-google-ad-tech-antitrust-trial-by-numbers-so-far/) that their AdX take rate extracted "irrationally high rents." A judge ruled it an illegal monopoly.

Those margins exist because lemons took over. George Akerlof's [market for lemons](https://en.wikipedia.org/wiki/The_Market_for_Lemons): when buyers cannot tell good from bad, quality sellers exit and the market fills with junk.

The ad exchange is a market for lemons. The bid request contains `site.domain` — Google knows whether an impression is on the New York Times or an AI-generated listicle farm. The advertiser does not. MFA garbage competes in the same auctions as real inventory. Keyword auctions need liquidity. Binning by quality would split the pool, thin the bidding, and destroy the rents. So Google pools them and takes [20% of every transaction](https://web.archive.org/web/20260211063736/https://www.bigtechontrial.com/p/google-knows-its-ad-exchange-isnt). The ANA found that [45% of marketers paid higher CPMs for MFA than for premium sites](https://www.ana.net/content/show/id/pr-2023-06-programmaticstudy). A typical campaign ran across [44,000 websites](https://www.ana.net/content/show/id/pr-2023-06-programmaticstudy) with no quality control. The margin is the fraud. In 2008, banks bundled subprime mortgages with prime ones into CDOs, slapped on a AAA rating, and sold the bundle as premium. The buyer could not see which loans were junk. The rating agency was paid by the issuer. [Performance Max](https://ads.google.com/intl/en_us/home/campaigns/performance-max/) is a CDO. MFA impressions are the subprime. ROAS is the AAA rating. Google is the bundler and the rating agency.

## Jenga

Google's US ad market share has [declined from 31.6% to 26.8%](https://www.emarketer.com/chart/251603/us-net-digital-ad-revenue-share-by-company-2019-2023-of-total-digital-ad-spending) since 2019. Revenue keeps climbing. [Don Marti](https://web.archive.org/web/20240913032955/https://blog.zgp.org/ad-supported-piracy/) identified what fills the gap: commoditize inventory so junk is interchangeable with real, then inflate volume. Piracy sites, AI-generated slop, made-for-advertising pages. Package them into a black box. Call it Performance Max.

![Jenga ROAS](/assets/jenga-roas.jpg)

The racket is a ratchet. Once junk is in the revenue baseline, removing it means missing the quarter. Each quarter's inflation becomes the floor for the next. As of 2025, [74% of newly published web pages](https://ahrefs.com/blog/ai-content-study/) contain AI-generated content and [bot traffic exceeds human traffic](https://web.archive.org/web/20260228222455/https://www.imperva.com/resources/resource-library/reports/2025-bad-bot-report/). The "[dead internet](/the-last-signal)" is the supply side scaling to meet demand for cheap impressions. Hershey's recently [replaced the chocolate](https://www.npr.org/sections/planet-money/2026/03/03/g-s1-111940/the-candy-heir-vs-chocolate-skimpflation) in Reese's cups with "chocolate candy." Same wrapper, cheaper filling. Carl Shapiro called this [quality shading](https://academic.oup.com/qje/article-abstract/98/4/659/1913487) in 1983. At least the FDA requires an ingredient list on the wrapper. Google does it with impressions. There is no ingredient list.

## The Fields Already Exist

The data to measure inventory quality is already in every bid request. [OpenRTB](https://www.iab.com/guidelines/openrtb/) defines the schema for programmatic advertising, and most of the relevant fields are contextual. They are supposed to describe the environment of each impression.

| [Fields](https://www.iab.com/guidelines/openrtb/) | What they tell you |
|---|---|
| `device.make`, `device.os`, `device.connectiontype` | iPhone on WiFi or emulated Android on a data center IP |
| `site.domain`, `app.bundle` | Who showed the ad |
| `site.cat`, `imp.bidfloor` | Content category and the publisher's own price signal |

Google uses these fields internally. Its [Smart Bidding system](https://support.google.com/google-ads/answer/7065882) optimizes on contextual signals that advertisers cannot see or adjust. But advertisers running Performance Max get only [impression counts per placement](https://www.searchenginejournal.com/google-ads-surfaces-pmax-search-partner-domains-in-placement-report/567922/), with no clicks, cost, or conversions attached. Google calls this a "brand safety tool, not a performance report." In 2022, Google [removed App campaign placement data](https://ads-developers.googleblog.com/2022/02/important-changes-to-placement.html) from API reports entirely.

No privacy law restricts these fields. They describe the ad slot, not the person. Google says it hides placement data to protect user privacy. Hiding which *website* showed an ad protects no *user*. It cloaks Google from exposure. So what has the rest of adtech built instead?

## The Wrong Fix

The industry's sidestep is brand safety. Vendors scan pages for drugs, violence, pornography. A piracy site passes. An MFA page with AI listicles passes. Brand safety asks "is this offensive?" not "is this worth anything?"

The other attempt is a quality score. Rate every publisher, certify the good ones, block the bad ones. But a niche app with 50,000 loyal users converts at 8% for a SaaS advertiser and 0.02% for a mobile game. Quality depends on who is buying. It cannot be scored in advance.

Both fixes try to define quality before the impression runs. Neither lets the advertiser measure it after. And neither threatens the liquidity pool for keywords. The auctions stay bundled, and Google keeps its 20%.

What if the advertiser could hold a signed receipt for every impression and match it against their own conversion data? What if they could see which publishers actually convert and which ones never did? That is [attested attribution](/attested-attribution). Coca-Cola [solved this in 1887](/adtech-from-1887).

---

*Part of the [Vector Space](/vector-space) series.*
