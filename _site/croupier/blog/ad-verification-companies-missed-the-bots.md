# The Ad Verification Industry Missed the Bots

*March 2026 | Croupier Blog*

<iframe width="560" height="315" src="https://www.youtube.com/embed/oVfHeWTKjag" frameborder="0" allowfullscreen></iframe>

In March 2025, Adalytics published a 240-page report — covered by The Wall Street Journal — showing that the three largest ad verification companies consistently failed to block ads from being served to known bots.

DoubleVerify missed 21% of bot visits in their sample data. IAS's publisher optimization tool labeled confirmed bot traffic as valid human visitors 77% of the time across a dataset spanning 2019-2024. The bots weren't sophisticated. They were "declared bots" — operating from known data center IP addresses. The easiest category to detect.

The companies advertisers pay to protect them from fraud were marking bot traffic as human.

## The Fallout

DoubleVerify's stock fell 36% in a single day after poor earnings and the Adalytics report. Across three disclosure events between February 2024 and February 2025, DV stock dropped more than 70%, from $39.24 to $13.90.

Multiple securities fraud class actions followed. Pomerantz, Glancy Prongay & Murray, Kirby McInerney, and Frank R. Cruz all filed on behalf of investors. The lawsuits allege DoubleVerify misrepresented its technology capabilities and systematically overbilled customers for impressions served to declared bots.

DoubleVerify's response was to sue Adalytics for defamation. Adalytics filed a motion to dismiss in October 2025.

Meanwhile, the DOJ and NCIS have been interviewing ad industry executives about the effectiveness of verification tools. The inquiry started after an August 2024 Adalytics report found U.S. Navy and National Guard recruitment ads running on sanctioned Russian and Iranian websites. Federal agencies spent more than $1.8 billion on advertising in 2023.

Senators Blackburn and Blumenthal wrote to DV and IAS expressing "serious concerns" after Adalytics found ads for Mars, PepsiCo, Domino's, Amazon, and the Department of Homeland Security running next to explicit content, including child sexual abuse material on image-sharing websites.

## The Scale of Bot Traffic

The 2025 Imperva Bad Bot Report found that automated bot traffic surpassed human traffic for the first time in a decade, constituting 51% of all web traffic. Bad bots alone account for 37% of all internet traffic — up for the sixth consecutive year.

Fraudlogix analyzed 105.7 billion impressions throughout 2025 and found a global invalid traffic rate of 20.64%. Roughly one in five ad impressions showed characteristics of fraudulent or non-human activity. Desktop invalid traffic was even higher at 27%.

The botnets are massive. In March 2025, HUMAN Security exposed BADBOX 2.0 — more than one million infected CTV devices across 222 countries. Google filed a lawsuit against the operators in July 2025. The FBI issued a public service announcement warning consumers.

The Vo1d botnet infected 1.59 million Android TV devices across 226 countries, performing ad fraud by simulating clicks and video views.

IAS's own Threat Lab discovered Genisys in September 2025 — 25 million compromised Android devices generating fake traffic through 115 malicious apps on Google Play and roughly 500 AI-generated publisher websites.

## The Verification Paradox

Ad verification is supposed to work like this: the advertiser pays a verification company to monitor where their ads run and block fraudulent impressions. The verification company checks each impression against known threats and reports the results.

The problem is structural. Verification companies are paid by advertisers to evaluate inventory sold by exchanges. But the same exchanges are also clients. DoubleVerify and IAS provide services to both sides of the transaction. When they flag too much inventory as fraudulent, they threaten the revenue of the exchanges they also serve.

Adalytics called this out directly: the companies that should be catching fraud have financial relationships with the entities perpetrating it.

And even when verification works perfectly, it only filters on the input side. It answers "was this impression fraudulent?" not "did this impression lead to a conversion?" An impression that passes every verification check — real human, real device, brand-safe context — can still deliver zero value if the human never noticed the ad.

## Verification vs. Attribution

Verification tries to prevent bad impressions. Attribution measures what actually happened after the impression.

These are different questions with different architectures:

| | Verification | Attribution |
|---|---|---|
| Question | Was this impression real? | Did this impression convert? |
| Who controls it | Third-party vendor | Advertiser |
| What it catches | Bots, brand-unsafe content | Low-performing channels |
| What it misses | Non-converting real impressions | Nothing — it measures outcomes |

An advertiser using cryptographic attribution doesn't need to guess which impressions were real. They count redemptions. Publisher A: 80 coupons redeemed out of 1,000 issued. Publisher B: 0 out of 1,000. The bot farm redeemed nothing because bots don't convert. The measurement inherently excludes fraud without needing a verification layer.

This isn't a replacement for verification on brand safety — you still don't want your ad next to harmful content. But for performance measurement, counting what actually converts is more reliable than trying to filter what's fake.

## What To Do

1. **Don't rely solely on verification.** The Adalytics report shows these tools miss significant fraud. Use verification for brand safety, not as your only quality signal.
2. **Measure outcomes, not impressions.** Shift your measurement framework from "was this impression valid?" to "did this channel produce conversions I can verify?"
3. **Run conversion-based attribution in parallel.** Issue cryptographic coupons alongside your existing campaigns. If Publisher A redeems at 8% and Publisher B at 0%, you know more than any verification report can tell you.

The verification industry spent a decade promising to clean up ad fraud. Bot traffic grew every year. Maybe the approach is wrong. Instead of trying to authenticate every impression upstream, let the advertiser count what came back downstream.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
