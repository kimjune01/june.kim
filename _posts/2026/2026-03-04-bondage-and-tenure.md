---
layout: post
title: "Bondage and Tenure"
tags: vector-space
image: "/assets/bondage_and_tenure.jpg"
---

![Bondage and tenure](/assets/bondage_and_tenure.jpg)

[How to Trust Advertisers](/how-to-trust-advertisers) solved entry. Payment history, reviews, business registration: a composite signal that's expensive to fake. A plumber with three years of clean Stripe history and 200 Google reviews can enter the auction and plant his flag at "emergency pipe repair." No gatekeeper approved him. His commercial identity is the pledge.

That handles the first flag. What about the second?

A national plumbing franchise reads the same post and sees opportunity. One verified identity, thirty flags. "Emergency pipe repair," "water heater installation," "sewer line replacement," "drain cleaning," every residential plumbing query in the space. Each flag has a real business behind it. The trust signals are legitimate. But thirty flags from one entity crowd out thirty independent plumbers who each serve one niche.

The composite signal stops scammers. It doesn't stop land grabs. This is the keyword-era strategy of occupying every position you can afford, replicated in embedding space.

## One Flag Is Free

Your first position costs nothing beyond the commercial identity you already have. The payment processor did KYC and the review platforms accumulated customer feedback. If you serve poorly, chargebacks rise, reviews tank, the composite signal degrades. Your identity is at risk every day you operate.

A new business shouldn't need to post capital to place its first ad. The [trust signals](/how-to-trust-advertisers) handle legitimacy.

## The Second Flag Costs Money

Paul Milgrom won the [2020 Nobel Prize](https://www.nobelprize.org/prizes/economic-sciences/2020/popular-information/) for designing the FCC spectrum auctions. One of his mechanisms: upfront deposits determine how much of the resource you can claim. One license, one deposit. Ten licenses, ten deposits. Refundable if you follow through.

The same mechanism in embedding space: each additional position beyond the first requires a refundable entry bond. The plumber who operates one shop and serves one niche posts no bond. His identity is his bond. The franchise that wants thirty positions posts twenty-nine bonds.

The bond is locked capital, recovered after a stability period. For a legitimate chain that actually operates thirty locations with thirty specialties, the bonds are temporary costs. For a land-grabber squatting on positions they don't serve, the bonds are permanent capital drain. They'll never stabilize because the positions don't match real operations.

```json
{
  "positions": [
    {
      "embedding": [0.23, -0.41, 0.87, ...],
      "sigma": 0.15,
      "bond_status": "waived",
      "reason": "primary_position"
    },
    {
      "embedding": [0.55, 0.12, -0.33, ...],
      "sigma": 0.20,
      "bond_status": "active",
      "bond_amount": 5000,
      "refund_eligible_round": 192
    }
  ]
}
```

The bond should be low enough that posting it is always cheaper than creating a fake identity. The [composite trust signal](/how-to-trust-advertisers) is the Sybil defense: faking a three-year payment history, 200 reviews, and a business registration costs more than any reasonable bond. If the bond exceeds that threshold, you've pushed rational advertisers toward identity fraud instead of compliance. The FCC calibrates upfront deposits to roughly 2-5% of expected total spend. That's a reasonable starting point.

Ethereum's proof-of-stake adds a refinement worth borrowing: the correlation penalty. If multiple positions from the same identity reset simultaneously, the forfeiture scales quadratically. One reset costs 1x. Five coordinated resets cost 25x. Organized squatting becomes unprofitable even if individual bonds are cheap.

## Identity Binding

Entry bonds only work if identities are hard to create. Without identity binding, the franchise creates thirty separate accounts, each getting a free first flag.

Google solved this in 2023. Their Advertiser Identity Verification program requires government-issued IDs, business incorporation documents, and payment credentials. Cross-account detection uses billing details, device fingerprints, IP patterns, and behavioral analysis. A new email address is trivial. A new business registration with a new credit card from a new IP address using a new device is expensive. The cost of creating a convincing identity exceeds the cost of posting the bond.

For an open protocol, identity binding must be portable across exchanges. The pragmatic version: bind identity to payment credentials. Same credit card across exchanges means same identity chain. The hash is computed inside the TEE. The exchange never sees the raw credential.

```json
{
  "identity_hash": "sha256(payment_credential + business_id)",
  "position_count": 3,
  "bonds_posted": 2
}
```

Two exchanges running the same attested code compute the same hash for the same advertiser. Position count follows the identity, not the account.

## Tenure

Nobody likes paying [relocation fees](/relocation-fees). And fees hit newcomers hardest: a new advertiser searching for the right position moves frequently while discovering where they belong, and pays relocation fees at every step. The veteran who already found their spot pays nothing. The fee penalizes exactly the exploration that produces good positioning.

Tenure discounts flip this. Instead of charging for movement, reward staying put. Newcomers are free to explore without penalty. Once they settle, the discount accumulates. The effect on long-run positioning should be similar to fees, but the psychology is different. A discount feels earned. A fee feels punitive.

The closest analog is insurance. Jean Lemaire formalized bonus-malus systems in 1995: policyholders earn progressive premium discounts for each claim-free year. A driver with 10 years of no claims pays 40-60% less than a new driver. Filing a claim resets the discount. Equity vesting schedules follow the same shape. Beyond these, the prior art is thin. Nobody has studied tenure discounts in auction markets.

The idea in embedding space: an advertiser who holds the same position for 200 rounds accumulates a fee discount. The discount is a financial asset. Whether this actually stabilizes positions in a live auction is untested.

This interacts with the entry bond. A new entrant posts a bond and starts with no discount. Over time, the bond is refunded and the discount grows. A long-tenured advertiser with a recovered bond and a 70% discount is paying less than a new entrant. Resetting means restarting at 0%, even if the identity binding is imperfect.

## Why Exchanges Adopt

Exchanges can't be forced to run this code. They have to want to.

Rochet and Tirole [formalized this in 2003](https://www.jstor.org/stable/40005175). In a two-sided market, adoption requires that one side sees clear benefit. Visa subsidized consumers through rewards until consumer adoption forced merchant acceptance. The demand-side critical mass made non-participation more expensive than compliance.

Exchanges that enforce bonds and tenure have better inventory. When each position is backed by either a commercial identity or locked capital, squatters are priced out and the remaining advertisers are differentiated. DSPs route more demand to exchanges with better match quality, which increases publisher revenue.

The exchange without these mechanisms gets the squatted inventory: thirty flags from one franchise, all serving generic responses regardless of the query. DSPs route demand elsewhere.

The [simulation data](/synthetic-friction) on relocation fees points in this direction: embeddings with fees earn surplus of 2.416 per round vs 2.155 without. Entry bonds and tenure haven't been simulated yet. The [simulation is open source](https://github.com/kimjune01/openauction). If you can show that tenure discounts stabilize positions as well as flat fees, or that they don't, I want to see the results.

## How the Pieces Fit

| Problem | Defense | Prior Art |
|---|---|---|
| Scammers entering | Composite trust signals | Payment networks, review platforms |
| One identity, many flags | Entry bond per additional position | FCC spectrum auctions (Milgrom, 2000) |
| Many identities, many free flags | Identity binding (credential hash) | Google AIV (2023) |
| Coordinated squatting | Correlation penalty | Ethereum PoS slashing (2022) |
| Account resets to dodge fees | Tenure discount (bonus-malus) | Insurance industry (Lemaire, 1995) |
| Exchange defection | Inventory quality loop | Rochet & Tirole (2003) |

Commercial identity handles entry. Entry bonds handle the land grab. Identity binding prevents circumvention, and tenure rewards staying put. Each mechanism has decades of deployment behind it. The assembly is new. The pieces aren't.

## References

- **Milgrom, P. (2000).** "Putting Auction Theory to Work: The Simultaneous Ascending Auction." *Journal of Political Economy*, 108(2), 245-272. Upfront deposits determine eligibility in FCC spectrum auctions. The deposit scales with how much of the resource you claim.

- **Douceur, J.R. (2002).** "The Sybil Attack." *IPTPS*. Prevention requires either a central identity authority, social trust, or economic cost.

- **Lemaire, J. (1995).** *Bonus-Malus Systems in Automobile Insurance.* Kluwer Academic. Progressive discounts for stability, progressive penalties for claims.

- **Rochet, J.-C. & Tirole, J. (2003).** "Platform Competition in Two-Sided Markets." *Journal of the European Economic Association*, 1(4), 990-1029. Why one side must be subsidized for platform adoption.

- **Klemperer, P. (1987).** "Markets with Consumer Switching Costs." *Quarterly Journal of Economics*, 102(2), 375-394. How artificial switching costs change equilibrium behavior.

- **Cramton, P. (2002).** "Spectrum Auctions." In *Handbook of Telecommunications Economics*. Upfront deposits, activity rules, and forfeiture mechanisms in the FCC's auction design.

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude researched prior art and drafted prose.*

*Part of the [Vector Space](/vector-space) series.*
