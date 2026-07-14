# The index card

*2026-07-11, the night of the reddit threads. Each item has a done-condition. Weekly metric at the bottom.*

1. **Ship the essay.** It's finished and it's flypaper. Done when it's live and posted where the people in it will see it (r/PPC would eat the "here's the demand, here's the blind spot" framing alive, in a good way).

2. **Talk to ten users this week.** Usernames in hand, profiles checked 2026-07-12:
   - [Ray_Dev_SG](https://old.reddit.com/user/Ray_Dev_SG) — ChatGPT Ads beta walkthrough.
   - [g_hock](https://old.reddit.com/user/g_hock) — early CTR numbers, doesn't know what a good number is.
   - [kaancata](https://old.reddit.com/user/kaancata) — **best target.** Active 3 days ago. Consultant who wired Codex/Claude into client workspaces: Ads API pulls, GA4/GTM audits, CRM offline-conversion uploads. His words: "'Configured' and 'proven with a recent lead' are not the same thing"; "cost per useful lead is the number I care about." Treats the API pull as source of truth, the dashboard as interpretation. Ask what a platform would have to show him to make that inversion unnecessary.
   - [timnewlinppc](https://old.reddit.com/user/timnewlinppc) — active 2 days ago, agency-side. 79-comment r/PPC thread on Google unilaterally changing capped tCPA/tROAS bidding. Five months ago: hand-matching CallRail gclids to converted leads because no export has the join key. The CRM-reconciliation behavior, documented in public.
   - ~~Middle_Teaching7434~~ — **dropped.** Recent history is pure karma-farming (generic feel-good one-liners, duplicate comments, likely LLM-driven). Not interviewable; discount the CPL datapoint.
   - [KangarooFree4442](https://old.reddit.com/user/KangarooFree4442) — replacement, with a caveat. Active 6 days ago, freelance tracking implementer (Dhaka). Builds the CRM → server-side GTM → Google Ads offline-conversion pipe for clients (HubSpot lifecycle-status webhooks carrying gclids). He's the plumber, not the budget owner — he sells the workaround, so ask what clients say when they hire him, not what he'd pay for.
   - ~~watraders~~ — checked and dropped. Founder of LeanPBX (AI voice agents); the "34x ad spend" post is content marketing cross-posted to four subreddits. Vendor, not a sufferer.

   One question, no pitch:

   > You're computing money-out from your own CRM because you don't trust the platform's numbers. What would a new channel have to show you to skip that step?

   Done when ten verbatim answers are written down. Highest information per hour on this list, and the item most likely to get skipped.

   *2026-07-13: ledger opened at [vector-space-interviews.md] — 5/10 from the r/PPC thread, plus a candidate pool from sub search.*

3. **Write the hypothesis to falsify.** Committed 2026-07-13: *an advertiser will repeatedly pay for placement inside an AI conversation when the measurement and the answer-integrity are checkable without trusting the platform.* "Repeatedly" is the load: one dollar proves the machinery, the renewal proves the demand. What counts against it — the two manual tests (codex, 2026-07-13):
   - *Demand:* ten advertisers in one high-intent vertical, offered "pay only for X, reported from your own system, under this settlement rule," deposit or signed pilot before any more infrastructure. Nobody deposits → refuted at the buyer.
   - *Supply:* one conversational surface runs one disclosed placement, settled manually with signed event batches. The surface won't run it, users punish it, or the advertiser declines to renew → refuted at the surface.
   A spreadsheet receipt suffices for the first campaign; the exchange stays frozen until two advertisers compete for the same opportunity or two surfaces need common routing.

4. **Build the smallest checkable artifact.** Not a platform. One conversation, one labeled placement, one receipt proving the answer wasn't shaped by the payment. Small enough to show in a DM to the ten people from item 2. Done when a stranger can check the claim without believing me. *Ungated 2026-07-13: the gate was "shaped by what they say," and they've said it (see [vector-space-interviews.md]) — the receipt must beat the platform's number AND the 30–60-day guess-and-check interval, and survive kaancata's inversion (raw pull as source of truth, dashboard as interpretation). Runs where we already have real traffic; a receipt on unseen inventory proves nothing.*

5. **One advertiser, one dollar.** Not a segment, not a TAM. One Rossmann-shaped business (captive budget, no channel of its own). Done when someone else's money has passed through the checkable thing once.

## The advertiser path (2026-07-13)

Advertisers are simple. Prove ROAS and attribution, validate budget, offer a demo with real traffic. The receipt is the demo; the first campaign is priced so the advertiser risks nothing and the receipt does the convincing. Item 2's interviews retarget from validating pain (validated — the corpus, the folk metrology, retail media pricing the join) to recruiting the item-5 advertiser and the surface with traffic.

## Don't

- Don't build the self-serve dashboard.
- Don't write the moat section.
- Don't compete for the monopolized auction — no SSP, no exchange, no incumbent retrofit. Their refusal to attribute is terrain, not a problem to solve; it's what makes the exit channel sellable.
- Don't study OpenAI's ads business further — its blind spot is stated policy (no ads near health/mental-health/politics; every chatbot that isn't ChatGPT).
- Don't do item 4 before item 2.

## From the two model evals (2026-07-12, Fable + codex, independent)

**Verdict: real, narrow, service-shaped.** Sell the audit run, not the skill. "An executable measurement audit for lead-gen agencies that blocks unproven performance claims." The skill is distribution; the harness is the product.

**Timing:** June 15, 2026 — Google began blocking Ads API offline-conversion uploads for most developers (Data Manager API migration). Every lead-gen agency's offline pipe is being forcibly rebuilt right now. First product scope: Google Ads + CallRail + HubSpot/GHL offline-conversion migration + verification. One deterministic chain. Not Meta, not MTA.

**Interview roles:** kaancata = design partner/competitor (not a buyer; the harness is his moat). KangarooFree4442 = price discovery (ask what one pipe build invoices for, and what breaks after he leaves). timnewlinppc = buyer archetype (pain, can't self-serve, retention depends on proving cost per qualified lead).

**Interview script (bring one real broken account):**
1. Show me the last reconciliation you performed.
2. What decision changed because of it?
3. How many hours did it consume?
4. Which source was treated as authoritative, and why?
5. Walk me through the last NEW channel you tested. What did it show you before you moved budget? What killed it or kept it?
6. The commitment ask, in their currency (access, not dollars): "Give me read access to one account and I'll produce the discrepancy report." Refusal at free = no $1k buyer existed. Acceptance = discrepancy data + join-key bestiary + a relationship.

*Dropped: "Would you pay $1,000 for a verified discrepancy report?" — hypothetical (collects politeness, Mom Test violation) and structurally wrong buyer: advertisers express willingness-to-pay as channel spend, not tooling spend; confirmation is the gate, not the product. Price discovery comes from KangarooFree4442's actual invoices, not survey yeses.*

**Design rules:** LLM never computes authoritative totals — deterministic code computes, model explains; failed invariant returns no headline number. Measure capture coverage BEFORE reconciling (the "70% unverifiable" report reads as failure to the customer). Call it an *evidence bundle*, not a cryptographic receipt — hashing mutable CRM rows is tamper-evidence, not proof the lead was real.

**Kill criteria (~10 conversations):** nobody grants account access even for a free audit; buyers only want more uploads, not validation; each account needs days of bespoke forensics; <half of outcomes have usable join evidence; the report changes no decision (budget, bidding, retention — nothing moves).

**The croupier bridge:** comforting as strategy, honest as evidence. The wedge's output for the thesis is a corpus of dated join-breakage receipts — and Google actively removing external verifiability (Enhanced Conversions black-box matching, Data Manager migration) is the best exhibit yet for born-auditable channels. Bridge becomes credible only when customers say unprompted they'd shift spend for independently verifiable conversion evidence.

**"Verifiable attribution" prior art (checked 2026-07-12):** [AdPriva](https://docs.adpriva.com/) (Horizen ecosystem, testnet beta Nov 2025) — headless JS tag emits HMAC-signed View/Click/ConsentProofs, Merkle-batched, ZK-verified, chain-anchored. Not croupier: HMAC = symmetric = trust the platform; proofs attest cheap browser events from publisher-controlled JS; needs consumer consent app + blockchain. Differentiation sentence: they anchor claims about traffic; croupier makes the conversion itself the proof. [CloudX](https://new.cloudx.io/) (MoPub/MAX founders, $30M Series A 2025, TEE-isolated auctions, "no games being played") anchors claims about the auction — same stack, one layer up, outcomes still untouched. AdPriva anchors traffic, CloudX anchors the auction, croupier anchors the conversion. Risk: crypto-flavored vocabulary pattern-matches to them — always lead with mechanism (blind signatures, costly conversion event, no chain).

**Competitors checked (Fable):** claude-ads (250+ checks, OSS Claude Code skill), google-ads-skills, marketing-skill directories — all platform-side dashboard reading. Nothing does the cross-source join with a blocking validator and row-level evidence. Differentiator is one sentence; don't market as "AI audits your ads" or die of adjacency.

## Copyedit sweep (2026-07-14)

All 46 Feb–Mar posts through the pipeline; edits sit uncommitted in the june.kim working tree. Direct self-contradiction fixes applied in place (synthetic-friction, the-price-of-relevance, marketing-speak-is-the-protocol, attested-attribution, publisher-ux, stone-soup, proof-of-trust). Flagged and still open, by severity:

1. ~~**Adserver privacy leak.**~~ **Done 2026-07-14.** Landed as vectorspace-adserver commit `6fc8861`: server-side user_id/frequency-cap removed, `FrequencyCapLocal` shipped in sdk-web, wire strip in all four SDKs, docs/OpenAPI updated. Verified: go build/test, sdk-web pnpm test + tsc, swift test, pytest all pass; Android sources changed but unverified (no gradle toolchain). publisher-api.md updated to match (capping is client-side, keyed by advertiser).
2. **Spec reconciliation.** The glow indicator is described three different ways (ask-first, publisher-ux, spec.md), and publisher-ux's impression/click event ordering doesn't match the Publisher API. One pass against the code, not the prose.
3. ~~**σ/log(b) formula family.**~~ **Done 2026-07-14**, source of truth the Lean proof (`~/Documents/auction-proof`). buying-space + three-levers: σ has no score-side tradeoff (center score is log(b) for all σ, per `score_at_center`); the tradeoff is payment-side, honest σ dominant (`gaussian_optimality`). room-to-exist: "proximity dominates" qualified with the 2.3-points-per-10x-bid arithmetic and the buyout allowed. power-diagrams: hyperplane boundaries caveated to equal σ; max-entropy claim tightened to mean+variance; "VCG-like" → VCG. price-of-relevance: negative generalist surplus explained (no-loss guarantee applies to the scored value function; b ≤ 1.1 discards the decay term). three-levers keeps the fake-lever conclusion (June's call, confirmed exact: b enters allocation only via σ/√ln(b), the sim implements the sweep as that substitution, Lean tracks the equilibrium claim as S3 pending σ best-response); closing now carries the reparameterization identity, an editor's note on the realization, and routes rent-seeking to relocation fees. price-of-relevance's σ-adaptation open question states the fixed-σ-transient scope explicitly.
4. **Citation misrepresentations** (most recurring failure): NYSE/NASDAQ (says the opposite), Rochet-Tirole and Coase (stretched), Lahaie & Lubin (iterative, not one-shot), Reese's/AP (misstated), MOSAIC Appendix B.2 (missing-players falsely says the paper ignores competing advertisers). All checkable against source.
5. **Legal/factual errors.** free-as-in-fire: CC BY-SA propagating through agent-compiled code fails copyright's idea/expression boundary (17 U.S.C. §102(b)); codex's fix keeps the spec-commons thesis, drops the propagation claim. unredactable: "nobody can patent it" is categorically wrong.
6. **Crypto/TEE overclaims.** croupier conflates blind signatures with confidentiality; bondage-and-tenure's identity binding is naive against card rotation; "the exchange can't see X" exceeds what attestation proves in attested-attribution, beyond-text, the-last-ad-layer.
7. **Wording fixes, already resolved in principle.** Gaming gap: auctions filter on willingness-to-pay, not truth (the-last-signal, room-to-exist). Relocation-fee exploit: stepwise fees close it. the-price-of-relevance's negative VCG surplus needs to be either fixed or stated as a modeling choice.
8. **trustworth self-contradiction.** "Depth creates stickiness" vs. public portable attestations — the switching cost only holds if attestations expire or stay proprietary; the post establishes neither. Its fraudlogix citation also reportedly contradicts the claim it supports.

Unverified codex assertions to check before acting: vectorspace-adserver's `make dev` not starting the embedding sidecar, mutable `:latest` Docker tags, unpinned embedding model revision — all reasoned from the post text, never checked against the repo.

## Weekly metric

Conversations with people who have the pain. Not words written, not features built. A week without one didn't count.

---

*Thread sources: [r/SEO search](https://old.reddit.com/r/SEO/search?q=AI+overviews+traffic&restrict_sr=on&sort=top&t=year) · [r/PPC search](https://old.reddit.com/r/PPC/search?q=ChatGPT+OR+%22AI+overviews%22+traffic+OR+performance&restrict_sr=on&sort=top&t=year) · [r/Blogging search](https://old.reddit.com/r/Blogging/search?q=traffic+AI+google&restrict_sr=on&sort=top&t=year)*
