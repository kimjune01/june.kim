---
variant: post
title: "Envelopay Spec v0.2.0"
tags: envelopay
monospace_title: true
---

[Certified Mail](/certified-mail) argued for the protocol. [Sent](/sent) demonstrated it. This is the reference.

## Protocol

Every envelopay message is an email. One thing is required:

- **Subject:** `TYPE | note` (or just `TYPE`)

The subject is the protocol. A bare `WHICH` with no body is valid. The `X-Envelopay-Type` header is optional — agents parsing via API can use it for routing, but most email clients don't surface custom headers.

**Subject parsing.** The first token of the subject (after stripping `Re:` prefixes) must be one of the nine all-caps keywords: `WHICH`, `METHODS`, `PAY`, `ORDER`, `FULFILL`, `INVOICE`, `OFFER`, `ACCEPT`, `OOPS`. Receivers must strip one or more `Re:` prefixes before matching — email clients add these on reply, and the protocol lives inside email threading. `Fwd:` prefixes are not stripped; a forwarded message is a different act (e.g. forwarding a payment notification) and should not be parsed as a protocol message. If the subject and JSON body disagree on type, the subject wins — reply OOPS if the mismatch matters.

When a JSON body is present, it must be a single JSON object containing `v` (version string) and `type` (lowercase type name). Unknown fields must be ignored. The email may contain signatures, rich text, HTML wrappers, or other MIME parts — the protocol is agnostic. Extraction of the JSON object from the message body (stripping signatures, HTML tags, quoted text) is the receiver's responsibility.

**Natural language mode.** A METHODS reply with no parseable JSON body is valid. If the receiver replies to WHICH with a correctly formatted subject line (`METHODS | ...`) and natural language in the body describing accepted rails, `accepts_natural_language` is implicitly `true`. The sender should extract payment details (chain, token, wallet, price) from the natural language and may use natural language in subsequent ORDER tasks and notes. When JSON is present and `accepts_natural_language` is explicitly set, the explicit value takes precedence.

**Subject classification.** When a receiver has signaled `accepts_natural_language` (explicitly or implicitly), the sender MAY omit the type keyword from the subject line entirely. The receiver classifies intent from the full message — subject, body, and thread context. A human writing "I'd like the bundle please" in a reply to METHODS is an ORDER; the receiver must not require the keyword to act on it. If classification fails or is ambiguous, the receiver replies OOPS with `error.code` set to `ambiguous_intent` and a `note` asking for clarification — in natural language. The structured subject line remains the canonical form; natural language subjects are a concession to human senders, not a replacement for agent↔agent traffic.

**Assets.** The `chain` + `token` pair is the asset identity. `USDC` on Solana and `USDC` on Base are different assets. Symbols (`SOL`, `USDC`) and contract addresses are both valid as `token`; `chain` disambiguates.

**Settlement model.** For PAY, ORDER (prepaid), and OFFER, payment moves before the email is composed — the email carries a proof that it already happened. ACCEPT is the same: the counter-payment moves first, then the email carries the proof. INVOICE and WHICH carry no proof; they are requests. The protocol transports proofs, requests, and work products. It does not touch, hold, or verify funds. Proof structure is rail-defined and opaque to the protocol.

**Identifiers.** Every message type should carry an `id` (sender-generated, opaque — how you generate it is an application concern, unique within sender namespace). Messages reference specific prior messages with typed refs: `order_ref`, `invoice_ref`, `offer_ref`, `which_ref`. For errors or other cross-type references, OOPS may include a generic `ref` field with the `id` of any message.

**Threading.** ORDER↔FULFILL, INVOICE↔PAY, and OFFER↔ACCEPT pairs should preserve email threading via `In-Reply-To` and `References`. Other reply types (METHODS, OOPS) may thread but are not required to.

**DKIM.** Senders should DKIM-sign all envelopay messages. Receivers should verify when available. DKIM is not a prerequisite — forwarders and legitimate setups may lack it.

## Nine message types

| Type | Direction | Purpose |
|------|-----------|---------|
| `WHICH` | A → B | "What do you accept?" |
| `METHODS` | B → A | Accepted rails, wallets, pricing |
| `PAY` | A → B | Payment proof, no task |
| `ORDER` | A → B | Task request, optionally prepaid |
| `FULFILL` | B → A | Work product |
| `INVOICE` | B → A | "You owe me this, here's my wallet" |
| `OFFER` | A → B | "I'll give you X for Y" + proof |
| `ACCEPT` | B → A | "Deal" + counter-proof |
| `OOPS` | either | Something went wrong |

## How to send each one

### WHICH

Ask what the receiver accepts.

```
To: agent@example.com
Subject: WHICH
```

Optionally include a task for pricing:

```json
{"v":"0.2.0",
 "type":"which",
 "id":"wch_1a2b",
 "note":"Looking for a security-focused code review",
 "task":{"description":"Review PR #417"}}
```

Expected response: METHODS. If you already know the receiver's wallet, skip to ORDER or PAY.

| Field | Required | Description |
|-------|----------|-------------|
| `id` | no | Sender-generated identifier |
| `note` | no | Human-readable context |
| `task` | no | Task description for pricing |

### METHODS

Reply with what you accept. Quotes are indicative, not binding — METHODS is cheap.

```
Subject: METHODS | $0.50 USDC, Solana preferred
```
```json
{"v":"0.2.0",
 "type":"methods",
 "id":"mth_3c4d",
 "which_ref":"wch_1a2b",
 "note":"$0.50 USDC, Solana preferred",
 "accepts_natural_language": true,
 "rails":[
   {"chain":"solana",
    "token":"SOL",
    "wallet":"6dL6n77jJFWq4bu3cQp57H8rMUPEXu7uYN1XApPxpUif",
    "price":"500000000"},
   {"chain":"base",
    "token":"USDC",
    "wallet":"0x1a2B...",
    "price":"500000"},
   {"chain":"stripe",
    "token":"USD",
    "wallet":"https://pay.stripe.com/c/cs_live_abc123",
    "price":"50"}
 ]}
```

| Field | Required | Description |
|-------|----------|-------------|
| `rails` | yes | At least one accepted rail. Fiat rails (Stripe, Interac, PayPal) use `chain` for the network and `wallet` for the payment address or URL. Each rail has `chain`, `token`, `wallet`, and indicative `price` (smallest unit string, same convention as `amount`) |
| `accepts_natural_language` | no | `true` if the receiver accepts natural language in ORDER tasks and notes. Default `false` — sender should use structured `task` objects. Implicitly `true` when the METHODS reply has no parseable JSON body |
| `id` | no | Sender-generated identifier |
| `which_ref` | no | The WHICH `id` this responds to |
| `note` | no | Human-readable summary |

### PAY

Send money. No task. No reply expected.

```
To: friend@example.com
Subject: PAY | Dinner split
```
```json
{"v":"0.2.0",
 "type":"pay",
 "id":"pay_5e6f",
 "note":"Dinner — my half",
 "amount":"30000000",
 "token":"USDC",
 "chain":"base",
 "proof":{"tx":"0x7a3f..."},
 "invoice_ref":"inv_9mN3"}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Sender-generated identifier |
| `amount` | yes | Amount in smallest unit (string) |
| `token` | yes | Asset symbol (`SOL`, `USDC`) or contract address |
| `chain` | yes | Settlement chain |
| `proof` | yes | Rail-specific evidence (tx hash, signed intent, etc.) — structure is rail-defined |
| `invoice_ref` | no | The INVOICE `id` this pays |
| `note` | no | Human-readable context |

### ORDER

Request work. Can be unpaid (worker replies INVOICE or FULFILL) or prepaid (payment proof included, worker replies FULFILL directly).

**Unpaid order** — the worker decides what to charge:

```
To: worker@example.com
Subject: ORDER | Review PR #417
```
```json
{"v":"0.2.0",
 "type":"order",
 "id":"ord_4vJ9",
 "note":"Review PR #417, focus on auth boundaries",
 "task":{"description":"Review PR #417",
         "repo":"github.com/alice/widget",
         "scope":"security"}}
```

**Prepaid order** — payment proof included, worker fulfills directly:

```
To: books@shop.com
Subject: ORDER | The Encrypted Commons, epub
```
```json
{"v":"0.2.0",
 "type":"order",
 "id":"ord_8xK2",
 "note":"The Encrypted Commons, epub format",
 "task":{"description":"The Encrypted Commons, epub"},
 "amount":"8000000",
 "token":"USDC",
 "chain":"base",
 "proof":{"tx":"0x9c4e..."}}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Sender-generated identifier |
| `task` | yes | What needs to be done |
| `amount` | no | Payment amount in smallest unit (string). Present when prepaid |
| `token` | no | Asset symbol or contract address. Required when `amount` is present |
| `chain` | no | Settlement chain. Required when `amount` is present |
| `proof` | no | Payment proof. Required when `amount` is present |
| `note` | no | Human-readable context |

When `amount` and `proof` are present, the ORDER is prepaid. The receiver verifies the proof and replies with FULFILL. When absent, the receiver replies with INVOICE, FULFILL (if free), or OOPS.

### FULFILL

Deliver the work. Should reply to the ORDER email via `In-Reply-To`.

```
Subject: FULFILL | Approved with 2 comments
```
```json
{"v":"0.2.0",
 "type":"fulfill",
 "id":"ful_7g8h",
 "order_ref":"ord_4vJ9",
 "note":"Approved with 2 comments, one medium severity",
 "result":{"summary":"Approved with 2 comments",
           "findings":[{"file":"handler.go","line":47,
                        "severity":"medium",
                        "finding":"Session token not validated before use"}]}
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Sender-generated identifier |
| `order_ref` | yes | The ORDER `id` this fulfills |
| `result` | yes | Work product |
| `note` | no | Human-readable summary |

### INVOICE

Bill someone. Expected response: PAY.

```
To: client@example.com
Subject: INVOICE | Additional auth hardening
```
```json
{"v":"0.2.0",
 "type":"invoice",
 "id":"inv_9mN3",
 "order_ref":"ord_4vJ9",
 "note":"Auth hardening beyond original scope",
 "amount":"1000000",
 "token":"SOL",
 "chain":"solana",
 "wallet":"6dL6n77jJFWq4bu3cQp57H8rMUPEXu7uYN1XApPxpUif",
 "due":"2026-04-15"}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Sender-generated identifier |
| `amount` | yes | Amount owed in smallest unit (string) |
| `token` | yes | Asset symbol or contract address |
| `chain` | yes | Settlement chain |
| `wallet` | yes | Where to send payment |
| `due` | no | ISO 8601 date (a signal, not enforced) |
| `order_ref` | no | The ORDER this relates to |
| `note` | no | Human-readable context |

### OFFER

Propose an exchange. The offerer moves their asset first, then sends the proof with what they want in return. Expected response: ACCEPT or OOPS. OFFER↔ACCEPT pairs should preserve email threading.

```
To: counterparty@example.com
Subject: OFFER | 1 SOL for 30 USDC
```
```json
{"v":"0.2.0",
 "type":"offer",
 "id":"ofr_2k3m",
 "note":"1 SOL for 30 USDC",
 "give":{"amount":"1000000000","token":"SOL","chain":"solana",
         "to":"6dL6n77jJFWq4bu3cQp57H8rMUPEXu7uYN1XApPxpUif",
         "proof":{"tx":"4vJ9..."}},
 "want":{"amount":"30000000","token":"USDC","chain":"base"},
 "wallet":"0x1a2B..."}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Sender-generated identifier |
| `give` | yes | What was sent: amount, token, chain, recipient wallet (`to`), and proof |
| `want` | yes | What is expected back: amount, token, chain |
| `wallet` | yes | Where to send the counter-asset |
| `note` | no | Human-readable context |

### ACCEPT

Complete an exchange. The accepter verifies the OFFER proof, moves the counter-asset, and sends proof. Should reply via `In-Reply-To`.

```
Subject: ACCEPT | 30 USDC sent
```
```json
{"v":"0.2.0",
 "type":"accept",
 "id":"acc_4n5p",
 "offer_ref":"ofr_2k3m",
 "amount":"30000000",
 "token":"USDC",
 "chain":"base",
 "proof":{"tx":"0x8c7d..."}}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Sender-generated identifier |
| `offer_ref` | yes | The OFFER `id` this accepts |
| `amount` | yes | Counter-payment amount (must match OFFER's `want.amount`) |
| `token` | yes | Counter-payment asset (must match OFFER's `want.token`) |
| `chain` | yes | Counter-payment chain (must match OFFER's `want.chain`) |
| `proof` | yes | Counter-payment proof — structure is rail-defined |
| `note` | no | Human-readable context |

### OOPS

Something went wrong. The `note` tells a human; the `error` object tells an agent.

```
Subject: OOPS | Payment not found on-chain
```
```json
{"v":"0.2.0",
 "type":"oops",
 "id":"oops_0i1j",
 "note":"Payment not found on-chain",
 "error":{"code":"tx_not_found","tx":"0x3a7f..."}}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | no | Sender-generated identifier |
| `note` | yes | Human-readable explanation |
| `error` | no | Machine-readable error object with `code` |
| `ref` | no | The `id` of the message this error relates to (any type) |

Error codes: `tx_not_found`, `amount_mismatch`, `dkim_failed`, `unknown_type`, `ambiguous_intent`, `insufficient_funds`, `missing_wallet`.

If the subject matches `^[A-Z]+(\s*\|.*)?$` but the keyword isn't one of the nine types, reply OOPS with `unknown_type` and the list of supported types.

No message requires a response. Silence is always valid. OOPS is a courtesy.

## Flows

**Pay:** `PAY` → done.

**Prepaid order:** `ORDER` (with proof) → `FULFILL`. Two emails.

**Order work:** `ORDER` → `INVOICE` → `PAY` → `FULFILL`. Four emails.

**Free work:** `ORDER` → `FULFILL`. Two emails.

**Invoice:** `INVOICE` → `PAY`. Two emails.

**First contact:** `WHICH` → `METHODS` → `ORDER` (with proof) → `FULFILL`. Four emails.

**First contact (unpaid):** `WHICH` → `METHODS` → `ORDER` → `INVOICE` → `PAY` → `FULFILL`. Six emails.

**Repeat customer:** `ORDER` (with proof) → `FULFILL`. Two emails.

**Exchange:** `OFFER` → `ACCEPT`. Two emails, two on-chain transfers.

## Verification

Receivers should verify before acting on any proof-carrying message (PAY, ORDER with proof, OFFER, ACCEPT):

1. DKIM signature (when available)
2. Payment proof per the rail's verification method (tx exists, amount matches, recipient matches)
3. Replay protection (sender + protocol `id` + proof deduplication)

## Example: AgentMail

Any email API works. Here's [AgentMail](https://www.agentmail.to) as one example.

```bash
# Send a prepaid ORDER
curl -X POST https://api.agentmail.to/v0/inboxes/me@agentmail.to/threads \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to":["books@shop.agentmail.to"],
       "subject":"ORDER | The Encrypted Commons",
       "text":"{\"v\":\"0.2.0\",\"type\":\"order\",\"id\":\"ord_1\",\"task\":{\"description\":\"The Encrypted Commons, epub\"},\"amount\":\"8000000\",\"token\":\"USDC\",\"chain\":\"base\",\"proof\":{\"tx\":\"0x9c4e...\"}}"}'

# Reply to a thread
curl -X POST https://api.agentmail.to/v0/inboxes/me@agentmail.to/threads/$THREAD_ID/reply \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subject":"FULFILL | Done",
       "text":"{\"v\":\"0.2.0\",\"type\":\"fulfill\",\"id\":\"ful_1\",\"order_ref\":\"ord_1\",\"result\":{\"summary\":\"Done\"}}"}'
```

Receive via webhook: register a URL at AgentMail, incoming emails arrive as POST. Parse the JSON body, route by subject type.

## What the protocol doesn't do

| Protocol | Application |
|----------|-------------|
| Message types and subject line | Discovery and ranking |
| Proof payload (opaque) | Proof verification per rail |
| Email threading | Retries and timeouts |
| DKIM (when available) | Reputation and trust |

Discovery, trust, escrow, disputes, refunds — application concerns. The protocol carries proofs. Applications decide policy.

---

[Certified Mail](/certified-mail) — the argument | [Sent](/sent) — the demo | [Repo](https://github.com/kimjune01/envelopay) | All Envelopay posts: [june.kim/envelopay](/envelopay)
