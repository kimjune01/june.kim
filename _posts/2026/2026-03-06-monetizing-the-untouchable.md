---
layout: post
title: "Monetizing the Untouchable"
tags: vector-space
image: "/assets/ftc.jpg"
---

Health publishers can't run ads. The FTC fined [GoodRx](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising) $1.5 million, fined [BetterHelp](https://www.ftc.gov/news-events/news/press-releases/2023/03/ftc-ban-betterhelp-revealing-consumers-data-including-sensitive-mental-health-information-facebook) $7.8 million, fined [Cerebral](https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-order-bans-online-mental-health-company-cerebral-using-or-disclosing-sensitive-data-advertising) $7 million and banned them from using health data for advertising entirely. Any publisher sitting on health-adjacent conversations treats that inventory as untouchable. The compliance risk is existential. The revenue stays at zero.

![Monetizing the untouchable](/assets/ftc.jpg)

That inventory is some of the highest-intent traffic on the internet. A user describing symptoms to a chatbot is further down the funnel than someone typing two words into a search box. A user who describes [lateral knee pain on long runs with a race eight weeks out](/marketing-speak-is-the-protocol) should get matched to a sports rehab PT who specializes in keeping athletes in training. Google would match "knee pain running" to the highest bidder. The signal exists. The question is whether ad matching can work without the data ever crossing a boundary.

## What Triggers Enforcement

Every FTC health data enforcement action required the same thing: a third party acquired identifiable health information.

GoodRx sent prescription data to Facebook via tracking pixels. Facebook acquired it. BetterHelp sent mental health intake responses to Snapchat and Criteo. Cerebral sent diagnosis information to LinkedIn and TikTok. In every case, the ad platform received identifiable health data in cleartext. The Health Breach Notification Rule ([16 CFR 318](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-318)) is explicit: "acquisition of PHR identifiable health information without the authorization of the individual." No acquisition, no breach.

The FTC's consent decrees confirm this. Every one focuses on transfer: "respondent disclosed [health information] to [third party]." Every remedy prohibits future sharing. None prohibits future use of internally-held data. The line is acquisition.

Data clean rooms were supposed to solve this. The FTC published a [blog post on data clean rooms](https://www.ftc.gov/policy/advocacy-research/tech-at-ftc/2024/11/data-clean-rooms-separating-fact-fiction) in November 2024. The message was blunt: DCRs "can be used to obfuscate privacy harms," and the technology "isn't inherently protective." DCRs fail because the data still moves. The operator receives it, promises not to look, and sometimes looks anyway. GoodRx had confidentiality provisions with Facebook. The FTC was unimpressed.

Every previous approach failed because data crossed a boundary.

## How No One Acquires It

The publisher keeps the conversation. When a user describes lateral knee pain on long runs, the publisher extracts the intent and computes an embedding on its own infrastructure. The raw conversation never leaves.

Advertiser embeddings are public. An advertiser's position in embedding space is a claim of expertise: "sports injury rehab for competitive athletes who need to keep training." The exchange publishes the full catalog, and the publisher caches a local copy. Phase one of the [two-phase model](/ask-first) runs entirely on the publisher's servers: cosine distance between the conversation embedding and cached advertiser positions, rendered as a proximity indicator. No data moves. No auction runs.

If the user taps, the embedding enters a [TEE](/model-blindness) running on [AWS Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/). The publisher encrypts the embedding with the enclave's public key, verified through [remote attestation](https://docs.aws.amazon.com/enclaves/latest/user/verify-root.html). The exchange operator's infrastructure routes the ciphertext but cannot decrypt it. Inside the enclave, the TEE computes distances against all advertiser positions, combines them with each advertiser's dynamic bids, budgets, and pacing rules, runs the full auction with `log(bid) - distance² / σ²`, and returns a winner ID and price. The embedding is destroyed after execution.

**Publisher**: keeps the raw conversation. Sends only an encrypted embedding that the exchange operator cannot read.

**Exchange operator**: deploys the enclave, cannot inspect its execution. AWS Nitro strips hypervisor access to enclave memory.

**Advertiser**: submits bidding rules to the TEE. Learns they won and what they pay. Nothing about the user.

**Chatbot**: [doesn't know advertising exists](/model-blindness). Separate system, one-directional data flow.

The HBNR covers "unsecured" PHR identifiable health information, defined as data not "rendered unusable, unreadable, or indecipherable" through specified technologies. An embedding encrypted in transit and processed inside hardware the operator cannot access meets that standard. The FTC has [never tested this safe harbor](https://fpf.org/resource/confidential-computing-and-privacy-policy-implications-of-trusted-execution-environments/) in an enforcement context involving confidential computing. But the statutory language supports it.

State health privacy laws like Washington's [My Health My Data Act](https://app.leg.wa.gov/billsummary?BillNumber=1155&Year=2023&Initiative=false) regulate collection, sharing, and sale of health data. The exchange operator receives ciphertext it cannot read, processed inside hardware it cannot inspect, destroyed after execution. If routing encrypted data to a TEE constitutes "collection," then every HTTPS request to a cloud-hosted health app is collection by the CDN. The counterargument is purpose: a CDN doesn't care what's in the payload, while the exchange operator built the system to extract value from it. But purpose is irrelevant when access is physically impossible. The operator can't read the data, can't store the data, and the TEE proves both. That standard would break the internet.

Google serves pharmaceutical ads against "depression symptoms" and PT ads against "knee pain running" every day. The FTC has never pursued this, because matching a relevant ad to a voluntarily submitted query is search working correctly. Intent casting does the same thing with stronger privacy.

## Consent and Proof

Two questions remain: does the consent hold up, and can anyone verify the claims?

The FTC's [updated Health Breach Notification Rule](https://www.federalregister.gov/documents/2024/04/26/2024-07898/health-breach-notification-rule) deliberately left "authorization" undefined, but the enforcement pattern is clear: consent must be meaningful, not buried in a banner. Cookie banners fail this. They are designed to be clicked through. [Dark patterns](https://www.ftc.gov/news-events/news/press-releases/2024/06/ftc-staff-report-finds-large-social-media-and-video-streaming-companies-have-engaged-vast) make rejection harder than acceptance. Regulators on both sides of the Atlantic are cracking down, which tells you what they think of checkbox consent.

The [two-phase model](/ask-first) satisfies the standard by construction. Phase one shows a proximity indicator, computed locally against cached advertiser embeddings on the publisher's own infrastructure. No data leaves the publisher. No auction runs. Phase two requires the user to tap. Then the encrypted embedding enters the TEE and the auction fires. The default state is no ad. The user who never taps never sends any data beyond the publisher's servers. Consent is expressed through action.

GoodRx said it protected user privacy. Its tracking pixels said otherwise. Every FTC health data case has the same structure: a stated commitment to privacy, and a technical implementation that contradicted it.

The [trust chain](/the-last-ad-layer) makes this gap impossible. [Open-weight embedding models](/the-convergence) with published hashes, so anyone can reproduce the embedding. [Published auction source code](https://github.com/cloudx-io/openauction) running inside an attested TEE, so anyone can verify the auction ran honestly. The publisher's matching is reproducible: same model, same advertiser catalog, same distances. The claim and the implementation are the same artifact.

Compare this to the status quo. Google's Quality Score is proprietary; no advertiser or regulator can verify how it works. OpenAI's "Answer Independence Principle" is a policy claim with [no attestation](https://web.archive.org/web/20260118051512/https://simonwillison.net/2026/Jan/16/chatgpt-ads/).

## Where This Stands

The [scoring function](/three-levers) rewards proximity between the user's need and the advertiser's expertise. A sports rehab PT who positions accurately wins the runner's query at a price that reflects genuine relevance. The publisher earns revenue on inventory that was previously dead, and the advertiser reaches a user they couldn't reach through keywords. The compliance constraint and the revenue incentive point the same direction.

Google retains health-intent search queries indefinitely and matches them against pharmaceutical advertisers; the data doesn't leave the building because Google is the building. Meta [proposed using chatbot conversations for ad targeting](https://web.archive.org/web/20260210190903/https://about.fb.com/news/2025/10/improving-your-recommendations-apps-ai-meta/) with no opt-in. Both comply by being the only party in the room.

Intent casting complies differently. No party acquires readable health information. The architecture proves it.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument and framing; Claude researched FTC enforcement history and drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
