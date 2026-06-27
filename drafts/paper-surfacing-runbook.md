# Paper surfacing runbook — Verifiable Knowledge + Hypothesis Graph

A repeatable workflow for getting a paper into the right niches. One canonical node (arXiv) fans out to many channels, each needing the same content reshaped. Split: **push** (self-submit, reliable, low-trust) vs **pull** (be present, probabilistic, high-trust). Fire as a *burst* on announce day (recency boost), not a drip.

## Status

- **VK** — submitted (`submit/7746104`), in moderation queue, expected announce ~Wed eve ET. Title: *Verifiable Knowledge: A Protocol for Trustless Agents*. cs.AI, CC BY-SA 4.0.
- **HG** — submitted, in moderation queue. Title: *The Hypothesis Graph: A Verifiable Semantic Memory for Coding Agents*. cs.AI (+ cs.SE cross-list if allowed).
- Both PDFs/blog live on june.kim; Marchal citation fixed.

## The differentiated one-liner (the sentence the convergent work can't say)

Reuse verbatim across every channel. This is the hook.

- **VK:** Knowledge as a three-state entitlement ledger with the *kill condition as structure*, witnessed by replay from a party that need not trust the author — not attestation, not receipts, not debate.
- **HG:** A semantic memory for coding agents whose value is *accountability* (a checkable contract), demonstrated by — but not reducible to — a capability lift. Externalize the XOR: the context window is the wrong place to compute a difference against truth (cost, latency, and correctness).

Lead with accountability/contract. The lift is the hook, never the headline.

## Phase 0 — assets (stage BEFORE announce)

- [ ] One-line hook per paper (above)
- [ ] Plain-language thread (X / LW-ready), ~8 beats, ending on the differentiator
- [ ] Blog crosspost already live (✓) — ensure abstract carries niche search terms (see v2 backlog)
- [ ] One money-shot figure each (VK: triangulation or replay-regress; HG: the lift table or inquire-skill)
- [ ] Repo READMEs point at the arXiv paper (abductor, hygraph-mechanism ✓)

## Phase 1 — canonical record (do once, permanent)

- [ ] arXiv announced (VK pending, HG to submit)
- [ ] Google Scholar profile (aggregates both under your name; makes citations visible)
- [ ] Semantic Scholar author claim
- [ ] alphaXiv claim + seed a discussion note

## Phase 2 — push channels (self-submit, on announce day)

- [ ] **HF Daily Papers** (huggingface.co/papers/submit) — AK + community curate. Biggest general reach. **Gated:** must have a *claimed* paper on HF to submit. Chicken-and-egg as a first-time author. Sequence: announce → HF paper page appears → claim authorship via ORCID `0009-0005-3153-9396` → verification → submit. Not announce-night; spread over days (submission window is multi-day, ~6d seen). Fallback: a peer with submit rights can submit it for you.
- [ ] **GitHub awesome-lists** — PR into `masamasa59/ai-agent-papers`, plus an `awesome-LLM-agents` / `awesome-AI-safety` list. One-line entry. Durable + agent-scrapable.
- [ ] alphaXiv discussion (from Phase 1)

## Phase 3 — pull channels (be present; feeds human curators)

> **Own-voice only.** LW/AF (and X, to a degree) detect and penalize AI-written prose — posting it backfires. Write these yourself. AI assist limited to: beat skeleton, raw contrast material, fact-check, and subtractive de-tic passes (`/humanize`, `/em-dash`, `/not-but`) on your own draft. HF blurbs and list entries are paper-factual and lower-stakes.

- [ ] **LW/Alignment Forum post** leading with the differentiator. Primary target thread: *What's important in AI for epistemics?* Contrast angle for ELK (you sidestep activation-reading with a replayable external check) and Debate (replay-of-a-check vs trade-of-assertions).
- [ ] **X thread** (the AK/HF + researcher ecosystem)
- [ ] **Substantive comments** on 2–3 adjacent threads/papers (list below) — useful, not promotional
- [ ] **Useful-not-cold outreach** to the few authors you extend: lead with a specific critique or a found gap, not an introduction

Human curators who read LW (reach them via presence, not email):
- **AI Safety at the Frontier** (aisafetyfrontier.substack.com + LW) — monthly highlights, exactly your area
- **Zvi Mowshowitz**, *Don't Worry About the Vase* — weekly roundups, huge AIS reach
- **Import AI** (Jack Clark), **ML Safety Newsletter** (CAIS) — broader

## Phase 4 — synchronous (durable reach)

- [ ] Workshop submissions (NeurIPS/ICLR/ICML co-located: LLM agents, evaluation, AI safety, multi-agent). Track deadlines.
- [ ] Talk pitches to lab reading groups / seminars

## Phase 5 — tend / compound

- [ ] Fold engagement feedback into v2
- [ ] Cite-forward in the next paper (the parallel-agents-via-hygraph project)
- [ ] Track who picks it up; nurture into next month's roundups

## Adjacent papers to engage (comment / cite / contrast)

- *Gaming the Judge: Unfaithful CoT Can Undermine Agent Evaluation* — arXiv:2601.14691. **Ammo for VK** (self-attestation insufficient, measured). Cite in v2.
- *Verify Before You Commit: Faithful Reasoning via Self-Auditing* — arXiv:2604.08401. **Contrast** (self-audit can't confer entitlement). Name and break.
- *Tool Receipts, Not ZK Proofs* — arXiv:2603.10060. Convergent infra; VK adds the semantic ledger.
- *Right to History: Verifiable AI Agent Execution* — arXiv:2602.20214. Provenance stack you argue past.
- *A Protocol for Trustless Verification Under Uncertainty* — arXiv:2507.00631.
- *Architecting Trust in Artificial Epistemic Agents* (Marchal et al.) — arXiv:2603.02960. Already cited.

## v2 backlog (bundle, don't churn per-item)

- [x] Marchal citation: title + unquote "verification crisis" (their phrase is "robust falsifiability")
- [ ] Standard-term abstract scan — ensure niche search vocabulary present (agent memory, self-verification, LLM-as-judge, specification ambiguity, verifiable reasoning) for human + agent retrieval
- [ ] HG §method: state the *necessity* version, not just efficiency — in-window XOR is computed against belief, not truth (cost + latency + correctness)
- [ ] Cross-cite the two papers by arXiv id once both announce

## Announce-day copy — HF Daily Papers submitter notes

Submit by arXiv ID (auto-pulls title+abstract); needs HF account + authorship claim. These are the "why this matters" notes. No em-dashes / tic constructions; voice-check before posting.

**Hypothesis Graph:** The hypothesis graph is a semantic memory for coding agents that holds reasoning as testable claims (nodes) wired to the conditions that refute them (edges), so any conclusion is checkable by replaying one recorded trial, with no trust in the author. On a single contamination-free bug, externalizing the comparator carried Sonnet 4.6 to a fix the strongest released model (Fable) could not reach on its own. Accountability is the contribution; the capability lift is the existence proof that the externalized check does real work.

**Verifiable Knowledge:** LLM agents cannot be held accountable: their reasoning vanishes with the context window, and a self-attested "done" is bitwise indistinguishable from a confident lie. Verifiable knowledge makes every claim carry a falsifiable check another agent can replay to the same verdict, so entitlement comes from re-running the check, not from trusting the author. A three-state ledger (true / false / untrue) plus replay by a distrusting party lets a population of agents share a canon without a gatekeeper.

## Structural notes

- **Push is automatable, pull is trust-bound.** The push half (format adaptation, submissions, list PRs, thread drafts) is mechanical and on-thesis to automate. The pull half resists automation for the same reason an LLM-judge can't be the oracle: credibility in a community isn't manufacturable. Candidate dogfooding project: an agent that runs the push half and hands you the pull half as queued human actions.
- **Vocabulary per channel.** Same content, but match each niche's terms; coinages ("methodeutics", "entitlement ledger") make you memorable but invisible to search unless paired with the standard concept.
- **Vividness beats benchmarks on this axis.** A crisp n=1 (weak-beats-strong; two agents reconcile a contradiction) travels further than a mediocre bench, and it's the only currency the accountability axis trades in.
