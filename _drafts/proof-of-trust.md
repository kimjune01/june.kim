---
layout: post
title: "Proof of Trust"
tags: vector-space
---

*Part of the [Vector Space](/vector-space) series.*

[How to Trust Advertisers](/how-to-trust-advertisers) described the composite signal: payment history, reviews, semantic consistency, DNS records. Independently verifiable, no gatekeeper. But each signal is isolated. A clean Stripe history doesn't know about a Yelp rating. A domain age doesn't know about a QuickBooks P&L. The signals sit in silos. The advertiser knows they're trustworthy. The evidence exists. Nobody can see the whole picture without scraping every source independently.

Proof of trust is a data structure that connects the signals into a graph.

## The declaration

An advertiser publishes a signed declaration of their trust relationships:

- **Payment processor**: "Stripe has processed my payments for three years. Here is Stripe's attestation."
- **Customers**: "These customers endorse my work. Here are their signed endorsements."
- **Vendors**: "I source from these suppliers. Here is mutual attestation of the relationship."
- **Licensing**: "I hold this license in this jurisdiction. Here is the registry link."
- **Platform history**: "My Shopify store has this rating. Here is the verifiable export."

Each relationship is bilateral. The advertiser claims it; the counterparty confirms it. The confirmation is cryptographic — a signed payload that anyone can verify without asking either party. Not a review. Not a testimonial. A proof.

The mechanism doesn't need a blockchain. It needs what email already has: signed declarations that third parties can verify. DKIM proves a mail server sent a message. The same pattern proves Stripe processed a merchant's payments. An OAuth-like handshake where both parties confirm the relationship, producing a signed artifact that anyone can scrape and verify.

## The exchange layer

Ad exchanges scrape and index the trust declarations. The exchange doesn't evaluate trust. It aggregates. The trust graph is a public data structure: nodes are businesses, edges are attested relationships, edge weights are the strength of the signal (duration, volume, consistency).

The exchange sees: this advertiser has three years of clean payment processing, 47 mutual customer attestations, two vendor relationships with reciprocal endorsements, and semantic consistency between their declared [market position](/market-position-json) and their public footprint. The exchange doesn't decide whether that's enough. It exposes the data.

## The curation layer

Curators interpret the graph. A curator is an independent party that publishes an allowlist — a set of advertisers that meet the curator's trust criteria. Different curators, different standards:

- A conservative health curator might require: licensed practitioner + clean payment history + minimum 20 patient attestations
- A general commerce curator might require: 6 months payment history + business registration + semantic consistency
- A community curator might require: 3 mutual endorsements from other businesses in the same locality

Curators stake their reputation on their lists. A curator whose allowlist lets through scammers loses subscribers. A curator whose allowlist is too restrictive loses relevance. The competition between curators produces trust standards the same way competition between credit rating agencies produces credit standards — imperfectly, but better than a monopoly.

No single curator has veto power. No single curator is required. The curation layer is a market.

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

This is how email works. Mail servers subscribe to blocklists (Spamhaus, Barracuda, SpamCop). Each server chooses which lists to trust. No single list controls the ecosystem. The competitive pressure between lists keeps them honest. Twenty years of email infrastructure proves the pattern scales.

## The topology is the credential

The trust graph doesn't score businesses. It exposes their topology. A business with deep, reciprocal, long-standing relationships occupies a different position in the graph than a business with thin, one-directional, recent claims.

Healthy relationships? Trustworthy. Sketchy relationships? Caution. No authority makes the call. The shape speaks.

The cost of faking a rich trust topology approaches the cost of actually being trustworthy. You need real payment processing, real customers willing to attest, real vendors willing to reciprocate, real platform history. You can't forge the graph without forging the relationships, and forging the relationships IS being a real business.

This is proof of trust. Not social credit — no authority assigns the score. Not reputation — no platform owns the data. A verifiable, decentralized, composable trust graph where the topology is the credential and the cost of deception approaches the cost of legitimacy.

New businesses aren't excluded. They start with fewer attestations, qualify for fewer curators' allowlists, and earn their way in. New domains start in the spam folder. New advertisers start in the conservative tier. The path from zero to trusted is open. It just takes time and real relationships. That's the point.

## The stack

| Layer | Role | Analogy |
|-------|------|---------|
| Advertiser | Declares trust relationships, signed | SPF/DKIM sender declaration |
| Exchange | Scrapes, indexes, exposes the graph | Mail exchange routing |
| Curator | Publishes allowlists based on graph criteria | Blocklist operators (Spamhaus) |
| Publisher | Composes trust policy from curators | Mail server spam policy |
| Audience | Sees filtered, trust-scored results | Inbox |

Five layers. No single point of control. Each layer is competitive, replaceable, and independently auditable. The protocol is open. Trust is layered on top.

## Every node is all three

When [firm size collapses to one](https://doi.org/10.1111/j.1468-0335.1937.tb00002.x), every person is advertiser, publisher, and consumer simultaneously. The same node in the trust graph. Your vibelog is your résumé. Your ad is your business card. Your trust topology is your credential.

The roles aren't firewalled. They share a reputation. Burn trust as an advertiser — revoked attestation, thinning topology — and your publishing credibility drops too. The graph doesn't know which hat you were wearing when you defaulted. It just sees a weaker node.

Defaulting is a topological reset. Not punishment — geometry. Your edges thin. Your ads rank lower. Your publishing reaches fewer people. The path back is the same as the path in: earn real relationships, accumulate real attestations, rebuild one edge at a time. New domains start in the spam folder. Reset nodes start there too.

This is the enforcement mechanism. No court, no regulator, no gatekeeper. The cost of defection is losing your place in the graph. And your place in the graph is your livelihood across all three roles. The topology self-enforces because the cost of burning edges exceeds the benefit of any single default.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude drafted prose.*
