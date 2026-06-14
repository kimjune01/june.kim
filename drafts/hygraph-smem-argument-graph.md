# Argument graph: The Hypothesis Graph — Semantic Memory Written by Methodeutics

The paper (`src/content/blog/2026-05-28-the-hypothesis-graph-semantic-memory-methodeutics.md`,
slug `/the-hypothesis-graph-semantic-memory-methodeutics`) is a **view onto this graph**.
This file is the skeleton: edit here first, then propagate to the view. Each node
carries its claim, its warrant, its status, and the paper section that renders it.
Statuses: `proven` (receipt-backed), `null-attributed` (null with mechanism),
`threshold`, `existence (n=1)`, `pending`, `declared` (norm, not finding).

The graph is itself the demonstration: nodes typed, warrants named, kills explicit.

## CURRENT STATE (2026-06-13) — read this first; governs where the dated blocks below conflict

- **The jewel = the hypothesis graph; abduction is ONE facet (do not let the facet eclipse the jewel).** The contribution is the DATA STRUCTURE: a typed semantic memory that holds inquiry — all three Peircean modes as CRUD-able, kill-graded nodes — epistemically grounded by the trilogy. Its sharpest *demonstrated* facet is **abduction**, the unnamed third mode the hygraph lets you EXTERNALIZE; abduction's engine is the **XOR of diffs**, a MATH op (the symmetric difference between what a fix changes and what the true predicate requires; the gate's `mishandles` made numeric), not a LANG op. (Abduction's DEFINITION is grounded in the theory leg via separation-logic **bi-abduction** — figure/ground, Calcagno/O'Hearn/Infer, tri-abduction Zilberstein, §application, with the figure caption "the XOR isolates the figure from the ground". XOR-on-diffs is its OPERATIONALIZATION, not a reductive redefinition. Codex-sniff #2 "reductive" = a CACHE ARTIFACT: the skeleton compresses out the bi-abduction leg; DISCARDED. Render duty: the XOR-on-diffs claim arrives tethered to the bi-abduction grounding, never floating free.) Deduction and induction are REAL and necessary but already culturally owned (compiler/types; tests/benchmarks) — do NOT explain them, the audience owns them; name and externalize the one that was missing. Externalize the XOR at the harness layer → a training-free lift. So: jewel = the graph; the discovery/evidence is the abductive facet.
- **Audience-aware structure (2026-06-13; supersedes the result-led 4-beat framing for the WHOLE paper — the "yes it works" energy now lives INSIDE the evidence beat):** (1) intro = the high-level view; (2) the OBJECT under examination = the hypothesis graph (hand them the jewel); (3) what it needs to be useful = the THEORY, BOTH legs load-bearing and NOT decoration — the pragmatist-inquiry / methodeutics leg (§grounding, §application) AND the epistemics leg (WCBF/VK: entitlement + buildable truth); (4) the supporting EVIDENCE (the dissection + multi-model); (5) close with a REFLECTION on what this increment means for AI development overall, in MANY directions (eval should measure generalize-beyond-induction; scale is not the only lever; reasoning at the harness layer; the trilogy/epistemics; FW2/FW3).
- **Goal reframe = generalize beyond induction (P5/Sutton, mode-theoretic):** we don't need to re-solve bugs that already have fixes (induction = fit visible tests / recall the answer); we need agents that **generalize beyond induction**, a sound general rule from incomplete evidence — which IS abduction. Narrow fix = inductive fit (passes the reported case); general fix = abductive generalization (catches the two OUT-OF-GRAMMAR held-outs `<u8 as Tr>::A`, `G<G<Void>>` it never saw → represents, not tabulates). One instance, existence-grade. This is the Sutton "beyond corpus synthesis" bookend in mode language (convex-hull framing cut, witness flux→Verus), and why the bench is the wrong instrument (it grades induction, spec handed over: §audit). ML-AUDIENCE DUTY (codex-sniff #4 adjudicated — do NOT soften; the objection near-confirms the gap, induction is ML's whole paradigm): SPELL OUT abduction as a distinct mode for readers who own induction but have no name for the other mode, grounded in PEIRCEAN inquiry / pragmatist lineage (established — Peirce names the mode; §grounding's three-modes figure already does this; citation-tiered on Peirce, NOT author coinage). TYPING RAIL: held-outs = EVIDENCE of beyond-shown-set generalization (strong, in-trace); "this is the abductive mode, not induction" = the THEORY leg that NAMES it (Peirce), not carried by the held-outs alone. Pre-empt "it's just OOD generalization / induction done well": abduction GENERATES the explanatory rule (the inhabitedness query), induction TESTS it; ML boosts induction + pattern-extrapolation, the agent here reached the explanatory structure = abduction.
- **The surprise = attribution (not the mechanics):** under the hood nothing surprises — the theory predicts every step. THE surprise is the **minimal necessary composition** that lifts over a *minimal-prompt + generic-advice* baseline: generic rigor, methodeutic vocabulary, the bare task, and more scale all NULL (§attribution); the only load-bearing ingredient is externalized abduction (enumerate → calibrate against an EXTERNAL oracle → gate), MINIMAL yet NECESSARY. CONSEQUENCE (vision-not-pitch — we are NOT arguing against scale): this points at an UNDEREXPLORED harness-layer area that DEMONSTRABLY lifts performance on the generalization/investigation band (localization-hard, verification-bottlenecked; §null-regime fences it). Existence-grade; the sigfig / large-n quantification is explicitly FUTURE WORK. Do NOT say "dismisses the necessity for more scale" (codex-flagged too hot), do NOT frame it as competing-with-scale, do NOT resurrect the walked-back billions-vs-pennies ECONOMIC-COMPETITION argument (harness replaces / out-competes scale on cost — the trap). The ACCESSIBILITY contrast IS fair and is the vision point: scale costs billions and is gated to a few labs, a harness is a **git clone away** — open, model-agnostic, anyone can run it. This is a FACT TODAY, not aspirational: the `abductor` is a public git-cloneable artifact (github.com/kimjune01/abductor), so the accessibility claim carries its own receipt (clone it, run it), consistent with receipts-first. Frame as accessibility / who-can-participate (vision-not-pitch), NOT as a market or cost-competition claim. The cheapness (harness layer, no training, no GPUs, weights frozen) stays as the ATTRIBUTION confirmation (the delta IS the encoding), not an anti-scale or cost headline. (K10 retired — no anti-scale claim left to kill; the lift's kill is the existence kill, K6/K7.) MODEL-AGNOSTIC BY CONSTRUCTION: a harness-layer lift lives OUTSIDE the weights, so it is portable / bolt-on across any model — the structural advantage over a fine-tune (which improves one model only), and the deep reason the multi-model evidence coheres. HONESTY RAIL: "model-agnostic" describes the LEVER's locus (portable), NOT a guarantee every model exploits it (codex-CLI hit an implementation wall) — claim the locus, not uniform success.
- **The mechanism bar (2026-06-13): ATTRIBUTE + attach confident CAUSAL LINKS, not just show the lift.** A mechanism paper owes (a) attribution of the lift to a cause and (b) the causal chain we believe produced it; "a lift happened" is a phenomenon, "this chain caused it" is a mechanism. What carries it here, by strength: (1) INTERVENTION — flip the oracle's source internal→external with everything else fixed, the outcome flips narrow→general (ablation is causal, not correlational); (2) MEDIATION shown in the trace — gate feeds uninhabited cases the narrow predicate misses, `mishandles>0` bars pass → model greps → finds rustc's inhabitedness query → generalizes `is_never()`→`is_inhabited_from` → lift; (3) BOTH-SIDES CONTROL — coverage is the lever: where the gate pushes the model generalizes correctly, where the gate is silent it over-rejects (`ho5`/divergence); the SAME mechanism predicts its own failure, control in both signs = the strongest evidence; (4) FROZEN WEIGHTS — the delta IS the encoding, rules out scale/recall; (5) LOCUS pinned by enum-calib — the cause is the external *calibration*, NOT the enumeration the model can self-build. Typed honestly: confident causal links for the DISSECTED instance (existence-grade); multi-model shows the pathway is not model-idiosyncratic; FW2/FW3 are where causality is *conjectured* beyond the receipt. Render duty: §right-regime + §attribution must state the chain explicitly (magnify the climb), with the both-sides control as the keystone, not lean on the bare lift. FORMALIZATION — the chain is a **Pearl causal DAG**, candidate paper FIGURE: treatment **O** = oracle source (do-intervenable; the ablation IS `do(O=external)`), mediators **O→M→S→G→L** (mishandles → search/grep → predicate-generality → lift), moderator **C** = gate coverage gating M and G (the both-sides control: `ho5` = C silent on that arm → G collapses to an OR → over-reject), backdoors (scale / recall / prompt-craft) blocked by frozen weights + fixed harness. HONESTY RAIL: present as the believed causal STRUCTURE + one interventional edge (`do(O)`), NOT do-calculus effect-estimation from observational data (n=1 gives the intervention, not a distribution to identify over). Middle scope per DS-bar: the DAG + prose, no do-calculus derivation.
- **Why n=1 suffices (the rigor argument, NOT an apology):** a causal DAG inherits its credibility from its EDGES. If every edge is sigfig-demonstrated ELSEWHERE, the paper owes only (i) the COMPOSITION — these edges chain to produce the lift — and (ii) the ONE novel interventional edge, here `do(O)→lift`, which the ablation establishes causally at n=1 (an intervention is causal at any sample size). No large-n significance is needed to re-establish borrowed edges. DISCIPLINE = an **EDGE AUDIT** (the hygraph's own ethos turned on the paper: every edge carries its warrant, as every node carries its kill), tiered: BY-CONSTRUCTION (O→M, the gate computes the symmetric difference deterministically; G→L, a general predicate covers its instances), LITERATURE (in-context degrades with size = context rot / lost-in-the-middle; models act on a failing signal = agentic-loop work), IN-TRACE (M→S→G mediation; C-moderation both-sides = the keystone; can't-self-supply-the-oracle = the v7 self-mislabel + enum-calib, the direct receipt), NOVEL-THIS-PAPER (`do(O)→lift`, ablation + both-sides control). Sigfig is owed ONLY at the novel edge. HONESTY (cuts both ways): a borrowed edge must ACTUALLY be established — don't borrow-significant a shaky edge to dodge the work; if it isn't sigfig'd elsewhere it gets demonstrated here or the DAG has a weak link. This is what licenses "n=1 is correct for a mechanism." CITATION STRATEGY (diffuse the n=1 concern): cite AGGRESSIVELY at the borrowed edges so each is visibly backed where it's significant (context rot + lost-in-the-middle; agentic-loop work; Pearl for the DAG; Peirce for the modes) — the more edges visibly established, the smaller the n=1 surface a skeptic can attack. NO ORPHAN EDGES: borrowed → cite; by-construction → definitional; in-trace → substantiated by DATA WE HOLD (the 43,586-line trace, the held-out files, the v7 record, the committed artifacts), each rendered pointing at its specific receipt (this IS the magnify-the-climb work). DPI DROPPED from the cite list (conceded overextended / not load-bearing per codex-sniff; render duty: soften DPI-as-proof in the abstract + §enum-calib down to the in-trace v7 evidence). EDGE-SUBSTANTIATION MAP (codex-researched w/ web search 2026-06-13; VERIFY every cite at render, confidence noted): **do(O)** Pearl *Causality* 2009 + Rubin potential outcomes + Shadish/Cook/Campbell 2002 (by-construction + well-established, high). **O→M** Barr et al. 2015 "The Oracle Problem in Software Testing" (high) + Huang et al. 2023 "LLMs Cannot Self-Correct Reasoning Yet" (high) + Tyen et al. 2023 (med-high) — established for testing, partial for the LLM-agent step. **M→S** Ko & Myers 2005, Sillito/Murphy/De Volder 2006/2008, Ko et al. 2006 (high) — partial. **S→G [WEAKEST]** concept-location (Rajlich & Wilde 2002, Sillito, Ko 2006, high) backs "search EXPOSES the abstraction" but NOT "search → chose the general predicate"; RESOLUTION = demonstrate S→G IN-TRACE (we have the data: grep→`is_inhabited_from` in the 43,586-line trace) AND weaken the literature claim to "search exposed the abstraction". **G→L** Mitchell 1980/1982 + APR-overfitting (Smith 2015, Le 2018, high) — well-established / partly by-construction. **C→M** Goodenough & Gerhart 1975, Zhu/Hall/May 1997, Ammann & Offutt (by-construction + well-established, high). **C→G** PBE/synthesis (Gulwani 2011, Lau 2003, high) + APR-overfitting — partial, needs paper-local evidence. NO edge has zero support; only S→G's strong form is demonstrated here (in-trace). SIGFIG (future work): factorial oracle × search × coverage, logs coded for predicate choice — substantiates S→G and C→G at significance. TIERING GUARD (per citation-tiering): aggressive on ESTABLISHED / canonical / peer-reviewed sources ONLY; the trilogy companions (WCBF/VK) and any author synthesis stay SELF-LINKS, not load-bearing cites (coupling the narrow claim to unestablished work hands a hostile reader an exit). The novel edge (`do(O)→lift`) rests on the INTERVENTION, not a citation. ACCURACY: aggressive citation raises the stakes — VERIFY every borrowed cite says what we claim at render; a miscited edge is worse than an uncited one.
- **Trilogy & root-not-patch:** two companions FIRST — epistemic (/what-cannot-be-false-cannot-be-true: trichotomy + buildable truth) and protocol (/verifiable-knowledge) — then this, the data structure. Recipe: pragmatist inquiry (Peirce's abduction/deduction/induction) × epistemics (WCBF/VK) → the hygraph, which **falls out of the theory as a consequence** (not a bolt-on) and, implemented, has the four properties + solves the loud industry problems (verification crisis, agent trust, lost reasoning, review bottleneck). Industry patches with scale/context/RAG; the trilogy fixes the root. CITATION TIERING: companions grounded BY REFERENCE (self-link/provenance), not load-bearing cites; published claims rest on standard results.
- **Thesis + lead witness + axis:** reasoning can be ENCODED at the harness layer, the load-bearing encoded thing being a kill's external **oracle** the model cannot self-supply (= abduction, the unnamed third mode; T3). Lead witness **Verus #2219 (E7)**: six self-graded methods plateau on the narrow fix, one externally-oracled arm reaches the general fix (recovers rustc's inhabitedness query). Sharpest = **enumeration inducible, oracle not self-generable (E8)**; cognitive why = addition (enumerate) not subtraction (find the complement) in-context. n=1 is correct for a mechanism — do not apologize. **Axis (A5)** = internal vs external oracle (carrier prompt-vs-CLI incidental); `abductor` (D7) = the external oracle as a **bolt-on** onto codex / Claude Code (industry harness fixed, tool the only delta).
- **Evidence shape & framing craft:** multi-model gate2 (merged hygraph-mechanism master 2026-06-13, branch `pilots-11-fable-minimal-ablation`): Fable (clean), Sonnet 4.6 (clean), Composer 2.5 (dirty) all near-A with the SAME carve-out + SAME `ho5` residual; codex-CLI out → read as NECESSITY + COVERAGE-BOUND, NOT a scoreboard. RETRACTION-SAFE (codex review 2026-06-13): "workflows" not "families"; "behavioral carve-out" not "same mechanism"; "recall not required, not excluded"; "efficiency/endpoint" RETRACTED; MANDATORY caveat — shared `ho5` miss is gate-funneled attractor, NOT independent rediscovery. NECESSITY vs RECEIPT (codex-sniff #5 adjudicated): "every instance reaches for the same operation, because that is how inquiry works" is a THEORY claim (FW2, necessity — we dissected one instance and took the XOR out to a CLI); the multi-model RECEIPT stays scoped (same behavioral carve-out, gate-funneled attractor, NOT independent rediscovery). The convergence is CONSISTENT-WITH / predicted-by the necessity; the receipt does not prove it. Do NOT let "must reach for it" leak into the empirical wording. Two inferred mechanisms (beat 3): (a) weak in-context XOR (self-mislabel: v7; INFERENCE-grade, rests on IN-TRACE enum-calib/v7 — the receipt; /compress-and-unfold a self-link; DPI demoted, not load-bearing); (b) degrades with DIFF size not model size (CONJECTURE FW3/K9; supported by context rot / lost-in-the-middle). De-frame "mechanism" (33× → earn by shown gears + cross-model, not repetition); n=1 stays the dissection unit, multi-model is its robustness. MAGNIFY the climb: 281 gate calls, plateau-then-break, the grep finding `is_inhabited_from`, before/after predicate, the held-outs, v7.
- **Genre + presentation (A6/A7):** data structure + protocol (verifiable-log / certificate family: CT, PCC, PROV), NOT pure DS — hygraph = DS (smem), methodeutics + gate = protocol (pmem). Punchline = **Local Replay Auditability** (A6 iv), not big-O; two replay levels (strong = Verus; artifact = LLM trials); invariants on the mechanical SKELETON, prose payload un-invarianted (A6 ii). §3 discipline (A6) = middle scope: named skeleton invariant + per-op preservation + comparison table + TMS/provenance-log/search-tree rebuttals; pre-empt **novelty collapse** (#1 failure mode).
- **Demoted / guards:** flux #1613 (E4) → one-paragraph auditability pointer (§other-cases), not a lift (oscillates de-hinted). Bench (B/C/D) → cornered instrument-note (oracle bracket C1 nulls it); do NOT re-inflate the 95.3% / 31–37pt bench-lift (the trap). Alignment/goal-setting → CUT from the paper (don't fight pedants), graph-internal only (P4).
- **Source docs:** `drafts/data-structure-introduction-range.md`; `~/Documents/hygraph-mechanism` (pilot 11 = Verus; multi-model merged 2026-06-13); `~/Documents/abductor`.

*Node sections (A–T, K, FW) below are current. The dated framing blocks and propagation logs are PROVENANCE/history — kept for the trail, superseded here.*

## Provenance & history — dependency diagram (framing prose collapsed 2026-06-13)

*Framing evolved 2026-06-10 → 06-13; CURRENT STATE above supersedes it, the dated propagation blocks below log what changed, and git holds the verbatim prose (the graph is a cache). The dependency diagram below is current. Skip to `## A — The substrate` for the live node sections.*

```
                            ┌──────────────────────────────┐
                            │ T  merit attaches to the work │  declared
                            │    hygraph = the unit of      │
                            │    accountable agent reasoning│
                            └──────┬───────────┬────────────┘
              grounds              │           │              witnesses
   F  epistemic foundation ────────┘           └──────── E  right-regime evidence
   (truth-is-buildable,                                   (Verus #2219 lead E7;
    attestation, protocol)                                 flux #1613 → audit)
                                                                ▲
        ▲                                                       │ predicted-by
        │ survives-because                                      │
   C  attribution: bench lift ◄── explains ── D  instrument:    │
      is not the mechanism's                  Pro can't see the smem
        ▲                                                ▲
        │ decomposes                                     │ audits
   B  the artifact: bench run + receipts  ───────────────┘
        ▲
        │ runs-on
   A  the substrate: hygraph as smem, methodeutics as pmem
```

---

## A — The substrate (definition) · §2 intro, §3 hygraph, §4 grounding, §5 application

- **A1.** The hygraph is a typed smem: node = claim bound to a recorded trial;
  edge = generated by a kill condition; invariant = every node reconstructible
  by replay. Operations: perturb-and-classify, edge-from-kill, prune, replay.
  `definition` · §3
- **A2.** Methodeutics (abduction / deduction / induction as write-time stage
  contracts) is the pmem that constructs A1; trajectories are epmem. Soar slot
  vocabulary adopted directly. `definition` · §2, §4
- **A3.** Novelty lives in the edge semantics (kills generate the next
  experiment; replay first-class), at the confluence of TMS (de Kleer),
  sequential design (Wald), argumentation (Dung). `positioned` · §3, appendix
- **A4.** Scope guard: power = the perturbation surface; without it the shape
  degrades to a plausibility tree (confabulation). `declared` · §3
- **A5.** (2026-06-12) The organizing axis: a kill edge's *calibration* is
  **internal** (the model grades cases against its own belief) or **external**
  (cases graded against a known-good baseline the model cannot see). The
  carrier is incidental — a prompt that hands over the answer key and a CLI
  tool that holds it are the same thing; what matters is the calibration lives
  at the **harness layer**, outside the weights. This is the variable that
  moves a climb narrow→general (E7/E8); refines A1's edge semantics.
  `definition` · §Results "contrast, sharpened"
- **A6.** (2026-06-12) **§3 presentation discipline — introduce the hygraph as a
  data structure at the right scope** (source: `drafts/data-structure-introduction-range.md`,
  fan-out of 3 convergent reviewers + codex). Scope target = the MIDDLE of the
  range (focal structure in cs.AI/cs.SE): "formal enough to prevent rebranding,"
  no more. The skeleton to render in §3, in order:
  - **(i) Constraints-first + failure-of-alternatives.** Keep the six-constraint
    opening, but for EACH constraint name the prior structure that fails it
    (TMS/ATMS, search/proof tree, provenance log, RAG/vector memory, plain
    scratchpad). Reviewers must SEE no prior structure clears all six, not be told.
  - **(ii) Replay invariant — on the mechanical SKELETON, not the prose** (the
    LLM-flavored subtlety, author 2026-06-12: "no clean way to turn each node into
    a structured invariant?"). Resolution: each node splits into an un-invarianted
    PAYLOAD (the hypothesis text / abductive content — prose, genuinely not
    formalizable) and a mechanical SKELETON (executable trial command, recorded
    outcome, mechanical verdict, mode-capped credence, kill-edge provenance). The
    invariant predicates ONLY on the skeleton:
      I1 (replay): a closed node's command re-executes to its recorded outcome.
      I2 (verdict): verdict = predicate(outcome), not a model preference.
      I3 (credence cap): credence ≤ cap(mode) (abduction low, induction test-backed).
      I4 (provenance): every non-seed node has an in-edge from a predecessor kill.
    Two cases by status: OPEN node ⇒ carries a stated falsifiable predicate + an
    executable command (no outcome yet); CLOSED node ⇒ replays (I1+I2). State it
    Merkle-style as a displayed contract: "every node is reconstructible, by a
    stranger who does not trust the author, from its recorded trial alone." The
    prose payload is DELIBERATELY unconstrained — it is the "what you'd otherwise
    trust," and replay is what replaces trusting it. That refusal IS the thesis
    (the residue of the thinking that survives a stranger's replay, not the
    thinking), and it's more defensible than a clean DS invariant because we don't
    pretend to formalize the unformalizable; we draw the line exactly where
    checkability begins. This makes A6(vii)'s by-construction (skeleton) vs
    conventional (prose/mode-label) split the LOAD-BEARING distinction. Precedent
    for non-hard invariants exists (skip-list statistical, rope soft-balance); ours
    is sharper — a HARD invariant on the skeleton + an explicitly unconstrained
    payload. The smart constructor (iii) is clean because admission checks the
    skeleton (open: has predicate+command; closed: replays), regardless of prose.
  - **(iii) Each operation: signature → body → one-clause preservation argument.**
    `append-node` is a **smart constructor** (a node is admissible only if its trial
    replays), so the invariant holds by induction over reachable graphs (the one
    structural theorem). `edge-from-kill` gets the most space (the novel op).
  - **(iv) THE PUNCHLINE = Local Replay Auditability** (RENAMED from "Local Audit
    Soundness" per codex sniff 2026-06-12: "soundness" invites "sound w.r.t. WHAT
    semantics? — truth? task success? command determinism?"; we only claim
    recorded-predicate-matched-recorded-outcome, so call it AUDITABILITY, not
    soundness, unless fully parameterized). Claim: "audit obligations stay local to
    a node and its kill-edge; an auditor verifies any single classification by
    re-running one recorded trial, without reconstructing the whole inquiry." NOT a
    forced big-O, NOT "compression" alone. Hygraph analogue of the Merkle audit
    path / PCC certificate (legit precedent for a non-asymptotic punchline: PCC/
    Necula, Certificate Transparency RFC 9162, W3C PROV).
    **TWO REPLAY LEVELS — the distinction codex says "saves the paper":**
      • STRONG replay = re-execute the command, reproduce the outcome. Holds for
        deterministic shells, pinned unit tests, compilers/parsers/type-checkers,
        static analyzers, containerized runs over frozen inputs. **The Verus lead
        case IS strong replay** (compiler verdicts, pinned toolchain 1.93.1,
        forced-fresh fingerprinted builds) — so the headline case is clean.
      • ARTIFACT replay = verify the recorded transcript/output/hash, rerun ONLY the
        deterministic predicate over that artifact. Claim THIS for LLM-driven
        trials, live API calls, retrieval over changing corpora — the command
        replays as a PROVENANCE EVENT, not a reproducible computation. (Replay
        quietly fails otherwise: LLM gen even at temp 0, timing races, wall-clock/
        seed/locale/env deps, outcomes needing human/model interpretation.)
      State the degradation explicitly; the honest core contribution is "local
      replay/audit obligations for LLM inquiry memory," strong→artifact as LLMs/live
      systems enter the loop.
    **Prune is a COROLLARY**, not a second theorem (preserves replayability for
    retained nodes; preserves negative evidence via kill-edge summaries; frontier-set
    op, never a destructive delete → append-only invariant untouched).
  - **(v) One running example threaded through ALL operations** — the dead-light
    inquiry (already have the figures), reused for create/replay/classify/
    edge-from-kill/prune; do NOT rotate examples per op.
  - **(vi) Comparison table** (rows: hygraph, TMS/ATMS, provenance/lineage,
    RAG/agent-memory, search tree; cols = the six constraints) + **three explicit
    "isn't this just X?" rebuttals** (TMS/ATMS is the most exposed cs.AI flank:
    belief-status vs trial-bound hypothesis; deductive-justification vs empirical-
    kill edge; non-monotone belief-revision vs monotone append; author-trusted vs
    stranger-replayable). This pre-empts the #1 failure mode, **novelty collapse**
    (reviewers deciding it's a renamed log/DAG/TMS). Extends A3's positioning.
  - **(vii) Honest cost register:** what is guaranteed BY CONSTRUCTION (command+
    outcome replay; idempotent kills) vs CONVENTIONAL (the credence-mode label
    depends on honest tagging). Absence of this reads as hand-waving.
  - **OVER-ENGINEERING GUARD (do NOT, for this venue):** no lower bounds, no forced
    asymptotic theorem, no amortized/banker-physicist machinery (wrong fit for a
    monotone no-rebalance structure), no multiple numbered invariants (one, used),
    no smart-constructor formalism beyond the admission check, no category-theory
    dress-up, no "general-purpose graph formalism" claim, ≤1 theorem unless the
    second is a direct corollary, no formalism before the worked example.
  - **CODEX INVARIANT TIGHTENINGS (sniff 2026-06-12):** I1 (replay) must be stated
    CONDITIONAL on a captured execution environment (tool versions, seeds, model
    IDs, retrieval corpus, timestamps, network/external state) — otherwise it is
    simply false. I2 (verdict = predicate(outcome)) is NOT circular ONLY IF the
    predicate is PREDECLARED before outcome evaluation and the gate is a named,
    versioned, deterministic evaluator (require a **gate hash**); it IS circular if
    the predicate is handwritten after seeing the outcome or the verdict is just a
    field copied from the model. I3 (credence ≤ cap(mode)) is a GOVERNANCE invariant
    (it stops abductive guesses masquerading as deductive certainty), NOT calibration
    — do not oversell it as epistemic. I4 (edge-from-kill) is the distinctive one,
    but state whether WITNESS/refinement edges also exist (does positive evidence
    generate descendants?) or reviewers ask why only kills spawn edges. ADD **I5**
    (immutability / append-only identity: closed-node contents content-addressed or
    tamper-evident; kills idempotent and unerasable) and **I6** (gate reproducibility:
    verdicts produced by the named deterministic evaluator over recorded artifacts,
    NOT by the LLM). Keep the theorem MODEST and operational — if I1–I6 read as a
    theorem but hold only under engineering assumptions, reviewers punish the mismatch.
  - **RESIDUAL REVIEWER ATTACKS to pre-empt (codex):** (1) novelty/"just provenance
    + test records" → answer: edge-from-kill + mode-capped credence + deterministic
    routing = a specific inquiry-memory discipline, not generic provenance; (2)
    semantics gap "you verify the envelope not the hypothesis" → ACCEPT it: we audit
    evidential warrant, not truth; (3) replay assumption → the strong-vs-artifact
    split (iv); (4) LLM dependence → LLM proposes, gate disposes, memory records the
    failures; (5) evaluation vs transcripts/ReAct/Reflexion → NOT missing, NOT a
    strawman: **abductor is a BOLT-ON tool** attached to the real shipped vendor
    harnesses (codex CLI, Claude Code) — themselves deployed ReAct-style loops, the
    industry baseline. The comparison is harness-as-shipped vs harness+abductor
    (harness held fixed, tool the only delta) → maximally ECOLOGICAL: the baseline
    is literally what people run. The bolted arm beats the bare harness on Verus
    (general where it plateaus narrow); bench + OSS deployment = population evidence.
    This also reinforces the genre (A7): a bolt-on *verifier layer* added to an
    existing producer = the PCC / Certificate-Transparency shape (don't rebuild the
    producer, add the checker). **Render fix:** say it plainly — "abductor bolts
    onto codex / Claude Code, the deployed agentic CLIs; the baseline is those
    harnesses unmodified" — so the reviewer sees the baseline is the real industry
    agent; (6) overformalization → keep it operational. Reframe per codex: "hygraph is a persistent semantic-memory
    structure whose safety properties are defined by the writer/verifier protocol
    that maintains it" — makes the hybrid explicit, not apologetic (feeds A7).
  `presentation discipline` · §3 (refines A1/A3/A4; render note)
- **A7.** (2026-06-12) **Genre: data structure + protocol, not pure DS** (author:
  "it's more like a protocol that happens to share the data structure? not sure we
  meet the strict definition"). Resolution: don't chase the strict pure-DS
  definition (B-tree/skip-list optimize a *machine* cost; the hygraph's guarantees
  are PROTOCOL/CONTRACT guarantees — auditability, replay, interop). The
  architecture already names both halves: **hygraph = the data structure (smem);
  methodeutics + the deterministic gate = the protocol (pmem) that writes and
  verifies it.** So §3 legitimately introduces a data structure (the smem
  artifact); we do NOT overclaim self-sufficiency — its value is realized by the
  surrounding protocol, presented separately (pmem §4, gate §harness). **Closest
  GENRE = verifiable-log / certificate structures**, which are ALL
  data-structure-plus-protocol, framed at the contract level: Certificate
  Transparency (RFC 9162 = a protocol with a Merkle tree inside), Proof-Carrying
  Code (a producer/consumer protocol with a proof format), W3C PROV (a model used
  inside provenance protocols), Git (Merkle DAG + commit/transfer protocol). A
  recognized, respectable category — meeting the strict pure-DS definition buys
  nothing. **This DISSOLVES the A6(ii) LLM-payload worry:** protocols carry opaque
  payloads with invariants only on the envelope/framing (HTTP body, TLS plaintext,
  Git blob contents are all un-invarianted). Opaque-payload + checkable-envelope is
  the NORMAL protocol shape — the prose payload rides along by genre, not by
  defect. The two doubts (no clean per-node invariant; is it really a DS) answer
  each other. **The one-line claim (codex 2026-06-12):** not "hygraph formalizes
  hypotheses" but "**hygraph makes claims auditable by binding opaque abductive
  content to executable evidence envelopes.**" (CT separates opaque log entries from
  append-only Merkle audit proofs — closest for monotonicity; PROV records
  provenance edges without proving semantic truth — closest for edge-from-kill; Git
  separates blobs from content-addressed structure; PCC separates untrusted code
  from a checkable certificate.) **Render consequence:** keep A6's DS discipline FOR
  THE ARTIFACT (skeleton invariant, ops, comparison table), but frame §3's VALUE as
  a protocol/contract guarantee — **Local Replay Auditability** (A6 iv) is a protocol
  property, not a complexity bound. Codex confirms the protocol framing STRENGTHENS
  the contribution AS LONG AS the title/abstract don't promise a new theoretical
  graph structure then deliver a logging discipline — ours is safe ("Semantic Memory
  *Written by Methodeutics*" already names the protocol). Phrase it: "hygraph is a
  persistent semantic-memory structure whose safety properties are defined by the
  writer/verifier protocol that maintains it" — hybrid made explicit, not apologetic.
  `classification` · §3 framing (refines A1/A3/A6)

- **A8.** (2026-06-12) **Epistemology grounding — a MACHINE-LEGIBLE epistemology**
  (author: "this is a kind of epistemology legible to machine"; the paper is heavy
  on A2's Peirce/abduction vocab, LIGHT on the epistemology — build it out parallel
  to A2). Anchors: [[belief-is-the-edge-of-knowing]] = the START, [[truth-is-buildable]]
  = the TERMINAL (they are explicit companions). **The frame:** most epistemology is
  about human knowers and *certainty* (justified-true-belief, in-the-head
  justification) — not runnable. The buildable-truth arc is the one a MACHINE can
  execute, because it reduces belief/knowledge/truth to buildable/checkable/replayable
  structures. A2 (Peirce modes) = HOW inquiry runs; A8 = WHAT the nodes mean (node
  semantics). The arc:
  - **Belief (start, [[belief-is-the-edge-of-knowing]]):** no tier above belief;
    knowledge = belief past a stakes-dependent threshold; truth is internal-to-
    projection (all cognition is lossy projection); credence is continuous (Ramsey:
    belief = a bet, strength = the odds). → the node's mode-capped credence. LLMs
    FAIL this by default ("confident confabulation": uniform apparent confidence, no
    calibration, no confidence-propagation) — the hygraph supplies the missing
    architecture (credence typed by mode, calibrated by trials). [belief-is-edge has
    a whole requirements table; cite as the diagnosis of the bare LLM.]
  - **Knowledge (middle):** a DERIVED predicate — belief past the action threshold,
    contextually indexed; not certainty but EXPOSURE (a real chance to fall), the
    build between the skeptic's impossible certainty-demand and the realist's
    unbuildable correctness. → a node that has survived its trial.
  - **Truth (terminal, [[truth-is-buildable]]):** truth = a build currently PASSING;
    lives in the EDGES (provenance/citations), not the nodes (a tautology is a
    detached node — irrefutable IS useless). Three states proven/refuted/OPEN =
    true/false/**untrue** (the conjecture state). Build parts map 1:1 to the hygraph:
    provenance = dependency graph; citation = an edge; attestation = the recorded
    trial; falsifiability = able to go red = the KILL CONDITION; test = reality
    pushing back = the world-facing trial; reproducibility = rebuild from source =
    REPLAY. Guardrail vs relativism: the build includes a test that can fail (a build
    that can't fail = a hardcoded return value = the rigged benchmark).
  - **Node-state mapping (the payoff):** witnessed = a passing build (true); killed =
    a red build (false); open = untrue (a conjecture awaiting its test). "Truth lives
    in the edges" = the kill-conditioned edges carry the warrant. So the hygraph IS
    this epistemology instantiated — which is *why* it is machine-legible (ties to §3
    "binds opaque content to an evidence envelope"; Local Replay Auditability =
    truth-is-buildable's reproducibility made local).
  **Where it lands:** EXPAND §grounding's one-line "pragmatist credence" into this
  full arc, parallel to the Peirce modes, grounded BY REFERENCE (link belief-is-edge
  + truth-is-buildable + /modes-of-reason + /abduction); F1 stays as the §12 callback.
  Citation-readiness: belief-is-edge + truth-is-buildable = author's-own-prior
  self-links; Ramsey/James/Dewey/Peirce canonical; three-valued-logic / intuitionism
  / Kant-noumenon lineage citable. `grounding` · §4 (expand), refines A2/F1
  - **PRIOR-ART / NOVELTY (codex search 2026-06-12; author: "cogarch is missing
    this").** Verdict: NO exact prior-art match; gap defensible if scoped NARROWLY.
    Scoped claim (codex's wording): *not* "no one represented uncertainty/truth/
    provenance/replay" but "no cognitive architecture or agent-memory system makes
    TRUTH a replayable, falsifiable, provenance-bearing BUILD artifact, with credence
    and warrant-state as first-class MEMORY NODE SEMANTICS." Closest prior art, where
    each stops:
      • **NARS** (Pei Wang) — nearest cogarch: experience-grounded truth-as-degree,
        non-axiomatic, revised by experience. STOPS: no provenance/warrant graph, no
        executable falsification edge, no signed trial, no replay-by-distrusting-party,
        no proven/refuted/open ledger. (Address head-on.)
      • **OpenCog AtomSpace / PLN** — typed hypergraph + truth values + executable
        procedures. STOPS: truth-as-LABEL, not truth-as-replayable-BUILD.
      • **Traxia** (arXiv 2606.08256, 2026-06-06) — IMPORTANT CONCURRENT near-miss:
        agent-native scientific publishing (confidence intervals, signed identities,
        provenance, replication record, living KG). STOPS: publishing infra, not typed
        agent-MEMORY semantics; no proven/refuted/open ledger, no falsifiability-as-
        kill-edge, no knowledge-as-stakes-threshold. /truth-is-buildable (06-04)
        predates it by 2 days → F7 timestamping move; cite as concurrent.
      • nanopublications/micropublications (machine-readable claims + provenance, but
        evidence not executable, no credence/threshold/kill-edge/replay); ReproZip /
        noWorkflow / executable research compendia (replay, but of computations not
        memory claims); Falkenhainer (TMS+credence, no executable falsifier/replay).
        TMS/ATMS + W3C PROV already the §3 nearest-neighbor rebuttals.
    **Most exposed = the SYNTHESIS attack** ("just NARS + TMS + PROV + ReproZip +
    nanopub"). Defense: none makes the combination the *semantic contract of memory
    nodes*, where truth is operationalized by replayable EDGE STRUCTURE, not a stored
    label or textual provenance. Frame the three states as a WARRANT-LEDGER STATE,
    NOT a new logic (else proven/refuted/open deflates to passed/failed/not-run).
    **RW action:** add NARS, OpenCog/PLN, Traxia (concurrent), nanopublications as the
    EPISTEMOLOGY-grounding neighbors, distinct from the cogarch-MEMORY neighbors
    (Soar/CoALA/AriGraph) already in §related-work.

## B — The bench, bounded (oracle availability, not the method) · §8, cornered

- **B1.** Pro public set, frozen harness, official grader: 95.3% frontier pair,
  93.1% open-weight pair. **Reframed (2026-06-10):** the number is a property of
  *oracle availability*, not the harness or method — on the public split the
  failing tests are visible, the gate iterates against them, and any competent
  agent handed that signal reaches the mid-nineties (oracle bracket C1 prices it).
  Stated ONCE, named as the mistake the section corrects; the bench renders AFTER
  the mechanism now, cornered. `proven` · §8, pointer-first
- **B3.** OSS trace: 81 merged PRs / 73 cold repos / 50.6%; agent-selected,
  agent-authored; GraphQL-recomputable. **Not graph-dependent (2026-06-10):** a
  minimal prompt digs the few levels most of them need; the merge rate feeds T
  (strangers merged work on receipts, not reputation) but is NOT evidence for the
  smem. `proven` · §7 Results notes the non-dependence, receipts in §8.
- **B4.** Artifact claim (receipt-bar table): no documented method combines
  equal receipts + higher rate. `proven, bounded` · appendix
  *(cost-as-virtue cut 2026-06-10: cost is a measurement, and the paper's
  thesis is that the hygraph's value escapes measurement; cost survives only
  as a receipt — the "C = cost ledger" disclosure column — never as a
  competitive claim. The "lower cost" leg of the artifact claim is gone.)*
- **B5.** Bounds: public split; not a leaderboard number; gate had oracle
  access; says nothing about the private split. `declared` · §8.2

## C — Attribution: the lift is not the mechanism's · §9

- **C1.** Oracle bracket: implement-only no-oracle 50% floor → gate-with-tests
  96% ceiling (n=50). The oracle is ~the whole lift. `proven` · §9.1
  *(kills the v1 thesis "reasoning lives in the harness"; the companion posts
  conceded it first)*
- **C2.** Prompt content (M/G/T) null at diagnosis: M−G −0.012, G−T +0.035,
  CIs straddle zero. `null-attributed` · §9.2 — reread by F4 as the expected
  null of a *protocol* measured per-instance.
- **C3.** Directed perturbation: +0.105 on underdetermined-cause stratum only;
  McNemar p=0.057; 11 gate-confirmed existence cases. `threshold` · §9.3
- **C4.** Gate compensation: the gate's cheap trustworthy verdict lets blind
  iteration substitute for aimed diagnosis; held-constant covariate produced
  the null. Falsifiable differential: degrade the gate, deprived arm worsens
  more. `mechanism finding` · §9.3 → predicts E's regime.
- **C5.** Craft-only (delete the whole diagnosis stage): ~1 point, resting on
  two instances. `null-attributed` · §9.4
- **C6.** Verdict: on Pro, smem ≈ 0 points, vocabulary = 0, aimed probe =
  sliver, oracle ≈ 46, model pair = 2.2 raw / 17–22 genuine. `proven` · §9.5
  Framing (user, 06-10): the null is the supporting argument for "how well
  does it work?", answered "not on the most popular coding bench, because the
  bottleneck there is not diagnosis" — which sets up E1's flip.

## D — Instrument: Pro structurally cannot measure the smem · §10 audit

- **D1.** 66% ENTAILED + 11% determined-codebase ⇒ ~77% spec-given ⇒ nothing
  to abduce (the hygraph degenerates to a single transcription node). `proven (grep)`
  *(flipt worked example CUT 2026-06-10 — degenerate single-node graph, weak
  demonstration; E4 is the in-paper witness now.)*
- **D2.** 11.4% mechanical spine + 26 two-expert = 15.0% proven underdetermined
  ⇒ lottery; no diagnosis can recover information absent from the materials.
  `proven (grep) / verified (two-family)` — self-citation is safe: rows are
  pointers to ambiguity, re-derivable, not opinion (user call). Guard, rendered
  as a parenthetical: cause-determinacy (C3 strata) ≠ task-determinacy (audit
  labels); how hard the diagnosis is vs whether there is one at all.
- **D3.** D1 + D2 + cheap visible oracle (C4) ⇒ the nulls in C are the
  *predicted signature*, not a refutation. `attributed` · §10
  - **D3-scope (author 2026-06-10, load-bearing precision).** The claim is
    *not* "benchmarks are worthless." It is the scoped, defensible one: this
    benchmark is not a valid measure of **our flavor of reasoning** — typed,
    diagnostic inquiry. SWE-bench Pro measures spec-conformance, and measures
    it fine; it simply cannot see the mechanism the hygraph encodes, because
    ~77% of its tasks hand over the spec (nothing to diagnose) and a cheap
    oracle lets blind iteration substitute for diagnosis. Frame it as
    **applicability, not fault**: the bench is *not applicable* to this
    construct, not a *bad* instrument (avoid the word "discredit" — it keeps
    the attacking frame the narrowness is meant to drop; N/A is the cooler,
    stronger verdict). Guards against the axe-grinding read (codex flag) and
    keeps the general bench-critique (illegible / teaches-nothing /
    depreciating, F2a) as supporting color, not the load-bearing claim.
- **D4.** Field implication (determinacy-aware denominators), the flipt
  mismatch example, the specification-lottery framing, and the tool (D6) all
  render as ONE side-note ¶ (user, 06-10): the bench-standards critique is
  the audit repo's own paper; this paper needs only the fraction that
  explains its nulls. `declared, demoted to side note`
- **D6.** The instrument generalizes: `determinacy`
  (github.com/kimjune01/determinacy) is the audit as a portable tool for any
  SWE-bench-shaped bench (TOML field-map; SWE-rebench already run; Verified
  and Pro configs shipped). Its name for the conflation: the **specification
  lottery** (capability shortfall vs spec shortfall, which no leaderboard
  separates). Mechanical spine over vibe check: LLM raters over-flag, so only
  the grep-provable floor is claimed. `proven, published` · §10, availability

- **D7.** (2026-06-12) The externalized kill condition generalizes too:
  `abductor` (github.com/kimjune01/abductor) is the enumerate/calibrate/gate
  loop as a standalone, domain-general instrument (`/debug` skill). Blind to
  the answer (leak-free prompt; a model rebuilt it, E8) and cross-domain (same
  shape on syft #4760 SBOM tool found 11 omitted cases vs a human's 4, plus a
  tabulation bug in the criterion). Sibling to D6's `determinacy`. The general
  object both exploit: a disagreement (symmetric difference between what the
  system believes and what is true) — the check tests/types can't give because
  absence has no test. `released` · §Results gate-general, availability

## E — The mechanism in the right regime · §11

- **E1.** Regime spec (from C4): no handed spec, no cheap oracle, hidden cause.
  Deployment data (B3) is that regime. `derived` · §11
  Flip (user, 06-10): the regime is most of software — every issue tracker is
  a backlog of undiagnosed problems waiting on the one expensive step the
  bench never exercises; flux #1613 (41 comments, maintainers stuck) is what
  undiagnosed looks like in the wild. The bench's bottleneck is not diagnosis;
  the world's is.
- **E2.** Design guards: essence oracle (not the pipeline's own shipped tests;
  self-audit went 4/4 false-green), mini-SWE-agent verbatim baseline,
  pre-cutoff blind regeneration (graph = treatment, contamination doesn't
  cancel). `committed` · §11
- **E3.** Eight nulls, attributed twice: selection artifact (triage fast-paths
  easy bugs around the graph) + baseline reach (frontier model in minimal loop
  fixes most reproducible bugs unaided). `null-attributed` · §11
- **E4.** flux #1613: both arms suite-green; minimal = shape-gated over-narrow
  (confident false positive); graph = cause-keyed (FoldLocal), generalizes;
  receipt discriminates (int-receipt VERIFY vs E0999; unsound twin both
  reject); 19 nodes, load-bearing nodes replayed, 3 in-trail self-corrections.
  `existence (n=1 instance)` · §Results (the live example worth more than the rate).
  - **E4-replication (pilot 09, 2026-06-10, committed 979195cf).** Reproduces on
    a SECOND model family (Sonnet 4.5), same oracle, identical split: n=1 instance
    → n=2 models, so the advantage is the methodology, not the model. Sonnet-
    minimal is worse than GPT-5.5-minimal, over-narrow AND **unsound** (accepts
    the invalid T3 twin every other arm rejects). That suite-green-but-unsound fix
    now LEADS the §Discussion "confidently wrong and impossible to verify" block
    (recommendation #3, the field's live fear demonstrated). `existence (n=2 models)`
  - Pending tail (golden ticket, recommendation #1): maintainer merge of the
    trace-backed fix = external attestation; staged, awaiting response; on merge,
    update §Results + the falsifiers (§Limitations "How to refute this").
- **E6.** Per-loop preregistration discipline adopted (testing X / predict Y /
  refuted by Z); 3–5 audited cases or the committed null is the next paper.
  `pending` · §13
- **E7.** (2026-06-12, NEW LEAD WITNESS) **Verus #2219**: erased ghost `!`
  marks following MIR unreachable ⇒ sound program wrongly rejected. Narrow fix
  keys on `is_never()` (= maintainer #2230, chg 114); general fix #2501.
  **FACTUAL CORRECTION (2026-06-13, live-PR verified via gh on verus-lang/verus,
  render pass 4):** the earlier claim "general fix uses `!ty.is_inhabited_from(...)`
  (= #2501)" was WRONG and is fixed in the paper. #2501's actual diff KEEPS
  `is_never` and gates it by call context (`record_call_inhabitedness`,
  conservative on proof-block `!`-returns) — i.e. #2501 IS the mode gate, the finer
  fix that separates erased-ghost artifact from real divergence. The
  `!ty.is_inhabited_from(...)` predicate was the MODEL's (codex arm) over-broad
  route, behaviorally REDUNDANT (Fable reaches identical grading with no
  inhabitedness query → operative mechanism = the mode gate, not the inhabitedness
  oracle; per pilots/11 RESULT-corrected.md 2026-06-12). So "the model recovered
  the verifier's own decision procedure" OVERSTATES — render now: model widens to a
  mode-gated APPROXIMATION under gate pressure, wide-but-broken; #2501 is finer.
  Live status: #2219 CLOSED 2026-06-05, #2230 MERGED 2026-03-09, #2501 MERGED
  2026-06-05 (the merge that closed #2219). On a fixed
  toolchain, forced-fresh fingerprinted builds: **six internally-calibrated
  methods × 3 draws = 0/18 reach general** (modal chg 114); the single
  **externally-calibrated** arm is the sole general fix (pass=true, chg 269,
  0 valid-preserve rejections) AND rejects two *out-of-grammar* held-outs
  (assoc-projection, nested-generic) the gate never showed it — proof of
  *represented predicate*, not tabulation (instrumentation: each arrives
  normalized to an uninhabited type). **Bench/golden setup (§verus-bench, added
  2026-06-12 per author "be clear what golden means"):** the tiny bench = base
  (buggy commit) + the two maintainer fixes + hand-built probe programs, each
  VERIFY/REJECT. A probe's *golden* = the verdict a correct compiler owes it.
  TWO golden sources, deliberately separated: (a) bug probes are uninhabited
  *by construction* → golden REJECT, base wrong on exactly them → base is a FREE
  reference; the gate enumerates these (2856 cases), grades vs base, passes only
  on flip-entire-bug-set (269) + zero sound-case regressions. (b) genuine-
  divergence probes → golden VERIFY (sound), base not usable, gate blind (no
  divergence-preserve shape in its grammar) → golden from human judgment,
  corroborated by approved fix #2501; held out, outside the gate grammar, so
  passing them tests representation not gate-fit. = the E9 asymmetry (easy-arm
  oracle free, hard-arm oracle costs a human). Integrity: forced-fresh +
  binary-fingerprinted builds (vendored rustc_mir_build doesn't rebuild
  incrementally; two earlier headlines were stale-binary artifacts); 21-artifact
  frozen dataset committed. Mechanism (frontier = gate coverage,
  read from the 43,586-line trace): under pressure from cases `is_never()`
  misses, the model greps and generalizes its own predicate to
  `is_inhabited_from`. Same mechanism predicts the failure: over-rejects two
  genuine-divergence cases (the gate's 2856-grammar never enumerated that
  preserve shape) = *wide-but-broken*; held-outs catch it. **Provenance (method,
  author "be clear we took a historical PR post-cutoff"):** real historical PR —
  base 2026-03-08, narrow fix +1 day, general fix #2501 merged 2026-06-05 — taken
  deliberately AFTER the solve models' cutoffs (contamination-controlled model =
  Fable, Jan 2026). Negative recall probe (model doesn't recover the fix, says
  so). Scoped (codex): reconstruction from general pre-cutoff competence (rustc
  *has* an inhabitedness query, old) NOT recall OF THE FIX (that it fixes #2219);
  carries P5. `mechanism, existence (n=1, the right unit)` · §Results lead, §verus-bench
- **E8.** (2026-06-12, the sharp one; recast 2026-06-12 per codex + cognition
  grounding) **Enumeration is inducible; calibration is not *self*-inducible.**
  Handed the same vague leak-free prompt with no gate, a second model (Fable)
  *rebuilt the gate itself* — a 7026-case enumeration — and hill-climbed to
  self-certified 0 over-rejections, then shipped the *same* wide-but-broken fix.
  A model can bootstrap the combinatorial breadth (the **domain** of cases —
  mechanical) but cannot author the **predicate** that labels them from outside
  its own belief. Scope precisely (codex K7): not "calibration is impossible to
  induce" (E9 mines it from approved history) but "calibration cannot come from
  the model's own belief without circularity."
  **Why the tool is REQUIRED, not merely helpful (author 2026-06-12): the deficit
  is SUBTRACTION.** LLMs are equipped for ADDITION (generate / enumerate /
  recombine — the inducible half) but not for finding the COMPLEMENT in-context:
  the symmetric difference between what the model believes and what is true, the
  case its own hypothesis MISSES. "Absence has no test" — a model can't author a
  check for the case it failed to imagine, and grading itself grades a fiction. The
  externalized oracle is required because it performs exactly that subtraction (the
  XOR/disagreement against an external baseline) the model cannot do on its own
  belief — re-reads Fable cleanly: it ADDED 7026 cases but could not SUBTRACT the
  divergence case its labels were blind to. Addition inducible, subtraction not.
  Grounds in [[complementations]] (the disagreement = symmetric difference; the
  check tests/types can't give because absence has no test). Three further
  groundings, by reference, not re-derived:
  - *Goals are predicates* (Capucci 2021, "what is a goal but a predicate on a
    system?"; [[framework-lexicon]], [[the-handshake]]). Enumeration generates
    the domain; calibration **is the goal predicate** evaluated on it. So the
    boundary is means (self-inducible) vs ends/goal-predicate (not).
  - *Grading yourself grades a fiction* ([[belief-is-the-edge-of-knowing]]: "any
    claim grading itself against ground truth is grading against a fiction";
    "second-order beliefs must be testable, the system is blind to its own
    introspection failure"). Fable's self-green-but-unsound gate is that
    blindness, witnessed.
  - *New information enters only from outside* — the data processing inequality
    ([[compress-and-unfold]]: "no computation on what you already hold can raise
    what it tells you about the world; recombination is only computation —
    recall in the costume of thought"), with its physical derivation in
    [[the-natural-framework]]: a system is defined by its boundary, so **Perceive
    is the only morphism that crosses from world to inside** (a lossy surjection;
    Landauer floor), and every other role operates on what is already held. Map
    onto the hygraph: **external calibration is the system's Perceive** — the
    sole world-facing boundary crossing that imports world-truth — while
    enumeration and the model's reasoning are the *internal* roles (map/filter on
    the held). So enumeration adds no world-information; only a world-facing trial
    (calibration) can, and a model grading itself never crosses the boundary.
    The floor under the whole claim, under P5 (discovery vs recall) and F8.
  `mechanism (n=1, both halves in one run) + grounded by reference` · §Results enum-calib
- **E9.** (2026-06-12) **Calibration from approved history.** The truth a model
  can't induce is cheap to the harness: merged fix, regression suite, issue
  label are goldens because a human approved them. #2219's missing oracle
  existed all along (#2501 verifies the over-rejected divergence case);
  calibrate differentially vs base AND approved fix to close a gate's blind
  spot. Deployment design = model enumerates+fixes, harness calibrates from
  approved history. Honest asymmetry: a *fresh* bug's hard arm has no golden
  until a human judges (why #2501 took expertise). `design + bounded` ·
  §Results enum-calib, §13 future-work

## F — Epistemic foundation · §12 discussion

- **F1.** Truth is buildable: true = built + able to fall + standing;
  provenance = dependency graph; attestation = signed build log. A node without
  a replayable trial is not a node; an uncheckable number is not a measurement.
  grounds A1, indicts the rate. `first-principles` (/truth-is-buildable)
- **F2.** Attestation displaces trust: verdict vs ledger; asymmetry engine
  (fabricated nodes must survive replay, confident narrative is cheap), with
  errors-as-fuel as its failure corollary (failed builder leaves a trail;
  failed oracle leaves nothing). E4 is the witness. `grounded + witnessed`
  · renders as ONE block; the verdict-vs-ledger facet renders in the §12
  opener alongside F5a (merged 2026-06-10)
  - **F2a.** Depreciating-asset facet (author 2026-06-10): a benchmark claim
    rests on trust in the bench, and that trust is being withdrawn
    industry-wide as saturated rulers are found full of flawed tests
    (OpenAI dropped Verified for this) — so a benchmark score is a
    *depreciating asset*, worth less each quarter. A replayed trace is the
    opposite: its warrant does not decay because a stranger re-runs it rather
    than trusting it. Appreciating vs depreciating is verdict-vs-ledger stated
    as economics. The bench's three weaknesses, stacked: barely legible,
    teaches nothing, untrustworthy-and-therefore-depreciating.
    CUT 2026-06-10 (author): removed from the paper entirely as too much
    editorializing / bench pile-on (codex flagged the same: stop hitting the
    number, it keeps it central). The point is sound but it is opinion stacked
    on the bench, not a finding the paper needs. Not relocated to §12 — moving
    editorializing just relocates the problem. The load-bearing demotion stays:
    "least insightful artifact" (once) + the instrument finding (§audit,
    applicability-not-fault). Do not reintroduce.
- **F3.** Persistence: reasoning that outlasts the context window
  (re-runnable, not just readable; box-death survival); provenance has no
  half-life (preserves checkability, not truth; runnable form inherits
  apparatus half-life). `grounded` · renders as ONE block (merged 2026-06-10)
- **F4.** Peircean typing = protocol, not rhetoric: null on any single instance
  by construction (C2 reread); across instances it gains **transitive
  accountability** — B verifies A's kill, C builds on B without re-running A,
  auditor enters at any link; loose vocabulary caps accountability at one hop.
  Common vocabulary = the protocol for verifying each other's work.
  `argued` · §12 — preconditions everything in §13.
- **F5.** Trust vs accountability as an alignment direction: not a trustworthy
  agent believed, an accountable one audited; reliability = attestations
  accumulated, never trust arrived at. `declared`
  - **F5a.** THE failure mode to emphasize (user call): **confidently wrong
    and impossible to verify**. Trust is the *default mode*; the explicit ask
    to the audience is substitution: accountability for trust, line by line,
    machine-checkable. Witnessed by Verus's self-graded gate (self-certified yet
    wide-but-broken) and the 4/4 false-green self-audit. `emphasis` · renders as the §12 opener ("name the enemy
    first"), not inside the trust block
  - **F5b.** Anticipated equilibrium: a GAAP-shaped accountability regime,
    the post-Enron lesson. Three-way match as the control shape: no claim
    accepted unless proposer's claim, recorded trial, and independent replay
    agree; no single party trusted, including the agent's self-report
    (Enron = self-attestation scaling until catastrophe legislates controls).
    There is no one answer; it is a control regime, not a property of the
    agent. `anticipated` · §12
  - **F5c.** Benches operationalize alignment as obedience and conformance
    (D1 is the receipt: 77% spec-given, grade = recover the pinned choice).
    Agency is neither: facing underspecified prose the agent can guess-and-
    conform (the lottery), refuse, or exercise agency (elicit the missing
    decision, decide, declare with receipts); benches score only the first.
    `argued` · §12, §13 elicitation
- **F6.** Two-level reading: surface = AI memory innovation in SWE; foundation
  = epistemology and our orientation with the world. `framing` · §2
- **F7.** Vocabulary by provenance, pointed not claimed (user call: never
  state authority, only point). Facts on the table: the trichotomy is
  Peirce's (1878/1903); ToTh v2 uses the mode words 44× and cites zero
  pragmatists (verified against arxiv.org/html/2506.07106v2, 2026-06-10) ⇒
  the field's citation graph for its own typing is incomplete, a dangling
  pointer (F1 resonance); this paper wires the vocabulary to sources
  (§4, lineage appendix); dated posts timestamp the primitive (03-17, 04-05,
  04-08 predate ADI 04-17; 04-27, 04-28 predate CMM 05-26; ToTh predates us —
  acknowledged; **/truth-is-buildable 06-04 predates Traxia 06-06 by two days**
  — the 4th independent convergence, and the first on the EPISTEMOLOGY leg, not
  the vocabulary). Interop (F4) forces one wire vocabulary; Peirce's is
  mode-complete, 150 years stable, credence-carrying, and needs no inventing.
  **Convergence-as-evidence (the running record): ToTh (Peircean typing), ADI
  (layered abductive protocol), CMM (typed-DAG memory), Traxia (agent-native
  epistemics) — four independent groups, no coordination = structural evidence
  the primitives are landing as natural, not idiosyncratic.** That argument
  already lives in §related-work; Traxia (A8 prior-art) is the freshest + tightest
  data point (two days) and extends it from typed-reasoning/memory to the
  epistemology. Strategic: two days = simultaneity, not the usual ~3mo lead → the
  priority window is live; cite Traxia as CONCURRENT, let convergence be evidence
  not threat.
  `pointed, receipt-backed` · §14, availability bullet, §related-work
- **F8.** (2026-06-12, the dunk) **Hidden effort is not reasoning you can
  check.** The labs ship "reasoning" as an opaque dial (high/xhigh/ultrathink),
  a knob on private tokens = more *internal* enumeration. E7/E8 is where that
  runs out: the strongest internal-effort arm (self-verifier, build-your-own-
  generator) plateaus with the rest; you cannot turn the dial past the
  calibration wall, because effort scales the inducible half and cannot
  manufacture external truth. And the dial ships no replayable kill — an effort
  setting is the purest *take my word for it*. Put the reasoning in the harness,
  typed and replayable, where its level is a trail the reader checks, not a knob
  they trust. Grounded in the DPI ([[compress-and-unfold]]): the dial buys more
  recombination of what the weights already hold, and recombination adds no
  world-information ("recall in the costume of thought") — so no setting can
  cross the calibration wall, which is a world-facing measurement, not more
  internal compute. `argued, witnessed (E7/E8), grounded` · §12 (renders between
  F3 and F5, before the trust block). NB: distinct from the cut F2a — F8 is a
  FINDING (the calibration wall), not bench editorializing; it stays.

- **F9.** (2026-06-12) **Cognition-series grounding — inherit, don't re-derive.**
  Per the series through-line (compress what I learn so the work compounds;
  [[compress-and-unfold]]) and the ground-by-reference rule, the mechanism
  paper stands on prior posts via link-anchors, not inline re-explanation.
  The load-bearing inheritances and where each lands:
  - **Goals are predicates** ([[framework-lexicon]] / Capucci, [[the-handshake]],
    [[goal-transmission]]) → A5, E8, P4 (calibration = the goal predicate).
  - **DPI / "new information enters only from outside"** ([[compress-and-unfold]];
    physically derived in [[the-natural-framework]]: a system's boundary makes
    Perceive the sole world-crossing morphism) → E8 floor, F8 dunk, P5. The
    mapping: external calibration ≈ the system's **Perceive**; enumeration ≈ the
    internal roles (cache/filter/attend on the held). Why internal effort can't
    substitute for a world-facing trial — it never crosses the boundary.
  - **Grading yourself = grading a fiction; second-order beliefs must be
    testable** ([[belief-is-the-edge-of-knowing]]) → E8 self-calibration
    impossibility; the credence/node-semantics lineage (pragmatist, A2).
  - **Type III error / verb-vs-evidence checklist; reflex vs demotion**
    ([[wrong-questions]], /type-iii-error) → the paper's self-discipline: scope
    every claim's *verb* to what the evidence supports (Verus = a mechanism that
    *can occur*, not a *discovery* or a *rate*); this is how the n=1 stays
    honest WITHOUT apologizing (author). Mapping: a **reflex** (mechanical check
    before belief forms) ≈ a kill condition; a **demotion** (narrower claim
    after evidence) ≈ the credence cap. The hygraph operationalizes both.
  - **Double-loop / six-slot complementation** ([[double-loop]],
    /general-intelligence, [[the-natural-framework]]) → E9 division of labor:
    "filter = kill what doesn't belong" is automatable (the gate/kill);
    "attend = judgment the skills can't automate" is not (the calibration the
    human supplies). The means/ends split in the series' own slot vocabulary.
  **Citation-readiness guard (author 2026-06-12).** These anchors split by how
  established they are. *Paper-citable now:* the standard DPI (Cover & Thomas),
  Capucci's goal-as-predicate (published), Peirce/pragmatists (canonical), the
  Type III error. *Self-link register (author's own prior, fine to point at):*
  /compress-and-unfold, /belief-is-the-edge-of-knowing, /wrong-questions,
  /the-handshake, /goal-transmission, /double-loop. *Graph-internal ONLY, NOT a
  paper citation yet:* /the-natural-framework and the Perceive-morphism mapping —
  the world isn't ready; keep the mechanism claim's credibility uncoupled from
  the grand synthesis. The deeper grounding lives here; the paper uses standard
  vocabulary.
  `grounding index` · threaded through §Results, §12, lineage appendix

## P — The prestige (the unlock) · §12 closing

What the data structure makes possible; the payoff act. **P5 is the peak** —
discovery beyond corpus synthesis, the claim the whole inverted arc climbs to;
P1–P4 are supporting affordances that render before it and set it up. Each
affordance names its warrant or its honest status:

- **P1.** *Parallel agents, shorter wall-clock.* Monotone graph (nodes append,
  kills idempotent) ⇒ lock-free fan-out across rival hypotheses; peers
  re-verify kills instead of trusting them (F4 transitive accountability is
  the precondition). `latent affordance — named, not run` · §13
- **P2.** *Model-provider independence.* smem lives in the harness in plain
  markdown; typed contracts any capable model reads/writes; the pair-swap run
  (B1) is the witness the structure ports wholesale. Reasoning accumulated in
  a vendor's window is a liability; in a substrate you own, an asset. `proven
  for the port; declared for the stance`
- **P3.** *Accountability.* Every claim ships with its replay (F2). `witnessed (E4)`
- **P4.** *Alignment.* Trust displaced by audit (F5). **Sharpened 2026-06-12
  (E8 + goals-are-predicates):** a goal is a predicate on a system (Capucci;
  [[framework-lexicon]], [[the-handshake]]); a kill condition *is* such a
  predicate; calibration is the goal predicate evaluated. So "calibration is
  not self-inducible" (E8) is the structural content of alignment: an agent
  induces its means (the domain/search) but cannot author its own ends (the
  goal predicate) without circularity — a predicate evaluated on its own
  authority is a tautology, not a goal. Alignment = the demand that the goal
  predicate be authored *outside* the agent (the world's semantics, approved
  history E9, or a human; [[goal-transmission]]: the spec is a lossy
  transmission, the executable kill is its precise replayable form). This
  upgrades P4 from "declared direction" to a structural claim the mechanism
  witnesses, with the honest edge: sharp where the predicate is sharp (code
  soundness), contested where the goal is (do not overclaim "solves
  alignment"). `declared direction → structural, witnessed (E7/E8)`
  - **DE-EMPHASIS (author 2026-06-12): goal-setting / alignment is a SECONDARY
    corollary, NOT the primary mechanism.** Primary = the encoded-reasoning /
    external-oracle lift (E7/E8: enumeration inducible, oracle not). Over-
    emphasizing goal-setting dilutes it and picks the alignment-philosophy fight.
    In the paper: claim 3 reverted to accountability-only (no goal-setting in the
    claims list); the goal-predicate discussion facet was **CUT entirely** (author
    2026-06-12: "don't pick fights with alignment people, too pedantic" — even a
    brief goal-setting claim baits them). Only the author's existing
    accountability-as-alignment-direction language stays (trust-vs-accountability,
    GAAP/three-way-match, the *Alignment* unlock). Capucci goal-as-predicate is
    now graph-internal only. Keep the structural framing HERE as deeper grounding;
    it does NOT appear in the published view.
- **P5.** *Discovery, in Sutton's sense — escaping the model's convexity.*
  Closes the epigraph. Unaided output is bounded by the convex hull of the
  training distribution; each node is anchored to a fresh trial of the world,
  so the graph steps outside the hull one verified step at a time. The Verus #2219
  general fix (E7) was absent from the reachable corpus until the inquiry built it,
  post-cutoff and recall-probed — so it cannot be recall of the merged patch. That is
  the precise, falsifiable content of the bold word: **a creative act, by some
  definition** — output outside the convex hull of the weights, anchored to a
  verified trial, surviving a stranger's replay. Not novelty asserted;
  novelty *witnessed and re-runnable*. Agents that contain what we discovered
  recall; an agent that can build and survive a hygraph discovers.
  `existence-witnessed (E7 Verus; flux E4 demoted)`
  *(REFRAME 2026-06-10, codex coherence pass + author call: the "convex hull /
  escaping convexity" framing was CUT paper-wide. It is a capability/geometry
  claim a referee kills on sight — Balestriero, Pesenti & LeCun 2021 ("Learning
  in High Dimension Always Amounts to Extrapolation") shows high-dim points are
  almost always OUTSIDE the training convex hull, so "bounded by the hull" is
  both unprovable and backwards. "Convexity" was never standard LLM vocabulary;
  it was the author's own adaptation, pointed the wrong way. The claim is now
  EPISTEMIC, not geometric: an unaudited model output gives no way to tell
  discovery from recall; the recorded graph does. Keep the bold spine
  ("discovery, not recall"; "a creative act by a definition precise enough to
  argue with"); scope "beyond corpus synthesis" → "beyond documented corpus
  recall"; scope every "corpus did not contain" → the audit claim (absent from
  reachable sources, cutoff predates fix, unresolved at freeze). The five-clause
  criterion stays as the falsifiable target — it replaces the hull as the thing
  a skeptic must attack clause by clause.)*

## T — The declaration · abstract, §12

- **T1.** Merit = the warrant work carries in itself, checkable without
  reference to the doer. Humans conflate doer and work for lack of vocabulary
  and norms; the hygraph is the vocabulary, the receipts-first PR the practice.
  Praise the work, blame the work, replay the work. `declared` — arxiv-searchable
  on purpose.
- **T2.** Publishing attributed nulls is part of the same posture: an
  unexplained null says stop; an attributed null says where to point the next
  instrument. `declared` · §12
- **T3.** (2026-06-13) *Abduction is the unnamed, underappreciated operation in
  agent-SWE.* The field operationalized **deduction** (compiler / types / proof)
  and **induction** (tests / benchmarks); the third Peircean mode — form the
  hypothesis, find the case it cannot explain — runs implicitly and ungraded
  inside the weights. Its engine is **XOR-on-diffs**, a MATH op (the symmetric
  difference between what the fix changes and what the true predicate requires),
  not a LANG op; the abductor *maths* it instead of *langing* it
  (/dont-lang-what-you-can-math). Seated in the triad (the hygraph holds
  abduction / deduction / induction as CRUD-able, kill-graded nodes),
  externalized abduction **expands capability** on reasoning tasks (the model
  reaches a rule it does not reach alone). The instrument hooks the reader; the
  data structure is the gift. `declared` · abstract, §intro claims, §grounding,
  §discussion

## FW — future-work nodes added post-rewrite · §13

- **FW1.** *Elicitation for underspecified prose.* The audit's proven fraction
  (D2) has a correct agent response that no bench scores: elicit the missing
  decision from the human who holds it, instead of recovering the author's
  unstated choice by guess. Natural hygraph home: an underdetermined choice is
  an open node whose kill condition is a human answer. Benches account for
  neither the question nor the credit (F5c: their alignment is obedience/
  conformance). Instrument design: reward pinning the spec before building.
  `future work` · §13
- **FW2.** (2026-06-13) *XOR-on-diffs is the necessary operation of inquiry.*
  Inquiry contracts H △ T, the symmetric difference between what you believe and
  what is true; every warrant-producing step locates a member (a case the
  hypothesis mishandles) and removes it. Generation cannot find it (addition has
  no floor); only a disagreement evaluated against an external reference can — so
  the operation is necessary AND **necessarily external**. The cross-paper spine
  (WCBF refutation = finding a member of H △ T; VK stranger-replay = computing
  the XOR against the build; /compress-and-unfold fold = the contraction step),
  but **kept graph-internal as a conjecture in the paper view** — CITATION GUARD:
  the cross-paper synthesis is author's-own-prior, NOT a load-bearing citation;
  the published claim rests on standard results, the synthesis stays a self-link.
  Own conjecture node in §future-work. `future work / conjecture` · §future-work
  · KILL K8
- **FW3.** (2026-06-13) *In-context abduction degrades with DIFF SIZE.* Holding
  the harness fixed, a model's ability to self-compute the XOR over a diff
  degrades as the diff / case-space grows: langing a large structured operation
  is the failure mode /dont-lang-what-you-can-math already names (code-as-input →
  hallucination). NOT model size (author correction 2026-06-13: "especially large
  ones" = large diffs). GROUNDING (author override 2026-06-13, render pass): the
  diff-size claim is a **CONTEXT-ROT story, NOT a lost-in-the-middle story**.
  lost-in-the-middle is POSITIONAL (mid-context placement) and was CUT as a lazy/
  bandwagon cite (codex concurred: it grades placement, not size; author: "you're
  just wanting to cite it because everyone else cites it"). The real, author-owned
  ground = **/context-synthesis-is-quadratic** (self-link): the XOR is a SYNTHESIS
  task (relate cases pairwise to find the mishandled one), so its load grows with
  the SQUARE of the case-space where a fact-lookup grows linearly → super-linear
  in-context degradation. **context rot** (Chroma 2025) kept as the named
  phenomenon (fall-off as input grows), scoped honestly: names the shape, NOT a
  measurement of XOR degradation; flag the missing direct measurement rather than
  borrow a result that grades something else. /dont-lang-what-you-can-math = the
  math-vs-lang framing.
  TWO REGIMES: (i) ENDPOINT, by construction, NO experiment — when the XOR's
  operands exceed the context window, in-context computation is impossible by
  definition, so externalization is the ONLY option at scale, not merely better
  (and the codebase outgrows any finite window eventually); (ii) INTERIOR, graded
  — within the window but large, it degrades (the conjecture part, context-rot
  supported, the K9 sweep). The endpoint proves the mandate; the interior is the
  falsifiable claim. Conjecture-grade for the interior; the Verus receipt is one
  diff size. `future work / conjecture` · §future-work · KILL K9

## Kill conditions (what would break the paper)

- K1. Oracle bracket fails to replicate (C1) → attribution table collapses.
- K2. Audit spine refuted by grep on its own receipts (D1/D2) → instrument
  finding falls; the nulls lose their attribution.
- K3. flux receipt fails replay, or a discriminating program shows the graph
  fix wrong (E4) → mechanism evidence returns to zero cases.
- K4. Right-regime craft-only passes everywhere as cases accumulate (E6) →
  smem redundant even where built to matter; commit the null (the thesis's own
  falsifier, stated in hygraph-mechanism README).
- K5. A leaderboard submission combining equal receipts + higher rate (B4)
  → artifact claim falls by citation.
- K6. (2026-06-12) Verus #2219 fails to replay on the clean forced-fresh
  harness, or a discriminating program shows the externally-calibrated fix
  wrong where #2501 is right (E7) → the lead mechanism evidence collapses.
- K7. (2026-06-12) The encoding boundary (E8) is refuted: a purely
  self-calibrated model reaches the XOR's hard arm (calibration turns out
  inducible after all), or an internally-calibrated method reaches general
  on a localization-hard bug → "enumeration inducible, calibration not" falls,
  and with it the sharpest claim of the re-spine.
- K8. (2026-06-13) XOR-necessity (FW2) dies: exhibit inquiry reaching a sound
  generalization that carries warrant, with NO step computing disagreement
  against a reference outside the inquirer's own belief. Lucky guesses don't
  count (no warrant); already-solved cases don't count (H △ T already empty).
- K9. (2026-06-13) Diff-size degradation (FW3) dies: a within-harness sweep over
  diff / case-space size shows in-context XOR accuracy flat or rising with size.

## Propagation of the inverted arc (2026-06-10)

Done:
- [x] Title + slug → *The Hypothesis Graph: Semantic Memory Written by Methodeutics*; draft marker dropped; redirect stubs removed.
- [x] Cost-as-virtue cut paper-wide (B4/K5); cost survives only as a receipt/ledger; replication narration → repo pointer.
- [x] Abstract rewritten as **hook + bold promise** (beyond corpus synthesis, discovery-not-recall, hygraph as the instrument, bench demoted to "least insightful artifact"). Methodology/ablation/audit detail kept in the intro/body, not the abstract.
- [x] Intro: discovery foreshadow added after the substrate ¶ (attested mechanical reasoning, old-news guard); example ¶ promoted with convex-hull / creative-act / Sutton; ladder lead-in flags importance ⟂ confidence; claim 4 sharpened to the discovery peak.

Remaining (deeper sections):
- [x] §4 grounding → thesis-2 callback landed at section close, qualified ("in a precise and limited sense... not a theory of mind, but a mechanical discipline of inquiry") to state the claim without the philosophy fight.
- [x] §11 right-regime (E) → "what the existence proof establishes" now lands discovery / built-not-recalled / reproducibility-at-the-example / Sutton discharge. Eight nulls kept honest.
- [x] §12 discussion + P5 → P5 reframed as the peak ("the claim the other four exist to support"); creative-act now carries an operational criterion (novel, sound, useful, corpus-absent, replayable — each clause a receipt); Sutton bookend closed. Legibility "confession" → "question" (intro de-confessed).
- [x] B/C/D sweep → already bounded post-reversal ("the chart scales the artifact; it ranks nothing"; "what the number is not"); no centerpiece overreach found.
- [x] §audit → "applicability, not fault" scope guard added (not "discredit"); bench is N/A to this construct, fair measure of spec-conformance.

Next:
- [ ] /copyedit one clean pass over the whole settled paper (user: after the rewrite).

## Propagation of the RE-SPINE (2026-06-10, supersedes the inverted arc)

The inverted arc still rendered the bench (B) up front as bait, then pivoted
(C/D) to the witness (E). The re-spine moves E onto the spine BEFORE the bench
and corners B/C/D into a single §8 ("The bench, bounded"). The motivation,
substrate (A), epistemics (F/T), and existence case (E4) are unchanged; the
frame is what moved. Almost a new paper, but the load-bearing bits persist.

Done:
- [x] Section reorder: harness → Procedure (mechanism) → Results (mechanism) →
      The bench, bounded (cornered, ## with ### Number/Attribution/Audit) →
      Discussion. Anchors preserved (autonumber resolves §(id) regardless of
      order); {#right-regime} now on Results, {#setup} on Procedure, {#bench} new.
- [x] Procedure + Results rewritten from the hygraph-mechanism worklog: two arms,
      essence oracle, contamination control, nine pilots = eight nulls + one
      divergence (flux #1613). Worklog digest is faithful (8 nulls confirmed:
      qrtool/slang-server/fjall/bat + others; flux #1613 the divergence).
- [x] Bench number reframed: stated once, "property of oracle availability, not
      the harness or method"; named as the mistake; minimal prompt reaching ~94%
      = the attribution made plain (craft-only jargon → "minimal prompt").
- [x] Cut the flipt worked example; gating + outer-loop compressed to one
      sentence (table stakes).
- [x] Checkpoint committed (e0d86c3c).

Done (trim + strengthening, committed cc177d07 / 979195cf):
- [x] **B/C/D condensed pointer-first.** The 5 attribution sub-analyses folded to
      the table + one paragraph ("Given the oracle, the rest adds almost nothing");
      statistics point to the repo; oracle-bracket + minimal-prompt attribution kept.
      Audit reduced to a vague "wrong tool for the job" (no companion paper exists
      yet, no justification needed). Open-weight run cut to one sentence; SWE-bench
      Verified dropped from the body. Number stated once in prose. Orphaned anchors
      repointed (prompt-ablation/perturbation → attribution-verdict, open-weight-run
      → models, tables → results).
- [x] **Cross-model replication** (E4-replication) + **unsound result leads the
      §Discussion enemy block** (#3) + **"How to refute this" falsifiers in
      §Limitations** (#4). Anatomy figure on the dimmer example.
- [x] **Sutton split out.** May-2026 talk briefly added to §P5 then reverted; now
      its own post (`2026-06-10-suttons-recipe-for-discovery.md`,
      /suttons-recipe-for-discovery), a table-driven pointer back to the paper.
      Keeps the paper from bloating.

## BACKLOG (groomed 2026-06-12; supersedes the 06-10 TODO)

**A — Biggest open content piece — DONE 2026-06-12.**
- [x] **A6/A7 propagated into §3 (`{#hygraph}`).** Added: invariant promoted to a
      named contract + the skeleton/payload split + smart-constructor admission;
      the **local replay auditability** punchline with strong-vs-artifact replay
      grades + prune-as-corollary; the honest cost register (checkable skeleton vs
      trusted mode-label); the three "isn't this just X?" rebuttals (TMS /
      provenance log / search-proof-tree) + the verifiable-log/certificate genre
      ("binds opaque content to an executable evidence envelope"). SCOPE CHOICE:
      rebuttals done as PROSE, not a second table (Related Work already has the
      comparison table) — middle scope, per the over-engineering guard. The
      "minimal = ReAct, bolt-on onto codex/Claude Code" line belongs at the
      comparison point → tracked in B, not §3.

**B — Paper coherence + smaller content:**
- [x] **Expand §grounding into the machine-legible epistemology arc (A8).** DONE
      2026-06-12. §grounding retitled "methodeutics and a runnable epistemology";
      the one-line pragmatist-credence replaced with the full belief→knowledge→truth
      arc (italic-header subsections parallel to the Peirce modes), grounded by
      reference (belief-is-edge start, truth-is-buildable terminal); node-states
      mapped witnessed/killed/open = true/false/untrue; build-parts 1:1 (provenance/
      citation/attestation/falsifiability/replay); replay invariant framed as
      "this epistemology made local." Novelty scoped narrowly (warrant ledger, not
      a new logic). Three-leg synthesis closes the section. §12 "Truth is buildable"
      block trimmed to a §grounding callback (no re-derived mapping; pointer-first).
      **"agent-native epistemics" KEPT as a coinage (author call 2026-06-12, reversed
      an initial de-coin): named as the territory in §grounding AND added to the
      subtitle** ("Agent-native epistemics: merit attaches to the work, not the
      doer"); sits next to DeepMind's "artificial epistemic agents" (§12) and Traxia
      (§typed-memory).
- [x] **Related Work: add the epistemology-grounding neighbors** (A8 prior-art). DONE
      2026-06-12. New §typed-memory paragraph: NARS (addressed head-on), OpenCog
      AtomSpace/PLN, nanopublications, **Traxia** (arXiv 2606.08256, concurrent, two
      days after truth-is-buildable, 4th convergence/first on epistemology leg).
      Framed distinct from the cogarch-MEMORY cluster; synthesis-attack reply +
      warrant-ledger-not-new-logic stated.
- [ ] Full **front-to-back coherence read** (the §method/harness section, and the
      abstract→intro→Procedure→Results→Discussion handoffs) — not done; many edits
      landed piecemeal.
- [ ] Name **"minimal arm = mini-SWE-agent = ReAct, bolt-on onto codex/Claude
      Code; baseline = harnesses unmodified"** at the point of comparison
      (§Procedure / §3 positioning) — pre-empts the strawman objection.
- [ ] **Cover & Thomas (DPI)** reference entry in the lineage appendix (the §Results
      DPI sentence cites it inline; no bib entry yet).
- [ ] **Trim pass** (author-deferred): the additive Results ¶s run long.
- [ ] **Discussion trim, pointer-first** ("Truth is buildable" → a pointer, not a
      re-derivation).
- [ ] **Compress AI-authored ¶s** (intro pains→gap, §Procedure, §hygraph
      constraints); tighten, leave the author's prose alone.
- [ ] Standardize the one stray "falsification condition" → "kill condition".

**C — Receipts / substance (author's hands):**
- [ ] **More existence cases (E6):** 3–5 audited under the preregistered protocol →
      upgrades the n=1 language; else the committed null is the next paper.
- [ ] **One-command Verus replay** (re-scoped from flux): reproduce the divergence
      on a clean forced-fresh build; bake in the vendored-crate / stale-binary
      gotcha. Kills the "I can't verify this" dismissal.
- [ ] *(Lower — flux demoted)* flux #1613 maintainer merge is now an auditability
      footnote, not the keystone; the keystone is a Verus-grade trace-backed merge.

**D — Release housekeeping:**
- [ ] **PDF rebuild** (`scripts/build-paper-pdf.sh`) + fix the stale download slug
      (`methodeutic-harness-paper.pdf`).
- [ ] **Zenodo DOIs** → §availability placeholders.
- [ ] **Push + deploy** (refresh the stale SHAs before relying on them).

**Done this session (2026-06-12):** oracle terminology sweep (calibration→oracle);
§Procedure rewrite to the Verus externalized-oracle method; flux cut to a brief
mention; four-claims alignment (claim 3 accountability-only); falsifiers K6/K7;
intro voice-mining; abductor in §availability + future-work; the earned DPI
sentence; alignment de-emphasis (goal-predicate facet **CUT**); §verus-bench setup
(two goldens) + historical-PR-post-cutoff method; A6/A7 graph spec + two codex
sniffs (DS-scope; framing/replay); the addition-vs-subtraction *why*; CURRENT STATE
block + history demarcation.

**Done earlier (06-10):** Sutton bookend; title/slug; cost-as-virtue cut;
abstract hook; intro discovery foreshadow; §4 thesis-2 callback; §audit
applicability-not-fault; B/C/D bounded.

## TERM DECISION 2026-06-12 (venue: arxiv cs.AI + cs.SE)

The noun **"calibration" collides with probability-calibration** (ECE, confidence
calibration), which is entrenched in cs.AI and would miscompile the claim in the
abstract/title where it travels without a gloss. Decision (author): in the **paper**,
the noun for the external ground-truth source is **"the (ground-truth) oracle"** —
collision-free in both fields, SE-native (test oracle), and it *unifies with the
paper's own spine* (oracle bracket, essence oracle, self-certification = the model
being its own oracle). The **verb** "calibrate against a known-good reference"
(metrology sense) is kept where it reads naturally. Headline is now **"Enumeration
is inducible; the oracle is not."** First use in §Results carries a one-clause gloss
distinguishing the metrology sense from probability-calibration. This graph keeps
"calibration" as internal shorthand in the nodes below; the paper view uses "oracle."
Mapping when propagating: internal calibration → self-graded / the model as its own
oracle; external calibration → an external oracle; "calibration is not self-inducible"
→ "the oracle is not self-generable."

## Propagation of the 2026-06-12 re-spine (Verus lead, oracle axis)

Done in the paper view (`...the-hypothesis-graph-semantic-memory-methodeutics.md`),
additive pass (trim deferred per author):
- [x] §Results recast as a mechanism arc: contrast-sharpened (A5) → instrument
      general & blind (D7) → the lift E7 (Verus) → frontier-is-coverage → E8
      (enumeration inducible, calibration not) → ablation grid → flux E4 demoted
      to "audit not lift" → §null-regime (E3 preserved).
- [x] Axis fixed to internal-vs-external calibration (A5); grid relabeled
      ("Kill calibration": internal / external (vs base) / internal (induced) /
      human). Carrier-is-incidental / harness-layer stated.
- [x] Abstract, claim-2, contribution ¶ → encoded-reasoning spine, positive
      mechanism, no n=1 apology. (Witness swapped flux→Verus.)
- [x] F8 dunk facet rendered in §Discussion (between persistence and trust).
- [x] `abductor` (D7) added to §availability; future-work repointed to
      gate-coverage + calibrate-from-approved-history (E9).

Remaining (now tracked in `## BACKLOG`):
- [x] §Introduction mining (ancestor voice + dial-dunk, anchored on Verus). DONE.
- [x] §Procedure widened to the oracle framing (self-graded vs external oracle). DONE.
- [x] Headline witness swap flux→Verus (paper Results lead with Verus; graph P5/F5a fixed). DONE.
- [ ] Trim pass → BACKLOG B. PDF rebuild → BACKLOG D.

Done (graph) 2026-06-12 — calibration=goal-predicate + cognition mine:
- [x] E8 recast: "calibration not *self*-inducible" (codex scope); grounded in
      goals-are-predicates + grading-yourself-is-fiction + DPI. P4 alignment
      sharpened to the external-goal-predicate claim. F8 dunk grounded in DPI.
      F9 cognition-grounding index added. K7 falsifier specifies "independent
      labels."

Remaining (paper, ground by reference — link-anchors carry it, NO inline re-derivation):
- [~] §12 alignment: a goal-predicate facet was added THEN **CUT entirely**
      (author 2026-06-12: "don't pick fights with alignment people"). Net: no
      goal-setting in the paper; only the pre-existing accountability-as-alignment
      language stays. Goal-as-predicate is graph-internal only (P4 de-emphasis).
- [x] §Results enum-calib: DONE — one earned sentence in standard language
      ("no computation on what a model already holds can increase what it tells
      us about the world, the data processing inequality... calibration is a
      world-facing trial") + /compress-and-unfold self-link. **CITATION GUARD (author 2026-06-12): the world isn't
      ready for the natural framework as a load-bearing citation.** The paper
      rests on the STANDARD DPI (textbook info theory, Cover & Thomas 1991), with
      /compress-and-unfold as an optional author's-own-prior self-link (blog
      register). Keep /the-natural-framework AND the Perceive-morphism mapping
      OUT of the published view — graph-internal grounding only — until the
      framework is established; citing it couples the narrow, un-dismissable
      mechanism claim to a wide unestablished synthesis and hands a hostile
      reader a free exit. NO "Perceive," no six roles, no boundary-morphism in
      the paper.
- [x] Claim-verb pass per /wrong-questions: DONE — added to §discussion
      "Attributed nulls and the typing protocol": typing runs on positive claims
      too (Verus = a mechanism that *can occur*, not a rate/discovery);
      reflex≈kill, demotion≈credence-cap stated as the hygraph's own instances;
      links /type-iii-error + /wrong-questions.

## Propagation of the 2026-06-13 re-spine (abduction declared; multi-model; XOR=math)

Trigger: author session 2026-06-13. The lift is no longer framed as "a mechanism
shown once"; it is framed as **abduction, the unnamed third mode, externalized as
a math op** (T3), shown on one bug (existence) and reached-for by every model
(necessity), explained by the encoding boundary, and seated in the data structure.
New evidence merged to `hygraph-mechanism` master (branch
`pilots-11-fable-minimal-ablation`): multi-model gate2 (Fable / Sonnet / Composer
near-A; codex-CLI out) + fairness control + codex retraction.

What changed (graph, this file):
- [x] CURRENT STATE → 2026-06-13: four-beat arc; XOR-on-diffs = math-not-lang;
      multi-model evidence + retraction-safe wording; two inferred mechanisms;
      de-frame "mechanism"; magnification inventory. Thesis bullet names abduction.
- [x] **T3** added (the declaration): abduction unnamed/underappreciated; triad
      completion expands capability; instrument hooks, data structure is the gift.
- [x] **FW2** (XOR-on-diffs is the necessary, necessarily-external operation of
      inquiry; cross-paper spine, graph-internal conjecture) + **K8**.
- [x] **FW3** (in-context abduction degrades with DIFF size, not model size;
      grounded by reference to /dont-lang-what-you-can-math) + **K9**.

Remaining (paper view `...the-hypothesis-graph-semantic-memory-methodeutics.md`),
render pass 2026-06-13 (build verified, 503 pages, anchors resolve):
- [x] **Abstract + §intro claims: T3 foregrounded — APPROVED ("commit, but soften")
      + committed 2026-06-13.** Epigraph + amnesiac-contractor opening left intact
      (proposed-first, not overwritten). Abstract: two sentences seat abduction as
      the unnamed third mode (field owns deduction=compiler/types, induction=tests/
      benchmarks) + XOR-as-math-op tethered to the external oracle; SOFTENED per
      author — jewel stays primary ("holding all three as kill-graded nodes is what
      the graph is for, and one facet it lets you externalize is that abductive
      step"), NOT "first-class / sharpest demonstrated power"; closing "Externalizing
      that one step thus delivers...". Intro "more vs the other answer" ¶: abduction-
      as-missing-mode beat added, XOR tethered to §(application) (never floats free).
      Claim-2 retitled "A mechanism, dissected: abduction externalized"; closing
      clause → "deliver the abductive step the model does not reach alone". Encoded-
      reasoning spine + DPI + Verus witness + merit close all preserved. No em-dashes.
- [x] §right-regime / §enum-calib: multi-model robustness rendered as a "*Not one
      model's artifact*" paragraph after the corrected-calibration ¶. Retraction-safe:
      "workflows" not "families", "behavioral carve-out" not "same mechanism",
      "recall not required, not excluded", efficiency/endpoint NOT claimed (retracted),
      MANDATORY attractor caveat present (gate-funnelled, not independent
      rediscovery), codex-CLI does-not-clear-in-either-protocol + fairness control,
      read as coverage-bound NOT a scoreboard; necessity typed as the FW2 conjecture
      (no "must" in the empirical wording). Source: hygraph-mechanism RESULTS.md
      (Fable/Sonnet 4.6 clean, Composer 2.5 dirty, all near-A, same ho5 miss).
- [x] De-frame "mechanism": light pass. Retitle already in place ("Results: the
      mechanism, in full"). Softened 3 crutch uses to "lift"/"capability lift"
      (§other-cases ×2, §null-regime ×1); kept the literal causal uses (frontier
      "the same mechanism predicts its own failure"; §audit "predicted signature of
      a mechanism"; §discussion "a mechanism that can occur"; the "mechanism
      experiment" repo name). Count 33→~30; the keystone causal claims stay bold.
- [x] §grounding / §application: confirmed load-bearing and left intact — the
      three-modes figure + "Peirce alone named abduction" (§grounding) and the
      bi-abduction diff figure "the XOR isolates the figure from the ground"
      (§application) already tether the math-op claim; the proposed abstract/intro
      point the XOR claim at §(application) so it never floats free.
- [x] §future-work: FW2 (XOR is the necessary, necessarily-external operation of
      inquiry; cross-paper spine kept as self-links/suggestive, K8 kill stated) +
      FW3 (in-context abduction degrades with diff size; endpoint-by-construction vs
      graded-interior; lost-in-the-middle Liu TACL 2024 + context rot Chroma 2025 at
      conjecture grade, verify-at-camera-ready; /dont-lang-what-you-can-math anchor;
      K9 kill stated) added as two conjecture bullets after "Coverage as the design
      lever". §enum-calib forward-points to them.
- [x] Citation guard holds: XOR-necessity synthesis (WCBF/VK/compress-and-unfold)
      rendered as SELF-LINKS "suggestive rather than evidential", not load-bearing
      cites; the boundary still rests on standard DPI (Cover & Thomas, §enum-calib).

## Codex substantiation pass + author corrections (2026-06-13, render pass 2)

Codex review run focused on substantiation (not prose). Build green throughout
(503 pages). Applied, with author overrides that SUPERSEDE earlier node guidance:

- [x] **No novelty over abduction (author override, supersedes T3 "unnamed third
      mode").** Infer (bi-abduction) and Voyager (observe-hypothesize-test) BOTH did
      abduction, with success — paper now says so explicitly and disclaims novelty
      over the mode. Contribution reframed: abduction *fits in a harness, graded
      from outside the model, and lifts where nothing else did*. All "first"/
      "unnamed"/"no tradition built that one"/"first general reasoner" claims CUT
      (not hedged — author: "we're not playing territory-grabbing games; novelty is
      the XOR discovery + epistemology + the composition"). Abstract + intro + §3
      reworded; ToTh "Peirce" table cell fixed to "abduction/deduction/induction…
      (no Peirce cite)" to match the Related-Work text (codex caught the contradiction).
- [x] **XOR = bi-abduction, tether made EXPLICIT (author: "XOR is just a coded term
      for bi-abduction, we weren't making the link explicit enough").** "math op"
      scoped to "this harness operationalizes"; new identity sentence in §application
      names the XOR as shorthand for bi-abduction's figure/ground split (Calcagno/
      O'Hearn cited for what bi-abduction actually establishes, not for "XOR").
      Resolves codex's "floats free as a redefinition" flag by tethering harder, not
      softening away.
- [x] **DPI demoted to theoretic motivation (author: "DPI is mostly theoretic,
      proving it is out of scope").** §enum-calib DPI ¶ reworded "offered as
      motivation rather than proof… turning this into a theorem… is out of scope";
      Cover & Thomas kept, /compress-and-unfold self-link kept.
- [x] **FW3 regrounded (author: "large XOR is a context-rot story, not a
      lost-in-the-middle story"; "lost-in-the-middle is a lazy citation").**
      lost-in-the-middle CUT entirely. New ground = **/context-synthesis-is-quadratic**
      (author's own prior, self-link): XOR is a SYNTHESIS task → load grows with the
      SQUARE of the case-space → super-linear in-context degradation. context rot
      (Chroma 2025) kept as the named phenomenon, scoped (names the shape, not a
      measurement); missing direct measurement flagged, not papered over. See FW3
      node above (updated). FW2 kill sharpened to codex's operational form (de-
      tautologized: "self-authored labels only, no external label/replay/human-
      approved reference/environmental execution before the discriminating step").
- [x] **Multi-model wording tightened** (codex residuals): "reach"→"driven to";
      "recall not required for this fix-class"→"these runs do not require a recall
      explanation for this case"; "every instance reaches for"→"every successful run
      here uses the same externally supplied discriminator"; budget-artifact phrasing.
- [x] **NEW §bench framing (author, approved → §bench de-frame): observability /
      reliability / attribution, NOT performance.** Added ¶ to the §bench opener:
      benches grade performance, but a harness is bottlenecked on observability,
      reliability, attribution; the four intro problems are all of that kind; grounded
      on the existing null + SWE-Effi (gate×oracle fixed → model tier moves ~2pts).
      Author's "no harness lift with stronger models since 2025" intuition kept as
      MOTIVATION only — the substantiated kernel (SWE-Effi + pair-swap) is stated, the
      bald temporal claim is NOT asserted (no receipt).
- [x] "debugging tools discard the search" softened (codex: some keep logs) →
      "do not persist the search as a typed, replayable hypothesis graph".

NOT yet done: nothing committed to git (author to confirm). PDF rebuild still pending
(BACKLOG D). Cover & Thomas + context-rot + Capucci bib entries still owed in lineage
appendix if the inline cites are to resolve formally.

## Codex argumentation+order sniff (2026-06-13, render pass 3)

Sniff requested: argumentation + ORDER only, not prose. Applied Root A + Root B +
honesty scoping; declined the structural reorders (codex conceded the spine is
"basically right"; author concurred). Build green (503 pages).

- [x] **ROOT A — align the top to what the body earns (codex soundness #1/#5/#6/#9).**
      The contradiction: abstract/intro/§verus said "sound, general fix" / "recovers
      the verifier's own decision procedure", but §frontier reveals wide-but-broken.
      FIX: the model's external-gate fix is now "the verifier's own inhabitedness
      query, a markedly more general fix bounded by gate coverage"; the *fully sound
      general fix is the maintainer's (#2501)*. §verus reveals wide-but-broken AT the
      point of the claim (in place, not a reorder). Intro claim-2 now types Verus as
      "a mechanism that *can occur*, not a rate or a general boundary claim
      (§right-regime, §limitations)" — existence framing pulled forward (#9).
- [x] **ROOT B — graph=substrate vs oracle=intervention + axis tightened (soundness
      #2/#7).** §right-regime now states plainly: the graph is NOT what moves the
      number (every arm writes the same graph), the external oracle is; the graph is
      the persistent replayable SUBSTRATE + the contributed object + the reason it's
      auditable, and the experiment isolates ONE variable within it. Protects
      jewel-not-facet without overclaiming the graph as the causal lever. Axis
      tightened: externality is NECESSARY NOT SUFFICIENT — thin coverage → wide-but-
      broken (§frontier); the real axis is whether the externally-supplied labels SPAN
      the needed distinction.
- [x] **Honesty #3** — "the oracle is not" scoped in §enum-calib: "at least not here…
      scoped to that circularity, not a proof that no model could ever induce an
      oracle from some other source." (matches the E8/K7 graph scoping.)
- [x] **Honesty #4** — abstract DPI overclaim removed: "because by the data processing
      inequality no internal computation imports the world-truth" → "since the missing
      truth enters only from a world-facing trial, never from recombining what the
      weights already hold." DPI now appears ONLY in §enum-calib, already demoted to
      motivation/out-of-scope. Abstract/§enum-calib no longer inconsistent.
- [x] **Honesty #8** — bench circularity defused in §setup: the regime is the audit's
      INDEPENDENT complement ("marked it out independently, and before these results"),
      not chosen because the method wins there. Foregrounds the audit criterion ahead
      of the null.
- [~] DECLINED (codex order #3/#5/#6/#7-order; soundness #10): move gate-general after
      verus-bench, split enum-calib, reorder discussion, replay-auditability scoping.
      Spine kept; higher risk/effort, low argument gain. Revisit only if a later read
      snags. #10 (replay = checkability not sufficiency) already stated in §hygraph +
      §limitations; left as-is.

## Live-PR honesty correction (2026-06-13, render pass 4) — author: "we do as much honesty as we can"

Triggered by author Q ("is the general fix live on their repo"). Verified live via
`gh` on verus-lang/verus, and caught a FACTUAL ERROR the verification exposed.

- [x] **Live status confirmed:** #2219 CLOSED 2026-06-05; #2230 (narrow) MERGED
      2026-03-09; #2501 (general) MERGED 2026-06-05 (the merge that closed #2219).
      Provenance in the paper (base 2026-03-08 → narrow next day → general 2026-06-05)
      is accurate; post-cutoff for Fable (Jan 2026) holds.
- [x] **FACTUAL FIX — #2501 mis-attribution.** Paper said "the general fix replaces
      `is_never()` with the verifier's own inhabitedness query `!ty.is_inhabited_from`,
      which is what #2501 does." FALSE per #2501's live diff: #2501 KEEPS `is_never`
      and gates it by call context (`record_call_inhabitedness`, conservative on
      proof-block `!`-returns) = the MODE GATE, the finer fix. `is_inhabited_from`
      was the MODEL's over-broad route, behaviorally redundant (Fable: identical
      grading, no inhabitedness query). Corrected §verus line: #2501 described as
      mode-gated/context-aware, not is_inhabited_from.
- [x] **Lift recast to a mode-gated approximation (max honesty, per RESULT-corrected.md
      2026-06-12).** §frontier now states the cross-model correction: the
      inhabitedness query the codex arm routed through is behaviorally redundant; the
      operative mechanism is the mode gate; "the model recovered the verifier's own
      decision procedure / reached the verifier's true oracle" OVERSTATES → "widens to
      a mode-gated approximation under external pressure." Held-outs still earn
      represents-not-tabulates (the rule it represents is the coarse mode gate).
- [x] Knock-on overclaims scrubbed: abstract + intro "onto the verifier's own
      inhabitedness query" → "onto a markedly more general fix"; §verus "reach the
      general inhabitedness predicate" → "break off the narrow plateau to a wider
      fix" + "reused the real oracle" → "applies its own general predicate";
      §gate-general "discover the verifier's own inhabitedness query" → "grep out
      rustc's own machinery for uninhabited types"; §verus-bench recall probe
      de-conflated ("the model's solution is reconstruction from prior competence,
      not recall of the post-cutoff patch"); table caption "inhabitedness
      generalization" → "uninhabited-return generalization".
- [x] E7 node corrected above with the live-PR verification + the mis-attribution fix.
      NB: line-18 mechanism-bar prose still narrates `is_never()→is_inhabited_from` as
      the lift — that is the codex-arm ROUTE (accurate as trace), but the operative-
      mechanism gloss is now the mode gate; left as provenance, governed by this note.
Build verified (503 pages). Committed.

## Pull hygraph-mechanism + propagate (2026-06-13, render pass 5)

Pulled the receipts (branch `pilots-11-fable-minimal-ablation` @ 43ac2d0). The new
commit added the matched-codex table row and, the load-bearing change, flagged
**`#2501`-clears-`ho5` as INFERRED, not force-graded** (#2501 is at toolchain 1.95.0,
not co-gradeable with the base-toolchain 1.93.1 arms; force-grading gold-on-`ho5` is
a logged, unrun control).

- [x] **Paper (§enum-calib multi-model ¶): hedged the anti-recall claim.** Was stated
      as fact ("the human general fix is finer… clearing `ho5`… so a model that had
      memorized the gold would have cleared it"). Now contingent: "appears finer…
      would mean… but that `ho5` clearance is inferred, not force-graded here (#2501 at
      a different toolchain, not co-gradeable); logged as an open control, and the
      argument leans on it." The Fable/Sonnet recall-not-required point is unaffected
      (that is force-graded).
- [x] **Paper (ablation table caption): added the toolchain caveat** so the table's
      "#2501 clears divergence" does not assert more than was graded ("the maintainer
      fix's clearance of the hardest divergence probe is inferred from #2501 at its own
      toolchain, not force-graded alongside these arms").
- [x] **Receipts correction (hygraph-mechanism, branch, commit 823b811, NOT pushed):**
      `MECHANISM-dissection.md` step 5 said "this is the lift: the verifier's own
      general query" — corrected to the mode-gated-approximation framing inline, citing
      the live `gh pr diff 2501` (keeps `is_never`, gates by call context) + the
      RESULT-corrected cross-model redundancy. The receipts now match the paper.
- [~] Multi-model "matched-codex rerun leaves the divergence wall standing" already in
      the paper; the new receipts row (pass=false, crash=1250, p1 over-rej) corroborates
      it — no paper change needed. clean_regrade stat-order fix is repo-internal.
Build verified (503 pages). june.kim committed; receipts branch commit local (unpushed).
