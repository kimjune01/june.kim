---
layout: post
title: "It Costs Money to Move"
tags: adtech
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude worked through the mechanism design and drafted prose.*

*Part of the [adtech](/adtech) series.*

---

The first post in this series flagged an [open problem](/power-diagrams-ad-auctions): advertisers in a power diagram auction have an incentive to lie about where they belong.

VCG payments make truthful bidding dominant — you can't profit by lying about what an impression is *worth*. But advertisers don't just choose a bid. They choose *where to plant their flag*. VCG does nothing to prevent a sneaker company from declaring its center at the densest traffic point in the space instead of at "running shoes" where it actually belongs.

This is the Hotelling problem. In 1929, Harold Hotelling showed that two ice cream vendors on a beach will both converge to the center, even though spreading out would serve customers better. In embedding space, the same dynamic: every advertiser drifts toward the peak of impression density, territory boundaries churn, and the equilibrium — if one exists — is turbulent.

The solution is the same one that prevents every store in a city from clustering at the same intersection. It costs money to move.

## The Gap VCG Leaves

Nike's true ideal customer lives at (0.6, 0.3) in embedding space — runners with moderate purchase intent. Impression density peaks at (0.5, 0.4) — general fitness with high purchase intent. If Nike declares (0.55, 0.35) as its center, it picks up denser traffic at the cost of slightly worse relevance. VCG charges more per impression, but the volume increase can still make the move profitable.

Three downstream effects:

1. **Convergence.** Every advertiser runs this calculation. Collectively, they drift toward the density peak. Boundaries thrash.

2. **Underserved edges.** Niche topics — ultrarunning nutrition, minimalist trail shoes — lose coverage. Not because no advertiser cares, but because every advertiser abandoned that territory to chase the center.

3. **Unstable budgets.** Spend depends on geometry, geometry depends on everyone's position, everyone's position is in flux. Budget forecasting breaks down.

VCG keeps bids honest. Nothing keeps positions honest. That's the gap.

![Hotelling drift vs. relocation fees](/assets/10_relocation_fees.jpg)

## Moving Costs

Real estate solves this without mechanism design theory. Moving your store costs money — lease termination, buildout, signage, logistics. A coffee shop doesn't relocate to the busiest corner every time foot traffic shifts because the relocation cost exceeds the marginal gain. Businesses spread out. The system is efficient not despite friction but because of it.

In embedding space, moving a center point costs nothing. A database write. The power diagram recomputes in milliseconds. Zero friction is why the Hotelling problem appears.

The fix: charge a relocation fee proportional to the distance moved.

```
relocation_fee = λ · ||c_new - c_old||²
```

Nike moves from (0.6, 0.3) to (0.55, 0.35). Distance squared: 0.005. With λ = $10,000, that's $50 — small enough for legitimate refinement. Moving all the way to the density peak costs $200. Moving from "running shoes" to "general health" costs $900. The cost grows faster than the distance.

Quadratic, not linear, because the score function is quadratic in distance. The benefit of gaming scales with d². A fee that also scales with d² means the cost of gaming tracks the benefit at every distance, not just large jumps. An advertiser can't game incrementally — each small step costs proportionally as much as a large leap.

## Why Platform-Level Fees Don't Work

I wrote the above and thought it was solved. Then I thought about it in the context of [the open protocol](/keywords-are-tiny-circles) — `embedding_model`, `sigma`, substrate-agnostic geometry — and realized the mechanism breaks.

If position vectors are portable across exchanges (which they must be for the open standard to work), an advertiser can discover their optimal position on a zero-fee platform, then port that vector to a fee-charging exchange at no cost. The relocation didn't happen on the fee-charging exchange. It happened elsewhere. The fee is unpayable because the drift is invisible.

This is inherent to the open standard. The same property that makes embeddings substrate-agnostic — any exchange can interpret `[0.23, -0.41, 0.87, ...]` in `openai/text-embedding-3-large` space — also makes position history platform-specific and therefore unenforceable. Platform A charges for movement. Platform B doesn't. The advertiser optimizes on B, bids on A. The fee evaporates.

A platform-level relocation fee is a tariff in a free-trade zone. It only works if you close the borders. An open protocol means the borders are open by design.

## The Protocol Layer

The fee has to live in the protocol, enforced by the exchange's TEE — not by any single platform's policy.

Here's how. The exchange running inside a [TEE](https://github.com/cloudx-io/openauction) (AWS Nitro Enclaves, attestable auction code) computes the relocation fee as part of the auction clearing. The advertiser's position history is an input to the fee calculation, stored as a cryptographic commitment — a hash of each previous center point and timestamp. The exchange can verify cumulative drift without seeing the advertiser's full bidding history. The position commitment travels with the bid, across exchanges, as a protocol field:

```json
{
  "embedding": [0.23, -0.41, 0.87, ...],
  "embedding_model": "openai/text-embedding-3-large",
  "sigma": 0.15,
  "position_commitment": "sha256:a1b2c3...",
  "prior_center_hash": "sha256:d4e5f6...",
  "drift_distance_sq": 0.005
}
```

The TEE verifies that `drift_distance_sq` is consistent with the transition from `prior_center_hash` to the current embedding. If the advertiser lies about their drift, the commitment check fails and the bid is rejected. The fee `λ · drift_distance_sq` is computed inside the enclave and deducted from the bid before scoring.

The critical property: no platform can waive fees for preferred partners or charge extra to suppress competitors. The fee schedule is in the attested code. Everyone sees it. The hardware proves it runs unmodified.

This is the same enforcement model as the [score function](/keywords-are-tiny-circles) itself — `log(b) - d²/σ²` is only trustworthy if the exchange proves it's evaluating it correctly. Relocation fees are just another line in the same attested code.

## What This Fixes

**Budget pacing.** Positions are sticky across all exchanges, not just one. Competitors adjust bids (bids have no switching cost, and shouldn't — VCG handles that). But position jumps are expensive everywhere. An advertiser's budget forecast becomes: "My territory is approximately stable. My spend next month looks like this month, plus or minus 15%." That's keyword-level predictability.

**Equilibrium.** Without fees, the strategy space is infinite-dimensional and frictionless. Every advertiser can move anywhere at any time. With protocol-level fees, the game becomes a potential game — each move has a direct cost. Most advertisers find a good position within a few adjustments, settle in, and compete on bid alone. The system converges because the economics make standing still the default rational choice.

**Depletion cascades.** When an advertiser depletes their budget and drops out, neighbors absorb the territory passively — they don't relocate to claim it because relocation costs more than the temporary windfall. The cascade the [first post](/power-diagrams-ad-auctions) worried about is broken because the middle step has a price.

## Model Updates and Multiple Models

Advertisers don't bid on coordinates. They bid on concepts — "running shoes," "marathon training," "flat feet support" — with a center and a sigma. The exchange embeds those concepts into coordinates using whatever model is active. If the model updates and the vector for "running shoes" drifts, the advertiser's flag doesn't move. The map changed underneath them. The exchange re-embeds the anchor text, the position follows, and the relocation fee is zero because the advertiser's intent didn't change.

Language shifts gradually. Relative positioning — "running shoes" is closer to "marathon training" than to "cooking recipes" — is stable across model versions. An advertiser's competitive neighborhood stays roughly intact even when the underlying coordinates shift. Performance drifts naturally over time the way keyword performance does. No re-anchoring window needed. No grace period. The exchange handles model transitions internally by re-embedding anchor texts.

This requires open-weight models. Not because the model needs to run inside the enclave — the auction is what needs attestation. Embedding is a commodity service. But open weights mean any participant can verify the embedding independently: take the input text, run the model, check the output. The exchange can't quietly swap models or apply proprietary adjustments to the embedding step because the result is reproducible. Open-weight models (Nomic, BGE, GTE, and their successors) make the embedding verifiable without attestation. The embedding becomes infrastructure, not a dependency on one company's API pricing.

Open weights also close the acquisition risk. If the dominant model is proprietary, whoever controls it controls the coordinate system — every advertiser's position, every publisher's inventory classification, every exchange's auction clearing. That's more power than Google has over keyword auctions, because keywords are human-readable strings that don't depend on a neural network. Open weights can be acquired but not recalled. The coordinate system is already public.

Multiple competing models are simpler than they look. Position history is per-model. An advertiser bidding in two different embedding spaces has two independent positions, two separate drift histories, two separate fee schedules. Different coordinate systems, different markets — like stores in New York and Tokyo with different leases. The cryptographic commitment tracks drift within each model across all exchanges that use it. Cross-model "porting" isn't a coherent concept because the positions aren't in the same space.

Multiple models split demand the way multiple currencies split trade. Each model that has active demand requires the exchange to embed every impression in that model and run a separate auction. The exchange can offer embedding as a service — publishers send raw conversation text, the exchange embeds it before the auction clears. The publisher doesn't run inference. But compute still scales with the number of active models. Thin markets clear at lower prices — fewer bidders means worse price discovery and lower publisher revenue. Demand concentrates in the models with the most bidders. The feedback loop narrows the field to one or two dominant models naturally.

The protocol carries `embedding_model` as a field and doesn't pick a winner. The market picks one. The `embedding_model` field means switching remains possible — an advertiser re-embeds their center point in a new model and re-optimizes, losing position history but not infrastructure. If a dominant model stagnates or its maintainers make bad decisions, the market can migrate. No single model is enshrined in the spec.

## The Updated Analogy

The [first post](/power-diagrams-ad-auctions) compared embedding space to real estate. The [previous post](/keywords-are-tiny-circles) added the protocol layer. This one fills in the enforcement column.

| Real Estate | Embedding Space | Enforcement |
|---|---|---|
| Location | Center point | Advertiser declares |
| Lot size | Reach σ | Protocol field |
| Rent | VCG payments | TEE-attested auction |
| Lease break fee | Relocation fee (λ · d²) | TEE-computed, protocol-enforced |
| Property records | Position commitment | Cryptographic hash chain |
| Property value | Impression density | Measured by exchange |
| Zoning | Brand safety zones | Platform policy |
| Transfer tax enforcement | Fee schedule | Attested code, auditable |

The mechanism is: VCG for pricing, power diagrams for allocation, relocation fees for stability, TEE attestation for enforcement. Each layer solves one problem and doesn't pretend to solve the others.

---

*Part of the [adtech](/adtech) series. june@june.kim*
