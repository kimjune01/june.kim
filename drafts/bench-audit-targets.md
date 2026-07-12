# Next audit targets — runner-first

Re-based 2026-07-10. The customer is the bench **runner** (frontier labs + evals shops), so
targets are ranked by service to a runner, not by how auditable a benchmark is. The old
version scored O/Ow/H/L (oracle / owner / harness / leaderboard); that optimizes "easy to
audit," which is how it surfaced WorkArena. WorkArena shipped ([#155](https://github.com/ServiceNow/WorkArena/issues/155),
draft PR [#156](https://github.com/ServiceNow/WorkArena/pull/156)) and was then shelved: no
frontier lab reports against it, so a merged fix changes nothing anyone reads. See
[[bench-audit-target-selection]].

**The pitch reframe.** Not "I audit benchmark datasets." It's *"I add runner-enforced validity
contracts at the state, scorer, and answer-key boundaries."* The deliverable is a harness
primitive, and the benchmarks are the receipts that prove it catches real defects.

*Provenance: landscape verified by codex (GPT-5.5) against 2026 model cards and the GitHub API,
2026-07-10. Independently confirmed the Gemini 3.5 Flash card (Terminal-Bench 2.1 + SWE-bench
Pro + MCP Atlas + Toolathlon + OSWorld-Verified, no Verified). OpenAI's SWE-bench-Verified
retirement page blocks automated fetch; treat specific card versions as of the search date and
spot-check any number before an outreach cites it.*

## Ranked targets

| rank | target | status | why it ranks | first deliverable |
|---:|---|---|---|---|
| 1 | **Inspect** (UK AISI, `UKGovernmentBEIS/inspect_ai`) | fresh | Convergence point: AISI runs it, METR is migrating to it, Epoch's platform is built on it, 200+ packaged evals. One accepted primitive touches many heterogeneous evals. Highest leverage in the portfolio. | validation API for eval authors (oracle exec, scorer determinism/totality, answer-key integrity) |
| 2 | **Harbor** (`harbor-framework/harbor`) | in progress | Terminal-Bench 2.x is the nearest-universal agentic coding bench (4/4 labs ex-Meta); Harbor is becoming a general agent runner. State boundary is clean. Already engaged (frame_gate, harbor#2266). | finish and upstream the frame/state-diff gate as a generic task contract |
| 3 | **τ²-bench** (`sierra-research/tau2-bench`) | fresh clause | Successor to the τ-bench you already audited (contamination). Different clause: nominal task success coexists with unauthorized DB/policy-state mutations, which is the frame gap, not decay. Broad cross-lab tool-use reporting. | end-state invariants, mutation ledger, counterfactual policy tests (Telecom/Retail) |
| 4 | **WebArena-Verified / OSWorld-Verified** | fresh | Stateful agent environments labs report against (Anthropic web, OpenAI computer-use). The frame clause bites hardest here, and neither is in your covered set. Oracle construction is the open risk. | pre-agent state manifest, off-task delta gate, gold-trajectory replay |
| 5 | **Inspect Cyber / Cybench** integration | fresh | Direct input to AISI and Anthropic safety decisions; cyber tasks carry acute answer-key, reachability, determinacy, collateral-state risks. Landing it through Inspect beats auditing Cybench alone. | environment preflight, exploit-reachability/oracle runner, reset validation, forbidden-side-effect assertions |

Short version: **Inspect first; finish Harbor; then τ²-bench (frame), a computer-use env, and Inspect-native cyber.** SWE-bench Pro and τ-bench are already covered (below), so they are receipts to cite, not targets to open.

## Already covered (don't re-open as targets)

Cite these as the receipts behind the pitch; do not list them as fresh.

- **SWE-bench Verified** — run as a runner (retired by OpenAI Feb 2026; historical).
- **SWE-bench Pro** — [determinacy audit](/a-determinacy-audit-of-swebench-pro) (15% floor) + [runner piece](/how-not-to-run-swebench-pro). Spec and runner sides done; only a distinct new clause would be fresh, and Pro's frame is already SWE-bench's PASS_TO_PASS.
- **τ-bench** — [contamination reprice](/reprice-contamination) (decay clause). τ²-bench above is the fresh-clause extension, not a re-do.
- **DeepSWE / DeepSWE v1.1** — gold + determinacy. **ProgramBench** — oracle/recall. **Terminal-Bench** — frame ([the template](/terminal-bench-frame)).

## Harness assessment (the load-bearing part)

The harness beats the benchmark repo as a fix-home, because one primitive covers every eval on it,
and the runner orgs are staffed to want correctness. GitHub API, 2026-07-10:

| harness | activity | external merges | verdict |
|---|---|---|---|
| **Inspect** (`inspect_ai`) | pushed today; 2.3k stars, 594 forks, 225 open issues; continuous releases | 78 recent merged PRs, many from non-maintainer CONTRIBUTORs | best fresh target |
| **Harbor** | pushed today; 3.1k stars, 1.3k forks, 487 open issues | 71 recent merged, community-oriented | best clean state-integrity target, already covered |
| METR `task-standard` | last substantive push 2025-02; a spec/interchange layer, not the executor | dormant | do not target alone |
| METR `vivaria` | maintained for existing users, new work winding down; METR recommends Inspect | — | drop as a fresh target |
| Epoch "rig" | built on Inspect + Inspect Evals | — | fold into Inspect |

### Inspect contribution shape (don't lead with a monolithic frame gate)

Inspect supports many sandbox types whose permitted mutations are intentionally broad, so a global
filesystem gate in core would not merge. The mergeable sequence:

1. **Validation API for eval authors**: reference-solution/oracle execution; scorer totality and
   determinism checks; repeated-grading consistency; dataset/sample-ID and answer-key integrity;
   explicit required/forbidden artifacts.
2. **Opt-in sandbox state assertion**: capture selected paths/commands before and after, normalize
   volatile state, specify allowed/required/forbidden changes, attach the diff and policy result to
   the eval log.
3. **CLI/CI preflight** that runs those checks over an Inspect task without a full model run.

This maps to Inspect's extensibility model and doesn't require AISI to endorse one definition of
"frame condition."

## What the labs actually report (agentic, late-2025/2026)

No agentic benchmark is 5-lab universal; Meta has no current serious agentic suite.

- **OpenAI** (GPT-5.4): Terminal-Bench 2.0, SWE-bench Pro, BrowseComp, τ²-bench, MCP Atlas, Toolathlon, OSWorld-Verified, MLE-Bench Revised, SWE-Lancer. Retired SWE-bench Verified.
- **Anthropic**: Terminal-Bench 2.0, SWE-bench (Verified/Pro/Multilingual/Multimodal), τ²-style, WebArena/WebArena-Verified, BrowseComp, Cybench, CyberGym, LAB-Bench. Broadest cards, esp. cyber + browser + science.
- **Google DeepMind** (Gemini 3.5 Flash): Terminal-Bench 2.1, SWE-bench Pro, MCP Atlas, Toolathlon, OSWorld-Verified, Finance Agent v2.
- **xAI** (Grok 4.5): Terminal-Bench 2.1, SWE-bench Pro, DeepSWE, τ²-bench Telecom, cyber incl. Cybench.
- **Meta**: no comparable agentic-eval card (Llama 4, Apr 2025); maintains CyberSecEval separately.

Cross-lab center of gravity: **Terminal-Bench 2.x (4/4), SWE-bench Pro (4/4), τ²-bench (3-4/4)**.

## Secondary lane: answer-key / tool-augmented QA

Good answer-key and contamination targets, but not stateful agent environments, so they exercise a
different primitive (answer-key runner, contamination reprice) than the frame gate:

- **BrowseComp** — heavily reported, strong contamination/answer-key surface; benchmark-specific audit, less leverage than Inspect.
- **FrontierMath** (Epoch) — answer-key/contamination, but private-item access constrains independent auditing; Epoch already on Inspect.
- **GPQA / AIME / HLE / SimpleQA** — answer-key/contamination lane, not agentic.

## Deferred, with reasons

- **MCP Atlas** — rising fast; enters the top five if its runner becomes a shared externally-maintained harness.
- **MLE-Bench Revised** — good construct fit, but mostly OpenAI-reported and costly.
- **RE-Bench / METR long-horizon** — high consequence, narrow use, expensive GPU validation.
