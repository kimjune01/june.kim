# LTFF application — draft

Reusable core for LTFF, Manifund, and Cooperative AI. Tuned for LTFF's questions.
Numbers in [brackets] are yours to set. Voice is yours; this is a starting cut to react to.
Reshaped 2026-07-20: auditor-shaped, Brundage et al. (AVERI) as the framing document.

---

## Project title

Independent AI evaluation auditing: the assurance level below AAL-1, with receipts

## One-paragraph summary

Frontier AI Auditing (Brundage et al. 2026, arXiv:2601.11699) calls for a third-party AI auditing
ecosystem; it is the launch paper of the AVERI institute, with 48 authors across GovAI, MIT CSAIL,
Stanford, and Mila. Its cheapest assurance level runs $300,000 to $600,000 per engagement by its authors' own
estimates, and its strongest levels are not yet feasible. I have been running the
level below their first: assurance attached to the artifact at the public boundary, against a declared
standard, under a named signature, at the cost of an auditor's time. Between May and July 2026 I audited
eight benchmarks this way, every severe defect shipped with a receipt a stranger re-runs. One finding
was confirmed externally: a month after my receipted SWE-bench Pro audit, OpenAI audited the same
benchmark, found overlapping failures, and deprecated it (details under Track record). My response to the AVERI agenda,
*Assurance at the Boundary* (DOI 10.5281/zenodo.21461148), argues that entitlement to a claim
comes from replay, so assurance attaches where replay is possible, and the field should spend its
audit budget from the cheapest demonstrated instrument upward. That declared standard is *Verifiable
Knowledge*, which converts the properties the field keeps requesting (falsifiability and
monitorability) into checkable ones. Its verdicts have survived external contact. This grant funds a year of the practice and the infrastructure that lets others run it.

## What I will do

I work as a full-stack researcher: every layer this practice needs ships from one person. The artifacts
(audit repos, the `determinacy` tool, upstream fixes, receipts under DOIs), the methodology (the
cost-ordered checklist, right of reply, preregistration), the argument (*Assurance at the Boundary*),
and the epistemics (*Verifiable Knowledge*). Funding
buys the next year of all four.

1. **Keep auditing, where the numbers steer.** Audit the evaluations that labs and evals shops actually
   report against, selected by citation weight rather than auditability. Each audit ships the same way
   the first eight did: re-runnable receipts, a right-of-reply to the authors before or at publication,
   and the actionable part filed where the maintainers work, as an issue or an implemented fix (the
   Terminal-Bench audit produced an upstream grader fix, harbor-framework/harbor#2266). Checks are
   declared before intensive review. Audits that find no material defect get published the same way.
   The instrument has come back near-empty before: the one benchmark re-audited after its revision
   mostly held, and I reported that. Deliverable: eight audits committed, ten targeted, in
   twelve months, each archived under its own DOI, with the target queue and selection rule published
   before the checks run. The evidence this cadence holds: the first eight took three months,
   unfunded, alongside two papers.

2. **Turn the checklist into the standard.** The eight audits compressed into a cost-ordered public
   checklist (june.kim/how-to-audit-a-benchmark) whose first five checks are free, and the checklist is
   why the eighth audit cost a fraction of the seven. Funding hardens it into the disclosure standard
   *Assurance at the Boundary* argues for: record schemas for what an eval must publish (tasks, per-task
   outcomes, harness configuration, grader identity), automatable checks kept cheap enough that a rival
   can run a competing one (my `determinacy` tool already audits benchmarks it was not written for), and
   failure modes filed into the standing registries where evaluators already look. BenchRisk/BenchRisk#8 is
   the first such filing: a new failure mode for the NeurIPS 2025 benchmark-reliability registry,
   whose own paper defers agentic benchmarks to future work. My audits are all agentic; the registry gap
   is exactly the work. Deliverables: a public v0.1 draft of the standard by month four, called v1 only after an outside
   team has used it, and four more failure modes filed. Six candidates from the checklist are already
   mapped against the registry and unfiled.

3. **Build the discovery benchmark.** My audit of all 728 public SWE-bench Pro tasks shows current
   benchmarks measure translation, leaving discovery untested. Most tasks are one-shot from the prompt,
   and a 15% floor grades unstated intent that is undiscoverable from the materials. OpenAI's
   deprecation vacated the field's default coding eval, and its own post closes by calling for
   replacements. I will build the eval that is missing: post-cutoff, discovery-hard bugs with golden
   verdicts, contamination-controlled by construction, receipts by construction. Deliverable: a
   ten-task, externally reviewed pilot by month nine; expansion to twenty tasks is stretch. Each task
   is held to the checklist this program audits others with. A public good independent of everything
   else here.

4. **(Stretch, not a committed deliverable) Extend receipts one level down, to agent reasoning.** The same replay standard applied to
   an agent's claims about its own work: the hypothesis graph, a harness-layer structure whose nodes are
   testable claims and whose edges are refutation conditions. A distrusting party re-runs the check
   instead of reading the transcript. Demonstrated once on a contamination-free, post-cutoff bug (the
   Verus experiment: preregistered, archived, regradeable), where the externalized check carried a weaker
   model to a fix the strongest released model could not reach. Deliverable: an exploratory
   with-check versus without-check replication on five new post-cutoff bugs, preregistered, nulls
   reported. Five bugs bound feasibility; they do not confirm generalization. Droppable to scope a smaller grant. If a
   benchmark audit can be priced in receipts, so can an agent's claim that its patch is correct, and this
   is where the practice points.

Everything ships as it lands: public repos, DOIs, reproducible from committed inputs, as the existing
artifacts are. Success is scored in recorded attempts, not promised adoption: right of reply documented
for every audit, outside reruns of sampled receipts solicited, maintainer responses ledgered, and one
outside implementation attempt of the standard. Audit policy, stated up front: targets and checks
declared before intensive review, conflicts disclosed per audit, corrections published in place, and
disputes resolved by re-running the receipt.

## Theory of change

Oversight of AI development currently routes through evaluations, and evaluation claims circulate on
authority. The SWE-bench Pro episode is the demonstration: the field followed OpenAI's recommendation and its
deprecation at the same speed, on a number that cannot be re-derived from anything published. An audit you must trust is indistinguishable from the auditor's
authority, and it fails exactly when the auditor's incentives and conclusions align. When evaluation
becomes the instrument regulators, insurers, and deployers act on, that failure mode is a scalable
oversight problem, upstream of the model-level one. The decision users are concrete: safety cases cite
evals, deployment gates cite evals, and procurement cites leaderboards. An audit of the eval is an
audit of every decision downstream of it.

The defense is structural and already deployed in older assurance fields: attach the claim to a check a
distrusting stranger re-runs. Receipts do not eliminate judgment. They expose its inputs and its
consequences, so another auditor can reproduce the judgment, contest it, or replace it. Brundage et al. reach record discipline at their top levels, after years
of access-building at several million dollars annually; the same discipline is deliverable at the public
boundary today for an auditor's time, and my eight audits are the existence proof. Every stronger
successor regime, including theirs, consumes exactly the records this practice starts preserving now.
What is missing is anyone funded to run the practice full time, write the
standard, and accumulate the timestamped record that later institutions cannot retroactively create.

## Relation to existing work

Brundage et al. (2026) build the access-based audit ecosystem; this funds the level below it, on the
public record. My response paper engages their framework directly.
BenchRisk (McGregor et al., NeurIPS 2025, arXiv:2510.21460) and BetterBench (Reuel et al., NeurIPS 2024, arXiv:2411.12990) are the standing
metaevaluation registries; both grew on chatbot benchmarks, and I am filing the agentic failure modes
their own papers defer. METR, UK AISI, and the labs' reciprocal evaluations run access-based engagements
whose findings are real and whose receipts are not published. The practice here is complementary and
answers the reproducibility demand now being raised within the field (Vishwarupe et al. 2026, arXiv:2605.08192).

On the mechanism side (deliverable 4), the closest neighbors are debate, prover-verifier games, and
externalized-reasoning oversight, which get the reasoning outside the model but stop at a transcript a
reader still has to trust. The hypothesis graph binds each claim to a typed check an untrusting party
re-runs, so the verdict is reconstructed rather than read.

## Track record

The strongest external check on my work happened without my involvement. On 21 June I published a
determinacy audit of all 728 public SWE-bench Pro tasks, proving a floor of 15.0% underdetermined, with
every label resolving to a committed receipt a stranger re-runs from a cold checkout
(github.com/kimjune01/swebench-pro-audit, DOI 10.5281/zenodo.20738219; right-of-reply issue filed on
Scale's tracker 9 June). On 8 July OpenAI audited the same benchmark, estimated ~30% of tasks broken in
overlapping failure categories, and retracted its February recommendation. The two audits
agree: mine is a proven floor beneath their broader estimate. The difference is the warrant. Their
number cannot be reconstructed from anything they published; mine re-runs without trusting me
(june.kim/an-epistemic-ablation).

The audit was one of eight I ran between May and July, all from the public side, distilled into a
cost-ordered checklist
(june.kim/how-to-audit-a-benchmark). The program has begun landing where evaluators work: a fix
implemented upstream for Terminal-Bench's grader (harbor-framework/harbor#2266), the audit archived
under its own DOI (10.5281/zenodo.21463236), a new failure mode filed into the BenchRisk registry
(BenchRisk/BenchRisk#8), and the response paper to the AVERI agenda (june.kim/assurance-at-the-boundary,
DOI 10.5281/zenodo.21461148).

The mechanism side, solo and in public, reproducible by a stranger:
- *The Hypothesis Graph*, *Verifiable Knowledge*, and *What Cannot Be False Cannot Be True* (preprints at
  june.kim).
- `abductor` (github.com/kimjune01/abductor) and the `inquire` skill, open source, with the
  contamination-free-by-construction worked example inquiries.
- The Verus mechanism experiment: repo and DOI, reproducible from committed inputs including a
  preregistration and regrade script.
- An iteration result: one-shot 43% → iterative 91% PR-approval across 27 merged PRs in 9 real
  repos (Go/TS/Rust), isolating the review loop as the bottleneck.

I work in public and design for a distrusting auditor by default, the same property this grant funds me
to practice full time.

## What I need

The year demonstrated I supply my own execution. The eight audits, the response paper, the tooling,
and the upstream fixes ran with no supervisor, institution, or funding, at a cadence I can
sustain.

The two inputs I do not supply are a salary and a problem-owner. The salary is the budget below. The
problem-owner is a senior researcher with named problems and no spare hands, who points this
instrument at their agenda and reads what comes back. The trade is concrete. They spend an hour a
month on direction; they gain a full-stack executor who ships audits, tools, and receipts against
their problems at no cost to them. The judgment calls this year that cost the most were choices of
*where* to point the instrument. If LTFF can make one introduction from its network, that is worth as
much to this program as the funding. Failing that, I will arrange the match separately and name it in
progress reports.

## Budget

$75,000 for 12 months, primarily as researcher salary/stipend to work full time. Compute is
modest: audits run on the benchmarks' own shipped artifacts for dollars (the highest-yield
check in the checklist costs about $1). Mechanism runs are 2–4h and parallelize, so ~$5k covers
experiments and ablations. The expensive inputs are auditor time and the curation of contamination-free,
post-cutoff cases, which is the same hard input deliverable 3 (the benchmark) produces at scale. I can
scope to a smaller grant by dropping the stretch mechanism deliverable and slowing the audit cadence; I
can absorb a larger one by widening both.

## Other funding and conflicts

Applying to Manifund in parallel for the same program; will update LTFF if it lands. I have no
financial relationship with any organization whose benchmarks or frameworks I have audited or
responded to, and no organization reviewed the audits before publication. Two interest disclosures, carried on the audit posts since publication: I applied for a role at
Epoch AI, co-producer of MirrorCode, one of the eight audited benchmarks (the application has since
been declined), and I have written to Laude Institute, maintainer of Terminal-Bench, about research
roles. They change none of the receipts, which is the point of the practice.
