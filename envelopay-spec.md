# Envelopay Spec v0.1.0

[Certified Mail](https://june.kim/certified-mail) argued for the protocol. [Sent](https://june.kim/sent) demonstrated it. This is the reference.

## Protocol

Every envelopay message is an email. One thing is required:

- **Subject:** `TYPE | note` (or just `TYPE`)

The subject is the protocol. A bare `WHICH` with no body is valid. The `X-Envelopay-Type` header is optional — agents parsing via API can use it for routing, but most email clients don't surface custom headers.

**Subject parsing.** The first token of the subject must be one of the nine all-caps keywords: `WHICH`, `METHODS`, `PAY`, `ORDER`, `FULFILL`, `INVOICE`, `OFFER`, `ACCEPT`, `OOPS`. No stripping — `Re:` and `Fwd:` prefixes mean the sender doesn't speak the protocol. If the subject and JSON body disagree on type, the subject wins — reply OOPS if the mismatch matters.

When a JSON body is present, it must be a single JSON object containing `v` (version string) and `type` (lowercase type name). Unknown fields must be ignored. The email may contain signatures, rich text, HTML wrappers, or other MIME parts — the protocol is agnostic. Extraction of the JSON object from the message body (stripping signatures, HTML tags, quoted text) is the receiver's responsibility.

**Assets.** The `chain` + `token` pair is the asset identity. `USDC` on Solana and `USDC` on Base are different assets. Symbols (`SOL`, `USDC`) and contract addresses are both valid as `token`; `chain` disambiguates.

**Settlement model.** For PAY and OFFER, payment moves before the email is composed — the email carries a proof that it already happened. ACCEPT is the same: the counter-payment moves first, then the email carries the proof. INVOICE and WHICH carry no proof; they are requests. The protocol transports proofs, requests, and work products. It does not touch, hold, or verify funds. Proof structure is rail-defined and opaque to the protocol.

**Identifiers.** Every message type should carry an `id` (sender-generated, opaque — how you generate it is an application concern, unique within sender namespace). Messages reference specific prior messages with typed refs: `order_ref`, `invoice_ref`, `offer_ref`, `which_ref`. For errors or other cross-type references, OOPS may include a generic `ref` field with the `id` of any message.

**Threading.** ORDER↔FULFILL, INVOICE↔PAY, and OFFER↔ACCEPT pairs should preserve email threading via `In-Reply-To` and `References`. Other reply types (METHODS, OOPS) may thread but are not required to.

**DKIM.** Senders should DKIM-sign all envelopay messages. Receivers should verify when available. DKIM is not a prerequisite — forwarders and legitimate setups may lack it.

## Nine message types

| Type | Direction | Purpose |
|------|-----------|---------|
| `WHICH` | A → B | "What do you accept?" |
| `METHODS` | B → A | Accepted rails, wallets, pricing |
| `PAY` | A → B | Payment proof, no task |
| `ORDER` | A → B | Task request |
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
{"v":"0.1.0",
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
{"v":"0.1.0",
 "type":"methods",
 "id":"mth_3c4d",
 "which_ref":"wch_1a2b",
 "note":"$0.50 USDC, Solana preferred",
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
{"v":"0.1.0",
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

Request work. The worker decides what to charge — they reply with INVOICE, FULFILL (if free), or OOPS.

```
To: worker@example.com
Subject: ORDER | Review PR #417
```
```json
{"v":"0.1.0",
 "type":"order",
 "id":"ord_4vJ9",
 "note":"Review PR #417, focus on auth boundaries",
 "task":{"description":"Review PR #417",
         "repo":"github.com/alice/widget",
         "scope":"security"}}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Sender-generated identifier |
| `task` | yes | What needs to be done |
| `note` | no | Human-readable context |

### FULFILL

Deliver the work. Should reply to the ORDER email via `In-Reply-To`.

```
Subject: FULFILL | Approved with 2 comments
```
```json
{"v":"0.1.0",
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
{"v":"0.1.0",
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
{"v":"0.1.0",
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
{"v":"0.1.0",
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
{"v":"0.1.0",
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

Error codes: `tx_not_found`, `amount_mismatch`, `dkim_failed`, `unknown_type`, `insufficient_funds`, `missing_wallet`.

If the subject matches `^[A-Z]+(\s*\|.*)?$` but the keyword isn't one of the nine types, reply OOPS with `unknown_type` and the list of supported types.

No message requires a response. Silence is always valid. OOPS is a courtesy.

## Flows

**Pay:** `PAY` → done.

**Order work:** `ORDER` → `INVOICE` → `PAY` → `FULFILL`. Four emails.

**Free work:** `ORDER` → `FULFILL`. Two emails.

**Invoice:** `INVOICE` → `PAY`. Two emails.

**First contact:** `WHICH` → `METHODS` → `ORDER` → `INVOICE` → `PAY` → `FULFILL`. Six emails.

**Repeat customer:** `ORDER` → `INVOICE` → `PAY` → `FULFILL`. Skip negotiation.

**Exchange:** `OFFER` → `ACCEPT`. Two emails, two on-chain transfers.

## Verification

Receivers should verify before acting on any proof-carrying message (PAY, OFFER, ACCEPT):

1. DKIM signature (when available)
2. Payment proof per the rail's verification method (tx exists, amount matches, recipient matches)
3. Replay protection (sender + protocol `id` + proof deduplication)

## Example: AgentMail

Any email API works. Here's [AgentMail](https://www.agentmail.to) as one example.

```bash
# Send a WHICH
curl -X POST https://api.agentmail.to/v0/inboxes/me@agentmail.to/threads \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to":["worker@agentmail.to"],
       "subject":"WHICH | Code review",
       "text":"{\"v\":\"0.1.0\",\"type\":\"which\",\"note\":\"Code review\"}"}'

# Reply to a thread
curl -X POST https://api.agentmail.to/v0/inboxes/me@agentmail.to/threads/$THREAD_ID/reply \
  -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subject":"FULFILL | Done",
       "text":"{\"v\":\"0.1.0\",\"type\":\"fulfill\",\"id\":\"ful_1\",\"order_ref\":\"ord_1\",\"result\":{\"summary\":\"Done\"}}"}'
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

[Certified Mail](https://june.kim/certified-mail) — the argument | [Sent](https://june.kim/sent) — the demo | [Repo](https://github.com/kimjune01/envelopay) | All Envelopay posts: [june.kim/envelopay](https://june.kim/envelopay)
