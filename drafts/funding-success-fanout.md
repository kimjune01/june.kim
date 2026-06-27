# Fan-out: what makes these funding applications successful

Topic: LTFF / Manifund / Cooperative AI Foundation — success factors, assessed against June's drafts
(`funding-strategy.md`, `ltff-application.md`, `manifund-proposal.md`, `one-pager.md`).

Cycle 1 (k=3): one Opus research agent per funder, sourced from each funder's own writeups.
Converged through codex (adversarial prune). Generic grant advice and overstated/time-sensitive
claims stripped; only funder-specific, sourced criteria survive.

---

## THE CONVERGENT THROUGHLINE (codex-validated, all three funders)

The drafts ask the funder to **trust too much**: trust the private framing (hypothesis graph,
entitlement ledger, typed three-mode loop), trust that an n=1 bug generalizes, trust that SWE-bench
*translation* implies *safety* relevance, trust that the capability lift is really oversight, and
trust that "distrust" means the same thing to every funder.

The fix is to make **distrust the structure of the application**, not just the theme of the project:
state the narrow claim, show exactly what a skeptical evaluator can rerun, separate oversight from
capability gain, and name the next experiment that would falsify the hypothesis. A project about
checkability should itself be maximally checkable on the page.

> Pruned thesis (works for all three, different wrappers):
> *Not a benchmark-performance project — a checkability project. Can externalized, replayable
> reasoning records let a skeptical third party verify agent claims without trusting the model?
> Evidence is promising but thin, so the grant funds a small, falsifiable next step that produces
> public artifacts and directly tests whether hypothesis graphs improve independent oversight.*
> LTFF wrapper: safety + downside control. Manifund: a small concrete person-bet. CAIF: a
> trust/commitment primitive, but only once moved into multi-agent incentives.

**Convergent red flag (LTFF + Manifund, independently):** "externalizing the check carried a weaker
model past the strongest released model" reads as **capability lift**, not oversight. Both funders
discount capabilities-accelerating work. This single line is the highest-shared risk in the drafts.
Reframe: the win is that *an independent, weaker auditor caught what the strong model's own report
missed* — training-free, adds no model capability, strictly an oversight tool.

---

## H1: LTFF — scalable-oversight fit, but the trust-tax is unpaid (codex round 1)

**Verdict:** Dead-center in scope; sinks on an empty track record + n=1 + a capability-lift read.

**Sourced criteria (survived prune):**
- Rewards a *specific causal* theory of change and **demonstrated independent strategic direction** —
  the exact trait they praise in unaffiliated applicants. [LTFF May2023–Mar2024 payout; "Marginal Grant" forum post]
- Rewards concrete **publishable artifacts** (funded scalable-oversight + evals work explicitly). [same]
- Named rejection patterns: **mediocre prior output** (most common), **"buzzwords + endorsements,
  no substance after careful reading,"** and **asserted novelty that's actually a standard subfield
  line** (they investigate and downgrade). [LTFF AUA; "hypothetical narrowly-rejected grants"]
- **Capabilities externality** is an explicit discount. [May2023–Mar2024 payout]
- Outsiders with unfamiliar framing pay a **legibility tax** (insider-bias admission). ["Reflections on my time on the LTFF"]

**Strong in draft:** the oversight/"defeat-device" framing maps to a funded category; DOIs +
preregistration + regrade scripts pre-empt the "no substance" kill; the "cite the 95.3% as
translation or not at all" instinct is exactly the calibration LTFF rewards.

**Funder-specific weaknesses (generic ones pruned):**
- Track-record section is a literal `[Fill in]` placeholder — sitting next to their #1 rejection reason.
- Capability-lift framing of Verus (the convergent red flag above).
- Novelty undefended vs debate / prover-verifier / process supervision / externalized-reasoning-oversight.
  The fix doubles as a *demonstration of field judgment* LTFF weights in early-career applicants.
- Private vocabulary forces decoding — adjacent to the "buzzwords, no substance" surface pattern.

**Codex corrections applied:** the −5..+5/2.9-threshold detail and "currently funding-constrained"
were cut (inside-baseball / time-sensitive, unciteable here). "Solo work is disfavored" softened —
LTFF funds independents; the real issue is *solo + thin track record + private ontology*. "95.3%
provides zero support" softened to *weak/indirect* support for implementation competence.

**Top fixes:** (1) reframe Verus as oversight-demonstration; (2) write the track record AND a
one-paragraph positioning-against-the-subfield; (3) de-jargon, demote deliverable 4 to a stretch
goal — make the *discovery benchmark* the spine, since it's a public good that survives even if the
core bet fails.

## H2: Manifund — "fund people," and the person is a placeholder (codex round 1)

**Verdict:** Right lane (evals/oversight), but the draft starves the one mechanism Manifund runs on.

**Sourced dynamics (survived prune):**
- **"Fund people, not projects"** — regrantors are selected and judged on taste in *people*; the
  bio is the load-bearing part, not boilerplate. [Manifund 2025 regrants writeup]
- **Solo, fast, small, early**: one regrantor commits alone against their own budget, $5k–$50k,
  counterfactual angel money for people "not yet on OpenPhil's radar." [manifund.org/about/regranting]
- **Public backing compounds**: visible early commitment is social proof that eases later
  fundraising and lets others co-fund. (codex softened "social-proof engine" → this.)
- Red flag: **benchmarks that could accelerate capabilities** are explicitly a concern. [AI-safety regrants review]

**Strong in draft:** the one-liner is legible; honesty about the 95.3% + null-reporting hits
"realistic metrics beyond papers"; Verus #2219 is the screenshot-able asset.

**Funder-specific weaknesses:**
- **No ask** (literal `[$X]`). And $75k is a harder *first yes* than the solo-regrant zone — needs
  tranching so one regrantor can make the first move (e.g. "$10k funds the benchmark MVP + n=1→n=5").
- **Bio is a placeholder** — worst possible omission under "fund people." June's real traction (works
  fully in public, 3 DOIs, 27 merged PRs across 9 repos, 43%→91% iteration result) is absent here.
- Capabilities-acceleration read unaddressed (convergent red flag).

**Codex corrections applied:** "coverage lanes" cut as taxonomy decoration unless a specific
regrantor is named; "$75k above the sweet spot" reframed from dispositive to "harder first yes,
so tranche it"; "AI-generated-looking" dropped (generic, not present in the draft).

**Top fixes:** (1) small tranched ask with a first-mover entry point; (2) lead with the person +
real traction; (3) one line neutralizing the capabilities read + the concrete next experiment the
first dollar buys.

## H3: CAIF — real but NARROW fit; current framing overreaches (codex round 1)

**Verdict:** "Their mandate IS agents who don't trust each other" is a stretch. Genuine fit only to
the new $10M multi-agent fund's agent-infrastructure pillar, and only after an incentive argument is added.

**Sourced scope (survived prune):**
- Mandate = **cooperation under mixed motives** (Open Problems in Cooperative AI: understanding,
  communication, commitment, institutions). Funds game-theoretic / MARL work, benchmark
  *environments*, welfare/norm metrics. [cooperativeai.com; arXiv:2012.08630]
- The **$10M fund** (CAIF + Schmidt Sciences + DeepMind + ARIA) has an agent-infrastructure pillar —
  "identity, **reputation**, and **commitment** protocols for secure cross-platform agent
  interaction" — the real opening. [DeepMind multi-agent safety announcement]

**Honest fit:** verification of *correctness* (what June solves) is orthogonal to the *incentive*
problem CAIF centers (why would a self-interested agent submit an honest, checkable record rather
than a plausible lie). A replay ledger a rational defector can simply decline to write honestly
doesn't address mixed-motive defection. Verification can be a cooperation *primitive*; it is not by
itself a cooperation proposal. (codex softened both blunt edges: not "does NOT fund single-agent
verification" but "poor fit unless converted to multi-agent infrastructure.")

**Codex corrections applied:** "Area 3" relabeled to the **agent-infrastructure pillar** (public
language is a pillar, not a numbered area); "honest reporting becomes the dominant strategy" softened
to "an incentive/attack-model argument showing *when* checkable reporting is favored or enforceable" —
the strong version is a major unproven mechanism-design claim.

**Top fixes:** (1) target the $10M fund's agent-infrastructure pillar explicitly, framing the
entitlement ledger as a reputation/commitment primitive in their words; (2) add the incentive/attack-
model layer (a mixed-motive setting where the ledger shifts the equilibrium toward honest reporting);
(3) package the deliverable as a multi-agent testbed with a cooperation metric, not a single-agent
harness extension. CAIF stays queued 2nd — but the framing needs surgery, not just a reorder.

---

## Pruning log (what codex killed or softened)

- **Killed:** LTFF scoring-rubric numerics + "funding-constrained" (unciteable/time-sensitive);
  Manifund "coverage lanes" and "AI-generated-looking" (generic); "$75k is above the sweet spot"
  as a verdict (reframed).
- **Softened:** "solo work disfavored," "95.3% = zero support," "does NOT fund single-agent
  verification," "honest reporting becomes dominant strategy," "verification ≠ cooperation,"
  "social-proof engine."
- **Pruned as GENERIC (true everywhere, not funder-specific insight):** have a theory of change,
  show artifacts, improve the bio, de-jargon, add traction, fill track record, make the ask
  explicit, use realistic metrics, address novelty, explain evidence→thesis, avoid looking
  capabilities-accelerating. Kept ONLY where tied to a funder-specific reason.
