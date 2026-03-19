---
layout: post-wide
title: "Proof of Trust"
tags: vector-space
---

*Part of the [Vector Space](/vector-space) series.*

Email is decentralized. No single company runs it. Billions of messages route through competing servers every day. Spam filters work without a central authority deciding what's legitimate. How does it work? And why can't trust work the same way?

[How to Trust Advertisers](/how-to-trust-advertisers) described the composite signal: payment history, reviews, semantic consistency, DNS records. Independently verifiable, no single gatekeeper. But each signal is isolated. A clean Stripe history doesn't know about a Yelp rating. A domain age doesn't know about a QuickBooks P&L.

A plumber who's served the same neighborhood for twenty years has the evidence: Stripe transactions, customer reviews, a business license, supplier relationships. When she buys an ad, the platform treats her the same as a dropshipper who registered yesterday. The signals exist. They just don't talk to each other.

## What you'd need

To connect these signals into a trust graph, you'd need:

**Cryptographic proof.** Relationships need verification without asking either party. A signed attestation anyone can check.

**Decentralized routing.** No single company controls the exchange. Attestations need to reach multiple competing indices without a gatekeeper.

**Universal adoption.** The infrastructure needs to already exist. Builds on deployed identity and routing systems, not new wallets, blockchain nodes, or key management.

**Federated curation.** No single authority decides what counts as trust. Competing curators publish standards, publishers choose which to follow.

Blockchain tried this. PGP tried this. Both failed. Blockchain requires nodes, wallets, transaction fees, and consensus: too much infrastructure for incremental adoption. PGP requires key management, manual verification, and technical expertise: too complex for businesses. LinkedIn has endorsements but they're locked in a closed platform. Certificate authorities have attestations but they're only for domains, not business relationships.

Every attempt required building new infrastructure or adding complexity to existing workflows. The adoption barrier killed them.

## Email is the protocol.

[DKIM](https://datatracker.ietf.org/doc/html/rfc6376) provides cryptographic signatures. Every mail server checks them. [SMTP](https://datatracker.ietf.org/doc/html/rfc5321) routes between competing servers without a central authority. Most business email uses DKIM. Stripe sends DKIM-signed emails. So does every payment processor, review platform, and business service.

DKIM proves origin, not truth. A DKIM signature proves Stripe's mail server sent the email; it doesn't prove the relationship claim inside is accurate. That gap narrows through structure: bilateral confirmation requires both parties to send emails directly to the exchange (mutual acknowledgement), the exchange publishes the graph publicly (anyone can audit), and curators decide what the topology means (reputation interpretation). The cryptography proves "this came from stripe.com." The bilateral flow attests that "both parties agreed to claim this." The public graph enables "anyone can audit the topology." Curators decide "this pattern suggests trust." Collusion is still possible—the system makes it expensive to fake at scale, not impossible.

Why direct send, not forwarding? DKIM is transport-layer authentication. When a merchant clicks "Forward" in Gmail, the client creates a new message signed by the merchant's domain; Stripe's DKIM signature is gone. [ARC](https://datatracker.ietf.org/doc/html/rfc8617) preserves authentication chains through forwarding, but requires the exchange to trust the merchant's mail server, which defeats the purpose. So nobody forwards anything. Each party sends their own DKIM-signed email directly. Two first-party messages, both verifiable.

The infrastructure has been running for twenty years. Attestors format claims as JSON in email bodies and send them directly to an exchange. The exchange is a mail server with an append-only log. Curators pull the log and build their own indexes. Publishers compose trust policies from multiple curators.

The pattern is email spam filtering. Mail servers subscribe to blocklists ([Spamhaus](https://www.spamhaus.org/blocklists/), Barracuda, SpamCop), each choosing which lists to trust. No single list controls the ecosystem. Federated curation has worked for twenty years.

[ads.txt](https://iabtechlab.com/ads-txt/) proved platforms will adopt voluntary protocols if the fraud reduction incentive is clear. The [IAB](https://www.iab.com/) got publishers, exchanges, and platforms to publish machine-readable seller declarations without central enforcement. New requirements: attestors emit structured JSON, exchanges parse and index, parties send attestations directly. Lower barrier than ads.txt: builds on email infrastructure already deployed, no new hosting needed. Bootstrap follows the [stone soup](/stone-soup) pattern: early exchanges publish graphs, early curators publish standards, and each participant shows up for their own fraud-reduction advantage.

## The declaration

An advertiser publishes a signed declaration of their trust relationships:

- **Payment processor**: "Stripe has processed my payments for three years. Here is Stripe's attestation."
- **Customers**: "These customers endorse my work. Here are their signed endorsements."
- **Vendors**: "I source from these suppliers. Here is mutual attestation of the relationship."
- **Licensing**: "I hold this license in this jurisdiction. Here is the registry link."
- **Platform history**: "My Shopify store has this rating. Here is the verifiable export."

Attestations come in two forms: bilateral (mutual relationships) and unilateral (observations).

**Bilateral attestations** require both parties to confirm. Stripe sends an attestation email to the exchange; the merchant sends a separate confirmation. Each DKIM signature is first-hop and verifiable. The exchange creates a mutual edge: merchant ←→ Stripe. Relationships: payment processing, vendor partnerships, customer endorsements.

**Unilateral attestations** come from platforms observing public data. Google sends an attestation about a restaurant's reviews directly to the exchange. The restaurant doesn't confirm; Google attests to their own platform data. The exchange creates a one-directional edge: restaurant ← Google. Observations: ratings, licenses, public records.

The confirmation is cryptographic: a DKIM-signed payload anyone can verify without asking either party. Bilateral edges attest to mutual agreement. Unilateral edges attest to the platform's claim about their own data.

The declarations are coarse by design. "This merchant has processed payments for three years," not the transaction log. "This restaurant has 4.5 stars from 247 reviews," not the review contents. Enough to verify topology, not enough to reconstruct private activity.

## The exchange layer

An exchange is a specialized mail server that receives, verifies, and indexes attestation emails.

**How it works:**

1. Stripe sends attestation email directly to `attestations@exchange.com`: "We attest to 3 years of payment processing for merchant@example.com"
2. Exchange receives email, verifies Stripe's DKIM signature, indexes the claim
3. Merchant sends confirmation email directly to `attestations@exchange.com`: "I confirm my relationship with Stripe" (referencing Stripe's attestation ID)
4. Exchange receives email, verifies merchant's DKIM signature, matches the pair
5. Exchange indexes: merchant ←→ Stripe (bilateral confirmation complete)

The merchant's confirmation is lightweight: Stripe's dashboard shows a "Confirm on exchange" link, a `mailto:` pre-filled with the confirmation payload. Click, send. Everybody on the internet has email.

The exchange is [SMTP](https://datatracker.ietf.org/doc/html/rfc5321) + DKIM verification + a public ledger. Discovery is [MX records](https://datatracker.ietf.org/doc/html/rfc5321#section-5.1), because the exchange is a mail server, and mail server discovery is already solved.

Attestation emails contain structured data:

```
From: attestations@stripe.com
To: attestations@exchange.com
DKIM-Signature: [cryptographic signature]
Subject: Payment Processing Attestation

{
  "attestation_type": "payment_processor",
  "attestation_id": "stripe_merchant123_2026",
  "subject": "merchant@example.com",
  "duration_years": 3,
  "status": "good_standing",
  "timestamp": "2026-03-18T15:00:00Z"
}
```

The merchant's confirmation references the attestation ID:

```
From: merchant@example.com
To: attestations@exchange.com
DKIM-Signature: [cryptographic signature]
Subject: Attestation Confirmation

{
  "action": "confirm",
  "attestation_id": "stripe_merchant123_2026"
}
```

Bilateral confirmation requires emails from both parties, sent directly. Only when both emails arrive does the exchange create a mutual edge in the graph. One-sided relationship claims don't count.

**Unilateral attestations work differently.** Google sends an attestation about a restaurant's reviews directly to the exchange:

```
From: attestations@google.com
To: attestations@exchange.com
DKIM-Signature: [cryptographic signature]

{
  "attestation_type": "platform_rating",
  "attestation_id": "google_restaurant456_2026",
  "subject": "restaurant@example.com",
  "rating": 4.5,
  "review_count": 247,
  "platform": "Google Reviews",
  "timestamp": "2026-03-18"
}
```

The restaurant doesn't confirm; Google attests to their own platform data. The exchange creates a one-directional edge: restaurant ← Google. The restaurant can't block unfavorable reviews (that's the point), but platforms stake their reputation on accuracy. If Google claims reviews that don't exist on their platform, anyone can verify and call them out.

The exchange builds a public graph: nodes are businesses, edges are attested relationships (bilateral) or observations (unilateral), edge weights are reported signal strength (duration, volume, consistency). The exchange passes through what attestors claim. Curators interpret what it means.

One advertiser has three years of clean payment processing, 47 mutual customer attestations, two vendor relationships with reciprocal endorsements. Another has a week-old domain and a self-reported rating. The exchange exposes both. Curators decide what qualifies.

The graph is public. Anyone can pull it. Private attestations are just claims; public attestations are verifiable topology. The exchange serves its ledger over HTTPS as an append-only feed. Curators sync the ledger and build their own indexes. The exchange competes on uptime, coverage, and freshness; the curator bears the aggregation cost.

Forgery is expensive: faking edges requires compromising multiple parties who each have reputations to lose. Like business licenses, domain [WHOIS](https://en.wikipedia.org/wiki/WHOIS), court records: trust infrastructure is public by design. Merchants control field-level disclosure (transaction volumes are opt-in), but edges are visible to everyone. The exchange may serve its ledger freely or charge curators by API volume. Business decision, not protocol constraint.

**Attestation types** are minimal but extensible. The protocol seeds a canonical set: `payment_processor`, `platform_rating`, `customer_endorsement`, `vendor_relationship`, `license`. Attestors extend with URI-prefixed types: `https://stripe.com/attestation/payment_processing`, `https://google.com/attestation/review_summary`. Curators normalize across synonyms. That's their job, and why they compete. No central registry governs the vocabulary. The pattern follows [IANA media types](https://www.iana.org/assignments/media-types/): a small canonical core, a permissionless extension space, usage-driven convergence.

## The curation layer

Curators pull the graph from exchanges and interpret it. A curator syncs one or more exchange ledgers, builds a local index, and publishes an allowlist: advertisers that meet their trust criteria. A curator that syncs five exchanges has a richer graph than one that syncs one. Different curators, different standards, different sources.

A conservative health curator might require: licensed practitioner + clean payment history + minimum 20 patient attestations. A general commerce curator might require: 6 months payment history + business registration + semantic consistency. A community curator might require: 3 mutual endorsements from other businesses in the same locality.

Curators stake their reputation on their lists. A curator whose allowlist lets through scammers loses subscribers. A curator whose allowlist is too restrictive loses relevance. The competition between curators produces trust standards, imperfectly, but better than a monopoly. The design inverts credit rating agencies: curators are paid by subscribers (publishers), not by the entities they evaluate. The incentive points toward accuracy, not accommodation.

The curation layer is a market.

## The publisher layer

Publishers compose their trust policy from curators:

```
trust_policy:
  require_any:
    - curator: health-trust-network
    - curator: general-commerce-verified
    - curator: local-biz-portland
  deny:
    - denylist: known-scam-advertisers
    - denylist: low-quality-supplements
```

Union the allowlists. Subtract the denylists. What remains is the set of advertisers eligible to appear on this publisher's pages.

A health vibelogger subscribes to a strict health curator and a local business curator. A general tech blogger subscribes to a general commerce curator. Each publisher takes responsibility for what their audience sees. The trust policy is as public as the content.

Email's curation layer works the same way. Mail servers subscribe to blocklists ([Spamhaus](https://www.spamhaus.org/blocklists/), Barracuda, SpamCop). Each server chooses which lists to trust. No single list controls the ecosystem. The competitive pressure between lists keeps them honest. Twenty years of decentralized policy composition suggests the pattern scales. Imperfectly, with concentration and false positives, but better than any centralized alternative.

## The stack

| Layer | Role | Email equivalent |
|-------|------|------------------|
| Advertiser | Declares trust relationships, signed | DKIM sender |
| Exchange | Receives attestation emails, verifies DKIM, serves public ledger | Mail server (SMTP + ledger) |
| Curator | Pulls exchange logs, builds indexes, publishes allowlists | Blocklist operators (Spamhaus) |
| Publisher | Composes trust policy from curators | Mail server spam policy |
| Audience | Sees filtered, trust-scored results | Inbox |

Five layers. No single point of control. The protocol is email.

## The topology is the credential

The trust graph exposes topology. A business with deep, reciprocal, long-standing relationships occupies a different position than one with thin, one-directional, recent claims. The shape speaks.

You can't forge the graph without forging the relationships. But you can outspend it. A well-funded actor with real relationships can try to dominate legitimately. That's what federation solves. No single curator's allowlist is the index.

The plumber's signals finally talk to each other.

---

## Appendix

### Revocation

Either party can unlink at any time by sending a revocation email:

```
From: attestations@stripe.com
To: attestations@exchange.com
DKIM-Signature: [cryptographic signature]
Subject: Attestation Revocation

{
  "action": "revoke",
  "attestation_id": "stripe_merchant123_2026",
  "reason": "account_closed",
  "timestamp": "2026-03-18T16:00:00Z"
}
```

Either party sends a revocation directly to the exchange. The exchange removes the edge. Unilateral: you don't need the other party's permission.

If Stripe detects fraud, they revoke. The merchant's payment processor edge disappears, curators see a thinner topology, the merchant drops from allowlists.

If a business relationship ends, either party can unlink. The graph reflects current state, not historical claims.

### Extensible schemas

Attestors can optionally declare additional fields. Merchants choose which fields to publish:

```json
{
  "attestation_type": "payment_processor",
  "merchant_id": "merchant@example.com",

  "standard_fields": {
    "duration_years": 3,
    "status": "good_standing",
    "timestamp": "2026-03-18T15:00:00Z"
  },

  "optional_fields": {
    "transaction_count": 14250,
    "average_monthly_volume": 48000,
    "dispute_rate": 0.002,
    "chargeback_rate": 0.001,
    "on_time_settlement": true
  }
}
```

The merchant opts in to publish specific fields:

```json
{
  "publish": ["duration_years", "status", "dispute_rate"],
  "redact": ["transaction_count", "average_monthly_volume"]
}
```

The exchange receives the full attestation but only publishes opted-in fields. Curators see "3 years, good standing, 0.2% disputes" but not transaction volumes.

Each attestor defines their own fields. The exchange stores what's declared and publishes what's opted in. Curators query whatever fields matter for their criteria.

Every edge is timestamped. The exchange records when attestations arrive, when they're confirmed, when they're revoked. Curators can weight recent attestations more heavily than old ones, or require minimum relationship duration. The timestamps make relationship age verifiable without trusting self-reported claims.

### Design concerns

| Concern | Implementation |
|---------|----------------|
| Privacy: How much must I disclose? | Extensible schemas with opt-in field publishing. Edges are public (who attests to whom), field values are optional (transaction volumes, dispute rates). |
| Forgery: Can someone fake relationships? | DKIM cryptographic signatures + bilateral confirmation + public topology. Faking requires compromising both parties and withstanding public audit. |
| Revocation: What if a relationship ends badly? | Either party can unlink via email. No permission needed. Graph reflects current state, not historical claims. |
| New businesses: How do newcomers start? | Start with fewer edges, earn incrementally. Path from zero to trusted is open, just slower than established businesses. |
| Centralization: Who controls this? | Federated curators compete. Publishers compose from multiple curators. Exchanges compete. No single gatekeeper. |
| Verification: How do I know claims are real? | DKIM proves mail server origin. Public graph enables audit. Anyone can verify signatures and query topology. |
| Cost: What does participation cost? | Email infrastructure only. No blockchain fees, no token purchases, no transaction costs beyond sending mail. |
| Gaming: Can this be spammed or abused? | Faking rich topology is expensive when counterparties are costly to compromise. Curators filter weak signals. Topology reveals gaming patterns. |
| Anti-abuse: DDoS, spam, forged DNS? | Solved problems. Exchange operators import modern web infrastructure—rate limiting, DKIM verification, spam filtering—the same way any mail server does. |

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
