---
layout: post
title: "Unredactable"
tags: vector-space
image: "/assets/unredactable.jpg"
---

AI companies are burning cash faster than they can monetize with subscriptions, every one of them earning negative margins. The biggest capital budgets in history, all greenlit without a plan to make any money. They're hoping it will eventually turn around. It won't fix itself. Nobody has found a way to monetize conversational AI under the current regulatory, privacy, and user trust constraints.

In this blog, I documented perhaps the only way it could ever work.

So why would I publish the full mechanism design as a blog series? [Scrollytelling](/advertising-journey), [scoring function](/power-diagrams-ad-auctions), [open-source simulation](https://github.com/kimjune01/openauction), blog posts explaining every piece. No company. No product. No funding. Why would anyone give away the secret sauce for free?

![Unredactable](/assets/unredactable.jpg)

## The Alternatives

I could have kept it to myself. Built a company, raised funding, tried to be the next celebrity tech founder. But the only way the mechanism works is if the auction code is public for all to see. It runs in a [TEE](/monetizing-the-untouchable), which means it has to be verifiable by design. Anyone can clone it in a second. There is no proprietary version of a transparent auction. The "secret sauce" would have been copied the moment the first auction cleared.

Or I could have kept it quiet to land a job. Walk into Google Research, whiteboard the scoring function, explain why TEE attestation makes the auction verifiable. They learn everything they need whether they hire me or not. The interview IS the knowledge transfer. The difference is that behind an NDA, nobody else gets it. Google captures the entire chat surface and we get another 20 years of monopoly.

Or I could have tried the academic route. Put my name on a paper, submit to conferences, apply for grants. That takes years of pitching blog posts to some of the highest-paid researchers in human history. We don't have years, and I'd rather not spend the prime years of my life begging for peer review.

## Why We Don't Have Years

OpenAI [quietly deleted](https://theintercept.com/2024/01/12/open-ai-military-ban-chatgpt/) its ban on military use in January 2024. By December, they had a [defense contract with Anduril](https://www.technologyreview.com/2024/12/04/1107897/openais-new-defense-contract-completes-its-military-pivot/). Google [removed](https://www.washingtonpost.com/technology/2025/02/04/google-ai-policies-weapons-harm/) its AI Principles pledge not to develop weapons or surveillance in February 2025, weeks after Sundar Pichai attended Trump's inauguration.

Anthropic was the holdout. In February 2026, they signed a [$200M Pentagon contract](https://www.cnbc.com/2026/02/26/anthropic-pentagon-ai-amodei.html) with restrictions: no mass domestic surveillance, no autonomous weapons. The Pentagon demanded "any lawful use" language. Anthropic refused. On February 27, Trump [ordered every federal agency](https://www.npr.org/2026/02/27/nx-s1-5729118/trump-anthropic-pentagon-openai-ai-weapons-ban) to stop using Claude. The Pentagon designated Anthropic a ["supply chain risk to national security"](https://www.cnn.com/2026/02/27/tech/anthropic-pentagon-deadline) - the only American company ever to receive that designation. Hours later, OpenAI [announced](https://fortune.com/2026/02/28/openai-pentagon-deal-anthropic-designated-supply-chain-risk-unprecedented-action-damage-its-growth/) it had struck its own Pentagon deal.

Altman [admitted](https://www.cnbc.com/2026/03/03/openai-sam-altman-pentagon-deal-amended-surveillance-limits.html) it "looked opportunistic and sloppy." Amodei [apologized](https://fortune.com/2026/03/06/anthropic-openai-ceo-apologizes-leaked-memo-supply-chain-risk-designation/) for a leaked memo calling OpenAI's messaging "straight up lies." Anthropic is [back at the negotiating table](https://www.cnbc.com/2026/03/05/anthropic-pentagon-ai-deal-department-of-defense-openai-.html). [PRISM](https://en.wikipedia.org/wiki/PRISM) showed this playbook in 2013. The AI companies are being captured in public this time, out in the open for all to see. They aren't even trying to hide it.

As the big labs get bigger, the small labs can't compete on the latest model grind. The researchers join the big labs because Anthropic pays $450K and generous equity. Why work for a measly $200K and worthless options at an independent lab? Independent research dies. The models consolidate under a few roofs. Inference becomes a tool for mind control, a direct extension of the government like public schools are. And the alternative is open-weight models out of communist China?

Government regulation accelerates the consolidation. The FTC [fined GoodRx](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising), [fined BetterHelp](https://www.ftc.gov/news-events/news/press-releases/2023/03/ftc-ban-betterhelp-revealing-consumers-data-including-sensitive-mental-health-information-facebook), [banned Cerebral](https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-order-bans-online-mental-health-company-cerebral-using-or-disclosing-sensitive-data-advertising) from using health data for ads. Without a privacy-first architecture, the compliance costs push small publishers toward Google, who can afford the lawyers. Rules framed as "privacy" and "consumer protection" consolidate data infrastructure toward the companies most likely to share it with the state.

Without ad revenue, these chatbot companies either raise until they can't, or sell to a larger player. Every round of consolidation puts private user data inside a data center that the government sponsored.

## The Darkest Thought

I emailed a Google Research scientist who designs RAG auctions. He replied to talk about my work. What if I just handed them the blueprint for the next round of capture? What if they build it, own it, and the government gets access to embedding-level intent data for every chatbot conversation suckling on Google revenue for subsistence?

## That's Exactly Why It Has to Be Open

The mechanism design, the scoring function, and the simulation are all public. Google can build their version, but so can Meta, PubMatic, The Trade Desk, anyone. The government built the wall with FTC enforcement and compliance costs that only incumbents can afford. The compliance gate is a direct path to the castle: [TEE attestation](/monetizing-the-untouchable) satisfies the government's own rules. A two-person chatbot startup gets the same privacy guarantees as Google, because the user's privates stay private without needing promises.

If the embedding layer lives inside any single company's stack, whoever has leverage over that company has leverage over the matching. An open protocol has no single point of pressure. And because it's all published, the mechanism is prior art. Nobody can patent it.

The IAB has seen the [scrollytelling](/advertising-journey). Thirty researchers across mechanism design and auction theory have the papers in their inbox. The ideas are already distributed. In a few days, this page will be on archive.org. Nobody can redact them.

The scrollytelling can't be unscrollytold. But I can disappear. The moment I join a company and they ask me to sign for money, the blog stops. So I'm writing as fast as I can while I still have the intellectual freedom to do so. But I also need to pay rent for my family.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
