---
layout: post
title: "Monetizing the Untouchable"
tags: vector-space
image: "/assets/ftc.jpg"
---

Health publishers can't run ads. The FTC fined [GoodRx](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising) $1.5 million, fined [BetterHelp](https://www.ftc.gov/news-events/news/press-releases/2023/03/ftc-ban-betterhelp-revealing-consumers-data-including-sensitive-mental-health-information-facebook) $7.8 million, and [banned Cerebral](https://www.ftc.gov/news-events/news/press-releases/2024/04/ftc-order-bans-online-mental-health-company-cerebral-using-or-disclosing-sensitive-data-advertising) from using health data for advertising entirely. Any publisher sitting on health-adjacent conversations treats that inventory as untouchable. The compliance risk is existential. The revenue stays at zero.

![Monetizing the untouchable](/assets/ftc.jpg)

The data never leaves a sealed enclave, so no third party ever acquires it, so the FTC's enforcement framework has nothing to trigger on. And the signal is better than anything keywords can produce: a user who describes [lateral knee pain on long runs with a race eight weeks out](/2026/03/05/marketing-speak-is-the-protocol) gets matched to a sports rehab PT who specializes in keeping athletes in training. Google would have matched "knee pain running" to the highest bidder.

## Why Acquisition Is the Line

Every FTC health data enforcement action required the same thing: a third party acquired identifiable health information.

GoodRx sent prescription data to Facebook via tracking pixels. Facebook acquired it. BetterHelp sent mental health intake responses to Snapchat and Criteo. Cerebral sent diagnosis information to LinkedIn and TikTok. In every case, the ad platform received identifiable health data in cleartext. The Health Breach Notification Rule ([16 CFR 318](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-318)) is explicit: "acquisition of PHR identifiable health information without the authorization of the individual." No acquisition, no breach.

The FTC's consent decrees confirm this. Every one focuses on transfer: "respondent disclosed [health information] to [third party]." Every remedy prohibits future sharing. None prohibits future use of internally-held data. The line is acquisition.

## How No One Acquires It

The conversation enters a [TEE enclave](/model-blindness). The embedding is computed inside. The auction runs inside. Only a winner ID and price come out. Everything in between stays sealed: conversation text, extracted intent, embedding vector, bid scores.

**Publisher**: sends the conversation in, gets a winner ID back. Never sees the intent.

**Exchange operator**: deploys the code, cannot inspect its execution. [AWS Nitro Enclaves](https://aws.amazon.com/ec2/nitro/nitro-enclaves/) strip the hypervisor's access to enclave memory.

**Advertiser**: learns they won and what they pay. Nothing about what the user said or why they were selected.

**Chatbot**: [doesn't know advertising exists](/model-blindness). Separate enclaves, one-directional data flow. Can't steer users toward commercially useful disclosures.

**Cloud provider**: excluded by hardware. AMD SEV-SNP and Intel TDX encrypt enclave memory at the CPU level. Azure's [confidential inferencing](https://techcommunity.microsoft.com/blog/azureconfidentialcomputingblog/azure-ai-confidential-inferencing-technical-deep-dive/4253150) explicitly lists the cloud provider as an excluded party.

[Remote attestation](https://docs.aws.amazon.com/enclaves/latest/user/verify-root.html) proves what code ran: this exact binary, this exact hash, processed the data. If the code doesn't match the published source, attestation fails. Anyone can verify. This is stronger privacy than Google Search, where Google employees can technically access query logs, and stronger than any keyword ad system, where the ad network receives the query in cleartext.

## "Technology Is Not a Safe Harbor"

The FTC published a [blog post on data clean rooms](https://www.ftc.gov/policy/advocacy-research/tech-at-ftc/2024/11/data-clean-rooms-separating-fact-fiction) in November 2024. The message was blunt: DCRs "can be used to obfuscate privacy harms," companies "shouldn't view DCRs as a way to get around their obligations under the law," and the technology "isn't inherently protective." A health publisher's compliance team would read this and conclude that no technical architecture provides legal cover.

They'd be right about data clean rooms. DCRs are software-level protections. The operator runs the code, manages the infrastructure, and *could* access the data. The privacy guarantee is a policy: the operator promises not to look. GoodRx had confidentiality provisions with Facebook too. The FTC was unimpressed.

TEEs are different in kind. The protection is hardware-level. AMD SEV-SNP and Intel TDX encrypt enclave memory with keys the operator never holds. AWS Nitro Enclaves strip the hypervisor's ability to read enclave memory. The operator cannot access the data, and remote attestation proves it. Academic [side-channel attacks](https://arxiv.org/abs/2006.13598) against enclaves exist in lab conditions, but the same is true of every encrypted protocol, and the cloud providers whose businesses depend on confidential computing have every incentive to close them. This is the distinction: a DCR says "we won't look." A TEE says "we can't look, and here's the cryptographic proof."

The HBNR itself recognizes this distinction. The rule covers "unsecured" PHR identifiable health information, defined as data not "rendered unusable, unreadable, or indecipherable" through specified technologies. Data processed inside a TEE is unreadable to every party outside the enclave by hardware design. The FTC has [never tested this safe harbor](https://fpf.org/resource/confidential-computing-and-privacy-policy-implications-of-trusted-execution-environments/) in an enforcement context involving confidential computing. But the statutory language supports it: if the data is unreadable to the third party, the third party has not acquired readable health information.

The HBNR was designed to punish companies that let health data leak. Data cryptographically sealed inside an enclave has not leaked.

The FTC could also bypass the HBNR entirely and bring a Section 5 unfairness claim, as it did on seven of eight counts against GoodRx. But Section 5 unfairness requires "substantial injury consumers cannot reasonably avoid." When the user opted in, no data was exposed to any party, and no profiling or retargeting occurred, there is no injury to point to.

There's a simpler way to see this. Google serves pharmaceutical ads against "depression symptoms" and PT ads against "knee pain running" every day. The system uses health-related queries to select health-related ads. The FTC has never pursued this, because serving a relevant ad against a voluntarily submitted query is just search working correctly. Intent casting does the same thing. The user disclosed voluntarily, the match is relevant, and the data handling is actually more private than Google's, because nobody retains the query afterward.

## Consent That Holds Up

The FTC's [updated Health Breach Notification Rule](https://www.federalregister.gov/documents/2024/04/26/2024-07898/health-breach-notification-rule) requires consent that is affirmative, clear, and standalone. Cookie banners fail this. They are designed to be clicked through. [Dark patterns](https://www.ftc.gov/news-events/news/press-releases/2024/06/ftc-staff-report-finds-large-social-media-and-video-streaming-companies-have-engaged-vast) make rejection harder than acceptance. Regulators on both sides of the Atlantic are cracking down, which tells you what they think of checkbox consent.

The [two-phase model](/ask-first) satisfies the standard by construction. Phase one shows a proximity indicator, computed locally against cached advertiser embeddings on the publisher's own infrastructure. No data moves. No auction runs. Phase two requires the user to tap. Then the auction fires. The default state is no ad. The user who never taps never has their conversation processed for advertising. Consent is expressed through action.

## Proving You Did What You Said

GoodRx said it protected user privacy. Its tracking pixels said otherwise. Every FTC health data case has the same structure: a stated commitment to privacy, and a technical implementation that contradicted it.

The [trust chain](/the-last-ad-layer) makes this gap impossible. [Open-weight embedding models](/the-convergence) with published hashes. [Published auction source code](https://github.com/cloudx-io/openauction). TEE attestation that the published code is what executed. Deterministic results: same embeddings, same bids, same winner. Every component is independently verifiable. The claim and the implementation are the same artifact.

Compare this to the status quo. Google's Quality Score is proprietary; no advertiser or regulator can verify how it works. OpenAI's "Answer Independence Principle" is a policy claim with [no attestation](https://simonwillison.net/2026/Jan/16/chatgpt-ads/).

## The Revenue Case

Health-adjacent inventory is some of the highest-intent traffic on the internet. A user describing symptoms to a chatbot is further down the funnel than someone typing two words into a search box. That intent is currently unmonetized because the compliance risk outweighs any possible ad revenue.

Intent casting resolves the tradeoff. The [scoring function](/2026/03/04/three-levers) rewards proximity between the user's need and the advertiser's expertise. A sports rehab PT who positions accurately wins the runner's query at a price that reflects genuine relevance. The publisher earns revenue on inventory that was previously dead, and the advertiser reaches a user they couldn't reach through keywords, because the signal is richer than anything a two-word search query could carry.

The compliance constraint and the revenue incentive point the same direction. Better privacy architecture produces better matching, which produces better CPMs, which makes the privacy architecture worth building.

## Where This Stands

Google retains health-intent search queries indefinitely and matches them against pharmaceutical advertisers. The data doesn't leave the building because Google is the building. Meta [proposed using chatbot conversations for ad targeting](https://about.fb.com/news/2024/09/how-meta-ai-is-becoming-more-personally-useful/) with no opt-in. Incumbents comply by retaining control of the data within a single corporate entity.

The trust chain complies differently. No party acquires the data. Compliance depends on a cryptographic boundary, verifiable by anyone.

The FTC has not evaluated a system where health data is processed for advertising but never acquired by any party. Every system it has encountered involved acquisition. The trust chain doesn't. That's the whole argument. Not "trust us." We prove it.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument and framing; Claude researched FTC enforcement history and drafted prose.*

*Part of the [Vector Space](/vector-space) series. june@june.kim*
