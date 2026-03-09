# Croupier vs Northbeam: ML Models vs Mathematical Proof

*March 2026 | Croupier Blog*

Northbeam is a marketing attribution platform that uses machine learning to stitch together customer journeys from first-party signals. Their DNS-level script integration is harder for ad blockers to detect than a standard JavaScript pixel. In October 2025, they launched "deterministic view-through attribution" for verified video impressions.

Northbeam represents the state of the art in model-based attribution. Croupier takes a fundamentally different approach: proof-based attribution.

## How Northbeam Works

Northbeam installs at the DNS level — their tracking script looks like first-party infrastructure to the browser. This gives them better data collection than pixel-based competitors since ad blockers have a harder time distinguishing Northbeam's script from the brand's own code.

Their ML model collects touchpoints across the customer journey and assigns fractional credit. A customer might see a Facebook ad (30% credit), click a Google search ad (50% credit), and convert on a direct visit (20% credit). The model decides the weights.

Pricing starts around $999/month for brands spending under $250K/month on ads, scaling to $2,500+ for larger spenders.

## The Model Problem

Northbeam's model is sophisticated. It's also a black box.

**You can't verify the weights.** When Northbeam says Facebook deserves 30% credit and Google deserves 50%, there's no way to independently check those numbers. The ML model is proprietary. You trust the output.

**Models optimize for plausibility, not truth.** ML attribution models find patterns in data that are statistically plausible. A plausible attribution is not the same as a proven attribution. If the model has a systematic bias — say, it over-credits view-through impressions — every output reflects that bias, and the advertiser can't detect it.

**"Deterministic" still means "Northbeam determined it."** Their new deterministic view-through feature ties verified video impressions to purchases. But "deterministic" here means Northbeam can deterministically link the view to the purchase using their data. It doesn't mean the advertiser can independently confirm the link.

**Platform data is still an input.** Northbeam collects first-party data from its DNS-level integration, but it also imports platform-reported data for ad spend, impressions, and clicks. The model's inputs include self-reported numbers from the platforms being measured.

## How Croupier Differs

Croupier doesn't model attribution. It proves it.

| | Northbeam | Croupier |
|---|---|---|
| Method | ML model assigns credit across touchpoints | Cryptographic signature verifies specific channel |
| Output | Fractional credit percentages | Binary: valid signature or not |
| Verifiable by advertiser? | No (proprietary model) | Yes (check own signature) |
| Multi-touch? | Yes (fractional credit) | Per-channel (one coupon per impression) |
| Accuracy claim | Model-dependent | Mathematical certainty |
| Requires trusting | Northbeam's algorithm | Cryptographic math |
| Pricing | $999-$2,500+/month | Flat monthly relay fee |

The distinction matters most when the numbers disagree. If Northbeam says a channel drove 30% of your conversions and your coupon redemptions show 5%, which number do you act on? The model is a prediction. The coupon is a receipt.

## Where Northbeam Wins

Northbeam provides capabilities Croupier doesn't:

- **Full-journey visualization.** See every touchpoint in the customer journey across all channels.
- **Media mix allocation.** Understand how budget shifts between channels affect overall performance.
- **View-through attribution.** Credit channels for impressions that influenced a conversion even without a click.
- **Real-time dashboards.** Monitor performance across campaigns continuously.

If you need a full marketing analytics platform with cross-channel journey mapping, Northbeam does that. Croupier is narrower: it proves which channels delivered real conversions.

## Where Croupier Wins

- **Cryptographic certainty.** No ML model is 100% accurate. A valid signature is.
- **No black box.** The advertiser verifies their own cryptographic signature. The logic is: valid signature = valid attribution. No algorithm to trust.
- **Hijack-proof.** A signed token can't be overwritten by a browser extension or faked by a bot.
- **No platform data dependency.** Croupier's measurement is entirely independent of platform-reported metrics.

## Using Them Together

The strongest setup: use Northbeam for strategic media planning and Croupier for ground-truth calibration.

Northbeam's model tells you the shape of your marketing funnel — which channels play which roles, where to shift budget. Croupier's coupons tell you the actual conversion rate per channel, verified cryptographically.

Calibrate the model against the proof. If Northbeam's model says Channel A drives 200 conversions/month and Croupier's coupons verify 190, the model is accurate for that channel. If the model says 200 and coupons verify 50, retrain or re-examine.

Models are useful for planning. Proof is necessary for accountability. The best measurement stack has both.

---

*Croupier is a blind relay for cryptographic coupon books. [Learn more](https://github.com/kimjune01/croupier) or [request early access](https://croupier.ad).*
