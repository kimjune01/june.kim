# Manifund proposal — draft

Public, regrantor-driven, fast. Punchier than LTFF; written to be read by non-specialists scrolling
a feed. Same core as the LTFF application, compressed.
Reshaped 2026-07-20: auditor-shaped, matching the LTFF reshape.

## Title

Independent audits of AI benchmarks, with receipts anyone can re-run

## Summary (the one-liner shown in lists)

I audit the evaluations the AI field steers by, and every finding ships with a receipt a stranger
re-runs. I published a receipted audit of SWE-bench Pro on 21 June; on 8 July OpenAI audited the same
benchmark, found overlapping failures, and deprecated it. Fund a year of the practice.

## What's the problem?

The field steers by evaluation numbers, and the numbers circulate on trust. In February OpenAI
recommended SWE-bench Pro and the field followed. In July OpenAI deprecated it and the field followed
again, at the same speed, on a headline number (~30% of tasks broken) that cannot be reconstructed from
anything they published. Between those two dates I audited the same benchmark and proved a 15.0% floor
of defective tasks, every label backed by a receipt that re-runs from a cold checkout. Same conclusion,
opposite warrant: theirs you have to trust, mine you can run.

SWE-bench Pro was one of eight benchmarks I audited between May and July, all from the public side, no
special access. Each one broke somewhere: answer keys that fail their own graders, leaderboards that
can't be re-derived from anything released, a benchmark where all 83 tasks still pass after the agent
destroys the user's unrelated files. The month I published a checklist of the checks, a 48-author paper
launching the AVERI audit institute priced the cheapest rung of its audit program at $300,000 per
engagement. The checks that caught everything above cost an auditor's time, and the first five are
free.

## What's the solution?

Keep running the cheap level, and make it standard. Each audit: pick an evaluation the field actually
cites, run the cost-ordered checks against its own shipped artifacts, publish every finding with a
re-runnable receipt, give the authors right of reply, and file the actionable part where the
maintainers work (the Terminal-Bench audit produced an implemented upstream fix to its grader).
Receipts do not remove judgment. They expose its inputs, so another auditor can reproduce or contest
it. Audits that come back clean get published too.

Then compound it: the checklist becomes a disclosure standard for what an eval must publish, the checks
become tools anyone can run (my `determinacy` tool already audits benchmarks it wasn't written for),
and the failure modes get filed into the standing registries evaluators already read (first filing:
BenchRisk/BenchRisk#8, the NeurIPS 2025 benchmark-reliability registry). The full argument is in
*Assurance at the Boundary* (DOI 10.5281/zenodo.21461148), my response to the AVERI agenda.

## What's the evidence it works?

- The head-to-head above, with receipts: my audit at DOI 10.5281/zenodo.20738219, the comparison
  written up at june.kim/an-epistemic-ablation.
- Eight audits, eight defects, all receipted: june.kim/how-to-audit-a-benchmark has the table and the
  cost-ordered checklist.
- The practice lands where evaluators work: an implemented Terminal-Bench grader fix
  (harbor-framework/harbor#2266), a failure mode filed into BenchRisk, audits archived under DOIs with
  regrade scripts.

## What will the money do?

Tranched, so one regrantor can make the first move and the rest can co-fund:

- **$10k:** the next two audits, targets chosen by citation weight, receipts and right of reply
  included; covers run costs and two months of full-time work.
- **$30k:** six audits total, plus the disclosure standard v1 (record schemas for what an eval must
  publish), the checklist hardened into tools a second team runs without me, and one documented
  outside reproduction of a sampled audit verdict.
- **$75k:** 12 months full time: eight audits committed and ten targeted, the standard, and a
  ten-task discovery-benchmark pilot to replace what the Pro deprecation vacated (post-cutoff,
  contamination-controlled by construction, receipts by construction; twenty tasks is stretch, and so
  is extending the same replay standard to AI agents' claims about their own work).

Every tranche ends in a public, reproducible artifact.

## Who am I?

June Kim, independent researcher, based in Canada. Full-stack: the artifacts (audit repos, tools,
upstream fixes, DOIs), the methodology (the checklist, right of reply, preregistration), the argument
(*Assurance at the Boundary*), and the epistemics behind it (*Verifiable Knowledge*, the declared
standard the audits grade against). Everything is at june.kim and github.com/kimjune01, reproducible
from committed inputs. I design for a distrusting auditor by default; the OpenAI convergence is what it
looks like when that pays.

## Risks / what could fail

Audits are demand-constrained: the checks are cheap, and the risk is that
nobody with stakes reads them. SWE-bench Verified's contamination was common
knowledge while it stayed the field's reported number for two years. Mitigations are built into the
shape of the work (findings filed as fixes where maintainers work, modes filed into registries
evaluators read), but a maintainer can ignore a fix and a registry can ignore a filing. Both have already happened. I record the outcome and move to the next target rather than chase it.

The discovery benchmark's hard input is curating contamination-free cases, which is slow. The stretch extension to agent reasoning rests on one
demonstrated case and may not generalize. A null result is a possible outcome of the grant, and
reporting it is part of the work.
