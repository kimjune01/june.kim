---
variant: post-medium
title: "Internal Reasoning of Prose Compiler"
tags: coding, methodology, projects, pageleft
---

Two pipelines, one compiler. Sweep takes a natural-language issue and emits a pull request with embedded receipts. Immune takes that pull request and emits a verdict that the maintainer reads in thirty seconds. Together they compile intent to commit. The hypothesis graph is the IR. The only human gate is the maintainer's merge.

I wrote [(Issue) → PR](/issue-to-pr) about the contributor half, and [(PR) → merged](/pr-to-merged) about the maintainer half. This post is what they are together.

### Two pipelines, mirrored

Each pipeline runs the same six-stage shape (perceive, cache, filter, attend, transmit, consolidate), one instance of [the Natural Framework's](/the-natural-framework) substrate. The mirroring:

| Stage | Sweep (contributor) | Immune (maintainer) |
|-------|---------------------|---------------------|
| Perceive | Scan repos for actionable issues | Receive PR webhook |
| Cache | Inbox actors, attestation chain | Labels on PR, GitHub metadata |
| Filter | AI-policy + body-count + saturation | Duplicate + reputation + policy |
| Attend | Hypothesis graph + adversarial volley | Replay test + LLM synthesis |
| Transmit | PR with embedded receipts | Verdict label the maintainer sees |
| Consolidate | Retro pager → parameter updates | Retro on the maintainer's merge corpus |

Sweep's transmit feeds immune's perceive. Both pipelines run on independent infrastructure (the contributor's machine and the maintainer's CI runner), communicating only through the artifacts GitHub already carries: PRs, labels, comments.

### HG is the IR

Compilers got better when [LLVM](https://llvm.org/) gave them a typed intermediate representation. The IR for sweep + immune is the hypothesis graph: prose-shaped so a human can audit it, graph-shaped so a machine can traverse it. Nodes are perturbations, edges are evidence trajectories, leaves carry e-value classifications with provenance back to the artifact each claim came from.

Sweep's attend stage produces one. Immune's perceive reads one. The maintainer skims one. Same artifact crosses three boundaries without lossy re-encoding. Attestation rows quote into it; PR bodies render from it; the retro pager folds against it.

The title holds only where the work is perturbable. Bug-fixing qualifies: the test suite is an oracle the loop reads each cycle, so recon abduces, craft acts, audit prunes. Feature-level UX does not. You cannot perturb human taste and read the verdict in-loop, so it cannot live in a hypothesis graph, and this compiler does not reach for it. The HG is the IR for the perturbable subset, and silent outside it.

The competitors ([Devin](https://cognition.ai/blog/introducing-devin), [Copilot Enterprise](https://github.com/features/copilot/plans), [Codium](https://www.qodo.ai/), [Greptile](https://www.greptile.com/)) fail this signature, as far as their public surfaces show. They pass opaque verdicts across the boundary: a vector embedding, a confidence score, a "trust us" paragraph. The maintainer has to take the system's word for the work or replay it by hand. There is no shared schema for what crosses. You need a typed IR to have a compiler. Without one you have a recommender with a UI.

That choice is expensive. Embeddings are cheaper than HGs; opaque verdicts are easier to produce than legible ones with cited substrates. The payoff is that every step is auditable. Maintainers verify before merging. Contributors debug before pushing. Nothing in the pipeline is un-quoted; the IR itself is the proof. Sweep and immune don't need a [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) backend or a hosted vector store, because the HG plus GitHub labels and markdown is sufficient state.

### One human gate

The maintainer's merge decision. One human choice with consequences; everything else automated. Thirty seconds of synthesis replaces twenty minutes of diff. That frees the maintainer for what machines can't do: architectural taste, project priorities, maintainer-relationship tone, the social work of code review.

The gate's position is the design's claim. Earlier (reviewing every receipt) wastes attention on machine-mechanical work. Later (post-merge auditing) creates the wrong incentives, because the merge already happened. The merge button is right because it's where commitment crystallizes.

### Two reasoners, one artifact

Before pushing, sweep runs codex + gemini volley. On receipt, immune runs replay-test + LLM synthesis. Two independent reasoners on the same artifact, plus mechanical gates (CI on both sides). A bug that fools sweep's cascade still has to fool immune's synthesis to reach the maintainer.

The redundancy is structural. Sweep's reviewers see the diff against the contributor's hypothesis graph; immune's reasoner sees it against the maintainer's own merge corpus. Different priors, different gates. A misbehaving contributor pipeline (a forked or compromised sweep) gets caught by the maintainer pipeline whose taste came from the maintainer's own repo.

### Distributed by construction

No central coordinator. Sweep runs wherever the contributor wants: local laptop, hosted instance, self-hosted box. Immune runs in the maintainer's CI runner. GitHub is the transport. The PR + the labels are the handshake. Swap operators without touching the spec; the spec is the prose contract between sweep's transmit and immune's perceive.

Forks are network nodes. Every sweep clone someone runs, every CI workflow that includes immune, is another node in the same distributed compiler. On every node, retro learnings feed upstream parameters. The architecture is the moat; the code is the public good.

### The economics

Both pipelines are [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html) (code) and [CC-BY-SA-NS](/cc-by-sa-ns) (prose). Network-services copyleft on both halves closes the SaaS-loophole that has killed prior maintainer-side filtering attempts: take the open code, wrap it as SaaS, capture the contributor base, never publish back.

The operator running a hosted instance funds it by accepting tips (BYO-credentials tier) and charging consultant rates (concierge tier, where the operator personally shepherds PRs). Credence buyers (customers who want a clean contribution graph without doing the engineering work) pay concierge rates because the alternative is hiring an engineer. Their fees fund the operator's time on the BYO-credentials tier, which everyone else uses for free. *Credence economy funds meritocracy economy.*

I'm the operator and a user. My own bugs flow through the same pipeline as everyone else's. That's the structural validation: if the system stops working for my own use, I notice first.

### What "contributor" means now

Once the compiler works, labor restratifies. The same shift hit assembly when it dropped from "the only way to program" to "what the compiler emits."

**Compiler authors.** The operator class. They maintain sweep, tune immune's gates, debug the retro loop. Few in number, high in leverage.

**Intent filers.** They describe what should be done in the repo's language. The product-manager class. Many in number, upstream of code.

**Janitors.** They handle what the compiler can't: social work with maintainers, edge cases that don't fit the IR, repos where the compiler is unwelcome.

Before the compiler existed, the "open source contributor" credential conflated all three. With the compiler, the label deflates to janitorial-by-default. Credence buyers paying for PRs in their name are buying a depreciating asset; as the compiler matures, the market reprices the credential. The work has always been janitorial in volume and compiler-authoring in leverage. The framing is catching up.

### The frontend

Today, the compiler requires you to speak its instruction set: GitHub accounts, [gh CLI](https://cli.github.com/), knowing how to file structured issues and read PR diffs. That is a programming skill, just at a different layer than C. A web frontend (not built yet; this section is the spec) would collapse the requirement to the universal skills: clear prose and reasonable judgment.

<img src="/assets/compiler-from-intent-to-commit.svg" alt="Web frontend on top, splits into Sweep and Immune, both connect to the GitHub bus at the bottom" />

Two surfaces, both web, both copyleft. The **filer surface** is the issue-writing UI: a prose box that coaches the writer into hypothesis-graph shape without making them learn the format. *What did you try? What failed? What would you expect to happen instead?* The output is a structured issue posted to GitHub on the user's behalf, with the original prose preserved verbatim alongside the structured fields. The job is to lower the bar for filing a *useful* issue.

The **reviewer surface** is the PR-judging UI. The user sees immune's synthesis paragraph, the test result, the hypothesis graph, and a button row: *merge / changes-needed / close*. They never see the diff unless they click for it. The job is to present a fix at the level of *does the reasoning sound right, does the test capture the bug, does the maintainer's likely position feel respected.* That's reasoning-tracing: a real skill, just not a coding one.

The architecture admits this surface for free. The IR is prose end-to-end. The frontend renders the same hypothesis graph a maintainer reads, with the same information density, in a UI tuned for a non-developer's attention span.

The political claim, plainly: credence buyers fund the compute, and the operator decides where the compute points. Aim it at concierge PRs and you get clean contribution graphs for the wealthy. Aim it at frontend users with real bugs they can describe and you get OSS bug-fixes shipped by people who couldn't have shipped them before. Same compute, different beneficiaries. Who gets routed where is the operator's policy lever; the architecture doesn't care. *Power to the prose writers and the reasoning tracers.* Prose-writing and reasoning-tracing are taught in every secondary school; software engineering is not.

### Future work

**Past the perturbable subset.** The HG is an IR only where an in-loop oracle exists. Bug-fixing has one; UX, design, and taste-level features do not, so they can't be perturbed and read inside the loop. Compiling them is the open problem: it needs a representation that carries intent no test can score, and a verdict that today only a human can give. Until then the honest edge of this compiler is the perturbable, and it stops there on purpose.

**The frontend.** The filer and reviewer surfaces above are a spec, not a build.

### What it isn't

Not a SaaS. Not AGI. Not a replacement for maintainers. A compiler.

Compilers don't replace programmers. They shift the level at which programmers work. The intent filer describes; the maintainer decides whether the produced artifact belongs. Between them, the work is automated, doubled, legible.

### Reference implementations

- [sweep](https://github.com/kimjune01/sweep) (AGPL-3.0) — contributor-side pipeline. 47 merges this month against 167 open; 55% of the PRs that *get reviewed* merge.
- [immune](https://github.com/kimjune01/immune) (AGPL-3.0) — maintainer-side pipeline. Drop into `.github/workflows/`.
- [The Natural Framework](/the-natural-framework) — the six-role substrate both pipelines instantiate.
- [(Issue) → PR](/issue-to-pr) — sweep's design rationale.
- [(PR) → merged](/pr-to-merged) — immune's design rationale.
- [Chewy TUI](/chewy-tui) — the operator dashboard for sweep.

Intent in, commits out. I'm running the prototype on my own bugs and yours. The scaffolding will rot; the compiler is the shape.
