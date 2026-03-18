---
layout: post
title: "Proof of Trust"
tags: vector-space
---

*Part of the [Vector Space](/vector-space) series.*

Email is decentralized. No single company runs it. Billions of messages route through competing servers every day. Spam filters work without a central authority deciding what's legitimate. How does it work? And why can't trust work the same way?

[How to Trust Advertisers](/how-to-trust-advertisers) described the composite signal: payment history, reviews, semantic consistency, DNS records. Independently verifiable, no single gatekeeper. But each signal is isolated. A clean Stripe history doesn't know about a Yelp rating. A domain age doesn't know about a QuickBooks P&L.

A plumber who's served the same neighborhood for twenty years has the evidence: Stripe transactions, customer reviews, a business license, supplier relationships. When she buys an ad, the platform treats her the same as a dropshipper who registered yesterday. The signals exist. They just don't talk to each other.

Proof of trust is a data structure that connects the signals into a graph. And it runs on email.

## The mechanism

This runs on DKIM-signed emails, not a blockchain. DKIM already proves a mail server sent a message. The same mechanism proves Stripe sent an attestation. Both parties confirm the relationship by forwarding DKIM-signed emails to the exchange. No new protocol—just email.

Why would Stripe participate? Because [ads.txt](https://iabtechlab.com/ads-txt/) already proved they will. The IAB got publishers, exchanges, and platforms to publish machine-readable seller declarations voluntarily. The incentive is fraud reduction: platforms that issue attestations attract advertisers who want to prove legitimacy. The ones that don't become the gap in the résumé.

And Stripe already sends DKIM-signed emails. The only new behavior is: format attestation data as JSON in the email body, merchant forwards it to an exchange. Lower adoption barrier than ads.txt, which required new infrastructure.

## The declaration

An advertiser publishes a signed declaration of their trust relationships:

- **Payment processor**: "Stripe has processed my payments for three years. Here is Stripe's attestation."
- **Customers**: "These customers endorse my work. Here are their signed endorsements."
- **Vendors**: "I source from these suppliers. Here is mutual attestation of the relationship."
- **Licensing**: "I hold this license in this jurisdiction. Here is the registry link."
- **Platform history**: "My Shopify store has this rating. Here is the verifiable export."

Each relationship is bilateral. The advertiser claims it; the counterparty confirms it. The confirmation is cryptographic: a signed payload anyone can verify without asking either party.

The declarations are coarse by design. "This merchant has processed payments for three years," not the transaction log. "This customer attests to the relationship," not the invoice. Enough to verify topology, not enough to reconstruct private activity.

## The exchange layer

An exchange is a specialized mail server that receives, verifies, and indexes attestation emails.

**How it works:**

1. Stripe sends merchant a DKIM-signed email: "We attest to 3 years of payment processing for merchant@example.com"
2. Merchant forwards the email to `attestations@exchange.com`
3. Exchange receives email, verifies DKIM signature, indexes the relationship
4. Merchant sends Stripe: "I confirm this relationship"
5. Stripe forwards to `attestations@exchange.com`
6. Exchange indexes: merchant ←→ Stripe (bilateral confirmation complete)

The exchange is just SMTP (receives emails) + DKIM verification (proves authenticity) + a graph database (indexes relationships) + a query API (exposes to curators).

Attestation emails contain structured data:

```
From: attestations@stripe.com
To: merchant@example.com
DKIM-Signature: [cryptographic signature]
Subject: Payment Processing Attestation

{
  "attestation_type": "payment_processor",
  "merchant_id": "merchant@example.com",
  "duration_years": 3,
  "status": "good_standing",
  "timestamp": "2026-03-18T15:00:00Z"
}
```

Bilateral confirmation requires emails from both parties. The merchant forwards Stripe's attestation; Stripe forwards the merchant's confirmation. Only when both emails arrive does the exchange create a mutual edge in the graph. One-sided claims don't count.

The exchange builds a public graph: nodes are businesses, edges are attested relationships, edge weights are reported signal strength (duration, volume, consistency). The exchange passes through what attestors claim. Curators interpret what it means.

One advertiser has three years of clean payment processing, 47 mutual customer attestations, two vendor relationships with reciprocal endorsements. Another has a week-old domain and a self-reported rating. The exchange exposes both. Curators decide what qualifies.

The graph is public. Anyone can query it. That's how trust works. Private attestations are just claims. Public attestations are verifiable topology. Curators read the graph to publish allowlists. Publishers verify curator criteria. Competitors audit each other's relationships. The transparency makes the graph unforgeable—you can't fake edges when anyone can see them. Like business licenses, domain WHOIS, court records: trust infrastructure is public by design. Merchants control field-level disclosure (transaction volumes are opt-in), but the edges themselves—who attests to whom—are visible to everyone.

## The curation layer

Curators interpret the graph. A curator is an independent party that publishes an allowlist: a set of advertisers that meet the curator's trust criteria. Different curators, different standards:

- A conservative health curator might require: licensed practitioner + clean payment history + minimum 20 patient attestations
- A general commerce curator might require: 6 months payment history + business registration + semantic consistency
- A community curator might require: 3 mutual endorsements from other businesses in the same locality

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

Email's curation layer works the same way. Mail servers subscribe to blocklists (Spamhaus, Barracuda, SpamCop). Each server chooses which lists to trust. No single list controls the ecosystem. The competitive pressure between lists keeps them honest. Twenty years of decentralized policy composition suggests the pattern scales. Imperfectly, with concentration and false positives, but better than any centralized alternative.

## The stack

| Layer | Role | Email equivalent |
|-------|------|------------------|
| Advertiser | Declares trust relationships, signed | DKIM sender |
| Exchange | Receives attestation emails, verifies DKIM, indexes graph | Mail server (SMTP + database) |
| Curator | Publishes allowlists based on graph criteria | Blocklist operators (Spamhaus) |
| Publisher | Composes trust policy from curators | Mail server spam policy |
| Audience | Sees filtered, trust-scored results | Inbox |

Five layers. No single point of control. The protocol is email.

## The topology is the credential

The trust graph exposes topology. A business with deep, reciprocal, long-standing relationships occupies a different position in the graph than a business with thin, one-directional, recent claims. The shape speaks.

Faking a rich trust topology gets expensive when the counterparties issuing attestations are themselves costly to compromise. A scammer can buy an old domain. Buying three years of clean Stripe processing, 47 customers willing to sign attestations, and two vendors willing to reciprocate is a different proposition. The graph is only as strong as the weakest attestor, which is why curation matters: curators decide which attestation types they require and which they discount.

You can't forge the graph without forging the relationships. But you can outspend it. A well-funded actor with real relationships can try to dominate legitimately. That's what federation solves. No single curator's allowlist is the index.

New businesses start with fewer attestations, qualify for fewer curators' allowlists, and earn their way in. New domains start in the spam folder. New advertisers start in the conservative tier. The path from zero to trusted is open. It just takes time and real relationships. That's the point.

## Every node is all three

Everything above assumes distinct advertisers, publishers, and audiences. As [transaction costs drop toward zero](https://doi.org/10.1111/j.1468-0335.1937.tb00002.x), those roles converge. Every person is advertiser, publisher, and consumer simultaneously. The same node in the trust graph. Your vibelog is your résumé. Your ad is your business card. Your topology is your credential.

The roles share a reputation. Burn trust as an advertiser (revoked attestation, thinning topology) and your publishing credibility drops too. The graph doesn't know which hat you were wearing when you defaulted. It just sees a weaker node.

Defaulting is a topological reset. Not punishment — geometry. Your edges thin. Your ads rank lower. Your publishing reaches fewer people. The path back is the same as the path in: earn real relationships, accumulate real attestations, rebuild one edge at a time. New domains start in the spam folder. Reset nodes start there too.

The cost of defection is losing your place in the graph, across all three roles. The topology self-corrects: burning edges tends to cost more than any single default is worth.

The plumber's signals finally talk to each other.

---

## Appendix

### Revocation

Either party can unlink at any time by sending a revocation email:

```
From: attestations@stripe.com
To: merchant@example.com
DKIM-Signature: [cryptographic signature]
Subject: Attestation Revocation

{
  "action": "revoke",
  "original_attestation_id": "merchant123_stripe_2023",
  "reason": "account_closed",
  "timestamp": "2026-03-18T16:00:00Z"
}
```

The merchant forwards it to the exchange. The exchange removes the edge from the graph. Unilateral—you don't need the other party's permission to unlink.

If Stripe detects fraud, they revoke the attestation. The merchant's payment processor edge disappears. Curators see a thinner topology. The merchant drops from allowlists. Their ads stop appearing.

If a business relationship ends, either party can unlink. The graph reflects current state, not historical claims. New businesses start with fewer edges and earn their way in. Businesses that burn relationships start over. The path back is the same as the path in: accumulate real attestations, rebuild one edge at a time.

The cost of defection is losing your place in the graph. You can't force anyone to stay connected. The graph is maintained by consent, updated by email, reset by defection.

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

The exchange receives the full attestation but only publishes opted-in fields. Curators see "3 years, good standing, 0.2% disputes" but not transaction volumes. More disclosure produces a stronger signal, but the merchant controls what to reveal.

Each attestor defines their own fields. The exchange doesn't need to know all possible schemas in advance—it just stores what's declared and publishes what's opted in. Curators query whatever fields matter for their criteria.

A merchant with minimal trust publishes "Stripe, 1 year, good standing" and qualifies for general commerce curators. Three years later, they add dispute rates and on-time settlement, qualifying for stricter verticals. Five years in, they publish transaction volumes, signaling "we're big enough to have something to lose," and qualify for premium allowlists. The privacy gradient lets businesses control their disclosure as they grow.

Every edge is timestamped. The exchange records when attestations arrive, when they're confirmed, when they're revoked. Curators can weight recent attestations more heavily than old ones, or require minimum relationship duration. The timestamps make relationship age verifiable without trusting self-reported claims.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
