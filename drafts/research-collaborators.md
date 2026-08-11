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

**Subject:** Documented construct vs validated construct

Hi Anka,

BetterBench came up while I was comparing my audit checklist with published ways of evaluating benchmarks. I was struck by where it leaves construct validity to deeper domain analysis.

My MirrorCode audit shows why that layer matters. The paper describes its task clearly, but the live reference oracle changes autonomous creation into reimplementation: https://june.kim/auditing-mirrorcode

Should BetterBench separate a documented construct translation from a validated one?

I'm building an auditing agent. BetterBench's lifecycle criteria seem like a strong checklist for what it should verify before it ever runs a task.

June

### Junlin Wang

**Subject:** Are you still developing ABA?

Hi Junlin,

While looking for other audits of Terminal-Bench, ABA was the closest work I found to what I am trying to automate. Its ability to recover defects that maintainers later fixed stood out to me.

I've been turning my own audits into a cost-ordered checklist for an auditing agent: https://june.kim/how-to-audit-a-benchmark. One angle is frame damage: an agent can finish a Terminal-Bench task, delete unrelated user assets, and still receive full credit.

Are you still developing ABA? If so, do any of these checks fit what you want it to catch next?

I'm building in the same direction and would be happy to share the cases and receipts behind the checklist if useful.

June

### Sean McGregor

**Subject:** Declared vs demonstrated mitigations

Hi Sean,

I came across BenchRisk while mapping failures from my audits into existing registries. Its decision to accept an author's statement that a mitigation exists caught my attention.

Frontier-Bench declares a preservation requirement, but its runner destroys the state needed to enforce it. The mitigation exists in the rubric. The verdict never checks it: https://june.kim/auditing-frontier-bench

Should BenchRisk distinguish declared mitigations from demonstrated ones?

I'm building an auditing agent, and I want it to test whether each claimed mitigation actually works.

June

### Joel Becker

**Subject:** What does "read every line" establish?

Hi Joel,

I found your developer-productivity work while looking at how benchmark performance translates into real work. The finding that 75% of participants read every line of AI-generated code stuck with me.

My SlopCodeBench audit made me wonder what "read every line" actually guarantees: https://june.kim/auditing-slopcodebench. If AI review is faster because it applies a weaker quality bar than human review, the speed comparison is hard to interpret.

Have you thought about how to establish quality parity before measuring speed or output?

I'm building an auditing agent and trying to define the gate it should clear before its output can count as a productivity gain.

June

### Maria Eriksson

**Subject:** Can public audits provide benchmark assurance?

Hi Maria,

I found your review while looking for work that connects benchmark defects to epistemology and policy. Its move from benchmarks toward red-teaming and bug bounties caught my attention.

I audited SWE-bench Pro before OpenAI raised its own concerns. The audit found hidden tests grading choices the public task never specified: https://june.kim/a-determinacy-audit-of-swebench-pro

Can adversarial public audits supply part of the missing assurance, or do they remain another benchmark layer?

I'm building an auditing agent. I want to know what its findings would need to show before they could count toward the assurance your review says benchmarks cannot supply alone.

June
