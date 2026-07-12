# Adtech Is an Accounting Problem — beats

*Vector Space post. Audience: ad practitioners and CFO-shaped readers. Thesis: the industry does statistics because it lacks source documents. Modeling is what you do without receipts.*

*Written 2026-07-12, out of the reddit-profiles night. Sits between [receipts-please] and [adtech-from-1887]; cites [impressions-and-clicks] for the demand side. Survived a codex + Fable adversarial pass 2026-07-12; narrowings below are deliberate.*

*The narrowed thesis, post-review: delivery is audited; outcomes are not; outcomes are what the money follows. Don't claim "no audit exists" anywhere — claim the audit stops at the loading dock.*

## Opening: the spreadsheet that was never hard

- Settlement is simple in principle. Spend per campaign in the left column, tagged arrivals in the right column, join, sumproduct. A business owner can build it in an afternoon. It is an accounting identity, not a model. (Say "settlement" or "tracking," NOT "attribution" — attribution smuggles in causation, which no spreadsheet answers; that distinction is handled explicitly later.)
- So why is there an incrementality tier charging $50k+ a year, a hundred courses on conversion tracking, and an agency lead spending months fishing gclids out of CallRail URL columns by hand?
- Because neither column holds still, and one of them is written by the parties being graded.

## The ledgers (the core section — every player keeps books, no two reconcile)

Walk the same single conversion through every ledger that records it. One customer clicks an ad and buys. Count the books it lands in. (Prose discipline for this section, from the reception test: for the practitioner this walk is their Tuesday — recognition, not information — so compress the walk and spend the words on the punchline. And every entry leads with the accounting noun, adtech noun in parenthesis, never the reverse — the CFO is reading this section too.)

1. **The platform's ledger** (Google Ads / Meta dashboard): claims the conversion, on its own attribution window, its own dedup rules, increasingly *modeled* — an estimate booked as a record. Precision matters here: the platform invoices for clicks and impressions at auction prices; the modeled conversion is not the invoice line. It is what tCPA/tROAS *spends against* and what the renewal is justified by. The goods receipt, not the bill — written by the seller.
2. **The analytics ledger** (GA4): same conversion, different number. GA4 and Google Ads disagree *with each other* — same company, two ledgers, 20-30% gaps treated as normal, and Google's own support docs explain why they can never balance. (One sentence in prose; don't elaborate the semantics — the reception test flags this nuance as the skimmed part.)
3. **The call tracker's ledger** (CallRail): the call happened, scored qualified — exported without the gclid. The join key to ledger #1 is missing by design. (Receipt: timnewlinppc's r/PPC thread, months of hand-matching via landing-page URL columns.)
4. **The CRM ledger** (HubSpot/GHL/Salesforce): the only ledger that knows if the lead became money. Knows nothing about which ad. Join key arrives only if someone plumbed a webhook to carry it.
5. **The agency's ledger** (the monthly report): a curated projection of ledger #1, produced by a party paid by ambiguity.
6. **The affiliate network's ledger**: last-click claims, rewritable at the checkout moment. (Honey receipt, stated precisely: the extension won last-click credit it didn't earn; 146k of ~181k listed stores had no affiliate partnership or consent at all. The 146k is the no-consent count, not an attribution-rewrite count.)
7. **The advertiser's bank statement**: the one honest ledger. It only knows money-out.

- Punchline of the section: **every player keeps single-entry books about the same transactions.** Within each firm, double-entry, controls, auditors. Between firms — where the money actually moves — zero shared entries. Nobody's ledger is anyone else's counterparty record. There is no trial balance for the industry because the columns don't share a key, a window, or a definition of the event.
- kaancata's line as the practitioner's summary: "'Configured' and 'proven with a recent lead' are not the same thing."

## Fraud vs. mark-to-model (keep the two diseases separate)

- Auditing standards (ISA 240) split every wrong number into *error* (unintentional) and *fraud* (intentional). Real fraud lives in the ecosystem: click farms, bot impressions, MFA arbitrage, Honey's last-click capture — intentional fake entries, ~$84B/yr (Juniper 2023, forecast $100B by 2026), with a whole vendor tier (DoubleVerify, CHEQ, HUMAN) chasing it. Spend "cooking the books" only where it's literally true (Honey).
- The platforms' disease is different: **the mark without the controls.** Marking to model is ordinary, legal finance — ASC 820 Level 3 fair value; every bank does it quarterly. What finance learned from Enron was not to abolish the mark but to cage it: a disclosure hierarchy that flags Level 3 estimates, disclosed unobservable inputs, independent price verification, auditor model testing. A modeled conversion is a Level 3 estimate with none of the cage: no flag distinguishing it from an observed record, no input disclosure, no independent verification of the model — and the modeler is the counterparty spending your budget against it. Enron appears exactly once, as illustration of what the uncaged mark did, not as the argument. (This framing survives the CFO reader who marks to model every quarter; the naked Enron comparison does not.)
- The asymmetry, narrowed to what's defensible: the industry polices fake entries at the *delivery* layer and has no mechanism for self-serving estimates at the *outcome* layer. The verification tier has seen the truck at the dock; it has never seen whether anyone bought anything.
- The auditability line, corrected (the old "unfalsifiable" version dies against the eBay holdout study — Blake, Nosko & Tadelis 2013 falsified platform attribution claims by turning paid search off; geo holdouts do it routinely): platform outcome claims are **unauditable entry by entry, falsifiable only in aggregate, at $50k+ per act**. The incrementality tier is the market price of a single act of falsification. That's what missing source documents cost: not "you can never know," but "knowing anything costs a study."

## The receiving dock advertising used to have

- The claim is NOT "advertising never had controls" — it had them first. The Audit Bureau of Circulations, 1914: advertisers founding an independent auditor for publisher-claimed circulation. Broadcast ran on *notarized affidavits of performance* — a station officer attesting under oath that the spots aired; agencies paid against the affidavit, not the station's say-so. An attested goods receipt. Advertising invented the delivery audit.
- Digital dismantled it. Not all of it — and here's the steelman, conceded in full because it sharpens the thesis: MRC accreditation covers Google's clicks, served impressions, viewability, IVT filtration. DV/IAS measure rendering from outside. Advertiser-side ad servers produce independent impression counts; publisher-vs-advertiser discrepancy reconciliation with contractual thresholds and makegoods is standard on guaranteed buys. Ebiquity and MediaSense audit agency contracts.
- Now read what that list covers: **all of it is delivery-side.** Did an ad render, was it viewable, was the traffic human. Google's MRC accreditations conspicuously do not cover conversions or attribution. The dock exists for impressions; there is no dock for outcomes — and outcomes are what tCPA spends against, what renewals are justified by, what the entire budget follows. The three-way match runs PO → receiving report → invoice; adtech has the first and last and a seller-written middle *for the only metric that decides the money*.
- The four questions, as an organizing ladder. **PROMOTE THIS: make it a real table, visually distinct, EARLY in this section, designed screenshot-shaped** — the reception test says the post's forward-ability IS this table plus one line. Caption it: "Delivery is audited; outcomes are not; outcomes are what the money follows." (A practitioner forwards a link + a screenshot + "this is what I've been telling you"; this table is the screenshot.)
  1. Was media delivered as contracted? → well-controlled: MRC, verification, makegoods.
  2. Did a conversion occur? → the advertiser's own CRM/transaction record.
  3. Which media touched it? → the missing join; the seven-ledger problem lives here.
  4. Did the media cause it? → only experiments answer this; no receipt ever will.
  The post's territory: rows 2-3 are unjoined, and platform dashboards deliberately blur rows 3 and 4.
- History beat, one line: audit demand grows with *distance* between payer and counter (agency → programmatic → auto-bidding → PMax, maximal by design), and the scandals are accumulating on schedule (ANA — stated precisely: ~36 cents of every dollar *entering a DSP* reaches a human, Dec 2023; Adalytics; Honey). The audit layer isn't overdue. It's repealed.
- The enforcement half-beat (verified 2026-07-12): regulators attack the visible interface because it's the only one that generates evidence — labels, banners, claims, all screenshot-able. Two attempts on the counting layer prove the frontier. 1963-64: the Harris hearings caught ratings services fabricating figures; the industry pre-empted regulation with what became the MRC, whose audit perimeter froze at what 1964 could verify — delivery — and never moved. 2018-present: DZ Reserve v. Meta — Potential Reach inflated 200-400%, eight years, no verdict, and the metric at issue is still only an audience estimate, not the outcome ledger. **The enforcement frontier is the auditability frontier.** Receipts don't compete with regulation; they're its prerequisite.
- Deadpan personal closer for the beat (verified — both PayPal notices in hand): the Facebook Consumer Privacy User Profile Litigation settlement administrator has paid me my full share of the Cambridge Analytica case — $725 million, the largest privacy class action settlement in U.S. history, eight years from filing to my inbox. It came to $42.03, in two installments: $35.30 on October 14, 2025, and a residual $6.73 on June 23, 2026. Note the craft: the administrator ran a multi-round distribution with a true-up to get my forty-two dollars exactly right — a more diligent reconciliation than the industry it was punishing runs on a trillion. I have the receipts. They're the only ones this industry has ever sent me.
- The timeline kicker, one breath only (two clever codas halve each other — the $42.03 beat keeps its full weight, this gets a single sentence): the residual cheque landed eight days after Google closed the offline-conversion path. Litigation cycles in eight years; the counting layer redesigns itself in a quarter.

## The reductio: if corporate finance worked like adtech

*Dramatize the missing outcome-side controls by porting adtech's norms into ordinary corporate finance. Deadpan, one norm per line. Every line must be a faithful translation — one unfair line licenses the reader to dismiss the device. Six lines maximum: the reception test found the device fatigues around line five (pallet-scoreboard and redesigned-pipe lines already cut as the fourth and fifth instances of a gotten pattern). Supplier-dock opens, railway lands:*

- Your supplier's delivery confirmation is written by the supplier, and there's an independent inspector at the loading dock — but the metric your renewal depends on is "units that increased your profit," and that number the supplier calculates itself, by a method it doesn't disclose, and updates while you sleep. (Platform-modeled outcomes behind MRC-audited delivery.)
- The bank sends no statement for the account that matters. It sends a performance dashboard where the figure is *modeled*, the model's inputs are the bank's, and the dashboard's own help page explains why it will never match your books. (Modeled conversions; the GA4/Ads discrepancy docs.)
- The performance calculation that decides your biggest vendor's renewal is defined by that vendor, and the definition changes via a help-center article. (Attribution windows; the tCPA/tROAS change announced in a support doc.)
- Quarterly close: your controller downloads seven CSVs with no shared key, and the reconciliation procedure is a YouTube course updated whenever the counterparty renames a column. (The curriculum.)
- No officer ever certifies the outcome numbers. Delivery gets audited, contracts get signed, makegoods happen — but the figure the money actually follows carries no attestation, no liability, and no restatement, because there is no record to restate. (No certification regime for attributed outcomes — the narrow, true version.)
- The landing beat: **this arrangement has been tried.** UK railway-mania accounting — self-reported earnings, owner far from operator — collapsed into the Companies Act 1900's mandatory audit after enough scandals, not out of virtue. (Keep the anchor UK-specific; US mandatory audit is 1933-34.) Corporate finance doesn't work like adtech because controls made honesty cheaper than fraud. Same species, different instruments.

## Steelman: the platforms' defense, conceded and answered

- Give the defense its full weight, in the platforms' own best terms: conversions happen in systems platforms can't observe; ATT, GDPR, and cookie death destroyed the join keys, and modeling is the legally compelled patch (Meta's conversion modeling is explicitly an ATT response); deterministic records are not automatically truer — tags fail, CRM stages are dirty, uploads are biased; the models are disclosed, validated against observed conversions, confidence-thresholded; real-time bidding can't wait for audited revenue; and independent verifiers can't have user-level data because privacy constraints are real, not a convenient excuse.
- Concede nearly all of it. Then the two answers that survive every concession:
  - Validation: the models are validated — *by the modeler*. Nothing in the defense establishes that the platform should be the sole producer, validator, reporter, and optimization-spender of the KPI that decides its own revenue.
  - Privacy: the tension between privacy and auditability is an artifact of the join being identity-based. It exists because the receipt was never designed. A blind-signature coupon proves the conversion happened and which batch it came from without identifying the customer — *more* private than hashed-email Enhanced Conversions, not less. Privacy is the platforms' best argument and the coupon's best on-ramp. (This is the post's one addition that converts the strongest objection into the fix's motivation. Link 1887 for mechanism.)

## Modeling is what you do without receipts

- MTA, MMM, incrementality studies: inference machinery. Inference is what you're forced into when you don't have source documents. The industry does statistics because the accounting is impossible, and calls it methodology.
- The platforms' answer to the missing join is to move the join *inside*: Enhanced Conversions matches hashed identity in a black box; June 15, 2026, offline-conversion uploads migrated to the Data Manager API. Stated precisely: an ingestion-path migration, no export removed, the advertiser keeps its own records. What the payer loses is the ability to recompute the *match* — the platform's join of your data to its claims happens where no outside party can replay it. The books stay on both sides; the reconciliation moved inside one of them.
- Where modeling is legitimate: optimization. Bid on models, learn on models. Where it is not: the record the money follows. (Holmström split — settle on what's verifiable, model for everything else. One sentence, link out.)
- The counterfactual concession, placed HERE and not three sections later: a receipt proves the touch and the conversion, never the cause. Receipts don't replace incrementality testing — they give it uncorrupted inputs. You cannot run causal inference on forged data. **Source documents constrain the model; they cannot replace the counterfactual.**

## The curriculum teaches feeding, not auditing

*(Reception test: this is the practitioner's section — the one aggregate fact about their own profession that daily pain doesn't teach. Highest landing-per-word in the post; don't keep it short out of modesty.)*

- The empirical check on "the outcome audit doesn't exist": look at what the industry teaches itself. Class Central lists 100+ courses on conversion tracking; MeasureSchool, Analytics Mania, and every mid-tier agency publish complete guides.
- Read the syllabus (softened from absolutes — one counterexample kills "not one," so phrase as a challenge): the taught canon is overwhelmingly **upload-side** — capture the gclid, store it in the CRM, fire the webhook, push your conversion truth INTO the platform so its bidding optimizes better. A reconciliation course — check what came back against your books — I could not find. If one exists, send it to me; its absence at hundred-course scale is the point either way.
- The curriculum churns on Google's schedule: ECL replaced gclid-only, the enhanced-conversions settings merged April 2026, the API path moved June 15. Every flagship tutorial carries "(updated for 2026)" because the platform keeps invalidating the textbook. A procedure has to track the platform's renames forever; a receipt is true regardless.

## The new channel ships with no dock at all

- Every delivery-side auditor works from one assumption: there is an inspectable artifact. A served page that can be crawled, a tag that can be wrapped, a pixel that can be verified. MRC viewability, DV/IAS — all inspect the artifact from outside.
- An ad inside an AI conversation has no artifact. The impression is a sentence in a private chat. No page to crawl, no tag to wrap, no third-party script inside the answer. Even the delivery-side audit — the half advertising still has — has no line of sight here.
- Receipts from the field:
  - Koah ("AdSense for GenAI," $20M+ raised): claims 7.5% CTR, ~$10 eCPMs, $10k first-month publisher earnings — every number self-reported. Don't claim "zero reviews exist" (an absence claim one blog post kills); the stronger fact is that there is *no verification surface on which an independent review could stand*. Nothing to accredit, nothing to wrap, nothing to crawl.
  - Nobody has defined the units. What is an "impression" inside a generated answer — the brand was named? Recommended? Compared favorably? The line between a labeled placement and a paid answer is a JSON field in the network's server.
  - OpenAI's own terms: "ChatGPT's answers stay independent." A promise checkable by no one outside OpenAI (cite impressions-and-clicks).
  - The nearest audit tool is synthetic-prompt monitoring (Profound, Scrunch et al.) — polling the model with test questions. That's not auditing the books; that's calling the store to ask if your ad ran.
- Important narrowing (survives the "platforms could offer logs/attestations/TEEs" objection): no-verification-surface is a *product-design choice*, not a technical inevitability — which is precisely the point. The old channel's dock was demolished; this one was never poured. Retrofitting a periscope is impossible here; the only audit this channel can ever have is one designed into the payload. The receipt rides in the answer or it doesn't exist.
- The escalation line: the old channel audits delivery and takes outcomes on faith. The new one takes *both* on faith.

## What reconciliation looks like when it's designed in

- The Monday-morning beat, BEFORE the coupon paragraph (reception test: without this, the practitioner finishes converted and idle, and idle readers don't forward). Practice under the current regime, derivable from the frame itself: treat the bank statement and the CRM as your only books, and everything platform-side as unaudited counterparty claims; label modeled numbers as estimates in your own client reporting; price one act of falsification (a holdout) into the annual budget.
- Leave one instrument dangling as a question the reader answers themselves (a frame lands when the reader gets to make a move unaided): **who is the advertiser's controller for media spend?** Ask it, don't answer it. The reader who arrives at "nobody — and the agency is the bookkeeper with a conflict" has proven the frame works on their own.
- The fix is boring on purpose: source documents, counterparty records that agree by construction, independence of the counter from the counted. Not smarter statistics — statistics with honest inputs.
- The coupon is the receiving report, scoped honestly: advertiser-signed at issuance, presented at conversion, verifiable by anyone — proof of touch and redemption, never of causation. (Link adtech-from-1887, croupier — one paragraph, don't re-explain the crypto.)
- The batch ledger is the shared trial balance: batch ID, Merkle root, batch size, redemption count. Deterministic formula, public inputs, anyone can replay. Two parties, one record, nothing to reconcile because the entry *is* the counterparty record.
- Closing pressure, two ratchets:
  - Transparency is irreversible. The first channel that offers an outcome-side receiving report forces every other channel to explain to a CFO why it won't. CFOs already believe in three-way match; nobody has to sell them the concept, only the dock.
  - The buyer is becoming software. Ad buying is going agentic (agent-to-agent auction protocols are already being drafted), and "trust me bro" doesn't parse for a buying agent evaluating machine-checkable claims. Automation on top of unreconciled books doesn't fix them; it launders them faster — and the buying agents' owners will figure that out. In an agent-mediated market, receipts stop being a preference and become a protocol requirement.
- Final line candidate: the books were always the product. An ad channel is a claim about what happened to money; the first channel whose claim checks itself is not a better dashboard, it's a different kind of ledger.

## Candidate lines (use or lose)

- "Modeling is what you do without receipts."
- "Every player keeps single-entry books about the same transactions."
- "Delivery is audited; outcomes are not; outcomes are what the money follows."
- "MRC accredits the impression; nobody accredits the conversion."
- "The dock existed; digital demolished it. The audit layer isn't overdue — it's repealed."
- "The verification tier has seen the truck at the dock; it has never seen whether anyone bought anything."
- "Unauditable entry by entry, falsifiable only in aggregate, at $50k per act."
- "The incrementality tier is the market price of a single act of falsification."
- "The mark without the Level 3 controls."
- "Validated — by the modeler."
- "Column left, column right, sumproduct. The spreadsheet was always right; the data was lying."
- "The books stay on both sides; the reconciliation moved inside one of them."
- "You cannot run causal inference on forged data."
- "Source documents constrain the model; they cannot replace the counterfactual."
- "A procedure has to track the platform's renames forever; a receipt is true regardless."
- "The old channel audits delivery and takes outcomes on faith. The new one takes both on faith."
- "That's not auditing the books; that's calling the store to ask if your ad ran."
- "The receipt rides in the answer or it doesn't exist."
- "Automation doesn't fix the books; it launders them faster."
- "Receipts stop being a preference and become a protocol requirement."
- "The books were always the product." (Reception test: weakest of the lines — aphorism that decorates rather than cashes out. Acceptable closer, first to cut.)

## Don't

- Don't explain blind signatures inline — link.
- Don't cite the parts-bin/Transmit-contract diagnosis beyond one linked sentence (that's the cognition-series post if ever).
- The chatbot section argues auditability only — the demand argument stays in impressions-and-clicks; link, don't re-make it.
- Don't say "attribution" when you mean settlement/tracking; the causation distinction is load-bearing and handled explicitly (four-question ladder + counterfactual beat).
- Don't claim "no audit exists" / "never had it" / "nobody signs anything" — the narrowed versions (outcome-side, officer-certification, repealed dock) are both true and stronger.
- Cut from earlier drafts, deliberately: watraders 34x (one hobbyist's buggy agent indicts that agent, not the ledger structure — the "launders faster" line survives in the agentic-buyer beat); the electricity-meter analogy (the meter is the seller's meter, trusted via regulated metrology — invites the regulation-not-receipts completion); the "name another spend category" dare (cloud billing answers it — AWS invoices off its own meter; if kept, pre-empt: cloud is re-derivable from the customer's own logs, which is exactly the receipt property ads lack); "fraud is falsifiable / unfalsifiable is worse" (dies against eBay 2013).
- Numbers trace to receipts, stated with their bases: ANA 36 cents *of every dollar entering a DSP* (Dec 2023); Honey 146k = stores with no affiliate partnership/consent (of ~181k), NOT an attribution-rewrite count; ad fraud $84B (Juniper 2023, $100B 2026 forecast); Koah ~$10 eCPM (Adweek), $20.5M Series A; "trillion" via WARC/GroupM global ad spend forecast (verify current figure); Measured $50k/yr floor corroborated, $400k top end unverified — drop or verify; Data Manager June 15 via Google dev blog; GA4/Ads gaps via Google's own discrepancy docs; UK Companies Act 1900 for the mandatory-audit anchor (don't extend to US).
- Don't name or dunk on individuals — the post indicts structures. Reddit quotes stay anonymous-by-username.
- The eyeballs-moved elegy (sailing-ship effect) stays OUT — different post's mood; this one is a diagnosis with a fix, not a eulogy.
