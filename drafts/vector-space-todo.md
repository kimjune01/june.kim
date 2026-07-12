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

3. **Write the hypothesis to falsify.** Draft: *an advertiser will pay for placement inside an AI conversation if the measurement and the answer-integrity are checkable without trusting the platform.* Done when it's one sentence, committed, with what evidence would count against it.

4. **Build the smallest checkable artifact.** Not a platform. One conversation, one labeled placement, one receipt proving the answer wasn't shaped by the payment. Small enough to show in a DM to the ten people from item 2. Done when a stranger can check the claim without believing me. Do this AFTER item 2 — shaped by what they say, not by what's fun to build.

5. **One advertiser, one dollar.** Not a segment, not a TAM. One Rossmann-shaped business (captive budget, no channel of its own). Done when someone else's money has passed through the checkable thing once.

## Don't

- Don't build the self-serve dashboard.
- Don't write the moat section.
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

**"Verifiable attribution" prior art (checked 2026-07-12):** [AdPriva](https://docs.adpriva.com/) (Horizen ecosystem, testnet beta Nov 2025) — headless JS tag emits HMAC-signed View/Click/ConsentProofs, Merkle-batched, ZK-verified, chain-anchored. Not croupier: HMAC = symmetric = trust the platform; proofs attest cheap browser events from publisher-controlled JS; needs consumer consent app + blockchain. Differentiation sentence: they anchor claims about traffic; croupier makes the conversion itself the proof. Risk: crypto-flavored vocabulary pattern-matches to them — always lead with mechanism (blind signatures, costly conversion event, no chain).

**Competitors checked (Fable):** claude-ads (250+ checks, OSS Claude Code skill), google-ads-skills, marketing-skill directories — all platform-side dashboard reading. Nothing does the cross-source join with a blocking validator and row-level evidence. Differentiator is one sentence; don't market as "AI audits your ads" or die of adjacency.

## Weekly metric

Conversations with people who have the pain. Not words written, not features built. A week without one didn't count.

---

*Thread sources: [r/SEO search](https://old.reddit.com/r/SEO/search?q=AI+overviews+traffic&restrict_sr=on&sort=top&t=year) · [r/PPC search](https://old.reddit.com/r/PPC/search?q=ChatGPT+OR+%22AI+overviews%22+traffic+OR+performance&restrict_sr=on&sort=top&t=year) · [r/Blogging search](https://old.reddit.com/r/Blogging/search?q=traffic+AI+google&restrict_sr=on&sort=top&t=year)*
