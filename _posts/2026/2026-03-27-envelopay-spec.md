---
layout: post
title: "Envelopay Spec"
tags: envelopay
description: "v0.1.0"
---

[Certified Mail](/certified-mail) argued for the protocol. [Sent](/sent) demonstrated it. This is the reference. If you can send email, you can implement envelopay from this page.

# Seven message types

Every message is an email with a JSON body. Set the subject to `TYPE | note` and the `X-Envelopay-Type` header to the type. Always include `"v":"0.1.0"` in the JSON.

| Type | Direction | Purpose |
|------|-----------|---------|
| `WHICH` | A → B | "What do you accept?" |
| `METHODS` | B → A | Accepted rails, wallets, pricing |
| `PAY` | A → B | Payment proof, no task |
| `ORDER` | A → B | Task + payment proof |
| `FULFILL` | B → A | Work product + settlement proof |
| `INVOICE` | B → A | "You owe me this, here's my wallet" |
| `OOPS` | either | Something went wrong |

# How to send each one

### WHICH

Ask what the receiver accepts. Optionally include a task for pricing.

```
To: agent@example.com
Subject: WHICH
X-Envelopay-Type: WHICH
```
```json
{"v":"0.1.0",
 "type":"which",
 "note":"Looking for a security-focused code review",
 "task":{"description":"Review PR #417"}}
```

You'll get back a METHODS reply with their rails and wallets.

If you already know the receiver's wallet, skip WHICH and send ORDER or PAY directly.

### METHODS

Reply with what you accept.

```
Subject: METHODS | $0.50 USDC, Solana preferred
X-Envelopay-Type: METHODS
```
```json
{"v":"0.1.0",
 "type":"methods",
 "note":"$0.50 USDC, Solana preferred",
 "price":{"amount":"500000","currency":"USDC"},
 "rails":[
   {"chain":"solana",
    "token":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "wallet":"6dL6n77jJFWq4bu3cQp57H8rMUPEXu7uYN1XApPxpUif"},
   {"chain":"base",
    "token":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "wallet":"0x1a2B..."}
 ],
 "fallback":"https://pay.stripe.com/c/cs_live_abc123"}
```

### PAY

Send money. No task. A tip, a split bill, a donation. No reply expected.

Move the money on-chain first, then send the email with the proof.

```
To: friend@example.com
Subject: PAY | Dinner split
X-Envelopay-Type: PAY
```
```json
{"v":"0.1.0",
 "type":"pay",
 "note":"Dinner — my half",
 "amount":"30000000",
 "token":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
 "chain":"base",
 "proof":{"tx":"0x7a3f..."}}
```

### ORDER

Send money with a task. Move the money first. You'll get back a FULFILL.

```
To: worker@example.com
Subject: ORDER | Review PR #417
X-Envelopay-Type: ORDER
```
```json
{"v":"0.1.0",
 "type":"order",
 "note":"Review PR #417, focus on auth boundaries",
 "task":{"description":"Review PR #417",
         "repo":"github.com/alice/widget",
         "scope":"security"},
 "amount":"500000",
 "token":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
 "chain":"solana",
 "proof":{"tx":"4vJ9..."}}
```

### FULFILL

Deliver the work. Reply to the ORDER — include `In-Reply-To` referencing the ORDER's Message-ID.

```
Subject: FULFILL | Approved with 2 comments
X-Envelopay-Type: FULFILL
```
```json
{"v":"0.1.0",
 "type":"fulfill",
 "note":"Approved with 2 comments, one medium severity",
 "result":{"summary":"Approved with 2 comments",
           "findings":[{"file":"handler.go","line":47,
                        "severity":"medium",
                        "finding":"Session token not validated before use"}]},
 "settlement":{"tx":"4vJ9...","verified":true,"block":285714200}}
```

### INVOICE

Bill someone. The recipient decides whether to pay. If they do, they send a PAY.

```
To: client@example.com
Subject: INVOICE | Additional auth hardening
X-Envelopay-Type: INVOICE
```
```json
{"v":"0.1.0",
 "type":"invoice",
 "note":"Auth hardening beyond original scope",
 "amount":"1000000",
 "token":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
 "chain":"solana",
 "wallet":"6dL6n77jJFWq4bu3cQp57H8rMUPEXu7uYN1XApPxpUif"}
```

### OOPS

Something went wrong. Any message can get an OOPS back. The `note` tells a human; the `error` object tells an agent.

```
Subject: OOPS | Payment not found on-chain
X-Envelopay-Type: OOPS
```
```json
{"v":"0.1.0",
 "type":"oops",
 "note":"Payment not found on-chain",
 "error":{"code":"tx_not_found","tx":"0x3a7f..."}}
```

Error codes: `tx_not_found`, `amount_mismatch`, `dkim_failed`, `unknown_type`, `insufficient_funds`, `missing_wallet`.

If you receive a subject that matches `^[A-Z]+(\s*\|.*)?$` but the keyword isn't one of the seven types, reply OOPS with `unknown_type` and the list of supported types.

No message requires a response. Silence is always valid. OOPS is a courtesy.

# Flows

**Pay:** `PAY` → done.

**Order work:** `ORDER` → `FULFILL`. Two emails.

**Invoice:** `INVOICE` → `PAY`. Two emails.

**First contact:** `WHICH` → `METHODS` → `ORDER` → `FULFILL`. Four emails.

**Repeat customer:** `ORDER` → `FULFILL`. Skip negotiation.

# Verification

Before doing work, verify:

1. Check DKIM signature on the incoming email
2. Verify the proof on-chain (tx exists, amount matches, recipient matches)
3. Check for replay (track processed Message-IDs)

# Example: AgentMail

Any email API works. Here's [AgentMail](https://www.agentmail.to) as one example.

**Send a WHICH:**

```bash
curl -X POST https://api.agentmail.to/v0/inboxes/me@agentmail.to/threads \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["worker@agentmail.to"],
    "subject": "WHICH | Code review",
    "text": "{\"v\":\"0.1.0\",\"type\":\"which\",\"note\":\"Code review\",\"task\":{\"description\":\"Review PR #417\"}}",
    "headers": {"X-Envelopay-Type": "WHICH"}
  }'
```

**Reply to a thread:**

```bash
curl -X POST https://api.agentmail.to/v0/inboxes/me@agentmail.to/threads/$THREAD_ID/reply \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "FULFILL | Done",
    "text": "{\"v\":\"0.1.0\",\"type\":\"fulfill\",\"note\":\"Done\",\"result\":{\"summary\":\"Approved\"}}",
    "headers": {"X-Envelopay-Type": "FULFILL"}
  }'
```

**Receive via webhook:**

Register a webhook URL at AgentMail. Incoming emails arrive as POST with a `message` object containing `from_`, `subject`, `text`, `thread_id`, and `message_id`. Parse the JSON body, route by type.

# What the protocol doesn't do

| Protocol | Application |
|----------|-------------|
| Message types and headers | Discovery and ranking |
| Proof payload | Pricing and negotiation |
| Email threading | Retries and timeouts |
| DKIM verification | Reputation and trust |

Discovery, trust, escrow, disputes, refunds — application concerns. The protocol carries proofs. Applications decide policy.

---

[Certified Mail](/certified-mail) — the argument | [Sent](/sent) — the demo | [Repo](https://github.com/kimjune01/envelopay) | [All Envelopay posts](/envelopay)
