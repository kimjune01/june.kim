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

**Fit after reading:** Strong. BetterBench explicitly places in-depth construct-validity analysis beyond its scope, so the audit series addresses an open layer rather than competing with the checklist.

### Junlin Wang

**Work:** First author of [Automated Benchmark Auditing for AI Agents and Large Language Models](https://arxiv.org/abs/2605.26079), which uses an agentic system to detect instruction, environment, and evaluation defects across a large benchmark corpus.

**Contact:** `junlin.wang2@duke.edu` ([Duke profile](https://scholars.duke.edu/person/junlin.wang2)).

**Intersection:** We independently arrived at benchmark auditing through complementary methods. Their work offers automated breadth; mine emphasizes exhaustive artifact reads, executable witnesses, lower-bound claims, symmetric validity gates, and an auditor's own error ledger.

**What might interest him:** My audits are an unusually rich external validation set for automated auditing. Each finding has a receipt, often an upstream response, and sometimes a documented false-positive history. Comparing systems could measure which failure classes automation detects, misses, or invents. My contract also includes construct, frame, decay, and run-level failures that a task-level instruction/environment/evaluation schema may flatten.

**What I would gain:** Scale, a way to test the portability of the audit methods, and direct comparison with the closest parallel research program.

**Good first exchange:** Blindly run the automated auditor on one of my completed corpora, then compare its findings against the preregistered or receipt-backed audit record.

**Boundary:** My work should not become merely a validation dataset for automated auditing. The comparison should allow the manual method to falsify the automated schema and vice versa.

**Fit after reading:** Strong for one methods collaboration. ABA already inspects artifacts, uses trajectory evidence, publishes structured records, and measures precision. The genuine contribution is a controlled corpus with symmetric gates and credible clean cases, not “receipts” in general.

### Sean McGregor

**Work:** Lead author of [BenchRisk](https://arxiv.org/abs/2510.21460), a taxonomy of benchmark failure modes and mitigations with a public [registry](https://github.com/BenchRisk/BenchRisk).

**Contact:** `computer23@seanbmcgregor.com` (public research address). An older organizational address is `sean@incidentdatabase.ai`.

**Intersection:** My checklist already reconciles its contract clauses against BenchRisk. Several executable-agent failures are absent or only adjacent: underdetermined hidden tests, failing answer keys, self-capturing goldens, unavailable environmental frames, miscomputed denominators, and claim/construct equivocation by benchmark producers.

**What might interest him:** The audits supply new registry entries with concrete witnesses and proposed mitigations. They also expose interactions between mitigations: isolating a grader may protect oracle integrity while destroying the state needed to audit the frame. That suggests BenchRisk may need relationships among failure modes, not only a flat inventory.

**What I would gain:** A durable home and shared vocabulary for findings, experience turning individual defects into general failure modes, and connections to the broader benchmark-risk community.

**Good first exchange:** Submit one well-supported agentic failure mode and ask whether the contract's clause-interaction model addresses a gap in the registry.

**Boundary:** The taxonomy should receive findings from the audits rather than determine what the audits are allowed to notice.

**Fit after reading:** Very strong. BenchRisk leaves simulator-based benchmarks to future work and explicitly relies on author representations without requiring evidence. Executable agent audits test both open choices directly.

### Joel Becker

**Work:** Researcher at METR working on AI capability measurement, developer-productivity experiments, time horizons, and whether benchmark-passing software changes survive contact with real development. [Research profile](https://joel-becker.com/).

**Contact:** `joel@metr.org` ([published on his site](https://joel-becker.com/)).

**Intersection:** My FrontierCode audit measured the gap between a patch grader marketed as mergeability and the reasons maintainers actually close pull requests. It proposes ecological accuracy: agreement between a benchmark verdict and a field outcome. Joel's work addresses the same benchmark-to-field gap from the deployment side.

**What might interest him:** I have a coded population of real maintainer closures and a general method for decomposing where a proxy loses the claimed construct. The result offers a mechanism behind the benchmark/productivity gap: benchmarks can accurately score a narrow artifact while omitting the interaction and judgment that decide outcomes in the field.

**What I would gain:** Stronger field-validation design, better treatment of selection and external validity, and criticism from someone measuring real developer outcomes rather than only benchmark internals.

**Good first exchange:** Compare the FrontierCode ecological-accuracy proposal with METR's mergeability and productivity work, focusing on where the operational definitions disagree.

**Boundary:** My program is not primarily capability forecasting. Field validation is one contract test, not the organizing purpose of every audit.

**Fit after reading:** Strong but narrow. METR measures hypothetical maintainer review with actual maintainers and calibrates reviewer noise against golden patches. My corpus observes actual closures and codes whether the deciding cause was visible in the patch. The datasets cover consecutive validity losses.

### Maria Eriksson

**Work:** Research Fellow at the European Centre for Algorithmic Transparency and collaborator on research about the epistemics, stakeholders, infrastructure, and policy of GenAI evaluation. She coauthored [Can We Trust AI Benchmarks?](https://arxiv.org/abs/2502.06559), an interdisciplinary review of benchmark problems. [Profile](https://www.mariaeriksson.net/about-me/).

**Contact:** `maria.eriksson@ec.europa.eu` (corresponding-author address in her benchmark review).

**Intersection:** Her work asks how evaluations acquire authority and how technical infrastructure, institutional interests, and policy uses shape what benchmark numbers mean. My audits show the artifact-level mechanisms through which that authority outruns the evidence.

**What might interest her:** The audit receipts connect abstract concerns about construct validity, incentives, and opacity to inspectable technical mechanisms. Right-of-reply records and conflict disclosures also provide material for studying how benchmark producers respond when public claims are challenged.

**What I would gain:** A vocabulary for institutional authority, stakeholder incentives, and the politics of evaluation; help distinguishing technical invalidity from legitimate disagreement about what ought to be measured.

**Good first exchange:** Ask her to critique the claim that rerunnable receipts solve an epistemic problem, including what social or institutional problems they leave untouched.

**Boundary:** The technical audits should not dissolve into discourse analysis. Their executable findings remain evidence with independent force.

**Fit after reading:** Good for conceptual exchange and networking, weaker for a direct methods collaboration. The review calls for alternatives to quantitative benchmarks but deliberately surveys systemic critique rather than auditing individual instruments.

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

**Subject:** BetterBench criterion 2 against three audited benchmarks

Hi Anka,

BetterBench leaves construct validity to deeper domain analysis.

I ran that analysis on MirrorCode. Its paper describes the task clearly, but the live reference oracle changes autonomous creation into reimplementation: https://june.kim/auditing-mirrorcode

Would BetterBench still count criterion 2 as fulfilled?

June

### Junlin Wang

**Subject:** Can ABA predict Terminal-Bench mutation outcomes?

Hi Junlin,

ABA recovered 66.7 percent of Terminal-Bench 2's maintainer fixes.

I tested a different defect on Terminal-Bench 2.1. All 83 graders accepted deletion of off-task assets, while 26 caught deletion inside their workspaces: https://june.kim/terminal-bench-frame

Would ABA classify the off-task result as an evaluation-quality defect?

June

### Sean McGregor

**Subject:** An evidence field for BenchRisk mitigations

Hi Sean,

BenchRisk accepts a benchmark author's statement that a mitigation exists.

Frontier-Bench says tasks must enforce preservation. But its runner destroys the state needed to check it, and nine witnessed deletions still received reward 1: https://june.kim/auditing-frontier-bench

Would BenchRisk count that rubric clause as a mitigation?

June

### Joel Becker

**Subject:** Cross-coding two sets of maintainer decisions

Hi Joel,

Your study had four maintainers review 296 agent patches.

I coded 98 actual closure threads. In 52 of 59 confident cases, the deciding cause sat outside the patch: https://june.kim/auditing-frontiercode

Do your review labels separate patch defects from process, identity, and repository state?

June

### Maria Eriksson

**Subject:** Is a public claim audit still a benchmark?

Hi Maria,

Your review says benchmarks cannot provide assurance alone and points to red-teaming and bug bounties.

I audit benchmark claims using fixed falsifiers. I published a 15 percent determinacy floor for SWE-bench Pro before OpenAI later reported problems with the same benchmark: https://june.kim/a-determinacy-audit-of-swebench-pro

Is that an alternative evaluation, or another benchmark layer?

June
