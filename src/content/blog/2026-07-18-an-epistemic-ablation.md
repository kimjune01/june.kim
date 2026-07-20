---
variant: post
title: "An Epistemic Ablation"
tags: epistemology, reflecting
---

On 9 June I filed a [right-of-reply issue](https://github.com/scaleapi/SWE-bench_Pro-os/issues/108) on Scale's SWE-bench Pro repository. On 21 June I published [the full audit](/a-determinacy-audit-of-swebench-pro). Across 728 public tasks it proves a floor of [15.0% underdetermined](/a-determinacy-audit-of-swebench-pro#results), including 11.4% [by grep alone](https://github.com/kimjune01/swebench-pro-audit/blob/main/CLAIMS.md). Every label resolves to a [committed receipt](https://github.com/kimjune01/swebench-pro-audit/tree/main/data/cases) a stranger re-runs from a cold checkout. Then I moved on to [the next benchmark](/how-to-audit-a-benchmark).

## Their audit

The news found me in a Subway, sandwich in one hand, scrolling LinkedIn with the other, the announcement wedged between two hiring posts. On 8 July OpenAI [audited the same benchmark](https://openai.com/index/separating-signal-from-noise-coding-evaluations/), estimated ~30% of tasks broken, and retracted the February recommendation that had sent the field there. The first feeling was vindication. The benchmark I audited was the one OpenAI told everyone to use, and now they agreed.

The vindication lasted half the sandwich. I opened the post itself and read it between bites, talking it over with Claude. An unreleased pipeline flagged 200 tasks, 27.4%. Five unnamed engineers flagged 249, 34.1%. The two paths agreed on category in 74% of flagged cases, one overlap figure standing in for the inter-rater statistics. No per-task labels. No false-positive inspection. Between 27.4 and 34.1 sits the headline, ~30%. The outlets repeated it within the week. Their headline example is real, an OpenLibrary task that fails a model for following the prompt, one leading space against the hidden test's two. An example is an anecdote with a screenshot, though. The number is asserted. Nothing they published re-derives it. Whatever their engineers saw, what the reader gets is vibes with a denominator.

## The ablation

So I put the two audits side by side. Two of their four failure categories are [mine](/a-determinacy-audit-of-swebench-pro#standard) with the labels filed off. Their "underspecified prompts" are requirements the hidden tests enforce that are, in their words, "not reasonably inferable." That is underdetermination. Their OpenLibrary case is what my taxonomy calls misdetermined, and my audit holds receipts for the same genre, down to a task whose test [pins a bcrypt digest](https://github.com/kimjune01/swebench-pro-audit/tree/main/data/cases/ansible_20ef733e) obtainable only by reading the test. The numbers are compatible too. Mine is a floor, only what a receipt proves. Theirs is an estimate that also counts [genres outside my determinacy scope](/how-to-audit-a-benchmark). A proven floor beneath, a broader estimate above, one conclusion from either direction.

That agreement makes the ablation clean. The finding cancels out, and what remains is the stance, two ways of asking to be believed. To believe ~30%, you trust OpenAI. To believe 15.0%, you [run it](https://github.com/kimjune01/swebench-pro-audit/blob/main/docs/ADMISSIBILITY-SPEC.md). Delete the author from each and what survives? [My receipts do not know my name](/provenance-has-no-half-life). Their headline rate cannot be reconstructed from anything they published. I did not come away doubting their conclusion. I came away unable to distinguish their conclusion from their authority.

## The timing

Then I noticed the timing. OpenAI recommended Pro in February. My issue sat on Scale's public tracker from 9 June. Their audit landed 8 July. The [top of the leaderboard](https://benchlm.ai/benchmarks/swePro) reads 80.3%, Claude Mythos 5's number, with Claude Fable 5 right behind it. OpenAI is absent from the top five. The uncharitable reading writes itself. The benchmark was a fine instrument while their models climbed it, and a broken one once a rival topped it. So the questions came. Did they run their pipeline before recommending Pro? Did they run it in the spring and hold the result until the standings made it useful? Their post is signed, in full, *Author: OpenAI*. There is no person to ask.

I don't know the answers, and that turned out to be the finding. Unpublished evidence can be withheld, timed, and released when interest aligns. No reader can tell diligence from convenience. My suspicion may be unfair to a team that did honest work. Nothing they published can clear them either. An audit without receipts leaves even its defenders empty-handed.

## The audience

Stepping back, the suspicion stops mattering. They don't need to time anything, because they don't need the epistemic stance at all. The post names no person, the pipeline is unreleased, the labels are unpublished, and none of it slowed the number down. The name was sufficient for circulation; receipts were not required.

Grade the episode the way I grade tasks. That their number cannot be reconstructed from what they published is demonstrated. That the timing served their interests is undecidable. That the name did the circulating is plausible, and no more. And the name has a track record. In February OpenAI discredited [SWE-bench Verified](/swebench-verified) and pointed the field at Pro, and the field went. In July they tombstoned Pro, and the field is going. Recommendation and retraction were believed at the same speed. On what evidence? The name. Their post closes by calling for new benchmarks; on this pattern, expect the replacement to meet the same end. That the audience keeps believing reflects on the audience more than on OpenAI or me.

In May I wrote that [credentials are papiermarks](/papiermark-credentials), notes that circulate on the issuer's name and store nothing. The audience still prices in papiermarks. OpenAI writes for the audience that exists. I write for one that doesn't exist yet.

I'm writing this past midnight, lights off, hunched over a laptop, Claude Code cowriting. The papiermark post ended with a prophecy. The exchange rate hasn't repriced yet. It will. I still believe the direction, but I'm less sure of the timetable. Repricing needs readers who check before believing. Filters that click links before trusting them. Insurers with losses on the line. A field burned by one scandal too many. I don't know which arrives first, or when. I know which currency I'm saving in.
