# Sourcegraph — Agent Engineer [IC4], Code Understanding team

Greenhouse: https://job-boards.greenhouse.io/sourcegraph91/jobs/6103567004?gh_src=0572f98b4us

Form facts: Vancouver, Canada. Remote NA, EST overlap fine from Pacific (their bar is 20h/week overlap; state it). Comp: posted IC4 Zone 2 base is $176k USD; answer "per your published Zone 2 band" rather than a number. No visa sponsorship needed (Canadian, staying in Canada).

---

## Q1. Experience aligning with role requirements

I have ten years of software engineering at Google/YouTube, Loom, and startups, and the last two years building and evaluating agent systems. In 2026 I built and operated an agentic open-source contribution pipeline (issue triage, patch generation, adversarial review, PR submission) with a 53% merge rate across real maintainer review, and I ran an independent evaluation program that audited ten coding-agent benchmarks, published as a method checklist at june.kim/how-to-audit-a-benchmark. The findings were filed upstream as issues and PRs, some merged. That combination, production engineering plus evaluation that survives contact with maintainers, is what I understand this role to be.

## Q2. Coding agent experience and opinions

Coding agents are my daily tooling and my research subject. I run Claude Code as the primary driver with GPT and Gemini as adversarial reviewers in a volley loop, and I've built the harness layer around them: skills for triage, QA, and review, plus a semantic memory design published as a preprint (june.kim/the-hypothesis-graph-semantic-memory-methodeutics).

The opinion I hold most firmly: agents are only as good as the verification around them. An agent's internal green light is a stop signal allowed to lie; the harness's oracle decides, and most failures I've measured are harness failures (oracle leakage, unguarded side effects, graders that check the wrong thing), documented across ten benchmark audits. This is why I want to work on the context and verification layer rather than the model layer. Cross-repo context is the binding constraint on enterprise agent reliability, and that's your product.

## Q3. Multi-step agentic systems (designed and shipped?)

Yes. The contribution pipeline above is a multi-stage agentic system I designed, built, and operated: repo triage fans out to per-issue investigation, patches go through an adversarial QA volley (two independent model families reviewing until convergence), and a pacing layer manages PR submission and maintainer feedback. I instrumented outcomes end to end: merge rate, review latency, rejection modes. At Little Bird Software I shipped production agentic ingestion pipelines with LLM condensation and deduplication that cut noise 90% for chat grounding.

## Q4. Production software services

Yes. At YouTube I directed the launch of a Premium sign-up framework serving 50M+ users with a 2% conversion lift. At Loom I took core video infrastructure from 97% to 99.7% reliability. At Little Bird I ran backend service migrations with zero user downtime.

## Q5. ML model building, evaluation, operation

Evaluation is where I'm strongest, and I can show receipts. I audited ten coding-agent benchmarks in eleven passes (SWE-bench Verified as a runner, DeepSWE twice, SWE-bench Pro, Terminal-Bench, τ-bench, and others), finding answer keys that fail their own graders, underdetermined specs, and graders that score destructive runs as passes. Every finding is a rerunnable receipt, and the method is published as a checklist (june.kim/how-to-audit-a-benchmark). In production settings I've built LLM eval harnesses for field-classification systems with confidence scoring, and model-selection comparisons across Claude, GPT, and Gemini for ingestion pipelines.

I have not fine-tuned models at production scale; my model work is selection, prompting, and evaluation rather than training.

## Q6. Why this role and company

Sourcegraph is building the layer I keep concluding matters: the context and verification infrastructure that makes agent work on large codebases trustworthy. My research program for the past year has been exactly this question (auditable agent systems, verifiable claims, evaluation that means what it says), pursued independently with preprints and upstream fixes. The JD line about determining when metrics genuinely validate improvements is the job I've been doing without the title. I want to do it where the evals gate a product that engineering teams actually run.

## Q7. How you heard

HN Who is Hiring, August 2026.

---

## Notes (not for the form)

- Resume gap for this role: the benchmark audit campaign isn't on the PDF. Add one line under Selected Research & Systems Work, e.g. "How to Audit a Benchmark (July 2026): audited ten agentic coding benchmarks in eleven passes; findings filed upstream (BenchRisk#8, Terminal-Bench, DeepSWE); method published as a checklist."
- Stack honesty: JD lists Go, TypeScript, GraphQL, PostgreSQL, Docker. You have TS/Postgres/Docker in production; Go is thin. Don't address it unless asked in interview; the answer there is the Rust/Swift/C++ track record showing language acquisition isn't the risk.
- Cover letter is optional; skip it. The essay answers carry everything a letter would.
- LinkedIn is a required field.
