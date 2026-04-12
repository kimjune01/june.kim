---
system: Soar
target: SoarGroup/Soar
stage: production/legacy
intake_input: ./S.md (finalized 2026-04-10, elicitation complete)
diagnose_run: 2026-04-10
diagnose_status: updated — reflects finalized S.md and elicitation
upstream_ref: origin/development @ f65f626e4 (2026-03-05) — SoarGroup/Soar
---

# Soar — Objective (tower table + code evidence)

*Evidence only. No role evaluation, no causal chain, no prescription. Any phrase that classifies a role as "broken," "missing as a failure," "design choice," or "blind spot" belongs in A.md, not here.*

## Status

S.md is finalized as of 2026-04-10. Sources S1 (Laird 2022), S2 (Derbinsky & Laird 2013), S5 (upstream source code), and S6 (meeting correspondence with Laird, 2026-04-09) are filed. S3 (Gentle Introduction) and S4 (manual) remain unfiled but are not load-bearing for any current tower-table cell. Elicitation is complete; answers are recorded in S.md and reflected throughout this file.

### Sources consulted

- **S1** Laird, J. E. (2022). *Introduction to the Soar Cognitive Architecture*. arXiv:2205.03854. §1–§7, §8 partial, §9.1–§9.3, §10 filed.
- **S2** Derbinsky, N. & Laird, J. E. (2013). *Effective and efficient forgetting of learned knowledge in Soar's working and procedural memories.* Cognitive Systems Research. Filed as C74–C82.
- **S5** `github.com/SoarGroup/Soar` at `origin/development` f65f626e4. Modules inspected: `decision_process/`, `soar_representation/`, `semantic_memory/`, `episodic_memory/`, `explanation_based_chunking/`, `reinforcement_learning/`, `shared/enums.h`.
- **S6** Correspondence with John Laird, 2026-04-09 meeting (paraphrased by June Kim). Filed as C90–C92.
- **Not consulted:** S3 (Gentle Introduction), S4 (manual).

## Upstream discipline

**S5 in this pass = `origin/development` at commit `f65f626e4` (2026-03-05, "Merge pull request #572 from moschmdt/cmake").** This is the canonical SoarGroup/Soar tree.

The repository on disk is currently checked out on local branch `smem-sweep-dominated`, which contains three unmerged commits by June Kim dated 2026-03-27:

- `e32d4d65e` Add smem --redundancy-check for tree inclusion detection
- `db2c86108` Add smem --sweep-dominated: budgeted mark-and-sweep eviction of dominated LTIs
- `92204812b` Add delete_ltm: full LTI deletion with proper bookkeeping

These add a new file `Core/SoarKernel/src/semantic_memory/smem_inclusion.cpp` containing `CLI_redundancy_check`, `CLI_sweep_dominated`, and a `smem_lti_has_r4_dependents` safety check with an explicit reference to *"Derbinsky & Laird's R4 forgetting policy"*. **This work is not part of Soar-the-architecture yet.** It is downstream from the prior disputed diagnosis and represents proposed work in progress. It is **excluded from the S5 evidence base** for this intake. A.md may reference it as author-local context; O.md must not.

All `origin/development:…` citations below have been verified against the upstream tree, not the local checkout.

---

## Tower table: Soar → framework role mappings

**Stack levels.** Three observed stack levels in Soar:

- **@ top** — the decision cycle itself (Input → Propose → Decide → Apply → Output)
- **@ Remember** — the long-term stores as sub-pipelines (each memory has its own internal structure)
- **@ Consolidate** — the learning modules as sub-pipelines (chunking, RL, episodic snapshot, smem deliberate write)

### Glossary (framework mappings grounded in evidence)

| Soar term | Proposed role(s) | Confidence | Evidence |
|---|---|---|---|
| Working memory | Cache | high | Short-term store holding situational state; tested by rules. [C3, C14] |
| Preference memory | Filter-stage buffer | medium | Holds preferences created by rules during elaboration; consumed by decision procedure. [C15] |
| Procedural memory | Remember (the store) + Consolidate (learning path) | medium | Holds rules. Productions written by chunking and updated by RL. [C2, C19] |
| Semantic memory | Remember (the store); Consolidate write path is deliberate only | medium-high (store) | Current write path per C42: deliberate agent-initiated storage. C71 lists "semantic learning" as still missing. C84 Figure 6: source of knowledge is "Existence in Working memory." Elicitation Q1: open problem from Laird's perspective. |
| Episodic memory | Remember (the store) + mechanical snapshot at decision boundary | high (store), medium (snapshot) | Storage is automatic per C45 — mechanical snapshotting of WM, not derivation of new knowledge. Retrieval is deliberate per C46. |
| Perceptual long-term memory | Remember (the store) | low | Accessed via SVS. §8 only partially read. [C3, C4, C89] |
| Operator | Spans proposal/evaluation/selection/application | medium | Structural unit, not a single role. Different phases map to Filter, Attend, Remember/Cache. [C9, C10] |
| Elaboration rules (narrow) | Cache | medium | "Create new structures entailed by existing structures in working memory." [C23] |
| Operator proposal rules | Filter | medium | "Test preconditions or affordances." Gating function. [C24] |
| Operator evaluation rules | Filter (ranking) or Attend (selection) | low | Where Filter ends and Attend begins is an A.md question. [C25, C16] |
| Operator selection (decision procedure) | Attend | high | Fixed procedure processes preference memory to pick one operator. [C26] |
| Operator application rules | Remember (write path) + Cache (WM mutation) | medium | Non-monotonic changes to WM. [C27, C28] |
| Chunking | Consolidate (write to procedural) | medium-high | Compile path from substate reasoning to procedural knowledge. Output includes RL rules per C34. [C61–C64] |
| RL | Consolidate (update numeric preferences) | high | Updates after operator application, using reward + expected future reward. Fallback layer per C31. [C29–C33] |
| Episodic learning | Automatic snapshot storage without generalization | medium-high | Per C45 and C49. Laird defends this as a learning method without generalization. |
| Decision cycle | (the pipeline itself) | high | Input → Elaboration → Selection → Application → Output. [C17] |
| Decision procedure | Attend | high | [C26] |
| Impasse | Consolidate trigger + control flow signal | medium | Double duty: control flow branching and chunking trigger. [C12, C62] |

### Top level (decision cycle)

| # | System term (Soar vocabulary) | Role | Stack | Evidence | Confidence |
|---|---|---|---|---|---|
| 1 | Input phase + perception buffers, SVS perception input | Perceive | top | `enums.h:208 INPUT_PHASE = 0` as first phase of `top_level_phase` enum; `run_soar.cpp:500 thisAgent->current_phase = PROPOSE_PHASE` on exit. S1 §2.1 direct quote (C18): *"the input phase processes data from perception, SVS, and retrievals from semantic and episodic memory, and adds that information to the associated buffers in working memory."* | medium (SVS detail deferred to §8 read) |
| 2 | Symbolic working memory (WM) | Cache | top | S1 §1 Fig.1, §1 p.2 (C3), §2.2 p.5 (C19, C20). Truth maintenance via retraction of I-supported structures when instantiations no longer match (C20). Primary data held in `soar_representation/working_memory.h`. | high |
| 3 | Elaboration phase (narrow: elaboration rules) | Cache (derivation) | top | S1 §2.2.1 (C23): *"create new structures entailed by existing structures in working memory."* Fires monotonically, retracted on instantiation death (C20, C21). | medium |
| 4 | Operator proposal rules | Filter (gating) | top | S1 §2.2.2 (C24): *"test the preconditions or affordances of an operator and create an explicit representation."* Creates acceptable preferences. Fires inside `PROPOSE_PHASE` (run_soar.cpp:506). | medium |
| 5 | Preference memory | Filter-stage buffer | top | S1 §2 p.4 (C15). Holds preferences created by evaluation rules, consumed by decision procedure. | low |
| 6 | Operator evaluation rules | Filter → Attend boundary | top | S1 §2.2.3 (C25, C16). Creates relative/absolute preferences and numeric preferences encoding expected future reward. | low |
| 7 | Decision procedure (fixed routine processing preference memory) | Attend | top | S1 §2.3 p.6 (C26) direct quote: *"a fixed decision procedure processes the contents of preference memory to choose the current operator."* Implementation: `decision_process/decide.cpp:1104 byte run_preference_semantics(agent*, slot*, preference**, bool, bool)`. Section banners at `decide.cpp:1191` Requires, `:1251` Acceptables–Prohibits–Rejects (grouped), `:1326` Better/Worse, `:1504` Bests, `:1573` Worsts, `:1662` Indifferents. Six named sections; unrolling Acceptables–Prohibits–Rejects yields the eight-step sequence the prior diagnosis cited. | high |
| 8 | Operator application rules | Remember (write path) + Cache (WM mutation) | top | S1 §2.4 p.6 (C27, C28). Non-monotonic WM mutation; additional write targets: motor buffer, SVS buffers, smem cue buffer, epmem cue buffer. | medium |
| 9 | Output phase + motor buffer | Remember (external write) | top | `enums.h:208 OUTPUT_PHASE`; `run_soar.cpp:858` end-of-output dispatch. | medium |
| 10 | Procedural memory (store of productions) | Remember | top, inner at Consolidate | S1 §1 Fig.1, §2.2 p.5 (C19). RETE-indexed production store. Implementation in `decision_process/rete.cpp`. | high |
| 11 | Semantic memory (store) | Remember | top, inner at Consolidate (current write path only) | S1 §1, §6 (C2, C36, C39, C40). Graph-structured store with activation-biased retrieval. Implementation in `semantic_memory/`. | high (store) |
| 12 | Episodic memory (store) | Remember | top, inner at Consolidate | S1 §1, §7 (C2, C44, C45, C48). Delta-encoded snapshot store. Implementation in `episodic_memory/`. | high |
| 13 | Perceptual long-term memory / SVS | Remember (non-symbolic) | top | S1 §1 Fig.1, §1 p.2 (C3, C4). **§8 partially read.** | low |
| 14 | Impasse → substate | Control flow (branching) + Consolidate trigger | top; substate inherits its own top-level | S1 §2 p.4 (C12), §3 (C56–C60). Recursive invocation of the decision cycle on a nested state. Chunking fires when substate results are created (C62), making impasse also a Consolidate trigger. | medium |
| 15 | Chunking (EBBS) | Consolidate (write to procedural) | — | See "Chunking sub-pipeline" below. | medium-high |
| 16 | Reinforcement learning (RL update on numeric preferences) | Consolidate (update existing rules) | — | See "RL sub-pipeline" below. | high |
| 17 | Automatic episodic store (`epmem_new_episode`) | Perceive → Remember mechanical snapshot (not Consolidate) | inner at Remember (epmem sub-pipeline) | See "Episodic memory sub-pipeline" below. | high that it is mechanical; medium that "not Consolidate" is the right label |
| 18 | Deliberate semantic store (`store_new` via agent rules) | Remember (write path from agent cognition) | — | See "Semantic memory sub-pipeline" below. | high (that this is the current write path) |

Blank cells at the top level: **none at the forward pass (Perceive/Cache/Filter/Attend/Remember all filled)**; Consolidate rows appear only under the sub-pipeline treatment below.

### Top-level decision cycle — textual diagram

```
  ┌─────────┐   ┌────────────────────────────────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
  │ INPUT   │ → │ PROPOSE (elaboration wave)         │ → │ DECIDE  │ → │ APPLY   │ → │ OUTPUT  │
  │ Perceive│   │  ├ elaboration rules    [Cache]    │   │ Attend  │   │ Remember│   │ Remember│
  │         │   │  ├ proposal rules       [Filter]   │   │ (fixed  │   │ (non-   │   │ (motor, │
  │ sym WM  │   │  └ evaluation rules     [Filter/   │   │  decision│  │  mono-  │   │  epmem  │
  │ buffers │   │                         Attend?]   │   │  proc)  │   │  tonic  │   │  trigger│
  │ filled  │   │  → preference memory    [buffer]   │   │         │   │  WM mut)│   │  here)  │
  └─────────┘   └────────────────────────────────────┘   └─────────┘   └─────────┘   └─────────┘
       ↑                                                                                    │
       │                                                                                    │
       └────────────────────────────── quiescence / next cycle ────────────────────────────┘

  Impasse (any phase): push substate → recursive decision cycle at level+1
                         on return: back-trace + EBBS → chunk written to procedural memory
```

---

## Sub-pipelines (Remember-level towers)

### Procedural memory sub-pipeline

| System term | Role | Evidence |
|---|---|---|
| Rule conditions (LHS) over WM | Perceive (into rete) | `decision_process/rete.cpp` `add_wme_to_rete`, `remove_wme_from_rete`. Incremental match. |
| Beta network activation state | Cache | Alpha/beta memories in `rete.cpp`. RETE caches partial match state. |
| Refraction / instantiation de-dup | Filter | S1 §2.2 (C19): *"All rules in Soar fire only once for a specific match to data in working memory."* |
| (no ranking among matched rules — all fire in parallel) | Attend = blank by design | S1 §2.2 (C21): elaboration proceeds in waves without ordering among rule types. |
| Production store (RHS + LHS, compiled RETE nodes) | Remember | `decision_process/rete.cpp` net; `soar_representation/production.h`. |
| Chunking + RL (write path into this store) | Consolidate | See below. |
| Excision (`excise_production_from_rete`) | eviction path | `rete.cpp:3975 excise_production_from_rete`; `run_soar.cpp:890 excise_production(thisAgent, const_cast<production*>(*p), false)`. Duplicate justifications auto-excise (`rete.cpp:3823`). Chunking itself excises on dup (`ebc_build.cpp:619`). No BLA-driven automatic excision policy visible in upstream — only CLI / duplicate-driven. |

### Semantic memory sub-pipeline

| System term | Role | Evidence |
|---|---|---|
| Cue buffer receive (`^query` / `^store` WMEs written by operator application rules) | Perceive (into smem) | S1 §6 (C40); `semantic_memory.cpp:480 cmd_store_new` path. |
| Spreading-activation + base-level-activation ranking | Filter (ranking) | S1 §6 (C41). Implementation in `semantic_memory/smem_activation.cpp`. Uses a `wma_decay_element` for the spread-source calculation (`smem_activation.cpp:1139 total_element.forget_cycle = 0`) — **note:** the `forget_cycle` field is re-used as a bookkeeping slot for the spreading math, **not** as a forget mechanism over smem. |
| Best-match selection | Attend | S1 §6 (C40): *"the cue is used to search semantic memory for the concept that best matches the cue, and once that is determined, the complete concept is retrieved into the working memory buffer."* |
| Retrieved concept written to smem result buffer → WM | Remember (read-return path) | Same §6 quote. |
| LTI store (SQLite-backed graph) | Remember (the store itself) | `semantic_memory/smem_db.cpp` schema. |
| **Write path from the agent** (`store_new` → `STM_to_LTM`) | Consolidate (deliberate) | `semantic_memory.cpp:480–500` invokes `store_new`. `smem_store.cpp:597 void SMem_Manager::store_new(...)` and `smem_store.cpp:608 void SMem_Manager::STM_to_LTM(...)`. Triggered by the `cmd_store_new` command path, which is how operator application rules ship WMEs into smem. This **is** the current smem write path. S1 §6 (C42): *"an agent can deliberately store information at any time."* |
| **Automatic write path** (a background mechanism that writes smem from other memories) | blank | S1 §6 (C42): *"As of yet, Soar does not have an automatic learning mechanism for semantic memory."* S1 §10 item 7 (C71): *"there are still types of architectural learning that are missing, such as semantic learning."* Elicitation Q1 answer: open problem from Laird's perspective (C71 confirms the gap). |
| **Forgetting / eviction path** | blank | Verified by grep: `git grep -i forget origin/development -- Core/SoarKernel/src/semantic_memory/` returns one match, `smem_activation.cpp:1139`, which is the bookkeeping re-use noted above, not a forget policy. No analog of `wma_forget_pq` exists in the upstream smem module. |

### Episodic memory sub-pipeline

| System term | Role | Evidence |
|---|---|---|
| Topstate snapshot assembly | Perceive (of WM → epmem) | S1 §7 (C45): *"An episode is a snapshot of the structures in the topstate. A new episode is automatically stored at the end of each decision."* |
| Delta encoding (only changes between episodes stored) | Cache / compression | S1 §7 (C48): *"Soar minimizes the memory overhead of episodic memory by storing only the changes between episodes."* Implementation: `episodic_memory.cpp` uses `epmem_wme_adds` and `epmem_node_removals` tables; unchanged WMEs stay in `_now` tables. |
| Automatic store dispatch | Perceive → Remember write path (mechanical) | `episodic_memory.cpp:5443 bool epmem_consider_new_episode(agent* thisAgent)`; with default `trigger=dc`, **unconditionally** sets `new_memory = true` (line ~5483), then calls `epmem_new_episode(thisAgent)` (line 2923). Invoked from `run_soar.cpp:858 epmem_go(thisAgent)` at the `output` phase when `epmem_params->phase == phase_output`. |
| Cue buffer receive (retrieval initiated by agent rule) | Perceive (into epmem) | S1 §7 (C46) — retrieval cue is a partial state specification. Deliberate, not automatic. |
| Recency-biased best match | Filter (ranking) | S1 §7 (C46). |
| Retrieved episode reconstructed in buffer | Remember (read-return) | S1 §7 (C46). |
| Episode store (SQLite-backed, delta-encoded) | Remember (the store itself) | `episodic_memory/episodic_memory.cpp` schema. |
| WME-lifecycle removal bookkeeping (`epmem_node_removals`, `epmem_edge_removals`) | **Not eviction** — part of the delta-encoding write path | `episodic_memory.h:646 epmem_id_removal_map* epmem_node_removals;`. Written at `decision_process/rete.cpp:1552 (*thisAgent->EpMem->epmem_node_removals)[ w->epmem_id ] = true;` inside `_epmem_remove_wme` when a WME is removed from working memory. Consumed at `episodic_memory.cpp:3051–3084` during the next episode encoding: for each entry with `r->second == true`, writes an interval-end row (`delete_epmem_wmes_constant_now`) plus either a point (`add_epmem_wmes_constant_point`) or an RIT interval (`epmem_rit_insert_interval`), then `->clear()` at `:3084`. This closes the temporal interval for a WME that existed from `range_start` to `range_end - 1`. It does **not** evict episodes from the store; it records that a WME's "NOW" status ended at this cycle so that time-range queries over the episodic store return the correct result. |
| **Episode-store eviction path** | blank | No code path removes entries from the episode store itself. `git grep -i "forget\|evict" origin/development -- episodic_memory/episodic_memory.cpp` returns only comments in `_epmem_remove_wme` referring to working-memory-side removal, not episode-store eviction. No `epmem_forget_pq` analog. S1 §7 (C48) describes growth as a characteristic with three existing mitigations: delta encoding, indexing, agent-controlled filtering. |
| **Generalization path (episode → semantic)** | blank | S1 §7 (C49) explicitly defends the absence: *"Episodic learning has often been ignored as a learning method because it does not have generalization mechanisms. However, even without generalization, it supports many important capabilities."* Elicitation Q2 answer: C49 defends the use case but does not architecturally rule out an additional generalization mechanism. |

### SVS sub-pipeline

Not fully covered in this pass. §8 partially read. SVS mediates 3D spatial reasoning and object persistence (C89). Insufficient evidence for a complete sub-pipeline characterization.

---

## Sub-pipelines (Consolidate-level)

### Chunking sub-pipeline (EBBS)

| System term | Role | Evidence |
|---|---|---|
| Substate result creation (trigger) | Perceive (of trace) | S1 §4 (C62): *"Chunking is automatic and is invoked whenever a result is created in a substate."* |
| Historical trace of substate processing | Cache | S1 §4 (C62): *"It analyzes a historical trace of the processing in the substate."* Implementation in `explanation_based_chunking/ebc_explanation_trace.cpp`. |
| Back-tracing through the rule that created the result | Filter (dependency isolation) | S1 §4 (C63). `explanation_based_chunking/ebc_backtrace.cpp:104 void Explanation_Based_Chunker::backtrace_through_instantiation`. Also `backtrace_through_OSK`. |
| Explanation-based generality analysis (EBBS) | Attend (select which conditions / generalizations to keep) | S1 §4 (C64): *"ensures that the resulting rules are correct relative to the reasoning in the substate and as general as possible without being over general."* Implementation in `explanation_based_chunking/ebc_build.cpp`, `ebc_constraints.cpp`, `ebc_variablize.cpp`. |
| New rule written into procedural memory | Remember (write back to parent store) | `ebc_build.cpp` final step; dup detection `ebc_build.cpp:619 excise_production(thisAgent, m_chunk_inst->prod, false, true)`. |
| Chunk-of-a-chunk (meta-learning, fixed-point) | blank | S1 §4 describes chunking as automatic and repeated; no explicit meta-learning cell visible. |
| **Restriction:** chunking does not fire when the substate's own decisions are made using numeric preferences | Blocked Filter input path | S1 §4 p.10 (C67): *"chunking requires that substate decisions be deterministic so that they will always create the same result. Therefore, chunking is not used when decisions are made using numeric preferences."* Laird's direct statement continues: *"We have plans to modify chunking so that such chunks are added to procedural memory when there is sufficient accumulated experience to ensure that they have a high probability of being correct."* |

### RL sub-pipeline

| System term | Role | Evidence |
|---|---|---|
| Operator application event (trigger) | Perceive (of state/operator/outcome tuple) | S1 §5 (C30): *"After an operator applies, all RL rules that created numeric preferences for it are updated based on the reward associated with the state and the expected future reward."* |
| Reward signal on state | Cache (of reward) | Reward WME consumed by update. `reinforcement_learning/reinforcement_learning.cpp` uses `reward_link` / `reward` structures. |
| RL rule match-set for (state, operator) | Filter (selection of rules to update) | S1 §5 (C33): *"the mapping from state and operator to expected reward (the value-function) is represented as collections of relational rules."* |
| Q-learning / SARSA / eligibility trace update rule | Attend (assign credit across the matched set) | `reinforcement_learning.cpp:795 void rl_perform_update(agent* thisAgent, double op_value, bool op_rl, Symbol* goal, bool update_efr)`. Called from `exploration.cpp:670` and `exploration.cpp:679`. S1 §5 fn.5 notes Q-learning + SARSA + eligibility traces supported. |
| Numeric preference update on matched RL rules | Remember (write back to procedural store) | Updates in-place on existing productions' numeric preference RHS. |
| RL across active substates | hierarchical extension | S1 §5 (C35): *"RL in Soar applies to every active substate, with independent rewards and updates for RL rules across the substates."* |
| **Composition direction with chunking**: chunking → RL rule with initial value → RL tuning | cross-Consolidate composition path | S1 §5 p.12 (C34): *"RL rules can be learned by chunking, where the initial value is initialized by the processing in a substate, and then subsequently tuned by the agent's experience and reward."* Also S1 §4 (C66), §9.3 item 3 (C86). |

### Deliberate semantic store sub-pipeline (the current smem write path)

| System term | Role | Evidence |
|---|---|---|
| Agent decision that a fact is worth storing | (agent cognition) | Out of architectural scope — it is the rule's own design. S1 §6 (C42): *"an agent can deliberately store information at any time."* |
| `^store` command written to smem buffer by operator application rule | Perceive (of store request) | `semantic_memory.cpp:480 if (path == cmd_store_new)` branch. |
| Source WMEs collected from topstate under the store symbol | Cache | Same branch; `store` list iteration `for (sym_p = store.begin(); sym_p != store.end(); ++sym_p)`. |
| (no policy deciding whether to accept the store) | Filter = blank | The architecture performs the store unconditionally when the command is present. Any filtering is in the agent's own rules (i.e., upstream of the architectural write). |
| `store_new(...)` / `STM_to_LTM(...)` — transactional write | Remember (write to store) | `smem_store.cpp:597 void SMem_Manager::store_new(...)`; `smem_store.cpp:608 void SMem_Manager::STM_to_LTM(...)`. SQLite transaction management in-line. |

### Episodic snapshot sub-pipeline (the current epmem write path)

| System term | Role | Evidence |
|---|---|---|
| End-of-output-phase trigger | Clock signal | `run_soar.cpp:858 epmem_go(thisAgent)` inside `if (epmem_enabled(thisAgent) && (thisAgent->EpMem->epmem_params->phase->get_value() == epmem_param_container::phase_output))`. |
| `epmem_consider_new_episode` decides whether to encode this cycle | Filter (policy) | `episodic_memory.cpp:5443 bool epmem_consider_new_episode(agent* thisAgent)`. |
| In default `trigger=dc` mode, unconditionally `new_memory = true` | Filter is identity | `episodic_memory.cpp` `if (trigger == epmem_param_container::dc) { new_memory = true; }`. In `trigger=output` mode, only fires if new output-link WMEs appeared. In `trigger=none`, does not fire. |
| `epmem_new_episode` assembles and writes delta | Remember (write) | `episodic_memory.cpp:2923 void epmem_new_episode(agent* thisAgent)`. |
| Agent-controlled filtering of which WMEs enter the snapshot | Filter (agent-level) | S1 §7 (C48): *"An agent can further limit the costs of retrievals by explicitly controlling which aspects of the state are stored, usually ignoring frequently changing low-level sensory data."* Note: this is a rule-level filter in the agent's code, not an architectural Filter cell — the *architecture* still encodes everything in the snapshot-eligible set. |

---

## Tower stack summary

| Role | @ top (decision cycle) | @ Remember (procedural) | @ Remember (semantic) | @ Remember (episodic) | @ Consolidate (chunking) | @ Consolidate (RL) |
|---|---|---|---|---|---|---|
| Perceive | Input phase + buffers | LHS match over WM | `^query`/`^store` cue buffer | `^query` cue buffer + auto topstate snapshot | substate result trigger | operator-apply event |
| Cache | WM + elaboration rules | RETE β-memories | cue buffer staging | delta-encoded `_now` tables | substate trace | reward + state tuple |
| Filter | proposal rules + evaluation rules | refraction / instantiation de-dup | base + spread activation ranking | recency-biased ranking; `epmem_consider_new_episode` trigger policy (identity in `dc` mode) | back-trace through instantiation | RL rule match-set |
| Attend | fixed decision procedure | blank (no ranking among matched rules — all fire) | best-match selection | best-match selection | EBBS generality analysis | `rl_perform_update` credit assignment |
| Remember | application rules + motor + output phase | production store | LTI SQLite store | delta-encoded episode store | new rule into procedural store | numeric pref update on existing productions |
| Consolidate | (impasse → chunking); (RL update); (auto epmem snapshot); (deliberate smem store) | chunking + RL | **deliberate `store_new`; no automatic write path in upstream** | mechanical `epmem_new_episode`; **no generalization; no eviction in upstream** | meta-chunk = blank | no meta-learning-rate store; delta-bar-delta is per-rule α, still driven by a global meta-α |

---

## Cross-source observations

**C45 framework mapping.** The automatic storage in C45 is mechanical snapshotting of WM at the decision boundary. In framework terms, this is a Perceive-to-Remember write path at the substrate level, not a Consolidate operation. The prior intake conflated "automatic storage of snapshots" with "automatic learning from experience into semantic memory."

**C84 cross-source note.** Figure 6's "Existence in Working memory" as smem's source of knowledge is independently confirmed by C42 (deliberate agent-initiated storage) and by code: smem stores graph structures (semantic_memory.cpp), epmem stores WM snapshots as deltas (episodic_memory.cpp). Different stores, different representations, different write paths.

**C88 synthesis.** §9.3 item 6 describes epmem + metareasoning + chunking combined for retrospective analysis. The implied learning path: epmem retrieval (deliberate) → metareasoning in substate → chunking compiles result into rules. Epmem contributes through deliberate retrospective analysis, not automatic consolidation.

**C91 cross-source confirmation.** Laird's meeting rejection (S6, C90–C91) of the unified-graph model is independently confirmed by C84 (Figure 6, §9.2) and by code structure (semantic_memory.cpp vs episodic_memory.cpp). Smem and epmem are structurally distinct stores with different representations, different write paths, and no architectural bridge between them.

---

## S5 code-audit findings: stochastic-substate chunking

*Answers pickup item 3: has Laird's planned "modify chunking to handle stochastic substates" (C67, §4 p.10) been implemented since 2022?*

**P17. Upstream has no implementation.** `origin/development` at `f65f626e4` (2026-03-05, latest upstream commit) contains no code for gating chunking on RL convergence, accumulated experience, or probability-of-correctness thresholds. Grepping for `sufficient.*experience`, `probability.*correct`, `accumulated.*experience`, `stochastic`, `nondeterministic`, `convergence` across `Core/SoarKernel/src/explanation_based_chunking/` returns no matches. The restriction described in C67 remains in place with no upstream mechanism to relax it. EBC commit history 2022-12 through 2025-12 (19 commits on `explanation_based_chunking/`) shows C++17 compatibility cleanup, literalization-test work on the singleton-attribute feature (2025-09-17 series), and a use-after-free refcounting fix (2025-12-31 `3d94c4d87`). No setting for gating chunking on accumulated experience appears in `ebc_settings.h` — the exposed settings are `max_chunks`, `max_dupes`, `bottom_level_only`, `add_OSK`, `add_ltm_links`, `repair_rhs`, `repair_lhs`, `merge`, `user_singletons`, `allow_missing_negative_reasoning`, `allow_opaque_knowledge`. None corresponds to Laird's stated plan.

**P18. Only known attempt is local.** The local branch contains commits `e4ef0c3ed` ("Add RL convergence gate for chunking"), `6833abd6f` and `bd759dbfc` (tests and dedup), all authored by June Kim on 2026-03-24. These implement an EMA-of-|ΔQ| convergence gate. This work is downstream from the prior disputed diagnosis and is not part of upstream Soar.

---

## Ambiguous mappings (resolved or narrowed by elicitation)

**A2. Episodic memory — automatic storage vs deliberate retrieval.** Storage is automatic per C6, C45. Retrieval is deliberate per C28, C46. Write side is Perceive-to-Remember (mechanical snapshot); read side is Remember.

**A3. Procedural memory — store vs learning paths.** The store is Remember; chunking and RL are Consolidate operations. "Procedural memory" is used in both senses across the paper.

**A4. Operator — spans proposal, evaluation, selection, application.** Structural unit, not a single role. Different phases map to Filter, Attend, Remember/Cache.

**A5. Elaboration phase vs elaboration rules.** The phase name covers all rule types firing in parallel. The narrow sense (elaboration rules only) is Cache.

**A6. Impasse as control signal vs Consolidate trigger.** Double duty: control flow branching and chunking trigger.

**A7 [RESOLVED by C66, C67, elicitation Q5].** Chunking–RL composition. §4 restriction and §5 composition claim cover different halves: deterministic substates allow chunking→RL rules (already supported); stochastic substates restrict chunking (C67). Laird's planned fix has not shipped in upstream Soar (P17). PR #577's EMA-of-|ΔQ| criterion is a stability signal; Laird's phrase names a correctness criterion. Direction aligned, criterion weaker. PRs #578–#580 retired per elicitation Q3.

---

## Gap inventory (unclassified)

Restated as a flat list. Classification (expected gap / design choice / blind spot) is reserved for A.md.

- [G1] Semantic memory has no automatic write mechanism in upstream. Laird himself names "semantic learning" as missing (C71). Elicitation: open problem from Laird's perspective.
- [G2] Semantic memory has no eviction mechanism in upstream.
- [G3] Episodic memory has no generalization mechanism; Laird defends as a learning method without generalization (C49). Elicitation: C49 defends the use case without architecturally ruling out an additional mechanism.
- [G4] Episodic memory has no **episode-store eviction** mechanism in upstream; Laird names three existing cost-growth mitigations (C48). **Distinct from** the `epmem_node_removals` / `epmem_edge_removals` machinery at `rete.cpp:1552` → `episodic_memory.cpp:3051–3084`, which is WME-lifecycle delta-encoding bookkeeping, not episode eviction.
- [G5] Procedural memory has no background BLA-driven excision policy in upstream; excision occurs only via CLI or duplicate-justification handling (`rete.cpp:3823, 3975, ebc_build.cpp:619`).
- [G6] Chunking does not fire when the substate's own decisions are numeric-preference-driven; Laird states planned modification (C67). **Verified: planned modification has not shipped to `origin/development` as of commit `f65f626e4` (2026-03-05).** No convergence-gated chunking path and no corresponding flag in `ebc_settings.h`.
- [G7] Among rules matching WM in a single elaboration wave, there is no ranking — all fire. Design per S1 §2.2.
- [G8] No architectural meta-learning-rate store for RL; delta-bar-delta provides per-rule α but is driven by a global meta-α. **Verified.** `reinforcement_learning.cpp:115 meta_learning_rate` (default 0.1, clamped to (0,1] by `btw_predicate`). Per-rule state `prod->rl_delta_bar_delta_beta` and `prod->rl_delta_bar_delta_h` provide the per-rule α adaptation, driven by the global `theta`. Decay modes declared at `reinforcement_learning.h:127 enum decay_choices`.
- [G9] SVS sub-pipeline not fully characterized — §8 partially read.

---

## Deltas from the prior (disputed) diagnosis

| # | Prior claim | Upstream S5 status |
|---|---|---|
| D1 | *"The word 'forget' does not appear anywhere in the semantic memory source."* | **Verified for upstream.** `git grep -i forget origin/development -- Core/SoarKernel/src/semantic_memory/` returns only `smem_activation.cpp:1139`, which is bookkeeping re-use, not a forget mechanism. |
| D2 | *"The source declares removal structures (`epmem_id_removal_map`) but never populates them."* | **Refuted as stated; underlying claim still holds.** The maps **are populated** at `rete.cpp:1552` inside `_epmem_remove_wme` and consumed at `episodic_memory.cpp:3051–3084` for delta-encoding of WME intervals. This is WME-lifecycle bookkeeping, not episode-store eviction. The deeper claim — no episode-store-side eviction — remains true. |
| D3 | *"Chunking can't compose with RL."* | **Refuted as stated.** S1 §5 p.12 (C34) and §4 p.10 (C66) show chunking produces RL rules initialized with numeric preferences that RL subsequently tunes. The composition is partial, not absent. The restriction is the narrower one in C67: chunking does not fire when the *substate's own decisions* are numeric-preference-driven. |
| D4 | *"Semantic learning is missing."* | **Partially verified.** Laird himself lists semantic learning as a still-missing form of architectural learning in §10 item 7 (C71). The narrower factual statement — no automatic mechanism in upstream — is verified. |
| D5 | *"Eviction is the obvious missing piece."* | **Recorded as a prior framing, not a fact.** The code shows no upstream eviction for smem or epmem. PRs #578–#580 retired per elicitation Q3. |
| D6 | PR #577's EMA-of-\|ΔQ\| gating is the right mechanism for Laird's planned modification. | **Recorded as prior judgment.** Direction aligned with Laird's plan; criterion weaker. PR #577 on hold per elicitation Q2. |
| D7 | Soar's gaps trace to a single root cause (missing merging in long-term declarative stores). | **Reserved for A.md.** |

---

## Code-read items

- [P1 RESOLVED] `epmem_id_removal_map` populated? **Yes**, at `rete.cpp:1552`. See D2.
- [P2] SVS sub-pipeline (§8) — requires fuller §8 read. **Not load-bearing for current thesis.**
- [P3 RESOLVED] §9.2 varieties of learning — Figure 6 enumerates five learning systems. No missed Consolidate cells. Image Memory is experimental.
- [P4/P12 RESOLVED] §9.3 combinations of reasoning and learning — eight combination patterns, all with chunking or RL as the learning terminus. C73 (item 5) explicitly names chunking as the terminus of multi-module combinations. C74 (item 6) places chunking as a participant in Mohan 2015's retrospective analysis. No retrieve-time selection of procedural knowledge is presented as an architectural alternative to chunking.
- [P5 RESOLVED] Has Laird's planned modification (C67) shipped? **No.** See P17.
- [P6 RESOLVED] Delta-bar-delta meta-α parameter: **Yes**, `reinforcement_learning.cpp:115`. See G8.
- [P7 RESOLVED] Decision-procedure eight-step sequence verified. `run_preference_semantics` at `decide.cpp:1104`, six named section banners.
- [P8] Whether SVG assets from the prior diagnosis need redrawing. **Still pending.**
- [P9] `_epmem_remove_wme` `= false` case at `episodic_memory.cpp:2909`. Low priority.
- [P10] EBC `mechanism_merge` setting — whether this is a Consolidate-of-Consolidate cell. Low priority.

---

## Additional evidence: experimental-branch comment in the kernel

During P14 (slower-than-decision-cycle scheduler grep), `git grep -n "consolidation\|VACUUM\|vacuum\|offline\|background_task\|maintenance" origin/development -- Core/SoarKernel/src/` returned a non-library match at `debug_code/debug.h:9`:

> *"(Not much here now. Will move some other utility stuff from experimental chunking and memory consolidation branches later.)"*

The kernel's own comment references *"experimental chunking and memory consolidation branches"* — a first-party note that work on chunking variants and memory consolidation was done on experimental branches that have not landed in mainline `origin/development`. The comment is inside `debug_code/`, a low-stability area, suggesting the direction was not load-bearing for the mainline development path. This is a code-level observation about what the maintainers have and have not chosen to merge.
