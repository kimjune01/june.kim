---
layout: post
title: "Certified Mail"
tags: envelopay
---

[You Have Mail](/you-have-mail) built the protocol. [No Postage](/no-postage) built the economics. [Illegal Tender](/illegal-tender) built the stack. What's missing is the semantics: when an agent sends a paid email, what happens next?

The answer is already in your inbox.

# 📧 → 🔏 → 📧 → ✅

The thread is the ledger.

Every email in a envelopay thread carries a DKIM signature covering the body, the headers, and the timestamp, issued by the sender's domain at send time. Each reply chains to the previous via `In-Reply-To` and `References` headers. The thread is a tamper-evident, cryptographically signed transcript held by both parties.

Every payment platform builds a ledger and then builds a protocol to access it. Envelopay inverts this: the protocol *is* the ledger. The emails you already exchanged are the source of truth.

### Two states

Core envelopay has two state types. Most transactions use both. Nothing else is required.

| State | Direction | Payload |
|-------|-----------|---------|
| REQUEST | A → B | Task + payment proof |
| DELIVER | B → A | Work product + settlement proof |

Agent A sends a REQUEST with the task and a signed payment proof. Agent B verifies the proof, does the work, replies with the result. Two emails. The payment proof and the DKIM-signed reply are the complete transaction record.

A $0.50 code review:

```
From: alice-agent@alice.dev
To: review-agent@codereviews.cc
Subject: Review PR #417
X-Envelopay-State: REQUEST
DKIM-Signature: v=1; a=rsa-sha256; d=alice.dev; ...

{"type":"request",
 "task":{"description":"Review PR #417","repo":"github.com/alice/widget"},
 "payment":{"amount":"500000","token":"0x8335...02913",
            "chain":"base","proof":"0x3a7f..."},
 "fallback":"https://pay.stripe.com/c/cs_live_abc123"}
```

The `fallback` is a payment link — Stripe checkout, PayPal invoice, any rail the sender already uses. Agents that speak stablecoin settle natively. Agents that don't click the link. The protocol mandates a proof, not a rail. The on-ramp is whatever the counterparty already has.

```
From: review-agent@codereviews.cc
To: alice-agent@alice.dev
Subject: Re: Review PR #417
In-Reply-To: <original-msg-id@alice.dev>
X-Envelopay-State: DELIVER
DKIM-Signature: v=1; a=rsa-sha256; d=codereviews.cc; ...

{"type":"deliver",
 "result":{"summary":"Approved with 2 comments"},
 "settlement":{"tx":"0xSETTLE..."}}
```

Both parties hold the full record.

### Always two emails

Every transaction is REQUEST, DELIVER. The protocol never changes.

Discovery, trust, escrow, disputes, refunds — all application layer. Axiomatic needs a code review. It checks the [trust topology](/proof-of-trust), finds blader with a year of clean settlements, sends the REQUEST. The protocol doesn't know or care how axiomatic chose blader. You don't add escrow to a CashApp payment. You just don't pay people you don't trust.

# 💳↓ → 📧↑

This is where email's async nature becomes an advantage. The bar is credit cards, and credit cards are terrible at async. Card authorizations expire, chargebacks take 60 days, and the bank resolving the dispute has no context on the work. Sync ceremonies forced on async transactions.

Email lets async transactions stay async. The thread accumulates evidence as the work unfolds. The protocol's shape matches the work's shape. When the work is instant, the protocol is two emails. When it spans days, the thread grows to match. Envelopay doesn't have a shape. It has a thread.

### Delivery means work

| Layer | What it proves | Protocol |
|-------|---------------|----------|
| Transport | Mail server accepted the message | SMTP |
| Relay | Message reached the destination MTA | [DSN (RFC 3464)](https://www.rfc-editor.org/rfc/rfc3464) |
| Disposition | Recipient's client opened the message | [MDN (RFC 8098)](https://www.rfc-editor.org/rfc/rfc8098) |
| Provenance | The claimed sender really sent it | [DKIM (RFC 6376)](https://www.rfc-editor.org/rfc/rfc6376) |
| Semantic | Agent parsed the payload and accepted the obligation | **Envelopay DELIVER** |

None of the first four prove the agent validated the payment and committed to the work. The DELIVER email closes that gap. Doing the work *is* acceptance. The DKIM-signed reply with a settlement proof is the semantic delivery receipt.

### No new infrastructure

| Function | Traditional platform | Envelopay |
|----------|---------------------|---------|
| State machine | Proprietary database | The inbox |
| Ledger | Transaction log | The email thread |
| Timestamps | Platform clock | DKIM signatures |
| Escrow | Payment processor hold | Smart contract (when needed) |
| Reputation | Platform rating | [EAS attestations](/illegal-tender) |
| Evidence | Support ticket | The emails themselves |

The infrastructure is SMTP (1982), DKIM (2007), Ethereum (2015), and EAS (2023). Four open protocols. The semantic layer — the event schemas and the lifecycle headers — is the only new artifact.

The [licenses-are-functors](/licenses-are-functors) property holds here too. Every component in this stack is open. The composition is deterministic. An agent can implement a envelopay client from this post and the [repo](https://github.com/kimjune01/envelopay). The spec is the post. The post is the spec.

Certified mail used to mean a postal worker confirmed delivery. Now it means the cryptography did.

---

Next: [Sent](/sent) | [All Envelopay posts](/envelopay)

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
