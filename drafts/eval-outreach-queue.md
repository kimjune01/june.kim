# Eval outreach queue

Built 2026-07-23 from live research. ~30 named people across ~20 orgs that hire or contract coding/agentic-eval work. Worked in warmth order: threads you already have, then best-fit cold-but-specific, then frontier labs.

## How to work this
- **Warm first.** The top tier is people you've already corresponded with via a filed audit. That's not cold outreach, it's replying where you've shown value.
- **Reach the person, not the portal.** For most of these there's a named human who owns the eval problem; a note to them beats the ATS.
- **Two live-check chores before any send:** (1) X handles couldn't be machine-verified (fetchers were blocked) — eyeball the profile first; (2) role links are on JS portals that rotate — click through before citing a req.
- **The note:** their work first, one artifact of yours that's relevant to *their* benchmark, one low-activation ask (a conversation or a contract, not "hire me"). Use the `email` skill.
- **Geography filter:** you're Remote / North America. Some of the best-fit roles are on-site (METR Berkeley, Vals SF, AISI London + UK clearance). For those, lead with the contract framing, not the W2 one.

---

## Tier 1 — warm threads (send this week)

**Scale AI / SWE-bench Pro** — your flagship audit, their flagship benchmark, and they're hiring eval engineers *right now*.
- Thread: `scaleapi/SWE-bench_Pro-os` (you filed here). Corresponding author to @-mention: **Jeff Da** (GitHub `jeff-da`).
- Also current: **Brad Kenstler** (X `@Bckenstler`, LinkedIn) leads agents research, author on SWE-bench Pro + SWE-Atlas. Reachable on X/LinkedIn; no verified email.
- Live SEAL roles: AI Research Engineer – Enterprise Evaluations, Tech Lead – LLM Evals, SEAL RS/RE (scale.com/careers, labs.scale.com/jobs).
- ⚠ Post-Meta-exodus staleness: do NOT contact Summer Yue, Sean Hendryx, Zifan Wang as Scale — all at Meta now.

**Terminal-Bench / harbor** — warm via your own harbor#2266 campaign. ✅ ALREADY CONTACTED — you sent Merrill + Shaw the TB 2.1 grader audit Jul 9 2026. This is follow-up territory, not a first send.
- Maintainer: **Alex Shaw** (GitHub `alexgshaw`, Laude; email `alexgshaw64@gmail.com`) — de-facto lead. Also **Mike Merrill** (`TheMikeMerrill` / `mchlmerrill@gmail.com`), now at Anthropic (see Tier 3).
- Repos: `harbor-framework/terminal-bench`, `harbor-framework/harbor` (moved from `laude-institute/*` — your old thread survives via redirect).

**ProgramBench + SWE-bench** — one thread spans two benchmarks. ✅ ALREADY CONTACTED — ProgramBench audit emailed to Yang + Lieret + Diyi Yang Jul 2 2026; John Yang also got your SWE-bench Verified result May 24 (`johnby@stanford.edu`). Follow-up, not first send.
- **John Yang** (email `johnby@meta.com`, GitHub `john-b-yang`, X `@jyangballin`) + **Kilian Lieret** (`klieret@meta.com`) are corresponding authors on ProgramBench, which you filed, and core SWE-bench people. Both now at Meta.
- ⚠ Verify Lieret still triages SWE-bench before routing SWE-bench mail there (affiliation flipped Princeton→Meta).

**SWE-rebench (Nebius)** — lower priority; no individual reach verified. File/reply on `SWE-rebench/SWE-rebench-V2` issues.
- ⚠ The `SWE-bench-fork` README lists `carlosej@`/`johnby@` — inherited boilerplate, NOT the Nebius maintainers. Don't route SWE-rebench mail there.

**DeepSWE** — ⚠ confirm which one you audited before contacting anyone:
- Agentica/Together *model* (harness = rLLM; `agentica-project/rllm`; Michael Luo `michaelzhiluo`), vs.
- the unrelated datacurve *benchmark* (`datacurve-ai/deep-swe`).

---

## Tier 2 — best fit, cold but specific (this week / next)

**Epoch AI — likely the single best org-fit on the list.** They have a job that is literally construct-validity auditing. ✅ ALREADY DEEP IN IT — you applied to Benchmark Reviews, interviewed with Greg Burnham (Jul 16), did the MirrorCode audit work-test, sent it Jul 18 + forwarded to Tom/David Rein/Florian, followed up Jul 19. Reads as stalled ("seems like I'm not getting the job"). NOT a cold target — this is a revive-or-close conversation, and given it's your best fit, worth handling deliberately.
- **Tom Adamczewski** — started Epoch's benchmark-eng team, sole byline on their SWE-bench Docker registry + MirrorCode. Email `tadamczewskipublic@gmail.com` (self-published), X `@tmkadamcz`, GitHub `tadamcz`. **Primary target.**
- **Greg Burnham** — owns the "Are AI benchmarks doomed?" methodology debate. Email `greg@epoch.ai`, X `@GregHBurnham`.
- Open role: **Researcher, Benchmark Reviews** — "develop critiques and assessments of AI benchmarks." Also SWE-Benchmarking, Researcher-Evaluations.

**AISI + Inspect / Meridian Labs** — framework-level; native to you (file a GitHub issue on `inspect_evals`).
- **JJ Allaire** — creator of Inspect, now Meridian. X `@fly_upside_down`, GitHub `jjallaire`.
- **Alexandra Abbas** — led `inspect_evals` (the benchmark-content repo, most construct-validity-relevant). GitHub `alexandraabbas`.
- Open role: SWE, Core Technology (London, needs UK clearance — likely out for you as a role; the framework relationship still matters).

**METR** — autonomy evals; migrated their harness onto Inspect (cite Inspect fluency).
- **Megan Kinniment** — "leads the benchmark creation effort." X `@MKinniment`, LinkedIn.
- **Thomas Kwa** — time-horizon lead author, posts eval-methodology critiques. X `@Kwathomas0`.
- Open role: MTS, Evaluation Execution ($285K–503K, **Berkeley on-site**, work-test-heavy). No public emails — X/LinkedIn.

**Vals AI** — independent third-party benchmarking; Vibe Code Bench is their coding surface.
- **Hung Tran** — first author, Vibe Code Bench. `hung@vals.ai`. Lead technical target.
- **Langston Nashold** — co-founder/CTO. `langston@vals.ai`. **Rayan Krishnan** — CEO, `rayan@vals.ai`, X `@RayanKrishnan` (best for the hiring conversation).
- Open role: MTS – Research (SF in-person).

**Arena (ex-LMArena)** — rebranded 2026-01-28, arena.ai; Code Arena / WebDev Arena are the coding surfaces.
- **Aryan Vichare** — built WebDev/Code Arena. X `@aryanvichare10`, GitHub `aryanvichare`. Best target.
- **Evan Frick** — eval methodology (Arena-Hard). X `@evan_a_frick`.
- Open role: ML Scientist, Open Source Lead ("reproducible benchmarks, new methodology").
- ⚠ A different "Arena Intelligence" (manufacturing) appears on job boards — verify a posting mentions human-preference/leaderboard.

---

## Tier 3 — frontier lab eval teams (cold, named person)

**OpenAI** — their frontier-evals team authored SWE-bench Verified and then *publicly retired it as contaminated*, which is your exact Verified finding. Strong opener: you reached the same conclusion independently.
- **Tejal Patwardhan** — leads the frontier evals team. X `@tejalpatwardhan`.
- **Wedge (verified from your own sent mail):** you published a SWE-bench Pro audit that *predates* OpenAI's "separating signal from noise" coding-eval blog post. You reached their team's public conclusion before they published it. Lead with that.
- Open role: Research Engineer, Frontier Evals & Environments (+ Backend SWE-Evals, RE Post-Training Evals).
- Mia Glaese (VP) — too senior for a cold IC note.

**Anthropic** — ownership spread across Model Evals / Agent Prompts & Evals / Evals Infra.
- **Mike Merrill** (also Tier 1 via Terminal-Bench) — building evals at Anthropic. `mchlmerrill@gmail.com`, X `@Mike_A_Merrill`. Top pick.
- **Gian Segato** — authored a 2026 agentic-coding-eval post. X `@giansegato`.
- Open roles: Evals Infrastructure Tech Lead/Manager (posted ~today, Python/Rust), EM Agent Prompts & Evals, RE Model Evaluations.

**Meta AI (FAIR CodeGen)** — SWE-RL, CWM (65.8% SWE-bench Verified).
- **Sida Wang** — cleanest contact, `sidawxyz@gmail.com`, GitHub `sidaw`. SWE-RL/CWM co-author.
- **Gabriel Synnaeve** — senior, leads RL & CodeGen. X `@syhw`.
- (John Yang + Kilian Lieret from Tier 1 are also here now.)

**Mistral** — Devstral; has an eval-titled role open.
- **Kush Jain** — Research Scientist, ML-for-SWE focus. `kdjain@andrew.cmu.edu`, X `@Kush_D_Jain`, GitHub `kjain14`.
- Open role: Applied AI, Evaluation Engineer (Lever).

**Cohere** — Code Agents team; North Mini Code.
- **Dennis Aumiller** — owns internal agentic-coding benchmarks. `dennis.aumiller+website@gmail.com`, GitHub `dennlinger`.
- Open roles: Senior RS Model Evaluation; MTS Data Analysis & Evaluation.

**Google DeepMind** — org in flux (a 2026 coding "strike team" with departures — verify current employer before sending).
- **Danny Tarlow** — "lead of Code AI efforts." X `@dtarlow2`, email via daniel.tarlow.org.
- **Nicholas Kang** — agentic-evals-at-scale talk. LinkedIn.
- Open roles: RE – SSI Coding Agents ("automated evaluation pipelines beyond lab benchmarks"), Senior Staff RE – Agent Evals & Quality.

**xAI** — no named eval owner verified. Role + org handle only: MTS – Model Evaluation (greenhouse), X `@xai`.

---

## Suggested first five sends (revised after Gmail check — dropped the ones already in flight)
1. **OpenAI / Tejal Patwardhan** — you audited SWE-bench Pro before their own team published the same finding. Strongest untouched wedge.
2. **Scale / Jeff Da** — warm GitHub thread + live SEAL roles + your flagship audit, all one org. Not yet emailed.
3. **METR / Megan Kinniment** — leads benchmark creation; live Evaluation Execution role. Cold, strong fit.
4. **Vals / Hung Tran** (`hung@vals.ai`) — first author Vibe Code Bench; only a LinkedIn alert so far, never contacted.
5. **AISI-Meridian / Alexandra Abbas** — file an `inspect_evals` issue; framework-native, no cold email needed.

Note: Epoch, Terminal-Bench (Merrill/Shaw), and Meta (Yang/Lieret) are already contacted — see the ✅ flags above. Epoch is a revive-or-close, not a fresh send.

## Standing flags
- X handles unverified by machine — spot-check each before sending.
- Role links rotate on JS portals — click through live.
- Verified self-published emails (highest trust): Adamczewski, Merrill, Sida Wang, Kush Jain, Aumiller, plus the `@vals.ai` and `@epoch.ai` addresses.
- No verified cold email for METR, AISI, Scale, Arena people — use X/LinkedIn/GitHub there.
- Several best-fit roles are on-site (METR Berkeley, Vals SF, AISI London+clearance) — lead with contract framing for those.
