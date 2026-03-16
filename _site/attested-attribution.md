A plumber pays Google $50 every time someone clicks his ad. Last month, 200 clicks, $10,000. He got 3 calls. He asks Google which clicks were real. Google says: all of them. He asks which ones came from people actually looking for a plumber. Google says: trust us. He has no way to check. He pays anyway.

![Attested attribution](/assets/attested-attribution.jpg)

That's attribution in digital advertising. Every participant in the chain reports their own numbers. Nobody can check anyone else's math. Any ad exchange can dial up revenue on demand because nobody can audit the meter.

## Everyone Cheats

When a click happens, the industry has two ways to track it. Both are broken.

*The publisher can lie.* UTM tags let the publisher append tracking parameters to the destination URL. The exchange has to trust that the publisher's SDK reported the right source and the right impression. The publisher controls the tag. The publisher can write whatever they want.

*The exchange can lie.* Redirects route clicks through the exchange's server before reaching the advertiser. The exchange logs the event. The publisher has to trust that the exchange attributed the click to the right slot and the right publisher. The exchange controls the redirect. The exchange can count whatever they want.

*Third parties can hijack.* UTM tags sit in the browser where anyone can overwrite them. PayPal's Honey extension [did exactly this](https://fortune.com/2024/12/23/honey-extension-scam-drama/). A YouTuber drives a viewer to a product page through an affiliate link. At checkout, Honey's popup appears. When the user clicks it, Honey silently overwrites the creator's affiliate cookie with its own. The creator drove the sale. Honey took the commission. By the most trusted name in fintech. Last-click attribution made this trivial: whoever touches the cookie last gets paid, regardless of who brought the customer.

These aren't edge cases. An Adalytics audit found that [80% of Google's TrueView video ad placements violated its own standards](https://adalytics.io/blog/invalid-google-video-partner-trueview-ads). Facebook [admitted](https://fortune.com/2018/10/17/advertisers-facebook-video-metrics/) to overstating average video watch time by 60 to 80 percent for two years. The Methbot operation ran [$3 to $5 million per day](https://krebsonsecurity.com/2016/12/report-3-5m-in-ad-fraud-daily-from-methbot/) in fake video impressions through legitimate exchanges. Ad fraud is an [$84 billion problem](https://searchengineland.com/ad-spend-lost-ad-fraud-2023-432610). Whoever controls the measurement controls the story.

When the lead costs $50 and the margin is thin, "trust me bro" is not a measurement strategy.

## Three Signed Handshakes

TEE attestation makes each step in the attribution chain verifiable by every participant. The chain has three phases. Each phase produces a signed receipt. The next phase checks the signature before proceeding. If any receipt is tampered with, the chain breaks and everyone knows it.

*Key issuance.* Before any ads are served, both the exchange and the publisher generate keys inside their TEEs and publish attestation certificates proving the keys were created in trusted hardware. Both sides can verify the other's keys before a single impression runs.

*Serve.* When the exchange selects a winning ad, it signs a receipt: which creative, which slot, what time, which device. The publisher verifies the signature and countersigns. Both parties hold a matching record. The receipts are sequenced, so neither side can inflate or suppress the count.

*Click.* The user clicks. The publisher signs a click receipt that chains back to the serve receipt. The exchange verifies the chain. No valid serve receipt, no attributed click. You can't fabricate a click for an impression that was never attested. The click receipt carries a signed timestamp that proves priority, so attribution goes to whoever brought the impression first. A late-arriving extension can't backdate a signature. Honey's hijack wouldn't work.

The only data that moves through the chain is timestamps and hashed device identifiers. Enough to prove the same device was present at each step, and useless for profiling. Both sides store their copies. Either side can audit the other's claims. No third-party arbitrator needed.

## Opt-In Ads Compress the Chain

In traditional display advertising, the impression happens passively. The user may or may not have seen the ad. Viewability is a probabilistic guess, so the first link in the attestation chain is already weak.

In [opt-in conversational ads](/the-easiest-sale), the handshake happens at creative-serving time. The user asked a question. The system found a relevant match. The ad appears as a suggestion the user can accept or ignore. The impression is an intentional act, so every link in the chain carries real signal.

Opt-in ads are naturally click-through events. The serve and the engagement are tightly coupled. The attestation chain from serve through click is a single continuous handshake instead of two disconnected events separated by hours of uncertainty.

The publisher doesn't need another dashboard to benefit from this. The signed receipts sit in existing systems and only matter when there's a dispute. Most of the time, the chain runs silently and the publisher collects revenue. When a discrepancy surfaces, the receipts are already there.

## What Changes

Today, a publisher tells the exchange "I showed your ad" and the exchange tells the advertiser "your ad got clicked." Tomorrow, both statements come with cryptographic proof.

Every fraud case above exploited the same structural weakness: the entity reporting the measurement was the entity with the incentive to inflate it. Nobody in adtech is fixing this. Fuzzy attribution is rent. Every middleman claims credit, and the advertiser can't prove otherwise.

This chain proves the click was real. Proving it led to a sale is the next problem.

The [ad exchange running inside a TEE](/the-last-ad-layer) already proves the auction was fair. Extending attestation to the full attribution chain is the same architecture applied to every link.

One exchange has to do it first. Once one does, the plumber's next question to Google changes. Instead of "which clicks were real?" it becomes "why can't you prove it like they can?"

---

*Written with Claude Opus 4.6 via [Claude Code](https://claude.ai/claude-code). I outlined the chain; Claude drafted the protocol.*

*Part of the [Vector Space](/vector-space) series.*
