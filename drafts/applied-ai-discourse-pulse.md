# Applied-AI discourse pulse (2025–2026)

Fan-out to find live rooms the hypothesis-graph / methodeutics work can write *into*,
not into the void. Four research branches → codex adversarial filter → converge on
2–3 rooms. Status: branch B in; A, C, D running.

---

## Branch B — Discovery + Reliability science  (general-purpose/opus, web; codex-filter PENDING)

**Verdict:** both sub-rooms have their *names* taken; the open slot is "the warrant is the trail, not the score" — discovery/reliability warranted by a replayable falsification trace, which neither camp occupies.

### Discovery / beyond-corpus-recall
- **CROWDED / LATE:** "post-cutoff ⇒ couldn't be recalled" is temporal holdout, owned since **LiveCodeBench** (arXiv 2403.07974, early 2024); SWE-rebench (2505.20411), SWE-MERA, SWE-bench++ all do post-cutoff decontamination. Do NOT claim novelty on the cutoff argument.
- **CONTESTED:** "impossible by provenance" is too strong — cutoff dates are fuzzy (RL post-training, inference-time retrieval can surface post-cutoff content; OpenReview EjiJmiA6ea). Recommended softening: **"recall is not evidenced, and unlike a benchmark the claim is auditable"** — sell the warrant mechanism (replay), not the metaphysics of "impossible."  ⚠️ *Bears on what we just shipped (the "post-cutoff data / impossible by provenance" framing).*
- **OPEN (the gap):** discovery as a **warranted single witnessed event** where the warrant is a *replayable inquiry trace*. The discovery-by-verifier camp (AlphaEvolve 2506.13131; Tao et al. 2511.02864) warrants by *external optimality proof*; the contamination crowd warrants by *aggregate dataset hygiene*. Nobody warrants by *process replay of an individual inquiry*.
- **Adversaries who'd kill "discovery":** Sakana-critique (2502.14297 — "novel to the model ≠ novel to the world," n=1 = anecdote); AlphaEvolve reviewers (real discovery = beats a known bound with external proof; a suite-green bug fix loses that word).
- **Closest stated-problem-different-answer:** Dami Gupta, "Can an LLM know that it knows?" (Medium, Feb 2026) — names "epistemic provenance" / "silent knowledge contamination," but answers via training-side machine-unlearning, not replay+audit.

### Agent reliability as a science
- **CROWDED:** the *name* "science of agent reliability" is planted — Rabanser, **Kapoor & Narayanan** et al., arXiv 2602.16666 (Feb 2026, Princeton CITP / *AI Snake Oil* crowd). 12 metrics over consistency/robustness/predictability/safety. Descriptive — they *measure*, don't *construct*.
- **CROWDED:** inference-level bitwise determinism — **Thinking Machines Lab** ("Defeating Nondeterminism in LLM Inference," Sept 2025), batch-invariant kernels.
- **OPEN:** determinism at the **decision/control layer** — "deterministic **gate over nondeterministic proposers**." Slot in as the *constructive* complement to Rabanser/Kapoor's *descriptive* science: achieve by architecture what they can only score.
- **Overclaim to avoid:** "our system is deterministic / every step replayable." Say "deterministic gate over nondeterministic proposers" (Thinking Machines kill: model calls aren't bitwise det). And keep **"replayable" (auditability) ≠ "reliable" (robustness)** — you can replay a consistently-wrong run (Rabanser kill).

### Most writeable-into (this branch): **"The warrant is the trail, not the score."**
Position against three named works: Rabanser/Kapoor 2602.16666 (construct what they measure), Dami Gupta Feb-2026 (provenance via replay+audit, not retraining), Sakana critique 2502.14297 (the single case survives *because* auditable). Legibility tax: this audience speaks safety-engineering/stats, not Peirce — translate methodeutics into consistency/predictability or pay for it.

---

## Branch A — Memory triad + Eval validity  (general-purpose/opus, web; codex-filter PENDING)

**Verdict:** both rooms more crowded than the paper assumes; in each, a recent paper sits almost on the thesis. Two SHIPPED-PAPER claims are now overclaims. The real opening is the *intersection*: falsification-as-memory with a deterministic gate.

### ⚠️ Bears on the shipped paper (corrections)
- **"LLM-agent memory reinvents the Soar/ACT-R triad WITHOUT citing the lineage" is FALSIFIABLE in one search.** **CoALA — "Cognitive Architectures for Language Agents"** (Sumers, Yao, Narasimhan, Griffiths; arXiv 2309.02427, **TMLR 2024**) explicitly maps language-agent memory onto Soar/ACT-R and the working/episodic/semantic/procedural split, and makes our exact analogy ("Soar uses production rules… CoALA replaces symbolic productions with LLM reasoning"). **Portable Agent Memory** (2605.11032) also cites Soar (Laird 1987) + ACT-R. → Narrow the claim to the defensible version: *vendor systems (Mem0, Zep, A-Mem, Letta/MemGPT) and the largest 2026 survey (2602.06052) ground the triad in Tulving-era psychology and skip the architectural mechanism + any soundness invariant.* Must cite CoALA as lineage we extend, not expose.
- **POPPER (2502.09858, Feb 2025) — "Automated Hypothesis Validation with Agentic Sequential Falsifications."** Sequential falsification with **e-value** error control. This is the falsification sibling, and our own `investigate` skill uses the *same* e-value machinery → must cite or we're reinventing it. Differentiate on *deterministic kill gate + persistence/replay* (POPPER is ephemeral + statistical gate).
- **FVDebug (2510.15906)** — an actual hypothesis graph for debugging (nodes, frontier, evidence) but **node selection is LLM-arbitrated** — exactly the arbiter we remove. Closest structural sibling; differentiate on "no model arbitrates the edge."
- **"Peirce pipeline for agents" is TAKEN** — "From Reasoning to Learning" survey (2505.21935, TMLR 2025) + IDEA (2408.10455) already cast agents as abduction→deduction→induction. Differentiator is the same: *induction = deterministic gate, not an LLM judge.* **Lead with the gate, not Peirce.**

### Memory thread
- CROWDED/owned: CoALA owns Soar→triad; 2025–26 surveys own the taxonomy (2602.06052 60+ authors; 2512.13564; 2603.07670); vendors own substrate (vector/graph/parametric).
- Provenance just emerging (2026) as *cryptographic integrity for portability* (Portable Agent Memory, Merkle-DAG/Ed25519) — NOT as a soundness invariant on inquiry.
- GENUINELY DIFFERENTIATED: semantic slot = a *typed, replayable falsification graph with deterministic kill edges*. No memory paper makes smem a falsification structure; provenance verifies *integrity*, we verify *warrant*.

### Eval-validity thread
- CROWDED (went open→crowded late-2025→mid-2026): **ORACLE-SWE (2604.07789)** quantifies oracle/spec leakage; **SLUMP "When the Specification Emerges" (2603.17104)** opens with our exact premise (benchmarks hand over the full spec, real coding doesn't); **What's in a Benchmark (ICSE-SEIP 2026, 2602.04449)**; OpenAI's "why we no longer evaluate SWE-bench Verified." → "tasks hand over the spec" as a *finding* is 3–6 months late.
- DIFFERENTIATED: the **"not applicable" verdict as a TYPE/CATEGORY claim** (running a diagnostic harness on a conformance bench is a type error, not a low score) — everyone else treats handover as a *bug to fix with a better benchmark*; we draw the *boundary* they keep crossing. Pair with the replay invariant (auditable warrant a pass/fail oracle structurally can't grade).

### Most writeable-into (this branch): **falsification-as-memory with a deterministic gate.**
The hole nobody fills: typed falsifiable nodes + a *deterministic non-LLM* kill gate + a *replay* soundness invariant, installed as the *semantic-memory slot of a Soar-style architecture*. POPPER has the gate, no memory; FVDebug has the graph, an LLM arbiter; CoALA has the slot, no falsification; provenance/replay people verify integrity, not warrant. In-conversation set: POPPER (cite first, highest overlap), FVDebug, CoALA, Portable Agent Memory, ORACLE-SWE/SLUMP.

---

## Branch C — Provenance + Verification  (general-purpose/opus, web; codex-filter PENDING)

**Verdict:** the seam is "reproducible ≠ re-derivable." Provenance taxonomy + receipts/replay are all shipped (2026); the empty rung is *evidentiary sufficiency* — a trace a hostile reader reruns to re-derive the **conclusion**, not just confirm the **events**.

- **Provenance taxonomy OWNED (weeks old):** *From Agent Traces to Trust* (2606.04990, Jun 2026) — enumerates provenance relations **including Contradict & Invalidate** (our kill conditions, but as inert descriptive schema, not the soundness engine), and lists "how provenance quality should be evaluated" as an OPEN problem. Also 2602.13855 (claim-level auditability), 2603.17445, 2603.21692.
- **Receipts/attestation now CROWDED (regulatory-driven, EU AI Act Art.12 / DORA):** Pipelock (`pipelock verify-receipt`), ARC-Hermes (`export-replay`), Verifiability-First Agents (2512.17259), 2603.14332. ⚠️ our phrase "one-command replay (receipts)" collides almost verbatim — must distinguish.
- **The two nearest neighbors to cite by name:**
  - **DFAH / Replayable Financial Agents (2601.15322)** — nearest on "replay as audit"; its own concession is our doorway: *"replay alone doesn't guarantee a third party independently derived the same conclusion; it only confirms the system behaves consistently."*
  - **From Hypotheses to Factors (2604.26747)** — nearest on "falsifiable hypotheses + deterministic engine + append-only trace," but domain-locked to quant factors. If we don't cite it, a reviewer will, and it reads as the thing we reinvented.
- **The ladder (top rung empty):** 1 Trace (telemetry — vendors own: LangSmith/Langfuse/Phoenix/OTel GenAI) → 2 Attestation (tamper-evident — receipts) → 3 Determinism-replay (same in→same out — DFAH) → **4 Evidentiary sufficiency (hostile reader re-derives the conclusion, trusting nothing) — UNCLAIMED as a named bar.**
- Overclaim to avoid: don't say tracing is "just debugging, nobody treats it as evidence" — false in 2026. Attack rung 3 (determinism), not rung 1 (a strawman).

## Branch D — Governance gates + Multi-agent custody  (general-purpose/opus, web; codex-filter PENDING)

**Verdict:** governance-as-gate is TAKEN (don't claim security). Multi-agent epistemic custody is HALF-OPEN — the framing is live, the typed kill-conditioned ledger is the gap. The genuinely unoccupied asset is the methodeutic deterministic ROUTER.

- **Governance/security as mechanical gates — CROWDED & CONVERGED, do NOT enter as a security thesis:** **CaMeL** (DeepMind, 2503.18813) is our exact idea (untrusted output never touches control flow; deterministic policy engine; "provable security"). **"Deterministic Architectural Boundaries" (2602.09947, Feb 2026)** formalizes our thesis in our own words: *policy gates, kill conditions, "no model in the trust path."* Invariant Labs (→Snyk) ships it. AgentDojo (2406.13352) is the benchmark, with red teams. ⚠️ claiming "security" = out of our depth.
- **Multi-agent epistemic custody — HALF-OPEN, the seam is clean:** **"Architecting Trust in Artificial Epistemic Agents"** (DeepMind, 2603.02960, Mar 2026) names our exact pains (ungrounded consensus, attribution, disagreement) but is a *principles paper with no mechanism* — the missing implementation is ours. The Ledger Delegation Protocol (2603.18043) tracks *who delegated to whom* (identity) but explicitly NOT hypotheses/conflicting evidence. Debate-consensus fixes (Free-MAD, CONSENSAGENT) are prompt-level, not structural. Single-agent hypothesis-DAGs exist (**InquiTree 2606.09550**, HypoAgent, AgentCDM/ACH) — none has shared custody + firing kill-edges.
- **DIFFERENTIATED:** *disagreement as graph structure, not chat residue* — typed nodes only, consensus disallowed without an evidence-bound trial, kill-edge fires mechanically so a retired hypothesis can't be silently re-agreed-into-truth. Nobody combines typed epistemic content + mechanical kill-conditions + shared custody. "Epistemic custody" naming is available.
- **The unoccupied asset:** the **abduce→deduce→induce deterministic predicate router**. The abduction literature (incl. 2604.08016 "Wiring the Why") treats abduction as a capability to elicit from a model; nobody routes between inquiry modes by mechanical predicate. The "deterministic gate, no model arbitrates" principle is already *validated and respected* on the safety side — transplant it from safety (taken) to inquiry-mode routing (empty).
- **Biggest exposure (convergent w/ Branch B):** replay-soundness under nondeterministic tools/env. **CodeTracer (2604.11641)** + SWE-agent literature: agent runs don't replay even at temp 0. "Soundness = replay" is a non-trivial systems claim — address head-on or get caught.

---

## CONVERGENCE (cross-branch)

**Convergent across A+C+D — the novel core is the INTERSECTION, not any single idea.** Each of the three signature ideas has a 2026 sibling; none combines all:
- typed falsifiable hypothesis NODE → FVDebug (LLM-arbitrated), InquiTree (no kill-edges), HypoAgent
- deterministic KILL-GATE no model arbitrates → POPPER (statistical, ephemeral), CaMeL/2602.09947 (safety only)
- REPLAY as soundness invariant → DFAH (concedes ≠ re-derivation), Portable Agent Memory (crypto integrity, not warrant)
- as the smem SLOT of a Soar architecture → CoALA (no falsification)
- domain-locked full combo → From Hypotheses to Factors (quant only)

**Convergent corrections to the SHIPPED paper (urgent):**
1. "reinvents the triad without citing the lineage" → FALSE (CoALA 2309.02427 cites Soar/ACT-R). Narrow + cite CoALA.
2. "post-cutoff ⇒ recall impossible by provenance" → LATE (LiveCodeBench temporal-holdout) + CONTESTED (cutoff fuzzy). Soften to "recall not evidenced, and unlike a score it's auditable."
3. "Peirce pipeline" → TAKEN (IDEA 2408.10455, survey 2505.21935). Lead with the GATE, not Peirce.
4. "tasks hand over the spec" → LATE (ORACLE-SWE 2604.07789, SLUMP 2603.17104). Keep only the *category/"not applicable"* move.
5. Missing must-cite siblings: **POPPER (2502.09858 — our own investigate skill uses its e-values)**, FVDebug, From Hypotheses to Factors, DFAH, From Agent Traces to Trust. "one-command receipts" collides with Pipelock/ARC-Hermes.

**The 2–3 rooms worth writing INTO (pre-codex):**
- **ROOM 1 — "Re-derivable, not just reproducible" (evidentiary sufficiency).** The empty top rung. Hygraph = the unit that makes a conclusion re-derivable by a hostile reader (typed falsifiable nodes + deterministic kill-edges + replay). In conversation with DFAH (2601.15322), From Agent Traces to Trust (2606.04990), From Hypotheses to Factors (2604.26747). *Strongest; unifies the program.*
- **ROOM 2 — Constructive complement to the science of agent reliability.** "Deterministic gate over nondeterministic proposers" *achieves by architecture* what Rabanser/Kapoor (2602.16666) only *measure*. Lead with the gate; translate to consistency/predictability.
- **ROOM 3 — Multi-agent epistemic custody.** Typed kill-conditioned shared ledger; the implementation DeepMind's 2603.02960 poses but doesn't build. Hottest-but-open extension; naming available.
- **Unifying machine (Branch D):** one harness — hygraph as shared epistemic ledger, kill-edges fire on replayable trials, abduce/deduce/induce as a deterministic predicate router, governance as the special case where the kill-condition is a safety policy.
- **Standing exposure to address up front in any of these:** replay-soundness under nondeterministic tools/env (CodeTracer 2604.11641).

---

## CODEX CONVERGENCE (web-verified quotes) — the slide-in target

**WINNER: "From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents" (arXiv 2606.04990).** FIT 9.5/10. The cleanest, least-over-read slide-in — it *names our machinery and leaves it unbuilt*. Verified quotes:
- > "the field lacks a unified view of what should be traced, how trace units should be connected, how provenance should be represented, and **how provenance quality should be evaluated** in agent systems." ← the open problem we answer (replay = the quality bar).
- > "we define seven relation types … Support, Derive, Depend-on, **Contradict, Invalidate**, Trigger, and Update." ← we make Contradict/Invalidate *executable kill conditions*, not passive labels.
- > "**Future provenance-aware agents should not only detect** unsafe or unsupported execution, **but also repair it.**"

**Ranked slide-ins (FIT × host strength):**
1. **From Agent Traces to Trust (2606.04990)** — FIT 9.5, host 7. *Write here first.*
2. **Towards a Science of AI Agent Reliability (2602.16666)** — FIT 7, host **9**. Verified: > "We **do not propose algorithms for improving reliability**" and future work: > "**optimizing agents directly for reliability dimensions** rather than capability alone." Slide in as reliability-by-construction (the gate). Highest-prestige host; needs us to show our metrics move.
3. **Architecting Trust in Artificial Epistemic Agents (DeepMind, 2603.02960)** — FIT 6.5, host 8. Verified: > "we propose the implementation of **robust falsifiability pipelines**" and > "True falsifiability requires that an agent's claims … are structured in a way that allows them to be **proven wrong**." Strong motivation, but normative — don't claim they asked for *our* mechanism.
4. **DFAH / Replayable Financial Agents (2601.15322)** — KILLED as primary (the "third party derived the same conclusion" concession was NOT found verbatim). Real, weaker gap: > "**a deterministic wrong answer is still wrong**." Keep as foil, not host.

**Codex adversarial flags:** DFAH slide-in was wishful (concession overstated). DeepMind is broad — motivation not mechanism-request. Reliability paper is adjacent — must show our construction moves *their* metrics. Agent-Traces is the only one with near-zero over-reading. One more host to vet: **TRACE (2606.07054)** — "connect evidence across temporally distant actions," but narrower/security-monitoring; related work, not host.

**Winner hook (codex draft, to refine):** *"Recent work on evidence tracing and execution provenance argues LLM-agent systems lack a unified account of 'what should be traced, how trace units should be connected, how provenance should be represented, and how provenance quality should be evaluated.' We answer this by introducing a replayable hypothesis graph: a typed semantic memory in which claims are falsifiable nodes bound to recorded trials, and Support/Contradict/Invalidate are executable kill conditions rather than passive labels — turning provenance from post-hoc explanation into a deterministic gate over abduction, deduction, and induction."*

---

## AGGRESSIVE CITATION MAP (to join the canon)

Every signature idea has a 2026 sibling; cite densely or be read as reinventing. Roles:

**HOST (slide into their open question):**
- From Agent Traces to Trust (2606.04990) — primary host; answer "how provenance quality should be evaluated" + make Contradict/Invalidate executable.
- Science of Agent Reliability (2602.16666) — secondary; reliability-by-construction.
- Architecting Trust in Artificial Epistemic Agents (2603.02960) — motivation; "robust falsifiability pipelines."

**LINEAGE (concede, then extend — fixes the shipped-paper overclaim):**
- **CoALA (2309.02427, TMLR 2024)** — *cites Soar/ACT-R already.* Concede it owns the triad mapping; claim the soundness invariant it lacks. ⚠️ REQUIRED — current paper's "without citing the lineage" is false against it.
- Soar (Laird 1987), ACT-R (Anderson) — the actual lineage.

**SIBLINGS (differentiate, by name — non-negotiable or a reviewer cites them for us):**
- **POPPER (2502.09858)** — falsification + e-values; *our own investigate skill uses this machinery.* Differentiate: deterministic kill gate + persistence/replay.
- **FVDebug (2510.15906)** — hypothesis graph for debugging, LLM-arbitrated. Differentiate: no model arbitrates the edge.
- **From Hypotheses to Factors (2604.26747)** — falsifiable + deterministic engine + append-only, quant-locked. Differentiate: general smem substrate, not a domain harness.
- **Portable Agent Memory (2605.11032)** — Merkle-DAG provenance, cites Soar/ACT-R. Differentiate: replay/warrant vs crypto integrity.
- IDEA (2408.10455), "From Reasoning to Learning" survey (2505.21935), "Wiring the Why" (2604.08016) — Peirce-pipeline siblings. Differentiate: deterministic mode-router gate. **Lead with the gate, not Peirce.**
- InquiTree (2606.09550), HypoAgent, AgentCDM/ACH — single-agent inquiry DAGs; extend to shared custody + firing kill-edges.

**EVAL-VALIDITY NEIGHBORS (cite to establish the problem is real, then make the category move):**
- ORACLE-SWE (2604.07789), SLUMP "When the Specification Emerges" (2603.17104), What's in a Benchmark (ICSE-SEIP 2602.04449), OpenAI "why we no longer evaluate SWE-bench Verified." Our move: "not applicable" as a *type* claim, not a measurement gripe.

**FOILS / CONTRAST:**
- DFAH (2601.15322) — "deterministic wrong answer is still wrong"; receipts (Pipelock, ARC-Hermes, 2512.17259) — attestation ≠ re-derivation.
- Thinking Machines "Defeating Nondeterminism" (2025) — say "deterministic gate over nondeterministic proposers," never "deterministic system."

**GOVERNANCE (cite as validated principle we generalize — do NOT claim security):**
- CaMeL (2503.18813), Deterministic Architectural Boundaries (2602.09947), Invariant/Snyk, AgentDojo (2406.13352).

**EXPOSURE to pre-empt:**
- CodeTracer (2604.11641) — agent runs don't replay even at temp 0; "soundness = replay" is a non-trivial systems claim; engage head-on.
- Sakana critique (2502.14297) — "novel to the model ≠ novel to the world," n=1 = anecdote.
- LiveCodeBench (2403.07974) — owns temporal-holdout; don't claim novelty on "post-cutoff."

---

## NEXT ACTIONS (for the human)
1. **Patch the shipped paper** (urgent): fix "without citing the lineage" (cite CoALA); soften "impossible by provenance" → "recall not evidenced + auditable"; add must-cite siblings (POPPER, FVDebug, From Hypotheses to Factors, From Agent Traces to Trust); lead methodeutics with the gate.
2. **Next paper**: write INTO 2606.04990's open problem — "the hypothesis graph as the executable provenance layer" / "re-derivable, not just reproducible."
3. Hold ROOM 3 (multi-agent epistemic custody) as the paper after — implement DeepMind's 2603.02960 falsifiability-pipeline agenda.
