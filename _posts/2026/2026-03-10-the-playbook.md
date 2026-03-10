---
layout: post
title: "The Playbook"
tags: vector-space
---

[The Easiest Sale](/the-easiest-sale) was the pitch. This is the playbook.

An ad exchange is a two-sided marketplace. The conventional wisdom says you need both sides before either side shows up. The conventional wisdom is wrong. You need a sequence.

## Step 1: Pay Publishers to Join

Publishers have the users. Without queries flowing through the exchange, there's nothing to sell. So publishers come first, and they get paid to show up.

Here's the offer:

1. **Open-source controllers.** The [tau-controller](https://github.com/kimjune01/tau-controller) sets the [recommendation frequency dial](/three-levers). The [sigma-controller](https://github.com/kimjune01/sigma-controller) tunes match precision. Both are open source. The publisher can read every line, fork it, modify it.

2. **Integration via skills, not SDKs.** The exchange ships [skills](/skills-over-sdks). The publisher's coding agent reads the [skill](https://github.com/kimjune01/vectorspace-skills), asks clarifying questions, and writes the integration into their codebase.

3. **Money up front.** A subsidy covers the integration cost plus months of inference. At [Gemini Flash 3 pricing](https://ai.google.dev/gemini-api/docs/pricing), $10k covers roughly 770,000 full conversations. For a mid-size vertical chatbot, that's five months of total inference. The publisher is cash-positive from day one. They're being paid to try.

4. **Privacy by construction.** The conversation never leaves the publisher's server. Intent extraction and embedding happen locally. Only a vector crosses the API boundary, encrypted in transit, processed inside a TEE, unextractable by design. There's nothing to leak because the exchange [never sees the data](/ask-first).

5. **Full UX control.** The publisher sets [tau](/three-levers), the dial that controls recommendation frequency. They choose the indicator style. They review every PR the skill generates. Their chatbot, their rules.

The downside is zero. They get paid, they keep control, and if it doesn't work, one command removes everything. Who's crazy enough to turn down free money?

## Step 2: Give Advertisers Free Traffic

Advertisers don't sign up. They get signed up. The qualification is simple: they're already spending money on Google Ads for related keywords. Search "addiction treatment" or "physical therapy near me" and the advertisers are right there in the sponsored results. The [Ads Transparency Center](https://adstransparency.google.com/) confirms who's running what. If they're buying these keywords, they've already proven willingness to pay for leads. For addiction treatment specifically, Google requires [LegitScript certification](https://www.legitscript.com/) to run ads. The qualification filters for legitimacy, not just spend. Lead gen is a search away.

1. **Scrape and embed.** Scrape the advertiser's homepage, about page, and service descriptions. Embed the marketing copy. The center lands wherever their language puts it in the vector space. Sigma is estimated from how narrow or broad their positioning is. A climbing PT's site talks about one thing. A general practice talks about everything.

2. **Resolve positions.** If the advertiser has a `market-position.json`, use it. If not, the scraped position works on its own.

3. **Email them.** Before any traffic flows, send the advertiser an email: here's your position in the vector space, here's how the exchange works, here's what's about to happen. They can ignore it, reply, or adjust their position. The email establishes the relationship. Everything after it is a reply in the same thread.

4. **Send real traffic.** The traffic is real. The publisher signs [serve receipts](/attested-attribution). The advertiser can verify every impression with cryptographic proof.

5. **Reply with the report.** Same thread, one reply: an attested attribution report and a suggested price. The suggested price is 10% of what they're already paying Google for equivalent traffic. Treatment providers paying [$75 per click](https://sagapixel.com/ppc/ppc-for-addiction-services-a-google-ads-guide/) on "addiction treatment" keywords see ~$7.50. Once there's enough volume, [VCG auctions](/one-shot-bidding) set the real price through competition. The fixed rate is scaffolding.

6. **Cut traffic immediately.** The report goes out, the traffic stops. Ball's in their court. If they pay, traffic resumes. If they don't, nothing changes for them. They got free leads and a clean exit.

Nobody else is bidding. Chatbot conversations have [zero recommendation infrastructure](/ask-first) today. These slots are uncontested.

The wedge is health and health-adjacent chatbots, where the user's intent is deeply commercial and the conversation gets thrown out after the session anyway. Monetize what you were already discarding. Get one publisher live, and the attribution reports sell the next.

## Step 3: The Report Is the Pitch

The attested attribution report *is* the sales deck. No slides, no demo, no call.

It says: your recommendation was served 847 times this week. Signed receipts prove each impression was real. The [audit trail](/croupier) shows the auction was honest. Cryptographic proof confirms nobody saw the user's conversation. The last page says: here's what it would cost to keep going.

Every ad exchange in history asks the advertiser to believe the numbers. This one hands them the receipts and says: check.

If the plumber from the [attribution post](/attested-attribution) got this report, he wouldn't need to ask Google "which clicks were real?" He'd already know.

## What the Advertiser Controls

The default works without any action from the advertiser. Their scraped marketing copy is the position. The exchange estimates sigma. The auction runs.

But if they want to refine:

- **`market-position.json`.** Override the scraped default with an explicit center and sigma. Declare exactly what you sell and how broadly you want to match.
- **Sigma adjustment.** Narrow sigma to match only highly specific queries. Widen it to match more broadly. The [sigma-controller](https://github.com/kimjune01/sigma-controller) can automate this.
- **Service area.** Declare a geographic service area. The publisher caches this from a public database and filters locally before the vector leaves their server. The exchange never sees the user's location.
- **Budget caps.** Set a daily or weekly spend limit. The exchange respects it.

No dashboard. No 47-tab console. The JSON is the configuration. The attribution report is the analytics. The exchange sends two things: a report and a suggested price.

## The Whole Stack Is Open

The protocol is [published](/power-diagrams-ad-auctions). The simulation is [open-source](https://github.com/kimjune01/openauction). So are the controllers, the skills, and this playbook.

Every publisher-first ad tech playbook worked. Here's what they all share.

|  | Publisher first | Subsidy | Reports convert demand | Wedge |
|---|---|---|---|---|
| **Double&shy;Click** | ✅ | ✅ | ✅ | All display |
| **Criteo** | ✅ | ✅ | ✅ | Retargeting |
| **AppLovin** | ✅ | ✅ | ✅ | Mobile games |
| **Taboola** | ✅ | ✅ | ✅ | All content |
| **AppNexus** | ✅ | ✅ | ✅ | All display |
| **This** | ✅ | ✅ | ✅ | Health chatbots |

The sequence is proven. Most also built moats through lock-in.

|  | Open source | PII stays local | No SDK | Easy exit |
|---|---|---|---|---|
| **Double&shy;Click** | ❌ | ❌ | ❌ | ❌ |
| **Criteo** | ❌ | ❌ | ❌ | ❌ |
| **AppLovin** | ❌ | ❌ | ❌ | ❌ |
| **Taboola** | ❌ | ❌ | ❌ | ❌ |
| **AppNexus** | ✅ | ❌ | ✅ | ✅ |
| **This** | ✅ | ✅ | ✅ | ✅ |

The pattern is proven. The sequence works. What's different here is what's missing: no proprietary SDK, no data extraction, no switching cost. The publisher can leave in one command and take their code with them.

The subsidy is a pilot cost. One publisher, one proof. The attribution reports from that pilot sell the next publisher without a subsidy. The burn rate is a single bet, not a recurring expense.

This blog is the trust signal. The scoring function, the pricing strategy, the go-to-market sequence, the code that runs it all. Published before the first publisher signs. Nothing hidden. A compliance officer can read the entire business model before taking the meeting. Anyone with a Claude Code subscription can point at this blog and say "implement."

The pitch was why. The playbook is four moves: publisher, advertiser, bill, convert.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I outlined the sequence; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
