# LTFF application — AS SUBMITTED 2026-07-20

Submitted via EA Funds Paperform (av20jp3z.paperform.co), confirmation page received.
Fund: Long-Term Future Fund. EAIF transfer: YES. Program: Applied GCR Grants. Individual.
Public reporting: PUBLIC. Referral to other funders: YES. Network sharing: YES.
Time-sensitive: NO. Dates: 2026-08-01 to 2027-07-31. USD. Requested: $75,000.
Location: Burnaby, British Columbia, Canada; implemented online.
Contact: kimjune01@gmail.com. Portfolio/CV: june.kim, github.com/kimjune01.
EV employment: never held any paid position.

## Short description (public, as submitted)

12-month salary to independently audit AI benchmarks, publishing re-runnable receipts and a disclosure standard

## Summary (as submitted)

Frontier AI Auditing (Brundage et al. 2026), AVERI's launch paper, calls for a third-party AI auditing ecosystem; its cheapest assurance level costs $300k per engagement and its strongest levels are not yet feasible. I have been running the level below: audits of public evaluation artifacts, every finding shipped with a receipt a stranger re-runs. I audited eight benchmarks May-July 2026, unfunded. One finding was confirmed externally: a month after my receipted SWE-bench Pro audit, OpenAI audited the same benchmark, found overlapping failures, and deprecated it. Their headline number cannot be reconstructed from what they published; mine re-runs from a cold checkout. The grant buys a year of the practice: 8-10 audits of the evals the field steers by, a disclosure standard for what an eval must publish, and a 10-task discovery-benchmark pilot. Evaluation numbers drive deployment, safety cases, and procurement; audits anyone can re-run are the cheap, demonstrated defense.

## Project goals (as submitted)

Actions: (1) Audit 8-10 widely cited AI evaluations from the public side, each with re-runnable receipts, right of reply to the authors, and the actionable part filed upstream as an issue or fix (my Terminal-Bench audit produced an implemented grader fix, harbor-framework/harbor#2266). Checks are declared before intensive review, and clean audits get published too. (2) Publish a v0.1 disclosure standard for evaluation records (schemas for tasks, per-task outcomes, harness configuration, grader identity) and file failure modes into the standing registries (first filing: BenchRisk/BenchRisk#8). (3) Build a ten-task discovery-benchmark pilot, post-cutoff and contamination-controlled, to replace what the SWE-bench Pro deprecation vacated. Goal: evaluation claims that regulators, insurers, and deployers act on become checkable by parties who do not trust the evaluator. Success is scored in recorded attempts, not promised adoption: right of reply documented per audit, outside reruns of sampled receipts solicited, maintainer responses ledgered, one outside implementation attempt of the standard. Fit: unaccountable evaluation claims are a scalable oversight failure in AI x-risk; receipts are the structural defense, deployable today at no training cost.

## Track record (as submitted)

The strongest external check on this work happened without my involvement. I published a determinacy audit of all 728 public SWE-bench Pro tasks on 21 June 2026: a proven 15.0% floor of underdetermined tasks, every label re-running from a cold checkout (DOI 10.5281/zenodo.20738219). On 8 July OpenAI audited the same benchmark, found overlapping failure categories, estimated ~30% broken, and retracted its February recommendation of it. The numbers are compatible, a proven floor under a broader estimate; the difference is that mine re-runs without trusting me (june.kim/an-epistemic-ablation). It was one of eight audits between May and July, all public-side, distilled into a cost-ordered checklist (june.kim/how-to-audit-a-benchmark). Where the work has landed: an implemented upstream Terminal-Bench grader fix (harbor-framework/harbor#2266), a failure mode filed into the NeurIPS 2025 BenchRisk registry (BenchRisk/BenchRisk#8), audits archived under DOIs with regrade scripts, and a response paper to the AVERI auditing agenda (june.kim/assurance-at-the-boundary, DOI 10.5281/zenodo.21461148). Failure disclosed: five earlier audits drew no substantial maintainer response; the fix-shaped ones landed. All of it unfunded and solo. 2026 to date: $0 external funding, 1 FTE.

## Funding amount and breakdown (as submitted)

Total $75,000 USD for 12 months, 1 FTE (me). Breakdown: 82% stipend (Canadian income tax and self-employment contributions included in the stipend line), 8% compute and audit run costs, 10% buffer (stated explicitly). Audit runs are cheap by design: the highest-yield check costs about $1 per benchmark, and mechanism runs are 2-4 hours and parallelize. No spreadsheet attached; the budget is one salary plus small compute, fully described here.

## Alternatives to funding (as submitted)

Applying to Manifund in parallel this week for the same program ($75k mainline, tranches from $10k; no decision yet; I will update LTFF either way). No other funding applications in the last 12 months. Without funding I continue at reduced cadence while contracting part-time; the practice survives, but the timestamped record accumulates slower exactly while eval-driven decisions accelerate.

## Use for additional funding (as submitted)

Expand the discovery pilot from ten toward twenty tasks, raise the audit cadence toward monthly, and fund an outside team's independent reproduction of sampled receipts, which is the strongest test of the premise.

## Anything else (as submitted)

Conflicts: I have no financial relationship with any organization whose benchmarks or frameworks I have audited or responded to, and no organization reviewed the audits before publication. Two interest disclosures, carried on the audit posts since publication: I applied for a role at Epoch AI, co-producer of MirrorCode, one of the eight audited benchmarks (the application has since been declined), and I have written to Laude Institute, maintainer of Terminal-Bench, about research roles. They change none of the receipts, which is the point of the practice. One further ask: the input I do not supply myself is direction. If a fund manager can introduce me to a senior researcher with named problems and no spare hands, an hour a month of their direction buys them a full-stack executor against their agenda; failing an introduction, I will arrange the match separately and name it in progress reports.

## How heard (as submitted)

Common knowledge in the AI safety community; LTFF is the standard first stop for independent AI safety researchers.
