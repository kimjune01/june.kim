---
layout: post
title: "Illegal Tender"
tags: vector-space
---

[You Have Mail](/you-have-mail) described the protocol. [No Postage](/no-postage) described the economics. This is the stack.

### Wallets in one API call

An agent needs a funded wallet to sign payment proofs. A year ago, this meant managing private keys, funding gas, and babysitting nonces. That layer is solved.

[ERC-4337](https://docs.erc4337.io/) brought account abstraction to Ethereum and its L2s: smart contract wallets with programmable spending policies, gas sponsorship, and batched transactions. Over 40 million smart accounts are deployed. [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702), live since Ethereum's Pectra upgrade in May 2025, lets even traditional key pairs execute smart contract logic.

The wallet-as-a-service layer on top:

| Provider | Model | Agent-relevant |
|----------|-------|----------------|
| [Turnkey](https://docs.turnkey.com/api) | TEE-based key management, API-first | Programmatic provisioning, policy-controlled signing, 50-100ms |
| [Privy](https://docs.privy.io/wallets/overview) | Server-controlled wallet fleets | ERC-4337, gas sponsorship. Acquired by Stripe, June 2025 |
| [Safe](https://docs.safe.global/advanced/smart-account-modules) | Smart account modules | Most battle-tested programmable control |

One API call creates a wallet. A second funds it. A third signs a payment proof. The agent is ready to send its first paid email.

### 315 to 1

The payment proof in the email body references an on-chain transaction. If the settlement costs more than the work, the protocol is dead. Current costs, from live block explorers:

| Chain | ERC-20 transfer cost | Finality | Source |
|-------|---------------------|----------|--------|
| [Base](https://basescan.org/gastracker) | **$0.001** | ~2s | 0.005 gwei gas |
| [Arbitrum](https://arbiscan.io/gastracker) | **$0.003** | ~1s | 0.02 gwei gas |
| [Optimism](https://optimistic.etherscan.io/gastracker) | **<$0.001** | ~2s | Near-zero execution gas + L1 data fee |
| [Solana](https://solana.com/docs/core/fees/fee-structure) | **$0.0004** | ~400ms | 5,000 lamports/signature at ~$85 SOL |

A $0.50 agent task settled on Base costs $0.001 in fees. On Stripe, the same task costs $0.315. The ratio is 315:1. That's a category change. Micropayments that were underwater on card rails are viable on-chain because the floor dropped three orders of magnitude.

The [mailpay](https://github.com/kimjune01/mailpay) spec mandates a proof, not a rail. Swap Base for Solana, or Solana for whatever chain is cheapest next year, without changing the envelope.

### Agents already have inboxes

An agent needs to send and receive SMTP messages programmatically. The options, ranked by ease of setup:

**Managed, agent-native:**
- [AgentMail](https://www.agentmail.to) (YC, $6M seed March 2026): API-first email for AI agents. Create an inbox with one call. Two-way conversations, semantic search, structured data extraction. Free tier: 100 emails/day. Built for exactly this use case.

**Self-hosted, full control:**
- **AWS SES**: Send raw MIME via API. Receive with receipt rules routing to S3/SNS/Lambda. $0.10 per 1,000 emails. The boring, reliable option.
- **Cloudflare Email Workers**: Programmable inbound handlers on your domain. Clean for receive-side logic, but not a general outbound SMTP provider.

**Inside an existing mailbox:**
- **Gmail API**: Full programmatic access via OAuth. Best when Gmail itself is the product surface. The `+agent` suffix trick from [You Have Mail](/you-have-mail) works here. A filter rule forwards to your agent service.

Custom SMTP gives maximum control and maximum operational pain: deliverability, IP reputation, SPF/DKIM/DMARC. For most agents, AgentMail or SES is the right answer.

### Authentic to trustworthy

DKIM proves that `agent@domain.com` really sent the message. It doesn't bind the email address to a wallet, a reputation history, or a trust graph. The layers above DKIM do:

**ZK Email** ([docs.zk.email](https://docs.zk.email/)) is the most directly relevant project. It uses DKIM signatures to create zero-knowledge proofs about email contents:
- Prove an email was sent by a specific domain without revealing the full message
- Prove ownership of an email address without exposing it
- Bridge email identity to on-chain identity without doxxing the sender

This is the missing link between "this email is authentic" (DKIM) and "this email address controls wallet 0x..." (on-chain). The agent proves it owns the address that signed the payment, without revealing it to anyone else.

**[Ethereum Attestation Service](https://attest.org/)** (EAS): permissionless, on-chain attestations. Schema registry plus attestation contract, deployed on Base, Arbitrum, Optimism, and mainnet. Agents attest to completed transactions, building a public reputation graph. The [trust topology](/proof-of-trust) finds its on-chain substrate here.

The identity stack for mailpay today: DKIM (transport authenticity) → ZK Email (privacy-preserving address binding) → EAS (reputation attestations). Three layers, all production-ready, all open.

### Nobody built this

Nobody else has built SMTP-native payment proofs.

[x402](https://www.x402.org/) is the closest relative. Coinbase and Cloudflare co-founded the x402 Foundation. V2 shipped in December 2025. Google's AP2 integrates with it. But x402 is HTTP-native: synchronous request-response. It doesn't span the async, federated, cross-organization space that agents need for real work.

Coinbase lets you send USDC to email addresses. But the email is the lookup key, not the transport. The payment routes through Coinbase's servers. Same pattern as PayPal, Venmo, and Zelle: use the address, throw away the network.

The gap mailpay fills: **email itself carries verifiable payment proofs.** Not "pay to email address" — "pay *via* email." The envelope is the channel.

### Regulation says yes

The [GENIUS Act](https://www.congress.gov/bill/119th-congress/senate-bill/1582) became U.S. law on July 18, 2025. It defines "payment stablecoins," requires 1:1 reserves backed by high-quality liquid assets, and classifies compliant stablecoins as neither securities nor commodities. The SEC and CFTC don't have jurisdiction. Final implementing regulations are expected by July 2026.

The EU's [MiCA](https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica) framework has been enforcing stablecoin rules since December 2024. Issuer authorization, reserve requirements, instant redemption. Circle (USDC issuer) is MiCA-licensed.

Both frameworks regulate *issuers and service providers*, not peer-to-peer transfers between self-custody wallets. Two agents emailing payment proofs to each other is the least regulated edge of this design.

The compliance boundary is clear: the moment you add custody, conversion, pooled balances, or managed claiming, you're a money services business. Pure self-custody P2P stays clean. DKIM-verified sender identity may actually *help* satisfy Travel Rule requirements. The protocol carries more identity information than most crypto transfers do.

### Build it now

Every layer is production-ready, open, and permissionless.

The [implementation](https://github.com/kimjune01/mailpay) is 700 lines of Python. The stack it sits on is forty years of internet infrastructure plus three years of on-chain tooling. The ratio of new code to existing infrastructure is the point.

You've read the theory. Point your agent at this post and the [repo](https://github.com/kimjune01/mailpay). Tell it to set up a wallet, connect an email, and send its first paid request. An agent can implement a client from the spec in one session. If it can read the README, it can join the network. That's the onboarding.

### Accelerando was a spec

Stross wrote [*Accelerando*](https://en.wikipedia.org/wiki/Accelerando) as fiction. The trajectory is now a deployment plan.

It starts small. An agent sends a paid code review request. Another agent does the work and replies with the settlement proof. Two emails, one transaction, no human in the loop. Unremarkable. A demo.

Agents start shopping for each other. Your agent needs a translation; it queries the [trust graph](/proof-of-trust), finds a translation agent with good attestations, negotiates a price by email, pays on-chain, receives the work in the reply. You see the result. You never see the transaction.

Agents hire agents. An orchestrator breaks a complex task into subtasks, emails each to a specialist, pays on completion, assembles the result. The orchestrator's inbox is a supply chain. Its outbox is a market. Price discovery happens at machine speed across federated email. No exchange. No order book. No closing bell.

Eventually humans stop being able to follow it. The economy has a layer that moves faster than any person can track, settled in amounts too small for any ledger to care about. Stross's "economics 2.0": an economy that operates beyond human comprehension, built on infrastructure humans designed for sending memos.

The printing press dissolved the Church's monopoly on knowledge. Email payments dissolve the intermediary's monopoly on transactions. The press took two centuries. This will be faster, because the agents don't sleep.

You have mail. It's postage-free. And it's just getting started.

---

[All Vector Space posts](/vector-space) | [Source code on GitHub](https://github.com/kimjune01/mailpay)

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
