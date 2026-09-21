# Reproduce the JevBench audit

This bundle accompanies “Auditing JevBench” (2026-09-21). It checks the pinned published artifacts without making model calls. No API keys are needed.

## Files

- `audit.py`: independent aggregate arithmetic checks and probes of the official scorer.
- `audit-results.json`: results, file hashes, exact probability witnesses, public paired outcomes and matched-cohort economics.
- `audit-run.txt`: captured output of the audit script.
- `UPSTREAM-LICENSE.txt`: JevBench's MIT license, retained for upstream-derived data.

Download these files into an empty working directory. Install `uv` and Git if needed, then obtain the pinned sources:

```sh
git clone https://github.com/fstandhartinger/jevbench.git upstream
git -C upstream checkout --detach f8ce71361165846101d02ebc83ad44e47ae44fc3
git clone https://github.com/anisselbd/jev-phishing-bench.git phishing-upstream
git -C phishing-upstream checkout --detach 1d56e8c64d029a9554a0874e2ef2901ed196e230
uv run --no-project python audit.py
```

The script overwrites `audit-results.json` with its computed results and prints its checks. To keep the downloaded receipt for comparison, rename it before running. The script uses only Python's standard library and the pinned JevBench source modules.

Run the upstream unit tests separately:

```sh
cd upstream
uv run --no-project --with pytest python -m pytest -q
```

The audited snapshot passed all 68 tests. The audit's own assertions also passed: 31 composite rows, 26 ranks, 231 public answer keys, the calibration probes, output-contract mutations, public outcome comparisons and the phishing confusion matrices.

## What the checks establish

`single_task_exact_gold` and `single_task_sharpened` apply the official scoring functions to the public incident-probability task in isolation. They show the objective's ordering, not a statistically estimated calibration rate. The sharper response earns 82.5 against the exact gold's 65.0 on that isolated probe. This does not establish that sharpening the actual models' responses would improve their leaderboard ranks.

`public_hard_gold` uses exact gold distributions on all ten public probability questions and one-hot gold labels on the other 101 public hard questions. Accuracy is 1, mean total variation distance is 0, ECE is 0.0299765766 and composite calibration is 97.0023423.

`full_cohort_economics` uses the same 534 decisions for both price and accuracy. Jev has 468 correct and DeepSeek 511. DeepSeek's additional reported price is $0.553768 per 1,000 decisions; its additional correct answers are 80.5243 per 1,000. The ratio is $0.00687703 per additional correct answer. It assumes equal error costs and excludes latency, retries and downstream costs. It is not an estimate over all AI workloads.

## What remains unverified

The composite checks reproduce arithmetic conditional on the supplied aggregates. They do not independently reconstruct the leading models' predictions, probability calibration, API usage or measured latency. Their raw responses are not shipped in the inspected repositories. The 231 one-hot-key passes check key/scorer compatibility, not the semantic correctness of all task texts. The audit makes no inference calls and does not test nonthinking DeepSeek.

The phishing supplement checks aggregate arithmetic and inspects the published method. It does not rerun the model calls, refit the signal classifier or independently validate the reported significance tests.

The post's preference for starting with DeepSeek V4.1 Flash is a discussion judgment about its measured accuracy advantage and small absolute price premium. Choosing Jev would require evidence that its cost or latency advantage matters on the intended workload at acceptable accuracy. The benchmark does not establish a universal winner. Findings had not received a maintainer response when this draft was prepared.
