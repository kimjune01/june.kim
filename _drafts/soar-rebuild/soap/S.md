---
system: Soar
target: SoarGroup/Soar
stage: production/legacy
stage_rationale: 40+ years of active development, maintained by the Soar group at University of Michigan under original architect John Laird. Current release is ~9.6. Active PRs and merges on SoarGroup/Soar as of 2026. Under production/legacy stage, gaps are presumed deliberate design commitments unless there is explicit evidence (issue tracker, author correspondence, rejected PR, published retrospective) that the gap is an acknowledged oversight.
intake_run: 2026-04-09
intake_prior: Prior intake produced 2026-03-23 diagnosis-soar, 2026-03-24 soap-notes-soar, 2026-03-23 prescription-soar. Disputed by John Laird in meeting on 2026-04-09 on architectural grounds (smem populated by deliberate cognition, not derived from epmem). This intake re-runs with the dispute recorded as primary source.
---

# Soar — Subjective synopsis (intake cache)

*Claims in Soar's own vocabulary, organized by Soar's own structural categories. Framework translations live in the translation records below the claims section, not in the claims themselves. Subject to elicitation before downstream stages consume this file.*

## CHECKPOINT: 2026-04-10, mid-session

**State.** Continuing from 2026-04-09 checkpoint. S2 (Derbinsky & Laird 2013) read cold and filed (C74–C83). §9.2 (C84), §9.3 (C85–C88), and §8 partial (C89) filed from Laird 2022 PDF. Key finding: D&L 2013 does NOT claim smem/epmem eviction is needed; the prior intake's extrapolation is confirmed as an extrapolation. S6 (meeting correspondence) still pending paraphrase from June.

**Previous checkpoint (2026-04-09):** Seven corrections applied after three rounds of bouncing with codex; see below for details.

## CHECKPOINT: 2026-04-09, end of day

**State.** Fresh /intake in progress, not complete. This file is a checkpoint — stable for sign-off, not ready for Diagnose. Seven corrections have been applied during today's pass after three rounds of bouncing with codex; the corrections are visible in the glossary, the ambiguity sections, and the §10 filing below, and should not be reverted without cause.

**Sources processed.** Only S1 (Laird 2022, "Introduction to the Soar Cognitive Architecture") read directly, and primarily §1–§7, §9.1, and §10. §8 (spatial-visual system), §9.2 (varieties of learning), §9.3 (combinations of reasoning and learning) partially read but not yet filed. S2 (Derbinsky & Laird 2013), S3 (Gentle Introduction), S4 (manual), S5 (source repo), S6 (meeting correspondence) all still pending as sources for downstream passes.

**Key finding 1 — current state vs architectural status of smem writes.** Per Laird 2022 §6 p.13 direct quote (C42), "Soar does not have an automatic learning mechanism for semantic memory, but an agent can deliberately store information at any time." The *factual* question of how current smem gets populated is resolved: deliberate agent-initiated storage, no automatic mechanism. The *interpretive* question — whether this is a permanent design commitment, an unfilled gap, or something else — is not fully resolved by §6 alone. **See also C71 (§10 p.19), where Laird himself explicitly lists "semantic learning" as a type of architectural learning that is still missing.** The §6 "as of yet" and the §10 "still missing" language together favor the gap reading at the narrow level, though the interpretive three-way framing (A1) remains on file for elicitation because "missing" does not by itself specify what mechanism should fill the gap, nor whether any specific proposed mechanism would be acceptable within Soar's architectural commitments.

**Key finding 2 — RL-chunking composition is partial, and PR #577 is architecturally adjacent to Laird's stated planned work, but not aligned on criterion.** §4 p.10 direct read (C66, C67) resolves the apparent tension between §4 and §5. Chunking produces RL rules with initial values when substates are deterministic (already supported); chunking does not fire when substates themselves use numeric preferences (restricted); Laird explicitly states he has plans to extend chunking to the restricted case "when there is sufficient accumulated experience to ensure that they have a high probability of being correct." PR #577's direction shares architectural shape with Laird's stated plan, but the EMA-of-|ΔQ| criterion is a stability signal, not a correctness proxy. Architecture adjacent; criterion weaker. See A7.

**Key finding 3 — §10 reframes the scaling motivation of the prior intake.** Laird rates Soar's real-time capability "yes, yes" (C69) with long-term memories of "millions of items," and rates diverse knowledge "yes" (C70) at scales of "millions and even tens of millions of rules, facts, and episodes, while still maintaining real-time reactivity." In the same section (item 7), he rates learning from environment and experience "partial, yes" and lists semantic learning as still missing (C71). In the closing §10 p.20, he identifies "bootstrap" as what he feels is most missing (C72). These §10 items are filed as direct quotes in S.md. Analyst interpretation of how they relate to prior intake claims about the "scaling wall" motivation, the Derbinsky & Laird 2013 extrapolation, and the prescribed mechanisms in PRs #578, #579, #580 is deferred to A.md and not filed as Subjective observation. **Concurrent meeting information from S6 (Laird, 2026-04-09) indicates the scaling-is-not-a-bottleneck position is also his current live stance; cross-source convergence is noted but its load-bearing implications are reserved for A.md.**

**Failures recorded during this pass.**
1. Committed to bouncing every load-bearing translation off codex inline and broke that commitment for three filings. Codex caught it after June asked "did you already ask codex."
2. Swung from the prior intake's "gap to fill" overread into a symmetrically opposite "design commitment" overread. Codex caught it in the first audit.
3. Surfaced Finding 2 (RL-chunking composition) before reading §4 directly. Codex flagged the order error; §4 was then read and the finding was refined.
4. Residual label slippage in the second round (three items flagged by codex, fixed).
5. Almost filed a framework-level multi-clock commitment into S.md. June caught it mid-task, flagging that the clock-speed assertion belongs in A.md (Assessment), not S.md (Subjective). Scope was revised before filing.
6. Initial draft of the §10 section had analyst vocabulary ("solved capability," "automatic semantic learning," "two separable statements," "not any specific mechanism") in the tracking commentary. Codex audit 3 caught it; the commentary was replaced with a neutral paraphrase closer to Laird's own wording.
7. C72 quote was initially truncated in a way that dropped the Rosie sentence and read harsher than the original. Codex flagged it; the Rosie sentence was restored.

**Active discipline lessons:**
- Skipping the codex bounce step is the failure mode. It never helps and it always costs a round of corrections.
- Swinging the opposite direction of an overclaim is still overclaiming.
- Relaying citations from the prior intake without direct read reproduces the same error category as the prior intake.
- Framework-level commitments and analyst inferences must not enter S.md. They belong in O.md (observations grounded in evidence) and A.md (assessment and judgment). When in doubt, reserve for A.md.
- The S.md "tracking commentary" / "synthesis" slot is a risky slot — it is easy to slip from "paraphrasing Laird" into "interpreting Laird." Prefer raw quotes plus minimal neutral paraphrase over any synthesis that involves connecting two of Laird's claims causally.

**Where to pick up (ordered by load-bearingness, updated 2026-04-10):**

1. ~~Read S2 (Derbinsky & Laird 2013).~~ **DONE 2026-04-10.** Answer: D&L 2013 does NOT claim smem/epmem eviction is needed. The paper treats smem as the stable backup store (R4) and epmem reconstruction cost as an argument for WM forgetting, not epmem eviction. Prior intake's extrapolation confirmed as extrapolation. Filed as C74–C83.
2. File S6 (meeting correspondence) as primary source. **Pending** — awaiting June's paraphrase of Laird's actual stance.
3. Consider checking S5 (source code) for whether Laird's planned "modify chunking to handle stochastic substates" (§4 p.10) has been implemented since 2022. Relevant to whether PR #577 should be framed as re-implementation or as rough adjacent attempt at planned work.
4. ~~Read §8, §9.2, §9.3.~~ **DONE 2026-04-10.** §9.2 (C84), §9.3 (C85–C88), §8 partial (C89) filed. Key finding from §9.2 Figure 6: smem source of knowledge is "Existence in Working memory," confirming the deliberate-from-WM write path.
5. Advance to Diagnose (produces O.md and A.md). Multi-clock framework commitment, scaling-vs-bootstrap reframe, PR retirement judgments, and any analyst interpretation of the §10 findings go in A.md — NOT in S.md. The clock-speed assertion in particular belongs in Assessment.
6. Run codex sniff on the full S.md (Phase 4 of /intake) before advancing to elicitation.
7. Only then — and only after the elicitation quiz is answered — should Diagnose be run against any actual prescription work.

**Do not re-run /intake from scratch without reading this checkpoint first.** The corrections applied today represent an active debugging pass on the pipeline itself, not just on the Soar synopsis. Re-running from zero loses the failure-mode observations.

---

## Source list

- `S1` Laird, J. E. (2022). "Introduction to the Soar Cognitive Architecture." arXiv:2205.03854. Primary recent overview.
- `S2` Derbinsky, N. & Laird, J. E. (2013). "Effective and efficient forgetting of learned knowledge in Soar's working and procedural memories." Cognitive Systems Research. Forgetting paper.
- `S3` Lehman, J. F., Laird, J. E., & Rosenbloom, P. S. (2006). "A Gentle Introduction to Soar, an Architecture for Human Cognition: 2006 Update." Tutorial-level introduction.
- `S4` Soar manual: https://soar.eecs.umich.edu/soar_manual/
- `S5` SoarGroup/Soar source repository: https://github.com/SoarGroup/Soar (Core/SoarKernel/src/*)
- `S6` Correspondence with John Laird, 2026-04-09 meeting (paraphrased by June Kim). Recorded as primary source because it disputes load-bearing framings in prior intake.

## Claims

*Organized by Soar's own section structure in Laird (2022), which is the primary source for this pass.*

### 1. Structure of Soar

**C1.** Soar is a task-independent infrastructure that "learns, encodes, and applies an agent's knowledge to produce behavior," intended as "a software implementation of a general theory of intelligence." [S1, introductory paragraphs p.1]

**C2.** Soar's long-term symbolic knowledge is stored in three memories: **procedural memory** (skills and "how-to" knowledge), **semantic memory** (facts about the world and the agent), and **episodic memory** (memories of experiences). [S1, §1 p.3]

**C3.** Soar also has **symbolic working memory**, **preference memory**, and **perceptual long-term memory** (accessed via the Spatial-Visual System). [S1, §1 p.2, Figure 1]

**C4.** Processing modules include the **decision procedure**, the **spatial-visual system (SVS)**, and **embodiment** (perception and motor). [S1, §1 p.2, Figure 1]

**C5.** Learning modules are attached to specific memories in Figure 1: **RL** and **chunking** attach to procedural memory, **semantic learning** attaches to semantic memory, **episodic learning** attaches to episodic memory. [S1, §1 p.2, Figure 1]

**C6. LOAD-BEARING.** *"Automatic learning mechanisms are associated with procedural and episodic memories."* [S1, §1 p.3, direct quote]

**C6 commentary.** Cross-check with §6 and §10 for scope of "automatic learning mechanisms."

**C7.** "Procedural knowledge drives behavior by responding to the contents of working memory and making modifications to it. Procedural memory implements purely internal reasoning, as well as initiating retrievals from semantic and episodic memory of knowledge into working memory." [S1, §1 p.3] — So retrievals from smem/epmem are initiated by procedural knowledge (rules), not by a background process.

**C8.** Cross-source note: the prior intake framed Soar as "missing automatic epmem→smem consolidation." Cross-check with §6 (C42) and §10 (C71). [internal note]

### 2. Deliberate Behavior: Selecting and Applying Operators

**C9.** Soar organizes knowledge about conditional action and reasoning into **operators**. An operator can be an internal action (e.g., arithmetic, retrieving from semantic/episodic memory, rotating an image in the spatial memory system) or an external action (e.g., moving a robot, generating natural language, accessing an external software system). [S1, §2 p.3]

**C10.** Each operator decomposes into three functions: **proposing potential operators**, **evaluating proposed operators**, and **applying the operator**. The knowledge for each function is represented as independent rules that fire in parallel when they match the current situation. [S1, §2 p.4]

**C11.** "Rules are not themselves alternative actions, but instead units of context-dependent knowledge that contribute to making a decision and taking action." [S1, §2 p.4, direct quote]

**C12.** When the available knowledge is insufficient to make a decision or apply an operator, an **impasse** arises, and the proposal, evaluation, and/or application phases are carried out via recursive operator selections and applications in a **substate**. [S1, §2 p.4]

**C13.** "This impasse-driven process is the means through which complex, hierarchical operators and reflective meta-reasoning (including planning) are implemented in Soar, instead of through additional task-specific modules." [S1, §2 p.4, direct quote]

**C14.** Working memory contains information tested by rules: goals, data retrieved from long-term memories, information from perception, results of internal operators. "Soar does not have any predefined structure for the contents of working memory except for the buffers that interface to other modules. Thus, there is no predefined structure for goals or even operators." [S1, §2 p.4, direct quote]

**C15. Preference memory** holds a special data structure called a **preference**. Preferences are created in the actions of rules and added to preference memory. Two classes: **acceptable** preferences (created by operator proposal rules, indicating an operator is available for selection) and **evaluative** preferences (of many types, specifying information about whether an operator should be selected). [S1, §2 p.4]

**C16.** There are also **numeric preferences** that "encode the expected future reward of an operator for the current situation as matched by the conditions of the rule." These are the interface point for reinforcement learning. [S1, §2.2.3 p.5]

### Decision cycle phases

**C17.** The decision cycle consists of phases: **Input → Elaboration (proposal & evaluation, wave-based) → Operator Selection → Operator Application → Output**, then back to Input. [S1, Figure 2, §2.1–2.4]

**C18. Input phase:** "the input phase processes data from perception, SVS, and retrievals from semantic and episodic memory, and adds that information to the associated buffers in working memory." [S1, §2.1 p.5, direct quote] — Note that smem/epmem retrievals land at the input phase, as the fulfillment of requests initiated previously.

**C19. Elaboration phase:** "rules fire that elaborate the situation, propose operators, and evaluate operators. All rules in Soar fire only once for a specific match to data in working memory (this is called an **instantiation**), and a given rule will fire multiple times if it matches different structures in working memory." [S1, §2.2 p.5, direct quote]

**C20.** Elaboration-phase rule firings make **monotonic** additions to working or preference memory. "The structures they create are valid only as long as the rule instantiation that created them matches"; they are **retracted** when the instantiation no longer matches. This is "an example of **justification-based truth maintenance**." [S1, §2.2 p.5]

**C21.** There is no ordering of firing and retracting among different rule types; they intermix within a wave. Elaboration proceeds in waves until **quiescence** (no more rule firings or retractions), at which point control passes to operator selection. [S1, §2.2 p.5]

**C22.** Operator application rules fire *only* during the operator application phase, even if they newly match due to input changes in elaboration. "Given the dynamics of elaboration, this ensures that they fire only when their tested operator is preferred for the current situation." [S1, §2.2 p.5]

**C23. Elaboration rules** "create new structures entailed by existing structures in working memory. Elaborations can simplify the knowledge required for operator proposal, evaluation, and application by detecting useful regularities or abstractions." [S1, §2.2.1 p.5, direct quote]

**C24. Operator proposal rules** test the current situation to determine if an operator is relevant. If it is, they propose the operator by creating an acceptable preference. They "test the preconditions or affordances of an operator and create an explicit representation, which often will include parameters." "Task knowledge is incorporated into the proposal to avoid proposing all operators that are legal in a situation." [S1, §2.2.2 p.5]

**C25. Operator evaluation rules** test the proposed operators and other WM contents and create preferences that determine which operator is selected. Soar has preferences for relative value (A better than B, A equal to B), absolute value (A as good as possible, B as bad as possible, C rejected), and numeric preferences for expected future reward. [S1, §2.2.3 p.5]

**C26. Operator selection phase:** "Once quiescence is reached, a fixed **decision procedure** processes the contents of preference memory to choose the current operator. If the available preferences are sufficient to make a choice, a structure is created in working memory indicating the selected operator. If the preferences are inconclusive or in conflict, then no operator is selected, and an impasse arises." [S1, §2.3 p.6, direct quote]

**C27. Operator application phase:** operator application rules make **non-monotonic** changes to working memory and "do not retract those changes when they no longer match." [S1, §2.4 p.6]

**C28.** Operator applications have four functional roles: (i) internal reasoning steps that modify internal state; (ii) external actions via the motor buffer; (iii) mental imagery actions via SVS buffers; (iv) **retrieval cues created in the semantic or episodic memory buffers**. [S1, §2.4 p.6] — Critical: retrievals are initiated by operator application rules writing to the smem/epmem buffers, not by a background process.

### 5. Reinforcement Learning: Learning Control Knowledge from Reward

**C29.** "Using RL in Soar is straightforward. The first step is to create operator evaluation rules that create numeric preferences, aptly called **RL rules**." RL rules are just operator evaluation rules whose numeric preference encodes expected future reward (Q value) for the matching state/operator pair. [S1, §5 p.11, direct quote]

**C30.** "After an operator applies, all RL rules that created numeric preferences for it are updated based on the reward associated with the state and the expected future reward." [S1, §5 p.11, direct quote]

**C31.** "RL influences operator selection only when the other, non-RL preferences are insufficient for making a decision. Thus, RL rules do not have to be relied on to avoid dangerous situations... when there are other sources of knowledge (such as other procedural knowledge or advice from a human) readily available." [S1, §5 p.11, direct quote] — RL is a fallback layer, not a replacement for symbolic preferences.

**C32.** Soar supports Q-learning and SARSA with eligibility traces. Learning rates and discount rates are fixed at agent initialization. [S1, §5 footnote 5 p.11]

**C33.** "One intriguing aspect of RL in Soar is that the mapping from state and operator to expected reward (the value-function) is represented as collections of relational rules. When there are multiple rules that test different state and operator features, they can provide flexible and complex value functions that map from states and operators to an expected value, supporting tile coding, hierarchical tile coding, coarse coding, and other combination mappings." [S1, §5 p.12, direct quote]

**C34. LOAD-BEARING — directly contradicts prior intake's "RL-chunking composition gap" framing.** Direct quote from §5 p.12:

> **"RL rules can be learned by chunking, where the initial value is initialized by the processing in a substate, and then subsequently tuned by the agent's experience and reward."**

**C34 commentary.** See O.md for analysis of how this relates to the §4 restriction (C67) and the prior intake's framing.

**C35.** "RL in Soar applies to every active substate, with independent rewards and updates for RL rules across the substates. Thus, Soar naturally supports hierarchical reinforcement learning for all different types of problem solving and reasoning, including when planning is used in substates (model-based RL), or in the topstate (model-free RL)." [S1, §5 p.12, direct quote]

### 6. Semantic Memory

**C36.** "Soar has two additional long-term symbolic declarative memories in addition to procedural memory. Semantic memory... encodes facts that an agent 'knows' about itself and the world, while episodic memory (described below in Section 7) encodes what it 'remembers' about its experiences. Thus, semantic memory serves as a knowledge base that encodes general context-independent world knowledge, but also specific knowledge about an agent's environment, capabilities, and long-term goals." [S1, §6 p.12, direct quote]

**C37.** Semantic and episodic memories differ from procedural memory in:
- **how knowledge is encoded**: graph structures instead of rules
- **how knowledge is accessed**: through deliberate cues biased by metadata, rather than matching of working memory to rule conditions
- **what is retrieved**: a declarative representation of the concept/episode, rather than the actions of a rule
- **how they are learned**: described below (§6 continued and §7)

[S1, §6 p.12, direct quote structure]

**C38.** "A common question is why the information in semantic memory cannot be maintained in working memory. Unfortunately, the cost of matching procedural knowledge against working memory increases significantly with working memory size, making it necessary to store long-term knowledge separately." [S1, §6 p.12, direct quote] — The motivation for having smem distinct from WM is RETE matching cost, not a cognitive-science-inspired distinction.

**C39.** "Concepts in semantic memory are encoded in the same symbolic graph structures as used in working memory." [S1, §6 p.12, direct quote]

**C40.** "Knowledge is retrieved from semantic memory by the creation of a cue in the semantic memory buffer. The cue is a partial specification of the concept to be retrieved... The cue is used to search semantic memory for the concept that best matches the cue, and once that is determined, the complete concept is retrieved into the working memory buffer, where it can then be tested by procedural memory to influence behavior." [S1, §6 p.12, direct quote] — Retrieval path: rule creates cue → smem matches → result placed in buffer → rules test retrieved content. The retrieval is always initiated by procedural knowledge.

**C41.** "Soar uses a combination of base-level activation and spreading activation to determine the best match, as used originally in ACT-R. Base-level activation biases the retrieval using recency and frequency of previous accesses of concepts (and noise), whereas spreading activation biases the retrieval to concepts that are linked to other concepts in working memory." [S1, §6 p.12–13, direct quote]

**C42. LOAD-BEARING — the primary-source text that resolves the prior intake's central ambiguity.** Direct quote from §6 p.13:

> **"Semantic memory can be initialized with knowledge from existing curated knowledge bases (such as WordNet or DBpedia) and/or built up incrementally by the agent during its operations. As of yet, Soar does not have an automatic learning mechanism for semantic memory, but an agent can deliberately store information at any time."**

**C42 commentary.** Four separable claims: (1) preloading from curated KBs supported, (2) incremental agent-driven growth supported, (3) no automatic learning mechanism in current Soar, (4) deliberate storage is the current path. See O.md/A.md for interpretive analysis.

**C43.** "In our robot, semantic memory would hold the agent's map of its environment, either preloaded from some other source or dynamically constructed as the robot explores its world. Other common uses are to maintain representations of words and their meaning for language processing, knowledge about different agents the robot interacts with, and declarative representations of hierarchical task structures it learns from instruction." [S1, §6 p.13, direct quote] — Use cases confirm the "deliberate agent construction" model. "Learned from instruction" is particularly telling: the learning path goes through the agent's cognition, not through a background process.

### 7. Episodic Memory

**C44.** "In contrast to semantic memory, which contains knowledge that is independent of when it was learned, Soar's episodic memory... contains memories of what has been experienced over time." [S1, §7 p.13, direct quote]

**C45. LOAD-BEARING — automatic storage of WM snapshots, not automatic derivation or consolidation.** Direct quote from §7 p.13:

> **"An episode is a snapshot of the structures in the topstate. A new episode is automatically stored at the end of each decision."**

**C45 commentary.** "Automatic" here means mechanical snapshotting of WM, not derivation of new knowledge. See O.md for framework mapping.

**C46.** "Retrievals from episodic memory are initiated via a cue created in the episodic memory buffer by procedural knowledge. Unlike semantic memory, a cue for an episodic retrieval is a partial specification of a complete state, as opposed to a single concept. Episodic memory is searched, and the best match is retrieved (biased by recency) and recreated in the buffer." [S1, §7 p.13, direct quote] — Retrieval is deliberate (rule-initiated), parallel to smem retrieval.

**C47.** "Once a memory is retrieved, memories before or after that episode can also be retrieved, providing the ability to replay an experience as a sequence of retrieved episodes or to move backward through an experience to determine factors that influenced the current situation, including prior operators, but also changes from the dynamics of the environment." [S1, §7 p.13, direct quote]

**C48. LOAD-BEARING — Soar's acknowledged epmem scaling characteristic with its stated mitigations.** Direct quote from §7 p.13:

> **"Soar minimizes the memory overhead of episodic memory by storing only the changes between episodes and uses indexing to minimize retrieval costs. However, memory does grow over time, and the cost to retrieve old episodes slowly increases as the number of episodes grows, whereas the time to retrieve recent episodes remains constant. An agent can further limit the costs of retrievals by explicitly controlling which aspects of the state are stored, usually ignoring frequently changing low-level sensory data."**

**C48 commentary.** Laird names three existing mitigations: (1) delta encoding, (2) indexing, (3) agent-controlled filtering. See A.md for comparison with prior intake's framing.

**C49.** "Episodic learning has often been ignored as a learning method because it does not have generalization mechanisms. However, even without generalization, it supports many important capabilities: virtual sensing of remembered locations and objects that are outside of immediate perception; learning action models for internal stimulation from memories of the effects of past operators that have external actions; learning operator evaluation knowledge via retrospective analysis of previous behavior; using prospective memory to trigger future behavior, by imagining hypothetical future situations that are stored in memory and then recalled at the appropriate time; using a string of episodes to reconstruct and debug a particular course of action." [S1, §7 p.13–14, direct quote] — Laird explicitly defends epmem as a learning method WITHOUT generalization. He lists five capabilities that work on raw episodes without any derived semantic structure. This is a direct defense of the design choice that the prior intake flagged as a gap.

### 9. Summary and Review — Levels of Processing

**C50.** Soar's levels of processing (mapped to Newell's bands): Substates (>~1 sec), Decision Cycle (~100ms), Module (10ms, rule matching and memory retrievals), Architecture (~1ms, C/C++ code). [S1, Figure 5, §9.1 p.15]

**C51.** "Chunking automatically converts processing in substates into rules, so that as an agent gets experience with a task, the higher-level processing levels are replaced by rules that select and apply operators." [S1, §9.1 p.16, direct quote] — Substate processing gets compiled into rules by chunking. Over time, the agent moves work down the level hierarchy from deliberation to automatic rule firing.

**C52.** "Substate operators can perform processing that is not possible in a single decision, such as making multiple retrievals of data from episodic or semantic memory, simulating hypothetical states in SVS, or even interacting with a human. This level is where full-scale sequential reflective reasoning can be used when the fast, automatic retrieval from procedural memory is insufficient for making a decision." [S1, §9.1 p.16, direct quote]

**C53.** Laird cautions against a naive Kahneman System 1 / System 2 mapping onto Soar's levels. [S1, §9.1 p.16]

### 3. Impasses and Substates: Responding to Incomplete Knowledge

**C54.** "Soar embraces a philosophy that additional relevant knowledge can be obtained through additional deliberate reasoning and retrieval from other sources, including internal reasoning with procedural memory (e.g., planning), reasoning with non-symbolic knowledge, retrieval from episodic memory or semantic memory, or interaction with the outside world. This is essentially the philosophy of 'going meta' when directly available knowledge is inadequate." [S1, §3 p.7, direct quote]

**C55.** "Soar commits to a single approach for both deliberation and meta-reasoning, which differs from architectures that have separate meta-processing modules, such as MIDCA and Clarion." [S1, §3 p.7, direct quote] — Single-mechanism commitment: the substate mechanism is the only meta-reasoning path in Soar. No parallel metacognitive subsystem.

**C56.** Three impasse types: **state no-change** (no operators proposed), **operator tie/conflict** (multiple operators proposed but evaluation preferences insufficient or in conflict), **operator no-change** (same operator stays selected across multiple decision cycles, indicating insufficient application knowledge). [S1, §3 p.7]

**C57.** A **substate** is created on impasse, linked to the existing **topstate** (its **superstate**). The substate has its own preference memory and can select and apply operators without disrupting processing in superstates. Substates are recursive — impasses in a substate create further substates, yielding a stack. [S1, §3 p.7–8]

**C58.** "Through the link to the superstate, [the substate] has access to all superstate structures. It has buffers for semantic memory and episodic memory, but not perception and motor, which must go through the topstate so that all interaction with the outside world can be monitored by reasoning in the topstate." [S1, §3 p.8, direct quote] — Design commitment: external-world I/O always flows through the topstate, not through substates.

**C59.** "When an operator in a substate creates and modifies structures in a superstate, those changes are the **results** of the substate. If the result is an elaboration in the superstate (state elaboration, operator proposal, or operator evaluation), it persists only as long as the superstate structures responsible for its creation exist. If the result is part of the application of an operator selected in the superstate (a **superoperator**), such as creating a motor command, the result does not retract." [S1, §3 p.8, direct quote]

**C60.** "Impasse-driven substates allow an agent to automatically transition from using parallel procedural knowledge to using more reflective, metacognitive reasoning when the procedural knowledge is insufficient to select and/or apply operators." [S1, §3.3 p.9, direct quote]

### 4. Chunking: Learning New Rules

**C61.** "Impasses arise when there is a lack of knowledge to select or apply an operator. The processing in a substate creates knowledge to resolve the impasse, creating an opportunity for learning. In Soar **chunking** compiles the processing in a substate into rules that create the substate results, eliminating future impasses and substate processing. Thus, chunking is a learning mechanism that converts deliberate, sequential reasoning into parallel rule firings." [S1, §4 p.9–10, direct quote]

**C62.** "Chunking is automatic and is invoked whenever a result is created in a substate. It analyzes a historical trace of the processing in the substate, determining which structures in the superstate had to exist for the results of the substate processing to be created. Those structures become the conditions of a rule, and the results become the actions. Independent results in a substate lead to the learning of multiple rules." [S1, §4 p.10, direct quote]

**C63.** Back-tracing mechanism: "when results are created, Soar **back-traces** through the rule that created them, finding the working memory elements that were tested in its conditions. All of those working memory elements that are part of a superstate are saved to become conditions along with additional tests in the conditions of the associated rules." [S1, §4 p.10, direct quote]

**C64.** Recent reimplementation: "Chunking has recently been completely reimplemented and the new implementation is based on recent analyses and a subsequent design that ensures that the resulting rules are correct relative to the reasoning in the substate and as general as possible without being over general. This new approach is called **explanation-based behavior summarization (EBBS; Assanie, 2022)**." [S1, §4 p.10, direct quote]

**C65.** Chunking can learn four types of rules, matching the four functional rule categories: **elaboration rules**, **operator proposal rules**, **operator evaluation rules**, **operator application rules**. [S1, §4 p.10]

**C66. LOAD-BEARING — the composition direction that reframes Finding 2.** Direct quote from the §4 Operator Evaluation bullet, page 10:

> "When there is a tie or conflict impasse, and a substate generates new preferences, chunking learns operator evaluation rules. When the substate processing involves planning, this involves compiling planning into knowledge that is variously called search-control, heuristics, or value functions. When those are numeric preferences, the rules created by chunking will be **RL rules that are initialized with whatever evaluation was generated. In the future, those rules can be further tuned by reinforcement learning (Laird et al., 2011).**"

**C66 commentary.** See A.md for analysis of composition direction and relationship to prior intake.

**C67. LOAD-BEARING — the specific limitation that the prior intake cited, and Laird's own stated planned fix.** Direct quote from §4 p.10:

> "One limitation is that chunking requires that substate decisions be deterministic so that they will always create the same result. Therefore, chunking is not used when decisions are made using numeric preferences. We have plans to modify chunking so that such chunks are added to procedural memory when there is sufficient accumulated experience to ensure that they have a high probability of being correct."

**C67 commentary.** Two separable claims: (1) the restriction — chunking does not fire when substate decisions use numeric preferences; (2) the planned fix — Laird states plans to extend chunking to this case. See A.md for PR #577 analysis.

**C68.** "A potential concern with chunking is that the costs of the analyses it performs to create a chunk could surpass its benefits. Our empirical results show that such overhead is minimal and that the performance improvements are much greater than the costs (Assanie, 2022)." [S1, §4 p.11, direct quote]

### 10. Evaluation of Soar as a General Cognitive Architecture

**C69 (§10 p.18 item 3, "Operate in real time," Laird rates "yes, yes").**

> "An agent must be responsive to the dynamics of its environment, which for Soar is determined by the loop from perception, decision, to motor action. Empirical evidence is that a decision cycle time of around 50 msec. is required for real-time behavior. Soar achieves that even with large long-term memories (millions of items)."

**C70 (§10 p.19 item 12, "Use diverse types and levels of knowledge," Laird rates "yes").**

> "An agent needs knowledge about how to perform tasks, about the objects and agents in its world, its experiences, etc. It must handle situations where its knowledge is incomplete and where reasoning or exploration are required to fill in the gaps, but it must also have the capacity to encode, store, and use vast bodies of knowledge. [...] In terms of the raw amount of knowledge, procedural, semantic, and episodic memories have all held not just thousands, but millions and even tens of millions of rules, facts, and episodes, while still maintaining real-time reactivity."

**C71 (§10 p.19 item 7, "Learn from the environment and experience," Laird rates "partial, yes").**

> "An agent needs to continually learn from its experience in its environment, acquiring new concepts and relations, improving its decision making, reducing the time it takes to make decisions, and building up a historical record of its experiences that it can use later for deliberate retrospection. [...] Further, there are still types of architectural learning that are missing, such as semantic learning, generalized perceptual category learning, and learning expectations or predictions of its own actions or the dynamics of its environment."

**C72 (§10 p.20, Laird's identification of what is most missing).**

> "What I feel is most missing from Soar is its ability to 'bootstrap' itself up from the architecture and a set of innate knowledge into being a fully capable agent across a breadth of tasks. Our agents do well when restricted to specific well-defined tasks. We have gone beyond that with Rosie. But without a human to closely guide it, Rosie is unable to get very far on its own, especially in being unable to learn new abstract symbolic concepts..."

**Paraphrase of §10 as Laird presents it.** In §10, Laird rates real-time operation "yes, yes" and diverse knowledge "yes," while rating learning from the environment and experience "partial, yes." He also states that semantic learning and other types of architectural learning are still missing, and that what feels most missing is Soar's ability to bootstrap from architecture and innate knowledge into a fully capable agent across a breadth of tasks.

*Analyst interpretation of how these items relate to prior intake claims, to the framework's roles, or to one another (e.g., whether item 3 + item 12 undercut item 7, or whether the bootstrap gap in C72 entails any specific mechanism, or whether Soar's single-clock architecture is adequate for these capabilities) is reserved for O.md and A.md.*

### S2. Derbinsky & Laird (2013) — Forgetting in WM and procedural memory

*Filed 2026-04-10. Read cold against S.md item 1: "does this paper actually claim smem/epmem eviction is needed, or is the prior intake's framing an extrapolation from WM/procedural to all memory types?"*

**C74. Scope of paper.** Title: "Effective and efficient forgetting of learned knowledge in Soar's **working and procedural** memories." The paper builds forgetting policies for two memory types only. Smem and epmem are not proposed as targets for forgetting. [S2, title + abstract]

**C75. Utility problem motivation.** "This issue, where more knowledge can harm problem-solving performance, has been dubbed the *utility problem*." The paper frames forgetting as a response to the utility problem: accumulated learned knowledge degrades the architecture's computational performance. [S2, §1 p.104]

**C76. WM forgetting safety requirement R4.** "R4. The WME augments an object, *e*, in semantic memory." [S2, §5 p.108] — WM forgetting only removes elements that have a backup in smem. Smem is the ground truth that makes WM forgetting safe. **R4 depends on smem being stable, not on smem being evicted.**

**C77. R4 rationale.** "Requirement R4 dictates that our mechanism only removes elements from working memory that augment objects in semantic memory. This requirement serves to balance the deletion of working-memory objects with support for sound reasoning. Knowledge in Soar's semantic memory is persistent, though it may change over time. Depending on the task and the model's knowledge-management strategies, it is possible that forgotten working-memory knowledge may be recovered via a deliberate reconstruction from semantic memory." [S2, §5 p.108, direct quote] — Smem is the **reconstruction source** for forgotten WM elements.

**C78. WM forgetting empirical results (Fig. 3, §5.1 p.109).** Robot visits 100+ rooms, builds topological map (~10,000 WMEs). Without forgetting (A0): WM grows to 12,000+ elements after 1 hour. With hand-coded forgetting (A1): ~2,000 elements. With task-independent policy at d=0.5 (A2): comparable to A1. [S2, §5.1 p.109]

**C79. Reconstruction cost observation (Fig. 4, §5.1 p.110).** "without sufficient working-memory management (A0; A2 with decay rate 0.3), episodic-memory retrievals are not tenable for a model that must reason with this amount of acquired information, as the maximum required processing time exceeds the reactivity threshold of 50 ms." [S2, §5.1 p.110, direct quote] — **This is an argument FOR WM forgetting, not for epmem eviction.** The causal direction: large WM at encoding time → large episodes → expensive epmem reconstruction. The fix is smaller WM (more aggressive WM forgetting), not epmem eviction.

**C80. Procedural forgetting R4.** "R4. The rule has not been updated by RL." [S2, §6 p.110] — For procedural memory, forgetting protects RL-updated rules because their expected-utility information "is not recorded by any other learning mechanism and cannot be regenerated." Same safety-net logic as WM forgetting.

**C81. Procedural forgetting scope.** "Soar learns rules to represent only those portions of the space it experiences, and our policy retains only those rules that include feedback from environmental reward." [S2, §6.2 p.112] — Forgetting is scoped to chunked and RL rules in procedural memory.

**C82. No future-work call for smem/epmem forgetting.** §7 (Concluding remarks, p.112): "there is additional work to evaluate these policies, and their parameters, across a wider variety of problem domains." No mention of extending forgetting to episodic or semantic memory. The paper treats its scope (WM + procedural) as complete; it does not gesture toward smem or epmem as the next frontier. [S2, §7 p.112]

**C83.** See A.md for assessment of how D&L 2013 relates to the prior intake's extrapolation. [moved to A.md]

### §9.2 Varieties of Learning (S1, Laird 2022)

*Filed 2026-04-10.*

**C84. Figure 6: Summary of Soar's Memory and Learning Systems.** [S1, §9.2 p.17, Figure 6]

| Memory/Learning System | Source of Knowledge | Representation of Learned Knowledge | Retrieval of Knowledge |
|---|---|---|---|
| Chunking | Traces of rule firings in subgoals | Rules | Exact match of rule conditions |
| Semantic Memory | Existence in Working memory | Graphs | Partial match biased by activation |
| Episodic Memory | Working memory co-occurrence | Episodes: Snapshots of working memory | Partial match, temporally adjacent episodes |
| Reinforcement Learning | Reward and preferences | Rules that create numeric preferences | Exact match of rule conditions |
| Image Memory | Image short-term memory | Image | Deliberate recall using symbolic referent |

**C84 commentary.** Semantic memory's source of knowledge is listed as "Existence in Working memory" — not episodic memory. This is Laird's own table.

### §9.3 Combinations of Reasoning and Learning (S1, Laird 2022)

*Filed 2026-04-10.*

**C85.** "One unique aspect of cognitive architectures is that they can combine multiple approaches to reasoning and learning depending on the available knowledge." Laird lists 8 examples. [S1, §9.3 p.17]

**C86.** Item 3: "Chunking is used to learn RL rules whose initial values are derived from internal probabilistic reasoning. Those values are then tuned by experience (Laird, 2011)." [S1, §9.3 p.17] — Confirms the chunking→RL composition direction from C34 and C66.

**C87.** Item 5: "A variety of knowledge sources are used to model the action of operators for planning, including procedural memory, semantic memory, episodic memory, and mental imagery (Laird et al., 2010), **all of which are compiled into rules by chunking.**" [S1, §9.3 p.17, direct quote with emphasis] — Chunking is the terminus for all knowledge types used in planning. Even when episodic and semantic memory contribute to reasoning, the result is compiled into procedural rules.

**C88.** Item 6: "Episodic memory, metareasoning, and chunking are combined in retrospective analysis that provides one-shot learning of new operator proposal and evaluation knowledge (Mohan, 2015)." [S1, §9.3 p.17]

### §8 Spatial-Visual System (S1, Laird 2022) — partial

*Filed 2026-04-10. Only tail of §8 visible in current pass (p.15).*

**C89.** SVS mediates interactions between motor actions and perception in 3D robotic environments. Object persistence: when an arm moves an object that obscures another, "the agent uses its knowledge of 3D space and object persistence to understand that the obscured object has not disappeared, and it can maintain a symbolic representation of the object in working memory." [S1, §8 p.15, paraphrase + partial quote from Mininger 2019]

### S6. Meeting with John Laird, 2026-04-09 (paraphrased by June Kim)

*Filed 2026-04-10.*

**C90. Smem and epmem are structurally distinct.** Laird stated that smem's data structure is completely different from epmem's. Episodic memories are not "edges" to semantic memory's "nodes" — that framing (from TVG, the prior intake's mental model) does not reflect the architecture. [S6, paraphrased]

**C91. The unified-graph model is wrong.** June presented a mental model in which memory has a singular graph representation with shared datatypes between epmem and smem, where epmem accumulates into smem. Laird rejected this. The architecture does not work that way. [S6, paraphrased]

**C91 commentary.** See O.md for cross-source confirmation.

**C92. Smem is populated from WM; epmem-to-smem is not straightforward.** The architectural path is: agents deliberate in WM, then store results to smem via operator application rules. [S6, paraphrased, see A.md for analysis]

### S5. Source code check: stochastic-substate chunking

*See O.md for code-audit findings on whether Laird's planned modification (C67) has been implemented.*

*(Pending: S3 (Gentle Introduction), S4 (manual) still to come.)*

## Glossary

*Moved to O.md. Framework mappings are observations, not source claims.*

## Ambiguous mappings

*Moved to O.md/A.md. Interpretive analysis belongs in downstream stages.*

## Open questions

*Internal tensions in Soar's own self-description, cross-source discrepancies, things the sources don't answer.*

## elicitation

**Q1. Semantic memory write path.** User position: (c) — open problem from Laird's perspective (C71 confirms the gap). Theoretically solved per user's own work (june.kim/functor-wizardry). But implementation inside Soar is not feasible without a curated write path from epmem to smem, which the architecture does not support (C90-C91: structurally different stores). And even with a write path, efficacy cannot be proven without evaluations that do not exist. **Net: the gap is real, the theory exists, the implementation path is blocked, the eval path is absent.**

**Q2. PR #577 (RL convergence gate for chunking).** User position: hold. Already a draft PR. Needs performance proofs and/or empirical evidence before it can be considered for merge. Direction is aligned with Laird's planned feature (C67) but criterion (EMA stability vs correctness) is unvalidated.

**Q3. PRs #578, #579, #580 (smem eviction, epmem eviction, cross-tier coherence).** User position: retire all three. Closed 2026-04-10 with documented wrongful assumptions (D&L 2013 extrapolation, epmem→smem pathway unsupported, scaling motivation retired).

**Q4. Prescription direction.** User position: the broken role is Consolidate at the *organizational* level, not the architectural level. PR efforts are not well directed — the prior intake is evidence of this. Root cause unknown. Speculation: monolith ossification — modules have tight couplings and the codebase is unable to provide quantitative or qualitative hill-climbing directives for contributors. Without a signal that tells you whether a change is an improvement, effort scatters.

**Q4 addendum (S6).** Near the end of the 2026-04-09 meeting, after many failed attempts at diagnosis-level alignment, June and Laird converged on one point of agreement: the need for evals — ways to prove that proposed improvements are legitimate. This was the only alignment reached in the meeting. This supports the organizational-Consolidate reading: the missing piece is not a mechanism but a *measurement*. Without evals, neither the contributor nor the maintainer can distinguish a real improvement from a plausible-sounding mistake.
