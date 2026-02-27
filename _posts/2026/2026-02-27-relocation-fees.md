---
layout: post
title: Relocation Fees
tags: coding
---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I directed the argument; Claude worked through the mechanism design and drafted prose.*

*Part of a series: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap) · [Keywords Are Tiny Circles](/keywords-are-tiny-circles)*

---

The first post in this series flagged an [open problem](/power-diagrams-ad-auctions): advertisers in a power diagram auction have an incentive to lie about where they belong.

VCG payments make it dominant strategy to bid truthfully — you can't profit by lying about what an impression is *worth*. But advertisers don't just choose a bid. They choose *where to plant their flag*. And VCG does nothing to prevent a sneaker company from declaring their center at the densest traffic point in the space instead of at "running shoes" where they actually belong.

This is the Hotelling problem. In 1929, Harold Hotelling showed that two competing ice cream vendors on a beach will both converge to the center, even though spreading out would serve customers better. The incentive to capture more foot traffic overrides the incentive to serve your natural customers well. In embedding space, the same dynamic plays out: every advertiser drifts toward the peak of impression density, territory boundaries churn constantly, and the equilibrium — if one exists — is a turbulent mess.

The solution is the same one that prevents every store in a city from clustering at the same intersection: **it costs money to move.**

## Why VCG Isn't Enough

VCG payments solve one dimension of truthfulness. If Nike's true value for an impression at point *x* is $5, VCG makes it optimal to bid $5. The mechanism aligns the bid with the value.

But the center point is a separate strategic variable. Nike's true ideal customer lives at (0.6, 0.3) in embedding space — runners with moderate purchase intent. Impression density peaks at (0.5, 0.4) — general fitness with high purchase intent. If Nike declares (0.55, 0.35) as their center, they pick up denser traffic at the cost of slightly worse relevance per impression. VCG charges them more per impression (because they're now competing with advertisers who genuinely belong near the density peak), but the volume increase can still make the move profitable.

This is position manipulation, and it has three downstream effects:

1. **Convergence to the center.** Every advertiser runs this same calculation. Collectively, they drift toward the density peak. Territory boundaries thrash as everyone jockeys for the same region.

2. **Underserved edges.** The periphery of embedding space — niche topics, unusual intents, long-tail queries — loses advertiser coverage. Users asking about ultrarunning nutrition or minimalist trail shoes see no ads, not because no advertiser cares, but because every advertiser abandoned that territory to chase the center.

3. **Unstable budgets.** When territories shift every time a competitor moves, budget forecasting breaks down. Spend depends on geometry, geometry depends on everyone's position, and everyone's position is in flux. The "equilibrium" is a limit cycle, not a fixed point.

VCG keeps bids honest. Nothing keeps positions honest. That's the gap.

## Moving Costs

Real estate solves this problem without mechanism design theory. Moving your store costs money. Lease termination fees, buildout costs, signage, logistics, customer notification. These costs aren't a market failure — they're what makes the market work. A coffee shop doesn't relocate to the busiest corner every time foot traffic shifts because the relocation cost exceeds the marginal traffic gain.

The result: businesses spread out. The system is efficient not despite friction but because of it.

In embedding space, moving a center point costs the platform nothing. A database write. The advertiser's flag moves from (0.6, 0.3) to (0.55, 0.35) and the power diagram recomputes in milliseconds. Zero friction. And zero friction is why the Hotelling problem appears.

![Hotelling drift vs. relocation fees](/assets/10_relocation_fees.jpg)

The fix: charge a **relocation fee** proportional to the distance moved.

```
relocation_fee = λ · ||c_new - c_old||²
```

Nike wants to move from (0.6, 0.3) to (0.55, 0.35). Distance squared: (0.05)² + (0.05)² = 0.005. With λ = $10,000, that's a $50 fee. Small enough to not block legitimate refinement. But scaling quadratically: moving all the way to the density peak at (0.5, 0.4) costs (0.1)² + (0.1)² = 0.02, or $200. Moving from "running shoes" to "general health" — a distance of 0.3 — costs $900. The further you drift from your natural position, the more it costs, and the cost grows faster than the distance.

## Why Quadratic

The power diagram score function is quadratic in distance:

```
score(x) = log(bid) - ||x - center||² / σ²
```

The benefit of moving your center closer to a high-traffic point is proportional to how much it improves your average score across impressions — which scales with the square of the distance moved. A relocation fee that's also quadratic in distance means the cost of gaming tracks the benefit of gaming. For any λ above a threshold, position manipulation is unprofitable at every distance, not just at large jumps.

Linear fees would only prevent large relocations. An advertiser could take a series of small steps, each individually cheap, that add up to a large drift. Quadratic fees make each step proportionally more expensive than its marginal benefit. You can't game incrementally because the incremental cost matches the incremental gain.

## Pure Platform Profit

The relocation fee goes straight to the platform's bottom line. No cost of goods sold — the advertiser writes a check, the center point moves. Margin: 100%.

This isn't a tax on advertising. It's a tax on *moving*. An advertiser who plants a flag on day one and never moves pays nothing. An advertiser who experiments with small adjustments pays small fees. Only an advertiser who repeatedly relocates across large distances — which is the exact behavior the mechanism is designed to discourage — pays a meaningful amount.

The platform has an incentive to set λ correctly because the fee is a Laffer curve. Too low: position manipulation persists, the market is unstable, advertisers leave. Too high: legitimate experimentation is suppressed, new advertisers can't explore the space, the platform collects fees but loses long-term demand. The platform maximizes revenue by setting λ at the point where position manipulation is unprofitable but honest exploration is cheap.

This is the same incentive structure as real estate transfer taxes. Governments set them high enough to discourage speculative flipping but low enough to allow genuine transactions.

## What It Fixes

### Budget Pacing

The first post identified budget pacing as unsolved: "your spend depends on the geometry of all competitors. Nike raises their bid, Peloton's territory shrinks, Peloton's budget drains slower, Peloton bids higher, Nike shrinks back."

With relocation fees, positions are sticky. Competitors still adjust bids — bids have no switching cost, and shouldn't, because VCG already handles bid truthfulness. But territorial boundaries shift only when someone pays to move or adjusts their bid. Bid adjustments are bounded and predictable. Position jumps are rare because they're expensive.

An advertiser's budget forecast becomes: "My territory is approximately stable. My win rate depends on competitors' bids, which change incrementally. My spend next month looks like this month, plus or minus 15%." That's the same predictability keyword advertisers have today. It's what makes budgets signable.

### Equilibrium

The open question from the first post: "does the game it creates converge to something stable, or is embedding-space advertising inherently turbulent?"

Without relocation fees, the strategy space is infinite-dimensional and frictionless. Every advertiser can move anywhere at any time. This is a continuous game with no reason to converge — the equilibrium, if one exists, could be a limit cycle or chaotic attractor.

Relocation fees add friction that damps oscillation. The game becomes a *potential game* — each move has a direct cost that makes most moves unprofitable. The only profitable moves are those where the gain from improved position exceeds the relocation fee, which shrinks the set of rational moves to a finite, typically small set.

In practice: most advertisers find a good position within a few adjustments, settle in, and compete on bid alone. The few who relocate pay for the privilege and absorb the cost. The system converges not because the math forces it but because the economics make standing still the default rational choice.

### Budget Depletion Cascades

The first post described a fragility: "Territory shifts continuously with bids, but budget depletion is discontinuous — you either have budget or you don't. This mismatch creates oscillation."

Relocation fees make territory shifts rare events instead of continuous drift. When an advertiser depletes their budget and drops out, their territory gets absorbed by neighbors. But those neighbors don't simultaneously relocate to claim it — relocation costs more than the temporary windfall is worth. They benefit passively through expanded territory at their existing position. When the depleted advertiser recharges, they return to their original position.

The cascade that the first post worried about — depletion → territory shift → neighbor bid adjustment → further depletion — is broken because the middle step (territory shift via relocation) has a price. Bids adjust, but positions don't, and bid adjustments alone produce bounded, predictable territory changes.

## What It Doesn't Fix

Relocation fees address position truthfulness, not every open problem in the series.

**Information asymmetry.** The platform still sees all N bid vectors. Each advertiser still sees only their own metrics. Relocation fees don't change this. If anything, they give the platform another lever — "our data suggests you'd perform better at position X" becomes a recommendation that costs money to follow, making the platform a paid advisor as well as a landlord.

**Content steering.** The platform's incentive to steer conversations toward high-value neighborhoods is unaffected. Relocation fees are about advertiser behavior, not platform behavior. A separate mechanism — auditable answer independence, or regulatory oversight — is still needed.

**Anisotropic preferences.** Relocation fees apply to center-point movement. They don't address the harder representation problems: how to express directional preferences, how to clear auctions with elliptical value functions, how to make non-isotropic preferences incentive-compatible. Those remain open.

## Calibrating λ

The relocation fee coefficient λ needs to be high enough to prevent gaming but low enough to not freeze the market. Three signals for calibration:

**Impression value density.** If the densest point in embedding space generates $10 CPM and the average generates $2 CPM, the maximum gain from relocating to the peak is roughly $8 per thousand impressions. At 100K impressions/month, that's $800/month. Setting λ so that a full relocation to the peak costs more than $800 makes the move unprofitable on a monthly basis.

**Advertiser tenure.** New advertisers are still finding their position. They should face low fees for the first N moves — a discovery period, like a new tenant's first month free. After the discovery period, full fees apply. This prevents the fee from blocking market entry while still preventing ongoing manipulation by established players.

**Market velocity.** If the embedding space itself is shifting — seasonal trends, cultural events, product launches — positions that were optimal last month may not be optimal this month. The fee should be set relative to the natural rate of market change, not so high that it prevents legitimate adaptation.

The platform doesn't need to get λ exactly right on day one. Start with a fee that's clearly too low — high enough to be nonzero, low enough to not affect anyone. Monitor position stability. Raise λ until Hotelling drift stops. The optimal λ reveals itself in the data: it's the lowest value at which average relocation distance per advertiser per month stabilizes.

## The Lease Analogy, Completed

The first post compared embedding space to real estate. This post completes the analogy.

| Real Estate | Embedding Space |
|------------|----------------|
| Location | Center point in embedding space |
| Lot size | Reach parameter σ |
| Rent | VCG payments per impression |
| Lease break fee | Relocation fee (λ · distance²) |
| Property value | Impression density at location |
| Zoning | Brand safety restriction zones |
| Moving costs | What prevents every store from clustering at the busiest intersection |

Every column now has an entry. The mechanism is complete: VCG for pricing, power diagrams for allocation, relocation fees for stability. Keywords are [tiny circles](/keywords-are-tiny-circles) that expand via σ. Positions are sticky because moving costs money.

---

*Previously: [Power Diagrams for Ad Auctions](/power-diagrams-ad-auctions) · [Buying Space, Not Keywords](/buying-space-not-keywords) · [The $200 Billion Bottleneck](/embedding-gap) · [Keywords Are Tiny Circles](/keywords-are-tiny-circles). If you're working on this problem, I'd like to hear from you — june@june.kim.*
