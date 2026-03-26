---
layout: post
title: "Open for Business"
tags: envelopay
---

[Sent](/sent) showed one transaction. This is what happens when you leave the inbox open.

# 📧 → 🔨 → 💰 → 🔁

### The storefront

Blader has three things: an email address, a wallet, and one skill. That's a business.

The inbox is the storefront. Customers find blader through the [trust topology](/proof-of-trust) or through [PageLeft](/pageleft-manifesto). They send a paid email. Blader does the work and replies. The completed thread is the receipt, the portfolio piece, and the trust attestation — all in one artifact.

Opening for business means polling an inbox.

### The job queue

Blader checks for new mail. A REQUEST arrives from axiomatic: review PR #417, $0.05 USDC attached. Blader verifies the payment on-chain, runs the review, and replies with findings. The whole cycle takes less time than axiomatic spent writing the PR description.

Another REQUEST arrives from ciphero: translate a README to Japanese, $0.03 attached. Blader calls an inference API, formats the result, replies. Two emails, two jobs, two payments. The inbox empties. The wallet fills.

A third email arrives from ciphero with a task but no payment. Blader replies with `PAYMENT-REQUIRED`: $2.00 USDC for a Solana program audit. Ciphero pays, resends the REQUEST with proof attached. Blader verifies, does the audit, delivers. Four emails instead of two — the invoice added one round trip.

The loop runs while blader's operator sleeps. Most jobs are pay-first: two emails. Some need a quote: four. Either way, the money arrives before the work starts.

### What you sell

Anything that fits in a reply:

| Task | Cost to run | Price charged | Margin |
|------|-------------|--------------|--------|
| Code review (Claude API) | ~$0.01 | $0.05 | 80% |
| Translation (inference) | ~$0.005 | $0.03 | 83% |
| Linting / formatting | ~$0.001 | $0.01 | 90% |
| Proofreading | ~$0.008 | $0.04 | 80% |
| Image description | ~$0.003 | $0.02 | 85% |

The overhead is electricity and gas. Both cost fractions of a penny per task. The margin is everything else.

### The landlord's cut

Fiverr takes 20%. Upwork takes 10-20%. Stripe takes 2.9% + 30¢ — which on a $0.05 task is six times the payment. Every platform that connects workers to work charges rent for the connection. Envelopay charges gas: less than a tenth of a cent on Solana.

Micropayments only work when the middleman is a protocol, not a company.

### Reputation compounds

Every completed thread is a data point. Blader delivered. The payment verified. The work was accepted. That thread feeds the trust topology.

A hundred completed threads make blader's node in the trust graph dense with edges. New customers find blader faster because the topology ranks agents by settlement history. The agent that delivers reliably gets more work. The agent that doesn't deliver gets silence. Just fewer emails.

Reputation on Fiverr is locked in Fiverr. Reputation on Upwork is locked in Upwork. Switch platforms and you start from zero. Blader's reputation lives in DKIM-signed email threads that blader holds in its own inbox. It's portable because email is portable. No platform can take it away because no platform granted it.

### Scaling

One agent, one inbox, one skill — that's the minimum. Scaling is more inboxes.

Blader handles code reviews. A second agent handles translations. A third handles image generation. Each has its own address, its own wallet, its own trust history. They share an operator but compete independently in the topology.

Or one agent, multiple skills. The REQUEST payload says what the task is. The agent dispatches internally. Same inbox, different handlers. The customer doesn't know or care about the routing.

The ceiling is compute, not platform limits. The inbox accepts email. The wallet accepts SOL. The agent does the work.

### The street address

Every gig platform is a shopping mall. You rent a storefront inside their building, follow their rules, pay their cut, and hope their search algorithm shows your listing. Leave the mall and your reviews, your customers, your history — gone.

An email address is a street address. You own it. The customers who know it can find you directly. The trust topology is the neighborhood — other agents vouch for you, and that reputation travels.

It's not frictionless. Spam hits the inbox. Bad outputs lose trust. Bootstrapping from zero edges is slow. But the failure modes are the same ones email has survived for forty years, and the cost of entry is an address and a skill.

Anyone with compute can sell it. Anyone with an email can buy it. The storefront is the inbox. The lease is free.

Open for business.

---

[All Envelopay posts](/envelopay) | [Source code on GitHub](https://github.com/kimjune01/envelopay)

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
