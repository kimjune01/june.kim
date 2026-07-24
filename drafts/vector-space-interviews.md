# Interview ledger — vector-space item 2

*Ten verbatim answers from people with the pain. Started 2026-07-13. Counting rule: an answer counts if it reveals what they actually do (behavior), not what they'd hypothetically want.*

## Tally: 5 / 10

## Source 1 — r/PPC thread, 2026-07-13

[How do you explain attribution discrepancies to clients?](https://old.reddit.com/r/PPC/comments/1uv7ywg/) — posted as u/grewgrewgrewgrew, outsider framing ("software engineer poking at PPC"). Post at 0 points; mods stickied a "low quality, search the sub" warning. Five substantive answers before it stalled.

1. **u/Glum-Statement9045** (2 pts): "You just pick one source of truth. In your case, the CRM would be the best option." — *Classification: pick-one-and-defend, CRM pole. The coping strategy named without embarrassment.*

2. **u/DReid25** (1 pt): explain attribution to the client through their own multi-device purchase behavior; "painting a picture they can relate to." — *Classification: the explanation is a script, not a document. Answer to "what do you show them" is a story.*

3. **u/No_Stranger91** (1 pt): sets up one source of truth "based on data from the back-end, not by any of the platforms"; starts with "a simple google sheet and capturing utm's, gclid etc." — *Classification: hand-rolled reconciliation. The CallRail-gclid behavior, volunteered unprompted. Best follow-up target in thread.*

4. **u/InformationVivid455** (1 pt): gives clients a touchpoint narrative ("average customer needs X touch points"); claims removal testing: "We tested removing X and saw a drop of percent." — *Classification: informal holdout — the $50k row done by feel. Follow-up: actual holdout or before/after?*

5. **u/Canes4life82** (0 pts): "The true source will always be Google Ads," assuming GTM is set correctly; explains GA4/CRM gaps mechanically (credit splitting, call dedup windows). — *Classification: pick-one-and-defend, platform pole. Defends the platform's books with the platform's own logic.*

**Finding:** nobody produced a reconciliation artifact. Two pick a source (opposite sources), two tell stories, one builds a spreadsheet. Five practitioners restated the thesis without having read it.

**Follow-ups to post in-thread (while alive):**
- No_Stranger91: "When the sheet and the platform disagree, whose number goes in the client report?"
- InformationVivid455: "How did you run the removal test — actual holdout or before/after?"

## Mod-check: was "search the sub" right?

Yes on frequency, and that's evidence, not refutation. Two searches (2026-07-13, past year, r/PPC only):

- "attribution discrepancies" — 7+ threads: platform vs GA4 vs CRM/backend mismatches (PPC_Princess: Meta says 374 forms, Google 71, GA4 says ~110/109; pars-distalis: Google Ads 100 leads, WhatConverts 60; Gwen-2021: Meta 5 purchases, Shopify 2, double-crediting across campaigns).
- "source of truth" — 10+ threads, the phrase is community vocabulary. Sure_Umpire3473 (9 pts, 19 comments): "How do you build a Source of Truth to steer the budget?" — Meta claims ~100% of store revenue. Exurge_Domine_: SOT (GA4) and engine data trend in opposite directions, "How are you supposed to optimize with conflicting data?" zsolesz719 (7 pts, 31 comments): audited inherited account, Stripe is "the actual source of truth," expects reported value to DROP when tracking becomes accurate, smart bidding trained on bad data. Lost_Albatross7593: SKAN/MMP numbers don't match and "my finance team keeps questioning the ROI reports."

**Reading:** the sub relitigates this monthly, per-account, in troubleshooting register, and it never resolves into a method. The recurrence IS the corpus — dated, public join-breakage receipts (essay's evidence appendix material). The mod sticky is itself a datapoint: the pain is so common the sub is bored of it.

**Lesson for the next post:** the well-received versions are asked from inside one account with real numbers (Meta 374 / Google 71 / GA4 110). Outsider industry-framing pattern-matched to low-effort/founder-fishing. Next post, if any, leads with a concrete broken account, not a systems question.

## Finding: guess-and-check on 30–60 day intervals (2026-07-13)

The sub's recommended verification procedure (thread reading, esp. zsolesz719's tROAS transition thread): change something, wait 30–60 days for conversion lag + bid-strategy relearning, compare aggregates. There is no entry-level check; the unit of verification is a month of live budget. The $50k-per-answer row, restated in practitioner currency: knowing costs the interval.

The closed-loop detail (not in the essay): the conversion numbers under test are also smart bidding's training signal. During the guess-and-check window the platform retrains on the disputed numbers, changes delivery, and moves the numbers. Mark-to-model where the model also steers the spend — the bookkeeper sets the budget from his own unaudited entries, and the control is watching whether his totals drift.

Interview question this unlocks (better than script Q5): "When you make a change, how long before you trust the read on it — and what does that waiting period cost the client?" Everyone has an interval; nobody has priced it.

## Finding: folk metrology — precision without accuracy as doctrine (2026-07-13)

Practitioners in these threads argue accuracy vs precision unprompted. The working doctrine: platform numbers are biased but consistently biased, so relative reads (trends, A vs B) are trusted while absolute numbers are not. "Directionally correct" is the sub's epistemology.

The doctrine's hidden dependency: bias stability. Platform model updates (Enhanced Conversions, modeled-conversion changes, attribution defaults) shift the systematic error silently — there is no changelog for the measuring instrument, and the "consistent bias" defense cannot detect when the bias moves. A trend read straddling a silent model update compares two instruments and calls it a trend.

Historical rhyme: fields stuck at accuracy-vs-precision get unstuck via a reference standard (calibration weights, NIST traceability), not better statistics. The receiving dock is the reference artifact. That the community reaches for metrology vocabulary is the demand signal: they know the standard is missing; it's the accounting name they don't have.

Interview probe: "Have you ever caught a platform model update moving your numbers? How did you know it was them and not you?"

## Candidate pool (from search, active past year, have the pain in public)

- **u/zsolesz719** — agency, inherited account, Stripe-vs-GA4 gap big enough to distrust attribution, mid server-side migration. Closest to the buyer archetype; also the June-15-adjacent rebuild in the wild.
- **u/Sure_Umpire3473** — agency-side, Shopify client, "flying blind" allocating between Google and Meta.
- **u/Exurge_Domine_** — SOT and platform disagree directionally; the four-question table as a lived problem.
- **u/PPC_Princess** — three-way mismatch, asks "Is GA4 my bible?"
- **u/Lost_Albatross7593** — iOS/SKAN, finance team questioning ROI: the practitioner→CFO forwarding path occurring naturally.

Plus the original index-card five (kaancata, timnewlinppc, Ray_Dev_SG, g_hock, KangarooFree4442) — still uncontaminated; the essay was never linked in the thread.

## Rules carried over

- No pitch, no essay link in interviews or threads. If asked "is this for a product": "maybe eventually — right now I'm trying to understand why the problem exists."
- DM only as continuation of a public exchange, never cold.
- Their comments in existing threads count toward the ten if they reveal behavior (what they check, what they tell clients, whose number wins).
