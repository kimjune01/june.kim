---
layout: post
title: "The Last Ad Layer"
tags: coding
---

The deal was simple. Free access to the world's information in exchange for your attention. You'd see ads. The ads would be relevant. Publishers would get paid. Everyone wins.

That deal is broken.

What the ad-supported web actually delivered was surveillance, manipulation, and a content ecosystem that optimizes for keeping you scrolling rather than helping you find what you need. A physical therapist who specializes in climbers' finger injuries — a real person solving a real problem — spends her evenings filming TikTok hooks instead of studying biomechanics. The content treadmill rewards spectacle, not expertise. And the people who need her can't find her.

This isn't an ad tech problem. It's an internet architecture problem. And for a narrow window — maybe 18 to 36 months — there's a way out.

## The Backbone Broke

Search was the backbone of the ad-supported internet. Not one channel among many — the foundation. Google Search was how people found things, how businesses got found, how the entire ad economy priced attention. Every other discovery channel — social media marketing, content strategy, paid ads — was built on top of search or in reaction to it.

Google's AI Overviews now answer queries directly, suppressing the links that used to connect searchers to experts. Organic click-through rates [dropped 65%](https://www.dataslayer.ai/blog/google-ai-overviews-the-end-of-traditional-ctr-and-how-to-adapt-in-2025) on queries where AI Overviews appeared. Zero-click searches — where you never leave Google — account for [roughly 60% of all queries](https://www.semrush.com/blog/ai-search-seo-traffic-study/). The SEO game that small businesses spent a decade learning is over. The links are gone. Google itself killed them — not because it wanted to destroy the ecosystem, but because answering the query directly keeps users on Google longer. The backbone was sacrificed for engagement.

**Social filled the gap, then captured it.** When search stopped delivering traffic, businesses moved to social media. Social media platforms then completed the cycle Cory Doctorow calls [enshittification](https://doctorow.medium.com/big-techs-attention-rents-fe97ba3fad90): first they serve users, then they exploit users for advertisers, then they exploit advertisers to extract all remaining value. The algorithm doesn't surface the best climbing instructor. It surfaces the climbing instructor who films the most engaging 30-second clips. Expertise and performance are different skills. The platforms select for performance.

**Paid search priced out the long tail.** The last fallback was paying for the traffic that used to be free. Google Ads operates on keywords — discrete text strings that advertisers bid on. "Physical therapy" is a keyword. Five physical therapists — a climbing specialist, a pelvic floor specialist, a pediatric specialist, a sports rehab specialist, and a generalist — all bid on it. The auction can't tell them apart. The climbing PT pays to compete on pelvic floor queries she'll never convert on. In a [recent industry poll](https://searchengineland.com/small-businesses-compete-google-ads-462009), more than 50% of respondents said small businesses have been priced out of Google Ads entirely. The keyword auction extracts maximum revenue by forcing specialists into competitions they can't win.

Every channel failed at once. Not cyclically. Structurally.

## The Chatbot Migration

People aren't stupid. When search results became ads and AI summaries, when social feeds became engagement traps, people migrated to the one interface that actually answers questions: AI chatbots.

ChatGPT has 800 million users. Perplexity, Claude, Gemini, and dozens of smaller tools handle millions more queries daily. People ask them everything — *my finger hurts after a climbing session, should I see a physical therapist?* — in natural language, expecting direct answers.

This is the right response to a broken discovery layer. Ask a question, get an answer, skip the noise.

But someone has to pay for inference. Every query costs money — AI isn't free the way search pretended to be. OpenAI's inference costs hit [$8.4 billion in 2025](https://www.wheresyoured.at/oai_docs/) and are projected to reach [$14 billion in 2026](https://finance.yahoo.com/news/openais-own-forecast-predicts-14-150445813.html). The company is forecasting a [$25 billion cash burn](https://mlq.ai/news/openai-revises-projections-upward-with-112-billion-extra-cash-burn-by-2030/) this year. Against that, they're [targeting $1 billion in ad revenue](https://techcrunch.com/2026/02/09/chatgpt-rolls-out-ads/) from free users — less than 7% of their inference bill. They launched ads in ChatGPT on February 9.

The ad layer is following people into the chatbot. And the gap between what ads need to earn and what they currently earn guarantees that the pressure to extract more from every query will only increase.

## The Fork

This is the moment that determines the next decade of the internet. The ad layer that gets installed inside AI chatbots will shape how billions of people discover products, services, and expertise. There are two paths.

**Path one: keywords again.** Take the existing ad infrastructure — keyword matching, category taxonomies, opaque auction mechanics — and bolt it onto chatbot conversations. This is what's happening now. OpenAI's ad system is closed. Nobody outside the company can verify how ads are targeted, priced, or selected. Conversational queries don't map to keywords — they're paragraphs, not strings. Cramming them into keyword resolution destroys the signal.

**Path two: match problems to expertise.** A conversational query has a precise meaning in the vector space where AI models represent language. *Rock climbing finger pulley injury rehabilitation* and *pelvic floor exercises after C-section* are far apart in that space. An ad auction that scores by proximity between the query's meaning and the advertiser's declared expertise can connect people to the right specialist without forcing unrelated businesses to bid against each other.

This isn't a theoretical distinction. It's the difference between advertising as interruption and advertising as introduction. And it's the difference between an internet where lead-gen-dependent small businesses have no sustainable channel, and one that supports millions of them.

## Matching by Meaning

Every modern AI model converts text into coordinates — high-dimensional vectors called embeddings that capture semantic meaning. Similar concepts land near each other. Dissimilar concepts land far apart. This is how chatbots understand language. It's already running at scale, billions of times a day.

An embedding-space auction lets each advertiser plant a flag at a point in this space that represents what they actually do. The climbing PT positions at her niche. The pelvic floor PT positions at hers. When a query arrives, the auction scores each advertiser by a formula that combines their bid with their proximity to the query: the closer your expertise is to what the person actually needs, the less you have to bid to win.

Keywords are a special case of this system — a keyword is just an embedding with zero radius. Everything that works today keeps working. The extension is purely additive. Specialists who were being taxed by dense keyword auctions can now compete only on the queries where they actually convert.

A person who asks a chatbot *I need a financial planner who understands freelance translation income* gets matched to someone who actually does that — not the highest bidder on "financial planning." The targeting comes from the geometry of meaning, not from surveillance, not from cookies, not from behavioral profiles. The person stated what they need. The auction connects them to it.

## The Trust Chain

The math is [published](https://arxiv.org/abs/2406.09459). The implementation is not the hard part. Trust is — and trust is a chain. Every link has to hold.

If a single company controls the ad auction inside a chatbot — sets the scoring function, runs the embedding model, determines who wins, decides how results appear — then users and advertisers are back where they started. Trusting the platform. Hoping it's fair. Unable to verify. This is Google's current model. It works for Google. It doesn't work for anyone else.

The alternative is a chain of trust where every link is verifiable:

**Link one: verifiable intent matching.** Open-weight embedding models like [Nomic](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5), BGE, and GTE are publicly available. Anyone can run the same model on the same text and get the same coordinates. No one has to trust the exchange to convert text to meaning correctly — you can check it yourself.

**Link two: verifiable auction execution.** Trusted execution environments — hardware enclaves that prove a specific piece of code ran unmodified. AWS Nitro Enclaves, Intel SGX, and others let an exchange publish its auction code and then prove, cryptographically, that the published code is what actually processed the bid. Not "trust us." Verify it. One ad exchange already runs this way, with the [code open-sourced](https://github.com/cloudx-io/openauction). The infrastructure exists and is in production.

**Link three: presentation that respects the user.** The first two links guarantee that the right match was found honestly. The third determines whether the user experiences it as help or as noise. When a chatbot conversation surfaces a relevant expert, the UX should present it as a suggestion — *a climbing PT who specializes in finger pulley injuries is available in your area* — not as a banner ad crammed into the response. The difference is whether the system treats the user as someone to connect or someone to sell to. Labeled clearly, offered at the right moment, relevant to what the person actually asked — that's introduction, not interruption. If the first two links work and the third one fails, the user still feels sold to, and trust collapses regardless of how clean the auction was.

Break any link and you're back to the same extractive ad layer wearing a new interface. Hold all three and you have an open protocol for advertising.

## Discovery Is Infrastructure

Doc Searls wrote [*The Intention Economy*](https://doc.searls.com/2024/12/30/the-real-intention-economy/) in 2012, arguing that the internet should let buyers signal intent directly to sellers instead of being tracked, profiled, and targeted. Fourteen years later, that hasn't happened — not because the idea was wrong, but because there was no protocol to make it work.

Embedding-space auctions are that protocol. A person stating *I need a financial planner who understands freelance translation income* is expressing intent with more precision than any tracking pixel or cookie ever captured. They're not being surveilled. They're declaring what they need. An auction that matches declared intent to declared expertise — verifiably, without intermediary manipulation — is the mechanism Searls described. The technology to build it didn't exist in 2012. It does now.

Brendan Eich built Brave and the Basic Attention Token to route ad revenue directly to users and cut out surveillance intermediaries. The structural insight was right: the ad layer needs to be rebuilt, not reformed. BAT approached it from the browser. Embedding auctions approach it from the auction mechanism itself. The two aren't competing — they're complementary layers of the same architectural argument.

The internet's discovery layer is infrastructure. Like roads. Like the postal system. When it works, experts find the people who need them and the internet delivers on its original promise. When it's captured by platforms optimizing for engagement and extraction, expertise dies on a content treadmill and consumers get noise instead of signal.

## Fragmentation, Not Monopoly

The threat isn't that one company monopolizes the chatbot ad layer. Google is under [active antitrust enforcement](https://www.justice.gov/atr/case/us-and-plaintiff-states-v-google-llc-2023) — the DOJ ruled they monopolized ad tech, and remedies may include breaking up parts of their ad business. The DoubleClick-to-dominance playbook probably can't repeat under that scrutiny.

The threat is fragmentation. OpenAI builds a closed ad system. Google builds a closed ad system. Perplexity, Anthropic, and a dozen vertical chatbot platforms each build their own. None of them interoperate. Five walled gardens instead of one — each with its own targeting taxonomy, its own opaque auction, its own advertiser onboarding. The climbing PT doesn't face one monopolist. She faces five separate platforms, each requiring separate campaigns, separate budgets, separate creative, none of them sharing a protocol. That's worse than a monopoly. At least a monopoly has liquidity.

The pieces to prevent this are converging independently. Academics are publishing embedding-space auction mechanisms. Industry labs have production-grade embedding infrastructure. Standards bodies are [forming working groups](https://iabtechlab.com/press-releases/iab-tech-lab-forms-ai-content-monetization-protocols-comp-working-group-to-set-ai-era-publisher-monetization-standards/) for AI-era monetization. Platform companies are launching ad products inside chatbots. An exchange has TEE attestation in production.

Nobody has assembled them into a single open protocol.

The window is the period between "every platform needs ad revenue" and "every platform has built its own proprietary system." Once each platform ships a closed ad product, switching costs lock it in — advertisers build campaigns, integrations harden, inertia takes over. Based on how fast these companies move, that window is approximately 18 to 36 months.

If an open protocol ships first, it becomes the default the way HTTP became the default — not because a committee chose it, but because it was open, implementable, and solved a real problem. Every chatbot platform that needs ad revenue — and they all do, because inference costs money — adopts the shared protocol rather than building from scratch. One campaign reaches every platform. One auction clears across the entire chatbot ecosystem. Liquidity pools instead of fragmenting.

If the protocol doesn't ship in time, the chatbot ad layer fragments into incompatible walled gardens. Each platform extracts maximum rent from both sides. Small businesses run five separate ad campaigns to reach the same audience across five platforms. The keyword tax replicates five times over.

The climbing PT goes back to filming TikToks.

## Who Goes First

The technology exists. This is a coordination problem.

One exchange needs to add embedding parameters to its auction — optional fields that let advertisers specify a position, a radius, and a model. Keywords keep working as before. Embedding-aware demand is additive.

One chatbot platform needs to route its ad inventory through an open exchange instead of building a proprietary system. Queries flow in as embeddings. The auction clears by proximity. Specialists win their own queries and stop paying for each other's.

One standards body needs to add an embedding vector field to the bid request spec — a few optional fields in the protocol. Once it's in the spec, every exchange and every platform can implement it.

None of these steps requires a breakthrough. Each requires someone to go first.

---

If you're building an ad exchange, a chatbot platform, or setting standards for AI-era monetization — the [mechanism is described](https://www.june.kim/power-diagrams-ad-auctions), the [simulation is open source](https://github.com/kimjune01/openauction/tree/main/cmd/simulate), and the [infrastructure exists](https://github.com/cloudx-io/openauction). I want to hear from you: [june@june.kim](mailto:june@june.kim).

---

*The technical argument: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap) · [Keywords Are Tiny Circles](/keywords-are-tiny-circles) · [It Costs Money to Move](/relocation-fees) · [The Relocation Fee Dividend](/relocation-fee-dividend) · [An Open Letter to CloudX](/letter-to-cloudx) · [The Convergence](/the-convergence) · [The Keyword Tax](/keyword-tax) · [Who Builds It?](/who-builds-it). Written with help from Claude Opus 4.6.*
