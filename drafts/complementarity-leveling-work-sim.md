# Complementarity, leveling, and compressed work simulation

Working notes. These are hypotheses and design constraints, not yet a finished argument.

## Goal

- Build a technical and organizational assessment agent that produces comparable, auditable evidence of capability from AI-mediated work.
- The eventual controlled form places a candidate in a simulated work environment for a one- to two-hour take-home. The nearer-term wedge may extract receipts from technical interviews, take-homes, coding-agent transcripts, and work artifacts that organizations already produce.
- The candidate should do compressed but recognizable work, not answer questions about how they would hypothetically behave.
- The environment should elicit generative contributions: framing the objective, choosing an economical scope, defining deliverables, delegating execution, and creating receipts that establish when the work is done.
- The result should be a task-conditioned profile of technical and organizational judgment, supported at the lowest level by replayable boolean receipts.
- It should not claim to infer a career level or general job performance from one short session. Its practical aim is to produce better, more inspectable hiring evidence within a realistic assessment budget.

### Product constraints

- **Duration:** approximately one to two hours of candidate time, with asynchronous agent execution excluded where practical.
- **Format:** take-home case-based work simulation in a disposable technical environment.
- **Interaction:** open generation rather than a menu of preferred interventions.
- **Compression:** skip routine execution time while preserving consequential decision boundaries.
- **Evidence:** retain the candidate's scopes, prompts, decisions, artifacts, definitions of done, generated checks, and outcome receipts.
- **Scoring:** test generated contracts against gold, defective, excessive, and valid-alternative outcomes; do not score presentation style or resemblance to a canonical process.
- **Report:** return a narrow profile with its observed opportunities, receipts, uncertainty, and limits—not a composite personality score or unsupported hire/no-hire verdict.

## Durable thesis

- Recruiting automation and candidate capability are orthogonal.
- Sourcing agents and synthetic interviewers automate recruiter labor. They do not necessarily improve what the organization can know about a candidate.
- Technical interviews, work samples, portfolios, references, and historical work already try to produce capability evidence. AI disrupts their attribution and cost structure; it does not create the underlying measurement problem.
- As long as agents are used at work, employers have reason to distinguish people who direct them effectively from people who merely perform the vocabulary of agent use.
- Trainability does not make current capability irrelevant to selection. Hiring trades off current capability, learning rate, onboarding cost, supervision capacity, time to productivity, and failure risk.
- The buyer-facing question is: **How much trustworthy work can this person produce with agents today, and how much supervision will they consume?**
- A useful assessment separates:
  - demonstrated capability;
  - performative fluency without consequential receipts;
  - learning response after informative feedback;
  - required support and controls;
  - verified output per unit of human attention.

## Current market direction

- The immediate trend is from observing unaided performance toward instrumenting AI-mediated work.
- Emerging formats permit or require AI, use real or multi-file codebases, capture the interaction trace, emphasize review/debugging/system design/scoping, and add a short walkthrough or defense to recover ownership.
- The market is splitting between controlling AI through supervised/proctored work and observing AI use through instrumented live sessions or take-homes.
- Take-homes are not necessarily disappearing. A polished repository alone is losing credibility; the likely stronger package is **take-home + agent trace + executable checks + short defense**.
- Young products already advertise real codebases, candidate AI use, trace capture, and automated technical-judgment rubrics. This validates that the category is forming, not that its measurement problems are solved.
- The open question is whether traces feed another impressionistic "AI fluency" score or preregistered, receipt-backed evidence of specific contributions.

## Automation should target the environment

- The useful assessment agent automates the environment in which capability becomes observable:
  - stage work situations;
  - execute delegated actions;
  - advance simulated time;
  - reveal consequences;
  - preserve evidence;
  - run candidate-generated receipts.
- The candidate supplies the capability under examination. The assessment agent supplies repeatability, compression, and observability.
- **Interview agents automate the assessor. Assessment agents automate the world in which capability becomes observable.**

## The bridge

- The HR perspective works downward: role -> required skills and levels -> evidence.
- The technical perspective works upward: boolean receipts -> observed contribution -> capability profile -> hiring decision.
- A defensible assessment needs the two chains to meet.
- The HR transcript calls the problem **evidence fog**: more polished applications and more process do not necessarily produce better hiring evidence.
- SFIA supplies vocabulary for skills and levels, but not the lowest-level measurement substrate.
- The complementarity test supplies that substrate: falsifiable observations of what the human changed in a composed human-agent system.
- Structure can standardize evidence collection while the final rating remains mostly gestalt. The failure chain is often: behavior -> interviewer interpretation -> rubric label -> committee interpretation -> rank.
- A stronger chain is: controlled opportunity -> candidate action -> executable consequence -> literal receipt -> capability profile.
- A value is not yet a construct, and a construct is not yet an assessment. Elastic labels such as "Googliness" can bundle collaboration, humility, initiative, ambiguity tolerance, ethics, and cultural conformity without specifying falsifiable observations.
- Values may guide situation design, but the assessment should grade narrow consequences rather than the value label itself.

## The human contribution should be generative

- Multiple choice is the wrong core interaction if it supplies the candidate with the intervention space they should generate.
- The candidate should generate the frame, hypotheses, scope, constraints, definition of done, and verification topology.
- The system or agent can execute the proposed action and compress the waiting and implementation time.
- Core loop: **open generation -> simulated execution -> observable consequence -> boolean receipt**.
- A conventional case asks for a persuasive recommendation. A useful technical case makes the recommendation consequential by returning evidence and testing the candidate's generated conditions.
- The human's scarce contribution may be generating a better frame within which execution becomes tractable and trustworthy.

## Candidate-generated definitions of done

- The candidate should generate:
  - the accountable outcome;
  - the assignable unit of work;
  - explicit exclusions and constraints;
  - the claims that require verification;
  - discriminating receipts for those claims;
  - failure, rollback, or escalation conditions;
  - priorities when not everything can be proven within the budget.
- The agent executes within that contract; the candidate accepts or revises the result using the generated receipts.
- The candidate creates a small evaluation system around the work: what must be true, how truth becomes observable, and when the system has earned acceptance.
- The receipts can themselves be tested:
  - **soundness:** known-bad artifacts fail;
  - **completeness:** the gold and valid alternatives pass;
  - **discrimination:** plausible near misses are separated from valid work;
  - **executability:** another actor can actually obtain the evidence;
  - **economy:** requirements do not exceed the warranted scope;
  - **closure:** passing supports a real accept, ship, or stop decision.

## Scoping as a leveling signal

- A useful hypothesis: level is demonstrated by finding the smallest assignable scope that closes the accountable outcome.
- Bigger scope is not automatically higher level. Senior judgment may correctly select a one-line change.
- Two symmetric failures:
  - **under-scoping:** assigning a patch when the failure lies in an interface, ownership boundary, or operating mechanism;
  - **over-scoping:** proposing a platform, migration, or reorganization when a bounded change would close the outcome.
- Scope is multidimensional: breadth of consequences, uncertainty, autonomy, influence, interdependence, and time horizon.
- A generated scope can be tested against hidden cases:
  - Does it resolve the stated outcome?
  - Does it preserve adjacent invariants?
  - Can the assigned actor execute it with the supplied authority and context?
  - Are its receipts sufficient for acceptance?
  - Does it introduce unnecessary surface area?
  - Does it strand essential work outside its boundary?
- Do not infer a stable career level from one case. Scoping is likely domain- and exercise-specific.
- Leveling needs matched situations: a case requiring a local fix, one requiring wider reframing, and negative controls where expansion or intervention is harmful.

### When a profile becomes a level

- A level claim asserts an ordered structure: whoever clears level five clears everything level four requires.
- That ordering is testable, not assertable. Pooled across candidates, the receipts must show a stable difficulty ordering (Guttman structure; IRT/Rasch puts item difficulty and person ability on one scale and tests the fit).
- Until the ordering holds empirically, a level is a narrative and the honest output is the task-conditioned profile.

## Organizational translation stack

- Provisional stack: **vision -> direction -> scope -> deliverables -> execution -> receipts**.
- Useful title shorthand, not a universal title taxonomy:
  - CEO primarily generates vision.
  - Director primarily generates direction.
  - Manager primarily generates bounded team scope.
  - IC primarily generates deliverables and technical receipts.
  - Agent or tool primarily executes.
- Pushback: senior ICs often generate direction and scope; managers may inherit scope; organizations distribute these responsibilities differently.
- Better generalization: a person at each boundary translates ambiguity from the layer above into an executable contract for the layer below without losing upstream intent or unnecessarily dictating downstream execution.
- Each layer has its own kind of definition of done. Higher layers may begin as qualitative judgment rather than booleans.

## The rubric recurses

- Hiring is itself a composed system: hiring manager plus recruiters, screeners, AI tools, and reference channels. The hiring manager occupies the same seat in it that the candidate occupies next to the coding agent.
- The four dimensions fire unchanged on the HR transcript's case hire:
  - **appropriate reliance:** accept the recruiter's shortlist when evidence backs it; reject the AI screener's score when the why is unavailable. The hiring manager's discomfort with unexplained screening outputs was correct reliance behavior, not technophobia;
  - **timely redirection:** notice the process is producing fog instead of evidence and redirect before the budget (open-req time, interviewer hours) is consumed;
  - **verification before acceptance:** the charming under-skilled candidate is agent output—locally polished, passes the visible check (the interview), fails the hidden verifier (the skills evidence). The structured skills interview is a receipt that discriminates the submitted candidate from a near miss;
  - **boundary specification:** the SFIA profile is boundary specification—deriving the role's external contract (five skills at level five) from intended use rather than accepting the literal brief ("senior architect, you know one when you see one").
- The same scarce contribution—attend and consolidate—at a different substrate. The manager's "agent" is the team, the process, the vendor, the screening tool: noisier and slower, but the rubric dimensions are unchanged; only the artifacts differ.
- **The instrument grades its own buyer.** An employer adopting the assessment must practice appropriate reliance on the assessment; automation bias toward a receipt profile is the identical failure the assessment measures in candidates. A vendor claiming to "validate capability with a high degree of confidence" gets interrogated like an agent asserting its patch is correct: show the receipt. The two feasibility gates are the buyer's due-diligence questions, and the Uniform Guidelines' validation demand is verification-before-acceptance enforced at the institutional level.
- This collapses IC and manager cases into one construct at different boundaries: same trigger taxonomy, different delegation substrate. It also explains why the translation stack works—every layer is an Attend/Consolidate role supervising a stochastic executor below it.

## Vibes and managerial definitions of done

- A good manager may supply a direction, quality bar, examples, counterexamples, constraints, and acceptable risk rather than a fully executable definition of done.
- Vibes are legitimate for qualitative outcomes when the manager can distinguish good and bad realizations, explain trade-offs, respond consistently to intermediate artifacts, and own the result.
- Vibes without those capabilities are hidden preference or managerial evasion.
- A useful managerial artifact may be a **judgment contract**:
  - What should become true, and for whom?
  - What must not be sacrificed?
  - Which decisions are delegated?
  - What evidence must return to the manager?
  - Which residual questions require managerial judgment?
- One possible test: give the manager's generated brief to several independent ICs or agents. Does it permit useful variation while excluding outcomes that violate the intended direction?

## Case-based work simulation

- A PR review is an artifact-centered case study. It samples review judgment, but not necessarily implementation, prioritization, delegation, or leadership.
- Better format: a **sequential case-based work simulation**.
- Give the candidate an understructured objective, relevant context, current artifacts, constraints, and limited attention budget.
- Ask the candidate to generate the next useful structure or action.
- Execute or simulate routine work, then jump to the next consequential decision boundary.
- This compresses hours of work without converting judgment into multiple-choice recognition.
- Possible sequence:
  1. Frame the accountable outcome.
  2. Generate scope and definition of done.
  3. Delegate or specify an intervention.
  4. Receive an agent artifact or new evidence.
  5. Generate a discriminating check or revise the scope.
  6. Accept, reject, redirect, escalate, or stop.

## The compression ceiling and its substitutes

- Jaques defines level of work as the time-span over which discretion operates before evaluation. A one- to two-hour simulation compresses time by design, so it structurally cannot observe discretion that takes months to be evaluated.
- State the ceiling plainly: compression caps the maximum level the instrument can attest directly. Claiming otherwise contradicts the anchor.
- The months already happened—just not to this candidate's current task. Four substitutes, in order of evidentiary strength:
  1. **Sealed-future cases:** build the case from a real recorded situation and hold out its future. The candidate decides at time T; the archive knows T+6 months. The public-PR construction already does this at small scale (later revisions, reverts, and bug reports are a free oracle). History runs the evaluation; the item cost is curation, not waiting.
  2. **Elicit the structure of long-span discretion:** attached to a live in-frame decision, does the candidate state leading indicators, kill conditions, and revisit triggers—what would tell them they were wrong in month three? Falsifiable within the session when the stated indicators do or do not discriminate the recorded failure modes of the case. Separates managing a horizon from making a call and hoping.
  3. **Parallelize what cannot be serialized:** months of delegation are brief -> execution -> correction cycles. The judgment-contract test above compresses the sequence into parallel runs across independent executors.
  4. **Audit the months that already happened to them:** the work-evidence compiler is the longitudinal channel. Uneven opportunity and selection bias, but real elapsed time. Reference checks are the degenerate version (talk about the past, no artifacts).
- No single channel reaches months; the four triangulate it. The ceiling becomes a design pattern rather than a conceded limitation.

## Latch onto existing processes first

- The credible adoption path is an evidence layer inside a process the employer already trusts, not a new chatbot that grills candidates and emits an opaque score.
- Existing inputs include:
  - supervised technical interviews;
  - take-home submissions;
  - coding-agent transcripts;
  - PRs and review comments;
  - interview scorecards and debriefs;
  - project documents, incidents, and retrospectives;
  - promotion packets and leveling frameworks.
- Begin in shadow mode: emit an evidence profile beside the employer's existing decision without changing that decision.
- The first trust request should be: **Inspect whether the system reproduces distinctions your own experts consider consequential.**
- A supervised AI-enabled interview is a strong insertion point because task, opportunity, provenance, and final artifact are already observable. Replace only the retrospective vibe-based debrief.
- A high-volume role may require an asynchronous take-home. Capture the same schema and add a short defense of one consequential recorded decision.
- The shared flow is: task -> candidate and agent work -> trace and artifacts -> preregistered opportunities and receipts -> evidence profile -> human decision.
- Frame the product as a role-calibrated work simulation, assessment harness, or technical work sample with executable evidence.

## Coding-agent transcripts as an evidence source

- Many coding agents retain resumable histories and support export, so transcript collection may add little candidate burden.
- A useful submission package contains:
  - original objective or issue;
  - relevant and authorized repository state;
  - agent transcript and available tool events;
  - resulting diff or commits;
  - tests, CI, and verifier output;
  - later review comments or corrections;
  - a short candidate annotation of consequential decisions.
- The transcript supplies attribution context; artifacts and verifiers supply outcome evidence.
- Strong chain: candidate generated condition -> agent attempted work -> candidate intervened or accepted -> artifact changed -> verifier established consequence.
- Candidate-exported history is candidate-supplied evidence, not an authoritative log. It can be edited, selectively submitted, or omit a second agent.
- A wrapper or instrumented environment improves provenance but can only claim coverage of the recorded channel.
- Bring-your-own-agent improves work resemblance but weakens cross-candidate comparison. A standardized agent improves comparison but may suppress familiar workflows. A hybrid can preserve familiar interfaces while routing events through a common logging boundary.
- Historical sessions introduce selection bias and confidentiality constraints. Treat them as optional portfolio evidence rather than a universal requirement.

## Ship the assessment as a skill

- Inversion: instead of the candidate coming to an assessment platform, the employer ships a skill package that runs inside the candidate's own agent and environment. The candidate self-measures with receipts attached.
- One architectural constraint decides everything: **nothing held-out can ship in the package.** The agent can read every file in a skill, so a bundled rubric, seeded-defect key, or verifier is disclosed to the system under measurement by construction.
- The surviving design is thin client, sealed server:
  - **skill = shim client:** orients the candidate, fetches task envelopes one at a time from the employer's endpoint (sequential reveal survives because the next task does not exist locally yet), instructs the agent to keep the append-only transcript, timestamps events against server nonces, packages the submission bundle;
  - **server = oracle:** hidden verifiers, seeded-condition keys, negative-control assignments, and the preregistered rubric never leave it. Artifacts go up; signed receipts come back.
- Bring-your-own-agent in the candidate's real environment is the highest available ecological validity: the pair measured is the pair that shows up to work. Claims stay pointwise about that pair; no cross-candidate ranking.
- Demand-side flip: the candidate has native demand. A signed receipt profile is a credential a polished repository cannot fake, and the candidate can attach it to applications. Candidates as first users; employers as issuers later. A skill file is near-zero-friction distribution.
- Self-administration adds two threats beyond the standard model: unlimited retries (submit the best run) and item leakage (one published candidate burns the family). Known answers—per-candidate sampled parallel forms, one-attempt invite tokens, retirement policy—but they force a tier split:
  - **practice tier:** unlimited retries, public items, no attestation;
  - **attested tier:** single-attempt sealed forms, signed receipts.
  - Conflating the tiers would let practice-mode receipts masquerade as attested ones.
- "The employer makes it" is the authoring product: the employer declares role criteria and domains; a task factory compiles the skill package plus server-side keys. The generation contract is the compiler's test suite.
- Honest limit: the skill cannot fix or attest the agent configuration. The receipt must name it, and the claim stays conditional on it. The receipt certifies the pair, never the human alone—the complementarity thesis restated as a product disclaimer.

## Work-evidence compiler

- A lower-friction precursor to simulation is to compile evidence from work and hiring records that already exist.
- Common schema: **role criterion -> claimed contribution -> source -> corroborating artifact -> observed consequence -> evidence state**.
- Evidence states:
  - **claimed:** a transcript attributes a contribution;
  - **corroborated:** another record confirms the action occurred;
  - **verified:** a falsifiable outcome supports it;
  - **contradicted:** downstream evidence opposes it;
  - **unresolved:** necessary evidence is unavailable.
- A transcript utterance is not normally a receipt. "We should test adjacent roles" proves that the person said it; a linked regression test that rejects the defective artifact and accepts the gold is the receipt.
- Historical evidence is ecological but uneven. Simulation supplies comparable opportunity; historical records supply longitudinal evidence and realistic task material.
- Safer internal uses include promotion packets, closed-project retrospectives, incident reviews, interviewer calibration, and internal mobility.
- Employee evidence extraction must be visible, contestable, source-linked, and bounded. Silent continuous performance scoring would create surveillance and distort meetings.

## Comparability is the immediate gain

- The primary gain over vibes and supervision is comparability under an explicit measurement contract, not an instant claim of perfect validity.
- Fix or record the objective, context, authority, budget, agent, tools, opportunities, hidden conditions, receipts, and mapping to evidence claims.
- Supervision observes people through unequal work. An eval gives people comparable work and records falsifiable consequences.
- Agent stochasticity can make opportunity unequal. Use fixed artifacts, controlled replay, or condition results on verified trigger exposure.
- The eval relocates judgment from retrospective impressions of candidates to prospective design of situations, contrasts, receipts, and decision rules.
- Preregistration and executable receipts make scoring cheap and auditable. They do not by themselves establish construct meaning, generalization across tasks, job relevance, or a hiring threshold.
- Keep literal event columns beneath interpreted capabilities:
  - generated check rejected mutant M3;
  - preserved invariant I2;
  - broadened scope after dependency D became observable;
  - avoided broadening scope in matched control C;
  - accepted valid artifact after receipt R.
- The expensive uncertainty moves upstream from judging candidates to designing tasks, receipts, and inference mappings. That is where it should be.

## Product surface and trust

- Buyers recognize a benchmark as a number or comparison; eval engineers recognize it as a collection of receipts. The product can sell the former while retaining rigor in the latter.
- Architecture: **receipts -> capability dimensions -> role-calibrated comparison -> decision summary**.
- The comparison is the front door; the receipt ledger is the warranty.
- Prefer a comparative capability profile over one global score until reliability supports aggregation.
- Progressive disclosure:
  - recruiter: advance, review, or gather more evidence;
  - hiring manager: capability profile and cohort bands;
  - technical reviewer: artifacts, decisions, and receipts;
  - assessment owner: controls, task calibration, reliability, and version history;
  - candidate: supporting evidence and a path to contest capture or scoring errors.
- Useful promise: **Compare candidates on the same work, with every score backed by replayable evidence.**
- Useful shorthand: **Benchmark the candidate. Audit every claim.**
- Recruiters experience volume and workflow pain, but engineering leaders own wrong-hire cost, interviewer time, technical leveling uncertainty, and the loss of attribution. Lead with the engineering problem and make administration easy for recruiting.
- Likely first customer: hires software ICs at meaningful volume, already permits AI, already uses live coding or take-homes, consumes expensive senior-engineer time, and is willing to run in shadow mode.

## Practice equals training when receipts resist ceremony

- If the benchmark is representative of best practices, practicing for the interview is practicing for the job. Free training. But this is a property the instrument must earn, not one benchmarks have in general.
- Teaching to the test equals training exactly when Goodhart has nowhere to grip. Two existing mechanisms close the gap:
  - **receipts graded on consequence:** if any scored behavior can be performed as ritual, practice optimizes the ritual. The grading-discrimination gate guarantees the only practicable path through the rubric is the capability itself. The equivalence is earned per item by blinded contrasts, not assumed from aggregate representativeness;
  - **inversion pairs:** "always redirect" cannot be memorized when the next task punishes needless redirection. Practice against positive-negative pairs can only teach selectivity, and selectivity is the job.
- Precedent: aviation. Practicing for a checkride is learning to fly, because the sim is high-fidelity and the check items are the actual failure modes. Nobody calls sim hours cheating.
- Consequence: if practice works, variance collapses. Learned items stop discriminating and retire from selection into onboarding, certification, or the harness—the same treadmill as items retiring when agents learn them, now running on the human side. Selection is structurally a shrinking, moving frontier.
- For the business: selection wants variance; a good training loop destroys variance and converges people to competence. That is a certification market (checkrides, trade tickets, cloud certs) and plausibly the larger one. The practice tier of the shipped skill is the free training; the receipts are the progress bar; the sealed single-attempt form is the certificate.
- The instrument is self-dual: the same artifact is a selection instrument at the frontier and a curriculum behind it, and items migrate from the first role to the second as they are learned. That migration is not leakage or decay; it is the product working.

## Familiar proxies and stronger evidence

- Hiring is an allocation decision under ramp time, supervision capacity, delivery urgency, compensation, and failure risk—not a theoretical question of whether anyone could eventually learn the job.
- Weak proxies survive because they are cheap, legible, searchable, and operationally convenient. "Years of experience with RAG" may loosely proxy exposure to production failure modes even though it does not prove capability.
- Do not require recruiters to abandon familiar claims. Give them a better evidentiary substrate:
  - "3+ years with RAG" -> demonstrated production-RAG capability;
  - "senior engineer" -> demonstrated system-scope judgment;
  - "strong with AI" -> produces verified agent work with bounded supervision;
  - "good reviewer" -> rejects defective changes while accepting valid controls;
  - "works autonomously" -> generates adequate scope, receipts, and closure.
- Historical exposure and pointwise demonstration are complementary: **historical exposure + demonstrated capability + required supervision**.
- The commercial promise is not epistemology as such. It is evidence about what the candidate can verify, ship, and safely delegate today.

## IC and manager cases

- Keep underlying facts similar; change authority, available actions, and accountable outcome.
- IC cases should ask the candidate to generate technical boundaries, experiments, deliverables, and receipts.
- Manager cases should ask the candidate to generate ownership, priorities, decision rights, evidence requirements, fallback conditions, and closure mechanisms.
- A manager should not receive extra credit for personally finding the planted technical defect if their accountable contribution is placing judgment at the right boundary and ensuring closure.
- Managerial receipts are often proxies because business and people outcomes may take months. Do not call an assigned owner or scheduled follow-up a verified reward unless closure is actually observable.

## Social-desirability constructs need implicit elicitation

- Traits with a social-desirability problem—accountability, intellectual honesty, escalation judgment—must be elicited implicitly, because the announced version measures knowledge of the desirable answer. In-frame elicitation is not merely better for these; it is the only valid channel.
- Accountability decomposes into trigger-action-receipt:
  - **trigger:** an outcome went wrong under attribution ambiguity, with a plausible alternative target for blame and a cost to owning it;
  - **action:** consequential ownership—disclosure before detection, correction attached, affected parties informed;
  - **receipt:** what changed—the disclosure carried information (what failed, what it affects, what to check now), not an apology.
- The composed session generates the trigger natively: the agent is the ideal scapegoat, and "the agent wrote that" is always available and often true. A candidate submits work containing a defect the agent introduced and they failed to catch; what they do next is the accountability observation.
- The short defense of one recorded decision is already the roleplay surface. Present the candidate with their own miss and observe whether they account for it or relitigate it.
- Ceremony screen: verbal ownership without correction ("I take full responsibility") earns nothing.
- Negative control: over-owning is a response bias, not a virtue. Match a catchable miss (owning it is correct) with a defect no reasonable check would have found under the budget (calibrated non-ownership is the better answer). Score selectivity across the pair.

## Design controls and threats

- Open generation improves authenticity but makes grading harder.
- The evaluator still embeds a theory of appropriate scope through the hidden near misses and verifier.
- Candidate-generated receipts can reward test-writing fluency rather than the actual job capability.
- An agent can generate the candidate's scope and receipts, recreating the attribution problem.
- Time-compressed cases expose only scopes recoverable from the supplied context.
- Use positive and negative controls so habitual skepticism, expansive reframing, and excessive verification do not score as seniority.
- Grade consequences, not vocabulary, verbosity, breadth, or agreement with an expert key.

## Literature anchors

- **SFIA:** professional skill plus autonomy, influence, and complexity; knowledge alone does not establish responsibility level. <https://sfia-online.org/en/about-sfia/how-sfia-works>
- **Jaques, time-span of discretion:** level of work as the duration over which discretion must operate before evaluation. Early empirical formulation: <https://doi.org/10.1016/0030-5073(74)90022-1>
- **Levels of automation:** the tradition that levels the human-machine division of labor rather than the person. Sheridan and Verplank's ten levels; Parasuraman, Sheridan, and Wickens's types-and-levels model <https://doi.org/10.1109/3468.844354>; SAE J3016's driving levels as a leveling of supervision responsibility (who monitors, who intervenes, who is the fallback). The direct precedent for "how much supervision will they consume." J3016 is also the cautionary tale: boundary cases (handoff) are where the trouble lives, and levels get misread constantly.
- **Item response theory / Guttman scaling:** the psychometric criterion for when receipts earn a level—pooled responses must fit a stable difficulty ordering before ordered performance classes are defensible.
- **Mumford, Campion, and Morgeson, leadership strataplex:** cognitive, interpersonal, business, and strategic skill requirements vary with organizational level; higher roles do not merely exchange one skill category for another. <https://doi.org/10.1016/j.leaqua.2007.01.005>
- **Morgeson and Humphrey, Work Design Questionnaire:** separates autonomy, complexity, problem solving, task identity, interdependence, and other work characteristics. <https://doi.org/10.1037/0021-9010.91.6.1321>
- **GQM+Strategies:** connects business goals and strategies to operational software goals, questions, and metrics. <https://arxiv.org/abs/1402.0292>
- **Assessment centers:** multiple job-related simulations with a common classification system; exercise specificity warns against treating one case as a stable trait. <https://doi.org/10.1177/0149206314567780>
- **Assessment-center construct validity:** scenario and scoring design determine whether dimensions are actually recoverable. <https://doi.org/10.1111/1468-2389.00085>
- **Constructed-response situational judgment tests:** open responses preserve generation but introduce scoring and validation problems; validity does not transfer automatically across formats. <https://doi.org/10.1111/medu.70245>
- **Person-job fit:** distinguish demands-abilities fit from needs-supplies and person-organization fit; capability and compatibility are not the same decision.
- **CoderPad State of Tech Hiring 2026:** algorithms remain common while real-world simulations, system design, pair programming, code review, debugging, and visible AI use are growing. <https://coderpad.io/survey-reports/coderpad-state-of-tech-hiring-2026/>
- **HackerRank Developer Skills Report 2025:** developers prefer practical challenges and report substantial mismatch between assessments and real work. <https://www.hackerrank.com/reports/developer-skills-report-2025>
- **HAI-Eval:** collaboration-necessary coding tasks compare the human-agent pair against unaided human and standalone-agent performance. <https://arxiv.org/abs/2512.04111>
- **World Bank assessment experiment:** proposes collecting AI transcripts and adding a human-in-the-loop score because final code no longer reveals enough methodological judgment. <https://blogs.worldbank.org/en/impactevaluations/rethinking-coding-assessment-in-an-ai-assisted-world>
- **Emerging products:** ThinkingTrace, Tandem AI, MarioHR, Probe, and Ella indicate a young category around real codebases, allowed AI, captured traces, and structured evaluation; their existence establishes convergence, not validity.

## Possible contribution

- The ingredients are established; the synthesis may still be distinctive.
- Candidate receives an understructured, level-appropriate objective.
- Candidate generates an assignable scope, definition of done, and executable receipts.
- Agent or simulation produces artifacts inside that generated contract.
- Assessment observes whether the candidate-generated contract preserves upstream intent while avoiding unnecessary control of downstream execution.
- Possible name: **generative work sample**, **case-based complementarity simulation**, or **candidate-constructed evaluation boundary**.
- Narrow claim: the assessment measures whether the candidate can translate an upstream objective into an economical, assignable, and verifiable downstream contract under the tested conditions.

## Open questions

- Is generating a definition of done a distinct construct, or an artifact produced by domain knowledge, conscientiousness, and general reasoning?
- Which parts of scope quality can be objectively verified, and which remain evaluator judgment?
- Can candidate-generated receipts be scored without collapsing them into a hidden canonical solution?
- How much context is required before broader scope becomes warranted rather than speculative?
- How should agent assistance be standardized without removing the candidate's normal working method?
- Can the same underlying case support IC and manager variants without leaking the expected abstraction level?
- What downstream outcomes would validate the case profile against actual job performance?
- How many sealed-future cases can be curated per domain before the archive of well-recorded decisions with knowable outcomes runs dry?
- At what rate do items migrate from selection to curriculum, and does the frontier replenish fast enough to keep a selection product viable, or does the business converge to certification?
