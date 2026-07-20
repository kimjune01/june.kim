---
variant: post-medium
title: "Game of Benches"
tags: methodology, epistemology, reflecting
---

Between late May and the middle of July I audited five coding benchmarks. [DeepSWE](/auditing-deepswe) landed on 26 May. [ProgramBench](/programbench-measures-recall) in June. [Terminal-Bench](/terminal-bench-frame), [MirrorCode](/auditing-mirrorcode), and [FrontierCode](/auditing-frontiercode) in July, the last two within a day of each other. [SWE-bench Pro](/a-determinacy-audit-of-swebench-pro) was already in the field on OpenAI's February recommendation.

Five instruments in eight weeks, all claiming to measure whether a model can do software engineering. If these are instruments, the fifth one is redundant and nobody funds it. If they are brands, the fifth one is a market entrant.

## Recognition is the asset

A bare score is not a claim. *80.3%* communicates nothing without a denominator, a task distribution, and a comparison class. The benchmark's name carries all three. A lab shipping a model needs a *common* instrument rather than a good one, a coordinate system that lets its number and a rival's sit in the same sentence. That is why a lab reporting its own internal eval gets discounted on arrival. Nobody knows the scale, so the number reads as a press release.

Recognition flows downhill, and a lab large enough can mint it. In February OpenAI [discredited SWE-bench Verified](/swebench-verified) and pointed the field at Pro, and the field went. On 8 July it [estimated ~30% of Pro broken](/an-epistemic-ablation) and retracted, and the field is going. The benchmark needs the lab's name more than the lab needs the benchmark's. And a benchmark is worth most to a lab while it is fresh and unsaturated, worth least once a rival tops it.

So the game is not a pure coordination game, where the field converges on one instrument and stays. Every lab wants a shared scale and wants to be at the top of it, and those two pull apart. The field coordinates until the standings make defection worth it to someone large enough to move the focal point. February and July were those defections, and that is why five instruments are in the field at once instead of one.

## Scandal becomes changelog

In May I found four DeepSWE reference solutions failing their own verifiers. On 14 June the maintainers shipped [v1.1](/auditing-deepswe-v1-1): v1 frozen, grading moved from process exit codes to specific test node IDs, the four flagged tasks up between 10 and 65 points while the pooled pass rate went 0.509 to 0.518. That is the good-faith response, carried out at the mechanism instead of buried in a caveat.

The defect is fixed and the headline survives. Nothing was retracted because nothing had to be. A version bump converts a scandal into a changelog.

Nothing structural stopped Scale from shipping a Pro v2. But version discipline only works as a defense if it predates the accusation. Datacurve froze v1 and published a delta before anyone needed it to, and a bump issued in answer to a charge reads as an admission. Pro arrived as one number and one release, so the only edit available to a reader was to stop believing it. A benchmark with no revision history to fall back on gets retired instead.

So DeepSWE never gets retired. Not because it stays clean. Because it versions. Contamination will eat the task set, since the repositories are public and active. The fix for that is another bump. v1.2. v2. Every defect anyone files arrives as a minor. My falsifier is a retirement or deprecation notice before the end of 2027.

That is the product. Scores climb toward the ceiling, the version bumps, the board resets near the floor, the climb starts over. A [Shepard tone](https://en.wikipedia.org/wiki/Shepard_tone), rising forever, arriving nowhere.

The version bump is also the immune response. Datacurve cannot defend its brand by being more correct, since correctness is what audits establish and audits are cheap for outsiders to run. It defends by shipping versions faster than defects accumulate.

## Effort tracks exposure

A company whose brand is its business will do whatever it takes to earn the brand, which is not what it takes to be true. The two coincide as far as someone is checking.

The DeepSWE ledger measures the gap. The scoring debt is paid; the disclosure debt is not. A broken gold is re-runnable by any stranger with a spot instance, so it threatens the asset. Datacurve fixed it within a month, without ever answering me.

I filed on their [issue tracker](https://github.com/datacurve-ai/deep-swe/issues/52), emailed, and asked on X. No response through any of them. The fix shipped and the acknowledgment never did. Answering in public would confer recognition on the auditor, and recognition is the asset in this game. Silence costs nothing, and the fix banks the benefit either way.

Datacurve also sells coding data to frontier labs, the same population its board ranks. Which labs are customers is not public, though with five plausible buyers in the world the secret is thin. The anchor is whoever has the deepest pockets and the largest appetite for coding data. That is deducible from the outside. That disclosure costs a sentence and breaks no comparability, and it did not ship. Neither did the excluded-trial reasons or the per-trial artifacts. Those make the benchmark more checkable without making it look better. If Datacurve publishes the excluded-trial reasons and the per-trial artifacts before the next DeepSWE version bump, I am wrong.

## Audits were never the bottleneck

Running a benchmark's answer key against its own verifier takes one spot machine, ten tasks at a time, under an hour, under a dollar, with no model in the loop. I audited five benchmarks in eight weeks, alone. Production is not scarce. Nobody is compelled to consume the output and nobody pays for it, so the constraint is demand.

The nearest thing to a buyer is a lab with a reason to discredit a rival's instrument, and even that one buys nothing. OpenAI ran its Pro audit in-house, with unnamed engineers and an unreleased pipeline, and released the number rather than the work.

So the channel is scandal, and scandal selects against receipts. OpenAI's ~30% is the scandal-shaped artifact: a round number, a benchmark to blame, no method to slow anyone down, repeated by the outlets within the week. My 15.0% underdetermination floor, on the same benchmark, is smaller, conservative by construction, and comes with an invitation to go re-run it. The qualifications that make a number checkable are the same properties that make it undramatic.

And when the scandal lands, the consequences are thin. Pro was tombstoned in July and its leaderboard still stands and its scores still circulate. FrontierCode v1.1 retired the Diamond subset its launch press quoted, and [Epoch reports the Diamond score today](/auditing-frontiercode) with no comparability note. On a third party's chart, a number outlives the subset it was computed on. That is what a consequence looks like here.

## The benchmark is the sample

Fresh data is expensive the way human expert labor is expensive. Datacurve produces it through [Shipd](https://datacurve.ai/), a bounty platform that has paid working engineers over $1 million to author tasks. The DeepSWE set is [113 problems written from scratch across 91 repositories](https://deepswe.datacurve.ai/), so no model could have seen the solutions at publication. That is the point of the benchmark and the cost structure of the company.

Against that cost the capitalization is thin. Datacurve has raised about $17.7 million. Scale had raised roughly $1.6 billion before Meta bought in, including a [$1 billion Series F](https://techcrunch.com/2024/05/21/data-labeling-startup-scale-ai-raises-1b-as-valuation-doubles-to-13-8b/) in 2024. And the buyers number about five, all of them frontier labs. They need to sign long and pay reliably, because there is no volume market underneath to fall back on.

The company sells ["frontier coding data for training and evaluating LLMs"](https://www.ycombinator.com/companies/datacurve). What it ships is expert-curated coding data, RLHF traces, and repository-wide reinforcement learning environments with unit-test verifiers. DeepSWE is 113 repository tasks in isolated environments with program-based verifiers, published free. Training set and benchmark are one product line, in the company's own words.

Which resolves the one recommendation of mine that will never ship. I asked for the full task materials, the prompts, the hidden tests, the node IDs, so a reader could see what was graded. From my side of the table that is a transparency request. From theirs it is a request to publish the goods. The disclosure costs a sentence and I expect it before the next version bump. The task materials cost the business.

## Entanglements

The dark version has already run once, with different names.

In June 2025 Meta [took 49% of Scale AI for $14.3 billion](https://www.cnbc.com/2025/06/12/scale-ai-founder-wang-announces-exit-for-meta-part-of-14-billion-deal.html) and Alexandr Wang left to run its superintelligence lab. Within hours [Google paused projects, OpenAI wound down its relationship, and xAI halted work](https://e.vnexpress.net/news/tech/enterprises/how-meta-s-14-3b-scale-ai-investment-triggers-shake-up-as-google-openai-cut-ties-with-the-startup-founded-by-world-s-youngest-self-made-billionaire-alexandr-wang-4903573.html). Scale publishes SWE-bench Pro.

The tempting inference is that OpenAI tombstoned Pro because Pro belongs to a Meta-aligned vendor, and the timeline refuses it. OpenAI cut ties with Scale in June 2025 and recommended Scale's benchmark anyway in February 2026. Ownership cannot explain a retraction that arrived thirteen months after the ownership changed. Meta-adjacency was no obstacle to pointing the field at Pro while Pro was useful, and no protection once it wasn't. My [ablation post](/an-epistemic-ablation) reached that from the leaderboard; here it arrives again from the cap table.

Datacurve stands in the same structure. It raised a [$15 million Series A in October 2025](https://techcrunch.com/2025/10/09/datacurve-raises-15-million-to-take-on-scaleai/) positioned to take on Scale. The round included participation from employees of DeepMind, Vercel, Anthropic and OpenAI, individuals rather than the companies. Employees of three frontier labs invested in the company that publishes the board, and no sentence anywhere on the benchmark says so.

That position has a name. A supplier who sinks large, relationship-specific cost into a good whose value depends on a handful of counterparties is exposed to [hold-up](https://en.wikipedia.org/wiki/Hold-up_problem). The counterparty can walk and the investment does not transfer. One standard resolution is vertical integration. The supplier gets absorbed by the party it is exposed to. June 2025 was that resolution arriving once already.

So the arc repeats. A frontier lab takes a position in Datacurve, or hires its founders, before the end of 2027. I would rather be wrong about this one.

A reliable customer scales that business. Anchor revenue buys more bounties, more authors, more repositories. That is a larger and more impressive instrument, which is better marketing, which brings the next customer.

The benchmark tasks and the training data come off the same production line, authored by the same bounty pool in the same idioms over similar repositories. I am not claiming shared items. If the sold data and the graded tasks overlapped, the contamination-free claim would be false, which is a larger finding than this one.

Style is enough. The prediction is that a model trained on that pool's output fits tasks written by that pool without having seen any of them. So the lab buying the most inventory is the lab best fitted to the distribution the benchmark draws from.

The prediction has a test that does not require reading anyone's intentions. If a lab becomes Datacurve's anchor customer, its DeepSWE rank should improve relative to its rank on coding benchmarks whose publishers it does not buy from, within two version bumps of the deal. Both leaderboards are public and the comparison is an afternoon's work.

What makes it dark is not corruption. The benchmark's standing will move for reasons that have nothing to do with whether it measures anything. Scale's instrument did not get worse in June 2025 and did not get worse in February 2026 either. Its credibility is downstream of its cap table, and DeepSWE is being built in the same position, by people who so far have fixed every scoring defect I have shown them.

## What would create a buyer

Three things manufacture demand for verification. Statute, which compels it. Liability, where an insurer with a loss on the books wants the check regardless of who runs it. And brand, where an auditor becomes recognizable enough that their verdict circulates the way OpenAI's did.

The third is the one everybody assumes I am chasing, and it is the one I am furthest from. If I win it, it also refutes this post, since a verdict that travels on my name is a [papiermark](/papiermark-credentials) with my face on it.

That leaves statute and liability, both reachable without a name, and the drafting is already underway. [Frontier AI Auditing](https://arxiv.org/abs/2601.11699), from Brundage and forty-odd coauthors in January, proposes four AI Assurance Levels ordered by how much non-public access the auditor is granted. It prices the entry level at $300,000 to $600,000 an engagement, for a market that does not yet exist.

I [answered that paper this month](/assurance-at-the-boundary) ([archived](https://doi.org/10.5281/zenodo.21448999)) with the level below their first: assurance attached to the artifact at the boundary, against a declared standard, under a named signature, adoptable now for an auditor's time. A standard gets written by whoever shows up with a working method while the drafting happens. An insurer's loss creates a buyer with no interest at all in who supplies the evidence. So the checklists and the boundary records are the play, and the individual audits are the working method that has to exist first.

The wheel in this game is the version bump. It is not going to stop turning because somebody proves a task is broken. It stops when somebody has to pay for being wrong.
