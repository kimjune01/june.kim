# Prior art: coding-agent scaffolds vs the externalized abductive comparator

*Research note for "The Hypothesis Graph" §right-regime / related-work. Compiled 2026-06-18 from a deep-research pass (5 angles, 15 sources fetched, 25 claims 3-0 adversarially verified, 0 killed) plus a codex prior-art search. All primary sources are arXiv. Time-sensitive: 2025–2026 landscape.*

## The question

Does any published system externalize an **abductive diagnosis step** — a set-difference (XOR) against an external golden the model cannot author — as a runtime tool call, such that a weaker model with it exceeds a stronger model without it on code diagnosis? I.e., is the paper's narrow novelty real?

## Verdict

**The comparator gap is unoccupied.** Established scaffolds externalize *actions, retrieval, pipeline, or tests* — diagnosis stays inline in the model. No system externalizes the diagnosis step against a hidden golden. The two real "weaker beats stronger" upsets are both **automation**, not capability, and both **one tier within a family**. The two-tier capability lift, isolated by ablation, has no public precedent found.

## Established scaffolds (architecture gradient; diagnosis inline)

- **Agentless** ([arXiv:2407.01489](https://arxiv.org/abs/2407.01489)) — fixed non-agentic 3-phase pipeline (localize → repair → validate). No autonomous tools, no runtime golden.
- **OpenHands** ([arXiv:2407.16741](https://arxiv.org/abs/2407.16741)) — event-stream / CodeAct, Docker sandbox. Externalizes *actions*.
- **AutoCodeRover** ([arXiv:2404.05427](https://arxiv.org/abs/2404.05427)) — search agent; the "proxy LLM" only JSON-ifies tool choices. Externalizes *tool selection*.
- None use a golden patch at runtime or externalize a diagnosis comparator.

## Scaffold-vs-model confound

- **SWE-Effi** ([arXiv:2509.09853](https://arxiv.org/abs/2509.09853)) — effectiveness emerges from *synergy* with the base LLM (e.g., SWE-Agent 21.8% with Qwen3-32B vs 5.1% with GPT-4o-mini). AutoCodeRover+Qwen3-32B 38% > OpenHands 34% > SWE-Agent 28% on the *same* model = scaffold-vs-scaffold, **not** a model upset.
- Scaffold-taxonomy paper ([arXiv:2604.03515](https://arxiv.org/abs/2604.03515), future-dated id, verified against its repo) — prior studies confound scaffold and model via different pairings.

## The two real "weaker + scaffold beats stronger" upsets — both automation

- **GradleFixer / AndroidBuildBench** ([arXiv:2510.08640](https://arxiv.org/abs/2510.08640)) — Gemini-2.5-**Flash** + GradleFixer beats **Pro** + shell agent. 81.4% pass@1; at 30 calls/task 74.0% vs 54.3% (Gemini), 59.6% vs 41.5% (GPT). **How it lifts:** domain-specific *execution primitives* ("Tool Bridging") for Gradle/Android builds — better-shaped actions, not reasoning. One generation, same family. *Caveat: within-Gemini, self-reported.*
- **Confucius Code Agent (CCA)** ([arXiv:2512.10398](https://arxiv.org/abs/2512.10398), Meta + Harvard) — Sonnet 4.5 + CCA 52.7% beats Opus 4.5 + Anthropic proprietary 52.0% on SWE-Bench-Pro. **But Opus 4.5 + CCA = 54.3%** — the upset *reverses* once the stronger model gets the same scaffold. **How it lifts:** externalized *notes* (memory/context management for large codebases). So it's a **scaffold effect**, not a capability crossing. One tier, same family. *Caveat: Opus 52.0 from Anthropic system card.*

## Golden-comparator near-neighbor

- **SWT-Bench** ([arXiv:2406.12952](https://arxiv.org/abs/2406.12952)) — grades *generated tests* by fail-on-original / pass-after-golden-patch. Same external-golden shape, but used as an **evaluation oracle for test generation**, not a runtime instrument a repair agent hill-climbs against with the answer key hidden. (Adding SWT-Bench-style tests roughly doubles SWE-Agent test precision.)
- **SWE-Bench Pro** ([arXiv:2509.16941](https://arxiv.org/abs/2509.16941)) grades fail2pass + pass2pass via a shared SWE-Agent scaffold; diagnosis is post-hoc LLM-as-judge.

## Implications for the paper

1. **Narrow novelty holds, query-backed:** no system externalizes the abductive comparator (hidden external-golden set-difference) as a runtime diagnosis tool. Cite GradleFixer, Confucius, SWT-Bench and distinguish.
2. **Two axes separate us cleanly:** *automation vs capability* (theirs are throughput/tractability; ours is a frontier extension) and *actions/notes/tests vs reasoning* (theirs externalize the former; ours externalizes the diagnosis).
3. **Confucius is the foil, not the threat.** Its upset reverses under scaffold control — a confounded whole-scaffold swap. Ours is isolated by the §right-regime ablation (hold model/loop/bug/graph fixed, vary only the verdict source), so it does **not** reverse when the stronger model is handed the same harness. Frame the claim as *the comparator's lift* (magnitude spans two tiers), never as a Sonnet>Fable model ranking.
4. **The crossings are one-tier; ours is two.** GradleFixer (Flash↔Pro) and Confucius (Sonnet↔Opus) are one tier within a family. Sonnet 4.6 → Fable spans two tiers, with no public precedent found — "first public demonstration of a lift that wide" is defensible (existence-grade, n=1).

## Provenance

Deep-research workflow run `wf_2861d7cf-a41`; codex prior-art search (web). Stats: 70 claims extracted, 25 verified, 25 confirmed, 0 killed.
