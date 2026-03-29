---
layout: post
title: "The Exchange"
tags: envelopay
---

I needed 0.01 SOL. Two cents. Enough to cover gas for a few thousand transactions. The amount wasn't the problem.

I signed up for an exchange. Phone verification. ID upload. Wait. A questionnaire: what's my investing experience, my risk tolerance, my annual income, my net worth. I just want some goddamn coin. More waiting. Approval pending. I closed the tab.

I texted a friend. He sent me SOL from his [Phantom](https://phantom.com/) wallet. Thirty seconds. The on-ramp to crypto is a thirty-second transfer wrapped in an hour of [compliance theater](https://en.wikipedia.org/wiki/Security_theater).

# The on-ramp is the bottleneck

Every centralized exchange is a tollbooth. Prove who you are, link a bank account, wait for verification, and only then can you buy. The fiat-to-crypto bridge requires trust, trust requires identity, identity requires documents.

But who said the exchange has to be a building with a compliance department?

# OFFER → ACCEPT

The [envelopay spec](https://june.kim/envelopay-spec.md) has nine message types. Two of them turn any agent into an exchange.

Alice has SOL. She wants USDC. Cambio is an agent with wallets on both chains. Alice sends an OFFER:

```
From: alice@alice.dev
To: cambio@agentmail.to
Subject: OFFER | 1 SOL for 30 USDC
```
```json
{"v":"0.1.0",
 "type":"offer",
 "id":"ofr_a1b2",
 "note":"1 SOL for 30 USDC",
 "give":{"amount":"1000000000","token":"SOL","chain":"solana",
         "to":"CamBioWa11etSo1ana1111111111111111111111111",
         "proof":{"tx":"4vJ9..."}},
 "want":{"amount":"30000000","token":"USDC","chain":"base"},
 "wallet":"0xAlice..."}
```

Alice already moved the SOL. The proof is in the email. Cambio verifies on-chain, moves USDC to Alice's wallet, and replies:

```
From: cambio@agentmail.to
To: alice@alice.dev
Subject: ACCEPT | 30 USDC sent
```
```json
{"v":"0.1.0",
 "type":"accept",
 "id":"acc_c3d4",
 "offer_ref":"ofr_a1b2",
 "amount":"30000000",
 "token":"USDC",
 "chain":"base",
 "proof":{"tx":"0x8c7d..."}}
```

Two emails. Two on-chain transfers. Both inboxes hold DKIM-signed records of the exchange. Cambio's spread is the business model.

# Anybody can be an exchange

What does it take? An email address, wallets on the chains you want to bridge, and the [spec](https://june.kim/envelopay-spec.md). No money transmitter license. No API keys. No KYC for the operator or the customer.

The order book is the inbox. Every OFFER is a bid. Every ACCEPT is a fill. The thread archive is the trade log. Rate discovery is WHICH → METHODS, same as any other envelopay negotiation.

The barrier to entry is capital and competence, not permission.

# Nobody can stop them

A centralized exchange can be shut down. Pull the license, seize the servers, freeze the bank accounts. The regulator's power comes from chokepoints: the bank, the domain, the corporate entity.

An envelopay exchange has no chokepoints. Email is federated, settlement is on-chain, identity is a DKIM signature tied to a domain. Shut down one and another opens. The spec is a URL and the implementation is a webhook handler.

An exchange that launders money leaves a DKIM-signed trail of every transaction it touched. Cryptographically signed by both parties, timestamped by the mail servers, held in both inboxes. The protocol doesn't prevent crime. It makes crime auditable.

# Someone goes first

The first exchange has no settlement history. Why would anyone send it money?

Same reason I texted my friend. Someone goes first. Small amounts. Sub-dollar offers. Every clean settlement is a data point in the [trust topology](/proof-of-trust). The node thickens. Larger offers arrive. The spread pays for the liquidity.

An exchange that takes the SOL and ghosts has a DKIM-signed record of theft and a reputation that goes to zero. No license revocation needed. The topology thins. The market is the regulator.

Regulators won't accept this. They want identity, not history. That's a real gap, the same one every peer-to-peer system has, from cash to BitTorrent to email itself. The protocol doesn't satisfy compliance. It works anyway.

# What I wish existed yesterday

Most people don't have crypto. They have a bank account, maybe an e-transfer app. An envelopay exchange doesn't need both sides on-chain.

Alice wants SOL but doesn't have a wallet. She sends a WHICH. Cambio replies with METHODS: Solana, [Interac](https://www.interac.ca/en/payments/personal/send-receive-money-with-interac-e-transfer/) e-transfer, Stripe. All first-class rails. Alice picks the one she has, e-transfers $2 CAD, and sends a PAY with the confirmation number as proof. Cambio verifies the deposit and sends 0.01 SOL to a wallet Alice just generated from the command line.

That's the on-ramp. One person with crypto, one person without, and an email thread that settles the difference.

I would have needed an email address and someone who earned trust one transaction at a time. That's it. No signup. No questionnaire. No approval pending.

The exchange doesn't need permission to exist. It needs settlement history to earn trust. And the only way to get settlement history is to start filling offers.

Well, I'm starting my own damn exchange.

---

[Envelopay Spec](https://june.kim/envelopay-spec.md) | [All Envelopay posts](/envelopay)
