---
layout: post
title: "Stay or Pay"
tags: vector-space
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched prior art and drafted prose.*

*Part of the [Vector Space](/vector-space) series.*

---

Every stable market has switching costs. The FCC charges spectrum license fees. ICANN charges domain renewal fees. Landlords charge lease termination fees. Insurance companies reward claim-free years with progressive discounts. These aren't frictions to be eliminated. They're structural features that prevent the market from collapsing into a land grab.

[Synthetic Friction](/synthetic-friction) proved that embedding-space auctions need the same thing — a relocation fee that prevents Hotelling drift. [It Costs Money to Move](/relocation-fees) showed the TEE-enforced mechanism. This post assembles the enforcement stack around it: identity binding, entry bonds, and tenure discounts. Every component has decades of prior art. Every one has been proven net-positive for all participants — not just the platform, but the advertisers who pay the fees.

The pattern is the same everywhere it appears. Introduce switching costs. Participants differentiate instead of clustering. Match quality improves. Surplus increases. The market with friction outperforms the market without it — and the friction pays for itself.

## Three Attack Surfaces

The relocation fee creates value. That value creates incentives to circumvent it.

**Account resets.** An advertiser accumulates drift history, owes a large relocation fee, and creates a new account. Fresh account, no history, no fee. The position commitment chain starts at zero.

**Exchange defection.** Exchange A enforces relocation fees. Exchange B launches with "zero fees, same inventory." Advertisers optimize positions on B for free, then bid on A with their discovered vectors.

**Bootstrapping friction.** New advertisers need to enter the market. A system that treats every new entrant as a suspected resetter will suppress legitimate demand. The enforcement has to distinguish a PT opening her first practice from Nike's seventeenth shell account.

Each attack has a known defense. The defenses come from spectrum auctions, insurance markets, payment networks, and platform identity systems. None of this is new. The pieces just haven't been assembled for continuous embedding space.

## Identity Binding

Google solved Problem 1 in 2023. Their Advertiser Identity Verification program requires government-issued IDs, business incorporation documents, and payment credentials. Cross-account detection uses billing details, device fingerprints, IP patterns, and behavioral analysis. Creating a new account after suspension is an "egregious" policy violation — immediate permanent ban, propagated to related accounts.

The mechanism is multi-signal. No single signal is sufficient. A new email address is trivial. A new credit card is easy. A new business registration with a new credit card from a new IP address using a new device — that's expensive. The cost of creating a convincing fake identity exceeds the cost of paying the relocation fee. That's the equilibrium.

For an embedding-space protocol, identity binding needs one additional property: it must be portable across exchanges. Google's identity verification is platform-specific — verified on Google, unknown on Meta. A protocol-level identity would bind position history to a verified credential that travels with the bid, the same way `position_commitment` already does.

The decentralized version exists. Gitcoin Passport (now Human Passport, acquired by Holonym Foundation in 2024) issues verifiable credentials — "Stamps" — that prove uniqueness without exposing personal information. A zero-knowledge proof of identity: the exchange verifies "this is a unique advertiser" without learning who they are. The credential travels across exchanges. The position history is bound to it. Creating a second credential requires defeating the proof-of-personhood layer, not just registering a new email.

The pragmatic version is simpler. Bind position history to payment credentials. Same credit card across exchanges means same position chain. The protocol field becomes:

```json
{
  "identity_hash": "sha256(payment_credential + business_id)",
  "position_commitment": "sha256:a1b2c3...",
  "tenure_rounds": 847,
  "drift_distance_sq": 0.005
}
```

The identity hash is computed inside the TEE. The exchange never sees the raw payment credential — it sees the hash and verifies it against the commitment chain. Two exchanges running the same attested code will compute the same hash for the same advertiser. Position history follows the advertiser, not the account.

## Entry Bond

The FCC solved this in 1994. Spectrum auctions require a refundable upfront deposit before bidding begins. The deposit establishes bidding eligibility and provides a source of funds for default penalties. Bidders who win and walk away forfeit the deposit. Bidders who participate honestly get it back.

The entry bond serves two functions in embedding space. First, it prices the option to create a new identity. If creating a fresh account requires posting $5,000 that you only recover after 6 months of stable positioning, the cost of an account reset is $5,000 in locked capital plus 6 months of reduced fee discounts. The relocation fee has to exceed that cost for the reset to be rational. For most advertisers, it won't.

Second, it distinguishes new entrants from resetters. A genuine new advertiser — the PT opening her first practice — posts the bond once. She finds her position, stabilizes, and recovers the bond after the tenure period. The cost is temporary. A serial resetter posts the bond every time. The cost is permanent and compounding.

Ethereum's proof-of-stake adds a refinement worth borrowing: the correlation penalty. If multiple related accounts (same identity hash cluster, similar timing, adjacent positions) all reset simultaneously, the forfeiture penalty scales with the number of coordinated resets. One reset costs 1x. Five coordinated resets cost 25x. The quadratic scaling makes organized gaming unprofitable even if individual resets are cheap.

The protocol field:

```json
{
  "bond_status": "active",
  "bond_amount": 5000,
  "bond_posted_round": 12,
  "refund_eligible_round": 192
}
```

The bond amount is a protocol parameter, like λ. Too low and it doesn't deter resets. Too high and it suppresses new entrants. The FCC calibrates upfront deposits to roughly 2-5% of expected total spend. That's a reasonable starting point — enough to hurt a casual gamer, not enough to block a legitimate small business.

## Tenure Discount

The insurance industry solved the stay-put problem in the 1960s. Bonus-malus systems — formalized by Jean Lemaire at Wharton in 1995 — give policyholders progressive premium discounts for each claim-free year. A driver with 10 years of no claims pays 40-60% less than a new driver. Filing a claim resets the discount. The system creates a financial asset — accumulated tenure — that the policyholder destroys by misbehaving.

In embedding space, the analog is a fee discount that grows with positional stability. An advertiser who holds the same center point (within noise) for 100 rounds pays a lower base rate than one who arrived last round. The relocation fee has two components:

```
effective_fee = base_fee × tenure_discount × λ · ‖move‖²
```

Where `tenure_discount` decays from 1.0 (new) toward a floor (say 0.3) over time. The discount applies to the base fee multiplier, not the distance component — a long-tenured advertiser who makes a large move still pays proportionally for distance, but the rate is lower.

This creates the asset the user described: a stay-put discount that makes switching relatively expensive. An advertiser with 200 rounds of tenure at position P has accumulated a 70% fee discount. Resetting to a new account means restarting at 0% discount. Even if the identity binding is imperfect — even if they successfully create a new identity — they lose the financial asset they built.

Google's Quality Score works this way implicitly. Accounts with long keyword history accumulate CTR data that improves Quality Scores, which lowers CPCs. A new account starts cold — same keywords, higher costs. The switching cost isn't a posted fee. It's embedded in the scoring function. Advertisers stay because leaving is expensive, not because a rule says they must.

The bonus-malus framing has one advantage over implicit stickiness: it's transparent. The advertiser knows the discount schedule. They can calculate the cost of resetting. The decision is explicit, not buried in an opaque quality score. Transparency is the theme of the [entire architecture](/model-blindness) — attested code, published scoring functions, verifiable embeddings. The tenure discount should be as visible as the relocation fee.

## Why Exchanges Adopt

Problems 1 and 3 — identity and bootstrapping — are mechanism design within the protocol. Problem 2 is different. You can't force competing exchanges to run your code. You need them to want to.

Rochet and Tirole formalized this in 2003. In a two-sided market, adoption requires that one side is subsidized. Visa subsidized consumers through rewards (funded by merchant interchange fees) until consumer adoption forced merchant acceptance. The payment network didn't need to mandate merchant participation. The demand-side critical mass made non-participation more expensive than compliance.

The embedding-space analog: exchanges that enforce relocation fees have better inventory. Not morally better. Measurably better.

The [simulation data](/synthetic-friction) shows it directly. Without fees, Hotelling drift compresses advertiser positions toward the demand centroid. Match quality degrades. Specialist surplus drops. The auction clears at higher prices for worse relevance. With fees, advertisers stay differentiated. Match quality is higher. Specialist surplus is 61% higher than keywords. The inventory is worth more because the ads are more relevant.

DSPs optimize for return on ad spend. An exchange where the climbing PT's ad appears on climbing queries — not on generic fitness queries — delivers higher conversion rates. DSPs route more demand to that exchange. Publisher revenue increases. The exchange with fees attracts the demand because the fees produce the inventory quality that justifies the demand.

The exchange without fees gets the Hotelling-collapsed inventory. Every advertiser clustered at the demand centroid. Generic matches. Lower conversion rates. DSPs route demand elsewhere. The "zero fee" exchange is cheaper for advertisers but worse for everyone — including the advertisers, who earn lower surplus in the collapsed market. The simulation proved this: embeddings without fees earn surplus of 2.155 per round; with fees, 2.416. The fee-charging exchange delivers more value to the advertisers it charges.

This is the OpenRTB adoption pattern. OpenRTB succeeded because it reduced integration cost — implement once, connect to all. The fee protocol succeeds because it increases inventory quality — enforce fees, attract demand. Both make non-adoption costly without mandating adoption. The difference is that OpenRTB's benefit was cost reduction (negative incentive to stay proprietary), while the fee protocol's benefit is revenue increase (positive incentive to adopt).

The cautionary tale is OpenRTB 3.0, released in 2020 and still not adopted because migration cost exceeded the benefit. The fee protocol has to be incrementally adoptable. An exchange that already runs TEE-attested auctions adds relocation fees as one more line in the clearing code. An exchange that doesn't run TEEs has a larger migration — but that migration is justified independently by the [demand-side preference for verifiable auctions](/keywords-are-tiny-circles), not by the fee protocol alone.

## The Stack

Five mechanisms, each with decades of deployment, each proven net-positive for participants.

| Attack | Defense | Prior Art | Net Effect |
|---|---|---|---|
| Account resets | Identity binding (payment credential hash) | Google AIV (2023), Human Passport (2024) | Continuity across exchanges |
| Cheap new accounts | Entry bond (refundable deposit) | FCC spectrum auctions (1994) | Screens out frivolous entrants |
| Fee dodging via switching | Tenure discount (bonus-malus) | Insurance industry (Lemaire, 1995) | Rewards stability, compounds over time |
| Exchange defection | Inventory quality loop | Rochet & Tirole (2003), OpenRTB (2010) | Fee-charging exchanges win on demand |
| Coordinated gaming | Correlation penalty | Ethereum PoS slashing (2022) | Quadratic cost for organized resets |

The mechanisms interact. A tenure discount that's too steep makes the entry bond redundant — the discount *is* the bond, accumulated over time. An entry bond that's too high makes the tenure discount unnecessary. The right calibration is empirical — the [simulation](https://github.com/kimjune01/openauction) can test parameter combinations the way it tested λ values for the relocation fee.

But the direction is clear. Every industry that has introduced switching costs into a frictionless market has seen the same result: participants differentiate, match quality improves, and total surplus increases. The FCC's spectrum auctions raised $44.9 billion because positional commitment made licenses valuable. Insurance bonus-malus systems reduced accident rates because tenure discounts made safe driving financially rational. The London congestion charge cut inner-city traffic 20% because the fee internalized an externality that was destroying the commons.

Embedding space is the same commons. The switching costs are the same solution. The prior art says it works — not in theory, but in markets that clear billions of dollars annually.

## References

- **Douceur, J.R. (2002).** "The Sybil Attack." *IPTPS*. The original formalization. Prevention requires either a central identity authority, social trust, or economic cost.

- **Lemaire, J. (1995).** *Bonus-Malus Systems in Automobile Insurance.* Kluwer Academic. The definitive treatment of tenure-based reward/penalty systems. Progressive discounts for stability, progressive penalties for claims.

- **Rochet, J.-C. & Tirole, J. (2003).** "Platform Competition in Two-Sided Markets." *Journal of the European Economic Association*, 1(4), 990-1029. Why one side must be subsidized for platform adoption. The theoretical backbone for voluntary exchange adoption.

- **Klemperer, P. (1987).** "Markets with Consumer Switching Costs." *Quarterly Journal of Economics*, 102(2), 375-394. How artificial switching costs change equilibrium behavior. Directly relevant to relocation fees as designed friction.

- **Cramton, P. (2002).** "Spectrum Auctions." In *Handbook of Telecommunications Economics*. Upfront deposits, activity rules, and forfeiture mechanisms in the FCC's auction design.

---

*Part of the [Vector Space](/vector-space) series. june@june.kim*
