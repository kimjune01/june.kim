# Vector Space Series — Distribution Plan

Goal: Find collaborators to build embedding-space ad infrastructure.
Last updated: 2026-03-02

---

## 1. Cold Emails

### Approach
- Short (< 150 words), specific to their work
- Link ONE post that's most relevant to them
- Clear ask: "Would you be open to a 20-minute call?"
- No attachments, no pitch decks

### Tier 1: Building the Pieces

**Andrej Kiska — Kontext**
- Hook: Kontext does real-time LLM analysis for ad placement, but collapses to categories at the protocol boundary
- Post: The $200 Billion Bottleneck
- Ask: How they think about the category collapse problem
- Status: SENT Mar 2 (andrej@kontext.so). No reply.

**Ryan Hudson — ZeroClick**
- Hook: 10K+ advertisers, $55M raised — but reasoning-time injection is one mechanism, spatial auctions are another
- Post: Keywords Are Tiny Circles
- Ask: Whether they've considered continuous-space bidding vs discrete categories
- Status: SENT Mar 2 (ryan@zeroclick.ai). No reply.

**Koah Labs team**
- Hook: "AdMob for AI chatbots" — they're building the SDK, you've simulated the auction
- Post: Keyword Tax (simulation evidence that embedding auctions redistribute surplus to specialists)
- Ask: How their auction mechanism works under the hood
- Status: SENT Mar 2 (nic@koahlabs.com). No reply.

**Seedtag (Madrid)**
- Hook: $250M+ raised, already running embedding-based targeting — closest existing infrastructure
- Post: Power Diagrams for Ad Auctions
- Ask: Whether they've explored spatial auction mechanisms beyond contextual matching
- Status: SENT Feb 27 — two emails (albert@seedtag.com + usa@seedtag.com). No reply. SKIPPING follow-up for now.

**CloudX / Peter Downs**
- Hook: TEE-attested auctions — closest to the full architecture described in the series
- Post: Letter to CloudX (already written for them)
- Status: ACTIVE — in hiring process, pitched embedding auction vision directly. Ongoing conversation.

**PubMatic / Nishant Khatri**
- Hook: SSP making bets on embeddings, NVIDIA partnership for confidential computing
- Post: The Convergence
- Ask: How they see the protocol evolving beyond OpenRTB
- Status: SENT Mar 2 (nishant@pubmatic.com). No reply.

**Criteo / Liva Ralaivola**
- Hook: CLEPR and DeepKNN — why collapse embeddings to IAB categories before auction?
- Post: The Convergence
- Status: SENT Feb 27 (l.ralaivola@criteo.com). No reply.

### Tier 2: Investors

**Tomasz Tunguz — Theory Ventures**
- Hook: Led Koah Series A, ex-Google AdSense — uniquely positioned to evaluate
- Post: Keyword Tax (economics proof that embedding auctions have natural wedge)
- Ask: Whether he sees the embedding-to-category collapse as the bottleneck
- Status: NOT SENT

**M13 Ventures**
- Hook: Led BOTH Kontext and Koah — already betting on the space
- Post: The Last Ad Layer
- Ask: What's missing in their portfolio companies' approach
- Status: NOT SENT

### Tier 3: Researchers & Thought Leaders

**Hajiaghayi et al. (UMD / Google Research)**
- Hook: Their NeurIPS paper on LLM ad auctions via RAG — your work extends their mechanism design
- Post: Power Diagrams for Ad Auctions → linked The Convergence
- Status: SENT Feb 27 (hajiagha@umd.edu). No reply.

**Zhao et al. (Alibaba)**
- Hook: LLM-Auction paper — your simulation validates similar dynamics
- Post: Relocation Fee Dividend
- Status: SENT Feb 27 (zhaochujie.zcj@alibaba-inc.com, cc dagui.cdg@alibaba-inc.com). No reply.

**Ben Thompson (Stratechery)**
- Hook: He called for embedding auction as marketplace mechanism — you built the simulation
- Post: The Last Ad Layer
- Status: SENT Feb 27 (admin@stratechery.com). Draft to ben@stratechery.com unsent. No reply.

**Doc Searls**
- Hook: The Intention Economy — embedding auctions are the protocol he described
- Post: The Last Ad Layer
- Status: SENT Feb 28. REPLIED SAME DAY — detailed line-by-line review. Invited you to ProjectVRM.
- Key feedback: use "customer" not "user", address privacy, plumber test as litmus test.
- Follow-up: You joined ProjectVRM list, posted Mar 1.

**Don Marti**
- Hook: His argument that perfectly-targeted ads are worthless — your signal theory extends this
- Post: The Last Signal
- Status: ENGAGED via ProjectVRM — he responded Mar 1 with substantive questions about dishonest bidders and prebid.js integration. No separate cold email needed.

**Cory Doctorow**
- Hook: Named enshittification — you describe the structural inverse
- Post: The Last Ad Layer
- Status: SENT Feb 28 (cory@craphound.com). No reply.

**Eric Seufert (Mobile Dev Memo)**
- Hook: Writes about ad-supported AI business models
- Post: The Convergence
- Status: SENT Feb 27 (eric@mobiledevmemo.com). No reply.

**Simon Willison**
- Hook: Noted ChatGPT ads, has massive dev/AI audience
- Post: The Plumber Test (most accessible, concrete)
- Ask: Not a collaborator pitch — more "thought you'd find this interesting" for amplification
- Status: NOT SENT

### Tier 4: Platforms & Standards

**Perplexity (Aravind Srinivas)**
- Hook: Killed ads to preserve trust — the TEE architecture solves their exact problem
- Post: Perplexity Was Right to Kill Ads
- Timing: Wait until you have a working prototype or stronger proof point
- Status: NOT SENT — holding

**IAB Tech Lab**
- Hook: AdCP and CoMP working group — your work proposes the missing embedding field
- Post: The $200 Billion Bottleneck
- Status: SENT Feb 27 (techlab@iabtechlab.com). No reply.

### Tier 5: Press & Publications

**Sarah — AdExchanger**
- Hook: Guest column pitch on why sell-side stack can't handle continuous intent
- Post: Power Diagrams for Ad Auctions
- Status: SENT Feb 28 (sarah@adexchanger.com). No reply.

### Other

**Adrian Gropper (HealthURL / MAIA)**
- Status: ENGAGED via ProjectVRM — called your post "dead-on", connected to MAIA TEE project and Phil Windley's authorization server work. Active thread.

**Atlas Research**
- Status: SENT Mar 1 (hi@atlasresear.ch). No reply.

**Matt Palmer**
- Status: Shared series link Feb 28 in existing conversation thread.

---

## 2. Twitter/X Strategy

Status: NOT STARTED

### Thread Candidates (best posts for threads)
Each thread should be 5-7 tweets distilling the core argument.

1. **The Plumber Test** — most accessible, concrete story everyone relates to
   - Frame: "Can a person with a sewage backup find a quality plumber without overpaying? Here's why the answer is still no, and what would fix it."

2. **Keywords Are Tiny Circles** — visual, conceptual, tweetable
   - Frame: "Every keyword auction is actually an embedding auction with σ → 0. Here's what happens when you let σ grow."

3. **The Last Signal** — philosophical, share-worthy
   - Frame: "Every signal on the internet has been killed. PageRank. Reviews. Organic social. Here's the pattern — and the one signal that survives."

4. **Keyword Tax** — data-driven, provocative
   - Frame: "We simulated 10,000 auction rounds. Specialists lose 3.5x more than generalists in keyword auctions. Here's the data."

### Engagement Targets
Reply to and engage with these accounts when they post about relevant topics:
- @stratechery (Ben Thompson) — ad tech, marketplace dynamics
- @simonw (Simon Willison) — AI tools, ChatGPT features
- @doctorow (Cory Doctorow) — enshittification, platform economics
- @donmarti — ad tech, privacy, signal quality
- Ad tech accounts: @AdalyticsHQ, @nichefire
- AI platform accounts: @OpenAI, @peraborgen (Perplexity)

### Hashtags / Topics to Monitor
- #adtech, #programmatic, #OpenRTB
- ChatGPT ads, AI advertising, agentic commerce
- DOJ Google antitrust updates

### Posting Cadence
- 2-3 original threads per week (one per post, distilled)
- Daily engagement: reply to 3-5 relevant conversations
- Quote-tweet relevant news with your framing

---

## 3. LinkedIn Strategy

Status: NOT STARTED

### Post Types
LinkedIn favors longer-form posts with professional framing.

1. **"I spent 4 weeks simulating ad auctions with real embeddings. Here's what I found."**
   - Lead with the Keyword Tax data
   - Professional tone, economics framing
   - Tag: PubMatic, Criteo, IAB

2. **"Perplexity was right to kill ads — but wrong about the solution."**
   - Provocative take that ad tech people will engage with
   - Tag: Perplexity, reference the $20K revenue number

3. **"The $200B bottleneck in AI advertising isn't the model. It's the protocol."**
   - Technical but accessible
   - Tag: IAB Tech Lab, OpenRTB

### Groups to Post In
- Programmatic Advertising & RTB
- AdTech Professionals
- AI in Marketing & Advertising
- Digital Advertising Technology

### People to Connect With
- Ad tech engineers at Google, Meta, Amazon, The Trade Desk
- SSP/DSP product managers
- IAB working group members
- AI startup founders in the ad space

---

## 4. Hacker News

Status: NOT STARTED

### Best Posts for HN (ranked by HN-appeal)

1. **The Plumber Test** — concrete, relatable, anti-Google-ads sentiment plays well
   - Title: "The Plumber Test: Can embedding auctions beat keyword ads for local search?"

2. **The Last Signal** — philosophical, pattern-matching, HN loves signal theory
   - Title: "Every internet signal has been killed — except one"

3. **Power Diagrams for Ad Auctions** — technical, novel, math-heavy
   - Title: "Using power diagrams to partition embedding space for ad auctions"

4. **Keywords Are Tiny Circles** — elegant concept, visual
   - Title: "Keywords are just embedding auctions with σ → 0"

### HN Approach
- Post one at a time, gauge response
- Start with The Plumber Test (most accessible)
- Best timing: Tuesday-Thursday, 9-11am ET
- Be present in comments to engage
- Don't post multiple in the same week

---

## 5. Reddit

Status: NOT STARTED

### Subreddit Mapping

| Subreddit | Best Post | Frame |
|-----------|-----------|-------|
| r/adops | Keyword Tax | "Simulated 10K rounds comparing keyword vs embedding auctions" |
| r/adtech | The $200B Bottleneck | "OpenRTB has no embedding vector field — that's the real bottleneck" |
| r/machinelearning | Power Diagrams | "Using Voronoi/power diagrams for continuous-space ad auctions" |
| r/programming | Keywords Are Tiny Circles | "An elegant mathematical unification of keyword and embedding auctions" |
| r/startups | The Last Ad Layer | "The next ad infrastructure opportunity: embedding-space auctions" |
| r/Economics | Relocation Fee Dividend | "Hotelling competition with relocation fees — simulation results" |

### Reddit Approach
- One post per subreddit per week max
- Build karma in these communities first by commenting
- Frame as "here's what I found" not "here's my blog"
- Be ready to engage in technical discussions

---

## 6. Newsletters & Podcasts

### Newsletter Guest Post Pitches
- **AdExchanger** — PITCHED Feb 28 (sarah@adexchanger.com). No reply.
- **Stratechery** — Ben Thompson emailed Feb 27. No reply.
- **The Information** — AI business coverage, pitch the market analysis angle
- **Import AI** — Jack Clark, AI implications angle
- **Lenny's Newsletter** — marketplace dynamics angle (The Plumber Test)

### Podcast Pitches
- **AdExchanger Talks** — ad tech industry podcast
- **The Ad Tech Podcast** — programmatic advertising
- **Latent Space** — AI engineering podcast (technical angle)
- **Acquired** — business history/strategy (long-term vision angle)
- **a16z podcast** — marketplace/platform dynamics

### Pitch Template (newsletters/podcasts)
"I've been running simulations of ad auctions using real embedding vectors. The results show that the $200B keyword auction market has a structural flaw: it taxes specialists 3.5x more than generalists. I've published the code (github.com/kimjune01/openauction) and a 20-post series on what an embedding-native auction system would look like. Would this be a fit for [your show/newsletter]?"

---

## 7. Sequencing (Week-by-Week)

### Week 0 (Feb 27 – Mar 2) — DONE
- [x] Send researcher emails (Hajiaghayi, Zhao)
- [x] Send industry emails (Criteo, Seedtag x2, IAB Tech Lab)
- [x] Send thought leader emails (Ben Thompson, Eric Seufert, Cory Doctorow)
- [x] Cold email Doc Searls → got detailed reply → joined ProjectVRM
- [x] ProjectVRM thread with Don Marti and Adrian Gropper
- [x] Pitch AdExchanger (sarah@adexchanger.com)
- [x] Email Atlas Research
- [x] CloudX — ongoing hiring + vision conversation

### Week 1 (Mar 2–8) — THIS WEEK
- [x] Send remaining Tier 1: Kontext, ZeroClick, Koah, PubMatic
- [ ] Send Simon Willison email
- [ ] Post The Plumber Test thread on Twitter
- [ ] Post on HN: The Plumber Test
- [ ] LinkedIn post: "I simulated 10K ad auction rounds..."
- [ ] Follow up with ProjectVRM thread (continue Don Marti / Adrian Gropper conversation)

### Week 2 (Mar 9–15)
- [ ] Send Tier 2 cold emails (Tunguz, M13)
- [ ] Post Keywords Are Tiny Circles thread on Twitter
- [ ] Reddit: r/adops (Keyword Tax), r/machinelearning (Power Diagrams)
- [ ] LinkedIn post: "Perplexity was right to kill ads..."
- [ ] Follow up on Week 0 unanswered emails (one follow-up each)

### Week 3 (Mar 16–22)
- [ ] Post The Last Signal thread on Twitter
- [ ] HN: The Last Signal
- [ ] Reddit: r/adtech, r/startups
- [ ] Pitch The Information, Import AI
- [ ] Pitch 2 podcasts (Latent Space, AdExchanger Talks)

### Week 4 (Mar 23–29)
- [ ] Post Keyword Tax thread on Twitter
- [ ] LinkedIn post: "$200B bottleneck..."
- [ ] Follow up on all remaining unanswered emails (final follow-up)
- [ ] Pitch Lenny's Newsletter, a16z podcast

### Ongoing
- Daily Twitter engagement (replies, quote-tweets)
- Weekly LinkedIn post
- Monitor and respond to all comments/replies
- Track which posts/channels generate actual conversations

---

## 8. Outreach Tracker

### Emails Sent

| # | Target | Email | Subject | Date | Response | Next Action |
|---|--------|-------|---------|------|----------|-------------|
| 1 | Prof. Hajiaghayi (UMD) | hajiagha@umd.edu | Your RAG auction paper + the exchange trust problem | Feb 27 | None | Follow up Week 2 |
| 2 | Zhao et al. (Alibaba) | zhaochujie.zcj@alibaba-inc.com | LLM-Auction + exchange infrastructure for deployment | Feb 27 | None | Follow up Week 2 |
| 3 | Liva Ralaivola (Criteo) | l.ralaivola@criteo.com | CLEPR + DeepKNN → embedding-space auctions | Feb 27 | None | Follow up Week 2 |
| 4 | Albert (Seedtag) | albert@seedtag.com | Contextual embeddings → auction layer | Feb 27 | None | Follow up Week 2 |
| 5 | Seedtag USA | usa@seedtag.com | Embedding-space auctions for contextual advertising | Feb 27 | None | — (covered by #4) |
| 6 | IAB Tech Lab | techlab@iabtechlab.com | Input for CoMP Working Group | Feb 27 | None | Follow up Week 2 |
| 7 | Ben Thompson | admin@stratechery.com | The auction mechanism for ChatGPT ads | Feb 27 | None | Follow up Week 2 |
| 8 | Eric Seufert (MDM) | eric@mobiledevmemo.com | Auction mechanisms for LLM ad inventory | Feb 27 | None | Follow up Week 2 |
| 9 | Doc Searls | doc@searls.com | The Intention Economy now has a protocol | Feb 28 | **REPLIED** — detailed review, invited to ProjectVRM | Continue relationship |
| 10 | Cory Doctorow | cory@craphound.com | Enshittification has a structural inverse | Feb 28 | None | Follow up Week 2 |
| 11 | Sarah (AdExchanger) | sarah@adexchanger.com | The untapped LLM intent signal | Feb 28 | None | Follow up Week 2 |
| 12 | Atlas Research | hi@atlasresear.ch | Advertising is the last place for signal | Mar 1 | None | Follow up Week 2 |
| 13 | ProjectVRM list | projectvrm@eon.law.harvard.edu | Forward: Intentcasting now has a protocol | Mar 1 | **Don Marti** + **Adrian Gropper** replied | Continue thread |
| 14 | Peter Downs (CloudX) | peter@cloudx.io | (in hiring thread) | Feb 27 | **Active** — ongoing conversation | Continue |
| 15 | Andrej Kiska (Kontext) | andrej@kontext.so | The category collapse in Kontext's pipeline | Mar 2 | None | Follow up Week 2 |
| 16 | Ryan Hudson (ZeroClick) | ryan@zeroclick.ai | Reasoning-time injection + spatial auctions | Mar 2 | None | Follow up Week 2 |
| 17 | Koah Labs (Nic) | nic@koahlabs.com | OpenRTB has no embedding field | Mar 2 | None | Follow up Week 2 |
| 18 | Nishant Khatri (PubMatic) | nishant@pubmatic.com | Embedding vector field for AI chat bid requests | Mar 2 | None | Follow up Week 2 |

### Emails Not Yet Sent

| Target | Planned Date | Post to Lead With |
|--------|-------------|-------------------|
| Simon Willison | Week 1 | The Plumber Test |
| Tomasz Tunguz (Theory) | Week 2 | Keyword Tax |
| M13 Ventures | Week 2 | The Last Ad Layer |

### Social Posts

| Channel | Post | Date | Engagement | Link |
|---------|------|------|------------|------|
| | | | | |

The goal metric isn't views — it's conversations that lead to calls.
