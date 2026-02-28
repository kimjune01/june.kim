---
layout: post
title: "Adtech: Who Builds It?"
tags: adtech
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument and sourced the evidence; Claude verified claims and drafted prose.*

*Part of the [adtech](/adtech) series.*

---

The [Keyword Tax](/keyword-tax) showed the switching incentive: embedding auctions redistribute surplus from publishers to the specialists who actually serve niche queries. But who builds the embedding auction? Not one visionary. An equilibrium is emerging from five independent forces — investors, SSPs, regulators, standards bodies, and analysts — each moving for their own reasons toward the same gap.

## The Money

[Theory Ventures](https://tomtunguz.com/koah-theory/) led [Koah's $20.5M Series A](https://www.adweek.com/media/koah-adsense-for-chatgpt-series-a/) in February 2026. Theory's Tomasz Tunguz — a Google AdSense alumnus — wrote: "Every major interface shift finds its answer to meeting the needs of a massive audience in advertising." Koah is the "AdSense for AI" SDK: native ads inside chatbot conversations, [7.5% CTR](https://siliconangle.com/2026/02/24/koah-raises-20-5m-scale-adsense-ai-across-apps/), 2M+ MAU across publishers including [Liner, Luzia, and DeepAI](https://techcrunch.com/2025/09/07/koah-raises-5m-to-bring-ads-into-ai-apps/).

[M13](https://www.m13.co/article/meet-kontext-redefining-the-future-of-ads-in-generative-ai) led [Kontext's $10M seed](https://www.finsmes.com/2025/08/kontext-raises-10m-in-seed-funding.html), joined by Torch Capital. Kontext generates contextual ads at inference time and routes them through PubMatic PMPs. Their [advertisers page](https://www.kontext.so/advertisers) claims 1B+ daily user impressions across their publisher portfolio and 3–5% CTR. [Adweek](https://www.adweek.com/programmatic/pitch-deck-kontext-raises-10-million-funding-ads-in-ai-chatbots/) reported advertisers including Amazon, Uber, and Canva.

The key gap: **neither has an embedding-based auction.** Koah uses keyword-based targeting — Tunguz's "full semantic context" describes real-time query understanding, not geometric bid scoring. Kontext uses LLM-generated ads routed through PubMatic PMPs — curated deals, not an open exchange. Both are proto-SSPs missing the mechanism.

## The Pipes

**PubMatic** is making the biggest bet: an [NVIDIA partnership](https://pubmatic.com/news/pubmatic-delivers-5x-faster-smarter-advertising-decisions-with-nvidia/) for sub-millisecond inference (October 2025), co-founding [AdCP](https://adcontextprotocol.org/) (October 2025), the first [SSP-to-chatbot bridge](https://pubmatic.com/blog/pubmatic-and-kontext-partner-to-open-programmatic-access-to-ai-powered-conversational-inventory/) via Kontext (December 2025), and [AgenticOS](https://pubmatic.com/news/pubmatic-launches-agenticos-the-operating-system-for-agent-to-agent-advertising/) for agent-to-agent ad execution (January 2026). They also [sued Google](https://investors.pubmatic.com/news-releases/news-release-details/pubmatic-files-lawsuit-against-google-restore-fair-competition) for antitrust damages.

The Kontext integration is PMP-first — curated deals, not open auction. This is rational for scarce inventory with unproven demand. But PMPs are bilateral. They don't scale to thousands of advertisers competing for long-tail conversational queries. As chatbot inventory grows, the pricing mechanism that replaces PMPs will need continuous, high-dimensional matching — which is what an embedding auction does.

**The Trade Desk** launched [OpenAds](https://www.thetradedesk.com/resources/openads-enabling-the-most-trusted-efficient-ad-auction) in October 2025 — auditable auction mechanics with code attestations. The signal: demand-side appetite for transparent, verifiable auctions.

All route through traditional RTB pipes. No native embedding-based scoring yet. The pipes are being laid; the auction mechanism is missing.

## The Rules

Antitrust is dismantling Google's ad tech monopoly from three directions. The [DOJ proved](https://www.justice.gov/opa/pr/department-justice-prevails-landmark-antitrust-case-against-google) Google illegally monopolized publisher ad servers and exchanges (April 2025). The [EU fined](https://www.techpolicy.press/breaking-down-the-eu-antitrust-decision-on-google-adtech/) Google €2.95B for self-preferencing (September 2025). Five SSPs — [OpenX](https://www.adexchanger.com/platforms/openx-becomes-the-first-ssp-to-sue-google-for-antitrust-damages/), PubMatic, Magnite, Raptive, Index Exchange — have filed private suits; the [SDNY applied issue preclusion](https://searchengineland.com/google-quietly-increases-ad-prices-targets-432155), so Google cannot relitigate liability.

The game theory matters more than the legal details. Every practice the court found — [Project Bernanke](https://www.techpolicy.press/how-google-manipulated-digital-ad-prices-and-hurt-publishers-per-doj/) (secret bid deflation), Project Poirot (steering demand from rival exchanges), First Look, Last Look — exploits the same lever: **information asymmetry**. Bernanke worked because Google knew the second-highest bid and competitors didn't. Poirot worked because Google controlled both buy-side and sell-side and could steer demand invisibly. The [MRC now requires](https://www.mediapost.com/publications/article/412394/going-going-gone-mrc-finalizes-ad-auction-stand.html) disclosing "use of advance information about bids and budgets" — a direct response.

An embedding auction with an open scoring function — `score = log(bid) - distance² / σ²` — eliminates this lever entirely. Every advertiser can compute their own score and every competitor's score for any query point. There's no hidden bid manipulation because the geometry is public. The auction is transparent not by policy but by construction.

## The Standards

The [Ad Context Protocol](https://adcontextprotocol.org/) launched in October 2025, founded by 20+ companies including Yahoo, PubMatic, and Magnite. AdCP is an [advertising-specific wrapper](https://docs.adcontextprotocol.org/docs/intro) built on Anthropic's Model Context Protocol — any MCP-compatible LLM can execute ad campaigns through standardized tasks. The [GitHub repo](https://github.com/adcontextprotocol/adcp) shows real infrastructure: v2.0 to v3.0-beta in four months.

The **IAB Tech Lab** published an [agentic roadmap](https://iabtechlab.com/press-releases/iab-tech-lab-unveils-agentic-roadmap-for-digital-advertising/) in January 2026: extending OpenRTB for agentic execution, open-source reference implementations, and a neutral MCP reference server for advertising. The **IAB CoMP** working group invited OpenAI, Anthropic, Google, Meta, and Perplexity — though [Digiday reported](https://digiday.com/media/the-coalition-of-the-willing-and-unable-publishers-rally-to-wall-off-ais-free-ride/) that only Google and Meta actually participated in initial workshops. The AI companies at the center of the problem didn't show up.

The CoMP coalition's proposed monetization model is a hybrid: pay-per-crawl (charge AI companies each time a bot ingests content) plus revenue share when content powers a response. The blocking strategy makes sense — publishers need leverage. But pay-per-crawl as a monetization signal has the same problem as pageviews: it rewards being ingested often, not being useful. Content farms will optimize for crawl volume the way they optimized for SEO. An embedding auction scores differently. Payment flows to whoever is semantically closest to the user's actual query — closest to the problem being solved — not whoever gets scraped the most.

The protocol layer is being built. AdCP even has a "[Sponsored Intelligence](https://docs.adcontextprotocol.org/docs/intro)" module — conversational ad sessions with `si_initiate_session` and `si_send_message` tasks. But Sponsored Intelligence is a delivery format: it defines how an ad enters a conversation, not how the auction decides *which* ad wins. There's no scoring mechanism. No bid-distance tradeoff. No geometric allocation rule. The gap is the auction layer itself — the module that takes a query embedding, a set of advertiser positions and bids, and returns a winner with a verifiable score. That's the piece this series has been building toward.

## The Signal

**Ben Thompson** [argued](https://stratechery.com/2025/the-agentic-web-and-original-sin/) that a world of one dominant AI making exclusive deals with a few blessed content creators is "a far less interesting one" than one driven by marketplaces and auctions. His proposed mechanism: AI providers build an auction that pays content sources based on usage frequency, settled via stablecoins at the protocol layer. The marketplace framing is right — and the settlement infrastructure he describes (protocol-level micropayments) could be the rails an embedding auction runs on.

Agentic traffic makes the case concrete. A user asking an agent "my basement floods every spring, what are my options?" will never see a car insurance banner — but a sump pump comparison or a waterproofing contractor is directly relevant. Only ads that match the intent survive the agentic filter. SEO can't serve this — it takes months to rank, favors incumbents, and optimizes for a search engine's algorithm rather than the user's problem. A startup with a better sump pump can't outrank Home Depot on Google, but it can bid closer to the query in embedding space. Proximity is instant, meritocratic, and indifferent to brand size.

**Perplexity** [abandoned ads entirely](https://www.macrumors.com/2026/02/18/perplexity-abandons-ai-advertising/) in February 2026 — total ad revenue of $20K, trust damage not worth it. Validates the externalized SSP model: if the platform doesn't run ads itself, trust is preserved.

**OpenAI** is [testing ads at $60 CPM](https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html) with a $200K minimum — first-party, opaque, not scalable to the long tail. **Anthropic** ran a [Super Bowl ad](https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html) with the tagline: "Ads are coming to AI. But not to Claude."

The signal from all directions: first-party chatbot ads either fail (Perplexity) or are expensive and opaque (OpenAI). The SSP model — externalized, transparent, auditable — is the remaining path.

## What's Missing

Each force has a piece. Investors fund proto-SSPs. SSPs bridge to chatbot inventory. Regulators demand transparency. Standards bodies build protocols. Analysts call for marketplaces.

### The Mechanism

One exchange has been building toward this. [CloudX](/letter-to-cloudx) already runs TEE-attested auctions — clearing code inside AWS Nitro Enclaves with [open-source auction logic](https://github.com/cloudx-io/openauction). What they haven't shipped yet is the embedding layer: the [power diagram scoring](/power-diagrams-ad-auctions), [per-advertiser σ](/keywords-are-tiny-circles), [relocation fees](/relocation-fees) that prevent Hotelling collapse, and the [simulation evidence](/relocation-fee-dividend) that fees create a dividend, not a tax. They have the trust infrastructure. The mechanism design from this series is the missing piece.

### The Trust Problem

There's a trust gap that none of the current players have solved. Perplexity abandoned ads because showing them eroded user trust. Anthropic promised "not to Claude." But the SSP model — externalize ads to a third party — doesn't fix this by itself. If a chatbot sends query embeddings to an SSP for auction scoring, the SSP now holds user intent data. Embeddings can be approximately reversed. "We don't run ads" is not a privacy guarantee if user queries flow to a third party that does.

### The Resolution: TEE Attestation

The auction runs inside a trusted execution environment on the chatbot's own infrastructure. The query embedding enters a sealed enclave. The scoring function (`log(bid) - distance² / σ²`) executes inside it. The enclave returns only the winning ad — the SSP never sees the query, the embedding, or any losing bids. Remote attestation proves that the code running inside the enclave is the published, audited scoring function, not something modified to exfiltrate data. Advertisers can verify their scores were computed correctly. Users get a cryptographic guarantee that their conversation never left the chatbot's infrastructure.

This is the privacy architecture that lets "externalized ads" and "user trust" coexist. It's a stronger claim than "we don't run ads" (which Perplexity tried and abandoned) and stronger than "trust us" (which is all OpenAI currently offers). The chatbot company can say: your query stays here, the auction runs in a sealed enclave, and here's the attestation proof.

### The Incumbent's Play

Google doesn't need to build the embedding auction. They need to make sure nobody else does it at scale.

An embedding auction has natural monopoly dynamics — advertisers go where the queries are, queries go where the advertisers are. A single dominant embedding SSP would threaten keyword revenue the way the [Keyword Tax](/keyword-tax) simulation showed: specialists switch to wherever they stop losing money, and the switching incentive compounds. Google's rational response: invest in several competing embedding SSPs and ensure the market stays fragmented. Five small exchanges competing with each other can't achieve the liquidity that makes any one a real alternative to keywords. The threat gets defused not by blocking it but by splintering it.

The defense is the open protocol. If every embedding SSP runs the same scoring function and settles through the same protocol, advertisers plant a position once and compete on every exchange simultaneously — the way RTB already works today. Without a shared protocol, Google wins by backing five horses and making sure none of them finish.

### Open or Proprietary

The question isn't whether it gets built. It's whether it's open or proprietary. And the regulatory environment is pushing hard toward open.

## Caveats

- **Koah may evolve into this.** Tunguz's "full semantic context" could become embeddings under the hood. Their SDK already processes queries in real time — the distance from query understanding to geometric scoring is small.
- **AdCP could add an embedding scoring module.** The protocol is extensible by design. A new task type for `score_embedding_bid` would fit the existing architecture.
- **Google could preempt or fragment.** Building an open embedding auction risks cannibalizing keyword revenue. Investing in competing SSPs to fragment the market is cheaper and harder to detect — but only works if there's no shared protocol.
- **Standards bodies move slowly.** IAB Tech Lab's OpenRTB extensions may take 12–18 months. The market may outrun them.
- **PubMatic is best-positioned incumbent** — NVIDIA partnership for latency, Kontext partnership for chatbot inventory, AgenticOS for agentic execution, AdCP co-founding for protocol access. But they've never built auction mechanism design from scratch.

The pieces are on the board. Someone assembles them.
