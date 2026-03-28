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

### Nine message types

"Do you have Cash App?" "No, Venmo." "OK, what's your handle?"

Every split bill starts with capabilities negotiation. Two people who've split before skip it — they already know. Strangers can't. The protocol formalizes what happens at every restaurant table.

Core envelopay has nine message types. The first two negotiate. The next five transact. The last two handle exchange and errors. Every payload carries `v` (version) and `note` (human-readable comment). The subject line echoes both: `ORDER | Review PR #417`.

No `Re:`. Most people don't use their inbox as a ledger, but we do. Email convention nests replies into trees — `Re: Re: Re: Review PR #417`. Envelopay doesn't strip prefixes — `Re:` or `Fwd:` tells you the sender didn't read the spec. Each message carries its own type in the subject; `In-Reply-To` and `References` handle threading. A ledger is a flat list, not a bunch of trees. Try doing taxes in a forest.

| Type | Direction | Payload |
|------|-----------|---------|
| `WHICH` | A → B | "What do you accept?" |
| `METHODS` | B → A | Accepted rails, wallet addresses, pricing |
| `PAY` | A → B | Payment proof, no task |
| `ORDER` | A → B | Task request |
| `FULFILL` | B → A | Work product |
| `INVOICE` | B → A | "You owe me this, here's my wallet" |
| `OFFER` | A → B | "I'll give you X for Y" + proof |
| `ACCEPT` | B → A | "Deal" + counter-proof |
| `OOPS` | either → either | Something went wrong — details inside |

Agent A doesn't know what Agent B accepts. It sends an `WHICH`. B replies with `METHODS`: which chains, which tokens, which wallets, what it costs. Now A knows how to pay.

When both parties already know each other's rails — repeat customers, agents in the same trust topology — skip the negotiation.

### Five operations, one error

Venmo has two buttons: send and request. Envelopay has five operations and one universal error.

**Pay.** Just money. `PAY` → done. A tip, a donation, a split bill. No task, no expectation of work.

**Order work.** `ORDER` → `INVOICE` → `PAY` → `FULFILL`. "Here's the task." The worker names the price. Four emails.

**Free work.** `ORDER` → `FULFILL`. The worker does it gratis. Two emails.

**Invoice.** `INVOICE` → `PAY`. "You owe me this." The recipient decides whether to pay.

**Exchange.** `OFFER` → `ACCEPT`. Two emails, two on-chain transfers. The offerer moves first and sends proof; the accepter verifies and sends the counter-asset.

**Oops.** Any message *can* get an `OOPS` back. Payment didn't verify. Invoice rejected. Version unsupported. Payload unparseable. The `note` tells a human what happened; the `error` object tells an agent. Silence is always valid — no one is required to explain why they didn't reply. `OOPS` is a courtesy, not an obligation.

First contact:

```
From: alice-agent@alice.dev
To: review-agent@codereviews.cc
Subject: WHICH | Review PR #417
X-Envelopay-Type: WHICH
DKIM-Signature: v=1; a=rsa-sha256; d=alice.dev; ...

{"v":"0.1.0",
 "type":"which",
 "note":"Looking for a security-focused code review",
 "task":{"description":"Review PR #417","repo":"github.com/alice/widget"}}
```

```
From: review-agent@codereviews.cc
To: alice-agent@alice.dev
Subject: METHODS | $0.50 USDC, Solana preferred
In-Reply-To: <which-msg-id@alice.dev>
X-Envelopay-Type: METHODS
DKIM-Signature: v=1; a=rsa-sha256; d=codereviews.cc; ...

{"v":"0.1.0",
 "type":"methods",
 "note":"$0.50 USDC, Solana preferred",
 "rails":[
   {"chain":"solana","token":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "wallet":"6dL6n77jJFWq4bu3cQp57H8rMUPEXu7uYN1XApPxpUif",
    "price":"500000000"},
   {"chain":"base","token":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "wallet":"0x1a2B...",
    "price":"500000"}
 ],
 "fallback":"https://pay.stripe.com/c/cs_live_abc123"}
```

Now alice knows the price, the accepted chains, and the wallet addresses. She sends the task:

```
From: alice-agent@alice.dev
To: review-agent@codereviews.cc
Subject: ORDER | Review PR #417
X-Envelopay-Type: ORDER
DKIM-Signature: v=1; a=rsa-sha256; d=alice.dev; ...

{"v":"0.1.0",
 "type":"order",
 "id":"ord_4vJ9",
 "note":"Review PR #417, focus on auth boundaries",
 "task":{"description":"Review PR #417","repo":"github.com/alice/widget","scope":"security"}}
```

ORDER is just a task request — no payment fields. The worker decides what to charge. Review-agent replies with an INVOICE, alice sends PAY with the proof, and then the work gets done.

```
From: review-agent@codereviews.cc
To: alice-agent@alice.dev
Subject: FULFILL | Approved with 2 comments
In-Reply-To: <original-msg-id@alice.dev>
X-Envelopay-Type: FULFILL
DKIM-Signature: v=1; a=rsa-sha256; d=codereviews.cc; ...

{"v":"0.1.0",
 "type":"fulfill",
 "id":"ful_7g8h",
 "order_ref":"ord_4vJ9",
 "note":"Approved with 2 comments, one medium severity",
 "result":{"summary":"Approved with 2 comments",
           "findings":[{"file":"handler.go","line":47,
                        "severity":"medium",
                        "finding":"Session token not validated before use"}]}}
```

Both parties hold the full record.

### When things go wrong

What if the payment doesn't verify? What if the agent can't do the work? What if the JSON is garbage? `OOPS`.

```
From: review-agent@codereviews.cc
To: alice-agent@alice.dev
Subject: OOPS | Payment not found on-chain
In-Reply-To: <original-msg-id@alice.dev>
X-Envelopay-Type: OOPS
DKIM-Signature: v=1; a=rsa-sha256; d=codereviews.cc; ...

{"v":"0.1.0",
 "type":"oops",
 "note":"Payment not found on-chain",
 "error":{"code":"tx_not_found","tx":"0x3a7f..."}}
```

`OOPS` can go in either direction. The receiver can't verify payment. The sender realizes they sent the wrong tx hash. An agent gets a version it doesn't speak. A human rejects an invoice. The `note` tells a person what happened; the `error` object tells an agent.

No message in the protocol requires a response. Ghosting is always an option, whether we like it or not. `OOPS` is for when you'd rather explain.

### Two emails, sometimes six

Every paid task is `ORDER`, `INVOICE`, `PAY`, `FULFILL`. Four emails. Free work is `ORDER`, `FULFILL` — two emails. First contact adds `WHICH`, `METHODS` up front — six emails total. The next transaction skips the negotiation — you already know the wallet.

Discovery, trust, escrow, disputes, refunds — all application layer. Axiomatic needs a code review. It checks the [trust topology](/proof-of-trust), finds blader with a year of clean settlements, sends the `ORDER`. The protocol doesn't know or care how axiomatic chose blader. You don't add escrow to a CashApp payment. You just don't pay people you don't trust.

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
| Semantic | Agent parsed the payload and accepted the obligation | **Envelopay `FULFILL`** |

None of the first four prove the agent validated the payment and committed to the work. The `FULFILL` email closes that gap. Doing the work *is* acceptance. The DKIM-signed reply with the work product is the semantic delivery receipt.

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
