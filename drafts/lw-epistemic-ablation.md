# LW/AF debut — the epistemic ablation, adapted

Status: starting cut, 2026-07-20. Adapted from [/an-epistemic-ablation](https://june.kim/an-epistemic-ablation) for the LW/AF audience per the funding funnel (outreach-plan Layer 1; LTFF application follows within days of posting).

Venue rules (non-negotiable, carried from the deleted fold-back doc):
1. Rewrite the final text in your own hand. LW's LLM policy requires added value, verification, and vouching; a pasted draft fails the post's own thesis.
2. Re-verify every number against the audit repo before posting: 728, 15.0%, 11.4%, 27.4% (200), 34.1% (249), 74%, ~30%, the dates.
3. Links in the first comment, body link-light (first-poster hygiene).

Register decisions: keep the grading paragraph (demonstrated/undecidable/plausible) intact, it is the disarming move. No papiermark prophecy, no "audience that doesn't exist yet". The close is the oversight bridge, stated plainly.

---

## Title

I audited SWE-bench Pro a month before OpenAI deprecated it

## Body

In February, OpenAI published criticism of SWE-bench Verified and recommended SWE-bench Pro in its place. The field followed; Pro became the number frontier coding claims cited.

On 9 June I filed a right-of-reply issue on Scale's SWE-bench Pro repository. On 21 June I published a determinacy audit of all 728 public tasks. It proves a floor of 15.0% underdetermined: tasks where passing the hidden test requires recovering a choice the stated problem never pinned, so a pass measures recovery of the author's unstated preference rather than solution of the stated problem. 11.4% of that floor is provable by grep alone, with no model judgment anywhere in the loop. Every label resolves to a committed receipt that re-runs from a cold checkout.

On 8 July, OpenAI audited the same benchmark, estimated ~30% of tasks broken, and retracted its February recommendation.

### The audits agree on the finding

Two of their four failure categories are my taxonomy with the labels filed off. Their "underspecified prompts" are requirements the hidden tests enforce that are, in their words, "not reasonably inferable." That is underdetermination. Their headline example, an OpenLibrary task that fails a model for emitting one leading space where the hidden test demands two, is what my audit calls misdetermined, and I hold receipts for the same genre, down to a task whose test pins a bcrypt digest obtainable only by reading the test.

The numbers are compatible too. Mine is a floor: only what a committed receipt proves. Theirs is an estimate that also counts failure genres outside my audit's scope. A proven floor beneath, a broader estimate above, one conclusion from either direction.

### The ablation

Because the finding agrees, the comparison isolates a single variable: the warrant.

Their method, as published: an unreleased pipeline flagged 200 tasks (27.4%). Five unnamed engineers flagged 249 (34.1%). The two paths agreed on category in 74% of flagged cases, one overlap figure standing in for the inter-rater statistics. The headline sits between the two paths. No per-task labels. No false-positive inspection. No released pipeline. Their example is real, but an example is an anecdote; the number is asserted.

Delete the author from each audit and ask what survives. My receipts do not know my name: a stranger who distrusts me re-runs them from a cold checkout and gets the same 15.0%. Their number cannot be reconstructed from anything they published. To believe ~30%, you trust OpenAI. I did not come away doubting their conclusion. I came away unable to distinguish their conclusion from their authority.

### The timing, graded

My issue sat on Scale's public tracker from 9 June. OpenAI's audit landed 8 July. The top of the Pro leaderboard is Anthropic's number; OpenAI is absent from the top five. The uncharitable reading writes itself: the benchmark was a fine instrument while their models climbed it and a broken one once a rival topped it. Their post is signed, in full, "Author: OpenAI." There is no person to ask.

So grade the episode the way I grade tasks. That their number cannot be reconstructed from what they published: demonstrated. That the timing served their interests: undecidable. That the name, rather than the evidence, did the circulating: plausible, and no more. My suspicion may be unfair to a team that did honest work. Nothing they published can clear them either. An audit without receipts leaves even its defenders empty-handed.

### Why this belongs here

This is a small, fully public instance of the failure mode scalable oversight worries about. An evaluation whose warrant is "trust the evaluator" is an authority claim wearing a denominator, and it fails exactly when it matters: when the evaluator's incentives and the evaluation's conclusion point the same way, no reader can separate diligence from convenience. The defense is structural, and it is cheap. Make the claim carry its own check: per-case receipts, a pinned environment, a verdict a distrusting stranger re-derives. My audit is one person, zero privileged access, a few dollars of compute, and it survives deletion of its author. The version from a frontier lab with every resource needed to ship receipts, published the same month, does not.

The same distinction runs one level down, from audits of benchmarks to models' reports about their own behavior, which is where I'm taking it next: reasoning externalized to a replayable structure at the harness layer, checkable by a party that does not trust the author. If a benchmark audit can be priced in receipts, so can an agent's claim that its patch is correct.

When the next benchmark recommendation or retraction circulates, run the one-line version of this post on it: delete the author, see what survives.

## First comment (links)

- The determinacy audit: https://june.kim/a-determinacy-audit-of-swebench-pro
- Audit repo, every receipt: https://github.com/kimjune01/swebench-pro-audit (archived: https://doi.org/10.5281/zenodo.20738219)
- Right-of-reply issue (9 June): https://github.com/scaleapi/SWE-bench_Pro-os/issues/108
- OpenAI's audit (8 July): https://openai.com/index/separating-signal-from-noise-coding-evaluations/
- The checklist distilled from eight of these audits: https://june.kim/how-to-audit-a-benchmark
- Blog version of this post (more personal register): https://june.kim/an-epistemic-ablation

## Disclosure line (end of body or first comment)

Drafted with LLM assistance and rewritten by hand; I vouch for every claim, and every number traces to the linked receipts.
