# June Kim

Vancouver, Canada · june@june.kim · www.june.kim · 604 356 1191 · github.com/kimjune01

## Summary

Research engineer for agent evaluation and environments. I turn ambiguous questions about coding-agent behavior into reproducible experiments, graders, datasets, and production systems. My benchmark audits ship as preregistered, re-runnable artifacts with public repositories and DOIs. I bring 10+ years of software engineering at Google, Loom, and startups, plus 100 merged pull requests across 81 external repositories in 2026 (GitHub search, July 26).

## Selected Research & Systems Work

### Independent Research Engineer — Agent Evaluation & Coding Benchmarks

2026 — present

- SWE-bench Pro determinacy audit: audited all 728 tasks and established a pointer-checkable 15% underdetermination floor; three gold patches fail the benchmark's own verifier. Preregistered, DOI-archived, and filed with the maintainers.
- Reproducible evaluation harness: ran all 728 SWE-bench Pro tasks under the official grader; froze every prediction and verdict in committed artifacts so any result can be independently regraded.
- ProgramBench construct-validity audit: showed that “% Resolved” partly measures recall of published algorithms rather than source-blind reconstruction; filed the evidence with the authors for right of reply.
- Built `determinacy`, a reusable auditor for tracing benchmark claims to the evidence available to an agent; applied it to SWE-rebench and SWE-bench Pro.

## Work Experience

### Independent Contractor

Applied AI Engineer  
2025 — 2026

- Anyteam.com: Designed and shipped an accessibility data pipeline for the Sales OS and a browser-extension web scraper to ingest and retrieve domain knowledge.
- Buildbetter.ai: Built third-party integrations (Circle.so, Notion, Front, Attio) with incremental sync, OAuth2, and deduplication, and an LLM field-classification system that maps import columns with confidence scoring.
- Shipped CI/CD quality gates, E2E test infrastructure, and reusable developer tooling (Claude Code skills for log querying, migration gen, CI failure analysis).

### Little Bird Software

Applied AI Engineer  
2024 — 2025

- Designed agentic data ingestion pipelines using LLM-based condensation (Claude, GPT-4, Gemini Flash) and deduplication to cut noise 90%, improving retrieval accuracy and chat grounding.
- Architected macOS and Chrome integrations (Swift, Tauri, Rust) over Accessibility APIs for real-time context injection, and core Python backend services for prompt orchestration and dedup with zero-downtime migrations.

### Loom

Senior Software Engineer  
2022 — 2023

- Raised core video reliability from 97% to 99.7% via multiresolution UI and Shaka Player interfacing; led a full TypeScript refactor of the Electron desktop app.

### YouTube / Google

Software Engineer  
2019 — 2022

- Re-architected the YouTube iOS app's rendering layer (C++ / TypeScript), cutting UI deployment cycles from months to days.
- Directed the launch of a Premium sign-up framework, a 2% conversion lift across 50M+ users.

### Earlier Experience

Software Engineer  
2013 — 2019

- iOS / mobile: Firework (patented video-view tech), Lipsi (#1 Lifestyle, US App Store, 2.3M users), and others.

## Independent Research & Open Source

### Published Research

2026

- The Hypothesis Graph, Verifiable Knowledge, and What Cannot Be False Cannot Be True: DOI-archived preprints with reproducible artifacts; full record and code at june.kim.
- Tested whether adversarial review loops improve test-passing LLM code from 43% to 91% merge-readiness; evaluated the workflow against real maintainer decisions.
- Methodology in public: a 22-question preregistration checklist, a published null result, and a post-mortem of a $1,000 mistake caused by held-out-test leakage.

### Open Source Software

2026

- Enzyme autodiff compiler: a proof-by-cases soundness gate reproduced two compiler bugs from structure alone (filed upstream); separately landed two autodiff fixes (merged).
- Representative merged fixes: godotengine/godot, hyperium/hyper, envoyproxy/envoy, servo/servo, pingcap/tidb, EnzymeAD/Enzyme, flux-rs/flux, wild-linker/wild.

## Education

### Bachelor of Science (2nd degree)

Simon Fraser University, Canada  
2015—2017

- Second degree in computing, after a prior business degree; focused on machine learning, systems, algorithms, databases, security, and computer vision.

### Bachelor of Business Administration

Simon Fraser University, Canada  
2008—2012

- Business administration degree focused on product, operations, strategy, finance, and entrepreneurship.

## Skills

- Evaluation: benchmark auditing, construct validity, LLM evaluation, red-teaming, evaluation harness design, data contamination / decontamination, ground-truth and label-quality audits, preregistration, reproducible artifacts
- AI/ML: agentic workflows, tool use / function calling, RAG, embeddings, vector databases, Model Context Protocol (MCP), Claude Code
- Languages: Python, Rust, TypeScript, C/C++, Go, Swift
- Infrastructure: FastAPI, CI/CD, Git/GitHub
