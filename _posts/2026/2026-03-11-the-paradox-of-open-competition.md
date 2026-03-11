---
layout: post
title: "The Paradox of Open Competition"
tags: reflecting
---

Traditionally, companies hide their code. NDAs, proprietary licenses, obfuscation. The fear: if a competitor sees your source, they can reproduce your product. That fear made sense when reading code was the only way to understand how something worked.

It doesn't make sense anymore.

## The Fool's Errand

Claude 4.5 can look at a product's UI, infer its behavior, and produce a working replica without ever seeing the code that built it. CNBC reporters with [zero coding experience rebuilt Monday.com](https://www.cnbc.com/2026/02/05/how-exposed-are-software-stocks-to-ai-tools-we-tested-vibe-coding.html) in under an hour for less than $15 using Claude Code. A developer [cloned ChatGPT's interface](https://x.com/Saboo_Shubham_/status/1804702852583190807) from a screenshot in two minutes with Claude 3.5 Sonnet. [StrongDM](https://simonwillison.net/2026/Feb/7/software-factory/) ships production security software where no human writes, reads, or reviews code.

Investors call it the [SaaSpocalypse](https://techcrunch.com/2026/03/01/saas-in-saas-out-heres-whats-driving-the-saaspocalypse/). Between January and February 2026, [$2 trillion](https://www.cnbc.com/2026/02/06/ai-anthropic-tools-saas-software-stocks-selloff.html) in software market cap evaporated. Atlassian dropped 35%. Salesforce dropped 28%. The S&P 500 Software Index fell 30%, erasing all gains since ChatGPT's launch. Builders are practicing what investors fear: [Klarna ditched Salesforce](https://techcrunch.com/2025/03/04/klarna-ceo-doubts-that-other-companies-will-replace-salesforce-with-ai/) and built their own AI replacement, saving $2 million. [Pieter Levels](https://www.fast-saas.com/blog/pieter-levels-success-story/) runs multiple SaaS products generating $3 million a year with zero employees.

So if your moat is "they can't see the code," you're protecting something that doesn't need seeing. The blog post is the prompt. The product demo is the blueprint. Hiding the source code from a world where the source code is trivially inferrable is a fool's errand.

## What Hiding Actually Costs You

Hiding your code fails to protect you. Worse, it refuses to consider the possibility that your competition might execute better than you on the same idea. Which they might.

When the code is hidden, the customer's evaluation criteria are fuzzy. Whose UI looks more polished? Whose servers respond faster? Whose compliance checklists are tighter? Who's better funded and more likely to survive? Who's more popular on Twitter and HN so I'll get more approval for picking the obvious choice? These are proxies. They're the best signals available when the real signal, who actually built the better system, is locked behind a login.

Now consider the matrix:

|  | **Innovator** | **Follower** |
|--|--|--|
| **Closed source** | Signals: funding, polish, popularity | Signals: funding, polish, popularity |
| **Open source** | Signal: commit timestamps | Signal: fork timestamps |

When the source is closed, the customer chooses between two black boxes using the same fuzzy signals. The follower can plausibly claim to be the innovator. Marketing budgets decide.

When the source is open, the customer chooses between the original repo and the fork. Every other signal collapses. The commit history is the proof. The timestamp of who came first is more trustworthy than any pitch deck.

For as long as the innovator is credibly innovating at a predictable rate, it's fair to assume the follower will never catch up. The customer receives a more innovative product by choosing the original. Open source makes the innovator's advantage *legible*.

## Open Source Is the Greedy Choice

I'm not a principled copyleft guy. This isn't about freedom or ethics or Richard Stallman's [four freedoms](https://www.gnu.org/philosophy/free-sw.en.html). Stallman was considered crazy to give up riches for principle. Linus Torvalds is worth [$150 million](https://www.celebritynetworth.com/richest-businessmen/linus-torvalds-net-worth/). Comfortable, but probably not a billionaire. For decades, the conventional wisdom was that open source is a sacrifice. You give up potential revenue, competitive advantage, control. In exchange you get community goodwill and the warm feeling of contributing to the commons.

That framing is dead. Open source is the greedy choice now, and the data proves it.

[Serena Capital's 2024 Commercial Open Source Report](https://blog.serenacapital.com/the-commercial-open-source-report-2024-3b4a8b4ebd08) found that open-core companies reach median IPO valuations of $1.3 billion versus $171 million for closed-source companies. They get to Series A 20% faster, Series B 34% faster, and convert from seed to Series A at 91% higher rates. This isn't a charity with good outcomes. This is a superior business strategy by every measurable metric.

The market is acting on it. [Twenty](https://techcrunch.com/2024/11/18/twenty-is-building-an-open-source-alternative-to-salesforce/) (YC S23) is building an open-source Salesforce. [Ubicloud](https://techcrunch.com/2024/03/05/ubicloud-wants-to-build-an-open-source-alternative-to-aws/) (YC W24) is building an open-source AWS. [Supabase](https://fortune.com/2025/04/22/exclusive-supabase-raises-200-million-series-d-at-2-billion-valuation/) (YC S20) built an open-source Firebase and hit a $2 billion valuation. [Cal.com](https://cal.com/) is open-source Calendly. [Documenso](https://documenso.com/) is open-source DocuSign. [PostHog](https://sacra.com/research/posthog-anti-modern-data-stack/) is open-source product analytics that hit [100,000 customers](https://posthog.com/handbook/story) and $9.5 million ARR through product-led growth alone. YC batches are full of companies whose entire pitch is "X, but open."

Closing what was open backfires spectacularly. In August 2023, [HashiCorp switched Terraform from MPL to BSL](https://spacelift.io/blog/terraform-license-change), a source-available license that restricts commercial use. Within two weeks, the [OpenTofu manifesto](https://opentofu.org/manifesto/) had 33,000 GitHub stars and 140 companies pledging support. The Linux Foundation accepted the fork. AWS, Google Cloud, and Oracle backed it. HashiCorp sent a cease-and-desist. It became a PR disaster. The same pattern played out with [MongoDB](https://en.wikipedia.org/wiki/Server_Side_Public_License) (2018), [Elasticsearch](https://devclass.com/2021/01/18/elastic-changes-licensing/) (2021, AWS forked it into OpenSearch), and [Redis](https://www.infoq.com/news/2024/03/redis-license-open-source/) (2024, Linux Foundation forked it into Valkey). Redis eventually [reversed course](https://kuray.dev/blog/backend-development/rediss-u-turn-abandoning-sspl-and-returning-to-open-source-202505) and went back to open source. [No clear link](https://redmonk.com/rstephens/2024/08/26/software-licensing-changes-and-their-impact-on-financial-outcomes/) between any of these license changes and improved revenue.

Greed points open now. In the past, open source people were the idealists and closed source people were the pragmatists. Now the pragmatists are going open because it's the dominant strategy. The principles go out the window when being open is the profitable option. Nobody needs to invoke Stallman's ethics to justify a strategy that produces 7.6x better IPO valuations.

## Why Small Beats Big

Open source selects for a different kind of company. When the code is visible, customers evaluate the product directly and brand reassurance matters less. So why would they choose the small innovator over the behemoth incumbent?

Consider [WorkOS](https://workos.com/), an enterprise authentication platform founded by Michael Grinich in 2019. They sell SSO, SCIM directory sync, and MFA to SaaS developers, competing directly with Auth0 (now owned by Okta, a $12B company with decades of enterprise entrenchment). Anthropic chose WorkOS. So did OpenAI, Cursor, Perplexity, Replit, and Vercel.

Why? [Michael Grinich](https://evilmartians.com/events/podcast-michael-grinich-workos) tells the story: Anthropic initially sold into huge companies without SSO. A year later, every enterprise customer was demanding it or threatening to churn. The security scrutiny on AI tools is the highest of any software category. They needed it fast and they needed it right.

WorkOS obliged. They had the fewest conflicting priorities. Whatever Anthropic needs, they ask for as a feature. WorkOS will fulfill that request faster and better than Auth0 because they are unencumbered by thousands of legacy enterprise customers whose feature requests also have to coincide in quarterly planning meetings. Anthropic doesn't have a quarter to wait.

Nobody gets fired for hiring IBM. That's been the saying for literal decades. But it's wrong now, and it was always a bad heuristic. The reason Anthropic went with WorkOS is precisely because WorkOS is small and hungry. At that point of decision, no amount of pricing strategy or playing golf with Anthropic execs (or whatever tech execs in SF like to do these days for fun, I'm scared to ask) is enough to convince them that Auth0 is the better choice.

Small. Agile. Open. Trustworthy. Easy to help.

## Where Moats Actually Are

No amount of AI will replicate the trust that comes from being the person who built the thing, in public, with receipts. The commit history is the resume. The repo is the pitch deck. Those moats get *stronger* the more you open up.

The more you share, the harder you are to replace. The more you hide, the easier you are to clone.

If that's true, it changes more than competitive strategy. It changes what a company even [is](/armed-guards-at-the-bouncy-castle).

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched citations and drafted prose.*
