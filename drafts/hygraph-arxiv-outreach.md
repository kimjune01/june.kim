# Hypothesis Graph — arXiv outreach drafts

Outreach for *The Hypothesis Graph: Semantic Memory Written by Methodeutics* (arXiv-pending).
Three clusters. Voice: direct, practitioner, lead with their work and the one result that's theirs to care about.

**Before sending:**
- Links point to https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics for now; swap to the arXiv URL once it's live.
- Deprioritize Sumers unless there's a specific reason — research says he's moved to AI safety, off this topic.
- Unverified contacts: FVDebug (email inferred → site), Yao (likely Tencent now; Princeton address may just forward).
- **Already contacted (2026-05-28, pre-publication) — these are FOLLOW-UPS, not cold opens:** Abdaljalil (Theorem-of-Thought) and Khalid/Arora (CMM). Drafts below are flagged and reframed.
- Wray & Kirk are on the Soar Workshop list with you (via Laird); not strangers.
- **Send order:** the three PRE-MINT fairness-check notes (Pradel, ORACLE-SWE, SLUMP, where you characterize or contrast their result) go out *before* the arXiv mint, asking them to confirm you've represented them fairly. Everyone else is a post-mint send, leading with the posted arXiv link.

---

## Cluster 1 — Programming-with-trust / repair

### Abhik Roychoudhury
**To:** abhik@nus.edu.sg · **alt:** @AbhikRoychoudh1
**Subject:** Programming with trust, made replayable

> Hi Professor Roychoudhury,
>
> You reframed the goal as programming with trust. A hypothesis graph is the unit of trust I think it needs. Every node is a claim bound to a trial an independent party reruns. A fix clears only when its recorded test re-executes, never because anyone vouches for the agent. That puts your verification-in-the-agent reframe into one auditable data structure.
>
> On one contamination-free Verus unsoundness, an externalized comparator carried a weaker model to a fix the strongest released model could not reach on its own. A controlled ablation pins the lift to the verdict source alone. AutoCodeRover shipping into SonarQube is exactly the deployment setting the accountability claim is built for.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Is a replayable per-node trial something a deployed repair agent like the SonarQube one could realistically put in front of a reviewer, or does product scale rule it out?
>
> June Kim (independent, self-funded)

### Martin Monperrus
**To:** monperrus@kth.se · **alt:** @martinmonperrus
**Subject:** Repairnator and replayable agent-repair PRs

> Hi Martin,
>
> Repairnator put autonomous patches in front of real maintainers years before anyone else. My paper is about what would make a maintainer merge one without trusting the author. The deployment thesis: agent PRs are drowning in justified slop suspicion, and a replayable trace is the antidote. It converts "trust my patch" into "audit my ledger." One flux maintainer merged a trace-backed fix I submitted on their hardest open issue, the author invisible to the verdict.
>
> Underneath it is a hypothesis graph of typed nodes, with kill conditions as the executable edges. Every consequential node replays on a clean build. The mechanism result is a two-tier capability lift on a post-cutoff bug, ablated to the external oracle rather than the scaffold. Your RepairBench instinct (grade against something the model can't author) is the same axis I land on.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Would a trace like this have changed how maintainers received Repairnator's patches, or was acceptance never really about the evidence?
>
> June Kim (independent)

### Claire Le Goues
**To:** clegoues@cs.cmu.edu · **alt:** clegoues.bsky.social
**Subject:** AdverIntent and underdetermined repair specs

> Hi Professor Le Goues,
>
> AdverIntent-Agent and this paper circle the same problem from two sides. Your agent infers the intended behavior. I argue the materials a SWE-bench task hands over often don't determine it at all. A determinacy audit of all 728 public Pro tasks puts a 15% floor on the undiscoverable ones. An adversarial challenger at the pre-patch hypothesis stage is where I put the work.
>
> The structure I land on is a hypothesis graph. Each fix carries the inquiry that produced it, replayable by someone who doesn't trust the author. The lead result is a contamination-free Verus bug where a weaker model with an external comparator reaches a fix a stronger model misses.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. When AdverIntent infers intent, what's your ground truth on a bug whose issue text underdetermines it?
>
> June Kim (independent, self-funded)

---

## Cluster 2 — Cognitive-architecture lineage

Warmest pair: **Wray + Kirk** (verified CIC emails, actively doing LLM × Soar). **Narasimhan** strong (SWE-bench creator + agent memory). **Yao** worth a note, likely Tencent now. **Sumers** deprioritized (moved to safety/red-teaming).

### Robert Wray & James Kirk
**To:** robert.wray@cic.iqmri.org, james.kirk@cic.iqmri.org
**Subject:** Filling the Soar smem slot, falsifiably

> Hi Dr. Wray, Dr. Kirk,
>
> You argued LLM agents should inherit cognitive-architecture design patterns. My paper instantiates that for one slot: the Soar semantic-memory store. I adopt the Soar memory typology as vocabulary, then fill the semantic-memory slot with a Peirce-typed, kill-conditioned hypothesis graph. A node is a claim bound to an executable trial. The manner of a hypothesis's death names its successor. It holds a *falsifiable* structure rather than verified facts, the gap I couldn't fill from the existing CoALA mapping.
>
> The mechanism result is a contamination-free coding bug where the externalized structure carried a weaker model past a stronger one.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Does the smem framing earn the Soar lineage, or am I overclaiming the mapping? And who else in the CIC orbit should see it?
>
> June Kim (independent)

### Karthik Narasimhan
**To:** karthikn@princeton.edu
**Subject:** A determinacy audit of SWE-bench Pro

> Hi Professor Narasimhan,
>
> Two threads of yours meet in this paper. SWE-bench is the substrate. My determinacy audit of all 728 public Pro tasks argues the benchmark mostly measures specification-to-implementation translation. A 15% floor of tasks have materials that don't determine the intended behavior. Separately, your work on agent self-improvement through experience is the live question I try to give a structure. That structure is a hypothesis graph as semantic memory that persists past the context window. It's typed and replayable, so a later run reruns a node instead of trusting it.
>
> The headline is a two-tier capability lift on a post-cutoff bug, ablated to the verdict source. I think the audit may be the part most useful to you.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Does a 15% underdetermined floor match what you've seen in Pro, or would you have guessed lower?
>
> June Kim (independent, self-funded)

### Shunyu Yao
**To:** shunyuy@princeton.edu · **alt:** @ShunyuYao12
**Subject:** Grading the trace, not the patch

> Hi Shunyu,
>
> "The Second Half" names evaluation as the frontier, and ReAct is the baseline this paper measures against. Scoring a final patch misses the in-run reasoning, so I make the trace itself the gradable object. It's a hypothesis graph of typed nodes, each a claim bound to a trial a stranger reruns. A ReAct trace's continuation policy lives in the controller and never in the record.
>
> The result is a contamination-free bug where an external comparator carried a weaker model to a fix a stronger one missed, pinned by ablation to the verdict source. "Score submissions on replayability" is the concrete version of the second-half move.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Is replayability an axis you'd actually want in a benchmark, or does collecting it cost too much at scale?
>
> June Kim (independent)

---

## Cluster 3 — Sibling-paper authors

Framing across all: *we arrived at adjacent points independently, here's the join* — never "you missed my prior work." Blog timestamps (Theory is load-bearing 2026-03-17, The Hypothesis Graph 2026-04-28) predate ADI and CMM, so provenance can be mentioned lightly.

### Kaiyu He (IDEA)
**To:** kaiyu.he@utdallas.edu
**Subject:** IDEA and a Peirce-typed coding agent

> Hi Kaiyu,
>
> IDEA and my paper reach for the same trichotomy from different domains. You run Peirce's three modes on RULEARN. I enforce them at write time per stage in a coding agent, each node capped at the confidence its mode earns. Several near-simultaneous papers reach for the trichotomy without crediting Peirce. Yours names him, and mine leans on him too.
>
> The coding-specific result is a contamination-free bug where externalizing the inductive check (a verdict the model can't author) produced a two-tier capability lift.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Does write-time typing map onto what you saw on RULEARN?
>
> June Kim (independent)

### Samir Abdaljalil (Theorem-of-Thought) — FOLLOW-UP to 2026-05-28 note
**To:** sabdaljalil@tamu.edu · **cc:** hkurban@hbku.edu.qa (co-author, was on the first note)
**Subject:** Re: Citing Theorem-of-Thought

> Hi Samir,
>
> Following up on my note from May. The paper's now posted, and it cites Theorem-of-Thought as an independent sibling. You type the three modes into separate agents. I run the same cycle but persist it as memory across cycles, so a kill condition fires live and the graph routes the next run. The typed cycle without persistence and persistence without the cycle look like complementary halves.
>
> The applied result is a coding bug where externalizing the inductive check carried a weaker model past a stronger one.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. What keeps ToT's three agents from collapsing into one pass: is the NLI coherence check enough on its own?
>
> June Kim (independent)

### Sankalp & Shlok Gilda (ADI)
**To:** shlok.gilda@ufl.edu (corresponding), sankalp.gilda@gmail.com
**Subject:** ADI and a hypothesis graph: invariants vs replay

> Hi Sankalp, Shlok,
>
> ADI is the closest thing to what I built that I've found, and near-simultaneous. Mine runs the same three modes over a coding agent's hypothesis graph. Propagation is a credence capped by the mode that earned a node. The invariant is replay: every node reconstructible from its recorded trial. Your "weakest link" bound and my mode-capped credence feel like the same instinct in different formalisms.
>
> The applied result is a contamination-free coding bug with a two-tier capability lift, ablated to the external verdict source.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Do the algebraic invariants buy you anything replay doesn't: soundness without re-execution?
>
> June Kim (independent)

### Sazan Khalid & Amit Arora (CMM) — FOLLOW-UP to 2026-05-28 note
**To:** sk2153@georgetown.edu (Sazan; delivered last time) · **Amit:** amiarora@amazon.com BOUNCED on the first note → reach via GitHub aarora79
**Subject:** Re: Heads-up — citing your Cognitive Memory Manager paper

> Hi Sazan, Amit,
>
> Following up on my May heads-up: the paper's now posted. CMM is the closest comparison I found for the agent-trace part of it, and we point opposite ways. You extract the typed DAG post hoc and graduate stable patterns into skills. Mine generates the graph live, with kills firing during the run. Observe-and-consume against perturb-and-falsify. They look complementary. I have ~385 hypothesis graphs committed to a public repo from OSS deployment, close to the corpus your graduation pipeline is built to consolidate.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. The graphs are at github.com/kimjune01/sweep: would they feed CMM's graduation pipeline as-is, or is the format too far off?
>
> June Kim (independent)

### Yunsheng Bai (FVDebug): loose sibling, optional
**To:** via yunshengb.com or LinkedIn (email unverified)
**Subject:** FVDebug, and choosing the next node mechanically

> Hi Yunsheng,
>
> FVDebug and my paper both build a graph over failure evidence and walk it toward a root cause. You work in hardware formal verification, me in software repair. One design difference: your LLM picks what to look at next by narrative exploration. I hand that choice to a mechanical kill predicate. A node dies when its trial fires, not because a model decided to move on. I cite you as an adjacent case, not an exact match.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Would removing the model from next-node selection even be desirable in formal verification, or is the narrative load-bearing there?
>
> June Kim (independent)

---

## Cluster 4 — Intro-citation authors (named the gap)

The survey/position authors your introduction cites as naming the missing piece. Frame: *you named this gap; a year on it's still open; here's the structure built into it.* All three are clean: the intro cite for Wang/Leeds was requalified to "persistent memory among the open challenges," which matches the draft's hook, so it's no longer contingent.

### Asaf Yehudai (evaluation survey)
**To:** Asaf.Yehudai@ibm.com
**Subject:** Evaluating agents by trajectory, not output

> Hi Asaf,
>
> Your 2025 survey calls for trajectory-level assessment. A replayable reasoning trace is what makes a trajectory gradable. My paper turns the trajectory into that object: a hypothesis graph where each node is a claim bound to a trial an independent reader reruns. I cite the survey in the intro as naming exactly this gap.
>
> The applied result is a contamination-free coding bug where grading the trajectory rather than the patch separated a general fix from a narrow one that passed the same tests.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Is trajectory-level scoring something you'd want a benchmark to require, or does collecting replayable traces cost too much to standardize?
>
> June Kim (independent)

### Yiling Lou (SE-agent survey)
**To:** yilinglou@illinois.edu · **alt:** yilinglou@fudan.edu.cn
**Subject:** The memory gap your SE-agent survey named

> Hi Professor Lou,
>
> Your 2024 survey named persistent agent memory as a missing piece. A year on it's still open, and replayable reasoning traces are my answer. The structure is a hypothesis graph as semantic memory that holds an agent's live reasoning. Each node is a claim bound to a trial a later run or a human can rerun. I open the paper on surveys like yours naming the gap.
>
> The result is a contamination-free coding bug where the externalized structure carried a weaker model to a fix a stronger one missed.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Of the 124 papers you surveyed, did any persist reasoning as a replayable structure you could refute, or did memory stay facts-and-traces?
>
> June Kim (independent)

### Huanting Wang & Zheng Wang (agentic-programming survey)
**To:** H.Wang7@leeds.ac.uk, z.wang5@leeds.ac.uk
**Subject:** Agentic programming, and a persistent reasoning memory

> Hi Huanting, Zheng,
>
> Your 2025 survey lists persistent memory among the open challenges for coding agents. Replayable reasoning traces are my answer to that one. The structure is a hypothesis graph as semantic memory that holds an agent's live reasoning. It's typed and replayable, so a later run reruns a node instead of trusting it. I cite the survey in the intro.
>
> The result is a contamination-free coding bug where the externalized structure carried a weaker model to a fix a stronger one missed.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Of the memory approaches you surveyed, did any hold falsifiable hypotheses rather than verified facts, or is that slot still open?
>
> June Kim (independent)

---

## Cluster 5 — Citation siblings (same-edge / posed the problem)

Authors whose contemporary work the paper engages directly. Tier 1 = same-edge siblings or people whose open problem you answer; Tier 2 = adjacent, plausible. Frame stays collegial: *we reached the same edge; here's where the line differs.* Not the papers you rebut (SWE-Effi / GradleFixer / Confucius) — those need a different posture and aren't here.

### Tier 1

#### Kexin Huang (POPPER)
**To:** kexinh@cs.stanford.edu
**Subject:** POPPER, and falsification that persists

> Hi Kexin,
>
> POPPER and my paper take the same sequential-falsification stance. You run it under strict Type-I error control, me inside a coding agent. The difference is where it stops and what it leaves behind. I terminate on a deterministic kill predicate over a single binary verdict, not an error-rate bound over a population. Each falsification persists as a replayable node, where POPPER's tests are ephemeral.
>
> The applied result is a contamination-free coding bug where externalizing the kill condition carried a weaker model to a fix a stronger one missed.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Does the e-value machinery still earn its keep when the system under test is deterministic and one trial settles the verdict, or does it only pay off under noise?
>
> June Kim (independent)

#### Yiqi Wang (From Agent Traces to Trust)
**To:** yiqi.wang.jennie@gmail.com
**Subject:** Provenance quality, with replay as the bar

> Hi Yiqi,
>
> Your survey names an open problem: how to evaluate provenance quality. Replayable reasoning traces are an answer. In my paper the quality bar is replay itself: a stranger reruns a node's recorded trial. Your Invalidate relation becomes an executable kill condition rather than a descriptive label.
>
> The mechanism result is a contamination-free coding bug where the externally-graded kill carried a weaker model to a fix a stronger one missed.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Would replayability work as a general quality metric across the methods you surveyed, or does it only bind where the trace is a deterministic command?
>
> June Kim (independent)

#### Santhosh Kumar Ravindran (Portable Agent Memory)
**To:** santhosh.ravindran@microsoft.com
**Subject:** Portable agent memory: integrity vs warrant

> Hi Santhosh,
>
> Portable Agent Memory and my paper are the closest things I've found to each other on agent-memory transfer. They certify different things. Your Merkle-DAG certifies integrity: the recorded bytes are untampered. My replay invariant certifies warrant: the node still survives its trial when a stranger reruns it. The two compose, and I think yours is the transport layer mine would ride on.
>
> The applied result is a contamination-free coding bug where a node that replays carried a weaker model to a fix a stronger one missed.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Does your protocol have a place for a node whose bytes verify but whose claim no longer replays, or is warrant out of scope by design?
>
> June Kim (independent)

#### Wang, Pradel & Liu ("Are 'Solved Issues' Really Solved Correctly?") — PRE-MINT fairness check
**To:** liu_zx@zju.edu.cn (corresponding), michael@binaervarianz.de · **cc:** prinzywang@zju.edu.cn
**Subject:** Patches that pass but diverge from intent

> Hi Zhongxin, Michael, You,
>
> Your ICSE study found plausible patches pass SWE-bench tests yet diverge from developer intent. My paper draws a line next to it. Your axis is patches that pass but are wrong. Mine is tasks whose materials don't determine which passing behavior was intended in the first place. Same crack in the bench, one upstream of the other.
>
> The lead case is a contamination-free Verus bug whose own suite passes for both a narrow and a general fix. It can't see the distinction the fix has to make, the blind spot your work documents at the patch level.
>
> The draft is at https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics, headed to arXiv shortly. Before that version locks, I want to be sure I've drawn the line between our two axes fairly. If I've mischaracterized yours, tell me and I'll fix it. (And if you're up for it: could PatchDiff tell a genuinely underdetermined task apart from a wrong patch, or do both just read as "differs from ground truth"?)
>
> June Kim (independent)

#### ORACLE-SWE (Kenan Li, Qirui Jin) — no printed email; PRE-MINT fairness check
**To:** no email in paper → reach via the arXiv submitter (Qirui Jin, Georgia Tech; Scholar profile) or Kenan Li (Microsoft)
**Subject:** ORACLE-SWE, and oracle signals as a category line

> Hi Qirui,
>
> ORACLE-SWE and my determinacy audit measure the same handover: the oracle and specification signals that leak through a SWE-bench task. We read it oppositely. You ablate the leak and measure the drop. My audit of all 728 public Pro tasks draws it as a category boundary, since a spec-conformance instrument and a measure of diagnostic inquiry are different types.
>
> The lead case is a contamination-free bug. With the leak gone, externally-graded inquiry carried a weaker model to a fix a stronger one missed.
>
> The draft is at https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics, headed to arXiv shortly. I part from you on the verdict, so before that version locks I'd like to know I've represented your result fairly. Tell me if the contrast is off. (And the real question: once you ablate the oracle signals, is what's left a weaker version of the same task, or a different task entirely?)
>
> June Kim (independent)

#### Xiangyu Zhang (SLUMP) — email is senior author's directory address; PRE-MINT fairness check
**To:** xyzhang@cs.purdue.edu (senior author; first author Lu Yan printed no email)
**Subject:** SLUMP, and underspecification as a category

> Hi Professor Zhang,
>
> SLUMP opens on a premise my paper shares: benchmarks hand over the full specification upfront while real coding reveals it progressively. We part on the remedy. You build an underspecified-by-design benchmark. My determinacy audit treats the handover as a category boundary, since a spec-conformance instrument and a measure of diagnostic inquiry are different types.
>
> The lead case is a contamination-free post-cutoff bug where discovery is the whole difficulty and the suite can't tell a narrow fix from a general one.
>
> The draft is at https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics, headed to arXiv shortly. We part on the remedy, so before that version locks I'd like to be sure I've stated SLUMP's position fairly. Correct me if I've got it wrong. (And a real question: can a benchmark keep measuring faithfulness loss as specs get more emergent, or does it become a different instrument?)
>
> June Kim (independent)

### Tier 2

#### Petr Anokhin (AriGraph)
**To:** anokhin@airi.net
**Subject:** AriGraph, and a falsifiable graph memory

> Hi Petr,
>
> AriGraph is the closest precedent I found for graph-structured agent memory. My paper sits one step over. The nodes aren't entities and relations but falsifiable claims, each bound to a trial a stranger can rerun. An edge is generated when a hypothesis is killed. Where AriGraph remembers what's true, this remembers what was tested.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Did you ever want an AriGraph node to carry a kill condition, a way to retract it on evidence, or did the world-model framing make that unnecessary?
>
> June Kim (independent)

#### Yikuan Huang & Zheqi Fan (From Hypotheses to Factors)
**To:** yk.huang@connect.ust.hk, zheqi.fan@connect.ust.hk
**Subject:** Perturb-and-falsify, outside finance

> Hi Yikuan, Zheqi,
>
> From Hypotheses to Factors runs the same loop my paper does: falsifiable hypotheses behind a deterministic engine over an append-only trace. You run it in crypto markets, me in software repair. I cite it as a sibling that locks the loop to one domain, where I claim the general semantic-memory substrate. The identical structure surfacing in trading was the clearest sign to me that the shape isn't domain-specific.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. In your loop, what plays the role of the external oracle when ground truth is future price rather than a test?
>
> June Kim (independent)

#### Wisdom Dogah (Traxia)
**To:** wisdom.dogah@traxia.ai
**Subject:** Verifiable agent-native publishing, converging

> Hi Wisdom,
>
> Traxia and a line of my writing converged on the same primitives within days of each other. We both make truth and uncertainty first-class in verifiable, agent-native reasoning. My paper lands them as a data structure: a hypothesis graph where a claim counts as knowledge only after it survives a replayable trial. I cite Traxia as independent convergence on the verification-first stance.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. In Traxia, what's the unit a reader reruns to check a published claim, and does it travel with the claim or sit in a separate ledger?
>
> June Kim (independent)

#### Sayash Kapoor & Arvind Narayanan (HAL)
**To:** sayashk@princeton.edu · **cc:** arvindn@princeton.edu
**Subject:** Extending HAL's cost transparency with traces

> Hi Sayash, Arvind,
>
> HAL set the precedent my paper builds on for agent evaluation: cost as a first-class axis, not just accuracy. My receipts extend that with a re-gradeable per-instance cost ledger, plus gate traces and hypothesis graphs. A reviewer recomputes every number and replays the reasoning, not just reads the score. I cite HAL as the cost-transparency precedent.
>
> The bench run reports a determinacy-aware denominator on SWE-bench Pro rather than a bare resolve rate, which I think is the axis the model × scaffold × benchmark grid is missing.
>
> https://www.june.kim/the-hypothesis-graph-semantic-memory-methodeutics. Would a replayability dimension fit the HAL grid, or is per-instance trace publication too heavy to standardize across submissions?
>
> June Kim (independent)

---

## Contact reference

| Person | Cluster | Channel | Verified? |
|---|---|---|---|
| Abhik Roychoudhury | repair/trust | abhik@nus.edu.sg · @AbhikRoychoudh1 | yes |
| Martin Monperrus | repair/trust | monperrus@kth.se · @martinmonperrus | yes |
| Claire Le Goues | repair/trust | clegoues@cs.cmu.edu · clegoues.bsky.social | yes |
| Robert Wray | cog-arch | robert.wray@cic.iqmri.org | yes |
| James Kirk | cog-arch | james.kirk@cic.iqmri.org | yes |
| Karthik Narasimhan | cog-arch | karthikn@princeton.edu · @karthik_r_n | yes |
| Shunyu Yao | cog-arch | shunyuy@princeton.edu · @ShunyuYao12 | email yes (alumni); Tencent unconfirmed |
| Ted Sumers | cog-arch | @tedsumers (DM) | no email; deprioritized |
| Kaiyu He | sibling | kaiyu.he@utdallas.edu | yes |
| Samir Abdaljalil | sibling | sabdaljalil@tamu.edu (cc hkurban@hbku.edu.qa) | yes — emailed 5/28, follow-up |
| Shlok Gilda | sibling | shlok.gilda@ufl.edu | yes |
| Sankalp Gilda | sibling | sankalp.gilda@gmail.com | yes |
| Sazan Khalid | sibling | sk2153@georgetown.edu | yes — delivered 5/28, follow-up |
| Amit Arora | sibling | amiarora@amazon.com BOUNCED → GitHub aarora79 | bounced 5/28 |
| Yunsheng Bai | sibling | yunshengb.com · LinkedIn | email inferred only |
| Asaf Yehudai | intro-cite | Asaf.Yehudai@ibm.com | yes |
| Yiling Lou | intro-cite | yilinglou@illinois.edu · alt yilinglou@fudan.edu.cn | yes |
| Huanting Wang | intro-cite | H.Wang7@leeds.ac.uk | yes |
| Zheng Wang (Leeds) | intro-cite | z.wang5@leeds.ac.uk | yes |
| Kexin Huang (POPPER) | cite-sibling T1 | kexinh@cs.stanford.edu | yes |
| Yiqi Wang (Traces→Trust) | cite-sibling T1 | yiqi.wang.jennie@gmail.com | yes (personal gmail, per paper) |
| Santhosh K. Ravindran (Portable Mem) | cite-sibling T1 | santhosh.ravindran@microsoft.com | yes |
| Zhongxin Liu / Pradel / You Wang | cite-sibling T1 | liu_zx@zju.edu.cn, michael@binaervarianz.de, cc prinzywang@zju.edu.cn | yes |
| ORACLE-SWE (Jin/Li) | cite-sibling T1 | no email in paper → arXiv submitter / Microsoft | NO email |
| Xiangyu Zhang (SLUMP) | cite-sibling T1 | xyzhang@cs.purdue.edu (senior; 1st author no email) | directory, not in paper |
| Petr Anokhin (AriGraph) | cite-sibling T2 | anokhin@airi.net | yes |
| Yikuan Huang / Zheqi Fan | cite-sibling T2 | yk.huang@connect.ust.hk, zheqi.fan@connect.ust.hk | yes |
| Wisdom Dogah (Traxia) | cite-sibling T2 | wisdom.dogah@traxia.ai | yes |
| Sayash Kapoor / Arvind Narayanan (HAL) | cite-sibling T2 | sayashk@princeton.edu, cc arvindn@princeton.edu | yes |
