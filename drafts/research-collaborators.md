# Research collaborators

## Why I am looking

I am building an independent research program around the epistemology of AI evaluation. Its empirical base is eleven audit passes across ten executable AI-agent benchmarks. Each audit follows the evidence from a benchmark's public claim through task selection, specification, oracle, executable gold, environmental frame, score, contamination, and reported run. The method produces rerunnable receipts and bounded findings rather than general suspicions.

I am looking for collaborators and an intellectual network, not an employer, funder, or director. The aim is to find people with whom one precise exchange could become a stronger method, a joint experiment, a paper, an introduction, or an ongoing critical conversation. I do not want to subordinate the work to an existing benchmark-quality framework. The useful collaborations are ones in which the approaches remain distinct enough to test each other.

## What I bring

- Eleven hands-on audit passes across ten benchmarks, including SWE-bench Verified, DeepSWE, SWE-bench Pro, ProgramBench, τ-bench, Terminal-Bench, MirrorCode, FrontierCode, Frontier-Bench, and SlopCodeBench.
- A benchmark-contract model connecting **claim → selection → specification → oracle → gold → frame → score → decay → run**.
- Re-executable methods for testing gold correctness, determinacy, grader coverage, environmental destruction, contamination resistance, construct validity, and verdict provenance.
- Findings that existing benchmark-quality catalogues do not fully represent: golds that fail their own graders, hidden tests that pin unstated choices, self-capturing oracles, graders blind to destructive side effects, and mitigations that improve one contract clause by weakening another.
- A broader epistemology of receipts, falsifiers, evidence trajectories, and verifiable knowledge that explains why rerunnability matters beyond software benchmarks.

## People

### Anka Reuel

**Work:** Lead author of [BetterBench](https://arxiv.org/abs/2411.12990). Her research develops measurement-theoretic and psychometric foundations for AI evaluation and asks when evaluation results justify capability or risk claims. [Research profile](https://ankareuel.com/research).

**Contact:** `anka@cs.stanford.edu` ([published on her site](https://ankareuel.com/)).

**Intersection:** BetterBench addresses benchmark quality across the evaluation lifecycle. My work supplies a more operational account for executable agent benchmarks: inspect the actual grader, run the gold, mutate the environment, retrieve the verdict receipt, and test whether the scored construct matches the advertised one.

**What might interest her:** The audits provide concrete cases where lifecycle best practices are satisfied while the measurement still fails, or where a technically sound mitigation transfers validity loss into a neighboring clause. They could test whether BetterBench's criteria predict defects found under execution and reveal criteria needed specifically for stateful agent benchmarks.

**What I would gain:** Measurement language, stronger construct-validity arguments, disciplined corpus design, and criticism of whether the contract clauses are independent and operationally codable.

**Good first exchange:** Compare the contract against BetterBench on two or three audited benchmarks and identify disagreements rather than forcing a merged framework.

**Boundary:** The audits should not become another checklist application. Their distinctive contribution is adversarial execution with receipts.

### Junlin Wang

**Work:** First author of [Automated Benchmark Auditing for AI Agents and Large Language Models](https://arxiv.org/abs/2605.26079), which uses an agentic system to detect instruction, environment, and evaluation defects across a large benchmark corpus.

**Contact:** `junlin.wang2@duke.edu` ([Duke profile](https://scholars.duke.edu/person/junlin.wang2)).

**Intersection:** We independently arrived at benchmark auditing through complementary methods. Their work offers automated breadth; mine emphasizes exhaustive artifact reads, executable witnesses, lower-bound claims, symmetric validity gates, and an auditor's own error ledger.

**What might interest him:** My audits are an unusually rich external validation set for automated auditing. Each finding has a receipt, often an upstream response, and sometimes a documented false-positive history. Comparing systems could measure which failure classes automation detects, misses, or invents. My contract also includes construct, frame, decay, and run-level failures that a task-level instruction/environment/evaluation schema may flatten.

**What I would gain:** Scale, a way to test the portability of the audit methods, and direct comparison with the closest parallel research program.

**Good first exchange:** Blindly run the automated auditor on one of my completed corpora, then compare its findings against the preregistered or receipt-backed audit record.

**Boundary:** My work should not become merely a validation dataset for automated auditing. The comparison should allow the manual method to falsify the automated schema and vice versa.

### Sean McGregor

**Work:** Lead author of [BenchRisk](https://arxiv.org/abs/2510.21460), a taxonomy of benchmark failure modes and mitigations with a public [registry](https://github.com/BenchRisk/BenchRisk).

**Contact:** `computer23@seanbmcgregor.com` (public research address). An older organizational address is `sean@incidentdatabase.ai`.

**Intersection:** My checklist already reconciles its contract clauses against BenchRisk. Several executable-agent failures are absent or only adjacent: underdetermined hidden tests, failing answer keys, self-capturing goldens, unavailable environmental frames, miscomputed denominators, and claim/construct equivocation by benchmark producers.

**What might interest him:** The audits supply new registry entries with concrete witnesses and proposed mitigations. They also expose interactions between mitigations: isolating a grader may protect oracle integrity while destroying the state needed to audit the frame. That suggests BenchRisk may need relationships among failure modes, not only a flat inventory.

**What I would gain:** A durable home and shared vocabulary for findings, experience turning individual defects into general failure modes, and connections to the broader benchmark-risk community.

**Good first exchange:** Submit one well-supported agentic failure mode and ask whether the contract's clause-interaction model addresses a gap in the registry.

**Boundary:** The taxonomy should receive findings from the audits rather than determine what the audits are allowed to notice.

### Joel Becker

**Work:** Researcher at METR working on AI capability measurement, developer-productivity experiments, time horizons, and whether benchmark-passing software changes survive contact with real development. [Research profile](https://joel-becker.com/).

**Contact:** `joel@metr.org` ([published on his site](https://joel-becker.com/)).

**Intersection:** My FrontierCode audit measured the gap between a patch grader marketed as mergeability and the reasons maintainers actually close pull requests. It proposes ecological accuracy: agreement between a benchmark verdict and a field outcome. Joel's work addresses the same benchmark-to-field gap from the deployment side.

**What might interest him:** I have a coded population of real maintainer closures and a general method for decomposing where a proxy loses the claimed construct. The result offers a mechanism behind the benchmark/productivity gap: benchmarks can accurately score a narrow artifact while omitting the interaction and judgment that decide outcomes in the field.

**What I would gain:** Stronger field-validation design, better treatment of selection and external validity, and criticism from someone measuring real developer outcomes rather than only benchmark internals.

**Good first exchange:** Compare the FrontierCode ecological-accuracy proposal with METR's mergeability and productivity work, focusing on where the operational definitions disagree.

**Boundary:** My program is not primarily capability forecasting. Field validation is one contract test, not the organizing purpose of every audit.

### Maria Eriksson

**Work:** Research Fellow at the European Centre for Algorithmic Transparency and collaborator on research about the epistemics, stakeholders, infrastructure, and policy of GenAI evaluation. She coauthored [Can We Trust AI Benchmarks?](https://arxiv.org/abs/2502.06559), an interdisciplinary review of benchmark problems. [Profile](https://www.mariaeriksson.net/about-me/).

**Contact:** `maria.eriksson@ec.europa.eu` (corresponding-author address in her benchmark review).

**Intersection:** Her work asks how evaluations acquire authority and how technical infrastructure, institutional interests, and policy uses shape what benchmark numbers mean. My audits show the artifact-level mechanisms through which that authority outruns the evidence.

**What might interest her:** The audit receipts connect abstract concerns about construct validity, incentives, and opacity to inspectable technical mechanisms. Right-of-reply records and conflict disclosures also provide material for studying how benchmark producers respond when public claims are challenged.

**What I would gain:** A vocabulary for institutional authority, stakeholder incentives, and the politics of evaluation; help distinguishing technical invalidity from legitimate disagreement about what ought to be measured.

**Good first exchange:** Ask her to critique the claim that rerunnable receipts solve an epistemic problem, including what social or institutional problems they leave untouched.

**Boundary:** The technical audits should not dissolve into discourse analysis. Their executable findings remain evidence with independent force.

## Missing collaborators

The current list is strongest in AI evaluation and weakest in empirical software engineering. A particularly valuable collaborator would combine:

- artifact evaluation and replication-study experience;
- software testing, hidden-oracle, and benchmark-validity expertise;
- measurement or philosophy-of-science literacy;
- comfort with adversarial negative results;
- interest in methods that can return empty rather than always finding a defect.

This person might be a better recurring collaborator than a prominent AI-evaluation researcher because they could strengthen the audit machinery without trying to make it serve a model leaderboard, governance program, or automated-auditing product.

## Outreach principle

Do not ask anyone to endorse or join the whole program. Lead with one disagreement, artifact, or experiment where both approaches could change. A useful first conversation should have a possible outcome in which my framework is wrong.

The recurring question is:

> What can we test together that neither approach can settle alone?

## Outreach drafts

### Anka Reuel

**Subject:** Testing BetterBench's fulfillment scores

Hi Anka,

BetterBench's scoring distinguishes a benchmark that mentions a practice from one that fulfills it. That is more useful than a disclosure checklist.

Your assessments necessarily read the evidence benchmark developers publish. My MirrorCode audit tested what happens when the practice exists but its evidence cannot settle the claim. MirrorCode ran a memorization screen, but the released data omit the join needed to measure how memorization affected its headline score: https://june.kim/auditing-mirrorcode

Would you be open to a 20-minute call about using executable audits to calibrate BetterBench's distinction between partial and full fulfillment?

June

### Junlin Wang

**Subject:** A blind validation set for ABA

Hi Junlin,

ABA's standardized schema and external validation across 168 benchmarks provide breadth my manual audits do not have.

I audited Terminal-Bench 2.1 by mutating its passing gold solutions. All 83 tested tasks still passed after off-task assets were deleted. The corpus preserves each execution witness, including apparent findings that a symmetric validity gate voided: https://june.kim/terminal-bench-frame

Would you be open to a 20-minute call about a blind comparison that scores ABA on confirmed findings, confirmed non-findings, and auditor false positives?

June

### Sean McGregor

**Subject:** When one BenchRisk mitigation creates another risk

Hi Sean,

BenchRisk gives individual benchmark failures a durable vocabulary and a mitigation path. My audits had neither before I reconciled them against your registry.

The scoring model treats mitigations as reducing risk. My Frontier-Bench audit found a signed interaction. Destroying the agent container protects the reward from tampering, but it also erases the state needed to detect destructive behavior: https://june.kim/auditing-frontier-bench

Would you be open to a 20-minute call about representing mitigation side effects as edges between BenchRisk failure modes?

June

### Joel Becker

**Subject:** Two losses between a grader and a merged PR

Hi Joel,

Your maintainer study measures the loss between an automated grader and code review. The golden-patch baseline also measures reviewer noise, which my work does not.

My FrontierCode audit measures the next loss between code review and the field outcome. In 52 of 59 confidently coded maintainer closures, the deciding cause sat outside the patch. Together the studies separate grader-to-review validity from review-to-field validity: https://june.kim/auditing-frontiercode

Would you be open to a 20-minute call about testing that two-stage decomposition on the two datasets?

June

### Maria Eriksson

**Subject:** An executable test for benchmark epistemics

Hi Maria,

Your review shows that benchmark problems are interconnected and that benchmarks shape the capabilities they appear merely to measure. That institutional account reaches farther than my technical audits.

I have an operational object for one edge of that account. My SWE-bench Pro audit found a 15 percent lower bound of tasks whose public materials do not determine what their hidden tests grade. Each verdict carries the artifact that would refute it: https://june.kim/a-determinacy-audit-of-swebench-pro

Would you be open to a 20-minute call about whether executable falsifiers can connect benchmark critique to an assurance practice without reducing the institutional problem to a technical one?

June
