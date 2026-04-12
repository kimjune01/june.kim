---
system: Soar
target: SoarGroup/Soar
purpose: input to /prescribe; not part of the SOAP diagnosis itself
derived_from: A.md §8 (hard/soft constraints) + Appendix A (forced-optimization argument)
created: 2026-04-09
status: provisional — blocked on S.md finalization and A.md sign-off before /prescribe consumes
---

# Pre-prescription input notes

*This file is not A.md. It is the prescription-adjacent content that was incorrectly included in A.md's first draft and moved here per codex review finding 5. Do not treat it as part of the diagnosis. When /prescribe runs, it should consume A.md as the diagnosis and this file as the constraint set.*

## 1. Hard constraints inherited from the S.md elicitation

These are commitments the diagnosis itself has made that /prescribe must respect. They are constraints on the *solution space*, not on the diagnosis.

1. **Do not assume epmem→smem consolidation is the filler for the Q1 semantic-learning gap.** Laird at the 2026-04-09 meeting (S6, paraphrased) rejected epmem→smem as a given on architectural grounds: *"smem populated by deliberate cognition, not derived from epmem."* /prescribe either proposes a mechanism that respects *"smem populated by deliberate cognition"* as the architectural commitment, or it must supply new evidence that the rejection was narrower than it appeared. S6 is a paraphrased meeting note, not a primary source; /prescribe should re-elicit if the constraint becomes load-bearing for a specific candidate.

2. **Do not treat C49's five-capability list as weak defense.** Laird actively defends the absence of episodic → semantic generalization via five named capabilities in §7 p.13–14, and §10 item 14 (C78) rates *"Reason about the past and the future (yes)"* on the strength of the non-generalized epmem capability. Any proposal to add a generalization mechanism must engage C49's list and explain why the additional mechanism provides value beyond what Laird has already claimed.

3. **Do not inherit PR #577's EMA-of-|ΔQ| criterion without justification.** EMA measures *stability*, not *correctness*. Laird's C67 phrase is *"sufficient accumulated experience to ensure that they have a high probability of being correct."* A high-probability-of-correctness criterion is not the same as a low-update-magnitude criterion. /prescribe should weigh alternative correctness proxies: confidence bounds, PAC-style guarantees, validation on held-out substate replays, inter-rule consistency checks, or other candidates from the literature. The PR's *direction* (gate chunking on some accumulation threshold) is architecture-adjacent to Laird's stated plan; the PR's *specific criterion* is weaker than Laird's phrase and should be treated as one candidate among several, not as inherited infrastructure.

4. **Do not motivate any proposal on "scaling is the bottleneck" grounds.** The Q3 elicitation retired the prior disputed diagnosis's D&L 2013-hardware extrapolation as the binding motivation. Any /prescribe proposal that needs a scaling-is-breaking argument has to show the scaling is actually breaking at the hardware the agent will run on. The C69 *"yes, yes"* rating and C70 *"tens of millions"* rating constrain what counts as "breaking."

## 2. Soft constraints inherited from the framework-level thesis

The thesis in A.md §2 (single clock, forced optimization at rate-mismatched interfaces) is a **human-input hypothesis under test**, not a grounded diagnosis. /prescribe should treat these as framings that may or may not hold, and not as premises.

5. **If the thesis holds, clock-splitting is the unifying direction.** The three invitations (Q1, Q4, Q5) may admit a family of mechanisms that share a clock-splitting move, rather than three one-off fixes. /prescribe could look for such a family.

6. **If the thesis does not hold, C55's single-mechanism commitment is the alternative framing.** In that case, /prescribe should weigh proposals that extend the single-mechanism (impasse → substate → chunking) path rather than introducing parallel scheduling. Extending C67's planned modification within the existing single-mechanism commitment is one candidate in this direction.

7. **The `input_period` knob at `run_soar.cpp:1023` is Soar's own precedent for count-of-cycles gating.** Any proposal that introduces timing differentiation should extend that idiom rather than introduce a foreign scheduler, if feasible.

8. **Experimental-branch precedent matters.** `debug_code/debug.h:9` records that *"experimental chunking and memory consolidation branches"* existed and did not land in mainline. /prescribe should attempt to access those branches (via git history or correspondence) and understand why the work did not ship. Otherwise /prescribe risks repeating a known failure mode.

## 3. Forced-optimization appendix (proposed for /prescribe)

*This appendix argues that clock splits at rate-mismatched interfaces are forced optimizations rather than nice-to-haves. It is presented as an argument for the prescription, not as a diagnostic finding. /prescribe may use it as framing material if the user approves.*

At every rate-mismatched interface in classical computing, a working system has instantiated a clock split. The splits are forced by the rate mismatch itself, not chosen for elegance.

1. **Memory hierarchy (cache ↔ storage).** L1 / L2 / L3 / DRAM are not a performance nicety but a forced optimization: the CPU cannot be fed by DRAM at DRAM rate. Each level runs on its own access-time clock, and coherence protocols manage the splits. [Citation: Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*. Specific edition and chapter to pull before /prescribe consumes.]

2. **Network I/O (network ↔ CPU).** Synchronous blocking on the network wastes CPU cycles that cost more than the network saves. Event loops, socket buffers, and asynchronous completion ports exist because CPU operates at nanosecond rate while network round-trips are milliseconds. [Citation: Kegel's *"The C10K problem"* (original 1999, later revisions). Pull specific version before /prescribe consumes.]

3. **Disk I/O (disk ↔ memory).** Page cache, DMA, asynchronous writeback — each exists because disk is orders of magnitude slower than memory. A synchronous single-clock system at memory rate would waste the CPU; at disk rate would break interactive applications. [Citation: Canonical OS textbook — Tanenbaum or Silberschatz. Pull before /prescribe consumes.]

4. **UI event loops (human ↔ machine).** Sixty-hertz frame rate is the human visual perception bound; backend processing runs at CPU rate. UI frameworks separate the two with event queues because binding them to one clock forces either frame drops or backend starvation. [Citation: Nielsen on response-time thresholds (0.1s, 1s, 10s); *Usability Engineering* 1993. Verify before /prescribe consumes.]

5. **Sleep-dependent memory consolidation (online ↔ offline learning).** The brain separates perception (wake) from consolidation (sleep) because concurrent consolidation interferes with the sensory processing wake is for. This is the biological precedent for the Consolidate-role clock split. [Citation: Diekelmann & Born 2010, *The memory function of sleep*, Nature Reviews Neuroscience. Already cited in prior soap-notes-soar.md; re-verify before /prescribe consumes.]

**Pattern.** At every rate-mismatched interface, a working system has instantiated a clock split. The splits are forced by the mismatch itself. A single-clock architecture at a rate-mismatched interface either throttles the fast side or starves the slow side. There are no working exceptions to the pattern. The biological case is the closest precedent for a Consolidate-role split.

**Proposed prescription direction (for /prescribe to weigh, not for A.md to assert):** give Consolidate a clock of its own. Mechanism candidates — separate thread, time-sliced cycles, periodic wall-clock trigger, subordinate agent — are to be evaluated by /prescribe against the S5 code idiom (`input_period` style) and the experimental-branch precedent in `debug_code/debug.h:9`.

## 4. What is explicitly NOT inherited from A.md

For discipline. /prescribe should not treat the following A.md content as prescription constraints:

- **A.md §2 thesis itself** is a hypothesis under test, not a committed premise. /prescribe should weigh mechanisms compatible with both the thesis-true and thesis-false cases.
- **A.md §3 causal chain** is a framework-level interpretation of the tower table. /prescribe should respect the underlying observations (Q1 gap, Q4 eager commit, Q5 restriction) but not the specific causal linkage to the single-clock root.
- **A.md §5 role verdicts** are diagnoses; the prescription move for each verdict is /prescribe's job.
- **The Q2 "design choice (defended)" verdict for epmem generalization** means /prescribe does not need to propose a generalization mechanism. If /prescribe proposes one anyway, the proposal must engage C49 and C78 directly.
- **The Q3 "compatible with §10" disposition** means /prescribe does not need to propose eviction or forgetting for smem or epmem under current hardware. If such a proposal is offered, it must show the scaling constraint has returned.

## 5. Status and next moves

**Status:** draft. Reviewed against codex feedback on A.md first draft. Held back from /prescribe consumption until:

- S.md is finalized (S2, S3, S4, S6 filed)
- A.md sign-off
- Citations in §3 (forced-optimization appendix) are pulled and verified
- Experimental-branch content referenced in constraint 8 is either accessed or declared inaccessible

**Next:** /prescribe runs after A.md is stable and this file is reviewed once.
